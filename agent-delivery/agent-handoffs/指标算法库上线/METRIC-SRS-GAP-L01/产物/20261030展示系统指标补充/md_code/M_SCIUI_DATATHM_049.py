#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_049 需求方月活跃天数——三源探针+产物生成（S3-05 L1）。

挂载 ApplicationWindow.jsx:233（demanderColumns「活跃天数」列 dataIndex activeDays）。
mock demanderUsageStats（mockData.js:978-985）八需求方 activeDays 28/26/24/25/22/20/21/27。
正式口径=需求方×月窗内 DISTINCT 调用日期数——需调用日志（create_by×DATE(create_time)）。
三源调用日志已排除（041 复用：call/invoke/api/reques 词族 0 张、sys_log 为管理 OAuth 面）。
本件新探针=dev sys_log 用户维度聚合（create_by × COUNT(DISTINCT DATE)）——
041 只做 URI 排除，本件补 per-user 活跃天数实测（管理面语义排除+附带交付双轨）。
"""
import json
import os

import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_049_out.json")

d041 = json.load(open(os.path.join(BASE, "M_SCIUI_DATATHM_041_out.json"), encoding="utf-8"))

conn = pymysql.connect(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
                       charset="utf8mb4", autocommit=True,
                       cursorclass=pymysql.cursors.DictCursor)
try:
    with conn.cursor() as cur:
        # 本件新探针①：sys_log 全期 per-user 活跃天数（DISTINCT DATE 聚合）
        cur.execute(
            "SELECT create_by, COUNT(DISTINCT DATE(create_time)) ad, COUNT(*) reqs, "
            "MIN(DATE(create_time)) d0, MAX(DATE(create_time)) d1 "
            "FROM gkxlumenx.sys_log GROUP BY create_by ORDER BY ad DESC, create_by")
        user_days_all = [[r["create_by"], r["ad"], r["reqs"], str(r["d0"]), str(r["d1"])]
                         for r in cur.fetchall()]
        # 本件新探针②：单月窗（2026-10 闭月）per-user 活跃天数（正式口径的月窗形态实测）
        cur.execute(
            "SELECT create_by, COUNT(DISTINCT DATE(create_time)) ad, COUNT(*) reqs "
            "FROM gkxlumenx.sys_log "
            "WHERE create_time >= '2026-10-01' AND create_time < '2026-11-01' "
            "GROUP BY create_by ORDER BY ad DESC, create_by")
        user_days_oct = [[r["create_by"], r["ad"], r["reqs"]] for r in cur.fetchall()]
        # 本件新探针③：admin 的 URI 构成（语义排除核心证据：是否全 OAuth token）
        cur.execute(
            "SELECT request_uri, COUNT(*) c FROM gkxlumenx.sys_log "
            "WHERE create_by='admin' GROUP BY request_uri ORDER BY c DESC LIMIT 5")
        admin_uri = [[r["request_uri"], r["c"]] for r in cur.fetchall()]
finally:
    conn.close()

ui_mock_active_days = [
    ["研发中心A", 28, 9143], ["实验室B", 26, 7269], ["企业C", 24, 6500],
    ["研究所D", 25, 5360], ["高校E", 22, 4455], ["项目组F", 20, 4350],
    ["创新工作室G", 21, 3619], ["临床中心H", 27, 4148],
]  # mockData.js:978-985 实抄（名称/activeDays/avgDaily；B5 按 activeDays 降序）

facts = {
    "dev_table_total": d041["facts"]["dev_table_total"],
    "dev_call_tables_reused_041": d041["facts"]["dev_call_tables"],
    "gkx_table_count": d041["facts"]["gkx_table_count"],
    "jiuxin_table_count_live": d041["facts"]["jiuxin_table_count_live"],
    "dev_sys_log_rows_reused_041": d041["facts"]["dev_sys_log_rows"],
    "dev_sys_log_user_days_all": user_days_all,
    "dev_sys_log_user_days_oct": user_days_oct,
    "dev_sys_log_admin_uri_dist": admin_uri,
    "ui_mock_demander_active_days": ui_mock_active_days,
    "ui_mock_active_days_max": 28,
    "ui_mock_active_days_min": 20,
    "ui_mock_month_days_assumed": 30,
}

derived = [
    {
        "key": "demander_monthly_active_days",
        "value": None,
        "numerator": None, "denominator": None,
        "note": "『需求方月活跃天数』正式口径（需求方×月窗 DISTINCT 调用日期）需业务调用日志——三源零承载（041 复用：call 词族 0 张）；sys_log 是管理面 OAuth 日志非业务调用（语义排除）；按 B10 不写伪指标值"
    },
    {
        "key": "admin_active_days_observed_oct",
        "value": user_days_oct[0][1] if user_days_oct else 0,
        "numerator": None, "denominator": None,
        "note": "附带交付（非需求方活跃）：sys_log 用户 admin 在 2026-10 闭月窗活跃 9 天（917 请求）——但 URI 构成 /oauth2/token 100%（1029/1037 全期），是管理系统 token 刷新日志非数据资源调用；admin≠需求方（系统管理员），语义双排除"
    },
]

absence_probe = [
    {
        "probe": "dev 业务调用日志（需求方×时间戳×资源）",
        "source": "dev",
        "sql": "call/invoke/api/reques 词族扫描（041 复用）+ sys_log 语义核对（本件新探针③）",
        "hits": 0,
        "hit_detail": "词族 0 张（041 同锚）；唯一时序面 sys_log（1,060 行）URI 构成 /oauth2/token 1029+/route 8——管理面 OAuth 刷新日志，无业务资源调用记录；create_by 6 用户全为系统账号（admin/admin1/demo/gkx/test/x），无需求方主体",
    },
    {
        "probe": "gkx 调用日志面",
        "source": "gkx",
        "sql": "词族扫描（041 复用 gkx_call_tables=[]）",
        "hits": 0,
        "hit_detail": "280 表 0 命中——供应商要素库无调用流水（041 同证）"
    },
    {
        "probe": "久新调用日志面",
        "source": "jiuxin",
        "sql": "词族扫描（041 复用 jiuxin_call_tables=[]，215 表 live）",
        "hits": 0,
        "hit_detail": "ads_* 分析结果面快照单期（as_of 2026-09-18），无逐笔调用（041 同证）"
    },
    {
        "probe": "需求原文「活跃天数/需求方活跃」指标定义",
        "source": "doc",
        "sql": "rg 检索三份需求真源（应用视窗 seq 392-395 需求方调用数据详情段）",
        "hits": 1,
        "hit_detail": "seq 393 累计调用次数统计（「全面统计每个需求方的数据资源累计调用次数」）+seq 394 调用行为分布可视化（「各需求方在不同时间段的数据调用分布状况」）——功能词近邻；「活跃天数」指标名级 0 命中（mock 表列题名）；月窗定义无（UI Progress 按 /30 折算暗示月窗但非定义）"
    },
]

doc = {
    "metric_id": "M_SCIUI_DATATHM_049",
    "batch": "S3-05",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:233",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:978",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "指标名级 0 命中；「活跃天数」为 mock 表列题名（ApplicationWindow demanderColumns）；最近功能叶 seq 393/394（需求方累计调用/行为分布——「不同时间段的数据调用分布」语义近邻）；月窗定义无（050 的 /30 折算暗示 30 天月）"
    },
    "base_years_used": [],
    "base_years_missing": ["完全不支持：三源零承载，无库内年份基期"],
    "base_years_note": "完全不支持：无基期；mock 演示值不构成基期证据",
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": "完全不支持",
    "notes": [
        "判档：业务调用日志三源零承载（041 复用同锚）——需求方×日期×资源三元组无源；sys_log 虽有 create_by×DISTINCT DATE 结构但语义双排除（管理 OAuth 面+系统账号非需求方）",
        "B11 对账：call 词族/sys_log 行数/URI 分布=041 同键（本件补 per-user 维度为增量键）；月窗探针窗常量与 047 同期（2026-10 闭月）",
        "050 联动：本件 activeDays 是 050 的分子（activeDays/30）——两件同根同触发器（调用日志落地双升）；mock 值 20-28 天与 sys_log 实测 9 天（10 月窗）不闭合",
        "B9：mock avgDaily 列（9143/7269/…）是日均调用——与活跃天数不同量纲，仅登记不作活跃证据",
    ],
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
print("user_days_all:", user_days_all[:3])
print("user_days_oct:", user_days_oct)
print("admin uri:", admin_uri[:3])
print("support:", doc["support_judgment"])
