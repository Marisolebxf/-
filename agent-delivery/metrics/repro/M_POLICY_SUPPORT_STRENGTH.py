#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_POLICY_SUPPORT_STRENGTH 支持力度 —— gkx 复现（2026-10-23）

注册表口径（cfg_metric-POLICY-seed.yaml，QPOL-02 未签）：
    支持力度 = 扶持力度档位*w1 + 政策层级权重*w2 + 政策数量*w3
    场景：区域政策创新成果综合评价（三维框架）之「支持力度」维
无同 ID 正本：`gkx-orchestration/agent-delivery/metrics/calc-logic/POLICY/` 下没有
M_POLICY_SUPPORT_STRENGTH.md（同目录 19 份正本里没有这一件），故本件口径只能来自
注册表 definition/formula 两句 + 本报告自拟的降级规则，全部写在 §1.6。

本件实测到的硬约束（决定了档位维必须置 null，不能置 0）：
  1. dwd_policy_base 共 33 列，没有任何金额/资金/补贴列（information_schema 全库扫描：
     gkx 下 123 个金额类列全部落在 dwd_bid_* 招标表，政策表一列没有）。
  2. policy_support 20,000 行 JSON_TYPE='NULL'，连「支持方式」都读不出来，更没有档位。
  3. 因此「扶持力度档位」是**无源维度**，按派单书约束置 null，不置 0、不自造资金强度。

可算的两维是「政策层级」（rank→level 四档）与「政策数量」。两维都按城市截面归一，
缺维后权重按剩余维重新归一（0.5 / 0.5），并额外给一版「仅层级」与「仅数量」的单维排序，
用来检验这个合成分到底有没有超出「政策条数排名」的信息量。

输入：code/_snapshots21/policy_text_20261023.json（rows_detail 带 city/level）
      code/_snapshots21/policy_dims_20261023.json（rank/level 分布对账）
输出：code/M_POLICY_SUPPORT_STRENGTH_out.json
"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_POLICY_SUPPORT_STRENGTH_out.json"

NULLS = ("__NULL__", "NULL", "")
LEVEL_W = {4: 1.0, 3: 0.75, 2: 0.5, 1: 0.25, 0: 0.0}
LEVEL_ZH = {4: "国家级", 3: "省级", 2: "市级", 1: "区级/园区级", 0: "未标注"}


def rank(v):
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


def spearman(a, b):
    ra, rb = rank(a), rank(b)
    n = len(ra)
    ma, mb = sum(ra) / n, sum(rb) / n
    cov = sum((ra[i] - ma) * (rb[i] - mb) for i in range(n))
    va = sum((ra[i] - ma) ** 2 for i in range(n)) ** 0.5
    vb = sum((rb[i] - mb) ** 2 for i in range(n)) ** 0.5
    return round(cov / (va * vb), 4) if va and vb else None


def minmax(vals):
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return [0.5] * len(vals)
    return [(v - lo) / (hi - lo) for v in vals]


