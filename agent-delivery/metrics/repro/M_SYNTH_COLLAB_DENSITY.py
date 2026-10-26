#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M_SYNTH_COLLAB_DENSITY —— 协同网络密度
复用 2026-10-21 已落盘网络事实，不重跑 DB 探针。
运行：python3 code/M_SYNTH_COLLAB_DENSITY.py
"""
import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _collab_c_common as cc

MID = "M_SYNTH_COLLAB_DENSITY"


def main():
    m191, cache, rel, org = cc.load_inputs()
    net = {c: cc.metrics_for(v) for c, v in cc.build_network(m191).items()}

    dens = {c: net[c]["density"] for c in cc.CITY_ORDER}
    scores = cc.minmax_scores(dens)
    rank = sorted(cc.CITY_ORDER, key=lambda c: dens[c] or 0, reverse=True)

    cities = {}
    for c in cc.CITY_ORDER:
        x = net[c]
        cities[cc.CITY_SHORT[c]] = {
            "nodes_n": x["n_nodes"],
            "edges_m": x["m_edges"],
            "possible_edges": x["possible_edges"],
            "density_raw": x["density"],
            "density_sci": f"{x['density']:.4e}" if x["density"] is not None else None,
            "density_log10": round(math.log10(x["density"]), 6) if x["density"] else None,
            "dim_score_0_100": scores[c],
            "edge_mix": {
                "joint_patent": x["e_joint_patent"],
                "coop_project": x["e_coop_project"],
                "talent_flow": x["e_talent_flow"],
            },
        }

    payload = {
        "metric_id": MID,
        "metric_name_zh": "协同网络密度",
        "grain": "区域（城市）× 统计窗口",
        "formula": "rho = 2m / [n(n-1)]；n>=2；m=联合专利边+合作项目边+人才流动边（无向简单图去重）",
        "compute": {
            "cities": cities,
            "distribution": cc.describe(dens),
            "rank_by_density": [cc.CITY_SHORT[c] for c in rank],
            "top": cc.CITY_SHORT[rank[0]],
            "bottom": cc.CITY_SHORT[rank[-1]],
            "span_orders_of_magnitude": round(
                math.log10(max(dens.values()) / min(v for v in dens.values() if v)), 4
            ),
        },
        "sensitivity": {
            "denominator_variants": {
                "full_node_set": {cc.CITY_SHORT[c]: dens[c] for c in cc.CITY_ORDER},
                "covered_subgraph": {
                    cc.CITY_SHORT[c]: (
                        2 * net[c]["m_edges"]
                        / (net[c]["covered_nodes_cached"] * (net[c]["covered_nodes_cached"] - 1))
                        if net[c]["covered_nodes_cached"] > 1 else None
                    )
                    for c in cc.CITY_ORDER
                },
            },
            "statement": "密度对分母（入网主体口径）高度敏感；本表主口径为全量主体集，覆盖子网仅作敏感性对照",
        },
        "reuse_evidence": {
            "m191_raw_measures_density": {
                c: m191.get("raw_measures", {}).get(c, {}).get("density_raw")
                for c in cc.CITY_ORDER
            },
            "m191_dim_scores_density": m191.get("dim_scores", {}).get("密度"),
        },
        "baseline": cc.baseline(org),
        "support_judgment": "部分支持",
        "support_reason": (
            "密度公式可执行、四城原始密度可算（10^-9—10^-3 量级，跨 5.7 个数量级）；但①合作项目边 0 条，"
            "分子只含联合专利与人才流动两类边；②分母为全量主体集，京沪企业主档 163/16 家与深广 95,600/49,605 家不可比，"
            "密度差异主要由分母采集口径驱动；③覆盖节点缓存值与 2E 上界冲突，无法用覆盖子网复核。按四档口径判部分支持。"
        ),
        "provenance": cc.provenance(m191),
        "note": "全图密度与归一化平均点度中心性为同一数学量（2m/[n(n-1)]），两者在本族不可互作独立证据。",
    }
    path = cc.write_out(MID, payload)
    print("[OK]", path)
    print("density:", {cc.CITY_SHORT[k]: f"{v:.4e}" for k, v in dens.items()})


if __name__ == "__main__":
    main()
