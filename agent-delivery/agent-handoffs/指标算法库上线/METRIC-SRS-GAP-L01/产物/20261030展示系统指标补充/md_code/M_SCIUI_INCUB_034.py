#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INCUB_034 指标时间趋势分析（通用）· 三源探针脚本（S3-07 L3）。

含义：软科学工作台「时间趋势分析」中心舞台 Tab（SoftScienceWorkbench.jsx:22
stageTabs {key:"trend", label:"时间趋势分析"}→ :941 SoftScienceTrendAnalysis
series={resolvedTrendSeries}）——通用多序列趋势看板：mock trendSeries 3 序列
（成果数量趋势 bar 12 点 1880→2486 项/转化效率趋势 line 8.8→7.4 个月/
重点区域贡献趋势 area 59.4→68.2%），每序列 trend/trendLabel 判读标注。

判档路径（口径 = 通用指标时序分析=多指标×月份粒度序列+趋势判读（涨/跌/平+
斜率/环差），权威参照 OECD MSSTI 时序惯例+Hyndman & Athanasopoulos FPP3
趋势成分分析）：
- 本件是「通用容器件」：本身不绑定单一指标，序列内容随指标接入而定——
  判档看「序列数据面」：mock 3 序列全手写（2025.05-2026.04 十二点）；
- dev：软科学成果序列无表（课题成果主档无表 INCUB_022 已证——成果数量/
  转化周期/区域贡献三序列的上游主档全缺）；trend 词族仅
  enterprise_growth_trend 0 行（企业维空壳）；
- gkx：要素库有原始实体（dwd_patent 等）可作年序列源，但软科学成果语义
  （课题成果/转化周期）不承载——转化周期（立项→示范落地月数）无任何表；
- 久新：ads_city_subfield_resource_yearly 27,722 行（city×subfield×year，
  paper_count/talent_count 年度序列结构在）——科研资源年度序列可作「通用
  时序容器」的演示数据源（非软科学语义）；趋势判读衍生列范式同
  hotspot_yearly（trend_status）；
- 判完全不支持（通用容器的真实序列面：软科学三序列上游主档无表；
  通用时序框架虽可由久新年度表充演示，但「指标时间趋势分析」作为软科学
  工作台 Tab 的实际序列数据三源零承载）。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
EXTRA = os.path.join(BASE, "_probe_s307_l3_incub_032334_extra_out.json")
P031 = os.path.join(BASE, "_probe_s307_l3_incub_031_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_probe_s307_l3_incub_out.json")
OUT = os.path.join(BASE, "M_SCIUI_INCUB_034_out.json")

extra = json.load(open(EXTRA, encoding="utf-8"))
p031 = json.load(open(P031, encoding="utf-8"))
snap = json.load(open(SNAP, encoding="utf-8"))

facts, derived, notes, absence = {}, [], [], []

# ============ ① mock 层 ============
MOCK_SERIES = {
    "total-results": {"title": "成果数量趋势", "unit": "项", "seriesType": "bar", "trend": "up", "trendLabel": "规模仍在上行区间",
                       "points_head": [1880, 1934, 1986], "points_tail": [2415, 2458, 2486], "n_points": 12},
    "conversion-cycle": {"title": "转化效率趋势", "unit": "个月", "seriesType": "line", "trend": "down", "trendLabel": "周期持续缩短",
                          "points_head": [8.8, 8.6, 8.5], "points_tail": [7.6, 7.5, 7.4], "n_points": 12},
    "focus-city-share": {"title": "重点区域贡献趋势", "unit": "%", "seriesType": "area", "trend": "up", "trendLabel": "集聚程度继续增强",
                          "points_head": [59.4, 60.8, 61.6], "points_tail": [67.4, 67.9, 68.2], "n_points": 12},
}
facts["ui_mounts"] = [
    "SoftScienceWorkbench.jsx:22-26（stageTabs {key:'trend', label:'时间趋势分析', icon}→ 中心舞台三 Tab 之一）",
    "SoftScienceWorkbench.jsx:731（resolvedTrendSeries = asArray(workbench.trendSeries)——mock 直取）+ :941（<SoftScienceTrendAnalysis series> 渲染）",
    "SoftScienceTrendAnalysis.jsx:1-95（buildChartGeometry 归一化折线/buildAreaPath 面积/buildTrendSummary 判读——纯前端几何，无数据接口）",
    "design-system/__tests__/SoftDesignSystem.test.jsx:129/138（SoftSegmentedControl「时间趋势分析」Tab 切换契约测试）",
]
facts["ui_mock_series"] = MOCK_SERIES
facts["ui_mock_semantics_note"] = ("3 序列×12 点（2025.05-2026.04）全手写；trend/trendLabel（up/down+判读语）为 mock 常数非计算值；"
                                   "SoftScienceTrendAnalysis 仅做归一化几何渲染（min/max 归一），无统计计算")

