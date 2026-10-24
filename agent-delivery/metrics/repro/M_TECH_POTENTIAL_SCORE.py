#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TECH_POTENTIAL_SCORE —— 技术产业化潜力评分（0—100，深圳口径）。

五维（权重合计 1.00）：
  规模 20%    n2024 对数刻度（100 件=0，10,000 件=100）
  增长 30%    g(2021→2024) 线性映射：0%=50 分，+50%=100 分，-50%=0 分
  份额 25%    LQ(2024)=深圳占比÷全国占比，LQ=1 记 50 分，LQ>=2 记 100 分
  质量 15%    分摊发明占比（0.15=0，0.70=100）——不用授权比，避免被未决申请稀释
  转化 10%    深圳「有转让记录主体」在该域 2024 件数中的占比，log 压缩（0.60 记满）

口径声明（单一分母）：
  - 规模/增长/质量/转化四维的分母都是**深圳**：域件数、深圳申请人口径；
  - 份额维的分母是**全国**：LQ 的分子是深圳件数、分母是全国同域件数，
    全国只在该维出现，且单独列表，不与深圳件数相加；
  - 转化维是「主体级代理」：`dwd_patent_transfer` 无 IPC 字段、pn 与专利面板不同码域，
    无法把转让记录落到域，只能用「有转让记录的深圳主体」的专利份额作代理。

