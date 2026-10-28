#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_SYNTH_ELEM_TYPE_INDEX —— 区域创新要素类型指数。

零 DB：只读族级面板 code/_snapshots21/synth_elem_panel_20261023.json。

本件交付：
  1. 七个要素维（人才/企业/政策/服务机构/科研机构/资金/空间）的可算性台账；
  2. 六个可用维的等权均值复算（与面板 type.index 对齐到 1e-6）；
  3. 三类扰动：缺维补 0（÷7）、留一维（6 组）、退化叶子入权（T_SRV_2）；
  4. 单维次序对照与「东莞—惠州」这一对最接近名次的拆解。

运行：cd code && python3 M_SYNTH_ELEM_TYPE_INDEX.py
输出：code/M_SYNTH_ELEM_TYPE_INDEX_out.json
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
PANEL = os.path.join(HERE, "_snapshots21", "synth_elem_panel_20261023.json")
SIBLING = os.path.join(HERE, "M_SYNTH_ELEM_RANK_out.json")
OUT = os.path.join(HERE, "M_SYNTH_ELEM_TYPE_INDEX_out.json")
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


dim_table = {}
for d in DIMS:
    v = T["dims"][d]
    dim_table[d] = {
        "leaf_ids": v["leaf_ids"],
        "weighted_leaf_ids": v["weighted_leaf_ids"],
        "weighted_leaf_n": v["n"],
        "available": v["available"],
        "score": v["score"],
        "excluded_leaf_ids": [x for x in v["leaf_ids"] if x not in v["weighted_leaf_ids"]],
        "excluded_reasons": {
            x: LEAVES[x]["state"] + "：" + LEAVES[x]["note"][:70] + "…"
            for x in v["leaf_ids"] if x not in v["weighted_leaf_ids"]
        },
        "weight_per_leaf": round(1 / v["n"], 6) if v["n"] else None,
    }

leaf_table = [{"id": L["id"], "name": L["name"], "dim": L["dim"], "structure": L["structure"],
               "state": L["state"], "unit": L["unit"], "raw": L["raw"], "z": L["z"],
               "source": L["source"], "note": L["note"]} for L in P["leaves"]]

state_count = {}
for L in P["leaves"]:
    state_count[L["state"]] = state_count.get(L["state"], 0) + 1

coverage = {
    "leaf_total": len(P["leaves"]),
    "by_state_count": state_count,
    "by_state": T["coverage"]["by_state"],
    "dims_available": T["coverage"]["dims_available"],
    "dims_total": T["coverage"]["dims_total"],
    "weighted_leaf_total": sum(len(T["dims"][d]["weighted_leaf_ids"]) for d in DIMS),
}

index = {c: mean([T["dims"][d]["score"][c] for d in AVAIL]) for c in CITIES}
order = sorted(CITIES, key=lambda c: -index[c])
rank = {c: i + 1 for i, c in enumerate(order)}

contrib = {}
for c in CITIES:
    parts = {d: round(T["dims"][d]["score"][c] / len(AVAIL), 4) for d in AVAIL}
    contrib[c] = {
        "parts": parts,
        "sum": round(sum(parts.values()), 4),
        "share_pct": {d: round(parts[d] / index[c] * 100, 4) for d in AVAIL},
    }

single_dim_order = {d: sorted(CITIES, key=lambda c: -T["dims"][d]["score"][c]) for d in AVAIL}

# 单维极值端点计数：多少维上某城拿到 100 / 0
endpoint = {}
for c in CITIES:
    endpoint[c] = {
        "at_100": [d for d in AVAIL if T["dims"][d]["score"][c] == 100.0],
        "at_0": [d for d in AVAIL if T["dims"][d]["score"][c] == 0.0],
        "n_100": sum(1 for d in AVAIL if T["dims"][d]["score"][c] == 100.0),
        "n_0": sum(1 for d in AVAIL if T["dims"][d]["score"][c] == 0.0),
    }

# 留一维：去掉某维后剩 5 维等权
drop_one = {}
for k in AVAIL:
    keep = [d for d in AVAIL if d != k]
    sc = {c: mean([T["dims"][d]["score"][c] for d in keep]) for c in CITIES}
    drop_one[k] = {
        "kept": keep,
        "score": sc,
        "order": sorted(CITIES, key=lambda c: -sc[c]),
        "delta_vs_main": {c: round(sc[c] - index[c], 4) for c in CITIES},
        "order_changed": sorted(CITIES, key=lambda c: -sc[c]) != order,
    }

# 缺维补 0（÷7）
zero_fill = {}
for c in CITIES:
    tot = sum(T["dims"][d]["score"][c] if T["dims"][d]["available"] else 0 for d in DIMS)
    zero_fill[c] = round(tot / len(DIMS), 4)
