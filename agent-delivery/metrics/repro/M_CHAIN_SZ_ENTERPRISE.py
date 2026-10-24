#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_SZ_ENTERPRISE · 深圳企业维度（四城对标，2026-10-21）

王惠口径（M_CHAIN_SZ_ENTERPRISE V2-20260819，源码表见 calc-logic）：
  企业维度 =（企业数量 + 企业规模 + 企业质量）/ 3
    企业数量 = 链上该市企业去重数（credit_code）
    企业规模 = 该市该链企业营收合计（年报 operating_revenue）
    企业质量 = 该市该链上市企业研发强度 = Σ研发投入 / Σ营业收入
  三个三级指标先在四城集合上 min-max 到 0–100，再等权合成。

输入：_snapshots/sz_chain_matrix_20261021.json
输出：code/M_CHAIN_SZ_ENTERPRISE_out.json
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _sz5_common as S  # noqa: E402

METRIC = "M_CHAIN_SZ_ENTERPRISE"
NAME = "深圳企业维度"


def main():
    t0 = time.time()
    m = S.load_matrix()
    chains = S.chains(m)
    per_chain, detail = [], []
    for c, nm in chains:
        cnt = {city: m["ent_city_base"][c][city] for city in S.CITY4}
        rev = {city: m["revenue"]["by_chain_city_yi"][c][city] for city in S.CITY4}
        revn = {city: m["revenue"]["by_chain_city_n"][c][city] for city in S.CITY4}
        rdc = m["rd"]["by_chain_city"][c]
        inten = {city: (rdc[city]["intensity_pct"] or 0.0) for city in S.CITY4}
        rdn = {city: rdc[city]["n"] for city in S.CITY4}

        s_cnt, meta_cnt = S.minmax(cnt)
        s_rev, meta_rev = S.minmax(rev)
        s_int, meta_int = S.minmax(inten)
        scores = {city: round((s_cnt[city] + s_rev[city] + s_int[city]) / 3, 2) for city in S.CITY4}

        per_chain.append({
            "industry_code": c, "industry_name": nm,
            "sz_dim_score": scores["深圳市"],
            "city_scores": scores,
            "sz_rank_4c": 1 + sum(1 for x in scores.values() if x > scores["深圳市"]),
            "sz_components": {"count": s_cnt["深圳市"], "scale": s_rev["深圳市"], "quality": s_int["深圳市"]},
        })
        detail.append({
            "industry_code": c, "industry_name": nm,
            "raw": {"count": cnt, "revenue_yi": rev, "rd_intensity_pct": inten},
            "coverage": {"revenue_orgs": revn, "rd_orgs": rdn},
        })

    per_chain.sort(key=lambda r: -r["sz_dim_score"])
    vals = [r["sz_dim_score"] for r in per_chain]
    ranks = [r["sz_rank_4c"] for r in per_chain]
    rep = {
        "metric_id": METRIC, "metric_name": NAME, "date": "2026-10-21",
        "calc_logic_ref": "metrics/calc-logic/CHAIN/M_CHAIN_SZ_ENTERPRISE.md (V2-20260819)",
        "formula": "企业维度 =（数量得分 + 规模得分 + 质量得分）/ 3，各三级在四城集合 min-max 至 0–100",
        "per_chain": per_chain,
        "detail": detail,
        "stats_sz": S.stats(vals),
        "rank_distribution": {k: ranks.count(k) for k in sorted(set(ranks))},
        "coverage": {
            "base_sz": 95600,
            "sz_companies_with_revenue": sum(m["revenue"]["by_chain_city_n"][c]["深圳市"] for c, _ in chains),
            "revenue_orgs_total_4c": m["revenue"]["n_orgs"],
            "rd_orgs_total_4c": m["rd"]["n_orgs"],
            "note": "营收/研发投入只覆盖有年报或上市财务记录的企业；同一企业取最新年度/最新报告期，"
                    "跨企业年份不一致，非单一统计年。",
        },
        "elapsed_sec": round(time.time() - t0, 1),
    }
    rep["support_judgment"] = {
        "data_support_level": "部分支持",
        "reason": ("企业数量维可用底册现算（12 链 100–8,402 家）；企业规模维虽有真实年报营收，"
                   "但四城合计仅 1,225 家企业有正营收（占底册 0.65%），深圳仅 0.94%（901/95,600）；"
                   "企业质量维仅 876 家上市企业有研发投入记录（深圳 559 家）。"
                   "三个三级中两个是稀疏样本聚合，城市间排序由个别龙头是否入库决定，"
                   "不满足『依赖维都能得到足够数据』，故判『部分支持』。"),
        "criteria": {"chains": len(per_chain), "sz_dim_min": min(vals), "sz_dim_max": max(vals),
                     "revenue_coverage_pct_of_base": round(100 * m["revenue"]["n_orgs"] / 189115, 2),
                     "rd_coverage_orgs": m["rd"]["n_orgs"],
                     "sparse_dims": ["企业规模", "企业质量"]},
    }
    S.write_out(METRIC, rep)
    print("stats_sz", rep["stats_sz"], "ranks", rep["rank_distribution"])
    for r in per_chain:
        print(f"  {r['industry_name']:10s} dim={r['sz_dim_score']:6.2f} rank={r['sz_rank_4c']} "
              f"comp={r['sz_components']} city={r['city_scores']}")


if __name__ == "__main__":
    main()
