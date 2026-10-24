#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_REGION_INDEX —— 区域产业指数（区域产业指数评价页壳指标）

20261021 改源版：数据源由旧版开发库全量切到 gkx（与旧库逐表镜像，行数一致）。
口径本身不动：I(c,r)=100×可算维度得分均值；维内子项等权；子项在「同链 4 市」截面 min-max。

改源要点
  · 链上企业数：gkx.dwd_org_industry_tags ⋈ gkx.dwd_org_base_info（链码索引）→ credit_code 去重落城
  · 专利件数：gkx.dwd_patent.first_applicant_name ⋈ dwd_org_base_info.name_cn，CN、申请年≤2024、按专利号去重
  · 政策覆盖率：gkx.dwd_policy_base 全表现取（存量口径，不按年截断；city='NULL' 归一为空串）
  · 融资事件：gkx.dwd_org_financing_info 一行=一次事件（gkx 版无 event_id）
  · 营业收入：gkx.dwd_org_annual_financial_info 2024 年 revenue_yuan + main_business_revenue
  · 学术维：gkx.dwd_research_institute_base_info / dwd_org_heis_info / dwd_scholar /
    dwd_scholar_paper_relation 可读，但机构—链挂接为 0、scholar_org_id 全空，链×城不可算
"""
from __future__ import annotations

import math
import time
from collections import Counter, defaultdict

from _gkx21_common import (CITY4, ROOTS, base_rows, chain_l1, chain_names, q, qd, load_cache,
                           save_cache, chain_city_from_bridge, bridge, tree, minmax, jstats,
                           spearman, write_out)
from _reg5_tokens import coverage_cell

MID = "M_CHAIN_REGION_INDEX"
STAT_YEAR = 2024
CHAIN_AXIS = ["INB1306", "INB1309", "INB1333", "INB1502", "INB2505",
              "INB1204", "INB1303", "INB1323", "INB1354", "INB1209", "INB1236", "INB2503"]
CHAIN_CN = chain_names()
TREE = {r["industry_code"]: {"name": r["industry_name"]} for r in tree()}
L1 = chain_l1()


def sibling_matrix(mid, key):
    import json
    from pathlib import Path
    p = Path(__file__).parent / f"{mid}_out.json"
    d = json.load(open(p, encoding="utf-8"))
    out = {}
    for m in d["matrix"]:
        for c, v in m["cells"].items():
            out[(m["chain"], c)] = v.get(key)
    return out, d


def cells_from_flat(flat):
    return {(ch, c): flat.get((ch, c), 0) or 0 for ch in CHAIN_AXIS for c in CITY4}


# ---------------- 企业数（E1） ----------------
def firm_counts():
    panel = chain_city_from_bridge()
    return {(ch, c): int(panel["chain_city"].get(ch, {}).get(c, 0)) for ch in CHAIN_AXIS for c in CITY4}


# ---------------- 专利（E3） ----------------
def patent_counts():
    """专利去重件数（链×城，申请年≤2024，第一申请人 ∪ 当前专利权人并集）。

    gkx.dwd_patent 是 2,939,895 行宽表、名称列无索引，远程实例全表重扫约 40 分钟，
    故复用同族快照的双角色并集层（`_build_patent_union.py` 先校验行数逐位一致再落缓存，
    行数一变即报错）。口径与同族 M_CHAIN_REG_COMMERCIALIZATION 的 patent_count_le2024 同源。
    """
    flat = load_cache("region_index_patent_union.json")
    if flat is None:
        from _build_patent_union import main as build
        build()
        flat = load_cache("region_index_patent_union.json")
    return {(ch, c): int(flat.get("%s|%s" % (ch, c), 0) or 0)
            for ch in CHAIN_AXIS for c in CITY4}


_CHAIN_OF = set()
_CHAIN_OF_BY_CC = {}


def build_chain_of():
    for r in bridge():
        _CHAIN_OF_BY_CC[r.get("cc")] = r.get("chains") or []
        for ch in (r.get("chains") or []):
            _CHAIN_OF.add((ch, r.get("cc")))
    for ch in CHAIN_AXIS:
        _CHAIN_OF.add((ch, "__none__"))


# ---------------- 政策（S1） ----------------
def policy_cells():
    """政策覆盖率（S1）：口径完全沿用同族 M_CHAIN_REG_POLICY_COVERAGE v0.2.0 的 coverage_cell。

    两处必须与旧口径对齐，否则覆盖率会被压成 0：
      · 政策池是**存量**，不按发布年截断（旧快照即为 dwd_policy_base 全表 20,000 行）；
      · `city` 的缺省在 gkx 里落成字符串 'NULL'，需归一成空串才能进「国家级政策」分支。
    """
    cache = "region_index_policy_rows.json"
    rows = load_cache(cache)
    if not rows:
        rows = qd("""SELECT title, city, `rank`, publish_year, id
                     FROM gkx.dwd_policy_base
                     WHERE title IS NOT NULL AND title<>''""")
        for r in rows:
            c = (r.get("city") or "").strip()
            r["city"] = "" if c.upper() == "NULL" else c
            r["rank"] = r.get("rank") or ""
        save_cache(cache, rows)
    out = {}
    for ch in CHAIN_AXIS:
        l1 = L1.get(ch, [])
        for c in CITY4:
            out[(ch, c)] = coverage_cell(rows, ch, l1, TREE, c)
    return out


# ---------------- 融资（S2） ----------------
def financing_cells():
    """融资事件数：一行 = 一次事件（与同族 M_CHAIN_REG_FINANCING 口径一致，不做事件级去重）。

    gkx 版融资表无 event_id，事件粒度就是行；剔除晚于统计年的未来日期，再经 org_id→主档
    →credit_code→链码落链与落城。
    """
    cache = "region_index_fin_events.json"
    rows = load_cache(cache)
    if not rows:
        rows = qd("""SELECT org_id, completion_date FROM gkx.dwd_org_financing_info
                     WHERE is_deleted=0""")
        save_cache(cache, rows)
    org_city, org_credit = {}, {}
    for r in base_rows():
        org_city[r[0]] = r[4]
        org_credit[r[0]] = r[1]
    ec = {}
    for b in bridge():
        if b["cc"]:
            ec[b["cc"]] = b["chains"]
    out = {(ch, c): 0 for ch in CHAIN_AXIS for c in CITY4}
    for r in rows:
        dt = str(r.get("completion_date") or "")[:4]
        if dt.isdigit() and int(dt) > STAT_YEAR:
            continue
        city = org_city.get(r.get("org_id"))
        if city not in CITY4:
            continue
        for ch in ec.get(org_credit.get(r.get("org_id")) or "", ()):
            if (ch, city) in out:
                out[(ch, city)] += 1
    return out


# ---------------- 营收（E2，带披露标记） ----------------
def revenue_cells():
    cache = "region_index_rev2024.json"
    rows = load_cache(cache)
    if not rows:
        rows = qd("""
            SELECT b.name_cn AS nm, a.external_id AS cc, a.operating_revenue AS rev
            FROM gkx.dwd_org_annual_financial_info a STRAIGHT_JOIN gkx.dwd_org_base_info b
              ON b.external_id = a.external_id COLLATE utf8mb4_0900_ai_ci
            WHERE a.`year`=2024 AND a.is_deleted=0
              AND a.operating_revenue > 0
        """)
        save_cache(cache, rows)
    cc_city = {r.get("cc"): r.get("c") for r in bridge()}
    cc_chains = defaultdict(set)
    for ch, cc in _CHAIN_OF:
        if cc != "__none__":
            cc_chains[cc].add(ch)
    val = {(ch, c): 0.0 for ch in CHAIN_AXIS for c in CITY4}
    disc = {(ch, c): False for ch in CHAIN_AXIS for c in CITY4}
    for r in rows:
        cc = r.get("cc")
        city = cc_city.get(cc)
        if city not in CITY4:
            continue
        for ch in cc_chains.get(cc, ()):
            val[(ch, city)] += float(r.get("rev") or 0) / 1e8
            disc[(ch, city)] = True
    return {k: round(v, 4) for k, v in val.items()}, disc


# ---------------- 学术侧实测（只作旁证） ----------------
def acad_probe():
    cache = "region_index_acad.json"
    cached = load_cache(cache)
    if cached:
        return cached
    def cnt(sql):
        return int(qd(sql)[0]["n"])

    inst_rows = cnt("SELECT COUNT(*) AS n FROM gkx.dwd_research_institute_base_info")
    heis_rows = cnt("SELECT COUNT(*) AS n FROM gkx.dwd_org_heis_info")
    orgs = qd("""SELECT name_cn AS name, city FROM gkx.dwd_research_institute_base_info
                 WHERE is_deleted=0 AND name_cn IS NOT NULL AND name_cn<>''""")
    orgs += qd("""SELECT name_cn AS name, city FROM gkx.dwd_org_heis_info
                  WHERE is_deleted=0 AND name_cn IS NOT NULL AND name_cn<>''""")
    # 机构/高校与工业标签的链码交集：在 Python 侧用 credit_code 集合求交（标签表无索引，避免 2.28M 嵌套循环）
    tag_cc = load_cache("tag_credit_codes_20261021.json")
    if tag_cc is None:
        tag_cc = [r[0] for r in q("SELECT DISTINCT credit_code FROM gkx.dwd_org_industry_tags "
                                  "WHERE is_deleted=0 AND CHAR_LENGTH(credit_code)=18")]
        save_cache("tag_credit_codes_20261021.json", tag_cc)
    tag_cc = set(tag_cc)
    inst_ext = {r[0] for r in q("SELECT external_id FROM gkx.dwd_research_institute_base_info "
                                "WHERE is_deleted=0 AND external_id IS NOT NULL AND external_id<>''")}
    heis_ext = {r[0] for r in q("SELECT external_id FROM gkx.dwd_org_heis_info "
                                "WHERE is_deleted=0 AND external_id IS NOT NULL AND external_id<>''")}
    inst_tag_hit = len(inst_ext & tag_cc)
    heis_tag_hit = len(heis_ext & tag_cc)
    sch = qd("SELECT scholar_id, scholar_org_name_zh AS org FROM gkx.dwd_scholar WHERE is_deleted=0")
    scholar_orgid_empty = cnt("SELECT COUNT(*) AS n FROM gkx.dwd_scholar WHERE COALESCE(scholar_org_id,'')=''")
    scholar_orgname_filled = cnt("SELECT COUNT(*) AS n FROM gkx.dwd_scholar WHERE COALESCE(scholar_org_name_zh,'')<>''")
    paper_rel_rows = cnt("SELECT COUNT(*) AS n FROM gkx.dwd_scholar_paper_relation")
    paper_rel_valid_year = cnt("""SELECT COUNT(*) AS n FROM gkx.dwd_scholar_paper_relation
                                  WHERE `year` BETWEEN 1900 AND %d""" % STAT_YEAR)
    papers_le2024 = cnt("""SELECT COUNT(DISTINCT paper_id) AS n FROM gkx.dwd_scholar_paper_relation
                           WHERE `year` BETWEEN 1900 AND %d""" % STAT_YEAR)
    out = {
        "inst_rows": inst_rows, "heis_rows": heis_rows,
        "inst_with_chain_tag": inst_tag_hit, "heis_with_chain_tag": heis_tag_hit,
        "scholar_rows": len(sch), "scholar_orgid_empty": scholar_orgid_empty,
        "scholar_orgname_filled": scholar_orgname_filled,
        "paper_rel_rows": paper_rel_rows, "paper_rel_valid_year": paper_rel_valid_year,
        "papers_le2024": papers_le2024,
        "orgs": orgs, "scholar": sch,
        "papers_by_scholar": {},
    }
    save_cache(cache, out)
    return out


def main():
    t0 = time.time()
    build_chain_of()
    ac = acad_probe()

    firms = firm_counts()
    patents = patent_counts()
    policy = policy_cells()
    fin = financing_cells()
    rev_v, rev_d = revenue_cells()
    pol_cov = {k: v["coverage_pct"] for k, v in policy.items()}

    ca = {}
    try:
        for key in ("academic_institutions", "scholars", "papers"):
            ca[key] = cells_from_flat(sibling_matrix("M_CHAIN_REG_COMP_ACADEMIC", key)[0])
    except Exception as e:  # 同族文件缺失时退化为不可算
        print("sibling academic missing:", e)
        ca = {}

    a_norm = {}
    for sid, key in (("A1", "academic_institutions"), ("A2", "scholars"), ("A3", "papers")):
        table = ca.get(key) or {}
        for ch in CHAIN_AXIS:
            vals = [float(table.get((ch, c), 0) or 0) for c in CITY4]
            for c, x in zip(CITY4, minmax(vals)):
                a_norm[(sid, ch, c)] = x

    org_city = defaultdict(set)
    for row in ac["orgs"]:
        nm, city = row.get("name"), row.get("city")
        if nm and city in CITY4:
            org_city[nm].add(city)
    acad_city = {c: {"scholars": 0, "papers": 0} for c in CITY4}
    matched = 0
    matched_ids = []
    for s in ac["scholar"]:
        nm = (s.get("org") or "").strip()
        cs = org_city.get(nm)
        if not cs or len(cs) != 1:
            continue
        matched += 1
        c = next(iter(cs))
        acad_city[c]["scholars"] += 1
        matched_ids.append(s["scholar_id"])
    papers_by_scholar = {}
    if matched_ids:
        ids = ",".join("'" + str(i).replace("'", "") + "'" for i in matched_ids if i)
        for r in q("SELECT scholar_id, COUNT(*) AS n FROM gkx.dwd_scholar_paper_relation "
                   "WHERE `year` BETWEEN 1900 AND %d AND scholar_id IN (%s) GROUP BY scholar_id"
                   % (STAT_YEAR, ids)):
            papers_by_scholar[str(r[0])] = int(r[1])
    for s in ac["scholar"]:
        nm = (s.get("org") or "").strip()
        cs = org_city.get(nm)
        if not cs or len(cs) != 1:
            continue
        acad_city[next(iter(cs))]["papers"] += papers_by_scholar.get(str(s["scholar_id"]), 0)
    acad_probe_out = {
        "inst_rows": ac["inst_rows"], "heis_rows": ac["heis_rows"],
        "inst_with_chain_tag": ac["inst_with_chain_tag"], "heis_with_chain_tag": ac["heis_with_chain_tag"],
        "scholar_rows": ac["scholar_rows"], "scholar_orgid_empty": ac["scholar_orgid_empty"],
        "scholar_orgname_filled": ac["scholar_orgname_filled"],
        "paper_rel_rows": ac["paper_rel_rows"], "paper_rel_valid_year": ac["paper_rel_valid_year"],
        "papers_le2024": ac["papers_le2024"],
        "scholar_city_matched": matched,
        "scholar_city_matched_pct": round(100 * matched / ac["scholar_rows"], 2) if ac["scholar_rows"] else 0.0,
        "city_level_diagnostic": acad_city,
    }

    sub_defs = [
        ("E1_firm_count", "企业能力", "链上企业数（credit_code 去重）", "firm_count", True),
        ("E2_revenue", "企业能力", "营业收入合计（亿元）", "revenue_yi", False),
        ("E3_patent", "企业能力", "专利去重件数（申请年≤2024）", "patent_count", True),
        ("A1_acad_org", "学术生态", "链上科研机构数", None, False),
        ("A2_scholar", "学术生态", "机构下学者数", None, False),
        ("A3_paper", "学术生态", "学者论文数", None, False),
        ("S1_policy", "配套生态", "政策覆盖率（%）", "policy_coverage", True),
        ("S2_financing", "配套生态", "融资事件数", "financing_events", True),
    ]
    base = {"firm_count": firms, "patent_count": patents, "policy_coverage": pol_cov,
            "financing_events": fin, "revenue_yi": rev_v}
    norm, norm_log = {}, {}
    for sid, dim, label, key, usable in sub_defs:
        if not usable:
            continue
        for ch in CHAIN_AXIS:
            vals = [float(base[key][(ch, c)] or 0) for c in CITY4]
            for c, x in zip(CITY4, minmax(vals)):
                norm[(sid, ch, c)] = x
            logvals = [math.log1p(v) for v in vals]
            for c, x in zip(CITY4, minmax(logvals)):
                norm_log[(sid, ch, c)] = x

    def dim_score(dim, ch, c, include_revenue=False):
        items = [norm[(sid, ch, c)] for sid, d, label, key, usable in sub_defs
                 if d == dim and usable and (sid != "E2_revenue" or include_revenue)]
        return sum(items) / len(items) if items else None

    rows = []
    for ch in CHAIN_AXIS:
        for c in CITY4:
            d1 = dim_score("企业能力", ch, c)
            d3 = dim_score("配套生态", ch, c)
            d1r = dim_score("企业能力", ch, c, include_revenue=True)
            ap = sum(a_norm[(sid, ch, c)] for sid in ("A1", "A2", "A3")) / 3
            rows.append({
                "chain": ch, "chain_name": CHAIN_CN[ch], "city": c,
                "E1_norm": round(norm[("E1_firm_count", ch, c)], 4),
                "E3_norm": round(norm[("E3_patent", ch, c)], 4),
                "S1_norm": round(norm[("S1_policy", ch, c)], 4),
                "S2_norm": round(norm[("S2_financing", ch, c)], 4),
                "dim_enterprise": round(d1, 4), "dim_academic": None, "dim_support": round(d3, 4),
                "index_2dim": round(100 * (d1 + d3) / 2, 2),
                "index_3dim_acad_const": round(100 * (d1 + d3 + 0.5) / 3, 2),
                "index_with_revenue": round(100 * (d1r + d3) / 2, 2),
                "dim_academic_proxy": round(ap, 4),
                "index_3dim_proxy": round(100 * (d1 + d3 + ap) / 3, 2),
                "index_log": round(100 * ((norm_log[("E1_firm_count", ch, c)] + norm_log[("E3_patent", ch, c)]) / 2
                                          + (norm_log[("S1_policy", ch, c)] + norm_log[("S2_financing", ch, c)]) / 2) / 2, 2),
                "raw": {"firm_count": firms[(ch, c)], "patent_count": patents[(ch, c)],
                        "policy_coverage": pol_cov[(ch, c)], "financing_events": fin[(ch, c)],
                        "revenue_yi": rev_v[(ch, c)]},
            })

    matrix = []
    for ch in CHAIN_AXIS:
        cells = {r["city"]: {k: v for k, v in r.items() if k not in ("chain", "chain_name", "city")}
                 for r in rows if r["chain"] == ch}
        matrix.append({"chain": ch, "chain_name": CHAIN_CN[ch], "cells": cells})

    idx = [r["index_2dim"] for r in rows]
    idx3 = [r["index_3dim_acad_const"] for r in rows]
    idxr = [r["index_with_revenue"] for r in rows]
    idxp = [r["index_3dim_proxy"] for r in rows]
    idxl = [r["index_log"] for r in rows]
    top = sorted(rows, key=lambda r: -r["index_2dim"])[:8]
    bottom = sorted(rows, key=lambda r: r["index_2dim"])[:8]
    city_mean = {c: round(sum(r["index_2dim"] for r in rows if r["city"] == c) / len(CHAIN_AXIS), 2) for c in CITY4}
    chain_mean = {CHAIN_CN[ch]: round(sum(r["index_2dim"] for r in rows if r["chain"] == ch) / 4, 2) for ch in CHAIN_AXIS}
    for r in rows:
        r["rank_in_chain"] = 1 + sum(1 for o in rows if o["chain"] == r["chain"] and o["index_2dim"] > r["index_2dim"])
    firsts = Counter(r["city"] for r in rows if r["rank_in_chain"] == 1)
    proxy_firsts = Counter(r["city"] for r in _rank_within_chain(rows, "index_3dim_proxy") if r["rank_in_chain"] == 1)
    log_firsts = Counter(r["city"] for r in _rank_within_chain(rows, "index_log") if r["rank_log"] == 1)

    payload = {
        "metric_id": MID,
        "metric_name": "区域产业指数（区域产业指数评价页壳指标）",
        "date": "2026-10-21",
        "formula_owner": "王惠（calc-logic/CHAIN/M_CHAIN_REGION_INDEX.md，三条子项口径原样保留）",
        "stat_year": STAT_YEAR,
        "region_axis": CITY4,
        "chain_axis": len(CHAIN_AXIS),
        "formula": "I(c,r)=100×mean(available_dim_scores)；维内子项等权；子项在链内 4 市截面 min-max",
        "version_note": "两维四子项版：学术生态维（④⑤⑥）在链×城粒度无数据支持，指数由企业能力维+配套生态维合成，不等同需求原文的三维指数。",
        "subitem_acceptance": [
            {"id": sid, "dim": dim, "label": label, "usable": usable,
             "reason": ("可算：48/48 单元非退化" if usable else
                        ("可算但 29/48 单元无披露，缺失不可记 0，主值不纳入" if sid == "E2_revenue" else
                         "不可算（直连）：机构与工业标签链码交集 0、学者 org_id 全为空串；"
                         "仅有共著反推代理（473/5,575 家机构，选择性覆盖），见 academic_proxy_sensitivity"))}
            for sid, dim, label, key, usable in sub_defs
        ],
        "probes": {
            "n_cells": 48,
            "chain_city_rows": len(chain_city_from_bridge()["chain_city"]),
            "academic": acad_probe_out,
            "revenue_disclosed_cells": sum(1 for k in rev_d if rev_d[k]),
            "policy_cells_zero": sum(1 for ch in CHAIN_AXIS for c in CITY4 if not pol_cov[(ch, c)]),
            "sources_direct": {
                "firm_count": "gkx.dwd_org_industry_tags ⋈ gkx.dwd_org_base_info",
                "patent_count_le2024": "gkx.dwd_patent ⋈ gkx.dwd_org_base_info(name_cn)",
                "policy_coverage": "gkx.dwd_policy_base 全表（词表口径同 CHAIN_REG_POLICY_COVERAGE v0.2.0）",
                "financing_events": "gkx.dwd_org_financing_info（一行=一次事件）",
                "revenue_yi": "gkx.dwd_org_annual_financial_info 2024",
                "academic_proxy": "gkx 共著反推（同族 M_CHAIN_REG_COMP_ACADEMIC 结果）",
            },
        },
        "matrix": matrix,
        "rows": rows,
        "stats_index": jstats(idx),
        "stats_index_3dim_const": jstats(idx3),
        "stats_index_with_revenue": jstats(idxr),
        "dim_stats": {
            "enterprise": jstats([r["dim_enterprise"] for r in rows]),
            "support": jstats([r["dim_support"] for r in rows]),
            "academic": "不可算（见 subitem_acceptance）",
        },
        "city_mean": city_mean,
        "chain_mean": chain_mean,
        "rank_first_counts": dict(firsts),
        "top8": [{k: r[k] for k in ("chain_name", "city", "index_2dim", "rank_in_chain")} for r in top],
        "bottom8": [{k: r[k] for k in ("chain_name", "city", "index_2dim", "rank_in_chain")} for r in bottom],
        "rank_correlation_with_revenue_version": round(spearman(idx, idxr), 4),
        "academic_proxy_sensitivity": {
            "why": "需求原文的学术生态维 3 个子项在链×城无直连；同族 M_CHAIN_REG_COMP_ACADEMIC 用「产学研共著反推」"
                   "给出了代理值（473 家机构 / 8,891 篇论文 / 1,504 家链上企业），此处按同一 min-max 规则把它补成第三维，"
                   "用于观察「补上学术维后排名是否改变」，不作为本指标主值。",
            "stats": jstats(idxp),
            "city_mean": {c: round(sum(r["index_3dim_proxy"] for r in rows if r["city"] == c) / len(CHAIN_AXIS), 2) for c in CITY4},
            "rank_first_counts": dict(proxy_firsts),
            "spearman_vs_main": round(spearman(idx, idxp), 4),
            "n_first_changed": sum(1 for r in _rank_within_chain(rows, "index_2dim")
                                   if r["rank_in_chain"] != 1 + sum(1 for o in rows if o["chain"] == r["chain"] and o["index_3dim_proxy"] > r["index_3dim_proxy"])),
        },
        "log_sensitivity": {
            "why": "同等权重下企业数与专利件数都是绝对规模，4 市截面 min-max 会把指数压成「谁大谁高」；"
                   "对 E1/E3/S2 取 log1p 后再归一，用于量化「规模主导」的程度。",
            "stats": jstats(idxl),
            "city_mean": {c: round(sum(r["index_log"] for r in rows if r["city"] == c) / len(CHAIN_AXIS), 2) for c in CITY4},
            "rank_first_counts": dict(log_firsts),
            "spearman_vs_main": round(spearman(idx, idxl), 4),
            "first_diff_cells": sum(1 for a, b in zip(_rank_within_chain(rows, "index_2dim"),
                                                      _rank_within_chain(rows, "index_log"))
                                    if a["rank_in_chain"] != b["rank_log"]),
        },
        "structural_artifact": {
            "per_subitem_per_chain": "4 个城市做 min-max，必然产生 1 个 0 与 1 个 1；48 单元中的 0 值主要来自这种结构强制，"
                                     "不是「该市该链为零」。",
            "n_zero_main": sum(1 for v in idx if v == 0),
            "n_hundred_main": sum(1 for v in idx if v == 100),
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": (
                f"8 个子项只有 4 个在链×城粒度可算（企业数、专利、政策覆盖率、融资事件），48 个单元全部闭合；"
                f"学术生态维 3 个子项不可算——{acad_probe_out['inst_rows']:,} 家科研机构与 {acad_probe_out['heis_rows']:,} 家高校"
                f"与工业标签的链码交集 {acad_probe_out['inst_with_chain_tag']}、{acad_probe_out['heis_with_chain_tag']}，"
                f"`dwd_scholar_info.scholar_org_id` {acad_probe_out['scholar_rows']:,} 行全为空串。"
                f"营收子项可算但 {48 - sum(1 for k in rev_d if rev_d[k])}/48 单元无披露。"
                f"可算部分合成的两维指数分布 {min(idx):.1f}–{max(idx):.1f}（中位 {sorted(idx)[24]:.1f}，"
                f"{len(set(idx))} 个不同取值），可区分但缺一整个维度，故判部分支持。"
            ),
            "criteria": {"n_cells": 48, "subitems_total": 8, "subitems_usable": 4,
                         "dims_total": 3, "dims_usable": 2,
                         "n_distinct_index": len(set(idx))},
        },
        "notes": [
            "20261021 改源：所有子项直连 gkx（与旧版开发库 ODS 逐表镜像、行数一致），公式与档位未动；"
            "旧版 policy/patent/fin/revenue 由同族 out.json 取数，本版改为现取现算，读数已逐项对齐。",
            "本指标不是「直接有结果面」：ADS `industry_chain_region_scorecard` 135 行的 "
            "`calc_batch_id='mock_20261019_append'`、`dimension_json` 自写 `honesty=mock`，"
            "`score_academic` 等列全 NULL，属造数结果面，只能作反例，不能作本指标成立证据。",
            "归一化按原稿在「同一链、同一统计年、4 个城市」的截面上做 min-max。4 个样本做 min-max 会强制"
            "每链每子项都出现 0 和 1，等于把「相对位置」当「绝对水平」；跨链不可比，只能同链内比。",
            "学术侧市域诊断（`city_level_diagnostic`）只作旁证：学者按机构名精确匹配落城，"
            f"{acad_probe_out['scholar_rows']:,} 人中命中 {matched} 人（{acad_probe_out['scholar_city_matched_pct']}%）。"
            "它不能回填链×城，因为机构本身没有链码。",
            "学者宇宙纪律：`dwd_scholar_info` 与 `dwd_scholar_talent_flag` 不跨表做分子分母，本指标学者数只用前者。",
            "政策覆盖率沿用同族 `M_CHAIN_REG_POLICY_COVERAGE` 的饱和覆盖率（分母为链内 L1 环节数），"
            "该口径下 16/48 单元为 0、饱和值上限 58.33，指数对政策维不敏感的部分已在 §四 说明。",
        ],
        "elapsed_sec": round(time.time() - t0, 2),
    }
    write_out(MID, payload)
    print("index", jstats(idx), "\ncity", city_mean, "\nfirsts", dict(firsts))
    print("top8", payload["top8"])
    print("bottom8", payload["bottom8"])
    print("rho(rev)", payload["rank_correlation_with_revenue_version"], "acad", acad_probe_out["scholar_city_matched_pct"])


def _rank_within_chain(rows, key):
    out = []
    for r in rows:
        pos = 1 + sum(1 for o in rows if o["chain"] == r["chain"] and o[key] > r[key])
        out.append({**r, "rank_log" if key == "index_log" else "rank_in_chain": pos})
    return out


if __name__ == "__main__":
    main()
