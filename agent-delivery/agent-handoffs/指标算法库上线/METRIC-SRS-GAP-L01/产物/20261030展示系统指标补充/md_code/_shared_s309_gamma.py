#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S3-09 路γ 共享探针：活动/竞赛/计量校准/环比宿主/机构属地分布（5 件薄壳共用）。

覆盖词族（三源逐一留证，dev 17 schema / gkx 280 表 / jiuxin SHOW TABLES 实数）：
  G1 活动主档面（activity|event|exchange|forum|conference|seminar|summit）
  G2 竞赛主档面（contest|competition|match|award|prize）
  G3 计量校准流水域（calibr|metrolog|geometry|geometric|cmm + measure）
  G4 环比宿主序列面（宿主=可承载环比的月/季/年频结果序列；探 yoy|mom|ratio|growth 列 + 已知年度序列面行数）
  G5 软科学成果属地分布（jiuxin ads_institution_profile 属地正读数 + soft_science 词族）

产物：code/_snapshots/_shared_s309_gamma_out.json
铁律：dev 只认 gkxlumenx_*（禁 demo_*/_devdb）；gkx 280 表只读；jiuxin SHOW TABLES 实数勿写死。
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pymysql  # noqa: E402

from _gkxdb import gkx  # noqa: E402

OUT = "_snapshots/_shared_s309_gamma_out.json"

DEV = dict(
    host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
    charset="utf8mb4", connect_timeout=15, read_timeout=120, autocommit=True,
    cursorclass=pymysql.cursors.DictCursor,
)

JX = dict(
    host="47.93.119.170", port=29030, user="test2",
    password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
    database="gkx_technology_analysis_dev", charset="utf8mb4",
    connect_timeout=20, read_timeout=300,
)

FAM_ACTIVITY = r"activity|event|exchange|forum|conference|seminar|summit|交流活动"
FAM_CONTEST = r"contest|competition|match|award|prize|竞赛"
FAM_CALIB = r"calibr|metrolog|geometr|cmm|coordinate.?measur"
FAM_MOM = r"mom_|qoq|env_ratio|growth_rate|yoy|chain"

def dev_scan(conn):
    cur = conn.cursor()
    cur.execute("SELECT SCHEMA_NAME AS sn FROM information_schema.schemata WHERE SCHEMA_NAME LIKE 'gkxlumenx%' ORDER BY 1")
    schemas = sorted(r["sn"] for r in cur.fetchall())
    cur.execute("SELECT COUNT(*) AS c FROM information_schema.tables WHERE table_schema LIKE 'gkxlumenx%'")
    dev_table_total = int(cur.fetchone()["c"])

    def fam_tables(rx):
        cur.execute(
            "SELECT table_schema AS ts, table_name AS tn FROM information_schema.tables "
            "WHERE table_schema LIKE 'gkxlumenx%%' AND LOWER(table_name) REGEXP %s ORDER BY 1,2", (rx,))
        return [f"{r['ts']}.{r['tn']}" for r in cur.fetchall()]

    out = {
        "dev_schema_count": len(schemas),
        "dev_schemas": schemas,
        "dev_table_total": dev_table_total,
        "dev_activity_family": fam_tables(FAM_ACTIVITY),
        "dev_contest_family": fam_tables(FAM_CONTEST),
        "dev_calibration_family": fam_tables(FAM_CALIB),
    }
    # 环比宿主：dev 已知年度序列面行数（软科学 S3-07 批探明三源无软科学成果主档）
    for t, key in [
        ("gkxlumenx_ods.dwd_patent_transfer", "dev_dwd_patent_transfer_rows"),
        ("gkxlumenx_dwd.enterprise_cooperation", "dev_enterprise_cooperation_rows"),
    ]:
        try:
            cur.execute(f"SELECT COUNT(*) AS c FROM {t}")
            out[key] = int(cur.fetchone()["c"])
        except Exception as e:  # noqa: BLE001
            out[key] = f"ERR:{type(e).__name__}"
    # 环比比例列扫描（宿主序列的比例/增速列）
    cur.execute("""
        SELECT table_schema AS ts, table_name AS tn, column_name AS cn
        FROM information_schema.columns
        WHERE table_schema LIKE 'gkxlumenx%%'
          AND (LOWER(column_name) REGEXP %s OR LOWER(column_name) REGEXP %s)
        ORDER BY table_schema, table_name, ordinal_position
    """, (FAM_MOM, r"percent|pct|ratio"))
    mom_cols = {}
    for r in cur.fetchall():
        mom_cols.setdefault(f"{r['ts']}.{r['tn']}", []).append(r["cn"])
    out["dev_mom_ratio_column_hits"] = mom_cols
    return out


