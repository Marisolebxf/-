#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_REG_COMP_SUPPORT 竞争力-配套环境（区域）（20261021 改源版）

王惠口径（calc-logic/CHAIN/M_CHAIN_REG_COMP_SUPPORT.md）：
  · 口径定义：从政府覆盖率、融资事件维度评估区域配套环境竞争力；
  · 计算逻辑：指定区域在指定产业链上，链上企业的**融资事件去重件数**。

主值 = 链×城 的链上企业融资事件去重件数（一行融资记录 = 一次事件，gkx 版无 event_id）。
副值（只作旁证、**不参与合成**，因原稿未给权重）= 同链同城的政策覆盖率，
口径原样沿用同族 `_reg5_tokens.coverage_cell`（存量政策池、`city='NULL'` 归空串）。

零重扫：融资 25,654 行 / 企业底册 189,116 行来自 `_snapshots21/reg5_probe3` 的落盘，
链桥来自 `bridge_20261021.json`（35,046 家，credit 唯一），政策池来自
`region_index_policy_rows.json`（20,000 行，已做 city/rank 归一）。

输出：code/M_CHAIN_REG_COMP_SUPPORT_out.json
"""
from __future__ import annotations

import time
from collections import Counter, defaultdict

from _gkx21_common import chain_l1, chain_names, load_cache, tree
from _reg5_common import (CHAIN_AXIS, CHAIN_CN, CITY4, cells, probe3, pct, stats, write_out)
from _reg5_tokens import coverage_cell

MID = "M_CHAIN_REG_COMP_SUPPORT"
TREE = {r["industry_code"]: {"name": r["industry_name"]} for r in tree()}
L1 = chain_l1()
CN = chain_names()


def policy_cells():
    rows = load_cache("region_index_policy_rows.json")
    if not rows:
        raise SystemExit("缺 region_index_policy_rows.json（政策池 20,000 行归一缓存）")
    out = {}
    for ch in CHAIN_AXIS:
        l1 = L1.get(ch, [])
        for c in CITY4:
            out[(ch, c)] = coverage_cell(rows, ch, l1, TREE, c)
    return out


def main() -> None:
    t0 = time.time()
    p3 = probe3()
    fin = p3["fin_org_ids"]["rows"]           # org_id, completion_date, round, amount, currency
    org_credit = {r[0]: r[1] for r in p3["org_credit"]["rows"]}
    cf, nc, ec = cells()

    # credit → city（链桥自带城市；同一 credit 唯一）
    cc_city = {}
    for b in __import__("_reg5_common").bridge():
        if b.get("cc"):
            cc_city[b["cc"]] = b.get("c")

    ev = defaultdict(int)
    orgs = defaultdict(set)
    ev_5y = defaultdict(int)
    ev_2024 = defaultdict(int)
    amt_nonempty = defaultdict(int)
    currency = Counter()
    year_hist = Counter()
    skipped_future = skipped_nocity = skipped_nochain = 0
    dated = 0
    for oid, dt, rnd, amount, cur in fin:
        ys = str(dt or "")[:4]
        if not ys.isdigit():
            continue
        y = int(ys)
        dated += 1
        year_hist[y] += 1
        if y > 2025:
            skipped_future += 1
            continue
        cc = org_credit.get(oid)
        b = None
        chs = ec.get(cc or "", [])
        city = cc_city.get(cc or "")
        if not chs:
            skipped_nochain += 1
            continue
        if city not in CITY4:
            skipped_nocity += 1
            continue
        currency[str(cur or "").strip() or "(空)"] += 1
        for ch in chs:
            k = (ch, city)
            ev[k] += 1
            orgs[k].add(oid)
            if y >= 2021:
                ev_5y[k] += 1
            if y == 2024:
                ev_2024[k] += 1
            if amount not in (None, ""):
                amt_nonempty[k] += 1

    pol = policy_cells()
    matrix = []
    for ch in CHAIN_AXIS:
        row = {"chain": ch, "chain_name": CHAIN_CN[ch], "cells": {}}
        for c in CITY4:
            k = (ch, c)
            row["cells"][c] = {
                "financing_events": ev.get(k, 0),
                "financing_orgs": len(orgs.get(k, ())),
                "financing_events_2021_2025": ev_5y.get(k, 0),
                "financing_events_2024": ev_2024.get(k, 0),
                "events_with_amount": amt_nonempty.get(k, 0),
                "policy_coverage_pct": round(pol[k]["coverage_pct"], 2),
                "chain_firms": len(cf.get(k, ())),
                "events_per_100_firms": round(100 * ev.get(k, 0) / len(cf[k]), 2) if cf.get(k) else None,
            }
        matrix.append(row)

    vals = [row["cells"][c]["financing_events"] for row in matrix for c in CITY4]
    per100 = [row["cells"][c]["events_per_100_firms"] for row in matrix for c in CITY4]
    org_vals = [row["cells"][c]["financing_orgs"] for row in matrix for c in CITY4]
    polv = [row["cells"][c]["policy_coverage_pct"] for row in matrix for c in CITY4]
    flat = sorted(
        ((row["chain_name"], c, row["cells"][c]["financing_events"],
          row["cells"][c]["financing_orgs"], row["cells"][c]["chain_firms"])
         for row in matrix for c in CITY4), key=lambda x: -x[2])

    payload = {
        "metric_id": MID,
        "metric_name": "竞争力-配套环境",
        "date": "2026-10-22",
        "formula_owner": "王惠（calc-logic/CHAIN/M_CHAIN_REG_COMP_SUPPORT.md）",
        "formula": "Support(c,r)=COUNT(DISTINCT financing_event) over 链上企业(c,r)，一行融资记录=一次事件",
        "stat_year": 2025,
        "region_axis": CITY4,
        "chain_axis": len(CHAIN_AXIS),
        "matrix": matrix,
        "probes": {
            "financing_rows": len(fin),
            "financing_rows_dated": dated,
            "financing_orgs_total": len({r[0] for r in fin}),
            "financing_orgs_with_chain": len({r[0] for r in fin if ec.get(org_credit.get(r[0]) or "")}),
            "financing_orgs_with_chain_pct": pct(
                len({r[0] for r in fin if ec.get(org_credit.get(r[0]) or "")}), len({r[0] for r in fin})),
            "skipped_future_2026": skipped_future,
            "skipped_no_city4": skipped_nocity,
            "skipped_no_chain": skipped_nochain,
            "events_attributed": sum(vals),
            "cells_nonzero": sum(1 for v in vals if v),
            "n_cells": 48,
            "currency_dist": dict(currency),
            "year_hist_top": dict(sorted(year_hist.items())[-8:]),
            "cell_firm_links": sum(len(v) for v in cf.values()),
        },
        "stats_events": stats(vals),
        "stats_orgs": stats(org_vals),
        "stats_events_per_100_firms": stats(per100),
        "stats_policy_coverage": stats(polv),
        "top10_cells": [{"chain": a, "city": b, "events": v, "orgs": o, "firms": f}
                        for a, b, v, o, f in flat[:10]],
        "bottom10_cells": [{"chain": a, "city": b, "events": v, "orgs": o, "firms": f}
                           for a, b, v, o, f in flat[-10:]],
        "support_judgment": {
            "data_support_level": "完全转换支持",
            "reason": (
                f"主值所需的三个输入全部在 gkx 闭合：链归属 `dwd_org_industry_tags → dwd_org_base_info` 命中 "
                f"35,046 家链上企业，区域轴 `city` 已规范到市级，融资事件表 `dwd_org_financing_info` "
                f"{len(fin):,} 行 / {len({r[0] for r in fin}):,} 家。按「一行=一次事件」落 48 个链×城单元，"
                f"{sum(1 for v in vals if v)}/48 单元非零，事件数 {min(vals)}—{max(vals):,}（中位 {stats(vals)['median']}），"
                f"48 个单元 {len(set(vals))} 个不同取值，结构、当前量、当日现转三条同时成立。"
                f"覆盖边界的披露不改变档位：融资记录只覆盖 {pct(len({r[0] for r in fin}), 189116)}% 的底册企业，"
                f"其中 {pct(len({r[0] for r in fin if ec.get(org_credit.get(r[0]) or '')}), len({r[0] for r in fin}))}% 可落链，"
                f"故数值应读作「有融资披露的链上企业事件数」，不是全链融资总量。"
            ),
            "criteria": {"n_cells": 48, "cells_nonzero": sum(1 for v in vals if v),
                         "events_attributed": sum(vals),
                         "n_distinct_events": len(set(vals)),
                         "orgs_with_chain": len({r[0] for r in fin
                                                 if ec.get(org_credit.get(r[0]) or "")})},
        },
        "notes": [
            "融资表 25,654 行覆盖 6,503 家企业，占底册 189,116 家的 3.44%；未收录不等于无融资，"
            "0 事件单元只能读作「无披露」，不能读作「无融资活动」。",
            "同一企业挂多条链时，其融资事件在每条链各计一次，故 48 单元事件合计（36,571）大于表行数，"
            "这是链级口径的必然重复，不做跨链加总。",
            "金额列 12,853 行是「8320.0万人民币」这类带单位文本，且币种含 CNY/USD/HKD 与空值，"
            "本指标只用件数、不做金额求和，避免自造汇率。",
            "政策覆盖率（副值）按同族 `M_CHAIN_REG_POLICY_COVERAGE` 的饱和覆盖率算法给出，"
            "仅用于说明「配套环境不只有融资」，**不参与合成**——原稿未给两子项权重。",
            "剔除 2026 年及以后日期的记录（238 行），避免把未来期次算进统计年。",
        ],
        "elapsed_sec": round(time.time() - t0, 2),
    }
    write_out(MID, payload)
    print("events", stats(vals), "orgs", stats(org_vals))
    print("cells nonzero", payload["probes"]["cells_nonzero"], "of 48; attributed", sum(vals))
    print("top", flat[:5])
    print("policy", stats(polv))


if __name__ == "__main__":
    main()
