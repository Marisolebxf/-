#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_052 数据资产调用量环比增速——产物生成（S3-05 L1）。

挂载 ApplicationWindow.jsx:208（assetColumns「环比」列 dataIndex growth，红绿箭头渲染）。
mock assetRanking（mockData.js:899-907）七资产 growth 15.2/22.5/8.3/12.7/-3.2/28.6/5.8。
正式口径=当期调用量 vs 上期调用量（环比）——需调用日志两期序列（调用族 041/049 同锚零承载）。
本件零新连库探针（041/049 全复用）；增量=mock 环比符号分布+与 usageCallTrend 序列自算环比的交叉核验
（mock 周序列 78200→85600 尾两点环比 +9.46% vs 资产表 growth 15.2%——mock 内部不闭合证据）。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_052_out.json")

d041 = json.load(open(os.path.join(BASE, "M_SCIUI_DATATHM_041_out.json"), encoding="utf-8"))
d049 = json.load(open(os.path.join(BASE, "M_SCIUI_DATATHM_049_out.json"), encoding="utf-8"))

# —— mock 资产环比（assetRanking，mockData.js:899-907 实抄；B5 按 growth 降序）——
mock_asset_growth = [
    ["AI训练数据集", 345000, 28.6], ["医学影像数据集", 642000, 22.5],
    ["基础研究主题库", 856000, 15.2], ["农业科技数据库", 423000, 12.7],
    ["工程设计规范库", 534000, 8.3], ["材料性能库", 298000, 5.8],
    ["环境监测数据集", 389000, -3.2],
]
growth_vals = [g for _, _, g in mock_asset_growth]
pos = sorted([g for g in growth_vals if g > 0])
neg = sorted([g for g in growth_vals if g < 0])

# —— mock 周序列自算环比（usageCallTrend calls：05-16~05-22 七点）——
trend_calls = [78200, 82100, 79500, 84300, 86800, 85200, 85600]
wow = [round((trend_calls[i] / trend_calls[i - 1] - 1) * 100, 2) for i in range(1, len(trend_calls))]
last_wow = wow[-1]

facts = {
    "dev_call_tables_reused_041": d041["facts"]["dev_call_tables"],
    "gkx_table_count": d041["facts"]["gkx_table_count"],
    "jiuxin_table_count_live": d041["facts"]["jiuxin_table_count_live"],
    "dev_sys_log_rows_reused_041": d041["facts"]["dev_sys_log_rows"],
    "dev_sys_log_admin_uri_reused_049": d049["facts"]["dev_sys_log_admin_uri_dist"],
    "ui_mock_asset_growth": mock_asset_growth,
    "ui_mock_growth_positive_sorted": pos,
    "ui_mock_growth_negative_sorted": neg,
    "ui_mock_trend_calls": trend_calls,
    "ui_mock_trend_wow_pct": wow,
    "ui_mock_trend_last_wow_pct": last_wow,
}

derived = [
    {
        "key": "asset_call_volume_mom_growth",
        "value": None,
        "numerator": None, "denominator": None,
        "note": "『数据资产调用量环比增速』正式口径（当期调用量/上期-1）需调用日志两期序列——三源零承载（041/049 复用：call 词族 0 张×3+sys_log 语义双排除）；环比是二阶指标（序列的差分），序列无则环比无；按 B10 不写伪指标值"
    },
    {
        "key": "observed_admin_call_wow_pct_oct",
        "value": None,
        "numerator": None, "denominator": None,
        "note": "附带交付尝试（管理面，语义双排除同 049）：sys_log admin 9 月/10 月请求量环比本可算——但 10 月 917 全为 OAuth token 刷新、9 月仅 8 行，环比值（+11362.5%）无业务意义且主体非需求方：不落数值，只登记『结构可算、语义不可用』（环比管线的负面边界证据）"
    },
]

absence_probe = [
    {
        "probe": "分子分母原料：调用量两期序列（调用日志）",
        "source": "dev/gkx/jiuxin",
        "sql": "041/049 全套复用（call 词族 0 张×3 + sys_log URI 99.4% OAuth + 6 用户全系统账号）",
        "hits": 0,
        "hit_detail": "环比是序列差分——序列无则环比无；调用族五件（041/049/050/052/053）统一根因；sys_log 即便算出环比（10 月 917 vs 9 月 8）也是 token 刷新节奏非业务调用量，语义不可用"
    },
    {
        "probe": "mock 内部一致性（资产表 growth vs 周序列自算环比）",
        "source": "ui",
        "sql": "usageCallTrend.calls 尾两点自算 vs assetRanking.growth（本件核验）",
        "hits": 0,
        "hit_detail": f"周序列尾两点环比 {last_wow}%（85600/85200-1——总量口径周环比）与资产表 growth（-3.2%~28.6% 资产口径）不同基不同义无法对账；资产 growth 无前期基数列（mock 未给上月 calls）——环比值不可复算，演示常量直接坐实",
    },
    {
        "probe": "需求原文「环比」指标定义",
        "source": "doc",
        "sql": "rg 检索三份需求真源",
        "hits": 0,
        "hit_detail": "「环比」指标名级 0 命中；应用视窗功能句（seq 376 排行「支持按时间…排序」/seq 381 供应方「按时间区段」）有时间维度词无环比口径；期定义（周环比/月环比？）与资产粒度（单资产/全库？）均无"
    },
]

doc = {
    "metric_id": "M_SCIUI_DATATHM_052",
    "batch": "S3-05",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:208",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:899",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "指标名级 0 命中；「环比」为 UI 表列题名（assetColumns，growth 字段红绿箭头渲染）；期定义（周/月环比）与粒度（单资产/全库）无；挂靠 seq 376 数据应用排行榜（时间维度功能词近邻）"
    },
    "base_years_used": [],
    "base_years_missing": ["完全不支持：三源零承载，无库内年份基期"],
    "base_years_note": "完全不支持：无基期；mock 演示值不构成基期证据",
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": "完全不支持",
    "notes": [
        "判档：环比是序列差分——调用量序列三源零承载（041/049 复用）则环比无源；sys_log 环比管线可算但语义不可用（token 刷新节奏）",
        "B11 对账：全套原料=041/049 同键；调用族五件统一锚",
        "mock 不闭合证据：资产表 growth 无前期基数（不可复算）+周序列自算环比（+0.47%）与任何资产 growth 不同基——演示层环比自成一套无对照",
        "B9：growth 单位 %（红涨绿跌）；wow 保留两位；admin 环比不落数值只登记边界",
    ],
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
print("wow:", wow, "| last:", last_wow)
print("pos/neg:", pos, neg)
print("support:", doc["support_judgment"])
