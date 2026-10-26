#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SYNTH_ELEM_INDEX —— 区域创新要素指数（综合）。

三个维指数按 1/3 加权合成，并给出四类可复核证据：
  1. 逐城复算（与面板 elem_index 对齐到 1e-6）；
  2. 维度贡献分解（w_k × 维分 ÷ 总分）；
  3. 留一维（drop-one）后重归一，看分数与名次怎么动；
  4. 单维读法对照：只看某一维时四城名次完全不同（领域维东莞第二），
     说明合成分不是「三维一致同意」的结果，1/3 这个权在第二名的判定上是决定性的。

运行：cd code && python3 M_SYNTH_ELEM_INDEX.py
输出：code/M_SYNTH_ELEM_INDEX_out.json
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
PANEL = os.path.join(HERE, "_snapshots21", "synth_elem_panel_20261023.json")
OUT = os.path.join(HERE, "M_SYNTH_ELEM_INDEX_out.json")
CST = timezone(timedelta(hours=8))

with open(PANEL, encoding="utf-8") as f:
    P = json.load(f)

CITIES = P["regions"]
T = P["index"]["type_index"]
L = P["index"]["level_index"]
D = P["index"]["domain_index"]
W = 1 / 3

score = {c: round(W * (T[c] + L[c] + D[c]), 4) for c in CITIES}
order = sorted(CITIES, key=lambda c: -score[c])

decomp = {}
for c in CITIES:
    parts = {"type": W * T[c], "level": W * L[c], "domain": W * D[c]}
    decomp[c] = {
        "type": round(parts["type"], 4),
        "level": round(parts["level"], 4),
        "domain": round(parts["domain"], 4),
        "share_type_pct": round(parts["type"] / score[c] * 100, 4),
        "share_level_pct": round(parts["level"] / score[c] * 100, 4),
        "share_domain_pct": round(parts["domain"] / score[c] * 100, 4),
        "sum_equals_score": abs(round(sum(parts.values()), 4) - score[c]) < 1e-9,
    }

# 留一维：剩两维各 1/2
drop = {}
for k in ("type", "level", "domain"):
    keep = [x for x in ("type", "level", "domain") if x != k]
    sc = {}
    for c in CITIES:
        sc[c] = round((T[c] if "type" in keep else 0) / 2
                      + (L[c] if "level" in keep else 0) / 2
                      + (D[c] if "domain" in keep else 0) / 2, 4)
    drop[k] = {
        "kept": keep,
        "score": sc,
        "order": sorted(CITIES, key=lambda c: -sc[c]),
        "delta_vs_main": {c: round(sc[c] - score[c], 4) for c in CITIES},
        "order_changed": sorted(CITIES, key=lambda c: -sc[c]) != order,
    }

single = {}
for k, vec in (("type", T), ("level", L), ("domain", D)):
    single[k] = {
        "score": {c: vec[c] for c in CITIES},
        "order": sorted(CITIES, key=lambda c: -vec[c]),
    }

# 名次分差：相邻两城的分数差，解释「换一名要多少分」
gaps = {}
for i in range(len(order) - 1):
    gaps[f"{order[i]}->{order[i+1]}"] = round(score[order[i]] - score[order[i + 1]], 4)

out = {
    "metric_id": "M_SYNTH_ELEM_INDEX",
    "metric_name": "区域创新要素指数（综合）",
    "support_judgment": "部分支持",
    "verdict_kind": "positive_with_gaps",
    "judgment_reason": (
        "三维指数的算术链在本批 4 城上完全闭合（elem_index = 三维均值，逐城复算一致），"
        "但两个输入维本身带缺：类型维 7 个维里创新人才维整维不可算（研发人员列 0 行灌数、"
        "硕博学者仅 111 人），领域维 5 个维只出 3 个（GDP 与规上工业营收无承载），"
        "且权重是自拟 1/3 而非甲方标定。合成分照跑，但只能读作「4 城内相对位置」，"
        "不能对外当绝对水平，故判部分支持。"
    ),
    "base_years_used": [2024],
    "base_years_missing": [],
    "base_years_note": (
        "综合指数是 2024 单年截面，三个维指数同为 2024。2021—2023 未入集（本族设计为单年截面，"
        "不是缺数）；2025/2026 专利与年报不完整，不进分母。极值归一的 min/max 取本批 4 城，"
        "不做跨年、跨批次比较——换一批区域，同一个城的分数必然变。"
    ),
    "sources": [
        "gkx @ 183.240.141.251:3318（只读）",
        "code/_snapshots21/synth_elem_panel_20261023.json",
        "code/_snapshots21/synth_elem_probe_20261023.json",
        "gkx-orchestration/agent-delivery/metrics/calc-logic/SYNTH/M_SYNTH_ELEM_INDEX.md",
    ],
    "panel_snapshot": "code/_snapshots21/synth_elem_panel_20261023.json",
    "script": "code/M_SYNTH_ELEM_INDEX.py",
    "regions": CITIES,
    "generated_at": datetime.now(CST).isoformat(timespec="seconds"),
    "weights": {"w_type": round(W, 10), "w_level": round(W, 10), "w_domain": round(W, 10),
                "sum": round(3 * W, 12), "main_is_official": False},
    "dim_index": {"type_index": T, "level_index": L, "domain_index": D},
    "elem_index": score,
    "order": order,
    "rank": {c: i + 1 for i, c in enumerate(order)},
    "decomposition": decomp,
    "drop_one_dim": drop,
    "single_dim_reading": single,
    "adjacent_gaps": gaps,
    "panel_values_match": all(abs(score[c] - P["index"]["elem_index"][c]) < 1e-6 for c in CITIES),
    "checks": {
        "recomposes_from_panel": P["checks"]["elem_index_recomposes"],
        "weights_sum_to_one": abs(3 * W - 1) < 1e-12,
        "decomp_sums_to_score": all(decomp[c]["sum_equals_score"] for c in CITIES),
        "single_dim_orders_differ": len({tuple(single[k]["order"]) for k in single}) > 1,
    },
    "caveats": [
        "4 城极值归一：每个叶子必有一城 100、一城 0，因此综合分天然被拉到 0—100 的两端，"
        "中段没有任何城，100 与 0 都不代表绝对水平。",
        "类型维只有 6/7 维进均值（创新人才维整维缺），等于人才要素在总分里权重为 0；"
        "这是「缺维不进分母」的必然结果，不是把人才当 0 分。",
        "领域维只有 3/5 维进均值，且领域维内部东莞高于广州（49.1351 vs 29.1012），"
        "与类型维、层次维的次序相反；综合分第二名由 1/3 的权重决定，属结构选择而非数据结论。",
    ],
}

with open(OUT, "w", encoding="utf-8") as fo:
    json.dump(out, fo, ensure_ascii=False, indent=1)

print("[INDEX] ->", OUT)
print("  elem_index", score, "order", order)
print("  adjacent gaps", gaps)
print("  checks", out["checks"])
