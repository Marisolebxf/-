#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INCUB_061 高分辨检测服务量（次）—— 薄壳校验脚本（负结论件）。

UI：instrumentSharingMock.js:70 能力标签「高分辨检测」（high-resolution）+
:358 serviceOrders[].serviceItem「高分辨形貌观察」等服务订单流 mock。
语义 = 能力标签为高分辨检测的仪器服务订单计数。探针：服务订单流水三源 0 命中
（dev service 表 0 张 + svc_metric 双表 0 行空壳）；能力标签本身是 mock 自设
维度（无字典承载）；检测语义面（svc_org_card.test 检测服务型机构卡）0 行。
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SHARED = "_snapshots/_shared_s308_lane_a_out.json"
OUT = "M_SCIUI_INCUB_061_out.json"


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        snap = json.load(f)

    dev = snap["dev"]
    gkx = snap["gkx"]
    jx = snap["jiuxin"]
    assert dev["table_total"] == 542 and gkx["table_count"] == 280
    assert jx["table_count_live"] == 218
    assert dev["service_count_like_columns"] == []

    out = {
        "metric_id": "M_SCIUI_INCUB_061",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/mock/instrumentSharingMock.js:70",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/mock/instrumentSharingMock.js:358",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:108",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "「高分辨检测」指标名三份说明书未出现；上位叶 SRS 1.1.1.1.4.6.4 服务机构资源展示（服务内容与能力明细）——检测服务为机构能力明细语义；INCUB 清单 row_01=616。",
        },
        "facts": {
            "ui_mount": "instrumentSharingMock.js:70 能力标签选项「高分辨检测」（value=high-resolution）——分析筛选器 capability 维的标签字典；:358 serviceOrders 服务订单流 mock（serviceItem=高分辨形貌观察等）",
            "ui_capability_labels": "CAPABILITY_LABELS（InstrumentSharingPage.jsx:107-111）：high-resolution=高分辨检测 / fast-report=快速出报告 / cross-agency=跨机构共享——能力标签为 mock 自设维度",
            "ui_service_item_note": "serviceOrders[].serviceItem 演示值（高分辨形貌观察/代谢组学分析等 8 项）——ui_demo_fallback，不参与支持度结论",
            "ui_semantics": "指标语义 = 能力标签为高分辨检测的仪器服务订单计数（次）——筛选器标签 + 服务订单流水的交叉计数",
            "dev_table_total": dev["table_total"],
            "dev_service_tables": "gkxlumenx_* 542 表中 service 词族表名 0 张（_shared_s308_lane_a 词族扫描）",
            "dev_svc_metric_shell": "gkxlumenx_ads.svc_metric_fact / svc_metric_series 双 0 行空壳（metric_id/period/value 列在——服务指标时序预留面无数据）",
            "dev_service_count_like_columns": dev["service_count_like_columns"],
            "gkx_table_count": gkx["table_count"],
            "gkx_service_word_tables": gkx["word_service"],
            "jiuxin_table_count_live": jx["table_count_live"],
            "jiuxin_service_note": "久新 218 表（SHOW TABLES 实数）service/order 词族 0 命中（ads_* 全系科技要素分析面）",
            "named_in_srs": False,
        },
        "derived": [
            {
                "name": "high_resolution_detection_service_count",
                "value": None,
                "numerator": None,
                "denominator": None,
                "note": "高分辨检测服务量 = COUNT(服务订单 WHERE 仪器能力标签=高分辨检测)。服务订单流水三源 0 命中 + 能力标签为 mock 自设维度（无字典承载）→ 不可构建，负结论 null 登记",
            },
        ],
        "absence_probe": [
            {"probe": "dev 服务订单流水面（service/order 词族 542 表 + service_count/total/item 列级三式）",
             "source": "dev", "sql": "information_schema 表名+列名双扫（_shared_s308_lane_a.py 快照）",
             "hits": 0, "note": "svc_metric_fact/series 0 行空壳为服务指标预留面；svc_org_card 0 行（检测服务型机构卡无数据）"},
            {"probe": "gkx service 词族（280 表）",
             "source": "gkx", "sql": "information_schema 表名扫描（快照）", "hits": 0},
            {"probe": "久新 service/order 词族（SHOW TABLES 实数 218 表）",
             "source": "jiuxin", "sql": "SHOW TABLES 词族过滤", "hits": 0},
            {"probe": "能力标签字典（high-resolution 同构维度）",
             "source": "doc", "sql": "三源字典面（dim.code_* 族）核对",
             "hits": 0, "note": "能力标签为 instrumentSharingMock.js 自设常量（CAPABILITY_LABELS），三源无仪器能力字典表"},
        ],
        "support_judgment": "完全不支持",
        "notes": [
            "判档理由：指标是「能力标签 × 服务订单流水」的交叉计数——两个依赖维三源均零承载：服务订单流水 0 表（svc_metric 双表 0 行空壳证明服务指标设计意图存在但无数据）；能力标签为 mock 自设字典（三源无仪器能力维表）。",
            "检测服务语义面：dev svc_org_card（服务型机构卡，service_type_candidate 列在）0 行——检测服务型机构画像同样空壳。",
            "同族关系：P10_060（热分析测试服务量）/P10_062（理化分析测试服务量）同检测服务流水域（路 C 件），根因同构——本件先行留证。",
            "升档路径：服务订单系统接入 + 仪器能力标签字典化 → 完全转换支持（标签×订单交叉计数）。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021-2026"],
        "base_years_note": "服务量为订单流水计数时序；三源无流水即无任何可观测年；mock serviceOrders 的 applyDate（2026-05 等）为演示标注。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted(
            ["542", "280", "218", "0", "8", "107", "111", "358"])},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 完全不支持 | 服务订单流水与能力标签双缺")


if __name__ == "__main__":
    main()
