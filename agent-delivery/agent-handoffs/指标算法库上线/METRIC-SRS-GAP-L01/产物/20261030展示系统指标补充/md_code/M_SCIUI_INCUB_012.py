#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INCUB_012 在孵企业毕业率 —— 薄壳校验脚本（部分支持件）。

UI 三挂载：
- 新版页 IncubationCarrierNewPage.jsx:1396 载体详情抽屉「毕业率 `(graduateRate*100).toFixed(1)%`」
- 新版页 :392 KPI「avgGraduateRate」（enterpriseCount 加权）
- 旧版页 IncubationCarrierPage.jsx:706/:710 毕业率折线（孵化毕业统计图，与 SOFTSCI_007 同图不同挂载行）
数据根因与 SOFTSCI_007 同（毕业语义零承载），但本件为 rate 字段独立留证：
新版页 19 载体 graduateRate 0.15-0.38；dev 链路 tenant 可近似分母、分子缺。
"""
from __future__ import annotations

import json

import pymysql

OUT = "M_SCIUI_INCUB_012_out.json"
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600", charset="utf8mb4")

# 新版页 mockData.js 19 载体 graduateRate（:48,60,72,84,96,108,120,132,144,156,168,180,192,204,216,228,240,252,264,276,288,300 行）
NEW_PAGE_RATES = [0.36, 0.33, 0.29, 0.22, 0.27, 0.38, 0.30, 0.31, 0.20, 0.32, 0.34, 0.28, 0.19, 0.37, 0.30, 0.26, 0.29, 0.24, 0.33, 0.18, 0.21, 0.15]
# 旧版页五载体（与 SOFTSCI_007 同 mock）：(inIncubation, graduated)
OLD_PAGE_PAIRS = [(86, 24), (112, 38), (64, 19), (58, 12), (72, 16)]


def main() -> None:
    conn = pymysql.connect(database="gkxlumenx_dim", **DEV)
    cur = conn.cursor()
    cur.execute("SELECT rel_type, COUNT(*) FROM carrier_org_rel GROUP BY rel_type ORDER BY rel_type")
    rel = dict(cur.fetchall())
    cur.execute("SELECT COUNT(*) FROM carrier")
    carriers = cur.fetchone()[0]
    conn.close()

    assert rel == {"self": 18, "tenant": 39}
    assert carriers == 28

    old_rates = [round(g / (i + g) * 100) for i, g in OLD_PAGE_PAIRS]

    out = {
        "metric_id": "M_SCIUI_INCUB_012",
        "batch": "S3-07-L2",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview-new/incubation-carrier-new/IncubationCarrierNewPage.jsx:1396",
            "repos/demo-ui-science/src/pages/achievement-preview-new/incubation-carrier-new/IncubationCarrierNewPage.jsx:392",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/incubation-carrier/components/IncubationCarrierPage.jsx:706",
        ],
        "facts": {
            "ui_mount_drawer": "IncubationCarrierNewPage.jsx:1396 载体详情抽屉详细资料 Descriptions「毕业率 `(graduateRate*100).toFixed(1)%`」",
            "ui_mount_kpi": "IncubationCarrierNewPage.jsx:392 avgGraduateRate = Σ(graduateRate×enterpriseCount)/ΣenterpriseCount ×100（enterpriseCount 加权）",
            "ui_mount_old_line": "IncubationCarrierPage.jsx:706-710 旧版页孵化毕业统计图毕业率折线 round(graduated/(inIncubation+graduated)×100)（与 SOFTSCI_007 同图，本件挂折线系列行）",
            "ui_mock_new_rates": "mockData.js 19+ 载体 graduateRate 0.15-0.38（小数制）",
            "ui_mock_old_rates": f"旧版五载体毕业率 {old_rates}（整数百分比，mock (86,24)(112,38)(64,19)(58,12)(72,16)）",
            "ui_mock_note": "mock 为演示值不参与判档；新版小数制×100 展示 vs 旧版整数制——两页口径形态不同（ui_demo_fallback 披露）",
            "dev_carrier_rows": carriers,
            "dev_rel_type_domain": rel,
            "denominator_note": "分母近似可用：tenant=39 在驻企业（SOFTSCI_007 已证近似口径）",
            "numerator_note": "分子零承载：rel_type 域={self,tenant} 无毕业态、end_date 全 NULL、无毕业名单表",
            "dev_empty_indicator_tables": ["gkxlumenx_dwd.enterprise_innovation_carrier=0", "gkxlumenx_ads.carrier_index=0"],
            "gkx_table_count": 280,
            "jiuxin_table_count_live": 218,
            "named_in_srs": False,
            "named_note": "三份说明书未出现「在孵企业毕业率」指标名（检索记录附录 A）。",
        },
        "derived": [
            {"name": "carrier_graduate_rate", "value": None,
             "reason": "分子（毕业企业数）零承载；分母可近似（tenant 在驻 39）。分子分母不同源同裂，禁拼半真指标。"},
            {"name": "avg_graduate_rate_weighted", "value": None,
             "reason": "KPI 加权均值依赖单载体率，同上不可算。"},
            {"name": "mock_reference", "value": {"new_page_range": [0.15, 0.38], "old_page_pct": old_rates},
             "disclosure": "ui_demo_fallback：mock 演示值。权威达标线参照：工信部 2025 标准级孵化器 ≥10%（上年度毕业企业在孵占比）；火炬 2019 指标体系 2.2 权重 4 分"},
        ],
        "absence_probe": [
            {"probe": "dev 542 表 incub/graduat 词族 + rel_type 域实查", "source": "dev",
             "sql": "information_schema.columns 词族扫描（快照）+ carrier_org_rel GROUP BY rel_type 实连",
             "hits": 4, "graduation_semantics": 0},
            {"probe": "gkx 280 表 incub/graduat 词族", "source": "gkx",
             "sql": "information_schema.columns 词族扫描（快照）", "hits": 0},
            {"probe": "jiuxin 218 表（SHOW TABLES 实数）incub/graduat 词族", "source": "jiuxin",
             "sql": "SHOW TABLES+列扫描（快照）", "hits": 0},
        ],
        "support_judgment": "部分支持",
        "notes": [
            "判档理由：与 SOFTSCI_007 同数据根因（毕业语义零承载）但本件是 rate 字段件：分母（在孵数）可由 tenant=39 近似，分子（毕业数）零承载——单一比率缺分子，判部分支持（子项=分母侧）。同族双件独立留证不互引代替。",
            "口径差登记：新版页 graduateRate 为小数制（0.36→36.0%）且 KPI 为 enterpriseCount 加权；旧版页为整数百分比 + 分母=在孵+已毕业。权威口径（火炬 2.2/工信部六(八)）分母=在孵企业总数。",
            "工信部 2025 标准级达标线 10%：mock 19 载体全部 ≥15%（0.15-0.38），演示值高于达标线下限——仅量级参照非真实结论。",
            "本件为薄壳：复用 SOFTSCI_007 探针结论（独立重跑 rel_type 断言）+ 新版页 mock 实读。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021", "2022", "2023", "2024", "2025", "2026"],
        "base_years_note": "毕业率无年度观测（end_date 全 NULL 无迁出时间；carrier_index.stat_period 0 行）；毕业态数据接入后首个完整考核年为基期。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted({
            "0.15", "0.38", "0.36", "0.33", "0.29", "0.22", "0.27", "0.38", "30", "31", "25", "23", "17", "18", "22",
            "39", "28", "57", "18", "10", "4", "19", "542", "280", "218",
        })},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 部分支持 | old rates:", old_rates, "| rel:", rel, "| carriers:", carriers)


if __name__ == "__main__":
    main()
