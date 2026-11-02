#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_040 图谱聚类系数 — 三源探针 + 真图实算 + 判档产物
挂载：mockData.js:390 fusionIndicators clustering（graphValue 0.68/ruleValue 0.70/modelValue 0.66/fusionValue 0.68）
语义：平均局部聚类系数（Watts-Strogatz C(v)=2T(v)/(k(v)(k(v)-1)) 的节点均值）；
并列全局聚类系数（transitivity=3×三角形/三角数）作口径对照。
主承载：久新技术图 5,000 框诱导子图（19,430/587,252 全图代价高——聚类系数 O(Σk²)，框内实算+边界披露）。
备承载：gkx.dwd_scholar_coauthor 20,000 边框。
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _s306_l3_base import (jx_connect, load_jiuxin_tech_frame, load_snap,
                           build_adj, gkx_coauthor_frame, ABSENCE_PROBE_TMPL)

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_KGANALY_040_out.json")
facts = {}
snap = load_snap()

facts["ui_mount"] = ("mockData.js:390 fusionIndicators[1] clustering（graphValue=0.68/ruleValue=0.70/"
                     "modelValue=0.66/fusionValue=0.68，weight=0.20，unit=ratio；talent 场景权重升至 0.30）")
facts["ui_algo_source"] = "融合面板未给公式（mock 常量）；语义锚=Watts-Strogatz 平均局部聚类系数（R1）"

# ---------- 三源探针 ----------
facts["dev_graph_word_table_rows"] = snap["facts"]["dev_graph_word_table_table_rows"] if "dev_graph_word_table_table_rows" in snap["facts"] else snap["facts"]["dev_graph_word_table_rows"]
dev_nonzero = {k: v for k, v in facts["dev_graph_word_table_rows"].items() if v > 0}
facts["dev_graph_tables_nonzero"] = dict(sorted(dev_nonzero.items()))

# ---------- ① 久新主承载 ----------
jx = jx_connect()
jc = jx.cursor()
jc.execute("SELECT COUNT(*) FROM ads_technology_graph_node")
facts["jiuxin_tech_nodes_total"] = jc.fetchone()[0]
jc.execute("SELECT COUNT(*) FROM ads_technology_graph_edge")
facts["jiuxin_tech_edges_total"] = jc.fetchone()[0]
jx.close()

frame = load_jiuxin_tech_frame(5000)
facts["jiuxin_tech_sample_frame"] = frame["frame"]
facts["jiuxin_tech_sample_induced_edges"] = len(frame["edges"])
adj = build_adj(frame["node_present"], frame["edges"])
present = sorted(adj.keys())
facts["jiuxin_tech_sample_present_nodes"] = len(present)

# ---------- ② gkx 备承载 ----------
gk = gkx_coauthor_frame(20000)
facts["gkx_coauthor_sample_edges"] = len(gk["edges"])
facts["gkx_coauthor_sample_nodes"] = len(gk["nodes"])
gadj = build_adj(gk["nodes"], gk["edges"])


def clustering_metrics(adj, nodes):
    """平均局部聚类系数（WS）+ 全局 transitivity + 低度节点占比披露。
    C(v) 分母 k(k-1)，k<2 节点不计入均值（NetworkX 惯例：nodes=None 时忽略 k<2）。"""
    total_c, cnt = 0.0, 0
    lowdeg = 0
    tri_angles = 0  # 三角形×3（每个三角形在 3 个顶点各贡献 1 个封闭角）
    tri_paths = 0   # 两跳路径数 = Σ k(k-1)/2
    for u in nodes:
        k = len(adj[u])
        if k < 2:
            lowdeg += 1
            continue
        neigh = adj[u]
        # T(v) = (Σ_{w∈N(v)} |N(w)∩N(v)|) / 2  —— 每条内部边计两次
        t2 = 0
        for w in sorted(neigh):
            t2 += len(adj[w] & neigh)
        t = t2 // 2
        total_c += 2.0 * t / (k * (k - 1))
        cnt += 1
        tri_angles += t          # 每个三角形在 3 顶点各计 1
        tri_paths += k * (k - 1) // 2
    avg_c = total_c / cnt if cnt else 0.0
    transitivity = (1.0 * tri_angles / tri_paths) if tri_paths else 0.0
    return {"avg_clustering": round(avg_c, 6),
            "transitivity_global": round(transitivity, 6),
            "nodes_ge2deg": cnt, "nodes_lt2deg": lowdeg,
            "triangles": tri_angles // 3}


derived = []
t0 = time.time()
jm = clustering_metrics(adj, present)
derived.append({
    "source": "jiuxin.ads_technology_graph_edge 诱导子图(5000节点框)",
    "nodes": len(present), "edges": len(frame["edges"]),
    **jm,
    "note": "主实算：WS 平均局部聚类 + transitivity 双口径并列（B10）",
})
gm = clustering_metrics(gadj, sorted(gadj.keys()))
derived.append({
    "source": "gkx.dwd_scholar_coauthor 采样框(dwd_id前20000行,去重后)",
    "nodes": len(gk["nodes"]), "edges": len(gk["edges"]),
    **gm,
    "note": "人-人合作语义备选（稀疏合作网聚类天然低）",
})

support = "完全转换支持" if frame["edges"] else "部分支持"
out = {"metric_id": "M_SCIUI_KGANALY_040", "metric_name": "图谱聚类系数（知识图谱·融合统计指标）",
       "facts": facts, "derived": derived, "absence_probe": ABSENCE_PROBE_TMPL,
       "support_judgment": support,
       "base_years_used": [], "base_years_missing": ["图谱为 2026-11-02 live 截面，无年度基期维"],
       "base_years_note": "物理口径基期=探针快照日（当日截面）；非年度基期，非「缺年按 0 摊入」"}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done ->", OUT, "| support:", support,
      "| jiuxin avg_c:", jm["avg_clustering"], "transitivity:", jm["transitivity_global"],
      "triangles:", jm["triangles"], "| gkx avg_c:", gm["avg_clustering"],
      "| calc_sec_rounds:", round(time.time() - t0, 1))
