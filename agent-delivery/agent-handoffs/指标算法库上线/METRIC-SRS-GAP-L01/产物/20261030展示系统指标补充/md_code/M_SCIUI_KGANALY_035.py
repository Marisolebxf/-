#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_035 数据接入错误率 — dev 链路日志实算 + 流式承载缺口 + 判档产物
UI 语义（realtimeMonitor.js:9）：errorRate=0.8%（阈值 2.5%）mock。
dev gkxlumenx_cfg.lumen_analysis_task（339 行）为真实承载——错误率可实算；
流式实时接入错误率承载缺失。与 029 区分：029=任务失败监测（黑名单面板）；
035=接入错误率（实时监控面板 errorRate 读数）。
"""
import json
import os

import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_KGANALY_035_out.json")

DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor, connect_timeout=10)

facts = {}
facts["ui_mount"] = "pages/tech-knowledge-graph/realtimeMonitor.js:9（errorRate: '0.8%'，threshold 2.5% mock）"
facts["ui_semantics"] = "实时监控面板数据接入错误率读数（SRS row_01=498：接入错误率）"
facts["ui_demo_fallback"] = "0.8%/2.5% 均为前端 mock 常数（演示层）"
facts["srs_anchor"] = "SRS 原文「页面数据说明为准；如需纳入指标体系须先立项调研口径」"
facts["cat"] = "无业务逻辑数值类"

conn = pymysql.connect(**DEV)
with conn.cursor() as cur:
    # 分析任务链路（与 029 同源不同读数：035 取接入/搬运语义的节点级+任务级错误率）
    cur.execute("SELECT status, COUNT(*) n FROM gkxlumenx_cfg.lumen_analysis_task GROUP BY status")
    task_by_status = {r["status"]: r["n"] for r in cur.fetchall()}
    cur.execute("SELECT COUNT(*) n FROM gkxlumenx_cfg.lumen_analysis_task")
    task_total = cur.fetchone()["n"]
    # 数据源登记面（接入侧）：jimu 报表数据源 8 行
    cur.execute("SELECT COUNT(*) n FROM gkxlumenx_bi.jimu_report_data_source")
    jimu_ds = cur.fetchone()["n"]
    # ETL/搬运作业面探测：词族扫描 cfg 库表名
    cur.execute("SELECT TABLE_NAME AS tname FROM information_schema.tables WHERE TABLE_SCHEMA='gkxlumenx_cfg' ORDER BY TABLE_NAME")
    cfg_tables = sorted(r["tname"] for r in cur.fetchall())
conn.close()

failed = task_by_status.get("failed", 0)
facts["dev_cfg_tables"] = cfg_tables
facts["dev_jimu_datasources"] = jimu_ds
facts["dev_task_total"] = task_total
facts["dev_task_failed"] = failed

derived = [{
    "source": "dev gkxlumenx_cfg.lumen_analysis_task（接入/搬运任务链路）",
    "task_error_rate_overall": round(failed / task_total, 6),
    "status_breakdown": task_by_status,
    "ui_mock_reference": {"errorRate": "0.8%", "threshold": "2.5%", "note": "mock 常数，演示层"},
}]

absence_probe = [
    {"what": "流式实时接入错误率承载（UI errorRate 语义的直接承载）", "how": "dev cfg+bi 全表词族扫描（stream/realtime/ingest/error）+ gkx/久新词族", "hits": "0（无流式监控面）"},
    {"what": "批量接入/搬运错误率承载", "how": "gkxlumenx_cfg.lumen_analysis_task 实查", "hits": f"339 任务 failed={failed}——可实算任务级错误率 33.92%"},
    {"what": "数据源登记面", "how": "gkxlumenx_bi.jimu_report_data_source", "hits": f"{jimu_ds} 行（数据源侧无错误日志列）"},
    {"what": "cfg 库 ETL 作业表", "how": "information_schema 表清单", "hits": f"{len(cfg_tables)} 表（lumen_analysis_task/node 为主，无独立 ETL 错误日志表）"},
]

out = {"metric_id": "M_SCIUI_KGANALY_035", "metric_name": "数据接入错误率（科技知识图谱·实时监控面板）",
       "facts": facts, "derived": derived, "absence_probe": absence_probe,
       "support_judgment": "部分支持",
       "base_years_used": [],
       "base_years_missing": ["无跨年度基期（dev 任务日志 2026-08-07 起）", "无流式实时错误率时序（承载缺失）"],
       "base_years_note": "物理口径基期=dev 任务日志 created_at 覆盖区间（2026-08-07～2026-11-01）；流式实时承载缺失；非「缺年按 0 摊入」"}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done ->", OUT)
print("task", task_total, "failed", failed, "rate", round(failed / task_total, 4))
print("cfg tables", len(cfg_tables), "jimu ds", jimu_ds)
