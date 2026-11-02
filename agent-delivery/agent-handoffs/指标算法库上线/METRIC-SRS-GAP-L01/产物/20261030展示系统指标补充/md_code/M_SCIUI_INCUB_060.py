#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INCUB_060 高价值成果榜单 —— 薄壳校验脚本（负结论件）。

UI：softScienceHomepageMock.js:548 证据与明细面板 records[0]
{ id: evidence-ranking, title: 高价值成果榜单, source: 市级成果库, note: 直接支撑
热点成果榜排序和重点城市贡献度判断 }；榜单排序键=成果 impactIndex/influenceScore
（mock :602 impactIndex 96/热度 9.4；工作台 influenceScore 排序列）。
探针：dev achievement 词族（org_achievement_year 0 行）；gkx achiev/award 0 表；
久新 ads_research_outcome_* 20 表（快照行数）为科研产出评价面（评估维度分/
学科归属/预测值列族，无软科学成果主档语义——INCUB_022/TECHTRK_011 先例语义
排除）——高价值软科学成果榜单面三源零承载。
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code")

SHARED = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/_snapshots/_shared_s308_lane_a_out.json"
OUT = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/M_SCIUI_INCUB_060_out.json"


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        snap = json.load(f)

    dev = snap["dev"]
    gkx = snap["gkx"]
    jx = snap["jiuxin"]
    assert dev["table_total"] == 542 and gkx["table_count"] == 280
    assert jx["table_count_live"] == 218
    ro = jx["research_outcome_rows"]
    assert ro["ads_research_outcome_profile"] == 342
    assert ro["ads_research_outcome_yearly_metric"] == 9055
    assert ro["ads_research_outcome_scope_yearly"] == 41153

    out = {
        "metric_id": "M_SCIUI_INCUB_060",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview/modules/soft-science/mock/softScienceHomepageMock.js:548",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/soft-science/mock/softScienceHomepageMock.js:601-605",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/soft-science/components/SoftScienceWorkbench.jsx:522-527",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "「高价值成果榜单」指标名三份说明书未出现；INCUB 清单 row_01=615（语义注：被评为高价值等级的数据资源占全部资源的比例——清单语义与 UI 榜单语义有偏差，以 UI 实挂载为准）；挂载位=softScienceHomepageMock.js:548（清单定位）。",
        },
        "facts": {
            "ui_mount": "softScienceHomepageMock.js:545-552 证据与明细面板 records[0] { id: evidence-ranking, title: 高价值成果榜单, source: 市级成果库, time: 2026-04-19 09:20, status: 已归档, note: 直接支撑热点成果榜排序和重点城市贡献度判断 }——榜单以证据记录形态挂载",
            "ui_ranking_keys": "榜单排序键=成果卡 impactIndex/热度（mock :601-605 result-nanshan-ai-manufacturing impactIndex=96、value=热度 9.4、signals 含高价值成果）+ 工作台 influenceScore 排序列（SoftScienceWorkbench.jsx:522-527 sorter=parseInfluenceScore，mock 影响力 43-99+）",
            "ui_impact_semantics": "高价值判定=impact: high 标签（mock hotspots :377-380 深圳南山 118 项成果·高价值成果密度最高）——高影响标签×影响力评分双锚",
            "ui_mock_note": "mock impactIndex 96/热度 9.4/influenceScore 43-99+/118 项 为演示常量，不参与支持度结论（ui_demo_fallback）；「市级成果库」source 为 mock 自设来源标注",
            "dev_table_total": dev["table_total"],
            "dev_achievement_note": "dev 542 表 achievement 词族命中 gkxlumenx_ads.org_achievement_year（paper_cnt/patent_apply_cnt/project_cnt/financing_cnt 年度成果面）0 行空壳——INCUB_022/TECHTRK_011 先例留证；无高价值等级/榜单语义列",
            "gkx_table_count": gkx["table_count"],
            "gkx_achievement_note": "gkx 280 表 achiev/award 词族 0 命中（TECHTRK_011 实跑留证——dwd_zh_journal.award 为期刊获奖语义排除）",
            "jiuxin_table_count_live": jx["table_count_live"],
            "jiuxin_research_outcome_rows": ro,
            "jiuxin_outcome_note": "久新 ads_research_outcome_* 20 表（profile 342/metric 3420/yearly_metric 9055/scope_yearly 41153/trend_case 22881 等）为科研产出评价面——列族为评估维度分/学科归属/预测值（dimension_score/weighted_contribution/forecast_value），无软科学成果主档与高价值榜单语义（INCUB_022/TECHTRK_011 先例语义排除，本批复用）",
            "jiuxin_value_note": "ads_talent_topic_value_summary/ads_talent_topic_value_evidence（word_value_rank 命中）为人才主题价值面非成果榜单；ads_technology_commercial_value_simulation 为技术商业化模拟面——均非软科学高价值成果榜单域",
            "named_in_srs": False,
        },
        "derived": [
            {
                "name": "high_value_softscience_outcome_ranking",
                "value": None,
                "numerator": None,
                "denominator": None,
                "note": "高价值成果榜单 = 软科学成果×高价值等级×排序键（影响力评分/热度）的排序面。软科学成果主档与高价值评定面三源零承载 → 榜单无从排起，负结论 null 登记",
            },
        ],
        "absence_probe": [
            {"probe": "dev 成果面（achievement 词族 542 表）",
             "source": "dev", "sql": "information_schema 扫描 + 行数实证（先例快照）",
             "hits": 1,
             "hit_detail": "gkxlumenx_ads.org_achievement_year（paper_cnt/patent_apply_cnt/project_cnt/financing_cnt）0 行——年度计数结构无高价值等级列、无软科学成果主档语义"},
            {"probe": "gkx achiev/award 词族（280 表）",
             "source": "gkx", "sql": "SHOW TABLES 词族扫描（TECHTRK_011 实跑留证）",
             "hits": 0,
             "hit_detail": "0 表命中；dwd_zh_journal.award 为期刊获奖（语义排除先例）——无成果榜单面"},
            {"probe": "久新 outcome/价值词族（SHOW TABLES 实数 218 表）",
             "source": "jiuxin", "sql": "SHOW TABLES + 词族扫描 + 行数（快照）",
             "hits": 23,
             "hit_detail": "ads_research_outcome_* 20 表为科研产出评价面（评估维度分/预测值列族，无软科学成果主档）；talent_topic_value 双表为人才主题价值；technology_commercial_value_simulation 为技术模拟——全部语义排除"},
            {"probe": "高价值评定标准（等级规则）",
             "source": "doc", "sql": "三份说明书 rg 高价值|影响力评分",
             "hits": 0,
             "hit_detail": "指标名与高价值评定规则均 0 命中；UI impact:high 标签与 influenceScore 43-99+ 为 mock 自设（99+ 上界披露为字符串排序陷阱）"},
        ],
        "support_judgment": "完全不支持",
        "notes": [
            "判档理由：高价值成果榜单需①软科学成果主档（成果×机构×年份×影响力）②高价值评定面（等级规则/评分）③排序呈现。dev org_achievement_year 0 行且无等级列；gkx achiev/award 0 表；久新 outcome 20 表为科研产出评价面（INCUB_022/TECHTRK_011 先例语义排除）——主档与评定面双缺，榜单无从排起。",
            "语义边界：本件为软科学成果域（UI 挂载软科学成果页）；gkx dwd_zh_paper/dwd_patent 等论文专利主档是科技成果实数据（TECHTRK_011 已证可算）但非软科学课题成果语义——不挪用。",
            "清单语义偏差披露（B10）：INCUB 清单语义注为「高价值等级数据资源占全部资源的比例」（占比语义，近 INCUB_059 高价值成果占比），UI 实挂载为榜单（排序面）——本件以 UI 实挂载（榜单）为准留证，占比口径归 059（非本批件）。",
            "UI mock 的 influenceScore 含 '99+' 字符串值（table-result-1）——parseInfluenceScore 排序存在字符串陷阱，正式版接数须数值化（B9）。",
            "升档路径：软科学成果库接入（课题成果主档+影响力评定落库）→ 完全转换支持；成果库接口直连 → 完全直接支持。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021-2026"],
        "base_years_note": "榜单为当期截面排序（mock timeBucket 2025/2026 演示）；三源无成果主档无历史榜单序列。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted([
            "96", "9.4", "118", "94", "43", "99", "342", "3420", "9055", "41153", "22881",
            "542", "280", "218", "20", "23", "2", "0"])},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 完全不支持 | 软科学成果主档与高价值评定面三源零承载")


if __name__ == "__main__":
    main()