# ============ ② dev ============
facts["dev_table_total"] = 542
facts["dev_trend_word_tables"] = extra["dev_trend_word_tables"]
facts["dev_trend_word_rows"] = extra["dev_rows"]
facts["dev_upstream_note"] = ("三序列上游主档全缺：成果数量——课题成果主档无表（INCUB_022 已证）；转化周期（立项→示范落地月数）——"
                              "无任何转化过程表（词族 convert/transfer 0 命中，INCUB_022 同证）；区域贡献——成果×区域关联面无表；"
                              "trend 词族仅 enterprise_growth_trend 0 行（企业维空壳，INCUB_020 同证）")

# ============ ③ gkx ============
facts["gkx_table_count"] = extra["gkx_table_count"]
facts["gkx_word_tables"] = extra["gkx_trend_word_tables"]
facts["gkx_note"] = "trend 词族 280 表 0 命中；gkx 有 dwd_patent 等原始实体可作年序列源，但课题成果/转化周期语义不承载（要素库无软科学成果维）"

# ============ ④ 久新 ============
jx = snap["jiuxin"]
facts["jiuxin_table_count_live"] = jx["table_count_live"]
facts["jiuxin_resource_yearly"] = {"ads_city_subfield_resource_yearly": 27720, "ads_institution_subfield_resource_yearly": 985555}
facts["jiuxin_semantics_note"] = ("通用时序容器的演示数据源在库：ads_city_subfield_resource_yearly 27,720 行（city×subfield×year "
                                  "年度网格，paper_count/talent_count/funding 序列结构完整）；趋势判读衍生列范式同 "
                                  "hotspot_yearly（trend_status）——但均为科研资源/技术热点语义，非软科学成果三序列口径")

# ============ ⑤ 需求溯源 ============
facts["named_in_srs"] = False
facts["named_note"] = "「时间趋势分析」作为指标名三份说明书未出现；软科学成果展示 SRS 有「趋势分析」功能分句（成果数量/转化效率按时间分布观察——功能行为描述非指标定义）；派单清单 §1 定名「指标时间趋势分析（通用）」"

# ============ ⑥ 权威口径 ============
facts["authoritative_reference"] = ("通用指标时序分析口径：OECD Main Science and Technology Indicators——指标×年份矩阵，"
                                    "缺失年显式标注；趋势判读按 Hyndman & Athanasopoulos《Forecasting: Principles and "
                                    "Practice》趋势成分（斜率/移动平均），方向判读（上涨/下降/平稳）需注明窗口；"
                                    "mock 三序列对应指标=数量（计数）/效率（均值）/占比（同基相除）三类典型")

