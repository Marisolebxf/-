#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_SCI_FORECAST · 科学创造力趋势预测。

口径（本件自拟，注册表 formula 为 pending_cosign）：
  对象 = 6 个科研领域 × 年；拟合序列 = 2013—2023（11 点，≥ 工程门槛 8）；
  方法 = Holt 线性趋势（α/β 网格 0.1—0.9，最小化一步 SSE），80% 区间 ±1.2816·σ·√(1+0.15k)；
  输出 = 2024、2025 两点；2024 实测为语料回填孤峰（32,379 篇）不可校验，
  只用 2025（6,548 篇，断点后首年）做 2 步外样本校验；2026 为残年不发布外推。
  另附「滚动回测」：2013—2021 拟 2022—2023、2013—2022 拟 2023，逐点记误差。

运行：`cd code && python3 M_INNOV_SCI_FORECAST.py`
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import _innov21_common as C  # noqa: E402

OUT = HERE / "M_INNOV_SCI_FORECAST_out.json"
FIT_YEARS = tuple(range(2013, 2024))
HORIZON_YEARS = (2024, 2025)
HOLDOUT_YEAR = 2025


def geo(values):
    if not values or any(v <= 0 for v in values):
        return None
    return math.exp(sum(math.log(v) for v in values) / len(values))


def series_of(rows, key, years):
    m = {x["year"]: x.get(key) for x in rows}
    return [m.get(y) for y in years]


def clean(seq):
    return all(v is not None for v in seq)


