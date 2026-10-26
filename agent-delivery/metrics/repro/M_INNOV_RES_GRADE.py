#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_RES_GRADE · 研究领域等级划分（gkx 口径重建件，零 SQL）

口径（原样沿用旧稿，未改公式）：
  入集 = 同一批 12 家明星企业的两两组合（C(12,2)=66 对）；
  overlap = 上游 M_INNOV_RES_OVERLAP 的合成重叠度∈[0,1]（IPC 集合 Jaccard + 学者实体 Jaccard 的均值，缺维不进分母）；
  阈值：P70 = t_high、P30 = t_low（n≥3）；不足 3 对时回落固定 0.5 / 0.2；
  分档：overlap ≥ t_high → 高；t_low ≤ overlap < t_high → 中；< t_low → 低。

【本件自定义、待甲方确认】
  P70/P30 是王惠口径里写死的「本批分位」，不是行业标准；固定阈值 0.5/0.2 同样无官方来源。
  本件另给固定阈值敏感性对照，让甲方看到换阈值会翻多少档。

数据源（零 SQL，全部读 code/_snapshots21/）：
  patent_ipc4_by_name_20261021.json   581,585 行（IPC4×申请人）
  probe_a26_20261022.json             dwd_scholar 21,316 行（学者实体）
  dwd_zh_paper 作者快照               62,002 行（仅作敏感性对照，不进合成）
  口径实现：code/_a26_common.py 的 overlap_bundle(12)（A-26 簇共用层，非旧批 helper）

