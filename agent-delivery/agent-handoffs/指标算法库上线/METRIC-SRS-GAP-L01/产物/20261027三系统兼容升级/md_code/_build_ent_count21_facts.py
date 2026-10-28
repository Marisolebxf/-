#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""E1 企业底数计数族共享事实快照生成器（五件共用）。

数据源：gkx @ 183.240.141.251:3318（只读）+ code/_snapshots21/ 已核验快照。
产物：code/_snapshots21/ent_count21_facts_20261023.json
     code/_snapshots21/ent_count21_raw_20261023.json（原始拉取证据，可选缓存）

纪律：窄投影 + SSCursor 流式；COUNT(*) 实测；信用码过滤 ^[0-9A-Z]{18}$；
链归属取 industry_code 首个 INB 前 7 位（DATA_FACTS §3.52/§3.55）。
"""
from __future__ import annotations

import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "ent_count21_facts_20261023.json")
RAW = os.path.join(SNAP, "ent_count21_raw_20261023.json")

BASE = os.path.join(SNAP, "base_20261021.json")
TAGS = os.path.join(SNAP, "tech_tags_20261021.json")
TAG_CC = os.path.join(SNAP, "tag_credit_codes_20261021.json")
CHAIN_AGG = os.path.join(SNAP, "chain_org_agg_20261022.json")
CHAIN_LEAF = os.path.join(SNAP, "chain21_leaf_20261022.json")
REGION_AGG = os.path.join(SNAP, "ent_region_agg_20261022.json")

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", connect_timeout=60,
           read_timeout=900, write_timeout=900, autocommit=True)

FOREIGN_KEYS = ("外商投资", "中外合资", "中外合作", "外资", "港澳台", "外国")
FOREIGN_MAINLAND = ("外商投资", "中外合资", "中外合作", "外资", "外国")


def source_block() -> dict:
    return {
        "db": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
        "readonly": True,
        "tables": ["gkx.dwd_org_base_info", "gkx.dwd_forg_base_info",
                   "gkx.dwd_org_tech_tag", "gkx.dwd_org_stock_base",
                   "gkx.dwd_org_industry_tags"],
        "snapshots": ["code/_snapshots21/base_20261021.json",
                      "code/_snapshots21/tech_tags_20261021.json",
                      "code/_snapshots21/tag_credit_codes_20261021.json",
                      "code/_snapshots21/chain_org_agg_20261022.json",
                      "code/_snapshots21/chain21_leaf_20261022.json",
                      "code/_snapshots21/ent_region_agg_20261022.json"],
        "method": "窄投影 + SSCursor 流式；链归属 industry_code 首个 INB 前 7 位；"
                  "信用码过滤 ^[0-9A-Z]{18}$",
        "pulled_at": "2026-10-23T02:40:00+08:00",
    }


def pull_raw() -> dict:
    import pymysql
    con = pymysql.connect(**GKX)
    raw = {"source": source_block(), "notes": []}
    try:
        cur = con.cursor(pymysql.cursors.SSCursor)
        cur.execute("SET NAMES utf8mb4")
        cur.execute("SET SESSION max_execution_time=0")
        t0 = time.time()
        cur.execute("SELECT org_id, org_type, org_size, listing_status "
                    "FROM gkx.dwd_org_base_info")
        rows = []
        while True:
            chunk = cur.fetchmany(10000)
            if not chunk:
                break
            rows.extend([list(r) for r in chunk])
        raw["base_attrs"] = rows
        raw["notes"].append("dwd_org_base_info 四列窄投影流式 %d 行，%.1fs"
                            % (len(rows), time.time() - t0))
        cur.close()

        cur = con.cursor(pymysql.cursors.SSCursor)
        cur.execute("SET NAMES utf8mb4")
        cur.execute("SELECT org_id, external_id, name_en, country_code, "
                    "company_type, incorporation_year FROM gkx.dwd_forg_base_info")
        raw["forg_rows"] = [list(r) for r in cur.fetchall()]
        cur.close()

        cur = con.cursor(pymysql.cursors.SSCursor)
        cur.execute("SET NAMES utf8mb4")
        cur.execute("SELECT org_id, stock_code, stock_type FROM gkx.dwd_org_stock_base")
        raw["stock_rows"] = [list(r) for r in cur.fetchall()]
        cur.close()

        cur = con.cursor()
        for key, sql in [
            ("base_count", "SELECT COUNT(*) FROM gkx.dwd_org_base_info"),
            ("forg_count", "SELECT COUNT(*) FROM gkx.dwd_forg_base_info"),
            ("tech_tag_count", "SELECT COUNT(*) FROM gkx.dwd_org_tech_tag"),
            ("stock_count", "SELECT COUNT(*) FROM gkx.dwd_org_stock_base"),
            ("industry_tag_count", "SELECT COUNT(*) FROM gkx.dwd_org_industry_tags"),
        ]:
            cur.execute(sql)
            raw[key] = int(cur.fetchall()[0][0])
        cur.close()
    finally:
        con.close()
    return raw


def load_raw(refresh: bool = False) -> dict:
    if not refresh and os.path.exists(RAW):
        with open(RAW, encoding="utf-8") as f:
            d = json.load(f)
        if d.get("base_attrs") and d.get("forg_rows"):
            return d
    raw = pull_raw()
    with open(RAW, "w", encoding="utf-8") as f:
        json.dump(raw, f, ensure_ascii=False)
    return raw


def has_tag(tags, needle: str) -> bool:
    return any(needle in t for t in tags)


def is_foreign(org_type: str, include_hmt: bool = True) -> bool:
    if not org_type:
        return False
    keys = FOREIGN_KEYS if include_hmt else FOREIGN_MAINLAND
    return any(k in org_type for k in keys)


def build(refresh: bool = False) -> dict:
    base = json.load(open(BASE, encoding="utf-8"))
    tech = json.load(open(TAGS, encoding="utf-8"))
    tag_cc = set(json.load(open(TAG_CC, encoding="utf-8")))
    chain_agg = json.load(open(CHAIN_AGG, encoding="utf-8"))
    chain_leaf = json.load(open(CHAIN_LEAF, encoding="utf-8"))
    region_agg = json.load(open(REGION_AGG, encoding="utf-8"))
    raw = load_raw(refresh)

    attrs = {r[0]: (r[1], r[2], r[3]) for r in raw["base_attrs"]}
    city = {r[0]: r[4] for r in base}

    city_dist, prov_dist, year_dist = {}, {}, {}
    for r in base:
        city_dist[r[4]] = city_dist.get(r[4], 0) + 1
        prov_dist[r[3]] = prov_dist.get(r[3], 0) + 1
        key = "无年份" if r[5] in (None, "") else str(int(r[5]))
        year_dist[key] = year_dist.get(key, 0) + 1
    sz = city_dist.get("深圳市", 0)

    base_block = {
        "rows": len(base),
        "distinct_org_id": len(set(r[0] for r in base)),
        "distinct_credit_code": len(set(r[1] for r in base)),
        "distinct_city": len(city_dist),
        "city_dist_top": sorted(city_dist.items(), key=lambda kv: -kv[1])[:15],
        "prov_dist_top": sorted(prov_dist.items(), key=lambda kv: -kv[1])[:10],
        "city_null": sum(1 for r in base if not r[4]),
        "shenzhen_city": sz,
        "shenzhen_share": round(sz / len(base), 6),
        "year_min": int(min(r[5] for r in base if r[5])),
        "year_max": int(max(r[5] for r in base if r[5])),
        "no_year": year_dist.get("无年份", 0),
        "source_rows": raw.get("base_count", len(base)),
    }

    type_counter, size_counter = {}, {}
    for ot, osz, ls in attrs.values():
        type_counter[ot or ""] = type_counter.get(ot or "", 0) + 1
        size_counter[osz or ""] = size_counter.get(osz or "", 0) + 1
    org_type_block = {
        "dist_top": sorted(type_counter.items(), key=lambda kv: -kv[1])[:20],
        "foreign_incl_hmt": sum(1 for ot, _, _ in attrs.values() if is_foreign(ot, True)),
        "foreign_excl_hmt": sum(1 for ot, _, _ in attrs.values() if is_foreign(ot, False)),
        "pattern": list(FOREIGN_KEYS),
    }
    org_size_block = {
        "dist": sorted(size_counter.items(), key=lambda kv: -kv[1]),
        "sme_small_micro": size_counter.get("小型", 0) + size_counter.get("微型", 0),
        "unknown": size_counter.get("未知", 0),
        "blank": size_counter.get("", 0) + size_counter.get("-", 0),
    }
    ls_nonempty = sum(1 for _, _, ls in attrs.values() if ls not in (None, ""))
    region_ls = region_agg.get("listing_status", {})
    region_ls_rows = region_ls.get("rows", []) if isinstance(region_ls, dict) else []
    region_ls_nonempty = sum(r[1] for r in region_ls_rows if r[0] not in ("", None))
    stock_types = {}
    for oid, code, st in raw["stock_rows"]:
        stock_types[st] = stock_types.get(st, 0) + 1
    listed_block = {
        "listing_status_nonempty": ls_nonempty,
        "listing_status_source": "code/_snapshots21/ent_region_agg_20261022.json 的 listing_status 分组",
        "listing_status_snapshot_nonempty": region_ls_nonempty,
        "stock_rows": len(raw["stock_rows"]),
        "stock_distinct_org": len(set(r[0] for r in raw["stock_rows"])),
        "stock_type_dist": sorted(stock_types.items(), key=lambda kv: -kv[1]),
        "note": "listing_status 为证券代码字符串，非空即视为上市/挂牌；stock_base 只覆盖 A/B 股",
    }

    tt_ht = sum(1 for v in tech.values() if has_tag(v, "高新技术企业"))
    tt_lg = sum(1 for v in tech.values() if has_tag(v, "专精特新中小企业"))
    tt_lgp = sum(1 for v in tech.values() if has_tag(v, "专精特新小巨人"))
    tag_block = {
        "orgs": len(tech),
        "tag_rows": sum(len(v) for v in tech.values()),
        "source_tag_rows": raw.get("tech_tag_count"),
        "high_tech": tt_ht,
        "little_giant": tt_lg,
        "little_giant_pro": tt_lgp,
        "share_of_base": round(len(tech) / len(base), 6),
    }

    forg = raw["forg_rows"]
    ctry = {}
    for r in forg:
        ctry[r[3] or ""] = ctry.get(r[3] or "", 0) + 1
    base_ids = set(r[0] for r in base)
    forg_block = {
        "rows": len(forg),
        "distinct_org_id": len(set(r[0] for r in forg)),
        "distinct_external_id": len(set(r[1] for r in forg if r[1] not in (None, "", "null"))),
        "countries": sorted(ctry.items(), key=lambda kv: -kv[1]),
        "distinct_country": len(ctry),
        "name_null": sum(1 for r in forg if (r[2] or "").strip().lower() in ("", "null")),
        "external_id_null": sum(1 for r in forg if (r[1] or "").strip().lower() in ("", "null")),
        "company_type_null": sum(1 for r in forg if (r[4] or "").strip().lower() in ("", "null")),
        "year_null": sum(1 for r in forg if r[5] in (None, "")),
        "overlap_base_org_id": sum(1 for r in forg if r[0] in base_ids),
        "overlap_note": "国外 org_id 为数字串命名空间，与底册 32 位 hex org_id 不重叠",
    }
    total_block = {
        "domestic": len(base),
        "foreign": len(forg),
        "union": len(base) + len(forg) - forg_block["overlap_base_org_id"],
        "formula": "COUNT(DISTINCT org_id) 国内 ∪ 国外；两侧命名空间不同，UNION 即可",
    }

    chain_names = chain_agg.get("chain_names", {})
    per_chain = chain_agg.get("per_chain", {})
    chain_rows = []
    for code, rec in per_chain.items():
        chain_rows.append({
            "chain": code, "chain_name": chain_names.get(code, ""),
            "firms": rec.get("firms", 0), "hitech": rec.get("hitech", 0),
            "in_base": rec.get("in_base", 0),
            "shenzhen": (rec.get("city") or {}).get("深圳市", 0),
            "hitech_shenzhen": (rec.get("city_hitech") or {}).get("深圳市", 0),
        })
    chain_rows.sort(key=lambda x: -x["firms"])
    union_firms = chain_agg.get("totals", {}).get("firms", 0)
    chain_block = {
        "chains": len(chain_rows), "per_chain": chain_rows,
        "sum_chain_firms": sum(r["firms"] for r in chain_rows),
        "union_firms": union_firms,
        "union_hitech": chain_agg.get("totals", {}).get("hitech", 0),
        "leaf_terminal_nodes": chain_leaf.get("terminal_nodes", 0),
        "source": "code/_snapshots21/chain_org_agg_20261022.json + chain21_leaf_20261022.json",
    }

    inter = [r for r in base if r[1] in tag_cc]
    inter_ids = [r[0] for r in inter]
    inter_set = set(inter_ids)
    inter_types = {
        "foreign": sum(1 for oid in inter_ids if is_foreign(attrs[oid][0], True)),
        "high_tech": sum(1 for oid in inter_ids if oid in tech and has_tag(tech[oid], "高新技术企业")),
        "sme": sum(1 for oid in inter_ids if attrs[oid][1] in ("小型", "微型")),
        "listed": sum(1 for oid in inter_ids if attrs[oid][2] not in (None, "")),
        "little_giant": sum(1 for oid in inter_ids if oid in tech and has_tag(tech[oid], "专精特新中小企业")),
        "little_giant_pro": sum(1 for oid in inter_ids if oid in tech and has_tag(tech[oid], "专精特新小巨人")),
    }
    base_types = {
        "foreign": org_type_block["foreign_incl_hmt"], "high_tech": tt_ht,
        "sme": org_size_block["sme_small_micro"], "listed": ls_nonempty,
        "little_giant": tt_lg, "little_giant_pro": tt_lgp,
    }
    sz_ids = [r[0] for r in base if r[4] == "深圳市"]
    sz_types = {
        "foreign": sum(1 for oid in sz_ids if is_foreign(attrs[oid][0], True)),
        "high_tech": sum(1 for oid in sz_ids if oid in tech and has_tag(tech[oid], "高新技术企业")),
        "sme": sum(1 for oid in sz_ids if attrs[oid][1] in ("小型", "微型")),
        "listed": sum(1 for oid in sz_ids if attrs[oid][2] not in (None, "")),
        "little_giant": sum(1 for oid in sz_ids if oid in tech and has_tag(tech[oid], "专精特新中小企业")),
        "little_giant_pro": sum(1 for oid in sz_ids if oid in tech and has_tag(tech[oid], "专精特新小巨人")),
    }
    inter_block = {
        "chain_credit_codes": len(tag_cc),
        "base_in_chain": len(inter),
        "share_of_chain_universe": round(len(inter) / union_firms, 6) if union_firms else None,
        "share_of_base": round(len(inter) / len(base), 6),
        "distinct_org": len(inter_set),
        "type_counts": inter_types,
        "type_ratio_of_inter": {k: round(v / len(inter), 6) for k, v in inter_types.items()},
        "sz_in_inter": sum(1 for oid in inter_ids if city[oid] == "深圳市"),
        "rule": "底册 credit_code ∈ 链标签信用码集合（code/_snapshots21/tag_credit_codes_20261021.json），"
                "该集合为 gkx.dwd_org_industry_tags 全表 2,283,761 个信用码，已按 §3.52 去脏",
    }
    type_block = {
        "base_universe": len(base), "counts": base_types,
        "ratio_of_base": {k: round(v / len(base), 6) for k, v in base_types.items()},
        "shenzhen_universe": sz, "shenzhen_counts": sz_types,
        "shenzhen_ratio": {k: round(v / sz, 6) for k, v in sz_types.items()},
        "definitions": {
            "foreign": "dwd_org_base_info.org_type 含 外商投资/中外合资/中外合作/外资/港澳台/外国",
            "high_tech": "dwd_org_tech_tag.org_tag 含 高新技术企业（三变体，按 org_id 去重）",
            "sme": "dwd_org_base_info.org_size ∈ {小型, 微型}",
            "listed": "dwd_org_base_info.listing_status 非空（证券代码）",
            "little_giant": "dwd_org_tech_tag.org_tag 含 专精特新中小企业",
            "little_giant_pro": "dwd_org_tech_tag.org_tag 含 专精特新小巨人",
        },
    }

    facts = {
        "source": source_block(),
        "generated_by": "code/_build_ent_count21_facts.py",
        "base": base_block, "org_type": org_type_block, "org_size": org_size_block,
        "listed": listed_block, "tech_tag": tag_block, "foreign": forg_block,
        "total": total_block, "chain": chain_block,
        "industry_intersection": inter_block, "types": type_block,
        "notes": [
            "表行数一律 COUNT(*) 实测：base=%d forg=%d tech_tag=%d stock=%d industry_tags=%d"
            % (raw.get("base_count", 0), raw.get("forg_count", 0), raw.get("tech_tag_count", 0),
               raw.get("stock_count", 0), raw.get("industry_tag_count", 0)),
            "底册 189,116 行即 189,116 个不同 org_id 与 189,116 个不同信用码，无重复键",
            "链标签信用码集合 2,283,761 个；与底册交集 %d 家，占链企业并集 %.2f%%"
            % (len(inter), 100.0 * len(inter) / union_firms if union_firms else 0),
        ],
    }
    os.makedirs(SNAP, exist_ok=True)
    with open(FACTS, "w", encoding="utf-8") as f:
        json.dump(facts, f, ensure_ascii=False, indent=1)
    return facts


def ensure(refresh: bool = False) -> dict:
    if not refresh and os.path.exists(FACTS):
        try:
            with open(FACTS, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return build(refresh=refresh)


if __name__ == "__main__":
    f = build(refresh="--refresh" in sys.argv)
    print("facts ->", FACTS)
    print("base", f["base"]["rows"], "sz", f["base"]["shenzhen_city"],
          "types", f["types"]["counts"], "inter", f["industry_intersection"]["base_in_chain"])
