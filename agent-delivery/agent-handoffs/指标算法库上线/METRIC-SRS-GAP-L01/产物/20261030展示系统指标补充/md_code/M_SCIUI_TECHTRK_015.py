#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TECHTRK_015 本次评估得分（当轮） —— 复现/探针脚本（批 S3-01 Lane 3）。

数据源：久新 Doris gkx_technology_analysis_dev（只读）。
产物：code/M_SCIUI_TECHTRK_015_out.json（脚本产出，禁手改）。
"""
from __future__ import annotations

import json
import os
from datetime import date, datetime
from decimal import Decimal

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "M_SCIUI_TECHTRK_015_out.json")

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

    # ---- stage_assessment（本轮评估结果面） ----
    facts["jiuxin_stage_assessment_rows_total"] = int(q1(cur,
        "SELECT COUNT(*) FROM ads_technology_stage_assessment"))
    facts["jiuxin_stage_assessment_nodes_single_version"] = int(q1(cur,
        "SELECT COUNT(DISTINCT technology_node_id) FROM ads_technology_stage_assessment"))
    facts["jiuxin_stage_assessment_rows_v2"] = int(q1(cur,
        "SELECT COUNT(*) FROM ads_technology_stage_assessment WHERE model_version='%s'" % V2))
    facts["jiuxin_stage_assessment_metrics_as_of_date"] = str(q1(cur,
        "SELECT DISTINCT metrics_as_of_date FROM ads_technology_stage_assessment"))
    facts["jiuxin_stage_assessment_stage_code_dist"] = [
        {"stage_code": r[0], "rows": int(r[1])}
        for r in qall(cur,
            "SELECT stage_code, COUNT(*) c FROM ads_technology_stage_assessment "
            "WHERE model_version='%s' GROUP BY stage_code ORDER BY c DESC" % V2)
    ]
    facts["jiuxin_stage_assessment_assessment_method"] = qall(cur,
        "SELECT DISTINCT assessment_method FROM ads_technology_stage_assessment")[0][0]
    facts["jiuxin_stage_assessment_scenario_type"] = qall(cur,
        "SELECT DISTINCT scenario_type FROM ads_technology_stage_assessment")[0][0]
    facts["jiuxin_stage_confidence_fixed"] = float(q1(cur,
        "SELECT DISTINCT stage_confidence FROM ads_technology_stage_assessment"))
    facts["jiuxin_development_potential_score_stats_v2"] = {
        "n": int(q1(cur, "SELECT COUNT(development_potential_score) FROM ads_technology_stage_assessment WHERE model_version='%s'" % V2)),
        "min": round(float(q1(cur, "SELECT MIN(development_potential_score) FROM ads_technology_stage_assessment WHERE model_version='%s'" % V2)), 6),
        "max": round(float(q1(cur, "SELECT MAX(development_potential_score) FROM ads_technology_stage_assessment WHERE model_version='%s'" % V2)), 6),
        "avg": round(float(q1(cur, "SELECT AVG(development_potential_score) FROM ads_technology_stage_assessment WHERE model_version='%s'" % V2)), 6),
    }
    # 转移阶段字典（stage_code 语义）
    facts["jiuxin_transfer_stage_dict"] = [
        {"stage_code": r[0], "stage_order": int(r[1]), "stage_name_zh": r[2]}
        for r in qall(cur,
            "SELECT stage_code, stage_order, stage_name_zh FROM ads_technology_transfer_stage "
            "ORDER BY stage_order")
    ]
    # UI 评估方法名对齐（techDevelopmentTracking.js:514-518 四方法）
    facts["jiuxin_assessment_methods_present"] = ["RULE_BASED_EVIDENCE_BASELINE"]

    # ---- 与 potential_assessment 冗余审计（同分证据） ----
    facts["jiuxin_stage_vs_potential_same_score_rows"] = int(q1(cur,
        "SELECT SUM(CASE WHEN a.development_potential_score = p.potential_score "
        "THEN 1 ELSE 0 END) FROM ads_technology_stage_assessment a "
        "JOIN ads_technology_potential_assessment p "
        "ON a.technology_node_id = p.technology_node_id "
        "AND a.model_version = p.model_version"))

    # ---- UI 矩阵 mock 侧读数登记（非数据证据） ----
    facts["ui_mock_current_overall_scores"] = {
        "expert": 82, "economic": 78, "operations": 75, "comprehensive": 80,
    }

    absence_probe = [
        {"probe": "dev 评估得分结果面（gkxlumenx_dwd + topic_enterprise 关键词）",
         "source": "dev",
         "sql": "SHOW TABLES FROM gkxlumenx_dwd LIKE '%score%'/'%assess%'/'%eval%'（命中仅政策类 policy_support_assessment 等 4 表，与技术评估得分无关）；topic_enterprise.evaluation_template 为参数模板（8 行 indicators_json/weights_json），无得分结果行",
         "hits": 0},
        {"probe": "gkx 技术评估得分结果面（280 表关键词扫描）",
         "source": "gkx",
         "sql": "SHOW TABLES FROM gkx LIKE '%score%'/'%assess%'/'%evaluation%'（全 0 命中，见 _probe_lane3_gkx_out.json）",
         "hits": 0},
        {"probe": "jiuxin 专家评估法/经济分析法/运筹学评价法等 UI 四方法（assessment_method 枚举实测）",
         "source": "jiuxin",
         "sql": "SELECT DISTINCT assessment_method FROM ads_technology_stage_assessment（仅 RULE_BASED_EVIDENCE_BASELINE 单值；scenario_type 仅 PUBLISHED_BASELINE）",
         "hits": 1},
        {"probe": "jiuxin 历史轮次（2023/2024/2025 评估）",
         "source": "jiuxin",
         "sql": "SELECT DISTINCT metrics_as_of_date FROM ads_technology_stage_assessment（仅 2026-10-16 单值）",
         "hits": 1},
        {"probe": "jiuxin 综合得分多方法并排矩阵（四方法×四维度 cells）",
         "source": "jiuxin",
         "sql": "potential_dimension 仅 BASELINE 单场景 6 维度（SCIENTIFIC_IMPACT/PROJECT_EVIDENCE/SCIENTIFIC_SCALE/PATENT_CONVERSION/SCIENTIFIC_GROWTH/INDUSTRY_PARTICIPATION），无 expert/economic/operations/comprehensive 方法轴",
         "hits": 0},
    ]

    out = {
        "metric_id": "M_SCIUI_TECHTRK_015",
        "batch": "S3-01",
        "ui_evidence": [
            "repos/demo-ui-science/src/techDevelopmentTracking.js:510",
            "repos/demo-ui-science/src/techDevelopmentTracking.js:506-549",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "三份说明书未出现「本次评估得分（当轮）」指标名；技术发展跟踪.md seq 55「评估结果追踪」仅述历史记录与对比功能，无评分模型定义。",
        },
        "facts": facts,
        "derived": [
            {"key": "jiuxin_nodes_Industrialization_share_pct",
             "value": round(100.0 * facts["jiuxin_stage_assessment_stage_code_dist"][0]["rows"]
                            / facts["jiuxin_stage_assessment_rows_v2"], 2),
             "numerator": facts["jiuxin_stage_assessment_stage_code_dist"][0]["rows"],
             "denominator": facts["jiuxin_stage_assessment_rows_v2"],
             "note": "分子=INDUSTRIALIZATION（产业化）节点数，分母=v2 单版本节点总数 19430；同源同版本（jiuxin stage_assessment v2）。"},
            {"key": "jiuxin_avg_score_v2",
             "value": facts["jiuxin_development_potential_score_stats_v2"]["avg"],
             "numerator": facts["jiuxin_development_potential_score_stats_v2"]["n"],
             "denominator": facts["jiuxin_stage_assessment_rows_v2"],
             "note": "均值口径：分子=非空分计数 19430，分母=单版本行数 19430（全非空）；AVG 由 SQL 直接聚合。"},
        ],
        "absence_probe": absence_probe,
        "support_judgment": "部分支持",
        "notes": [
            "「本次评估得分」UI 语义是评估历史矩阵「本次评估」列的当轮得分（综合得分/成熟度/产业化能力/创新活跃度四维度×四方法）；久新侧唯一承载是 ads_technology_stage_assessment.development_potential_score（单方法 RULE_BASED_EVIDENCE_BASELINE、单场景 PUBLISHED_BASELINE、单轮次 2026-10-16）。",
            "stage 与 potential 两表分数逐节点 100% 同值（38860/38860），系同一分数双表冗余存储；引用时只作一条证据计。",
            "UI mock 四方法当前列 82/78/75/80 分为演示值（演示值，不参与支持度结论）。",
            "维度名映射：UI「产业化能力」≈ potential_dimension 的 PATENT_CONVERSION+INDUSTRY_PARTICIPATION，「创新活跃度」≈ SCIENTIFIC_GROWTH；「技术成熟度」≈ stage_code 阶段档（非 0-100 连续分），为推测映射需甲方确认。",
        ],
        "base_years_used": ["2026"],
        "base_years_missing": ["2023", "2024", "2025"],
        "base_years_note": "UI 矩阵含 2023/2024/2025/本次 四轮；久新仅单轮快照（metrics_as_of_date=2026-10-16），历史三轮无承载。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": [
            "38860", "19430", "2026-10-16", "20816", "18044", "0.9",
            "10.95939", "88.354264", "44.871899", "82", "78", "75", "80","116580"]},
    }
    cur.close()
    conn.close()
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)


if __name__ == "__main__":
    main()
