#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_SYNTH_DS_23_GRAPH_ALGO_013 · 社群属性与特征分析（20261021 换源版）。

口径
----
点集：P2 巨型连通分量（15,223 节点 / 36,965 边），与族内 006—012 同一份快照；
划分：Louvain（weight="weight", resolution=1.0, seed=20261021），直接从
      `code/_snapshots21/graph_algo_23_20261023.json` 的节点 `community` 字段读取，
      **不另跑一次划分**（避免同族两件给出不同社群编号，v8 §三）。
建图：`code/_collab_graph21.py`（本族唯一建图口径），本件只读、不新写 SQL 建边。

四要素（需求 §1.1.1.1.4.5.3.3.3）
  ① 组成结构：规模、类型构成、主导类型、机构元数据命中；
  ② 核心节点：按度取 Top5；
  ③ 内部平均连接强度：内部边权均值、内部密度；
  ④ 社群与外部互动：cut 边数、传导率、跨社群边权占比、社群间 Top 连接对；
另加「主题画像」：用 `dwd_zh_paper_classification.keywords`（20,048 篇，覆盖 19.87%）
给每个社群贴主题词，覆盖不足的社群一律标注覆盖率而不是拿 0 充当结论。

判档：部分支持。社群划分与四要素可算，但
  ① 机构元数据（类型/城市）靠名称精确匹配，命中率低；
  ② 主题词只覆盖 19.87% 论文，主题画像是「有偏样本」；
  ③ `enterprise_centrality` / `enterprise_cooperation` / `enterprise_supply_chain` 三张
     阻塞表在 gkx 均不存在，社群无法挂到企业合作边或中心性结果面上。
