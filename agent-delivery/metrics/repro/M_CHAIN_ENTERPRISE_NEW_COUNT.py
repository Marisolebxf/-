#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_ENTERPRISE_NEW_COUNT 新增关联企业数（否定性证据 + 成立年代理观察）

官方口径（2026-10-14 拍板）：该年首次挂上链的企业去重家数，时间轴 = first_link_date。
本件结论：官方口径在 gkx 不可执行（0 行，不是 0 家），故 support_judgment = 完全不支持。
同时给出“当年成立且当前在链”的代理观察表，仅用于说明缺口量级，不充作指标值。

纯快照复算：
  code/_snapshots21/chain_firm_year_20261023.json
  code/_snapshots21/ent_base_year_20261022.json
  code/_snapshots21/probe_chain_meta_20261022.json
产出：code/M_CHAIN_ENTERPRISE_NEW_COUNT_out.json
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_CHAIN_ENTERPRISE_NEW_COUNT_out.json"

F = json.loads((SNAP / "chain_firm_year_20261023.json").read_text(encoding="utf-8"))
BASE = json.loads((SNAP / "ent_base_year_20261022.json").read_text(encoding="utf-8"))
META = json.loads((SNAP / "probe_chain_meta_20261022.json").read_text(encoding="utf-8"))

CHAIN_NAME = F["chain_name"]
RECENT = [2021, 2022, 2023, 2024, 2025]

# 全库底册年份分布
base_year = {int(r["year"]): int(r["n"]) for r in BASE["rows"] if r.get("year") is not None}
base_total = sum(base_year.values())
base_declared = sum(int(r["n"]) for r in BASE["rows"])
base_no_year = sum(int(r["n"]) for r in BASE["rows"] if r.get("year") is None)
base_recent = sum(base_year.get(y, 0) for y in RECENT)


def chain_years(ch: str) -> dict[int, int]:
    out = {}
    for k, v in F["chain_year"].items():
        c, y = k.split("|")
        if c == ch:
            out[int(y)] = int(v)
    return out


per_chain = []
for ch in sorted(CHAIN_NAME):
    ys = chain_years(ch)
    matched = int(F["chain_matched"].get(ch, 0))
    firms = int(F["chain_firms"][ch])
    new_recent = sum(ys.get(y, 0) for y in RECENT)
    new_2026 = ys.get(2026, 0)
    pre2021 = sum(v for y, v in ys.items() if y <= 2020)
    per_chain.append({
        "chain_code": ch,
        "chain_name": CHAIN_NAME[ch],
        "chain_firms": firms,
        "year_known": matched,
        "coverage_pct": round(100.0 * matched / firms, 2) if firms else 0.0,
        "new_2021_2025_proxy": new_recent,
        "new_2026_residual": new_2026,
        "stock_le_2020_proxy": pre2021,
        "proxy_share_pct": round(100.0 * new_recent / matched, 2) if matched else 0.0,
        "year_series": {str(y): ys.get(y, 0) for y in range(2019, 2027)},
    })

matched_total = sum(r["year_known"] for r in per_chain)
new_total = sum(r["new_2021_2025_proxy"] for r in per_chain)
new_2026_total = sum(r["new_2026_residual"] for r in per_chain)
stock_total = sum(r["stock_le_2020_proxy"] for r in per_chain)
firms_total = sum(r["chain_firms"] for r in per_chain)

year_totals = {}
for y in list(range(2019, 2027)):
    year_totals[str(y)] = sum(chain_years(ch).get(y, 0) for ch in CHAIN_NAME)

base_share = {str(y): round(100.0 * base_year.get(y, 0) / base_total, 3) for y in range(2019, 2027)}
chain_share = {str(y): round(100.0 * year_totals[str(y)] / matched_total, 3) for y in range(2019, 2027)}
finding = (
    f"链内可匹配样本偏老：2021 年全库占 {base_share['2021']:.3f}%、链内样本占 {chain_share['2021']:.3f}%；"
    f"2024 年全库占 {base_share['2024']:.3f}%、链内样本仅 {chain_share['2024']:.3f}%；"
    f"2021—2025 合计全库占 {100.0 * base_recent / base_total:.2f}%、链内样本占 {100.0 * new_total / matched_total:.2f}%。"
    "故代理的“新成立占比”被系统性压低"
)

