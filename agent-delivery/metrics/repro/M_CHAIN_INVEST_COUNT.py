#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_INVEST_COUNT 投融资事件数 — gkx 三方库实测脚本（20261021 改源版）

口径（calc-logic v0.2.0，徐滕强 2026-10-14 拍板）：
  链上企业（被投视角）融资事件去重件数；去重键 (org_id, completion_date, funding_round)；
  org_id 全键挂链，禁名称匹配。

数据源（20261021 改源）：`gkx.dwd_org_financing_info` 25,654 行（三方库，与旧开发库逐表镜像）；
链归属：org_id -> 主档 credit_code（`gkx.dwd_org_base_info.external_id`）
        -> `gkx.dwd_org_industry_tags`（52,906 条可联标签行 / 35,046 家）的 12 条顶层链。
  旧版读的是本地落盘快照（来源为旧版开发库 ODS 镜像），本版改为**直连 gkx 现查**，
  公式、去重键、筛选规则一律不动。

输出：M_CHAIN_INVEST_COUNT_out.json
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _gkx21_common import (ROOTS, chain_names, ent_chain_map, org_index, q,  # noqa: E402
                          stats, write_out)

METRIC = "M_CHAIN_INVEST_COUNT"


def financing_rows():
    return q("SELECT org_id, name_cn, funding_round, funding_amount, completion_date "
             "FROM gkx.dwd_org_financing_info WHERE is_deleted=0")


def main():
    names = chain_names()
    ec = ent_chain_map()
    oi = org_index()
    fin = financing_rows()

    dropped_future = 0
    dropped_nodate = 0
    seen = set()
    dup_rows = 0
    per_chain = {c: {"events": 0, "orgs": set(), "rounds": Counter(), "years": Counter()}
                 for c in ROOTS}
    city = Counter()
    round_all = Counter()
    year_all = Counter()
    matched = 0
    chain_unmatched = 0
    city_missing = 0
    city_out4 = 0
    total_clean = 0

    for org_id, nm, rnd, amt, dt in fin:
        if not dt:
            dropped_nodate += 1
            continue
        y = int(str(dt)[:4])
        if y > 2025:
            dropped_future += 1
            continue
        key = (org_id, dt, rnd or "")
        if key in seen:
            dup_rows += 1
            continue
        seen.add(key)
        total_clean += 1
        round_all[rnd or "(空)"] += 1
        year_all[str(y)] += 1

        meta = oi.get(org_id)
        credit, _n, _p, c = (meta[1], meta[2], meta[3], meta[4]) if meta else (None, None, None, None)
        if not c:
            city_missing += 1
        elif c not in ("深圳市", "广州市", "东莞市", "惠州市"):
            city_out4 += 1
        else:
            city[c] += 1

        chains = ec.get(credit or "") or []
        if not chains:
            chain_unmatched += 1
            continue
        matched += 1
        for ch in chains:
            if ch in per_chain:
                per_chain[ch]["events"] += 1
                per_chain[ch]["orgs"].add(org_id)
                per_chain[ch]["rounds"][rnd or "(空)"] += 1
                per_chain[ch]["years"][str(y)] += 1

    rows = []
    for ch in ROOTS:
        d = per_chain[ch]
        rows.append({"chain": ch, "chain_name": names.get(ch),
                     "invest_events": d["events"], "n_orgs": len(d["orgs"]),
                     "top_rounds": d["rounds"].most_common(5),
                     "peak_year": d["years"].most_common(1)[0] if d["years"] else None})
    rows.sort(key=lambda r: -r["invest_events"])

    n_city4 = sum(city.values())
    report = {
        "metric_id": METRIC,
        "metric_name": "投融资事件数",
        "date": "2026-10-21",
        "calc_logic_ref": "gkx-orchestration/agent-delivery/metrics/calc-logic/CHAIN/M_CHAIN_INVEST_COUNT.md（v0.2.0）",
        "data_source": {
            "engine": "三方库 gkx（183.240.141.251:3318），唯一连库入口 code/_gkxdb.py",
            "tables": ["gkx.dwd_org_financing_info", "gkx.dwd_org_base_info", "gkx.dwd_org_industry_tags"],
            "note": "与旧开发库逐表镜像（行数一致），公式与去重键未改，仅换数据源",
        },
        "probes": {
            "financing_rows": len(fin),
            "dropped_future_date": dropped_future,
            "dropped_no_date": dropped_nodate,
            "duplicate_business_key_rows": dup_rows,
            "events_after_dedup": total_clean,
            "orgs_distinct": len({r[0] for r in fin}),
            "city_missing": city_missing,
            "city_out_of_4": city_out4,
            "city4_events": n_city4,
            "city4_rate_pct": round(100.0 * n_city4 / total_clean, 2) if total_clean else None,
            "chain_matched_events": matched,
            "chain_matched_pct": round(100.0 * matched / total_clean, 2) if total_clean else None,
            "chain_unmatched_events": chain_unmatched,
            "round_classes": len(round_all),
            "round_top20": round_all.most_common(20),
            "year_dist": dict(sorted(year_all.items())),
            "date_range": [min(r[4] for r in fin if r[4]), max(r[4] for r in fin if r[4])],
        },
        "chain_rows": rows,
        "stats_events": stats([r["invest_events"] for r in rows]),
        "sum_chain_events": sum(r["invest_events"] for r in rows),
        "note": "多链企业的一笔事件在每条链各计一次，故 12 链事件之和大于去重事件数，禁止把链和当事件总数。",
    }

    nz = sum(1 for r in rows if r["invest_events"] > 0)
    report["support_judgment"] = {
        "data_support_level": "完全转换支持",
        "reason": (
            f"gkx 真实融资表 {len(fin):,} 行，去重后 {total_clean:,} 起事件；"
            f"{matched:,} 起（{report['probes']['chain_matched_pct']}%）可经 org_id→credit_code→产业标签挂到 12 条链，"
            f"{nz}/12 链非零（{rows[0]['invest_events']:,}—{rows[-1]['invest_events']:,} 起）；"
            f"城市侧 {n_city4:,} 起可落四市（{report['probes']['city4_rate_pct']}%）。"
            "结构与当前数据量均足，现转即可产出非退化计数。"
        ),
        "criteria": {"events_after_dedup": total_clean, "chain_matched": matched,
                     "n_chain_nonzero": nz, "city4_rate_pct": report["probes"]["city4_rate_pct"]},
    }
    write_out(METRIC, report)
    print("events", total_clean, "chain matched", matched, "city4", n_city4)
    for r in rows:
        print(r["chain"], r["chain_name"], r["invest_events"], r["n_orgs"])


if __name__ == "__main__":
    main()
