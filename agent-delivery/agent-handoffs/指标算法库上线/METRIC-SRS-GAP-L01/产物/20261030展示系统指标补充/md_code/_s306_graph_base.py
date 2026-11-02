#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S3-06 L2 批共享图底座：久新技术图确定性采样框 + 度数/年度趋势/类型分组/BFS 工具。

一次拉图缓存（_snapshots/_s306_graph_cache.json.gz），供 12 件（025-030/033-038）复用：
  - jiuxin nodes: ads_technology_graph_node ORDER BY technology_node_id LIMIT 5000（确定性框，B5）
  - jiuxin edges: 框内诱导子图边（ads_technology_graph_edge）
  - evolution 边（同框）: ads_technology_evolution_edge 带 first_evidence_year（时间维）
  - gkx 备选: dwd_scholar_coauthor ORDER BY dwd_id LIMIT 20000（is_deleted=0）
三源只读；零 demo_*；重试纪律：连接失败 15s 重试一次，两次即停。
"""
import gzip
import json
import os
import pymysql
import time

BASE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(BASE, "_snapshots", "_s306_graph_cache.json.gz")

JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev", charset="utf8mb4",
          connect_timeout=10, read_timeout=600)


def jx_connect(tries=2):
    last = None
    for i in range(tries):
        try:
            return pymysql.connect(**JX)
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(15)
    raise SystemExit("jiuxin unreachable: %r" % (last,))


def build_cache():
    jx = jx_connect()
    jc = jx.cursor()
    # 节点框：确定性前 5000
    jc.execute("""SELECT technology_node_id, technology_name_original, technology_name_zh, technology_name_en,
                         current_development_phase, chain_role, community_role, community_id,
                         weighted_degree, first_publication_year, latest_publication_year
                  FROM ads_technology_graph_node
                  ORDER BY technology_node_id LIMIT 5000""")
    node_rows = jc.fetchall()
    node_ids = [r[0] for r in node_rows]
    idset = set(node_ids)
    # 诱导子图边（主图表）
    # 诱导子图边（主图表）：子查询框写法与 KGANALY_001 同构（其已验证可跑）
    jc.execute("""SELECT source_technology_node_id, target_technology_node_id
                  FROM ads_technology_graph_edge
                  WHERE source_technology_node_id IN (SELECT technology_node_id FROM
                      (SELECT technology_node_id FROM ads_technology_graph_node
                       ORDER BY technology_node_id LIMIT 5000) t)
                    AND target_technology_node_id IN (SELECT technology_node_id FROM
                      (SELECT technology_node_id FROM ads_technology_graph_node
                       ORDER BY technology_node_id LIMIT 5000) t2)""")
    main_edges = [(r[0], r[1]) for r in jc.fetchall()]
    # 演化边（带年份，时间维）：同框写法
    jc.execute("""SELECT source_technology_node_id, target_technology_node_id, first_evidence_year, is_path_eligible
                  FROM ads_technology_evolution_edge
                  WHERE source_technology_node_id IN (SELECT technology_node_id FROM
                      (SELECT technology_node_id FROM ads_technology_graph_node
                       ORDER BY technology_node_id LIMIT 5000) t)
                    AND target_technology_node_id IN (SELECT technology_node_id FROM
                      (SELECT technology_node_id FROM ads_technology_graph_node
                       ORDER BY technology_node_id LIMIT 5000) t2)""")
    evo_rows = [(r[0], r[1], r[2], r[3]) for r in jc.fetchall()]
    # 全图计数与时间维（当日 live）
    jc.execute("SELECT COUNT(*) FROM ads_technology_graph_node")
    nodes_total = jc.fetchone()[0]
    jc.execute("SELECT COUNT(*) FROM ads_technology_graph_edge")
    edges_total = jc.fetchone()[0]
    jx.close()

    import sys
    sys.path.insert(0, BASE)
    from _gkxdb import gkx  # noqa: E402
    gc = gkx()
    gc.execute("""SELECT scholar_id, co_scholar_id FROM gkx.dwd_scholar_coauthor
                  WHERE is_deleted=0 ORDER BY dwd_id LIMIT 20000""")
    gkx_edges = [(r[0], r[1]) for r in gc.fetchall()]

    cache = {
        "node_rows": node_rows, "main_edges": main_edges, "evo_rows": evo_rows,
        "nodes_total": nodes_total, "edges_total": edges_total, "gkx_edges": gkx_edges,
    }
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    with gzip.open(CACHE, "w") as fh:
        fh.write(json.dumps(cache, ensure_ascii=False).encode("utf-8"))
    return cache


def load_cache():
    if os.path.exists(CACHE):
        with gzip.open(CACHE, "r") as fh:
            return json.loads(fh.read().decode("utf-8"))
    return build_cache()


# ---------------- 图工具（全部确定性：sorted 迭代，B5） ----------------

def degree_map(nodes, edges):
    """无向度数（主值）；返回 {node: degree}。"""
    deg = {n: 0 for n in nodes}
    for u, v in edges:
        deg[u] = deg.get(u, 0) + 1
        deg[v] = deg.get(v, 0) + 1
    return deg


def adjacency(edges):
    adj = {}
    for u, v in edges:
        adj.setdefault(u, set()).add(v)
        adj.setdefault(v, set()).add(u)
    return adj


def bfs_dist(adj, start):
    from collections import deque
    dist = {start: 0}
    q = deque([start])
    while q:
        u = q.popleft()
        for v in sorted(adj.get(u, ())):
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def sample_avg_path_length(adj, nodes, k=500, seed_text="node_id-prefix"):
    """确定性前 k 节点 BFS 采样平均路径长度（UI 单位=跳）。

    seed_text 记录采样方式（非随机，前缀确定性框），B5。
    返回 dict(k, pairs, total_dist, avg, reachable_pairs, unreachable_pairs)
    """
    sources = sorted(nodes)[:k]
    total = 0
    pairs = 0
    reach_pairs = 0
    unreach = 0
    n = len(nodes)
    for s in sources:
        d = bfs_dist(adj, s)
        for t in nodes:
            if t == s:
                continue
            pairs += 1
            if t in d:
                total += d[t]
                reach_pairs += 1
            else:
                unreach += 1
    avg = (total / reach_pairs) if reach_pairs else None
    return {"k": len(sources), "n": n, "pairs": pairs, "total_dist": total,
            "avg_path_length": round(avg, 4) if avg is not None else None,
            "reachable_pairs": reach_pairs, "unreachable_pairs": unreach,
            "sampling": seed_text}


def connected_components(adj, nodes):
    seen = set()
    comps = []
    for n in sorted(nodes):
        if n in seen:
            continue
        comp = []
        q = [n]
        seen.add(n)
        while q:
            u = q.pop()
            comp.append(u)
            for v in sorted(adj.get(u, ())):
                if v not in seen:
                    seen.add(v)
                    q.append(v)
        comps.append(sorted(comp))
    return sorted(comps, key=lambda c: (-len(c), c[0]))
