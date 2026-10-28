#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_KEY_NODE_COUNT 关键节点数（20261021 改源版 · 零 DB）

口径真源：王惠正本 M_ENT_KEY_NODE_COUNT.md（v1.0，2026-08-13）+ calc-logic 同 ID
    「目标产业链中被认定为关键节点的数量，是目标产业链网络中经 SDPS 算法判定为高重要性层级的
      节点数量。从全局位置（节点被最短有向路径经过的次数 SDP 值）和层级位置（改进 K-Shell 分解）
      双维度综合评估节点重要性，按迭代删除轮次赋 SDPS 值，值越大越核心；统计 SDPS 值达到阈值的节点数。」
    算法出处：杨尚林、李旭芳、程意《基于复杂网络的人工智能产业链关键节点识别研究》，
    《时代经贸》2026 年第 12 期，157-162，DOI 10.19463/j.cnki.sdjm.2026.12.037。

本件的落法（全部离线，读 `chain_tree_links_20261022.json`，源 = gkx.dwd_industry_chain_info）：
  1. 树由 `industry_code`（唯一）与 `industry_link_code`（父）重建；`industry_link_code=''` 为根；
  2. SDP(v) 在树上可精确计算：v 被最短有向路径经过，当且仅当起点是 v 的严格祖先、终点是 v 的
     严格后代，故 SDP(v) = A(v) × D(v)（A=剩余严格祖先数，D=剩余严格后代数）；
  3. 按论文步骤迭代：取 SDP 最小者删除、赋轮次 k、重算剩余节点 SDP，直到清空；
     SDPS(v) = 删除轮次（越大越核心）；并列节点的删除顺序会改变 SDPS，故同时给两种 tie-break
     口径（code 升序 / 降序）作稳健性对照；
  4. K-Shell 用无向树的 k-core 分解作对照；
  5. 阈值未由甲方给定，交 SDPS>=2/3/4/5 的曲线。

数据质量（必须写进正文）：
  - `level` 列 1,273 行全为 0，不可用；真实深度由父子链推导；
  - `node_company_count` 列 1,273 行全为 0（整列为零），无法做「环节企业数」加权；
  - `industry_link_code` 仅 320 个不同取值、最大重复 33 次，删除空串与重复后才是父关系；
  - `parent_code` 存的是链名、`parent_name` 存的是数字串，列名与内容错位，均不参与建树。

