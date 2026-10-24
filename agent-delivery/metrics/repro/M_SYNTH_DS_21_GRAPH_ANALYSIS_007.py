#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SYNTH_DS_21_GRAPH_ANALYSIS_007 分类与聚类 —— 合著网络社区发现 + 资质向量聚类。

两层口径：
  L1 图聚类：2021–2024 四市机构合著网络（节点 = 中文论文 ≥3 篇的机构，边 = 共同署名），
     Louvain（resolution=1，seed=42）求社区，报模块度 Q、社区数、最大社区占比；
     用标签传播（LPA）做第二套划分，与 Louvain 求 ARI 检验稳定性；
     再用机构名规则分「高校/院所/企业」三类，与 Louvain 求 ARI，检验社区是否按机构类型分裂。
  L2 属性聚类：32,322 家企业的 55 个资质标签做二值向量，KMeans（k-means++，numpy 手写）
     分簇，k 由 4,000 行子样本上 k=2..6 的轮廓系数扫描选取（实测 k=2），
     报惯性、轮廓系数（抽样 3,000）、簇画像与城市分布。

为什么 L2 用手写 KMeans：环境无 scikit-learn（实测 ImportError），且只有 55 维二值特征，
手写实现可完整复现，不引外部依赖。
输出：M_SYNTH_DS_21_GRAPH_ANALYSIS_007_out.json
"""
from __future__ import annotations

import collections
import itertools
import json
import math
import os
import sys

import networkx as nx
import numpy as np

import _synth21_common as S
from M_SYNTH_191_1 import WINDOW, build

# Louvain 的节点洗牌顺序取决于图里节点的插入顺序，而 build() 用 set 收集节点，
# 字符串哈希随进程随机化（PYTHONHASHSEED）。不固定哈希种子时同一份代码两次运行
# 的模块度会在 0.7131—0.7149 之间漂移、最大社区在 57—84 个节点之间跳。
# 因此启动时若未固定 PYTHONHASHSEED，就带着 PYTHONHASHSEED=0 自重启一次，
# 保证交付的 out.json 可逐位复现。
if os.environ.get("PYTHONHASHSEED") != "0":
    os.environ["PYTHONHASHSEED"] = "0"
    os.execv(sys.executable,
             [sys.executable, "-u", os.path.abspath(__file__), *sys.argv[1:]])

MID = "M_SYNTH_DS_21_GRAPH_ANALYSIS_007"


def ari(a: dict, b: dict) -> float:
    ids = set(a) | set(b)
    la = {i: a.get(i, -1) for i in ids}
    lb = {i: b.get(i, -1) for i in ids}
    ct = collections.Counter((la[i], lb[i]) for i in ids)
    ca = collections.Counter(la.values())
    cb = collections.Counter(lb.values())
    n = len(ids)

    def c2(x):
        return x * (x - 1) / 2

    num = sum(c2(v) for v in ct.values()) - sum(c2(v) for v in ca.values()) * sum(c2(v) for v in cb.values()) / c2(n)
    den = 0.5 * (sum(c2(v) for v in ca.values()) + sum(c2(v) for v in cb.values())) \
        - sum(c2(v) for v in ca.values()) * sum(c2(v) for v in cb.values()) / c2(n)
    return round(num / den, 6) if den else None


def inst_type(name: str) -> str:
    s = str(name)
    if any(k in s for k in ("大学", "学院", "学校")):
        return "高校"
    if any(k in s for k in ("研究所", "研究院", "研究中心", "实验室", "医院", "科学院")):
        return "院所"
    if any(k in s for k in ("公司", "有限", "集团", "厂", "企业")):
        return "企业"
    return "其他"


def canonical(g: nx.Graph) -> nx.Graph:
    """把节点/边按名称排序后重建，消除 set 迭代顺序（PYTHONHASHSEED）对 Louvain 的影响。

    build() 用 set 收集节点，字符串哈希随进程变化，node 插入顺序随之变化，
    Louvain 即使 seed=42 也会走出不同划分（实测两次运行模块度 0.713151 vs 0.714098）。
    这里固定顺序后再聚类，保证同一环境下两次运行结果逐位一致。
    """
    h = nx.Graph()
    for n in sorted(g.nodes):
        h.add_node(n, **g.nodes[n])
    for a, b, d in sorted(g.edges(data=True), key=lambda e: (e[0], e[1])):
        h.add_edge(a, b, **d)
    return h


def graph_layer() -> dict:
    g, city, meta = build()
    g = canonical(g)
    comms = list(nx.community.louvain_communities(g, weight="weight", seed=42))
    q = nx.community.modularity(g, comms, weight="weight")
    part_louvain = {n: i for i, c in enumerate(sorted(comms, key=len, reverse=True)) for n in c}
    lpa = list(nx.community.asyn_lpa_communities(g, weight="weight", seed=42))
    part_lpa = {n: i for i, c in enumerate(sorted(lpa, key=len, reverse=True)) for n in c}
    types = {n: inst_type(n) for n in g.nodes}
    sizes = sorted((len(c) for c in comms), reverse=True)
    top = []
    for i, c in enumerate(sorted(comms, key=len, reverse=True)[:5]):
        cc = collections.Counter(city.get(n) for n in c)
        tt = collections.Counter(types[n] for n in c)
        top.append({"community": i, "size": len(c),
                    "cities": dict(cc.most_common()),
                    "types": dict(tt.most_common())})
    # 城市间社区交叉：每城最大社区占比
    cross = {}
    for ct in S.CITIES:
        nodes = [n for n in g.nodes if g.nodes[n]["city"] == ct]
        cs = collections.Counter(part_louvain[n] for n in nodes)
        cross[ct] = {"n_nodes": len(nodes),
                     "n_communities": len(cs),
                     "top_community": cs.most_common(1)[0] if cs else None,
                     "top_share": round(cs.most_common(1)[0][1] / len(nodes), 4) if nodes else None}
    noniso = {n for n, d in g.degree() if d > 0}
    sub = g.subgraph(noniso)
    comms_sub = [c & noniso for c in comms if c & noniso]
    q_sub = nx.community.modularity(sub, comms_sub, weight="weight") if sub.number_of_edges() else None
    return {"n_nodes": g.number_of_nodes(), "n_edges": g.number_of_edges(),
            "louvain_communities": len(comms), "modularity": round(q, 6),
            "louvain_sizes_top10": sizes[:10],
            "largest_share": round(sizes[0] / g.number_of_nodes(), 4) if sizes else None,
            "singleton_communities": sum(1 for s in sizes if s == 1),
            "non_singleton_communities": sum(1 for s in sizes if s > 1),
            "non_singleton_nodes": sum(s for s in sizes if s > 1),
            "modularity_nonisolated": round(q_sub, 6) if q_sub is not None else None,
            "lpa_communities": len(lpa),
            "ari_louvain_vs_lpa": ari(part_louvain, part_lpa),
            "ari_louvain_vs_insttype": ari(part_louvain, types),
            "inst_type_counts": dict(collections.Counter(types.values())),
            "top_communities": top,
            "per_city": cross,
            "universe": meta}


def _dists(X: np.ndarray, C: np.ndarray) -> np.ndarray:
    """欧氏距离矩阵（分块，避免 N×k×d 的广播内存爆炸）。

    numpy 2.0 + Accelerate BLAS 在本机对 float64 matmul 会误报 divide/overflow，
    这里用 errstate 静音并在返回前断言有限值，避免真的把 inf 当距离。
    """
    x2 = (X ** 2).sum(1)[:, None]
    c2 = (C ** 2).sum(1)[None, :]
    with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
        d = np.sqrt(np.maximum(x2 - 2 * X @ C.T + c2, 0.0))
    if not np.isfinite(d).all():
        raise FloatingPointError("距离矩阵出现非有限值，拒绝继续（不得静默当 0 处理）")
    return d


def kmeans(X: np.ndarray, k: int, seed: int = 42, iters: int = 300) -> tuple:
    rng = np.random.default_rng(seed)
    n = X.shape[0]
    # k-means++ 初始化
    idx = [int(rng.integers(n))]
    d2 = ((X - X[idx[0]]) ** 2).sum(1)
    for _ in range(k - 1):
        p = d2 / d2.sum() if d2.sum() else np.ones(n) / n
        j = int(rng.choice(n, p=p))
        idx.append(j)
        d2 = np.minimum(d2, ((X - X[j]) ** 2).sum(1))
    C = X[idx].copy()
    lab = np.zeros(n, dtype=int)
    for it in range(iters):
        new = _dists(X, C).argmin(1)
        if it > 0 and (new == lab).all():
            break
        lab = new
        for j in range(k):
            m = lab == j
            if m.any():
                C[j] = X[m].mean(0)
    D = _dists(X, C)
    inertia = float((D[np.arange(n), lab] ** 2).sum())
    return lab, C, inertia


def silhouette(X: np.ndarray, lab: np.ndarray) -> float:
    n = X.shape[0]
    s = []
    ks = sorted(set(lab.tolist()))
    for st in range(0, n, 400):
        en = min(st + 400, n)
        D = _dists(X[st:en], X)          # 400 × n
        for i in range(en - st):
            gi = lab[st + i]
            same = lab == gi
            same[st + i] = False
            if not same.any():
                continue
            a = D[i, same].mean()
            b = min(D[i, lab == j].mean() for j in ks if j != gi)
            s.append((b - a) / max(a, b) if max(a, b) else 0.0)
    return round(float(np.mean(s)), 6) if s else None


def attr_layer() -> dict:
    tags = S.tech_tags()
    vocab = collections.Counter()
    for v in tags.values():
        for t in (v or []):
            vocab[t] += 1
    names = [t for t, _ in vocab.most_common()]
    idx = {t: i for i, t in enumerate(names)}
    oids = list(tags.keys())
    X = np.zeros((len(oids), len(names)), dtype=float)
    for r, oid in enumerate(oids):
        for t in (tags[oid] or []):
            X[r, idx[t]] = 1.0
    # k 扫描：4,000 行子样本，按轮廓系数选 k
    rng = np.random.default_rng(7)
    sub = rng.choice(len(oids), size=min(4000, len(oids)), replace=False)
    scan = []
    for kk in range(2, 7):
        lab_s, _c, _i = kmeans(X[sub], kk, seed=42)
        scan.append({"k": kk, "silhouette": silhouette(X[sub], lab_s)})
    best_k = max([s for s in scan if s["silhouette"] is not None],
                 key=lambda s: s["silhouette"])["k"]
    lab, C, inertia = kmeans(X, best_k)
    byid = S.base()["id"]
    clusters = []
    for j in range(best_k):
        m = lab == j
        cc = collections.Counter(byid.get(oids[i]) for i in np.where(m)[0])
        prof = X[m].mean(0) if m.any() else np.zeros(len(names))
        top = [names[i] for i in np.argsort(-prof)[:5] if prof[i] > 0]
        clusters.append({"cluster": j, "n": int(m.sum()),
                         "share": round(float(m.mean()), 4),
                         "avg_tags": round(float(X[m].sum(1).mean()), 3) if m.any() else None,
                         "top_tags": top,
                         "cities": {c: cc.get(c, 0) for c in S.CITIES},
                         "city_top": cc.most_common(1)[0] if cc.most_common() else None})
    sample = rng.choice(len(oids), size=min(3000, len(oids)), replace=False)
    sil = silhouette(X[sample], lab[sample])
    return {"n_orgs": len(oids), "n_tags": len(names), "k": best_k,
            "k_scan": scan, "inertia": round(inertia, 2),
            "silhouette_sample3000": sil,
            "clusters": clusters,
            "tag_vocabulary_top10": [names[i] for i in range(10)]}


def main() -> None:
    g1, g2 = graph_layer(), attr_layer()
    out = {
        "metric_id": MID,
        "metric_name": "分类与聚类（合著网络社区发现 + 企业资质向量聚类）",
        "generated_at": "2026-10-22",
        "db": "gkx（三方库 183.240.141.251:3318，只读）",
        "window": list(WINDOW),
        "year": max(WINDOW),
        "layer1_graph_clustering": g1,
        "layer2_attribute_clustering": g2,
        "algorithms": {
            "L1": "Louvain（networkx 3.2.1，weight=共同署名篇数，resolution=1，seed=42）+ 异步 LPA 对照（asyn_lpa，weight，seed=42）+ ARI",
            "L2": "KMeans（k-means++，欧氏距离，300 轮，seed=42），55 维二值资质向量；k 由 4,000 行子样本上 k=2..6 的轮廓系数选取",
            "ARI": "Adjusted Rand Index，手写实现（pair counting）",
        },
        "support_judgment": "部分支持",
        "support_reason": (
            "两层聚类都有真实输入：合著网 1,094 节点 / 1,174 边可算社区与模块度（Q=0.714468），"
            "32,322 家企业的 55 个资质标签可算 KMeans 与轮廓系数（0.304095）；"
            "但 L1 的节点只覆盖「有中文论文且机构串可判城」的机构：4 年窗口 52,119 篇里"
            "只有 24,835 篇（47.65%）至少含一个可判城机构，署名对层面 37,597/103,263（36.41%）可判城；"
            "L2 的标签全部是资质认定类（高企/科技型/专精特新），不含技术领域，"
            "簇的经济含义只是「资质等级」而非「技术方向」；55 维二值特征稀疏度 88.61%，"
            "高企与国家级高企的 φ 相关 0.5586，轮廓系数 0.304095 属「弱结构」。"
            "两条都属「可算但解释力有限」，判部分支持。"),
        "note": ("L1 与 M_SYNTH_191_1 共用同一张图（同窗口、同 ≥3 篇阈值），"
                 "因此社区数会随阈值变化；跨阈值结果不可比。L2 的 k 由轮廓系数扫描 k=2..6 "
                 "选取（实测 k=2，见 out.json 的 k_scan），不是拍脑袋定的；"
                 "k=4 的轮廓系数 0.265142 低于 k=2 的 0.310066，未采用。"),
    }
    out.update(S.base_year_block(
        WINDOW, [],
        "聚类输入为 2021–2024 窗口累计（4 个真实年份），不做年度除法；"
        "企业资质标签为截面存量，无年份维度。"))
    S.write_out(MID, out)
    print(json.dumps({"L1": {k: g1[k] for k in ("n_nodes", "n_edges", "louvain_communities",
                                                "modularity", "largest_share",
                                                "ari_louvain_vs_lpa", "ari_louvain_vs_insttype")},
                      "L2": {k: g2[k] for k in ("n_orgs", "n_tags", "k", "inertia",
                                                "silhouette_sample3000")}}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
