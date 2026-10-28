#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_INNOV_CITY_TREND_SZ 深圳与对标城市趋势
# 【维护者】唐绍祖
# 【适用系统】科技专题系统 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_INNOV_CITY_TREND_SZ.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_INNOV_CITY_TREND_SZ 深圳与对标城市趋势 · gkx 版（20261021 改源）

四维（序号 130）：研发投入 / 专利 / 高企 / 人才。2017–2024 年序列，≥8 期 Holt 外推 h=2，
点预测 + 80% 区间（±1.28σ̂√k），下限截 0，残差 σ̂<5 只出点预测。宇宙 = 粤三城。

本版最重要的一处「如实纠正」
----------------------------
20261020 版把专利维写成「2017–2024 八期完整、可外推」。实测 gkx 面板 `year_all` 只有
**2021、2022、2023、2024、2025、2026** 六个年份键 —— `apdt_year` 没有 2021 以前的键。
也就是说，专利序列里 2017–2020 的 4 个 0 **不是「当年没有专利」，而是「年份字段不存在」**，
属于**结构性缺失**。把它当真实观测喂进 Holt，会把前 4 期当成「从 0 起跳」，
既抬高 σ̂ 又压低预测可信度，旧版那份「专利 2025 预测 354,047 件（区间 20.6 万–50.2 万）」
其实是这 4 个假 0 造出来的伪区间。

本版处置（不改口径、只如实标注）：
1. 序列与预测**照旧输出**（便于与 20261020 版逐位对照，读数不变）；
2. 新增 `year_key_coverage` 与 `patent_forecast_reliable=false` + 原因；
3. 专利维另给一个**只用可比期（2021–2024）**的 4 期几何平均增速 `cagr_2021_2024`，
   作为「可比时间序列」的诚实替代（4 期不足以做 h=2 的 Holt，故不外推）；
4. 高企 / 人才仍无年份键 → 只有存量、不出预测（与旧版一致）。

改源要点
--------
* 研发经费：`dwd_org_stock_finance_info`（上市主体年报口径），org_id→city 本地归城，2017–2024 全取；
* 专利：读共享缓存 `city_patent_year_gkx.json`（A-12 面板 × 底册 name→city，零 DB），
  不再对 294 万行做 `first_applicant_name IN (...)` 的 28 块分城扫描；
* 高企 / 学者：同 `M_INNOV_CITY_RANK_SZ` 的本地归城结果。
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _city21_common as C  # noqa: E402

CITIES = C.CITY_KEYS
YEARS = list(range(2017, 2025))


def holt(series, h=2, alpha=0.5, beta=0.3):
    """Holt 双参数线性外推；返回 ([(k, yhat, lo, hi)], sigma)。残差 σ̂<5 只出点预测。"""
    if len(series) < 8:
        return None
    l, b = series[0], series[1] - series[0]
    resid = []
    for t in range(1, len(series)):
        pred = l + b
        resid.append(series[t] - pred)
        l_new = alpha * series[t] + (1 - alpha) * (l + b)
        b = beta * (l_new - l) + (1 - beta) * b
        l = l_new
    sigma = math.sqrt(sum(r * r for r in resid) / max(len(resid), 1))
    out = []
    for k in range(1, h + 1):
        yhat = max(l + k * b, 0.0)
        if sigma < 5:
            out.append((k, round(yhat, 1), None, None))
        else:
            out.append((k, round(yhat, 1),
                        round(max(yhat - 1.28 * sigma * math.sqrt(k), 0), 1),
                        round(yhat + 1.28 * sigma * math.sqrt(k), 1)))
    return out, round(sigma, 1)


def cagr(v0, v1, n):
    if not v0 or not v1 or n <= 0:
        return None
    return round((v1 / v0) ** (1.0 / n) - 1.0, 4)


