#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_TECH_PATH_CENTRALITY 中心度
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_TECH_PATH_CENTRALITY.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_TECH_PATH_CENTRALITY —— 深圳 IPC4 技术点图的五维中心性。

口径：深圳单口径（节点=深圳 IPC4 前 4 位 2024 年 ≥100 件；边=同一深圳申请人共现
co≥20 且 Jaccard≥0.05）。全国不参与，本件无 LQ 分母。

零 SQL：全部读 _snapshots21 / _snapshots_gkx21 已落盘缓存。
直接跑：cd code && python3 M_TECH_PATH_CENTRALITY.py
"""
from __future__ import annotations

import json
from datetime import datetime

import _path_graph21 as P

METRIC_ID = "M_TECH_PATH_CENTRALITY"
OUT = P.CODE / f"{METRIC_ID}_out.json"

# 五维：判据阈值（判定口径写在文档 §〇，代码只执行）
GATE = {
    "degree": {"name": "度中心性", "stat": "max/median", "op": ">=", "thr": 3.0},
    "wdegree": {"name": "强度中心性（边权=共现户数）", "stat": "max/min", "op": ">=", "thr": 10.0},
    "betweenness": {"name": "介数中心性", "stat": "tau_threshold", "op": ">=", "thr": 0.80},
    "harmonic": {"name": "调和接近中心性", "stat": "p95/p05", "op": ">=", "thr": 2.0},
    "pagerank": {"name": "加权 PageRank", "stat": "max/min", "op": ">=", "thr": 10.0},
}


def p05(v):
    v = sorted(v)
    return v[int(round(0.05 * (len(v) - 1)))]


def main():
    nodes, seq, cell = P.node_universe()
    g = P.build(nodes)
    adj = g["adj"]
    C = P.all_centralities(g)
    comps = P.components(nodes, adj)
    iso = [x for x in nodes if not adj[x]]

    # ---- 阈值敏感性：边规则 ±50% / 2× ----
    sens = []
    for co_min, jac_min, tag in [(15, 0.04, "放宽 50%"), (20, 0.05, "基准"), (30, 0.07, "收紧 50%"), (40, 0.10, "收紧 100%")]:
        gg = P.build(nodes, co_min, jac_min)
        CC = P.all_centralities(gg)
        sens.append({
            "tag": tag, "co_min": co_min, "jac_min": jac_min, "edges": len(gg["edges"]),
            "tau_degree": round(P.spearman([C["degree"][x] for x in nodes], [CC["degree"][x] for x in nodes]), 4),
            "tau_wdegree": round(P.spearman([C["wdegree"][x] for x in nodes], [CC["wdegree"][x] for x in nodes]), 4),
            "tau_betweenness": round(P.spearman([C["betweenness"][x] for x in nodes], [CC["betweenness"][x] for x in nodes]), 4),
            "tau_harmonic": round(P.spearman([C["harmonic"][x] for x in nodes], [CC["harmonic"][x] for x in nodes]), 4),
            "tau_pagerank": round(P.spearman([C["pagerank"][x] for x in nodes], [CC["pagerank"][x] for x in nodes]), 4),
        })
    base_tau = {k: [r[f"tau_{k}"] for r in sens if r["tag"] != "基准"] for k in GATE}

    # ---- 判档 ----
    deg_v = [C["degree"][x] for x in nodes]
    wd_v = [C["wdegree"][x] for x in nodes]
    bc_v = [C["betweenness"][x] for x in nodes]
    hc_v = [C["harmonic"][x] for x in nodes]
    pr_v = [C["pagerank"][x] for x in nodes]
    med_deg = P.stats(deg_v)["median"] or 1
    med_wd = P.stats(wd_v)["median"] or 1

    # 调和接近中心性在两处测量：全图（含 9 个孤立点，会把 p05 拉到 0.17，虚高区分度）
    # 与巨连通块内（226 个，唯一有意义的比较域）。判档用巨连通块，全图仅作对照。
    giant = comps[0]
    hc_g = sorted([C["harmonic"][x] for x in giant])
    p05_g = hc_g[int(round(0.05 * (len(hc_g) - 1)))]
    p95_g = hc_g[int(round(0.95 * (len(hc_g) - 1)))]
    band = sum(1 for v in hc_g if 0.30 <= v <= 0.51) / len(hc_g)

    measured = {
        "degree": round(max(deg_v) / med_deg, 2),
        "wdegree": round(max(wd_v) / max(1, min([v for v in wd_v if v > 0])), 2),
        "betweenness": round(min(base_tau["betweenness"]), 4),
        "harmonic": round(p95_g / p05_g, 2),
        "pagerank": round(max(pr_v) / min(pr_v), 2),
    }
    gate = []
    for k, cfg in GATE.items():
        m, thr = measured[k], cfg["thr"]
        ok = m >= thr
        verdict = "可用" if ok else ("退化" if k == "harmonic" else "有条件可用")
        reason = {
            "degree": f"max {max(deg_v)} 件 / 中位 {int(med_deg)} 件 = {m} 倍，238 个节点 {len(set(deg_v))} 个不同取值",
            "wdegree": f"最大 {max(wd_v)} / 最小非零 {min([v for v in wd_v if v > 0])} = {m} 倍",
            "betweenness": f"边规则 ±50%/2× 四档重算，与基准 Spearman 最低 {m}（阈值 {thr}）→ 名次不稳",
            "harmonic": f"巨连通块 226 点内 p95 {round(p95_g,4)} / p05 {round(p05_g,4)} = {m} 倍，{round(band*100,1)}% 的节点挤在 0.30—0.51 的 0.21 宽窄带里",
            "pagerank": f"max {round(max(pr_v),5)} / min {round(min(pr_v),5)} = {m} 倍",
        }[k]
        gate.append({"dim": k, "name": cfg["name"], "measured": m, "criterion": f"{cfg['stat']} {cfg['op']} {thr}",
                     "pass": ok, "verdict": verdict, "reason": reason})

    n_ok = sum(1 for x in gate if x["verdict"] == "可用")
    support = "完全转换支持" if n_ok == 5 else ("部分支持" if n_ok >= 2 else "不支持")

    # ---- 排序 / 百分位 ----
    def rank_map(vals):
        order = sorted(vals, key=lambda x: -vals[x])
        return {x: i + 1 for i, x in enumerate(order)}

    ranks = {k: rank_map(v) for k, v in
             [("degree", C["degree"]), ("wdegree", C["wdegree"]), ("betweenness", C["betweenness"]),
              ("harmonic", C["harmonic"]), ("pagerank", C["pagerank"])]}

    rows = []
    for x in nodes:
        rows.append({
            "ipc4": x, "n_2024": seq[x][-1], "n_window": sum(seq[x]),
            "degree": C["degree"][x], "wdegree": C["wdegree"][x],
            "betweenness": round(C["betweenness"][x], 6), "harmonic": round(C["harmonic"][x], 6),
            "pagerank": round(C["pagerank"][x], 6),
            "rank_degree": ranks["degree"][x], "rank_wdegree": ranks["wdegree"][x],
            "rank_betweenness": ranks["betweenness"][x], "rank_harmonic": ranks["harmonic"][x],
            "rank_pagerank": ranks["pagerank"][x],
        })

    top = {}
    for k in ("degree", "wdegree", "betweenness", "harmonic", "pagerank"):
        top[k] = [{"ipc4": r["ipc4"], "v": r[f"{k}" if k != "wdegree" else "wdegree"], "n_2024": r["n_2024"]}
                  for r in sorted(rows, key=lambda r: -r[k])[:10]]

    # 多榜共识：五维里进前 20 的次数（不含退化维）
    use = ["degree", "wdegree", "betweenness", "pagerank"]
    hit = {x: sum(1 for k in use if ranks[k][x] <= 20) for x in nodes}
    consensus = [{"ipc4": x, "n_list": hit[x], "ranks": {k: ranks[k][x] for k in use}}
                 for x in sorted(nodes, key=lambda x: (-hit[x], ranks["pagerank"][x])) if hit[x] >= 3]

    corr = [{"a": a, "b": b, "spearman": round(P.spearman([C[a][x] for x in nodes], [C[b][x] for x in nodes]), 4)}
            for i, a in enumerate(("degree", "wdegree", "betweenness", "harmonic", "pagerank"))
            for b in ("degree", "wdegree", "betweenness", "harmonic", "pagerank") if a < b]

    density = 2 * len(g["edges"]) / (len(nodes) * (len(nodes) - 1))
    out = {
        "metric_id": METRIC_ID,
        "metric_name": "技术路径中心性（深圳 IPC4 技术点图五维中心性）",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": P.SOURCE,
        "caliber": "深圳单口径；全国不参与，无 LQ 分母",
        "support_level": support,
        "support_note": f"五维中 {n_ok} 维判可用（度/强度/PageRank），介数条件可用，调和接近退化",
        "universe": {
            "n_nodes": len(nodes), "n_edges": len(g["edges"]), "density": round(density, 5),
            "n_components": len(comps), "giant_component": len(comps[0]),
            "component_sizes": [len(c) for c in comps], "n_isolated": len(iso), "isolated": iso,
            "n_applicants_with_graph_ipc": g["n_applicants_with_graph_ipc"],
        },
        "graph_params": g["params"],
        "gate": gate,
        "stats": {"degree": P.stats(deg_v), "wdegree": P.stats(wd_v), "betweenness": P.stats(bc_v),
                  "harmonic": P.stats(hc_v), "pagerank": P.stats(pr_v),
                  "harmonic_giant": {"n": len(hc_g), "min": round(hc_g[0], 6), "p05": round(p05_g, 6),
                                     "median": round(hc_g[len(hc_g) // 2], 6), "p95": round(p95_g, 6),
                                     "max": round(hc_g[-1], 6),
                                     "share_in_030_051": round(band, 4),
                                     "p95_over_p05": round(p95_g / p05_g, 4)}},
        "sensitivity": sens,
        "rank_corr": corr,
        "top10": top,
        "consensus": consensus,
        "nodes": rows,
        "base_years_used": [2021, 2022, 2023, 2024],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": "图结构用 2021—2024 四年深圳件累计共现；2025/2026 不入图（2026 为残年）；库内 2017—2020 无专利行，不补零",
        "key_numbers": {
            "bridge_top": top["betweenness"][0]["ipc4"], "bridge_top_v": top["betweenness"][0]["v"],
            "hub_top_degree": top["degree"][0]["ipc4"], "hub_top_degree_v": top["degree"][0]["v"],
            "pr_top": top["pagerank"][0]["ipc4"], "pr_top_v": top["pagerank"][0]["v"],
            "tau_bc_min": min(base_tau["betweenness"]), "tau_pr_min": min(base_tau["pagerank"]),
            "consensus_n": len(consensus),
        },
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("done ->", OUT)
    print(json.dumps({"nodes": len(nodes), "edges": len(g["edges"]), "support": support,
                      "gate": {x["dim"]: [x["measured"], x["verdict"]] for x in gate},
                      "bridge": top["betweenness"][0], "hub": top["degree"][0]}, ensure_ascii=False))


if __name__ == "__main__":
    main()


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题服务算法库', '科技信息展示系统']

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
    out_json = here / "M_TECH_PATH_CENTRALITY_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_TECH_PATH_CENTRALITY.py 等价）
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
        "metric_id": "M_TECH_PATH_CENTRALITY",
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
