#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_TECH_POWER_SCORE · 企业技术力评分（gkx 单库代理版）

旧稿口径
--------
企业技术力 = 0.5×专利规模 + 0.3×技术领域广度 + 0.2×技术新鲜度，各维 min-max 归一到 0—1。
  D1 专利规模：log1p(专利数)
  D2 广度：IPC4 distinct 数
  D3 新鲜度：2024 年申请量 / 全期申请量

数据事实
--------
`tech_power` 与 `enterprise_score` 两张结果面在 gkx 都不存在（均 source_absent，
见 TABLE_ABSENCE_EVIDENCE 对应两节）。可用的只有专利侧：
`dwd_patent` 按申请人聚合的 581,585 条企业×IPC4 与 60,009 条 2024 申请/授权。
旧稿里「人才、成果转化、研发投入」三维在 gkx 没有任何可挂到企业个体的表，
本件不造这三项，只出专利三维分，并明确标注为「专利技术力」而非完整技术力。

输出：code/M_ENT_TECH_POWER_SCORE_out.json
"""
from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_ENT_TECH_POWER_SCORE_out.json"
METRIC = "M_ENT_TECH_POWER_SCORE"


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def main() -> None:
    ipc = defaultdict(set)
    pat = defaultdict(int)
    for ipc4, name, c in load("patent_ipc4_by_name_20261021.json"):
        ipc[name].add(ipc4)
        pat[name] += c
    apply24 = {n: int(v[0]) for n, v in load("patent_2024_by_name_20261021.json").items()
               if isinstance(v, list) and v}

    names = [n for n in ipc if pat[n] >= 1]
    logs = {n: math.log1p(pat[n]) for n in names}
    brd = {n: len(ipc[n]) for n in names}
    rec = {n: (apply24.get(n, 0) / pat[n] if pat[n] else 0.0) for n in names}

    def norm(d):
        lo, hi = min(d.values()), max(d.values())
        span = (hi - lo) or 1.0
        return {k: (v - lo) / span for k, v in d.items()}

    n1, n2, n3 = norm(logs), norm(brd), norm(rec)
    score = {n: 0.5 * n1[n] + 0.3 * n2[n] + 0.2 * n3[n] for n in names}

    city_of = load("org_name_city_20261021.json")["map"]
    top = sorted(score.items(), key=lambda x: -x[1])[:100]
    rows = [{"rank": i, "name": n, "score": round(s, 4), "patents": pat[n],
             "ipc4_breadth": brd[n], "recency_2024": round(rec[n], 4),
             "city": city_of.get(n)}
            for i, (n, s) in enumerate(top, 1)]

    vals = sorted(score.values())
    def pct(q):
        return round(vals[min(len(vals) - 1, int(q * (len(vals) - 1)))], 4)

    city_scores = defaultdict(list)
    for n, s in score.items():
        c = city_of.get(n)
        if c:
            city_scores[c].append(s)
    city_rows = [{"city": c, "orgs": len(a), "mean_score": round(sum(a) / len(a), 4),
                  "max_score": round(max(a), 4)}
                 for c, a in sorted(city_scores.items(), key=lambda x: -len(x[1]))[:8]]

    out = {
        "metric_id": METRIC,
        "metric_name": "企业技术力评分",
        "data_source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）+ code/_snapshots21/ 落盘快照",
        "formula": "score = 0.5*minmax(log1p(专利数)) + 0.3*minmax(IPC4广度) + 0.2*minmax(2024申请占比)",
        "blocking_tables": {
            "tech_power": {"triage": "source_absent",
                           "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §tech_power"},
            "enterprise_score": {"triage": "source_absent",
                                 "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §enterprise_score"},
        },
        "proxy_path": "dwd_patent 三维（规模/广度/新鲜度）→ 0.5/0.3/0.2 加权",
        "proxy_deviation": "旧稿技术力含「人才、成果转化、研发投入」三维，gkx 无企业级载体，本件只出专利三维，是有偏的：研发投入大但专利少的企业会被低估，代工型专利多的企业会被高估；权重 0.5/0.3/0.2 为项目默认值",
        "coverage": {"orgs_scored": len(names), "orgs_total_base": 189116,
                     "ipc4_name_rows": 581585, "weight": {"d1": 0.5, "d2": 0.3, "d3": 0.2}},
        "distribution": {"p25": pct(0.25), "median": pct(0.5), "p75": pct(0.75),
                         "p90": pct(0.9), "p99": pct(0.99), "max": pct(1.0)},
        "cities": city_rows,
        "top100": rows,
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": "两张结果面（tech_power、enterprise_score）都不存在，旧稿六维里只有专利侧三维能从 dwd_patent 逐企业算出，人才/转化/投入三维在 gkx 没有任何企业级表可挂。专利三维本身结构与量都够（134,152 家企业有专利），可产出完整分布与排名；缺三维意味着分值是「专利技术力」而不是「技术力」，故判部分支持而不是完全转换支持。",
            "criteria": {
                "result_tables": 2, "result_tables_present": 0,
                "dims_total": 6, "dims_computable": 3,
                "orgs_scored": len(names), "proxy_used": True,
            },
        },
        "base_years_used": [2021, 2022, 2023, 2024],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": "专利表只有 2021—2026（2017—2020 零行），D1 分母是全期申请，D3 用 2024 年申请占比；2025/2026 为残年不入分子。人才/转化维不涉及年份，因整维缺失而不存在基期。",
        "sources": [
            {"path": "code/_snapshots21/patent_ipc4_by_name_20261021.json",
             "table": "gkx.dwd_patent", "rows": 581585,
             "role": "企业×IPC4 计数（D1/D2）"},
            {"path": "code/_snapshots21/patent_2024_by_name_20261021.json",
             "table": "gkx.dwd_patent", "rows": 60009,
             "role": "2024 申请量（D3）"},
            {"path": "code/_snapshots21/org_name_city_20261021.json",
             "table": "gkx.dwd_org_base_info", "rows": 189068,
             "role": "企业名→城市"},
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[OK] {METRIC} -> {OUT.name} scored={len(names)} median={out['distribution']['median']}")
    for r in rows[:5]:
        print("  ", r["rank"], r["name"][:20], r["score"], r["patents"], r["ipc4_breadth"])


if __name__ == "__main__":
    main()
