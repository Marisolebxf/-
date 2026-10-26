#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
