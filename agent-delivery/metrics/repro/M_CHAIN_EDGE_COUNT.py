#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_EDGE_COUNT 产业链边数（链位关系数）

纯快照复算，不连库：
  code/_snapshots21/chain_tree_links_20261022.json  (dwd_industry_chain_info 全量 1,273 行窄投影)
  code/_snapshots21/probe_chain_meta_20261022.json  (当日列结构/批次日戳探针)

产出：code/M_CHAIN_EDGE_COUNT_out.json
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_CHAIN_EDGE_COUNT_out.json"

TREE = json.loads((SNAP / "chain_tree_links_20261022.json").read_text(encoding="utf-8"))
META = json.loads((SNAP / "probe_chain_meta_20261022.json").read_text(encoding="utf-8"))
ROWS = TREE["data"]

# ---------- 结构 ----------
CHAIN_NAME = {
    "INB1204": "机器人", "INB1209": "智能网联汽车", "INB1236": "低空经济",
    "INB1303": "集成电路", "INB1306": "软件与信息服务", "INB1309": "人工智能",
    "INB1323": "传感器", "INB1333": "智能终端", "INB1354": "具身智能",
    "INB1502": "数字创意", "INB2503": "生物医药", "INB2505": "合成生物",
}
CODES = [r["industry_code"] for r in ROWS]
CODE_SET = set(CODES)
NAME = {r["industry_code"]: r["industry_name"] for r in ROWS}
PARENT_CODE = {r["industry_code"]: (r.get("industry_link_code") or "") for r in ROWS}
PARENT_NAME = {r["industry_code"]: (r.get("parent_code") or "") for r in ROWS}

ROOTS = [c for c in CODES if len(c) == 7]
EDGES = [(PARENT_CODE[c], c) for c in CODES if len(c) > 7]
CHILDREN = defaultdict(list)
for p, c in EDGES:
    CHILDREN[p].append(c)
LEAVES = [c for c in CODES if c not in CHILDREN]
CONTAINERS = [c for c in CODES if c in CHILDREN]

