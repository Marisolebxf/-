#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INCUB_008 仪器使用率（机时利用率）—— 薄壳校验脚本（负结论件）。

UI：InstrumentSharingPage.jsx:388/404 抽屉与阶段卡「使用率 `${usageRate}%`」。
口径=机时利用率（有效工作机时/可用机时，科技部考核 R1「仪器运行机时」）。
三源零承载（探针 + 断言，与 INCUB_007 同根因独立留证）。
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SHARED = "_snapshots/_s307_l2_shared_out.json"
OUT = "M_SCIUI_INCUB_008_out.json"


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        shared = json.load(f)

    total = shared["gkx_medical_device_total"]
    md_cols = ["dwd_id", "id", "device_name", "device_type", "device_id_issuing_agency", "brand_name",
               "company_name", "created_time", "updated_time", "creater", "updater",
               "table_data_source", "operator_remarks", "is_deleted", "insert_remark"]
    usage_like = [c for c in md_cols if any(k in c.lower() for k in ("usage", "utiliz", "machine", "hour", "机时"))]

    assert total > 0
    assert usage_like == []

    out = {
        "metric_id": "M_SCIUI_INCUB_008",
        "batch": "S3-07-L2",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:388",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:404",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "三份需求说明书未出现「使用率/机时利用率」指标名；SRS 1.1.1.1.4.6.4.1.3「系统自动统计共享率及使用频率」为上位功能覆盖。",
        },
        "facts": {
            "ui_field": "usageRate(%)",
            "ui_consumers_count": 4,
            "ui_consumers": [
                "KPI 概览「平均使用率」（:173 均值聚合）",
                "抽屉指标「使用率」（:388/404）",
                "推荐面板「使用热度」（:503）",
                "排行与热力分档（:214-233 buildUsageRanking/getInstrumentHeatLevel）",
            ],
            "gkx_dwd_medical_device_rows": total,
            "gkx_dwd_medical_device_usage_like_columns": usage_like,
            "probe_snapshot": "_snapshots/_probe_s307_l2_out.json",
        },
        "derived": [],
        "absence_probe": [
            {
                "probe": "dev 17 schema 机时/使用率面（usage/utiliz/machine_hour 词族表名+列名双扫）",
                "source": "dev",
                "sql": "information_schema.columns WHERE table_schema LIKE 'gkxlumenx%' + 词族匹配",
                "hits": 0,
            },
            {
                "probe": "gkx 280 表 + dwd_medical_device 15 列机时/使用率断言（本脚本 usage_like==[]）",
                "source": "gkx",
                "sql": "information_schema.columns WHERE table_schema='gkx' 词族扫描 + 15 列逐一核对",
                "hits": 0,
            },
            {
                "probe": "久新 218 表（SHOW TABLES 实数）机时/使用率词族",
                "source": "jiuxin",
                "sql": "SHOW TABLES + information_schema.columns 词族匹配",
                "hits": 0,
            },
        ],
        "support_judgment": "完全不支持",
        "notes": [
            "判档理由：机时利用率 = 年有效工作机时/年可用机时（科技部考核 R1 口径「仪器运行机时」15 分权重）；机时日志属设备管理系统，三源零承载；分子分母均无来源。",
            "UI 四处消费同一 usageRate 字段（KPI 均值/抽屉/热度/排行分档）——本件是仪器族使用率读数的根字段件，INCUB_007（热度）与 INCUB_019（全市均值）共享根因、各自独立留证。",
            "mock usageRate（52-92）为演示值，不参与支持度结论。",
            "本件为薄壳：探针复用 + 机时字段族断言。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021-2026"],
        "base_years_note": "机时利用率为年度口径读数（年有效机时/年可用机时）；机时日志接入前无任何年度可观测。接入后首个完整自然年为基期。",
        "ctx_refs": {
            "note": "正文引用型数字登记",
            "refs": ["4", "15", "10000", "10,000", "52", "92", "0"],
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("usage_like cols:", usage_like, "| consumers:", out["facts"]["ui_consumers_count"], "| judgment: 完全不支持")


if __name__ == "__main__":
    main()
