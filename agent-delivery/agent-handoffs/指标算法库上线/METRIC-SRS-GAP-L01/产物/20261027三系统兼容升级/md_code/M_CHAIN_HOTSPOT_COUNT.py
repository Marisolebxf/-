#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_HOTSPOT_COUNT 热点/历程事件数（热点领域数）

三路信号（均在同一母体内取率，再跨 L1 做 min-max 归一）：
  growth  = 2021—2025 成立企业数 / 有成立年的企业数
  fin     = 2021—2025 融资事件数 / 可映射企业数
  patent  = 累计专利数 / 可映射企业数
综合分 = 0.34*growth_z + 0.33*fin_z + 0.33*patent_z；>= 0.60 记为热点 L1。

纯快照复算：
  code/_snapshots21/chain_firm_year_20261023.json
  code/_snapshots21/chain_firm_index_20261023.json
  code/_snapshots21/chain21_fin_degree_20261022.json
  code/_snapshots21/star_applicant_agg_gkx.json
产出：code/M_CHAIN_HOTSPOT_COUNT_out.json
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_CHAIN_HOTSPOT_COUNT_out.json"

F = json.loads((SNAP / "chain_firm_year_20261023.json").read_text(encoding="utf-8"))
IDX = json.loads((SNAP / "chain_firm_index_20261023.json").read_text(encoding="utf-8"))
PAT = json.loads((SNAP / "star_applicant_agg_gkx.json").read_text(encoding="utf-8"))
FIN = json.loads((SNAP / "chain21_fin_degree_20261022.json").read_text(encoding="utf-8"))

CHAIN_NAME = F["chain_name"]
RECENT = range(2021, 2026)
WEIGHTS = {"growth": 0.34, "fin": 0.33, "patent": 0.33}
THRESHOLD = 0.60
FLOOR = 30

NAME_L1 = IDX["name_l1"]
L1_NAME = F["l1_name"]
L1_FIRMS = F["l1_firms"]

# 母体 1：可映射企业（按公司名映射到 L1；融资/专利都靠这张表）
mapped_firms = defaultdict(int)
for name, l1 in NAME_L1.items():
    mapped_firms[l1] += 1

# 母体 2：专利（申请人名 -> L1）
patent_total = sum(v[0] for v in PAT["agg"].values())
patent_inv = sum(v[1] for v in PAT["agg"].values())
patent_l1 = defaultdict(int)
patent_l1_inv = defaultdict(int)
patent_names = 0
for name, (cnt, inv) in PAT["agg"].items():
    l1 = NAME_L1.get(name)
    if not l1:
        continue
    patent_names += 1
    patent_l1[l1] += cnt
    patent_l1_inv[l1] += inv

# 母体 3：融资事件（2021—2025）
fin_total = len(FIN["fin"])
fin_total_recent = 0
fin_l1 = defaultdict(int)
for r in FIN["fin"]:
    y = (r[6] or "")[:4]
    if not y or not (2021 <= int(y) <= 2025):
        continue
    fin_total_recent += 1
    l1 = NAME_L1.get(r[1])
    if l1:
        fin_l1[l1] += 1

rows = []
for l1, firms in L1_FIRMS.items():
    yk = 0
    recent = 0
    for k, v in F["l1_year"].items():
        code, ys = k.split("|")
        if code != l1:
            continue
        yk += v
        if 2021 <= int(ys) <= 2025:
            recent += v
    mf = mapped_firms.get(l1, 0)
    rows.append({
        "l1_code": l1,
        "l1_name": L1_NAME[l1],
        "chain_code": l1[:7],
        "chain_name": CHAIN_NAME.get(l1[:7], ""),
        "l1_firms": firms,
        "year_known": yk,
        "mapped_firms": mf,
        "patents": patent_l1.get(l1, 0),
        "patents_invention": patent_l1_inv.get(l1, 0),
        "fin_events_2021_2025": fin_l1.get(l1, 0),
        "growth_rate": round(recent / yk, 4) if yk else None,
        "patent_density": round(patent_l1.get(l1, 0) / mf, 2) if mf else None,
        "fin_density": round(fin_l1.get(l1, 0) / mf, 4) if mf else None,
        "eligible": mf >= FLOOR and yk >= FLOOR,
    })

eligible = [r for r in rows if r["eligible"]]
excluded = [
    {
        "l1_code": r["l1_code"],
        "l1_name": r["l1_name"],
        "mapped_firms": r["mapped_firms"],
        "year_known": r["year_known"],
        "reason": "可映射企业<30" if r["mapped_firms"] < FLOOR else "有成立年企业<30",
    }
    for r in rows if not r["eligible"]
]


