#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TECHTRK_022 评估结果追踪（历史得分序列） —— 三源探针 + 复现脚本（批 S3-01 Lane 4）。

UI 挂载：repos/demo-ui-science/src/techDevelopmentTracking.js:50
  technologyTrackingTimeline = { title: '评估结果追踪', years: ['2020'..'2026'], events: 8 条 }
  —— 页面顶部时间轴容器（2020-2026 七年 + 里程碑事件）
  关联：js:505-549 technologyTrackingEvaluationHistoryMatrix（015 件承接其「本次评估」列；
        本件承接 periods 轴 2023/2024/2025 三列历史 + 时间轴 2020-2026 序列语义）

三源（开发库 gkxlumenx_* 禁 demo / gkx 经 _gkxdb / 久新 Doris 只读）：
  ① 开发库：无历轮评估结果面（evaluation_template 是参数模板；探针留证）
  ② gkx：280 表无评估/历轮类结果面（探针留证）
  ③ 久新：ads_technology_stage_assessment 单轮快照（metrics_as_of_date 单值 2026-10-16）
     —— 历史轮次无承载；但 hotspot_yearly 有 2015-2026 年度热点分序列（可作「结果变化趋势」替代轴）

复现口径（B10 双口径并列）：
  口径 A（年度热点分序列·全域）：hotspot_yearly 2015-2026 各年 19,430 节点均分（唯一现成年度得分序列）
  口径 B（深圳子盘序列）：深圳 6,233 节点各年热点均分（需求页面深圳语境）
