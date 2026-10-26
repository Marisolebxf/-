#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_TYPE_COUNT 企业分类型数量（高企/专精特新/小巨人/外资/小微/上市）。

六类口径（calc-logic + wanghui 正本对齐，详见 MD §1.3）：
  high_tech       dwd_org_tech_tag.org_tag 含「高新技术企业」（三变体，org_id 去重）
  little_giant    org_tag 含「专精特新中小企业」
  little_giant_pro org_tag 含「专精特新小巨人」
  foreign         dwd_org_base_info.org_type 含 外商投资/中外合资/中外合作/外资/港澳台/外国
  sme             dwd_org_base_info.org_size ∈ {小型, 微型}
  listed          dwd_org_base_info.listing_status 非空
零 SQL：读 ent_count21_facts 快照 + tech_tags 快照。
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _build_ent_count21_facts import ensure, load_raw, has_tag, is_foreign  # noqa: E402

OUT = os.path.join(HERE, "M_ENT_TYPE_COUNT_out.json")
TAGS = os.path.join(HERE, "_snapshots21", "tech_tags_20261021.json")
BASE = os.path.join(HERE, "_snapshots21", "base_20261021.json")
ORDER = ["high_tech", "little_giant", "little_giant_pro", "foreign", "sme", "listed"]
CN = {"high_tech": "高新技术企业", "little_giant": "专精特新中小企业",
      "little_giant_pro": "专精特新小巨人", "foreign": "外资企业",
      "sme": "小微企业", "listed": "上市/挂牌企业"}


def main():
    f = ensure()
    types = f["types"]
    base_n = types["base_universe"]
    counts = types["counts"]

    tech = json.load(open(TAGS, encoding="utf-8"))
    base = json.load(open(BASE, encoding="utf-8"))
    raw = load_raw()
    attrs = {r[0]: (r[1], r[2], r[3]) for r in raw["base_attrs"]}

    def flag(oid):
        ot, sz, ls = attrs[oid]
        tg = tech.get(oid, [])
        return {
            "high_tech": has_tag(tg, "高新技术企业"),
            "little_giant": has_tag(tg, "专精特新中小企业"),
            "little_giant_pro": has_tag(tg, "专精特新小巨人"),
            "foreign": is_foreign(ot, True),
            "sme": sz in ("小型", "微型"),
            "listed": ls not in (None, ""),
        }

    flags = {r[0]: flag(r[0]) for r in base}
    pairs = {}
    for i, a in enumerate(ORDER):
        for b in ORDER[i + 1:]:
            pairs[f"{a}∩{b}"] = sum(1 for o, fl in flags.items() if fl[a] and fl[b])
    triple_ht_lg = sum(1 for fl in flags.values()
                       if fl["high_tech"] and fl["little_giant"] and fl["little_giant_pro"])
    none_of = sum(1 for fl in flags.values() if not any(fl.values()))

    variants = {}
    for needle in ("高新技术企业", "专精特新", "小巨人"):
        c = {}
        for v in tech.values():
            for t in v:
                if needle in t:
                    c[t] = c.get(t, 0) + 1
        variants[needle] = sorted(c.items(), key=lambda kv: -kv[1])

    sz_counts = types["shenzhen_counts"]
    tsum = sum(counts[k] for k in ORDER)
    out = {
        "metric_id": "M_ENT_TYPE_COUNT",
        "metric_name": "企业分类型数量",
        "support_judgment": "部分支持",
        "judgment_reason": (
            "六类中四类（高企/专精特新/小巨人/小微）表结构+表数据直接可算；"
            "外资类 org_type 是工商登记类型自由文本，需关键词口径且含港澳台；"
            "上市类底册 listing_status 仅 1,971 家、dwd_org_stock_base 只覆盖 A/B 股 975 家，"
            "缺港股/美股/新三板，六类口径不等权，合计不可当『企业总数』使用。"
        ),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面资质计数，无年度序列；资质本身有授予年（高企 3 年有效），"
                            "但 gkx 标签表无生效/失效日期列，故不拆年份",
        "sources": [
            "code/_snapshots21/ent_count21_facts_20261023.json",
            "code/_snapshots21/tech_tags_20261021.json",
            "code/_snapshots21/base_20261021.json",
            "gkx.dwd_org_tech_tag",
            "gkx.dwd_org_base_info",
            "gkx.dwd_org_stock_base",
        ],
        "universe": base_n,
        "chain_linked_universe": sum(r["in_base"] for r in f["chain"]["per_chain"]),
        "types": [
            {"key": k, "name": CN[k], "count": counts[k],
             "ratio_of_base": types["ratio_of_base"][k],
             "ratio_pct": round(100 * types["ratio_of_base"][k], 2),
             "shenzhen": sz_counts[k],
             "shenzhen_ratio_pct": round(100 * types["shenzhen_ratio"][k], 2),
             "definition": types["definitions"][k]}
            for k in ORDER
        ],
        "type_sum": tsum,
        "base_ratio_sum_pct": round(100 * tsum / base_n, 2),
        "covered_orgs": base_n - none_of,
        "coverage_pct": round(100 * (base_n - none_of) / base_n, 2),
        "shenzhen_vs_nation_pp": {
            k: round(100 * (sz_counts[k] / types["shenzhen_universe"]
                            - counts[k] / base_n), 2) for k in ORDER
        },
        "listed_not_in_stock": counts["listed"] - f["listed"]["stock_distinct_org"],
        "foreign_excl_hmt_pct": round(100 * f["org_type"]["foreign_excl_hmt"] / base_n, 2),
        "foreign_incl_minus_excl": f["org_type"]["foreign_incl_hmt"] - f["org_type"]["foreign_excl_hmt"],
        "type_sum_note": f"六类互有重叠且口径不等权，求和 {tsum} 不是企业数（底册 {base_n}）",
        "overlap": {"pairs": pairs, "high_tech_little_giant_lgp": triple_ht_lg,
                    "none_of_six": none_of},
        "tag_variants": variants,
        "tag_coverage": f["tech_tag"],
        "tag_share_pct": round(100 * f["tech_tag"]["share_of_base"], 2),
        "tagged_orgs": f["tech_tag"]["orgs"],
        "untagged_orgs": base_n - f["tech_tag"]["orgs"],
        "org_size": f["org_size"],
        "foreign_detail": f["org_type"],
        "listed_detail": f["listed"],
        "shenzhen_universe": types["shenzhen_universe"],
        "checks": {
            "sme_eq_small_plus_micro": f["org_size"]["sme_small_micro"]
            == dict(f["org_size"]["dist"])["小型"] + dict(f["org_size"]["dist"])["微型"],
            "listed_eq_region_snapshot": f["listed"]["listing_status_nonempty"]
            == f["listed"]["listing_status_snapshot_nonempty"],
            "high_tech_eq_variant_union": counts["high_tech"] == len(
                [1 for v in tech.values() if has_tag(v, "高新技术企业")]),
        },
        "gaps": [
            "外资口径含港澳台（10,417），剔除港澳台后 3,307，两口径差 7,110 家须在报表注明",
            "上市口径 listing_status 非空 1,971 vs stock_base 975，差额 996 家为挂牌/非 A/B 股，无法拆分市场",
            "org_size 有 46,897 家『未知』+287 家『-』，小微 125,477 是下限而非全量",
            "标签表无资质有效期，高企/专精特新为『历史获得』累计口径，非当前有效存量",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("counts", counts, "sum", out["type_sum"], "none_of_six", none_of)


if __name__ == "__main__":
    main()
