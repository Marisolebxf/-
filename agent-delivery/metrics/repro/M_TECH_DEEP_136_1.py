#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TECH_DEEP_136_1 技术转化瓶颈堵点原因识别模型 —— 离线复算（零 SQL）。

可算：专利活跃度结构画像（规模、收缩、申请人集中度、头部 2024 授权率），输出堵点候选面。
不可算：转化流量（转让/许可 22,809 行、名称命中 2.07%，且无 IPC4 字段）、
       市场归因（融资表无域/技术标签）、政策归因（政策 theme 19,998/20,000 为空）、
       链环停留/转化率（无运营表）。按缺口披露，不硬造归因分。
"""
from __future__ import annotations

import collections
import json
import math

import _tech21_common as C

M = "M_TECH_DEEP_136_1"
WINDOW = C.COMPLETE_YEARS
MIN_N24, MIN_GROWTH = 1000, -0.10  # 候选门槛：规模≥1000 且 2021→2024 跌幅≥10%

cell, by_year, domains_all = C.load_ipc_year()   # 全国基准（仅域清单/参照）
sz_cell, sz_year = C.load_sz_ipc_year()         # 深圳主口径
name_dom_sz = C.load_sz_name_dom()              # 深圳申请人×域（全期）
star_agg = C.load_star_agg()[0]                 # 申请人全期 [申请, 授权]

name_dom = collections.defaultdict(list)
for ipc4, nm, n in C.load_ipc_name():
    if nm in name_dom_sz.get(ipc4, {}):
        name_dom[ipc4].append((nm, name_dom_sz[ipc4][nm]))


def nat(code, year):
    return sz_cell.get((code, year), 0)


def orgs(code, year):
    return cell.get((code, year), (0, 0))[1]


all_rows = []
for d in sorted(domains_all):
    n21, n23, n24 = nat(d, 2021), nat(d, 2023), nat(d, 2024)
    if n21 <= 0 or n23 <= 0 or n24 < 100:
        continue
    g_total = (n24 - n21) / n21
    g_near = (n24 - n23) / n23
    lst = sorted(name_dom.get(d, []), key=lambda x: -x[1])
    tot = sum(c for _, c in lst)
    top5 = lst[:5]
    grant_den = sum(star_agg.get(nm, [0, 0])[0] for nm, _ in top5)
    grant_num = sum(star_agg.get(nm, [0, 0])[1] for nm, _ in top5)
    all_rows.append({
        "ipc4": d, "label": C.label(d), "n2021": n21, "n2023": n23, "n2024": n24,
        "growth_21_24_pct": C.pct(g_total), "growth_23_24_pct": C.pct(g_near),
        "n_applicants_all": len(lst),
        "n_applicants": len(lst),
        "top1_name": top5[0][0] if top5 else None,
        "top1_share_pct": C.pct(top5[0][1] / tot) if top5 and tot else None,
        "top5_share_pct": C.pct(sum(c for _, c in top5) / tot) if tot else None,
        "applicant_hhi": C.hhi(collections.Counter(dict(lst))),
        "top5_allperiod_grant_rate_pct": C.pct(grant_num / grant_den) if grant_den else None,
        "_g_total": g_total,
    })

candidates = [r for r in all_rows if r["n2024"] >= MIN_N24 and r["_g_total"] <= MIN_GROWTH]
for r in candidates:
    r["severity"] = round(-r["_g_total"] * math.log(r["n2024"]), 3)
candidates.sort(key=lambda r: -r["severity"])
for r in candidates:
    if r["top1_share_pct"] and r["top1_share_pct"] >= 10:
        r["structure"] = "头部集中"
    elif r["n_applicants"] >= 3000:
        r["structure"] = "长尾分散"
    else:
        r["structure"] = "中度分散"
    r.pop("_g_total", None)

# 全库结构基线（用于说明候选面不是普遍现象）
neg = sum(1 for r in all_rows if r["growth_21_24_pct"] < 0)
neg_big = sum(1 for r in all_rows if r["growth_21_24_pct"] <= -10)

# 缺口事实：只读缓存/清单，不查库
facts = json.load(open(C.SNAP / "innov21_facts_20261021.json", encoding="utf-8"))
transfer = facts.get("transfer_city", {})
policy_null = facts.get("policy_theme_null")
policy_total = facts.get("policy_total")

# 分类学校验：H01L 的下跌部分来自 H10x 新码迁入，不能全部算作「堵点」。
semi_codes = ["H01L", "H10H", "H10D", "H10K"]
semi_series = {str(y): sum(nat(c, y) for c in semi_codes) for y in (2021, 2022, 2023, 2024)}
semi_growth = (semi_series["2024"] - semi_series["2021"]) / semi_series["2021"]

payload = {
    "metric_id": M,
    "generated_at": "2026-10-22",
    "params": {
        "time_axis": "apdt_year（申请年）",
        "window": WINDOW,
        "candidate_rule": "n2024>=1000 且 g(2021→2024)<=-10%",
        "severity": "-g_total × ln(n2024)（跌幅×规模）",
        "base_years_used": WINDOW,
        "base_years_missing": C.MISSING_BASE_YEARS,
        "excluded_years": [2025, 2026],
    },
    "universe": {"ipc4_total": len(domains_all), "eligible_domains": len(all_rows),
                 "negative_growth": neg, "drop_ge_10pct": neg_big},
    "candidates": {
        "n": len(candidates),
        "share_of_eligible_pct": C.pct(len(candidates) / len(all_rows)),
        "top20": candidates[:20],
        "structure_dist": dict(collections.Counter(r["structure"] for r in candidates)),
    },
    "conversion_flow_dim": {
        "available": False,
        "transfer_rows": transfer.get("rows"),
        "edges_matched": transfer.get("edges_matched"),
        "name_hit_rate_pct": round((transfer.get("name_hit_rate") or 0) * 100, 2),
        "shenzhen_edges": transfer.get("by_city", {}).get("深圳市"),
        "blocker": "dwd_patent_transfer 22,809 行、名称命中 2.07%（779 条边），且无 IPC4/技术域字段；无法算域级转化率或环节停留。",
    },
    "market_attribution_dim": {
        "available": False,
        "blocker": "dwd_org_financing_info 25,654 行无技术域/IPC 标签，企业→域的映射缺键；融资热度不能归因到域。",
    },
    "policy_attribution_dim": {
        "available": False,
        "policy_rows": policy_total,
        "theme_null_rows": policy_null,
        "blocker": "政策 theme 19,998/20,000 为空、keywords 无有效值，无法把政策映射到 IPC4 域；政策归因不可算。",
    },
    "chain_stage_dim": {
        "available": False,
        "blocker": "研发→中试→量产→市场的环节流量/停留时长无运营表，链环堵点只能停留在框架层。",
    },
    "taxonomy_check": {
        "note": "H01L 的 2021→2024 跌幅含 H10H/H10D/H10K 新码迁入影响；合并半导体族后跌幅收窄，H01L 不能单独作为堵点结论。",
        "merged_family": "H01L+H10H+H10D+H10K",
        "merged_series": semi_series,
        "merged_growth_21_24_pct": C.pct(semi_growth),
        "h01l_growth_21_24_pct": C.pct((nat("H01L", 2024) - nat("H01L", 2021)) / nat("H01L", 2021)),
    },
    "base_years_used": WINDOW,
    "base_years_missing": C.MISSING_BASE_YEARS,
}

payload["support_judgment"] = {
    "data_support_level": "部分支持",
    "criteria": {
        "candidate_surface": True,
        "eligible_domains": len(all_rows),
        "candidates": len(candidates),
        "conversion_flow_dim": False,
        "market_attribution_dim": False,
        "policy_attribution_dim": False,
        "chain_stage_dim": False,
    },
    "reason": (
        f"候选面可交付：{len(all_rows)} 个域中筛出 {len(candidates)} 个「规模≥1000 且 2021→2024 跌幅≥10%」的堵点候选，"
        "含集中度、头部授权率与结构类型；但转化流量（转让命中 2.07%、无域字段）、市场融资（无域键）、"
        "政策 theme 空值（19,998/20,000）与链环运营数据四类归因证据均缺，故只能给候选面+框架，判部分支持。"
    ),
}

C.write_out(M, payload)
