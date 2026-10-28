#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""年度新增服务机构数（M_SVC_ORG_NEW_COUNT）—— gkx 口径，自包含。

数据源（只读落盘快照，零 SQL、零 demo）：
    code/_snapshots21/svc21_facts_20261022.json   pool 44,153（inc_year / city / types）
    code/_snapshots21/base_20261021.json          189,116 行（成立年回退）

口径：出生存量计数（历年新设且至今仍在池），与 M_SVC_NEW_CNT 同序列、同口径双挂。
      2023—2025 右截断不进趋势；缺失年不补 0。
产出：code/M_SVC_ORG_NEW_COUNT_out.json（覆盖写）
运行：cd code && python3 M_SVC_ORG_NEW_COUNT.py
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
OUT = os.path.join(HERE, "M_SVC_ORG_NEW_COUNT_out.json")


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
    n = len(pool)
    n_inc = sum(inc.values())

    series = [[y, inc.get(y, 0)] for y in range(2013, 2023)]
    yoy = []
    for y in range(2014, 2023):
        a, b = inc.get(y - 1, 0), inc.get(y, 0)
        yoy.append([y, b, round((b - a) / a * 100, 2) if a else None])

    # 近五年新增的城市与类型结构（只取完整年）
    city = Counter()
    typ = Counter()
    stage = Counter()
    for o, v in pool.items():
        y = v.get("inc_year")
        if y and 2018 <= int(y) <= 2022:
            city[v.get("city") or "（空）"] += 1
            for t in v.get("types") or []:
                typ[t] += 1
            for s in v.get("stages") or []:
                stage[s] += 1
    sum_18_22 = sum(inc.get(y, 0) for y in range(2018, 2023))

    out = {
        "metric_id": "M_SVC_ORG_NEW_COUNT",
        "metric_name": "年度新增服务机构数",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": (
            "出生存量序列可现转（成立年覆盖 99.95%、2013—2022 十个完整年）；"
            "但出清侧（注销/吊销）缺失、2023—2025 成立年右截断，"
            "「净新增」与近年趋势均不可算"),
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
            "2013—2022 为十个完整年，进趋势与环比；2023—2025 成立年右截断"
            "（218/66/12 家）按缺失处理、不进分母；2026 无行。"
            "序列为「出生存量」口径：历年新设且至今仍在池，不含已退出机构"),
        "population": {
            "distinct_org_id": n,
            "inc_year_nonnull": n_inc,
            "inc_year_missing": n - n_inc,
            "coverage": round(n_inc / n, 6),
            "periods": len(inc),
            "year_min": min(inc),
            "year_max": max(inc),
        },
        "series_2013_2022": series,
        "yoy_2014_2022": yoy,
        "peak": {"year": max(inc, key=inc.get), "count": max(inc.values())},
        "recent_structure_2018_2022": {
            "new_orgs": sum_18_22,
            "city_top": [[c, v] for c, v in city.most_common(8)],
            "type_counts": [[k, v] for k, v in typ.most_common()],
            "stage_counts": [[k, v] for k, v in stage.most_common()],
            "type_multiplicity_sum": sum(typ.values()),
            "stage_multiplicity_sum": sum(stage.values()),
        },
        "cumulative_from_2013": [[y, sum(inc.get(k, 0) for k in range(2013, y + 1))] for y in range(2013, 2023)],
        "cumulative": {
            "2021_2022": sum(inc.get(y, 0) for y in (2021, 2022)),
            "2015_2017": sum(inc.get(y, 0) for y in (2015, 2016, 2017)),
            "2013_2022": sum(inc.get(y, 0) for y in range(2013, 2023)),
        },
        "difference_vs_old_draft": {
            "population": "旧稿 43,296 → 本件 44,153",
            "peak": "旧稿 2016 年 4,242 家 → 本件 2015 年 3,342 家",
            "recent": "旧稿 2025 年 1,251 家 → 本件 2025 年仅 12 家（右截断，不可比）",
            "reason": "旧稿成立年来自演示库主档，近年登记更完整；gkx 底册近年成立年明显缺登",
        },
        "gaps": {
            "exit_side": "无注销/吊销事件流，出生存量≠净新增",
            "right_truncation": "2023—2025 成立年登记不完整，近三年不可作趋势",
            "industry_slice": "无机构×产业稳定映射，只能给六类服务类型/六环节切片",
        },
        "compute": {"status": "ok", "elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("new_count 2013-2022 sum=%d peak=%s 2018-2022=%d -> %s"
          % (out["cumulative"]["2013_2022"], out["peak"], sum_18_22, OUT))


if __name__ == "__main__":
    main()
