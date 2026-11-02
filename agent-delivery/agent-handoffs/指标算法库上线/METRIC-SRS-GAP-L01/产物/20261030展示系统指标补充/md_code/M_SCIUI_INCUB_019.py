#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INCUB_019 仪器平均使用率（全市均值，机时利用率）· 三源探针脚本（S3-07 L3）。

含义：大型科学仪器共享页 KPI「平均使用率」与机构表「平均使用率」列——仪器机时
利用率的全市均值（%）。UI：InstrumentSharingPage.jsx:177（KPI averageUsage 均值）/
:1018（机构聚合表 averageUsage 列）。mock 源 instrumentSharingMock.js
instruments[].usageRate（76/88/64/52…）+ 机构聚合 averageUsage=ΣusageRate/台数。

判档路径（口径 = 年有效工作机时 ÷ 年额定机时，权威见科技部 50 万+ 仪器开放共享
评价考核细则与利用与共享指数报告）：
- 计算前提是「仪器主档（单台）+ 机时流水（有效机时/对外服务机时）」两层——三源：
  dev：instrument/equipment 词族 542 表 0 命中（唯一仪器承载是 mock 层）；
  gkx：280 表 instrument 词族 0 命中（含列级 carrier/instrument 列探 0）；
  久新：218 表 live 复核 instrument 0 命中（ads_* 为论文/专利/人才/技术分析面）；
- 深圳对接语义：SRS 大型科学仪器共享.md 序号 524「对接深圳市大型科学仪器共享平台」
  ——外部平台有数（2020 末入网 9262 台/共享率 60.59%，主需求 :3565），但三源库内
  无镜像表；
- 判完全不支持（机时流水与仪器主档三源均无法构建；外部平台对接未落库）。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_INCUB_019_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s307_l3_incub_out.json")

facts, derived, notes, absence = {}, [], [], []
probe = json.load(open(PROBE, encoding="utf-8"))

# ============ ① mock 层（UI 语义披露，不作数据证据） ============
MOCK_USAGE_RATES = [76, 88, 64, 52]  # instrumentSharingMock.js:242/263/284/305
facts["ui_mount"] = ("InstrumentSharingPage.jsx:177（KPI「平均使用率」usageRate 均值，buildKpis L172）/ "
                     ":1018（机构聚合表「平均使用率」averageUsage 列，buildAgencyTable L555 ΣusageRate/台数）")
facts["ui_mock_usage_rates"] = MOCK_USAGE_RATES
facts["ui_mock_kpi_note"] = "mock instruments[].usageRate 4 值 76/88/64/52（另有机构聚合 averageUsage=round(ΣusageRate/instrumentCount)）——演示值，不参与支持度结论"
facts["ui_mock_agency_formula"] = "averageUsage = Math.round(item.usageTotal / item.instrumentCount)，usageTotal=Σ instrument.usageRate（InstrumentSharingPage.jsx:538/555 实读）"
facts["ui_heat_tiers"] = "usageRate≥80 高热 / ≥60 中热（:224-228 分级着色），排序键 usageRate 降序（:214）"

# ============ ② dev ============
dev = probe["dev"]
facts["dev_table_total"] = dev["table_total"]
facts["dev_instrument_word_tables"] = dev["word_instrument"]
facts["dev_instrument_hits_note"] = "instrument/equipment/apparatus/facility/machine 词族 542 表 0 命中——dev 无仪器主档/机时流水任何承载"

# ============ ③ gkx ============
facts["gkx_table_count"] = probe["gkx"]["table_count"]
facts["gkx_instrument_word_tables"] = probe["gkx"]["word_hits"]["instrument"]
facts["gkx_carrier_instrument_columns"] = probe["gkx"].get("carrier_instrument_columns", [])

# ============ ④ 久新 ============
jx = probe["jiuxin"]
facts["jiuxin_table_count_live"] = jx["table_count_live"]
facts["jiuxin_instrument_word_tables"] = jx["word_hits"]["instrument"]
facts["jiuxin_hits_note"] = "instrument/equipment 词族 218 表 live 复核 0 命中——ads_* 全系为论文/专利/人才/技术分析面，无仪器资产面"

# ============ ⑤ 需求溯源与外部平台参照 ============
facts["srs_anchor"] = "SRS 大型科学仪器共享.md 序号 524「对接深圳市大型科学仪器共享平台」（展示区域分布/功能类别/开放共享情况）+ 序号 532 服务类型和共享率统计"
facts["named_in_srs"] = False
facts["named_note"] = "「平均使用率/机时利用率」指标名在三份说明书与主需求均未出现；语义锚为共享平台对接功能分句与「系统自动统计共享率及使用频率」（SRS 序号 527 段）"
facts["external_platform_reference"] = "主需求 :3565：深圳共享平台截至 2020-12 入网仪器 9262 台套/开放共享 5612 台套/共享率 60.59%/注册单位 499 家——外部平台有现成统计，但三源库内无镜像表（对接未落库）"

