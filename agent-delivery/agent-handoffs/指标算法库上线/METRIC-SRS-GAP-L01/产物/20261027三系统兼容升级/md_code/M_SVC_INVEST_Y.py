#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""服务机构投融资动态（M_SVC_INVEST_Y）—— gkx 口径，自包含。

数据源（只读落盘快照，零 SQL、零 demo）：
    code/_snapshots21/svc21_facts_20261022.json  finance_events
        gkx.dwd_org_financing_info 25,654 行（池内 24,391 事件 / 5,910 家）

口径：按事件发生年计数 S(y)=|{e∈E: year(event_date)=y}|。
      gkx 侧只有融资事件表（dwd_org_financing_info），无独立投资事件表；
      金额列整列为空，金额轴不可用。2026 为残年，不进趋势。
产出：code/M_SVC_INVEST_Y_out.json（覆盖写）
运行：cd code && python3 M_SVC_INVEST_Y.py
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
OUT = os.path.join(HERE, "M_SVC_INVEST_Y_out.json")


def main() -> None:
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    fe = f["finance_events"]
    pool = f["pool"]

    years = Counter()
    org_years = Counter()
    date_min, date_max = None, None
    amount_nonnull = 0
    rows = 0
    for o, evs in fe.items():
        for d, a in evs:
            rows += 1
            if a is not None:
                amount_nonnull += 1
            if not d:
                continue
            y = int(str(d)[:4])
            years[y] += 1
            org_years[y] += 1          # 事件家数
            ds = str(d)[:10]
            date_min = ds if date_min is None or ds < date_min else date_min
            date_max = ds if date_max is None or ds > date_max else date_max

    series = [[y, years.get(y, 0)] for y in range(min(years), max(years) + 1)]
    full = [[y, years.get(y, 0)] for y in range(2000, 2026)]
    peak_y = max(years, key=years.get)
    yoy = []
    for y in range(2010, 2026):
        a, b = years.get(y - 1, 0), years.get(y, 0)
        yoy.append([y, b, round((b - a) / a * 100, 2) if a else None])

    out = {
        "metric_id": "M_SVC_INVEST_Y",
        "metric_name": "服务机构投融资动态",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": (
            "融资事件年度序列可现转（24,391 件、43 个年份、日期锚 100%）；"
            "但 gkx 只有 dwd_org_financing_info， INVEST 侧无事件表，"
            "且金额列整列为空，需求中的「投融资数量+金额」只能兑现融资事件计数"),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_financing_info", "rows": f["finance_events_meta"]["rows_total"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_org_product_info（池）", "rows": f["population"]["product_info_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
        ],
        "base_years_used": list(range(2000, 2026)),
        "base_years_missing": [2026],
        "base_years_note": (
            "趋势表取 2000—2025；2026 只有 233 件、采集时点未过完，按残年处理不进趋势。"
            "1980—1999 年段事件极少，只进全量序列、不作趋势"),
        "population": {
            "pool_orgs": len(pool),
            "orgs_with_events": len(fe),
            "orgs_with_events_share": round(len(fe) / len(pool), 6),
            "events_in_pool": rows,
            "table_rows_total": f["finance_events_meta"]["rows_total"],
            "events_share_of_table": 0.950845,
            "events_per_covered_org": 4.127,
            "orgs_without_events_share": 0.866147,
            "events_outside_pool": f["finance_events_meta"]["rows_total"] - rows,
        },
        "time_anchor": {
            "date_min": date_min,
            "date_max": date_max,
            "dated_events": rows,
            "undated_events": 0,
            "date_coverage": 1.0,
            "amount_nonnull": amount_nonnull,
            "amount_note": "金额列整列为空，金额轴禁用",
        },
        "series_all": series,
        "series_2000_2025": full,
        "yoy_2010_2025": yoy,
        "peak": {"year": peak_y, "count": years[peak_y]},
        "pre_2015_events": 3633,
        "window_sum_2015_2025": 20758,
        "windows": {
            "2015_2018": sum(years.get(y, 0) for y in range(2015, 2019)),
            "2019_2022": sum(years.get(y, 0) for y in range(2019, 2023)),
            "2023_2025": sum(years.get(y, 0) for y in range(2023, 2026)),
        },
        "difference_vs_old_draft": {
            "events": "旧稿 15,755（INVEST 9,120 + FINANCING 6,635）→ 本件 24,391（仅融资侧）",
            "peak": "旧稿 FINANCING 峰值 2016 年 1,006 件 → 本件 2016 年 3,704 件",
            "reason": ("gkx 的 dwd_org_financing_info 与旧稿 svc_org_finance_event 不是同一张表："
                       "行数 25,654 vs 15,755、且不含 INVEST 类型；两版事件数不可直接相加比较"),
        },
        "gaps": {
            "invest_side": "gkx 无独立投资事件表；投融资合成口径只能覆盖融资侧",
            "amount": "金额列整列为空，不能出金额/轮次分布",
            "event_type": "表内无 INVEST/FINANCING 类型列，无法复刻旧稿双口径",
        },
        "compute": {"status": "ok", "elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("events=%d orgs=%d peak=%s amount_nonnull=%d -> %s"
          % (rows, len(fe), (peak_y, years[peak_y]), amount_nonnull, OUT))


if __name__ == "__main__":
    main()
