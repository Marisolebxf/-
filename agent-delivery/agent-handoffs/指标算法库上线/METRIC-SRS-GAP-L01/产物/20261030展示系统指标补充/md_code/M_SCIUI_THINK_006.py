#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_THINK_006 平台内容总条数 —— 薄壳校验脚本（部分支持件）。

UI：TechCommunication.jsx:141 统计概览四卡之一「总内容数」
（Statistic value=communicationStats.totalContents，mock 3,567）。
口径=平台发布内容（文章/报告/视频等）总条数——内容主档面。
判定=部分支持：dev CMS 结构面在（cms_content_news 12 行等，近乎空壳）、
三方新闻面量足（gkx 166.8 万/org_important_news_info，总体=企业新闻≠平台内容）、
jiuxin 30 行人才媒体报道——总体错位 + 平台内容主档量不足。
"""
from __future__ import annotations

import json

SHARED_A = "_snapshots/_shared_s309_alpha_out.json"
SHARED_B = "_snapshots/_probe_s309_alpha_b_out.json"
OUT = "M_SCIUI_THINK_006_out.json"


def main() -> None:
    with open(SHARED_A, encoding="utf-8") as f:
        snap_a = json.load(f)
    with open(SHARED_B, encoding="utf-8") as f:
        snap_b = json.load(f)

    dev = snap_a["dev"]
    gkx = snap_a["gkx"]
    jx = snap_a["jiuxin"]
    cms_news = snap_b["dev"]["gkxlumenx_cms.cms_content_news"]
    cms_sz = snap_b["dev"]["gkxlumenx_cms.cms_content_sz"]
    cms_roster = snap_b["dev"]["gkxlumenx_cms.cms_content_region_roster"]
    ent_news_rows = snap_b["dev"]["gkxlumenx_dwd.enterprise_news"]["rows"]
    assert dev["table_total"] == 542 and gkx["table_count"] == 280
    assert jx["table_count_live"] == 218
    assert cms_news["rows"] == 12 and cms_sz["rows"] == 11 and cms_roster["rows"] == 6
    assert ent_news_rows == 1668414
    assert gkx["content_table_rows"]["dwd_org_important_news_info"] == 1668414

    cms_sum = cms_news["rows"] + cms_sz["rows"] + cms_roster["rows"]

    out = {
        "metric_id": "M_SCIUI_THINK_006",
        "batch": "S3-09",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/tech-service/TechCommunication.jsx:141",
            "repos/demo-ui-science/src/pages/tech-service/TechCommunication.jsx:154-161",
            "repos/demo-ui-science/src/pages/tech-service/mockData.js:335-340",
            "repos/demo-ui-science/src/pages/tech-service/mockData.js:299-308",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "「平台内容总条数」指标名三份说明书未出现；清单 row_01=709（_phase3_screen_v3.json）l3=总内容数，mean 注「文章/报告等内容受用户欢迎程度的统计」（清单语义宽泛）。科技传播页为主需求科技创新服务全景平台（1.2 域）UI 挂载件。",
        },
        "facts": {
            "ui_mount": "TechCommunication.jsx:141 统计概览四卡之一 { label: 总内容数, value: communicationStats.totalContents }——清单挂载位；:154-161 Statistic 卡渲染",
            "ui_mock_stats": "mockData.js:335-340 communicationStats { totalContents: 3567, monthlyViews: 1258000, activeUsers: 45600, newContents: 234 }——ui_demo_fallback 演示值",
            "ui_categories": "mockData.js:299-308 communicationCategories 九分类卡（创新成果展览 156/科学人讲坛 234/院士风采 89/学术期刊 45/学术会议 178/科技图书 567/信息素养 123/科学文化 234/新媒体 1890）——九类合计 3,516 ≠ totalContents 3,567（差 51，演示值不勾稽）",
            "dev_table_total": dev["table_total"],
            "dev_cms_content_news": {"rows": cms_news["rows"], "columns": cms_news["columns"],
                                      "note": "16 列含 domain/title/kind/content/pub_date/status——平台内容主档结构面（近乎空壳）"},
            "dev_cms_content_sz": {"rows": cms_sz["rows"]},
            "dev_cms_content_region_roster": {"rows": cms_roster["rows"]},
            "dev_cms_content_sum": cms_sum,
            "dev_app_article": {"rows": dev["content_table_rows"]["gkxlumenx_app.app_article"],
                                 "note": "app 文章主档 0 行空壳"},
            "dev_news_ods": {"rows": snap_b["dev"]["gkxlumenx_ods.news"]["rows"], "note": "ods 通用新闻 0 行空壳"},
            "gkx_table_count": gkx["table_count"],
            "gkx_content_table_rows": gkx["content_table_rows"],
            "jiuxin_table_count_live": jx["table_count_live"],
            "jiuxin_content_word_tables": jx["word_content"],
            "jiuxin_content_word_rows": jx["word_content_rows"],
            "named_in_srs": False,
        },
        "derived": [
            {
                "name": "platform_content_total",
                "value": None,
                "numerator": None,
                "denominator": None,
                "note": "平台内容总条数 = 平台内容主档（文章/报告/视频等）全量 COUNT。本库真源判定：dev CMS 主档面三表合计 29 行（cms_content_news 12 + cms_content_sz 11 + cms_content_region_roster 6，结构在量近乎空壳）；app_article/ods.news 0 行空壳；gkx/jiuxin 新闻面为企业新闻/人才媒体报道语义（总体错位）。UI 口径的平台内容主档量不足、代理面语义错位 → 无可信总数，null 登记（负读数；判部分支持依据结构面在）",
            },
            {
                "name": "gkx_news_family_total",
                "value": sum(gkx["content_table_rows"].values()),
                "note": "gkx 内容词族五表行数合计（dwd_org_important_news_info 1,668,414 + dwd_zh_paper_reference_content 196,619 + dwd_industry_chain_news_info 108,052 + dwd_news_base 20,000 + dwd_industry_analysis_content_types 1,000）= 1,994,085——企业/产业链新闻语义代理面规模参照（非平台内容口径）",
            },
        ],
        "absence_probe": [
            {
                "probe": "dev 平台内容主档量（cms/app/news 族行数实证 542 表）",
                "source": "dev",
                "sql": "COUNT(*) 逐表（_probe_s309_alpha_b 快照 + _shared_s309_alpha 快照 content_table_rows）",
                "hits": 3,
                "hit_detail": "cms_content_news 12 行 + cms_content_sz 11 行 + cms_content_region_roster 6 行 = 29 行；app_article/app_article_category/app_article_collect 0 行；ods.news 0 行；policy_latest_news/chain_news 0 行——结构面在、量近乎空壳（主降档因之一）",
            },
            {
                "probe": "gkx 内容词族（280 表 content/article/publish/media/news/cms）",
                "source": "gkx",
                "sql": "表名词族扫描 + COUNT（快照 gkx.content_table_rows）",
                "hits": 5,
                "hit_detail": "五表合计 1,994,085 行——语义全为企业新闻/产业链新闻/论文引用内容（dwd_org_important_news_info=机构重要新闻等），非「平台发布内容」主档口径（总体错位，主降档因之二）",
            },
            {
                "probe": "jiuxin 内容词族（SHOW TABLES 实数 218 表）",
                "source": "jiuxin",
                "sql": "SHOW TABLES + content/article/publish/media/news/cms 词族 + 行数（快照 jiuxin.word_content/_rows）",
                "hits": 2,
                "hit_detail": "ads_talent_media_report 30 行 + ads_talent_media_sentiment_assessment 15 行——人才媒体报道语义（30 列含 published_at/title/publisher），非平台内容主档",
            },
            {
                "probe": "UI 分类勾稽核（演示值内部一致性）",
                "source": "ui",
                "sql": "九分类 count 合计 vs totalContents 人工核对",
                "hits": 1,
                "hit_detail": "九类合计 3,516 ≠ totalContents 3,567（差 51）——mock 自身不勾稽，演示值不可作基数",
            },
        ],
        "support_judgment": "部分支持",
        "notes": [
            "判档理由：平台内容总条数需「平台内容主档（发布内容×类型×状态）」。dev CMS 结构面完整在（cms_content_news 16 列含 domain/kind/content/pub_date/status）但量近乎空壳（三表合计 29 行）；gkx/jiuxin 新闻面量足但总体错位（企业新闻/人才媒体报道≠平台发布内容）。结构部分可得、可信总量不可得 → 部分支持（双降档因：主档量不足 + 代理总体错位）。",
            "同族关系：与 THINK_009（内容发布时间趋势）共享内容主档缺口与探针快照；与 THINK_010/011/012（浏览/点赞族，路 β）同挂科技传播页四卡（月浏览量/累计浏览/点赞）——四卡同根。",
            "语义错位披露（B10）：gkx 1,994,085 行为企业/产业链新闻面（org_important_news_info 机构重要新闻等），jiuxin 45 行为人才媒体报道——即使取数也只是「新闻池规模」而非「平台内容总数」；dev CMS 29 行是唯一口径正确的面但量不足。",
            "UI 披露：mock totalContents 3,567 与九分类合计 3,516 不勾稽（差 51）——演示值双重不可作基数。",
            "升档路径：dev CMS 主档灌数（平台发布内容接入）→ 完全直接支持；接受新闻池代理口径 → 仍部分支持且须标注「企业新闻池规模，非平台内容总数」。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021-2026"],
        "base_years_note": "总条数为存量截面读数（无时序维度）；dev CMS 主档近乎空壳无年度可谈；若接入真实内容主档以收录起始年为基期。",
        "ctx_refs": {
            "note": "正文引用型数字登记",
            "refs": sorted(["3567", "3,567", "3516", "3,516", "51", "29", "12", "11", "6", "16",
                            "542", "280", "218", "1668414", "1,668,414", "1994085", "1,994,085",
                            "196619", "108052", "20000", "1000", "30", "15", "156", "234", "89", "45", "178", "567", "123", "1890"]),
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 部分支持 | dev CMS 三表合计:", cms_sum,
          "| gkx 五表合计:", sum(gkx["content_table_rows"].values()),
          "| jiuxin:", jx["word_content_rows"])


if __name__ == "__main__":
    main()
