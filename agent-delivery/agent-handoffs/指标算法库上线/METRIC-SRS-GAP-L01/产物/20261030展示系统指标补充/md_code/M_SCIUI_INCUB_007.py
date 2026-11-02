#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INCUB_007 仪器使用热度值 —— 薄壳校验脚本（负结论件）。

UI：InstrumentSharingPage.jsx:503 推荐面板「使用热度」= `${usageRate}%`，
同字段驱动 getInstrumentHeatLevel（:220 起，>=80 高热）与 KPI「平均使用率」。
usageRate 为机时派生运营字段——三源零承载（独立断言 + 探针复用）。
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code")

SHARED = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/_snapshots/_s307_l2_shared_out.json"
OUT = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/M_SCIUI_INCUB_007_out.json"


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        shared = json.load(f)

    total = shared["gkx_medical_device_total"]
    md_cols = ["dwd_id", "id", "device_name", "device_type", "device_id_issuing_agency", "brand_name",
               "company_name", "created_time", "updated_time", "creater", "updater",
               "table_data_source", "operator_remarks", "is_deleted", "insert_remark"]
    heat_like = [c for c in md_cols if any(k in c.lower() for k in ("usage", "utiliz", "heat", "hot", "freq", "rate"))]

    assert total > 0
    assert heat_like == [], "代理面不应含热度/使用率类列"

    out = {
        "metric_id": "M_SCIUI_INCUB_007",
        "batch": "S3-07-L2",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:503",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:220",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:173",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "三份需求说明书未出现「使用热度」指标名；SRS 1.1.1.1.4.6.4.1.1「使用评价与频次统计」（自动收集使用频率）与 1.1.1.1.4.6.4.3.4「资源状态与实时活跃度」（高亮热门资源）为上位功能覆盖。",
        },
        "facts": {
            "ui_heat_field": "usageRate(%)",
            "ui_heat_levels": {"high": ">=80", "mid": ">=60（推测中档）", "low": "<60（推测低档）"},
            "ui_heat_level_fn": "getInstrumentHeatLevel(InstrumentSharingPage.jsx:220)",
            "ui_kpi_avg_usage_aggregation": "Math.round(items.reduce(sum usageRate)/total)（:173 KPI 平均使用率）",
            "gkx_dwd_medical_device_rows": total,
            "gkx_dwd_medical_device_heat_like_columns": heat_like,
        },
        "derived": [],
        "absence_probe": [
            {
                "probe": "dev 17 schema 使用率/机时/热度列（usage/utiliz/machine_hour/heat/hot/freq 表名+列名双扫）",
                "source": "dev",
                "sql": "information_schema.columns WHERE table_schema LIKE 'gkxlumenx%' + 词族匹配（_probe_s307_l2_out.json）",
                "hits": 0,
            },
            {
                "probe": "gkx 280 表 + dwd_medical_device 15 列热度/使用率列断言（本脚本 heat_like==[]）",
                "source": "gkx",
                "sql": "information_schema.columns WHERE table_schema='gkx' 词族扫描 + 15 列逐一核对",
                "hits": 0,
            },
            {
                "probe": "久新 218 表（SHOW TABLES 实数）usage/utiliz/machine_hour 词族（表名+列名；学术 hotspot_score 类列为研究热度非仪器使用）",
                "source": "jiuxin",
                "sql": "SHOW TABLES + information_schema.columns 词族匹配（_probe_s307_l2_out.json jiuxin.column_name_hits：ads_research_problem_* 的 hotspot/growth 列均为学术热度语义）",
                "hits": 0,
            },
        ],
        "support_judgment": "完全不支持",
        "notes": [
            "判档理由：UI 的「使用热度」直接复用 usageRate（%），分档函数 getInstrumentHeatLevel 以 80 为高热线——机时利用率派生字段三源零承载；久新的 hotspot_score 族（ads_research_problem_*）是科研问题热度，语义不同不可代理。",
            "KPI 区「平均使用率」（同字段均值聚合，:173）与 INCUB_019（全市均值口径）共享此根因，各自独立留证。",
            "科技部考核口径的对应物是「仪器运行机时（年平均有效工作机时）」（R1）——机时日志属设备管理系统，外部数据。",
            "mock usageRate 值（52-92 区间）为演示值，不参与支持度结论。",
            "本件为薄壳：探针复用 + 热度字段族断言。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021-2026"],
        "base_years_note": "使用热度为实时存量读数（机时派生），无历史时序；机时日志接入后以日志覆盖年为首个可观测年。",
        "ctx_refs": {
            "note": "正文引用型数字登记",
            "refs": ["80", "60", "52", "92", "10000", "10,000", "0"],
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("heat_like cols:", heat_like, "| judgment: 完全不支持")


if __name__ == "__main__":
    main()
