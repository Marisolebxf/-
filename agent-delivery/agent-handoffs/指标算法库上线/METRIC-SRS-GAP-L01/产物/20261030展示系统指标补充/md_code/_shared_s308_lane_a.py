#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S3-08 路 A（INCUB 下半 13 件）族级共享探针：三源一次实探，产物供各薄壳复用。

覆盖词族/事实面（按件分组）：
- 035/039/057/061 仪器运营族：reserv/service_order/service_count 词族复核（l2 已证 0，本探针 dev 列级复核 service 词族）
- 038 时空热点：dev heat 词族行数实证（chain_hotspot/innovation_event/sys_area 等）+ jiuxin ads_geo_yearly_metrics
  （location×year 区域创新活跃度量——区域热点强度转换候选）深圳区县覆盖实查
- 043/047 评分面：dev ads.enterprise_score 列+行、ads.carrier_index（已证 0 行复核）、gkx score 词族表名
- 049 跨区协作：jiuxin SHOW TABLES 实数复核（聚合复算由薄壳独立实连，不走本快照）
- 050/051/052 路径强度：三源 path/link/route/corridor 词族 + jiuxin ads_talent_mobility_yearly_flow
  flow_dimension/flow_level 分布（区域对流量参照，语义裁定用）
- 054 载体成长：dev dim.carrier / dwd.enterprise_growth_trend / dwd.enterprise_innovation_carrier 行数复核
- 060 高价值成果：jiuxin ads_research_outcome_* 表清单+行数（科研产出评价面语义裁定用）

