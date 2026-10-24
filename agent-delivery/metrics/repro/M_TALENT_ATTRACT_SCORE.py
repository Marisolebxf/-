#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_ATTRACT_SCORE —— 引入人才推荐指数（TALENT 展示面 §1.1.1.2.4.2.5.8）

池：外部候选池 = 有姓名的学者中**现机构不在深圳**者（现职深圳者被排除，因为本件语义是「从外面引谁」）。
四维：A 学术力 0.30 / P 产业力 0.15 / M 产业契合 0.25 / C 深圳连接 0.30，缺维按剩余权重归一。

四维各自的可用面（本批实测，全部零 SQL）：
  A —— `dwd_scholar` 21,316 行三列 100% 非空 → 全池可算
  P —— 发明人姓名计数缓存（403,743 名）；同名多人判缺测 → 可用约七成
  M —— 研究方向标签（9.3% 可连）∪ 中文论文关键词（姓名+机构双锚定，68.3%）→ 可用约七成
  C —— 深圳署名论文（外部学者 10.3%）∪ 深圳履历（子表 9.3% 可连）→ 可用约一成
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _talent21_common import (  # noqa: E402
    anchored_papers, clusters_of, log_minmax, paper_clusters, paper_insts, patent_of, pctl,
    research, scholars, spearman, st, work, write_out,
)

METRIC = "M_TALENT_ATTRACT_SCORE"
W = {"A": 0.30, "P": 0.15, "M": 0.25, "C": 0.30}


