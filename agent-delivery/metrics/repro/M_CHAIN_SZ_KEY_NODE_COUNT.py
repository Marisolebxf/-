#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""深圳关键节点数（M_CHAIN_SZ_KEY_NODE_COUNT）—— 深圳集聚度代理，自包含。

口径：与全国版同一门槛规则（该链叶级企业数中位数），分子换成「深圳有企业」的环节。
    这样全国值与深圳值可直接相减，得到「深圳缺口环节」，避免两个口径各算一套。

产物：headline = 深圳关键环节数；chains[].value；attach_rate = 深圳关键环节/全国关键环节。


运行：cd code && python3 M_CHAIN_SZ_KEY_NODE_COUNT.py
产物：code/M_CHAIN_SZ_KEY_NODE_COUNT_out.json（覆盖写）
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_SZ_KEY_NODE_COUNT_out.json")

BASE_USED = []
BASE_MISSING = []
BASE_NOTE = '截面指标：统计当前存量，不设年度分母。'

SOURCES = [
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
      "table": "gkx.dwd_org_industry_tags", "rows": 2283762,
      "snapshot": "code/_snapshots21/chain_panel21.json"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
      "table": "gkx.dwd_industry_chain_info", "rows": 1273,
      "snapshot": "code/_snapshots21/chain_tree_20261021.json"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
      "table": "gkx.dwd_org_base_info", "rows": 189116,
      "snapshot": "code/_snapshots21/base_20261021.json"},
]


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    t0 = time.time()
    panel = load("chain_panel21.json")
    chains = panel["chains"]
    tree = load("chain_tree_20261021.json")
    import statistics
    rows = []
    for c in chains:
        lf = c.get("leaf_firms") or {}
        sz = c.get("leaf_sz") or {}
        vals = sorted(lf.values())
        med = statistics.median(vals) if vals else 0
        keys_nat = [k for k, v in lf.items() if med and v >= med]
        keys_sz = [k for k in keys_nat if sz.get(k, 0) > 0]
        rows.append({"chain": c["chain"], "name": c["name"], "value": len(keys_sz),
                     "national": len(keys_nat), "threshold": med,
                     "attach_rate": round(len(keys_sz) / len(keys_nat), 4) if keys_nat else None,
                     "nonleaf": None, "leaves": c["leaves"], "l1": None})
    rows.sort(key=lambda r: -r["value"])
    tn = sum(r["national"] for r in rows); ts = sum(r["value"] for r in rows)
    headline = {"value": ts, "unit": "个深圳关键环节（集聚度代理）",
                "national": tn, "attach_rate": round(ts / tn, 4) if tn else None,
                "rule": "全国关键环节中深圳有企业的部分"}
    facts = [
        {"label": "全国关键环节", "value": tn},
        {"label": "深圳关键环节", "value": ts},
        {"label": "深圳承接率", "value": headline["attach_rate"]},
        {"label": "深圳关键环节最多链", "value": f'{rows[0]["name"]} {rows[0]["value"]}'},
        {"label": "深圳零关键环节链", "value": sum(1 for r in rows if r["value"] == 0)},
    ]
    population = {"defined_as": "全国关键环节 × 深圳叶级企业命中",
                  "national": tn, "sz": ts}
    compute = {"formula": "COUNT(leaf WHERE firm_count>=median AND sz_firm_count>0)",
               "proxy": True}
    STEPS = ["读链面板的叶级全国/深圳企业数", "沿用全国版中位数门槛",
             "筛深圳有企业的关键环节", "算深圳承接率"]
    out = {
        "metric_id": "M_CHAIN_SZ_KEY_NODE_COUNT",
        "metric_name": "深圳关键节点数",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": '深圳关键环节可由标签表的深圳切片直接现算；但门槛仍是集聚度代理，且深圳切片按主档城市判定，跨市注册的深圳企业在库内不可追。',
        "sources": SOURCES,
        "base_years_used": BASE_USED,
        "base_years_missing": BASE_MISSING,
        "base_years_note": BASE_NOTE,
        "headline": headline,
        "facts": facts,
        "chains": rows,
        "method_steps": STEPS,
        "population": population,
        "compute": compute,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("[ok]", "M_CHAIN_SZ_KEY_NODE_COUNT", json.dumps(headline, ensure_ascii=False),
          "chains", len(rows), "sec", round(time.time() - t0, 2))


if __name__ == "__main__":
    main()
