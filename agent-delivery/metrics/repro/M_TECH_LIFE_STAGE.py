#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TECH_LIFE_STAGE —— 技术生命周期阶段（萌芽 / 成长 / 成熟 / 衰退）。

口径（单一，深圳）：
  - 主体 = 深圳市申请人（`dwd_org_base_info.name_cn` 归属到「深圳市」的 77,846 个名称）；
  - 件数 = 申请年 2021—2024、按 pn 去重、IPC 主分类前 4 位（`patent_scan_20261021.pkl`）；
  - 分母 = 每个 IPC4 域自身的 2021 年与 2023 年件数，不跨城、不跨域；
  - 全国件数只在一张「参照表」里出现（LQ 分母），不进入任何阶段判定。

零 SQL：只读 _snapshots21 / _snapshots_gkx21 授权缓存。
基期：2017—2020 在 dwd_patent 为零行（DATA_FACTS_gkx21 §3.13），只允许 2021 起算。
"""
from __future__ import annotations

import collections
import statistics

import _tech21_scope as sc
from _tech21_common import IPC_LABEL

METRIC = "M_TECH_LIFE_STAGE"
YEARS = [2021, 2022, 2023, 2024]

# 2025.01 版 IPC 新码（半导体族从 H01L 迁入），增长率不可与旧码直接比较
NEW_CODES = {"H10B", "H10D", "H10F", "H10H", "H10K", "H10N", "H10P", "H10W"}


def build_panel():
    cell, _ = sc.load_sz_ipc()
    domains = {d for (d, y) in cell}
    panel = {d: {y: int(cell.get((d, y), 0)) for y in YEARS} for d in domains}
    return panel


def classify(v):
    """四阶段判定（顺序即优先级：萌芽 > 衰退 > 成长 > 成熟）。"""
    n21, n22, n23, n24 = v[2021], v[2022], v[2023], v[2024]
    g_total = (n24 - n21) / n21 if n21 else None
    g_near = (n24 - n23) / n23 if n23 else None
    if g_total is None or g_near is None:
        return "缺基期", g_total, g_near
    if g_total >= 1.00 and n21 < 500 and n24 < 1500:
        return "萌芽", g_total, g_near
    if g_total <= -0.20 or g_near <= -0.20:
        return "衰退", g_total, g_near
    if g_total >= 0.20 and g_near > 0:
        return "成长", g_total, g_near
    return "成熟", g_total, g_near


def main():
    panel = build_panel()
    nat_cell, nat_year = sc.load_nat_ipc()
    sz_year = collections.Counter()
    for d, v in panel.items():
        for y in YEARS:
            sz_year[y] += v[y]

    qualified = sorted([d for d, v in panel.items() if v[2024] >= 100])
    rows = []
    for d in qualified:
        v = panel[d]
        stage, g_total, g_near = classify(v)
        lq = None
        if nat_cell.get((d, 2024)):
            lq = ((v[2024] / sz_year[2024]) /
                  (nat_cell[(d, 2024)] / nat_year[2024]))
        rows.append({
            "ipc4": d, "label": IPC_LABEL.get(d, ""), "n": [v[y] for y in YEARS],
            "g_total": None if g_total is None else round(g_total, 4),
            "g_near": None if g_near is None else round(g_near, 4),
            "stage": stage, "lq_2024": None if lq is None else round(lq, 4),
            "new_code": d in NEW_CODES,
        })

    dist = collections.Counter(r["stage"] for r in rows)
    by_stage = {}
    for st in ("萌芽", "成长", "成熟", "衰退"):
        sub = [r for r in rows if r["stage"] == st]
        lqs = [r["lq_2024"] for r in sub if r["lq_2024"] is not None]
        by_stage[st] = {
            "domains": len(sub),
            "share": round(len(sub) / len(rows), 4),
            "n2024": sum(r["n"][3] for r in sub),
            "n2024_share": round(sum(r["n"][3] for r in sub) / sz_year[2024], 4),
            "lq_median": round(statistics.median(lqs), 4) if lqs else None,
            "new_codes": sorted(r["ipc4"] for r in sub if r["new_code"]),
        }

    def top(key, reverse, k=15):
        pool = [r for r in rows if r[key] is not None]
        pool.sort(key=lambda r: r[key], reverse=reverse)
        return [{"ipc4": r["ipc4"], "label": r["label"], "stage": r["stage"],
                 "n2021": r["n"][0], "n2024": r["n"][3],
                 "g_total": r["g_total"], "g_near": r["g_near"],
                 "lq_2024": r["lq_2024"], "new_code": r["new_code"]}
                for r in pool[:k]]

    # 规模分层 × 阶段交叉
    bands = [(100, 499), (500, 999), (1000, 4999), (5000, 10 ** 9)]
    cross = []
    for lo, hi in bands:
        sub = [r for r in rows if lo <= r["n"][3] <= hi]
        c = collections.Counter(r["stage"] for r in sub)
        cross.append({"band": f"{lo}-{hi if hi < 10**9 else 'max'}", "domains": len(sub),
                      "萌芽": c["萌芽"], "成长": c["成长"], "成熟": c["成熟"], "衰退": c["衰退"]})

    # 新码剔除后的敏感性
    no_new = [r for r in rows if not r["new_code"]]
    new_share = collections.Counter(r["stage"] for r in rows if r["new_code"])
    sens = {
        "all": dict(dist),
        "excl_new_codes": dict(collections.Counter(r["stage"] for r in no_new)),
        "new_code_domains": len([r for r in rows if r["new_code"]]),
        "new_code_stage": dict(new_share),
    }

    # 全国参照（只做 LQ 分母，单独成表）
    nat_ref = {str(y): nat_year[y] for y in YEARS}
    sz_ref = {str(y): sz_year[y] for y in YEARS}

    payload = {
        "metric_id": METRIC,
        "generated_at": "2026-10-22",
        "scope": "深圳",
        "scope_statement": (
            "本件唯一分母是深圳：域件数、阶段判定、规模分层全部只用深圳市申请人的"
            "2021—2024 申请年件数。全国件数只在 §2.6 的 LQ 参照表出现，作 LQ 分母，"
            "不进入任何阶段规则，也不与深圳件数同列相加。"
        ),
        "main_db": "gkx @ 183.240.141.251:3318 (gkx_reader_zp, read-only)",
        "sql_count": 0,
        "base_years_used": YEARS,
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": (
            "dwd_patent.apdt_year 只有 2021—2026，2017—2020 零行；因此基期只能取 2021，"
            "四年窗口为 2021—2024。2025（440,401 件）与 2026（74,810 件）是采集残年，"
            "不进入增长分母；缺失年不按 0 摊入任何均值。"
        ),
        "input": {
            "sz_patent": "code/_snapshots21/patent_scan_20261021.pkl",
            "nat_patent": "code/_snapshots21/patent_panel_innov_20261021.json",
            "sz_applicants": "code/_snapshots_gkx21/sz_patent_city_name_gkx.json",
        },
        "reused_from": "_tech21_scope.py（共用离线取数层，零 SQL）",
        "thresholds": {
            "sample_gate_n2024": 100,
            "sprout": "g_total>=1.00 且 n2021<500 且 n2024<1500",
            "decline": "g_total<=-0.20 或 g_near<=-0.20",
            "growth": "g_total>=0.20 且 g_near>0",
            "mature": "其余",
            "rule_order": "萌芽 > 衰退 > 成长 > 成熟（互斥）",
        },
        "panel": {
            "sz_domains_all": len(panel),
            "sz_domains_2024": len([d for d, v in panel.items() if v[2024] > 0]),
            "qualified_domains": len(rows),
            "sz_year_total": sz_ref,
            "nat_year_total": nat_ref,
        },
        "stage_distribution": by_stage,
        "top_growth": top("g_total", True, 15),
        "top_decline": top("g_total", False, 15),
        "top_near_growth": top("g_near", True, 10),
        "top_near_decline": top("g_near", False, 10),
        "size_band_cross": cross,
        "sensitivity": sens,
        "domains": rows,
        "support_judgment": {
            "data_support_level": "部分支持",
            "structure_support": "部分",
            "data_support": "部分",
            "reason": (
                "四年申请年面板可复算四阶段形态（238 域），但生命周期需要技术替代关系、"
                "法律状态与更长序列；库内 patent 只有主分类、无替代关系，2017—2020 零行，"
                "被引覆盖 0.70%，因此只能交付「申请量形态阶段」，不能交付技术生命周期本体。"
            ),
        },
        "headline": {
            "qualified": len(rows),
            "sprout": dist["萌芽"], "growth": dist["成长"],
            "mature": dist["成熟"], "decline": dist["衰退"],
            "sprout_new_codes": len(by_stage["萌芽"]["new_codes"]),
            "sz_total_2024": sz_year[2024],
            "sz_total_2021": sz_year[2021],
            "sz_change_2021_2024": round((sz_year[2024] - sz_year[2021]) / sz_year[2021], 4),
        },
    }
    sc.write_out(METRIC, payload)


if __name__ == "__main__":
    main()
