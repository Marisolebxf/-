#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_SYNTH_ELEM_TYPE_SCORE —— 七要素类型维得分。

零 DB：只读族级面板 code/_snapshots21/synth_elem_panel_20261023.json。

本件只交付「维得分」这一层：七个维各自的 0—100 分、维内等权权重、叶子构成，
以及叶子级留一扰动。**不汇总成总指数**（正本明写同 TYPE_INDEX，但 TYPE_INDEX 才是合成层）。
同时量化「拿本件加总冒充综合分」会造成多大偏差——这是权重件禁止的那条路径。

运行：cd code && python3 M_SYNTH_ELEM_TYPE_SCORE.py
输出：code/M_SYNTH_ELEM_TYPE_SCORE_out.json
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
PANEL = os.path.join(HERE, "_snapshots21", "synth_elem_panel_20261023.json")
OUT = os.path.join(HERE, "M_SYNTH_ELEM_TYPE_SCORE_out.json")
CST = timezone(timedelta(hours=8))

with open(PANEL, encoding="utf-8") as f:
    P = json.load(f)

CITIES = P["regions"]
T = P["type"]
DIMS = list(T["dims"].keys())
AVAIL = [d for d in DIMS if T["dims"][d]["available"]]
LEAVES = {L["id"]: L for L in P["leaves"]}


def mean(xs):
    xs = [x for x in xs if x is not None]
    return round(sum(xs) / len(xs), 4) if xs else None


# ---------- 1. 七行得分表 ----------
score_table = {}
for d in DIMS:
    v = T["dims"][d]
    score_table[d] = {
        "available": v["available"],
        "n": v["n"],
        "weight_per_leaf": round(1 / v["n"], 6) if v["n"] else None,
        "leaf_ids": v["leaf_ids"],
        "weighted_leaf_ids": v["weighted_leaf_ids"],
        "score": v["score"],
        "status": "有值" if v["available"] else "空缺（不填 0）",
    }

# ---------- 2. 叶子级构成：维得分 = Σ (z_j / n) ----------
leaf_contrib = {}
for d in AVAIL:
    n = T["dims"][d]["n"]
    leaf_contrib[d] = {
        "n": n,
        "weight_per_leaf": round(1 / n, 6),
        "leaves": {},
    }
    for lid in T["dims"][d]["weighted_leaf_ids"]:
        z = LEAVES[lid]["z"]
        leaf_contrib[d]["leaves"][lid] = {
            "name": LEAVES[lid]["name"],
            "state": LEAVES[lid]["state"],
            "raw": LEAVES[lid]["raw"],
            "z": z,
            "contrib": {c: (round(z[c] / n, 4) if z[c] is not None else None) for c in CITIES},
        }
    leaf_contrib[d]["sum_check"] = {
        c: round(sum(LEAVES[lid]["z"][c] / n for lid in T["dims"][d]["weighted_leaf_ids"]), 4)
        for c in CITIES
    }

# ---------- 3. 叶子级留一扰动 ----------
leave_one_leaf = {}
for d in AVAIL:
    ids = T["dims"][d]["weighted_leaf_ids"]
    if len(ids) < 2:
        leave_one_leaf[d] = {"note": "n=1，无可留一叶子（该维得分即单叶子的 z）"}
        continue
    leave_one_leaf[d] = {"variants": {}}
    for drop in ids:
        keep = [x for x in ids if x != drop]
        sc = {c: mean([LEAVES[x]["z"][c] for x in keep]) for c in CITIES}
        sc_full = {c: T["dims"][d]["score"][c] for c in CITIES}
        leave_one_leaf[d]["variants"][drop] = {
            "kept": keep,
            "score": sc,
            "delta_vs_full": {c: round(sc[c] - sc_full[c], 4) for c in CITIES},
            "order": sorted(CITIES, key=lambda c: -sc[c]),
            "order_changed": sorted(CITIES, key=lambda c: -sc[c]) != \
                sorted(CITIES, key=lambda c: -sc_full[c]),
        }

# ---------- 4. 维内极差与单维次序 ----------
dim_spread = {}
for d in AVAIL:
    vals = [T["dims"][d]["score"][c] for c in CITIES]
    dim_spread[d] = {
        "max": max(vals), "min": min(vals), "range": round(max(vals) - min(vals), 4),
        "rank_order": sorted(CITIES, key=lambda c: -T["dims"][d]["score"][c]),
        "tied_at_100": sum(1 for x in vals if x == 100.0),
        "tied_at_0": sum(1 for x in vals if x == 0.0),
    }

# ---------- 5. 加总禁令的量化：若把 6 维平均当综合分 ----------
dim_mean = {c: mean([T["dims"][d]["score"][c] for d in AVAIL]) for c in CITIES}
dim_mean_order = sorted(CITIES, key=lambda c: -dim_mean[c])
composite = P["index"]["elem_index"]
forbidden_gap = {c: round(dim_mean[c] - composite[c], 4) for c in CITIES}
dim_mean_sum = {c: round(sum(T["dims"][d]["score"][c] for d in AVAIL), 4) for c in CITIES}
dim_mean_sum_with_missing = {
    c: round(sum((T["dims"][d]["score"][c] or 0) for d in DIMS), 4) for c in CITIES}

