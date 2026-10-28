#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""服务机构实体关系抽取（M_SVC_GRAPH_113_1）—— gkx 口径，自包含。

口径（旧稿公式照抄，数据源整体换到 gkx）：
    节点域   = M_SVC_GRAPH_112_1 同源的圈定池 org_id 集合（本脚本内联重建，不 import 112）；
    边集     = 投资边 dwd_org_invest_info(org_id → inv_org_id)
             ∪ 机构股东边 dwd_org_shareholder_info(org_id ← inv_org_id)；
    口径规则 = 双端在池 / 无向去重 / 去自环 / 对端为空（自然人股东）剔除并单独计数。

与旧稿的差异：
    旧稿边集来自 demo 侧同为 dwd 的两张表（46,967 / 400,286 行，与 gkx 同行数），
    本件在 gkx 上重抽，读数因此不应有量级差；真正变的是「池」——旧稿池是物化表
    43,296 家，本件池是 44,153 家（口径改为经营范围命中，见 112 §2.2）。

数据源：code/_snapshots21/svc21_facts_20261022.json
产出：code/M_SVC_GRAPH_113_1_out.json
运行：cd code && python3 M_SVC_GRAPH_113_1.py
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
OUT = os.path.join(HERE, "M_SVC_GRAPH_113_1_out.json")


def q(vals, p):
    """分位数（最近秩法），用于度分布的 p90/p99 读数。"""
    if not vals:
        return None
    xs = sorted(vals)
    k = min(len(xs) - 1, max(0, int(round(p * (len(xs) - 1)))))
    return xs[k]


def main():
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    pool = f["pool"]
    inv = f["invest_edges"]
    sh = f["shareholder_edges"]
    im = f.get("invest_meta") or {}
    sm = f.get("shareholder_meta") or {}
    su = f.get("subsidiary_edges") or []
    sum_meta = f.get("subsidiary_meta") or {}
    ids = set(pool)
    n = len(ids)

    # ---- 步骤 1：单类边的两端在池判定 -------------------------------------------
    inv_in, inv_empty = 0, 0
    sh_in, sh_empty = 0, 0
    pairs_inv, pairs_sh = set(), set()
    self_loop = 0
    for e in inv:
        a, b = e[0], e[1]
        if not b:
            inv_empty += 1
            continue
        if a in ids and b in ids:
            if a == b:
                self_loop += 1
                continue
            inv_in += 1
            pairs_inv.add(tuple(sorted((a, b))))
    for e in sh:
        a, b = e[0], e[1]
        if not b:
            sh_empty += 1
            continue
        if a in ids and b in ids:
            if a == b:
                self_loop += 1
                continue
            sh_in += 1
            pairs_sh.add(tuple(sorted((a, b))))

    # ---- 步骤 2：合并去重（无向）与双类共现 -------------------------------------
    allpairs = pairs_inv | pairs_sh
    both = pairs_inv & pairs_sh
    only_inv = pairs_inv - pairs_sh
    only_sh = pairs_sh - pairs_inv

    # ---- 步骤 3：度分布与枢纽 -----------------------------------------------------
    deg = Counter()
    for a, b in allpairs:
        deg[a] += 1
        deg[b] += 1
    dvals = list(deg.values())
    top = sorted(deg.items(), key=lambda x: (-x[1], x[0]))[:10]
    top_named = [{"org_id": o, "name": pool[o]["name"], "type": pool[o].get("ptype2"),
                  "city": pool[o].get("city"), "degree": d} for o, d in top]

    # ---- 步骤 4：连通结构 ---------------------------------------------------------
    adj = {}
    for a, b in allpairs:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    seen, comps = set(), []
    for s in adj:
        if s in seen:
            continue
        stack = [s]
        seen.add(s)
        cnt = 0
        while stack:
            x = stack.pop()
            cnt += 1
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        comps.append(cnt)
    comps.sort(reverse=True)

    # ---- 步骤 5：需求点名的关系类型覆盖 -------------------------------------------
    required = ["服务类型", "服务内容", "服务范围", "合作伙伴", "客户", "资本纽带(投资/股东)"]
    covered = {"资本纽带(投资/股东)": "已抽（本件）"}
    missing_types = [r for r in required if r not in covered]

    reason = ("资本纽带边（投资 + 机构股东）双端在池 %d 条、覆盖 %d 个节点，可现转；"
              "但需求点名的服务类型/服务内容/服务范围/合作伙伴/客户五类语义边在 gkx 无承载表"
              "（子公司表双端在池 0 条），多元关系仅落地一类，故落部分支持。"
              % (len(allpairs), len(deg)))

    out = {
        "metric_id": "M_SVC_GRAPH_113_1",
        "metric_name": "服务机构实体关系抽取",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": reason,
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_invest_info", "rows": im.get("rows_total"),
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_shareholder_info", "rows": sm.get("rows_total"),
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_subsidiary_info", "rows": sum_meta.get("rows_total"),
             "note": "双端在池边 0 条（对端 org_id 与底册 org_id 不同码域），不作边源",
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
        ],
        "base_years_used": [2026],
        "base_years_missing": [],
        "base_years_note": ("关系抽取为截面件（边集为快照时点的存量关系），不做年度序列；"
                            "投资金额字段存在但非本件合成输入，未按年折算。"),
        "population": {"node_domain": n},
        "edges": {
            "invest_rows_touching_pool": len(inv),
            "invest_internal_raw": inv_in,
            "invest_unique_pairs": len(pairs_inv),
            "invest_empty_counterpart": inv_empty,
            "shareholder_rows_touching_pool": len(sh),
            "shareholder_internal_raw": sh_in,
            "shareholder_unique_pairs": len(pairs_sh),
            "shareholder_empty_counterpart": sh_empty,
            "self_loop_dropped": self_loop,
            "internal_unique_pairs": len(allpairs),
            "both_types": len(both),
            "only_invest": len(only_inv),
            "only_shareholder": len(only_sh),
            "share_of_domain_pct": round(100.0 * len(deg) / n, 2),
        },
        "degree": {
            "nodes_with_degree": len(deg),
            "mean": round(statistics.mean(dvals), 4),
            "median": q(dvals, 0.5),
            "p90": q(dvals, 0.90),
            "p99": q(dvals, 0.99),
            "max": max(dvals),
            "top10": top_named,
        },
        "components": {"count": len(comps), "top_sizes": comps[:8],
                       "giant_share_of_domain_pct": round(100.0 * comps[0] / n, 2)},
        "relation_types": {"required": required, "covered": list(covered),
                           "missing": missing_types},
        "compute": {"elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("节点域", n, "内部边", len(allpairs), "有度节点", len(deg),
          "巨型分量", comps[0])
    print("投资内部", inv_in, "股东内部", sh_in, "双类共现", len(both))
    print("度 median/p99/max", out["degree"]["median"], out["degree"]["p99"],
          out["degree"]["max"])
    print("top1", top_named[0]["name"], top_named[0]["degree"])
    print("->", OUT)


if __name__ == "__main__":
    main()
