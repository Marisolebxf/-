#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TECH_STAGE_JUDGE —— 技术阶段判定（初级 / 中级 / 高级，含得分表与瓶颈）。

与同族 137（技术阶段分析模型）的分工：
  - 137 用「增长规则」判形态三档（增长 / 平台 / 收缩），把收缩叫「高级」；
  - 本件用「得分表」判技术阶段：规模 40 + 成熟度 40 + 动能 20，满分 100，
    高分 = 已进入规模化应用阶段。两者语义不同，§四给交叉表，不互相覆盖。

口径（单一，深圳）：
  - 域 = IPC 主分类前 4 位；门槛 n2024 >= 100；只统计深圳市申请人；
  - 规模分 = n2024 的对数刻度（100 件=0，10,000 件=100），权重 40%；
  - 成熟度分 = 五维成熟度（见 `_tech21_domainfeat.py`），权重 40%；
  - 动能分 = 样本内百分位（总增长 60% + 近端增长 40%），权重 20%；
  - 为什么动能只占 20%：阶段的主判据是「走到哪一段」（规模 + 成熟度），
    增长是「还在不在往前走」的修正项；若给动能 40%，小体量暴涨域会被抬到中级，
    与生命周期判定的「萌芽」冲突（初版即如此，已改）。
  - 全国件数不参与评分，只用于 §2.6 的 LQ 参照表。

