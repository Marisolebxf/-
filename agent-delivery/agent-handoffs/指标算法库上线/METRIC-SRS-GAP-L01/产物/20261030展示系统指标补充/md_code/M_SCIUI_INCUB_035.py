#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INCUB_035 仪器月度预约趋势（INCUB 挂载件）—— 薄壳校验脚本（负结论件）。

UI：InstrumentSharingPage.jsx:1375 服务统计窗「月度预约趋势」折线（同位 SOFTSCI_010，
S3-07 批已判完全不支持）；本件为 INCUB 清单行 590 的独立留证（同根因、独立产物）。
三源探针：dev 542 表 reserv/booking/appoint 词族 0 命中（含列级 service_count_like=0）；
gkx 280 表 0 命中；久新 218 表（SHOW TABLES 实数）0 命中。
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code")

SHARED = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/_snapshots/_shared_s308_lane_a_out.json"
OUT = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/M_SCIUI_INCUB_035_out.json"


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        snap = json.load(f)

    dev = snap["dev"]
    gkx = snap["gkx"]
    jx = snap["jiuxin"]
    assert dev["table_total"] == 542 and gkx["table_count"] == 280
    assert jx["table_count_live"] == 218
    assert dev["word_reserv"] == []

    out = {
        "metric_id": "M_SCIUI_INCUB_035",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:1375",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:180",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/mock/instrumentSharingMock.js:111",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "「仪器月度预约趋势」指标名三份说明书未出现；上位叶 SRS 1.1.1.1.4.6.4.2 预约订单追踪与排期调度（订单进展管理功能分句）；主需求 3565 行「有效订单数 1336 个」为深圳平台 2020 年末背景快照。",
        },
        "facts": {
            "ui_mount": "InstrumentSharingPage.jsx:1375 服务统计窗四宫格之首「月度预约趋势」折线（SoftChartFrame metric=reservationTotal unit=单 badge=服务需求）",
            "ui_scale_fn": "buildScaledMonthlyReservations（InstrumentSharingPage.jsx:180）按筛选集 reservationCount 合计占比缩放 mock 6 点基线，下限 1",
            "ui_mock_baseline": "instrumentSharingMock.js:111-118 月度 6 点（1-6 月 82/94/111/123/138/151，合计 699 单）+ instruments[].reservationCount 字段（128/156/89/42 等）——ui_demo_fallback 演示值，不参与支持度结论",
            "ui_sibling_metric": "同位 SOFTSCI_010（S3-07 批，判完全不支持）——本件为 INCUB 清单行 590 同语义独立留证",
            "dev_table_total": dev["table_total"],
            "dev_reserv_word_tables": dev["word_reserv"],
            "dev_service_count_like_columns": dev["service_count_like_columns"],
            "gkx_table_count": gkx["table_count"],
            "gkx_reserv_word_tables": gkx["word_reserv"],
            "jiuxin_table_count_live": jx["table_count_live"],
            "jiuxin_reserv_note": "久新 218 表 reserv/booking/appoint 词族 0 命中（_probe_s307_l2_out.json jiuxin.table_name_hits 无 reservation 族）",
            "three_source_reservation_table_hits": {"dev": 0, "gkx": 0, "jiuxin": 0},
            "ui_mock_monthly_reservations_6points_sum": 699,
            "named_in_srs": False,
        },
        "derived": [
            {
                "name": "monthly_reservation_trend",
                "value": None,
                "numerator": None,
                "denominator": None,
                "note": "月度预约趋势 = 按月聚合预约订单流水。流水表三源 0 命中（dev 542/gkx 280/久新 218 词族双扫）→ 不可构建，负结论 null 登记",
            },
        ],
        "absence_probe": [
            {"probe": "dev reserv/booking/appoint 词族（表名 542 表 + 列级 service_count/service_total/service_item 三式）",
             "source": "dev", "sql": "information_schema 表名+列名双扫（_shared_s308_lane_a.py 快照）",
             "hits": 0, "note": "word_reserv=[] 且 service_count_like_columns=[]——BI test_order 0 行与 pay 订单表 0 行均为电商语义非预约"},
            {"probe": "gkx reserv/booking/appoint 词族（280 表）",
             "source": "gkx", "sql": "information_schema.tables 表名扫描（快照）", "hits": 0},
            {"probe": "久新 reserv/booking/appoint 词族（SHOW TABLES 实数 218 表）",
             "source": "jiuxin", "sql": "SHOW TABLES 词族过滤（S3-07 l2 快照 + 本批 live 复核 218 表实数）",
             "hits": 0, "note": "ads_* 全系科技要素分析面，无预约订单流"},
        ],
        "support_judgment": "完全不支持",
        "notes": [
            "判档理由：月度预约趋势的分母材料是预约订单流水（每单一条：仪器/用户/提交时间/服务时间），三源表名+列名双扫 0 命中；gkx 唯一设备主表 dwd_medical_device（10,000 行 15 列）纯静态注册台账无预约列（S3-07 l2b 快照列断言）。",
            "同根复判：与 SOFTSCI_010（S3-07）同 UI 位同根因，派单 §二路 A 表明示「SOFTSCI_010 同根因（预约流水零承载）预期复判；独立留证」——本件独立跑探针独立落产物，结论复判一致。",
            "UI 缩放逻辑依赖每台仪器的 reservationCount 字段（流水派生列），该字段三源同样零承载——流水表与仪器级汇总列须分开验收（前者是根）。",
            "mock 6 点合计 699 单为演示值（ui_demo_fallback 披露）；SRS 附录 A「有效订单数 1336 个」为深圳平台 2020 年末快照，属外部运营数据非库内承载。",
            "升档路径：预约订单系统接入（流水表落库）→ 完全直接支持（月度聚合直查）。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021-2026"],
        "base_years_note": "预约趋势为月度流水聚合时序；三源无流水即无任何可观测年；mock 月份（1-6 月）为标签字符串非真实年月。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted(
            ["699", "82", "94", "111", "123", "138", "151", "128", "156", "89", "42", "1336",
             "542", "280", "218", "0", "10000", "10,000", "15", "1", "6"])},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 完全不支持 | reserv hits dev/gkx/jiuxin = 0/0/0")


if __name__ == "__main__":
    main()
