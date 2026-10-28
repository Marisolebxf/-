#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_GBA_RES_INDEX · 创新资源指数（湾区 4 城实测）

王惠口径（calc-logic/INNOV/M_INNOV_GBA_RES_INDEX.md）：湾区 11 城
「专利资源 / 论文资源 / 研发投入」三维加权平均，取值 0—100。
需求未给权重 → 等权（1/3），并在 out.json 明示这是补全而非原文。

本脚本按该口径在 gkx + 共享缓存上复算，把三处口径塌缩点全部打进 out.json：
  1. 11 城只有 4 城有实体机构（珠海/佛山/中山/江门/肇庆 0–1 家，港澳 0）；
  2. 研发投入只能取上市公司年报（856 家，占四城底册 0.24%–0.57%），非全量企业研发；
  3. 论文 2024 为入库批次断点（3.2 万篇 vs 2023 年 6,651 篇），主口径剔除 2024。

取数（零 demo、专利零 SQL）
--------------------------
- 专利：`_snapshots21/patent_scan_20261021.pkl` 的 `row_city`（2021–2024）。
- 论文：`_snapshots21/papers_city_year_gkx21.json`（第一作者单位 → 城市）。
- 研发：`_snapshots21/cityfam_stock_2019_2026_20261021.json`（gkx.dwd_org_stock_finance_info
  按 org 的研发费用，取 12 月报告期、2019–2024），org_id → city 用底册缓存。

