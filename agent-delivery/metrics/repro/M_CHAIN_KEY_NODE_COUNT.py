#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""关键节点数（M_CHAIN_KEY_NODE_COUNT）—— 环节集聚度代理，自包含。

需求/王惠 V2 的三因子定义是「附加值率 ≥ 同链环节均值、技术壁垒 ≥ 50、CR4 ≥ 0.5」
三因子同时过线后 COUNT(DISTINCT industry_link_code)。在 gkx：
  - 附加值率：需要环节级营收，gkx 只有企业级年报（且只覆盖上市主体），无环节分摊键；
  - 技术壁垒：需要「环节—专利」键，gkx 专利只有 IPC/申请人，无环节码；
  - CR4：同样卡在环节级营收。
三因子都不可算，故本件不冒充三因子，改用唯一在库内可得的一维「环节企业数」
做分位代理，并把代理的构造性缺陷写清：

  主值：叶级环节企业数 ≥ 该链叶级中位数 → 463/916（50.55%）。
        这是中位数分割的定义性质：任何分布都会切出约一半，**不是产业事实**。
  敏感性：P75 门槛 → 229/916（25.00%）；帕累托「覆盖链内 50% 企业的最少环节数」
        → 38 个（逐链 1—10 个，随链规模变化，才是有区分度的读数）。

产物：headline 主值 + sensitivity；chains[] 逐链三口径。

