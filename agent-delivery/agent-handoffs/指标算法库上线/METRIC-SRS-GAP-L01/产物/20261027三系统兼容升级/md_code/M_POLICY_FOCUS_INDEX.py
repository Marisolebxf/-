#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_POLICY_FOCUS_INDEX 政策焦点指数 —— gkx 复现（2026-10-23）

口径（calc-logic/POLICY/M_POLICY_FOCUS_INDEX.md，权重待 QPOL-02）：
    四维 = 制定背景（依据词频/正文字数）/ 政策目标（目标词频/正文字数）
          / 适用范围（范围词频 + I(support_object 非空)）/ 措施执行（behavior+way 去重数）
    合成 = 各维截面 min-max → 缺维不进平均 → 等权 → ×100；全样本同值取 0.5。

唯一整维缺失：措施执行情况。policy_support 20,000 行全是 JSON null，
behavior / way 两个子键都读不出来，四维只有三维可算。词表全闭集、逐字照抄 calc-logic。

输入：code/_snapshots21/policy_text_20261023.json
      code/_snapshots21/policy_struct_20261023.json
输出：code/M_POLICY_FOCUS_INDEX_out.json
"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_POLICY_FOCUS_INDEX_out.json"

NULL = "__NULL__"
NULLS = ("__NULL__", "NULL", "")


def pct(vals, p):
    if not vals:
        return None
    s = sorted(vals)
    return round(s[min(len(s) - 1, int(len(s) * p))], 6)


def minmax(vals):
    """截面 min-max；全样本同值按 calc-logic 取 0.5（不是 0）。"""
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return [0.5] * len(vals)
    return [(v - lo) / (hi - lo) for v in vals]


def rank(v):
    """并列取平均秩，手算 Spearman 用（不引 scipy）。"""
    order = sorted(range(len(v)), key=lambda i: v[i])
    rk = [0.0] * len(v)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1
        for t in range(i, j + 1):
            rk[order[t]] = avg
        i = j + 1
    return rk


