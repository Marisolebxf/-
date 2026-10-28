#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""服务关系链模型（M_SVC_DEEP_173_1）—— gkx 口径，自包含。

三维（需规 §1.1.1.1.1.1.1.9.2，社会网络分析测度族）：
    关系强度 —— 关系频次（双端在池内的边数）+ 交易规模（投资金额合计）+ 信用（失信/处罚反向）
    关系层次 —— 一阶可达（度）+ 二阶可达（2-hop 去重计数）
    关系密度 —— 局部聚类系数（邻居之间的实际连边 / 可能连边）

节点域 = 服务机构池（44,153 家）；边集 = 投资边（dwd_org_invest_info）+ 机构股东边
（dwd_org_shareholder_info 中对端也是机构的那部分）。人才流动边、竞争边、正式合作/交易
合同边在 gkx 无源（待建 svc_coop_edge / svc_trade_contract），本件用资本纽带代理。

数据源：code/_snapshots21/svc21_facts_20261022.json（gkx 只读快照）
产出：code/M_SVC_DEEP_173_1_out.json
运行：cd code && python3 M_SVC_DEEP_173_1.py
"""
from __future__ import annotations

import json
import os
import statistics
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
OUT = os.path.join(HERE, "M_SVC_DEEP_173_1_out.json")


def mm(vals: dict) -> dict:
    """min-max（内联复制自 M_SVC_DEEP_174_1.py，不 import 共享模块）"""
    xs = [v for v in vals.values() if v is not None]
    if not xs:
        return {}
    lo, hi = min(xs), max(xs)
    if hi - lo <= 1e-12:
        return {k: 0.5 for k in vals if vals[k] is not None}
    return {k: (v - lo) / (hi - lo) for k, v in vals.items() if v is not None}


def main():
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    pool, risk = f["pool"], f["risk"]

    adj = defaultdict(set)
    amt = defaultdict(float)
    freq = defaultdict(int)
    n_inv = n_sh = 0

    for a, b, money in f["invest_edges"]:
        if a in pool and b in pool and a != b:
            adj[a].add(b); adj[b].add(a)
            freq[a] += 1; freq[b] += 1
            if money:
                amt[a] += float(money); amt[b] += float(money)
            n_inv += 1

    for a, b in f["shareholder_edges"]:
        if b and a in pool and b in pool and a != b:
            adj[a].add(b); adj[b].add(a)
            freq[a] += 1; freq[b] += 1
            n_sh += 1

    nodes = list(adj.keys())
    deg = {o: len(adj[o]) for o in nodes}

    # 二阶可达（2-hop，去重，不含自身）
    hop2 = {}
    for o in nodes:
        s = set()
        for nb in adj[o]:
            s |= adj[nb]
        s.discard(o)
        hop2[o] = len(s)

    # 局部聚类系数（度 >= 2 才有定义）
    cc = {}
    for o in nodes:
        nb = adj[o]
        if len(nb) < 2:
            continue
        links = 0
        for u in nb:
            links += len(nb & adj[u])
        cc[o] = links / (len(nb) * (len(nb) - 1))   # 有向计数 /2 已并入

    riskcnt = {o: int((risk.get(o) or {}).get("shixin", 0)) + int((risk.get(o) or {}).get("punish", 0)) for o in nodes}

    s_strength, s_level, s_density = {}, {}, {}
    f_n, a_n, r_n = mm({o: freq[o] for o in nodes}), mm({o: amt[o] for o in nodes}), mm({o: -riskcnt[o] for o in nodes})
    d_n, h_n = mm(deg), mm(hop2)
    for o in nodes:
        parts = [f_n[o]] + ([a_n[o]] if o in a_n else []) + ([r_n[o]] if o in r_n else [])
        s_strength[o] = sum(parts) / len(parts)
        s_level[o] = (d_n[o] + h_n[o]) / 2.0
    for o, v in cc.items():
        s_density[o] = v / max(cc.values()) if max(cc.values()) > 0 else 0.5

    idx = {}
    for o in nodes:
        av = [s_strength[o], s_level[o]]
        if o in s_density:
            av.append(s_density[o])
        idx[o] = 100.0 * sum(av) / len(av)

    vals = sorted(idx.values())
    ranked = sorted(idx.items(), key=lambda x: -x[1])
    top = [{"org_id": o, "name": pool[o]["name"], "city": pool[o]["city"], "ptype": pool[o].get("ptype2"),
            "index": round(v, 2), "degree": deg[o], "hop2": hop2[o],
            "invest_amount": round(amt[o], 2), "clustering": round(cc.get(o, 0), 4),
            "risk_cnt": riskcnt[o]} for o, v in ranked[:10]]

    # 连通分量（在双端都落池的边集上）
    seen, comps = set(), []
    for o in nodes:
        if o in seen:
            continue
        stack, comp = [o], []
        seen.add(o)
        while stack:
            u = stack.pop()
            comp.append(u)
            for w in adj[u]:
                if w not in seen:
                    seen.add(w); stack.append(w)
        comps.append(len(comp))
    comps.sort(reverse=True)

    edge_total = n_inv + n_sh
    density = 2.0 * edge_total / (len(nodes) * (len(nodes) - 1)) if len(nodes) > 1 else None

    out = {
        "metric_id": "M_SVC_DEEP_173_1",
        "metric_name": "服务关系链模型",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": ("三维（强度/层次/密度）在「资本纽带」代理图上均可算，但正式合作边、"
                            "交易合同边、信用评分表在 gkx 无源（待建 svc_coop_edge / svc_trade_contract / "
                            "svc_credit_score），强度维只能由投资/股东事件 + 失信处罚反向代理 → 部分支持"),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_invest_info", "rows": f["invest_meta"]["rows_total"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_shareholder_info", "rows": f["shareholder_meta"]["rows_total"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_risk_shixin / dwd_org_company_punish",
             "rows": 142032, "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("本件是截面图模型，不涉年度序列；投资/股东表未带可靠业务年份，"
                            "故不设基期，也不做同比——避免把「采集时点快照」伪装成年度序列"),
        "graph": {
            "nodes_in_pool": len(pool),
            "nodes_with_degree": len(nodes),
            "edges_internal": edge_total,
            "edges_invest": n_inv, "edges_shareholder": n_sh,
            "edges_dropped_shareholder_no_partner": f["shareholder_meta"]["rows_total"] - len([1 for a, b in f["shareholder_edges"] if b]),
            "degree_mean": round(statistics.mean(deg.values()), 4) if deg else None,
            "degree_median": statistics.median(deg.values()) if deg else None,
            "degree_max": max(deg.values()) if deg else None,
            "density": round(density, 8) if density else None,
            "components": len(comps),
            "largest_component": comps[0] if comps else 0,
            "isolated_nodes": len(pool) - len(nodes),
        },
        "dimensions": {
            "关系强度": {"n": len(s_strength), "inputs": ["频次", "投资金额", "失信处罚反向"]},
            "关系层次": {"n": len(s_level), "inputs": ["一阶度", "二阶可达"]},
            "关系密度": {"n": len(s_density), "inputs": ["局部聚类系数（度>=2）"]},
        },
        "index": {"n": len(idx), "mean": round(statistics.mean(vals), 2) if vals else None,
                  "median": round(statistics.median(vals), 2) if vals else None,
                  "max": round(vals[-1], 2) if vals else None, "min": round(vals[0], 2) if vals else None},
        "top10": top,
        "missing_edges": {
            "coop": "svc_coop_edge（联合申报、联合中标、共同研发）—— gkx 无联合申报/中标表",
            "trade": "svc_trade_contract（服务合同金额与频次）—— gkx 无合同/发票类表",
            "credit": "svc_credit_score（信用评分）—— 只有失信/处罚二元事件，无评分",
            "talent": "人才流动边 —— 无任职变动表",
        },
        "compute": {"elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("内部边", edge_total, "(投资", n_inv, "股东", n_sh, ") 有度节点", len(nodes),
          "最大分量", comps[0] if comps else 0, "密度", round(density, 8) if density else None)
    print("指数 均/中位/最大", out["index"]["mean"], out["index"]["median"], out["index"]["max"])
    print("top1", top[0] if top else None)
    print("->", OUT)


if __name__ == "__main__":
    main()
