#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_THINK_005 竞赛奖金总额 —— 薄壳校验脚本（负结论件）。

UI：TechCompetition.jsx:150 KPI 四卡之四「奖金总额 2.8 亿元」
（trend rise +18.3%）+ :66-68 竞赛卡奖金徽标（TrophyOutlined 奖金 {prize}，
mock prize 字符串 100万/50万/30万/200万/80万/150万）+ :242-248 奖金规模筛选。
口径=赛事奖金总额（货币金额）——竞赛台账（prize 列）零承载
（CONTEST_001 已证台账缺口，本件独立留证：奖金/资金词族三源探针）。
"""
from __future__ import annotations

import json

SHARED = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/_snapshots/_shared_s309_alpha_out.json"
OUT = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/M_SCIUI_THINK_005_out.json"


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        snap = json.load(f)

    dev = snap["dev"]
    gkx = snap["gkx"]
    jx = snap["jiuxin"]
    assert dev["table_total"] == 542 and gkx["table_count"] == 280
    assert jx["table_count_live"] == 218
    assert dev["word_competition"] == []
    assert gkx["word_competition"] == []
    assert len(jx["word_competition"]) == 2

    out = {
        "metric_id": "M_SCIUI_THINK_005",
        "batch": "S3-09",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/tech-service/TechCompetition.jsx:150",
            "repos/demo-ui-science/src/pages/tech-service/TechCompetition.jsx:66-68",
            "repos/demo-ui-science/src/pages/tech-service/TechCompetition.jsx:242-248",
            "repos/demo-ui-science/src/pages/tech-service/mockData.js:264-269",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "「竞赛奖金总额」指标名三份说明书未出现；清单 row_01=708（_phase3_screen_v3.json）自注「涉及资金的货币金额统计——单位一般为元/万元」。科技竞赛页为主需求科技创新服务全景平台（1.2 域）UI 挂载件。",
        },
        "facts": {
            "ui_mount": "TechCompetition.jsx:150 KPI 四卡之四 { label: 奖金总额, value: 2.8, unit: 亿元, trend: rise, change: 18.3 }——清单挂载位",
            "ui_prize_badge": "TechCompetition.jsx:66-68 竞赛卡图片区奖金徽标 <TrophyOutlined/> 奖金 {competition.prize}（prize 为字符串如 100万）",
            "ui_prize_filter": "TechCompetition.jsx:242-248 更多筛选·奖金规模 Select（全部/100万以上/50-100万/50万以下）——筛选条件为前端常量未联动 prize 字段",
            "ui_mock_data": "mockData.js:264-269 competitions 6 行 prize 字符串（100万/50万/30万/200万/80万/150万，字符串带单位非数值）——ui_demo_fallback 演示值；KPI 2.8 亿元与六赛事合计约 610 万不勾稽",
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
                "name": "competition_prize_total",
                "value": None,
                "numerator": None,
                "denominator": None,
                "note": "竞赛奖金总额 = Σ 赛事奖金（竞赛台账 prize/bonus 数值列年度求和）。竞赛台账三源零承载（dev/gkx 竞赛词族 0 表、jiuxin 2 表学术竞争度异域）；mock prize 为字符串常量（含单位不可聚合），KPI 2.8 亿元为演示值 → 不可构建，负结论 null 登记",
            },
        ],
        "absence_probe": [
            {
                "probe": "dev 竞赛台账·奖金列（competition/contest/award/prize/match_ 词族 542 表）",
                "source": "dev",
                "sql": "information_schema.tables 表名词族扫描（快照 dev.word_competition）+ 列级 prize/award 复探（_probe_s309_alpha_b 快照 dev.competition_like_columns）",
                "hits": 0,
                "hit_detail": "表名 0 命中；列级 competition/contest/prize/award/participant 仅 industry_chain_investment_participant.participant_record_id（投融资异域）——无竞赛奖金面",
            },
            {
                "probe": "gkx 竞赛台账·奖金列（280 表）",
                "source": "gkx",
                "sql": "information_schema.tables 表名词族扫描（快照 gkx.word_competition）",
                "hits": 0,
                "note": "gkx word_competition=[]——要素库无竞赛域（无 prize/award 表）",
            },
            {
                "probe": "jiuxin 竞赛台账·奖金列（SHOW TABLES 实数 218 表）",
                "source": "jiuxin",
                "sql": "SHOW TABLES + competition/contest/award/prize/match_ 词族 + 行数（快照 jiuxin.word_competition/_rows）",
                "hits": 2,
                "hit_detail": "ads_research_problem_competition_rank 46,835 行（学术竞争度排名，无奖金列语义）+ ads_talent_research_problem_discipline_match_topic 2,059,636 行（匹配族）——均无奖金/资助金额语义",
            },
            {
                "probe": "KPI 勾稽核（演示值内部一致性）",
                "source": "ui",
                "sql": "mock prize 六值合计 vs KPI 2.8 亿元 人工核对",
                "hits": 1,
                "hit_detail": "六赛事 prize 合计约 610 万（100+50+30+200+80+150 万），与 KPI 2.8 亿元相差 45 倍+——演示值各自独立编写不勾稽，佐证均不可作基数",
            },
        ],
        "support_judgment": "完全不支持",
        "notes": [
            "判档理由：竞赛奖金总额需「竞赛台账含 prize/bonus 数值列」。三源竞赛词族：dev 0 表（列级仅投融资参与方 ID 异域）、gkx 0 表、jiuxin 2 表学术竞争度/匹配异域（无奖金语义）。台账零承载则总额无从聚合；mock prize 为字符串常量（含单位不可聚合），KPI 2.8 亿元为演示值且与明细不勾稽。",
            "同族关系：与 THINK_003/004/013/014/CONTEST_001 共享竞赛台账缺口（六件一族）；奖金规模筛选（:242-248）为前端常量未联动数据——同为演示态自证。",
            "类型陷阱披露（B9）：mock prize 为带单位字符串（'100万'）非数值——即使 mock 可用也需解析单位；清单自注单位「一般为元/万元」而 KPI 用亿元——单位口径三态（元/万元/亿元）未统一。",
            "升档路径：竞赛台账接入（prize 数值列+币种+年度）→ 完全转换支持；办赛平台 API 直连 → 完全直接支持。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021-2026"],
        "base_years_note": "奖金总额为年度/届次聚合读数；三源无竞赛台账无历史序列；mock 亦无年度维度（KPI change +18.3% 为演示涨幅）。",
        "ctx_refs": {
            "note": "正文引用型数字登记",
            "refs": sorted(["2.8", "18.3", "100万", "50万", "30万", "200万", "80万", "150万", "610", "542", "280", "218", "46835", "2059636", "0", "2"]),
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 完全不支持 | competition word dev/gkx/jiuxin:",
          len(dev["word_competition"]), len(gkx["word_competition"]), len(jx["word_competition"]))


if __name__ == "__main__":
    main()
