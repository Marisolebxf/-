#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_CONTEST_001 竞赛类型分布 —— 薄壳校验脚本。

共享探针真源：code/_shared_s309_gamma.py（dev/gkx/jiuxin 竞赛主档面三源词族）
本脚本职责：①引用共享快照断言 ②竞赛主档面零承载复核 ③判档 ④基期三键 ⑤落盘。
"""
from __future__ import annotations

import json

SHARED = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/_snapshots/_shared_s309_gamma_out.json"
OUT = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/M_SCIUI_CONTEST_001_out.json"


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        snap = json.load(f)

    dev = snap["dev"]
    gkx = snap["gkx"]
    jiuxin = snap["jiuxin"]

    # 断言：竞赛主档面三源零承载（异域命中逐一登记）
    assert gkx["gkx_contest_family"] == [], "gkx contest 族应为空"
    assert dev["dev_contest_family"] == ["gkxlumenx_ads.policy_match"]
    assert len(jiuxin["jiuxin_contest_family"]) == 4

    out = {
        "metric_id": "M_SCIUI_CONTEST_001",
        "batch": "S3-09",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/tech-service/TechCompetition.jsx:333-346",
            "repos/demo-ui-science/src/pages/tech-service/TechCompetition.jsx:176-181",
            "repos/demo-ui-science/src/pages/tech-service/mockData.js:263-270",
            "repos/demo-ui-science/src/pages/tech-service/TechCompetition.jsx:203-215",
            "repos/demo-ui-science/src/pages/tech-service/TechCompetition.jsx:143-151",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "三份说明书未出现「竞赛类型分布」指标名；科技竞赛页为科技创新服务全景平台（主需求 1.2 域）UI 挂载件，竞赛类型筛选为类型维功能面上位覆盖；清单登记 row_01=722。与 EXCH_001（活动类型分布）同页族同构件。",
        },
        "facts": {
            "ui_mount": "TechCompetition.jsx:333-346 排行榜 Tab 右栏「竞赛类型分布」饼图卡（ReactECharts，series.type=pie，data=typeDistribution 内联数组）",
            "ui_inline": "TechCompetition.jsx:176-181 typeDistribution 六类硬编码（数据科学 15/人工智能 12/创新创业 10/量子计算 8/生物医药 8/其他 15，合计 68）——组件内联常量，连 mockData 都未走——ui_demo_fallback 演示值",
            "ui_filter": "TechCompetition.jsx:203-215 竞赛类型筛选（全部/数据科学/人工智能/创新创业/量子计算/生物医药），联动 :156-160 filteredCompetitions",
            "ui_master": "mockData.js:263-270 competitions 6 行演示竞赛主档（type/level/organizer/startDate/endDate/status/participants/teams/prize）——竞赛台账语义演示",
            "ui_kpi": "TechCompetition.jsx:143-151 KPI 四卡（年度赛事 68 场/参赛团队 8.9 万支/参赛人数 45.6 万人/奖金总额 2.8 亿元）——演示值；六类合计 68 与「年度赛事 68 场」数值巧合同值但无勾稽逻辑",
            "jiuxin_contest_family": jiuxin["jiuxin_contest_family"],
            "gkx_contest_family": gkx["gkx_contest_family"],
            "dev_contest_family": dev["dev_contest_family"],
            "gkx_table_count": gkx["gkx_table_count"],
            "dev_table_total": dev["dev_table_total"],
            "jiuxin_table_count_live": jiuxin["jiuxin_table_count_live"],
            "named_in_srs": False,
        },
        "derived": [
            {
                "name": "contest_type_distribution",
                "value": None,
                "note": "负结论登记：竞赛类型分布 = 竞赛台账按 type 列分组计数（数据科学/人工智能/创新创业/量子计算/生物医药/其他）。mock 主档 competitions 仅 6 行演示且分布为组件内联硬编码；三源竞赛词族命中全为异域（jiuxin 4 表为科研难题 competition_rank 排名/机构匹配族，dev 1 表为 policy_match 政策匹配，gkx 0 命中）。无竞赛台账即无类型分布，null 登记。",
            },
        ],
        "absence_probe": [
            {
                "probe": "jiuxin 218 表（SHOW TABLES 实数）竞赛主档面（contest|competition|match|award|prize）",
                "source": "jiuxin",
                "sql": "SHOW TABLES + 表名词族匹配（快照 jiuxin.jiuxin_contest_family）",
                "hits": 4,
                "hit_tables": jiuxin["jiuxin_contest_family"],
                "verdict": "全为异域：ads_research_problem_competition_rank 为科研难题领域『竞争强度/排名』语义（competition=学术竞争度），三张 match 表为人才-难题-学科匹配族——无科技竞赛赛事主档",
            },
            {
                "probe": "dev 17 schema（542 表）竞赛词族",
                "source": "dev",
                "sql": "information_schema.tables 表名词族扫描（快照 dev.dev_contest_family）",
                "hits": 1,
                "hit_tables": dev["dev_contest_family"],
                "verdict": "异域：gkxlumenx_ads.policy_match 为政策-企业匹配语义（match=匹配），非竞赛",
            },
            {
                "probe": "gkx 280 表竞赛词族",
                "source": "gkx",
                "sql": "information_schema.tables table_name REGEXP contest|competition|match|award|prize（快照 gkx.gkx_contest_family）",
                "hits": 0,
                "verdict": "零命中（280 表全 dwd_* 要素库，无竞赛域）",
            },
        ],
        "support_judgment": "完全不支持",
        "notes": [
            "判档理由：竞赛类型分布需「科技竞赛赛事台账（竞赛×类型×级别×时间×状态）」主档面。三源竞赛词族逐一探针：jiuxin 4 表为科研难题竞争排名/人才匹配族（competition=学术竞争度语义）；dev 1 表为政策匹配（match=匹配语义）；gkx 0 命中。词族命中逐一语义排除后竞赛台账三源零承载，判完全不支持。",
            "词族歧义披露：jiuxin ads_research_problem_competition_rank 的 competition 是『领域竞争强度/排名』分析语义（科研难题热度面），非赛事；dev policy_match 的 match 是『匹配』语义，非比赛。与 EXCH_001 的 foreign_exchange（外汇）同为词族命中≠语义命中的样本。",
            "UI 内联硬编码披露：本件分布数据连 mockData.js 都未走，直接硬编码在组件 :176-181（typeDistribution 常量），六类合计 68 与 KPI『年度赛事 68 场』同值但无代码勾稽——演示值双重不可作基数。",
            "同族关系：与 EXCH_001（活动类型分布）共享「主档面零承载」同构缺口与共享探针快照；THINK_003/004/005/013/014（S3-09 路 α/β 竞赛族）共享同一竞赛台账缺口。",
            "本件为薄壳：共享探针 code/_shared_s309_gamma.py + 快照；本脚本仅做断言+判档落盘。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021-2026"],
        "base_years_note": "分布为当期截面计数（无时间轴）；竞赛台账零承载故无任何年度可用。若接入竞赛台账，基期轴应取赛事举办年度（startDate 年份）。",
        "ctx_refs": {
            "note": "正文引用型数字登记",
            "refs": sorted(["68", "6", "15", "12", "10", "8", "15", "4", "1", "0", "542", "280", "218", "17", "8.9", "45.6", "2.8"]),
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 完全不支持 | jiuxin/gkx/dev contest hits:",
          len(jiuxin["jiuxin_contest_family"]), len(gkx["gkx_contest_family"]), len(dev["dev_contest_family"]))


if __name__ == "__main__":
    main()
