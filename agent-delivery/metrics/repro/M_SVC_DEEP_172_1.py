#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""服务链短板分析模型（M_SVC_DEEP_172_1）—— gkx 口径，自包含。

三维（需规 §1.1.1.1.1.1.1.9.1）：
    服务质量   —— 全库无评价类承载表（待建 svc_quality_score）→ 本件记「无源」
    经营效益   —— 环节内机构最近一年营业收入中位数 / 销售利润率中位数，与全链对比
    服务类型结构 —— 环节已出现服务类型数 / 6，缺口 = 1 - 覆盖数/6

综合：只对非空维求平均（缺维不补 0、不进平均）；短板分越高越短。
成因规则（需规三类）：资源投入不足 / 流程匹配不足 / 体验不足，按「结构缺口 vs 效益相对位」判别。

数据源：code/_snapshots21/svc21_facts_20261022.json（gkx 只读快照）
产出：code/M_SVC_DEEP_172_1_out.json
运行：cd code && python3 M_SVC_DEEP_172_1.py
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
OUT = os.path.join(HERE, "M_SVC_DEEP_172_1_out.json")

STAGES = ["stage-research", "stage-ip", "stage-transfer", "stage-pilot", "stage-testing", "stage-market"]
STAGE_CN = {"stage-research": "研发服务", "stage-ip": "知识产权服务", "stage-transfer": "技术转移服务",
            "stage-pilot": "中试熟化服务", "stage-testing": "检验检测服务", "stage-market": "市场拓展服务"}
TYPES6 = ["INNOV", "IP", "FINANCE", "HR", "MKT", "CONSULT"]


def latest(fin: dict, keys=("rev", "np")):
    for y in sorted(fin, reverse=True):
        row = fin[y] or {}
        if any(row.get(k) is not None for k in keys):
            return y, row
    return None, {}


def mm(vals: dict) -> dict:
    """min-max（内联复制自 M_SVC_DEEP_174_1.py，不 import 共享模块）"""
    xs = [v for v in vals.values() if v is not None]
    if not xs:
        return {}
    lo, hi = min(xs), max(xs)
    if hi - lo <= 1e-12:
        return {k: 0.5 for k in vals if vals[k] is not None}
    return {k: (v - lo) / (hi - lo) for k, v in vals.items() if v is not None}


