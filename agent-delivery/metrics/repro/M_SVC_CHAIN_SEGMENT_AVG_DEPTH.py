#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""环节平均服务深度（M_SVC_CHAIN_SEGMENT_AVG_DEPTH）—— gkx 口径，自包含。

目标口径（calc-logic 0.2.0）：
    avg_depth(s) = AVG(depth_i) ,  i ∈ 环节 s 内的机构
    分子 depth_i = 机构在该环节的服务深度分（0—100，沿 M_SVC_ORG_COVERAGE_DEPTH）
    空环节 / 无深度 → 返回空（页面「—」），**不伪造 0**

本件实测结论：分子在 gkx 无任何可辩护来源。
    · gkx 280 表中不存在 svc_* 任何表（20261021 版已禁引演示库的 svc_* 结果面）
    · `M_SVC_ORG_COVERAGE_DEPTH` 公式未签（Q-SVCCHAIN-02）→ 无口径即无分
    · gkx 内四个可作「深度原料」的列（研发人员/研发费用/期刊影响因子/下载数）
      中有两列整列为空（DATA_FACTS §3.10），另两列属论文域，不能代理机构服务深度
因此本脚本产出的是「分母与分组（可算）+ 分子（无源）」的结构化证据，
每格 avg_depth 显式写 null，并写 depth_status。

数据源：
    code/_snapshots21/svc21_facts_20261022.json
    code/_snapshots21/svc21_kw_20261022.json
    code/_snapshots21/city_family_probe_20261021.json（§3.10 四列非空自检的实测证据）

运行：cd code && python3 M_SVC_CHAIN_SEGMENT_AVG_DEPTH.py
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
KW = os.path.join(SNAP, "svc21_kw_20261022.json")
PROBE = os.path.join(SNAP, "city_family_probe_20261021.json")
OUT = os.path.join(HERE, "M_SVC_CHAIN_SEGMENT_AVG_DEPTH_out.json")

STAGE_NAME = {
    "stage-research": "研发与科研合作",
    "stage-ip": "知识产权与标准",
    "stage-transfer": "技术转移与孵化",
    "stage-pilot": "中试熟化",
    "stage-testing": "检测认证",
    "stage-market": "市场化服务",
}
ORDER = list(STAGE_NAME)

BASE_NOTE = ("本件不产出任何深度数值：分子（机构×环节服务深度分）在 gkx 与 live 均无来源，"
             "口径未签（Q-SVCCHAIN-02），故不存在可声明的基期窗口；分母侧的环节计数为截面存量。")

# DATA_FACTS §3.10 的四列（整列为空），此处只做「本件是否误用」的负向证据
EMPTY_COLS = [
    ("dwd_org_annual_financial_info", "development_employee"),
    ("dwd_org_annual_financial_info", "arch_development_am"),
    ("dwd_zh_journal", "impact_score"),
    ("dwd_zh_paper", "download_num"),
]


def main():
    t0 = time.time()
    fact = json.load(open(FACTS, encoding="utf-8"))
    kw = json.load(open(KW, encoding="utf-8"))
    probe = json.load(open(PROBE, encoding="utf-8")) if os.path.exists(PROBE) else {}
    pool = fact["pool"]
    n_pool = len(pool)

    cnt = Counter()
    for v in pool.values():
        for s in v["stages"]:
            cnt[s] += 1

    rows = []
    for s in ORDER:
        n = cnt.get(s, 0)
        rows.append({
            "stage_id": s,
            "stage_name": STAGE_NAME[s],
            "org_count": n,
            "avg_depth": None,
            "display": "—",
            "depth_status": "无源",
            "empty_rule": ("环节无机构 → 空" if n == 0 else "环节有机构但深度分缺失 → 空（不伪造 0）"),
        })

    # 四列空值自检证据（只读快照，不再查库）
    empty_evidence = []
    probes = {}
    if isinstance(probe, dict):
        for k in ("zero_cols", "empty_cols", "col_nonnull", "cols"):
            if k in probe:
                probes[k] = probe[k]
    for t, c in EMPTY_COLS:
        empty_evidence.append({"table": t, "column": c,
                               "known_fact": "非空/非零计数 0（DATA_FACTS §3.10，2026-10-22 08:00 逐列探针）",
                               "used_by_this_metric": False})

    out = {
        "metric_id": "M_SVC_CHAIN_SEGMENT_AVG_DEPTH",
        "metric_name": "环节平均服务深度",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": (
            "分母与分组可算（六环节 44,153 家口径）；分子「机构×环节服务深度分」无源："
            "口径未签（Q-SVCCHAIN-02）且 gkx 无任何 svc_* 深度表/列 → 全部分格为「—」"),
        "formula_source": "calc-logic SVC/M_SVC_CHAIN_SEGMENT_AVG_DEPTH.md（0.2.0 目标口径）",
        "formula": "avg_depth(s) = AVG(depth_i), i ∈ {org: stage(org)=s}；空 → null（不伪造 0）",
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_org_product_info（分母/分组）",
             "rows": fact["population"]["product_info_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_org_product_info(main_activities 单词计数)",
             "rows": kw["rows"], "snapshot": "code/_snapshots21/svc21_kw_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "四列整列为空自检（development_employee / arch_development_am / "
                      "impact_score / download_num）",
             "snapshot": "code/_snapshots21/city_family_probe_20261021.json"},
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": BASE_NOTE,
        "population_orgs": n_pool,
        # 财务覆盖家数（=6759 的来源），供正文「全池 6,759 家有年报」溯源
        "finance_cover": len(fact.get("finance") or {}),
        "stage_rows": rows,
        "depth_gap": {
            "missing_input": "机构×环节 服务深度分（0—100）",
            "blocking": ["Q-SVCCHAIN-02 口径未签", "SVC-P0-3 机构×环节成员表未建",
                         "gkx 无 svc_* 结果面/深度列"],
            "rejected_alternatives": [
                {"alt": "研发人员数（development_employee）", "why": "整列为空（0 行非空）"},
                {"alt": "研发费用（arch_development_am）", "why": "整列为空（0 行非空）"},
                {"alt": "上市研发费用（dwd_org_stock_finance_info）", "why": "仅上市主体，且是投入口径不是服务深度"},
                {"alt": "环节家数归一化", "why": "把广度当深度，语义造假"},
                {"alt": "产业链环节覆盖率（industry_link_code）", "why": "码域与链树不一致（§3.9），且是产业轴不是服务环节轴"},
            ],
            "empty_column_evidence": empty_evidence,
        },
        "difference_vs_old_draft": {
            "old": "演示库 svc_chain_gap 6 行 fixture（研发 93.02 等，pending_client_confirm=1），正文判定不可引用",
            "new": "gkx 无同名表，深度分在源侧即不存在；本件六格全部「—」",
            "conclusion": "两版结论同向（不可算），但证据不同：旧稿靠「壳表有值但矛盾」，本件靠「源侧无表无列」",
        },
        "compute": {"status": "dual_gap", "elapsed_sec": round(time.time() - t0, 3)},
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("六环节 avg_depth 全部为 null；分母：", {r["stage_id"]: r["org_count"] for r in rows})
    print("->", OUT)


if __name__ == "__main__":
    main()
