#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M_SVC_RELATION_RISK｜服务关系风险

零 DB：只读 code/_snapshots21/svc21_facts_20261022.json + 阻塞表负证据快照。

口径：
  - 风险主体 = 服务机构池 44,153 家中，在 dwd_org_company_punish（行政处罚）或
    dwd_org_risk_shixin（失信被执行人）至少命中一条的机构（快照 risk 段）。
  - 风险传导 = 只在「已知边」上做一跳：边集与 M_SVC_RELATION_DENSITY 完全一致
    （池内两端可解析的投资边 + 股东边，无向去重）。
  - 风险暴露 = 非风险机构中存在至少一个风险邻居（一跳）。
  - 二跳暴露单列，仅作旁证，不进入主口径的分母。

复现：cd code && python3 M_SVC_RELATION_RISK.py
"""
from __future__ import annotations

import json
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_SVC_RELATION_RISK_out.json")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
PROBE = os.path.join(HERE, "_probe_blocked_f2_20261023.json")

ID = "M_SVC_RELATION_RISK"


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    d = load(FACTS)
    pool = d["pool"]
    pool_ids = set(pool)
    risk = d["risk"]
    risky = set(risk)

    # 风险类型
    shixin = {k for k, v in risk.items() if v.get("shixin", 0) > 0}
    punish = {k for k, v in risk.items() if v.get("punish", 0) > 0}
    both = shixin & punish
    only_shixin = shixin - punish
    only_punish = punish - shixin
    shixin_records = sum(v.get("shixin", 0) for v in risk.values())
    punish_records = sum(v.get("punish", 0) for v in risk.values())
    max_records = max(sum(v.values()) for v in risk.values())

    # 边集
    edges = set()
    for e in d["invest_edges"] + d["shareholder_edges"]:
        a, b = e[0], e[1]
        if a in pool_ids and b in pool_ids and a != b:
            edges.add(tuple(sorted((a, b))))
    E = len(edges)

    adj = defaultdict(set)
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)

    rr = mixed = clean = 0
    exposed = set()
    for a, b in edges:
        ra, rb = a in risky, b in risky
        if ra and rb:
            rr += 1
        elif ra or rb:
            mixed += 1
            exposed.add(b if ra else a)
        else:
            clean += 1

    risky_active = {n for n in adj if n in risky}
    clean_active = {n for n in adj if n not in risky}

    # 二跳：一跳暴露节点再向外一跳（不含风险主体本身、不含一跳暴露）
    two_hop = set()
    for n in exposed:
        for m in adj[n]:
            if m not in risky and m not in exposed:
                two_hop.add(m)

    # 风险类型组合（一跳暴露节点）
    exposure_type = Counter()
    for n in exposed:
        kinds = []
        for m in adj[n]:
            v = risk.get(m)
            if not v:
                continue
            if v.get("shixin"):
                kinds.append("shixin")
            if v.get("punish"):
                kinds.append("punish")
        if "shixin" in kinds and "punish" in kinds:
            exposure_type["两类均有"] += 1
        elif "shixin" in kinds:
            exposure_type["仅失信"] += 1
        elif "punish" in kinds:
            exposure_type["仅处罚"] += 1

    # 城市切片
    def city(nid):
        return (pool.get(nid) or {}).get("city") or "（空）"

    city_rows = []
    for c in ("深圳市", "广州市", "东莞市", "惠州市"):
        nodes = {n for n in pool_ids if city(n) == c}
        r = nodes & risky
        ex = {n for n in exposed if city(n) == c}
        city_rows.append({
            "city": c,
            "nodes": len(nodes),
            "risky": len(r),
            "shixin": len(nodes & shixin),
            "punish": len(nodes & punish),
            "exposed_clean": len(ex),
        })

    out = {
        "metric": ID,
        "metric_name": "服务关系风险",
        "support_judgment": "部分支持",
        "verdict_kind": "partial_with_gaps",
        "generated_at": "2026-10-23T04:42:00+08:00",
        "sources": {
            "db": "gkx",
            "host": "183.240.141.251:3318",
            "user": "gkx_reader_zp",
            "mode": "read-only",
            "tables": [
                "gkx.dwd_org_company_punish",
                "gkx.dwd_org_risk_shixin",
                "gkx.dwd_org_invest_info",
                "gkx.dwd_org_shareholder_info",
                "gkx.dwd_org_org_product_info",
            ],
            "snapshots": [
                "code/_snapshots21/svc21_facts_20261022.json",
                "code/_probe_blocked_f2_20261023.json",
            ],
            "demo_used": False,
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "行政处罚与失信被执行均为存量累计口径（表内无可靠事件年份），本件不按年切片；风险率是快照日截面。",
        "population": {
            "pool_n": len(pool_ids),
            "risky_n": len(risky),
            "shixin_n": len(shixin),
            "punish_n": len(punish),
            "both_n": len(both),
            "only_shixin_n": len(only_shixin),
            "only_punish_n": len(only_punish),
            "shixin_records_in_pool": shixin_records,
            "punish_records_in_pool": punish_records,
            "max_records_single_org": max_records,
            "clean_pool_n": len(pool_ids) - len(risky),
        },
        "edges": {
            "undirected_internal_edges": E,
            "risk_risk_edges": rr,
            "mixed_edges": mixed,
            "clean_clean_edges": clean,
            "risky_active_nodes": len(risky_active),
            "clean_active_nodes": len(clean_active),
        },
        "exposure": {
            "exposed_clean_n": len(exposed),
            "two_hop_clean_n": len(two_hop),
            "exposure_type": dict(exposure_type),
        },
        "city_slices": city_rows,
        "derived": {
            "risk_rate_pct": {
                "value": round(len(risky) / len(pool_ids) * 100, 4),
                "numerator": len(risky),
                "denominator": len(pool_ids),
                "denominator_note": "分子=池内至少命中一条处罚或失信记录的机构数 population.risky_n，分母=服务机构池家数 population.pool_n",
            },
            "shixin_rate_pct": {
                "value": round(len(shixin) / len(pool_ids) * 100, 4),
                "numerator": len(shixin),
                "denominator": len(pool_ids),
                "denominator_note": "分子=池内失信被执行机构数 population.shixin_n，分母=服务机构池家数 population.pool_n",
            },
            "punish_rate_pct": {
                "value": round(len(punish) / len(pool_ids) * 100, 4),
                "numerator": len(punish),
                "denominator": len(pool_ids),
                "denominator_note": "分子=池内行政处罚机构数 population.punish_n，分母=服务机构池家数 population.pool_n",
            },
            "both_share_of_risky_pct": {
                "value": round(len(both) / len(risky) * 100, 4),
                "numerator": len(both),
                "denominator": len(risky),
                "denominator_note": "分子=同时有处罚与失信的机构数 population.both_n，分母=风险机构数 population.risky_n",
            },
            "risk_risk_edge_share_pct": {
                "value": round(rr / E * 100, 4),
                "numerator": rr,
                "denominator": E,
                "denominator_note": "分子=两端均风险的无向边数 edges.risk_risk_edges，分母=池内无向边总数 edges.undirected_internal_edges",
            },
            "mixed_edge_share_pct": {
                "value": round(mixed / E * 100, 4),
                "numerator": mixed,
                "denominator": E,
                "denominator_note": "分子=一端风险的边数 edges.mixed_edges，分母=池内无向边总数 edges.undirected_internal_edges",
            },
            "clean_edge_share_pct": {
                "value": round(clean / E * 100, 4),
                "numerator": clean,
                "denominator": E,
                "denominator_note": "分子=两端均无风险记录的边数 edges.clean_clean_edges，分母=池内无向边总数 edges.undirected_internal_edges",
            },
            "exposure_rate_active_clean_pct": {
                "value": round(len(exposed) / len(clean_active) * 100, 4),
                "numerator": len(exposed),
                "denominator": len(clean_active),
                "denominator_note": "分子=一跳暴露的非风险机构数 exposure.exposed_clean_n，分母=有边的非风险机构数 edges.clean_active_nodes",
            },
            "exposure_rate_all_clean_pct": {
                "value": round(len(exposed) / (len(pool_ids) - len(risky)) * 100, 4),
                "numerator": len(exposed),
                "denominator": len(pool_ids) - len(risky),
                "denominator_note": "分子=一跳暴露的非风险机构数 exposure.exposed_clean_n，分母=池内非风险机构数（pool_n − risky_n）",
            },
            "two_hop_over_one_hop_x": {
                "value": round(len(two_hop) / len(exposed), 4) if exposed else None,
                "numerator": len(two_hop),
                "denominator": len(exposed),
                "denominator_note": "分子=二跳新增的非风险机构数 exposure.two_hop_clean_n，分母=一跳暴露机构数 exposure.exposed_clean_n（倍率）",
            },
            "sz_risk_share_of_all_risky_pct": {
                "value": round(city_rows[0]["risky"] / len(risky) * 100, 4),
                "numerator": city_rows[0]["risky"],
                "denominator": len(risky),
                "denominator_note": "分子=深圳风险机构数 city_slices[深圳市].risky，分母=池内风险机构总数 population.risky_n",
            },
            "risky_active_share_pct": {
                "value": round(len(risky_active) / len(risky) * 100, 4),
                "numerator": len(risky_active),
                "denominator": len(risky),
                "denominator_note": "分子=有边的风险机构数 edges.risky_active_nodes，分母=风险机构数 population.risky_n",
            },
            "clean_active_share_pct": {
                "value": round(len(clean_active) / (len(pool_ids) - len(risky)) * 100, 4),
                "numerator": len(clean_active),
                "denominator": len(pool_ids) - len(risky),
                "denominator_note": "分子=有边的非风险机构数 edges.clean_active_nodes，分母=池内非风险机构数（pool_n − risky_n）",
            },
            "two_hop_over_all_clean_pct": {
                "value": round(len(two_hop) / (len(pool_ids) - len(risky)) * 100, 4),
                "numerator": len(two_hop),
                "denominator": len(pool_ids) - len(risky),
                "denominator_note": "分子=二跳新增的非风险机构数 exposure.two_hop_clean_n，分母=池内非风险机构数（pool_n − risky_n）",
            },
            "only_punish_share_of_exposed_pct": {
                "value": round(exposure_type["仅处罚"] / len(exposed) * 100, 4),
                "numerator": exposure_type["仅处罚"],
                "denominator": len(exposed),
                "denominator_note": "分子=只通过处罚主体暴露的机构数 exposure.exposure_type.仅处罚，分母=一跳暴露机构数 exposure.exposed_clean_n",
            },
            "only_shixin_share_of_exposed_pct": {
                "value": round(exposure_type["仅失信"] / len(exposed) * 100, 4),
                "numerator": exposure_type["仅失信"],
                "denominator": len(exposed),
                "denominator_note": "分子=只通过失信主体暴露的机构数 exposure.exposure_type.仅失信，分母=一跳暴露机构数 exposure.exposed_clean_n",
            },
            "both_kinds_share_of_exposed_pct": {
                "value": round(exposure_type["两类均有"] / len(exposed) * 100, 4),
                "numerator": exposure_type["两类均有"],
                "denominator": len(exposed),
                "denominator_note": "分子=同时通过处罚与失信主体暴露的机构数 exposure.exposure_type.两类均有，分母=一跳暴露机构数 exposure.exposed_clean_n",
            },
            "shixin_records_per_risky": {
                "value": round(shixin_records / len(shixin) * 1.0, 4),
                "numerator": shixin_records,
                "denominator": len(shixin),
                "denominator_note": "分子=池内失信被执行记录行数 population.shixin_records_in_pool，分母=失信机构数 population.shixin_n（条/家）",
            },
            "punish_records_per_punish": {
                "value": round(punish_records / len(punish), 4),
                "numerator": punish_records,
                "denominator": len(punish),
                "denominator_note": "分子=池内行政处罚记录行数 population.punish_records_in_pool，分母=受处罚机构数 population.punish_n（条/家）",
            },
            "city_risk_rate_sz_pct": {
                "value": round(city_rows[0]["risky"] / city_rows[0]["nodes"] * 100, 4),
                "numerator": city_rows[0]["risky"],
                "denominator": city_rows[0]["nodes"],
                "denominator_note": "分子=深圳风险机构数 city_slices[深圳市].risky，分母=深圳池家数 city_slices[深圳市].nodes",
            },
            "city_risk_rate_gz_pct": {
                "value": round(city_rows[1]["risky"] / city_rows[1]["nodes"] * 100, 4),
                "numerator": city_rows[1]["risky"],
                "denominator": city_rows[1]["nodes"],
                "denominator_note": "分子=广州风险机构数 city_slices[广州市].risky，分母=广州池家数 city_slices[广州市].nodes",
            },
            "city_risk_rate_dg_pct": {
                "value": round(city_rows[2]["risky"] / city_rows[2]["nodes"] * 100, 4),
                "numerator": city_rows[2]["risky"],
                "denominator": city_rows[2]["nodes"],
                "denominator_note": "分子=东莞风险机构数 city_slices[东莞市].risky，分母=东莞池家数 city_slices[东莞市].nodes",
            },
            "city_risk_rate_hz_pct": {
                "value": round(city_rows[3]["risky"] / city_rows[3]["nodes"] * 100, 4),
                "numerator": city_rows[3]["risky"],
                "denominator": city_rows[3]["nodes"],
                "denominator_note": "分子=惠州风险机构数 city_slices[惠州市].risky，分母=惠州池家数 city_slices[惠州市].nodes",
            },
            "only_punish_share_of_risky_pct": {
                "value": round(len(only_punish) / len(risky) * 100, 4),
                "numerator": len(only_punish),
                "denominator": len(risky),
                "denominator_note": "分子=仅处罚机构数 population.only_punish_n，分母=风险机构数 population.risky_n",
            },
            "only_shixin_share_of_risky_pct": {
                "value": round(len(only_shixin) / len(risky) * 100, 4),
                "numerator": len(only_shixin),
                "denominator": len(risky),
                "denominator_note": "分子=仅失信机构数 population.only_shixin_n，分母=风险机构数 population.risky_n",
            },
            "unexposed_risky_share_pct": {
                "value": round((len(risky) - len(risky_active)) / len(risky) * 100, 4),
                "numerator": len(risky) - len(risky_active),
                "denominator": len(risky),
                "denominator_note": "分子=无股权边的风险机构数（population.risky_n − edges.risky_active_nodes），分母=风险机构数 population.risky_n",
            },
            "sz_exposed_share_of_all_exposed_pct": {
                "value": round(city_rows[0]["exposed_clean"] / len(exposed) * 100, 4),
                "numerator": city_rows[0]["exposed_clean"],
                "denominator": len(exposed),
                "denominator_note": "分子=深圳一跳暴露机构数 city_slices[深圳市].exposed_clean，分母=池内一跳暴露机构总数 exposure.exposed_clean_n",
            },
        },
        "absence_probe": {
            "file": "code/_probe_blocked_f2_20261023.json",
            "blocked": [
                {"table": r["table"],
                 "gkx_exists": r["gkx_information_schema"]["exists"],
                 "live_demo_row_class": ("全量装载" if (r["live_where"].get("rows") or 0) >= 10000 else "样例级"),
                 "verdict": r["live_where"].get("verdict")}
                for r in load(PROBE).get("blocked", [])
                if r["table"] in ("enterprise_cooperation", "enterprise_supply_chain",
                                  "svc_org_circle", "svc_org_card")
            ],
        },
        "rejected_dimensions": [
            {
                "dimension": "合作关系风险传导",
                "reason": "gkx 无 enterprise_cooperation（information_schema 命中 0 表），合作边不存在；演示库同名表为全量装载，铁律禁引，不构成支持",
                "alternative": "投资/股东边一跳暴露",
                "difference": "股权关系不等于业务合作，风险沿股权的传导只覆盖控制/参股链，漏掉合作方与客户；暴露率不可外推为「合作风险率」",
            },
            {
                "dimension": "供应链风险传导",
                "reason": "gkx 无 enterprise_supply_chain（0 表），供应商/客户关系无承载",
                "alternative": "无（本维拒拟）",
                "difference": "替代口径无法覆盖上下游停摆风险，只能作股权关联风险",
            },
            {
                "dimension": "风险事件时间序列与处置进度",
                "reason": "处罚/失信表无可靠事件日期与结案状态列，gkx 无 svc_metric_series",
                "alternative": "存量计数",
                "difference": "只能回答「有没有记录」，不能回答「何时发生、是否已修复」",
            },
        ],
        "gaps": [
            "风险口径只覆盖行政处罚与失信被执行，不纳入经营异常、司法执行、税务处罚等其他风险类表（不在本件 calc-logic 范围）",
            "股权边 95.64% 只有一端可解析，传导覆盖不完整",
            "风险记录无事件日期，无法区分历史已修复与当前仍在",
        ],
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"risky={len(risky)} shixin={len(shixin)} punish={len(punish)} edges={E} "
          f"mixed={mixed} exposed={len(exposed)} twohop={len(two_hop)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
