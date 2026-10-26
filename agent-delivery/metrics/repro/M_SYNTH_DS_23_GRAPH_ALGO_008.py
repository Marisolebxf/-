#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SYNTH_DS_23_GRAPH_ALGO_008 中介中心性计算与展示。

口径（Brandes，无向、无权、精确）：
  C_B(v) = 2 / ((n-1)(n-2)) * sum_{s!=v!=t} sigma_st(v) / sigma_st
sigma_st 是 s 到 t 的最短路径数，sigma_st(v) 是其中经过 v 的条数。
主点集 = P2 巨型连通分量（15,223 节点 / 36,965 边）。**精确算法，15,223 个源全跑**，
不是抽样近似；另用 k=400 抽样值与精确值做秩相关，量化「抽样要多大 k 才够」。

P0/P1 不计算：那两个点集含 4,186 / 646 个连通分量，Brandes 的归一化分母按全图 n 取，
跨分量的分数不可比。这不是省事，是「算了也不能用」。

零 SQL：读数来自族级共享快照 code/_snapshots21/graph_algo_23_20261023.json。

输出：code/M_SYNTH_DS_23_GRAPH_ALGO_008_out.json
"""
from __future__ import annotations

import json

import _graph_algo_23_common as C

MID = "M_SYNTH_DS_23_GRAPH_ALGO_008"


def concentration(vals):
    """中介中心性的集中度：总量的多少落在前 1% / 前 10% / 前 100 名手里。"""
    v = sorted((x for x in vals.values()), reverse=True)
    tot = sum(v)
    if not tot:
        return {}
    k1 = max(1, len(v) // 100)
    k10 = max(1, len(v) // 10)
    return {
        "total": round(tot, 6),
        "top1pct_n": k1,
        "top1pct_share_pct": round(sum(v[:k1]) / tot * 100, 2),
        "top10pct_n": k10,
        "top10pct_share_pct": round(sum(v[:k10]) / tot * 100, 2),
        "top100_share_pct": round(sum(v[:100]) / tot * 100, 2),
        "median": round(C.quant(v, 0.5), 8),
    }


def main():
    snap = C.load()
    rows = snap["nodes"]
    n2 = snap["graph"]["giant"]["n_nodes"]
    e2 = snap["graph"]["giant"]["n_edges"]
    stats = snap["centrality_stats"]

    betw = {r["name"]: r["c_betw"] for r in rows}
    deg = {r["name"]: r["c_deg"] for r in rows}

    ps_stats = {
        "P2": C.rescale(stats["P2_betweenness"], 100),
        "P3": C.rescale(stats["P3_betweenness"], 100),
        "P4": C.rescale(stats["P4_betweenness"], 100),
    }
    top20 = C.topn(rows, "c_betw", 20, 100, 3)

    sens = {}
    for pid in ("P3", "P4"):
        sub = C.sub_series(snap, pid, "c_betw")
        common = {k: betw[k] for k in sub}
        meta = next(p for p in snap["point_sets"] if p["id"] == pid)
        sens[pid] = {
            "coverage_nodes_pct": round(meta["coverage_nodes"] * 100, 2),
            "n_nodes": meta["n_nodes"],
            "n_edges": meta["n_edges"],
            "spearman_vs_P2": C.spearman(common, sub),
            "top100": C.top100_overlap(betw, sub),
            "max_pct": C.rescale(stats["%s_betweenness" % pid], 100)["max"],
            "zero_share_pct": round(C.rescale(stats["%s_betweenness" % pid], 100)["n_zero"]
                                    / meta["n_nodes"] * 100, 2),
        }

    peer = {}
    p7 = C.HERE / "M_SYNTH_DS_23_GRAPH_ALGO_007_out.json"
    if p7.exists():
        d7 = json.loads(p7.read_text(encoding="utf-8"))
        s7 = d7["results"]["subgraph_sensitivity"]
        peer["007_closeness_subgraph_spearman"] = {
            "P3": s7["P3"]["spearman_vs_P2"], "P4": s7["P4"]["spearman_vs_P2"],
            "note": "同族 007 的紧密中心性在同样两个子图上的秩相关，用于对照「中介中心性对截断最敏感」"}

    zero_n = stats["P2_betweenness"].get("n_zero") or 0
    doc = {
        "metric_id": MID,
        "metric_name": "中介中心性计算与展示",
        "generated_at": "2026-10-23",
        "db": "gkx（三方库 183.240.141.251:3318，只读）；本脚本零 SQL，只读族级共享快照",
        "data_source": snap["source"],
        "formula": ("C_B(v) = 2/((n-1)(n-2)) * sum_{s!=v!=t} sigma_st(v)/sigma_st，"
                    "Brandes 算法，无向、无权、精确"),
        "reporting_unit": ("正文以百分比（x100）报中介中心性：35.123 表示 35.123%，"
                           "即 0.35123。归一化后取值 0—100%，表示「所有最短路对中经过该节点的份额」。"),
        "scope": {
            "main_point_set": "P2 巨型连通分量（15,223 节点 / 36,965 边），15,223 个源全跑",
            "main_reason": ("中介中心性度量「桥」的位置，只在连通分量内有定义；"
                            "P0 含 4,186 个分量、P1 含 646 个，归一化分母跨分量不可比，故不计算"),
            "sensitivity_point_sets": ["P3 度>=5 子图（4,469 节点 / 17,160 边）",
                                       "P4 度>=10 子图（1,573 节点 / 6,963 边）"],
            "not_computed": ["P0 全图", "P1 有边子图"],
            "not_computed_reason": ("P0 含 4,186 个分量、P1 含 646 个，Brandes 分母按全图规模取，"
                                    "跨分量的分数不可比；算出来的数不构成可比结论"),
        },
        "graph": C.graph_block(snap),
        "construction": snap["construction"],
        "point_sets": snap["point_sets"],
        "results": {
            "n_nodes": n2,
            "n_edges": e2,
            "centrality_stats_pct": ps_stats,
            "top20": top20,
            "top1_name": top20[0]["name"],
            "top1_pct": top20[0]["value"],
            "top1_degree": top20[0]["degree"],
            "top1_papers": top20[0]["papers"],
            "top100_type_mix": C.type_mix(rows, "c_betw", 100),
            "type_mix_all": snap["type_mix"]["all"],
            "concentration": concentration(betw),
            "max_raw": round(ps_stats["P2"]["max"] / 100.0, 6),
            "n_zero": zero_n,
            "zero_share_pct": round(zero_n / n2 * 100, 2),
            "n_below_1pct": sum(1 for v in betw.values() if v < 0.01),
            "n_below_1pct_share_pct": round(sum(1 for v in betw.values() if v < 0.01)
                                            / n2 * 100, 2),
            "sample_check": {
                "k": snap["betweenness"]["sample_check_k"],
                "spearman_sample_vs_exact": snap["betweenness"]["spearman_sample_vs_exact"],
                "note": ("用 k=400 抽样近似值与 15,223 源精确值做 Spearman："
                         "系数越接近 1，说明抽样只影响排序尾部；本件正文给出该系数，"
                         "并以此说明「为什么正式口径用精确值而不是抽样」"),
            },
            "spearman_vs_degree": snap["rank_corr"]["degree~betweenness"],
            "spearman_vs_closeness": snap["rank_corr"]["closeness~betweenness"],
            "spearman_vs_pagerank": snap["rank_corr"]["betweenness~pagerank"],
            "top100_overlap_vs_degree": snap["top100_overlap"]["degree~betweenness"],
            "top100_overlap_vs_closeness": snap["top100_overlap"]["closeness~betweenness"],
            "peer_cross_check": peer,
            "subgraph_sensitivity": sens,
        },
        "display_spec": {
            "entry": "图谱页节点属性面板 / 桥梁节点榜",
            "sort": "按中介中心性降序，同分按机构名升序",
            "fields": ["rank", "name", "type", "degree", "papers", "value(%)"],
            "pagination_hint": ("top20 可直接展示；全量 15,223 行见快照 nodes 数组。"
                                "展示必须标注「巨型分量内、精确 Brandes」"),
        },
        "support_judgment": "完全转换支持",
        "support_reason": (
            "两库均无中介中心性结果面（gkx 侧 enterprise_centrality 不存在，见附录 B），"
            "但边表可由 dwd_zh_paper.author_info_list 重建。在 15,223 节点 / 36,965 边的"
            "巨型分量上跑完整 Brandes（15,223 个源、无抽样），算得最高 %.3f%% 的桥节点，"
            "零值节点占比 %.2f%%，并用 k=400 抽样值反证精确值的必要性。结构与数据量都够，"
            "现在即可算出，故判完全转换支持。"
            % (top20[0]["value"], zero_n / n2 * 100)),
        "caveats": [
            "中介中心性是「桥」的位置，不是重要性总量；度很低但连接两个集团的节点会排第一。",
            "精确 Brandes 是 O(V*E)，15,223 源已跑满；换更大语料必须改抽样并重新标口径。",
            "P0/P1 不计算，任何「全图中介中心性」的表述都是错的。",
            "节点未做机构归并，院系级碎片会产生假桥：同一所大学的不同学院之间会被当成两个集团。",
            "边只有论文共著；「桥」是共著意义上的桥，不含供应/合作关系。",
        ],
        "paper_year_dist": snap["papers"]["year"],
        "sources": C.source_list(snap),
    }
    doc["edge_sources"] = C.edge_sources()
    doc.update(C.base_years(snap))
    C.write_out(MID, doc)
    print(json.dumps({"top10": top20[:10], "P2": ps_stats["P2"], "P3": ps_stats["P3"],
                      "conc": doc["results"]["concentration"],
                      "zero": [zero_n, round(zero_n / n2 * 100, 2)],
                      "sample": doc["results"]["sample_check"], "sens": sens},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
