#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M_INNOV_DS_FACTORS_016 · 要素聚类分析（对齐 M_INNOV_FACTOR_CLUSTER）
王惠口径：会议 / 项目 / 专利 / 期刊四类要素，各取影响力得分 + 类型独热，
          样本≥30 用 K-Means（K=2..8 取最大轮廓），5—29 用层次聚类，
          输出簇标签与簇规模（不是 0-100 分）。

数据面：三方库 gkx（只读）。
  期刊：gkx.dwd_zh_journal / dwd_en_journal（影响指数全空，走 015 重归一口径）
  项目：gkx.dwd_zh_project（资助金额 + 结题摘要完备；参与机构维退化）
  专利：gkx.dwd_patent.value（被引维覆盖 0.016%，仅价值维）
  会议：四张出版物表 publication_type 无会议枚举 → 0 条

输出：code/M_INNOV_DS_FACTORS_016_out.json
"""
import json
import math
import os
import random
import statistics
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "M_INNOV_DS_FACTORS_016_out.json")
random.seed(42)
np.random.seed(42)


def q1(cur, sql):
    cur.execute(sql)
    return cur.fetchone()


def pct_rank(vals):
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    n = len(vals)
    out = [0.0] * n
    i = 0
    while i < n:
        k = i
        while k + 1 < n and vals[order[k + 1]] == vals[order[i]]:
            k += 1
        r = (i + k) / 2.0
        for m in range(i, k + 1):
            out[order[m]] = 100.0 * r / (n - 1) if n > 1 else 0.0
        i = k + 1
    return out


res = {
    "metric_id": "M_INNOV_DS_FACTORS_016",
    "name": "要素聚类分析",

    # 基期披露（派单书铁律 5）：聚类是截面结构分析，输入为全量特征矩阵，不涉及时序分母。
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": ("聚类为截面结构分析，输入是库内全量要素特征矩阵，不做逐年切片、"
                        "不做增速或同比，因此无基期分母。"),
    "aligned_to": "M_INNOV_FACTOR_CLUSTER",
    "data_plane": "gkx（183.240.141.251:3318）",
    "probe_time": "2026-10-22",
}
cur = gkx()
cur.execute("SET SESSION max_execution_time=120000")

# ---------------------------------------------------------------- 四类入集探测
res["probes"] = {}
cur.execute("""SELECT SUM(publication_type IN ('会议','Conference','conference','Proceedings')),
                      COUNT(*) FROM gkx.dwd_zh_journal""")
r = cur.fetchone()
res["probes"]["conference_publications_zh"] = {"conference": int(r[0] or 0), "n": int(r[1])}
cur.execute("""SELECT SUM(publication_type IN ('会议','Conference','conference','Proceedings')),
                      COUNT(*) FROM gkx.dwd_en_journal""")
r = cur.fetchone()
res["probes"]["conference_publications_en"] = {"conference": int(r[0] or 0), "n": int(r[1])}
cur.execute("SELECT publication_type, COUNT(*) FROM gkx.dwd_zh_journal GROUP BY publication_type")
res["probes"]["zh_journal_type"] = [[t, int(c)] for t, c in cur.fetchall()]
cur.execute("SELECT publication_type, COUNT(*) FROM gkx.dwd_en_journal GROUP BY publication_type")
res["probes"]["en_journal_type"] = [[t, int(c)] for t, c in cur.fetchall()]
cur.execute("SELECT publication_type, COUNT(*) FROM gkx.dwd_zh_paper GROUP BY publication_type")
res["probes"]["zh_paper_type"] = [[t, int(c)] for t, c in cur.fetchall()]
cur.execute("""SELECT COUNT(*), SUM(funded_amount IS NOT NULL AND funded_amount>0),
                      SUM(final_report_abstract IS NOT NULL AND final_report_abstract<>''),
                      SUM(participating_institution LIKE '%、%'),
                      SUM(funded_institution IS NOT NULL AND funded_institution<>'')
               FROM gkx.dwd_zh_project""")
r = cur.fetchone()
res["probes"]["zh_project"] = {
    "n": int(r[0]), "amt": int(r[1] or 0), "abst": int(r[2] or 0),
    "multi_inst": int(r[3] or 0), "funded_inst": int(r[4] or 0)}

# ---------------------------------------------------------------- 三类要素影响力
# (1) 期刊：015 口径（影响指数缺测 → 0.5*发文 + 0.5*累计被引；英文单维）
cur.execute("SELECT publication_id, zh_name, paper_nums, cite_nums FROM gkx.dwd_zh_journal")
zh = cur.fetchall()
cur.execute("SELECT publication_id, zh_name, en_name, paper_nums FROM gkx.dwd_en_journal")
en = cur.fetchall()
jour = []
rp = pct_rank([float(r[2] or 0) for r in zh])
rc = pct_rank([float(r[3] or 0) for r in zh])
for i, r in enumerate(zh):
    jour.append({"kind": "期刊", "id": r[0], "name": r[1],
                 "score": round(0.5 * rp[i] + 0.5 * rc[i], 3)})
rpe = pct_rank([float(r[3] or 0) for r in en])
for i, r in enumerate(en):
    jour.append({"kind": "期刊", "id": r[0], "name": r[1] or r[2],
                 "score": round(rpe[i], 3)})

# (2) 项目：金额(log) + 结题摘要完备；参与机构维退化
cur.execute("""SELECT id, title, funded_amount, participating_institution,
                      LENGTH(final_report_abstract), approval_year
               FROM gkx.dwd_zh_project""")
proj_rows = cur.fetchall()
amts = [math.log10(float(r[2])) for r in proj_rows if r[2]]
LO_A, HI_A = min(amts), max(amts)
proj = []
for r in proj_rows:
    a = r[2]
    s_amt = (100.0 * (math.log10(float(a)) - LO_A) / (HI_A - LO_A)) if a else None
    s_done = 1.0 if (r[4] or 0) > 0 else 0.0
    dims = [(0.5, s_amt), (0.5, 100.0 * s_done)]
    live = [(w, v) for w, v in dims if v is not None]
    ws = sum(w for w, _ in live)
    proj.append({"kind": "项目", "id": r[0], "name": r[1],
                 "year": (int(r[5]) // 10000 if r[5] else None),
                 "score": round(sum(w * v for w, v in live) / ws, 3) if ws else None})
proj = [p for p in proj if p["score"] is not None]

# (3) 专利：价值维（被引维覆盖 0.016%，不可用）
PAT_LO, PAT_HI = math.log10(3000.0), math.log10(7740000.0)


def sample_patents(n=2500):
    """按主键序取前 n 条 value 非空记录（单次早停扫，不做 COUNT(*)、不做大 OFFSET）。

    dwd_patent 无年份/申请人/IPC 索引，COUNT(*) 与 OFFSET 深翻都会撞
    max_execution_time。这里只发一条 `ORDER BY dwd_id LIMIT n`（主键序扫描，
    命中 n 行即停），并用分布快照校验样本代表性。
    """
    cur.execute("SET SESSION max_execution_time=300000")
    cur.execute(f"""SELECT pn, first_applicant_name, value, apdt_year
                    FROM gkx.dwd_patent
                    WHERE value IS NOT NULL AND value>0
                    ORDER BY dwd_id LIMIT {n}""")
    return cur.fetchall()


def sample_vs_universe(rows):
    """把主键序样本的价值分布与全量 value 分组快照对比，披露抽样偏差。"""
    snap = os.path.join(HERE, "_snapshots21", "patent_value_agg_gkx.json")
    scores = sorted(max(0.0, min(100.0, 100.0 * (math.log10(float(r[2])) - PAT_LO)
                               / (PAT_HI - PAT_LO))) for r in rows)
    hist = {}
    for s in scores:
        b = int(math.floor(s / 5.0) * 5)
        hist[b] = hist.get(b, 0) + 1
    n = len(scores)
    out = {
        "sample_n": n,
        "sample_median_score": round(statistics.median(scores), 2) if scores else None,
        "sample_p90_score": round(scores[int(0.9 * (n - 1))], 2) if scores else None,
        "sample_hist_5pt": [[b, round(100.0 * hist[b] / n, 2)] for b in sorted(hist)],
        "note": "按 dwd_id 主键序取前 2,500 条 value>0 记录（确定性样本，非随机抽样）",
    }
    if os.path.exists(snap):
        agg = json.load(open(snap, encoding="utf-8"))
        tot = agg.get("n_nonnull") or 1
        uh = {int(b): round(100.0 * c / tot, 2) for b, c in agg.get("histogram_score_5pt", [])}
        out["universe"] = {
            "source": "_snapshots21/patent_value_agg_gkx.json（全量 GROUP BY value）",
            "n_nonnull": tot,
            "n_distinct_value": agg.get("n_distinct_value"),
            "median_value": agg.get("median_value"),
            "median_score": round(max(0.0, min(100.0, 100.0 * (
                math.log10(float(agg["median_value"])) - PAT_LO) / (PAT_HI - PAT_LO))), 2)
            if agg.get("median_value") else None,
            "hist_5pt": [[b, uh[b]] for b in sorted(uh)],
        }
        if out.get("sample_median_score") is not None and out["universe"]["median_score"]:
            out["median_gap_pt"] = round(
                out["sample_median_score"] - out["universe"]["median_score"], 2)
    return out


pat_rows = sample_patents(2500)
res["probes"]["patent_sample_check"] = sample_vs_universe(pat_rows)
pat = []
for r in pat_rows:
    s = 100.0 * (math.log10(float(r[2])) - PAT_LO) / (PAT_HI - PAT_LO)
    pat.append({"kind": "专利", "id": r[0], "name": r[1],
                "year": r[3], "score": round(max(0.0, min(100.0, s)), 3)})

res["probes"]["element_counts"] = {"期刊": len(jour), "项目": len(proj),
                                   "专利": len(pat), "会议": 0}
res["probes"]["project_amt_range"] = {"log10_min": round(LO_A, 4),
                                      "log10_max": round(HI_A, 4)}
res["probes"]["project_dim_notes"] = {
    "funded_institution_fill": res["probes"]["zh_project"]["funded_inst"],
    "multi_institution_rows": res["probes"]["zh_project"]["multi_inst"],
    "conclusion": "参与机构数维退化（受资助机构 100% 空、参与机构 99.95% 单一机构），按缺测处理",
}

# ---------------------------------------------------------------- 特征矩阵与 K-Means
random.shuffle(jour)
random.shuffle(proj)
random.shuffle(pat)
sample = jour[:1000] + proj[:2500] + pat[:2500]
random.shuffle(sample)
kinds = ["期刊", "项目", "专利"]
X = np.array([[e["score"]] + [1.0 if e["kind"] == k else 0.0 for k in kinds]
              for e in sample], dtype=float)
mu, sd = X.mean(axis=0), X.std(axis=0)
sd[sd == 0] = 1.0
Z = (X - mu) / sd


def kmeans(Zm, k, iters=120, restarts=6):
    best = None
    for _ in range(restarts):
        idx = [np.random.randint(len(Zm))]
        d2 = ((Zm - Zm[idx[0]]) ** 2).sum(axis=1)
        for _ in range(k - 1):
            p = d2 / d2.sum() if d2.sum() > 0 else None
            idx.append(np.random.choice(len(Zm), p=p))
        C = Zm[idx].copy()
        lab = np.zeros(len(Zm), dtype=int)
        for _ in range(iters):
            D = ((Zm[:, None, :] - C[None, :, :]) ** 2).sum(axis=2)
            new = D.argmin(axis=1)
            if (new == lab).all():
                break
            lab = new
            for c in range(k):
                m = lab == c
                if m.any():
                    C[c] = Zm[m].mean(axis=0)
        sse = float(((Zm - C[lab]) ** 2).sum())
        if best is None or sse < best[0]:
            best = (sse, lab.copy(), C.copy())
    return best


def silhouette(Zm, lab, n_probe=1200):
    n = len(Zm)
    idx = np.random.choice(n, min(n_probe, n), replace=False)
    P = Zm[idx]
    D = np.sqrt(((P[:, None, :] - Zm[None, :, :]) ** 2).sum(axis=2))
    s = []
    for i, gi in enumerate(idx):
        same = (lab == lab[gi])
        same[i] = False
        if same.sum() == 0:
            continue
        a = D[i][same].mean()
        b = min(D[i][lab == c].mean() for c in set(lab)
                if c != lab[gi] and (lab == c).any())
        if max(a, b) > 0:
            s.append((b - a) / max(a, b))
    return round(float(np.mean(s)), 4) if s else None


runs = {}
for k in range(2, 9):
    sse, lab, C = kmeans(Z, k)
    runs[k] = {"sse": round(sse, 3), "silhouette": silhouette(Z, lab)}

best_k = max(runs, key=lambda k: (runs[k]["silhouette"] or -9))
sse, lab, C = kmeans(Z, best_k)

res["compute"] = {"n_elements": len(sample),
                  "k_selection": {str(k): v for k, v in runs.items()},
                  "best_k": best_k, "silhouette": runs[best_k]["silhouette"]}

# 变体 B：仅影响力分（去掉类型独热）
Z1 = Z[:, [0]]
runs1 = {}
for k in range(2, 9):
    sse1, lab1, C1 = kmeans(Z1, k)
    runs1[k] = {"sse": round(sse1, 3), "silhouette": silhouette(Z1, lab1)}
best_k1 = max(runs1, key=lambda k: (runs1[k]["silhouette"] or -9))
sse1, lab1, C1 = kmeans(Z1, best_k1)
res["compute"]["variant_b_score_only"] = {
    "features": "仅要素影响力分（1 维，z-score）",
    "k_selection": {str(k): v for k, v in runs1.items()},
    "best_k": best_k1, "silhouette": runs1[best_k1]["silhouette"]}


def describe(mask):
    sub = [sample[i] for i in np.where(mask)[0]]
    sc = [e["score"] for e in sub]
    mix = {}
    for e in sub:
        mix[e["kind"]] = mix.get(e["kind"], 0) + 1
    return {"size": len(sub), "share_pct": round(100.0 * len(sub) / len(sample), 2),
            "mean_score": round(float(np.mean(sc)), 2),
            "score_p05_p95": [round(float(np.percentile(sc, 5)), 2),
                              round(float(np.percentile(sc, 95)), 2)],
            "type_mix": mix}


res["compute"]["clusters"] = {str(c): describe(lab == c) for c in range(best_k)}
res["compute"]["cluster_members_sample"] = {
    str(c): [{"kind": e["kind"], "name": (e["name"] or "")[:40], "score": e["score"]}
             for e in [sample[i] for i in np.where(lab == c)[0][:5]]]
    for c in range(best_k)}
res["compute"]["score_distribution"] = {
    "min": round(float(np.min([e["score"] for e in sample])), 2),
    "median": round(float(np.median([e["score"] for e in sample])), 2),
    "max": round(float(np.max([e["score"] for e in sample])), 2)}


def describe1(mask):
    sub = [sample[i] for i in np.where(mask)[0]]
    sc = [e["score"] for e in sub]
    mix = {}
    for e in sub:
        mix[e["kind"]] = mix.get(e["kind"], 0) + 1
    return {"size": len(sub), "share_pct": round(100.0 * len(sub) / len(sample), 2),
            "mean_score": round(float(np.mean(sc)), 2),
            "score_range": [round(float(min(sc)), 2), round(float(max(sc)), 2)],
            "type_mix": mix}


res["compute"]["variant_b_clusters"] = {str(c): describe1(lab1 == c)
                                        for c in range(best_k1)}

# ---------------------------------------------------------------- 定档
res["dimension_status"] = {
    "期刊要素": {"rows": len(jour), "status": "可用（影响指数维缺测，走 015 重归一口径）"},
    "项目要素": {"rows": len(proj), "status": "可用（金额 + 摘要完备；参与机构维退化）"},
    "专利要素": {"rows": len(pat),
               "status": "可用但仅价值维（被引 0.016% 覆盖）；主键序样本见 patent_sample_check"},
    "会议要素": {"rows": 0,
               "status": "不可用——dwd_zh_journal/dwd_en_journal/dwd_zh_paper 的 "
                         "publication_type 仅期刊/丛书/图书，全库 0 条会议记录"},
}
res["support_judgment"] = "部分支持"
res["judgment_reason"] = (
    "王惠口径要求会议 / 项目 / 专利 / 期刊四类要素入集，gkx 会议类实体 0 条"
    "（publication_type 无会议枚举），四类仅得三类；且专利影响力退化为价值单维、"
    "项目参与机构数维退化、期刊影响指数缺测。聚类算法本身可跑通并产出簇标签与规模"
    f"（K={best_k}，轮廓系数 {runs[best_k]['silhouette']}），但要素集不完整，故判部分支持。"
)
res["computable_subset"] = {
    "kinds_available": ["期刊", "项目", "专利"],
    "kinds_missing": ["会议"],
    "n_elements_used": len(sample),
    "method": f"z-score 标准化 + K-Means（K=2..8，轮廓系数择优 → K={best_k}）",
}

cur.close()
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1, default=str)

print(json.dumps(res["probes"], ensure_ascii=False, default=str)[:1600])
print("k_selection:", json.dumps(res["compute"]["k_selection"], ensure_ascii=False))
print("clusters:", json.dumps(res["compute"]["clusters"], ensure_ascii=False))
print("variant_b:", json.dumps(res["compute"]["variant_b_clusters"], ensure_ascii=False))
print("->", OUT)
