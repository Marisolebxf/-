#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_025 应用使用热度值 · 三源探针脚本（S3-04 L6）。

含义：科技数据资源·总体视窗·资源应用状态·累计调用与趋势分析（seq 346）的「应用热度」研判读数
——按资源类型的累计调用分档标Tag（高热/中热/升温/低热 × 成熟期/成长期/导入期/衰退期）。
UI：repos/demo-ui-science/src/pages/data-resources/components/CumulativeCallTrendAnalysis.jsx:107-118
（typeColumns 的「应用热度」列，render Tag color=HEAT_COLOR[t]；mock 源 mockData.js:888-893
byResourceType[].heat：结构化 44.0% 高热 / 非结构化 31.3% 高热 / 半结构化 19.7% 中热 / 实时流 4.9% 升温；
:164-168 整卡 heatLevel '高热' + lifecycleHint）。

判档路径（口径=「按资源类型的累计调用热度分档 Tag」）：
- 直接承载：需资源调用台账（资源类型×累计调用量）——三源词族 0 命中
  （dev 5 张命中表全 0 行且语义为产业链热点/企业排名/政策排名，语义排除）；
- gkx 280 表调用词族 0 命中；久新 ads_* 热度词族命中全是科研问题/技术热点热度（语义排除）；
- 判完全不支持（指标及关键依赖三源均无法构建——无资源调用台账）。
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_025_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_probe_s304_l6_heat_out.json")

facts, derived, notes, absence = {}, [], [], []
probe = json.load(open(SNAP, encoding="utf-8"))["probes"]

# ============ ① dev：调用/热度词族命中 + 行数复核（语义排除证据） ============
facts["dev_call_rank_heat_tables"] = probe["dev_call_rank_heat_tables"]
facts["dev_call_rank_heat_table_rows"] = probe["dev_call_rank_heat_table_rows"]
facts["dev_table_total"] = probe["dev_table_total"]

# ============ ② gkx：词族复核（0 命中） ============
facts["gkx_call_rank_heat_tables"] = probe["gkx_call_rank_heat_tables"]

# ============ ③ 久新：词族 live 复核 + 语义排除 ============
facts["jiuxin_probe_mode"] = probe["jiuxin_probe_mode"]
facts["jiuxin_table_count_live"] = probe["jiuxin_table_count_live"]
facts["jiuxin_call_rank_heat_tables"] = probe["jiuxin_call_rank_heat_tables"]

# 语义排除专段数据（久新热度词族命中的语义归属）
facts["jiuxin_heat_hits_semantic_note"] = (
    "命中 14 张全部为科研问题/技术热点/新兴主题热度面：ads_research_problem_heat_component"
    "（科研问题热度分量）、ads_technology_hotspot_*（技术热点信号/快照/年度）、"
    "ads_emerging_topic_snapshot（新兴主题快照）等——度量对象是『科研问题/技术主题的文献热度』，"
    "非『数据资源被调用热度』，语义排除")

# ================= 派生（负结论登记，B10） =================
derived.append({
    "key": "resource_heat_level_by_type",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『按资源类型的应用使用热度分档』需资源调用台账（资源类型×累计调用量）——三源词族"
            "0 命中（dev 5 张命中表全 0 行且语义为产业链/企业/政策面，排除；gkx 0 命中；久新 14 张"
            "命中全为科研问题/技术热点热度，语义排除）→ 不可构建，按 B10 留空即负结论登记",
})

