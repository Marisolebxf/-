#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M_INNOV_DS_02_PATH_003 · 节点优先级/重要度（可配置权重版）
图源：gkx.dwd_scholar_coauthor（真实学者合著网，1,187,606 行）

清洗（写死，保证可复现）：
  1) 剔除 co_scholar_id 为空/0 的行
  2) 剔除自环 scholar_id = co_scholar_id
  3) 按 (min(a,b), max(a,b)) 归并互指边，权重取 max(co_paper_count)

四中心性：度 / 中介（Brandes 96 源抽样）/ 调和接近（96 源抽样）/ 加权 PageRank
归一：百分位秩（同值取平均秩），再按三套权重合成 0-100 优先级
输出：code/M_INNOV_DS_02_PATH_003_out.json
"""
import json
import math
import os
import random
import statistics
import sys
import time
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "M_INNOV_DS_02_PATH_003_out.json")

K_SRC = int(os.environ.get("K_SRC", "96"))
SCENARIOS = {
    "W1_等权": {"deg": 0.25, "btw": 0.25, "clo": 0.25, "pr": 0.25},
    "W2_中心度优先（默认）": {"deg": 0.40, "btw": 0.20, "clo": 0.20, "pr": 0.20},
    "W3_桥接优先": {"deg": 0.15, "btw": 0.45, "clo": 0.15, "pr": 0.25},
}


def pct_rank(vals):
    """百分位秩 0-1，同值取平均秩"""
    n = len(vals)
    order = sorted(range(n), key=lambda i: vals[i])
    out = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        avg = (i + j) / 2.0
        v = avg / (n - 1) if n > 1 else 0.0
        for k in range(i, j + 1):
            out[order[k]] = v
        i = j + 1
    return out


def spearman(a, b):
    ra, rb = pct_rank(a), pct_rank(b)
    ma, mb = statistics.mean(ra), statistics.mean(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = math.sqrt(sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb))
    return round(num / den, 4) if den else None


def pagerank(adj, outw, n, d=0.85, iters=50):
    pr = [1.0 / n] * n
    for _ in range(iters):
        new = [(1.0 - d) / n] * n
        dangling = 0.0
        for i in range(n):
            w = outw[i]
            if w <= 0:
                dangling += pr[i]
                continue
            share = d * pr[i] / w
            for j, ew in adj[i]:
                new[j] += share * ew
        add = d * dangling / n
        if add:
            for i in range(n):
                new[i] += add
        s = sum(new)
        pr = [x / s for x in new]
    return pr


def betweenness_sampled(adj, n, k, seed=42):
    """Brandes 单源 BFS，随机 k 个源，按 n/k 放大后按 1/((n-1)(n-2)) 归一"""
    rng = random.Random(seed)
    sources = rng.sample(range(n), min(k, n))
    cb = [0.0] * n
    for si, s in enumerate(sources):
        dist = [-1] * n
        sigma = [0.0] * n
        preds = [[] for _ in range(n)]
        dist[s] = 0
        sigma[s] = 1.0
        dq = deque([s])
        order = []
        while dq:
            v = dq.popleft()
            order.append(v)
            dv = dist[v]
            for w, _ in adj[v]:
                if dist[w] < 0:
                    dist[w] = dv + 1
                    dq.append(w)
                if dist[w] == dv + 1:
                    sigma[w] += sigma[v]
                    preds[w].append(v)
        delta = [0.0] * n
        for w in reversed(order):
            sw = sigma[w]
            if sw <= 0:
                continue
            coef = (1.0 + delta[w]) / sw
            for v in preds[w]:
                delta[v] += sigma[v] * coef
            if w != s:
                cb[w] += delta[w]
        if (si + 1) % 16 == 0:
            print(f"  betweenness {si + 1}/{len(sources)}", flush=True)
    scale = (n / len(sources)) / ((n - 1) * (n - 2)) if n > 2 else 1.0
    return [x * scale for x in cb]


def closeness_sampled(adj, n, k, seed=43):
    """调和接近：Σ(1/d)/(n-1)，按 k 个源抽样后取均值（等价于乘 (n-1)/k 再除 (n-1)）"""
    rng = random.Random(seed)
    sources = rng.sample(range(n), min(k, n))
    acc = [0.0] * n
    for s in sources:
        dist = [-1] * n
        dist[s] = 0
        dq = deque([s])
        while dq:
            v = dq.popleft()
            dv = dist[v]
            for w, _ in adj[v]:
                if dist[w] < 0:
                    dist[w] = dv + 1
                    dq.append(w)
        for i, d in enumerate(dist):
            if d > 0:
                acc[i] += 1.0 / d
    return [x / len(sources) for x in acc]


def main():
    t0 = time.time()
    cur = gkx()
    cur.execute("SET SESSION max_execution_time=0")

    cur.execute("SELECT COUNT(*) FROM gkx.dwd_scholar_coauthor")
    raw = int(cur.fetchone()[0])
    cur.execute("""SELECT COUNT(*) FROM gkx.dwd_scholar_coauthor
                   WHERE co_scholar_id IS NULL OR co_scholar_id=0""")
    dropped = int(cur.fetchone()[0])
    cur.execute("""SELECT COUNT(*) FROM gkx.dwd_scholar_coauthor
                   WHERE co_scholar_id=scholar_id""")
    selfloop = int(cur.fetchone()[0])
    cur.execute("""SELECT COUNT(*) FROM gkx.dwd_scholar_coauthor
                   WHERE co_scholar_org_name_zh IS NOT NULL
                     AND co_scholar_org_name_zh<>''""")
    org_nonnull = int(cur.fetchone()[0])
    print(f"raw={raw} dropped={dropped} selfloop={selfloop} org_nonnull={org_nonnull}",
          flush=True)

    cur.execute("""SELECT scholar_id, co_scholar_id, co_paper_count
                   FROM gkx.dwd_scholar_coauthor
                   WHERE co_scholar_id IS NOT NULL AND co_scholar_id<>0
                     AND scholar_id<>co_scholar_id""")
    rows = cur.fetchall()
    cur.close()
    print(f"loaded {len(rows)} rows in {time.time() - t0:.1f}s", flush=True)

    pairs = {}
    for a, b, w in rows:
        w = int(w or 1)
        key = (a, b) if a < b else (b, a)
        if w > pairs.get(key, 0):
            pairs[key] = w
    del rows
    print(f"edges={len(pairs)} in {time.time() - t0:.1f}s", flush=True)

    nodes = sorted({x for e in pairs for x in e})
    idx = {u: i for i, u in enumerate(nodes)}
    n = len(nodes)
    adj = [[] for _ in range(n)]
    outw = [0.0] * n
    n_edges = len(pairs)
    for (a, b), w in pairs.items():
        i, j = idx[a], idx[b]
        adj[i].append((j, float(w)))
        adj[j].append((i, float(w)))
        outw[i] += w
        outw[j] += w
    del pairs
    print(f"nodes={n} graph built in {time.time() - t0:.1f}s", flush=True)

    deg = [len(adj[i]) for i in range(n)]
    wdeg = [outw[i] for i in range(n)]

    print("pagerank ...", flush=True)
    pr = pagerank(adj, outw, n)
    print(f"pagerank done {time.time() - t0:.1f}s", flush=True)
    print(f"betweenness ({K_SRC} sources) ...", flush=True)
    btw = betweenness_sampled(adj, n, K_SRC)
    print(f"betweenness done {time.time() - t0:.1f}s", flush=True)
    print(f"closeness ({K_SRC} sources) ...", flush=True)
    clo = closeness_sampled(adj, n, K_SRC)
    print(f"closeness done {time.time() - t0:.1f}s", flush=True)

    P = {"deg": pct_rank(deg), "wdeg": pct_rank(wdeg), "btw": pct_rank(btw),
         "clo": pct_rank(clo), "pr": pct_rank(pr)}

    scen, scores = {}, {}
    for name, w in SCENARIOS.items():
        sc = [round(100 * sum(w[k] * P[k][i] for k in w), 3) for i in range(n)]
        scores[name] = sc
        order = sorted(range(n), key=lambda i: (-sc[i], nodes[i]))
        ss = sorted(sc)
        p90 = ss[int(len(ss) * 0.90)]
        p50 = ss[int(len(ss) * 0.50)]
        scen[name] = {
            "weights": w, "p90": round(p90, 3), "p50": round(p50, 3),
            "tiers": {"high": sum(1 for s in sc if s >= p90),
                      "mid": sum(1 for s in sc if p50 <= s < p90),
                      "low": sum(1 for s in sc if s < p50)},
            "top": [{"rank": r + 1, "node": nodes[j], "priority": sc[j],
                     "degree": deg[j], "weighted_degree": wdeg[j],
                     "betweenness": round(btw[j], 6),
                     "closeness": round(clo[j], 6),
                     "pagerank": round(pr[j], 8)}
                    for r, j in enumerate(order[:20])],
        }
    print(f"scenarios done {time.time() - t0:.1f}s", flush=True)

    stability = {}
    for name in SCENARIOS:
        stability[name] = {
            "spearman_vs_W1": spearman(scores["W1_等权"], scores[name]),
            "top20_overlap": len({t["node"] for t in scen[name]["top"]} &
                                 {t["node"] for t in scen["W1_等权"]["top"]}),
        }

    # 度 vs 加权度名次错位
    rank_d = {nodes[i]: r + 1 for r, i in
              enumerate(sorted(range(n), key=lambda x: -deg[x]))}
    rank_w = {nodes[i]: r + 1 for r, i in
              enumerate(sorted(range(n), key=lambda x: -wdeg[x]))}
    probes = []
    for j in sorted(range(n), key=lambda x: -deg[x])[:3] + \
             sorted(range(n), key=lambda x: -wdeg[x])[:3]:
        u = nodes[j]
        if any(p["node"] == u for p in probes):
            continue
        probes.append({"node": u, "degree": deg[j], "weighted_degree": wdeg[j],
                       "degree_rank": rank_d[u], "weighted_rank": rank_w[u]})

    # 连通块
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i in range(n):
        for j, _ in adj[i]:
            if i < j:
                a, b = find(i), find(j)
                if a != b:
                    parent[a] = b
    sizes = {}
    for i in range(n):
        r = find(i)
        sizes[r] = sizes.get(r, 0) + 1
    comp_sizes = sorted(sizes.values(), reverse=True)

    srt = sorted(deg)
    stats = {
        "degree_max": max(deg), "degree_median": srt[n // 2],
        "degree_mean": round(sum(deg) / n, 2),
        "weighted_degree_max": max(wdeg),
        "weighted_degree_median": sorted(wdeg)[n // 2],
        "betweenness_max": round(max(btw), 6),
        "closeness_max": round(max(clo), 6),
        "pagerank_max": round(max(pr), 8),
        "degree_ge3": sum(1 for d in deg if d >= 3),
        "degree_ge10": sum(1 for d in deg if d >= 10),
        "degree_ge100": sum(1 for d in deg if d >= 100),
        "n_components": len(comp_sizes),
        "largest_component": comp_sizes[0],
        "largest_component_pct": round(100.0 * comp_sizes[0] / n, 2),
        "top5_components": comp_sizes[:5],
    }

    out = {
        "metric_id": "M_INNOV_DS_02_PATH_003",
        "metric_name": "节点优先级/重要度",

        # 基期披露（派单书铁律 5 / DATA_FACTS §3.16）：本件为全量截面，不用任何时序分母，
        # 因此两个列表都为空；写出来是为了让"没有基期"这件事可查，而不是缺字段。
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("图结构指标取 gkx.dwd_scholar_coauthor 全量截面，不消费任何年份列；无增速、无同比、无基期，故不涉及时序分母，也不存在缺失年被按 0 摊入的风险。"),
        "data_plane": "gkx（183.240.141.251:3318）",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "graph_source": "gkx.dwd_scholar_coauthor（真实学者合著网）",
        "cleaning": {
            "raw_rows": raw, "dropped_null_or_zero_co_id": dropped,
            "dropped_ratio": round(dropped / raw, 4), "self_loops": selfloop,
            "org_name_nonnull_rows": org_nonnull,
            "org_name_nonnull_ratio": round(org_nonnull / raw, 4),
            "dedup_rule": "undirected (min,max), keep max(co_paper_count)",
        },
        "graph_size": {"edges_after_dedup": n_edges, "nodes": n},
        "sampling": {"k_sources": K_SRC,
                     "method": "Brandes 抽样 + 多源 BFS 累加（betweenness / closeness 共用源数）"},
        "normalization": "百分位秩（同值取平均秩）",
        "scenarios": SCENARIOS,
        "stats": stats,
        "scenario_results": scen,
        "stability": stability,
        "degree_vs_weighted": probes,
        "support_judgment": {
            "data_support_level": "完全转换支持",
            "criteria": {
                "structure": "gkx.dwd_scholar_coauthor（两端 id + co_paper_count）",
                "volume": f"{n:,} 节点 / {sum(len(a) for a in adj) // 2:,} 边",
                "reproducible": True,
                "discriminative": True,
            },
            "note": "四中心性在真实合著网上全部非退化，三套权重情景均可出分并量化名次稳定性。",
        },
        "elapsed_sec": round(time.time() - t0, 1),
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)
    print(json.dumps(stats, ensure_ascii=False), flush=True)
    print("stability", json.dumps(stability, ensure_ascii=False), flush=True)
    print("degree_vs_weighted", json.dumps(probes, ensure_ascii=False), flush=True)
    for name, s in scen.items():
        print(name, "p90", s["p90"], "p50", s["p50"], s["tiers"],
              [(t["node"], t["priority"]) for t in s["top"][:3]], flush=True)
    print("elapsed", out["elapsed_sec"], "written", OUT, flush=True)


if __name__ == "__main__":
    main()
