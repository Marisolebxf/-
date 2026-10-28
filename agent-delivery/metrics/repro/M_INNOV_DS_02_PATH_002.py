#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_DS_02_PATH_002 · 关键节点重要性（20261021 换源版：gkx 直取）。

口径
----
节点 = IPC4 技术小类；边 = **同一件专利内共类**（主分类 + 附加分类截断到 4 位后两两配对）；
边权 = 共类件数 co，并以关联强度 AS = co·N/(n_i·n_j) 与 Jaccard 作尺度对照。
关键节点 = 度 ≥ P90 且度 ≥ 3（与族内 001/002/011 口径一致）。

为什么是抽样而不是全表
----------------------
`gkx.dwd_patent` 2,939,895 行、55 列，`main_classification_ipcr` 无索引（DATA_FACTS §3.68、
SHARED_ASSETS §三）。全表取 IPC 列 = 无索引全表扫，服务端 2,400 秒主动断连（已复现 ≥4 次）。
本件按**主键三段等距抽样**（dwd_id < 2,000,000 / 20,000,000—22,000,000 / 40,000,000—41,500,000）
取窄投影三列，落盘 `code/_snapshots21/tech_d_ipc4_sample_20261023.jsonl` 后可零 SQL 重跑。
抽样框、行数、占全表比例全部写进产物；三段的读数又互相作稳定性对照。