payload = {
    "metric_id": "M_CHAIN_ENTERPRISE_NEW_COUNT",
    "metric_name": "新增关联企业数",
    "formula_owner": "human:徐滕强 2026-10-14 拍板（首挂年口径）；本件否定性复核 2026-10-22",
    "support_judgment": "完全不支持",
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": (
        "官方口径以 first_link_date 分年，该字段不存在，无法确定基期；"
        "代理观察用成立年 2021—2025（2026 仅 5 家，作残年单列，不进取数窗口）"
    ),
    "value": None,
    "unit": "家",
    "value_note": "官方口径不可得：不是 0 家，而是 0 行（无 first_link_date，无法分年）",
    "scope": "官方对象 = 当年首次挂链企业；本件代理观察对象 = 当年成立且当前仍在链的企业",
    "official": {
        "definition": "年度新增挂链企业数 = 该年首次挂上链的企业去重家数（退出后重挂不计）",
        "formula": "YEAR(MIN(first_link_date)) GROUP BY org_id，外层按年 COUNT(DISTINCT org_id)",
        "executable": False,
        "rows": 0,
        "reasons": [
            "gkx 库不存在 enterprise_industry_chain 表（SHOW TABLES 仅 dwd_industry_chain_info / dwd_industry_chain_news_info）",
            "dwd_org_industry_tags 16 列中无 first_link_date、无 org_id",
            "created_time 全表 2,283,762 行只有 1 个取值 2026-08-27 11:08:26，是单批入库戳，不能分年",
            "calc-logic 明写禁止用注册年分布替代首挂年（B 档语义偷换）",
        ],
    },
    "proxy": {
        "name": "当年成立且当前在链（成立年代理）",
        "is_official": False,
        "new_2021_2025": new_total,
        "new_2026_residual": new_2026_total,
        "stock_le_2020": stock_total,
        "year_known": matched_total,
        "coverage_pct": round(100.0 * matched_total / firms_total, 2),
        "recent_share_pct": round(100.0 * new_total / matched_total, 2),
        "why_not_metric": (
            "成立年与首次挂链年无单调关系：老企业可以 2024 年才挂链，新企业也可能尚未挂链；"
            "且代理只覆盖 1.63% 的链企业，量级比全链企业少两个数量级，不能当新增挂链数"
        ),
    },
    "per_chain": per_chain,
    "year_totals_proxy": year_totals,
    "base_distribution": {
        "base_rows_declared": base_declared,
        "base_rows_snapshot": base_declared,
        "base_with_year": base_total,
        "base_no_year": base_no_year,
        "meta_with_year": 188761,
        "one_row_diff_note": "逐行求和 188,762 与元数据 188,761 差 1 行；本件引用时写“底册 189,116 行、其中 354 行无成立年”，不把 188,761/188,762 当指标值",
        "base_recent_2021_2025": base_recent,
        "base_recent_share_pct": round(100.0 * base_recent / base_total, 2),
    },
    "caliber": {
        "rows_total": 2283762,
        "empty_link_rows": 569303,
        "bad_credit_rows": 2,
        "chain_nonempty_rows": 1714459,
        "chain_clean_old": 1714458,
        "chain_clean_dedup": 1714457,
        "note": "1,714,457 为本件默认（去脏+链内+去重）；1,714,458 为链内未去脏旧口径；1,714,459 为全表非空行数",
    },
    "coverage": {
        "chain_firms_clean": firms_total,
        "matched_base": matched_total,
        "matched_pct": round(100.0 * matched_total / firms_total, 2),
        "chain_unmatched": firms_total - matched_total,
        "chain_matched_no_year": 0,
        "credit_bad_rows": F.get("bad_credit_rows", 2),
        "empty_link_rows": F.get("empty_rows", 569303),
    },
    "bias_check": {
        "base_year_share_pct": base_share,
        "chain_matched_share_pct": chain_share,
        "finding": finding,
    },
    "integrity": {
        "sum_check_matched": matched_total,
        "sum_check_parts": new_total + new_2026_total + stock_total,
        "chain_sum_equals_clean_total": firms_total == 1714457,
        "year_range": F.get("year_range", {}).get("min", 1959),
        "year_range_max": F.get("year_range", {}).get("max", 2026),
    },
    "sources": [
        "code/_snapshots21/chain_firm_year_20261023.json",
        "code/_snapshots21/ent_base_year_20261022.json",
        "code/_snapshots21/probe_chain_meta_20261022.json",
    ],
    "notes": [
        "1,714,457 是去脏 + 链内口径（§3.50）：2,283,762 行 - 569,303 空链行 - 2 个非 18 位信用码，再按链去重",
        "同一企业可挂多链，chain_firms 逐链去重后相加 = 1,714,457，恰好等于全表去重值，说明多链重复与去重抵消属巧合，不应当作划分",
        "2026 年仅 5 家，是残年；不得把 2026 当完整年做同比",
        "底册 189,116 行中 354 行无成立年，链内匹配样本 0 行无成立年",
    ],
}

OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print("wrote", OUT)
print("matched", matched_total, "new", new_total, "2026", new_2026_total, "stock", stock_total)
print("sum", new_total + new_2026_total + stock_total)
