#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INCUB_057 仪器预约量（次）—— 薄壳校验脚本（负结论件）。

UI：InstrumentSharingPage.jsx:902 选中仪器统计详情「预约量」= `${reservationCount} 单`。
reservationCount 为预约流水派生运营字段——三源零承载（独立断言 + 探针复用）。
与 INCUB_035（月度趋势）同字段族不同粒度（单台仪器级 vs 全平台月度），独立留证。
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code")

SHARED = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/_snapshots/_shared_s308_lane_a_out.json"
OUT = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/M_SCIUI_INCUB_057_out.json"


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        snap = json.load(f)

    dev = snap["dev"]
    gkx = snap["gkx"]
    jx = snap["jiuxin"]
    assert dev["table_total"] == 542 and gkx["table_count"] == 280
    assert jx["table_count_live"] == 218
    assert dev["word_reserv"] == []
    assert dev["service_count_like_columns"] == []

    out = {
        "metric_id": "M_SCIUI_INCUB_057",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:902",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/mock/instrumentSharingMock.js:243",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "「仪器预约量」指标名三份说明书未出现；上位叶 SRS 1.1.1.1.4.6.4.1.1 使用评价与频次统计 + 1.1.1.1.4.6.4.2 预约订单追踪；主需求 3565 行「有效订单数 1336 个」为深圳平台 2020 年末背景快照。",
        },
        "facts": {
            "ui_mount": "InstrumentSharingPage.jsx:902 服务统计窗选中仪器统计详情 statisticRows「预约量：${formatNumber(instrument.reservationCount)} 单」",
            "ui_field": "reservationCount（每台仪器的累计预约单数）",
            "ui_sibling_consumers": "同字段另驱动 KPI「预约申请」合计（:1511 起）与月度预约趋势缩放（buildScaledMonthlyReservations :180，INCUB_035 件）",
            "ui_mock_note": "mock instruments[].reservationCount 4 值 128/156/89/42（instrumentSharingMock.js:243/264/285/306）——ui_demo_fallback 演示值，不参与支持度结论",
            "dev_table_total": dev["table_total"],
            "dev_reserv_word_tables": dev["word_reserv"],
            "dev_service_count_like_columns": dev["service_count_like_columns"],
            "gkx_table_count": gkx["table_count"],
            "gkx_reserv_word_tables": gkx["word_reserv"],
            "jiuxin_table_count_live": jx["table_count_live"],
            "jiuxin_reserv_note": "久新 218 表（SHOW TABLES 实数）reserv/booking/appoint 词族 0 命中",
            "three_source_reservation_table_hits": {"dev": 0, "gkx": 0, "jiuxin": 0},
            "named_in_srs": False,
        },
        "derived": [
            {
                "name": "instrument_reservation_count",
                "value": None,
                "numerator": None,
                "denominator": None,
                "note": "仪器预约量 = COUNT(预约订单 WHERE instrument_id=X)。订单流水表三源 0 命中 → 单台计数不可构建，负结论 null 登记",
            },
        ],
        "absence_probe": [
            {"probe": "dev reserv/booking/appoint 词族（542 表名 + service_count/total/item 列级三式）",
             "source": "dev", "sql": "information_schema 表名+列名双扫（_shared_s308_lane_a.py 快照）",
             "hits": 0, "note": "BI test_order 0 行与 pay 订单 0 行均为电商语义"},
            {"probe": "gkx reserv 词族（280 表）+ dwd_medical_device 15 列断言",
             "source": "gkx", "sql": "information_schema 表名扫描 + S3-07 l2b 快照 15 列核对",
             "hits": 0, "note": "静态注册台账无 reservationCount 类列"},
            {"probe": "久新 reserv 词族（SHOW TABLES 实数 218 表）",
             "source": "jiuxin", "sql": "SHOW TABLES 词族过滤", "hits": 0},
        ],
        "support_judgment": "完全不支持",
        "notes": [
            "判档理由：UI「预约量」是仪器级 reservationCount 字段直读——该字段是预约流水派生列，流水表三源 0 命中则派生列无从谈起；gkx 医疗器械代理面 15 列无预约列。",
            "同族关系：与 INCUB_035（月度趋势，全平台月度聚合）同 reservationCount 字段族不同粒度，与 SOFTSCI_010（S3-07）同根因——本件独立留证。",
            "科技部考核口径对应物是「有效订单数」（SRS 附录 A 1,336 个，深圳平台 2020 年末快照）——订单数据属共享平台运营系统，外部数据。",
            "升档路径：预约订单系统接入（流水表）→ 单台计数物化 → 完全直接支持。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021-2026"],
        "base_years_note": "预约量为累计存量读数（流水派生），无历史时序；流水接入后以日志覆盖年为首个可观测年。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted(
            ["128", "156", "89", "42", "1336", "1,336", "542", "280", "218", "0", "15"])},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 完全不支持 | reservationCount 承载三源 0 命中")


if __name__ == "__main__":
    main()
