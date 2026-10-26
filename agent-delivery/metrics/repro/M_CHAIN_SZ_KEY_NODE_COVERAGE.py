#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_SZ_KEY_NODE_COVERAGE 深圳关键环节覆盖率（W13-C1）。

只读 code/_snapshots21/ 下的落盘快照，零 SQL、零本地 helper：
  - chain_tree_20261021.json            链树 1,273 节点 / 954 叶 / 12 顶层链
  - chain_stage_leaf_20261021.json      叶级「全国企业家数」与「深圳市企业家数」
  - chain21_sz_nodecov_20261022.json    深圳节点覆盖（全节点口径 + 前缀口径）
  - chain_firm_index_20261023.json      12 链企业数、L1 企业数、链名
  - chain21_layer_20261022.json         12 链深圳挂接次数（4403 口径）

口径：
  1) 树侧：parent = 去掉末 2 位的定长分段，叶 = 无子节点的非根码（954）。
  2) 关键：逐链取「有企业叶级环节」全国企业家数的中位数，
     n_national >= median 记为关键（与已交付 M_CHAIN_KEY_NODE_COUNT /
     M_CHAIN_SZ_KEY_NODE_COUNT 同一套门槛，463 / 411 逐位可对）。
  3) 覆盖：关键叶中至少 1 家深圳企业（credit_code[2:6]='4403'）。
  分子分母同源（同一棵树的同一批叶），不与链企业数相除（§3.54 陷阱）。
