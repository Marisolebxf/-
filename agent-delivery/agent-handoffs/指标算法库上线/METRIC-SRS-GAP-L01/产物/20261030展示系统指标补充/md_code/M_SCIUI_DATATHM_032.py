#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_032 季度区段调用量 · 三源探针脚本（S3-04 L6）。

含义：科技数据资源·总体视窗·累计调用与趋势分析（seq 346）的「按季度」时间区段序列
——按季度聚合的区段调用量柱状 + 上线以来累计折线（双轴）。
UI：repos/demo-ui-science/src/pages/data-resources/components/CumulativeCallTrendAnalysis.jsx:26-77
（getTrendOption：series[0] '区段调用量' bar + series[1] '上线以来累计' line yAxisIndex 1；
periodKey='quarter' :9 PERIOD_OPTIONS；mock 源 mockData.js:882-886 periods.quarter：
2025Q2-2026Q2 五点 calls [920000,1280000,1680000,2280000,2856000] cumulative 同值）。

判档路径（口径=「按季度区段聚合的资源调用量序列」）：
- 直接承载：需资源调用台账（调用×时间戳，季度可聚合）——三源词族 0 命中
  （dev 5 张命中表全 0 行且语义排除）；
- 时间细分最近邻：dev enterprise_base.update_time 月维仅 2 点（2026-08/09，批次式灌库，
  DATAIN_001/002 族已证）——但它是底册表更新时间，与「资源调用」无语义关联，不作代理；
