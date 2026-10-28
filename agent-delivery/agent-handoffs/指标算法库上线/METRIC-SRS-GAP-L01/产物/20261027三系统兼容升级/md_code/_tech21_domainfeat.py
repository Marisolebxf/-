#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TECH 成熟度/阶段/潜力三件共用的「域特征层」（20261022 批，零 SQL）。

口径固定：
  - 域 = IPC 主分类前 4 位；窗口 2021—2024；样本门槛 n2024 >= 100；
  - 只统计深圳市申请人（`sz_patent_city_name_gkx.json` 的 77,846 个名称）；
  - 授权数按「申请人域内件数 / 该申请人全期件数 × 该申请人全期授权数」分摊；
  - 发明件数同法分摊；HHI 用域内申请人件数份额；
  - 全国件数不进入本层任何字段（只在 LQ 维另行取用）。
"""
from __future__ import annotations

import collections
import math

import _tech21_scope as sc
from _tech21_common import IPC_LABEL

YEARS = [2021, 2022, 2023, 2024]
NEW_CODES = {"H10B", "H10D", "H10F", "H10H", "H10K", "H10N", "H10P", "H10W"}
WEIGHTS = {"size": 0.25, "grant": 0.25, "invention": 0.15, "hhi": 0.15, "stability": 0.20}
LEVEL_CUTS = [30, 42, 50, 58]


def clamp(x):
    return max(0.0, min(100.0, x))


def s_size(n):
    return clamp(100 * (math.log(max(n, 1)) - math.log(100)) / (math.log(10000) - math.log(100)))


def s_grant(g):
    return clamp(100 * (g - 0.50) / (0.90 - 0.50))


def s_invention(v):
    return clamp(100 * (v - 0.15) / (0.70 - 0.15))


def s_hhi(h):
    return clamp(100 * (math.log(max(h, 1)) - math.log(50)) / (math.log(1000) - math.log(50)))


def s_stability(g):
    return clamp(100 * (1 - min(abs(g), 0.50) / 0.50))


def level_of(score):
    if score < LEVEL_CUTS[0]:
        return "L1"
    if score < LEVEL_CUTS[1]:
        return "L2"
    if score < LEVEL_CUTS[2]:
        return "L3"
    if score < LEVEL_CUTS[3]:
        return "L4"
    return "L5"


def build():
    """返回 (features, meta)。features 按 2024 件数降序。"""
    cell, sz_year = sc.load_sz_ipc()
    panel = {d: {y: int(cell.get((d, y), 0)) for y in YEARS} for d in {d for d, _ in cell}}
    qualified = sorted([d for d, v in panel.items() if v[2024] >= 100])

    ipc_name = sc.load_ipc_name()
    sz_groups = sc.load_sz_groups()
    sz_meta = {g["nm"]: g for g in sz_groups}
    agg, agg_meta = sc.load_star_agg()

    dom_apps = collections.defaultdict(dict)
    for ipc4, nm, n in ipc_name:
        if nm in sz_meta:
            dom_apps[ipc4][nm] = dom_apps[ipc4].get(nm, 0) + int(n)

    feats = []
    for d in qualified:
        apps = dom_apps.get(d, {})
        total = sum(apps.values())
        grants = inv = 0.0
        for nm, c in apps.items():
            a = agg.get(nm)
            if not a or not a[0]:
                continue
            share = c / a[0]
            grants += share * a[1]
            inv += share * sz_meta[nm].get("invention", 0)
        v = panel[d]
        grant_ratio = grants / total if total else 0.0
        inv_share = inv / total if total else 0.0
        hhi = sum((c / total) ** 2 for c in apps.values()) * 10000 if total else 0.0
        g_total = (v[2024] - v[2021]) / v[2021] if v[2021] else None
        g_near = (v[2024] - v[2023]) / v[2023] if v[2023] else None
        parts = {
            "size": s_size(v[2024]), "grant": s_grant(grant_ratio),
            "invention": s_invention(inv_share), "hhi": s_hhi(hhi),
            "stability": s_stability(g_near or 0.0),
        }
        score = sum(parts[k] * WEIGHTS[k] for k in WEIGHTS)
        feats.append({
            "ipc4": d, "label": IPC_LABEL.get(d, ""), "n": [v[y] for y in YEARS],
            "n2024": v[2024],
            "g_total": None if g_total is None else round(g_total, 4),
            "g_near": None if g_near is None else round(g_near, 4),
            "grant_ratio": round(grant_ratio, 4),
            "grants_alloc": round(grants, 1),
            "invention_share": round(inv_share, 4),
            "hhi": round(hhi, 1),
            "applicants": len(apps),
            "patents_in_scope": total,
            "maturity_parts": {k: round(p, 1) for k, p in parts.items()},
            "maturity_score": round(score, 2),
            "maturity_level": level_of(score),
            "new_code": d in NEW_CODES,
        })
    feats.sort(key=lambda r: -r["n2024"])
    meta = {
        "sz_domains_all": len(panel),
        "qualified": len(feats),
        "sz_total_2024": sum(v[2024] for v in panel.values()),
        "qualified_total_2024": sum(f["n2024"] for f in feats),
        "sz_applicants": len(sz_meta),
        "agg_table_rows": agg_meta.get("table_rows"),
        "agg_names": agg_meta.get("names"),
        "ipc_by_name_rows": len(ipc_name),
        "sz_year_total": {str(y): sz_year[y] for y in YEARS},
    }
    return feats, meta
