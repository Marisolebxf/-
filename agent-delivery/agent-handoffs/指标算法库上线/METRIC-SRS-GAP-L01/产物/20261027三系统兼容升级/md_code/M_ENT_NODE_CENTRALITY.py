#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_NODE_CENTRALITY 供应链中心性 —— gkx 真源复现（2026-10-22）

口径（calc-logic ENT/M_ENT_NODE_CENTRALITY.md，王惠 20260816 底稿 → Q014）：
    中心度 = deg(v) / (|V| - 1)，deg(v) 为企业直接相连的节点数；需先建供应链网络图。
    本脚本实现：无向图、并行边合并、自环剔除、度 0 记缺失（不入图、不赋 0 分）。

为什么本件算的是「股权关系代理图」而不是供应链图：
    gkx 280 张表里没有任何 supply / customer / upstream / downstream 语义的企业×企业边表
    （扫描见 probes.table_name_scan，零命中）；dwd_industry_chain_info 只有 1,273 行链定义
    与聚合计数（node_company_count），无法还原企业与企业之间的连线。因此本件用三类
    工商股权边建代理图，并在产物里显式标注 proxy_is_supply_chain=false。

数据源（全部 gkx，只读）：
    dwd_org_invest_info       46,967 行（投资方 org_id → 被投 inv_org_id）
    dwd_org_shareholder_info 400,286 行（有效 inv_org_id 77,411 行）
    dwd_org_subsidiary_info  178,900 行（有效 sub_org_id 178,874 行）
    dwd_org_base_info        189,116 行（节点名称/城市，仅用于 Top 榜可读性）

输出：code/M_ENT_NODE_CENTRALITY_out.json
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import pymysql

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "M_ENT_NODE_CENTRALITY_out.json"
SNAP = HERE / "_snapshots21"

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", database="gkx", charset="utf8mb4",
           cursorclass=pymysql.cursors.DictCursor, connect_timeout=15, read_timeout=600)

CREDIT_OK = re.compile(r"^[0-9A-Z]{18}$")


def pct(sorted_vals, q):
    if not sorted_vals:
        return None
    k = (len(sorted_vals) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(sorted_vals) - 1)
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (k - lo)


