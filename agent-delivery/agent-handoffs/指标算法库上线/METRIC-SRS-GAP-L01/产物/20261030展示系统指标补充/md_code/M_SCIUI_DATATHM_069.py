#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_069 存在质量问题的资源数 · 三源探针脚本（S3-05 L2 质量组末件）。

含义：接入视窗两处问题资源计数读数：
- AccessWindow KPI 卡「问题资源数」23 个（accessKPIs[1]，mockData.js:1663）
- 问题资源清单 problemResources 8 行（pr-001..008，:821-830——存在质量问题的资源明细）
- 问题资源统计报表 problemResourceStats（:1674-1714：byType 6 类/byLevel 3 级/byChannel 5 渠道/
  monthlyTrend 5 月——问题资源的稽核流水形态）
挂载：AccessWindow.jsx:355-359（KPI 卡）/​:171-193（问题资源表格列）/​:514-620（P1-11 问题资源增强
——统计报表 Tab + 列表 Tab）。需规锚：mock 注释自标「需规 seq 367」/「seq 343」。

判档路径（口径=「稽核判定存在质量问题的资源去重计数」——稽核违例流水的聚合读数）：
- 与 058 同根但更进一层：不仅缺评分面，连「问题/违例登记台账」都三源零承载
  （problem/issue/alarm/error 词族——dev/gkx/久新 0 命中，L7 族探针）；
- dev quality 词族唯一命中 cfg.degrade_switch（语义排除）；久新 value 唯一命中商业化仿真面（语义排除）；
- mock 的 23（KPI）与 8（清单）与 23（5 月合计？18+22+25+20+23=108——KPI 23 恰为 5 月 total，
  但清单只有 8 行）三套数字互不对账——演示值非稽核产出；
- 判完全不支持（违例台账零承载 → 问题资源计数无从去重统计）。

