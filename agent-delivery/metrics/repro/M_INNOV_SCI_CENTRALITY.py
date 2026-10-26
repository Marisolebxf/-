#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_SCI_CENTRALITY 科学网络中心性（20261023，W16-F1）。

口径
----
节点 = 中文论文 `author_info_list` 的原始机构串（不做上下级归并）；
边   = 同一篇论文共同署名（无向），边权 = 共同署名篇数；门槛 = 机构全语料 ≥2 篇。
点集 = P0 全图 / P1 去孤立 / P2 巨连通 / P3 度≥5 / P4 度≥10；
中心性主口径 **只在 P2（15,223 节点 / 36,965 边）** 上算，归一化分母为 n−1。

不重算 closeness：直接读 `_snapshots21/graph_algo_23_20261023.json`
（全量 BFS 93.7 s 的结果已落盘，§3.60 明令族内复用）。

负证据：`enterprise_cooperation` 在 gkx 不存在（information_schema 实查），
因此本件只有「论文共著」一种边，不含企业合作关系边；代理口径与影响见
`code/_probe_blocked_f1_20261023.json`。

输出：code/M_INNOV_SCI_CENTRALITY_out.json
"""
from __future__ import annotations

import json
from collections import Counter

import networkx as nx

import _f1_common as F
import _synth21_common as S

MID = "M_INNOV_SCI_CENTRALITY"
SNAP = F.load("graph_algo_23_20261023.json")
NODES = SNAP["nodes"]


def rank_of(field: str, n: int = 20):
    rows = sorted(NODES, key=lambda r: (-r[field], r["name"]))[:n]
    out = []
    for i, r in enumerate(rows, 1):
        out.append({
            "rank": i,
            "name": r["name"],
            "type": r["type"],
            "degree": r["degree"],
            "papers": r["papers"],
            "value": round(r[field], 10),
            "community": r["community"],
        })
    return out


def top20_overlap(a, b) -> dict:
    sa = {r["name"] for r in a}
    sb = {r["name"] for r in b}
    return {"intersection": len(sa & sb), "jaccard": round(len(sa & sb) / len(sa | sb), 4)}


def main() -> None:
    ps = {p["id"]: p for p in SNAP["point_sets"]}
    p0, p1, p2, p3, p4 = (ps[k] for k in ("P0", "P1", "P2", "P3", "P4"))
    n2 = p2["n_nodes"]
    denom = n2 - 1

    top_deg = rank_of("c_deg")
    top_close = rank_of("c_close")
    top_betw = rank_of("c_betw")
    top_pr = rank_of("c_pr")

    # 前 20 的类型结构
    def mix(rows):
        return dict(Counter(r["type"] for r in rows))

    # 度/中心性集中度（P2）
    degs = [r["degree"] for r in NODES]
    prs = sorted((r["c_pr"] for r in NODES), reverse=True)
    top1pct_n = max(1, round(n2 * 0.01))
    top10pct_n = max(1, round(n2 * 0.10))
    sum_deg, sum_pr = sum(degs), sum(prs)
    top10_deg = sum(sorted(degs, reverse=True)[:10])
    top1pct_pr = sum(prs[:top1pct_n])
    top10pct_pr = sum(prs[:top10pct_n])

    meta = S.paper_meta()
    papers_total = meta["n"]
    with_inst = meta["n_with_inst"]
    with_city = meta["n_with_city"]
    inst_universe = SNAP["construction"]["inst_universe"]

    # 核心指标：按 P2 度分布给出归一化分位
    p2stat = SNAP["centrality_stats"]["P2_degree"]

    derived = {
        "p2_node_share_pct": {
            "value": p2["coverage_nodes"] * 100,
            "numerator": p2["n_nodes"], "denominator": p0["n_nodes"],
            "denominator_note": "P2 节点数 / P0 节点数（15,223 / 20,436）",
        },
        "p2_edge_share_pct": {
            "value": p2["coverage_edges"] * 100,
            "numerator": p2["n_edges"], "denominator": p0["n_edges"],
            "denominator_note": "P2 边数 / P0 边数（36,965 / 38,208）",
        },
        "isolate_share_pct": {
            "value": SNAP["components"]["isolate_share"] * 100,
            "numerator": p0["isolates"], "denominator": p0["n_nodes"],
            "denominator_note": "P0 孤立点数 / P0 节点数（3,540 / 20,436）",
        },
        "outside_giant_share_pct": {
            "value": round(100 - p2["coverage_nodes"] * 100, 4),
            "numerator": p0["n_nodes"] - p2["n_nodes"], "denominator": p0["n_nodes"],
            "denominator_note": "P0 中不在 P2 的节点数 / P0 节点数（5,213 / 20,436）",
        },
        "p1_retention_pct": {
            "value": p1["coverage_nodes"] * 100,
            "numerator": p1["n_nodes"], "denominator": p0["n_nodes"],
            "denominator_note": "P1 节点数 / P0 节点数（16,896 / 20,436）",
        },
        "papers_with_inst_pct": {
            "value": F.pct(with_inst, papers_total),
            "numerator": with_inst, "denominator": papers_total,
            "denominator_note": "有机构串的论文数 / 论文总数（100,865 / 100,900）",
        },
        "papers_with_city_pct": {
            "value": F.pct(with_city, papers_total),
            "numerator": with_city, "denominator": papers_total,
            "denominator_note": "可归珠三角城市的论文数 / 论文总数（47,802 / 100,900）",
        },
        "inst_retention_pct": {
            "value": F.pct(p0["n_nodes"], inst_universe),
            "numerator": p0["n_nodes"], "denominator": inst_universe,
            "denominator_note": "入图机构数 / 机构全宇宙（20,436 / 84,320，门槛≥2 篇）",
        },
        "degree_norm_max": {
            "value": p2stat["max"],
            "numerator": p0["max_degree"], "denominator": denom,
            "denominator_note": "P2 最大度 / (P2 节点数−1)（194 / 15,222）",
        },
        "degree_norm_median": {
            "value": p2stat["median"],
            "numerator": 3, "denominator": denom,
            "denominator_note": "P2 度中位数 / (P2 节点数−1)（3 / 15,222）",
        },
        "top10_degree_share_pct": {
            "value": F.pct(top10_deg, sum_deg),
            "numerator": top10_deg, "denominator": sum_deg,
            "denominator_note": "P2 度前 10 名度数和 / P2 度总和（1,290 / 73,930）",
        },
        "top1pct_pagerank_share_pct": {
            "value": F.pct(top1pct_pr, sum_pr),
            "numerator": round(top1pct_pr, 10), "denominator": round(sum_pr, 10),
            "denominator_note": "P2 PageRank 前 1% 节点（152 个）的 PR 之和 / P2 PR 总和（0.0881778602 / 1.000000002）",
        },
        "top10pct_pagerank_share_pct": {
            "value": F.pct(top10pct_pr, sum_pr),
            "numerator": round(top10pct_pr, 10), "denominator": round(sum_pr, 10),
            "denominator_note": "P2 PageRank 前 10% 节点（1,522 个）的 PR 之和 / P2 PR 总和（0.3422023946 / 1.000000002）",
        },
        "degree_gini": {
            "value": SNAP["degree"]["gini_giant"],
            "numerator": "degree_gini", "denominator": "P2 度序列",
            "denominator_note": "P2 度分布的 Gini 系数（0—1，越大越不均）",
        },
        "degree_hhi": {
            "value": SNAP["degree"]["hhi_giant"],
            "numerator": "degree_hhi", "denominator": "P2 度份额",
            "denominator_note": "P2 度份额的 HHI（0—10,000）",
        },
        "closeness_degree_spearman": {
            "value": SNAP["rank_corr"]["degree~closeness"],
            "numerator": "rank_corr.degree~closeness", "denominator": "P2 全节点",
            "denominator_note": "P2 上度与接近中心性的 Spearman 秩相关",
        },
        "betweenness_degree_spearman": {
            "value": SNAP["rank_corr"]["degree~betweenness"],
            "numerator": "rank_corr.degree~betweenness", "denominator": "P2 全节点",
            "denominator_note": "P2 上中介中心性与度的 Spearman 秩相关",
        },
        "pagerank_degree_spearman": {
            "value": SNAP["rank_corr"]["degree~pagerank"],
            "numerator": "rank_corr.degree~pagerank", "denominator": "P2 全节点",
            "denominator_note": "P2 上 PageRank 与度的 Spearman 秩相关",
        },
        "betweenness_zero_share_pct": {
            "value": SNAP["betweenness"]["zero_share_giant"] * 100,
            "numerator": SNAP["betweenness"]["n_zero_giant"], "denominator": n2,
            "denominator_note": "P2 上中介中心性为 0 的节点数 / P2 节点数（5,629 / 15,223）",
        },
        "top20_degree_close_jaccard": {
            "value": top20_overlap(top_deg, top_close)["jaccard"],
            "numerator": top20_overlap(top_deg, top_close)["intersection"], "denominator": 40 - top20_overlap(top_deg, top_close)["intersection"],
            "denominator_note": "度前 20 与接近前 20 的 Jaccard（交集/并集）",
        },
        "top100_degree_close_jaccard": {
            "value": SNAP["top100_overlap"]["degree~closeness"]["jaccard"],
            "numerator": SNAP["top100_overlap"]["degree~closeness"]["top100_intersection"],
            "denominator": 200 - SNAP["top100_overlap"]["degree~closeness"]["top100_intersection"],
            "denominator_note": "度前 100 与接近前 100 的 Jaccard（交集/并集）",
        },
        "top100_degree_betw_jaccard": {
            "value": SNAP["top100_overlap"]["degree~betweenness"]["jaccard"],
            "numerator": SNAP["top100_overlap"]["degree~betweenness"]["top100_intersection"],
            "denominator": 200 - SNAP["top100_overlap"]["degree~betweenness"]["top100_intersection"],
            "denominator_note": "度前 100 与中介前 100 的 Jaccard（交集/并集）",
        },
        "top100_close_betw_jaccard": {
            "value": SNAP["top100_overlap"]["closeness~betweenness"]["jaccard"],
            "numerator": SNAP["top100_overlap"]["closeness~betweenness"]["top100_intersection"],
            "denominator": 200 - SNAP["top100_overlap"]["closeness~betweenness"]["top100_intersection"],
            "denominator_note": "接近前 100 与中介前 100 的 Jaccard（交集/并集）",
        },
        "louvain_community_n": {
            "value": SNAP["communities"]["n_communities"],
            "numerator": "n_communities", "denominator": "P2 节点",
            "denominator_note": "Louvain 社群数（resolution=1.0, seed=20261021, weight）",
        },
        "louvain_modularity": {
            "value": SNAP["communities"]["modularity"],
            "numerator": "modularity", "denominator": "P2 边权",
            "denominator_note": "Louvain 模块度（同一参数下的确定值）",
        },
        "largest_community_share_pct": {
            "value": SNAP["communities"]["largest_share"] * 100,
            "numerator": SNAP["communities"]["sizes_top15"][0], "denominator": n2,
            "denominator_note": "最大社群节点数 / P2 节点数（1,637 / 15,223）",
        },
        "degree_papers_pearson": {
            "value": SNAP["pearson_degree_papers"],
            "numerator": "pearson_degree_papers", "denominator": "P2 全节点",
            "denominator_note": "P2 上度与机构论文数的 Pearson 相关",
        },
        "top20_degree_type_enterprise_pct": {
            "value": F.pct(mix(top_deg).get("企业", 0), 20),
            "numerator": mix(top_deg).get("企业", 0), "denominator": 20,
            "denominator_note": "度前 20 中企业数 / 20",
        },
        "top20_degree_type_univ_pct": {
            "value": F.pct(mix(top_deg).get("高校", 0), 20),
            "numerator": mix(top_deg).get("高校", 0), "denominator": 20,
            "denominator_note": "度前 20 中高校数 / 20",
        },
        "top1_over_top2_papers_ratio": {
            "value": round(top_deg[0]["papers"] / top_deg[1]["papers"], 4),
            "numerator": top_deg[0]["papers"], "denominator": top_deg[1]["papers"],
            "denominator_note": "度榜第 1 名论文数 / 第 2 名论文数（751 / 334）",
        },
        "top1_over_top2_degree_ratio": {
            "value": round(top_deg[0]["degree"] / top_deg[1]["degree"], 4),
            "numerator": top_deg[0]["degree"], "denominator": top_deg[1]["degree"],
            "denominator_note": "度榜第 1 名度 / 第 2 名度（194 / 156）",
        },
        "p2_enterprise_node_share_pct": {
            "value": F.pct(SNAP["type_mix"]["all"]["企业"], n2),
            "numerator": SNAP["type_mix"]["all"]["企业"], "denominator": n2,
            "denominator_note": "P2 企业节点数 / P2 节点数（2,408 / 15,223）",
        },
        "citation_edges_vs_collab_edges_pct": {
            "value": F.pct(SNAP["citation_closure"]["reference_ids_in_panel"], p0["n_edges"]),
            "numerator": SNAP["citation_closure"]["reference_ids_in_panel"], "denominator": p0["n_edges"],
            "denominator_note": "可闭合引用 id 数 / P0 共著边数（165 / 38,208）",
        },
    }

    payload = {
        "metric_name": "科学网络中心性",
        "source": SNAP["source"],
        "graph_definition": SNAP["graph_definition"],
        "params": SNAP["params"],
        "point_sets": SNAP["point_sets"],
        "normalization": {
            "denominator": "n-1",
            "n_by_point_set": {k: ps[k]["n_nodes"] for k in ps},
            "p0_n_minus_1": p0["n_nodes"] - 1,
            "note": "度中心性 = 度 / (点集节点数−1)；接近/中介/PageRank 只在 P2 上算，"
                    "P0/P1 的读数只用于标口径差，不与 P2 混引。",
        },
        "coverage": {
            "papers_total": papers_total,
            "papers_with_inst": with_inst,
            "papers_with_city": with_city,
            "inst_universe": inst_universe,
            "nodes_after_min_papers": p0["n_nodes"],
            "inst_not_in_graph": inst_universe - p0["n_nodes"],
            "min_papers": 2,
            "note": "机构全宇宙 84,320 个原始串，≥2 篇门槛后 20,436 个；"
                    "未归并上下级，同名不同院系会拆成多节点。",
        },
        "type_mix_p2": SNAP["type_mix"]["all"],
        "centrality": {
            "degree": {"definition": "COUNT(DISTINCT 合作邻居)", "field": "degree",
                       "top20": top_deg, "type_mix_top20": mix(top_deg)},
            "closeness": {"definition": "Wasserman-Faust 归一化接近中心性（P2 全量 BFS）",
                          "field": "c_close", "top20": top_close, "type_mix_top20": mix(top_close)},
            "betweenness": {"definition": "Brandes 中介中心性（k=100 采样，normalized=True）",
                           "field": "c_betw", "top20": top_betw, "type_mix_top20": mix(top_betw)},
            "pagerank": {"definition": "PageRank(alpha=0.85, tol=1e-12)",
                         "field": "c_pr", "top20": top_pr, "type_mix_top20": mix(top_pr)},
        },
        "centrality_stats": SNAP["centrality_stats"],
        "distribution": {
            "degree_full": SNAP["degree"]["full"],
            "degree_giant": SNAP["degree"]["giant"],
            "buckets_giant": SNAP["degree"]["buckets_giant"],
            "gini_giant": SNAP["degree"]["gini_giant"],
            "hhi_giant": SNAP["degree"]["hhi_giant"],
        },
        "concentration": {
            "top10_degree_sum": top10_deg,
            "degree_sum": sum_deg,
            "top1pct_n": top1pct_n,
            "top10pct_n": top10pct_n,
            "top1pct_pagerank_sum": round(top1pct_pr, 10),
            "top10pct_pagerank_sum": round(top10pct_pr, 10),
            "pagerank_sum": round(sum_pr, 10),
        },
        "communities": {
            "n": SNAP["communities"]["n_communities"],
            "modularity": SNAP["communities"]["modularity"],
            "sizes_top15": SNAP["communities"]["sizes_top15"],
            "median_size": SNAP["communities"]["median_size"],
            "n_size_ge10": SNAP["communities"]["n_size_ge10"],
            "largest_share_pct": round(SNAP["communities"]["largest_share"] * 100, 4),
        },
        "rank_corr": SNAP["rank_corr"],
        "top100_overlap": SNAP["top100_overlap"],
        "null_model": {
            "reps": SNAP["null_model"]["reps"],
            "observed_modularity": SNAP["communities"]["modularity"],
            "null_modularity_min": min(r["modularity_of_observed_partition"] for r in SNAP["null_model"]["runs"]),
            "null_modularity_max": max(r["modularity_of_observed_partition"] for r in SNAP["null_model"]["runs"]),
            "best_modularity_min": min(r["best_modularity"] for r in SNAP["null_model"]["runs"]),
            "best_modularity_max": max(r["best_modularity"] for r in SNAP["null_model"]["runs"]),
            "best_modularity_mean": SNAP["null_model"]["best_modularity_mean"],
            "observed_partition_on_null_mean": SNAP["null_model"]["observed_partition_on_null_mean"],
            "z_score": SNAP["null_model"]["z_score"],
            "note": "度序列保持的双边交换零模型；观测划分在零模型上的模块度只有 0.12—0.13，"
                    "说明 0.755 的模块度主要来自度序列本身，不能当「真实社群边界」的证据。",
        },
        "cross_metric": {
            "inventor_nodes_014": 31188,
            "note": "M_SYNTH_DS_23_GRAPH_ALGO_014 的发明人节点数，用于说明两件节点对象不同源；"
                    "该数来自 014 产物，不在本件图中。",
        },
        "citation_closure": SNAP["citation_closure"],
        "rejected_dimensions": [
            {"dimension": "企业合作关系边",
             "reason": "gkx 无 enterprise_cooperation（information_schema 实查 0 行）",
             "replacement": "论文共著机构图（dwd_zh_paper 作者机构名归一）作为代理；明示共著≠企业合作",
             "negative_evidence": "code/_probe_blocked_f1_20261023.json → enterprise_cooperation"},
            {"dimension": "引文网络",
             "reason": "引用 id 与本库论文 id 不同源，闭合率 0.0857%（165 / 192,600）",
             "replacement": "不建引文图；只用论文—机构二部图投影算中心性，引文维度拒拟",
             "negative_evidence": "graph_algo_23_20261023.json → citation_closure"},
            {"dimension": "官方中心性标尺校验",
             "reason": "gkx 无 enterprise_centrality / node_influence，无法与官方分值对照",
             "replacement": "自算 Degree/Closeness/Betweenness/PageRank，明示无官方标尺，不做对标结论",
             "negative_evidence": "code/_probe_blocked_f1_20261023.json"},
        ],
        "verdict_kind": "negative_evidence",
        "absence_probe": F.absence_probe(['enterprise_cooperation', 'enterprise_supply_chain', 'node_influence', 'enterprise_centrality', 'graph_edge']),
        "derived": derived,
        "sources": [
            "code/_snapshots21/graph_algo_23_20261023.json",
            "code/_snapshots21/a25_paper_panel.json",
            "code/_collab_graph21.py",
            "code/_probe_blocked_f1_20261023.json",
        ],
    }

    F.write_out(
        MID, payload, support="部分支持",
        used=[], missing=[],
        note="全量截面图（论文年份 1980—2026），不做年度切片；2025/2026 是滞后/残年，"
             "只影响边权，不改变 2024 年前已形成的机构节点集合。",
    )
    print(json.dumps({"p2": [p2["n_nodes"], p2["n_edges"]],
                      "top1": top_deg[0]["name"], "communities": SNAP["communities"]["n_communities"]},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
