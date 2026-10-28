#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_SYNTH_191_1 区域创新协同分析模型 —— 合作网络密度（20261022 复现）。

王惠口径（calc-logic）：实际合作边占完全图边数的比重 —— 实际无向边数 ÷ n(n-1)/2，
节点不足两个记空。本脚本按机构级合作网络实现：
  节点 = 深圳/广州/东莞/惠州 四市内、2021–2024 年中文论文 ≥3 篇的机构（去重机构串）
  边   = 同一篇论文的共同署名（无向、按论文去重后累加权重）
  密度 = 去重边数 ÷ n(n-1)/2
同时给出：分城市子图密度、城市对合作矩阵、平均度、连通分量、跨城桥接机构 TOP。

为什么不用专利共同申请：gkx.dwd_patent_applicants 只有 20,000 个 patent_id / 28,964 行，
抽样且以境外申请人为主（阿里巴巴、西门子、3M、固特异…），无法支撑四市企业合作网络；
本节在 §三 明写该维不可得。
输出：M_SYNTH_191_1_out.json
"""
from __future__ import annotations

import collections
import itertools
import json

import networkx as nx

import _synth21_common as S

MID = "M_SYNTH_191_1"
WINDOW = (2021, 2022, 2023, 2024)
MIN_PAPERS = 3


def build() -> tuple[nx.Graph, dict, dict]:
    pc = collections.Counter()
    city = {}
    edges = collections.Counter()
    for p in S.papers():
        if p["year"] not in WINDOW:
            continue
        ins = sorted({i for i in p["insts"] if i})
        for i in ins:
            pc[i] += 1
            if i not in city:
                city[i] = S.inst_city(i)
        for a, b in itertools.combinations(ins, 2):
            edges[(a, b)] += 1
    nodes = {i for i, n in pc.items() if n >= MIN_PAPERS and city.get(i) in S.CITIES}
    g = nx.Graph()
    for i in nodes:
        g.add_node(i, city=city[i], papers=pc[i])
    ne = 0
    for (a, b), w in edges.items():
        if a in nodes and b in nodes:
            g.add_edge(a, b, weight=w)
            ne += 1
    return g, city, {"papers_universe": len(S.papers()),
                     "inst_universe": len(pc), "edge_pairs_universe": len(edges),
                     "nodes_before_filter": sum(1 for i in pc if city.get(i) in S.CITIES),
                     "edges_before_filter": ne}


def density(g: nx.Graph) -> dict:
    n, e = g.number_of_nodes(), g.number_of_edges()
    den = e / (n * (n - 1) / 2) if n >= 2 else None
    comps = list(nx.connected_components(g)) if n else []
    return {"n_nodes": n, "n_edges": e, "density": round(den, 8) if den is not None else None,
            "density_per_mille": round(den * 1000, 4) if den is not None else None,
            "avg_degree": round(2 * e / n, 4) if n else None,
            "components": len(comps),
            "largest_component_share": round(max(len(c) for c in comps) / n, 4) if comps else None,
            "isolates": sum(1 for v, d in g.degree() if d == 0)}


def city_pairs() -> dict:
    m = collections.Counter()
    for p in S.papers():
        if p["year"] not in WINDOW:
            continue
        cs = sorted({S.inst_city(i) for i in p["insts"] if S.inst_city(i)})
        for a, b in itertools.combinations(cs, 2):
            m[tuple(sorted((a, b)))] += 1
    return {"%s|%s" % k: v for k, v in sorted(m.items(), key=lambda x: -x[1])}


def main() -> None:
    g, city, meta = build()
    base = density(g)
    per_city = {}
    for c in S.CITIES:
        sub = g.subgraph([n for n, d in g.nodes(data=True) if d["city"] == c]).copy()
        per_city[c] = density(sub)
    # 跨城边占比
    cross = sum(1 for a, b in g.edges if g.nodes[a]["city"] != g.nodes[b]["city"])
    within = g.number_of_edges() - cross
    # 桥接机构：跨城邻居数
    bridge = []
    for n, d in g.nodes(data=True):
        other = {g.nodes[m]["city"] for m in g.neighbors(n)} - {d["city"]}
        if other:
            bridge.append({"name": n, "city": d["city"], "papers": d["papers"],
                           "degree": g.degree(n), "partner_cities": sorted(other)})
    bridge.sort(key=lambda x: (-len(x["partner_cities"]), -x["degree"]))
    # 全样本参照（含京沪等）
    g_all = nx.Graph()
    for p in S.papers():
        if p["year"] not in WINDOW:
            continue
        ins = sorted({i for i in p["insts"] if i and S.inst_city(i)})
        for a, b in itertools.combinations(ins, 2):
            g_all.add_edge(a, b)
    all_nodes = {n for n in g_all if sum(1 for p in () ) == 0} if False else set(g_all.nodes)
    all_den = (g_all.number_of_edges() / (len(all_nodes) * (len(all_nodes) - 1) / 2)
               if len(all_nodes) >= 2 else None)

    out = {
        "metric_id": MID,
        "metric_name": "区域创新协同分析模型（合作网络密度）",
        "generated_at": "2026-10-22",
        "db": "gkx（三方库 183.240.141.251:3318，只读）",
        "formula_owner": "王惠（calc-logic：实际无向边数 ÷ 节点两两相连边数）",
        "evaluation_set": S.CITIES,
        "window": list(WINDOW),
        "year": max(WINDOW),
        "node_definition": ("四市内、窗口期中文论文 ≥%d 篇的机构（原始机构串，未做上下级合并）；"
                            "论文机构串来自 dwd_zh_paper.author_info_list" % MIN_PAPERS),
        "edge_definition": "同一篇论文共同署名，无向边；权重 = 共同署名论文数",
        "region": {**base, "cross_city_edges": cross, "within_city_edges": within,
                   "cross_city_share": round(cross / base["n_edges"], 4) if base["n_edges"] else None},
        "per_city": per_city,
        "city_pairs": city_pairs(),
        "bridge_institutions_top20": bridge[:20],
        "reference_all_cities": {"n_nodes": len(all_nodes),
                                 "n_edges": g_all.number_of_edges(),
                                 "density": round(all_den, 8) if all_den is not None else None},
        "universe": meta,
        "unavailable": {
            "patent_co_application": ("dwd_patent_applicants 仅 20,000 个 patent_id / 28,964 行，"
                                      "抽样且境外申请人占多数，四市企业合作网络不可得"),
            "project_cooperation": "dwd_zh_project 58,453 行但金额/参与机构字段不可用（nn 全空）",
            "scholar_coauthor_edges": ("dwd_scholar_paper_relation 1,065,385 行未落缓存；"
                                       "本批零 SQL 约束下改用论文机构共现建边"),
        },
        "support_judgment": "部分支持",
        "support_reason": (
            "王惠口径（边数 ÷ 完全图边数）可直接计算，节点与边都由真实论文署名构造，"
            "四市子图与城市对矩阵均有量；但只能覆盖学术协同：专利共同申请表只有 2 万件抽样、"
            "合作项目表金额与参与方字段全空，产学研协同的另外两条腿缺失；"
            "论文机构串仅 47.4% 能判城（其余机构名不含城市与校名），密度绝对值偏低。"
            "故判部分支持，不抬到完全转换支持。"),
        "note": ("节点阈值 ≥%d 篇是稳定性选择：阈值 1/2/3/5/10 时节点数为 7,215/1,979/1,094/613/268，"
                 "密度 0.022%%/0.089%%/0.196%%/0.446%%/1.205%%，随阈值单调上升；"
                 "本批固定 3 篇并同时给出分城子图，禁止跨阈值比较。" % MIN_PAPERS),
    }
    out.update(S.base_year_block(
        WINDOW, [],
        "论文窗口 2021–2024 四个真实年份；合作边为该窗口内共现，不含 2025–2026（2026 为残年）。"
        "本指标为窗口累计截面，不做年度分母除法。"))
    S.write_out(MID, out)
    print(json.dumps({"region": out["region"], "per_city": per_city,
                      "city_pairs": out["city_pairs"],
                      "all": out["reference_all_cities"]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
