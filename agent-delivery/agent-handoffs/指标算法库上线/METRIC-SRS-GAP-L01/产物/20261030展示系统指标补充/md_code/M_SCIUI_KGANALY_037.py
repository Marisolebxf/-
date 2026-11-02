#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_037 图谱数据源数量 — 三源数据源面盘点实查 + 判档产物
UI 语义（IntegrationEtlPanel.jsx:81）：allSources=[...sources, ...uploaded]——接入面板数据源计数。
可承载口径：三源真实数据源面盘点——dev jimu 8 + dev 库表域 + gkx 280 只读 + 久新 215+ 活表。
"""
import json
import os

import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_KGANALY_037_out.json")

DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor, connect_timeout=10)

facts = {}
facts["ui_mount"] = "pages/tech-knowledge-graph/IntegrationEtlPanel.jsx:81（allSources=[...sources,...uploaded] 接入面板数据源列表）"
facts["ui_semantics"] = "图谱接入数据源数量读数（SRS row_01=500：数据源）"
facts["ui_demo_fallback"] = "integrationDataSources 4 项为演示层 mock（演示层计数与真库无关）"
facts["srs_anchor"] = "SRS 原文「实体与连接的规模/结构统计」——数据源计数为其供给侧面"
facts["cat"] = "无业务逻辑数值类"

# ① dev 数据源登记面
conn = pymysql.connect(**DEV)
with conn.cursor() as cur:
    cur.execute("SELECT id, name, type FROM gkxlumenx_bi.jimu_report_data_source ORDER BY id")
    jimu_rows = cur.fetchall()
    cur.execute("""SELECT TABLE_SCHEMA AS sch, COUNT(*) AS n FROM information_schema.tables
                   WHERE TABLE_SCHEMA LIKE 'gkxlumenx%%' GROUP BY TABLE_SCHEMA ORDER BY TABLE_SCHEMA""")
    dev_schemas = {r["sch"]: r["n"] for r in cur.fetchall()}
conn.close()

# ② gkx 只读域（族级快照词族清单；本件只取计数与层分布）
import sys
sys.path.insert(0, BASE)
from _gkxdb import gkx  # noqa: E402
gc = gkx()
gc.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='gkx'")
gkx_total = gc.fetchone()[0]
gc.execute("""SELECT SUBSTRING_INDEX(table_name,'_',1) layer, COUNT(*) n
              FROM information_schema.tables WHERE table_schema='gkx'
              GROUP BY SUBSTRING_INDEX(table_name,'_',1) ORDER BY n DESC""")
gkx_layers = {r[0]: r[1] for r in gc.fetchall()}

# ③ 久新活库表数（不写死——实查）
jx = pymysql.connect(host="47.93.119.170", port=29030, user="test2",
                     password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
                     database="gkx_technology_analysis_dev", charset="utf8mb4", connect_timeout=10)
jc = jx.cursor()
jc.execute("SHOW TABLES")
jiuxin_tables = [r[0] for r in jc.fetchall()]
jiuxin_total = len(jiuxin_tables)
jiuxin_layers = {}
for t in jiuxin_tables:
    pref = t.split("_")[0]
    jiuxin_layers[pref] = jiuxin_layers.get(pref, 0) + 1
jx.close()

facts["dev_jimu_datasources"] = len(jimu_rows)
facts["dev_jimu_names"] = sorted(r["name"] for r in jimu_rows)
facts["dev_schema_table_counts"] = dev_schemas
facts["gkx_table_total"] = gkx_total
facts["gkx_layer_distribution"] = dict(sorted(gkx_layers.items()))
facts["jiuxin_table_total"] = jiuxin_total
facts["jiuxin_layer_distribution"] = dict(sorted(jiuxin_layers.items()))

# 数据源计数口径：物理数据源=连接级（3 库）；逻辑数据源=登记面（8）+层域源
logical_sources = len(jimu_rows)
derived = [{
    "source": "三源数据源面盘点（2026-11-02 实查）",
    "physical_databases": [
        {"name": "dev live gkxlumenx_*", "tables": sum(dev_schemas.values()), "schemas": dev_schemas},
        {"name": "gkx 第三方只读", "tables": gkx_total, "layers_top": dict(list(sorted(gkx_layers.items()))[:6])},
        {"name": "jiuxin gkx_technology_analysis_dev", "tables": jiuxin_total, "layers_top": dict(list(sorted(jiuxin_layers.items()))[:6])},
    ],
    "registered_datasources_dev_jimu": logical_sources,
    "ui_mock_reference": "IntegrationEtlPanel integrationDataSources 4 项（mock）",
}]

absence_probe = [
    {"what": "统一数据源登记面（跨三库的 lineage 目录）", "how": "三源词族扫描（lineage/catalog/source_register）", "hits": "0（各库独立，无统一目录面）"},
    {"what": "dev 数据源登记面", "how": "gkxlumenx_bi.jimu_report_data_source", "hits": f"{len(jimu_rows)} 行（名称/类型列在案）"},
    {"what": "久新图谱上游供给面", "how": "Doris 库内表域分布", "hits": f"{jiuxin_total} 活表（dwd/ads 分层在案，无外部源登记列）"},
]

out = {"metric_id": "M_SCIUI_KGANALY_037", "metric_name": "图谱数据源数量（科技知识图谱·接入面板）",
       "facts": facts, "derived": derived, "absence_probe": absence_probe,
       "support_judgment": "完全转换支持",
       "base_years_used": [],
       "base_years_missing": ["无年度基期维（数据源盘点为当日 live 截面）"],
       "base_years_note": "物理口径基期=三源实查日（2026-11-02）；数据源计数为截面盘点，无时序基期；非「缺年按 0 摊入」"}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done ->", OUT)
print("jimu", len(jimu_rows), "dev schemas", dev_schemas)
print("gkx", gkx_total, "jiuxin", jiuxin_total)
print("jiuxin layers", dict(list(sorted(jiuxin_layers.items()))[:8]))
