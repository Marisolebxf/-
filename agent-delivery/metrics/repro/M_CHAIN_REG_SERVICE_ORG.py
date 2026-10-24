#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""区域服务机构（M_CHAIN_REG_SERVICE_ORG）—— 国标行业重建，自包含。

口径：服务机构 = gkx 主档中属于商务服务/科技服务/信息服务等行业的法人（按国标行业门类），
    按链标签挂链、按城市切片。原「服务机构池」表在 gkx 不存在（只有演示产物），
    本件改由主档行业重建，准入规则与原池不等价。

产物：chains[].value = 该链三市服务机构合计；city_counts 给深圳/广州/东莞/惠州分市数。


运行：cd code && python3 M_CHAIN_REG_SERVICE_ORG.py
产物：code/M_CHAIN_REG_SERVICE_ORG_out.json（覆盖写）
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_REG_SERVICE_ORG_out.json")

BASE_USED = []
BASE_MISSING = []
BASE_NOTE = '截面指标：统计当前存量，不设年度分母。'

SOURCES = [
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
      "table": "gkx.dwd_org_industry_tags", "rows": 2283762,
      "snapshot": "code/_snapshots21/chain_panel21.json",
      "pulled_at": "2026-10-22T15:32:34+08:00"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
      "table": "gkx.dwd_industry_chain_info", "rows": 1273,
      "snapshot": "code/_snapshots21/chain_tree_20261021.json"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
      "table": "gkx.dwd_org_base_info（国标行业门类）", "rows": 189116,
      "snapshot": "code/_snapshots21/base_20261021.json"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
      "table": "gkx.dwd_org_base_info × gkx.dwd_org_industry_tags（链×市聚合）", "rows": 1552,
      "snapshot": "code/_snapshots21/svc_chain_city_20261022.json",
      "pulled_at": "2026-10-22T15:26:04+08:00",
      "note": "42 个非空链×市单元；按主档国标行业服务业门类 + 链标签重建，非原 svc_org_circle 池"},
]


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    t0 = time.time()
    panel = load("chain_panel21.json")
    chains = panel["chains"]
    tree = load("chain_tree_20261021.json")
    svc = load("svc_chain_city_20261022.json")
    cell = defaultdict(dict)
    for c, city, n in svc:
        cell[c][city] = n
    rows = []
    for c in chains:
        d = cell.get(c["chain"], {})
        rows.append({"chain": c["chain"], "name": c["name"],
                     "value": sum(d.values()), "city_counts": d,
                     "nonleaf": None, "leaves": None, "l1": None})
    rows.sort(key=lambda r: -r["value"])
    total = sum(r["value"] for r in rows)
    sz = sum(r["city_counts"].get("深圳市", 0) for r in rows)
    CITY_ORDER = ["深圳市", "广州市", "东莞市", "惠州市"]
    city_totals = {c: sum(r["city_counts"].get(c, 0) for r in rows) for c in CITY_ORDER}
    empty_cells = [f"{c['chain']}|{city}" for c in chains for city in CITY_ORDER
                   if city not in cell.get(c["chain"], {})]
    cities = sorted({k for r in rows for k in r["city_counts"]})
    headline = {"value": total, "unit": "家（四市服务机构挂接次数，跨链可重复计）",
                "sz": sz, "cells": len(svc), "cities": CITY_ORDER,
                "city_totals": city_totals,
                "definition": "主档国标行业属服务业的法人，按链标签挂链"}
    facts = [
        {"label": "链×市非空单元", "value": f"{len(svc)}/48"},
        {"label": "服务机构挂接合计", "value": total},
        {"label": "其中深圳", "value": sz},
        {"label": "四市分布", "value": "、".join(f"{k[:-1]} {v}" for k, v in city_totals.items())},
        {"label": "服务机构最多的链", "value": f'{rows[0]["name"]} {rows[0]["value"]}'},
    ]
    population = {"defined_as": "gkx 主档国标行业服务业门类 + 链标签",
                  "cells": len(svc), "cities": cities}
    compute = {"formula": "COUNT(DISTINCT credit_code) GROUP BY chain, city",
               "source_snapshot": "code/_snapshots21/svc_chain_city_20261022.json",
               "rebuild": True}
    STEPS = ["读取已落盘的服务机构×链×市快照（42 个非空单元）",
             "按链汇总三市合计与深圳分市数", "标出空单元（48 格中 6 格为空）",
             "声明重建准入：主档国标行业，不等价于原服务机构池"]
    out = {
        "metric_id": "M_CHAIN_REG_SERVICE_ORG",
        "metric_name": "区域服务机构",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": '服务机构可用主档国标行业重建，42/48 个链×市单元有值；但原服务机构池在 gkx 不存在，重建准入规则与原池不等价，须甲方确认后才能定版。',
        "sources": SOURCES,
        "base_years_used": BASE_USED,
        "base_years_missing": BASE_MISSING,
        "base_years_note": BASE_NOTE,
        "headline": headline,
        "facts": facts,
        "empty_cells": empty_cells,
        "chains": rows,
        "method_steps": STEPS,
        "population": population,
        "compute": compute,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("[ok]", "M_CHAIN_REG_SERVICE_ORG", json.dumps(headline, ensure_ascii=False),
          "chains", len(rows), "sec", round(time.time() - t0, 2))


if __name__ == "__main__":
    main()
