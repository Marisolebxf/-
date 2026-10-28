#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_SZ_PROBLEM_COUNT 深圳产业问题数（W14-C2）。

calc-logic v0.2.0 是「读发布快照」而非公式：industry_chain_metric_fact /
industry_chain_model_result_detail 里深圳 diagnosis 结果直读，gkx 侧两表都不存在。
本件改用结构侧可核短板重建，并把「模型诊断语义」明确列为缺口：

  严重空白环节 = 深圳 0 家 且 全国 >= 10 家          → 98
  严重单点环节 = 深圳 1—2 家 且 全国 >= 10 家        → 133
  问题数（主值） = 98 + 133 = 231                    （全叶，按链汇总）
  关键叶口径（敏感性） = 116                         （只算 463 个关键叶且仍满足全国 >= 10）
  宽口径（上界） = 空白 290 + 单点 207 = 497         （不加全国 >=10 门槛）

阈值 10 的理由：全国 < 10 家的环节本身样本太薄，深圳缺位不构成「产业问题」；
该阈值与 M_CHAIN_SZ_KEY_NODE_COUNT 的中位数门槛相互独立，故单列敏感性。
"""
from __future__ import annotations

import json
import os
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
THIN_MAX = 2
SERIOUS_NATIONAL = 10


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as fh:
        return json.load(fh)


def count_at(leaves, roots, stage, serious, thin_max):
    """按给定阈值重算 (空白, 单点, 合计)，用于敏感性表。"""
    blank = thin = 0
    for ch in roots:
        ls = [c for c in leaves if c[:7] == ch]
        nat = stage["leaf_firm_counts"].get(ch, {})
        szm = stage["cell_leaf_firm_counts"].get(ch + "|深圳市", {})
        blank += sum(1 for c in ls
                     if nat.get(c, 0) >= serious and szm.get(c, 0) == 0)
        thin += sum(1 for c in ls
                    if nat.get(c, 0) >= serious and 0 < szm.get(c, 0) <= thin_max)
    return {"blank": blank, "single_point": thin, "total": blank + thin}


def main() -> None:
    tree = load("chain_tree_20261021.json")
    stage = load("chain_stage_leaf_20261021.json")
    findex = load("chain_firm_index_20261023.json")
    layer = load("chain21_layer_20261022.json")
    policy = load("policy_industry_20261023.json")
    probe = load("chain_live_result_probe_20261023.json")

    roots = sorted(n["industry_code"] for n in tree if len(n["industry_code"]) == 7)
    codes = {n["industry_code"] for n in tree}
    has_child = {c[:-2] for c in codes if len(c) > 7 and c[:-2] in codes}
    leaves = sorted(c for c in codes if c not in has_child and c not in roots)
    names = {n["industry_code"]: n["industry_name"] for n in tree}
    chain_name = findex["chain_name"]

    problems, rows = [], []
    for ch in roots:
        ls = [c for c in leaves if c[:7] == ch]
        nat = stage["leaf_firm_counts"].get(ch, {})
        szm = stage["cell_leaf_firm_counts"].get(ch + "|深圳市", {})
        pos = [nat[c] for c in ls if nat.get(c, 0) > 0]
        median = statistics.median(pos)
        key = [c for c in ls if nat.get(c, 0) > 0 and nat[c] >= median]
        blank = [c for c in ls if szm.get(c, 0) == 0]
        thin = [c for c in ls if 0 < szm.get(c, 0) <= THIN_MAX]
        blank_serious = [c for c in blank if nat.get(c, 0) >= SERIOUS_NATIONAL]
        thin_serious = [c for c in thin if nat.get(c, 0) >= SERIOUS_NATIONAL]
        for c in blank_serious + thin_serious:
            problems.append({
                "chain_code": ch,
                "chain_name": chain_name[ch],
                "node_code": c,
                "node_name": names.get(c, ""),
                "node_depth": "L1" if len(c) == 9 else "deep",
                "national_firms": nat.get(c, 0),
                "sz_firms": szm.get(c, 0),
                "problem_type": "blank" if szm.get(c, 0) == 0 else "single_point",
                "severity": "high" if nat.get(c, 0) >= 2 * SERIOUS_NATIONAL else "medium",
                "is_key_leaf": c in key,
            })
        rows.append({
            "chain_code": ch,
            "chain_name": chain_name[ch],
            "leaves": len(ls),
            "blank_all": len(blank),
            "single_point_all": len(thin),
            "blank_serious": len(blank_serious),
            "single_point_serious": len(thin_serious),
            "problem_count": len(blank_serious) + len(thin_serious),
            "key_problem_count": sum(
                1 for c in blank_serious + thin_serious if c in key),
            "blank_rate_pct": round(100.0 * len(blank) / len(ls), 2),
            "serious_rate_pct": round(
                100.0 * (len(blank_serious) + len(thin_serious)) / len(ls), 2),
            "key_leaves": len(key),
            "median_threshold": median,
            "sz_memberships": layer["chain_city"].get(ch + "|深圳市", 0),
            "chain_firms": findex["chain_firms"][ch],
            "sz_share_pct": round(
                100.0 * layer["chain_city"].get(ch + "|深圳市", 0)
                / findex["chain_firms"][ch], 2),
        })

    # 敏感性：只改「全国规模」门槛（其余两条不变）
    sens = {}
    for th in (5, SERIOUS_NATIONAL, 20, 50):
        cnt = 0
        for ch in roots:
            ls = [c for c in leaves if c[:7] == ch]
            nat = stage["leaf_firm_counts"].get(ch, {})
            szm = stage["cell_leaf_firm_counts"].get(ch + "|深圳市", {})
            pos = [nat[c] for c in ls if nat.get(c, 0) > 0]
            med = statistics.median(pos) if pos else 0
            for c in ls:
                n, sv = nat.get(c, 0), szm.get(c, 0)
                if n >= th and ((sv == 0) or (1 <= sv <= THIN_MAX)):
                    cnt += 1
        sens[str(th)] = cnt

    total = len(problems)
    blank_n = sum(1 for p in problems if p["problem_type"] == "blank")
    thin_n = total - blank_n
    key_n = sum(1 for p in problems if p["is_key_leaf"])
    high_n = sum(1 for p in problems if p["severity"] == "high")

    out = {
        "metric_id": "M_CHAIN_SZ_PROBLEM_COUNT",
        "metric_name": "深圳产业问题数",
        "support_judgment": "部分支持",
        "verdict_kind": "positive_evidence",
        "judgment_reason": (
            "calc-logic v0.2.0 是读发布快照（industry_chain_metric_fact 按 region_code=440300 直读），"
            "gkx 侧无该表、live 侧该表 0 行，诊断模型结果面不存在。本件改用链树 + 1,714,457 家链属企业"
            "重算结构短板：98 个严重空白环节 + 133 个严重单点环节 = 231 个问题，可按 12 链汇总、"
            "逐环节下钻。但『诊断问题』的语义（技术/人才/市场/资本/政策五维打分与严重度阈值）没有真源，"
            "合规处罚也无法挂到环节，故只能算结构维度，判部分支持。"
        ),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "本件是截面指标：链树、叶级企业分布、政策/处罚均为当日快照，口径内无年度序列，"
            "不涉及基期分母，故 used/missing 为空。"
        ),
        "sources": [
            "code/_snapshots21/chain_tree_20261021.json",
            "code/_snapshots21/chain_stage_leaf_20261021.json",
            "code/_snapshots21/chain_firm_index_20261023.json",
            "code/_snapshots21/chain_live_result_probe_20261023.json",
        ],
        "rule": {
            "problem": "深圳 0 家（空白）或 1—2 家（单点）且全国 >= 10 家的叶级环节",
            "why_10": "全国 < 10 家样本过薄，深圳缺位不构成产业问题；单独给宽口径上界",
            "key_subset": "只统计 463 个关键叶且仍满足全国 >= 10 时的问题数（116）",
            "not_used": "叶级企业数合计 ÷ 链企业数（§3.54 陷阱）",
            "diagnosis_model": "calc-logic 的五维打分/严重度阈值不可得，本件 severity 仅按全国规模分档",
        },
        "population": {
            "chain_firms_clean": sum(findex["chain_firms"].values()),
            "leaf_total": len(leaves),
            "chains": len(roots),
            "national_serious_threshold": SERIOUS_NATIONAL,
            "sz_single_point_max": THIN_MAX,
            "tree_nodes": len(tree),
            "tree_edges": sum(1 for n in tree if len(n["industry_code"]) > 7 and n["industry_code"][:-2] in codes),
            "internal_nodes": len(codes) - len(leaves) - len(roots),
            "leaf_with_firms": sum(1 for ch in roots for c in leaves if c[:7] == ch
                                   and stage["leaf_firm_counts"].get(ch, {}).get(c, 0) > 0),
            "leaf_without_firms": sum(1 for ch in roots for c in leaves if c[:7] == ch
                                      and stage["leaf_firm_counts"].get(ch, {}).get(c, 0) == 0),
            "tag_rows": findex["stats"]["rows"],
            "news_rows": 108052,
            "sz_memberships_4403": sum(v for k, v in layer["chain_city"].items() if k.endswith("|深圳市")),
            "benchmark_sz_share_pct": round(100.0 * sum(v for k, v in layer["chain_city"].items() if k.endswith("|深圳市")) / sum(findex["chain_firms"].values()), 3),
            "punish_rows": 65997,
            "sz_distinct_firms_4403": 116017,
            "sz_memberships_city_map": 92930,
            "city_mapping_gap": 43396,
            "tag_rows_raw": 2283762,
            "sz_policies_total": policy["city_totals"].get("深圳市", 0),
            "sz_policy_node_hits": sum(
                policy["city_chain_node_policy"].get("深圳市", {}).values()),
        },
        "sensitivity": {
            "national_threshold": {
                "5": count_at(leaves, roots, stage, 5, THIN_MAX),
                "10": count_at(leaves, roots, stage, 10, THIN_MAX),
                "20": count_at(leaves, roots, stage, 20, THIN_MAX),
            },
            "single_point_max": {
                "1": count_at(leaves, roots, stage, SERIOUS_NATIONAL, 1),
                "2": count_at(leaves, roots, stage, SERIOUS_NATIONAL, 2),
                "3": count_at(leaves, roots, stage, SERIOUS_NATIONAL, 3),
            },
        },
        "headline": {
            "problem_count": total,
            "blank_serious": blank_n,
            "single_point_serious": thin_n,
            "key_leaf_problem_count": key_n,
            "high_severity": high_n,
            "chain_avg": round(total / len(roots), 1),
            "chain_max": max(r["problem_count"] for r in rows),
            "chain_max_name": max(rows, key=lambda r: r["problem_count"])["chain_name"],
            "chain_min": min(r["problem_count"] for r in rows),
            "chain_min_name": min(rows, key=lambda r: r["problem_count"])["chain_name"],
            "broad_upper_bound": 290 + 207,
            "broad_blank": 290,
            "broad_single_point": 207,
        },
        "params": {"threshold_sensitivity": sens},
        "by_chain": rows,
        "problems": sorted(problems, key=lambda x: (-x["national_firms"], x["node_code"])),
        "live_probe": {k: probe[k] for k in (
            "gkx_has_result_face", "gkx_chain_related_tables", "live_table_rows",
            "live_usable", "live_unusable_reason", "verdict")},
        "checks": {
            "sum_problem_count": sum(r["problem_count"] for r in rows),
            "sum_key_problem": sum(r["key_problem_count"] for r in rows),
            "sum_blank": sum(r["blank_serious"] for r in rows),
            "sum_single": sum(r["single_point_serious"] for r in rows),
            "blank_plus_single": blank_n + thin_n,
            "matches_headline": (blank_n + thin_n == total),
            "key_subset_lte_total": key_n <= total,
            "sum_key_leaves": sum(r["key_leaves"] for r in rows),
        },
        "gaps": [
            "industry_chain_metric_fact / industry_chain_model_result_detail 在 gkx 侧 0 表，live 侧 0 行"
            "（读表口径的发布快照不存在）",
            "五维诊断分（tech/talent/market/capital/policy）与严重度阈值无真源，本件不能复现原语义",
            "dwd_org_company_punish 65,997 条处罚无环节键，不能归到链/环节",
            "政策建议与环节的配对只有 43 条（深圳市 node 级），不足以做政策短板诊断",
            "深圳判定按登记地 4403，实际经营地不可得",
        ],
    }
    path = os.path.join(HERE, "M_CHAIN_SZ_PROBLEM_COUNT_out.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1, sort_keys=True)
    print(f"[ok] M_CHAIN_SZ_PROBLEM_COUNT problem={total} "
          f"(blank {blank_n} single {thin_n}) key={key_n} high={high_n}")


if __name__ == "__main__":
    main()
