#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_THINK_013 数据科学赛道报名数 —— 薄壳校验脚本（完全不支持件）。

UI：TechCompetition.jsx:163-168 handleRegister 确认报名弹窗
（Modal.confirm onOk 仅 message.success 前端提示，无落库）；
清单 l3 名「确认报名＞数据科学」指 typeDistribution 饼图
数据科学扇区（:174 { value: 15, name: '数据科学' }）与报名
动作的合成语义。数据：报名流水域（用户×竞赛×赛道×时间戳）
三源零承载——enroll 词族命中全为污染：gkx enrollment_count
（临床试验入组人数）、registered_capital（注册资本）、
jiuxin early_entry_score（课题入场分）；竞赛主档三源 0 表
（competition 命中为 chain_competitiveness 产业链竞争力/
科研问题竞争排名语义错位）。
"""
from __future__ import annotations

import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP1 = os.path.join(BASE, "_snapshots", "_shared_s309_think_beta_probe_out.json")
SNAP2 = os.path.join(BASE, "_snapshots", "_shared_s309_think_beta_probe2_out.json")
SNAP4 = os.path.join(BASE, "_snapshots", "_shared_s309_think_beta_probe4_out.json")
OUT = os.path.join(BASE, "M_SCIUI_THINK_013_out.json")

VERDICT = "完全不支持"


def main() -> None:
    s1 = json.load(open(SNAP1, encoding="utf-8"))
    s2 = json.load(open(SNAP2, encoding="utf-8"))
    s4 = json.load(open(SNAP4, encoding="utf-8"))
    dev1, gkx1, jx1 = s1["dev"], s1["gkx"], s1["jiuxin"]
    gkx4, jx2 = s4["gkx"], s2["jiuxin"]

    # ---- 快照一致性断言（B11）----
    assert dev1["dev_table_total"] == 542 and gkx1["gkx_table_count"] == 280
    assert jx1["jiuxin_table_count_live"] == 218

    # ---- enroll 词族三源命中与语义裁定 ----
    dev_hits = dict(dev1["dev_table_name_hits"])
    dev_enroll_tables = sorted(k for k, v in dev_hits.items() if "enroll" in v)
    gkx_hits = dict(gkx1["gkx_table_name_hits"])
    gkx_enroll_tables = sorted(k for k, v in gkx_hits.items() if "enroll" in v)
    jx_hits = dict(jx1["jiuxin_table_name_hits"])
    jx_enroll_tables = sorted(k for k, v in jx_hits.items() if "enroll" in v)
    assert dev_enroll_tables == [] and gkx_enroll_tables == [] \
        and jx_enroll_tables == ["ads_institution_topic_entry"]
    # gkx 列名 enroll 命中语义污染断言（四期）
    assert gkx4["gkx_dwd_clinical_trial_enroll_cols"] == ["enrollment_count"]
    assert gkx4["gkx_dwd_forg_base_info_enroll_cols"] == [
        "registered_capital_currency_code", "registered_capital_value"]
    assert gkx4["gkx_dwd_org_base_info_enroll_cols"] == ["registered_capital_value"]
    # jiuxin 课题条目表语义断言（二期：OpenAlex 课题快照非报名）
    assert jx2["jx_topic_entry_rows"] == 3358401
    assert "openalex_topic_id" in jx2["jx_topic_entry_columns"]

    # ---- competition 词族语义错位断言 ----
    dev_comp_tables = sorted(k for k, v in dev_hits.items() if "competition" in v)
    jx_comp_tables = sorted(k for k, v in jx_hits.items() if "competition" in v)

    out = {
        "metric_id": "M_SCIUI_THINK_013",
        "batch": "S3-09",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/tech-service/TechCompetition.jsx:163-168",
            "repos/demo-ui-science/src/pages/tech-service/TechCompetition.jsx:174",
            "repos/demo-ui-science/src/pages/tech-service/mockData.js:265-270",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "srs_anchor": "科技竞赛.md 序号 588 竞赛发布与组织（『提供竞赛活动全流程的组织支持』——报名流程上位叶）；序号 584 竞赛项目数据归集与分类（赛事主档上位叶）；SRS 无报名数指标",
            "note": "THINK 系为 UI 侧指标编号族，SRS 无此编号",
        },
        "facts": {
            "ui_mount": "TechCompetition.jsx:163-168 handleRegister → Modal.confirm({ title: '确认报名', content: 竞赛名, onOk: message.success('报名成功！请查看报名确认邮件。') })——纯前端提示，无任何接口调用/落库动作；竞赛卡报名按钮 :86-91",
            "ui_track_context": "TechCompetition.jsx:173-180 typeDistribution 饼图首扇区 { value: 15, name: '数据科学' }（mock 15 场数据科学类赛事）；竞赛卡 teams/participants 字段（mock comp1 数据科学赛 1200 队 5600 人）——清单 l3「确认报名＞数据科学」= 报名动作×数据科学赛道的合成指标",
            "ui_mock_note": "ui_demo_fallback：mockData.js:265-270 competitions 6 条（数据科学/AI/创新创业/量子计算/生物医药/机器人），participants 演示值 5600/3200/2800/0/0/4500；typeDistribution 数据科学 15——全为静态演示，不参与支持度结论",
            "dev_enroll_word_tables": dev_enroll_tables,
            "dev_enroll_note": "dev 542 表 enroll/register/signup/apply/entry 词族表名 0 命中；报名流水零预置",
            "gkx_enroll_word_tables": gkx_enroll_tables,
            "gkx_enroll_semantic_note": "gkx 280 表表名 0 命中；列名命中全为污染：dwd_clinical_trial.enrollment_count（临床试验入组人数）、dwd_forg_base_info/dwd_org_base_info.registered_capital（注册资本）——无一处赛事报名语义",
            "jiuxin_enroll_tables": jx_enroll_tables,
            "jiuxin_enroll_semantic_note": "jiuxin 218 表（SHOW TABLES 实数）表名命中 1 张 ads_institution_topic_entry（3,358,401 行）——entry=OpenAlex 课题条目快照（列含 openalex_topic_id/observed_paper_count），机构×课题×年度观测面，非用户报名流水；列名 early_entry_score（课题入场分）同族污染",
            "competition_host_note": "竞赛主档三源 0 表：dev competition 词族命中全为 chain_competitiveness（产业链竞争力）/enterprise_ranking/score（企业评分）/policy_support_rank（政策排名）语义错位；jiuxin 4 张 competition 命中为 ads_research_problem_competition_rank（科研问题区域竞争排名，46,835 行，competition_scope=CITY/PROVINCE/COUNTRY）与人才评分 demo 表——无一张科技赛事主档",
            "register_action_note": "UI 报名动作本身无后端（handleRegister 仅前端 message），报名流水连演示落库链路都没有",
            "dev_table_total": dev1["dev_table_total"],
            "gkx_table_count": gkx1["gkx_table_count"],
            "jiuxin_table_count_live": jx1["jiuxin_table_count_live"],
        },
        "derived": [
            {
                "name": "datascience_track_registrations_negative",
                "value": None,
                "note": "负结论登记：赛道报名数需「竞赛主档（含赛道/类型字段）+报名事件流水（用户×竞赛×时间戳）」双面，三源竞赛主档 0 表、报名流水 0 表，禁伪公式",
            },
        ],
        "absence_probe": [
            {"probe": "dev 542 表 enroll/register/signup/apply/entry 词族（表名+列名双扫 information_schema 全 gkxlumenx% schema）",
             "source": "dev", "hits": dev_enroll_tables, "rows": 0,
             "note": "表名 0 命中——报名流水零预置；竞赛主档 competition 词族命中全为产业链竞争力/企业评分语义错位"},
            {"probe": "gkx 280 表 enroll 词族（表名+列名双扫）", "source": "gkx",
             "hits": gkx_enroll_tables,
             "note": "表名 0 命中；列名命中全为污染（临床试验入组 enrollment_count/注册资本 registered_capital），无赛事报名语义"},
            {"probe": "jiuxin 218 表（SHOW TABLES 实数）enroll 词族（表名+列名逐表 DESCRIBE）", "source": "jiuxin",
             "hits": jx_enroll_tables,
             "note": "唯一命中 ads_institution_topic_entry 为 OpenAlex 课题条目快照（335.8 万行，entry=条目非报名）；competition 词族命中为科研问题竞争排名（46,835 行）非科技赛事"},
        ],
        "support_judgment": VERDICT,
        "notes": [
            "判档理由：赛道报名数需要两个前提面——竞赛主档（含赛道/类型字段，可筛『数据科学』）与报名事件流水（用户×竞赛×时间戳）。竞赛主档三源 0 表（competition 词族命中全为产业链竞争力/科研问题竞争排名语义错位）；报名流水三源 0 表（enroll 词族命中全为临床试验入组/注册资本/课题条目污染）。双面皆缺，判完全不支持。",
            "UI 报名动作本身是纯前端演示：handleRegister 的 Modal.confirm onOk 仅 message.success 提示，无接口调用无落库——即使平台上线，报名数据也无采集链路，需与后端一并立项。",
            "与 THINK_014（竞赛排行榜 TOP10）同宿主缺：竞赛主档 0 表导致整页竞赛域（THINK_003/004/005/013/014 及 CONTEST_001）全族零承载，本件为报名流水子面独立留证。",
            "mock 6 条竞赛（participants 0-5600）与 typeDistribution（数据科学 15）为静态演示值，ui_demo_fallback 披露，不参与支持度结论。",
            "升档路径：竞赛主档接入（SRS 序号 584 赛事归集）+ 报名事件表落库（序号 588 全流程组织支持）→ 完全转换支持；赛事平台 API 直连（如 Kaggle 类平台报名接口）→ 完全直接支持。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021", "2022", "2023", "2024", "2025", "2026"],
        "base_years_note": "无任何真实报名数据（竞赛主档与报名流水双零承载）；基期无从谈起，全空登记。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted({
            "0", "1", "4", "6", "15", "218", "280", "542",
            "5600", "3200", "2800", "4500",
            "3358401", "46835", "1200",
            "2021", "2022", "2023", "2024", "2025", "2026",
        })},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment:", VERDICT)


if __name__ == "__main__":
    main()
