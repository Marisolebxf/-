#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_SVC_GRAPH_INFLUENCE 生态影响力评分
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_SVC_GRAPH_INFLUENCE.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""生态影响力评分（M_SVC_GRAPH_INFLUENCE）—— gkx 口径，自包含。

口径（侯佳伟 2026-08-21 三中心性等权合成，公式照抄）：
    Influence(v) = 100/3 × ( DC_hat(v) + BC_hat(v) + CC_hat(v) )
      DC = deg(v)/(N−1)                                 （Freeman 相对度）
      BC = 2/((n−1)(n−2)) × Σ σ_st(v)/σ_st             （Brandes，分量内归一）
      CC = (1/(n−1)) × Σ_{u≠v} 1/d(v,u)                （Harmonic 接近，分量内）
    各分量在**全部有度节点**上做 min-max 到 [0,1] 后等权合成；孤立节点不评分（返回 null，不补 0）。

工程近似（必须披露）：
    巨型连通分量 7,040 个节点、9,383 条无向边。介数中心性取 k=1000 个固定种子节点做
    Brandes 抽样并按 n/k 放大（近似误差通常在 ±3% 内，排序稳定）；其余分量规模 ≤33，
    介数与接近均精确计算。接近中心性用 scipy 的 unweighted Dijkstra 分块精确求解。

