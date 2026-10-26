#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""节点度中心性（M_SVC_GRAPH_CENTRALITY）—— gkx 口径，自包含。

口径（侯佳伟 2026-08-21 度体系，公式照抄）：
    DC(v) = deg(v) / (N − 1)        （Freeman 相对度，无向简单图）
    边集  = 投资边 ∪ 机构股东边，双端在池、无向去重、去自环（与 113_1 同源同规则）
    两个分母口径并列：全池 N=44,153（生态位覆盖率语义）、活跃子网 N=12,905（枢纽排位语义）

与旧稿的差异：
    旧稿 N=43,296 / E=2,859（物化池）；本件 N=44,153 / E=13,141（经营范围池）。
    边数放大 4.6 倍不是「换库导致的数据差异」，而是旧稿的池是 `svc_org_card` 的窄口径
    （只收被档案卡收编的机构），本件池是主档经营范围命中，双端同时在池的概率更高。
    两个读数不可直接比大小，只能比结构（度右偏、度=1 长尾、枢纽具名）。

数据源：code/_snapshots21/svc21_facts_20261022.json
产出：code/M_SVC_GRAPH_CENTRALITY_out.json
运行：cd code && python3 M_SVC_GRAPH_CENTRALITY.py
"""
from __future__ import annotations

import json
import os
import statistics
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
OUT = os.path.join(HERE, "M_SVC_GRAPH_CENTRALITY_out.json")


def build_pairs(pool, inv, sh):
    """投资边 ∪ 机构股东边 → 双端在池的无向去重边集。"""
    ids = set(pool)
    pairs, selfloop, empty = set(), 0, 0
    for e in inv:
        a, b = e[0], e[1]
        if not b:
            empty += 1
            continue
        if a in ids and b in ids:
            if a == b:
                selfloop += 1
            else:
                pairs.add(tuple(sorted((a, b))))
    for e in sh:
        a, b = e[0], e[1]
        if not b:
            empty += 1
            continue
        if a in ids and b in ids:
            if a == b:
                selfloop += 1
            else:
                pairs.add(tuple(sorted((a, b))))
    return pairs, selfloop, empty


def q(vals, p):
    xs = sorted(vals)
    k = min(len(xs) - 1, max(0, int(round(p * (len(xs) - 1)))))
    return xs[k]


def main():
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    pool, inv, sh = f["pool"], f["invest_edges"], f["shareholder_edges"]
    N = len(pool)
    pairs, selfloop, empty = build_pairs(pool, inv, sh)

    deg = Counter()
    for a, b in pairs:
        deg[a] += 1
        deg[b] += 1
    n_act = len(deg)
    dvals = list(deg.values())

    dc_pool = {o: d / (N - 1) for o, d in deg.items()}
    dc_act = {o: d / (n_act - 1) for o, d in deg.items()}
    pv = list(dc_pool.values())
    av = list(dc_act.values())

    top = sorted(deg.items(), key=lambda x: (-x[1], x[0]))[:10]
    top_rows = [{"rank": i + 1, "org_id": o, "name": pool[o]["name"],
                 "type": pool[o].get("ptype2"), "city": pool[o].get("city"),
                 "degree": d,
                 "dc_pool": round(d / (N - 1), 9),
                 "dc_active": round(d / (n_act - 1), 6)} for i, (o, d) in enumerate(top)]

    deg1 = sum(1 for v in dvals if v == 1)
    hubs = sum(1 for v in dvals if v >= 50)
    zero = N - n_act

    reason = ("代理边集（投资 + 机构股东，双端在池 %d 条）上度中心性可现算并已出榜单；"
              "但需求口径的「服务关系边」（合作/交易/客户）在 gkx 无承载表，"
              "正式语义的服务网络度无源，故落部分支持。"
              % len(pairs))

    out = {
        "metric_id": "M_SVC_GRAPH_CENTRALITY",
        "metric_name": "节点度中心性",
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
        "base_years_note": ("度是截面量（快照时点的存量关系），无年度序列；"
                            "同一机构在不同年份的边会增减，但库内没有边的生效年份字段可拆年，"
                            "故不做年度度序列、也不补任何年份为 0。"),
        "caliber": {
            "formula": "DC(v) = deg(v) / (N - 1)",
            "edge_rule": "投资边 ∪ 机构股东边；双端在池；无向去重；去自环；对端空值（自然人股东）剔除",
            "N_pool": N,
            "N_active": n_act,
            "edges": len(pairs),
            "self_loop_dropped": selfloop,
            "empty_counterpart_rows": empty,
        },
        "degree_dist": {
            "nodes_scored": n_act,
            "nodes_isolated": zero,
            "share_scored_pct": round(100.0 * n_act / N, 2),
            "median": q(dvals, 0.5), "mean": round(statistics.mean(dvals), 4),
            "p90": q(dvals, 0.90), "p99": q(dvals, 0.99), "max": max(dvals),
            "deg_eq_1": deg1, "deg_eq_1_share_pct": round(100.0 * deg1 / n_act, 2),
            "hubs_ge_50": hubs,
        },
        "normalized": {
            "pool_caliber": {"min": round(min(pv), 9), "median": round(statistics.median(pv), 9),
                             "max": round(max(pv), 9)},
            "active_caliber": {"min": round(min(av), 8), "median": round(statistics.median(av), 8),
                               "max": round(max(av), 8)},
        },
        "top10": top_rows,
        "compute": {"elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("N", N, "E", len(pairs), "有度", n_act, "孤立", zero)
    print("度 median/p90/p99/max", out["degree_dist"]["median"], out["degree_dist"]["p90"],
          out["degree_dist"]["p99"], out["degree_dist"]["max"])
    print("DC(全池) max", out["normalized"]["pool_caliber"]["max"],
          "DC(活跃) max", out["normalized"]["active_caliber"]["max"])
    print("top1", top_rows[0]["name"], top_rows[0]["degree"])
    print("->", OUT)


if __name__ == "__main__":
    main()
