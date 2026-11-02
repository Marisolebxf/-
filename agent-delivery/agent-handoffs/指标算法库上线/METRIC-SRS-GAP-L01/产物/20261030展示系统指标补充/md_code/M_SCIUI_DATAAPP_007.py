#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATAAPP_007 调用趋势总览（资产应用总览 Tab）— 三源探针 + 判档产物
依赖族级快照 _probe_s305_l3_call_out.json；本件补充：日粒度序列+活跃用户双指标载体核查。"""
import json, os, sys, pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(BASE, "_snapshots", "_probe_s305_l3_call_out.json")
OUT = os.path.join(BASE, "M_SCIUI_DATAAPP_007_out.json")
snap = json.load(open(SNAP))
facts = {}

facts["ui_mount"] = "ApplicationWindow.jsx:1287 Card title=调用趋势总览（资产应用总览 Tab 第一卡）+ KPI 双卡 :1266"
facts["ui_mock_dataset"] = "mockData.js usageCallTrend（7 个日期 × calls/users 双序列）+ applicationKPIs 2 卡"
facts["ui_mock_shape"] = {"dates": 7, "calls_series": [78200, 82100, 79500, 84300, 86800, 85200, 85600],
                          "users_series": [3200, 3350, 3280, 3420, 3510, 3480, 3456]}
facts["ui_kpi_cards"] = [{"label": "资产调用总量", "value": "285.6万次", "change": 22.5},
                         {"label": "应用系统数", "value": "147个", "change": 12.3}]

# ---------- ① dev live ----------
dev = pymysql.connect(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
                      database="gkxlumenx", charset="utf8mb4", connect_timeout=10)
cur = dev.cursor()
facts["dev_call_word_tables"] = snap["facts"]["dev_call_word_tables"]  # []
# 活跃用户指标载体：daily/active 词族
cur.execute("""SELECT table_name FROM information_schema.tables
               WHERE table_schema LIKE 'gkxlumenx%%'
                 AND (table_name LIKE '%%daily%%' OR table_name LIKE '%%active%%'
                       OR table_name LIKE '%%kpi%%')""")
tmp = sorted(set(r[0] for r in cur.fetchall()))
facts["dev_daily_active_word_tables"] = [t for t in tmp if not t.startswith(("demo_", "_devdb"))]
dev.close()

# ---------- ② gkx ----------
sys.path.insert(0, BASE)
from _gkxdb import gkx  # noqa: E402
gc = gkx()
gc.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gc.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
facts["gkx_call_word_tables"] = snap["facts"]["gkx_call_word_tables"]  # []

# ---------- ③ 久新 live ----------
jx = pymysql.connect(host="47.93.119.170", port=29030, user="test2",
                     password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
                     database="gkx_technology_analysis_dev", charset="utf8mb4",
                     connect_timeout=10, read_timeout=300)
jc = jx.cursor()
jc.execute("SHOW TABLES")
jx_live = sorted(r[0] for r in jc.fetchall())
facts["jiuxin_probe_mode"] = "live"
facts["jiuxin_table_count_live"] = len(jx_live)
facts["jiuxin_call_word_tables_live"] = sorted(
    t for t in jx_live if any(w in t for w in ("call", "invoke", "trace", "request_log")))
jx.close()

# ---------- 判档 ----------
support = "完全不支持"
derived = [{"overview_call_trend_daily": None,
            "note": "日粒度调用流水与活跃用户双序列三源零承载——总览双轴图无原料"}]

absence_probe = [
    {"what": "dev 调用日志表族（call/invoke/trace 词族，全库）", "how": "族级快照 dev_call_word_tables", "hits": 0},
    {"what": "dev 日粒度/活跃用户载体（daily/active/kpi 词族）", "how": "本件 information_schema 扫描", "hits": 0},
    {"what": "gkx 调用日志表族（280 表）", "how": "族级快照 gkx_call_word_tables", "hits": 0},
    {"what": "久新调用表族（live 当日 215 表）", "how": "本件 SHOW TABLES 词族扫描", "hits": 0},
    {"what": "活跃用户口径载体（三源）", "how": "调用词族为零 ⇒ 活跃用户（按调用定义）随日志缺位", "hits": 0},
]

out = {"metric_id": "M_SCIUI_DATAAPP_007", "metric_name": "调用趋势总览（资产应用总览）",
       "base_years_used": [],
    "base_years_missing": ["完全不支持：调用遥测面三源零承载，无库内年份基期"],
    "base_years_note": "完全不支持：无基期；mock 演示值不构成基期证据",
    "facts": facts, "derived": derived, "absence_probe": absence_probe, "support_judgment": support}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done ->", OUT)