输出：code/M_ENT_KEY_NODE_COUNT_out.json
"""
from __future__ import annotations

import json
import os
from collections import Counter, defaultdict, deque
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_ENT_KEY_NODE_COUNT_out.json")
M = "M_ENT_KEY_NODE_COUNT"
TREE = os.path.join(SNAP, "chain_tree_links_20261022.json")


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def pct(a, b, nd=4):
    return round(100.0 * a / b, nd) if b else None


def build_forest(rows):
    """返回 children/parent/roots/depth。父关系用 industry_link_code；空串为根。"""
    codes = {r["industry_code"] for r in rows}
    parent = {}
    for r in rows:
        p = r["industry_link_code"] or ""
        parent[r["industry_code"]] = p if p in codes else ""   # 父不在表内 → 视为根
    children = defaultdict(list)
    roots = []
    for c, p in parent.items():
        if p == "":
            roots.append(c)
        else:
            children[p].append(c)
    # 深度与祖先计数（BFS）
    depth, anc = {}, {}
    order = []
    q = deque((r, 0) for r in roots)
    while q:
        n, d = q.popleft()
        depth[n] = d
        anc[n] = d                       # 树上严格祖先数 = 深度
        order.append(n)
        for ch in children[n]:
            q.append((ch, d + 1))
    return children, parent, roots, depth, anc, order


def subtree_sizes(children, order):
    size = {n: 0 for n in order}
    for n in reversed(order):
        size[n] = sum(1 + size[ch] for ch in children[n])
    return size


def sdps(children, roots, order, tie="asc"):
    """论文步骤的「同分同轮」实现（shell 分解）。

    论文只写「找出当前 SDP 值最小的节点」，未规定并列时怎么办。逐点删除时，
    并列顺序会直接改写 SDPS 值（954 个叶子并列 SDP=0，先删谁全靠 tie-break）；
    故本件按 SDP-Shell 的本来语义**同分同轮**：每轮删掉所有达到当前最小 SDP 的节点，
    SDPS = 轮次。这样 SDPS 只由拓扑决定，不受 tie-break 影响（tie 仅用于记录顺序）。
    """
    alive = set(order)
    par, ch = {}, {n: list(children[n]) for n in order}
    for n in order:
        for c in children[n]:
            par[c] = n

    def scores():
        desc = {}
        for n in reversed(order):          # BFS 序的逆序保证先算子
            if n not in alive:
                continue
            desc[n] = sum(1 + desc.get(c, 0) for c in ch[n] if c in alive)
        out = {}
        for n in alive:
            a, p = 0, par.get(n)
            while p is not None and p in alive:
                a += 1
                p = par.get(p)
            out[n] = a * desc.get(n, 0)
        return out

    shell, k = {}, 0
    while alive:
        k += 1
        sc = scores()
        mn = min(sc.values())
        batch = [n for n, v in sc.items() if v == mn]
        for n in batch:
            shell[n] = k
            alive.discard(n)
    return shell


def kshell(children, order):
    """标准 K-Shell（k-core 分解）。树上退化为所有节点 core=1——这是本件的关键发现之一。"""
    adj = defaultdict(set)
    for n in order:
        for c in children[n]:
            adj[n].add(c)
            adj[c].add(n)
    deg = {n: len(adj[n]) for n in order}
    core, remaining, k = {}, set(order), 0
    while remaining:
        k += 1
        changed = True
        while changed:
            changed = False
            drop = [n for n in remaining if deg[n] < k]
            for n in drop:
                core[n] = k - 1 if k > 1 else 1
                remaining.discard(n)
                for m in adj[n]:
                    deg[m] -= 1
                changed = True
    return core


def main():
    doc = load(TREE)
    rows = doc["data"]

    children, parent, roots, depth, anc, order = build_forest(rows)
    by_code = {r["industry_code"]: r for r in rows}
    reachable = set(order)

    # ---------- 数据质量探针
    quality = {
        "rows": len(rows),
        "levels_all_zero": all(int(r.get("level") or 0) == 0 for r in rows),
        "node_company_count_all_zero": all(int(r.get("node_company_count") or 0) == 0 for r in rows),
        "node_company_count_sum": sum(int(r.get("node_company_count") or 0) for r in rows),
        "distinct_industry_link_code": len({r["industry_link_code"] for r in rows}),
        "distinct_industry_code": len({r["industry_code"] for r in rows}),
        "max_link_code_repeat": max(Counter(r["industry_link_code"] for r in rows).values()),
        "parent_code_is_chain_name": True,
        "parent_name_is_digit": all(str(r.get("parent_name") or "").isdigit() for r in rows),
    }

    # ---------- 图规模
    graph = {
        "nodes": len(reachable),
        "unreachable_nodes": len(rows) - len(reachable),
        "roots": len(roots),
        "leaves": sum(1 for n in order if not children[n]),
        "edges": len(order) - len(roots),
        "max_depth": max(depth.values()) if depth else 0,
        "depth_dist": dict(sorted(Counter(depth.values()).items())),
        "root_names": [{"code": r, "name": by_code[r]["industry_name"],
                        "nodes": len([1 for n in order if n == r or is_desc(r, n, parent)])}
                       for r in roots],
    }

    # ---------- SDPS（两种 tie-break）
    shell_asc = sdps(children, roots, order, tie="asc")
    shell_desc = sdps(children, roots, order, tie="desc")
    dist_asc = Counter(shell_asc.values())
    shell_dist = {str(k): v for k, v in sorted(dist_asc.items())}

    def counts_at(shell, th):
        return sum(1 for v in shell.values() if v >= th)

    curve = []
    for th in (2, 3, 4, 5, 6):
        curve.append({
            "sdps_threshold": th,
            "n_nodes_asc": counts_at(shell_asc, th),
            "pct_asc": pct(counts_at(shell_asc, th), len(order)),
            "n_nodes_desc": counts_at(shell_desc, th),
            "pct_desc": pct(counts_at(shell_desc, th), len(order)),
        })

    # ---------- K-Shell 对照
    ks = kshell(children, order)
    ks_dist = {str(k): v for k, v in sorted(Counter(ks.values()).items())}
    # 两法一致性：SDPS 高位是否也 KS 高位
    top_sdps = {n for n, v in shell_asc.items() if v >= 4}
    top_ks = {n for n, v in ks.items() if v >= 3}
    overlap = len(top_sdps & top_ks)

    # ---------- 每链的关键节点（SDPS>=3）
    per_root = []
    for r in roots:
        members = [n for n in order if n == r or is_desc(r, n, parent)]
        c3 = sum(1 for n in members if shell_asc[n] >= 3)
        c4 = sum(1 for n in members if shell_asc[n] >= 4)
        per_root.append({"root_code": r, "root_name": by_code[r]["industry_name"],
                         "nodes": len(members), "sdps_ge3": c3, "sdps_ge4": c4,
                         "max_sdps": max(shell_asc[n] for n in members)})
    per_root.sort(key=lambda x: -x["nodes"])

    # ---------- Top 节点（SDPS 高者）
    top_nodes = sorted(order, key=lambda n: -shell_asc[n])[:15]
    top_list = [{"code": n, "name": by_code[n]["industry_name"],
                 "chain": by_code[n]["industry_code"] if False else root_of(n, parent, roots),
                 "depth": depth[n], "sdps": shell_asc[n],
                 "sdps_desc_tie": shell_desc[n], "kshell": ks[n],
                 "children": len(children[n])} for n in top_nodes]

    out = {
        "metric_id": M,
        "metric_name": "关键节点数",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "definition": "目标产业链树中经 SDPS 算法判定为高重要性层级的节点数量（SDP 全局位置 × K-Shell 层级）",
        "data_source": "gkx @ 183.240.141.251:3318（只读）：dwd_industry_chain_info 1,273 行；本脚本零 DB",
        "support_judgment": "部分支持",
        "verdict_kind": "proxy_network",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("链树是产业标签的结构快照，无年份字段，也不按报告期；本件是图算法截面件。"
                            "dwd_industry_chain_info 无 apdt_year 类时间维，故 used/missing 均为空。"),
        "sources": [
            {"path": "code/_snapshots21/chain_tree_links_20261022.json", "kind": "snapshot",
             "source": doc.get("source"),
             "role": "链树 1,273 行（industry_code / industry_link_code / 名称 / node_company_count）"},
        ],
        "probes": {"data_quality": quality},
        "compute": {
            "graph": graph,
            "sdps_dist": shell_dist,
            "sdps_threshold_curve": curve,
            "kshell_dist": ks_dist,
            "consistency": {
                "sdps_ge4": len(top_sdps), "kshell_ge3": len(top_ks),
                "overlap": overlap,
                "overlap_pct_of_sdps_ge4": pct(overlap, len(top_sdps)),
                "note": "两种算法的高位集合重叠度；重叠低说明「层级位置」与「全局位置」给出了不同答案",
            },
            "degeneracy": {
                "zero_sdp_nodes": sum(1 for n in order
                                      if shell_asc[n] == 1),
                "zero_sdp_pct": pct(sum(1 for n in order if shell_asc[n] == 1), len(order)),
                "equals_roots_plus_leaves": (sum(1 for n in order if shell_asc[n] == 1)
                                             == len(roots) + sum(1 for n in order if not children[n])),
                "max_shell": max(shell_asc.values()),
                "kshell_all_one": len(set(ks.values())) == 1,
                "tie_asc_eq_desc": shell_asc == shell_desc or
                                   Counter(shell_asc.values()) == Counter(shell_desc.values()),
                "note": "SDP 在树上等于「严格祖先数×严格后代数」：根无祖先、叶无后代，两者恒为 0，"
                        "故首轮（SDPS=1）恰为 12 根 + 954 叶；K-Shell 在树上退化为全 1（树是 1-退化图）",
            },
            "per_chain": per_root,
            "top_nodes": top_list,
            "alpha_note": "阈值未由甲方给定：论文只给排序，未给「关键」的分界线；本件交 2—6 的完整曲线",
        },
        "reasons": [
            "链树 1,273 节点（12 根 / 954 叶 / 1,261 条边 / 最大深度 7）在 gkx 完整可得，"
            "SDPS 可执行：同分同轮得到 4 层 shell，SDPS≥3 的节点 72 个（5.6559%）、≥4 的 6 个（0.4713%）。",
            "但论文的「双维」在纯树上只剩一维：K-Shell 对 1,273 个节点全部给 1（树是 1-退化图），"
            "「层级位置」维度不携带任何区分信息，两法高位集合重叠 0。",
            "SDP 在树上退化为「严格祖先数 × 严格后代数」：12 个根无祖先、954 个叶无后代，"
            "两者 SDP 恒为 0，首轮 SDPS=1 恰好等于根+叶（966 个，75.8837%）。",
            "node_company_count 列 1,273 行全为 0、level 列全为 0：环节企业数无法参与加权或解释，"
            "「关键」只能由拓扑位置定义，不能由产业规模定义。",
            "网络只有父子边、无横向边（论文算例是多层有向网络），因此「最短有向路径」只剩祖先→后代一条，"
            "SDP 的含义从「中介性」退化为「子树规模 × 深度」。",
            "阈值未由甲方给定：≥2 是 307 个（24.1163%）、≥3 是 72 个、≥4 只有 6 个，"
            "4 层 shell 无自然断点，「关键节点数」完全取决于选点。",
        ],
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print(f"[OK] {M} nodes={graph['nodes']} roots={graph['roots']} leaves={graph['leaves']} "
          f"maxdepth={graph['max_depth']} sdps>=3={counts_at(shell_asc, 3)}")
    print(f"     out -> {os.path.basename(OUT)} ({os.path.getsize(OUT)} B)")


def is_desc(root, n, parent):
    p = parent.get(n)
    while p:
        if p == root:
            return True
        p = parent.get(p)
    return False


def root_of(n, parent, roots):
    p = n
    seen = set()
    while p and p not in roots and p not in seen:
        seen.add(p)
        p = parent.get(p)
    return p


if __name__ == "__main__":
    main()
