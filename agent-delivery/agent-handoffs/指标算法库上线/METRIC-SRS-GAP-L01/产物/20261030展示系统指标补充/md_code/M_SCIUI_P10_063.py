#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_P10_063 精密几何量计量校准服务量（次）—— 薄壳校验脚本。

共享探针真源：code/_shared_s309_gamma.py（计量校准词族三源）+ code/_shared_s308_laneC.py（检测服务流水域，同族）
本脚本职责：①引用两份共享快照断言（与 P10_060/062 同族） ②计量校准流水域零承载独立复核 ③判档 ④基期三键 ⑤落盘。
"""
from __future__ import annotations

import json

SHARED_G = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/_snapshots/_shared_s309_gamma_out.json"
SHARED_C = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/_snapshots/_shared_s308_laneC_out.json"
OUT = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/M_SCIUI_P10_063_out.json"


def main() -> None:
    with open(SHARED_G, encoding="utf-8") as f:
        sg = json.load(f)
    with open(SHARED_C, encoding="utf-8") as f:
        sc = json.load(f)

    jiuxin_g = sg["jiuxin"]
    gkx_g = sg["gkx"]
    dev_g = sg["dev"]
    jiuxin_c = sc["jiuxin"]

    # 断言：计量校准词族三源零命中 + 订单流水族空（S3-08 laneC 同族证据）
    assert dev_g["dev_calibration_family"] == [], "dev calib 族应为空"
    assert gkx_g["gkx_calibration_family"] == [], "gkx calib 族应为空"
    assert jiuxin_g["jiuxin_calibration_family"] == [], "jiuxin calib 族应为空"
    assert jiuxin_c["jiuxin_booking_order_family"] == [], "jiuxin booking/order 族应为空（laneC）"
    assert jiuxin_c["jiuxin_service_family"] == [], "jiuxin service 族应为空（laneC）"
    assert sc["gkx"]["gkx_medical_device_measure_like_rows"] == 2

    out = {
        "metric_id": "M_SCIUI_P10_063",
        "batch": "S3-09",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview-new/instrument-sharing-new/mockData.js:153",
            "repos/demo-ui-science/src/pages/achievement-preview-new/instrument-sharing-new/mockData.js:167-184",
            "repos/demo-ui-science/src/pages/achievement-preview-new/instrument-sharing-new/InstrumentSharingNewPage.jsx:695-703",
            "repos/demo-ui-science/src/pages/achievement-preview-new/instrument-sharing-new/InstrumentSharingNewPage.jsx:719-731",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "三份说明书未出现「精密几何量计量校准服务量」指标名；上位功能叶 1.1.1.1.4.6.6.3 预约服务（SRS 大型科学仪器共享.md:123「系统自动显示服务状态、周期及频率……」）为功能面上位覆盖；本件=检测服务订单流水按服务类别的年度计数切片（类别=计量校准·精密几何量），与 P10_060 热分析/P10_062 理化分析同族同因（派单标注三件族尾）。清单登记 row_01=682。",
        },
        "facts": {
            "ui_mount": "mockData.js:153 SVC-0009「精密几何量计量校准」服务项（type 计量校准/shareType 完全开放/cycle 1–2 个工作日/org 深圳市计量质量检测研究院/district 光明区/freq 140/rating 4.6）——检测服务列表项语义（ui_demo_fallback 演示值）",
            "ui_service_master": "mockData.js:167-184 SERVICES 14 项服务主档（type 四类：检测服务/分析测试/计量校准/软件测评），SVC-0009 为计量校准类唯一项",
            "ui_lineage": "InstrumentSharingNewPage.jsx:695-703「服务类型统计」图（M_IS_SERVICE_TYPE，源表 ads_is_service）+ :719-731「预约订单追踪」表（ORDERS 12 行演示）——类别统计语义的 lineage 契约",
            "ui_kpi": "mockData.js:53-57 有效订单 KPI（M_IS_VALID_ORDER value=1,336 个，本年度已完成及服务中预约订单总数不含已取消；源表 ads_is_order；T+1；v1.0）——服务量总口径 lineage 契约",
            "jiuxin_calibration_family": jiuxin_g["jiuxin_calibration_family"],
            "gkx_calibration_family": gkx_g["gkx_calibration_family"],
            "dev_calibration_family": dev_g["dev_calibration_family"],
            "jiuxin_booking_order_family": jiuxin_c["jiuxin_booking_order_family"],
            "jiuxin_service_family": jiuxin_c["jiuxin_service_family"],
            "jiuxin_ads_is_hits": jiuxin_c["jiuxin_ads_is_hits"],
            "gkx_medical_device_measure_like_rows": sc["gkx"]["gkx_medical_device_measure_like_rows"],
            "gkx_table_count": gkx_g["gkx_table_count"],
            "dev_table_total": dev_g["dev_table_total"],
            "jiuxin_table_count_live": jiuxin_g["jiuxin_table_count_live"],
        },
        "derived": [
            {
                "name": "precision_geometry_calibration_volume",
                "value": None,
                "note": "负结论登记：精密几何量计量校准服务量 = 检测服务订单流水按服务类别（计量校准·精密几何量）的年度计数。lineage 源表族 ads_is_order/ads_is_service 及 ads_is_* 全族三源 0 实存；计量校准词族（calibr|metrolog|geometr|cmm|coordinate measur）三源 0 命中；booking/order/service 词族三源 0 语义命中（S3-08 laneC 快照）。gkx 唯一近似面 dwd_medical_device 命名含 measur 仅 2 行且为骨科螺钉注册名碎片（MEASURING SCREWDRIVER），非计量校准。订单流水零承载，类别切片无从谈起，null 登记。与 P10_060/062 共享流水域缺口（两份快照证据），独立薄壳落盘。",
            },
        ],
        "absence_probe": [
            {
                "probe": "计量校准词族（calibr|metrolog|geometr|cmm|coordinate.?measur）三源表名扫描",
                "source": "dev+gkx+jiuxin",
                "sql": "information_schema.tables / SHOW TABLES 词族匹配（快照 _shared_s309_gamma_out.json dev/gkx/jiuxin *_calibration_family）",
                "hits": 0,
                "verdict": "dev 542 表 0 命中 / gkx 280 表 0 命中 / jiuxin 218 表（SHOW TABLES 实数）0 命中——计量校准域三源零表",
            },
            {
                "probe": "检测服务订单流水族（ads_is_* / booking|order / service 词族）",
                "source": "jiuxin",
                "sql": "SHOW TABLES + 词族匹配（快照 _shared_s308_laneC_out.json jiuxin_booking_order_family/jiuxin_service_family/jiuxin_ads_is_hits）",
                "hits": 0,
                "verdict": "jiuxin ads_is_hits=[] / booking_order_family=[] / service_family=[]——订单流水族零实存（与 P10_060/062 同快照同断言）",
            },
            {
                "probe": "dev/gkx service 词族异域排除 + gkx 医疗器械 measure 语义检查",
                "source": "dev+gkx",
                "sql": "表名词族扫描 + dwd_medical_device LIKE measur|coordinate（快照 laneC dev_service_family_table_hits / gkx_service_family / gkx_medical_device_measure_like_rows）",
                "hits": 0,
                "verdict": "dev 22 表命中全为 test_*/analysis_task 内部测试面；gkx 7 表为 dwd_industry_analysis_* 行业分析族；dwd_medical_device 含 measur 仅 2 行（MEASURING SCREWDRIVER 骨科螺钉注册名碎片，FDA 注册语义）——无一为计量校准流水",
            },
        ],
        "support_judgment": "完全不支持",
        "notes": [
            "判档理由：精密几何量计量校准服务量 = 检测服务订单流水按服务类别的年度计数，与 P10_060（热分析）/P10_062（理化分析）同族同因，本件为三件族尾（切片类别=计量校准·精密几何量）。三重探针：①计量校准词族三源 0 表；②订单流水族（ads_is_*/booking/order/service）三源 0 语义实存；③唯一 measure 近似面 dwd_medical_device 仅 2 行注册名碎片。无流水即无类别切片，判完全不支持。",
            "「精密几何量」的计量学语义：几何量计量（长度/角度/形位）是计量学十大专业之一，三坐标测量机（CMM）/激光干涉仪为其核心装备——S3-08 批 INCUB 探针已证 CMM 词族三源零承载（laneC 快照 FAM_CMM），本件词族含 cmm/coordinate measur 复扫仍 0 命中，两批证据互证。",
            "与 P10_060/062 的分件边界：三件共享「检测服务流水域」缺口与 laneC 快照证据，差异仅在切片对象（本件=计量校准·精密几何量 SVC-0009；060=热分析 ORG-005；062=理化分析 ORG-002）；本件另叠加深层词族（calibr/metrolog/geometr/cmm）独立复核（s309 gamma 快照），独立薄壳各自落盘，判档一致。",
            "UI mock SERVICES 14 项/ORDERS 12 行/SVC-0009 freq=140 为演示值，不参与支持度结论（ui_demo_fallback 披露）。",
            "本件为薄壳：共享探针 code/_shared_s309_gamma.py + _shared_s308_laneC.py + 两快照；本脚本仅做断言+判档落盘。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021-2026"],
        "base_years_note": "服务量为年度流量读数（订单完成时间维度），订单流水零承载故无任何年度可用；lineage 口径「本年度已完成及服务中（不含已取消）」提示正式口径应取订单完成年度。若接入 ads_is_order 需以完成时间为基期轴（与 P10_060/062 同）。",
        "ctx_refs": {
            "note": "正文引用型数字登记",
            "refs": sorted(["14", "12", "1,336", "140", "2", "0", "542", "280", "218", "22", "7", "4", "SVC-0009", "T+1", "v1.0"]),
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 完全不支持 | calib family dev/gkx/jiuxin:",
          dev_g["dev_calibration_family"], gkx_g["gkx_calibration_family"], jiuxin_g["jiuxin_calibration_family"],
          "| measure-like:", sc["gkx"]["gkx_medical_device_measure_like_rows"])


if __name__ == "__main__":
    main()
