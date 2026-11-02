#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_029 异常数据监测 — 三源探针 + dev 任务链路失败率实算 + 判档产物
UI 语义（kgL6Functions.js:22 / BlacklistTriggerPanel）：数据搬运/刷新任务失败监测。
dev cfg.lumen_analysis_task（339 行）是真实链路日志承载——失败率可实算；
流式实时错误率承载缺失（realtimeMonitor.js 为 mock 读数 0.8%）。
"""
import json
import os

import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_KGANALY_029_out.json")

DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor, connect_timeout=10)

facts = {}
facts["ui_mount"] = "pages/tech-knowledge-graph/kgL6Functions.js:22（异常数据监测卡片）| BlacklistTriggerPanel.jsx:147 | IndicatorDisplay.jsx:33 | mockData.js:285"
facts["ui_semantics"] = "数据搬运/刷新任务失败监测——数据链路健康度（SRS row_01=492：「数据链路出没出问题」）"
facts["ui_demo_fallback"] = "realtimeMonitor.js:9 mock 读数 errorRate=0.8%（阈值 2.5%）——前端演示常数，非实算"
facts["srs_anchor"] = "分析展示.md seq 408：异常数据监测（黑名单触发面板）"
facts["cat"] = "无业务逻辑数值类"

task_stats = {}
node_stats = {}
daily_fail = []
err_samples = []

conn = pymysql.connect(**DEV)
with conn.cursor() as cur:
    cur.execute("SELECT COUNT(*) n FROM gkxlumenx_cfg.lumen_analysis_task")
    task_stats["total"] = cur.fetchone()["n"]
    cur.execute("""SELECT status, COUNT(*) n
                   FROM gkxlumenx_cfg.lumen_analysis_task GROUP BY status ORDER BY status""")
    task_stats["by_status"] = {r["status"]: r["n"] for r in cur.fetchall()}
    cur.execute("""SELECT COUNT(DISTINCT DATE(created_at)) n FROM gkxlumenx_cfg.lumen_analysis_task""")
    task_stats["distinct_dates"] = cur.fetchone()["n"]
    cur.execute("""SELECT DATE(created_at), SUM(status='failed') failed, COUNT(*) total
                   FROM gkxlumenx_cfg.lumen_analysis_task GROUP BY DATE(created_at) ORDER BY DATE(created_at)""")
    for r in cur.fetchall():
        daily_fail.append({"date": str(r["DATE(created_at)"]), "failed": int(r["failed"]), "total": int(r["total"]),
                           "fail_rate": round(int(r["failed"]) / r["total"], 6) if r["total"] else None})
    cur.execute("""SELECT error_message, COUNT(*) n FROM gkxlumenx_cfg.lumen_analysis_task
                   WHERE status='failed' GROUP BY error_message ORDER BY n DESC LIMIT 5""")
    for r in cur.fetchall():
        err_samples.append({"error": (r["error_message"] or "")[:120], "count": r["n"]})
    try:
        cur.execute("""SELECT node_status, COUNT(*) n FROM gkxlumenx_cfg.lumen_analysis_task_node
                       GROUP BY node_status ORDER BY node_status""")
        node_stats["by_status"] = {r["node_status"]: r["n"] for r in cur.fetchall()}
        cur.execute("SELECT COUNT(*) n FROM gkxlumenx_cfg.lumen_analysis_task_node")
        node_stats["total"] = cur.fetchone()["n"]
    except Exception as ex:
        node_stats["error"] = str(ex)[:200]
conn.close()

total = task_stats["total"]
failed = task_stats["by_status"].get("failed", 0)
success = task_stats["by_status"].get("success", 0)
cancelled = task_stats["by_status"].get("cancelled", 0)
facts["dev_task_total"] = total
facts["dev_task_failed"] = failed
facts["dev_task_success"] = success
facts["dev_task_cancelled"] = cancelled
facts["dev_task_distinct_dates"] = task_stats["distinct_dates"]

derived = [{
    "source": "dev gkxlumenx_cfg.lumen_analysis_task（真实链路日志）",
    "task_fail_rate_overall": round(failed / total, 6) if total else None,
    "task_fail_rate_excl_cancelled": round(failed / (total - cancelled), 6) if (total - cancelled) else None,
    "status_breakdown": task_stats["by_status"],
    "node_status_breakdown": node_stats.get("by_status"),
    "daily_fail_series": daily_fail,
    "top_error_messages": err_samples,
}]

absence_probe = [
    {"what": "流式/实时接入错误率承载面", "how": "dev+gkx+久新三源词族扫描（stream/realtime/error_rate/offset/lag）", "hits": "0（无 Flink/Kafka lag 面、无实时错误率表）"},
    {"what": "久新图谱侧任务日志", "how": "218 表词族扫描（task/job/etl/log）", "hits": "0（Doris 为分析结果面，无调度日志）"},
    {"what": "UI 实时错误率读数来源", "how": "realtimeMonitor.js 读码", "hits": "mock 常数 0.8%（阈值 2.5%），演示层自披露"},
    {"what": "dev 任务链路日志", "how": "gkxlumenx_cfg.lumen_analysis_task 实查", "hits": f"{total} 行真实执行记录（failed={failed}）——批量链路承载在案"},
]

out = {"metric_id": "M_SCIUI_KGANALY_029", "metric_name": "异常数据监测（科技知识图谱·数据链路健康度）",
       "facts": facts, "derived": derived, "absence_probe": absence_probe,
       "support_judgment": "部分支持",
       "base_years_used": [],
       "base_years_missing": ["无跨年度基期（dev 任务日志为近期执行记录）"],
       "base_years_note": "物理口径基期=dev 任务日志 DATE(created_at) 覆盖区间；流式实时错误率承载缺失故无实时基期；非「缺年按 0 摊入」"}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done ->", OUT)
print("total", total, "failed", failed, "rate", round(failed / total, 4) if total else None)
print("daily points", len(daily_fail), "node_stats", node_stats.get("by_status") or node_stats.get("error"))
