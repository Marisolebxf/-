#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TECH_DEEP_137_1 技术阶段分析模型 —— 离线复算（零 SQL）。

主路径：IPC4 域 2021—2024 完整年申请量，双信号（总增长 2021→2024、近端增长 2023→2024）三档判别。
对照实验：logistic S 曲线用 2021—2023 拟合、预测 2024，量化四点窗的不可靠程度。
缺口：被引字段无域级缓存（全表 20,515 行 / 2,939,895 = 0.70%），专家阈值无登记表。
"""
from __future__ import annotations

import collections
import math
import statistics

import _tech21_common as C

M = "M_TECH_DEEP_137_1"
WINDOW = C.COMPLETE_YEARS
MIN_N24 = 100

cell, by_year, domains_all = C.load_ipc_year()   # 全国基准（仅用于分母/参照）
sz_cell, sz_year = C.load_sz_ipc_year()         # 深圳主口径


def n(code, year):
    return sz_cell.get((code, year), 0)


rows = []
for d in sorted(domains_all):
    n21, n22, n23, n24 = n(d, 2021), n(d, 2022), n(d, 2023), n(d, 2024)
    if n24 < MIN_N24 or n21 <= 0 or n23 <= 0:
        continue
    g_total = (n24 - n21) / n21
    g_near = (n24 - n23) / n23
    if g_total >= 0.6 and n24 < 3000:
        stage = "初级"
    elif g_total <= -0.15 or g_near <= -0.20:
        stage = "高级"
    else:
        stage = "中级"
    rows.append({"ipc4": d, "label": C.label(d), "n2021": n21, "n2022": n22, "n2023": n23,
                 "n2024": n24, "g_total": g_total, "g_near": g_near, "stage": stage})

dist = collections.Counter(r["stage"] for r in rows)


def out(r):
    return {"ipc4": r["ipc4"], "label": r["label"], "n2021": r["n2021"], "n2024": r["n2024"],
            "growth_21_24_pct": C.pct(r["g_total"]), "growth_23_24_pct": C.pct(r["g_near"]),
            "stage": r["stage"]}


top_growth = [out(r) for r in sorted(rows, key=lambda x: -x["g_total"])[:15]]
top_decline = [out(r) for r in sorted(rows, key=lambda x: x["g_total"])[:15]]

# 规模分层，检查阶段分布是否被小域主导
bands = [(">=5000", 5000, 10**9), ("1000-4999", 1000, 4999), ("500-999", 500, 999), ("100-499", 100, 499)]
band_dist = {}
for name, lo, hi in bands:
    sub = [r for r in rows if lo <= r["n2024"] <= hi]
    band_dist[name] = {"n": len(sub), **dict(collections.Counter(r["stage"] for r in sub))}

# S 曲线对照：3 点拟合 logistic，留出 2024 检验（累计量）
def fit_logistic(cum, grid_l=40, grid_k=40, grid_t=40):
    ymax = max(cum)
    best = None
    for i in range(1, grid_l + 1):
        L = ymax * (1 + 2.0 * i / grid_l)          # 1.0 ~ 3.0 倍峰值
        for j in range(1, grid_k + 1):
            k = 0.05 + 2.95 * j / grid_k            # 0.05 ~ 3.0
            for m in range(grid_t + 1):
                t0 = -3 + 9 * m / grid_t            # -3 ~ 6
                pred = [L / (1 + math.exp(-k * (t - t0))) for t in range(4)]
                sse = sum((a - b) ** 2 for a, b in zip(pred, cum))
                if best is None or sse < best[0]:
                    best = (sse, L, k, t0)
    return best


s_curve = []
param_shift = []
for r in sorted(rows, key=lambda x: -x["n2024"])[:50]:
    y = [r["n2021"], r["n2022"], r["n2023"], r["n2024"]]
    cum = [y[0], y[0] + y[1], y[0] + y[1] + y[2], sum(y)]
    _, L3, k3, t03 = fit_logistic(cum[:3])
    pred24 = L3 / (1 + math.exp(-k3 * (3 - t03)))
    err = abs(pred24 - cum[3]) / cum[3] if cum[3] else None
    _, L4, k4, t04 = fit_logistic(cum)
    param_shift.append({"ipc4": r["ipc4"],
                        "L_shift_pct": C.pct(abs(L4 - L3) / L4) if L4 else None,
                        "k_shift_pct": C.pct(abs(k4 - k3) / k4) if k4 else None,
                        "t0_shift_abs": round(abs(t04 - t03), 3)})
    s_curve.append({"ipc4": r["ipc4"], "n2024": r["n2024"], "cum2024": cum[3],
                    "pred2024": round(pred24, 1), "abs_pct_err": C.pct(err) if err is not None else None})

errs = [x["abs_pct_err"] for x in s_curve if x["abs_pct_err"] is not None]
within20 = sum(1 for e in errs if e <= 20)
med_l = statistics.median(x["L_shift_pct"] for x in param_shift)
med_k = statistics.median(x["k_shift_pct"] for x in param_shift)
med_t = statistics.median(x["t0_shift_abs"] for x in param_shift)

# 被引：只用本地清单算上限覆盖率，不查库
CITED_ROWS = 20515
PATENT_ROWS = 2939895

# 分类学校验：H10x 是 2025.01 新码，2021—2023 的低基数是旧码迁入造成的；
# 这会把一批半导体新码误判为「初级」。剔除新码后单列初级域数量。
new_codes = ["H10B", "H10D", "H10F", "H10H", "H10K", "H10N", "H10P", "H10W"]
new_in_eligible = [r["ipc4"] for r in rows if r["ipc4"] in new_codes]
initial_new = sum(1 for r in rows if r["stage"] == "初级" and r["ipc4"] in new_codes)
semi_all = ["H01L"] + new_codes
semi_series = {str(y): sum(n(c, y) for c in semi_all) for y in (2021, 2022, 2023, 2024)}
semi_growth = (semi_series["2024"] - semi_series["2021"]) / semi_series["2021"]

payload = {
    "metric_id": M,
    "generated_at": "2026-10-22",
    "params": {
        "time_axis": "apdt_year（申请年）",
        "window": WINDOW,
        "thresholds": {"初级": "g_total>=0.60 且 n2024<3000", "高级": "g_total<=-0.15 或 g_near<=-0.20", "中级": "其余"},
        "min_n2024": MIN_N24,
        "threshold_source": "经验阈值（继承 20261020 批），非甲方/专家登记口径",
        "base_years_used": WINDOW,
        "base_years_missing": C.MISSING_BASE_YEARS,
        "excluded_years": [2025, 2026],
    },
    "universe": {"ipc4_total": len(domains_all), "eligible_domains": len(rows),
                 "national_2024_ipc_patents": by_year[2024],
                 "sz_2024_ipc_patents": sz_year[2024]},
    "stage_dist": dict(dist),
    "stage_pct": {k: C.pct(v / len(rows)) for k, v in dist.items()},
    "stage_by_scale": band_dist,
    "top_growth": top_growth,
    "top_decline": top_decline,
    "s_curve_check": {
        "n_domains_tested": len(s_curve),
        "median_abs_pct_err": round(statistics.median(errs), 2) if errs else None,
        "mean_abs_pct_err": round(statistics.mean(errs), 2) if errs else None,
        "within_20pct": within20,
        "within_20pct_share": C.pct(within20 / len(errs)) if errs else None,
        "param_shift_3pt_vs_4pt": {"median_L_shift_pct": med_l, "median_k_shift_pct": med_k,
                                   "median_t0_shift_years": med_t},
        "verdict": (
            f"3 点拟合 3 参数为恰好识别（自由度 0），留出误差小只是插值，不是预测力；"
            f"加入第 4 点后参数中位漂移 L {med_l}%、k {med_k}%、t0 {med_t} 年，"
            "说明四点窗下 S 曲线位置不可作为正式分档依据。"
        ),
        "examples": s_curve[:10],
    },
    "taxonomy_check": {
        "note": "H10x（H10B/D/F/H/K/N/P/W）为 2025.01 新版 IPC 新码，历史低基数来自旧码迁入；这批域被判为「初级」是分类迁移，不是技术早期。",
        "new_codes": new_codes,
        "new_codes_in_eligible": len(new_in_eligible),
        "initial_total": dist.get("初级", 0),
        "initial_new_code_count": initial_new,
        "initial_excl_new_codes": dist.get("初级", 0) - initial_new,
        "merged_family": "H01L+" + "+".join(new_codes),
        "merged_series": semi_series,
        "merged_growth_21_24_pct": C.pct(semi_growth),
    },
    "citation_dim": {
        "available": False,
        "cited_rows": CITED_ROWS,
        "patent_rows": PATENT_ROWS,
        "max_coverage_pct": round(CITED_ROWS / PATENT_ROWS * 100, 2),
        "blocker": "dwd_patent_cited 只有 20,515 行（上限覆盖 0.70%），且无域级缓存；按技术维零 SQL 纪律不查库，创新度指数不可算。",
    },
    "expert_threshold_dim": {
        "available": False,
        "blocker": "库内无专家阈值登记表；当前 0.60/-0.15/-0.20 为经验值，不能冒充专家口径。",
    },
    "base_years_used": WINDOW,
    "base_years_missing": C.MISSING_BASE_YEARS,
}

payload["support_judgment"] = {
    "data_support_level": "部分支持",
    "criteria": {
        "stage_classification": True,
        "eligible_domains": len(rows),
        "stage_dist": dict(dist),
        "s_curve_median_err_pct": payload["s_curve_check"]["median_abs_pct_err"],
        "citation_dim": False,
        "expert_threshold": False,
        "years_available": WINDOW,
    },
    "reason": (
        f"形态三档可交付：{len(rows)} 个域按双信号分为初级 {dist['初级']} / 中级 {dist['中级']} / 高级 {dist['高级']}；"
        f"但需求点名的技术成熟度指数（S 曲线）在四点窗上留出预测中位误差 {payload['s_curve_check']['median_abs_pct_err']}%、"
        "创新度指数受被引 0.70% 上限覆盖钳制、专家阈值无登记表，故判部分支持。"
    ),
}

C.write_out(M, payload)