零 SQL：专利读缓存，转让读 `gba_transfer_rows_20261021.json`（全量 22,809 行）。
"""
from __future__ import annotations

import collections
import math
import statistics

import _tech21_scope as sc
import _tech21_domainfeat as feat

METRIC = "M_TECH_POTENTIAL_SCORE"
YEARS = feat.YEARS
W = {"size": 0.20, "growth": 0.30, "lq": 0.25, "quality": 0.15, "transfer": 0.10}
QUALITY_FIELD = "invention_share"


def clamp(x):
    return max(0.0, min(100.0, x))


def s_growth(g):
    if g is None:
        return 50.0
    return clamp(50 + 100 * g)


def s_lq(lq):
    if lq is None:
        return 50.0
    return clamp(50 * lq)


def s_transfer(cov):
    return clamp(100 * math.log1p(max(cov, 0.0)) / math.log1p(0.60))


def main():
    rows, meta = feat.build()
    nat_cell, nat_year = sc.load_nat_ipc()
    sz_year = {int(k): v for k, v in meta["sz_year_total"].items()}

    # 深圳转让活跃主体（转让人或受让人名称命中深圳申请人名单）
    transfers = sc._load(sc.SNAP / "gba_transfer_rows_20261021.json")
    party_names = set()
    for r in transfers:
        for nm in (r.get("before") or []) + (r.get("after") or []):
            party_names.add(nm)
    sz_names = {g["nm"] for g in sc.load_sz_groups()}
    active = party_names & sz_names
    year_count = collections.Counter(str(r.get("date"))[:4] for r in transfers)

    ipc_name = sc.load_ipc_name()
    dom_apps = collections.defaultdict(dict)
    for ipc4, nm, n in ipc_name:
        if nm in sz_names:
            dom_apps[ipc4][nm] = dom_apps[ipc4].get(nm, 0) + int(n)

    out = []
    for r in rows:
        d = r["ipc4"]
        lq = None
        if nat_cell.get((d, 2024)):
            lq = (r["n2024"] / sz_year[2024]) / (nat_cell[(d, 2024)] / nat_year[2024])
        apps = dom_apps.get(d, {})
        tot = sum(apps.values())
        act = sum(c for nm, c in apps.items() if nm in active)
        cov = act / tot if tot else 0.0
        parts = {
            "size": feat.s_size(r["n2024"]),
            "growth": s_growth(r["g_total"]),
            "lq": s_lq(lq),
            "quality": feat.s_invention(r["invention_share"]),
            "transfer": s_transfer(cov),
        }
        score = sum(parts[k] * W[k] for k in W)
        out.append({
            "ipc4": d, "label": r["label"], "n": r["n"], "n2024": r["n2024"],
            "g_total": r["g_total"], "g_near": r["g_near"],
            "lq_2024": None if lq is None else round(lq, 4),
            "grant_ratio": r["grant_ratio"],
            "invention_share": r["invention_share"],
            "transfer_coverage": round(cov, 4),
            "score": round(score, 2),
            "parts": {k: round(v, 1) for k, v in parts.items()},
            "new_code": r["new_code"],
        })
    out.sort(key=lambda r: -r["score"])

    scores = [r["score"] for r in out]
    dist = {
        "min": round(min(scores), 2), "max": round(max(scores), 2),
        "mean": round(statistics.mean(scores), 2), "median": round(statistics.median(scores), 2),
        "quartiles": [round(x, 2) for x in statistics.quantiles(scores, n=4)],
        "ge70": sum(1 for x in scores if x >= 70),
        "60_70": sum(1 for x in scores if 60 <= x < 70),
        "50_60": sum(1 for x in scores if 50 <= x < 60),
        "lt50": sum(1 for x in scores if x < 50),
    }

    # 产业聚合（20+8 映射，未覆盖单列）
    ind = collections.defaultdict(lambda: {"domains": 0, "n2024": 0, "score_sum": 0.0})
    unmapped = {"domains": 0, "n2024": 0, "score_sum": 0.0}
    for r in out:
        k = sc.ipc_industry(r["ipc4"])
        box = ind[k] if k else unmapped
        box["domains"] += 1
        box["n2024"] += r["n2024"]
        box["score_sum"] += r["score"]
    industry = [{"industry": k, "domains": v["domains"], "n2024": v["n2024"],
                 "mean_score": round(v["score_sum"] / v["domains"], 2)}
                for k, v in ind.items()]
    industry.sort(key=lambda x: -x["mean_score"])

    # 新码敏感性：剔除 H10x 后的前 10
    no_new = [r for r in out if not r["new_code"]]

    payload = {
        "metric_id": METRIC,
        "generated_at": "2026-10-22",
        "scope": "深圳（份额维分母为全国）",
        "scope_statement": (
            "四维（规模、增长、质量、转化）的分母都是深圳：深圳域件数、深圳申请人、"
            "深圳转让活跃主体。第五维 LQ 的分母是全国同域件数，全国只出现在这一维，"
            "并在 §2.5 单独成表；全国件数不与深圳件数相加，也不进入其他四维。"
        ),
        "main_db": "gkx @ 183.240.141.251:3318 (gkx_reader_zp, read-only)",
        "sql_count": 0,
        "base_years_used": YEARS,
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": (
            "增长维用 2021→2024 首尾比，基期只能是 2021（2017—2020 零行）；2025/2026 为残年，"
            "不进入分母。缺失年未按 0 摊入任何均值；LQ 只用 2024 单年，不跨年。"
        ),
        "input": {
            "sz_patent": "code/_snapshots21/patent_scan_20261021.pkl",
            "nat_patent": "code/_snapshots21/patent_panel_innov_20261021.json",
            "ipc_by_name": "code/_snapshots21/patent_ipc4_by_name_20261021.json",
            "transfer": "code/_snapshots21/gba_transfer_rows_20261021.json",
        },
        "reused_from": "_tech21_domainfeat.py（域特征层，零 SQL）",
        "weights": W,
        "transfer_meta": {
            "transfer_rows": len(transfers),
            "transfer_years": {str(y): year_count.get(str(y), 0) for y in
                               (2021, 2022, 2023, 2024, 2025, 2026)},
            "party_names": len(party_names),
            "sz_active_parties": len(active),
            "sz_active_share_of_applicants": round(len(active) / len(sz_names), 4),
            "note": ("dwd_patent_transfer 无 IPC 字段，pn 为公开号、专利面板 pn 为内部哈希，"
                     "无法逐件落到 IPC4；本维只能做「主体级」代理"),
        },
        "panel": {
            "qualified_domains": meta["qualified"],
            "sz_total_2024": meta["sz_total_2024"],
            "qualified_total_2024": meta["qualified_total_2024"],
            "nat_total_2024": nat_year[2024],
        },
        "score_distribution": dist,
        "top30": no_new[:30],
        "new_code_watch": [r for r in out if r["new_code"]],
        "bottom10": out[-10:],
        "industry": industry,
        "unmapped": {"domains": unmapped["domains"], "n2024": unmapped["n2024"],
                     "mean_score": round(unmapped["score_sum"] / unmapped["domains"], 2)
                     if unmapped["domains"] else None},
        "top10_excl_new_codes": no_new[:10],
        "rank_note": "主榜（top30）剔除 H10x 新码；新码单列 new_code_watch，不参与主榜排序",
        "domains": out,
        "support_judgment": {
            "data_support_level": "部分支持",
            "structure_support": "部分",
            "data_support": "部分",
            "reason": (
                "专利侧四维与 LQ 可复算，但需求点名的「基础科研（论文）」与「产品市场（销售、"
                "市场调研）」两维缺源：论文表无 IPC/技术域标引，库内无市场销售或市场规模表；"
                "转化维只能用 134 家深圳转让活跃主体作代理，覆盖率中位 4.79%，"
                "单家企业即可把一个域推到 80% 以上。故只能交付「专利侧产业化潜力分」。"
            ),
        },
        "headline": {
            "qualified": len(out),
            "top1": no_new[0]["ipc4"], "top1_score": no_new[0]["score"],
            "top2": no_new[1]["ipc4"], "top2_score": no_new[1]["score"],
            "top3": no_new[2]["ipc4"], "top3_score": no_new[2]["score"],
            "new_code_scored": len([r for r in out if r["new_code"]]),
            "median": dist["median"],
            "sz_active_parties": len(active),
        },
    }
    sc.write_out(METRIC, payload)


if __name__ == "__main__":
    main()
