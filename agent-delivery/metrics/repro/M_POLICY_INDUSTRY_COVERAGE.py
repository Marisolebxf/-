#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""政策产业覆盖度（M_POLICY_INDUSTRY_COVERAGE）——只读快照。

注册表口径（`pending_algorithm`）：
    已覆盖产业节点数 / 产业链全节点数 × 100%
源侧本应是 `keywords` / `elements`；实测 `keywords`、`keypoints` 全表 0 行有值、
`theme` 仅 2 行有值，故政策侧实际只剩 `title`。

三个口径同时落盘，供甲方选一个发布：
  literal  ：1,261 个环节名全量子串匹配（注册表字面口径）
  no2char  ：剔除 24 个 2 字通用名（制造/测试/软件/农业/医药/化工/食品…）
  anchored ：只有政策同时点到「链名」时才把环节名计入（链锚定）

输入：code/_snapshots21/policy_industry_20261023.json
      code/_snapshots21/policy_struct_20261023.json（字段填充率）
输出：code/M_POLICY_INDUSTRY_COVERAGE_out.json
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).parent
IND = HERE / "_snapshots21" / "policy_industry_20261023.json"
STRUCT = HERE / "_snapshots21" / "policy_struct_20261023.json"
OUT = HERE / "M_POLICY_INDUSTRY_COVERAGE_out.json"

METRIC = "M_POLICY_INDUSTRY_COVERAGE"


def main() -> int:
    ind = json.loads(IND.read_text(encoding="utf-8"))
    st = json.loads(STRUCT.read_text(encoding="utf-8"))
    ov = ind["overall"]
    el = st["elements"]

    chains = []
    for c in sorted(ind["chains"], key=lambda d: -d["nodes_hit"]):
        chains.append({
            "chain_code": c["chain_code"],
            "chain_name": c["chain_name"],
            "nodes_total": c["nodes_total"],
            "nodes_hit": c["nodes_hit"],
            "coverage_pct": c["node_coverage_pct"],
            "nodes_hit_excl_2char": c["nodes_hit_excl_2char"],
            "coverage_excl_2char_pct": c["node_coverage_excl_2char_pct"],
            "nodes_hit_anchored": c["nodes_hit_anchored"],
            "policies_hit_t0": c["policies_hit_t0"],
            "policies_hit_t1": c["policies_hit_t1"],
            "top_nodes": c["top_nodes"][:5],
        })

    out = {
        "metric_id": METRIC,
        "support_judgment": "部分支持",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "截面指标，覆盖度按库内存量 20,000 条计，不设年度分母。"
            "库内 2023—2024 采集断档意味着「当前覆盖」实际停在 2022-08，"
            "本件不把它换算成「近年覆盖率」。"),
        "headline": {
            "policy_total": st["rows"],
            "chain_count": ind["chain_count"],
            "nodes_total": ov["nodes_total"],
            "nodes_hit": ov["nodes_hit"],
            "coverage_pct": ov["node_coverage_pct"],
            "coverage_excl_2char_pct": ov["node_coverage_excl_2char_pct"],
            "coverage_anchored_pct": ov["node_coverage_anchored_pct"],
            "nodes_hit_anchored": ov["nodes_hit_anchored"],
            "policies_hit_any_chain": ov["policies_hit_any_t0"],
            "share_any_chain_pct": ov["share_any_t0_pct"],
            "policies_hit_any_chain_with_abstract": ov["policies_hit_any_t1"],
            "share_any_chain_with_abstract_pct": ov["share_any_t1_pct"],
            "policies_hit_any_node": ov["policies_hit_node_t0"],
            "share_any_node_pct": ov["share_node_t0_pct"],
            "policies_chain_only": ov["policies_chain_only_t0"],
            "spread_ratio": round(ov["node_coverage_pct"]
                                  / ov["node_coverage_anchored_pct"], 4)
            if ov["node_coverage_anchored_pct"] else None,
        },
        "field_support": {
            "theme_nonnull": el["theme_nonnull"],
            "keywords_nonnull": el["keywords_nonnull"],
            "keypoints_nonnull": el["keypoints_nonnull"],
            "field_set": ["title", "keywords", "keypoints", "theme"],
            "effective_field": "title",
            "why": "四字段里 keywords/keypoints 全表 0 行有值、theme 仅 2 行，"
                   "匹配事实上只发生在标题上",
        },
        "chains": chains,
        "layers": {
            "literal": {"nodes_hit": ov["nodes_hit"], "pct": ov["node_coverage_pct"],
                        "note": "注册表字面口径；含 24 个 2 字通用名，上界"},
            "no2char": {"nodes_hit": ov["nodes_hit_excl_2char"],
                        "pct": ov["node_coverage_excl_2char_pct"],
                        "note": "剔除 2 字通用名后的稳健口径"},
            "anchored": {"nodes_hit": ov["nodes_hit_anchored"],
                         "pct": ov["node_coverage_anchored_pct"],
                         "note": "链锚定口径；要求政策同时点到链名，下界"},
        },
        "generic_name_effect": {
            "two_char_hits": [
                {"chain": n["chain_name"], "name": n["name"], "name_len": n["name_len"],
                 "policies": n["policies"]}
                for n in sorted([x for x in ind["node_hit_detail"]
                                 if x["policies"] > 0 and x["name_len"] <= 2],
                                key=lambda d: -d["policies"])
            ],
            "note": "2 字通用名命中数远高于具体环节名，是把「食品加工管理办法」算成"
                    "合成生物环节覆盖的直接原因",
        },
        "checks": [
            {"name": "各链节点数合计 = 树叶子节点（1,273 − 12 链根）",
             "value": sum(c["nodes_total"] for c in chains),
             "expected": ind["node_count"],
             "ok": sum(c["nodes_total"] for c in chains) == ind["node_count"]},
            {"name": "各链命中节点合计", "value": sum(c["nodes_hit"] for c in chains),
             "expected": ov["nodes_hit"], "ok": sum(c["nodes_hit"] for c in chains)
             == ov["nodes_hit"]},
            {"name": "字面口径 ≥ 锚定口径", "value": ov["node_coverage_pct"],
             "expected": ov["node_coverage_anchored_pct"],
             "ok": ov["node_coverage_pct"] >= ov["node_coverage_anchored_pct"]},
            {"name": "链级命中政策 ⊆ 全库", "value": ov["policies_hit_any_t0"],
             "expected": st["rows"], "ok": ov["policies_hit_any_t0"] <= st["rows"]},
        ],
        "provenance": {
            "snapshots": ["code/_snapshots21/policy_industry_20261023.json",
                          "code/_snapshots21/policy_struct_20261023.json"],
            "builders": ["code/_build_policy_industry_20261023.py",
                         "code/_build_policy_struct_20261023.py"],
            "tree": "code/_snapshots21/chain_tree_20261021.json",
            "source": ind["source"],
        },
        "notes": [
            "节点数 1,261 是 1,273 个树节点减去 12 个链根；链根不算「环节」。",
            "1,273 个节点里有 123 个重名，本件按 industry_code 去重、按 name 匹配，"
            "同名环节在它所属的每条链里各计一次。",
            "只用 title 匹配的覆盖率天然偏低；本件不把「没点到」解释成「政策不关注该产业」。",
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[OK] {OUT}")
    print("coverage", ov["node_coverage_pct"], "anch", ov["node_coverage_anchored_pct"],
          "no2char", ov["node_coverage_excl_2char_pct"])
    print("policies any", ov["policies_hit_any_t0"], "t1", ov["policies_hit_any_t1"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
