#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""瓶颈堵点判定（M_SVC_CHAIN_BOTTLENECK）—— gkx 口径，自包含。

公式沿用王惠口径（calc-logic 真源）：六环节并列分档，0→服务空白；≤1→薄弱环节；
平均服务深度非空且 <55→资源瓶颈；否则正常。三档互斥，优先空白、再薄弱、再瓶颈。
数据源全部换到 gkx 落盘快照（零 demo、零 helper import）。

数据源：
    code/_snapshots21/svc21_facts_20261022.json   pool + 六环节词表命中（gkx product_info）
    code/_snapshots21/svc21_kw_20261022.json      单词命中量（词表敏感性）
    code/_snapshots21/base_20261021.json          底册（城市）

产出：code/M_SVC_CHAIN_BOTTLENECK_out.json

运行：cd code && python3 M_SVC_CHAIN_BOTTLENECK.py
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter
from statistics import median

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
KW = os.path.join(SNAP, "svc21_kw_20261022.json")
BASE = os.path.join(SNAP, "base_20261021.json")
OUT = os.path.join(HERE, "M_SVC_CHAIN_BOTTLENECK_out.json")

STAGE_NAME = {
    "stage-research": "研发与科研合作",
    "stage-ip": "知识产权与标准",
    "stage-transfer": "技术转移与孵化",
    "stage-pilot": "中试熟化",
    "stage-testing": "检测认证",
    "stage-market": "市场化服务",
}
ORDER = list(STAGE_NAME)

BASE_NOTE = ("截面指标：六环节分档基于当前存量计数，无年度分母；"
             "第三档（资源瓶颈）依赖的「平均服务深度分」在 gkx 无任何来源，"
             "故 base_years 与深度窗口均不适用，已逐环节记 depth_status。")


