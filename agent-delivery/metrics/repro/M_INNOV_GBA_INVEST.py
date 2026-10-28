#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_GBA_INVEST · 湾区创新投入（20261021 版，gkx 单库）

口径：分城市、分年度的**上市公司研发费用**（亿元）。
关键工程裁定：`occur_period` 末两位 03/06/09/12 是「年初至今累计」，只能取 12 月；
四期相加会把同一笔费用重复计入（实测虚增 2.43 倍，见 out.json 的 wrong_caliber）。

数据来源（全部本地快照，零 SQL）：
  cityfam_stock_2019_2026_20261021.json ← gkx.dwd_org_stock_finance_info（40,239 行）
  innov_base_20261021.json              ← gkx.dwd_org_base_info（189,116 行）

输出：code/M_INNOV_GBA_INVEST_out.json
"""
from __future__ import annotations

import _gba21_common as G

METRIC = "M_INNOV_GBA_INVEST"
BASE_ORGS = {"深圳市": 95600, "广州市": 49605, "东莞市": 33590, "惠州市": 9979}


def main():
    rd = G.rd()
    years = [str(y) for y in range(2019, 2025)]
    per = rd["by_city_year_yi"]
    orgs = rd["orgs_by_city"]
    total = round(sum(rd["by_city_sum_yi"].values()), 2)

    rows = []
    for c in G.CITY4:
        yearly = {y: per.get(c, {}).get(y, 0.0) for y in years}
        s = round(sum(yearly.values()), 2)
        rows.append({
            "city": c,
            "rd_yi_by_year": yearly,
            "rd_sum_yi": s,
            "share": round(s / total, 4) if total else None,
            "listed_orgs": orgs.get(c, 0),
            "base_orgs": BASE_ORGS.get(c, 0),
            "coverage_pct": round(orgs.get(c, 0) / BASE_ORGS[c], 5) if BASE_ORGS.get(c) else None,
            "growth_2024_vs_2019": (round(yearly["2024"] / yearly["2019"] - 1, 4)
                                    if yearly.get("2019") else None),
        })
    rows.sort(key=lambda r: -r["rd_sum_yi"])

    # 错误口径对照：把 03/06/09/12 四期全部相加（旧稿 18,231.5 亿的来历）
    stock = G.load("cityfam_stock_2019_2026_20261021.json") or []
    org2city = {r["org_id"]: r.get("city") for r in G.base_rows()}
    wrong = {}
    for oid, period, amt in stock:
        if amt is None:
            continue
        y = str(period)[:4]
        c = org2city.get(oid)
        if c in G.CITY4 and "2019" <= y <= "2024":
            wrong[c] = wrong.get(c, 0.0) + float(amt)
    wrong_total = round(sum(wrong.values()) / 1e8, 2)

    # 研发强度旁证：四城研发费用 / 底册机构数（元/家·年）
    per_org = {r["city"]: round(r["rd_sum_yi"] * 1e8 / r["base_orgs"], 0)
               for r in rows if r["base_orgs"]}

    result = {
        "metric_id": METRIC,
        "name": "湾区创新投入",
        "formula_owner": "AI-20261016（非王惠；本版沿用 20261020 已验收口径）",
        "asof": "2026-10-22",
        "unit": "亿元（人民币，现价，名义值）",
        "caliber": "上市公司年报研发费用，按注册地归城，仅取 12 月报告期",
        "window": ["2019", "2024"],
        "rows": rows,
        "total_yi": total,
        "wrong_caliber": {
            "sum_all_periods_yi": wrong_total,
            "by_city_yi": {c: round(v / 1e8, 2) for c, v in wrong.items()},
            "inflation_ratio": round(wrong_total / total, 4) if total else None,
            "why_wrong": "occur_period 03/06/09/12 均为年初至今累计值，四期相加=同一笔费用被计 4 次",
        },
        "quality_audit": rd["anomaly"],
        "rd_per_base_org_yuan": per_org,
        "coverage": {
            "listed_orgs_with_rd": rd["orgs_total"],
            "base_orgs_4city": sum(BASE_ORGS.values()),
            "pct": round(rd["orgs_total"] / sum(BASE_ORGS.values()), 5),
            "note": "覆盖率为「有 12 月研发费用的上市公司数 / 四城底册机构数」，不是研发活动覆盖率",
        },
        "city_coverage": {
            "computable": G.CITY4,
            "missing": G.MISSING7,
            "n_computable": 4, "n_gba11": 11,
            "pct": round(4 / 11, 4),
            "hk_mo_note": ("dwd_forg_base_info 20,000 行经实测 country 全为 NULL、country_code 99.16% 为 GB，"
                           "无香港/澳门机构，无法补入港澳"),
        },
        "probes": {
            "stock_finance_rows": G.load("gba_rd_20261021.json")["rows_total"],
            "stock_finance_null_amount": G.load("gba_rd_20261021.json")["rows_null_amount"],
            "annual_arch_development_am": "90,926 行，非空 0（整列为空，禁用）",
            "occur_period_periods": ["03", "06", "09", "12"],
            "rd_rows_4city_2019_2024": sum(1 for oid, p, a in stock
                                           if a is not None and org2city.get(oid) in G.CITY4
                                           and "2019" <= str(p)[:4] <= "2024"),
        },
        "support_judgment": "部分支持",
        "support_reason": (
            "研发金额口径存在且可年度对齐，但只覆盖上市公司（856 家 / 四城底册 188,774 家 = 0.45%）；"
            "11 城仅 4 城有机构与研发数据，港澳在 gkx.dwd_forg_base_info 中为 0；"
            "24.8% 的公司-年存在「12 月 < 9 月」数值矛盾；无全社会 R&D、无财政科技支出表 —— 故判部分支持，"
            "对外只能称「湾区上市公司研发费用合计」，不可当全社会创新投入发布"
        ),
    }
    G.write_out(METRIC, result)
    print("total", total, "wrong", wrong_total, "ratio", result["wrong_caliber"]["inflation_ratio"])
    for r in rows:
        print(r["city"], r["rd_sum_yi"], r["share"], r["listed_orgs"], r["coverage_pct"],
              r["growth_2024_vs_2019"])


if __name__ == "__main__":
    main()
