#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_RES_CI_LEVEL · 竞争情报等级（gkx 口径重建件，零 SQL）

口径（原样沿用旧稿）：
  对象 = 12 家明星企业的企业对（含对角）；
  分值 = overlap × 100（overlap 来自上游 M_INNOV_RES_OVERLAP 的合成重叠度）；
  阈值 = 与 M_INNOV_RES_GRADE 同一套（P70/P30，页面可改）；
  对角 = 同一企业，固定 100 分 /「高」，且**不进入** P70/P30 计算；
  输出 = 企业对清单 + 12×12 竞争矩阵。

【本件自定义、待甲方确认】
  「高/中/低」三档断点由本批 P70/P30 决定，不是官方或行业标准；页面若改阈值，分档会整体移动。

数据源（零 SQL）：同 M_INNOV_RES_GRADE，读 code/_snapshots21/，
口径实现为 code/_a26_common.py::overlap_bundle(12)。

运行：cd code && python3 M_INNOV_RES_CI_LEVEL.py
产物：code/M_INNOV_RES_CI_LEVEL_out.json
"""
from __future__ import annotations

import json
import math
import os
import statistics
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _a26_common as A  # noqa: E402

MID = "M_INNOV_RES_CI_LEVEL"
K = 12


def quantile(vals, q):
    s = sorted(vals)
    if not s:
        return None
    k = (len(s) - 1) * q
    lo, hi = math.floor(k), math.ceil(k)
    if lo == hi:
        return s[int(k)]
    return s[lo] * (hi - k) + s[hi] * (k - lo)


def stats(vals):
    s = sorted(vals)
    n = len(s)
    return {"n": n, "min": round(s[0], 2), "p25": round(quantile(s, .25), 2),
            "median": round(statistics.median(s), 2), "mean": round(sum(s) / n, 2),
            "p75": round(quantile(s, .75), 2), "p90": round(quantile(s, .90), 2),
            "max": round(s[-1], 2)}


def main():
    b = A.overlap_bundle(K)
    names = b["names"]
    pairs = [p for p in b["pairs"] if p["composite"] is not None]
    vals = [p["composite"] for p in pairs]
    hi, lo = quantile(vals, .70) * 100, quantile(vals, .30) * 100

    def level(s):
        return "高" if s >= hi else ("低" if s < lo else "中")

    rows = [{"a": p["a"], "b": p["b"], "overlap": p["composite"],
             "score": round(p["composite"] * 100, 1),
             "ci_level": level(round(p["composite"] * 100, 1)),
             "ipc_jaccard": p["ipc_jaccard"], "scholar_jaccard": p["scholar_jaccard"]}
            for p in pairs]
    for r in rows:
        r["ci_level"] = level(r["score"])
    dist = {g: sum(1 for r in rows if r["ci_level"] == g) for g in ("高", "中", "低")}
    scores = [r["score"] for r in rows]
    bins = [0] * 10
    for s in scores:
        bins[min(9, max(0, int(s // 10)))] += 1

    matrix = b["matrix"]

    # 每家企业的「竞争强度」画像：对手均分、最高对手、高档对手数
    per = {}
    for n in names:
        mine = [r for r in rows if n in (r["a"], r["b"])]
        sc = [r["score"] for r in mine]
        best = max(mine, key=lambda r: r["score"])
        per[n] = {
            "n_pairs": len(mine),
            "avg_score": round(sum(sc) / len(sc), 2) if sc else None,
            "max_score": round(best["score"], 2),
            "max_partner": best["b"] if best["a"] == n else best["a"],
            "high_level_partners": sum(1 for r in mine if r["ci_level"] == "高"),
            "papers": b.get("papers", {}).get(n, 0),
            "ipc_count": len(b["ipc_sets"].get(n, [])),
        }

    payload = {
        "metric_id": MID,
        "metric_name": "竞争情报等级",
        "domain": "TOPIC-INNOV / 企业竞争情报",
        "formula_owner": "王惠（旧稿口径）",
        "support_judgment": "部分支持",
        "support_reason": (
            f"{len(rows)} 对企业的分值、三档等级与 12×12 矩阵均可复现，且与 RES_GRADE 100% 同档；"
            "但分值完全由 IPC4 集合 Jaccard 决定——学者维 0 对可用，论文主题、项目学科、市场重叠均未进入；"
            "「竞争情报」在本库只能读作「技术分类重叠度」，不能读作市场竞争强度。"
        ),
        "generated_at": "2026-10-22",
        "main_db": "gkx @ 183.240.141.251:3318（gkx_reader_zp，只读）",
        "sql_count": 0,
        "sources": [
            "code/_snapshots21/patent_ipc4_by_name_20261021.json（581,585 行）",
            "code/_snapshots21/probe_a26_20261022.json（dwd_scholar 21,316 行）",
            "code/_a26_common.py::overlap_bundle（上游 RES_OVERLAP 同一实现）",
        ],
        "base_years_used": [2021, 2022, 2023, 2024],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": (
            "IPC 集合为全期累计；专利表申请年只有 2021—2026（2017—2020 零行），"
            "故不产出年度竞争强度序列，只给截面矩阵。"
        ),
        "definition_note": (
            "本件自定义、待甲方确认：分值 = overlap×100 是线性刻度，不改变名次；"
            "高/中/低断点取本批 P70/P30，属统计惯例，无官方出处。"
        ),
        "probes": {
            "n_firm": len(names), "n_pairs": len(rows),
            "pairs_with_scholar_dim": sum(1 for p in pairs if p["scholar_jaccard"] is not None),
            "matrix_cells": len(matrix) * len(matrix) if matrix else 0,
        },
        "formula": {"score": "overlap × 100",
                    "thresholds": {"t_high": round(hi, 2), "t_low": round(lo, 2),
                                   "rule": "score ≥ t_high → 高；t_low ≤ score < t_high → 中；否则 低"}},
        "diagonal_rule": {"score": 100, "ci_level": "高", "excluded_from_percentile": True,
                          "note": "对角为同一企业，按旧稿固定 100/高，不进入 P70/P30"},
        "score_stats": stats(scores),
        "histogram_10bin": {"bins": [f"[{i*10},{i*10+10})" for i in range(10)], "counts": bins},
        "level_dist": dist,
        "level_share": {g: round(v / len(rows), 4) for g, v in dist.items()},
        "top10": sorted(rows, key=lambda r: -r["score"])[:10],
        "bottom5": sorted(rows, key=lambda r: r["score"])[:5],
        "boundary_high": sorted(rows, key=lambda r: abs(r["score"] - hi))[:5],
        "boundary_low": sorted(rows, key=lambda r: abs(r["score"] - lo))[:5],
        "per_enterprise": per,
        "matrix": {"names": names, "values": matrix,
                   "note": "对角 100；非对角为 overlap×100；None 表示上游 overlap 不可算"},
        "consistency_with_grade": {
            "same_threshold_source": f"P70={round(hi,2)} / P30={round(lo,2)}（与 RES_GRADE 同一 overlap）",
            "expected_agreement": "100%",
            "note": "两件等级定义等价，产品页不必重复计算，直接由 overlap 派生即可。",
        },
        "pairs": rows,
        "gaps": [
            "学者维全部缺失：12 家企业中 0 家有精确匹配的学者组织记录，Jaccard 只由 IPC 一维构成；",
            "无市场重叠数据：客户、产品线、招投标、出口市场均无表，竞争强度不等于市场竞争；",
            "IPC4 小类粒度：同小类内可能完全无竞争（如 G06F 覆盖数据库与芯片架构）；",
            "12 家样本按授权量选取，未覆盖中小企业与外资企业；",
            "分值为截面，不反映竞争态势的时间演化（专利年表从 2021 才完整）。",
        ],
    }

    out = os.path.join(HERE, f"{MID}_out.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)

    print("wrote", os.path.basename(out))
    print("pairs", len(rows), "hi", round(hi, 2), "lo", round(lo, 2))
    print("stats", payload["score_stats"], "dist", dist)
    print("hist", bins)
    print("top3", [(r["a"], r["b"], r["score"], r["ci_level"]) for r in payload["top10"][:3]])
    print("matrix", len(matrix), "x", len(matrix[0]) if matrix else 0)


if __name__ == "__main__":
    main()