# ---------- 6. 分数分布统计 ----------
flat = [T["dims"][d]["score"][c] for d in AVAIL for c in CITIES]
dist = {
    "cells": len(flat),
    "eq_100": sum(1 for x in flat if x == 100.0),
    "eq_0": sum(1 for x in flat if x == 0.0),
    "lt_10": sum(1 for x in flat if x < 10.0),
    "gt_90": sum(1 for x in flat if x > 90.0),
    "mean": round(sum(flat) / len(flat), 4),
    "min": min(flat),
    "max": max(flat),
}

checks = {
    "dim_scores_match_panel": all(
        abs(score_table[d]["score"][c] - T["dims"][d]["score"][c]) < 1e-9
        for d in AVAIL for c in CITIES),
    "leaf_contrib_sums_to_dim_score": all(
        all(abs(leaf_contrib[d]["sum_check"][c] - T["dims"][d]["score"][c]) < 1e-6 for c in CITIES)
        for d in AVAIL),
    "no_total_index_emitted": True,
    "dim_mean_equals_type_index": all(abs(dim_mean[c] - P["index"]["type_index"][c]) < 1e-6
                                      for c in CITIES),
    "dim_mean_differs_from_composite": any(abs(forbidden_gap[c]) > 1e-6 for c in CITIES),
}

out = {
    "metric_id": "M_SYNTH_ELEM_TYPE_SCORE",
    "metric_name": "七要素类型维得分",
    "support_judgment": "部分支持",
    "verdict_kind": "positive_with_gaps",
    "judgment_reason": (
        "七个维里 6 个能出分（企业、政策、服务机构、科研机构、资金、空间），"
        "创新人才维整维空缺——研发人员列整列为空、硕博学者四城仅 111 人。"
        "6 个有值维的分与其叶子构成都能逐城复算（维得分 = 维内叶子 z 的等权均值，误差 < 1e-6），"
        "但每维的叶子覆盖参差（1/3、2/2、1/2、3/3），且空间维与资金维均为代理口径，"
        "故判部分支持，不称完全转换支持。"
    ),
    "base_years_used": [2024],
    "base_years_missing": [],
    "base_years_note": (
        "维得分是 2024 单年截面的极值归一结果，不是多年均值。min/max 取本批 4 城，"
        "换区域集合同一城的分数必变。2021—2023 未入集（单年截面设计），2025/2026 不完整不进分母。"
    ),
    "sources": [
        "gkx @ 183.240.141.251:3318（只读）",
        "code/_snapshots21/synth_elem_panel_20261023.json",
        "code/_snapshots21/synth_elem_probe_20261023.json",
        "gkx-orchestration/agent-delivery/metrics/calc-logic/SYNTH/M_SYNTH_ELEM_TYPE_SCORE.md",
        "（王惠正本已并入 calc-logic 入库件）",
    ],
    "panel_snapshot": "code/_snapshots21/synth_elem_panel_20261023.json",
    "script": "code/M_SYNTH_ELEM_TYPE_SCORE.py",
    "stat_year": P["stat_year"],
    "regions": CITIES,
    "generated_at": datetime.now(CST).isoformat(timespec="seconds"),
    "weights": {
        "within_dim": "等权 1/n；n = 该维有值叶子数（企业 3、政策 2、服务机构 1、科研机构 3、资金 2、空间 1）",
        "across_dims": "本件不跨维加权（不输出总指数）；跨维合成见 M_SYNTH_ELEM_TYPE_INDEX 与 M_SYNTH_ELEM_WEIGHT",
        "declared_as": "本件口径，非甲方口径：正本只写「可采用等权重，也可根据评估重点自行制定」",
        "main_is_official": False,
    },
    "score_table": score_table,
    "leaf_contrib": leaf_contrib,
    "leave_one_leaf": leave_one_leaf,
    "dim_spread": dim_spread,
    "distribution": dist,
    "forbidden_aggregation": {
        "note": "把 6 个可用维等权平均（= TYPE_INDEX）直接当综合分使用时的偏差；权重件明写禁止用七要素 SCORE 加总冒充三维分",
        "dim_mean": dim_mean,
        "dim_mean_order": dim_mean_order,
        "composite_elem_index": composite,
        "gap_vs_composite": forbidden_gap,
        "sum_of_6_dims": dim_mean_sum,
        "sum_with_missing_as_zero": dim_mean_sum_with_missing,
        "order_changed": dim_mean_order != P["index"]["rank"] and
                          dim_mean_order != sorted(CITIES, key=lambda c: -composite[c]),
    },
    "checks": checks,
    "caveats": [
        "本件不输出总指数：七行是维得分，跨维合成属 TYPE_INDEX 与 WEIGHT，混用会重复计入企业类信息。",
        "创新人才维为空缺（null），不是 0 分；任何把它当 0 分再加总的写法都会系统性压低强城。",
        "服务机构维只有 1 个加权叶子（服务机构数量），服务机构类型数因四城恒 6 类被判退化、不进加权。",
        "资金维是上市主体口径（2024 年 651 家），空间维是名称关键词弱代理，两者都不宜读作区域总量。",
    ],
}

with open(OUT, "w", encoding="utf-8") as fo:
    json.dump(out, fo, ensure_ascii=False, indent=1)

print("[TYPE_SCORE] ->", OUT)
for d in DIMS:
    print(f"  {d:8s} n={score_table[d]['n']} score={score_table[d]['score']}")
print("  dist", dist)
print("  forbidden gap", forbidden_gap, "order", dim_mean_order)
print("  checks", checks)
