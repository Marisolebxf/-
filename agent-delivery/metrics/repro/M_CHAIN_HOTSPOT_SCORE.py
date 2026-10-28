#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_HOTSPOT_SCORE 产业链热点综合评分（W14-C2，零 DB）。

calc-logic v0.2.0 的四维是 企业增速 / 投融资热度 / 专利密度 / 资讯热度，
结果表 chain_hotspot 在 gkx 侧 0 张（GKX_INVENTORY 280 表里 hotspot/layout/
milestone/recommend/roadmap 全部 0 命中），live 侧只有 8 行未来产业种子样例。
本件在链级（12 条链）用四维可核代理重建，每维 min-max 归一后等权合成：

  D1 企业增速   = 2021—2025 成立企业数 / 该链有成立年的企业数
  D2 投融资热度 = 2021—2025 链内融资事件数 / 可映射企业名数 × 1000
  D3 专利密度   = 链内申请人专利件数 / 该链企业家数
  D4 资讯热度   = 2025—2026 资讯挂链次数 / 该链企业家数 × 1000

权重是本件自定义（main_is_official=false）：等权为主值，熵权作客观参照，
并在 4 维单纯形网格（步长 0.05，1,771 组）上给出首名稳定性。

纯快照复算，不连库：
  code/_snapshots21/chain_tree_20261021.json
  code/_snapshots21/chain_firm_year_20261023.json
  code/_snapshots21/chain_firm_index_20261023.json
  code/_snapshots21/star_applicant_agg_gkx.json
  code/_snapshots21/chain21_fin_degree_20261022.json
  code/_snapshots21/chain_news_year_20261023.json
  code/_snapshots21/chain_live_result_probe_20261023.json
