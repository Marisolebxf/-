#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_DS_07_INDUSTRY_POTENTIAL_006 · 产业发展潜力综合评估（gkx 单库代理版）

定义（AS-IS 口径）
------------------
五维极值归一 + 用户自定义权重加权 → 产业级综合分 → 产业排名。
五维：产业投入、技术产品成熟度、产业产值、科学影响力、技术影响力。
旧稿的权重来自 `eval_weight` 表（用户可自定义），该表在 gkx 不存在
（source_absent，见 TABLE_ABSENCE_EVIDENCE §eval_weight）。

本件的做法
----------
五维逐项找可测代理，全部落在链（12 条顶层链）粒度：
  D1 产业投入   ：链内企业专利密度 = 链内专利总数 / 链内企业数
  D2 成熟度     ：K 节点覆盖率（深圳口径）
  D3 产业产值   ：链内样本营收合计（2014 基准年，覆盖最全的一年）
  D4 科学影响力 ：链内企业论文数（若快照无覆盖则该维缺，见 missing_dims）
  D5 技术影响力 ：链内专利总量（log）
权重无官方值时用等权，并在 weights_source 标注「等权替代，不等于甲方权重」。

输出：code/M_ENT_DS_07_INDUSTRY_POTENTIAL_006_out.json
"""
from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_ENT_DS_07_INDUSTRY_POTENTIAL_006_out.json"
METRIC = "M_ENT_DS_07_INDUSTRY_POTENTIAL_006"


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def minmax(vals):
    lo, hi = min(vals), max(vals)
    span = (hi - lo) or 1.0
    return [(v - lo) / span for v in vals]


def main() -> None:
    roots = {c["chain"]: c["name"] for c in load("chain_panel21.json")["chains"]}
    names = load("chain21_layer_20261022.json")["names"]
    orgs = defaultdict(int)
    for _, ch in names.items():
        orgs[ch] += 1

    pat = defaultdict(int)
    for ipc4, name, c in load("patent_ipc4_by_name_20261021.json"):
        ch = names.get(name)
        if ch:
            pat[ch] += c

    cov = load("chain21_sz_nodecov_20261022.json")["chains"]

    rev = load("chain21_revenue_20261022.json")["annual"]
    year_orgs = defaultdict(set)
    for r in rev:
        if r[4] and r[4] > 0:
            year_orgs[int(r[3])].add(r[1])
    rev_year = max(year_orgs, key=lambda y: len(year_orgs[y])) if year_orgs else None
    chain_rev = defaultdict(float)
    for r in rev:
        if r[4] and r[4] > 0 and int(r[3]) == rev_year:
            ch = names.get(r[1])
            if ch:
                chain_rev[ch] += float(r[4])

    # 论文侧：链内企业论文数不可得（论文快照按机构/作者组织，无企业名挂链），该维缺
    rows = []
    for code in sorted(roots):
        k = cov.get(code, {})
        k_nodes = k.get("K_nodes", 0)
        rows.append({
            "chain": code, "chain_name": roots[code],
            "orgs": orgs.get(code, 0),
            "patents": pat.get(code, 0),
            "patent_density": round(pat.get(code, 0) / orgs[code], 3) if orgs.get(code) else None,
            "k_coverage": round(k.get("k_covered", 0) / k_nodes, 4) if k_nodes else None,
            "revenue_sample": round(chain_rev.get(code, 0.0), 2),
        })

    d1 = minmax([r["patent_density"] or 0 for r in rows])
    d2 = [r["k_coverage"] if r["k_coverage"] is not None else 0.0 for r in rows]
    d3 = minmax([math.log1p(r["revenue_sample"]) for r in rows])
    d5 = minmax([math.log1p(r["patents"]) for r in rows])
    for i, r in enumerate(rows):
        r["d1_invest"] = round(d1[i], 4)
        r["d2_maturity"] = round(d2[i], 4)
        r["d3_output"] = round(d3[i], 4)
        r["d4_science"] = None
        r["d5_tech_influence"] = round(d5[i], 4)
        r["potential_score"] = round((d1[i] + d2[i] + d3[i] + d5[i]) / 4, 4)
    rows.sort(key=lambda r: -r["potential_score"])
    for i, r in enumerate(rows, 1):
        r["rank"] = i

    out = {
        "metric_id": METRIC,
        "metric_name": "产业发展潜力综合评估",
        "data_source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）+ code/_snapshots21/ 落盘快照",
        "formula": "potential = mean(minmax(D1 专利密度), D2 K覆盖率, D3 营收样本, D5 专利总量)；D4 科学影响力缺失",
        "blocking_tables": {
            "eval_weight": {"triage": "source_absent",
                            "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §eval_weight"},
        },
        "proxy_path": "五维各自找链级可测代理：专利密度（投入）、K 覆盖（成熟度）、样本营收（产值）、专利总量（技术影响力）",
        "proxy_deviation": "D4 科学影响力没有可用代理（论文快照按作者/机构组织，无企业名挂链）；D3 产值只有样本营收（2014 年 752 家），不是全口径产值；D2 只有深圳 K 覆盖；权重等权替代「用户自定义权重」，结论不能当甲方验收分",
        "weights_source": "等权替代（用户自定义权重表 eval_weight 不存在）",
        "weights": {"d1": 0.25, "d2": 0.25, "d3": 0.25, "d4": 0.0, "d5": 0.25},
        "missing_dims": ["D4 科学影响力（链内企业论文数无载体）"],
        "revenue_base_year": rev_year,
        "chains": rows,
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": "eval_weight（用户权重表）不存在，但五维里有四维能找到链级代理且都是真数：专利密度、K 覆盖率、样本营收、专利总量，12 链齐全。等权替代权重后综合分与排名可直接产出，故不判完全不支持；科学影响力维无载体、产值只有样本、权重非甲方值，故判部分支持。",
            "criteria": {
                "result_table_exists": False,
                "dims_total": 5, "dims_proxied": 4, "dims_missing": 1,
                "weight_table_exists": False, "proxy_used": True,
            },
        },
        "base_years_used": [rev_year] if rev_year else [],
        "base_years_missing": [],
        "base_years_note": f"营收基准取 {rev_year}（有效企业最多的一年，752 家）；2015 年后样本逐年塌陷至 34 家，用末年会让 D3 变成小样本噪声，故不用末年、也不按 0 补齐中间年。专利窗口 2021—2024。",
        "sources": [
            {"path": "code/_snapshots21/chain21_revenue_20261022.json",
             "table": "gkx.dwd_org_stock_finance_info + gkx.dwd_org_annual_financial_info",
             "rows": 41586, "role": "D3 产值"},
            {"path": "code/_snapshots21/patent_ipc4_by_name_20261021.json",
             "table": "gkx.dwd_patent", "rows": 581585, "role": "D1/D5"},
            {"path": "code/_snapshots21/chain21_sz_nodecov_20261022.json",
             "table": "gkx.dwd_org_industry_tags × gkx.dwd_industry_chain_info",
             "rows": 116017, "role": "D2 成熟度"},
            {"path": "code/_snapshots21/chain21_layer_20261022.json",
             "table": "gkx.dwd_org_industry_tags", "rows": 36993, "role": "企业→链"},
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[OK] {METRIC} -> {OUT.name} rev_year={rev_year}")
    for r in rows:
        print(f"  #{r['rank']:<2} {r['chain']} {r['chain_name'][:8]:<8} "
              f"d1={r['d1_invest']} d2={r['d2_maturity']} d3={r['d3_output']} "
              f"d5={r['d5_tech_influence']} -> {r['potential_score']}")


if __name__ == "__main__":
    main()
