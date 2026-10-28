#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_SYNTH_COLLAB_COMPLETENESS 协同网络完整度
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_SYNTH_COLLAB_COMPLETENESS.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""
M_SYNTH_COLLAB_COMPLETENESS —— 协同网络完整度（有边主体/主体全集）
复用 2026-10-21 已落盘网络事实，不重跑 DB 探针。
运行：python3 code/M_SYNTH_COLLAB_COMPLETENESS.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _collab_c_common as cc

MID = "M_SYNTH_COLLAB_COMPLETENESS"


def main():
    m191, cache, rel, org = cc.load_inputs()
    net = {c: cc.metrics_for(v) for c, v in cc.build_network(m191).items()}

    cov = {c: net[c]["completeness"] for c in cc.CITY_ORDER}
    scores = cc.minmax_scores(cov)
    rank = sorted(cc.CITY_ORDER, key=lambda c: cov[c] or 0, reverse=True)

    cities = {}
    for c in cc.CITY_ORDER:
        x = net[c]
        cities[cc.CITY_SHORT[c]] = {
            "n_nodes": x["n_nodes"],
            "org_nodes": x["org_nodes"],
            "ri_nodes": x["ri_nodes"],
            "scholar_org_nodes": x["scholar_org_nodes"],
            "edges_m": x["m_edges"],
            "covered_nodes_cached": x["covered_nodes_cached"],
            "covered_upper_bound_2m": x["covered_upper_bound_2m"],
            "covered_graph_consistent": x["covered_graph_consistent"],
            "completeness_raw": x["completeness"],
            "completeness_pct": round((x["completeness"] or 0) * 100, 4),
            "completeness_upper_bound_pct": round(
                (x["completeness_upper_bound"] or 0) * 100, 4
            ),
            "dim_score_0_100": scores[c],
        }

    payload = {
        "metric_id": MID,
        "metric_name_zh": "协同网络完整度",
        "grain": "区域（城市）× 统计窗口",
        "formula": "Completeness = n_covered / N × 100；N=企业∪科研机构∪学者所属机构（含无边主体）",
        "compute": {
            "cities": cities,
            "distribution": cc.describe(cov),
            "rank_by_completeness": [cc.CITY_SHORT[c] for c in rank],
            "top": cc.CITY_SHORT[rank[0]],
            "bottom": cc.CITY_SHORT[rank[-1]],
        },
        "consistency_check": {
            "issue": "上游覆盖节点缓存值在有 3 城超过无向简单图 2E 上界（深 128>26、京 236>150、沪 214>126）",
            "cities_over_2m": [
                cc.CITY_SHORT[c] for c in cc.CITY_ORDER if not net[c]["covered_graph_consistent"]
            ],
            "handling": "同时登记缓存值（主口径，沿用 191）与 2E 上界值（可复核下界），差值即覆盖节点口径的不确定区间",
            "note": "沪 214≤2E=126 不成立，故上界列以 min(缓存,2E) 截断；该差异须在甲方口径确认前披露",
        },
        "reuse_evidence": {
            "m191_raw_measures_completeness": {
                c: m191.get("raw_measures", {}).get(c, {}).get("completeness_raw")
                for c in cc.CITY_ORDER
            },
            "m191_dim_scores_completeness": m191.get("dim_scores", {}).get("完整度"),
            "funded_institution_nonnull": m191.get("network_facts", {}).get(
                "funded_institution_nonnull"
            ),
        },
        "baseline": cc.baseline(org),
        "support_judgment": "部分支持",
        "support_reason": (
            "完整度公式可执行、四城覆盖率可算；但①分子侧三类边仅两类可建（合作项目边 funded_institution 全空），"
            "完整度是『两类协同』而非『三类协同』的覆盖率；②分母含无边主体，京沪企业主档 163/16 家、深广 95,600/49,605 家，"
            "分母口径双向失真；③覆盖节点缓存值与 2E 图论上界冲突（3 城超界），且无 window 主体名册表（calc-logic 登记的 "
            "ads.synth_collab_subject 缺口），分子不可复核。按四档口径判部分支持。"
        ),
        "provenance": cc.provenance(m191),
        "note": "完整度分母含孤立节点（算法钉）；N=0 不可算，n=0 且 N>0 记 0；本批四城 N 均远大于 0。",
    }
    path = cc.write_out(MID, payload)
    print("[OK]", path)
    print("coverage%:", {cc.CITY_SHORT[k]: round((v or 0) * 100, 4) for k, v in cov.items()})


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
    out_json = here / "M_SYNTH_COLLAB_COMPLETENESS_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_SYNTH_COLLAB_COMPLETENESS.py 等价）
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
        "metric_id": "M_SYNTH_COLLAB_COMPLETENESS",
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
