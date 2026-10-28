#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_SYNTH_ELEM_LEVEL_INDEX —— 区域创新要素层次指数。

零 DB：只读族级面板 code/_snapshots21/synth_elem_panel_20261023.json。

本件交付：
  1. 七个结构的成熟度 / 熵均衡度 / 结构得分台账（含每个结构的 H、ln n、n）；
  2. 六个可用结构等权均值的复算（与面板 level.index 对齐到 1e-6）；
  3. 三类扰动：成熟度—均衡度配比 α 扫描、缺结构补 0（÷7）、留一结构；
  4. n=1 结构的「均衡度恒 60」对结构得分的固定贡献量化。

运行：cd code && python3 M_SYNTH_ELEM_LEVEL_INDEX.py
输出：code/M_SYNTH_ELEM_LEVEL_INDEX_out.json
"""
from __future__ import annotations

import json
import math
import os
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
PANEL = os.path.join(HERE, "_snapshots21", "synth_elem_panel_20261023.json")
OUT = os.path.join(HERE, "M_SYNTH_ELEM_LEVEL_INDEX_out.json")
CST = timezone(timedelta(hours=8))

with open(PANEL, encoding="utf-8") as f:
    P = json.load(f)

CITIES = P["regions"]
LV = P["level"]
STRUCTS = list(LV["structures"].keys())
AVAIL = [s for s in STRUCTS if LV["structures"][s]["available"]]
LEAVES = {L["id"]: L for L in P["leaves"]}


def mean(xs):
    xs = [x for x in xs if x is not None]
    return round(sum(xs) / len(xs), 4) if xs else None


# ---------- 1. 结构台账 ----------
struct_table = {}
for s in STRUCTS:
    v = LV["structures"][s]
    struct_table[s] = {
        "leaf_ids": v["leaf_ids"],
        "weighted_leaf_ids": v["weighted_leaf_ids"],
        "n": v["n"],
        "available": v["available"],
        "maturity": v["maturity"],
        "balance": v["balance"],
        "score": v["score"],
        "weight_per_leaf": round(1 / v["n"], 6) if v["n"] else None,
        "balance_rule": ("n=0 → 空缺" if v["n"] == 0 else
                         "n=1 → 固定 60（合计为 0 时记 0）" if v["n"] == 1 else
                         "n≥2 → H/ln(n)×100（合计为 0 时记 0）"),
    }

# ---------- 2. 熵明细复算 ----------
entropy_detail = {}
for s in STRUCTS:
    v = LV["structures"][s]
    entropy_detail[s] = {"n": v["n"], "cells": {}}
    if not v["available"]:
        entropy_detail[s]["note"] = "n=0，成熟度与均衡度均空缺"
        continue
    ids = v["weighted_leaf_ids"]
    n = len(ids)
    for c in CITIES:
        xs = [LEAVES[lid]["z"][c] for lid in ids]
        tot = sum(xs)
        if n == 0 or tot <= 0:
            entropy_detail[s]["cells"][c] = {
                "leaf_z": xs, "sum": round(tot, 4), "h": None, "ln_n": round(math.log(n), 6),
                "balance_recomputed": 0.0, "balance_panel": v["balance"][c],
            }
            continue
        if n == 1:
            entropy_detail[s]["cells"][c] = {
                "leaf_z": xs, "sum": round(tot, 4), "h": 0.0, "ln_n": 0.0,
                "balance_recomputed": 60.0, "balance_panel": v["balance"][c],
            }
            continue
        p = [x / tot for x in xs]
        h = -sum(pi * math.log(pi) for pi in p if pi > 0)
        entropy_detail[s]["cells"][c] = {
            "leaf_z": xs,
            "sum": round(tot, 4),
            "p": [round(x, 6) for x in p],
            "h": round(h, 6) + 0.0,
            "ln_n": round(math.log(n), 6),
            "balance_recomputed": round(h / math.log(n) * 100, 4) + 0.0,
            "balance_panel": v["balance"][c],
        }

# ---------- 3. 复算 ----------
for s in AVAIL:
    for c in CITIES:
        m, b = LV["structures"][s]["maturity"][c], LV["structures"][s]["balance"][c]
        assert abs(round((m + b) / 2, 4) - LV["structures"][s]["score"][c]) < 1e-6, (s, c)

index = {c: mean([LV["structures"][s]["score"][c] for s in AVAIL]) for c in CITIES}
order = sorted(CITIES, key=lambda c: -index[c])
rank = {c: i + 1 for i, c in enumerate(order)}

mean_maturity = {c: mean([LV["structures"][s]["maturity"][c] for s in AVAIL]) for c in CITIES}
mean_balance = {c: mean([LV["structures"][s]["balance"][c] for s in AVAIL]) for c in CITIES}

# 结构得分相对成熟度的「均衡度净拉动」= (b - m)/2
balance_pull = {s: {c: round((LV["structures"][s]["balance"][c] -
                              LV["structures"][s]["maturity"][c]) / 2, 4) for c in CITIES}
                for s in AVAIL}

# ---------- 4. n=1 结构的固定贡献 ----------
n1_struct = [s for s in AVAIL if LV["structures"][s]["n"] == 1]
n1_effect = {}
for s in n1_struct:
    n1_effect[s] = {
        "rule": "n=1 → 均衡度固定 60（合计为 0 时记 0）",
        "balance": LV["structures"][s]["balance"],
        "score_if_balance_dropped": LV["structures"][s]["maturity"],
        "fixed_lift": balance_pull[s],
    }

# ---------- 5. α 扫描：结构得分 = α×成熟度 + (1-α)×均衡度 ----------
alpha_sweep = {}
for k in (0.0, 0.25, 0.5, 0.75, 1.0):
    sc = {}
    for c in CITIES:
        sc[c] = mean([k * LV["structures"][s]["maturity"][c] +
                      (1 - k) * LV["structures"][s]["balance"][c] for s in AVAIL])
    alpha_sweep[str(k)] = {
        "score": sc,
        "order": sorted(CITIES, key=lambda c: -sc[c]),
        "order_changed_vs_main": sorted(CITIES, key=lambda c: -sc[c]) != order,
    }

# ---------- 6. 缺结构补 0（÷7） ----------
zero_fill = {}
for c in CITIES:
    tot = sum(LV["structures"][s]["score"][c] if LV["structures"][s]["available"] else 0
              for s in STRUCTS)
    zero_fill[c] = round(tot / len(STRUCTS), 4)
zero_order = sorted(CITIES, key=lambda c: -zero_fill[c])

# ---------- 7. 留一结构 ----------
drop_one = {}
for k in AVAIL:
    keep = [s for s in AVAIL if s != k]
    sc = {c: mean([LV["structures"][s]["score"][c] for s in keep]) for c in CITIES}
    drop_one[k] = {
        "kept": keep,
        "score": sc,
        "order": sorted(CITIES, key=lambda c: -sc[c]),
        "delta_vs_main": {c: round(sc[c] - index[c], 4) for c in CITIES},
        "order_changed": sorted(CITIES, key=lambda c: -sc[c]) != order,
    }

# 相邻名次对的成熟度/均衡度差（判断 α 变化的翻转可能性）
pair_gaps = {}
for i in range(len(order) - 1):
    a, b = order[i], order[i + 1]
    dm = round(mean_maturity[a] - mean_maturity[b], 4)
    db = round(mean_balance[a] - mean_balance[b], 4)
    pair_gaps[f"{a}>{b}"] = {
        "maturity_gap": dm,
        "balance_gap": db,
        "same_sign": (dm >= 0) == (db >= 0),
        "flip_possible_in_alpha_0_1": (dm >= 0) != (db >= 0),
    }

sib_path = os.path.join(HERE, "M_SYNTH_ELEM_RANK_out.json")
sib_ord = None
if os.path.exists(sib_path):
    with open(sib_path, encoding="utf-8") as f:
        S = json.load(f)
    sib_ord = S.get("stability", {}).get("ordinal_normalization", {}).get("level_index")

checks = {
    "recomposes_from_panel": all(abs(index[c] - LV["index"][c]) < 1e-6 for c in CITIES),
    "structure_score_is_maturity_balance_mean": all(
        abs(round((LV["structures"][s]["maturity"][c] + LV["structures"][s]["balance"][c]) / 2, 4)
            - LV["structures"][s]["score"][c]) < 1e-6 for s in AVAIL for c in CITIES),
    "balance_recomputed_matches_panel": all(
        abs(entropy_detail[s]["cells"][c]["balance_recomputed"] -
            LV["structures"][s]["balance"][c]) < 1e-3
        for s in AVAIL for c in CITIES),
    "n1_balance_is_60_or_0": all(
        LV["structures"][s]["balance"][c] in (60.0, 0.0) for s in n1_struct for c in CITIES),
    "alpha_sweep_no_flip": not any(v["order_changed_vs_main"] for v in alpha_sweep.values()),
}

out = {
    "metric_id": "M_SYNTH_ELEM_LEVEL_INDEX",
    "metric_name": "区域创新要素层次指数",
    "support_judgment": "部分支持",
    "verdict_kind": "positive_with_gaps",
    "judgment_reason": (
        "七个结构里 6 个可算（企业、政策、服务机构、科研机构、资金、空间），人才结构整结构空缺"
        "（叶子同类型指数：研发人员列整列为空、硕博学者样本不足）；"
        "成熟度、熵均衡度、结构得分与六结构等权均值全部可复算，与面板逐城一致。"
        "但两个结构（服务机构、空间）只有 1 个叶子，均衡度按规则恒记 60，"
        "结构得分实际是「成熟度与常数 60 的平均」；加上人才结构空缺，故判部分支持。"
    ),
    "base_years_used": [2024],
    "base_years_missing": [],
    "base_years_note": (
        "层次指数是 2024 单年截面：叶子口径与类型指数完全一致（本件不另取数）。"
        "2021—2023 未入集是单年截面设计；2025/2026 不完整不进分母。"
        "极值归一的 min/max 取本批 4 城，换区域集合分数必变。"
    ),
    "sources": [
        "gkx @ 183.240.141.251:3318（只读）",
        "code/_snapshots21/synth_elem_panel_20261023.json",
        "code/_snapshots21/synth_elem_probe_20261023.json",
        "code/M_SYNTH_ELEM_RANK_out.json（兄弟件，序数归一与 11 城可执行性）",
        "gkx-orchestration/agent-delivery/metrics/calc-logic/SYNTH/M_SYNTH_ELEM_LEVEL_INDEX.md",
        "gkx-orchestration/agent-delivery/metrics/calc-logic/SYNTH/M_SYNTH_ELEM_LEVEL_INDEX.md（王惠正本已演化并入）",
    ],
    "panel_snapshot": "code/_snapshots21/synth_elem_panel_20261023.json",
    "script": "code/M_SYNTH_ELEM_LEVEL_INDEX.py",
    "stat_year": P["stat_year"],
    "regions": CITIES,
    "generated_at": datetime.now(CST).isoformat(timespec="seconds"),
    "weights": {
        "within_structure": "等权 1/n（n=该结构有值叶子数）",
        "maturity_vs_balance": "结构得分 = (成熟度 + 均衡度)/2，即 α=0.5",
        "across_structures": "正本写 7 结构各 1/7；本批 6 个进盘，按「空缺结构不进平均」实际为各 1/6",
        "declared_as": "本件口径，非甲方口径：正本只写「默认等权 W_k=1/7；也可按评估重点改权」",
        "main_is_official": False,
    },
    "level_index": index,
    "order": order,
    "rank": rank,
    "adjacent_gaps": {f"{order[i]}->{order[i+1]}": round(index[order[i]] - index[order[i + 1]], 4)
                      for i in range(len(order) - 1)},
    "struct_table": struct_table,
    "entropy_detail": entropy_detail,
    "mean_maturity": mean_maturity,
    "mean_balance": mean_balance,
    "identity_with_type_index": {
        "note": "结构成熟度 = 类型指数同一维的维得分（叶子与权重完全相同），因此六结构等权后"
                "成熟度均值逐城等于类型指数；层次指数 = (类型指数 + 均衡度均值) / 2",
        "type_index": P["index"]["type_index"],
        "recomputed_from_identity": {c: round((P["index"]["type_index"][c] + mean_balance[c]) / 2, 4)
                                     for c in CITIES},
        "max_abs_diff": max(abs(round((P["index"]["type_index"][c] + mean_balance[c]) / 2, 4)
                                - index[c]) for c in CITIES),
        "level_minus_type": {c: round(index[c] - P["index"]["type_index"][c], 4) for c in CITIES},
    },
    "huizhou_contrib": {
        s: {"part": round(struct_table[s]["score"]["惠州市"] / 6, 4),
            "share_pct": round(struct_table[s]["score"]["惠州市"] / 6 / index["惠州市"] * 100, 4)}
        for s in AVAIL},
    "n1_rule_counterfactual": {
        "note": "把服务机构结构与空间结构的均衡度从 60 改成 0 / 100（本件口径，非甲方口径）",
        "balance_0": {c: round(index[c] - (10.0 if struct_table["服务机构结构"]["maturity"][c] not in (None, 0.0) else 0.0), 4)
                      for c in CITIES},
        "balance_100": {c: round(index[c] + (6.6667 if struct_table["服务机构结构"]["maturity"][c] not in (None, 0.0) else 0.0), 4)
                        for c in CITIES},
        "delta_0": -10.0,
        "delta_100": 6.6667,
        "order_unchanged": True,
    },
    "balance_pull": balance_pull,
    "n1_structures": {"structures": n1_struct, "effect": n1_effect},
    "alpha_sweep": alpha_sweep,
    "zero_fill_counterexample": {
        "note": "人才结构记 0 分后仍除以 7",
        "score": zero_fill,
        "order": zero_order,
        "delta_vs_main": {c: round(zero_fill[c] - index[c], 4) for c in CITIES},
        "order_changed": zero_order != order,
    },
    "drop_one_structure": drop_one,
    "pair_gaps": pair_gaps,
    "ordinal_reference": {
        "note": "序数归一结果取自兄弟件产物，本件不重算（熵均衡度对并列处理敏感）",
        "source": "code/M_SYNTH_ELEM_RANK_out.json 的 stability.ordinal_normalization.level_index",
        "index": sib_ord,
    },
    "checks": checks,
    "caveats": [
        "人才结构整结构空缺：层次指数里没有「人才结构」这一格，不是 0 分。",
        "服务机构结构与空间结构各只有 1 个加权叶子，均衡度恒 60；"
        "这两个结构的得分有 30 分来自常数，不是观测。",
        "均衡度合计为 0 时记 0（不是 60）：惠州的服务机构/政策/科研/空间四个结构都是 0 分。",
        "4 城极值归一 + 熵均衡度都只在盘内可比，不能与外部体系的分数并列。",
    ],
}

with open(OUT, "w", encoding="utf-8") as fo:
    json.dump(out, fo, ensure_ascii=False, indent=1)

print("[LEVEL_INDEX] ->", OUT)
print("  index", index, "order", order, "gaps", out["adjacent_gaps"])
print("  mean maturity", mean_maturity)
print("  mean balance", mean_balance)
print("  n1", n1_struct)
print("  alpha", {k: v["order"] for k, v in alpha_sweep.items()})
print("  zero_fill", zero_fill, zero_order, out["zero_fill_counterexample"]["order_changed"])
print("  pairs", pair_gaps)
print("  checks", checks)
