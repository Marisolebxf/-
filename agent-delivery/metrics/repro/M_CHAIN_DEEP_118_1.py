#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_DEEP_118_1 · 深圳产业链模型构建（gkx 单库代理版）

要建的东西（需求原意）
----------------------
把 12 条顶层产业链各自切出「深圳切片」：链内深圳企业清单与规模、链上关键环节
（K 节点）在深圳的覆盖情况、深圳高校与科研院所的落位。输出是链×深圳的一张表，
供产业链分析页的深圳视图消费。

数据事实
--------
`chain_sz_dist` / `chain_sz_elements` / `chain_sz_panorama` 三张结果面在 gkx 都不存在
（source_absent，见 TABLE_ABSENCE_EVIDENCE 对应三节）。可用的是四张原始表：
  - `dwd_org_industry_tags` × `dwd_org_base_info`（city 过滤）→ 深圳企业在链内的分布
  - `dwd_industry_chain_info`（1,273 节点树）→ 关键环节集合 K
  - `dwd_org_heis_info`（3,501 行）→ 深圳高校
  - `dwd_research_institute_base_info`（2,074 行）→ 深圳院所
K 节点覆盖靠企业名 token 命中环节名，属于弱归属，已在 proxy_deviation 披露。

输出：code/M_CHAIN_DEEP_118_1_out.json
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_CHAIN_DEEP_118_1_out.json"
METRIC = "M_CHAIN_DEEP_118_1"


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def main() -> None:
    layer = load("chain21_layer_20261022.json")
    sz_by_chain = defaultdict(int)
    for k, n in layer["chain_city"].items():
        code, city = k.split("|")
        if city.startswith("深圳"):
            sz_by_chain[code] += n

    roots = {c["chain"]: c["name"] for c in load("chain_panel21.json")["chains"]}
    cov = load("chain21_sz_nodecov_20261022.json")
    inst = load("inst_base_gkx21.json")["rows"]
    heis = load("heis21_20261022.json")["rows"]

    inst_sz = [r for r in inst if str(r[1]).startswith("深圳")]
    heis_sz = [r for r in heis if str(r[2]).startswith("深圳")]

    chain_rows = []
    for code in sorted(roots):
        c = cov["chains"].get(code, {})
        chain_rows.append({
            "chain": code, "chain_name": roots[code],
            "sz_orgs": sz_by_chain.get(code, 0),
            "k_nodes": c.get("K_nodes", 0),
            "k_covered": c.get("k_covered", 0),
            "k_leaf": c.get("K_leaf", 0),
            "k_leaf_covered": c.get("k_leaf_covered", 0),
            "k_coverage_rate": round(c.get("k_covered", 0) / c["K_nodes"], 4) if c.get("K_nodes") else None,
        })

    total_sz = sum(r["sz_orgs"] for r in chain_rows)
    total_k = sum(r["k_nodes"] for r in chain_rows)
    total_kc = sum(r["k_covered"] for r in chain_rows)

    out = {
        "metric_id": METRIC,
        "metric_name": "深圳产业链模型构建",
        "data_source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）+ code/_snapshots21/ 落盘快照",
        "formula": "深圳切片 = 链内企业 ∩ city like '深圳%'；K 节点覆盖 = 深圳企业名 token 命中环节名；载体 = 深圳高校/院所计数",
        "blocking_tables": {
            "chain_sz_dist": {"triage": "source_absent",
                              "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §chain_sz_dist"},
            "chain_sz_elements": {"triage": "source_absent",
                                  "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §chain_sz_elements"},
            "chain_sz_panorama": {"triage": "source_absent",
                                  "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §chain_sz_panorama"},
        },
        "proxy_path": "企业标签表按 city 切片 + 环节名 token 命中做 K 节点覆盖 + 高校/院所按 city 计数",
        "proxy_deviation": "企业→链靠 dwd_org_industry_tags（多标签，131,978 行一行多链，链内合计会大于企业数）；K 覆盖靠企业名含环节名，命中率低（全库 1,056 个环节 token 覆盖 116,017 行深圳标签），只说明「有企业名提到该环节」，不等于该企业在该环节有产出",
        "sz_totals": {
            "sz_tag_rows": cov["rows_sz"], "sz_orgs_in_12_chains": total_sz,
            "k_nodes_total": total_k, "k_covered_total": total_kc,
            "k_coverage_rate": round(total_kc / total_k, 4) if total_k else None,
            "sz_universities": len(heis_sz), "sz_institutes": len(inst_sz),
            "distinct_leaf_tokens": cov["distinct_tokens"],
        },
        "chains": chain_rows,
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": "三张深圳切片结果面都不存在，但切片所需的四类原料在 gkx 齐备且量足：深圳标签行 116,017、12 链深圳企业可逐链汇总、K 节点树 1,273 节点且已有 coverage 计算（90/90 等）、深圳高校与院所可按 city 直接数出。切片是可现在加工的，故不判完全不支持；但链归属靠多标签表、K 覆盖靠企业名 token，两项都是弱归属，切片只能作「分布画像」不能作「环节强度」结论，故判部分支持。",
            "criteria": {
                "result_tables": 3, "result_tables_present": 0,
                "raw_tables_present": 4, "sz_tag_rows": cov["rows_sz"],
                "k_nodes_total": total_k, "proxy_used": True,
            },
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "本件是截面切片（当前时点的企业/载体分布），不做年度序列，故无基期年份；标签表与底册均为当前快照，不含历史版本，无法回溯往年切片。",
        "sources": [
            {"path": "code/_snapshots21/chain21_layer_20261022.json",
             "table": "gkx.dwd_org_industry_tags", "rows": 2283762,
             "role": "链×城市分布（深圳切片分子）"},
            {"path": "code/_snapshots21/chain21_sz_nodecov_20261022.json",
             "table": "gkx.dwd_org_industry_tags × gkx.dwd_industry_chain_info",
             "rows": 116017, "role": "深圳 K 节点覆盖"},
            {"path": "code/_snapshots21/inst_base_gkx21.json",
             "table": "gkx.dwd_research_institute_base_info", "rows": 2074,
             "role": "科研院所落位"},
            {"path": "code/_snapshots21/heis21_20261022.json",
             "table": "gkx.dwd_org_heis_info", "rows": 3501,
             "role": "高校落位"},
            {"path": "code/_snapshots21/chain_panel21.json",
             "table": "gkx.dwd_industry_chain_info", "rows": 12,
             "role": "链名与节点规模"},
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[OK] {METRIC} -> {OUT.name}  total_sz={total_sz} K={total_kc}/{total_k} "
          f"univ={len(heis_sz)} inst={len(inst_sz)}")
    for r in chain_rows:
        print(f"  {r['chain']} {r['chain_name'][:8]:<8} sz={r['sz_orgs']:<7} "
              f"K={r['k_covered']}/{r['k_nodes']} leaf={r['k_leaf_covered']}/{r['k_leaf']}")


if __name__ == "__main__":
    main()
