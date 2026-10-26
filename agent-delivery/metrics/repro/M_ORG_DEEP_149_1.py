#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ORG_DEEP_149_1 · 科研机构重点技术领域布局模型（ORG 域）

需求锚点：bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/科研机构/深度分析.md 序号 149
  「基于技术知识图谱及多源技术数据，对科研机构在重点技术领域的投入情况进行识别与量化分析，
    构建科研机构的技术知识图谱，识别核心技术领域，计算在不同领域的科技综合实力，
    识别需加强投入的关键领域。」输出：布局图谱 / 各领域综合实力评分 / 需加强领域清单 / 可视化报告。

本件口径（可复现、零 SQL）：
  1) 技术领域 = IPC4（国际专利分类小类），按 curated 前缀规则映射到 7 大领域；
     映射规则写在 `_org_deep21_common.IPC_RULES`，规则顺序即优先级。
  2) 投入结构 `share_{i,d}` = 机构 i 在领域 d 的专利件数 / 机构专利总件数。
     数据源 `_snapshots21/patent_ipc4_by_name_20261021.json`（581,585 行，全量扫描产物）。
  3) 综合实力 `S_{i,d}` = 100 × (0.70·share^P + 0.20·share^K + 0.10·1[J=d]) × scale_i，
     scale_i = min(1, log1p(P_i)/log1p(P95))，缺维在剩余维重归一。
       share^P 专利结构份额（IPC4 件数）
       share^K 论文关键词结构份额（面板 kw_top，仅 top5 关键词，弱信号）
       1[J=d]  项目学科是否落在该领域（面板 discipline_top，单值）
  4) 需加强投入 = 城市级前 5 领域中，机构份额为 0（空白）或低于城市份额一半（薄弱）的领域。
     只对「有 ≥5 个 IPC4 小类」的机构出清单，避免把刚起步的机构全判成空白。

硬约束（必须披露）：
  - 专利 IPC4 只覆盖 194/2,074 家（9.35%）；论文关键词 kw_top 只有 9 家（cls 字段仅 100,900 篇
    论文中的小样本可解析），项目学科 53 家；其余机构无布局证据。
  - 专利库无「申请人 × 国别」拆分，国际合作维不可算；库内无技术知识图谱边表，图谱结构不可算。
  - 机构技术标签表（tech_tags）只命中 1 家，不能作为领域来源。
