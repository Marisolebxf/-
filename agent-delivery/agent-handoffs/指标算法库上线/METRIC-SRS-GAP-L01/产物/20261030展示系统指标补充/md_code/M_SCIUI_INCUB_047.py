#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INCUB_047 仪器共享能力评分（排行/推荐/导出）—— 薄壳校验脚本（负结论件）。

UI：InstrumentSharingPage.jsx:1568-1577 rankItems（score 排序 分）+ :1884-1896
SoftRankList（投资者角色 rankTitle=机构能力排行）+ :459-470 综合评分推荐项
（ruleMap.score）+ orgAnalysisReport.js:23/:46 导出列「共享能力评分/综合能力分」
（mock 95）。score 语义=仪器/机构共享能力 mock 自设分制。
探针：dev 评分面 enterprise_score 0 行、carrier_index 0 行；gkx score 词族 0 表；
久新评分族（人才 99,996/100,000 行、技术 potential）为人才/技术维度——共享能力
评分域三源零承载。
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code")

SHARED = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/_snapshots/_shared_s308_lane_a_out.json"
OUT = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/M_SCIUI_INCUB_047_out.json"


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        snap = json.load(f)

    dev = snap["dev"]
    gkx = snap["gkx"]
    jx = snap["jiuxin"]
    es = dev["gkxlumenx_ads.enterprise_score"]
    ci = dev["gkxlumenx_ads.carrier_index"]
    assert dev["table_total"] == 542 and gkx["table_count"] == 280
    assert jx["table_count_live"] == 218
    assert es["rows"] == 0 and ci["rows"] == 0
    assert "score_total" in es["columns"]

    out = {
        "metric_id": "M_SCIUI_INCUB_047",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:1568",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:1885",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:467",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/orgAnalysisReport.js:23",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "「仪器共享能力评分」指标名三份说明书未出现；语义锚 SRS 大型科学仪器共享.md 序号 535 机构弹窗「共享能力评分等多维数据」分句——功能要求在、评分口径未给。",
        },
        "facts": {
            "ui_mount": "InstrumentSharingPage.jsx:1568-1577 rankItems（filteredInstruments 按 score 降序 SoftRankList，scoreUnit=分）+:1884-1896 排行卡（投资者角色 rankTitle=机构能力排行，instrumentSharingMock.js:183）",
            "ui_recommend": ":459-470 buildRecommendationItems ruleMap.score「综合评分」项（value=instrument.score 分，reason=机构能力、服务次数与共享稳定性综合靠前）；:1858-1863 推荐面板挂载",
            "ui_export": "orgAnalysisReport.js:23 flattenInstitutionRows「共享能力评分: org.score」（mock institutions 95）+:36-48 flattenAgencyCapabilityRows「综合能力分: row.score」——CSV/JSON/TXT 导出列",
            "ui_mock_note": "mock instruments[].score（94/91/87/76）+ institutions[].score（95）为 ui_demo_fallback 演示自设分制；排序键/推荐理由文案（共享稳定性综合）无数据源依据——不参与支持度结论",
            "dev_table_total": dev["table_total"],
            "dev_enterprise_score": {"columns": es["columns"], "rows": es["rows"]},
            "dev_carrier_index": {"rows": ci["rows"]},
            "dev_svc_tech_power_score": {"note": "word_score 命中 gkxlumenx_ads.svc_tech_power_score（企业技术实力评分域）——非仪器共享能力域，语义不匹配"},
            "gkx_table_count": gkx["table_count"],
            "gkx_score_word_tables": gkx["word_score"],
            "jiuxin_table_count_live": jx["table_count_live"],
            "jiuxin_score_note": "久新评分族（ads_talent_capability_assessment 99,996 行/ads_talent_potential_result 100,000 行，INCUB_027 已证）为人才维度；ads_technology_potential_* 为技术维度——仪器共享能力评分域 0 命中（INCUB_027 检索留证，本批复用结论）",
            "named_in_srs": False,
        },
        "derived": [
            {
                "name": "instrument_sharing_capability_score",
                "value": None,
                "numerator": None,
                "denominator": None,
                "note": "仪器共享能力评分 = 共享能力多维加权分（UI 排行/推荐/导出三挂载）。评分事实面（仪器/机构×分值）与模型权重三源零承载 → 不可构建，负结论 null 登记",
            },
        ],
        "absence_probe": [
            {"probe": "dev 评分结果面（score/rating/evaluat/assess 词族 542 表）",
             "source": "dev", "sql": "information_schema 表名扫描 + 行数实证（_shared_s308_lane_a.py 快照）",
             "hits": 7,
             "hit_detail": "enterprise_score（14 列含 score_total/score_level/model_version）0 行；carrier_index 0 行；svc_tech_power_score 为企业技术实力域；其余为政策评估/操作状态字典/BI 模板语义——仪器共享能力评分域全空壳/不匹配"},
            {"probe": "gkx score 词族（280 表）",
             "source": "gkx", "sql": "information_schema 表名扫描（快照）",
             "hits": 0, "note": "gkx word_score=[]——要素库无评分面"},
            {"probe": "久新 仪器共享能力评分（SHOW TABLES 实数 218 表）",
             "source": "jiuxin", "sql": "SHOW TABLES + 评分族语义核（INCUB_027 留证复用）",
             "hits": 0,
             "hit_detail": "评分族全为人才（talent_capability 99,996 行/talent_potential 100,000 行）与技术（technology_potential）维度——仪器共享能力评分 0 命中"},
            {"probe": "评分模型定义（维度/权重/分制）",
             "source": "doc", "sql": "三份说明书 + 主需求 rg 共享能力评分|仪器共享能力",
             "hits": 1,
             "hit_detail": "SRS 序号 535 机构弹窗多维数据分句（共享能力评分字样）——功能要求在，无评分公式/权重/分制定义"},
        ],
        "support_judgment": "完全不支持",
        "notes": [
            "判档理由：仪器共享能力评分需①评分事实面（仪器/机构×分值）②评分模型（维度/权重）两层。dev enterprise_score/carrier_index 空壳、svc_tech_power_score 企业域不匹配；gkx 0 表；久新评分族人才/技术维度——事实面零承载；模型层三说明书仅功能分句。两层皆缺。",
            "UI 侧评分纯 mock 自设分制：instruments[].score 94/91/87/76 + institutions[].score 95，排行按 score 降序、推荐理由文案自拟（机构能力、服务次数与共享稳定性综合靠前）——演示态自证，orgAnalysisReport.js:5-6 导出免责声明亦自认演示数据非真源。",
            "同族关系：INCUB_043（综合能力评分，机构画像雷达）同 UI 页同评分域不同挂载位；P10_041（共享能力评分）路 C 同族——三件独立留证。挂载差异：043=机构画像卡/雷达，047=排行/推荐/导出链。",
            "语义锚 SRS 序号 535「共享能力评分等多维数据」证明需求意图在——若接入深圳共享平台机构评价/仪器评价数据可升档。",
            "升档路径：共享平台评价结果接入（仪器/机构×评分面落库）→ 完全转换支持；平台侧评分接口直连 → 完全直接支持。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021-2026"],
        "base_years_note": "共享能力评分为当期截面读数（评分快照）；三源无评分面无历史序列；mock 亦无年度序列。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted(
            ["94", "91", "87", "76", "95", "100", "542", "280", "218",
             "99996", "99,996", "100000", "100,000", "14", "0"])},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 完全不支持 | 共享能力评分面三源空壳/0 命中")


if __name__ == "__main__":
    main()
