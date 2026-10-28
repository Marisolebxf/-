#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_SVC_SZ_COMPARE_METRIC 城市对比指标值
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_SVC_SZ_COMPARE_METRIC.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_SVC_SZ_COMPARE_METRIC｜城市对比指标值（深圳现状对比面板）。

面板是「城市 × 小项」多格，不是单一标量：
  orgCount      服务机构数量
  avgTechScore  城市平均技术力
  networkDensity 服务网络密度
本件逐格判「可发布 / 不可发布」，可发布的格必须与 M_SVC_PT_SZ_TOTAL 同数。

数据面：gkx（183.240.141.251:3318，只读 gkx_reader_zp）；零 SQL 运行。
产出：code/M_SVC_SZ_COMPARE_METRIC_out.json
运行：cd code && python3 M_SVC_SZ_COMPARE_METRIC.py
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FAM = os.path.join(SNAP, "svcsz21_facts_20261023.json")
OUT = os.path.join(HERE, "M_SVC_SZ_COMPARE_METRIC_out.json")

SZ = "深圳市"
POOL_CITIES = ["广州市", "东莞市", "惠州市"]
BENCH_CITIES = ["北京市", "上海市"]


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def pct(a, b):
    return round(a / b * 100, 2) if b else None


ITEMS = ["orgCount", "avgTechScore", "networkDensity"]


