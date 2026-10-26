#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""服务网络密度（M_SVC_GRAPH_DENSITY）—— gkx 口径，自包含。

口径（侯佳伟 2026-08-21 标准图论密度，公式照抄）：
    D = 2|E| / (|N| × (|N| − 1))
    两个分母口径并列：全池 N=44,153（生态位覆盖率）、活跃子网 N=12,905（参与者紧密度）
    分母 |N|(|N|−1)/2 为无向简单图的可能边数；|N| < 2 时不输出。

口径裁决（沿用 Q-SVCCHAIN-03 会签结论）：
    「服务网络密度」的边**不算**投资/股东边。因此本件算出的密度只能以
    「资本纽带密度（代理）」身份披露，不能宣称是正式服务网络密度；
    正式语义需要合作/交易/人才流动边，gkx 无承载表。

数据源：code/_snapshots21/svc21_facts_20261022.json
产出：code/M_SVC_GRAPH_DENSITY_out.json
运行：cd code && python3 M_SVC_GRAPH_DENSITY.py
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
OUT = os.path.join(HERE, "M_SVC_GRAPH_DENSITY_out.json")


def density(E, N):
    if N is None or N < 2:
        return None
    return 2.0 * E / (N * (N - 1))


def sci(x):
    return None if x is None else float("%.4e" % x)


def main():
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    pool, inv, sh = f["pool"], f["invest_edges"], f["shareholder_edges"]
    ids = set(pool)
    N = len(ids)

    # ---- 主口径边集（两类合并、去重、去自环）-----------------------------------
    pairs, only_inv, only_sh, empty = set(), set(), set(), 0
    for e in inv:
        a, b = e[0], e[1]
        if not b:
            empty += 1
            continue
        if a in ids and b in ids and a != b:
            pairs.add(tuple(sorted((a, b))))
            only_inv.add(tuple(sorted((a, b))))
    for e in sh:
        a, b = e[0], e[1]
        if not b:
            empty += 1
            continue
        if a in ids and b in ids and a != b:
            pairs.add(tuple(sorted((a, b))))
            only_sh.add(tuple(sorted((a, b))))

    deg = Counter()
    for a, b in pairs:
        deg[a] += 1
        deg[b] += 1
    n_act = len(deg)
    E = len(pairs)

    D_pool = density(E, N)
    D_act = density(E, n_act)

    # ---- 口径敏感度：单类边、以及含无向重复计数的宽松口径 ----------------------
    # 实测：投资边的节点对几乎全部同时出现在股东表里（同一笔资本关系两边各记一次），
    # 因此「只算投资边」的独立贡献为 0 条——这不是取数 bug，写进 sensitivity 一并披露。
    D_inv_only = density(len(only_inv - only_sh), N)
    D_sh_only = density(len(only_sh - only_inv), N)
    # 宽松口径：不做无向去重，投资 + 股东两边各计一条（用于说明「口径差 1 倍量级在哪」）
    raw = 0
    for e in inv:
        if e[1] and e[0] in ids and e[1] in ids and e[0] != e[1]:
            raw += 1
    for e in sh:
        if e[1] and e[0] in ids and e[1] in ids and e[0] != e[1]:
            raw += 1
    D_raw = density(raw, N)

    # ---- 可能边数与实际占比 -------------------------------------------------------
    possible = N * (N - 1) / 2
    realized_pct = 100.0 * E / possible

    reason = ("代理密度可现转（全池 %.3e / 活跃子网 %.3e），结构与计算链完整；"
              "但会签口径 Q-SVCCHAIN-03 明确「服务网络密度的边不算投资/股东」，"
              "正式服务关系边在 gkx 无承载表，始终有一维缺正式数据，故落部分支持。"
              % (D_pool, D_act))

    out = {
        "metric_id": "M_SVC_GRAPH_DENSITY",
        "metric_name": "服务网络密度",
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
        "base_years_note": ("密度是截面量（快照时点存量边），不做年度序列；"
                            "库内边表无「关系生效年」字段，按年拆边会把存量关系误摊成流量，故不拆。"),
        "formula": "D = 2|E| / (|N| * (|N| - 1))",
        "main": {
            "edge_set": "投资边 ∪ 机构股东边（双端在池、无向去重、去自环）",
            "E": E,
            "N_pool": N,
            "N_active": n_act,
            "possible_edges_pool": round(possible, 1),
            "realized_share_pct": round(realized_pct, 8),
            "density_pool": sci(D_pool),
            "density_active": sci(D_act),
            "density_pool_raw": D_pool,
            "density_active_raw": D_act,
        },
        "sensitivity": {
            "invest_pairs": len(only_inv),
            "shareholder_pairs": len(only_sh),
            "overlap_pairs": len(only_inv & only_sh),
            "invest_edges_only": {"E": len(only_inv - only_sh), "density_pool": sci(D_inv_only),
                                  "note": "投资边的节点对 %d 条中 %d 条同时出现在股东表，"
                                          "独立贡献为 0 条——同一笔资本关系两表各记一次所致，"
                                          "须按无向去重合并，不能相加"
                                          % (len(only_inv), len(only_inv & only_sh))},
            "shareholder_edges_only": {"E": len(only_sh - only_inv), "density_pool": sci(D_sh_only)},
            "no_undirected_dedup": {"E": raw, "density_pool": sci(D_raw),
                                    "note": "同一对机构在两表各出现一次即计两条，仅用于说明口径敏感度"},
            "empty_counterpart_rows": empty,
        },
        "caliber_ruling": {
            "code": "Q-SVCCHAIN-03",
            "ruling": "服务网络密度的边不算投资/股东",
            "consequence": "本件数值只能以「资本纽带密度（代理）」身份披露，不得宣称正式服务网络密度",
        },
        "compute": {"elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("E=%d N_pool=%d N_act=%d" % (E, N, n_act))
    print("D(全池)=%.6e  D(活跃)=%.6e" % (D_pool, D_act))
    print("可能边 %.3e，实现占比 %.8f%%" % (possible, realized_pct))
    print("敏感度：单投资 %.4e / 单股东 %.4e / 不去重 %.4e" % (D_inv_only, D_sh_only, D_raw))
    print("->", OUT)


if __name__ == "__main__":
    main()