"""
from __future__ import annotations

import json
import os
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as fh:
        return json.load(fh)


def tree_index(tree):
    codes = {n["industry_code"] for n in tree}
    roots = sorted(n["industry_code"] for n in tree if len(n["industry_code"]) == 7)
    has_child = {c[:-2] for c in codes if len(c) > 7 and c[:-2] in codes}
    leaves = sorted(c for c in codes if c not in has_child and c not in roots)
    l1 = sorted(c for c in codes if len(c) == 9)
    return codes, roots, leaves, l1


def main() -> None:
    tree = load("chain_tree_20261021.json")
    stage = load("chain_stage_leaf_20261021.json")
    nodecov = load("chain21_sz_nodecov_20261022.json")
    findex = load("chain_firm_index_20261023.json")
    layer = load("chain21_layer_20261022.json")
    probe = load("chain_live_result_probe_20261023.json")
    codes, roots, leaves, l1 = tree_index(tree)
    names = findex["chain_name"]

    by_chain = {r: [c for c in leaves if c[:7] == r] for r in roots}
    rows = []
    key_total = key_cov = leaf_total = leaf_nat = leaf_sz = 0
    for ch in roots:
        ls = by_chain[ch]
        nat_map = stage["leaf_firm_counts"].get(ch, {})
        sz_map = stage["cell_leaf_firm_counts"].get(ch + "|深圳市", {})
        nat = [nat_map.get(c, 0) for c in ls]
        positive = [x for x in nat if x > 0]
        median = statistics.median(positive)
        key = [c for c in ls if nat_map.get(c, 0) > 0 and nat_map.get(c, 0) >= median]
        key_hit = [c for c in key if sz_map.get(c, 0) > 0]
        nat_hit = [c for c in ls if nat_map.get(c, 0) > 0]
        sz_hit = [c for c in ls if sz_map.get(c, 0) > 0]
        nc = nodecov["chains"][ch]
        rows.append({
            "chain_code": ch,
            "chain_name": names[ch],
            "leaves": len(ls),
            "leaves_with_national_firms": len(nat_hit),
            "leaves_with_sz_firms": len(sz_hit),
            "leaf_coverage_pct": round(100.0 * len(sz_hit) / len(ls), 2),
            "median_threshold": median,
            "key_leaves": len(key),
            "key_leaves_covered_sz": len(key_hit),
            "key_coverage_pct": round(100.0 * len(key_hit) / len(key), 2),
            "key_gap": len(key) - len(key_hit),
            "nodecov_K_nodes": nc["K_nodes"],
            "nodecov_k_covered": nc["k_covered"],
            "nodecov_K_leaf": nc["K_leaf"],
            "nodecov_k_leaf_covered": nc["k_leaf_covered"],
            "sz_memberships_4403": layer["chain_city"].get(ch + "|深圳市", 0),
            "sz_memberships_city_map": findex["chain_city"].get(ch, {}).get("深圳市", 0),
            "chain_firms": findex["chain_firms"][ch],
        })
        leaf_total += len(ls)
        leaf_nat += len(nat_hit)
        leaf_sz += len(sz_hit)
        key_total += len(key)
        key_cov += len(key_hit)

    # L1 折叠口径（calc-logic v0.2.0 原意）：41 个 L1 节点，关键 = L1 企业数 >= 本链中位
    uncovered = {ch: set(v["uncovered_nodes"]) for ch, v in nodecov["chains"].items()}
    l1f = findex["l1_firms"]
    l1_rows = []
    l1_key_total = l1_key_cov = 0
    for ch in roots:
        cs = [c for c in l1 if c[:7] == ch]
        pos = [l1f[c] for c in cs if l1f.get(c, 0) > 0]
        median = statistics.median(pos)
        key = [c for c in cs if l1f.get(c, 0) > 0 and l1f[c] >= median]
        hit = [c for c in key if c not in uncovered.get(ch, set())]
        allhit = [c for c in cs if c not in uncovered.get(ch, set())]
        l1_key_total += len(key)
        l1_key_cov += len(hit)
        l1_rows.append({
            "chain_code": ch,
            "chain_name": names[ch],
            "l1_nodes": len(cs),
            "l1_covered": len(allhit),
            "key_l1": len(key),
            "key_l1_covered": len(hit),
            "median_threshold": median,
        })

    k_nodes = sum(v["K_nodes"] for v in nodecov["chains"].values())
    k_cov = sum(v["k_covered"] for v in nodecov["chains"].values())
    k_leaf = sum(v["K_leaf"] for v in nodecov["chains"].values())
    k_leaf_cov = sum(v["k_leaf_covered"] for v in nodecov["chains"].values())
    sz_memberships = sum(v for k, v in layer["chain_city"].items() if k.endswith("|深圳市"))

    out = {
        "metric_id": "M_CHAIN_SZ_KEY_NODE_COVERAGE",
        "metric_name": "深圳关键环节覆盖率",
        "support_judgment": "部分支持",
        "verdict_kind": "positive_evidence",
        "judgment_reason": (
            "覆盖率的分子分母都能在同一条链树上闭合：954 个叶级环节、463 个按全国中位数门槛"
            "判定的关键叶、其中 411 个有深圳企业（88.77%），与已交付 M_CHAIN_SZ_KEY_NODE_COUNT 的"
            "411/463 逐位一致。但 calc-logic 的『关键』由 importance_level 值集定义，该列在 gkx "
            "不存在（GAP-CHAIN-IMPORTANCE-ENUM 未签），本件只能用全国中位数分位代理；"
            "且 calc-logic 要求折 L1，41 个 L1 节点上关键集 25/25 全被覆盖，比率恒为 100%、零区分度。"
            "关键定义依赖外部标注，故判部分支持。"
        ),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "本件是截面指标：链树与挂链桥都是当日快照，口径内没有年度序列，"
            "不涉及基期分母，故 used/missing 为空。"
        ),
        "sources": [
            "code/_snapshots21/chain_tree_20261021.json",
            "code/_snapshots21/chain_stage_leaf_20261021.json",
            "code/_snapshots21/chain21_sz_nodecov_20261022.json",
            "code/_snapshots21/chain_firm_index_20261023.json",
            "code/_snapshots21/chain21_layer_20261022.json",
            "code/_snapshots21/chain_live_result_probe_20261023.json",
        ],
        "rule": {
            "leaf": "定长分段编码：父码 = 去末 2 位；叶 = 无子节点的非根码（954）",
            "key": "逐链 median(有企业叶级环节的全国企业家数)；n_national >= median",
            "covered": "该叶级环节在 chain_stage_leaf 的深圳市切片里企业家数 > 0",
            "not_used": "不用『叶级企业数合计 / 链企业数』做覆盖率（§3.54：7 条链会超过 100%）",
        },
        "population": {
            "chain_firms_clean": 1714457,
            "chain_firms_union_note": "1,714,457 = 1,714,459 行有链 - 2 条畸形信用码（§3.52）",
            "tag_rows_raw": 2283762,
            "empty_link_rows": 569303,
            "internal_node_only_memberships": 147724,
            "bad_credit_rows": 2,
            "sz_memberships_4403": sz_memberships,
            "sz_memberships_city_map": sum(v.get("深圳市", 0) for v in findex["chain_city"].values()),
            "sz_distinct_firms_4403": nodecov["rows_sz"],
            "leaf_total": leaf_total,
            "leaf_with_national_firms": leaf_nat,
            "leaf_with_sz_firms": leaf_sz,
            "l1_total": len(l1),
        },
        "headline": {
            "key_leaf_total": key_total,
            "key_leaf_covered_sz": key_cov,
            "key_leaf_coverage_pct": round(100.0 * key_cov / key_total, 2),
            "key_leaf_gap": key_total - key_cov,
            "leaf_total": leaf_total,
            "leaf_covered_sz": leaf_sz,
            "leaf_coverage_pct": round(100.0 * leaf_sz / leaf_total, 2),
            "leaf_covered_sz_prefix": k_leaf_cov,
            "leaf_coverage_prefix_pct": round(100.0 * k_leaf_cov / k_leaf, 2),
            "leaf_with_national_firms_pct": round(100.0 * leaf_nat / leaf_total, 2),
            "all_node_total": k_nodes,
            "all_node_covered_sz": k_cov,
            "all_node_coverage_pct": round(100.0 * k_cov / k_nodes, 2),
            "l1_key_total": l1_key_total,
            "l1_key_covered_sz": l1_key_cov,
            "l1_key_coverage_pct": round(100.0 * l1_key_cov / l1_key_total, 2),
            "l1_all_coverage_pct": round(
                100.0 * sum(r["l1_covered"] for r in l1_rows) / len(l1), 2
            ),
        },
        "by_chain": rows,
        "l1_by_chain": l1_rows,
        "live_probe": {k: probe[k] for k in (
            "gkx_has_result_face", "gkx_chain_related_tables", "live_table_rows",
            "live_usable", "live_unusable_reason", "verdict")},
        "checks": {
            "sum_key_leaves": sum(r["key_leaves"] for r in rows),
            "sum_key_covered": sum(r["key_leaves_covered_sz"] for r in rows),
            "sum_leaves": sum(r["leaves"] for r in rows),
            "match_sibling_key_node_count": (key_total == 463 and key_cov == 411),
            "match_national_leaf_coverage": (leaf_nat == 916 and leaf_total == 954),
            "prefix_minus_exact_sz_leaves": k_leaf_cov - leaf_sz,
            "non_sz_memberships": 1714457 - sz_memberships,
            "city_mapping_gap": (
                sz_memberships - sum(v.get("深圳市", 0) for v in findex["chain_city"].values())
            ),
        },
        "gaps": [
            "importance_level 在 gkx 不存在，关键值集只能中位数代理（GAP-CHAIN-IMPORTANCE-ENUM）",
            "calc-logic 的 L1 折叠在本树上是 25/25 恒 100%，无区分度",
            "深圳判定按登记地 4403，实际经营地不可得",
            "chain_firm_index 的城市映射用 admin_area 精确匹配，admin_area 快照仅 20,000 行覆盖不全，深圳被判成未匹配；本件改用 4403 前缀并与 M_CHAIN_SZ_ENTERPRISE_COUNT 对齐",
        ],
    }
    path = os.path.join(HERE, "M_CHAIN_SZ_KEY_NODE_COVERAGE_out.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1, sort_keys=True)
    print(f"[ok] M_CHAIN_SZ_KEY_NODE_COVERAGE key={key_cov}/{key_total} "
          f"leaf={leaf_sz}/{leaf_total} l1={l1_key_cov}/{l1_key_total}")


if __name__ == "__main__":
    main()
