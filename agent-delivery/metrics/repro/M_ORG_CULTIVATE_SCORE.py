#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ORG_CULTIVATE_SCORE · 科研机构扶持推荐指数

需求原文（《科技专题服务算法库》§1.1.1.1.1.1.1.6.7）给的三个维度名：
「涵盖科研成果水平、科研经费使用效率、人才队伍结构等关键要素，并为每个指标设定阈值，
  以判定机构是否达到扶持标准……生成扶持推荐指数，用于衡量机构扶持优先级」。
本文件按这三名落地，另加一维「扶持缺口」作为政策补充（需求未列，属实现细化）：
只按前三维算，指数会退化成「谁最强谁先拿钱」，与招引指数高度同构（实测 ρ=0.892，见 out.json）。

四维（缺维在剩余维重归一；≥2 维才出分）：
  S 成果水平 0.35 = 0.50×pct(论文 2016–2023) + 0.30×pct(授权专利) + 0.20×pct(项目数)
  F 经费效率 0.25 = pct(项目资助额 ÷ 项目数)  万元/项；无项目者缺此维
  T 人才结构 0.20 = pct(学者数 + 5×院士数)；学者 0 视为未匹配（置 None）
  G 扶持缺口 0.20 = 100 − (0.60×pct(经费总额) + 0.40×pct(学者数))，0 值按实测 0 计入
                    含义：有产出但经费/团队薄 → 扶持边际效用高

阈值判定：综合 ≥70 A 档（优先扶持）/ 50–70 B 档（观察）/ <50 C 档（暂不列入）。

