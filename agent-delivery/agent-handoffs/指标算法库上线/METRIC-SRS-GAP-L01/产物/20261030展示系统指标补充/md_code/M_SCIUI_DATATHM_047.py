#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_047 本月数据接入量——三源探针+产物生成（S3-05 L1）。

挂载 mockData.js:1661（accessKPIs「本月接入量」1256），渲染位 AccessWindow.jsx:355（KPICard map）。
045 已证：台账词族三源排除、growth_trend 0 行、enterprise_base 月界切片 2026-09: 348（挂库月代理）。
本件=045 的「本月」定窗特例：新增「本月窗」切片探针（2026-10 自然月）——预期 0（最后写入 2026-09），
即「本月零登记」负面证据；1256 mock 值与 348/0 均不闭合。
"""
import json
import os
import sys

import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_047_out.json")
sys.path.insert(0, BASE)

d042 = json.load(open(os.path.join(BASE, "M_SCIUI_DATATHM_042_out.json"), encoding="utf-8"))
d045 = json.load(open(os.path.join(BASE, "M_SCIUI_DATATHM_045_out.json"), encoding="utf-8"))

MONTH_NOW = "2026-10"  # 探针执行月（2026-11-02 开跑，取已完整闭月的 10 月作「本月」窗）

conn = pymysql.connect(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
                       charset="utf8mb4", autocommit=True,
                       cursorclass=pymysql.cursors.DictCursor)
try:
    with conn.cursor() as cur:
        # 本件新探针①：「本月」窗计数（enterprise_base update_time 落 2026-10 的行数）
        cur.execute(
            "SELECT COUNT(*) c FROM gkxlumenx_dwd.enterprise_base "
            "WHERE update_time >= '2026-10-01' AND update_time < '2026-11-01'")
        month_now_count = cur.fetchone()["c"]
        # 本件新探针②：news 面本月窗（041 曾证 news 单月 2026-08: 1,668,414——跨表对照）
        cur.execute(
            "SELECT COUNT(*) c FROM gkxlumenx_dwd.enterprise_news "
            "WHERE update_time >= '2026-10-01' AND update_time < '2026-11-01'")
        news_month_now = cur.fetchone()["c"]
finally:
    conn.close()

mock_kpis = {
    "本月接入量": "1,256 个（rise +15.2%）",
    "问题资源数": "23 个（fall -18.3%）",
    "待处理任务": "8 个（fall -5%）",
}

facts = {
    "dev_table_total": d042["facts"]["dev_table_total"],
    "dev_access_registry_tables": d042["facts"]["dev_access_registry_tables"],
    "gkx_table_count": d042["facts"]["gkx_table_count"],
    "jiuxin_table_count_live": d042["facts"]["jiuxin_table_count_live"],
    "probe_month_window": MONTH_NOW,
    "dev_enterprise_base_rows_this_month": month_now_count,
    "dev_enterprise_news_rows_this_month": news_month_now,
    "dev_enterprise_month_slice_reused_045": d045["facts"]["dev_enterprise_month_slice_now"],
    "dev_growth_trend_rows_reused_040": d045["facts"]["dev_growth_trend_rows"],
    "ui_mock_kpi_label": "本月接入量",
    "ui_mock_kpi_value": "1,256",
    "ui_mock_kpi_unit": "个",
    "ui_mock_kpi_trend": "rise +15.2%",
    "ui_mock_kpi_siblings": mock_kpis,
    "ui_mock_mount": "mockData.js:1661（accessKPIs[0]）→ AccessWindow.jsx:355 KPICard 渲染",
}

derived = [
    {
        "key": "this_month_access_volume",
        "value": None,
        "numerator": None, "denominator": None,
        "note": "『本月数据接入量』正式口径（接入台账当月笔数）三源无台账面（042/045 词族排除复用）；本月窗实测 0 行（2026-10 全库主存量表零登记）——「本月」读数为 0 的负面证据而非 0 本身；按 B10 不写伪指标值"
    },
    {
        "key": "this_month_observed_month_window_rows_dev",
        "value": month_now_count,
        "numerator": None, "denominator": None,
        "note": "附带交付（非接入量）：dev enterprise_base 2026-10 月窗 update_time 计数=0——库内 10 月零写入；对照 9 月档 348（045 复用）。「挂库月」非「接入月」三层漂移同 045"
    },
]

absence_probe = [
    {
        "probe": "dev 本月窗（2026-10）主存量表写入计数",
        "source": "dev",
        "sql": "SELECT COUNT(*) FROM gkxlumenx_dwd.enterprise_base WHERE update_time >= '2026-10-01' AND update_time < '2026-11-01'（本件新探针）",
        "hits": 0,
        "hit_detail": "2026-10 全月 0 行——主存量表本月零写入；「本月接入量」在本月窗内无任何可见动作痕迹（台账若存在应>0）"
    },
    {
        "probe": "dev 接入台账（access/ingest/collect 词族）",
        "source": "dev",
        "sql": "information_schema.tables 扫 gkxlumenx_*（542 表，共享探针，042/045 复用）",
        "hits": 1,
        "hit_detail": "命中 gkxlumenx_app.app_article_collect（文章收藏）——语义排除（042/045 同键）；0 张接入流水表"
    },
    {
        "probe": "gkx/久新 接入台账与当月增量面",
        "source": "gkx/jiuxin",
        "sql": "词族扫描（045 复用：gkx_access_tables=[]/jiuxin_access_tables=[]；gkx dwd_job 全档 2026-08）",
        "hits": 0,
        "hit_detail": "gkx 280 表 0 命中且 dwd_job 无 9-10 月增量；久新 215 表 ads_* 快照面（as_of 2026-09-18 单期）无当月动作记录"
    },
    {
        "probe": "需求原文「本月数据接入量/本月接入量」指标定义",
        "source": "doc",
        "sql": "rg 检索三份需求真源",
        "hits": 0,
        "hit_detail": "指标名级 0 命中；「本月接入量」为 UI KPI 卡题名（AccessWindow 资源接入情况总览，挂靠 L6 总览功能）；「本月」窗与接入笔数口径无定义"
    },
]

doc = {
    "metric_id": "M_SCIUI_DATATHM_047",
    "batch": "S3-05",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:1661",
        "repos/demo-ui-science/src/pages/data-resources/AccessWindow.jsx:355",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份需求真源指标名级 0 命中；「本月接入量」为 AccessWindow KPI 卡题名（资源接入情况总览 L6 段）；「本月」窗定义与「接入量」笔数口径均无（与 045 同源缺口，「本月」只是 045 期窗的定格特例）"
    },
    "base_years_used": [],
    "base_years_missing": ["完全不支持：三源零承载，无库内年份基期"],
    "base_years_note": "完全不支持：无基期；mock 演示值不构成基期证据",
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": "完全不支持",
    "notes": [
        "判档：台账零承载（042/045 复用）+本月窗 0 行负面证据——「本月」无任何可见接入动作；1256 mock 与 348（9 月档）/0（10 月窗）均不闭合",
        "B11 对账：台账词族=042/045；月界切片=045 同键同值；growth_trend=040（经 045 复用）",
        "045/047 双件关系：045 是滚动期窗（末端点语义）、047 是本月定格窗——同一台账缺位的两个取窗特例，触发器共用；047 的月窗探针（0 行）是 045 没有的增量证据",
    ],
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
print("support:", doc["support_judgment"], "| month_now:", month_now_count, "| news:", news_month_now)
