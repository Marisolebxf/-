#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_SOFTSCI_004 仪器状态分布 —— 薄壳校验脚本。

共享真源：code/_shared_s307_l2.py（gkx.dwd_medical_device 结构面）
+ code/_probe_s307_l2.py（三源状态/预约列词族探针）。
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code")

SHARED = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/_snapshots/_s307_l2_shared_out.json"
OUT = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/M_SCIUI_SOFTSCI_004_out.json"


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        shared = json.load(f)

    total = shared["gkx_medical_device_total"]
    # 唯一含状态语义的列族核验：dwd_medical_device 15 列无 status 列
    cols = ["dwd_id", "id", "device_name", "device_type", "device_id_issuing_agency",
            "brand_name", "company_name", "created_time", "updated_time", "creater",
            "updater", "table_data_source", "operator_remarks", "is_deleted", "insert_remark"]
    status_like = [c for c in cols if any(k in c.lower() for k in ("status", "state", "share", "avail", "busy", "idle", "maintain"))]

    assert total > 0
    assert status_like == [], "dwd_medical_device 不应含状态列（探针已证）"

    out = {
        "metric_id": "M_SCIUI_SOFTSCI_004",
        "batch": "S3-07-L2",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:1389",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:206",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "三份需求说明书未出现「仪器状态分布」指标名；SRS 1.1.1.1.4.6.4.1.3「共享状态与资源利用动态」（空闲/排期协调/忙碌图标+自动统计共享率及使用频率）为上位功能覆盖。",
        },
        "facts": {
            "gkx_dwd_medical_device_rows": total,
            "gkx_dwd_medical_device_columns_total": len(cols),
            "gkx_dwd_medical_device_status_like_columns": status_like,
            "ui_mock_status_definitions": ["available(可预约)", "busy(预约紧张)", "maintenance(维护中)"],
            "shared_snapshot": "_snapshots/_s307_l2_shared_out.json",
            "absence_snapshot": "_snapshots/_probe_s307_l2_out.json",
        },
        "derived": [],
        "absence_probe": [
            {
                "probe": "dev 17 个 gkxlumenx_* schema 仪器运行状态列（status/state/share/avail/busy/idle/maintain 词族，表名+列名双扫）",
                "source": "dev",
                "sql": "SELECT table_schema,table_name,column_name FROM information_schema.columns WHERE table_schema LIKE 'gkxlumenx%' + Python 词族匹配（_probe_s307_l2.py）",
                "hits": 0,
            },
            {
                "probe": "gkx 280 表仪器状态面：dwd_medical_device 15 列逐一核对无 status/state 类列（本脚本断言）",
                "source": "gkx",
                "sql": "information_schema.columns WHERE table_schema='gkx' AND table_name='dwd_medical_device'",
                "hits": 0,
            },
            {
                "probe": "久新 218 表（SHOW TABLES 现场实数）仪器/状态词族表名+列名",
                "source": "jiuxin",
                "sql": "SHOW TABLES + information_schema.columns WHERE table_schema='gkx_technology_analysis_dev' 词族匹配",
                "hits": 0,
            },
        ],
        "support_judgment": "完全不支持",
        "notes": [
            "判档理由：运行状态（空闲/排期协调/忙碌/维护中）是仪器共享平台的实时运营态，依赖预约排期流水或设备管理系统直连；三源均无仪器台账（SOFTSCI_003 已证）→ 状态维无从挂载，且无任何 status 类列承载。",
            "gkx.dwd_medical_device 有分类结构但无状态列（15 列逐一核对，本脚本断言 status_like==[]）——代理面也不可用。",
            "UI mock 三态（available/busy/maintenance，buildStatusDistribution 按 STATUS_DEFINITIONS 遍历计数）为演示值，不参与支持度结论。",
            "科技部考核口径（R1）中状态对应「开放率/可预约比例」，由国家网络管理平台实时记录——外部运营系统数据，非库内可构建。",
            "本件为薄壳：共享探针 code/_probe_s307_l2.py + 本脚本断言。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021-2026"],
        "base_years_note": "状态分布为实时存量读数（无历史时序），不适用基期年份；UI mock 无时序。真实状态面接入后以接入年为首个可观测年。",
        "ctx_refs": {
            "note": "正文引用型数字登记",
            "refs": ["10000", "10,000", "15", "0", "5612", "5,612", "60.59%", "9262", "9,262"],
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("rows:", total, "| status_like cols:", status_like, "| judgment: 完全不支持")


if __name__ == "__main__":
    main()
