#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_TALENT_ACADEMIC_SCORE —— 人才学术力指数（TALENT 展示面 §1.1.1.2.4.2.5.6）

口径：需求列五维（论文数量/被引次数/H 指数/期刊影响力/学术合作广度），本件只实现前三维克，
后两维在 gkx 与 live 两侧均无承载（分别见 §四：期刊影响因子整列为空、合作表只有数量无期刊维）。

计算：
  1. 三维原始值 → log1p → 池内 min-max 到 0—1（重尾治理先于权重）；
  2. 等权合成 ×100；
  3. 60/30 双阈值切三档；
  4. 敏感性：池内百分位口径（Spearman + Top50 重合）、单维加倍三组（Top10 重合 + 分档穿越率）。

数据：`_snapshots21/probe_a26_20261022.json` scholar_dump（21,316 行，A-26 批窄列落盘），
本脚本**零 SQL、零 demo 表**。
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _talent21_common import (  # noqa: E402
    academicians, log_minmax, pct_rank, pctl, research, scholars, spearman, st, write_out,
)

METRIC = "M_TALENT_ACADEMIC_SCORE"
W = {"paper": 1 / 3, "cite": 1 / 3, "h": 1 / 3}


def tier_of(x: float) -> str:
    return "强势层" if x >= 60 else ("中坚层" if x >= 30 else "储备层")


