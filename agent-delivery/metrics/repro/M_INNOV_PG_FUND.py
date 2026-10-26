#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""经费支持（M_INNOV_PG_FUND）——零 SQL 复算。

需求 seq 154 明列三类经费：科研经费 / 产业基金 / 补贴资金。
  科研经费：gkx.dwd_org_stock_finance_info.research_development_amount（上市主体年报口径）
  产业基金：gkx.dwd_industrial_fund_basic_info（10,891 只基金，注册地/注册资本/设立年）
  补贴资金：gkx 无补贴台账（dwd_fund_basic_info 0 行），live 侧亦无 → 不可算

口径要点：
  1) 研发费用按年报取数（occur_period 月=12），不与季报累加，避免 4 倍重复；
  2) 产业基金金额是「注册资本」，不是「实缴/投资额」，实缴列仅 1,808/10,891 有值；
  3) 项目资助额（dwd_zh_project.funded_amount）属 seq 155 项目支持，不并入本指标，仅作旁证。

输入：code/_snapshots21/pg_stock_rd_annual_20261021.json
      code/_snapshots21/pg_fund_rows_20261021.json
      code/_snapshots21/pg_probe2_20261021.json
      code/_snapshots21/base_20261021.json
产物：code/M_INNOV_PG_FUND_out.json
"""
from __future__ import annotations

import json
import os
import re
import statistics
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_INNOV_PG_FUND_out.json")
METRIC_ID = "M_INNOV_PG_FUND"
FOUR = ["深圳市", "广州市", "东莞市", "惠州市"]
RD_WINDOW = (2021, 2025)


def parse_capital_wan(s):
    """把 '29120万元' / '5亿元' / '3000元' 统一成万元；无法解析返回 None。"""
    if not s:
        return None
    m = re.search(r"([\d.]+)\s*(亿元|万元|元)", str(s))
    if not m:
        return None
    v = float(m.group(1))
    unit = m.group(2)
    if unit == "万元":
        return v
    if unit == "亿元":
        return v * 10000.0
    return v / 10000.0


def fund_city(reg):
    """reg_region 形如 '中国-广东省-深圳市-南山区'，取第一个『市』级片段。"""
    if not reg:
        return ""
    parts = [p for p in str(reg).split("-") if p]
    for p in parts:
        if p.endswith("市"):
            return p
    return ""


def main() -> None:
    t0 = time.time()
    rd_rows = json.load(open(os.path.join(SNAP, "pg_stock_rd_annual_20261021.json"), encoding="utf-8"))
    fund_rows = json.load(open(os.path.join(SNAP, "pg_fund_rows_20261021.json"), encoding="utf-8"))
    probe = json.load(open(os.path.join(SNAP, "pg_probe2_20261021.json"), encoding="utf-8"))
    base = json.load(open(os.path.join(SNAP, "base_20261021.json"), encoding="utf-8"))
    org_city = {b[0]: b[4] for b in base}

    # ---------- 1. 科研经费（上市主体年报） ----------
    by_year = defaultdict(lambda: {"n": 0, "sum": 0.0, "cities": Counter()})
    by_city = defaultdict(lambda: {"n": 0, "sum": 0.0, "orgs": set()})
    for r in rd_rows:
        y = int(str(r["period"])[:4])
        city = org_city.get(r["org_id"], "未匹配")
        by_year[y]["n"] += 1
        by_year[y]["sum"] += r["rd"]
        by_year[y]["cities"][city] += 1
        if RD_WINDOW[0] <= y <= RD_WINDOW[1]:
            by_city[city]["n"] += 1
            by_city[city]["sum"] += r["rd"]
            by_city[city]["orgs"].add(r["org_id"])

    rd_years = []
    for y in sorted(by_year):
        b = by_year[y]
        if y < 2017:
            continue
        rd_years.append({"year": y, "n": b["n"], "sum_yi": round(b["sum"] / 1e8, 2),
                         "avg_yi": round(b["sum"] / 1e8 / b["n"], 3)})

    rd_city_rows = []
    for c in FOUR:
        b = by_city.get(c, {"n": 0, "sum": 0.0, "orgs": set()})
        rd_city_rows.append({
            "city": c, "rows": b["n"], "orgs": len(b["orgs"]),
            "sum_yi": round(b["sum"] / 1e8, 2),
            "avg_yi": round(b["sum"] / 1e8 / b["n"], 3) if b["n"] else 0.0,
        })
    listed_orgs = len({r["org_id"] for r in rd_rows})
    rd_window_orgs = len({r["org_id"] for r in rd_rows if RD_WINDOW[0] <= int(str(r["period"])[:4]) <= RD_WINDOW[1]})

    # ---------- 2. 产业基金 ----------
    fc = Counter(fund_city(f["reg_region"]) for f in fund_rows)
    n_fund = len(fund_rows)
    ids = {f["fund_id"] for f in fund_rows}
    cap_vals = [parse_capital_wan(f.get("reg_capital")) for f in fund_rows]
    caps_ok = [v for v in cap_vals if v is not None]
    real_ok = [parse_capital_wan(f.get("real_capital")) for f in fund_rows]
    real_ok = [v for v in real_ok if v is not None]
    cap_by_city = defaultdict(lambda: {"n": 0, "sum_wan": 0.0})
    for f in fund_rows:
        v = parse_capital_wan(f.get("reg_capital"))
        c = fund_city(f["reg_region"])
        if v is not None:
            cap_by_city[c]["n"] += 1
            cap_by_city[c]["sum_wan"] += v

    fund_city_rows = []
    for c in FOUR:
        b = cap_by_city.get(c, {"n": 0, "sum_wan": 0.0})
        fund_city_rows.append({
            "city": c, "funds": fc.get(c, 0),
            "capital_rows": b["n"],
            "capital_yi": round(b["sum_wan"] / 10000.0, 2),
            "avg_yi": round(b["sum_wan"] / 10000.0 / b["n"], 3) if b["n"] else 0.0,
        })

    est_years = Counter((str(f.get("est_date") or "")[:4]) for f in fund_rows)
    est_clean = {k: v for k, v in est_years.items() if k.isdigit()}
    fund_types = Counter(f.get("fund_type") or "（未标注）" for f in fund_rows)
    owned = Counter(f.get("state_owned") or "（未标注）" for f in fund_rows)

    # ---------- 3. 补贴资金（缺表，显式记 0） ----------
    subsidy = {
        "tables_found": 0,
        "note": "gkx.dwd_fund_basic_info 0 行；live 与 gkx 均无补贴/资助台账表；不得用项目资助额冒充",
    }

    # ---------- 4. 项目资助（旁证，不并入） ----------
    proj = {int(str(y)[:4]): {"n": n, "amt_wan": float(amt or 0)}
            for y, n, amt, fin in probe["proj_year"]}
    proj_total_n = sum(v["n"] for v in proj.values())
    proj_total_amt = sum(v["amt_wan"] for v in proj.values())

    result = {
        "metric_id": METRIC_ID,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "data_source": "gkx.dwd_org_stock_finance_info / dwd_industrial_fund_basic_info @ 183.240.141.251:3318（快照复算，零 SQL）",
        "support_judgment": "部分支持",
        "n_records": {
            "rd_annual_rows": len(rd_rows),
            "industrial_funds": n_fund,
            "industrial_fund_ids": len(ids),
        },
        "rd": {
            "source_note": "上市公司年报研发费用（research_development_amount），仅上市主体，非全量企业研发投入",
            "annual_rows": len(rd_rows),
            "distinct_orgs_all_years": listed_orgs,
            "distinct_orgs_2021_2025": rd_window_orgs,
            "base_orgs": len(base),
            "listed_coverage_of_base": round(100 * listed_orgs / len(base), 3),
            "by_year": rd_years,
            "by_city_2021_2025": rd_city_rows,
            "window": {"from": RD_WINDOW[0], "to": RD_WINDOW[1]},
            "base_years_used": [y for y in range(RD_WINDOW[0], RD_WINDOW[1] + 1) if by_year.get(y, {}).get("n", 0) > 0],
            "base_years_missing": [2026],
        },
        "fund": {
            "source_note": "产业基金基本表；金额为注册资本（reg_capital），不是实缴资本或投资额",
            "n_funds": n_fund,
            "n_distinct_ids": len(ids),
            "capital_parseable": len(caps_ok),
            "capital_parse_rate": round(100 * len(caps_ok) / n_fund, 2),
            "capital_sum_yi": round(sum(caps_ok) / 10000.0, 2),
            "capital_median_yi": round(statistics.median(caps_ok) / 10000.0, 3) if caps_ok else None,
            "capital_max_yi": round(max(caps_ok) / 10000.0, 2) if caps_ok else None,
            "real_capital_parseable": len(real_ok),
            "real_capital_parse_rate": round(100 * len(real_ok) / n_fund, 2),
            "by_city": fund_city_rows,
            "city_unspecified": fc.get("", 0),
            "n_cities": len([c for c in fc if c]),
            "top_cities": [{"city": k, "n": v} for k, v in fc.most_common(12)],
            "types": [{"type": k, "n": v} for k, v in fund_types.most_common()],
            "state_owned": dict(owned),
            "est_years": [{"year": int(k), "n": v} for k, v in sorted(est_clean.items())],
            "est_missing": sum(v for k, v in est_years.items() if not k.isdigit()),
        },
        "subsidy": subsidy,
        "project_funding_reference": {
            "n_projects": proj_total_n,
            "total_wan": round(proj_total_amt, 1),
            "total_yi": round(proj_total_amt / 1e4, 2),
            "note": "属 seq 155 项目支持（M_INNOV_PG_PROJECT），不并入本指标，避免两指标重复计数",
        },
        "caveats": [
            "科研经费仅覆盖上市主体：全期 6,098 条年报、约 700 家/年，占底册 189,116 家的 0.37%",
            "产业基金注册资本填充率 58.57%（6,379/10,891），实缴资本仅 16.60%（1,808/10,891）",
            "基金注册地有 892 条『未披露』与 75 条仅『中国』，城市归属不可得",
            "补贴资金无任何表，需求三类经费中第三类整类缺失",
            "研发费用 2024 年跳升、2025 年回落，样本主体变动会显著影响城市合计，不可作增速结论",
        ],
        "runtime_sec": None,
    }

    print(f"[{METRIC_ID}] rd_rows={len(rd_rows)} funds={n_fund}")
    print("研发年度:", [(x["year"], x["n"], x["sum_yi"]) for x in rd_years])
    print("研发四城 2021-2025:", [(x["city"], x["orgs"], x["sum_yi"]) for x in rd_city_rows])
    print("基金四城:", [(x["city"], x["funds"], x["capital_yi"]) for x in fund_city_rows])
    print(f"基金资本: 可解析 {len(caps_ok)}/{n_fund}，合计 {result['fund']['capital_sum_yi']} 亿元")
    print(f"项目资助旁证: {proj_total_n} 项 / {result['project_funding_reference']['total_yi']} 亿元")

    result["runtime_sec"] = round(time.time() - t0, 3)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print(f"saved {OUT} ({result['runtime_sec']}s)")


if __name__ == "__main__":
    main()
