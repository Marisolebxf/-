#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_P10_065 指标环比增速（较上一统计周期）—— 薄壳校验脚本。

共享探针真源：code/_shared_s309_gamma.py（宿主序列面 + 环比比例列三源扫描）
本脚本职责：①依赖链裁定：宿主指标承载性证明 ②mock 环比重算复核（演示算术核验）
③判档 ④基期三键 ⑤落盘。
"""
from __future__ import annotations

import json

SHARED = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/_snapshots/_shared_s309_gamma_out.json"
OUT = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/M_SCIUI_P10_065_out.json"

# UI mock 宿主序列（mockData.js:813-817 investment.values，清单登记宿主）
MOCK_HOST = [8.2, 9.6, 11.4, 10.8, 12.6, 14.2, 13.5, 15.8, 16.4, 18.2]
MOCK_LABELS = ["2024Q1", "2024Q2", "2024Q3", "2024Q4", "2025Q1", "2025Q2", "2025Q3", "2025Q4", "2026Q1", "2026Q2"]


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        snap = json.load(f)

    dev = snap["dev"]
    gkx = snap["gkx"]
    jiuxin = snap["jiuxin"]

    # ---- mock 环比重算复核（B7：数字-出处核对，演示算术核验）----
    mom_mock = [None] + [
        round((MOCK_HOST[i] - MOCK_HOST[i - 1]) / MOCK_HOST[i - 1] * 100, 1)
        for i in range(1, len(MOCK_HOST))
    ]
    # IncubationCarrierNewPage.jsx:250 UI 公式复刻：首点 null，其余 (v[i]-v[i-1])/v[i-1]*100 保留 1 位
    assert mom_mock[1] == 17.1 and mom_mock[3] == -5.3 and mom_mock[9] == 11.0

    out = {
        "metric_id": "M_SCIUI_P10_065",
        "batch": "S3-09",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview-new/incubation-carrier-new/IncubationCarrierNewPage.jsx:249-264",
            "repos/demo-ui-science/src/pages/achievement-preview-new/incubation-carrier-new/IncubationCarrierNewPage.jsx:1318",
            "repos/demo-ui-science/src/pages/achievement-preview-new/incubation-carrier-new/mockData.js:813-817",
            "repos/demo-ui-science/src/pages/tech-service/TechExchange.jsx:139-143",
            "repos/demo-ui-science/src/pages/tech-service/TechCompetition.jsx:143-151",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "三份说明书未出现「指标环比增速（较上一统计周期）」指标名；清单 mean 注明科技企业孵化器运营监测平台场景，口径注记「和上年同期比还是和上一期比，见指标名称」——本件挂载为环比（MoM/QoQ）非同比（YoY）。清单登记 row_01=684，mount=IncubationCarrierNewPage.jsx:253/:262（实查 :249-264 环比计算块）。",
        },
        "facts": {
            "ui_mount": "IncubationCarrierNewPage.jsx:249-264 investmentOption 计算块：const mom = values.map((v,i)=> i===0?null:+(((v-values[i-1])/values[i-1])*100).toFixed(1))——环比增速由前端对宿主序列现算，非独立数据；:1318 绩效监控 Tab 投资趋势图渲染（bar 季度投资总额 + line 环比增速双轴）",
            "ui_host_series": "mockData.js:813-817 operations.investment：labels 2024Q1-2026Q2 十季 + values [8.2, 9.6, 11.4, 10.8, 12.6, 14.2, 13.5, 15.8, 16.4, 18.2] 亿元——宿主=季度投资总额（演示值，ui_demo_fallback）",
            "ui_mom_demo": "mock 环比重算复核：+17.1/+18.8/-5.3/+16.7/+12.7/-4.9/+17.0/+3.8/+11.0（首点 null）——B7 算术核验通过，与 UI 前端公式逐点一致",
            "ui_kpi_change": "科技交流页 KPI change%（TechExchange.jsx:139-143：18.5/22.3/15.2/12.8）与科技竞赛页（TechCompetition.jsx:143-151：25.6/32.1/28.5/18.3）为环比语义变体挂载（KPI 卡涨跌幅）——同为前端硬编码演示值",
            "ui_formula_definer": "UI 前端自带公式（(v[i]-v[i-1])/v[i-1]*100，首点 null，保留 1 位）——公式定义人=前端组件，无外部权威口径",
            "jiuxin_mom_column_hits": jiuxin["jiuxin_mom_ratio_column_hits"],
            "dev_mom_column_note": "dev growth_rate/yoy/ratio 列命中全为产业链/政策/企业面自建 ADS 列（chain_* 族 growth_rate、policy_* 族 yoy），无孵化器运营季度序列宿主",
            "jiuxin_soft_science_family": jiuxin["jiuxin_soft_science_family"],
            "gkx_table_count": gkx["gkx_table_count"],
            "dev_table_total": dev["dev_table_total"],
            "jiuxin_table_count_live": jiuxin["jiuxin_table_count_live"],
        },
        "derived": [
            {
                "name": "host_indicator_support_chain",
                "value": {
                    "host_ui": "季度投资总额（incubation-carrier-new operations.investment）",
                    "host_probe_dev": "dev 542 表无孵化器运营/投资季度序列面（carrier 族仅 dim.carrier 28 行静态维表 + dwd.enterprise_innovation_carrier 0 行空壳，S3-08 laneC 快照）",
                    "host_probe_gkx": "gkx 280 表无 incub/投资序列面（carrier 族 0 命中，S3-08 laneC 快照）",
                    "host_probe_jiuxin": "jiuxin 218 表 incub/carrier 族 0 命中（S3-08 laneC 快照）；ads_* 年度序列面（geo/collab 等）均为论文域语义，非孵化器投资流水",
                    "chain_verdict": "宿主指标（季度投资总额）三源零承载 → 环比增速随之零承载（依赖链传导）",
                },
                "note": "依赖链判定：环比增速是二阶指标——先有宿主序列，才有环比。清单场景宿主=孵化器季度投资总额，其承载面（孵化器运营/投资台账）三源零承载（S3-08 INCUB 族已证，laneC 快照互证）；本批 dev/jiuxin 环比比例列扫描（growth_rate/yoy/mom 等 20+ 列命中）全为产业链/专利/论文域预计算列，无孵化器域。宿主零承载则本件判零承载。",
            },
            {
                "name": "mom_formula_recheck",
                "value": {"host": MOCK_HOST, "labels": MOCK_LABELS, "mom_pct": mom_mock},
                "note": "mock 环比重算（B7 核验）：UI 公式 (v[i]-v[i-1])/v[i-1]*100 首点 null；重算与前端渲染值逐点一致（如 2024Q2=+17.1%/2024Q4=-5.3%/2026Q2=+11.0%）。演示算术核验仅证明前端公式实现正确，不构成数据支持。",
            },
        ],
        "absence_probe": [
            {
                "probe": "宿主序列面：孵化器运营/投资季度台账（incub|carrier|investment + quarterly/monthly 序列）",
                "source": "dev+gkx+jiuxin",
                "sql": "S3-08 laneC 快照 carrier/incub 词族 + 本批 s309 gamma 复扫（dev_table_total=542/gkx_table_count=280/jiuxin_table_count_live=218）",
                "hits": 0,
                "verdict": "dev dim.carrier 28 行静态维表+dwd.enterprise_innovation_carrier 0 行空壳；gkx carrier 族 0；jiuxin incub/carrier 族 0——宿主台账三源零承载",
            },
            {
                "probe": "环比/同比比例列（mom|qoq|yoy|growth_rate|month_growth_rate 等词族）全库列扫描",
                "source": "dev+jiuxin",
                "sql": "information_schema.columns（dev）/ 逐表 DESCRIBE（jiuxin）（快照 dev_mom_ratio_column_hits / jiuxin_mom_ratio_column_hits）",
                "hits": "dev 60+ 列 / jiuxin 21 列",
                "verdict": "命中全为异域预计算列：dev chain_*/policy_*/enterprise_* 族 growth_rate/yoy（产业链与政策域）；jiuxin ads_patent_analysis_* growth_rate、ads_research_problem_monthly_metrics month_growth_rate（专利/论文域）——无孵化器运营域环比结果面，且均为宿主已算好的比例列非本件「通用环比引擎」",
            },
            {
                "probe": "软科学成果年度序列（P10_066 姊妹件的宿主候选，交叉登记）",
                "source": "jiuxin",
                "sql": "SHOW TABLES + soft_science/topic 词族（快照 jiuxin_soft_science_family）",
                "hits": 16,
                "hit_tables_head": ["ads_discipline_topic", "ads_emerging_topic_yearly_metrics", "ads_institution_topic_entry", "ads_project_topic"],
                "verdict": "全为论文/专利域 topic 族（OpenAlex 语义），非软科学成果（课题报告/政策研究）主档——软科学域宿主亦零承载（P10_066 另证）",
            },
        ],
        "support_judgment": "完全不支持",
        "notes": [
            "判档理由（依赖链传导）：环比增速=宿主指标序列的一阶差分百分比，是二阶（复合）指标。清单场景宿主=孵化器季度投资总额（operations.investment 十季序列），其承载面（孵化器运营/投资台账）经 S3-08 INCUB 族与 S3-08/09 两批快照证明三源零承载；三源虽存在大量 growth_rate/yoy 预计算列（dev 60+/jiuxin 21），但全部为产业链/专利/论文域异域宿主的比例列，无孵化器域，且非「任意宿主可插拔的环比引擎」。宿主零承载 → 环比无从差分，判完全不支持。",
            "口径裁定：清单 mean 注记「和上年同期比还是和上一期比，见指标名称」——本件名称为「较上一统计周期」即环比（MoM/QoQ），非同比（YoY）；UI 前端公式 (v[i]-v[i-1])/v[i-1]*100 与环比口径一致。三源 yoy 列（ads_research_outcome_yearly_metric.year_over_year_growth_rate 等）即便可用也是同比口径，与本件环比口径不同。",
            "复用性说明：若未来任一宿主指标序列入湖（如孵化器运营台账、软科学成果年度序列），本件随宿主即活——环比计算本身零边际成本（前端公式已实现且经 B7 核验正确）。",
            "UI mock 宿主序列十季 8.2→18.2 亿元与 KPI 涨跌幅（18.5%/22.3% 等）均为演示值，不参与支持度结论（ui_demo_fallback 披露）。",
            "本件为薄壳：共享探针 code/_shared_s309_gamma.py + 快照；本脚本含 mock 环比重算断言（B7）。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021-2026"],
        "base_years_note": "环比基期=上一统计周期（宿主序列相邻两点），非日历年。宿主台账零承载故无任何周期可用。mock 时轴 2024Q1-2026Q2 十季（首点无环比）；若接入宿主台账，基期轴取季度（QoQ），与清单「较上一统计周期」口径一致。",
        "ctx_refs": {
            "note": "正文引用型数字登记",
            "refs": sorted(["17.1", "18.8", "-5.3", "16.7", "12.7", "-4.9", "17.0", "3.8", "11.0", "8.2", "18.2", "10", "542", "280", "218", "28", "0", "60", "21", "16", "18.5", "22.3", "25.6", "32.1", "2024Q1", "2026Q2"]),
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 完全不支持（依赖链：宿主零承载→环比零承载）| mom demo recheck:", mom_mock)


if __name__ == "__main__":
    main()
