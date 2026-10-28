#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""金融服务机构技术力评价模型（M_SVC_DEEP_174_1）—— gkx 口径，自包含。

四维（需规 §1.1.1.1.1.1.1.9.3）：
    资金规模 = 资产总额 + 注册资本
    融资成本 = 无利率源（缺维，不补 0、不进平均）
    资金风险 = 资产负债率反向 + 失信/处罚件数反向
    服务质量 = 资讯提及量代理（正式分待建）

合成：各维截面 min-max → [0,1]；等权平均（只对非空维求平均）；×100。
阈值：>=70 强 / 50-70 中 / <50 弱（等分位三分）。

数据源：code/_snapshots21/svc21_facts_20261022.json（gkx 只读快照）
产出：code/M_SVC_DEEP_174_1_out.json
运行：cd code && python3 M_SVC_DEEP_174_1.py
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
OUT = os.path.join(HERE, "M_SVC_DEEP_174_1_out.json")


# ---- mm()/latest() 与 M_SVC_CHAIN_SEGMENT_ORG_COUNT.py 同源（内联复制，不 import 共享模块）----
def mm(vals: dict) -> dict:
    """min-max 到 [0,1]；全体同值时给 0.5（无区分度，不制造极值）。"""
    xs = [v for v in vals.values() if v is not None]
    if not xs:
        return {}
    lo, hi = min(xs), max(xs)
    if hi - lo <= 1e-12:
        return {k: 0.5 for k in vals if vals[k] is not None}
    return {k: (v - lo) / (hi - lo) for k, v in vals.items() if v is not None}


def latest(fin: dict, keys=("rev", "ta", "tl", "np", "emp")):
    """取最近一个有值的年份（不为缺失年补 0，见 DATA_FACTS 3.16）。"""
    for y in sorted(fin, reverse=True):
        row = fin[y] or {}
        if any(row.get(k) is not None for k in keys):
            return y, row
    return None, {}


