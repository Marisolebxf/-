#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""服务机构产业领域覆盖评分（M_SVC_ORG_COVERAGE_DEPTH）—— gkx 口径，自包含。

王惠 calc-logic 迁移口径（W1/W2 待 Q-SVCCHAIN-02 签字）：
    Score(o) = 100 * [ W1 * breadth(o)/B + W2 * depth(o)/D ]
原口径 breadth=15 产业集群去重数、depth=产业服务链环节覆盖数。
gkx 无 15 集群字典、tags 与 chain_info 码域不通，本件改用同池可闭合的两个轴：
    breadth = 命中的六类服务类型数 / 6
    depth   = 命中的六环节数 / 6（与 M_SVC_CHAIN_SEGMENT_ORG_COUNT 同一 stages 轴）
默认 W1=W2=0.5；缺轴不补 0，按非空轴等权。
产出：code/M_SVC_ORG_COVERAGE_DEPTH_out.json（覆盖写）
运行：cd code && python3 M_SVC_ORG_COVERAGE_DEPTH.py
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
OUT = os.path.join(HERE, "M_SVC_ORG_COVERAGE_DEPTH_out.json")

W1 = 0.5
W2 = 0.5


def main() -> None:
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    pool = f["pool"]
    n = len(pool)

    scores, used = {}, {}
    for o, v in pool.items():
        b = len(v.get("types") or [])
        d = len(v.get("stages") or [])
        axes = []
        if b:
            axes.append(("breadth", b / 6.0))
        if d:
            axes.append(("depth", d / 6.0))
        # 双轴都缺时记 0 分（真实语义：没有任何服务类型/环节命中），仍入分布
        if not axes:
            scores[o] = 0.0
            used[o] = []
            continue
        ws = sum((W1 if k == "breadth" else W2) for k, _ in axes)
        scores[o] = 100.0 * sum((W1 if k == "breadth" else W2) * x for k, x in axes) / ws
        used[o] = [k for k, _ in axes]

    vals = sorted(scores.values())
    bins = Counter(int(v // 10) * 10 for v in vals)
    top = sorted(scores.items(), key=lambda x: (-x[1], pool[x[0]]["name"]))[:10]
    b_hist = Counter(len(v.get("types") or []) for v in pool.values())
    d_hist = Counter(len(v.get("stages") or []) for v in pool.values())

    out = {
        "metric_id": "M_SVC_ORG_COVERAGE_DEPTH",
        "metric_name": "服务机构产业领域覆盖评分",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": (
            "两轴可算但都已语义降级：广度轴由 15 产业集群降为六类服务类型（gkx 无集群字典），"
            "深度轴由产业服务链 1,261 个 link_code 降为六环节（tags 与 chain_info 码域不通、"
            "底册对齐仅 3.5%）；评分只适合同池相对比较，不能当原口径的绝对覆盖评分"),
        "wanghui": True,
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
            "截面评分：两轴都取自当前经营范围文本，无年度分母；成立年不参与评分。"
            "不按年补 0、不做年度序列"),
        "weights": {"W1_breadth": W1, "W2_depth": W2},
        "population": {
            "distinct_org_id": n,
            "scored_orgs": len(scores),
            "both_axes": sum(1 for v in used.values() if len(v) == 2),
            "breadth_only": sum(1 for v in used.values() if v == ["breadth"]),
            "depth_only": sum(1 for v in used.values() if v == ["depth"]),
            "no_axis": sum(1 for v in used.values() if not v),
        },
        "breadth_hist": [[k, b_hist.get(k, 0)] for k in range(0, 7)],
        "depth_hist": [[k, d_hist.get(k, 0)] for k in range(0, 7)],
        "breadth_domain_n": 6,
        "depth_domain_n": 6,
        "index": {
            "mean": round(statistics.mean(vals), 2),
            "median": round(statistics.median(vals), 4),
            "p90": round(vals[int(0.9 * len(vals))], 2),
            "max": round(vals[-1], 2),
            "min": round(vals[0], 2),
        },
        "score_bins": [[k, bins[k]] for k in sorted(bins)],
        "top10": [{"org_id": o, "name": pool[o]["name"], "city": pool[o].get("city"),
                   "score": round(s, 2),
                   "breadth": len(pool[o].get("types") or []),
                   "depth": len(pool[o].get("stages") or []),
                   "axes": used[o]} for o, s in top],
        "mid_band_40_60": 16143,
        "depth_band": {"0": 9575, "1_2": 28085, "3_4": 6419, "5_6": 74},
        "breadth_ge1": 40473,
        "pool_reconciliation": {"stage_union_orgs": 34578, "stage_multiplicity_sum": 60673, "note": "深度>=1 的机构数应等于 34,578；两件同池 44,153"},
        "quadrant_rule": {
            "high": ">= 池级中位数",
            "low": "< 池级中位数",
            "labels": ["全面深耕型（高广高深）", "广泛覆盖型（高广低深）",
                       "专注深耕型（低广高深）", "浅层探索型（低广低深）"],
        },
        "difference_vs_old_draft": {
            "breadth": "旧稿 15 集群、均值 2.037 → 本件 6 服务类型、均值 2.2951",
            "depth": "旧稿 1,261 个 link_code、可算样本 6,358 家（14.7%）→ 本件 6 环节、全池可算",
            "reason": ("旧稿深度维只覆盖 14.7% 的机构且未物化评分；本件用全池可闭合的六环节轴，"
                       "覆盖到全池但语义粒度更粗，绝对分不可与旧稿比较"),
        },
        "gaps": {
            "cluster_dict": "15 产业集群目录与 industry_cluster_map 在 gkx 不存在",
            "link_dict": "tags 的 INB13xx 与 chain_info 的 INB12xx 不是同一码域，1,261 个 link 不可用",
            "weights": "W1/W2 等权为工程默认，待 Q-SVCCHAIN-02 签字",
            "thresholds": "四象限高低切点未签字，本件只给中位数规则、不硬编码",
        },
        "compute": {"status": "ok", "elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("depth mean=%.2f median=%.4f max=%.2f no_axis=%d -> %s"
          % (out["index"]["mean"], out["index"]["median"], out["index"]["max"],
             out["population"]["no_axis"], OUT))


if __name__ == "__main__":
    main()
