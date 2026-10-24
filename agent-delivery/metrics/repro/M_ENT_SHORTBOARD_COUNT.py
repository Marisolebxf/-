#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_SHORTBOARD_COUNT —— 短板指标数（W13-E4）

口径（calc-logic 正本 + 本件实现规则）：
  企业每个 L3 与「同链 × 同年」均值比；正向指标低于均值、资产负债率高于均值 → 记 1 条短板。
  空值不判（不计入分子，也不当「低于」）；同业均值的样本 < 5 家不判（本件加严，见 note）。

L3 九项来自 calc-logic（SCORE 四维现稿）：
  6 项可从 gkx.dwd_org_annual_financial_info 算；3 项无原料（本科及以上占比无字段、
  研发人员占比 development_employee 全空、市占率只有 15 行药品市场数据）。

运行：cd code && python3 M_ENT_SHORTBOARD_COUNT.py
产物：code/M_ENT_SHORTBOARD_COUNT_out.json
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_ENT_SHORTBOARD_COUNT_out.json")

MIN_PEERS = 5          # 同链同年样本下限（含本企业），低于此不判
RATIO_CLIP = 10.0      # 比率型 L3 的截尾（|值| > 10 记 10，并计被截条数）

# key, 名称, 方向, 取数说明
L3 = [
    ("total_assets", "资产总额", "pos", "total_assets > 0"),
    ("employees_number", "从业人员数", "pos", "employees_number > 0"),
    ("profit_margin", "营收利润率", "pos", "total_profit / operating_revenue（revenue>0）"),
    ("debt_ratio", "资产负债率", "neg", "total_liabilities / total_assets（assets>0）"),
    ("asset_turnover", "总资产周转率", "pos", "operating_revenue / total_assets（assets>0）"),
    ("revenue", "销售收入", "pos", "operating_revenue > 0"),
]

L3_MISSING = [
    {"key": "bachelor_share", "name": "本科及以上学历占比",
     "status": "无字段", "evidence": "全库 6,312 列无学历结构列（edu/degree/本科 仅命中司法案件与学者表）"},
    {"key": "rd_staff_share", "name": "研发人员占比",
     "status": "整列为空", "evidence": "dwd_org_annual_financial_info.development_employee 0 行有值（DATA_FACTS §3.51）"},
    {"key": "market_share", "name": "市场占有率",
     "status": "无行业分母（仅 15 行药品市场）", "evidence": "dwd_market 15 行 / market_share 列；无同行业营收汇总面"},
]


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def num(x):
    if x is None:
        return None
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return v