- 判完全不支持（指标及关键依赖三源均无法构建）。
"""
import json
import os
import sys

import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_032_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_probe_s304_l6_heat_out.json")
L4SNAP = os.path.join(BASE, "_snapshots", "_probe_s304_l4_collect_out.json")

facts, derived, notes, absence = {}, [], [], []
probe = json.load(open(SNAP, encoding="utf-8"))["probes"]

# ============ ① dev：调用词族命中复核 + 季度聚合轴探针 ============
facts["dev_call_rank_heat_tables"] = probe["dev_call_rank_heat_tables"]
facts["dev_call_rank_heat_table_rows"] = probe["dev_call_rank_heat_table_rows"]
facts["dev_table_total"] = probe["dev_table_total"]

# 库内唯一时间序列最近邻：enterprise_base.update_time 月维（L4 族已证，本件复跑口径核对）
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
d = pymysql.connect(**DEV)
c = d.cursor()
c.execute(
    "SELECT DATE_FORMAT(update_time, '%Y-%m') m, COUNT(*) FROM gkxlumenx_dwd.enterprise_base "
    "GROUP BY m ORDER BY m")
facts["dev_enterprise_update_month_dist"] = [[str(a), int(b)] for a, b in c.fetchall()]
d.close()

# ============ ② gkx / 久新：词族复核 ============
facts["gkx_call_rank_heat_tables"] = probe["gkx_call_rank_heat_tables"]
facts["jiuxin_probe_mode"] = probe["jiuxin_probe_mode"]
facts["jiuxin_table_count_live"] = probe["jiuxin_table_count_live"]
facts["jiuxin_call_rank_heat_tables"] = probe["jiuxin_call_rank_heat_tables"]

# ================= 派生（负结论登记，B10） =================
n_months = len(facts["dev_enterprise_update_month_dist"])
derived.append({
    "key": "quarterly_call_volume_series",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『按季度区段聚合的资源调用量序列』需资源调用台账（调用×时间戳）——三源词族"
            "0 命中（dev 5 张命中全 0 行语义排除；gkx 0 命中；久新 14 张命中全为科研问题/"
            "技术热度语义排除）→ 不可构建；库内唯一时间序列面 enterprise_base.update_time "
            f"月维仅 {n_months} 点（批次式灌库）且语义为底册更新非调用，不作代理，按 B10 留空",
})

# ================= absence_probe =================
absence += [
    {"probe": "dev 资源调用台账面（call/invoke/usage/heat/hot/trend/ranking/visit/click/download/api_log 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表）+ 命中表 COUNT 复核",
     "hits": 0,
     "hit_detail": "词族命中 5 张全部语义排除且 0 行（chain_hotspot/enterprise_ranking/"
                   "industry_chain_graph_snapshot/enterprise_growth_trend/policy_support_rank）"
                   "——无一含调用×时间戳明细，季度聚合无从做起",
     },
    {"probe": "gkx 调用词族（call/invoke/usage/rank/heat/hot/trend/visit/click/download）",
     "source": "gkx",
     "sql": "information_schema.tables 扫 gkx（280 表，经 _gkxdb.py）",
     "hits": 0,
     "hit_detail": "命中 []——gkx 为要素明细库，无任何调用监控面；要素表时间列（专利 apdt_year/"
                   "论文 cover_year_start）是内容年份非调用时间，语义排除",
     },
    {"probe": "久新调用词族（同词族 live 复核）",
     "source": "jiuxin",
     "sql": "SHOW TABLES（活库 212 表）词族扫 + 语义核对",
     "hits": 0,
     "hit_detail": "命中 14 张全部语义排除（科研问题/技术热点/新兴主题热度与快照面）——"
                   "快照管理形态 metrics_as_of_date 单日一期（DATAIN_003 已证），无逐期调用记录；"
                   "探测模式 live",
     },
    {"probe": "需求原文「按时间区段」定义段",
     "source": "doc",
     "sql": "rg 时间区段|季度 三份需求真源",
     "hits": 1,
     "hit_detail": "SRS 总体视窗.md seq 346『自动归集各类数据资源自上线以来的累计调用量，"
                   "并按时间区段进行趋势分析』——『时间区段』粒度（周/月/季）无定义；"
                   "UI PERIOD_OPTIONS 三档（近一周/近半年月/按季度）为前端演示约定"
                   "（mockData.js:882-886 quarter 五点演示值），不作数据证据",
     },
]

support = "完全不支持"

notes += [
    "判档：季度区段调用量=按季度聚合的资源调用序列——前置依赖是资源调用台账（调用×时间戳），"
    "三源词族逐一 0 命中 → 指标及关键依赖三源均无法构建 → 完全不支持",
    "时间序列最近邻披露：dev enterprise_base.update_time 月维仅 "
    f"{facts['dev_enterprise_update_month_dist']}（{n_months} 点，批次式灌库，与 DATAIN_001/002 族"
    "同法同读数）——语义是企业底册更新时间非资源调用，且月维两点不足以构成季度序列，不作代理（B10）",
    "mock 披露：CumulativeCallTrendAnalysis.jsx:26-77 双轴图（区段 bar+累计 line）消费 "
    "mockData.js:882-886 periods.quarter（2025Q2-2026Q2 五点 92 万→285.6 万）——演示值，不作数据证据",
    "需求侧证据：seq 346 功能句把『按时间区段进行趋势分析』列为功能要求——工程前提"
    "（累计调用量归集+时间戳）三源未建（缺口归属『表不存在』，修复动作是调用台账接入）",
    "权威口径参照（R2 深圳开放平台）：接口调用量按近七日/累计双窗口公示——区段聚合的官方实践形态，"
    "前提同样是调用日志",
    "B11 对账：词族扫描与 L5/L6 族探针一致；enterprise_base 月维与 DATAIN_001/002/DATATHM_015 族"
    "同读数零漂移",
    "升档触发器（B10）：①API 网关/调用台账接入（调用×时间戳）→ 升完全直接支持"
    "（周/月/季三粒度一次到位，族级共用）；②维持现状 → 完全不支持（UI 该图建议『暂无数据』）",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_032",
    "batch": "S3-04",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/components/CumulativeCallTrendAnalysis.jsx:26",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:882",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现「季度区段调用量」指标名；语义锚 SRS 总体视窗 seq 346"
                "『按时间区段进行趋势分析』（功能在、区段粒度与聚合口径无）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "区段序列类读数，库内无调用时间轴，不涉基期年",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["346", "542", "280", "212", "920000", "2856000"][:8]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
