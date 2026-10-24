#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""政策时序指标（M_POLICY_TIMESERIES）——只读落盘快照，不连库。

输入：
  code/_snapshots21/policy_dims_20261023.json    年份/层级/类型底数（五件共用）
  code/_snapshots21/policy_struct_20261023.json  月度分布 + 2015—2024 可比政策窗口
输出：
  code/M_POLICY_TIMESERIES_out.json

口径（与 `calc-logic` / 注册表对齐，差异写在 MD §1.7）：
  发布量   = COUNT(*) GROUP BY publish_year（主键唯一，等价 COUNT(DISTINCT id)）
  同比     = (N_t − N_{t−1}) / N_{t−1}，只对**完整年**计算
  年化     = (N_end / N_start)^(1/k) − 1，端点只取完整年
  连续性   = 密度窗口内「有记录月份数 / 窗口月份数」
  可比政策 = 剔除 12 词表命中的采购/招标/展会/安保/通告类文本

「完整年」不是日历判断，而是**库内月份覆盖判断**：某年 12 个月都有记录才算完整年。
2022 只有 1—8 月有记录（9 月、11 月、12 月空），故 2022 不入同比与年化端点。
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).parent
DIMS = HERE / "_snapshots21" / "policy_dims_20261023.json"
STRUCT = HERE / "_snapshots21" / "policy_struct_20261023.json"
OUT = HERE / "M_POLICY_TIMESERIES_out.json"

METRIC = "M_POLICY_TIMESERIES"
STATS_MONTH = "2026-10"          # 统计月，只用于计算「尾部无记录月数」


