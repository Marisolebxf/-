#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_DEEP_156_1 —— 重点人才识别模型（TALENT 深度分析第 156 号）

需求语义：以「学历 / 工作经验 / 科研成果」三类指标识别科研能力突出或具战略价值的个人，
按阈值输出重点人才名单。需求未给公式、权重、阈值。

本文口径（全部实测，零 SQL）：
  1. 打分池 = `gkx.dwd_scholar` 全量 21,316 行（A-26 批窄列快照 probe_a26_20261022.json）。
  2. 复合分 K = 100 × (0.40·z_h + 0.35·z_cite + 0.25·z_paper)，三维各自 log1p 后池内 min-max。
     选 log1p 是因为三列均为重尾（h 的 p99 是 p50 的十几倍），直接 min-max 会把 99% 的人压到 3 分以下。
  3. 院士标识只作**外部校验**、不进权重：`dwd_scholar_talent_flag` 的 academician=1 共 112 行，
     其中只有 80 行能挂到学者主档（7.5 折损耗），若按 0.2 权重入模，等于给 99.6% 的人封顶 80 分，
     这不是「战略价值维」，是「名单维」。
  4. 分领域识别改用**姓名+机构双锚定的中文论文**判簇（anchored_papers，覆盖 68.34%），
     不用 research_direction（该表 scholar_id 与主档只有 9.3% 交集，见 id_gap）。

产物：code/M_TALENT_DEEP_156_1_out.json（本脚本唯一写出，不读任何其他指标产物）。
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _talent21_common import (  # noqa: E402
    academicians, anchored_papers, base_year_block, clusters_of, log_minmax,
    paper_clusters, pctl, research, scholars, st, talent, write_out, work,
)

METRIC = "M_TALENT_DEEP_156_1"
W = {"h": 0.40, "cite": 0.35, "paper": 0.25}
Q_HIGH, Q_MID = 0.95, 0.80   # 需求未给阈值数值，按池内分位标定：前 5% 为重点、前 20% 为关注


