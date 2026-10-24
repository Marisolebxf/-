#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_CHAIN_STAGE_COVERAGE 产业链环节覆盖（企业上链环节覆盖广度）。

口径（calc-logic ENT，王惠 20260816 底稿的降级实现）：
    王惠原式：`dwd_org_industry_tags` 关联 `dwd_industry_chain_info`
    **按 level 分组（上游/中游/下游）**，COUNT(DISTINCT industry_link_code)。
    当前目录 `level` 全为 0、无上/中/下游命名行 → 段位分组不可执行。
    本脚本输出三组可复现结果：
      A. 目录侧环节覆盖：链目录叶子节点中被企业实际驻扎的比例（k/K）；
      B. 企业侧覆盖广度：每家企业驻扎的链环节数（叶子码去重）；
      C. 码深代理分箱：按环节码长度切浅/中/深三档（**分类学深度，不是业务段位**）。

取数（全部离线，零 SQL）：
    `_snapshots21/chain_stage_leaf_20261021.json` —— 228 万行标签的 keyset 全表聚合
        （按链 / 链×城 去重叶子集合、每叶子企业数、每档企业数）
    `_snapshots21/chain_tree_20261021.json`       —— 链目录 1,273 节点（954 叶子）

产物：code/M_ENT_CHAIN_STAGE_COVERAGE_out.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

BASE = Path(__file__).parent
SNAP = BASE / "_snapshots21"
OUT = BASE / "M_ENT_CHAIN_STAGE_COVERAGE_out.json"
METRIC = "M_ENT_CHAIN_STAGE_COVERAGE"
CITY4 = ["深圳市", "广州市", "东莞市", "惠州市"]


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def band(code: str) -> str:
    n = len(code)
    return "shallow" if n <= 9 else ("medium" if n <= 13 else "deep")


