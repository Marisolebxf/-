#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TECHTRK_014 评估数据收集量 —— 复现/探针脚本（批 S3-01 Lane 3）。

数据源：久新 Doris gkx_technology_analysis_dev（只读）。
产物：code/M_SCIUI_TECHTRK_014_out.json（脚本产出，禁手改）。
"""
from __future__ import annotations

import json
import os
from datetime import date, datetime
from decimal import Decimal

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "M_SCIUI_TECHTRK_014_out.json")

JIUXIN = dict(
    host="47.93.119.170", port=29030, user="test2",
    password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
    database="gkx_technology_analysis_dev", charset="utf8mb4",
    connect_timeout=30, read_timeout=300, autocommit=True,
)

UI_SOURCES = ["论文", "专利", "项目", "资讯", "知识图谱"]  # techDevelopmentTracking.js:1100


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

    # ---- 久新技术画像底册（多源证据量总盘） ----
    facts["jiuxin_ads_technology_profile_rows"] = int(q1(cur,
        "SELECT COUNT(*) FROM ads_technology_profile"))
    facts["jiuxin_profile_sum_paper_count"] = int(q1(cur,
        "SELECT SUM(paper_count) FROM ads_technology_profile"))
    facts["jiuxin_profile_sum_patent_count"] = int(q1(cur,
        "SELECT SUM(patent_count) FROM ads_technology_profile"))
    facts["jiuxin_profile_sum_institution_count"] = int(q1(cur,
        "SELECT SUM(institution_count) FROM ads_technology_profile"))
    facts["jiuxin_profile_sum_company_count"] = int(q1(cur,
        "SELECT SUM(company_count) FROM ads_technology_profile"))
    facts["jiuxin_profile_sum_project_case_count"] = int(q1(cur,
        "SELECT SUM(project_case_count) FROM ads_technology_profile"))
    facts["jiuxin_profile_sum_application_case_count"] = int(q1(cur,
        "SELECT SUM(application_case_count) FROM ads_technology_profile"))

    # ---- data_coverage 域级证据量（014 的核心读数：本轮评估各源收集量） ----
    facts["jiuxin_data_coverage_rows"] = int(q1(cur,
        "SELECT COUNT(*) FROM ads_technology_data_coverage"))
    facts["jiuxin_data_coverage_node_count"] = int(q1(cur,
        "SELECT COUNT(DISTINCT technology_node_id) FROM ads_technology_data_coverage"))
    facts["jiuxin_data_coverage_by_domain"] = [
        {"domain_code": r[0], "rows": int(r[1]), "evidence_sum": int(r[2]),
         "evidence_avg": round(float(r[3]), 2) if r[3] is not None else None}
        for r in qall(cur,
            "SELECT domain_code, COUNT(*) c, SUM(evidence_count) s, AVG(evidence_count) a "
            "FROM ads_technology_data_coverage GROUP BY domain_code ORDER BY domain_code")
    ]
    facts["jiuxin_data_coverage_status_dist"] = [
        {"coverage_status": r[0], "rows": int(r[1])}
        for r in qall(cur,
            "SELECT coverage_status, COUNT(*) c FROM ads_technology_data_coverage "
            "GROUP BY coverage_status ORDER BY c DESC")
    ]

    # ---- 评估证据明细表（本轮评估引用的证据行数） ----
    facts["jiuxin_assessment_evidence_rows"] = int(q1(cur,
        "SELECT COUNT(*) FROM ads_technology_assessment_evidence"))
    facts["jiuxin_assessment_evidence_by_type"] = [
        {"evidence_type": r[0], "rows": int(r[1])}
        for r in qall(cur,
            "SELECT evidence_type, COUNT(*) c FROM ads_technology_assessment_evidence "
            "GROUP BY evidence_type ORDER BY c DESC")
    ]

    # ---- 图谱接入读数 ----
    facts["jiuxin_graph_node_rows"] = int(q1(cur,
        "SELECT COUNT(*) FROM ads_technology_graph_node"))
    facts["jiuxin_graph_edge_rows"] = int(q1(cur,
        "SELECT COUNT(*) FROM ads_technology_graph_edge"))

    # ---- gkx / dev：论文与资讯源的可用性（共享快照键 + 本件实跑） ----
    # 共享快照 _shared_probe_s3_01_out.json：gkx 论文 dwd_zh_paper=100900、
    # 新闻 dwd_news_base=20000、政策 dwd_policy_base=20000；dev 无论文表。
    facts["gkx_dwd_zh_paper_rows_shared_snapshot"] = 100900
    facts["gkx_dwd_news_base_rows_shared_snapshot"] = 20000
    facts["gkx_dwd_policy_base_rows_shared_snapshot"] = 20000
    facts["dev_gkxlumenx_dwd_paper_tables"] = 0  # 共享快照 dims.dev：SHOW TABLES LIKE '%paper%' 命中 0

    # ---- 派生：五源对齐率 ----
    dom = {d["domain_code"]: d for d in facts["jiuxin_data_coverage_by_domain"]}
    ui_align = {
        "论文 PAPER": dom.get("PAPER", {}).get("evidence_sum", 0),
        "专利 PATENT": dom.get("PATENT", {}).get("evidence_sum", 0),
        "项目 PROJECT": dom.get("PROJECT", {}).get("evidence_sum", 0),
        "资讯 NEWS/MARKET": dom.get("MARKET", {}).get("evidence_sum", 0),
        "知识图谱 GRAPH_EDGE": facts["jiuxin_graph_edge_rows"],
    }
    matched = sum(1 for v in ui_align.values() if v and v > 0)
    derived = [{
        "key": "jiuxin_ui5source_align_rate_pct",
        "value": round(100.0 * matched / len(ui_align), 1),
        "numerator": matched,
        "denominator": len(ui_align),
        "note": "分子=UI 五源(论文/专利/项目/资讯/知识图谱, techDevelopmentTracking.js:1100)中久新本轮证据量>0 的源数；分母=5。同源口径：分子分母均来自 jiuxin data_coverage/domain 与 graph_edge 实测。",
    }]

    absence_probe = [
        {"probe": "dev 评估工作流数据收集量表（gkxlumenx_dwd 按关键词扫描）",
         "source": "dev",
         "sql": "SHOW TABLES FROM gkxlumenx_dwd LIKE '%coverage%'（另探 collect/gather/assess/score/potential/hotspot/heat/maturity/tech 各键，行号见 _probe_lane3_gkx_out.json）",
         "hits": 0},
        {"probe": "gkx 技术评估数据收集量结果面（280 表关键词扫描）",
         "source": "gkx",
         "sql": "SHOW TABLES FROM gkx LIKE '%assess%'/'%evaluation%'/'%score%'/'%coverage%'（关键词逐一扫描，见 _probe_lane3_gkx_out.json）",
         "hits": 0},
        {"probe": "jiuxin 资讯/新闻域（203 表 news/media/literature 关键词扫描）",
         "source": "jiuxin",
         "sql": "SHOW TABLES 后本地过滤 news/media/literature/report（见 _probe_lane3_final_out.json）",
         "hits": 0},
        {"probe": "jiuxin MARKET/POLICY 域证据量（data_coverage 域级实测）",
         "source": "jiuxin",
         "sql": "SELECT domain_code, SUM(evidence_count) FROM ads_technology_data_coverage GROUP BY domain_code（MARKET=0, POLICY=0）",
         "hits": 0},
    ]

    out = {
        "metric_id": "M_SCIUI_TECHTRK_014",
        "batch": "S3-01",
        "ui_evidence": [
            "repos/demo-ui-science/src/techDevelopmentTracking.js:1100",
            "repos/demo-ui-science/src/techDevelopmentTracking.js:1097-1105",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "三份说明书（《科技全域态势》《技术发展跟踪》《全球创新监测》）未出现「评估数据收集量」指标名；技术发展跟踪.md seq 52「评估流程概览」仅列环节名「数据收集」，无收集量指标定义。",
        },
        "facts": facts,
        "derived": derived,
        "absence_probe": absence_probe,
        "support_judgment": "部分支持",
        "notes": [
            "「评估数据收集量」UI 侧为评估工作流环节数据收集的状态注记（techDevelopmentTracking.js:1100），非数值读数；本件把「收集量」落为久新本轮评估（model_version=technology_insight_mvp_v2_eto_cluster_technology, metrics_as_of_date=2026-10-16）各源证据量实测。",
            "jiuxin 本轮单版本节点数 19430（profile/data_coverage 同基），全表行数 38860/194300 为双 model_version（v1+v2 同内容）所致，读数时须去重。",
            "UI 五源中「资讯」源在久新三源均无证据量（MARKET=0/POLICY=0、203 表无 news 类、gkx 新闻表未入评估链），是降档主因；gkx dwd_news_base=20000 行存在但未接入技术评估口径。",
            "domain_code×coverage_status 矩阵、case_type 单一值等分布读数来自 _probe_lane3_jiuxin3/4_out.json 快照，与共享快照 _shared_probe_s3_01_out.json 的 ads_* 行数零漂移。",
        ],
        "base_years_used": ["2026"],
        "base_years_missing": ["2025", "2024"],
        "base_years_note": "久新 data_coverage/stage_assessment 等 ADS 表为快照表（单 metrics_as_of_date=2026-10-16），无历史轮次；历史轮次评估记录（2023–2025 评估）三源均无承载。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": [
            "19430", "38860", "194300", "269882", "100900", "20000", "587252",
            "108479", "1071763", "2528802", "181735", "99821", "80", "5","20252024"]},
    }
    cur.close()
    conn.close()
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)


if __name__ == "__main__":
    main()
