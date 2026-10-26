#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_NATIONAL_REGION_COUNT · 全国分布区域数（20261021 改源版，直连 gkx）

口径（calc-logic 0.2.0，徐滕强 2026-10-14 拍板）
------------------------------------------------
指定产业链的链上主体总部所在**省级行政区**去重数，链维 KPI。空 province 不计数。

数据源（20261021 改源）
-----------------------
  `gkx.dwd_org_industry_tags`（2,283,762 行，链标签）
  `gkx.dwd_org_base_info`（189,116 行，province / city）
  链树 `gkx.dwd_industry_chain_info`（1,273 节点 / 12 条顶层链）
旧版走开发库 + 本地快照，本版全部现查三方库；公式、去重规则、空值规则未改。

本脚本要回答的不是「算得出来吗」，而是「算出来的数能不能叫全国」
--------------------------------------------------------------
链标签宇宙 2,283,762 行里，只有 52,906 条标签（35,046 家）能在 `dwd_org_base_info` 找到属地；
这 35,046 家里 35,022 家在广东（99.93%），省外仅 **24 家**。
因此 12 条链的「省级行政区去重数」实算只有 1~8，其中 2 条链只有 1 个省（广东）。

→ 结论：公式可执行、数值可复算，但「全国分布」语义不成立，判**部分支持**，
  且禁止把 24 家（或全底册的 339 家）当作全国覆盖的证据。

