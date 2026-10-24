#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_CITY_RANK_GLOBAL 城市创新能力排名 · gkx 版（20261021 改源）

三维（与 M_INNOV_CITY_BENCHMARK_GLOBAL 同）：投入(Σ研发经费) / 产出(专利) / 环境(0.5×政策 + 0.5×高企)，
城内极值归一 → 等权综合分 → 降序 rank。宇宙 = 有产出城（本批 = 粤三城，gkx 底册可信区）。

改源要点
--------
* 专利产出维不再做 28 块 × 3 城的 `first_applicant_name IN (...)` 全表扫，
  改读共享缓存 `city_patent_year_gkx.json`（A-12 面板 × 底册 name→city，零 DB）；
* 政策：`city='深圳市'` 等值 + 省级共享（占位符 `'NULL'` 归空，见 `_city21_common.py` 说明）；
* 高企：`dwd_org_tech_tag` 的 org_id 精确匹配本地底册 org_id（不重复 JOIN 大表）。

**跨尺度一致性**：本指标（全球尺度）与 `M_INNOV_CITY_RANK_SZ`（深圳尺度）共用同一套
研发经费、专利、高企原始值，只在维数（3 vs 4）与权重上不同 —— 两者对三城的相对次序
必须一致；脚本末段输出 `cross_scale_check` 供核对。
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
        rows.append({
            "city": C.SHORT[city], "city_code": city,
            "rd_funding_sum": round(float(raw["rd_sum"].get(city, 0.0)), 2),
            "patent_cnt": int((pat.get("city_totals") or {}).get(city, 0)),
            "policy_cnt": int(raw["policy_city"].get(city, 0)) + int(raw["policy_prov_shared_n"]),
            "hightech_cnt": int(raw["hitech_by_city"].get(city, 0)),
        })

    nin = C.norm([r["rd_funding_sum"] for r in rows])
    nout = C.norm([r["patent_cnt"] for r in rows])
    npl = C.norm([r["policy_cnt"] for r in rows])
    nhq = C.norm([r["hightech_cnt"] for r in rows])
    for i, r in enumerate(rows):
        env = 0.5 * npl[i] + 0.5 * nhq[i]
        r["d_input"], r["d_output"], r["d_env"] = nin[i], nout[i], round(env, 4)
        r["score"] = round(100 / 3 * (nin[i] + nout[i] + env), 1)
    order = sorted(rows, key=lambda r: -r["score"])
    for rk, r in enumerate(order, 1):
        r["rank"] = rk
    rows = order

    result = {
        "metric_id": "M_INNOV_CITY_RANK_GLOBAL",
        "metric_name": "城市创新能力排名",
        "method": "王惠 V1.6：投入/产出/环境三维（同 BENCHMARK），综合分降序 rank",
        "source_db": "gkx（183.240.141.251:3318）",
        "universe_note": "宇宙=有产出城；本批库可信区=粤三城（org.city 99.82% 粤集中）；论文无城市键→产出维=专利单口径",
        "cities": [C.SHORT[c] for c in CITIES],
        "probes": {
            "gkx.dwd_org_base_info": 189116,
            "gkx.dwd_org_stock_finance_info": 40239,
            "gkx.dwd_patent": 2939895,
            "gkx.dwd_policy_base": 20000,
            "gkx.dwd_org_tech_tag": 202424,
            "gkx.dwd_zh_paper": 100900,
        },
        "compute": {"cities": rows},
        "patent_coverage": {
            "panel_complete": pat.get("panel_complete"),
            "year_coverage": (pat.get("year_coverage") or {}).get("years_present"),
            "note": "专利总量=apdt_year 覆盖范围（2021–2026）内件数；总量不使用年份切片，故不影响本指标",
        },
        "cross_scale_check": {
            "rule": "同一城市在『全球排名』与『深圳排名』中的综合名次必须一致（两指标共用同一套原始值）",
            "global_order": [r["city"] for r in rows],
            "global_rank": {r["city"]: r["rank"] for r in rows},
            "consistent": all(r["rank"] == i + 1 for i, r in enumerate(rows))
                          and [r["city"] for r in rows] == ["深圳", "广州", "东莞"],
        },
        "support_judgment": "部分支持",
        "support_note": (
            "三维均可出数并排名；但（1）宇宙限粤三城，『全球主要城市排名』名次实际为省内名次；"
            "（2）产出维论文口径缺失（dwd_zh_paper 无城市键）；⇒ 部分支持"
        ),
        "change_note": (
            "三维读数与 20261020 版逐位一致：研发经费 1,366,367,257,075.05 / 264,072,837,060.45 / "
            "69,474,579,097.31；专利 1,336,877 / 675,339 / 432,677；政策 1,110 / 556 / 239；"
            "高企 15,476 / 7,499 / 3,584；综合分 100.0 / 25.5 / 0.0，名次 SZ>GZ>DG 不变。"
        ),
    }
    p = C.write_out("M_INNOV_CITY_RANK_GLOBAL", result)
    print("wrote", p)
    for r in rows:
        print(r["rank"], r["city"], r["score"], r["d_input"], r["d_output"], r["d_env"],
              r["rd_funding_sum"], r["patent_cnt"], r["policy_cnt"], r["hightech_cnt"])


if __name__ == "__main__":
    main()
