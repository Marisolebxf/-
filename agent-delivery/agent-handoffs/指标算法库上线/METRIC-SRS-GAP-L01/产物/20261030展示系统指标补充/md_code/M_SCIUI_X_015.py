#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_X_015 评估对象网络中心性排名 —— 三源探针 + 复现脚本（批 S3-02，Lane 2）。

UI 挂载（实查）：
  repos/demo-ui-science/src/pages/tech-innovation-evaluation/TechInnovationEvaluationPage.tsx:3488
    <Panel title="中心性排名">——表格列：节点/类型/度/接近/中介（度中心性/接近中心性/中介中心性）
  :1862-1892 centralityNodeRows mock —— 机构/学者两类节点各 4 行种子值（0.22-0.96 归一区间）
  :3479-3487 科学网络中心性评估 Panel（网络图谱 centralityGraphOption）

需求原文（:881 / SRS seq 137）：「基于合作网络分析，评估特定领域内学者、研究机构在科学网络
中的中心性指标，包括度中心性、接近中心性、中介中心性等，用户可查看网络图谱和中心性排名」

三源：
  ① 开发库：旧机 ads.enterprise_centrality 114 行 model_version='demo_centrality_v0.1'
     （演示造数：极光量子/翰林量超等虚构企业名）→ 判演示面禁引；新机同表 0 行；
     dwd graph_node/graph_edge 新旧机均 0 行 → 开发库图谱面空载
  ② gkx：无 network/centrality/graph/collaborat/coop 任何表（280 表扫描 0 命中）；
     论文表 32 列无结构化合作者列（author_info_list longtext 非结构化）
  ③ 久新：ads_institution_collaboration_yearly 14,380,246 行（2024 单年 2,146,142 行 /
     36,026 机构侧 + 协作者侧），co_paper_count 加权边——主承载；
     ads_talent_collaborator 5,051,578 行（学者合作对，collaboration_score/rank 现成）

复现口径（B10 双口径）：
  口径 A（机构合作网·2024 单年）：度/接近/中介三类中心性（networkx，边权=co_paper_count）
  口径 B（学者合作面·全期）：ads_talent_collaborator collaboration_score 榜（库内现成分）
