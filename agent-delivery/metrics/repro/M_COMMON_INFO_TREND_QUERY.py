#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_COMMON_INFO_TREND_QUERY · 共性信息趋势查询（gkx 单库代理版）

要做什么
--------
给定一条产业链（或一个关键词），返回「信息量随时间的走势」：逐月条数、环比、
峰值月、来源分布。它是趋势查询服务，不是一个固定的年度指标，所以交付物是
「可查询的月度序列 + 查询口径」，而不是单个分数。

数据事实
--------
`enterprise_news_stat` 结果面在 gkx 不存在（source_absent，见 TABLE_ABSENCE_EVIDENCE
§enterprise_news_stat）。可用的两张原始表：
  - `dwd_industry_chain_news_info` 108,052 行，字段 pk_id / industry_code(JSON 数组) /
    industry_name / title / publish_date / source，日期只覆盖 2025—2026（64,958 + 43,094）；
  - `dwd_news_base` 20,000 行，2018-06-01 至 2026-05-08，5,066 个来源（仅聚合事实已落盘）。
链标签是多值（一条新闻打多个链码），所以「各链条数之和」远大于新闻条数，
查询必须按「是否命中该链」去重，不能把多标签直接相加。

输出：code/M_COMMON_INFO_TREND_QUERY_out.json
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_COMMON_INFO_TREND_QUERY_out.json"
METRIC = "M_COMMON_INFO_TREND_QUERY"


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def month_key(d: str) -> str:
    return str(d)[:7]


def main() -> None:
    news = load("news21_chain_items_20261022.json")
    rows = news["rows"]
    roots = {c["chain"]: c["name"] for c in load("chain_panel21.json")["chains"]}

    monthly_all = defaultdict(int)
    monthly_chain = defaultdict(lambda: defaultdict(int))
    src = Counter()
    months = set()
    codes_seen = set()
    for r in rows:
        d = month_key(r[4])
        monthly_all[d] += 1
        months.add(d)
        src[r[5]] += 1
        try:
            codes = json.loads(r[1])
        except Exception:
            codes = []
        for c in set(codes):
            codes_seen.add(c)
            if c in roots:
                monthly_chain[c][d] += 1

    months = sorted(months)
    n_codes = len(codes_seen)
    series_all = [{"month": m, "n": monthly_all[m]} for m in months]
    mom = []
    for i in range(1, len(series_all)):
        prev, cur = series_all[i - 1]["n"], series_all[i]["n"]
        mom.append({"month": series_all[i]["month"],
                    "mom": round(cur / prev - 1, 4) if prev else None})

    chain_rows = []
    for code in sorted(roots):
        ser = monthly_chain[code]
        vals = [ser.get(m, 0) for m in months]
        total = sum(vals)
        peak = max(months, key=lambda m: ser.get(m, 0)) if months else None
        chain_rows.append({
            "chain": code, "chain_name": roots[code], "news_total": total,
            "months_covered": sum(1 for v in vals if v),
            "peak_month": peak, "peak_n": ser.get(peak, 0) if peak else 0,
            "last_month_n": vals[-1] if vals else 0,
            "series": {m: ser.get(m, 0) for m in months},
        })
    chain_rows.sort(key=lambda r: -r["news_total"])

    yoy_ready = all(any(m.startswith(y) for m in months) for y in ("2025", "2026"))
    out = {
        "metric_id": METRIC,
        "metric_name": "共性信息趋势查询",
        "data_source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）+ code/_snapshots21/ 落盘快照",
        "formula": "series(chain, month) = COUNT(DISTINCT news) WHERE chain_code ∈ industry_code；环比 = 本月/上月-1；同比需同月两年齐全",
        "blocking_tables": {
            "enterprise_news_stat": {
                "triage": "source_absent",
                "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §enterprise_news_stat",
            }
        },
        "proxy_path": "dwd_industry_chain_news_info 逐月/逐链去重计数；dwd_news_base 作为长窗口旁证（2018-06 起）",
        "proxy_deviation": "链标签表只有 2025—2026 两年，只能出 18 个月、不能出同比；一条新闻多链标签，逐链计数按「命中即计」去重，链条数之和不可加；dwd_news_base 虽有 2018 起的窗口，但只有 20,000 行且无链标签，只能做总量旁证",
        "coverage": {
            "news_rows": len(rows),
            "months": [months[0], months[-1]] if months else [],
            "n_months": len(months),
            "distinct_sources": len(src),
            "distinct_chain_codes": n_codes,
            "yoy_available": False,
            "long_window_reference": {"table": "gkx.dwd_news_base", "rows": 20000,
                                      "window": ["2018-06-01", "2026-05-08"],
                                      "sources": 5066},
        },
        "monthly_total": series_all,
        "monthly_mom": mom,
        "top_sources": [{"source": s, "n": n} for s, n in src.most_common(10)],
        "chains": chain_rows,
        "query_spec": {
            "input": ["chain_code", "month_from", "month_to", "keyword?"],
            "output": ["month", "n", "mom", "peak", "source_top"],
            "dedup": "按 pk_id 去重，多链标签命中即计",
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": "enterprise_news_stat 结果面不存在，但趋势查询的原料齐全且是真数据：108,052 条带链标签的新闻、18 个月、206 个来源，逐月去重计数即可回答「某链信息量怎么走」。不能判完全转换支持的原因是时间窗只有 2025—2026：18 个月够看月度起伏与环比，但不够同比，也看不到 2018—2024 的长趋势（长窗口旁证表只有 20,000 行且无链标签）。故判部分支持。",
            "criteria": {
                "result_table_exists": False,
                "news_rows": len(rows),
                "months": len(months),
                "yoy_available": False,
                "chain_tagged": True,
                "proxy_used": True,
            },
        },
        "base_years_used": [2025, 2026],
        "base_years_missing": [2018, 2019, 2020, 2021, 2022, 2023, 2024],
        "base_years_note": "链标签新闻只有 2025—2026 两年（2026 截至 5 月），2018—2024 在链标签表里一行都没有——不是补 0，而是该表根本没有这些年份。dwd_news_base 有 2018-06 起的长窗口，但无链标签，只能做总量旁证，不能补链级序列。",
        "sources": [
            {"path": "code/_snapshots21/news21_chain_items_20261022.json",
             "table": "gkx.dwd_industry_chain_news_info", "rows": 108052,
             "role": "链标签新闻全量（月度序列唯一输入）"},
            {"path": "code/_snapshots21/proxy_facts_20261022.json",
             "table": "gkx.dwd_news_base", "rows": 20000,
             "role": "长窗口总量旁证（2018-06 起）"},
            {"path": "code/_snapshots21/chain_panel21.json",
             "table": "gkx.dwd_industry_chain_info", "rows": 12,
             "role": "12 链名称与链码"},
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[OK] {METRIC} -> {OUT.name} rows={len(rows)} months={len(months)} "
          f"span={months[0]}~{months[-1]} sources={len(src)}")
    for r in chain_rows[:5]:
        print(f"  {r['chain']} {r['chain_name'][:8]:<8} n={r['news_total']:<6} peak={r['peak_month']}")


if __name__ == "__main__":
    main()
