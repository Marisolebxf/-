#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_SYNTH_COLLAB_CENTRALITY 协同网络中心度
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_SYNTH_COLLAB_CENTRALITY.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""
M_SYNTH_COLLAB_CENTRALITY —— 协同网络中心度（平均点度中心性）
复用 2026-10-21 已落盘网络事实，不重跑 DB 探针。
运行：python3 code/M_SYNTH_COLLAB_CENTRALITY.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _collab_c_common as cc

MID = "M_SYNTH_COLLAB_CENTRALITY"


def main():
    m191, cache, rel, org = cc.load_inputs()
    net = {c: cc.metrics_for(v) for c, v in cc.build_network(m191).items()}

    deg = {c: net[c]["deg_avg"] for c in cc.CITY_ORDER}
    scores = cc.minmax_scores(deg)
    rank = sorted(cc.CITY_ORDER, key=lambda c: deg[c] or 0, reverse=True)

    cities = {}
    for c in cc.CITY_ORDER:
        x = net[c]
        cities[cc.CITY_SHORT[c]] = {
            "nodes_n": x["n_nodes"],
            "edges_m": x["m_edges"],
            "deg_avg_raw": round(x["deg_avg"], 10),
            "deg_centrality_norm": x["deg_centrality_norm"],
            "density_raw": x["density"],
            "identity_gap_norm_minus_density": abs(
                (x["deg_centrality_norm"] or 0) - (x["density"] or 0)
            ),
            "covered_nodes_cached": x["covered_nodes_cached"],
            "covered_subgraph_avg_deg": (
                round(x["covered_subgraph_avg_deg"], 6)
                if x["covered_subgraph_avg_deg"] is not None else None
            ),
            "dim_score_0_100": scores[c],
        }

    payload = {
        "metric_id": MID,
        "metric_name_zh": "协同网络中心度（平均点度中心性）",
        "grain": "区域（城市）× 统计窗口",
        "formula": "C_avg = (1/n) * sum_i k_i = 2m/n；归一化 C'_avg = C_avg/(n-1) = 2m/[n(n-1)]",
        "compute": {
            "cities": cities,
            "distribution": cc.describe(deg),
            "rank_by_centrality": [cc.CITY_SHORT[c] for c in rank],
            "top": cc.CITY_SHORT[rank[0]],
            "bottom": cc.CITY_SHORT[rank[-1]],
        },
        "identity_check": {
            "statement": "无向简单图上，归一化平均点度中心性恒等于图密度",
            "max_abs_gap": max(v["identity_gap_norm_minus_density"] for v in cities.values()),
            "implication": "均值口径的中心度与密度秩相关=1，不能独立识别枢纽节点；枢纽识别需节点级度清单",
        },
        "reuse_evidence": {
            "m191_raw_measures": m191.get("raw_measures"),
            "m191_dim_scores_centrality": m191.get("dim_scores", {}).get("中心度"),
            "relation_input_edges": rel.get("边"),
            "relation_input_total": rel.get("合计"),
        },
        "baseline": cc.baseline(org),
        "support_judgment": "部分支持",
        "support_reason": (
            "联合专利边（dwd_patent_applicants 28,964 行）与人才流动边（dwd_scholar_work_experience 57,117 行）"
            "可现转，平均点度中心性四城可算；但①合作项目边结构性缺失（dwd_zh_project.funded_institution 58,453 行全空，0 边），"
            "三边并集缺一类；②节点分母失真（京沪企业主档仅 163/16 家，深广全量 95,600/49,605 家），中心度均值由分母口径主导；"
            "③节点级度清单未落盘，覆盖节点缓存值（深 128 > 2E=26）超出图论上界，枢纽节点无法复核。"
            "故按四档口径判部分支持。"
        ),
        "provenance": cc.provenance(m191),
        "note": "维度分值为四城 min-max 归一（与 191 dim_scores 同法）；中心度均值口径沿用王惠 INDEX 子项定义。",
    }
    path = cc.write_out(MID, payload)
    print("[OK]", path)
    print("deg_avg:", {k: round(v, 10) for k, v in deg.items()})
    print("scores:", {cc.CITY_SHORT[k]: v for k, v in scores.items()})


if __name__ == "__main__":
    main()


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题服务算法库', '科技专题系统', '科技信息展示系统']

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
    out_json = here / "M_SYNTH_COLLAB_CENTRALITY_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_SYNTH_COLLAB_CENTRALITY.py 等价）
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
        "metric_id": "M_SYNTH_COLLAB_CENTRALITY",
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
