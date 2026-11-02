#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_THINK_014 竞赛排行榜 TOP10 —— 薄壳校验脚本（完全不支持件）。

UI：TechCompetition.jsx:323 Card title="竞赛排行榜 TOP10"
（Table columns=rankingColumns :98-136：排名/团队/项目名称/得分；
dataSource=competitionRankings mock 10 条，mockData.js:271-283）。
数据：排行=排序面，依托「竞赛得分（团队×竞赛×分数）+ 竞赛主档」
双前提——竞赛主档三源 0 表（competition 词族全语义错位），
团队得分面三源 0 表（score 命中为企业评分/人才评分语义错位），
mock score 98.5-89.9 为演示序列。依托评分零承载 → 随动零承载。
"""
from __future__ import annotations

import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP1 = os.path.join(BASE, "_snapshots", "_shared_s309_think_beta_probe_out.json")
SNAP2 = os.path.join(BASE, "_snapshots", "_shared_s309_think_beta_probe2_out.json")
OUT = os.path.join(BASE, "M_SCIUI_THINK_014_out.json")

VERDICT = "完全不支持"


def main() -> None:
    s1 = json.load(open(SNAP1, encoding="utf-8"))
    s2 = json.load(open(SNAP2, encoding="utf-8"))
    dev1, gkx1, jx1 = s1["dev"], s1["gkx"], s1["jiuxin"]
    jx2 = s2["jiuxin"]

    # ---- 快照一致性断言（B11）----
    assert dev1["dev_table_total"] == 542 and gkx1["gkx_table_count"] == 280
    assert jx1["jiuxin_table_count_live"] == 218

    # ---- 竞赛主档 0 表断言（语义错位清单）----
    dev_hits = dict(dev1["dev_table_name_hits"])
    dev_comp_tables = sorted(k for k, v in dev_hits.items() if "competition" in v)
    gkx_hits = dict(gkx1["gkx_table_name_hits"])
    gkx_comp_tables = sorted(k for k, v in gkx_hits.items() if "competition" in v)
    jx_hits = dict(jx1["jiuxin_table_name_hits"])
    jx_comp_tables = sorted(k for k, v in jx_hits.items() if "competition" in v)
    assert gkx_comp_tables == []
    assert "ads_research_problem_competition_rank" in jx_comp_tables

    # ---- jiuxin 科研问题竞争排名语义错位断言（二期/三期）----
    assert jx2["jx_rp_compet_rank_rows"] == 46835
    cols = jx2["jx_rp_compet_rank_columns"]
    assert "competition_scope" in cols and "ranking_dimension" in cols

    # ---- mock TOP10 序列断言（读源文件）----
    ui_src = os.path.join(BASE, "..", "..", "..", "..", "..", "..",
                          "repos", "demo-ui-science", "src", "pages",
                          "tech-service", "mockData.js")
    with open(ui_src, encoding="utf-8") as f:
        mock_txt = f.read()
    assert "竞赛排行榜" in mock_txt
    assert mock_txt.count("rank: ") >= 10
    assert "QuantumForce" in mock_txt and "score: 98.5" in mock_txt

    out = {
        "metric_id": "M_SCIUI_THINK_014",
        "batch": "S3-09",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/tech-service/TechCompetition.jsx:323",
            "repos/demo-ui-science/src/pages/tech-service/TechCompetition.jsx:98-136",
            "repos/demo-ui-science/src/pages/tech-service/mockData.js:271-283",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "srs_anchor": "科技竞赛.md 序号 592 成绩榜单接口（『为成绩排行榜、参赛行为等提供独立数据接口』——榜单上位叶）；序号 585 参赛社区内容结构化整合（『将参赛者数据、参与记录、论坛发言、排行榜等内容关联归档』）；SRS 无 TOP10 指标",
            "note": "THINK 系为 UI 侧指标编号族，SRS 无此编号",
        },
        "facts": {
            "ui_mount": "TechCompetition.jsx:323 <Card title='竞赛排行榜 TOP10'> Table（rankingColumns :98-136：排名 rank/团队 team+institution/项目名称 project/得分 score；前三名 Trophy 徽标 :103-109）dataSource=competitionRankings，pagination=false 固定 10 行",
            "ui_mock_note": "ui_demo_fallback：mockData.js:271-283 competitionRankings 10 条，rank 1-10 团队 QuantumForce/DeepMindLab/BioInnovators/DataWizards/RoboMasters/NeuralNets/GreenTech/CodeBreakers/SpaceExplorers/MedTechPro，score 98.5→89.9 递减，institution 清华/北大/中科院/复旦/哈工大/浙大/上海交大/中科大/北航/中山大学——静态演示，不参与支持度结论",
            "ui_neighbors": "排行榜 tab（TrophyOutlined）左栏榜单+右栏竞赛类型分布饼图（CONTEST_001 域）；同 tab 另有社区讨论",
            "ranking_prereq_note": "排行的两前提：①排序键=竞赛评审得分（团队×竞赛×分数）；②排序域=竞赛主档（哪场赛、哪届）。THINK_003（竞赛项目评审得分）探针已证 score 面零承载；本件探针独立复核竞赛主档侧",
            "competition_host_note": "竞赛主档三源 0 表：dev 7 张 competition 命中全语义错位（chain_competitiveness 产业链竞争力/enterprise_ranking/enterprise_score/svc_tech_power_score 企业评分族/policy_support_rank 政策排名/cms_pano_competitive_position 竞争定位）；gkx 0 张；jiuxin 4 张（research_problem_competition_rank 科研问题竞争排名 + talent 评分 demo 表 3 张）——无一张科技赛事主档",
            "jiuxin_rp_rank_note": "jiuxin ads_research_problem_competition_rank（46,835 行）最近邻结构复核：competition_scope=CITY 22,445/PROVINCE 16,725/COUNTRY 7,370/DISTRICT 295；ranking_dimension=FRONTIER_LEADERSHIP/RESEARCH_SUBJECT_TOTAL/INVESTMENT/OVERALL_COMPETITION/RESEARCH_HEAT 各 9,367——按城市/省份对科研问题（rp_*）竞争力排名，subject 是城市/机构非参赛团队，无竞赛得分语义",
            "score_semantic_note": "dev score 词族命中（enterprise_score/svc_tech_power_score/industry_chain_region_scorecard）全为企业/产业链评分面，S3-08 INCUB_043/047 已证评分模型域双缺；团队竞赛得分（评审打分）三源 0 表",
            "dev_table_total": dev1["dev_table_total"],
            "gkx_table_count": gkx1["gkx_table_count"],
            "jiuxin_table_count_live": jx1["jiuxin_table_count_live"],
        },
        "derived": [
            {
                "name": "competition_top10_negative",
                "value": None,
                "note": "负结论登记：TOP10 榜单需「团队得分面（可排序键）+ 竞赛主档（排序域）」双前提，三源双面零承载（score 命中为企业评分语义错位、competition 命中为科研问题竞争排名语义错位），禁伪公式；排序本身（ORDER BY score DESC LIMIT 10）是零成本操作，缺的是排序键数据",
            },
        ],
        "absence_probe": [
            {"probe": "dev 542 表 compet/contest/award/rank/score/prize 词族（表名+列名双扫 information_schema 全 gkxlumenx% schema）",
             "source": "dev", "hits": dev_comp_tables,
             "note": "7 张命中全语义错位：产业链竞争力/企业评分排名族/政策排名/竞争定位文案——无科技赛事主档、无团队得分表"},
            {"probe": "gkx 280 表 competition 词族（表名+列名双扫）", "source": "gkx",
             "hits": gkx_comp_tables,
             "note": "表名 0 命中——供应商要素库无赛事域"},
            {"probe": "jiuxin 218 表（SHOW TABLES 实数）competition 词族（表名+列名逐表 DESCRIBE）", "source": "jiuxin",
             "hits": jx_comp_tables,
             "note": "4 张命中：ads_research_problem_competition_rank（46,835 行）为科研问题×城市/机构竞争力排名（scope/dimension 实测分布留证），3 张 talent 评分 demo 表——无科技赛事得分面"},
        ],
        "support_judgment": VERDICT,
        "notes": [
            "判档理由：排行榜是排序面，排序操作零成本，判档只看排序键与排序域两前提。团队竞赛得分（排序键）三源 0 表——score 词族命中全为企业/产业链评分（enterprise_score 族，S3-08 INCUB_043/047 已证评分模型域双缺，本件独立复核）；竞赛主档（排序域）三源 0 表——competition 命中全语义错位。双前提皆缺，判完全不支持。",
            "jiuxin ads_research_problem_competition_rank（46,835 行）是结构最近邻：有 ranking/ranked_subject_count/score 类 metric_value 列，但实测 scope=CITY/PROVINCE/COUNTRY/DISTRICT、dimension=前沿引领/主体总数/投入/综合竞争/研究热度——它回答『哪个城市在某个科研问题上竞争力强』，subject 是城市/机构非参赛团队，与科技竞赛团队榜语义完全错位，禁作代理。",
            "与 THINK_013（报名数）同宿主缺：竞赛主档 0 表导致整页竞赛族全零承载；与 THINK_003（竞赛项目评审得分）构成键-榜对：003 缺排序键、本件缺键+域，均独立留证。",
            "mock 10 条榜单（QuantumForce 98.5 → MedTechPro 89.9）为静态演示，ui_demo_fallback 披露，不参与支持度结论。",
            "升档路径：竞赛评审系统落库（团队×竞赛×评审得分）→ 完全转换支持（ORDER BY 得分 DESC LIMIT 10 即得）；赛事平台 API 直连（Kaggle leaderboard）→ 完全直接支持。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021", "2022", "2023", "2024", "2025", "2026"],
        "base_years_note": "无任何真实竞赛得分/榜单数据（双前提零承载）；基期无从谈起，全空登记。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted({
            "0", "3", "4", "7", "10", "218", "280", "542",
            "98.5", "89.9", "46835", "22445", "16725", "7370", "295", "9367",
            "2021", "2022", "2023", "2024", "2025", "2026",
        })},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment:", VERDICT)


if __name__ == "__main__":
    main()
