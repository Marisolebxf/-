#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M_SYNTH_COLLAB_OUTPUT_CORR —— 协同—创新产出关联结果
复用 2026-10-21 已落盘网络事实与专利授权存量，不重跑 DB 探针。
运行：python3 code/M_SYNTH_COLLAB_OUTPUT_CORR.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _collab_c_common as cc

import math
import itertools

MID = "M_SYNTH_COLLAB_OUTPUT_CORR"


def _rank(vals):
    """平均秩（处理并列）。"""
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    ranks = [0.0] * len(vals)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def spearman(xs, ys):
    """Spearman rho：秩上的 Pearson，等价于 1-6Σd²/[n(n²-1)]（无并列时）。"""
    n = len(xs)
    if n < 3 or n != len(ys):
        return None
    return cc.pearson(_rank(xs), _rank(ys))


def perm_pvalue(xs, ys, observed, two_sided=True):
    """精确置换检验：穷举 n! 个 Y 排列，返回 |r| >= |r_obs| 的比例。"""
    n = len(xs)
    if n > 8 or observed is None:
        return None
    hits = 0
    total = 0
    for perm in itertools.permutations(ys):
        r = cc.pearson(xs, list(perm))
        if r is None:
            continue
        total += 1
        if two_sided and abs(r) >= abs(observed) - 1e-12:
            hits += 1
    return round(hits / total, 4) if total else None


def self_test():
    """双恒值/退化输入自检：确保相关函数不把零方差误报为 1 或 0。"""
    cases = []
    r1 = cc.pearson([1, 2, 3], [2, 4, 6])
    cases.append({"case": "完全正线性", "r": r1, "pass": abs(r1 - 1.0) < 1e-12})
    r2 = cc.pearson([1, 2, 3], [6, 4, 2])
    cases.append({"case": "完全负线性", "r": r2, "pass": abs(r2 + 1.0) < 1e-12})
    r3 = cc.pearson([5, 5, 5], [1, 2, 3])
    cases.append({"case": "X 恒值（零方差）", "r": r3, "pass": r3 is None})
    r4 = cc.pearson([5, 5, 5], [5, 5, 5])
    cases.append({"case": "X、Y 双恒值", "r": r4, "pass": r4 is None})
    r5 = cc.pearson([1, 2], [1, 2])
    cases.append({"case": "n=2（不可判显著）", "r": r5, "pass": r5 is not None})
    r6 = cc.pearson([1, 2, 3], [1, 2])
    cases.append({"case": "长度不等", "r": r6, "pass": r6 is None})
    return {
        "cases": cases,
        "all_pass": all(c["pass"] for c in cases),
        "note": "演示面造数双恒值时 r 必须返回 None（无定义），不得返回 1.0/0.0；n=2 虽可算出 ±1 但不构成统计证据",
    }