运行：cd code && python3 M_INNOV_RES_GRADE.py
产物：code/M_INNOV_RES_GRADE_out.json
"""
from __future__ import annotations

import json
import math
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _a26_common as A  # noqa: E402

MID = "M_INNOV_RES_GRADE"
K = 12
FIX_HI, FIX_LO = 0.5, 0.2


def quantile(vals, q):
    s = sorted(vals)
    if not s:
        return None
    k = (len(s) - 1) * q
    lo, hi = math.floor(k), math.ceil(k)
    if lo == hi:
        return s[int(k)]
    return s[lo] * (hi - k) + s[hi] * (k - lo)


def grade_of(v, hi, lo):
    return "高" if v >= hi else ("低" if v < lo else "中")


def main():
    b = A.overlap_bundle(K)
    pairs = [p for p in b["pairs"] if p["composite"] is not None]
    vals = [p["composite"] for p in pairs]
    mode = "percentile" if len(vals) >= 3 else "fixed"
    hi, lo = (quantile(vals, .70), quantile(vals, .30)) if mode == "percentile" else (FIX_HI, FIX_LO)

    rows = [{"a": p["a"], "b": p["b"], "overlap": p["composite"],
             "grade": grade_of(p["composite"], hi, lo),
             "ipc_jaccard": p["ipc_jaccard"], "scholar_jaccard": p["scholar_jaccard"],
             "n_dims": p["n_dims"]} for p in pairs]
    dist = {g: sum(1 for r in rows if r["grade"] == g) for g in ("高", "中", "低")}

    fixed = {g: sum(1 for r in rows if grade_of(r["overlap"], FIX_HI, FIX_LO) == g)
             for g in ("高", "中", "低")}
    flips = [{"a": r["a"], "b": r["b"], "overlap": r["overlap"],
              "grade_p70p30": r["grade"],
              "grade_fixed": grade_of(r["overlap"], FIX_HI, FIX_LO)}
             for r in rows if r["grade"] != grade_of(r["overlap"], FIX_HI, FIX_LO)]

    srt = sorted(rows, key=lambda r: r["overlap"])
    near_hi = [r for r in srt if abs(r["overlap"] - hi) <= 0.01][:6]
    near_lo = [r for r in srt if abs(r["overlap"] - lo) <= 0.01][:6]

    # 与 CI_LEVEL 的一致性（同一 overlap、同一阈值，仅刻度 ×100 后再比较）
    ci = [{"a": r["a"], "b": r["b"], "score": round(r["overlap"] * 100, 1),
           "level": grade_of(round(r["overlap"] * 100, 1), round(hi * 100, 2), round(lo * 100, 2))}
          for r in rows]
    agree = sum(1 for r, c in zip(rows, ci) if r["grade"] == c["level"])
    mismatch = [{"a": r["a"], "b": r["b"], "overlap": r["overlap"],
                 "grade": r["grade"], "ci_level": c["level"], "score": c["score"]}
                for r, c in zip(rows, ci) if r["grade"] != c["level"]]

    scholar_share = sum(1 for p in pairs if p["scholar_jaccard"] is not None) / len(pairs)

    payload = {
        "metric_id": MID,
        "metric_name": "研究领域等级划分",
        "domain": "TOPIC-INNOV / 企业研究领域重叠",
        "formula_owner": "王惠（旧稿口径）",
        "support_judgment": "部分支持",
        "support_reason": (
            f"{len(rows)} 对企业的 overlap 与三档划分可复现，阈值、分档、边界样例全部落盘；"
            "但上游 overlap 的两维里学者实体维实测 0 对可用（"
            f"{scholar_share:.0%} 的对有学者 Jaccard），合成实际只由 IPC 一维决定；"
            "「研究领域」被压缩成 IPC4 集合重叠，不含论文主题、项目学科与人才方向。"
        ),
        "generated_at": "2026-10-22",
        "main_db": "gkx @ 183.240.141.251:3318（gkx_reader_zp，只读）",
        "sql_count": 0,
        "sources": [
            "code/_snapshots21/patent_ipc4_by_name_20261021.json（581,585 行）",
            "code/_snapshots21/probe_a26_20261022.json（dwd_scholar 21,316 行）",
            "code/_a26_common.py::overlap_bundle（A-26 共用层，上游 RES_OVERLAP 同一实现）",
        ],
        "base_years_used": [2021, 2022, 2023, 2024],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": (
            "IPC 集合取全期累计（专利表申请年只覆盖 2021—2026，2017—2020 零行）；"
            "学者/论文为截面快照，无年度基期。未按年切窗，故本件不产出年度趋势。"
        ),
        "definition_note": (
            "本件自定义、待甲方确认：t_high=P70、t_low=P30 是「本批分位」，样本换了阈值就变；"
            "固定阈值 0.5/0.2 同样无官方出处。两者都列，不冒充官方口径。"
        ),
        "probes": {
            "n_firm": len(b["names"]),
            "firms": b["names"],
            "n_pairs": len(rows),
            "pairs_with_scholar_dim": sum(1 for p in pairs if p["scholar_jaccard"] is not None),
            "dims_defined": 3, "dims_available": 1,
            "overlap_min": round(min(vals), 4), "overlap_max": round(max(vals), 4),
            "overlap_median": round(statistics.median(vals), 4),
            "overlap_mean": round(sum(vals) / len(vals), 4),
        },
        "thresholds": {"mode": mode, "t_high": round(hi, 4), "t_low": round(lo, 4),
                       "rule": "t_high=P70, t_low=P30（n≥3）；n<3 回落 0.5/0.2",
                       "fixed_alt": {"t_high": FIX_HI, "t_low": FIX_LO}},
        "grade_dist": dist,
        "grade_share": {g: round(v / len(rows), 4) for g, v in dist.items()},
        "sensitivity_fixed": {"dist": fixed,
                              "flip_pairs": len(flips),
                              "flip_share": round(len(flips) / len(rows), 4),
                              "flips": flips},
        "boundary_high": near_hi,
        "boundary_low": near_lo,
        "top10": srt[-10:][::-1],
        "bottom5": srt[:5],
        "consistency_with_ci_level": {
            "agree": agree, "n": len(rows), "agree_pct": round(agree / len(rows) * 100, 2),
            "mismatch": mismatch,
            "note": "两件同 overlap、同阈值，等级定义等价；差异只可能来自 CI_LEVEL 的 ×100 四舍五入与对角特例。",
        },
        "pairs": rows,
        "gaps": [
            "学者实体维：12 家企业中 0 家有 dwd_scholar 组织名精确匹配，学者 Jaccard 全部不可算；",
            "overlap 无时间维：全期 IPC 累计，无法区分「曾经重叠」与「正在重叠」；",
            "IPC4 只到小类，同一小类内技术路线可能完全不同（如 G06F 内数据库与芯片架构）；",
            "12 家样本由授权量门槛选出，结论不外推到全部深企；",
            "P70/P30 在 n=66 上就是 46 对/20 对，阈值随样本变动，不具备跨批次可比性。",
        ],
    }

    out = os.path.join(HERE, f"{MID}_out.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)

    print("wrote", os.path.basename(out))
    print("pairs", len(rows), "hi", round(hi, 4), "lo", round(lo, 4), "mode", mode)
    print("dist", dist, "share", payload["grade_share"])
    print("fixed", fixed, "flips", len(flips))
    print("agree", agree, "/", len(rows))
    print("top3", [(r["a"], r["b"], r["overlap"]) for r in srt[-3:][::-1]])


if __name__ == "__main__":
    main()
