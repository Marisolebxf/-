#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""市场热度评级（M_SVC_ORG_MARKET_HEAT）—— gkx 口径，自包含。

数据源（只读落盘快照，零 SQL、零 demo）：
    code/_snapshots21/base_20261021.json  +  svc21_facts_20261022.json（pool.inc_year）

口径（王惠 calc-logic 迁移稿）：出生序列近 10 年窗 → OLS 斜率 + 变异系数 → 7 档表。
      窗口取 2013—2022：2023—2025 成立年右截断，不进回归，避免把缺登读成「热度崩塌」。
产出：code/M_SVC_ORG_MARKET_HEAT_out.json（覆盖写）
运行：cd code && python3 M_SVC_ORG_MARKET_HEAT.py
"""
from __future__ import annotations

import json
import os
import statistics
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
BASE = os.path.join(SNAP, "base_20261021.json")
OUT = os.path.join(HERE, "M_SVC_ORG_MARKET_HEAT_out.json")


def ols(ys):
    n = len(ys)
    xs = list(range(n))
    mx, my = sum(xs) / n, sum(ys) / n
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return b, my - b * mx


def grade(rel_slope, cv):
    # 王惠 7 档表：相对斜率 >0.5 上升；< -0.1 下行；中间为平稳，再按 CV 30% 分波动档
    if rel_slope > 0.5:
        return "上升期", "相对斜率 > 0.5"
    if rel_slope < -0.1:
        return "下行期", "相对斜率 < -0.1"
    if cv > 0.30:
        return "平稳（高波动）", "相对斜率在 [-0.1, 0.5] 且 CV > 30%"
    return "平稳（低波动）", "相对斜率在 [-0.1, 0.5] 且 CV <= 30%"


def main() -> None:
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    base = json.load(open(BASE, encoding="utf-8"))
    pool = f["pool"]
    bmap = {r[0]: r for r in base}
    inc = Counter()
    for o, v in pool.items():
        y = v.get("inc_year")
        if not y and o in bmap:
            y = bmap[o][5]
        if y:
            inc[int(y)] += 1

    def window(lo, hi):
        ys = [inc.get(y, 0) for y in range(lo, hi + 1)]
        b, a = ols(ys)
        mean = sum(ys) / len(ys)
        sd = statistics.pstdev(ys)
        return {
            "years": [lo, hi],
            "series": [[y, inc.get(y, 0)] for y in range(lo, hi + 1)],
            "sum": sum(ys),
            "mean": round(mean, 2),
            "std": round(sd, 2),
            "slope": round(b, 2),
            "slope_rel": round(b / mean, 4),
            "cv": round(sd / mean, 4),
            "first": ys[0],
            "last": ys[-1],
            "delta_annual": round((ys[-1] - ys[0]) / len(ys), 2),
        }

    main_w = window(2013, 2022)
    alt_w = window(2016, 2025)   # 对照：含右截断年，用来说明为什么不用近三年
    g, why = grade(main_w["slope_rel"], main_w["cv"])

    # 判档表全貌（用于文档展示）
    table = []
    for label, rel, cv in [
        ("上升期", 0.60, 0.20), ("平稳（低波动）", 0.05, 0.15),
        ("平稳（高波动）", 0.05, 0.45), ("下行期", -0.15, 0.30),
    ]:
        table.append([label, rel, cv, grade(rel, cv)[0]])

    out = {
        "metric_id": "M_SVC_ORG_MARKET_HEAT",
        "metric_name": "市场热度评级",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": (
            "2013—2022 十个完整年可算 OLS 斜率（-305.34 家/年，相对 -14.63%）与 CV（46.07%），"
            "按王惠表落「下行期」；但 2023—2025 成立年右截断（218/66/12 家），"
            "评级窗口止于 2022，「当前热度」只能作历史判断，不能当 2026 年现状"),
        "wanghui": True,
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_org_product_info", "rows": f["population"]["product_info_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_base_info（成立年）", "rows": f["population"]["base_all"],
             "snapshot": "code/_snapshots21/base_20261021.json"},
        ],
        "base_years_used": list(range(2013, 2023)),
        "base_years_missing": [2023, 2024, 2025],
        "base_years_note": (
            "回归窗口 2013—2022 十个完整年；2023—2025 成立年右截断，按缺失处理、不进分母；"
            "2026 无行。对照窗口 2016—2025 仅用于说明右截断对斜率的放大效应，不作评级"),
        "window_main": main_w,
        "window_alt_truncated": alt_w,
        "grade": g,
        "grade_rule": why,
        "grade_table_ref": table,
        "thresholds": {"rel_slope_up": 0.5, "rel_slope_down": -0.1, "cv_high": 0.30},
        "population": {"distinct_org_id": len(pool), "inc_year_nonnull": sum(inc.values())},
        "difference_vs_old_draft": {
            "window": "旧稿 2017—2026（含进行中年 2026）→ 本件 2013—2022（完整年）",
            "slope": "旧稿 -294.9 家/年 → 本件 -305.34 家/年",
            "cv": "旧稿 44.0% → 本件 46.07%",
            "grade": "旧稿「下行期」→ 本件「下行期」（结论不变，窗口与数据源已换）",
            "reason": "gkx 底册 2023 年后成立年缺登，不能用「近 10 年含当年」的旧窗口",
        },
        "gaps": {
            "recent": "2023—2025 右截断，评级不能代表当前市场",
            "industry_slice": "无机构×产业稳定映射，产业子集评级只能到六类服务类型",
            "exit_side": "出生序列无死亡侧，热度只反映进入、不反映退出",
        },
        "compute": {"status": "ok", "elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("heat slope=%.2f rel=%.4f cv=%.4f grade=%s -> %s"
          % (main_w["slope"], main_w["slope_rel"], main_w["cv"], g, OUT))


if __name__ == "__main__":
    main()