B11 锚：三源表数 542/280/210（快照）+212（live）；词族 = _probe_s304_l7_quality_out.json。
"""
import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_069_out.json")
SNAP7 = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s304_l7_quality_out.json")
MOCK = "/Users/samuel_tang/my_project/gkx-lumen/repos/demo-ui-science/src/pages/data-resources/mockData.js"

snap = json.load(open(SNAP7, encoding="utf-8"))
probe = json.load(open(PROBE, encoding="utf-8"))
mock_src = open(MOCK, encoding="utf-8").read()
mock_lines = mock_src.split("\n")

# accessKPIs 问题资源数（mockData.js:1663）
kpi_block = re.search(r"export const accessKPIs = \[(.*?)\];", mock_src, re.S).group(1)
m = re.search(r"label: '问题资源数', value: '(\d+)'", kpi_block)
kpi_problem_count = int(m.group(1))  # 23

# problemResources 明细（:821-830 逐行解析）
pr_block = re.search(r"export const problemResources = \[(.*?)\n\];", mock_src, re.S).group(1)
pr_rows = re.findall(r"id: '(pr-\d+)'", pr_block)
pr_count = len(pr_rows)  # 8

# problemResourceStats（:1674-1714）
stats_block = re.search(r"export const problemResourceStats = \{(.*?)\n\};", mock_src, re.S).group(1)
by_type = re.findall(r"type: '(.*?)', count: (\d+)", stats_block)
by_level = re.findall(r"level: '(.*?)', count: (\d+)", stats_block)
trend = re.findall(r"month: '(\d+月)', total: (\d+), resolved: (\d+)", stats_block)
trend_total = sum(int(t) for _, t, _ in trend)          # 18+22+25+20+23 = 108
trend_resolved = sum(int(r) for _, _, r in trend)       # 15+18+20+17+16 = 86
type_sum = sum(int(c) for _, c in by_type)              # 6+5+4+3+3+2 = 23
level_sum = sum(int(c) for _, c in by_level)            # 3+8+12 = 23

facts = {
    "dev_table_count": sum(snap["dev"]["schema_table_counts"].values()),
    "gkx_table_count": snap["gkx"]["table_count"],
    "jiuxin_table_count_snapshot_20261101": len(snap["jiuxin"]["tables"]),
    "jiuxin_table_count_live_20261102": probe["jiuxin_table_count_live"],
    "dev_reliability_like_tables": probe["dev_reliability_like_tables"],  # []
    "dev_value_like_tables": probe["dev_value_like_tables"],  # [cfg.degrade_switch]
    "gkx_reliability_like_tables": probe["gkx_reliability_like_tables"],  # []
    "gkx_value_like_tables": probe["gkx_value_like_tables"],  # []
    "jiuxin_value_like_tables": probe["jiuxin_value_like_tables"],  # [商业化仿真面]
    "dev_degrade_switch_semantic": "gkxlumenx_cfg.degrade_switch 运维降级开关配置表，无问题资源字段——语义排除",
    "jiuxin_value_table_semantic": "ads_technology_commercial_value_simulation 商业化价值仿真面，语义≠质量稽核——语义排除",
    # UI 挂载证据
    "ui_mount_kpi_card": "AccessWindow.jsx:355-359 KPI 卡（accessKPIs.map → KPICard；问题资源数 23 个 trend fall -18.3%）",
    "ui_mount_problem_columns": "AccessWindow.jsx:171-193 问题资源表格列（名称/类型/渠道/级别/状态/发现时间）",
    "ui_mount_p1_11_tabs": "AccessWindow.jsx:514-620 P1-11 问题资源增强——统计报表 Tab（byType/byChannel/monthlyTrend 导出）+ 列表 Tab（problemResources 明细）",
    "ui_mount_trend_chart": "AccessWindow.jsx:162-166 月度趋势双线（问题总数/已解决——monthlyTrend）",
    # mock 演示值（实算，结构证据，不作源）
    "ui_mock_kpi_problem_count": kpi_problem_count,  # 23
    "ui_mock_problem_list_count": pr_count,  # 8
    "ui_mock_by_type": {t: int(c) for t, c in sorted(by_type)},
    "ui_mock_by_level": {l: int(c) for l, c in sorted(by_level)},
    "ui_mock_trend_months": [m for m, _, _ in trend],
    "ui_mock_trend_total_sum": trend_total,      # 108
    "ui_mock_trend_resolved_sum": trend_resolved,  # 86
    "ui_mock_type_sum": type_sum,   # 23
    "ui_mock_level_sum": level_sum,  # 23
    # 三套演示数字互不对账披露
    "ui_mock_inconsistency_notes": [
        "KPI 卡 23 = byType 合计 23 = byLevel 合计 23（三处对上）——但问题清单只有 8 行明细",
        "monthlyTrend 5 个月 total 合计 108（若为累计口径应≈当前未解决量级，若为当月新增则 KPI 23 恰为 5 月值）",
        "月度口径未定义：23 是「当月新增」还是「当前存量未解决」——KPI 卡与趋势线共用 23 但语义不自洽",
        "结论：mock 三套数字（KPI/清单/统计报表）仅部分对账，稽核流水不存在——均不作计数原料（B10）",
    ],
}

derived = [{
    "key": "problem_resource_count",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『存在质量问题的资源数』= 稽核违例台账的资源去重计数（COUNT(DISTINCT resource_id) WHERE 违例未解决）"
            "——违例登记台账三源零承载（problem/issue/alarm/error 词族 0 命中）。mock 三套数字互不对账"
            "（KPI 23/清单 8/趋势合计 108），不作计数原料。按 B10 留空即负结论登记",
}]

absence_probe = [
    {"probe": "dev 问题/违例登记台账（problem/issue/alarm/error/quality 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表，L7 族探针 2026-11-02）",
     "hits": 0,
     "hit_detail": "quality/reliability/value 词族唯一命中 cfg.degrade_switch（运维开关，语义排除）；"
                   "problem/issue/alarm/error 词族 0 命中——dev 无违例登记台账，无问题资源计数面"},
    {"probe": "gkx 问题/违例登记台账（同词族）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）词族扫（经 _gkxdb.py）",
     "hits": 0,
     "hit_detail": "命中 []——要素明细库无稽核违例面"},
    {"probe": "久新问题/违例登记台账（同词族）",
     "source": "jiuxin",
     "sql": "SHOW TABLES（2026-11-02 live，212 表）词族扫",
     "hits": 0,
     "hit_detail": "quality/reliability 0 命中；value 唯一命中商业化仿真面（语义排除）——ads_* 无问题资源登记表"},
    {"probe": "需求原文问题资源数定义段",
     "source": "doc",
     "sql": "rg 问题资源|问题数|质量问题的资源 三份需求真源",
     "hits": 2,
     "hit_detail": "SRS 接入视窗 seq 367「问题资源自动识别与可视化统计」（识别+统计双能力——台账前提）；"
                   "seq 343「异常告警」（告警流水前提）；两处均为能力描述，未给计数口径（存量 vs 当月新增/去重否）"},
]

notes = [
    "判档：问题资源数是稽核违例台账的聚合读数——违例登记台账（资源×问题×状态×时间）三源零承载"
    "→ COUNT(DISTINCT) 无从执行 → 完全不支持；比 058 更进一层：不仅评分面缺，连违例台账都缺"
    "（问题资源是质量稽核的最小产出物——评分可以缓建，台账不能没有）",
    "UI 语义核：问题资源是 P1-11 增强的整套能力族——KPI 计数（:355-359）+ 统计报表（byType/byLevel/"
    "byChannel/monthlyTrend，:514-566 导出）+ 自动识别列表（problemResources 8 行，:613-620）+ "
    "月度趋势双线（问题总数/已解决，:162-166）——需规锚 seq 367（识别与统计）+ seq 343（异常告警）",
    "月度口径陷阱（B9）：KPI 23 与 monthlyTrend 5 月 total 恰同值——但 trend 5 个月合计 108，"
    "若 23 是当月新增则与 trend[5月].total=23 对上；若 23 是存量未解决则应远小于累计——mock 自身未定义口径",
    "mock 披露：三套数字互不对账——KPI 23 = byType 合计 23 = byLevel 合计 23（对上），但清单仅 8 行明细、"
    "趋势合计 108——稽核流水不存在，均不作计数原料（B10）",
    "B11 对账：三源表数 542/280/210+212；词族与 _probe_s304_l7_quality_out.json 逐键一致（与 058/059/060/061 共享同一探针）",
    "升档触发器（B10）：①质量稽核违例台账立项（识别规则+登记+状态流转）→ COUNT(DISTINCT resource_id) 直查"
    "→ 升完全直接支持；②乙方自建核查脚本+问题登记 → 升完全转换支持（口径须登记：存量/当月/去重）；"
    "③维持现状 → 完全不支持（UI KPI 卡与列表建议「暂无数据」）",
    "权威口径参照（R3 GB/T 39912-2021）：汇交质量审核不通过项登记台账——问题登记的制度形态；"
    "（R1 GB/T 36344-2018）：六维校验的违例即问题——问题类型枚举的维度源（mock byType 六类与之同构）",
]

support = "完全不支持"

out = {
    "metric_id": "M_SCIUI_DATATHM_069",
    "batch": "S3-05",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/AccessWindow.jsx:355",
        "repos/demo-ui-science/src/pages/data-resources/AccessWindow.jsx:171",
        "repos/demo-ui-science/src/pages/data-resources/AccessWindow.jsx:514",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:1663",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "SRS 接入视窗 seq 367「问题资源自动识别与可视化统计」+ seq 343「异常告警」——能力描述在，"
                "计数口径（存量/当月/去重）无定义；「问题资源数」KPI 字面仅见 UI",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["问题资源月度序列整体缺承载（monthlyTrend 语义的稽核流水不存在）"],
    "base_years_note": "月度趋势（问题总数/已解决）为稽核流水的期次聚合，台账缺位则序列无从产出",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["542", "280", "210", "212", "23", "8", "108", "86", "18", "22", "25", "20", "355", "171", "514", "1663"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
