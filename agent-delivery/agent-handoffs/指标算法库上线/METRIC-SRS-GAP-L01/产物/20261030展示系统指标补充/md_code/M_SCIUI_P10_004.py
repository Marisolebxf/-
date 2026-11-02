#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_P10_004 互动统计（M_SS_INTER_*）—— 薄壳校验脚本（完全不支持件）。

UI：BottomTabs.jsx:866「互动统计与传播分析」SectionCard（评论交流 tab）：
四格统计 statItems（累计评论 M_SS_INTER_COMMENT/累计点赞 M_SS_INTER_LIKE/
累计分享 M_SS_INTER_SHARE/知识库条目 M_SS_INTER_KB）+ 六月互动趋势折线。
数据：互动事件流水（用户×成果×行为×时间戳）三源零承载——
dev interact 词族命中全为股东(shareholder)/报表分享(jimu_report_share)语义污染；
gkx 同族污染（shareholder/market）；jiuxin 218 表 0 张互动事件表
（interact 命中列为机构合作语义 institution_cooperation 非用户互动）。
"""
from __future__ import annotations

import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(BASE, "_snapshots", "_shared_s308_laneb_probe_out.json")
OUT = os.path.join(BASE, "M_SCIUI_P10_004_out.json")

VERDICT = "完全不支持"


def main() -> None:
    snap = json.load(open(SNAP, encoding="utf-8"))
    dev, gkx, jx = snap["dev"], snap["gkx"], snap["jiuxin"]

    dev_hits = dict(dev["dev_table_name_hits"])
    dev_interact_tables = sorted(k for k, v in dev_hits.items() if "interact" in v)
    gkx_hits = dict(gkx["gkx_table_name_hits"])
    gkx_interact_tables = sorted(k for k, v in gkx_hits.items() if "interact" in v)
    jx_hits = dict(jx["jiuxin_table_name_hits"])
    jx_interact_tables = sorted(k for k, v in jx_hits.items() if "interact" in v)

    assert dev["dev_table_total"] == 542 and gkx["gkx_table_count"] == 280
    assert jx["jiuxin_table_count_live"] == 218

    out = {
        "metric_id": "M_SCIUI_P10_004",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview-new/soft-science-new/BottomTabs.jsx:866",
            "repos/demo-ui-science/src/pages/achievement-preview-new/soft-science-new/BottomTabs.jsx:753-758",
            "repos/demo-ui-science/src/pages/achievement-preview-new/soft-science-new/mockData.js:214-220",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "srs_anchor": "软科学成果展示.md 序号 475「互动统计与传播分析」（需规描述：自动统计用户互动行为及成果传播效果，生成影响力数据报告）；另序号 472 评论交流与专家互动/473 关注收藏与动态推送/474 多渠道成果社交分享为同域邻叶",
            "note": "M_SS_INTER_* 为 UI 侧指标编号族（MetricInfo title 自带），SRS 无此编号",
        },
        "facts": {
            "ui_mount": "BottomTabs.jsx:866 SectionCard title=互动统计与传播分析（MetricInfo title=互动统计（M_SS_INTER_*），口径：评论/点赞/分享/知识库归档按月归集；源表：ads_soft_science_interact（Mock）+ MockBadge）",
            "ui_stat_items": "BottomTabs.jsx:753-758 statItems 四格：累计评论 M_SS_INTER_COMMENT（comments.length 运行时态）/累计点赞 M_SS_INTER_LIKE（totalLikes）/累计分享 M_SS_INTER_SHARE（INTERACTION_TREND.shares 求和）/知识库条目 M_SS_INTER_KB（kbEntries.length）",
            "ui_trend_chart": "BottomTabs.jsx:681-682 折线双系列（评论/点赞，INTERACTION_TREND.comments/likes 六月序列）",
            "ui_mock_note": "ui_demo_fallback：mock 六月序列 评论 12/19/15/24/31/18、点赞 45/62/58/80/96/54、分享 8/14/11/19/27/16（2026-03~08）；评论计数为前端会话运行时态非库数据",
            "dev_interact_word_tables": dev_interact_tables,
            "dev_interact_semantic_note": "命中全为语义污染：enterprise_shareholder/dwd_forg_shareholder_info/dwd_org_shareholder_info（股东 share 解析歧义）、jimu_report_share/onl_drag_share（BI 报表分享配置）——无一张是用户×成果互动事件流水",
            "gkx_interact_word_tables": gkx_interact_tables,
            "gkx_interact_semantic_note": "dwd_forg_shareholder_info/dwd_org_shareholder_info（股东）、dwd_market（market 解析歧义）、dwd_zh_journal/dwd_en_journal（期刊 share 列为占比语义）——同族污染",
            "jiuxin_interact_tables": jx_interact_tables,
            "jiuxin_interact_note": "表名 0 命中互动事件域；列名命中（ads_institution_collaboration_yearly 等 60+ 表 cooperation/collaborator 列）全为机构合作语义，非平台用户互动",
            "dev_table_total": dev["dev_table_total"],
            "gkx_table_count": gkx["gkx_table_count"],
            "jiuxin_table_count_live": jx["jiuxin_table_count_live"],
        },
        "derived": [
            {
                "name": "interact_stats_negative",
                "value": None,
                "note": "负结论登记：四格统计（评论/点赞/分享/知识库）与月度趋势均需「用户×成果×行为类型×时间戳」互动事件流水，三源零承载，禁伪公式",
            },
        ],
        "absence_probe": [
            {"probe": "dev 542 表 interact/comment/like/share/review 词族（表名+列名双扫）", "source": "dev",
             "hits": dev_interact_tables, "rows": 0,
             "note": "语义污染清单见 facts.dev_interact_semantic_note；无互动事件表"},
            {"probe": "gkx 280 表 interact 词族", "source": "gkx",
             "hits": gkx_interact_tables,
             "note": "股东/期刊占比语义污染；无互动事件表"},
            {"probe": "jiuxin 218 表（SHOW TABLES 实数）interact 词族", "source": "jiuxin",
             "hits": jx_interact_tables,
             "note": "表名 0 命中；列命中为机构合作语义。学术库无平台用户行为流"},
        ],
        "support_judgment": VERDICT,
        "notes": [
            "判档理由：互动统计的原料是平台用户行为日志（谁对哪条成果做了评论/点赞/分享/归档，何时）——这是平台运营面数据，三源（dev 要素库镜像/gkx 供应商要素库/jiuxin 学术分析库）均无此类表；词族命中全为 shareholder（股东）等解析歧义污染。",
            "软科学课题库本身三源零承载（fund_project/enterprise_fund_project 0 行空壳、gkx 无中文课题表、jiuxin ads_project_profile 为 OpenAlex 英文资助项目非深圳软科学课题）——互动流水的宿主对象都不存在，更无互动面。",
            "mock 的评论/点赞计数是前端会话运行时态（useState 种子+用户操作），连演示值都不是稳定数；六月趋势为固定 mock。",
            "与 SOFTSCI_012（满意度分布）同判完全不支持但根因域不同：本件缺用户行为流水，SOFTSCI_012 缺问卷评价面；独立留证。",
            "升档唯一路径：平台互动事件表入湖（cms/app 域运营表若接入且含成果 ID+用户 ID+行为类型+时间）。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021", "2022", "2023", "2024", "2025", "2026"],
        "base_years_note": "无任何真实年度数据（mock 趋势仅 2026-03~08 演示段）；基期无从谈起，全空登记。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted({
            "0", "12", "19", "15", "24", "31", "18", "45", "62", "58", "80", "96", "54",
            "8", "14", "11", "27", "16", "4", "6", "542", "280", "218", "2026",
        })},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment:", VERDICT)


if __name__ == "__main__":
    main()
