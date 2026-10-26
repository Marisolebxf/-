#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_TOTAL_COUNT 企业总数（国内 ∪ 国外主档）——gkx 换源复算。

口径（calc-logic 正本）：
    COUNT(DISTINCT org_id) FROM (enterprise_base UNION enterprise_forg_base)
    国内 = gkx.dwd_org_base_info（一企一码）；国外 = gkx.dwd_forg_base_info。
本脚本零 SQL：读 code/_snapshots21/ent_count21_facts_20261023.json。
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _build_ent_count21_facts import ensure  # noqa: E402

OUT = os.path.join(HERE, "M_ENT_TOTAL_COUNT_out.json")


def pct(a, b):
    return round(100.0 * a / b, 2) if b else None


def main():
    f = ensure()
    base = f["base"]
    forg = f["foreign"]
    total = f["total"]
    chain = f["chain"]
    inter = f["industry_intersection"]

    domestic = total["domestic"]
    foreign = total["foreign"]
    union = total["union"]
    named = foreign - forg["name_null"]
    ctry = dict(forg["countries"])
    gb, us, ca = ctry.get("GB", 0), ctry.get("US", 0), ctry.get("CA", 0)
    gd = dict(base["prov_dist_top"]).get("广东省", 0)
    out = {
        "metric_id": "M_ENT_TOTAL_COUNT",
        "metric_name": "企业总数",
        "support_judgment": "部分支持",
        "judgment_reason": (
            "国内主档完整可算（189,116 家、189,116 个 org_id/信用码），"
            "但国外主档 gkx.dwd_forg_base_info 只有 20,000 行、3 个国家"
            "（GB 19,832 / US 159 / CA 9），其中 7,365 行 name_en 为字面 'null'，"
            "属样本性主档而非全球企业名录；『全球企业总数』的国外维无法闭合。"
        ),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面计数，无年度序列；基期不适用（库内成立年跨 1900—2026，"
                            "但本指标不按年摊分母，故 used/missing 均为空）",
        "sources": [
            "code/_snapshots21/ent_count21_facts_20261023.json",
            "code/_snapshots21/base_20261021.json",
            "code/_snapshots21/chain_org_agg_20261022.json",
            "gkx.dwd_org_base_info @ 183.240.141.251:3318",
            "gkx.dwd_forg_base_info @ 183.240.141.251:3318",
        ],
        "population": {
            "domestic": domestic,
            "foreign": foreign,
            "union": union,
            "overlap_base_org_id": forg["overlap_base_org_id"],
            "domestic_share_pct": pct(domestic, union),
            "shenzhen_share_of_union_pct": pct(base["shenzhen_city"], union),
            "foreign_share_pct": pct(foreign, union),
            "foreign_named": named,
            "foreign_name_null": forg["name_null"],
            "foreign_name_null_pct": pct(forg["name_null"], foreign),
            "foreign_external_id_null": forg["external_id_null"],
            "foreign_external_id_distinct": forg["distinct_external_id"],
            "foreign_external_id_nonnull_pct": pct(forg["distinct_external_id"], foreign),
            "foreign_company_type_null": forg["company_type_null"],
            "foreign_year_null": forg["year_null"],
            "foreign_countries": forg["distinct_country"],
            "foreign_country_dist": forg["countries"],
            "foreign_gb": gb,
            "foreign_us": us,
            "foreign_ca": ca,
            "foreign_gb_pct": pct(gb, foreign),
        },
        "domestic_structure": {
            "distinct_org_id": base["distinct_org_id"],
            "distinct_credit_code": base["distinct_credit_code"],
            "distinct_city": base["distinct_city"],
            "city_null": base["city_null"],
            "prov_dist_top": base["prov_dist_top"],
            "city_dist_top": base["city_dist_top"],
            "shenzhen_city": base["shenzhen_city"],
            "shenzhen_share_pct": pct(base["shenzhen_city"], domestic),
            "guangdong": gd,
            "prd_four_city_sum": base["shenzhen_city"] + sum(
                dict(base["city_dist_top"]).get(c, 0) for c in ("广州市", "东莞市", "惠州市")),
            "prd_four_city_share_of_gd_pct": pct(
                base["shenzhen_city"] + sum(dict(base["city_dist_top"]).get(c, 0)
                                            for c in ("广州市", "东莞市", "惠州市")), gd),
            "other_prov_sum": domestic - gd,
            "guangdong_share_pct": pct(gd, domestic),
            "year_min": base["year_min"],
            "year_max": base["year_max"],
            "no_year": base["no_year"],
        },
        "industry_slice": {
            "chain_count": chain["chains"],
            "chain_union_firms": chain["union_firms"],
            "chain_sum_firms": chain["sum_chain_firms"],
            "industry_table_credit_codes": inter["chain_credit_codes"],
            "industry_table_membership_in_base": inter["base_in_chain"],
            "chain_linked_in_base": sum(r["in_base"] for r in chain["per_chain"]),
            "chain_linked_in_base_pct": pct(sum(r["in_base"] for r in chain["per_chain"]),
                                            chain["union_firms"]),
            "unlinked_in_table": inter["base_in_chain"] - sum(r["in_base"] for r in chain["per_chain"]),
            "membership_share_of_base_pct": inter["share_of_base"] * 100,
            "top3_chain_sum": sum(r["firms"] for r in chain["per_chain"][:3]),
            "top3_chain_pct": pct(sum(r["firms"] for r in chain["per_chain"][:3]),
                                  chain["union_firms"]),
            "per_chain": [
                dict(r, share_of_chain_universe_pct=pct(r["firms"], chain["union_firms"]))
                for r in chain["per_chain"]
            ],
            "rule": "链归属取 industry_code 首个 INB 前 7 位；未选产业时返回全量企业总数",
        },
        "checks": {
            "domestic_rows_eq_distinct_org": base["rows"] == base["distinct_org_id"],
            "domestic_rows_eq_distinct_credit": base["rows"] == base["distinct_credit_code"],
            "union_formula": f"{domestic} + {foreign} - {forg['overlap_base_org_id']} = {union}",
            "overlap_zero": forg["overlap_base_org_id"] == 0,
        },
        "gaps": [
            "国外主档仅 GB/US/CA 三国 20,000 行，且 7,365 行名称为字面 null，不能称全球名录",
            "国外无产业链上链表（无 enterprise_forg_industry_chain），选产业时国外侧不能并入",
            "港澳台企业不计入国外侧（calc-logic 明示），但底册 org_type 中的港澳台投资企业仍计入国内",
            "gkx 无 dwd_org_industry_chain_dtl，产业过滤只能用 dwd_org_industry_tags 的 industry_code",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("total", union, "domestic", domestic, "foreign", foreign,
          "named", named, "overlap", forg["overlap_base_org_id"])


if __name__ == "__main__":
    main()
