#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_SYNTH_ELEM_DOMAIN_INDEX —— 区域创新要素领域指数。

零 DB：只读族级面板 code/_snapshots21/synth_elem_panel_20261023.json。
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
PANEL = os.path.join(HERE, "_snapshots21", "synth_elem_panel_20261023.json")
SIBLING = os.path.join(HERE, "M_SYNTH_ELEM_RANK_out.json")
OUT = os.path.join(HERE, "M_SYNTH_ELEM_DOMAIN_INDEX_out.json")
CST = timezone(timedelta(hours=8))

with open(PANEL, encoding="utf-8") as f:
    P = json.load(f)

CITIES = P["regions"]
DOM = P["domain"]
DIMS = list(DOM["dims"].keys())
LEAVES = {L["id"]: L for L in P["domain_leaves"]}


def mean(xs):
    xs = [x for x in xs if x is not None]
    return round(sum(xs) / len(xs), 4) if xs else None


dim_table = {}
for d, v in DOM["dims"].items():
    dim_table[d] = {
        "leaf_ids": v["leaf_ids"],
        "weighted_leaf_ids": v["weighted_leaf_ids"],
        "weighted_leaf_n": v["n"],
        "available": v["available"],
        "score": v["score"],
        "excluded_leaf_ids": [x for x in v["leaf_ids"] if x not in v["weighted_leaf_ids"]],
        "excluded_reasons": {
            x: LEAVES[x]["state"] + "：" + LEAVES[x]["note"][:60] + "…"
            for x in v["leaf_ids"] if x not in v["weighted_leaf_ids"]
        },
    }

leaf_table = []
for lid, L in LEAVES.items():
    leaf_table.append({
        "id": lid,
        "name": L["name"],
        "dim": L["dim"],
        "state": L["state"],
        "raw": L["raw"],
        "z": L["z"],
        "source": L["source"],
        "note": L["note"],
    })

state_count = {}
for L in P["domain_leaves"]:
    state_count[L["state"]] = state_count.get(L["state"], 0) + 1

coverage = {
    "leaf_total": len(P["domain_leaves"]),
    "by_state_count": state_count,
    "by_state": DOM["coverage"]["by_state"],
    "dims_available": DOM["coverage"]["dims_available"],
    "dims_total": DOM["coverage"]["dims_total"],
}

index = {}
for c in CITIES:
    vals = [dim_table[d]["score"][c] for d in DIMS if dim_table[d]["available"]]
    index[c] = mean(vals)
order = sorted(CITIES, key=lambda c: -index[c])
rank = {c: i + 1 for i, c in enumerate(order)}

contrib = {}
for c in CITIES:
    parts = {d: round(dim_table[d]["score"][c] / 3, 4) for d in DIMS if dim_table[d]["available"]}
    contrib[c] = {
        "parts": parts,
        "sum": round(sum(parts.values()), 4),
        "share_pct": {d: round(parts[d] / index[c] * 100, 4)
                      for d in DIMS if dim_table[d]["available"]},
    }

single_dim_order = {d: sorted(CITIES, key=lambda c: -dim_table[d]["score"][c])
                    for d in DIMS if dim_table[d]["available"]}

zero_fill = {}
for c in CITIES:
    tot = sum(dim_table[d]["score"][c] if dim_table[d]["available"] else 0 for d in DIMS)
    zero_fill[c] = round(tot / len(DIMS), 4)
zero_order = sorted(CITIES, key=lambda c: -zero_fill[c])


def ordinal_vec(vals: dict):
    uniq = sorted(set(vals.values()))
    if len(uniq) != len(vals):
        return None
    step = 100.0 / (len(vals) - 1)
    return {c: round(uniq.index(vals[c]) * step, 4) for c in vals}


ord_dims = {}
for d in DIMS:
    if not dim_table[d]["available"]:
        ord_dims[d] = {c: None for c in CITIES}
        continue
    per_leaf = {}
    ok = True
    for lid in dim_table[d]["weighted_leaf_ids"]:
        v = ordinal_vec(LEAVES[lid]["raw"])
        if v is None:
            ok = False
            break
        per_leaf[lid] = v
    ord_dims[d] = {c: mean([per_leaf[l][c] for l in per_leaf]) for c in CITIES} if ok else \
        {c: None for c in CITIES}

ordinal = {c: mean([ord_dims[d][c] for d in DIMS if ord_dims[d][c] is not None]) for c in CITIES}
ord_order = sorted(CITIES, key=lambda c: -ordinal[c])
ord_gap_gz_dg = round(ordinal["广州市"] - ordinal["东莞市"], 4)

