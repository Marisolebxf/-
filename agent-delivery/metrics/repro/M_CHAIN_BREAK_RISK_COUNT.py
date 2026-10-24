#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""产业链断链风险数（M_CHAIN_BREAK_RISK_COUNT）—— 环节空位计数，自包含。

口径：断链风险 = 该链叶级环节中「链内企业数为 0」的环节个数。
    叶级环节来自链树（长度最深的节点），企业命中来自 2,283,762 行标签的 link 码。
这是结构空位，不是供应链断供风险：真正的断供要看上下游交易关系，gkx 没有。

产物：chains[].value = 空位环节数；gap_share = 空位/叶数；gap_examples 前 5 个空位名。


运行：cd code && python3 M_CHAIN_BREAK_RISK_COUNT.py
产物：code/M_CHAIN_BREAK_RISK_COUNT_out.json（覆盖写）
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_BREAK_RISK_COUNT_out.json")

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
    rows = []
    for c in chains:
        lf = c.get("leaf_firms") or {}
        leaves = c["leaves"]
        gaps = [x for x in c["leaf_codes"] if x not in lf]
        names = c.get("leaf_names") or {}
        rows.append({"chain": c["chain"], "name": c["name"], "value": len(gaps),
                     "gap_share": round(len(gaps) / leaves, 4) if leaves else None,
                     "leaves": leaves, "covered": len(lf),
                     "gap_examples": [names.get(x, x) for x in gaps[:5]],
                     "nonleaf": None, "l1": None})
    rows.sort(key=lambda r: -r["value"])
    headline = {"value": sum(r["value"] for r in rows), "unit": "个空位环节",
                "leaves": sum(r["leaves"] for r in rows),
                "gap_share": round(sum(r["value"] for r in rows) / sum(r["leaves"] for r in rows), 4),
                "zero_gap_chains": [r["chain"] for r in rows if r["value"] == 0]}
    facts = [
        {"label": "空位环节合计", "value": headline["value"]},
        {"label": "全部叶级环节", "value": headline["leaves"]},
        {"label": "整体空位率", "value": headline["gap_share"]},
        {"label": "空位最多链", "value": f'{rows[0]["name"]} {rows[0]["value"]}'},
        {"label": "无空位链", "value": "、".join(headline["zero_gap_chains"]) or "无"},
        {"label": "标签表行数", "value": panel["meta"]["rows_scanned"]},
        {"label": "无环节码行", "value": load("chain_stage_leaf_20261021.json")["empty_rows"]},
        {"label": "有环节码行（链级企业合计）", "value": sum(c["firms"] for c in chains)},
        {"label": "叶级企业合计", "value": sum(sum((c.get("leaf_firms") or {}).values()) for c in chains)},
    ]
    population = {"defined_as": "链树叶级环节 × 标签表叶级企业命中",
                  "leaves": headline["leaves"], "gaps": headline["value"]}
    compute = {"formula": "COUNT(leaf WHERE firm_count=0)",
               "gap_share": headline["gap_share"],
               "scope": "结构空位，不含供应链断供"}
    STEPS = ["读链树叶级环节清单", "读标签表叶级企业数", "逐链取企业数为 0 的环节",
             "统计空位数与空位率，列前 5 个空位名", "标注：结构空位≠供应链断供"]
    out = {
        "metric_id": "M_CHAIN_BREAK_RISK_COUNT",
        "metric_name": "产业链断链风险数",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": '环节空位可用链树 + 标签现算，整体空位率 3.98%；但语义只能是「没有企业挂接的环节」，不是供应链断供风险，后者需要上下游交易关系。',
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
    print("[ok]", "M_CHAIN_BREAK_RISK_COUNT", json.dumps(headline, ensure_ascii=False),
          "chains", len(rows), "sec", round(time.time() - t0, 2))


if __name__ == "__main__":
    main()
