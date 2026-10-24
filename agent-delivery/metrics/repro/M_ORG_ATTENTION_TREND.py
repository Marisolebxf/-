#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ORG_ATTENTION_TREND · 科研关注度（趋势）

口径：需求文档只给「模型通过对区域创新科技/产业/人才/政策四大维度分析结果设计指标体系」
这一句战略描述，王惠与 calc-logic 均未定义 → 推测定义（wanghui=false），见 §1.6。

本件把「科研关注度」操作化为**机构在学术与政策两个注意力场里的年度曝光强度**：
  A_i = 0.65·pct(2016–2018 与 2021–2023 论文合计) + 0.20·pct(政策提及数) + 0.15·pct(科研项目数)
  trend_i = (2021–2023 年均论文) / (2016–2018 年均论文) − 1
区域序列 A_t = 当年论文数 + 当年政策提及数 + 当年项目数（分列给出，不强行合成一个跨源指数）。

只读面板，零 SQL。产物 `code/M_ORG_ATTENTION_TREND_out.json`。
"""
from __future__ import annotations

import json
import os
from collections import Counter, defaultdict

import _org_family_common as C

MID = "M_ORG_ATTENTION_TREND"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, f"{MID}_out.json")

BASE = ["2016", "2017", "2018"]
LATE = ["2021", "2022", "2023"]
EXCLUDED = {
    "2024": "论文整批补录（全表 32,379 篇，是 2023 年 6,651 篇的 4.87 倍；匹配集 1,159 对 205）",
    "2025": "残年（全表 6,548 篇，采集未收全）",
    "2026": "残年（全表 2,989 篇，截至 2026-10）",
}


def main():
    panel = C.load_panel()
    inst = panel["institutions"]
    cov = panel["coverage"]

    # ---------- 区域年度序列（三源分列，不做跨源合成分） ----------
    pap_yr = Counter()
    pol_yr = Counter()
    prj_yr = Counter()
    for i in inst:
        for y, v in i["papers_year"].items():
            pap_yr[y] += v
        for y, v in i["policy_year"].items():
            pol_yr[y] += v
        for y, v in i["projects_year"].items():
            prj_yr[y] += v
    years = [str(y) for y in range(2014, 2027)]
    region_series = {y: {"papers": pap_yr.get(y, 0), "policy_mentions": pol_yr.get(y, 0),
                         "projects": prj_yr.get(y, 0)} for y in years}

    # ---------- 机构级关注度 ----------
    pool = [i for i in inst if C.signal_count(i) > 0]
    for key, col in (("pap", None), ("pol", "policy_mentions"), ("prj", "projects")):
        if col is None:
            vals = [sum(i["papers_year"].get(y, 0) for y in BASE + LATE) for i in pool]
        else:
            vals = [i[col] for i in pool]
        rk = C.pct_rank(vals)
        for i, r in zip(pool, rk):
            i["_" + key] = r
    for i in pool:
        i["_paper_5y"] = sum(i["papers_year"].get(y, 0) for y in BASE + LATE)
        dims = {"pap": (i["_pap"], 0.65), "pol": (i["_pol"], 0.20), "prj": (i["_prj"], 0.15)}
        s, k = C.weighted(dims, None)
        i["_attn"] = s
        i["_dims"] = k

    scored = [i for i in pool if i["_attn"] is not None and i["_paper_5y"] > 0]
    scored.sort(key=lambda x: -x["_attn"])

    # ---------- 趋势（3 年对 3 年，只用真实完整年） ----------
    def ymean(i, ys):
        vs = [i["papers_year"].get(y) for y in ys]
        vs = [v for v in vs if v is not None]
        return sum(vs) / len(vs) if vs else None

    trend = []
    for i in pool:
        b, l = ymean(i, BASE), ymean(i, LATE)
        if b and b >= 2.0:   # 基期年均 <2 篇的增速是 1→3 这类噪声，单列不给增速
            trend.append({
                "name": i["name"], "city": i["city"],
                "base_1618": round(b, 2), "late_2123": round(l, 2) if l is not None else None,
                "growth_pct": round((l - b) / b * 100, 1) if l is not None else None,
                "attn": i["_attn"],
            })
    ups = sorted([t for t in trend if t["growth_pct"] is not None],
                 key=lambda x: -x["growth_pct"])
    downs = sorted([t for t in trend if t["growth_pct"] is not None],
                   key=lambda x: x["growth_pct"])

    # ---------- 区域级增速（同一 3 年对 3 年口径） ----------
    def rsum(ys, key):
        return sum(region_series[y][key] for y in ys)
    reg_growth = {}
    for key in ("papers", "policy_mentions", "projects"):
        b, l = rsum(BASE, key), rsum(LATE, key)
        reg_growth[key] = {
            "base_1618_sum": b, "late_2123_sum": l,
            "base_year_mean": round(b / 3, 2), "late_year_mean": round(l / 3, 2),
            "growth_pct": round((l - b) / b * 100, 2) if b else None,
        }

    # ---------- 集中度 ----------
    papers_all = sorted((i["_paper_5y"] for i in pool), reverse=True)
    tot = sum(papers_all)
    top10 = sum(papers_all[:10])
    top10_names = [i["name"] for i in sorted(pool, key=lambda x: -x["_paper_5y"])[:10]]
    conc = {
        "institutes_with_papers": sum(1 for i in inst if i["papers"] > 0),
        "papers_total_matched": sum(i["papers"] for i in inst),
        "papers_dedup": cov["papers_with_institute"],
        "paper_org_slots": cov["papers_with_institute"] + sum(1 for i in inst if i["papers"] > 0 and False),
        "top10_share_pct": round(top10 / tot * 100, 2) if tot else None,
        "hhi": round(sum((v / tot) ** 2 for v in papers_all) * 10000, 1) if tot else None,
        "top10_names": top10_names,
    }

    # ---------- 城市对比 ----------
    city = []
    for c in C.CITY_ORDER:
        sub = [i for i in inst if i["city"] == c]
        p = sum(i.get("_paper_5y", 0) for i in sub)
        city.append({"city": c, "orgs": len(sub),
                     "orgs_with_papers": sum(1 for i in sub if i["papers"] > 0),
                     "papers_2016_2023": p,
                     "policy_mentions": sum(i["policy_mentions"] for i in sub),
                     "attn_mean": round(sum(i["_attn"] for i in sub
                                            if i.get("_attn") is not None)
                                        / max(sum(1 for i in sub
                                                  if i.get("_attn") is not None), 1), 2)})

    # ---------- 权重敏感性（同一套分位，只换权重） ----------
    def rescore(w):
        out = {}
        for i in pool:
            d = {"pap": (i["_pap"], w[0]), "pol": (i["_pol"], w[1]), "prj": (i["_prj"], w[2])}
            s, k = C.weighted(d, None)
            if s is not None and i["_paper_5y"] > 0:
                out[i["name"]] = s
        return out

    base_map = {i["name"]: i["_attn"] for i in scored}
    names = list(base_map)
    sens = []
    for label, w in [("论文偏重", (0.85, 0.10, 0.05)), ("政策偏重", (0.45, 0.40, 0.15)),
                     ("项目偏重", (0.45, 0.15, 0.40)), ("等权", (0.34, 0.33, 0.33))]:
        am = rescore(w)
        common = [n for n in names if n in am]
        rho = C.spearman([base_map[n] for n in common], [am[n] for n in common])
        t10b = {n for n in sorted(names, key=lambda x: -base_map[x])[:10]}
        t10a = {n for n in sorted(am, key=lambda x: -am[x])[:10]}
        sens.append({"weights": label, "w": list(w), "spearman": rho,
                     "top10_overlap": len(t10b & t10a)})

    out = {
        "metric_id": MID,
        "metric_name": "科研关注度",
        "support_judgment": "部分支持",
        "generated_from": "code/_snapshots21/org_family_panel_20261021.json",
        "panel_built_at": panel["built_at"],
        "unit": "gkx.dwd_research_institute_base_info 2,074 家（广东四市）",
        "formula": "A_i = 0.65·pct(论文 2016–2023 合计) + 0.20·pct(政策提及) + 0.15·pct(项目数)，缺维重归一",
        "weights": {"papers": 0.65, "policy": 0.20, "projects": 0.15},
        "dims_impl": {
            "papers": "pct(2016–2018 + 2021–2023 论文篇次合计)",
            "policy": "pct(政策正文提及该机构名的次数)",
            "projects": "pct(获批项目数)",
        },
        "attn_dist": C.dist([i["_attn"] for i in scored]),
        "trend_table": sorted([t for t in trend if t["growth_pct"] is not None],
                              key=lambda x: -x["growth_pct"]),
        "sensitivity": sens,
        "base_years_used": BASE + LATE,
        "base_years_missing": [],
        "excluded_years": EXCLUDED,
        "coverage": cov,
        "region_series": region_series,
        "region_growth": reg_growth,
        "concentration": conc,
        "city": city,
        "scored_orgs": len(scored),
        "top_attention": [{"name": i["name"], "city": i["city"], "attn": i["_attn"],
                           "papers_2016_2023": i["_paper_5y"],
                           "policy_mentions": i["policy_mentions"],
                           "projects": i["projects"], "dims": i["_dims"]}
                          for i in scored[:30]],
        "trend_scored_orgs": len(trend),
        "top_gainers": ups[:15],
        "top_losers": downs[:10],
        "gaps": [
            "被引维断裂：dwd_zh_paper_citation 20,031 行中 19,249 行（96.10%）id 回连不到 dwd_zh_paper，"
            "匹配集 2,938 篇论文里只有 18 篇有被引数，无法充当关注度主口径",
            "新闻维断裂：dwd_org_important_news_info 1,668,414 行为上市公司公告类资讯，"
            "按 name_cn 连 2,074 家机构仅 6 条命中（5 家机构）",
            "下载维不可用：dwd_zh_paper.download_num 整列为 0（DATA_FACTS §3.10）",
            "项目维封顶：dwd_zh_project 匹配集 2021 年 27 项、2022 年 1 项，"
            "2023 年后无数据，不能用于 2023 年之后的趋势",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)

    print(f"{MID}: 出分机构 {len(scored)} / {len(inst)}；趋势可算 {len(trend)} 家")
    print("  区域增速（2016–18 → 2021–23）:", json.dumps(reg_growth, ensure_ascii=False))
    print(f"  集中度: top10 占 {conc['top10_share_pct']}%  HHI={conc['hhi']}")
    print(f"  -> {OUT}")


if __name__ == "__main__":
    main()
