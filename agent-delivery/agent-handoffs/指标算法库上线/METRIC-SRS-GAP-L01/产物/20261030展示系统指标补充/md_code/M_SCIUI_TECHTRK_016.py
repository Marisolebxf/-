#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TECHTRK_016 技术潜力评估得分 —— 复现/探针脚本（批 S3-01 Lane 3）。

数据源：久新 Doris gkx_technology_analysis_dev（只读）。
产物：code/M_SCIUI_TECHTRK_016_out.json（脚本产出，禁手改）。
"""
from __future__ import annotations

import json
import os
from datetime import date, datetime
from decimal import Decimal

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "M_SCIUI_TECHTRK_016_out.json")

JIUXIN = dict(
    host="47.93.119.170", port=29030, user="test2",
    password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
    database="gkx_technology_analysis_dev", charset="utf8mb4",
    connect_timeout=30, read_timeout=300, autocommit=True,
)

V2 = "technology_insight_mvp_v2_eto_cluster_technology"


def _f(v):
    if isinstance(v, Decimal):
        return float(v)
    return v


def q1(cur, sql):
    cur.execute(sql)
    r = cur.fetchone()
    return _f(r[0]) if r else None


def qall(cur, sql):
    cur.execute(sql)
    return [[_f(v) for v in r] for r in cur.fetchall()]


def main():
    conn = pymysql.connect(**JIUXIN)
    cur = conn.cursor()
    facts = {}

    # ---- potential_assessment（潜力评估得分主结果面） ----
    facts["jiuxin_potential_assessment_rows_total"] = int(q1(cur,
        "SELECT COUNT(*) FROM ads_technology_potential_assessment"))
    facts["jiuxin_potential_assessment_nodes_single_version"] = int(q1(cur,
        "SELECT COUNT(DISTINCT technology_node_id) FROM ads_technology_potential_assessment"))
    facts["jiuxin_potential_assessment_scenario"] = qall(cur,
        "SELECT DISTINCT scenario_id FROM ads_technology_potential_assessment")[0][0]
    facts["jiuxin_potential_assessment_method"] = qall(cur,
        "SELECT DISTINCT assessment_method FROM ads_technology_potential_assessment")[0][0]
    facts["jiuxin_potential_assessment_status"] = qall(cur,
        "SELECT DISTINCT assessment_status FROM ads_technology_potential_assessment")[0][0]
    facts["jiuxin_potential_score_stats_v2"] = {
        "n": int(q1(cur, "SELECT COUNT(potential_score) FROM ads_technology_potential_assessment WHERE model_version='%s'" % V2)),
        "min": round(float(q1(cur, "SELECT MIN(potential_score) FROM ads_technology_potential_assessment WHERE model_version='%s'" % V2)), 6),
        "max": round(float(q1(cur, "SELECT MAX(potential_score) FROM ads_technology_potential_assessment WHERE model_version='%s'" % V2)), 6),
        "avg": round(float(q1(cur, "SELECT AVG(potential_score) FROM ads_technology_potential_assessment WHERE model_version='%s'" % V2)), 6),
    }
    facts["jiuxin_metric_weight_coverage_all_one"] = float(q1(cur,
        "SELECT MIN(metric_weight_coverage) FROM ads_technology_potential_assessment"))  # 1.0（min=max=1.0）
    facts["jiuxin_potential_percentile_stats_v2"] = {
        "min": round(float(q1(cur, "SELECT MIN(potential_percentile) FROM ads_technology_potential_assessment WHERE model_version='%s'" % V2)), 6),
        "max": round(float(q1(cur, "SELECT MAX(potential_percentile) FROM ads_technology_potential_assessment WHERE model_version='%s'" % V2)), 6),
    }

    # ---- potential_dimension（六维度权重体系） ----
    facts["jiuxin_potential_dimension_rows_total"] = int(q1(cur,
        "SELECT COUNT(*) FROM ads_technology_potential_dimension"))
    facts["jiuxin_potential_dimensions_v2"] = [
        {"dimension_code": r[0], "rows": int(r[1]), "avg_weight": round(float(r[2]), 4)}
        for r in qall(cur,
            "SELECT dimension_code, COUNT(*) c, AVG(dimension_weight) w "
            "FROM ads_technology_potential_dimension WHERE model_version='%s' "
            "GROUP BY dimension_code ORDER BY dimension_code" % V2)
    ]
    # 单节点全维度样本（复现加权过程）
    sample_node = q1(cur,
        "SELECT MIN(technology_node_id) FROM ads_technology_potential_dimension WHERE model_version='%s'" % V2)
    facts["jiuxin_potential_dimension_sample_node"] = [
        {"technology_node_id": sample_node, "dimension_code": r[0],
         "raw_value": r[1], "dimension_score": round(float(r[2]), 6),
         "dimension_weight": float(r[3]), "weighted_score": round(float(r[4]), 6),
         "coverage_status": r[5]}
        for r in qall(cur,
            "SELECT dimension_code, raw_value, dimension_score, dimension_weight, "
            "weighted_score, coverage_status FROM ads_technology_potential_dimension "
            "WHERE model_version='%s' AND technology_node_id='%s' ORDER BY dimension_code"
            % (V2, sample_node))
    ]
    # 加和一致性（权重体系可复算性证据）
    facts["jiuxin_weighted_sum_consistent_nodes"] = int(q1(cur,
        "SELECT SUM(CASE WHEN ABS(t.dim_sum - t.score) < 0.0001 THEN 1 ELSE 0 END) FROM ("
        "SELECT d.technology_node_id, SUM(d.weighted_score) dim_sum, "
        "ANY_VALUE(p.potential_score) score "
        "FROM ads_technology_potential_dimension d "
        "JOIN ads_technology_potential_assessment p "
        "ON p.technology_node_id = d.technology_node_id AND p.model_version = d.model_version "
        "WHERE d.model_version='%s' GROUP BY d.technology_node_id) t" % V2))
    # v1 与 v2 同分（版本冗余证据）
    facts["jiuxin_v1_v2_same_score_nodes"] = int(q1(cur,
        "SELECT SUM(CASE WHEN a.potential_score = b.potential_score THEN 1 ELSE 0 END) "
        "FROM ads_technology_potential_assessment a "
        "JOIN ads_technology_potential_assessment b "
        "ON a.technology_node_id = b.technology_node_id "
        "AND a.model_version='technology_insight_mvp_v1' AND b.model_version='%s'" % V2))

    # ---- 与 stage 表同值审计 ----
    facts["jiuxin_stage_vs_potential_same_rows"] = int(q1(cur,
        "SELECT SUM(CASE WHEN a.development_potential_score = p.potential_score "
        "THEN 1 ELSE 0 END) FROM ads_technology_stage_assessment a "
        "JOIN ads_technology_potential_assessment p "
        "ON a.technology_node_id = p.technology_node_id AND a.model_version = p.model_version"))

    # ---- 潜力证据表 ----
    facts["jiuxin_potential_evidence_rows"] = int(q1(cur,
        "SELECT COUNT(*) FROM ads_technology_potential_evidence"))
    facts["jiuxin_potential_evidence_distinct_assessments"] = int(q1(cur,
        "SELECT COUNT(DISTINCT assessment_id) FROM ads_technology_potential_evidence"))

    # UI mock 读数登记（非数据证据）
    facts["ui_mock_plan_records_potential"] = [92, 95, 86, 88, 90, 87, 80]
    facts["ui_mock_metrics_card_label"] = "潜力均值"

    absence_probe = [
        {"probe": "dev 技术潜力得分结果面",
         "source": "dev",
         "sql": "SHOW TABLES FROM gkxlumenx_dwd LIKE '%potential%'/'%score%'（0 命中；评估类仅政策侧 4 表，见 _probe_lane3_gkx_out.json）",
         "hits": 0},
        {"probe": "gkx 技术潜力结果面（280 表）",
         "source": "gkx",
         "sql": "SHOW TABLES FROM gkx LIKE '%potential%'（0 命中，见 _probe_lane3_gkx_out.json）",
         "hits": 0},
        {"probe": "jiuxin 多场景权重体系（scenario 轴）",
         "source": "jiuxin",
         "sql": "SELECT DISTINCT scenario_id FROM ads_technology_potential_assessment（仅 BASELINE 单场景）",
         "hits": 1},
        {"probe": "jiuxin 历史轮次",
         "source": "jiuxin",
         "sql": "SELECT DISTINCT metrics_as_of_date FROM ads_technology_potential_assessment（单轮次 2026-10-16）",
         "hits": 1},
    ]

    out = {
        "metric_id": "M_SCIUI_TECHTRK_016",
        "batch": "S3-01",
        "ui_evidence": [
            "repos/demo-ui-science/src/techDevelopmentPlan.js:307",
            "repos/demo-ui-science/src/techDevelopmentPlan.js:483",
            "repos/demo-ui-science/src/techDevelopmentPlan.js:296",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "三份说明书未出现「技术潜力评估得分」指标名。近义功能名存在于其他板块说明书：《科技专题服务系统》技术链分析.md seq 17「潜力评估模型计算」、可视化管理.md seq 291「科技潜力评估可视化」——非本件挂载页所属说明书，仅作方法参考。",
        },
        "facts": facts,
        "derived": [
            {"key": "jiuxin_potential_avg_score_v2",
             "value": facts["jiuxin_potential_score_stats_v2"]["avg"],
             "numerator": facts["jiuxin_potential_score_stats_v2"]["n"],
             "denominator": facts["jiuxin_potential_assessment_nodes_single_version"],
             "note": "分子=v2 非空分计数 19430，分母=单版本节点数 19430（全节点有分）；AVG 由 SQL 聚合。"},
            {"key": "jiuxin_dimension_weight_sum",
             "value": round(sum(d["avg_weight"] for d in facts["jiuxin_potential_dimensions_v2"]), 4),
             "numerator": len(facts["jiuxin_potential_dimensions_v2"]),
             "denominator": len(facts["jiuxin_potential_dimensions_v2"]),
             "note": "六维权重合计=1.0（0.2+0.2+0.2+0.15+0.15+0.1）；分子分母均为 v2 维度数 6，值为权重和。"},
            {"key": "jiuxin_score_span_pct",
             "value": round(facts["jiuxin_potential_score_stats_v2"]["max"]
                            - facts["jiuxin_potential_score_stats_v2"]["min"], 6),
             "numerator": round(facts["jiuxin_potential_score_stats_v2"]["max"], 6),
             "denominator": round(facts["jiuxin_potential_score_stats_v2"]["min"], 6),
             "note": "极差=max-min（分子分母同 v2 单版本口径）；非相除关系，denominator 记 min 供对账。"},
        ],
        "absence_probe": absence_probe,
        "support_judgment": "部分支持",
        "notes": [
            "「技术潜力评估得分」在久新有结构完整的直接承载（potential_score + 六维 weighted_score 加权体系 + 百分位 + 证据表），且 19430 节点全量有分、权重覆盖 100%、加和可复算；降档主因是单场景（BASELINE）单轮次——UI 的「潜力评估」维度（techDevelopmentPlan.js:307）挂多区域规划记录，库侧无可配置场景/区域裁剪。",
            "v1 与 v2 两版本逐节点同分（19430/19430 同值），两行是同分数重复存储；全表 38860 行须按单版本 19430 读数。",
            "UI mock planRecords.potential 92/95/86/88/90/87/80 与维度卡「潜力均值」为演示值（不参与支持度结论）。",
            "维度语义映射需甲方确认：INDUSTRY_PARTICIPATION→产业参与、PATENT_CONVERSION→专利转化、PROJECT_EVIDENCE→项目证据、SCIENTIFIC_*→科研规模/增长/影响。",
            "04-科技专题服务系统/技术链分析.md seq 17「潜力评估模型计算」属科技专题服务系统板块，与展示系统技术发展跟踪页非同页，引用时注明跨板块。",
        ],
        "base_years_used": ["2026"],
        "base_years_missing": ["2023", "2024", "2025"],
        "base_years_note": "UI 时间轴 2020-2026；库侧单轮快照（2026-10-16），无历史轮次得分序列。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": [
            "38860", "19430", "233160", "269882", "10.95939", "88.354264",
            "44.871899", "1.0", "0.2", "0.15", "0.1", "6", "92", "95", "86","0.0001","27.717587","4289"]},
    }
    cur.close()
    conn.close()
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)


if __name__ == "__main__":
    main()
