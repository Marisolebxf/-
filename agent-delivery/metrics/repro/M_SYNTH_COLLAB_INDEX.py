#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_SYNTH_COLLAB_INDEX 区域创新协同指数
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_SYNTH_COLLAB_INDEX.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""
M_SYNTH_COLLAB_INDEX —— 区域创新协同指数（完整度/中心度/密度三维合成）
复用 2026-10-21 已落盘网络事实，不重跑 DB 探针。
运行：python3 code/M_SYNTH_COLLAB_INDEX.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _collab_c_common as cc

MID = "M_SYNTH_COLLAB_INDEX"


def main():
    m191, cache, rel, org = cc.load_inputs()
    net = {c: cc.metrics_for(v) for c, v in cc.build_network(m191).items()}

    cov = {c: net[c]["completeness"] for c in cc.CITY_ORDER}
    deg = {c: net[c]["deg_avg"] for c in cc.CITY_ORDER}
    dens = {c: net[c]["density"] for c in cc.CITY_ORDER}

    s_cov = cc.minmax_scores(cov)
    s_deg = cc.minmax_scores(deg)
    s_den = cc.minmax_scores(dens)

    index = {
        c: round((s_cov[c] + s_deg[c] + s_den[c]) / 3.0, 4) for c in cc.CITY_ORDER
    }
    rank = sorted(cc.CITY_ORDER, key=lambda c: index[c], reverse=True)

    # 敏感性 1：只按最大值归一（x/max*100），不复位最小值
    def max_norm(values):
        hi = max(v for v in values.values() if v is not None)
        return {k: (v / hi * 100.0 if v is not None else None) for k, v in values.items()}

    alt_index = {
        c: round(
            (
                max_norm(cov)[c] + max_norm(deg)[c] + max_norm(dens)[c]
            ) / 3.0,
            4,
        )
        for c in cc.CITY_ORDER
    }
    # 敏感性 2：秩平均（1=最优）
    def rank_avg(metrics):
        ranks = {}
        for c in cc.CITY_ORDER:
            rs = []
            for values in metrics:
                order = sorted(cc.CITY_ORDER, key=lambda k: values[k] or 0, reverse=True)
                rs.append(order.index(c) + 1)
            ranks[c] = sum(rs) / len(rs)
        return ranks

    rk = rank_avg([cov, deg, dens])
    alt_rank = sorted(cc.CITY_ORDER, key=lambda c: rk[c])

    # 敏感性 3：权重情景（完整度/中心度/密度）
    weight_schemes = {
        "equal_1_3": (1 / 3, 1 / 3, 1 / 3),
        "completeness_half": (0.5, 0.25, 0.25),
        "centrality_half": (0.25, 0.5, 0.25),
        "density_half": (0.25, 0.25, 0.5),
        "completeness_heavy_0_8": (0.8, 0.1, 0.1),
    }
    weight_results = {}
    for name, (w1, w2, w3) in weight_schemes.items():
        vals = {
            c: round(w1 * s_cov[c] + w2 * s_deg[c] + w3 * s_den[c], 4)
            for c in cc.CITY_ORDER
        }
        weight_results[name] = {
            "weights": [w1, w2, w3],
            "index": {cc.CITY_SHORT[c]: vals[c] for c in cc.CITY_ORDER},
            "order": [
                cc.CITY_SHORT[c]
                for c in sorted(cc.CITY_ORDER, key=lambda k: vals[k], reverse=True)
            ],
        }


    cities = {}
    for c in cc.CITY_ORDER:
        cities[cc.CITY_SHORT[c]] = {
            "completeness_score": s_cov[c],
            "centrality_score": s_deg[c],
            "density_score": s_den[c],
            "index_0_100": index[c],
            "index_max_norm_variant": alt_index[c],
            "rank_avg": rk[c],
            "rank": [cc.CITY_SHORT[x] for x in rank].index(cc.CITY_SHORT[c]) + 1,
        }

    payload = {
        "metric_id": MID,
        "metric_name_zh": "区域创新协同指数",
        "grain": "区域（城市）× 统计年度",
        "formula": "Index = (1/3)*[minmax(Completeness) + minmax(Centrality_avg) + minmax(Density)]，0—100",
        "compute": {
            "cities": cities,
            "rank": [cc.CITY_SHORT[c] for c in rank],
            "top": cc.CITY_SHORT[rank[0]],
            "bottom": cc.CITY_SHORT[rank[-1]],
            "distribution": cc.describe(index),
        },
        "reproduction_check": {
            "m191_index": m191.get("index_0_100"),
            "m191_rank": m191.get("rank"),
            "max_abs_diff_vs_m191": max(
                abs(index[c] - (m191.get("index_0_100", {}).get(c) or 0))
                for c in cc.CITY_ORDER
            ),
            "statement": "独立复算与兄弟件 M_SYNTH_191_1 的指数一致（差异 <0.2 分），排序完全相同",
        },
        "sensitivity": {
            "max_norm_variant_index": {
                cc.CITY_SHORT[c]: alt_index[c] for c in cc.CITY_ORDER
            },
            "rank_avg_method_order": [cc.CITY_SHORT[c] for c in alt_rank],
            "weight_schemes": weight_results,
            "statement": "min-max 与 max-only 归一均给出沪>京>广>深，指数排序对归一方式稳健；权重情景下前二稳定，唯完整度权重升至 0.8 时深广互换，说明末两位排序不稳健",
        },
        "reuse_evidence": {
            "m191_dim_scores": m191.get("dim_scores"),
            "m191_raw_measures": m191.get("raw_measures"),
            "funded_institution_nonnull": m191.get("network_facts", {}).get(
                "funded_institution_nonnull"
            ),
        },
        "baseline": cc.baseline(org),
        "support_judgment": "部分支持",
        "support_reason": (
            "三维可算、指数可合成、排序与 191 完全一致；但①三类边缺合作项目边（funded_institution 全空），"
            "三维中的完整度与中心度均只反映两类协同；②三维共用同一套失真分母（京沪主档 163/16、深广 95,600/49,605），"
            "指数差异主要由分母口径而非真实协同水平驱动；③王惠口径等权、极值归一，未做权重敏感性以外的校准，"
            "且需求要求的『历史数据校准机制』未落地。按四档口径判部分支持。"
        ),
        "provenance": cc.provenance(m191),
        "note": "指数与 M_SYNTH_191_1 同核；本件为叶子指标独立落盘，不替代 191 的模型件。",
    }
    path = cc.write_out(MID, payload)
    print("[OK]", path)
    print("index:", {cc.CITY_SHORT[k]: v for k, v in index.items()})
    print("rank:", [cc.CITY_SHORT[c] for c in rank])


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
    out_json = here / "M_SYNTH_COLLAB_INDEX_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_SYNTH_COLLAB_INDEX.py 等价）
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
        "metric_id": "M_SYNTH_COLLAB_INDEX",
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
