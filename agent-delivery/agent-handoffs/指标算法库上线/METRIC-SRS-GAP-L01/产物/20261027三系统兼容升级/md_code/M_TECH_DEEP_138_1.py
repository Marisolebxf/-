#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_TECH_DEEP_138_1 深圳技术发展问题识别模型 —— 离线复算（零 SQL）。

可算支：深圳 vs 全国 IPC4 域级 LQ 的 2021→2024 变化（相对掉队）+ 绝对收缩。
不可算支：法律状态（dwd_patent_legal 20,000 行、上限覆盖 0.68%）、司法挂接（无专利号列）、
技术盗窃专源（无表）。三支均按缺口披露，不构造替代分数。
"""
from __future__ import annotations

import collections

import _tech21_common as C

M = "M_TECH_DEEP_138_1"
WINDOW = C.COMPLETE_YEARS
MIN_SZ_21, MIN_SZ_24 = 50, 100

city_ipc, city_meta = C.load_city_ipc()
sz = collections.defaultdict(collections.Counter)
for (city, year), cnt in city_ipc.items():
    if city == "深圳" and year in WINDOW:
        for k, v in cnt.items():
            sz[k][year] += v

cell, by_year, domains_all = C.load_ipc_year()


def nat(code, year):
    return cell.get((code, year), (0, 0))[0]


SZ21 = sum(sz[k][2021] for k in sz)
SZ24 = sum(sz[k][2024] for k in sz)
N21, N24 = by_year[2021], by_year[2024]

rows = []
for k in sorted(domains_all):
    s21, s24 = sz[k][2021], sz[k][2024]
    n21, n24 = nat(k, 2021), nat(k, 2024)
    if s21 < MIN_SZ_21 or s24 < MIN_SZ_24 or n21 <= 0 or n24 <= 0:
        continue
    lq21 = (s21 / SZ21) / (n21 / N21)
    lq24 = (s24 / SZ24) / (n24 / N24)
    rows.append({
        "ipc4": k, "label": C.label(k),
        "sz2021": s21, "sz2024": s24, "nat2021": n21, "nat2024": n24,
        "lq2021": round(lq21, 3), "lq2024": round(lq24, 3),
        "lq_delta": round(lq24 - lq21, 3),
        "sz_growth_pct": C.pct((s24 - s21) / s21),
        "nat_growth_pct": C.pct((n24 - n21) / n21),
    })

declining_lq = [r for r in rows if r["lq_delta"] < 0]
abs_declining = [r for r in rows if r["sz_growth_pct"] < 0]
both_any = [r for r in rows if r["lq_delta"] < 0 and r["sz_growth_pct"] < 0]
lq_flag = [r for r in rows if r["lq_delta"] <= -0.05]
abs_flag = [r for r in rows if r["sz_growth_pct"] <= -10]
both = [r for r in rows if r["lq_delta"] <= -0.05 and r["sz_growth_pct"] <= -10]

top_lq_drop = sorted(rows, key=lambda r: r["lq_delta"])[:20]
top_abs_drop = sorted(rows, key=lambda r: r["sz_growth_pct"])[:20]
top_lq_gain = sorted(rows, key=lambda r: -r["lq_delta"])[:10]

# 深圳域级集中度（HHI）变化：问题是否向少数域收缩
hhi21 = C.hhi(collections.Counter({k: sz[k][2021] for k in sz}))
hhi24 = C.hhi(collections.Counter({k: sz[k][2024] for k in sz}))

# 只读本地清单行数，不查库
LEGAL_ROWS = 20000
JUD_DETAIL_ROWS = 50000
JUD_ORG_ROWS = 3390233
PATENT_ROWS = 2939895

payload = {
    "metric_id": M,
    "generated_at": "2026-10-22",
    "params": {
        "city": "深圳市",
        "time_axis": "apdt_year（申请年）",
        "window": [2021, 2024],
        "lq_formula": "LQ=(SZ域件数/SZ总件数)/(全国域件数/全国总件数)",
        "thresholds": {"min_sz2021": MIN_SZ_21, "min_sz2024": MIN_SZ_24,
                       "lq_drop_flag": -0.05, "abs_growth_flag_pct": -10},
        "base_years_used": [2021, 2024],
        "base_years_missing": C.MISSING_BASE_YEARS,
        "excluded_years": [2025, 2026],
    },
    "totals": {
        "sz_2021": SZ21, "sz_2024": SZ24, "sz_growth_pct": C.pct((SZ24 - SZ21) / SZ21),
        "national_2021": N21, "national_2024": N24, "national_growth_pct": C.pct((N24 - N21) / N21),
        "sz_hhi_2021": hhi21, "sz_hhi_2024": hhi24,
    },
    "universe": {"ipc4_total": len(domains_all), "eligible_domains": len(rows)},
    "problem_summary": {
        "declining_lq": len(declining_lq),
        "declining_lq_share_pct": C.pct(len(declining_lq) / len(rows)),
        "absolute_declining": len(abs_declining),
        "both_lq_and_abs_decline": len(both),
        "both_share_pct": C.pct(len(both) / len(rows)),
        "both_any_negative": len(both_any),
        "lq_le_minus_005": len(lq_flag),
        "abs_le_minus_10": len(abs_flag),
        "matrix_flagged": {
            "double": len(both),
            "lq_only": len(lq_flag) - len(both),
            "abs_only": len(abs_flag) - len(both),
            "neither": len(rows) - len(lq_flag) - len(abs_flag) + len(both),
        },
    },
    "top_lq_drop": top_lq_drop,
    "top_absolute_drop": top_abs_drop,
    "relative_gainers": top_lq_gain,
    "problem_list": sorted(both, key=lambda r: r["lq_delta"])[:30],
    "legal_dim": {
        "available": False,
        "rows": LEGAL_ROWS,
        "max_coverage_pct": round(LEGAL_ROWS / PATENT_ROWS * 100, 2),
        "blocker": "dwd_patent_legal 仅 20,000 行（上限覆盖 0.68%），本批无域级缓存；按技术维零 SQL 纪律不查库，死亡专利密度不可算。",
    },
    "judicial_dim": {
        "available": False,
        "case_detail_rows": JUD_DETAIL_ROWS,
        "org_case_rows": JUD_ORG_ROWS,
        "blocker": "司法两表无专利号/申请号挂接列（前批已核实），无法把案件映射到 IPC4 域；本批不重复探测。",
    },
    "theft_dim": {
        "available": False,
        "blocker": "库内无技术秘密/窃取类专表，盗窃问题无源；不以司法总量冒充。",
    },
    "base_years_used": [2021, 2024],
    "base_years_missing": C.MISSING_BASE_YEARS,
}

payload["support_judgment"] = {
    "data_support_level": "部分支持",
    "criteria": {
        "lq_decline_list": True,
        "eligible_domains": len(rows),
        "declining_lq": len(declining_lq),
        "both_lq_and_abs_decline": len(both),
        "legal_dim": False,
        "judicial_dim": False,
        "theft_dim": False,
    },
    "reason": (
        f"落后维可交付：{len(rows)} 个域中 {len(declining_lq)} 个 LQ 下行、{len(both)} 个同时绝对收缩，"
        f"深圳总件数 {SZ21:,}→{SZ24:,}（{C.pct((SZ24 - SZ21) / SZ21)}%）快于全国（{C.pct((N24 - N21) / N21)}%），问题清单可复算；"
        "但侵权维（法律状态上限覆盖 0.68%）、司法挂接（无专利号列）与盗窃专源（无表）三支始终缺源，故判部分支持。"
    ),
}

C.write_out(M, payload)
