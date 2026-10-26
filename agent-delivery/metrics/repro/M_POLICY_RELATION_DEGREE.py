#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_POLICY_RELATION_DEGREE —— 政策关联度（P1 政策评估族，否定性证据件）

正本口径
--------
注册表 `cfg_metric-POLICY-seed.yaml`：`formula = pending_algorithm`，
「NebulaGraph 加权度中心性：support / apply_to / regulate / cite 四类边加权，权重待 QPOL-03」；
definition 另给一条临时默认：「按 pedigree 引用条数 + 标签共现做无权度数」。
无同 ID calc-logic 正本。

本脚本证明三件事
----------------
E1 四类业务边在 gkx 侧一张表都没有（280 表里无 policy_entity/policy_graph_edge/policy_graph_node）；
E2 注册表给的临时口径也不成立：`quote_policy` 真值只有 2 行（其余 19,998 行是字面 'NULL'），
   `theme` 2 行、`keywords` 0 行、`keypoints` 0 行，标签共现无字段可用；
   `pedigree` 列在 gkx.dwd_policy_base 的 33 列里不存在，live 的 policy_base_info 0 行；
E3 即便退到最宽的代理（标题命中产业链环节名），度分布仍是 93% 以上为 0，
   Gini 接近 1——这不是「关联度」，是「绝大多数政策一条边都没有」。

取数：gkx 共享快照（零 SQL）+ 两份逐表 COUNT(*) 清单。
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SNAP = os.path.join(HERE, "_snapshots21")
WORK = os.path.join(ROOT, "_work_gkx21")
OUT = os.path.join(HERE, "M_POLICY_RELATION_DEGREE_out.json")

EDGE_TYPES = ["support（扶持）", "apply_to（适用）", "regulate（监管）", "cite（引用）"]


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def pct(a, b, nd=4):
    return round(a * 100.0 / b, nd) if b else None


def gini(values):
    xs = sorted(values)
    n = len(xs)
    s = sum(xs)
    if n == 0 or s == 0:
        return None
    cum = 0.0
    for i, x in enumerate(xs, 1):
        cum += i * x
    return round((2 * cum) / (n * s) - (n + 1) / n, 6)


