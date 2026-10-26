#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M_SYNTH_COLLAB_COMPLETENESS —— 协同网络完整度（有边主体/主体全集）
复用 2026-10-21 已落盘网络事实，不重跑 DB 探针。
运行：python3 code/M_SYNTH_COLLAB_COMPLETENESS.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _collab_c_common as cc

MID = "M_SYNTH_COLLAB_COMPLETENESS"


def main():
    m191, cache, rel, org = cc.load_inputs()
    net = {c: cc.metrics_for(v) for c, v in cc.build_network(m191).items()}

    cov = {c: net[c]["completeness"] for c in cc.CITY_ORDER}
    scores = cc.minmax_scores(cov)
    rank = sorted(cc.CITY_ORDER, key=lambda c: cov[c] or 0, reverse=True)

    cities = {}
    for c in cc.CITY_ORDER:
        x = net[c]
        cities[cc.CITY_SHORT[c]] = {
            "n_nodes": x["n_nodes"],
            "org_nodes": x["org_nodes"],
            "ri_nodes": x["ri_nodes"],
            "scholar_org_nodes": x["scholar_org_nodes"],
            "edges_m": x["m_edges"],
            "covered_nodes_cached": x["covered_nodes_cached"],
            "covered_upper_bound_2m": x["covered_upper_bound_2m"],
            "covered_graph_consistent": x["covered_graph_consistent"],
            "completeness_raw": x["completeness"],
            "completeness_pct": round((x["completeness"] or 0) * 100, 4),
            "completeness_upper_bound_pct": round(
                (x["completeness_upper_bound"] or 0) * 100, 4
            ),
            "dim_score_0_100": scores[c],
        }

    payload = {
        "metric_id": MID,
        "metric_name_zh": "协同网络完整度",
        "grain": "区域（城市）× 统计窗口",
        "formula": "Completeness = n_covered / N × 100；N=企业∪科研机构∪学者所属机构（含无边主体）",
        "compute": {
            "cities": cities,
            "distribution": cc.describe(cov),
            "rank_by_completeness": [cc.CITY_SHORT[c] for c in rank],
            "top": cc.CITY_SHORT[rank[0]],
            "bottom": cc.CITY_SHORT[rank[-1]],
        },
        "consistency_check": {
            "issue": "上游覆盖节点缓存值在有 3 城超过无向简单图 2E 上界（深 128>26、京 236>150、沪 214>126）",
            "cities_over_2m": [
                cc.CITY_SHORT[c] for c in cc.CITY_ORDER if not net[c]["covered_graph_consistent"]
            ],
            "handling": "同时登记缓存值（主口径，沿用 191）与 2E 上界值（可复核下界），差值即覆盖节点口径的不确定区间",
            "note": "沪 214≤2E=126 不成立，故上界列以 min(缓存,2E) 截断；该差异须在甲方口径确认前披露",
        },
        "reuse_evidence": {
            "m191_raw_measures_completeness": {
                c: m191.get("raw_measures", {}).get(c, {}).get("completeness_raw")
                for c in cc.CITY_ORDER
            },
            "m191_dim_scores_completeness": m191.get("dim_scores", {}).get("完整度"),
            "funded_institution_nonnull": m191.get("network_facts", {}).get(
                "funded_institution_nonnull"
            ),
        },
        "baseline": cc.baseline(org),
        "support_judgment": "部分支持",
        "support_reason": (
            "完整度公式可执行、四城覆盖率可算；但①分子侧三类边仅两类可建（合作项目边 funded_institution 全空），"
            "完整度是『两类协同』而非『三类协同』的覆盖率；②分母含无边主体，京沪企业主档 163/16 家、深广 95,600/49,605 家，"
            "分母口径双向失真；③覆盖节点缓存值与 2E 图论上界冲突（3 城超界），且无 window 主体名册表（calc-logic 登记的 "
            "ads.synth_collab_subject 缺口），分子不可复核。按四档口径判部分支持。"
        ),
        "provenance": cc.provenance(m191),
        "note": "完整度分母含孤立节点（算法钉）；N=0 不可算，n=0 且 N>0 记 0；本批四城 N 均远大于 0。",
    }
    path = cc.write_out(MID, payload)
    print("[OK]", path)
    print("coverage%:", {cc.CITY_SHORT[k]: round((v or 0) * 100, 4) for k, v in cov.items()})


if __name__ == "__main__":
    main()
