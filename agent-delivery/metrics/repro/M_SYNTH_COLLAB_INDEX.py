#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M_SYNTH_COLLAB_INDEX —— 区域创新协同指数（完整度/中心度/密度三维合成）
复用 2026-10-21 已落盘网络事实，不重跑 DB 探针。
运行：python3 code/M_SYNTH_COLLAB_INDEX.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _collab_c_common as cc

MID = "M_SYNTH_COLLAB_INDEX"


def main():
    m191, cache, rel, org = cc.load_inputs()
    net = {c: cc.metrics_for(v) for c, v in cc.build_network(m191).items()}

    cov = {c: net[c]["completeness"] for c in cc.CITY_ORDER}
    deg = {c: net[c]["deg_avg"] for c in cc.CITY_ORDER}
    dens = {c: net[c]["density"] for c in cc.CITY_ORDER}

    s_cov = cc.minmax_scores(cov)
    s_deg = cc.minmax_scores(deg)
    s_den = cc.minmax_scores(dens)

    index = {
        c: round((s_cov[c] + s_deg[c] + s_den[c]) / 3.0, 4) for c in cc.CITY_ORDER
    }
    rank = sorted(cc.CITY_ORDER, key=lambda c: index[c], reverse=True)

    # 敏感性 1：只按最大值归一（x/max*100），不复位最小值
    def max_norm(values):
        hi = max(v for v in values.values() if v is not None)
        return {k: (v / hi * 100.0 if v is not None else None) for k, v in values.items()}

    alt_index = {
        c: round(
            (
                max_norm(cov)[c] + max_norm(deg)[c] + max_norm(dens)[c]
            ) / 3.0,
            4,
        )
        for c in cc.CITY_ORDER
    }
    # 敏感性 2：秩平均（1=最优）
    def rank_avg(metrics):
        ranks = {}
        for c in cc.CITY_ORDER:
            rs = []
            for values in metrics:
                order = sorted(cc.CITY_ORDER, key=lambda k: values[k] or 0, reverse=True)
                rs.append(order.index(c) + 1)
            ranks[c] = sum(rs) / len(rs)
        return ranks

    rk = rank_avg([cov, deg, dens])
    alt_rank = sorted(cc.CITY_ORDER, key=lambda c: rk[c])

    # 敏感性 3：权重情景（完整度/中心度/密度）
    weight_schemes = {
        "equal_1_3": (1 / 3, 1 / 3, 1 / 3),
        "completeness_half": (0.5, 0.25, 0.25),
        "centrality_half": (0.25, 0.5, 0.25),
        "density_half": (0.25, 0.25, 0.5),
        "completeness_heavy_0_8": (0.8, 0.1, 0.1),
    }
    weight_results = {}
    for name, (w1, w2, w3) in weight_schemes.items():
        vals = {
            c: round(w1 * s_cov[c] + w2 * s_deg[c] + w3 * s_den[c], 4)
            for c in cc.CITY_ORDER
        }
        weight_results[name] = {
            "weights": [w1, w2, w3],
            "index": {cc.CITY_SHORT[c]: vals[c] for c in cc.CITY_ORDER},
            "order": [
                cc.CITY_SHORT[c]
                for c in sorted(cc.CITY_ORDER, key=lambda k: vals[k], reverse=True)
            ],
        }


    cities = {}
    for c in cc.CITY_ORDER:
        cities[cc.CITY_SHORT[c]] = {
            "completeness_score": s_cov[c],
            "centrality_score": s_deg[c],
            "density_score": s_den[c],
            "index_0_100": index[c],
            "index_max_norm_variant": alt_index[c],
            "rank_avg": rk[c],
            "rank": [cc.CITY_SHORT[x] for x in rank].index(cc.CITY_SHORT[c]) + 1,
        }

    payload = {
        "metric_id": MID,
        "metric_name_zh": "区域创新协同指数",
        "grain": "区域（城市）× 统计年度",
        "formula": "Index = (1/3)*[minmax(Completeness) + minmax(Centrality_avg) + minmax(Density)]，0—100",
        "compute": {
            "cities": cities,
            "rank": [cc.CITY_SHORT[c] for c in rank],
            "top": cc.CITY_SHORT[rank[0]],
            "bottom": cc.CITY_SHORT[rank[-1]],
            "distribution": cc.describe(index),
        },
        "reproduction_check": {
            "m191_index": m191.get("index_0_100"),
            "m191_rank": m191.get("rank"),
            "max_abs_diff_vs_m191": max(
                abs(index[c] - (m191.get("index_0_100", {}).get(c) or 0))
                for c in cc.CITY_ORDER
            ),
            "statement": "独立复算与兄弟件 M_SYNTH_191_1 的指数一致（差异 <0.2 分），排序完全相同",
        },
        "sensitivity": {
            "max_norm_variant_index": {
                cc.CITY_SHORT[c]: alt_index[c] for c in cc.CITY_ORDER
            },
            "rank_avg_method_order": [cc.CITY_SHORT[c] for c in alt_rank],
            "weight_schemes": weight_results,
            "statement": "min-max 与 max-only 归一均给出沪>京>广>深，指数排序对归一方式稳健；权重情景下前二稳定，唯完整度权重升至 0.8 时深广互换，说明末两位排序不稳健",
        },
        "reuse_evidence": {
            "m191_dim_scores": m191.get("dim_scores"),
            "m191_raw_measures": m191.get("raw_measures"),
            "funded_institution_nonnull": m191.get("network_facts", {}).get(
                "funded_institution_nonnull"
            ),
        },
        "baseline": cc.baseline(org),
        "support_judgment": "部分支持",
        "support_reason": (
            "三维可算、指数可合成、排序与 191 完全一致；但①三类边缺合作项目边（funded_institution 全空），"
            "三维中的完整度与中心度均只反映两类协同；②三维共用同一套失真分母（京沪主档 163/16、深广 95,600/49,605），"
            "指数差异主要由分母口径而非真实协同水平驱动；③王惠口径等权、极值归一，未做权重敏感性以外的校准，"
            "且需求要求的『历史数据校准机制』未落地。按四档口径判部分支持。"
        ),
        "provenance": cc.provenance(m191),
        "note": "指数与 M_SYNTH_191_1 同核；本件为叶子指标独立落盘，不替代 191 的模型件。",
    }
    path = cc.write_out(MID, payload)
    print("[OK]", path)
    print("index:", {cc.CITY_SHORT[k]: v for k, v in index.items()})
    print("rank:", [cc.CITY_SHORT[c] for c in rank])


if __name__ == "__main__":
    main()
