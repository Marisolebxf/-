#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_REG_TECH_MATURITY 区域技术成熟度（链 × 城，0—100 分）。

口径来源：calc-logic V2-20260824（公式定义人 王惠）。
    区域链上企业专利按**公开年**近 k 年复合增速判定技术生命周期位置。
本库实现的三处受限期（全部在 MD §三/§四 披露，判档据此降为「部分支持」）：
    1. 面板仅落 `apdt_year`（申请年，窗口 2021—2024），无 `pbdt_year` 缓存
       → 时间轴用申请年代理（源表有 pbdt_year，但取它要扫 294 万行，禁）；
    2. `dwd_patent` 2017—2020 零行 → 上期增速只能用 k=2 年化口径回算
       （g_prev 与 g 窗口不等长，已在公式中标注）；
    3. 面板 app_year 窗口止于 2024 → 统计年只能取 2024，无法出 2025。

取数：全部离线。`patent_panel_innov_20261021.json`（申请人×年）×
`bridge_20261021.json`（企业→链→城）字典 join，零 DB。
"""
from __future__ import annotations

import json
import time
from pathlib import Path

BASE = Path(__file__).parent
SNAP = BASE / "_snapshots21"
METRIC = "M_CHAIN_REG_TECH_MATURITY"

ROOTS = ["INB1204", "INB1209", "INB1236", "INB1303", "INB1306", "INB1309",
         "INB1323", "INB1333", "INB1354", "INB1502", "INB2503", "INB2505"]
CITY4 = ["深圳市", "广州市", "东莞市", "惠州市"]
THETA = 0.05      # 近零阈值
STAT_YEAR = 2024  # 面板 app_year 窗口上限
K = 3             # 主窗口 2021→2024


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def chain_names():
    t = load("chain_tree_20261021.json")
    return {r["industry_code"]: r["industry_name"] for r in t if len(r["industry_code"]) == 7}


def bridge_index(br):
    """企业名 → [(chain, city, weight)]；底册同名多主体按 1/k 计权（§3.5 的 47 个重名）。"""
    by_name = {}
    for b in br:
        by_name.setdefault(b["nm"], []).append(b)
    out = {}
    for nm, rows in by_name.items():
        w = 1.0 / len(rows)
        pairs = []
        for r in rows:
            for ch in r["chains"]:
                pairs.append((ch, r["c"], w))
        out[nm] = pairs
    return out


def main():
    t0 = time.time()
    panel = load("patent_panel_innov_20261021.json")
    br = load("bridge_20261021.json")
    cn = chain_names()
    idx = bridge_index(br)

    # ---- 链 × 城 × 年 件数（专利一经第一申请人归链、归城）
    cells = {}
    cells_stable = {}
    matched = 0
    years_seen = set()
    per_name = {}
    for key, n in panel["app_year"].items():
        y, _, nm = key.partition("|")
        pairs = idx.get(nm)
        if not pairs:
            continue
        per_name.setdefault(nm, {})[y] = n
    # 稳定队列：四个年度都有 >=1 件的申请人（剔除「更名/主体迁移」造成的整段断裂）
    stable = {nm for nm, ys in per_name.items() if all(ys.get(str(y)) for y in range(2021, 2025))}
    for key, n in panel["app_year"].items():
        y, _, nm = key.partition("|")
        pairs = idx.get(nm)
        if not pairs:
            continue
        matched += n
        years_seen.add(int(y))
        for ch, city, w in pairs:
            c = cells.setdefault((ch, city), {})
            c[y] = c.get(y, 0.0) + n * w
            if nm in stable:
                s = cells_stable.setdefault((ch, city), {})
                s[y] = s.get(y, 0.0) + n * w

    # ---- 评分
    def cagr(p0, p1, k):
        if p0 <= 0:
            return None
        return (p1 / p0) ** (1.0 / k) - 1.0

    def score_cell(p):
        g = cagr(p[STAT_YEAR - K], p[STAT_YEAR], K)
        # 上期增速：2018—2020 零行，只能取 t-1 的 k=2 年化值（2021→2023）
        g_prev = cagr(p[2021], p[2023], 2)
        if p[STAT_YEAR] <= 0 and p[STAT_YEAR - K] <= 0:
            return "无公开", 0.0, g, g_prev
        if p[STAT_YEAR - K] <= 0 and p[STAT_YEAR] > 0:
            return "萌芽", 25.0, g, g_prev
        if g is not None and g > THETA:
            if g_prev is not None and g < g_prev:
                return "趋于成熟", 70.0, g, g_prev
            return "成长", 50.0, g, g_prev
        if g is not None and abs(g) <= THETA:
            return "成熟", 90.0, g, g_prev
        if g is not None and g < -THETA:
            s = round(min(90.0, max(0.0, 90.0 * p[STAT_YEAR] / p[STAT_YEAR - K])), 2)
            return "衰退", s, g, g_prev
        return "无公开", 0.0, g, g_prev

    rows = []
    for (ch, city), ys in sorted(cells.items()):
        p = {y: ys.get(str(y), 0.0) for y in range(2021, 2025)}
        stage, score, g, g_prev = score_cell(p)
        ys2 = cells_stable.get((ch, city), {})
        p2 = {y: ys2.get(str(y), 0.0) for y in range(2021, 2025)}
        stage2, score2, g2, _ = score_cell(p2)
        alt = cagr(p[2022], p[2024], 2)
        rows.append({
            "chain": ch, "chain_name": cn.get(ch, ch), "city": city,
            "P": {str(y): round(p[y], 2) for y in range(2021, 2025)},
            "g_3y": None if g is None else round(g, 6),
            "g_prev_2y": None if g_prev is None else round(g_prev, 6),
            "g_alt_2y": None if alt is None else round(alt, 6),
            "stage": stage, "score": score,
            "stable_P": {str(y): round(p2[y], 2) for y in range(2021, 2025)},
            "stable_g": None if g2 is None else round(g2, 6),
            "stable_stage": stage2, "stable_score": score2,
            "is_city4": city in CITY4,
        })

    c4 = [r for r in rows if r["is_city4"]]
    outside = [r for r in rows if not r["is_city4"]]
    scores = [r["score"] for r in c4]
    stage_dist = {}
    for r in c4:
        stage_dist[r["stage"]] = stage_dist.get(r["stage"], 0) + 1
    stage_dist_stable = {}
    for r in c4:
        stage_dist_stable[r["stable_stage"]] = stage_dist_stable.get(r["stable_stage"], 0) + 1

    chain_tot, city_tot = {}, {}
    for r in c4:
        chain_tot[r["chain_name"]] = chain_tot.get(r["chain_name"], 0) + sum(r["P"].values())
        city_tot[r["city"]] = city_tot.get(r["city"], 0) + sum(r["P"].values())

    by_city_score = {}
    for r in c4:
        by_city_score.setdefault(r["city"], []).append({"chain": r["chain_name"], "score": r["score"],
                                                        "stage": r["stage"]})

    payload = {
        "metric_id": METRIC,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_sec": round(time.time() - t0, 2),
        "support_judgment": "部分支持",
        "params": {"theta": THETA, "stat_year": STAT_YEAR, "k": K,
                   "time_axis": "apdt_year（申请年，代公开年）",
                   "window": [STAT_YEAR - K, STAT_YEAR]},
        "coverage": {
            "panel_rows": panel["rows"],
            "panel_years_available": sorted(years_seen),
            "app_year_window": panel.get("window"),
            "bridge_firms": len(br),
            "bridge_names": len(idx),
            "matched_names": len(per_name),
            "stable_cohort_names": len(stable),
            "stable_cohort_pct": round(len(stable) / len(per_name), 4),
            "patents_matched": matched,
            "matched_pct": round(matched / panel["rows"], 4),
            "cells_city4": len(c4), "cells_outside_city4": len(outside),
            "chains_seen": len({r["chain"] for r in c4}),
            "cities_seen": len({r["city"] for r in c4}),
        },
        "stats": {
            "n": len(scores), "min": min(scores), "max": max(scores),
            "mean": round(sum(scores) / len(scores), 2),
            "n_zero": sum(1 for s in scores if s == 0),
            "n_distinct": len({round(s, 4) for s in scores}),
            "median": round(sorted(scores)[len(scores) // 2], 2),
        },
        "stats_stable": {
            "n": len(c4),
            "mean": round(sum(r["stable_score"] for r in c4) / len(c4), 2),
            "n_distinct": len({round(r["stable_score"], 4) for r in c4}),
            "n_stage_changed": sum(1 for r in c4 if r["stage"] != r["stable_stage"]),
        },
        "stage_dist": stage_dist,
        "stage_dist_stable": stage_dist_stable,
        "chain_totals": dict(sorted(chain_tot.items(), key=lambda kv: -kv[1])),
        "city_totals": dict(sorted(city_tot.items(), key=lambda kv: -kv[1])),
        "by_city_score": {k: sorted(v, key=lambda x: -x["score"]) for k, v in by_city_score.items()},
        "cells": sorted(rows, key=lambda r: (r["city"], r["chain"])),
        "notes": [
            "时间轴为申请年 apdt_year（面板窗口 2021—2024），源表 pbdt_year 存在但无缓存，取它需全表扫，禁。",
            "dwd_patent 2017—2020 零行：上期增速 g_prev 只能取 2021→2023 的 k=2 年化值，与主窗口 k=3 不等长。",
            "统计年止于 2024：面板 app_year 不含 2025/2026，故无法出 2025 年值。",
            "链上企业 = 228 万行标签中 credit_code 可落主档的 35,046 家；专利按第一申请人名匹配。",
            "底册 47 个重名按 1/k 计权；同一专利若企业属多条链会在多个格子各计一次，"
            "故 48 格件数之和（3,008,860）约为唯一匹配专利（%d）的 %.2f 倍，不可与面板行数对账。"
            % (matched, sum(chain_tot.values()) / matched),
            "稳定队列（四年度均有件的 %d 名，占 %.1f%%）用于剥离更名/主体迁移造成的序列断裂；"
            "两套结果并列输出，stage_changed 计数见 stats_stable。" % (len(stable), 100.0 * len(stable) / len(per_name)),
        ],
    }
    out = BASE / f"{METRIC}_out.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: payload[k] for k in ("support_judgment", "coverage", "stats", "stage_dist")},
                     ensure_ascii=False, indent=1))
    print("cells", len(rows), "-> written", out.name)


if __name__ == "__main__":
    main()
