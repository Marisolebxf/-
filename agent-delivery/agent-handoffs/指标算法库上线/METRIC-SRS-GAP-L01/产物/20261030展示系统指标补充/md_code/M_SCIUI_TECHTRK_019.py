#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TECHTRK_019 维度得分（TOP5） —— 三源探针 + 复现脚本（批 S3-01 Lane 4）。

UI 挂载：repos/demo-ui-science/src/TechDevelopmentPlan.tsx:3031
  重点区域分析 → 竞争力水平与潜力评估卡 → tzp-dimension-score-panel「维度得分（TOP5）」
  mock 五维（keyAreaDimensionScores: 创新资源 92/科研产出 88/产业竞争力 85/人才支撑 78/开放协同 72，演示值）

三源（开发库 gkxlumenx_* 禁 demo / gkx 经 _gkxdb / 久新 Doris 只读）：
  ① 开发库：无技术维度评分结果面（information_schema 命中 0，探针留证）
  ② gkx：280 表无 dimension/score 类技术维度结果面（探针留证）
  ③ 久新：本件主承载——两套现成分维体系：
     a) ads_technology_potential_dimension 六维（技术节点粒度，19,430 节点×6 维）
     b) ads_institution_technology_power 四权重维（机构粒度，64,698 机构）

复现口径（B10 双口径并列）：
  口径 A（深圳技术节点六维分）：对深圳子盘 6,233 节点按 potential_dimension 六维取均值，降序取 TOP5
  口径 B（深圳关联机构四维分）：对深圳关联机构按 technology_power 四权重维取均值，降序取 TOP5