def main() -> int:
    text = json.load(open(SNAP / "policy_text_20261023.json", encoding="utf-8"))
    dims = json.load(open(SNAP / "policy_dims_20261023.json", encoding="utf-8"))
    rows = text["rows_detail"]

    city = {}
    for r in rows:
        c = r["city"]
        if c in NULLS:
            continue
        d = city.setdefault(c, {"n": 0, "lvl_sum": 0.0, "lvl_cnt": {}, "prov": r["province"]})
        d["n"] += 1
        lv = r["level"] if isinstance(r["level"], int) else 0
        d["lvl_sum"] += LEVEL_W.get(lv, 0.0)
        d["lvl_cnt"][lv] = d["lvl_cnt"].get(lv, 0) + 1

    names = sorted(city, key=lambda c: -city[c]["n"])
    n_min = 30
    keep = [c for c in names if city[c]["n"] >= n_min]

    cnt = [city[c]["n"] for c in keep]
    lvl = [city[c]["lvl_sum"] / city[c]["n"] for c in keep]
    z_cnt = minmax(cnt)
    z_lvl = minmax(lvl)
    score = [100.0 * (0.5 * z_cnt[i] + 0.5 * z_lvl[i]) for i in range(len(keep))]

    table = []
    for i, c in enumerate(keep):
        d = city[c]
        table.append({
            "city": c,
            "policies": d["n"],
            "level_mean": round(lvl[i], 4),
            "level_mix": {LEVEL_ZH[k]: v for k, v in sorted(d["lvl_cnt"].items())},
            "count_norm": round(z_cnt[i], 4),
            "level_norm": round(z_lvl[i], 4),
            "strength_score": round(score[i], 4),
            "tier_dim": None,
        })
    table.sort(key=lambda x: -x["strength_score"])

    # 合成分与「纯政策条数」的秩相关：如果接近 1，说明层级维没有提供额外信息
    sp_cnt = spearman([t["strength_score"] for t in table], [t["policies"] for t in table])
    sp_lvl = spearman([t["strength_score"] for t in table], [t["level_mean"] for t in table])

    # 深圳市单独核对（与已交付政策件对齐）
    sz = next((t for t in table if t["city"] == "深圳市"), None)

    # 含国家级口径（国家级政策对每个城市都适用，会把 2,174 条加到每个城市）
    nat = dims["national"]["level4_rows"]
    cnt_nat = [c + nat if c != nat else c for c in cnt]  # 市级行已不含国家级（city 为空）
    z_cnt_nat = minmax(cnt_nat)
    score_nat = [100.0 * (0.5 * z_cnt_nat[i] + 0.5 * z_lvl[i]) for i in range(len(keep))]
    sp_nat = spearman(score_nat, cnt_nat)

    out = {
        "metric_id": "M_POLICY_SUPPORT_STRENGTH",
        "support_judgment": "部分支持",
        "publishable": True,
        "registered_metric_value": round(statistics.mean(score), 4),
        "headline": {
            "policy_total": text["rows"],
            "cities_total": len(names),
            "cities_in_table": len(table),
            "min_policies_per_city": n_min,
            "dims_total": 3,
            "dims_computable": 2,
            "dims_missing": 1,
            "missing_dim": "扶持力度档位（policy_support 全 null；政策表 0 个金额列）",
            "score_min": round(min(score), 4),
            "score_median": round(statistics.median(score), 4),
            "score_max": round(max(score), 4),
            "sz_score": sz["strength_score"] if sz else None,
            "sz_policies": sz["policies"] if sz else None,
        },
        "cities": table,
        "dims": [
            {"dim": "扶持力度档位", "field": "policy_support / 金额列", "computable": False,
             "value": None, "weight_nominal": 0.333333, "weight_used": 0.0,
             "evidence": "policy_support JSON null 20,000/20,000；33 列中金额类列 0 个"},
            {"dim": "政策层级权重", "field": "rank→level", "computable": True,
             "value": "level∈{4,3,2,1,0} → 权重 {1.0,0.75,0.5,0.25,0}，按城市取均值",
             "weight_nominal": 0.333333, "weight_used": 0.5},
            {"dim": "政策数量", "field": "city 计数", "computable": True,
             "value": "该市政策条数，截面 min-max",
             "weight_nominal": 0.333333, "weight_used": 0.5},
        ],
        "diagnostics": {
            "spearman_score_vs_policy_count": sp_cnt,
            "spearman_score_vs_level_mean": sp_lvl,
            "level_mean_min": round(min(lvl), 4),
            "level_mean_max": round(max(lvl), 4),
            "level_mean_median": round(statistics.median(lvl), 4),
            "national_policy_rows": nat,
            "spearman_with_national_included_vs_count": sp_nat,
            "note": ("合成分与政策条数的秩相关若接近 1，说明本件实际交付的是「政策条数排名」的"
                     "单调变换，层级维只做微调；这正是「档位维缺失后不该把结果叫支持力度」的量化依据。"),
        },
        "probes": {
            "rank_dist": dims["rank_dist"],
            "level_dist": dims["level_dist"],
            "city_null_rows": dims["city_dist"]["__NULL__"],
            "city_rows": sum(dims["city_dist"].values()) - dims["city_dist"]["__NULL__"],
            "amount_columns_in_policy_table": 0,
            "amount_columns_in_gkx_total": 123,
            "amount_columns_scope": "全部落在 dwd_bid_* 招标表；政策两表（dwd_policy_base / dwd_global_policy_base）无金额列",
        },
        "custom_thresholds": {
            "weights": "档位维缺失后按剩余两维等权 0.5/0.5（QPOL-02 未签，本件不称官方权重）",
            "min_city_size": n_min,
            "level_weight_map": {str(k): v for k, v in LEVEL_W.items()},
            "tier_dim_rule": "无源维度置 null 不置 0；不发布任何金额口径的「资金强度」",
        },
        "reused_from": "code/_snapshots21/policy_text_20261023.json",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面件：政策池取 20,000 条存量全表，不按年度切窗。"
                            "支持力度度量的是存量供给结构，与单一年份无关；"
                            "若改按年度切分，2023/2024 的零行会被误读成「支持力度归零」，"
                            "而那是采集断档（publish_year 分布见 policy_dims_20261023.json）。"),
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("support_judgment", "headline")}, ensure_ascii=False, indent=1))
    print(json.dumps(out["diagnostics"], ensure_ascii=False, indent=1))
    print(json.dumps(table[:8], ensure_ascii=False, indent=0))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
