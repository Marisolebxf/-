#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_SYNTH_ELEM_RANK —— 对比范围要素综合排名。

只做 `M_SYNTH_ELEM_INDEX` 的排序算子，但把「名次稳不稳」当成第一等交付：
  1. 主名次（RANK，同分并列下一名跳号）与四城分差；
  2. 默认 11 城对比范围的可执行性实测（读底册城市分布，逐城给主体数）；
  3. 三种扰动下的名次稳定性：三维权重单纯形网格、留一维、换归一方式（序数归一）。
     三种扰动下名次是否变，直接决定这份榜能不能对外。

运行：cd code && python3 M_SYNTH_ELEM_RANK.py
输出：code/M_SYNTH_ELEM_RANK_out.json
"""
from __future__ import annotations

import json
import math
import os
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
PANEL = os.path.join(SNAP, "synth_elem_panel_20261023.json")
BASE = os.path.join(SNAP, "base_20261021.json")
OUT = os.path.join(HERE, "M_SYNTH_ELEM_RANK_out.json")
CST = timezone(timedelta(hours=8))

with open(PANEL, encoding="utf-8") as f:
    P = json.load(f)
with open(BASE, encoding="utf-8") as f:
    BASE_ROWS = json.load(f)

CITIES = P["regions"]
T = P["index"]["type_index"]
L = P["index"]["level_index"]
D = P["index"]["domain_index"]


def rank_of(score):
    """RANK()：同分并列，下一名跳号。"""
    order = sorted([c for c in score if score[c] is not None], key=lambda c: -score[c])
    out, prev, prev_rank = {}, None, 0
    for i, c in enumerate(order, 1):
        if prev is not None and score[c] == score[prev]:
            out[c] = prev_rank
        else:
            out[c] = i
            prev_rank = i
        prev = c
    return out, order


def composite(w):
    return {c: w[0] * T[c] + w[1] * L[c] + w[2] * D[c] for c in CITIES}


main_score = {c: round((T[c] + L[c] + D[c]) / 3, 4) for c in CITIES}
main_rank, main_order = rank_of(main_score)

# ---------------------------------------------------------------- 11 城范围实测
city_counts = {}
for r in BASE_ROWS:
    city_counts[r[4]] = city_counts.get(r[4], 0) + 1
DEFAULT_SCOPE = ["北京市", "上海市", "广州市", "深圳市", "杭州市", "南京市",
                 "武汉市", "重庆市", "宁波市", "成都市", "合肥市"]
scope = {c: city_counts.get(c, 0) for c in DEFAULT_SCOPE}
scope_executable = {c: (v >= 500) for c, v in scope.items()}
scope_total = sum(scope.values())
scope_other = scope_total - scope.get("广州市", 0) - scope.get("深圳市", 0)
scope_other_pct = round(scope_other / len(BASE_ROWS) * 100, 4)
scope_note = {
    "default_scope": DEFAULT_SCOPE,
    "city_base_rows": scope,
    "executable": scope_executable,
    "executable_n": sum(1 for v in scope_executable.values() if v),
    "scope_total_rows": scope_total,
    "base_total_rows": len(BASE_ROWS),
    "note": "11 城里只有广深两城主体量级够做极值归一（东莞、惠州不在默认 11 城名单里，"
            "但它们是本库仅有的另外两个可算城市）；京沪杭宁汉蓉渝合甬 9 城合计 "
            f"{scope_other} 行，占底册 {scope_other_pct}%，"
            "任何叶子在这 9 城都会退化成 0 或常数。",
}

# ---------------------------------------------------------------- 扰动 1：权重网格
n = 100
grid_first, grid_second, grid_order = {}, {}, {}
for i in range(n + 1):
    for j in range(n + 1 - i):
        k = n - i - j
        sc = composite((i / n, j / n, k / n))
        o = sorted(CITIES, key=lambda c: -sc[c])
        grid_first[o[0]] = grid_first.get(o[0], 0) + 1
        grid_second[o[1]] = grid_second.get(o[1], 0) + 1
        key = ">".join(o)
        grid_order[key] = grid_order.get(key, 0) + 1
grid_total = sum(grid_first.values())

# ---------------------------------------------------------------- 扰动 2：留一维
drop = {}
for k in (0, 1, 2):
    sc = {}
    for c in CITIES:
        parts = [T[c], L[c], D[c]]
        kept = [parts[i] for i in range(3) if i != k]
        sc[c] = round(sum(kept) / 2, 4)
    r, o = rank_of(sc)
    drop[["type", "level", "domain"][k]] = {"score": sc, "order": o, "rank": r,
                                            "order_changed": o != main_order}

# ---------------------------------------------------------------- 扰动 3：序数归一
# 把每个叶子的 4 城原值换成名次（1..4）后线性映射到 0/33.33/66.67/100，
# 再按面板同一套聚合规则重算三层指数。目的：看结论是否依赖极值归一的「距离」。
def ordinal_z(raw):
    vals = {c: v for c, v in raw.items() if v is not None}
    if len(set(vals.values())) <= 1:
        return {c: (50.0 if c in vals else None) for c in raw}
    asc = sorted(set(vals.values()))
    m = {v: (i / (len(asc) - 1) * 100 if len(asc) > 1 else 50.0) for i, v in enumerate(asc)}
    return {c: (None if v is None else round(m[v], 4)) for c, v in raw.items()}


def entropy_balance(zs):
    if not zs:
        return None
    if len(zs) == 1:
        return 60.0
    tot = sum(zs)
    if tot <= 0:
        return 0.0
    h = 0.0
    for s in zs:
        p = s / tot
        if p > 0:
            h -= p * math.log(p)
    return round(h / math.log(len(zs)) * 100, 4)


ord_z = {}
for lf in P["leaves"] + P["domain_leaves"]:
    ord_z[lf["id"]] = ordinal_z(lf["raw"])

type_dims, level_structs, domain_dims = {}, {}, {}
for d, v in P["type"]["dims"].items():
    type_dims[d] = {c: (round(sum(ord_z[i][c] for i in v["weighted_leaf_ids"]
                                 if ord_z[i][c] is not None)
                             / len([i for i in v["weighted_leaf_ids"] if ord_z[i][c] is not None]), 4)
                       if v["weighted_leaf_ids"] else None) for c in CITIES}
for d, v in P["level"]["structures"].items():
    mat, bal, sc = {}, {}, {}
    for c in CITIES:
        zs = [ord_z[i][c] for i in v["weighted_leaf_ids"] if ord_z[i][c] is not None]
        if not zs:
            mat[c] = bal[c] = sc[c] = None
            continue
        mat[c] = round(sum(zs) / len(zs), 4)
        bal[c] = entropy_balance(zs)
        sc[c] = round((mat[c] + bal[c]) / 2, 4)
    level_structs[d] = sc
for d, v in P["domain"]["dims"].items():
    domain_dims[d] = {c: (round(sum(ord_z[i][c] for i in v["weighted_leaf_ids"]
                                   if ord_z[i][c] is not None)
                               / len([i for i in v["weighted_leaf_ids"] if ord_z[i][c] is not None]), 4)
                         if v["weighted_leaf_ids"] else None) for c in CITIES}

av_t = P["type"]["available_dims"]
av_l = P["level"]["available"]
av_d = P["domain"]["available_dims"]
ord_T = {c: round(sum(type_dims[d][c] for d in av_t) / len(av_t), 4) for c in CITIES}
ord_L = {c: round(sum(level_structs[d][c] for d in av_l) / len(av_l), 4) for c in CITIES}
ord_D = {c: round(sum(domain_dims[d][c] for d in av_d) / len(av_d), 4) for c in CITIES}
ord_score = {c: round((ord_T[c] + ord_L[c] + ord_D[c]) / 3, 4) for c in CITIES}
ord_rank, ord_order = rank_of(ord_score)

# ---------------------------------------------------------------- 同分并列规则演示
tie_demo_score = {"A": 70.0, "B": 70.0, "C": 55.0, "D": 55.0, "E": 10.0}
tie_demo_rank, _ = rank_of(tie_demo_score)

out = {
    "metric_id": "M_SYNTH_ELEM_RANK",
    "metric_name": "对比范围要素综合排名",
    "support_judgment": "部分支持",
    "verdict_kind": "positive_with_gaps",
    "judgment_reason": (
        "排序算子本身完整可执行（RANK，同分并列下一名跳号），4 城内名次在权重、留一维、"
        "序数归一三种扰动下都不变；但 calc-logic 写死的默认对比范围 11 城里，"
        f"只有广深两城在底册有足量主体，其余 9 城合计仅 {scope_other} 行"
        f"（占底册 {scope_other_pct}%），"
        "做不出可比的极值归一，故默认 11 城榜不可执行，只能出 4 城局部榜——据此判部分支持。"
    ),
    "base_years_used": [2024],
    "base_years_missing": [],
    "base_years_note": (
        "名次是 2024 单年截面名次，不是多年均值名次。2021—2023 未入集（本族单年截面设计），"
        "2025/2026 不完整不进分母。名次只在同一批区域集合内可比——扩城会改极值，名次可能变。"
    ),
    "sources": [
        "gkx @ 183.240.141.251:3318（只读）",
        "code/_snapshots21/synth_elem_panel_20261023.json",
        "code/_snapshots21/base_20261021.json",
        "gkx-orchestration/agent-delivery/metrics/calc-logic/SYNTH/M_SYNTH_ELEM_RANK.md",
    ],
    "panel_snapshot": "code/_snapshots21/synth_elem_panel_20261023.json",
    "script": "code/M_SYNTH_ELEM_RANK.py",
    "regions": CITIES,
    "generated_at": datetime.now(CST).isoformat(timespec="seconds"),
    "elem_index": main_score,
    "rank": main_rank,
    "order": main_order,
    "score_gap_to_next": {
        f"{main_order[i]}->{main_order[i+1]}":
            round(main_score[main_order[i]] - main_score[main_order[i+1]], 4)
        for i in range(len(main_order) - 1)
    },
    "tie_rule": {
        "method": "RANK() OVER (ORDER BY elem_index DESC)，同分并列、下一名跳号",
        "demo_score": tie_demo_score,
        "demo_rank": tie_demo_rank,
        "ties_in_current_panel": len({main_score[c] for c in CITIES}) < len(CITIES),
    },
    "default_scope_feasibility": scope_note,
    "stability": {
        "weight_grid": {
            "step": 0.01,
            "combinations": grid_total,
            "first_place_pct": {c: round(v / grid_total * 100, 4) for c, v in grid_first.items()},
            "second_place_pct": {c: round(v / grid_total * 100, 4) for c, v in grid_second.items()},
            "order_counts": dict(sorted(grid_order.items(), key=lambda kv: -kv[1])),
        },
        "drop_one_dim": drop,
        "ordinal_normalization": {
            "type_index": ord_T, "level_index": ord_L, "domain_index": ord_D,
            "elem_index": ord_score, "rank": ord_rank, "order": ord_order,
            "same_order_as_main": ord_order == main_order,
        },
    },
    "checks": {
        "rank_is_permutation": sorted(main_rank.values()) == [1, 2, 3, 4],
        "index_matches_panel": all(abs(main_score[c] - P["index"]["elem_index"][c]) < 1e-6
                                   for c in CITIES),
        "first_place_stable_all_perturbations": (
            set(grid_first) == {main_order[0]}
            and all(drop[k]["order"][0] == main_order[0] for k in drop)
            and ord_order[0] == main_order[0]),
        "tie_demo_shows_skip": tie_demo_rank["C"] == 3,
    },
    "caveats": [
        "4 城榜不是 11 城榜的子集：少 7 个城，极值 min/max 全变，分数不可与任何外部榜单拼。",
        "名次对权重稳、对「加城」不稳：这是 4 城截面榜的固有性质，不是本件能修的口径问题。",
        "禁止用类型/层次/领域任一单维名次冒充综合名次——领域维单项排序是 深圳>东莞>广州>惠州，"
        "与综合名次不同。",
    ],
}

with open(OUT, "w", encoding="utf-8") as fo:
    json.dump(out, fo, ensure_ascii=False, indent=1)

print("[RANK] ->", OUT)
print("  rank", main_rank, "order", main_order)
print("  scope rows", scope)
print("  ordinal order", ord_order, "same", ord_order == main_order)
print("  checks", out["checks"])
