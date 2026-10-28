#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_FACTOR_EDGE_WEIGHT · 要素间影响程度（20261021 换源版）

旧稿公式（照抄，seed 未签字）
----------------------------
边权 = 共现/关联次数；辅以关联强度 AS 与 Jaccard 归一；
节点影响力 = 加权度归一到 0—100；技术点另用共现加权 PageRank（阻尼 0.85）。

换源后的五类边（全部来自 gkx 快照，零外部造数）
----------------------------------------------
  E1 机构—专利：`collab_inputs21.json` 的 dwd_patent_applicants（28,964 行 / 20,000 pn）
  E2 机构—论文：`factor_authors_20261021.json` 的 institution—paper_id（62,002 行）
  E3 学者—论文：同表的 zh_name—paper_id
  E4 学者—学者：同一 paper_id 上的作者两两配对，权重 = 合作论文数
  E6 技术点—技术点：`patent_ipc4_by_name_20261021.json` 的机构—IPC4 计数，
     同一机构涉猎的 IPC4 两两配对（**机构组合层面**，不是同件专利共类）

覆盖缺口（写进 support_judgment，不掩盖）
----------------------------------------
- E1 只覆盖 20,000 个 pn（主表 2,939,895 件的 0.68%），边权是样本口径；
- E2/E3/E4 只覆盖 dwd_zh_author 的 62,002 行，不是全部论文；
- E6 没有「单件专利的 IPC 列表」，只能做机构组合共现，不能做同专利共类；
- 学者按姓名聚合，存在同名合并（王伟等），不是 ORCID 级身份。