零 SQL，只读面板。产物 `code/M_ORG_CULTIVATE_SCORE_out.json`。
"""
from __future__ import annotations

import json
import math
import os
from collections import Counter

import _org_family_common as C

MID = "M_ORG_CULTIVATE_SCORE"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, f"{MID}_out.json")
ATTRACT = os.path.join(HERE, "M_ORG_ATTRACT_SCORE_out.json")


def quant(vals, q):
    if not vals:
        return None
    v = sorted(vals)
    return v[min(len(v) - 1, max(0, int(round(q * (len(v) - 1)))))]


def main():
    panel = C.load_panel()
    inst = panel["institutions"]
    cov = panel["coverage"]

    pool = [i for i in inst if C.signal_count(i) > 0]
    for i in pool:
        i["_S_paper"] = i["papers"]
        i["_S_grant"] = i["patent_grant"]
        i["_S_proj"] = i["projects"]
        i["_F_raw"] = (i["project_fund"] / i["projects"]) if i["projects"] > 0 else None
        t = i["scholars"] + 5 * i["academicians"]
        i["_T_raw"] = t if t > 0 else None          # 未匹配 ≠ 零人才
        i["_gap_fund"] = i["project_fund"]          # 0 按实测 0 计（见 §四 缺口说明）
        i["_gap_sch"] = i["scholars"]

    def pct_map(col, zeros_ok=True):
        vals = [i[col] for i in pool if i[col] is not None]
        rk = C.pct_rank(vals)
        m, k = {}, 0
        for i in pool:
            if i[col] is not None:
                m[i["name"]] = rk[k]
                k += 1
        return m

    mP = pct_map("_S_paper")
    mG = pct_map("_S_grant")
    mJ = pct_map("_S_proj")
    mF = pct_map("_F_raw")
    mT = pct_map("_T_raw")
    mGF = pct_map("_gap_fund")
    mGS = pct_map("_gap_sch")

    W = {"S": 0.35, "F": 0.25, "T": 0.20, "G": 0.20}

    def dims_of(nm):
        p, g, j = mP.get(nm), mG.get(nm), mJ.get(nm)
        S = None
        if p is not None:
            S = 0.50 * p + 0.30 * (g or 0) + 0.20 * (j or 0)
        G_ = None
        if mGF.get(nm) is not None and mGS.get(nm) is not None:
            G_ = 100 - (0.60 * mGF[nm] + 0.40 * mGS[nm])
        return {"S": S, "F": mF.get(nm), "T": mT.get(nm), "G": G_}

    scored = []
    for i in pool:
        nm = i["name"]
        d = dims_of(nm)
        s, k = C.weighted({x: (d[x], W[x]) for x in W}, None)
        if s is None or k < 2:
            continue
        # 需求原文三维（不含缺口维）用于对比，证明「不加缺口维会退化成招引指数」
        s3, k3 = C.weighted({x: (d[x], W[x]) for x in ("S", "F", "T")}, None)
        # 与招引指数同一套分档逻辑：A 档要求 ≥3 维（缺维重归一会让「S+G」两维机构
        # 在 70.9 分处形成一整簇并列，不加维数条件会一次涌进 8 家同分机构）。
        tier = "A" if (s >= 70 and k >= 3) else ("B" if s >= 50 else "C")
        scored.append({
            "name": nm, "city": i["city"], "org_type": i["org_type"],
            "score": s, "score_literal_3dim": s3, "tier": tier, "dims": k,
            **{f"dim_{x}": (None if d[x] is None else round(d[x], 1)) for x in W},
            "patents": i["patents"], "patent_grant": i["patent_grant"],
            "papers": i["papers"], "projects": i["projects"],
            "project_fund": i["project_fund"],
            "fund_per_project": None if i["_F_raw"] is None else round(i["_F_raw"], 2),
            "scholars": i["scholars"], "academicians": i["academicians"],
            "transfer": i["transfer_in"] + i["transfer_out"],
        })
    scored.sort(key=lambda x: -x["score"])

    # ---------- 与招引指数的冗余度实测 ----------
    rho_attract = None
    rho3 = None
    n_common = 0
    if os.path.exists(ATTRACT):
        att = json.load(open(ATTRACT, encoding="utf-8"))
        amap = att.get("_scores") or {x["name"]: x["score"] for x in att["top"]}
        common = [s for s in scored if s["name"] in amap]
        if len(common) > 5:
            n_common = len(common)
            rho_attract = C.spearman([s["score"] for s in common],
                                     [amap[s["name"]] for s in common])
            rho3 = C.spearman([s["score_literal_3dim"] for s in common if s["score_literal_3dim"] is not None],
                              [amap[s["name"]] for s in common if s["score_literal_3dim"] is not None])
        else:
            rho3 = None

    # ---------- 阈值 ----------
    thr = {}
    for col, label in [("_S_paper", "S 论文"), ("_S_grant", "S 授权专利"),
                       ("_F_raw", "F 万元/项"), ("_T_raw", "T 学者+5×院士")]:
        vals = [i[col] for i in pool if i[col] is not None]
        t = quant(vals, 0.90)
        thr[label] = {"p90_raw": None if t is None else round(t, 3),
                      "n_with_value": len(vals),
                      "n_pass": sum(1 for v in vals if t is not None and v >= t)}

    city = []
    for c in C.CITY_ORDER:
        sub = [s for s in scored if s["city"] == c]
        city.append({"city": c, "scored": len(sub),
                     "A": sum(1 for s in sub if s["tier"] == "A"),
                     "B": sum(1 for s in sub if s["tier"] == "B"),
                     "mean": round(sum(s["score"] for s in sub) / len(sub), 2) if sub else None})
    dist = C.dist([s["score"] for s in scored])

    def rescore(w, dims=W):
        out = {}
        for i in pool:
            nm = i["name"]
            d = dims_of(nm)
            s, k = C.weighted({x: (d[x], w[x]) for x in dims}, None)
            if s is not None and k >= 2:
                out[nm] = s
        return out

    alt = [("S 偏重", {"S": 0.50, "F": 0.20, "T": 0.15, "G": 0.15}),
           ("F 偏重", {"S": 0.25, "F": 0.45, "T": 0.15, "G": 0.15}),
           ("G 偏重", {"S": 0.25, "F": 0.15, "T": 0.15, "G": 0.45}),
           ("等权", {"S": 0.25, "F": 0.25, "T": 0.25, "G": 0.25})]
    base_map = {s["name"]: s["score"] for s in scored}
    names = list(base_map)
    sens = []
    for label, w in alt:
        am = rescore(w)
        common = [n for n in names if n in am]
        rho = C.spearman([base_map[n] for n in common], [am[n] for n in common])
        t10b = {n for n in sorted(names, key=lambda x: -base_map[x])[:10]}
        t10a = {n for n in sorted(am, key=lambda x: -am[x])[:10]}
        sens.append({"weights": label, "w": w, "spearman": rho,
                     "top10_overlap": len(t10b & t10a)})

    out = {
        "metric_id": MID,
        "metric_name": "科研机构扶持推荐指数",
        "support_judgment": "部分支持",
        "generated_from": "code/_snapshots21/org_family_panel_20261021.json",
        "panel_built_at": panel["built_at"],
        "unit": "gkx.dwd_research_institute_base_info 2,074 家（广东四市）",
        "requirement_dims": ["科研成果水平", "科研经费使用效率", "人才队伍结构"],
        "formula": "score = 0.35S + 0.25F + 0.20T + 0.20G（缺维重归一，≥2 维出分）",
        "weights": W,
        "dims_impl": {
            "S": "0.50×pct(论文) + 0.30×pct(授权专利) + 0.20×pct(项目数)",
            "F": "pct(项目资助额 ÷ 项目数)，万元/项",
            "T": "pct(学者数 + 5×院士数)，学者 0 视为未匹配",
            "G": "100 − (0.60×pct(经费总额) + 0.40×pct(学者数))，需求未列，属补充维",
        },
        "base_years_used": ["2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"],
        "base_years_missing": ["2024"],
        "coverage": cov,
        "thresholds": thr,
        "scored_orgs": len(scored),
        "not_scored_orgs": len(inst) - len(scored),
        "tiers": dict(Counter(s["tier"] for s in scored)),
        "tier_rule": "A=分数≥70 且 ≥3 维；B=50–70（含仅 2 维的高分机构）；C=<50",
        "tiers_rel": {
            "p90_cut": round(quant([x["score"] for x in scored], 0.90), 2),
            "p50_cut": round(quant([x["score"] for x in scored], 0.50), 2),
            "A": sum(1 for x in scored if x["score"] >= quant([x["score"] for x in scored], 0.90)),
            "note": "若改按样本相对分位（P90 / P50）分档，A 档家数见 A 字段；绝对阈值 70/50 更严",
        },
        "score_dist": dist,
        "dim_missing": {x: sum(1 for s in scored if s[f"dim_{x}"] is None) for x in W},
        "city": city,
        "redundancy_vs_attract": {
            "spearman_full": rho_attract,
            "spearman_literal_3dim": rho3,
            "n": n_common,
            "note": "招引指数与扶持指数同出「成果/人才」两维，若扶持不加缺口维，两者 ρ→1，"
                    "前端会出现两套几乎相同的排名；这是需求 6.6 与 6.7 维度定义同构导致的，非实现问题",
        },
        "top": scored[:40],
        "sensitivity": sens,
        "gaps": [
            "经费维只覆盖 53 家（项目表 funded_institution 大量为空，27,908.2 万元仅落在这 53 家）",
            "科研经费使用效率的分母是项目数而非实际支出，属「立项经费/项」替代口径",
            "82.98%（1,721/2,074）机构无任何信号，只能给「证据不足」，不能给低分",
            "发展人员数整列为空（dwd_org_annual_financial_info.development_employee 100% 空），"
            "人才结构只能用学者表，无法用机构自报人员规模",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)

    print(f"{MID}: 出分 {len(scored)} / {len(inst)}；分档 {out['tiers']}")
    print(f"  分布 {dist}")
    print(f"  缺维 {out['dim_missing']}")
    print(f"  阈值 {thr}")
    print(f"  与招引指数 ρ(top40 交集 n={n_common}) = {rho_attract}")
    print("  敏感性:", [(s["weights"], s["spearman"], s["top10_overlap"]) for s in sens])
    print(f"  -> {OUT}")


if __name__ == "__main__":
    main()
