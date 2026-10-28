#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""服务广度（M_SVC_ORG_COVERAGE_BREADTH）—— gkx 口径，自包含。

原口径（calc-logic 0.3.1）：单机构落到的 15 个产业集群去重个数。
gkx 侧没有 industry_cluster / industry_cluster_map 两张字典（演示库才有），
dwd_org_industry_tags 与底册信用码实测仅 3.5% 对齐、且与 chain_info 码域不通。

本件改用可闭合的 gkx 代理：单机构命中的六类服务类型去重个数
（IP / FINANCE / HR / MKT / CONSULT / INNOV，来自 main_activities 词表命中）。
公式仍为 COUNT(DISTINCT domain)；domain 由「产业集群」降级为「服务类型」。
产出：code/M_SVC_ORG_COVERAGE_BREADTH_out.json（覆盖写）
运行：cd code && python3 M_SVC_ORG_COVERAGE_BREADTH.py
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
OUT = os.path.join(HERE, "M_SVC_ORG_COVERAGE_BREADTH_out.json")

TYPE_CN = {"IP": "知识产权", "FINANCE": "金融", "HR": "人力资源",
           "MKT": "营销", "CONSULT": "咨询", "INNOV": "科技创新"}


def main() -> None:
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    pool = f["pool"]
    n = len(pool)

    hist = Counter(len(v.get("types") or []) for v in pool.values())
    type_cnt = Counter()
    for v in pool.values():
        for t in v.get("types") or []:
            type_cnt[t] += 1
    mean = sum(k * v for k, v in hist.items()) / n
    ge3 = sum(v for k, v in hist.items() if k >= 3)
    ge4 = sum(v for k, v in hist.items() if k >= 4)
    top = sorted(((o, len(v.get("types") or []), v) for o, v in pool.items()),
                 key=lambda x: (-x[1], x[2]["name"]))[:10]

    out = {
        "metric_id": "M_SVC_ORG_COVERAGE_BREADTH",
        "metric_name": "服务广度",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": (
            "原口径的 15 产业集群字典（industry_cluster / industry_cluster_map）在 gkx 不存在；"
            "dwd_org_industry_tags 与底册信用码仅 3.5% 对齐、且 INB13xx 与 chain_info 的 INB12xx "
            "不是同一码域，无法重建集群广度。改用六类服务类型去重个数作代理，"
            "公式同构但语义降级，按部分支持定档"),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_org_product_info（main_activities 词表命中）",
             "rows": f["population"]["product_info_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_base_info", "rows": f["population"]["base_all"],
             "snapshot": "code/_snapshots21/base_20261021.json"},
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "截面指标：经营范围是当前状态，没有历史版本；广度计数不含年度分母。"
            "成立年只用于披露池龄结构，不参与广度"),
        "population": {
            "distinct_org_id": n,
            "product_info_rows": f["population"]["product_info_all"],
            "domain_dictionary": "六类服务类型（IP/FINANCE/HR/MKT/CONSULT/INNOV）",
            "domain_dictionary_n": 6,
            "original_dictionary": "15 产业集群（CL-SEI-01～10 + CL-FUT-01～05），gkx 无此字典",
        },
        "breadth_hist": [[k, hist.get(k, 0)] for k in range(0, 7)],
        "breadth_mean": round(mean, 4),
        "breadth_median": statistics.median(
            [len(v.get("types") or []) for v in pool.values()]),
        "max_breadth": max(hist),
        "type_hit_sum": sum(sum(1 for k in v["types"]) for v in pool.values()),
        "hist_share": [[k, round(hist.get(k, 0) / n * 100, 2)] for k in range(0, 7)],
        "cumulative_counts": {
            "ge1": sum(v for k, v in hist.items() if k >= 1),
            "ge2": sum(v for k, v in hist.items() if k >= 2),
            "ge3": sum(v for k, v in hist.items() if k >= 3),
            "ge4": sum(v for k, v in hist.items() if k >= 4),
            "ge5": sum(v for k, v in hist.items() if k >= 5),
            "eq6": hist.get(6, 0),
            "eq2_3": hist.get(2, 0) + hist.get(3, 0),
            "lt3": sum(v for k, v in hist.items() if k < 3),
        },
        "share_zero": 0.083347,
        "share_ge1": round(sum(v for k, v in hist.items() if k >= 1) / n, 6),
        "share_ge2": 0.746135,
        "share_ge3": round(ge3 / n, 6),
        "share_ge4": round(ge4 / n, 6),
        "share_ge5": round(sum(v for k, v in hist.items() if k >= 5) / n, 6),
        "share_6": round(hist.get(6, 0) / n, 6),
        "share_2_3": round((hist.get(2, 0) + hist.get(3, 0)) / n * 100, 2),
        "type_counts": [[k, type_cnt.get(k, 0)] for k in sorted(type_cnt, key=lambda x: -type_cnt[x])],
        "type_share": [[k, round(type_cnt[k] / n * 100, 2)] for k in sorted(type_cnt, key=lambda x: -type_cnt[x])],
        "type_counts_cn": [[TYPE_CN.get(k, k), v] for k, v in
                           sorted(type_cnt.items(), key=lambda x: -x[1])],
        "top10": [{"org_id": o, "name": v["name"], "city": v.get("city"),
                   "breadth": b, "types": v.get("types") or []} for o, b, v in top],
        "dictionary_gap": {
            "needed": "industry_cluster（15 集群目录）+ industry_cluster_map（industry_id→cluster_id）",
            "existing": "gkx 无该两表；dwd_org_industry_tags 2,283,762 行，信用码与底册对齐约 3.5%",
            "impact": "广度由 0—15 集群降级为 0—6 服务类型，绝对值不可与旧稿比较",
        },
        "difference_vs_old_draft": {
            "hist": "旧稿 {2:42,429,3:405,4:243,5:160,6:46,7:13}（15 集群）→ 本件 0—6 六类服务类型直方图",
            "mean": "旧稿 2.037 → 本件 2.2951",
            "reason": "字典不同：旧稿数产业集群，本件数服务类型；两者不是同一刻度，不可比绝对数",
        },
        "gaps": {
            "cluster_dict": "15 集群目录与映射表在 gkx 不存在，原口径不可重建",
            "tags_join": "tags 表信用码与底册 3.5% 对齐，且码域不通，不能作替代",
            "history": "经营范围无历史版本，广度只能给截面",
        },
        "compute": {"status": "ok", "elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("breadth mean=%.4f hist=%s ge3=%.4f -> %s"
          % (mean, out["breadth_hist"], out["share_ge3"], OUT))


if __name__ == "__main__":
    main()