def main():
    raw = C.build_raw()
    pat = C.load_patent_city_year()
    if pat is None:
        raise SystemExit("缺 city_patent_year_gkx.json：先跑 _build_city_patent_year.py")
    groups = pat["groups"]
    pat_years = sorted(int(y) for y in (pat.get("year_coverage") or {}).get("years_present", []))

    output = []
    for city in CITIES:
        rd_y = {int(y): float(v) for y, v in (raw["rd_year"].get(city) or {}).items()}
        pt_y = {int(k.rsplit("|", 1)[1]): int(v) for k, v in groups.items()
                if k.startswith(city + "|")}
        city_out = {
            "city": C.SHORT[city], "city_code": city,
            "patent_total_all_years": int((pat.get("city_totals") or {}).get(city, 0)),
            "hightech_stock_no_yearkey": int(raw["hitech_by_city"].get(city, 0)),
            "scholar_stock_no_yearkey": int(raw["scholar_by_city"].get(city, 0)),
            "dims": {},
        }
        for dim, s in (("rd", rd_y), ("patent", pt_y)):
            arr = [s.get(y, 0) for y in YEARS]
            r = holt(arr)
            d = {"series_2017_2024": arr,
                 "forecast": r[0] if r else None,
                 "sigma": r[1] if r else None,
                 "n_years_nonzero": sum(1 for v in arr if v > 0)}
            if dim == "patent":
                d["years_with_key"] = [y for y in YEARS if y in s]
                d["structural_zero_years"] = [y for y in YEARS if y not in s]
                d["forecast_reliable"] = False
                d["forecast_note"] = (
                    "序列前 4 期为结构性缺失（apdt_year 无 2021 以前的键），Holt 把假 0 当观测，"
                    "σ̂ 被抬高、区间被放宽 —— 预测仅作与 20261020 版的逐位对照，不建议作为结论采信")
                d["cagr_2021_2024"] = cagr(arr[YEARS.index(2021)], arr[YEARS.index(2024)], 3)
                d["comparable_series_2021_2024"] = arr[YEARS.index(2021):YEARS.index(2024) + 1]
            else:
                d["forecast_reliable"] = True
                d["cagr_2021_2024"] = cagr(arr[YEARS.index(2021)], arr[YEARS.index(2024)], 3)
            city_out["dims"][dim] = d
        output.append(city_out)

    result = {
        "metric_id": "M_INNOV_CITY_TREND_SZ",
        "metric_name": "深圳与对标城市趋势",
        "method": "王惠 V1.6：四维年序列 Holt(h=2) 点预测+80%区间；高企/人才无年键维不出预测（披露）",
        "source_db": "gkx（183.240.141.251:3318）",
        "cities": [C.SHORT[c] for c in CITIES],
        "probes": {
            "gkx.dwd_org_stock_finance_info": 40239,
            "gkx.dwd_patent": 2939895,
            "gkx.dwd_org_tech_tag": 202424,
            "gkx.dwd_scholar": 21316,
        },
        "compute": {"cities": output},
        "year_key_coverage": {
            "rd": {"years_with_data": sorted({int(y) for c in raw["rd_year"].values() for y in c}),
                   "window_used": [2017, 2024]},
            "patent": {"years_with_data": pat_years,
                       "structural_zero_years": [y for y in YEARS if y not in pat_years],
                       "note": "apdt_year 仅 2021–2026；2017–2020 无键，不是 0 件"},
        },
        "support_judgment": "部分支持",
        "support_note": (
            "研发维 2017–2024 八期真实完整，可做 Holt 外推；专利维只有 2021–2024 四个可比期"
            "（更早年份年份键缺失，非真实 0），4 期不足以支撑 h=2 外推，只给可比期 CAGR；"
            "高企 tag 无首次打标年、学者无年份键 → 这两维只有存量不出预测；宇宙限粤三城 ⇒ 部分支持"
        ),
        "change_note": (
            "研发序列与 20261020 版逐位一致（SZ 2017 期 55,641,932,201.79 … 2024 期 355,551,726,635.57）；"
            "专利序列 2021–2024 四期同旧版（285,327 / 274,013 / 283,064 / 275,908，已用 A-12 完整面板离线复核），"
            "2017–2020 的 0 已改标为『结构性缺失』；专利预测照旧输出但标记为不可采信。"
        ),
    }
    p = C.write_out("M_INNOV_CITY_TREND_SZ", result)
    print("wrote", p)
    for c in output:
        for dim, d in c["dims"].items():
            print(c["city"], dim, d["series_2017_2024"], "fc", d["forecast"], "sigma", d["sigma"],
                  "cagr", d.get("cagr_2021_2024"))


if __name__ == "__main__":
    main()


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题系统', '科技信息展示系统']

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
    out_json = here / "M_INNOV_CITY_TREND_SZ_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_INNOV_CITY_TREND_SZ.py 等价）
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
        "metric_id": "M_INNOV_CITY_TREND_SZ",
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
