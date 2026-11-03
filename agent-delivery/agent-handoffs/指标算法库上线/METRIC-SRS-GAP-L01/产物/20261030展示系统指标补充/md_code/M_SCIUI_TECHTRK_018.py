#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TECHTRK_018 技术竞争力水平与潜力评估 —— 复现/探针脚本（批 S3-01 Lane 3）。

数据源：久新 Doris gkx_technology_analysis_dev（只读）。
产物：code/M_SCIUI_TECHTRK_018_out.json（脚本产出，禁手改）。
"""
from __future__ import annotations

import json
import os
from datetime import date, datetime
from decimal import Decimal

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "M_SCIUI_TECHTRK_018_out.json")

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

    # ---- region_assessment（区域竞争力×潜力主结果面） ----
    facts["jiuxin_region_assessment_rows_total"] = int(q1(cur,
        "SELECT COUNT(*) FROM ads_technology_region_assessment"))
    facts["jiuxin_region_assessment_nodes_single_version"] = int(q1(cur,
        "SELECT COUNT(DISTINCT technology_node_id) FROM ads_technology_region_assessment"))
    facts["jiuxin_region_assessment_locations"] = int(q1(cur,
        "SELECT COUNT(DISTINCT location_id) FROM ads_technology_region_assessment"))
    facts["jiuxin_regional_potential_score_stats"] = {
        "n": int(q1(cur, "SELECT COUNT(regional_potential_score) FROM ads_technology_region_assessment")),
        "min": round(float(q1(cur, "SELECT MIN(regional_potential_score) FROM ads_technology_region_assessment")), 6),
        "max": round(float(q1(cur, "SELECT MAX(regional_potential_score) FROM ads_technology_region_assessment")), 6),
        "avg": round(float(q1(cur, "SELECT AVG(regional_potential_score) FROM ads_technology_region_assessment")), 6),
    }
    facts["jiuxin_region_stage_code_dist"] = [
        {"regional_stage_code": r[0], "rows": int(r[1])}
        for r in qall(cur,
            "SELECT regional_stage_code, COUNT(*) c FROM ads_technology_region_assessment "
            "GROUP BY regional_stage_code ORDER BY c DESC")
    ]
    facts["jiuxin_region_coverage_status"] = qall(cur,
        "SELECT DISTINCT evidence_coverage_status FROM ads_technology_region_assessment")[0][0]
    # 重点城市聚合读数（对应 UI 重点区域卡片）
    facts["jiuxin_region_key_cities"] = [
        {"location_name_zh": r[0], "rows": int(r[1]),
         "nodes": int(r[2]), "avg_score": round(float(r[3]), 6)}
        for r in qall(cur,
            "SELECT location_name_zh, COUNT(*), COUNT(DISTINCT technology_node_id), "
            "AVG(regional_potential_score) FROM ads_technology_region_assessment "
            "WHERE location_name_zh IN ('北京市','上海','广州市','深圳','杭州市','南京市') "
            "GROUP BY location_name_zh ORDER BY AVG(regional_potential_score) DESC")
    ]

    # ---- institution_power（区域/机构竞争力分项） ----
    facts["jiuxin_institution_power_rows"] = int(q1(cur,
        "SELECT COUNT(*) FROM ads_institution_technology_power"))
    facts["jiuxin_power_score_stats"] = {
        "min": round(float(q1(cur, "SELECT MIN(technology_power_score) FROM ads_institution_technology_power")), 6),
        "max": round(float(q1(cur, "SELECT MAX(technology_power_score) FROM ads_institution_technology_power")), 6),
        "avg": round(float(q1(cur, "SELECT AVG(technology_power_score) FROM ads_institution_technology_power")), 6),
    }
    facts["jiuxin_power_top5"] = [
        {"rank": int(r[0]), "institution_name_zh": r[1],
         "technology_power_score": round(float(r[2]), 6),
         "paper_count": int(r[3]), "cited_by_count": int(r[4]), "talent_count": int(r[5])}
        for r in qall(cur,
            "SELECT technology_power_rank, institution_name_zh, technology_power_score, "
            "paper_count, cited_by_count, talent_count "
            "FROM ads_institution_technology_power ORDER BY technology_power_rank LIMIT 5")
    ]

    # ---- 协作网络（开放协同维承载） ----
    facts["jiuxin_collaboration_yearly_rows"] = int(q1(cur,
        "SELECT COUNT(*) FROM ads_institution_collaboration_yearly"))
    facts["jiuxin_collaboration_intl_pair_rows"] = int(q1(cur,
        "SELECT COUNT(*) FROM ads_institution_collaboration_yearly "
        "WHERE collaborator_country_code IS NOT NULL"))

    # ---- 潜力分（018 潜力侧复用 016 同源） ----
    facts["jiuxin_potential_assessment_rows_total"] = int(q1(cur,
        "SELECT COUNT(*) FROM ads_technology_potential_assessment"))
    facts["jiuxin_potential_nodes_single_version"] = int(q1(cur,
        "SELECT COUNT(DISTINCT technology_node_id) FROM ads_technology_potential_assessment"))

    # ---- UI mock 卡片读数登记（非数据证据） ----
    facts["ui_mock_competitiveness_metrics"] = {
        "composite": 78.5, "innovation": 88, "industry": 85,
        "openness": 62, "potential": 82,
    }
    facts["ui_mock_dimension_scores_top5"] = [92, 88, 85, 78, 72]

    absence_probe = [
        {"probe": "dev 竞争力评估结果面（gkxlumenx_dwd）",
         "source": "dev",
         "sql": "SHOW TABLES FROM gkxlumenx_dwd LIKE '%compet%'/'%assess%'/'%eval%'/'%score%'（0 命中技术竞争力类；仅政策侧 4 表，见 _probe_lane3_gkx_out.json）",
         "hits": 0},
        {"probe": "gkx 竞争力结果面（280 表）",
         "source": "gkx",
         "sql": "SHOW TABLES FROM gkx LIKE '%compet%'/'%score%'/'%potential%'（0 命中，见 _probe_lane3_gkx_out.json）",
         "hits": 0},
        {"probe": "jiuxn 区域能力/开放协同维度（UI 五卡：综合/创新/产业基础/开放协同/发展潜力）",
         "source": "jiuxin",
         "sql": "region_assessment 仅 regional_potential_score 单一总分 + evidence 计数（institution/company/paper/patent/project），无五维分项结构；institution_power 有四分项（paper/citation/talent/topic）但主体是机构非区域；开放协同需 collaboration 表另行聚合",
         "hits": 0},
        {"probe": "jiuxin 重点园区/城区粒度（UI 对标行：南山区/深圳湾合作区/天河区/香港科技园/横琴）",
         "source": "jiuxin",
         "sql": "region_assessment location 命名实测 Top 均为市级（北京市/上海/广州市…），无园区/合作区级 location（region_assessment 区域名 Top15 探针，见 _probe_lane3_jiuxin4_out.json）",
         "hits": 0},
    ]

    # 派生：重点城市平均分相对读数
    kc = {c["location_name_zh"]: c for c in facts["jiuxin_region_key_cities"]}
    bj = kc.get("北京市", {}).get("avg_score", 0)
    sz = kc.get("深圳", {}).get("avg_score", 0)
    derived = [
        {"key": "jiuxin_beijing_avg_regional_score",
         "value": bj,
         "numerator": kc.get("北京市", {}).get("rows", 0),
         "denominator": kc.get("北京市", {}).get("nodes", 0),
         "note": "分子=北京市行数（node×location×model_version），分母=去重节点数；值为 AVG(regional_potential_score) 由 SQL 聚合。"},
        {"key": "jiuxin_beijing_vs_shenzhen_score_gap",
         "value": round(bj - sz, 6),
         "numerator": bj,
         "denominator": sz,
         "note": "北京市均分−深圳均分（同源同表同口径差值，非相除；denominator 记深圳均分供对账；库内命名「深圳」无「市」字）。"},
    ]

    out = {
        "metric_id": "M_SCIUI_TECHTRK_018",
        "batch": "S3-01",
        "ui_evidence": [
            "repos/demo-ui-science/src/TechDevelopmentPlan.tsx:3015",
            "repos/demo-ui-science/src/TechDevelopmentPlan.tsx:862-876",
            "repos/demo-ui-science/src/techDevelopmentPlan.js:39",
        ],
        "requirement_trace": {
            "named_in_srs": True,
            "note": "《科技发展规划.md》seq 186（excel_row 189）「竞争力水平与潜力评估」与指标名同义命中，功能描述原文见附录 A；但该叶属科技发展态势/科技发展规划页（非本件 UI 挂载的技术发展跟踪页），本件挂载组件为科技发展规划页重点领域规划 Tab——口径记录：指标名在需求文档存在（跨页面同名功能），三份指定说明书（科技全域态势/技术发展跟踪/全球创新监测）本身未出现该指标名。需求主文档《科技信息展示系统和科技专题服务系统.md》1129/1135 行同名词命中（重点领域规划功能列举）。",
        },
        "facts": facts,
        "derived": derived,
        "absence_probe": absence_probe,
        "support_judgment": "部分支持",
        "notes": [
            "「技术竞争力水平与潜力评估」UI 卡片（综合指数/创新能力/产业基础/开放协同/发展潜力 五卡+维度 TOP5+对标排名）在久新有部分承载：区域潜力分 region_assessment（2708162 行、7816 区域）、机构科技力量 institution_power（64698 行、四分项+权重）、协作网络 collaboration（1438 万行对）。",
            "降档主因一：无区域五维分项结构——UI 五卡需按维度出分，库侧区域粒度只有单一总分+证据计数，分维需自建（institution_power 四分项可撑创新/产出维，但主体是机构非行政区）；主因二：对标粒度失配——UI 对标行是园区/城区级（南山区/深圳湾合作区），库侧 location 最细到市级。",
            "全部 2708162 行 evidence_coverage_status=PARTIAL_INTERNAL_EVIDENCE（单一值），官方口径是『内部证据部分覆盖』，政策/市场证据未接入——评估结论展示须带覆盖度标签。",
            "region_assessment 亦为 v1/v2 双版本同内容（2×1354081），读数按单版本；stage 分布 EARLY_RESEARCH 占 99.3%。",
            "UI mock 五卡 78.5/88/85/62/82 与维度 92/88/85/78/72 为演示值（不参与支持度结论）。",
        ],
        "base_years_used": ["2026"],
        "base_years_missing": ["2023", "2024", "2025"],
        "base_years_note": "region_assessment/institution_power 为单轮快照（2026-10-16）；UI 需要历史对比的竞争力演进序列无承载（region_yearly_metrics 有 2015-2026 年度证据计数但无评分）。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": [
            "2708162", "1354081", "7816", "64698", "14380246", "0.0", "100.0",
            "39.834562", "99.3", "78.5", "88", "85", "62", "82", "92", "72",
            "48.889888", "47.926008", "47.059274","2930","3050"]},
    }
    cur.close()
    conn.close()
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)


if __name__ == "__main__":
    main()
