#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SYNTH_GRAPHAPI_116_1 图谱 API 节点/边供给能力（20261023，W16-F1）。

口径
----
「图 API」不是要交付一个 HTTP 服务，而是交付**每个图端点能不能供数**的清单：
节点域（论文/专利/企业/机构/人才/政策/产业链）各多少、边类型（共著/共同申请人/
投资/股东/产业标签/技术应用/转让/政策/人才/服务/合作）各多少、哪些端点能返回、
哪些必须 404。所有计数来自已落盘快照与 gkx 实查，不新发全表扫。

9 类关系按 P20 口径：4 类有边（投资/归属/产业所属/技术应用），5 类缺结构。
产出：code/M_SYNTH_GRAPHAPI_116_1_out.json
"""
from __future__ import annotations

import json

import _f1_common as F

MID = "M_SYNTH_GRAPHAPI_116_1"
G = F.load("graph_algo_23_20261023.json")
E = F.load("ent_graph109_20261023.json")
B = F.load("inventor_scholar_bridge_20261023.json")
IDX = F.load("chain_firm_index_20261023.json")
PAPER = F.load("papers_city_year_gkx21.json")
BASE = F.load("base_20261021.json")
EDGE_ROWS = F.load("ent_edges_20261021.json")


def main() -> None:
    ps = {p["id"]: p for p in G["point_sets"]}
    p0, p2 = ps["P0"], ps["P2"]
    ff = E["firm_firm"]
    # 企业—企业图节点必须与 M_ORG_GRAPH_115_1 同口径：两端都在底册、去掉自环、无向去重。
    # 快照 `ent_graph109` 的 node_with_edge_n=19,835 未做底册过滤，含 67 个底册外端点，
    # 与 115 的 19,768 差 67；此处现算，避免两件同域节点数打架。
    _base_ids = {r[0] for r in BASE}
    _ff_pairs = set()
    for _a, _b in EDGE_ROWS["invest"] + EDGE_ROWS["shareholder"]:
        if _a in _base_ids and _b in _base_ids and _a != _b:
            _ff_pairs.add(tuple(sorted((_a, _b))))
    _ff_nodes = len({_x for _p in _ff_pairs for _x in _p})
    rel = E["relation_rows"]
    avail = [r for r in rel if r["status"] in ("available", "proxy")]
    absent = [r for r in rel if r["status"] == "absent"]

    nodes = {
        "paper": {"rows": 100900, "snapshot": "a25_paper_panel.json",
                  "graph_nodes": p0["n_nodes"], "note": "论文 100,900 篇；入图机构 20,436 个"},
        "paper_institution": {"rows": p0["n_nodes"], "graph_nodes": p0["n_nodes"],
                              "note": "原始机构串，未做上下级归并"},
        "patent": {"rows": 2939895, "note": "按公开件计，未做同族合并（§3.67）"},
        "patent_applicant": {"rows": 169226, "note": "全量申请人去重数（star_applicant_agg_gkx）"},
        "patent_inventor": {"rows": B["rows"]["inventor_rows"],
                            "distinct_names": B["rows"]["inventor_distinct_raw"],
                            "covered_patents": B["rows"]["inventor_patents"],
                            "note": "20,000 件专利样本，非全量"},
        "scholar": {"rows": B["rows"]["scholar_rows"], "names": B["rows"]["scholar_names"],
                    "relation_rows": B["rows"]["relation_rows"],
                    "relation_scholars": B["rows"]["relation_scholars"]},
        "firm": {"rows": E["nodes"]["base_firm_n"],
                 "with_any_edge": E["nodes"]["firm_with_any_edge_n"],
                 "firm_firm_nodes": _ff_nodes},
        "research_org": {"rows": 20000, "note": "dwd_forg_research_org_info 20,000 行（样例表）"},
        "university": {"rows": 20000, "note": "dwd_forg_university_org_info 20,000 行（样例表）"},
        "policy": {"rows": 20000, "city_tagged": 10294, "note": "dwd_policy_base 20,000 条"},
        "industry_chain": {"rows": 12, "l1": 41, "tree_nodes": 1273},
    }

    edges = {
        "coauthor": {"rows": p0["n_edges"], "nodes": p0["n_nodes"],
                     "source": "dwd_zh_paper.author_info_list", "status": "available"},
        "coapplicant": {"rows": E["collaboration"]["coassignee_pair_n"],
                        "in_base": E["collaboration"]["coassignee_pair_in_base_n"],
                        "patents_with_multi": E["collaboration"]["patent_with_multi_assignee_n"],
                        "source": "dwd_patent_assignees", "status": "proxy"},
        "invest": {"rows": E["relation_rows"][0]["edge_n"],
                   "source": "dwd_org_invest_info", "status": "available"},
        "shareholder": {"rows": E["relation_rows"][1]["edge_n"],
                        "source": "dwd_org_shareholder_info", "status": "available"},
        "industry_chain": {"rows": E["relation_rows"][2]["edge_n"],
                           "source": "dwd_org_industry_tags", "status": "available"},
        "industry_l1": {"rows": E["industry"]["firm_l1_pair_n"],
                        "source": "dwd_org_industry_tags", "status": "available"},
        "tech_ipc": {"rows": E["tech"]["firm_ipc_pair_n"],
                     "source": "dwd_patent × IPC4", "status": "proxy"},
        "transfer": {"rows": E["transfer"]["pair_n"],
                     "rows_raw": E["transfer"]["rows"],
                     "source": "patent_transfer_rows_20261022.json", "status": "proxy"},
        "policy": {"rows": 0, "source": "—", "status": "absent"},
        "talent": {"rows": 0, "source": "—", "status": "absent"},
        "service": {"rows": 0, "source": "—", "status": "absent"},
        "cooperation": {"rows": 0, "source": "—", "status": "absent"},
    }

    endpoints = [
        {"path": "/graph/node/paper/{id}", "status": "available",
         "returns": "论文节点 + 作者机构列表 + 年份", "basis": "a25_paper_panel"},
        {"path": "/graph/node/firm/{org_id}", "status": "available",
         "returns": "企业节点 + 投资/股东/产业标签邻居", "basis": "base + ent_edges + industry"},
        {"path": "/graph/node/patent/{id}", "status": "partial",
         "returns": "专利节点 + 申请人；发明人仅 20,000 件样本有", "basis": "dwd_patent + inventors"},
        {"path": "/graph/neighbors/coauthor/{inst}", "status": "available",
         "returns": "机构共著邻居（边权=共同署名篇数）", "basis": "collab graph P2"},
        {"path": "/graph/neighbors/invest/{org_id}", "status": "available",
         "returns": "投资/股东邻居", "basis": "ent_edges"},
        {"path": "/graph/path", "status": "partial",
         "returns": "只在同域内最短路（论文共著 P2 / 企业投资图 P2）；跨域 404",
         "basis": "无统一 node_id，跨域路径不可建"},
        {"path": "/graph/community/{domain}", "status": "partial",
         "returns": "仅论文共著图返回 Louvain 社群；企业图社群为算法产物",
         "basis": "graph_algo_23 + ent_graph109"},
        {"path": "/graph/centrality/{domain}", "status": "partial",
         "returns": "论文图 P2 四类中心性；企业图仅度/中介",
         "basis": "graph_algo_23"},
        {"path": "/graph/policy/{id}", "status": "unavailable",
         "returns": "404：政策图节点/边在 gkx 不存在", "basis": "policy_graph_node/edge 0 行"},
        {"path": "/graph/cross-domain/path", "status": "unavailable",
         "returns": "404：无统一节点编号，跨域边只有 4/9 类", "basis": "graph_node 缺表"},
    ]

    def node_total():
        return sum(v.get("rows", 0) for v in nodes.values())

    derived = {
        "relation_available_pct": {
            "value": F.pct(len(avail), len(rel)),
            "numerator": len(avail), "denominator": len(rel),
            "denominator_note": "有边/代理边的关系类数 / 9 类要求（4 / 9）",
        },
        "relation_absent_n": {
            "value": len(absent), "numerator": len(absent), "denominator": len(rel),
            "denominator_note": "缺结构的关系类数 / 9 类（5 / 9）",
        },
        "paper_graph_p2_node_share_pct": {
            "value": p2["coverage_nodes"] * 100, "numerator": p2["n_nodes"],
            "denominator": p0["n_nodes"],
            "denominator_note": "论文图 P2 节点数 / P0 节点数（15,223 / 20,436）",
        },
        "paper_graph_p2_edge_share_pct": {
            "value": p2["coverage_edges"] * 100, "numerator": p2["n_edges"],
            "denominator": p0["n_edges"],
            "denominator_note": "论文图 P2 边数 / P0 边数（36,965 / 38,208）",
        },
        "patent_applicant_map_pct": {
            "value": 92.9898, "numerator": 157363, "denominator": 169226,
            "denominator_note": "能落到底册的申请人名数 / 申请人去重数（157,363 / 169,226）",
        },
        "paper_with_inst_pct": {
            "value": F.pct(100865, 100900), "numerator": 100865, "denominator": 100900,
            "denominator_note": "有机构串的论文数 / 论文总数（100,865 / 100,900）",
        },
        "paper_with_city_pct": {
            "value": F.pct(47802, 100900), "numerator": 47802, "denominator": 100900,
            "denominator_note": "可归珠三角城市的论文数 / 论文总数（47,802 / 100,900）",
        },
        "policy_city_tagged_pct": {
            "value": 51.47, "numerator": 10294, "denominator": 20000,
            "denominator_note": "有城市标签的政策数 / 政策总数（10,294 / 20,000）",
        },
        "firm_with_any_edge_pct": {
            "value": F.pct(E["nodes"]["firm_with_any_edge_n"], E["nodes"]["base_firm_n"]),
            "numerator": E["nodes"]["firm_with_any_edge_n"], "denominator": E["nodes"]["base_firm_n"],
            "denominator_note": "至少有一条可用关系的底册企业数 / 底册企业数（177,444 / 189,116）",
        },
        "firm_firm_node_pct": {
            "value": F.pct(_ff_nodes, E["nodes"]["base_firm_n"]),
            "numerator": _ff_nodes, "denominator": E["nodes"]["base_firm_n"],
            "denominator_note": f"企业—企业图节点数 / 底册企业数（{_ff_nodes:,} / {E['nodes']['base_firm_n']:,}）",
        },
        "coapplicant_in_base_pct": {
            "value": F.pct(E["collaboration"]["coassignee_pair_in_base_n"],
                           E["collaboration"]["coassignee_pair_n"]),
            "numerator": E["collaboration"]["coassignee_pair_in_base_n"],
            "denominator": E["collaboration"]["coassignee_pair_n"],
            "denominator_note": "两端都在底册的共同申请人对 / 全部共同申请人对（14 / 1,192）",
        },
        "transfer_resolved_pct": {
            "value": F.pct(E["transfer"]["resolved_both_ends_n"], E["transfer"]["rows"]),
            "numerator": E["transfer"]["resolved_both_ends_n"], "denominator": E["transfer"]["rows"],
            "denominator_note": "两端都能解析的转让行 / 转让行数（212 / 22,809）",
        },
        "inventor_sample_coverage_pct": {
            "value": F.pct(B["rows"]["inventor_patents"], 2939895),
            "numerator": B["rows"]["inventor_patents"], "denominator": 2939895,
            "denominator_note": "发明人表覆盖专利件数 / 专利全表行数（20,000 / 2,939,895）",
        },
        "tech_ipc_per_firm": {
            "value": E["tech"]["mean_ipc_per_firm"], "numerator": E["tech"]["firm_ipc_pair_n"],
            "denominator": E["tech"]["firm_n"],
            "denominator_note": "企业—IPC4 对数 / 有 IPC 的企业数（523,352 / 122,563）",
        },
        "endpoint_available_pct": {
            "value": F.pct(sum(1 for e in endpoints if e["status"] == "available"), len(endpoints)),
            "numerator": sum(1 for e in endpoints if e["status"] == "available"),
            "denominator": len(endpoints),
            "denominator_note": "完全可用的端点 / 10 个端点",
        },
        "endpoint_partial_pct": {
            "value": F.pct(sum(1 for e in endpoints if e["status"] == "partial"), len(endpoints)),
            "numerator": sum(1 for e in endpoints if e["status"] == "partial"),
            "denominator": len(endpoints),
            "denominator_note": "部分可用（需降级/限域）的端点 / 10 个端点",
        },
        "endpoint_unavailable_pct": {
            "value": F.pct(sum(1 for e in endpoints if e["status"] == "unavailable"), len(endpoints)),
            "numerator": sum(1 for e in endpoints if e["status"] == "unavailable"),
            "denominator": len(endpoints),
            "denominator_note": "不可用（应 404）的端点 / 10 个端点",
        },
        "node_domain_rows_total": {
            "value": node_total(), "numerator": node_total(), "denominator": "7+ 节点域",
            "denominator_note": "各节点域行数直接相加只作规模参考；域间有重叠，不是单一图节点数",
        },
    }

    payload = {
        "metric_name": "图谱 API 节点/边供给能力",
        "source": {
            "db": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）",
            "snapshots": [
                "code/_snapshots21/graph_algo_23_20261023.json",
                "code/_snapshots21/ent_graph109_20261023.json",
                "code/_snapshots21/inventor_scholar_bridge_20261023.json",
                "code/_snapshots21/chain_firm_index_20261023.json",
                "code/_snapshots21/papers_city_year_gkx21.json",
            ],
        },
        "nodes": nodes,
        "edges": edges,
        "relation_9": rel,
        "relation_available_n": len(avail),
        "relation_absent_n": len(absent),
        "endpoints": endpoints,
        "api_contract": {
            "version": "20261023",
            "id_spaces": {
                "paper": "dwd_zh_paper.id",
                "firm": "dwd_org_base_info.org_id",
                "patent": "dwd_patent.patent_id",
                "policy": "dwd_policy_base.id",
                "industry": "industry_code (INB4/INB6)",
            },
            "cross_domain_id": None,
            "pagination": "node/edge 端点一律 limit≤1000、cursor=主键；禁止全图导出",
            "rate_limit": "单客户端 ≤5 req/s；全表扫类查询不开放",
        },
        "blocked": {
            "graph_node": "gkx 无表；live ADS 145 行为 ORG0000000x 演示节点",
            "graph_edge": "gkx 无表；live ADS 589 行为演示边",
            "graph_membership": "gkx 无表；live ADS 120 行",
            "enterprise_centrality": "gkx 无表；live ADS 114 行",
            "policy_graph_node": "gkx 无表；live ADS 806 行",
            "policy_graph_edge": "gkx 无表；live ADS 3,726 行，calc_batch_id=mock_20260623",
        },
        "rejected_dimensions": [
            {"dimension": "政策图端点",
             "reason": "policy_graph_node / policy_graph_edge 在 gkx 均不存在；"
                       "live ADS 的 806 / 3,726 行是 mock_20260623 造数",
             "replacement": "政策只作为文本节点，不提供图邻居/路径",
             "negative_evidence": "code/_probe_blocked_f1_20261023.json → policy_graph_node、policy_graph_edge"},
            {"dimension": "跨域最短路",
             "reason": "无统一 node_id；graph_node 缺表，企业/论文/专利/政策各自一套 id",
             "replacement": "同域内最短路（论文共著 P2、企业投资图 P2）",
             "negative_evidence": "graph_node：gkx 0 行；api_contract.cross_domain_id=null"},
            {"dimension": "人才/服务/合作边",
             "reason": "发明人表无 org_id；svc 关系表 0 张；coop 表 0 张",
             "replacement": "人才只给姓名桥匹配率；服务/合作端点 404",
             "negative_evidence": "P20、P14、_probe_blocked_f1_20261023.json"},
            {"dimension": "社区归属官方口径",
             "reason": "graph_membership 缺表；Louvain 社群编号不稳定（§3.60）",
             "replacement": "社群端点标 experimental，不返回稳定主数据",
             "negative_evidence": "graph_membership：gkx 0 行；§3.60 删边稳定性"},
        ],
        "verdict_kind": "negative_evidence",
        "absence_probe": F.absence_probe(['graph_node', 'graph_edge', 'graph_membership', 'enterprise_centrality', 'policy_graph_node', 'policy_graph_edge']),
        "derived": derived,
        "sources": [
            "code/_snapshots21/graph_algo_23_20261023.json",
            "code/_snapshots21/ent_graph109_20261023.json",
            "code/_snapshots21/inventor_scholar_bridge_20261023.json",
            "code/_probe_blocked_f1_20261023.json",
            "PENDING_RULINGS_20261023.md P20",
        ],
    }

    F.write_out(MID, payload, support="部分支持", used=[], missing=[],
                note="图谱 API 是截面能力清单，不做年度切片；各节点域的行数来自各自快照，"
                     "域间重叠，不能相加当单一图规模。")
    print(json.dumps({"nodes": len(nodes), "edges": len(edges),
                      "available": len(avail), "absent": len(absent),
                      "endpoints": len(endpoints)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