"""
from __future__ import annotations

import json
import math
import os
import re
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
DIMS = ("growth", "finance", "patent", "news")
GROWTH_YEARS = range(2021, 2026)
FIN_YEARS = range(2021, 2026)
NEWS_YEARS = (2025, 2026)
GRID_STEP = 0.05


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as fh:
        return json.load(fh)


def minmax(vals):
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return [50.0 for _ in vals], lo, hi
    return [100.0 * (v - lo) / (hi - lo) for v in vals], lo, hi


def entropy_weights(matrix):
    """矩阵行=对象、列=维度，值已归一到 0—100（非负）。返回 (w, e)。"""
    n = len(matrix)
    eps = 1e-12
    e = []
    for j in range(len(matrix[0])):
        col = [row[j] + eps for row in matrix]
        s = sum(col)
        p = [c / s for c in col]
        ej = -sum(pi * math.log(pi) for pi in p) / math.log(n)
        e.append(ej)
    d = [1.0 - x for x in e]
    tot = sum(d)
    return [x / tot for x in d], e


def rank_list(values):
    order = sorted(range(len(values)), key=lambda i: -values[i])
    ranks = [0] * len(values)
    for r, i in enumerate(order, 1):
        ranks[i] = r
    return ranks


def spearman(a, b):
    ra, rb = rank_list(a), rank_list(b)
    n = len(a)
    mean_r = (n + 1) / 2.0
    num = sum((ra[i] - mean_r) * (rb[i] - mean_r) for i in range(n))
    den = math.sqrt(sum((x - mean_r) ** 2 for x in ra) * sum((x - mean_r) ** 2 for x in rb))
    return round(num / den, 4) if den else None


def grid_weights(step=GRID_STEP):
    k = int(round(1.0 / step))
    out = []
    for a in range(k + 1):
        for b in range(k + 1 - a):
            for c in range(k + 1 - a - b):
                d = k - a - b - c
                out.append((a / k, b / k, c / k, d / k))
    return out


def main() -> None:
    tree = load("chain_tree_20261021.json")
    fy = load("chain_firm_year_20261023.json")
    idx = load("chain_firm_index_20261023.json")
    pat = load("star_applicant_agg_gkx.json")
    fin = load("chain21_fin_degree_20261022.json")["fin"]
    news = load("chain_news_year_20261023.json")
    probe = load("chain_live_result_probe_20261023.json")

    roots = sorted(n["industry_code"] for n in tree if len(n["industry_code"]) == 7)
    codes = {n["industry_code"] for n in tree}
    has_child = {c[:-2] for c in codes if len(c) > 7 and c[:-2] in codes}
    leaves = sorted(c for c in codes if c not in has_child and c not in roots)
    chain_name = idx["chain_name"]
    name_chain = idx["name_chain"]
    chain_firms = idx["chain_firms"]

    # ---- 维度 1：企业增速（成立年分布，2019/2020 等早年不进分母口径说明见 MD）----
    growth = {}
    with_year = {}
    new_2125 = {}
    for ch in roots:
        years = {}
        for k, v in fy["chain_year"].items():
            code, ys = k.split("|")
            if code == ch:
                years[int(ys)] = v
        with_year[ch] = sum(years.values())
        new_2125[ch] = sum(years.get(y, 0) for y in GROWTH_YEARS)
        growth[ch] = round(100.0 * new_2125[ch] / with_year[ch], 2) if with_year[ch] else None

    # ---- 维度 2：投融资热度（名称可映射的融资事件）----
    mapped_names = {ch: 0 for ch in roots}
    for nm, ch in name_chain.items():
        if ch in mapped_names:
            mapped_names[ch] += 1
    fin_events = {ch: 0 for ch in roots}
    fin_unmapped = 0
    fin_out_window = 0
    for r in fin:
        nm = r[1]
        y = (r[6] or "")[:4]
        ch = name_chain.get(nm)
        if not ch:
            fin_unmapped += 1
            continue
        if not y or int(y) not in FIN_YEARS:
            fin_out_window += 1
            continue
        fin_events[ch] += 1
    fin_rate = {ch: (1000.0 * fin_events[ch] / mapped_names[ch] if mapped_names[ch] else None)
                for ch in roots}

    # ---- 维度 3：专利密度（申请人名 → 链，再除以链企业数）----
    patent_by_chain = {ch: 0 for ch in roots}
    patent_names_mapped = 0
    for nm, (cnt, _inv) in pat["agg"].items():
        ch = name_chain.get(nm)
        if not ch or ch not in patent_by_chain:
            continue
        patent_names_mapped += 1
        patent_by_chain[ch] += cnt
    pat_density = {ch: 1000.0 * patent_by_chain[ch] / chain_firms[ch] for ch in roots}

    # ---- 维度 4：资讯热度（2025—2026 挂链次数）----
    news_cnt = {ch: 0 for ch in roots}
    truncated = 0
    for arr, year, cnt in news["cells"]:
        if int(year) not in NEWS_YEARS:
            continue
        if isinstance(arr, str):
            try:
                codes = json.loads(arr)
            except json.JSONDecodeError:
                truncated += 1
                codes = re.findall(r"IN[AB]\d+", arr)
        else:
            codes = list(arr)
        for ch in {x[:7] for x in codes if isinstance(x, str) and x[:7] in news_cnt}:
            news_cnt[ch] += int(cnt)
    news_rate = {ch: 1000.0 * news_cnt[ch] / chain_firms[ch] for ch in roots}

    raw = {ch: {
        "growth_pct": growth[ch],
        "finance_per_1k_names": round(fin_rate[ch], 3),
        "patent_per_1k_firms": round(pat_density[ch], 1),
        "news_per_1k_firms": round(news_rate[ch], 2),
        "firms_with_year": with_year[ch],
        "new_firms_2021_2025": new_2125[ch],
        "mapped_names": mapped_names[ch],
        "finance_events_2021_2025": fin_events[ch],
        "patent_count": patent_by_chain[ch],
        "chain_firms": chain_firms[ch],
        "news_memberships_2025_2026": news_cnt[ch],
    } for ch in roots}

    # ---- 归一与合成 ----
    cols = {}
    for dim, key in (("growth", "growth_pct"), ("finance", "finance_per_1k_names"),
                     ("patent", "patent_per_1k_firms"), ("news", "news_per_1k_firms")):
        vals = [raw[ch][key] for ch in roots]
        scores, lo, hi = minmax(vals)
        cols[dim] = {"scores": dict(zip(roots, scores)), "min": lo, "max": hi,
                     "mean": round(statistics.fmean(vals), 4),
                     "sd": round(statistics.pstdev(vals), 4)}

    matrix = [[cols[d]["scores"][ch] for d in DIMS] for ch in roots]
    equal_scores = [round(statistics.fmean(row), 2) for row in matrix]
    ent_w, ent_e = entropy_weights(matrix)
    entropy_scores = [round(sum(w * v for w, v in zip(ent_w, row)), 2) for row in matrix]

    growth_heavy = (0.40, 0.20, 0.20, 0.20)
    heavy_scores = [round(sum(w * v for w, v in zip(growth_heavy, row)), 2) for row in matrix]

    # 单纯形网格：首名稳定性
    grid = grid_weights()
    top1 = {ch: 0 for ch in roots}
    for w in grid:
        sc = [sum(wi * vi for wi, vi in zip(w, row)) for row in matrix]
        top1[roots[sc.index(max(sc))]] += 1

    equal_rank = rank_list(equal_scores)
    rows = []
    for i, ch in enumerate(roots):
        rows.append({
            "chain_code": ch,
            "chain_name": chain_name[ch],
            **raw[ch],
            "score_growth": round(cols["growth"]["scores"][ch], 2),
            "score_finance": round(cols["finance"]["scores"][ch], 2),
            "score_patent": round(cols["patent"]["scores"][ch], 2),
            "score_news": round(cols["news"]["scores"][ch], 2),
            "hotspot_score": equal_scores[i],
            "rank": equal_rank[i],
            "entropy_score": entropy_scores[i],
            "entropy_rank": rank_list(entropy_scores)[i],
            "growth_heavy_score": heavy_scores[i],
            "top1_weight_share_pct": round(100.0 * top1[ch] / len(grid), 3),
        })
    rows.sort(key=lambda r: r["rank"])

    z_lo = min(rows, key=lambda r: r["hotspot_score"])
    # 翻转阈值：等权下第一名，需要把其 growth 权重降到多少才会被第二名超过
    first = rows[0]
    second = rows[1]
    def score_with(wg, row_ch):
        i = roots.index(row_ch)
        w = (wg, (1 - wg) / 3, (1 - wg) / 3, (1 - wg) / 3)
        return sum(wi * vi for wi, vi in zip(w, matrix[i]))
    flip = None
    for step in range(41):
        wg = 0.25 + 0.01 * step  # 只往上抬首名权重
        if score_with(wg, first["chain_code"]) <= score_with(wg, second["chain_code"]):
            flip = round(wg, 2)
            break

    out = {
        "metric_id": "M_CHAIN_HOTSPOT_SCORE",
        "metric_name": "产业链热点综合评分",
        "support_judgment": "部分支持",
        "verdict_kind": "positive_evidence",
        "judgment_reason": (
            "calc-logic 的四维结果表 chain_hotspot 在 gkx 侧 0 张（280 表里 hotspot 关键词零命中），"
            "live 侧只有 8 行未来产业种子样例、与 12 链仅 1 条重名，不能当结果面。"
            "企业增速、投融资、专利、资讯四个原始字段都没有真源，只能用可核代理重建："
            "成立年分布、融资事件、申请人专利、资讯挂链次数。四维结构与 min-max 合成方式对得上，"
            "但每个代理与模型原分不是同一把尺（事件数不是热度、专利件数不是密度分、资讯条数不是关注度），"
            "且权重未冻结（本件等权为自定义），故判部分支持。"
        ),
        "main_is_official": False,
        "base_years_used": [2021, 2022, 2023, 2024, 2025, 2026],
        "base_years_missing": [],
        "base_years_note": (
            "增速维用 2021—2025 成立企业数（2026 残年不进增速分母）；资讯维用 2025—2026 两个完整/残年，"
            "2026 按资讯表实际覆盖计、不折算年化。2019 及更早的成立年只进「有成立年企业数」分母，"
            "不单独做基期。库内无更早的资讯年份（2024 及以前 0 行），故 missing 为空而非摊 0。"
        ),
        "sources": [
            "code/_snapshots21/chain_tree_20261021.json",
            "code/_snapshots21/chain_firm_year_20261023.json",
            "code/_snapshots21/chain_firm_index_20261023.json",
            "code/_snapshots21/star_applicant_agg_gkx.json",
            "code/_snapshots21/chain21_fin_degree_20261022.json",
            "code/_snapshots21/chain_news_year_20261023.json",
            "code/_snapshots21/chain_live_result_probe_20261023.json",
        ],
        "rule": {
            "growth": "2021—2025 成立企业数 ÷ 该链有成立年的企业数 ×100",
            "finance": "2021—2025 链内融资事件数 ÷ 名称可映射企业数 ×1000",
            "patent": "链内申请人专利件数 ÷ 该链企业家数 ×1000",
            "news": "2025—2026 资讯挂链次数 ÷ 该链企业家数 ×1000",
            "normalize": "每维 min-max 到 0—100；极差为 0 时该维全部记 50",
            "compose": "hotspot_score = 0.25×(四维得分之和)，权重本件自定义、非官方",
            "stability": "熵权与 4 维单纯形网格（步长 0.05，1,771 组）首名占比",
        },
        "weights": {
            "main": {"growth": 0.25, "finance": 0.25, "patent": 0.25, "news": 0.25},
            "entropy": {d: round(w, 4) for d, w in zip(DIMS, ent_w)},
            "entropy_e": {d: round(e, 4) for d, e in zip(DIMS, ent_e)},
            "growth_heavy": {"growth": 0.40, "finance": 0.20, "patent": 0.20, "news": 0.20},
            "flip_note": "把首名链的 growth 权重从 0.25 往上抬到 flip_growth_weight 时首名易主；null 表示 0.65 内不翻转",
            "flip_growth_weight": flip,
            "spearman_equal_vs_entropy": spearman(equal_scores, entropy_scores),
            "spearman_equal_vs_growth_heavy": spearman(equal_scores, heavy_scores),
        },
        "params": {
            "grid_step": GRID_STEP,
            "grid_combos": len(grid),
            "growth_years": list(GROWTH_YEARS),
            "finance_years": list(FIN_YEARS),
            "news_years": list(NEWS_YEARS),
            "dim_ranges": {d: {"min": cols[d]["min"], "max": cols[d]["max"],
                               "mean": cols[d]["mean"], "sd": cols[d]["sd"]} for d in DIMS},
        },
        "population": {
            "chains": len(roots),
            "chain_firms_clean": sum(chain_firms.values()),
            "leaf_total": len(leaves),
            "mapped_names_total": sum(mapped_names.values()),
            "patent_names_mapped": patent_names_mapped,
            "patent_names_total": idx["stats"].get("patent_names_total"),
            "fin_rows": len(fin),
            "fin_unmapped_names": fin_unmapped,
            "fin_out_of_window": fin_out_window,
            "news_rows": news["rows"],
            "news_cells": len(news["cells"]),
            "news_truncated_cells": truncated,
        },
        "headline": {
            "chains": len(rows),
            "top_chain": rows[0]["chain_name"],
            "top_score": rows[0]["hotspot_score"],
            "second_chain": rows[1]["chain_name"],
            "second_score": rows[1]["hotspot_score"],
            "bottom_chain": z_lo["chain_name"],
            "bottom_score": z_lo["hotspot_score"],
            "score_mean": round(statistics.fmean(equal_scores), 2),
            "score_sd": round(statistics.pstdev(equal_scores), 2),
            "top1_equal_share_pct": rows[0]["top1_weight_share_pct"],
            "entropy_top_chain": chain_name[roots[entropy_scores.index(max(entropy_scores))]],
            "entropy_top_score": max(entropy_scores),
        },
        "chains": rows,
        "live_probe": {k: probe[k] for k in (
            "gkx_has_result_face", "gkx_chain_related_tables", "live_table_rows",
            "live_usable", "live_unusable_reason", "verdict")},
        "negative_probe": {
            "gkx_tables_total": 280,
            "pattern_hits": {"hotspot": 0, "layout": 0, "milestone": 0, "recommend": 0,
                             "roadmap": 0, "problem": 0, "opportunity": 0, "score": 0},
            "only_chain_tables": ["dwd_industry_chain_info", "dwd_industry_chain_news_info"],
            "news_columns": ["pk_id", "industry_code", "industry_name", "title", "publish_date", "source"],
            "note": "资讯表无 event_type / hot / views 列，资讯热度只能用条数代理；无热点结果表可直读",
        },
        "gaps": [
            "chain_hotspot 结果面两库均无（gkx 0 表；live 8 行种子样例，GAP-CHAIN-RESULT-TABLE）",
            "四维原始分（enterprise_growth_score / investment_score / 专利密度分 / news_freq_score）无真源",
            "节点级（954 叶）热点不可算：资讯只到链级、专利只能按申请人名归链",
            "权重未冻结（等权为本报告自定义，main_is_official=false）",
            "资讯表 47,403/98,103 个 industry_code 单元被 varchar(255) 截断，截断后的链无法恢复",
            "链树 level 列全为 0、node_company_count 全为 0，无法做层级加权（见 M_ENT_KEY_NODE_COUNT 披露）",
        ],
        "checks": {
            "sum_chain_firms": sum(chain_firms.values()),
            "sum_patent_counts": sum(patent_by_chain.values()),
            "sum_news_memberships": sum(news_cnt.values()),
            "sum_fin_events": sum(fin_events.values()),
            "fin_events_plus_unmapped_plus_out": sum(fin_events.values()) + fin_unmapped + fin_out_window,
            "fin_rows": len(fin),
            "top1_shares_sum_pct": round(sum(r["top1_weight_share_pct"] for r in rows), 3),
        },
    }
    path = os.path.join(HERE, "M_CHAIN_HOTSPOT_SCORE_out.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1, sort_keys=True)
    print(f"[ok] M_CHAIN_HOTSPOT_SCORE top={rows[0]['chain_name']} "
          f"{rows[0]['hotspot_score']} bottom={z_lo['chain_name']} {z_lo['hotspot_score']}")


if __name__ == "__main__":
    main()
