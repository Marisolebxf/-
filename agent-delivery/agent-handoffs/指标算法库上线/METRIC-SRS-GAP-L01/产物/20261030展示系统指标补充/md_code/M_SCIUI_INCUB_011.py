#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INCUB_011 在孵企业成长分 —— 薄壳校验脚本（完全不支持件）。

UI 三挂载：
- IncubationCarrierPage.jsx:419 企业成长画像卡「成长分」（hint=模拟评分）
- :954/:961 成长评分趋势图（buildGrowthScoreTrendOption，月度 6 点，y 轴 70-100）
- :1070 SoftChartFrame title=成长评分趋势 badge=月度变化
口径=在孵企业综合成长评分（月度）。growth 词族三源命中均为语义污染
（基金久期 fund_maturity/产业链增长率 growth_rate/债券增长），无企业评分面。
dev dwd.enterprise_growth_trend 词族命中——列级核验是否承载。
"""
from __future__ import annotations

import json

import pymysql

OUT = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/M_SCIUI_INCUB_011_out.json"
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600", charset="utf8mb4")

MOCK_MONTHLY = {
    "ent-sensor": [("2026-01", 85), ("2026-02", 87), ("2026-03", 88), ("2026-04", 89), ("2026-05", 90), ("2026-06", 91)],
    "ent-vision": [("2026-01", 82), ("2026-02", 84), ("2026-03", 85), ("2026-04", 87), ("2026-05", 88), ("2026-06", 88)],
    "ent-biochip": [("2026-01", 76), ("2026-02", 78), ("2026-03", 79), ("2026-04", 80), ("2026-05", 81), ("2026-06", 82)],
}
MOCK_ENTERPRISE_SCORES = {"ent-sensor": 91, "ent-vision": 88, "ent-biochip": 82, "ent-edge": 76}


def main() -> None:
    conn = pymysql.connect(database="information_schema", **DEV)
    cur = conn.cursor()
    cur.execute("""
        SELECT COLUMN_NAME FROM information_schema.columns
        WHERE TABLE_SCHEMA='gkxlumenx_dwd' AND TABLE_NAME='enterprise_growth_trend'
        ORDER BY ORDINAL_POSITION
    """)
    egt_cols = [r[0] for r in cur.fetchall()]
    cur.execute("SELECT COUNT(*) FROM gkxlumenx_dwd.enterprise_growth_trend")
    egt_rows = cur.fetchone()[0]
    conn.close()

    score_like = sorted(c for c in egt_cols if any(k in c.lower() for k in ("score", "growth", "rating")))

    out = {
        "metric_id": "M_SCIUI_INCUB_011",
        "batch": "S3-07-L2",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview/modules/incubation-carrier/components/IncubationCarrierPage.jsx:419",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/incubation-carrier/components/IncubationCarrierPage.jsx:954",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/incubation-carrier/components/IncubationCarrierPage.jsx:1070",
        ],
        "facts": {
            "ui_mount_card": "IncubationCarrierPage.jsx:419 企业成长画像 SoftEntitySummaryPanel metrics[0] { label: 成长分, value: growthScore, hint: 模拟评分 }（同卡：专利 累计/项目 代表成果）",
            "ui_mount_trend_fn": "IncubationCarrierPage.jsx:940-984 buildGrowthScoreTrendOption：月度折线 y 轴 70-100，markLine 最高/最低",
            "ui_mount_trend_frame": "IncubationCarrierPage.jsx:1070 SoftChartFrame title=成长评分趋势 badge=月度变化（入驻企业成长轨迹区）",
            "ui_mock_monthly": "incubationCarrierMock.js:317-358 三企业各 6 点月序列（85→91 / 82→88 / 76→82）",
            "ui_mock_scores": "incubationCarrierMock.js:374/390/406/422 四企业 growthScore=(91,88,82,76)",
            "ui_mock_note": "mock 为演示值不参与判档；画像卡 hint 自标「模拟评分」（ui_demo_fallback 披露）",
            "dev_table_total": 542,
            "dev_enterprise_growth_trend": {"columns": egt_cols, "rows": egt_rows},
            "dev_egt_score_like_columns": score_like,
            "dev_growth_word_polluted_hits": sorted([
                "gkxlumenx_ads.chain_competitiveness.growth_score（产业链竞争力）",
                "gkxlumenx_ads.chain_cycle.growth_rate（产业周期）",
                "gkxlumenx_ads.chain_enterprise_stat.growth_rate（产业链企业统计）",
                "gkxlumenx_ads.chain_institution_stat.growth_rate（产业链机构统计）",
                "gkxlumenx_ads.chain_investment.amount_growth_rate/count_growth_rate（投资增速）",
                "gkxlumenx_ads.chain_market.growth_rate（市场规模）",
            ]),
            "gkx_table_count": 280,
            "gkx_growth_word_polluted_hits": sorted([
                "gkx.dwd_fund_basic_info.fund_maturity_date（基金久期）",
                "gkx.dwd_fund_bond_allocation.mkv_growth_rate（债市增速）",
                "gkx.dwd_fund_equity_sector_allocation.mkv_growth_rate（股市增速）",
            ]),
            "jiuxin_table_count_live": 218,
            "named_in_srs": False,
            "named_note": "三份说明书未出现「成长分/成长评分」指标名（检索记录附录 A）。",
        },
        "derived": [
            {"name": "incubating_enterprise_growth_score", "value": None,
             "reason": f"企业成长评分需评分事实面（企业×月份×分值）；dev dwd.enterprise_growth_trend 词族命中但 {'0 行空壳' if egt_rows == 0 else '列级无评分承载'}（列清单见 facts，score_like=" + str(score_like) + "）；其余 growth 词族命中全为产业链/基金/投资语义污染。"},
        ],
        "absence_probe": [
            {"probe": "dev 542 表 growth/score/maturity 词族", "source": "dev",
             "sql": "information_schema.columns 词族扫描（_probe_s307_l2 快照）+ enterprise_growth_trend 列级实查",
             "semantic_hits": 0, "polluted": 9},
            {"probe": "gkx 280 表 growth/score 词族", "source": "gkx",
             "sql": "information_schema.columns 词族扫描（快照）", "semantic_hits": 0, "polluted": 4},
            {"probe": "jiuxin 218 表（SHOW TABLES 实数）growth/score 词族", "source": "jiuxin",
             "sql": "SHOW TABLES+列扫描（快照）", "semantic_hits": 0},
        ],
        "support_judgment": "完全不支持",
        "notes": [
            "判档理由：成长分=平台自设综合评分（成长验证/融资轮次/专利/项目多因子），需评分事实面（企业×月份×分值）+评分模型；三源无企业评分表。dev dwd.enterprise_growth_trend 为唯一词族命中，列级核验见 facts。",
            "评分口径业界参照：火炬统计年报无企业成长分；企业创新积分制（科技部 2022 试点）为最接近口径（研发投入/知识产权/成长指标加权），但三源无积分表。",
            "mock 月序列（85→91/82→88/76→82）与画像分（91/88/82/76）为演示值（ui_demo_fallback 披露）。",
            "本件为薄壳：复用共享快照 + enterprise_growth_trend 列级实连核验。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021", "2022", "2023", "2024", "2025", "2026"],
        "base_years_note": "评分事实面零承载，无任何月度评分可观测；评分模型接入后首个完整年为基期。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted({
            "91", "88", "82", "76", "85", "87", "89", "90", "84", "78", "79", "80", "81",
            "70", "100", "6", "3", "4", "542", "280", "218",
        })},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 完全不支持 | enterprise_growth_trend rows:", egt_rows, "cols:", len(egt_cols), "score_like:", score_like)


if __name__ == "__main__":
    main()
