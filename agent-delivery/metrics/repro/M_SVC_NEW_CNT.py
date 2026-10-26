#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""新增服务机构动态（M_SVC_NEW_CNT）—— gkx 口径，自包含。

数据源（只读落盘快照，零 SQL、零 demo）：
    code/_snapshots21/svc21_facts_20261022.json   pool 44,153（inc_year 来自底册）
    code/_snapshots21/base_20261021.json          成立年列（第 6 列）

口径：毛出生计数 B(y)=|{e∈Pool: inc_year(e)=y}|；缺失年不入序列、不补 0。
      gkx 底册成立年在 2023—2025 明显右截断（218/66/12），序列只发布到 2022。
产出：code/M_SVC_NEW_CNT_out.json（覆盖写）
运行：cd code && python3 M_SVC_NEW_CNT.py
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
BASE = os.path.join(SNAP, "base_20261021.json")
OUT = os.path.join(HERE, "M_SVC_NEW_CNT_out.json")


def main() -> None:
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    base = json.load(open(BASE, encoding="utf-8"))
    pool = f["pool"]
    bmap = {r[0]: r for r in base}

    inc = Counter()
    for o, v in pool.items():
        y = v.get("inc_year")
        if not y and o in bmap:
            y = bmap[o][5]
        if y:
            inc[int(y)] += 1
    n_pool = len(pool)
    n_inc = sum(inc.values())
    missing = n_pool - n_inc

    series = [[y, inc[y]] for y in sorted(inc)]
    full = [[y, inc.get(y, 0)] for y in range(min(inc), 2023)]
    recent = [[y, inc.get(y, 0)] for y in range(2013, 2023)]
    yoy = []
    for y in range(2014, 2023):
        a, b = inc.get(y - 1, 0), inc.get(y, 0)
        yoy.append([y, b, round((b - a) / a * 100, 2) if a else None])
    peak_y, peak_v = max(inc.items(), key=lambda kv: kv[1])
    left_years = [y for y in range(min(inc), 2000) if inc.get(y, 0) < 10]

    out = {
        "metric_id": "M_SVC_NEW_CNT",
        "metric_name": "新增服务机构动态",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": (
            "毛出生序列可现转（成立年覆盖 99.95%），但 gkx 底册成立年在 2023—2025 右截断"
            "（218/66/12 家），且无注销/吊销事件流，净新增不可算；近年序列不可用于趋势结论"),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_org_product_info", "rows": f["population"]["product_info_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_base_info（成立年）", "rows": f["population"]["base_all"],
             "snapshot": "code/_snapshots21/base_20261021.json"},
        ],
        "base_years_used": list(range(2013, 2023)),
        "base_years_missing": [2023, 2024, 2025],
        "base_years_note": (
            "趋势窗口取 2013—2022 十个完整年；2023—2025 虽有行但成立年右截断"
            "（218/66/12 家，明显低于 2022 的 483），按缺失处理、不进分母。"
            "1951—2000 年段计数极小，属左截断，只披露不作趋势"),
        "population": {
            "distinct_org_id": n_pool,
            "inc_year_nonnull": n_inc,
            "inc_year_missing": missing,
            "coverage": round(n_inc / n_pool, 6),
            "year_min": min(inc),
            "year_max": max(inc),
            "periods": len(inc),
            "left_truncated_years_lt10": len(left_years),
        },
        "series_all": series,
        "series_to_2022": full,
        "recent_2013_2022": recent,
        "yoy_2014_2022": yoy,
        "peak": {"year": peak_y, "count": peak_v},
        "total_2013_2022": sum(c for y, c in inc.items() if 2013 <= y <= 2022),
        "recent_sum": {
            "2013_2015": sum(inc.get(y, 0) for y in (2013, 2014, 2015)),
            "2016_2018": sum(inc.get(y, 0) for y in (2016, 2017, 2018)),
            "2019_2022": sum(inc.get(y, 0) for y in (2019, 2020, 2021, 2022)),
        },
        "recent_structure_2018_2022": {
            "new_orgs": sum(c for y, c in inc.items() if 2018 <= y <= 2022),
            "city_top": [[c, v] for c, v in sorted(
                Counter(pool[o]["city"] for o in pool if 2018 <= (pool[o].get("inc_year") or 0) <= 2022).items(),
                key=lambda x: -x[1])],
            "type_counts": [[k, v] for k, v in sorted(
                Counter(t for o in pool if 2018 <= (pool[o].get("inc_year") or 0) <= 2022
                        for t in (pool[o].get("types") or [])).items(), key=lambda x: -x[1])],
            "stage_counts": [[k, v] for k, v in sorted(
                Counter(t for o in pool if 2018 <= (pool[o].get("inc_year") or 0) <= 2022
                        for t in (pool[o].get("stages") or [])).items(), key=lambda x: -x[1])],
        },
        "old_draft_2025": 1251,
        "difference_vs_old_draft": {
            "population": "旧稿 43,296（演示库 svc_org_circle）→ 本件 44,153（gkx 经营范围机构）",
            "coverage": "旧稿成立年非空 89.9% → 本件 99.95%（仅 21 家缺失）",
            "peak": "旧稿峰值 2016 年 4,242 家 → 本件 2015 年 3,342 家",
            "reason": ("换源后成立年取自 gkx 底册，覆盖更高但近年右截断更明显；"
                       "两版峰值年份相差一年，绝对数不可直接比较"),
        },
        "gaps": {
            "right_truncation": "2023—2025 成立年登记不完整，近年新增被系统性低估",
            "exit_side": "无注销/吊销事件流，只有出生、没有死亡",
            "industry_slice": "gkx 无稳定的机构×产业映射，产业切片只能到六类服务类型代理",
        },
        "compute": {"status": "ok", "elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("pool=%d inc=%d miss=%d peak=%s recent=%s -> %s"
          % (n_pool, n_inc, missing, (peak_y, peak_v), recent[-3:], OUT))


if __name__ == "__main__":
    main()
