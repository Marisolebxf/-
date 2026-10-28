#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_DOMAIN_COVERAGE_BREADTH · 技术领域覆盖广度（gkx 单库转换版）

定义
----
企业技术领域覆盖广度 = 该企业专利所落入的 IPC4 小类数（distinct）。
它衡量「一家企业的技术活动横跨多少个技术领域」，不是专利数量，也不是质量。
口径取 IPC 前 4 位（如 H05K、G06F），与旧稿一致。

为什么判「完全转换支持」
------------------------
`industry_cluster` 结果面在 gkx 不存在（source_absent，见 TABLE_ABSENCE_EVIDENCE
§industry_cluster），但本指标不需要任何结果面：`dwd_patent.main_classification_ipcr`
直接给出每条专利的 IPC，按申请人名 + IPC4 去重计数即可。库内 581,585 条
（企业×IPC4）覆盖 134,152 个申请人、634 个 IPC4 小类，量足以支撑分布、排名与分档。

输出：code/M_ENT_DOMAIN_COVERAGE_BREADTH_out.json
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_ENT_DOMAIN_COVERAGE_BREADTH_out.json"
METRIC = "M_ENT_DOMAIN_COVERAGE_BREADTH"


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def pct(sorted_vals, q):
    if not sorted_vals:
        return None
    i = min(len(sorted_vals) - 1, max(0, int(round(q * (len(sorted_vals) - 1)))))
    return sorted_vals[i]


def main() -> None:
    ipc_by_name = defaultdict(set)
    pat_by_name = defaultdict(int)
    for ipc4, name, c in load("patent_ipc4_by_name_20261021.json"):
        ipc_by_name[name].add(ipc4)
        pat_by_name[name] += c

    city_of = load("org_name_city_20261021.json")["map"]
    breadth = {n: len(s) for n, s in ipc_by_name.items()}
    vals = sorted(breadth.values())

    def band(b):
        if b >= 100:
            return "A >=100"
        if b >= 50:
            return "B 50-99"
        if b >= 20:
            return "C 20-49"
        if b >= 10:
            return "D 10-19"
        if b >= 5:
            return "E 5-9"
        return "F 1-4"

    dist = defaultdict(int)
    for b in vals:
        dist[band(b)] += 1

    city_breadth = defaultdict(list)
    for n, b in breadth.items():
        c = city_of.get(n)
        if c:
            city_breadth[c].append(b)

    top = sorted(breadth.items(), key=lambda x: (-x[1], -pat_by_name[x[0]]))[:50]
    rows = [{"name": n, "ipc4_breadth": b, "patents": pat_by_name[n],
             "patents_per_field": round(pat_by_name[n] / b, 2),
             "city": city_of.get(n)} for n, b in top]

    city_rows = []
    for c, arr in sorted(city_breadth.items(), key=lambda x: -len(x[1]))[:8]:
        arr_sorted = sorted(arr)
        city_rows.append({"city": c, "orgs_with_patent": len(arr),
                          "mean_breadth": round(sum(arr) / len(arr), 2),
                          "median_breadth": pct(arr_sorted, 0.5),
                          "p90_breadth": pct(arr_sorted, 0.9)})

    total_orgs = len(breadth)
    out = {
        "metric_id": METRIC,
        "metric_name": "技术领域覆盖广度",
        "data_source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）+ code/_snapshots21/ 落盘快照",
        "formula": "breadth_i = COUNT(DISTINCT substr(ipc,1,4)) BY 申请人；附带 patents_per_field = 专利数 / breadth",
        "blocking_tables": {
            "industry_cluster": {
                "triage": "source_absent",
                "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §industry_cluster",
            }
        },
        "conversion_path": "dwd_patent.main_classification_ipcr → IPC4 → 按申请人去重计数；无结果面依赖",
        "coverage": {
            "orgs_with_patent": total_orgs,
            "distinct_ipc4": len({i for s in ipc_by_name.values() for i in s}),
            "patent_rows_scanned": 2939895,
            "ipc4_name_rows": 581585,
        },
        "distribution": {
            "min": vals[0] if vals else None,
            "p25": pct(vals, 0.25), "median": pct(vals, 0.5),
            "p75": pct(vals, 0.75), "p90": pct(vals, 0.9),
            "p99": pct(vals, 0.99), "max": vals[-1] if vals else None,
            "mean": round(sum(vals) / len(vals), 2) if vals else None,
        },
        "bands": dict(sorted(dist.items())),
        "cities": city_rows,
        "top50": rows,
        "support_judgment": {
            "data_support_level": "完全转换支持",
            "reason": "本指标不依赖任何缺失的结果面：dwd_patent 的 main_classification_ipcr 直接给出每条专利的 IPC，取前 4 位后按申请人去重计数即得覆盖广度。库内 2,939,895 条专利、581,585 条企业×IPC4 记录、134,152 个申请人、634 个 IPC4 小类，分布从 1 到 100+ 完整可算，排名、分档、城市均值都能直接产出，无需代理、无需补数。",
            "criteria": {
                "result_table_needed": False,
                "source_table_exists": True,
                "orgs_covered": total_orgs,
                "ipc4_covered": len({i for s in ipc_by_name.values() for i in s}),
                "proxy_used": False,
            },
        },
        "base_years_used": [2021, 2022, 2023, 2024],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": "专利表 apdt_year 只有 2021—2026（2017—2020 零行，DATA_FACTS 陷阱 3.13），本件按全期去重计广度，不按年切分；2025/2026 为不完整年，若做年度增量需单列。广度是存量口径，年份窗口只影响「哪些专利被纳入」，不影响字段语义。",
        "sources": [
            {"path": "code/_snapshots21/patent_ipc4_by_name_20261021.json",
             "table": "gkx.dwd_patent", "rows": 581585,
             "role": "企业×IPC4 计数（唯一输入）"},
            {"path": "code/_snapshots21/org_name_city_20261021.json",
             "table": "gkx.dwd_org_base_info", "rows": 189068,
             "role": "企业名→城市（城市均值用）"},
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[OK] {METRIC} -> {OUT.name} orgs={total_orgs} "
          f"median={out['distribution']['median']} max={out['distribution']['max']}")
    print("  bands", out["bands"])
    for r in rows[:5]:
        print("  top", r["name"][:18], r["ipc4_breadth"], r["patents"])


if __name__ == "__main__":
    main()
