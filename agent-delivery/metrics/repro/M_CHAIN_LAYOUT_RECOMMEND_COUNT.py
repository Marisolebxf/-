#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_LAYOUT_RECOMMEND_COUNT 重点布局推荐数（W14-C2，零 DB）。

calc-logic v0.2.0（方案A）把本指标定义为「发布快照里单链布局推荐条数」：
`industry_chain_metric_fact` 按 `object_type='chain'` + `metric_id` 直读，
模型侧由 `industry_chain_model_result_detail.priority_level` 归档档位。
两库都没有这张结果表（gkx 280 表 layout/recommend 关键词 0 命中；live 侧
`industry_chain_metric_fact` 0 行），所以本件把「推荐」写成一条可复算的布尔规则：

  入集条件（三条同时满足）：
    R1 规模：全国该叶企业数 >= 10
    R2 关键：全国该叶企业数 >= 该链正样本叶的中位数
    R3 缺口：深圳该叶挂链为 0，或深圳占全国比 < 深圳基准（7.952%）
  推荐条数 = 满足 R1∧R2∧R3 的叶级环节数（按链汇总）

  档位（同一规则内的强弱分层）：
    A 空白强需求：深圳 0 家 且 全国 >= 50
    B 空白中需求：深圳 0 家 且 10 <= 全国 < 50
    C 单点不足：深圳 > 0 且 深圳占比 < 基准 且 全国 >= 10

阈值 10 / 50 是本件自定义的可复算门槛，另给 5 / 20 两档敏感性。
不产出「推荐分数」——原模型的 priority_level 与权重没有真源。

纯快照复算：
  code/_snapshots21/chain_tree_20261021.json
  code/_snapshots21/chain_stage_leaf_20261021.json
  code/_snapshots21/chain_firm_index_20261023.json
  code/_snapshots21/chain21_layer_20261022.json
  code/_snapshots21/chain_live_result_probe_20261023.json