DEPTH = {c: (len(c) - 7) // 2 for c in CODES}


def chain_of(code: str) -> str:
    return code[:7]


# ---------- 完整性 ----------
self_loops = sum(1 for p, c in EDGES if p == c)
dup_codes = len(CODES) - len(CODE_SET)
orphan = sum(1 for p, c in EDGES if p not in CODE_SET)
# 每个非根节点是否恰好一个父（industry_link_code 是父指针）
parents = defaultdict(set)
for p, c in EDGES:
    parents[c].add(p)
multi_parent = sum(1 for c, ps in parents.items() if len(ps) > 1)
# 父名与父码是否指向同一节点（parent_code 存的是名称，不是编码）
name_mismatch = 0
for c in CODES:
    if len(c) <= 7:
        continue
    p = PARENT_CODE[c]
    if p in CODE_SET and PARENT_NAME[c] != NAME[p]:
        name_mismatch += 1
# 编码链式规则：子码前 len(父码) 位 == 父码
prefix_violation = sum(1 for p, c in EDGES if not c.startswith(p))
# 深度跳级：子深度 = 父深度 + 1
depth_violation = sum(1 for p, c in EDGES if DEPTH[c] != DEPTH[p] + 1)

# ---------- 分布 ----------
depth_rows = []
for d in sorted({DEPTH[c] for c in CODES}):
    ns = [c for c in CODES if DEPTH[c] == d]
    es = [(p, c) for p, c in EDGES if DEPTH[c] == d]
    lv = [c for c in ns if c in CHILDREN]
    depth_rows.append({
        "depth": d, "nodes": len(ns), "edges": len(es),
        "containers": len(lv), "leaves": len(ns) - len(lv),
    })

per_chain = []
for ch in sorted(CHAIN_NAME):
    ns = [c for c in CODES if chain_of(c) == ch]
    es = [(p, c) for p, c in EDGES if chain_of(c) == ch]
    lv = [c for c in ns if c in CHILDREN]
    per_chain.append({
        "chain_code": ch, "chain_name": CHAIN_NAME[ch],
        "nodes": len(ns), "edges": len(es),
        "containers": len(lv), "leaves": len(ns) - len(lv),
        "l1_nodes": len([c for c in ns if len(c) == 9]),
        "max_depth": max(DEPTH[c] for c in ns),
    })

# ---------- 口径对照 ----------
distinct_link_codes = len({PARENT_CODE[c] for c in CODES if len(c) > 7})
# parent_code 列实际存的是链名（12 个取值），不是父节点名
distinct_parent_code_values = len({PARENT_NAME[c] for c in CODES})
# 全表按 (parent_code, industry_link_code) 去重 = 319 个非根父码 + 12 个根节点空父码哨兵
distinct_pairs_all = len({(PARENT_NAME[c], PARENT_CODE[c]) for c in CODES})
dup_names = len(CODES) - len({NAME[c] for c in CODES})
leaf_names = len({NAME[c] for c in LEAVES})

edge_types = [
    {
        "edge_type": "parent_child",
        "label_zh": "父子归属边",
        "source": "gkx.dwd_industry_chain_info.industry_link_code（父指针）+ industry_code（子码）",
        "rows": len(EDGES),
        "status": "有源可数",
        "evidence": "1,273 行中 1,261 行带父码；12 个 7 位根节点父码为空",
    },
    {
        "edge_type": "belongs_to",
        "label_zh": "归属边",
        "source": "NebulaGraph gkx_chain（本环境不可访问）",
        "rows": 0,
        "status": "无源",
        "evidence": "gkx 库 SHOW TABLES LIKE '%chain%' 仅返回 dwd_industry_chain_info / dwd_industry_chain_news_info，无图空间表",
    },
    {
        "edge_type": "participates",
        "label_zh": "参与边",
        "source": "NebulaGraph gkx_chain（本环境不可访问）",
        "rows": 0,
        "status": "无源",
        "evidence": "同上；企业-环节关系仅在 dwd_org_industry_tags 的打标行，不是图谱边",
    },
    {
        "edge_type": "supplies",
        "label_zh": "供应边",
        "source": "无",
        "rows": 0,
        "status": "无源",
        "evidence": "源表无上下游对手方字段；不能用专利共现/同名企业自造供应关系",
    },
    {
        "edge_type": "depends_on",
        "label_zh": "依赖边",
        "source": "无",
        "rows": 0,
        "status": "无源",
        "evidence": "源表无依赖声明字段；专利引用是知识流，不是产业链依赖边",
    },
]

payload = {
    "metric_id": "M_CHAIN_EDGE_COUNT",
    "metric_name": "产业链边数（链位关系数）",
    "formula_owner": "AI 补漏调研（2026-08-21 初版；本件 2026-10-22 复算）",
    "support_judgment": "部分支持",
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "截面指标，无年度基期；快照日期 2026-10-22，源表无时间分区可用",
    "value": len(EDGES),
    "unit": "条",
    "scope": "gkx.dwd_industry_chain_info 全量 1,273 个环节节点、12 条产业链",
    "headline": {
        "node_count": len(CODES),
        "edge_count": len(EDGES),
        "leaf_count": len(LEAVES),
        "container_count": len(CONTAINERS),
        "root_count": len(ROOTS),
        "max_depth": max(DEPTH.values()),
        "leaf_share_pct": round(100.0 * len(LEAVES) / len(CODES), 2),
        "distinct_node_names": len({NAME[c] for c in CODES}),
        "duplicate_name_nodes": dup_names,
        "distinct_leaf_names": leaf_names,
    },
    "per_chain": per_chain,
    "depth_distribution": depth_rows,
    "edge_types": edge_types,
    "caliber_compare": {
        "primary_tree_edges": len(EDGES),
        "naive_pair_count_331": distinct_pairs_all,
        "distinct_parent_codes": distinct_link_codes,
        "distinct_parent_code_values": distinct_parent_code_values,
        "why_331_is_wrong": (
            f"全表按 (parent_code, industry_link_code) 去重得 {distinct_pairs_all}："
            f"{distinct_link_codes} 个真实父码 + 12 个根节点（industry_link_code 为空串）各算一对；"
            f"另外 parent_code 列存的不是父节点名而是链名（仅 {distinct_parent_code_values} 个取值），"
            "按它去重既漏父又造哨兵对，不能当边数"
        ),
        "legacy_ads_claim_832": {
            "rows": 832,
            "source": "calc-logic/CHAIN/M_CHAIN_EDGE_COUNT.md 引用的演示库 ADS 表 chain_panorama_edges",
            "usable": False,
            "note": "该表不在 gkx；演示库口径与源表 1,261 不一致，且无法复算，本件不采",
        },
    },
    "integrity": {
        "duplicate_industry_codes": dup_codes,
        "self_loops": self_loops,
        "orphan_edges": orphan,
        "multi_parent_nodes": multi_parent,
        "parent_name_mismatch": name_mismatch,
        "prefix_rule_violations": prefix_violation,
        "depth_rule_violations": depth_violation,
    },
    "related_tables": {"dwd_industry_chain_news_info": 108052},
    "sources": [
        "code/_snapshots21/chain_tree_links_20261022.json",
        "code/_snapshots21/probe_chain_meta_20261022.json",
    ],
    "notes": [
        "industry_link_code 是父指针（319 个不同取值 = 319 个容器节点），不是链编码；链归属只能取 industry_code 前 7 位",
        "parent_code 列存的是链名（12 个取值），不是父节点名；1,220 个非根行的 parent_code 与其父节点名称不一致，故该列不可用于还原父子关系",
        "父子边之外的四类关系边（belongs_to/participates/supplies/depends_on）在 gkx 无源表，不能以专利共现替代",
        "1,261 = 1,273 - 12 个根节点；954 + 319 = 1,273；954 - 12 = 942 ≠ 1,261，故边数不可由叶子数反推",
    ],
}

OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print("wrote", OUT)
print("edges", len(EDGES), "nodes", len(CODES), "leaves", len(LEAVES), "containers", len(CONTAINERS))
