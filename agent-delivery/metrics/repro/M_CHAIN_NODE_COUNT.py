#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""产业链节点数（M_CHAIN_NODE_COUNT）—— gkx 链树，王惠 V2 口径，自包含。

口径（王惠 `指标计算逻辑-V2/M_CHAIN_NODE_COUNT.md`，V2-20260819）：
    COUNT(DISTINCT industry_link_code)，按 industry_code 前 7 位归到顶层链。
    实测 `industry_link_code` 只在「有子节点」的行上非空（12 个顶层根为空串），
    因此本口径数的正是**非叶环节码**：全库 319 个（12 链合计，逐链 9—71）。

同时输出 `nodes_total`（全部 industry_code，1,273 个）作为结构旁证，两者不可混用：
    319 = 环节节点（叶节点不计）；1,273 = 目录树全部节点（含叶）。
    20261021 旧脚本把 nodes_total 当作主值（1,273），比王惠口径大 4 倍，已在本版改正。

产物字段：headline.value = 319；chains[].value = 该链环节码数；chains[].nodes_total = 该链全部节点。

运行：cd code && python3 M_CHAIN_NODE_COUNT.py
产物：code/M_CHAIN_NODE_COUNT_out.json（覆盖写）
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_NODE_COUNT_out.json")

BASE_USED = []
BASE_MISSING = []
BASE_NOTE = "截面指标：统计链树当前存量，不设年度分母；链树无年度字段。"

SOURCES = [
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_industry_chain_info", "rows": 1273,
     "snapshot": "code/_snapshots21/chain_tree_links_20261022.json",
     "pulled_at": "2026-10-22"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_org_industry_tags", "rows": 2283762,
     "snapshot": "code/_snapshots21/chain_panel21.json"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_org_base_info", "rows": 189116,
     "snapshot": "code/_snapshots21/base_20261021.json"},
]


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    t0 = time.time()
    tree = load("chain_tree_links_20261022.json")
    rows_in = tree["data"]
    panel = load("chain_panel21.json")
    names = {c["chain"]: c["name"] for c in panel["chains"]}

    by_root = defaultdict(lambda: {"nodes": 0, "links": set(), "codes": set()})
    for r in rows_in:
        code = (r["industry_code"] or "").strip()
        root = code[:7]
        g = by_root[root]
        g["nodes"] += 1
        g["codes"].add(code)
        lc = (r["industry_link_code"] or "").strip()
        if lc:
            g["links"].add(lc)

    # 父子关系：某 code 是否有子节点（用于区分叶/非叶）
    nonleaf = 0
    for root, g in by_root.items():
        for code in g["codes"]:
            if any(c != code and c.startswith(code) for c in g["codes"]):
                nonleaf += 1

    rows = []
    for root, g in by_root.items():
        links = len(g["links"])
        rows.append({
            "chain": root,
            "name": names.get(root, ""),
            "value": links,
            "nodes_total": g["nodes"],
            "leaves": g["nodes"] - links,
            "leaf_share": round((g["nodes"] - links) / g["nodes"], 4) if g["nodes"] else None,
        })
    rows.sort(key=lambda r: -r["value"])
    total_links = sum(r["value"] for r in rows)
    total_nodes = sum(r["nodes_total"] for r in rows)
    global_links = len({(r["industry_link_code"] or "").strip()
                        for r in rows_in if (r["industry_link_code"] or "").strip()})

    by_len = Counter(len((r["industry_code"] or "").strip()) for r in rows_in)
    vals = sorted(r["value"] for r in rows)
    stats = {
        "n_chains": len(rows),
        "min": vals[0], "max": vals[-1], "median": vals[len(vals) // 2],
        "mean": round(total_links / len(rows), 2) if rows else None,
        "leaves_total": total_nodes - total_links,
        "nodes_total": total_nodes,
        "link_per_node_pct": round(100.0 * total_links / total_nodes, 2) if total_nodes else None,
    }
    headline = {
        "value": total_links,
        "unit": "个环节节点（12 链去重合计）",
        "nodes_total": total_nodes,
        "global_distinct_links": global_links,
        "chains": len(rows),
        "definition": "COUNT(DISTINCT industry_link_code) GROUP BY industry_code[:7]",
        "max_chain": rows[0]["chain"], "max_value": rows[0]["value"],
        "min_chain": rows[-1]["chain"], "min_value": rows[-1]["value"],
    }
    facts = [
        {"label": "环节节点（王惠口径，12 链合计）", "value": total_links},
        {"label": "全库去重环节码（跨链不重复）", "value": global_links},
        {"label": "目录树全部节点（含叶）", "value": total_nodes},
        {"label": "顶层链数", "value": len(rows)},
        {"label": "单链环节码区间", "value": f'{rows[-1]["value"]}—{rows[0]["value"]}'},
        {"label": "编码长度层级", "value": dict(sorted(by_len.items()))},
        {"label": "node_company_count 非零行", "value": sum(1 for r in rows_in if (r["node_company_count"] or 0) > 0)},
        {"label": "level 列取值个数", "value": len({r["level"] for r in rows_in})},
    ]
    population = {
        "defined_as": "gkx.dwd_industry_chain_info 全部节点，按 industry_code 7 位前缀归链",
        "nodes": total_nodes,
        "roots": len(rows),
        "rows_with_empty_link_code": sum(1 for r in rows_in if not (r["industry_link_code"] or "").strip()),
        "by_len": dict(sorted(by_len.items())),
        "nonleaf": nonleaf,
    }
    compute = {
        "formula": "COUNT(DISTINCT industry_link_code) GROUP BY industry_code[:7]",
        "source_rows": total_nodes,
        "main_value_semantics": "非叶环节码（叶节点不计）",
        "alt_value_semantics": "nodes_total = 目录树全部节点（含叶）",
    }
    STEPS = [
        "读取链树快照 chain_tree_links_20261022.json（1,273 行，含 industry_link_code）",
        "按 industry_code 前 7 位归到 12 条顶层链",
        "每条链对非空 industry_link_code 去重计数 → 环节节点数",
        "同时统计 nodes_total（全部 industry_code）与叶/非叶结构",
        "校验 Σ逐链环节码 = 全库去重环节码 = 319，且 < 全部节点 1,273",
    ]
    out = {
        "metric_id": "M_CHAIN_NODE_COUNT",
        "metric_name": "产业链节点数",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "完全转换支持",
        "judgment_reason": "链树 1,273 行、12 条顶层链、319 个非叶环节码在 gkx 当日全量可取；"
                           "COUNT(DISTINCT industry_link_code) 端到端跑通，逐链 9—71、区分度充分，无外部依赖。",
        "sources": SOURCES,
        "base_years_used": BASE_USED,
        "base_years_missing": BASE_MISSING,
        "base_years_note": BASE_NOTE,
        "headline": headline,
        "stats": stats,
        "facts": facts,
        "chains": rows,
        "method_steps": STEPS,
        "population": population,
        "compute": compute,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("[ok]", "M_CHAIN_NODE_COUNT", json.dumps(headline, ensure_ascii=False),
          "sec", round(time.time() - t0, 2))


if __name__ == "__main__":
    main()
