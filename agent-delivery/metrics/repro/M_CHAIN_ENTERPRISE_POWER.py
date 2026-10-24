#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_ENTERPRISE_POWER 企业能力 — gkx 真源两维降级试算（20261021）

王惠口径（wanghui_agg.json，creator=王惠）：产业生态(企业数) / 企业营收 / 产业化程度(专利)
三维等权，同链同年度、对比区域截面 min-max 归一化 ×100；某维全同取 0.5。

实测约束（决定降为两维）：
  - 营收维：dwd_org_annual_financial_info 90,926 行仅 2,193 行 operating_revenue 非空（2.41%），
    2024 年正营收仅 47 家主体 → 不足以做 4 城 × 12 链截面
  - 专利维：dwd_patent 2,939,895 行，用 200k 样本（6.81%，按 dwd_id 截取非随机）匹配企业名
  - 企业数维：tags × base 流式归集，仅 4 城可归（base 命中 35,046 / 2,283,762 = 1.53%）

输出：M_CHAIN_ENTERPRISE_POWER_out.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _chain_common import write_out  # noqa: E402

METRIC = "M_CHAIN_ENTERPRISE_POWER"
NAME = "企业能力"
STREAM = Path(__file__).parent / "_snapshots" / "chain_h_stream_20261021.v1.json"
CITY4 = ["深圳市", "广州市", "东莞市", "惠州市"]


def minmax(vals: list[float]) -> list[float]:
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return [0.5] * len(vals)
    return [(v - lo) / (hi - lo) for v in vals]


def main() -> None:
    st = json.loads(STREAM.read_text(encoding="utf-8"))
    city4 = st["city4_chain"]
    pat = st["pat_city_chain"]
    total = st["total"]

    rows = []
    for code, n_total in total.items():
        cities = {}
        ec = [int(city4.get(c, {}).get(code, 0)) for c in CITY4]
        pc = [int(pat.get(code, {}).get(c, 0)) for c in CITY4]
        e_norm = minmax(ec)
        p_used = sum(pc) > 0
        p_norm = minmax(pc) if p_used else [0.5] * 4
        for i, c in enumerate(CITY4):
            dims = [("产业生态（企业数）", round(e_norm[i], 4))]
            if p_used:
                dims.append(("产业化程度（专利 200k 样本）", round(p_norm[i], 4)))
            score = sum(v for _, v in dims) / len(dims) * 100
            cities[c] = {
                "enterprise_count": ec[i],
                "enterprise_norm": round(e_norm[i], 4),
                "patent_sample_hits": pc[i],
                "patent_norm": round(p_norm[i], 4) if p_used else None,
                "dims_used": [k for k, _ in dims],
                "score": round(score, 2),
            }
        rows.append({"chain_code": code, "chain_name": None, "chain_total_national": n_total,
                     "cities": cities, "patent_dim_used": p_used,
                     "revenue_dim_used": False})
    rows.sort(key=lambda r: -r["cities"]["深圳市"]["score"])
    for i, r in enumerate(rows, 1):
        r["rank_sz"] = i

    report = {
        "metric_id": METRIC,
        "metric_name": NAME,
        "date": "2026-10-21",
        "data_source": "gkx schema gkx（dwd_org_industry_tags × dwd_org_base_info × dwd_patent 200k 样本）",
        "calc_logic_ref": "calc-logic/CHAIN/M_CHAIN_ENTERPRISE_POWER.md（王惠口径三维等权截面 min-max）",
        "note": ("王惠三维中营收维不足（非空 2,193/90,926 = 2.41%，2024 正营收主体 47 家），"
                 "降为『产业生态 + 产业化程度（专利样本）』两维等权试算；企业数维仅覆盖可归域子集 1.53%，"
                 "故本产物为方向性试算，不作正式 KPI 交付值。"),
        "probes": {
            "city4_covered_chains": len(rows),
            "base_join_hits": st["tags"]["base_hit"],
            "base_join_pct": st["tags"]["base_hit_pct"],
            "annual_fin_rows": 90926,
            "annual_fin_distinct_org": 8132,
            "annual_fin_revenue_nonnull": 2193,
            "annual_fin_revenue_nonnull_pct": round(2193 / 90926 * 100, 2),
            "annual_fin_2024_positive_orgs": 47,
            "patent_master_rows": 2939895,
            "patent_sample_rows": 200000,
            "patent_sample_rate_pct": round(200000 / 2939895 * 100, 2),
            "patent_sample_names": st["pat_sample_names"],
            "stream_elapsed_sec": st["elapsed_sec"],
        },
        "compute": {
            "cities": CITY4,
            "weights": "等权 0.5/0.5（王惠：默认等权，前端可调）",
            "dims_available": ["产业生态（企业数）", "产业化程度（专利 200k 样本）"],
            "dims_missing": ["企业营收（非空 2.41%，无法截面归一）"],
            "rows": rows,
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": ("产业生态维可算但仅覆盖可归域子集（35,046/2,283,762 = 1.53%），"
                       "营收维非空 2,193/90,926 行（2.41%）、2024 正营收仅 47 家，无法做 4 城 × 12 链截面归一；"
                       "专利维仅有 200k 样本（6.81%，非随机截取）作下限代理。"
                       "三维中一维受限、一维缺失、一维样本级，故为部分支持。"),
            "criteria": {"revenue_nonnull_pct": 2.41, "base_join_pct": st["tags"]["base_hit_pct"],
                         "patent_sample_rate_pct": 6.81},
        },
    }
    write_out(METRIC, report)
    for r in rows:
        print(r["chain_code"], {c: (v["enterprise_count"], v["score"]) for c, v in r["cities"].items()})


if __name__ == "__main__":
    main()
