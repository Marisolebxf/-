#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_MARKET_GROWTH 产业链市场增长 —— gkx 三方库可行性否证脚本（20261021 改源版）

增长率的定义是「同一口径的规模量在两个时点的比」，因此它比 M_CHAIN_MARKET_SIZE 多两个必要条件：
  (a) 规模量本身成立（市场规模：完全不支持）；
  (b) 两期主体集合可比（同一批企业、同一量纲、连续年份）。
本脚本逐条体检 (b)，结论：连「两期可比」都不成立。

数据源（20261021 改源）：全部改直连三方库 gkx
  `gkx.dwd_org_annual_financial_info`（90,926 行，其中营收 >0 的 2,191 行）
  `gkx.dwd_org_base_info` / `gkx.dwd_org_industry_tags`（企业 → 属地 / 链归属）
旧版这里经开发库专用连接取数、并用本地 snapshot 面板；本版只读 gkx，不引用任何造数面，
公式与判定标准一律不动。

本脚本不输出增长率（输出即造假），只输出可比性体检与四档机判。
输出：code/M_CHAIN_MARKET_GROWTH_out.json
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _gkx21_common import (chain_names, ent_chain_map, org_index, q, q1)  # noqa: E402

OUT = HERE / "M_CHAIN_MARKET_GROWTH_out.json"