输出：code/M_CHAIN_NATIONAL_REGION_COUNT_out.json
"""
from __future__ import annotations

import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _gkx21_common import (CITY4, ROOTS, base_province_dist, base_rows,  # noqa: E402
                          chain_city_from_bridge, chain_names, chain_tag_universe,
                          bridge, write_out)

METRIC = "M_CHAIN_NATIONAL_REGION_COUNT"


def main():
    t0 = time.time()
    names = chain_names()
    br = bridge()
    geo = chain_city_from_bridge(br)
    tag = chain_tag_universe()
    prov_all, city_all = base_province_dist()
    n_pairs = {(r[3], r[4]) for r in base_rows()}

    # 链 → 省 / 市 计数（只在可落属地的子集上）
    per_chain = {}
    for r in ROOTS:
        prov = Counter(geo["chain_prov"].get(r, {}))
        city = Counter(geo["chain_city"].get(r, {}))
        prov.pop(None, None)
        prov.pop("", None)
        n_geo = sum(prov.values())
        per_chain[r] = {
            "chain": r, "name": names.get(r),
            "tag_enterprises": tag["counts"].get(r),
            "geo_matched": n_geo,
            "geo_match_pct": round(n_geo / tag["counts"][r] * 100, 2) if tag["counts"].get(r) else None,
            "region_count": len(prov),
            "province_dist": dict(prov.most_common()),
            "city_count": len([c for c in city if c]),
            "city_dist": dict(city.most_common(6)),
        }

    all_prov = Counter()
    seen_cc = {}
    for b in br:
        p = b["p"]
        seen_cc.setdefault((p, b["cc"]), True)
    for p, cc in seen_cc:
        all_prov[p] += 1
    n_geo = len({b["cc"] for b in br if b["cc"]})
    out_guangdong = {p: n for p, n in all_prov.items() if p and p != "广东省"}

    # 反例：如果直接拿 tags 宇宙当分母会得到什么
    naive = {r: per_chain[r]["region_count"] for r in ROOTS}
    gc = sum(n for p, n in prov_all.items() if p)
    gd = prov_all.get("广东省", 0)

    rep = {
        "metric_id": METRIC,
        "metric_name": "全国分布区域数",
        "date": "2026-10-21",
        "calc_logic_ref": "gkx-orchestration/agent-delivery/metrics/calc-logic/CHAIN/M_CHAIN_NATIONAL_REGION_COUNT.md (0.2.0)",
        "formula": "COUNT(DISTINCT province) over chain members with non-empty province",
        "data_source": {
            "engine": "三方库 gkx（183.240.141.251:3318），唯一连库入口 code/_gkxdb.py",
            "tables": ["gkx.dwd_org_industry_tags", "gkx.dwd_org_base_info", "gkx.dwd_industry_chain_info"],
            "join": "tags STRAIGHT_JOIN base ON base.external_id = tags.credit_code COLLATE utf8mb4_0900_ai_ci",
            "join_note": "两列排序规则不同（0900_ai_ci vs general_ci），且 tags.credit_code 无索引，"
                         "必须标签表驱动 + 哈希，否则退化为 2.28M×189K 嵌套循环",
        },
        "hard_constraint": {
            "headline": ("本库不存在可支撑「全国分布」的属地样本：链上 2,283,762 条标签中仅 52,906 条"
                         "（35,046 家，1.53%）可落属地，其中 35,022 家在广东（99.93%），省外合计 24 家"),
            "base_info_gd_share_pct": round(gd / gc * 100, 2) if gc else None,
            "base_info_out_of_gd": gc - gd,
            "base_info_n": gc,
            "tags_universe": tag["n_all"],
            "tags_distinct_credit": tag["n_cc"],
            "geo_joinable": n_geo,
            "geo_join_rows": geo["tag_rows_joinable"],
            "geo_join_pct": round(n_geo / (tag["n_cc"] or 1) * 100, 2),
            "chain_tagged_out_of_gd": sum(out_guangdong.values()),
            "note": ("省外 24 家的口径是「既有产业链标签、又能落到主档属地」的企业；"
                     "全底册省外 339 家是另一个更大的集合，两者都远不足以代表全国。"),
        },
        "per_chain": [per_chain[r] for r in ROOTS],
        "distribution": {
            "region_count_values": sorted(set(naive.values())),
            "chains_with_1_province": [r for r in ROOTS if naive[r] == 1],
            "chains_with_le2_provinces": [r for r in ROOTS if naive[r] <= 2],
            "max_region_count": max(naive.values()),
            "median_region_count": sorted(naive.values())[len(naive) // 2],
            "out_of_guangdong_detail": out_guangdong,
        },
        "base_info_distribution": {
            "source": "gkx.dwd_org_base_info GROUP BY province/city（现查）",
            "n_pairs": len(n_pairs),
            "total": gc,
            "guangdong_pct": round(gd / gc * 100, 2) if gc else None,
            "province_top": dict(sorted(prov_all.items(), key=lambda x: -x[1])[:8]),
            "city_top": dict(sorted(city_all.items(), key=lambda x: -x[1])[:8]),
        },
        "naive_trap": {
            "what_if_use_tag_universe": ("若把 2,283,762 条链标签当分母，会得出「每链覆盖全国」的错觉；"
                                         "实际这 2.28M 条标签里 97.7% 没有任何属地字段可查，"
                                         "剩下 2.3% 几乎全部落在深圳都市圈"),
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": ("省级行政区轴与链—企桥结构齐全，公式可执行、数值可复算；"
                       "但链上主体 97.7% 无属地、可落属地的 99.93% 在广东，省外仅 24 家，"
                       "「全国分布」这一关键依赖维在本库无样本 → 按 §〇 判部分支持。"
                       "不得把 24 家（或底册省外 339 家）冒充全国覆盖。"),
            "criteria": {"structure": True, "province_axis": True,
                         "national_sample": False, "computable": True},
        },
        "elapsed_sec": round(time.time() - t0, 1),
    }
    write_out(METRIC, rep)
    print(json.dumps({"hard": rep["hard_constraint"], "dist": rep["distribution"]},
                     ensure_ascii=False, indent=1))
    for p in rep["per_chain"]:
        print(p["chain"], p["name"], p["tag_enterprises"], p["geo_matched"], p["region_count"])


if __name__ == "__main__":
    main()