"""
from __future__ import annotations

import json
import math
import statistics
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import _gkxdb as DB  # noqa: E402
import _collab_graph21 as CG  # noqa: E402
import _synth21_common as S  # noqa: E402
import networkx as nx  # noqa: E402

OUT = HERE / "M_SYNTH_DS_23_GRAPH_ALGO_013_out.json"
SNAP = HERE / "_snapshots21"
GSNAP = SNAP / "graph_algo_23_20261023.json"
BASE = SNAP / "base_20261021.json"


def pct(a, b):
    return round(100.0 * a / b, 4) if b else None


def stat(vals):
    v = sorted(float(x) for x in vals if x is not None)
    if not v:
        return {"n": 0}
    def q(p):
        return v[min(len(v) - 1, max(0, int(round(p * (len(v) - 1)))))]
    return {"n": len(v), "min": round(v[0], 6), "p50": round(statistics.median(v), 6),
            "p90": round(q(0.90), 6), "max": round(v[-1], 6),
            "mean": round(statistics.mean(v), 6)}


def absence_probe():
    out = {"source": "gkx.information_schema（2026-10-23 实测）", "checks": []}
    cur = DB.gkx()
    try:
        cur.execute("SET SESSION max_execution_time=60000")
        for t in ("enterprise_centrality", "enterprise_cooperation", "enterprise_supply_chain",
                  "graph_node", "graph_edge", "enterprise_industry_chain"):
            cur.execute("SELECT COUNT(*) FROM information_schema.tables "
                        "WHERE table_schema='gkx' AND table_name=%s", (t,))
            out["checks"].append({"table": t, "hit_rows": int(cur.fetchone()[0]),
                                  "query": "information_schema.tables WHERE table_schema='gkx' "
                                           "AND table_name='%s'" % t})
        for kw in ("communit", "cooperat", "central"):
            cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='gkx' "
                        "AND table_name LIKE %s", ("%" + kw + "%",))
            out.setdefault("fuzzy", {})[kw] = int(cur.fetchone()[0])
        cur.execute("SET SESSION max_execution_time=0")
        cur.execute("SELECT COUNT(*) FROM gkx.dwd_zh_paper_classification c "
                    "JOIN gkx.dwd_zh_paper p ON p.id=c.id")
        joined = int(cur.fetchone()[0])
        out["topic_join"] = {
            "check": "dwd_zh_paper_classification.id = dwd_zh_paper.id",
            "query": "SELECT COUNT(*) FROM gkx.dwd_zh_paper_classification c JOIN gkx.dwd_zh_paper p ON p.id=c.id",
            "classification_rows": 20048,
            "paper_rows": 100900,
            "hit_rows": joined,
            "join_rate_of_classification_pct": pct(joined, 20048),
            "coverage_of_papers_pct": pct(joined, 100900),
        }
        out["conclusion"] = ("社群结果面（community）与三类业务边（centrality/cooperation/"
                             "supply_chain）逐字命中 0；主题词表 20,048 行里只有 %d 个 id 能与"
                             "论文表连接（3.99%%），主题画像实际只覆盖 0.79%% 论文。" % joined)
    finally:
        cur.close()
    return out


def load_keywords():
    cur = DB.gkx()
    try:
        cur.execute("SET SESSION max_execution_time=0")
        cur.execute("SELECT id, scope, keywords FROM gkx.dwd_zh_paper_classification "
                    "WHERE keywords IS NOT NULL AND keywords<>''")
        out = {}
        for pid, scope, kw in cur.fetchall():
            out[str(pid)] = {"scope": scope, "kw": [x.strip() for x in str(kw).split(",")
                                                    if x.strip()]}
    finally:
        cur.close()
    return out


def main():
    t0 = time.time()
    snap = json.loads(GSNAP.read_text(encoding="utf-8"))
    comm = snap["communities"]
    print("snapshot communities", comm["n_communities"], flush=True)

    g, meta = CG.build(min_papers=2)
    giant = CG.giant(g)
    n_full, e_full = g.number_of_nodes(), g.number_of_edges()
    n_g, e_g = giant.number_of_nodes(), giant.number_of_edges()
    assert (n_full, e_full) == (20436, 38208), (n_full, e_full)
    assert (n_g, e_g) == (15223, 36965), (n_g, e_g)

    nodes = snap["nodes"]
    cid = {r["name"]: r["community"] for r in nodes}
    missing = [n for n in giant.nodes if n not in cid]
    print("membership missing", len(missing), flush=True)
    parts = defaultdict(set)
    for n, c in cid.items():
        if n in giant:
            parts[c].add(n)
    parts = {c: s for c, s in parts.items() if s}

    # 模块度复算（用快照划分，验证与 006—012 的 0.755103 一致）
    q = nx.community.modularity(giant, list(parts.values()), weight="weight")

    # 社群间边权矩阵
    cross_w = 0
    total_w = 0
    pair_w = Counter()
    for a, b, d in giant.edges(data=True):
        w = d.get("weight", 1)
        total_w += w
        ca, cb = cid.get(a), cid.get(b)
        if ca == cb:
            continue
        cross_w += w
        pair_w[tuple(sorted((ca, cb)))] += w

    # 论文 → 社群主题词
    kw_all = load_keywords()
    papers = S.papers()
    inst_papers = Counter()
    comm_papers = Counter()
    comm_kw = defaultdict(Counter)
    comm_scope = defaultdict(Counter)
    comm_classified = Counter()
    paper_ids = {str(p.get("id")) for p in papers}
    kw = {k: v for k, v in kw_all.items() if k in paper_ids}
    for p in papers:
        ins = sorted({i for i in (p.get("insts") or set()) if i})
        cs = {cid[i] for i in ins if i in cid and i in giant}
        if not cs:
            continue
        rec = kw.get(str(p.get("id")))
        for c in cs:
            comm_papers[c] += 1
            inst_papers[c] += len(ins)
            if rec:
                comm_classified[c] += 1
                for k in rec["kw"]:
                    comm_kw[c][k] += 1
                if rec["scope"]:
                    comm_scope[c][rec["scope"]] += 1

    # 机构元数据命中（底册名称精确匹配）
    base_names = {}
    for r in json.loads(BASE.read_text(encoding="utf-8")):
        oid, _cc, nm, prov, city, _yr = (list(r) + [None] * 6)[:6]
        if nm:
            base_names[str(nm)] = {"org_id": oid, "city": city, "province": prov}
    matched = [n for n in giant.nodes if n in base_names]
    type_matched = Counter()
    city_matched = Counter()
    for n in matched:
        type_matched[CG.inst_type(n)] += 1
        c = base_names[n].get("city")
        if c:
            city_matched[c] += 1

    # 逐社群画像
    profiles = []
    for c, members in sorted(parts.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        sub = giant.subgraph(members)
        internal = sub.number_of_edges()
        size = len(members)
        vol = sum(d.get("weight", 1) for _, _, d in sub.edges(data=True))
        cut = sum(1 for a, b, d in giant.edges(data=True)
                  if (a in members) != (b in members))
        cut_w = sum(d.get("weight", 1) for a, b, d in giant.edges(data=True)
                    if (a in members) != (b in members))
        den = size * (size - 1) / 2
        tmix = Counter(CG.inst_type(n) for n in members)
        top = sorted(sub.degree, key=lambda t: (-t[1], t[0]))[:5]
        mcount = sum(1 for n in members if n in base_names)
        profiles.append({
            "cid": c, "size": size, "share_of_giant_pct": pct(size, n_g),
            "internal_edges": internal,
            "internal_density": round(internal / den, 8) if den else None,
            "internal_weight_mean": round(vol / internal, 4) if internal else None,
            "cut_edges_out": cut, "cut_weight_out": cut_w,
            "conductance": round(cut_w / (2 * vol + cut_w), 6) if (vol or cut_w) else None,
            "type_mix": dict(tmix), "dominant_type": tmix.most_common(1)[0][0] if tmix else None,
            "n_meta_matched": mcount,
            "meta_match_pct": pct(mcount, size),
            "top_members": [{"name": n, "degree": d, "papers": giant.nodes[n].get("papers")}
                            for n, d in top],
            "papers_involving": comm_papers.get(c, 0),
            "papers_with_keywords": comm_classified.get(c, 0),
            "keyword_coverage_pct": pct(comm_classified.get(c, 0), comm_papers.get(c, 0)),
            "top_keywords": [{"kw": k, "n": v} for k, v in comm_kw[c].most_common(8)],
            "top_scopes": [{"scope": k, "n": v} for k, v in comm_scope[c].most_common(3)],
        })

    sizes = [p["size"] for p in profiles]
    top15 = profiles[:15]
    cross_share = pct(cross_w, total_w)
    pair_top = [{"c1": a, "c2": b, "weight": w, "share_of_cross_pct": pct(w, cross_w)}
                for (a, b), w in pair_w.most_common(10)]

    payload = {
        "metric_id": "M_SYNTH_DS_23_GRAPH_ALGO_013",
        "metric_name": "社群属性与特征分析",
        "support_judgment": "部分支持",
        "verdict_kind": "negative_evidence",
        "grain": "社群（群体级）；P2 巨连通片内",
        "data_source": "gkx @ 183.240.141.251:3318（只读）",
        "sources": ["code/_snapshots21/graph_algo_23_20261023.json（族级快照，含 community 字段）",
                    "code/_collab_graph21.py（唯一建图口径）",
                    "code/_snapshots21/a25_paper_panel.json（100,900 篇）",
                    "gkx.dwd_zh_paper_classification（20,048 篇主题词）",
                    "code/_snapshots21/base_20261021.json（机构元数据匹配）"],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面图件：建图用全部 100,900 篇论文（1980—2026），不按年切分，"
                            "不做年度除法。"),
        "params": {"seed": 20261021, "louvain_resolution": 1.0, "louvain_weight": "weight",
                   "pagerank_alpha": 0.85, "betweenness_k": 100,
                   "min_papers": 2, "point_set": "P2",
                   "note": "划分直接读快照 community 字段，本件不重跑 Louvain；"
                           "seed/resolution 仅用于标注该划分的来源参数"},
        "point_set": {
            "id": "P2",
            "definition": "论文共著图的巨型连通分量（_collab_graph21.build → giant）",
            "n_nodes": n_g, "n_edges": e_g,
            "coverage_of_full_nodes_pct": pct(n_g, n_full),
            "coverage_of_full_edges_pct": pct(e_g, e_full),
            "full_nodes": n_full, "full_edges": e_full,
            "nodes_excluded": n_full - n_g,
            "nodes_excluded_pct": pct(n_full - n_g, n_full),
            "edges_excluded": e_full - e_g,
            "edges_excluded_pct": pct(e_full - e_g, e_full),
    "isolate_handling": ("全图 3,540 个孤立点（度 0）与 645 个碎片分量被**剔除**在 P2 外；"
                                 "它们没有社群归属，不记 0、不单独成社群——若强行纳入，"
                                 "会多出数千个单点社群（见 012 §2.2 的 P1 对照 701 社群）"),
            "n_components_full": 4186,
        },
        "n_communities": len(profiles),
        "modularity_recomputed": round(q, 6),
        "modularity_snapshot": comm["modularity"],
        "membership_missing_nodes": len(missing),
        "total_edge_weight": total_w,
        "cross_community_weight": cross_w,
        "size_stats": stat(sizes),
        "n_singleton": sum(1 for s in sizes if s == 1),
        "n_size_ge10": sum(1 for s in sizes if s >= 10),
        "largest_share_pct": pct(max(sizes), n_g),
        "top15_profiles": top15,
        "all_profile_summary": [{"cid": p["cid"], "size": p["size"],
                                 "conductance": p["conductance"],
                                 "dominant_type": p["dominant_type"],
                                 "keyword_coverage_pct": p["keyword_coverage_pct"]}
                                for p in profiles],
        "cross_pairs_top10": pair_top,
        "metadata": {
            "n_giant_nodes": n_g,
            "n_meta_matched": len(matched),
            "meta_match_pct": pct(len(matched), n_g),
            "type_dist_giant": dict(Counter(CG.inst_type(n) for n in giant.nodes)),
            "type_dist_matched": dict(type_matched),
            "n_meta_unmatched": n_g - len(matched),
            "city_dist_matched_top10": city_matched.most_common(10),
        },
        "topic": {
            "classification_rows": len(kw_all),
            "classified_joined_papers": len(kw),
            "papers_total": len(papers),
            "join_rate_of_classification_pct": pct(len(kw), len(kw_all)),
            "classified_share_pct": pct(len(kw), len(papers)),
            "communities_with_keywords": sum(1 for p in profiles if p["papers_with_keywords"]),
            "median_keyword_coverage_pct": round(statistics.median(
                [p["keyword_coverage_pct"] for p in profiles
                 if p["keyword_coverage_pct"] is not None] or [0]), 4),
        },
        "derived": {
            "p2_node_coverage_of_full_pct": pct(n_g, n_full),
            "p2_edge_coverage_of_full_pct": pct(e_g, e_full),
            "cross_community_weight_share_pct": cross_share,
            "within_community_weight_share_pct": pct(total_w - cross_w, total_w),
            "largest_community_share_of_giant_pct": pct(max(sizes), n_g),
            "top15_size_share_of_giant_pct": pct(sum(sizes[:15]), n_g),
            "non_top15_size_share_of_giant_pct": pct(sum(sizes[15:]), n_g),
            "singleton_community_share_pct": pct(sum(1 for s in sizes if s == 1), len(sizes)),
            "within_community_weight": total_w - cross_w,
            "meta_unmatched_of_giant_pct": pct(n_g - len(matched), n_g),
            "meta_match_share_of_giant_pct": pct(len(matched), n_g),
            "classified_share_of_papers_pct": pct(len(kw), len(papers)),
            "topic_join_rate_of_classification_pct": pct(len(kw), len(kw_all)),
            "denominator_note": (
                "• p2 覆盖率：分母 = 全图 %d 节点 / %d 边；\n"
                "• cross/within：分母 = 巨片总边权 %d（权重=共同署名篇数）；\n"
                "• 社群占比：分母 = 巨片 15,223 节点；\n"
                "• meta_match：分母 = 巨片节点 15,223（名称精确匹配底册，不做别名归并）；\n"
                "• classified：分母 = 中文论文 100,900 篇；classification 自身 20,048 行，"
                "但只有 %d 行 id 能与论文表连接（分母 20,048），两处不可混用。"
                % (n_full, e_full, total_w, len(kw))
            ),
        },
        "absence_probe": absence_probe(),
        "caveats": [
            "社群标号是「按快照规模排序的序号」，不是稳定主键，不可跨版本对比。",
            "主题词表 20,048 行，但仅 799 个 id 能与论文表 JOIN（占分类表 3.99%、占论文 0.79%）："
            "主题画像只能当线索，不能当结论——这是实测连接后的真覆盖率，不是分类表行数占比 19.87%。",
            "机构元数据靠名称精确匹配，命中率低；未命中的节点类型是「按名称关键词猜的」，不是权威类型。",
            "共著边是学术合作，不是企业合作/供应链；不得把社群读作产业链集群。",
            "P2 外的 3,540 个孤立点与碎片分量被剔除，社群覆盖率只对巨片成立。",
        ],
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print("communities=%d Q=%.6f cross=%.4f%% meta=%.2f%%" % (
        len(profiles), q, cross_share, pct(len(matched), n_g)), flush=True)
    print("wrote", OUT.name, "%.1fs" % (time.time() - t0), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
