#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_P10_019 服务频率与资源利用统计 —— 薄壳校验脚本（完全不支持件）。

UI：IncubationCarrierNewPage.jsx:1325「服务频率与资源利用统计」双轴图：
服务场次（柱，政策宣讲 46/投融资路演 32/专家门诊 58/技术对接 41/创业培训 65）
+ 资源利用率（线，86/92/78/83/88%）。
数据：INCUB_008/039 同根字段族（服务流水+利用率零承载）复判——
dev 预约/服务流水表不存在（dwd_instrument_reservation/service_record 均无）；
svc_org_card 0 行空壳；jiuxin service 词族命中为技术热点 stage 码语义。
"""
from __future__ import annotations

import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(BASE, "_snapshots", "_shared_s308_laneb_probe_out.json")
OUT = os.path.join(BASE, "M_SCIUI_P10_019_out.json")

VERDICT = "完全不支持"


def main() -> None:
    snap = json.load(open(SNAP, encoding="utf-8"))
    dev, gkx, jx = snap["dev"], snap["gkx"], snap["jiuxin"]

    # 词族命中里的 service 语义面
    dev_col_hits = dev["dev_column_name_hits"]
    svc_hits = sorted(k for k, v in dev_col_hits.items() if "service" in v)
    jx_hits = dict(jx["jiuxin_table_name_hits"])

    assert dev["dev_table_total"] == 542 and gkx["gkx_table_count"] == 280
    assert jx["jiuxin_table_count_live"] == 218

    out = {
        "metric_id": "M_SCIUI_P10_019",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview-new/incubation-carrier-new/IncubationCarrierNewPage.jsx:1325",
            "repos/demo-ui-science/src/pages/achievement-preview-new/incubation-carrier-new/IncubationCarrierNewPage.jsx:283-294",
            "repos/demo-ui-science/src/pages/achievement-preview-new/incubation-carrier-new/mockData.js:823-827",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "srs_anchor": "创新载体孵化载体.md 序号 555「服务频率与资源利用统计」（需规描述：平台动态统计载体提供服务频率、服务资源使用率，自动生成效率分析报告）——本件即该功能叶的 UI 落位图表（同名）",
            "note": "区块标题与 SRS 功能叶 555 同名",
        },
        "facts": {
            "ui_mount": "IncubationCarrierNewPage.jsx:1325 SectionCard title=服务频率与资源利用统计 extra=MockBadge；serviceOption 双轴图（:283-294）：柱=服务场次（政策宣讲/投融资路演/专家门诊/技术对接/创业培训五类），线=资源利用率%（y2 轴 max=100）",
            "ui_mock_note": "ui_demo_fallback：mock 服务场次 46/32/58/41/65、利用率 86/92/78/83/88%（mockData.js:823-827 operations.service）——五类目与双序列均演示",
            "dev_service_word_hits": svc_hits,
            "dev_service_semantic_note": "命中全为框架/配置语义：sys_log（管理日志）、svc_org_card（0 行空壳）、svc_tech_power_score（0 行）、group_capacity/tenant_capacity（容量配置）、svc_org_circle（0 行）——无服务事件流水；dwd_instrument_reservation/service_record 表不存在（本批探针复核）",
            "dev_dim_carrier_columns": ["admin_code", "carrier_id", "carrier_level", "carrier_type", "lat", "lng", "name", "operator_org_uid", "source"],
            "dev_dim_carrier_rows": 28,
            "dev_dim_carrier_note": "dim.carrier 28 行 9 列纯名录（无服务/频率/利用率列）——载体台账存在但无运营态",
            "gkx_service_note": "280 表 service 词族命中 dwd_drug_profile（适应症 indications）、dwd_bid_*（招标服务）——语义污染",
            "jiuxin_service_note": "218 表 service 词族命中为 ads_technology_hotspot_stage 码（技术阶段）与 drug service 列——学术库无载体服务语义",
            "sibling_verdicts": "INCUB_008（仪器使用率）/INCUB_039（热门仪器利用率排行）同根字段族（usageRate/机时）已判完全不支持；本件为载体服务域复判，独立留证",
            "dev_table_total": dev["dev_table_total"],
            "gkx_table_count": gkx["gkx_table_count"],
            "jiuxin_table_count_live": jx["jiuxin_table_count_live"],
        },
        "derived": [
            {
                "name": "service_frequency_negative",
                "value": None,
                "note": "负结论登记：服务频率需服务事件流水（载体×服务类型×场次×时间），三源零承载；资源利用率需资源使用量/总量双面，同缺——禁伪公式",
            },
        ],
        "absence_probe": [
            {"probe": "dev 542 表 service/reserv/booking/appoint/usage 词族（表名+列名双扫）+ 预约流水表直查", "source": "dev",
             "hits": svc_hits,
             "rows": 0,
             "note": "框架配置语义污染清单见 facts；dwd_instrument_reservation/service_record 物理不存在；svc_* 三表 0 行"},
            {"probe": "gkx 280 表 service 词族", "source": "gkx",
             "hits": ["dwd_drug_profile", "dwd_bid_base_out", "dwd_bid_target_item_out"],
             "note": "适应症/招标服务语义污染；无载体服务流水"},
            {"probe": "jiuxin 218 表（SHOW TABLES 实数）service/usage 词族", "source": "jiuxin",
             "hits": [],
             "note": "学术分析库无载体运营域表（表名 0 命中）"},
        ],
        "support_judgment": VERDICT,
        "notes": [
            "判档理由：双轴图两序列同缺原料——服务场次（柱）需载体服务事件流水（政策宣讲/路演/门诊等服务类型×场次×时间），资源利用率（线）需使用量/总量双面：三源逐一探查零承载，dev 命中全为框架配置（sys_log/容量配置）与 0 行空壳（svc_* 三表），预约流水表物理不存在。",
            "dim.carrier 28 行 9 列为载体名录（含坐标/类型/层级）——结构面存在但无任何运营态列，无法派生服务频率。",
            "与 INCUB_008/039（仪器域 usageRate 族）同根不同载体：本件为载体服务域（政策宣讲类软服务），仪器族为设备机时域；两域同判完全不支持、独立留证。",
            "SRS 555「动态统计…自动生成效率分析报告」承诺整链依赖载体运营系统对接（服务登记/资源预约模块），库内无路径。",
            "升档路径：载体服务管理系统接入（服务事件表：载体 ID+服务类型+时间+场次；资源表：资源 ID+容量+使用量）→ 完全转换支持。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021", "2022", "2023", "2024", "2025", "2026"],
        "base_years_note": "无任何真实服务/利用率数据（mock 为无时间轴的类别演示序列）；基期无从谈起，全空登记。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted({
            "46", "32", "58", "41", "65", "86", "92", "78", "83", "88", "5",
            "28", "9", "0", "542", "280", "218",
        })},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment:", VERDICT)


if __name__ == "__main__":
    main()
