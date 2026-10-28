#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""监测异常点识别（M_INNOV_FACTOR_ANOMALY）——A-16 批正式实现。

口径（metrics/calc-logic/INNOV/M_INNOV_FACTOR_ANOMALY.md）：
  用专利 apdt_year、论文 cover_year_start、机构/学者存量按年聚合，拼成长度 ≥8 的监测时序；
  异常点：|x − median| / MAD > 3.5；
  突变点：邻期绝对变化量 > 序列 MAD × 3。
  只输出命中行。

**实测发现（本文件存在的第二个理由）**：口径原式把「全序列中枢」当基准，在**单调增长的
年序列**上会系统性失效——中文论文序列 46 期里 19 期被判异常（中位数落在 1990 年代水平，
2014 年之后每一期都「高于中枢」）。因此本脚本同时产出三套口径：

  levels   口径原式：基准=全序列 median，尺度=MAD            （保留，用于证明其退化）
  yoy      同比：对 Δ% 序列做同样的 MAD 检测                  （识别增速异常）
  rolling  稳健改良：基准=前 5 期滚动 median，尺度=残差 MAD    （推荐，输出最终命中表）

三套口径都要在文档里报数，禁止只报对自己有利的那套。

三条铁律落实：
  1. 专利年度件数**只读面板缓存** `_snapshots21/patent_panel_innov_20261021.json`
     （2,939,895 行全量），不对 `gkx.dwd_patent` 发任何 SQL；
  2. 其余序列只扫 ≤106 万行的小表（论文 10 万、学者-论文关系 106 万、底册 18.9 万），
     单条查询均带 `SET SESSION max_execution_time`，跑一条落盘一条；
  3. 全流程不出现任何演示库 schema 名（本批铁律）。

产物：
  code/_snapshots21/a16_raw_series.json       （五条原始序列，--refresh 重拉）
  code/_snapshots21/a16_anomaly_series.json   （检测结果，供 019 镜像复用）
  code/M_INNOV_FACTOR_ANOMALY_out.json
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import _gkxdb
from _innov_gkx21_common import load_cache, save_cache, write_out

METRIC = "M_INNOV_FACTOR_ANOMALY"
PANEL = HERE / "_snapshots21" / "patent_panel_innov_20261021.json"
RAW_CACHE = "a16_raw_series.json"
SERIES_CACHE = "a16_anomaly_series.json"

THRESH_ANOM = 3.5      # 口径：|x-median|/MAD > 3.5
MUT_MULT = 3.0         # 口径：邻期 |Δ| > MAD × 3
MIN_LEN = 8            # 口径：时序长度 ≥8
ROLL_WIN = 5           # 滚动中枢窗口（改良式，5 期≈一个五年计划跨度）


# ------------------------------------------------------------------ 取数
def q(sql):
    cur = _gkxdb.gkx()
    try:
        cur.execute("SET SESSION max_execution_time=120000")
        cur.execute(sql)
        return cur.fetchall()
    finally:
        cur.close()


def _series_from_pairs(rows, y_lo=None, y_hi=None):
    out = {}
    for y, n in rows:
        if y is None:
            continue
        try:
            yi = int(float(y))
        except (TypeError, ValueError):
            continue
        if y_lo is not None and yi < y_lo:
            continue
        if y_hi is not None and yi > y_hi:
            continue
        if yi <= 0:
            continue
        out[yi] = out.get(yi, 0) + int(n)
    return dict(sorted(out.items()))


