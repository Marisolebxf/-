#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_FACTOR_FORECAST · 监测趋势预测（INNOV / DS-01-FACTORS）。

口径（王惠 calc-logic，原样沿用）：
  「对会议/项目/专利/期刊逐年件数序列外推。满 8 期默认 Holt 线性趋势（年预 2 期）；
    件数不为负。输出点预测与约 80% 区间。」→ 输出件数点预测 + 区间，不是 0-100 分。

硬约束（DATA_FACTS §3.13）：
  `gkx.dwd_patent.apdt_year` 只有 2021–2026，**2017–2020 零行**。专利序列因此只有 6 期，
  不足 8 期门槛，**不做外推**；任何「前 N 年基线」都不能把 2017–2020 当 0 摊进分母。
  专利全量年序列只读 `patent_panel_innov_20261021.json`，本脚本零专利 SQL。

输出：code/M_INNOV_FACTOR_FORECAST_out.json
"""
from __future__ import annotations

import json
import math
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
FACTS = HERE / "_snapshots21" / "innov21_facts_20261021.json"
OUT = HERE / "M_INNOV_FACTOR_FORECAST_out.json"
METRIC_ID = "M_INNOV_FACTOR_FORECAST"
Z80 = 1.2816


def holt(vals, h=2, alpha=0.5, beta=0.3):
    """Holt 线性趋势；返回点预测、80% 区间、残差标准差、样本内 MAPE。"""
    level, trend = vals[0], vals[1] - vals[0]
    resid = []
    for v in vals[1:]:
        pred = level + trend
        resid.append(v - pred)
        prev_level = level
        level = alpha * v + (1 - alpha) * (level + trend)
        trend = beta * (level - prev_level) + (1 - beta) * trend
    sigma = math.sqrt(sum(r * r for r in resid) / len(resid)) if resid else 0.0
    pts, lo, hi = [], [], []
    for k in range(1, h + 1):
        p = max(level + k * trend, 0.0)
        band = Z80 * sigma * math.sqrt(k)
        pts.append(round(p, 1))
        lo.append(round(max(p - band, 0.0), 1))
        hi.append(round(p + band, 1))
    mape = (sum(abs(r) / v for r, v in zip(resid, vals[1:]) if v) / len(resid)
            if resid else None)
    return {"point": pts, "pi80_low": lo, "pi80_high": hi,
            "sigma": round(sigma, 1),
            "in_sample_mape": round(mape, 4) if mape is not None else None,
            "alpha": alpha, "beta": beta, "n_periods": len(vals)}


def main():
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    py = {int(k): int(v) for k, v in f["paper_year"].items()}
    jy = {int(k): int(v) for k, v in f["project_year"].items()}
    pat = {int(k): int(v) for k, v in f["patent"]["year"].items()}

    pap_vals = [(y, py[y]) for y in range(2008, 2024)]
    prj_vals = [(y, jy[y]) for y in range(2008, 2021)]
    pat_years = sorted(pat)

    pap_f = holt([v for _, v in pap_vals], h=2)
    prj_f = holt([v for _, v in prj_vals], h=2)

    forecasts = {
        "论文": {
            "train": [{"year": y, "value": v} for y, v in pap_vals],
            "forecast": [{"year": 2024 + i, "value": pap_f["point"][i],
                          "pi80": [pap_f["pi80_low"][i], pap_f["pi80_high"][i]]} for i in range(2)],
            "fit": {k: pap_f[k] for k in ("sigma", "in_sample_mape", "alpha", "beta", "n_periods")},
            "excluded": "2024（32,379 篇入库批）与 2025/2026（645 期未满 + 采集未闭环）不入训练集",
            "baseline_years": [2008, 2023],
        },
        "项目": {
            "train": [{"year": y, "value": v} for y, v in prj_vals],
            "forecast": [{"year": 2021 + i, "value": prj_f["point"][i],
                          "pi80": [prj_f["pi80_low"][i], prj_f["pi80_high"][i]]} for i in range(2)],
            "fit": {k: prj_f[k] for k in ("sigma", "in_sample_mape", "alpha", "beta", "n_periods")},
            "excluded": "2021-2023（入库截断，仅 2,339/58/6 条）不入训练集",
            "baseline_years": [2008, 2020],
        },
        "专利": {
            "train": [{"year": y, "value": pat[y]} for y in pat_years],
            "forecast": [],
            "reason": (
                f"apdt_year 仅 {pat_years[0]}-{pat_years[-1]} 共 {len(pat_years)} 期 < 8 期门槛；"
                "2017–2020 在 gkx.dwd_patent 中零行，不能靠「补 0」把序列拉长到 8 期；"
                "2026 采集止于 2026-10（残年），末端截断；6 期样本下 Holt 的 β（趋势）与 σ（残差）均不可靠，"
                "ARIMA(p,d,q) 需 ≥30 期，故不做外推，仅保留历史序列。"
            ),
            "baseline_years": [pat_years[0], pat_years[-1]],
            "missing_years_not_imputed": [2017, 2018, 2019, 2020],
        },
        "期刊": {
            "train": [], "forecast": [],
            "reason": "dwd_zh_journal（2,796 行）是期刊名录，无年度件数时序列；"
                      "publication_type 全为「期刊」，不含会议。",
        },
        "会议": {
            "train": [], "forecast": [],
            "reason": "会议实体 0（zh_paper / en_journal 均无会议类型），无法建序列。",
        },
    }

    backtest = {
        "论文_2024实测": {"actual": py.get(2024), "pred": pap_f["point"][0],
                       "note": "实测 32,379 远超 80% 区间上界，证实 2024 为入库批；外推口径不受其影响"},
        "论文_2025实测": {"actual": py.get(2025), "pred": pap_f["point"][1],
                       "note": "实测 6,548 落在 80% 区间内，但 2025 仍有 645 期未满，仅作披露"},
        "项目_2021实测": {"actual": jy.get(2021), "pred": prj_f["point"][0],
                       "note": "实测 2,339 远低于区间下界，证实 2021 起入库截断"},
        "专利_不外推": {"actual": None, "pred": None,
                     "note": "6 期 < 8 期门槛；2017–2020 零行不得补 0"},
    }

    out = {
        "metric_id": METRIC_ID,
        "metric_name": "监测趋势预测",
        "domain": "INNOV / DS-01-FACTORS",
        "formula_owner": "王惠（calc-logic 口径，本轮沿用并实测）",
        "generated_at": time.strftime("%Y-%m-%d"),
        "source_db": "gkx",
        "source_detail": {
            "论文/项目": "gkx.dwd_zh_paper.cover_year_start / gkx.dwd_zh_project.approval_year",
            "专利": "patent_panel_innov_20261021.json（全量，零专利 SQL）",
        },
        "definition_used": "Holt 线性趋势（满 8 期），年预 2 期，点预测+80% 区间，件数非负",
        "probes": {
            "dwd_patent": sum(pat.values()),
            "dwd_zh_paper": sum(py.values()),
            "dwd_zh_project": sum(jy.values()),
            "conference_entities": 0,
            "patent_year_coverage": [pat_years[0], pat_years[-1]],
            "patent_missing_years": [2017, 2018, 2019, 2020],
        },
        "forecasts": forecasts,
        "backtest": backtest,
        "support_judgment": {
            "data_support_level": "部分支持",
            "criteria": {
                "structure": "论文/项目序列满足 Holt 门槛（16/13 期）；专利仅 6 期且 2017–2020 零行；期刊/会议无序列",
                "volume": "论文 10.09 万篇、项目 5.85 万项、专利 293.99 万件",
                "reproducible": True,
                "all_four_factors": False,
            },
            "note": "seed 要求会议/项目/专利/期刊四类外推，实际仅论文、项目两类可做 Holt；"
                    "专利样本过短（6 期、2017–2020 结构性缺失、2026 残年）不做外推；"
                    "期刊/会议无年度件数承载 -> 部分支持。",
        },
        "elapsed_sec": round(time.time() - t0, 2),
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(json.dumps({"level": out["support_judgment"]["data_support_level"],
                      "paper": forecasts["论文"]["forecast"],
                      "paper_mape": pap_f["in_sample_mape"],
                      "project": forecasts["项目"]["forecast"],
                      "project_mape": prj_f["in_sample_mape"],
                      "backtest": backtest}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