# ================= absence_probe =================
absence += [
    {"probe": "dev 资源调用台账面（call/invoke/usage/heat/hot/trend/ranking/visit/click/download/api_log 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表）+ 命中表 COUNT 复核",
     "hits": 0,
     "hit_detail": "词族命中 5 张全部语义排除且 0 行：gkxlumenx_ads.chain_hotspot（产业链热点，0 行）/ "
                   "enterprise_ranking（企业排名，0 行）/ industry_chain_graph_snapshot（产业链图快照，0 行）/ "
                   "gkxlumenx_dwd.enterprise_growth_trend（企业成长趋势，0 行）/ policy_support_rank"
                   "（政策支持排名，0 行）——无一为资源调用台账；dev 词族独立复跑与 L5 族探针一致",
     },
    {"probe": "gkx 调用/热度词族（call/invoke/usage/rank/heat/hot/trend/leaderboard/popular/visit/click/download）",
     "source": "gkx",
     "sql": "information_schema.tables 扫 gkx（280 表，经 _gkxdb.py）",
     "hits": 0,
     "hit_detail": "命中 []——gkx 为要素明细库（论文/专利/机构/学者），无任何调用监控/热度面",
     },
    {"probe": "久新调用/热度词族（同词族 live 复核）",
     "source": "jiuxin",
     "sql": "SHOW TABLES（活库 212 表）词族扫 + 语义核对",
     "hits": 0,
     "hit_detail": "词族命中 14 张全部语义排除：ads_research_problem_heat_component / "
                   "ads_technology_hotspot_{signal,snapshot,yearly} / ads_emerging_topic_snapshot 等"
                   "——度量对象是科研问题/技术主题热度（文献计量面），非数据资源调用热度；"
                   "探测模式 live（当日直连实测）",
     },
    {"probe": "需求原文「热度」定义段",
     "source": "doc",
     "sql": "rg 热度|生命周期 三份需求真源",
     "hits": 1,
     "hit_detail": "SRS 总体视窗.md seq 346（excel_row 349）『自动归集各类数据资源自上线以来的累计调用量，"
                   "并按时间区段进行趋势分析，帮助用户判断资源应用热度和生命周期，优化资源运维策略』"
                   "——『热度』为研判目标词，分档阈值（高热/中热/升温/低热）与算式无定义；"
                   "UI byResourceType[].heat 四档 Tag 为 mock 演示值（mockData.js:888-893），不作数据证据",
     },
]

support = "完全不支持"

notes += [
    "判档：应用使用热度值=按资源类型的累计调用热度分档——前置依赖是资源调用台账"
    "（资源类型×累计调用量×时间），三源词族逐一 0 命中（dev 5 张命中全 0 行且语义排除、"
    "gkx 0 命中、久新 14 张命中全为科研问题/技术热度语义排除）→ 指标及关键依赖三源均无法构建 → 完全不支持",
    "mock 披露：CumulativeCallTrendAnalysis.jsx:107-118「应用热度」列消费 mockData.js:888-893 "
    "byResourceType[].heat（结构化 44.0% 高热/非结构化 31.3% 高热/半结构化 19.7% 中热/实时流 4.9% 升温）"
    "——演示值，不作数据证据（B10）",
    "需求侧证据：SRS seq 346 功能句把『热度』列为趋势分析研判目标（判断资源应用热度和生命周期）——"
    "工程前提（累计调用量归集）三源未建（缺口归属『表不存在』，修复动作是 API 网关日志/调用台账接入）",
    "权威口径参照（R1 国家数据局调查报告）：政务数据共享枢纽调用次数 5,500 亿次按枢纽级汇总——"
    "调用量是官方数据资源统计的核心动作量纲，但其前提是调用日志采集",
    "B11 对账：dev 542/gkx 280/久新 212（live）表数与本件 L6 族探针一致；词族扫描与 L5 族探针同法同结论",
    "升档触发器（B10）：①API 网关/调用台账接入（资源类型×调用量×时间）→ 升完全直接支持"
    "（与 020/021/022/032/034/035 族级共用）；②乙方自建分档阈值口径并采买第三方调用监测 → "
    "升完全转换支持（阈值须甲方裁定）",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_025",
    "batch": "S3-04",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/components/CumulativeCallTrendAnalysis.jsx:107",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:888",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现「应用使用热度值」指标名；语义锚 SRS 总体视窗 seq 346"
                "『判断资源应用热度和生命周期』（研判目标词在、算式与分档阈值无）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "热度分档类读数，不涉基期年",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["346", "542", "280", "212", "14", "5", "0"][:8]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
