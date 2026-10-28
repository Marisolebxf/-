#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TECH PATH 三件（CENTRALITY / KEYNODE / PRIORITY）共用取数层 —— 纯本地、零 SQL。

为什么单独存在：三件共用同一张技术点图，若各自建图会出现「节点数、边数、阈值」
三处不一致，跨文档对账时无法逐节点核对。本模块只做四件事：建图、连通块、
五维中心性、统计工具；不含任何数据库连接，也不读写 out.json。

图口径（单一，深圳）：
  节点 = 深圳 IPC4 主分类前 4 位，2024 年 ≥100 件（238 个，与 M_TECH_HEAT_INDEX /
         M_TECH_LIFE_STAGE 同一域宇宙）；
  边   = 同一深圳申请人名下的两个 IPC4，共现申请人户数 co ≥ 20 且 Jaccard ≥ 0.05；
  边权 = co（共现申请人户数）；
  口径与 code/M_TECH_GRAPH_STRUCT.py 的边规则一致（那边节点宇宙是全国前 200）。

输入（只读授权缓存，均已在 _snapshots21 / _snapshots_gkx21 落盘）：
  patent_scan_20261021.pkl               深圳×年×IPC4 去重 pn 集合（件数、节点筛选）
  patent_ipc4_by_name_20261021.json      IPC4×申请人 件数（共现投影）
  _snapshots_gkx21/sz_patent_city_name_gkx.json  深圳申请人名单（77,846）
