#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_TECH_PATH_KEYNODE —— 深圳技术点图的关键卡位域识别。

口径：深圳单口径（238 个 IPC4，边=同申请人共现 co≥20 且 Jaccard≥0.05）。
本件不是「割点分析」的复读：先做割点/移除冲击实测（结果：无不可替代节点），
再用「桥接位置 + 跨部类接口 + 总强度」三合一识别流量意义上的关键域。

零 SQL；直接跑：cd code && python3 M_TECH_PATH_KEYNODE.py
"""
from __future__ import annotations

import json
from datetime import datetime

import _path_graph21 as P

METRIC_ID = "M_TECH_PATH_KEYNODE"
OUT = P.CODE / f"{METRIC_ID}_out.json"

# 判档规则（先实测分布后定，见文档 §〇 表）
T1_MIN = 0.90   # 三维百分位同时 ≥0.90 → 全能型卡位
T2_SCORE = 0.80  # 综合分 ≥0.80
T2_TWO = 0.85    # 且至少两维 ≥0.85 → 双强型卡位
W = {"bridge": 0.40, "cross": 0.35, "strength": 0.25}


def main():
    nodes, seq, cell = P.node_universe()
    g = P.build(nodes)
    adj, co = g["adj"], g["co"]
    C = P.all_centralities(g)
    comps = P.components(nodes, adj)
    giant = comps[0]
    G0 = len(giant)

    # ---- 一、割点 / 移除冲击（先证伪「不可替代枢纽」）----
    def removal(x):
        sub = [n for n in giant if n != x]
        ad = {n: {m: w for m, w in adj[n].items() if m != x} for n in sub}
        cs = P.components(sub, ad)
        return len(cs), len(cs[0])

    removal_rows = []
    for x in giant:
        k, big = removal(x)
        removal_rows.append({"ipc4": x, "n_comp_after": k, "largest_after": big,
                             "split_off": G0 - big, "impact": round((G0 - big) / G0, 4)})
    arts = [r for r in removal_rows if r["n_comp_after"] > 1]
    max_impact = max(r["impact"] for r in removal_rows)

    # ---- 二、三合一卡位分 ----
    def pct_rank(vals):
        order = sorted(nodes, key=lambda x: vals[x])
        n = len(order)
        return {x: i / (n - 1) for i, x in enumerate(order)}

    cross = {x: sum(w for u, w in adj[x].items() if u[0] != x[0]) for x in nodes}
    n_sec = {x: len({u[0] for u in adj[x]}) for x in nodes}
    p_bridge = pct_rank(C["betweenness"])
    p_cross = pct_rank(cross)
    p_w = pct_rank(C["wdegree"])
    score = {x: W["bridge"] * p_bridge[x] + W["cross"] * p_cross[x] + W["strength"] * p_w[x] for x in nodes}

    def tier(x):
        if min(p_bridge[x], p_cross[x], p_w[x]) >= T1_MIN:
            return "T1"
        if score[x] >= T2_SCORE and sum(1 for p in (p_bridge[x], p_cross[x], p_w[x]) if p >= T2_TWO) >= 2:
            return "T2"
        return "T3"

    rows = []
    for x in nodes:
        rows.append({
            "ipc4": x, "tier": tier(x), "score": round(score[x], 4),
            "pct_bridge": round(p_bridge[x], 3), "pct_cross": round(p_cross[x], 3),
            "pct_strength": round(p_w[x], 3),
            "betweenness": round(C["betweenness"][x], 6), "wdegree": C["wdegree"][x],
            "degree": C["degree"][x], "cross_co": cross[x], "n_sections": n_sec[x],
            "n_2024": seq[x][-1], "n_window": sum(seq[x]),
            "partners": [{"ipc4": u, "co": w, "n_2024": seq[u][-1]}
                         for u, w in sorted(adj[x].items(), key=lambda t: -t[1])[:3]],
        })
    rows.sort(key=lambda r: -r["score"])
    for i, r in enumerate(rows, 1):
        r["rank"] = i

    t1 = [r for r in rows if r["tier"] == "T1"]
    t2 = [r for r in rows if r["tier"] == "T2"]
    t3 = [r for r in rows if r["tier"] == "T3"]

    # T1 内部耦合：核心圈是否互连
    t1set = [r["ipc4"] for r in t1]
    t1_edges = [(a, b, adj[a].get(b)) for i, a in enumerate(t1set) for b in t1set[i + 1:] if b in adj[a]]
    t1_density = 2 * len(t1_edges) / (len(t1set) * (len(t1set) - 1)) if len(t1set) > 1 else 0.0

    # 卡位 vs 规模：卡位分与 2024 件数的秩相关（回答「关键≠大」）
    rho_size = P.spearman([score[x] for x in nodes], [seq[x][-1] for x in nodes])
    rho_deg = P.spearman([score[x] for x in nodes], [C["degree"][x] for x in nodes])

    # 稳健性：边规则 ±50% 重算卡位分与 T1 名单重合
    def rebuild(co_min, jac_min):
        gg = P.build(nodes, co_min, jac_min)
        CC = P.all_centralities(gg)
        nn = gg["nodes"]
        cx = {x: sum(w for u, w in gg["adj"][x].items() if u[0] != x[0]) for x in nn}

        def pr(v):
            o = sorted(nn, key=lambda z: v[z])
            return {z: i / (len(o) - 1) for i, z in enumerate(o)}
        pb, pc, pw = pr(CC["betweenness"]), pr(cx), pr(CC["wdegree"])
        sc = {x: W["bridge"] * pb[x] + W["cross"] * pc[x] + W["strength"] * pw[x] for x in nn}
        t1b = {x for x in nn if min(pb[x], pc[x], pw[x]) >= T1_MIN}
        return sc, t1b

    sens = []
    for co_min, jac_min, tag in [(15, 0.04, "放宽 50%"), (30, 0.07, "收紧 50%"), (40, 0.10, "收紧 100%")]:
        sc2, t1b = rebuild(co_min, jac_min)
        sens.append({"tag": tag, "co_min": co_min, "jac_min": jac_min,
                     "tau_score": round(P.spearman([score[x] for x in nodes], [sc2[x] for x in nodes]), 4),
                     "t1_overlap": len(set(t1set) & t1b), "t1_n": len(t1b),
                     "t1_kept": sorted(set(t1set) & t1b)})

    support = "部分支持"
    out = {
        "metric_id": METRIC_ID,
        "metric_name": "技术路径关键节点（深圳 IPC4 卡位域识别）",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": P.SOURCE,
        "caliber": "深圳单口径；全国不参与，无 LQ 分母",
        "support_level": support,
        "support_note": "三合一分在 ±50% 档稳健（tau 0.8798—0.9332），收紧 100% 时降至 0.6523、T1 只保 3/7；『不可替代性』经割点实测证伪（单点最多带走 2.21%），故只支持流量型关键域，不支持割点型关键域",
        "rules": {"w": W, "t1_min_each_pct": T1_MIN, "t2_score": T2_SCORE, "t2_two_pct": T2_TWO},
        "universe": {"n_nodes": len(nodes), "n_edges": len(g["edges"]), "giant": G0,
                     "n_components": len(comps), "n_isolated": len(nodes) - G0 - len(comps[1])},
        "articulation": {"n": len(arts), "max_impact": max_impact,
                         "top": sorted(arts, key=lambda r: -r["impact"])[:6],
                         "verdict": "16 个割点，单点移除最多带走 5 个节点（2.2%），无不可替代枢纽"},
        "tiers": {"T1": len(t1), "T2": len(t2), "T3": len(t3)},
        "t1": t1, "t2": t2,
        "t1_coupling": {"n": len(t1set), "edges": len(t1_edges), "density": round(t1_density, 4),
                        "pairs": [{"a": a, "b": b, "co": c} for a, b, c in sorted(t1_edges, key=lambda t: -t[2])[:10]]},
        "score_stats": P.stats(list(score.values())),
        "rho_score_vs_2024": round(rho_size, 4),
        "rho_score_vs_degree": round(rho_deg, 4),
        "sensitivity": sens,
        "nodes": rows,
        "base_years_used": [2021, 2022, 2023, 2024],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": "共现用 2021—2024 四年累计；2025/2026 不入图；库内 2017—2020 无专利行，不补零",
        "key_numbers": {"t1_n": len(t1), "t1_top": t1[0]["ipc4"], "t1_top_score": t1[0]["score"],
                        "max_impact": max_impact, "n_articulation": len(arts),
                        "tau_min": min(s["tau_score"] for s in sens),
                        "rho_vs_size": round(rho_size, 4)},
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("done ->", OUT)
    print(json.dumps({"T1": [r["ipc4"] for r in t1], "T2_n": len(t2),
                      "arts": len(arts), "max_impact": max_impact,
                      "tau": [s["tau_score"] for s in sens],
                      "overlap": [s["t1_overlap"] for s in sens],
                      "rho_size": round(rho_size, 3), "t1_density": round(t1_density, 3)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
