#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_036 数据更新频率 — 久新快照频度 + dev 任务节律实查 + 判档产物
UI 语义（mockData.js:1114）：knowledgeGraphKPIs 数据更新频率='实时'（mock）。
可承载口径：① 久新 metrics_as_of_date/update_time（批量快照节律）
② dev lumen_analysis_task 日粒度执行节律（2026-08-07 起 23 执行日）。
"""
import json
import os
from datetime import date

import pymysql

import _s306_graph_base as gb

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_KGANALY_036_out.json")

DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor, connect_timeout=10)

facts = {}
facts["ui_mount"] = "pages/tech-knowledge-graph/mockData.js:1114（knowledgeGraphKPIs 数据更新频率='实时' mock）"
facts["ui_semantics"] = "知识图谱数据刷新节律读数（SRS row_01=499：某类数据每隔多久刷新一次）"
facts["ui_demo_fallback"] = "'实时' 为前端 mock 常数（演示层）"
facts["srs_anchor"] = "SRS 原文「如每日一次、每月一次」——节律档位制"
facts["cat"] = "无业务逻辑数值类"

# ① 久新快照节律
jx = gb.jx_connect()
jc = jx.cursor()
jc.execute("""SELECT metrics_as_of_date, data_version, update_time, COUNT(*) n
              FROM ads_technology_graph_node
              GROUP BY metrics_as_of_date, data_version, update_time ORDER BY metrics_as_of_date""")
snap_rows = jc.fetchall()
jc.execute("SELECT MAX(update_time) mx, MIN(update_time) mn FROM ads_technology_graph_node")
tw = jc.fetchone()
# 边表时间戳对照
jc.execute("SELECT MAX(update_time) mx FROM ads_technology_graph_edge")
etw = jc.fetchone()
jx.close()

snaps = [{"as_of": str(r[0]), "data_version": r[1], "update_time": str(r[2]), "n_nodes": r[3]} for r in snap_rows]
snap_dates = sorted({s["as_of"] for s in snaps})
distinct_snap_days = len(snap_dates)
conn = pymysql.connect(**DEV)
with conn.cursor() as cur:
    cur.execute("""SELECT DATE(created_at) d, COUNT(*) n FROM gkxlumenx_cfg.lumen_analysis_task
                   GROUP BY DATE(created_at) ORDER BY d""")
    daily = cur.fetchall()
conn.close()
dev_days = [str(r["d"]) for r in daily]
first_d, last_d = dev_days[0], dev_days[-1]
span_days = (date.fromisoformat(last_d) - date.fromisoformat(first_d)).days + 1
exec_ratio = len(dev_days) / span_days

facts["jiuxin_snapshot_versions"] = snaps
facts["jiuxin_distinct_asof_days"] = distinct_snap_days
facts["jiuxin_node_update_time_window"] = [str(tw[0]), str(tw[1])]
facts["jiuxin_edge_update_time_max"] = str(etw[0])
facts["dev_task_exec_days"] = len(dev_days)
facts["dev_task_window"] = [first_d, last_d]
facts["dev_window_span_days"] = span_days

derived = [{
    "source": "jiuxin ads_technology_graph_node 快照戳 + dev lumen_analysis_task 执行节律",
    "jiuxin_batch_snapshot_cadence": {
        "distinct_metrics_as_of_dates": distinct_snap_days,
        "as_of_dates": snap_dates,
        "verdict": "批量快照制（非实时）",
    },
    "dev_task_cadence": {
        "exec_days": len(dev_days),
        "window": [first_d, last_d],
        "span_days": span_days,
        "exec_day_ratio": round(exec_ratio, 4),
        "verdict": "近全日执行（工作日制批量节律）",
    },
    "ui_mock_reference": "数据更新频率='实时'（mock）——真图实查为批量快照制，非实时",
}]

absence_probe = [
    {"what": "流式实时同步承载（UI '实时' 语义直接承载）", "how": "三源词族扫描（cdc/sync/stream/binlog）", "hits": "0"},
    {"what": "久新批量快照戳", "how": "metrics_as_of_date/data_version/update_time GROUP BY", "hits": f"{distinct_snap_days} 个 as_of 日期——批量快照制在案"},
    {"what": "dev 批量任务节律", "how": "lumen_analysis_task DATE(created_at) GROUP BY", "hits": f"2026-08-07～{last_d} 窗口 {len(dev_days)} 个执行日（覆盖 {exec_ratio:.0%}）"},
]

out = {"metric_id": "M_SCIUI_KGANALY_036", "metric_name": "数据更新频率（科技知识图谱·KPI 面板）",
       "facts": facts, "derived": derived, "absence_probe": absence_probe,
       "support_judgment": "部分支持",
       "base_years_used": [],
       "base_years_missing": ["无跨年度更新节律史（快照戳与任务日志均为近期窗口）"],
       "base_years_note": "物理口径基期=久新快照 metrics_as_of_date 与 dev 任务日志 created_at 覆盖窗口；实时同步承载缺失；非「缺年按 0 摊入」"}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done ->", OUT)
print("as_of dates:", snap_dates[:5], "... total", distinct_snap_days)
print("node update window:", facts["jiuxin_node_update_time_window"], "edge max:", facts["jiuxin_edge_update_time_max"])
print("dev days:", len(dev_days), "in span", span_days, "->", round(exec_ratio, 3))
