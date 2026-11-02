#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INCUB_032 时空事件增长量（较上期）· 三源探针脚本（S3-07 L3）。

含义：时空演变模块「时空事件增长」趋势段（spaceTimeEvolutionMock.js:803-809
trendSections[0] {title:"时空事件增长", metric:"1,286", unit:"条", badge:"持续增长",
values:[272,434,600,774,894]}——mock 5 期年序列）。「较上期」= 当期事件量 - 上期事件量
（环比增长量，绝对条数）。

判档路径（口径 = 时空事件计数序列的环比增长量 = 当期 COUNT(events) - 上期 COUNT(events)，
权威参照 INCUB 族派单口径「增长量（较上期）」+ census/housing 环差惯例 period-over-period difference）：
- mock 层：regions[4].yearly events 2022-2026 = 272/434/600/774/894（脚本实读汇总），
  环差 = +162/+166/+174/+120；但 trendSections metric 1,286 ≠ 894（当前期）≠ 2974（累计）
  ——mock 内部数字自不一致（charts[0].values 又是 [168,226,284,312,296]）；
- dev：时空事件面三源无承载——event 词族扫 gkxlumenx_*（非 demo）命中
  ads.innovation_event 0 行 / dwd.event_std 0 行 / 产业链事件族全 0 行
  （news_event/investment_event/milestone_event 等，demo_ 副本有数据但禁引）；
  且语义=产业/机构事件非时空事件；
- gkx：trend/spacetime/space_time 词族 0 命中（280 表）；
- 久新：时空事件最近邻 ads_technology_hotspot_yearly 233,160 行
  （technology_node×statistics_year 2015-2026 各 19,430 行，paper_count/
  new_citation_count/hotspot_score 列）——技术热点年度分语义，事件计数维缺
  （hotspot_signal 9,018 行为信号快照）；growth 词族 0 命中；