零 SQL：只读 _snapshots21 / _snapshots_gkx21 授权缓存。
"""
from __future__ import annotations

import collections
import statistics

import _tech21_scope as sc
import _tech21_domainfeat as feat

METRIC = "M_TECH_STAGE_JUDGE"
YEARS = feat.YEARS
W = {"size": 0.40, "maturity": 0.40, "energy": 0.20}
CUTS = [40, 60]  # 初级 <40 <= 中级 <60 <= 高级


def life_stage(r):
    n = r["n"]
    g_total = (n[3] - n[0]) / n[0] if n[0] else None
    g_near = (n[3] - n[2]) / n[2] if n[2] else None
    if g_total is None or g_near is None:
        return "缺基期"
    if g_total >= 1.00 and n[0] < 500 and n[3] < 1500:
        return "萌芽"
    if g_total <= -0.20 or g_near <= -0.20:
        return "衰退"
    if g_total >= 0.20 and g_near > 0:
        return "成长"
    return "成熟"


def rank_pct(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    n = len(values)
    out = [0.0] * n
    for rank, i in enumerate(order):
        out[i] = 100.0 * rank / (n - 1) if n > 1 else 50.0
    return out


def main():
    rows, meta = feat.build()
    energy = [0.6 * a + 0.4 * b for a, b in zip(
        rank_pct([r["g_total"] for r in rows]),
        rank_pct([r["g_near"] for r in rows]))]

    scored = []
    for r, e in zip(rows, energy):
        size_p = feat.s_size(r["n2024"])
        total = W["size"] * size_p + W["maturity"] * r["maturity_score"] + W["energy"] * e
        dims = {"规模": size_p, "成熟度": r["maturity_score"], "动能": e}
        bottleneck = min(dims, key=dims.get)
        stage = "初级" if total < CUTS[0] else ("中级" if total < CUTS[1] else "高级")
        scored.append({
            "ipc4": r["ipc4"], "label": r["label"], "n": r["n"], "n2024": r["n2024"],
            "g_total": r["g_total"], "g_near": r["g_near"],
            "score_size": round(size_p, 1),
            "score_energy": round(e, 1),
            "score_maturity": round(r["maturity_score"], 1),
            "score_total": round(total, 2),
            "stage": stage,
            "bottleneck": bottleneck,
            "potential_rank": round(e, 1),
            "life_stage": life_stage(r),
            "new_code": r["new_code"],
        })
    scored.sort(key=lambda r: -r["score_total"])

    dist = collections.Counter(r["stage"] for r in scored)
    stage_block = {}
    for st in ("初级", "中级", "高级"):
        sub = [r for r in scored if r["stage"] == st]
        stage_block[st] = {
            "domains": len(sub),
            "share": round(len(sub) / len(scored), 4),
            "n2024": sum(r["n2024"] for r in sub),
            "n2024_share": round(sum(r["n2024"] for r in sub) / meta["qualified_total_2024"], 4),
            "median_score": round(statistics.median(r["score_total"] for r in sub), 2),
            "examples": [r["ipc4"] for r in sub[:6]],
        }

    # 阶段 × 生命周期交叉
    cross = collections.Counter((r["stage"], r["life_stage"]) for r in scored)
    cross_tab = [{"stage": st, "萌芽": cross[(st, "萌芽")], "成长": cross[(st, "成长")],
                  "成熟": cross[(st, "成熟")], "衰退": cross[(st, "衰退")]}
                 for st in ("初级", "中级", "高级")]

    # 瓶颈分布
    bottleneck = collections.Counter(r["bottleneck"] for r in scored)
    bn_by_stage = {st: dict(collections.Counter(
        r["bottleneck"] for r in scored if r["stage"] == st))
        for st in ("初级", "中级", "高级")}
    buckets = [(">=70", 70, 1e9), ("60-70", 60, 70), ("50-60", 50, 60),
               ("40-50", 40, 50), ("<40", -1e9, 40)]
    score_buckets = [{"band": b, "domains": sum(1 for r in scored if lo <= r["score_total"] < hi),
                      "share": round(sum(1 for r in scored if lo <= r["score_total"] < hi) / len(scored), 4)}
                     for b, lo, hi in buckets]

    # 权重敏感性：三套权重下的阶段分布与头部
    def run_weights(w):
        tmp = []
        for r, e in zip(rows, energy):
            t = w["size"] * feat.s_size(r["n2024"]) + w["maturity"] * r["maturity_score"] + w["energy"] * e
            st = "初级" if t < CUTS[0] else ("中级" if t < CUTS[1] else "高级")
            tmp.append({"ipc4": r["ipc4"], "score": round(t, 2), "stage": st})
        tmp.sort(key=lambda x: -x["score"])
        c = collections.Counter(x["stage"] for x in tmp)
        return {"weights": w, "dist": {k: c[k] for k in ("初级", "中级", "高级")},
                "top5": [[x["ipc4"], x["score"]] for x in tmp[:5]]}

    sens = [
        run_weights({"size": 0.40, "maturity": 0.40, "energy": 0.20}),
        run_weights({"size": 0.30, "maturity": 0.30, "energy": 0.40}),
        run_weights({"size": 0.50, "maturity": 0.30, "energy": 0.20}),
    ]
    # 新码敏感性
    no_new = [r for r in scored if not r["new_code"]]
    new_watch = [r for r in scored if r["new_code"]]

    # LQ 参照（只作参照表）
    nat_cell, nat_year = sc.load_nat_ipc()
    sz_year = {int(k): v for k, v in meta["sz_year_total"].items()}
    for r in scored:
        n24 = r["n2024"]
        r["lq_2024"] = round(((n24 / sz_year[2024]) /
                              (nat_cell[(r["ipc4"], 2024)] / nat_year[2024])), 4) \
            if nat_cell.get((r["ipc4"], 2024)) else None

    lq_ref = []
    # 参照表取「规模前 10」与「LQ 前 3」的并集：
    # 正文 §2.6 的表既列了规模头部，也点名了「LQ 次高」的 G09G（规模只排到第 40 名开外），
    # 原来只取 scored[:10]，导致 G09G 那一行的 nat_2024 / LQ 在 out.json 里查不到，
    # 只能重跑脚本才能核对。取并集后正文出现的每一行都能在产物里指到。
    lq_top3 = sorted([r for r in scored if r.get("lq_2024") and r["n2024"] >= 1000],
                     key=lambda r: -r["lq_2024"])[:3]
    ref_rows, seen_ipc = [], set()
    for r in scored[:10] + lq_top3:
        if r["ipc4"] in seen_ipc:
            continue
        seen_ipc.add(r["ipc4"])
        ref_rows.append(r)
    for r in ref_rows:
        nat24 = nat_cell.get((r["ipc4"], 2024))
        lq_ref.append({
            "ipc4": r["ipc4"], "label": r["label"], "sz_2024": r["n2024"], "nat_2024": nat24,
            "sz_share": round(r["n2024"] / sz_year[2024] * 100, 2),
            "nat_share": round(nat24 / nat_year[2024] * 100, 2) if nat24 else None,
            "lq_2024": r["lq_2024"],
        })

    payload = {
        "metric_id": METRIC,
        "generated_at": "2026-10-22",
        "scope": "深圳",
        "scope_statement": (
            "本件评分全部落在深圳：规模、动能、成熟度三维只用深圳市申请人的 2021—2024 "
            "申请年件数与其专利结构。全国件数只出现在 §2.6 的 LQ 参照列（作 LQ 分母），"
            "不进入总分、不参与阶段阈值，也不与深圳件数同列相加。"
        ),
        "main_db": "gkx @ 183.240.141.251:3318 (gkx_reader_zp, read-only)",
        "sql_count": 0,
        "base_years_used": YEARS,
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": (
            "四项年序列只遍历库内真实存在的 2021—2024（2017—2020 零行）；2025/2026 为采集残年，"
            "不进动能与稳定性分母。缺失年未按 0 摊入，基期只能是 2021。"
        ),
        "input": {
            "sz_patent": "code/_snapshots21/patent_scan_20261021.pkl",
            "nat_patent": "code/_snapshots21/patent_panel_innov_20261021.json",
            "ipc_by_name": "code/_snapshots21/patent_ipc4_by_name_20261021.json",
        },
        "reused_from": "_tech21_domainfeat.py（域特征层，零 SQL）",
        "weights": W,
        "stage_cuts": CUTS,
        "stage_rule": "初级 <40；中级 40—60；高级 >=60（满分 100）",
        "panel": {
            "qualified_domains": meta["qualified"],
            "sz_total_2024": meta["sz_total_2024"],
            "qualified_total_2024": meta["qualified_total_2024"],
            "qualified_coverage": round(meta["qualified_total_2024"] / meta["sz_total_2024"], 4),
            "unqualified_total_2024": meta["sz_total_2024"] - meta["qualified_total_2024"],
            "sz_year_total": meta["sz_year_total"],
            "nat_year_total": {str(k): v for k, v in sorted(nat_year.items())},
            "sz_share_of_national": {str(k): round(meta["sz_year_total"][str(k)] / nat_year[k] * 100, 2)
                                     for k in sorted(nat_year)},
            "sz_domains_all": meta["sz_domains_all"],
        },
        "stage_distribution": stage_block,
        "stage_vs_life_cross": cross_tab,
        "bottleneck_distribution": dict(bottleneck),
        "bottleneck_share": {k: round(v / len(scored) * 100, 2) for k, v in bottleneck.items()},
        "bottleneck_by_stage": bn_by_stage,
        "lq_reference": lq_ref,
        "score_buckets": score_buckets,
        "weight_sensitivity": sens,
        "no_new_code": {
            "domains": len(no_new),
            "dist": {st: sum(1 for r in no_new if r["stage"] == st)
                     for st in ("初级", "中级", "高级")},
        },
        "top20": scored[:20],
        "bottom15": scored[-15:],
        "new_code_watch": new_watch,
        "score_stats": {
            "min": round(min(r["score_total"] for r in scored), 2),
            "max": round(max(r["score_total"] for r in scored), 2),
            "mean": round(statistics.mean(r["score_total"] for r in scored), 2),
            "median": round(statistics.median(r["score_total"] for r in scored), 2),
            "quartiles": [round(x, 2) for x in
                          statistics.quantiles([r["score_total"] for r in scored], n=4)],
        },
        "domains": scored,
        "support_judgment": {
            "data_support_level": "部分支持",
            "structure_support": "部分",
            "data_support": "部分",
            "reason": (
                "「阶段判定」在算法库要求「成熟度指数 + 技术创新度指数 + 专家阈值」，"
                "本库三项都不完整：成熟度只能用五维专利形态替代（无 TRL/被引/标准），"
                "创新度依赖被引（20,515 行、覆盖 0.70%），专家阈值无登记表。"
                "因此本件交付「得分表 + 瓶颈 + 潜力位」，阶段阈值是经验值，不是专家口径。"
            ),
        },
        "headline": {
            "qualified": len(scored),
            "beginner": dist["初级"], "intermediate": dist["中级"], "advanced": dist["高级"],
            "top1": scored[0]["ipc4"], "top1_score": scored[0]["score_total"],
            "top2": scored[1]["ipc4"], "top2_score": scored[1]["score_total"],
            "top3": scored[2]["ipc4"], "top3_score": scored[2]["score_total"],
            "new_code_domains": len(new_watch),
            "bottleneck_top": bottleneck.most_common(1)[0] if bottleneck else None,
        },
    }
    sc.write_out(METRIC, payload)


if __name__ == "__main__":
    main()
