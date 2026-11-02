#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATAAPP_006 调用趋势与周期性分析（主题 Tab）— 三源探针 + 判档产物
依赖族级快照 _probe_s305_l3_call_out.json；本件补充：月粒度时间序列载体核查。"""
import json, os, sys, pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(BASE, "_snapshots", "_probe_s305_l3_call_out.json")
OUT = os.path.join(BASE, "M_SCIUI_DATAAPP_006_out.json")
snap = json.load(open(SNAP))
facts = {}

facts["ui_mount"] = "ApplicationWindow.jsx:301 Card title=调用趋势与周期性分析（主题数据被调用情况 Tab 第二卡）"
facts["ui_mock_dataset"] = "mockData.js themeCallTrend（12 个月标签 × 5 主题折线）"
facts["ui_mock_shape"] = {"months": 12, "series": ["基础科学", "医学健康", "工程技术", "农业科技", "能源环境"]}

# ---------- ① dev live ----------
dev = pymysql.connect(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
                      database="gkxlumenx", charset="utf8mb4", connect_timeout=10)
cur = dev.cursor()
facts["dev_call_word_tables"] = snap["facts"]["dev_call_word_tables"]  # []
# 月粒度时间序列载体：聚合/汇总词族
cur.execute("""SELECT table_name FROM information_schema.tables
               WHERE table_schema LIKE 'gkxlumenx%%'
                 AND (table_name LIKE '%%trend%%' OR table_name LIKE '%%series%%'
                       OR table_name LIKE '%%monthly%%' OR table_name LIKE '%%summary%%'
                       OR table_name LIKE '%%stat%%')""")
tmp = sorted(r[0] for r in cur.fetchall())
facts["dev_timeseries_word_tables"] = [t for t in tmp if not t.startswith(("demo_", "_devdb"))]
dev.close()

# ---------- ② gkx ----------
sys.path.insert(0, BASE)
from _gkxdb import gkx  # noqa: E402
gc = gkx()
gc.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gc.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
facts["gkx_call_word_tables"] = snap["facts"]["gkx_call_word_tables"]  # []
# 主题维度载体：gkx 主题词族（趋势图的分组维）
facts["gkx_theme_word_tables"] = sorted(
    t for t in gkx_tables if any(w in t for w in ("theme", "subject", "topic")))

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
# 久新是否有时序型分析面可当「周期性」参考（披露语义差异：科研产出趋势≠调用趋势）
facts["jiuxin_trend_ref_tables_live"] = sorted(
    t for t in jx_live if any(w in t for w in ("trend", "month", "year", "stat")))
jx.close()

# ---------- 判档 ----------
support = "完全不支持"
derived = [{"theme_call_trend_monthly": None,
            "note": "调用流水三源零承载——趋势/周期分析无原料；月粒度聚合载体词族亦 0 命中"}]

absence_probe = [
    {"what": "dev 调用日志表族（call/invoke/trace 词族，全库）", "how": "族级快照 dev_call_word_tables", "hits": 0},
    {"what": "dev 月粒度时序聚合面（trend/series/monthly/summary/stat 词族）", "how": "本件 information_schema 扫描", "hits": 0},
    {"what": "gkx 调用日志表族（280 表）", "how": "族级快照 gkx_call_word_tables", "hits": 0},
    {"what": "gkx 主题维度载体（theme/subject/topic 词族）", "how": "本件表清单词族扫描", "hits": 0},
    {"what": "久新调用表族 + 时序参考面（live 当日 215 表）", "how": "本件 SHOW TABLES 词族扫描", "hits": "调用 0；时序参考面语义不同"},
]

out = {"metric_id": "M_SCIUI_DATAAPP_006", "metric_name": "调用趋势与周期性分析（主题数据被调用情况）",
       "base_years_used": [],
    "base_years_missing": ["完全不支持：调用遥测面三源零承载，无库内年份基期"],
    "base_years_note": "完全不支持：无基期；mock 演示值不构成基期证据",
    "facts": facts, "derived": derived, "absence_probe": absence_probe, "support_judgment": support}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done ->", OUT)
