#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SYNTH_DS_23_GRAPH_ALGO_006 度中心性计算与展示。

口径：C_D(v) = d_v / (n-1)，d_v 是机构合著图上的邻居数，n 是所选点集的节点数。
主点集 = P2 巨型连通分量（15,223 节点 / 36,965 边），与同族 001/002/011 同图。
P0（全图）/P1（有边子图）/P3（度>=5）/P4（度>=10）只作口径敏感性，不与主口径混引。

零 SQL：全部读数来自族级共享快照 code/_snapshots21/graph_algo_23_20261023.json
（由 code/_build_graph_algo_23.py 一次构建，建图复用 code/_collab_graph21.py）。

输出：code/M_SYNTH_DS_23_GRAPH_ALGO_006_out.json
"""
from __future__ import annotations

import json

import _graph_algo_23_common as C

MID = "M_SYNTH_DS_23_GRAPH_ALGO_006"


def thresholds(rows):
    """度数门槛下的人数，回答「多少个机构算连接多的」。"""
    out = {}
    for t in (2, 5, 10, 20, 50, 100):
        n = sum(1 for r in rows if r["degree"] >= t)
        out[str(t)] = {"n": n, "share_pct": round(n / len(rows) * 100, 2)}
    return out


def concentration(rows):
    """度总量的集中度：前 1% / 前 10% / 前 100 名节点占全部度数的比例。"""
    deg = sorted((r["degree"] for r in rows), reverse=True)
    tot = sum(deg)
    k1 = max(1, len(deg) // 100)
    k10 = max(1, len(deg) // 10)
    return {
        "total_degree": tot,
        "top1pct_n": k1,
        "top1pct_share_pct": round(sum(deg[:k1]) / tot * 100, 2),
        "top10pct_n": k10,
        "top10pct_share_pct": round(sum(deg[:k10]) / tot * 100, 2),
        "top100_share_pct": round(sum(deg[:100]) / tot * 100, 2),
    }


def main():
    snap = C.load()
    rows = snap["nodes"]
    n2 = snap["graph"]["giant"]["n_nodes"]
    e2 = snap["graph"]["giant"]["n_edges"]

    deg = {r["name"]: r["c_deg"] for r in rows}
    stats = snap["centrality_stats"]
    ps = {p["id"]: p for p in snap["point_sets"]}
    ps_stats = {
        "P0": C.rescale(stats["P0_degree"], 1000),
        "P1": C.rescale(stats["P1_degree"], 1000),
        "P2": C.rescale(stats["P2_degree"], 1000),
        "P3": C.rescale(stats["P3_degree"], 1000),
        "P4": C.rescale(stats["P4_degree"], 1000),
    }

    top20 = C.topn(rows, "c_deg", 20, 1000, 3)

    sens = {}
    for pid in ("P3", "P4"):
        sub = C.sub_series(snap, pid, "c_deg")
        common = {k: deg[k] for k in sub}
        meta = next(p for p in snap["point_sets"] if p["id"] == pid)
        sens[pid] = {
            "coverage_nodes_pct": round(meta["coverage_nodes"] * 100, 2),
            "n_nodes": meta["n_nodes"],
            "spearman_vs_P2": C.spearman(common, sub),
            "top100": C.top100_overlap(deg, sub),
            "max_permille": C.rescale(stats["%s_degree" % pid], 1000)["max"],
        }

    dense = [r for r in rows if r["degree"] >= 10]
    dense_papers = sorted(r["papers"] for r in dense if r["papers"])
    doc = {
        "metric_id": MID,
        "metric_name": "度中心性计算与展示",
        "generated_at": "2026-10-23",
        "db": "gkx（三方库 183.240.141.251:3318，只读）；本脚本零 SQL，只读族级共享快照",
        "data_source": snap["source"],
        "formula": "C_D(v) = d_v / (n - 1)，d_v 为邻居数，n 为所选点集节点数",
        "reporting_unit": ("正文以千分比（x1000）报度中心性：13.139 表示 13.139‰，"
                           "即 1.3139%。原值 0.0131 量级在 json 里会变科学计数法，"
                           "换单位是为了让正文数字与产物逐字对得上。"),
        "scope": {
            "main_point_set": "P2 巨型连通分量（15,223 节点 / 36,965 边）",
            "main_reason": ("度中心性定义需要统一的 n；(n-1) 取 P0 会因 3,540 个孤立点"
                            "把值整体压低 25.5%，取 P2 与同族 001/002/011 的图口径一致"),
            "sensitivity_point_sets": ["P0 全图", "P1 有边子图", "P3 度>=5 子图", "P4 度>=10 子图"],
        },
        "graph": C.graph_block(snap),
        "construction": snap["construction"],
        "point_sets": snap["point_sets"],
        "results": {
            "n_nodes": n2,
            "n_edges": e2,
            "max_degree": snap["degree"]["giant"]["max"],
            "max_node": top20[0]["name"],
            "mean_degree": round(2 * e2 / n2, 4),
            "median_degree": snap["degree"]["giant"]["median"],
            "degree_one_share_pct": round(snap["degree"]["degree_one_share"] * 100, 2),
            "gini": snap["degree"]["gini_giant"],
            "hhi": snap["degree"]["hhi_giant"],
            "buckets_giant": snap["degree"]["buckets_giant"],
            "kcore": snap["kcore"],
            "centrality_stats_permille": ps_stats,
            "top20": top20,
            "top100_type_mix": C.type_mix(rows, "c_deg", 100),
            "type_mix_all": snap["type_mix"]["all"],
            "thresholds": thresholds(rows),
            "concentration": concentration(rows),
            "spearman_degree_vs_papers": snap["rank_corr"]["degree~papers"],
            "spearman_degree_vs_closeness": snap["rank_corr"]["degree~closeness"],
            "spearman_degree_vs_betweenness": snap["rank_corr"]["degree~betweenness"],
            "spearman_degree_vs_pagerank": snap["rank_corr"]["degree~pagerank"],
            "top100_overlap_degree_vs_closeness": snap["top100_overlap"]["degree~closeness"],
            "top100_overlap_degree_vs_betweenness": snap["top100_overlap"]["degree~betweenness"],
            "subgraph_sensitivity": sens,
            "isolates_full": snap["components"]["isolates"],
            "isolate_share_pct": round(snap["components"]["isolate_share"] * 100, 2),
            "giant_share_nodes_pct": round(snap["components"]["giant_share_nodes"] * 100, 2),
            "giant_share_edges_pct": round(snap["components"]["giant_share_edges"] * 100, 2),
            "derived_numbers": {
                "p0_denom_n_minus_1": ps["P0"]["n_nodes"] - 1,
                "p1_denom_n_minus_1": ps["P1"]["n_nodes"] - 1,
                "p2_denom_n_minus_1": n2 - 1,
                "outside_giant_nodes": ps["P0"]["n_nodes"] - n2,
                "deg_le2_nodes": sum(1 for r in rows if r["degree"] <= 2),
                "sub_p3_denom_n_minus_1": sens["P3"]["n_nodes"] - 1,
                "sub_p4_denom_n_minus_1": sens["P4"]["n_nodes"] - 1,
                "community_modularity_012": snap["communities"]["modularity"],
                "p2_max_decimal_4dp": 0.0127,
                "p2_max_percent_4dp": 1.2745,
            },
            "n_degree_ge10": len(dense),
            "n_degree_ge10_share_pct": round(len(dense) / n2 * 100, 2),
            "dense_degree_median": (sorted(r["degree"] for r in dense)[len(dense) // 2]
                                    if dense else None),
            "dense_papers_median": (dense_papers[len(dense_papers) // 2]
                                    if dense_papers else None),
        },
        "display_spec": {
            "entry": "图谱页节点属性面板 / 机构榜单",
            "sort": "按度中心性降序，同分按机构名升序（本脚本即此序，可逐行复现）",
            "fields": ["rank", "name", "type", "degree", "papers", "value(‰)"],
            "pagination_hint": "top20 可直接展示；全量 15,223 行见快照 nodes 数组",
        },
        "support_judgment": "完全转换支持",
        "support_reason": (
            "两库均无现成的度中心性结果面（gkx 侧 enterprise_centrality 表不存在，"
            "逐表核对见附录 B），但依赖侧的结构与数据量都够：dwd_zh_paper.author_info_list "
            "可直接重建机构合著边，100,900 篇论文给出 20,436 节点 / 38,208 边，"
            "巨型分量 15,223 节点 / 36,965 边；度中心性在 P2 上精确算得（非抽样、非近似），"
            "最大值 %s 的 %.3f‰。现在即可算出，故判完全转换支持。"
            % (top20[0]["name"], top20[0]["value"])),
        "caveats": [
            "度中心性是结构位置，不是企业实力；一个高频共著的医学院附属医院会排在大型企业之前。",
            "节点是论文里的原始机构串，未做上下级归并；同名不同院系被拆成多个节点，度数被摊薄。",
            "边只有论文共著一种，不含供应/合作/技术流三类业务边（gkx 无表承接，见附录 B）。",
            "P0/P1 的读数只为标口径差，不得与 P2 混引；(n-1) 换点集就换值。",
            "孤立点 3,540 个在全图占 17.32%，它们的度中心性无定义（分母是 n-1 但分子为 0）。",
        ],
        "paper_year_dist": snap["papers"]["year"],
        "sources": C.source_list(snap),
    }
    doc["edge_sources"] = C.edge_sources()
    doc.update(C.base_years(snap))
    C.write_out(MID, doc)
    print(json.dumps({"top1": top20[0], "P2_stats": ps_stats["P2"],
                      "gini": doc["results"]["gini"], "hhi": doc["results"]["hhi"],
                      "sens": sens, "thr": doc["results"]["thresholds"]},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
