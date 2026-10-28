#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_SYNTH_ELEM_CONTRIB —— 要素贡献度与影响路径（4 要素 × 2 靶点 + Top6 路径）。

本件重算而不是只读面板，原因是「科研机构」这一格有两种口径，必须两个都摆出来：
  A. 只认 `dwd_research_institute_base_info`（2,074 家）——calc-logic 字面口径；
  B. 再并上高校名单（`probe_talent21.heis`，2,933 个校名）——专利署名主体口径。
两者差 29 倍（607 件 vs 17,731 件授权），只写一个会把「科研机构贡献」讲错。

同时给：产业侧四类主体规模代理份额、人才残余（实测为 0 → 按 calc-logic 转结构代理）、
资金侧「有研发投入机构营收占比」的可算性实测、Top6 路径与并集披露。

运行：cd code && python3 M_SYNTH_ELEM_CONTRIB.py
输出：code/M_SYNTH_ELEM_CONTRIB_out.json
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_SYNTH_ELEM_CONTRIB_out.json")
CST = timezone(timedelta(hours=8))


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


P = load("synth_elem_panel_20261023.json")
BASE = load("base_20261021.json")
PAT = load("patent2024_scan_20261021.json")["by_name"]
PROBE = load("synth_elem_probe_20261023.json")
TAL = load("probe_talent21_20261022.json")
PAPERS = load("papers_city_year_gkx21.json")["first_city_year"]

CITIES = P["regions"]
YEAR = P["stat_year"]

id2city = {r[0]: r[4] for r in BASE}
name2cities = {}
for r in BASE:
    if r[2]:
        name2cities.setdefault(r[2], []).append(r[4])

inst_names = {}
for city, _ot, nm in PROBE["research_institutes"]:
    if nm:
        inst_names.setdefault(nm, []).append(city)

hei_city = {}
for nm, _prov, city, _src, _lvl in TAL["heis"]["rows"]:
    if nm and city:
        hei_city.setdefault(nm, city)

inst_with_heis = dict(inst_names)
for nm, city in hei_city.items():
    inst_with_heis.setdefault(nm, [city])


def attribute(names_map):
    """专利按第一申请人名落主体桶；一个主体落多城时按 1/n 摊。"""
    ent = {c: 0.0 for c in CITIES}
    inst = {c: 0.0 for c in CITIES}
    for nm, (_pn, _g, gp) in PAT.items():
        cities = names_map.get(nm)
        if not cities:
            continue
        cities = sorted(set(cities))
        w = 1.0 / len(cities)
        for c in cities:
            if c in CITIES:
                inst[c] += gp * w
    return ent, inst


def attribute_split(inst_map):
    ent = {c: 0.0 for c in CITIES}
    inst = {c: 0.0 for c in CITIES}
    for nm, (_pn, _g, gp) in PAT.items():
        if nm in inst_map:
            cities, bucket = inst_map[nm], inst
        else:
            cities, bucket = name2cities.get(nm), ent
        if not cities:
            continue
        cities = sorted(set(cities))
        w = 1.0 / len(cities)
        for c in cities:
            if c in CITIES:
                bucket[c] += gp * w
    return ent, inst


ent_a, inst_a = attribute_split(inst_names)          # A 口径：只有机构表
ent_b, inst_b = attribute_split(inst_with_heis)      # B 口径：机构表 ∪ 高校

pop = P["population"]
ht = pop["hightech"]
inst_cnt = pop["institutes_with_heis"]
sch = pop["scholars_city"]
rd_orgs = pop["rd_2024_orgs"]
rd_yi = pop["rd_2024_yi"]
fin_yi = pop["finance_2024_yi"]
rev_yi = pop["annual_2024_revenue_yi"]

