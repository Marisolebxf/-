#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_SUPPORT_POWER 配套服务（配套生态竞争力，0—100）。

口径：calc-logic V2-2026-08-21（公式定义人 王惠）
    Score(c,r) = 100 × mean( minmax_city(policy_cov), minmax_city(fin_events) )
    政策覆盖率：政策命中环节数 / 全链环节数；融资环境：区域链上融资事件数。
    两维在同一产业链内对 4 个城市做截面 min-max；某维全城相同则取 0.5。

取数（全部离线，零 DB）：
  · `_snapshots21/region_index_policy_rows.json` —— gkx.dwd_policy_base 全表 20,000 条（title/city/rank/year）
  · `_snapshots21/region_index_fin_events.json`  —— gkx.dwd_org_financing_info 25,654 行（org_id/日期）
  · `_snapshots21/bridge_20261021.json`          —— 企业→链→城（35,046 家）
  · `_snapshots21/base_20261021.json`            —— 底册（org_id→credit_code/city）
  · `_reg5_tokens.coverage_cell`                 —— 政策环节词表与命中函数（同族 v0.2.0 口径）
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import _reg5_tokens as TOK

BASE = Path(__file__).parent
SNAP = BASE / "_snapshots21"
METRIC = "M_CHAIN_SUPPORT_POWER"

ROOTS = ["INB1204", "INB1209", "INB1236", "INB1303", "INB1306", "INB1309",
         "INB1323", "INB1333", "INB1354", "INB1502", "INB2503", "INB2505"]
CITY4 = ["深圳市", "广州市", "东莞市", "惠州市"]
STAT_YEAR = 2025


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def minmax(vals):
    lo, hi = min(vals), max(vals)
    if hi - lo <= 1e-12:
        return [0.5 for _ in vals]
    return [(v - lo) / (hi - lo) for v in vals]


