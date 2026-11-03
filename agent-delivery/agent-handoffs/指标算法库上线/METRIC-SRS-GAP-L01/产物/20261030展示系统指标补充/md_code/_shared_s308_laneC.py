#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S3-08 路C 共享探针：仪器共享/地图/服务量族（11 件薄壳共用）。

覆盖词族（三源逐一留证）：
  L1 仪器台账/使用频率/开放率/共享率（instrument|equip|device|usage|freq|open_rate|share_rate）
  L2 检测/测试服务流水（service|test|detect|calibr|thermal|analy）
  L3 创新券（voucher|coupon）
  L4 载体坐标/孵化载体（carrier|incub|park + lng/lat 列）
  L5 全球主体时空分布（jiuxin ads_geo_yearly_* / ads_institution_profile 正读数）
  L6 三坐标测量机（CMM 词族 + gkx dwd_medical_device 计数）

产物：code/_snapshots/_shared_s308_laneC_out.json
铁律：dev 只认 gkxlumenx_*（17 schema 实数）；gkx 280 表；jiuxin SHOW TABLES 实数（勿写死）。
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pymysql  # noqa: E402

from _gkxdb import gkx  # noqa: E402

OUT = "_snapshots/_shared_s308_laneC_out.json"

DEV = dict(
    host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
    charset="utf8mb4", connect_timeout=15, read_timeout=120, autocommit=True,
    cursorclass=pymysql.cursors.DictCursor,
)

JX = dict(
    host="47.93.119.170", port=29030, user="test2",
    password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
    database="gkx_technology_analysis_dev", charset="utf8mb4",
    connect_timeout=20, read_timeout=180,
)

# 词族（小写 substring / regex）
FAM_INSTRUMENT = r"instrument|equip|apparatus|machine_hour|usage|freq|open_rate|share_rate|open_share"
FAM_SERVICE = r"service|test|detect|calibr|thermal|analy|measure"
FAM_VOUCHER = r"voucher|coupon"
FAM_CARRIER = r"carrier|incub|park|space"
FAM_CMM = r"coordinate.?measur|cmm|三坐标|几何量"


def dev_scan(conn):
    cur = conn.cursor()
    cur.execute("SELECT SCHEMA_NAME AS sn FROM information_schema.schemata WHERE SCHEMA_NAME LIKE 'gkxlumenx%' ORDER BY 1")
    schemas = sorted(r["sn"] for r in cur.fetchall())
    cur.execute("""
        SELECT table_schema AS ts, table_name AS tn, column_name AS cn
        FROM information_schema.columns
        WHERE table_schema LIKE 'gkxlumenx%%'
          AND (LOWER(table_name) REGEXP %s OR LOWER(column_name) REGEXP %s)
        ORDER BY table_schema, table_name, ordinal_position
    """, (FAM_INSTRUMENT, FAM_INSTRUMENT))
    instr_hits = {}
    for r in cur.fetchall():
        instr_hits.setdefault(f"{r['ts']}.{r['tn']}", []).append(r["cn"])
    # service / voucher / carrier families: table names only (column scan too broad)
    def fam_tables(rx):
        cur.execute(
            "SELECT table_schema AS ts, table_name AS tn FROM information_schema.tables "
            "WHERE table_schema LIKE 'gkxlumenx%%' AND LOWER(table_name) REGEXP %s ORDER BY 1,2", (rx,))
        return [f"{r['ts']}.{r['tn']}" for r in cur.fetchall()]
    svc_hits = fam_tables(FAM_SERVICE)
    voucher_hits = fam_tables(FAM_VOUCHER)
    carrier_hits = fam_tables(FAM_CARRIER)
    # carrier dim detail
    cur.execute("SELECT COUNT(*) AS c FROM gkxlumenx_dim.carrier")
    carrier_rows = cur.fetchone()["c"]
    cur.execute("SELECT COUNT(*) AS c FROM gkxlumenx_dim.carrier WHERE lng IS NOT NULL AND lat IS NOT NULL")
    carrier_coords = cur.fetchone()["c"]
    cur.execute("SELECT carrier_type, COUNT(*) AS c FROM gkxlumenx_dim.carrier GROUP BY carrier_type ORDER BY c DESC")
    carrier_types = {r["carrier_type"]: r["c"] for r in cur.fetchall()}
    cur.execute("SELECT COUNT(*) AS c FROM gkxlumenx_dwd.enterprise_innovation_carrier")
    ent_innov_carrier_rows = cur.fetchone()["c"]
    # ads_is-like tables (仪器共享 ADS 指引表)
    cur.execute(
        "SELECT table_schema AS ts, table_name AS tn FROM information_schema.tables "
        "WHERE table_schema LIKE 'gkxlumenx%%' AND LOWER(table_name) LIKE 'ads_is%%' ORDER BY 1,2")
    ads_is_hits = [f"{r['ts']}.{r['tn']}" for r in cur.fetchall()]
    # 兑付/抵扣金额类列
    cur.execute("""
        SELECT table_schema AS ts, table_name AS tn FROM information_schema.tables
        WHERE table_schema LIKE 'gkxlumenx%%' AND LOWER(table_name) REGEXP 'pay|trade|order|fund|subsid|grant'
        ORDER BY 1,2
    """)
    pay_hits = [f"{r['ts']}.{r['tn']}" for r in cur.fetchall()]
    cur.execute("SELECT COUNT(*) AS c FROM information_schema.tables WHERE table_schema LIKE 'gkxlumenx%'")
    dev_table_total = cur.fetchone()["c"]
    # semantic check for pay tables (they are commerce pay, not science voucher)
    return {
        "dev_schema_count": len(schemas),
        "dev_schemas": schemas,
        "dev_table_total": dev_table_total,
        "dev_instrument_family_hits": instr_hits,
        "dev_service_family_table_hits": svc_hits,
        "dev_voucher_family_table_hits": voucher_hits,
        "dev_carrier_family_table_hits": carrier_hits,
        "dev_ads_is_hits": ads_is_hits,
        "dev_pay_family_table_hits": pay_hits,
        "dev_dim_carrier_rows": carrier_rows,
        "dev_dim_carrier_rows_with_coords": carrier_coords,
        "dev_dim_carrier_type_dist": carrier_types,
        "dev_dwd_enterprise_innovation_carrier_rows": ent_innov_carrier_rows,
    }


