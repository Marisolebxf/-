#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_SYNTH_DS_21_GRAPH_ANALYSIS_005 产业链图谱结构分析（20261023，W16-F1）。

口径
----
本件要的是「产业链图上的结构量」，不是企业关系图。gkx 侧：
  * `dwd_industry_chain_info` 1,273 行 → `chain_tree_20261021.json`；
  * `dwd_org_industry_tags` 2,283,762 行 → `chain_firm_index_20261023.json`
    （12 条链 / 41 个一级环节 / 35,046 个去重企业—链对 / 49,234 个企业—一级环节对）。
阻塞：`graph_node`、`industry_chain_entity_rel` 在 gkx 均不存在（实查 information_schema），
所以**企业级图上中心性拒拟**；本件只算链级/一级环节级的结构量，并显式声明。

链树实测：`parent_code` 不是 `industry_code`，而是 12 个**链名**；`level` 整列为 0。
因此真实层级是「链名 → 叶节点」两层，不存在三层以上深度；`level` 列不可用。

输出：code/M_SYNTH_DS_21_GRAPH_ANALYSIS_005_out.json
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict

import networkx as nx

import _f1_common as F

MID = "M_SYNTH_DS_21_GRAPH_ANALYSIS_005"
TREE = F.load("chain_tree_20261021.json")
IDX = F.load("chain_firm_index_20261023.json")
ENT = F.load("ent_graph109_20261023.json")


def concentration(values: dict) -> dict:
    vals = sorted(values.values(), reverse=True)
    total = sum(vals)
    return {
        "n": len(vals),
        "total": total,
        "max": vals[0] if vals else 0,
        "top1_share_pct": F.pct(vals[0], total) if vals else 0.0,
        "top3_share_pct": F.pct(sum(vals[:3]), total) if vals else 0.0,
        "top5_share_pct": F.pct(sum(vals[:5]), total) if vals else 0.0,
        "gini": F.gini(vals),
        "hhi": F.hhi(vals),
        "effective_n": round(10000 / F.hhi(vals), 2) if F.hhi(vals) else 0.0,
    }


