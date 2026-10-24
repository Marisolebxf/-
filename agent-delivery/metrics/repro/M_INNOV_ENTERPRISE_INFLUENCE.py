#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_ENTERPRISE_INFLUENCE 企业影响力 —— 王惠三维口径（科技创新 / 成果转化 / 产业带动）。

数据全部落在《MOCK_TABLE_REGISTRY》白名单：
  科技创新：ods.dwd_patent(first_applicant_name, granted_number, apdt_year) + ods.dwd_zh_paper(author_info_list)
  成果转化：ods.dwd_patent(first_current_assignee_name≠first_applicant_name) + ods.dwd_patent_transfer
  产业带动：ods.dwd_org_subsidiary_info（按 name_cn 对齐；org_id 与底册不同源）
营收兜底：ods.dwd_org_annual_financial_info.operating_revenue 实测近乎全空（2025 年仅 34/6,908 行非空），不作兜底。

辅助（不进入主分）：产学研共著广度 —— 同篇论文内与「企业」共现的其他机构数，用于校验「影响力」的网络面。
"""
import os
import sys
import json
import math
import pickle
import statistics as st
from collections import Counter, defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(BASE, "_snapshots")
OUT = os.path.join(BASE, "M_INNOV_ENTERPRISE_INFLUENCE_out.json")


def load(name):
    return json.load(open(os.path.join(SNAP, name)))


def minmax(vals):
    lo, hi = min(vals), max(vals)
    if hi - lo < 1e-12:
        return [0.0] * len(vals)
    return [(v - lo) / (hi - lo) for v in vals]


def pct(vals, p):
    s = sorted(vals)
    k = (len(s) - 1) * p
    f, c = math.floor(k), math.ceil(k)
    return s[int(k)] if f == c else s[f] * (c - k) + s[c] * (k - f)


def parse_names(s):
    if not s:
        return []
    try:
        v = json.loads(s)
        return [x.get("name") for x in v if isinstance(x, dict) and x.get("name")]
    except Exception:
        return []


def main():
    orgs = load("innov_w6_orgs.json")
    pat = load("innov_w6_patent_applicants.json")
    asg = load("innov_w6_patent_assignee.json")
    tr = load("innov_w6_patent_transfer.json")
    sub = load("innov_w6_subsidiary.json")
    rev = load("innov_w6_revenue.json")

    pat_map = {r[0]: r[1:] for r in pat}          # name -> [n, y0, y1, n_2124, n_grant]
    asg_map = dict((r[0], r[1]) for r in asg)
    sub_map = dict((r[0], r[1]) for r in sub)
    org_names = {o[1] for o in orgs if o[1]}

    # 成果转化（转移表，名字为 JSON 数组）
    tr_map = Counter()
    tr_rows = 0
    for pn, before, after, d in tr:
        tr_rows += 1
        for nm in set(parse_names(before) + parse_names(after)):
            if nm in org_names:
                tr_map[nm] += 1

    # 论文维度：篇级去重 + 产学研共现宽度
    papers = pickle.load(open(os.path.join(SNAP, "papers_authors_20261021.pkl"), "rb"))
    paper_cnt = Counter()
    partner = defaultdict(set)
    paper_total = 0
    papers_with_org = 0
    papers_industry_academia = 0
    aff_fill = 0
    slots = 0
    for p in papers:
        paper_total += 1
        affs = []
        for a in p.get("authors") or []:
            slots += 1
            if isinstance(a, (list, tuple)) and len(a) > 1 and a[1]:
                aff_fill += 1
                affs.append(a[1])
        if not affs:
            continue
        uniq = set(affs)
        hit = uniq & org_names
        if hit:
            papers_with_org += 1
        has_co = any(("公司" in x) or ("集团" in x) for x in uniq)
        has_uni = any(("大学" in x) or ("学院" in x) or ("研究所" in x) or ("研究院" in x) for x in uniq)
        if has_co and has_uni:
            papers_industry_academia += 1
        for nm in hit:
            paper_cnt[nm] += 1
            for other in uniq:
                if other != nm:
                    partner[nm].add(other)

    rows = []
    for o in orgs:
        oid, name, prov, city, ind = o[0], o[1], o[2], o[3], o[4]
        p = pat_map.get(name)
        n_pat = p[0] if p else 0
        n_paper = paper_cnt.get(name, 0)
        n_trans = asg_map.get(name, 0) + tr_map.get(name, 0)
        n_sub = sub_map.get(name, 0)
        rows.append({"org_id": oid, "name": name, "province": prov, "city": city, "industry": ind,
                     "patents": n_pat, "patents_2124": p[3] if p else 0, "granted": p[4] if p else 0,
                     "papers": n_paper, "transfers": n_trans, "subsidiaries": n_sub,
                     "partners": len(partner.get(name, ())),
                     "rev": 0.0})
    rev_map = {r[0]: r[2] for r in rev}  # 仅 1,302 条，占位

    def wins(vals, p=0.999):
        pos = sorted(v for v in vals if v > 0)
        cap = pos[int(p * (len(pos) - 1))] if pos else 0
        return [min(v, cap) for v in vals], cap

    d1_raw = [r["patents"] + r["papers"] for r in rows]
    d2_raw = [r["transfers"] for r in rows]
    d3_raw = [r["subsidiaries"] for r in rows]
    w1, c1 = wins(d1_raw)
    w2, c2 = wins(d2_raw)
    w3, c3 = wins(d3_raw)
    n1 = minmax([math.log1p(v) for v in w1])
    n2 = minmax([math.log1p(v) for v in w2])
    n3 = minmax([math.log1p(v) for v in w3])
    for i, r in enumerate(rows):
        r["d1"] = round(n1[i] * 100, 2)
        r["d2"] = round(n2[i] * 100, 2)
        r["d3"] = round(n3[i] * 100, 2)
        r["score"] = round((n1[i] + n2[i] + n3[i]) / 3 * 100, 2)
    scored = [r["score"] for r in rows]
    top = sorted(rows, key=lambda x: -x["score"])[:20]
    nonzero = sum(1 for s in scored if s > 0)

    # 辅助校验：产学研共著广度 vs 主分
    with_partner = [r for r in rows if r["partners"] > 0]
    def corr(a, b):
        n = len(a)
        ma, mb = sum(a) / n, sum(b) / n
        c = sum((x - ma) * (y - mb) for x, y in zip(a, b)) / n
        sa = math.sqrt(sum((x - ma) ** 2 for x in a) / n)
        sb = math.sqrt(sum((y - mb) ** 2 for y in b) / n)
        return round(c / (sa * sb), 4) if sa and sb else 0.0
    r_net = corr([r["score"] for r in with_partner], [r["partners"] for r in with_partner]) if len(with_partner) > 2 else 0
    r_pat_paper = corr([r["patents"] for r in rows if r["patents"] > 0 and r["papers"] > 0],
                       [r["papers"] for r in rows if r["patents"] > 0 and r["papers"] > 0]) if True else 0

    def slim(r, keys=("org_id", "name", "city", "industry", "patents", "papers", "transfers",
                      "subsidiaries", "partners", "d1", "d2", "d3", "score")):
        return {k: r[k] for k in keys}

    res = {
        "metric_id": "M_INNOV_ENTERPRISE_INFLUENCE",
        "name": "企业影响力",
        "formula_owner": "王惠",
        "unit": "企业（ods.dwd_org_base_info 底册 189,116 家，按 name_cn 对齐）",
        "method": {
            "formula": "Score = 100*(minmax(log1p(D1)) + minmax(log1p(D2)) + minmax(log1p(D3)))/3",
            "D1_tech": "专利去重件数(first_applicant_name) + 论文篇数(作者单位对齐)",
            "D2_transfer": "现权利人≠原始申请人的专利件数 + 专利转移表记录数",
            "D3_drive": "子公司去重数（营收兜底不可用）",
            "deviation": "王惠原文为线性极值归一；因专利/子公司呈重尾（华为 81,376 件、万科 3,819 家子公司），"
                         "改为「P99.9 缩尾 + log1p + min-max」，权重仍为三维等权，属实现适配而非口径改变",
            "winsor_caps": {"D1": c1, "D2": c2, "D3": c3},
        },
        "coverage": {
            "orgs": len(rows),
            "patent_hit_orgs": sum(1 for r in rows if r["patents"] > 0),
            "patent_hit_rate": round(sum(1 for r in rows if r["patents"] > 0) / len(rows) * 100, 2),
            "paper_hit_orgs": sum(1 for r in rows if r["papers"] > 0),
            "transfer_hit_orgs": sum(1 for r in rows if r["transfers"] > 0),
            "transfer_hit_rate": round(sum(1 for r in rows if r["transfers"] > 0) / len(rows) * 100, 2),
            "subsidiary_hit_orgs": sum(1 for r in rows if r["subsidiaries"] > 0),
            "subsidiary_hit_rate": round(sum(1 for r in rows if r["subsidiaries"] > 0) / len(rows) * 100, 2),
            "revenue_available_orgs": len(rev),
            "revenue_available_note": "operating_revenue 实测近乎全空，2025 年仅 34/6,908 行非空，兜底不可用",
        },
        "source_scale": {
            "patent_rows": 2939895, "patent_applicant_names": len(pat),
            "patent_covered_by_orgs": sum(r[1] for r in pat if r[0] in org_names),
            "transfer_rows": tr_rows, "transfer_names_matched": len(tr_map),
            "assignee_transfer_names": len(asg), "assignee_transfer_matched": len([1 for k in asg_map if k in org_names]),
            "subsidiary_rows": 178900, "subsidiary_parents": len(sub),
            "papers": paper_total, "author_slots": slots, "affiliation_fill": round(aff_fill / max(slots, 1) * 100, 2),
            "papers_with_org": papers_with_org, "papers_industry_academia": papers_industry_academia,
        },
        "stats": {"n": len(scored), "nonzero": nonzero, "min": round(min(scored), 2), "max": round(max(scored), 2),
                  "mean": round(sum(scored) / len(scored), 2), "median": round(st.median(scored), 2),
                  "p90": round(pct(scored, 0.9), 2), "p99": round(pct(scored, 0.99), 2),
                  "ge50": sum(1 for s in scored if s >= 50), "ge70": sum(1 for s in scored if s >= 70)},
        "top20": [slim(r) for r in top],
        "network_check": {
            "orgs_with_partners": len(with_partner),
            "corr_score_partner_breadth": r_net,
            "corr_patents_papers": r_pat_paper,
            "top_partner_orgs": [{k: r[k] for k in ("name", "partners", "papers", "patents", "score")}
                                 for r in sorted(with_partner, key=lambda x: -x["partners"])[:10]],
            "note": "产学研共著广度由 dwd_zh_paper.author_info_list 同篇机构共现抽取；仅作网络面校验，不进入主分",
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": "科技创新维全量可得（专利率 83.23% 企业命中、论文 7,820 家命中）；"
                      "成果转化维真实但覆盖仅 2.88% 企业（专利转移 22,809 行 + 现权利人变更 26,504 个主体）；"
                      "产业带动维子公司覆盖 11.58%、营收兜底近乎全空。三维中两维覆盖不足，按四档口径判「部分支持」，"
                      "不得因代码跑通而升「完全转换支持」。",
            "criteria": {"structure": "dwd_patent / dwd_zh_paper / dwd_patent_transfer / dwd_org_subsidiary_info 四表齐备",
                         "volume": "专利 293.99 万件、论文 10.09 万篇、转移 2.28 万行、子公司 17.89 万行",
                         "reproducible": True,
                         "distribution_discriminative": True,
                         "d2_coverage": 2.88, "d3_coverage": 11.58, "revenue_fallback": False},
        },
    }
    json.dump(res, open(OUT, "w"), ensure_ascii=False, indent=1, default=str)
    print("coverage", json.dumps(res["coverage"], ensure_ascii=False))
    print("stats", res["stats"], "net", res["network_check"]["orgs_with_partners"], r_net)
    for r in top[:8]:
        print(" ", r["name"], r["patents"], r["papers"], r["transfers"], r["subsidiaries"], r["score"])
    print("wrote", OUT)


if __name__ == "__main__":
    main()