# ============ ⑥ 权威口径参照（WebSearch 核验） ============
facts["authoritative_formula"] = "机时利用率 = 年有效工作机时 ÷ 年额定机时 × 100%（有效机时含必要开机准备/测试/必需后处理，不含空载；额定机时通用 1400h/专用 800h，指数报告口径 1600h）"
facts["related_authoritative_metrics"] = "对外服务机时率 = 年对外服务机时 ÷ 年额定机时；共享率 = 年对外服务机时 ÷ 年有效工作机时（科技部 2022 细则第五条/2026 修订版）"

# ============ ⑦ absence_probe ============
absence = [
    {"probe": "dev 仪器主档/机时流水面（instrument/equipment/apparatus/facility/machine 词族，542 表）",
     "source": "dev", "sql": "information_schema.tables 扫 gkxlumenx_*（_probe_s307_l3_incub）",
     "hits": 0,
     "hit_detail": "0 命中——dev 无仪器资产台账、无机时记录表；UI 页整页数据来自 instrumentSharingMock.js"},
    {"probe": "gkx 仪器面（instrument 词族表名+列名，280 表）",
     "source": "gkx", "sql": "information_schema.tables + columns 扫 gkx",
     "hits": 0,
     "hit_detail": "表名 0 命中；列名 carrier/instrument 列探 0 命中——gkx 为论文/专利/机构/学者要素库"},
    {"probe": "久新仪器面（instrument/equipment 词族，live 218 表复核）",
     "source": "jiuxin", "sql": "SHOW TABLES 词族过滤",
     "hits": 0,
     "hit_detail": "0 命中——ads_* 全系科技要素分析面（论文/专利/人才/技术/难题），无仪器资产/共享运营面"},
    {"probe": "需求原文「使用率/机时」定义段",
     "source": "doc", "sql": "rg 平均使用率|机时 三份说明书+主需求",
     "hits": 0,
     "hit_detail": "指标名 0 命中；主需求 :3565 深圳平台参照数字（9262 台/共享率 60.59%）为外部平台官网统计非计算口径定义；SRS 序号 527「系统自动统计共享率及使用频率」为功能分句"},
]

# ============ ⑧ derived（负结论留空登记） ============
derived = [
    {"key": "instrument_avg_usage_rate_citywide", "value": None, "numerator": None, "denominator": None,
     "note": "『仪器平均使用率（全市均值）』= mean(单台 年有效工作机时/年额定机时)。需仪器主档+机时流水两层——dev/gkx/久新 instrument 词族三源 0 命中（外部深圳平台有数未落库）→ 不可构建，按 B10 留空即负结论登记"},
    {"key": "instrument_avg_usage_rate_mock_reference", "value": 70.0, "numerator": sum(MOCK_USAGE_RATES), "denominator": len(MOCK_USAGE_RATES),
     "note": "mock 4 台均值 70%（76+88+64+52)/4——仅演示量级参照（B10 披露，不作数据证据）"},
]

notes = [
    "判档：机时利用率两层依赖（仪器主档+机时流水）三源词族 0 命中；深圳共享平台（外部）有现成统计（2020 末 9262 台/共享率 60.59%）但库内无镜像 → 指标及关键依赖三源均无法构建 → 完全不支持",
    "权威口径（R1 科技部办公厅《国家重大科研基础设施和大型科研仪器开放共享评价考核实施细则》2022/2026 修订）：仪器运行机时=年平均有效工作机时、共享率=年平均对外服务机时/年平均运行机时；R2 指数报告：单台利用率=年有效工作机时/年额定工作机时（1600h），区域均值为按原值占比加权平均；R3 高校效益评价：通用 1400h/专用 800h 额定基准",
    "mock 披露：usageRate=[76,88,64,52]，KPI=筛选集均值、机构表 averageUsage=Σ/台数——UI 的「平均」是台均（未加权原值），与指数报告的原值加权口径不同（口径差异披露）",
    "同族件关系：INCUB_007（使用热度值）/INCUB_008（使用率单台）为 L2 批同页件，本件为全市聚合口径；SOFTSCI_010（月度预约趋势）同为该页运营流水——三件共享「三源无仪器运营面」探针结论（本件独立留证）",
    "升档路径：对接深圳共享平台入湖（仪器主档+机时月表落 ods）→ 完全转换支持（均值可算）；平台侧直接出区域统计接口 → 完全直接支持",
]

out = {
    "metric_id": "M_SCIUI_INCUB_019",
    "batch": "S3-07",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:177",
        "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:1018",
        "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/mock/instrumentSharingMock.js:242",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现「平均使用率/机时利用率」指标名；语义锚 SRS 大型科学仪器共享.md 序号 524 深圳平台对接+序号 527「系统自动统计共享率及使用频率」功能分句",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": "完全不支持",
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["无年度基期维（机时利用率为年度统计量，三源无承载无历史序列；mock 亦无年度序列）"],
    "base_years_note": "权威口径为年度统计（年有效机时/年额定机时）；三源无承载无基期可言；非「缺年按 0 摊入」",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": ["76", "88", "64", "52", "70", "1400", "800", "1600", "9262", "5612", "60.59", "499", "542", "280", "218", "0", "524", "527", "532", "3565"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", OUT)
print("support_judgment:", out["support_judgment"])
