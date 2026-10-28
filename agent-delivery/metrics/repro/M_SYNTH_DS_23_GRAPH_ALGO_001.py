#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_SYNTH_DS_23_GRAPH_ALGO_001 多种路径搜索算法支持（gkx 换源版）。

需求：科技信息展示系统 §1.1.1.1.4.5.3.1.1「内置 BFS、DFS、Dijkstra、Bellman-Ford、A* 等」。

本批在 gkx 中文论文自建的机构合著图上逐一实现六种口径，用同一批起讫对交叉校验
可达性、最短路长度与运行时间：
  BFS              无权重最短路（跳数最少）
  DFS              只保证可达，不保证最短（栈式，取首次到达路径）
  Dijkstra(无权)    跳数最短路
  Dijkstra(加权)    代价 c=1/w，w=共著篇数（合作越强代价越低）
  Bellman-Ford      无权重，20 对子样本（O(V·E)，全网 200 对不经济）
  A*(ALT 地标)      8 个地标，h(v)=max_l |d(l,t)−d(l,v)|，三角不等式保证可采纳

输出：code/M_SYNTH_DS_23_GRAPH_ALGO_001_out.json
"""
from __future__ import annotations

import heapq
import json
import random
import time

import networkx as nx

import _collab_graph21 as CG

MID = "M_SYNTH_DS_23_GRAPH_ALGO_001"
N_PAIRS = 200
N_BF_PAIRS = 20
N_LANDMARKS = 8
SEED = 20261021

W = lambda u, v, d: 1.0 / d["weight"]  # noqa: E731


def astar_alt(g, s, t, dist_l):
    """单位权 ALT-A*，返回 (路径, 展开节点数)。"""
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

    openq = [(h(s), 0, s)]
    dist = {s: 0}
    parent = {s: None}
    closed = set()
    explored = 0
    while openq:
        _f, gc, u = heapq.heappop(openq)
        if u in closed:
            continue
        closed.add(u)
        explored += 1
        if u == t:
            path = []
            cur = u
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            return path[::-1], explored
        for v in g[u]:
            ng = gc + 1
            if v not in dist or ng < dist[v]:
                dist[v] = ng
                parent[v] = u
                heapq.heappush(openq, (ng + h(v), ng, v))
    return None, explored


def dfs_path(g, s, t):
    stack = [(s, [s])]
    seen = {s}
    while stack:
        u, path = stack.pop()
        if u == t:
            return path
        for v in g[u]:
            if v not in seen:
                seen.add(v)
                stack.append((v, path + [v]))
    return None


def main() -> None:
    t_start = time.time()
    g_full, meta = CG.build(min_papers=2)
    st_full = CG.basic_stats(g_full)
    H = CG.giant(g_full)
    nodes = sorted(H.nodes())
    rng = random.Random(SEED)

    pairs = []
    tries = 0
    while len(pairs) < N_PAIRS and tries < 200000:
        tries += 1
        s, t = rng.choice(nodes), rng.choice(nodes)
        if s == t:
            continue
        d = nx.bidirectional_shortest_path(H, s, t)
        if len(d) - 1 >= 3:
            pairs.append((s, t))

    landmarks = rng.sample(nodes, N_LANDMARKS)
    dist_l = [nx.single_source_shortest_path_length(H, l) for l in landmarks]

    rows = []
    agree = 0
    dfs_excess = []
    astar_explored = []
    t_bf = 0.0
    for i, (s, t) in enumerate(pairs):
        r = {"s": s, "t": t}

        t0 = time.perf_counter()
        p_bfs = nx.shortest_path(H, s, t)
        r["bfs_hops"] = len(p_bfs) - 1
        r["bfs_ms"] = round((time.perf_counter() - t0) * 1000, 3)

        t0 = time.perf_counter()
        p_dfs = dfs_path(H, s, t)
        r["dfs_hops"] = (len(p_dfs) - 1) if p_dfs else None
        r["dfs_ms"] = round((time.perf_counter() - t0) * 1000, 3)
        if r["dfs_hops"] is not None:
            dfs_excess.append(r["dfs_hops"] - r["bfs_hops"])

        t0 = time.perf_counter()
        p_dij = nx.shortest_path(H, s, t, method="dijkstra")
        r["dijkstra_hops"] = len(p_dij) - 1
        r["dijkstra_ms"] = round((time.perf_counter() - t0) * 1000, 3)

        t0 = time.perf_counter()
        p_astar, explored = astar_alt(H, s, t, dist_l)
        r["astar_hops"] = (len(p_astar) - 1) if p_astar else None
        r["astar_ms"] = round((time.perf_counter() - t0) * 1000, 3)
        r["astar_explored"] = explored
        astar_explored.append(explored)

        t0 = time.perf_counter()
        cost_w, p_w = nx.single_source_dijkstra(H, s, t, weight=W)
        r["dijkstra_weighted_cost"] = round(cost_w, 6)
        r["dijkstra_weighted_hops"] = len(p_w) - 1
        r["dijkstra_weighted_ms"] = round((time.perf_counter() - t0) * 1000, 3)

        if i < N_BF_PAIRS:
            t0 = time.perf_counter()
            bf = nx.bellman_ford_path_length(H, s, t, weight=None)
            r["bellman_ford_hops"] = bf
            r["bellman_ford_ok"] = bf is not None
            r["bellman_ford_ms"] = round((time.perf_counter() - t0) * 1000, 3)
            t_bf += r["bellman_ford_ms"]

        if len({r["bfs_hops"], r["dijkstra_hops"], r["astar_hops"]}) == 1:
            agree += 1
        rows.append(r)

    bf_rows = [r for r in rows if "bellman_ford_hops" in r]
    ok = {
        "BFS": sum(1 for r in rows if r.get("bfs_hops") is not None),
        "DFS": sum(1 for r in rows if r.get("dfs_hops") is not None),
        "Dijkstra": sum(1 for r in rows if r.get("dijkstra_hops") is not None),
        "Dijkstra_weighted": sum(1 for r in rows if r.get("dijkstra_weighted_cost") is not None),
        "Bellman-Ford": sum(1 for r in bf_rows if r.get("bellman_ford_ok")),
        "A*": sum(1 for r in rows if r.get("astar_hops") is not None),
    }
    timing = {
        "BFS": round(sum(r["bfs_ms"] for r in rows) / len(rows), 3),
        "DFS": round(sum(r["dfs_ms"] for r in rows) / len(rows), 3),
        "Dijkstra": round(sum(r["dijkstra_ms"] for r in rows) / len(rows), 3),
        "Dijkstra_weighted": round(sum(r["dijkstra_weighted_ms"] for r in rows) / len(rows), 3),
        "A*": round(sum(r["astar_ms"] for r in rows) / len(rows), 3),
        "Bellman-Ford": round(t_bf / max(1, len(bf_rows)), 3),
    }

    # 小世界：巨型分量内随机起讫对的跳数分布（500 对）
    dists = []
    for _ in range(500):
        s, t = rng.choice(nodes), rng.choice(nodes)
        if s == t:
            continue
        dists.append(nx.shortest_path_length(H, s, t))
    dists.sort()
    distance_stats = {
        "n_sample": len(dists),
        "mean": round(sum(dists) / len(dists), 3),
        "median": dists[len(dists) // 2],
        "p90": dists[int(0.9 * (len(dists) - 1))],
        "max": dists[-1],
        "note": "巨型分量内随机起讫对的最短跳数；数值小说明经超级枢纽形成小世界",
    }

    # 具名样例：取巨型分量内度最高的 5 个枢纽与 5 个高校/院所端点配对
    hubs = [n for n, _ in sorted(H.degree, key=lambda x: (-x[1], x[0]))][:4]
    ends = [n for n, d in sorted(H.degree, key=lambda x: (x[1], x[0])) if d > 0][:4]
    examples = []
    for s in hubs:
        for t in ends[:2]:
            if s == t:
                continue
            path = nx.shortest_path(H, s, t, method="dijkstra")
            examples.append({"source": s, "target": t, "hops": len(path) - 1,
                             "path": path[:8] + (["…"] if len(path) > 8 else []),
                             "edge_weights": [H[path[i]][path[i + 1]]["weight"]
                                              for i in range(min(len(path) - 1, 7))],
                             "source_degree": H.degree(s), "target_degree": H.degree(t)})
            if len(examples) >= 5:
                break
        if len(examples) >= 5:
            break

    out = {
        "metric_id": MID,
        "metric_name": "多种路径搜索算法支持",
        "generated_at": "2026-10-22",
        "db": "gkx（三方库 183.240.141.251:3318，只读）",
        "data_source": CG.SOURCE,
        "algorithms": ["BFS", "DFS", "Dijkstra(无权)", "Dijkstra(加权 c=1/w)",
                       "Bellman-Ford", "A*(ALT 地标)"],
        "graph": {
            "full": st_full,
            "giant": {"n_nodes": H.number_of_nodes(), "n_edges": H.number_of_edges(),
                      "share_of_full": round(H.number_of_nodes() / st_full["n_nodes"], 4)},
            "construction": meta,
            "node_definition": "中文论文 author_info_list 的原始机构串，全语料 ≥2 篇",
            "edge_definition": "同一篇论文共同署名（无向），边权=共著篇数",
        },
        "probes": {
            "papers": meta["papers_used"],
            "sample_pairs": len(pairs),
            "pair_sampling": "巨型连通分量内随机取样、要求跳数≥3，固定种子 20261021",
            "sampling_tries": tries,
            "bellman_ford_pairs": len(bf_rows),
            "landmarks": N_LANDMARKS,
            "astar_heuristic": "ALT: h(v)=max_l |d(l,t)−d(l,v)|（可采纳、三角不等式）",
        },
        "compute": {
            "algorithm_success_pairs": ok,
            "hop_agreement_bfs_dijkstra_astar": agree,
            "bellman_ford_matches_bfs": sum(1 for r in bf_rows
                                            if r.get("bellman_ford_hops") == r.get("bfs_hops")),
            "dfs_hop_excess": {
                "mean": round(sum(dfs_excess) / len(dfs_excess), 3) if dfs_excess else None,
                "max": max(dfs_excess) if dfs_excess else None,
                "n": len(dfs_excess),
                "note": "DFS 只保证可达、不保证最短；超出量说明『可行路径』与『最优路径』的区别",
            },
            "avg_ms_per_query": timing,
            "astar_explored_mean": round(sum(astar_explored) / len(astar_explored), 1),
            "astar_explored_vs_nodes": round(
                (sum(astar_explored) / len(astar_explored)) / H.number_of_nodes(), 5),
            "distance_distribution": distance_stats,
            "examples": examples,
            "pair_rows_head": rows[:10],
        },
        "support_judgment": "完全转换支持",
        "support_reason": (
            "无现成「图算法服务」结果面，但依赖侧结构与数据量都够：在 %d 节点 / %d 边"
            "（巨型分量 %d 节点 / %d 边）的真实机构合著图上，六种算法全部跑通——"
            "BFS/Dijkstra/A* 各 %d/%d 对、DFS %d/%d 对、Bellman-Ford %d/%d 对，"
            "BFS/Dijkstra/A* 跳数一致 %d/%d 对，可直接作为路径搜索服务底座。"
            % (st_full["n_nodes"], st_full["n_edges"],
               H.number_of_nodes(), H.number_of_edges(),
               ok["BFS"], len(pairs), ok["DFS"], len(pairs),
               ok["Bellman-Ford"], len(bf_rows),
               agree, len(pairs))),
        "caveats": [
            "图为无向合著图，最短『跳数』不等于最强合作；加权代价口径见 M_SYNTH_DS_23_GRAPH_ALGO_002。",
            "Bellman-Ford 为 O(V·E)，仅在前 20 对上验证；全量 200 对不经济，未做。",
            "DFS 返回可行路径而非最短路，跳数普遍大于 BFS，二者用途不同，不可互相替代。",
            "A* 用 ALT 地标启发式；若启发式恒 0 则退化为 Dijkstra，本批用地标保证非退化。",
            "机构串未做上下级归并，同名不同院系是不同节点（见 §四）。",
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
    out.update(CG.S.base_year_block(
        [2021, 2022, 2023, 2024], [],
        "路径搜索的输入是全语料合著图的截面结构，不做年度除法；"
        "图中论文年份覆盖 1980—2026，但统计窗口取 2021—2024 与同族 191_1/007 对齐。"))
    out["elapsed_sec"] = round(time.time() - t_start, 1)
    CG.S.write_out(MID, out)
    print(json.dumps({"graph": out["graph"]["full"], "giant": out["graph"]["giant"],
                      "ok": ok, "agree": f"{agree}/{len(pairs)}",
                      "timing": timing, "dist": distance_stats},
                     ensure_ascii=False, indent=1))
    print("elapsed", out["elapsed_sec"], "s")


if __name__ == "__main__":
    main()
