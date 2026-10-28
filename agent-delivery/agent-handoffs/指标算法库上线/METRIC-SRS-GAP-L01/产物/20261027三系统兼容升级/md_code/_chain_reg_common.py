#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CHAIN 区域族（REG-*）共享计算库（20261021）

统一读取 4 份本地缓存（均由 `_chain_reg_panel_ods.py` / `_chain_reg_patent_build.py` /
`_chain_reg_small_pull.py` 一次性拉取后落盘；拉取时走的是三方 gkx 的只读镜像库，
行数与 gkx 一致，来源与口径见 DATA_FACTS_gkx21.md §3.21），供 5 个区域指标脚本复用：

  chain_reg_panel_20261021.json    链×城 企业面板、环节码分布、企业—链归属、学术底册命中
  chain_reg_patent_20261021.json   2,939,895 件专利的链×城普查归集
  chain_reg_small_20261021.json    主档 org 映射、年报、上市财务、融资、投资、学者、论文关联

口径常量：REGION_AXIS（4 市）、CHAIN_AXIS（12 条顶层链）、STAT_YEAR（统计年 2025，
专利按王惠口径取申请年 ≤2024）。
"""
from __future__ import annotations

import json
import statistics
from collections import defaultdict
from pathlib import Path

SNAP = Path(__file__).parent / "_snapshots"
CITY4 = ["深圳市", "广州市", "东莞市", "惠州市"]
CHAIN_AXIS = ["INB1306", "INB1309", "INB1333", "INB1502", "INB2505",
              "INB1204", "INB1303", "INB1323", "INB1354", "INB1209", "INB1236", "INB2503"]
STAT_YEAR = 2025
PAT_CUTOFF = 2024


def _load(name):
    return json.loads((SNAP / name).read_text())


def load_panel():
    return _load("chain_reg_panel_20261021.json")


def load_patent():
    return _load("chain_reg_patent_20261021.json")


def load_small():
    return _load("chain_reg_small_20261021.json")


def load_tree():
    """链树 code -> {name, link}（1,273 节点）"""
    snap = _load("chain_h_agg_20261021.json")
    return {k: {"name": v["name"], "link": (v.get("link") or "").strip()} for k, v in snap["chains"].items()}


def l1_index(tree):
    """任意环节码 -> 其所属 L1 环节码（链码长度 9 且父为根链）；无法归一返回 None"""
    idx = {}
    for code in tree:
        cur, seen = code, 0
        found = None
        while cur and seen < 12:
            p = tree.get(cur, {}).get("link")
            if len(cur) == 9 and p and len(p) == 7:
                found = cur
                break
            if not p:
                break
            cur = p
            seen += 1
        idx[code] = found
    return idx


def chain_name_map(panel):
    return {k: v for k, v in panel["roots"].items()}


def stats(vals):
    vals = [v for v in vals if v is not None]
    if not vals:
        return {"n": 0}
    vals_sorted = sorted(vals)
    n = len(vals_sorted)
    return {
        "n": n,
        "min": round(min(vals), 4), "max": round(max(vals), 4),
        "mean": round(sum(vals) / n, 4),
        "median": round(statistics.median(vals_sorted), 4),
        "p90": round(vals_sorted[int(0.9 * (n - 1))], 4),
        "n_zero": sum(1 for v in vals if v == 0),
        "n_distinct": len(set(round(v, 6) for v in vals)),
    }


def panel_matrix(chain_city, chains=None, cities=None, default=0):
    """{chain:{city:v}} -> 二维表（list of dict）"""
    chains = chains or CHAIN_AXIS
    cities = cities or CITY4
    rows = []
    for ch in chains:
        r = {"chain": ch, "city": {c: (chain_city.get(ch, {}) or {}).get(c, default) for c in cities}}
        r["total"] = sum(r["city"].values())
        rows.append(r)
    return rows


def chain_totals(chain_city, chains=None, cities=None):
    chains = chains or CHAIN_AXIS
    cities = cities or CITY4
    return {ch: sum((chain_city.get(ch, {}) or {}).get(c, 0) for c in cities) for ch in chains}


def write_out(metric_id, payload):
    path = Path(__file__).parent / f"{metric_id}_out.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", path)
    return path
