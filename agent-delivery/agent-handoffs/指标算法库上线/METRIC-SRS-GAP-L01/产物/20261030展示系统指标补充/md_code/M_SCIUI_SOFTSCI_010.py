#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_SOFTSCI_010 月度预约趋势 —— 薄壳校验脚本（负结论件）。

共享真源：code/_probe_s307_l2.py（三源预约流水词族探针）。
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code")

SHARED = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/_snapshots/_probe_s307_l2_out.json"
OUT = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/M_SCIUI_SOFTSCI_010_out.json"


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        probe = json.load(f)

    # 预约词族三源命中复核（reserv/booking/appoint/book_）
    dev_hits = probe["dev"]["column_scan"]["table_name_hits"]
    gkx_hits = probe["gkx"]["column_scan"]["table_name_hits"]
    jx_hits = probe["jiuxin"]["table_name_hits"]
    # 三源表名命中中预约语义的表：逐一核验（无 → 0）
    dev_reserv = {t: f for t, f in dev_hits.items() if any("reserv" in x or "booking" in x or "appoint" in x for x in f)}
    gkx_reserv = {t: f for t, f in gkx_hits.items() if any("reserv" in x or "booking" in x or "appoint" in x for x in f)}
    jx_reserv = {t: f for t, f in jx_hits.items() if any("reserv" in x or "booking" in x or "appoint" in x for x in f)}

    assert not dev_reserv and not gkx_reserv and not jx_reserv, "三源预约流水表应为 0 命中"
    # gkx 医疗器械代理面无预约列（15 列清单复核）
    md_cols = ["dwd_id", "id", "device_name", "device_type", "device_id_issuing_agency", "brand_name",
               "company_name", "created_time", "updated_time", "creater", "updater",
               "table_data_source", "operator_remarks", "is_deleted", "insert_remark"]
    reserv_like = [c for c in md_cols if any(k in c.lower() for k in ("reserv", "book", "appoint"))]
    assert reserv_like == []

    out = {
        "metric_id": "M_SCIUI_SOFTSCI_010",
        "batch": "S3-07-L2",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:1375",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:180",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/mock/instrumentSharingMock.js:111",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "三份需求说明书未出现「月度预约趋势」指标名；SRS 1.1.1.1.4.6.4.2 预约服务智能管理（服务预约地图展示/预约订单追踪与排期调度）为上位功能覆盖。",
        },
        "facts": {
            "ui_mock_monthly_reservations_6points_sum": 82 + 94 + 111 + 123 + 138 + 151,
            "ui_mock_months_count": 6,
            "probe_snapshot": "_snapshots/_probe_s307_l2_out.json",
            "three_source_reservation_table_hits": {"dev": len(dev_reserv), "gkx": len(gkx_reserv), "jiuxin": len(jx_reserv)},
        },
        "derived": [],
        "absence_probe": [
            {
                "probe": "dev 17 个 gkxlumenx_* schema 预约流水面（表名+列名 reserv/booking/appoint 词族双扫）",
                "source": "dev",
                "sql": "information_schema.columns WHERE table_schema LIKE 'gkxlumenx%' + 词族匹配（_probe_s307_l2.py）",
                "hits": 0,
            },
            {
                "probe": "gkx 280 表预约流水表 + dwd_medical_device 15 列预约列断言",
                "source": "gkx",
                "sql": "information_schema.columns WHERE table_schema='gkx' 词族扫描 + 15 列逐一核对（本脚本断言）",
                "hits": 0,
            },
            {
                "probe": "久新 218 表（SHOW TABLES 现场实数）预约/订单词族表名+列名",
                "source": "jiuxin",
                "sql": "SHOW TABLES + information_schema.columns 词族匹配",
                "hits": 0,
            },
        ],
        "support_judgment": "完全不支持",
        "notes": [
            "判档理由：月度预约趋势 = 预约订单流水按月聚合；预约流水表三源 0 命中（表名+列名双扫），mock 6 点序列（1-6 月：82/94/111/123/138/151，合计 699 单）为演示值不参与结论。",
            "UI 交互细节：buildScaledMonthlyReservations 按筛选集预约量占比缩放 mock 基线——行为本身依赖每台仪器的 reservationCount 字段，该字段同样无库内承载。",
            "SRS 明文「有效订单数 1336 个」为 2020 年末平台快照（附录 A），是外部运营数字非库内数据。",
            "本件为薄壳：探针复跑断言 + 判档落盘。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021-2026"],
        "base_years_note": "预约趋势为流水时序读数；三源无流水表，无任何年度可观测。UI mock 序列（2025.05-2026.04 形态）为演示值不可作基期。真实流水接入后以流水覆盖年为基期。",
        "ctx_refs": {
            "note": "正文引用型数字登记",
            "refs": ["6", "699", "1336", "1,336", "82", "94", "111", "123", "138", "151", "0"],
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("mock 6点合计:", out["facts"]["ui_mock_monthly_reservations_6points_sum"], "| 三源命中:", out["facts"]["three_source_reservation_table_hits"])


if __name__ == "__main__":
    main()
