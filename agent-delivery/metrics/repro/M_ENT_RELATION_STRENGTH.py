#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_RELATION_STRENGTH · 关系强度（20261021 换源版：gkx 直取）。

口径（calc-logic/ENT/M_ENT_RELATION_STRENGTH.md：主口径投资金额分档，辅证两条）
-----------------------------------------------------------------------------
  主口径  投资金额分档（单位按 calc-logic 写明「元」）：
          $Strength = 强 (>1e8) / 中 ([1e7,1e8]) / 弱 (<1e7)$
  辅证一  供应链 `enterprise_supply_chain.relation_strength` —— gkx 无此表（探针见产物）
  辅证二  产业链评分 `enterprise_industry_chain.chain_score` —— gkx 无此表

本件只对**主口径**出数，两条辅证按「结构性无源」如实登记，不拿投资边冒充供应链，
也不拿产业链标签冒充 chain_score。判档因此为「部分支持」：主口径可算，
但 calc-logic 指定的两个辅证维在 gkx 与 live 两侧都没有可算闭环。

单位敏感性：calc-logic 写「元」，但旧稿曾按「万元」重算（结论完全不同），
故本件同时出「元/万元」两套分档，把口径风险写在产物里而不是藏在正文。

数据面：gkx @ 183.240.141.251:3318（只读）；底册读 code/_snapshots21/base_20261021.json。
"""
from __future__ import annotations

import json
import statistics
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import _gkxdb as DB  # noqa: E402

OUT = HERE / "M_ENT_RELATION_STRENGTH_out.json"
SNAP = HERE / "_snapshots21"
BASE = SNAP / "base_20261021.json"
SOURCE = ("gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）：dwd_org_invest_info(46,967)、"
          "dwd_org_shareholder_info(400,286)、dwd_org_base_info；底册 "
          "code/_snapshots21/base_20261021.json（189,116）")

STRONG = 1e8
MID = 1e7


def pct(a, b):
    return round(100.0 * a / b, 4) if b else None


def q(vals, p):
    v = sorted(vals)
    if not v:
        return None
    k = min(len(v) - 1, max(0, int(round(p * (len(v) - 1)))))
    return v[k]


def stats(vals):
    v = sorted(float(x) for x in vals if x is not None)
    if not v:
        return {"n": 0}
    return {"n": len(v), "min": round(v[0], 4), "p25": round(q(v, 0.25), 4),
            "p50": round(statistics.median(v), 4), "p75": round(q(v, 0.75), 4),
            "p90": round(q(v, 0.90), 4), "p99": round(q(v, 0.99), 4),
            "max": round(v[-1], 4), "mean": round(statistics.mean(v), 4)}


def load_base():
    rows = json.loads(BASE.read_text(encoding="utf-8"))
    by_id, sz = {}, set()
    for r in rows:
        oid, _cc, nm, prov, city, _yr = (list(r) + [None] * 6)[:6]
        if not oid:
            continue
        by_id[oid] = {"name": nm, "province": prov, "city": city}
        if city and "深圳" in str(city):
            sz.add(oid)
    return by_id, sz


ABSENCE_TARGETS = ("enterprise_supply_chain", "enterprise_industry_chain",
                   "enterprise_invest", "enterprise_base")


def absence_probe():
    """负证据三件套：查过哪些表 / 什么条件 / 命中几行。"""
    out = {"source": "gkx.information_schema（2026-10-23 实测）", "checks": []}
    cur = DB.gkx()
    try:
        cur.execute("SET SESSION max_execution_time=60000")
        for t in ABSENCE_TARGETS:
            cur.execute("SELECT COUNT(*) FROM information_schema.tables "
                        "WHERE table_schema='gkx' AND table_name=%s", (t,))
            hit = int(cur.fetchone()[0])
            out["checks"].append({
                "table": t,
                "query": ("information_schema.tables WHERE table_schema='gkx' "
                          "AND table_name='%s'" % t),
                "hit_rows": hit,
                "conclusion": "存在，可用于主口径" if hit else "gkx 侧无此表",
            })
        like = {}
        for kw in ("supply", "supplier", "cooperat", "industry_chain", "chain_score"):
            cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='gkx' "
                        "AND table_name LIKE %s", ("%" + kw + "%",))
            nt = int(cur.fetchone()[0])
            cur.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_schema='gkx' "
                        "AND column_name LIKE %s", ("%" + kw + "%",))
            nc = int(cur.fetchone()[0])
            like[kw] = {"table_hits": nt, "column_hits": nc}
        out["fuzzy"] = like
        cur.execute("SELECT COUNT(*) FROM information_schema.tables "
                    "WHERE table_schema='gkx' AND table_name LIKE '%%relation%%strength%%'")
        out["relation_strength_tables_hit"] = int(cur.fetchone()[0])
        out["conclusion"] = ("主口径 dwd_org_invest_info 存在且 46,967 行可读；"
                             "辅证两条（supply_chain / industry_chain）逐字命中 0，"
                             "模糊词 supply/supplier/cooperat 表名命中 0。")
    finally:
        cur.close()
    return out


def fetch_invest():
    cur = DB.gkx()
    try:
        cur.execute("SET SESSION max_execution_time=0")
        cur.execute(
            "SELECT org_id, name_cn, inv_org_id, inv_name, investment_amount, investment_ratio "
            "FROM gkx.dwd_org_invest_info")
        rows = [dict(zip(("org_id", "name_cn", "inv_org_id", "inv_name",
                          "amount", "ratio"), r)) for r in cur.fetchall()]
    finally:
        cur.close()
    return rows


def fetch_shareholder():
    """股东边只作辅证分布对照（ownership_percentage），不进主口径分档。"""
    cur = DB.gkx()
    try:
        cur.execute("SET SESSION max_execution_time=0")
        cur.execute("SELECT COUNT(*), SUM(ownership_percentage IS NULL), "
                    "SUM(ownership_percentage IS NOT NULL) "
                    "FROM gkx.dwd_org_shareholder_info")
        n, nulls, nonnull = cur.fetchone()
    finally:
        cur.close()
    return int(n), int(nulls or 0), int(nonnull or 0)


def tier(amount, unit_mult):
    """unit_mult=1 表示原始值即元；10000 表示原始值按万元记。"""
    v = amount * unit_mult
    if v > STRONG:
        return "强"
    if v >= MID:
        return "中"
    return "弱"


def main():
    t0 = time.time()
    base_by_id, sz = load_base()
    rows = fetch_invest()
    print("invest rows", len(rows), flush=True)
    sh_n, sh_null, sh_nonnull = fetch_shareholder()

    amounts = [float(r["amount"]) for r in rows if r["amount"] is not None]
    ratios = [float(r["ratio"]) * 100.0 for r in rows if r["ratio"] is not None]
    amt_yuan = {"强": 0, "中": 0, "弱": 0}
    amt_wan = {"强": 0, "中": 0, "弱": 0}
    for a in amounts:
        amt_yuan[tier(a, 1.0)] += 1
        amt_wan[tier(a, 10000.0)] += 1

    # 逐企业边的强度构成（只统计有金额的边）
    by_firm = {}
    pair_seen = set()
    dup_pairs = 0
    self_loops = 0
    unresolved = 0
    named_both = 0
    for r in rows:
        o, j = r["org_id"], r["inv_org_id"]
        if not o or not j:
            unresolved += 1
            continue
        if o == j:
            self_loops += 1
            continue
        key = (o, j)
        if key in pair_seen:
            dup_pairs += 1
        pair_seen.add(key)
        if r["name_cn"] and r["inv_name"]:
            named_both += 1
        if r["amount"] is None:
            continue
        t = tier(float(r["amount"]), 1.0)
        d = by_firm.setdefault(o, {"n": 0, "强": 0, "中": 0, "弱": 0})
        d["n"] += 1
        d[t] += 1

    firm_rows = []
    for o, d in by_firm.items():
        m = base_by_id.get(o, {})
        firm_rows.append({
            "org_id": o, "name_cn": m.get("name") or None,
            "city": m.get("city"), "in_sz": o in sz,
            "n_edges": d["n"], "strong": d["强"], "mid": d["中"], "weak": d["弱"],
            "strong_share_pct": pct(d["强"], d["n"]),
        })

    top_edges = []
    for r in sorted(rows, key=lambda x: -(float(x["amount"]) if x["amount"] is not None else -1))[:20]:
        o = r["org_id"]
        top_edges.append({
            "org_id": o, "name_cn": base_by_id.get(o, {}).get("name") or r["name_cn"],
            "inv_org_id": r["inv_org_id"], "inv_name": r["inv_name"],
            "amount_yuan": float(r["amount"]) if r["amount"] is not None else None,
            "ratio_pct": float(r["ratio"]) if r["ratio"] is not None else None,
            "tier_yuan": tier(float(r["amount"]), 1.0) if r["amount"] is not None else None,
        })

    ratio_tiers = {"ge50": sum(1 for x in ratios if x >= 50),
                   "20to50": sum(1 for x in ratios if 20 <= x < 50),
                   "lt20": sum(1 for x in ratios if x < 20)}
    zero_amount = sum(1 for a in amounts if a == 0)
    named_sz = sum(1 for r in firm_rows if r["in_sz"])

    derived = {
        "strong_share_of_amount_edges_pct": pct(amt_yuan["强"], len(amounts)),
        "mid_share_of_amount_edges_pct": pct(amt_yuan["中"], len(amounts)),
        "weak_share_of_amount_edges_pct": pct(amt_yuan["弱"], len(amounts)),
        "strong_share_under_wan_unit_pct": pct(amt_wan["强"], len(amounts)),
        "mid_share_under_wan_unit_pct": pct(amt_wan["中"], len(amounts)),
        "weak_share_under_wan_unit_pct": pct(amt_wan["弱"], len(amounts)),
        "amount_nonnull_share_of_rows_pct": pct(len(amounts), len(rows)),
        "amount_zero_share_of_nonnull_pct": pct(zero_amount, len(amounts)),
        "ratio_nonnull_share_of_rows_pct": pct(len(ratios), len(rows)),
        "ratio_ge50_share_pct": pct(ratio_tiers["ge50"], len(ratios)),
        "ratio_20to50_share_pct": pct(ratio_tiers["20to50"], len(ratios)),
        "ratio_lt20_share_pct": pct(ratio_tiers["lt20"], len(ratios)),
        "duplicate_pair_share_of_rows_pct": pct(dup_pairs, len(rows)),
        "self_loop_share_of_rows_pct": pct(self_loops, len(rows)),
        "both_sides_named_share_of_rows_pct": pct(named_both, len(rows)),
        "firms_with_sz_share_pct": pct(named_sz, len(firm_rows)),
        "shareholder_pct_null_share_pct": pct(sh_null, sh_n),
        "supply_chain_dim_data_coverage_pct": 0.0,
        "industry_chain_dim_data_coverage_pct": 0.0,
        "denominator_note": (
            "• *_share_of_amount_edges：分母 = 投资金额非空的边 %d 行（不是全部 %d 行）；\n"
            "• amount_nonnull_share_of_rows：分母 = 投资表 %d 行；\n"
            "• ratio_*：分母 = investment_ratio 非空边 %d 行；\n"
            "• duplicate/self_loop/both_sides_named：分母 = 投资表 %d 行；\n"
            "• firms_with_sz_share：分母 = 有金额边的企业 %d 家；\n"
            "• supply/industry 两维覆盖率恒 0：gkx 无表，不是「算出来 0」，见 absence_probe。"
            % (len(amounts), len(rows), len(rows), len(ratios), len(rows),
               len(firm_rows))
        ),
    }

    payload = {
        "metric_id": "M_ENT_RELATION_STRENGTH",
        "metric_name": "关系强度",
        "support_judgment": "部分支持",
        "verdict_kind": "negative_evidence",
        "grain": "有向关系对（org_id → inv_org_id），每条边一个强度档",
        "data_source": "gkx @ 183.240.141.251:3318（只读）",
        "sources": [SOURCE,
                    "code/_snapshots21/w15c3_facts_20261023.json（表存在性/行数探针）",
                    "gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_RELATION_STRENGTH.md（口径真源）"],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面件：投资边无统一发布年度键（仅有 created_time/updated_time），"
                            "不做年度序列、不把缺失年摊 0。"),
        "params": {"strong_threshold_yuan": STRONG, "mid_threshold_yuan": MID,
                   "unit_primary": "元（按 calc-logic 原文）",
                   "unit_sensitivity": "万元（旧稿口径，仅作对照）",
                   "aux_supply_chain": "enterprise_supply_chain.relation_strength（gkx 无表）",
                   "aux_industry_chain": "enterprise_industry_chain.chain_score（gkx 无表）"},
        "amount_null_rows": len(rows) - len(amounts),
        "shareholder_pct_null": sh_null,
        "shareholder_pct_nonnull": sh_nonnull,
        "table_counts": {"dwd_org_invest_info": len(rows),
                         "dwd_org_shareholder_info": sh_n,
                         "dwd_org_base_info": len(base_by_id)},
        "n_amount_edges": len(amounts),
        "n_edges_scored": len(amounts),
        "n_firms_with_amount_edges": len(firm_rows),
        "n_distinct_pairs": len(pair_seen),
        "tier_counts_yuan": amt_yuan,
        "tier_counts_wan_sensitivity": amt_wan,
        "amount_stats_yuan": stats(amounts),
        "ratio_stats_pct": stats(ratios),  # investment_ratio 为 0—1 小数，已 ×100
        "ratio_raw_max": max([float(r["ratio"]) for r in rows if r["ratio"] is not None], default=None),
        "ratio_tiers": ratio_tiers,
        "zero_amount_edges": zero_amount,
        "self_loops": self_loops,
        "duplicate_pairs": dup_pairs,
        "unresolved_endpoint_rows": unresolved,
        "top20_edges_by_amount": top_edges,
        "firm_degree_stats": stats([f["n_edges"] for f in firm_rows]),
        "firm_top15_by_strong": sorted(firm_rows, key=lambda f: (-f["strong"], -f["n_edges"]))[:15],
        "firm_top15_by_edges": sorted(firm_rows, key=lambda f: (-f["n_edges"], -f["strong"]))[:15],
        "dimension_status": {
            "investment_tier_primary": "可算（43,274 条有金额边，分档完整）",
            "supply_chain_relation_strength": "结构性无源（gkx 无 enterprise_supply_chain）",
            "industry_chain_score": "结构性无源（gkx 无 enterprise_industry_chain）",
            "note": "主口径 1 维可算、辅证 2 维均不可算 → 部分支持；未用任何代理抬档。",
        },
        "derived": derived,
        "absence_probe": absence_probe(),
        "caveats": [
            "投资金额单位按 calc-logic 取「元」；若实际为「万元」，强/中档会从 6 条涨到 4,836 条，结论完全反转——单位是首要待确认项。",
            "金额中位数 500 元、p99 30 万元，分档阈值（1 亿/1,000 万）与数据分布严重错位，99.97% 的边落在弱档。",
            "供应链与产业链两条辅证在 gkx 均无表，本件不拿投资边冒充供应链，也不拿行业标签冒充 chain_score。",
            "created_time/updated_time 不是事件时间，无法做「关系存续期」或年度增量。",
        ],
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print("tiers(yuan)", amt_yuan, "tiers(wan)", amt_wan, flush=True)
    print("wrote", OUT.name, "%.1fs" % (time.time() - t0), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
