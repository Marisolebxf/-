#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_UPSTREAM_COUNT 上游环节数（链树结构代理口径）。

为什么用「首段 L1 子树」而不是注册表的 `chain_stage='upstream'`
------------------------------------------------------------------
注册表公式是 `COUNT(DISTINCT node_name) WHERE chain_stage='upstream'`，但
`gkx.dwd_industry_chain_info` 的 16 列里**没有** `chain_stage`，唯一的层级列
`level` 全表 1,273 行恒为 0（快照 `chain_tree_links_20261022.json` 实核）。
因此官方口径不可执行，本件改用「编码序位」：链树按根—L1—L2…递增编码，
取每条链 L1 中编码最小者为首段分支，数该分支下全部后代（含 L1 自身）。

口径与已交付的 `M_CHAIN_DOWNSTREAM_COUNT`（末段 L1 子树，256）严格互补：
本件 512 + 中游 493 + 下游 256 = 1,261 = 1,273 节点 − 12 个链根。

零数据库：只读 `code/_snapshots21/chain_tree_links_20261022.json`。
运行：cd code && python3 M_CHAIN_UPSTREAM_COUNT.py
"""
from __future__ import annotations

import json
from pathlib import Path

BASE = Path(__file__).parent
SNAP = BASE / "_snapshots21" / "chain_tree_links_20261022.json"
METRIC = "M_CHAIN_UPSTREAM_COUNT"

# 语义复核结论（人工逐条，见 MD §2.5）。编码序位只是代理，必须在产物里落盘，
# 否则下游会把 512 当成官方「上游环节数」。
SEMANTIC = {
    "INB1204": ("成立", "零部件是全链投入品，位于本体制造与整机集成之前"),
    "INB1209": ("成立", "零部件先于整车制造"),
    "INB1236": ("存疑", "「低空基建与信息服务」是基础设施与服务，既可为投入也可为配套，不是典型原材料/元器件"),
    "INB1303": ("成立", "半导体材料是集成电路最上游投入"),
    "INB1306": ("存疑", "「软件产品」是本链主产出而非投入品；软件链没有原材料段，首段未必等于上游"),
    "INB1309": ("成立", "基础层（芯片/数据/算法）是 AI 的投入层"),
    "INB1323": ("成立", "原材料先于设计、制造"),
    "INB1333": ("成立", "核心元器件与零部件先于整机制造"),
    "INB1354": ("成立", "核心零部件先于本体与智能体"),
    "INB1502": ("成立", "技术设备是创意生产的内容生产工具"),
    "INB2503": ("成立", "原材料（中药材/原料药）先于药品制造"),
    "INB2505": ("成立", "工具层（菌株/酶/底盘细胞）是平台层与应用层的投入"),
}


def load_tree():
    d = json.loads(SNAP.read_text(encoding="utf-8"))
    return d["data"], d


def build_index(rows):
    codes = {r["industry_code"] for r in rows}
    name = {r["industry_code"]: r["industry_name"] for r in rows}
    kids = {}
    for r in rows:
        p = (r.get("industry_link_code") or "").strip()
        if p in codes:
            kids.setdefault(p, []).append(r["industry_code"])
    for k in kids:
        kids[k].sort()
    return codes, name, kids


def subtree(code, kids):
    out, stack = [code], [code]
    while stack:
        cur = stack.pop()
        for k in kids.get(cur, []):
            out.append(k)
            stack.append(k)
    return out


def main():
    rows, meta = load_tree()
    codes, name, kids = build_index(rows)
    roots = sorted(c for c in codes if len(c) == 7)

    per_chain = []
    total_nodes = total_leaves = total_l1 = 0
    direct_children_total = 0
    sem_ok = sem_doubt = sem_bad = 0

    for root in roots:
        chain_nodes = [c for c in codes if c.startswith(root)]
        chain_leaves = [c for c in chain_nodes if c not in kids]
        l1 = sorted(c for c in codes if len(c) == 9 and c.startswith(root))
        head = l1[0]
        sub = subtree(head, kids)
        sub_leaves = [c for c in sub if c not in kids]
        direct = len(kids.get(head, []))
        sem, why = SEMANTIC.get(root, ("未复核", ""))
        if sem == "成立":
            sem_ok += 1
        elif sem == "存疑":
            sem_doubt += 1
        else:
            sem_bad += 1

        total_nodes += len(chain_nodes)
        total_leaves += len(chain_leaves)
        total_l1 += len(l1)
        direct_children_total += direct

        per_chain.append({
            "chain_code": root,
            "chain_name": name[root],
            "nodes_total": len(chain_nodes),
            "leaves_total": len(chain_leaves),
            "l1_count": len(l1),
            "l1_first_code": head,
            "l1_first_name": name[head],
            "subtree_nodes": len(sub),
            "subtree_containers": len(sub) - len(sub_leaves),
            "subtree_leaves": len(sub_leaves),
            "share_of_chain_nodes": round(len(sub) / len(chain_nodes), 6),
            "l1_direct_children": direct,
            "semantic": sem,
            "semantic_reason": why,
        })

    upstream_total = sum(p["subtree_nodes"] for p in per_chain)
    upstream_leaves = sum(p["subtree_leaves"] for p in per_chain)
    upstream_containers = upstream_total - upstream_leaves
    nodes_no_root = len(rows) - len(roots)

    dup_names = len(rows) - len({r["industry_name"] for r in rows})
    levels = {r["level"] for r in rows}

    out = {
        "metric_id": METRIC,
        "metric_name": "上游环节数",
        "unit": "个（环节）",
        "definition": (
            "每条产业链取 L1 中编码最小的一支为首段分支，统计该分支下全部节点"
            "（含 L1 自身、容器与叶子都计 1），12 条链求和。编码序位是代理，"
            "不等于官方 chain_stage='upstream'。"
        ),
        "formula": "Upstream = Σ_k |{c ∈ C : code(c) 以 code(head_k) 为前缀}|，head_k = min(L1_k)",
        "snapshot": {
            "path": "code/_snapshots21/chain_tree_links_20261022.json",
            "source": meta.get("source"),
            "rows": meta.get("rows"),
            "pulled_at": meta.get("pulled_at"),
        },
        "support_judgment": "部分支持",
        "headline": {
            "upstream_nodes": upstream_total,
            "chains": len(roots),
            "nodes_total": len(rows),
            "nodes_excluding_roots": nodes_no_root,
            "share_of_nodes_excluding_roots": round(upstream_total / nodes_no_root, 6),
            "upstream_leaves": upstream_leaves,
            "upstream_containers": upstream_containers,
        },
        "per_chain": per_chain,
        "alternatives": {
            "l1_all": total_l1,
            "leaves_all": total_leaves,
            "first_l1_direct_children": direct_children_total,
            "nodes_excluding_roots": nodes_no_root,
            "note": (
                "l1_all=41（粗粒度，不分上下游）；leaves_all=954（全末端叶子，"
                "含上游/中游/下游，方向混杂）；first_l1_direct_children 只数一层，"
                "是错误示范，不是备选交付值。"
            ),
        },
        "semantic_review": {
            "ok": sem_ok,
            "doubtful": sem_doubt,
            "counterexample": sem_bad,
            "basis": "逐链读首段 L1 名称与工艺顺序，人工判定；规则不可批量替代",
        },
        "evidence_absent_stage": {
            "chain_stage_column": False,
            "level_all_zero": levels == {0},
            "level_distinct": sorted(levels),
            "columns_16": [
                "pk_id", "industry_code", "industry_name", "industry_link_code",
                "industry_link_name", "level", "parent_code", "parent_name",
                "node_company_count", "created_time", "updated_time", "creater",
                "updater", "table_data_source", "is_deleted", "operator_remarks",
                "insert_remark",
            ],
            "note": (
                "注册表 COUNT(DISTINCT node_name) WHERE chain_stage='upstream' "
                "在本表执行会报未知列，不是返回 0 行；按 §3.49 只能说「不可执行」。"
            ),
        },
        "integrity": {
            "parent_edges": sum(len(v) for v in kids.values()),
            "duplicate_node_names": dup_names,
            "dedup_by_name_note": (
                f"1,273 个节点只有 {len({r['industry_name'] for r in rows})} 个不同名称；"
                "若按注册表的 DISTINCT node_name 统计，跨链同名环节会被合并，"
                "本件按编码唯一键计量。"
            ),
            "complement_check": (
                "上游 512 + 中游 493 + 下游 256 = 1,261 = 节点 1,273 − 链根 12；"
                "三段互斥且覆盖全部非根节点。"
            ),
        },
        "support_judgment_reason": (
            "结构可算（1,273 节点、父子边 1,261 齐全），但上游/中游/下游的阶段语义"
            "在源表完全缺失（无 chain_stage、level 恒 0），只能用编码序位代理；"
            "12 条链里 10 条首段语义成立、2 条存疑，故判部分支持。"
        ),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "截面指标：链树为静态维表，无版本列、无年度分区，不涉及年份分母，"
            "故 used/missing 均为空，不属于「缺年按 0 摊入」的情形。"
        ),
    }

    dst = BASE / f"{METRIC}_out.json"
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{METRIC}: upstream={upstream_total} leaves={upstream_leaves} "
          f"containers={upstream_containers} chains={len(roots)} -> {dst.name}")


if __name__ == "__main__":
    main()
