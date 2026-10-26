#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_TINN_PATENT_COUNT · 专利数量（判：部分支持）

口径真源：`metrics/calc-logic/INNOV/M_INNOV_TINN_PATENT_COUNT` 并入 TINN_COMPOSITE 的
「专利数量（规模）」维：一行一个 IPC4，含申请量与授权量。

零 SQL：申请量取全表面板 `patent_panel_innov_20261021.json`（2,939,895 行，100% 扫描）；
授权量只有全域口径（`star_applicant_agg_gkx.json` 的 `agg[nm][1]` 合计 2,140,420），
**不能按 IPC4 拆**，故本文件只交付申请量维 + 全域授权率，并按此降档。

运行：python3 code/M_INNOV_TINN_PATENT_COUNT.py
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _tail21_common as T  # noqa: E402

MID = "M_INNOV_TINN_PATENT_COUNT"
TOTAL_ROWS = 2_939_895


def main() -> None:
    panel = json.loads((T.SNAP / "patent_panel_innov_20261021.json").read_text(encoding="utf-8"))
    iy = panel["ipc_year"]                       # "year|IPC4" -> 件数
    year_all = {int(k): int(v) for k, v in panel["year_all"].items()}
    ipc_all = {k: int(v) for k, v in panel["ipc_all"].items()}

    per: dict[str, dict[int, int]] = {}
    for k, n in iy.items():
        y, _, ipc = k.partition("|")
        per.setdefault(ipc, {})[int(y)] = int(n)
    ipc_sum = sum(sum(v.values()) for v in per.values())

    agg = json.loads((T.SNAP / "star_applicant_agg_gkx.json").read_text(encoding="utf-8"))["agg"]
    pub_total = sum(v[0] for v in agg.values())
    grant_total = sum(v[1] for v in agg.values())

    # 域排名：以 2021—2024 四年合计（2025/2026 不完整，不进排名分母）
    real_years = [2021, 2022, 2023, 2024]
    tot24 = sum(v.get(2024, 0) for v in per.values()) or 1
    hhi = sum((v.get(2024, 0) / tot24) ** 2 for v in per.values())
    window_rows = sum(year_all[y] for y in real_years)
    window_tagged = sum(sum(v.get(y, 0) for y in real_years) for v in per.values())
    ranking = sorted(per.items(), key=lambda kv: -sum(kv[1].get(y, 0) for y in real_years))
    rows = []
    for ipc, ser in ranking[:40]:
        c21, c24 = ser.get(2021, 0), ser.get(2024, 0)
        rows.append({
            "ipc4": ipc,
            "n_2021": c21, "n_2022": ser.get(2022, 0), "n_2023": ser.get(2023, 0),
            "n_2024": c24, "n_2025": None, "n_2026": None,
            "sum_2021_2024": sum(ser.get(y, 0) for y in real_years),
            "growth_2021_2024_pct": round(100 * (c24 - c21) / c21, 2) if c21 else None,
            "cagr_2021_2024_pct": round(100 * ((c24 / c21) ** (1 / 3) - 1), 2) if c21 else None,
            "share_2024_pct": round(100 * c24 / tot24, 3),
        })

    res = {
        "metric_id": MID,
        "metric_name": "专利数量",
        "support_judgment": "部分支持",
        "object": "技术领域（IPC 主分类前 4 位）× 申请年",
        "verdict_reason": (
            "申请量维完全可算（全表面板 2,939,895 行，IPC4×年 2,456 格）；"
            "授权量维无法按 IPC4 拆——库内只有全域授权数 2,140,420（授权率 72.81%）与"
            "按申请人的授权数，没有任何缓存带「IPC4×年×授权」。要拆必须对 294 万行主表按 "
            "granted_number 做全表聚合，实测该类查询 600 秒断连（DATA_FACTS §3.6/§3.12），故不执行。"
            "两个子项缺一，按档位定义落「部分支持」"),
        "data_source": "code/_snapshots21/patent_panel_innov_20261021.json（全量 2,939,895 行）；"
                       "star_applicant_agg_gkx.json（授权数合计）",
        "sql_count": 0,
        "probe": {
            "patent_rows": TOTAL_ROWS,
            "panel_rows": panel["rows"],
            "panel_chunks": panel["chunks"],
            "panel_partial": panel["rows"] < TOTAL_ROWS,
            "ipc4_distinct": len(per),
            "ipc_year_cells": len(iy),
            "ipc_all_rows_all_years": sum(ipc_all.values()),
            "ipc_year_window": panel["window"],
            "ipc_tagged_rows_window": window_tagged,
            "ipc_window_rows": window_rows,
            "ipc_tagged_pct_window": round(100 * window_tagged / window_rows, 2),
            "ipc_untagged_rows_window": window_rows - window_tagged,
            "ipc_2025_2026_breakdown": "面板未采（window 仅 2021—2024），2025/2026 的 IPC4 序列不可从缓存取",
            "applicants": len(agg),
            "grant_total": grant_total,
            "grant_rate_pct": round(100 * grant_total / pub_total, 2),
            "hhi_2024_ipc4": round(hhi, 4),
            "effective_domains_2024": round(1 / hhi, 1),
        },
        "year_all": {str(k): v for k, v in sorted(year_all.items())},
        "type_by_year": {str(k): v for k, v in sorted(panel["year_all"].items())},
        "top_ipc4": rows,
        "growth": {
            "base_window": [2021],
            "end_year": 2024,
            "note": "库内专利只覆盖 2021—2026；2021 是唯一可用基线年，故 CAGR 分母只有 2021 单年，"
                    "不是五年均值。2025（440,401）与 2026（74,810）为不完整年，不进增速",
        },
        "base_years_used": [2021, 2022, 2023, 2024],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_year_block": T.base_year_block(
            [2021, 2022, 2023, 2024], [2017, 2018, 2019, 2020],
            "gkx.dwd_patent 的 apdt_year 只有 2021—2026；2017—2020 零行，任何「五年基线」都不成立，"
            "CAGR 分母只能用 2021 单年"),
        "coverage": {
            "apply_dim": "全量：面板 2,939,895/2,939,895 = 100%",
            "ipc_dim": f"2021—2024 窗口内主分类 IPC4 已标注 {window_tagged:,}/{window_rows:,} = "
                       f"{round(100 * window_tagged / window_rows, 2)}%；全表（含 2025/2026）"
                       f"{sum(ipc_all.values()):,}/{TOTAL_ROWS:,} = "
                       f"{round(100 * sum(ipc_all.values()) / TOTAL_ROWS, 2)}%",
            "grant_dim": "仅全域（2,140,420 件 / 72.81%），无 IPC4 拆分",
            "year_dim": "2021—2026 六档，其中 2025/2026 不完整",
        },
        "gaps": [
            "授权量不可按 IPC4 拆：需供应方提供 IPC4×年×授权号非空的聚合结果表",
            f"2021—2024 窗口内 {window_rows - window_tagged:,} 行无主分类 IPC（"
            f"{round(100 * (window_rows - window_tagged) / window_rows, 2)}%），按 IPC4 排名时分母不是全表",
            "2025/2026 的 IPC4×年明细不在面板 window 内，只有全表 IPC4 合计",
            "2017—2020 零行，无法做五年趋势或五年基线",
            "2025（440,401）与 2026（74,810）为截断年，不能与 2021—2024 直接同比",
        ],
        "repair_requirements": [
            "补 IPC4×年×授权量结果表（或给 dwd_patent.apdt_year/main_classification_ipcr 建联合索引）",
            "补 2020 及以前年度的专利行，才能支撑五年基线",
        ],
    }
    T.write_out(MID, res)
    print(json.dumps(res["probe"], ensure_ascii=False, indent=1))
    print(rows[:5])


if __name__ == "__main__":
    main()