def main():
    base = load(os.path.join(SNAP, "policy_base_20261021.json"))
    struct = load(os.path.join(SNAP, "policy_struct_20261023.json"))
    fill = load(os.path.join(SNAP, "policy_field_fill_20261022.json"))
    fields = load(os.path.join(SNAP, "policy_fields_a23_20261021.json"))
    tree = load(os.path.join(SNAP, "chain_tree_20261021.json"))
    industry = load(os.path.join(SNAP, "policy_industry_20261023.json"))
    gkx_inv = load(os.path.join(WORK, "GKX_INVENTORY.json"))
    live_inv = load(os.path.join(WORK, "LIVE_INVENTORY.json"))

    n = len(base)
    cols = [r[0] for r in fields["columns"]["rows"]]

    # ---------------- E1：边表 / 实体表
    edge_like = ["policy_graph_edge", "policy_graph_node", "policy_entity",
                 "policy_entity_relation", "policy_entity_type", "policy_focus"]
    gkx_hits = [t for t in edge_like if t in gkx_inv]
    gkx_policy_tables = sorted(t for t in gkx_inv if "policy" in t)
    # 只留行数：查询耗时（sec）属易变键，按 v6 §十 不进产物
    live_hits = {t: live_inv[k]["rows"] for t in edge_like for k in live_inv if k.endswith("." + t)}
    live_policy_zero = {k: v["rows"] for k, v in live_inv.items()
                        if "policy" in k and v["rows"] == 0}

    # ---------------- E2：临时口径的字段真值
    quote_real = fill["fields"]["quote_policy"]["nonempty"]
    theme_real = struct["elements"]["theme_nonnull"]
    kw_real = struct["elements"]["keywords_nonnull"]
    kp_real = struct["elements"]["keypoints_nonnull"]
    support_json_null = struct["elements"]["support_json_type_dist"].get("JSON_NULL", 0)

    # quote_policy 的两行真值：解析出引用条数、可解析到库内政策的条数
    title_to_id = {}
    for b in base:
        title_to_id.setdefault((b.get("title") or "").strip(), b["id"])
    quote_probe = load(os.path.join(SNAP, "policy_aux_20261022.json"))["probes"]["theme_quote_rows"]
    quote_edges = 0
    quote_resolved = 0
    for row in quote_probe:
        try:
            arr = json.loads(row.get("quote_policy") or "[]")
        except Exception:
            arr = []
        quote_edges += len(arr)
        for name in arr:
            if (name or "").strip() in title_to_id:
                quote_resolved += 1

    # ---------------- E3：最宽代理（标题命中链树节点名）
    node_names = sorted({t["industry_name"] for t in tree if len(t["industry_name"]) >= 2})
    degree = []
    edges = 0
    for b in base:
        t = b.get("title") or ""
        d = sum(1 for nm in node_names if nm in t)
        degree.append(d)
        edges += d
    docs_any = sum(1 for d in degree if d)
    dist = {}
    for d in degree:
        dist[str(d)] = dist.get(str(d), 0) + 1
    g = gini(degree)
    top = sorted(range(len(degree)), key=lambda i: -degree[i])[:5]

    # 把引用边并进代理图：度 = 产业链节点边 + 引用边
    deg_with_quote = list(degree)
    for row in quote_probe:
        pid = row.get("id")
        idx = next((i for i, b in enumerate(base) if b["id"] == pid), None)
        if idx is not None:
            try:
                deg_with_quote[idx] += len(json.loads(row.get("quote_policy") or "[]"))
            except Exception:
                pass
    docs_any_all = sum(1 for d in deg_with_quote if d)

    out = {
        "metric_id": "M_POLICY_RELATION_DEGREE",
        "metric_name_zh": "政策关联度",
        "support_judgment": "完全不支持",
        "verdict_kind": "negative_evidence",
        "judgment_reason": (
            "关联度=图谱节点加权度中心性，依赖政策实体关系图谱的四类边。"
            "gkx 280 表里没有任何边表或实体表；注册表给的临时口径（pedigree 引用 + 标签共现）"
            "同样不成立：引用字段真值 2 行、标签字段 0—2 行、pedigree 列不存在。"
            "结构与数据两端都不具备可算闭环 → 完全不支持。"
        ),
        "publishable": False,
        "registered_metric_value": None,
        "headline": {
            "policy_nodes": n,
            "edge_tables_in_gkx": len(gkx_hits),
            "real_citation_rows": quote_real,
            "real_label_rows": {"theme": theme_real, "keywords": kw_real, "keypoints": kp_real},
            "proxy_policies_with_edge": docs_any,
            "proxy_zero_degree_pct": pct(n - docs_any, n),
            "proxy_gini": g,
            "verdict": "度中心性对 99% 以上节点无定义，不构成可发布的关联度",
        },
        "edge_source_audit": [
            {"edge": EDGE_TYPES[0], "table_in_gkx": None,
             "note": "support 边需要政策—企业/对象关系表；policy_support 全表 JSON null，"
                     "无对象可取，边无从生成"},
            {"edge": EDGE_TYPES[1], "table_in_gkx": None,
             "note": "apply_to 边需要政策—产业/技术关系表；gkx 无 policy_entity / policy_graph_edge"},
            {"edge": EDGE_TYPES[2], "table_in_gkx": None,
             "note": "regulate 边需要监管关系表；两库均无"},
            {"edge": EDGE_TYPES[3], "table_in_gkx": None,
             "note": f"cite 边的唯一候选字段 quote_policy 真值只有 {quote_real} 行，"
                     f"另 {n - quote_real:,} 行是字面 'NULL'；可解析到库内政策标题的引用 {quote_resolved} 条"},
        ],
        "field_truth": {
            "quote_policy_rows_real": quote_real,
            "quote_policy_rows_literal_null": 19998,
            "theme_rows_real": theme_real,
            "keywords_rows_real": kw_real,
            "keypoints_rows_real": kp_real,
            "policy_support_json_null_rows": support_json_null,
            "pedigree_column_present": "pedigree" in cols,
            "policy_base_columns": len(cols),
            "note": "字面 'NULL' 是字符串而不是 SQL NULL：`NULLIF(TRIM(col),'') IS NOT NULL` 会把"
                    "19,998 行全部算成「有值」（实测返回 20,000）。必须先排除字面 'NULL' 再判。",
        },
        "tables": {
            "gkx_policy_tables": gkx_policy_tables,
            "gkx_edge_or_entity_tables": gkx_hits,
            "live_edge_or_entity_tables": live_hits,
            "live_policy_tables_zero_rows": len(live_policy_zero),
            "live_policy_base_info_rows": live_inv.get("gkxlumenx_dwd.policy_base_info", {}).get("rows"),
            "mock_caveat": "live 的 policy_graph_node(806)/policy_graph_edge(3,726)/policy_entity(7,517) "
                           "登记在 Mock @ batch=mock_20260623，属造数面；"
                           "同批 MOCK_TABLE_REGISTRY.md 记录 weight 恒 1、model_version 带 demo 后缀，"
                           "不得作证据。",
        },
        "proxy_degree": {
            "method": "以标题命中链树节点名（≥2 字，1,150 个名字）作为政策—产业边，"
                      "叠加 quote_policy 的引用边，算无权度数",
            "edges": edges,
            "quote_edges_parsed": quote_edges,
            "quote_edges_resolved_to_local_policy": quote_resolved,
            "docs_with_edge": docs_any,
            "docs_with_edge_pct": pct(docs_any, n),
            "docs_with_edge_after_quote": docs_any_all,
            "zero_degree_docs": n - docs_any,
            "zero_degree_pct": pct(n - docs_any, n),
            "max_degree": max(degree),
            "mean_degree": round(edges / n, 4),
            "gini": g,
            "degree_dist": dict(sorted(dist.items(), key=lambda kv: int(kv[0]))),
            "top_nodes": [
                {"id": base[i]["id"], "title": (base[i]["title"] or "")[:50], "degree": degree[i]}
                for i in top
            ],
            "cross_check": {
                "policy_industry_snapshot": {
                    "nodes_total": industry["overall"]["nodes_total"],
                    "nodes_hit": industry["overall"]["nodes_hit"],
                    "node_coverage_pct": industry["overall"]["node_coverage_pct"],
                    "nodes_hit_excl_2char": industry["overall"]["nodes_hit_excl_2char"],
                },
                "note": "该快照按「节点→政策数」统计，本件按「政策→节点数」统计，两者是同一批边的两个投影；"
                        "节点侧 6.1063% 的环节覆盖与本件政策侧 6.345% 的有边率同量级，互相印证边源极稀。",
            },
        },
        "why_not_partial": (
            "「部分支持」要求主口径成立、只有个别维缺数据。本件的主口径是单一标量（每条政策的度），"
            "度的载体是边；四类边一张表都没有，代理边只覆盖 6.345% 的政策、其余 93.655% 恒为 0。"
            "对 93.655% 的主体没有定义，不是「部分维缺失」，是「主口径不成立」。"
        ),
        "repair_path": [
            "建 policy_entity / policy_graph_edge（edge_type 取 support/apply_to/regulate/cite，带权重与来源句）",
            "回填 quote_policy（现真值 2 行），并建政策标题—id 的引用消歧表",
            "补 policy_support.support_object，才能生成 support 边",
            "QPOL-03 签认边权与匹配规则后，才可把无权度数升级为加权度中心性",
        ],
        "sources": [
            "code/_snapshots21/policy_base_20261021.json（20,000 条）",
            "code/_snapshots21/policy_struct_20261023.json（theme/keywords/keypoints/policy_support 真值）",
            "code/_snapshots21/policy_field_fill_20261022.json（quote_policy=2）",
            "code/_snapshots21/policy_fields_a23_20261021.json（33 列清单，无 pedigree）",
            "code/_snapshots21/policy_aux_20261022.json（两条 quote_policy 原文）",
            "code/_snapshots21/chain_tree_20261021.json（1,273 节点）",
            "code/_snapshots21/policy_industry_20261023.json（节点侧覆盖交叉校验）",
            "_work_gkx21/GKX_INVENTORY.json / LIVE_INVENTORY.json（逐表 COUNT(*)）",
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面指标：关联度按当前政策集合的图结构一次性计算，不按年出值；"
                           "故无基期年。发布年只作节点属性，不进入度数的分母。",
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print("gkx edge tables:", gkx_hits)
    print("live edge/entity:", live_hits)
    print("quote real:", quote_real, "resolved:", quote_resolved, "of", quote_edges)
    print("proxy edges", edges, "docs_any", docs_any, "zero%", pct(n - docs_any, n), "gini", g)
    print("max degree", max(degree), "dist", dist)
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