运行：cd code && python3 M_CHAIN_KEY_NODE_COUNT.py
产物：code/M_CHAIN_KEY_NODE_COUNT_out.json（覆盖写）
"""
from __future__ import annotations

import json
import os
import statistics
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_KEY_NODE_COUNT_out.json")

BASE_USED = []
BASE_MISSING = []
BASE_NOTE = '截面指标：统计当前存量，不设年度分母。'

SOURCES = [
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_org_industry_tags", "rows": 2283762,
     "snapshot": "code/_snapshots21/chain_panel21.json"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_industry_chain_info", "rows": 1273,
     "snapshot": "code/_snapshots21/chain_tree_20261021.json"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_org_annual_financial_info", "rows": 90926,
     "snapshot": "code/_snapshots21/chain_lm_fin_20261021.json"},
]


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def pareto_nodes(vals):
    """覆盖链内 50% 企业所需的最少环节数（按企业数降序累加）。"""
    total = sum(vals)
    if not total:
        return 0
    acc, k = 0, 0
    for v in sorted(vals, reverse=True):
        acc += v
        k += 1
        if acc >= total * 0.5:
            break
    return k


def main():
    t0 = time.time()
    panel = load("chain_panel21.json")
    LEAF_COV = load("chain_leaf_cov_20261022.json")
    chains = panel["chains"]

    rows = []
    for c in chains:
        lf = c.get("leaf_firms") or {}
        vals = sorted(v for v in lf.values() if v > 0)
        if not vals:
            rows.append({"chain": c["chain"], "name": c["name"], "value": 0,
                         "threshold": 0, "leaves_with_firms": 0, "leaves": c["leaves"],
                         "p75_threshold": 0, "p75_value": 0, "pareto_nodes": 0,
                         "leaf_firm_sum": 0, "chain_firms": c["firms"],
                         "nonleaf": None, "l1": None, "key_examples": []})
            continue
        med = statistics.median(vals)
        p75 = statistics.quantiles(vals, n=4)[2] if len(vals) >= 4 else max(vals)
        keys = [k for k, v in lf.items() if v >= med and v > 0]
        keys75 = [k for k, v in lf.items() if v >= p75 and v > 0]
        rows.append({
            "chain": c["chain"], "name": c["name"], "value": len(keys),
            "threshold": med, "leaves_with_firms": len(vals), "leaves": c["leaves"],
            "p75_threshold": p75, "p75_value": len(keys75),
            "pareto_nodes": pareto_nodes(vals),
            "leaf_firm_sum": sum(vals), "chain_firms": c["firms"],
            "nonleaf": None, "l1": None,
            "key_examples": [c.get("leaf_names", {}).get(k, k) for k in keys[:5]],
        })
    rows.sort(key=lambda r: -r["value"])

    leaves_covered = sum(r["leaves_with_firms"] for r in rows)
    total = sum(r["value"] for r in rows)
    total75 = sum(r["p75_value"] for r in rows)
    total_par = sum(r["pareto_nodes"] for r in rows)
    leaf_sum = sum(r["leaf_firm_sum"] for r in rows)
    chain_firms = sum(r["chain_firms"] for r in rows)
    leaves_total = sum(r["leaves"] for r in rows)

    headline = {
        "value": total,
        "unit": "个关键环节（中位数分位代理，占比恒约 50%）",
        "rule": "叶级环节企业数 ≥ 该链叶级中位数",
        "leaves_covered": leaves_covered,
        "leaves_total": leaves_total,
        "share": round(total / leaves_covered, 4) if leaves_covered else 0,
        "is_constructed_half": True,
    }
    sensitivity = {
        "p75_value": total75,
        "p75_share": round(total75 / leaves_covered, 4) if leaves_covered else 0,
        "p75_rule": "叶级环节企业数 ≥ 该链 P75（上四分位）",
        "pareto_nodes": total_par,
        "pareto_rule": "按企业数降序累加，覆盖链内 50% 企业所需的最少环节数",
        "pareto_range": f"{min(r['pareto_nodes'] for r in rows)}—{max(r['pareto_nodes'] for r in rows)}",
        "note": "三个口径都是代理：中位数与 P75 的占比由构造决定（50%/25%），"
                "只有帕累托口径的绝对值随链规模变化，建议前端用帕累托值或直接展示环节分布。",
    }
    facts = [
        {"label": "关键环节合计（中位数代理）", "value": total},
        {"label": "有企业环节合计", "value": leaves_covered},
        {"label": "构造占比（中位数规则）", "value": f"{headline['share']*100:.2f}%"},
        {"label": "敏感性：P75 口径", "value": f"{total75}（{sensitivity['p75_share']*100:.2f}%）"},
        {"label": "敏感性：帕累托口径", "value": total_par},
        {"label": "树侧覆盖：954 叶级中有企业", "value": f"{leaves_covered}（{leaves_covered/leaves_total*100:.2f}%）"},
    ]

    out = {
        "metric_id": "M_CHAIN_KEY_NODE_COUNT",
        "metric_name": "关键节点数",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": (
            "12 条链的叶级环节企业数均可得（916/954 个叶级环节有企业），但王惠 V2 的三因子里"
            "只有「企业规模」一维可算；附加值率与 CR4 卡在环节级营收、技术壁垒卡在环节—专利键，"
            "故只能给分位代理值（463，占比 50.55% 由中位数规则决定），"
            "不是三因子结论，判部分支持。"
        ),
        "sources": SOURCES,
        "base_years_used": BASE_USED,
        "base_years_missing": BASE_MISSING,
        "base_years_note": BASE_NOTE,
        "headline": headline,
        "sensitivity": sensitivity,
        "facts": facts,
        "chains": rows,
        "method_steps": [
            "读 chain_panel21.json 的逐链叶级企业数（来源：tags 的 industry_link_code 快照）",
            "逐链取叶级企业数中位数作主门槛，计数 ≥ 门槛的环节",
            "同口径再算 P75 门槛与帕累托 50% 覆盖，作为敏感性对照",
            "核对叶级企业数与链企业数：两列口径不同，逐链比值有 7 条超过 100%，"
            "故不给统一覆盖率，只给「954 叶级中 916 个有企业」这一树侧覆盖",
            "标注：三因子中仅企业规模可得，主值是下限代理，不是关键环节的完整判定",
        ],
        "population": {
            "defined_as": "链内叶级环节的企业数分布",
            "leaves_total": leaves_total,
            "leaves_with_firms": leaves_covered,
            "leaf_tree_coverage": round(leaves_covered / leaves_total, 4) if leaves_total else None,
            "leaf_firm_sum": leaf_sum,
            "leaf_firm_sum_note": "逐叶企业数直接相加，同一企业挂多个叶级环节会重复计入，"
                                   "是「环节—企业家次」而非「企业家数」，不可当分母或覆盖率",
            "chain_firms": chain_firms,
            "leaf_coverage_of_chain_firms": None,
            "leaf_coverage_note": "不给统一覆盖率：链归属取 industry_code（链根），环节取 "
                                  "industry_link_code（路径），两列口径不同。12 条链中 7 条的"
                                  "叶级去重企业数超过本链企业数（具身智能 682.64%、机器人 441.36%），"
                                  "相除得到的 91.38% 是两个不同母体的比值，不是覆盖率",
            "leaf_distinct_sum": LEAF_COV["totals"]["leaf_distinct_sum"],
            "leaf_distinct_sum_note": "逐链叶级去重企业数相加（%d），同一企业跨链会重复计入，"
                                      "同样不能当覆盖率" % LEAF_COV["totals"]["leaf_distinct_sum"],
            "chains_over_100_pct": sum(1 for r in LEAF_COV["per_chain"] if r["ratio"] > 1),
            "empty_link_rows": 569303,
            "empty_link_ratio": round(569303 / 2283762, 4),
            "link_rows_with_code": 1714459,
            "leaf_firm_sum_ratio_max": 2.5519,
            "leaf_firm_sum_ratio_max_pct": 255.19,
            "leaf_firm_sum_ratio_max_chain": "传感器（75,813 / 29,708）",
        },
        "leaf_coverage_by_chain": LEAF_COV["per_chain"],
        "compute": {
            "formula": "COUNT(leaf WHERE firm_count >= median(firm_count))",
            "proxy": True,
            "dims_available": 1,
            "dims_required": 3,
            "three_factor": {
                "value_added_rate": "不可算：无环节级营收，年报只有企业级且仅上市主体",
                "tech_barrier": "不可算：无环节—专利键（专利只有 IPC/申请人）",
                "cr4": "不可算：同上，缺环节级营收分母",
            },
        },
        "gaps": [
            "三因子中两维不可算：环节级营收与环节—专利键在 gkx 均不存在",
            "中位数代理的占比由构造决定（约 50%），不能用于链间排序",
            "叶级只覆盖有 link 码的行：叶级计位合计 1,566,734，仅为链企业 1,714,458 的 91.38%，另 8.62% 的链位没有环节码",
            "4 个叶级环节在 tags 中无企业（920 个环节里 916 个有值）",
            "importance_level 字段在 gkx 不存在，旧稿据此判「关键」的路径不可用",
        ],
        "difference_vs_old_draft": {
            "old_source": "演示库 chain_key_node 结果面（0 行）与 importance_level 列（114 行全空）",
            "old_note": "旧稿严格跑三因子漏斗，终点 0（34 家 2025 年有正营收、技术壁垒 0 个可算），"
                        "判 0 为「数据不足」；本件不重复该漏斗，改用企业规模分位代理给下限值 463",
            "now_source": "gkx.dwd_org_industry_tags link 码环节家数",
            "direction": "旧稿 0 与本件 463 不是同一口径：旧稿是三因子交点，本件是单维分位；"
                         "两者都不可当「关键环节」的最终答案",
        },
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("[ok]", "M_CHAIN_KEY_NODE_COUNT", json.dumps(headline, ensure_ascii=False),
          "p75", total75, "pareto", total_par, "chains", len(rows),
          "sec", round(time.time() - t0, 2))


if __name__ == "__main__":
    main()