def spearman(xs, ys):
    def rank(a):
        order = sorted(range(len(a)), key=lambda i: a[i])
        r = [0.0] * len(a)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and a[order[j + 1]] == a[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    rx, ry = rank(xs), rank(ys)
    n = len(xs)
    mx, my = sum(rx) / n, sum(ry) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return round(cov / den, 4) if den else None


def main():
    t0 = time.time()
    tree_rows = load("chain_tree_20261021.json")
    tree = {r["industry_code"]: {"name": r["industry_name"], "parent": r["parent_code"]}
            for r in tree_rows}
    chain_name = {c: tree[c]["name"] for c in ROOTS if c in tree}
    l1 = {c: sorted(r["industry_code"] for r in tree_rows
                    if len(r["industry_code"]) == 9 and r["industry_code"].startswith(c))
          for c in ROOTS}
    pol_rows = load("region_index_policy_rows.json")
    fin_rows = load("region_index_fin_events.json")
    base_rows = load("base_20261021.json")
    br = load("bridge_20261021.json")

    org_city = {r[0]: r[4] for r in base_rows}
    org_credit = {r[0]: r[1] for r in base_rows}
    cc_chains = {b["cc"]: b["chains"] for b in br if b["cc"]}

    # ---- 政策覆盖率（S1）
    pol = {}
    for ch in ROOTS:
        for c in CITY4:
            pol[(ch, c)] = TOK.coverage_cell(pol_rows, ch, l1[ch], tree, c)

    # ---- 融资事件（S2）：主口径 ≤2025，另算 ≤2024 变体用于与同族已验收产物对账
    fin = {(ch, c): 0 for ch in ROOTS for c in CITY4}
    fin24 = {(ch, c): 0 for ch in ROOTS for c in CITY4}
    fin_future = 0
    for r in fin_rows:
        dt = str(r.get("completion_date") or "")[:4]
        if dt.isdigit() and int(dt) > STAT_YEAR:
            fin_future += 1
            continue
        oid = r.get("org_id")
        city = org_city.get(oid)
        if city not in CITY4:
            continue
        for ch in cc_chains.get(org_credit.get(oid) or "", ()):
            if (ch, city) in fin:
                fin[(ch, city)] += 1
                if int(dt) <= 2024:
                    fin24[(ch, city)] += 1

    # ---- 归一与合成
    rows = []
    for ch in ROOTS:
        covs = [pol[(ch, c)]["coverage_pct"] for c in CITY4]
        bins = [pol[(ch, c)]["binary_coverage_pct"] for c in CITY4]
        fins = [fin[(ch, c)] for c in CITY4]
        n1 = minmax(covs)
        n1b = minmax(bins)
        n2 = minmax(fins)
        n2_24 = minmax([fin24[(ch, c)] for c in CITY4])
        for i, c in enumerate(CITY4):
            score = round(100.0 * (n1[i] + n2[i]) / 2, 2)
            rows.append({
                "chain": ch, "chain_name": chain_name.get(ch, ch), "city": c,
                "n_links": pol[(ch, c)]["n_links"],
                "n_links_hit": pol[(ch, c)]["n_links_hit"],
                "policy_coverage_pct": covs[i],
                "policy_binary_pct": bins[i],
                "policy_pool": pol[(ch, c)]["policy_pool_size"],
                "policy_hits_total": pol[(ch, c)]["total_hits"],
                "financing_events": fins[i],
                "financing_events_le2024": fin24[(ch, c)],
                "n_policy": round(n1[i], 4), "n_fin": round(n2[i], 4),
                "score": score,
                "score_binary_variant": round(100.0 * (n1b[i] + n2[i]) / 2, 2),
                "score_policy_only": round(100.0 * n1[i], 2),
                "score_fin_le2024": round(100.0 * (n1[i] + n2_24[i]) / 2, 2),
                "links": pol[(ch, c)]["links"],
            })

    scores = [r["score"] for r in rows]
    by_city = {}
    for r in rows:
        by_city.setdefault(r["city"], []).append(r["score"])
    city_mean = {c: round(sum(v) / len(v), 2) for c, v in by_city.items()}
    first = {}
    for ch in ROOTS:
        top = max((r for r in rows if r["chain"] == ch), key=lambda x: x["score"])
        first[top["city"]] = first.get(top["city"], 0) + 1
    corr_bin = spearman(scores, [r["score_binary_variant"] for r in rows])
    corr_pol = spearman(scores, [r["score_policy_only"] for r in rows])
    zero_pol = sum(1 for r in rows if r["policy_coverage_pct"] == 0)
    zero_fin = sum(1 for r in rows if r["financing_events"] == 0)

    payload = {
        "metric_id": METRIC,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_sec": round(time.time() - t0, 2),
        "support_judgment": "部分支持",
        "params": {"stat_year": STAT_YEAR, "weight": "等权", "norm": "链内 4 市 min-max",
                   "policy_formula": "Σ hit_i/(hit_i+5)/|L1| ×100（饱和覆盖率，同族 v0.2.0）",
                   "fin_formula": "链上企业融资事件行数（一行=一次事件，≤统计年）"},
        "coverage": {
            "policy_rows": len(pol_rows),
            "fin_rows": len(fin_rows),
            "fin_rows_future_dropped": fin_future,
            "bridge_firms": len(br),
            "l1_links_total": sum(len(v) for v in l1.values()),
            "cells": len(rows),
            "zero_policy_cells": zero_pol,
            "zero_fin_cells": zero_fin,
            "chain_first_place": dict(sorted(first.items(), key=lambda kv: -kv[1])),
        },
        "stats": {"n": len(scores), "min": min(scores), "max": max(scores),
                  "mean": round(sum(scores) / len(scores), 2),
                  "median": round(sorted(scores)[len(scores) // 2], 2),
                  "n_distinct": len({round(s, 4) for s in scores})},
        "city_mean": dict(sorted(city_mean.items(), key=lambda kv: -kv[1])),
        "sensitivity": {"spearman_vs_binary_policy": corr_bin,
                        "spearman_vs_policy_only": corr_pol,
                        "spearman_vs_fin_le2024": spearman(scores, [r["score_fin_le2024"] for r in rows]),
                        "max_abs_delta_fin_le2024": round(
                            max(abs(r["score"] - r["score_fin_le2024"]) for r in rows), 2)},
        "rows": rows,
        "notes": [
            "政策池为存量全表 20,000 条，不按发布年截断（按年截断会把覆盖率打成 0，见 DATA_FACTS §3.7）。",
            "status 全表 20,000 行均为「有效」，该条件不起过滤作用，已在口径中注明。",
            "keywords/keypoints 两列整列为空、theme 仅 2 行有值 → 环节命中实际只能落在 title，属口径退化项。",
            "融资表一行=一次事件，无事件 ID，故不做事件级去重（与同族 M_CHAIN_REGION_INDEX 一致）。",
            "4 城 min-max 会强制每条链产生 0 与 100 各一方，分数是链内相对位置，跨链不可比。",
        ],
    }
    out = BASE / f"{METRIC}_out.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: payload[k] for k in ("support_judgment", "coverage", "stats",
                                              "city_mean", "sensitivity")},
                     ensure_ascii=False, indent=1))
    # 与已验收同族 out.json 交叉核对（其 STAT_YEAR=2024，故用 le2024 变体对账）
    ref = json.loads((BASE / "M_CHAIN_REGION_INDEX_out.json").read_text(encoding="utf-8"))
    diff = 0
    for rr in ref["rows"]:
        mine = next((x for x in rows if x["chain"] == rr["chain"] and x["city"] == rr["city"]), None)
        if not mine:
            diff += 1
            continue
        if (abs(mine["policy_coverage_pct"] - rr["raw"]["policy_coverage"]) > 0.011
                or mine["financing_events_le2024"] != rr["raw"]["financing_events"]):
            diff += 1
    print("cross-check vs M_CHAIN_REGION_INDEX:", "48/48 一致" if diff == 0 else f"{diff} 格不一致")


if __name__ == "__main__":
    main()
