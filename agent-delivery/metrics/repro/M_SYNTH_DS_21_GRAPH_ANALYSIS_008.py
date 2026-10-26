#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SYNTH_DS_21_GRAPH_ANALYSIS_008 智能推荐（机构合作者推荐，gkx 换源版）。

需求：科技信息展示系统 §1.1.1.1.4.5.1.2.4「根据用户的查询行为、兴趣偏好或实际业务需求，
      动态分析并推荐相关的文献、专家、机构、研究项目或技术方案……结合图谱整体关系，
      从相似节点、协同创新网络中推送高相关性资源」。

本批实现「图谱协同推荐」这一条腿，并做**时序切分的离线评估**：
  训练图 = 2020 年及以前的中文论文机构合著图（≥2 篇门槛，7,742 节点）；
  测试正样本 = 2021 年及以后新出现、两端都在训练图中的机构对（训练图里没有这条边）；
  负样本 = 随机抽的「非边」（同一节点集、非自环、非已有边）。
打分器：共同邻居(CN) / Jaccard / Adamic-Adar(AA) / Resource Allocation(RA) /
        个性化 PageRank(PPR，α=0.85)。评估：AUC、Precision@10、Recall@10、命中来源占比。

输出：code/M_SYNTH_DS_21_GRAPH_ANALYSIS_008_out.json
"""
from __future__ import annotations

import collections
import itertools
import json
import math
import random
import time

import networkx as nx

import _collab_graph21 as CG
import _synth21_common as S

MID = "M_SYNTH_DS_21_GRAPH_ANALYSIS_008"
SPLIT_YEAR = 2020
N_POS_AUC = 2000
N_NEG_PER_POS = 100
N_SOURCES_PK = 200
SEED = 20261021


def cn(g, u, v):
    return len(set(g[u]) & set(g[v]))


def jaccard(g, u, v):
    a, b = set(g[u]), set(g[v])
    return len(a & b) / len(a | b) if (a | b) else 0.0


def aa(g, u, v):
    s = 0.0
    for w in set(g[u]) & set(g[v]):
        d = g.degree(w)
        if d > 1:
            s += 1.0 / math.log(d)
    return s


def ra(g, u, v):
    return sum(1.0 / g.degree(w) for w in set(g[u]) & set(g[v]) if g.degree(w) > 0)


SCORERS = {"CN": cn, "Jaccard": jaccard, "AA": aa, "RA": ra}


def auc(ps, ns):
    """Mann-Whitney AUC（并列取平均秩 0.5）。"""
    allv = [(x, 1) for x in ps] + [(x, 0) for x in ns]
    allv.sort(key=lambda t: t[0])
    rank_sum_pos = 0.0
    i = 0
    while i < len(allv):
        j = i
        while j < len(allv) and allv[j][0] == allv[i][0]:
            j += 1
        avg = (i + j + 1) / 2.0
        for k in range(i, j):
            if allv[k][1] == 1:
                rank_sum_pos += avg
        i = j
    n1, n0 = len(ps), len(ns)
    if not n1 or not n0:
        return None
    return round((rank_sum_pos - n1 * (n1 + 1) / 2.0) / (n1 * n0), 4)


def main() -> None:
    t_start = time.time()
    train_papers, test_papers = [], []
    for p in CG.papers():
        if not p["year"]:
            continue
        (train_papers if p["year"] <= SPLIT_YEAR else test_papers).append(p)

    g, meta = CG.build(min_papers=2, upto_year=SPLIT_YEAR)
    st = CG.basic_stats(g)
    nodes = sorted(g.nodes())

    test_edges = set()
    for p in test_papers:
        ins = sorted({i for i in p["insts"] if i in g})
        for a, b in itertools.combinations(ins, 2):
            if not g.has_edge(a, b):
                test_edges.add((a, b))
    test_edges = sorted(test_edges)

    rng = random.Random(SEED)
    pos_sample = rng.sample(test_edges, min(N_POS_AUC, len(test_edges)))
    neg_pool = []
    guard = 0
    while len(neg_pool) < N_POS_AUC * N_NEG_PER_POS and guard < N_POS_AUC * N_NEG_PER_POS * 20:
        guard += 1
        x, y = rng.choice(nodes), rng.choice(nodes)
        if x != y and not g.has_edge(x, y):
            neg_pool.append((x, y))

    auc_res = {}
    for name, fn in SCORERS.items():
        ps = [fn(g, u, v) for u, v in pos_sample]
        ns = [fn(g, u, v) for u, v in neg_pool]
        auc_res[name] = auc(ps, ns)

    # PPR
    ppr = {}

    def ppr_vec(s):
        if s not in ppr:
            ppr[s] = nx.pagerank(g, alpha=0.85, personalization={s: 1.0}, tol=1e-8)
        return ppr[s]

    t0 = time.perf_counter()
    ps = [ppr_vec(u).get(v, 0.0) for u, v in pos_sample]
    ns = [ppr_vec(u).get(v, 0.0) for u, v in neg_pool]
    auc_res["PPR"] = auc(ps, ns)
    ppr_auc_sec = round(time.perf_counter() - t0, 1)

    # P@10 / R@10
    by_src = collections.defaultdict(set)
    for u, v in test_edges:
        by_src[u].add(v)
        by_src[v].add(u)
    srcs = [s for s in by_src if by_src[s]]
    rng.shuffle(srcs)
    srcs = srcs[:N_SOURCES_PK]
    prec, rec, prec_ppr, rec_ppr = [], [], [], []
    hit_aa, hit_ppr = 0, 0
    for s in srcs:
        truth = by_src[s]
        cand = set(g[s])
        for m in g[s]:
            cand |= set(g[m])
        cand -= {s}
        cand -= set(g[s])
        if not cand:
            continue
        scored = sorted(((aa(g, s, c), c) for c in cand), reverse=True)[:10]
        top = [c for _, c in scored]
        h = len(set(top) & truth)
        prec.append(h / 10.0)
        rec.append(h / len(truth))
        hit_aa += 1 if h else 0

        vec = ppr_vec(s)
        top_ppr = sorted(cand, key=lambda c: -vec.get(c, 0.0))[:10]
        h2 = len(set(top_ppr) & truth)
        prec_ppr.append(h2 / 10.0)
        rec_ppr.append(h2 / len(truth))
        hit_ppr += 1 if h2 else 0

    # 具名推荐清单：取训练图度最高的 4 个机构
    named = [n for n, _ in sorted(g.degree, key=lambda t: (-t[1], t[0]))][:4]
    recs = []
    for s in named:
        cand = set()
        for m in g[s]:
            cand |= set(g[m])
        cand -= {s}
        cand -= set(g[s])
        scored = sorted(((aa(g, s, c), cn(g, s, c), c) for c in cand),
                        key=lambda t: (-t[0], -t[1], t[2]))[:10]
        recs.append({
            "source": s,
            "source_degree": g.degree(s),
            "source_papers": g.nodes[s]["papers"],
            "n_candidates": len(cand),
            "top10": [{"target": c, "adamic_adar": round(a, 4), "common_neighbors": k,
                       "target_papers": g.nodes[c]["papers"],
                       "seen_in_test_period": c in by_src.get(s, set())}
                      for a, k, c in scored],
        })

    out = {
        "metric_id": MID,
        "metric_name": "智能推荐（机构合作者推荐）",
        "generated_at": "2026-10-22",
        "db": "gkx（三方库 183.240.141.251:3318，只读）",
        "data_source": CG.SOURCE,
        "method": {
            "task": "机构合作者推荐（图谱协同创新网络）",
            "split": "中文论文年份 ≤2020 建训练图；2021—2026 新出现的机构对作测试正样本",
            "scorers": ["Common Neighbors", "Jaccard", "Adamic-Adar",
                        "Resource Allocation", "Personalized PageRank(α=0.85)"],
            "candidate_generation": "2 跳邻居候选集（排除源点与已合作邻居）",
        },
        "probes": {
            "papers_total": CG.paper_meta()["n"],
            "train_papers": len(train_papers),
            "test_papers": len(test_papers),
            "train_graph": st,
            "train_graph_construction": meta,
            "test_new_edges": len(test_edges),
            "auc_positives": len(pos_sample),
            "auc_negatives": len(neg_pool),
            "sources_evaluated": len(prec),
            "ppr_auc_seconds": ppr_auc_sec,
        },
        "compute": {
            "auc": auc_res,
            "precision_at_10": round(sum(prec) / len(prec), 4) if prec else None,
            "recall_at_10": round(sum(rec) / len(rec), 4) if rec else None,
            "ppr_precision_at_10": round(sum(prec_ppr) / len(prec_ppr), 4) if prec_ppr else None,
            "ppr_recall_at_10": round(sum(rec_ppr) / len(rec_ppr), 4) if rec_ppr else None,
            "source_hit_rate_aa": round(hit_aa / len(srcs), 4) if srcs else None,
            "source_hit_rate_ppr": round(hit_ppr / len(srcs), 4) if srcs else None,
            "named_recommendations": recs,
        },
        "support_judgment": "部分支持",
        "support_reason": (
            "图谱协同推荐链路已跑通并可离线评估：训练图 %d 节点 / %d 边，2021 年后新增测试边 %d 条；"
            "PPR AUC=%.4f、Adamic-Adar AUC=%.4f、AA Precision@10=%.4f、PPR Precision@10=%.4f。"
            "但需求点名的『用户查询行为/兴趣偏好』在 gkx 中没有任何日志表，"
            "『文献/研究项目/技术方案』三类对象也没有对应的推荐边，无法做个性化排序与在线 A/B，"
            "只能交付机构/专家的图谱关系推荐，故判部分支持。"
            % (st["n_nodes"], st["n_edges"], len(test_edges),
               auc_res["PPR"], auc_res["AA"],
               (sum(prec) / len(prec) if prec else 0),
               (sum(prec_ppr) / len(prec_ppr) if prec_ppr else 0))),
        "caveats": [
            "无用户行为、点击、曝光日志，无法做个性化推荐或 CTR/NDCG 评估；本报告只做离线链接预测。",
            "测试期论文采集强度高于训练期（2024 年单年 32,379 篇，是 2023 年的 4.87 倍），AUC 受时间分布影响。",
            "负样本为随机非边，未做难负样本挖掘，AUC 偏乐观；真实业务的候选集里相似度分布更接近非边。",
            "推荐结果只表示『论文共著可能性』，不表示真实合作意向或商业关系。",
            "训练图按 ≤2020 切分，节点仅覆盖该窗口内 ≥2 篇的机构；2021 年后新出现的机构不进候选集。",
        ],
        "sources": [
            {"file": "code/_snapshots21/a25_paper_panel.json",
             "content": "100,900 篇中文论文（含 author_info_list）",
             "source": "gkx @ 183.240.141.251:3318 / dwd_zh_paper"},
            {"file": "code/_snapshots21/probe_a26_20261022.json",
             "content": "中文被引 20,031 行",
             "source": "gkx @ 183.240.141.251:3318 / dwd_zh_paper_citation"},
        ],
        "elapsed_sec": None,
    }
    used = sorted({p["year"] for p in train_papers})
    out.update(S.base_year_block(
        used, [],
        "训练图用 ≤2020 的全部真实年份（1980—2020 逐年有论文，无补零）；"
        "测试边用 2021—2026 的新增共著对，2026 为残年但只作测试集的一小部分，不进分母。"))
    out["elapsed_sec"] = round(time.time() - t_start, 1)
    S.write_out(MID, out)
    print(json.dumps({"train_graph": st, "test_edges": len(test_edges),
                      "auc": auc_res,
                      "p@10": out["compute"]["precision_at_10"],
                      "r@10": out["compute"]["recall_at_10"],
                      "ppr_p@10": out["compute"]["ppr_precision_at_10"],
                      "hit_aa": out["compute"]["source_hit_rate_aa"]},
                     ensure_ascii=False, indent=1))
    print("elapsed", out["elapsed_sec"], "s")


if __name__ == "__main__":
    main()
