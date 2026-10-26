#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TECH_DEEP_134_1 技术前沿热点领域识别模型 —— 离线复算（零 SQL）。

主维：IPC4×年专利量（2021—2024 完整年），近端增长 2023→2024 + 规模 z 分合成热点分。
辅维：论文/新闻侧有语料但无「论文→IPC4 / 新闻→IPC4」挂接，按缺口披露，不硬凑权重。
"""
from __future__ import annotations

import collections
import json
import math
import statistics

import _tech21_common as C

M = "M_TECH_DEEP_134_1"
WINDOW = C.COMPLETE_YEARS
MIN_N24, MIN_N23, MIN_N21 = 50, 20, 20

cell, by_year, domains_all = C.load_ipc_year()          # 全国基准
sz_cell, sz_year = C.load_sz_ipc_year()                # 深圳主口径
name_dom_sz = C.load_sz_name_dom()                     # 深圳申请人×域（全期）


def n(code, year):
    return sz_cell.get((code, year), 0)


def orgs(code, year):
    # 深圳域级年度机构数无缓存；用全期申请人名数作结构参照，字段名标 all
    return len(name_dom_sz.get(code, {}))


eligible = []
for d in sorted(domains_all):
    n21, n23, n24 = n(d, 2021), n(d, 2023), n(d, 2024)
    if n24 < MIN_N24 or n23 < MIN_N23 or n21 < MIN_N21:
        continue
    g_near = (n24 - n23) / n23
    g_total = (n24 - n21) / n21
    eligible.append({"ipc4": d, "n2021": n21, "n2023": n23, "n2024": n24,
                     "g_near": g_near, "g_total": g_total, "n_applicants_all": orgs(d, 2024)})

gz, mu_g, sd_g = C.zscores([x["g_near"] for x in eligible])
lz, mu_l, sd_l = C.zscores([math.log(x["n2024"]) for x in eligible])
for x, a, b in zip(eligible, gz, lz):
    x["hot_score"] = round(0.5 * a + 0.5 * b, 4)

ranked = sorted(eligible, key=lambda x: -x["hot_score"])


def row(x, rank=None):
    return {
        "rank": rank,
        "ipc4": x["ipc4"],
        "label": C.label(x["ipc4"]),
        "n2021": x["n2021"],
        "n2023": x["n2023"],
        "n2024": x["n2024"],
        "growth_23_24_pct": C.pct(x["g_near"]),
        "growth_21_24_pct": C.pct(x["g_total"]),
        "n_applicants_all": x["n_applicants_all"],
        "hot_score": x["hot_score"],
    }


top20 = [row(x, i + 1) for i, x in enumerate(ranked[:20])]

# 敏感性：只用增长 / 只用规模时的 Top20 重合度
growth_only = [x["ipc4"] for x in sorted(eligible, key=lambda x: -x["g_near"])[:20]]
scale_only = [x["ipc4"] for x in sorted(eligible, key=lambda x: -x["n2024"])[:20]]
base_top = [x["ipc4"] for x in ranked[:20]]
overlap_g = len(set(base_top) & set(growth_only))
overlap_s = len(set(base_top) & set(scale_only))

# 规模加权下的热点集中度：Top20 域 2024 件数占全部有 IPC 件的比重
top20_vol = sum(x["n2024"] for x in ranked[:20])
total_2024 = by_year[2024]

# 增长分布
pos = sum(1 for x in eligible if x["g_near"] > 0)
neg = len(eligible) - pos
strong = sum(1 for x in eligible if x["g_near"] >= 0.2)
sharp_drop = sum(1 for x in eligible if x["g_near"] <= -0.2)

# 20+8 命中（按 IPC 前缀，只作语义对照，不作覆盖结论）
hot20_codes = [x["ipc4"] for x in ranked[:20]]


def industry_of(code):
    for ind, prefixes in C.SZ208_MAP.items():
        if any(code.startswith(p) for p in prefixes):
            return ind
    return "未映射"


hot20_industry = collections.Counter(industry_of(c) for c in hot20_codes)

# 论文侧：只到城市/学科，不能落 IPC4
papers = json.load(open(C.SNAP / "papers_city_year_gkx21.json", encoding="utf-8"))
facts = json.load(open(C.SNAP / "innov21_facts_20261021.json", encoding="utf-8"))
paper_year = papers.get("year_all", {})
paper_sz = facts.get("paper_city", {}).get("by_city", {}).get("深圳市")
paper_2024 = paper_year.get("2024")

# 分类学校验：H10H/H10D 是 2025.01 新版 IPC 新码，历史件数受「旧码迁新码」影响，
# 不能把新码的增长率直接读成技术热度。把 H01L 与 H10x 合并成「半导体器件族」做对照。
semi_codes = ["H01L", "H10H", "H10D", "H10K"]


def semi_sum(year):
    return sum(n(c, year) for c in semi_codes)


semi_series = {str(y): semi_sum(y) for y in (2021, 2022, 2023, 2024)}
semi_growth = (semi_series["2024"] - semi_series["2021"]) / semi_series["2021"]

payload = {
    "metric_id": M,
    "generated_at": "2026-10-22",
    "params": {
        "time_axis": "apdt_year（申请年）",
        "window": WINDOW,
        "near_growth": [2023, 2024],
        "thresholds": {"min_n2024": MIN_N24, "min_n2023": MIN_N23, "min_n2021": MIN_N21},
        "weights": {"growth_23_24": 0.5, "log_scale_2024": 0.5},
        "base_years_used": WINDOW,
        "base_years_missing": C.MISSING_BASE_YEARS,
        "excluded_years": [2025, 2026],
    },
    "universe": {
        "ipc4_total": len(domains_all),
        "eligible_domains": len(eligible),
        "national_2024_ipc_patents": total_2024,
        "sz_2024_ipc_patents": sz_year[2024],
        "note": "合格域要求 2021/2023/2024 三年均有最低量，避免小基数增长率噪声。",
    },
    "hot_top20": top20,
    "distribution": {
        "positive_growth": pos,
        "negative_growth": neg,
        "positive_pct": C.pct(pos / len(eligible)),
        "strong_growth_ge20pct": strong,
        "sharp_drop_le_minus20pct": sharp_drop,
        "zscore_params": {"growth_mean": round(mu_g, 4), "growth_sd": round(sd_g, 4),
                          "log_scale_mean": round(mu_l, 4), "log_scale_sd": round(sd_l, 4)},
    },
    "sensitivity": {
        "top20_overlap_growth_only": overlap_g,
        "top20_overlap_scale_only": overlap_s,
        "interpretation": "合成分 Top20 与单维 Top20 的重合数；重合低说明热点排序由双维共同决定，不是单一规模榜。",
    },
    "hot20_volume": {"sum_n2024": top20_vol, "share_of_national_pct": C.pct(top20_vol / total_2024)},
    "industry_crosswalk": {"by_20_8": dict(hot20_industry.most_common()), "note": "IPC 前缀一对多，归属次不可加。"},
    "paper_dim": {
        "available": False,
        "corpus_rows": sum(paper_year.values()) if paper_year else None,
        "shenzhen_papers": paper_sz,
        "paper_2024_rows": paper_2024,
        "discipline_top": facts.get("discipline", [])[:5],
        "blocker": "论文语料只有城市/学科/年份，没有 IPC4 或技术域字段；无法与专利域做同域合成，故权重设为 0。",
    },
    "news_dim": {
        "available": False,
        "blocker": "新闻表无「技术域/IPC4」挂接字段，无法计算域级新闻热度；按缺口披露，不构造代理。",
    },
    "taxonomy_check": {
        "note": "H10H/H10D 为 2025.01 新版 IPC 新码，2021—2023 件数受旧码（H01L 等）迁入影响；新码增长率不可直接读作技术热度。",
        "new_codes": ["H10H", "H10D", "H10K"],
        "predecessor": "H01L",
        "merged_family": "H01L+H10H+H10D+H10K",
        "merged_series": semi_series,
        "merged_growth_21_24_pct": C.pct(semi_growth),
        "h01l_series": {str(y): n("H01L", y) for y in (2021, 2022, 2023, 2024)},
    },
    "base_years_used": WINDOW,
    "base_years_missing": C.MISSING_BASE_YEARS,
}

payload["support_judgment"] = {
    "data_support_level": "部分支持",
    "criteria": {
        "patent_hotspot_rank": True,
        "eligible_domains": len(eligible),
        "top20_overlap_growth_only": overlap_g,
        "paper_dim": False,
        "news_dim": False,
        "years_available": WINDOW,
    },
    "reason": (
        f"专利侧热点排序可交付：{len(eligible)} 个合格域、Top20 合成分、增长分布（正增长 {C.pct(pos / len(eligible))}%）"
        "均由全量面板复算；但论文维（100,900 篇，深圳 9,520 篇）只有城市/学科粒度、新闻维无技术域挂接，"
        "需求的多源热度合成只能退化为专利单源，故判部分支持。"
    ),
}

C.write_out(M, payload)