"""
from __future__ import annotations

import json
import math
import os
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _org_deep21_common as OC  # noqa: E402

MID = "M_ORG_DEEP_149_1"


def main() -> None:
    panel = OC.load_panel()
    inst = panel["institutions"]
    ipc = OC.load_ipc_by_name()
    probe = OC.load_probe()

    # ---------------- 1. 领域向量 ----------------
    orgs = []
    dom_pat = Counter()
    ipc_class = Counter()
    method = Counter()
    for x in inst:
        nm = x["name"]
        vec = ipc.get(nm) or {}
        if not vec:
            continue
        p = Counter()
        for k, c in vec.items():
            p[OC.ipc_domain(k)] += c
            ipc_class[k] += c
        kvec = Counter()
        for kw in (x.get("kw_top") or []):
            d = OC.text_domain(kw)
            if d:
                kvec[d] += 1
        jdom = OC.text_domain(x.get("discipline_top") or "")
        orgs.append({"name": nm, "city": x["city"], "org_type": x["org_type"],
                     "inc_year": x.get("inc_year"), "patents": x["patents"],
                     "papers": x["papers"], "projects": x["projects"],
                     "scholars": x["scholars"], "fund": x["project_fund"],
                     "ipc_n": len(vec), "p_vec": dict(p), "k_vec": dict(kvec),
                     "j_dom": jdom, "ipc_top": sorted(vec.items(), key=lambda t: -t[1])[:6]})
        for d, c in p.items():
            dom_pat[d] += c
    for k in ipc_class:
        method["rule_prefix" if any(k.startswith(p) for p, _ in OC.IPC_RULES) else "section"] += 1

    # ---------------- 2. 综合实力 ----------------
    pvals = sorted(o["patents"] for o in orgs)
    p95 = pvals[int(len(pvals) * .95)] if pvals else 1
    lp95 = math.log1p(max(p95, 1))
    pairs = []
    for o in orgs:
        pi = sum(o["p_vec"].values()) or 1
        ki = sum(o["k_vec"].values())
        scale = min(1.0, math.log1p(pi) / lp95) if lp95 else 0.0
        o["scale"] = round(scale, 4)
        o["hhi"] = round(sum((c / pi) ** 2 for c in o["p_vec"].values()), 4)
        o["dom_n"] = sum(1 for c in o["p_vec"].values() if c / pi >= 0.01)
        # 只对「有专利证据」的领域出分：布局的最小证据是 1 件专利，
        # 仅靠论文关键词/项目学科推断的领域单列为潜在领域（见 potential_pairs），不参与综合实力排名。
        for d in OC.DOMAINS:
            if d not in o["p_vec"]:
                continue
            parts, ws = [o["p_vec"][d] / pi], [0.70]
            if ki and d in o["k_vec"]:
                parts.append(o["k_vec"][d] / ki); ws.append(0.20)
            if o["j_dom"] == d:
                parts.append(1.0); ws.append(0.10)
            wsum = sum(ws)
            s = 100 * sum(v * w / wsum for v, w in zip(parts, ws)) * scale
            pairs.append({"name": o["name"], "city": o["city"], "domain": d,
                          "score": round(s, 2),
                          "pat": o["p_vec"].get(d, 0),
                          "share": round(o["p_vec"].get(d, 0) / pi, 4),
                          "n_dims": len(parts)})

    # 潜在领域：无专利但论文关键词/项目学科指向的领域，单列不进排名
    potential = []
    for o in orgs:
        if o["ipc_n"] < 5:
            continue
        for d in set(o["k_vec"]) | ({o["j_dom"]} if o["j_dom"] else set()):
            if d in o["p_vec"]:
                continue
            ev = []
            if d in o["k_vec"]:
                ev.append("论文关键词×%d" % o["k_vec"][d])
            if o["j_dom"] == d:
                ev.append("项目学科")
            if ev:
                potential.append({"name": o["name"], "city": o["city"], "domain": d,
                                  "evidence": "、".join(ev)})

    # 领域内分位（同一领域内跨机构可比）
    by_dom = defaultdict(list)
    for p in pairs:
        by_dom[p["domain"]].append(p)
    for d, rows in by_dom.items():
        pr = OC.pct_rank([r["score"] for r in rows])
        for r, q in zip(rows, pr):
            r["pct_in_domain"] = round(q, 1)

    # ---------------- 3. 需加强投入 ----------------
    city_dom = defaultdict(Counter)
    for o in orgs:
        for d, c in o["p_vec"].items():
            city_dom[o["city"]][d] += c
    city_top = {}
    for city, c in city_dom.items():
        tot = sum(c.values())
        city_top[city] = [(d, v / tot) for d, v in c.most_common(5)] if tot else []

    gaps = []
    for o in orgs:
        if o["ipc_n"] < 5:
            continue
        pi = sum(o["p_vec"].values()) or 1
        top = city_top.get(o["city"]) or []
        miss = []
        for d, cs in top:
            s = o["p_vec"].get(d, 0) / pi
            if s == 0:
                miss.append({"domain": d, "city_share": round(cs, 4), "org_share": 0.0,
                             "kind": "空白"})
            elif s < cs * 0.5:
                miss.append({"domain": d, "city_share": round(cs, 4),
                             "org_share": round(s, 4), "kind": "薄弱"})
        if miss:
            gaps.append({"name": o["name"], "city": o["city"], "ipc_n": o["ipc_n"],
                         "patents": o["patents"], "gaps": miss})
    gap_kinds = Counter(g2["kind"] for g in gaps for g2 in g["gaps"])

    # ---------------- 4. 城市/类型对照 ----------------
    city_stat = {}
    for city in ["深圳市", "广州市", "东莞市", "惠州市"]:
        rows = [o for o in orgs if o["city"] == city]
        c = Counter()
        for o in rows:
            for d, v in o["p_vec"].items():
                c[d] += v
        city_stat[city] = {"orgs_with_ipc": len(rows),
                           "patents": sum(sum(o["p_vec"].values()) for o in rows),
                           "domain_share": OC.share(c),
                           "median_ipc_n": (sorted(o["ipc_n"] for o in rows)[len(rows) // 2]
                                            if rows else None),
                           "hhi_mean": round(sum(o["hhi"] for o in rows) / len(rows), 4) if rows else None}

    org_type_stat = {}
    for t, rows in sorted(((t, [o for o in orgs if o["org_type"] == t])
                           for t in {o["org_type"] for o in orgs}), key=lambda kv: -len(kv[1])):
        c = Counter()
        for o in rows:
            for d, v in o["p_vec"].items():
                c[d] += v
        org_type_stat[t] = {"orgs_with_ipc": len(rows), "domain_share": OC.share(c)}

    # ---------------- 5. 汇总 ----------------
    top_org = sorted(orgs, key=lambda o: (-o["dom_n"], -o["patents"]))
    top_pairs = sorted(pairs, key=lambda p: -p["score"])
    scores = [p["score"] for p in pairs]

    out = {
        "metric_id": MID,
        "metric_name": "科研机构重点技术领域布局模型",
        "domain": "ORG / 科研机构深度分析（序号 149）",
        "formula_owner": "AI-20261022（推测定义，wanghui=false）",
        "support_judgment": "部分支持",
        **OC.base_years(
            [2021, 2022, 2023, 2024, 2025, 2026], [2017, 2018, 2019, 2020],
            "专利为存量口径（库内 apdt_year 仅 2021—2026，2017—2020 零行，不按 0 摊入）；"
            "论文/项目只作结构辅助，不参与基期。2026 为残年（采集至 2026-10），不做趋势外推。"),
        "inputs": {
            "org_roster": "gkx.dwd_research_institute_base_info 2,074 家（快照 org_family_panel_20261021.json）",
            "patent_ipc4": "patent_ipc4_by_name_20261021.json 581,585 行 [ipc4, 申请人, 件数]",
            "paper_keywords": "a25_paper_panel.json cls 字段（100,900 篇）经面板聚合为 kw_top",
            "project_discipline": "gkx.dwd_zh_project.discipline（58,452 行，面板聚合为 discipline_top）",
        },
        "coverage": {
            "institutes": len(inst),
            "orgs_with_ipc": len(orgs),
            "orgs_with_ipc_pct": round(len(orgs) / len(inst), 4),
            "orgs_with_paper_kw": sum(1 for x in inst if x.get("kw_top")),
            "orgs_with_discipline": sum(1 for x in inst if x.get("discipline_top")),
            "orgs_with_tags": panel["coverage"].get("inst_with_tags"),
            "ipc_classes_used": len(ipc_class),
            "ipc_patents_used": sum(ipc_class.values()),
            "org_patents_total": sum(o["patents"] for o in orgs),
            "ipc_universe_classes": 634,
            "mapping_classes": dict(method),
            "mapping_note": "领域映射按 IPC4 前缀规则（curated）+ 部级兜底；规则见 _org_deep21_common.IPC_RULES。",
        },
        "domain_distribution": {
            "patents": dict(dom_pat.most_common()),
            "share": OC.share(dom_pat),
        },
        "strength_dist": OC.dist(scores),
        "top_orgs_by_breadth": [
            {"name": o["name"], "city": o["city"], "org_type": o["org_type"],
             "patents": sum(o["p_vec"].values()), "ipc_n": o["ipc_n"],
             "dom_n": o["dom_n"], "hhi": o["hhi"], "scale": o["scale"],
             "top_ipc": o["ipc_top"][:3],
             "dom_vec": OC.share(Counter(o["p_vec"]))}
            for o in top_org[:20]
        ],
        "top_pairs": top_pairs[:25],
        "potential_domains": {
            "rule": "无专利证据，仅论文关键词或项目学科指向的领域；只对 IPC4 小类 ≥5 的机构单列，不参与综合实力排名。",
            "n": len(potential),
            "examples": sorted(potential, key=lambda p: p["name"])[:20],
        },
        "domain_leaders": {
            d: [{"name": p["name"], "city": p["city"], "score": p["score"],
                 "pat": p["pat"], "share": p["share"]}
                for p in sorted(rows, key=lambda r: -r["score"])[:5]]
            for d, rows in by_dom.items()
        },
        "gaps_need_investment": {
            "rule": "城市前 5 领域中，机构份额为 0（空白）或 < 城市份额×0.5（薄弱）；仅对 IPC4 小类 ≥5 的机构出清单。",
            "orgs_eligible": sum(1 for o in orgs if o["ipc_n"] >= 5),
            "orgs_with_gap": len(gaps),
            "gap_type_count": dict(gap_kinds),
            "examples": sorted(gaps, key=lambda g: -g["patents"])[:20],
        },
        "city_stat": city_stat,
        "org_type_stat": org_type_stat,
        "probes": {
            "chg_head": (probe.get("chg_head") or {}).get("rows"),
            "fin_rows": (probe.get("fin_rows") or {}).get("rows"),
            "note": "机构底册与工商注册库（dwd_org_base_info / 变更记录 / 年报）org_id 与 external_id 均零交集，"
                    "故本件一切布局证据只能来自论文/专利/项目三源。",
        },
        "limits": [
            "IPC4 只覆盖 194/2,074 家（9.35%），布局图谱对 90.65% 的机构无法出图。",
            "论文关键词 kw_top 只有 9 家可用（236 家有论文但关键词解析不出），"
            "share^K 只在 9 家生效，权重压到 0.20；其余机构实际是 0.70 专利份额 + scale。",
            "项目学科 discipline_top 只有 53 家有值，1[J=d] 只在 53 家生效，且单值不能表达跨领域。",
            "无「申请人 × 国别」拆分，国际合作维不可算；无技术知识图谱边表，图谱结构不可算。",
            "技术标签表只命中 1 家机构，不能作为领域来源。",
            "专利库无申请年 × 机构交叉表（star agg 只有存量合计），无法做领域布局的年度演化。",
        ],
    }
    path = OC.write_out(out, MID)
    print("wrote", path)
    print("orgs_with_ipc", len(orgs), "pairs", len(pairs), "dist", out["strength_dist"])
    print("domains", out["domain_distribution"]["share"])
    print("top", [(p["name"], p["domain"], p["score"]) for p in top_pairs[:6]])
    print("gaps", out["gaps_need_investment"]["orgs_with_gap"], out["gaps_need_investment"]["gap_type_count"])


if __name__ == "__main__":
    main()
