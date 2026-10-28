#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_SYNTH_DS_23_GRAPH_ALGO_002 最优路径发现与展示（gkx 换源版）。

需求：科技信息展示系统 §1.1.1.1.4.5.3.1.2「自动计算并可视化展示起始节点与目标节点之间的
      最优路径（如最短路径、代价最低路径）」。

两种「最优」口径同时算、同时报：
  最短路径（hop）  = 跳数最少（BFS / 无权 Dijkstra）
  代价最低（cost） = 边代价 c(u,v)=1/w(u,v)，w=两机构共同署名论文篇数
                     （合作越强代价越低）；Dijkstra 与 Bellman-Ford 互校，A*(ALT) 加速
两条路径都输出节点序列、跳数、路径总代价、沿途合作强度，供前端高亮展示。

输出：code/M_SYNTH_DS_23_GRAPH_ALGO_002_out.json
"""
from __future__ import annotations

import heapq
import json
import random
import time

import networkx as nx

import _collab_graph21 as CG
import _synth21_common as S

MID = "M_SYNTH_DS_23_GRAPH_ALGO_002"
N_PAIRS = 200
N_LANDMARKS = 6
N_BF = 15
SEED = 20261021

W = lambda u, v, d: 1.0 / d["weight"]  # noqa: E731


def astar_weighted(g, s, t, dist_l):
    """代价图上的 ALT-A*，返回 (路径, 总代价, 展开节点数)。"""
    def h(v):
        best = 0.0
        for dl in dist_l:
            dlt, dlv = dl.get(t), dl.get(v)
            if dlt is None or dlv is None:
                continue
            val = abs(dlt - dlv)
            if val > best:
                best = val
        return best

    openq = [(h(s), 0.0, s)]
    dist = {s: 0.0}
    parent = {s: None}
    closed = set()
    while openq:
        _f, gc, u = heapq.heappop(openq)
        if u in closed:
            continue
        closed.add(u)
        if u == t:
            path = []
            cur = u
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            return path[::-1], gc, len(closed)
        for v, d in g[u].items():
            ng = gc + W(u, v, d)
            if v not in dist or ng < dist[v] - 1e-12:
                dist[v] = ng
                parent[v] = u
                heapq.heappush(openq, (ng + h(v), ng, v))
    return None, None, len(closed)


def describe(g, path, weighted_cost=None):
    hops = len(path) - 1
    ws = [g[path[i]][path[i + 1]]["weight"] for i in range(hops)]
    return {
        "hops": hops,
        "path": path,
        "edge_weights": ws,
        "sum_coauthored_papers": sum(ws),
        "min_edge_weight": min(ws) if ws else None,
        "cost_1_over_w": round(sum(1.0 / w for w in ws), 4),
        "weighted_cost": None if weighted_cost is None else round(weighted_cost, 4),
    }


def main() -> None:
    t_start = time.time()
    g_full, meta = CG.build(min_papers=2)
    st_full = CG.basic_stats(g_full)
    H = CG.giant(g_full)
    nodes = sorted(H.nodes())
    rng = random.Random(SEED)

    landmarks = rng.sample(nodes, N_LANDMARKS)
    dist_l = [nx.single_source_dijkstra_path_length(H, l, weight=W) for l in landmarks]

    pairs = []
    tries = 0
    while len(pairs) < N_PAIRS and tries < 200000:
        tries += 1
        s, t = rng.choice(nodes), rng.choice(nodes)
        if s == t:
            continue
        if len(nx.shortest_path(H, s, t)) - 1 >= 3:
            pairs.append((s, t))

    rows = []
    differ = 0
    cost_gain = []
    hop_cheaper = 0
    for i, (s, t) in enumerate(pairs):
        hop_path = nx.shortest_path(H, s, t)
        w_cost, w_path = nx.single_source_dijkstra(H, s, t, weight=W)
        t0 = time.perf_counter()
        a_path, a_cost, a_explored = astar_weighted(H, s, t, dist_l)
        a_ms = round((time.perf_counter() - t0) * 1000, 3)
        r = {
            "s": s, "t": t,
            "hop_shortest": describe(H, hop_path),
            "cost_cheapest": describe(H, w_path, w_cost),
            "astar_cost": round(a_cost, 4) if a_cost is not None else None,
            "astar_ms": a_ms,
            "astar_cost_same": a_cost is not None and abs(a_cost - w_cost) < 1e-9,
            "astar_path_identical": a_path == w_path,
            "astar_explored": a_explored,
        }
        if hop_path != w_path:
            differ += 1
            gain = r["hop_shortest"]["cost_1_over_w"] - r["cost_cheapest"]["weighted_cost"]
            cost_gain.append(gain)
        if r["cost_cheapest"]["hops"] > r["hop_shortest"]["hops"]:
            hop_cheaper += 1
        if i < N_BF:
            bf_cost, _bf_path = nx.single_source_bellman_ford(H, s, t, weight=W)
            r["bellman_ford_cost"] = round(bf_cost, 4)
            r["bellman_ford_cost_same"] = abs(bf_cost - w_cost) < 1e-9
        rows.append(r)

    # 具名样例：从巨型分量里挑「论文数最多」的机构作起点，配 4 个低度端点
    by_papers = sorted(((H.nodes[n]["papers"], n) for n in H.nodes), reverse=True)
    ends = [n for n, d in sorted(H.degree, key=lambda x: (x[1], x[0])) if d == 1][:8]
    examples = []
    for _pn, s in by_papers[:3]:
        for t in ends:
            if s == t or len(examples) >= 5:
                continue
            hop_path = nx.shortest_path(H, s, t)
            w_cost, w_path = nx.single_source_dijkstra(H, s, t, weight=W)
            examples.append({
                "source": s, "target": t,
                "source_papers": H.nodes[s]["papers"], "target_papers": H.nodes[t]["papers"],
                "hop_shortest": {k: v for k, v in describe(H, hop_path).items() if k != "path"},
                "cost_cheapest": {k: v for k, v in describe(H, w_path, w_cost).items()
                                  if k != "path"},
                "same_path": hop_path == w_path,
                "hop_path": hop_path[:6] + (["…"] if len(hop_path) > 6 else []),
                "cost_path": w_path[:6] + (["…"] if len(w_path) > 6 else []),
            })
    out = {
        "metric_id": MID,
        "metric_name": "最优路径发现与展示",
        "generated_at": "2026-10-22",
        "db": "gkx（三方库 183.240.141.251:3318，只读）",
        "data_source": CG.SOURCE,
        "definitions": {
            "shortest_path": "边数最少（BFS / 无权 Dijkstra）",
            "cheapest_path": "边代价 c=1/w 之和最小，w=两机构共同署名论文篇数",
        },
        "graph": {
            "full": st_full,
            "giant": {"n_nodes": H.number_of_nodes(), "n_edges": H.number_of_edges(),
                      "share_of_full": round(H.number_of_nodes() / st_full["n_nodes"], 4)},
            "construction": meta,
        },
        "probes": {
            "papers": meta["papers_used"],
            "sample_pairs": len(pairs),
            "pair_sampling": "巨型分量内随机取样、跳数≥3，固定种子 20261021",
            "sampling_tries": tries,
            "landmarks": N_LANDMARKS,
            "bellman_ford_pairs": sum(1 for r in rows if "bellman_ford_cost" in r),
        },
        "compute": {
            "n_pairs": len(rows),
            "cheapest_differs_from_shortest": differ,
            "cheapest_differs_share": round(differ / len(rows), 4),
            "cheapest_hop_longer": hop_cheaper,
            "mean_cost_gain": round(sum(cost_gain) / len(cost_gain), 4) if cost_gain else 0,
            "max_cost_gain": round(max(cost_gain), 4) if cost_gain else None,
            "astar_cost_matches": sum(1 for r in rows if r["astar_cost_same"]),
            "astar_path_identical": sum(1 for r in rows if r["astar_path_identical"]),
            "bellman_ford_cost_matches": sum(1 for r in rows if r.get("bellman_ford_cost_same")),
            "bellman_ford_pairs": sum(1 for r in rows if "bellman_ford_cost" in r),
            "astar_explored_mean": round(sum(r["astar_explored"] for r in rows) / len(rows), 1),
            "astar_explored_vs_nodes": round(
                (sum(r["astar_explored"] for r in rows) / len(rows)) / H.number_of_nodes(), 5),
            "astar_ms_mean": round(sum(r["astar_ms"] for r in rows) / len(rows), 3),
            "cost_scale": {
                "max_edge_weight": max(d["weight"] for _u, _v, d in H.edges(data=True)),
                "min_edge_cost": round(1.0 / max(d["weight"] for _u, _v, d in H.edges(data=True)), 4),
                "example_cost_gains": [
                    round(e["hop_shortest"]["cost_1_over_w"] - e["cost_cheapest"]["cost_1_over_w"], 4)
                    for e in examples],
            },
            "examples": examples,
            "pair_rows_head": rows[:6],
        },
        "support_judgment": "完全转换支持",
        "support_reason": (
            "依赖侧结构与数据量足够：在 %d 节点 / %d 边真实合著图上（巨型分量 %d 节点），"
            "加权最短路（代价=1/共著篇数）可现算，Dijkstra 与 A* 代价 %d/%d 对完全一致、"
            "路径 %d/%d 对逐节点相同，Bellman-Ford %d/%d 对一致；且 %d/%d 对的"
            "『代价最低路径』与『跳数最短路径』不同，说明双口径有实质区分，"
            "不是同一结果的两种说法。"
            % (st_full["n_nodes"], st_full["n_edges"], H.number_of_nodes(),
               sum(1 for r in rows if r["astar_cost_same"]), len(rows),
               sum(1 for r in rows if r["astar_path_identical"]), len(rows),
               sum(1 for r in rows if r.get("bellman_ford_cost_same")),
               sum(1 for r in rows if "bellman_ford_cost" in r),
               differ, len(rows))),
        "caveats": [
            "『最优』在本图中有两种口径（跳数 vs 合作强度代价），二者 %d/%d 对不同，"
            "前端须让用户显式选择。" % (differ, len(rows)),
            "代价函数 c=1/w 为本报告设定，需求未给；甲方可改为 c=1/log(1+w) 或按金额/项目数加权。",
            "超级枢纽会使大量跨域路径经由该节点，展示时应标注其为聚合节点而非单一院系。",
            "路径只证明『论文共著链存在』，不代表机构间存在实际合同、项目或资金关系。",
            "Bellman-Ford 仅在 15 对上验证（O(V·E)，全量不经济）。",
        ],
        "sources": [
            {"file": "code/_snapshots21/a25_paper_panel.json",
             "content": "100,900 篇中文论文（含 author_info_list）",
             "source": "gkx @ 183.240.141.251:3318 / dwd_zh_paper"},
            {"file": "code/_snapshots21/probe_a26_20261022.json",
             "content": "中文被引 20,031 行",
             "source": "gkx @ 183.240.141.251:3318 / dwd_zh_paper_citation"},
        ],
        "elapsed_sec": None,
    }
    out.update(S.base_year_block(
        [2021, 2022, 2023, 2024], [],
        "最优路径依赖的是全语料合著图的截面结构，不做年度除法；"
        "边权为共著篇数（全语料累计），窗口 2021—2024 只用于与同族指标对齐口径。"))
    out["elapsed_sec"] = round(time.time() - t_start, 1)
    S.write_out(MID, out)
    print(json.dumps({"graph": out["graph"]["full"], "giant": out["graph"]["giant"],
                      "differ": f"{differ}/{len(rows)}",
                      "astar_cost_matches": out["compute"]["astar_cost_matches"],
                      "astar_path_identical": out["compute"]["astar_path_identical"],
                      "bf": f"{out['compute']['bellman_ford_cost_matches']}/{N_BF}",
                      "mean_cost_gain": out["compute"]["mean_cost_gain"]},
                     ensure_ascii=False, indent=1))
    print("elapsed", out["elapsed_sec"], "s")


if __name__ == "__main__":
    main()