def main():
    t0 = time.time()
    fact = json.load(open(FACTS, encoding="utf-8"))
    kw = json.load(open(KW, encoding="utf-8"))
    base = json.load(open(BASE, encoding="utf-8"))
    pool = fact["pool"]
    bmap = {r[0]: r for r in base}
    fin = fact["finance"]
    n_pool = len(pool)

    # 环节计数 + 环节内财务中位数（辅助证据，不参与分档）
    cnt = Counter()
    stage_ids = {s: [] for s in ORDER}
    for oid, v in pool.items():
        for s in v["stages"]:
            cnt[s] += 1
            stage_ids[s].append(oid)
    sz = {o for o in pool if (bmap.get(o) or ["", "", "", "", ""])[4] == "深圳市"}

    rows = []
    for s in ORDER:
        n = cnt.get(s, 0)
        ids = stage_ids[s]
        revs = []
        for o in ids:
            ys = fin.get(o) or {}
            for y in ("2024", "2023", "2025"):
                r = (ys.get(y) or {}).get("rev")
                if r:
                    revs.append(float(r))
                    break
        sz_n = sum(1 for o in ids if o in sz)
        share = n / n_pool
        # 相对短板档（本件自定辅助档，非需规三档；用于在「都有供给」时仍能排出强弱）
        if share < 0.005:
            rtier, rbasis = "极薄弱", "供给占比 < 0.5%（池内占比）"
        elif share < 0.05:
            rtier, rbasis = "薄弱", "0.5% ≤ 供给占比 < 5%"
        elif share < 0.20:
            rtier, rbasis = "偏紧", "5% ≤ 供给占比 < 20%"
        else:
            rtier, rbasis = "充足", "供给占比 ≥ 20%"
        if n == 0:
            tier, basis = "服务空白", "家数维：COUNT(DISTINCT org_id)=0"
        elif n <= 1:
            tier, basis = "薄弱环节", "家数维：COUNT(DISTINCT org_id)≤1"
        else:
            tier, basis = "有供给（档位待深度分）", "家数维未触发前两档；深度维无源"
        rows.append({
            "stage_id": s,
            "stage_name": STAGE_NAME[s],
            "org_count": n,
            "share_of_pool": round(n / n_pool, 6),
            "shenzhen_org_count": sz_n,
            "avg_depth": None,
            "depth_status": "无源（Q-SVCCHAIN-02 口径未签；gkx 无 svc_* 深度表）",
            "tier": tier,
            "tier_basis": basis,
            "relative_tier": rtier,
            "relative_basis": rbasis,
            "revenue_median_in_stage": round(median(revs), 2) if revs else None,
            "revenue_sample": len(revs),
        })

    tiers = Counter(r["tier"] for r in rows)
    rtiers = Counter(r["relative_tier"] for r in rows)

    out = {
        "metric_id": "M_SVC_CHAIN_BOTTLENECK",
        "metric_name": "瓶颈堵点判定",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": (
            "家数维可词表代理现转（六环节 30,776/776/13,878/8/4,533/10,702）；"
            "第三档「资源瓶颈」所需的平均服务深度分在 gkx/live 均无任何来源"
            "（Q-SVCCHAIN-02 口径未签、SVC-P0-3 成员表未建）→ 三档只能判前两档"),
        "formula_source": "calc-logic SVC/M_SVC_CHAIN_BOTTLENECK.md（王惠 20260829 口径）",
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_org_product_info", "rows": fact["population"]["product_info_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_annual_financial_info（环节内营收中位，辅助）",
             "rows": fact["finance_meta"]["rows_total"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_base_info（城市，经底册快照）",
             "rows": fact["population"]["base_all"],
             "snapshot": "code/_snapshots21/base_20261021.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_org_product_info(main_activities 单词计数)",
             "rows": kw["rows"], "snapshot": "code/_snapshots21/svc21_kw_20261022.json"},
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": BASE_NOTE,
        "thresholds": {"blank": 0, "weak": 1, "bottleneck_depth": 55,
                       "status": "演示阈值（Q-SVCCHAIN-03 未正式化）"},
        "population_orgs": n_pool,
        "stage_rows": rows,
        "tier_summary": dict(tiers),
        "relative_tier_summary": dict(rtiers),
        "relative_tier_rule": ("需规三档（空白/薄弱/资源瓶颈）要求深度分，而深度分无源 → 三档全部落在「有供给」；"
                               "为使结论仍有区分度，本件另设「相对短板档」，只按环节供给占池比切四段，"
                               "属本件辅助口径，不外推为官方分档，也不写入 ADS 档位字段"),
        "keyword_sensitivity": {
            "note": "单词命中量（全表 45,011 行）；窄词全 0 说明旧稿「研发服务空白」是词表造成的，不是产业事实",
            "narrow_zero": [k for k, v in kw["kw"].items()
                            if k in ("委托研发", "联合攻关", "大设施", "算力服务", "概念验证", "熟化")
                            and v == 0],
            "pairs": [
                {"word": "检验检测", "n": kw["kw"]["检验检测"]},
                {"word": "检测", "n": kw["kw"]["检测"]},
                {"word": "研发", "n": kw["kw"]["研发"]},
                {"word": "技术开发", "n": kw["kw"]["技术开发"]},
                {"word": "研究开发", "n": kw["kw"]["研究开发"]},
                {"word": "技术转让", "n": kw["kw"]["技术转让"]},
                {"word": "技术转移", "n": kw["kw"]["技术转移"]},
            ],
        },
        "difference_vs_old_draft": {
            "old_counts": "0/151/3/2/412/8（演示库 svc_org_circle 43,296 × 王惠窄词表）",
            "new_counts": "30,776/776/13,878/8/4,533/10,702（gkx 44,153 家 × 扩展词表）",
            "old_tier": "研发判「服务空白」，其余五环节「有供给」",
            "new_tier": "六环节均「有供给」，无空白/薄弱环节可判",
            "verdict": ("旧稿的「研发=服务空白」在 gkx 上无法复现：四个窄词在 45,011 条经营范围里"
                        "命中 0，但「研发」17,736 家、「技术开发」22,563 家——空白是词表产物，"
                        "换源后必须撤回该结论"),
        },
        "compute": {"status": "partial_depth_gap", "elapsed_sec": round(time.time() - t0, 3)},
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for r in rows:
        print("%-16s n=%-6d tier=%s relative=%s share=%.4f" %
              (r["stage_id"], r["org_count"], r["tier"], r["relative_tier"], r["share_of_pool"]))
    print("tiers=%s -> %s" % (dict(tiers), OUT))


if __name__ == "__main__":
    main()
