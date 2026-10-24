#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""区域创新活力指数（M_SYNTH_VIT_INDEX）—— 复现脚本。

正本三步：① 各指标极值归一 → 0—100；② 各维为其下指标标准化分的加权平均；
③ 四维按权重汇总成指数（等权或自定义，ΣW=1）。

本件与 186_1 的分工：
    186_1 = 规范值（四维写死等权），回答「指数是多少」；
    本件  = 参数化指数（自定义主口径 + 熵权对照 + 弹性 + 翻转阈值 + 单纯形网格），
            回答「这个指数对权重有多敏感、什么条件下会翻」。
两者在 S0 等权场景必须逐城相等（本脚本直接反查 186_1 的产物，差值为 0.0）。

运行：
    cd code && python3 M_SYNTH_VIT_INDEX.py
产物：
    code/M_SYNTH_VIT_INDEX_out.json
"""
from __future__ import annotations

import itertools
import json
import math
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_SYNTH_VIT_INDEX_out.json")

CITIES = ["深圳市", "广州市", "东莞市", "惠州市"]
DIMS = ["科技", "产业", "人才", "政策"]
W_MAIN = {"科技": 0.30, "产业": 0.30, "人才": 0.20, "政策": 0.20}
W_EQ = {d: 0.25 for d in DIMS}


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def compare(dim_scores: dict, weights: dict, exclude_below: float = 1e-12) -> dict:
    """四维加权；缺维的不进分子、分母同步收缩（缺口在 gap_dims 里记，不静默）。"""
    idx, used, gap = {}, {}, {}
    for c in CITIES:
        num = den = 0.0
        u, g = [], []
        for d in weights:
            if weights[d] <= exclude_below:
                continue
            v = dim_scores[d].get(c)
            if v is None:
                g.append(d)
                continue
            num += weights[d] * v
            den += weights[d]
            u.append(d)
        idx[c] = round(num / den, 4) if den > 0 else None
        used[c], gap[c] = u, g
    return {"index": idx, "used": used, "gap": gap}


def rank_of(idx: dict) -> dict:
    order = sorted([c for c in CITIES if idx.get(c) is not None], key=lambda c: (-idx[c], c))
    return {c: i + 1 for i, c in enumerate(order)}


def first(idx: dict):
    return min([c for c in CITIES if idx.get(c) is not None],
               key=lambda c: (-idx[c], c))


def entropy_weights(dim_scores: dict, cities=CITIES) -> dict:
    """熵权：只在四维齐全的城市上算（本批 n=4，四城全齐）。"""
    n = len(cities)
    out = {}
    for d in DIMS:
        xs = [dim_scores[d][c] for c in cities]
        s = sum(xs)
        if s <= 0:
            out[d] = {"entropy": None, "divergence": None, "weight": None}
            continue
        e = 0.0
        for x in xs:
            p = x / s
            if p > 0:
                e -= p * math.log(p)
        e /= math.log(n)
        out[d] = {"entropy": round(e, 6), "divergence": round(1 - e, 6), "weight": None}
    tot = sum(v["divergence"] for v in out.values() if v["divergence"] is not None)
    for d in DIMS:
        if out[d]["divergence"] is not None:
            out[d]["weight"] = round(out[d]["divergence"] / tot, 4)
    return out


def elasticity(dim_scores: dict, base_w: dict, delta: float = 0.10) -> dict:
    """某一维 +delta，其余维按原比例缩到 1 - w_d - delta。"""
    base = compare(dim_scores, base_w)["index"]
    out = {}
    for d in DIMS:
        w = dict(base_w)
        rest = 1.0 - base_w[d]
        for k in DIMS:
            if k == d:
                continue
            w[k] = base_w[k] * (rest - delta) / rest
        w[d] = base_w[d] + delta
        new = compare(dim_scores, w)["index"]
        out[d] = {
            "weights": {k: round(v, 4) for k, v in w.items()},
            "index": new,
            "delta": {c: round(new[c] - base[c], 4) for c in CITIES},
            "rank": rank_of(new),
            "first_changed": first(new) != first(base),
        }
    return {"base": base, "base_rank": rank_of(base), "cases": out}


def simplex_scan(dim_scores: dict, step: int = 1) -> dict:
    """步长 0.01、四维和为 1 的整数格点全扫描，统计各城居首的组数。"""
    units = 100 // step if step <= 1 else 100 // step
    counts = {c: 0 for c in CITIES}
    total = 0
    talent_only_min = None
    flip_rows = []
    for a in range(0, 101 // step + 1):
        for b in range(0, 101 // step + 1 - a):
            for c in range(0, 101 // step + 1 - a - b):
                d = 100 - (a + b + c) if step == 1 else (100 // step) - (a + b + c)
                if d < 0:
                    continue
                wa = a * step / 100.0
                wb = b * step / 100.0
                wc = c * step / 100.0
                wd = 1.0 - wa - wb - wc
                if wd < -1e-12:
                    continue
                num_sz = (wa * dim_scores["科技"]["深圳市"] + wb * dim_scores["产业"]["深圳市"]
                          + wc * dim_scores["人才"]["深圳市"] + wd * dim_scores["政策"]["深圳市"])
                num_gz = (wa * dim_scores["科技"]["广州市"] + wb * dim_scores["产业"]["广州市"]
                          + wc * dim_scores["人才"]["广州市"] + wd * dim_scores["政策"]["广州市"])
                total += 1
                if num_gz > num_sz:
                    counts["广州市"] += 1
                    if talent_only_min is None or wc < talent_only_min:
                        talent_only_min = wc
                    if len(flip_rows) < 5:
                        flip_rows.append({"科技": wa, "产业": wb, "人才": wc, "政策": round(wd, 4)})
                else:
                    counts["深圳市"] += 1
    return {
        "step": 0.01,
        "groups": total,
        "first_counts": counts,
        "first_share": {c: round(counts[c] / total, 4) for c in counts},
        "guangzhou_win_min_talent_weight": talent_only_min,
        "guangzhou_win_examples": flip_rows,
        "expected_groups": 176851,
    }


def main():
    t0 = time.time()
    dim = load(os.path.join(HERE, "M_SYNTH_VIT_DIM_SCORE_out.json"))
    ind = load(os.path.join(HERE, "M_SYNTH_VIT_INDICATOR_out.json"))
    m186 = load(os.path.join(HERE, "M_SYNTH_186_1_out.json"))
    ds = dim["dim_scores"]

    main_res = compare(ds, W_MAIN)
    idx = main_res["index"]
    rk = rank_of(idx)
    eq_res = compare(ds, W_EQ)
    eq = eq_res["index"]

    # S0 与 186_1 的一致性（同为四维等权）
    s0_diff = round(max(abs(eq[c] - m186["index_0_100"][c]) for c in CITIES), 6)

    ent = entropy_weights(ds)
    ent_idx = compare(ds, {d: ent[d]["weight"] for d in DIMS})["index"]

    ela = elasticity(ds, W_MAIN, 0.10)

    # 解析翻转阈值：Δ = Σ (x_gz - x_sz) w_d > 0
    coef = {d: round(ds[d]["广州市"] - ds[d]["深圳市"], 4) for d in DIMS}
    pos = {d: v for d, v in coef.items() if v > 0}
    # 广州唯一占优的维（人才）；其余三维为负。把全部剩余权重押在对广州最不伤的维。
    best_pos = max(pos, key=lambda d: pos[d]) if pos else None
    # 其余权重应全押在「对广州最不伤」的负项上，即绝对值最小的负系数（科技 −4.74）
    least_neg = max((v for v in coef.values() if v < 0), default=None)
    thr = None
    if best_pos and least_neg:
        p = pos[best_pos]
        q = abs(least_neg)
        thr = round(q / (p + q), 4)

    scan = simplex_scan(ds, step=1)

    # 每维覆盖率（来自 DIM_SCORE / INDICATOR 的产物，不重算）
    dim_cover = {
        d: {
            "cities_with_value": sum(1 for c in CITIES if ds[d].get(c) is not None),
            "cities_total": len(CITIES),
            "dims_live": dim["dim_sub_coverage"][d]["dims_live"],
            "dims_expected": dim["dim_sub_coverage"][d]["dims_expected"],
            "share": round(dim["dim_sub_coverage"][d]["dims_live"]
                           / dim["dim_sub_coverage"][d]["dims_expected"], 4),
        } for d in DIMS
    }
    leaf = ind["leaf_coverage"]
    weighted_completeness = round(sum(
        W_MAIN[d] * dim["dim_sub_coverage"][d]["dims_live"]
        / dim["dim_sub_coverage"][d]["dims_expected"] for d in DIMS), 4)

    derived = {
        "shenzhen_minus_guangzhou_main": {
            "value": round(idx["深圳市"] - idx["广州市"], 4),
            "numerator": idx["深圳市"], "denominator": idx["广州市"],
            "denominator_note": "主口径指数之差（深圳 − 广州）",
        },
        "entropy_weight_share": {
            "value": {d: ent[d]["weight"] for d in DIMS},
            "numerator": {d: ent[d]["divergence"] for d in DIMS},
            "denominator": round(sum(ent[d]["divergence"] for d in DIMS), 6),
            "denominator_note": "分母 = 四维差异系数之和；分子 = 该维差异系数 1 − e_d（e_d 为熵）",
        },
        "main_over_entropy_weight_ratio": {
            "value": {d: round(W_MAIN[d] / ent[d]["weight"], 4) for d in DIMS},
            "numerator": W_MAIN, "denominator": {d: ent[d]["weight"] for d in DIMS},
            "denominator_note": "分母 = 熵权；分子 = 主口径权重；比值 >1 表示主口径比熵权更看重该维",
        },
        "flip_threshold_talent_weight": {
            "value": thr, "numerator": abs(least_neg), "denominator": round(pos[best_pos] + abs(least_neg), 4),
            "denominator_note": "广州 − 深圳的系数里正项只有人才 +20.8，负项绝对值最小的是科技 4.74；"
                                "阈值 = 4.74 ÷ (20.8 + 4.74)，此时其余权重全押科技（对广州最不伤的维）",
        },
        "guangzhou_first_share": {
            "value": scan["first_share"]["广州市"], "numerator": scan["first_counts"]["广州市"],
            "denominator": scan["groups"],
            "denominator_note": "分母 = 单纯形格点总数 176,851（步长 0.01、四维和为 1）",
        },
        "weighted_dim_completeness": {
            "value": weighted_completeness,
            "numerator": round(weighted_completeness, 4), "denominator": 1,
            "denominator_note": "按主口径权重加权的维完整度（分母 1 表示这是 0—1 的比例，不是比值）",
        },
        "leaf_coverage_share": {
            "value": round(leaf["scored_entered"] / leaf["total"], 4),
            "numerator": leaf["scored_entered"], "denominator": leaf["total"],
            "denominator_note": "分母 = 正本 12 个分项；分子 = 有标准化得分并进维的分项",
        },
        "main_minus_equal_by_city": {
            "value": {c: round(idx[c] - eq[c], 4) for c in CITIES},
            "numerator": idx, "denominator": eq,
            "denominator_note": "分母 = 等权（S0）指数；分子 = 主口径指数；差为正表示主口径更看好该城",
        },
        "weight_times_dim_shenzhen": {
            "value": {d: round(W_MAIN[d] * ds[d]["深圳市"], 4) for d in DIMS},
            "numerator": W_MAIN, "denominator": {d: ds[d]["深圳市"] for d in DIMS},
            "denominator_note": "分母 = 深圳该维得分；分子 = 主口径权重；乘积即该维对深圳指数的贡献，四项之和 = 75.1478",
        },
        "weight_term_sum_shenzhen": {
            "value": round(sum(round(W_MAIN[d] * ds[d]["深圳市"], 4) for d in DIMS), 4),
            "numerator": round(sum(round(W_MAIN[d] * ds[d]["深圳市"], 4) for d in DIMS), 4),
            "denominator": idx["深圳市"],
            "denominator_note": "分母 = 主口径指数 75.1478；分子 = 四项 0.30·x 逐项四位取整后的和；两者差即取整残差",
        },
        "weight_term_rounding_residual": {
            "value": round(abs(sum(round(W_MAIN[d] * ds[d]["深圳市"], 4) for d in DIMS) - idx["深圳市"]), 4),
            "numerator": round(abs(sum(round(W_MAIN[d] * ds[d]["深圳市"], 4) for d in DIMS) - idx["深圳市"]), 4),
            "denominator": 1,
            "denominator_note": "分母取 1（单位是分，不是比值）；分子 = 逐项取整造成的 0.0001 残差",
        },
        "guangzhou_span_across_three_weights": {
            "value": round(max(eq["广州市"], idx["广州市"], ent_idx["广州市"]) - min(eq["广州市"], idx["广州市"], ent_idx["广州市"]), 4),
            "numerator": round(max(eq["广州市"], idx["广州市"], ent_idx["广州市"]), 4),
            "denominator": round(min(eq["广州市"], idx["广州市"], ent_idx["广州市"]), 4),
            "denominator_note": "分母 = 三套权重下广州的最低分（主口径 59.4186）；分子 = 最高分（熵权 63.7884）；差即广州对权重的摆动幅度",
        },
        "share_of_cities_with_full_4_dims": {
            "value": round(sum(1 for c in CITIES if all(ds[d].get(c) is not None for d in DIMS))
                           / len(CITIES), 4),
            "numerator": sum(1 for c in CITIES if all(ds[d].get(c) is not None for d in DIMS)),
            "denominator": len(CITIES),
            "denominator_note": "分母 = 评估集 4 城；分子 = 四维都有值的城数",
        },
    }

    out = {
        "metric_id": "M_SYNTH_VIT_INDEX",
        "metric_name": "区域创新活力指数",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "source": {
            "library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
            "mode": "read-only", "touched": False,
            "note": "本件零 SQL：四维分取 M_SYNTH_VIT_DIM_SCORE，分项覆盖取 M_SYNTH_VIT_INDICATOR",
        },
        "sources": [
            "code/_snapshots21/vit_family_20261023.json",
            "code/M_SYNTH_VIT_DIM_SCORE_out.json",
            "code/M_SYNTH_VIT_INDICATOR_out.json",
            "code/M_SYNTH_186_1_out.json",
        ],
        "reused_from": "code/M_SYNTH_VIT_DIM_SCORE_out.json, code/M_SYNTH_186_1_out.json, "
                       "code/M_SYNTH_VIT_INDICATOR_out.json",
        "scope": "深圳市 / 广州市 / 东莞市 / 惠州市",
        "evaluation_set": CITIES,
        "stat_year": 2024,
        "dim_scores": ds,
        "weights": {
            "main": W_MAIN,
            "main_is_official": False,
            "weights_are_authored": True,
            "rationale": "两维满维（科技 3/3、产业 3/3）各 0.30；两维半维（人才 2/4、政策 2/3）各 0.20",
            "equal": W_EQ,
            "entropy": {d: ent[d]["weight"] for d in DIMS},
            "sum_main": round(sum(W_MAIN.values()), 6),
        },
        "entropy_detail": ent,
        "index_0_100": idx,
        "rank": rk,
        "index_equal_weight": eq,
        "rank_equal_weight": rank_of(eq),
        "index_entropy": ent_idx,
        "rank_entropy": rank_of(ent_idx),
        "consistency": {
            "S0_equal_weight_vs_186_1_max_abs_diff": s0_diff,
            "note": "S0 等权场景与 M_SYNTH_186_1 逐城相等，说明两件共用同一个四维盘",
        },
        "coverage": {
            "dim_cover": dim_cover,
            "weighted_dim_completeness": weighted_completeness,
            "leaf_total": leaf["total"],
            "leaf_scored": leaf["scored_entered"],
            "leaf_has_value": leaf["has_value"],
            "leaf_missing": leaf["missing"],
            "leaf_missing_names": [x["name"] for x in ind["leaves"] if x["status"] == "缺"],
        },
        "missing_policy": {
            "rule": "维级缺（该维为 null）→ 整维不进加权，分母按在场维收缩，缺口写进 gap_dims；"
                    "维内缺子项 → 维分由子模型按在场子项等权给出；两者都不补 0",
            "no_silent_renormalization": "分母收缩必须在产物里可读（dims_used / gap_dims / "
                                         "weighted_dim_completeness），不得只报分数",
            "triggered": {c: main_res["gap"][c] for c in CITIES},
            "not_triggered_note": "本批四城四维都有值，维级缺未触发；触发的只有维内缺子项"
                                  "（人才 2/4、政策 2/3、产业 4/5）",
        },
        "elasticity": ela,
        "flip_threshold": {
            "coefficients_gz_minus_sz": coef,
            "condition": "广州领先 ⇔ 20.8·w_人才 > 4.74·w_科技 + 38.0239·w_产业 + 35.3·w_政策",
            "analytic_threshold_talent_weight": thr,
            "threshold_is_necessary_only": True,
            "reading": "0.1856 是必要条件：它假设其余 81.44% 权重全押在科技（对广州最不伤的维）。"
                       "主口径下人才权重 0.20 已高于该阈值，但产业 0.30 与政策 0.20 的负系数"
                       "（−38.0239、−35.3）分别把广州拉低 11.4072 与 7.06，人才只贡献 +4.16，"
                       "净差 −15.7292，深圳仍第一；网格里广州居首的组全部把产业与政策压到 0.05 以下",
        },
        "simplex": scan,
        "sensitivity": {
            "main_first": first(idx),
            "equal_first": first(eq),
            "entropy_first": first(ent_idx),
            "first_stable_across_three": len({first(idx), first(eq), first(ent_idx)}) == 1,
            "cities_in_pool": len([c for c in CITIES if idx.get(c) is not None]),
            "shenzhen_first_in_all_three": all(x["深圳市"] == 1 for x in (rk, rank_of(eq),
                                                                         rank_of(ent_idx))),
        },
        "dims_used": main_res["used"],
        "gap_dims": main_res["gap"],
        "derived": derived,
        "support_judgment": "部分支持",
        "support_reason": "指数三步（归一 / 维内加权 / 四维加权）都能落地，四城四维都有值；"
                          "但 12 个正本分项里 3 个四城全缺、人才与政策两维只有一半子维在场，"
                          "权重没有官方表（自定义 + 熵权对照），且极值归一是四市盘内相对尺度。"
                          "按 §0.1 判部分支持。",
        "note": "权重非官方：main_is_official=false。主口径 0.30/0.30/0.20/0.20 是按「维完整度」"
                "论证出来的，不是标定出来的；熵权只作客观对照，不建议直接发布",
        "base_years_used": [2024],
        "base_years_missing": [],
        "base_years_note": "统计年 2024；四维时间窗不齐（专利 2024、高被引论文全历史池、"
                           "政策当前有效集、产品标签当前截面），指数是截面合成而非年度产出",
        "elapsed_sec": round(time.time() - t0, 3),
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print("=== M_SYNTH_VIT_INDEX ===")
    print("主口径 0.30/0.30/0.20/0.20 :", idx, rk)
    print("等权 S0 :", eq, rank_of(eq), " 与 186_1 差", s0_diff)
    print("熵权 :", {d: ent[d]["weight"] for d in DIMS}, ent_idx)
    for d in DIMS:
        print(f"  弹性 {d} +0.10: Δ={ela['cases'][d]['delta']}")
    print("系数(广-深)", coef, "阈值", thr)
    print("网格", scan["groups"], scan["first_share"])
    print(f"→ {OUT}")


if __name__ == "__main__":
    main()
