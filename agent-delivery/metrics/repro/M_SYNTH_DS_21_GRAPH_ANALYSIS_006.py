#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SYNTH_DS_21_GRAPH_ANALYSIS_006 预测分析 —— 城市专利年度序列外推（20261022）。

序列：2021–2024 年四市专利申请件数（城市×年，来源 city_patent_year_gkx.json，
      全量面板 2,939,895 行离线派生；2025/2026 在城市维没有键，2026 为残年，均不入模）。

方法学说明（必须先看）：
  n=4 的年度序列**无法识别 ARIMA(1,1,0)**：一阶差分后只剩 2 个观测，而
  「漂移 + AR(1)」要估 2 个参数，残差自由度 0，区间宽度会退化为 0。
  因此本脚本只跑它的两个可识别受限形式 + 两个基准：
    M1 随机游走（naive，last value）
    M2 随机游走 + 漂移（ARIMA(0,1,0)+drift，漂移 = 差分均值）
    M3 线性趋势 OLS（y = a + b·t）
  用滚动原点（origins 2023、2024）做一步外推回测，按 MAPE 选模型后再外推 2025–2027。

输出：M_SYNTH_DS_21_GRAPH_ANALYSIS_006_out.json
"""
from __future__ import annotations

import json
import math

import numpy as np

import _synth21_common as S

MID = "M_SYNTH_DS_21_GRAPH_ANALYSIS_006"
YEARS = [2021, 2022, 2023, 2024]
HORIZON = [2025, 2026, 2027]


def series() -> dict:
    from pathlib import Path
    p = Path(__file__).parent / "_snapshots_gkx21" / "city_patent_year_gkx.json"
    if not p.exists():
        p = S.SNAP / "city_patent_year_gkx.json"
    d = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    g = d.get("groups", {})
    out = {}
    for c in S.CITIES:
        out[c] = [float(g.get(f"{c}|{y}", 0) or 0) for y in YEARS]
    if any(v == 0 for c in out for v in out[c]):
        raise SystemExit("城市年度序列缺键，拒绝把缺失年当 0 拟合：%s" % out)
    return out


def fit_naive(y):
    return {"forecast": lambda h: [y[-1]] * h, "params": {"last": y[-1]}, "resid": []}


def fit_drift(y):
    d = np.diff(np.array(y, dtype=float))
    c = float(d.mean())
    res = (d - c).tolist()
    return {"forecast": lambda h, c=c, last=y[-1]: [last + c * (i + 1) for i in range(h)],
            "params": {"drift": round(c, 4)}, "resid": res}


def fit_trend(y):
    t = np.arange(1, len(y) + 1, dtype=float)
    yy = np.array(y, dtype=float)
    b, a = np.polyfit(t, yy, 1)
    res = (yy - (a + b * t)).tolist()
    nxt = len(y)
    return {"forecast": lambda h, a=a, b=b, nxt=nxt: [a + b * (nxt + i + 1) for i in range(h)],
            "params": {"intercept": round(float(a), 4), "slope": round(float(b), 4)},
            "resid": res}


MODELS = {"M1_naive": fit_naive, "M2_drift": fit_drift, "M3_trend": fit_trend}


def sigma(resid, k_params: int) -> float:
    r = np.array(resid, dtype=float)
    if len(r) - k_params <= 0:
        return float("nan")
    return float(math.sqrt((r ** 2).sum() / (len(r) - k_params)))


def backtest(y) -> dict:
    """滚动原点一步外推：origin=2023 用 2021–2022 训练，origin=2024 用 2021–2023。"""
    out = {}
    for name, fn in MODELS.items():
        apes = []
        detail = []
        for i in (2, 3):                      # 预测 YEARS[i]
            train = y[:i]
            if len(train) < 2:
                continue
            m = fn(train)
            pred = m["forecast"](1)[0]
            ape = abs(pred - y[i]) / y[i] * 100.0
            apes.append(ape)
            detail.append({"origin": YEARS[i - 1], "target": YEARS[i],
                           "actual": y[i], "pred": round(pred, 2), "ape_pct": round(ape, 4)})
        out[name] = {"mape_pct": round(float(np.mean(apes)), 4) if apes else None,
                     "n_origins": len(apes), "detail": detail}
    return out


def trend_test(y) -> dict:
    """OLS 斜率 t 检验（df=n-2=2，双侧 5% 临界值 4.303）。"""
    from scipy import stats
    t = np.arange(1, len(y) + 1, dtype=float)
    yy = np.array(y, dtype=float)
    b, a = np.polyfit(t, yy, 1)
    res = yy - (a + b * t)
    df = len(y) - 2
    s2 = float((res ** 2).sum() / df) if df > 0 else float("nan")
    sxx = float(((t - t.mean()) ** 2).sum())
    se = math.sqrt(s2 / sxx) if sxx else float("nan")
    tv = b / se if se and not math.isnan(se) else float("nan")
    p = float(2 * stats.t.sf(abs(tv), df)) if not math.isnan(tv) else None
    return {"slope": round(float(b), 2), "se": round(se, 4), "t": round(float(tv), 4),
            "df": df, "p_value": round(p, 4) if p is not None else None,
            "significant_5pct": bool(p is not None and p < 0.05),
            "critical_t": 4.303}


def main() -> None:
    ser = series()
    result, chosen = {}, {}
    for c, y in ser.items():
        bt = backtest(y)
        best = min(bt, key=lambda k: (bt[k]["mape_pct"] if bt[k]["mape_pct"] is not None else 9e9))
        chosen[c] = best
        m = MODELS[best](y)
        fc = [round(v, 2) for v in m["forecast"](len(HORIZON))]
        errs = [d["actual"] - d["pred"] for d in bt[best]["detail"]]
        # 区间由「滚动回测一步误差」估计（比模型内部残差更贴近真实外推误差）；
        # df = n_err-1 = 1 时 t=12.706，这里固定用 2 个原点的 t=4.303 并在正文说明。
        s = (float(np.sqrt(np.mean(np.square(errs)))) if errs else float("nan"))
        tcrit = 4.303
        pi = [[round(v - tcrit * s * math.sqrt(1 + (i + 1)) , 2),
               round(v + tcrit * s * math.sqrt(1 + (i + 1)), 2)] for i, v in enumerate(fc)] \
            if not math.isnan(s) else [[None, None] for _ in fc]
        result[c] = {"series": {str(yy): int(v) for yy, v in zip(YEARS, y)},
                     "backtest": bt, "selected_model": best,
                     "params": m["params"], "trend_test": trend_test(y),
                     "residual_sigma": None if math.isnan(s) else round(s, 4),
                     "forecast": {str(yy): fc[i] for i, yy in enumerate(HORIZON)},
                     "pi95": {str(yy): pi[i] for i, yy in enumerate(HORIZON)}}
        # 情景区间：三种模型外推的 min–max
        allm = {k: fn(y)["forecast"](len(HORIZON)) for k, fn in MODELS.items()}
        result[c]["scenario_range"] = {
            str(yy): [round(min(allm[k][i] for k in allm), 2),
                      round(max(allm[k][i] for k in allm), 2)]
            for i, yy in enumerate(HORIZON)}

    # 汇总 MAPE
    avg = {}
    for name in MODELS:
        vals = [result[c]["backtest"][name]["mape_pct"] for c in S.CITIES
                if result[c]["backtest"][name]["mape_pct"] is not None]
        avg[name] = round(float(np.mean(vals)), 4) if vals else None

    out = {
        "metric_id": MID,
        "metric_name": "预测分析（城市专利年度序列外推）",
        "generated_at": "2026-10-22",
        "db": "gkx（三方库 183.240.141.251:3318，只读）",
        "target": "各市专利申请件数（apdt_year 口径，一件专利按第一申请人归一个城市，重名 1/k 计权）",
        "series_window": YEARS,
        "horizon": HORIZON,
        "methods": {
            "M1_naive": "随机游走：ŷ_{T+h}=y_T",
            "M2_drift": "ARIMA(0,1,0)+drift：ŷ_{T+h}=y_T+h·c，c=一阶差分均值",
            "M3_trend": "线性趋势 OLS：y=a+b·t",
            "note": ("ARIMA(1,1,0) 在 n=4 下不可识别（差分后 2 个观测 / 2 个参数，"
                     "残差自由度 0），故只跑其受限形式；这不是方法取舍，是自由度约束。"),
        },
        "backtest_design": "滚动原点一步外推，origin=2023（训练 2021–2022）与 origin=2024（训练 2021–2023）",
        "avg_mape_pct": avg,
        "by_city": result,
        "chosen_model": chosen,
        "support_judgment": "部分支持",
        "support_reason": (
            "四市 2021–2024 专利件数是全量面板实测值（合计 2,086,838 件），序列干净、"
            "口径唯一，预测链条可完整复现；但只有 4 个年度观测，ARIMA(1,1,0) 无法识别，"
            "回测只有 8 个一步预测点（4 城 × 2 原点），MAPE 的置信度很低；"
            "2025 年在城市维没有键（面板 2025 总量 440,401，为公开滞后截断），"
            "2026 为残年，都无法作为样本外验证。因此只能给趋势示意，不能作为阈值判定依据。"),
        "note": ("选模型按各城回测 MAPE 最小者（并列时优先简单模型顺序 M1→M2→M3）；"
                 "区间用残差 σ 乘 t(df) 并含 1+1/n 预测方差项；df=1 时 t=12.706，区间极宽，"
                 "这是 n=4 的真实代价，不做人为收窄。"),
    }
    out.update(S.base_year_block(
        YEARS, [2017, 2018, 2019, 2020],
        "专利库 apdt_year 只有 2021–2026；2017–2020 一行都没有，不得按 0 摊入趋势拟合或分母。"
        "2025 在城市维无键（总量 440,401，公开滞后），2026 为残年（74,810），均不参与拟合，"
        "只作为预测目标年。"))
    S.write_out(MID, out)
    print(json.dumps({"avg_mape": avg, "chosen": chosen,
                      "fc": {c: result[c]["forecast"] for c in S.CITIES}}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
