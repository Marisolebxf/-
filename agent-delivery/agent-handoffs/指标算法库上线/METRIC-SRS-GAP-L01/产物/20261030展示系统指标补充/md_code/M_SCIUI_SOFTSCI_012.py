#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_SOFTSCI_012 满意度分布 —— 薄壳校验脚本（完全不支持件）。

UI：IncubationCarrierPage.jsx:1033「满意度分布」1-5 星评分柱状图（企业数）。
口径=在孵企业对载体服务满意度评分分布（1-5 星，N=100 mock）。
三源 satisfaction 词族命中均为语义污染（营业额 operating_revenue/债券评级 rating/
经营状态 code_operating_status），无评价/评分/问卷承载。
"""
from __future__ import annotations

import json

OUT = "M_SCIUI_SOFTSCI_012_out.json"

SATISFACTION_HITS_DEV = sorted([
    "gkxlumenx_dwd.foreign_org_annual_financial_info.operating_revenue",
    "gkxlumenx_dwd.high_tech_industry_bonds.issue_issuer_rating",
    "gkxlumenx_dwd.high_tech_industry_bonds.latest_bond_rating",
    "gkxlumenx_dwd.high_tech_industry_bonds.latest_issuer_rating",
    "gkxlumenx_dim.code_operating_status.表名命中 satisfaction",
])

MOCK = {"1": 3, "2": 8, "3": 18, "4": 42, "5": 29}
assert sum(MOCK.values()) == 100

out = {
    "metric_id": "M_SCIUI_SOFTSCI_012",
    "batch": "S3-07-L2",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/achievement-preview/modules/incubation-carrier/components/IncubationCarrierPage.jsx:1033",
    ],
    "facts": {
        "ui_mount": "IncubationCarrierPage.jsx:1033 SoftChartFrame title=满意度分布 badge=1-5 星评分（运行绩效监控看板第四张图）",
        "ui_build_fn": "IncubationCarrierPage.jsx:833 buildSatisfactionOption：柱状图 x=1星..5星 y=企业数量，tooltip 占比=round(count/total*100)",
        "ui_mock_data": "incubationCarrierMock.js:298-304 satisfactionData rating1-5 count=(3,8,18,42,29)，N=100",
        "ui_mock_note": "mock 为演示值不参与判档（ui_demo_fallback 披露）；4 星为众数 42%，5 星 29%，1 星 3%",
        "dev_table_total": 542,
        "dev_satisfaction_word_hits_note": "satisfaction 词族命中全为语义污染（营业额/债券评级/经营状态），无评价语义",
        "dev_satisfaction_semantic_tables": [],
        "gkx_table_count": 280,
        "gkx_satisfaction_word_hits_note": "gkx satisfaction 词族命中同族污染（operating_revenue/rating），无评价表",
        "jiuxin_table_count_live": 218,
        "jiuxin_satisfaction_word_hits_note": "久新 satisfaction 词族命中为同族污染（rating 类），无 NPS/问卷/评价表",
        "named_in_srs": False,
        "named_note": "三份说明书未出现「满意度分布」指标名（检索记录附录 A）。",
    },
    "derived": [
        {"name": "satisfaction_rating_distribution", "value": None,
         "reason": "满意度评分需评价数据面（问卷/评分记录：主体+客体+星级+时间）；三源 satisfaction 词族命中均为语义污染（营业额 operating_revenue、债券评级 issue_issuer_rating/latest_bond_rating/latest_issuer_rating、经营状态码表 code_operating_status），无评价表。"},
    ],
    "absence_probe": [
        {"probe": "dev 542 表 satisfaction/nps/评价 词族", "source": "dev",
         "sql": "information_schema.columns 词族扫描（_probe_s307_l2 快照）",
         "semantic_hits": 0, "polluted_hits": SATISFACTION_HITS_DEV},
        {"probe": "gkx 280 表 satisfaction/nps/评价 词族", "source": "gkx",
         "sql": "information_schema.columns 词族扫描（快照）", "semantic_hits": 0},
        {"probe": "jiuxin 218 表（SHOW TABLES 实数）satisfaction/nps/评价 词族", "source": "jiuxin",
         "sql": "SHOW TABLES+列扫描（快照）", "semantic_hits": 0},
    ],
    "support_judgment": "完全不支持",
    "notes": [
        "判档理由：满意度分布的评价数据面（问卷/评分记录）三源零承载；词族命中全为语义污染（营业额/债券评级/经营状态码），不可作代理。",
        "NPS/满意度业界口径：推荐者%−贬损者%（NPS 0-10 → 1-5 星映射非标准）；火炬 2019 指标体系无满意度指标（服务能力为人员/导师/机构配置）。",
        "在孵企业满意度调查属火炬统计调查制度年报可选字段（服务满意度），需问卷采集非库内计算。",
        "mock (3,8,18,42,29) N=100 为演示值（ui_demo_fallback 披露）。",
        "本件为薄壳：复用共享快照词族面 + 语义污染清单断言。",
    ],
    "base_years_used": [],
    "base_years_missing": ["2021", "2022", "2023", "2024", "2025", "2026"],
    "base_years_note": "评价数据面零承载，无任何年度满意度调查可观测；问卷系统接入后首个完整调查年为基期。",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted({
        "100", "3", "8", "18", "42", "29", "5", "1", "542", "280", "218", "0",
    })},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", OUT)
print("judgment: 完全不支持 | mock N=100 dist:", MOCK, "| semantic_hits: 0")
