#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""要素聚类（M_INNOV_FACTOR_CLUSTER）——A-16 批实现。

口径（metrics/calc-logic/INNOV/M_INNOV_FACTOR_CLUSTER.md）：
  对会议、项目（含课题）、专利、期刊四类要素，用各自影响力得分做无监督分簇；
  输出簇标签与簇规模，不是 0—100 分。
  特征 = 类型独热 + 影响力分；样本 ≥30 用 K-Means（K=2..8 取最大轮廓），5—29 用层次聚类。

落地实况（决定了判档）：
  项目 58,453 项、专利 20,000 件（被引表去重 pn）、期刊 3,401 种 —— 三类有影响力分；
  **会议 0 条**：gkx 里 `dwd_zh_paper.publication_type` 与 `dwd_zh_journal.publication_type`
  全表只有「期刊」，`dwd_en_journal` 只有 Journal/Book/Book in series，没有任何会议实体表。
  所以特征是「3 类独热 + 影响力」，不是口径写的 4 类。

算法全部本地实现（不依赖 sklearn，本机未装）：
  K-Means：k-means++ 初始化、固定随机种子、多起点取最小惯量；
  轮廓系数：在分层随机样本上算（全量 8 万点做 O(n²) 不现实，样本量如实披露）；
  层次聚类：scipy Ward，仅当 5 ≤ n ≤ 29 时触发（本批未触发，保留分支并说明）。

产物：code/M_INNOV_FACTOR_CLUSTER_out.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import _gkxdb
from _innov_gkx21_common import write_out

METRIC = "M_INNOV_FACTOR_CLUSTER"
SEED = 42
SIL_SAMPLE = 1500


def q(sql):
    cur = _gkxdb.gkx()
    try:
        cur.execute("SET SESSION max_execution_time=120000")
        cur.execute(sql)
        return cur.fetchall()
    finally:
        cur.close()


def norm01(v):
    v = np.asarray(v, dtype=float)
    lo, hi = np.nanmin(v), np.nanmax(v)
    if hi <= lo:
        return np.full_like(v, 0.5)
    return (v - lo) / (hi - lo)


# ------------------------------------------------------------------ 取数
def load_elements():
    """返回三类要素的影响力分（0—100）与样本元信息。"""
    # 项目：资助金额 0.5 + 结题摘要 0.5（与 M_INNOV_PROJECT_INFLUENCE 同构，等权缺测不补）
    rows = q("SELECT funded_amount, "
             "CASE WHEN final_report_abstract IS NOT NULL AND final_report_abstract<>'' "
             "THEN 1 ELSE 0 END AS done FROM gkx.dwd_zh_project")
    amt = np.array([float(r[0]) for r in rows if r[0] is not None])
    done = np.array([float(r[1]) for r in rows if r[0] is not None])
    proj_score = 100.0 * (0.5 * norm01(amt) + 0.5 * done)

    # 专利：被引次数（0.8）+ 专利价值缺失（0.2 缺测，重归一后即纯被引）
    rows = q("SELECT pn, cited_by_nums FROM gkx.dwd_patent_cited")
    best = {}
    for pn, cb in rows:
        if pn is None:
            continue
        v = float(cb or 0)
        if pn not in best or v > best[pn]:
            best[pn] = v
    pn_list = list(best.keys())
    cb = np.array([best[p] for p in pn_list], dtype=float)
    pat_score = 100.0 * norm01(cb)

    # 期刊：累计被引 0.5 + 篇均被引 0.5（影响因子列整列为空，不能当影响力分）
    rows = q("SELECT cite_nums, paper_nums FROM gkx.dwd_zh_journal")
    cite = np.array([float(r[0] or 0) for r in rows])
    pap = np.array([float(r[1] or 1) for r in rows])
    per = cite / np.where(pap > 0, pap, 1)
    zh_score = 100.0 * (0.5 * norm01(cite) + 0.5 * norm01(per))

    rows = q("SELECT paper_nums, citation_rate FROM gkx.dwd_en_journal")
    ep = np.array([float(r[0] or 0) for r in rows])
    ec = np.array([float(r[1] or 0) for r in rows])
    # 英文刊 citation_rate 全 0，只剩 paper_nums 一维，单独成类会与中文刊混为一谈 → 只作伴生统计
    en_note = {
        "n": int(len(rows)),
        "paper_nums_min": float(ep.min()) if len(ep) else None,
        "paper_nums_max": float(ep.max()) if len(ep) else None,
        "citation_rate_nonzero": int((ec > 0).sum()),
    }
    return {
        "project": {"score": proj_score, "n": int(len(proj_score))},
        "patent": {"score": pat_score, "n": int(len(pat_score))},
        "journal": {"score": zh_score, "n": int(len(zh_score))},
        "en_journal_note": en_note,
        "conference": {"n": 0,
                       "why": "publication_type 全表只有「期刊」；无会议实体表"},
    }


