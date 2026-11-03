#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INCUB_050 技术路径强度（关键路径维度）—— 薄壳校验脚本（负结论件）。

UI：SpaceTimeEvolutionPage.jsx:1840 路径控制面板「路径强度」筛选组
（pathStrengthOptions 高/中/低）+ :294 路径抽屉 metrics 首项
{ label: 路径强度, value: entity.score, hint: scoreUnit }（mock 96/88/82）。
路径强度=区域间技术流动路径的强度评分（0-100 自设分制）。
探针：dev path 词族 2 表（sys_route_conf 系统路由配置语义错位/chain_roadmap
0 行产业链路线图）；gkx path 词族 0 表；久新 path 词族 2 表
（ads_research_problem_research_path 研发路径/ads_technology_evolution_path_step
技术演化路径步骤）为技术主题演化域非区域流动路径域——区域流动路径强度面三源零承载。
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SHARED = "_snapshots/_shared_s308_lane_a_out.json"
OUT = "M_SCIUI_INCUB_050_out.json"


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        snap = json.load(f)

    dev = snap["dev"]
    gkx = snap["gkx"]
    jx = snap["jiuxin"]
    assert dev["table_total"] == 542 and gkx["table_count"] == 280
    assert jx["table_count_live"] == 218
    assert dev["word_path"] == ["gkxlumenx.sys_route_conf", "gkxlumenx_ads.chain_roadmap"]
    assert gkx["word_path"] == []
    assert jx["word_path"] == ["ads_research_problem_research_path", "ads_technology_evolution_path_step"]

    out = {
        "metric_id": "M_SCIUI_INCUB_050",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview/modules/space-time-evolution/components/SpaceTimeEvolutionPage.jsx:1840",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/space-time-evolution/components/SpaceTimeEvolutionPage.jsx:294",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/space-time-evolution/mock/spaceTimeEvolutionMock.js:82-86",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/space-time-evolution/mock/spaceTimeEvolutionMock.js:316-318",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "「技术路径强度」指标名三份说明书未出现；INCUB 清单 row_01=605 语义注为科技知识图谱实体/连接规模统计（清单语义归知识图谱域，本件按 UI 实挂载=时空演进路径强度域留证）；挂载位=SpaceTimeEvolutionPage.jsx:1840+:294（清单定位）。",
        },
        "facts": {
            "ui_mount_filter": "SpaceTimeEvolutionPage.jsx:1840 pathLayerPanel pathStrength 筛选组（items=pathStrengthItems，三档高/中/低，mock :82-86 pathStrengthOptions）——路径强度作为路径筛选维度",
            "ui_mount_drawer": ":294 buildDrawerMetrics 路径实体分支首项 { label: 路径强度, value: String(entity.score), hint: entity.scoreUnit }——路径详情抽屉强度读数（scoreUnit=强度）",
            "ui_mock_scores": "mock paths[].score/strength（:316-318 南山->宝安 96 / :357-359 南山->坪山 88 / :396-399 光明->南山 82）+ driverFactors 四因子（政策支持/产业集聚/人才吸引/资本活跃，值 49-80）——0-100 自设分制",
            "ui_strength_semantics": "路径=区域间技术流动链路（source/target 城市对 + coords + badges 论文/专利），强度 score 隐含多维合成（driverFactors）但无权重定义",
            "ui_mock_note": "mock score 96/88/82 与四因子值为演示常量，不参与支持度结论（ui_demo_fallback）",
            "dev_table_total": dev["table_total"],
            "dev_path_word_tables": dev["word_path"],
            "dev_chain_roadmap": {"rows": 0, "note": "gkxlumenx_ads.chain_roadmap 0 行（产业链技术路线图域，非区域流动路径）——快照词族命中"},
            "gkx_table_count": gkx["table_count"],
            "gkx_path_word_tables": gkx["word_path"],
            "jiuxin_table_count_live": jx["table_count_live"],
            "jiuxin_path_word_tables": jx["word_path"],
            "jiuxin_path_note": "久新 path 词族 2 表均为技术主题演化域：ads_research_problem_research_path（科研问题研发路径）/ads_technology_evolution_path_step（技术演化路径步骤）——无区域对（source/target）与流动语义，非本件区域流动路径强度域",
            "jiuxin_mobility_note": "久新流动面 ads_talent_mobility_yearly_flow（51,489 行）为人才流动事件（flow_dimension/flow_level 五维分布），无路径强度评分列——流动事件原料≠路径强度结果面",
            "named_in_srs": False,
        },
        "derived": [
            {
                "name": "tech_path_strength_score",
                "value": None,
                "numerator": None,
                "denominator": None,
                "note": "技术路径强度 = 区域对技术流动路径的强度评分（0-100，UI 隐含政策/产业/人才/资本四因子合成）。路径强度事实面（区域对×强度值）与评分模型三源零承载 → 不可构建，负结论 null 登记",
            },
        ],
        "absence_probe": [
            {"probe": "dev path 词族（542 表）",
             "source": "dev", "sql": "information_schema 表名扫描（快照）",
             "hits": 2,
             "hit_detail": "gkxlumenx.sys_route_conf=系统路由配置（语义错位）；gkxlumenx_ads.chain_roadmap=产业链技术路线图 0 行（域错位：链路线图非区域流动路径）——区域流动路径强度域 0 有效命中"},
            {"probe": "gkx path 词族（280 表）",
             "source": "gkx", "sql": "information_schema 表名扫描（快照）",
             "hits": 0, "note": "gkx word_path=[]——要素库无路径面"},
            {"probe": "久新 path 词族（SHOW TABLES 实数 218 表）",
             "source": "jiuxin", "sql": "SHOW TABLES + 词族扫描（快照）",
             "hits": 2,
             "hit_detail": "ads_research_problem_research_path/ads_technology_evolution_path_step 均为技术主题演化域（问题→路径/技术→步骤），无区域对与流动语义——域错位"},
            {"probe": "路径强度评分模型（四因子/权重）",
             "source": "doc", "sql": "三份说明书 rg 路径强度|技术路径",
             "hits": 0,
             "hit_detail": "指标名与模型定义均 0 命中；UI driverFactors 四因子（政策支持/产业集聚/人才吸引/资本活跃）为 mock 自设，无权重"},
        ],
        "support_judgment": "完全不支持",
        "notes": [
            "判档理由：技术路径强度需①路径强度事实面（区域对×强度值）②强度模型（因子/权重）。dev path 词族 2 表逐一排除（系统路由语义错位/产业链路线图域错位且 0 行）；gkx 0；久新 2 表均为技术演化域无区域对语义；流动面 mobility_flow（51,489 行）有流动事件无强度评分。模型层 UI 四因子无权重定义——两层皆缺。",
            "域界定：本件按 UI 实挂载（时空演进页路径筛选/抽屉强度读数）界定为「区域间技术流动路径强度」；INCUB 清单语义注（知识图谱实体/连接规模）与 UI 挂载语义有偏差，以 UI 实挂载为准留证。",
            "同族关系：INCUB_051（路径强度变化，mock :638 图表）/INCUB_052（路径强度抬升幅度，mock :811 报表段）同 mock paths[].score 字段族——三件独立留证。",
            "久新技术演化路径域（research_path/evolution_path_step）若映射「技术路径」字面语义，可作另件调研（技术演化域），本件不挪用——语义锚定 UI 区域流动路径。",
            "升档路径：区域对流动强度面落库（mobility_flow 聚合区域对×强度）+ 强度模型立项 → 完全转换支持。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021-2026"],
        "base_years_note": "路径强度为当期截面读数（mock periodValues 2022-2026 演示）；三源无路径强度面无历史序列。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted([
            "96", "88", "82", "49", "80", "100", "51489", "51,489", "542", "280", "218", "2", "0"])},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 完全不支持 | 区域流动路径强度面三源零承载（词族 2+2 表均域错位）")


if __name__ == "__main__":
    main()