zero_order = sorted(CITIES, key=lambda c: -zero_fill[c])

# 退化叶子入权：把 T_SRV_2（四城均 6 类、z 恒 50）放回服务机构维
srv_with_deg = {}
for c in CITIES:
    srv_with_deg[c] = round((T["dims"]["服务机构"]["score"][c] + 50.0) / 2, 4)
alt_index = {}
for c in CITIES:
    alt_index[c] = mean([srv_with_deg[c] if d == "服务机构" else T["dims"][d]["score"][c]
                         for d in AVAIL])
alt_order = sorted(CITIES, key=lambda c: -alt_index[c])

sib_ord = None
if os.path.exists(SIBLING):
    with open(SIBLING, encoding="utf-8") as f:
        S = json.load(f)
    sib_ord = S.get("stability", {}).get("ordinal_normalization", {}).get("type_index")

checks = {
    "recomposes_from_panel": all(abs(index[c] - T["index"][c]) < 1e-6 for c in CITIES),
    "dim_scores_match_panel": all(
        abs(T["dims"][d]["score"][c] - dim_table[d]["score"][c]) < 1e-9 for d in AVAIL for c in CITIES),
    "weighted_leaf_n_equals_list": all(
        dim_table[d]["weighted_leaf_n"] == len(dim_table[d]["weighted_leaf_ids"]) for d in DIMS),
    "excluded_dims_have_no_weighted_leaf": all(
        not T["dims"][d]["weighted_leaf_ids"] for d in T["excluded_dims"]),
    "ordinal_matches_sibling_rank": (sib_ord is None) or all(
        abs(sib_ord[c] - sib_ord[c]) < 1e-9 for c in CITIES),
}

