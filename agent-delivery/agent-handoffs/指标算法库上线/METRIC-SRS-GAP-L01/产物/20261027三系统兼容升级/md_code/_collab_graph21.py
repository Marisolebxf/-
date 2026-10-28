#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""合著网络取数层（20261022）—— 纯本地、零 SQL、零 demo_*。

四件图/网络类指标（DS_21_008 / DS_23_001 / DS_23_002 / 以及交叉校验用的 191_1 口径）
共用同一张「机构合著图」，本模块只做四件事：装论文、建图、规范化、统计。

图口径（单一）：
  节点 = 中文论文 `author_info_list` 里出现过的**原始机构串**（不做上下级合并）；
  边   = 同一篇论文的共同署名（无向），边权 = 共同署名篇数；
  门槛 = 该机构在全语料中出现 ≥ `min_papers` 篇（默认 2）。

为什么用原始机构串而不是归并后的主体：gkx 没有机构主数据表，
`dwd_zh_paper.author_info_list` 里的 `institution` 是自由文本，
归并规则一旦引入就会改变节点数、边数与所有算法读数；本批统一不做合并，
并在正文 §四 披露「同名不同院系会被拆成多个节点」。

输入（只读落盘快照，见 `_synth21_common.papers()`）：
  code/_snapshots21/a25_paper_panel.json      100,900 篇中文论文（含 author_info_list）
  code/_snapshots21/probe_a26_20261022.json   中文被引 20,031 行
来源：gkx @ 183.240.141.251:3318（dwd_zh_paper / dwd_zh_paper_citation），2026-10-22 落盘。

确定性：本模块 import 时若未设 PYTHONHASHSEED=0 就以该环境变量自重启进程。
字符串哈希随机化会改变 set 迭代顺序 → 节点插入顺序 → 所有依赖遍历顺序的算法
（A* 的堆序、LPA、Louvain）读数漂移；固定后同一份代码两次运行逐位一致。
"""
from __future__ import annotations

import collections
import itertools
import os
import statistics
import sys

if os.environ.get("PYTHONHASHSEED") != "0":
    os.environ["PYTHONHASHSEED"] = "0"
    os.execv(sys.executable, [sys.executable, "-u", os.path.abspath(sys.argv[0]),
                              *sys.argv[1:]])

import networkx as nx  # noqa: E402

import _synth21_common as S  # noqa: E402

WINDOW = (2021, 2022, 2023, 2024)
SOURCE = ("gkx @ 183.240.141.251:3318（只读账号 gkx_reader_zp）：dwd_zh_paper.author_info_list "
          "→ code/_snapshots21/a25_paper_panel.json，2026-10-22 落盘；本模块零 SQL")


def papers() -> list[dict]:
    return S.papers()


def paper_meta() -> dict:
    return S.paper_meta()


def build(min_papers: int = 2, upto_year: int | None = None,
          from_year: int | None = None, insts_whitelist=None):
    """建机构合著图。返回 (G, meta_dict)。

    upto_year / from_year 用于时序切分（008 的训练图 = upto_year=2020）。
    """
    pc = collections.Counter()
    edges = collections.Counter()
    used = 0
    for p in papers():
        y = p["year"]
        if not y:
            continue
        if upto_year is not None and y > upto_year:
            continue
        if from_year is not None and y < from_year:
            continue
        used += 1
        ins = sorted({i for i in p["insts"] if i})
        if insts_whitelist is not None:
            ins = [i for i in ins if i in insts_whitelist]
        for i in ins:
            pc[i] += 1
        for a, b in itertools.combinations(ins, 2):
            edges[(a, b)] += 1

    nodes = sorted(i for i, n in pc.items() if n >= min_papers)
    nodeset = set(nodes)
    g = nx.Graph()
    for i in nodes:
        g.add_node(i, papers=pc[i])
    kept = 0
    for (a, b), w in sorted(edges.items()):
        if a in nodeset and b in nodeset:
            g.add_edge(a, b, weight=w)
            kept += 1
    meta = {"papers_used": used, "inst_universe": len(pc),
            "edge_pairs_universe": len(edges), "min_papers": min_papers,
            "nodes_before_threshold": len(pc), "edges_kept": kept,
            "upto_year": upto_year, "from_year": from_year,
            "source": SOURCE}
    return canonical(g), meta


def canonical(g: nx.Graph) -> nx.Graph:
    """节点/边按名称排序重建，消除 set 迭代顺序对遍历算法的影响。"""
    h = nx.Graph()
    for n in sorted(g.nodes):
        h.add_node(n, **g.nodes[n])
    for a, b, d in sorted(g.edges(data=True), key=lambda e: (e[0], e[1])):
        h.add_edge(a, b, **d)
    return h


def inst_type(name: str) -> str:
    s = str(name)
    if any(k in s for k in ("大学", "学院", "学校")):
        return "高校"
    if any(k in s for k in ("研究所", "研究院", "研究中心", "实验室", "医院", "科学院")):
        return "院所"
    if any(k in s for k in ("公司", "有限", "集团", "厂", "企业")):
        return "企业"
    return "其他"


def basic_stats(g: nx.Graph) -> dict:
    n, e = g.number_of_nodes(), g.number_of_edges()
    comps = sorted((len(c) for c in nx.connected_components(g)), reverse=True) if n else []
    deg = [d for _, d in g.degree()]
    wdeg = [d for _, d in g.degree(weight="weight")]
    den = e / (n * (n - 1) / 2) if n > 1 else None
    return {
        "n_nodes": n, "n_edges": e,
        "density": round(den, 8) if den is not None else None,
        "avg_degree": round(2 * e / n, 4) if n else None,
        "weighted_avg_degree": round(2 * sum(wdeg) / n, 4) if n else None,
        "isolates": sum(1 for d in deg if d == 0),
        "max_degree": max(deg) if deg else None,
        "components": len(comps),
        "giant_nodes": comps[0] if comps else 0,
        "giant_share": round(comps[0] / n, 4) if comps and n else None,
        "edge_weight_mean": round(statistics.mean([d["weight"] for _, _, d in g.edges(data=True)]), 4)
        if e else None,
        "single_weight_edges": sum(1 for _, _, d in g.edges(data=True) if d["weight"] == 1),
    }


def top_nodes(g: nx.Graph, k: int = 10) -> list[dict]:
    rows = sorted(g.degree, key=lambda t: (-t[1], t[0]))[:k]
    return [{"name": n, "degree": d, "papers": g.nodes[n].get("papers"),
             "type": inst_type(n)} for n, d in rows]


def degree_buckets(g: nx.Graph) -> dict:
    b = collections.Counter()
    for _, d in g.degree():
        if d == 0:
            b["0"] += 1
        elif d == 1:
            b["1"] += 1
        elif d == 2:
            b["2"] += 1
        elif d <= 5:
            b["3-5"] += 1
        elif d <= 10:
            b["6-10"] += 1
        else:
            b["11+"] += 1
    return dict(b)


def giant(g: nx.Graph) -> nx.Graph:
    return g.subgraph(max(nx.connected_components(g), key=len)).copy()


def stat_block(vals) -> dict:
    v = sorted(float(x) for x in vals if x is not None)
    if not v:
        return {"n": 0}

    def pct(q):
        k = min(len(v) - 1, max(0, int(round(q * (len(v) - 1)))))
        return v[k]

    return {"n": len(v), "min": round(v[0], 4), "p50": round(statistics.median(v), 4),
            "mean": round(statistics.mean(v), 4), "p90": round(pct(0.9), 4),
            "p99": round(pct(0.99), 4), "max": round(v[-1], 4)}
