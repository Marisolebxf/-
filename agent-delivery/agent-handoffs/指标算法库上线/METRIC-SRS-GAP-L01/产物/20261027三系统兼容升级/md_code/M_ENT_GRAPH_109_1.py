#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_GRAPH_109_1 企业实体关系抽取（零 DB，族级快照重算）。

SRS 序号 109 要求 9 类关系；本件按「结构面是否具备」逐类判定，并把可建的四类建边：
  投资 / 归属 / 产业所属 / 技术应用（技术转移作为技术应用的补充证据）。
输出不含任何 centrality/score 造数列，只交付边清单计数与图结构统计。
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21", "ent_graph109_20261023.json")
EDGES = os.path.join(HERE, "_snapshots21", "ent_edges_20261021.json")
INDEX = os.path.join(HERE, "_snapshots21", "chain_firm_index_20261023.json")
OUT = os.path.join(HERE, "M_ENT_GRAPH_109_1_out.json")


def pct(a, b):
    return round(a / b * 100, 4) if b else 0.0


def main():
    d = json.load(open(SNAP, encoding="utf-8"))
    ff = d["firm_firm"]
    ind = d["industry"]
    tech = d["tech"]
    tr = d["transfer"]
    co = d["collaboration"]
    nodes = d["nodes"]

    # 原始行数不在 graph109 快照里，从边快照的 meta 读取，避免正文手算
    em = json.load(open(EDGES, encoding="utf-8"))["meta"]
    invest_rows_n = int(em["invest"]["rows"])
    sh_rows_n = int(em["shareholder"]["rows"])
    sh_nonnull_n = int(em["shareholder"]["edges_nonnull"])
    sh_unique_n = int(em["shareholder"]["edges_unique"])
    idx = json.load(open(INDEX, encoding="utf-8"))
    chain_name = idx["chain_name"]

    base_n = nodes["base_firm_n"]
    isolate_n = base_n - ff["node_with_edge_n"]
    any_edge_n = nodes["firm_with_any_edge_n"]

    # 关系覆盖：4 类可用（投资/归属/产业所属/技术应用），1 类仅 14 条偶然边，4 类无结构
    rel = []
    for r in d["relation_rows"]:
        x = dict(r)
        if x["relation"] == "科研合作":
            x["status"] = "insufficient" if co["coassignee_pair_in_base_n"] else "absent"
            x["edge_n"] = co["coassignee_pair_in_base_n"]
        rel.append(x)

    # 派生比值：分子分母都取本件产物/同批快照内的字段，正文只引用这里的结果
    derived = {
        "invest_raw_rows_n": invest_rows_n,
        "invest_in_base_share_of_raw_rows_pct": pct(ff["invest_edge_n"], invest_rows_n),
        "shareholder_raw_rows_n": sh_rows_n,
        "shareholder_nonnull_edge_n": sh_nonnull_n,
        "shareholder_dedup_edge_n": sh_unique_n,
        "shareholder_in_base_share_of_dedup_pct": pct(ff["shareholder_edge_n"], sh_unique_n),
        "firm_l1_over_chain_edge_n": ind["firm_l1_pair_n"] - ind["firm_chain_pair_n"],
        "transfer_resolved_both_ends_share_of_rows_pct": pct(tr["resolved_both_ends_n"], tr["rows"]),
        "transfer_pair_share_of_rows_pct": pct(tr["pair_n"], tr["rows"]),
        "chain_share_of_industry_base_pct": {
            chain_name.get(c, c): pct(n, ind["base_firm_n"])
            for c, n in ind["chain_firm_n"].items()
        },
        "denominator_note": "invest_in_base_share_of_raw_rows_pct 的分母是投资表原始行 46,967；"
                            "shareholder_in_base_share_of_dedup_pct 的分母是归属表去重边 70,034；"
                            "firm_l1_over_chain_edge_n = 一级环节边 49,234 − 链边 35,046；"
                            "transfer_* 的分母是转让表原始行 22,809；"
                            "chain_share_of_industry_base_pct 的分母是产业所属企业 35,046。",
    }

    doc = {
        "metric_id": "M_ENT_GRAPH_109_1",
        "metric_name": "企业实体关系抽取",
        "script": "M_ENT_GRAPH_109_1.py",
        "data_source": "gkx @ 183.240.141.251:3318（只读）",
        "grain": "relation_type -> edge list; node = base enterprise / chain / L1 / IPC4",
        "probes": {
            "base_firm_n": base_n,
            "base_credit_valid_n": nodes["base_credit_valid_n"],
            "firm_with_any_edge_n": any_edge_n,
            "firm_with_any_edge_pct": pct(any_edge_n, base_n),
            "firm_without_firm_firm_edge_n": isolate_n,
            "firm_without_firm_firm_edge_pct": pct(isolate_n, base_n),
            "relation_required_n": 9,
            "relation_available_n": 4,
            "relation_insufficient_n": 1,
            "relation_absent_n": 4,
            "relation_coverage_pct": pct(4, 9),
            "relation_direct_coverage_pct": pct(3, 9),
            "firm_firm_edge_pct": pct(ff["node_with_edge_n"], base_n),
            "largest_component_share_of_base_pct": pct(ff["largest_component_n"], base_n),
            "no_any_edge_firm_n": base_n - any_edge_n,
            "no_any_edge_pct": pct(base_n - any_edge_n, base_n),
            "transfer_unresolved_pct": pct(tr["unresolved_n"], tr["rows"]),
            "coassignee_pair_in_base_pct": pct(co["coassignee_pair_in_base_n"], co["coassignee_pair_n"]),
            "firm_firm": {
                **{k: v for k, v in ff.items() if k != "top10_degree"},
                "isolate_n": isolate_n,
                "isolate_pct": pct(isolate_n, base_n),
            },
            "industry": {k: v for k, v in ind.items()},
            "tech": tech,
            "transfer": tr,
            "collaboration": co,
            "edge_total_by_type": {
                "invest": ff["invest_edge_n"],
                "shareholder": ff["shareholder_edge_n"],
                "industry_chain": ind["firm_chain_pair_n"],
                "industry_l1": ind["firm_l1_pair_n"],
                "tech_application": tech["firm_ipc_pair_n"],
                "tech_transfer": ff["transfer_edge_n"],
                "research_cooperation": co["coassignee_pair_in_base_n"],
            },
            "denominator_note": "企业侧比例分母是底册 189,116；关系类型覆盖率分母是 SRS 的 9 类。"
                                "两个分母不可互换，也不能用 190 万链上企业当底册。",
            "field_basis": {
                "投资": "dwd_org_invest_info，两端 org_id 均在底册",
                "归属": "dwd_org_shareholder_info，两端 org_id 均在底册",
                "产业所属": "dwd_org_industry_tags，industry_code 首个 INB4；一企一链（单值归属）",
                "技术应用": "dwd_patent 申请人名 × IPC 小类，名称对齐底册",
                "技术转移": "dwd_patent_transfer，转让前后权利人名均在底册且唯一对应",
            },
        },
        "derived": derived,
        "probes_negative": {
            "live": d["absent_probe"]["live"],
            "gkx_graph_tables": d["absent_probe"]["gkx_graph_tables"],
            "inventor_rows": d["absent_probe"]["inventor_rows"],
            "inventor_columns": d["absent_probe"]["inventor_columns"],
            "policy_rows": d["absent_probe"]["policy_rows"],
            "coop_tables": d["absent_probe"]["coop_tables"],
            "svc_tables": d["absent_probe"]["svc_tables"],
            "gkx_side": d["negative_evidence"]["gkx_side"],
            "live_side": d["negative_evidence"]["live_side"],
            "conclusion": d["negative_evidence"]["conclusion"],
        },
        "result": {
            "relation_rows": rel,
            "firm_firm_graph": {
                "node_n": ff["node_with_edge_n"],
                "undirected_edge_n": ff["undirected_pair_n"],
                "directed_edge_n": ff["directed_edge_n"],
                "component_n": ff["component_n"],
                "largest_component_n": ff["largest_component_n"],
                "largest_component_share_pct": ff["largest_component_share_pct"],
                "component_size_buckets": ff["component_size_buckets"],
                "degree_median": ff["degree_median"],
                "degree_p90": ff["degree_p90"],
                "degree_max": ff["degree_max"],
            },
            "bipartite": {
                "firm_chain_edge_n": ind["firm_chain_pair_n"],
                "firm_chain_node_n": ind["base_firm_n"],
                "firm_l1_edge_n": ind["firm_l1_pair_n"],
                "firm_ipc_edge_n": tech["firm_ipc_pair_n"],
                "firm_ipc_node_n": tech["firm_n"],
                "ipc4_node_n": tech["ipc4_n"],
            },
        },
        "support_judgment": "部分支持",
        "verdict_kind": "partial_relation_coverage",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面件：关系边是库内当前快照，无统一年度键；投资/转让有日期字段但"
                           "不构成年度序列，不设基期，不做跨年增长率。",
        "sources": [
            "code/_snapshots21/ent_graph109_20261023.json",
            "code/_snapshots21/ent_edges_20261021.json",
            "code/_snapshots21/base_20261021.json",
            "code/_snapshots21/chain_firm_index_20261023.json",
            "code/_snapshots21/patent_ipc4_by_name_20261021.json",
            "code/_snapshots21/patent_transfer_rows_20261022.json",
            "gkx.dwd_org_invest_info (46,967)", "gkx.dwd_org_shareholder_info (400,286)",
            "gkx.dwd_org_industry_tags (2,283,762)", "gkx.dwd_patent_assignees (22,198)",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    print("wrote", OUT)
    print("any_edge", any_edge_n, pct(any_edge_n, base_n), "isolate", isolate_n)
    print("ff", doc["result"]["firm_firm_graph"])
    print("relations", [(r["relation"], r["status"], r["edge_n"]) for r in rel])


if __name__ == "__main__":
    main()
