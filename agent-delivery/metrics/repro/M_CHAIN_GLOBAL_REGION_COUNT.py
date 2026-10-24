#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_GLOBAL_REGION_COUNT 全球分布区域数（20261021 改源版）

口径（calc-logic/CHAIN，徐滕强）：产业链基础指标模型的「全球产业区域分布」维，
即「每个国家对应的企业和机构总数」；本指标取其派生量：该链覆盖多少个区域。

本脚本能做的与不能做的（这一节直接决定判档，勿删）：
  · 能做：`gkx.dwd_patent.country_code` 的 6 个区域代码（CN / WO / HK / JP / TW / MO）
    全局计数，以及**按申请人名落到 35,046 家链上企业**后的「链 × PCT/日本」件数；
  · 不能做：企业/机构按国家计数——`dwd_org_base_info` 只有省/市、无国别字段，
    `dwd_research_institute_base_info` 2,074 家全在中国境内，
    `dwd_forg_*` 外国企业 20,000 行虽带 GB/US，但与工业标签交集为 0（见 chain_intl 缓存）；
  · 因此「区域数」在链级只能取到 1—2（CN 与 WO），对 12 条链没有区分度，
    不能冒充需求定义里的「每个国家的企业/机构总数」。判 **完全不支持**。

零 DB：全部读 `_snapshots21/chain_intl_gkx_20261021.json`（2026-10-22 01:14 生成，
专利 2,939,895 行、国别 6 码、PCT 申请人 4,001 名）+ `bridge_20261021.json`。

