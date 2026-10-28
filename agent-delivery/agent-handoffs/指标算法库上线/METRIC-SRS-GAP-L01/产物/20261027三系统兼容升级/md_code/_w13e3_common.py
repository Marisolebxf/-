#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W13-E3 族内共享口径（只读落盘快照，不连任何数据库）。

五件共用：
  M_ENT_DOMAIN_COVERAGE_COUNT / M_ENT_DOMAIN_DIST_TOPIC /
  M_ENT_REGIONAL_COUNT_TOPIC / M_ENT_SUPPLY_STRUCT_TOPIC / M_ENT_TYPE_DIST_TOPIC

数据只来自 code/_snapshots21/ 下的共享快照：
  base_20261021.json                 企业底册 189,116 行
  chain_firm_index_20261023.json     去脏链属企业 1,714,457 家、12 链 × 城市/省
  chain_tree_20261021.json           链树 1,273 节点 / 12 根
  tech_tags_20261021.json            技术标签 32,322 家
  star_roster_gkx_20261021.json      明星名单 4,561 家（授权 ≥50）
  w13e3_probe_20261023.json          本族探针（表名/列名/链码/上市/招投标/live）
  w13e3_region_scope_20261023.json   region_scope_member 15 行（仅作区域键定义）

本模块只做纯函数与常量，不写文件；每个件的脚本自己写 <ID>_out.json。
"""
from __future__ import annotations

import json
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")

DB_GKX = "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）"
AS_OF = "2026-10-23"

CHAIN_ORDER = [
    "INB1306", "INB1502", "INB1333", "INB2503", "INB1309", "INB2505",
    "INB1323", "INB1303", "INB1204", "INB1354", "INB1209", "INB1236",
]

# 区域键定义：来自 live dim.region_scope_member 15 行（已落盘为
# _snapshots21/w13e3_region_scope_20261023.json）。这里只作定义常量，
# 企业家数一律来自 gkx 底册，不由维表贡献。
GBA_CITIES = ["广州市", "深圳市", "珠海市", "佛山市", "江门市", "惠州市", "东莞市", "中山市"]
YRD_PROVINCES = ["上海市", "江苏省", "浙江省", "安徽省"]
JJJ_PROVINCES = ["北京市", "天津市", "河北省"]
FOCUS_CITIES = ["深圳市", "广州市", "东莞市", "惠州市"]

YEAR_MIN = 2015
YEAR_MAX = 2026


def load(name: str):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def pct(a, b, nd: int = 4) -> float | None:
    if not b:
        return None
    return round(a * 100.0 / b, nd)


def base_rows():
    """底册行：[org_id, credit_code, name, province, city, year]（year 为字符串或 None）。"""
    return load("base_20261021.json")


def base_panel(rows=None):
    """年 × 区域面板（以成立年作「年度队列」代理，见各件 §二 声明）。

    返回：
      year_total        年 -> 当年成立且仍在底册的企业数
      year_city         年 -> 4 个重点市的家数
      year_scope        年 -> gba / yrd / jjj 家数
      year_share        年 -> 4 市占当年队列的百分比
      stock_total       年 -> 截至年末的存量（成立年 <= 年）
      stock_city        年 -> 4 市截至年末存量
      city_total        全期市家数
      prov_total        全期省家数
      scope_total       全期 gba / yrd / jjj
    """
    if rows is None:
        rows = base_rows()
    years = [int(r[5]) for r in rows if r[5] not in (None, "", "0")]
    city_total = Counter((r[4] or "（空）") for r in rows)
    prov_total = Counter((r[3] or "（空）") for r in rows)

    year_total, year_city, year_scope, year_share = {}, {}, {}, {}
    for y in range(YEAR_MIN, YEAR_MAX + 1):
        sub = [r for r in rows if r[5] not in (None, "", "0") and int(r[5]) == y]
        n = len(sub)
        year_total[str(y)] = n
        cc = Counter((r[4] or "（空）") for r in sub)
        year_city[str(y)] = {c: cc.get(c, 0) for c in FOCUS_CITIES}
        year_share[str(y)] = {c: pct(cc.get(c, 0), n, 2) for c in FOCUS_CITIES}
        year_scope[str(y)] = {
            "gba": sum(cc.get(c, 0) for c in GBA_CITIES),
            "yrd": sum(len([1 for r in sub if (r[3] or "") == p]) for p in YRD_PROVINCES),
            "jjj": sum(len([1 for r in sub if (r[3] or "") == p]) for p in JJJ_PROVINCES),
        }

    stock_total, stock_city = {}, {}
    for y in range(YEAR_MIN, YEAR_MAX + 1):
        n = sum(1 for v in years if v <= y)
        stock_total[str(y)] = n
        stock_city[str(y)] = {
            c: sum(1 for r in rows if r[5] not in (None, "", "0")
                   and int(r[5]) <= y and (r[4] or "") == c)
            for c in FOCUS_CITIES
        }

    scope_total = {
        "gba": sum(city_total.get(c, 0) for c in GBA_CITIES),
        "yrd": sum(prov_total.get(p, 0) for p in YRD_PROVINCES),
        "jjj": sum(prov_total.get(p, 0) for p in JJJ_PROVINCES),
    }

    return {
        "n_rows": len(rows),
        "n_year_present": len(years),
        "n_year_missing": len(rows) - len(years),
        "year_min": min(years) if years else None,
        "year_max": max(years) if years else None,
        "n_province": len([k for k in prov_total if k not in ("", "（空）")]),
        "n_city": len([k for k in city_total if k not in ("", "（空）")]),
        "city_total": dict(city_total.most_common()),
        "prov_total": dict(prov_total.most_common()),
        "scope_total": scope_total,
        "year_total": year_total,
        "year_city": year_city,
        "year_scope": year_scope,
        "year_share_pct": year_share,
        "stock_total": stock_total,
        "stock_city": stock_city,
    }


def chain_panel():
    """链属企业面板（链归属取 industry_code 链根；已按 18 位信用码去脏）。"""
    c = load("chain_firm_index_20261023.json")
    firms = c["chain_firms"]
    total = sum(firms.values())
    shares = {k: pct(v, total, 4) for k, v in firms.items()}
    hhi = round(sum((v / total) ** 2 for v in firms.values()), 6)

    city_total = Counter()
    for ch, cc in c["chain_city"].items():
        for city, n in cc.items():
            city_total[city] += n
    prov_total = Counter()
    for ch, pp in c["chain_prov"].items():
        for prov, n in pp.items():
            prov_total[prov] += n

    city_cov = {}
    for city in city_total:
        if city == "未匹配":
            continue
        city_cov[city] = sum(1 for ch in c["chain_city"] if c["chain_city"][ch].get(city, 0) > 0)
    cov_dist = Counter(city_cov.values())

    name_chain = c["name_chain"]
    base = base_rows()
    base_names = {r[2] for r in base if r[2]}
    base_matched = [r for r in base if r[2] in name_chain]
    base_matched_names = base_names & set(name_chain)
    base_chain = Counter(name_chain[n] for n in base_matched_names)
    roster = load("star_roster_gkx_20261021.json")["rows"]
    roster_matched = [r for r in roster if r["name_cn"] in name_chain]
    roster_chain = Counter(name_chain[r["name_cn"]] for r in roster_matched)

    l1 = c["l1_firms"]
    l1_top = sorted(l1.items(), key=lambda kv: -kv[1])[:12]

    return {
        "total": total,
        "firms": firms,
        "shares_pct": shares,
        "hhi": hhi,
        "top1_pct": shares[CHAIN_ORDER[0]],
        "top3_pct": pct(sum(firms[k] for k in CHAIN_ORDER[:3]), total, 4),
        "n_chains": len(firms),
        "n_cities": len([k for k in city_total if k != "未匹配"]),
        "city_total": dict(city_total.most_common()),
        "city_unmatched": city_total.get("未匹配", 0),
        "city_coverage": city_cov,
        "city_coverage_dist": {str(k): v for k, v in sorted(cov_dist.items())},
        "n_cities_full": cov_dist.get(12, 0),
        "prov_total": dict(prov_total.most_common()),
        "base_matched_rows": len(base_matched),
        "base_matched_names": len(base_matched_names),
        "base_matched_share_pct": pct(len(base_matched_names), len(base_names), 4),
        "base_chain": dict(base_chain.most_common()),
        "roster_matched_rows": len(roster_matched),
        "roster_matched_share_pct": pct(len(roster_matched), len(roster), 4),
        "roster_chain": dict(roster_chain.most_common()),
        "l1_top": [{"code": k, "n": v} for k, v in l1_top],
        "stats": c.get("stats", {}),
        "source": c.get("source", {}),
        "rule": c.get("rule", {}),
    }


def type_panel():
    """重点名单 × 四类（高企 / 小微 / 上市 / 外资）面板。"""
    roster = load("star_roster_gkx_20261021.json")["rows"]
    tags = load("tech_tags_20261021.json")
    probe = load("w13e3_probe_20261023.json")
    listed_ids = set(probe["D_listed"]["org_ids"])
    orgsize = load("w13e3_roster_orgsize_20261023.json")

    def has(org_id, kw):
        return any(kw in t for t in tags.get(org_id, []))

    hi = {r["org_id"] for r in roster if has(r["org_id"], "高新技术企业")}
    sme = {r["org_id"] for r in roster if has(r["org_id"], "科技型中小企业")}
    zx = {r["org_id"] for r in roster if has(r["org_id"], "专精特新")}
    lg = {r["org_id"] for r in roster if has(r["org_id"], "小巨人")}
    innov = {r["org_id"] for r in roster if has(r["org_id"], "创新型中小企业")}
    listed = {r["org_id"] for r in roster if r["org_id"] in listed_ids}
    micro = {r["org_id"] for r in roster if orgsize.get(r["org_id"]) in ("小型", "微型")}
    unknown_size = {r["org_id"] for r in roster if orgsize.get(r["org_id"]) in (None, "未知", "-")}
    foreign = {r["org_id"] for r in roster
               if any(k in (r.get("org_type") or "")
                      for k in ("外商投资", "中外合资", "中外合作", "外国"))}

    union3 = hi | sme | listed
    all3 = hi & sme & listed
    none = {r["org_id"] for r in roster} - union3

    key_total_path = os.path.join(HERE, "M_ENT_KEY_TOTAL_out.json")
    key_total = None
    if os.path.exists(key_total_path):
        with open(key_total_path, encoding="utf-8") as f:
            key_total = json.load(f).get("result", {}).get("key_assignees_ge50")

    return {
        "roster_n": len(roster),
        "roster_grant_min": min(r["grant_cnt"] for r in roster),
        "roster_grant_sum": sum(r["grant_cnt"] for r in roster),
        "tag_orgs": len(tags),
        "high_tech_n": len(hi),
        "sme_n": len(sme),
        "listed_n": len(listed),
        "foreign_tag_n": 0,
        "foreign_orgtype_n": len(foreign),
        "zx_n": len(zx),
        "little_giant_n": len(lg),
        "innovative_n": len(innov),
        "hi_sme": len(hi & sme),
        "hi_listed": len(hi & listed),
        "sme_listed": len(sme & listed),
        "all3": len(all3),
        "union3": len(union3),
        "none3": len(none),
        "micro_n": len(micro),
        "unknown_size_n": len(unknown_size),
        "hi_micro": len(hi & micro),
        "micro_listed": len(micro & listed),
        "all3_micro": len(hi & micro & listed),
        "sum_four_pct": pct(len(hi) + len(sme) + len(listed) + len(foreign), len(roster), 2),
        "key_total_ge50": key_total,
        "stock_base_rows": probe["D_listed"]["stock_base_rows"],
        "stock_base_orgs": probe["D_listed"]["stock_base_distinct_org"],
        "listed_status_dist": probe["D_listed"]["listed_status_dist"],
        "stock_type_dist": probe["D_listed"]["stock_type_dist"],
    }