def main():
    t0 = time.time()
    panel = load("chain_stage_leaf_20261021.json")
    tree = load("chain_tree_20261021.json")

    nodes = {n["industry_code"]: n for n in tree}
    codes = set(nodes)
    leaves = {c for c in codes if not any(o != c and o.startswith(c) for o in codes)}
    chain_name, chain_leaves = {}, {}
    for c in leaves:
        ch = c[:7]
        chain_leaves.setdefault(ch, set()).add(c)
        chain_name[ch] = nodes[ch]["industry_name"] if ch in nodes else ch

    leaf_firm = panel["leaf_firm_counts"]
    cell_leaf = panel["cell_leaf_firm_counts"]
    cell_firm = panel["cell_firm_counts"]
    band_rows = panel["band_row_counts"]

    # ---------------------------------------------------------------- A 目录覆盖
    chain_rows, tot_k = [], {"k": 0, "k4": 0, "kn": 0}
    for ch in sorted(chain_leaves, key=lambda x: chain_name[x]):
        K = chain_leaves[ch]
        cov_all = set(leaf_firm.get(ch, {}))
        cov_in = cov_all & K
        cov4 = set()
        for city in CITY4:
            cov4 |= set(cell_leaf.get(f"{ch}|{city}", {})) & K
        outside = cov_all - K
        row = {
            "chain": ch, "chain_name": chain_name[ch],
            "K_catalog_leaves": len(K),
            "k_covered_national": len(cov_in),
            "coverage_pct_national": round(100.0 * len(cov_in) / len(K), 2),
            "k_covered_city4": len(cov4),
            "coverage_pct_city4": round(100.0 * len(cov4) / len(K), 2),
            "codes_outside_catalog": len(outside),
            "firms_national": panel["chain_firm_counts"].get(ch, 0),
            "firms_city4": sum(cell_firm.get(f"{ch}|{c}", 0) for c in CITY4),
        }
        chain_rows.append(row)
        tot_k["k"] += len(K)
        tot_k["k4"] += len(cov4)
        tot_k["kn"] += len(cov_in)

    # ---------------------------------------------------------------- B 企业广度
    breadth = []
    for ch in chain_leaves:
        d = leaf_firm.get(ch, {})
        n_firms = panel["chain_firm_counts"].get(ch, 0)
        n_leaves = sum(d.values())
        breadth.append({
            "chain": ch, "chain_name": chain_name[ch],
            "firms": n_firms, "leaf_links": n_leaves,
            "mean_leaves_per_firm": round(n_leaves / n_firms, 3) if n_firms else None,
            "max_leaf_firm_count": max(d.values()) if d else 0,
        })

    # 每家企业叶子数分布（全表，来自 v1 面板 hist 不可用 → 用链加权近似：
    # 这里用 cell 行数与企业数的比，只作量级参考，不冒充逐企业分布）
    cell_rows = []
    band_leaf_tot = {"shallow": 0, "medium": 0, "deep": 0}
    for ch in sorted(chain_leaves, key=lambda x: chain_name[x]):
        for city in CITY4:
            ck = f"{ch}|{city}"
            nf = cell_firm.get(ck, 0)
            if not nf:
                continue
            K = chain_leaves[ch]
            cov = set(cell_leaf.get(ck, {}))
            br = band_rows.get(ck, {"shallow": 0, "medium": 0, "deep": 0})
            cell_rows.append({
                "chain": ch, "chain_name": chain_name[ch], "city": city,
                "firms": nf,
                "leaves_covered_in_catalog": len(cov & K),
                "coverage_pct": round(100.0 * len(cov & K) / len(K), 2),
                "leaves_covered_total": len(cov),
                "mean_leaves_per_firm": round(sum(cell_leaf[ck].values()) / nf, 3),
                "firms_shallow": br["shallow"], "firms_medium": br["medium"],
                "firms_deep": br["deep"],
            })
            for b in band_leaf_tot:
                band_leaf_tot[b] += br[b]

    # ---------------------------------------------------------------- C 段位代理
    stage_proxy = {
        "available": False,
        "reason": ("`dwd_industry_chain_info.level` 全库 1,273/1,273 行为 0，"
                   "无『上游/中游/下游』命名行；段位分组不可执行。"),
        "proxy_rule": "按环节码长度三分：≤9 浅、11—13 中、≥15 深（分类学深度，非业务段位）",
        "catalog_leaf_by_band": {
            b: sum(1 for c in leaves if band(c) == b) for b in ("shallow", "medium", "deep")
        },
        "firm_rows_by_band": band_leaf_tot,
        "warning": "代理分箱不得对外表述为上游/中游/下游，不得用于补链决策。",
    }

    # ---------------------------------------------------------------- 判档
    total_city4_rows = sum(cell_firm.get(f"{ch}|{c}", 0)
                           for ch in chain_leaves for c in CITY4)
    support = {
        "data_support_level": "部分支持",
        "criteria": {
            "stage_field_usable": False,
            "catalog_leaf_coverage_computable": True,
            "enterprise_breadth_computable": True,
            "city_attribution_reliable": "credit_code 行政区划码（登记地）",
            "empty_link_code_pct": round(100.0 * panel["empty_rows"] / panel["rows_seen"], 2),
        },
        "reason": (
            f"目录侧 {len(leaves)} 个叶子节点、{len(codes)} 个节点可用于覆盖率，"
            f"企业侧 {panel['rows_seen']:,} 行标签中 {panel['empty_rows']:,} 行"
            f"（{100.0*panel['empty_rows']/panel['rows_seen']:.2f}%）`industry_link_code` 为空、"
            f"无法定位环节，可算行 {total_city4_rows:,}（四城）。"
            "但王惠原式要求的『上游/中游/下游』段位字段 `level` 全为 0、命名行 0 条，"
            "段位维整块缺失；另发现标签体系使用 {0:,} 个目录外环节码，目录（1,273 节点）"
            "只是企业实际使用分类的一小部分，k/K 只能读作『目录口径覆盖率』，"
            "不能读作『真实产业链覆盖率』。故判部分支持。".format(
                sum(r["codes_outside_catalog"] for r in chain_rows))
        ),
        "upgrade_path": [
            "供应方为 dwd_industry_chain_info 补 level / stage 字段（上/中/下游），或按工信部图谱重排目录",
            "对齐企业标签分类与本项目链目录（当前目录外环节码 5,674 个），否则 k/K 分母失真",
            "补 industry_link_code 为空的 56.9 万行（24.93%），否则环节覆盖系统性低估",
            "企业侧补 credit_code 以外的主体标识，使标签全集能与底册对齐（当前两库几乎不相交）",
        ],
    }

    out = {
        "metric_id": METRIC,
        "metric_name": "产业链环节覆盖",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_sec": round(time.time() - t0, 2),
        "support_judgment": support,
        "definition": {
            "unit": "% / 个环节",
            "formula_catalog": "k_K = |被企业驻扎的目录叶子 ∩ 链目录叶子| / |链目录叶子|",
            "formula_breadth": "breadth = Σ叶子关联数 / 企业数",
            "stage_grouping": "原式按 level 上/中/下游；当前不可执行，仅给码深代理",
        },
        "panel": {
            "tag_rows": panel["rows_seen"],
            "empty_link_code_rows": panel["empty_rows"],
            "multi_leaf_rows": panel["multi_leaf_rows"],
            "bad_chain_rows": panel["bad_chain_rows"],
            "credit_city_totals": panel["credit_city_totals"],
            "catalog_nodes": len(codes), "catalog_leaves": len(leaves),
            "distinct_codes_in_tags": len(leaves) + sum(r["codes_outside_catalog"] for r in chain_rows),
        },
        "totals": {
            "K_catalog_leaves": tot_k["k"],
            "k_covered_national": tot_k["kn"],
            "coverage_pct_national": round(100.0 * tot_k["kn"] / tot_k["k"], 2),
            "k_covered_city4": tot_k["k4"],
            "coverage_pct_city4": round(100.0 * tot_k["k4"] / tot_k["k"], 2),
            "firms_city4_rows": total_city4_rows,
        },
        "chains": chain_rows,
        "breadth": breadth,
        "cells": sorted(cell_rows, key=lambda r: (r["chain_name"], r["city"])),
        "stage_proxy": stage_proxy,
        "notes": [
            "城市归属取 credit_code 第 3—6 位行政区划码（4401/4403/4419/4413），是登记地，不是经营地。",
            "标签全集（广东段 350,156 个 credit_code）与底册 189,115 行几乎不相交，"
            "禁止把本指标的企业数与 M_ENT_INNOVATIVE_COUNT 等底册口径相加或互校。",
            "目录外环节码 5,674 个说明企业标签用的是更大分类体系；k/K 的分母是链目录，不是真实分类全集。",
            "`level` 全 0 是目录数据缺陷，不是查询问题：换任何 SQL 写法都拿不到上/中/下游。",
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(out["totals"], ensure_ascii=False, indent=1))
    print("support:", support["data_support_level"], "| elapsed", out["elapsed_sec"], "s")
    for r in chain_rows:
        print(f"{r['chain_name']:<12} K={r['K_catalog_leaves']:>4} k4={r['k_covered_city4']:>4} "
              f"city4={r['coverage_pct_city4']:>6}% firms4={r['firms_city4']:>7}")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
