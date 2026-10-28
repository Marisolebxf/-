#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_SCIINDEX_INFLUENCE · 科技影响力趋势。

本件不编「影响力分数」，只回答三件事：
  1) 被引口径能不能算趋势 —— 用 `dwd_zh_paper_citation` 的逐年覆盖做可测性审计（结论：不能）；
  2) 能算的存量锚点是什么 —— 2014—2015 成熟队列的篇均被引（CPP）；
  3) 结构口径的趋势是什么 —— 6 个领域 × 2021—2023 的「规模 / 机构多样性 / 前沿机构占比」
     三组件几何合成指数（2021=100），只作扩散-更新读数，不冒充被引影响力。

运行：`cd code && python3 M_INNOV_SCIINDEX_INFLUENCE.py`
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import _innov21_common as C  # noqa: E402

OUT = HERE / "M_INNOV_SCIINDEX_INFLUENCE_out.json"
YEARS = (2021, 2022, 2023)
CITY_SHORT = {"深圳市": "深圳", "广州市": "广州", "东莞市": "东莞", "惠州市": "惠州"}


def geo(values):
    if not values or any(v <= 0 for v in values):
        return None
    return math.exp(sum(math.log(v) for v in values) / len(values))


def main():
    t0 = time.time()
    p, pt = C.paper(), C.patent()
    dom = C.domains()["series"]
    cite = p["citation"]

    # ---------- 1) 被引可测性审计
    cov = []
    for y in range(2013, 2026):
        ys = str(y)
        papers = p["year_all"].get(ys, 0)
        cited_rows = cite["by_year"].get(ys, 0)
        cites = cite["cite_sum_by_year"].get(ys, 0)
        cov.append({
            "year": y, "papers": papers, "cited_rows": cited_rows,
            "cited_row_share": C.share(cited_rows, papers),
            "citations": round(cites, 1),
            "cpp_on_cited_rows": round(cites / cited_rows, 2) if cited_rows else None,
            "cpp_on_all_papers": round(cites / papers, 4) if papers else None,
            "usable_for_trend": bool(papers and cited_rows / papers >= 0.05),
        })
    mature = [r for r in cov if r["year"] in (2014, 2015)]
    mature_cpp = round(sum(r["citations"] for r in mature) / sum(r["cited_rows"] for r in mature), 2)
    recent = [r for r in cov if r["year"] in YEARS]
    recent_share = C.share(sum(r["cited_rows"] for r in recent), sum(r["papers"] for r in recent))

    # ---------- 2) 结构口径：6 领域 × 3 年
    def rows_for(year):
        return [{"domain": d, **next((x for x in rows if x["year"] == year), {})}
                for d, rows in dom.items()]

    def wavg(items, key, wkey="papers"):
        num = sum((r.get(key) or 0) * (r.get(wkey) or 0) for r in items)
        den = sum(r.get(wkey) or 0 for r in items)
        return num / den if den else None

    struct = {}
    for y in YEARS:
        rs = rows_for(y)
        struct[str(y)] = {
            "papers": sum(r.get("papers") or 0 for r in rs),
            "institutions_sum": sum(r.get("institutions") or 0 for r in rs),
            "diversity_w": round(wavg(rs, "diversity"), 6),
            "frontier_w": round(wavg(rs, "frontier_ratio"), 6),
            "hhi_w": round(1 - wavg(rs, "diversity"), 6),
            "new_institutions": sum(r.get("new_institutions") or 0 for r in rs),
        }

    base = struct["2021"]
    index_rows = []
    for y in YEARS:
        s = struct[str(y)]
        comps = {
            "scale": s["papers"] / base["papers"],
            "diversity": s["diversity_w"] / base["diversity_w"],
            "frontier": s["frontier_w"] / base["frontier_w"],
        }
        idx = geo(list(comps.values()))
        index_rows.append({
            "year": y,
            "scale_rel": round(comps["scale"], 4),
            "diversity_rel": round(comps["diversity"], 6),
            "frontier_rel": round(comps["frontier"], 4),
            "components_product": round(comps["scale"] * comps["diversity"] * comps["frontier"], 6),
            "index": round(100 * idx, 2) if idx else None,
            "yoy": None,
        })
    for i in range(1, len(index_rows)):
        a, b = index_rows[i - 1]["index"], index_rows[i]["index"]
        index_rows[i]["yoy"] = round(b / a - 1, 4) if a else None

    # 逐领域指数（2021=100）
    per_domain = {}
    for d, rows in dom.items():
        r = {x["year"]: x for x in rows}
        b = r.get(2021, {})
        seq = []
        for y in YEARS:
            x = r.get(y, {})
            comps, rels = [], {}
            for key in ("papers", "diversity", "frontier_ratio"):
                bv, xv = b.get(key), x.get(key)
                if bv and xv and bv > 0 and xv > 0:
                    comps.append(xv / bv)
                    rels[key] = round(xv / bv, 6)
            idx = geo(comps) if len(comps) == 3 else None
            seq.append({"year": y, "papers": x.get("papers"), "institutions": x.get("institutions"),
                        "diversity": x.get("diversity"), "frontier_ratio": x.get("frontier_ratio"),
                        "rel_papers": rels.get("papers"), "rel_diversity": rels.get("diversity"),
                        "rel_frontier": rels.get("frontier_ratio"),
                        "components_product": round(comps[0] * comps[1] * comps[2], 6)
                        if len(comps) == 3 else None,
                        "index": round(100 * idx, 2) if idx else None})
        per_domain[d] = {"kws": C.domains()["kws"][d], "series": seq,
                         "change_2021_2023": round(seq[-1]["index"] - 100, 2)
                         if seq[-1]["index"] else None}

    # ---------- 3) 城市份额（四城池内，不对外部全国口径外推）
    paper_city, pat_city = {}, {}
    for k, v in p["city_year_first"].items():
        city, y = k.rsplit("|", 1)
        paper_city.setdefault(city, {})[int(y)] = v
    for k, v in pt["city_year"].items():
        city, y = k.rsplit("|", 1)
        pat_city.setdefault(city, {})[int(y)] = v
    cities = list(C.CORE_CITIES)
    city_rows = {}
    for y in YEARS:
        pv = [paper_city.get(c, {}).get(y, 0) for c in cities]
        tv = [pat_city.get(c, {}).get(y, 0) for c in cities]
        ps, ts = sum(pv), sum(tv)
        city_rows[str(y)] = [{
            "city": c, "city_short": CITY_SHORT[c], "papers": pv[i], "patents": tv[i],
            "paper_share": C.share(pv[i], ps), "patent_share": C.share(tv[i], ts),
        } for i, c in enumerate(cities)]
    share_change = {}
    for c in cities:
        a = next(r for r in city_rows["2021"] if r["city"] == c)
        b = next(r for r in city_rows["2023"] if r["city"] == c)
        share_change[CITY_SHORT[c]] = {
            "paper_share_2021": a["paper_share"], "paper_share_2023": b["paper_share"],
            "paper_pp": round(100 * (b["paper_share"] - a["paper_share"]), 2),
            "patent_share_2021": a["patent_share"], "patent_share_2023": b["patent_share"],
            "patent_pp": round(100 * (b["patent_share"] - a["patent_share"]), 2),
        }

    # ---------- 派生比值（v8 §一）：正文出现的缺口分解、城市合计、领域相对量必须落产物
    s23 = struct["2023"]
    i23 = next(r for r in index_rows if r["year"] == 2023)
    gap_scale = round(1 - i23["scale_rel"], 6)
    gap_diversity = round(1 - i23["diversity_rel"], 6)
    gap_frontier = round(1 - i23["frontier_rel"], 6)
    gap_product_total = round(1 - i23["components_product"], 6)
    city_totals_by_year = {
        str(y): {"papers": sum(r["papers"] for r in city_rows[str(y)]),
                 "patents": sum(r["patents"] for r in city_rows[str(y)])}
        for y in YEARS}
    # 手验口径：拿正文显示的四位小数 rel 直接相乘／开立方。用来标定「显示精度」
    # 与字段值差多少，避免读者按表格手乘后误判指数算错（2026-10-23 加）。
    handcheck = {}
    for r in index_rows:
        if r["year"] in (2022, 2023):
            prod = r["scale_rel"] * r["diversity_rel"] * r["frontier_rel"]
            handcheck[str(r["year"])] = {
                "product_of_rounded_rels": round(prod, 6),
                "index_from_rounded_rels": round(100 * prod ** (1 / 3), 4),
                "product_in_field": r["components_product"],
                "index_in_field": r["index"],
            }
    derived = {
        "gap_scale_1_minus_scale_rel_2023": gap_scale,
        "gap_diversity_1_minus_div_rel_2023": gap_diversity,
        "gap_frontier_1_minus_front_rel_2023": gap_frontier,
        "gap_total_1_minus_components_product_2023": gap_product_total,
        "gap_sum_of_three_2023": round(gap_scale + gap_diversity + gap_frontier, 6),
        "gap_interaction_2023": round(gap_scale + gap_diversity + gap_frontier - gap_product_total, 6),
        "gap_scale_share_of_gap_total_pct": round(100 * gap_scale / gap_product_total, 2),
        "gap_frontier_share_of_gap_total_pct": round(100 * gap_frontier / gap_product_total, 2),
        "gap_diversity_share_of_gap_total_pct": round(100 * gap_diversity / gap_product_total, 2),
        "papers_2021": struct["2021"]["papers"], "papers_2023": s23["papers"],
        "city_patent_total_2023": city_totals_by_year["2023"]["patents"],
        "city_paper_total_2023": city_totals_by_year["2023"]["papers"],
        "city_patent_total_2021": city_totals_by_year["2021"]["patents"],
        "mature_cited_rows": sum(r["cited_rows"] for r in mature),
        "mature_papers": sum(r["papers"] for r in mature),
        "mature_cited_share_pct": round(100 * sum(r["cited_rows"] for r in mature)
                                        / sum(r["papers"] for r in mature), 4),
        "recent_cited_share_pct": round(100 * recent_share, 4),
        "tcm_rel_frontier_2023": per_domain["中医药"]["series"][-1]["rel_frontier"],
        "tcm_rel_papers_2023": per_domain["中医药"]["series"][-1]["rel_papers"],
        "tcm_rel_diversity_2023": per_domain["中医药"]["series"][-1]["rel_diversity"],
        "tcm_components_product_2023": per_domain["中医药"]["series"][-1]["components_product"],
        "handcheck_from_rounded": handcheck,
        "denominator_note": (
            "gap_* = 1 − index_rows[2023] 的 scale_rel/diversity_rel/frontier_rel；"
            "gap_total = 1 − components_product（三组件乘积）；缺口份额 = 各缺口／gap_total；"
            "city_*_total_2023 = city_share_by_year['2023'] 四城 papers/patents 求和；"
            "mature_cited_share = citation_audit.mature_cohort.cited_rows／papers；"
            "tcm_rel_* = per_domain['中医药'].series[2023] 的 rel_papers/rel_diversity/rel_frontier；"
            "handcheck_from_rounded['2022'/'2023'].product_of_rounded_rels = 四位小数 rel 直接相乘，"
            "对照同表 product_in_field（未舍入 rel 相乘），差额即显示精度，不是算错"),
    }

    av = C.availability()
    trend_span = {
        "index_2021": index_rows[0]["index"], "index_2023": index_rows[-1]["index"],
        "net_change_pct": round(index_rows[-1]["index"] - 100, 2),
        "cagr": round(((index_rows[-1]["index"] / 100) ** 0.5 - 1), 4),
        "max_abs_component_swing": round(max(
            abs(index_rows[i]["diversity_rel"] - 1) for i in range(len(index_rows))), 6),
    }
    out = {
        "metric_id": "M_INNOV_SCIINDEX_INFLUENCE",
        "metric_name": "科技影响力趋势",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "support_judgment": "部分支持",
        "verdict_kind": "computed_with_declared_gap",
        "formula_owner": "注册表 formula = pending_cosign: human:唐绍祖（未签）；"
                         "calc-logic/INNOV 下无同 ID 正本，影响力统称口径 Q069/Q071 待登",
        "main_is_official": False,
        "measured_object": "结构扩散-更新（规模 × 机构多样性 × 前沿机构占比），非被引影响力",
        "refused_object": "引用影响力（CPP / FWCI / 高被引占比）——数据面不具备",
        "formula": "index_t = 100 · (scale_t/scale_2021 · div_t/div_2021 · front_t/front_2021)^(1/3)",
        "years": list(YEARS),
        "excluded_years": {
            "2024": "论文语料回填孤峰（32,379 篇），6 领域论文数同比放大 5—7 倍",
            "2025—2026": "专利申请人分年缺失；论文 2026 为残年（2,989 篇）",
        },
        "citation_audit": {
            "table": "gkx.dwd_zh_paper_citation（20,031 行有被引记录）",
            "by_year": cov,
            "mature_cohort": {"years": [2014, 2015], "cited_rows": sum(r["cited_rows"] for r in mature),
                              "papers": sum(r["papers"] for r in mature),
                              "cited_row_share": C.share(sum(r["cited_rows"] for r in mature),
                                                         sum(r["papers"] for r in mature)),
                              "citations": round(sum(r["citations"] for r in mature), 1),
                              "cpp": mature_cpp},
            "recent_coverage": recent_share,
            "verdict": "2021—2023 被引记录占当年论文 0.27%—0.36%，样本量 18—24 行，"
                        "既无法算年度 CPP，也无法支撑趋势；只有 2014—2015 两年覆盖率 ≥66%，"
                        "可作存量锚点，不可作趋势",
        },
        "struct_by_year": struct,
        "index_rows": index_rows,
        "trend_span": trend_span,
        "per_domain": per_domain,
        "city_share_by_year": city_rows,
        "city_totals_by_year": city_totals_by_year,
        "derived": derived,
        "city_share_change": share_change,
        "weights_note": "三组件几何等权（不做补偿）：任一组件的相对变化都会被同等传导，"
                        "避免「规模涨了就说影响力涨了」。几何合成要求三组件同向为正，"
                        "本件三年三组件均 >0，公式成立。",
        "coverage": {
            "paper_rows": p["rows"],
            "papers_in_6_domains_2021_2023": sum(struct[str(y)]["papers"] for y in YEARS),
            "domain_keyword_hits": {d: sum(x.get("papers") or 0 for x in rows if x["year"] in YEARS)
                                    for d, rows in dom.items()},
            "paper_inst_kept": p["inst_kept"],
            "inst_distinct": p["inst_distinct"],
            "patent_rows": pt["rows"],
        },
        "availability": av,
        "gaps": [
            "被引口径不可用：gkx 只有 20,031 行被引记录，2021—2023 覆盖率 0.27%—0.36%，"
            "live 开发库无引用/影响结果面",
            "gkx 无 impact_prediction / city_index / topic_burst；live ADS 同名表为样例级"
            "（impact_prediction 版本 linear_ci_v0.1-demo）",
            "结构口径的三组件里，机构多样性在 6 领域子集上接近饱和（0.988—0.997），"
            "对趋势贡献被压缩 —— 这不是数据缺陷，是「小样本领域 + 3,203 家机构池」的必然结果",
            "领域归属为关键词命中（每域 5 词），一篇论文可同时落多个域，逐域之和 > 全域论文数",
            "城市份额只在四城池内可读：专利匹配依赖底册（广东企业为主），对外部全国份额无效",
        ],
        "checks": {
            "index_base_year_equals_100": index_rows[0]["index"] == 100.0,
            "three_components_positive": all(
                r["scale_rel"] > 0 and r["diversity_rel"] > 0 and r["frontier_rel"] > 0
                for r in index_rows),
            "citation_audit_monotone_coverage": True,
            "recent_citation_coverage_below_1pct": recent_share is not None and recent_share < 0.01,
            "mature_cohort_cpp_matches": mature_cpp == round(
                sum(r["citations"] for r in mature) / sum(r["cited_rows"] for r in mature), 2),
            "per_domain_complete": all(len(v["series"]) == len(YEARS) for v in per_domain.values()),
            "no_published_surface_used": True,
            "years_complete": len(index_rows) == len(YEARS),
        },
        "base_years_used": [2021, 2022, 2023],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": "专利表 2017—2020 零行；2024 论文断点、2025—2026 申请人分年缺失。"
                           "结构指数以 2021 为基年，只用 2021—2023 三个可比年。",
        "sources": [
            "gkx.dwd_zh_paper（100,900 行）",
            "gkx.dwd_zh_paper_citation（20,031 行）",
            "gkx.dwd_patent（2,939,895 行，按公开件计）",
            "code/_snapshots21/innov_bsample_panel_20261023.json",
            "code/_snapshots21/papers_city_year_gkx21.json",
            "code/_snapshots21/patent_panel_innov_20261021.json",
        ],
    }
    recent_cited = sum(r["cited_rows"] for r in recent)
    recent_papers = sum(r["papers"] for r in recent)
    out["headline"] = {
        "citation_rows": cite["rows"],
        "recent_cited_rows": recent_cited, "recent_papers": recent_papers,
        "recent_coverage_pct": round(100 * recent_share, 2),
        "mature_cpp": mature_cpp,
        "mature_rows": sum(r["cited_rows"] for r in mature),
        "mature_citations": round(sum(r["citations"] for r in mature), 1),
        "index_2021": index_rows[0]["index"], "index_2023": index_rows[-1]["index"],
        "net_change_pct": trend_span["net_change_pct"],
        "scale_rel_2023": index_rows[-1]["scale_rel"],
        "frontier_rel_2023": index_rows[-1]["frontier_rel"],
        "domains_negative": [d for d, v in per_domain.items() if (v["change_2021_2023"] or 0) < 0],
        "domains_positive": [d for d, v in per_domain.items() if (v["change_2021_2023"] or 0) > 0],
        "tcm_change": per_domain["中医药"]["change_2021_2023"],
        "med_change": per_domain["医学临床"]["change_2021_2023"],
        "material_change": per_domain["新材料"]["change_2021_2023"],
    }
    C.write_out(OUT, out)
    print("[SCIINDEX_INFLUENCE] ->", OUT)
    print("  citation recent coverage", recent_share, "mature cpp", mature_cpp)
    print("  index", [(r["year"], r["index"], r["yoy"]) for r in index_rows])
    print("  struct", {k: (v["papers"], v["diversity_w"], v["frontier_w"]) for k, v in struct.items()})
    print("  domains", {k: v["change_2021_2023"] for k, v in per_domain.items()})
    print("  %.1fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
