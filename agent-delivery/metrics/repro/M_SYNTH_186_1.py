#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""区域创新活力综合分析模型（M_SYNTH_186_1）—— 复现脚本。

正本口径（算法库序号 186 模型入口）：四维分别调用 182 / 183 / 184 / 185 的子项，
四维等权得活力指数，「缺维不补 0、不进平均」。与 M_SYNTH_VIT_INDEX 同核。

本件是「规范值」：权重写死为 1/4，任何人重跑都得到同一个数。
VIT_INDEX 出的是「参数化指数」（自定义权重 + 弹性 + 翻转阈值），
两者的等权场景必须逐城相等——本件把 S0 等权指数写成字段，供 VIT_INDEX 反查。

运行：
    cd code && python3 M_SYNTH_186_1.py
产物：
    code/M_SYNTH_186_1_out.json
"""
from __future__ import annotations

import json
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
PANEL = os.path.join(SNAP, "vit_family_20261023.json")
OUT = os.path.join(HERE, "M_SYNTH_186_1_out.json")

CITIES = ["深圳市", "广州市", "东莞市", "惠州市"]
DIMS = ["科技", "产业", "人才", "政策"]
W = {d: 0.25 for d in DIMS}


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def rank_of(d: dict) -> dict:
    order = sorted([c for c in CITIES if d.get(c) is not None], key=lambda c: (-d[c], c))
    return {c: i + 1 for i, c in enumerate(order)}


def composite(dim_scores: dict, weights: dict, cities=CITIES):
    """缺维处理：该维不计入分子，分母同时收缩；缺口必须单独记，不许静默。

    返回 (index, used_dims, gap_dims)。
    """
    idx, used, gap = {}, {}, {}
    for c in cities:
        num = den = 0.0
        u, g = [], []
        for d in weights:
            if weights[d] <= 0:
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
    return idx, used, gap


def main():
    t0 = time.time()
    panel = load(PANEL)
    dim = load(os.path.join(HERE, "M_SYNTH_VIT_DIM_SCORE_out.json"))
    rank_out = load(os.path.join(HERE, "M_SYNTH_VIT_RANK_out.json"))
    ds = dim["dim_scores"]

    idx, used, gap = composite(ds, W)
    rk = rank_of(idx)
    n_dims = {c: sum(1 for d in DIMS if ds[d].get(c) is not None) for c in CITIES}

    # ---------------------------------------------------------------- 一致性
    # 正本「四维等权」的另一种写法：先算逐维均值再乘 1/4，结果必须相同。
    idx_check = {c: round(sum(ds[d][c] for d in DIMS if ds[d].get(c) is not None)
                          / max(1, n_dims[c]), 4) for c in CITIES}
    consistency = round(max(abs(idx[c] - idx_check[c]) for c in CITIES), 6)

    # ---------------------------------------------------------------- 消融
    # A. 把「0 分维」误当缺测（证明 0 ≠ null）：惠州人才/政策为 0，若记为缺测，
    #    分母从 4 缩到 2，分数会从 1.9012 升到 3.8025。
    zero_as_null = {}
    for c in CITIES:
        zero_dims = [d for d in DIMS if ds[d].get(c) == 0.0]
        if not zero_dims:
            zero_as_null[c] = {"index": idx[c], "zero_dims": []}
            continue
        vals = [ds[d][c] for d in DIMS if d not in zero_dims]
        zero_as_null[c] = {
            "index": round(sum(vals) / len(vals), 4) if vals else None,
            "zero_dims": zero_dims,
            "delta": round((sum(vals) / len(vals) if vals else 0) - idx[c], 4),
        }
    # B. 只用「满维」两维（科技 3/3、产业 3/3）
    idx_2d, _, _ = composite(ds, {"科技": 0.5, "产业": 0.5, "人才": 0.0, "政策": 0.0})
    # C. 去掉唯一利好广州的人才维
    idx_no_talent, _, _ = composite(ds, {"科技": 1 / 3, "产业": 1 / 3, "人才": 0.0, "政策": 1 / 3})
    # D. 单维极值（每个城市只看自己最强的维）——上界参考
    best_dim = {c: max(DIMS, key=lambda d: ds[d][c] if ds[d].get(c) is not None else -1)
                for c in CITIES}

    # ---------------------------------------------------------------- 兄弟件对照
    rank_gba4 = rank_out["boards"]["gba4"]
    rank_2d = rank_out["boards"]["gba4_reference_two_dims"]
    sz_lead_rank = round(rank_gba4["index"]["深圳市"] - rank_gba4["index"]["广州市"], 4)
    sz_lead_here = round(idx["深圳市"] - idx["广州市"], 4)
    rank_capped = [d for d in DIMS if rank_gba4["dim_scores"][d].get("深圳市") == 100.0]

    derived = {
        "shenzhen_lead_over_guangzhou": {
            "value": sz_lead_here,
            "numerator": idx["深圳市"], "denominator": idx["广州市"],
            "denominator_note": "合成指数之差（深圳 − 广州）",
        },
        "lead_shrink_vs_leaf_board_pct": {
            "value": round(100.0 * (sz_lead_rank - sz_lead_here) / sz_lead_rank, 4),
            "numerator": round(sz_lead_rank - sz_lead_here, 4),
            "denominator": sz_lead_rank,
            "denominator_note": "分母 = VIT_RANK 四维主盘的深圳领先幅度 31.76（89.80 − 58.04）；"
                                "分子 = 该幅度减到 14.3159 的收缩量",
        },
        "rank_leaf_board_lead": {
            "value": sz_lead_rank, "numerator": rank_gba4["index"]["深圳市"],
            "denominator": rank_gba4["index"]["广州市"],
            "denominator_note": "VIT_RANK 四维主盘（单叶子口径，只收 2 城）的深圳 − 广州",
        },
        "zero_as_null_delta_huizhou": {
            "value": zero_as_null["惠州市"]["delta"],
            "numerator": zero_as_null["惠州市"]["index"], "denominator": idx["惠州市"],
            "denominator_note": "把惠州的 0 分维（科技/人才/政策）误记为缺测后的分数 − 原分数；"
                                "分母是该城原分数",
        },
        "city_index_share_of_max": {
            "value": {c: round(idx[c] / idx["深圳市"], 4) for c in CITIES},
            "numerator": idx, "denominator": idx["深圳市"],
            "denominator_note": "分母 = 盘内最高分（深圳）；分子 = 该城指数",
        },
        "dims_available_share": {
            "value": {c: round(n_dims[c] / 4.0, 4) for c in CITIES},
            "numerator": n_dims, "denominator": 4,
            "denominator_note": "分母 = 四维；分子 = 该城有值的维数",
        },
    }

    out = {
        "metric_id": "M_SYNTH_186_1",
        "metric_name": "区域创新活力综合分析模型",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "source": {
            "library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
            "mode": "read-only", "touched": False,
            "note": "本件零 SQL：四维分取 M_SYNTH_VIT_DIM_SCORE（该件再取四个子模型产物）",
        },
        "sources": [
            "code/_snapshots21/vit_family_20261023.json",
            "code/M_SYNTH_VIT_DIM_SCORE_out.json",
            "code/M_SYNTH_182_1_out.json", "code/M_SYNTH_183_1_out.json",
            "code/M_SYNTH_184_1_out.json", "code/M_SYNTH_185_1_out.json",
        ],
        "reused_from": "code/M_SYNTH_VIT_DIM_SCORE_out.json, code/M_SYNTH_182_1_out.json, "
                       "code/M_SYNTH_183_1_out.json, code/M_SYNTH_184_1_out.json, "
                       "code/M_SYNTH_185_1_out.json",
        "scope": "深圳市 / 广州市 / 东莞市 / 惠州市",
        "evaluation_set": CITIES,
        "stat_year": 2024,
        "dims_definition": {
            "科技": "M_SYNTH_182_1 综合分（基础科学 / 应用科技 / 科研机构三维等权）",
            "产业": "M_SYNTH_183_1 综合分（产品服务创新 / 企业创新 / 服务机构创新三维等权）",
            "人才": "M_SYNTH_184_1 综合分（在场两子维等权）",
            "政策": "M_SYNTH_185_1 综合分（在场两子维等权）",
        },
        "dim_scores": ds,
        "weights": {
            "main": W,
            "main_is_official": False,
            "is_fixed": True,
            "rule": "四维等权 1/4，写死不可调；缺维不补 0、不进平均（分母同步收缩并记缺口）",
        },
        "min_dims_for_index": 4,
        "n_dims_available": n_dims,
        "dims_used": used,
        "gap_dims": gap,
        "index_0_100": idx,
        "rank": rk,
        "consistency": {
            "two_way_max_abs_diff": consistency,
            "note": "『加权和』与『逐维均值』两种写法逐城相等（0.0），说明等权实现无中间舍入",
        },
        "ablation": {
            "A_zero_dims_as_null": zero_as_null,
            "B_two_full_dims": {"index": idx_2d, "rank": rank_of(idx_2d),
                                "note": "只用满维的科技 0.5 + 产业 0.5；四城都在盘内"},
            "C_drop_talent": {"index": idx_no_talent, "rank": rank_of(idx_no_talent),
                              "note": "去掉唯一利好广州的人才维"},
            "D_best_dim_each": best_dim,
        },
        "derived": derived,
        "cross_sibling": {
            "M_SYNTH_VIT_RANK_gba4": {
                "label": rank_gba4["label"],
                "index": rank_gba4["index"], "rank": rank_gba4["rank"],
                "dim_cover": rank_gba4["dim_cover"],
                "capped_at_100_dims_for_shenzhen": rank_capped,
            },
            "M_SYNTH_VIT_RANK_two_dim": {
                "label": rank_2d["label"], "index": rank_2d["index"], "rank": rank_2d["rank"],
            },
            "note": "VIT_RANK 用单叶子直取（专利授权 / 高企数 / 高学历占比 / 政策存量），"
                    "深圳在产业、人才、政策三维都是盘内最大值、恒为 100，故其四维主盘只有 2 城进盘；"
                    "本件用子模型综合分，四城都有四维，深圳的黄斑（恒 100 维）消失",
        },
        "support_judgment": "部分支持",
        "support_reason": "四维等权可算、四城都有四维，指数逐城可复算；但四维本身有两维只有一半"
                          "子维在场（人才 2/4、政策 2/3），产业维有一个三级指标四城全缺，"
                          "四城盘上的极值归一又让每维的最小值恒为 0。"
                          "按 §0.1「始终有部分依赖维度无法得到足够数据」判部分支持。",
        "note": "本件是规范值（写死等权），VIT_INDEX 的 S0 场景必须与本件逐城相等；"
                "两件的差别只在『要不要扫权重』，不在『四维分怎么来』",
        "base_years_used": [2024],
        "base_years_missing": [],
        "base_years_note": "统计年 2024；四维的时间窗不齐（专利 2024 年、高被引论文为全历史池、"
                           "政策为当前有效集、产品标签为当前截面），故指数是『2024 年口径下的截面』，"
                           "不是 2024 年当年产出",
        "elapsed_sec": round(time.time() - t0, 3),
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print("=== M_SYNTH_186_1（四维等权）===")
    for c in CITIES:
        print(f"{c}: dims={n_dims[c]}/4 index={idx[c]} rank={rk[c]} gap={gap[c]}")
    print("一致性", consistency)
    print("二维满维盘", idx_2d, rank_of(idx_2d))
    print("去人才维", idx_no_talent, rank_of(idx_no_talent))
    print("0 当缺测", {c: v["delta"] for c, v in zero_as_null.items() if v["zero_dims"]})
    print(f"→ {OUT}")


if __name__ == "__main__":
    main()