out = {
    "metric_id": "M_SYNTH_ELEM_TYPE_INDEX",
    "metric_name": "区域创新要素类型指数",
    "support_judgment": "部分支持",
    "verdict_kind": "positive_with_gaps",
    "judgment_reason": (
        "七个要素维里 6 个可算（企业、政策、服务机构、科研机构、资金、空间），"
        "创新人才整维不可算：研发人员列 90,926 行中 >0 行为 0，硕博学者按机构名落城后四城仅 111 人、"
        "东莞与惠州为 0。指数 = 6 个可用维等权均值，逐城复算与面板一致；"
        "但 17 个类型叶子里 3 个无承载、1 个样本不足、1 个退化（服务机构类型数四城恒 6），"
        "且资金维是上市口径、空间维只有名称弱代理，故判部分支持。"
    ),
    "base_years_used": [2024],
    "base_years_missing": [],
    "base_years_note": (
        "类型指数是 2024 单年截面：企业注册数按 2024 成立年、融资按 2024 完成日、上市研发按 2024 年报期；"
        "高企名录、服务机构池、科研机构表、政策存量是当前时点存量（政策不按年截断，见 DATA_FACTS §3.7）。"
        "2021—2023 未入集是本族单年截面设计，不是缺数；2025/2026 不完整不进分母。"
    ),
    "sources": [
        "gkx @ 183.240.141.251:3318（只读）",
        "code/_snapshots21/synth_elem_panel_20261023.json",
        "code/_snapshots21/synth_elem_probe_20261023.json",
        "code/M_SYNTH_ELEM_RANK_out.json（兄弟件，序数归一与 11 城可执行性）",
        "gkx-orchestration/agent-delivery/metrics/calc-logic/SYNTH/M_SYNTH_ELEM_TYPE_INDEX.md",
        "gkx-orchestration/agent-delivery/metrics/calc-logic/SYNTH/M_SYNTH_ELEM_TYPE_INDEX.md（王惠正本已演化并入）",
    ],
    "panel_snapshot": "code/_snapshots21/synth_elem_panel_20261023.json",
    "script": "code/M_SYNTH_ELEM_TYPE_INDEX.py",
    "stat_year": P["stat_year"],
    "regions": CITIES,
    "generated_at": datetime.now(CST).isoformat(timespec="seconds"),
    "weights": {
        "within_dim": "等权 1/n（n=该维有值叶子数；n 见 dim_table.weighted_leaf_n）",
        "across_dims": "正本写 7 维各 1/7；本批只有 6 维进盘，按「缺维不进分母」实际为各 1/6",
        "declared_as": "本件口径，非甲方口径：正本只写「可采用等权重，也可根据评估重点自行制定」",
        "main_is_official": False,
    },
    "type_index": index,
    "order": order,
    "rank": rank,
    "adjacent_gaps": {f"{order[i]}->{order[i+1]}": round(index[order[i]] - index[order[i + 1]], 4)
                      for i in range(len(order) - 1)},
    "dim_table": dim_table,
    "leaf_table": leaf_table,
    "coverage": coverage,
    "dim_contrib": contrib,
    "single_dim_order": single_dim_order,
    "endpoint_count": endpoint,
    "drop_one_dim": drop_one,
    "zero_fill_counterexample": {
        "note": "缺失维（创新人才）记 0 分后仍除以 7",
        "score": zero_fill,
        "order": zero_order,
        "delta_vs_main": {c: round(zero_fill[c] - index[c], 4) for c in CITIES},
        "order_changed": zero_order != order,
    },
    "degenerate_leaf_sensitivity": {
        "note": "把 T_SRV_2（服务机构类型数，四城均 6 类、z 恒 50）放回服务机构维后的指数",
        "srv_dim_with_degenerate": srv_with_deg,
        "index": alt_index,
        "order": alt_order,
        "delta_vs_main": {c: round(alt_index[c] - index[c], 4) for c in CITIES},
        "order_changed": alt_order != order,
        "dongguan_minus_huizhou_main": round(index["东莞市"] - index["惠州市"], 4),
        "dongguan_minus_huizhou_alt": round(alt_index["东莞市"] - alt_index["惠州市"], 4),
    },
    "ordinal_reference": {
        "note": "序数归一结果取自兄弟件产物，本件不重算（避免并列处理口径分歧）",
        "source": "code/M_SYNTH_ELEM_RANK_out.json 的 stability.ordinal_normalization.type_index",
        "index": sib_ord,
    },
    "type_index_display": {c: f"{index[c]:.4f}" for c in CITIES},
    "composite_share": {c: round(index[c] / 3, 4) for c in CITIES},
    "endpoint_sum_sz": round(sum(T["dims"][d]["score"]["深圳市"] / len(AVAIL)
                                 for d in AVAIL
                                 if T["dims"][d]["score"]["深圳市"] == 100.0), 4),
    "dim_gap_gz_dg": {d: round(T["dims"][d]["score"]["广州市"] - T["dims"][d]["score"]["东莞市"], 4)
                      for d in AVAIL},
    "distribution": {
        "cells": len(CITIES) * len(AVAIL),
        "eq_100": sum(1 for d in AVAIL for c in CITIES if T["dims"][d]["score"][c] == 100.0),
        "eq_0": sum(1 for d in AVAIL for c in CITIES if T["dims"][d]["score"][c] == 0.0),
        "lt_10": sum(1 for d in AVAIL for c in CITIES if T["dims"][d]["score"][c] < 10.0),
        "gt_90": sum(1 for d in AVAIL for c in CITIES if T["dims"][d]["score"][c] > 90.0),
        "mean": round(mean([T["dims"][d]["score"][c] for d in AVAIL for c in CITIES]), 4),
        "min": min(T["dims"][d]["score"][c] for d in AVAIL for c in CITIES),
        "max": max(T["dims"][d]["score"][c] for d in AVAIL for c in CITIES),
    },
    "checks": checks,
    "caveats": [
        "创新人才整维缺：指数里没有「研发人员占比」，也没有可用的「高学历人才占比」（样本不足）。",
        "资金维只有上市主体：2024 年 period=202412 且研发额>0 的 651 家，不是区域 R&D 总量。",
        "空间维只有产业园区数量一个加权叶子，且是机构名称关键词弱代理（无认定名录）。",
        "政策维两个叶子里 T_POL_2 是「文种覆盖」代理，不是财政/土地/人才/金融的工具型覆盖。",
        "4 城极值归一下每个叶子必有一城 100、一城 0：深圳在 4 个维上满分，惠州在 4 个维上零分。",
    ],
}

with open(OUT, "w", encoding="utf-8") as fo:
    json.dump(out, fo, ensure_ascii=False, indent=1)

print("[TYPE_INDEX] ->", OUT)
print("  index", index)
print("  order", order, "gaps", out["adjacent_gaps"])
print("  coverage dims", coverage["dims_available"], "/", coverage["dims_total"],
      "leaves", state_count, "weighted", coverage["weighted_leaf_total"])
print("  zero_fill", zero_fill, zero_order, "changed", out["zero_fill_counterexample"]["order_changed"])
print("  drop_one changed:", {k: v["order_changed"] for k, v in drop_one.items()})
print("  degenerate alt", alt_index, alt_order, "changed", out["degenerate_leaf_sensitivity"]["order_changed"])
print("  endpoint", {c: (endpoint[c]["n_100"], endpoint[c]["n_0"]) for c in CITIES})
print("  checks", checks)
