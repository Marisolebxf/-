#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_TINN_FORECAST · 技术创新趋势预测（判：部分支持）

口径真源：`metrics/calc-logic/INNOV/M_INNOV_TINN_FORECAST.md`（V1.5-20260901）
三维年序列：专利数量（年申请量）/ 专利质量（年被引合计）/ 技术市场潜力（年转移）；
Holt 线性趋势外推 h=2，约 80% 区间；有效期数 n = t_max - t_min + 1，**n < 8 不出预测**。

本批实测
--------
* 专利数量：IPC4×年只有 2021—2024 四个真实年（2025/2026 为截断年）→ n=4 < 8 → 不拟合；
* 专利质量：被引表无申请年字段、无法回连主表 → 无年序列；
* 技术市场潜力：转移表 22,809 行有年份（2021—2026），但无 IPC4 归属 → 只有全域序列。
按派单书与口径，本脚本**不做任何回归外推**，改为截面动量打分（2021→2024 真实增速），
并在产物里把 `forecast` 置空、写明 `skip_reason=short_series`。

运行：python3 code/M_INNOV_TINN_FORECAST.py（零 SQL）
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _tail21_common as T  # noqa: E402

MID = "M_INNOV_TINN_FORECAST"
REAL_YEARS = [2021, 2022, 2023, 2024]
MIN_YEARS = 8


def main() -> None:
    panel = json.loads((T.SNAP / "patent_panel_innov_20261021.json").read_text(encoding="utf-8"))
    per: dict[str, dict[int, int]] = {}
    for k, n in panel["ipc_year"].items():
        y, _, ipc = k.partition("|")
        per.setdefault(ipc, {})[int(y)] = int(n)
    year_all = {int(k): int(v) for k, v in panel["year_all"].items()}
    tr_year = {int(r[0]): int(r[1]) for r in T.rows_of(T.tail(), "transfer_year")}

    cand = []
    for ipc, s in per.items():
        base = s.get(2021, 0)
        if base < 100:            # 基数过小的域增速不稳定，先剔（口径外工程约束，正文披露）
            continue
        c24 = s.get(2024, 0)
        cand.append({"ipc4": ipc, "n_2021": base, "n_2024": c24,
                     "growth_pct": round(100 * (c24 - base) / base, 2),
                     "cagr_pct": round(100 * ((c24 / base) ** (1 / 3) - 1), 2)})
    cand.sort(key=lambda r: -r["n_2024"])
    growths = [r["growth_pct"] for r in cand]
    pctl = {r["ipc4"]: round(100 * sum(1 for g in growths if g <= r["growth_pct"]) / len(growths), 1)
            for r in cand}
    for r in cand:
        r["momentum_pctile"] = pctl[r["ipc4"]]

    n_years = len(REAL_YEARS)
    res = {
        "metric_id": MID,
        "metric_name": "技术创新趋势预测",
        "support_judgment": "部分支持",
        "object": "技术领域（IPC 主分类前 4 位）",
        "verdict_reason": (
            "口径要求 n≥8 才拟合 Holt；库内专利只有 2021—2024 四个真实年（2017—2020 零行、"
            "2025/2026 截断），n=4，且三维中只有「专利数量」有 IPC4 年序列（年被引无年份字段、"
            "年转移无 IPC4 归属）。故不拟合、不外推，改交截面动量（真实增速 + 分位）"),
        "data_source": "patent_panel_innov_20261021.json（IPC4×年 2021—2024）+ dwd_patent_transfer 年分布（全域）",
        "sql_count": 0,
        "probe": {
            "years_available": REAL_YEARS,
            "n_years": n_years,
            "min_years_required": MIN_YEARS,
            "skip_reason": "short_series",
            "forecast_emitted": False,
            "domains_considered": len(cand),
            "domains_base_ge_100": len(cand),
            "dim_count_series": {
                "专利数量": "IPC4×年 2021—2024，4 点",
                "专利质量（年被引）": "0 点：dwd_patent_cited 无申请年，20,515 行仅 475 可回连",
                "技术市场潜力（年转移）": "全域 6 点（2021—2026），但无 IPC4 归属",
            },
        },
        "transfer_year_global": {str(k): v for k, v in sorted(tr_year.items())},
        "patent_year_global": {str(k): v for k, v in sorted(year_all.items())},
        "momentum_top30": sorted(cand, key=lambda r: -r["momentum_pctile"])[:30],
        "momentum_bottom15": sorted(cand, key=lambda r: r["momentum_pctile"])[:15],
        "growth_dist": T.st(growths),
        "forecast": [],
        "forecast_note": "n=4 < 8，按口径不出预测；也未以任何线性/对数回归替代，避免把 4 个点外推成趋势",
        "base_years_used": REAL_YEARS,
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_year_block": T.base_year_block(
            REAL_YEARS, [2017, 2018, 2019, 2020],
            "增速分母只取 2021 单年（真实存在）；2017—2020 在库内零行，不按 0 摊入任何均值"),
        "gaps": [
            "2017—2020 零行，年序列只有 4 个真实点，达不到 n≥8 的拟合门槛",
            "年被引无年份字段（被引表只有 pn/patent_id + 计数），无法形成年度序列",
            "年转移序列只有全域口径，无 IPC4 归属",
            "2025/2026 为截断年，不能补足序列",
        ],
        "repair_requirements": [
            "补 2017—2020 专利行，使 IPC4×年至少 8 个真实点",
            "给 dwd_patent_cited 增加 apdt_year，或提供 pn→申请年映射",
            "给 dwd_patent_transfer 增加 ipc4 字段",
        ],
    }
    T.write_out(MID, res)
    print(json.dumps(res["probe"], ensure_ascii=False, indent=1))
    print(res["growth_dist"])
    print(res["momentum_top30"][:5])


if __name__ == "__main__":
    main()
