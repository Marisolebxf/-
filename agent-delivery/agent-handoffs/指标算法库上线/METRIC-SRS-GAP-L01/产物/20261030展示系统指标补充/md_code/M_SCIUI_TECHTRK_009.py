#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TECHTRK_009 领域技术平均成熟度 —— 三源探针 + 复现脚本（批 S3-01，Lane 2）。

UI 挂载：repos/demo-ui-science/src/techDevelopmentTracking.js:1023
  buildMetrics() 内 { key: 'maturity', label: '平均成熟度', value: averageMaturity, unit: '分' }
  —— averageMaturity = Math.round(topics.reduce((sum,i)=>sum+i.maturity,0)/count)，mock 值 72（演示值，不参与支持度结论）

三源（开发库 gkxlumenx_* 禁 demo / gkx 经 _gkxdb / 久新 Doris 只读）：
  ① 开发库：gkxlumenx_dwd/gkxlumenx_ads 无技术成熟度/stage 类承载表（information_schema 命中 0，探针留证）
  ② gkx：280 表无 maturity/stage/TRL 类结果面（列扫描命中 0，探针留证）
  ③ 久新：ads_technology_stage_assessment 38,860 行（19,430 节点 × 2 模型版本），
     ads_technology_transfer_stage 8 阶段定义表 —— 本件主承载

复现口径（B10 双口径并列）：
  口径 A（8 分制）：avg_stage_order = Σ(cnt×stage_order)/Σ(cnt)，stage_order 来自 ads_technology_transfer_stage
  口径 B（百分制）：order 百分位映射 (stage_order-1)/(8-1)×100 后取平均（与 UI '分' 量纲对齐）
