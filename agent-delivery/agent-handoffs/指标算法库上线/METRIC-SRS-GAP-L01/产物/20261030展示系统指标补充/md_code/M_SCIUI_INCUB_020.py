#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INCUB_020 载体平均增长率（年）· 三源探针脚本（S3-07 L3）。

含义：时空演进页「演进回放」面板的「平均增长率」——相邻回放快照时空事件数的环比
变化率（%）。UI：SpaceTimeEvolutionPage.jsx:1126（buildPlaybackFeatureItems
growthRate 项）+ :1042 formatGrowthRate。mock 源 spaceTimeEvolutionMock.js
playback.snapshots.year[].metrics.events（272/434/600/774/894 → 环比
59.6%/38.2%/29.0%/15.5%，均值 35.6%）。

判档路径（口径 = 载体存量年度环比/CAGR，权威 Eurostat AAGR/BEA 复利式）：
- 计算前提是「载体主档年度序列（新增/备案时间）」——三源：
  dev：dim.carrier 28 行（v1_approx 主档，无成立/备案年份列——9 列全读）；
  dwd.enterprise_innovation_carrier 0 行（publish_date 列在但空壳）；
  ads.carrier_index 0 行（stat_period/index_score 在但空壳）；
  gkx：incub/carrier 词族 0 命中；
  久新：incub 词族 218 表 live 复核 0 命中；
- UI 侧口径实为「回放快照 events 序列环比」（formatGrowthRate =
  (cur-prev)/prev*100 toFixed(1)），mock 值 18.4% 环比是 KPI trendLabel；
- 判完全不支持（载体年度序列与事件快照序列两层三源均无数据承载）。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_INCUB_020_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s307_l3_incub_out.json")

facts, derived, notes, absence = {}, [], [], []
probe = json.load(open(PROBE, encoding="utf-8"))

# ============ ① mock 层（UI 语义披露，不作数据证据） ============
SNAP_EVENTS = [272, 434, 600, 774, 894]  # 2022-2026 年快照
facts["ui_mount"] = ("SpaceTimeEvolutionPage.jsx:1126（演进回放面板「平均增长率」growthRate 项，"
                     "formatGrowthRate(metrics.events, previousMetrics.events)）+ :1042（环比公式实现）")
facts["ui_formula_read"] = "formatGrowthRate = ((currentValue - previousValue) / previousValue * 100).toFixed(1)%（:1042-1048 实读）；previous=0 时显示「基准」"
facts["ui_mock_snapshot_events"] = SNAP_EVENTS
facts["ui_mock_snapshot_labels"] = ["2022", "2023", "2024", "2025", "2026"]
yoy = [round((SNAP_EVENTS[i] - SNAP_EVENTS[i-1]) / SNAP_EVENTS[i-1] * 100, 1) for i in range(1, len(SNAP_EVENTS))]
facts["ui_mock_yoy_series"] = yoy  # [59.6, 38.2, 29.0, 15.5]
facts["ui_mock_yoy_mean"] = round(sum(yoy) / len(yoy), 1)  # 35.6
facts["ui_mock_kpi_trendlabel"] = "18.4% 环比（mock KPI 卡 trendLabel，最近一期环比非全期均值——口径差异披露）"
facts["ui_mock_note"] = "mock 演示序列（spaceTimeEvolutionMock.js:436-520 playback.snapshots.year），不参与支持度结论"

# ============ ② dev ============
dev = probe["dev"]
facts["dev_table_total"] = dev["table_total"]
facts["dev_dim_carrier_rows"] = dev["gkxlumenx_dim.carrier"]["rows"]
facts["dev_dim_carrier_cols"] = [c["col"] for c in dev["gkxlumenx_dim.carrier"]["columns"]]
facts["dev_dim_carrier_note"] = "dim.carrier 28 行 9 列（carrier_id/name/carrier_type/carrier_level/operator_org_uid/admin_code/lng/lat/source）——无成立/备案年份列，年度序列无从构建"
facts["dev_enterprise_innovation_carrier_rows"] = dev["gkxlumenx_dwd.enterprise_innovation_carrier"]["rows"]
facts["dev_enterprise_innovation_carrier_cols"] = [c["col"] for c in dev["gkxlumenx_dwd.enterprise_innovation_carrier"]["columns"]]
facts["dev_carrier_index_rows"] = dev["gkxlumenx_ads.carrier_index"]["rows"]
facts["dev_carrier_index_note"] = "carrier_index 0 行（stat_period/index_score/rank 列齐但空壳）；enterprise_innovation_carrier 0 行（publish_date 列在但空壳）——dev 结构面预留、数据未灌"

# ============ ③ gkx / 久新 ============
facts["gkx_table_count"] = probe["gkx"]["table_count"]
facts["gkx_incub_word_tables"] = probe["gkx"]["word_hits"]["incub"]
facts["jiuxin_table_count_live"] = probe["jiuxin"]["table_count_live"]
facts["jiuxin_incub_word_tables"] = probe["jiuxin"]["word_hits"]["incub"]

# ============ ④ 需求溯源 ============
facts["srs_anchor"] = "SRS 科技创新生态展示.md 序号 486「载体年度与季度增量统计」（自动采集年度和季度内新建立和新备案的创新载体数据…同比、环比变化分析）+ 主需求 :3423 同文"
facts["named_in_srs"] = False
facts["named_note"] = "「平均增长率」指标名在三份说明书与主需求均未出现；语义锚为序号 486 增量统计功能分句（环比口径在 UI 实现为快照序列环比）"

