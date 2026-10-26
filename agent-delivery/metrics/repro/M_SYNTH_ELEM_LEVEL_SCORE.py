#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SYNTH_ELEM_LEVEL_SCORE —— 七大结构层次评价。

零 DB：只读族级面板 code/_snapshots21/synth_elem_panel_20261023.json。

本件只输出「结构层评价」：七个结构 × 四城的成熟度、熵均衡度、达标，
**不汇总成总指数**（总指数是 M_SYNTH_ELEM_LEVEL_INDEX）。
达标口径按正本：成熟度 ≥ 本批该结构成熟度均值。本件另给三种替代阈值
（留一城均值、中位数、固定 60 分）做敏感性，量化「达标」这件事有多依赖阈值定义。

运行：cd code && python3 M_SYNTH_ELEM_LEVEL_SCORE.py
输出：code/M_SYNTH_ELEM_LEVEL_SCORE_out.json
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
PANEL = os.path.join(HERE, "_snapshots21", "synth_elem_panel_20261023.json")
OUT = os.path.join(HERE, "M_SYNTH_ELEM_LEVEL_SCORE_out.json")
CST = timezone(timedelta(hours=8))

with open(PANEL, encoding="utf-8") as f:
    P = json.load(f)

CITIES = P["regions"]
LV = P["level"]
STRUCTS = list(LV["structures"].keys())
AVAIL = [s for s in STRUCTS if LV["structures"][s]["available"]]


def mean(xs):
    xs = [x for x in xs if x is not None]
    return round(sum(xs) / len(xs), 4) if xs else None


def median(xs):
    xs = sorted(x for x in xs if x is not None)
    n = len(xs)
    if not n:
        return None
    return round((xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2), 4)


# ---------- 1. 达标主口径 ----------
threshold = {s: mean([LV["structures"][s]["maturity"][c] for c in CITIES]) for s in STRUCTS}
rows = {}
for s in STRUCTS:
    v = LV["structures"][s]
    rows[s] = {
        "n": v["n"],
        "available": v["available"],
        "maturity": v["maturity"],
        "balance": v["balance"],
        "score": v["score"],
        "threshold_mean_maturity": threshold[s],
        "margin_vs_threshold": {c: (round(v["maturity"][c] - threshold[s], 4)
                                    if v["maturity"][c] is not None and threshold[s] is not None
                                    else None) for c in CITIES},
        "meets_standard": {c: (None if v["maturity"][c] is None or threshold[s] is None
                               else (1 if v["maturity"][c] >= threshold[s] else 0))
                           for c in CITIES},
    }

meet_count = {c: sum(1 for s in AVAIL if rows[s]["meets_standard"][c] == 1) for c in CITIES}
miss_count = {c: sum(1 for s in AVAIL if rows[s]["meets_standard"][c] == 0) for c in CITIES}
null_count = {c: sum(1 for s in STRUCTS if rows[s]["meets_standard"][c] is None) for c in CITIES}

# ---------- 2. 替代阈值 ----------
alt_threshold = {}
for s in STRUCTS:
    m = {c: LV["structures"][s]["maturity"][c] for c in CITIES}
    nonnull = [c for c in CITIES if m[c] is not None]
    loo = {}
    for c in nonnull:
        others = [m[x] for x in nonnull if x != c]
        loo[c] = mean(others)
    alt_threshold[s] = {
        "main_mean": threshold[s],
        "loo_mean": loo,
        "median": median([m[c] for c in nonnull]),
        "fixed_60": 60.0,
        "meets_main": {c: rows[s]["meets_standard"][c] for c in CITIES},
        "meets_loo": {c: (1 if m[c] >= loo[c] else 0) if c in loo else None for c in CITIES},
        "meets_median": {c: (1 if m[c] >= median([m[x] for x in nonnull]) else 0)
                         if c in nonnull else None for c in CITIES},
        "meets_fixed_60": {c: (1 if m[c] >= 60.0 else 0) if c in nonnull else None for c in CITIES},
    }

alt_counts = {}
for k in ("meets_main", "meets_loo", "meets_median", "meets_fixed_60"):
    alt_counts[k] = {c: sum(1 for s in AVAIL if alt_threshold[s][k][c] == 1) for c in CITIES}

# 阈值方案之间「判定不同」的格子
disagreements = {}
for s in AVAIL:
    d = []
    for c in CITIES:
        vals = {k: alt_threshold[s][k][c] for k in
                ("meets_main", "meets_loo", "meets_median", "meets_fixed_60")}
        if len(set(vals.values())) > 1:
            d.append({"city": c, "by_rule": vals})
    if d:
        disagreements[s] = d

# ---------- 3. 结构与均衡度的描述统计 ----------
balance_stats = {}
for s in AVAIL:
    vals = [LV["structures"][s]["balance"][c] for c in CITIES]
    balance_stats[s] = {
        "min": min(vals), "max": max(vals), "range": round(max(vals) - min(vals), 4),
        "constant": len(set(vals)) == 1,
        "all_zero_except": [c for c in CITIES if vals[CITIES.index(c)] == 0.0],
    }

