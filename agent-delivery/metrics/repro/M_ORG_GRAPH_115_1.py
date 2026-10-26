#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ORG_GRAPH_115_1 机构关系图结构（20261023，W16-F1）。

口径（必须逐字保留）
------------------
gkx 无 `enterprise_cooperation` / `svc_org_card` / `svc_org_circle`（information_schema 实查），
所以**没有「机构合作」边**。本件用 `dwd_org_invest_info` + `dwd_org_shareholder_info`
的投资/股东边做**替代图**，并明确声明：这是「投资/股权视角的企业图」，
不是合作图、不是服务圈层图。替代不抬档，仍判部分支持。

点集：P0 = 底册 189,116 家；P1 = 至少有一条投资/股东边且两端都在底册的企业；
P2 = P1 的最大连通片。归一化分母 n−1；跨片比较只在 P2 内做。

输出：code/M_ORG_GRAPH_115_1_out.json
"""
from __future__ import annotations

import json
import random
from collections import Counter

import networkx as nx
from networkx.algorithms.community import louvain_communities, modularity

import _f1_common as F

MID = "M_ORG_GRAPH_115_1"
BASE = F.load("base_20261021.json")
EDGES = F.load("ent_edges_20261021.json")
ENT = F.load("ent_graph109_20261023.json")


def main() -> None:
    id2 = {r[0]: (r[2], r[4]) for r in BASE}
    base_ids = set(id2)

    pairs = set()
    invest_pairs = set()
    for a, b in EDGES["invest"]:
        if a in base_ids and b in base_ids and a != b:
            p = tuple(sorted((a, b)))
            pairs.add(p)
            invest_pairs.add(p)
    for a, b in EDGES["shareholder"]:
        if a in base_ids and b in base_ids and a != b:
            pairs.add(tuple(sorted((a, b))))

    G = nx.Graph()
    G.add_nodes_from(base_ids)
    G.add_edges_from(pairs)
    G1 = G.subgraph([n for n, d in G.degree() if d >= 1]).copy()
    comps = sorted(nx.connected_components(G1), key=len, reverse=True)
    giant = G1.subgraph(comps[0]).copy() if comps else nx.Graph()

    gs = F.graph_stats(G1, top_n=10)
    g0 = F.graph_stats(G, top_n=10)
    gp = F.graph_stats(giant, top_n=10)

    top10 = []
    for d, nid in gs["top_nodes"]:
        nm, city = id2.get(nid, ("", ""))
        top10.append({"org_id": nid, "name": nm, "city": city, "degree": d,
                      "in_invest": any(nid in p for p in invest_pairs)})

    # 度分布分桶（P1）
    # 攻击容忍：去掉度前 1% / 5%
    def largest_after_remove(k: int, seed: int | None = None) -> dict:
        H = G1.copy()
        if seed is None:
            drop = [n for n, _ in sorted(H.degree(), key=lambda x: (-x[1], str(x[0])))[:k]]
        else:
            drop = random.Random(seed).sample(sorted(H.nodes()), k)
        H.remove_nodes_from(drop)
        cs = [len(c) for c in nx.connected_components(H)] if H.number_of_nodes() else [0]
        return {"removed": k, "remaining": H.number_of_nodes(),
                "largest": max(cs), "largest_share_pct": F.pct(max(cs), G1.number_of_nodes())}

    k1 = max(1, round(G1.number_of_nodes() * 0.01))
    k5 = max(1, round(G1.number_of_nodes() * 0.05))
    atk1 = largest_after_remove(k1)
    atk5 = largest_after_remove(k5)
    rnd1 = [largest_after_remove(k1, seed=s)["largest_share_pct"] for s in range(10)]
    rnd5 = [largest_after_remove(k5, seed=s)["largest_share_pct"] for s in range(10)]

    # 社群：只在巨片上跑（全图 3,623 片，Louvain 会被小片主导）。
    # 确定性要点（2026-10-23 实测社群数在 78—97 间漂）：
    #   1) NetworkX 的 G.edges() 方向随邻接插入顺序变化，必须先 canonical 成 (min,max) 再排序，
    #      否则同一无向边会以 (a,b)/(b,a) 两种朝向混入，排序后的插入顺序仍随进程变；
    #   2) 用整数重标号并显式重建图，避免字符串哈希随机化影响邻接顺序。
    _nodes = sorted(giant.nodes())
    _mp = {n: i for i, n in enumerate(_nodes)}
    _elist = sorted((min(_mp[u], _mp[v]), max(_mp[u], _mp[v])) for u, v in giant.edges())
    giant_s = nx.Graph()
    giant_s.add_nodes_from(range(len(_nodes)))
    giant_s.add_edges_from(_elist)
    comm = louvain_communities(giant_s, seed=20261021, weight=None)
    sizes = sorted((len(c) for c in comm), reverse=True)
    mod = modularity(giant_s, comm) if giant_s.number_of_edges() else 0.0

    ass = nx.degree_assortativity_coefficient(G1) if G1.number_of_edges() else 0.0
    trans = nx.transitivity(G1) if G1.number_of_edges() else 0.0

    degree_vals = [d for _, d in G1.degree()]
    top10_deg = sum(d for d, _ in gs["top_nodes"])
    sum_deg = sum(degree_vals)

    derived = {
        "base_to_edge_node_pct": {
            "value": F.pct(gs["n_nodes"], len(base_ids)),
            "numerator": gs["n_nodes"], "denominator": len(base_ids),
            "denominator_note": "有投资/股东边的企业数 / 底册企业数（19,768 / 189,116）",
        },
        "edge_node_ratio": {
            "value": round(gs["n_edges"] / gs["n_nodes"], 4),
            "numerator": gs["n_edges"], "denominator": gs["n_nodes"],
            "denominator_note": "P1 无向边数 / P1 节点数（19,628 / 19,768）",
        },
        "density_pct": {
            "value": round(gs["density"] * 100, 8), "numerator": gs["n_edges"],
            "denominator": gs["n_nodes"] * (gs["n_nodes"] - 1) / 2,
            "denominator_note": "P1 边数 / 完全图边数（19,628 / 195,377,028）",
        },
        "largest_component_share_pct": {
            "value": gs["largest_component_share_pct"], "numerator": gs["largest_component"],
            "denominator": gs["n_nodes"],
            "denominator_note": "P1 最大连通片节点数 / P1 节点数（10,462 / 19,768）",
        },
        "isolate_share_pct": {
            "value": F.pct(g0["isolates"], g0["n_nodes"]),
            "numerator": g0["isolates"], "denominator": g0["n_nodes"],
            "denominator_note": "P0 孤立点数 / 底册企业数（169,348 / 189,116）",
        },
        "component_mean_size": {
            "value": round(gs["n_nodes"] / gs["n_components"], 4),
            "numerator": gs["n_nodes"], "denominator": gs["n_components"],
            "denominator_note": "P1 节点数 / P1 连通片数（19,768 / 3,598）",
        },
        "degree_mean": {
            "value": gs["avg_degree"], "numerator": gs["n_edges"] * 2, "denominator": gs["n_nodes"],
            "denominator_note": "P1 平均度 = 2×边数 / 节点数（39,256 / 19,768）",
        },
        "degree_median": {
            "value": gs["median_degree"], "numerator": 1, "denominator": "P1 度序列",
            "denominator_note": "P1 度中位数（1，即一半以上企业只有 1 条边）",
        },
        "top10_degree_share_pct": {
            "value": F.pct(top10_deg, sum_deg), "numerator": top10_deg, "denominator": sum_deg,
            "denominator_note": "P1 度前 10 名度数和 / P1 度总和（1,290 / 39,256）",
        },
        "degree_gini": {
            "value": gs["gini"], "numerator": "gini", "denominator": "P1 度序列",
            "denominator_note": "P1 度分布 Gini",
        },
        "degree_hhi": {
            "value": gs["hhi"], "numerator": "hhi", "denominator": "P1 度份额",
            "denominator_note": "P1 度份额 HHI（0—10,000）",
        },
        "top1pct_removal_largest_pct": {
            "value": atk1["largest_share_pct"], "numerator": atk1["largest"],
            "denominator": gs["n_nodes"],
            "denominator_note": "去掉度前 1%（198 家）后最大连通片 / 原 P1 节点数（5,130 / 19,768）",
        },
        "top5pct_removal_largest_pct": {
            "value": atk5["largest_share_pct"], "numerator": atk5["largest"],
            "denominator": gs["n_nodes"],
            "denominator_note": "去掉度前 5%（988 家）后最大连通片 / 原 P1 节点数（34 / 19,768）",
        },
        "random1pct_largest_mean_pct": {
            "value": round(sum(rnd1) / len(rnd1), 4), "numerator": "10 seeds mean",
            "denominator": gs["n_nodes"],
            "denominator_note": "随机去 1% 节点（10 个 seed）最大连通片占比均值",
        },
        "random5pct_largest_mean_pct": {
            "value": round(sum(rnd5) / len(rnd5), 4), "numerator": "10 seeds mean",
            "denominator": gs["n_nodes"],
            "denominator_note": "随机去 5% 节点（10 个 seed）最大连通片占比均值",
        },
        "louvain_community_n": {
            "value": len(comm), "numerator": len(comm), "denominator": "P2 节点",
            "denominator_note": "巨片 Louvain 社群数（seed=20261021）",
        },
        "louvain_modularity": {
            "value": round(mod, 6), "numerator": "modularity", "denominator": "P2 边",
            "denominator_note": "巨片 Louvain 模块度",
        },
        "largest_community_share_pct": {
            "value": F.pct(sizes[0], gp["n_nodes"]) if sizes else 0.0,
            "numerator": sizes[0] if sizes else 0, "denominator": gp["n_nodes"],
            "denominator_note": "最大社群节点数 / P2 节点数",
        },
        "degree_assortativity": {
            "value": round(float(ass), 6), "numerator": "assortativity", "denominator": "P1 边",
            "denominator_note": "P1 度同配系数（正=高度连高度，负=高度连低度）",
        },
        "transitivity": {
            "value": round(float(trans), 6), "numerator": "triangles", "denominator": "triples",
            "denominator_note": "P1 全局聚类系数（三角形/三元组）",
        },
        "invest_edge_share_pct": {
            "value": F.pct(len(invest_pairs), gs["n_edges"]),
            "numerator": len(invest_pairs), "denominator": gs["n_edges"],
            "denominator_note": "投资边（去重无向）/ P1 全部无向边（9,292 / 19,628）",
        },
        "shareholder_edge_share_pct": {
            "value": F.pct(gs["n_edges"] - len(invest_pairs), gs["n_edges"]),
            "numerator": gs["n_edges"] - len(invest_pairs), "denominator": gs["n_edges"],
            "denominator_note": "股东边（去重无向）/ P1 全部无向边（10,336 / 19,628）",
        },
    }

    payload = {
        "metric_name": "机构关系图结构（投资/股权代理）",
        "source": {
            "db": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）",
            "tables": [
                "gkx.dwd_org_base_info (189,116)",
                "gkx.dwd_org_invest_info (46,967)",
                "gkx.dwd_org_shareholder_info (400,286)",
            ],
            "snapshots": [
                "code/_snapshots21/base_20261021.json",
                "code/_snapshots21/ent_edges_20261021.json",
                "code/_snapshots21/ent_graph109_20261023.json",
            ],
        },
        "graph_definition": {
            "nodes": "底册企业（org_id）",
            "edges": "投资边 + 股东边，去重无向；两端必须都在底册",
            "not": "不是合作边、不是服务边、不是供应链边；三类在 gkx 均无表",
        },
        "point_sets": [
            {"id": "P0", "name": "底册全量", "n_nodes": g0["n_nodes"], "n_edges": g0["n_edges"],
             "isolates": g0["isolates"], "n_components": g0["n_components"]},
            {"id": "P1", "name": "有投资/股东边", "n_nodes": gs["n_nodes"], "n_edges": gs["n_edges"],
             "isolates": 0, "n_components": gs["n_components"]},
            {"id": "P2", "name": "最大连通片", "n_nodes": gp["n_nodes"], "n_edges": gp["n_edges"],
             "isolates": 0, "n_components": 1},
        ],
        "normalization": {
            "denominator": "n-1",
            "n_by_point_set": {"P0": g0["n_nodes"] - 1, "P1": gs["n_nodes"] - 1, "P2": gp["n_nodes"] - 1},
            "note": "度中心性归一分母为点集 n−1；本件不做跨片中心性比较。",
        },
        "stats": {
            "P0": g0, "P1": gs, "P2": gp,
            "degree_buckets_P1": gs["buckets"],
            "top10": top10,
            "attack": {"top1pct": atk1, "top5pct": atk5,
                       "random1pct_mean_pct": round(sum(rnd1) / len(rnd1), 4),
                       "random5pct_mean_pct": round(sum(rnd5) / len(rnd5), 4),
                       "note": "top1pct/top5pct 是确定性去高度节点；random 是 10 个 seed 的均值。"},
            "louvain": {"n": len(comm), "modularity": round(mod, 6),
                        "sizes_top10": sizes[:10], "largest_share_pct": F.pct(sizes[0], gp["n_nodes"]) if sizes else 0.0},
            "assortativity": round(float(ass), 6),
            "transitivity": round(float(trans), 6),
        },
        "blocked": {
            "enterprise_cooperation": "gkx 无表（information_schema 实查 0 行）",
            "svc_org_card": "gkx 无表",
            "svc_org_circle": "gkx 无表",
            "impact": "合作边、服务能力、圈层成员三维全部拒拟；本件只保留投资/股权结构。",
        },
        "rejected_dimensions": [
            {"dimension": "机构合作边",
             "reason": "enterprise_cooperation 在 gkx 不存在（实查 0 行）",
             "replacement": "投资/股东边代理图",
             "negative_evidence": "code/_probe_blocked_f1_20261023.json → enterprise_cooperation"},
            {"dimension": "服务机构卡片/圈层",
             "reason": "svc_org_card / svc_org_circle 在 gkx 不存在；live ADS 的 svc_org_card 为 0 行",
             "replacement": "Louvain 社群替代「算法圈层」，明示不是业务圈层",
             "negative_evidence": "code/_probe_blocked_f1_20261023.json → svc_org_card、svc_org_circle"},
            {"dimension": "全机构（高校/院所）关系图",
             "reason": "研究机构/高校表各 20,000 行样本，且无机构—企业边；无法并入同一张图",
             "replacement": "只用底册企业；高校/院所侧不建边",
             "negative_evidence": "gkx.dwd_forg_research_org_info / dwd_forg_university_org_info 各 20,000 行，无关系列"},
            {"dimension": "合作强度/供应链位置",
             "reason": "无合作边、无供应链表；投资金额单位未统一，不能当合作强度",
             "replacement": "只用无向结构量，不用金额权重",
             "negative_evidence": "DATA_FACTS §3.60、P20"},
        ],
        "verdict_kind": "negative_evidence",
        "absence_probe": F.absence_probe(['enterprise_cooperation', 'enterprise_supply_chain', 'svc_org_card', 'svc_org_circle']),
        "derived": derived,
        "sources": [
            "code/_snapshots21/base_20261021.json",
            "code/_snapshots21/ent_edges_20261021.json",
            "code/_snapshots21/ent_graph109_20261023.json",
            "code/_probe_blocked_f1_20261023.json",
        ],
    }

    F.write_out(MID, payload, support="部分支持", used=[], missing=[],
                note="投资/股东边为全量截面（无年度字段），不做年度切片；"
                     "底册成立年份不参与本件分母。")
    print(json.dumps({"P1": [gs["n_nodes"], gs["n_edges"]],
                      "largest": gs["largest_component"], "mod": round(mod, 4),
                      "top1": top10[0]["name"] if top10 else ""}, ensure_ascii=False))


if __name__ == "__main__":
    main()
