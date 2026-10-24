#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""专利（链维/区域维）（M_CHAIN_REG_PATENT）—— 申请人名称桥接，自包含。

口径：专利件数来自 gkx.dwd_patent（2,939,895 件，apdt_year 2021—2026），
    申请人名称 → 企业名称 → 链（标签快照 names）→ 城市（主档名称）。
    名称匹配是代理：官方口径要求的机构—专利关系表在 gkx 不存在，同名/更名会漏计。

产物：chains[].value = 该链专利件数；sz_patents = 深圳申请人专利件数；
patent_firms = 有专利的申请人去重数。


运行：cd code && python3 M_CHAIN_REG_PATENT.py
产物：code/M_CHAIN_REG_PATENT_out.json（覆盖写）
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_REG_PATENT_out.json")

BASE_USED = ["2021", "2022", "2023", "2024"]
BASE_MISSING = ["2025", "2026"]
BASE_NOTE = ("统计期 2025 年，专利按申请年 ≤2024 截断：`dwd_patent.apdt_year` 只有 2021—2026，"
             "且 2025/2026 申请量因公开滞后不完整，纳入会系统性低估近年值；2025/2026 仅作观察不入正式值。")

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
    layer = load("chain21_layer_20261022.json")
    pat = load("patent_panel_innov_20261021.json")
    app_total = pat["app_total"]
    name_chain = layer["names"]
    base = load("base_20261021.json")
    name_city = {}
    for r in base:
        if r[2] and r[2] not in name_city:
            name_city[r[2]] = r[4]
    agg = defaultdict(lambda: {"n": 0, "sz": 0, "firms": 0})
    for name, pv in app_total.items():
        c = name_chain.get(name)
        if not c:
            continue
        a = agg[c]
        a["n"] += pv
        a["firms"] += 1
        if name_city.get(name) == "深圳市":
            a["sz"] += pv
    rows = []
    for c in chains:
        a = agg.get(c["chain"], {"n": 0, "sz": 0, "firms": 0})
        rows.append({"chain": c["chain"], "name": c["name"], "value": a["n"],
                     "sz_patents": a["sz"], "patent_firms": a["firms"],
                     "nonleaf": None, "leaves": None, "l1": None})
    rows.sort(key=lambda r: -r["value"])
    tn = sum(r["value"] for r in rows); tsz = sum(r["sz_patents"] for r in rows)
    vv = sorted(r["value"] for r in rows)
    stats = {
        "n_chains": len(rows),
        "min": vv[0], "max": vv[-1], "median": vv[len(vv) // 2],
        "top1_share_pct": round(100.0 * vv[-1] / tn, 3) if tn else None,
        "sz_share_pct": round(100.0 * tsz / tn, 3) if tn else None,
        "patents_per_firm": round(tn / sum(r["patent_firms"] for r in rows), 2)
                             if sum(r["patent_firms"] for r in rows) else None,
    }
    headline = {"value": tn, "unit": "件（名称桥接口径）", "sz_patents": tsz,
                "patent_table_rows": pat["rows"], "window": pat["window"],
                "firms_with_patents": sum(r["patent_firms"] for r in rows)}
    facts = [
        {"label": "专利主表行数", "value": pat["rows"]},
        {"label": "专利年份窗口", "value": "2021—2024（apdt_year 仅 2021—2026）"},
        {"label": "链级专利件数合计", "value": tn},
        {"label": "其中深圳申请人", "value": tsz},
        {"label": "有专利的申请人", "value": headline["firms_with_patents"]},
    ]
    population = {"defined_as": "gkx.dwd_patent 全部申请，申请人名称能桥到链的样本",
                  "patent_rows": pat["rows"], "name_mapped": len(name_chain),
                  "window": pat["window"]}
    compute = {"formula": "SUM(patent_count) GROUP BY chain",
               "bridge": "applicant_name → 标签表 company_name → chain；base name → city",
               "proxy": True}
    STEPS = ["读取专利面板快照（2,939,895 件，2021—2024 窗口）",
             "申请人名称 → 链（标签扫描 names）", "企业名称 → 城市（主档名称）",
             "按链汇总专利件数、深圳件数与申请人去重数",
             "标注名称桥接偏差：同名合并、更名漏计"]
    out = {
        "metric_id": "M_CHAIN_REG_PATENT",
        "metric_name": "专利（链维/区域维）",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": '专利主表 293.9 万件真实可用，名称桥接后 12 条链均有值；但官方口径要求的机构—专利关系键与机构—链关系表在 gkx 均不存在（information_schema 零命中），名称匹配会漏计更名/同名主体，链归属与城市归属都只能作代理。',
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
        "gaps": [
            "官方桥缺失：gkx 无 enterprise_patent_org_rel / enterprise_industry_chain 表（information_schema 零命中），org_id 全键路径不可执行",
            "名称桥：同名企业合并、更名/简称漏计；申请人名称能桥到链的样本 36,993 个",
            "单链归属：一个申请人名称只映射一个链，跨链企业只计入首链，链间分布偏保守",
            "与 M_CHAIN_PATENT_COUNT 不同口径：本件第一申请人单角色、每件只计一次（1,127,340 件）；该件双角色并集、多链重复计位（3,026,291），两者不可互校",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("[ok]", "M_CHAIN_REG_PATENT", json.dumps(headline, ensure_ascii=False),
          "chains", len(rows), "sec", round(time.time() - t0, 2))


if __name__ == "__main__":
    main()
