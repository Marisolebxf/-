#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_TYPE_RATIO 企业分类型占比。

规则：占比 = 同口径分子 / 同口径分母，分母跟随筛选条件：
  未选产业 → 底册 189,116（gkx.dwd_org_base_info 去重 org_id）
  选产业   → 12 条战略链真链属 28,031（industry_link_code 非空，链=industry_code 首个 INB）
分子与分母同源（同一 org_id 集合），不做跨库拼接。
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _build_ent_count21_facts import ensure  # noqa: E402

OUT = os.path.join(HERE, "M_ENT_TYPE_RATIO_out.json")
LINKED = os.path.join(HERE, "_snapshots21", "chain_linked_type_20261023.json")
TYPE_OUT = os.path.join(HERE, "M_ENT_TYPE_COUNT_out.json")
ORDER = ["high_tech", "little_giant", "little_giant_pro", "foreign", "sme", "listed"]
CN = {"high_tech": "高新技术企业", "little_giant": "专精特新中小企业",
      "little_giant_pro": "专精特新小巨人", "foreign": "外资企业",
      "sme": "小微企业", "listed": "上市/挂牌企业"}


def pct(a, b):
    return round(100.0 * a / b, 2)


def main():
    f = ensure()
    lk = json.load(open(LINKED, encoding="utf-8"))
    tcnt = json.load(open(TYPE_OUT, encoding="utf-8")) if os.path.exists(TYPE_OUT) else {}
    base_n = f["types"]["base_universe"]
    bc = f["types"]["counts"]
    lc = lk["types"]
    ln = lk["universe"]

    rows = []
    for k in ORDER:
        rows.append({
            "key": k, "name": CN[k],
            "base_count": bc[k], "base_denom": base_n,
            "base_ratio": round(bc[k] / base_n, 6), "base_pct": pct(bc[k], base_n),
            "chain_count": lc[k], "chain_denom": ln,
            "chain_ratio": round(lc[k] / ln, 6), "chain_pct": pct(lc[k], ln),
            "delta_pct_pp": round(pct(lc[k], ln) - pct(bc[k], base_n), 2),
            "shenzhen_pct": pct(f["types"]["shenzhen_counts"][k], f["types"]["shenzhen_universe"]),
            "chain_shenzhen_pct": pct(lk["shenzhen_types"][k], lk["shenzhen"]),
        })

    tot_base = sum(bc.values())
    tot_chain = sum(lc.values())
    out = {
        "metric_id": "M_ENT_TYPE_RATIO",
        "metric_name": "企业分类型占比",
        "support_judgment": "部分支持",
        "judgment_reason": (
            "分子分母都来自 gkx，同源可算；但分母存在两套互不兼容口径："
            f"未选产业 {base_n:,}、选产业真链属 {ln:,}（宽口径表内成员 35,046）。"
            "报表若不在页脚声明分母口径，同一『占比』会相差数倍；"
            "另外资含港澳台、小微含『未知』下限问题使占比只能作结构性参考。"
        ),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面占比，无年度序列；不设基期（分子分母同年同库）",
        "sources": [
            "code/_snapshots21/ent_count21_facts_20261023.json",
            "code/_snapshots21/chain_linked_type_20261023.json",
            "gkx.dwd_org_base_info",
            "gkx.dwd_org_tech_tag",
        ],
        "rule": {
            "formula": "ratio_type = COUNT(DISTINCT org_id WHERE type) / COUNT(DISTINCT org_id)",
            "denom_no_industry": base_n,
            "denom_with_industry": ln,
            "wide_denom_with_industry": f["industry_intersection"]["base_in_chain"],
            "rule_note": "分子分母必须来自同一 org_id 集合；禁止用全库分子除以筛选后分母",
            "rounding": "四舍五入到 2 位小数；各行独立四舍五入，合计不必为 100%",
        },
        "rows": rows,
        "sum_check": {
            "base_numerator_sum": tot_base,
            "base_ratio_sum_pct": round(100.0 * tot_base / base_n, 2),
            "chain_numerator_sum": tot_chain,
            "chain_ratio_sum_pct": round(100.0 * tot_chain / ln, 2),
            "note": "六类互有重叠（一家可同时是高企+专精特新+小微），占比和>100% 属正常，不是错误",
        },
        "overlap": tcnt.get("overlap"),
        "listed_stock_count": f["listed"]["stock_distinct_org"],
        "listed_stock_pct": pct(f["listed"]["stock_distinct_org"], base_n),
        "wide_minus_strict": f["industry_intersection"]["base_in_chain"] - ln,
        "wide_minus_strict_pct": pct(f["industry_intersection"]["base_in_chain"] - ln, ln),
        "chain_shenzhen": lk["shenzhen"],
        "shenzhen_chain_rows": [
            {"key": k, "count": lk["shenzhen_types"][k], "denom": lk["shenzhen"],
             "pct": pct(lk["shenzhen_types"][k], lk["shenzhen"])} for k in ORDER
        ],
        "ht_reduction_pct": pct(bc["high_tech"] - lc["high_tech"], bc["high_tech"]),
        "denom_reduction_pct": pct(base_n - ln, base_n),
        "shenzhen_rows": [
            {"key": k, "name": CN[k], "count": f["types"]["shenzhen_counts"][k],
             "denom": f["types"]["shenzhen_universe"],
             "pct": pct(f["types"]["shenzhen_counts"][k], f["types"]["shenzhen_universe"])}
            for k in ORDER
        ],
        "chain_rows": [
            {"chain": b["chain"], "chain_name": b["chain_name"], "orgs": b["orgs"],
             "share_of_linked_pct": pct(b["orgs"], ln),
             "types": {k: b["types"][k] for k in ORDER}}
            for b in lk["per_chain"]
        ],
        "checks": {
            "base_denom_eq_base_rows": base_n == f["base"]["rows"],
            "chain_denom_eq_sum_per_chain": ln == lk["sum_chain_orgs"],
            "no_multi_chain_double_count": lk["multi_chain_orgs"] == 0,
        },
        "gaps": [
            "两套分母（189,116 / 28,031）需在报表页脚显式声明，否则占比不可比",
            "外资含港澳台（10,417），剔除后 3,307，占比从 5.51% 降到 1.75%",
            "小微分母含 46,897 家 org_size=未知，125,477/189,116=66.35% 是下限",
            "高企/专精特新为历史获得累计口径，无有效期，占比高估当前有效存量",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("base", base_n, "chain", ln, "rows", [(r["key"], r["base_pct"], r["chain_pct"]) for r in rows])


if __name__ == "__main__":
    main()
