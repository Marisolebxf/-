#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S3-06 L3 批共享图算子底座（KGANALY_039/040/042/043/044/045/046/049/050/051/052 复用，勿直接运行）
与 L2 批的 _s306_graph_base.py 相互独立（L2 已占用该名；本文件为 L3 专用 _s306_l3_base.py）。
三源纪律：dev 图表面 26 张全 0 行（复用族级快照 _probe_s305_l3_call_out.json，勿重跑）；
gkx 经 _gkxdb.py（唯一入口）；久新 live 直连（限流 1203 → 15 秒重试；失败 2 次即停登记）。
主承载：久新 ads_technology_graph_node/edge（19,430 节点/587,252 边，技术知识图谱真图）。
备承载：gkx.dwd_scholar_coauthor（1,187,606 边，人-人合作语义）。
B5 确定性：节点 sorted()；采样框 ORDER BY 主键 LIMIT 固定；LPA 标签序节点 id 升序 + 平局取字典序最小。
"""
import json, os, sys, time
import pymysql
from collections import defaultdict, deque

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(BASE, "_snapshots", "_probe_s305_l3_call_out.json")

JX_CONF = dict(host="47.93.119.170", port=29030, user="test2",
               password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
               database="gkx_technology_analysis_dev", charset="utf8mb4",
               connect_timeout=10, read_timeout=600)


def jx_connect(retries=2):
    """久新连接（限流 1203 偶发 → 15 秒重试；失败 2 次即停登记）"""
    last = None
    for i in range(retries + 1):
        try:
            return pymysql.connect(**JX_CONF)
        except Exception as e:  # noqa: BLE001
            last = e
            if i >= retries:
                raise
            time.sleep(15)


def gkx_connect():
    sys.path.insert(0, BASE)
    from _gkxdb import gkx  # noqa: E402
    return gkx()


def load_snap():
    return json.load(open(SNAP))


# ---------- 久新技术图装载（确定性采样框） ----------

def load_jiuxin_tech_frame(frame=5000):
    """主承载：node ORDER BY technology_node_id LIMIT frame 的确定性采样框 + 框内诱导子图。
    返回 dict(frame, node_ids, node_present, id_name, id_comm, edges)；边 canonical (min,max) 去重排序（B5）。"""
    jx = jx_connect()
    cur = jx.cursor()
    cur.execute("""SELECT technology_node_id, technology_name_original, community_id,
                   weighted_degree FROM ads_technology_graph_node
                   ORDER BY technology_node_id LIMIT %s""", (frame,))
    rows = cur.fetchall()
    node_ids = {r[0] for r in rows}
    id_name = {r[0]: (r[1] or "") for r in rows}
    id_comm = {r[0]: (r[2] or "") for r in rows}
    cur.execute("""SELECT source_technology_node_id, target_technology_node_id
                   FROM ads_technology_graph_edge
                   WHERE source_technology_node_id IN (SELECT technology_node_id FROM
                       (SELECT technology_node_id FROM ads_technology_graph_node
                        ORDER BY technology_node_id LIMIT %s) t)
                     AND target_technology_node_id IN (SELECT technology_node_id FROM
                       (SELECT technology_node_id FROM ads_technology_graph_node
                        ORDER BY technology_node_id LIMIT %s) t2)""", (frame, frame))
    edges = [(min(r[0], r[1]), max(r[0], r[1])) for r in cur.fetchall()]
    jx.close()
    canon_edges = sorted(set(edges))
    present = set()
    for u, v in canon_edges:
        present.add(u); present.add(v)
    return {"frame": frame, "node_ids": sorted(node_ids), "node_present": sorted(present),
            "id_name": id_name, "id_comm": id_comm, "edges": canon_edges}


# ---------- 简单无向图算子（邻接以 set 存，遍历按 sorted 键） ----------

def build_adj(nodes, edges):
    adj = {n: set() for n in nodes}
    for u, v in edges:
        if u in adj and v in adj:
            adj[u].add(v); adj[v].add(u)
    return adj


def graph_density(n_nodes, n_edges):
    """无向简单图密度 D = 2E / (N(N-1))；N<2 → 0"""
    if n_nodes < 2:
        return 0.0
    return 2.0 * n_edges / (n_nodes * (n_nodes - 1))


def average_clustering(adj, nodes):
    """平均局部聚类系数（Watts-Strogatz）+ 全局 transitivity 双口径。
    C(v)=2T(v)/(k(k-1))，k<2 不计入均值（NetworkX 惯例）；transitivity=3×三角形/两跳路径数。"""
    total_c, cnt, lowdeg = 0.0, 0, 0
    tri_angles, tri_paths = 0, 0
    for u in nodes:
        k = len(adj[u])
        if k < 2:
            lowdeg += 1
            continue
        neigh = adj[u]
        t2 = 0
        for w in sorted(neigh):
            t2 += len(adj[w] & neigh)
        t = t2 // 2
        total_c += 2.0 * t / (k * (k - 1))
        cnt += 1
        tri_angles += t
        tri_paths += k * (k - 1) // 2
    avg_c = total_c / cnt if cnt else 0.0
    transitivity = (1.0 * tri_angles / tri_paths) if tri_paths else 0.0
    return {"avg_clustering": round(avg_c, 6), "transitivity_global": round(transitivity, 6),
            "nodes_ge2deg": cnt, "nodes_lt2deg": lowdeg, "triangles": tri_angles // 3}


def bfs_all(adj, src):
    """单源 BFS（确定性：邻居访问按 sorted 序）"""
    dist = {src: 0}
    q = deque([src])
    while q:
        u = q.popleft()
        for v in sorted(adj[u]):
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def component_sizes(adj):
    """连通块（确定性：种子按 sorted 序）"""
    seen, comps = set(), []
    for n in sorted(adj):
        if n in seen:
            continue
        dist = bfs_all(adj, n)
        comp = sorted(dist.keys())
        seen.update(comp)
        comps.append(comp)
    return comps


def label_propagation(adj, nodes, max_iter=50):
    """LPA 社区发现（确定性：节点 id 升序遍历；标签计数平局取字典序最小标签）"""
    labels = {n: n for n in nodes}
    for _ in range(max_iter):
        changed = 0
        for u in nodes:
            counts = defaultdict(int)
            for v in sorted(adj[u]):
                counts[labels[v]] += 1
            if not counts:
                continue
            best = min(counts.items(), key=lambda kv: (-kv[1], str(kv[0])))[0]
            if best != labels[u]:
                labels[u] = best
                changed += 1
        if not changed:
            break
    groups = defaultdict(list)
    for n in nodes:
        groups[labels[n]].append(n)
    comms = sorted(groups.values(), key=lambda g: (-len(g), g[0]))
    return labels, comms


def community_density(adj, members):
    """社群内密度：内部实际边 / 理论最大边 C(k,2)（与 CommunityPanel communityDensity 同式）"""
    ms = set(members)
    k = len(ms)
    if k < 2:
        return 0.0
    internal = 0
    for u in sorted(ms):
        internal += sum(1 for v in adj[u] if v in ms and u < v)
    return 2.0 * internal / (k * (k - 1))


def modularity(adj, comms, m):
    """Newman 模块度 Q（无向等权）"""
    if m == 0:
        return 0.0
    q = 0.0
    for g in comms:
        gs = set(g)
        lc, kc = 0, 0
        for u in sorted(gs):
            kc += len(adj[u])
            lc += sum(1 for v in adj[u] if v in gs and u < v)
        q += lc / m - (kc / (2.0 * m)) ** 2
    return q


def pagerank(adj, nodes, damping=0.85, max_iter=40, tol=1e-6):
    """power iteration（与 UI centralityAlgo.js computePageRank 同构：悬挂点均匀回散）"""
    n = len(nodes)
    pr = {i: 1.0 / n for i in nodes}
    for it in range(max_iter):
        nxt = {i: (1 - damping) / n for i in nodes}
        dangling = sum(pr[u] for u in nodes if len(adj[u]) == 0)
        for u in nodes:
            k = len(adj[u])
            if k == 0:
                continue
            share = damping * pr[u] / k
            for v in sorted(adj[u]):
                nxt[v] += share
        for u in nodes:
            nxt[u] += damping * dangling / n
        diff = sum(abs(nxt[u] - pr[u]) for u in nodes)
        pr = nxt
        if diff < tol:
            break
    return pr, it + 1, diff


def composite_score_centrality(adj, nodes, weights=None):
    """CentralityPanel compare Tab 综合分：度/紧密/中介/PR 四维加权（UI 默认各 25%）。
    紧密=BFS 全源；中介=Brandes（无权无向）；PR=power iteration。返回五字典。"""
    w = weights or {"degree": 0.25, "closeness": 0.25, "betweenness": 0.25, "pagerank": 0.25}
    deg = {u: len(adj[u]) for u in nodes}
    close = {u: 0.0 for u in nodes}
    btw = {u: 0.0 for u in nodes}
    for s in nodes:
        dist = {s: 0}; preds = defaultdict(list); sigma = defaultdict(float); sigma[s] = 1.0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in sorted(adj[u]):
                if v not in dist:
                    dist[v] = dist[u] + 1
                    q.append(v)
                if dist[v] == dist[u] + 1:
                    sigma[v] += sigma[u]
                    preds[v].append(u)
        reach_sum = sum(d for d in dist.values() if d > 0)
        if reach_sum > 0:
            close[s] = (len(dist) - 1) / reach_sum
        delta = defaultdict(float)
        order = sorted(dist.keys(), key=lambda x: -dist[x])
        for u in order:
            if u == s:
                continue
            for p in preds[u]:
                delta[p] += sigma[p] / sigma[u] * (1.0 + delta[u])
            btw[u] += delta[u] / 2.0
    pr, iters, diff = pagerank(adj, nodes)

    def norm(dct):
        lo, hi = min(dct.values()), max(dct.values())
        return {k: (dct[k] - lo) / (hi - lo) if hi > lo else 0.0 for k in sorted(dct)}
    nd, nc, nb, np_ = norm(deg), norm(close), norm(btw), norm(pr)
    comp = {u: round(w["degree"] * nd[u] + w["closeness"] * nc[u]
                     + w["betweenness"] * nb[u] + w["pagerank"] * np_[u], 6)
            for u in nodes}
    return {"degree": deg, "closeness": {k: round(v, 6) for k, v in close.items()},
            "betweenness": {k: round(v, 6) for k, v in btw.items()},
            "pagerank": {k: round(v, 6) for k, v in pr.items()}, "composite": comp,
            "pagerank_iters": iters, "pagerank_final_diff": round(diff, 12)}


def gkx_coauthor_frame(limit=20000):
    """备承载：gkx.dwd_scholar_coauthor 按 dwd_id 升序确定性采样框（is_deleted=0）
    返回 dict(nodes, edges, edge_weights, rows)——边 canonical 去重；权重取同边最大 co_paper_count。"""
    gc = gkx_connect()
    gc.execute("""SELECT scholar_id, co_scholar_id, co_paper_count FROM gkx.dwd_scholar_coauthor
                  WHERE is_deleted=0 ORDER BY dwd_id LIMIT %s""", (limit,))
    rows = gc.fetchall()
    edges = sorted(set((min(r[0], r[1]), max(r[0], r[1])) for r in rows))
    weights = {}
    for r in rows:
        key = (min(r[0], r[1]), max(r[0], r[1]))
        weights[key] = max(weights.get(key, 0), int(r[2] or 0))
    nodes = set()
    for u, v in edges:
        nodes.add(u); nodes.add(v)
    return {"nodes": sorted(nodes), "edges": edges, "edge_weights": weights, "rows": len(rows)}


ABSENCE_PROBE_TMPL = [
    {"what": "dev 图结构面（graph_node/graph_edge/policy_graph_* 等 26 张）",
     "how": "族级快照 _probe_s305_l3_call_out.json 精确计数", "hits": "26 张全部 0 行（非零仅 jimu_report_link 5 / cms_expert_knowledge 61 / cms_kg_relation 8 / cms_kg_relation_type 7，均非图拓扑语义）"},
    {"what": "久新现成结果面（density/clustering/community/composite 结果表）",
     "how": "SHOW TABLES 词族扫描（本批共用）", "hits": "无独立结果面；node 表自带 community_id 列（社群归属现成）"},
    {"what": "gkx 图语义表", "how": "族级快照 gkx_graph_word_tables", "hits": "dwd_scholar_coauthor（合作边可作图原料）"},
]
