#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_CHAIN_ENTERPRISE_POWER 企业能力
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D2 口径级分歧（本件复核为可兼容·配置型） ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_CHAIN_ENTERPRISE_POWER.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_CHAIN_ENTERPRISE_POWER 企业能力 — gkx 真源两维降级试算（20261021）

王惠口径（wanghui_agg.json，creator=王惠）：产业生态(企业数) / 企业营收 / 产业化程度(专利)
三维等权，同链同年度、对比区域截面 min-max 归一化 ×100；某维全同取 0.5。

实测约束（决定降为两维）：
  - 营收维：dwd_org_annual_financial_info 90,926 行仅 2,193 行 operating_revenue 非空（2.41%），
    2024 年正营收仅 47 家主体 → 不足以做 4 城 × 12 链截面
  - 专利维：dwd_patent 2,939,895 行，用 200k 样本（6.81%，按 dwd_id 截取非随机）匹配企业名
  - 企业数维：tags × base 流式归集，仅 4 城可归（base 命中 35,046 / 2,283,762 = 1.53%）

输出：M_CHAIN_ENTERPRISE_POWER_out.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _chain_common import write_out  # noqa: E402

METRIC = "M_CHAIN_ENTERPRISE_POWER"
NAME = "企业能力"
STREAM = Path(__file__).parent / "_snapshots" / "chain_h_stream_20261021.v1.json"
CITY4 = ["深圳市", "广州市", "东莞市", "惠州市"]


def minmax(vals: list[float]) -> list[float]:
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return [0.5] * len(vals)
    return [(v - lo) / (hi - lo) for v in vals]


def main() -> None:
    st = json.loads(STREAM.read_text(encoding="utf-8"))
    city4 = st["city4_chain"]
    pat = st["pat_city_chain"]
    total = st["total"]

    rows = []
    for code, n_total in total.items():
        cities = {}
        ec = [int(city4.get(c, {}).get(code, 0)) for c in CITY4]
        pc = [int(pat.get(code, {}).get(c, 0)) for c in CITY4]
        e_norm = minmax(ec)
        p_used = sum(pc) > 0
        p_norm = minmax(pc) if p_used else [0.5] * 4
        for i, c in enumerate(CITY4):
            dims = [("产业生态（企业数）", round(e_norm[i], 4))]
            if p_used:
                dims.append(("产业化程度（专利 200k 样本）", round(p_norm[i], 4)))
            score = sum(v for _, v in dims) / len(dims) * 100
            cities[c] = {
                "enterprise_count": ec[i],
                "enterprise_norm": round(e_norm[i], 4),
                "patent_sample_hits": pc[i],
                "patent_norm": round(p_norm[i], 4) if p_used else None,
                "dims_used": [k for k, _ in dims],
                "score": round(score, 2),
            }
        rows.append({"chain_code": code, "chain_name": None, "chain_total_national": n_total,
                     "cities": cities, "patent_dim_used": p_used,
                     "revenue_dim_used": False})
    rows.sort(key=lambda r: -r["cities"]["深圳市"]["score"])
    for i, r in enumerate(rows, 1):
        r["rank_sz"] = i

    report = {
        "metric_id": METRIC,
        "metric_name": NAME,
        "date": "2026-10-21",
        "data_source": "gkx schema gkx（dwd_org_industry_tags × dwd_org_base_info × dwd_patent 200k 样本）",
        "calc_logic_ref": "calc-logic/CHAIN/M_CHAIN_ENTERPRISE_POWER.md（王惠口径三维等权截面 min-max）",
        "note": ("王惠三维中营收维不足（非空 2,193/90,926 = 2.41%，2024 正营收主体 47 家），"
                 "降为『产业生态 + 产业化程度（专利样本）』两维等权试算；企业数维仅覆盖可归域子集 1.53%，"
                 "故本产物为方向性试算，不作正式 KPI 交付值。"),
        "probes": {
            "city4_covered_chains": len(rows),
            "base_join_hits": st["tags"]["base_hit"],
            "base_join_pct": st["tags"]["base_hit_pct"],
            "annual_fin_rows": 90926,
            "annual_fin_distinct_org": 8132,
            "annual_fin_revenue_nonnull": 2193,
            "annual_fin_revenue_nonnull_pct": round(2193 / 90926 * 100, 2),
            "annual_fin_2024_positive_orgs": 47,
            "patent_master_rows": 2939895,
            "patent_sample_rows": 200000,
            "patent_sample_rate_pct": round(200000 / 2939895 * 100, 2),
            "patent_sample_names": st["pat_sample_names"],
            "stream_elapsed_sec": st["elapsed_sec"],
        },
        "compute": {
            "cities": CITY4,
            "weights": "等权 0.5/0.5（王惠：默认等权，前端可调）",
            "dims_available": ["产业生态（企业数）", "产业化程度（专利 200k 样本）"],
            "dims_missing": ["企业营收（非空 2.41%，无法截面归一）"],
            "rows": rows,
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": ("产业生态维可算但仅覆盖可归域子集（35,046/2,283,762 = 1.53%），"
                       "营收维非空 2,193/90,926 行（2.41%）、2024 正营收仅 47 家，无法做 4 城 × 12 链截面归一；"
                       "专利维仅有 200k 样本（6.81%，非随机截取）作下限代理。"
                       "三维中一维受限、一维缺失、一维样本级，故为部分支持。"),
            "criteria": {"revenue_nonnull_pct": 2.41, "base_join_pct": st["tags"]["base_hit_pct"],
                         "patent_sample_rate_pct": 6.81},
        },
    }
    write_out(METRIC, report)
    for r in rows:
        print(r["chain_code"], {c: (v["enterprise_count"], v["score"]) for c, v in r["cities"].items()})


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
    out_json = here / "M_CHAIN_ENTERPRISE_POWER_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_CHAIN_ENTERPRISE_POWER.py 等价）
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
        "metric_id": "M_CHAIN_ENTERPRISE_POWER",
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
