#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_TECH_POWER · 技术能力（链技术力）（gkx 单库代理版）

王惠三维框架（旧稿沿用）
------------------------
技术力 = (D1 专利规模 + D2 断链壁垒 + D3 成熟度) / 3，等权，min-max 归一到 0—1。
  D1 专利规模：链内企业专利总量取 log 后 min-max
  D2 断链壁垒：1 − K 节点覆盖率（关键环节无人覆盖 = 技术空白）
  D3 成熟度：近一年（2024）申请量 / 全期申请量（专利存量的「新鲜度」）

数据事实
--------
`tech_power` 结果面在 gkx 不存在（source_absent，见 TABLE_ABSENCE_EVIDENCE §tech_power）。
D1/D3 用 `dwd_patent`（2,939,895 行，2021—2026 窗口）按申请人名聚合的落盘快照；
D2 用 `dwd_org_industry_tags` × `dwd_industry_chain_info` 的深圳 K 覆盖快照。
D2 只有深圳口径（全国 K 覆盖没有落盘），已在 proxy_deviation 披露。

输出：code/M_CHAIN_TECH_POWER_out.json
"""
from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_CHAIN_TECH_POWER_out.json"
METRIC = "M_CHAIN_TECH_POWER"


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def minmax(vals):
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return [0.5 for _ in vals]
    return [(v - lo) / (hi - lo) for v in vals]


def main() -> None:
    name2chain = load("chain21_layer_20261022.json")["names"]
    roots = {c["chain"]: c["name"] for c in load("chain_panel21.json")["chains"]}

    pat = defaultdict(int)
    ipc = defaultdict(set)
    for ipc4, name, c in load("patent_ipc4_by_name_20261021.json"):
        ch = name2chain.get(name)
        if not ch:
            continue
        pat[ch] += c
        ipc[ch].add(ipc4)

    p24 = load("patent_2024_by_name_20261021.json")
    apply24 = defaultdict(int)
    for name, v in p24.items():
        ch = name2chain.get(name)
        if ch and isinstance(v, list) and v:
            apply24[ch] += int(v[0])

    cov = load("chain21_sz_nodecov_20261022.json")["chains"]

    base = []
    for code in sorted(roots):
        k = cov.get(code, {})
        k_nodes = k.get("K_nodes", 0)
        k_cov = k.get("k_covered", 0)
        gap = round(1 - k_cov / k_nodes, 4) if k_nodes else None
        base.append({
            "chain": code, "chain_name": roots[code],
            "patents": pat.get(code, 0), "ipc4_breadth": len(ipc.get(code, ())),
            "patents_2024_apply": apply24.get(code, 0),
            "recency": round(apply24.get(code, 0) / pat[code], 4) if pat.get(code) else None,
            "k_nodes": k_nodes, "k_covered": k_cov, "uncov_share": gap,
        })

    d1 = minmax([math.log1p(r["patents"]) for r in base])
    d2 = [r["uncov_share"] if r["uncov_share"] is not None else 0.0 for r in base]
    d3 = minmax([r["recency"] if r["recency"] is not None else 0.0 for r in base])
    for i, r in enumerate(base):
        r["d1_patent_scale"] = round(d1[i], 4)
        r["d2_barrier"] = round(d2[i], 4)
        r["d3_recency"] = round(d3[i], 4)
        r["tech_power"] = round((d1[i] + d2[i] + d3[i]) / 3, 4)
    base.sort(key=lambda r: -r["tech_power"])
    for i, r in enumerate(base, 1):
        r["rank"] = i

    total_pat = sum(r["patents"] for r in base)
    out = {
        "metric_id": METRIC,
        "metric_name": "技术能力（链技术力）",
        "data_source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）+ code/_snapshots21/ 落盘快照",
        "formula": "tech_power = (D1专利规模 + D2断链壁垒 + D3近一年申请占比) / 3，各维 min-max 归一",
        "blocking_tables": {
            "tech_power": {
                "triage": "source_absent",
                "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §tech_power",
            }
        },
        "proxy_path": "dwd_patent 按申请人名聚合（D1/D3）+ 深圳 K 节点覆盖（D2）",
        "proxy_deviation": "D2 只有深圳口径的 K 覆盖（全国环节覆盖未落盘），12 链的壁垒分实际是「深圳缺环率」；D1/D3 只统计能按名挂链的企业（36,993/189,116），链内专利总量是下限",
        "weights": {"d1": 1 / 3, "d2": 1 / 3, "d3": 1 / 3,
                    "note": "等权为项目默认值，甲方未裁定权重"},
        "totals": {"patents_12_chains": total_pat, "patent_table_rows": 2939895,
                   "chains": len(base), "equal_weight": True},
        "chains": base,
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": "tech_power 结果面不存在，但三维里有二维半可用：专利规模与近一年申请占比都能从 dwd_patent 的 2,939,895 行按申请人名聚合出来（12 链合计专利见 totals），断链壁垒可以用 K 节点未覆盖率算，但只有深圳口径。权重是等权默认值、甲方未裁定。结构与数据都够跑，缺的是全国 K 覆盖与官方权重，判部分支持。",
            "criteria": {
                "result_table_exists": False,
                "dims_total": 3,
                "dims_full": 2,
                "dims_partial": 1,
                "patent_rows": 2939895,
                "proxy_used": True,
            },
        },
        "base_years_used": [2021, 2022, 2023, 2024],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": "专利表 apdt_year 只有 2021—2026，2017—2020 零行（DATA_FACTS 陷阱 3.13），所以「近一年占比」的分母是 2021—2024 全期申请，不是十年存量；2025/2026 为不完整年，不进分母。",
        "sources": [
            {"path": "code/_snapshots21/patent_ipc4_by_name_20261021.json",
             "table": "gkx.dwd_patent", "rows": 581585,
             "role": "企业×IPC4 专利计数（D1 与 IPC 广度）"},
            {"path": "code/_snapshots21/patent_2024_by_name_20261021.json",
             "table": "gkx.dwd_patent", "rows": 60009,
             "role": "企业 2024 申请/授权（D3 新鲜度）"},
            {"path": "code/_snapshots21/chain21_sz_nodecov_20261022.json",
             "table": "gkx.dwd_org_industry_tags × gkx.dwd_industry_chain_info",
             "rows": 116017, "role": "深圳 K 节点覆盖（D2）"},
            {"path": "code/_snapshots21/chain21_layer_20261022.json",
             "table": "gkx.dwd_org_industry_tags", "rows": 36993,
             "role": "企业名→链映射"},
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[OK] {METRIC} -> {OUT.name} total_pat={total_pat}")
    for r in base:
        print(f"  #{r['rank']:<2} {r['chain']} {r['chain_name'][:8]:<8} pat={r['patents']:<7} "
              f"ipc={r['ipc4_breadth']:<3} rec={r['recency']} uncov={r['uncov_share']} "
              f"-> {r['tech_power']}")


if __name__ == "__main__":
    main()