def main():
    rev = [{"org_id": r[0], "name_cn": r[1], "year": int(r[2]), "operating_revenue": float(r[3])}
           for r in q("SELECT org_id, name_cn, year, operating_revenue "
                      "FROM gkx.dwd_org_annual_financial_info "
                      "WHERE is_deleted=0 AND operating_revenue>0")]
    roots = chain_names()
    org2cc = {k: v[1] for k, v in org_index().items()}
    ent_chain = ent_chain_map()

    fin_rows = int(q1("SELECT COUNT(*) n FROM gkx.dwd_org_annual_financial_info WHERE is_deleted=0")[0])

    # 企业-年面板
    firm_years = defaultdict(set)
    firm_vals = defaultdict(dict)
    for r in rev:
        firm_years[r["org_id"]].add(int(r["year"]))
        firm_vals[r["org_id"]][int(r["year"])] = r["operating_revenue"]
    n_multi_year = sum(1 for v in firm_years.values() if len(v) >= 2)
    n_two_plus_consecutive = sum(1 for v in firm_years.values()
                                 if any((y + 1) in v for y in v))

    # 链级年份矩阵 + 同企同年配对
    per = defaultdict(lambda: defaultdict(list))
    for r in rev:
        cc = org2cc.get(r["org_id"])
        if not cc:
            continue
        for ch in ent_chain.get(cc, []):
            per[ch][int(r["year"])].append(r)

    chain_year = {}
    yoy_pairs = {}
    for c, name in roots.items():
        yrs = per.get(c, {})
        chain_year[c] = {
            "chain_name": name,
            "years": {str(y): len(v) for y, v in sorted(yrs.items())},
            "n_years_ge1": len(yrs),
            "n_years_ge5": sum(1 for v in yrs.values() if len(v) >= 5),
            "last_year": max(yrs) if yrs else None,
            "last_year_rows": len(yrs[max(yrs)]) if yrs else 0,
        }
        # 2019 年以来相邻两年「同一企业」配对数（可比增长的唯一合法样本）
        pairs = 0
        pair_detail = []
        for y in range(2019, 2025):
            a = {r["org_id"]: r for r in yrs.get(y, [])}
            b = {r["org_id"]: r for r in yrs.get(y + 1, [])}
            both = set(a) & set(b)
            pairs += len(both)
            if both:
                pair_detail.append({"pair": f"{y}->{y+1}", "n_same_firm": len(both)})
        yoy_pairs[c] = {"chain_name": name, "same_firm_pairs_2019_2025": pairs, "detail": pair_detail}

    # 全库 2023→2024 同企配对
    def pairs_between(y0, y1):
        a = {r["org_id"] for r in rev if r["year"] == y0}
        b = {r["org_id"] for r in rev if r["year"] == y1}
        return len(a & b)

    pair_2023_2024 = pairs_between(2023, 2024)
    pair_2022_2023 = pairs_between(2022, 2023)

    # 反证：用不同企业集合硬算 2023→2024 「增长」
    def chain_sum(c, y):
        return sum(r["operating_revenue"] for r in per.get(c, {}).get(y, []))

    naive_growth = {}
    for c, name in roots.items():
        s23, s24 = chain_sum(c, 2023), chain_sum(c, 2024)
        naive_growth[c] = {
            "chain_name": name,
            "sum_2023_yi": round(s23 / 1e8, 3),
            "sum_2024_yi": round(s24 / 1e8, 3),
            "n_2023": len(per.get(c, {}).get(2023, [])),
            "n_2024": len(per.get(c, {}).get(2024, [])),
            "naive_yoy_pct": (round(100 * (s24 - s23) / s23, 1) if s23 else None),
        }

    # 2024 全链覆盖（复用市场规模脚本的结论口径）
    r24 = [r for r in rev if r["year"] == 2024]
    mapped24 = [r for r in r24 if ent_chain.get(org2cc.get(r["org_id"], ""))]
    sum24_all = sum(r["operating_revenue"] for r in r24)
    sum24_map = sum(r["operating_revenue"] for r in mapped24)

    out = {
        "metric_id": "M_CHAIN_MARKET_GROWTH",
        "metric_name": "产业链市场增长",
        "generated_at": "2026-10-21",
        "data_source": {
            "engine": "三方库 gkx（183.240.141.251:3318），唯一连库入口 code/_gkxdb.py",
            "tables": ["gkx.dwd_org_annual_financial_info", "gkx.dwd_org_base_info",
                       "gkx.dwd_org_industry_tags"],
            "note": "旧版经开发库专用连接取数；本版全部改直连 gkx，口径与判定未改",
        },
        "metric_value": None,
        "value_null_reason": "增长率的两个前提（规模量成立、两期主体可比）均不成立；任何百分比都来自不同企业集合相减",
        "financial_table_rows": fin_rows,
        "revenue_positive_rows": len(rev),
        "firm_panel": {
            "distinct_firms": len(firm_years),
            "firms_with_ge2_years": n_multi_year,
            "firms_with_consecutive_years": n_two_plus_consecutive,
            "same_firm_pairs_2022_2023": pair_2022_2023,
            "same_firm_pairs_2023_2024": pair_2023_2024,
            "note": "同一企业连续两年都有正营收，是全库唯一可合法计算 YoY 的样本；2023→2024 只有 "
                    f"{pair_2023_2024} 对，2022→2023 只有 {pair_2022_2023} 对。",
        },
        "chain_year_matrix": chain_year,
        "same_firm_pairs_by_chain": yoy_pairs,
        "naive_growth_counterexample": naive_growth,
        "coverage_2024": {
            "rows": len(r24),
            "mapped_rows": len(mapped24),
            "sum_yi": round(sum24_all / 1e8, 1),
            "mapped_sum_yi": round(sum24_map / 1e8, 1),
            "mapped_share_pct": round(100 * sum24_map / sum24_all, 2) if sum24_all else None,
        },
        "why_no_growth": [
            "增长率要求同一口径两期相除。市场规模本身完全不支持（见 M_CHAIN_MARKET_SIZE），增长率无处附着。",
            "两期主体不可比：2023 年 45 条、2024 年 47 条营收记录分属不同企业；2023→2024 同企配对仅 "
            f"{pair_2023_2024} 对，2022→2023 仅 {pair_2022_2023} 对，不足以代表任何一条链。",
            "链级年份覆盖断裂：8/12 链 2024 年有记录，其中 4 条链 2024 年为 0；2019 年以前有量、2020 年后锐减，"
            "时间轴本身是「录入停摆」而非产业周期。",
            "即使强行相减，结果与产业事实冲突：2024 年人工智能链合计 38.2 亿、智能终端 8.2 亿，"
            "仅因为前者恰好有 6 家、后者 8 家可报营收企业；这不是增长，是样本更替。",
        ],
        "support_judgment": {
            "data_support_level": "完全不支持",
            "criteria": {
                "market_size_supported": False,
                "same_firm_pairs_2023_2024": pair_2023_2024,
                "chains_with_2024_revenue": sum(1 for c in roots if len(per.get(c, {}).get(2024, [])) > 0),
                "chains_with_adjacent_years_both_ge5": sum(
                    1 for c in roots if any(len(per.get(c, {}).get(y, [])) >= 5
                                            and len(per.get(c, {}).get(y + 1, [])) >= 5
                                            for y in range(2019, 2025))),
                "chains_with_adjacent_years_both_ge20": sum(
                    1 for c in roots if any(len(per.get(c, {}).get(y, [])) >= 20
                                            and len(per.get(c, {}).get(y + 1, [])) >= 20
                                            for y in range(2019, 2025))),
            },
            "reason": "市场规模型指标本身不成立；增长率还额外要求两期主体可比，而全库 2023→2024 同企配对只有 "
                      f"{pair_2023_2024} 对，12 条链中仅 8 条有 2024 年记录、4 条为 0。"
                      "结构与数据均不具备可算闭环 → 完全不支持。",
        },
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("firm_panel", "chain_year_matrix", "naive_growth_counterexample",
                                          "coverage_2024", "support_judgment")},
                     ensure_ascii=False, indent=1, default=str)[:5000])
    print("written", OUT)


if __name__ == "__main__":
    main()
