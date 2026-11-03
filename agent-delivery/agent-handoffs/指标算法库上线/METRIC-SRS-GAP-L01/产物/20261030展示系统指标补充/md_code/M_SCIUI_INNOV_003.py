#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INNOV_003 技术关联强度（共现/引用）—— 三源探针 + 复现脚本（批 S3-01，Lane 5）。

UI 挂载（三处，均实查）：
  ① repos/demo-ui-science/src/graphEntityRanking.js:8
     ENTITY_RANKING_SORT_OPTIONS { key: 'relationStrength', label: '关联强度' }（默认排序列）
     :22-26 getGraphEntityMetricValue: relationStrength ?? Math.round(score*0.95) —— 无真值时以 score×0.95 伪造
  ② repos/demo-ui-science/src/graphObjectDetail.js:7-9
     GRAPH_NODE_METRICS = { robot:{relationStrength:92,...}, embodied:{relationStrength:96,...}, vision:{...88} }
     :51 metricCards { label: '关联强度', value: metrics.relationStrength }
     :130 relationStrength = entity?.relationStrength ?? Math.max(72, score-4) —— 兜底伪值
  mock 值 88-96（演示值，不参与支持度结论）

三源：
  ① 开发库：graph_node/graph_edge（gkxlumenx_ads+dwd）存在但需行数核查（产业链图谱非技术关联）
  ② gkx：280 表无关联强度/共现结果面（absence 探针留证）
  ③ 久新：ads_technology_graph_edge 587,252 行
     （relation_type 4 类 × relation_confidence_score 27.08-100 × topic_jaccard × evidence_level）
     + ads_institution_collaboration_yearly 14,380,246 行（collaboration_strength）—— 本件主承载

复现口径（B10 双口径并列，与 UI「关系权重」0-100 语义对齐）：
  口径 A（边置信度）：relation_confidence_score 直读（relation_type 分组均值+全局均值）
  口径 B（Jaccard 共现）：topic_jaccard 直读（同分组；与 R1 共现分析权威方法同族）
