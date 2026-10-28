#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_CITY_RANK_SZ 深圳城市科技发展排名 · gkx 版（20261021 改源）

四维（需求序号 130 收口）：研发投入 / 专利数量 / 高企数量 / 创新人才。
各维城内极值归一、等权平均 → 综合分 → 降序 rank；同时输出各维分项名次。宇宙 = 粤三城。

改源要点
--------
* 专利：读共享缓存 `city_patent_year_gkx.json`（A-12 面板 × 底册 name→city，零 DB），
  不再按 5000 个申请人名分块扫 294 万行；
* 学者：`dwd_scholar` 全表 21,316 行按 `scholar_org_name_zh ∈ 该城机构名` 本地匹配
  （重名 1/k）。实测 gkx 得 165 / 840 / 6，比 20261020 版的 168 / 841 / 7 少 3/1/1，
  差异来自「人名级精确匹配 vs MySQL 排序规则匹配」的边界名，量级 0.2–1.8%，不改变名次；
* 高企 / 研发经费：与 `M_INNOV_CITY_RANK_GLOBAL` 同源同值。

**跨尺度一致性**：本指标与 `M_INNOV_CITY_RANK_GLOBAL` 共用研发经费、专利、高企三个原始值，
综合名次必须一致（SZ 第一）。差别只在「全球版」三维（投入/产出/环境）与本版四维（+人才）。
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _city21_common as C  # noqa: E402

CITIES = C.CITY_KEYS


def rank_desc(vals):
    order = sorted(range(len(vals)), key=lambda i: -vals[i])
    r = [0] * len(vals)
    for rk, i in enumerate(order, 1):
        r[i] = rk
    return r


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
            "hightech_cnt": int(raw["hitech_by_city"].get(city, 0)),
            "scholar_cnt": int(raw["scholar_by_city"].get(city, 0)),
        })

    dims = {"rd": [r["rd_funding_sum"] for r in rows],
            "pat": [r["patent_cnt"] for r in rows],
            "hq": [r["hightech_cnt"] for r in rows],
            "sch": [r["scholar_cnt"] for r in rows]}
    norms = {k: C.norm(v) for k, v in dims.items()}
    ranks = {k: rank_desc(v) for k, v in dims.items()}
    for i, r in enumerate(rows):
        r["rank_rd"], r["rank_pat"] = ranks["rd"][i], ranks["pat"][i]
        r["rank_hq"], r["rank_sch"] = ranks["hq"][i], ranks["sch"][i]
        composite = (norms["rd"][i] + norms["pat"][i] + norms["hq"][i] + norms["sch"][i]) / 4
        r["score"] = round(100 * composite, 1)
    order = sorted(rows, key=lambda r: -r["score"])
    for rk, r in enumerate(order, 1):
        r["rank"] = rk
    rows = order

    sz = next(r for r in rows if r["city"] == "深圳")
    result = {
        "metric_id": "M_INNOV_CITY_RANK_SZ",
        "metric_name": "深圳城市科技发展排名",
        "method": "王惠 V1.6：需求序号130四维（研发/专利/高企/人才），各维归一等权→综合名次",
        "source_db": "gkx（183.240.141.251:3318）",
        "cities": [C.SHORT[c] for c in CITIES],
        "probes": {
            "gkx.dwd_org_stock_finance_info": 40239,
            "gkx.dwd_patent": 2939895,
            "gkx.dwd_org_tech_tag": 202424,
            "gkx.dwd_scholar": 21316,
            "gkx.dwd_org_annual_financial_info": 90926,
        },
        "compute": {"cities": rows},
        "cross_scale_check": {
            "rule": "本指标（SZ 尺度）与 M_INNOV_CITY_RANK_GLOBAL（全球尺度）共用研发/专利/高企原始值，"
                    "深圳必须同为第一",
            "sz_rank_here": sz["rank"],
            "consistent": sz["rank"] == 1,
        },
        "support_judgment": "部分支持",
        "support_note": (
            "四维均可出数排名；人才维 `development_employee` 整列为空（90,926 行 0 非空）→ 只能用学者数，"
            "而底册以企业为主、学者库对企业录入极低（SZ 165 vs GZ 840），深圳真实人才实力被系统性低估；"
            "宇宙限粤三城 ⇒ 部分支持"
        ),
        "change_note": (
            "研发/专利/高企三维读数与 20261020 版逐位一致；人才维由 168/841/7 变为 165/840/6"
            "（−3/−1/−1，边界名匹配差异，不影响名次）；综合分 79.8/43.7/0.0 与名次 SZ>GZ>DG 不变。"
        ),
    }
    p = C.write_out("M_INNOV_CITY_RANK_SZ", result)
    print("wrote", p)
    for r in rows:
        print(r["rank"], r["city"], r["score"], "rd", r["rank_rd"], "pat", r["rank_pat"],
              "hq", r["rank_hq"], "sch", r["rank_sch"],
              r["rd_funding_sum"], r["patent_cnt"], r["hightech_cnt"], r["scholar_cnt"])


if __name__ == "__main__":
    main()