def main() -> None:
    all_rows = scholars()
    n_all = len(all_rows)
    sch = [s for s in all_rows if s["name"]]          # 无姓名行无法落到人，剔除出打分池（不补 0）
    n = len(sch)

    h = [s["h"] for s in sch]
    cite = [s["cite"] for s in sch]
    paper = [s["paper"] for s in sch]
    zh, zc, zp = log_minmax(h), log_minmax(cite), log_minmax(paper)
    K = [100 * (W["h"] * zh[i] + W["cite"] * zc[i] + W["paper"] * zp[i]) for i in range(n)]

    cut_high, cut_mid = pctl(K, Q_HIGH), pctl(K, Q_MID)

    def tier(x: float) -> str:
        return ("重点人才（K≥p95）" if x >= cut_high
                else ("关注人才（p80≤K<p95）" if x >= cut_mid else "一般（K<p80）"))

    order = sorted(range(n), key=lambda i: (-K[i], -sch[i]["h"], sch[i]["sid"]))
    tiers = Counter(tier(x) for x in K)

    def row(i: int, rank: int = 0) -> dict:
        s = sch[i]
        return {"rank": rank, "name": s["name"], "org": s["org"], "h": s["h"],
                "cite": s["cite"], "paper": s["paper"], "score": round(K[i], 2)}

    top20 = [row(i, k) for k, i in enumerate(order[:20], 1)]
    sz_idx = [i for i in order if "深圳" in sch[i]["org"]]
    sz_top10 = [row(i, k) for k, i in enumerate(sz_idx[:10], 1)]

    # ---- 院士标识：跨表损耗与外部校验 ----
    t = talent()
    flag_rows = t["academician"]["rows"]
    acad_all = {r[0] for r in flag_rows}
    acad = academicians()
    main_ids = {s["sid"] for s in all_rows}
    acad_in_main = acad & main_ids
    acad_pos = [K[i] for i, s in enumerate(sch) if s["sid"] in acad_in_main]
    acad_pct = sorted(round(100 * sum(1 for x in K if x <= v) / n, 2) for v in acad_pos)
    top100_ids = {sch[i]["sid"] for i in order[:100]}
    acad_top100 = len(acad_in_main & top100_ids)

    # ---- 学历 / 履历 / 研究方向三表的 ID 断裂（决定「学历腿」为何不进权重）----
    edu_rows = t["edu"]["rows"]
    we_rows = work()
    rd = research()
    edu_ids = {r[0] for r in edu_rows}
    we_ids = {w["sid"] for w in we_rows}
    rd_ids = set(rd)
    phd_rows = sum(1 for r in edu_rows if "博士" in (r[2] or ""))
    degree_empty = sum(1 for r in edu_rows if not (r[2] or "").strip())

    # ---- 分领域识别：姓名+机构双锚定论文判簇 ----
    cov = 0
    cluster_n = Counter()
    cluster_scores: dict[str, list[float]] = {}
    for i, s in enumerate(sch):
        if not s["name"]:
            continue
        papers = anchored_papers(s)
        if not papers:
            continue
        cov += 1
        tags: list[str] = []
        for p in papers:
            tags.extend(paper_clusters(p["pid"], p["kw"], p["ti"]))
        cl = clusters_of(tags) if tags else []
        for c in cl:
            cluster_n[c] += 1
            cluster_scores.setdefault(c, []).append(K[i])
    fields = []
    for c, m in cluster_n.most_common():
        if m < 30:
            continue
        ss = sorted(cluster_scores[c], reverse=True)
        fields.append({"cluster": c, "n": m, "top1": round(ss[0], 2),
                       "mean": round(sum(ss) / len(ss), 2)})
    fields.sort(key=lambda x: -x["top1"])

    payload = {
        "metric": METRIC,
        "support_judgment": "部分支持",
        "support_reason": (
            "学术影响力三列（h / citation_nums / paper_nums）在 gkx.dwd_scholar 21,316 行上 100% 非空、"
            "可全量打分，院士标识与中文论文面可作外部校验，识别主链成立；但需求输入第一项「企业人才库数据」"
            "与「招聘/薪资市场信号」在库内无表（dwd_job 仅 10 行），学历/履历/研究方向三张子表与身份主档"
            "只有 9.3% 可行对齐，识别池退化为学者口径 → 部分支持。"),
        "method": {
            "formula": "K = 100 × (0.40·z_h + 0.35·z_cite + 0.25·z_paper)，z 为 log1p 后池内 min-max",
            "weights": W,
            "cuts_percentile": [Q_HIGH, Q_MID],
            "cuts_score": [cut_high, cut_mid],
            "tier_names": ["重点人才（K≥p95）", "关注人才（p80≤K<p95）", "一般（K<p80）"],
            "cut_rationale": "需求未给阈值数值；若用绝对分 60，池内 23.6% 入选，名单失去『重点』含义，故改分位阈值",
            "academician_usage": "仅外部校验，不入权重（112 行标识仅 80 行可挂主档）",
            "field_method": "姓名+机构前缀双锚定的中文论文关键词 → 20+8 集群字典判簇",
        },
        "pool": {
            "scholar_rows": n_all,
            "named_rows": n,
            "nameless_rows": n_all - n,
            "excluded_no_name": n_all - n,
            "sz_scholars": len(sz_idx),
            "h_nonnull": sum(1 for v in h if v is not None),
            "cite_nonnull": sum(1 for v in cite if v is not None),
            "paper_nonnull": sum(1 for v in paper if v is not None),
            "h_pos": sum(1 for v in h if v > 0),
            "cite_pos": sum(1 for v in cite if v > 0),
            "paper_pos": sum(1 for v in paper if v > 0),
        },
        "dist": {"h": st(h), "cite": st(cite), "paper": st(paper), "K": st(K),
                 "K_p99": pctl(K, 0.99), "K_p999": pctl(K, 0.999)},
        "tiers": dict(tiers),
        "thresholds": {
            "cut_high": cut_high, "cut_mid": cut_mid,
            "ge_cut_high": sum(1 for x in K if x >= cut_high),
            "ge_cut_mid": sum(1 for x in K if x >= cut_mid),
            "gt60": sum(1 for x in K if x > 60),
            "gt60_pct": round(100 * sum(1 for x in K if x > 60) / n, 2),
            "pct_below_60": round(100 * sum(1 for x in K if x < 60) / n, 2),
        },
        "top20": top20,
        "sz_top10": sz_top10,
        "academician_check": {
            "flag_rows": len(flag_rows),
            "distinct_ids": len(acad_all),
            "matched_in_scholar": len(acad_in_main),
            "not_matched": len(acad_all - main_ids),
            "match_rate_pct": round(100 * len(acad_in_main) / max(1, len(acad_all)), 2),
            "in_top100": acad_top100,
            "top100_hit_pct": round(100 * acad_top100 / max(1, len(acad_in_main)), 2),
            "score_percentile_median": acad_pct[len(acad_pct) // 2] if acad_pct else None,
            "display_only": True,
        },
        "id_gap": {
            "edu_rows": len(edu_rows),
            "edu_distinct_ids": len(edu_ids),
            "edu_linked": len(edu_ids & main_ids),
            "edu_linked_pct": round(100 * len(edu_ids & main_ids) / max(1, len(edu_ids)), 2),
            "work_rows": len(we_rows),
            "work_distinct_ids": len(we_ids),
            "work_linked": len(we_ids & main_ids),
            "work_linked_pct": round(100 * len(we_ids & main_ids) / max(1, len(we_ids)), 2),
            "research_rows": len(rd_ids),
            "research_linked": len(rd_ids & main_ids),
            "research_linked_pct": round(100 * len(rd_ids & main_ids) / max(1, len(rd_ids)), 2),
            "note": "三张子表用另一套 scholar_id 码域，且表内无姓名列可回连；「学历/经历腿」只能独立成表，"
                    "不能落到主档个人。",
        },
        "edu_layer": {
            "rows": len(edu_rows),
            "distinct_ids": len(edu_ids),
            "phd_rows": phd_rows,
            "phd_share_pct": round(100 * phd_rows / max(1, len(edu_rows)), 2),
            "degree_zh_empty": degree_empty,
            "degree_empty_pct": round(100 * degree_empty / max(1, len(edu_rows)), 2),
        },
        "field_layer": {
            "anchored_scholars": cov,
            "coverage_pct": round(100 * cov / max(1, n), 2),
            "clusters_ge30": len(fields),
            "cluster_hits_total": sum(cluster_n.values()),
            "clusters_per_covered_scholar": round(sum(cluster_n.values()) / max(1, cov), 2),
            "clusters_top1_ge_cut": sum(1 for f in fields if f["top1"] >= cut_high),
            "top": fields[:12],
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面口径：K 用三列的生涯累计值（paper_nums / citation_nums / h_index），"
                            "不含年度窗口，也不做任何跨年基准或增长率，故无基期年份。"
                            "论文面的年度数据只用于 158/161，不参与本件打分。"),
        "probes": {
            "sql_count": 0,
            "source": "gkx.dwd_scholar 快照 _snapshots21/probe_a26_20261022.json（21,316 行）",
            "sub_tables": "probe_talent21_20261022.json（work 57,117 / edu 43,766 / research 20,030 / academician 112）",
            "paper_panel": "a25_paper_panel.json（100,900 篇中文论文，215,816 条作者记录）",
        },
        "reused_from": [],
    }
    write_out(METRIC, payload)


if __name__ == "__main__":
    main()
