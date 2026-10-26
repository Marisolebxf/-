#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_DEEP_129_1 重点布局产业推荐模型

三维合成（复用同目录三件已交付产物，不重扫库）：
  advantage = M_CHAIN_SZ_ADVANTAGE_SCORE_out.json 的 sz_score_available_dims
  opportunity = M_CHAIN_DEEP_128_1_out.json 的 opportunity_index
  policy = M_CHAIN_POLICY_MATCH_SCORE_out.json 的 match_score
  recommend_index = 1/3 * (advantage + opportunity + policy)
  level: >=70 优先布局；55—70 重点培育；<55 观察

产出：code/M_CHAIN_DEEP_129_1_out.json
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "M_CHAIN_DEEP_129_1_out.json"

ADV = json.loads((HERE / "M_CHAIN_SZ_ADVANTAGE_SCORE_out.json").read_text(encoding="utf-8"))
OPP = json.loads((HERE / "M_CHAIN_DEEP_128_1_out.json").read_text(encoding="utf-8"))
POL = json.loads((HERE / "M_CHAIN_POLICY_MATCH_SCORE_out.json").read_text(encoding="utf-8"))

W = {"advantage": 1 / 3, "opportunity": 1 / 3, "policy": 1 / 3}
TH = {"priority": 70.0, "cultivate": 55.0}

adv = {r["industry_code"]: r for r in ADV["per_chain"]}
opp = {r["chain"]: r for r in OPP["compute"]["chains"]}
pol = {r["chain"]: r for r in POL["chain_rows"]}


def level(x: float) -> str:
    if x >= TH["priority"]:
        return "优先布局"
    if x >= TH["cultivate"]:
        return "重点培育"
    return "观察"


def index(a: float, o: float, p: float, w: dict) -> float:
    return round(w["advantage"] * a + w["opportunity"] * o + w["policy"] * p, 2)


rows = []
for code in sorted(adv):
    a = float(adv[code]["sz_score_available_dims"])
    o = float(opp[code]["opportunity_index"])
    p = float(pol[code]["match_score"])
    rows.append({
        "chain_code": code,
        "chain_name": adv[code]["industry_name"],
        "advantage": round(a, 2),
        "opportunity": round(o, 2),
        "policy": round(p, 2),
        "policy_hits": pol[code]["policy_hits"],
        "shenzhen_hits": pol[code]["shenzhen_hits"],
        "recommend_index": index(a, o, p, W),
        "level": level(index(a, o, p, W)),
    })

rows.sort(key=lambda r: (-r["recommend_index"], r["chain_code"]))
for i, r in enumerate(rows, 1):
    r["rank"] = i
rank_map = {r["chain_code"]: r["rank"] for r in rows}

# 敏感性
def ranks_with(w: dict) -> dict:
    tmp = sorted(
        rows,
        key=lambda r: (-(w["advantage"] * r["advantage"] + w["opportunity"] * r["opportunity"] + w["policy"] * r["policy"]), r["chain_code"]),
    )
    return {r["chain_code"]: i for i, r in enumerate(tmp, 1)}


sens_defs = {
    "equal": W,
    "advantage_led": {"advantage": 0.5, "opportunity": 0.25, "policy": 0.25},
    "opportunity_led": {"advantage": 0.25, "opportunity": 0.5, "policy": 0.25},
    "policy_led": {"advantage": 0.25, "opportunity": 0.25, "policy": 0.5},
    "policy_dropped": {"advantage": 0.5, "opportunity": 0.5, "policy": 0.0},
}
sens = {}
for name, w in sens_defs.items():
    rk = ranks_with(w)
    top = min(rk, key=rk.get)
    sens[name] = {
        "weights": {k: round(v, 3) for k, v in w.items()},
        "rank": {r["chain_name"]: rk[r["chain_code"]] for r in rows},
        "top": next(r["chain_name"] for r in rows if r["chain_code"] == top),
        "index": {r["chain_name"]: index(r["advantage"], r["opportunity"], r["policy"], w) for r in rows},
    }

# 维度一致性（Spearman，平均秩处理并列）
def spearman(xs: list[float], ys: list[float]) -> float:
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    rx, ry = ranks(xs), ranks(ys)
    n = len(xs)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return round(num / den, 3) if den else 0.0


A = [r["advantage"] for r in rows]
O = [r["opportunity"] for r in rows]
P = [r["policy"] for r in rows]
corr = {
    "advantage_vs_opportunity": spearman(A, O),
    "advantage_vs_policy": spearman(A, P),
    "opportunity_vs_policy": spearman(O, P),
}

