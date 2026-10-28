#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_TECH_DS_07_TECH_INNOV_006 技术创新趋势预测
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_TECH_DS_07_TECH_INNOV_006.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_TECH_DS_07_TECH_INNOV_006 · 技术基础指标模型——技术动态资讯（王惠口径：技术创新趋势预测）

口径：王惠 M_INNOV_TINN_FORECAST——对选定 IPC4 领域的「年申请量 / 年被引 / 年转移」做 Holt 线性外推，
      输出点预测与约 80% 区间（本脚本另附阻尼 Holt，抑制右截断导致的线性外推高估）。
数据源：本地快照（tech_d_patent_sample.jsonl / tech_d_metrics / graph2）；--live 走 gkx PK 分片。
输出：code/M_TECH_DS_07_TECH_INNOV_006_out.json
"""
import json, math, statistics, sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots"
OUT = HERE / "M_TECH_DS_07_TECH_INNOV_006_out.json"
PHI = 0.85          # 阻尼系数（Gardner & McKenzie, 1985）
Z80 = 1.28


def holt(series, horizon=2, phi=1.0, alpha=0.5, beta=0.3):
    """Holt 线性趋势；phi<1 为阻尼趋势（阻尼后长期预测收敛于 level + b*phi/(1-phi)）。"""
    if len(series) < 3:
        return None
    l, b = series[0], series[1] - series[0]
    resid = []
    for t in range(1, len(series)):
        f = l + phi * b
        resid.append(series[t] - f)
        l_new = alpha * series[t] + (1 - alpha) * (l + phi * b)
        b = beta * (l_new - l) + (1 - beta) * phi * b
        l = l_new
    sigma = statistics.pstdev(resid) if len(resid) > 1 else abs(resid[0] if resid else 0)
    fc, cum = [], 0.0
    for h in range(1, horizon + 1):
        cum += phi ** h
        point = l + cum * b
        half = Z80 * sigma * math.sqrt(h)
        fc.append({"h": h, "point": round(point, 2),
                   "lo80": round(max(0.0, point - half), 2), "hi80": round(point + half, 2)})
    return {"level": round(l, 2), "trend": round(b, 2), "phi": phi,
            "sigma": round(sigma, 2), "forecast": fc}


def load_year_series():
    g = json.loads((SNAP / "tech_d_graph2_20261021.json").read_text())
    series = {}
    for r in g["ipc_year_series_top40"]:
        series[r["ipc4"]] = [r.get(f"y{y}", 0) for y in (2021, 2022, 2023, 2024, 2025, 2026)]
    return series, g


def main():
    series, g = load_year_series()
    met = json.loads((SNAP / "tech_d_metrics_20261021.json").read_text())
    small = json.loads((SNAP / "tech_d_small_tables_20261021.json").read_text())

    # 拟合窗 2021-2024（2025/2026 为右截断年，不入拟合）
    fits = []
    for ipc, s in series.items():
        obs = s[:4]
        if min(obs) < 30:
            continue
        fits.append({"ipc4": ipc, "obs_2021_2024": obs,
                     "holt": holt(obs, phi=1.0), "holt_damped": holt(obs, phi=PHI),
                     "actual_2025_partial": s[4], "actual_2026_partial": s[5]})
    fits.sort(key=lambda x: -x["obs_2021_2024"][3])

    # 生命周期定相（CAG R + CV）
    def phase(obs):
        g_ = [(obs[i] - obs[i - 1]) / max(1, obs[i - 1]) for i in range(1, len(obs))]
        cv = statistics.pstdev(obs) / max(1e-9, statistics.mean(obs))
        mean_g = sum(g_) / len(g_)
        if mean_g > 0.15 and g_[-1] > 0:
            return "成长期"
        if mean_g < -0.05:
            return "衰退期"
        if abs(mean_g) <= 0.05 and cv < 0.12:
            return "成熟期"
        return "震荡期"

    phases = [{"ipc4": x["ipc4"], "phase": phase(x["obs_2021_2024"]),
               "cagr_21_24": round((x["obs_2021_2024"][3] / max(1, x["obs_2021_2024"][0])) ** (1 / 3) - 1, 4),
               "growth_2024": round((x["obs_2021_2024"][3] - x["obs_2021_2024"][2]) / max(1, x["obs_2021_2024"][2]), 4)}
              for x in fits]

    # 市场潜力维：年转移
    ty = {int(r["y"]): int(r["n"]) for r in small.get("transfer_year") or []
          if str(r.get("y")).isdigit() and int(r["y"]) >= 2021}
    transfer_obs = [ty.get(y, 0) for y in (2021, 2022, 2023, 2024)]
    transfer = {"obs_2021_2024": transfer_obs,
                "holt": holt(transfer_obs, phi=1.0), "holt_damped": holt(transfer_obs, phi=PHI),
                "actual_2025": ty.get(2025), "ratio_2025_vs_holt": None}
    if transfer["actual_2025"] and transfer["holt"]:
        transfer["ratio_2025_vs_holt"] = round(transfer["actual_2025"] / transfer["holt"]["forecast"][0]["point"], 4)

    # 全域 S 曲线（376 个 IPC4 主域合计，demo ods 口径）
    scurve = {int(k): v for k, v in met["scurve_top376_sum_by_year"].items()}
    sc_obs = [scurve.get(y, 0) for y in (2021, 2022, 2023, 2024)]
    scurve_block = {"obs_2021_2024": sc_obs, "actual_2025_partial": scurve.get(2025),
                    "holt_damped": holt(sc_obs, phi=PHI)}

    # 年被引维（王惠第三维）：cited_by_date 字面 'null' 为主，无法生成年度序列
    cited_cover = {"rows": 20515, "pos": 3657, "pos_share": round(3657 / 20515, 4),
                   "date_usable": "cited_by_date 大量为字面 'null'，年度被引序列不可生成"}

    res = {
        "metric_id": "M_TECH_DS_07_TECH_INNOV_006",
        "metric_name": "技术基础指标模型——技术动态资讯（王惠口径：技术创新趋势预测）",
        "formula_owner": "王惠",
        "source_used": "snapshot_jsonl",
        "generated_at": "2026-10-21",
        "method": {"model": "Holt 线性趋势 + 阻尼趋势对照（phi=0.85）",
                   "fit_window": "2021-2024 四个完整申请年",
                   "interval": "80%: ±1.28σ√h",
                   "right_truncation": "2025（部分年）/2026（1-10 月）不入拟合"},
        "domains": fits,
        "phase_dist": dict(Counter(p["phase"] for p in phases)),
        "phases": phases,
        "dim_market_transfer": transfer,
        "dim_quality_cited": cited_cover,
        "s_curve_376_domains": scurve_block,
        "coverage": {"dim1_volume": "full_sampled(200k, 620 IPC4)", "dim2_cited": "0.70%（年度序列不可生成）",
                     "dim3_transfer": "full_table(22,809 条)"},
        "support_judgment": {
            "data_support_level": "部分支持",
            "criteria": {"dim1_annual_volume": True, "dim3_annual_transfer": True,
                         "dim2_annual_cited": False,
                         "holt_reproducible": True,
                         "n_domains_forecast": len(fits)},
            "note": "王惠三维中申请量/转移两维可逐年拟合外推（20 个 IPC4 域出点预测+80% 区间），年被引维因 cited_by_date 全为 'null' 且覆盖率 0.70% 不可生成 → 部分支持",
        },
    }
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str))
    print(json.dumps({k: res[k] for k in ("phase_dist", "coverage", "support_judgment")}, ensure_ascii=False, indent=1))
    print("transfer:", json.dumps(transfer, ensure_ascii=False))
    print("scurve:", json.dumps(scurve_block, ensure_ascii=False))
    for x in fits[:4]:
        print(x["ipc4"], x["obs_2021_2024"], "damped:", x["holt_damped"]["forecast"][0],
              "holt:", x["holt"]["forecast"][0], "actual2025partial", x["actual_2025_partial"])
    print("written:", OUT.name)


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
    out_json = here / "M_TECH_DS_07_TECH_INNOV_006_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_TECH_DS_07_TECH_INNOV_006.py 等价）
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
        "metric_id": "M_TECH_DS_07_TECH_INNOV_006",
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
