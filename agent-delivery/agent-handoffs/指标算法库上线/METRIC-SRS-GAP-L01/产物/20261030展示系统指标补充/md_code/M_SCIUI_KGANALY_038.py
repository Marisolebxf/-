#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_038 图谱平均路径长度 — 采样框 BFS 实算 + 判档产物
UI 语义（mockData.js:404）：avg_path: '3.2 hops' mock。
久真图采样框（5,000 节点/38,383 边诱导子图）上 500 源节点 BFS 全对采样估计平均路径长度。
"""
import json
import os

import _s306_graph_base as gb

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_KGANALY_038_out.json")

facts = {}
facts["ui_mount"] = "pages/tech-knowledge-graph/mockData.js:404（avg_path: '3.2 hops' mock）"
facts["ui_semantics"] = "图谱全局平均最短路径长度（SRS row_01=501：新能源技术形成3个主要集群＞平均路径长度）"
facts["ui_demo_fallback"] = "3.2 hops 为前端 mock 常数（演示层）"
facts["srs_anchor"] = "小世界性读数——六度分隔/小世界网络家族指标"
facts["cat"] = "无业务逻辑数值类"

c = gb.load_cache()
nodes = [r[0] for r in c["node_rows"]]
names = {r[0]: r[1] for r in c["node_rows"]}
edges_main = [tuple(e) for e in c["main_edges"]]

facts["jiuxin_nodes_total"] = c["nodes_total"]
facts["jiuxin_edges_total"] = c["edges_total"]
facts["frame_nodes"] = len(nodes)
facts["frame_edges"] = len(edges_main)

# 连通域分解（披露估计域：最大连通域内路径才有定义）
adj = gb.adjacency(edges_main)
comp = gb.connected_components(adj, nodes)
comp_sizes = [len(s) for s in comp]
facts["connected_components"] = len(comp)
facts["largest_cc_size"] = comp_sizes[0]
facts["top5_cc_sizes"] = sorted(comp_sizes, reverse=True)[:5]

# 500 源 BFS 采样估计（确定性：sorted 节点等距抽样）
lcc = comp[0]
lcc_sorted = sorted(lcc)
step = max(1, len(lcc_sorted) // 500)
sources = lcc_sorted[::step][:500]
total_hops = 0
pair_count = 0
ecc_max = 0
for s in sources:
    dist = gb.bfs_dist(adj, s)
    hops = [d for d in dist.values() if d > 0]
    total_hops += sum(hops)
    pair_count += len(hops)
    if hops:
        ecc_max = max(ecc_max, max(hops))

avg_path = total_hops / pair_count if pair_count else None

derived = [{
    "source": "jiuxin 采样框（5,000 节点/38,383 诱导边）最大连通域 500 源 BFS 全对采样",
    "method": "等距确定性抽 500 源 × BFS 单源最短路 → 可达对均值（NetworkX average_shortest_path_length 采样估计式）",
    "largest_cc": {"nodes": comp_sizes[0], "share_of_frame": round(comp_sizes[0] / len(nodes), 4)},
    "components_total": len(comp),
    "top5_cc_sizes": sorted(comp_sizes, reverse=True)[:5],
    "sources_sampled": len(sources),
    "reachable_pairs": pair_count,
    "avg_path_length_hops": round(avg_path, 4) if avg_path else None,
    "max_eccentricity_observed": ecc_max,
    "ui_mock_reference": "3.2 hops（mock）——本件实算对照见 2.5",
}]

absence_probe = [
    {"what": "久新现成路径长度结果列", "how": "节点表 26 列全扫（path/distance/hop）", "hits": "0（需图算法实算）"},
    {"what": "gkx 路径承载", "how": "280 表词族扫描", "hits": "0"},
    {"what": "dev 路径面", "how": "族级快照", "hits": "0 行"},
    {"what": "UI avg_path 来源", "how": "mockData.js 读码", "hits": "3.2 hops mock 常数"},
]

out = {"metric_id": "M_SCIUI_KGANALY_038", "metric_name": "图谱平均路径长度（科技知识图谱·网络统计卡）",
       "facts": facts, "derived": derived, "absence_probe": absence_probe,
       "support_judgment": "完全转换支持",
       "base_years_used": [],
       "base_years_missing": ["无年度基期维（路径长度为当日 live 截面结构量）"],
       "base_years_note": "物理口径基期=探针快照日；平均路径长度为截面图结构量，无时序基期；非「缺年按 0 摊入」"}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done ->", OUT)
dv = derived[0]
print("CC", dv["components_total"], "LCC", dv["largest_cc"], "sources", dv["sources_sampled"])
print("pairs", dv["reachable_pairs"], "avg_path", dv["avg_path_length_hops"], "max_ecc", dv["max_eccentricity_observed"])