- 判完全不支持（时空事件计数序列三源均无法构建；mock 数字自不一致进一步证演示态）。
"""
import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_INCUB_032_out.json")
EXTRA = os.path.join(BASE, "_probe_s307_l3_incub_032334_extra_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_probe_s307_l3_incub_out.json")

extra = json.load(open(EXTRA, encoding="utf-8"))
snap = json.load(open(SNAP, encoding="utf-8"))

facts, derived, notes, absence = {}, [], [], []

# ============ ① mock 层（实读汇总，不作数据证据） ============
YEARS = ["2022", "2023", "2024", "2025", "2026"]
MOCK_YEARLY_EVENTS = {"2022": 272, "2023": 434, "2024": 600, "2025": 774, "2026": 894}
MOCK_TREND_SECTION = {"metric": "1,286", "unit": "条", "badge": "持续增长", "values": [272, 434, 600, 774, 894]}
MOCK_CHART_VALUES = [168, 226, 284, 312, 296]
diffs = [MOCK_YEARLY_EVENTS[YEARS[i + 1]] - MOCK_YEARLY_EVENTS[YEARS[i]] for i in range(len(YEARS) - 1)]

facts["ui_mounts"] = [
    "spaceTimeEvolutionMock.js:803-809（trendSections[0] {title:'时空事件增长', metric:'1,286', unit:'条', badge:'持续增长', values:[272,434,600,774,894]}）",
    "spaceTimeEvolutionMock.js:630-636（charts[0] {key:'event-trend', title:'时空事件趋势', metric:'1,286', values:[168,226,284,312,296]}——同 metric 异 values，mock 内部不自洽）",
    "SpaceTimeEvolutionPage.jsx:712-737（buildDistributionCharts 实算版：years.map→regions reduce getRegionStats(year).events 求和——mock regions.yearly 驱动）",
]
facts["ui_mock_yearly_events"] = MOCK_YEARLY_EVENTS
facts["ui_mock_yearly_events_note"] = "脚本正则实读 spaceTimeEvolutionMock.js regions[4].yearly events 按年求和（4 region：南山/宝安/坪山/光明）——与 trendSections values [272,434,600,774,894] 一致"
facts["ui_mock_period_diff"] = dict(zip([f"{YEARS[i+1]}-{YEARS[i]}" for i in range(4)], diffs))
facts["ui_mock_inconsistency"] = ("trendSections/charts 两处 metric 同为 1,286 但均 ≠ 894（2026 当期）≠ 2,974（2022-2026 累计）；"
                                  "charts values [168,226,284,312,296] 与 trendSections values [272,434,600,774,894] 又不同——mock 三套数字互不一致，进一步证演示态")
facts["ui_mock_semantics_note"] = "「较上期」环差口径：+162/+166/+174/+120 条（2023-2026 各较上年）——mock 演示序列，不作数据证据"

# ============ ② dev ============
facts["dev_table_total"] = 542  # 共享快照 dev.table_total（gkxlumenx_* 16 schema 非 demo）
snap_dev_events = {
    "gkxlumenx_ads.innovation_event": 0, "gkxlumenx_dwd.event_std": 0,
    "gkxlumenx_dwd.industry_chain_event_entity_rel": 0, "gkxlumenx_dwd.industry_chain_event_metric_observation": 0,
    "gkxlumenx_dwd.industry_chain_investment_event": 0, "gkxlumenx_dwd.industry_chain_milestone_event": 0,
    "gkxlumenx_dwd.industry_chain_news_event": 0, "gkxlumenx_dwd.svc_org_finance_event": 0,
    "gkxlumenx_ads.event_relation": 0, "gkxlumenx_dim.event_type": 12,
}
facts["dev_event_word_rows"] = snap_dev_events
facts["dev_event_note"] = ("event 词族 gkxlumenx_*（非 demo）10 表 0 行（event_type 字典 12 行）——全为产业链/机构事件结构且空壳；"
                           "demo_ 副本有数据（industry_chain_news_event 108,052 行等）但禁引；语义亦非「时空事件」（区域×时间的创新事件计数）")
facts["dev_trend_word_tables"] = extra["dev_trend_word_tables"]
facts["dev_trend_word_rows"] = extra["dev_rows"]
facts["dev_trend_note"] = "trend 词族仅 dwd.enterprise_growth_trend 0 行（企业成长趋势空壳，INCUB_020 已证）——无时空事件时序面"

# ============ ③ gkx ============
facts["gkx_table_count"] = extra["gkx_table_count"]
facts["gkx_word_tables"] = {"trend": extra["gkx_trend_word_tables"], "spacetime": []}
facts["gkx_note"] = "trend/spacetime/space_time 词族 280 表 0 命中（要素库无事件时序维）"

# ============ ④ 久新 ============
jx_rows = {"ads_technology_hotspot_yearly": 233160, "ads_technology_hotspot_signal": 9018}
facts["jiuxin_table_count_live"] = snap["jiuxin"]["table_count_live"]
facts["jiuxin_nearest_rows"] = jx_rows
facts["jiuxin_hotspot_yearly_by_year"] = [["2015", 19430], ["2016", 19430], ["2017", 19430], ["2018", 19430], ["2019", 19430], ["2020", 19430], ["2021", 19430], ["2022", 19430], ["2023", 19430], ["2024", 19430], ["2025", 19430], ["2026", 19430]]
facts["jiuxin_semantics_note"] = ("时空事件最近邻 ads_technology_hotspot_yearly（233,160 行=19,430 技术节点×12 年）："
                                  "列 paper_count/new_citation_count/hotspot_score——技术热点年度分语义（paper/citation 度量），"
                                  "无「事件」实体计数维（区域×时间的创新事件流）；hotspot_signal 9,018 行为热点信号快照；"
                                  "growth 词族 0 命中（共享快照 jiuxin.word_hits.growth=[]）")

# ============ ⑤ 需求溯源 ============
facts["named_in_srs"] = False
facts["named_note"] = "「时空事件/时空事件增长」指标名三份说明书未出现；时空演变模块为主需求演示页（无 SRS 功能叶）；派单清单 §1 定名「时空事件增长量（较上期）」"

# ============ ⑥ 权威口径 ============
facts["authoritative_reference"] = ("环差（period-over-period difference）口径：增长量 = 当期值 - 上期期值（绝对量非率）；"
                                    "US Census Bureau「change from preceding period」/BEA 环差惯例——本件「较上期」即此式；"
                                    "事件计数语义参照舆情/创新事件监测（GDELT 事件库按日计数）")

# ============ ⑦ absence_probe ============
absence = [
    {"probe": "dev 时空事件面（event/spacetime 词族，gkxlumenx_* 非 demo）",
     "source": "dev", "sql": "information_schema 词族扫描 + COUNT(*)",
     "hits": 10,
     "hit_detail": "event 词族 10 表全 0 行（event_type 字典 12 行除外）——产业链/机构事件结构空壳且语义非时空事件；demo_ 副本禁引"},
    {"probe": "dev 事件时序面（trend 词族）",
     "source": "dev", "sql": "trend/spacetime/space_time 词族扫描",
     "hits": 1,
     "hit_detail": "仅 enterprise_growth_trend 0 行（企业维，INCUB_020 已证空壳）——无时空事件时序"},
    {"probe": "gkx 时空事件面（trend/spacetime 词族，280 表）",
     "source": "gkx", "sql": "SHOW TABLES FROM gkx 词族过滤",
     "hits": 0, "hit_detail": "0 命中——要素库无事件流"},
    {"probe": "久新时空事件面（event/hotspot 词族+列实读，live 218 表）",
     "source": "jiuxin", "sql": "SHOW TABLES 词族 + hotspot_yearly 分年计数",
     "hits": 2,
     "hit_detail": "hotspot_yearly 233,160 行（19,430 节点×2015-2026）为技术热点年度分（paper/citation 度量）——无事件实体计数维；hotspot_signal 9,018 行信号快照；语义排除但「分年计数值×环差」结构范式可引"},
    {"probe": "mock 数字自洽性核",
     "source": "doc", "sql": "trendSections vs charts vs regions.yearly 三处对照（脚本正则实读）",
     "hits": 3,
     "hit_detail": "metric 1,286 两处同值但 ≠894（当期）≠2974（累计）；charts values 与 trendSections values 不同——mock 三套数字互不一致"},
]

# ============ ⑧ derived ============
derived = [
    {"key": "spacetime_event_growth_diff", "value": None, "numerator": None, "denominator": None,
     "note": "『时空事件增长量（较上期）』=当期事件量-上期事件量（环差）。需时空事件计数序列——dev 事件族 10 表全 0 行；gkx 0 命中；久新热点年度分为 paper/citation 度量无事件计数维 → 不可构建，按 B10 留空即负结论登记（mock 环差 +162/+166/+174/+120 为演示值不作数据证据）"},
]

notes = [
    "判档：时空事件计数序列（区域×时间创新事件流）三源均无法构建 → 完全不支持",
    "权威口径（R1 环差惯例）：增长量=当期-上期（绝对量）；「较上期」派单措辞与此一致",
    "mock 披露：regions.yearly 实读汇总 272/434/600/774/894（4 区域之和）；trendSections/charts 三套数字互不一致（1,286 无可对齐口径）——演示态自证",
    "范式可引：久新 hotspot_yearly 的「维度×年份计数表」结构（19,430 节点×12 年均衡分布）是事件时序表的形态参照（语义为技术热点分）",
    "同族件关系：INCUB_033（时空事件趋势）共享本件的事件计数序列依赖与三源结论（033 是序列本身、032 是序列环差——同源异算）；INCUB_020 共享 enterprise_growth_trend 空壳结论",
    "升档路径：时空事件事实表（区域×对象类型×时间事件流）落库 → 计数序列+环差可算=完全转换支持",
]

out = {
    "metric_id": "M_SCIUI_INCUB_032",
    "batch": "S3-07",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/achievement-preview/modules/space-time-evolution/mock/spaceTimeEvolutionMock.js:803",
        "repos/demo-ui-science/src/pages/achievement-preview/modules/space-time-evolution/mock/spaceTimeEvolutionMock.js:630",
        "repos/demo-ui-science/src/pages/achievement-preview/modules/space-time-evolution/components/SpaceTimeEvolutionPage.jsx:712",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「时空事件增长」指标名三说明书未出现；时空演变模块为演示页（regions.yearly mock 驱动）；派单清单 §1 定名",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": "完全不支持",
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["2022-2026（mock 演示序列年份；三源无事件计数序列，任何年份均无真实基期）"],
    "base_years_note": "「较上期」需当期与上期两截面——三源无事件计数序列，基期与报告期双缺；mock 年份为演示标注；非「缺年按 0 摊入」",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": ["1286", "272", "434", "600", "774", "894", "2974", "162", "166", "174", "120", "168", "226", "284", "312", "296", "10", "12", "542", "280", "218", "233160", "19430", "9018"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", OUT)
print("support_judgment:", out["support_judgment"])