# ------------------------------------------------------------------ K-Means
def kmeans(X, k, rng, n_init=8, max_iter=100, tol=1e-6):
    n, d = X.shape
    best = None
    for _ in range(n_init):
        # k-means++ 初始化
        centers = [X[rng.integers(n)]]
        for _ in range(1, k):
            d2 = np.min(((X[:, None, :] - np.array(centers)[None, :, :]) ** 2).sum(-1), axis=1)
            s = d2.sum()
            probs = d2 / s if s > 0 else np.full(n, 1.0 / n)
            centers.append(X[rng.choice(n, p=probs)])
        C = np.array(centers)
        lab = None
        for _ in range(max_iter):
            dist = ((X[:, None, :] - C[None, :, :]) ** 2).sum(-1)
            new = dist.argmin(1)
            if lab is not None and (new == lab).all():
                break
            lab = new
            for j in range(k):
                m = lab == j
                if m.any():
                    C[j] = X[m].mean(0)
        inertia = float(((X - C[lab]) ** 2).sum())
        if best is None or inertia < best[0] - tol:
            best = (inertia, lab.copy(), C.copy())
    return best


def silhouette(X, labels):
    """平均轮廓系数（O(n²)，只在抽样上算）。"""
    n = len(X)
    uniq = np.unique(labels)
    if len(uniq) < 2 or len(uniq) >= n:
        return None
    d = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(-1))
    s = np.zeros(n)
    for i in range(n):
        own = labels == labels[i]
        own_n = own.sum()
        if own_n <= 1:
            s[i] = 0.0
            continue
        a = d[i, own].sum() / (own_n - 1)
        b = min(d[i, labels == c].mean() for c in uniq if c != labels[i])
        s[i] = (b - a) / max(a, b) if max(a, b) > 0 else 0.0
    return float(s.mean())