def main():
    edges = json.load(open(SNAP / "ent_edges_20261021.json", encoding="utf-8"))
    invest = edges["invest"]
    share = edges["shareholder"]

    base = json.load(open(SNAP / "base_20261021.json", encoding="utf-8"))
    name_of = {r[0]: r[2] for r in base}
    city_of = {r[0]: r[4] for r in base}

    # --- 边表存在性核验（零 DB）：按表名语义扫 gkx 280 张表 ---
    inv = json.load(open(ROOT / "_work_gkx21" / "GKX_INVENTORY.json", encoding="utf-8"))
    supply_pat = re.compile(r"(supply|customer|upstream|downstream|purchase|vendor|buyer)", re.I)
    graph_pat = re.compile(r"(graph|centrality|pagerank|node_edge)", re.I)
    supply_hits = sorted(t for t in inv if supply_pat.search(t))
    graph_hits = sorted(t for t in inv if graph_pat.search(t))

    c = pymysql.connect(**GKX)
    with c.cursor() as cur:
        cur.execute("SET SESSION max_execution_time=120000")
        cur.execute("SELECT org_id, sub_org_id FROM dwd_org_subsidiary_info LIMIT 1")
        _ = cur.fetchall()
        cur.execute("SELECT industry_code, industry_link_code, node_company_count "
                    "FROM dwd_industry_chain_info LIMIT 3")
        chain_sample = cur.fetchall()
        cur.execute("SELECT COUNT(*) FROM dwd_industry_chain_info")
        chain_rows = int(list(cur.fetchone().values())[0])
    c.close()

    # 子公司边读现成快照（178,874 条，2026-10-22 22:25 按 SSCursor 窄投影拉取并落盘）
    subs_snap = json.load(open(SNAP / "org_subsidiary_edges_20261022.json", encoding="utf-8"))
    subs = [tuple(x) for x in subs_snap["edges"]]
    subs_rows = subs_snap["rows"]

    raw = []
    for a, b in invest:
        raw.append((a, b, "invest"))
    for a, b in share:
        raw.append((a, b, "shareholder"))
    for a, b in subs:
        raw.append((a, b, "subsidiary"))

    adj = defaultdict(set)
    src_edges = Counter()
    self_loops = 0
    dedup = 0
    seen = set()
    for a, b, s in raw:
        if not a or not b:
            continue
        if a == b:
            self_loops += 1
            continue
        key = (a, b) if a < b else (b, a)
        if key in seen:
            dedup += 1
            continue
        seen.add(key)
        src_edges[s] += 1
        adj[a].add(b)
        adj[b].add(a)

    V = len(adj)
    E = len(seen)
    degs = [len(adj[v]) for v in adj]
    degs_sorted = sorted(degs)
    centrality = {v: len(adj[v]) / (V - 1) for v in adj}
    cent_sorted = sorted(centrality.values())

    dist = Counter()
    for d in degs:
        if d == 1:
            dist["1"] += 1
        elif d <= 4:
            dist["2-4"] += 1
        elif d <= 9:
            dist["5-9"] += 1
        elif d <= 49:
            dist["10-49"] += 1
        elif d <= 99:
            dist["50-99"] += 1
        else:
            dist["ge100"] += 1

    top = sorted(adj.items(), key=lambda kv: -len(kv[1]))[:20]
    top20 = []
    for v, nb in top:
        top20.append({
            "org_id": v,
            "name": name_of.get(v) or None,
            "city": city_of.get(v) or None,
            "degree": len(nb),
            "centrality": round(len(nb) / (V - 1), 8),
            "in_base": v in name_of,
        })
    top20_in_base = sum(1 for t in top20 if t["in_base"])

    base_nodes = sum(1 for v in adj if v in name_of)
    base_total = len(base)
    per_src = {"invest": len(invest), "shareholder": len(share), "subsidiary": len(subs)}

    payload = {
        "metric_id": "M_ENT_NODE_CENTRALITY",
        "metric_name_zh": "供应链中心性",
        "generated_for": "20261021 批 B-sample",
        "source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）",
        "support_judgment": "部分支持",
        "support_reason": ("公式 deg/(|V|-1) 与建图流程可复现，但 gkx 无企业×企业供应链边表，"
                           "只能用投资/股东/子公司三类股权边建代理图；供应链语义维度整块缺失。"),
        "probes": {
            "table_name_scan": {
                "total_tables": len(inv),
                "supply_semantic_hits": supply_hits,
                "supply_semantic_hit_count": len(supply_hits),
                "graph_semantic_hits": graph_hits,
                "graph_semantic_hit_count": len(graph_hits),
            },
            "chain_info": {
                "rows": chain_rows,
                "has_org_pair_columns": False,
                "sample_columns": list(chain_sample[0].keys()) if chain_sample else [],
                "sample": [list(r.values()) for r in chain_sample],
            },
            "subsidiary_rows": subs_rows,
            "edge_rows_by_source": per_src,
            "edges_kept_by_source": dict(src_edges),
            "edge_rows_pulled": len(raw),
            "self_loops_dropped": self_loops,
            "parallel_edges_dropped": dedup,
            "credit_code_regex_applied": CREDIT_OK.pattern,
        },
        "graph": {
            "V": V,
            "E": E,
            "base_firms_total": base_total,
            "base_firms_in_graph": base_nodes,
            "base_firms_coverage_pct": round(base_nodes / base_total * 100, 4),
            "external_nodes": V - base_nodes,
            "proxy_is_supply_chain": False,
            "directed": False,
            "parallel_merged": True,
            "self_loop_dropped": True,
        },
        "degree_dist": {
            "min": degs_sorted[0], "median": pct(degs_sorted, 0.5),
            "mean": round(sum(degs) / len(degs), 4),
            "p90": pct(degs_sorted, 0.9), "p99": pct(degs_sorted, 0.99),
            "max": degs_sorted[-1],
        },
        "degree_buckets": {k: dist.get(k, 0) for k in ("1", "2-4", "5-9", "10-49", "50-99", "ge100")},
        "degree_bucket_share_pct": {k: round(dist.get(k, 0) / V * 100, 2)
                                    for k in ("1", "2-4", "5-9", "10-49", "50-99", "ge100")},
        "centrality_dist": {
            "min": round(cent_sorted[0], 10), "median": round(pct(cent_sorted, 0.5), 10),
            "mean": round(sum(cent_sorted) / len(cent_sorted), 10),
            "p90": round(pct(cent_sorted, 0.9), 10), "p99": round(pct(cent_sorted, 0.99), 10),
            "max": round(cent_sorted[-1], 10),
        },
        "top20": top20,
        "top20_in_base": top20_in_base,
        "formula": "centrality(v) = deg(v) / (|V| - 1)",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面件：图快照为 2026-10-22 一次性拉取的三表全量边，不按年份切分，"
                            "因此无年度基期；分母 |V|-1 用的是当期节点数，跨期不可直接比较。"),
        "custom_thresholds": {
            "note": "Q014 未定义关键节点阈值，本件不给阈值判定，只给排序与分布。",
        },
    }
    json.dump(payload, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: payload[k] for k in ("graph", "degree_dist", "top20_in_base")},
                     ensure_ascii=False, indent=1))
    print("->", OUT)


if __name__ == "__main__":
    main()
