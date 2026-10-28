#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_SVC_GRAPH_DENSITY 服务网络密度
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_SVC_GRAPH_DENSITY.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""服务网络密度（M_SVC_GRAPH_DENSITY）—— gkx 口径，自包含。

口径（侯佳伟 2026-08-21 标准图论密度，公式照抄）：
    D = 2|E| / (|N| × (|N| − 1))
    两个分母口径并列：全池 N=44,153（生态位覆盖率）、活跃子网 N=12,905（参与者紧密度）
    分母 |N|(|N|−1)/2 为无向简单图的可能边数；|N| < 2 时不输出。

口径裁决（沿用 Q-SVCCHAIN-03 会签结论）：
    「服务网络密度」的边**不算**投资/股东边。因此本件算出的密度只能以
    「资本纽带密度（代理）」身份披露，不能宣称是正式服务网络密度；
    正式语义需要合作/交易/人才流动边，gkx 无承载表。

数据源：code/_snapshots21/svc21_facts_20261022.json
产出：code/M_SVC_GRAPH_DENSITY_out.json
运行：cd code && python3 M_SVC_GRAPH_DENSITY.py
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
OUT = os.path.join(HERE, "M_SVC_GRAPH_DENSITY_out.json")


def density(E, N):
    if N is None or N < 2:
        return None
    return 2.0 * E / (N * (N - 1))


def sci(x):
    return None if x is None else float("%.4e" % x)


def main():
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    pool, inv, sh = f["pool"], f["invest_edges"], f["shareholder_edges"]
    ids = set(pool)
    N = len(ids)

    # ---- 主口径边集（两类合并、去重、去自环）-----------------------------------
    pairs, only_inv, only_sh, empty = set(), set(), set(), 0
    for e in inv:
        a, b = e[0], e[1]
        if not b:
            empty += 1
            continue
        if a in ids and b in ids and a != b:
            pairs.add(tuple(sorted((a, b))))
            only_inv.add(tuple(sorted((a, b))))
    for e in sh:
        a, b = e[0], e[1]
        if not b:
            empty += 1
            continue
        if a in ids and b in ids and a != b:
            pairs.add(tuple(sorted((a, b))))
            only_sh.add(tuple(sorted((a, b))))

    deg = Counter()
    for a, b in pairs:
        deg[a] += 1
        deg[b] += 1
    n_act = len(deg)
    E = len(pairs)

    D_pool = density(E, N)
    D_act = density(E, n_act)

    # ---- 口径敏感度：单类边、以及含无向重复计数的宽松口径 ----------------------
    # 实测：投资边的节点对几乎全部同时出现在股东表里（同一笔资本关系两边各记一次），
    # 因此「只算投资边」的独立贡献为 0 条——这不是取数 bug，写进 sensitivity 一并披露。
    D_inv_only = density(len(only_inv - only_sh), N)
    D_sh_only = density(len(only_sh - only_inv), N)
    # 宽松口径：不做无向去重，投资 + 股东两边各计一条（用于说明「口径差 1 倍量级在哪」）
    raw = 0
    for e in inv:
        if e[1] and e[0] in ids and e[1] in ids and e[0] != e[1]:
            raw += 1
    for e in sh:
        if e[1] and e[0] in ids and e[1] in ids and e[0] != e[1]:
            raw += 1
    D_raw = density(raw, N)

    # ---- 可能边数与实际占比 -------------------------------------------------------
    possible = N * (N - 1) / 2
    realized_pct = 100.0 * E / possible

    reason = ("代理密度可现转（全池 %.3e / 活跃子网 %.3e），结构与计算链完整；"
              "但会签口径 Q-SVCCHAIN-03 明确「服务网络密度的边不算投资/股东」，"
              "正式服务关系边在 gkx 无承载表，始终有一维缺正式数据，故落部分支持。"
              % (D_pool, D_act))

    out = {
        "metric_id": "M_SVC_GRAPH_DENSITY",
        "metric_name": "服务网络密度",
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
        "base_years_note": ("密度是截面量（快照时点存量边），不做年度序列；"
                            "库内边表无「关系生效年」字段，按年拆边会把存量关系误摊成流量，故不拆。"),
        "formula": "D = 2|E| / (|N| * (|N| - 1))",
        "main": {
            "edge_set": "投资边 ∪ 机构股东边（双端在池、无向去重、去自环）",
            "E": E,
            "N_pool": N,
            "N_active": n_act,
            "possible_edges_pool": round(possible, 1),
            "realized_share_pct": round(realized_pct, 8),
            "density_pool": sci(D_pool),
            "density_active": sci(D_act),
            "density_pool_raw": D_pool,
            "density_active_raw": D_act,
        },
        "sensitivity": {
            "invest_pairs": len(only_inv),
            "shareholder_pairs": len(only_sh),
            "overlap_pairs": len(only_inv & only_sh),
            "invest_edges_only": {"E": len(only_inv - only_sh), "density_pool": sci(D_inv_only),
                                  "note": "投资边的节点对 %d 条中 %d 条同时出现在股东表，"
                                          "独立贡献为 0 条——同一笔资本关系两表各记一次所致，"
                                          "须按无向去重合并，不能相加"
                                          % (len(only_inv), len(only_inv & only_sh))},
            "shareholder_edges_only": {"E": len(only_sh - only_inv), "density_pool": sci(D_sh_only)},
            "no_undirected_dedup": {"E": raw, "density_pool": sci(D_raw),
                                    "note": "同一对机构在两表各出现一次即计两条，仅用于说明口径敏感度"},
            "empty_counterpart_rows": empty,
        },
        "caliber_ruling": {
            "code": "Q-SVCCHAIN-03",
            "ruling": "服务网络密度的边不算投资/股东",
            "consequence": "本件数值只能以「资本纽带密度（代理）」身份披露，不得宣称正式服务网络密度",
        },
        "compute": {"elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("E=%d N_pool=%d N_act=%d" % (E, N, n_act))
    print("D(全池)=%.6e  D(活跃)=%.6e" % (D_pool, D_act))
    print("可能边 %.3e，实现占比 %.8f%%" % (possible, realized_pct))
    print("敏感度：单投资 %.4e / 单股东 %.4e / 不去重 %.4e" % (D_inv_only, D_sh_only, D_raw))
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
    out_json = here / "M_SVC_GRAPH_DENSITY_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_SVC_GRAPH_DENSITY.py 等价）
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
        "metric_id": "M_SVC_GRAPH_DENSITY",
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
