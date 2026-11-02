#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_P10_008 企业满意度（M_IC_SATISFACTION）—— 薄壳校验脚本（完全不支持件）。

UI：IncubationCarrierNewPage.jsx:1333「用户评价与满意度报告」SectionCard
（:1339-1343 大读数 4.6 + Rate 五星 + 样本 386 份；:1505 摘要卡 M_IC_SATISFACTION）。
数据：SOFTSCI_012 已证评价流零承载（同判复判）；本件独立留证——
satisfaction 词族三源命中全为语义污染（债券评级/经营状态/舆情模拟），
dev svc_org_card 0 行空壳；jiuxin 218 表 0 张问卷/评价面。
"""
from __future__ import annotations

import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(BASE, "_snapshots", "_shared_s308_laneb_probe_out.json")
OUT = os.path.join(BASE, "M_SCIUI_P10_008_out.json")

VERDICT = "完全不支持"


def main() -> None:
    snap = json.load(open(SNAP, encoding="utf-8"))
    dev, gkx, jx = snap["dev"], snap["gkx"], snap["jiuxin"]

    dev_hits = dict(dev["dev_table_name_hits"])
    dev_sat_tables = sorted(k for k, v in dev_hits.items() if "satisfaction" in v)
    gkx_hits = dict(gkx["gkx_table_name_hits"])
    gkx_sat_cols = {k: v for k, v in gkx["gkx_column_name_hits"].items()
                    if "satisfaction" in v}
    jx_hits = dict(jx["jiuxin_table_name_hits"])
    jx_sat_tables = sorted(k for k, v in jx_hits.items() if "satisfaction" in v)

    assert dev["dev_table_total"] == 542 and gkx["gkx_table_count"] == 280
    assert jx["jiuxin_table_count_live"] == 218

    out = {
        "metric_id": "M_SCIUI_P10_008",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview-new/incubation-carrier-new/IncubationCarrierNewPage.jsx:1333",
            "repos/demo-ui-science/src/pages/achievement-preview-new/incubation-carrier-new/IncubationCarrierNewPage.jsx:1505",
            "repos/demo-ui-science/src/pages/achievement-preview-new/incubation-carrier-new/mockData.js:828-834",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "srs_anchor": "创新载体孵化载体.md 序号 556「用户评价与满意度报告」（需规描述：支持循环收集企业用户评价和满意度评分，自动归纳服务优劣项及改进建议）",
            "note": "M_IC_SATISFACTION 为 UI 侧指标编号（KpiTile metricId）；SRS 无此编号",
        },
        "facts": {
            "ui_mount": "IncubationCarrierNewPage.jsx:1333 SectionCard title=用户评价与满意度报告（extra 含 MetricInfo title=企业满意度（M_IC_SATISFACTION）口径自述：2026 年上半年在孵企业满意度问卷 386 份满分 5 分 + MockBadge）；:1339-1343 大读数 operations.satisfaction.score + Rate 五星 + 样本 responses 份；:1347-1351 优劣项 Tag",
            "ui_summary_tile": "IncubationCarrierNewPage.jsx:1505 KpiTile label=企业满意度 value=4.6 unit=分 metricId=M_IC_SATISFACTION + Rate",
            "ui_mock_note": "ui_demo_fallback：mock 4.6 分/386 份/优势 4 项/改进 3 项均为演示设定，不参与判档",
            "dev_satisfaction_word_tables": dev_sat_tables,
            "dev_satisfaction_semantic_note": "gkxlumenx_dim.code_operating_status（经营状态码表）、gkxlumenx_topic_enterprise.evaluation_template（评价模板配置 8 行，无问卷数据）——非满意度评价面；gkxlumenx_ads.svc_org_card 0 行空壳（服务要素卡）",
            "gkx_satisfaction_column_tables": sorted(gkx_sat_cols),
            "gkx_satisfaction_semantic_note": "命中列全为 rating 类金融语义：dwd_high_tech_industry_bonds/dwd_sci_tech_inno_bonds（债券评级）、dwd_org_annual_financial_info（机构财务评级）——SOFTSCI_012 同族污染复判",
            "jiuxin_satisfaction_tables": jx_sat_tables,
            "jiuxin_satisfaction_note": "表名 0 命中；ads_talent_media_sentiment_assessment（媒体情感评估）/ads_talent_political_assessment_demo（demo 后缀演示表禁引）为人才域情感面非载体满意度",
            "sibling_verdict": "M_SCIUI_SOFTSCI_012（满意度分布）同判完全不支持——评价流零承载同根因；本件独立留证",
            "dev_table_total": dev["dev_table_total"],
            "gkx_table_count": gkx["gkx_table_count"],
            "jiuxin_table_count_live": jx["jiuxin_table_count_live"],
        },
        "derived": [
            {
                "name": "satisfaction_score_negative",
                "value": None,
                "note": "负结论登记：满意度均分需问卷评价面（评价主体企业+载体客体+评分+批次时间），三源零承载，禁伪公式",
            },
        ],
        "absence_probe": [
            {"probe": "dev 542 表 satisfaction/survey/rating/feedback/evaluat 词族（表名+列名双扫）", "source": "dev",
             "hits": dev_sat_tables,
             "note": "经营状态码表/评价模板配置/舆情模拟列（policy_public_opinion/policy_simulation_result 为政策域演示面）——无问卷评价表；svc_org_card 0 行"},
            {"probe": "gkx 280 表 satisfaction 词族", "source": "gkx",
             "hits": sorted(gkx_sat_cols),
             "note": "债券评级/机构财务评级语义污染（latest_bond_rating 等 rating 列）"},
            {"probe": "jiuxin 218 表（SHOW TABLES 实数）satisfaction 词族", "source": "jiuxin",
             "hits": jx_sat_tables,
             "note": "表名 0 命中；人才情感评估表语义不符（媒体舆情非在孵企业问卷）"},
        ],
        "support_judgment": VERDICT,
        "notes": [
            "判档理由：企业满意度需「在孵企业→载体」问卷评价面（主体+客体+评分+批次），三源零承载——dev 词族命中为经营状态码/评价模板配置（8 行模板无数据），gkx 为债券/财务评级污染，jiuxin 为人才媒体情感面语义不符。",
            "SOFTSCI_012（满意度分布，1-5 星）已证同根因零承载；本件（均分制 5 分）为复判+独立留证，两件判档一致互为佐证。",
            "火炬统计调查制度年报含在孵企业满意度问卷字段——属采集面非库内计算，需问卷系统对接。",
            "mock 口径自述「2026 年上半年问卷 386 份」为演示设定（MetricInfo 原文即带 MockBadge）。",
            "升档唯一路径：满意度问卷系统接入（载体服务平台的评价模块导出）落评价表 → 完全转换支持。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021", "2022", "2023", "2024", "2025", "2026"],
        "base_years_note": "无任何真实满意度数据（mock 仅 2026 上半年演示批次）；基期无从谈起，全空登记。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted({
            "4.6", "386", "5", "4", "3", "8", "0", "542", "280", "218", "2026",
        })},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment:", VERDICT)


if __name__ == "__main__":
    main()