def main():
    base = load("base_20261021.json")
    fam = load("supply_family_20261023.json")
    org_credit = {r[0]: r[1] for r in base if r[0] and r[1]}
    credit_chain = fam["credit_chain_base"]

    sys.path.insert(0, HERE)
    from _gkxdb import gkx

    cur = gkx()
    cur.execute("SET SESSION max_execution_time=0")
    cur.execute("SELECT org_id, name_cn, year, total_assets, total_liabilities, "
                "operating_revenue, total_profit, employees_number "
                "FROM gkx.dwd_org_annual_financial_info WHERE is_deleted=0")

    rows = []
    while True:
        chunk = cur.fetchmany(20000)
        if not chunk:
            break
        rows.extend(chunk)

    stats = {
        "rows": len(rows),
        "distinct_orgs": len({r[0] for r in rows}),
        "orgs_in_base": 0,
        "orgs_with_chain": 0,
        "rows_used": 0,
        "clip_counts": {},
        "fill": {},
    }

    # 列级填充（非空 / >0 / >0 主体数），用于与同族已交付件对账（v6 §九）
    col_idx = {"total_assets": 3, "total_liabilities": 4, "operating_revenue": 5,
               "total_profit": 6, "employees_number": 7}
    for col, ix in col_idx.items():
        nn = pos = 0
        pos_orgs = set()
        for r in rows:
            v = num(r[ix])
            if v is None:
                continue
            nn += 1
            if v > 0:
                pos += 1
                pos_orgs.add(r[0])
        stats["fill"][col] = {"notnull_rows": nn, "positive_rows": pos,
                              "positive_orgs": len(pos_orgs),
                              "share_of_rows_pct": round(pos / max(1, len(rows)) * 100, 2)}

    # 逐行算 L3 原值
    recs = []
    for org_id, name, year, ta, tl, rev, tp, emp in rows:
        org_id = (org_id or "").strip()
        if not org_id:
            continue
        ta, tl, rev, tp, emp = map(num, (ta, tl, rev, tp, emp))
        y = int(year) if year is not None else None
        v = {}
        if ta is not None and ta > 0:
            v["total_assets"] = ta
        if emp is not None and emp > 0:
            v["employees_number"] = emp
        if rev is not None and rev > 0 and tp is not None:
            v["profit_margin"] = tp / rev
        if ta is not None and ta > 0 and tl is not None:
            v["debt_ratio"] = tl / ta
        if ta is not None and ta > 0 and rev is not None:
            v["asset_turnover"] = rev / ta
        if rev is not None and rev > 0:
            v["revenue"] = rev
        if not v:
            continue
        # 比率型截尾
        for k in ("profit_margin", "debt_ratio", "asset_turnover"):
            if k in v and abs(v[k]) > RATIO_CLIP:
                v[k] = RATIO_CLIP if v[k] > 0 else -RATIO_CLIP
                stats["clip_counts"][k] = stats["clip_counts"].get(k, 0) + 1
        cc = org_credit.get(org_id)
        chain = credit_chain.get(cc, {}).get("chain") if cc else None
        recs.append({"org_id": org_id, "name": (name or "").strip(), "year": y,
                     "chain": chain, "v": v})

    stats["rows_used"] = len(recs)
    stats["orgs_in_base"] = len({r["org_id"] for r in recs if r["org_id"] in org_credit})
    stats["orgs_with_chain"] = len({r["org_id"] for r in recs if r["chain"]})

    # 每企业取「L3 覆盖最广」的一年（并列取较晚年份）。
    # 不用「绝对最新年」：年报各年填的列不同，取最新年会把只在前几年披露过的 L3 丢掉
    # （实测：取最新年只剩 531 家有资产总额，取覆盖最广年可恢复到 1,000+）。
    oy = {}
    for r in recs:
        if r["year"] is None:
            continue
        key = (r["org_id"], r["year"])
        tgt = oy.setdefault(key, {"org_id": r["org_id"], "name": r["name"],
                                  "year": r["year"], "chain": r["chain"], "v": {}})
        for k, val in r["v"].items():
            tgt["v"].setdefault(k, val)
        if not tgt["chain"] and r["chain"]:
            tgt["chain"] = r["chain"]
    merged = {}
    for (org_id, year), r in oy.items():
        cur_best = merged.get(org_id)
        if cur_best is None or len(r["v"]) > len(cur_best["v"]) or (
                len(r["v"]) == len(cur_best["v"]) and year > cur_best["year"]):
            merged[org_id] = r

    # 年度 × 列填充（解释「为什么可判企业集中在 2013—2015」）
    year_fill = {}
    for r in recs:
        if r["year"] is None:
            continue
        y = str(r["year"])
        cell = year_fill.setdefault(y, {"rows": 0, **{k: 0 for k, _, _, _ in L3}})
        cell["rows"] += 1
        for k in r["v"]:
            cell[k] += 1
    stats["year_fill"] = dict(sorted(year_fill.items()))

    def judge_set(mm):
        cells = {}
        for r in mm.values():
            if not r["chain"]:
                continue
            for k, val in r["v"].items():
                cells.setdefault((r["chain"], r["year"], k), []).append(val)
        cs_map = {(ch, y, k): {"n": len(v), "mean": sum(v) / len(v)}
                  for (ch, y, k), v in cells.items()}
        per = {k: {"n_values": 0, "n_orgs": 0, "n_judged": 0, "cells": 0, "cells_ok": 0}
               for k, _, _, _ in L3}
        jd = {}
        for r in mm.values():
            if not r["chain"]:
                continue
            cnt, bits, n_ok = 0, [], 0
            for k, name, direction, _ in L3:
                if k not in r["v"]:
                    continue
                per[k]["n_values"] += 1
                cs = cs_map.get((r["chain"], r["year"], k))
                if not cs or cs["n"] < MIN_PEERS:
                    continue
                per[k]["n_judged"] += 1
                n_ok += 1
                worse = (r["v"][k] > cs["mean"]) if direction == "neg" else (r["v"][k] < cs["mean"])
                if worse:
                    cnt += 1
                    bits.append(k)
            if n_ok:
                jd[r["org_id"]] = {"org_id": r["org_id"], "name": r["name"],
                                   "chain": r["chain"], "year": r["year"],
                                   "shortboard_count": cnt, "bits": bits,
                                   "n_l3_judged": n_ok}
        for k in per:
            per[k]["n_orgs"] = len({r["org_id"] for r in mm.values()
                                    if k in r["v"] and r["chain"]})
        for (ch, y, k), cs in cs_map.items():
            if k in per:
                per[k]["cells"] += 1
                if cs["n"] >= MIN_PEERS:
                    per[k]["cells_ok"] += 1
        return jd, per, cs_map

    judged, per_l3, cell_stats = judge_set(merged)

    # 敏感性：换成「绝对最新年」口径（每企业取有 L3 值的最大年份）
    latest = {}
    for (org_id, year), r in oy.items():
        if org_id not in latest or year > latest[org_id]["year"]:
            latest[org_id] = r
    judged_latest, _, _ = judge_set(latest)
    variant = {
        "rule": "每企业取有 L3 值的最大年份（不挑覆盖最广年）",
        "orgs_judged": len(judged_latest),
        "shortboard_count_avg": round(
            sum(x["shortboard_count"] for x in judged_latest.values()) / len(judged_latest), 3)
        if judged_latest else None,
        "dist": {str(c): sum(1 for x in judged_latest.values() if x["shortboard_count"] == c)
                 for c in range(len(L3) + 1)},
    }

    dist = {}
    for r in judged.values():
        key = str(r["shortboard_count"])
        dist[key] = dist.get(key, 0) + 1
    by_chain = {}
    by_year = {}
    for r in judged.values():
        by_chain[r["chain"]] = by_chain.get(r["chain"], 0) + 1
        by_year[str(r["year"])] = by_year.get(str(r["year"]), 0) + 1
    stats["orgs_with_chain"] = len({r["org_id"] for r in merged.values() if r["chain"]})
    n_judged = len(judged)
    avg = round(sum(r["shortboard_count"] for r in judged.values()) / n_judged, 3) if n_judged else None
    top = sorted(judged.values(), key=lambda x: (-x["shortboard_count"], x["name"]))[:20]
    zero = sum(1 for r in judged.values() if r["shortboard_count"] == 0)

    # 同链同年 cell 规模分布
    cell_sizes = {}
    for (ch, y, k), cs in cell_stats.items():
        if k == "total_assets":
            cell_sizes[f"{ch}|{y}"] = cs["n"]

    years = sorted({r["year"] for r in merged.values() if r["year"] is not None})
    judged_years = sorted({r["year"] for r in judged.values() if r["year"] is not None})

    out = {
        "metric_id": "M_ENT_SHORTBOARD_COUNT",
        "metric_name": "短板指标数",
        "support_judgment": "部分支持",
        "judgment_reason": (
            "九个 L3 里 6 项可从 gkx 年报财务表算出、3 项无原料（学历无字段 / 研发人员整列为空 / "
            "市占率仅 15 行），且能判定的企业只占底册的极小比例；同链同年均值在本库是小样本，"
            "按 min_peers=5 有大量 cell 不判。结构与数据都在，但覆盖不足 → 部分支持。"),
        "verdict_kind": "partial_evidence",
        "formula": "shortboard_count_i = COUNT(L3_j | x_ij 存在 AND 同链同年均值存在(n>=5) AND 方向判定为更差)",
        "params": {"min_peers": MIN_PEERS, "ratio_clip": RATIO_CLIP,
                   "peer_key": "chain_code + year", "year_rule": "widest_l3_coverage_year"},
        "base_years_used": judged_years,
        "base_years_missing": [],
        "base_years_note": (
            "本件是截面口径（每企业取 L3 覆盖面最广的一年，并列取较晚年），不是多期均值；"
            f"财报表年份覆盖 {'—'.join(str(y) for y in (min(years), max(years)))}，"
            f"判定实际落到 {judged_years}。没有任何年份被按 0 摊进分母。"),
        "coverage": stats,
        "l3_available": per_l3,
        "l3_missing": L3_MISSING,
        "totals": {
            "orgs_with_any_l3": len(merged),
            "orgs_judged": n_judged,
            "orgs_shortboard_zero": zero,
            "share_zero_pct": round(zero / n_judged * 100, 2) if n_judged else None,
            "shortboard_count_avg": avg,
            "dist": dict(sorted(dist.items(), key=lambda kv: int(kv[0]))),
            "max_possible": len(L3),
            "chain_year_cells_total_assets": len(cell_sizes),
            "judged_by_chain": dict(sorted(by_chain.items(), key=lambda kv: -kv[1])),
            "judged_by_year": dict(sorted(by_year.items())),
        },
        "variant_latest_year": variant,
        "peer_cell_sizes_total_assets": dict(sorted(cell_sizes.items(),
                                                     key=lambda kv: -kv[1])[:24]),
        "top20": top,
        "sources": {
            "db": "gkx @ 183.240.141.251:3318",
            "tables": ["gkx.dwd_org_annual_financial_info", "gkx.dwd_market",
                       "gkx.dwd_org_base_info", "gkx.dwd_org_industry_tags"],
            "snapshots": ["code/_snapshots21/base_20261021.json",
                          "code/_snapshots21/supply_family_20261023.json"],
        },
        "generated_at": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print(json.dumps({k: out[k] for k in ("support_judgment", "coverage", "totals")},
                     ensure_ascii=False, indent=1))
    print("per_l3", json.dumps(per_l3, ensure_ascii=False))
    print("saved", OUT)


if __name__ == "__main__":
    main()
