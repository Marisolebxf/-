#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_THINK_003 竞赛项目评审得分（project score）—— 薄壳校验脚本（负结论件）。

UI：TechCompetition.jsx:131 排行榜 Tab「竞赛排行榜 TOP10」表格得分列
（dataIndex=score，mockData.js:273-283 competitionRankings 十行 98.5→89.9）。
口径=竞赛项目按评价模型算出的分数——竞赛评审面（项目×评委×得分）+
评价模型双缺；竞赛台账本身三源零承载（CONTEST_001 已证，本件独立留证）。
"""
from __future__ import annotations

import json

SHARED = "_snapshots/_shared_s309_alpha_out.json"
OUT = "M_SCIUI_THINK_003_out.json"


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        snap = json.load(f)

    dev = snap["dev"]
    gkx = snap["gkx"]
    jx = snap["jiuxin"]
    assert dev["table_total"] == 542 and gkx["table_count"] == 280
    assert jx["table_count_live"] == 218
    # 竞赛词族：dev 0 表 / gkx 0 表 / jiuxin 2 表（学术竞争度异域）
    assert dev["word_competition"] == []
    assert gkx["word_competition"] == []
    assert len(jx["word_competition"]) == 2

    out = {
        "metric_id": "M_SCIUI_THINK_003",
        "batch": "S3-09",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/tech-service/TechCompetition.jsx:131",
            "repos/demo-ui-science/src/pages/tech-service/TechCompetition.jsx:324-333",
            "repos/demo-ui-science/src/pages/tech-service/mockData.js:273-283",
            "repos/demo-ui-science/src/pages/tech-service/TechCompetition.jsx:103-134",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "「竞赛项目评审得分（project score）」指标名三份说明书未出现；清单 row_01=706（_phase3_screen_v3.json）自注「评分维度和算法需要立项调研后才能确定」（需业务建模类）。科技竞赛页为主需求科技创新服务全景平台（1.2 域）UI 挂载件。",
        },
        "facts": {
            "ui_mount": "TechCompetition.jsx:131 排行榜 Tab「竞赛排行榜 TOP10」表格得分列（rankingColumns[2]：title=得分 dataIndex=score width=100，render ts-rank-score 样式）——清单挂载位",
            "ui_table": "TechCompetition.jsx:324-333 Card title=竞赛排行榜 TOP10 + Table columns=rankingColumns dataSource=competitionRankings rowKey=rank（pagination=false 十行全显）",
            "ui_mock_data": "mockData.js:273-283 competitionRankings 十行（rank 1-10：QuantumForce 98.5 量子机器学习算法 清华大学 … MedTechPro 89.9 医疗影像AI 中山大学；含 team/project/institution/members 四维）——ui_demo_fallback 演示值",
            "ui_columns_fn": "TechCompetition.jsx:103-134 rankingColumns 模块级常量：排名徽章（rank<=3 TrophyOutlined）/团队（Avatar+机构）/项目名称/得分——纯展示无计算",
            "dev_table_total": dev["table_total"],
            "dev_competition_word_tables": dev["word_competition"],
            "gkx_table_count": gkx["table_count"],
            "gkx_competition_word_tables": gkx["word_competition"],
            "jiuxin_table_count_live": jx["table_count_live"],
            "jiuxin_competition_word_tables": jx["word_competition"],
            "jiuxin_competition_word_rows": jx["word_competition_rows"],
            "named_in_srs": False,
        },
        "derived": [
            {
                "name": "competition_project_review_score",
                "value": None,
                "numerator": None,
                "denominator": None,
                "note": "竞赛项目评审得分 = 竞赛评审面（项目×评委×得分，或模型算分）输出。竞赛台账/评审流水/评分模型三源零承载：dev 542 表竞赛词族 0 命中、gkx 280 表 0 命中、jiuxin 2 表命中为科研难题竞争排名（competition=学术竞争度语义）。mock score 98.5-89.9 为演示值 → 不可构建，负结论 null 登记",
            },
        ],
        "absence_probe": [
            {
                "probe": "dev 竞赛评审面（competition/contest/award/prize/match_ 词族 542 表）",
                "source": "dev",
                "sql": "information_schema.tables 表名词族扫描（快照 dev.word_competition）+ 列级复探（_probe_s309_alpha_b 快照 dev.competition_like_columns）",
                "hits": 0,
                "hit_detail": "表名 0 命中；列级 competition/contest/prize/award/participant 仅命中 gkxlumenx_dwd.industry_chain_investment_participant.participant_record_id（投融资参与方记录 ID，语义不匹配）",
            },
            {
                "probe": "gkx 竞赛评审面（280 表）",
                "source": "gkx",
                "sql": "information_schema.tables 表名词族扫描（快照 gkx.word_competition）",
                "hits": 0,
                "note": "gkx word_competition=[]——要素库无竞赛域",
            },
            {
                "probe": "jiuxin 竞赛评审面（SHOW TABLES 实数 218 表）",
                "source": "jiuxin",
                "sql": "SHOW TABLES + competition/contest/award/prize/match_ 词族 + 行数（快照 jiuxin.word_competition/_rows）",
                "hits": 2,
                "hit_detail": "ads_research_problem_competition_rank 46,835 行为科研难题『竞争强度排名』（competition=学术竞争度，CONTEST_001 已证同表异域）；ads_talent_research_problem_discipline_match_topic 2,059,636 行为人才-难题-学科匹配族——均非竞赛评审面",
            },
            {
                "probe": "评审模型定义（维度/权重/分制）",
                "source": "doc",
                "sql": "三份说明书 + 主需求 rg 竞赛项目评审得分|project score|评审得分",
                "hits": 0,
                "hit_detail": "指标名 0 命中；清单 row_01=706 自注「评分维度和算法需要立项调研后才能确定」——模型层官方确认空白",
            },
        ],
        "support_judgment": "完全不支持",
        "notes": [
            "判档理由：竞赛项目评审得分需①竞赛台账（项目报名面）②评审流水/评分结果面（项目×评委×得分 或模型输出）③评价模型三层。三源竞赛词族：dev 0 表（列级仅投融资参与方 ID 异域命中）、gkx 0 表、jiuxin 2 表全为学术竞争度/匹配异域。三层皆缺，mock score 98.5→89.9 纯演示。",
            "同族关系：与 THINK_004（参与人数）/THINK_005（奖金总额）/THINK_013（报名数）/THINK_014（排行榜 TOP10）共享竞赛台账缺口；CONTEST_001（竞赛类型分布，路 γ）同词族证据（jiuxin competition_rank 同表异域判定复用）；派单提示「mock score 大概率零承载」已证实。",
            "UI 行为披露：排行榜为纯展示链（模块级 rankingColumns 常量 + mock 十行），无任何排序/计算逻辑（rank 字段为 mock 预排序常量，score 降序仅呈现在数据本身）；得分为两位小数分制（98.5-89.9），分制/满分未定义。",
            "升档路径：竞赛评审系统接入（项目×得分面落库）→ 完全转换支持；办赛平台评审 API 直连 → 完全直接支持；仅有报名无评审 → 需评审模型立项后才可算。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021-2026"],
        "base_years_note": "评审得分为届次/赛季截面读数（每赛事一套评分）；三源无评审面无历史序列；mock 十行无年度维度。",
        "ctx_refs": {
            "note": "正文引用型数字登记",
            "refs": sorted(["10", "98.5", "89.9", "97.2", "96.8", "542", "280", "218", "46835", "46,835", "2059636", "2,059,636", "0", "2", "100"]),
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 完全不支持 | dev/gkx/jiuxin competition hits:",
          len(dev["word_competition"]), len(gkx["word_competition"]), len(jx["word_competition"]))


if __name__ == "__main__":
    main()
