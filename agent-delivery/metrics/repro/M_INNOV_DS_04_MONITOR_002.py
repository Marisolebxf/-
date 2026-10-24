#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""创新点价值评估（M_INNOV_DS_04_MONITOR_002）—— 词条级 · **详情视角**

父件是 `M_INNOV_DS_04_MONITOR_001`（同一批词条、同一套 burst 与 is_new）。本件对
**已入选的候选词条**逐条打分，回答「这条候选值不值得跟」，而不是重新发现候选。

王惠口径（calc-logic INNOV V1.5-20260829 / M_INNOV_POINT_VALUE）：
  新颖性   = 1 / (1 + T − 首次出现年)
  影响潜力 = 专利被引合计 + 中文论文被引合计
  成熟度   = 授权专利件数 / 专利件数
  合成分   = 三维极值归一后加权平均 ×100；**缺测维不补 0，剩余维重归一**

本件的实测结论：三维里只有**新颖性**是逐件实测、**成熟度**只能分摊估算、
**影响潜力在词条层不可算**（被引表 20,515 行里只有 467 个 pn 能连回专利主表，2.28%）。
因此合成分是「二维重归一」口径，不是王惠的三维等权原式。

重建背景：原稿读 20261020 目录的共享 bundle（连演示库 + 2017—2020 补零，DATA_FACTS §3.19），
本脚本零 SQL、零 bundle，候选与三维原始值全部现算。

产物：code/M_INNOV_DS_04_MONITOR_002_out.json
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import _a25_common as A
import _ds04_common as D

METRIC = "M_INNOV_DS_04_MONITOR_002"
MIN_RECENT = 3
DIMS_AVAILABLE = ("novelty", "maturity")
DIMS_MISSING = ("impact",)


def candidates() -> list:
    """复算 MONITOR_001 的 IPC4 候选集（同一口径、同一输入，独立算一遍）。"""
    ipc = D.ipc_year()
    years = sorted({y for yc in ipc.values() for y in yc})
    rows = []
    for term, yc in ipc.items():
        st = D.window_stats(yc, D.BASE_FORMULA, D.RECENT, years)
        if st["recent_total"] < MIN_RECENT:
            continue
        if not (st["burst"] >= 1 or (st["t0"] is not None and st["t0"] >= D.T - 2)):
            continue
        st["term"] = term
        st["year_counts"] = {str(y): yc[y] for y in sorted(yc)}
        rows.append(st)
    rows.sort(key=lambda r: (-r["burst"], -r["recent_total"], r["term"]))
    return rows


def cited_joinability() -> dict:
    """专利被引表能否连回专利主表——决定「影响潜力」在词条层能不能算。"""
    facts = A.facts()
    cited = (facts.get("cited_rows") or [{}])[0]
    link = (facts.get("cited_link") or [{}])[0]
    n_cited = int(cited.get("n") or 0)
    n_link = int(link.get("n") or 0)
    return {
        "cited_rows": n_cited,
        "pn_joinable": n_link,
        "join_rate": round(n_link / n_cited, 4) if n_cited else None,
        "cited_positive": int(cited.get("pos") or 0),
        "cited_max": int(cited.get("mx") or 0),
        "table_rows": 2939895,
        "coverage_of_patents": round(n_link / 2939895, 6),
        "note": ("`dwd_patent_cited` 20,515 行、其中 3,657 行被引>0、最大 55；"
                 "但只有 467 个 pn 能在 `dwd_patent` 命中（2.28%），"
                 "而 467 个 pn 再按 IPC4 归并后几乎全落在候选集之外，"
                 "词条级「被引合计」在 gkx 上不成立"),
    }


def paper_side() -> dict:
    """论文关键词侧：被引**可以**逐词条算（分类表 20,048 篇里 20,031 篇有被引记录）。"""
    tp = A.term_panel()
    p_year = A.paper_year_all()
    years = sorted(y for y in p_year if p_year[y] > 0)
    rows = []
    for term, yc in tp["kwa"].items():
        st = D.window_stats(yc, D.BASE_FORMULA, D.RECENT, years)
        if st["recent_total"] < MIN_RECENT:
            continue
        rows.append({
            "term": term, "burst": st["burst"], "recent_total": st["recent_total"],
            "t0": st["t0"], "novelty": D.novelty(st["t0"]),
            "citations": round(tp["kwa_cite"].get(term, 0.0), 1),
            "base_years_used": st["base_years_used"],
        })
    return {
        "n_terms": len(rows),
        "note": ("论文关键词侧只有 2 个词条满足近窗≥3，被引维可算但样本量不足以成排名；"
                 "列在此处只为说明「影响潜力缺的是专利侧，不是论文侧」"),
        "rows": rows,
    }


