#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""产业链完整度评分（M_CHAIN_COMPLETENESS_SCORE）—— 覆盖 + 均匀度，自包含。

口径：完整度 = 100 × (0.6 × 环节覆盖率 + 0.4 × 归一化熵)
    环节覆盖率 = 有企业的叶级环节 / 全部叶级环节
    归一化熵 = H(企业数分布) / ln(叶级环节数)，衡量环节间是否均衡
两项都来自链树 + 标签表，不含产值维（gkx 无环节级产值），故是结构完整度。

产物：chains[].value = 0—100 分；coverage、entropy_norm 分列。


运行：cd code && python3 M_CHAIN_COMPLETENESS_SCORE.py
产物：code/M_CHAIN_COMPLETENESS_SCORE_out.json（覆盖写）
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_COMPLETENESS_SCORE_out.json")

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
    import math
    rows = []
    for c in chains:
        lf = c.get("leaf_firms") or {}
        leaves = c["leaves"]
        cov = len(lf) / leaves if leaves else 0.0
        tot = sum(lf.values())
        ent = 0.0
        if tot and len(lf) > 1:
            ent = -sum((v / tot) * math.log(v / tot) for v in lf.values()) / math.log(leaves or 2)
        score = 100 * (0.6 * cov + 0.4 * ent)
        rows.append({"chain": c["chain"], "name": c["name"], "value": round(score, 2),
                     "coverage": round(cov, 4), "entropy_norm": round(ent, 4),
                     "leaves": leaves, "covered": len(lf),
                     "nonleaf": None, "l1": None})
    rows.sort(key=lambda r: -r["value"])
    headline = {"value": round(sum(r["value"] for r in rows) / len(rows), 2),
                "unit": "分（0—100）", "max_chain": rows[0]["name"], "max": rows[0]["value"],
                "min_chain": rows[-1]["name"], "min": rows[-1]["value"],
                "formula": "100*(0.6*覆盖率+0.4*归一化熵)"}
    facts = [
        {"label": "12 链平均完整度", "value": headline["value"]},
        {"label": "最高链", "value": f'{rows[0]["name"]} {rows[0]["value"]}'},
        {"label": "最低链", "value": f'{rows[-1]["name"]} {rows[-1]["value"]}'},
        {"label": "满分链数", "value": sum(1 for r in rows if r["value"] >= 99.99)},
        {"label": "平均环节覆盖率", "value": round(sum(r["coverage"] for r in rows) / len(rows), 4)},
        {"label": "全批加权覆盖率", "value": round(sum(r["covered"] for r in rows) / sum(r["leaves"] for r in rows), 4)},
        {"label": "叶级企业合计", "value": sum(sum((c.get("leaf_firms") or {}).values()) for c in chains)},
    ]
    population = {"defined_as": "链树叶级环节 × 标签表企业命中",
                  "leaves": sum(r["leaves"] for r in rows),
                  "covered": sum(r["covered"] for r in rows)}
    compute = {"formula": "100*(0.6*coverage+0.4*entropy_norm)",
               "weights": {"coverage": 0.6, "entropy": 0.4},
               "entropy_base": "ln(叶级环节数)"}
    STEPS = ["读链树的叶级环节数与标签表叶级企业数", "算环节覆盖率",
             "对叶级企业数分布算香农熵并按 ln(叶数) 归一",
             "按 0.6/0.4 加权成 0—100 分", "标注不含产值维"]
    out = {
        "metric_id": "M_CHAIN_COMPLETENESS_SCORE",
        "metric_name": "产业链完整度评分",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": '覆盖与均匀度两维可用链树 + 标签现算，12 条链均有分；产值维在 gkx 不存在，评分只反映结构完整度，不能替代含产值的完整度。',
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
    print("[ok]", "M_CHAIN_COMPLETENESS_SCORE", json.dumps(headline, ensure_ascii=False),
          "chains", len(rows), "sec", round(time.time() - t0, 2))


if __name__ == "__main__":
    main()