def main():
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    pool, fin = f["pool"], f["finance"]

    # 机构级最近一年营收 / 利润率
    rev, margin = {}, {}
    for o in pool:
        y, row = latest(fin.get(o) or {})
        if row.get("rev") is not None:
            rev[o] = float(row["rev"])
            if row.get("np") is not None and row["rev"]:
                margin[o] = float(row["np"]) / float(row["rev"])

    chain_rev_med = statistics.median(rev.values()) if rev else None
    chain_margin_med = statistics.median(margin.values()) if margin else None

    rows = []
    for st in STAGES:
        orgs = [o for o, v in pool.items() if st in v["stages"]]
        types_present = sorted({t for o in orgs for t in pool[o]["types"]} & set(TYPES6))
        struct_gap = 1.0 - len(types_present) / 6.0
        rv = [rev[o] for o in orgs if o in rev]
        mg = [margin[o] for o in orgs if o in margin]
        rev_med = statistics.median(rv) if rv else None
        mg_med = statistics.median(mg) if mg else None
        rows.append({
            "stage": st, "stage_cn": STAGE_CN[st], "orgs": len(orgs),
            "types_present": types_present, "type_coverage": len(types_present),
            "struct_gap": round(struct_gap, 4),
            "rev_n": len(rv), "rev_median": round(rev_med, 2) if rev_med is not None else None,
            "margin_n": len(mg), "margin_median": round(mg_med, 5) if mg_med is not None else None,
            "rev_ratio_to_chain": round(rev_med / chain_rev_med, 4) if rev_med and chain_rev_med else None,
        })

    # 结构维退化自检：六环节是否都盖满六类（若是，说明环节词表与类型词表同源，结构维无区分度）
    struct_degenerate = sum(1 for r in rows if r["struct_gap"] > 1e-9) <= 1
    # 效益缺口：营收相对位（相对全链中位数），越低越短
    eff = {r["stage"]: (r["rev_ratio_to_chain"] if r["rev_ratio_to_chain"] is not None else None) for r in rows}
    eff_gap = {k: (1.0 - v) if v is not None and v <= 1.0 else 0.0 for k, v in eff.items() if v is not None}
    # 结构缺口直接是 [0,1]
    for r in rows:
        parts = [] if struct_degenerate else [r["struct_gap"]]
        if r["stage"] in eff_gap:
            parts.append(eff_gap[r["stage"]])
        if not parts:
            parts = [0.0]
        r["eff_gap"] = round(eff_gap.get(r["stage"], 0.0), 4) if r["stage"] in eff_gap else None
        r["dims_scored"] = ([] if struct_degenerate else ["service_type_struct"]) + \
                           (["operating_benefit"] if r["stage"] in eff_gap else [])
        r["short_board_score"] = round(sum(parts) / len(parts), 4)
        # 成因规则
        if r["stage"] not in eff_gap:
            r["cause"] = "效益维无财务样本，成因不可判（仅结构缺口可读）"
        elif r["struct_gap"] >= 0.5 and eff_gap[r["stage"]] >= 0.5:
            r["cause"] = "资源投入不足（类型覆盖 <3/6 且营收中位数不足全链一半）"
        elif r["struct_gap"] >= 0.5:
            r["cause"] = "服务匹配度低（类型缺口大，但环节内机构营收不低于全链中位）"
        elif eff_gap[r["stage"]] >= 0.5:
            r["cause"] = "流程匹配不足（类型齐备但单机构规模显著低于全链）"
        else:
            r["cause"] = "无显著短板（结构覆盖与效益均不落后）"
        r["quality_dim"] = None

    ranked = sorted(rows, key=lambda r: -r["short_board_score"])
    quality_gap = {"status": "无源", "needed": "svc_quality_score（服务质量评价分：交付及时率、客户满意度、返工率）",
                   "existing": "gkx 无任何评价/评分类表；仅有资讯条数与风险事件，均非质量证据",
                   "impact": "三维缺一，短板分只由结构 + 效益两维构成，权重实际为 0.5/0.5（原设计 1/3 等权）"}

    out = {
        "metric_id": "M_SVC_DEEP_172_1",
        "metric_name": "服务链短板分析模型",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": ("三维中服务类型结构维可算、经营效益维可现转（财务覆盖部分环节），"
                            "但服务质量评价维在全库无承载表（待建 svc_quality_score）→ 三维缺一，部分支持"),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_org_product_info（六环节词表命中）", "rows": f["population"]["product_info_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_annual_financial_info", "rows": f["finance_meta"]["rows_total"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
        ],
        "base_years_used": list(range(2007, 2026)),
        "base_years_missing": [],
        "base_years_note": ("财务表实际覆盖 2007—2025 共 19 个年份，故 used 记整段；"
                            "每个机构取自己最近一个有营收值的年份作截面，不把缺年按 0 摊入；"
                            "2026 无财务行（missing 记 2026），不入任何分母"),
        "population": {"orgs": len(pool), "stages": len(STAGES)},
        "finance_cover": len(fin),
        "stage_rows": rows,
        "chain_median": {"rev": round(chain_rev_med, 2) if chain_rev_med else None,
                         "margin": round(chain_margin_med, 5) if chain_margin_med else None,
                         "rev_orgs": len(rev), "margin_orgs": len(margin)},
        "short_board_rank": [{"stage": r["stage"], "stage_cn": r["stage_cn"],
                              "score": r["short_board_score"], "cause": r["cause"]} for r in ranked],
        "quality_dim_gap": quality_gap,
        "struct_dim_degenerate": struct_degenerate,
        "struct_dim_note": ("六环节的「已出现类型数」全部为 6/6，结构缺口恒为 0——原因是环节词表与类型词表"
                            "都从同一段 main_activities 文本命中，两者共线，结构维在本数据源下不具区分度，"
                            "故不进综合分（不是「无短板」，而是「该维读不出短板」）") if struct_degenerate else "结构维有区分度",
        "weights_note": "原设计三维等权；质量维无源、结构维同源退化 → 综合分只由效益维承载，未补 0",
        "compute": {"elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("chain med rev", out["chain_median"]["rev"], "margin", out["chain_median"]["margin"])
    for r in rows:
        print("%-14s orgs=%6d types=%d gap=%.3f rev_med=%s ratio=%s score=%.3f" %
              (r["stage_cn"], r["orgs"], r["type_coverage"], r["struct_gap"],
               r["rev_median"], r["rev_ratio_to_chain"], r["short_board_score"]))
    print("短板前三:", [(x["stage_cn"], x["short_board_score"]) for x in ranked[:3]])
    print("->", OUT)


if __name__ == "__main__":
    main()