def _pull_series():
    series = {}

    # S1 专利年度件数 —— 只读面板（零 DB）
    panel = json.loads(PANEL.read_text(encoding="utf-8"))
    pat = {int(y): int(v if not isinstance(v, dict) else v.get("total", 0))
           for y, v in panel["year_all"].items()}
    pat = dict(sorted(pat.items()))
    series["patent_year"] = {
        "label": "专利年度申请件数",
        "unit": "件",
        "source": "专利面板 patent_panel_innov_20261021.json（全量 2,939,895 行，零 DB）",
        "years": list(pat.keys()),
        "values": list(pat.values()),
        "note": "gkx.dwd_patent 的 apdt_year 只覆盖 2021—2026，2026 为残年；长度 6 < 8。",
    }

    # S2 中文论文年度篇数
    rows = q("SELECT cover_year_start y, COUNT(*) n FROM gkx.dwd_zh_paper "
             "GROUP BY cover_year_start")
    s = _series_from_pairs(rows, 1980, 2025)
    series["zh_paper_year"] = {
        "label": "中文论文年度篇数",
        "unit": "篇",
        "source": "gkx.dwd_zh_paper（100,900 行）",
        "years": list(s.keys()),
        "values": list(s.values()),
        "note": "2026 为残年已截去；2024 年 32,379 篇为邻年 5 倍，属入库口径突变。",
    }

    # S3 学者-论文关系年度条数
    rows = q("SELECT `year` y, COUNT(*) n FROM gkx.dwd_scholar_paper_relation "
             "WHERE `year` BETWEEN 1988 AND 2025 GROUP BY `year`")
    s = _series_from_pairs(rows, 1988, 2025)
    series["scholar_rel_year"] = {
        "label": "学者-论文关系年度条数",
        "unit": "条",
        "source": "gkx.dwd_scholar_paper_relation（1,065,385 行，WHERE year 1988—2025）",
        "years": list(s.keys()),
        "values": list(s.values()),
        "note": "原表 year 存在 0 与 1970 两档脏值（4,601 + 4,690 行），已按口径截断排除。",
    }

    # S4 机构新设年度家数（底册 incorporation_year）
    rows = q("SELECT incorporation_year y, COUNT(*) n FROM gkx.dwd_org_base_info "
             "WHERE incorporation_year BETWEEN 1980 AND 2025 GROUP BY incorporation_year")
    s = _series_from_pairs(rows, 1980, 2025)
    series["org_reg_year"] = {
        "label": "机构新设年度家数",
        "unit": "家",
        "source": "gkx.dwd_org_base_info.incorporation_year（189,116 行，354 行年份为空）",
        "years": list(s.keys()),
        "values": list(s.values()),
        "note": "底册 99.82% 为深圳都市圈机构，本序列不是全国新设序列。",
    }

    # S5 项目立项年度（补充序列，定义未列，用于对照）
    rows = q("SELECT LEFT(approval_year,4) y, COUNT(*) n FROM gkx.dwd_zh_project "
             "GROUP BY y")
    s = _series_from_pairs(rows, 1986, 2023)
    series["project_year"] = {
        "label": "项目立项年度项数（补充序列）",
        "unit": "项",
        "source": "gkx.dwd_zh_project（58,453 行，全部 NSFC）",
        "years": list(s.keys()),
        "values": list(s.values()),
        "note": "定义未列此序列，仅作对照；2021—2023 为入库截断（4,719→2,339→58→6）。",
        "supplementary": True,
    }
    return series


def build_series(refresh=False):
    """默认读缓存（同一脚本产出，可复现）；--refresh 重新拉库。"""
    if not refresh:
        cached = load_cache(RAW_CACHE)
        if cached:
            return cached["series"]
    series = _pull_series()
    save_cache(RAW_CACHE, {"built_at": "2026-10-22",
                           "note": "由 M_INNOV_FACTOR_ANOMALY.py --refresh 重新生成",
                           "series": series})
    return series


# ------------------------------------------------------------------ 检测
def _mad(xs):
    med = statistics.median(xs)
    dev = [abs(x - med) for x in xs]
    return med, statistics.median(dev)


def _scale(vals, med):
    mad = statistics.median([abs(v - med) for v in vals])
    if mad == 0:
        return sum(abs(v - med) for v in vals) / len(vals), "mean_abs_dev（MAD=0 兜底）"
    return mad, "MAD"


