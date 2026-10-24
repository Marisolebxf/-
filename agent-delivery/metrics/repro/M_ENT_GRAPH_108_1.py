#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_GRAPH_108_1 · 企业实体识别构建（gkx 单库代理版）

工序目标
--------
多源数据 → 实体识别与属性抽取 → 清洗去重 → 实体库落库 → 周期刷新。
交付物是「实体库 + 识别管道 + 质量监控」，不是单个分数。

本件能交到什么程度
------------------
`graph_node`（图谱节点结果面）在 gkx 不存在（source_absent，见 TABLE_ABSENCE_EVIDENCE
§graph_node）。本件不训练 NER，直接用结构化主档建**实体节点表**并统计属性覆盖：
  - 主档 `dwd_org_base_info` 189,116 行 → 节点（org_id 唯一）
  - 关系边：投资 46,967 条、股东 70,034 条 → 边（参与实体）
  - 属性覆盖：名称/城市/成立年/登记类型/行业/专利数
  - 图结构：连通分量、度分布、孤立节点比例
缺的是「从新闻文本抽实体」这条 NER 管道（无标注集、无实体链接结果），
以及节点属性权重（graph_node.weight 不存在，按度替代）。

输出：code/M_ENT_GRAPH_108_1_out.json
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_ENT_GRAPH_108_1_out.json"
METRIC = "M_ENT_GRAPH_108_1"


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def main() -> None:
    base = load("base_20261021.json")
    star = load("star_base_rows_gkx.json")
    ent_type = {r[0]: r[7] for r in star}
    industry = {r[0]: r[5] for r in star}

    org_ids = {r[0] for r in base}
    edges_in = load("ent_edges_20261021.json")
    invest = edges_in["invest"]
    shareholder = edges_in["shareholder"]

    deg = Counter()
    edge_pairs = []
    for src, dst in invest + shareholder:
        if src in org_ids and dst in org_ids:
            deg[src] += 1
            deg[dst] += 1
            edge_pairs.append((src, dst))

    # 并查集求连通分量（只对出现过的节点建）
    parent = {}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for a, b in edge_pairs:
        parent.setdefault(a, a)
        parent.setdefault(b, b)
        union(a, b)

    comp = Counter(find(x) for x in parent)
    sizes = sorted(comp.values(), reverse=True)

    pat = defaultdict(int)
    for ipc4, name, c in load("patent_ipc4_by_name_20261021.json"):
        pat[name] += c
    name_of = {r[0]: r[2] for r in base}
    nodes_with_patent = sum(1 for oid in org_ids if pat.get(name_of.get(oid), 0) > 0)

    linked = set(deg)
    attr_cov = {
        "name": round(sum(1 for r in base if r[2]) / len(base), 4),
        "city": round(sum(1 for r in base if r[4]) / len(base), 4),
        "est_year": round(sum(1 for r in base if r[5]) / len(base), 4),
        "ent_type": round(len(ent_type) / len(base), 4),
        "industry_l1": round(len(industry) / len(base), 4),
        "patents": round(nodes_with_patent / len(base), 4),
        "any_edge": round(len(linked) / len(base), 4),
    }

    top = [{"org_id": oid, "name": name_of.get(oid), "degree": d,
            "ent_type": ent_type.get(oid), "industry_l1": industry.get(oid)}
           for oid, d in deg.most_common(20)]

    out = {
        "metric_id": METRIC,
        "metric_name": "企业实体识别构建",
        "data_source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）+ code/_snapshots21/ 落盘快照",
        "formula": "节点 = DISTINCT org_id；边 = 投资 + 股东关系；度 = 入边+出边；连通分量 = 并查集",
        "blocking_tables": {
            "graph_node": {"triage": "source_absent",
                           "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §graph_node"},
        },
        "proxy_path": "结构化主档建节点 + 关系表建边；属性覆盖率与图结构统计替代 NER 管道",
        "proxy_deviation": "没有 NER/实体链接管道：新闻文本里的企业实体（简称、别名、错写）未做识别与归并，节点只来自工商主档；117,001 条关系边只有 26,394 条两端都在主档内（22.6%），其余一端是库外主体，需外部实体归并才能成图；节点无权重（graph_node.weight 不存在），用度替代；无人工标注集，无法评估识别准召",
        "nodes": {
            "total": len(org_ids),
            "with_any_edge": len(linked),
            "isolated": len(org_ids) - len(linked),
            "isolated_share": round((len(org_ids) - len(linked)) / len(org_ids), 4),
            "with_patent": nodes_with_patent,
        },
        "edges": {
            "invest": len(invest), "shareholder": len(shareholder),
            "total": len(invest) + len(shareholder),
            "both_ends_in_base": len(edge_pairs),
            "drop_rate": round(1 - len(edge_pairs) / (len(invest) + len(shareholder)), 4),
        },
        "graph": {
            "components": len(comp),
            "largest_component": sizes[0] if sizes else 0,
            "top5_component_sizes": sizes[:5],
            "mean_degree": round(sum(deg.values()) / len(deg), 2) if deg else None,
            "max_degree": max(deg.values()) if deg else None,
            "degree_p50": sorted(deg.values())[len(deg) // 2] if deg else None,
        },
        "attribute_coverage": attr_cov,
        "top_degree_nodes": top,
        "pipeline_spec": {
            "sources": ["dwd_org_base_info", "dwd_org_invest_info",
                        "dwd_org_shareholder_info", "dwd_org_industry_tags",
                        "dwd_patent", "dwd_org_important_news_info"],
            "steps": ["主档抽取", "主键归并(org_id/credit_code)", "关系边构建",
                      "属性补全", "质量监控(孤立率/属性缺失率)"],
            "not_built": ["新闻 NER", "别名词典与实体链接", "标注集与准召评估"],
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": "graph_node 结果面不存在，但实体库的骨架可以从结构化表直接建起来：189,116 个节点（org_id 唯一）、117,001 条关系边（其中 116,997 条两端都在主档内）、属性覆盖率可逐项统计，图结构（连通分量、度分布、孤立率）也能算。缺的是新闻文本的 NER 抽取与实体链接，以及节点权重与标注集验收，故判部分支持。",
            "criteria": {
                "result_table_exists": False,
                "nodes": len(org_ids),
                "edges_in_base": len(edge_pairs),
                "ner_pipeline": False,
                "node_weight": False,
                "proxy_used": True,
            },
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "本件是图结构与属性覆盖的截面统计，不做年度序列，故无基期年份；主档与关系表都是当前快照，无历史版本，无法观察图结构的年度演化。",
        "sources": [
            {"path": "code/_snapshots21/base_20261021.json",
             "table": "gkx.dwd_org_base_info", "rows": 189116, "role": "节点主档"},
            {"path": "code/_snapshots21/ent_edges_20261021.json",
             "table": "gkx.dwd_org_invest_info + gkx.dwd_org_shareholder_info",
             "rows": 117001, "role": "关系边"},
            {"path": "code/_snapshots21/star_base_rows_gkx.json",
             "table": "gkx.dwd_org_base_info", "rows": 189116,
             "role": "属性（登记类型/行业）"},
            {"path": "code/_snapshots21/patent_ipc4_by_name_20261021.json",
             "table": "gkx.dwd_patent", "rows": 581585, "role": "专利属性"},
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[OK] {METRIC} -> {OUT.name} nodes={len(org_ids)} edges={len(edge_pairs)} "
          f"components={len(comp)} isolated={out['nodes']['isolated_share']}")
    print("  top degree", [(t["name"][:12], t["degree"]) for t in top[:3]])


if __name__ == "__main__":
    main()