"""
from __future__ import annotations

import json
import os
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
SCALE_MIN = 10
BLANK_STRONG = 50


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as fh:
        return json.load(fh)


def main() -> None:
    tree = load("chain_tree_20261021.json")
    stage = load("chain_stage_leaf_20261021.json")
    idx = load("chain_firm_index_20261023.json")
    layer = load("chain21_layer_20261022.json")
    probe = load("chain_live_result_probe_20261023.json")

    roots = sorted(n["industry_code"] for n in tree if len(n["industry_code"]) == 7)
    codes = {n["industry_code"] for n in tree}
    has_child = {c[:-2] for c in codes if len(c) > 7 and c[:-2] in codes}
    leaves = sorted(c for c in codes if c not in has_child and c not in roots)
    names = {n["industry_code"]: n["industry_name"] for n in tree}
    chain_name = idx["chain_name"]
    chain_firms = idx["chain_firms"]

    sz_total = sum(v for k, v in layer["chain_city"].items() if k.endswith("|深圳市"))
    nat_total = sum(chain_firms.values())
    benchmark = 100.0 * sz_total / nat_total

    recommended, rows = [], []
    for ch in roots:
        ls = [c for c in leaves if c[:7] == ch]
        nat = stage["leaf_firm_counts"].get(ch, {})
        szm = stage["cell_leaf_firm_counts"].get(ch + "|深圳市", {})
        pos = [nat[c] for c in ls if nat.get(c, 0) > 0]
        median = statistics.median(pos) if pos else 0
        key = [c for c in ls if nat.get(c, 0) > 0 and nat[c] >= median]

        cond_scale, cond_key, cond_gap, rec = 0, 0, 0, 0
        tier_a = tier_b = tier_c = 0
        blank_all = sum(1 for c in ls if szm.get(c, 0) == 0)
        for c in ls:
            n = nat.get(c, 0)
            s = szm.get(c, 0)
            share = 100.0 * s / n if n else 0.0
            r1 = n >= SCALE_MIN
            r2 = c in key
            r3 = (s == 0) or (share < benchmark)
            cond_scale += 1 if r1 else 0
            cond_key += 1 if r2 else 0
            cond_gap += 1 if r3 else 0
            if not (r1 and r2 and r3):
                continue
            rec += 1
            if s == 0 and n >= BLANK_STRONG:
                tier = "A"
                tier_a += 1
            elif s == 0:
                tier = "B"
                tier_b += 1
            else:
                tier = "C"
                tier_c += 1
            recommended.append({
                "chain_code": ch,
                "chain_name": chain_name[ch],
                "node_code": c,
                "node_name": names.get(c, ""),
                "national_firms": n,
                "sz_firms": s,
                "sz_share_pct": round(share, 3),
                "is_key_leaf": r2,
                "tier": tier,
            })

        rows.append({
            "chain_code": ch,
            "chain_name": chain_name[ch],
            "leaves": len(ls),
            "key_leaves": len(key),
            "median_threshold": median,
            "blank_all": blank_all,
            "national_sum": sum(nat.get(c, 0) for c in ls),
            "sz_sum": sum(szm.get(c, 0) for c in ls),
            "cond_scale": cond_scale,
            "cond_key": cond_key,
            "cond_gap": cond_gap,
            "recommend_count": rec,
            "tier_a": tier_a,
            "tier_b": tier_b,
            "tier_c": tier_c,
            "recommend_share_pct": round(100.0 * rec / len(ls), 2) if ls else 0.0,
            "chain_firms": chain_firms[ch],
            "sz_memberships": layer["chain_city"].get(ch + "|深圳市", 0),
        })

    total = len(recommended)
    ta = sum(r["tier_a"] for r in rows)
    tb = sum(r["tier_b"] for r in rows)
    tc = sum(r["tier_c"] for r in rows)

    # 敏感性：只改 R1 的规模门槛
    sens = {}
    for th in (5, SCALE_MIN, 20, 50):
        cnt = 0
        for ch in roots:
            ls = [c for c in leaves if c[:7] == ch]
            nat = stage["leaf_firm_counts"].get(ch, {})
            szm = stage["cell_leaf_firm_counts"].get(ch + "|深圳市", {})
            pos = [nat[c] for c in ls if nat.get(c, 0) > 0]
            med = statistics.median(pos) if pos else 0
            for c in ls:
                n = nat.get(c, 0)
                s = szm.get(c, 0)
                share = 100.0 * s / n if n else 0.0
                if n >= th and n > 0 and n >= med and ((s == 0) or (share < benchmark)):
                    cnt += 1
        sens[str(th)] = cnt

    out = {
        "metric_id": "M_CHAIN_LAYOUT_RECOMMEND_COUNT",
        "metric_name": "产业链重点布局推荐数",
        "support_judgment": "部分支持",
        "verdict_kind": "positive_evidence",
        "judgment_reason": (
            "calc-logic v0.2.0（方案A）是读发布快照：industry_chain_metric_fact 按单链直读推荐条数，"
            "模型侧由 industry_chain_model_result_detail.priority_level 定档。"
            "gkx 侧无这两张表（280 表里 layout/recommend 关键词零命中），live 侧 metric_fact 0 行，"
            "推荐模型的权重、档位阈值、评分口径均无真源。本件用链树 + 1,714,457 家链属企业 + 深圳挂链"
            "重建「全国有规模、属关键叶、深圳相对缺位」的环节清单并计数，规则可复算、可逐环节下钻；"
            "但它不是原模型的推荐结果，只能算结构侧布局建议，故判部分支持。"
        ),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "本件是截面指标：链树、叶级企业数、深圳挂链次数均为当日快照，口径内无年度序列，"
            "不涉及基期分母，故 used/missing 为空。"
        ),
        "sources": [
            "code/_snapshots21/chain_tree_20261021.json",
            "code/_snapshots21/chain_stage_leaf_20261021.json",
            "code/_snapshots21/chain_firm_index_20261023.json",
            "code/_snapshots21/chain21_layer_20261022.json",
            "code/_snapshots21/chain_live_result_probe_20261023.json",
        ],
        "rule": {
            "universe": "954 个叶级环节（1,273 节点 − 12 链根 − 307 内部节点）",
            "R1_scale": f"全国该叶企业数 >= {SCALE_MIN}",
            "R2_key": "全国该叶企业数 >= 该链正样本叶企业数的中位数",
            "R3_gap": f"深圳该叶 0 家，或深圳占全国比 < 深圳基准 {round(benchmark, 3)}%",
            "count": "满足 R1∧R2∧R3 的叶级环节数，按链汇总",
            "tier_A": f"深圳 0 家 且 全国 >= {BLANK_STRONG}",
            "tier_B": "深圳 0 家 且 10 <= 全国 < 50",
            "tier_C": "深圳 > 0 且 深圳占比 < 基准 且 全国 >= 10",
            "not_used": "原模型 priority_level / 推荐权重 / 评分阈值均不可得，本件不做推荐分数",
        },
        "params": {
            "benchmark_sz_share_pct": round(benchmark, 3),
            "scale_min": SCALE_MIN,
            "blank_strong": BLANK_STRONG,
            "sensitivity_scale_min": sens,
        },
        "population": {
            "chains": len(roots),
            "leaf_total": len(leaves),
            "chain_firms_clean": nat_total,
            "sz_memberships_4403": sz_total,
            "leaf_with_national_firms": sum(1 for ch in roots for c in leaves
                                            if c[:7] == ch and stage["leaf_firm_counts"].get(ch, {}).get(c, 0) > 0),
        },
        "headline": {
            "recommend_count": total,
            "tier_a": ta,
            "tier_b": tb,
            "tier_c": tc,
            "chain_avg": round(total / len(roots), 1),
            "chain_max": max(r["recommend_count"] for r in rows),
            "chain_max_name": max(rows, key=lambda r: r["recommend_count"])["chain_name"],
            "chain_min": min(r["recommend_count"] for r in rows),
            "chain_min_name": min(rows, key=lambda r: r["recommend_count"])["chain_name"],
            "chains_with_zero": sum(1 for r in rows if r["recommend_count"] == 0),
            "recommend_share_pct": round(100.0 * total / len(leaves), 2),
        },
        "by_chain": rows,
        "recommended": sorted(recommended, key=lambda x: (-x["national_firms"], x["node_code"])),
        "live_probe": {k: probe[k] for k in (
            "gkx_has_result_face", "gkx_chain_related_tables", "live_table_rows",
            "live_usable", "live_unusable_reason", "verdict")},
        "negative_probe": {
            "gkx_tables_total": 280,
            "pattern_hits": {"layout": 0, "recommend": 0, "priority": 0, "score": 0,
                             "chain_stage": 0, "node_scoring": 0},
            "only_chain_tables": ["dwd_industry_chain_info", "dwd_industry_chain_news_info"],
            "note": "无 chain_layout_recommend / chain_node_scoring / chain_stage / industry_chain_entity_rel 任何一张",
        },
        "gaps": [
            "chain_layout_recommend / chain_node_scoring / chain_stage / industry_chain_entity_rel 两库均无",
            "industry_chain_metric_fact 在 live 侧 0 行、gkx 侧 0 表，读表口径无结果面",
            "推荐模型 priority_level、权重、阈值无真源，本件档位 A/B/C 仅为规模—缺口分层",
            "链树 level 列全为 0、node_company_count 全为 0，不能做层级加权或企业规模加权",
            "深圳判定按登记地 credit_code[2:6]='4403'，实际经营地不可得",
        ],
        "checks": {
            "sum_recommend": sum(r["recommend_count"] for r in rows),
            "tier_sum": ta + tb + tc,
            "tier_matches_total": ta + tb + tc == total,
            "sum_leaves": sum(r["leaves"] for r in rows),
            "leaves_total": len(leaves),
            "sum_tier_a": sum(r["tier_a"] for r in rows),
            "sum_tier_b": sum(r["tier_b"] for r in rows),
            "sum_tier_c": sum(r["tier_c"] for r in rows),
        },
    }
    path = os.path.join(HERE, "M_CHAIN_LAYOUT_RECOMMEND_COUNT_out.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1, sort_keys=True)
    print(f"[ok] M_CHAIN_LAYOUT_RECOMMEND_COUNT rec={total} A={ta} B={tb} C={tc} "
          f"bench={round(benchmark, 3)}%")


if __name__ == "__main__":
    main()
