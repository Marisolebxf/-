#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""产业链全景模型构建（M_CHAIN_DEEP_117_1）—— 树 + 企业挂接，自包含。

口径（三步构建法）：
    ① 节点层：链树 1,273 个 industry_code 作为全景节点，父子边 = 末 2 位去尾；
    ② 实体层：2,283,762 行标签把企业挂到叶级环节；
    ③ 汇总层：逐链输出节点数、边数、可挂接实体数、叶级覆盖率。
缺口：关系边只有「父子」一种，没有跨环节的供应/合作/技术流边（gkx 无此源），
    故本模型是「结构全景」而非「关系全景」。

产物：chains[].value = 该链全景子图节点数；edges/entities/leaf_coverage 分列。


运行：cd code && python3 M_CHAIN_DEEP_117_1.py
产物：code/M_CHAIN_DEEP_117_1_out.json（覆盖写）
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_DEEP_117_1_out.json")

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
    edges = 0
    codes = {r["industry_code"] for r in tree}
    for r in tree:
        c = r["industry_code"]
        if len(c) > 7 and c[:-2] in codes:
            edges += 1
    rows = []
    for c in chains:
        lf = c.get("leaf_firms") or {}
        ent = sum(lf.values())
        rows.append({"chain": c["chain"], "name": c["name"], "value": c["nodes_total"],
                     "edges": c["nodes_total"] - 1,
                     "entities": ent, "covered_leaves": len(lf),
                     "leaf_coverage": round(len(lf) / c["leaves"], 4) if c["leaves"] else None,
                     "nonleaf": c["nodes_nonleaf"], "leaves": c["leaves"], "l1": c["l1_count"]})
    rows.sort(key=lambda r: -r["value"])
    headline = {"value": panel["tree"]["nodes"], "unit": "个全景节点",
                "edges": panel["tree"]["edges"], "chains": len(rows),
                "entities": sum(r["entities"] for r in rows),
                "leaf_coverage": round(sum(r["covered_leaves"] for r in rows) / sum(r["leaves"] for r in rows), 4),
                "edge_types": 1}
    facts = [
        {"label": "全景节点", "value": panel["tree"]["nodes"]},
        {"label": "父子边", "value": panel["tree"]["edges"]},
        {"label": "挂接企业（含多环节）", "value": headline["entities"]},
        {"label": "叶级覆盖率", "value": headline["leaf_coverage"]},
        {"label": "边类型数", "value": "1（仅父子，无跨环节关系边）"},
    ]
    population = {"defined_as": "链树节点 + 标签表企业挂接",
                  "nodes": panel["tree"]["nodes"], "edges": panel["tree"]["edges"]}
    compute = {"formula": "nodes=COUNT(industry_code); edges=COUNT(parent-child); entities=COUNT(firm-leaf)",
               "edge_types": ["parent-child"], "missing_edges": ["供应", "合作", "技术流"]}
    STEPS = ["读链树，按末 2 位去尾建立父子边", "按链切子图并统计节点/边",
             "读标签表叶级企业数作为实体挂接", "算叶级覆盖率", "标注：仅结构边，无跨环节关系边"]
    out = {
        "metric_id": "M_CHAIN_DEEP_117_1",
        "metric_name": "产业链全景模型构建",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": '全景子图可由链树 + 标签表端到端构建（1,273 节点、1,261 条父子边、叶级覆盖 96.0%）；但边只有父子一种，跨环节的供应/合作/技术流边在 gkx 无源，图谱只能作结构全景。',
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
    print("[ok]", "M_CHAIN_DEEP_117_1", json.dumps(headline, ensure_ascii=False),
          "chains", len(rows), "sec", round(time.time() - t0, 2))


if __name__ == "__main__":
    main()
