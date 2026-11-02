#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_P10_037 入网仪器月均使用频率（次/月）—— 薄壳校验脚本。

共享探针真源：code/_shared_s308_laneC.py
UI：InstrumentSharingNewPage.jsx:952 仪器详情 Modal + :1066 机构详情 Modal + :623 频率Top10 图。
INCUB_008 同根字段（usageFreq 机时/频率零承载）预期复判——独立留证。
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code")

SHARED = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/_snapshots/_shared_s308_laneC_out.json"
OUT = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/M_SCIUI_P10_037_out.json"


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        snap = json.load(f)
    dev = snap["dev"]
    gkx = snap["gkx"]
    jx = snap["jiuxin"]

    assert jx["jiuxin_ads_is_hits"] == []
    assert jx["jiuxin_booking_order_family"] == []
    assert gkx["gkx_instrument_family"] == []

    out = {
        "metric_id": "M_SCIUI_P10_037",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview-new/instrument-sharing-new/InstrumentSharingNewPage.jsx:952",
            "repos/demo-ui-science/src/pages/achievement-preview-new/instrument-sharing-new/InstrumentSharingNewPage.jsx:1066",
            "repos/demo-ui-science/src/pages/achievement-preview-new/instrument-sharing-new/InstrumentSharingNewPage.jsx:623",
            "repos/demo-ui-science/src/pages/achievement-preview-new/instrument-sharing-new/InstrumentSharingNewPage.jsx:194-197",
            "repos/demo-ui-science/src/pages/achievement-preview-new/instrument-sharing-new/mockData.js:245-248",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "三份说明书未出现「入网仪器月均使用频率」指标名；SRS 大型科学仪器共享.md:75「系统自动统计共享率及使用频率」/:107「自动收集用户对仪器使用后的反馈评价及使用频率」/:235「实时动态统计各服务机构仪器资源开放率、当前活跃状态及使用频率」三处上位覆盖。",
        },
        "facts": {
            "ui_mount": "三挂载位：:952 仪器详情 Modal { label: 使用频率, value: `${activeInstrument.usageFreq} 次/月` }；:1066 机构详情 Modal { label: 使用频率, value: `${activeOrg.usageFreq} 次/月` }；:623 使用频率 Top10 图（CHART_METRICS.usageFreq metricId=M_IS_USAGE_FREQ lineage 源表 ads_is_instrument_usage）",
            "ui_compute_chain": ":194-197 freqTop = [...filteredInstruments].sort((a,b)=>b.usageFreq-a.usageFreq).slice(0,10)；:332-359 freqOption 条形图（tooltip 双值：使用频率 + 使用评价 rating）",
            "ui_mock": "mockData.js INSTRUMENTS 32 台仪器 usageFreq 38-260 次/月（:109 起 INS-0001 96/INS-0003 210/INS-0012 260……）；INSTITUTIONS 14 机构 usageFreq 65-260——ui_demo_fallback 演示值",
            "ui_lineage_note": "CHART_METRICS.usageFreq lineage: 口径：仪器月均使用频次（次/月）与使用评价（5 分制）。源表：ads_is_instrument_usage；更新频率：T+1——UI 侧口径契约同 P10_040 指定源表族",
            "probe_jiuxin_ads_is": jx["jiuxin_ads_is_hits"],
            "probe_jiuxin_booking_order": jx["jiuxin_booking_order_family"],
            "probe_dev_usage_cols": dev["dev_instrument_family_hits"],
            "probe_gkx_instrument_family": gkx["gkx_instrument_family"],
            "probe_dev_table_total": dev["dev_table_total"],
            "probe_gkx_table_count": gkx["gkx_table_count"],
            "probe_jiuxin_table_count_live": jx["jiuxin_table_count_live"],
            "family_note": "INCUB_008 入网仪器月均使用频率（S3-07 批同根因件，机时/频率零承载已证）预期复判；本件独立留证。SOFTSCI_015 热门仪器利用率排行同字段族。",
        },
        "derived": [
            {
                "name": "instrument_monthly_avg_usage_freq",
                "value": None,
                "note": "负结论 null 登记：使用频率的承载源表 ads_is_instrument_usage（UI lineage 指定）与等价预约/机时流水三源零承载；dev usage 列命中仅为 config.group_capacity.usage（容量配额语义）；gkx dwd_medical_device 无 usage 列。频率=流水聚合（Σ月内预约完成单/台），无流水即无频率。",
            },
        ],
        "absence_probe": [
            {
                "probe": "jiuxin 218 表（SHOW TABLES 实数）ads_is_instrument_usage 指定源表 + order/book/reserv 预约流水族",
                "source": "jiuxin",
                "sql": "SHOW TABLES LIKE 'ads_is%' = 0；SHOW TABLES REGEXP order|book|reserv = 0（快照 jiuxin_ads_is_hits/jiuxin_booking_order_family 均空）",
                "hits": 0,
            },
            {
                "probe": "dev 17 schema（542 表）usage/freq/machine_hour 列 + 预约订单表",
                "source": "dev",
                "sql": "information_schema.columns 词族扫描（快照 dev_instrument_family_hits：usage 命中仅 config.group_capacity/tenant_capacity 容量配额语义；freq 命中 chain_hotspot.news_freq_score 资讯热度/policy_subscription.push_frequency 推送频率——均非仪器使用）",
                "hits": 0,
                "note": "bi.test_order 为积木报表测试单语义（order_name/order_sign_date），非仪器预约",
            },
            {
                "probe": "gkx 280 表仪器使用流水/机时列",
                "source": "gkx",
                "sql": "information_schema 词族扫描（快照 gkx_instrument_family=[]）；dwd_medical_device 15 列无 usage/机时/预约列",
                "hits": 0,
            },
        ],
        "support_judgment": "完全不支持",
        "notes": [
            "判档理由：月均使用频率=Σ月内预约完成单÷台（或机时折算），承载要求是预约/订单流水表——UI lineage 指定源表 ads_is_instrument_usage 在久新 218 表 0 实存（P10_040 同族 ads_is_* 缺失）；dev 542 表 usage/freq/机时列命中全为容量配额/资讯热度/推送频率语义；jiuxin order/book/reserv 词族 0 命中；gkx 280 表仪器族 0（dwd_medical_device 注册库无 usage 列）。无流水即无频率，判完全不支持——与 S3-07 批 INCUB_008 同根因复判一致，本件独立留证。",
            "mock 32 仪器 38-260 次/月 + 14 机构 65-260 次/月为演示值（ui_demo_fallback 披露）；需规背景（3565 行）仅有有效订单 1,336 个总量数，无单机频率口径。",
            "修复路径：共享平台 ADS 表族接入（ads_is_order 预约单 + ads_is_instrument_usage 频率表）→ 完全直接支持；仅接入 ads_is_order 也可转换聚合（月度单量÷台数）→ 完全转换支持。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021", "2022", "2023", "2024", "2025", "2026"],
        "base_years_note": "使用频率为月度滚动读数（月均口径）；需规背景仅 2020-12 底有效订单总量 1,336 个（单时点）。库内无任何月份承载。若接入订单流水可建月度序列，以接入月为基期。",
        "ctx_refs": {
            "note": "正文引用型数字登记",
            "refs": sorted(["38", "260", "96", "210", "32", "14", "65", "1336", "1,336", "542", "280", "218", "10", "2020"]),
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 完全不支持 | ads_is:", jx["jiuxin_ads_is_hits"], "| booking:", jx["jiuxin_booking_order_family"])


if __name__ == "__main__":
    main()