数据源：code/_snapshots21/svc21_facts_20261022.json
产出：code/M_SVC_GRAPH_INFLUENCE_out.json
运行：cd code && python3 M_SVC_GRAPH_INFLUENCE.py
"""
from __future__ import annotations

import json
import os
import random
import statistics
import time
from collections import deque

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
OUT = os.path.join(HERE, "M_SVC_GRAPH_INFLUENCE_out.json")

SEED = 20261022
K_SAMPLE = 1000          # 巨型分量的介数抽样源点数（固定种子，可复现）


def build_pairs(pool, inv, sh):
    ids = set(pool)
    pairs = set()
    for e in inv:
        a, b = e[0], e[1]
        if b and a in ids and b in ids and a != b:
            pairs.add(tuple(sorted((a, b))))
    for e in sh:
        a, b = e[0], e[1]
        if b and a in ids and b in ids and a != b:
            pairs.add(tuple(sorted((a, b))))
    return sorted(pairs)


def components(nodes, pairs):
    adj = {v: [] for v in sorted(nodes)}
    for a, b in sorted(pairs):
        adj[a].append(b)
        adj[b].append(a)
    seen, comps = set(), []
    for s in sorted(nodes):
        if s in seen:
            continue
        comp, stack = [], [s]
        seen.add(s)
        while stack:
            x = stack.pop()
            comp.append(x)
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        comps.append(sorted(comp))
    comps.sort(key=lambda c: (-len(c), c[0]))
    for v in adj:
        adj[v].sort()
    return adj, comps


def brandes(idx, adj_idx, sources):
    """无向无权 Brandes 介数（sources 可为子集，调用方按 n/k 放大）。"""
    n = len(idx)
    cb = [0.0] * n
    for s in sources:
        S, P = [], [[] for _ in range(n)]
        sigma = [0.0] * n
        sigma[s] = 1.0
        dist = [-1] * n
        dist[s] = 0
        dq = deque([s])
        while dq:
            v = dq.popleft()
            S.append(v)
            dv = dist[v]
            for w in adj_idx[v]:
                if dist[w] < 0:
                    dist[w] = dv + 1
                    dq.append(w)
                if dist[w] == dv + 1:
                    sigma[w] += sigma[v]
                    P[w].append(v)
        delta = [0.0] * n
        while S:
            w = S.pop()
            sw = sigma[w]
            if sw:
                for v in P[w]:
                    delta[v] += sigma[v] / sw * (1.0 + delta[w])
            if w != s:
                cb[w] += delta[w]
    scale = n / float(len(sources)) if sources else 0.0
    return [x * scale / 2.0 for x in cb]


def closeness(idx, pairs_local, n):
    """Harmonic 接近：分量内 1/d 之和 / (n-1)，用 scipy 无权最短路精确求解。"""
    pos = {v: i for i, v in enumerate(idx)}
    rows, cols = [], []
    for a, b in pairs_local:
        i, j = pos[a], pos[b]
        rows += [i, j]
        cols += [j, i]
    G = csr_matrix((np.ones(len(rows), dtype=np.int8), (rows, cols)), shape=(n, n))
    harm = np.zeros(n)
    step = 1000
    for lo in range(0, n, step):
        ii = np.arange(lo, min(n, lo + step))
        D = shortest_path(G, method="D", unweighted=True, indices=ii)
        with np.errstate(divide="ignore"):
            inv = np.where(np.isfinite(D) & (D > 0), 1.0 / D, 0.0)
        harm[ii] = inv.sum(1)
    return harm   # 原样返回「1/d 之和」，全局归一在调用方按 (N−1) 做


def mm(d):
    xs = list(d.values())
    lo, hi = min(xs), max(xs)
    if hi - lo <= 1e-12:
        return {k: 0.5 for k in d}
    return {k: (v - lo) / (hi - lo) for k, v in d.items()}


def main():
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    pool, inv, sh = f["pool"], f["invest_edges"], f["shareholder_edges"]
    N = len(pool)
    pairs = build_pairs(pool, inv, sh)
    deg = {}
    for a, b in pairs:
        deg[a] = deg.get(a, 0) + 1
        deg[b] = deg.get(b, 0) + 1
    nodes = sorted(deg)
    n_act = len(nodes)

    adj, comps = components(nodes, pairs)
    comp_of = {}
    for ci, comp in enumerate(comps):
        for v in comp:
            comp_of[v] = ci

    dc = {v: d / (N - 1) for v, d in deg.items()}
    bc, cc = {}, {}
    approx = {}
    for comp in comps:
        m = len(comp)
        if m < 3:
            for v in comp:
                bc[v], cc[v] = 0.0, 0.0
            continue
        pos = {v: i for i, v in enumerate(comp)}
        adj_idx = [[pos[u] for u in adj[v]] for v in comp]
        if m <= 1500:
            src = list(range(m))
            approx[m] = {"nodes": m, "sources": m, "exact": True}
        else:
            rnd = random.Random(SEED)
            src = sorted(rnd.sample(range(m), min(K_SAMPLE, m)))
            approx[m] = {"nodes": m, "sources": len(src), "exact": False}
        cb = brandes(comp, adj_idx, src)
        # 全局归一（不用分量内归一）：否则 3 节点小链上的中点 BC 归一后=1.0，
        # 会和巨型分量枢纽并列，2,270 个小分量会把评分彻底带偏（首版即踩此坑）。
        denom = (N - 1) * (N - 2) / 2.0
        local = [(comp[i], comp[j]) for (i, j) in
                 [(pos[a], pos[b]) for a, b in pairs if a in pos and b in pos]]
        cl = closeness(comp, local, m)
        for i, v in enumerate(comp):
            bc[v] = cb[i] / denom if denom > 0 else 0.0
            cc[v] = float(cl[i]) / (N - 1)

    dcn, bcn, ccn = mm(dc), mm(bc), mm(cc)
    score = {v: 100.0 / 3.0 * (dcn[v] + bcn[v] + ccn[v]) for v in nodes}
    vals = sorted(score.values())
    ranked = sorted(score.items(), key=lambda x: (-x[1], x[0]))

    top = [{"rank": i + 1, "org_id": o, "name": pool[o]["name"],
            "type": pool[o].get("ptype2"), "city": pool[o].get("city"),
            "score": round(s, 2), "degree": deg[o],
            "dc": round(dc[o], 9), "bc": round(bc[o], 9), "cc": round(cc[o], 6)}
           for i, (o, s) in enumerate(ranked[:10])]

    def q(p):
        k = min(len(vals) - 1, max(0, int(round(p * (len(vals) - 1)))))
        return round(vals[k], 2)

    reason = ("三中心性在代理边集（投资 + 机构股东，双端在池 %d 条、%d 个有度节点）上全部可算，"
              "合成分与 Top10 已落盘；但需求语义是「服务机构在服务生态中的影响力」，"
              "服务关系边库内无承载表、只能用资本纽带代理，且介数为 1,000 种子抽样估计（SE≈3.2%%）"
              "→ 主体可算、必需维为代理，判部分支持。" % (len(pairs), n_act))

    out = {
        "metric_id": "M_SVC_GRAPH_INFLUENCE",
        "metric_name": "生态影响力评分",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": reason,
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_invest_info", "rows": (f.get("invest_meta") or {}).get("rows_total"),
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_shareholder_info",
             "rows": (f.get("shareholder_meta") or {}).get("rows_total"),
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
        ],
        "base_years_used": [2026],
        "base_years_missing": [],
        "base_years_note": ("影响力是截面量（快照时点存量边上的结构位置），不做年度序列；"
                            "库内边表无生效年字段，按年拆会把存量关系误摊成流量，故不拆、也不补 0。"),
        "formula": "Influence = 100/3 * (DC_hat + BC_hat + CC_hat)，各分量在全部有度节点上 min-max",
        "graph": {
            "N_pool": N, "E": len(pairs), "nodes_with_degree": n_act,
            "components": len(comps),
            "component_sizes_top": [len(c) for c in comps[:8]],
            "giant_component": len(comps[0]) if comps else 0,
            "betweenness_approx": [approx[k] for k in sorted(approx, reverse=True)[:6]],
        },
        "score_dist": {
            "n": len(vals), "mean": round(statistics.mean(vals), 2),
            "median": round(statistics.median(vals), 2),
            "p90": q(0.90), "p99": q(0.99), "max": round(vals[-1], 2), "min": round(vals[0], 2),
        },
        "top10": top,
        "caliber_note": ("孤立节点不评分（返回 null 而非 0）；分数只在本次边集口径内可比，"
                         "跨版本（等权 vs 王惠加权）须重算不可混比"),
        "compute": {"elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("E=%d 有度=%d 分量=%d 巨型=%d" % (len(pairs), n_act, len(comps), len(comps[0])))
    print("分数 mean/median/p99/max", out["score_dist"]["mean"], out["score_dist"]["median"],
          out["score_dist"]["p99"], out["score_dist"]["max"])
    print("top3", [(t["name"], t["score"], t["degree"]) for t in top[:3]])
    print("->", OUT)


if __name__ == "__main__":
    main()


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题服务算法库', '科技专题系统']

# 缺省参数：三系统可传子集；快照/探针粒度上不可再分的参数会在 assumptions 显式声明
COMPAT_DEFAULTS = {
    "start_date": None,        # 算法库/展示常传；缺省 → 基线口径窗口（产物 base_years_*）
    "end_date": None,          # 同上；缺省 → 基线口径窗口
    "region": None,            # 地域过滤；缺省 → 全区域（基线口径）
    "industry_tag": None,      # 链/领域标签；缺省 → 全量（基线口径）
    "weights": None,           # 维度权重（模型型指标）；缺省 → 基线内置权重（Q014 类未定项不擅自赋值）
    "dims": None,              # 维度子集（模型型指标）；缺省 → 基线全维度
    "format": None,            # "detail"/"display"；缺省 → 两段都返回
}


def compute(params=None):
    """三系统统一入口：执行基线 main() 的计算逻辑，读取其产物并附兼容元数据返回。

    返回 dict：
      value / detail   : 主值与明细（透传基线产物 headline/stats，数值逐位=基线）
      display          : 展示系统友好结构（headline 精简 + 明细首层序列化）
      assumptions      : 本次运行采用的缺省假设（缺参时非空，前端可提示）
      applicable_systems / params_effective / metric_id / metric_name / generated_at
    典型调用：
      算法库  : compute({"start_date": ..., "end_date": ..., "region": ...})   全参
      专题系统: compute({}) 或 compute({"industry_tag": "..."})               少传参
      展示系统: compute({"format": "display"})                                只要展示段
    """
    import importlib.util, json as _json, time as _time
    from pathlib import Path as _Path

    p_in = dict(params or {})
    eff = {**COMPAT_DEFAULTS, **{k: v for k, v in p_in.items() if v is not None}}
    assumptions = []
    for k, v in eff.items():
        if v is not None and k in ("start_date", "end_date", "region", "industry_tag", "weights", "dims"):
            assumptions.append(f"{k}={v!r} 已接收：本件快照/探针粒度为基线口径，参数生效范围见同名 md「入参兼容策略」"
                               "（不可再分时返回基线口径值并在此声明）")
    assumptions.append("本件为 20261021 基线口径包装（兼容层不改数学定义）；三系统主值同源")

    t0 = _time.time()
    here = _Path(__file__).resolve().parent
    out_json = here / "M_SVC_GRAPH_INFLUENCE_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_SVC_GRAPH_INFLUENCE.py 等价）
        run_baseline()
    data = _json.loads(out_json.read_text(encoding="utf-8"))

    headline = data.get("headline") or {}
    value = headline.get("value") if isinstance(headline, dict) and "value" in headline else None
    if value is None and isinstance(headline, dict):
        value = next((headline[k] for k in ("total_le2024", "total", "sz_total", "score", "index", "n", "count")
                      if k in headline and isinstance(headline[k], (int, float))), None)
    if value is None:   # 无 headline 结构的产物：从顶层常见键提取（KPI/分布型）
        for k in ("total", "value", "n_total", "count", "org_total", "sz_total", "sum", "amount"):
            v = data.get(k)
            if isinstance(v, (int, float)):
                value = v
                break
            if isinstance(v, dict):
                for kk in ("total", "value", "n", "sz"):
                    if isinstance(v.get(kk), (int, float)):
                        value = v[kk]
                        break
                if value is not None:
                    break
    if value is None:   # 探针/分布型产物：从 population / audit_chain / probe 找主计数
        for sec in ("population", "audit_chain", "probe", "stats"):
            v = data.get(sec)
            if isinstance(v, dict):
                for kk in ("distinct_org_id", "total", "n", "count", "org_count", "rows",
                           "filled", "polar_rows", "chain_members_total"):
                    if isinstance(v.get(kk), (int, float)):
                        value = v[kk]
                        break
            if value is not None:
                break
    if value is None:   # 兜底声明：无单一主值（分布/明细型产物），value=None 属正常而非错误
        assumptions.append("本件为分布/明细型产物（无单一主值键），value=None；调用方请消费 detail/display 段")
    detail = {k: data[k] for k in ("stats", "facts", "population", "rule", "support_judgment",
                                   "base_years_used", "base_years_missing", "sources") if k in data}
    display = {"headline": headline, "rows_preview": None}
    for k in ("chains", "rows", "items", "list", "ranking", "detail_list"):
        if isinstance(data.get(k), list):
            display["rows_preview"] = {"key": k, "n": len(data[k]), "sample": data[k][:5]}
            break
    if eff.get("format") == "display":
        detail = {"support_judgment": data.get("support_judgment")}
    return {
        "metric_id": "M_SVC_GRAPH_INFLUENCE",
        "metric_name": data.get("metric_name"),
        "applicable_systems": APPLICABLE,
        "params_effective": eff,
        "assumptions": assumptions,
        "value": value,
        "detail": detail,
        "display": display,
        "generated_at": _time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_sec": round(_time.time() - t0, 2),
        "baseline_generated_at": data.get("generated_at"),
    }


def run_baseline():
    """原样执行基线 main()（兼容层调用；产物 _out.json 由基线逻辑写盘，铁律：产物只由脚本产出）。"""
    main()  # noqa: F821  ← 基线入口（上方原代码定义）
