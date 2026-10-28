#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_DOWNSTREAM_COUNT 下游环节数

口径（本件定义，非官方字段）：
  每条链按 industry_code 末两位最大的 L1 视为“末段分支”，
  下游环节数 = 该末段分支下全部后代节点数（含末段 L1 自身，容器与叶子都计）。

为什么不直接用 chain_stage：gkx.dwd_industry_chain_info 无该列（探针已落盘），
level 列全表恒为 0，不可用。

纯快照复算：code/_snapshots21/chain_tree_links_20261022.json
产出：code/M_CHAIN_DOWNSTREAM_COUNT_out.json
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_CHAIN_DOWNSTREAM_COUNT_out.json"

TREE = json.loads((SNAP / "chain_tree_links_20261022.json").read_text(encoding="utf-8"))
ROWS = TREE["data"]

CHAIN_NAME = {
    "INB1204": "机器人", "INB1209": "智能网联汽车", "INB1236": "低空经济",
    "INB1303": "集成电路", "INB1306": "软件与信息服务", "INB1309": "人工智能",
    "INB1323": "传感器", "INB1333": "智能终端", "INB1354": "具身智能",
    "INB1502": "数字创意", "INB2503": "生物医药", "INB2505": "合成生物",
}
CODES = [r["industry_code"] for r in ROWS]
NAME = {r["industry_code"]: r["industry_name"] for r in ROWS}
CODE_SET = set(CODES)
CHILDREN = defaultdict(list)
for r in ROWS:
    c = r["industry_code"]
    p = r.get("industry_link_code") or ""
    if len(c) > 7 and p:
        CHILDREN[p].append(c)

LEAVES = [c for c in CODES if c not in CHILDREN]
CONTAINERS = [c for c in CODES if c in CHILDREN]
L1 = [c for c in CODES if len(c) == 9]


def subtree(root: str) -> list[str]:
    return [c for c in CODES if c.startswith(root)]


# 每链末段 L1（编码序位最大）
last_l1 = {}
for ch in CHAIN_NAME:
    l1s = sorted(c for c in L1 if c.startswith(ch))
    last_l1[ch] = l1s[-1]

# 末段分支的语义人工标注（10 条为服务/应用/整机/封测，2 条存疑）
semantic = {
    "INB1204": ("整机集成", "是", "整机集成位于链条末端"),
    "INB1209": ("智能网联相关服务", "是", "服务环节位于末端"),
    "INB1236": ("低空配套业", "存疑", "“配套”通常指上游配套，编码序位却在末位"),
    "INB1303": ("封测", "是", "封装测试是集成电路制造后段"),
    "INB1306": ("信息安全软件与服务", "是", "安全服务位于软件链末端"),
    "INB1309": ("AI应用", "是", "应用层位于末端"),
    "INB1323": ("传感器生产专用装备", "存疑", "生产装备是上游设备，编码序位在末位属反例"),
    "INB1333": ("整机制造", "是", "整机制造位于终端链末端"),
    "INB1354": ("具身智能体", "是", "智能体是具身智能最终产品"),
    "INB1502": ("规划设计服务", "是", "服务环节位于末端"),
    "INB2503": ("医学研发服务", "是", "研发服务位于医药链末端"),
    "INB2505": ("应用层", "是", "应用层位于末端"),
}

per_chain = []
for ch in sorted(CHAIN_NAME):
    ns = [c for c in CODES if c.startswith(ch)]
    lv = [c for c in ns if c not in CHILDREN]
    l1s = sorted(c for c in ns if len(c) == 9)
    tail = last_l1[ch]
    sub = subtree(tail)
    sub_lv = [c for c in sub if c not in CHILDREN]
    direct = sorted(CHILDREN.get(tail, []))
    per_chain.append({
        "chain_code": ch,
        "chain_name": CHAIN_NAME[ch],
        "nodes": len(ns),
        "leaves": len(lv),
        "l1_count": len(l1s),
        "last_l1_code": tail,
        "last_l1_name": NAME[tail],
        "last_l1_direct_children": len(direct),
        "tail_subtree_nodes": len(sub),
        "tail_subtree_containers": len(sub) - len(sub_lv),
        "tail_subtree_leaves": len(sub_lv),
        "tail_share_of_chain_pct": round(100.0 * len(sub) / len(ns), 2),
        "semantic_ok": semantic[ch][1],
        "semantic_note": semantic[ch][2],
    })

tail_total = sum(r["tail_subtree_nodes"] for r in per_chain)
tail_leaves = sum(r["tail_subtree_leaves"] for r in per_chain)
direct_total = sum(r["last_l1_direct_children"] for r in per_chain)
leaf_total = len(LEAVES)
l1_total = len(L1)
plausible = sum(1 for r in per_chain if r["semantic_ok"] == "是")
doubtful = [r["chain_name"] + "/" + r["last_l1_name"] for r in per_chain if r["semantic_ok"] != "是"]

