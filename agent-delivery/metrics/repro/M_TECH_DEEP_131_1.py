#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TECH_DEEP_131_1 深圳技术链模型 —— gkx 口径重建（20261022）。

只连 gkx；专利取数走 2021—2024 四城×年×IPC4 pn 面板（gkx.dwd_patent 全表扫描产物）。
产物：code/M_TECH_DEEP_131_1_out.json

切片：深圳 2021—2024 有 IPC 的专利归属次（按主 IPC4 落域）
属性：深圳集中度、区级矩阵（底册 area）、企业数（申请人去重）、科技资质（dwd_org_tech_tag）
应用领域：dwd_org_industry_product_tags（信用代码桥→底册名→深圳）＋ dwd_industry_chain_info 字典
产业规模：无域级营收字段 → 如实缺维
"""
from __future__ import annotations

import collections
import json
import pickle
import time
from pathlib import Path

import pymysql

M = "M_TECH_DEEP_131_1"
CODE = Path(__file__).resolve().parent
SNAP = CODE / "_snapshots21"
SNAPG = CODE / "_snapshots_gkx21"
GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", connect_timeout=60,
           read_timeout=600, write_timeout=600, autocommit=True)
BASE = [2021, 2022, 2023, 2024]


def gkx():
    last = None
    for i in range(5):
        try:
            c = pymysql.connect(**GKX)
            with c.cursor() as cur:
                cur.execute("SET NAMES utf8mb4")
                cur.execute("SET SESSION max_execution_time=120000")
            return c
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(1.5 * (2 ** i))
    raise RuntimeError(f"gkx connect failed: {last!r}")


def q(sql, cap=120000):
    last = None
    for i in range(3):
        try:
            c = gkx()
            try:
                with c.cursor() as cur:
                    cur.execute(f"SET SESSION max_execution_time={cap}")
                    cur.execute(sql)
                    cols = [d[0] for d in cur.description] if cur.description else []
                    return [dict(zip(cols, r)) for r in cur.fetchall()]
            finally:
                c.close()
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2.0 * (2 ** i))
    raise RuntimeError(f"query failed: {last!r} :: {sql[:120]}")


def load_json(p):
    return json.load(open(p, encoding="utf-8"))


const = load_json(SNAP / "tech5_constants_20261022.json")
ipc_year = load_json(SNAP / "patent_ipc4_year_20261021.json")
ipc_name = load_json(SNAP / "patent_ipc4_by_name_20261021.json")
innov = load_json(SNAP / "innov_base_20261021.json")
base = load_json(SNAP / "base_20261021.json")
tags = load_json(SNAP / "tech_tags_20261021.json")

nat = collections.defaultdict(collections.Counter)
for ipc4, y, n, _ in ipc_year:
    nat[ipc4][int(y)] += int(n)

with open(SNAP / "patent_scan_20261021.pkl", "rb") as f:
    raw = pickle.load(f)
sz = collections.defaultdict(collections.Counter)
for (c, y, ipc4), pns in raw["ipc_pn"].items():
    if c == "深圳" and y in BASE:
        sz[ipc4][y] += len(pns)

sz_total = sum(sum(v.values()) for v in sz.values())
sz_by_year = collections.Counter()
for v in sz.values():
    for y, n in v.items():
        sz_by_year[y] += n
sz_all = {d: sum(v.values()) for d, v in sz.items()}
top = sorted(sz_all, key=lambda d: -sz_all[d])[:15]
top_rows = []
for d in top:
    n21, n24 = sz[d][2021], sz[d][2024]
    natv = sum(nat[d].get(y, 0) for y in BASE)
    top_rows.append({
        "ipc4": d, "sz_2021_2024": sz_all[d],
        "share_of_sz_pct": round(sz_all[d] / sz_total * 100, 2),
        "national_2021_2024": natv,
        "sz_concentration_pct": round(sz_all[d] / natv * 100, 2) if natv else None,
        "n2021": n21, "n2024": n24,
        "growth_pct": round((n24 - n21) / n21 * 100, 2) if n21 else None,
    })

hhi_sz = round(sum((sz_all[d] / sz_total) ** 2 for d in sz_all) * 10000, 2)
nat_total = sum(sum(v.values()) for v in nat.values())
hhi_nat = round(sum((sum(nat[d].values()) / nat_total) ** 2 for d in nat) * 10000, 2)
top10_share = round(sum(sz_all[d] for d in sorted(sz_all, key=lambda d: -sz_all[d])[:10]) / sz_total * 100, 2)

# ---------- 区级矩阵（全期截面：IPC4×申请人 × 底册 area） ----------
area_of, area_meta = {}, {"ambiguous": 0}
conf = collections.defaultdict(set)
for r in innov:
    if r.get("city") != "深圳市":
        continue
    a = (r.get("area") or "").strip()
    if a:
        conf[r["name_cn"]].add(a)
for nm, s in conf.items():
    if len(s) == 1:
        area_of[nm] = next(iter(s))
    else:
        area_meta["ambiguous"] += 1

dist_tot = collections.Counter()
dist_dom = collections.Counter()
matched = 0
for ipc4, nm, n in ipc_name:
    a = area_of.get(nm)
    if not a:
        continue
    matched += n
    dist_tot[a] += n
    if ipc4 in top[:8]:
        dist_dom[(ipc4, a)] += n
districts = [a for a, _ in dist_tot.most_common()]
district_rows = []
for d in top[:8]:
    row = {"ipc4": d, "all_years_total": sum(nat[d].values())}
    for a in districts:
        row[a] = dist_dom.get((d, a), 0)
    district_rows.append(row)

# 深圳全期有 IPC 专利（对照区级覆盖）
groups = load_json(SNAPG / "sz_patent_city_name_gkx.json")["groups"]
sz_names_all, sz_n, sz_ipc_empty = {}, 0, 0
for r in groups:
    if r.get("city") != "深圳市":
        continue
    sz_names_all[r["nm"]] = int(r.get("n", 0))
    sz_n += int(r.get("n", 0))
    sz_ipc_empty += int(r.get("ipc_empty", 0))
sz_ipc_all = sz_n - sz_ipc_empty

# ---------- 企业数与科技资质 ----------
name_org, org_name = {}, {}
for r in innov:
    if r.get("city") == "深圳市":
        name_org[r["name_cn"]] = r["org_id"]
        org_name[r["org_id"]] = r["name_cn"]
ent_per_dom = collections.Counter()
ent_matched = 0
for ipc4, nm, n in ipc_name:
    if nm in sz_names_all:
        ent_per_dom[ipc4] += 1
        ent_matched += 1
tagged = 0
tag_kinds = collections.Counter()
sel_dom_names = collections.defaultdict(set)
for ipc4, nm, n in ipc_name:
    if nm in sz_names_all:
        sel_dom_names[ipc4].add(nm)
ent_total = len({nm for nm in sz_names_all})
for nm in sz_names_all:
    oid = name_org.get(nm)
    if oid and tags.get(oid):
        tagged += 1
        for t in tags[oid]:
            tag_kinds[t] += 1

# ---------- 应用领域：信用代码桥 → 底册名 → 深圳 ----------
prod_rows = q("""SELECT company_name, industry_link_name FROM gkx.dwd_org_industry_product_tags""")
ind_dict = q("SELECT industry_code, industry_name FROM gkx.dwd_industry_chain_info")
code2name = {r["industry_code"]: r["industry_name"] for r in ind_dict}
cc2name = {r[1]: r[2] for r in base if r[1] and r[1] != "NULL"}
name2city = {r[2]: r[4] for r in base}
prod_hit = prod_sz = 0
prod_ind = collections.Counter()
for r in prod_rows:
    cc = r.get("company_name") or ""
    nm = cc2name.get(cc)
    if not nm:
        continue
    prod_hit += 1
    if name2city.get(nm) not in ("深圳市", "深圳"):
        continue
    prod_sz += 1
    try:
        codes = json.loads(r.get("industry_link_name") or "[]")
    except Exception:  # noqa: BLE001
        codes = []
    for c in set(codes):
        prod_ind[code2name.get(c, c)] += 1

# ---------- 产业规模：可用的只有上市主体财务，且无技术域字段 ----------
fin_cols = q("""SELECT COLUMN_NAME FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA='gkx' AND TABLE_NAME='dwd_org_stock_finance_info'
                ORDER BY ORDINAL_POSITION""")
fin_col_names = [r["COLUMN_NAME"] for r in fin_cols]

out = {
    "metric_id": M,
    "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    "domain_mapping_version": const["domain_mapping_version"],
    "patent_dedup_key": const["patent_dedup_key"],
    "base_years_used": const["base_years_used"],
    "base_years_missing": const["base_years_missing"],
    "base_years_note": const["base_years_note"],
    "constants_ref": "code/_snapshots21/tech5_constants_20261022.json",
    "slice": {
        "city": "深圳",
        "sz_ipc_total_2021_2024": sz_total,
        "sz_ipc_by_year": {str(k): v for k, v in sorted(sz_by_year.items())},
        "sz_domain_count": len(sz_all),
        "national_ipc_total_2021_2024": nat_total,
        "sz_share_of_national_pct": round(sz_total / nat_total * 100, 2),
        "top_domains": top_rows,
        "hhi_sz": hhi_sz,
        "hhi_national": hhi_nat,
        "top10_share_sz_pct": top10_share,
    },
    "district": {
        "matched_assignments_all_years": matched,
        "sz_ipc_patents_all_years": sz_ipc_all,
        "sz_patents_all_years": sz_n,
        "coverage_of_ipc_pct": round(matched / sz_ipc_all * 100, 3) if sz_ipc_all else None,
        "coverage_of_all_pct": round(matched / sz_n * 100, 2) if sz_n else None,
        "ambiguous_names": area_meta["ambiguous"],
        "districts": districts,
        "district_totals": {a: dist_tot[a] for a in districts},
        "matrix_top8": district_rows,
        "window_note": "区级矩阵为全期截面（名称×IPC4 缓存不按年），与 2021—2024 主窗口不完全一致",
    },
    "enterprise": {
        "sz_applicant_names": ent_total,
        "domain_applicant_matches": ent_matched,
        "tagged_names": tagged,
        "tag_coverage_pct": round(tagged / ent_total * 100, 2) if ent_total else None,
        "tag_kinds": dict(tag_kinds.most_common(12)),
        "top_domains_by_applicants": [
            {"ipc4": d, "applicants": ent_per_dom[d]} for d in
            sorted(ent_per_dom, key=lambda x: -ent_per_dom[x])[:10]],
    },
    "application_field": {
        "product_rows": len(prod_rows),
        "credit_code_matched_rows": prod_hit,
        "credit_code_match_pct": round(prod_hit / len(prod_rows) * 100, 2),
        "sz_rows": prod_sz,
        "top_industries_sz": dict(prod_ind.most_common(12)),
        "industry_dict_rows": len(ind_dict),
    },
    "industry_scale": {
        "domain_revenue_field": "无",
        "listed_finance_table": "dwd_org_stock_finance_info",
        "listed_finance_columns": fin_col_names[:12],
        "note": "上市公司财务仅有主体级数据，无技术域字段；且仅覆盖上市主体，不足以做域级产业规模",
    },
    "criteria": {
        "direct_structure": "部分（无 sz 结果面，按专利面板重建切片）",
        "direct_data": "部分（专利/企业/区级齐；产业规模无域级字段）",
        "dependency_structure": "部分（应用领域经信用代码桥，覆盖 12.99%）",
        "dependency_data": "部分（区级矩阵全期截面、应用领域覆盖低）",
    },
    "missing_sources": [
        "产业规模：无域级营收/产值字段，上市财务仅主体级且无域标签",
        "应用领域：产品表列错位（company_name 存信用代码），经信用代码桥仅匹配 12.99%",
        "区级年度序列：名称×IPC4 缓存不按年，无法做 2021—2024 逐年区级矩阵",
        "论文/标准：无论文域码、标准表零命中，无法做深圳论文/标准切片",
    ],
    "support_judgment": "部分支持",
    "judgment_reason": "深圳切片（890,009 件归属次、609 域）、区级矩阵（覆盖有 IPC 专利 99.996%）、"
                       "企业数与科技资质可复算；但产业规模无域级字段、应用领域经信用代码桥仅覆盖 12.99%、"
                       "区级年度序列与论文/标准切片缺源——属地多维属性始终缺维。",
    "verdict_kind": "reconstructed",
    "sources": const["source"],
}

json.dump(out, open(CODE / f"{M}_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({"sz_total": sz_total, "domains": len(sz_all), "hhi_sz": hhi_sz,
                  "district_cov": out["district"]["coverage_of_ipc_pct"],
                  "ent": ent_total, "tagged": tagged, "prod_sz": prod_sz,
                  "support": out["support_judgment"]}, ensure_ascii=False))