city_all = P["population"]["city_all"]
city_alive = P["population"]["city_alive"]
d2 = LEAVES["D2_1"]
# raw = 授权件 / 存续企业数 × 10000 → 换分母时乘 alive/all（不是除）
raw_all = {c: round(d2["raw"][c] * city_alive[c] / city_all[c], 2) for c in CITIES}
lo, hi = min(raw_all.values()), max(raw_all.values())
d2_all_z = {c: round((raw_all[c] - lo) / (hi - lo) * 100, 4) for c in CITIES}

alt_dim = {d: dict(dim_table[d]["score"]) for d in DIMS if dim_table[d]["available"]}
alt_dim["技术领域应用深度"] = d2_all_z
alt_index = {c: mean([alt_dim[d][c] for d in alt_dim]) for c in CITIES}
alt_order = sorted(CITIES, key=lambda c: -alt_index[c])

sib_ord = None
if os.path.exists(SIBLING):
    with open(SIBLING, encoding="utf-8") as f:
        S = json.load(f)
    sib_ord = S.get("stability", {}).get("ordinal_normalization", {}).get("domain_index")

checks = {
    "recomposes_from_panel": all(abs(index[c] - DOM["index"][c]) < 1e-6 for c in CITIES),
    "dim_scores_match_panel": all(
        abs(dim_table[d]["score"][c] - DOM["dims"][d]["score"][c]) < 1e-9
        for d in DIMS if dim_table[d]["available"] for c in CITIES),
    "weighted_leaf_n_equals_list": all(
        dim_table[d]["weighted_leaf_n"] == len(dim_table[d]["weighted_leaf_ids"]) for d in DIMS),
    "ordinal_matches_sibling_rank": (sib_ord is None) or all(
        abs(ordinal[c] - sib_ord[c]) < 1e-3 for c in CITIES),
    "zero_fill_changes_order": zero_order != order,
}

