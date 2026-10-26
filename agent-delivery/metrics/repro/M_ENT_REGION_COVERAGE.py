#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_REGION_COVERAGE · 区域覆盖数（gkx 口径）

口径（calc-logic/ENT/M_ENT_REGION_COVERAGE.md）：
    企业集合实际覆盖的行政区域去重数 = COUNT(DISTINCT province) / COUNT(DISTINCT city)
    源表字段：gkx.dwd_org_base_info(org_id, province, city)

本脚本只连 gkx（183.240.141.251:3318，只读 gkx_reader_zp），不接任何演示库。
唯一查询：按 province/city/area 分组计数（一次全表扫描，实测约 75—120 秒）。
产物：code/M_ENT_REGION_COVERAGE_out.json

运行：cd code && python3 M_ENT_REGION_COVERAGE.py
"""
from __future__ import annotations

import json
import statistics
import time
from collections import Counter
from decimal import Decimal
from pathlib import Path

import pymysql

HERE = Path(__file__).resolve().parent
OUT = HERE / "M_ENT_REGION_COVERAGE_out.json"
METRIC_ID = "M_ENT_REGION_COVERAGE"

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", connect_timeout=60,
           read_timeout=1800, write_timeout=1800, autocommit=True)

SQL_REGION = (
    "SELECT province, city, area, COUNT(*) AS n FROM gkx.dwd_org_base_info "
    "WHERE is_deleted=0 GROUP BY province, city, area"
)
SQL_TOTAL = "SELECT COUNT(*) AS n FROM gkx.dwd_org_base_info WHERE is_deleted=0"

# 大陆省级行政区数（不含港澳台）。这是外部常量，不是库内值：
# 用来把「覆盖 29 个省」换算成比率，必须在产物里显式声明，避免下游把 29 当分母。
NATIONAL_PROVINCE_UNITS = 31


def j(v):
    if isinstance(v, (bytes, bytearray)):
        return v.decode("utf-8", "replace")
    if isinstance(v, Decimal):
        return float(v)
    if hasattr(v, "isoformat"):
        try:
            return v.isoformat()
        except TypeError:
            return str(v)
    return v


def connect():
    """gkx 会间歇性 15—20 秒超时（约 2/10），必须 5 次指数退避重试。"""
    last = None
    for i in range(5):
        try:
            return pymysql.connect(**GKX)
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 ** i)
    raise RuntimeError(f"gkx 连不上（5 次重试）：{last}")


def q(cur, sql, ms=900000):
    cur.execute(f"SET SESSION max_execution_time={ms}")
    cur.execute(sql)
    return [list(map(j, r)) for r in cur.fetchall()]


def main() -> None:
    t0 = time.time()
    conn = connect()
    cur = conn.cursor()
    total_rows = int(q(cur, SQL_TOTAL, 900000)[0][0])
    cells = q(cur, SQL_REGION, 900000)
    conn.close()

    prov = Counter()
    city = Counter()
    area_cell = Counter()
    gd_city = Counter()
    for p, c, a, n in cells:
        if p:
            prov[p] += int(n)
        if p and c:
            city[(p, c)] += int(n)
            if p == "广东省":
                gd_city[c] += int(n)
        if p and c and a:
            area_cell[(p, c, a)] += int(n)

    cells_total = sum(int(r[3]) for r in cells)
    prov_rows = sum(prov.values())
    city_rows = sum(city.values())
    area_rows = sum(area_cell.values())

    def rate(a, b):
        return round(a / b * 100, 4) if b else None

    top_prov = [{"province": k, "orgs": v, "share_pct": rate(v, cells_total)}
                for k, v in prov.most_common(10)]
    top_city = [{"province": k[0], "city": k[1], "orgs": v}
                for k, v in city.most_common(10)]
    eff = sum(1 for v in prov.values() if v >= 10)

    payload = {
        "metric_id": METRIC_ID,
        "metric_name": "区域覆盖数",
        "support_judgment": "完全直接支持",
        "verdict_kind": "positive",
        "judgment_reason": (
            "calc-logic 的源表字段就是 gkx.dwd_org_base_info(org_id, province, city)，"
            "去重计数即定义本身，无需换算、无需补维：实测 189,116 行底册可得 29 个省级、"
            "65 个市级、146 个县级覆盖格，province/city 非空率 99.9995%。"
        ),
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "sources": {
            "primary": "gkx @ 183.240.141.251:3318 (readonly gkx_reader_zp)",
            "tables": ["gkx.dwd_org_base_info"],
            "sql": [SQL_TOTAL, SQL_REGION],
            "calc_logic": "gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_REGION_COVERAGE.md",
        },
        "compute": {
            "base_rows": total_rows,
            "group_cells": len(cells),
            "cells_total_orgs": cells_total,
            "distinct": {
                "province": len(prov),
                "city": len(city),
                "county_cells": len(area_cell),
                "county_names": len({k[2] for k in area_cell}),
            },
            "fill": {
                "province_non_empty": prov_rows,
                "city_non_empty": city_rows,
                "area_non_empty": area_rows,
                "province_rate_pct": rate(prov_rows, total_rows),
                "city_rate_pct": rate(city_rows, total_rows),
                "area_rate_pct": rate(area_rows, total_rows),
            },
            "coverage": {
                "national_province_units": NATIONAL_PROVINCE_UNITS,
                "province_rate_pct": rate(len(prov), NATIONAL_PROVINCE_UNITS),
                "effective_threshold_orgs": 10,
                "effective_provinces": eff,
                "effective_rate_pct": rate(eff, NATIONAL_PROVINCE_UNITS),
                "note": "分母 31 为大陆省级行政区数（外部常量，非库内值）；"
                        "市级与县级不做全国比率，因为库内无区划总量表",
            },
            "concentration": {
                "guangdong_orgs": prov.get("广东省", 0),
                "guangdong_share_pct": rate(prov.get("广东省", 0), cells_total),
                "out_of_guangdong_orgs": cells_total - prov.get("广东省", 0),
                "guangdong_cities": [{"city": k, "orgs": v} for k, v in gd_city.most_common()],
            },
            "top_provinces": top_prov,
            "top_cities": top_city,
            "mean_orgs_per_province": round(prov_rows / len(prov), 2),
            "mean_orgs_per_city": round(city_rows / len(city), 2),
            "mean_orgs_per_county": round(area_rows / len(area_cell), 2),
            "median_orgs_per_province": statistics.median(prov.values()),
        },
        "probes": {
            "retry_policy": "5 次指数退避",
            "max_execution_time_ms": 900000,
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "截面件：口径是「当前底册覆盖多少个行政区域」，不含年度序列，故无基期年份。"
            "若要做跨年覆盖变化，需按底册快照日期留档（民政部每年调整区划代码，跨期比须先对齐版本）。"
        ),
        "notes": [
            "只做去重计数，不加权、不按人口/面积标准化。",
            "县级用 province+city+area 三元组去重，避免同名区县跨市合并。",
            "底册高度偏粤：广东 188,776 家占 99.82%，省外仅 339 家，覆盖率不能读成市场覆盖率。",
        ],
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[{METRIC_ID}] 行数={total_rows} 省={len(prov)} 市={len(city)} "
          f"县格={len(area_cell)} -> {OUT.name}")


if __name__ == "__main__":
    main()