def minmax(key: str):
    vals = [r[key] for r in eligible]
    lo, hi = min(vals), max(vals)
    z = {r["l1_code"]: ((r[key] - lo) / (hi - lo) if hi > lo else 0.5) for r in eligible}
    return z, lo, hi


zg, g_lo, g_hi = minmax("growth_rate")
zf, f_lo, f_hi = minmax("fin_density")
zp, p_lo, p_hi = minmax("patent_density")

for r in eligible:
    code = r["l1_code"]
    r["z_growth"] = round(zg[code], 4)
    r["z_fin"] = round(zf[code], 4)
    r["z_patent"] = round(zp[code], 4)
    r["hotspot_score"] = round(
        WEIGHTS["growth"] * zg[code] + WEIGHTS["fin"] * zf[code] + WEIGHTS["patent"] * zp[code], 4
    )
    r["hotspot_score_display"] = f"{r['hotspot_score']:.3f}"
    r["is_hotspot"] = r["hotspot_score"] >= THRESHOLD

hot = [r for r in eligible if r["is_hotspot"]]
hot.sort(key=lambda r: -r["hotspot_score"])

# 链级汇总
per_chain = []
for ch in sorted(CHAIN_NAME):
    ls = [r for r in rows if r["chain_code"] == ch]
    ev = [r for r in ls if r["eligible"]]
    hs = [r for r in ev if r["is_hotspot"]]
    per_chain.append({
        "chain_code": ch,
        "chain_name": CHAIN_NAME[ch],
        "l1_total": len(ls),
        "l1_evaluable": len(ev),
        "hotspot_count": len(hs),
        "hotspot_l1": [r["l1_name"] for r in hs],
        "max_score": max((r["hotspot_score"] for r in ev), default=None),
    })

# 敏感性
def count_at(th: float, w=WEIGHTS, floor=FLOOR) -> int:
    ev = [r for r in rows if r["mapped_firms"] >= floor and r["year_known"] >= floor]
    if not ev:
        return 0
    def zz(key):
        vs = [r[key] for r in ev]
        lo, hi = min(vs), max(vs)
        return {r["l1_code"]: ((r[key] - lo) / (hi - lo) if hi > lo else 0.5) for r in ev}
    a, b, c = zz("growth_rate"), zz("fin_density"), zz("patent_density")
    n = 0
    for r in ev:
        s = w["growth"] * a[r["l1_code"]] + w["fin"] * b[r["l1_code"]] + w["patent"] * c[r["l1_code"]]
        if s >= th:
            n += 1
    return n


sensitivity = {
    "threshold": [{"threshold": t, "hotspot_count": count_at(t)} for t in (0.50, 0.55, 0.60, 0.65, 0.70)],
    "weights": [
        {"name": "equal", "w": {"growth": 1 / 3, "fin": 1 / 3, "patent": 1 / 3}, "hotspot_count": count_at(THRESHOLD, {"growth": 1 / 3, "fin": 1 / 3, "patent": 1 / 3})},
        {"name": "capital_led", "w": {"growth": 0.2, "fin": 0.45, "patent": 0.35}, "hotspot_count": count_at(THRESHOLD, {"growth": 0.2, "fin": 0.45, "patent": 0.35})},
        {"name": "growth_led", "w": {"growth": 0.5, "fin": 0.25, "patent": 0.25}, "hotspot_count": count_at(THRESHOLD, {"growth": 0.5, "fin": 0.25, "patent": 0.25})},
    ],
    "floor": [{"floor": f, "evaluable": len([r for r in rows if r["mapped_firms"] >= f and r["year_known"] >= f]), "hotspot_count": count_at(THRESHOLD, WEIGHTS, f)} for f in (30, 50, 100)],
}