checks = {
    "maturity_equals_type_dim_score": all(
        abs(LV["structures"][s]["maturity"][c] - P["type"]["dims"][
            "创新人才" if s == "人才结构" else s.replace("结构", "")]["score"][c]) < 1e-6
        for s in AVAIL for c in CITIES),
    "structure_score_is_mean_of_two": all(
        abs(round((LV["structures"][s]["maturity"][c] + LV["structures"][s]["balance"][c]) / 2, 4)
            - LV["structures"][s]["score"][c]) < 1e-6 for s in AVAIL for c in CITIES),
    "thresholds_recomputed": all(
        (threshold[s] is None and mean([LV["structures"][s]["maturity"][c] for c in CITIES]) is None)
        or (threshold[s] is not None and
            abs(threshold[s] - mean([LV["structures"][s]["maturity"][c] for c in CITIES])) < 1e-9)
        for s in STRUCTS),
    "meets_standard_complete": all(
        rows[s]["meets_standard"][c] is None or rows[s]["meets_standard"][c] in (0, 1)
        for s in STRUCTS for c in CITIES),
    "no_total_index_emitted": True,
}

out = {
    "metric_id": "M_SYNTH_ELEM_LEVEL_SCORE",
    "metric_name": "七大结构层次评价",
    "support_judgment": "部分支持",
    "verdict_kind": "positive_with_gaps",
    "judgment_reason": (
        "七个结构里 6 个能给出成熟度、均衡度与达标（人才结构因研发人员整列空、硕博学者样本不足而整结构空缺）；"
        "成熟度与均衡度逐城可复算，达标按「成熟度 ≥ 本批均值」逐格可复算。"
        "但两个结构只有 1 个叶子（均衡度恒 60）、达标阈值是本批 4 城的相对均值而非绝对标准，"
        "且换一种阈值（中位数）就会让广州的资金结构从「未达标」变「达标」——"
        "判档依赖阈值定义，故判部分支持。"
    ),
    "base_years_used": [2024],
    "base_years_missing": [],
    "base_years_note": (
        "结构评价是 2024 单年截面，叶子与类型指数同源。2021—2023 未入集（单年截面设计），"
        "2025/2026 不完整不进分母。达标阈值取本批四城该结构成熟度均值——"
        "换一批城市阈值就变，达标结果不可跨批复用。"
    ),
    "sources": [
        "gkx @ 183.240.141.251:3318（只读）",
        "code/_snapshots21/synth_elem_panel_20261023.json",
        "code/_snapshots21/synth_elem_probe_20261023.json",
        "gkx-orchestration/agent-delivery/metrics/calc-logic/SYNTH/M_SYNTH_ELEM_LEVEL_SCORE.md",
        "local-workspace/docs/metrics/王惠阶段性成果/20260904_综合智能/指标计算逻辑/M_SYNTH_ELEM_LEVEL_SCORE.md",
    ],
    "panel_snapshot": "code/_snapshots21/synth_elem_panel_20261023.json",
    "script": "code/M_SYNTH_ELEM_LEVEL_SCORE.py",
    "stat_year": P["stat_year"],
    "regions": CITIES,
    "generated_at": datetime.now(CST).isoformat(timespec="seconds"),
    "weights": {
        "within_structure": "等权 1/n（成熟度）",
        "maturity_vs_balance": "结构得分 = (成熟度+均衡度)/2（本件只作展示，不汇总）",
        "across_structures": "本件不跨结构加权（不输出总指数）",
        "declared_as": "本件口径，非甲方口径：正本只写「默认等权」与「达标=成熟度≥本批均值」",
        "main_is_official": False,
    },
    "rows": rows,
    "meet_count": meet_count,
    "miss_count": miss_count,
    "null_count": null_count,
    "standard_rule": "达标_k = 1 当且仅当 成熟度_k ≥ 本批该结构成熟度均值（正本第三步）",
    "threshold_margin_notes": {
        "sz_enterprise_vs_median": round(median([rows["企业结构"]["maturity"][c] for c in CITIES]) - rows["企业结构"]["maturity"]["深圳市"], 4),
        "single_leaf_z_lift_to_mean": round(0.8 / rows["企业结构"]["n"], 4),
        "note": "深圳企业结构成熟度 43.5428 距中位数 47.1334 差 3.5906；单叶子 z 升 0.8 对 3 叶均值的拉动为 0.2667",
    },
    "alternative_thresholds": alt_threshold,
    "alternative_meet_counts": alt_counts,
    "threshold_disagreements": disagreements,
    "balance_stats": balance_stats,
    "checks": checks,
    "caveats": [
        "人才结构整结构空缺（成熟度/均衡度/达标均为 null），不是未达标。",
        "达标是「本批四城相对」的判定，不是绝对标准；换城市集合，阈值与达标同时变。",
        "服务机构结构与空间结构的均衡度恒为 60（n=1），这两个结构的「均衡」不含信息。",
        "深圳的企业结构成熟度 43.5428 低于本批均值 43.8068，差 0.2640，是全表最薄的一处判定。",
    ],
}

with open(OUT, "w", encoding="utf-8") as fo:
    json.dump(out, fo, ensure_ascii=False, indent=1)

print("[LEVEL_SCORE] ->", OUT)
for s in STRUCTS:
    print(f"  {s:8s} thr={threshold[s]} meets={rows[s]['meets_standard']}")
print("  meet_count", meet_count, "miss", miss_count, "null", null_count)
print("  alt counts", alt_counts)
print("  disagreements", json.dumps(disagreements, ensure_ascii=False))
print("  checks", checks)