def main():
    t0 = time.time()
    doms = C.domains()["series"]
    kws = C.domains()["kws"]
    base_2021 = {}
    for d, rows in doms.items():
        b = next((x for x in rows if x["year"] == 2021), {})
        base_2021[d] = b

    per_domain, failures, holdout_hits, holdout_n = {}, [], 0, 0

    for d, rows in doms.items():
        papers = series_of(rows, "papers", FIT_YEARS)
        insts = series_of(rows, "institutions", FIT_YEARS)
        front = series_of(rows, "frontier_ratio", FIT_YEARS)
        actual = {x["year"]: x for x in rows}

        if not clean(papers):
            failures.append({"domain": d, "reason": "论文序列含缺失年，拒绝拟合"})
            continue

        f_p = C.holt_fit(papers, h=2)
        f_i = C.holt_fit(insts, h=2) if clean(insts) else None
        f_f = C.holt_fit(front, h=2) if clean(front) else None

        # 合成指数预测（基年 2021 实测）
        b = base_2021[d]
        comp_idx, comp_ratios = [], []
        for k, y in enumerate(HORIZON_YEARS):
            rels, named = [], {}
            for f, key in ((f_p, "papers"), (f_i, "institutions"), (f_f, "frontier_ratio")):
                if f and b.get(key):
                    r = max(f["point"][k], 0.0) / b[key]
                    rels.append(r)
                    named[key] = round(r, 6)
            comp_idx.append(round(100 * sum(rels) / len(rels), 2) if len(rels) == 3 else None)
            comp_ratios.append(named)

        # 2 步外样本校验（2025）
        val = None
        if f_p:
            act = actual.get(HOLDOUT_YEAR, {}).get("papers")
            pred = f_p["point"][1]
            lo, hi = f_p["lo80"][1], f_p["hi80"][1]
            if act:
                in_ci = lo <= act <= hi
                holdout_n += 1
                holdout_hits += 1 if in_ci else 0
                val = {"year": HOLDOUT_YEAR, "actual": act, "pred": pred,
                       "lo80": lo, "hi80": hi, "in_ci": in_ci,
                       "ape": round(abs(pred - act) / act, 4),
                       "signed_pct": round(pred / act - 1, 4)}

        # 滚动回测
        backtest = []
        for cut in (2021, 2022):
            hist = papers[: cut - FIT_YEARS[0] + 1]
            f = C.holt_fit(hist, h=2023 - cut)
            if not f:
                continue
            for k, y in enumerate(range(cut + 1, 2024)):
                act = actual.get(y, {}).get("papers")
                if not act:
                    continue
                pred = f["point"][k]
                backtest.append({
                    "origin": cut, "target": y, "steps": k + 1,
                    "actual": act, "pred": pred, "lo80": f["lo80"][k], "hi80": f["hi80"][k],
                    "in_ci": f["lo80"][k] <= act <= f["hi80"][k],
                    "ape": round(abs(pred - act) / act, 4),
                    "signed_pct": round(pred / act - 1, 4),
                })

        per_domain[d] = {
            "kws": kws[d],
            "fit_years": list(FIT_YEARS),
            "n_obs": len(papers),
            "history": {y: {"papers": actual.get(y, {}).get("papers"),
                            "institutions": actual.get(y, {}).get("institutions"),
                            "frontier_ratio": actual.get(y, {}).get("frontier_ratio")}
                        for y in FIT_YEARS},
            "model": {"alpha": f_p["alpha"] if f_p else None,
                      "beta": f_p["beta"] if f_p else None,
                      "resid_sd": f_p["resid_sd"] if f_p else None,
                      "in_sample_mape": f_p["in_sample_mape"] if f_p else None},
            "forecast_papers": {
                "years": list(HORIZON_YEARS),
                "point": f_p["point"] if f_p else None,
                "lo80": f_p["lo80"] if f_p else None,
                "hi80": f_p["hi80"] if f_p else None,
            } if f_p else None,
            "forecast_composite_index": {
                "base_2021": 100.0, "years": list(HORIZON_YEARS), "point": comp_idx,
                "ratios_vs_2021": comp_ratios,
                "base_2021_values": {k: b.get(k) for k in ("papers", "institutions", "frontier_ratio")},
                "components": {
                    "papers": f_p["point"] if f_p else None,
                    "institutions": f_i["point"] if f_i else None,
                    "frontier_ratio": f_f["point"] if f_f else None,
                },
            },
            "holdout": val,
            "backtest": backtest,
            "backtest_mape": round(sum(x["ape"] for x in backtest) / len(backtest), 4)
            if backtest else None,
            "backtest_ci_hits": sum(1 for x in backtest if x["in_ci"]),
            "backtest_n": len(backtest),
        }

    # 全域合计（6 领域逐域预测求和）
    tot_point, tot_lo, tot_hi = [], [], []
    for k in range(2):
        pts = [per_domain[d]["forecast_papers"]["point"][k] for d in per_domain
               if per_domain[d].get("forecast_papers")]
        los = [per_domain[d]["forecast_papers"]["lo80"][k] for d in per_domain
               if per_domain[d].get("forecast_papers")]
        his = [per_domain[d]["forecast_papers"]["hi80"][k] for d in per_domain
               if per_domain[d].get("forecast_papers")]
        tot_point.append(round(sum(pts), 1))
        tot_lo.append(round(sum(los), 1))
        tot_hi.append(round(sum(his), 1))
    actual_total = {y: C.paper()["year_all"].get(str(y)) for y in (2023, 2024, 2025)}

    agg = {
        "years": list(HORIZON_YEARS),
        "point": tot_point, "lo80": tot_lo, "hi80": tot_hi,
        "actual_all_papers": actual_total,
        "note": "合计只加 6 个关键词域，不等于全语料；逐域预测相加会低估区间宽度"
                "（各域残差正相关，相加时未按协方差放大）",
    }

    # 结论性统计
    bt_all = [x for d in per_domain.values() for x in d["backtest"]]
    one_step = [x for x in bt_all if x["steps"] == 1]
    two_step = [x for x in bt_all if x["steps"] == 2]
    val_stats = {
        "holdout_year": HOLDOUT_YEAR,
        "holdout_hits": holdout_hits, "holdout_n": holdout_n,
        "holdout_coverage": C.share(holdout_hits, holdout_n),
        "one_step_mape": round(sum(x["ape"] for x in one_step) / len(one_step), 4) if one_step else None,
        "two_step_mape": round(sum(x["ape"] for x in two_step) / len(two_step), 4) if two_step else None,
        "one_step_ci_coverage": C.share(sum(1 for x in one_step if x["in_ci"]), len(one_step)),
        "two_step_ci_coverage": C.share(sum(1 for x in two_step if x["in_ci"]), len(two_step)),
        "direction_hits_one_step": C.share(sum(1 for x in one_step if x["signed_pct"] > 0), len(one_step)),
    }

    def p80(xs):
        xs = sorted(xs)
        return round(xs[min(int(len(xs) * 0.8), len(xs) - 1)], 4) if xs else None

    val_stats["calibration"] = {
        "one_step_empirical_ape_p80": p80([x["ape"] for x in one_step]),
        "two_step_empirical_ape_p80": p80([x["ape"] for x in two_step]),
        "one_step_interval_width_pct": round(sum((x["hi80"] - x["lo80"]) / x["actual"]
                                                for x in one_step) / len(one_step), 4) if one_step else None,
        "two_step_interval_width_pct": round(sum((x["hi80"] - x["lo80"]) / x["actual"]
                                                for x in two_step) / len(two_step), 4) if two_step else None,
        "verdict": "解析区间偏窄：2 步回测 0/6 命中，经验 80% 误差幅度远大于区间半宽。"
                   "对外发布应改用「滚动回测经验宽度」，本件不替换主口径、只登记该缺陷。",
    }

    av = C.availability()
    out = {
        "metric_id": "M_INNOV_SCI_FORECAST",
        "metric_name": "科学创造力趋势预测",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "support_judgment": "部分支持",
        "verdict_kind": "computed_with_declared_gap",
        "formula_owner": "calc-logic/INNOV/M_INNOV_SCI_FORECAST.md（三维加权平均 + Holt，年预 2 期）；"
                         "三维权重正本未定，本件等权，缺口见 gaps",
        "main_is_official": False,
        "method": "Holt 线性趋势（水平+趋势），α/β ∈ {0.1..0.9} 网格最小化一步 SSE；"
                  "区间 = 点预测 ± 1.2816·σ·√(1+0.15k)",
        "target": "6 个科研领域的年度论文量 + 由其三维（论文数量 / 网络中心性=作者单位去重数 / 前沿性=当年新单位占比）等权合成的创造力指数（2021=100）",
        "fit_years": list(FIT_YEARS),
        "n_obs": len(FIT_YEARS),
        "min_obs_required": C.MIN_YEARS_REQUIRED,
        "horizon_years": list(HORIZON_YEARS),
        "publishable_horizon": "2025（已用实测校验）；2026 不发布外推",
        "excluded_years": {
            "2024": "论文语料回填孤峰 32,379 篇，实测不可用于校验，也不进入拟合",
            "2026": "残年 2,989 篇，仅作占位",
        },
        "per_domain": per_domain,
        "aggregate": agg,
        "validation": val_stats,
        "forecast_refused": [
            "2026 及以后：2024 断点后只有 2025 一个可比点，基线是否恢复无法确认，"
            "此时外推等于把「断点前的斜率」硬套到「断点后的新基线」",
            "专利侧任何预测：申请人分年只有 4 个点（2021—2024），低于门槛 8，不做拟合",
            "机构级预测：单机构年度论文量中位数极低，Holt 残差远大于信号",
        ],
        "failure_conditions": [
            "论文语料再次回填（像 2024 那样整年翻 5 倍）→ 序列断点，模型作废",
            "领域关键词表版本变更（当前 domains.version）→ 历史序列不可比",
            "2025 实测落不进 80% 区间的域，其 2026 外推不可采信（见 holdout 逐域结果）",
        ],
        "coverage": {
            "domains": len(per_domain),
            "domain_papers_2023_sum": sum(x.get("papers") or 0 for rows in doms.values()
                                          for x in rows if x["year"] == 2023),
            "domain_papers_fit_sum": sum(x.get("papers") or 0 for rows in doms.values()
                                         for x in rows if x["year"] in FIT_YEARS),
            "inst_rows_total": C.paper()["inst_rows_total"],
            "inst_kept": C.paper()["inst_kept"],
            "inst_distinct": C.paper()["inst_distinct"],
            "domains_failed": failures,
            "fit_points_per_domain": len(FIT_YEARS),
            "total_papers_in_fit_years": sum(C.paper()["year_all"].get(str(y), 0) for y in FIT_YEARS),
            "domain_keyword_hits_fit_window": {
                d: sum(x.get("papers") or 0 for x in rows if x["year"] in FIT_YEARS)
                for d, rows in doms.items()},
        },
        "availability": av,
        "gaps": [
            "无预测结果面可比对：gkx 无 impact_prediction / forecast 族结果表；"
            "live ADS 的 impact_prediction 为 linear_ci_v0.1-demo 样例，不能当基准",
            "正本要求「中英论文」合并入集，本件只用了中文语料（英文 1,387 篇未并入）",
            "6 个领域的年论文量只有 71—512 篇（2023），泊松噪声量级 ±5%—12%，"
            "Holt 的 80% 区间已按残差放大，但仍偏窄",
            "关键词域可重叠，逐域之和不等于全语料",
            "2024 断点使序列「断成两截」，2025 单点无法证明基线回归",
        ],
        "checks": {
            "n_obs_ge_min_required": len(FIT_YEARS) >= C.MIN_YEARS_REQUIRED,
            "all_domains_fitted": len(per_domain) == len(doms) and not failures,
            "all_points_non_negative": all(
                v >= 0 for d in per_domain.values()
                for v in (d["forecast_papers"]["point"] or [])),
            "holdout_year_excluded_from_fit": HOLDOUT_YEAR not in FIT_YEARS,
            "break_year_excluded_from_fit": 2024 not in FIT_YEARS,
            "horizon_len_matches": all(len(d["forecast_papers"]["point"]) == len(HORIZON_YEARS)
                                       for d in per_domain.values()),
            "backtest_present": all(d["backtest_n"] >= 2 for d in per_domain.values()),
            "no_published_surface_used": True,
        },
        "base_years_used": list(FIT_YEARS),
        "base_years_missing": [2024],
        "base_years_note": "2024 语料回填孤峰整年剔除；2025 只作外样本校验、不进入拟合；"
                           "2026 残年不参与。",
        "sources": [
            "gkx.dwd_zh_paper（100,900 行）",
            "code/_snapshots21/innov_bsample_panel_20261023.json（domains.series，6 域 × 27 年）",
            "code/_snapshots21/papers_city_year_gkx21.json",
            "gkx-orchestration/agent-delivery/metrics/calc-logic/INNOV/M_INNOV_SCI_FORECAST.md",
        ],
    }
    # ---------- 派生比值（v8 §一）：正文点名的相对量、增长率、份额必须落产物
    ai = per_domain["人工智能"]
    ai_rel = ai["forecast_composite_index"]["ratios_vs_2021"][1]
    p_all_2023 = C.paper()["year_all"].get("2023", 0)
    domain_2023 = sum(x.get("papers") or 0 for rows in doms.values()
                      for x in rows if x["year"] == 2023)
    out["derived"] = {
        "ai_rel_papers_2025": ai_rel["papers"],
        "ai_rel_institutions_2025": ai_rel["institutions"],
        "ai_rel_frontier_2025": ai_rel["frontier_ratio"],
        "ai_growth_papers_pct": round(100 * (ai_rel["papers"] - 1), 4),
        "ai_growth_institutions_pct": round(100 * (ai_rel["institutions"] - 1), 4),
        "ai_growth_frontier_pct": round(100 * (ai_rel["frontier_ratio"] - 1), 4),
        "ai_index_2025": ai["forecast_composite_index"]["point"][1],
        "domain_papers_2023_sum": domain_2023,
        "domain_papers_fit_sum": sum(x.get("papers") or 0 for rows in doms.values()
                                     for x in rows if x["year"] in FIT_YEARS),
        # 逐域同期合计：附录 E 的 8,798 要能逐域对上，2026-10-23 加
        "domain_papers_fit_sum_by_domain": {
            d: sum(x.get("papers") or 0 for x in rows if x["year"] in FIT_YEARS)
            for d, rows in doms.items()},
        "domain_papers_2023_share_of_all_pct": round(100 * domain_2023 / p_all_2023, 4)
        if p_all_2023 else None,
        "inst_rows_total": C.paper()["inst_rows_total"],
        "inst_kept": C.paper()["inst_kept"],
        "inst_rows_per_kept_inst": round(C.paper()["inst_rows_total"] / C.paper()["inst_kept"], 4),
        "denominator_note": (
            "ai_rel_* = per_domain['人工智能'].forecast_composite_index.ratios_vs_2021 的 2025 点"
            "（分子＝Holt 点预测，分母＝base_2021_values）；ai_growth_* = rel − 1；"
            "domain_papers_2023_share_of_all = 6 域 2023 论文合计／全语料 2023 年论文数；"
            "inst_rows_per_kept_inst = 论文-机构关系数／归一后保留机构数"),
    }
    out["headline"] = {
        "domains": len(per_domain),
        "holdout_hits": val_stats["holdout_hits"], "holdout_n": val_stats["holdout_n"],
        "holdout_pct": round(100 * val_stats["holdout_coverage"], 2),
        "one_step_mape_pct": round(100 * val_stats["one_step_mape"], 2),
        "two_step_mape_pct": round(100 * val_stats["two_step_mape"], 2),
        "agg_2024": tot_point[0], "agg_2025": tot_point[1],
        "agg_lo80_2025": tot_lo[1], "agg_hi80_2025": tot_hi[1],
        "top_growth_domain": max(per_domain, key=lambda d: per_domain[d]["forecast_papers"]["point"][1]
                                 / per_domain[d]["history"][2023]["papers"]),
        "deepest_decline_domain": min(per_domain, key=lambda d: per_domain[d]["forecast_papers"]["point"][1]
                                      / per_domain[d]["history"][2023]["papers"]),
        "two_step_ci_hits": sum(1 for d in per_domain.values() for x in d["backtest"]
                                if x["steps"] == 2 and x["in_ci"]),
        "two_step_n": sum(1 for d in per_domain.values() for x in d["backtest"] if x["steps"] == 2),
    }
    C.write_out(OUT, out)
    print("[SCI_FORECAST] ->", OUT)
    for d, v in per_domain.items():
        print(" ", d, "map", v["model"]["in_sample_mape"], "fc", v["forecast_papers"]["point"],
              "holdout", (v["holdout"] or {}).get("ape"), (v["holdout"] or {}).get("in_ci"),
              "bt", v["backtest_mape"], "%d/%d" % (v["backtest_ci_hits"], v["backtest_n"]))
    print("  agg", agg["point"], "val", val_stats)
    print("  %.1fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