"""
from __future__ import annotations

import collections
import itertools
import json
import pickle
import statistics
from pathlib import Path

CODE = Path(__file__).resolve().parent
SNAP = CODE / "_snapshots21"
SNAPG = CODE / "_snapshots_gkx21"

YEARS = [2021, 2022, 2023, 2024]
GUARD_2024 = 100
CO_MIN = 20
JAC_MIN = 0.05

SOURCE = ("gkx @ 183.240.141.251:3318（只读账号 gkx_reader_zp）：dwd_patent 按 dwd_id 分页"
          "流式扫描，2026-10-21 21:30—2026-10-22 08:32 产出；本模块零 SQL")


def load_sz_cells():
    with open(SNAP / "patent_scan_20261021.pkl", "rb") as f:
        raw = pickle.load(f)
    cell = collections.Counter()
    for (city, y, ipc), pns in raw["ipc_pn"].items():
        if city != "深圳" or int(y) not in YEARS:
            continue
        cell[(ipc, int(y))] = len(pns)
    return cell


def load_sz_applicants():
    with open(SNAPG / "sz_patent_city_name_gkx.json", encoding="utf-8") as f:
        d = json.load(f)
    return {g["nm"] for g in d["groups"] if g.get("city") == "深圳市" and g.get("nm")}


def load_ipc_by_name():
    with open(SNAP / "patent_ipc4_by_name_20261021.json", encoding="utf-8") as f:
        return json.load(f)


def node_universe():
    """238 个深圳 IPC4（2024 年 ≥100 件），附窗口件数与逐年序列。"""
    cell = load_sz_cells()
    n2024 = {ipc: n for (ipc, y), n in cell.items() if y == 2024}
    nodes = sorted([ipc for ipc, n in n2024.items() if n >= GUARD_2024])
    seq = {ipc: [cell.get((ipc, y), 0) for y in YEARS] for ipc in nodes}
    return nodes, seq, cell


def build(nodes=None, co_min=CO_MIN, jac_min=JAC_MIN):
    """同申请人共现投影 → 图。返回 nodes / edges / adj / co / deg_app / wdeg。"""
    if nodes is None:
        nodes, _, _ = node_universe()
    nodeset = set(nodes)
    sznames = load_sz_applicants()
    by_name = collections.defaultdict(set)
    for ipc, nm, _c in load_ipc_by_name():
        if nm in sznames and ipc in nodeset:
            by_name[nm].add(ipc)

    deg_app = collections.Counter()
    co = collections.Counter()
    for nm, ds in by_name.items():
        ds = sorted(ds)
        for a in ds:
            deg_app[a] += 1
        for a, b in itertools.combinations(ds, 2):
            co[(a, b)] += 1

    edges = {}
    for k, v in co.items():
        j = v / (deg_app[k[0]] + deg_app[k[1]] - v)
        if v >= co_min and j >= jac_min:
            edges[k] = {"co": v, "jaccard": round(j, 4)}

    adj = {x: {} for x in nodes}
    for (a, b), w in edges.items():
        adj[a][b] = w["co"]
        adj[b][a] = w["co"]
    wdeg = {x: sum(adj[x].values()) for x in nodes}
    return {
        "nodes": nodes, "edges": edges, "adj": adj, "co": co,
        "deg_app": deg_app, "wdeg": wdeg,
        "n_applicants_with_graph_ipc": len(by_name),
        "params": {"co_min": co_min, "jac_min": jac_min, "guard_2024": GUARD_2024,
                   "years": list(YEARS)},
    }


def components(nodes, adj):
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
    return comps


def betweenness(nodes, adj):
    """Brandes 全源精确，归一化 1/((n-1)(n-2))。"""
    bc = {v: 0.0 for v in nodes}
    for s in nodes:
        S, P, sig, D = [], {v: [] for v in nodes}, {v: 0.0 for v in nodes}, {s: 0}
        sig[s] = 1.0
        Q = collections.deque([s])
        while Q:
            v = Q.popleft()
            S.append(v)
            for w in adj[v]:
                if w not in D:
                    D[w] = D[v] + 1
                    Q.append(w)
                if D[w] == D[v] + 1:
                    sig[w] += sig[v]
                    P[w].append(v)
        delta = {v: 0.0 for v in nodes}
        while S:
            w = S.pop()
            for v in P[w]:
                if sig[w]:
                    delta[v] += sig[v] / sig[w] * (1 + delta[w])
            if w != s:
                bc[w] += delta[w]
    n = len(nodes)
    denom = (n - 1) * (n - 2) if n > 2 else 1
    return {k: v / denom for k, v in bc.items()}


def harmonic(nodes, adj):
    n = len(nodes)
    out = {}
    for s in nodes:
        D = {s: 0}
        Q = collections.deque([s])
        while Q:
            v = Q.popleft()
            for w in adj[v]:
                if w not in D:
                    D[w] = D[v] + 1
                    Q.append(w)
        out[s] = sum(1.0 / d for u, d in D.items() if u != s) / (n - 1) if n > 1 else 0.0
    return out


def pagerank(nodes, adj, damping=0.85, iters=60):
    n = len(nodes)
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


def all_centralities(g):
    nodes, adj = g["nodes"], g["adj"]
    deg = {x: len(adj[x]) for x in nodes}
    bc = betweenness(nodes, adj)
    hc = harmonic(nodes, adj)
    pr = pagerank(nodes, adj)
    return {"degree": deg, "wdegree": g["wdeg"], "betweenness": bc,
            "harmonic": hc, "pagerank": pr}


def stats(values):
    v = sorted(values)
    return {
        "n": len(v), "min": round(v[0], 6), "median": round(statistics.median(v), 6),
        "mean": round(statistics.mean(v), 6), "max": round(v[-1], 6),
        "p75": round(pct(v, 0.75), 6), "p90": round(pct(v, 0.90), 6),
        "p95": round(pct(v, 0.95), 6), "p99": round(pct(v, 0.99), 6),
    }


def pct(v, q):
    if not v:
        return 0.0
    k = min(len(v) - 1, max(0, int(round(q * (len(v) - 1)))))
    return v[k]


def spearman(xs, ys):
    def rank(a):
        order = sorted(range(len(a)), key=lambda i: a[i])
        r = [0.0] * len(a)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and a[order[j + 1]] == a[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    rx, ry = rank(xs), rank(ys)
    n = len(rx)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = sum((a - mx) ** 2 for a in rx) ** 0.5
    dy = sum((b - my) ** 2 for b in ry) ** 0.5
    return num / (dx * dy) if dx and dy else 0.0