# 优势列替换敏感性：available_dims → wanghui4_filled
adv4_rows = []
for r in rows:
    a4 = float(adv[r["chain_code"]]["sz_score_wanghui4_filled"])
    idx4 = index(a4, r["opportunity"], r["policy"], W)
    adv4_rows.append({"chain_name": r["chain_name"], "advantage_wanghui4": round(a4, 2), "index": idx4})
adv4_rows.sort(key=lambda x: (-x["index"], x["chain_name"]))
for i, r in enumerate(adv4_rows, 1):
    r["rank"] = i

tier_counts = {"优先布局": 0, "重点培育": 0, "观察": 0}
for r in rows:
    tier_counts[r["level"]] += 1

payload = {
    "metric_id": "M_CHAIN_DEEP_129_1",
    "metric_name": "重点布局产业推荐模型",
    "formula_owner": "AI 补漏调研 2026-08-21（算法库深链模型）；本件 2026-10-22 复算",
    "support_judgment": "部分支持",
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "截面合成指标，无年度基期；三个输入件各自的口径与基期见其产物文件",
    "value": rows[0]["recommend_index"],
    "unit": "分",
    "scope": "12 条产业链；每条链一个推荐指数与等级",
    "definition": (
        "推荐指数 = 1/3 × 深圳产业优势分 + 1/3 × 产业机遇分 + 1/3 × 政策匹配分；"
        ">=70 优先布局，55—70 重点培育，<55 观察。权重与阈值均为本件自定义，非甲方确认参数"
    ),
    "headline": {
        "top_chain": rows[0]["chain_name"],
        "top_index": rows[0]["recommend_index"],
        "tier_counts": tier_counts,
        "chain_total": len(rows),
        "priority_threshold": TH["priority"],
        "cultivate_threshold": TH["cultivate"],
        "weights": {k: round(v, 3) for k, v in W.items()},
        "max_advantage": max(rows, key=lambda r: r["advantage"])["chain_name"],
        "max_opportunity": max(rows, key=lambda r: r["opportunity"])["chain_name"],
        "max_policy": max(rows, key=lambda r: r["policy"])["chain_name"],
    },
    "per_chain": rows,
    "dimension_correlation": corr,
    "advantage_column_variant": {
        "note": "把优势列从 sz_score_available_dims 换成 sz_score_wanghui4_filled 后的排名；用于证明结论对优势口径也敏感",
        "rows": adv4_rows,
    },
    "sensitivity": sens,
    "input_provenance": {
        "advantage": {
            "file": "code/M_CHAIN_SZ_ADVANTAGE_SCORE_out.json",
            "field": "per_chain[].sz_score_available_dims",
            "available_dim_min": min(r["advantage"] for r in rows),
            "available_dim_max": max(r["advantage"] for r in rows),
            "note": "该件按可获取维度占比分与王惠四维分双列，本件取 available_dims 列以保 12 链可比",
        },
        "opportunity": {
            "file": "code/M_CHAIN_DEEP_128_1_out.json",
            "field": "compute.chains[].opportunity_index",
            "note": "机遇分由优势分、趋势分、缺口分合成，与本件优势维存在同源重叠，故两维并非独立",
        },
        "policy": {
            "file": "code/M_CHAIN_POLICY_MATCH_SCORE_out.json",
            "field": "chain_rows[].match_score",
            "note": "政策分是标题关键词命中的归一值；具身智能 0 命中是词表未覆盖，不是无政策",
        },
    },
    "caveats": [
        "权重/阈值无甲方参数：calc-logic 明写需专家推荐策略参数表，该表未建",
        "优势维与机遇维同源（机遇件以优势分为输入之一），三维并不正交，简单加权会重复计权",
        "政策维对新兴链不公平：具身智能标题 0 命中直接把它从优势第 7 拉到综合第 12",
        "12 条链样本太小，排名对阈值极敏感；55—70 区间内有 7 条链，1—2 分变动即换档",
    ],
    "sources": [
        "code/M_CHAIN_SZ_ADVANTAGE_SCORE_out.json",
        "code/M_CHAIN_DEEP_128_1_out.json",
        "code/M_CHAIN_POLICY_MATCH_SCORE_out.json",
    ],
}

OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print("wrote", OUT)
print("top", rows[0]["chain_name"], rows[0]["recommend_index"], tier_counts)
print("corr", corr)
print("policy_dropped top", sens["policy_dropped"]["top"])
for r in rows:
    print(r["rank"], r["chain_name"], r["advantage"], r["opportunity"], r["policy"], r["recommend_index"], r["level"], sens["policy_dropped"]["rank"][r["chain_name"]])
