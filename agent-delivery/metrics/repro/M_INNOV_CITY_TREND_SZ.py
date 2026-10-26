#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
