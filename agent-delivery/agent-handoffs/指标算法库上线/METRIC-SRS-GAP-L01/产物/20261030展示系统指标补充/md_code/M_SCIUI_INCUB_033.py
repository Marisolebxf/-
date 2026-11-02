#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INCUB_033 时空事件趋势（时序）· 三源探针脚本（S3-07 L3）。

含义：时空演变模块「时空事件趋势」时序图（SpaceTimeEvolutionPage.jsx:724
buildDistributionCharts 返回 {key:"event-trend", values: eventValues}——按
distributionYears 2022-2026 对 regions.yearly.events 求和的 5 点时序；mock
charts[0] 静态版 values [168,226,284,312,296] metric 1,286 条）。

判档路径（口径 = 时空事件计数年度时序 = [COUNT(events, y) for y in years]）：
- 与 INCUB_032 同源异算：032 是序列的环差、033 是序列本身——依赖同为
  「时空事件计数序列」，三源结论共享（独立留证）；
- dev：event 词族 10 表全 0 行（innovation_event/event_std/产业链事件族）；
  trend 词族仅 enterprise_growth_trend 0 行——事件时序无承载；
- gkx：trend/spacetime 词族 280 表 0 命中；
- 久新：ads_technology_hotspot_yearly 233,160 行（19,430×12 年）技术热点
  年度分（paper/citation 度量）——最近邻语义排除；其 hotspot_score_yoy_change/
  rolling_3y_score/trend_status 列证明「年度分×时序衍生」结构范式在库可仿；
- mock：组件实算链（regions.yearly 驱动）与 charts 静态值两套并存且不一致
  （组件实算 272/434/600/774/894 vs charts [168,226,284,312,296]）；
- 判完全不支持（时空事件计数时序三源均无法构建）。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_INCUB_033_out.json")
EXTRA = os.path.join(BASE, "_probe_s307_l3_incub_032334_extra_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_probe_s307_l3_incub_out.json")

extra = json.load(open(EXTRA, encoding="utf-8"))
snap = json.load(open(SNAP, encoding="utf-8"))

facts, derived, notes, absence = {}, [], [], []

# ============ ① mock 层 ============
facts["ui_mounts"] = [
    "SpaceTimeEvolutionPage.jsx:712-737（buildDistributionCharts：years.map→regions filter→getRegionStats(year).events reduce 求和——组件实算时序，values 随筛选联动）",
    "SpaceTimeEvolutionPage.jsx:46（distributionYears=['2022','2023','2024','2025','2026'] 硬编码）+ :388-390（getRegionStats 读 region.yearly[year]）",
    "spaceTimeEvolutionMock.js:630-636（charts[0] 静态版 {key:'event-trend', metric:'1,286', values:[168,226,284,312,296]}）",
    "spaceTimeEvolutionMock.js:795-801（region periodStats 短周期版：12m/90d/quarter/month current/previous 双截面 events）",
]
facts["ui_mock_computed_series"] = {"2022": 272, "2023": 434, "2024": 600, "2025": 774, "2026": 894}
facts["ui_mock_chart_static_values"] = [168, 226, 284, 312, 296]
facts["ui_mock_periodstats_12m_head"] = {"nanshan_current": 186, "nanshan_previous": 148}
facts["ui_mock_semantics_note"] = ("组件实算链（regions.yearly 求和 272/434/600/774/894）与 mock charts 静态 values "
                                   "[168,226,284,312,296] 两套并存且数字不一致（同 metric 1,286）——演示态；"
                                   "短周期（12m 等）走 periodStats current/previous 双截面，同为手写")

# ============ ② dev ============
facts["dev_table_total"] = 542
snap_dev_events = {
    "gkxlumenx_ads.innovation_event": 0, "gkxlumenx_dwd.event_std": 0,
    "gkxlumenx_dwd.industry_chain_event_entity_rel": 0, "gkxlumenx_dwd.industry_chain_event_metric_observation": 0,
    "gkxlumenx_dwd.industry_chain_investment_event": 0, "gkxlumenx_dwd.industry_chain_milestone_event": 0,
    "gkxlumenx_dwd.industry_chain_news_event": 0, "gkxlumenx_dwd.svc_org_finance_event": 0,
    "gkxlumenx_ads.event_relation": 0, "gkxlumenx_dim.event_type": 12,
}
facts["dev_event_word_rows"] = snap_dev_events
facts["dev_event_note"] = ("event 词族 gkxlumenx_*（非 demo）10 表 0 行（event_type 字典 12 行）——"
                           "产业链/机构事件结构空壳且语义非时空事件；demo_ 副本有数据（news_event 108,052 行）禁引")
facts["dev_trend_word_tables"] = extra["dev_trend_word_tables"]
facts["dev_trend_word_rows"] = extra["dev_rows"]
facts["dev_trend_note"] = "trend 词族仅 enterprise_growth_trend 0 行（企业维空壳，INCUB_020 同证）——无事件年度时序面"

# ============ ③ gkx ============
facts["gkx_table_count"] = extra["gkx_table_count"]
facts["gkx_word_tables"] = {"trend": extra["gkx_trend_word_tables"], "spacetime": []}
facts["gkx_note"] = "trend/spacetime/space_time 词族 280 表 0 命中（要素库无事件时序维）"

# ============ ④ 久新 ============
jx = snap["jiuxin"]
facts["jiuxin_table_count_live"] = jx["table_count_live"]
facts["jiuxin_nearest_rows"] = {"ads_technology_hotspot_yearly": 233160, "ads_technology_hotspot_signal": 9018}
facts["jiuxin_hotspot_yearly_trend_cols"] = [c for c in jx.get("ads_technology_hotspot_yearly_cols", [])
                                             if c in ("statistics_year", "hotspot_score", "hotspot_score_yoy_change",
                                                      "hotspot_score_yoy_rate", "rolling_3y_score", "trend_status",
                                                      "paper_activity_score", "citation_attention_score")]
