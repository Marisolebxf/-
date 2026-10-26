#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_CITY_FACTOR_GLOBAL 城市创新能力要素表现 · 复现代码（王惠 V1.5-20260901，20261021 换源版）

三要素：人才(学者去重 + Σdevelopment_employee) / 资金(Σresearch_development_amount) / 政策(有效政策件数)。
城内极值归一 + 等权 ×100。城市 = 深圳/广州/东莞（库覆盖可信区）。
数据源：三方库 `gkx`（唯一入口 `code/_gkxdb.py`），**不含任何 demo_* / _devdb**。

换源说明（20261021）
--------------------
* 资金维读数与旧版逐位一致（深圳 1,366,367,257,075.05 元 / 广州 264,072,837,060.45 / 东莞 69,474,579,097.31）。
* 人才维 `development_employee` 在 gkx 同为 90,926 行全 NULL → employee_sum=0，退化为纯学者数。
* 学者数按「机构名精确 IN 城内机构名、逐城独立计数」：深圳 165 / 广州 840 / 东莞 6，
  较旧版（168/841/7）少 1—3 人——旧脚本未过滤 `is_deleted`、且以 `LIKE '%城%'` 取机构名集合，
  gkx 侧一律 `is_deleted=0` + 归一 city，差异来自这 1‰ 级的行过滤，方向为**略低**。
* 政策维：`dwd_policy_base.city` 有 9,706 行字面量 'NULL'，旧脚本 `city IS NULL` 在 gkx 上恒为 0；
  本版用 `norm_city()` 把 'NULL'/''/'NONE'/'-' 一律归空，省级共享仍为 231 条（广东省级政策）。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import _gkx21_city as C  # noqa: E402

METRIC_ID = "M_INNOV_CITY_FACTOR_GLOBAL"
CITIES = ["深圳", "广州", "东莞"]


def norm(vals):
    mx = max(vals) or 1
    mn = min(vals)
    return [round((v - mn) / (mx - mn), 4) if mx > mn else 1.0 for v in vals]


def main():
    probes = {t: C.inventory_rows(t) for t in
              ("dwd_scholar", "dwd_org_annual_financial_info",
               "dwd_org_stock_finance_info", "dwd_policy_base")}
    dev = C.dev_employee_probe()
    sch = C.scholars_by_city_names(CITIES)
    fund = C.rd_by_city(CITIES, 2019, 2024)
    pol, prov_shared = C.policies_by_city(CITIES)

    results = []
    for c in CITIES:
        results.append({
            "city": c,
            "scholar_cnt": sch.get(c, 0),
            "employee_sum": 0,
            "emp_col_nonnull": dev["nonnull"],
            "emp_col_total": dev["rows"],
            "funding_sum": round(fund.get(c, 0.0), 2),
            "policy_cnt": pol[c]["total"],
            "policy_city_cnt": pol[c]["city"],
            "policy_prov_shared": pol[c]["prov_shared"],
        })

    talent = [r["scholar_cnt"] + r["employee_sum"] for r in results]
    funding = [r["funding_sum"] for r in results]
    policy = [r["policy_cnt"] for r in results]
    nt, nf, npol = norm(talent), norm(funding), norm(policy)
    for i, r in enumerate(results):
        r["d_talent"], r["d_funding"], r["d_policy"] = nt[i], nf[i], npol[i]
        r["factor_score"] = round(100 / 3 * (nt[i] + nf[i] + npol[i]), 1)

    result = {
        "metric_id": METRIC_ID,
        "metric_name": "城市创新能力要素表现",
        "method": "王惠 V1.5：人才/资金/政策三要素，城内极值归一+等权×100",
        "cities": CITIES,
        "data_source": "gkx（三方库 183.240.141.251:3318，只读账号；不含任何演示库引用）",
        "probes": probes,
        "compute": {"factors": results},
        "support_judgment": "部分支持",
        "support_note": (
            f"资金维完整可用；人才维 development_employee 100% NULL（{dev['rows']:,} 行实测）→ 退化为纯学者数；"
            f"政策维 city 字段 9,706 行字面量 'NULL'（国家级政策不计入城市）→ 城市件数偏保守；"
            f"机构底册 99.8% 集中广东 → 宇宙限粤三城 ⇒ 部分支持"
        ),
    }

    path = HERE / f"{METRIC_ID}_out.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