def main():
    fam = load(FAM)
    total = fam["pool"]["total"]
    sz_total = fam["pool"]["shenzhen"]
    city_rows = {r[0]: r[1] for r in fam["pool"]["city_rows"]}

    grid = []
    grid.append({
        "city": "深圳市",
        "orgCount": sz_total,
        "orgCount_status": "可发布",
        "orgCount_basis": "服务机构池 ∩ city='深圳市'；与 M_SVC_PT_SZ_TOTAL 同规则同数",
        "avgTechScore": None,
        "avgTechScore_status": "不可发布",
        "avgTechScore_basis": "MODEL 未签（Q-SVCCHAIN-01）；三子指标中研发投入/研发人员分子列整列为空",
        "networkDensity": None,
        "networkDensity_status": "不可发布",
        "networkDensity_basis": "无服务机构↔服务机构边（SVC-P1-1 未交付）；投资/股东边不是服务关系",
    })
    for c in POOL_CITIES:
        grid.append({
            "city": c,
            "orgCount": city_rows.get(c, 0),
            "orgCount_status": "样本值（不作发布格）",
            "orgCount_basis": "同池同规则可数，但池 100% 落广东，外市基准须甲方指定（Q-SVCCHAIN-04）",
            "avgTechScore": None,
            "avgTechScore_status": "不可发布",
            "avgTechScore_basis": "同深圳格：模型未签 + 两子指标分子为空",
            "networkDensity": None,
            "networkDensity_status": "不可发布",
            "networkDensity_basis": "无边源",
        })
    for c in BENCH_CITIES:
        grid.append({
            "city": c,
            "orgCount": city_rows.get(c, 0),
            "orgCount_status": "不可发布（0 家）",
            "orgCount_basis": "池内 0 家：底册回联 44,132 行 100% 为广东省，北京/上海无样本",
            "avgTechScore": None,
            "avgTechScore_status": "不可发布",
            "avgTechScore_basis": "无样本 + 模型未签",
            "networkDensity": None,
            "networkDensity_status": "不可发布",
            "networkDensity_basis": "无边源",
        })
    grid.append({
        "city": "全国平均",
        "orgCount": None,
        "orgCount_status": "不可发布",
        "orgCount_basis": "无全国服务机构池；用底册 189,116 全量工商按城平均是错误口径（会把制造业算进服务业）",
        "avgTechScore": None,
        "avgTechScore_status": "不可发布",
        "avgTechScore_basis": "无城市集合，均值无定义",
        "networkDensity": None,
        "networkDensity_status": "不可发布",
        "networkDensity_basis": "无边源",
    })
    grid.append({
        "city": "未回联底册",
        "orgCount": city_rows.get("", 0),
        "orgCount_status": "不入格",
        "orgCount_basis": "org_id 在底册无对应行，城市未知；单列不并入任何城市",
        "avgTechScore": None,
        "avgTechScore_status": "不适用",
        "avgTechScore_basis": "—",
        "networkDensity": None,
        "networkDensity_status": "不适用",
        "networkDensity_basis": "—",
    })

    # 可发布格统计
    live_cells = []
    for g in grid:
        for item in ITEMS:
            if g[item + "_status"] == "可发布":
                live_cells.append({"city": g["city"], "item": item, "value": g[item]})

    # 反证：投资/股东边存在，但不是服务关系
    counter_evidence = {
        "invest_edges_total": fam["edges"]["invest_edges_total"],
        "invest_edges_touching_sz": fam["edges"]["invest_edges_touching_sz"],
        "shareholder_edges_total": fam["edges"]["shareholder_edges_total"],
        "shareholder_edges_from_sz": fam["edges"]["shareholder_edges_from_sz"],
        "why_not_density": (
            "密度定义的分母是「服务机构 A —服务关系— 服务机构 B」的边集；"
            "投资边（dwd_org_invest_info）与股东边（dwd_org_shareholder_info）表达的是资本关系，"
            "同一对被投/持股主体里大量不是服务机构，且方向与语义都不同，"
            "拿来算密度会把「资本网络」冒充「服务网络」。"
        ),
    }

    out = {
        "metric_id": "M_SVC_SZ_COMPARE_METRIC",
        "metric_name": "城市对比指标值",
        "support_judgment": "部分支持",
        "judgment_reason": (
            "三小项 × 多城市的面板里，只有「深圳 × orgCount」一格可发布（25,597，与 M_SVC_PT_SZ_TOTAL 同数）；"
            "外市 orgCount 虽在同池内可数，但池 100% 落广东省、北京/上海 0 家，不构成城市基准；"
            "avgTechScore 三子指标有两个分子整列为空且模型未签；networkDensity 无服务机构间边源。"
            "九格中一格可发布、其余不可，故判部分支持。"
        ),
        "verdict_kind": "positive",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "本件是当期面板（截面），不使用基期年份；技术力若将来解挂，需要三子指标同一年份，"
            "而营收/员工最新有值年集中在 2014—2016，年份对齐是解挂前置条件之一。"
        ),
        "sources": {
            "library": "gkx",
            "host": "183.240.141.251:3318",
            "user": "gkx_reader_zp",
            "mode": "read-only",
            "tables": [
                "gkx.dwd_org_org_product_info（机构池）",
                "gkx.dwd_org_base_info（city）",
                "gkx.dwd_org_invest_info（投资边，反证用）",
                "gkx.dwd_org_shareholder_info（股东边，反证用）",
            ],
            "snapshots": [
                "code/_snapshots21/svcsz21_facts_20261023.json",
                "code/_snapshots21/svc21_facts_20261022.json",
            ],
            "calc_logic": "gkx-orchestration/agent-delivery/metrics/calc-logic/SVC/M_SVC_SZ_COMPARE_METRIC.md",
        },
        "params": {
            "items": ITEMS,
            "grid_cities": ["深圳市", "广州市", "东莞市", "惠州市", "北京市", "上海市", "全国平均"],
            "pool_total": total,
            "sz_total": sz_total,
            "publish_rule": "只有状态为「可发布」的格允许进 ADS / 前端 live；其余格保持 fixture + 排除声明",
        },
        "value": {
            "live_cells": len(live_cells),
            "total_cells": len(grid) * len(ITEMS),
            "sz_org_count": sz_total,
            "sz_org_count_share_of_pool_pct": pct(sz_total, total),
            "sz_org_count_share_of_pool_cities_pct": pct(
                sz_total, sz_total + sum(city_rows.get(c, 0) for c in POOL_CITIES)),
        },
        "grid": grid,
        "live_cell_detail": live_cells,
        "supplementary_sz": {
            "note": "以下量可披露，但不是面板三小项，不得填进 avgTechScore / networkDensity 格",
            "large_orgs": fam["size"]["rows"][0][1],
            "patent_matched_orgs": fam["patent"]["matched_orgs"],
            "patent_apps": fam["patent"]["apps"],
            "patent_grants": fam["patent"]["grants"],
            "risk_orgs": fam["risk"]["orgs_with_risk"],
            "news_orgs": fam["edges"]["news_sz_orgs"],
            "finance_event_orgs": fam["edges"]["finance_events_sz_orgs"],
            "stage_hit_orgs": fam["stage"]["hit_orgs"],
        },
        "counter_evidence": counter_evidence,
        "gaps": [
            {
                "gap": "外市/全国城市基准源缺失",
                "detail": "Q-SVCCHAIN-04 待甲方指定；现池北京/上海 0 家、全国平均无定义",
                "impact": "九个对比格里 6 格外市格全部不可发布，面板只能亮深圳一列",
                "fix": "甲方交付城市基准源（同口径服务机构圈定），或明确「仅深圳单列」的展示口径",
            },
            {
                "gap": "avgTechScore 模型未签 + 两子指标分子为空",
                "detail": "M_SVC_ORG_TECH_SCORE 定义卡未签（Q-SVCCHAIN-01 / 唐绍祖）；arch_development_am 与 development_employee 整列为空",
                "impact": "技术力整列不可发布，且不是「覆盖低」而是「列建好没灌数」",
                "fix": "先签算法定义卡，再补研发费用/研发人员数据源",
            },
            {
                "gap": "服务网络密度无边源",
                "detail": "SVC-P1-1 服务机构↔服务机构边未交付；gkx 无任何 svc_* 边表",
                "impact": "密度整列不可发布",
                "fix": "供方交付服务关系边；在此之前不得用投资/股东边替代",
            },
            {
                "gap": "未回联 21 家",
                "detail": "org_id 在底册无对应行，城市未知",
                "impact": "占池 0.05%，不并入任何城市格",
                "fix": "核对 org_id 或补底册行",
            },
        ],
        "cross_refs": {
            "M_SVC_PT_SZ_TOTAL": {"sz_org_count": sz_total, "same_number": True},
            "M_SVC_SZ_TIER": {"shared_grid": True},
            "M_SVC_SZ_CHAIN_COMPLETENESS": {"completeness_excluded": True,
                                            "note": "完整度另件，不属本面板三小项"},
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written", OUT)
    print("live_cells=%d / %d" % (len(live_cells), len(grid) * len(ITEMS)))
    print("sz_org=%d" % sz_total)


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
    out_json = here / "M_SVC_SZ_COMPARE_METRIC_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_SVC_SZ_COMPARE_METRIC.py 等价）
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
        "metric_id": "M_SVC_SZ_COMPARE_METRIC",
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
