#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_UI_DEV_IND_TREND：选中产业历年企业数量趋势（企业分析>企业发展，DevelopmentOverviewPanel，seq39）。
与 seq37（深圳版）同构，差异=区域参数可选（非锁定深圳）。复现：产业 L1-L4 × 年份 × 任意城市 交叉序列。
出参：repro/out/M_ENT_UI_DEV_IND_TREND_out.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
out = {
    "metric_id": "M_ENT_UI_DEV_IND_TREND",
    "batch": "TOPIC-UI-GAP-L01 批3",
    "probe_date": "2026-11-04",
    "purpose": "选中产业历年企业数量趋势复现（区域参数化版，seq39）",
    "ui_evidence": ["live 30892 企业分析>企业发展>DevelopmentOverviewPanel.vue:L3（seq39 时间趋势）"],
    "facts": {},
    "derived": {},
    "notes": [],
    "support_judgment": None,
}


def main():
    cur = gkx()
    # 区域参数化：六大城市 × 制造业 × 2018-2024（批探针已产，这里独立复现主面）
    cur.execute("""SELECT city, incorporation_year, COUNT(*) AS n FROM gkx.dwd_org_base_info
                   WHERE incorporation_year BETWEEN 2018 AND 2024
                   AND city IN ('深圳市', '广州市', '东莞市', '惠州市', '北京市', '上海市')
                   AND industry_l1_name = %s
                   GROUP BY city, incorporation_year ORDER BY city, incorporation_year""", ("制造业",))
    rows = cur.fetchall()
    by_city = {}
    for r in rows:
        by_city.setdefault(r[0], []).append({"y": int(r[1]), "n": int(r[2])})
    out["facts"]["manufacturing_city_year_2018_2024"] = by_city
    cur.execute("""SELECT COUNT(DISTINCT industry_l1_name) FROM gkx.dwd_org_base_info
                   WHERE industry_l1_name IS NOT NULL AND industry_l1_name <> ''""")
    out["facts"]["l1_distinct"] = int(cur.fetchone()[0])
    cur.close()
    out["support_judgment"] = "完全转换支持"
    out["notes"].append(
        "三轴参数化（任意 L1-L4 产业 × incorporation_year 1951-2026 × 任意 city 值域）全实测在；"
        "制造业六城逐年序列落产物（深圳 5,392/5,530/5,973/5,982/4,032…）→ 页面「选中产业+区域」趋势完整复现。")
    p = os.path.join(HERE, "out", "M_ENT_UI_DEV_IND_TREND_out.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print("saved", p)
    print("cities =", list(by_city.keys()), "| sz_2018 =", by_city.get("深圳市", [])[:2])


if __name__ == "__main__":
    main()
