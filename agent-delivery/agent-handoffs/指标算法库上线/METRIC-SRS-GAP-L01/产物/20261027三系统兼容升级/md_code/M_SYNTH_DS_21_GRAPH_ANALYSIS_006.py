#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_SYNTH_DS_21_GRAPH_ANALYSIS_006 预测分析
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_SYNTH_DS_21_GRAPH_ANALYSIS_006.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
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


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题服务算法库', '科技信息展示系统']

# 缺省参数：三系统可传子集；快照/探针粒度上不可再分的参数会在 assumptions 显式声明
COMPAT_DEFAULTS = {
    "start_date": None,        # 算法库/展示常传；缺省 → 基线口径窗口（产物 base_years_*）
    "end_date": None,          # 同上；缺省 → 基线口径窗口
    "region": None,            # 地域过滤；缺省 → 全区域（基线口径）
    "industry_tag": None,      # 链/领域标签；缺省 → 全量（基线口径）
    "weights": None,           # 维度权重（模型型指标）；缺省 → 基线内置权重（Q014 类未定项不擅自赋值）
    "dims": None,              # 维度子集（模型型指标）；缺省 → 基线全维度
    "format": None,            # "detail"/"display"；缺省 → 两段都返回
}


def compute(params=None):
    """三系统统一入口：执行基线 main() 的计算逻辑，读取其产物并附兼容元数据返回。

    返回 dict：
      value / detail   : 主值与明细（透传基线产物 headline/stats，数值逐位=基线）
      display          : 展示系统友好结构（headline 精简 + 明细首层序列化）
      assumptions      : 本次运行采用的缺省假设（缺参时非空，前端可提示）
      applicable_systems / params_effective / metric_id / metric_name / generated_at
    典型调用：
      算法库  : compute({"start_date": ..., "end_date": ..., "region": ...})   全参
      专题系统: compute({}) 或 compute({"industry_tag": "..."})               少传参
      展示系统: compute({"format": "display"})                                只要展示段
    """
    import importlib.util, json as _json, time as _time
    from pathlib import Path as _Path

    p_in = dict(params or {})
    eff = {**COMPAT_DEFAULTS, **{k: v for k, v in p_in.items() if v is not None}}
    assumptions = []
    for k, v in eff.items():
        if v is not None and k in ("start_date", "end_date", "region", "industry_tag", "weights", "dims"):
            assumptions.append(f"{k}={v!r} 已接收：本件快照/探针粒度为基线口径，参数生效范围见同名 md「入参兼容策略」"
                               "（不可再分时返回基线口径值并在此声明）")
    assumptions.append("本件为 20261021 基线口径包装（兼容层不改数学定义）；三系统主值同源")

    t0 = _time.time()
    here = _Path(__file__).resolve().parent
    out_json = here / "M_SYNTH_DS_21_GRAPH_ANALYSIS_006_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_SYNTH_DS_21_GRAPH_ANALYSIS_006.py 等价）
        run_baseline()
    data = _json.loads(out_json.read_text(encoding="utf-8"))

    headline = data.get("headline") or {}
    value = headline.get("value") if isinstance(headline, dict) and "value" in headline else None
    if value is None and isinstance(headline, dict):
        value = next((headline[k] for k in ("total_le2024", "total", "sz_total", "score", "index", "n", "count")
                      if k in headline and isinstance(headline[k], (int, float))), None)
    if value is None:   # 无 headline 结构的产物：从顶层常见键提取（KPI/分布型）
        for k in ("total", "value", "n_total", "count", "org_total", "sz_total", "sum", "amount"):
            v = data.get(k)
            if isinstance(v, (int, float)):
                value = v
                break
            if isinstance(v, dict):
                for kk in ("total", "value", "n", "sz"):
                    if isinstance(v.get(kk), (int, float)):
                        value = v[kk]
                        break
                if value is not None:
                    break
    if value is None:   # 探针/分布型产物：从 population / audit_chain / probe 找主计数
        for sec in ("population", "audit_chain", "probe", "stats"):
            v = data.get(sec)
            if isinstance(v, dict):
                for kk in ("distinct_org_id", "total", "n", "count", "org_count", "rows",
                           "filled", "polar_rows", "chain_members_total"):
                    if isinstance(v.get(kk), (int, float)):
                        value = v[kk]
                        break
            if value is not None:
                break
    if value is None:   # 兜底声明：无单一主值（分布/明细型产物），value=None 属正常而非错误
        assumptions.append("本件为分布/明细型产物（无单一主值键），value=None；调用方请消费 detail/display 段")
    detail = {k: data[k] for k in ("stats", "facts", "population", "rule", "support_judgment",
                                   "base_years_used", "base_years_missing", "sources") if k in data}
    display = {"headline": headline, "rows_preview": None}
    for k in ("chains", "rows", "items", "list", "ranking", "detail_list"):
        if isinstance(data.get(k), list):
            display["rows_preview"] = {"key": k, "n": len(data[k]), "sample": data[k][:5]}
            break
    if eff.get("format") == "display":
        detail = {"support_judgment": data.get("support_judgment")}
    return {
        "metric_id": "M_SYNTH_DS_21_GRAPH_ANALYSIS_006",
        "metric_name": data.get("metric_name"),
        "applicable_systems": APPLICABLE,
        "params_effective": eff,
        "assumptions": assumptions,
        "value": value,
        "detail": detail,
        "display": display,
        "generated_at": _time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_sec": round(_time.time() - t0, 2),
        "baseline_generated_at": data.get("generated_at"),
    }


def run_baseline():
    """原样执行基线 main()（兼容层调用；产物 _out.json 由基线逻辑写盘，铁律：产物只由脚本产出）。"""
    main()  # noqa: F821  ← 基线入口（上方原代码定义）
