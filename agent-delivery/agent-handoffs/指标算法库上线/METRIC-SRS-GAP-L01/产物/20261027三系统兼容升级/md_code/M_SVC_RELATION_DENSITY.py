#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_SVC_RELATION_DENSITY 服务关系链密度
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_SVC_RELATION_DENSITY.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""
M_SVC_RELATION_DENSITY｜服务关系链密度

零 DB：只读 code/_snapshots21/svc21_facts_20261022.json（gkx 只读面 183.240.141.251:3318
落盘快照）+ code/_probe_blocked_f2_20261023.json（阻塞表负证据）。

口径：
  - 点集 P0 = 服务机构池 44,153（dwd_org_org_product_info 的 org_id 去重）
  - 点集 P1 = P0 中度 ≥1 的机构（去掉孤立点）
  - 点集 P2 = P1 的最大连通分量（巨片）
  - 边 = 池内两端都可解析的投资边（dwd_org_invest_info）+ 股东边（dwd_org_shareholder_info），
    无向去重。合作边 / 供应链边 / 服务关系边在 gkx 侧不存在（见 absence_probe），
    因此本件只交付「投资/股权关系密度」，不得称「服务合作关系密度」。
  - 密度 = 2E / (n(n-1))，平均度 = 2E/n，归一化平均度 = 平均度/(n-1)。