facts["jiuxin_semantics_note"] = ("最近邻 ads_technology_hotspot_yearly（233,160 行=19,430 节点×2015-2026 各年）："
                                  "自带时序衍生列 hotspot_score_yoy_change/_yoy_rate/rolling_3y_score/trend_status——"
                                  "「年度分×时序衍生」结构范式在库可仿；但度量=技术热点分（paper/citation）非事件计数——语义排除；"
                                  "growth 词族 0 命中")

# ============ ⑤ 需求溯源 ============
facts["named_in_srs"] = False
facts["named_note"] = "「时空事件趋势」指标名三份说明书未出现；时空演变模块为主需求演示页；派单清单 §1 定名（挂载 SpaceTimeEvolutionPage.jsx:724 + mock:630 双点）"

# ============ ⑥ 权威口径 ============
facts["authoritative_reference"] = ("事件计数时序口径：GDELT 事件库按日/周/月计数作时间序列（update frequency 固定、"
                                    "时区口径披露）；OECD Main Science and Technology Indicators 年度指标时序惯例——"
                                    "固定年份网格+缺失年显式标注；本件 mock 年粒度（2022-2026 五点）")

# ============ ⑦ absence_probe ============
absence = [
    {"probe": "dev 时空事件时序面（event/trend 词族，gkxlumenx_* 非 demo）",
     "source": "dev", "sql": "information_schema 词族扫描 + COUNT(*)",
     "hits": 11,
     "hit_detail": "event 词族 10 表全 0 行 + trend 词族 enterprise_growth_trend 0 行（企业维）——事件年度时序无承载；demo_ 副本禁引"},
    {"probe": "gkx 事件时序面（trend/spacetime 词族，280 表）",
     "source": "gkx", "sql": "SHOW TABLES FROM gkx 词族过滤",
     "hits": 0, "hit_detail": "0 命中——要素库无事件流时序"},
    {"probe": "久新事件时序面（hotspot 词族+列实读，live 218 表）",
     "source": "jiuxin", "sql": "SHOW TABLES 词族 + hotspot_yearly 时序列实读",
     "hits": 2,
     "hit_detail": "hotspot_yearly 233,160 行自带 yoy_change/rolling_3y_score/trend_status 时序衍生列——结构范式可仿；但度量=paper/citation 热点分非事件计数——语义排除"},
    {"probe": "mock 时序数字自洽性核（组件实算 vs charts 静态）",
     "source": "doc", "sql": "buildDistributionCharts 求和链 vs charts[0].values 对照",
     "hits": 2,
     "hit_detail": "组件实算（regions.yearly 求和）272/434/600/774/894 ≠ charts 静态 [168,226,284,312,296]（同 metric 1,286）——两套演示数字不一致"},
]

# ============ ⑧ derived ============
derived = [
    {"key": "spacetime_event_yearly_series", "value": None, "numerator": None, "denominator": None,
     "note": "『时空事件趋势（时序）』=[COUNT(events,y) for y in years] 年度时序。与 INCUB_032 同源异算（033=序列本身/032=序列环差）——"
               "依赖同为事件计数序列：dev 事件族 10 表 0 行、gkx 0 命中、久新热点年度分语义排除 → 不可构建，按 B10 留空即负结论登记"},
]

notes = [
    "判档：时空事件计数时序三源均无法构建 → 完全不支持（与 032 共享上游结论，独立留证）",
    "权威口径（R1 GDELT/R2 OECD）：事件计数时序=固定年份网格+计数；OECD 惯例缺失年显式标注（不插零）",
    "mock 披露：组件实算链与 charts 静态两套数字不一致（272/434/600/774/894 vs 168/226/284/312/296）——演示态自证；periodStats 短周期双截面亦手写",
    "范式可引：久新 hotspot_yearly 的 yoy_change/rolling_3y_score/trend_status 衍生列证明「年度表→时序衍生」加工范式在库成熟（语义为技术热点分）",
    "同族件关系：INCUB_032（环差）同源异算共享结论；INCUB_020 共享 enterprise_growth_trend 空壳结论；INCUB_034（通用时间趋势分析）为软科学侧另一趋势件（不同模块不同判）",
    "升档路径：时空事件事实表落库 → 年度时序+环差+短周期一次到位（032/033 联动升完全转换支持）",
]

out = {
    "metric_id": "M_SCIUI_INCUB_033",
    "batch": "S3-07",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/achievement-preview/modules/space-time-evolution/components/SpaceTimeEvolutionPage.jsx:724",
        "repos/demo-ui-science/src/pages/achievement-preview/modules/space-time-evolution/components/SpaceTimeEvolutionPage.jsx:46",
        "repos/demo-ui-science/src/pages/achievement-preview/modules/space-time-evolution/mock/spaceTimeEvolutionMock.js:630",
        "repos/demo-ui-science/src/pages/achievement-preview/modules/space-time-evolution/mock/spaceTimeEvolutionMock.js:795",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「时空事件趋势」指标名三说明书未出现；时空演变模块为演示页；派单清单 §1 定名",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": "完全不支持",
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["2022-2026（mock 演示年份网格；三源无事件计数序列，任何年份均无真实数据）"],
    "base_years_note": "时序件需完整年份网格（OECD 惯例缺失年显式标注不插零）；三源无序列全年份皆缺；mock 年份为演示标注；非「缺年按 0 摊入」",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": ["272", "434", "600", "774", "894", "168", "226", "284", "312", "296", "1286", "186", "148", "10", "12", "542", "280", "218", "233160", "19430", "9018"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", OUT)
print("support_judgment:", out["support_judgment"])
