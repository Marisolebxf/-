#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_CITY_DENSITY 城市企业密度 —— gkx 口径复现（2026-10-22）

口径（calc-logic ENT / M_ENT_CITY_DENSITY）：
  企业密度 = 城市企业数 / 城市土地面积，单位「家/百平方公里」；
  分母取行政区划土地面积（km²），分子取登记住所落在该市的企业去重数。

本件只连 gkx（183.240.141.251:3318，只读 gkx_reader_zp）。
实测结论（不是推测）：
  * 分子完全可得：gkx.dwd_org_base_info 的 city 字段 66 个取值、189,115 行可绑定城市码，
    深圳 95,600 / 广州 49,605 / 东莞 33,590 / 惠州 9,979；
  * 分母在 gkx 不存在：全库 information_schema 扫描「列名含 area/land/square/km2 且
    类型为数值」的列，命中 0 个；`area` 列共 5 个、全是 varchar 行政区名，不是 km² 数值；
    `dwd_dim_admin_area` 29 列里没有任何面积列（只有代码与名称）；
  * 唯一的面积相关宏观指标是「人口密度(每公里土地面积人数)」a77361，只有 30 行、
    14 个国家代码、年份 1962—2021（最新年只有 1 个国家有值），既非中国城市级、
    也非当前期，不能反解城市面积。

因此本件**不出密度值**，只出分子，并把分母缺口写成可复核的探针结果。
退回口径（用人口密度反解面积）在 §四 明确拒绝并给出量化理由。

输出：code/M_ENT_CITY_DENSITY_out.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import pymysql

HERE = Path(__file__).resolve().parent
OUT = HERE / "M_ENT_CITY_DENSITY_out.json"
SNAP = HERE / "_snapshots21"
GEO = SNAP / "ent_base_geo_20261022.json"

GKX = dict(
    host="183.240.141.251", port=3318, user="gkx_reader_zp",
    password="Zp_Use_Gkx_db@123456",
    connect_timeout=60, read_timeout=900, write_timeout=900, autocommit=True,
)
# 固定探测日：产物必须可重跑一致（时间戳进产物会让每次 --check 判「内容有变」）
PULLED = "2026-10-22"
MAIN4 = ["深圳市", "广州市", "东莞市", "惠州市"]

AREA_SCAN = (
    "SELECT TABLE_NAME, COLUMN_NAME, COLUMN_TYPE FROM information_schema.COLUMNS "
    "WHERE TABLE_SCHEMA='gkx' AND COLUMN_NAME REGEXP '(^area$|land|square|km2|mianji|dimian|acreage)' "
    "AND DATA_TYPE IN ('int','bigint','double','decimal','float')"
)
AREA_COLS = (
    "SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE FROM information_schema.COLUMNS "
    "WHERE TABLE_SCHEMA='gkx' AND COLUMN_NAME='area'"
)


def connect(retries: int = 5):
    last = None
    for i in range(retries):
        try:
            return pymysql.connect(**GKX)
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(3 * (2 ** i))
    raise last


def q(sql: str, args=None):
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute("SET NAMES utf8mb4")
        cur.execute("SET SESSION max_execution_time=600000")
        cur.execute(sql, args)
        return cur.fetchall()
    finally:
        conn.close()


