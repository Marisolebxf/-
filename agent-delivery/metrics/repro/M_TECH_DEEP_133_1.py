#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_TECH_DEEP_133_1 深圳细分领域分布模型 —— 离线复算（gkx 授权缓存，零 SQL）。

输出：领域覆盖率、集中度（HHI）、Top 领域、区级分布矩阵、产业链承接面。
数据：patent_scan_20261021.pkl（四城×年×IPC4）、patent_ipc4_by_name、
      sz_patent_city_name_gkx、innov_base_20261021（名称→区）、bridge/chain_tree。
判档：先实测后定档；预测维无「域×行业×年」面板，如实写入缺口。
"""
from __future__ import annotations

import collections

import _tech21_common as C

M = "M_TECH_DEEP_133_1"
WINDOW = C.COMPLETE_YEARS

city_ipc, city_meta = C.load_city_ipc()
sz_year = collections.Counter()
sz_dom_year = collections.defaultdict(collections.Counter)
for (city, year), cnt in city_ipc.items():
    if city != "深圳" or year not in WINDOW:
        continue
    sz_year[year] = sum(cnt.values())
    for ipc4, n in cnt.items():
        sz_dom_year[ipc4][year] += n

domains = sorted(sz_dom_year)
dom_total = {d: sum(sz_dom_year[d].values()) for d in domains}
sz_all = sum(dom_total.values())
hhi_by_year = {y: C.hhi(collections.Counter({d: sz_dom_year[d][y] for d in domains})) for y in WINDOW}
hhi_all = C.hhi(collections.Counter(dom_total))

top = sorted(domains, key=lambda d: -dom_total[d])[:20]
top_rows = [{
    "ipc4": d,
    "label": C.label(d),
    "assignments_2021_2024": dom_total[d],
    "share_pct": C.pct(dom_total[d] / sz_all),
    "n2021": sz_dom_year[d][2021],
    "n2024": sz_dom_year[d][2024],
    "growth_21_24_pct": C.pct((sz_dom_year[d][2024] - sz_dom_year[d][2021]) / sz_dom_year[d][2021])
    if sz_dom_year[d][2021] else None,
} for d in top]

# 20+8 覆盖率（2021—2024 深圳是否存在该产业任一 IPC 前缀）
cov = {}
for ind, prefixes in C.SZ208_MAP.items():
    n = sum(dom_total[d] for d in domains if any(d.startswith(p) for p in prefixes))
    cov[ind] = n
covered = [k for k, v in cov.items() if v > 0]

# 区级矩阵：全期截面（名称→区），并披露窗口与覆盖
area_of, area_meta = C.load_sz_area()
ipc_name = C.load_ipc_name()
district_tot = collections.Counter()
district_dom = collections.Counter()
matched = 0
for ipc4, nm, n in ipc_name:
    a = area_of.get(nm)
    if not a:
        continue
    matched += n
    district_tot[a] += n
    if ipc4 in top:
        district_dom[(ipc4, a)] += n

sz_names, sz_counts, sz_inv, sz_ipc_empty = C.load_sz_names()
sz_patents_all = sum(sz_counts.values())
sz_patents_ipc = sz_patents_all - sum(sz_ipc_empty.values())
district_rows = []
for d in top[:10]:
    row = {"ipc4": d, "label": C.label(d), "all_years_total": dom_total[d]}
    for a, _ in district_tot.most_common():
        row[a] = district_dom.get((d, a), 0)
    district_rows.append(row)

# 产业承接面：bridge 的深圳企业 → 链（12 链）
bridge, code2name, bridge_meta = C.load_bridge_and_tree()
chain_firm = collections.Counter()
sz_firms = set()
for r in bridge:
    if r.get("c") != "深圳市":
        continue
    sz_firms.add(r.get("nm"))
    for code in r.get("chains", []):
        chain_firm[code2name.get(code, code)] += 1
chain_rows = [{"chain": k, "firms": v} for k, v in chain_firm.most_common(12)]

# 机构技术标签（org_id 挂接底册；只读 tech_tags_20261021.json）
tag_raw = C._load(C.SNAP / "tech_tags_20261021.json")
base_rows = C._load(C.SNAP / "base_20261021.json")
sz_org_ids = {r[0] for r in base_rows if r[4] == "深圳市"}
tag_counter = collections.Counter()
tagged = 0
for oid, tags in tag_raw.items():
    if oid in sz_org_ids:
        tagged += 1
        for t in tags:
            tag_counter[t] += 1
TECH_TAG = {"n": tagged, "top": tag_counter.most_common(15)}

# 描述性趋势（替代 ML 预测）：HHI 与第一大域份额
first_share = {}
for y in WINDOW:
    c = collections.Counter({d: sz_dom_year[d][y] for d in domains})
    first_share[y] = C.pct(max(c.values()) / sum(c.values())) if c else 0

payload = {
    "metric_id": M,
    "generated_at": "2026-10-22",
    "params": {
        "city": "深圳市",
        "time_axis": "apdt_year（申请年）",
        "window": WINDOW,
        "ipc_granularity": "IPC4（主分类前 4 位）",
        "district_window": "缓存全期截面（patent_ipc4_by_name 未按年拆分）",
        "base_years_used": WINDOW,
        "base_years_missing": C.MISSING_BASE_YEARS,
        "excluded_years": [2025, 2026],
        "excluded_reason": "2025 年仅 440,401 件、2026 年仅 74,810 件（采集残年），不进入完整年比较",
    },
    "sources": {
        "city_ipc": city_meta,
        "ipc_by_name": "code/_snapshots21/patent_ipc4_by_name_20261021.json（2,420,915 件有 IPC）",
        "sz_names": "code/_snapshots_gkx21/sz_patent_city_name_gkx.json（168,827 组，深圳 77,846 组）",
        "area": "code/_snapshots21/innov_base_20261021.json（深圳 95,600 家，名称→区）",
        "chain": "code/_snapshots21/bridge_20261021.json × chain_tree_20261021.json（35,046 家 → 1,273 节点）",
    },
    "sz_ipc_assignments_by_year": {str(y): sz_year[y] for y in WINDOW},
    "sz_ipc_assignments_total": sz_all,
    "sz_domain_union": len(domains),
    "concentration": {
        "hhi_by_year": {str(k): v for k, v in hhi_by_year.items()},
        "hhi_2021_2024_pooled": hhi_all,
        "first_domain_share_pct_by_year": {str(k): v for k, v in first_share.items()},
        "hhi_delta_2021_to_2024": round(hhi_by_year[2024] - hhi_by_year[2021], 2),
    },
    "top_domains": top_rows,
    "coverage_20_8": {
        "n_total": len(C.SZ208_MAP),
        "n_covered": len(covered),
        "covered": sorted(covered),
        "by_industry_assignments": dict(sorted(cov.items(), key=lambda x: -x[1])),
    },
    "district": {
        "matched_assignments": matched,
        "sz_patents_all_years": sz_patents_all,
        "sz_patents_with_ipc_all_years": sz_patents_ipc,
        "coverage_of_all_patents_pct": round(matched / sz_patents_all * 100, 3),
        "coverage_of_ipc_patents_pct": round(matched / sz_patents_ipc * 100, 3),
        "district_totals": dict(district_tot.most_common()),
        "top10_matrix": district_rows,
        "ambiguous_names": area_meta["ambiguous_names"],
        "caveat": "区级用申请人名精确匹配底册 area；同名多区已剔除（实测 0 例）。窗口为缓存全期，与 2021—2024 分布窗口不完全一致。",
    },
    "tech_tag_base": {
        "tagged_firms": TECH_TAG["n"],
        "top_tags": TECH_TAG["top"],
        "note": "tech_tags 以 org_id 挂接底册；只覆盖有资质的 18,090 家，不是深圳企业全量。",
    },
    "industry_base": {
        "sz_chain_tagged_firms": len(sz_firms),
        "sz_chain_memberships": sum(chain_firm.values()),
        "n_chains": len(chain_firm),
        "chains": chain_rows,
        "caveat": "bridge 只覆盖有链标签的 35,046 家（深圳 19,909 家），不是深圳企业全量 95,600 家。",
    },
    "prediction": {
        "ml_feasible": False,
        "blocker": "需求要求「域×行业×年」历史特征面板训练覆盖率/集中度预测；库内企业主档为当前截面、专利无行业直连标签，面板键不可构。",
        "delivered_instead": "HHI 与第一大域份额的 2021—2024 四点描述序列（非 ML 预测）",
    },
    "base_years_used": WINDOW,
    "base_years_missing": C.MISSING_BASE_YEARS,
}

crit = {
    "coverage_20_8": f"{len(covered)}/{len(C.SZ208_MAP)}",
    "hhi_2021_2024": hhi_all,
    "sz_ipc_assignments": sz_all,
    "sz_domain_union": len(domains),
    "district_coverage_of_ipc_patents_pct": round(matched / sz_patents_ipc * 100, 3),
    "chain_tagged_sz_firms": len(sz_firms),
    "ml_prediction": False,
}
payload["support_judgment"] = {
    "data_support_level": "部分支持",
    "criteria": crit,
    "reason": (
        f"深圳 2021—2024 年 IPC4 分布 {sz_all:,} 件、{len(domains)} 个域、20+8 覆盖 {len(covered)}/{len(C.SZ208_MAP)}、"
        f"HHI {hhi_all} 均可复算；区级矩阵覆盖有 IPC 专利的 {round(matched / sz_patents_ipc * 100, 3)}%、产业链承接面 {len(sz_firms):,} 家可交付。"
        "但需求点名的「机器学习预测领域覆盖率与集中度」缺「域×行业×年」特征面板，只能降级为四点描述序列，"
        "故按四档口径判部分支持，不抬档。"
    ),
}

C.write_out(M, payload)
