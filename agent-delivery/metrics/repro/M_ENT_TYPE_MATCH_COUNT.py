#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_TYPE_MATCH_COUNT 企业分类型匹配数量（选产业 ∩ 选类型）。

口径：COUNT(DISTINCT org_id) WHERE 链属(industry_link_code 非空, 12 条战略链)
      AND 企业类型 ∈ 选中集合。
链归属：industry_code 首个 INB 前 7 位；一家只挂一条链（multi_chain_orgs=0），
故多选产业可直接相加，不产生重复计数。
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _build_ent_count21_facts import ensure  # noqa: E402

OUT = os.path.join(HERE, "M_ENT_TYPE_MATCH_COUNT_out.json")
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
    ln = lk["universe"]
    lc = lk["types"]

    rows = [{"key": k, "name": CN[k], "count": lc[k], "denom": ln,
             "pct": pct(lc[k], ln),
             "shenzhen": lk["shenzhen_types"][k],
             "shenzhen_pct": pct(lk["shenzhen_types"][k], lk["shenzhen"])}
            for k in ORDER]

    matrix = []
    for b in lk["per_chain"]:
        matrix.append({
            "chain": b["chain"], "chain_name": b["chain_name"], "orgs": b["orgs"],
            "sz": b["sz"],
            "types": {k: b["types"][k] for k in ORDER},
            "type_pct": {k: pct(b["types"][k], b["orgs"]) for k in ORDER},
        })

    out = {
        "metric_id": "M_ENT_TYPE_MATCH_COUNT",
        "metric_name": "企业分类型匹配数量",
        "support_judgment": "部分支持",
        "judgment_reason": (
            f"12 条战略链真链属 {ln:,} 家在底册内，与六类资质同源可交，"
            "链×类型矩阵 12×6 全部有数；但产业侧只有『链属』没有『非链属但属该产业』，"
            "标签表 7,015 家只挂顶层链无细分链被排除，且链标签来自 dwd_org_industry_tags "
            "单一表、无第二来源校验，故判部分支持。"
        ),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面交叉计数，无年度序列；不设基期",
        "sources": [
            "code/_snapshots21/chain_linked_type_20261023.json",
            "code/_snapshots21/chain_org_agg_20261022.json",
            "code/_snapshots21/ent_count21_facts_20261023.json",
            "code/_probe_linked_chain_strict.py",
            "gkx.dwd_org_industry_tags",
            "gkx.dwd_org_base_info",
            "gkx.dwd_org_tech_tag",
        ],
        "universe": ln,
        "universe_rule": "底册 credit_code ∈ 产业标签信用码 AND industry_link_code 非空；"
                         "链 = SUBSTRING(industry_code, LOCATE('INB', industry_code), 7)",
        "rows": rows,
        "matrix": matrix,
        "chain_union": {
            "sum_chain_orgs": lk["sum_chain_orgs"],
            "distinct_orgs": ln,
            "multi_chain_orgs": lk["multi_chain_orgs"],
            "additive": lk["multi_chain_orgs"] == 0,
            "wide_membership": f["industry_intersection"]["base_in_chain"],
            "unlinked_in_table": f["industry_intersection"]["base_in_chain"] - ln,
        },
        "overlap_pairs": lk["overlap_pairs"],
        "union_examples": {
            "high_tech|little_giant": lc["high_tech"] + lc["little_giant"]
            - lk["overlap_pairs"]["high_tech∩little_giant"],
            "foreign|sme": lc["foreign"] + lc["sme"] - lk["overlap_pairs"]["foreign∩sme"],
            "high_tech|sme": lc["high_tech"] + lc["sme"] - lk["overlap_pairs"]["high_tech∩sme"],
        },
        "sz_strict": lk["shenzhen"],
        "sz_wide": f["industry_intersection"]["sz_in_inter"],
        "none_of_six": lk["none_of_six"],
        "type_sum": lk["type_sum"],
        "duplicate_rate_pct": lk["duplicate_rate_pct"],
        "foreign_excl_hmt": lk["foreign_excl_hmt"],
        "shenzhen_vs_nation_pp": {
            k: round(100 * (lk["shenzhen_types"][k] / lk["shenzhen"]
                            - lc[k] / ln), 2) for k in ORDER
        },
        "naive_sums": {
            "high_tech+little_giant": lc["high_tech"] + lc["little_giant"],
            "software+ai_chain_orgs": 9335 + 4860,
            "six_type_sum": lk["type_sum"],
        },
        "parent_union": f["total"]["union"],
        "wide_scope_reference": {
            "denom": f["industry_intersection"]["base_in_chain"],
            "types": f["industry_intersection"]["type_counts"],
            "note": "宽口径=产业表全表信用码 ∩ 底册（含 7,015 家无细分链），仅作敏感性对照，不作发布值",
        },
        "checks": {
            "per_chain_sum_eq_universe": lk["sum_chain_orgs"] == ln,
            "matrix_sum_eq_type_total": all(
                sum(b["types"][k] for b in lk["per_chain"]) == lc[k] for k in ORDER),
            "sz_le_universe": lk["shenzhen"] <= ln,
            "agg_alignment": lk["check_all_equal"],
        },
        "gaps": [
            "7,015 家只有顶层链、无细分链的企业被排除；宽口径 35,046 与本口径 28,031 差 7,015",
            "链标签单表来源，无工商/专利侧二次校验，链归属可能有误挂",
            "国外主档无产业链上链表，选产业时国外 20,000 家整体缺席",
            "六类重叠（如高企∩专精特新 7,8xx 家），多选类型时并集<求和",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("universe", ln, "rows", [(r["key"], r["count"], r["pct"]) for r in rows])


if __name__ == "__main__":
    main()
