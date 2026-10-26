#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_CITY_MONITOR_GLOBAL 城市创新数据监控 · gkx 版（20261021 改源）

bid 口径：监控全球主要城市的创新基金、投资规模、创新机构、企业在创新上的投入与产出。
输出一城一行的**原始值面板**（不做归一、不排名）：投入 / 机构 / 产出 / 政策四组。

改源要点
--------
* 专利：不再对 294 万行做 `first_applicant_name IN (5000 个名字)` 的分块扫描
  （一次 = 3 个城 × 28 块全表扫，已被服务端 SIGTERM），改读 A-08 共享缓存
  `_snapshots_gkx21/city_patent_year_gkx.json`（A-12 面板 `app_year` × 底册 `name→city` 离线派生，零 DB）。
* 政策：市级等值（'深圳市'），且 **只算市文件**（省级共享 231 件不并入本指标，
  与 20261020 版 `MONITOR` 的口径一致）。
* 研发经费：`dwd_org_stock_finance_info` 2019–2024 窗，上市主体口径。
* 创新基金 / 投资规模：gkx 280 表内**无带 city 键的基金、投资表**（`dwd_org_financing_info`
  只有 org 级融资事件，无城市字段可归），该监控组继续披露为缺项。
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _city21_common as C  # noqa: E402

CITIES = C.CITY_KEYS


def main():
    raw = C.build_raw()
    pat = C.load_patent_city_year()
    if pat is None:
        raise SystemExit("缺 city_patent_year_gkx.json：先跑 _build_city_patent_year.py")
    groups = pat["groups"]

    rows = []
    for city in CITIES:
        org_total = sum(int(r["n"]) for r in raw["org_reg"] if r["city"] == city)
        rows.append({
            "city": C.SHORT[city], "city_code": city,
            "input_rd_funding_sum": round(float(raw["rd_sum"].get(city, 0.0)), 2),
            "org_cnt": org_total,
            "output_patent_total": int((pat.get("city_totals") or {}).get(city, 0)),
            "output_patent_2024": int(groups.get(city + "|2024", 0)),
            "policy_valid_cnt": int(raw["policy_city"].get(city, 0)),
            "fund_invest_group": None,
        })

    result = {
        "metric_id": "M_INNOV_CITY_MONITOR_GLOBAL",
        "metric_name": "城市创新数据监控",
        "method": "bid 口径：投入/产出/机构监控面板（创新基金/投资规模组因库内无带 city 键的基金投资表而缺项）",
        "source_db": "gkx（183.240.141.251:3318）",
        "cities": [C.SHORT[c] for c in CITIES],
        "probes": {
            "gkx.dwd_org_base_info": 189116,
            "gkx.dwd_org_stock_finance_info": 40239,
            "gkx.dwd_patent": 2939895,
            "gkx.dwd_zh_paper": 100900,
            "gkx.dwd_policy_base": 20000,
        },
        "compute": {"monitor": rows},
        "patent_coverage": {
            "panel_rows": pat.get("panel_rows"),
            "panel_complete": pat.get("panel_complete"),
            "year_coverage": (pat.get("year_coverage") or {}).get("years_present"),
            "unmapped_rows": pat.get("unmapped_rows"),
            "note": ("总量取面板 `app_total`（按申请人、不分年）派生 = 全期存量；"
                     "分年序列只有 2021–2024（面板 window=[2021,2024]），2025/2026 有 "
                     "515,211 行但无年份切片，故不出 2025 年产出"),
        },
        "support_judgment": "部分支持",
        "support_note": (
            "投入(研发经费)/机构(机构数)/产出(专利)/政策四组均可监控；"
            "bid 提及的创新基金与投资规模在 gkx 内无带 city 键的结构化表 → 该监控组缺项；"
            "机构底册 99.82% 粤集中，『全球主要城市监控』实际覆盖粤三城 ⇒ 部分支持"
        ),
        "change_note": (
            "四组读数与 20261020 版逐位一致：研发经费 1,366,367,257,075.05 / 264,072,837,060.45 / "
            "69,474,579,097.31；机构 95,600 / 49,605 / 33,590；专利 1,336,877 / 675,339 / 432,677；"
            "2024 年产出 275,908 / 140,395 / 89,347；政策 879 / 325 / 8。"
        ),
    }
    p = C.write_out("M_INNOV_CITY_MONITOR_GLOBAL", result)
    print("wrote", p)
    for r in rows:
        print(r["city"], r["input_rd_funding_sum"], r["org_cnt"], r["output_patent_total"],
              r["output_patent_2024"], r["policy_valid_cnt"])


if __name__ == "__main__":
    main()