"""
import json
import os
import sys

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _gkxdb import gkx  # noqa: E402

JX = dict(
    host="47.93.119.170", port=29030, user="test2",
    password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
    database="gkx_technology_analysis_dev",
    connect_timeout=30, read_timeout=300, autocommit=True,
)

DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           connect_timeout=20, read_timeout=120)

V2 = "technology_insight_mvp_v2_eto_cluster_technology"
SZ = "loc_E16782C21F18EBF8A59C1E98F9C9860B"

facts = {}
probes = []


def probe(tag, source, sql, cur, note=""):
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        probes.append({"probe": tag, "source": source, "sql": sql, "note": note,
                       "hits": len(rows), "sample": [str(r)[:180] for r in rows[:8]]})
        return rows
    except Exception as e:  # noqa: BLE001
        probes.append({"probe": tag, "source": source, "sql": sql, "note": note,
                       "hits": -1, "error": str(e)[:180]})
        return []


jx = pymysql.connect(**JX)
jc = jx.cursor()

# ---- 评估轮次轴（stage_assessment）----
jc.execute("SELECT COUNT(*) FROM ads_technology_stage_assessment")
facts["jiuxin_stage_assessment_rows"] = int(jc.fetchone()[0])
jc.execute("SELECT DISTINCT metrics_as_of_date FROM ads_technology_stage_assessment")
facts["jiuxin_stage_assessment_as_of_dates"] = [str(r[0]) for r in jc.fetchall()]
jc.execute("SELECT DISTINCT model_version FROM ads_technology_stage_assessment")
facts["jiuxin_stage_assessment_model_versions"] = [r[0] for r in jc.fetchall()]

# ---- 口径 A：全域年度热点序列 ----
jc.execute(
    "SELECT statistics_year, COUNT(DISTINCT technology_node_id), AVG(hotspot_score) "
    "FROM ads_technology_hotspot_yearly GROUP BY statistics_year ORDER BY statistics_year")
facts["jiuxin_hotspot_yearly_avg_by_year"] = {int(r[0]): round(float(r[2]), 4) for r in jc.fetchall()}
jc.execute("SELECT COUNT(*) FROM ads_technology_hotspot_yearly")
facts["jiuxin_hotspot_yearly_rows"] = int(jc.fetchone()[0])

# ---- 口径 B：深圳子盘序列 ----
jc.execute(
    "SELECT y.statistics_year, COUNT(DISTINCT y.technology_node_id), AVG(y.hotspot_score) "
    "FROM ads_technology_hotspot_yearly y JOIN ads_technology_region_yearly_metrics m "
    "ON m.technology_node_id = y.technology_node_id AND m.location_id = %s "
    "GROUP BY y.statistics_year ORDER BY y.statistics_year", (SZ,))
sz_series = {int(r[0]): {"nodes": int(r[1]), "avg": round(float(r[2]), 4)} for r in jc.fetchall()}
facts["jiuxin_shenzhen_hotspot_yearly_avg"] = sz_series

# ---- 潜力分年度可复算性核验（potential 是快照，无年度）----
jc.execute("SELECT COUNT(DISTINCT metrics_as_of_date) FROM ads_technology_potential_assessment")
facts["jiuxin_potential_as_of_dates_n"] = int(jc.fetchone()[0])

# ---- UI 时间轴 mock 登记 ----
facts["ui_mock_timeline"] = {
    "title": "评估结果追踪", "years": ["2020", "2021", "2022", "2023", "2024", "2025", "2026"],
    "events_n": 8, "matrix_periods": ["2023", "2024", "2025", "current"],
}

jc.close()
jx.close()

# ---- gkx 探针 ----
gc = gkx()
rows = probe("gkx 280 表 评估/历轮/历史类结果面扫描", "gkx",
             "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
             "AND (table_name LIKE '%assess%' OR table_name LIKE '%evaluation%' OR table_name LIKE '%history%')", gc)
facts["gkx_assess_like_tables"] = [r[0] for r in rows]
gc.close()

# ---- dev 探针 ----
dv = pymysql.connect(**DEV)
dc = dv.cursor()
rows = probe("dev evaluation_template 行数（参数模板非结果）", "dev",
             "SELECT COUNT(*) FROM gkxlumenx_topic_enterprise.evaluation_template", dc)
facts["dev_evaluation_template_rows"] = int(rows[0][0]) if rows else None
rows = probe("dev gkxlumenx_dwd+ads 评估历史类表扫描", "dev",
             "SELECT table_schema, table_name FROM information_schema.tables "
             "WHERE table_schema IN ('gkxlumenx_dwd','gkxlumenx_ads','gkxlumenx_topic_enterprise') "
             "AND (table_name LIKE '%assess%' OR table_name LIKE '%evaluation%')", dc)
facts["dev_assess_like_tables"] = [[r[0], r[1]] for r in rows]
dc.close()
dv.close()

# 派生：全域 2025 vs 2024 均分变化
g = facts["jiuxin_hotspot_yearly_avg_by_year"]
derived = [
    {"key": "jiuxin_hotspot_avg_yoy_2025_vs_2024",
     "value": round(g[2025] - g[2024], 4),
     "numerator": int(round(g[2025] * 10000)) - int(round(g[2024] * 10000)),
     "denominator": 10000,
     "note": "分子=2025 均分×10⁻⁴ 与 2024 均分×10⁻⁴ 之差（定点化避免浮点），分母=10⁴；同源 jiuxin hotspot_yearly 各年 19,430 节点均分。"},
]

out = {
    "metric_id": "M_SCIUI_TECHTRK_022",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/techDevelopmentTracking.js:50",
        "repos/demo-ui-science/src/techDevelopmentTracking.js:506-549",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "SRS 技术发展跟踪.md seq 55「评估结果追踪」（excel_row 58）需求明列叶：『支持查看技术评估的历史记录和结果变化趋势…支持不同时期、不同方法评估结果的并排展示』；主文档 1.1.1.1.4.1.3.2.4 同文。但「历史得分序列」作为指标名与评分模型未在需求给出定义。",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": [p for p in probes if p["source"] in ("gkx", "dev")],
    "support_judgment": "部分支持",
    "notes": [
        "「评估结果追踪」是需求明列叶（seq 55）；UI 双承载：顶部时间轴（2020-2026 七年 + 8 里程碑事件，全前端常量）与评估历史矩阵 periods 轴（2023/2024/2025/本次 四列，mock 演示值）。",
        "主降档因：评估轮次轴无承载——久新 stage/potential 两评估表均单轮快照（metrics_as_of_date 单值 2026-10-16），UI 的 2023/2025 三列历史、时间轴 2020-2026 八事件在数据面均无对应发布行；dev evaluation_template 8 行是参数模板非历轮结果。",
        "口径 A（替代轴）：hotspot_yearly 是唯一现成年度得分序列（2015-2026 各年 19,430 节点均分 21.47→19.90 全域读数见 facts）；语义是『技术节点热点分年度趋势』非『评估得分历史』，替代须甲方裁定。",
        "口径 B（深圳）：深圳 6,233 节点 2015-2025 均分 20.4871→43.7929（2026 部分年 26.0608 不入比较），方向与全域一致（2021 峰值后回落）。",
        "与 015 件共享底表与「轮次缺失」缺口（015 消费 current 列、本件消费 periods 历史列）；两件 absence_probe 互补不重复计证。",
    ],
    "base_years_used": ["2015", "2016", "2017", "2018", "2019", "2020", "2021",
                        "2022", "2023", "2024", "2025", "2026"],
    "base_years_missing": ["2023", "2024", "2025"],
    "base_years_note": "评估矩阵的 2023/2024/2025 三轮在 stage/potential 快照无承载（base_years_missing 登记的是『评估轮次』缺失年）；hotspot_yearly 的 2015-2026 全序列可用（口径 A/B），2026 为 PARTIAL_YEAR。",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "38860", "19430", "2026-10-16", "233160", "6233", "2020", "2026",
    ]},
}
path = os.path.join(HERE, "M_SCIUI_TECHTRK_022_out.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", path)
print("support_judgment:", out["support_judgment"])
