#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""区域营收（M_CHAIN_REG_REVENUE）—— 年报营收 × 链标签，自包含。

口径：营收取 gkx.dwd_org_annual_financial_info（operating_revenue>0）的最近一年，
    按链汇总 rev_sum；深圳营收取主档城市=深圳的子集。年报覆盖极稀（全表 2.41% 行有正值），
    因此本值只能读作「有披露企业的营收和」，不是全链营收。

产物：chains[].value = 该链最近一年营收和（元）；n_rev = 有营收企业数；n_ent = 链内企业数。


运行：cd code && python3 M_CHAIN_REG_REVENUE.py
产物：code/M_CHAIN_REG_REVENUE_out.json（覆盖写）
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_REG_REVENUE_out.json")

BASE_USED = [2016, 2023, 2025]
BASE_MISSING = []
BASE_NOTE = ('逐链取该链最近一个有正营收的年度，再跨链求和：9 条链落在 2025、生物医药与智能网联汽车落 2023、'
             '低空经济落 2016（该链 2017—2025 全无正营收记录，不按 0 摊、不补插值）。'
             '2026 年全库 0 行，未纳入；不做同比、不做 CAGR。')

SOURCES = [
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
      "table": "gkx.dwd_org_industry_tags", "rows": 2283762,
      "snapshot": "code/_snapshots21/chain_panel21.json",
      "pulled_at": "2026-10-22T15:32:34+08:00"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
      "table": "gkx.dwd_org_annual_financial_info", "rows": None,
      "snapshot": "code/_snapshots21/chain_lm_fin_20261021.json",
      "pulled_at": "2026-10-21",
      "note": "fin.rev_sum = operating_revenue>0 按链×年求和；fin.sz_rev 仅覆盖上市主体"},
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
        fin = c.get("fin") or {}
        rows.append({"chain": c["chain"], "name": c["name"],
                     "value": round(fin.get("rev_sum", 0.0), 2),
                     "sz_revenue": round(fin.get("sz_rev", 0.0), 2),
                     "n_rev": fin.get("n_rev", 0), "n_ent": fin.get("n_ent", 0),
                     "rev_year": fin.get("rev_year"),
                     "nonleaf": None, "leaves": None, "l1": None})
    rows.sort(key=lambda r: -r["value"])
    tv = sum(r["value"] for r in rows); tsz = sum(r["sz_revenue"] for r in rows)
    nrev = sum(r["n_rev"] for r in rows); nent = sum(r["n_ent"] for r in rows)
    years = sorted({r["rev_year"] for r in rows if r["rev_year"]})
    mixed = [{"chain": r["chain"], "name": r["name"], "rev_year": r["rev_year"]}
             for r in rows if r["rev_year"] != (max(years) if years else None)]
    headline = {"value": round(tv, 2), "unit": "元（有披露企业营收和）",
                "sz_revenue": round(tsz, 2), "n_rev": nrev, "n_ent": nent,
                "coverage": round(nrev / nent, 4) if nent else None,
                "year": years[-1] if years else None,
                "years_used": years,
                "sz_n": sum((c.get("fin") or {}).get("sz_n", 0) for c in chains),
                "mixed_year_chains": mixed}
    facts = [
        {"label": "链级营收合计", "value": round(tv / 1e8, 2) if tv else 0, "unit": "亿元"},
        {"label": "其中深圳（仅上市主体）", "value": round(tsz / 1e8, 2) if tsz else 0, "unit": "亿元"},
        {"label": "有营收披露企业 / 链内企业", "value": f"{nrev:,} / {nent:,}"},
        {"label": "营收覆盖率", "value": headline["coverage"]},
        {"label": "深圳营收覆盖主体数", "value": headline["sz_n"]},
        {"label": "实际使用年度", "value": "、".join(str(y) for y in years)},
    ]
    population = {"defined_as": "gkx.dwd_org_annual_financial_info operating_revenue>0，按链归集",
                  "n_rev": nrev, "n_ent": nent,
                  "source_snapshot": "code/_snapshots21/chain_lm_fin_20261021.json"}
    compute = {"formula": "SUM(operating_revenue) GROUP BY chain, latest_year",
               "coverage": headline["coverage"],
               "years_used": years,
               "sz_revenue_scope": "仅 gkx.dwd_org_stock_finance_info 中可定位到深圳的上市主体（sz_n）"} 
    STEPS = ["读链财务快照 chain_lm_fin_20261021.json",
             "取每条链最近一个有正营收的年度",
             "按链汇总营收与深圳子集营收",
             "算营收披露覆盖率（有营收企业/链内企业）",
             "标注口径：有披露企业营收和，不是全链营收"]
    out = {
        "metric_id": "M_CHAIN_REG_REVENUE",
        "metric_name": "区域营收",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": '营收—链—城市三段管道在真实表白名单内跑通，12 条链均有值；但年报营收字段九成以上为空，覆盖企业数远小于链内企业数，只能作「有披露企业营收和」。',
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
    print("[ok]", "M_CHAIN_REG_REVENUE", json.dumps(headline, ensure_ascii=False),
          "chains", len(rows), "sec", round(time.time() - t0, 2))


if __name__ == "__main__":
    main()