输出：code/M_INNOV_GBA_RES_INDEX_out.json
"""
from __future__ import annotations

import json
import statistics
import sys
import time
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _gba_gkx_common as C  # noqa: E402

T0 = time.time()
MID = "M_INNOV_GBA_RES_INDEX"
CITIES = list(C.COVERED)          # 深圳/广州/东莞/惠州
MISSING = [c for c in C.GBA11 if c not in CITIES]

base = C.load_base()
_name_city, org_city, dup = C.name_city_maps(base)
scan = C.load_patent_scan()
papers = C.load_papers()
pc = C.patent_city_year(scan)
pp = C.paper_city_year(papers)

# ---------- 维度 1：专利资源（2021–2024，申请口径，全部 kind） ----------
pat_raw = {c: sum(pc.get((c, y), 0) for y in C.YEARS_FULL) for c in CITIES}

# ---------- 维度 2：论文资源（2021–2023，剔除 2024 入库断点） ----------
pap_raw = {c: sum(pp.get((c, y), 0) for y in (2021, 2022, 2023)) for c in CITIES}
pap_raw_incl24 = {c: sum(pp.get((c, y), 0) for y in C.YEARS_FULL) for c in CITIES}

# ---------- 维度 3：研发投入（上市公司年报，12 月报告期，2019–2024） ----------
stock = json.loads((C.SNAP / "cityfam_stock_2019_2026_20261021.json").read_text(encoding="utf-8"))
rd_raw = defaultdict(float)
rd_orgs = defaultdict(set)
rd_by_year = defaultdict(lambda: defaultdict(float))
rd_org_amount = defaultdict(float)
n_annual_rows = 0
n_null_amount = 0
for org_id, period, amt in stock:
    if amt is None:
        n_null_amount += 1
        continue
    period = str(period)
    y, mm = int(period[:4]), period[4:]
    if mm != "12" or not (2019 <= y <= 2024):
        continue
    c = org_city.get(org_id)
    if not c or c not in CITIES:
        continue
    v = float(amt)
    rd_raw[c] += v
    rd_orgs[c].add(org_id)
    rd_by_year[c][y] += v
    rd_org_amount[(c, org_id)] += v
    n_annual_rows += 1

rd = {c: rd_raw.get(c, 0.0) for c in CITIES}
rd_yi = {c: round(rd[c] / 1e8, 2) for c in CITIES}

# 机构总数（底册城市分布）与研发样本覆盖率
org_total = defaultdict(int)
for row in base:
    org_total[row[4]] += 1
coverage = {c: round(len(rd_orgs.get(c, ())) / org_total[c] * 100, 4) for c in CITIES}

# 单家最大贡献占比（研发维的集中度风险）
top1_share = {}
for c in CITIES:
    vals = {o: v for (cc, o), v in rd_org_amount.items() if cc == c}
    top1_share[c] = round(max(vals.values()) / rd[c] * 100, 2) if vals and rd[c] else None

# ---------- 归一与合成 ----------
W = {"patent_res": round(1 / 3, 6), "paper_res": round(1 / 3, 6), "rd_res": round(1 / 3, 6)}


def minmax_map(raw: dict) -> dict:
    vals = [raw[c] for c in CITIES]
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return {c: 50.0 for c in CITIES}
    return {c: round((raw[c] - lo) / (hi - lo) * 100, 2) for c in CITIES}


n_pat = minmax_map(pat_raw)
n_pap = minmax_map(pap_raw)
n_rd = minmax_map(rd)

main = {c: round(n_pat[c] / 3 + n_pap[c] / 3 + n_rd[c] / 3, 2) for c in CITIES}
two = {c: round((n_pat[c] + n_pap[c]) / 2, 2) for c in CITIES}
n_pap24 = minmax_map(pap_raw_incl24)
three_b = {c: round((n_pat[c] + n_pap24[c] + n_rd[c]) / 3, 2) for c in CITIES}


def rank_desc(score: dict) -> dict:
    order = sorted(CITIES, key=lambda c: -score[c])
    return {c: i + 1 for i, c in enumerate(order)}


rank_main, rank_two, rank_b = rank_desc(main), rank_desc(two), rank_desc(three_b)
scores = list(main.values())

out = {
    "metric_id": MID,
    "metric_name": "创新资源指数",
    "domain": "INNOV / 湾区创新监测（DS-05）",
    "formula_owner": "王惠（三维口径沿用；需求未给权重 → 等权补全，已披露）",
    "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    "universe": {
        "documented_cities": 11,
        "observable_cities": len(CITIES),
        "cities": CITIES,
        "missing_cities": MISSING,
        "evidence": {
            "org_base_total": sum(org_total.values()),
            "org_by_city": {c: org_total[c] for c in CITIES},
            "missing_city_org_counts": {c: org_total.get(c, 0) for c in MISSING},
            "note": "底册 189,116 行中 99.82% 在深广莞惠四城；珠海/佛山各 1 家、中山 1 家、江门/肇庆/港澳 0 家，"
                    "无法构造 11 城排名。",
        },
    },
    "dimensions": {
        "patent_res": {
            "raw": pat_raw, "unit": "件", "window": "2021–2024",
            "src": "patent_scan_20261021.pkl row_city（gkx.dwd_patent 全表 2,939,895 行，"
                   "城市由第一申请人名对齐底册）",
            "norm": n_pat, "status": "full",
        },
        "paper_res": {
            "raw": pap_raw, "unit": "篇", "window": "2021–2023",
            "src": "papers_city_year_gkx21.json（gkx.dwd_zh_paper 100,900 行，第一作者单位归属）",
            "norm": n_pap, "status": "truncated",
            "excl_2024_reason": "全国论文量 2023→2024 由 6,651 篇跳至 32,379 篇（4.87 倍），"
                                "11 城同步同比跳增，属入库批次断点而非产出增长",
        },
        "rd_res": {
            "raw": {c: round(rd[c], 2) for c in CITIES}, "yi": rd_yi, "unit": "元", "window": "2019–2024（12 月报告期）",
            "src": "cityfam_stock_2019_2026_20261021.json（gkx.dwd_org_stock_finance_info，上市公司年报）",
            "norm": n_rd, "status": "narrow",
            "coverage_pct": coverage, "n_orgs": {c: len(rd_orgs.get(c, ())) for c in CITIES},
            "top1_org_share_pct": top1_share,
            "by_year_yi": {c: {str(y): round(v / 1e8, 2) for y, v in sorted(rd_by_year[c].items())}
                           for c in CITIES},
            "limit_note": "仅上市主体年报口径，覆盖四城底册 0.24%–0.57%；不是全量企业研发投入，"
                          "也不含非上市企业与科研院所。",
        },
    },
    "weights": W,
    "weights_note": "需求未给权重；等权是可复核的缺省，不是甲方签署口径。",
    "score_main": main,
    "rank_main": rank_main,
    "sensitivity": {
        "excl_rd_2dim": {
            "score": two, "rank": rank_two,
            "note": "剔除研发投入（覆盖不足 0.6%）后名次如何变化，用于检验第一名的稳健性。",
        },
        "paper_incl_2024": {
            "score": three_b, "rank": rank_b,
            "paper_raw": pap_raw_incl24,
            "note": "论文含 2024 入库断点年；只作敏感性，不作主口径。",
        },
    },
    "score_stats": {
        "n": len(scores), "min": min(scores), "max": max(scores),
        "mean": round(statistics.mean(scores), 2), "median": round(statistics.median(scores), 2),
        "distinct_values": len(set(scores)),
    },
    "probes": {
        "patent_rows": scan["row_total"],
        "paper_corpus": papers["rows_declared"],
        "paper_first_author_mapped": sum(pp.values()),
        "stock_rows": len(stock),
        "stock_null_amount_rows": n_null_amount,
        "rd_annual_rows_used": n_annual_rows,
        "base_rows": len(base),
        "dup_names": len(dup),
    },
    "support_judgment": {
        "data_support_level": "部分支持",
        "criteria": {
            "structure": "专利 / 论文 / 上市公司研发三表结构齐全（gkx 均有承载）",
            "volume": f"11 城仅 {len(CITIES)} 城可观测；研发投入覆盖 0.24%–0.57%",
            "reproducible": True,
            "discriminative": True,
        },
        "blocking_gaps": [
            "11 城中 7 城无实体机构数据，指数无法形成湾区 11 城排名。",
            "研发投入仅上市公司口径（四城 856 家），不含非上市企业与科研院所。",
            "论文语料 2024 入库断点，主口径只能取 2021–2023。",
        ],
        "note": "三维可算但两维受限：专利维完整、论文维需截断、研发维样本极窄。按 §〇 判部分支持。",
    },
    "runtime_sec": round(time.time() - T0, 2),
}

C.write_out(MID, out)
print(f"[{time.time() - T0:.1f}s] {'城市':<6}{'专利':>12}{'论文':>8}{'研发(亿)':>12}{'主分':>8}{'名次':>5}")
for c in sorted(CITIES, key=lambda x: -main[x]):
    print(f"  {C.SHORT[c]:<6}{pat_raw[c]:>12,}{pap_raw[c]:>8,}{rd_yi[c]:>12,.0f}"
          f"{main[c]:>8.2f}{rank_main[c]:>5}")
print("  coverage%:", coverage, " top1share%:", top1_share)
print("  2-dim:", two, rank_two)