def stratified_sample(labels, n_target, rng):
    idx = []
    classes = np.unique(labels)
    per = max(1, n_target // len(classes))
    for c in classes:
        pool = np.where(labels == c)[0]
        take = min(per, len(pool))
        idx.extend(rng.choice(pool, size=take, replace=False).tolist())
    return np.array(sorted(idx))


def purity(type_idx, labels):
    """簇纯度：每个簇内占比最高的类型份额，按簇规模加权。"""
    tot = 0
    hit = 0
    for c in np.unique(labels):
        m = labels == c
        vals, cnt = np.unique(type_idx[m], return_counts=True)
        tot += int(m.sum())
        hit += int(cnt.max())
    return hit / tot if tot else None


def main():
    el = load_elements()
    types = ["project", "patent", "journal"]
    X_list, t_list = [], []
    for i, t in enumerate(types):
        s = el[t]["score"]
        X_list.append(np.column_stack([np.full(len(s), i, dtype=float), s / 100.0]))
        t_list.append(np.full(len(s), i, dtype=int))
    # 类型独热（3 列）+ 影响力（1 列）
    type_idx = np.concatenate(t_list)
    onehot = np.zeros((len(type_idx), len(types)))
    onehot[np.arange(len(type_idx)), type_idx] = 1.0
    infl = np.concatenate([el[t]["score"] for t in types]) / 100.0
    X = np.column_stack([onehot, infl])

    rng = np.random.default_rng(SEED)
    sil_idx = stratified_sample(type_idx, SIL_SAMPLE, rng)

    models = []
    best = None
    for k in range(2, 9):
        inertia, lab, C = kmeans(X, k, rng)
        sil = silhouette(X[sil_idx], lab[sil_idx])
        models.append({"k": k, "inertia": round(inertia, 3),
                       "silhouette": round(sil, 4) if sil is not None else None})
        if sil is not None and (best is None or sil > best["silhouette"]):
            best = {"k": k, "silhouette": round(sil, 4), "labels": lab, "centers": C,
                    "inertia": inertia}
    lab = best["labels"]

    clusters = []
    for c in range(best["k"]):
        m = lab == c
        comp = {}
        for i, t in enumerate(types):
            comp[t] = int(((type_idx == i) & m).sum())
        sc = infl[m] * 100
        clusters.append({
            "cluster": c,
            "n": int(m.sum()),
            "share": round(float(m.sum()) / len(lab), 4),
            "composition": comp,
            "dominant_type": max(comp, key=comp.get),
            "influence_mean": round(float(sc.mean()), 3),
            "influence_p10": round(float(np.percentile(sc, 10)), 3),
            "influence_p90": round(float(np.percentile(sc, 90)), 3),
            "centroid": [round(float(x), 4) for x in best["centers"][c]],
        })
    clusters.sort(key=lambda x: -x["n"])

    # 对照：去掉类型独热，只按影响力聚类（看簇是否由类型驱动）
    Xb = infl.reshape(-1, 1)
    models_b, best_b = [], None
    for k in range(2, 9):
        inertia, labb, C = kmeans(Xb, k, rng)
        sil = silhouette(Xb[sil_idx], labb[sil_idx])
        models_b.append({"k": k, "silhouette": round(sil, 4) if sil is not None else None})
        if sil is not None and (best_b is None or sil > best_b["silhouette"]):
            best_b = {"k": k, "silhouette": round(sil, 4), "labels": labb}
    variant_b = {
        "features": "仅影响力分（1 维）",
        "best_k": best_b["k"],
        "best_silhouette": best_b["silhouette"],
        "purity_by_type": round(purity(type_idx, best_b["labels"]), 4),
        "models": models_b,
    }

    # ---------- 在类内做影响力分层（跨类合并聚类的替代交付形态） ----------
    within = {}
    for i, t in enumerate(types):
        s = el[t]["score"]
        Xt = (s / 100.0).reshape(-1, 1)
        rng_t = np.random.default_rng(SEED)
        idx_t = rng_t.choice(len(Xt), size=min(SIL_SAMPLE, len(Xt)), replace=False)
        best_t = None
        models_t = []
        for k in range(2, 9):
            if len(Xt) < k * 5:
                continue
            inertia, labt, Ct = kmeans(Xt, k, rng_t)
            sil = silhouette(Xt[idx_t], labt[idx_t])
            models_t.append({"k": k, "silhouette": round(sil, 4) if sil is not None else None})
            if sil is not None and (best_t is None or sil > best_t["silhouette"]):
                best_t = {"k": k, "silhouette": round(sil, 4), "labels": labt}
        if best_t is None:
            continue
        bands = []
        for c in np.unique(best_t["labels"]):
            m = best_t["labels"] == c
            sc = s[m]
            bands.append({"band": int(c), "n": int(m.sum()),
                          "share": round(float(m.sum()) / len(s), 4),
                          "influence_min": round(float(sc.min()), 3),
                          "influence_max": round(float(sc.max()), 3),
                          "influence_mean": round(float(sc.mean()), 3)})
        bands.sort(key=lambda x: -x["influence_mean"])
        within[t] = {"n": int(len(s)), "best_k": best_t["k"],
                     "best_silhouette": best_t["silhouette"],
                     "bands": bands, "models": models_t}

    payload = {
        "metric_id": METRIC,
        "metric_name": "要素聚类",
        "data_support_level": "部分支持",
        "run_at": "2026-10-22",
        "db": "gkx@183.240.141.251:3318（专利仅读被引表 20,515 行，未扫 dwd_patent）",
        "element_universe": {t: el[t]["n"] for t in types} | {"conference": 0},
        "en_journal_note": el["en_journal_note"],
        "conference_gap": el["conference"]["why"],
        "params": {"seed": SEED, "k_range": [2, 8], "silhouette_sample": len(sil_idx),
                   "n_init": 8, "max_iter": 100, "feature": "3 类独热 + 影响力(0-1)"},
        "n_samples": int(len(X)),
        "models": models,
        "best": {"k": best["k"], "silhouette": best["silhouette"],
                 "inertia": round(best["inertia"], 3),
                 "purity_by_type": round(purity(type_idx, lab), 4)},
        "clusters": clusters,
        "variant_influence_only": variant_b,
        "within_type": within,
        "degeneration": {
            "cross_type_purity": round(purity(type_idx, lab), 4),
            "why": "类型独热（3 维）与影响力（1 维）等权时，K-Means 的最优解就是按类型切分："
                   "轮廓系数 0.97、纯度 1.00，簇 = 类型，跨类合并聚类不含额外信息。"
                   "真正可交付的是类内影响力分层（within_type）。",
        },
        "hierarchical_branch": {
            "triggered": False,
            "rule": "5 ≤ n ≤ 29 用层次聚类（Ward）",
            "why": f"本批 n={len(X)} ≥ 30，按口径走 K-Means 分支；分支已实现未触发",
        },
        "gaps": [
            "会议要素 0 条：gkx 无会议实体表，publication_type 只有「期刊」，四类要素实为三类。",
            "专利影响力只覆盖被引表里的 20,000 件（占全库 2,939,895 件的 0.68%），且专利价值列不在被引表，"
            "影响力实为「纯被引」。",
            "期刊影响因子列整列为空，期刊影响力改用「累计被引 + 篇均被引」代理。",
            "项目影响力只到投入侧（金额）与履约侧（结题摘要），无产出侧。",
            "聚类结果依赖抽样算轮廓系数，K 选择对样本敏感；本文固定 seed=42 可复现。",
        ],
    }
    write_out(METRIC, payload)
    print(json.dumps({"n": len(X), "best_k": best["k"], "sil": best["silhouette"],
                      "purity": payload["best"]["purity_by_type"],
                      "variant_b": {k: variant_b[k] for k in ("best_k", "best_silhouette", "purity_by_type")}},
                     ensure_ascii=False, indent=1))
    for c in clusters:
        print(c["cluster"], c["n"], c["composition"], c["influence_mean"])


if __name__ == "__main__":
    main()
