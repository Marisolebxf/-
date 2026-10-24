#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""产业集中度（M_CHAIN_CONCENTRATION_INDEX）—— 环节份额 HHI，自包含。

口径：以「环节」为市场参与者，用链内各叶级环节的企业数份额算 HHI：
    HHI = Σ (firm_i / firm_total)^2，取值 1/n—1；另给首位环节份额 CR1 与等效环节数 1/HHI。
这是结构集中度（企业数份额），不是营收/市值份额：gkx 无环节级营收，份额只能按家数。

产物：chains[].value = HHI；cr1、eff_n、covered_leaves。


运行：cd code && python3 M_CHAIN_CONCENTRATION_INDEX.py
产物：code/M_CHAIN_CONCENTRATION_INDEX_out.json（覆盖写）
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_CONCENTRATION_INDEX_out.json")

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
        tot = sum(lf.values())
        hhi = sum((v / tot) ** 2 for v in lf.values()) if tot else None
        top = max(lf.items(), key=lambda kv: kv[1]) if lf else ("", 0)
        rows.append({"chain": c["chain"], "name": c["name"],
                     "value": round(hhi, 6) if hhi is not None else None,
                     "cr1": round(top[1] / tot, 4) if tot else None,
                     "top_leaf": c.get("leaf_names", {}).get(top[0], top[0]),
                     "eff_n": round(1 / hhi, 2) if hhi else None,
                     "covered_leaves": len(lf),
                     "nonleaf": None, "leaves": c["leaves"], "l1": None})
    rows.sort(key=lambda r: -(r["value"] or 0))
    headline = {"value": round(sum(r["value"] or 0 for r in rows) / len(rows), 6),
                "unit": "HHI（企业数份额）", "max_chain": rows[0]["name"],
                "max_hhi": rows[0]["value"], "min_chain": rows[-1]["name"],
                "min_hhi": rows[-1]["value"]}
    facts = [
        {"label": "12 链平均 HHI", "value": headline["value"]},
        {"label": "最高集中链", "value": f'{rows[0]["name"]} {rows[0]["value"]}（CR1 {rows[0]["cr1"]}）'},
        {"label": "最低集中链", "value": f'{rows[-1]["name"]} {rows[-1]["value"]}'},
        {"label": "HHI>0.25（高集中）链数", "value": sum(1 for r in rows if (r["value"] or 0) > 0.25)},
        {"label": "覆盖环节合计", "value": sum(r["covered_leaves"] for r in rows)},
        {"label": "叶级企业合计（份额分母）", "value": sum(sum((c.get("leaf_firms") or {}).values()) for c in chains)},
        {"label": "链级企业合计", "value": sum(c["firms"] for c in chains)},
    ]
    population = {"defined_as": "链内叶级环节的企业数分布",
                  "leaves_with_firms": sum(r["covered_leaves"] for r in rows),
                  "firms": sum(c["firms"] for c in chains)}
    compute = {"formula": "HHI = Σ share_i^2；CR1 = max share；eff_n = 1/HHI",
               "share_unit": "企业数（非营收）", "proxy": True}
    STEPS = ["读链面板的叶级企业数分布", "逐链算份额平方和 HHI",
             "算首位环节份额 CR1 与等效环节数", "标注份额口径为企业数而非营收"]
    out = {
        "metric_id": "M_CHAIN_CONCENTRATION_INDEX",
        "metric_name": "产业集中度",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": 'HHI 可用 2,283,762 行标签的叶级企业数现算，12 条链全部有值；但份额只能按企业数，gkx 无环节级营收/市值，故是结构集中度而非市场集中度。',
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
    print("[ok]", "M_CHAIN_CONCENTRATION_INDEX", json.dumps(headline, ensure_ascii=False),
          "chains", len(rows), "sec", round(time.time() - t0, 2))


if __name__ == "__main__":
    main()