def main() -> None:
    sch = [s for s in scholars() if s["name"]]
    n = len(sch)
    paper = [s["paper"] for s in sch]
    cite = [s["cite"] for s in sch]
    h = [s["h"] for s in sch]

    zp, zc, zh = log_minmax(paper), log_minmax(cite), log_minmax(h)
    score = [100 * (W["paper"] * zp[i] + W["cite"] * zc[i] + W["h"] * zh[i]) for i in range(n)]

    # ---- 分档 ----
    tiers = {"强势层": 0, "中坚层": 0, "储备层": 0}
    for x in score:
        tiers[tier_of(x)] += 1

    # ---- 直方图（10 分一档）----
    hist = {f"{i}-{i+10}": 0 for i in range(0, 100, 10)}
    for x in score:
        hist[f"{min(90, int(x // 10) * 10)}-{min(100, int(x // 10) * 10 + 10)}"] = \
            hist.get(f"{min(90, int(x // 10) * 10)}-{min(100, int(x // 10) * 10 + 10)}", 0) + 1
    for k in list(hist):
        if hist[k] == 0 and k != "90-100":
            hist.pop(k)

    # ---- Top10 / 深圳子榜 ----
    order = sorted(range(n), key=lambda i: (-score[i], -sch[i]["h"], sch[i]["sid"]))
    def row(i):
        s = sch[i]
        return {"rank": 0, "name": s["name"], "org": s["org"], "score": round(score[i], 2),
                "paper": s["paper"], "cite": s["cite"], "h": s["h"]}
    top10 = [row(i) for i in order[:10]]
    sz_idx = [i for i in order if "深圳" in sch[i]["org"]]
    sz_top = [row(i) for i in sz_idx[:10]]
    for k, r in enumerate(top10, 1):
        r["rank"] = k
    for k, r in enumerate(sz_top, 1):
        r["rank"] = k

    # ---- 领域组：scholar_id 只 9.3% 可连，组内榜不可交付（实测见 id_gap）----
    tags = research()
    field_tag_total = sum(len(v) for v in tags.values())
    from collections import Counter
    cnt = Counter()
    for sid, ts in tags.items():
        for t in ts:
            cnt[t] += 1
    linked = {s["sid"] for s in sch} & set(tags)
    field_top = [{"field": k, "n": v} for k, v in cnt.most_common(10)]

    # ---- 敏感性 1：池内百分位口径 ----
    qp, qc, qh = pct_rank(paper), pct_rank(cite), pct_rank(h)
    pct_score = [(qp[i] + qc[i] + qh[i]) / 3 for i in range(n)]
    sp = spearman(score, pct_score)
    top50_main = {sch[i]["sid"] for i in order[:50]}
    pct_order = sorted(range(n), key=lambda i: -pct_score[i])
    top50_pct = {sch[i]["sid"] for i in pct_order[:50]}
    overlap50 = len(top50_main & top50_pct)

    # ---- 敏感性 2：单维加倍 ----
    sens = []
    for dim, wts in (("paper", (0.5, 0.25, 0.25)), ("cite", (0.25, 0.5, 0.25)), ("h", (0.25, 0.25, 0.5))):
        s2 = [100 * (wts[0] * zp[i] + wts[1] * zc[i] + wts[2] * zh[i]) for i in range(n)]
        o2 = sorted(range(n), key=lambda i: -s2[i])
        top10_hit = len({sch[i]["sid"] for i in order[:10]} & {sch[i]["sid"] for i in o2[:10]})
        crossed = sum(1 for i in range(n) if tier_of(score[i]) != tier_of(s2[i]))
        sens.append({"shift": f"{dim}×2", "weights": list(wts),
                     "top10_overlap": top10_hit,
                     "tier_cross_rate_pct": round(100 * crossed / n, 2)})

    # ---- 覆盖与完整性 ----
    acad = academicians()
    acad_hit = [i for i, s in enumerate(sch) if s["sid"] in acad]
    acad_median = statistics_median([score[i] for i in acad_hit])
    acad_pctile = round(100 * sum(1 for x in score if x <= acad_median) / n, 1) if acad_hit else None

    payload = {
        "metric": METRIC,
        "support_judgment": "部分支持",
        "support_reason": "需求五维中三维（论文/被引/H）在 gkx.dwd_scholar 100% 非空、可全量打分；"
                          "期刊影响力维无任何期刊分区/影响因子表（dwd_zh_journal.impact_score 2,796 行非空 0），"
                          "学术合作广度维只有 dwd_scholar_coauthor 1,187,606 行的合著数量、无期刊/机构维度，"
                          "两维始终无法补齐 → 部分支持。",
        "method": {
            "normalization": "log1p → 池内 min-max（三维各自归一，互不影响）",
            "weights": W, "tier_cuts": [60, 30],
            "tier_names": ["强势层", "中坚层", "储备层"],
            "pool": "gkx.dwd_scholar 全池（有姓名者）",
        },
        "coverage": {
            "scholars_total": len(scholars()),
            "scored": n,
            "no_name_excluded": len(scholars()) - n,
            "paper_nonnull": sum(1 for v in paper if v is not None),
            "paper_pos": sum(1 for v in paper if v > 0),
            "cite_pos": sum(1 for v in cite if v > 0),
            "h_pos": sum(1 for v in h if v > 0),
            "dims_available": {"paper": True, "cite": True, "h": True,
                               "journal_impact": False, "coauthor_breadth": False},
        },
        "dist": {
            "paper": st(paper), "cite": st(cite), "h": st(h), "score": st(score),
            "distinct_scores": len({round(x, 2) for x in score}),
        },
        "hist": hist,
        "tiers": tiers,
        "top10": top10,
        "sz_top10": sz_top,
        "sz_pool": len(sz_idx),
        "field_tags": {"n_tags": len(cnt), "n_tagged_scholars": len(tags),
                       "tag_hits": field_tag_total, "top": field_top},
        "id_gap": {
            "note": "研究方向/履历/学历三张子表的 scholar_id 与主档不同域，只有 9.3% 可连且无姓名可核对，"
                    "故「领域组内榜」在本批不可交付；领域分布改由 M_TALENT_BASE_98_1 独立成表给出。",
            "research_linked": len(linked),
            "research_rows": len(tags),
            "linked_pct": round(100 * len(linked) / len(tags), 2),
        },
        "sensitivity": {"pct_spearman": sp, "top50_overlap": overlap50, "weight_shift": sens},
        "academician_check": {"n": len(acad), "matched_in_scholar": len(acad_hit),
                              "median_score": acad_median,
                              "pool_percentile": acad_pctile, "display_only": True},
        "integrity": {
            "h_gt_paper": sum(1 for s in sch if s["h"] > s["paper"]),
            "h_gt_paper_pct": round(100 * sum(1 for s in sch if s["h"] > s["paper"]) / n, 2),
            "reference_nums_note": "dwd_scholar.reference_nums 本批未取（A-26 批实测 21,316 行非空 0，整列为空）",
        },
        "probes": {"sql_count": 0, "source": "_snapshots21/probe_a26_20261022.json (A-26 批落盘)",
                   "journal_impact_evidence": "_snapshots21/city_family_probe_20261021.json "
                                              "probes.journal_impact = [2796, 0]"},
    }
    write_out(METRIC, payload)


def statistics_median(vals):
    import statistics
    return round(statistics.median(vals), 2) if vals else None


if __name__ == "__main__":
    main()
