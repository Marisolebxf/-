#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""市场营销服务机构技术力评价模型（M_SVC_DEEP_177_1）—— gkx 口径，自包含。

三维（需规 §1.1.1.1.1.1.1.9.6）：
    调研能力     —— 调研方法专业性/数据采集广度均无承载表 → 无源
    策划能力     —— 方案创新性/执行落地性/资源整合均无承载表 → 无源
    成功项目案例 —— 正式计数待建；现用资讯条数代理（弱）

结论形态：三维里只有第三维有代理量，故**不出「技术力指数」**，只出
「案例维代理分」与三维可得性矩阵——避免用一个弱代理冒充综合指数。

数据源：code/_snapshots21/svc21_facts_20261022.json（gkx 只读快照）
产出：code/M_SVC_DEEP_177_1_out.json
运行：cd code && python3 M_SVC_DEEP_177_1.py
"""
from __future__ import annotations

import json
import os
import statistics
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
OUT = os.path.join(HERE, "M_SVC_DEEP_177_1_out.json")


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
    pool, news, tags = f["pool"], f["news"], f["tags"]
    mkt_pool = [o for o, v in pool.items() if v.get("ptype2") == "MKT"]
    n = len(mkt_pool)

    newsc = {o: int(news.get(o, 0)) for o in mkt_pool}
    tagc = {o: int(tags.get(o, 0)) for o in mkt_pool}
    with_news = {o: v for o, v in newsc.items() if v > 0}
    score = {o: 100.0 * v for o, v in mm(with_news).items()}

    vals = sorted(newsc.values())
    news_total = sum(vals)
    top = sorted(with_news.items(), key=lambda x: -x[1])[:10]
    top_rows = [{"org_id": o, "name": pool[o]["name"], "city": pool[o]["city"],
                 "news": v, "case_proxy_score": round(score[o], 2), "tags": tagc[o]} for o, v in top]

    cov = {
        "调研能力": {"n": 0, "evidence": "无", "needed": "svc_research_score：调研报告份数、样本量、方法说明"},
        "策划能力": {"n": 0, "evidence": "无", "needed": "svc_planning_score：方案数、比稿中标、执行验收"},
        "成功项目案例": {"n": len(with_news), "evidence": "资讯条数（曝光度代理）",
                         "needed": "svc_success_case_count：项目数、行业分布、客户复购"},
    }

    out = {
        "metric_id": "M_SVC_DEEP_177_1",
        "metric_name": "市场营销服务机构技术力评价模型",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": ("三维中调研能力、策划能力在 gkx 无任何承载表（连弱代理都缺文本级命中），"
                            "仅成功项目案例有资讯条数代理 → 只能出单维代理分、不能合成技术力指数；"
                            "按「有部分维度可取」落部分支持，不因指数不可合成而降为完全不支持"),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_important_news_info", "rows": 1668414,
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_tech_tag", "rows": 202424,
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("资讯表无可靠业务年份口径（采集时点快照），故不设基期、不做趋势；"
                            "若后续接入 publish_time 可补年度序列，届时需重新声明基期"),
        "population": {"orgs_mkt_primary": n, "share_of_pool": round(n / len(pool), 6)},
        "dimension_availability": cov,
        "case_proxy": {"orgs_with_news": len(with_news), "share_of_pool": round(len(with_news) / n, 6) if n else None,
                       "news_total": news_total,
                       "news_median_all": statistics.median(vals) if vals else None,
                       "news_max": vals[-1] if vals else None,
                       "score_note": f"单维 min-max ×100，仅在 {len(with_news)} 家有资讯的机构内可比，不代表技术力"},
        "top10": top_rows,
        "index_withheld": {"reason": "3 维中 2 维无源；若强行用单维代理 ×100 冒充指数，会把曝光度当技术力",
                           "what_would_unblock": ["svc_research_score", "svc_planning_score",
                                                  "svc_success_case_count"]},
        "compute": {"elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("MKT 池", n, "有资讯", len(with_news), "资讯合计", news_total)
    print("top", [(t["name"], t["news"]) for t in top_rows[:3]])
    print("->", OUT)


if __name__ == "__main__":
    main()
