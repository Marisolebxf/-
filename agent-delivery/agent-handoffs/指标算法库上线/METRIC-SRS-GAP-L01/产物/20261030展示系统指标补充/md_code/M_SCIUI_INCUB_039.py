#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INCUB_039 热门仪器利用率排行 —— 薄壳校验脚本（负结论件）。

UI：InstrumentSharingPage.jsx:1442 服务统计窗「热门仪器利用率排行」横向条形图；
buildUsageRanking(:212) 对 instruments 按 usageRate 降序取 Top5——usageRate（机时
利用率）根字段零承载（INCUB_008 S3-07 已证）。本件 INCUB 清单行 594 独立留证：
rg 实查消费点（buildUsageRanking/排序键/条形 option/点击联动）+ 三源探针复核。
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code")

SHARED = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/_snapshots/_shared_s308_lane_a_out.json"
OUT = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/M_SCIUI_INCUB_039_out.json"


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        snap = json.load(f)

    dev = snap["dev"]
    gkx = snap["gkx"]
    jx = snap["jiuxin"]
    assert dev["table_total"] == 542 and gkx["table_count"] == 280
    assert jx["table_count_live"] == 218

    out = {
        "metric_id": "M_SCIUI_INCUB_039",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:1442",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:212",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:1453",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "「热门仪器利用率排行」指标名三份说明书未出现；上位叶 SRS 1.1.1.1.4.6.4.1.1 使用评价与频次统计（自动收集使用频率）；INCUB_008（S3-07 usageRate 根字段件）同页同根因。",
        },
        "facts": {
            "ui_mount": "InstrumentSharingPage.jsx:1442 服务统计窗「热门仪器利用率排行」横向条形图（SoftChartFrame + buildHorizontalBarOption(usageRanking, \"％\")）",
            "ui_ranking_fn": "buildUsageRanking（InstrumentSharingPage.jsx:212-221）：[...items].sort((l,r)=>r.usageRate-l.usageRate).slice(0,5)——usageRate 降序 Top5",
            "ui_click_link": "InstrumentSharingPage.jsx:1456 点击条形联动选中仪器（params.name 匹配）刷新统计详情（INCUB_057 件消费点）",
            "ui_mock_top5": "mock 4 台仪器 usageRate 88/76/64/52（instrumentSharingMock.js:242/263/284/305）→ mock 排行 4 项——ui_demo_fallback 演示值，不参与支持度结论",
            "ui_root_field": "usageRate（%）：与 INCUB_007（使用热度分档）/INCUB_008（单台使用率）/INCUB_019（全市均值）同一根字段",
            "dev_table_total": dev["table_total"],
            "dev_usage_word_note": "dev usage/utiliz/machine_hour 词族（表名+列名双扫）0 命中（_probe_s307_l2_out.json：config.group_capacity.usage/tenant_capacity.usage 为容量配置语义非机时）",
            "gkx_table_count": gkx["table_count"],
            "gkx_usage_note": "gkx 280 表 usage 词族命中仅 dwd_drug_profile.indications_and_usage（药品适应症语义）；dwd_medical_device 15 列断言无 usage/utiliz 列（S3-07 l2b 快照）",
            "jiuxin_table_count_live": jx["table_count_live"],
            "jiuxin_usage_note": "久新 218 表 usage/utiliz/machine_hour 词族 0 命中；hotspot_score 族为学术研究热度语义（INCUB_007 已排除）",
            "named_in_srs": False,
        },
        "derived": [
            {
                "name": "instrument_usage_rate_ranking_top5",
                "value": None,
                "numerator": None,
                "denominator": None,
                "note": "排行 = 单台机时利用率降序 Top5。usageRate 根字段（年有效机时/年可用机时）三源 0 命中 → 排行不可构建，负结论 null 登记",
            },
        ],
        "absence_probe": [
            {"probe": "dev usage/utiliz/machine_hour 词族（542 表名+列名双扫）",
             "source": "dev", "sql": "information_schema 双扫（_probe_s307_l2_out.json + _shared_s308_lane_a 复核）",
             "hits": 0, "note": "词族命中列均为容量配置/药品适应症语义，机时零承载"},
            {"probe": "gkx usage 词族（280 表 + dwd_medical_device 15 列断言）",
             "source": "gkx", "sql": "information_schema 扫描 + 15 列逐一核对",
             "hits": 0, "note": "唯一设备主表为静态注册台账（10,000 行）无运行态列"},
            {"probe": "久新 usage/utiliz/machine_hour 词族（SHOW TABLES 实数 218 表）",
             "source": "jiuxin", "sql": "SHOW TABLES + 列扫描",
             "hits": 0, "note": "ads_* 全系科技要素分析面，无设备运行面"},
        ],
        "support_judgment": "完全不支持",
        "notes": [
            "判档理由：排行的排序键是单台 usageRate（机时利用率），根字段三源零承载（词族双扫 0 命中 + 医疗器械 15 列断言）——排序无键即排行空转；台账（排行主体）三源亦无表。",
            "同族关系：INCUB_008（usageRate 根字段件，S3-07 判完全不支持）为本件上位证；INCUB_007（热度分档同字段）/INCUB_019（全市均值同字段）同根因独立留证；本件为「排行面」粒度。",
            "科技部考核口径对应物「仪器运行机时」（权重 15 分）——机时日志属设备管理系统，外部数据。",
            "mock Top5 实为 Top4（mock 仅 4 台仪器 88/76/64/52）——演示态自证仪器池规模不足，不作数据证据。",
            "升档路径：机时日志接入 → 单台利用率可算 → 排行即 sort 直出 → 完全转换支持；台账+利用率结果面直供 → 完全直接支持。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021-2026"],
        "base_years_note": "利用率为年度统计量（年有效机时/年可用机时）；三源无承载无基期可言；mock 无年度序列。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted(
            ["88", "76", "64", "52", "5", "4", "15", "10000", "10,000", "542", "280", "218", "0", "212", "221"])},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 完全不支持 | usageRate 根字段三源 0 命中，排行无键")


if __name__ == "__main__":
    main()