def month_range(a: str, b: str) -> list[str]:
    y, m = int(a[:4]), int(a[5:7])
    out = []
    while (y, m) <= (int(b[:4]), int(b[5:7])):
        out.append(f"{y:04d}-{m:02d}")
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def main() -> int:
    dims = json.loads(DIMS.read_text(encoding="utf-8"))
    st = json.loads(STRUCT.read_text(encoding="utf-8"))

    year_dist = {int(k): v for k, v in dims["publish_year_dist"].items()
                 if k.isdigit()}
    month_dist = st["publish_month_dist"]
    win = st["effective_window"]
    pol_year = {int(k): v for k, v in win["policy_by_year"].items()}
    npol_year = {int(k): v for k, v in win["nonpolicy_by_year"].items()}

    # ---- 完整年判定：12 个月都有记录 ----
    month_by_year = {}
    for ym, n in month_dist.items():
        month_by_year.setdefault(int(ym[:4]), {})[ym[5:7]] = n
    full_years = sorted(y for y, mm in month_by_year.items() if len(mm) == 12)

    # ---- 年度序列（1981—2024 全量；窗口内另给可比口径）----
    series = []
    for y in sorted(year_dist):
        rec = {"year": y, "rows": year_dist[y], "share_of_total_pct":
               round(year_dist[y] / dims["rows"] * 100, 4)}
        if y in pol_year:
            rec["nonpolicy_excluded"] = npol_year.get(y, 0)
            rec["policy_rows"] = pol_year[y]
        rec["months_with_records"] = len(month_by_year.get(y, {}))
        rec["complete_year"] = y in full_years
        series.append(rec)

    # ---- 同比：只对「本年与上年都是完整年」的相邻对计算 ----
    yoy = {}
    for i in range(1, len(full_years)):
        y0, y1 = full_years[i - 1], full_years[i]
        if y1 - y0 != 1:
            continue
        n0 = year_dist.get(y0, 0)
        n1 = year_dist.get(y1, 0)
        if n0:
            yoy[str(y1)] = {
                "prev_year": y0, "prev_rows": n0, "rows": n1,
                "yoy_pct": round((n1 - n0) / n0 * 100, 4),
                "policy_yoy_pct": (round((pol_year[y1] - pol_year[y0]) / pol_year[y0] * 100, 4)
                                   if pol_year.get(y0) and pol_year.get(y1) else None),
            }

    # ---- 年化：2015→2021（连续 7 个完整年，6 个间隔）----
    base_a, base_b = 2015, 2021
    k = base_b - base_a
    cagr_all = ((year_dist[base_b] / year_dist[base_a]) ** (1 / k) - 1) * 100
    cagr_pol = ((pol_year[base_b] / pol_year[base_a]) ** (1 / k) - 1) * 100

    # ---- 连续性：先找最长连续有记录月段 ----
    months_in_window = sorted(m for m in month_dist if "2015" <= m[:4] <= "2024")
    run, best = [], []
    for m in months_in_window:
        if not run:
            run = [m]
            continue
        a, b = run[-1], m
        y, mo = int(a[:4]), int(a[5:7]) + 1
        if mo == 13:
            y, mo = y + 1, 1
        if f"{y:04d}-{mo:02d}" == b:
            run.append(b)
        else:
            if len(run) > len(best):
                best = run
            run = [b]
    if len(run) > len(best):
        best = run
    dense_start, dense_end = best[0], best[-1]
    dense_months = month_range(dense_start, dense_end)
    missing_inside = [m for m in dense_months if m not in month_dist]

    # 尾部：密度窗口结束后到统计月
    tail_months = month_range(
        (lambda s: f"{int(s[:4]) + (int(s[5:7]) == 12):04d}-"
                   f"{1 if int(s[5:7]) == 12 else int(s[5:7]) + 1:02d}")(dense_end),
        STATS_MONTH)
    tail_with = [m for m in tail_months if m in month_dist]
    tail_empty = [m for m in tail_months if m not in month_dist]

    # ---- 月度季节性与构成 ----
    season = {}
    for m in dense_months:
        if int(m[:4]) <= 2021:
            season[m[5:7]] = season.get(m[5:7], 0) + month_dist[m]
    season_total = sum(season.values())

    ytc = {}
    for kk, v in st["year_typeclass_cross"].items():
        y, tc = kk.split("|")
        if not y.isdigit():
            continue
        ytc.setdefault(int(y), {})[tc] = v
    composition = []
    for y in range(2015, 2025):
        row = ytc.get(y, {})
        tot = sum(row.values()) or 1
        composition.append({
            "year": y,
            "rows": sum(row.values()),
            "policy_doc_rows": row.get("政策文件类", 0) + row.get("规范性文件类", 0),
            "policy_doc_share_pct": round(
                (row.get("政策文件类", 0) + row.get("规范性文件类", 0)) / tot * 100, 4),
            "notice_rows": row.get("事务通知类", 0),
            "notice_share_pct": round(row.get("事务通知类", 0) / tot * 100, 4),
            "unlabeled_rows": row.get("未标注", 0),
        })

    ylc = {}
    for kk, v in st["year_level_cross"].items():
        y, lv = kk.split("|")
        if not y.isdigit():
            continue
        ylc.setdefault(int(y), {})[int(lv)] = v
    level_series = []
    for y in range(2015, 2023):
        row = ylc.get(y, {})
        level_series.append({
            "year": y,
            "national": row.get(4, 0), "provincial": row.get(3, 0),
            "city": row.get(2, 0), "district": row.get(1, 0), "unlabeled": row.get(0, 0),
        })

    out = {
        "metric_id": METRIC,
        "support_judgment": "部分支持",
        "base_years_used": [2015, 2016, 2017, 2018, 2019, 2020, 2021],
        "base_years_missing": [2022, 2023, 2024],
        "base_years_note": (
            "同比与年化只取 2015—2021 七个完整年（每年 12 个月都有记录）。"
            "2022 库内只有 1—8 月记录（9、11、12 月空），按不完整年排除，不入任何分母；"
            "2023 全年 0 行、2024 仅 1 行（2024-02-18），是采集断档，不按 0 摊入均值或趋势；"
            "2025—2026 未入库。故本件不产出 2022 年以后的同比与年化。"),
        "headline": {
            "rows": dims["rows"],
            "distinct_id": dims["distinct_id"],
            "year_min": min(year_dist),
            "year_max": max(year_dist),
            "years_with_records": len(year_dist),
            "full_years": len(full_years),
            "peak_year": max(year_dist, key=lambda y: year_dist[y]),
            "peak_rows": max(year_dist.values()),
            "latest_full_year": max(full_years),
            "latest_full_year_rows": year_dist[max(full_years)],
            "publish_date_min": st["publish_date"]["min"],
            "publish_date_max": st["publish_date"]["max"],
            "policy_rows_2015_2024": win["policy_rows_after_exclusion"],
            "nonpolicy_excluded": win["nonpolicy_excluded"],
        },
        "series": series,
        "growth": {
            "yoy_by_year": yoy,
            "cagr": {
                "start_year": base_a, "end_year": base_b, "intervals": k,
                "start_rows": year_dist[base_a], "end_rows": year_dist[base_b],
                "cagr_pct": round(cagr_all, 4),
                "start_policy_rows": pol_year[base_a], "end_policy_rows": pol_year[base_b],
                "cagr_policy_pct": round(cagr_pol, 4),
                "excluded": "2022 起（不完整年 + 断档），原因见 base_years_note",
            },
        },
        "continuity": {
            "dense_start": dense_start,
            "dense_end": dense_end,
            "dense_months": len(dense_months),
            "months_with_records": len(dense_months) - len(missing_inside),
            "missing_inside": missing_inside,
            "continuity_pct": round((len(dense_months) - len(missing_inside))
                                    / len(dense_months) * 100, 4),
            "tail_start": tail_months[0] if tail_months else None,
            "tail_months": len(tail_months),
            "tail_months_with_records": {m: month_dist[m] for m in tail_with},
            "tail_empty_months": len(tail_empty),
            "tail_first_empty": tail_empty[0] if tail_empty else None,
        },
        "seasonality": {
            "basis_years": "2015—2021 完整年",
            "by_month": {m: season[m] for m in sorted(season)},
            "by_month_share_pct": {m: round(season[m] / season_total * 100, 4)
                                   for m in sorted(season)},
            "peak_month": max(season, key=lambda m: season[m]),
            "trough_month": min(season, key=lambda m: season[m]),
        },
        "composition": composition,
        "level_series": level_series,
        "checks": [
            {"name": "年份合计闭合", "value": sum(year_dist.values()),
             "expected": dims["rows"], "ok": sum(year_dist.values()) == dims["rows"]},
            {"name": "窗口内可比政策", "value": win["policy_rows_after_exclusion"],
             "expected": win["window_rows"] - win["nonpolicy_excluded"],
             "ok": win["policy_rows_after_exclusion"] ==
             win["window_rows"] - win["nonpolicy_excluded"]},
            {"name": "完整年数", "value": len(full_years), "expected": 7,
             "ok": len(full_years) == 7},
        ],
        "provenance": {
            "snapshots": [
                "code/_snapshots21/policy_dims_20261023.json",
                "code/_snapshots21/policy_struct_20261023.json",
            ],
            "builders": [
                "code/_build_policy_dims_20261023.py",
                "code/_build_policy_struct_20261023.py",
            ],
            "source": dims["source"],
        },
        "notes": [
            "20,000 是库内存量，不是全国政策总量；年份字段覆盖 1981—2024。",
            "2023/2024 零行按采集断档记「未测」，不写「政策归零」。",
            "口径已剔除 620 条采购/招标/展会/安保/通告类文本，剔除词表 12 个，见 nonpolicy_rule。",
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[OK] {OUT}")
    print("full_years", full_years)
    print("peak", out["headline"]["peak_year"], out["headline"]["peak_rows"])
    print("cagr", round(cagr_all, 4), "policy", round(cagr_pol, 4))
    print("dense", dense_start, dense_end, len(dense_months), "missing", missing_inside)
    print("tail empty", len(tail_empty), "first", tail_empty[0] if tail_empty else None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
