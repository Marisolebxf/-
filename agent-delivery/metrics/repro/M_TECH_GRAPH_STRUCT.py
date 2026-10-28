#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_TECH_GRAPH_STRUCT · 技术点网图结构（20261022 三方库版）

口径（单一）：
  节点 = IPC4 技术域（全期（2021—2026）件数前 200）；
  边 = 同一申请人共现，骨干阈 共现 ≥20 且 Jaccard ≥0.05；
  结构指标 = 节点/边/密度/度分布/连通分量/聚类系数/PageRank。
  本件交付「可由专利数据复算的技术域图」，不是 Nebula A 面 entity_type=technology 的
  技术点主键图；节点主键是 IPC4，不是技术点实体 ID，这一点在 §三/§四 披露。

运行：python3 code/M_TECH_GRAPH_STRUCT.py（零 SQL）
"""
from __future__ import annotations

import collections
import itertools
import json
import math
import sys

sys.path.insert(0, ".")
import _tech21_scope as S  # noqa: E402

MID = "M_TECH_GRAPH_STRUCT"
TOP_N = 200
MIN_CO = 20
MIN_JACCARD = 0.05


def pagerank(nodes, adj, damping=0.85, iters=60):
    n = len(nodes)
    if not n:
        return {}
    pr = {x: 1.0 / n for x in nodes}
    for _ in range(iters):
        new = {x: (1 - damping) / n for x in nodes}
        for x in nodes:
            w = sum(adj[x].values())
            if not w:
                continue
            share = damping * pr[x] / w
            for y, wt in adj[x].items():
                new[y] += share * wt
        pr = new
    s = sum(pr.values()) or 1.0
    return {k: v / s for k, v in pr.items()}


def main():
    panel = json.load(open(S.SNAP / "patent_panel_innov_20261021.json", encoding="utf-8"))
    top = sorted(panel["ipc_all"].items(), key=lambda kv: -kv[1])[:TOP_N]
    topset = {k for k, _ in top}
    size = {k: v for k, v in top}

    by_name = collections.defaultdict(set)
    deg = collections.Counter()
    for ipc, nm, n in S.load_ipc_name():
        if ipc in topset:
            by_name[nm].add(ipc)
            deg[ipc] += 1

    co = collections.Counter()
    for ds in by_name.values():
        if len(ds) < 2:
            continue
        for a, b in itertools.combinations(sorted(ds), 2):
            co[(a, b)] += 1

    edges = {}
    for (a, b), c in co.items():
        j = c / (deg[a] + deg[b] - c)
        if c >= MIN_CO and j >= MIN_JACCARD:
            edges[(a, b)] = {"co": c, "jaccard": round(j, 4)}

    nodes = sorted(topset)
    adj = {x: {} for x in nodes}
    for (a, b), w in edges.items():
        adj[a][b] = w["co"]
        adj[b][a] = w["co"]

    E = len(edges)
    N = len(nodes)
    density = 2 * E / (N * (N - 1)) if N > 1 else 0.0
    degrees = {x: len(adj[x]) for x in nodes}
    isolated = [x for x in nodes if degrees[x] == 0]

    # 连通分量
    seen, comps = set(), []
    for x in nodes:
        if x in seen:
            continue
        stack, comp = [x], []
        seen.add(x)
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        comps.append(comp)
    comps.sort(key=len, reverse=True)

    # 聚类系数（无向简单图）
    tri = {}
    for x in nodes:
        nb = list(adj[x])
        if len(nb) < 2:
            tri[x] = 0.0
            continue
        links = sum(1 for a, b in itertools.combinations(nb, 2)
                    if (a, b) in edges or (b, a) in edges)
        tri[x] = 2 * links / (len(nb) * (len(nb) - 1))
    avg_cc = sum(tri.values()) / N if N else 0.0

    pr = pagerank(nodes, adj)
    top_deg = sorted(nodes, key=lambda x: -degrees[x])[:15]
    top_pr = sorted(nodes, key=lambda x: -pr[x])[:15]

    # 度分布分桶
    bins = collections.Counter()
    for d in degrees.values():
        if d == 0:
            bins["0"] += 1
        elif d <= 10:
            bins["1-10"] += 1
        elif d <= 30:
            bins["11-30"] += 1
        elif d <= 60:
            bins["31-60"] += 1
        elif d <= 100:
            bins["61-100"] += 1
        else:
            bins["101+"] += 1

    sections = collections.Counter()
    sec_edges = collections.Counter()
    for x in nodes:
        sections[x[0]] += 1
    for (a, b) in edges:
        sec_edges["-".join(sorted([a[0], b[0]]))] += 1

    chain = json.load(open(S.SNAP / "chain_tree_20261021.json", encoding="utf-8"))

    payload = {
        "metric_id": MID,
        "metric_name": "技术点网图结构",
        "caliber": {
            "节点": f"IPC4 技术域，全期（2021—2026）件数前 {TOP_N}",
            "边": f"同一申请人共现，co≥{MIN_CO} 且 Jaccard≥{MIN_JACCARD}",
            "节点主键": "IPC4（技术域代码），不是 Nebula 技术点实体 ID",
            "图类型": "无向加权简单图；权重=共现申请人数",
            "口径声明": "本件是「专利数据可复算的技术域图」，不是 Nebula A 面快照",
        },
        "base_years_used": [],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": "节点筛选用 2024 单年截面；2021—2024 在库，2017—2020 零行。",
        "graph": {
            "nodes": N,
            "edges": E,
            "density": round(density, 6),
            "avg_degree": round(2 * E / N, 4) if N else 0.0,
            "max_degree": max(degrees.values()) if degrees else 0,
            "isolated_nodes": len(isolated),
            "components": len(comps),
            "largest_component": len(comps[0]) if comps else 0,
            "largest_component_share": round(len(comps[0]) / N, 4) if comps and N else 0.0,
            "avg_clustering": round(avg_cc, 4),
            "weight_total": int(sum(w["co"] for w in edges.values())),
            "weight_max": max((w["co"] for w in edges.values()), default=0),
        },
        "raw_graph": {
            "pairs": len(co),
            "density_if_all": round(2 * len(co) / (N * (N - 1)), 6) if N > 1 else 0.0,
            "note": "不设阈值时 200 节点几乎两两相连，密度接近 1，无法解释结构；必须稀疏化",
        },
        "degree_bins": dict(bins),
        "components_detail": [{"size": len(c), "ipc4": sorted(c)[:12]} for c in comps[:10]],
        "top_degree": [{"ipc4": x, "degree": degrees[x], "n_patents_2024": size[x],
                        "betweenness_proxy": round(degrees[x] / max(1, N - 1), 4)} for x in top_deg],
        "top_pagerank": [{"ipc4": x, "pagerank": round(pr[x], 6), "degree": degrees[x]} for x in top_pr],
        "top_clustering": [{"ipc4": x, "clustering": round(tri[x], 4), "degree": degrees[x]}
                           for x in sorted(nodes, key=lambda z: -tri[z])[:10]],
        "sections": dict(sections),
        "section_edges": dict(sec_edges),
        "chain_tree_compare": {
            "chain_nodes": len(chain),
            "chain_edges": len(chain) - 1,
            "chain_note": "链树是 1,273 节点的树（边=节点-1），与本图的域共现图不是同一对象，只作规模对照",
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "criteria": {
                "节点/边/密度": "可算（IPC4 域图）",
                "度分布/中心性": "可算（度 + PageRank）",
                "连通分量/聚类": "可算",
                "Nebula 技术点主键图": "缺（无 entity_type=technology 快照）",
                "图层级/类型配色/布局": "缺（图壳属性不在本库）",
            },
            "note": "结构指标可在 IPC4 代理图上完整复算；但节点不是技术点实体、无图壳属性，判部分支持",
        },
    }
    S.write_out(MID, payload)

    print(json.dumps(payload["graph"], ensure_ascii=False, indent=1))
    print("raw", payload["raw_graph"])
    print("bins", dict(bins))
    print("top degree", [(x["ipc4"], x["degree"]) for x in payload["top_degree"][:8]])
    print("top pr", [(x["ipc4"], x["pagerank"]) for x in payload["top_pagerank"][:8]])
    print("components", len(comps), [len(c) for c in comps[:8]])


if __name__ == "__main__":
    main()
