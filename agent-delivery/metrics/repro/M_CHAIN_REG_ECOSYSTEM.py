#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""区域产业生态（M_CHAIN_REG_ECOSYSTEM）—— 一级环节覆盖法，自包含。

口径（王惠 v0.2.0 方案 A）：生态 = 该链在指定城市「有一级环节落地」的比例。
    分母 = 该链 L1 环节码个数（链树长度 9 的节点）；
    分子 = 该城市有 ≥1 家企业的 L1 环节数（L1 由叶码前 9 位还原）。
L1 口径天然易饱和（每链只有 3—6 个 L1），故比例分辨力有限，须与环节级覆盖并列看。

产物：chains[].value = 深圳市 L1 覆盖率；city_rates 给四市覆盖率。


运行：cd code && python3 M_CHAIN_REG_ECOSYSTEM.py
产物：code/M_CHAIN_REG_ECOSYSTEM_out.json（覆盖写）
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_REG_ECOSYSTEM_out.json")

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
    leaf = load("chain_stage_leaf_20261021.json")
    cell_leaf = leaf["cell_leaf_firm_counts"]
    l1_by_chain = defaultdict(set)
    for r in tree:
        if len(r["industry_code"]) == 9:
            l1_by_chain[r["industry_code"][:7]].add(r["industry_code"])
    cities = ["深圳市", "广州市", "东莞市", "惠州市"]
    rows = []
    for c in chains:
        code = c["chain"]
        denom = len(l1_by_chain.get(code, ()))
        city_rates = {}
        for city in cities:
            d = cell_leaf.get(code + "|" + city, {})
            covered = {k[:9] for k, v in d.items() if v > 0 and len(k) >= 9}
            city_rates[city] = round(len(covered & l1_by_chain[code]) / denom, 4) if denom else None
        rows.append({"chain": code, "name": c["name"], "value": city_rates["深圳市"],
                     "l1_total": denom, "city_rates": city_rates,
                     "nonleaf": None, "leaves": None, "l1": c["l1_count"]})
    rows.sort(key=lambda r: -(r["value"] or 0))
    headline = {"value": round(sum(r["value"] or 0 for r in rows) / len(rows), 4),
                "unit": "深圳 L1 覆盖率均值", "l1_total": sum(r["l1_total"] for r in rows),
                "chains": len(rows), "cities": cities}
    facts = [
        {"label": "L1 环节总数（12 链）", "value": sum(r["l1_total"] for r in rows)},
        {"label": "深圳平均覆盖率", "value": headline["value"]},
        {"label": "深圳覆盖率最高链", "value": f'{rows[0]["name"]} {rows[0]["value"]}'},
        {"label": "深圳覆盖率最低链", "value": f'{rows[-1]["name"]} {rows[-1]["value"]}'},
        {"label": "四市口径", "value": "、".join(cities)},
    ]
    population = {"defined_as": "gkx 链树 L1 节点 × 标签表城市 × 环节叶码命中",
                  "l1_total": sum(r["l1_total"] for r in rows),
                  "cell_source": "code/_snapshots21/chain_stage_leaf_20261021.json"}
    compute = {"formula": "|{L1: 该城市有企业}| / |L1|",
               "l1_rule": "叶码前 9 位还原 L1，L1 分母取链树长度 9 节点",
               "saturation": "每链 3—6 个 L1，比例易饱和"}
    STEPS = ["读环节叶级快照（2,283,762 行标签按 link 码解析）",
             "由叶码前 9 位还原 L1，分母取链树 L1 节点数",
             "按四市统计有企业的 L1 集合", "算覆盖率并标注 L1 口径饱和风险"]
    out = {
        "metric_id": "M_CHAIN_REG_ECOSYSTEM",
        "metric_name": "区域产业生态",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": 'L1 覆盖率可由链树 + 2,283,762 行标签现算，48 个链×市单元均可产出；但每链仅 3—6 个 L1，覆盖率天然易饱和到 1.0，分辨力弱于环节级口径。',
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
    print("[ok]", "M_CHAIN_REG_ECOSYSTEM", json.dumps(headline, ensure_ascii=False),
          "chains", len(rows), "sec", round(time.time() - t0, 2))


if __name__ == "__main__":
    main()