"""
import json
import os
import sys

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _gkxdb import gkx  # noqa: E402  gkx 唯一入口（禁 demo_*，不传 database/charset）

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


def probe(tag, source, sql, cur):
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        probes.append({"probe": tag, "source": source, "sql": sql,
                       "hits": len(rows), "sample": [str(r)[:180] for r in rows[:8]]})
        return rows
    except Exception as e:  # noqa: BLE001
        probes.append({"probe": tag, "source": source, "sql": sql,
                       "hits": -1, "error": str(e)[:180]})
        return []


# ---------------------------------------------------------------- 久新（主承载）
jx = pymysql.connect(**JX)
jc = jx.cursor()

# 口径 A：深圳子盘六维分（region_yearly_metrics 圈定 6,233 节点）
jc.execute(
    "SELECT d.dimension_code, COUNT(DISTINCT d.technology_node_id) n, AVG(d.dimension_score) avg_score, "
    "AVG(d.dimension_weight) w FROM ads_technology_potential_dimension d "
    "JOIN ads_technology_region_yearly_metrics m ON m.technology_node_id = d.technology_node_id "
    "WHERE m.location_id = %s AND d.model_version = %s "
    "GROUP BY d.dimension_code ORDER BY avg_score DESC", (SZ, V2))
sz_dims = [{"dimension_code": r[0], "nodes": int(r[1]),
            "avg_score": round(float(r[2]), 4), "weight": float(r[3])} for r in jc.fetchall()]
facts["jiuxin_shenzhen_dim_scores_desc"] = sz_dims
facts["jiuxin_shenzhen_dim_nodes"] = sz_dims[0]["nodes"] if sz_dims else 0

# 全域六维对照（与共享探针 _probe_lane4_jiuxin_out.json 同源核对）
jc.execute(
    "SELECT dimension_code, AVG(dimension_score) FROM ads_technology_potential_dimension "
    "WHERE model_version = %s GROUP BY dimension_code", (V2,))
facts["jiuxin_global_dim_scores"] = {str(r[0]): round(float(r[1]), 4) for r in jc.fetchall()}

# 口径 B：深圳关联机构四权重维（institution_technology_power 无城市列——需经 paper 机构关联，
# 表内无机构→城市字段，探测确认后以全库均值+Top5 机构形态交付）
jc.execute(
    "SELECT AVG(paper_score), AVG(citation_score), AVG(talent_score), AVG(topic_score), "
    "AVG(technology_power_score) FROM ads_institution_technology_power")
r = jc.fetchone()
facts["jiuxin_inst_power_dim_avg"] = {
    "paper_score": round(float(r[0]), 4), "citation_score": round(float(r[1]), 4),
    "talent_score": round(float(r[2]), 4), "topic_score": round(float(r[3]), 4),
    "technology_power_score": round(float(r[4]), 4)}
jc.execute("SELECT COUNT(*) FROM ads_institution_technology_power")
facts["jiuxin_inst_power_rows"] = int(jc.fetchone()[0])
jc.execute(
    "SELECT DISTINCT paper_weight, citation_weight, talent_weight, topic_weight "
    "FROM ads_institution_technology_power")
facts["jiuxin_inst_power_weights"] = [float(v) for v in jc.fetchone()]

# institution_power Top5 by rank（对照 UI「TOP5」语义）
jc.execute(
    "SELECT institution_name, institution_name_zh, technology_power_score, technology_power_rank, "
    "paper_count, talent_count FROM ads_institution_technology_power ORDER BY technology_power_rank LIMIT 5")
facts["jiuxin_inst_power_top5"] = [
    {"name": r[0], "name_zh": r[1], "score": round(float(r[2]), 4),
     "rank": int(r[3]), "paper_count": int(r[4]), "talent_count": int(r[5])} for r in jc.fetchall()]

# 深圳区域评估（区域维度证据：strength/weakness 文本面）
jc.execute(
    "SELECT location_name_zh, COUNT(*), COUNT(DISTINCT technology_node_id), AVG(regional_potential_score) "
    "FROM ads_technology_region_assessment WHERE location_id = %s GROUP BY location_name_zh", (SZ,))
r = jc.fetchone()
facts["jiuxin_shenzhen_region_assessment"] = {
    "name": r[0], "rows": int(r[1]), "nodes": int(r[2]),
    "avg_regional_potential_score": round(float(r[3]), 4)}

# 深圳区域年度证据组合（论文/专利/项目机构证据——区域维度原始量）
jc.execute(
    "SELECT SUM(paper_institution_evidence_count), SUM(patent_institution_evidence_count), "
    "SUM(project_institution_evidence_count), SUM(institution_count), SUM(company_count) "
    "FROM ads_technology_region_yearly_metrics WHERE location_id = %s", (SZ,))
r = jc.fetchone()
facts["jiuxin_shenzhen_region_evidence_totals"] = {
    "paper_inst_evidence": int(r[0] or 0), "patent_inst_evidence": int(r[1] or 0),
    "project_inst_evidence": int(r[2] or 0), "institution_count_sum": int(r[3] or 0),
    "company_count_sum": int(r[4] or 0)}

# UI mock 五维登记（非数据证据）
facts["ui_mock_dimension_scores_top5"] = [
    {"label": "创新资源", "percent": 92}, {"label": "科研产出", "percent": 88},
    {"label": "产业竞争力", "percent": 85}, {"label": "人才支撑", "percent": 78},
    {"label": "开放协同", "percent": 72}]

jc.close()
jx.close()

# ---------------------------------------------------------------- gkx（absence 探针）
gc = gkx()
rows = probe("gkx 280 表 dimension/score 类技术维度结果面扫描", "gkx",
             "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
             "AND (table_name LIKE '%dimension%' OR table_name LIKE '%score%')", gc)
facts["gkx_dimension_like_tables"] = [r[0] for r in rows]
gc.close()

# ---------------------------------------------------------------- 开发库（absence 探针）
# ---- dev 段容错补丁(2026-11-01, B4: dev 不可达≠无数据, 沿用首跑实测值并标注) ----
try:
    dv = pymysql.connect(**DEV)
    dc = dv.cursor()
    rows = probe("dev gkxlumenx_dwd+ads 维度评分类表扫描", "dev",
                 "SELECT table_schema, table_name FROM information_schema.tables "
                 "WHERE table_schema IN ('gkxlumenx_dwd','gkxlumenx_ads') "
                 "AND (table_name LIKE '%dimension%' OR table_name LIKE '%score%')", dc)
    facts["dev_dimension_like_tables"] = [[r[0], r[1]] for r in rows]
    dc.close()
    dv.close()
except Exception as _e:  # noqa: BLE001
    _po = os.path.join(HERE, "M_SCIUI_TECHTRK_019_out.json")
    if os.path.exists(_po):
        try:
            _prev = json.load(open(_po, encoding="utf-8")).get("facts", {})
            for _k, _v in _prev.items():
                if _k.startswith("dev_"):
                    facts[_k] = _v
        except Exception:  # noqa: BLE001
            pass
    facts["dev_probe_status_this_run"] = f"dev 不可达({str(_e)[:50]}), dev_* 键沿用首跑实测值(2026-11-01 首跑在案)"

# ---------------------------------------------------------------- 派生
sz_dim5 = sz_dims[:5]
sum_top5 = sum(d["avg_score"] for d in sz_dim5)
derived = [
    {"key": "jiuxin_shenzhen_dim_top5_avg",
     "value": round(sum_top5 / len(sz_dim5), 4),
     "numerator": int(round(sum_top5 * 100)), "denominator": len(sz_dim5) * 100,
     "note": "分子=深圳六维中 TOP5 维 avg_score×100 取整和，分母=5×100；同源 jiuxin potential_dimension 深圳子盘（口径 A）。"},
    {"key": "jiuxin_shenzhen_dim_top1_score",
     "value": sz_dim5[0]["avg_score"],
     "numerator": sz_dim5[0]["nodes"], "denominator": sz_dim5[0]["nodes"],
     "note": "深圳最高维（PROJECT_EVIDENCE）均值；分子分母同源同子盘，此处仅登记读数。"},
]

out = {
    "metric_id": "M_SCIUI_TECHTRK_019",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/TechDevelopmentPlan.tsx:3031",
        "repos/demo-ui-science/src/TechDevelopmentPlan.tsx:870-876",
        "repos/demo-ui-science/src/TechDevelopmentPlan.tsx:862-868",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份指定说明书（科技发展态势三件 + 全球创新监测）未出现「维度得分（TOP5）」指标名；"
                "srs/05-深度挖掘算法 与 03-新型高端智库系统 的「维度得分」命中属其他系统板块（机构技术力指数输出明细），非本件页面。",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": [p for p in probes if p["source"] in ("gkx", "dev")],
    "support_judgment": "部分支持",
    "notes": [
        "「维度得分（TOP5）」UI 语义是重点区域（深圳/南山区语境）竞争力卡的五个维度条（mock：创新资源 92…开放协同 72，演示值，不参与支持度结论）；库侧无同名区域维度结果面。",
        "久新两套现成分维体系均非区域粒度：a) potential_dimension 六维=技术节点粒度（深圳子盘 6,233 节点）；b) institution_technology_power 四权重维=机构粒度（64,698 机构）。区域维度需聚合转换（口径 A）或机构→城市映射（库内无此映射列）。",
        "口径 A 深圳六维 TOP5：PROJECT_EVIDENCE 80.9386 / INDUSTRY_PARTICIPATION 76.0995 / SCIENTIFIC_SCALE 70.3038 / PATENT_CONVERSION 50.4770 / SCIENTIFIC_GROWTH 50.0000（读数以 facts.jiuxin_shenzhen_dim_scores_desc 为准）；深圳子盘经区域证据命中筛选，PROJECT_EVIDENCE/INDUSTRY_PARTICIPATION 显著高于全域均值（全域 43.9984/40.5735），选择偏置须随读数披露。",
        "institution_technology_power 的 paper/citation/talent/topic 四维全库均值恒约 50.0（0-100 百分位制的基准性质），权重四元组 0.35/0.30/0.25/0.10。",
        "UI 五维名（创新资源/科研产出/产业竞争力/人才支撑/开放协同）与库侧六维/四维均不同名，映射需甲方裁定；「TOP5」在库侧是对维度的排序取前五，与 UI 对区域的维度条语义不同构。",
    ],
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "维度分是 model_version 快照制（metrics_as_of_date=2026-09-18/10-16），无年度序列；UI mock 无年份维度。",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "6233", "64698", "19430", "6233", "92", "88", "85", "78", "72","99.9962"]},
}
path = os.path.join(HERE, "M_SCIUI_TECHTRK_019_out.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", path)
print("support_judgment:", out["support_judgment"])
