#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_DOMAIN_COVERAGE_COUNT 覆盖领域数（20261021 改源版）。

口径正本：gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_DOMAIN_COVERAGE_COUNT.md
  COUNT(DISTINCT cluster_id) over industry_cluster_map（15 集群）。
王惠正本：local-workspace/docs/metrics/王惠阶段性成果/20260817/指标计算逻辑-V3-2/M_ENT_DOMAIN_COVERAGE_COUNT.md

本件只读 code/_snapshots21/ 的落盘快照，不连数据库。
15 集群目录与 industry_cluster_map 在 gkx 与 live 均不存在（见探针），
故按 12 条产业链根码做代理口径，并给出「链→集群」不可映射的证据。
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _w13e3_common as C

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "M_ENT_DOMAIN_COVERAGE_COUNT_out.json")
ID = "M_ENT_DOMAIN_COVERAGE_COUNT"


def main():
    probe = C.load("w13e3_probe_20261023.json")
    tree = C.load("chain_tree_20261021.json")
    ch = C.chain_panel()
    base = C.base_panel()

    # 15 集群目录证据
    gkx_tables = probe["A_schema_scan"]["tables"]
    gkx_cols = probe["A_schema_scan"]["columns"]
    live = probe["F_live"]
    live_hits = live["table_name_hits"]["cluster"]
    live_exact = live["exact_counts"]

    roots = sorted(ch["firms"].keys())
    coverage_examples = {}
    for city in ["深圳市", "广州市", "东莞市", "惠州市", "北京市", "上海市", "杭州市", "成都市"]:
        n = ch["city_coverage"].get(city)
        if n is not None:
            coverage_examples[city] = n

    low_examples = {}
    for city, n in ch["city_coverage"].items():
        if n <= 6 and len(low_examples) < 8:
            low_examples[city] = {"coverage": n, "firms": ch["city_total"].get(city, 0)}

    # 按链覆盖的「链目录规模」与「声明目录规模」并列，不做伪映射
    nominal = C.pct(ch["n_chains"], 15, 2)

    result = {
        "declared_domain_catalog": {
            "name": "industry_cluster（10 战新 + 5 未来）",
            "n_declared": 15,
            "catalog_available_in_gkx": False,
            "catalog_available_in_live": False,
            "evidence": {
                "gkx_tables_matching_cluster": gkx_tables["table_name_hits"]["cluster"],
                "gkx_n_tables": gkx_tables["n_tables"],
                "gkx_cluster_id_columns": gkx_cols["column_hits"]["cluster_id"],
                "gkx_cluster_name_columns": gkx_cols["column_hits"]["cluster_name"],
                "gkx_n_cluster_columns": gkx_cols["n_cluster_columns"],
                "live_tables_matching_cluster": live_hits,
                "live_industry_cluster": live_exact.get("gkxlumenx_dim.industry_cluster"),
                "live_industry_cluster_map": live_exact.get("gkxlumenx_dim.industry_cluster_map"),
            },
        },
        "proxy_domain_catalog": {
            "name": "dwd_industry_chain_info 产业链根码 12 条",
            "n_chains": ch["n_chains"],
            "roots": roots,
            "chain_names": {k: C.load("chain_firm_index_20261023.json")["chain_name"][k] for k in roots},
            "tree_rows": len(tree) if isinstance(tree, list) else (tree.get("n_nodes") or 0),
            "tree_has_inb17_or_inb18": probe["B_chain_info"]["has_inb17"] + probe["B_chain_info"]["has_inb18"],
            "tag_distinct_industry_code": probe["C_chain_code_universe"]["distinct_industry_code"],
            "tag_has_inb17_or_inb18": probe["C_chain_code_universe"]["any_inb17_or_inb18"],
        },
        "nominal_chain_vs_declared_pct": nominal,
        "nominal_ratio_comparable": False,
        "nominal_ratio_note": "12 条链与 15 个集群没有码级映射，12/15 只表示两个目录的规模比，不是覆盖率。",
        "universe": {
            "tag_rows": ch["stats"].get("rows", 2283762),
            "bad_credit_rows": ch["stats"].get("bad_credit_rows", 2),
            "empty_link_rows": ch["stats"].get("empty_link_rows", 569303),
            "linked_firms_clean": ch["total"],
            "multi_code_rows": ch["stats"].get("multi_chain_rows", 131978),
            "multi_code_row_share_pct": C.pct(ch["stats"].get("multi_chain_rows", 131978),
                                              ch["stats"].get("rows", 2283762), 2),
        },
        "coverage_by_set": {
            "全国链属企业": {"n_firms": ch["total"], "coverage": ch["n_chains"]},
            "明星名单可对齐子集": {"n_firms": ch["roster_matched_rows"],
                                    "coverage": len(ch["roster_chain"]),
                                    "match_share_pct": ch["roster_matched_share_pct"]},
            "底册专利名可对齐子集": {"n_firms": ch["base_matched_names"],
                                        "coverage": len(ch["base_chain"]),
                                        "match_share_pct": ch["base_matched_share_pct"]},
            "深圳市": {"n_firms": ch["city_total"].get("深圳市", 0), "coverage": ch["city_coverage"].get("深圳市")},
            "广州市": {"n_firms": ch["city_total"].get("广州市", 0), "coverage": ch["city_coverage"].get("广州市")},
            "东莞市": {"n_firms": ch["city_total"].get("东莞市", 0), "coverage": ch["city_coverage"].get("东莞市")},
            "惠州市": {"n_firms": ch["city_total"].get("惠州市", 0), "coverage": ch["city_coverage"].get("惠州市")},
        },
        "city_coverage_examples": coverage_examples,
        "low_coverage_cities": low_examples,
        "city_coverage_dist": ch["city_coverage_dist"],
        "n_cities_evaluated": ch["n_cities"],
        "n_cities_full_12": ch["n_cities_full"],
        "city_full_12_share_pct": C.pct(ch["n_cities_full"], ch["n_cities"], 2),
        "chain_firms": ch["firms"],
        "chain_share_pct": ch["shares_pct"],
        "hhi": ch["hhi"],
        "top1_chain_pct": ch["top1_pct"],
        "top3_chain_pct": ch["top3_pct"],
        "per_firm": {
            "rule": "industry_code 首个 INB 链根；一家企业一个链根",
            "n_firms": ch["total"],
            "coverage_value": 1,
            "distribution": {"1": ch["total"]},
            "multi_code_rows_dropped": ch["stats"].get("multi_chain_rows", 131978),
        },
        "base": {
            "n_rows": base["n_rows"],
            "n_province": base["n_province"],
            "n_city": base["n_city"],
        },
        "five_cluster_names_with_chain_homonym": [
            "人工智能", "智能终端", "软件与信息服务", "生物医药", "合成生物"
        ],
        "cluster_to_chain_mapping": {
            "mapped_by_code": 0,
            "mapped_by_exact_name": 0,
            "homonym_only": 5,
            "note": "同名词不能当映射：无 cluster_id、无 map 表，同名词的成员范围也未核。",
        },
    }

    out = {
        "metric_id": ID,
        "metric_name": "覆盖领域数",
        "script": ID + ".py",
        "as_of": C.AS_OF,
        "source": {
            "db": C.DB_GKX,
            "snapshots": [
                "code/_snapshots21/chain_firm_index_20261023.json",
                "code/_snapshots21/chain_tree_20261021.json",
                "code/_snapshots21/base_20261021.json",
                "code/_snapshots21/star_roster_gkx_20261021.json",
                "code/_snapshots21/w13e3_probe_20261023.json",
            ],
        },
        "calc_logic_ref": "gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_DOMAIN_COVERAGE_COUNT.md",
        "wanghui_ref": "local-workspace/docs/metrics/王惠阶段性成果/20260817/指标计算逻辑-V3-2/M_ENT_DOMAIN_COVERAGE_COUNT.md",
        "support_judgment": "部分支持",
        "verdict_kind": "proxy_constructed",
        "four_judgment": {
            "表结构直接支持（开发库+三方库）": "否：两库均无「覆盖领域数」结果面；gkx 无 cluster/结果表，live 无结果表",
            "表数据直接支持（开发库+三方库）": "否：15 集群目录无数据载体",
            "依赖表结构支持（开发库/三方库）": "部分：企业↔链结构在 gkx（dwd_org_industry_tags），15 集群 dim 与 map 两库均无",
            "依赖表数据支持（开发库/三方库）": "是（降维后）：链属企业 1,714,457 家可算 12 链覆盖；集群维不可算",
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "本件是截面计数：链归属表无 stat_year 字段，输出的是当日快照上的集合覆盖数，"
                            "不存在年度分母，故 used/missing 为空；不是把缺年按 0 摊入。",
        "result": result,
        "extra_probes": {
            "tags_created_time_distinct": "单一批次（2026-08-27），无年度键",
            "chain_info_level_dist": probe["B_chain_info"]["level_dist"],
            "chain_info_root_count": probe["B_chain_info"]["root_7_count"],
            "live_nonempty_tables": live.get("nonempty_tables"),
            "live_enterprise_industry_chain_rows": live_exact.get("gkxlumenx_dwd.enterprise_industry_chain"),
        },
        "notes": [
            "15 集群目录（10 战新 + 5 未来）在 gkx 280 表中 0 命中，live 侧 industry_cluster / industry_cluster_map 直接不存在。",
            "gkx 的 industry_code 只出现 12 个链根码，没有 INB1701—1710 / INB1801—1805，因此无法用链码反推集群。",
            "代理口径只回答「这批企业覆盖了几条产业链」，不能回答「覆盖了几个 15 集群」。",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote", OUT)
    print("linked", ch["total"], "chains", ch["n_chains"], "cities_full", ch["n_cities_full"],
          "roster_matched", ch["roster_matched_rows"], "base_matched", ch["base_matched_names"])
    print("coverage examples", coverage_examples)


if __name__ == "__main__":
    main()
