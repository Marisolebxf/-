#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_SYNTH_DS_23_GRAPH_ALGO_014 发明人—学者桥图算法（20261023，W16-F1）。

口径
----
`dwd_patent_inventors` 69,647 行 / 20,000 件专利（全表 2,939,895 件的 0.6803%），
没有 org_id / 任职单位列；`dwd_scholar` 21,316 行，`dwd_scholar_paper_relation`
1,065,385 行 / 20,015 位学者。姓名桥 = 两侧姓名去空格/标点后精确匹配。

本件做三件事：
  1. 测姓名桥匹配率（783 个交集，发明人侧 2.5167%、学者侧 4.1731%）；
  2. 在发明人合作图上算度分布/连通片/中介（P0/P1/P2 点集显式声明）；
  3. 做同名碰撞敏感性：去掉 35 个高频歧义名后巨片从 2,617 掉到 731，
     据此**拒拟真实桥接人物排名**，只保留「样本图结构」。

快照：code/_snapshots21/inventor_scholar_bridge_20261023.json（由
`_build_inventor_bridge_20261023.py` 生成，本脚本零 SQL）。

输出：code/M_SYNTH_DS_23_GRAPH_ALGO_014_out.json
"""
from __future__ import annotations

import json

import _f1_common as F

MID = "M_SYNTH_DS_23_GRAPH_ALGO_014"
S = F.load("inventor_scholar_bridge_20261023.json")


def main() -> None:
    r = S["rows"]
    b = S["bridge"]
    g = S["graph"]
    p0, p1, p2 = g["P0"], g["P1"], g["P2"]
    cs = S["collision_sensitivity"]

    patent_total = 2939895
    inv_sum_deg = 2 * p0["n_edges"]
    top1_deg = p0["max_degree"]

    derived = {
        "patent_sample_coverage_pct": {
            "value": F.pct(r["inventor_patents"], patent_total),
            "numerator": r["inventor_patents"], "denominator": patent_total,
            "denominator_note": "发明人表覆盖专利件数 / 专利全表行数（20,000 / 2,939,895）",
        },
        "inventor_per_patent": {
            "value": round(r["inventor_rows_used"] / r["inventor_patents"], 4),
            "numerator": r["inventor_rows_used"], "denominator": r["inventor_patents"],
            "denominator_note": "发明人行数 / 覆盖专利件数（69,647 / 20,000）",
        },
        "inventor_name_collapse_pct": {
            "value": F.pct(r["inventor_distinct_raw"] - r["inventor_distinct_norm"], r["inventor_distinct_raw"]),
            "numerator": r["inventor_distinct_raw"] - r["inventor_distinct_norm"],
            "denominator": r["inventor_distinct_raw"],
            "denominator_note": "归一后减少的姓名数 / 原始姓名数（76 / 31,188）",
        },
        "bridge_inventor_side_pct": {
            "value": b["inventor_side_pct"], "numerator": b["intersection_names"],
            "denominator": r["inventor_distinct_norm"],
            "denominator_note": "交集姓名数 / 发明人侧归一姓名数（783 / 31,112）",
        },
        "bridge_scholar_side_pct": {
            "value": b["scholar_side_pct"], "numerator": b["intersection_names"],
            "denominator": r["scholar_names_norm"],
            "denominator_note": "交集姓名数 / 学者侧姓名数（783 / 18,763）",
        },
        "bridge_high_conf_pct": {
            "value": F.pct(b["high_confidence_names"], b["intersection_names"]),
            "numerator": b["high_confidence_names"], "denominator": b["intersection_names"],
            "denominator_note": "双侧词频≤2 的高置信姓名数 / 交集姓名数（412 / 783）",
        },
        "bridge_ambiguous_pct": {
            "value": F.pct(b["ambiguous_names"], b["intersection_names"]),
            "numerator": b["ambiguous_names"], "denominator": b["intersection_names"],
            "denominator_note": "任一侧词频>10 的歧义姓名数 / 交集姓名数（35 / 783）",
        },
        "bridge_edge_share_pct": {
            "value": F.pct(b["bridge_edges"], p1["n_edges"]),
            "numerator": b["bridge_edges"], "denominator": p1["n_edges"],
            "denominator_note": "两端都能落到学者表的合作边数 / P1 边数（459 / 77,296）",
        },
        "p1_share_pct": {
            "value": F.pct(p1["n_nodes"], p0["n_nodes"]),
            "numerator": p1["n_nodes"], "denominator": p0["n_nodes"],
            "denominator_note": "P1 节点数 / P0 节点数（29,463 / 31,188）",
        },
        "p2_node_share_pct": {
            "value": g["P2_share_nodes_pct"], "numerator": p2["n_nodes"], "denominator": p0["n_nodes"],
            "denominator_note": "P2 节点数 / P0 节点数（2,617 / 31,188）",
        },
        "p2_edge_share_pct": {
            "value": g["P2_share_edges_pct"], "numerator": p2["n_edges"], "denominator": p0["n_edges"],
            "denominator_note": "P2 边数 / P0 边数（11,931 / 77,296）",
        },
        "isolate_share_pct": {
            "value": F.pct(p0["isolates"], p0["n_nodes"]),
            "numerator": p0["isolates"], "denominator": p0["n_nodes"],
            "denominator_note": "P0 孤立发明人数 / P0 节点数（1,725 / 31,188）",
        },
        "component_mean_size": {
            "value": round(p1["n_nodes"] / p1["n_components"], 4),
            "numerator": p1["n_nodes"], "denominator": p1["n_components"],
            "denominator_note": "P1 节点数 / P1 连通片数（29,463 / 5,229）",
        },
        "largest_component_share_pct": {
            "value": p1["largest_component_share_pct"], "numerator": p1["largest_component"],
            "denominator": p1["n_nodes"],
            "denominator_note": "P1 最大连通片节点数 / P1 节点数（2,617 / 29,463）",
        },
        "degree_mean": {
            "value": p1["avg_degree"], "numerator": p1["n_edges"] * 2, "denominator": p1["n_nodes"],
            "denominator_note": "P1 平均度 = 2×边数 / 节点数（154,592 / 29,463）",
        },
        "degree_max_share_pct": {
            "value": F.pct(top1_deg, inv_sum_deg), "numerator": top1_deg, "denominator": inv_sum_deg,
            "denominator_note": "P0 最大度 / P0 度总和（67 / 154,592）",
        },
        "degree_gini": {
            "value": p1["gini"], "numerator": "gini", "denominator": "P1 度序列",
            "denominator_note": "P1 度分布 Gini",
        },
        "scholar_relation_coverage_pct": {
            "value": F.pct(r["relation_scholars"], r["scholar_rows"]),
            "numerator": r["relation_scholars"], "denominator": r["scholar_rows"],
            "denominator_note": "有论文关系的学者数 / 学者表行数（20,015 / 21,316）",
        },
        "collision_edge_share_pct": {
            "value": cs["incident_edge_share_pct"], "numerator": "incident edges",
            "denominator": p1["n_edges"],
            "denominator_note": "与 35 个歧义名相连的边数 / P1 边数",
        },
        "giant_drop_pct": {
            "value": F.pct(cs["P2_nodes_before"] - cs["P2_nodes_after"], cs["P2_nodes_before"]),
            "numerator": cs["P2_nodes_before"] - cs["P2_nodes_after"],
            "denominator": cs["P2_nodes_before"],
            "denominator_note": "去歧义名后巨片减少的节点数 / 原巨片节点数（1,886 / 2,617）",
        },
        "high_conf_subgraph_density_pct": {
            "value": round(cs["high_conf_subgraph_edges"] /
                           (cs["high_conf_subgraph_nodes"] * (cs["high_conf_subgraph_nodes"] - 1) / 2) * 100, 6),
            "numerator": cs["high_conf_subgraph_edges"],
            "denominator": cs["high_conf_subgraph_nodes"] * (cs["high_conf_subgraph_nodes"] - 1) / 2,
            "denominator_note": "高置信桥子图边数 / 完全图边数（64 / 75,466）",
        },
    }

    payload = {
        "metric_name": "发明人—学者桥图算法",
        "source": S["source"],
        "rows": r,
        "bridge": b,
        "graph": g,
        "top_degree": S["top_degree"],
        "top_betweenness": S["top_betweenness"],
        "collision_sensitivity": cs,
        "point_sets": [
            {"id": "P0", "name": "全图（含孤立点）", "n_nodes": p0["n_nodes"],
             "n_edges": p0["n_edges"], "isolates": p0["isolates"],
             "n_components": p0["n_components"], "density": p0["density"]},
            {"id": "P1", "name": "去孤立（度≥1）", "n_nodes": p1["n_nodes"],
             "n_edges": p1["n_edges"], "isolates": 0,
             "n_components": p1["n_components"], "density": p1["density"]},
            {"id": "P2", "name": "巨连通分量", "n_nodes": p2["n_nodes"],
             "n_edges": p2["n_edges"], "isolates": 0,
             "n_components": 1, "density": p2["density"]},
        ],
        "normalization": {
            "denominator": "n-1",
            "n_by_point_set": {"P0": p0["n_nodes"] - 1, "P1": p1["n_nodes"] - 1, "P2": p2["n_nodes"] - 1},
            "note": "度中心性归一分母为点集 n−1；中介中心性用 networkx normalized=True；"
                    "本件主结构描述用 P1（去孤立），跨片比较只在 P2 内做。",
        },
        "rejected_dimensions": [
            {"dimension": "全量发明人度分布",
             "reason": "dwd_patent_inventors 只有 20,000 件专利（全表 0.6803%），不是全量",
             "replacement": "样本图 P0/P1/P2 结构量，正文一律带「样本」前缀",
             "negative_evidence": "inventor_scholar_bridge_20261023.json → rows.inventor_patents=20,000"},
            {"dimension": "企业—人才边",
             "reason": "发明人表无 org_id / 任职单位列，无法建企业—人才边（P14 未解）",
             "replacement": "只做姓名桥，不做主体桥",
             "negative_evidence": "code/_probe_blocked_f1_20261023.json；PENDING_RULINGS P14"},
            {"dimension": "真实桥接人物排名",
             "reason": "姓名精确匹配会把同名不同人合并；去掉 35 个高频歧义名后巨片从 2,617 掉到 731，"
                       "中介排名不具稳定性",
             "replacement": "只报高置信 412 人的桥接覆盖率，不报人物榜",
             "negative_evidence": "collision_sensitivity.giant_drop_pct"},
            {"dimension": "官方中心性对照",
             "reason": "gkx 无 enterprise_centrality / node_influence",
             "replacement": "自算度/中介，明示无官方标尺",
             "negative_evidence": "code/_probe_blocked_f1_20261023.json"},
        ],
        "caveats": S["caveats"],
        "verdict_kind": "negative_evidence",
        "absence_probe": F.absence_probe(['graph_node', 'node_influence', 'enterprise_centrality']),
        "derived": derived,
        "sources": [
            "code/_snapshots21/inventor_scholar_bridge_20261023.json",
            "code/_build_inventor_bridge_20261023.py",
            "code/_probe_blocked_f1_20261023.json",
            "PENDING_RULINGS_20261023.md P14",
        ],
    }

    F.write_out(MID, payload, support="部分支持", used=[], missing=[],
                note="发明人表只覆盖 20,000 件专利（2021—2024 公开件样本），无年度字段可用；"
                     "本件不做年度趋势，只做样本截面。")
    print(json.dumps({"bridge": b["intersection_names"], "P2": p2["n_nodes"],
                      "giant_after": cs["P2_nodes_after"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
