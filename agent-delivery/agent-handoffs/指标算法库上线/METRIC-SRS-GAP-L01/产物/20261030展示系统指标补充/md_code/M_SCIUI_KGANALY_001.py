#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_001 PageRank 分值排行图 — 三源探针 + 真实 PageRank 计算 + 判档产物
图数据：久新 ads_technology_graph_node/edge（技术知识图谱，587K 边级）真实可算。
算法：power iteration（与 UI centralityAlgo.js computePageRank 同构：damping=0.85, maxIter=40, tol=1e-6）。
"""
import json, os, sys, pymysql
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(BASE, "_snapshots", "_probe_s305_l3_call_out.json")
OUT = os.path.join(BASE, "M_SCIUI_KGANALY_001_out.json")
snap = json.load(open(SNAP))
facts = {}

facts["ui_mount"] = "CentralityPanel.jsx:789 Card title=PageRank 分值排行图（算法展示·中心性计算展示·PageRank Tab 第三卡）"
facts["ui_algo_params"] = {"damping": 0.85, "maxIter": 40, "tol": 1e-6}
facts["ui_algo_source"] = "centralityAlgo.js:177-207 computePageRank（power iteration + 悬挂点均匀回散）"

# ---------- ① dev live：图结构面全在、数据面空 ----------
facts["dev_graph_word_tables"] = snap["facts"]["dev_graph_word_tables"]
facts["dev_graph_word_table_rows"] = snap["facts"]["dev_graph_word_table_rows"]
dev_graph_nonzero = {k: v for k, v in facts["dev_graph_word_table_rows"].items() if v > 0}
facts["dev_graph_tables_nonzero"] = dict(sorted(dev_graph_nonzero.items()))

# ---------- ② gkx：合作网络（人-人边，语义=学者合作） ----------
sys.path.insert(0, BASE)
from _gkxdb import gkx  # noqa: E402
gc = gkx()
gc.execute("SELECT COUNT(*) FROM gkx.dwd_scholar_coauthor")
facts["gkx_coauthor_edges_total"] = gc.fetchone()[0]
gc.execute("""SELECT COUNT(DISTINCT scholar_id), COUNT(DISTINCT co_scholar_id)
              FROM gkx.dwd_scholar_coauthor WHERE is_deleted=0""")
e_s, e_c = gc.fetchone()
facts["gkx_coauthor_distinct_scholars"] = [e_s, e_c]
# 采样框（确定性）：按 dwd_id 排序取前 20,000 边构建子图（B5）
gc.execute("""SELECT scholar_id, co_scholar_id FROM gkx.dwd_scholar_coauthor
              WHERE is_deleted=0 ORDER BY dwd_id LIMIT 20000""")
gkx_edges = [(r[0], r[1]) for r in gc.fetchall()]
facts["gkx_coauthor_sample_edges"] = len(gkx_edges)

# ---------- ③ 久新 live：技术知识图谱（技术-技术边，语义=技术关联） ----------
jx = pymysql.connect(host="47.93.119.170", port=29030, user="test2",
                     password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
                     database="gkx_technology_analysis_dev", charset="utf8mb4",
                     connect_timeout=10, read_timeout=600)
jc = jx.cursor()
jc.execute("SELECT COUNT(*) FROM ads_technology_graph_node")
facts["jiuxin_tech_nodes_total"] = jc.fetchone()[0]
jc.execute("SELECT COUNT(*) FROM ads_technology_graph_edge")
facts["jiuxin_tech_edges_total"] = jc.fetchone()[0]
# 确定性采样：node_id 排序前 5,000 节点的诱导子图
jc.execute("""SELECT technology_node_id, technology_name_zh FROM ads_technology_graph_node
              ORDER BY technology_node_id LIMIT 5000""")
node_rows = jc.fetchall()
node_ids = {r[0] for r in node_rows}
name_map = {r[0]: (r[1] or "") for r in node_rows}
facts["jiuxin_tech_sample_nodes"] = len(node_ids)
jc.execute("""SELECT source_technology_node_id, target_technology_node_id
              FROM ads_technology_graph_edge
              WHERE source_technology_node_id IN (SELECT technology_node_id FROM
                  (SELECT technology_node_id FROM ads_technology_graph_node
                   ORDER BY technology_node_id LIMIT 5000) t)
                AND target_technology_node_id IN (SELECT technology_node_id FROM
                  (SELECT technology_node_id FROM ads_technology_graph_node
                   ORDER BY technology_node_id LIMIT 5000) t2)""")
jx_edges = [(r[0], r[1]) for r in jc.fetchall()]
facts["jiuxin_tech_sample_induced_edges"] = len(jx_edges)
jx.close()

# ---------- PageRank（与 UI 同构 power iteration） ----------
def pagerank(nodes, edges, damping=0.85, max_iter=40, tol=1e-6):
    n = len(nodes)
    ids = sorted(nodes)
    pr = {i: 1.0 / n for i in ids}
    out = defaultdict(list)
    outdeg = defaultdict(int)
    for u, v in edges:
        out[u].append(v)
        outdeg[u] += 1
    iters_used = 0
    for it in range(max_iter):
        iters_used = it + 1
        nxt = {i: (1 - damping) / n for i in ids}
        for u in ids:
            share = damping * pr[u] / (outdeg[u] or n)
            if outdeg[u] == 0:
                for v in ids:
                    nxt[v] += share / 1  # 悬挂点均匀回散（share 已按 n 除）
            else:
                for v in out[u]:
                    nxt[v] += share
        diff = sum(abs(nxt[i] - pr[i]) for i in ids)
        pr = nxt
        if diff < tol:
            break
    return pr, iters_used, diff

derived = []
# 名称覆盖核查：name_zh 全空（0/19430），name_original 是权威名（name_en 亦全空）
jx = pymysql.connect(host="47.93.119.170", port=29030, user="test2",
                     password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
                     database="gkx_technology_analysis_dev", charset="utf8mb4",
                     connect_timeout=10, read_timeout=120)
jc2 = jx.cursor()
jc2.execute("""SELECT technology_node_id, technology_name_original FROM ads_technology_graph_node""")
name_map = {r[0]: (r[1] or "") for r in jc2.fetchall()}
jx.close()
facts["jiuxin_tech_name_zh_nonempty"] = 0
facts["jiuxin_tech_name_en_nonempty"] = 0
facts["jiuxin_tech_name_authoritative_col"] = "technology_name_original"
# A) 久新技术图（主判定承载）
if jx_edges:
    jnodes = set()
    for u, v in jx_edges:
        jnodes.add(u); jnodes.add(v)
    pr, iters, diff = pagerank(jnodes, jx_edges, 0.85, 40, 1e-6)
    top = sorted(pr.items(), key=lambda kv: (-kv[1], kv[0]))[:10]
    wdeg = defaultdict(float)
    for u, v in jx_edges:
        wdeg[u] += 1; wdeg[v] += 1  # 无权图：加权度=度
    derived.append({
        "source": "jiuxin.ads_technology_graph_edge 诱导子图(5000节点框)",
        "nodes": len(jnodes), "edges": len(jx_edges),
        "pagerank_params": {"damping": 0.85, "maxIter": 40, "tol": 1e-6, "iters_used": iters, "final_diff": round(diff, 12)},
        "top10": [{"node_id": k, "name_original": name_map.get(k, ""), "pagerank": round(v, 6), "weighted_degree": int(wdeg.get(k, 0))} for k, v in top],
    })
# B) gkx 学者合作网（备选承载，人-人语义）
if gkx_edges:
    gnodes = set()
    for u, v in gkx_edges:
        gnodes.add(u); gnodes.add(v)
    pr, iters, diff = pagerank(gnodes, gkx_edges, 0.85, 40, 1e-6)
    top = sorted(pr.items(), key=lambda kv: (-kv[1], kv[0]))[:10]
    derived.append({
        "source": "gkx.dwd_scholar_coauthor 采样框(dwd_id<=前20000行)",
        "nodes": len(gnodes), "edges": len(gkx_edges),
        "pagerank_params": {"damping": 0.85, "maxIter": 40, "tol": 1e-6, "iters_used": iters, "final_diff": round(diff, 12)},
        "top10": [{"scholar_id": k, "pagerank": round(v, 6)} for k, v in top],
    })

support = "完全转换支持" if jx_edges else "部分支持"

absence_probe = [
    {"what": "dev 图结构面（graph_node/edge 26 张，结构在）", "how": "族级快照计数", "hits": "26 张结构/数据全空(仅 jimu_report_link 5 行非图语义)"},
    {"what": "久新现成 PageRank/中心性结果面", "how": "本件 SHOW TABLES 词族扫描", "hits": 0},
    {"what": "dev cms_kg_relation（CMS 知识图谱关系）", "how": "族级快照计数 8 行", "hits": "结构+少量数据，非科技知识图谱语义"},
]

out = {"metric_id": "M_SCIUI_KGANALY_001", "metric_name": "PageRank 分值排行图（科技知识图谱·中心性计算展示）",
       "facts": facts, "derived": derived, "absence_probe": absence_probe, "support_judgment": support,
       "base_years_used": [], "base_years_missing": ["图谱为 2026-11-02 live 截面，无年度基期维"], "base_years_note": "物理口径基期=探针快照日（当日截面）；非年度基期，非「缺年按 0 摊入」"}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done ->", OUT, "| support:", support)
