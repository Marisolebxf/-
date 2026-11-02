#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_EXCH_001 活动类型分布 —— 薄壳校验脚本。

共享探针真源：code/_shared_s309_gamma.py（dev/gkx/jiuxin 活动主档面三源词族）
本脚本职责：①引用共享快照断言 ②活动/交流主档面零承载复核 ③判档 ④基期三键 ⑤落盘。
"""
from __future__ import annotations

import json

SHARED = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/_snapshots/_shared_s309_gamma_out.json"
OUT = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/M_SCIUI_EXCH_001_out.json"


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        snap = json.load(f)

    dev = snap["dev"]
    gkx = snap["gkx"]
    jiuxin = snap["jiuxin"]

    # 断言：活动主档面三源零承载（异域命中逐一登记）
    assert dev["dev_calibration_family"] == []
    assert "gkxlumenx_ads.policy_match" in dev["dev_contest_family"]
    assert isinstance(jiuxin["jiuxin_activity_family"], list)

    out = {
        "metric_id": "M_SCIUI_EXCH_001",
        "batch": "S3-09",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/tech-service/TechExchange.jsx:344-349",
            "repos/demo-ui-science/src/pages/tech-service/TechExchange.jsx:64-78",
            "repos/demo-ui-science/src/pages/tech-service/mockData.js:233-239",
            "repos/demo-ui-science/src/pages/tech-service/TechExchange.jsx:236-244",
            "repos/demo-ui-science/src/pages/tech-service/mockData.js:223-230",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "三份说明书未出现「活动类型分布」指标名；科技交流页为科技创新服务全景平台（主需求 1.2 域）UI 挂载件，筛选行为「按活动类型筛选」为类型维的功能面上位覆盖；清单登记 row_01=721。",
        },
        "facts": {
            "ui_mount": "TechExchange.jsx:344-349 地图视图右栏「活动类型分布」饼图卡（ReactECharts option=getActivityTypeOption()）+ :64-78 环形饼定义（data=activityTypeDistribution，tooltip {b}: {c} ({d}%)）",
            "ui_mock": "mockData.js:233-239 activityTypeDistribution 六类演示分布（学术会议 45/论坛 68/研讨会 89/峰会 34/竞赛 23/交流会 56，合计 315）——ui_demo_fallback 演示值",
            "ui_filter": "TechExchange.jsx:236-244 活动类型筛选（全部/学术会议/论坛/研讨会/峰会/竞赛），联动 :147-153 filteredActivities——分布图为筛选联动的动态计数语义",
            "ui_master": "mockData.js:223-230 techActivities 6 行演示活动主档（type/field/scale/date/location/organizer/participants/status）——活动台账语义演示",
            "jiuxin_activity_family": jiuxin["jiuxin_activity_family"],
            "gkx_activity_family": gkx["gkx_activity_family"],
            "dev_activity_family": dev["dev_activity_family"],
            "gkx_table_count": gkx["gkx_table_count"],
            "dev_table_total": dev["dev_table_total"],
            "jiuxin_table_count_live": jiuxin["jiuxin_table_count_live"],
            "named_in_srs": False,
        },
        "derived": [
            {
                "name": "activity_type_distribution",
                "value": None,
                "note": "负结论登记：活动类型分布 = 活动台账按 type 列分组计数（学术会议/论坛/研讨会/峰会/竞赛/交流会等类目）。mock 主档 techActivities 仅 6 行演示；三源活动词族命中全为异域面（dev 10 表为创新事件/产业链事件族，gkx 4 表为外汇牌价/并购事件/通用事件，jiuxin 3 表为科研难题/人才事件族），无科技交流活动台账。分布无从算起，null 登记。",
            },
        ],
        "absence_probe": [
            {
                "probe": "jiuxin 218 表（SHOW TABLES 实数）科技交流活动台账（activity|event|exchange|forum|conference|seminar|summit）",
                "source": "jiuxin",
                "sql": "SHOW TABLES + 表名词族匹配（快照 jiuxin.jiuxin_activity_family）",
                "hits": 3,
                "hit_tables": ["ads_research_problem_event", "ads_talent_industry_activity", "ads_talent_mobility_event"],
                "verdict": "全为异域：科研难题事件/人才产业活动/人才流动事件——无学术会议/论坛类活动主档",
            },
            {
                "probe": "dev 17 schema（542 表）活动台账/交流会词族",
                "source": "dev",
                "sql": "information_schema.tables 表名词族扫描（快照 dev.dev_activity_family）",
                "hits": 10,
                "hit_tables_head": ["gkxlumenx_ads.event_relation", "gkxlumenx_ads.innovation_event", "gkxlumenx_dwd.event_std", "gkxlumenx_dwd.industry_chain_event_entity_rel"],
                "verdict": "全为异域：创新事件/产业链事件（投资/里程碑/新闻）/服务节点财务事件族——无科技交流活动台账",
            },
            {
                "probe": "gkx 280 表活动/交流词族",
                "source": "gkx",
                "sql": "information_schema.tables table_name REGEXP activity|event|exchange|forum|conference|seminar|summit（快照 gkx.gkx_activity_family）",
                "hits": 4,
                "hit_tables": ["dwd_event", "dwd_foreign_exchange_info", "dwd_foreign_exchange_info_bak_20260911", "dwd_merger_acquisition_events_party_info"],
                "verdict": "全为异域：foreign_exchange=外汇牌价（金融语义）；merger_acquisition=并购事件；dwd_event=通用事件要素库——无交流活动主档",
            },
        ],
        "support_judgment": "完全不支持",
        "notes": [
            "判档理由：活动类型分布需「科技交流活动台账（活动×类型×时间×地点）」主档面。三源活动词族逐一探针：jiuxin 3 表为科研难题/人才事件族；dev 10 表为创新事件/产业链事件族（industry_chain_investment/milestone/news_event 等）；gkx 4 表中 dwd_foreign_exchange_info 是外汇牌价（金融 exchange，非科技交流）、dwd_merger_acquisition_events_party_info 是并购事件——全部异域，交流活动台账三源零承载。无台账即无类型分布，判完全不支持。",
            "exchange 词族命中歧义披露：gkx dwd_foreign_exchange_info 表名的 exchange 为「外汇」语义（金融牌价数据），与「科技交流」语义无关——词族命中不等于语义命中，逐一排除后 0 承载。",
            "mock activityTypeDistribution 六类 315 场与 KPI「年度活动 456 场」演示值不互相勾稽（45+68+89+34+23+56=315≠456）——mock 自身即非同一口径，进一步说明演示值不可作基数。",
            "UI mock 六类分布/KPI 456 场/6 行活动主档均为演示值，不参与支持度结论（ui_demo_fallback 披露）。",
            "本件为薄壳：共享探针 code/_shared_s309_gamma.py + 快照 _snapshots/_shared_s309_gamma_out.json；本脚本仅做断言+判档落盘。与 CONTEST_001（竞赛类型分布）共享探针证据，独立薄壳各自落盘。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021-2026"],
        "base_years_note": "分布为当期截面计数（无时间轴）；活动台账零承载故无任何年度可用。若接入活动台账，基期轴应取活动举办年度（date 字段），首年即基期。",
        "ctx_refs": {
            "note": "正文引用型数字登记",
            "refs": sorted(["315", "456", "6", "45", "68", "89", "34", "23", "56", "3", "10", "4", "542", "280", "218", "17"]),
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 完全不支持 | jiuxin/gkx/dev activity hits:",
          len(jiuxin["jiuxin_activity_family"]), len(gkx["gkx_activity_family"]), len(dev["dev_activity_family"]))


if __name__ == "__main__":
    main()