def gkx_scan(cur):
    cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='gkx'")
    total = int(cur.fetchone()[0])
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' ORDER BY table_name")
    tables = [r[0] for r in cur.fetchall()]
    return {
        "gkx_table_count": total,
        "gkx_activity_family": sorted(t for t in tables if re.search(FAM_ACTIVITY, t, re.I)),
        "gkx_contest_family": sorted(t for t in tables if re.search(FAM_CONTEST, t, re.I)),
        "gkx_calibration_family": sorted(t for t in tables if re.search(FAM_CALIB, t, re.I)),
    }


def jiuxin_scan(conn):
    cur = conn.cursor()
    cur.execute("SHOW TABLES")
    tables = sorted(r[0] for r in cur.fetchall())
    out = {
        "jiuxin_table_count_live": len(tables),
        "jiuxin_activity_family": [t for t in tables if re.search(FAM_ACTIVITY, t, re.I)],
        "jiuxin_contest_family": [t for t in tables if re.search(FAM_CONTEST, t, re.I)],
        "jiuxin_calibration_family": [t for t in tables if re.search(FAM_CALIB, t, re.I)],
        "jiuxin_soft_science_family": [t for t in tables if re.search(r"soft.?science|policy_research|topic", t, re.I)],
    }
    # ---- G5 正读数：软科学成果空间分布（机构属地）----
    # 候选承载 = ads_institution_profile（83,745 行属地字段）
    cur.execute("SELECT COUNT(*) FROM ads_institution_profile")
    out["jiuxin_profile_rows"] = int(cur.fetchone()[0])
    for col, key in [
        ("province_name", "jiuxin_profile_province_nonnull"),
        ("city_name", "jiuxin_profile_city_nonnull"),
        ("district_name", "jiuxin_profile_district_nonnull"),
        ("country_name", "jiuxin_profile_country_nonnull"),
        ("latitude", "jiuxin_profile_lat_nonnull"),
    ]:
        cur.execute(f"SELECT COUNT(*) FROM ads_institution_profile WHERE {col} IS NOT NULL AND {col} != ''")
        out[key] = int(cur.fetchone()[0])
    # 属地分布（中国机构按省；全球按国家）
    cur.execute(
        "SELECT country_name, COUNT(*) AS c FROM ads_institution_profile "
        "GROUP BY country_name ORDER BY c DESC LIMIT 15")
    out["jiuxin_profile_country_top15"] = {str(r[0]): int(r[1]) for r in cur.fetchall()}
    cur.execute(
        "SELECT province_name, COUNT(*) AS c FROM ads_institution_profile "
        "WHERE country_name = '中国' GROUP BY province_name ORDER BY c DESC LIMIT 15")
    out["jiuxin_profile_cn_province_top15"] = {str(r[0]): int(r[1]) for r in cur.fetchall()}
    cur.execute(
        "SELECT city_name, COUNT(*) AS c FROM ads_institution_profile "
        "WHERE country_name = '中国' GROUP BY city_name ORDER BY c DESC LIMIT 15")
    out["jiuxin_profile_cn_city_top15"] = {str(r[0]): int(r[1]) for r in cur.fetchall()}
    # 广东省下钻（深圳属地候选）
    cur.execute(
        "SELECT city_name, COUNT(*) AS c FROM ads_institution_profile "
        "WHERE province_name = '广东省' GROUP BY city_name ORDER BY c DESC LIMIT 10")
    out["jiuxin_profile_gd_city_top10"] = {str(r[0]): int(r[1]) for r in cur.fetchall()}
    # 软科学语义过滤：名称含研究/院/所/政策类词的中国机构属地下钻（代理骨架；列名=name_zh/name_en，DESCRIBE 实测）
    cur.execute(
        "SELECT province_name, COUNT(*) AS c FROM ads_institution_profile "
        "WHERE country_name = '中国' AND (name_zh LIKE '%%研究院%%' OR name_zh LIKE '%%研究所%%' "
        "OR name_zh LIKE '%%发展研究中心%%' OR name_zh LIKE '%%软科学%%' OR name_zh LIKE '%%战略研究%%') "
        "GROUP BY province_name ORDER BY c DESC LIMIT 15")
    out["jiuxin_profile_cn_research_province_top15"] = {str(r[0]): int(r[1]) for r in cur.fetchall()}
    cur.execute(
        "SELECT COUNT(*) FROM ads_institution_profile WHERE country_name = '中国' "
        "AND (name_zh LIKE '%%研究院%%' OR name_zh LIKE '%%研究所%%' OR name_zh LIKE '%%发展研究中心%%' "
        "OR name_zh LIKE '%%软科学%%' OR name_zh LIKE '%%战略研究%%')")
    out["jiuxin_profile_cn_research_total"] = int(cur.fetchone()[0])
    # ---- G4 环比宿主：jiuxin 年度序列面（已证可承载环比的序列规模）----
    cur.execute("SELECT COUNT(*) FROM ads_geo_yearly_metrics")
    out["jiuxin_geo_yearly_metrics_rows"] = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM ads_institution_collaboration_yearly")
    out["jiuxin_collab_yearly_rows"] = int(cur.fetchone()[0])
    cur.execute(
        "SELECT statistics_year, COUNT(*) AS c FROM ads_geo_yearly_metrics "
        "WHERE location_id IN (SELECT location_id FROM ads_location WHERE location_level='CITY' AND country_code='CN' AND name_zh='深圳') "
        "GROUP BY statistics_year ORDER BY statistics_year LIMIT 5")
    out["jiuxin_shenzhen_geo_series_head"] = {str(r[0]): int(r[1]) for r in cur.fetchall()}
    # 环比比例列扫描（全库）
    cur.execute("SHOW TABLES")
    all_tables = [r[0] for r in cur.fetchall()]
    mom_hits = {}
    for t in all_tables:
        try:
            cur.execute(f"DESCRIBE `{t}`")
            cols = [r[0] for r in cur.fetchall() if re.search(FAM_MOM, r[0], re.I)]
            if cols:
                mom_hits[t] = sorted(cols)
        except Exception:  # noqa: BLE001
            continue
    out["jiuxin_mom_ratio_column_hits"] = mom_hits
    return out


def main() -> None:
    out = {"generated": 20261102, "batch": "S3-09-gamma"}

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
    print("dev activity:", out["dev"]["dev_activity_family"][:6],
          "| contest:", out["dev"]["dev_contest_family"][:6],
          "| calib:", out["dev"]["dev_calibration_family"][:6])
    print("gkx activity:", out["gkx"]["gkx_activity_family"],
          "| contest:", out["gkx"]["gkx_contest_family"])
    print("jiuxin activity:", out["jiuxin"]["jiuxin_activity_family"],
          "| contest:", out["jiuxin"]["jiuxin_contest_family"],
          "| calib:", out["jiuxin"]["jiuxin_calibration_family"])
    print("jiuxin profile rows:", out["jiuxin"]["jiuxin_profile_rows"],
          "| cn province top5:", list(out["jiuxin"]["jiuxin_profile_cn_province_top15"].items())[:5])
    print("jiuxin mom cols:", out["jiuxin"]["jiuxin_mom_ratio_column_hits"])


if __name__ == "__main__":
    main()
