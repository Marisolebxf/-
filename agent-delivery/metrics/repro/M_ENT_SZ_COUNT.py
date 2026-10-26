#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_SZ_COUNT 深圳企业数量。

口径：底册 dwd_org_base_info.city='深圳市' 的去重 org_id 数；
选产业时用链属快照（chain_linked_type_20261023）内的 city='深圳市' 子集。
深圳=全市（含深汕合作区），不按区县拆分（底册无区县列）。
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _build_ent_count21_facts import ensure  # noqa: E402

OUT = os.path.join(HERE, "M_ENT_SZ_COUNT_out.json")
LINKED = os.path.join(HERE, "_snapshots21", "chain_linked_type_20261023.json")
ORDER = ["high_tech", "little_giant", "little_giant_pro", "foreign", "sme", "listed"]
CN = {"high_tech": "高新技术企业", "little_giant": "专精特新中小企业",
      "little_giant_pro": "专精特新小巨人", "foreign": "外资企业",
      "sme": "小微企业", "listed": "上市/挂牌企业"}


def pct(a, b):
    return round(100.0 * a / b, 2)


def main():
    f = ensure()
    lk = json.load(open(LINKED, encoding="utf-8"))
    base = f["base"]
    n = f["types"]["base_universe"]
    sz = base["shenzhen_city"]

    cities = [{"city": c, "count": v, "pct": pct(v, n)} for c, v in base["city_dist_top"]]
    gd = dict(base["prov_dist_top"]).get("广东省", 0)
    others_gd = [c for c in cities if c["city"] in ("广州市", "东莞市", "惠州市")]
    rest_gd = gd - sz - sum(c["count"] for c in others_gd)

    out = {
        "metric_id": "M_ENT_SZ_COUNT",
        "metric_name": "深圳企业数量",
        "support_judgment": "部分支持",
        "judgment_reason": (
            "底册有 city='深圳市' 中文市名，95,600 家可直接 GROUP BY 得到，且与广东省 188,776 家、"
            "全国 189,116 家勾稽；但 calc-logic 钉死的 region_id LIKE '4403%' 行政区划码在 gkx "
            "dwd_org_base_info 中不存在（列字典 44 列无 region_id/adcode），只能用中文市名代理，"
            "故判部分支持而非完全转换支持。"
        ),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面计数；不按成立年拆分（底册成立年跨 1900—2026，无『当年新增』语义）",
        "sources": [
            "code/_snapshots21/ent_count21_facts_20261023.json",
            "code/_snapshots21/base_20261021.json",
            "code/_snapshots21/chain_linked_type_20261023.json",
            "gkx.dwd_org_base_info",
        ],
        "nationwide": n,
        "guangdong": gd,
        "shenzhen": sz,
        "share_of_nation_pct": pct(sz, n),
        "share_of_guangdong_pct": pct(sz, gd),
        "city_top": cities,
        "other_prd": [{"city": c["city"], "count": c["count"], "pct_of_nation": c["pct"]}
                      for c in others_gd],
        "other_guangdong": rest_gd,
        "prd_four_city_sum": sz + sum(c["count"] for c in others_gd),
        "prd_four_city_share_of_gd_pct": pct(sz + sum(c["count"] for c in others_gd), gd),
        "other_city_sum": n - (sz + sum(c["count"] for c in others_gd) + rest_gd),
        "chain_vs_nation_pp": round(pct(lk["shenzhen"], lk["universe"]) - pct(sz, n), 2),
        "wide_minus_strict_sz": f["industry_intersection"]["sz_in_inter"] - lk["shenzhen"],
        "wide_minus_strict_sz_pct": pct(f["industry_intersection"]["sz_in_inter"] - lk["shenzhen"], lk["shenzhen"]),
        "sz_top3_chain_sum": sum(b["sz"] for b in lk["per_chain"][:3]),
        "sz_top3_chain_pct": pct(sum(b["sz"] for b in lk["per_chain"][:3]), lk["shenzhen"]),
        "legacy_ods_probe": 17562,
        "legacy_mock_value": 12860,
        "city_null": base["city_null"],
        "city_count": base["distinct_city"],
        "other_prov_sum": n - gd,
        "four_city_gap_to_gd": gd - (sz + sum(c["count"] for c in others_gd)),
        "guangdong_outside_prd": gd - sz - sum(c["count"] for c in others_gd),
        "types": [
            {"key": k, "name": CN[k], "count": f["types"]["shenzhen_counts"][k],
             "pct_of_sz": pct(f["types"]["shenzhen_counts"][k], sz),
             "chain_count": lk["shenzhen_types"][k],
             "pct_of_chain_sz": pct(lk["shenzhen_types"][k], lk["shenzhen"])}
            for k in ORDER
        ],
        "chain_slice": {
            "linked_universe": lk["universe"],
            "shenzhen": lk["shenzhen"],
            "share_of_linked_pct": pct(lk["shenzhen"], lk["universe"]),
            "wide_slice_shenzhen": f["industry_intersection"]["sz_in_inter"],
            "wide_slice_denom": f["industry_intersection"]["base_in_chain"],
            "wide_slice_pct": pct(f["industry_intersection"]["sz_in_inter"],
                                  f["industry_intersection"]["base_in_chain"]),
        },
        "per_chain_shenzhen": [
            {"chain": b["chain"], "chain_name": b["chain_name"], "sz": b["sz"],
             "orgs": b["orgs"], "sz_pct": pct(b["sz"], b["orgs"])}
            for b in lk["per_chain"]
        ],
        "checks": {
            "sz_le_guangdong": sz <= gd,
            "guangdong_le_nation": gd <= n,
            "city_sum_le_nation": sum(v for _, v in base["city_dist_top"]) <= n,
            "sz_plus_other_prd_plus_rest_eq_gd": sz + sum(
                c["count"] for c in others_gd) + rest_gd == gd,
            "city_null_explained": base["city_null"] == 1,
        },
        "gaps": [
            "底册 city 为工商注册地，非实际经营地；深圳注册的集团总部会高估本地产业活动",
            "1 家 city 为空，按地市汇总时全国合计会差 1",
            "深汕特别合作区企业归属深圳统计，与惠州口径存在行政边界差异",
            "选产业后的深圳链属 16,875 家只覆盖 12 条战略链，不等于深圳全部产业企业",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("sz", sz, "share", out["share_of_nation_pct"], "gd", gd,
          "chain_sz", lk["shenzhen"], out["chain_slice"]["share_of_linked_pct"])


if __name__ == "__main__":
    main()
