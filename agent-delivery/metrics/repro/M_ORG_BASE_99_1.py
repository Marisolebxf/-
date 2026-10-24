#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ORG_BASE_99_1 · 科研机构基础指标模型构建（需规序号 99 / DS-01-FACTORS / TOPIC-ORG-05）

口径来源：需求原文四大维度（涉及产业领域 / 重点科研机构 / 科研机构资讯 / 新增科研机构动态），
王惠与 calc-logic 均未定义 → 本件为「推测定义」（wanghui=false），公式在 §1.6 写明。

单位：`gkx.dwd_research_institute_base_info` 2,074 家（广东省，深圳 1,014 / 广州 822 /
东莞 127 / 惠州 111）。四个维度分别落到论文关键词、项目学科、综合产出分位、成立年。

零 SQL：全部读 `code/_snapshots21/org_family_panel_20261021.json`
（由 `code/_build_org_family_panel.py` 一次性建成，见该脚本头部注释的取数清单）。

产物：`code/M_ORG_BASE_99_1_out.json`
"""
from __future__ import annotations

import json
import os
from collections import Counter, defaultdict

import _org_family_common as C

MID = "M_ORG_BASE_99_1"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, f"{MID}_out.json")


def main():
    panel = C.load_panel()
    inst = panel["institutions"]
    cov = panel["coverage"]

    # ---------- 维度 1：涉及产业领域（论文关键词 + 项目学科） ----------
    dom_share = defaultdict(Counter)
    org_domains = {}
    for i in inst:
        c = Counter()
        for kw in i.get("kw_top") or []:
            d = C.domain_of(kw)
            if d:
                c[d] += 1
        d = C.domain_of(i.get("discipline_top"))
        if d:
            c[d] += 3  # 项目学科比单个关键词更接近「领域」判断，权重 3
        if c:
            org_domains[i["name"]] = c.most_common(1)[0][0]
            for k, v in c.items():
                dom_share[i["city"]][k] += v
    n_domain = len(org_domains)
    dom_total = {c: sum(dom_share[c].values()) for c in C.CITY_ORDER}
    dom_top = {c: dom_share[c].most_common(3) for c in C.CITY_ORDER}

    # ---------- 维度 2：重点科研机构（产出分位阈值） ----------
    for i in inst:
        i["_core"] = i["patents"] + 2 * i["papers"] + i["projects"]
    sig = [i for i in inst if C.signal_count(i) > 0]
    core_vals = sorted(i["_core"] for i in sig if i["_core"] > 0)
    n = len(core_vals)
    p90 = core_vals[int(n * 0.9)] if n else 0
    key_orgs = [i for i in sig if i["_core"] > 0 and i["_core"] >= p90]
    abs_rule = [i for i in inst if i["patents"] >= 50 or i["papers"] >= 30 or i["projects"] >= 20]

    # ---------- 维度 3：综合科研实力（分位合成） ----------
    for i in inst:
        i["_sig"] = C.signal_count(i)
    pool = [i for i in inst if i["_sig"] > 0]
    for key, col in (("pat", "patents"), ("pap", "papers"),
                     ("prj", "projects"), ("sch", "scholars")):
        rk = C.pct_rank([i[col] for i in pool])
        for i, r in zip(pool, rk):
            i["_" + key] = r
    for i in pool:
        i["_strength"] = round(0.35 * i["_pat"] + 0.35 * i["_pap"]
                               + 0.20 * i["_prj"] + 0.10 * i["_sch"], 2)
    strength = sorted((i for i in pool if i["_core"] > 0), key=lambda x: -x["_strength"])

    # ---------- 维度 3b：趋势（论文 3 年对 3 年，只用真实完整年） ----------
    BASE = ["2016", "2017", "2018"]
    LATE = ["2021", "2022", "2023"]
    EXCLUDED = {"2024": "整批补录（匹配集 1,159 篇，是 2023 年 205 篇的 5.65 倍，非真实增长）",
                "2025": "残年（全表 6,548 篇，采集未收全）",
                "2026": "残年（全表 2,989 篇，截至 2026-10）"}

    def ymean(i, ys):
        vs = [i["papers_year"].get(y) for y in ys]
        vs = [v for v in vs if v is not None]
        return sum(vs) / len(vs) if vs else None

    movers = []
    for i in pool:
        b, l = ymean(i, BASE), ymean(i, LATE)
        if b and l and b >= 2:
            movers.append({"name": i["name"], "city": i["city"],
                           "base": round(b, 1), "late": round(l, 1),
                           "growth_pct": round((l - b) / b * 100, 1)})
    movers.sort(key=lambda x: -x["growth_pct"])

    # ---------- 维度 4：新增科研机构（成立年） ----------
    yr = Counter()
    yr_city = defaultdict(Counter)
    for i in inst:
        y = i.get("inc_year")
        if y:
            yr[y] += 1
            yr_city[y][i["city"]] += 1
    years = [str(y) for y in range(2001, 2027)]
    yearly = {y: yr.get(y, 0) for y in years}
    yearly_city = {y: {c: yr_city[y].get(c, 0) for c in C.CITY_ORDER} for y in years}
    peak_year = max(yearly, key=lambda y: yearly[y])

    # ---------- 区域汇总 ----------
    reg = []
    for c in C.CITY_ORDER:
        sub = [i for i in inst if i["city"] == c]
        reg.append({
            "city": c, "orgs": len(sub),
            "with_signal": sum(1 for i in sub if i["_sig"] > 0),
            "patents": sum(i["patents"] for i in sub),
            "papers": sum(i["papers"] for i in sub),
            "projects": sum(i["projects"] for i in sub),
            "scholars": sum(i["scholars"] for i in sub),
            "key_orgs": sum(1 for i in key_orgs if i["city"] == c),
        })

    out = {
        "metric_id": MID,
        "metric_name": "科研机构基础指标模型构建",
        "support_judgment": "部分支持",
        "generated_from": "code/_snapshots21/org_family_panel_20261021.json",
        "panel_built_at": panel["built_at"],
        "unit": "gkx.dwd_research_institute_base_info 2,074 家（广东四市）",
        "dimensions": {
            "D1_industry_domain": {"available": True, "orgs": n_domain,
                                   "share_note": "领域权重 = 论文关键词命中数 + 3×项目学科"},
            "D2_key_org": {"available": True, "rule": "综合产出(专利+2×论文+项目) ≥ 信号正集 P90",
                           "p90": p90, "count": len(key_orgs), "abs_rule_count": len(abs_rule)},
            "D3_strength": {"available": True, "scored_orgs": len(strength)},
            "D3_trend": {"available": True, "base_years": BASE, "late_years": LATE,
                         "excluded_years": EXCLUDED, "movers_n": len(movers)},
            "D4_new_org": {"available": True, "years": years, "peak_year": peak_year},
        },
        "coverage": cov,
        "base_years_used": BASE + LATE,
        "base_years_missing": [],
        "excluded_years": EXCLUDED,
        "region": reg,
        "domain_by_city": {c: {"total": dom_total[c], "top3": dom_top[c],
                               "share": {k: round(v / dom_total[c] * 100, 2)
                                         for k, v in dom_share[c].most_common()}
                               if dom_total[c] else {}} for c in C.CITY_ORDER},
        "key_orgs": [{"name": i["name"], "city": i["city"], "org_type": i["org_type"],
                      "patents": i["patents"], "papers": i["papers"],
                      "projects": i["projects"], "scholars": i["scholars"],
                      "core": i["_core"], "strength": i.get("_strength")}
                     for i in sorted(key_orgs, key=lambda x: -x["_core"])[:40]],
        "top_strength": [{"name": i["name"], "city": i["city"], "strength": i["_strength"],
                          "patents": i["patents"], "papers": i["papers"],
                          "projects": i["projects"], "scholars": i["scholars"]}
                         for i in strength[:30]],
        "new_org_yearly": yearly,
        "new_org_yearly_city": yearly_city,
        "fast_growth": movers[:20],
        "gaps": [
            "D1 产业链领域：dwd_org_industry_tags 32,322 家标签库与本底册按 org_id 仅 1 家可连，"
            "credit_code 与底册命中率 3.5%，故产业领域只能用论文关键词+项目学科反推，不是产业链口径",
            "D3 资讯：dwd_org_important_news_info 1,668,414 行为上市公司公告类资讯，"
            "按 name_cn 与 2,074 家机构仅 6 条命中，资讯维不可用",
            "D3 影响力：dwd_zh_paper_citation 20,031 行中 19,249 行（96.10%）的 id 回连不到 dwd_zh_paper",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)

    print(f"{MID}: 机构 {len(inst)}，有信号 {len(sig)}，重点机构 {len(key_orgs)}（P90={p90}）")
    print(f"  领域可判 {n_domain} 家；实力出分 {len(strength)} 家；增速可算 {len(movers)} 家")
    print(f"  新增机构峰值年 {peak_year}：{yearly[peak_year]} 家")
    print(f"  -> {OUT}")


if __name__ == "__main__":
    main()