"""
import json
import os
import sys

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _gkxdb import gkx  # noqa: E402

JX = dict(
    host="47.93.119.170",
    port=29030,
    user="test2",
    password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
    database="gkx_technology_analysis_dev",
    connect_timeout=30,
    read_timeout=300,
)
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           connect_timeout=20, read_timeout=120)

facts = {}
probes = []


def probe(tag, source, sql, cur):
    try:
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


def q(sql):
    jc.execute(sql)
    return jc.fetchall()


facts["jiuxin_graph_edge_rows"] = int(q("SELECT COUNT(*) FROM ads_technology_graph_edge")[0][0])
facts["jiuxin_graph_node_rows"] = 19430  # 共享快照 _probe_lane3_final_out.json（B11 零漂移）

# 口径 A：relation_confidence_score 按 relation_type
facts["jiuxin_edge_confidence_by_type"] = [
    {"relation_type": str(t), "edges": int(n),
     "avg_confidence": round(float(a), 4), "min_confidence": round(float(mn), 4),
     "max_confidence": round(float(mx), 4)}
    for t, n, a, mn, mx in q(
        "SELECT relation_type, COUNT(*), AVG(relation_confidence_score), "
        "MIN(relation_confidence_score), MAX(relation_confidence_score) "
        "FROM ads_technology_graph_edge GROUP BY relation_type ORDER BY 2 DESC")]
r = q("SELECT AVG(relation_confidence_score), MIN(relation_confidence_score), "
      "MAX(relation_confidence_score) FROM ads_technology_graph_edge")[0]
facts["jiuxin_edge_confidence_global_avg"] = round(float(r[0]), 4)
facts["jiuxin_edge_confidence_global_min"] = round(float(r[1]), 4)
facts["jiuxin_edge_confidence_global_max"] = round(float(r[2]), 4)

# 口径 B：topic_jaccard 按 relation_type
facts["jiuxin_edge_jaccard_by_type"] = [
    {"relation_type": str(t), "edges": int(n),
     "avg_jaccard": round(float(a), 6), "max_jaccard": round(float(mx), 6)}
    for t, n, a, mx in q(
        "SELECT relation_type, COUNT(*), AVG(topic_jaccard), MAX(topic_jaccard) "
        "FROM ads_technology_graph_edge GROUP BY relation_type ORDER BY 2 DESC")]

# 证据等级与来源
facts["jiuxin_edge_evidence_level_dist"] = {str(k): int(v) for k, v in q(
    "SELECT evidence_level, COUNT(*) FROM ads_technology_graph_edge "
    "GROUP BY evidence_level ORDER BY 2 DESC")}
facts["jiuxin_edge_relation_source_dist"] = {str(k): int(v) for k, v in q(
    "SELECT relation_source, COUNT(*) FROM ads_technology_graph_edge "
    "GROUP BY relation_source ORDER BY 2 DESC")}
facts["jiuxin_edge_direction_status_dist"] = {str(k): int(v) for k, v in q(
    "SELECT direction_status, COUNT(*) FROM ads_technology_graph_edge "
    "GROUP BY direction_status ORDER BY 2 DESC")}

# Top8 强关联边（两口径并列展示）
facts["jiuxin_top8_edges_by_confidence"] = [
    {"relation_type": str(t), "confidence": round(float(cf), 4),
     "jaccard": round(float(j), 6), "shared_topics": int(st),
     "shared_patents": int(sp)}
    for t, cf, j, st, sp in q(
        "SELECT relation_type, relation_confidence_score, topic_jaccard, shared_topic_count, "
        "shared_patent_count FROM ads_technology_graph_edge "
        "ORDER BY relation_confidence_score DESC, topic_jaccard DESC LIMIT 8")]

# 机构协同强度表（语义相邻承载，实体粒度非技术粒度）
facts["jiuxin_institution_collab_rows"] = int(q("SELECT COUNT(*) FROM ads_institution_collaboration_yearly")[0][0])
r = q("SELECT AVG(collaboration_strength), MAX(collaboration_strength), "
      "SUM(CASE WHEN collaboration_strength >= 0.5 THEN 1 ELSE 0 END) "
      "FROM ads_institution_collaboration_yearly")[0]
facts["jiuxin_collab_strength_avg"] = round(float(r[0]), 6)
facts["jiuxin_collab_strength_max"] = round(float(r[1]), 6)
facts["jiuxin_collab_strength_ge_half"] = int(r[2])

# 图节点社区角色（弦线图「节点」侧）
facts["jiuxin_graph_node_community_role_dist"] = {str(k): int(v) for k, v in q(
    "SELECT community_role, COUNT(*) FROM ads_technology_graph_node "
    "GROUP BY community_role ORDER BY 2 DESC")}

jc.close()
jx.close()

# ---------------------------------------------------------------- gkx（absence 探针）
gc = gkx()
rows = probe("gkx 280 表关联强度/共现结果面扫描", "gkx",
             "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
             "AND (table_name LIKE '%relation%' OR table_name LIKE '%coocur%' "
             "OR table_name LIKE '%strength%' OR table_name LIKE '%converge%')", gc)
facts["gkx_relation_like_tables"] = [r[0] for r in rows]
rows = probe("gkx 列名 relation_strength/jaccard 扫描", "gkx",
             "SELECT table_name, column_name FROM information_schema.columns WHERE table_schema='gkx' "
             "AND (column_name LIKE '%relation_strength%' OR column_name LIKE '%jaccard%' "
             "OR column_name LIKE '%association_strength%') LIMIT 20", gc)
facts["gkx_relation_like_columns"] = [[r[0], r[1]] for r in rows]
gc.close()

# ---------------------------------------------------------------- 开发库（absence 探针）
# ---- dev 段容错补丁(2026-11-01, B4: dev 不可达≠无数据, 沿用首跑实测值并标注) ----
try:
    dv = pymysql.connect(**DEV)
    dc = dv.cursor()
    rows = probe("dev gkxlumenx_dwd+ads graph/关联类表扫描", "dev",
                 "SELECT table_schema, table_name FROM information_schema.tables "
                 "WHERE table_schema IN ('gkxlumenx_dwd','gkxlumenx_ads') "
                 "AND (table_name LIKE '%graph%' OR table_name LIKE '%relation%')", dc)
    graph_tables = [(r[0], r[1]) for r in rows]
    facts["dev_graph_like_tables"] = [[s, t] for s, t in graph_tables]
    facts["dev_graph_table_rows"] = {}
    for sch, t in graph_tables:
        if t in ("policy_graph_edge", "policy_graph_node", "graph_edge", "graph_node",
                 "event_relation", "enterprise_graph_rel"):
            try:
                dc.execute(f"SELECT COUNT(*) FROM {sch}.{t}")
                facts["dev_graph_table_rows"][t] = int(dc.fetchone()[0])
            except Exception as e:  # noqa: BLE001
                facts["dev_graph_table_rows"][t] = f"error: {str(e)[:80]}"
    dc.close()
    dv.close()
except Exception as _e:  # noqa: BLE001
    _po = os.path.join(HERE, "M_SCIUI_INNOV_003_out.json")
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
n_edges = facts["jiuxin_graph_edge_rows"]
out = {
    "metric_id": "M_SCIUI_INNOV_003",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/graphEntityRanking.js:8",
        "repos/demo-ui-science/src/graphObjectDetail.js:51",
        "repos/demo-ui-science/src/graphObjectDetail.js:7-9",
        "repos/demo-ui-science/src/graphObjectDetail.js:130",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「技术关联强度/关联强度」作为指标名未出现在三份说明书；最近语义为技术发展跟踪.md seq 51 弦线图展示『线条粗细表示技术间关联强度』（可视化映射描述非定义）与科学技术全景.md seq 叶『每个实体显示基本信息如名称、类型和关联强度』（展示字段非计算口径）",
    },
    "facts": facts,
    "derived": {
        "jiuxin_high_evidence_edge_pct": {
            "value": round(facts["jiuxin_edge_evidence_level_dist"].get("HIGH", 0) / n_edges * 100, 4),
            "numerator": facts["jiuxin_edge_evidence_level_dist"].get("HIGH", 0),
            "denominator": n_edges,
            "note": "分子=evidence_level=HIGH 边数，分母=全部边数；同表 ads_technology_graph_edge（B3 同基）",
        },
        "jiuxin_low_evidence_edge_pct": {
            "value": round(facts["jiuxin_edge_evidence_level_dist"].get("LOW", 0) / n_edges * 100, 4),
            "numerator": facts["jiuxin_edge_evidence_level_dist"].get("LOW", 0),
            "denominator": n_edges,
            "note": "分子=evidence_level=LOW 边数，分母同上；LOW 占 62.91% 是主降档因",
        },
    },
    "absence_probe": probes,
    "support_judgment": "部分支持",
    "notes": [
        "主承载是技术-技术边（19,430 个 ETO 研究簇候选节点 × 587,252 条边），与 UI 挂载的实体粒度（技术点/机构/论文/专利/专家混合图）不同构：UI 的 relationStrength 挂在实体上，库内强度挂在技术对上",
        "全部边 relation_source=DWS_INFERRED（推断），evidence_level LOW 占 62.91%（369,428 条）——强读数前须按证据等级过滤，否则弦线图会把弱推断画成粗线",
        "UI 前端两处兜底伪值（score×0.95 与 max(72, score-4)）说明前端作者知道 relationStrength 无真值来源；mock 88-96 为演示值不参与支持度结论",
        "口径 A（confidence 0-100）与 UI「关系权重」量纲同构可直映射；口径 B（Jaccard 0-1）是 R1/R2 权威共现方法族，两者并列待甲方裁定",
        "ads_institution_collaboration_yearly（1,438 万行）是机构-机构协同强度（论文/专利合作），语义相邻可作为实体粒度的补充承载，但其 Top 强度全为 1.000000（单篇合作顶格）区分度存疑",
        "「节点关联强度」（弦线图节点粗细）可由边聚合导出：node 表有 weighted_degree 列，属转换路径而非现成结果面",
    ],
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "graph_edge 无统计年份列（graph_release_id 快照制）；机构协同表有 statistics_year 但本件只消费强度列",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "587252", "19430", "49.0162", "100.0", "27.0797", "369428", "103358", "62.9079", "17.6003", "14380246", "964513","217824"]},
}
path = os.path.join(HERE, "M_SCIUI_INNOV_003_out.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", path)
print("support_judgment:", out["support_judgment"])
print("confidence by type:", facts["jiuxin_edge_confidence_by_type"])
print("jaccard by type:", facts["jiuxin_edge_jaccard_by_type"])
print("evidence:", facts["jiuxin_edge_evidence_level_dist"])