# ============ ⑤ 权威口径 ============
facts["authoritative_formula"] = "AAGR/CAGR = (期末值/期初值)^(1/n) - 1（Eurostat AAGR/BEA 复利式）；年度环比 = (本年-上年)/上年×100%（OECD 年度增长率口径）"

# ============ ⑥ absence_probe ============
absence = [
    {"probe": "dev 载体年度序列（成立/备案年份维）",
     "source": "dev", "sql": "SELECT columns+COUNT(*) FROM gkxlumenx_dim.carrier / gkxlumenx_dwd.enterprise_innovation_carrier / gkxlumenx_ads.carrier_index",
     "hits": 0,
     "hit_detail": "dim.carrier 28 行无年份列（9 列全读）；enterprise_innovation_carrier 0 行（publish_date 空壳）；carrier_index 0 行（stat_period 空壳）——载体存量截面有近似主档、年度序列无任何承载"},
    {"probe": "gkx 载体面（incub/carrier 词族，280 表）",
     "source": "gkx", "sql": "information_schema.tables 扫 gkx",
     "hits": 0, "hit_detail": "0 命中——gkx 为论文/专利/机构/学者要素库"},
    {"probe": "久新载体面（incub 词族，live 218 表复核）",
     "source": "jiuxin", "sql": "SHOW TABLES 词族过滤",
     "hits": 0, "hit_detail": "0 命中——ads_* 全系科技要素分析面，无载体资产/年度序列"},
    {"probe": "需求原文「平均增长率」定义段",
     "source": "doc", "sql": "rg 平均增长率 三份说明书+主需求",
     "hits": 0,
     "hit_detail": "指标名 0 命中；序号 486「载体年度与季度增量统计」给出采集要求（新建立/新备案+同比环比）但未定义平均口径；UI 实现为快照序列逐期环比"},
]

# ============ ⑦ derived ============
derived = [
    {"key": "carrier_avg_growth_rate_annual", "value": None, "numerator": None, "denominator": None,
     "note": "『载体平均增长率（年）』需载体年度序列（新备案/存量逐年）——dev dim.carrier 无年份列、序列面双表 0 行；gkx/久新 0 命中 → 不可构建，按 B10 留空即负结论登记"},
    {"key": "ui_mock_yoy_mean_reference", "value": facts["ui_mock_yoy_mean"], "numerator": sum(yoy), "denominator": len(yoy),
     "note": "mock 快照序列环比均值 35.6%（59.6/38.2/29.0/15.5 四期均值）——演示量级参照（B10 披露，不作数据证据）；UI 面板实际展示逐期值非均值"},
]

notes = [
    "判档：载体年度序列两层（存量年份维+增量流水）三源均无数据——dev 唯一近似主档 dim.carrier 28 行 v1_approx 无年份列，序列预留面双 0 行 → 完全不支持",
    "权威口径（R1 Eurostat AAGR/R2 BEA）：平均年增长率=复利式 (期末/期初)^(1/n)-1；R3 OECD 年度口径=本年四季和/上年四季和-1——UI 实现为逐期环比（OECD 式单期），「平均」语义未在需求定义",
    "mock 披露：snapshots.year events=[272,434,600,774,894] 逐期环比 [59.6,38.2,29.0,15.5]%、KPI trendLabel 18.4% 环比——三个数字口径各不相同（逐期/均值/最近期），演示层口径混用已披露",
    "挂载点归属注记：派单书将本件挂 INCUB（创新载体孵化载体 l3=平均增长率），实际挂载在时空演进页回放面板——语义主锚是「时空事件增长率的回放呈现」，载体增量语义锚（序号 486）为需求侧平行锚；两锚共享「年度序列无承载」结论",
    "升档路径：载体备案/成立年份落 dim.carrier 扩列（或 enterprise_innovation_carrier 灌数）→ 年度序列可构建 → 完全转换支持",
]

out = {
    "metric_id": "M_SCIUI_INCUB_020",
    "batch": "S3-07",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/achievement-preview/modules/space-time-evolution/components/SpaceTimeEvolutionPage.jsx:1126",
        "repos/demo-ui-science/src/pages/achievement-preview/modules/space-time-evolution/components/SpaceTimeEvolutionPage.jsx:1042",
        "repos/demo-ui-science/src/pages/achievement-preview/modules/space-time-evolution/mock/spaceTimeEvolutionMock.js:436",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现「平均增长率」指标名；语义锚 SRS 序号 486 载体年度与季度增量统计（主需求 :3423 同文）+ 时空演进回放语义（序号 501）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": "完全不支持",
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["年度基期维整体缺失（载体年度序列三源无承载；mock 序列 2022-2026 为演示）"],
    "base_years_note": "增长率天然依赖基期——基期序列本身无承载是本件判档主因；非「缺年按 0 摊入」",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": ["272", "434", "600", "774", "894", "59.6", "38.2", "29.0", "15.5", "35.6", "18.4", "28", "0", "486", "501", "3423", "542", "280", "218"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", OUT)
print("mock yoy:", yoy, "mean:", facts["ui_mock_yoy_mean"])
print("support_judgment:", out["support_judgment"])