# ============ ⑦ absence_probe ============
absence = [
    {"probe": "dev 软科学成果序列上游（成果主档/转化过程/区域关联）",
     "source": "dev", "sql": "INCUB_022 结论复核 + trend 词族扫描",
     "hits": 0,
     "hit_detail": "课题成果主档无表（INCUB_022 已证）；转化周期无过程表；成果×区域关联面无表；trend 词族仅 enterprise_growth_trend 0 行——三序列上游全缺"},
    {"probe": "gkx 序列源（trend 词族+软科学语义核，280 表）",
     "source": "gkx", "sql": "SHOW TABLES FROM gkx 词族过滤",
     "hits": 0, "hit_detail": "trend 0 命中；dwd_patent 等可作年序列源但课题成果/转化周期语义不承载"},
    {"probe": "久新年度序列面（resource_yearly 词族+列实读，live 218 表）",
     "source": "jiuxin", "sql": "city/institution resource_yearly 行数+列实读",
     "hits": 2,
     "hit_detail": "city_subfield_resource_yearly 27,720 行/institution 985,555 行——年度网格序列结构完整（可作通用容器演示源）；但度量=paper/talent/funding 科研资源语义，非软科学成果三序列"},
    {"probe": "UI 序列数据接口",
     "source": "doc", "sql": "SoftScienceWorkbench resolvedTrendSeries 链路实读",
     "hits": 1,
     "hit_detail": "series 直取 workbench.trendSeries（softScienceHomepageMock.js:339-378 手写 3 序列×12 点）；SoftScienceTrendAnalysis 无任何数据接口（纯几何渲染）"},
]

# ============ ⑧ derived ============
derived = [
    {"key": "generic_metric_trend_analysis", "value": None, "numerator": None, "denominator": None,
     "note": "『指标时间趋势分析（通用）』=多指标×时间粒度序列+趋势判读的通用容器。容器逻辑（归一化几何+方向标注）前端已备；"
               "但软科学三序列（成果数量/转化周期/区域贡献）上游主档三源全缺——容器无真实序列可载 → 判完全不支持，按 B10 留空即负结论登记"},
]

notes = [
    "判档：通用容器的实际序列数据（软科学三序列）三源均无法构建 → 完全不支持",
    "权威口径（R2 OECD/R3 FPP3）：指标×年份矩阵+缺失年显式标注；趋势判读需注明窗口与方法（斜率/移动平均）",
    "mock 披露：3 序列（bar 项/line 个月/area %）×12 点全手写；trend/trendLabel 判读为常数非计算值——「通用」仅指容器形态，序列内容特定于软科学",
    "范式可引：久新 city_subfield_resource_yearly（27,720 行年度网格）可作通用时序容器的演示数据源（若平台需非软科学演示）；趋势判读范式同 hotspot_yearly trend_status",
    "同族件关系：INCUB_022（成果主档无表）/INCUB_020（growth_trend 空壳）上游结论共享；INCUB_032/033 是时空演变侧时序件（不同模块，同判完全不支持但证据链独立）",
    "升档路径：成果主档+转化过程表落库 → 三序列可算=完全转换支持；或容器接入久新 resource_yearly 作科研资源趋势演示（换语义需产品裁定）",
]

out = {
    "metric_id": "M_SCIUI_INCUB_034",
    "batch": "S3-07",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/achievement-preview/modules/soft-science/components/SoftScienceWorkbench.jsx:22",
        "repos/demo-ui-science/src/pages/achievement-preview/modules/soft-science/components/SoftScienceWorkbench.jsx:941",
        "repos/demo-ui-science/src/pages/achievement-preview/modules/soft-science/mock/softScienceHomepageMock.js:339",
        "repos/demo-ui-science/src/pages/achievement-preview/modules/soft-science/design-system/__tests__/SoftDesignSystem.test.jsx:129",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "软科学 SRS 有「趋势分析」功能分句（成果数量/转化效率按时间分布观察）；「指标时间趋势分析」作为指标名未出现；派单清单 §1 定名（通用）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": "完全不支持",
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["2025.05-2026.04（mock 十二月演示网格；三源无软科学成果序列，任何期间均无真实数据）"],
    "base_years_note": "通用时序件无固定基期（随所载指标而定）；三序列上游主档全缺即无任何期间数据；mock 月粒度为演示标注；非「缺年按 0 摊入」",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": ["1880", "1934", "1986", "2415", "2458", "2486", "8.8", "8.6", "8.5", "7.6", "7.5", "7.4", "59.4", "60.8", "61.6", "67.4", "67.9", "68.2", "12", "3", "542", "280", "218", "27720", "985555", "0"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", OUT)
print("support_judgment:", out["support_judgment"])
