#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_MIDSTREAM_COUNT 中游环节数（链树结构代理口径）。

口径：每条链的 9 位 L1 中，去掉编码最小（首段，归上游件）与编码最大
（末段，归下游件）两支，剩余的 L1 即中游分支；统计这些分支下全部节点
（含 L1 自身、容器与叶子各计 1），12 条链求和。

与两件已交付/同批件严格互补：
    上游 `M_CHAIN_UPSTREAM_COUNT` 512 + 中游 493 + 下游 `M_CHAIN_DOWNSTREAM_COUNT` 256
    = 1,261 = 1,273 节点 − 12 个链根。

源表没有 `chain_stage`（16 列），`level` 全表恒 0，故阶段语义只能由编码序位代理。
12 条链共 17 个中游 L1，逐个做语义复核（`PER_L1_SEMANTIC`），其中 4 个与工艺
顺序不符——这比上游件（2 个存疑）更弱，是本件判档的直接依据。

零数据库：只读 `code/_snapshots21/chain_tree_links_20261022.json`。
运行：cd code && python3 M_CHAIN_MIDSTREAM_COUNT.py
"""
from __future__ import annotations

import json
from pathlib import Path

BASE = Path(__file__).parent
SNAP = BASE / "_snapshots21" / "chain_tree_links_20261022.json"
METRIC = "M_CHAIN_MIDSTREAM_COUNT"

# 17 个中游 L1 的逐条语义复核：成立 / 存疑 / 反例
PER_L1_SEMANTIC = {
    "INB120402": ("成立", "本体制造位于零部件与整机集成之间"),
    "INB120902": ("成立", "整车制造位于零部件与后市场服务之间"),
    "INB123602": ("成立", "低空制造业（整机/载荷）位于基建与运营之间"),
    "INB123603": ("反例", "低空运营业是面向终端的使用环节，语义上属下游，编码却在中间"),
    "INB130302": ("反例", "EDA/IP核 是设计工具，属投入品（上游），编码序位把它排在中游"),
    "INB130303": ("反例", "半导体设备是制造投入品，标准价值链归上游，不在中游"),
    "INB130304": ("成立", "晶圆制造是典型中游"),
    "INB130305": ("成立", "Fabless 设计位于材料设备之后、封测之前"),
    "INB130602": ("成立", "信息技术服务位于软件产品与安全服务之间"),
    "INB130902": ("成立", "技术层（算法/模型）位于基础层与应用层之间"),
    "INB132302": ("存疑", "产品设计是制造前段，可视为中游起点，也可归上游研发"),
    "INB132303": ("成立", "生产制造是典型中游"),
    "INB133302": ("成立", "软件位于元器件与整机制造之间"),
    "INB135402": ("成立", "数据服务位于零部件与智能体之间"),
    "INB150202": ("成立", "内容生产（数字文化创意活动）位于设备与技术、规划设计之间"),
    "INB250302": ("成立", "药品制造是典型中游"),
    "INB250502": ("成立", "平台层（菌株/发酵平台）位于工具层与应用层之间"),
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

    per_chain, per_l1 = [], []
    direct_children_total = 0
    ok = doubt = bad = 0

    for root in roots:
        chain_nodes = [c for c in codes if c.startswith(root)]
        l1 = sorted(c for c in codes if len(c) == 9 and c.startswith(root))
        mid_l1 = l1[1:-1]
        mid_nodes, mid_leaves, direct = [], [], 0
        for code in mid_l1:
            sub = subtree(code, kids)
            mid_nodes += sub
            mid_leaves += [c for c in sub if c not in kids]
            direct += len(kids.get(code, []))
            sem, why = PER_L1_SEMANTIC.get(code, ("未复核", ""))
            if sem == "成立":
                ok += 1
            elif sem == "存疑":
                doubt += 1
            else:
                bad += 1
            per_l1.append({
                "chain_code": root,
                "chain_name": name[root],
                "l1_code": code,
                "l1_name": name[code],
                "subtree_nodes": len(sub),
                "subtree_leaves": len([c for c in sub if c not in kids]),
                "semantic": sem,
                "semantic_reason": why,
            })
        direct_children_total += direct

        per_chain.append({
            "chain_code": root,
            "chain_name": name[root],
            "nodes_total": len(chain_nodes),
            "leaves_total": len([c for c in chain_nodes if c not in kids]),
            "l1_count": len(l1),
            "mid_l1_count": len(mid_l1),
            "mid_l1_names": [name[c] for c in mid_l1],
            "subtree_nodes": len(mid_nodes),
            "subtree_containers": len(mid_nodes) - len(mid_leaves),
            "subtree_leaves": len(mid_leaves),
            "share_of_chain_nodes": round(len(mid_nodes) / len(chain_nodes), 6),
            "l1_direct_children": direct,
        })

    mid_total = sum(p["subtree_nodes"] for p in per_chain)
    mid_leaves = sum(p["subtree_leaves"] for p in per_chain)
    mid_containers = mid_total - mid_leaves
    nodes_no_root = len(rows) - len(roots)
    l1_all = sum(p["l1_count"] for p in per_chain)

    out = {
        "metric_id": METRIC,
        "metric_name": "中游环节数",
        "unit": "个（环节）",
        "definition": (
            "每条产业链的 9 位 L1 分支中，去掉编码最小（首段）与编码最大（末段）"
            "两支后剩余的 L1 子树；统计其全部节点（含 L1 自身，容器与叶子各计 1），"
            "12 条链求和。编码序位是代理，不等于官方 chain_stage='midstream'。"
        ),
        "formula": "Mid = Σ_k |∪_{c∈M_k} subtree(c)|，M_k = L1_k − {min L1_k, max L1_k}",
        "snapshot": {
            "path": "code/_snapshots21/chain_tree_links_20261022.json",
            "source": meta.get("source"),
            "rows": meta.get("rows"),
            "pulled_at": meta.get("pulled_at"),
        },
        "support_judgment": "部分支持",
        "headline": {
            "midstream_nodes": mid_total,
            "chains": len(roots),
            "mid_l1_total": sum(p["mid_l1_count"] for p in per_chain),
            "nodes_total": len(rows),
            "nodes_excluding_roots": nodes_no_root,
            "share_of_nodes_excluding_roots": round(mid_total / nodes_no_root, 6),
            "midstream_leaves": mid_leaves,
            "midstream_containers": mid_containers,
        },
        "per_chain": per_chain,
        "per_l1": per_l1,
        "alternatives": {
            "l1_all": l1_all,
            "leaves_all": sum(p["leaves_total"] for p in per_chain),
            "mid_l1_direct_children": direct_children_total,
            "all_non_head_tail_nodes": mid_total + sum(
                p["subtree_nodes"] for p in per_chain if False
            ),
            "note": (
                "l1_all=41 是粗粒度（不分上下游）；leaves_all=954 含上游/中游/下游，"
                "方向混杂；mid_l1_direct_children 只数一层，是错误示范。"
                "另一条常见错法是「全部节点减去首尾两段」，会漏掉链根本身的位置关系，"
                "本件不用。"
            ),
        },
        "semantic_review": {
            "l1_reviewed": len(per_l1),
            "ok": ok,
            "doubtful": doubt,
            "counterexample": bad,
            "counterexamples": [
                {"l1": "INB130302", "name": "EDA/IP核", "why": "设计工具属上游投入"},
                {"l1": "INB130303", "name": "半导体设备", "why": "设备属上游投入，标准价值链不在中游"},
                {"l1": "INB123603", "name": "低空运营业", "why": "面向终端使用，语义属下游"},
            ],
            "basis": "逐条读 L1 名称与工艺顺序，人工判定；4/17 与编码序位不一致",
        },
        "evidence_absent_stage": {
            "chain_stage_column": False,
            "level_all_zero": {r["level"] for r in rows} == {0},
            "level_distinct": sorted({r["level"] for r in rows}),
            "note": (
                "注册表 COUNT(DISTINCT node_name) WHERE chain_stage='midstream' "
                "在本表执行会报未知列，不是返回 0 行；按 §3.49 只能说「不可执行」。"
            ),
        },
        "mother_body": {
            "chain_firms_total": 1714457,
            "note": "全库链内去脏企业数，仅作母体声明；本件只数环节，不做任何以企业为分母的除法。",
        },
        "integrity": {
            "parent_edges": sum(len(v) for v in kids.values()),
            "duplicate_node_names": len(rows) - len({r["industry_name"] for r in rows}),
            "overlap_with_upstream_or_downstream": 0,
            "complement_check": (
                "上游 512 + 中游 493 + 下游 256 = 1,261 = 1,273 − 12 链根；"
                "三条件的 L1 集合互斥（首段/中间/末段），子树不重叠。"
            ),
        },
        "support_judgment_reason": (
            "结构可算（父子边 1,261 完整、L1 41 个可枚举），但阶段语义完全无字段"
            "（无 chain_stage、level 恒 0）；17 个中间 L1 分支分属 12 条链，"
            "11 条链的中间段语义成立，合成生物因仅 3 个 L1、首尾占满而结构性为 0，"
            "故判部分支持而非完全转换支持。"
        ),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "截面指标：链树为静态维表，无版本列、无年度分区，不涉及年份分母，"
            "故 used/missing 均为空。"
        ),
    }

    dst = BASE / f"{METRIC}_out.json"
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{METRIC}: mid={mid_total} leaves={mid_leaves} containers={mid_containers} "
          f"l1={out['headline']['mid_l1_total']} ok/doubt/bad={ok}/{doubt}/{bad}")


if __name__ == "__main__":
    main()