铁律：dev 只认 gkxlumenx_*（禁 demo_*/_devdb）；gkx 只读；jiuxin SHOW TABLES 实数勿写死表数。
产物：code/_snapshots/_shared_s308_lane_a_out.json
"""
import json
import os
import sys
import time

import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "_snapshots", "_shared_s308_lane_a_out.json")

R = {"generated": "2026-11-02", "lane": "S3-08-LaneA"}

DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor,
           connect_timeout=20, read_timeout=300)

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", connect_timeout=60,
           read_timeout=600, write_timeout=600, autocommit=True)

JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev", charset="utf8mb4",
          cursorclass=pymysql.cursors.DictCursor, connect_timeout=30, read_timeout=600)


def retry_connect(cfg, n=3):
    last = None
    for _ in range(n):
        try:
            return pymysql.connect(**cfg)
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(3)
    raise last


# ============ ① dev live ============
dev_out = {}
try:
    conn = retry_connect(DEV)
    cur = conn.cursor()
    # 词族表名扫描（gkxlumenx_* 全库，禁 demo_；该实例 information_schema 列名大写）
    cur.execute("SELECT TABLE_SCHEMA AS sch, TABLE_NAME AS tbl FROM information_schema.tables "
                "WHERE TABLE_SCHEMA LIKE 'gkxlumenx%%' ORDER BY TABLE_SCHEMA, TABLE_NAME")
    dev_tables = [f"{r['sch']}.{r['tbl']}" for r in cur.fetchall()]
    dev_out["table_total"] = len(dev_tables)
    fams = {
        "score": ["score", "rating", "evaluat", "assess"],
        "heat": ["heat", "hot"],
        "path": ["path", "route", "corridor", "roadmap"],
        "reserv": ["reserv", "booking", "appoint"],
        "service_order": ["service_order", "service_log", "order"],
    }
    for g, ws in fams.items():
        dev_out[f"word_{g}"] = sorted([t for t in dev_tables if any(w in t.lower() for w in ws)])
    # 043/047 评分面实证
    for schema, table in [("gkxlumenx_ads", "enterprise_score"), ("gkxlumenx_ads", "carrier_index"),
                          ("gkxlumenx_ads", "chain_hotspot"), ("gkxlumenx_ads", "innovation_event"),
                          ("gkxlumenx_dwd", "enterprise_growth_trend"),
                          ("gkxlumenx_dwd", "enterprise_innovation_carrier"),
                          ("gkxlumenx_dim", "carrier")]:
        key = f"{schema}.{table}"
        try:
            cur.execute(f"SELECT COLUMN_NAME AS col FROM information_schema.columns "
                        f"WHERE TABLE_SCHEMA='{schema}' AND TABLE_NAME='{table}' ORDER BY ORDINAL_POSITION")
            cols = [r["col"] for r in cur.fetchall()]
            cur.execute(f"SELECT COUNT(*) AS n FROM `{schema}`.`{table}`")
            n = cur.fetchone()["n"]
            dev_out[key] = {"columns": cols, "rows": n}
        except Exception as e:  # noqa: BLE001
            dev_out[key] = {"error": repr(e)}
    # 061 service 词族列级复核（service_count/service_item 类列在哪些表）
    cur.execute("SELECT TABLE_SCHEMA AS sch, TABLE_NAME AS tbl, COLUMN_NAME AS col "
                "FROM information_schema.columns "
                "WHERE TABLE_SCHEMA LIKE 'gkxlumenx%%' AND (COLUMN_NAME LIKE '%%service_count%%' "
                "OR COLUMN_NAME LIKE '%%service_total%%' OR COLUMN_NAME LIKE '%%service_item%%') "
                "ORDER BY TABLE_SCHEMA, TABLE_NAME")
    dev_out["service_count_like_columns"] = [
        f"{r['sch']}.{r['tbl']}.{r['col']}" for r in cur.fetchall()]
    cur.close(); conn.close()
except Exception as e:  # noqa: BLE001
    dev_out["error"] = repr(e)
R["dev"] = dev_out

# ============ ② gkx ============
gkx_out = {}
try:
    conn = retry_connect(GKX)
    cur = conn.cursor()
    cur.execute("SET NAMES utf8mb4")
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' ORDER BY table_name")
    gkx_tables = sorted([r[0] for r in cur.fetchall()])
    gkx_out["table_count"] = len(gkx_tables)
    fams_g = {
        "score": ["score", "rating", "evaluat", "assess"],
        "heat": ["heat", "hot"],
        "path": ["path", "route", "corridor", "roadmap"],
        "reserv": ["reserv", "booking", "appoint"],
        "service": ["service"],
    }
    for g, ws in fams_g.items():
        gkx_out[f"word_{g}"] = sorted([t for t in gkx_tables if any(w in t.lower() for w in ws)])
    cur.close(); conn.close()
except Exception as e:  # noqa: BLE001
    gkx_out["error"] = repr(e)
R["gkx"] = gkx_out

# ============ ③ jiuxin（Doris，SHOW TABLES 实数） ============
jx = {}
try:
    conn = retry_connect(JX)
    cur = conn.cursor()
    cur.execute("SHOW TABLES")
    tables = sorted([list(r.values())[0] for r in cur.fetchall()])
    jx["table_count_live"] = len(tables)
    fams_j = {
        "path": ["path", "route", "corridor", "roadmap", "link"],
        "outcome": ["research_outcome"],
        "value_rank": ["value", "ranking", "rank"],
    }
    for g, ws in fams_j.items():
        jx[f"word_{g}"] = sorted([t for t in tables if any(w in t.lower() for w in ws)])
    # 038 区域热点候选：ads_geo_yearly_metrics 结构+覆盖（patent_count 列不存在，用实有度量列）
    cur.execute("SELECT COUNT(*) AS n FROM ads_geo_yearly_metrics")
    jx["geo_yearly_rows"] = cur.fetchone()["n"]
    cur.execute("SELECT location_level, COUNT(*) AS n FROM ads_geo_yearly_metrics "
                "GROUP BY location_level")
    jx["geo_yearly_level_dist"] = {r["location_level"]: r["n"] for r in cur.fetchall()}
    cur.execute("SELECT statistics_year, COUNT(*) AS n FROM ads_geo_yearly_metrics "
                "GROUP BY statistics_year ORDER BY statistics_year")
    jx["geo_yearly_year_dist"] = {str(r["statistics_year"]): r["n"] for r in cur.fetchall()}
    # 深圳市级 + 区县级 location 覆盖（ads_location 自带 city_location_id）
    cur.execute("SELECT location_id, name_zh, location_level FROM ads_location "
                "WHERE location_id IN (SELECT city_location_id FROM ads_location "
                "WHERE name_zh = '深圳') OR name_zh = '深圳' ORDER BY location_level, name_zh LIMIT 20")
    jx["sz_location_candidates"] = [
        {"location_id": r["location_id"], "name": r["name_zh"], "level": r["location_level"]}
        for r in cur.fetchall()]
    sz_ids = [c["location_id"] for c in jx["sz_location_candidates"]]
    if sz_ids:
        ids = ",".join(f"'{i}'" for i in sz_ids)
        cur.execute(f"SELECT m.location_id, m.statistics_year, m.paper_count, "
                    f"m.project_count, m.institution_count, m.mobility_event_count, m.new_institution_count "
                    f"FROM ads_geo_yearly_metrics m WHERE m.location_id IN ({ids}) "
                    f"ORDER BY m.location_id, m.statistics_year LIMIT 200")
        jx["sz_geo_yearly_sample"] = [
            {k: (str(v) if v is not None else None) for k, v in r.items()} for r in cur.fetchall()]
    # 050-052 路径域参照：ads_talent_mobility_yearly_flow 分布
    cur.execute("SELECT COUNT(*) AS n FROM ads_talent_mobility_yearly_flow")
    jx["mobility_flow_rows"] = cur.fetchone()["n"]
    cur.execute("SELECT flow_dimension, flow_level, COUNT(*) AS n FROM ads_talent_mobility_yearly_flow "
                "GROUP BY flow_dimension, flow_level ORDER BY n DESC LIMIT 20")
    jx["mobility_flow_dim_dist"] = [
        {"flow_dimension": r["flow_dimension"], "flow_level": r["flow_level"], "n": r["n"]}
        for r in cur.fetchall()]
    # 060 成果价值面：ads_research_outcome_* 行数
    outcome_tables = [t for t in tables if "research_outcome" in t]
    jx["research_outcome_rows"] = {}
    for t in outcome_tables:
        try:
            cur.execute(f"SELECT COUNT(*) AS n FROM `{t}`")
            jx["research_outcome_rows"][t] = cur.fetchone()["n"]
        except Exception as e:  # noqa: BLE001
            jx["research_outcome_rows"][t] = repr(e)
    cur.close(); conn.close()
except Exception as e:  # noqa: BLE001
    jx["error"] = repr(e)
R["jiuxin"] = jx

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(R, f, ensure_ascii=False, indent=1, default=str)
print("probe written:", OUT)
print("dev tables:", dev_out.get("table_total"), "| gkx:", gkx_out.get("table_count"),
      "| jiuxin live:", jx.get("table_count_live"))
print("dev enterprise_score:", dev_out.get("gkxlumenx_ads.enterprise_score", {}).get("rows"),
      "| carrier_index:", dev_out.get("gkxlumenx_ads.carrier_index", {}).get("rows"))
print("jiuxin geo_yearly rows:", jx.get("geo_yearly_rows"), "| sz candidates:",
      len(jx.get("sz_location_candidates", [])))
print("mobility flow rows:", jx.get("mobility_flow_rows"))
print("outcome tables:", jx.get("research_outcome_rows"))