输出：`code/M_INNOV_FACTOR_EDGE_WEIGHT_out.json`
"""
from __future__ import annotations

import json
import math
import statistics
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
AUTH = SNAP / "factor_authors_20261021.json"
APPL = SNAP / "collab_inputs21.json"
IPC = SNAP / "patent_ipc4_by_name_20261021.json"
OUT = HERE / "M_INNOV_FACTOR_EDGE_WEIGHT_out.json"
METRIC = "M_INNOV_FACTOR_EDGE_WEIGHT"
NAME = "要素间影响程度"


def wstats(weights):
    if not weights:
        return {"n_edges": 0}
    s = sorted(weights)
    n = len(s)
    q = lambda p: s[min(n - 1, int(p * (n - 1)))]
    return {"n_edges": n, "min": s[0], "p50": q(0.5), "p90": q(0.9),
            "p99": q(0.99), "max": s[-1], "mean": round(sum(s) / n, 4),
            "sum": sum(s)}


def top_nodes(deg, names=None, k=10):
    out = []
    mx = max(deg.values()) if deg else 1
    for node, w in sorted(deg.items(), key=lambda kv: -kv[1])[:k]:
        out.append({"node": node, "name": (names or {}).get(node, ""),
                    "weighted_degree": w, "score_0_100": round(100.0 * w / mx, 2)})
    return out


def pagerank(edges, damping=0.85, iters=40):
    """edges: {(a,b): w} 无向按双向累权。"""
    nodes = sorted({x for e in edges for x in e})
    idx = {n: i for i, n in enumerate(nodes)}
    n = len(nodes)
    out = [0.0] * n
    adj = [[] for _ in range(n)]
    for (a, b), w in edges.items():
        i, j = idx[a], idx[b]
        out[i] += w
        out[j] += w
        adj[i].append((j, w))
        adj[j].append((i, w))
    pr = [1.0 / n] * n
    for _ in range(iters):
        nxt = [(1 - damping) / n] * n
        for i in range(n):
            if out[i] <= 0:
                continue
            share = damping * pr[i] / out[i]
            for j, w in adj[i]:
                nxt[j] += share * w
        pr = nxt
    return {nodes[i]: pr[i] for i in range(n)}


def main() -> None:
    auth = json.loads(AUTH.read_text(encoding="utf-8"))
    appl = json.loads(APPL.read_text(encoding="utf-8"))
    ipc = json.loads(IPC.read_text(encoding="utf-8"))

    # E1 机构—专利
    e1 = defaultdict(int)
    for pn, name in appl["patent_applicants"]:
        if pn and name:
            e1[(name, pn)] += 1
    # E2 机构—论文 / E3 学者—论文
    e2, e3 = defaultdict(int), defaultdict(int)
    paper_authors = defaultdict(set)
    for pid, author, inst in auth["rows"]:
        e3[(author, pid)] += 1
        if inst:
            e2[(inst, pid)] = 1
        paper_authors[pid].add(author)
    # E4 学者—学者（同一论文两两配对）
    e4 = Counter()
    for pid, authors in paper_authors.items():
        if 2 <= len(authors) <= 30:
            for a, b in combinations(sorted(authors), 2):
                e4[(a, b)] += 1
    # E6 IPC 共现（机构组合层）
    org_ipc = defaultdict(Counter)
    for code, org, cnt in ipc:
        if code and org:
            org_ipc[org][code] += int(cnt)
    e6 = Counter()
    orgs_used = 0
    for org, cc in org_ipc.items():
        codes = [c for c, _ in cc.most_common(8)]
        if 2 <= len(codes) <= 8:
            orgs_used += 1
            for a, b in combinations(sorted(codes), 2):
                e6[(a, b)] += 1

    d1, d2, d3, d4, d6 = (defaultdict(int) for _ in range(5))
    for (a, b), w in e1.items():
        d1[a] += w
    for (a, b), w in e2.items():
        d2[a] += w
    for (a, b), w in e3.items():
        d3[a] += w
    for (a, b), w in e4.items():
        d4[a] += w
        d4[b] += w
    for (a, b), w in e6.items():
        d6[a] += w
        d6[b] += w

    pr = pagerank(e6)
    pr_top = sorted(pr.items(), key=lambda kv: -kv[1])[:10]
    pr_sum = sum(pr.values())

    def sample(edges, k=10):
        return [[a, b, w] for (a, b), w in sorted(edges.items(), key=lambda kv: -kv[1])[:k]]

    report = {
        "metric_id": METRIC,
        "metric_name": NAME,
        "date": "2026-10-22",
        "data_source": (
            "gkx @ 183.240.141.251:3318（只读）：dwd_patent_applicants / dwd_zh_author / "
            "dwd_patent（IPC 快照）；零 demo、零造数关系表"
        ),
        "formula": (
            "edge_weight=共现次数；node_influence=100×weighted_degree/max(type)；"
            "E6 另做 damping=0.85 的加权 PageRank，∑PR=1"
        ),
        "probes": {
            "author_rows": len(auth["rows"]),
            "author_papers": len(paper_authors),
            "author_names": len({r[1] for r in auth["rows"]}),
            "author_insts": len({r[2] for r in auth["rows"] if r[2]}),
            "applicant_rows": len(appl["patent_applicants"]),
            "applicant_pns": len({r[0] for r in appl["patent_applicants"]}),
            "ipc_org_rows": len(ipc),
            "ipc_orgs_with_2_8": orgs_used,
            "patent_total_rows": 2939895,
            "e1_pn_coverage_pct": round(100.0 * len({r[0] for r in appl["patent_applicants"]}) / 2939895, 4),
        },
        "edges": {
            "E1_org_patent": {"stats": wstats(list(e1.values())), "top": sample(e1),
                              "n_nodes_org": len(d1), "top_org": top_nodes(d1),
                              "weight_semantics": "1 件专利 1 条边；样本 20,000 pn"},
            "E2_org_paper": {"stats": wstats(list(e2.values())), "top": sample(e2),
                             "n_nodes_org": len(d2), "top_org": top_nodes(d2),
                             "weight_semantics": "机构—论文二值边（同一机构多作者去重）；节点加权度=论文数"},
            "E3_scholar_paper": {"stats": wstats(list(e3.values())), "top": sample(e3),
                                 "n_nodes_scholar": len(d3), "top_scholar": top_nodes(d3),
                                 "weight_semantics": "1 篇论文 1 条边；姓名聚合"},
            "E4_scholar_scholar": {"stats": wstats(list(e4.values())), "top": sample(e4),
                                   "n_nodes_scholar": len(d4), "top_scholar": top_nodes(d4),
                                   "weight_semantics": "合作论文篇数；无向边"},
            "E6_ipc_ipc": {"stats": wstats(list(e6.values())), "top": sample(e6),
                           "n_nodes_ipc": len(d6), "top_ipc": top_nodes(d6),
                           "weight_semantics": "同时涉猎两 IPC4 的机构数（机构组合层）"},
        },
        "pagerank_E6": {
            "damping": 0.85, "iterations": 40, "pr_sum": round(pr_sum, 8),
            "top": [[k, round(v, 6)] for k, v in pr_top],
        },
        "normalization": {
            "node_score": "同型内 100×加权度/最大值；不可跨型比较",
            "as_jaccard": "本件未强制 AS/Jaccard：E1/E2/E3 是二部图计数，Jaccard 分母（共同邻居）无业务含义；E4 用原始合作篇数",
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": (
                f"五类边全部可算，且 PageRank ∑PR={round(pr_sum,8)} 自洽；"
                f"但 E1 只覆盖 {len({r[0] for r in appl['patent_applicants']}):,} 个 pn"
                f"（主表 2,939,895 件的 {round(100.0*len({r[0] for r in appl['patent_applicants']})/2939895,4)}%），"
                f"边权是 0.68% 样本；E2/E3/E4 只覆盖 {len(auth['rows']):,} 行作者记录、"
                f"{len(paper_authors):,} 篇论文，不是全部论文；"
                f"E6 没有单件专利的 IPC 列表，只能做机构组合共现（{orgs_used:,} 家机构），"
                "不是同专利共类；学者按姓名聚合，存在同名合并。"
                "结构与算法闭环成立，但四个覆盖缺口使边权不能当全量真值，故判部分支持。"
            ),
            "criteria": {
                "edge_types_computed": 5,
                "e1_pn_coverage_pct": round(100.0 * len({r[0] for r in appl["patent_applicants"]}) / 2939895, 4),
                "e2_e3_rows": len(auth["rows"]),
                "e6_patent_level": False,
                "scholar_identity": "name_only",
                "pagerank_sum": round(pr_sum, 8),
            },
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "本指标是截面图结构：边权由当前快照的共现计数一次算出，公式与产物均无年度键；"
            "used/missing 为空表示无年度基期，不是「缺年按 0 摊入」。"
        ),
        "sources": [
            {"path": "code/_snapshots21/factor_authors_20261021.json", "table": "gkx.dwd_zh_author",
             "rows": len(auth["rows"]), "role": "论文—作者—机构"},
            {"path": "code/_snapshots21/collab_inputs21.json", "table": "gkx.dwd_patent_applicants",
             "rows": len(appl["patent_applicants"]), "role": "机构—专利（20,000 pn 样本）"},
            {"path": "code/_snapshots21/patent_ipc4_by_name_20261021.json", "table": "gkx.dwd_patent",
             "rows": len(ipc), "role": "机构—IPC4 计数"},
        ],
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, v in report["edges"].items():
        print(k, v["stats"])
    print("pagerank sum", pr_sum, "top", pr_top[:3])
    print("wrote", OUT)


if __name__ == "__main__":
    main()
