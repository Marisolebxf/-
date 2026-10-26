#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TECH_PATH_CENTRALITY —— 深圳 IPC4 技术点图的五维中心性。

口径：深圳单口径（节点=深圳 IPC4 前 4 位 2024 年 ≥100 件；边=同一深圳申请人共现
co≥20 且 Jaccard≥0.05）。全国不参与，本件无 LQ 分母。

零 SQL：全部读 _snapshots21 / _snapshots_gkx21 已落盘缓存。
直接跑：cd code && python3 M_TECH_PATH_CENTRALITY.py
"""
from __future__ import annotations

import json
from datetime import datetime

import _path_graph21 as P

METRIC_ID = "M_TECH_PATH_CENTRALITY"
OUT = P.CODE / f"{METRIC_ID}_out.json"

# 五维：判据阈值（判定口径写在文档 §〇，代码只执行）
GATE = {
    "degree": {"name": "度中心性", "stat": "max/median", "op": ">=", "thr": 3.0},
    "wdegree": {"name": "强度中心性（边权=共现户数）", "stat": "max/min", "op": ">=", "thr": 10.0},
    "betweenness": {"name": "介数中心性", "stat": "tau_threshold", "op": ">=", "thr": 0.80},
    "harmonic": {"name": "调和接近中心性", "stat": "p95/p05", "op": ">=", "thr": 2.0},
    "pagerank": {"name": "加权 PageRank", "stat": "max/min", "op": ">=", "thr": 10.0},
}


def p05(v):
    v = sorted(v)
    return v[int(round(0.05 * (len(v) - 1)))]


def main():
    nodes, seq, cell = P.node_universe()
    g = P.build(nodes)
    adj = g["adj"]
    C = P.all_centralities(g)
    comps = P.components(nodes, adj)
    iso = [x for x in nodes if not adj[x]]

    # ---- 阈值敏感性：边规则 ±50% / 2× ----
    sens = []
    for co_min, jac_min, tag in [(15, 0.04, "放宽 50%"), (20, 0.05, "基准"), (30, 0.07, "收紧 50%"), (40, 0.10, "收紧 100%")]:
        gg = P.build(nodes, co_min, jac_min)
        CC = P.all_centralities(gg)
        sens.append({
            "tag": tag, "co_min": co_min, "jac_min": jac_min, "edges": len(gg["edges"]),
            "tau_degree": round(P.spearman([C["degree"][x] for x in nodes], [CC["degree"][x] for x in nodes]), 4),
            "tau_wdegree": round(P.spearman([C["wdegree"][x] for x in nodes], [CC["wdegree"][x] for x in nodes]), 4),
            "tau_betweenness": round(P.spearman([C["betweenness"][x] for x in nodes], [CC["betweenness"][x] for x in nodes]), 4),
            "tau_harmonic": round(P.spearman([C["harmonic"][x] for x in nodes], [CC["harmonic"][x] for x in nodes]), 4),
            "tau_pagerank": round(P.spearman([C["pagerank"][x] for x in nodes], [CC["pagerank"][x] for x in nodes]), 4),
        })
    base_tau = {k: [r[f"tau_{k}"] for r in sens if r["tag"] != "基准"] for k in GATE}

    # ---- 判档 ----
    deg_v = [C["degree"][x] for x in nodes]
    wd_v = [C["wdegree"][x] for x in nodes]
    bc_v = [C["betweenness"][x] for x in nodes]
    hc_v = [C["harmonic"][x] for x in nodes]
    pr_v = [C["pagerank"][x] for x in nodes]
    med_deg = P.stats(deg_v)["median"] or 1
    med_wd = P.stats(wd_v)["median"] or 1

    # 调和接近中心性在两处测量：全图（含 9 个孤立点，会把 p05 拉到 0.17，虚高区分度）
    # 与巨连通块内（226 个，唯一有意义的比较域）。判档用巨连通块，全图仅作对照。
    giant = comps[0]
    hc_g = sorted([C["harmonic"][x] for x in giant])
    p05_g = hc_g[int(round(0.05 * (len(hc_g) - 1)))]
    p95_g = hc_g[int(round(0.95 * (len(hc_g) - 1)))]
    band = sum(1 for v in hc_g if 0.30 <= v <= 0.51) / len(hc_g)

    measured = {
        "degree": round(max(deg_v) / med_deg, 2),
        "wdegree": round(max(wd_v) / max(1, min([v for v in wd_v if v > 0])), 2),
        "betweenness": round(min(base_tau["betweenness"]), 4),
        "harmonic": round(p95_g / p05_g, 2),
        "pagerank": round(max(pr_v) / min(pr_v), 2),
    }
    gate = []
    for k, cfg in GATE.items():
        m, thr = measured[k], cfg["thr"]
        ok = m >= thr
        verdict = "可用" if ok else ("退化" if k == "harmonic" else "有条件可用")
        reason = {
            "degree": f"max {max(deg_v)} 件 / 中位 {int(med_deg)} 件 = {m} 倍，238 个节点 {len(set(deg_v))} 个不同取值",
            "wdegree": f"最大 {max(wd_v)} / 最小非零 {min([v for v in wd_v if v > 0])} = {m} 倍",
            "betweenness": f"边规则 ±50%/2× 四档重算，与基准 Spearman 最低 {m}（阈值 {thr}）→ 名次不稳",
            "harmonic": f"巨连通块 226 点内 p95 {round(p95_g,4)} / p05 {round(p05_g,4)} = {m} 倍，{round(band*100,1)}% 的节点挤在 0.30—0.51 的 0.21 宽窄带里",
            "pagerank": f"max {round(max(pr_v),5)} / min {round(min(pr_v),5)} = {m} 倍",
        }[k]
        gate.append({"dim": k, "name": cfg["name"], "measured": m, "criterion": f"{cfg['stat']} {cfg['op']} {thr}",
                     "pass": ok, "verdict": verdict, "reason": reason})

    n_ok = sum(1 for x in gate if x["verdict"] == "可用")
    support = "完全转换支持" if n_ok == 5 else ("部分支持" if n_ok >= 2 else "不支持")

    # ---- 排序 / 百分位 ----
    def rank_map(vals):
        order = sorted(vals, key=lambda x: -vals[x])
        return {x: i + 1 for i, x in enumerate(order)}

    ranks = {k: rank_map(v) for k, v in
             [("degree", C["degree"]), ("wdegree", C["wdegree"]), ("betweenness", C["betweenness"]),
              ("harmonic", C["harmonic"]), ("pagerank", C["pagerank"])]}

    rows = []
    for x in nodes:
        rows.append({
            "ipc4": x, "n_2024": seq[x][-1], "n_window": sum(seq[x]),
            "degree": C["degree"][x], "wdegree": C["wdegree"][x],
            "betweenness": round(C["betweenness"][x], 6), "harmonic": round(C["harmonic"][x], 6),
            "pagerank": round(C["pagerank"][x], 6),
            "rank_degree": ranks["degree"][x], "rank_wdegree": ranks["wdegree"][x],
            "rank_betweenness": ranks["betweenness"][x], "rank_harmonic": ranks["harmonic"][x],
            "rank_pagerank": ranks["pagerank"][x],
        })

    top = {}
    for k in ("degree", "wdegree", "betweenness", "harmonic", "pagerank"):
        top[k] = [{"ipc4": r["ipc4"], "v": r[f"{k}" if k != "wdegree" else "wdegree"], "n_2024": r["n_2024"]}
                  for r in sorted(rows, key=lambda r: -r[k])[:10]]

    # 多榜共识：五维里进前 20 的次数（不含退化维）
    use = ["degree", "wdegree", "betweenness", "pagerank"]
    hit = {x: sum(1 for k in use if ranks[k][x] <= 20) for x in nodes}
    consensus = [{"ipc4": x, "n_list": hit[x], "ranks": {k: ranks[k][x] for k in use}}
                 for x in sorted(nodes, key=lambda x: (-hit[x], ranks["pagerank"][x])) if hit[x] >= 3]

    corr = [{"a": a, "b": b, "spearman": round(P.spearman([C[a][x] for x in nodes], [C[b][x] for x in nodes]), 4)}
            for i, a in enumerate(("degree", "wdegree", "betweenness", "harmonic", "pagerank"))
            for b in ("degree", "wdegree", "betweenness", "harmonic", "pagerank") if a < b]

    density = 2 * len(g["edges"]) / (len(nodes) * (len(nodes) - 1))
    out = {
        "metric_id": METRIC_ID,
        "metric_name": "技术路径中心性（深圳 IPC4 技术点图五维中心性）",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": P.SOURCE,
        "caliber": "深圳单口径；全国不参与，无 LQ 分母",
        "support_level": support,
        "support_note": f"五维中 {n_ok} 维判可用（度/强度/PageRank），介数条件可用，调和接近退化",
        "universe": {
            "n_nodes": len(nodes), "n_edges": len(g["edges"]), "density": round(density, 5),
            "n_components": len(comps), "giant_component": len(comps[0]),
            "component_sizes": [len(c) for c in comps], "n_isolated": len(iso), "isolated": iso,
            "n_applicants_with_graph_ipc": g["n_applicants_with_graph_ipc"],
        },
        "graph_params": g["params"],
        "gate": gate,
        "stats": {"degree": P.stats(deg_v), "wdegree": P.stats(wd_v), "betweenness": P.stats(bc_v),
                  "harmonic": P.stats(hc_v), "pagerank": P.stats(pr_v),
                  "harmonic_giant": {"n": len(hc_g), "min": round(hc_g[0], 6), "p05": round(p05_g, 6),
                                     "median": round(hc_g[len(hc_g) // 2], 6), "p95": round(p95_g, 6),
                                     "max": round(hc_g[-1], 6),
                                     "share_in_030_051": round(band, 4),
                                     "p95_over_p05": round(p95_g / p05_g, 4)}},
        "sensitivity": sens,
        "rank_corr": corr,
        "top10": top,
        "consensus": consensus,
        "nodes": rows,
        "base_years_used": [2021, 2022, 2023, 2024],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": "图结构用 2021—2024 四年深圳件累计共现；2025/2026 不入图（2026 为残年）；库内 2017—2020 无专利行，不补零",
        "key_numbers": {
            "bridge_top": top["betweenness"][0]["ipc4"], "bridge_top_v": top["betweenness"][0]["v"],
            "hub_top_degree": top["degree"][0]["ipc4"], "hub_top_degree_v": top["degree"][0]["v"],
            "pr_top": top["pagerank"][0]["ipc4"], "pr_top_v": top["pagerank"][0]["v"],
            "tau_bc_min": min(base_tau["betweenness"]), "tau_pr_min": min(base_tau["pagerank"]),
            "consensus_n": len(consensus),
        },
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("done ->", OUT)
    print(json.dumps({"nodes": len(nodes), "edges": len(g["edges"]), "support": support,
                      "gate": {x["dim"]: [x["measured"], x["verdict"]] for x in gate},
                      "bridge": top["betweenness"][0], "hub": top["degree"][0]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