contrib = {}
for c in CITIES:
    tot_a = ent_a[c] + inst_a[c]
    tot_b = ent_b[c] + inst_b[c]
    pool = {"企业": ht[c], "科研机构": inst_cnt[c], "高层次人才": sch[c], "科研资金": rd_orgs[c]}
    pool_total = sum(pool.values())
    shares = {k: round(v / pool_total, 6) for k, v in pool.items()} if pool_total else {}
    # 人才残余：calc-logic 要求先算「第一机构对不上、但作者落区域」的残余；本库无作者级
    # 机构字段（dwd_zh_author.institution 未入快照），实测残余恒为 0 → 转 3 类主体结构代理。
    talent_resid = 0.0
    talent_proxy = round(sch[c] / (ht[c] + inst_cnt[c] + sch[c]), 6) if (ht[c] + inst_cnt[c] + sch[c]) else None
    contrib[c] = {
        "成果侧_A_仅机构表": {
            "patent_ent": round(ent_a[c], 2),
            "patent_inst": round(inst_a[c], 2),
            "attributed": round(tot_a, 2),
            "ent_share": round(ent_a[c] / tot_a, 6) if tot_a else None,
            "inst_share": round(inst_a[c] / tot_a, 6) if tot_a else None,
        },
        "成果侧_B_含高校": {
            "patent_ent": round(ent_b[c], 2),
            "patent_inst": round(inst_b[c], 2),
            "attributed": round(tot_b, 2),
            "ent_share": round(ent_b[c] / tot_b, 6) if tot_b else None,
            "inst_share": round(inst_b[c] / tot_b, 6) if tot_b else None,
            "talent_share": 0.0,
            "fund_share": None,
            "paper_total": PAPERS.get(f"{c}|{YEAR}", 0),
        },
        "产业侧": {
            "pool": pool,
            "pool_total": pool_total,
            "shares": shares,
            "talent_residual": talent_resid,
            "talent_structural_proxy": talent_proxy,
        },
        "资金侧": {
            "rd_orgs": rd_orgs[c],
            "rd_yi": rd_yi[c],
            "finance_yi": fin_yi[c],
            "annual_revenue_yi": rev_yi[c],
            "rd_org_revenue_share": None,
        },
    }

# 资金侧：有研发投入机构的营收 / 区域营收（年报口径）。实测年报营收只覆盖 2.41% 企业，
# 且上市研发主体几乎不在年报表里，两者不同源，按 DATA_FACTS §3.46 不做除法。
for c in CITIES:
    contrib[c]["资金侧"]["rd_org_revenue_share_note"] = (
        "计算所需「有研发投入机构的营收」在年报表取不到：研发主体来自上市财务表"
        "（19,585 行/876 家），营收主体来自年报表（2,193 行），两表 org_id 集合几乎不交，"
        "分子会退化为 0 行。按 §3.46 同源要求，本格留 null，不给 0。")

# Top6 路径（边权 = 成果侧 B 口径份额 + 产业侧份额）
edges = []
for c in CITIES:
    b = contrib[c]["成果侧_B_含高校"]
    ind = contrib[c]["产业侧"]["shares"]
    edges.append((c, "企业", "创新成果", b["ent_share"]))
    edges.append((c, "科研机构", "创新成果", b["inst_share"]))
    edges.append((c, "企业", "产业发展", ind["企业"]))
    edges.append((c, "科研机构", "产业发展", ind["科研机构"]))
    edges.append((c, "高层次人才", "产业发展", ind["高层次人才"]))
    edges.append((c, "科研资金", "产业发展", ind["科研资金"]))
edges.sort(key=lambda x: -x[3])
top6 = [{"region": e[0], "element": e[1], "target": e[2], "weight": round(e[3], 6)} for e in edges[:6]]

sum_checks = {}
for c in CITIES:
    b = contrib[c]["成果侧_B_含高校"]
    sum_checks[c] = {
        "outcome_sum": round(b["ent_share"] + b["inst_share"] + b["talent_share"], 6),
        "industry_sum": round(sum(contrib[c]["产业侧"]["shares"].values()), 6),
    }

# 机构口径的两种结果差多少（正文对比表用）
inst_variant = {
    c: {
        "inst_share_A_pct": round(contrib[c]["成果侧_A_仅机构表"]["inst_share"] * 100, 4),
        "inst_share_B_pct": round(contrib[c]["成果侧_B_含高校"]["inst_share"] * 100, 4),
        "inst_patent_A": contrib[c]["成果侧_A_仅机构表"]["patent_inst"],
        "inst_patent_B": contrib[c]["成果侧_B_含高校"]["patent_inst"],
        "ratio_B_over_A": round(contrib[c]["成果侧_B_含高校"]["patent_inst"]
                                / contrib[c]["成果侧_A_仅机构表"]["patent_inst"], 2)
        if contrib[c]["成果侧_A_仅机构表"]["patent_inst"] else None,
    } for c in CITIES
}

