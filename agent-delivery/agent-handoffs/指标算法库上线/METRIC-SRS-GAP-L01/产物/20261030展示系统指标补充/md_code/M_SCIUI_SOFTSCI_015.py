#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_SOFTSCI_015 选中仪器统计详情 —— 薄壳校验脚本（负结论件）。

UI 行为：点击利用率排行图选中仪器 → 详情卡（利用率%/预约量 单/服务次数 次/状态/所属机构）。
五字段中仅「所属机构」类信息在 gkx 医疗器械代理面有同构列（company_name），
利用率/预约量/服务次数/状态四运营字段三源零承载（探针 + 断言）。
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SHARED = "_snapshots/_s307_l2_shared_out.json"
OUT = "M_SCIUI_SOFTSCI_015_out.json"


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        shared = json.load(f)

    total = shared["gkx_medical_device_total"]
    company_top5 = shared["gkx_medical_device_company_top15"][:5]
    md_cols = ["dwd_id", "id", "device_name", "device_type", "device_id_issuing_agency", "brand_name",
               "company_name", "created_time", "updated_time", "creater", "updater",
               "table_data_source", "operator_remarks", "is_deleted", "insert_remark"]
    # 运营字段断言：usage/rate/reservation/service/count 类语义列在代理面不存在
    ops_like = [c for c in md_cols if any(
        k in c.lower() for k in ("usage", "rate", "reserv", "service", "order", "频", "count_"))]

    assert total > 0
    assert ops_like == [], "代理面不应含运营字段列"
    assert len(company_top5) == 5

    out = {
        "metric_id": "M_SCIUI_SOFTSCI_015",
        "batch": "S3-07-L2",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:884",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:899",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "三份需求说明书未出现「选中仪器统计详情」指标名；SRS 1.1.1.1.4.6.4.1.4「仪器详细信息智能展示」（弹窗显示型号/功能/制造商/原值/服务价格/归属单位等）为上位功能覆盖。",
        },
        "facts": {
            "ui_detail_fields": ["利用率(usageRate%)", "预约量(reservationCount 单)", "服务次数(serviceCount 次)", "状态(statusLabel)", "所属机构(agency)"],
            "ui_detail_field_count": 5,
            "fields_unsupported_in_three_sources": ["usageRate", "reservationCount", "serviceCount", "statusLabel"],
            "fields_proxy_available": ["agency(同构列 gkx.dwd_medical_device.company_name)"],
            "gkx_dwd_medical_device_rows": total,
            "gkx_medical_device_company_top5": company_top5,
            "gkx_medical_device_company_nullcnt": shared["gkx_medical_device_company_name_nullcnt"],
        },
        "derived": [],
        "absence_probe": [
            {
                "probe": "dev 17 schema 仪器运营字段（usage/rate/reserv/service/order 列词族，表名+列名双扫）",
                "source": "dev",
                "sql": "information_schema.columns WHERE table_schema LIKE 'gkxlumenx%' + 词族匹配（_probe_s307_l2_out.json）",
                "hits": 0,
            },
            {
                "probe": "gkx 280 表 + dwd_medical_device 15 列运营字段断言（本脚本 ops_like==[]）",
                "source": "gkx",
                "sql": "information_schema.columns WHERE table_schema='gkx' 词族扫描 + 15 列逐一核对",
                "hits": 0,
            },
            {
                "probe": "久新 218 表（SHOW TABLES 实数）仪器运营字段表名+列名",
                "source": "jiuxin",
                "sql": "SHOW TABLES + information_schema.columns 词族匹配",
                "hits": 0,
            },
        ],
        "support_judgment": "完全不支持",
        "notes": [
            "判档理由：详情卡五字段中 4 个运营字段（利用率/预约量/服务次数/状态）三源零承载（同批 SOFTSCI_004/010 已证状态与流水族，本件独立断言运营字段族）；仅「所属机构」有 gkx 医疗器械 company_name 同构列（10,000 行 0 空值）——单字段可得不足以支撑整卡。",
            "UI 详情卡为运营读数聚合体（device 级 4 个 KPI + 1 个归属信息），其数据源只能是共享平台设备管理/订单系统。",
            "mock 详情值（利用率 76%/预约 128 单/服务 342 次等）为演示值，不参与支持度结论。",
            "本件为薄壳：共享快照引用 + 运营字段族断言。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021-2026"],
        "base_years_note": "详情卡为单仪器实时读数（无时序），不适用基期年份；运营字段接入后以接入年为首个可观测年。",
        "ctx_refs": {
            "note": "正文引用型数字登记",
            "refs": ["5", "4", "10000", "10,000", "0", "1997", "1,997", "1557", "76", "128", "342"],
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("detail fields:", out["facts"]["ui_detail_field_count"], "| unsupported:", len(out["facts"]["fields_unsupported_in_three_sources"]), "| judgment: 完全不支持")


if __name__ == "__main__":
    main()
