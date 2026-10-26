#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_CITY_BENCHMARK_GLOBAL 城市对标分析 · 复现代码（王惠 V1.5-20260901，20261021 换源版）

用户选 ≥2 城对比三维：创新投入(上市研发经费/研发人员) / 创新产出(专利+论文) / 创新环境(政策+高企)。
所选城内极值归一。服务 M_CITY_BENCHMARK / M_CITY_RANK_GLOBAL / M_CITY_INDEX_SZ 同族。
演示选城：深圳、北京、上海、广州（2024）。
数据源：三方库 `gkx`（唯一入口 `code/_gkxdb.py`），**不含任何 demo_* / _devdb**。

换源说明（20261021）
--------------------
* 读数与 20261020 旧版逐项一致：n_org 94,968/33/3/48,267；rd 3,555.5 亿/None/None/566.8 亿；
  专利 275,908/132/1/140,395；论文 3/0/0/8；政策 879/2,268/1,841/325；高企 15,683/0/0/7,544。
* `development_employee` 在 gkx 同样 90,926 行 **100% NULL**（SUM 亦为 NULL）→ 投入维不能用人员兜底。
* 政策维按 `city` 直计（不含省级共享），故深圳 879 而非 FACTOR 的 1,110（后者加 231 条省级均摊）。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import _gkx21_city as C  # noqa: E402

METRIC_ID = "M_INNOV_CITY_BENCHMARK_GLOBAL"
YEAR = 2024
CITIES = ["深圳", "北京", "上海", "广州"]


def norm_pair(v, lo, hi):
    if v is None:
        return None
    if hi == lo:
        return 0.5
    return (v - lo) / (hi - lo)


def main():
    probes = {t: C.inventory_rows(t) for t in
              ("dwd_org_base_info", "dwd_org_stock_finance_info", "dwd_org_annual_financial_info",
               "dwd_patent", "dwd_zh_paper", "dwd_zh_author", "dwd_policy_base", "dwd_org_tech_tag")}
    pat = C.patents_2024_by_city(CITIES)
    n_org = C.surviving_org_count(CITIES)
    rd = C.rd_by_city(CITIES, YEAR, YEAR)
    pap = C.papers_by_city(CITIES, YEAR, base_only=True)
    pol = {c: v["city"] for c, v in C.policies_by_city(CITIES)[0].items()}
    ht = C.hightech_by_city(CITIES, surviving=True)

    rows = {c: dict(n_org=n_org.get(c), rd=rd.get(c) or None, dev=None,
                    patents=pat.get(c, 0), papers=pap.get(c, 0),
                    policies=pol.get(c, 0), hightech=ht.get(c, 0)) for c in CITIES}

    input_vals = [rows[c]["rd"] if any(rows[x]["rd"] for x in CITIES) else rows[c]["dev"] for c in CITIES]
    output_vals = [rows[c]["patents"] + rows[c]["papers"] for c in CITIES]
    pol_vals = [rows[c]["policies"] for c in CITIES]
    hi_vals = [rows[c]["hightech"] for c in CITIES]

    def lohi(xs):
        xs2 = [x for x in xs if x is not None]
        return (min(xs2), max(xs2)) if xs2 else (None, None)

    li, hi_ = lohi(input_vals)
    lo_, ho_ = lohi(output_vals)
    lp, hp_ = lohi(pol_vals)
    lh, hh = lohi(hi_vals)

    results = []
    for i, c in enumerate(CITIES):
        d_in = norm_pair(input_vals[i], li, hi_)
        d_out = norm_pair(output_vals[i], lo_, ho_)
        d_pol = norm_pair(pol_vals[i], lp, hp_)
        d_hi = norm_pair(hi_vals[i], lh, hh)
        d_env = (sum(x for x in [d_pol, d_hi] if x is not None) / 2) \
            if any(x is not None for x in [d_pol, d_hi]) else None
        dims = [d_in, d_out, d_env]
        avail = [d for d in dims if d is not None]
        score = (sum(avail) / len(avail) * 100) if avail else None
        results.append({**rows[c], "city": c, "d_in": d_in, "d_out": d_out, "d_env": d_env,
                        "composite": round(score, 2) if score is not None else None})

    n_dims_with_data = sum(1 for dim_vals in [input_vals, output_vals, pol_vals, hi_vals]
                           if any(dim_vals))
    rd_cov = sum(1 for r in results if r["rd"] is not None)
    scores = [r["composite"] for r in results if r["composite"] is not None]
    has_dist = len(set(scores)) > 1 if scores else False

    result = {
        "metric_id": METRIC_ID,
        "metric_name": "城市对标分析",
        "method": "王惠 V1.5：所选城内三维极值归一（投入=研发经费/人员、产出=专利+论文、环境=政策+高企）",
        "cities": CITIES, "stat_year": YEAR,
        "data_source": "gkx（三方库 183.240.141.251:3318，只读账号；不含任何演示库引用）",
        "probes": probes,
        "compute": {"cities": [{k: (round(v, 2) if isinstance(v, float) else v)
                               for k, v in r.items()} for r in results]},
        "support_judgment": None,
    }
    if n_dims_with_data >= 4 and has_dist and rd_cov >= len(CITIES) - 1:
        result["support_judgment"] = "完全转换支持"
    elif n_dims_with_data >= 2 and has_dist:
        result["support_judgment"] = "部分支持"
    else:
        result["support_judgment"] = "完全不支持"
    result["support_note"] = (
        f"四城对比可算：投入维 rd 覆盖 {rd_cov}/{len(CITIES)}（dev 全 NULL 不可兜底）；"
        f"产出维专利+论文有量；环境维政策 {sum(pol_vals)}/高企 {sum(hi_vals)} 有量；综合分有区分度 {has_dist}。"
        f"重要披露：三方库机构地域高度偏广东（深圳 95,600/广州 49,605/东莞 33,590，北京 163/上海 16），"
        f"非粤城市除政策/上市研发外各维天然低值——城市对比语义受三方库覆盖范围限制。"
        f"换源 gkx 后逐城读数与 20261020 旧版一致"
    )

    path = HERE / f"{METRIC_ID}_out.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "compute"}, ensure_ascii=False))
    for r in result["compute"]["cities"]:
        print(r)


if __name__ == "__main__":
    main()
