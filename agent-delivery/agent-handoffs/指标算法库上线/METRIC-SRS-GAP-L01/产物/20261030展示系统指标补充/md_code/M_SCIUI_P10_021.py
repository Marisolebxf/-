#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_P10_021 用户评价与满意度报告 —— 薄壳校验脚本（完全不支持件）。

UI：IncubationCarrierNewPage.jsx:1330「用户评价与满意度报告」SectionCard
（:1339-1353 大读数+五星+样本+优劣项归纳）。
与 P10_008（企业满意度 M_IC_SATISFACTION）同卡同根（评价流零承载）——
P10_008 聚焦 KpiTile 摘要位（:1505），本件聚焦报告卡主体（:1330 区块，
含优劣项文本归纳面）；SOFTSCI_012 先证；独立留证。
"""
from __future__ import annotations

import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(BASE, "_snapshots", "_shared_s308_laneb_probe_out.json")
OUT = os.path.join(BASE, "M_SCIUI_P10_021_out.json")

VERDICT = "完全不支持"


def main() -> None:
    snap = json.load(open(SNAP, encoding="utf-8"))
    dev, gkx, jx = snap["dev"], snap["gkx"], snap["jiuxin"]

    dev_hits = dict(dev["dev_table_name_hits"])
    dev_sat_tables = sorted(k for k, v in dev_hits.items() if "satisfaction" in v)

    assert dev["dev_table_total"] == 542 and gkx["gkx_table_count"] == 280
    assert jx["jiuxin_table_count_live"] == 218

    out = {
        "metric_id": "M_SCIUI_P10_021",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview-new/incubation-carrier-new/IncubationCarrierNewPage.jsx:1330",
            "repos/demo-ui-science/src/pages/achievement-preview-new/incubation-carrier-new/IncubationCarrierNewPage.jsx:1345-1353",
            "repos/demo-ui-science/src/pages/achievement-preview-new/incubation-carrier-new/mockData.js:828-834",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "srs_anchor": "创新载体孵化载体.md 序号 556「用户评价与满意度报告」——本件即该功能叶的 UI 落位报告卡主体（需规描述：循环收集企业用户评价和满意度评分，自动归纳服务优劣项及改进建议）",
            "note": "本件与 P10_008 同挂序号 556：P10_008=KpiTile 摘要位（M_IC_SATISFACTION 编号），本件=报告卡主体（评分+优劣项归纳双面）",
        },
        "facts": {
            "ui_mount": "IncubationCarrierNewPage.jsx:1330 SectionCard title=用户评价与满意度报告（extra=MetricInfo 企业满意度口径自述+MockBadge）；:1339-1343 左栏大读数 operations.satisfaction.score（4.6）+Rate 五星+样本 386 份；:1345-1351 右栏优势项归纳 4 Tag（绿）/改进建议 3 Tag（橙）",
            "ui_report_faces": "报告卡双面：①评分面（score/responses）；②文本归纳面（advantages/improvements——SRS「自动归纳服务优劣项」的落位）",
            "ui_mock_note": "ui_demo_fallback：mock 4.6 分/386 份/优势 4 项（导师辅导响应及时/空间与配套完善/投融资对接高效/政策解读到位）/改进 3 项（申报节点提醒不够前置/跨区资源联动不足/活动报名渠道分散）——MetricInfo 自述即带（演示数据）",
            "dev_satisfaction_word_tables": dev_sat_tables,
            "dev_satisfaction_semantic_note": "code_operating_status（经营状态码）/evaluation_template（8 行模板配置无数据行）/policy_public_opinion+policy_simulation_result（政策舆情演示列）——无问卷评价面；与 P10_008 同扫同判",
            "jiuxin_sentiment_note": "ads_talent_media_sentiment_assessment 为人才媒体舆情情感（对象=人才新闻），非在孵企业对载体的问卷评价；语义双错位（主体+客体）",
            "sibling_verdicts": "P10_008（同卡 KpiTile 位）+SOFTSCI_012（满意度分布先证）同判完全不支持；本件为报告卡主体位独立留证",
            "dev_table_total": dev["dev_table_total"],
            "gkx_table_count": gkx["gkx_table_count"],
            "jiuxin_table_count_live": jx["jiuxin_table_count_live"],
        },
        "derived": [
            {
                "name": "satisfaction_report_negative",
                "value": None,
                "note": "负结论登记：报告卡双面（评分面+文本归纳面）原料同缺——评分需问卷评价行，归纳需评论文本流；三源零承载，禁伪公式",
            },
        ],
        "absence_probe": [
            {"probe": "dev 542 表 satisfaction/survey/rating/feedback/evaluat 词族（表名+列名双扫）", "source": "dev",
             "hits": dev_sat_tables,
             "note": "经营状态/模板配置/政策舆情语义污染——无问卷评价表（与 P10_008 同扫）"},
            {"probe": "gkx 280 表 satisfaction 词族", "source": "gkx",
             "hits": ["dwd_high_tech_industry_bonds", "dwd_org_annual_financial_info", "dwd_foreign_org_annual_financial_info", "dwd_org_stock_finance_info"],
             "note": "债券/机构财务评级 rating 列污染"},
            {"probe": "jiuxin 218 表（SHOW TABLES 实数）satisfaction/评价词族", "source": "jiuxin",
             "hits": [],
             "note": "表名 0 命中；人才情感评估表语义双错位（主体=新闻客体=人才，非企业→载体）"},
        ],
        "support_judgment": VERDICT,
        "notes": [
            "判档理由：报告卡双面零承载——评分面（企业×载体×评分×批次）与文本归纳面（评价原文流）三源均无：dev 词族污染（经营状态/模板配置/政策舆情），gkx 金融评级污染，jiuxin 人才舆情语义双错位。",
            "本件与 P10_008 同卡同 SRS 叶 556 不同挂点：P10_008=页尾 KpiTile 摘要位（:1505），本件=报告卡主体（:1330，优劣项归纳面是本件独有侧）；两件独立留证。",
            "「自动归纳服务优劣项」需 NLP 对评价原文聚类——原文流零承载则归纳面无从谈起（比评分面更深一层缺口）。",
            "SOFTSCI_012（1-5 星分布）为先证件（S3-07 批）；本批 P10_008/021 复判成立，三件互为佐证。",
            "升档路径：载体服务平台问卷模块接入（评分行+评价文本双入湖）→ 评分面完全转换支持+归纳面 NLP 可做。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021", "2022", "2023", "2024", "2025", "2026"],
        "base_years_note": "无任何真实评价数据（mock 仅 2026 上半年演示批次）；基期无从谈起，全空登记。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted({
            "4.6", "386", "5", "4", "3", "8", "0", "542", "280", "218", "2026", "1330", "1505",
        })},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment:", VERDICT)


if __name__ == "__main__":
    main()
