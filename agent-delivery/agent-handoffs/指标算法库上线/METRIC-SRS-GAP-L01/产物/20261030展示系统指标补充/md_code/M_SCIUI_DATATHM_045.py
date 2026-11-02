#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_045 本期数据接入量——三源探针+产物生成（S3-05 L1）。

挂载 AccessHistorySituation.jsx:84「历史接入量」bar 末端点（本期=labels 末月 3360）。
040 已证 dev enterprise_growth_trend 0 行（期际序列零承载）；042 已证台账缺位（词族三源排除）。
本件补期界增量探针：dev live 主存量表挂库月切片（update_time 分月，列名 update_time 非 updated_at）。
产物键与 040/042 零漂移（B11）：growth 0 行复用、存量 186335492 复用、月界切片新键。
"""
import json
import os
import sys

import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_045_out.json")
sys.path.insert(0, BASE)
import _gkxdb
from _gkxdb import gkx

# —— 复用 040/042 本批产物（B11 零漂移；勿重跑已落盘探针）——
d040 = json.load(open(os.path.join(BASE, "M_SCIUI_DATATHM_040_out.json"), encoding="utf-8"))
d042 = json.load(open(os.path.join(BASE, "M_SCIUI_DATATHM_042_out.json"), encoding="utf-8"))

growth_rows = d040["facts"]["dev_growth_trend_rows"]  # 0（040 实测）
cum_proxy = d042["derived"][0]["value"]  # 186335492.0（042 存量代理）

# —— 本件新探针①：dev live（10.50.11.76）主存量表挂库月切片（update_time 分月计数）——
conn = pymysql.connect(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
                       charset="utf8mb4", autocommit=True,
                       cursorclass=pymysql.cursors.DictCursor)
try:
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) c FROM gkxlumenx_dwd.enterprise_base")
        ent_total_now = cur.fetchone()["c"]
        cur.execute(
            "SELECT DATE_FORMAT(update_time,'%Y-%m') ym, COUNT(*) c "
            "FROM gkxlumenx_dwd.enterprise_base GROUP BY ym ORDER BY ym")
        month_dist_now = [[r["ym"], r["c"]] for r in cur.fetchall()]
finally:
    conn.close()

# —— 本件新探针②：gkx dwd_job 挂库月分布（280 表内唯一带 update_time 的高频更新表，042 计数 10）——
gcur = gkx()
gcur.execute("SELECT COUNT(*) FROM gkx.dwd_job")
gkx_job_window = gcur.fetchone()[0]
# 列名 updated_time（gkx 供应商表命名）；日期列含 '0000-00-00' 零值需过滤（只读直查）
gcur.execute(
    "SELECT DATE_FORMAT(updated_time,'%Y-%m') ym, COUNT(*) c FROM gkx.dwd_job "
    "WHERE updated_time > '1971-01-01' GROUP BY ym ORDER BY ym")
gkx_job_month_dist = [list(r) for r in gcur.fetchall()]

# —— UI mock「本期」末端点（口径边界证据，不作数据）——
mock_labels = d042["facts"]["ui_mock_trend_labels"]
mock_volume = d042["facts"]["ui_mock_trend_access_volume"]
mock_current = mock_volume[-1]

facts = {
    "dev_table_total": d042["facts"]["dev_table_total"],
    "dev_access_registry_tables": d042["facts"]["dev_access_registry_tables"],
    "gkx_table_count": d042["facts"]["gkx_table_count"],
    "jiuxin_table_count_live": d042["facts"]["jiuxin_table_count_live"],
    "dev_enterprise_base_rows": ent_total_now,
    "dev_enterprise_month_slice_now": month_dist_now,
    "dev_growth_trend_rows": growth_rows,
    "gkx_dwd_job_rows": gkx_job_window,
    "gkx_dwd_job_month_dist": gkx_job_month_dist,
    "cumulative_proxy_reused_042": cum_proxy,
    "ui_mock_trend_labels": mock_labels,
    "ui_mock_trend_access_volume": mock_volume,
    "ui_mock_current_period_endpoint": mock_current,
    "ui_mock_prev_endpoint": mock_volume[-2],
    "ui_mock_period_over_period_delta": mock_current - mock_volume[-2],
}

derived = [
    {
        "key": "current_period_access_volume_proxy_dev_month_slice",
        "value": month_dist_now[-1][1] if month_dist_now else None,
        "numerator": None, "denominator": None,
        "note": "本期增量代理=dev enterprise_base 挂库月切片（update_time 月界最后一档计数）——「挂库月」非「接入月」：快照表全量重挂即漂移，仅作期界两侧存量差参考；语义披露：库内数据资产月界登记，非接入动作增量"
    },
    {
        "key": "current_period_access_volume",
        "value": None,
        "numerator": None, "denominator": None,
        "note": "『本期数据接入量』正式口径（接入台账当期笔数；本期=自然月，窗随日期滚动）三源无台账面（042 词族排除复用）；序列侧 growth_trend 0 行（040 复用）；按 B10 不写伪指标值"
    },
]

absence_probe = [
    {
        "probe": "dev 逐期接入序列（本期=末端点）",
        "source": "dev",
        "sql": "SELECT COUNT(*) FROM gkxlumenx_enterprise.enterprise_growth_trend（040 实测）",
        "hits": 0,
        "hit_detail": "enterprise_growth_trend 0 行——期际序列零承载（040 同锚）；本期值无序列可取末端点"
    },
    {
        "probe": "dev 接入台账（access_log/ingest/collect 词族）",
        "source": "dev",
        "sql": "information_schema.tables 扫 gkxlumenx_*（542 表，共享探针，042 复用）",
        "hits": 1,
        "hit_detail": "命中 gkxlumenx_app.app_article_collect（文章收藏-用户行为表）——语义排除（042 同键）；0 张接入流水表"
    },
    {
        "probe": "gkx 接入台账/期际序列（access/ingest 词族+growth/trend 表名）",
        "source": "gkx",
        "sql": "词族扫描（共享探针 gkx_access_tables=[]；growth/trend 表名 0 命中）",
        "hits": 0,
        "hit_detail": "280 表 0 命中；dwd_job 挂库月分布可查但 10 行样本无期界语义"
    },
    {
        "probe": "久新接入台账/期际序列（access/ingest 词族+growth/trend 表名）",
        "source": "jiuxin",
        "sql": "词族扫描（共享探针 jiuxin_access_tables=[]，215 表 live）",
        "hits": 0,
        "hit_detail": "0 命中——ads_* 全部分析结果面，快照管理无逐笔接入记录（042 同证）"
    },
    {
        "probe": "需求原文「本期数据接入量」指标定义",
        "source": "doc",
        "sql": "rg 检索三份需求真源",
        "hits": 0,
        "hit_detail": "三份需求说明书未出现「本期数据接入量」（指标名级 0 命中）；挂靠 seq 362（历史资源接入情况总览——「动态跟踪接入量…的历史变化」功能词在，本期口径无定义）；seq 361/360 亦无"
    },
]

doc = {
    "metric_id": "M_SCIUI_DATATHM_045",
    "batch": "S3-05",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/components/AccessHistorySituation.jsx:84",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:1427",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份需求真源指标名级 0 命中；「历史接入量」为 UI series 图例（:84），本期=序列末端点（mock 末月 3360）；挂靠 seq 362 历史资源接入情况总览——功能词「动态跟踪接入量…的历史变化」在，「本期」窗定义（自然月/周/滚动窗）无"
    },
    "base_years_used": [],
    "base_years_missing": ["完全不支持：三源零承载，无库内年份基期"],
    "base_years_note": "完全不支持：无基期；mock 演示值不构成基期证据",
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": "完全不支持",
    "notes": [
        "判档：正式口径（台账当期笔数）三源零承载+期际序列 0 行——「本期」末端点无序列可挂；月界切片是「挂库月」非「接入月」，语义漂移不补判档",
        "B11 对账：cumulative_proxy 186335492 复用 042 同值；growth_trend 0 行复用 040；台账词族三源排除复用 042/共享探针",
        "040/042/045 三件同根：040 序列（期际变化）、042 存量（累计）、045 增量（当期）——台账缺位一因三果，触发器共用（台账落地即三件全升）",
    ],
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
print("support:", doc["support_judgment"], "| proxy:", derived[0]["value"], "| mock current:", mock_current)