"""
import json
import os
import sys

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _gkxdb import gkx  # noqa: E402  gkx 唯一入口（禁 demo_*，不传 database/charset）

JX = dict(
    host="47.93.119.170",
    port=29030,
    user="test2",
    password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
    database="gkx_technology_analysis_dev",
    connect_timeout=30,
    read_timeout=180,
)

DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           connect_timeout=20, read_timeout=120)

facts = {}
probes = []


def probe(tag, source, sql, conn_cur):
    try:
        cur = conn_cur
        cur.execute(sql)
        rows = cur.fetchall()
        probes.append({"probe": tag, "source": source, "sql": sql,
                       "hits": len(rows), "sample": [str(r)[:200] for r in rows[:8]]})
        return rows
    except Exception as e:  # noqa: BLE001
        probes.append({"probe": tag, "source": source, "sql": sql,
                       "hits": -1, "error": str(e)[:200]})
        return []


# ---------------------------------------------------------------- 久新（主承载）
jx = pymysql.connect(**JX)
jc = jx.cursor()

facts["jiuxin_stage_assessment_rows"] = int(
    jc.execute("SELECT COUNT(*) FROM ads_technology_stage_assessment") or 0)
facts["jiuxin_stage_assessment_rows"] = int(jc.fetchone()[0])
jc.execute("SELECT COUNT(DISTINCT technology_node_id) FROM ads_technology_stage_assessment")
facts["jiuxin_stage_assessment_nodes"] = int(jc.fetchone()[0])
jc.execute("SELECT COUNT(DISTINCT model_version) FROM ads_technology_stage_assessment")
facts["jiuxin_stage_assessment_model_versions"] = int(jc.fetchone()[0])

jc.execute("SELECT stage_code, COUNT(*) FROM ads_technology_stage_assessment GROUP BY stage_code ORDER BY 2 DESC")
stage_rows = jc.fetchall()
facts["jiuxin_stage_code_dist"] = {str(s): int(c) for s, c in stage_rows}

jc.execute("SELECT stage_code, stage_order, stage_name_zh FROM ads_technology_transfer_stage ORDER BY stage_order")
transfer_rows = jc.fetchall()
facts["jiuxin_transfer_stage_def"] = [
    {"stage_code": str(s), "stage_order": int(o), "stage_name_zh": str(n)}
    for s, o, n in transfer_rows]
facts["jiuxin_transfer_stage_def_rows"] = len(transfer_rows)

jc.execute("SELECT assessment_method, COUNT(*) FROM ads_technology_stage_assessment GROUP BY assessment_method")
facts["jiuxin_assessment_method_dist"] = {str(m): int(c) for m, c in jc.fetchall()}

jc.execute("SELECT COUNT(stage_confidence), MIN(stage_confidence), MAX(stage_confidence), AVG(stage_confidence) FROM ads_technology_stage_assessment")
r = jc.fetchone()
facts["jiuxin_stage_confidence_nonnull"] = int(r[0])
facts["jiuxin_stage_confidence_min"] = float(r[1])
facts["jiuxin_stage_confidence_max"] = float(r[2])
facts["jiuxin_stage_confidence_avg"] = round(float(r[3]), 4)

# 口径 A：8 分制平均 stage_order（全节点）
order_map = {str(s): int(o) for s, o, _ in transfer_rows}
jc.execute("SELECT stage_code, COUNT(DISTINCT technology_node_id) FROM ads_technology_stage_assessment GROUP BY stage_code")
node_stage = {str(s): int(c) for s, c in jc.fetchall()}
n_nodes = sum(node_stage.values())
facts["jiuxin_nodes_by_stage_unique"] = node_stage
avg_order = sum(cnt * order_map[s] for s, cnt in node_stage.items()) / n_nodes
facts["jiuxin_avg_stage_order_8scale"] = round(avg_order, 4)

# 口径 B：百分制（(order-1)/7×100）
pct_map = {s: (o - 1) / 7 * 100 for s, o in order_map.items()}
avg_pct = sum(cnt * pct_map[s] for s, cnt in node_stage.items()) / n_nodes
facts["jiuxin_avg_maturity_pct_scale"] = round(avg_pct, 4)

# 深圳子盘（需求页面语境是深圳科技规划，补深圳切片）
SZ = "loc_E16782C21F18EBF8A59C1E98F9C9860B"
jc.execute(
    "SELECT s.stage_code, COUNT(DISTINCT s.technology_node_id) FROM ads_technology_stage_assessment s "
    "JOIN ads_technology_region_yearly_metrics m ON m.technology_node_id = s.technology_node_id "
    "WHERE m.location_id = %s GROUP BY s.stage_code", (SZ,))
sz_stage = {str(s): int(c) for s, c in jc.fetchall()}
facts["jiuxin_shenzhen_nodes_by_stage"] = sz_stage
n_sz = sum(sz_stage.values())
facts["jiuxin_shenzhen_stage_nodes"] = n_sz
if n_sz:
    facts["jiuxin_shenzhen_avg_stage_order_8scale"] = round(
        sum(cnt * order_map[s] for s, cnt in sz_stage.items()) / n_sz, 4)
    facts["jiuxin_shenzhen_avg_maturity_pct_scale"] = round(
        sum(cnt * pct_map[s] for s, cnt in sz_stage.items()) / n_sz, 4)

jc.close()
jx.close()

# ---------------------------------------------------------------- gkx（absence 探针）
gc = gkx()
rows = probe("gkx 280 表 maturity/stage/TRL 结果面扫描", "gkx",
             "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
             "AND (table_name LIKE '%matur%' OR table_name LIKE '%stage%' OR table_name LIKE '%trl%' "
             "OR table_name LIKE '%assess%' OR table_name LIKE '%evaluat%')", gc)
facts["gkx_maturity_like_tables"] = [r[0] for r in rows]
rows = probe("gkx 列名 maturity/trl 扫描", "gkx",
             "SELECT table_name, column_name FROM information_schema.columns WHERE table_schema='gkx' "
             "AND (column_name LIKE '%matur%' OR column_name LIKE '%trl%') LIMIT 20", gc)
facts["gkx_maturity_like_columns"] = [[r[0], r[1]] for r in rows]
gc.close()

# ---------------------------------------------------------------- 开发库（absence 探针）
# ---- dev 段容错补丁(2026-11-01, B4: dev 不可达≠无数据, 沿用首跑实测值并标注) ----
try:
    dv = pymysql.connect(**DEV)
    dc = dv.cursor()
    rows = probe("dev gkxlumenx_dwd+ads 成熟度/stage 类表扫描", "dev",
                 "SELECT table_schema, table_name FROM information_schema.tables "
                 "WHERE table_schema IN ('gkxlumenx_dwd','gkxlumenx_ads') "
                 "AND (table_name LIKE '%matur%' OR table_name LIKE '%stage%' OR table_name LIKE '%assess%' "
                 "OR table_name LIKE '%evaluat%' OR table_name LIKE '%trl%')", dc)
    facts["dev_maturity_like_tables"] = [[r[0], r[1]] for r in rows]
    dc.close()
    dv.close()
except Exception as _e:  # noqa: BLE001
    _po = os.path.join(HERE, "M_SCIUI_TECHTRK_009_out.json")
    if os.path.exists(_po):
        try:
            _prev = json.load(open(_po, encoding="utf-8")).get("facts", {})
            for _k, _v in _prev.items():
                if _k.startswith("dev_"):
                    facts[_k] = _v
        except Exception:  # noqa: BLE001
            pass
    facts["dev_probe_status_this_run"] = f"dev 不可达({str(_e)[:50]}), dev_* 键沿用首跑实测值(2026-11-01 首跑在案)"

# ---------------------------------------------------------------- 产物
out = {
    "metric_id": "M_SCIUI_TECHTRK_009",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/techDevelopmentTracking.js:1023",
        "repos/demo-ui-science/src/techDevelopmentTracking.js:1017",
        "repos/demo-ui-science/src/techDevelopmentTracking.js:59",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书（《科技发展态势/技术发展跟踪.md》《科技全域态势.md》《全球创新监测.md》）未出现「平均成熟度」该指标名；技术发展跟踪.md seq 50 动态气泡图叶提及「位置表示技术发展阶段或成熟度」属可视化描述非指标定义",
    },
    "facts": facts,
    "derived": {
        "jiuxin_avg_stage_order_8scale": {
            "value": facts["jiuxin_avg_stage_order_8scale"],
            "numerator": int(round(avg_order * n_nodes)),
            "denominator": n_nodes,
            "note": "分子=Σ(节点数×stage_order)（8 分制加权和取整），分母=19,430 节点；同源表 ads_technology_stage_assessment+transfer_stage",
        },
        "jiuxin_avg_maturity_pct_scale": {
            "value": facts["jiuxin_avg_maturity_pct_scale"],
            "numerator": int(round(avg_pct * n_nodes)),
            "denominator": n_nodes,
            "note": "百分制映射 (stage_order-1)/7×100 后按节点数加权；分子为加权整数和，分母同上",
        },
    },
    "absence_probe": [p for p in probes if p["source"] in ("gkx", "dev")],
    "support_judgment": "部分支持",
    "notes": [
        "久新 stage_assessment 是 RULE_BASED_EVIDENCE_BASELINE 规则基线（非 TRL 认证、非专家确认），stage_confidence 全表恒 0.9",
        "每节点 2 行对应 2 个 model_version（technology_insight_mvp_v1 / v2_eto_cluster_technology），节点级聚合已按 DISTINCT technology_node_id 去重",
        "UI mock 平均成熟度 72（演示值，不参与支持度结论）；百分制口径 72.4476 与 mock 量纲（分）对齐纯属巧合，不得引用作数据证据",
        "8 分制均值 6.0713 受基线阶段只落在 ENGINEERING(5)/INDUSTRIALIZATION(7) 两档限制——19,430 节点无一落在 1-4/6/8 档，读数含义是『平均已过工程化、贴近产业化』",
        "「领域」维度：候选节点是 ETO 研究簇候选（node_identity_type=RESEARCH_CLUSTER_CANDIDATE），无正式技术目录/领域映射，领域切片口径待裁定",
    ],
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "stage_assessment 无统计年份列（版本化 data_version/model_version 制，非年度序列）；热点对照窗 2020-2022/近期窗 2023-2025 属上游 hotspot 口径，本表不含年份",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "38860", "19430", "72.4476", "6.0713", "20816", "18044", "10408", "9022", "0.9000","7688","85.7143"]},
}
path = os.path.join(HERE, "M_SCIUI_TECHTRK_009_out.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", path)
print("support_judgment:", out["support_judgment"])
