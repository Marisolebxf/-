#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_CITY_AVG_TECH_POWER · 城市平均技术力（gkx 单库代理版）

定义
----
城市平均技术力 = 该城市所有「有专利企业」的技术力分值均值。
分值口径与 M_ENT_TECH_POWER_SCORE 一致：0.5×专利规模 + 0.3×IPC4 广度 + 0.2×2024 新鲜度，
各维在城市集合内 min-max 归一前的企业级归一。

数据事实
--------
`tech_power` 结果面在 gkx 不存在（source_absent，见 TABLE_ABSENCE_EVIDENCE §tech_power）。
可用：`dwd_patent` 企业×IPC4 计数（581,585 行）+ `dwd_org_base_info` 企业城市（189,116 行）。
分母是「有专利企业数」，不是「全部企业数」——这是本件最重要的口径披露：
把无专利企业按 0 摊进均值会把城市均值压成「专利覆盖率」，与「平均技术力」不是同一个量。

输出：code/M_ENT_CITY_AVG_TECH_POWER_out.json
"""
from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_ENT_CITY_AVG_TECH_POWER_out.json"
METRIC = "M_ENT_CITY_AVG_TECH_POWER"


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def main() -> None:
    base = load("base_20261021.json")  # [org_id, credit, name, province, city, est_year]
    city_of = {r[2]: r[4] for r in base}
    est_of = {r[2]: r[5] for r in base}

    ipc = defaultdict(set)
    pat = defaultdict(int)
    for ipc4, name, c in load("patent_ipc4_by_name_20261021.json"):
        ipc[name].add(ipc4)
        pat[name] += c
    apply24 = {n: int(v[0]) for n, v in load("patent_2024_by_name_20261021.json").items()
               if isinstance(v, list) and v}

    names = [n for n in ipc if pat[n] > 0]
    logs = {n: math.log1p(pat[n]) for n in names}
    brd = {n: len(ipc[n]) for n in names}
    rec = {n: apply24.get(n, 0) / pat[n] for n in names}

    def norm(d):
        lo, hi = min(d.values()), max(d.values())
        span = (hi - lo) or 1.0
        return {k: (v - lo) / span for k, v in d.items()}

    n1, n2, n3 = norm(logs), norm(brd), norm(rec)
    score = {n: 0.5 * n1[n] + 0.3 * n2[n] + 0.2 * n3[n] for n in names}

    city_scores = defaultdict(list)
    city_pat = defaultdict(int)
    for n, s in score.items():
        c = city_of.get(n)
        if c:
            city_scores[c].append(s)
            city_pat[c] += pat[n]

    base_by_city = defaultdict(int)
    for r in base:
        base_by_city[r[4]] += 1

    rows = []
    for c, arr in city_scores.items():
        arr_s = sorted(arr)
        rows.append({
            "city": c, "orgs_with_patent": len(arr),
            "orgs_total": base_by_city.get(c, 0),
            "patent_coverage": round(len(arr) / base_by_city[c], 4) if base_by_city.get(c) else None,
            "patents_total": city_pat[c],
            "mean_tech_power": round(sum(arr) / len(arr), 4),
            "median_tech_power": round(arr_s[len(arr_s) // 2], 4),
            "p90_tech_power": round(arr_s[int(0.9 * (len(arr_s) - 1))], 4),
        })
    all_rows = sorted(rows, key=lambda r: -r["mean_tech_power"])
    # 只给「有专利企业 >=100 家」的城市排名：n=1 的城市均值是单点噪声，
    # 排进去会让「城市平均技术力」变成小样本抽奖。
    rows = [r for r in all_rows if r["orgs_with_patent"] >= 100]
    rows.sort(key=lambda r: -r["mean_tech_power"])
    for i, r in enumerate(rows, 1):
        r["rank"] = i

    out = {
        "metric_id": METRIC,
        "metric_name": "城市平均技术力",
        "data_source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）+ code/_snapshots21/ 落盘快照",
        "formula": "city_avg = AVG(0.5*专利规模 + 0.3*IPC4广度 + 0.2*新鲜度) OVER 该市有专利企业",
        "blocking_tables": {
            "tech_power": {"triage": "source_absent",
                           "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §tech_power"},
        },
        "proxy_path": "企业级专利三维分 → 按 city 求均值",
        "proxy_deviation": "均值分母是「有专利企业」而非全部企业：深圳 95,600 家企业里有专利的只是一部分，把无专利企业当 0 会把均值变成覆盖率；人才/转化/投入三维缺失，分值是专利技术力",
        "denominator_note": "分母 = 该市有专利企业数；orgs_total 与 patent_coverage 一并给出，便于读者判断均值代表多少企业",
        "min_orgs_for_rank": 100,
        "cities": rows,
        "small_cities_excluded": [{"city": r["city"], "orgs_with_patent": r["orgs_with_patent"],
                                   "mean_tech_power": r["mean_tech_power"]}
                                  for r in all_rows if r["orgs_with_patent"] < 100][:12],
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": "tech_power 结果面不存在，但城市平均量可由企业级专利三维分聚合得到：专利计数、IPC4 广度、2024 申请量都在 dwd_patent 里，企业城市在 dwd_org_base_info 里，聚合链完整。缺的是技术力的另外三维（人才/转化/投入）与「全部企业」分母口径，故判部分支持。",
            "criteria": {
                "result_table_exists": False,
                "cities_computed": len(rows), "min_orgs_for_rank": 100,
                "dims_used": 3, "dims_missing": 3,
                "proxy_used": True,
            },
        },
        "base_years_used": [2021, 2022, 2023, 2024],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": "专利表只有 2021—2026（2017—2020 零行），D1 分母为全期申请，D3 用 2024 年占比；2025/2026 残年不入分子。本件是截面均值，不做年度序列，故不列逐年基期。",
        "sources": [
            {"path": "code/_snapshots21/patent_ipc4_by_name_20261021.json",
             "table": "gkx.dwd_patent", "rows": 581585, "role": "企业专利三维输入"},
            {"path": "code/_snapshots21/patent_2024_by_name_20261021.json",
             "table": "gkx.dwd_patent", "rows": 60009, "role": "2024 申请量"},
            {"path": "code/_snapshots21/base_20261021.json",
             "table": "gkx.dwd_org_base_info", "rows": 189116, "role": "企业→城市"},
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[OK] {METRIC} -> {OUT.name} cities={len(rows)}")
    for r in rows[:6]:
        print(f"  #{r['rank']} {r['city']:<6} n={r['orgs_with_patent']:<6} "
              f"cov={r['patent_coverage']} mean={r['mean_tech_power']}")


if __name__ == "__main__":
    main()