out = {
    "metric_id": "M_SYNTH_ELEM_CONTRIB",
    "metric_name": "要素贡献度与影响路径",
    "support_judgment": "部分支持",
    "verdict_kind": "positive_with_gaps",
    "judgment_reason": (
        "份额分解与 Top6 路径都能算，但两处口径退化：① 创新成果侧只能拆企业与科研机构，"
        "人才残余实测为 0（库内无作者级机构字段），按 calc-logic 转结构代理；"
        "② 产业侧四类主体规模互不互斥（高企同时可能有研发投入），份额是结构代理不是归因，"
        "论文侧无机构类型字段、无法进份额分解。再加「科研机构」两种口径差 29 倍，"
        "读者必须同时看到两组数，故判部分支持。"
    ),
    "base_years_used": [2024],
    "base_years_missing": [],
    "base_years_note": (
        "成果侧=2024 授权专利（去重公开号），产业侧=2024 时点的主体存量（高企/机构/学者/"
        "有研发投入机构四个数都不是年度流量），资金侧=2024 完成日融资与 2024 年报期研发额。"
        "2021—2023 未入集（单年截面设计）；2025/2026 不完整不进分母。"
        "四个数的时间语义不同（存量 vs 流量），故产业侧只作结构代理。"
    ),
    "sources": [
        "gkx @ 183.240.141.251:3318（只读）",
        "code/_snapshots21/synth_elem_panel_20261023.json",
        "code/_snapshots21/patent2024_scan_20261021.json",
        "code/_snapshots21/base_20261021.json",
        "code/_snapshots21/synth_elem_probe_20261023.json",
        "code/_snapshots21/probe_talent21_20261022.json",
        "code/_snapshots21/papers_city_year_gkx21.json",
        "code/_snapshots21/cityfam_hightech_20261021.json",
    ],
    "panel_snapshot": "code/_snapshots21/synth_elem_panel_20261023.json",
    "script": "code/M_SYNTH_ELEM_CONTRIB.py",
    "regions": CITIES,
    "generated_at": datetime.now(CST).isoformat(timespec="seconds"),
    "basis": {
        "elements": ["企业", "科研机构", "高层次人才", "科研资金"],
        "targets": ["创新成果", "产业发展"],
        "outcome_unit": "2024 授权专利（按第一申请人落主体；多城主体 1/n 摊）",
        "industry_unit": "四类主体规模（高企数 / 机构含高校数 / 学者数 / 有研发投入机构数）",
        "is_causal": False,
        "mutually_exclusive": False,
        "note": "份额同行和为 1 是归一化的结果，不是互斥拆分；同一家企业可同时是高企、"
                "有研发投入、且由学者任职，四类主体互相重叠。",
    },
    "contrib": contrib,
    "inst_variant": inst_variant,
    "paths_top6": top6,
    "path_note": "边权=该格份额，只表示关联强度，不表示因果；Top6 里出现 4 条「企业→创新成果」"
                 "是因为四城的企业份额都在 85% 以上，排序被这一格结构主导。",
    "sum_checks": sum_checks,
    "checks": {
        "outcome_shares_sum_to_one": all(abs(v["outcome_sum"] - 1) < 1e-6 for v in sum_checks.values()),
        "industry_shares_sum_to_one": all(abs(v["industry_sum"] - 1) < 1e-6 for v in sum_checks.values()),
        "top6_sorted_desc": all(top6[i]["weight"] >= top6[i+1]["weight"] for i in range(len(top6) - 1)),
        "panel_outcome_matches_B": all(
            abs(P["contrib"][c]["成果侧"]["inst_share"] - contrib[c]["成果侧_B_含高校"]["inst_share"]) < 1e-6
            for c in CITIES),
    },
    "caveats": [
        "人才份额：calc-logic 规定「残余为 0 时改用学者数 ÷（企业+机构+学者）作结构代理，"
        "结果标结构代理」。本件照此执行，故人才格在成果侧为 0、在产业侧为结构代理，两者不可混读。",
        "资金份额：研发额只有上市主体（876 家），与营收主体（2,193 行）不同源，"
        "分子分母无法同源相除，本格留 null；这不是缺数，是不允许拼。",
        "论文：第一作者城市有总量（四城 7,214 篇），但无机构类型字段，进不了份额分解，"
        "只在成果侧单列为区域成果，不参与分母。",
    ],
}

with open(OUT, "w", encoding="utf-8") as fo:
    json.dump(out, fo, ensure_ascii=False, indent=1)

print("[CONTRIB] ->", OUT)
for c in CITIES:
    print(" ", c, "A inst", inst_variant[c]["inst_share_A_pct"], "%",
          "| B inst", inst_variant[c]["inst_share_B_pct"], "%",
          "| industry", contrib[c]["产业侧"]["shares"])
print("  top6", [(t["region"], t["element"], t["target"], t["weight"]) for t in top6])
print("  checks", out["checks"])