def detect(series, mode="levels", thresh=THRESH_ANOM, mut_mult=MUT_MULT):
    """mode: levels（口径原式）/ yoy（同比变化率）/ rolling（滚动中枢残差）。"""
    years = [int(y) for y in series["years"]]
    vals = [float(v) for v in series["values"]]
    n = len(vals)
    rec = {
        "key": series.get("key"),
        "label": series["label"],
        "unit": series["unit"],
        "source": series["source"],
        "note": series.get("note", ""),
        "mode": mode,
        "n": n,
        "eligible": n >= MIN_LEN,
    }
    if n == 0:
        rec["reason"] = "序列为空"
        return rec
    if n < MIN_LEN:
        rec["reason"] = f"序列长度 {n} < {MIN_LEN}，按口径不进入异常检测"
        rec["years"] = years
        rec["values"] = vals
        return rec

    if mode == "levels":
        base_years, base = list(years), list(vals)
        med = statistics.median(base)
        scale, kind = _scale(base, med)
        resid = [v - med for v in base]
        center_desc = "全序列 median"
        grid = years
    elif mode == "rolling":
        # 前 ROLL_WIN 期作基线，之后逐期与「前 5 期滚动 median」比
        win = ROLL_WIN
        grid, resid = [], []
        for i in range(win, n):
            base = vals[i - win:i]
            bmed = statistics.median(base)
            sd = statistics.median([abs(x - bmed) for x in base])
            if sd == 0:
                sd = max(1.0, bmed * 0.05)
            grid.append(years[i])
            resid.append((vals[i] - bmed) / sd)
        # 标准化后的残差本身就是「MAD 倍数」，再做一次跨期条件化：
        # 以残差序列自身的中枢为参照，保证仍然满足口径「相对序列中枢」的形态。
        med = statistics.median(resid)
        scale, kind = _scale(resid, med)
        base_years, base = grid, resid
        center_desc = f"前 {win} 期滚动 median，残差再按全序列残差中枢标准化"
    elif mode == "yoy":
        grid, rates = [], []
        for i in range(1, n):
            if vals[i - 1] == 0:
                continue
            grid.append(years[i])
            rates.append((vals[i] - vals[i - 1]) / vals[i - 1])
        base_years, base = grid, rates
        med = statistics.median(rates)
        scale, kind = _scale(rates, med)
        resid = [r - med for r in rates]
        center_desc = "同比变化率 median"
    elif mode == "yoy_floor":
        # 交付口径：同比变化率 + 物质性门槛。
        #   低基数期（本文取「上年 < 序列峰值 1%」）不判，避免 16→37 家这类基数效应；
        #   其余沿用口径原式的 median + MAD 判据（阈值 3.5）。
        floor = 0.01 * max(vals)
        grid, rates = [], []
        for i in range(1, n):
            if vals[i - 1] <= 0 or max(vals[i], vals[i - 1]) < floor:
                continue
            grid.append(years[i])
            rates.append((vals[i] - vals[i - 1]) / vals[i - 1])
        if len(rates) < MIN_LEN - 1:
            rec["reason"] = f"物质性门槛过滤后仅剩 {len(rates)} 期，不足以检测"
            rec["materiality"] = {"level_floor": round(floor, 2)}
            return rec
        base_years, base = grid, rates
        med = statistics.median(rates)
        scale, kind = _scale(rates, med)
        center_desc = f"同比变化率 median（低基数期 < 峰值 1% = {floor:.0f} 已剔除）"
    else:
        raise ValueError(mode)

    anomalies = []
    joined = []
    for yr, r in zip(base_years, base):
        score = abs(r - med) / scale if scale > 0 else 0.0
        joined.append((yr, r, score))
        if score > thresh:
            anomalies.append({
                "year": int(yr),
                "value": round(float(r), 4) if mode != "levels" else round(float(r), 2),
                "score": round(score, 3),
                "direction": "高于中枢" if r > med else "低于中枢",
            })

    mutations = []
    for i in range(1, len(base)):
        d = base[i] - base[i - 1]
        if abs(d) > mut_mult * scale:
            mutations.append({
                "year": int(base_years[i]),
                "prev_year": int(base_years[i - 1]),
                "value": round(float(base[i]), 4) if mode != "levels" else round(float(base[i]), 2),
                "prev_value": round(float(base[i - 1]), 4) if mode != "levels" else round(float(base[i - 1]), 2),
                "delta": round(float(d), 4) if mode != "levels" else round(float(d), 2),
                "delta_ratio": (round(float(d / base[i - 1]), 4)
                                if mode == "levels" and base[i - 1] else None),
                "threshold": round(float(mut_mult * scale), 4) if mode != "levels" else round(float(mut_mult * scale), 2),
            })

    rec.update({
        "years": [int(y) for y in years],
        "values": [round(v, 2) for v in vals],
        "base_years": [int(y) for y in base_years],
        "base_series": [round(float(x), 4) if mode != "levels" else round(float(x), 2)
                        for x in base],
        "center": center_desc,
        "median": round(float(med), 4) if mode != "levels" else round(float(med), 3),
        "scale": round(float(scale), 4) if mode != "levels" else round(float(scale), 3),
        "scale_kind": kind,
        "anomaly_threshold_abs": round(float(thresh * scale), 4) if mode != "levels"
        else round(float(thresh * scale), 3),
        "mutation_threshold_abs": round(float(mut_mult * scale), 4) if mode != "levels"
        else round(float(mut_mult * scale), 3),
        "anomalies": anomalies,
        "mutations": mutations,
        "n_anomalies": len(anomalies),
        "n_mutations": len(mutations),
        "anomaly_share": round(len(anomalies) / max(len(base), 1), 4),
        "min_year": years[0],
        "max_year": years[-1],
    })
    if mode == "yoy_floor":
        # 突变点按口径定义仍算在**原始年序列**上（邻期 |Δ| > 序列 MAD × 3），
        # 不能算在同比率序列上，否则量纲与口径都不对。
        med_l = statistics.median(vals)
        scale_l, _ = _scale(vals, med_l)
        muts = []
        for i in range(1, n):
            d = vals[i] - vals[i - 1]
            if abs(d) > mut_mult * scale_l:
                muts.append({
                    "year": years[i], "prev_year": years[i - 1],
                    "value": round(vals[i], 2), "prev_value": round(vals[i - 1], 2),
                    "delta": round(d, 2),
                    "delta_ratio": round(d / vals[i - 1], 4) if vals[i - 1] else None,
                    "threshold": round(mut_mult * scale_l, 2),
                })
        rec["mutations"] = muts
        rec["n_mutations"] = len(muts)
        rec["mutation_threshold_abs"] = round(mut_mult * scale_l, 2)
        rec["mutation_note"] = "突变点按原始年序列算（MAD × 3），与异常点口径分离"
        rec["materiality"] = {"level_floor": round(floor, 2),
                             "rule": "上年或当年 < 序列峰值 1% 的期次不进入异常判定"}
    return rec


