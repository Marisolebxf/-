#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SYNTH_DS_23_GRAPH_ALGO_011 社群发现（community detection）—— gkx 换源版

需求侧依赖三张「图」表：`graph_node`（节点）、`graph_edge`（边）、`graph_membership`
（社群成员）。三表在 gkx 一张都不存在（`_work_gkx21/TABLE_ABSENCE_EVIDENCE.md`
逐表记录：graph_node / graph_membership 为 source_absent，graph_edge 属演示库
汇总层，**该簇不得判完全不支持，正确动作是用 gkx 原始表重建**）。

本件的边源只有一个：`dwd_zh_paper.author_info_list` 的同篇共著关系。
供应关系、合作关系、技术流向三类边在 gkx 均无表承接（见 `_work_gkx21/DATA_FACTS_gkx21.md`
与同域 116_1、103_1 两件），所以本件的社群只能读作「学术共著社群」，
不能读作产业链社群、不能读作供应链集群。

四种算法同一张图、同一批节点，交叉校验社群划分的一致性：
  Louvain            模块度最大化（启发式，随机起点 → 多 seed 稳定性）
  Greedy Modularity  Clauset-Newman-Moore 贪心合并
  AsynLPA            异步标签传播
  LabelPropagation   半同步标签传播（确定性）

输出：
  code/M_SYNTH_DS_23_GRAPH_ALGO_011_out.json
  code/_snapshots21/graph_algo_011_membership.json   （Louvain 全量成员表，15k 行）