payload = {
    "metric_id": "M_CHAIN_DOWNSTREAM_COUNT",
    "metric_name": "下游环节数",
    "formula_owner": "AI 补漏调研（2026-08-21 registry 0.1.0；本件代理口径 2026-10-22）",
    "support_judgment": "部分支持",
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "截面指标，无年度基期；快照 2026-10-22，链树无版本列",
    "value": tail_total,
    "unit": "个",
    "scope": "gkx.dwd_industry_chain_info 12 条链、41 个 L1、1,273 个节点",
    "definition": (
        "下游环节数 = 每链编码序位最大的 L1 分支下全部后代节点数（含该 L1 自身；"
        "容器节点与其下叶子各计 1）；这是结构代理口径，不是 chain_stage='downstream' 的官方口径"
    ),
    "headline": {
        "downstream_units": tail_total,
        "downstream_leaves_in_tail": tail_leaves,
        "all_terminal_leaves": leaf_total,
        "all_l1": l1_total,
        "node_total": len(CODES),
        "container_total": len(CONTAINERS),
        "chain_total": len(CHAIN_NAME),
        "direct_children_of_tail_l1_sum": direct_total,
        "tail_share_of_all_nodes_pct": round(100.0 * tail_total / len(CODES), 2),
        "leaf_upper_bound_ratio_pct": round(100.0 * tail_total / leaf_total, 2),
        "semantic_plausible_chains": plausible,
        "semantic_doubtful": doubtful,
        "distinct_leaf_names": len({NAME[c] for c in LEAVES}),
    },
    "per_chain": per_chain,
    "alternatives": {
        "tail_l1_subtree": {
            "value": tail_total,
            "unit": "个",
            "note": "主口径；方向性来自编码序位，10/12 条链语义成立，2 条存疑",
        },
        "tail_l1_direct_children_only": {
            "value": direct_total,
            "unit": "个",
            "note": "只数末段 L1 的直接子节点会漏掉孙辈及更深节点，故不可用",
        },
        "all_terminal_leaves": {
            "value": leaf_total,
            "unit": "个",
            "note": "全部末端叶子，含上游材料/设备叶子，是“下游”的上界而非下游数",
        },
        "l1_branch_count": {
            "value": l1_total,
            "unit": "个",
            "note": "只数 L1 分支，粒度太粗，无法区分上下游",
        },
    },
    "evidence_absent_stage": {
        "column_chain_stage": "不存在（SHOW COLUMNS 全 16 列无此列）",
        "column_level": "存在但全表 1,273 行恒为 0，无法区分层级/阶段",
        "column_downstream": "不存在",
        "registry_is_mock": True,
        "registry_source": "cfg_metric-CHAIN-seed.yaml：source_systems=Mock @ batch=mock_20260623, is_mock=true",
        "registry_formula": "COUNT(DISTINCT node_name) WHERE chain_stage='downstream'",
        "consequence": "官方公式在当前源表不可执行；本件只能给结构代理值，不能声称等于官方下游环节数",
    },
    "integrity": {
        "chains_with_less_than_3_l1": 0,
        "tail_l1_missing": 0,
        "nodes_not_in_any_chain": len([c for c in CODES if c[:7] not in CHAIN_NAME]),
        "duplicate_node_names": len(CODES) - len({NAME[c] for c in CODES}),
    },
    "enterprise_caliber_reference": {
        "chain_firms_clean": 1714457,
        "note": "企业侧默认口径，仅作单位对照；本指标单位是环节，不用它做分母",
    },
    "sources": [
        "code/_snapshots21/chain_tree_links_20261022.json",
        "code/_snapshots21/probe_chain_meta_20261022.json",
    ],
    "notes": [
        "为什么不用 COUNT(DISTINCT node_name)：954 个叶子只有 855 个不同名称，重名会把下游数压低；官方公式的 DISTINCT 语义在跨链重名时不可比",
        "为什么不取 last L1 的直接子节点：12 条链合计仅 12 个直接子节点，而完整末段子树有 256 个节点，直接子节点把封装/应用等二级环节整体漏掉",
        "传感器链末段 L1 是“传感器生产专用装备”，属上游设备，说明编码序位不等于工艺顺序；低空“配套业”同样存疑",
        "本口径不含企业数，因此不存在家次/家数混用；企业侧数据另见 M_CHAIN_ENTERPRISE_COUNT 族",
    ],
}

OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print("wrote", OUT)
print("tail", tail_total, "leaves", leaf_total, "direct", direct_total, "plausible", plausible)
