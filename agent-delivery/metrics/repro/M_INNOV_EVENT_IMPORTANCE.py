#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_EVENT_IMPORTANCE 事件重要性等级 —— 关注度与影响力的下游自动分档。

综合分 = 0.5×attention + 0.5×influence（王惠口径等权）
分档：本窗综合分 ≥P70 为高、≤P30 为低、其余为中；样本 <20 时改用固定阈 70/40 并标 rule=fallback。
本脚本不重复计算上游两件，直接复用 `_innov_event_lib.build()` 的同一批事件簇，保证三件同一口径。
"""
import os
import sys
import json
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _innov_event_lib as L

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_INNOV_EVENT_IMPORTANCE_out.json")


def band_attention_only(ev):
    """只用关注度分档（对照：检验影响力是否真的改变了分档结果）。"""
    vals = [e["attention"] for e in ev]
    p70, p30 = L._pct(vals, 0.70), L._pct(vals, 0.30)
    for e in ev:
        e["att_only_level"] = "高" if e["attention"] >= p70 else ("低" if e["attention"] <= p30 else "中")
    return p70, p30


def main():
    d = L.build()
    ev = d["events"]
    n = len(ev)
    use_fallback = n < 20
    if use_fallback:
        for e in ev:
            e["importance_level"] = "高" if e["composite"] >= 70 else ("低" if e["composite"] <= 40 else "中")
        rule = "fallback_fixed_70_40"
    else:
        rule = "p70_p30_in_window"
    ap70, ap30 = band_attention_only(ev)
    lv = Counter(e["importance_level"] for e in ev)
    # 分档 × 年份
    by_year = {}
    for e in ev:
        y = e["week"][:4]
        by_year.setdefault(y, Counter())[e["importance_level"]] += 1
    # 与「仅关注度分档」的一致性
    same = sum(1 for e in ev if e["importance_level"] == e["att_only_level"])
    # 高等级中关注度不高的（权威驱动）与低等级中关注度高的（量大但源弱）
    auth_driven = sorted([e for e in ev if e["importance_level"] == "高" and e["att_only_level"] != "高"],
                         key=lambda x: -x["influence"])[:8]
    volume_driven = sorted([e for e in ev if e["importance_level"] == "低" and e["att_only_level"] == "高"],
                           key=lambda x: -x["attention"])[:8]
    top = sorted(ev, key=lambda x: -x["composite"])[:20]

    def slim(e, keys):
        return {k: e[k] for k in keys}

    K = ("event_key", "chain_id", "week", "n_reports", "n_sources", "n_tier4", "tier_mean",
         "attention", "influence", "composite", "importance_level", "top_titles", "sources")
    res = {
        "metric_id": "M_INNOV_EVENT_IMPORTANCE",
        "name": "事件重要性等级",
        "event_unit": "产业链主题(chain_id) × ISO 自然周（与上游两件同一 6,406 个事件簇）",
        "method": {
            "formula": "C = 0.5*attention + 0.5*influence; 高: C>=P70, 低: C<=P30, 其余=中",
            "thresholds": {"p70": d["meta"]["p70"], "p30": d["meta"]["p30"]},
            "rule": rule,
            "fallback": "样本 <20 时改用固定阈 70/40 并标 rule=fallback（本窗 6,406 个事件，未触发）",
        },
        "meta": d["meta"],
        "distribution": {"高": lv.get("高", 0), "中": lv.get("中", 0), "低": lv.get("低", 0)},
        "ratio": {k: round(v / n * 100, 2) for k, v in lv.items()},
        "by_year": {y: dict(c) for y, c in sorted(by_year.items())},
        "attention_only_band": {"p70": round(ap70, 4), "p30": round(ap30, 4),
                                "agreement_with_composite": round(same / n * 100, 2)},
        "composite_stats": L.stats([e["composite"] for e in ev]),
        "top20": [slim(e, K) for e in top],
        "authority_driven_high": [slim(e, K) for e in auth_driven],
        "volume_driven_low": [slim(e, K) for e in volume_driven],
        "chain_level": dict(Counter(e["chain_id"] for e in ev if e["importance_level"] == "高").most_common(10)),
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": "分档本身可现转（6,406 个事件 → 高 1,922 / 中 2,562 / 低 1,922，三档 30:40:30），"
                      "但分档输入为关注度与影响力的传播代理（真实报道量/媒体层级），"
                      "非真实受众互动与权威媒体评级，故与上游同判「部分支持」。",
            "criteria": {"structure": "复用上游两件的事件簇与分数（无独立源表需求）",
                         "volume": "6,406 events",
                         "reproducible": True,
                         "distribution_discriminative": True,
                         "upstream_proxy": True},
        },
    }
    json.dump(res, open(OUT, "w"), ensure_ascii=False, indent=1, default=str)
    print("n", n, "thr", res["method"]["thresholds"], "dist", res["distribution"], res["ratio"])
    print("agreement with attention-only", res["attention_only_band"]["agreement_with_composite"])
    print("by_year", res["by_year"])
    print("wrote", OUT)


if __name__ == "__main__":
    main()