def main() -> None:
    all_sch = [s for s in scholars() if s["name"]]
    pool = [s for s in all_sch if "深圳" not in s["org"]]
    n = len(pool)
    sz_pool = len(all_sch) - n

    rd = research()
    wx_sz = {w["sid"] for w in work() if "深圳" in w["org"]}

    # ---- 原始维 ----
    paper = [s["paper"] for s in pool]
    cite = [s["cite"] for s in pool]
    h = [s["h"] for s in pool]

    pat = []
    pat_flag = Counter()
    for s in pool:
        v, why = patent_of(s)
        pat.append(v)
        pat_flag[why] += 1

    m_raw = []          # 命中集群数
    m_src = Counter()
    c_raw = []          # 深圳连接：深圳合作者论文数 + 深圳履历（0—2 起步，缺测 None）
    c_src = Counter()
    wx_any = {w["sid"] for w in work()}
    insts = paper_insts()
    n_anch = 0
    for s in pool:
        tags = list(rd.get(s["sid"], []))
        recs = anchored_papers(s)
        if recs:
            n_anch += 1
        cl: list[str] = list(clusters_of(tags)) if tags else []
        for r in recs:
            cl.extend(paper_clusters(r["pid"], r["kw"], r["ti"]))
        merged = list(dict.fromkeys(cl))
        has_m = bool(tags or recs)
        m_raw.append(len(merged) if has_m else None)
        m_src["fields" if tags else ("paper" if recs else "none")] += 1

        # C：合作缘用**本人锚定论文的共同作者机构**（不受同名影响）；履历缘用子表（9.3% 可连）
        sz_co = 0
        for r in recs:
            others = insts.get(r["pid"], [])
            if any("深圳" in x for x in others):
                sz_co += 1
        sz_work = s["sid"] in wx_sz
        if not recs and s["sid"] not in wx_any:
            c_raw.append(None)
            c_src["no_source"] += 1
        else:
            c_raw.append(sz_co + (1 if sz_work else 0))
            if sz_co:
                c_src["sz_coauthor"] += 1
            if sz_work:
                c_src["sz_work"] += 1
            if not sz_co and not sz_work:
                c_src["zero"] += 1

    # ---- 归一（缺测不参与 min-max，也不补 0）----
    zA = log_minmax([1.0 * paper[i] for i in range(n)])
    zA = [(zA[i] + log_minmax(cite)[i] + log_minmax(h)[i]) / 3 for i in range(n)]

    p_idx = [i for i in range(n) if pat[i] is not None]
    p_norm = log_minmax([float(pat[i]) for i in p_idx])
    zP = {i: p_norm[k] for k, i in enumerate(p_idx)}

    m_idx = [i for i in range(n) if m_raw[i] is not None]
    m_norm = log_minmax([float(m_raw[i]) for i in m_idx])
    zM = {i: m_norm[k] for k, i in enumerate(m_idx)}

    c_norm = log_minmax([float(c_raw[i] if c_raw[i] is not None else 0) for i in range(n)])
    zC = {i: c_norm[i] for i in range(n)}

    # ---- 合成（缺维按剩余权重归一）----
    score = [0.0] * n
    dims = [0] * n
    parts = [dict() for _ in range(n)]
    for i in range(n):
        acc, wsum = 0.0, 0.0
        acc += W["A"] * zA[i]; wsum += W["A"]; parts[i]["A"] = round(100 * zA[i], 2)
        if i in zP:
            acc += W["P"] * zP[i]; wsum += W["P"]; parts[i]["P"] = round(100 * zP[i], 2)
        if i in zM:
            acc += W["M"] * zM[i]; wsum += W["M"]; parts[i]["M"] = round(100 * zM[i], 2)
        if c_raw[i] is not None:
            acc += W["C"] * zC[i]; wsum += W["C"]; parts[i]["C"] = round(100 * zC[i], 2)
        score[i] = 100 * acc / wsum if wsum else 0.0
        dims[i] = len(parts[i])

    # 只对「至少两维可测」的人出可发布排名：单维者（实测 2,306 人）在重归一后等于该维本身，
    # 会把「缺测」伪装成「满分」，故不进入榜单，只保留分值与 incomplete 标记。
    rankable = [i for i in range(n) if dims[i] >= 2]
    order = sorted(rankable, key=lambda i: -score[i])

    def row(i):
        s = pool[i]
        tags = rd.get(s["sid"], [])
        recs = anchored_papers(s)
        cl: list[str] = list(clusters_of(tags)) if tags else []
        for r in recs:
            cl.extend(paper_clusters(r["pid"], r["kw"], r["ti"]))
        cl = list(dict.fromkeys(cl))
        return {"name": s["name"], "org": s["org"], "score": round(score[i], 2),
                "dims": dims[i], "comp": parts[i], "clusters": cl[:6],
                "patent": pat[i],
                "sz_link": bool(c_raw[i]), "anchor_papers": len(recs)}

    top = [row(i) for i in order[:15]]
    ext_sz = [i for i in order if (c_raw[i] or 0) > 0]
    top_sz_link = [row(i) for i in ext_sz[:10]]

    # ---- 敏感性 ----
    eq = [(zA[i] + zP.get(i, 0) + zM.get(i, 0) + zC.get(i, 0)) / 4 * 100 for i in range(n)]
    a_only = [100 * zA[i] for i in range(n)]
    sp_final_a = spearman(score, a_only)
    sp_final_eq = spearman(score, eq)
    top50 = {pool[i]["sid"] for i in order[:50]}
    top50_a = {pool[i]["sid"] for i in sorted(rankable, key=lambda i: -a_only[i])[:50]}

    payload = {
        "metric": METRIC,
        "support_judgment": "部分支持",
        "support_reason": "A/P/M 三维在外部池可算（A 全覆盖、P 约七成、M 约七成），但 C 维（深圳连接）只有约"
                          "一成候选可测：深圳署名论文 10.3%、深圳履历受「子表 scholar_id 仅 9.3% 可连」"
                          "限制；需求所指的招聘平台真源 `dwd_job` 仅 10 行、无投递/意向交互日志，"
                          "「智能筛选」只能降级为规则化筛选 → 部分支持。",
        "method": {
            "pool": "有姓名的学者中现机构不含「深圳」者（现职深圳者排除）",
            "weights": W, "renormalize": "缺维按剩余权重归一，逐人记录 dims_available",
            "normalization": "log1p → 池内 min-max",
            "dims": {
                "A": "论文/被引/H 三维等权合成的学术力",
                "P": "发明人姓名件数（同名多人判缺测）",
                "M": "深圳 20+8 集群命中数（研究方向标签 ∪ 中文论文关键词）",
                "C": "深圳连接：锚定论文的共同作者含深圳机构（合作缘）+ 深圳履历（履历缘），按论文数计",
            },
            "sql_count": 0,
        },
        "universe": {
            "named_scholars": len(all_sch), "sz_current_excluded": sz_pool, "pool": n,
            "dim_availability": {
                "A": n,
                "P": len(p_idx), "P_pct": round(100 * len(p_idx) / n, 2),
                "M": len(m_idx), "M_pct": round(100 * len(m_idx) / n, 2),
                "C_nonzero": sum(1 for x in c_raw if x),
                "C_nonzero_pct": round(100 * sum(1 for x in c_raw if x) / n, 2),
            },
            "patent_flags": dict(pat_flag),
            "m_sources": dict(m_src),
            "c_sources": dict(c_src),
            "dims_available_hist": dict(Counter(dims)),
        },
        "score_stats": st(score),
        "score_stats_rankable": st([score[i] for i in rankable]),
        "rankable": len(rankable),
        "top15": top,
        "sz_link_top10": top_sz_link,
        "sensitivity": {"spearman_vs_A_only": sp_final_a, "spearman_vs_equal_weight": sp_final_eq,
                        "top50_overlap_vs_A_only": len(top50 & top50_a)},
        "cluster_hits": [{"cluster": k, "n": v} for k, v in
                         Counter(c for i in range(n) for c in clusters_of(rd.get(pool[i]["sid"], []))).most_common(10)],
        "weights_note": "0.30/0.15/0.25/0.30 沿用上一版先验；P 维权重压到 0.15 是因姓名匹配噪声，"
                        "与 OECD/JRC「不确定性高的维度降权」一致。",
        "probes": {"source": "_snapshots21/probe_talent21_20261022.json; a25_paper_panel.json; "
                             "patent_inventor_counts_gkx.json; probe_a26_20261022.json"},
    }
    write_out(METRIC, payload)
    print("pool", n, "top:", [(r["name"], r["score"], r["dims"]) for r in top[:5]])
    print("dims hist", dict(Counter(dims)), "pct M", round(100 * len(m_idx) / n, 2))


if __name__ == "__main__":
    main()
