#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_SCHOLAR_INFLUENCE · 专家学者影响力（0—100）

口径（calc-logic 真源，王惠迁移版）
--------------------------------
三维加权平均：H 指数 / 被引数量 / 论文数量；院士标签仅展示、不进分。
本脚本把三维各自转成**同一学者池内的百分位分**（0—100），再等权平均。理由见 MD §2.3：
三列量纲差异极大（h 中位 18、被引中位 1,047、发文中位 51），min-max 会被极值压扁，
百分位分对长尾稳健且可解释为「在该学者池中的相对位置」。

数据面（共 2 条 SQL，均 ≤2.2 万行小表）
--------------------------------------
1) `gkx.dwd_scholar` 21,316 行窄列 → 已由 `_probe_a26.py` 落盘；
2) `gkx.dwd_scholar_talent_flag` 取院士名单（112 人），仅用于展示标记。

运行：python3 code/M_INNOV_SCHOLAR_INFLUENCE.py
"""
from __future__ import annotations

import json
import math
import os
import statistics
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _a26_common as C
from _gkxdb import gkx

MID = "M_INNOV_SCHOLAR_INFLUENCE"
W = {"h_index": 1 / 3, "citation_nums": 1 / 3, "paper_nums": 1 / 3}


def academicians() -> list[str]:
    cur = gkx()
    try:
        cur.execute("SET SESSION max_execution_time=30000")
        cur.execute("SELECT scholar_id FROM gkx.dwd_scholar_talent_flag WHERE academician=1")
        return sorted({r[0] for r in cur.fetchall() if r[0]})
    except Exception as e:  # 院士名单只影响展示，取不到不阻断主结果
        print("[warn] academician query failed:", e)
        return []
    finally:
        cur.close()


def main() -> None:
    S = C.scholars()
    n = len(S)
    acad = set(academicians())

    for key in ("h_index", "citation_nums", "paper_nums"):
        vals = [float(s[key]) for s in S]
        C._CACHE[f"r_{key}"] = C.rank_pct(vals)

    # 主口径：log1p 后池内 min-max（0—100），避免三列量纲差异与长尾压扁；
    # 敏感性口径：池内百分位分（等权），用于检验排序稳健性。
    logs = {}
    for key in W:
        v = [math.log1p(float(s[key])) for s in S]
        lo, hi = min(v), max(v)
        logs[key] = [100 * (x - lo) / (hi - lo) if hi > lo else 50.0 for x in v]

    for i, s in enumerate(S):
        s["score"] = round(sum(W[k] * logs[k][i] for k in W), 2)
        s["score_pct"] = round(sum(W[k] * C._CACHE[f"r_{k}"][i] for k in W), 2)

    scores = [s["score"] for s in S]
    pct_scores = [s["score_pct"] for s in S]
    # 分档：百分位分等距五档，用于展示
    def tier(x: float) -> str:
        if x >= 80:
            return "T1 领军"
        if x >= 60:
            return "T2 骨干"
        if x >= 40:
            return "T3 中坚"
        if x >= 20:
            return "T4 成长"
        return "T5 起步"

    for s in S:
        s["tier"] = tier(s["score"])

    tiers = defaultdict(int)
    for s in S:
        tiers[s["tier"]] += 1

    # 敏感性：池内百分位分等权，用于检验排序稳健性
    alt = pct_scores
    rho = C.spearman(scores, alt)

    # 机构聚合（按学者所属机构名，2,108 个机构）
    org = defaultdict(list)
    for s in S:
        if s["org"]:
            org[s["org"]].append(s)
    org_rows = []
    for k, v in org.items():
        if len(v) < 10:
            continue
        org_rows.append({"org": k, "n": len(v),
                         "mean_score": round(statistics.mean(x["score"] for x in v), 2),
                         "median_h": round(statistics.median(x["h_index"] for x in v), 1),
                         "sum_citation": sum(x["citation_nums"] for x in v)})
    org_rows.sort(key=lambda r: (-r["mean_score"], -r["n"]))

    # 完整性体检：h 不可能大于发文量（Hirsch 定义）
    conflict = [s for s in S if s["h_index"] > s["paper_nums"]]
    zero_paper = [s for s in S if s["paper_nums"] == 0]
    zero_cite = [s for s in S if s["citation_nums"] == 0]

    top = sorted(S, key=lambda s: (-s["score"], -s["citation_nums"], s["scholar_id"]))[:50]
    acad_rows = [s for s in S if s["scholar_id"] in acad]
    acad_scored = sorted(acad_rows, key=lambda s: -s["score"])

    # 院校 vs 企业：用机构名尾缀粗分，仅作展示结构
    def org_kind(name: str) -> str:
        if any(k in name for k in ("大学", "学院", "学校")):
            return "高校"
        if "研究院" in name or "研究所" in name or "科学院" in name:
            return "院所"
        if "医院" in name:
            return "医院"
        if "公司" in name or "集团" in name or "厂" in name:
            return "企业"
        return "其他"

    kinds = defaultdict(list)
    for s in S:
        kinds[org_kind(s["org"])].append(s["score"])

    res = {
        "metric_id": MID,
        "metric_name": "专家学者影响力",
        "support_judgment": "完全转换支持",
        "generated_from": "gkx.dwd_scholar 21,316 行（窄列快照）+ gkx.dwd_scholar_talent_flag 院士名单",
        "sql_count": 2,
        "method": {
            "formula": "score = 100 × Σ w_k · norm_k，w=(1/3,1/3,1/3)，k∈{h_index, citation_nums, paper_nums}",
            "normalization": "主口径：log1p 后在 21,316 人池内 min-max；敏感性口径：池内百分位（rank/(n-1)×100，并列取平均秩）",
            "weight_note": "calc-logic 写「加权平均」但未给权重，本版等权；等权是口径缺省，不是数据结论",
            "academician": "仅作展示标记，不进分（口径明示）",
        },
        "coverage": {
            "n_scholars": n,
            "distinct_scholar_id": len({s["scholar_id"] for s in S}),
            "h_index_notnull": sum(1 for s in S if s["h_index"] is not None),
            "h_index_positive": sum(1 for s in S if s["h_index"] > 0),
            "citation_positive": sum(1 for s in S if s["citation_nums"] > 0),
            "paper_positive": sum(1 for s in S if s["paper_nums"] > 0),
            "org_filled": sum(1 for s in S if s["org"]),
            "org_distinct": len(org),
            "academician_flagged": len(acad),
            "talent_flag_rows": 20030,
        },
        "dim_stats": {
            "h_index": C.st(dim_vals := [float(s["h_index"]) for s in S]),
            "citation_nums": C.st([float(s["citation_nums"]) for s in S]),
            "paper_nums": C.st([float(s["paper_nums"]) for s in S]),
        },
        "score_stats": C.st(scores),
        "score_hist_10pt": [[b, sum(1 for x in scores if b <= x < b + 10)] for b in range(0, 100, 10)],
        "tiers": dict(sorted(tiers.items())),
        "sensitivity": {
            "alt": "池内百分位等权（与主口径仅差单调变换的稳健性对照）",
            "spearman_main_vs_alt": rho,
            "top50_overlap": len({s["scholar_id"] for s in top} &
                                 {S[i]["scholar_id"] for i in sorted(range(n), key=lambda i: -alt[i])[:50]}),
        },
        "integrity": {
            "h_gt_paper_rows": len(conflict),
            "h_gt_paper_pct": round(100 * len(conflict) / n, 4),
            "zero_paper_rows": len(zero_paper),
            "zero_citation_rows": len(zero_cite),
            "note": "h_index>paper_nums 违反 Hirsch 定义，属供应方字段内部矛盾；本版保留原值并打标，不静默修正",
        },
        "org_dim": {
            "n_orgs_ge10": len(org_rows),
            "top20": org_rows[:20],
        },
        "academician_dim": {
            "n": len(acad_rows),
            "median_score": round(statistics.median(x["score"] for x in acad_rows), 2) if acad_rows else None,
            "median_rank_pct_of_all": round(100 * sum(1 for s in S if s["score"] < statistics.median(
                x["score"] for x in acad_rows)) / n, 2) if acad_rows else None,
            "top10": [{"scholar_id": s["scholar_id"], "name": s["name"], "org": s["org"],
                       "h_index": s["h_index"], "citation_nums": s["citation_nums"],
                       "paper_nums": s["paper_nums"], "score": s["score"]} for s in acad_scored[:10]],
        },
        "kind_dim": {k: {"n": len(v), "mean": round(statistics.mean(v), 2)} for k, v in kinds.items()},
        "top50": [{"rank": i + 1, "scholar_id": s["scholar_id"], "name": s["name"], "org": s["org"],
                   "h_index": s["h_index"], "citation_nums": s["citation_nums"],
                   "paper_nums": s["paper_nums"], "score": s["score"], "tier": s["tier"],
                   "academician": s["scholar_id"] in acad} for i, s in enumerate(top)],
        "base_year_block": C.base_year_block([], [], "本指标为截面排行，无年度分母需求"),
        "gaps": [
            "h_index / citation_nums 为供应方外采值，库内无逐篇引用明细，无法复算 Hirsch 值",
            "719 行 h_index>paper_nums（3.37%）字段内部矛盾，只能打标不能修正",
            "21,316 位学者为库内学者池，不等于全国学者总体；跨库比较需统一学者 ID",
            "dwd_scholar.scholar_org_id 全空，机构维只能按名称字符串聚合",
        ],
    }
    C.write_out(MID, res)
    print(json.dumps({k: res[k] for k in ("support_judgment", "score_stats", "tiers")},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
