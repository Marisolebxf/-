#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M_SYNTH_COLLAB_CENTRALITY —— 协同网络中心度（平均点度中心性）
复用 2026-10-21 已落盘网络事实，不重跑 DB 探针。
运行：python3 code/M_SYNTH_COLLAB_CENTRALITY.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _collab_c_common as cc

MID = "M_SYNTH_COLLAB_CENTRALITY"


def main():
    m191, cache, rel, org = cc.load_inputs()
    net = {c: cc.metrics_for(v) for c, v in cc.build_network(m191).items()}

    deg = {c: net[c]["deg_avg"] for c in cc.CITY_ORDER}
    scores = cc.minmax_scores(deg)
    rank = sorted(cc.CITY_ORDER, key=lambda c: deg[c] or 0, reverse=True)

    cities = {}
    for c in cc.CITY_ORDER:
        x = net[c]
        cities[cc.CITY_SHORT[c]] = {
            "nodes_n": x["n_nodes"],
            "edges_m": x["m_edges"],
            "deg_avg_raw": round(x["deg_avg"], 10),
            "deg_centrality_norm": x["deg_centrality_norm"],
            "density_raw": x["density"],
            "identity_gap_norm_minus_density": abs(
                (x["deg_centrality_norm"] or 0) - (x["density"] or 0)
            ),
            "covered_nodes_cached": x["covered_nodes_cached"],
            "covered_subgraph_avg_deg": (
                round(x["covered_subgraph_avg_deg"], 6)
                if x["covered_subgraph_avg_deg"] is not None else None
            ),
            "dim_score_0_100": scores[c],
        }

    payload = {
        "metric_id": MID,
        "metric_name_zh": "协同网络中心度（平均点度中心性）",
        "grain": "区域（城市）× 统计窗口",
        "formula": "C_avg = (1/n) * sum_i k_i = 2m/n；归一化 C'_avg = C_avg/(n-1) = 2m/[n(n-1)]",
        "compute": {
            "cities": cities,
            "distribution": cc.describe(deg),
            "rank_by_centrality": [cc.CITY_SHORT[c] for c in rank],
            "top": cc.CITY_SHORT[rank[0]],
            "bottom": cc.CITY_SHORT[rank[-1]],
        },
        "identity_check": {
            "statement": "无向简单图上，归一化平均点度中心性恒等于图密度",
            "max_abs_gap": max(v["identity_gap_norm_minus_density"] for v in cities.values()),
            "implication": "均值口径的中心度与密度秩相关=1，不能独立识别枢纽节点；枢纽识别需节点级度清单",
        },
        "reuse_evidence": {
            "m191_raw_measures": m191.get("raw_measures"),
            "m191_dim_scores_centrality": m191.get("dim_scores", {}).get("中心度"),
            "relation_input_edges": rel.get("边"),
            "relation_input_total": rel.get("合计"),
        },
        "baseline": cc.baseline(org),
        "support_judgment": "部分支持",
        "support_reason": (
            "联合专利边（dwd_patent_applicants 28,964 行）与人才流动边（dwd_scholar_work_experience 57,117 行）"
            "可现转，平均点度中心性四城可算；但①合作项目边结构性缺失（dwd_zh_project.funded_institution 58,453 行全空，0 边），"
            "三边并集缺一类；②节点分母失真（京沪企业主档仅 163/16 家，深广全量 95,600/49,605 家），中心度均值由分母口径主导；"
            "③节点级度清单未落盘，覆盖节点缓存值（深 128 > 2E=26）超出图论上界，枢纽节点无法复核。"
            "故按四档口径判部分支持。"
        ),
        "provenance": cc.provenance(m191),
        "note": "维度分值为四城 min-max 归一（与 191 dim_scores 同法）；中心度均值口径沿用王惠 INDEX 子项定义。",
    }
    path = cc.write_out(MID, payload)
    print("[OK]", path)
    print("deg_avg:", {k: round(v, 10) for k, v in deg.items()})
    print("scores:", {cc.CITY_SHORT[k]: v for k, v in scores.items()})


if __name__ == "__main__":
    main()
