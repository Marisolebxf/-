#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_THINK_009 内容发布时间趋势 —— 薄壳校验脚本（部分支持件）。

UI：ThinkTankService.jsx:551 智库服务页「时间趋势」折线卡
（timeTag 维度成果/案例/建议三线）+ TechCommunication.jsx:251-257
科技传播页时间轴视图（communicationTimeline 8 点）+ 详情抽屉发布时间行。
口径=内容发布量随时间的趋势——内容主档 publish_time 序列。
判定=部分支持（与 THINK_006 同根）：dev 主档近乎空壳（时序不可算）；
dev enterprise_news 1,668,414 行 2018-2026 年度序列可算（宽口径代理，
总体=企业新闻）；gkx dwd_news_base 20,000 行 fbsj 年度分布（小样本）。
"""
from __future__ import annotations

import json

SHARED_A = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/_snapshots/_shared_s309_alpha_out.json"
SHARED_C = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/_snapshots/_probe_s309_alpha_c_out.json"
OUT = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/M_SCIUI_THINK_009_out.json"


def main() -> None:
    with open(SHARED_A, encoding="utf-8") as f:
        snap_a = json.load(f)
    with open(SHARED_C, encoding="utf-8") as f:
        snap_c = json.load(f)

    dev = snap_a["dev"]
    gkx = snap_a["gkx"]
    jx = snap_a["jiuxin"]
    ent_dist = snap_c["dev"]["enterprise_news_year_dist"]
    assert dev["table_total"] == 542 and gkx["table_count"] == 280
    assert jx["table_count_live"] == 218
    assert sum(ent_dist.values()) == 1668414
    # 断言：年度序列 2018-2026 九年连续
    assert sorted(ent_dist.keys()) == [str(y) for y in range(2018, 2027)]

    out = {
        "metric_id": "M_SCIUI_THINK_009",
        "batch": "S3-09",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/tech-service/ThinkTankService.jsx:551-555",
            "repos/demo-ui-science/src/pages/tech-service/TechCommunication.jsx:244-257",
            "repos/demo-ui-science/src/pages/tech-service/TechCommunication.jsx:124",
            "repos/demo-ui-science/src/pages/tech-service/mockData.js:323-330",
            "repos/demo-ui-science/src/pages/tech-service/mockData.js:310-320",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "「内容发布时间趋势」指标名三份说明书未出现；清单 row_01=711（_phase3_screen_v3.json）l3=时间趋势，mean 注「指标随时间的上升/下降情况——和上年同期比还是和上一期比见指标名称」（清单语义宽泛）。挂载多点：清单 mount 登记三处（TechInnovationEvaluationPage:423/:441 + ThinkTankService:551），本件按科技智库/传播页两处调研。",
        },
        "facts": {
            "ui_mount_thinktank": "ThinkTankService.jsx:551-555 智库服务页四图卡之二 Card title=时间趋势（ReactECharts 折线，xAxis=timeTag，三系列：成果/案例/建议按时间标签聚合 buildAggregate(trendEntries).byTime）",
            "ui_mount_comm": "TechCommunication.jsx:244-257 科技传播页时间轴视图（Timeline 组件，communicationTimeline 8 点 date+title，highlight 红蓝标记）——卡片视图/时间轴视图切换（:203-209 视图模式 Select）",
            "ui_detail_date": "TechCommunication.jsx:124 详情抽屉基本信息区 { label: 发布时间, value: detailTarget.data.date } 行——单条内容发布日",
            "ui_sort": "TechCommunication.jsx:207-212 排序 Select：最新发布（date）/最多浏览（views）/最多点赞（likes）——发布时间为排序键之一",
            "ui_mock_timeline": "mockData.js:323-330 communicationTimeline 8 点（2026-05-20 深圳国际创新成果展开幕 … 2026-05-01 科学文化系列文章发布）——ui_demo_fallback 演示值（一个月跨度 8 点）",
            "ui_mock_contents": "mockData.js:310-320 communicationContents 8 行 date 字段（2026-05-01 至 2026-05-20）——发布时间维在 mock 主档",
            "dev_table_total": dev["table_total"],
            "dev_cms_content_news_rows": 12,
            "dev_enterprise_news_rows": 1668414,
            "dev_enterprise_news_year_dist": ent_dist,
            "dev_enterprise_news_empty_time_rows": 0,
            "gkx_table_count": gkx["table_count"],
            "gkx_dwd_news_base_rows": 20000,
            "jiuxin_table_count_live": jx["table_count_live"],
            "jiuxin_talent_media_report_rows": 30,
            "jiuxin_talent_media_report_published_at": "列在（_probe_s309_alpha_b 快照 talent_media_report_columns 含 published_at/published_at_raw）",
            "named_in_srs": False,
        },
        "derived": [
            {
                "name": "content_publish_time_trend",
                "value": None,
                "note": "口径 A（平台内容主档发布趋势）：dev CMS 主档 pub_date 序列——主档 29 行近乎空壳，时序不可算。口径 B（企业新闻发布趋势，宽口径代理）：dev enterprise_news publish_time 年度序列可算（见 derived[1]）但总体=企业新闻非平台内容。两口径均不能产出「平台内容发布趋势」真值 → null 登记",
            },
            {
                "name": "enterprise_news_publish_yearly",
                "value": ent_dist,
                "formula": "COUNT(*) GROUP BY SUBSTRING(publish_time,1,4)，publish_time datetime 列 0 空值",
                "source": "dev gkxlumenx_dwd.enterprise_news",
                "note": "宽口径代理序列（2018-2026 九年连续）：2018=15,767 / 2019=41,104 / 2020=3,203 / 2021=158,521 / 2022=256,110 / 2023=308,765 / 2024=366,413 / 2025=421,067 / 2026=97,464（截断年）——总体为企业新闻，非平台内容口径（代理读数禁对外）",
            },
            {
                "name": "trend_peak_year",
                "value": "2025",
                "note": "代理序列峰值年 2025（421,067 条）；2020 低谷（3,203 条，疫情年采集缺口语义待核）；2026 截断（97,464 条）",
            },
        ],
        "absence_probe": [
            {
                "probe": "dev 平台内容主档发布时序（cms pub_date 列序列）",
                "source": "dev",
                "sql": "cms_content_news 16 列含 pub_date（_probe_s309_alpha_b 快照）+ 三表合计 29 行",
                "hits": 1,
                "hit_detail": "pub_date 列在但主档量近乎空壳（29 行）——时序粒度不足（29 点撑不起趋势图）",
            },
            {
                "probe": "dev 企业新闻年度序列（宽口径代理）",
                "source": "dev",
                "sql": "SELECT SUBSTRING(publish_time,1,4), COUNT(*) FROM gkxlumenx_dwd.enterprise_news GROUP BY 1（_probe_s309_alpha_c 快照）",
                "hits": 9,
                "hit_detail": "2018-2026 九年连续全序列（合计 1,668,414 行、publish_time 0 空值）——量足可用但总体=企业新闻（语义错位：企业融资/动态新闻≠平台发布内容）",
            },
            {
                "probe": "gkx 新闻发布时序（dwd_news_base.fbsj）",
                "source": "gkx",
                "sql": "SUBSTRING(CAST(fbsj AS CHAR),1,4) 分布（_probe_s309_alpha_d 快照）",
                "hits": 9,
                "hit_detail": "2018-2026 分布 169/547/35/1918/2932/3831/4102/4896/1570（合计 20,000 行）——同为新闻语义且样本小（2 万行）",
            },
            {
                "probe": "jiuxin 内容发布时序（talent_media_report.published_at）",
                "source": "jiuxin",
                "sql": "DESCRIBE ads_talent_media_report（_probe_s309_alpha_b 快照 talent_media_report_columns）",
                "hits": 1,
                "hit_detail": "published_at 列在、30 行——人才媒体报道域（语义错位+量不足双排除）",
            },
        ],
        "support_judgment": "部分支持",
        "notes": [
            "判档理由：内容发布时间趋势需「平台内容主档×发布时间序列」。dev CMS 主档 pub_date 列在但 29 行近乎空壳（时序不可算）；宽口径代理 dev enterprise_news 九年序列可算（1,668,414 行 0 空值）但总体=企业新闻≠平台内容；gkx dwd_news_base 2 万行小样本同新闻语义；jiuxin 30 行人才域。口径正确面量不足、量足面总体错位 → 部分支持（与 THINK_006 同根同判）。",
            "同族关系：与 THINK_006（平台内容总条数）共享内容主档缺口与探针快照（alpha/alpha_b/alpha_c）；与 THINK_010/011/012（路 β）同挂科技传播页——时间轴视图与卡片 date 字段是本件的 UI 界面表达。",
            "挂载多点披露：清单 mount 登记三处（TechInnovationEvaluationPage.tsx:423/:441 科技创新评估页另有时间趋势图，非本件主挂载）；本件按智库服务页折线卡（:551）+ 传播页时间轴（:244-257）两处调研——智库页时间趋势的 timeTag 维是「近一周/近一月/近三月/近一年」相对标签（thinkTankModel.js timeTag 函数），非发布日期序列，口径更宽。",
            "代理序列读数披露（B10）：enterprise_news 年度序列为宽口径代理（企业新闻发布趋势），2020 年 3,203 条低谷疑采集缺口（2019 年 41,104 → 2020 骤降 92%）；2026 截断年 97,464 条——代理读数禁对外。",
            "升档路径：dev CMS 主档灌数（≥千行量级）→ 完全直接支持（pub_date GROUP BY 即活）；接受企业新闻代理 → 仍部分支持且须标注「企业新闻发布趋势」。",
        ],
        "base_years_used": ["2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026"],
        "base_years_missing": ["2013-2017"],
        "base_years_note": "代理序列（enterprise_news）2018-2026 九年连续可用（2026 截断年需标注）；2013-2017 无数据。平台内容主档口径的基期待主档灌数后以收录起始年定。",
        "ctx_refs": {
            "note": "正文引用型数字登记",
            "refs": sorted(["8", "12", "29", "30", "542", "280", "218", "1668414", "1,668,414",
                            "15767", "41104", "3203", "158521", "256110", "308765", "366413", "421067", "97464",
                            "20000", "169", "547", "35", "1918", "2932", "3831", "4102", "4896", "1570", "2018", "2026"]),
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 部分支持 | ent_news yearly:", ent_dist)


if __name__ == "__main__":
    main()
