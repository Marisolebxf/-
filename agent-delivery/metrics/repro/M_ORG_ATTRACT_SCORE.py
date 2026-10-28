#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ORG_ATTRACT_SCORE · 科研机构招引推荐指数

需求原文（《科技专题服务算法库》§1.1.1.1.1.1.1.6.6）明确给了三个维度名：
「围绕学术影响力、科技成果、科研团队实力等核心维度设计评价指标及判断阈值，
  通过综合计算得到衡量科研机构招引价值的推荐指数」→ 本文件严格按这三名落地，
另加一维「招引势能」作为区分度补充（需求未列，属实现细化，已在文中披露）。

四维（缺维在剩余维重归一；≥2 维才出分）：
  A 学术影响力 0.35 = 0.75×pct(论文存量 2016–2023) + 0.25×pct(学者 h 均值)
                       （h 指数仅 29 家有值 → 该机构降为纯论文口径，不补 0）
  S 科技成果   0.35 = pct(log1p(授权专利 + 2×论文 + 项目数))
  T 团队实力   0.30 = pct(学者数 + 5×院士数)（仅 29 家有学者、1 家有院士 → 其余视为未匹配，
                       置 None 后在剩余维重归一，不当 0 分压分）
  R 招引势能   0.15 = 论文 2021–2023 年均 / 2016–2018 年均，增速封顶 [−80%, +300%]

阈值判定（需求要求「设定判断阈值」，故不止给分数还给达标线）：
  综合 ≥70 分 A 档（可入招引候选）/ 50–70 B 档（观察）/ <50 C 档（暂不推荐）；
  单维阈值取样本 P90，逐维给出通过家数。

与同域 M_ORG_DEEP_154_1（同为序号 154「科研机构引入推荐模型」）的区别：
  那件是候选清单模型（1,060 家省内非深机构、含学科契合 Q 与稀缺 S、输出 9 家名单）；
  本件是全体 2,074 家的单值指数（含深圳本地机构、含动量 R、不含学科 Q）。
  两者同属序号 154，属「一需求两实现」，不是两个需求项 —— 已在 out.json 披露。