def gkx_scan(cur):
    cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='gkx'")
    total = int(cur.fetchone()[0])
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' ORDER BY table_name")
    tables = [r[0] for r in cur.fetchall()]
    out = {
        "gkx_table_count": total,
        "gkx_instrument_family": sorted(t for t in tables if re.search(r"instrument|equip|apparatus", t, re.I)),
        "gkx_service_family": sorted(t for t in tables if re.search(r"service|test|detect|calibr|thermal|analy|measure", t, re.I)),
        "gkx_voucher_family": sorted(t for t in tables if re.search(r"voucher|coupon", t, re.I)),
        "gkx_carrier_family": sorted(t for t in tables if re.search(r"carrier|incub|park", t, re.I)),
    }
    # 医疗器械库 CMM 语义检查
    cur.execute(
        "SELECT COUNT(*) FROM gkx.dwd_medical_device "
        "WHERE device_name LIKE '%%measur%%' OR device_name LIKE '%%coordinate%%' "
        "OR device_type LIKE '%%measur%%'")
    out["gkx_medical_device_measure_like_rows"] = int(cur.fetchone()[0])
    cur.execute(
        "SELECT device_name, device_type FROM gkx.dwd_medical_device "
        "WHERE device_name LIKE '%%measur%%' OR device_name LIKE '%%coordinate%%' LIMIT 8")
    out["gkx_medical_device_measure_like_samples"] = [
        {"device_name": r[0], "device_type": r[1]} for r in cur.fetchall()]
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_medical_device")
    out["gkx_dwd_medical_device_rows"] = int(cur.fetchone()[0])
    return out


