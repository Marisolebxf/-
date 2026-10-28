#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_SZ_OPPORTUNITY_COUNT 深圳产业机遇数（W13-C1）。

口径（与 calc-logic v0.2.0 对齐后的可算代理）：
  机遇环节 = 关键叶级环节 ∧ 深圳相对全国显著薄弱
    - 关键：逐链 median(有企业叶级环节全国企业家数)，n_national >= median（463 个）
    - 薄弱：深圳份额 = sz/national < 全国基准 7.952%（= 136,326 / 1,714,457
      挂链次数口径，分子分母同单位），或 sz = 0
    - 计数：OPPORTUNITY_COUNT = 关键叶中薄弱环节个数（254）
  全国基准同时给出企业去重口径 6.767%（116,017 / 1,714,457）作敏感性，
  该口径下为 227。两套都写进产物，正文默认用同单位口径。

只读快照，零 SQL。"""
from __future__ import annotations

import json
import os
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as fh:
        return json.load(fh)


def tree_index(tree):
    codes = {n["industry_code"] for n in tree}
    roots = sorted(n["industry_code"] for n in tree if len(n["industry_code"]) == 7)
    has_child = {c[:-2] for c in codes if len(c) > 7 and c[:-2] in codes}
    leaves = sorted(c for c in codes if c not in has_child and c not in roots)
    return roots, leaves


def main() -> None:
    tree = load("chain_tree_20261021.json")
    stage = load("chain_stage_leaf_20261021.json")
    findex = load("chain_firm_index_20261023.json")
    layer = load("chain21_layer_20261022.json")
    probe = load("chain_live_result_probe_20261023.json")
    roots, leaves = tree_index(tree)
    names = {n["industry_code"]: n["industry_name"] for n in tree}
    chain_name = findex["chain_name"]

    total_members = sum(findex["chain_firms"].values())
    sz_members = sum(v for k, v in layer["chain_city"].items() if k.endswith("|深圳市"))
    bench = round(100.0 * sz_members / total_members, 3)
    bench_distinct = round(100.0 * 116017 / total_members, 3)

    rows, gaps, low = [], [], []
    key_total = 0
    for ch in roots:
        ls = [c for c in leaves if c[:7] == ch]
        nat_map = stage["leaf_firm_counts"].get(ch, {})
        sz_map = stage["cell_leaf_firm_counts"].get(ch + "|深圳市", {})
        positive = [nat_map[c] for c in ls if nat_map.get(c, 0) > 0]
        median = statistics.median(positive)
        key = [c for c in ls if nat_map.get(c, 0) > 0 and nat_map[c] >= median]
        g = [c for c in key if sz_map.get(c, 0) == 0]
        w = [c for c in key if sz_map.get(c, 0) > 0
             and 100.0 * sz_map[c] / nat_map[c] < bench]
        key_total += len(key)
        for c in g:
            gaps.append({"chain_code": ch, "chain_name": chain_name[ch],
                         "node_code": c, "node_name": names.get(c, ""),
                         "national_firms": nat_map[c], "sz_firms": 0,
                         "sz_share_pct": 0.0, "kind": "blank"})
        for c in w:
            low.append({"chain_code": ch, "chain_name": chain_name[ch],
                        "node_code": c, "node_name": names.get(c, ""),
                        "national_firms": nat_map[c], "sz_firms": sz_map[c],
                        "sz_share_pct": round(100.0 * sz_map[c] / nat_map[c], 2),
                        "kind": "thin_share"})
        rows.append({
            "chain_code": ch,
            "chain_name": chain_name[ch],
            "key_leaves": len(key),
            "blank": len(g),
            "thin_share": len(w),
            "opportunity": len(g) + len(w),
            "opportunity_rate_pct": round(100.0 * (len(g) + len(w)) / len(key), 2),
            "median_threshold": median,
            "sz_memberships": layer["chain_city"].get(ch + "|深圳市", 0),
            "chain_firms": findex["chain_firms"][ch],
            "sz_share_pct": round(
                100.0 * layer["chain_city"].get(ch + "|深圳市", 0)
                / findex["chain_firms"][ch], 2),
        })

    # 敏感性：不同基准 / 不同门槛下的计数，全部落盘，正文只取一套主值
    def count_with(bench_pct, key_mult=1.0):
        n = 0
        for ch in roots:
            ls = [c for c in leaves if c[:7] == ch]
            nat_map = stage["leaf_firm_counts"].get(ch, {})
            sz_map = stage["cell_leaf_firm_counts"].get(ch + "|深圳市", {})
            pos = [nat_map[c] for c in ls if nat_map.get(c, 0) > 0]
            med = statistics.median(pos) * key_mult
            for c in ls:
                if nat_map.get(c, 0) > 0 and nat_map[c] >= med:
                    s = sz_map.get(c, 0)
                    if s == 0 or 100.0 * s / nat_map[c] < bench_pct:
                        n += 1
        return n

    sensitivity = {
        "bench_membership_7_952": count_with(bench),
        "bench_distinct_6_767": count_with(bench_distinct),
        "bench_5pct": count_with(5.0),
        "bench_10pct": count_with(10.0),
        "bench_7_952_key_x1_5": count_with(bench, 1.5),
    }

    out = {
        "metric_id": "M_CHAIN_SZ_OPPORTUNITY_COUNT",
        "metric_name": "深圳产业机遇数",
        "support_judgment": "部分支持",
        "verdict_kind": "positive_evidence",
        "judgment_reason": (
            "机遇的『链×深圳 vs 全国』对照可以在链树上重算：463 个关键叶里，52 个深圳为零、"
            "202 个深圳份额低于全国基准 7.952%，合计 254 个薄弱环节，可作为『产业发展方向机遇』的可算代理。"
            "但 calc-logic 的三类机遇（产业发展方向/政策优化/创新方向）里，后两类需要政策建议与专利主题"
            "到环节的配对，gkx 无环节级标注，只能记缺口；且原结果表 chain_sz_opportunity 在 gkx 零表、"
            "live 侧仅 8 行未来产业种子样例（与 12 链只重名 1 条），机遇的价值排序与可投性无法计算，故判部分支持。"
        ),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "本件是截面指标：链树 + 挂链桥 + 叶级企业分布均为当日快照，"
            "口径内无年度序列，不涉及基期分母，故 used/missing 为空。"
        ),
        "sources": [
            "code/_snapshots21/chain_tree_20261021.json",
            "code/_snapshots21/chain_stage_leaf_20261021.json",
            "code/_snapshots21/chain_firm_index_20261023.json",
            "code/_snapshots21/chain21_layer_20261022.json",
            "code/_snapshots21/chain_live_result_probe_20261023.json",
        ],
        "rule": {
            "opportunity": "关键叶 ∧ (深圳份额 < 全国基准 或 深圳为零)",
            "key": "逐链 median(有企业叶级环节全国企业家数)；n_national >= median（463）",
            "bench": "136,326 深圳挂链次数 / 1,714,457 全国挂链次数 = 7.952%",
            "bench_alt": "116,017 深圳去重企业 / 1,714,457 = 6.767%（敏感性，227）",
            "not_used": "不用叶级企业数合计 ÷ 链企业数（§3.54：7 条链超 100%）",
        },
        "population": {
            "chain_firms_clean": total_members,
            "sz_memberships_4403": sz_members,
            "sz_distinct_firms_4403": 116017,
            "key_leaf_total": key_total,
            "leaf_total": len(leaves),
        },
        "headline": {
            "bench_pct": bench,
            "bench_distinct_pct": bench_distinct,
            "key_leaves": key_total,
            "blank_key_leaves": len(gaps),
            "thin_share_key_leaves": len(low),
            "industry_direction_opportunity_count": len(gaps) + len(low),
            "opportunity_count": len(gaps) + len(low),
            "opportunity_rate_pct": round(100.0 * (len(gaps) + len(low)) / key_total, 2),
            "blank_share_of_opportunity_pct": round(100.0 * len(gaps) / (len(gaps) + len(low)), 2),
        },
        "type_breakdown": {
            "industry_direction": {
                "count": len(gaps) + len(low),
                "status": "proxy_computable",
                "note": "关键环节缺口清单，作为『产业发展方向机遇』的可算代理；不是 suggestions 文本抽取",
            },
            "policy_optimization": {
                "count": None,
                "status": "blocked",
                "reason": "政策优化机遇需 policy 与链/环节的可执行建议配对；dwd_policy_base 无环节级标注，"
                          "879 条深圳政策只有 13 条能按链命中，无法抽出建议条目",
            },
            "innovation_direction": {
                "count": None,
                "status": "blocked",
                "reason": "创新方向机遇需专利/技术主题到环节的映射；专利申请人名仅 23,756/169,226 能映射到链，"
                          "且只落首个链、无环节级，无法去重成条",
            },
        },
        "sensitivity": sensitivity,
        "by_chain": rows,
        "live_probe": {k: probe[k] for k in (
            "gkx_has_result_face", "gkx_chain_related_tables", "live_table_rows",
            "live_usable", "live_unusable_reason", "verdict")},
        "opportunities_blank": sorted(gaps, key=lambda x: (-x["national_firms"], x["node_code"])),
        "opportunities_thin": sorted(low, key=lambda x: (-x["national_firms"], x["node_code"])),
        "checks": {
            "sum_key_leaves": sum(r["key_leaves"] for r in rows),
            "sum_opportunity": sum(r["opportunity"] for r in rows),
            "blank_plus_thin": len(gaps) + len(low),
            "gap_matches_key_node_coverage_gap": (len(gaps) == 52),
        },
        "gaps": [
            "chain_sz_opportunity / chain_sz_advantage 在 gkx 侧 0 表；live 侧 8 行是未来产业种子样例，与 12 链只重名 1 条（GAP-CHAIN-RESULT-TABLE）",
            "政策优化/创新方向两类机遇无环节级标注，本件只还原产业发展方向一类",
            "机遇价值量、优先级、可投性三列无真源，只能给环节名单不能给排序",
            "全国基准用挂链次数，若改为去重企业数则 254 → 227，口径差 27 个环节",
            "深圳判定按登记地 4403，实际经营地/分支机构不可得",
        ],
    }
    path = os.path.join(HERE, "M_CHAIN_SZ_OPPORTUNITY_COUNT_out.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1, sort_keys=True)
    print(f"[ok] M_CHAIN_SZ_OPPORTUNITY_COUNT bench={bench}% "
          f"opportunity={len(gaps) + len(low)}/{key_total} "
          f"(blank {len(gaps)} thin {len(low)})")


if __name__ == "__main__":
    main()