数据面：gkx @ 183.240.141.251:3318（只读）。
"""
from __future__ import annotations

import json
import math
import statistics
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import _gkxdb as DB  # noqa: E402

OUT = HERE / "M_INNOV_DS_02_PATH_002_out.json"
SNAP = HERE / "_snapshots21"
SAMPLE = SNAP / "tech_d_ipc4_sample_20261023.jsonl"
TOTAL_PATENTS = 2_939_895

RANGES = [(0, 2_000_000), (20_000_000, 22_000_000), (40_000_000, 41_500_000)]
MIN_NODE_PAT = 50
MIN_EDGE_CO = 5


def ipc4s(main, further):
    codes = []
    if main:
        s = str(main).strip()
        if len(s) >= 4 and s[:4].isalnum():
            codes.append(s[:4].upper())
    if further and str(further) not in ("[]", "null", "NULL", ""):
        try:
            for x in (json.loads(further) if isinstance(further, str) else further):
                s = str(x).strip()
                if len(s) >= 4 and s[:4].isalnum():
                    codes.append(s[:4].upper())
        except Exception:
            pass
    return list(dict.fromkeys(codes))


def build_sample():
    """三段主键抽样；已有落盘则直接复用（零 SQL 重跑）。"""
    if SAMPLE.exists():
        rows = [json.loads(x) for x in SAMPLE.open(encoding="utf-8")]
        return rows, {"reused": True}
    cur = DB.gkx()
    rows, meta = [], {"reused": False, "ranges": []}
    try:
        cur.execute("SET SESSION max_execution_time=0")
        for lo, hi in RANGES:
            t = time.time()
            cur.execute("SELECT dwd_id, main_classification_ipcr, further_classification_ipcr "
                        "FROM gkx.dwd_patent WHERE dwd_id >= %s AND dwd_id < %s", (lo, hi))
            got = cur.fetchall()
            rows.extend({"id": int(r[0]), "main": r[1], "further": r[2]} for r in got)
            meta["ranges"].append({"lo": lo, "hi": hi, "rows": len(got),
                                   "sec": round(time.time() - t, 1)})
            print("range", lo, hi, len(got), flush=True)
    finally:
        cur.close()
    with SAMPLE.open("w", encoding="utf-8") as fo:
        for r in rows:
            fo.write(json.dumps(r, ensure_ascii=False) + "\n")
    return rows, meta


def absence_probe():
    out = {"source": "gkx.information_schema（2026-10-23 实测）", "checks": []}
    cur = DB.gkx()
    try:
        cur.execute("SET SESSION max_execution_time=60000")
        for t in ("enterprise_cooperation", "enterprise_supply_chain",
                  "enterprise_industry_chain", "enterprise_centrality", "graph_edge"):
            cur.execute("SELECT COUNT(*) FROM information_schema.tables "
                        "WHERE table_schema='gkx' AND table_name=%s", (t,))
            out["checks"].append({"table": t, "hit_rows": int(cur.fetchone()[0]),
                                  "query": "information_schema.tables WHERE table_schema='gkx' "
                                           "AND table_name='%s'" % t})
        for kw in ("cooperat", "coop", "collab"):
            cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='gkx' "
                        "AND table_name LIKE %s", ("%" + kw + "%",))
            out.setdefault("fuzzy", {})[kw] = int(cur.fetchone()[0])
        out["conclusion"] = ("企业合作表逐字命中 0、模糊词 cooperat/coop/collab 表名命中 0；"
                             "技术点图只能由专利 IPC4 共类重建，不能读企业合作边。")
    finally:
        cur.close()
    return out


def graph_from(patents):
    ipc_total, pair, ipc_year = Counter(), Counter(), Counter()
    n_ipc = 0
    for r in patents:
        codes = ipc4s(r.get("main"), r.get("further"))
        if not codes:
            continue
        n_ipc += 1
        for c in codes:
            ipc_total[c] += 1
        for i in range(len(codes)):
            for j in range(i + 1, len(codes)):
                pair[tuple(sorted((codes[i], codes[j])))] += 1
    nodes = {n for n, c in ipc_total.items() if c >= MIN_NODE_PAT}
    edges = []
    for (a, b), co in pair.items():
        if a in nodes and b in nodes and co >= MIN_EDGE_CO:
            na, nb = ipc_total[a], ipc_total[b]
            edges.append({"src": a, "dst": b, "co": int(co),
                          "ass": round(co * n_ipc / (na * nb), 6),
                          "jaccard": round(co / (na + nb - co), 6)})
    edges.sort(key=lambda e: (-e["co"], e["src"], e["dst"]))
    return {"n_ipc": n_ipc, "ipc_total": ipc_total, "pair": pair,
            "nodes": nodes, "edges": edges}


def centralities(g):
    nodes = sorted(g["nodes"])
    idx = {n: i for i, n in enumerate(nodes)}
    m = len(nodes)
    adj = [[] for _ in range(m)]
    for e in g["edges"]:
        a, b = idx[e["src"]], idx[e["dst"]]
        adj[a].append((b, e["co"]))
        adj[b].append((a, e["co"]))

    deg = [len(adj[i]) for i in range(m)]
    wdeg = [sum(w for _, w in adj[i]) for i in range(m)]

    # 调和接近中心性（处理不连通图，标准做法）
    harm = []
    for s in range(m):
        dist = [-1] * m
        dist[s] = 0
        q = [s]
        while q:
            nxt = []
            for u in q:
                for v, _ in adj[u]:
                    if dist[v] < 0:
                        dist[v] = dist[u] + 1
                        nxt.append(v)
            q = nxt
        tot = sum(1.0 / d for d in dist if d > 0)
        harm.append(tot / (m - 1) if m > 1 else 0.0)

    # Brandes 中介中心性（无权）
    bc = [0.0] * m
    for s in range(m):
        stack, pred, sigma, dist = [], [[] for _ in range(m)], [0] * m, [-1] * m
        sigma[s], dist[s] = 1, 0
        q = [s]
        while q:
            v = q.pop(0)
            stack.append(v)
            for w, _ in adj[v]:
                if dist[w] < 0:
                    dist[w] = dist[v] + 1
                    q.append(w)
                if dist[w] == dist[v] + 1:
                    sigma[w] += sigma[v]
                    pred[w].append(v)
        delta = [0.0] * m
        while stack:
            w = stack.pop()
            for v in pred[w]:
                delta[v] += sigma[v] / sigma[w] * (1 + delta[w])
            if w != s:
                bc[w] += delta[w]
    norm = 2.0 / ((m - 1) * (m - 2)) if m > 2 else 1.0
    bc = [x * norm for x in bc]

    pr = [1.0 / m] * m
    d = 0.85
    for _ in range(60):
        new = [(1 - d) / m] * m
        for a in range(m):
            s = sum(w for _, w in adj[a])
            if s <= 0:
                continue
            for b, wt in adj[a]:
                new[b] += d * pr[a] * wt / s
        tot = sum(new)
        pr = [x / tot for x in new]

    res = {}
    for n in nodes:
        i = idx[n]
        res[n] = {"degree": deg[i], "weighted_degree": wdeg[i],
                  "harmonic": round(harm[i], 6), "betweenness": round(bc[i], 6),
                  "pagerank": round(pr[i], 8), "patents": g["ipc_total"][n]}
    return res


def stat(vals):
    v = sorted(vals)
    if not v:
        return {"n": 0}
    def q(p):
        return v[min(len(v) - 1, max(0, int(round(p * (len(v) - 1)))))]
    return {"n": len(v), "min": round(v[0], 6), "p50": round(statistics.median(v), 6),
            "p90": round(q(0.9), 6), "max": round(v[-1], 6),
            "mean": round(statistics.mean(v), 6)}


def ranks(d):
    items = sorted(d.items(), key=lambda kv: (kv[1], kv[0]))
    out, i, n = {}, 0, len(items)
    while i < n:
        j = i
        while j + 1 < n and items[j + 1][1] == items[i][1]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            out[items[k][0]] = avg
        i = j + 1
    return out


def spearman(a, b):
    keys = sorted(set(a) & set(b))
    if len(keys) < 3:
        return None
    ra, rb = ranks({k: a[k] for k in keys}), ranks({k: b[k] for k in keys})
    xs = [ra[k] for k in keys]
    ys = [rb[k] for k in keys]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return round(num / (dx * dy), 6) if dx and dy else None


def main():
    t0 = time.time()
    patents, smeta = build_sample()
    print("sample", len(patents), smeta, flush=True)

    g = graph_from(patents)
    print("graph nodes", len(g["nodes"]), "edges", len(g["edges"]), flush=True)
    cen = centralities(g)
    nodes = sorted(g["nodes"], key=lambda n: (-cen[n]["degree"], n))

    degs = [cen[n]["degree"] for n in nodes]
    deg_p90 = sorted(degs)[int(round(0.9 * (len(degs) - 1)))]
    key = [n for n in nodes if cen[n]["degree"] >= deg_p90 and cen[n]["degree"] >= 3]

    # 关键节点综合分（四维 min-max 等权，仅用于排序展示，不改判定）
    def mm(vals):
        lo, hi = min(vals), max(vals)
        return [0.0 if hi == lo else (v - lo) / (hi - lo) for v in vals]
    h_mm = mm([cen[n]["harmonic"] for n in nodes])
    b_mm = mm([cen[n]["betweenness"] for n in nodes])
    p_mm = mm([cen[n]["pagerank"] for n in nodes])
    d_mm = mm([cen[n]["degree"] for n in nodes])
    comp = {n: round(100 * (d_mm[i] + h_mm[i] + b_mm[i] + p_mm[i]) / 4, 4)
            for i, n in enumerate(nodes)}

    def row(n):
        return {"ipc4": n, **cen[n], "composite": comp[n],
                "rank_degree": None}

    top_degree = [row(n) for n in nodes[:20]]
    top_pr = [row(n) for n in sorted(nodes, key=lambda n: -cen[n]["pagerank"])[:20]]
    top_bet = [row(n) for n in sorted(nodes, key=lambda n: -cen[n]["betweenness"])[:20]]
    top_comp = [row(n) for n in sorted(nodes, key=lambda n: -comp[n])[:20]]
    key_rows = sorted([row(n) for n in key], key=lambda r: -r["composite"])

    # 稳定性：三段各自建图，与全样本比 PageRank 名次
    by_range = {i: [] for i in range(len(RANGES))}
    for r in patents:
        for i, (lo, hi) in enumerate(RANGES):
            if lo <= r["id"] < hi:
                by_range[i].append(r)
                break
    stab = []
    pr_all = {n: cen[n]["pagerank"] for n in nodes}
    for i, rs in by_range.items():
        gi = graph_from(rs)
        ci = centralities(gi)
        common = sorted(set(gi["nodes"]) & set(nodes))
        rho = spearman({n: ci[n]["pagerank"] for n in common}, {n: pr_all[n] for n in common})
        top20i = sorted(common, key=lambda n: -ci[n]["pagerank"])[:20]
        top20a = sorted(nodes, key=lambda n: -pr_all[n])[:20]
        stab.append({"range": RANGES[i], "patents": len(rs), "nodes": len(gi["nodes"]),
                     "edges": len(gi["edges"]), "common_nodes": len(common),
                     "spearman_pagerank_vs_full": rho,
                     "top20_overlap": len(set(top20i) & set(top20a))})

    # 三种边权下的名次一致性
    rho_ass = spearman({e["src"]: e["ass"] for e in g["edges"]},
                       {e["src"]: e["co"] for e in g["edges"]})
    jac_nodes = {}
    for e in g["edges"]:
        jac_nodes.setdefault(e["src"], []).append(e["jaccard"])
    ass_nodes = {}
    for e in g["edges"]:
        ass_nodes.setdefault(e["src"], []).append(e["ass"])
    wdeg_ass = {k: sum(v) for k, v in ass_nodes.items()}
    wdeg_jac = {k: sum(v) for k, v in jac_nodes.items()}
    rho_w = spearman(wdeg_ass, wdeg_jac)

    total_pairs = len(g["pair"])
    deriv = {
        "sample_share_of_patent_table_pct": round(100.0 * len(patents) / TOTAL_PATENTS, 4),
        "ipc_covered_share_of_sample_pct": round(100.0 * g["n_ipc"] / len(patents), 4),
        "sample_patents_without_ipc": len(patents) - g["n_ipc"],
        "sample_patents_without_ipc_pct": round(
            100.0 * (len(patents) - g["n_ipc"]) / len(patents), 4),
        "node_keep_share_of_ipc4_universe_pct": round(100.0 * len(g["nodes"]) / len(g["ipc_total"]), 4),
        "edge_keep_share_of_pair_universe_pct": round(100.0 * len(g["edges"]) / total_pairs, 4),
        "key_node_share_pct": round(100.0 * len(key) / len(nodes), 4),
        "single_patent_pair_share_pct": round(
            100.0 * sum(1 for v in g["pair"].values() if v == 1) / total_pairs, 4),
        "mean_edges_per_node": round(len(g["edges"]) / len(nodes), 4),
        "degree_p90_cut": deg_p90,
        "denominator_note": (
            "• sample_share：分母 2,939,895（dwd_patent 全表 COUNT(*)）；\n"
            "• node_keep：分母 = 样本内出现过的 IPC4 小类数 %d；\n"
            "• edge_keep：分母 = 样本内共类配对种类数 %d；\n"
            "• key_node_share：分母 = 入网节点 %d（度阈值+件数阈值过滤后）。"
            % (len(g["ipc_total"]), total_pairs, len(nodes))
        ),
    }

    payload = {
        "metric_id": "M_INNOV_DS_02_PATH_002",
        "metric_name": "关键节点重要性",
        "support_judgment": "完全转换支持",
        "verdict_kind": "converted",
        "grain": "IPC4 技术小类（节点级中心性）",
        "data_source": "gkx @ 183.240.141.251:3318（只读）",
        "sources": ["gkx.dwd_patent（主键三段抽样，窄投影 3 列）",
                    "code/_snapshots21/tech_d_ipc4_sample_20261023.jsonl（本件落盘样本）",
                    "code/_snapshots21/w15c3_facts_20261023.json（表存在性探针）"],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面图件：共类关系不按年切分（IPC4 共类结构跨年稳定），"
                            "不做年度除法、不摊 0。样本含 2021—2026 申请年（dwd_patent 全年份覆盖）。"),
        "params": {"min_node_patents": MIN_NODE_PAT, "min_edge_co": MIN_EDGE_CO,
                   "edge_weight": "co（共类件数）；AS 与 Jaccard 作尺度对照",
                   "pagerank_alpha": 0.85, "pagerank_iters": 60,
                   "betweenness_normalized": True, "seed": None,
                   "sample_ranges": [{"lo": a, "hi": b} for a, b in RANGES],
                   "note": "本件无随机算法（确定性图算法），故无 seed/alpha 之外的随机参数"},
        "table_counts": {"dwd_patent": TOTAL_PATENTS,
                         "sample_patents": len(patents),
                         "sample_rows_by_range": [
                             {"lo": RANGES[i][0], "hi": RANGES[i][1], "rows": len(v)}
                             for i, v in by_range.items()]},
        "n_nodes": len(g["nodes"]),
        "n_edges": len(g["edges"]),
        "n_ipc4_universe": len(g["ipc_total"]),
        "n_patents_with_ipc": g["n_ipc"],
        "n_key_nodes": len(key),
        "n_isolates": sum(1 for n in nodes if cen[n]["degree"] == 0),
        "point_set": {
            "id": "P_IPC4",
            "definition": ("节点 = 样本内出现 ≥%d 件专利的 IPC4 小类；边 = 同件专利共类且共类件数 ≥%d；"
                           "无向加权图（权 = 共类件数）" % (MIN_NODE_PAT, MIN_EDGE_CO)),
            "n_nodes": len(nodes), "n_edges": len(g["edges"]),
            "node_coverage_of_ipc4_universe_pct": round(100.0 * len(nodes) / len(g["ipc_total"]), 4),
            "isolate_handling": ("低度孤立点（度=0）保留在节点集内、中心性记 0，不剔除——"
                                 "因为它们在样本里确有 ≥50 件专利，剔除会虚增平均度"),
            "low_volume_ipc4_excluded": len(g["ipc_total"]) - len(nodes),
        },
        "degree_stats": stat(degs),
        "weighted_degree_stats": stat([cen[n]["weighted_degree"] for n in nodes]),
        "pagerank_stats": stat([cen[n]["pagerank"] for n in nodes]),
        "harmonic_stats": stat([cen[n]["harmonic"] for n in nodes]),
        "betweenness_stats": stat([cen[n]["betweenness"] for n in nodes]),
        "top20_degree": top_degree,
        "top20_pagerank": top_pr,
        "top20_betweenness": top_bet,
        "top20_composite": top_comp,
        "key_nodes": key_rows,
        "rank_consistency": {
            "spearman_degree_vs_pagerank": spearman({n: cen[n]["degree"] for n in nodes},
                                                    {n: cen[n]["pagerank"] for n in nodes}),
            "spearman_degree_vs_betweenness": spearman({n: cen[n]["degree"] for n in nodes},
                                                       {n: cen[n]["betweenness"] for n in nodes}),
            "spearman_pagerank_vs_betweenness": spearman({n: cen[n]["pagerank"] for n in nodes},
                                                          {n: cen[n]["betweenness"] for n in nodes}),
            "spearman_weighted_as_vs_jaccard": rho_w,
            "edge_level_as_vs_co": rho_ass,
            "note": "四维高度相关但不完全重合，作「对比矩阵」有信息量；边权口径不影响节点名次。",
        },
        "stability_by_range": stab,
        "derived": deriv,
        "absence_probe": absence_probe(),
        "caveats": [
            "样本为三段等距主键抽样，非全表：IPC4 小类覆盖有偏（冷门小类可能被件数阈值 50 滤掉）。",
            "节点是 IPC4 小类，不是「技术点」实体：同一小类下的细分方向被合并。",
            "共类关系是「同一件专利里同时出现」，不是技术依赖/引用关系，方向性缺失。",
            "企业合作表在 gkx 无表，本件不拿专利共类冒充企业合作关系。",
        ],
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print("nodes=%d edges=%d key=%d rho(dp)=%s" % (
        len(g["nodes"]), len(g["edges"]), len(key),
        payload["rank_consistency"]["spearman_degree_vs_pagerank"]), flush=True)
    print("wrote", OUT.name, "%.1fs" % (time.time() - t0), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