payload = {
    "metric_id": "M_CHAIN_HOTSPOT_COUNT",
    "metric_name": "热点/历程事件数（热点领域数）",
    "formula_owner": "AI 补漏调研 2026-08-21（算法库 1.1.1.1.1.1.1.3.4 转写）；本件 2026-10-22 复算",
    "support_judgment": "部分支持",
    "base_years_used": [2021, 2022, 2023, 2024, 2025],
    "base_years_missing": [],
    "base_years_note": (
        "增速与融资取 2021—2025 五年窗口；2026 为残年（链内仅 5 家新成立、融资 238 笔），"
        "不进取数窗口；专利为累计存量，不分年"
    ),
    "value": len(hot),
    "unit": "个",
    "scope": "12 条链、41 个 L1 环节；28 个达到证据门槛的环节参与热点判定",
    "definition": (
        "热点领域数 = 在可评估 L1 中，企业增速、投融资热度、专利密度三信号"
        "min-max 归一加权后综合分 >= 0.60 的环节去重数；对象是环节，不是资讯条数"
    ),
    "headline": {
        "hotspot_count": len(hot),
        "evaluable_l1": len(eligible),
        "total_l1": len(rows),
        "excluded_l1": len(excluded),
        "chains_with_hotspot": sum(1 for c in per_chain if c["hotspot_count"] > 0),
        "threshold": THRESHOLD,
        "weights": WEIGHTS,
        "floor": FLOOR,
        "top_hotspot": hot[0]["l1_name"] if hot else None,
        "top_score": hot[0]["hotspot_score"] if hot else None,
        "top_score_display": hot[0]["hotspot_score_display"] if hot else None,
        "gap_to_threshold": round(THRESHOLD - sorted((r["hotspot_score"] for r in eligible if not r["is_hotspot"]), reverse=True)[0], 4) if hot else None,
    },
    "hotspots": [
        {
            "rank": i,
            "l1_code": r["l1_code"],
            "l1_name": r["l1_name"],
            "chain_name": r["chain_name"],
            "score": r["hotspot_score"],
            "score_display": r["hotspot_score_display"],
            "growth_rate": r["growth_rate"],
            "fin_density": r["fin_density"],
            "patent_density": r["patent_density"],
            "z": [r["z_growth"], r["z_fin"], r["z_patent"]],
        }
        for i, r in enumerate(hot, 1)
    ],
    "per_l1": sorted(rows, key=lambda r: (-(r.get("hotspot_score") or -1), r["l1_code"])),
    "per_chain": per_chain,
    "excluded": excluded,
    "normalization": {
        "method": "min-max，仅在 28 个可评估 L1 内归一",
        "growth_range": [g_lo, g_hi],
        "fin_range": [f_lo, f_hi],
        "patent_range": [p_lo, p_hi],
    },
    "sensitivity": sensitivity,
    "signal_coverage": {
        "growth": {
            "mother": "链内有成立年的企业",
            "numerator": sum(v for k, v in F["l1_year"].items() if 2021 <= int(k.split("|")[1]) <= 2025),
            "denominator": sum(F["l1_year"].values()),
            "coverage_of_chain_firms_pct": round(100.0 * sum(F["l1_year"].values()) / 1714457, 2),
            "chain_matched_total": sum(F["chain_matched"].values()),
            "l1_matched_total": sum(F["l1_year"].values()),
            "chain_matched_without_l1": sum(F["chain_matched"].values()) - sum(F["l1_year"].values()),
        },
        "fin": {
            "mother": "可按公司名映射到 L1 的企业",
            "events_total": fin_total,
            "events_recent": fin_total_recent,
            "events_recent_mapped": sum(fin_l1.values()),
            "mapped_share_pct": round(100.0 * sum(fin_l1.values()) / fin_total_recent, 2) if fin_total_recent else 0.0,
            "mapped_firms": sum(mapped_firms.values()),
        },
        "patent": {
            "mother": "可按申请人名映射到 L1 的企业",
            "applicant_names_total": len(PAT["agg"]),
            "applicant_names_mapped": patent_names,
            "name_share_pct": round(100.0 * patent_names / len(PAT["agg"]), 2),
            "patents_total": patent_total,
            "patents_mapped": sum(patent_l1.values()),
            "patent_share_pct": round(100.0 * sum(patent_l1.values()) / patent_total, 2),
            "invention_total": patent_inv,
        },
    },
    "related_tables": {"dwd_industry_chain_news_info": 108052},
    "sources": [
        "code/_snapshots21/chain_firm_year_20261023.json",
        "code/_snapshots21/chain_firm_index_20261023.json",
        "code/_snapshots21/chain21_fin_degree_20261022.json",
        "code/_snapshots21/star_applicant_agg_gkx.json",
    ],
    "notes": [
        "阈值 0.60 与权重 0.34/0.33/0.33 均为本件自定义，不是甲方确认口径；旧稿只写“阈值待甲方确认”",
        "三路信号的母体不同（成立年 28,031 家、可映射 21,933 家），综合分是三个归一分的加权，不是同一分母下的率",
        "专利为申请人名下累计专利，不是环节内企业专利全集：可映射申请人只占 12.96% 的名称、32.31% 的专利量",
        "融资只取 2021—2025，避免把 2015—2016 双创高峰的累计融资当成当前热度",
        "可评估 28 个 L1，13 个因可映射企业或有成立年企业少于 30 家被排除；热点数不能外推为 41 个环节的热点总数",
    ],
}

OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print("wrote", OUT)
print("hot", len(hot), [h["l1_name"] for h in hot], "eligible", len(eligible))