def main():
    t0 = time.time()
    rows = candidates()
    mat = D.ipc_maturity()
    mat_meta = D.maturity_meta()

    for r in rows:
        r["novelty"] = D.novelty(r["t0"])
        m = mat.get(r["term"]) or {}
        r["patent_n"] = m.get("n")
        r["n_applicants"] = m.get("n_applicants")
        r["granted_est"] = m.get("granted_est")
        r["maturity_est"] = m.get("grant_rate_est")
        r["impact"] = None                      # 缺测，不补 0

    nv = [r["novelty"] for r in rows]
    mt = [r["maturity_est"] for r in rows if r["maturity_est"] is not None]
    nn = D.minmax(nv)
    mn = D.minmax(mt)
    for r, a, b in zip(rows, nn, mn):
        r["norm_novelty"] = round(a, 4)
        r["norm_maturity"] = round(b, 4)
        r["value_score"] = round(100 * (a + b) / 2, 1)   # 二维重归一（缺测维不参与权重）
    rows.sort(key=lambda r: (-r["value_score"], -(r["recent_total"] or 0), r["term"]))
    for i, r in enumerate(rows, 1):
        r["rank"] = i
        r["missing_dims"] = list(DIMS_MISSING)

    scores = [r["value_score"] for r in rows]
    year_spread = sorted({r["t0"] for r in rows})
    mat_spread = sorted({r["maturity_est"] for r in rows})

    out = {
        "metric_id": METRIC,
        "name": "创新点价值评估",
        "vendor_metric": "M_INNOV_POINT_VALUE",
        "formula_owner": "王惠",
        "view": "detail",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "runtime_sec": None,
        "data_source": ("父件候选集来自 gkx.dwd_patent IPC 小类全量缓存；"
                        "成熟度来自 star_applicant_agg（全量 169,226 名）× patent_ipc4_by_name（全量 581,585 组）"),
        "db": "gkx @ 183.240.141.251:3318（只读，本脚本零 SQL）",
        "definition": ("对 MONITOR_001 的候选词条逐条打分：新颖性 1/(1+T−t0)、"
                       "影响潜力（专利被引+论文被引）、成熟度（授权/件数），"
                       "极值归一后加权平均 ×100；缺测维不补 0，剩余维重归一。"),
        "statistical_year": D.T,
        "windows": {"recent": list(D.RECENT), "base_formula": list(D.BASE_FORMULA),
                    "base_used": list(D.BASE_USED_PATENT)},
        "params": {
            "weights": "equal among available dims",
            "dims_available": list(DIMS_AVAILABLE),
            "dims_missing": list(DIMS_MISSING),
            "norm": "min-max within candidate set; all-equal → 0.5",
            "missing_dim_policy": "不补 0，剩余维重归一（王惠原式）",
            "n_dims_scored": 2,
        },

        # ---- 硬约束：基期三字段进顶层 ----
        "base_years_used": list(D.BASE_USED_PATENT),
        "base_years_missing": list(D.BASE_MISSING_PATENT),
        "base_years_note": D.BASE_NOTE,

        "family": {
            "group": "M_INNOV_DS_04（科技发展态势·全球创新监测）",
            "this": "MONITOR_002 = 词条级突现监测的**详情视角**（逐候选三维价值分）",
            "parent": "M_INNOV_DS_04_MONITOR_001（列表视角，候选主键即本件的 point_key）",
            "sibling": {
                "M_INNOV_DS_04_REALTIME_004": "实体换成机构/IPC 节点，算产出规模与影响分",
                "M_INNOV_DS_04_REALTIME_005": "在节点年序列上做 Holt 外推",
            },
        },

        "probes": {
            "cited_joinability": cited_joinability(),
            "maturity": mat_meta,
            "patent_cited_table": {"rows": 20515, "positive": 3657, "max": 55},
            "zh_paper_citation": {"rows": 20031, "max": 670, "positive": 20031},
            "candidate_universe": {"n_candidates": len(rows), "min_recent": MIN_RECENT},
        },
        "paper_side": paper_side(),
        "compute": {
            "n_scored": len(rows),
            "value_min": min(scores) if scores else None,
            "value_max": max(scores) if scores else None,
            "value_mean": round(sum(scores) / len(scores), 2) if scores else None,
            "value_median": round(sorted(scores)[len(scores) // 2], 2) if scores else None,
            "value_dist": D.dist(scores),
            "distinct_novelty": len(set(nv)),
            "distinct_first_year": len(year_spread),
            "distinct_maturity": len(mat_spread),
            "novelty_range": [min(nv), max(nv)] if nv else None,
            "maturity_range": [min(mt), max(mt)] if mt else None,
            "impact_coverage": 0.0,
            "impact_note": "影响潜力在词条层覆盖 0.0（被引不可连），未参与权重",
        },
        "top": rows,

        "quarantine_delta": {
            "why": ("隔离前旧稿读 20261020 共享 bundle（演示库 + 2017—2020 补零），"
                    "且成熟度用 `kind IN ('B','U')` 近似授权、被引直接取 bundle 值"),
            "old_vs_new": [
                {"item": "打分词条数", "old": 30, "new": len(rows),
                 "cause": "旧稿只取 bundle 的 Top30 切片；本件对全部 33 个候选逐条打分"},
                {"item": "value_min", "old": 16.7, "new": min(scores) if scores else None,
                 "cause": "候选集与成熟度口径同时变化"},
                {"item": "value_max", "old": 66.3, "new": max(scores) if scores else None,
                 "cause": "同上；旧稿最高分来自 C07K14/015（首现 2022 的新颖性优势）"},
                {"item": "被引为 0 的候选占比", "old": 1.0, "new": None,
                 "cause": "本件不把「被引不可连」写成 0，而是标为缺测并不参与权重"},
                {"item": "新颖性取值个数", "old": 2, "new": len(set(nv)),
                 "cause": "旧稿候选首现年只有 2021/2022；本件含 2023 年首现（B60V）"},
            ],
        },
        "support_judgment": "部分支持",
        "support_basis": (
            "候选集（33 条）与新颖性（t0 全量 IPC 面板）是逐件实测；成熟度只能按"
            "「申请人在其各 IPC 上授权率一致」的分摊法估算（全表两侧，合计可复核）；"
            "影响潜力在词条层不可算（被引表 pn 与专利主表连通率 2.28%，且落不到候选 IPC 上），"
            "故合成分是二维重归一，不是王惠三维等权原式——按「始终有部分依赖维拿不到数据」判部分支持。"),
        "reasons": [
            "新颖性可算但被库内年份截断：t0 最小 2021，故 1/(1+T−t0) 只能取 0.25/0.333/0.5 三档，"
            "不是连续量，排名分辨率低；",
            "影响潜力缺测：dwd_patent_cited 仅 20,515 行（占专利 0.70%），"
            "其中 467 个 pn 能连回主表（2.28%），词条级被引合计无法闭合；",
            "成熟度为分摊估算：逐件授权号在 granted_number 上有，但按 IPC 聚合需对 294 万行无索引表 "
            "GROUP BY（§3.6 禁止），只能用「申请人授权率 × 该 IPC 件数」分摊，"
            "全量合计 %s 件、对应授权率 %.2f%%，与全表 72.81%% 差 %.2f 个百分点（无 IPC 的 51.9 万件未进分母）；"
            % (f"{mat_meta['sum_granted_est']:,.0f}", 100 * mat_meta["sum_granted_est"] / mat_meta["sum_n"],
               100 * 0.7281 - 100 * mat_meta["sum_granted_est"] / mat_meta["sum_n"]),
            "论文侧被引可算（20,031 篇全部有值、最大 670），但论文关键词只有 2 个候选，"
            "不能把「影响潜力」这一维从专利侧挪到论文侧补足；",
            "三维权重王惠原文只写「加权平均」未给具体权重，本件取等权并在 params 里写明，属口径假设。",
        ],
        "notes": [
            "本脚本零 SQL、无 reused_from；候选集在本脚本内独立复算，与 MONITOR_001 同一口径。",
            "value_score 的绝对高低不可跨批次比较：min-max 是在 33 条候选内做的。",
            "成熟度是估算值，`granted_est` 与 `maturity_est` 必须与 `is_estimate=true` 一起展示。",
            "不要把本件的 value_score 当作「创新点价值排名」对外发布：它只用了两维，"
            "影响潜力维缺失会让高被引的老词条系统性偏低。",
        ],
    }
    out["runtime_sec"] = round(time.time() - t0, 1)

    p = D.write_out(METRIC, out)
    print("written", p)
    print("n", len(rows), "score", min(scores), max(scores),
          "mean", out["compute"]["value_mean"])
    print("top5:", [(r["term"], r["value_score"], r["novelty"], r["maturity_est"]) for r in rows[:5]])
    print("bottom3:", [(r["term"], r["value_score"]) for r in rows[-3:]])
    print("paper side:", out["paper_side"]["n_terms"])


if __name__ == "__main__":
    main()