out = {
    "metric_id": "M_SYNTH_ELEM_DOMAIN_INDEX",
    "metric_name": "区域创新要素领域指数",
    "support_judgment": "部分支持",
    "verdict_kind": "positive_with_gaps",
    "judgment_reason": (
        "领域指数要求的五个维里只有 3 个能从 gkx 侧凑出可加权叶子（产业领域覆盖广度、"
        "技术领域应用深度、创新产出强度），人才结构合理性与经济贡献度两维在 2024 年四城上零承载："
        "规上工业增加值与地区生产总值在 dwd_macro_index_data 里四城均无 2024 行，"
        "研发人员列整列为空、硕博学者四城仅 111 人。三条可用维的等权均值可复算且与面板逐城一致，"
        "但指数只覆盖 3/5 维、其中 2 个维只有 1 个加权叶子，且 D2_1 分母为存续口径——"
        "按「始终有部分依赖维度无法得到足够数据」判部分支持。"
    ),
    "base_years_used": [2024],
    "base_years_missing": [],
    "base_years_note": (
        "领域指数是 2024 单年截面：分子侧专利为 2024 授权年、政策为全库存量（不按年截断，"
        "见 DATA_FACTS §3.7）、高企与服务机构池为当前名录。2021—2023 未入集是本族单年截面设计，"
        "不是缺数；2025/2026 专利与年报不完整，不进分母。极值归一 min/max 取本批 4 城，"
        "换一批城市同一城的分数必然变。"
    ),
    "sources": [
        "gkx @ 183.240.141.251:3318（只读）",
        "code/_snapshots21/synth_elem_panel_20261023.json",
        "code/_snapshots21/synth_elem_probe_20261023.json",
        "code/M_SYNTH_ELEM_RANK_out.json（兄弟件，序数归一与 11 城可执行性）",
        "gkx-orchestration/agent-delivery/metrics/calc-logic/SYNTH/M_SYNTH_ELEM_DOMAIN_INDEX.md",
        "（王惠正本已并入 calc-logic 入库件）",
    ],
    "panel_snapshot": "code/_snapshots21/synth_elem_panel_20261023.json",
    "script": "code/M_SYNTH_ELEM_DOMAIN_INDEX.py",
    "stat_year": P["stat_year"],
    "regions": CITIES,
    "generated_at": datetime.now(CST).isoformat(timespec="seconds"),
    "weights": {
        "within_dim": "等权 1/n（n=该维有值叶子数）",
        "across_dims": "正本写 5 维各 1/5；本批只有 3 维进盘，按「缺维不进分母」实际为各 1/3",
        "declared_as": "本件口径，非甲方口径：正本只写「可采用等权重，也可根据评估重点自行制定」，无甲方标定值",
        "main_is_official": False,
    },
    "domain_index": index,
    "order": order,
    "rank": rank,
    "adjacent_gaps": {f"{order[i]}->{order[i+1]}": round(index[order[i]] - index[order[i + 1]], 4)
                      for i in range(len(order) - 1)},
    "dim_table": dim_table,
    "leaf_table": leaf_table,
    "coverage": coverage,
    "dim_contrib": contrib,
    "single_dim_order": single_dim_order,
    "zero_fill_counterexample": {
        "note": "把 5 个维都摊开、缺失维记 0 分仍除以 5（正本未写缺维规则；本族按「不进分母」执行）",
        "score": zero_fill,
        "order": zero_order,
        "delta_vs_main": {c: round(zero_fill[c] - index[c], 4) for c in CITIES},
        "order_changed": zero_order != order,
    },
    "ordinal_normalization": {
        "note": "每叶四城原值换成 0/33.3333/66.6667/100 后按同一聚合规则重算",
        "dim_scores": ord_dims,
        "index": ordinal,
        "order": ord_order,
        "gap_guangzhou_minus_dongguan": ord_gap_gz_dg,
        "tie_band": abs(ord_gap_gz_dg) < 0.01,
        "source": "本件按面板 raw 值重算；与 code/M_SYNTH_ELEM_RANK_out.json 的 "
                  "stability.ordinal_normalization.domain_index 对照",
    },
    "d2_denominator_counterfactual": {
        "note": "D2_1 分母由「存续企业数」换回「底册全量行数」，分子不变（2024 授权件）",
        "denominator_alive": city_alive,
        "denominator_all": city_all,
        "alive_rate_pct": {c: round(city_alive[c] / city_all[c] * 100, 4) for c in CITIES},
        "raw_alive": d2["raw"],
        "raw_all_denominator": raw_all,
        "z_all_denominator": d2_all_z,
        "spread_alive": round(max(d2["raw"].values()) - min(d2["raw"].values()), 2),
        "spread_all": round(max(raw_all.values()) - min(raw_all.values()), 2),
        "alive_rate_gap_pct": {c: round(100 - city_alive[c] / city_all[c] * 100, 4)
                               for c in CITIES},
        "by_city": {c: {"d21_alt": round(raw_all[c], 2),
                        "z_alt": d2_all_z[c],
                        "index_alt": alt_index[c],
                        "index_delta": round(alt_index[c] - index[c], 4)}
                    for c in CITIES},
        "index": alt_index,
        "order": alt_order,
        "order_changed": alt_order != order,
    },
    "gap_sz_gz": round(index["深圳市"] - index["广州市"], 4),
    "gap_head_tail": round(index["深圳市"] - index["惠州市"], 4),
    "checks": checks,
    "caveats": [
        "五维只出三维：人才结构合理性与经济贡献度整维空缺，指数不含「人才」与「经济贡献」两块内容。",
        "产业领域覆盖广度与技术领域应用深度各只有 1 个加权叶子（D1_1、D2_1），"
        "这两维的「均值」实际等于单个叶子的极值归一得分，没有维内平均的平滑作用。",
        "D2_1 分母为存续企业数，四城存续率 58.19%—99.34% 差异极大；"
        "这是本件最需要甲方裁决的口径（见 §四）。",
        "4 城极值归一使每个叶子必有一城 100、一城 0；指数只能读作「四城内相对位置」。",
    ],
}

with open(OUT, "w", encoding="utf-8") as fo:
    json.dump(out, fo, ensure_ascii=False, indent=1)

print("[DOMAIN_INDEX] ->", OUT)
print("  index", index)
print("  order", order, "gaps", out["adjacent_gaps"])
print("  coverage dims", coverage["dims_available"], "/", coverage["dims_total"],
      "leaves", coverage["by_state_count"])
print("  zero_fill", zero_fill, zero_order, "changed", out["zero_fill_counterexample"]["order_changed"])
print("  ordinal", ordinal, ord_order, "gap 广-莞", ord_gap_gz_dg)
print("  d2 alt", alt_index, alt_order, "changed", out["d2_denominator_counterfactual"]["order_changed"])
print("  checks", checks)