输出：code/M_CHAIN_GLOBAL_REGION_COUNT_out.json
"""
from __future__ import annotations

import time

from _reg5_common import (CHAIN_AXIS, CHAIN_CN, SNAP, _load, chain_firms, pct, stats, write_out)

MID = "M_CHAIN_GLOBAL_REGION_COUNT"


def main() -> None:
    t0 = time.time()
    ci = _load("chain_intl_gkx_20261021.json", {})
    if not ci:
        raise SystemExit("缺 chain_intl_gkx_20261021.json，先跑 code/_build_chain_intl_gkx.py")

    country = [(r["country_code"], int(r["n"])) for r in ci["patent_country"]]
    total_pat = sum(n for _, n in country)
    wo = {r["nm"]: int(r["n"]) for r in ci["wo_applicants"]}
    jp = {r["nm"]: int(r["n"]) for r in ci["jp_applicants"]}
    name_patent = ci["name_patent"]          # name -> [全量件数, WO/PCT 件数]（**不是授权数**）
    firms = chain_firms()

    matrix = []
    for ch in CHAIN_AXIS:
        names = firms.get(ch, [])
        pat_cnt = sum(int(name_patent.get(n, [0, 0])[0]) for n in names)
        wo_names = [n for n in names if wo.get(n)]
        jp_names = [n for n in names if jp.get(n)]
        wo_cnt = sum(wo[n] for n in wo_names)
        jp_cnt = sum(jp[n] for n in jp_names)
        regions = ["CN"]
        if wo_cnt:
            regions.append("WO")
        if jp_cnt:
            regions.append("JP")
        matrix.append({
            "chain": ch,
            "chain_name": CHAIN_CN[ch],
            "firms": len(names),
            "firms_with_patent": sum(1 for n in names if int(name_patent.get(n, [0, 0])[0]) > 0),
            "patent_rows_all_regions": pat_cnt,
            "pct_firms_with_pct": pct(len(wo_names), len(names)),
            "pct_firms": len(wo_names),
            "pct_patent_rows": wo_cnt,
            "jp_firms": len(jp_names),
            "jp_patent_rows": jp_cnt,
            "cn_patent_rows_est": max(0, pat_cnt - wo_cnt - jp_cnt),
            "regions_covered": regions,
            "n_regions_covered": len(regions),
        })

    n_region_dist = {}
    for m in matrix:
        k = str(m["n_regions_covered"])
        n_region_dist[k] = n_region_dist.get(k, 0) + 1

    payload = {
        "metric_id": MID,
        "metric_name": "全球分布区域数",
        "date": "2026-10-22",
        "formula_owner": "徐滕强（CHAIN 域 calc-logic）",
        "source": "gkx.dwd_patent(country_code) + gkx.dwd_org_base_info + gkx.dwd_org_industry_tags",
        "patent_rows": ci.get("patent_rows"),
        "country_total": [{"region": c, "rows": n, "share_pct": pct(n, total_pat)} for c, n in country],
        "chain_axis": len(CHAIN_AXIS),
        "matrix": matrix,
        "probes": {
            "patent_rows_total": total_pat,
            "distinct_country_codes": len(country),
            "china_share_pct": pct(dict(country).get("CN", 0), total_pat),
            "pct_applicants": len(wo),
            "jp_applicants": len(jp),
            "chain_firms": sum(m["firms"] for m in matrix),
            "firms_with_pct": sum(m["pct_firms"] for m in matrix),
            "firms_with_pct_pct": pct(sum(m["pct_firms"] for m in matrix),
                                       sum(m["firms"] for m in matrix)),
            "n_regions_distribution": n_region_dist,
            "foreign_org_base_rows": int(ci.get("forg_rows", {}).get("dwd_forg_base_info", 0)),
            "foreign_org_country": ci.get("forg_country"),
            "foreign_extid_in_tags": ci.get("forg_extid_in_tags"),
            "foreign_name_in_chain": ci.get("forg_name_in_chain"),
            "hk_rows": dict(country).get("HK"),
            "mo_rows": dict(country).get("MO"),
            "tw_rows": dict(country).get("TW"),
        },
        "stats_pct_patent_rows": stats([m["pct_patent_rows"] for m in matrix]),
        "support_judgment": {
            "data_support_level": "完全不支持",
            "reason": (
                f"需求定义是「每个国家对应的企业和机构总数」，而 gkx 侧企业底册 189,116 行只有省/市、无国别字段，"
                f"境内科研机构 2,074 家全在中国境内，三张境外主体表各 20,000 行却无产业链列，"
                f"外国企业表与工业标签交集为 0、与链上企业名交集为 0；"
                f"唯一带国别的 `dwd_patent.country_code` 只有 {len(country)} 个代码，"
                f"China 占 {pct(dict(country).get('CN', 0), total_pat)}%、WO(PCT) 占 "
                f"{pct(dict(country).get('WO', 0), total_pat)}%，其余四码合计不足 0.04%。"
                f"按链聚合后，12 条链里 {sum(1 for m in matrix if m['n_regions_covered'] == 2)} 条只覆盖 2 个区域（CN + WO），"
                f"仅传感器链因 1 家企业有日本专利而达到 3 个，剔除 WO 后 11 条链的境外区域数为 0，"
                f"既不能给出企业/机构的国家分布，也没有任何区分度，故判完全不支持。"
            ),
            "criteria": {"patent_rows": total_pat, "distinct_country_codes": len(country),
                         "chains": len(CHAIN_AXIS), "n_regions_distribution": n_region_dist,
                         "chains_with_gt2_regions": sum(1 for m in matrix if m["n_regions_covered"] > 2)},
        },
        "notes": [
            "WO 是 WIPO/PCT 国际申请通道，不是国家；把它当作一个「区域」会把专利布局口径和国家口径混为一谈。",
            "HK/MO/TW 的件数只有全局值（952 / 4 / 20），没有按申请人的分布，无法分摊到链，故链级只列 CN/WO/JP。",
            "链级 CN 件数是「该链企业全部专利行 − PCT − 日本」的推算值，含少量港澳台，属上界。",
            "「覆盖区域数」全为 2 是数据结构的必然结果，不是产业事实；不得用于排名或趋势。",
            "若甲方需要该指标，最小补数是「企业/机构国别字段」或「链上企业境外分支表」，两者在 gkx 均无承载。",
        ],
        "elapsed_sec": round(time.time() - t0, 2),
    }
    write_out(MID, payload)
    print("country", payload["country_total"])
    print("regions", n_region_dist, "pct firms",
          payload["probes"]["firms_with_pct"], "/", payload["probes"]["chain_firms"])
    print("matrix head", [(m["chain"], m["pct_firms"], m["n_regions_covered"]) for m in matrix[:4]])


if __name__ == "__main__":
    main()