def sensitivity(series, mode):
    out = {}
    for t in (2.5, 3.5, 5.0):
        r = detect(series, mode=mode, thresh=t)
        out[str(t)] = {"n_anomalies": r.get("n_anomalies", 0),
                       "years": [a["year"] for a in r.get("anomalies", [])]}
    return out


def run_all(series, modes=("levels", "rolling", "yoy", "yoy_floor")):
    results = []
    for k, s in series.items():
        s2 = dict(s)
        s2["key"] = k
        rec = {"key": k, "label": s["label"], "n": len(s["values"]),
               "eligible": len(s["values"]) >= MIN_LEN,
               "note": s.get("note", ""), "supplementary": bool(s.get("supplementary")),
               "modes": {}}
        if not rec["eligible"]:
            rec["reason"] = f"序列长度 {rec['n']} < {MIN_LEN}"
            rec["years"] = s["years"]
            rec["values"] = s["values"]
        for m in modes:
            r = detect(s2, mode=m)
            r["sensitivity"] = sensitivity(s2, m) if rec["eligible"] else {}
            rec["modes"][m] = r
        results.append(rec)
    return results


def main():
    refresh = "--refresh" in sys.argv
    series = build_series(refresh=refresh)
    results = run_all(series)

    cache = {
        "metric": METRIC,
        "built_at": "2026-10-22",
        "params": {"threshold": THRESH_ANOM, "mutation_mult": MUT_MULT,
                   "min_len": MIN_LEN, "rolling_window": ROLL_WIN},
        "series": results,
    }
    save_cache(SERIES_CACHE, cache)

    eligible = [r for r in results if r["eligible"]]
    inelig = [r for r in results if not r["eligible"]]
    payload = {
        "metric_id": METRIC,
        "metric_name": "监测异常点识别",
        "data_support_level": "部分支持",
        "run_at": "2026-10-22",
        "db": "gkx@183.240.141.251:3318（专利序列零 DB，读面板缓存）",
        "params": cache["params"],
        "modes": {
            "levels": "口径原式：全序列 median + MAD，|x-median|/MAD > 3.5",
            "yoy": "同比变化率序列上的同一阈值",
            "rolling": "前 5 期滚动 median 作局部中枢，残差按 MAD 标准化",
            "yoy_floor": "同比变化率 + 低基数物质性门槛（< 峰值 1% 不判），推荐交付口径",
        },
        "recommended_mode": "yoy_floor",
        "eligible_series": len(eligible),
        "ineligible_series": [
            {"key": r["key"], "label": r["label"], "n": r["n"], "reason": r["reason"]}
            for r in inelig
        ],
        "series": results,
        "summary": {
            "n_series_total": len(results),
            "n_series_eligible": len(eligible),
            "literal_levels_anomalies": sum(r["modes"]["levels"].get("n_anomalies", 0)
                                            for r in eligible),
            "rolling_anomalies": sum(r["modes"]["rolling"].get("n_anomalies", 0)
                                     for r in eligible),
            "yoy_anomalies": sum(r["modes"]["yoy"].get("n_anomalies", 0)
                                 for r in eligible),
            "yoy_floor_anomalies": sum(r["modes"]["yoy_floor"].get("n_anomalies", 0)
                                      for r in eligible),
            "yoy_floor_hits": [{"key": r["key"],
                               "hits": [{"year": a["year"], "value": a["value"],
                                         "score": a["score"], "direction": a["direction"]}
                                        for a in r["modes"]["yoy_floor"]["anomalies"]]}
                              for r in eligible if r["modes"]["yoy_floor"]["anomalies"]],
            "level_degenerate_series": [
                r["key"] for r in eligible
                if r["modes"]["levels"].get("anomaly_share", 0) > 0.30
            ],
        },
        "gaps": [
            "专利年度序列只有 2021—2026 共 6 期，达不到口径要求的 ≥8，不能作为监测时序。",
            "学者只有存量表（h_index/paper_nums 为截面），没有按年存量，学者序列实为「学者-论文关系条数」。",
            "底册 99.82% 为深圳都市圈机构，机构新设序列是都市圈序列，不是全国序列。",
            "口径原式（全序列中枢）在中文论文（19/46=41.3%）与项目（12/38=31.6%）两条序列上命中率过高，已判定退化，不能直接出结论。",
            "备选算法孤立森林未实施：单变量年序列 + 无标签，MAD 已足够，且无法验证。",
        ],
    }
    write_out(METRIC, payload)

    print(json.dumps(payload["summary"], ensure_ascii=False, indent=1)[:4000])
    for r in results:
        if r["eligible"]:
            print(f"{r['key']:<18} n={r['n']:<3} "
                  f"levels={r['modes']['levels']['n_anomalies']:<3} "
                  f"rolling={r['modes']['rolling']['n_anomalies']:<3} "
                  f"yoy={r['modes']['yoy']['n_anomalies']:<3} "
                  f"yoy_floor={r['modes']['yoy_floor']['n_anomalies']:<3} "
                  f"share_levels={r['modes']['levels']['anomaly_share']}")
        else:
            print(f"{r['key']:<18} n={r['n']:<3} INELIGIBLE")


if __name__ == "__main__":
    main()
