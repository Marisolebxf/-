#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_SVC_GRAPH_CENTRALITY 节点度中心性
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_SVC_GRAPH_CENTRALITY.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""节点度中心性（M_SVC_GRAPH_CENTRALITY）—— gkx 口径，自包含。

口径（侯佳伟 2026-08-21 度体系，公式照抄）：
    DC(v) = deg(v) / (N − 1)        （Freeman 相对度，无向简单图）
    边集  = 投资边 ∪ 机构股东边，双端在池、无向去重、去自环（与 113_1 同源同规则）
    两个分母口径并列：全池 N=44,153（生态位覆盖率语义）、活跃子网 N=12,905（枢纽排位语义）

与旧稿的差异：
    旧稿 N=43,296 / E=2,859（物化池）；本件 N=44,153 / E=13,141（经营范围池）。
    边数放大 4.6 倍不是「换库导致的数据差异」，而是旧稿的池是 `svc_org_card` 的窄口径
    （只收被档案卡收编的机构），本件池是主档经营范围命中，双端同时在池的概率更高。
    两个读数不可直接比大小，只能比结构（度右偏、度=1 长尾、枢纽具名）。

数据源：code/_snapshots21/svc21_facts_20261022.json
产出：code/M_SVC_GRAPH_CENTRALITY_out.json
运行：cd code && python3 M_SVC_GRAPH_CENTRALITY.py
"""
from __future__ import annotations

import json
import os
import statistics
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
OUT = os.path.join(HERE, "M_SVC_GRAPH_CENTRALITY_out.json")


def build_pairs(pool, inv, sh):
    """投资边 ∪ 机构股东边 → 双端在池的无向去重边集。"""
    ids = set(pool)
    pairs, selfloop, empty = set(), 0, 0
    for e in inv:
        a, b = e[0], e[1]
        if not b:
            empty += 1
            continue
        if a in ids and b in ids:
            if a == b:
                selfloop += 1
            else:
                pairs.add(tuple(sorted((a, b))))
    for e in sh:
        a, b = e[0], e[1]
        if not b:
            empty += 1
            continue
        if a in ids and b in ids:
            if a == b:
                selfloop += 1
            else:
                pairs.add(tuple(sorted((a, b))))
    return pairs, selfloop, empty


def q(vals, p):
    xs = sorted(vals)
    k = min(len(xs) - 1, max(0, int(round(p * (len(xs) - 1)))))
    return xs[k]


def main():
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    pool, inv, sh = f["pool"], f["invest_edges"], f["shareholder_edges"]
    N = len(pool)
    pairs, selfloop, empty = build_pairs(pool, inv, sh)

    deg = Counter()
    for a, b in pairs:
        deg[a] += 1
        deg[b] += 1
    n_act = len(deg)
    dvals = list(deg.values())

    dc_pool = {o: d / (N - 1) for o, d in deg.items()}
    dc_act = {o: d / (n_act - 1) for o, d in deg.items()}
    pv = list(dc_pool.values())
    av = list(dc_act.values())

    top = sorted(deg.items(), key=lambda x: (-x[1], x[0]))[:10]
    top_rows = [{"rank": i + 1, "org_id": o, "name": pool[o]["name"],
                 "type": pool[o].get("ptype2"), "city": pool[o].get("city"),
                 "degree": d,
                 "dc_pool": round(d / (N - 1), 9),
                 "dc_active": round(d / (n_act - 1), 6)} for i, (o, d) in enumerate(top)]

    deg1 = sum(1 for v in dvals if v == 1)
    hubs = sum(1 for v in dvals if v >= 50)
    zero = N - n_act

    reason = ("代理边集（投资 + 机构股东，双端在池 %d 条）上度中心性可现算并已出榜单；"
              "但需求口径的「服务关系边」（合作/交易/客户）在 gkx 无承载表，"
              "正式语义的服务网络度无源，故落部分支持。"
              % len(pairs))

    out = {
        "metric_id": "M_SVC_GRAPH_CENTRALITY",
        "metric_name": "节点度中心性",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": reason,
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_invest_info", "rows": (f.get("invest_meta") or {}).get("rows_total"),
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_shareholder_info",
             "rows": (f.get("shareholder_meta") or {}).get("rows_total"),
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
        ],
        "base_years_used": [2026],
        "base_years_missing": [],
        "base_years_note": ("度是截面量（快照时点的存量关系），无年度序列；"
                            "同一机构在不同年份的边会增减，但库内没有边的生效年份字段可拆年，"
                            "故不做年度度序列、也不补任何年份为 0。"),
        "caliber": {
            "formula": "DC(v) = deg(v) / (N - 1)",
            "edge_rule": "投资边 ∪ 机构股东边；双端在池；无向去重；去自环；对端空值（自然人股东）剔除",
            "N_pool": N,
            "N_active": n_act,
            "edges": len(pairs),
            "self_loop_dropped": selfloop,
            "empty_counterpart_rows": empty,
        },
        "degree_dist": {
            "nodes_scored": n_act,
            "nodes_isolated": zero,
            "share_scored_pct": round(100.0 * n_act / N, 2),
            "median": q(dvals, 0.5), "mean": round(statistics.mean(dvals), 4),
            "p90": q(dvals, 0.90), "p99": q(dvals, 0.99), "max": max(dvals),
            "deg_eq_1": deg1, "deg_eq_1_share_pct": round(100.0 * deg1 / n_act, 2),
            "hubs_ge_50": hubs,
        },
        "normalized": {
            "pool_caliber": {"min": round(min(pv), 9), "median": round(statistics.median(pv), 9),
                             "max": round(max(pv), 9)},
            "active_caliber": {"min": round(min(av), 8), "median": round(statistics.median(av), 8),
                               "max": round(max(av), 8)},
        },
        "top10": top_rows,
        "compute": {"elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("N", N, "E", len(pairs), "有度", n_act, "孤立", zero)
    print("度 median/p90/p99/max", out["degree_dist"]["median"], out["degree_dist"]["p90"],
          out["degree_dist"]["p99"], out["degree_dist"]["max"])
    print("DC(全池) max", out["normalized"]["pool_caliber"]["max"],
          "DC(活跃) max", out["normalized"]["active_caliber"]["max"])
    print("top1", top_rows[0]["name"], top_rows[0]["degree"])
    print("->", OUT)


if __name__ == "__main__":
    main()


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
    out_json = here / "M_SVC_GRAPH_CENTRALITY_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_SVC_GRAPH_CENTRALITY.py 等价）
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
        "metric_id": "M_SVC_GRAPH_CENTRALITY",
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
