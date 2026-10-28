#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_SYNTH_ELEM_WEIGHT —— 类型/层次/领域权重分布（1/3×3 + 敏感性三件套）。

本件输出四样东西：
  1. 主权重（三维各 1/3）与四城 elem_score 复算；
  2. `main_is_official = false` 的书面结论（甲方未给 AHP 矩阵/专家打分）；
  3. 客观参照：4 城 × 3 维的熵权，以及等权 vs 熵权的排序对照；
  4. 翻转阈值：某个维权重单独抬到多少，第一名/第二名会换人；再给 0.01 步长
     单纯形网格（5,151 组）的首名/次名占比。

运行：cd code && python3 M_SYNTH_ELEM_WEIGHT.py
输出：code/M_SYNTH_ELEM_WEIGHT_out.json
"""
from __future__ import annotations

import json
import math
import os
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
PANEL = os.path.join(HERE, "_snapshots21", "synth_elem_panel_20261023.json")
OUT = os.path.join(HERE, "M_SYNTH_ELEM_WEIGHT_out.json")
CST = timezone(timedelta(hours=8))

with open(PANEL, encoding="utf-8") as f:
    P = json.load(f)

CITIES = P["regions"]
T = P["index"]["type_index"]
L = P["index"]["level_index"]
D = P["index"]["domain_index"]
W = {"type": 1 / 3, "level": 1 / 3, "domain": 1 / 3}

DIMS = ["type", "level", "domain"]
DIM_CN = {"type": "类型维", "level": "层次维", "domain": "领域维"}
SCORE = {"type": T, "level": L, "domain": D}


def composite(w):
    return {c: w["type"] * T[c] + w["level"] * L[c] + w["domain"] * D[c] for c in CITIES}


def ranked(sc):
    return sorted(CITIES, key=lambda c: -sc[c])


main_score = {c: round(composite(W)[c], 4) for c in CITIES}
main_order = ranked(main_score)

# ---------------------------------------------------------------- 熵权参照
# 4 城 × 3 维，列内按城归一后算信息熵；d=1-e，再归一为熵权。
ent = {}
for d in DIMS:
    vals = [SCORE[d][c] for c in CITIES]
    tot = sum(vals)
    ps = [v / tot for v in vals if v > 0]
    h = -sum(p * math.log(p) for p in ps)
    ent[d] = round(h / math.log(len(vals)), 6)
div = {d: round(1 - ent[d], 6) for d in DIMS}
div_sum = sum(div.values())
ent_w = {d: round(div[d] / div_sum, 6) for d in DIMS}

ent_score = {c: round(sum(ent_w[d] * SCORE[d][c] for d in DIMS), 4) for c in CITIES}
ent_order = ranked(ent_score)

# ---------------------------------------------------------------- 弹性：单维 +0.10 后其余按比例收缩
elastic = {}
for d in DIMS:
    w2 = {}
    for k in DIMS:
        w2[k] = W[k] + 0.10 if k == d else W[k] - 0.10 / 2
    sc = composite(w2)
    elastic[d] = {
        "weights_after": {k: round(v, 6) for k, v in w2.items()},
        "score": {c: round(sc[c], 4) for c in CITIES},
        "delta_vs_main": {c: round(sc[c] - main_score[c], 4) for c in CITIES},
        "order": ranked(sc),
        "order_changed": ranked(sc) != main_order,
    }

# ---------------------------------------------------------------- 翻转阈值（解析）
# 固定第三维 = 1/3、另两维在 2/3 内对调：S_i(t) = t*X_i + (2/3-t)*Y_i + (1/3)*Z_i
# 两城打平的 t* = [ (2/3)(Y_j-Y_i) + (1/3)(Z_j-Z_i) ] / [ (Y_j-Y_i) - (X_j-X_i) ]
def flip_t(a, b, x, y, z):
    """在第三维固定 1/3 的 2 维盘上，b 追上 a 时的 t（a 的权重），无解返回 None。"""
    dy = y[b] - y[a]
    dz = z[b] - z[a]
    dx = x[b] - x[a]
    num = (2 / 3) * dy + (1 / 3) * dz
    den = dx - dy
    if abs(den) < 1e-12:
        return None
    t = -num / den
    return t if -1e-9 <= t <= 2 / 3 + 1e-9 else None


flips = {}
for xk, yk, zk in [("type", "level", "domain"), ("level", "type", "domain"),
                   ("type", "domain", "level"), ("domain", "type", "level")]:
    key = f"{xk}_vs_{yk}_with_{zk}_fixed"
    flips[key] = {}
    for a, b in [(main_order[0], main_order[1]), (main_order[1], main_order[2]),
                 (main_order[2], main_order[3])]:
        t = flip_t(a, b, SCORE[xk], SCORE[yk], SCORE[zk])
        flips[key][f"{b}>={a}"] = None if t is None else round(t, 6)

# ---------------------------------------------------------------- 单纯形网格
grid = []
step = 0.01
n = int(round(1 / step))
counts_first = {c: 0 for c in CITIES}
counts_second = {c: 0 for c in CITIES}
counts_order = {}
flip_second_domain = None
for i in range(n + 1):
    for j in range(n + 1 - i):
        k = n - i - j
        w = {"type": i / n, "level": j / n, "domain": k / n}
        sc = composite(w)
        order = ranked(sc)
        counts_first[order[0]] += 1
        counts_second[order[1]] += 1
        key = ">".join(order)
        counts_order[key] = counts_order.get(key, 0) + 1
        if order[1] == "东莞市" and flip_second_domain is None:
            flip_second_domain = round(w["domain"], 4)
        grid.append(w)

total_grid = len(grid)
first_share = {c: round(v / total_grid * 100, 4) for c, v in counts_first.items()}
second_share = {c: round(v / total_grid * 100, 4) for c, v in counts_second.items()}

# 东莞在第二名出现时的最小 w_domain（= 广州被挤出前二的门槛）
dom_min_for_dg_second = None
for w in grid:
    sc = composite(w)
    order = ranked(sc)
    if order[0] == "深圳市" and order[1] == "东莞市":
        if dom_min_for_dg_second is None or w["domain"] < dom_min_for_dg_second:
            dom_min_for_dg_second = round(w["domain"], 4)

out = {
    "metric_id": "M_SYNTH_ELEM_WEIGHT",
    "metric_name": "类型/层次/领域权重分布",
    "support_judgment": "部分支持",
    "verdict_kind": "positive_with_gaps",
    "judgment_reason": (
        "权重的算术部分可算且闭合（三维各 1/3、合计 1，四城 elem_score 与 "
        "M_SYNTH_ELEM_INDEX 逐城一致），但权重本身不是甲方标定值：calc-logic 明写"
        "「可采用等权重，也可根据评估重点自行制定」，上游另标 is_mock: true、"
        "Q-SYNTH-E-01 仍 🟡，且这 1/3 落在的两个维（类型、领域）各自还有整维缺失，"
        "故判部分支持——公式能跑，权重没有权威出处。"
    ),
    "base_years_used": [2024],
    "base_years_missing": [],
    "base_years_note": (
        "权重是结构性参数，不带年份；被加权的三条维指数都是 2024 单年截面。"
        "2021—2023 未入集（本族设计为单年截面），2025/2026 不完整不进分母。"
        "权重不随年份重估——若要按年重估熵权，需先把 2021—2023 的叶子补齐。"
    ),
    "sources": [
        "gkx @ 183.240.141.251:3318（只读）",
        "code/_snapshots21/synth_elem_panel_20261023.json",
        "gkx-orchestration/agent-delivery/metrics/calc-logic/SYNTH/M_SYNTH_ELEM_WEIGHT.md",
        "gkx-orchestration/agent-delivery/metrics/calc-logic/SYNTH/M_SYNTH_ELEM_INDEX.md",
    ],
    "panel_snapshot": "code/_snapshots21/synth_elem_panel_20261023.json",
    "script": "code/M_SYNTH_ELEM_WEIGHT.py",
    "regions": CITIES,
    "generated_at": datetime.now(CST).isoformat(timespec="seconds"),
    "weights": {
        "main": {k: round(v, 10) for k, v in W.items()},
        "main_sum": round(sum(W.values()), 12),
        "main_is_official": False,
        "official_evidence_found": False,
        "official_gap": "无 AHP 判断矩阵、无专家打分记录、无熵权原始计算表；"
                        "calc-logic 把权重写成「可采用等权重，也可自行制定」，"
                        "即甲方未定值。上游标 is_mock: true，Q-SYNTH-E-01 仍 🟡。",
        "declared_as": "本件自拟（沿 calc-logic 的 1/3 等权占位，不称官方值）",
    },
    "dim_scores": {d: {c: SCORE[d][c] for c in CITIES} for d in DIMS},
    "elem_score": main_score,
    "elem_order": main_order,
    "entropy_reference": {
        "entropy": ent,
        "divergence": div,
        "weights": ent_w,
        "score": ent_score,
        "order": ent_order,
        "order_equals_main": ent_order == main_order,
        "note": "4 城样本算熵权只有 4 个观测/列，熵值本身极不稳定（n=4 时 H/ln4 上限被"
                "样本量压住），只作客观参照，不替换主权重。",
    },
    "elasticity": elastic,
    "flip_thresholds": flips,
    "simplex_grid": {
        "step": step,
        "combinations": total_grid,
        "first_place_share_pct": first_share,
        "second_place_share_pct": second_share,
        "order_counts": dict(sorted(counts_order.items(), key=lambda kv: -kv[1])),
        "min_domain_weight_for_dongguan_second": dom_min_for_dg_second,
        "conclusion": "首名在 5,151 组权重里恒为深圳；第二名在领域权重大于门槛后由广州换成东莞，"
                      "第三/第四名互换的门槛更高。名次的「谁第一」对权重不敏感，"
                      "「第二是谁」对权重敏感——这是本件最重要的结论。",
    },
    "checks": {
        "weights_sum_to_one": abs(sum(W.values()) - 1) < 1e-12,
        "elem_score_equals_index": all(
            abs(main_score[c] - P["index"]["elem_index"][c]) < 1e-6 for c in CITIES),
        "grid_covers_simplex": total_grid == (n + 1) * (n + 2) // 2,
        "entropy_weights_sum_to_one": abs(sum(ent_w.values()) - 1) < 1e-6,
    },
}

with open(OUT, "w", encoding="utf-8") as fo:
    json.dump(out, fo, ensure_ascii=False, indent=1)

print("[WEIGHT] ->", OUT)
print("  main weights", out["weights"]["main"], "sum", out["weights"]["main_sum"])
print("  elem_score", main_score)
print("  entropy w", ent_w, "order", ent_order)
print("  simplex", total_grid, "first", first_share, "second", second_share)
print("  checks", out["checks"])
