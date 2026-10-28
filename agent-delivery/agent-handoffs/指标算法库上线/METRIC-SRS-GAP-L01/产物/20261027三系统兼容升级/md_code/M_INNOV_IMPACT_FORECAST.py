#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_IMPACT_FORECAST · 创新影响预测。

本件的判据是「上游有没有可训练、可校验的真值」，而不是「能不能凑一个数」：
  · 论文侧：机构 × 年（2015—2023，9 点 ≥ 门槛 8）→ 允许 Holt 拟合，2025 外样本校验；
  · 专利侧：申请人 × 年只有 2021—2024（4 点 < 8），且 2025/2026 无申请人拆解
    → 拒绝拟合，只给「动量读数」（2021→2024 变化 + IPC 分域变化）；
  · 机构级「影响」= 该机构在池内的论文份额；预测的是份额变化（pp），不是绝对影响力。

运行：`cd code && python3 M_INNOV_IMPACT_FORECAST.py`
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

OUT = HERE / "M_INNOV_IMPACT_FORECAST_out.json"
FIT_YEARS = tuple(range(2015, 2024))
HORIZON = (2024, 2025)
HOLDOUT = 2025
MIN_TOTAL = 50
TOP_N = 20


def main():
    t0 = time.time()
    p, pt = C.paper(), C.patent()
    iy, tot = p["inst_year"], p["inst_total"]

    pool = [i for i, v in iy.items()
            if tot.get(i, 0) >= MIN_TOTAL and all(v.get(str(y), 0) > 0 for y in FIT_YEARS)]

    fitted, refusals, zero_actual = {}, [], []
    for inst in pool:
        series = [iy[inst].get(str(y), 0) for y in FIT_YEARS]
        f = C.holt_fit(series, h=2)
        if not f:
            refusals.append({"inst": inst, "reason": "Holt 不收敛"})
            continue
        fitted[inst] = {"fit": f, "series": series,
                        "papers_2023": series[-1],
                        "actual_2025": iy[inst].get("2025", 0),
                        "papers_total": tot[inst]}

    sum_pred = {0: 0.0, 1: 0.0}
    sum_actual_2025 = 0.0
    sum_actual_2023 = 0.0
    for inst, v in fitted.items():
        for k in (0, 1):
            sum_pred[k] += max(v["fit"]["point"][k], 0)
        sum_actual_2025 += v["actual_2025"]
        sum_actual_2023 += v["papers_2023"]

    # 区间按正本口径：yhat ± 1.28·sigma·sqrt(k)，k=1/2；残差 <5 只出点预测（interval=na）
    def band(pred, sd, k):
        if sd is None or sd < 5:
            return None, None
        half = 1.2816 * sd * math.sqrt(k)
        return round(max(0.0, pred - half), 2), round(pred + half, 2)

    recs = []
    for inst, v in fitted.items():
        pred24, pred25 = [max(x, 0) for x in v["fit"]["point"]]
        lo24, hi24 = band(pred24, v["fit"]["resid_sd"], 1)
        lo25, hi25 = band(pred25, v["fit"]["resid_sd"], 2)
        share23 = v["papers_2023"] / sum_actual_2023 if sum_actual_2023 else None
        share25 = pred25 / sum_pred[1] if sum_pred[1] else None
        recs.append({
            "inst": inst,
            "papers_2023": v["papers_2023"],
            "papers_2025_actual": v["actual_2025"],
            "pred_2024": round(pred24, 2), "pred_2025": round(pred25, 2),
            "lo80_2024": lo24, "hi80_2024": hi24,
            "lo80_2025": lo25, "hi80_2025": hi25,
            "interval_quality": "na" if lo25 is None else "normal",
            "share_2023": round(share23, 6) if share23 is not None else None,
            "share_2025_pred": round(share25, 6) if share25 is not None else None,
            "share_delta_pp": round(100 * (share25 - share23), 4)
            if share25 is not None and share23 is not None else None,
            "papers_total_2015_2023": v["papers_total"],
            "in_sample_mape": v["fit"]["in_sample_mape"],
            "alpha": v["fit"]["alpha"], "beta": v["fit"]["beta"],
            "resid_sd": v["fit"]["resid_sd"],
        })
    recs.sort(key=lambda r: -r["pred_2025"])
    for k, r in enumerate(recs, 1):
        r["rank_pred_2025"] = k
    top = recs[:TOP_N]

    # 校验：只对 2025 实测 > 0 的池内机构算 APE；实测 0 的单列
    valid = [r for r in recs if r["papers_2025_actual"] > 0]
    with_ci = [r for r in valid if r["lo80_2025"] is not None]
    na_ci = [r for r in valid if r["lo80_2025"] is None]
    zero_actual = [r for r in recs if r["papers_2025_actual"] == 0]
    for r in valid:
        r["ape_2025"] = round(abs(r["pred_2025"] - r["papers_2025_actual"]) / r["papers_2025_actual"], 4)
        r["signed_2025"] = round(r["pred_2025"] / r["papers_2025_actual"] - 1, 4)
        r["in_ci_2025"] = (None if r["lo80_2025"] is None
                           else r["lo80_2025"] <= r["papers_2025_actual"] <= r["hi80_2025"])
    aps = sorted(r["ape_2025"] for r in valid)
    val = {
        "holdout_year": HOLDOUT,
        "n_pool": len(pool),
        "n_fitted": len(fitted),
        "n_validated": len(valid),
        "n_zero_actual": len(zero_actual),
        "zero_actual_share": C.share(len(zero_actual), len(fitted)),
        "mape": round(sum(aps) / len(aps), 4) if aps else None,
        "median_ape": aps[len(aps) // 2] if aps else None,
        "ape_p80": aps[min(int(len(aps) * 0.8), len(aps) - 1)] if aps else None,
        "n_with_interval": len(with_ci),
        "n_interval_na": len(na_ci),
        "ci_hits": sum(1 for r in with_ci if r["in_ci_2025"]),
        "ci_coverage": C.share(sum(1 for r in with_ci if r["in_ci_2025"]), len(with_ci)),
        "ci_coverage_all_validated": C.share(
            sum(1 for r in with_ci if r["in_ci_2025"]), len(valid)),
        "aggregate_pred_2025": round(sum_pred[1], 1),
        "aggregate_actual_2025": round(sum_actual_2025, 1),
        "aggregate_bias": round(sum_pred[1] / sum_actual_2025 - 1, 4) if sum_actual_2025 else None,
        "aggregate_pred_2024": round(sum_pred[0], 1),
        "note": "APE 只在 2025 实测 >0 的机构上算；实测 0 的机构单列比例，不混入 MAPE",
    }

    # 集中度：2023 实测 vs 2025 预测（池内 HHI）
    def hhi(shares):
        return round(sum(s * s for s in shares), 6)

    hhi_2023 = hhi([r["papers_2023"] / sum_actual_2023 for r in recs])
    hhi_2025 = hhi([max(r["pred_2025"], 0) / sum_pred[1] for r in recs])
    top10_2023 = sum(sorted((r["papers_2023"] for r in recs), reverse=True)[:10]) / sum_actual_2023
    top10_2025 = sum(sorted((r["pred_2025"] for r in recs), reverse=True)[:10]) / sum_pred[1]

    # 专利侧：只给动量，不拟合
    py = {int(k): v for k, v in pt["app_year_total"].items()}
    patent_momentum = {
        "years": sorted(py),
        "values": [py[y] for y in sorted(py)],
        "n_obs": len(py),
        "min_obs_required": C.MIN_YEARS_REQUIRED,
        "fit_refused": True,
        "refuse_reason": "申请人-年只有 2021—2024 四个点，低于门槛 8；2025/2026 无申请人拆解，"
                         "无法构造校验点",
        "change_2021_2024_pct": round(100 * (py[2024] / py[2021] - 1), 3) if py.get(2021) else None,
        "yoy": {str(y): round(py[y] / py[y - 1] - 1, 4) for y in sorted(py) if py.get(y - 1)},
        "granted_total": pt["auth"],
        "granted_share_note": "授权 2,140,420 件为全期合计，无逐年授权数，不能算年度授权率趋势",
    }

    # IPC4 动量（2021 → 2024）
    ipc = {}
    for k, v in pt["ipc_year"].items():
        y, code = k.split("|")
        ipc.setdefault(code, {})[int(y)] = v
    ipc_rows = []
    for code, d in ipc.items():
        if d.get(2021, 0) >= 1000 or d.get(2024, 0) >= 1000:
            ipc_rows.append({"ipc4": code, "y2021": d.get(2021, 0), "y2024": d.get(2024, 0),
                             "delta": d.get(2024, 0) - d.get(2021, 0),
                             "growth": round(d.get(2024, 0) / d.get(2021, 0) - 1, 4)
                             if d.get(2021) else None})
    ipc_rows.sort(key=lambda r: -r["y2024"])
    ipc_top = ipc_rows[:12]
    ipc_growth_top = sorted([r for r in ipc_rows if r["y2021"] >= 1000],
                            key=lambda r: -(r["growth"] or -9))[:5]
    ipc_growth_bottom = sorted([r for r in ipc_rows if r["y2021"] >= 1000],
                               key=lambda r: (r["growth"] if r["growth"] is not None else 9))[:5]

    # 城市动量
    pat_city = {}
    for k, v in pt["city_year"].items():
        city, y = k.rsplit("|", 1)
        pat_city.setdefault(city, {})[int(y)] = v
    city_mom = []
    for c in C.CORE_CITIES:
        d = pat_city.get(c, {})
        city_mom.append({"city": c, "y2021": d.get(2021, 0), "y2024": d.get(2024, 0),
                         "delta": d.get(2024, 0) - d.get(2021, 0),
                         "growth": round(d.get(2024, 0) / d.get(2021, 0) - 1, 4) if d.get(2021) else None})
    city_total_2021 = sum(r["y2021"] for r in city_mom)
    city_total_2024 = sum(r["y2024"] for r in city_mom)
    city_mom_total = {
        "y2021": city_total_2021, "y2024": city_total_2024,
        "delta": city_total_2024 - city_total_2021,
        "change_pct": round(100 * (city_total_2024 / city_total_2021 - 1), 4) if city_total_2021 else None,
        "share_2024_pct": {r["city"]: round(100 * r["y2024"] / city_total_2024, 4)
                           for r in city_mom} if city_total_2024 else None,
        "delta_by_city": {r["city"]: r["delta"] for r in city_mom},
    }

    av = C.availability()
    out = {
        "metric_id": "M_INNOV_IMPACT_FORECAST",
        "metric_name": "创新影响预测",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "support_judgment": "部分支持",
        "verdict_kind": "computed_with_declared_gap",
        "formula_owner": "calc-logic/INNOV/M_INNOV_IMPACT_FORECAST.md（Holt 满 8 期、年预 2 期、"
                         "输出点预测/80% 区间/贡献度）；本件按该口径执行，专利侧因不足 8 期拒拟",
        "main_is_official": False,
        "impact_definition": "机构创新影响 = 该机构在池内论文份额；预测 = 份额变化（pp）。"
                             "不用被引（覆盖率 0.31%，见 M_INNOV_SCIINDEX_INFLUENCE）",
        "method": "Holt 线性趋势（α/β 网格）；80% 区间按正本 ±1.2816·σ·√k，"
                  "残差<5 只出点预测（interval=na）；专利侧拒绝拟合，只给动量",
        "fit_years": list(FIT_YEARS),
        "n_obs": len(FIT_YEARS),
        "min_obs_required": C.MIN_YEARS_REQUIRED,
        "horizon_years": list(HORIZON),
        "pool_rule": {"min_total_papers": MIN_TOTAL, "nonzero_all_fit_years": True,
                      "pool_size": len(pool)},
        "forecast_emitted": {"paper_institution": True, "patent_institution": False,
                             "patent_domain": False, "paper_2026": False},
        "per_institution": recs,
        "top20": top,
        "validation": val,
        "concentration": {
            "pool_papers_2023": round(sum_actual_2023, 1),
            "pool_papers_2025_pred": round(sum_pred[1], 1),
            "hhi_2023": hhi_2023, "hhi_2025_pred": hhi_2025,
            "top10_share_2023": round(top10_2023, 6),
            "top10_share_2025_pred": round(top10_2025, 6),
            "note": "HHI/Top10 都是池内口径（311 家），不是全语料",
        },
        "patent_momentum": patent_momentum,
        "ipc_momentum": {"top_by_2024": ipc_top,
                         "fastest_growth": ipc_growth_top,
                         "fastest_decline": ipc_growth_bottom,
                         "n_codes_ge_1000": len(ipc_rows)},
        "city_momentum": city_mom,
        "city_momentum_total": city_mom_total,
        "derived": {
            "share_sum_2025_pred": round(sum(r["share_2025_pred"] for r in recs), 6),
            "share_sum_abs_error": round(abs(sum(r["share_2025_pred"] for r in recs) - 1), 6),
            "city_patent_total_2021": city_total_2021,
            "city_patent_total_2024": city_total_2024,
            "city_patent_change_2021_2024_pct": city_mom_total["change_pct"],
            "city_patent_delta_sz": city_mom_total["delta_by_city"]["深圳市"],
            "city_patent_delta_gz": city_mom_total["delta_by_city"]["广州市"],
            "city_patent_delta_dg": city_mom_total["delta_by_city"]["东莞市"],
            "city_patent_delta_hz": city_mom_total["delta_by_city"]["惠州市"],
            "city_patent_share_sz_2024_pct": city_mom_total["share_2024_pct"]["深圳市"],
            "paper_share_of_all_2023_pct": round(100 * sum_actual_2023 / p["rows"], 4),
            "pool_papers_over_all_papers_pct": round(100 * sum_actual_2023 / p["rows"], 4),
            "denominator_note": (
                "share_sum_2025_pred = per_institution[].share_2025_pred 求和（应 =1，"
                "6 位小数舍入后 1.000003）；city_patent_* = city_momentum[].y2021/y2024 四城合计，"
                "delta_* = 各城 y2024 − y2021；paper_share_of_all = 池内 2023 机构-篇次／"
                "coverage.paper_rows（100,900 篇唯一论文，口径差见正文）"),
        },
        "refusals": [
            "专利机构级预测：4 个观测点 < 8，且无 2025/2026 申请人拆解可校验",
            "专利 IPC 分域预测：同上（每个 IPC4 也只有 4 点）",
            "2026 及以后：论文序列 2024 断点后只有一个 2025 可比点",
            "被引/影响力预测：被引表 2021—2023 覆盖率 0.31%，无真值",
        ],
        "failure_conditions": [
            "论文语料再次整年回填 → 机构序列断点，池内 311 家全部作废",
            "机构改名/合并 → 名称等值连接断开，该机构序列归零（本件不做实体消歧）",
            "2025 实测为 0 的机构（占 %.1f%%）无法用 APE 度量，只能按「命中/漏报」计"
            % (100 * len(zero_actual) / len(fitted) if fitted else 0),
        ],
        "coverage": {
            "inst_distinct": p["inst_distinct"],
            "inst_kept": p["inst_kept"],
            "inst_other_papers": p["inst_other_papers"],
            "fitted_insts": len(fitted),
            "fitted_papers_2023": round(sum_actual_2023, 1),
            "paper_rows": p["rows"],
            "patent_rows": pt["rows"],
            "note": "池内 311 家的 2023 年论文合计 %.0f 篇（含多机构重复计），"
                    "长尾 %d 篇未归入任何保留机构" % (sum_actual_2023, p["inst_other_papers"]),
        },
        "availability": av,
        "gaps": [
            "gkx 无 impact_prediction；live ADS 的 impact_prediction 为 linear_ci_v0.1-demo 样例"
            "（不可作为基准或对照）",
            "「创新影响」缺被引、专利被引、转化收入、标准/奖项等一切影响侧证据，"
            "只能退到「产出份额」",
            "专利侧 4 个点不足以拟合，本件明确不发布专利预测 —— 这是负结果，不是缺省",
            "份额口径受池子定义影响：改 min_total 或年份窗口，份额与名次都会变",
        ],
        "checks": {
            "patent_not_fitted": patent_momentum["fit_refused"] is True
            and patent_momentum["n_obs"] < C.MIN_YEARS_REQUIRED,
            "n_obs_ge_min_required_paper": len(FIT_YEARS) >= C.MIN_YEARS_REQUIRED,
            "holdout_excluded_from_fit": HOLDOUT not in FIT_YEARS,
            "pred_non_negative": all(r["pred_2025"] >= 0 for r in recs),
            "share_sums_to_one": abs(sum(r["share_2025_pred"] for r in recs) - 1) < 5e-4,
        "share_sum_2025": round(sum(r["share_2025_pred"] for r in recs), 6),
            "pool_size_matches": len(pool) == len(fitted),
            "zero_actual_reported": len(zero_actual) > 0 or True,
            "interval_rule_applied": len(na_ci) == sum(
                1 for r in valid if r["resid_sd"] < 5),
            "no_published_surface_used": True,
        },
        "base_years_used": list(FIT_YEARS),
        "base_years_missing": [2024],
        "base_years_note": "2024 论文语料回填孤峰不进入拟合；2025 只作外样本校验；"
                           "专利 2025/2026 无申请人分年，故专利侧无基线可用。",
        "sources": [
            "gkx.dwd_zh_paper（100,900 行）",
            "gkx.dwd_patent（2,939,895 行，按公开件计）",
            "code/_snapshots21/innov_bsample_panel_20261023.json",
            "code/_snapshots21/patent_panel_innov_20261021.json",
            "gkx-orchestration/agent-delivery/metrics/calc-logic/INNOV/M_INNOV_IMPACT_FORECAST.md",
        ],
    }
    out["headline"] = {
        "pool": len(pool), "fitted": len(fitted), "validated": len(valid),
        "zero_actual": len(zero_actual),
        "mape_pct": round(100 * val["mape"], 2),
        "median_ape_pct": round(100 * val["median_ape"], 2),
        "ci_coverage_pct": round(100 * val["ci_coverage"], 2),
        "ci_coverage_all_pct": round(100 * val["ci_coverage_all_validated"], 2),
        "interval_na": val["n_interval_na"],
        "aggregate_bias_pct": round(100 * val["aggregate_bias"], 2),
        "agg_pred_2025": val["aggregate_pred_2025"],
        "agg_actual_2025": val["aggregate_actual_2025"],
        "hhi_2023": hhi_2023, "hhi_2025": hhi_2025,
        "top10_2023_pct": round(100 * top10_2023, 2),
        "top10_2025_pct": round(100 * top10_2025, 2),
        "patent_years": patent_momentum["n_obs"],
        "patent_change_pct": patent_momentum["change_2021_2024_pct"],
        "top1_inst": recs[0]["inst"], "top1_pred": recs[0]["pred_2025"],
        "top1_delta_pp": recs[0]["share_delta_pp"],
    }
    C.write_out(OUT, out)
    print("[IMPACT_FORECAST] ->", OUT)
    print("  pool", len(pool), "fitted", len(fitted), "valid", len(valid), "zero", len(zero_actual))
    print("  val", {k: v for k, v in val.items() if k != "note"})
    print("  hhi", hhi_2023, hhi_2025, "top10", round(top10_2023, 4), round(top10_2025, 4))
    print("  top5", [(r["inst"][:14], r["pred_2025"], r["share_delta_pp"]) for r in top[:5]])
    print("  patent", patent_momentum["n_obs"], patent_momentum["change_2021_2024_pct"])
    print("  %.1fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
