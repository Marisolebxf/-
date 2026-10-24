#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_SZ_OPPORTUNITY_SCORE 深圳产业机遇评分（W14-C2）。

calc-logic v0.2.0：score = (trend_score + policy_score + market_score) / 3，0—100。
gkx 无 chain_sz_opportunity（trend/policy/market 三列零真源），本件用可核代理重建：

  trend  = 链级新闻关注度年化增速（dwd_industry_chain_news_info，2025 全年 vs 2026 年化）
  policy = 深圳市政策按链命中数（dwd_policy_base × 链树，policy_industry 快照 city_chain_t0）
  market = 深圳挂链次数（credit_code[2:6]='4403'，chain21_layer）

三列各自在 12 链上做 z 标准化 → 50 + 10z（截断 0—100），再等权平均。
某维原始值不可得（如 2025 无新闻基线）→ 该链按剩余维等权重算，并在 dims_used 标注。
这是「相对强弱指数」，不是原模型的机会概率校准值。"""
from __future__ import annotations

import json
import math
import os
import re
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
YEAR_FRACTION_2026 = 296.0 / 365.0  # 2026-10-23 = 第 296 天


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as fh:
        return json.load(fh)


def zscores(vals):
    mean = statistics.fmean(vals)
    sd = statistics.pstdev(vals)
    if sd == 0:
        return [50.0 for _ in vals], mean, sd
    return [max(0.0, min(100.0, 50.0 + 10.0 * (v - mean) / sd)) for v in vals], mean, sd


def entropy_weights(matrix):
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
    m = (n + 1) / 2.0
    num = sum((ra[i] - m) * (rb[i] - m) for i in range(n))
    den = math.sqrt(sum((x - m) ** 2 for x in ra) * sum((x - m) ** 2 for x in rb))
    return round(num / den, 4) if den else None


def main() -> None:
    tree = load("chain_tree_20261021.json")
    stage = load("chain_stage_leaf_20261021.json")
    findex = load("chain_firm_index_20261023.json")
    layer = load("chain21_layer_20261022.json")
    news = load("chain_news_year_20261023.json")
    policy = load("policy_industry_20261023.json")
    probe = load("chain_live_result_probe_20261023.json")

    roots = sorted(n["industry_code"] for n in tree if len(n["industry_code"]) == 7)
    codes = {n["industry_code"] for n in tree}
    has_child = {c[:-2] for c in codes if len(c) > 7 and c[:-2] in codes}
    leaves = sorted(c for c in codes if c not in has_child and c not in roots)
    chain_name = findex["chain_name"]

    # 新闻：一条新闻挂多链，逐链各计一次（§3.55 同规则）。
    # 源列 varchar(255) 会在数组中途截断（实测 47,403/98,103 个单元不以 ']' 结尾），
    # json.loads 失败时退回正则抓已写出的链码；截断之后的链无法恢复，属已知缺口。
    news_cnt = {}
    news_truncated = 0
    news_year_totals = {}
    for arr, year, cnt in news["cells"]:
        news_year_totals[int(year)] = news_year_totals.get(int(year), 0) + int(cnt)
        if isinstance(arr, str):
            try:
                cl = json.loads(arr)
            except json.JSONDecodeError:
                news_truncated += 1
                cl = re.findall(r"IN[AB]\d+", arr)
        else:
            cl = list(arr)
        for c in {x[:7] for x in cl if isinstance(x, str) and x[:7] in roots}:
            news_cnt[(c, int(year))] = news_cnt.get((c, int(year)), 0) + int(cnt)

    sz_policy = policy["city_chain_t0"].get("深圳市", {})
    sz_policy_node = policy["city_chain_node_policy"].get("深圳市", {})

    market_total = sum(v for k, v in layer["chain_city"].items() if k.endswith("|深圳市"))
    bench = 100.0 * market_total / sum(findex["chain_firms"].values())

    raw = []
    for ch in roots:
        ls = [c for c in leaves if c[:7] == ch]
        nat = stage["leaf_firm_counts"].get(ch, {})
        szm = stage["cell_leaf_firm_counts"].get(ch + "|深圳市", {})
        pos = [nat[c] for c in ls if nat.get(c, 0) > 0]
        med = statistics.median(pos)
        key = [c for c in ls if nat.get(c, 0) > 0 and nat[c] >= med]
        opp = sum(1 for c in key if szm.get(c, 0) == 0
                  or 100.0 * szm[c] / nat[c] < bench)
        n25 = news_cnt.get((ch, 2025), 0)
        n26 = news_cnt.get((ch, 2026), 0)
        growth = None
        if n25 >= 50:
            growth = 100.0 * ((n26 / YEAR_FRACTION_2026) / n25 - 1.0)
        raw.append({
            "chain_code": ch,
            "chain_name": chain_name[ch],
            "news_2025": n25,
            "news_2026": n26,
            "news_2026_annualized": round(n26 / YEAR_FRACTION_2026, 1),
            "trend_growth_pct": None if growth is None else round(growth, 2),
            "policy_sz_t0": sz_policy.get(ch, 0),
            "policy_sz_node": sz_policy_node.get(ch, 0),
            "market_sz_memberships": layer["chain_city"].get(ch + "|深圳市", 0),
            "opportunity_nodes": opp,
            "key_leaves": len(key),
        })

    # 趋势维：只有 2025 有 >=50 条新闻的链可算增速；其余标注不可得
    trend_idx = [i for i, r in enumerate(raw) if r["trend_growth_pct"] is not None]
    trend_score, trend_mean, trend_sd = zscores([raw[i]["trend_growth_pct"] for i in trend_idx])
    trend_map = {trend_idx[k]: trend_score[k] for k in range(len(trend_idx))}

    pol_score, pol_mean, pol_sd = zscores([r["policy_sz_t0"] for r in raw])
    mkt_score, mkt_mean, mkt_sd = zscores([r["market_sz_memberships"] for r in raw])

    rows = []
    for i, r in enumerate(raw):
        dims, vals = [], []
        if i in trend_map:
            dims.append("trend")
            vals.append(trend_map[i])
        dims += ["policy", "market"]
        vals += [pol_score[i], mkt_score[i]]
        comp = round(sum(vals) / len(vals), 1)
        rows.append({
            **r,
            "trend_score": None if i not in trend_map else round(trend_map[i], 1),
            "policy_score": round(pol_score[i], 1),
            "market_score": round(mkt_score[i], 1),
            "dims_used": dims,
            "opportunity_score": comp,
            "rank": None,
        })
    for rank, r in enumerate(sorted(rows, key=lambda x: -x["opportunity_score"]), 1):
        r["rank"] = rank

    # ---- 权重审计（v6 §三.59）：熵权参照 + 三维单纯形网格首名稳定性 ----
    full = [r for r in rows if len(r["dims_used"]) == 3]
    mat = [[r["trend_score"], r["policy_score"], r["market_score"]] for r in full]
    ent_w, ent_e = entropy_weights(mat)
    ent_scores = [round(sum(w * v for w, v in zip(ent_w, row)), 1) for row in mat]
    grid = []
    k = 20
    for a in range(k + 1):
        for b in range(k + 1 - a):
            c = k - a - b
            grid.append((a / k, b / k, c / k))
    top1 = {r["chain_name"]: 0 for r in full}
    for w in grid:
        sc = [sum(wi * vi for wi, vi in zip(w, row)) for row in mat]
        top1[full[sc.index(max(sc))]["chain_name"]] += 1
    weights_audit = {
        "main_is_official": False,
        "main_weights": {"trend": 0.3333, "policy": 0.3333, "market": 0.3333},
        "note": "等权来自 calc-logic「默认等权、ΣW=1」，但权重未冻结；主值是本报告自定义口径，不是官方值",
        "entropy_weights": {d: round(w, 4) for d, w in zip(("trend", "policy", "market"), ent_w)},
        "entropy_e": {d: round(e, 4) for d, e in zip(("trend", "policy", "market"), ent_e)},
        "entropy_scores": [{"chain_name": r["chain_name"], "score": s}
                           for r, s in zip(full, ent_scores)],
        "entropy_top": sorted(zip([r["chain_name"] for r in full], ent_scores),
                              key=lambda x: -x[1])[0][0],
        "spearman_equal_vs_entropy": spearman([r["opportunity_score"] for r in full], ent_scores),
        "grid_step": 0.05,
        "grid_combos": len(grid),
        "top1_share_pct": {k2: round(100.0 * v / len(grid), 2) for k2, v in top1.items()},
        "subset": "只含三维齐全的链（n=%d）；缺 trend 的链不参与网格" % len(full),
    }

    out = {
        "metric_id": "M_CHAIN_SZ_OPPORTUNITY_SCORE",
        "metric_name": "深圳产业机遇评分",
        "support_judgment": "部分支持",
        "verdict_kind": "positive_evidence",
        "judgment_reason": (
            "calc-logic 的三维是 trend_score / policy_score / market_score，源表 chain_sz_opportunity "
            "在 gkx 侧零表；live 侧同名表只有 8 行未来产业种子样例（model_version 后缀 -demo），"
            "与 12 链只重名 1 条，不能当结果面。三列本身没有真源，只能各自用可核代理重建："
            "链级新闻关注度增速、深圳市政策按链命中数、深圳挂链次数。三维结构、等权公式、0—100 量纲"
            "都能对上，但每个代理与模型原分数不是同一把尺（新闻条数不是趋势、政策命中不是政策力度、"
            "挂链次数不是市场空间），且 5 条链缺 2025 新闻基线只能两维加权。故判部分支持。"
        ),
        "base_years_used": [2025, 2026],
        "base_years_missing": [],
        "base_years_note": (
            "趋势维只用 2025 全年与 2026 年化（截至 10-23，按 296/365 折算），两年都在 gkx "
            "有数据，故 used=[2025,2026]、missing 为空；2024 及更早新闻为 0 行，不构成可用基期，"
            "未纳入。政策维与市场维是截面，不带年份。"
        ),
        "sources": [
            "code/_snapshots21/chain_news_year_20261023.json",
            "code/_snapshots21/policy_industry_20261023.json",
            "code/_snapshots21/chain21_layer_20261022.json",
            "code/_snapshots21/chain_tree_20261021.json",
            "code/_snapshots21/chain_stage_leaf_20261021.json",
            "code/_snapshots21/chain_firm_index_20261023.json",
            "code/_snapshots21/chain_live_result_probe_20261023.json",
        ],
        "rule": {
            "formula": "opportunity_score = mean(available dims) of 50 + 10z",
            "trend": "100*((news_2026/0.811)/news_2025 - 1)，要求 news_2025 >= 50",
            "policy": "深圳市政策×链 T0 命中数（policy_industry.city_chain_t0['深圳市']）",
            "market": "深圳挂链次数（credit_code[2:6]='4403'），非去重企业数",
            "reweight": "缺 trend 的链按 policy/market 各 1/2 计，dims_used 标注",
            "zscore": "50 + 10*(x-mean)/pstdev，截断 0—100",
        },
        "population": {
            "chain_firms_clean": sum(findex["chain_firms"].values()),
            "sz_memberships_4403": market_total,
            "national_bench_pct": round(bench, 3),
            "chains": len(roots),
            "news_rows": 108052,
            "news_cells": len(news["cells"]),
            "news_truncated_cells": news_truncated,
            "news_year_totals": {str(k): v for k, v in sorted(news_year_totals.items())},
            "news_2025_memberships": sum(v for (c, y), v in news_cnt.items() if y == 2025),
            "news_2026_memberships": sum(v for (c, y), v in news_cnt.items() if y == 2026),
            "news_2026_annualized_memberships": round(
                sum(v for (c, y), v in news_cnt.items() if y == 2026) / YEAR_FRACTION_2026, 1),
            "policy_rows": policy["rows"],
            "sz_policies_total": policy["city_totals"].get("深圳市", 0),
        },
        "params": {
            "trend_mean": round(trend_mean, 3) if trend_idx else None,
            "trend_sd": round(trend_sd, 3) if trend_idx else None,
            "policy_mean": round(pol_mean, 3),
            "policy_sd": round(pol_sd, 3),
            "market_mean": round(mkt_mean, 1),
            "market_sd": round(mkt_sd, 1),
            "year_fraction_2026": round(YEAR_FRACTION_2026, 4),
        },
        "chains": sorted(rows, key=lambda x: x["rank"]),
        "strict_three_dim": [
            {"chain_name": r["chain_name"], "opportunity_score": r["opportunity_score"],
             "rank_in_subset": i}
            for i, r in enumerate(sorted(
                [x for x in rows if len(x["dims_used"]) == 3],
                key=lambda x: -x["opportunity_score"]), 1)
        ],
        "headline": {
            "chains": len(rows),
            "top_chain": sorted(rows, key=lambda x: -x["opportunity_score"])[0]["chain_name"],
            "top_score": sorted(rows, key=lambda x: -x["opportunity_score"])[0]["opportunity_score"],
            "bottom_chain": sorted(rows, key=lambda x: -x["opportunity_score"])[-1]["chain_name"],
            "bottom_score": sorted(rows, key=lambda x: -x["opportunity_score"])[-1]["opportunity_score"],
            "score_mean": round(statistics.fmean(r["opportunity_score"] for r in rows), 1),
            "score_sd": round(statistics.pstdev([r["opportunity_score"] for r in rows]), 1),
            "chains_full_three_dims": len(rows) - (len(rows) - len(trend_idx)),
            "top_reweighted": len(sorted(rows, key=lambda x: -x["opportunity_score"])[0]["dims_used"]) < 3,
        },
        "weights_audit": weights_audit,
        "live_probe": {k: probe[k] for k in (
            "gkx_has_result_face", "gkx_chain_related_tables", "live_table_rows",
            "live_usable", "live_unusable_reason", "verdict")},
        "checks": {
            "sum_sz_policy_t0": sum(r["policy_sz_t0"] for r in rows),
            "sum_market_sz": sum(r["market_sz_memberships"] for r in rows),
            "chains_with_trend": len(trend_idx),
            "chains_reweighted": len(rows) - len(trend_idx),
            "top_chain": sorted(rows, key=lambda x: -x["opportunity_score"])[0]["chain_name"],
            "bottom_chain": sorted(rows, key=lambda x: -x["opportunity_score"])[-1]["chain_name"],
        },
        "gaps": [
            "chain_sz_opportunity / chain_sz_advantage 在 gkx 侧 0 表；live 侧 8 行种子样例不可用（GAP-CHAIN-RESULT-TABLE）",
            "trend/policy/market 三个原始 score 均不可得，本件全部是代理",
            "5 条链（智能网联汽车/软件/智能终端/传感器/集成电路）2025 新闻不足 50 条，趋势维缺失",
            "深圳市政策×链 T0 仅 13 条，8 条链政策维为 0，方差大、解释力弱",
            "市场维用挂链次数而非市场空间金额，规模与机遇不是单调关系",
            "三维权重待甲方确认，本件沿用 calc-logic 等权 1/3",
        ],
    }
    path = os.path.join(HERE, "M_CHAIN_SZ_OPPORTUNITY_SCORE_out.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1, sort_keys=True)
    print("[ok] M_CHAIN_SZ_OPPORTUNITY_SCORE chains=", len(rows),
          "top=", out["checks"]["top_chain"], "bottom=", out["checks"]["bottom_chain"])


if __name__ == "__main__":
    main()
