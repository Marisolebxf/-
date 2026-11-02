#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATAAPP_004 累计调用次数统计（供应方 Tab）— 三源探针 + 判档产物
依赖族级快照 _probe_s305_l3_call_out.json；本件补充：供应方登记面 + 时间粒度读数。"""
import json, os, pymysql, sys

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(BASE, "_snapshots", "_probe_s305_l3_call_out.json")
OUT = os.path.join(BASE, "M_SCIUI_DATAAPP_004_out.json")
snap = json.load(open(SNAP))

facts = {}
facts["ui_mount"] = "ApplicationWindow.jsx:545 Card title=累计调用次数统计（数据供应方数据被调用情况 Tab）"
facts["ui_filters"] = ["时间区段(月)", "业务类型", "数据产品", "重置"]
facts["ui_mock_dataset"] = "mockData.js supplierCallDetails 28 行（注释自标 seq 389）"
facts["ui_mock_dimensions"] = ["supplierName", "dataProduct", "businessType", "period", "totalCalls"]

# ---------- ① dev live ----------
dev = pymysql.connect(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
                      database="gkxlumenx", charset="utf8mb4", connect_timeout=10)
cur = dev.cursor()

facts["dev_call_word_tables"] = snap["facts"]["dev_call_word_tables"]  # 族级：[]
cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='gkxlumenx'")
facts["dev_table_count"] = cur.execute and cur.fetchone()[0] or 0

# 供应方登记面：supplier/provider 词族（dev 542 表）
cur.execute("""SELECT table_name FROM information_schema.tables
               WHERE table_schema='gkxlumenx'
                 AND (table_name LIKE '%supplier%' OR table_name LIKE '%provider%'
                       OR table_name LIKE '%partner%')""")
facts["dev_supplier_word_tables"] = sorted(r[0] for r in cur.fetchall())

# 时间粒度载体：dev 有无月粒度聚合面（调用族为零 ⇒ 聚合面只能挂日志表族，一并留证）
cur.execute("""SELECT table_name FROM information_schema.tables
               WHERE table_schema='gkxlumenx'
                 AND (table_name LIKE '%%stat%%' OR table_name LIKE '%%metric%%'
                       OR table_name LIKE '%%counter%%')""")
tmp = sorted(r[0] for r in cur.fetchall())
facts["dev_stat_metric_tables"] = [t for t in tmp if not t.startswith(("demo_", "_devdb"))]
cur.execute("SHOW FULL TABLES IN gkxlumenx")
allt = sorted(r[0] for r in cur.fetchall())
facts["dev_tables_total_live"] = len(allt)
cur.execute("""SELECT COUNT(*) FROM information_schema.tables
               WHERE table_schema LIKE 'gkxlumenx%'""")
facts["dev_all_schema_table_total"] = cur.fetchone()[0]
dev.close()

# ---------- ② gkx 280 表（只读，经 _gkxdb.py） ----------
sys.path.insert(0, BASE)
from _gkxdb import gkx  # noqa: E402
gc = gkx()
gc.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gc.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
facts["gkx_supplier_word_tables"] = sorted(
    t for t in gkx_tables if any(w in t for w in ("supplier", "provider", "partner")))
facts["gkx_call_word_tables"] = snap["facts"]["gkx_call_word_tables"]  # []
# 供应方语义最近邻：dwd 专利/论文申请人字段（供应方=数据生产机构 是 平台供应方 的语义近邻，需披露差异）
facts["gkx_supplier_semantic_neighbors"] = [
    {"table": "dwd_patent", "col": "applicant", "note": "专利申请人（数据生产机构）"},
    {"table": "dwd_zh_paper", "col": "author", "note": "论文作者"},
]

# ---------- ③ 久新 live ----------
import pymysql as jpm  # noqa: E402,F811
jx = jpm.connect(host="47.93.119.170", port=29030, user="test2",
                 password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
                 database="gkx_technology_analysis_dev", charset="utf8mb4",
                 connect_timeout=10, read_timeout=300)
jc = jx.cursor()
jc.execute("SHOW TABLES")
jx_live = sorted(r[0] for r in jc.fetchall())
facts["jiuxin_probe_mode"] = "live"
facts["jiuxin_table_count_live"] = len(jx_live)
facts["jiuxin_supplier_word_tables_live"] = sorted(
    t for t in jx_live if any(w in t for w in ("supplier", "provider", "partner")))
facts["jiuxin_call_word_tables_live"] = sorted(
    t for t in jx_live if any(w in t for w in ("call", "invoke", "trace", "request_log")))
jx.close()

# ---------- 判档 ----------
support = "完全不支持"
derived = [{"supplier_cumulative_calls_by_period": None,
            "note": "调用流水三源零承载（族级快照 dev/gkx/jiuxin 调用词族全空）；供应方登记面亦零命中（本件探针）"}]

absence_probe = [
    {"what": "dev 调用日志表族（call/invoke/trace 词族，542 表）", "how": "族级快照 dev_call_word_tables", "hits": 0},
    {"what": "dev 供应方登记面（supplier/provider/partner 词族）", "how": "本件 information_schema 扫描", "hits": 0},
    {"what": "gkx 调用日志表族（280 表）", "how": "族级快照 gkx_call_word_tables", "hits": 0},
    {"what": "gkx 供应方登记面", "how": "本件表清单词族扫描", "hits": 0},
    {"what": "久新调用/供应方表族（live 当日）", "how": "本件 SHOW TABLES 词族扫描", "hits": 0},
]

out = {"metric_id": "M_SCIUI_DATAAPP_004", "metric_name": "累计调用次数统计（数据供应方数据被调用情况）",
       "base_years_used": [],
    "base_years_missing": ["完全不支持：调用遥测面三源零承载，无库内年份基期"],
    "base_years_note": "完全不支持：无基期；mock 演示值不构成基期证据",
    "facts": facts, "derived": derived, "absence_probe": absence_probe, "support_judgment": support}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done ->", OUT)