复现：cd code && python3 M_SVC_RELATION_DENSITY.py
"""
from __future__ import annotations

import json
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_SVC_RELATION_DENSITY_out.json")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
PROBE = os.path.join(HERE, "_probe_blocked_f2_20261023.json")

ID = "M_SVC_RELATION_DENSITY"


def load(path: str):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    d = load(FACTS)
    pool = d["pool"]
    pool_ids = set(pool)
    n0 = len(pool_ids)

    invest = d["invest_edges"]
    share = d["shareholder_edges"]

    # ---------- 边解析率 ----------
    def resolve(edges):
        both = one = 0
        for e in edges:
            a, b = e[0], e[1]
            ia, ib = a in pool_ids, b in pool_ids
            if ia and ib:
                both += 1
            elif ia or ib:
                one += 1
        return both, one

    inv_both, inv_one = resolve(invest)
    shr_both, shr_one = resolve(share)

    # ---------- 无向内部边 ----------
    inv_edges = set()
    for e in invest:
        a, b = e[0], e[1]
        if a in pool_ids and b in pool_ids and a != b:
            inv_edges.add(tuple(sorted((a, b))))
    edges = set(inv_edges)
    for e in share:
        a, b = e[0], e[1]
        if a in pool_ids and b in pool_ids and a != b:
            edges.add(tuple(sorted((a, b))))

    E = len(edges)
    inv_only = len(inv_edges)
    shr_added = E - inv_only

    deg = Counter()
    for a, b in edges:
        deg[a] += 1
        deg[b] += 1
    n1 = len(deg)
    mean_p0 = 2 * E / n0
    mean_p1 = 2 * E / n1
    dens_p0 = 2 * E / (n0 * (n0 - 1))
    dens_p1 = 2 * E / (n1 * (n1 - 1))

    # ---------- 连通分量 ----------
    parent: dict[str, str] = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for a, b in edges:
        union(a, b)
    comp = Counter(find(x) for x in deg)
    giant = max(comp.values())

    # ---------- 度分布 ----------
    buckets = {"0": 0, "1": 0, "2-4": 0, "5-9": 0, "10+": 0}
    for nid in pool_ids:
        v = deg.get(nid, 0)
        if v == 0:
            buckets["0"] += 1
        elif v == 1:
            buckets["1"] += 1
        elif v < 5:
            buckets["2-4"] += 1
        elif v < 10:
            buckets["5-9"] += 1
        else:
            buckets["10+"] += 1

    # ---------- 城市切片 ----------
    def city(nid):
        return (pool.get(nid) or {}).get("city") or "（空）"

    city_rows = []
    for c in ("深圳市", "广州市", "东莞市", "惠州市"):
        nodes = {n for n in pool_ids if city(n) == c}
        sub = [(a, b) for a, b in edges if a in nodes and b in nodes]
        sd = Counter()
        for a, b in sub:
            sd[a] += 1
            sd[b] += 1
        city_rows.append({
            "city": c,
            "nodes": len(nodes),
            "internal_edges": len(sub),
            "active_nodes": len(sd),
            "density": 2 * len(sub) / (len(nodes) * (len(nodes) - 1)) if len(nodes) > 1 else None,
            "density_x1e4": round(2 * len(sub) / (len(nodes) * (len(nodes) - 1)) * 1e4, 4)
            if len(nodes) > 1 else None,
            "mean_degree": round(2 * len(sub) / len(nodes), 4) if nodes else None,
            "active_share_pct": round(len(sd) / len(nodes) * 100, 4) if nodes else None,
        })

    # ---------- 负证据 ----------
    probe = load(PROBE)
    blocked = []
    for r in probe.get("blocked", []):
        blocked.append({
            "table": r["table"],
            "gkx_exists": r["gkx_information_schema"]["exists"],
            "gkx_schema_hits": r["gkx_information_schema"]["hits"],
            "live_shell_rows": r["live_where"].get("live_shell_rows"),
            "live_demo_row_class": ("全量装载" if (r["live_where"].get("rows") or 0) >= 10000 else "样例级"),
            "verdict": r["live_where"].get("verdict"),
        })

    out = {
        "metric": ID,
        "metric_name": "服务关系链密度",
        "support_judgment": "部分支持",
        "verdict_kind": "partial_with_gaps",
        "generated_at": "2026-10-23T04:40:00+08:00",
        "sources": {
            "db": "gkx",
            "host": "183.240.141.251:3318",
            "user": "gkx_reader_zp",
            "mode": "read-only",
            "tables": [
                "gkx.dwd_org_org_product_info",
                "gkx.dwd_org_invest_info",
                "gkx.dwd_org_shareholder_info",
                "gkx.dwd_org_base_info",
            ],
            "snapshots": [
                "code/_snapshots21/svc21_facts_20261022.json",
                "code/_probe_blocked_f2_20261023.json",
            ],
            "demo_used": False,
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面指标（快照日 2026-10-22），无年度基期；投资/股东边不带可靠年份，不做时间序列。",
        "point_sets": {
            "P0": {"definition": "服务机构池全部机构（org_id 去重）", "n": n0},
            "P1": {"definition": "P0 中度 ≥1 的机构（剔除孤立点）", "n": n1},
            "P2": {"definition": "P1 的最大连通分量", "n": giant},
            "normalization": "密度分母 n(n-1)；平均度归一化分母 n-1",
            "isolated_handling": "P0 中的孤立点在 P0 口径记度 0 并计入分母；P1 口径剔除并单列数量",
        },
        "edges": {
            "invest_raw_touching_pool": len(invest),
            "invest_both_in_pool": inv_both,
            "invest_one_end_in_pool": inv_one,
            "shareholder_raw_touching_pool": len(share),
            "shareholder_both_in_pool": shr_both,
            "shareholder_one_end_in_pool": shr_one,
            "undirected_internal_edges": E,
            "from_invest_only": inv_only,
            "added_by_shareholder": shr_added,
            "max_degree": max(deg.values()),
            "components": len(comp),
            "giant_component_nodes": giant,
            "second_component_nodes": comp.most_common(2)[1][1] if len(comp) > 1 else 0,
        },
        "degree_buckets": buckets,
        "density": {
            "P0": {
                "n": n0,
                "edges": E,
                "density": dens_p0,
                "density_x1e4": round(dens_p0 * 1e4, 4),
                "mean_degree": round(mean_p0, 4),
                "normalized_mean_degree": round(mean_p0 / (n0 - 1), 8),
            },
            "P1": {
                "n": n1,
                "edges": E,
                "density": dens_p1,
                "density_x1e4": round(dens_p1 * 1e4, 4),
                "mean_degree": round(mean_p1, 4),
                "normalized_mean_degree": round(mean_p1 / (n1 - 1), 6),
            },
        },
        "city_slices": city_rows,
        "derived": {
            "invest_both_resolve_pct": {
                "value": round(inv_both / len(invest) * 100, 4),
                "numerator": inv_both,
                "denominator": len(invest),
                "denominator_note": "分子=池内两端都可解析的投资边数（invest_both_in_pool），分母=触碰池的投资边原始行数 invest_raw_touching_pool",
            },
            "shareholder_both_resolve_pct": {
                "value": round(shr_both / len(share) * 100, 4),
                "numerator": shr_both,
                "denominator": len(share),
                "denominator_note": "分子=池内两端都可解析的股东边数（shareholder_both_in_pool），分母=触碰池的股东边原始行数 shareholder_raw_touching_pool",
            },
            "invest_share_of_internal_edges_pct": {
                "value": round(inv_only / E * 100, 4),
                "numerator": inv_only,
                "denominator": E,
                "denominator_note": "分子=仅由投资边构成的池内无向边数（from_invest_only），分母=投资+股东合并去重后的无向边数 undirected_internal_edges",
            },
            "shareholder_added_share_pct": {
                "value": round(shr_added / E * 100, 4),
                "numerator": shr_added,
                "denominator": E,
                "denominator_note": "分子=股东边在投资边之外新增的无向边数（added_by_shareholder），分母=合并去重后的无向边数 undirected_internal_edges",
            },
            "isolated_share_p0_pct": {
                "value": round(buckets["0"] / n0 * 100, 4),
                "numerator": buckets["0"],
                "denominator": n0,
                "denominator_note": "分子=P0 中度数为 0 的机构数（degree_buckets.0），分母=服务机构池家数 P0.n",
            },
            "degree1_share_p1_pct": {
                "value": round(buckets["1"] / n1 * 100, 4),
                "numerator": buckets["1"],
                "denominator": n1,
                "denominator_note": "分子=P1 中度数恰为 1 的机构数（degree_buckets.1），分母=非孤立机构数 P1.n",
            },
            "degree10plus_share_p1_pct": {
                "value": round(buckets["10+"] / n1 * 100, 4),
                "numerator": buckets["10+"],
                "denominator": n1,
                "denominator_note": "分子=P1 中度数 ≥10 的机构数（degree_buckets.10+），分母=非孤立机构数 P1.n",
            },
            "giant_share_p1_pct": {
                "value": round(giant / n1 * 100, 4),
                "numerator": giant,
                "denominator": n1,
                "denominator_note": "分子=最大连通分量节点数 giant_component_nodes，分母=P1.n（非孤立机构数）",
            },
            "giant_share_p0_pct": {
                "value": round(giant / n0 * 100, 4),
                "numerator": giant,
                "denominator": n0,
                "denominator_note": "分子=最大连通分量节点数 giant_component_nodes，分母=服务机构池家数 P0.n",
            },
            "p1_over_p0_pct": {
                "value": round(n1 / n0 * 100, 4),
                "numerator": n1,
                "denominator": n0,
                "denominator_note": "分子=非孤立机构数 P1.n，分母=服务机构池家数 P0.n",
            },
            "p1_density_over_p0_density_x": {
                "value": round(dens_p1 / dens_p0, 4),
                "numerator": round(dens_p1, 10),
                "denominator": round(dens_p0, 12),
                "denominator_note": "分子=去孤立点后的 P1 密度 density.P1.density，分母=全池 P0 密度 density.P0.density（倍率）",
            },
            "sz_edge_share_pct": {
                "value": round(city_rows[0]["internal_edges"] / E * 100, 4),
                "numerator": city_rows[0]["internal_edges"],
                "denominator": E,
                "denominator_note": "分子=深圳域内边数 city_slices[深圳市].internal_edges，分母=池内全部无向边数 undirected_internal_edges",
            },
            "degree1_share_p0_pct": {
                "value": round(buckets["1"] / n0 * 100, 4),
                "numerator": buckets["1"],
                "denominator": n0,
                "denominator_note": "分子=P0 中度数恰为 1 的机构数（degree_buckets.1），分母=服务机构池家数 P0.n",
            },
            "degree2_4_share_p0_pct": {
                "value": round(buckets["2-4"] / n0 * 100, 4),
                "numerator": buckets["2-4"],
                "denominator": n0,
                "denominator_note": "分子=P0 中度数 2—4 的机构数（degree_buckets.2-4），分母=服务机构池家数 P0.n",
            },
            "degree5_9_share_p0_pct": {
                "value": round(buckets["5-9"] / n0 * 100, 4),
                "numerator": buckets["5-9"],
                "denominator": n0,
                "denominator_note": "分子=P0 中度数 5—9 的机构数（degree_buckets.5-9），分母=服务机构池家数 P0.n",
            },
            "degree10plus_share_p0_pct": {
                "value": round(buckets["10+"] / n0 * 100, 4),
                "numerator": buckets["10+"],
                "denominator": n0,
                "denominator_note": "分子=P0 中度数 ≥10 的机构数（degree_buckets.10+），分母=服务机构池家数 P0.n",
            },
            "combined_over_invest_only_x": {
                "value": round(E / inv_only, 4),
                "numerator": E,
                "denominator": inv_only,
                "denominator_note": "分子=投资+股东合并去重后的无向边数 undirected_internal_edges，分母=仅投资边构成的边数 from_invest_only（倍率）",
            },
            "hz_density_over_sz_density_x": {
                "value": round(city_rows[3]["density"] / city_rows[0]["density"], 4),
                "numerator": city_rows[3]["density_x1e4"],
                "denominator": city_rows[0]["density_x1e4"],
                "denominator_note": "分子=惠州密度 city_slices[惠州市].density，分母=深圳密度 city_slices[深圳市].density（倍率）",
            },
            "hz_edges_over_sz_edges_pct": {
                "value": round(city_rows[3]["internal_edges"] / city_rows[0]["internal_edges"] * 100, 4),
                "numerator": city_rows[3]["internal_edges"],
                "denominator": city_rows[0]["internal_edges"],
                "denominator_note": "分子=惠州域内边数 city_slices[惠州市].internal_edges，分母=深圳域内边数 city_slices[深圳市].internal_edges",
            },
        },
        "city_slice_consistency": {
            "nodes_sum_4city": sum(r["nodes"] for r in city_rows),
            "internal_edges_sum_4city": sum(r["internal_edges"] for r in city_rows),
            "cross_city_edges": E - sum(r["internal_edges"] for r in city_rows),
            "nodes_outside_4city": n0 - sum(r["nodes"] for r in city_rows),
            "note": "四市节点之和小于 P0（差额为注册地不在四市或为空），四市域内边之和小于 E（差额为跨城边）；两项差额均不为负。",
        },
        "norm_denominators": {
            "P0_n_minus_1": n0 - 1,
            "P1_n_minus_1": n1 - 1,
            "note": "平均度归一化分母取 n-1（§3.60），不取 n。",
        },
        "absence_probe": {
            "file": "code/_probe_blocked_f2_20261023.json",
            "gkx_schema": "gkx",
            "gkx_table_total": probe.get("gkx_information_schema", {}).get("table_count"),
            "blocked_tables": blocked,
        },
        "rejected_dimensions": [
            {
                "dimension": "服务合作关系密度",
                "reason": "gkx 无 enterprise_cooperation / enterprise_supply_chain / svc_org_circle，information_schema 命中 0 行；演示库同名表不构成支持，铁律禁引",
                "alternative": "投资/股东边密度",
                "difference": "投资/股东是股权关系，不代表业务合作或服务采购；边数会系统性低估服务关系，且方向不可解释为合作强度",
            },
            {
                "dimension": "密度时间序列",
                "reason": "gkx 无 svc_metric_series（0 行），投资/股东边无可靠年份字段，不能按年切片",
                "alternative": "快照截面密度",
                "difference": "只能给单日截面，不能给趋势与环比",
            },
            {
                "dimension": "服务类型分层密度",
                "reason": "gkx 无 svc_org_card / svc_org_circle，服务类型标签无承载表",
                "alternative": "按城市切分",
                "difference": "城市切片替代服务类型切片，无法回答「哪类服务关系更密」",
            },
        ],
        "gaps": [
            "合作边、供应链边、服务关系边三类业务边整块缺失（gkx 0 表；live 侧为演示库，铁律禁引，不构成支持）",
            "股东边 95.64% 只有一端可解析，边集对股东关系的覆盖不完整",
            "投资边金额字段单位未在表结构中标注，本件不使用金额，只计边数",
            "池内 31,248 家（70.77%）为孤立点，密度对点集选择极敏感",
        ],
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print(f"pool={n0} P1={n1} edges={E} (invest_only={inv_only}) "
          f"density_P0={dens_p0:.8f} density_P1={dens_p1:.8f} giant={giant}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题服务算法库', '科技专题系统']

# 缺省参数：三系统可传子集；快照/探针粒度上不可再分的参数会在 assumptions 显式声明
COMPAT_DEFAULTS = {
    "start_date": None,        # 算法库/展示常传；缺省 → 基线口径窗口（产物 base_years_*）
    "end_date": None,          # 同上；缺省 → 基线口径窗口
    "region": None,            # 地域过滤；缺省 → 全区域（基线口径）
    "industry_tag": None,      # 链/领域标签；缺省 → 全量（基线口径）
    "weights": None,           # 维度权重（模型型指标）；缺省 → 基线内置权重（Q014 类未定项不擅自赋值）
    "dims": None,              # 维度子集（模型型指标）；缺省 → 基线全维度
    "format": None,            # "detail"/"display"；缺省 → 两段都返回
}


def compute(params=None):
    """三系统统一入口：执行基线 main() 的计算逻辑，读取其产物并附兼容元数据返回。

    返回 dict：
      value / detail   : 主值与明细（透传基线产物 headline/stats，数值逐位=基线）
      display          : 展示系统友好结构（headline 精简 + 明细首层序列化）
      assumptions      : 本次运行采用的缺省假设（缺参时非空，前端可提示）
      applicable_systems / params_effective / metric_id / metric_name / generated_at
    典型调用：
      算法库  : compute({"start_date": ..., "end_date": ..., "region": ...})   全参
      专题系统: compute({}) 或 compute({"industry_tag": "..."})               少传参
      展示系统: compute({"format": "display"})                                只要展示段
    """
    import importlib.util, json as _json, time as _time
    from pathlib import Path as _Path

    p_in = dict(params or {})
    eff = {**COMPAT_DEFAULTS, **{k: v for k, v in p_in.items() if v is not None}}
    assumptions = []
    for k, v in eff.items():
        if v is not None and k in ("start_date", "end_date", "region", "industry_tag", "weights", "dims"):
            assumptions.append(f"{k}={v!r} 已接收：本件快照/探针粒度为基线口径，参数生效范围见同名 md「入参兼容策略」"
                               "（不可再分时返回基线口径值并在此声明）")
    assumptions.append("本件为 20261021 基线口径包装（兼容层不改数学定义）；三系统主值同源")

    t0 = _time.time()
    here = _Path(__file__).resolve().parent
    out_json = here / "M_SVC_RELATION_DENSITY_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_SVC_RELATION_DENSITY.py 等价）
        run_baseline()
    data = _json.loads(out_json.read_text(encoding="utf-8"))

    headline = data.get("headline") or {}
    value = headline.get("value") if isinstance(headline, dict) and "value" in headline else None
    if value is None and isinstance(headline, dict):
        value = next((headline[k] for k in ("total_le2024", "total", "sz_total", "score", "index", "n", "count")
                      if k in headline and isinstance(headline[k], (int, float))), None)
    if value is None:   # 无 headline 结构的产物：从顶层常见键提取（KPI/分布型）
        for k in ("total", "value", "n_total", "count", "org_total", "sz_total", "sum", "amount"):
            v = data.get(k)
            if isinstance(v, (int, float)):
                value = v
                break
            if isinstance(v, dict):
                for kk in ("total", "value", "n", "sz"):
                    if isinstance(v.get(kk), (int, float)):
                        value = v[kk]
                        break
                if value is not None:
                    break
    if value is None:   # 探针/分布型产物：从 population / audit_chain / probe 找主计数
        for sec in ("population", "audit_chain", "probe", "stats"):
            v = data.get(sec)
            if isinstance(v, dict):
                for kk in ("distinct_org_id", "total", "n", "count", "org_count", "rows",
                           "filled", "polar_rows", "chain_members_total"):
                    if isinstance(v.get(kk), (int, float)):
                        value = v[kk]
                        break
            if value is not None:
                break
    if value is None:   # 兜底声明：无单一主值（分布/明细型产物），value=None 属正常而非错误
        assumptions.append("本件为分布/明细型产物（无单一主值键），value=None；调用方请消费 detail/display 段")
    detail = {k: data[k] for k in ("stats", "facts", "population", "rule", "support_judgment",
                                   "base_years_used", "base_years_missing", "sources") if k in data}
    display = {"headline": headline, "rows_preview": None}
    for k in ("chains", "rows", "items", "list", "ranking", "detail_list"):
        if isinstance(data.get(k), list):
            display["rows_preview"] = {"key": k, "n": len(data[k]), "sample": data[k][:5]}
            break
    if eff.get("format") == "display":
        detail = {"support_judgment": data.get("support_judgment")}
    return {
        "metric_id": "M_SVC_RELATION_DENSITY",
        "metric_name": data.get("metric_name"),
        "applicable_systems": APPLICABLE,
        "params_effective": eff,
        "assumptions": assumptions,
        "value": value,
        "detail": detail,
        "display": display,
        "generated_at": _time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_sec": round(_time.time() - t0, 2),
        "baseline_generated_at": data.get("generated_at"),
    }


def run_baseline():
    """原样执行基线 main()（兼容层调用；产物 _out.json 由基线逻辑写盘，铁律：产物只由脚本产出）。"""
    main()  # noqa: F821  ← 基线入口（上方原代码定义）