def jiuxin_scan(conn):
    cur = conn.cursor()
    cur.execute("SHOW TABLES")
    tables = sorted(r[0] for r in cur.fetchall())
    out = {
        "jiuxin_table_count_live": len(tables),
        "jiuxin_instrument_family": [t for t in tables if re.search(r"instrument|equip|apparatus|device", t, re.I)],
        "jiuxin_ads_is_hits": [t for t in tables if t.lower().startswith("ads_is")],
        "jiuxin_service_family": [t for t in tables if re.search(r"service|test|detect|calibr|thermal|measure", t, re.I)],
        "jiuxin_voucher_family": [t for t in tables if re.search(r"voucher|coupon", t, re.I)],
        "jiuxin_carrier_family": [t for t in tables if re.search(r"carrier|incub|park", t, re.I)],
        "jiuxin_booking_order_family": [t for t in tables if re.search(r"order|book|reserv", t, re.I)],
    }
    # ---- 正读数：geo_yearly_metrics（全球研究主体时空分布核心面）----
    cur.execute("SELECT COUNT(*) FROM ads_geo_yearly_metrics")
    out["jiuxin_geo_yearly_metrics_rows"] = int(cur.fetchone()[0])
    cur.execute(
        "SELECT statistics_year, COUNT(*) FROM ads_geo_yearly_metrics "
        "GROUP BY statistics_year ORDER BY statistics_year")
    out["jiuxin_geo_yearly_metrics_year_counts"] = {str(r[0]): int(r[1]) for r in cur.fetchall()}
    # 国家级 主体数/论文数 top12（2024 与 2018 两时点）
    for yr in (2018, 2024, 2025):
        cur.execute(
            "SELECT l.name_en, l.name_zh, g.institution_count, g.paper_count, g.talent_count "
            "FROM ads_geo_yearly_metrics g JOIN ads_location l ON g.location_id = l.location_id "
            "WHERE g.statistics_year = %s AND l.location_level = 'COUNTRY' "
            "ORDER BY g.institution_count DESC LIMIT 12", (yr,))
        out[f"jiuxin_geo_country_top12_{yr}"] = [
            {"country_en": r[0], "country_zh": r[1], "institution_count": int(r[2] or 0),
             "paper_count": int(r[3] or 0), "talent_count": int(r[4] or 0)} for r in cur.fetchall()]
    # 中国/深圳 城市级下钻（2024）
    cur.execute(
        "SELECT l.name_zh, l.name_en, g.institution_count, g.paper_count "
        "FROM ads_geo_yearly_metrics g JOIN ads_location l ON g.location_id = l.location_id "
        "WHERE g.statistics_year = 2024 AND l.location_level = 'CITY' AND l.country_code = 'CN' "
        "ORDER BY g.institution_count DESC LIMIT 12")
    out["jiuxin_geo_cn_city_top12_2024"] = [
        {"city_zh": r[0], "city_en": r[1], "institution_count": int(r[2] or 0),
         "paper_count": int(r[3] or 0)} for r in cur.fetchall()]
    # institution_type 维（主体类型分布 2024 全球，国家级地点聚合）
    cur.execute(
        "SELECT t.name_zh, SUM(m.institution_count) AS inst_sum FROM ads_geo_yearly_institution_type_metrics m "
        "JOIN ads_institution_type t ON m.institution_type_id = t.institution_type_id "
        "JOIN ads_location l ON m.location_id = l.location_id "
        "WHERE m.statistics_year = 2024 AND l.location_level = 'COUNTRY' "
        "GROUP BY t.name_zh ORDER BY inst_sum DESC")
    out["jiuxin_geo_institution_type_2024"] = {r[0]: int(r[1] or 0) for r in cur.fetchall()}
    # profile 表读数（坐标覆盖 / 国家分布）
    cur.execute("SELECT COUNT(*) FROM ads_institution_profile")
    out["jiuxin_institution_profile_rows"] = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM ads_institution_profile WHERE latitude IS NOT NULL AND longitude IS NOT NULL")
    out["jiuxin_institution_profile_rows_with_coords"] = int(cur.fetchone()[0])
    cur.execute(
        "SELECT country_name, COUNT(*) FROM ads_institution_profile GROUP BY country_name ORDER BY 2 DESC LIMIT 12")
    out["jiuxin_institution_profile_country_top12"] = {str(r[0]): int(r[1]) for r in cur.fetchall()}
    return out


def main() -> None:
    out = {"generated": 20261102, "batch": "S3-08-laneC"}

    conn = pymysql.connect(**DEV)
    out["dev"] = dev_scan(conn)
    conn.close()

    cur = gkx()
    out["gkx"] = gkx_scan(cur)
    cur.close()

    jconn = pymysql.connect(**JX)
    out["jiuxin"] = jiuxin_scan(jconn)
    jconn.close()

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)
    print("written:", OUT)
    print("dev tables:", out["dev"]["dev_table_total"],
          "| gkx tables:", out["gkx"]["gkx_table_count"],
          "| jiuxin tables:", out["jiuxin"]["jiuxin_table_count_live"])
    print("dev instrument hits:", list(out["dev"]["dev_instrument_family_hits"])[:8])
    print("jiuxin ads_is:", out["jiuxin"]["jiuxin_ads_is_hits"],
          "| jiuxin instrument:", out["jiuxin"]["jiuxin_instrument_family"],
          "| voucher:", out["jiuxin"]["jiuxin_voucher_family"])
    print("geo 2024 top3:", out["jiuxin"]["jiuxin_geo_country_top12_2024"][:3])


if __name__ == "__main__":
    main()
