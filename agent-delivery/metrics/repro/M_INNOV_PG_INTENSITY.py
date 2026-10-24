#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""政策扶持力度（M_INNOV_PG_INTENSITY）——零 SQL 复算。

王惠口径（V1.5-20260901）：政策数量 / 政策类型 / 政策覆盖面 三维，城内极值归一后等权 ×100。
本脚本对三维逐一实测：
  D1 数量 = COUNT(DISTINCT id)
  D2 类型 = COUNT(DISTINCT type)
  D3 覆盖面 = COUNT(DISTINCT district)；district 全空时退 theme —— 本库 theme 恒为 0，
     故 D3 在四城全部不可算，主分只合成 D1+D2（权重重归一），D3 另出敏感性变体。

输入：code/_snapshots21/pg_policy_rows_20261021.json
产物：code/M_INNOV_PG_INTENSITY_out.json
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_INNOV_PG_INTENSITY_out.json")
METRIC_ID = "M_INNOV_PG_INTENSITY"
PLACEHOLDER = {"NULL", "", "NONE", "-"}
FOUR = ["深圳市", "广州市", "东莞市", "惠州市"]
WINDOW = (2016, 2021)  # 近期年窗（2022 起语料截断）


def norm(v) -> str:
    s = "" if v is None else str(v).strip()
    return "" if s.upper() in PLACEHOLDER else s


def parse_rank(v) -> str:
    s = norm(v)
    if not s:
        return ""
    if s.startswith("["):
        try:
            arr = json.loads(s)
            return norm(arr[0]) if arr else ""
        except Exception:
            return ""
    return s


def minmax(vals, x):
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return 50.0
    return 100.0 * (x - lo) / (hi - lo)


def main() -> None:
    t0 = time.time()
    rows = json.load(open(os.path.join(SNAP, "pg_policy_rows_20261021.json"), encoding="utf-8"))
    base = json.load(open(os.path.join(SNAP, "base_20261021.json"), encoding="utf-8"))
    for r in rows:
        for k in ("city", "district", "type", "province"):
            r[k] = norm(r.get(k))
        r["lvl"] = parse_rank(r.get("rank"))
        y = norm(r.get("publish_year"))
        r["yr"] = int(y) if y.isdigit() else None

    firms = Counter(b[4] for b in base)
    n_all = len(rows)

    # theme 维体检：若全表 theme 只有一个取值，王惠的 fallback 失效
    theme_vals = Counter()
    raw_theme = json.load(open(os.path.join(SNAP, "policy_base_20261021.json"), encoding="utf-8"))
    for r in raw_theme:
        theme_vals[str(r.get("theme"))] += 1

    # ---------- 三维原始值（全量 / 近期窗口各一套） ----------
    def calc(city, window=None):
        sub = [r for r in rows if r["city"] == city]
        if window:
            sub = [r for r in sub if r["yr"] and window[0] <= r["yr"] <= window[1]]
        return {
            "n": len(sub),
            "ids": len({r["id"] for r in sub}),
            "types": len({r["type"] for r in sub if r["type"]}),
            "districts": len({r["district"] for r in sub if r["district"]}),
            "levels": len({r["lvl"] for r in sub if r["lvl"]}),
            "type_list": sorted({r["type"] for r in sub if r["type"]}),
        }

    all_stats = {c: calc(c) for c in FOUR}
    win_stats = {c: calc(c, WINDOW) for c in FOUR}

    # ---------- 主分：D1+D2（D3 不可算，权重重归一） ----------
    def score(stats):
        vals_n = [s["ids"] for s in stats.values()]
        vals_t = [s["types"] for s in stats.values()]
        out = {}
        for c, s in stats.items():
            sn, st = minmax(vals_n, s["ids"]), minmax(vals_t, s["types"])
            out[c] = {"n_norm": round(sn, 2), "type_norm": round(st, 2),
                      "score_2dim": round((sn + st) / 2, 2)}
        return out

    score_all = score(all_stats)
    score_win = score(win_stats)

    # ---------- 敏感性：用层级广度代替区县广度（明确标注为报告假设） ----------
    def score_3dim(stats):
        vals_n = [s["ids"] for s in stats.values()]
        vals_t = [s["types"] for s in stats.values()]
        vals_l = [s["levels"] for s in stats.values()]
        out = {}
        for c, s in stats.items():
            v = (minmax(vals_n, s["ids"]) + minmax(vals_t, s["types"]) + minmax(vals_l, s["levels"])) / 3
            out[c] = round(v, 2)
        return out

    lvl_score = score_3dim(all_stats)

    # ---------- 四城明细 ----------
    detail = []
    for c in FOUR:
        a, w = all_stats[c], win_stats[c]
        detail.append({
            "city": c,
            "all": a,
            "window_2016_2021": w,
            "firms": firms.get(c, 0),
            "policies_per_1000_firms": round(1000 * a["ids"] / firms.get(c, 1), 3),
            "window_per_1000_firms": round(1000 * w["ids"] / firms.get(c, 1), 3),
            "score_all_2dim": score_all[c]["score_2dim"],
            "score_window_2dim": score_win[c]["score_2dim"],
            "score_all_3dim_level_proxy": lvl_score[c],
            "coverage_dim_usable": a["districts"] > 0,
        })

    result = {
        "metric_id": METRIC_ID,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "data_source": "gkx.dwd_policy_base @ 183.240.141.251:3318（快照 20,000 行，零 SQL 复算）",
        "support_judgment": "部分支持",
        "formula": "score = mean(norm(COUNT(DISTINCT id)), norm(COUNT(DISTINCT type))) × 100（D3 缺测，权重重归一）",
        "n_records": n_all,
        "window": {"from": WINDOW[0], "to": WINDOW[1],
                   "reason": "2022 年 289 条、2023—2026 无有效记录，年窗止于 2021"},
        "base_years_used": list(range(WINDOW[0], WINDOW[1] + 1)),
        "base_years_missing": [2022, 2023, 2024, 2025, 2026],
        "theme_check": {
            "distinct_values": len(theme_vals),
            "dist": theme_vals.most_common(5),
            "verdict": "theme 全表仅 0/1 两值且 19,998 行为 0，王惠的 district→theme 回退链在本库失效",
        },
        "detail": detail,
        "score_2dim_all": score_all,
        "score_2dim_window": score_win,
        "score_3dim_level_proxy": lvl_score,
        "caveats": [
            "D3 覆盖面在四城均不可算：深圳 4 个区县、广州/东莞 0 个、惠州无记录；theme 回退亦失效",
            "覆盖率偏斜：东莞全库 8 条、惠州 0 条，与其企业数（33,590 / 9,979）严重不匹配，属采集偏向",
            "极值归一以四城为批内，样本仅 4 城，min-max 对最大值（深圳）天然给 100 分，排序不可外推",
            "level 代理的 3 维分只作敏感性，不得替代王惠的区县覆盖面",
        ],
        "runtime_sec": None,
    }

    print(f"[{METRIC_ID}] n={n_all}")
    print("theme 体检:", result["theme_check"]["dist"])
    for d in detail:
        print(f"{d['city']}: 全量 {d['all']['ids']} 件/{d['all']['types']} 类/区县 {d['all']['districts']}；"
              f"2016-2021 {d['window_2016_2021']['ids']} 件；2维分 {d['score_all_2dim']}（窗口 {d['score_window_2dim']}）")
    print("3维(level 代理):", lvl_score)

    result["runtime_sec"] = round(time.time() - t0, 3)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print(f"saved {OUT} ({result['runtime_sec']}s)")


if __name__ == "__main__":
    main()