def main():
    m191, cache, rel, org = cc.load_inputs()
    net = {c: cc.metrics_for(v) for c, v in cc.build_network(m191).items()}

    cov = {c: net[c]["completeness"] for c in cc.CITY_ORDER}
    deg = {c: net[c]["deg_avg"] for c in cc.CITY_ORDER}
    dens = {c: net[c]["density"] for c in cc.CITY_ORDER}
    s_cov, s_deg, s_den = (
        cc.minmax_scores(cov),
        cc.minmax_scores(deg),
        cc.minmax_scores(dens),
    )
    index = {c: (s_cov[c] + s_deg[c] + s_den[c]) / 3.0 for c in cc.CITY_ORDER}

    grant = (cache.get("patent", {}) or {}).get("grant_all", {})
    grant = {c: grant.get(c) for c in cc.CITY_ORDER}

    xs_index = [index[c] for c in cc.CITY_ORDER]
    xs_density = [dens[c] for c in cc.CITY_ORDER]
    xs_centrality = [deg[c] for c in cc.CITY_ORDER]
    ys = [grant[c] for c in cc.CITY_ORDER]

    r_index = cc.pearson(xs_index, ys)
    r_density = cc.pearson(xs_density, ys)
    r_centrality = cc.pearson(xs_centrality, ys)
    rho_index = spearman(xs_index, ys)
    rho_density = spearman(xs_density, ys)
    rho_centrality = spearman(xs_centrality, ys)
    st = self_test()

    cities = {}
    for c in cc.CITY_ORDER:
        cities[cc.CITY_SHORT[c]] = {
            "X_index": round(index[c], 4),
            "X_density": dens[c],
            "X_centrality_avg": deg[c],
            "Y_joint_invention_grant_all": grant[c],
        }

    payload = {
        "metric_id": MID,
        "metric_name_zh": "协同—创新产出关联结果",
        "grain": "区域（城市）× 统计年度（交付口径）；本批复用数据仅有单窗，无法展开年度序列",
        "formula": "r_k = Pearson(X_{k,t}, Y_t)，n>=3、双侧方差>0；X∈{Index, Density, Centrality_avg}，Y=联合发明专利授权去重数",
        "compute": {
            "cities": cities,
            "delivery_status": "insufficient",
            "delivery_reason": (
                "王惠口径要求同一区域窗口内按年展开（区域×年序列，n>=3 年）；"
                "本批复用的 191 网络事实为单统计窗快照，无年度 X_{k,t} 序列，"
                "dwd_patent 的 pbdt_year 年度侧面亦未在缓存中落盘。"
                "按口径不得以 4 城截面替代时间序列，故不交付 r。"
            ),
            "diagnostic_cross_section_only": {
                "warning": "仅 4 城截面，n=4；口径明确禁止多区域截面相关，下列 r 不作交付值、不得解释为因果",
                "n": 4,
                "r_index_vs_grant": round(r_index, 4) if r_index is not None else None,
                "r_density_vs_grant": round(r_density, 4) if r_density is not None else None,
                "r_centrality_vs_grant": round(r_centrality, 4) if r_centrality is not None else None,
                "rho_index_vs_grant": round(rho_index, 4) if rho_index is not None else None,
                "rho_density_vs_grant": round(rho_density, 4) if rho_density is not None else None,
                "rho_centrality_vs_grant": round(rho_centrality, 4) if rho_centrality is not None else None,
                "perm_p_index_two_sided": perm_pvalue(xs_index, ys, r_index),
                "perm_p_density_two_sided": perm_pvalue(xs_density, ys, r_density),
                "perm_p_centrality_two_sided": perm_pvalue(xs_centrality, ys, r_centrality),
                "min_achievable_p": 2.0 / math.factorial(4),
                "note": "n=4 时双侧精确置换 p 的下限为 2/4!=0.0833，即使秩完全单调也无法达到 0.05，故截面 r 不具统计显著性",
            },
            "self_test": st,
        },
        "interpretation": {
            "sign": "截面 r 为负",
            "cause": (
                "上海节点分母仅 304（企业主档 16 家）、北京 642（163 家），指数被小分母抬高，"
                "而两地发明专利授权存量分别仅 2,262/4,928 件；深圳节点分母 96,754、指数垫底，"
                "但授权存量 203,246 件。负相关由分母采集缺口与专利归属采集差异共同驱动，"
                "不能读作『协同越低产出越高』。"
            ),
            "same_source_note": "密度/中心度的边含联合专利，与 Y 部分同源；r 偏高只说明结构相关，不构成因果",
        },
        "reuse_evidence": {
            "patent_grant_all": grant,
            "m191_index": m191.get("index_0_100"),
            "m191_raw_measures": m191.get("raw_measures"),
        },
        "baseline": cc.baseline(org),
        "support_judgment": "部分支持",
        "support_reason": (
            "协同侧 X 三件套可由 191 单窗事实算出，产出侧 Y（发明专利授权存量）按城可得；"
            "但①缺区域×年序列，无法按王惠口径组 n>=3 的年样本，交付状态 insufficient；"
            "②合作项目边 0 条使 X 的结构维不完整；③X 与 Y 均受分母/归属采集缺口影响，"
            "4 城截面 r 为负且不可解释。按四档口径判部分支持（有结构、有部分量，但关键年度序列与边维始终不足）。"
        ),
        "provenance": cc.provenance(m191),
        "note": "同源提醒：密度/中心度的联合专利边与 Y 同出 dwd_patent_applicants，二者非独立变量。",
    }
    path = cc.write_out(MID, payload)
    print("[OK]", path)
    print("index:", {cc.CITY_SHORT[k]: round(v, 4) for k, v in index.items()})
    print("grant:", {cc.CITY_SHORT[k]: v for k, v in grant.items()})
    print("r (diagnostic, n=4):", round(r_index, 4), round(r_density, 4), round(r_centrality, 4))
    print("rho (diagnostic, n=4):", round(rho_index, 4), round(rho_density, 4), round(rho_centrality, 4))
    print("perm p:", perm_pvalue(xs_index, ys, r_index), "self_test all_pass:", st["all_pass"])


if __name__ == "__main__":
    main()
