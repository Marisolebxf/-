#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""深圳产业链企业占比（M_CHAIN_SZ_ENTERPRISE_RATIO）—— gkx 标签 × 主档城市，自包含。

口径：分子 = 该链下 credit_code 在主档城市为「深圳市」的企业数；
    分母 = 该链下全部有城市归属的企业数（gkx 底册 189,116 家的链内子集）。
分母不是「全国该链企业总数」：gkx 主档本身是深圳都市圈底册（99.82% 在广东），
全国口径在库内不存在，故本值只能读作「底册范围内深圳占比」，须带限定语。

产物：chains[].value = 深圳占比（小数 4 位），附 sz/total。


运行：cd code && python3 M_CHAIN_SZ_ENTERPRISE_RATIO.py
产物：code/M_CHAIN_SZ_ENTERPRISE_RATIO_out.json（覆盖写）
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_SZ_ENTERPRISE_RATIO_out.json")

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
        f = c["firms"]; sz = c["sz_firms"]
        rows.append({"chain": c["chain"], "name": c["name"],
                     "value": round(sz / f, 4) if f else None,
                     "sz_firms": sz, "total_firms": f,
                     "nonleaf": None, "leaves": None, "l1": None})
    rows.sort(key=lambda r: -(r["value"] or 0))
    tsz = sum(r["sz_firms"] for r in rows); tf = sum(r["total_firms"] for r in rows)
    headline = {"value": round(tsz / tf, 4) if tf else None,
                "unit": "深圳占比（0—1）", "sz_firms": tsz, "total_firms": tf,
                "denominator_scope": "gkx 底册链内企业（非全国）"}
    facts = [
        {"label": "链内企业合计", "value": tf},
        {"label": "其中深圳", "value": tsz},
        {"label": "总体深圳占比", "value": headline["value"]},
        {"label": "占比最高链", "value": f'{rows[0]["name"]} {rows[0]["value"]}'},
        {"label": "占比最低链", "value": f'{rows[-1]["name"]} {rows[-1]["value"]}'},
    ]
    population = {"defined_as": "gkx.dwd_org_industry_tags 一行=一家企业，城市取主档",
                  "total_firms": tf, "sz_firms": tsz,
                  "city_totals": load("org_name_city_20261021.json")["city_totals"]}
    compute = {"formula": "SUM(city='深圳市')/COUNT(*) GROUP BY chain",
               "denominator_caveat": "底册为深圳都市圈口径，不能外推全国份额"}
    STEPS = ["读取链面板的链内企业数与深圳企业数",
             "逐链算深圳占比 = sz_firms / firms",
             "汇总全链总体占比",
             "标注分母限定：底册口径而非全国口径"]
    out = {
        "metric_id": "M_CHAIN_SZ_ENTERPRISE_RATIO",
        "metric_name": "深圳产业链企业占比",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": '分子分母都能从 gkx 标签 × 主档城市直接算，12 条链全部有值；但分母是深圳都市圈底册（189,116 家，99.82% 在广东），不是全国该链企业总数，语义须降为「底册内占比」。',
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
    print("[ok]", "M_CHAIN_SZ_ENTERPRISE_RATIO", json.dumps(headline, ensure_ascii=False),
          "chains", len(rows), "sec", round(time.time() - t0, 2))


if __name__ == "__main__":
    main()