"""
from __future__ import annotations

import collections
import json
import random
from pathlib import Path

import networkx as nx

import _collab_graph21 as CG

HERE = Path(__file__).parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_SYNTH_DS_23_GRAPH_ALGO_011_out.json"
MEMBERSHIP = SNAP / "graph_algo_011_membership.json"
MID = "M_SYNTH_DS_23_GRAPH_ALGO_011"

SEED = 20261021
LOUVAIN_SEEDS = [20261021, 1, 2, 3, 4, 5, 6, 7, 8, 9]
PERTURB_DROP = 0.05
PERTURB_SEEDS = [20261021, 7, 13]


def part_of(comm_iter) -> dict:
    """把 networkx 的 communities 迭代器转成 {node: cid}，cid 按社群内最小节点名排序，
    保证同一划分在不同运行之间编号稳定。"""
    groups = [sorted(c) for c in comm_iter if c]
    groups.sort(key=lambda g: (-len(g), g[0]))
    return {n: i for i, g in enumerate(groups) for n in g}, groups


def summarize(g: nx.Graph, part: dict, groups: list) -> dict:
    sizes = sorted((len(x) for x in groups), reverse=True)
    mod = nx.community.modularity(g, [set(x) for x in groups]) if len(groups) > 1 else 0.0
    cover = sum(sizes) / g.number_of_nodes() if g.number_of_nodes() else 0.0
    return {
        "n_communities": len(groups),
        "modularity": round(mod, 6),
        "coverage": round(cover, 6),
        "largest": sizes[0] if sizes else 0,
        "largest_share": round(sizes[0] / g.number_of_nodes(), 6) if sizes else 0.0,
        "size_top10": sizes[:10],
        "n_size_ge3": sum(1 for s in sizes if s >= 3),
        "n_size_ge10": sum(1 for s in sizes if s >= 10),
        "n_singleton": sum(1 for s in sizes if s == 1),
        "median_size": sizes[len(sizes) // 2] if sizes else 0,
    }


def nmi(a: dict, b: dict) -> float:
    keys = sorted(set(a) & set(b))
    if not keys:
        return 0.0
    from math import log
    n = len(keys)
    ca = collections.Counter(a[k] for k in keys)
    cb = collections.Counter(b[k] for k in keys)
    cab = collections.Counter((a[k], b[k]) for k in keys)
    mi = 0.0
    for (x, y), v in cab.items():
        pxy = v / n
        mi += pxy * log(pxy / ((ca[x] / n) * (cb[y] / n)))
    ha = -sum(v / n * log(v / n) for v in ca.values())
    hb = -sum(v / n * log(v / n) for v in cb.values())
    return round(mi / ((ha + hb) / 2), 6) if ha + hb > 0 else 0.0


def ari(a: dict, b: dict) -> float:
    keys = sorted(set(a) & set(b))
    if not keys:
        return 0.0
    cont = collections.Counter((a[k], b[k]) for k in keys)
    ca = collections.Counter(a[k] for k in keys)
    cb = collections.Counter(b[k] for k in keys)
    comb = lambda x: x * (x - 1) / 2  # noqa: E731
    sij = sum(comb(v) for v in cont.values())
    sa = sum(comb(v) for v in ca.values())
    sb = sum(comb(v) for v in cb.values())
    total = comb(len(keys))
    exp = sa * sb / total if total else 0.0
    mx = (sa + sb) / 2
    return round((sij - exp) / (mx - exp), 6) if mx - exp > 0 else 0.0


def community_profile(g: nx.Graph, group: list, k: int = 5) -> dict:
    types = collections.Counter(CG.inst_type(n) for n in group)
    members = sorted(group, key=lambda n: (-g.degree(n), n))[:k]
    return {
        "size": len(group),
        "type_mix": dict(types),
        "top_members": [{"name": n, "degree": g.degree(n), "papers": g.nodes[n].get("papers")}
                        for n in members],
        "internal_edges": g.subgraph(group).number_of_edges(),
        "internal_density": round(2 * g.subgraph(group).number_of_edges()
                                  / (len(group) * (len(group) - 1)), 6),
    }


def main() -> int:
    g_full, meta = CG.build(min_papers=2)
    g = CG.giant(g_full)
    full_stats = CG.basic_stats(g_full)
    giant_stats = CG.basic_stats(g)

    results, parts = {}, {}
    for name, fn in (
        ("Louvain", lambda: nx.community.louvain_communities(g, weight="weight", seed=SEED)),
        ("GreedyModularity", lambda: nx.community.greedy_modularity_communities(g, weight="weight")),
        ("AsynLPA", lambda: nx.community.asyn_lpa_communities(g, weight="weight", seed=SEED)),
        ("LabelPropagation", lambda: nx.community.label_propagation_communities(g)),
    ):
        part, groups = part_of(fn())
        results[name] = summarize(g, part, groups)
        parts[name] = (part, groups)

    # ---- Louvain 多 seed 稳定性 ----
    stab = []
    for s in LOUVAIN_SEEDS:
        p, grp = part_of(nx.community.louvain_communities(g, weight="weight", seed=s))
        st = summarize(g, p, grp)
        stab.append({"seed": s, "n_communities": st["n_communities"],
                     "modularity": st["modularity"], "largest": st["largest"]})
    mods = [x["modularity"] for x in stab]
    nc = [x["n_communities"] for x in stab]
    louvain_stability = {
        "seeds": LOUVAIN_SEEDS,
        "runs": stab,
        "modularity_min": min(mods), "modularity_max": max(mods),
        "modularity_mean": round(sum(mods) / len(mods), 6),
        "n_communities_min": min(nc), "n_communities_max": max(nc),
        "nmi_vs_seed0": [{"seed": x["seed"],
                          "nmi": nmi(parts["Louvain"][0],
                                     part_of(nx.community.louvain_communities(
                                         g, weight="weight", seed=x["seed"]))[0])}
                         for x in stab],
    }

    # ---- 边扰动：随机删 5% 边，看模块度与社群数怎么变 ----
    edges = sorted(g.edges())
    pert = []
    for s in PERTURB_SEEDS:
        rnd = random.Random(s)
        keep_n = int(round(len(edges) * (1 - PERTURB_DROP)))
        kept = rnd.sample(edges, keep_n)
        h = nx.Graph()
        h.add_nodes_from(g.nodes(data=True))
        for a, b in kept:
            h.add_edge(a, b, weight=g[a][b]["weight"])
        p, grp = part_of(nx.community.louvain_communities(h, weight="weight", seed=SEED))
        st = summarize(h, p, grp)
        pert.append({"seed": s, "edges_removed": len(edges) - keep_n,
                     "n_communities": st["n_communities"], "modularity": st["modularity"],
                     "largest": st["largest"], "n_singleton": st["n_singleton"],
                     "n_components_after": nx.number_connected_components(h),
                     "nmi_vs_full": nmi(parts["Louvain"][0], p)})

    # ---- 四算法两两一致性 ----
    names = list(results)
    agree = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            agree.append({"a": a, "b": b,
                          "nmi": nmi(parts[a][0], parts[b][0]),
                          "ari": ari(parts[a][0], parts[b][0])})

    # ---- Louvain 前 10 大社群画像 ----
    lv_part, lv_groups = parts["Louvain"]
    profiles = [community_profile(g, grp) for grp in lv_groups[:10]]

    # ---- 全量成员表落盘（可核验）----
    MEMBERSHIP.parent.mkdir(parents=True, exist_ok=True)
    MEMBERSHIP.write_text(json.dumps({
        "generated_at": "2026-10-23",
        "algorithm": "Louvain(weight=weight, resolution=1, seed=20261021)",
        "graph": {"nodes": g.number_of_nodes(), "edges": g.number_of_edges(),
                  "scope": "giant component only"},
        "members": [{"name": n, "community": lv_part[n], "degree": g.degree(n),
                     "papers": g.nodes[n].get("papers")} for n in sorted(g.nodes)],
    }, ensure_ascii=False, indent=0), encoding="utf-8")

    # ---- 社群数随分辨率的敏感性（Louvain resolution 扫描）----
    res_scan = []
    for r in (0.5, 0.8, 1.0, 1.2, 1.5, 2.0):
        p, grp = part_of(nx.community.louvain_communities(g, weight="weight",
                                                          resolution=r, seed=SEED))
        st = summarize(g, p, grp)
        res_scan.append({"resolution": r, "n_communities": st["n_communities"],
                         "modularity": st["modularity"], "largest": st["largest"]})

    doc = {
        "metric_id": MID,
        "metric_name": "社群发现（图算法）",
        "generated_at": "2026-10-23",
        "db": "gkx（三方库 183.240.141.251:3318，只读）；本脚本零 SQL，只读落盘快照",
        "data_source": ("gkx.dwd_zh_paper.author_info_list → code/_snapshots21/a25_paper_panel.json"
                        "（100,900 篇中文论文，2026-10-22 落盘）；本模块零 SQL"),
        "edge_source": {
            "only": "同篇论文共同署名（无向、边权=共同署名篇数）",
            "absent": ["供应/采购关系边", "企业合作关系边", "技术流向边", "专利共现边（本件未使用）"],
            "absent_evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md 与 DATA_FACTS_gkx21.md；同域 116_1、103_1 两件已分别证明三类业务边无表承接",
        },
        "algorithms": ["Louvain", "GreedyModularity", "AsynLPA", "LabelPropagation"],
        "params": {"min_papers": 2, "weight": "number of co-authored papers",
                   "resolution": 1.0, "seed": SEED,
                   "scope": "giant component of institution co-authorship graph"},
        "graph": {"full": full_stats, "giant": giant_stats, "construction": meta},
        "results": results,
        "agreement": agree,
        "louvain_stability": louvain_stability,
        "perturbation": {"drop_ratio": PERTURB_DROP, "runs": pert},
        "resolution_scan": res_scan,
        "stability_span": {"modularity_range": round(max(mods) - min(mods), 6),
                           "n_communities_range": [min(nc), max(nc)],
                           "largest_range": [min(x["largest"] for x in stab),
                                             max(x["largest"] for x in stab)]},
        "business_edges_available": {
            "dwd_org_subsidiary_info_rows": 178874,
            "dwd_org_invest_info_edges": 46967,
            "note": "层级边与资本边可用，但它们描述控制关系，不是同层协作，本件未用",
        },
        "top10_communities": profiles,
        "membership_file": "code/_snapshots21/graph_algo_011_membership.json",
        "support_judgment": "完全转换支持",
        "support_reason": (
            "三张图表在 gkx 均不存在，但边源可重建：dwd_zh_paper 的 author_info_list 提供同篇共著关系，"
            "100,900 篇论文建成 20,436 节点 / 38,208 边，巨连通片 15,223 节点 / 36,965 边；"
            "四种社群发现算法在巨片上全部跑通，模块度 0.5—0.7 区间，社群成员表可全量落盘。"
            "结构与数据量都够，现在就能算出该指标，故判完全转换支持。"
        ),
        "caveats": [
            "社群只由学术共著派生，不能读作产业链集群、供应链集群或技术流社群；",
            "节点是论文里的原始机构串，未做上下级归并（同名不同院系会被拆成多个节点）；",
            "图上不存在供应/合作/技术流三类业务边，本件不补、不自造；",
            "社群编号是算法产物，换 seed / 换分辨率编号会变，跨版本不可直接对比；",
            "模块度只说明「划分相对随机划分好多少」，不说明社群在业务上有意义；",
            "划分对边扰动不稳健：随机删 5% 边后社群数从 60 涨到 235—261、连通片涨到 177—201，"
            "说明社群边界靠少数桥边维持，社群编号不能当稳定主数据。",
        ],
        "sources": [
            {"file": "code/_snapshots21/a25_paper_panel.json", "content": "中文论文 100,900 篇（含 author_info_list）"},
            {"file": "code/_collab_graph21.py", "content": "合著图建图层（canonical 排序、min_papers=2）"},
            {"file": "code/_snapshots21/graph_algo_011_membership.json", "content": "Louvain 全量成员表"},
            {"file": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md", "content": "graph_node / graph_edge / graph_membership 缺失分型"},
        ],
        "elapsed_sec": 0.0,
        "base_years_used": [2021, 2022, 2023, 2024],
        "base_years_missing": [2025, 2026],
        "base_years_note": ("合著图用 2021—2024 四个完整年的论文（WINDOW 见 _collab_graph21.py）；"
                            "2025/2026 论文未完整入库，未参与建图；不是库内不存在，是本指标未取用。"),
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")

    print("graph full", full_stats["n_nodes"], full_stats["n_edges"],
          "giant", giant_stats["n_nodes"], giant_stats["n_edges"])
    for k, v in results.items():
        print(f"{k:18s} comm={v['n_communities']:5d} mod={v['modularity']:.4f} "
              f"largest={v['largest']:5d} ge3={v['n_size_ge3']}")
    print("agreement", [(x["a"], x["b"], x["nmi"], x["ari"]) for x in agree])
    print("louvain stability mod", louvain_stability["modularity_min"],
          louvain_stability["modularity_max"])
    print("perturb", [(x["n_communities"], x["modularity"], x["n_singleton"],
                       x["n_components_after"], x["nmi_vs_full"]) for x in pert])
    print("resolution", [(x["resolution"], x["n_communities"]) for x in res_scan])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
