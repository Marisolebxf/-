#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_THINK_011 内容累计浏览量 —— 薄壳校验脚本（部分支持件）。

UI：TechCommunication.jsx:125 内容详情抽屉「浏览量」行
（detailTarget.data.views，源自 communicationContents[].views）；
另内容卡 meta 行 :80 EyeOutlined views 直显。
数据：与 THINK_010 同族——三源浏览事件流水零承载，
dev 三处浏览快照列（chain_news.views/policy_latest_news.view_count/
app_article.visit）全部 0 行，gkx dwd_information.click_number 32 行全 NULL；
唯一有数的 jimu_report.view_count（66 行 SUM=749,666）为 BI 报表
语义错位。累计口径只需快照列不需月度面，结构与数据缺口与 010 同构，
独立留证。
"""
from __future__ import annotations

import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP1 = os.path.join(BASE, "_snapshots", "_shared_s309_think_beta_probe_out.json")
SNAP3 = os.path.join(BASE, "_snapshots", "_shared_s309_think_beta_probe3_out.json")
SNAP4 = os.path.join(BASE, "_snapshots", "_shared_s309_think_beta_probe4_out.json")
SNAP5 = os.path.join(BASE, "_snapshots", "_shared_s309_think_beta_probe5_out.json")
OUT = os.path.join(BASE, "M_SCIUI_THINK_011_out.json")

VERDICT = "部分支持"


def main() -> None:
    s1 = json.load(open(SNAP1, encoding="utf-8"))
    s3 = json.load(open(SNAP3, encoding="utf-8"))
    s4 = json.load(open(SNAP4, encoding="utf-8"))
    s5 = json.load(open(SNAP5, encoding="utf-8"))
    dev1, gkx1, jx1 = s1["dev"], s1["gkx"], s1["jiuxin"]
    dev3, gkx4, gkx5 = s3["dev"], s4["gkx"], s5["gkx"]

    # ---- 快照一致性断言（B11）----
    assert dev1["dev_table_total"] == 542 and gkx1["gkx_table_count"] == 280
    assert jx1["jiuxin_table_count_live"] == 218

    # ---- 承载面断言 ----
    assert dev3["chain_news_rows"] == 0
    assert dev3["policy_latest_news_rows"] == 0
    assert dev3["app_article_rows"] == 0
    assert dev3["app_article_columns"].count("visit") == 1  # 累计快照列存在
    assert dev3["chain_news_columns"].count("views") == 1
    assert dev3["jimu_report_rows"] == 66
    assert dev3["jimu_report_view_count_stat"]["sum"] == 749666
    assert gkx4["gkx_information_rows"] == 32
    assert gkx5["gkx_information_click_stat"]["non_null_rows"] == 0

    dev_hits = dict(dev1["dev_table_name_hits"])
    dev_view_tables = sorted(k for k, v in dev_hits.items() if "view" in v)
    gkx_hits = dict(gkx1["gkx_table_name_hits"])
    gkx_view_tables = sorted(k for k, v in gkx_hits.items() if "view" in v)
    jx_hits = dict(jx1["jiuxin_table_name_hits"])
    jx_view_tables = sorted(k for k, v in jx_hits.items() if "view" in v)

    out = {
        "metric_id": "M_SCIUI_THINK_011",
        "batch": "S3-09",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/tech-service/TechCommunication.jsx:125",
            "repos/demo-ui-science/src/pages/tech-service/TechCommunication.jsx:80",
            "repos/demo-ui-science/src/pages/tech-service/mockData.js:311-319",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "srs_anchor": "科技传播.md 序号 600 内容数据接口服务（『提供具体传播内容的详细数据接口…支撑前端对内容详情的完整呈现』——详情抽屉浏览量行的上位叶）；SRS 无同名指标",
            "note": "THINK 系为 UI 侧指标编号族，SRS 无此编号",
        },
        "facts": {
            "ui_mount": "TechCommunication.jsx:125 详情抽屉基本信息 items { label: '浏览量', value: detailTarget.data.views }；:80 内容卡 meta <EyeOutlined /> {content.views} 直显",
            "ui_mock_note": "ui_demo_fallback：mockData.js:311-319 communicationContents 8 条逐条 views 演示值 3450/4230/5670/6540/7230/8920/12580/15680（降序），静态数组不参与支持度结论",
            "ui_neighbors": "详情抽屉同组行：发布时间/浏览量（本件）/点赞数（THINK_012）；展览地点/主讲人/作者按类型扩展",
            "dev_snapshot_columns": [
                "gkxlumenx_dwd.chain_news.views 16 列 0 行",
                "gkxlumenx_dwd.policy_latest_news.view_count 20 列 0 行",
                "gkxlumenx_app.app_article.visit 15 列 0 行",
            ],
            "gkx_information_click": "gkx.dwd_information 32 行（2019-2025 供应商资讯），click_number 32 行全 NULL——快照列结构在、数据无",
            "dev_bi_view_proxy": "gkxlumenx_bi.jimu_report.view_count 66 行全有值 SUM=749,666 MAX=54,003——BI 报表浏览计数，语义错位仅内验",
            "jiuxin_view_note": "jiuxin 218 表（SHOW TABLES 实数）表名 view 命中 1 张为 overview 子串误中；列名 42 处全为 review_status/reviewer 评审语义污染，无浏览计数列",
            "dev_view_tables": dev_view_tables,
            "gkx_view_tables": gkx_view_tables,
            "jiuxin_view_tables": jx_view_tables,
            "dev_table_total": dev1["dev_table_total"],
            "gkx_table_count": gkx1["gkx_table_count"],
            "jiuxin_table_count_live": jx1["jiuxin_table_count_live"],
        },
        "derived": [
            {
                "name": "cumulative_views_negative",
                "value": None,
                "note": "负结论登记：内容累计浏览量需内容主档浏览快照列或事件流累计求和，承载行全 0/NULL，累计读数不可算，禁伪公式",
            },
            {
                "name": "jimu_report_view_sum_proxy",
                "value": 749666,
                "numerator": "jimu_report.view_count 全表求和（66 行）",
                "denominator": "无（计数总和，非比率）",
                "note": "BI 报表浏览代理读数：语义错位（BI 工具报表浏览 ≠ 科技传播内容浏览），仅证明「累计计数列+求和」计算链可跑通，不可对外",
            },
        ],
        "absence_probe": [
            {"probe": "dev 542 表 view/browse/pv/visit/click 词族（表名+列名双扫 information_schema 全 gkxlumenx% schema）",
             "source": "dev", "hits": dev_view_tables, "rows": 0,
             "note": "表名命中 1 张为 overview 子串误中（0 行）；列名正语义命中 chain_news.views/policy_latest_news.view_count/app_article.visit 全部 0 行——无浏览事件流水、快照列空载"},
            {"probe": "gkx 280 表 view 词族（表名+列名双扫）", "source": "gkx",
             "hits": gkx_view_tables,
             "note": "表名 0 命中；列名唯一候选 dwd_information.click_number 32 行全 NULL——结构在、数据无"},
            {"probe": "jiuxin 218 表（SHOW TABLES 实数）view 词族（表名+列名逐表 DESCRIBE）", "source": "jiuxin",
             "hits": jx_view_tables,
             "note": "表名命中 1 张为 overview 子串误中；列名 42 处全为 review_status/reviewer 评审语义污染——学术分析库无平台浏览行为面"},
        ],
        "support_judgment": VERDICT,
        "notes": [
            "判档理由：累计浏览量只需内容主档上的浏览快照列（比 THINK_010 的月度面要求更低），三源恰好存在该结构（dev 3 处列 + gkx click_number）但承载行全 0/NULL——结构与数据缺口同构于 THINK_010，判部分支持；独立留证不引用 010 产物作判据。",
            "累计口径的宿主是十类传播内容主档（SRS 序号 596），三源侧 cms_content_news 12 行通用新闻无浏览列、app_article 0 行——宿主主档本身待建全，快照列随主档缺口同缺。",
            "唯一有数的 jimu_report.view_count（66 行 SUM=749,666）为 BI 报表浏览，语义错位仅内验；mock 8 条 views 演示值 ui_demo_fallback 披露。",
            "与 THINK_010（月浏览量）同族同判部分支持但口径要求不同：010 需月度聚合面（chain_news_stat 结构在 0 行），本件只需快照列——两者升档触发器相同（新闻/资讯入湖），本件对数据形态要求更宽松（单批灌数即可出累计值，无需多月份快照）。",
            "升档路径：内容主档+浏览快照列灌数 → 完全转换支持；平台 PV 事件流接入（可算真累计）→ 完全直接支持。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021", "2022", "2023", "2024", "2025", "2026"],
        "base_years_note": "无任何真实累计浏览数据（快照列承载全 0/NULL；gkx 资讯 2019-2025 但 click_number 全 NULL）；基期无从谈起，全空登记。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted({
            "0", "1", "3", "8", "12", "32", "42", "66", "218", "280", "542",
            "3450", "4230", "5670", "6540", "7230", "8920", "12580", "15680",
            "749666", "54003",
            "2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026",
        })},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment:", VERDICT)


if __name__ == "__main__":
    main()
