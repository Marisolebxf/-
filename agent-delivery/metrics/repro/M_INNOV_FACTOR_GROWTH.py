#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_FACTOR_GROWTH · 科创要素增长趋势（INNOV / DS-01-FACTORS）。

seed 定义：选定要素类型在历史窗口上的增长率与趋势曲线，主展示年同比；
预测不混入本条（见 M_INNOV_FACTOR_FORECAST）。故本脚本只做历史增长率/趋势，不外推。

口径：
  年同比 g_t = (x_t - x_{t-1}) / x_{t-1}
  CAGR = (x_end / x_start)^(1/(y_end-y_start)) - 1   ← 分母是**真实存在的年份差**
  趋势 = OLS 斜率 + R²（在可比窗口内）

硬约束（DATA_FACTS §3.13 / 派单书专利陷阱）：
  `gkx.dwd_patent.apdt_year` 仅 2021–2026，**2017–2020 零行**。
  专利 CAGR 的 n 取 4（2021→2025 的年份差），**不是 5**；把 2017–2020 当 0
  或把缺失年摊进分母都会把增速放大数倍。专利数字只读面板缓存，零专利 SQL。

输出：code/M_INNOV_FACTOR_GROWTH_out.json
"""
from __future__ import annotations

import json
import math
import time
from pathlib import Path

import _gkxdb as G

HERE = Path(__file__).resolve().parent
FACTS = HERE / "_snapshots21" / "innov21_facts_20261021.json"
OUT = HERE / "M_INNOV_FACTOR_GROWTH_out.json"
METRIC_ID = "M_INNOV_FACTOR_GROWTH"

PAPER_BATCH_YEARS = (2024,)
PATENT_MISSING = (2017, 2018, 2019, 2020)


def yoy(series, skip=()):
    rows = []
    keys = sorted(series)
    for i in range(1, len(keys)):
        a, b = series[keys[i - 1]], series[keys[i]]
        if keys[i] in skip:
            rows.append({"year": keys[i], "value": b, "yoy": None,
                         "excluded": "入库批 / 残年，不作同比"})
            continue
        rows.append({"year": keys[i], "value": b,
                     "yoy": round((b - a) / a, 4) if a else None})
    return rows


def cagr(series, y0, y1):
    if y0 in series and y1 in series and series[y0] > 0:
        n = y1 - y0
        return round((series[y1] / series[y0]) ** (1 / n) - 1, 4), n
    return None, None


def ols(vals):
    n = len(vals)
    xs = list(range(n))
    mx, my = sum(xs) / n, sum(vals) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, vals))
    slope = sxy / sxx if sxx else 0.0
    pred = [my + slope * (x - mx) for x in xs]
    ssr = sum((y - p) ** 2 for y, p in zip(vals, pred))
    sst = sum((y - my) ** 2 for y in vals)
    return slope, (1 - ssr / sst if sst else 0.0)


def trend(series, y0, y1, skip=()):
    ys = [y for y in range(y0, y1 + 1) if y in series and y not in skip]
    vals = [series[y] for y in ys]
    if len(vals) < 3:
        return None
    slope, r2 = ols(vals)
    mean = sum(vals) / len(vals)
    return {"y0": ys[0], "y1": ys[-1], "n_periods": len(vals),
            "slope_per_year": round(slope, 1),
            "slope_pct_of_mean": round(100 * slope / mean, 2) if mean else None,
            "r2": round(r2, 4),
            "direction": ("上升" if slope > 0 and r2 >= 0.3
                          else ("下降" if slope < 0 and r2 >= 0.3 else "不明/平稳"))}


def monthly_paper_cv(year=2024):
    cur = G.gkx()
    try:
        cur.execute("SELECT LEFT(cover_date_start,6) m, COUNT(*) n FROM gkx.dwd_zh_paper "
                    "WHERE cover_year_start=%s GROUP BY 1 ORDER BY 1", (str(year),))
        rows = cur.fetchall()
    finally:
        cur.close()
    vals = [int(n) for _, n in rows if n]
    if not vals:
        return None, []
    mu = sum(vals) / len(vals)
    sd = math.sqrt(sum((v - mu) ** 2 for v in vals) / len(vals))
    return (round(sd / mu, 4) if mu else None,
            [{"month": m, "n": int(n)} for m, n in rows])


def main():
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    py = {int(k): int(v) for k, v in f["paper_year"].items()}
    jy = {int(k): int(v) for k, v in f["project_year"].items()}
    pat = {int(k): int(v) for k, v in f["patent"]["year"].items()}

    series = {
        "专利": {k: v for k, v in pat.items() if 2021 <= k <= 2026},
        "论文": {k: v for k, v in py.items() if 2005 <= k <= 2026},
        "项目": {k: v for k, v in jy.items() if 2005 <= k <= 2023},
    }
    comparable = {"专利": (2021, 2025), "论文": (2005, 2023), "项目": (2005, 2020)}

    YOY_SKIP = {"专利": (2026,), "论文": (2024, 2025, 2026), "项目": (2021, 2022, 2023)}
    out_series = {}
    for name, s in series.items():
        keys = sorted(s)
        y0, y1 = comparable[name]
        skip = PAPER_BATCH_YEARS if name == "论文" else ()
        sc = {k: v for k, v in s.items() if y0 <= k <= y1 and k not in skip}
        c, n = cagr(sc, y0, y1)
        out_series[name] = {
            "years": keys,
            "values": [s[k] for k in keys],
            "n_periods": len(keys),
            "yoy_all": yoy(s, skip=YOY_SKIP[name]),
            "comparable_window": [y0, y1],
            "cagr_denominator_years": n,
            "yoy_comparable": yoy(sc),
            "cagr_comparable": c,
            "trend_comparable": trend(sc, y0, y1, skip=skip),
            "trend_window": [y0, y1],
        }

    # 专利 CAGR 的「分母陷阱」自证：只作对照，不参与结论
    pat2021, pat2025 = pat.get(2021), pat.get(2025)
    n_real = 2025 - 2021
    trap = {
        "real_years": n_real,
        "cagr_n4": round((pat2025 / pat2021) ** (1 / 4) - 1, 4),
        "cagr_if_wrongly_divided_by_5": round((pat2025 / pat2021) ** (1 / 5) - 1, 4),
        "note": "真实年份差为 4；若把 2017–2020 的空缺摊进分母写成 5，会把 -7.62% 读成 -6.10%，"
                "方向不变但幅度被压缩 1.5 个百分点；把缺失年当 0 更会得到荒谬的负增长。",
    }

    pap_clean = {k: v for k, v in series["论文"].items() if k not in PAPER_BATCH_YEARS}
    main_view = {
        "专利_2021_2025": {"yoy": out_series["专利"]["yoy_comparable"],
                         "cagr": out_series["专利"]["cagr_comparable"],
                         "trend": out_series["专利"]["trend_comparable"]},
        "论文_2005_2023_去2024": {"yoy": out_series["论文"]["yoy_comparable"],
                               "cagr_2015_2023": cagr(pap_clean, 2015, 2023)[0],
                               "trend_2015_2023": trend(pap_clean, 2015, 2023)},
        "项目_2005_2020": {"yoy": out_series["项目"]["yoy_comparable"],
                         "cagr": out_series["项目"]["cagr_comparable"],
                         "trend": out_series["项目"]["trend_comparable"]},
    }

    cv, mrows = monthly_paper_cv(2024)
    gaps = {
        "期刊": "dwd_zh_journal（2,796 行）为期刊名录，publication_type 全为「期刊」，"
                "无年度件数时序列（founding_time 是创刊时间，不是年度产出）",
        "会议": "zh/en journal 与 zh_paper 的 publication_type 均无「会议」；会议实体 0",
        "专利截断": "apdt_year 仅 2021–2026；2017–2020 零行（结构性缺失，不是「无专利」）。"
                    "2026 为残年（74,810 件，采集止于 2026-10 且公开滞后），不与 2025 做同比。"
                    "专利可比窗口固定为 2021–2025（5 个观测、4 个年份差）。",
        "论文2024": f"2024 年 32,379 篇 = 2023 年（6,651）的 4.87 倍，2025 又回落至 6,548；"
                    f"2024 年月度分布 CV={cv}（近均匀、连续有值），更符合批量入库年而非真实发表激增，"
                    "故 2024 不纳入趋势/同比主口径，仅作披露",
        "项目截断": "项目库 2021/2022/2023 仅 2,339/58/6 条（2015-2020 年均约 4,300 条）→ 2021 起为入库截断，"
                    "项目趋势窗口收缩至 2005–2020，2021 年后不可解释",
    }

    out = {
        "metric_id": METRIC_ID,
        "metric_name": "科创要素增长趋势",
        "domain": "INNOV / DS-01-FACTORS",
        "formula_owner": "仿王惠（推测定义）：seed 公式 pending_cosign（唐绍祖未签）",
        "generated_at": time.strftime("%Y-%m-%d"),
        "source_db": "gkx",
        "source_detail": {
            "专利": "patent_panel_innov_20261021.json（全量 2,939,895 行，零专利 SQL）",
            "论文/项目": "gkx.dwd_zh_paper / gkx.dwd_zh_project（小表聚合）",
        },
        "definition_used": "年同比 g_t=(x_t-x_{t-1})/x_{t-1}；CAGR=(x_end/x_start)^(1/(y_end-y_start))-1；"
                           "OLS 斜率+R²；不含预测",
        "baseline_policy": {
            "patent_present_years": sorted(pat),
            "patent_missing_years": list(PATENT_MISSING),
            "patent_comparable_window": [2021, 2025],
            "cagr_denominator_years": 4,
            "rule": "分母只用真实存在的年份；缺失年不补 0、不摊进分母；2026 残年不入同比",
        },
        "probes": {"dwd_patent": sum(pat.values()), "dwd_zh_paper": sum(py.values()),
                   "dwd_zh_project": sum(jy.values()),
                   "dwd_zh_journal": int(f["table_counts"]["dwd_zh_journal"]["rows"]),
                   "conference_entities": 0},
        "series": out_series,
        "main_view": main_view,
        "cagr_denominator_check": trap,
        "granularity": {
            "年": "专利/论文/项目均可",
            "月": "论文可由 cover_date_start 派生（2024 月度为入库批，CV 见 gaps）；"
                  "专利 apdt_month 需在面板新增维度后才可取数，**当前禁止为月粒度查 dwd_patent**",
            "季": "论文可派生；专利当前不可（同上）",
            "日/周": "不承诺：项目无可靠日粒度，专利日粒度需新增面板维",
            "paper_2024_monthly_cv": cv,
            "paper_2024_monthly": mrows,
        },
        "gaps": gaps,
        "support_judgment": {
            "data_support_level": "部分支持",
            "criteria": {
                "structure": "专利/论文/项目三要素时序结构齐备；期刊、会议无年度件数序列",
                "volume": "专利 293.99 万件（6 期）、论文 10.09 万篇（22 期）、项目 5.85 万项（38 期）",
                "reproducible": True,
                "complete_dimension": False,
            },
            "note": "seed 要求的四要素（会议/项目/专利/期刊）中，期刊与会议两维无年度件数承载；"
                    "专利仅 6 期（2021–2026）、2017–2020 结构性缺失、2026 残年；论文 2024 存在入库年偏斜。"
                    "三要素历史同比/CAGR 可算，但四维不齐 -> 部分支持。",
        },
        "elapsed_sec": round(time.time() - t0, 2),
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(json.dumps({"level": out["support_judgment"]["data_support_level"],
                      "patent": out_series["专利"]["trend_comparable"],
                      "patent_cagr": out_series["专利"]["cagr_comparable"],
                      "patent_trap": trap,
                      "paper": out_series["论文"]["trend_comparable"],
                      "paper_cagr": main_view["论文_2005_2023_去2024"]["cagr_2015_2023"],
                      "project": out_series["项目"]["trend_comparable"],
                      "cv2024": cv}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