零 SQL，只读面板。产物 `code/M_ORG_ATTRACT_SCORE_out.json`。
"""
from __future__ import annotations

import json
import math
import os
import re
from collections import Counter

import _org_family_common as C

MID = "M_ORG_ATTRACT_SCORE"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, f"{MID}_out.json")

BASE = ["2016", "2017", "2018"]
LATE = ["2021", "2022", "2023"]


def core_name(n):
    """机构名去括号注、去行政区前缀，用于识别同族（深圳先进院/先进院/中科院深圳先进院）。"""
    n = re.sub(r"\([^()]*\)", "", str(n or ""))
    n = re.sub(r"^(广东省|深圳市|广州市|东莞市|惠州市|中国|国家|中国科学院)", "", n)
    return re.sub(r"(有限责任公司|有限公司)$", "", n).strip()


def same_family(a, b):
    ca, cb = core_name(a), core_name(b)
    if not ca or not cb:
        return False
    if ca in b or cb in a:
        return True
    k = 0
    for x, y in zip(ca, cb):
        if x != y:
            break
        k += 1
    return k >= 6


def quant(vals, q):
    if not vals:
        return None
    v = sorted(vals)
    idx = min(len(v) - 1, max(0, int(round(q * (len(v) - 1)))))
    return v[idx]


def main():
    panel = C.load_panel()
    inst = panel["institutions"]
    cov = panel["coverage"]
    city_of = {i["name"]: i["city"] for i in inst}

    # ---------- 同族伪边识别（仅用于披露，本指标不直接用合著边） ----------
    edge_raw = panel["pairs"]
    n_family = sum(1 for e in edge_raw if same_family(e[0], e[1]))

    # ---------- 各维原始值 ----------
    pool = [i for i in inst if C.signal_count(i) > 0]
    for i in pool:
        i["_S_raw"] = math.log1p(i["patent_grant"] + 2 * i["papers"] + i["projects"])
        i["_A_raw"] = i["papers"]                      # 学术影响力主口径：2016–2023 论文存量
        i["_A_h"] = i["h_mean"]                # 副口径：学者 h 均值（29 家有值）
        # 学者表 21,316 人里只有 147 人可匹配到底册机构 → 匹配不上视为「未匹配」而非「零人才」，
        # 故 0 值置 None（该维在剩余维重归一），不当作实测 0 压分。
        t_raw = i["scholars"] + 5 * i["academicians"]
        i["_T_raw"] = t_raw if t_raw > 0 else None
        vs = [i["papers_year"].get(y) for y in BASE]
        vs = [v for v in vs if v is not None]
        i["_base"] = sum(vs) / len(vs) if vs else None
        vl = [i["papers_year"].get(y) for y in LATE]
        vl = [v for v in vl if v is not None]
        i["_late"] = sum(vl) / len(vl) if vl else None
        if i["_base"] and i["_base"] >= 2.0 and i["_late"] is not None:
            g = (i["_late"] - i["_base"]) / i["_base"]
            i["_R_raw"] = max(-0.8, min(3.0, g))       # 小基数封顶，防 1→10 篇读成 +900%
        else:
            i["_R_raw"] = None

    def pct_map(col):
        vals = [i[col] for i in pool if i.get(col) is not None]
        rk = C.pct_rank(vals)
        m, k = {}, 0
        for i in pool:
            if i.get(col) is not None:
                m[i["name"]] = rk[k]
                k += 1
        return m

    mS = pct_map("_S_raw")
    mAp = pct_map("_A_raw")
    mAh = pct_map("_A_h")
    mT = pct_map("_T_raw")
    mR = pct_map("_R_raw")

    def dims_of(nm):
        """A 维：有 h 指数时 0.75 论文 + 0.25 h，否则纯论文（不补 0）。"""
        a_p, a_h = mAp.get(nm), mAh.get(nm)
        A = None if a_p is None else (0.75 * a_p + 0.25 * a_h if a_h is not None else a_p)
        return {"A": A, "S": mS.get(nm), "T": mT.get(nm), "R": mR.get(nm)}

    W = {"A": 0.35, "S": 0.35, "T": 0.30, "R": 0.15}
    scored = []
    for i in pool:
        nm = i["name"]
        d = dims_of(nm)
        raw, k = C.weighted({x: (d[x], W[x]) for x in W}, None)
        if raw is None or k < 2:
            continue
        # 证据覆盖折减：缺维会让重归一后的均分系统性偏高（2 维机构等于只取自己最好的两维），
        # 故按覆盖维数折减 0.80 + 0.05×k（k=2→0.90，k=3→0.95，k=4→1.00），
        # 使「分高」与「证据足」同向，避免 2 维机构霸榜。
        cov_k = 0.80 + 0.05 * k
        s = raw * cov_k
        # 分档把「证据充分度」写进阈值：A 档要求 ≥3 维（缺维重归一会让 2 维机构虚高，
        # 实测有机构仅 A/S 两维就冲到 98.3，不能与四维齐全者同列 A）。
        if s >= 70 and k >= 3:
            tier, note = "A", "四维证据充分"
        elif s >= 70:
            tier, note = "B", "分数高但仅 2 维证据"
        elif s >= 50:
            tier, note = "B", "中等"
        else:
            tier, note = "C", "偏弱"
        scored.append({
            "name": nm, "city": i["city"], "org_type": i["org_type"],
            "score": s, "score_raw": raw, "coverage_factor": cov_k,
            "tier": tier, "tier_note": note, "dims": k,
            **{f"dim_{x}": (None if d[x] is None else round(d[x], 1)) for x in W},
            "patents": i["patents"], "patent_grant": i["patent_grant"],
            "papers": i["papers"], "projects": i["projects"],
            "project_fund": i["project_fund"], "scholars": i["scholars"],
            "academicians": i["academicians"], "papers_base": i["_base"],
            "papers_late": i["_late"],
            "growth_pct": None if i["_R_raw"] is None else round(i["_R_raw"] * 100, 1),
        })
    scored.sort(key=lambda x: -x["score"])

    # ---------- 单维阈值（P90）与达标家数 ----------
    thr = {}
    for col, label in [("_S_raw", "S 科技成果"), ("_A_raw", "A 学术影响力"),
                       ("_T_raw", "T 团队实力")]:
        vals = [i[col] for i in pool if i.get(col) is not None]
        t = quant(vals, 0.90)
        thr[label] = {"p90_raw": None if t is None else round(t, 3),
                      "n_with_value": len(vals),
                      "n_pass": sum(1 for v in vals if t is not None and v >= t)}

    # ---------- 城市与层级结构 ----------
    city = []
    for c in C.CITY_ORDER:
        sub = [s for s in scored if s["city"] == c]
        city.append({"city": c, "scored": len(sub),
                     "A": sum(1 for s in sub if s["tier"] == "A"),
                     "B": sum(1 for s in sub if s["tier"] == "B"),
                     "mean": round(sum(s["score"] for s in sub) / len(sub), 2) if sub else None})
    dist = C.dist([s["score"] for s in scored])

    # ---------- 权重敏感性 ----------
    def rescore(w):
        out = {}
        for i in pool:
            nm = i["name"]
            d = dims_of(nm)
            s, k = C.weighted({x: (d[x], w[x]) for x in W}, None)
            if s is not None and k >= 2:
                out[nm] = s * (0.80 + 0.05 * k)
        return out

    alt = [("A 偏重", {"A": 0.50, "S": 0.25, "T": 0.15, "R": 0.10}),
           ("S 偏重", {"A": 0.25, "S": 0.50, "T": 0.15, "R": 0.10}),
           ("T 偏重", {"A": 0.25, "S": 0.15, "T": 0.50, "R": 0.10}),
           ("等权", {"A": 0.25, "S": 0.25, "T": 0.25, "R": 0.25})]
    base_map = {s["name"]: s["score"] for s in scored}
    names = list(base_map)
    sens = []
    for label, w in alt:
        alt_map = rescore(w)
        common = [n for n in names if n in alt_map]
        rho = C.spearman([base_map[n] for n in common], [alt_map[n] for n in common])
        t10b = {n for n in sorted(names, key=lambda x: -base_map[x])[:10]}
        t10a = {n for n in sorted(alt_map, key=lambda x: -alt_map[x])[:10]}
        sens.append({"weights": label, "w": w, "spearman": rho,
                     "top10_overlap": len(t10b & t10a)})

    out = {
        "metric_id": MID,
        "metric_name": "科研机构招引推荐指数",
        "support_judgment": "部分支持",
        "generated_from": "code/_snapshots21/org_family_panel_20261021.json",
        "panel_built_at": panel["built_at"],
        "unit": "gkx.dwd_research_institute_base_info 2,074 家（广东四市）",
        "requirement_dims": ["学术影响力", "科技成果", "科研团队实力"],
        "formula": "score = (0.35A + 0.35S + 0.30T + 0.15R 在缺失维重归一) × 证据覆盖折减(0.80+0.05×维数)；≥2 维出分",
        "weights": W,
        "dims_impl": {
            "A": "0.75×pct(论文存量2016–2023) + 0.25×pct(学者 h 均值)；h 缺则纯论文",
            "S": "pct(log1p(授权专利 + 2×论文 + 项目数))",
            "T": "pct(学者数 + 5×院士数)",
            "R": "论文 2021–2023 年均 / 2016–2018 年均，封顶 [−80%,+300%]",
        },
        "base_years_used": BASE + LATE,
        "base_years_missing": ["2019", "2020", "2024"],
        "coverage": cov,
        "name_key": {"rows": 2074, "distinct_names": cov.get("institution_names"),
                     "note": "4 个重名按 org_id 保留 4 行，聚合时按 (name, city) 不合并"},
        "edge": {"raw_pairs": len(edge_raw), "family_pairs": n_family,
                 "note": "合著同族伪边 6 条已识别，本指标不使用边维"},
        "thresholds": thr,
        "tier_rule": "A=分数≥70 且 ≥3 维；B=50–70（含仅 2 维的高分机构）；C=<50",
        "coverage_penalty": {"k2": 0.90, "k3": 0.95, "k4": 1.00,
                             "why": "缺维重归一会让 2 维机构只按自己最好的两维算均分，实测原口径下 2 维机构霸占前 5 名中的 4 席，故加折减"},
        "scored_orgs": len(scored),
        "not_scored_orgs": len(inst) - len(scored),
        "tiers": dict(Counter(s["tier"] for s in scored)),
        "dim_missing": {x: sum(1 for s in scored if s[f"dim_{x}"] is None) for x in W},
        "score_dist": dist,
        "city": city,
        "top": scored[:60],
        "_scores": {x["name"]: round(x["score"], 2) for x in scored},
        "sensitivity": sens,
        "vs_org_deep_154_1": {
            "same": "同一机构底册、同一批信号（专利/论文/项目/学者），同属需求序号 154",
            "diff": "154 件只算 1,060 家省内非深机构、五维含学科契合 Q 与稀缺 S、输出 9 家名单；"
                    "本件算全体 2,074 家（含深圳本地）、四维含动量 R、输出 0–100 单值与 A/B/C 分档",
            "risk": "两件同时上线会出现两个「招引推荐指数」，前端只能挂一个，须先合并口径",
        },
        "gaps": [
            "84.6% 的机构（1,721/2,074）无任何信号，指数只能给「证据不足」不能给低分",
            "学术影响力无被引数：论文表 100,900 行里 18 篇有 cited_by，且 16 篇 cited_by=0",
            "科研团队实力仅 29 家有学者、1 家有院士，T 维对 324 家为空（重归一，不补 0）",
            "项目资助额封顶在 2020 年（2021 年 27 项、2022 年 1 项），不含经费维",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)

    print(f"{MID}: 出分 {len(scored)} / {len(inst)}；分档 {out['tiers']}")
    print(f"  分布 {dist}")
    print(f"  缺维 {out['dim_missing']}")
    print(f"  阈值 {thr}")
    print(f"  同族伪边 {n_family}（原始 {len(edge_raw)}）")
    print("  敏感性:", [(s["weights"], s["spearman"], s["top10_overlap"]) for s in sens])
    print(f"  -> {OUT}")


if __name__ == "__main__":
    main()