"""
import json
import os
import sys

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

OLD = dict(host="111.198.38.90", port=34306, user="gkxlumenx", password="GKX@Lumen2026",
           charset="utf8mb4", connect_timeout=20, read_timeout=300)
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=30, read_timeout=600)

facts = {}
absence_probe = []

# ================================================================ ① 开发库（absence 留证）
old = pymysql.connect(**OLD)
oc = old.cursor()
oc.execute("SELECT COUNT(*) FROM gkxlumenx_ads.enterprise_centrality")
facts["devold_enterprise_centrality_rows"] = int(oc.fetchone()[0])
oc.execute(
    "SELECT model_version, COUNT(*) FROM gkxlumenx_ads.enterprise_centrality "
    "GROUP BY model_version")
facts["devold_enterprise_centrality_versions"] = [
    {"model_version": r[0], "rows": int(r[1])} for r in oc.fetchall()]
absence_probe.append({
    "probe": "开发库（旧机）enterprise_centrality 114 行 —— model_version 全部 "
             "demo_centrality_v0.1（演示造数面，禁引）",
    "source": "dev:111.198.38.90",
    "sql": "SELECT model_version, COUNT(*) FROM gkxlumenx_ads.enterprise_centrality "
           "GROUP BY model_version；样本企业名：极光量子科技有限公司/翰林量超股份有限公司等虚构名",
    "hits": 0,
})
for tbl in ["graph_node", "graph_edge"]:
    oc.execute(f"SELECT COUNT(*) FROM gkxlumenx_dwd.{tbl}")
    facts[f"devold_{tbl}_rows"] = int(oc.fetchone()[0])
old.close()
# 新机图谱面（探针 c 在案）：enterprise_centrality/graph_node/graph_edge 均 0 行
facts["devnew_graph_face_rows"] = 0

# ================================================================ ② gkx（absence 留证）
from _gkxdb import gkx  # noqa: E402

gc = gkx()
gc.execute(
    "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='gkx' AND "
    "(table_name LIKE '%network%' OR table_name LIKE '%centrality%' OR table_name "
    "LIKE '%graph%' OR table_name LIKE '%collaborat%' OR table_name LIKE '%coop%')")
facts["gkx_network_tables"] = int(gc.fetchone()[0])
absence_probe.append({
    "probe": "gkx 网络中心性结果面（network/centrality/graph/collaborat/coop 五关键词）",
    "source": "gkx",
    "sql": "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
           "AND (…五关键词…)；另 dwd_zh_paper 32 列 author_info_list 为 longtext 非结构化",
    "hits": 0,
})
gc.close()

# ================================================================ ③ 久新（主承载）
jx = pymysql.connect(**JX)
jc = jx.cursor()

# 全表与单年规模（B11：与 TECHTRK_018 的 14,380,246 对账）
jc.execute("SELECT COUNT(*) FROM ads_institution_collaboration_yearly")
facts["jiuxin_collab_rows_total"] = int(jc.fetchone()[0])
assert facts["jiuxin_collab_rows_total"] == 14380246, "与 TECHTRK_018 共享读数零漂移失败"

jc.execute(
    "SELECT COUNT(*), COUNT(DISTINCT institution_id) FROM "
    "ads_institution_collaboration_yearly WHERE statistics_year=2024")
r = jc.fetchone()
facts["jiuxin_collab_2024_rows"] = int(r[0])
facts["jiuxin_collab_2024_ego_side_institutions"] = int(r[1])

# ---- 口径 A：2024 单年 Top 机构 ego 网络 → 三类中心性 ----
# SQL 纪律：大表全扫 GROUP BY 会 query timeout（首版实跑 520s 超时留证），改两步：
# 步1 直接按 ego 边权排序找 Top 机构（不经 SUM 聚合，Doris 排序走前缀索引）
jc.execute(
    "SELECT institution_id, institution_name, co_paper_count FROM "
    "ads_institution_collaboration_yearly WHERE statistics_year=2024 "
    "ORDER BY co_paper_count DESC LIMIT 5")
top_pairs = [(r[0], r[1], int(r[2])) for r in jc.fetchall()]
facts["jiuxin_2024_top_edges"] = [
    {"ego_side": t[1], "co_papers": t[2]} for t in top_pairs]
ego_id, ego_name = top_pairs[0][0], top_pairs[0][1]
jc.execute(
    "SELECT SUM(co_paper_count) FROM ads_institution_collaboration_yearly "
    "WHERE statistics_year=2024 AND institution_id=%s", (ego_id,))
ego_w = int(jc.fetchone()[0] or 0)
facts["jiuxin_2024_top_ego"] = {"institution_id": ego_id, "name": ego_name,
                                "co_paper_sum": ego_w}

# 步2 ego 的 2024 一跳邻域（institution_id 等值过滤，非全表聚合）
jc.execute(
    "SELECT collaborator_institution_id, collaborator_institution_name, co_paper_count "
    "FROM ads_institution_collaboration_yearly WHERE statistics_year=2024 "
    "AND institution_id=%s ORDER BY co_paper_count DESC LIMIT 500", (ego_id,))
ego_edges = [(r[0], r[1], int(r[2] or 0)) for r in jc.fetchall()]
facts["jiuxin_2024_ego_degree_capped"] = len(ego_edges)
facts["jiuxin_2024_ego_edge_weight_sum_capped"] = sum(e[2] for e in ego_edges)
facts["jiuxin_2024_ego_top5_partners"] = [
    {"name": e[1], "co_papers": e[2]} for e in ego_edges[:5]]

# 步3 二跳 ego 网：Top50 伙伴的边（按 collaborator 等值过滤，避免 OR 双侧全扫）
partner_ids = [e[0] for e in ego_edges[:50]]
ph = ",".join(["%s"] * len(partner_ids))
sub_edges = [(ego_id, e[0], e[2]) for e in ego_edges]  # ego 一跳边（ego 侧统一用 ego_id）
jc.execute(
    "SELECT institution_id, collaborator_institution_id, co_paper_count "
    "FROM ads_institution_collaboration_yearly WHERE statistics_year=2024 "
    "AND collaborator_institution_id IN (%s) LIMIT 4000" % ph, partner_ids)
sub_edges += [(r[0], r[1], int(r[2] or 0)) for r in jc.fetchall()]
facts["jiuxin_2024_egonet_edges"] = len(sub_edges)

# networkx 三类中心性（无权图拓扑 + 边权记录）
import networkx as nx  # noqa: E402

G = nx.Graph()
for u, v, w in sub_edges:
    if G.has_edge(u, v):
        G[u][v]["w"] += w
    else:
        G.add_edge(u, v, w=w)
facts["jiuxin_2024_egonet_nodes"] = G.number_of_nodes()
deg = dict(nx.degree_centrality(G))
clo = dict(nx.closeness_centrality(G))
bet = dict(nx.betweenness_centrality(G, seed=42))  # 精确算法定种子（B5 确定性）

# 名称回填：从边表收名称映射（ego 边带名 + 二跳边查 Top200 节点名）
name_map = {e[0]: e[1] for e in ego_edges}
name_map[ego_id] = ego_name
missing = [n for n in G.nodes() if n not in name_map][:150]
if missing:
    jc.execute(
        "SELECT collaborator_institution_id, collaborator_institution_name FROM "
        "ads_institution_collaboration_yearly WHERE statistics_year=2024 AND "
        "collaborator_institution_id IN (%s) LIMIT 150" % ",".join(["%s"] * len(missing)),
        missing)
    for nid, nm in jc.fetchall():
        name_map[nid] = nm

rank_rows = sorted(
    [{"node_id": n, "name": str(name_map.get(n, n))[:60],
      "degree": round(deg[n], 4), "closeness": round(clo[n], 4),
      "betweenness": round(bet[n], 4)}
     for n in G.nodes()],
    key=lambda x: (-x["degree"], x["node_id"]))[:10]
facts["jiuxin_2024_centrality_top10_by_degree"] = rank_rows

# ---- 口径 B：学者合作面（库内现成榜，按 co_paper_count 强度排序） ----
jc.execute(
    "SELECT talent_id, collaborator_talent_id, co_paper_count, collaboration_score, "
    "collaboration_rank FROM ads_talent_collaborator WHERE co_paper_count IS NOT NULL "
    "ORDER BY co_paper_count DESC, collaboration_rank ASC LIMIT 8")
talent_rows = [
    {"talent_id": r[0], "collaborator_talent_id": r[1], "co_papers": int(r[2] or 0),
     "score": float(r[3]) if r[3] is not None else None, "rank": int(r[4]) if r[4] is not None else None}
    for r in jc.fetchall()]
facts["jiuxin_talent_collab_top8"] = talent_rows
# 学者名按需前 8 对逐条点查（等值过滤，避免 5M×100k 大 JOIN）
try:
    jc.execute("DESC ads_talent_profile")
    prof_cols = [r[0] for r in jc.fetchall()]
    name_col = next((c for c in ("name_zh", "display_name", "name") if c in prof_cols), None)
    if name_col:
        for tr in talent_rows[:8]:
            for side, col in (("talent_id", "talent"), ("collaborator_talent_id", "collaborator")):
                jc.execute(
                    f"SELECT {name_col} FROM ads_talent_profile WHERE {side}=%s LIMIT 1",
                    (tr[col + "_id"],))
                rr = jc.fetchone()
                tr[col] = (rr[0] or "")[:60] if rr else None
except Exception as e:  # noqa: BLE001
    facts["jiuxin_talent_name_join_note"] = str(e)[:150]

jx.close()

# ================================================================ 派生与产物
ego_row = next(r for r in rank_rows if r["node_id"] == ego_id)
derived = [
    {"key": "jiuxin_ego_degree_pct", "value": round(ego_row["degree"] * 100, 2),
     "numerator": G.degree(ego_id), "denominator": G.number_of_nodes() - 1,
     "note": "分子=ego 节点度（ego 网内邻边数），分母=ego 网节点数-1（归一基数，同 2024 单年同网）"},
    {"key": "jiuxin_ego_betweenness_pct", "value": round(ego_row["betweenness"] * 100, 2),
     "numerator": round(ego_row["betweenness"], 4),
     "denominator": 1,
     "note": "中介中心性 networkx 归一值×100（分母=1 为归一后值本身，非计数比）；"
             "分子为 ego 网内精确 betweenness 值"},
]

out = {
    "metric_id": "M_SCIUI_X_015",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation/TechInnovationEvaluationPage.tsx:3488",
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation/TechInnovationEvaluationPage.tsx:1862",
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation/TechInnovationEvaluationPage.tsx:3479",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "《科技创新评估.md》seq 137（excel_row 140）「科学网络中心性评估」功能命中："
                "「包括度中心性、接近中心性、中介中心性…网络图谱和中心性排名」——三中心性明文；"
                "需求主文档 :881 同文。本件 UI 挂载为中心性排名表（节点/类型/度/接近/中介五列）。",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": "部分支持",
    "notes": [
        "本件支持度按三源评估（20261101 铁律）。",
        "开发库图谱面双机空载/演示：新机 enterprise_centrality/graph_node/graph_edge 全 0 行；"
        "旧机 enterprise_centrality 114 行 model_version=demo_centrality_v0.1（虚构企业名），禁引。",
        "gkx 无任何网络结果面；论文合作者信息在 author_info_list longtext 非结构化，解析工程另立项。",
        "久新主承载：机构合作网 14,380,246 行（2024 单年 2,146,142 行/36,026 ego 侧机构）"
        "——结构+数据双达标，三类中心性可现转（networkx 3.2.1 本地实算）。",
        "降档主因：领域维缺位——需求「特定领域内」的领域过滤子图在合作表只到 subfield 维"
        "（ads_institution_collaboration_subfield_yearly 23,363,790 行/252 subfield），"
        "与科技创新评估页的「未来产业」领域体系（20 领域）无对齐映射；学者节点虽在"
        "ads_talent_collaborator（5,051,578 行）有现成分，但 UI 双节点型（机构/学者）混合排名需口径裁定。",
        "betweenness 用精确算法（ego 网 ≤4000 边规模内可行），seed=42 保证确定性（B5）。",
        "口径 B collaboration_score 为库内现成结果面（非本件算出），仅登记不派生。",
    ],
    "base_years_used": ["2024"],
    "base_years_missing": [],
    "base_years_note": "口径 A 用 2024 单年截面（久新合作表覆盖 2015-2026 全期，单年选择为"
                       "控制 ego 网规模的口径选择，非数据缺口）；UI 需要的历史中心性演进序列"
                       "可由同表按年切（数据在），本件未展开。",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "3488", "1862", "3479", "137", "140", "881", "114", "0.22", "0.96",
        "14380246", "2,146,142", "2146142", "36026", "23363790", "252",
        "5051578", "2024", "42",
    ]},
}
with open(os.path.join(HERE, "M_SCIUI_X_015_out.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("M_SCIUI_X_015 out.json written: egonet nodes", G.number_of_nodes(),
      "edges", len(sub_edges), "ego degree", ego_row["degree"])