def main():
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    pool, fin, risk, news, tags = f["pool"], f["finance"], f["risk"], f["news"], f["tags"]
    bf = f.get("base_fields") or {}
    fin_meta = f["finance_meta"]

    fin_pool = [o for o, v in pool.items() if v.get("ptype2") == "FINANCE"]
    n = len(fin_pool)

    cap, asset, debt, riskcnt, newsc, tagc, reven, prof = {}, {}, {}, {}, {}, {}, {}, {}
    years_used = Counter()
    for o in fin_pool:
        c = (bf.get(o) or {}).get("cap")
        if c:
            cap[o] = float(c)
        y, row = latest(fin.get(o) or {})
        if row.get("ta") is not None:
            asset[o] = float(row["ta"])
            years_used[y] += 1
        if row.get("ta") not in (None, 0) and row.get("tl") is not None:
            debt[o] = float(row["tl"]) / float(row["ta"])
        if row.get("rev") is not None:
            reven[o] = float(row["rev"])
            if row.get("np") is not None and row["rev"]:
                prof[o] = float(row["np"]) / float(row["rev"])
        r = risk.get(o) or {}
        riskcnt[o] = int(r.get("shixin", 0)) + int(r.get("punish", 0))
        newsc[o] = int(news.get(o, 0))
        tagc[o] = int(tags.get(o, 0))

    s_size = {}
    aset_n, cap_n = mm(asset), mm(cap)
    for o in fin_pool:
        parts = [x for x in (aset_n.get(o), cap_n.get(o)) if x is not None]
        if parts:
            s_size[o] = sum(parts) / len(parts)

    s_risk = {}
    debt_n = mm(debt)
    rk_n = mm({o: -v for o, v in riskcnt.items()})
    for o in fin_pool:
        parts = []
        if o in debt_n:
            parts.append(1.0 - debt_n[o])
        if o in rk_n:
            parts.append(rk_n[o])
        if parts:
            s_risk[o] = sum(parts) / len(parts)

    s_qual = mm({o: v for o, v in newsc.items() if v > 0})

    dims = {"资金规模": s_size, "融资成本": {}, "资金风险": s_risk, "服务质量": s_qual}
    weights = {"资金规模": 0.25, "融资成本": 0.25, "资金风险": 0.25, "服务质量": 0.25}

    idx, used = {}, {}
    for o in fin_pool:
        av = [(k, dims[k][o]) for k in dims if o in dims[k]]
        if len(av) < 2:
            continue
        wsum = sum(weights[k] for k, _ in av)
        idx[o] = 100.0 * sum(weights[k] * v for k, v in av) / wsum
        used[o] = [k for k, _ in av]

    vals = sorted(idx.values())
    bands = {"强(>=70)": 0, "中(50-70)": 0, "弱(<50)": 0}
    for v in vals:
        bands["强(>=70)" if v >= 70 else ("中(50-70)" if v >= 50 else "弱(<50)")] += 1

    ranked = sorted(idx.items(), key=lambda x: -x[1])
    top = [{"org_id": o, "name": pool[o]["name"], "city": pool[o]["city"],
            "index": round(v, 2), "dims": used[o], "asset": asset.get(o), "cap": cap.get(o),
            "debt_ratio": round(debt[o], 4) if o in debt else None,
            "risk_cnt": riskcnt.get(o), "news": newsc.get(o)} for o, v in ranked[:10]]
    bottom = [{"org_id": o, "name": pool[o]["name"], "index": round(v, 2),
               "dims": used[o], "risk_cnt": riskcnt.get(o)} for o, v in ranked[-5:]]

    dim_cov = {k: {"n": len(v), "share_of_pool": round(len(v) / n, 6)} for k, v in dims.items()}
    dim_n = Counter(len(used[o]) for o in used)

    out = {
        "metric_id": "M_SVC_DEEP_174_1",
        "metric_name": "金融服务机构技术力评价模型",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": ("四维中资金规模、资金风险、服务质量三维可现转；融资成本维全库无利率字段、"
                            "结构性无源（待建 financing_cost_rate），故为部分支持，不抬档"),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_annual_financial_info", "rows": fin_meta["rows_total"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_base_info(cap) + dwd_org_risk_shixin + dwd_org_company_punish + dwd_org_important_news_info",
             "rows": 189116, "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
        ],
        "base_years_used": list(range(2007, 2026)),
        "base_years_missing": [2026],
        "base_years_note": ("财务表实际覆盖 2007—2025 共 19 个年份，used 记整段；"
                            "每个机构取自己最近一个有财务值的年份作截面，未把缺年按 0 摊入；"
                            "2026 无财务行，missing 记 2026"),
        "years_used": {str(k): v for k, v in sorted(years_used.items(), key=lambda x: -x[1])[:8]},
        "population": {"orgs_finance_primary": n, "share_of_svc_pool": round(n / len(pool), 6)},
        "dimensions": dim_cov,
        "dimension_scores_note": "min-max 到 [0,1]，等权 0.25；空维不进平均、不补 0；<2 维不出指数",
        "index": {"n": len(idx), "mean": round(statistics.mean(vals), 2) if vals else None,
                  "median": round(statistics.median(vals), 2) if vals else None,
                  "p25": round(vals[len(vals) // 4], 2) if vals else None,
                  "p75": round(vals[3 * len(vals) // 4], 2) if vals else None,
                  "max": round(vals[-1], 2) if vals else None,
                  "min": round(vals[0], 2) if vals else None},
        "bands": bands,
        "dim_count_dist": {str(k): v for k, v in sorted(dim_n.items())},
        "top10": top,
        "bottom5": bottom,
        "grade_thresholds": {"strong": 70, "mid": 50,
                             "basis": "等分位三分，需规只要求合理阈值，本件不虚构行业均值"},
        "quality_proxy": {"source": "gkx.dwd_org_important_news_info 标题条数",
                          "coverage": len([o for o in fin_pool if newsc.get(o)]),
                          "limit": "曝光度代理，不等于客户满意度；正式分待建"},
        "cost_dim_gap": {"needed": "financing_cost_rate（利率/费率/融资成本明细）",
                         "existing": "gkx.dwd_org_financing_info 仅事件 + 金额，无利率列",
                         "impact": "该维权重 0.25 常年由其余三维分摊，指数语义缺一角"},
        "tag_coverage": {"orgs_with_tag": len([o for o in fin_pool if tagc.get(o)]),
                         "note": "技术标签仅作旁证，不进四维"},
        "compute": {"elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("FINANCE 池", n, "指数覆盖", len(idx), "均/中位", out["index"]["mean"], out["index"]["median"])
    print("分维覆盖", {k: v["n"] for k, v in dim_cov.items()})
    print("档位分布", bands, "维数分布", dict(dim_n))
    print("top1", top[0]["name"] if top else None, top[0]["index"] if top else None)
    print("->", OUT)


if __name__ == "__main__":
    main()
