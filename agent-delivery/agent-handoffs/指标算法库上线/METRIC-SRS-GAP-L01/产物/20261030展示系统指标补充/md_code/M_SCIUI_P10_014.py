#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_P10_014 单位贡献度（M_SS_UNIT_CONTRIB）—— 薄壳校验脚本（完全不支持件）。

UI：BottomTabs.jsx:568「单位贡献度 Top8（点击柱条联动地图）」SectionCard。
口径：getContribution(t) = round(rating*20 + progress*0.4 + min(30, budget*0.15))
（BottomTabs.jsx:31，mock 自设权重）。
数据：贡献度三要素（课题 rating/进度/经费）随软科学课题库三源零承载——
dev 课题表 0 行空壳；gkx 无中文软科学课题面；jiuxin ads_project_profile
为 OpenAlex 英文资助项目（无 rating/progress 列，语义错位）。
"""
from __future__ import annotations

import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(BASE, "_snapshots", "_shared_s308_laneb_probe_out.json")
OUT = os.path.join(BASE, "M_SCIUI_P10_014_out.json")

VERDICT = "完全不支持"


def main() -> None:
    snap = json.load(open(SNAP, encoding="utf-8"))
    dev, gkx, jx = snap["dev"], snap["gkx"], snap["jiuxin"]

    assert dev["dev_table_total"] == 542 and gkx["gkx_table_count"] == 280
    assert jx["jiuxin_table_count_live"] == 218

    out = {
        "metric_id": "M_SCIUI_P10_014",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview-new/soft-science-new/BottomTabs.jsx:568",
            "repos/demo-ui-science/src/pages/achievement-preview-new/soft-science-new/BottomTabs.jsx:30-32",
            "repos/demo-ui-science/src/pages/achievement-preview-new/soft-science-new/mockData.js:96",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "srs_anchor": "软科学成果展示.md 序号 468「单位贡献度与空间分布统计」（需规描述：平台批量输出各单位、机构及区域的课题贡献度报表，多维图表联动地理分布地图）；另 1.2.x 成果优选「按立项时间、贡献度…排序」为消费侧上位",
            "note": "M_SS_UNIT_CONTRIB 为 UI 侧指标编号（MetricInfo 自带）；SRS 无此编号",
        },
        "facts": {
            "ui_mount": "BottomTabs.jsx:568 SectionCard title=单位贡献度 Top8（点击柱条联动地图）（MetricInfo title=单位贡献度（M_SS_UNIT_CONTRIB）口径自述：承担单位贡献度合计（影响力×20+进度×0.4+经费权重）+ MockBadge）；unitBarOption 柱图 onEvents click handleUnitClick 联动地图；邻卡区域贡献度 Top8（M_SS_REGION_CONTRIB）",
            "ui_formula": "BottomTabs.jsx:30-32 getContribution(t) = Math.round(t.rating*20 + t.progress*0.4 + Math.min(30, (t.budget||0)*0.15))（注释：与列表页口径一致（演示））",
            "ui_build": "BottomTabs.jsx:62-99 buildContributionSheets(topics)：unitMap/typeMap/regionMap 三聚合，按 contribution 降序",
            "ui_mock_note": "ui_demo_fallback：mock SOFT_TOPICS 课题 rating 4.2-4.9/progress 18-100/budget 55-120 万元——三要素全演示，权重 20/0.4/0.15 为自设",
            "dev_topic_tables": "gkxlumenx_ods.fund_project（7 列 0 行空壳）/gkxlumenx_dwd.enterprise_fund_project（9 列 0 行空壳）",
            "gkx_topic_note": "280 表无中文软科学课题面（dwd_en_project 为英文资助项目 20,000 行，无 rating/progress/承担单位评分列）",
            "jiuxin_project_note": "ads_project_profile 1,838,841 行为 OpenAlex 资助项目画像（funder/amount/start_year 等 46 列）——无 rating（专家评分）无 progress（进度%）列，软科学语义错位；无承担单位贡献度汇总面",
            "contribution_like_columns": [],
            "dev_table_total": dev["dev_table_total"],
            "gkx_table_count": gkx["gkx_table_count"],
            "jiuxin_table_count_live": jx["jiuxin_table_count_live"],
        },
        "derived": [
            {
                "name": "unit_contribution_negative",
                "value": None,
                "note": "负结论登记：贡献度=Σ(课题 rating/progress/budget 加权)，三要素随软科学课题库零承载，库内无构建路径，禁伪公式",
            },
        ],
        "absence_probe": [
            {"probe": "dev 542 表 soft/topic/subject/project 词族 + 贡献度三要素列扫", "source": "dev",
             "hits": ["gkxlumenx_ods.fund_project", "gkxlumenx_dwd.enterprise_fund_project", "gkxlumenx_dwd.enterprise_fund_project 同族"],
             "rows": 0,
             "note": "课题表全空壳（0 行）；无 rating/progress 贡献度列"},
            {"probe": "gkx 280 表贡献度词族（contrib/rating+progress 组合）", "source": "gkx",
             "hits": [],
             "note": "0 命中；dwd_en_project 20,000 行英文项目无评分/进度列"},
            {"probe": "jiuxin 218 表（SHOW TABLES 实数）contrib/贡献度词族", "source": "jiuxin",
             "hits": [],
             "note": "0 命中；ads_project_profile（1,838,841 行）为资助金额面，无课题评分/进度语义"},
        ],
        "support_judgment": VERDICT,
        "notes": [
            "判档理由：单位贡献度 = 承担单位全部课题的加权合计，权重三要素（影响力评分/进度/经费）全部挂在软科学课题库上——该库三源零承载（dev 空壳 0 行、gkx 无中文课题面、jiuxin 英文项目画像语义错位），宿主无则贡献度无。",
            "mock 权重（影响力×20+进度×0.4+经费×0.15 封顶 30）为演示自设，无权威出处；SRS 468 亦未给权重——正式口径需立项裁定（B10）。",
            "与 P10_004（互动统计）同宿主（软科学课题库零承载）不同侧面：本件缺课题评价要素，P10_004 缺行为流水；独立留证。",
            "jiuxin ads_project_profile 的 amount 列（资助金额）可算「单位获资助金额排名」但那是资金面不是贡献度（权重结构缺失），语义错位不冒用。",
            "升档路径：软科学课题库接入（含承担单位+评分+进度+经费四列）→ 完全转换支持；权重口径立项裁定后生效。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021", "2022", "2023", "2024", "2025", "2026"],
        "base_years_note": "无任何真实课题年度数据（mock 课题年份 2023-2026 演示段）；基期无从谈起，全空登记。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted({
            "20", "0.4", "0.15", "30", "8", "0", "20000", "20,000", "1838841", "1,838,841",
            "542", "280", "218", "4.2", "4.9", "18", "100", "55", "120",
        })},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment:", VERDICT)


if __name__ == "__main__":
    main()