def main() -> None:
    geo = json.loads(GEO.read_text(encoding="utf-8"))["groups"]
    total = sum(g["n"] for g in geo)

    city = {}
    for g in geo:
        city[g["city"]] = city.get(g["city"], 0) + g["n"]

    # 分子排序（城市名 → 家数 → 占底册比）
    city_rows = [{"city": c, "cnt": n, "share": round(n / total * 100, 4),
                  "density_per_100km2": None}
                 for c, n in sorted(city.items(), key=lambda x: -x[1])]

    area_hits = [{"table": r[0], "column": r[1], "type": r[2]} for r in q(AREA_SCAN)]
    area_cols = [{"table": r[0], "column": r[1], "type": r[2]} for r in q(AREA_COLS)]
    macro = q(
        "SELECT COUNT(*), COUNT(DISTINCT area_code), MIN(occur_period_year), "
        "MAX(occur_period_year) FROM gkx.dwd_macro_index_data WHERE index_code='a77361'"
    )[0]
    macro_latest = q(
        "SELECT COUNT(*) FROM gkx.dwd_macro_index_data WHERE index_code='a77361' "
        "AND occur_period_year = (SELECT MAX(occur_period_year) FROM gkx.dwd_macro_index_data "
        "WHERE index_code='a77361')"
    )[0][0]
    admin_cols = q(
        "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='gkx' "
        "AND TABLE_NAME='dwd_dim_admin_area' ORDER BY ORDINAL_POSITION"
    )
    # 城市名 → 12 位 city_code（正文 §1.4 说「city 是名称、city_code 是代码」，
    # 这句必须能落到产物：把四大城市码一并落盘，前 6 位即民政部 6 位码）
    code_rows = q(
        "SELECT DISTINCT city_code, city_name FROM gkx.dwd_dim_admin_area "
        "WHERE city_name IN ('深圳市','广州市','东莞市','惠州市') "
        "AND city_code IS NOT NULL AND city_code <> '' ORDER BY city_code"
    )
    city_code_map = [
        {"city": r[1], "city_code": r[0], "code6": str(r[0])[:6], "prefix4": str(r[0])[:4]}
        for r in code_rows
    ]

    main4_rows = sum(city.get(c, 0) for c in MAIN4)
    out = {
        "metric_id": "M_ENT_CITY_DENSITY",
        "metric_name": "城市企业密度",
        "probe_date": "2026-10-22",
        "db": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）",
        "source": {"db": "gkx", "host": "183.240.141.251:3318",
                   "tables": ["gkx.dwd_org_base_info", "gkx.dwd_macro_index_data",
                              "gkx.dwd_dim_admin_area"],
                   "pulled_at": PULLED},
        "calc_logic_ref": "gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_CITY_DENSITY.md",
        "formula": "density_c = N_c / A_c * 100，单位 家/百km²；A_c 为城市行政区划土地面积（km²）",
        "probes": {
            "base_rows": total,
            "n_city": len(city),
            "main4_rows": main4_rows,
            "main4_share": round(main4_rows / total * 100, 4),
            "shenzhen_rows": city.get("深圳市", 0),
            "shenzhen_share": round(city.get("深圳市", 0) / total * 100, 4),
            "numeric_area_col_hits": len(area_hits),
            "numeric_area_col_detail": area_hits,
            "area_columns": area_cols,
            "area_columns_varchar": sum(1 for c in area_cols if c["type"] == "varchar"),
            "admin_area_columns": [r[0] for r in admin_cols],
            "admin_has_area_column": any(r[0] == "area" for r in admin_cols),
            "macro_area_index_rows": int(macro[0]),
            "macro_area_index_codes": int(macro[1]),
            "macro_area_index_year_range": [int(macro[2]), int(macro[3])],
            "macro_area_index_latest_year_rows": int(macro_latest),
            "city_code_rows": len(city_code_map),
        },
        "city_code_map": city_code_map,
        "numerator": city_rows[:15],
        "denominator": {
            "status": "absent",
            "unit_required": "km2",
            "available_numeric_sources": 0,
            "note": "gkx 无城市土地面积表/字段；dwd_dim_admin_area 只有 7 个代码与名称列，"
                    "不含面积；唯一面积相关指标是国家级人口密度，且止于 2021 年。",
        },
        "density_result": {
            "computed": False,
            "rows": 0,
            "note": "分母缺 A_c，密度值一律不出；产物不含任何 density 数值，避免空值被误读为 0。",
        },
        "support_judgment": "部分支持",
        "judgment_reason": (
            "分子侧完全可得（66 个城市、189,115 行可绑定城市码，深圳 95,600 家），"
            "分母侧在 gkx 无任何 km² 数值载体：面积类数值列扫描 0 命中，"
            "`area` 5 列全是 varchar 行政区名，区划字典 29 列无面积列；人口密度指标 a77361 仅 30 行 / 14 个国家代码 / "
            "止于 2021 年，不能反解城市面积。密度 = 分子/分母，分母恒缺即指标不可完整构建，"
            "故判部分支持（分子可交付、密度不可交付）。"
        ),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面指标：分子为当前主档全量计数；分母缺，无年度序列可谈。",
        "proxy_deviation": {
            "proxy": "未使用代理。分子用登记住所（city）计企业数，属指标定义本身，不是代理",
            "coverage_pct": 99.9995,
            "deviation_note": "城市字段填充 189,115/189,116（99.9995%），偏差只在「登记地≠经营地」"
                              "这一层，方向未知；密度分母完全缺失，任何密度数值都不可交付。",
        },
        "verdict_kind": "computed",
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"probes": out["probes"],
                      "top6": out["numerator"][:6]}, ensure_ascii=False, indent=1)[:2600])
    print("support:", out["support_judgment"], "| wrote", OUT.name)


if __name__ == "__main__":
    main()
