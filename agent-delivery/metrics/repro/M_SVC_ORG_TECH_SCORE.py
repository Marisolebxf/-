#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""服务机构影响力（M_SVC_ORG_TECH_SCORE）—— gkx 口径，自包含。

五维口径（王惠 calc-logic 迁移稿）：专利有效件数 / 研发金额 / 研发人员数 /
可验证案例数 / 标准参与数 → 对比集合内 min-max → 等权平均 ×100，缺维不入平均。

gkx 实际可得：
    专利维   star_applicant_agg_gkx.json 的 agg[name]=[件数, 授权数]（按机构名对齐）
    研发维   a25_income.json（仅上市主体年报，3,180 行，按名称对齐）
    案例维   dwd_org_important_news_info 资讯条数（弱代理，曝光度≠成功案例）
    专家维   无（dwd_org_annual_financial_info.development_employee 整列为空）
    标准维   无承载表
产出：code/M_SVC_ORG_TECH_SCORE_out.json（覆盖写）
运行：cd code && python3 M_SVC_ORG_TECH_SCORE.py
"""
from __future__ import annotations

import json
import os
import statistics
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
STAR = os.path.join(SNAP, "star_applicant_agg_gkx.json")
INCOME = os.path.join(SNAP, "a25_income.json")
OUT = os.path.join(HERE, "M_SVC_ORG_TECH_SCORE_out.json")


def mm(vals):
    xs = list(vals.values())
    lo, hi = min(xs), max(xs)
    if hi - lo <= 1e-12:
        return {k: 0.5 for k in vals}
    return {k: (v - lo) / (hi - lo) for k, v in vals.items()}


def main() -> None:
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    star = json.load(open(STAR, encoding="utf-8"))["agg"]
    income = json.load(open(INCOME, encoding="utf-8"))["rows"]
    pool = f["pool"]

    rd = {}
    for r in income:
        if r.get("yffy") in (None, ""):
            continue
        y, v = str(r.get("hjnd")), float(r["yffy"])
        if r["jgmc"] not in rd or y > rd[r["jgmc"]][0]:
            rd[r["jgmc"]] = (y, v)

    dims = {
        "patents": {o: star[v["name"]][0] for o, v in pool.items()
                    if v["name"] in star and star[v["name"]][0] > 0},
        "rd": {o: rd[v["name"]][1] for o, v in pool.items()
               if v["name"] in rd and rd[v["name"]][1] > 0},
        "cases": {o: int(f["news"].get(o, 0)) for o in pool if f["news"].get(o, 0) > 0},
        "experts": {},
        "standards": {},
    }
    weights = {"patents": 0.2, "rd": 0.2, "cases": 0.2, "experts": 0.2, "standards": 0.2}
    norm = {k: mm(v) for k, v in dims.items() if v}

    idx, used = {}, {}
    for o in pool:
        av = [(k, norm[k][o]) for k in norm if o in norm[k]]
        if len(av) < 2:
            continue
        ws = sum(weights[k] for k, _ in av)
        idx[o] = 100.0 * sum(weights[k] * v for k, v in av) / ws
        used[o] = sorted(k for k, _ in av)

    vals = sorted(idx.values())
    bins = Counter(int(v // 10) * 10 for v in vals)
    top = sorted(idx.items(), key=lambda x: -x[1])[:10]

    out = {
        "metric_id": "M_SVC_ORG_TECH_SCORE",
        "metric_name": "服务机构影响力",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": (
            "五维中专利（52.97% 覆盖）、研发（仅上市主体 3.12%）、案例资讯代理（55.8%）三维可现转；"
            "专家维依赖的 development_employee 整列为空、标准维无承载表，两维始终缺，"
            "评分实为三维合成，按部分支持定档"),
        "wanghui": True,
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_patent（申请人聚合）", "rows": 2939895,
             "snapshot": "code/_snapshots21/star_applicant_agg_gkx.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_stock_finance_info（上市主体研发费用）", "rows": 3180,
             "snapshot": "code/_snapshots21/a25_income.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_important_news_info", "rows": 1668414,
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "截面评分：各维取当前存量/最近年报年，不做年度序列。"
            "专利件数为全量存量（dwd_patent.apdt_year 只有 2021—2026，不做年份拆分）；"
            "研发维取 2023/2024 年报最近值"),
        "population": {
            "distinct_org_id": len(pool),
            "scored_orgs": len(idx),
            "scored_share": round(len(idx) / len(pool), 6),
            "unscored_orgs": len(pool) - len(idx),
            "dim_count_dist": [[k, v] for k, v in sorted(Counter(len(u) for u in used.values()).items())],
            "scoring_basis": "缺维不入平均：按可用维权重重新归一（2 维各 50%，3 维各 33.3%）；不足 2 维不评分",
        },
        "dimensions": {
            k: {
                "n": len(v),
                "share": round(len(v) / len(pool), 6),
                "weight": weights[k],
                "status": ("可算" if k in ("patents", "rd", "cases") else "缺源"),
            } for k, v in dims.items()
        },
        "dimension_totals": {
            "patents_sum": sum(dims["patents"].values()),
            "patents_granted_sum": sum(star[pool[o]["name"]][1] for o in dims["patents"]),
            "patents_median": statistics.median(dims["patents"].values()),
            "patents_max": max(dims["patents"].values()),
            "rd_sum_yi": round(sum(dims["rd"].values()) / 1e8, 2),
            "rd_median_wan": round(statistics.median(dims["rd"].values()) / 1e4, 2),
            "cases_sum": sum(dims["cases"].values()),
            "cases_median": statistics.median(dims["cases"].values()),
        },
        "index": {
            "n": len(idx),
            "mean": round(statistics.mean(vals), 2),
            "median": round(statistics.median(vals), 2),
            "p90": round(vals[int(0.9 * len(vals))], 2),
            "max": round(vals[-1], 2),
            "min": round(vals[0], 2),
        },
        "score_bins": [[k, bins[k]] for k in sorted(bins)],
        "dim_combo": [["+".join(k), v] for k, v in
                      Counter(tuple(v) for v in used.values()).most_common()],
        "top10": [{
            "org_id": o, "name": pool[o]["name"], "city": pool[o]["city"],
            "score": round(s, 2),
            "dims": used[o],
            "patents": dims["patents"].get(o, 0),
            "rd": dims["rd"].get(o),
            "news": dims["cases"].get(o, 0),
        } for o, s in top],
        "difference_vs_old_draft": {
            "patents": "旧稿 35,838 家 / 483,225 件 → 本件 23,387 家 / 1,404,617 件",
            "rd": "旧稿研发金额 0 家 → 本件上市主体 1,376 家（仅上市口径，不能代表全池）",
            "experts": "旧稿 408 家（development_employee 异常值）→ 本件 0 家（该列整列为空）",
            "reason": ("换源后专利按全量申请人聚合对齐，覆盖与件数都放大；"
                       "研发维改用上市年报，覆盖从 0 到 3.12% 但只覆盖上市主体"),
        },
        "gaps": {
            "experts": "development_employee 整列为空（90,926 行非空 0），专家维不可算",
            "standards": "gkx 无标准起草单位表，标准维不可算",
            "cases": "资讯条数只是曝光度代理，不等于成功案例；负面新闻同样计入",
            "rd_scope": "研发金额仅上市主体年报，3.12% 覆盖，不能冒充全量企业研发投入",
            "skew": "min-max 原始值受头部极值支配，中位分 0.01，评分只适合作头部排序",
        },
        "compute": {"status": "ok", "elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("tech_score n=%d mean=%.2f max=%.2f top=%s -> %s"
          % (len(idx), out["index"]["mean"], out["index"]["max"],
             [(t["name"], t["score"]) for t in out["top10"][:3]], OUT))


if __name__ == "__main__":
    main()