def main() -> int:
    text = json.load(open(SNAP / "policy_text_20261023.json", encoding="utf-8"))
    struct = json.load(open(SNAP / "policy_struct_20261023.json", encoding="utf-8"))
    rows = text["rows_detail"]

    scoreable = [r for r in rows if r["has_content"] and r["clen"] > 0]
    unscored = [r for r in rows if not (r["has_content"] and r["clen"] > 0)]

    bg_rate = [r["bg"] / r["clen"] for r in scoreable]
    goal_rate = [r["goal"] / r["clen"] for r in scoreable]
    scope_cnt = [float(r["scope"]) for r in scoreable]

    z_bg = minmax(bg_rate)
    z_goal = minmax(goal_rate)
    z_scope = minmax(scope_cnt)

    scores = [100.0 * (z_bg[i] + z_goal[i] + z_scope[i]) / 3.0
              for i in range(len(scoreable))]

    idx = sorted(range(len(scores)), key=lambda i: scores[i])
    k = max(1, len(idx) // 10)
    deciles = []
    for d in range(10):
        seg = idx[d * k:(d + 1) * k] if d < 9 else idx[9 * k:]
        lens = [scoreable[i]["clen"] for i in seg]
        deciles.append({
            "decile": d + 1,
            "n": len(seg),
            "score_min": round(min(scores[i] for i in seg), 4),
            "score_max": round(max(scores[i] for i in seg), 4),
            "content_len_median": int(statistics.median(lens)),
        })

    rs = rank(scores)
    rl = rank([float(r["clen"]) for r in scoreable])
    n = len(rs)
    mx, my = sum(rs) / n, sum(rl) / n
    cov = sum((rs[i] - mx) * (rl[i] - my) for i in range(n))
    vx = sum((rs[i] - mx) ** 2 for i in range(n)) ** 0.5
    vy = sum((rl[i] - my) ** 2 for i in range(n)) ** 0.5
    spearman = round(cov / (vx * vy), 4) if vx and vy else None

    # 敏感性：把三维修剪到 p99 再 min-max（极值单点决定刻度，见 deciles 与 raw_max）
    def winsor(vals, q=0.99):
        cap = sorted(vals)[min(len(vals) - 1, int(len(vals) * q))]
        return [min(v, cap) for v in vals]

    z_bg_w = minmax(winsor(bg_rate))
    z_goal_w = minmax(winsor(goal_rate))
    z_scope_w = minmax(winsor(scope_cnt))
    scores_w = [100.0 * (z_bg_w[i] + z_goal_w[i] + z_scope_w[i]) / 3.0
                for i in range(len(scoreable))]

    by_city = {}
    for i, r in enumerate(scoreable):
        c = r["city"]
        if c in NULLS:
            continue
        d = by_city.setdefault(c, {"n": 0, "s": [], "w": []})
        d["n"] += 1
        d["s"].append(scores[i])
        d["w"].append(scores_w[i])
    city_scores = [
        {"city": c, "n": d["n"], "mean_score": round(statistics.mean(d["s"]), 4),
         "median_score": round(statistics.median(d["s"]), 4),
         "mean_score_winsor": round(statistics.mean(d["w"]), 4)}
        for c, d in by_city.items() if d["n"] >= 100
    ]
    city_scores.sort(key=lambda x: -x["mean_score"])

    # 城市排序在两个口径下是否稳定
    rc = rank([c["mean_score"] for c in city_scores])
    rw = rank([c["mean_score_winsor"] for c in city_scores])
    m = len(rc)
    mcx, mcy = sum(rc) / m, sum(rw) / m
    cc = sum((rc[i] - mcx) * (rw[i] - mcy) for i in range(m))
    vcx = sum((rc[i] - mcx) ** 2 for i in range(m)) ** 0.5
    vcy = sum((rw[i] - mcy) ** 2 for i in range(m)) ** 0.5
    city_rank_stability = round(cc / (vcx * vcy), 4) if vcx and vcy else None

    order = sorted(range(len(scores)), key=lambda i: -scores[i])
    top = [{"id": scoreable[i]["id"], "score": round(scores[i], 4),
            "clen": scoreable[i]["clen"], "bg": scoreable[i]["bg"],
            "goal": scoreable[i]["goal"], "scope": scoreable[i]["scope"]}
           for i in order[:10]]
    bottom = [{"id": scoreable[i]["id"], "score": round(scores[i], 4),
               "clen": scoreable[i]["clen"], "bg": scoreable[i]["bg"],
               "goal": scoreable[i]["goal"], "scope": scoreable[i]["scope"]}
              for i in order[-10:]]

    out = {
        "metric_id": "M_POLICY_FOCUS_INDEX",
        "support_judgment": "部分支持",
        "publishable": True,
        "registered_metric_value": round(statistics.mean(scores), 4),
        "headline": {
            "policy_total": text["rows"],
            "scoreable_rows": len(scoreable),
            "unscored_rows": len(unscored),
            "dims_total": 4,
            "dims_computable": 3,
            "dims_missing": 1,
            "missing_dim": "措施执行情况（policy_support.support_behavior / support_way）",
            "score_min": round(min(scores), 4),
            "score_median": round(statistics.median(scores), 4),
            "score_mean": round(statistics.mean(scores), 4),
            "score_p90": pct(scores, 0.9),
            "score_max": round(max(scores), 4),
        },
        "dims": [
            {"dim": "制定背景（依据词频/正文字数）", "field": "content + abstract",
             "raw_min": round(min(bg_rate), 6),
             "raw_median": round(statistics.median(bg_rate), 6),
             "raw_max": round(max(bg_rate), 6),
             "docs_hit": sum(1 for r in scoreable if r["bg"] > 0),
             "weight": 0.333333, "computable": True},
            {"dim": "政策目标（目标词频/正文字数）", "field": "content",
             "raw_min": round(min(goal_rate), 6),
             "raw_median": round(statistics.median(goal_rate), 6),
             "raw_max": round(max(goal_rate), 6),
             "docs_hit": sum(1 for r in scoreable if r["goal"] > 0),
             "weight": 0.333333, "computable": True},
            {"dim": "适用范围（范围词频 + I(support_object)）",
             "field": "content + policy_support.support_object",
             "raw_min": min(scope_cnt), "raw_median": statistics.median(scope_cnt),
             "raw_max": max(scope_cnt),
             "docs_hit": sum(1 for r in scoreable if r["scope"] > 0),
             "weight": 0.333333, "computable": True,
             "note": "I(support_object 非空) 恒取 0（policy_support 全表 JSON null）"},
            {"dim": "措施执行情况（behavior+way 去重数）", "field": "policy_support",
             "raw_min": None, "raw_median": None, "raw_max": None,
             "docs_hit": 0, "weight": 0.0, "computable": False,
             "note": "policy_support 20,000 行 JSON_TYPE='NULL'，两子键不可读；缺维不进平均"},
        ],
        "distribution": {
            "quantiles": {"p10": pct(scores, 0.1), "p25": pct(scores, 0.25),
                          "p50": pct(scores, 0.5), "p75": pct(scores, 0.75),
                          "p90": pct(scores, 0.9)},
            "zero_scope_docs": sum(1 for r in scoreable if r["scope"] == 0),
            "spearman_score_vs_content_len": spearman,
            "deciles": deciles,
            "sensitivity_winsor_p99": {
                "mean": round(statistics.mean(scores_w), 4),
                "median": round(statistics.median(scores_w), 4),
                "p90": pct(scores_w, 0.9),
                "max": round(max(scores_w), 4),
                "city_rank_spearman_vs_main": city_rank_stability,
                "note": "三维各自先截到 p99 再 min-max；不替代主口径，只用来证明刻度被极值单点主导",
            },
            "scoreable_without_city": sum(1 for r in scoreable if r["city"] in NULLS),
            "cities_in_table": len(city_scores),
        },
        "city_scores": city_scores[:12],
        "samples": {"top10": top, "bottom10": bottom},
        "probes": {
            "policy_support_json_type_dist": struct["elements"]["support_json_type_dist"],
            "support_way_rows": struct["elements"]["support_way_rows"],
            "support_behavior_rows": struct["elements"]["support_behavior_rows"],
            "support_object_rows": struct["elements"]["support_object_rows"],
            "bg_total_hits": text["agg"]["bg_total_hits"],
            "goal_total_hits": text["agg"]["goal_total_hits"],
            "scope_total_hits": text["agg"]["scope_total_hits"],
            "content_db_rows": text["agg"]["content_db_rows"],
            "content_local_rows": text["agg"]["content_local_rows"],
            "lexicons": {k: text["lexicons"][k] for k in
                         ("focus_bg", "focus_goal", "focus_scope")},
        },
        "custom_thresholds": {
            "weights": "等权 1/3（QPOL-02 未签；缺维后按剩余维重新归一）",
            "minmax": "截面 min-max；全样本同值取 0.5",
            "scope_dim": "范围词频不除以正文长度（calc-logic 原文未给分母，不擅自引入）",
        },
        "reused_from": "code/_snapshots21/policy_text_20261023.json",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面件：不按年度切分，政策池取 20,000 条存量全表（publish_year 跨 1981—2024）。"
                            "焦点指数度量文本写法，与发布年份无关，故不设基期；"
                            "也不得把「某年没有新政策」读成焦点为 0。"),
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("support_judgment", "headline")},
                     ensure_ascii=False, indent=1))
    print("spearman(score,len)=", spearman)
    print("city top3", json.dumps(city_scores[:3], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
