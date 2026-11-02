#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_039 图谱网络密度 — 三源探针 + 真图实算 + 判档产物
挂载：mockData.js:376 fusionIndicators net_density（graphValue 0.32）+ queryAssetDeepAnalysis.js:30 KPI「网络密度%」
语义：无向简单图密度 D = 2E / (N(N-1))（queryAssetDeepAnalysis.js 原式 edgeCount/(C(N,2)) 同义）。
主承载：久新技术图（全图 19,430/587,252 直查 + 5,000 框诱导子图实算）；
备承载：gkx.dwd_scholar_coauthor 20,000 边框（人-人语义）。
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _s306_l3_base import (jx_connect, load_jiuxin_tech_frame,
                           load_snap, build_adj, graph_density, gkx_coauthor_frame,
                           ABSENCE_PROBE_TMPL)

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_KGANALY_039_out.json")
facts = {}
snap = load_snap()

facts["ui_mount"] = ("mockData.js:376 fusionIndicators[0] net_density（graphValue=0.32/ruleValue=0.35/"
                     "modelValue=0.31/fusionValue=0.33，unit=ratio）+ queryAssetDeepAnalysis.js:30 KPI「网络密度 %」"
                     "（原式 density=+(edgeCount/(nodeCount*(nodeCount-1)/2)*100).toFixed(1)）")
facts["ui_algo_source"] = "queryAssetDeepAnalysis.js:24-30（D=E/C(N,2)，与标准无向密度 2E/(N(N-1)) 同义）"

# ---------- 三源探针 ----------
facts["dev_graph_word_tables"] = snap["facts"]["dev_graph_word_tables"]
facts["dev_graph_word_table_rows"] = snap["facts"]["dev_graph_word_table_rows"]
dev_nonzero = {k: v for k, v in facts["dev_graph_word_table_rows"].items() if v > 0}
facts["dev_graph_tables_nonzero"] = dict(sorted(dev_nonzero.items()))

# ---------- ① 久新主承载 ----------
jx = jx_connect()
jc = jx.cursor()
jc.execute("SELECT COUNT(*) FROM ads_technology_graph_node")
facts["jiuxin_tech_nodes_total"] = jc.fetchone()[0]
jc.execute("SELECT COUNT(*) FROM ads_technology_graph_edge")
facts["jiuxin_tech_edges_total"] = jc.fetchone()[0]
jc.execute("SELECT COUNT(DISTINCT source_technology_node_id), COUNT(DISTINCT target_technology_node_id), COUNT(DISTINCT edge_id) FROM ads_technology_graph_edge")
r = jc.fetchone()
facts["jiuxin_tech_edge_endpoints"] = {"distinct_source": r[0], "distinct_target": r[1], "distinct_edge_id": r[2]}
jx.close()

frame = load_jiuxin_tech_frame(5000)
facts["jiuxin_tech_sample_frame"] = frame["frame"]
facts["jiuxin_tech_sample_nodes"] = len(frame["node_ids"])
facts["jiuxin_tech_sample_induced_edges"] = len(frame["edges"])
adj = build_adj(frame["node_present"], frame["edges"])
present = sorted(adj.keys())

# ---------- ② gkx 备承载 ----------
gk = gkx_coauthor_frame(20000)
facts["gkx_coauthor_sample_edges"] = len(gk["edges"])
facts["gkx_coauthor_sample_nodes"] = len(gk["nodes"])
gadj = build_adj(gk["nodes"], gk["edges"])

derived = []
# 全图直查密度（分子=587,252 全边，分母=C(19430,2)）——注意全边含框外节点，本键只作量级参考
derived.append({
    "source": "jiuxin.ads_technology_graph 全图直查",
    "nodes": facts["jiuxin_tech_nodes_total"], "edges": facts["jiuxin_tech_edges_total"],
    "density_pct": round(graph_density(facts["jiuxin_tech_nodes_total"],
                                       facts["jiuxin_tech_edges_total"]) * 100, 4),
    "note": "全图口径：N=全节点数 E=全边数（含两端均入图的全部边）；量级参考——技术图密图",
})
# 采样框诱导子图密度（主实算）
derived.append({
    "source": "jiuxin.ads_technology_graph_edge 诱导子图(5000节点框)",
    "nodes": len(present), "edges": len(frame["edges"]),
    "density_pct": round(graph_density(len(present), len(frame["edges"])) * 100, 6),
    "note": "采样框口径：两端均落框内的诱导子图（B5 确定性）",
})
# gkx 备承载
derived.append({
    "source": "gkx.dwd_scholar_coauthor 采样框(dwd_id前20000行,去重后)",
    "nodes": len(gk["nodes"]), "edges": len(gk["edges"]),
    "density_pct": round(graph_density(len(gk["nodes"]), len(gk["edges"])) * 100, 6),
    "note": "人-人合作语义备选（稀疏，合作网密度天然低）",
})

support = "完全转换支持" if frame["edges"] else "部分支持"
out = {"metric_id": "M_SCIUI_KGANALY_039", "metric_name": "图谱网络密度（知识图谱·融合统计指标/查询资产深入分析）",
       "facts": facts, "derived": derived, "absence_probe": ABSENCE_PROBE_TMPL,
       "support_judgment": support,
       "base_years_used": [], "base_years_missing": ["图谱为 2026-11-02 live 截面，无年度基期维"],
       "base_years_note": "物理口径基期=探针快照日（当日截面）；非年度基期，非「缺年按 0 摊入」"}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done ->", OUT, "| support:", support,
      "| induced density%:", derived[1]["density_pct"])
