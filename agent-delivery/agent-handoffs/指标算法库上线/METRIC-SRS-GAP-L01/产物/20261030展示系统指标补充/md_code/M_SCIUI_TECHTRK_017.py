#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TECHTRK_017 技术热点热度值 —— 复现/探针脚本（批 S3-01 Lane 3）。

数据源：久新 Doris gkx_technology_analysis_dev（只读）。
产物：code/M_SCIUI_TECHTRK_017_out.json（脚本产出，禁手改）。
"""
from __future__ import annotations

import json
import os
from datetime import date, datetime
from decimal import Decimal

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "M_SCIUI_TECHTRK_017_out.json")

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

    # ---- hotspot_snapshot（热度值主结果面） ----
    facts["jiuxin_hotspot_snapshot_rows_total"] = int(q1(cur,
        "SELECT COUNT(*) FROM ads_technology_hotspot_snapshot"))
    facts["jiuxin_hotspot_nodes_single_version"] = int(q1(cur,
        "SELECT COUNT(DISTINCT technology_node_id) FROM ads_technology_hotspot_snapshot"))
    facts["jiuxin_hotspot_score_stats_v2"] = {
        "n": int(q1(cur, "SELECT COUNT(hotspot_score) FROM ads_technology_hotspot_snapshot WHERE model_version='%s'" % V2)),
        "min": round(float(q1(cur, "SELECT MIN(hotspot_score) FROM ads_technology_hotspot_snapshot WHERE model_version='%s'" % V2)), 6),
        "max": round(float(q1(cur, "SELECT MAX(hotspot_score) FROM ads_technology_hotspot_snapshot WHERE model_version='%s'" % V2)), 6),
        "avg": round(float(q1(cur, "SELECT AVG(hotspot_score) FROM ads_technology_hotspot_snapshot WHERE model_version='%s'" % V2)), 6),
    }
    facts["jiuxin_hotspot_status_dist_v2"] = [
        {"hotspot_status": r[0], "rows": int(r[1])}
        for r in qall(cur,
            "SELECT hotspot_status, COUNT(*) c FROM ads_technology_hotspot_snapshot "
            "WHERE model_version='%s' GROUP BY hotspot_status ORDER BY c DESC" % V2)
    ]
    # Top5（单版本去重口径）+ 技术中文名
    top5 = qall(cur,
        "SELECT h.technology_node_id, h.hotspot_score, h.hotspot_rank, h.hotspot_status, "
        "p.technology_name_zh FROM ads_technology_hotspot_snapshot h "
        "LEFT JOIN ads_technology_profile p ON p.technology_node_id = h.technology_node_id "
        "WHERE h.model_version='%s' ORDER BY h.hotspot_rank LIMIT 5" % V2)
    facts["jiuxin_hotspot_top5_v2"] = [
        {"rank": int(r[2]), "technology_node_id": r[0],
         "hotspot_score": round(float(r[1]), 6), "hotspot_status": r[3],
         "technology_name_zh": r[4]}
        for r in top5
    ]
    # 分量分（单版本 Top1 的五分量，复现口径）
    comp = qall(cur,
        "SELECT growth_score, author_diffusion_score, institution_diffusion_score, "
        "impact_score, patent_signal_score FROM ads_technology_hotspot_snapshot "
        "WHERE model_version='%s' ORDER BY hotspot_rank LIMIT 1" % V2)
    facts["jiuxin_hotspot_top1_components"] = {
        "growth_score": round(float(comp[0][0]), 6),
        "author_diffusion_score": round(float(comp[0][1]), 6),
        "institution_diffusion_score": round(float(comp[0][2]), 6),
        "impact_score": round(float(comp[0][3]), 6),
        "patent_signal_score": round(float(comp[0][4]), 6),
    }

    # ---- hotspot_yearly（年度热度序列；本表 model_version=technology_hotspot_yearly_v1） ----
    facts["jiuxin_hotspot_yearly_rows_total"] = int(q1(cur,
        "SELECT COUNT(*) FROM ads_technology_hotspot_yearly"))
    facts["jiuxin_hotspot_yearly_model_version"] = qall(cur,
        "SELECT DISTINCT model_version FROM ads_technology_hotspot_yearly")[0][0]
    facts["jiuxin_hotspot_yearly_years"] = [
        {"statistics_year": int(r[0]), "rows": int(r[1]),
         "avg_hotspot_score": round(float(r[2]), 6)}
        for r in qall(cur,
            "SELECT statistics_year, COUNT(*), AVG(hotspot_score) "
            "FROM ads_technology_hotspot_yearly "
            "GROUP BY statistics_year ORDER BY statistics_year DESC")
    ]
    facts["jiuxin_hotspot_yearly_trend_status_dist"] = [
        {"trend_status": r[0], "rows": int(r[1])}
        for r in qall(cur,
            "SELECT trend_status, COUNT(*) c FROM ads_technology_hotspot_yearly "
            "GROUP BY trend_status ORDER BY c DESC")
    ]

    # ---- hotspot_signal（资讯型热点信号词） ----
    facts["jiuxin_hotspot_signal_rows"] = int(q1(cur,
        "SELECT COUNT(*) FROM ads_technology_hotspot_signal"))
    facts["jiuxin_hotspot_signal_distinct_nodes"] = int(q1(cur,
        "SELECT COUNT(DISTINCT technology_node_id) FROM ads_technology_hotspot_signal"))
    facts["jiuxin_hotspot_signal_extraction_methods"] = [
        r[0] for r in qall(cur,
            "SELECT DISTINCT extraction_method FROM ads_technology_hotspot_signal")
    ]
    facts["jiuxin_hotspot_signal_sample"] = [
        {"signal_text_zh": r[0], "keyword_rank": int(r[1]),
         "evidence_paper_count": int(r[2]), "first_observed_year": int(r[3])}
        for r in qall(cur,
            "SELECT signal_text_zh, keyword_rank, evidence_paper_count, first_observed_year "
            "FROM ads_technology_hotspot_signal WHERE signal_text_zh IS NOT NULL "
            "ORDER BY keyword_rank LIMIT 5")
    ]

    # ---- gkx 侧热点词表 absence ----
    # 共享快照/第五轮探针：gkx dwd_industry_analysis_topics=1052 行（产业分析主题，
    # 文档级，无热度值列）；dwd_industry_analysis_topic_dict=92 行
    facts["gkx_industry_analysis_topics_rows"] = 1052
    facts["gkx_industry_analysis_topic_dict_rows"] = 92

    # UI mock 读数登记（非数据证据）
    facts["ui_mock_core_topics_heat"] = [92, 86, 81, 74, 78, 84, 89, 77]
    facts["ui_mock_trend_series_label"] = "热点热度"

    absence_probe = [
        {"probe": "dev 技术热度结果面",
         "source": "dev",
         "sql": "SHOW TABLES FROM gkxlumenx_dwd LIKE '%hot%'/'%heat%'/'%score%'（0 命中，见 _probe_lane3_gkx_out.json）",
         "hits": 0},
        {"probe": "gkx 技术热度结果面（280 表）",
         "source": "gkx",
         "sql": "SHOW TABLES FROM gkx LIKE '%hotspot%'/'%heat%'（0 命中；dwd_industry_analysis_topics 1052 行为产业分析文档主题表，12 列无热度值列，见 _probe_lane3_final_out.json）",
         "hits": 0},
        {"probe": "jiuxin hotspot_score 合成权重口径文档",
         "source": "jiuxin",
         "sql": "metric_definition_version 列存在但表内值为口径版本号（字符串），权重配比未见数据面承载（hotspot_score 与五分量分的相关结构可实测复算，权重本身未入库）",
         "hits": 0},
        {"probe": "jiuxin 资讯类热度分量（news/media 源）",
         "source": "jiuxin",
         "sql": "203 表 SHOW TABLES 本地过滤 news/media/literature（0 命中，见 _probe_lane3_final_out.json）；五分量均为论文/专利衍射，无资讯热度分量",
         "hits": 0},
    ]

    # 派生：单版本口径的可用热度节点占比
    n_nodes = facts["jiuxin_hotspot_nodes_single_version"]
    st = {s["hotspot_status"]: s["rows"] for s in facts["jiuxin_hotspot_status_dist_v2"]}
    evidence_sufficient = (st.get("ESTABLISHED_GROWING", 0) + st.get("MATURE", 0)
                           + st.get("WATCH", 0) + st.get("EARLY_EMERGING", 0))
    derived = [
        {"key": "jiuxin_hotspot_evidence_sufficient_share_pct",
         "value": round(100.0 * evidence_sufficient / n_nodes, 2),
         "numerator": evidence_sufficient,
         "denominator": n_nodes,
         "note": "分子=非 INSUFFICIENT_EVIDENCE 状态节点数（ESTABLISHED_GROWING+MATURE+WATCH+EARLY_EMERGING），分母=v2 单版本节点 19430；同源同版本。"},
        {"key": "jiuxin_insufficient_evidence_share_pct",
         "value": round(100.0 * st.get("INSUFFICIENT_EVIDENCE", 0) / n_nodes, 2),
         "numerator": st.get("INSUFFICIENT_EVIDENCE", 0),
         "denominator": n_nodes,
         "note": "分子=INSUFFICIENT_EVIDENCE 节点数，分母=v2 单版本节点 19430；同源同版本。"},
    ]

    out = {
        "metric_id": "M_SCIUI_TECHTRK_017",
        "batch": "S3-01",
        "ui_evidence": [
            "repos/demo-ui-science/src/techDevelopmentPlan.js:327",
            "repos/demo-ui-science/src/techDevelopmentPlan.js:473",
            "repos/demo-ui-science/src/techDevelopmentTracking.js:112",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "三份说明书未出现「技术热点热度值」指标名；技术发展跟踪.md seq 48「话题热力图展示」描述热度分布图功能但未定义热度值算法。",
        },
        "facts": facts,
        "derived": derived,
        "absence_probe": absence_probe,
        "support_judgment": "部分支持",
        "notes": [
            "「技术热点热度值」在久新有直接结果面：hotspot_score（0-100）+ 五分量分（growth/author_diffusion/institution_diffusion/impact/patent_signal）+ 年度序列 hotspot_yearly（2015-2026）+ 热点信号词表。",
            "降档主因一：19430 节点中 15976（82.23%）状态为 INSUFFICIENT_EVIDENCE——热度分可算但证据强度不足；主因二：五分量全为论文/专利衍射，UI 榜单语义的「资讯热度」无分量承载。",
            "hotspot_rank Top1 节点状态也是 INSUFFICIENT_EVIDENCE（rank=1, hotspot_status=INSUFFICIENT_EVIDENCE），榜单展示须带状态标签。",
            "v1/v2 双版本同内容（各 19430 行，总 38860 行），读数按单版本；hotspot_signal 表另有 filter_stage_20261031/unfiltered_20261031 两个日期缀快照表，引用主表为准。",
            "UI mock 热度值（92/86/81/74/78/84/89/77）与趋势序列「热点热度」为演示值（不参与支持度结论）。",
        ],
        "base_years_used": ["2015", "2016", "2017", "2018", "2019", "2020",
                            "2021", "2022", "2023", "2024", "2025", "2026"],
        "base_years_missing": [],
        "base_years_note": "hotspot_yearly 单版本覆盖 2015-2026 全 12 年（每年 19430 行），UI 时间轴 2020-2026 完整可得；2026 年均分骤降系年度进行中（数据截至 2026-10-16），非缺失。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": [
            "38860", "19430", "233160", "9018", "11.12924", "79.090792",
            "77.245098", "76.369602", "76.108652", "74.775593", "15976",
            "2539", "766", "292", "82.23", "13.07", "2015", "2026","1010","1018","159769"]},
    }
    cur.close()
    conn.close()
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)


if __name__ == "__main__":
    main()