def main() -> None:
    # ---- 链树：12 个链名根 + 1,273 个叶 ----
    codes = [r["industry_code"] for r in TREE]
    parents = Counter(r["parent_code"] for r in TREE)
    code_set = set(codes)
    resolvable_parent = sum(v for k, v in parents.items() if k in code_set)
    chain_name = IDX["chain_name"]
    name_to_code = {v: k for k, v in chain_name.items()}
    roots = sorted(parents)
    root_codes = [name_to_code.get(r, r) for r in roots]
    leaves_per_chain = {name_to_code.get(k, k): v for k, v in parents.items()}

    # ---- 12 链 / 41 个一级环节 ----
    l1_name = IDX["l1_name"]
    l1_per_chain = defaultdict(list)
    for c in l1_name:
        l1_per_chain[c[:7]].append(c)
    chain_firm = {k: int(v) for k, v in ENT["industry"]["chain_firm_n"].items()}
    l1_tag = {k: int(v) for k, v in IDX["l1_firms"].items()}

    # ---- 一级环节共现图：同一企业落多个 L1 时连边 ----
    G = nx.Graph()
    G.add_nodes_from(l1_name)
    multi = [sorted(set(v)) for v in IDX["fin_credit_l1"].values() if len(set(v)) > 1]
    pair_w = Counter()
    for vs in multi:
        for i in range(len(vs)):
            for j in range(i + 1, len(vs)):
                pair_w[(vs[i], vs[j])] += 1
    for (a, b), w in pair_w.items():
        G.add_edge(a, b, weight=w)

    gs = F.graph_stats(G, top_n=10)
    betw = nx.betweenness_centrality(G, normalized=True, weight=None)
    deg_w = dict(G.degree(weight="weight"))
    top_betw = sorted(((v, k) for k, v in betw.items()), reverse=True)[:10]
    top_deg = sorted(((deg_w[k], k) for k in deg_w), reverse=True)[:10]

    # ---- 链级集中度 ----
    cc = concentration(chain_firm)
    lc = concentration(l1_tag)

    # 链名 → 一级环节数
    l1_count_by_chain = {c: len(v) for c, v in l1_per_chain.items()}
    min_l1 = min(l1_count_by_chain.values())
    max_l1 = max(l1_count_by_chain.values())

    # 链树分支：每条链的叶节点数
    leaf_vals = sorted(leaves_per_chain.values(), reverse=True)

    derived = {
        "tree_resolvable_parent_pct": {
            "value": F.pct(resolvable_parent, len(TREE)),
            "numerator": resolvable_parent, "denominator": len(TREE),
            "denominator_note": "parent_code 能解析到 industry_code 的行数 / 链树行数（0 / 1,273）",
        },
        "tree_root_n": {
            "value": len(roots), "numerator": len(roots), "denominator": "distinct parent_code",
            "denominator_note": "链树根节点数 = parent_code 去重数（12 个链名）",
        },
        "tree_leaf_per_root_mean": {
            "value": round(len(TREE) / len(roots), 4),
            "numerator": len(TREE), "denominator": len(roots),
            "denominator_note": "叶节点数 / 根节点数（1,273 / 12）",
        },
        "tree_max_depth": {
            "value": 2, "numerator": "根→叶", "denominator": "parent_code→industry_code",
            "denominator_note": "实测最大层级：链名根 → 叶，共 2 层；level 整列为 0，不能当层级",
        },
        "l1_per_chain_min": {
            "value": min_l1, "numerator": min_l1, "denominator": "12 条链",
            "denominator_note": "每条链下最少一级环节数",
        },
        "l1_per_chain_max": {
            "value": max_l1, "numerator": max_l1, "denominator": "12 条链",
            "denominator_note": "每条链下最多一级环节数（集成电路 6 个）",
        },
        "l1_per_chain_mean": {
            "value": round(sum(l1_count_by_chain.values()) / len(l1_count_by_chain), 4),
            "numerator": sum(l1_count_by_chain.values()), "denominator": len(l1_count_by_chain),
            "denominator_note": "41 个一级环节 / 12 条链",
        },
        "chain_top1_share_pct": {
            "value": cc["top1_share_pct"], "numerator": cc["max"], "denominator": cc["total"],
            "denominator_note": "企业数最多链的去重企业数 / 12 链去重企业—链对总数（软件与信息服务 9,773 / 35,046）",
        },
        "chain_top3_share_pct": {
            "value": cc["top3_share_pct"], "numerator": sum(sorted(chain_firm.values(), reverse=True)[:3]),
            "denominator": cc["total"],
            "denominator_note": "前 3 链去重企业数之和 / 12 链去重企业—链对总数",
        },
        "chain_hhi": {
            "value": cc["hhi"], "numerator": "chain_hhi", "denominator": "12 链企业份额",
            "denominator_note": "12 条链的去重企业数份额 HHI（0—10,000）",
        },
        "chain_gini": {
            "value": cc["gini"], "numerator": "chain_gini", "denominator": "12 链企业数",
            "denominator_note": "12 条链企业数分布的 Gini",
        },
        "chain_effective_n": {
            "value": cc["effective_n"], "numerator": 10000, "denominator": cc["hhi"],
            "denominator_note": "有效链数 = 10,000 / HHI",
        },
        "l1_top5_share_pct": {
            "value": lc["top5_share_pct"], "numerator": sum(sorted(l1_tag.values(), reverse=True)[:5]),
            "denominator": lc["total"],
            "denominator_note": "前 5 个一级环节的标签行数 / 41 个一级环节标签行总数（标签行，非去重企业）",
        },
        "l1_hhi": {
            "value": lc["hhi"], "numerator": "l1_hhi", "denominator": "41 个一级环节标签行份额",
            "denominator_note": "一级环节标签行份额 HHI（标签行口径）",
        },
        "l1_graph_density_pct": {
            "value": round(gs["density"] * 100, 6), "numerator": gs["n_edges"],
            "denominator": gs["n_nodes"] * (gs["n_nodes"] - 1) / 2,
            "denominator_note": "一级环节共现图边数 / 完全图边数（32 / 820）",
        },
        "l1_graph_component_share_pct": {
            "value": gs["largest_component_share_pct"], "numerator": gs["largest_component"],
            "denominator": gs["n_nodes"],
            "denominator_note": "一级环节共现图最大连通片节点数 / 41",
        },
        "l1_multi_chain_firm_pct": {
            "value": F.pct(len(multi), len(IDX["fin_credit_l1"])),
            "numerator": len(multi), "denominator": len(IDX["fin_credit_l1"]),
            "denominator_note": "落多个一级环节的企业数 / fin_credit_l1 覆盖企业数（402 / 6,479）",
        },
        "chain_firm_per_chain_mean": {
            "value": round(cc["total"] / 12, 4), "numerator": cc["total"], "denominator": 12,
            "denominator_note": "35,046 个去重企业—链对 / 12 条链",
        },
        "chain_leaf_per_firm": {
            "value": round(len(TREE) / cc["total"], 6), "numerator": len(TREE), "denominator": cc["total"],
            "denominator_note": "链树叶节点数 / 去重企业—链对数（1,273 / 35,046），仅表示目录密度",
        },
    }

    payload = {
        "metric_name": "产业链图谱结构分析",
        "source": {
            "db": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）",
            "tables": [
                "gkx.dwd_industry_chain_info (1,273)",
                "gkx.dwd_org_industry_tags (2,283,762)",
            ],
            "snapshots": [
                "code/_snapshots21/chain_tree_20261021.json",
                "code/_snapshots21/chain_firm_index_20261023.json",
                "code/_snapshots21/ent_graph109_20261023.json",
            ],
        },
        "chain_tree": {
            "rows": len(TREE),
            "unique_industry_code": len(code_set),
            "distinct_parent_code": len(parents),
            "resolvable_parent_rows": resolvable_parent,
            "level_values": dict(Counter(r["level"] for r in TREE)),
            "roots": [{"name": r, "code": name_to_code.get(r), "leaves": parents[r]} for r in roots],
            "max_depth": 2,
            "depth_note": "parent_code 是 12 个链名而不是 industry_code；level 整列为 0。"
                          "真实层级只有「链名→叶」两层，不能声称三层以上。",
            "leaves_per_chain": {name_to_code.get(k, k): v for k, v in parents.items()},
            "leaves_per_chain_max": leaf_vals[0] if leaf_vals else 0,
            "leaves_per_chain_min": leaf_vals[-1] if leaf_vals else 0,
        },
        "chain_level": {
            "n_chains": len(chain_name),
            "n_l1": len(l1_name),
            "l1_per_chain": {k: len(v) for k, v in l1_per_chain.items()},
            "chain_name": chain_name,
            "l1_name": l1_name,
            "firm_chain_pairs": cc["total"],
            "firm_l1_pairs": 49234,
            "note": "firm_chain_pairs 是去重口径（ent_graph109）；firm_l1_pairs 来自 §3.55 的 49,234；"
                    "l1_firms 的 537,129 等是标签行，不是企业数，不得混用。",
        },
        "chain_concentration": {
            **cc,
            "values": chain_firm,
        },
        "l1_concentration": {
            **lc,
            "values_tag_rows": l1_tag,
            "note": "一级环节没有去重企业数快照，只有标签行；本段所有占比按标签行算，不得写成企业数。",
        },
        "l1_graph": {
            "definition": "节点=41 个一级环节；边=同一企业落多个一级环节（fin_credit_l1 的 402 家企业）",
            "n_nodes": gs["n_nodes"],
            "n_edges": gs["n_edges"],
            "density": gs["density"],
            "avg_degree": gs["avg_degree"],
            "max_degree": gs["max_degree"],
            "isolates": gs["isolates"],
            "n_components": gs["n_components"],
            "largest_component": gs["largest_component"],
            "largest_component_share_pct": gs["largest_component_share_pct"],
            "component_top5": gs["component_top5"],
            "top_degree": [{"name": l1_name.get(k, k), "code": k, "weighted_degree": v} for v, k in top_deg],
            "top_betweenness": [{"name": l1_name.get(k, k), "code": k, "betweenness": round(v, 8)} for v, k in top_betw],
            "multi_l1_firm_n": len(multi),
            "cooccurrence_pair_n": len(pair_w),
            "note": "这是链环节共现投影，不是企业关系图；不能据此说两家企业合作。",
        },
        "blocked": {
            "graph_node": "gkx 无表（information_schema 实查 0 行）",
            "industry_chain_entity_rel": "gkx 无表（实查 0 行）",
            "impact": "企业级图上中心性（度/中介/接近）拒拟；只保留链级/一级环节级结构量。",
        },
        "rejected_dimensions": [
            {"dimension": "企业级图上中心性",
             "reason": "industry_chain_entity_rel / graph_node 在 gkx 均不存在，缺企业—链关系边",
             "replacement": "12 链 / 41 一级环节的集中度与共现图结构量",
             "negative_evidence": "code/_probe_blocked_f1_20261023.json → industry_chain_entity_rel、graph_node"},
            {"dimension": "三层以上链树深度",
             "reason": "chain_tree.parent_code 只指向 12 个链名，level 整列为 0，实际只有两层",
             "replacement": "以 12 链 → 41 一级环节的两级映射替代",
             "negative_evidence": "chain_tree_20261021.json 的 level 全 0、parent 可解析行 0"},
            {"dimension": "上/中/下游归属",
             "reason": "P17 明确该映射为本工程自建，且 4 条链目录缺下游环节",
             "replacement": "不做上中下游切分，只报链级/环节级结构",
             "negative_evidence": "PENDING_RULINGS_20261023.md P17"},
        ],
        "verdict_kind": "negative_evidence",
        "absence_probe": F.absence_probe(['industry_chain_entity_rel', 'graph_node', 'industry_chain_node']),
        "derived": derived,
        "sources": [
            "code/_snapshots21/chain_tree_20261021.json",
            "code/_snapshots21/chain_firm_index_20261023.json",
            "code/_snapshots21/ent_graph109_20261023.json",
            "code/_probe_blocked_f1_20261023.json",
        ],
    }

    F.write_out(MID, payload, support="部分支持", used=[], missing=[],
                note="链树与链标签为全量截面（无年度字段），不做年度切片；"
                     "本件不含企业级关系边，故无基期可分。")
    print(json.dumps({"chains": len(chain_name), "l1": len(l1_name),
                      "tree_rows": len(TREE), "l1_edges": gs["n_edges"],
                      "top_chain": max(chain_firm, key=chain_firm.get)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
