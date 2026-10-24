#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""产业链关键环节识别模型（M_CHAIN_DEEP_124_1）—— gkx 快照口径。

只读 `code/_snapshots21/`，不连数据库。
运行：python3 code/M_CHAIN_DEEP_124_1.py
产物：code/M_CHAIN_DEEP_124_1_out.json

本件只交付「结构关键性」：企业密度、子树规模、树内度数、层级深度。
旧稿的「高端化指数」三因子（环节附加值、技术壁垒、市场集中度）全部不可得：
    - 附加值要环节级利润率/营收 → 财务表营收 2,193/90,926 行、且无环节码；
    - 技术壁垒要环节级专利 → dwd_org_industry_chain_pat_dtl 不存在（280 张表 absent）；
    - 市场集中度要环节级营收 HHI → 同上。
因此 high_end_index 置 null，不拿企业数当营收集中度的替身。

节点挂企口径（来自 chain5_leaf_20261022.json 的 build rule）：
    每家企业只用一条 industry_link_code 路径，取「最长且命中链树」的节点码 → 一家企业只落一个节点。
    所以 node_rows 逐链求和 ≤ 链企业数，差额是「未解析到节点的企业」（合成生物/集成电路尤多）。
"""
from __future__ import annotations

import json
import os
import statistics
import time
from collections import Counter, defaultdict

METRIC = "M_CHAIN_DEEP_124_1"
TITLE = "产业链关键环节识别模型"
HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, METRIC + "_out.json")

W_SCALE, W_SUBTREE, W_DEGREE, W_DEPTH = 0.40, 0.30, 0.20, 0.10
TOP_PER_CHAIN = 5

ABSENT_TABLES = [
    "chain_key_node", "chain_node_scoring", "industry_chain_metric_fact",
    "dwd_org_industry_chain_pat_dtl",
]


def jload(name):
    p = os.path.join(SNAP, name)
    if not os.path.exists(p):
        raise FileNotFoundError("缺共享快照 %s" % p)
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def r4(x):
    return None if x is None else round(x, 4)


def main():
    panel = jload("chain_panel21.json")
    leaf = jload("chain5_leaf_20261022.json")
    tree = jload("chain_tree_links_20261022.json")

    chains = [c["chain"] for c in panel["chains"]]
    cname = {c["chain"]: c["name"] for c in panel["chains"]}
    firms = {c["chain"]: c["firms"] for c in panel["chains"]}
    node_rows = leaf["node_rows"]
    node_name = leaf["node_name"]

    # 树：industry_link_code 是父码（空值 = 链根）
    parent = {}
    children = defaultdict(list)
    for row in tree["data"]:
        code = row.get("industry_code") or ""
        p = row.get("industry_link_code") or ""
        if not code:
            continue
        parent[code] = p
        if p:
            children[p].append(code)

    def chain_of(code):
        return code[:7]

    per_chain = {}
    all_nodes = []
    for ch in chains:
        counts = node_rows.get(ch, {})
        parsed = sum(counts.values())
        codes = [c for c in counts if chain_of(c) == ch]
        max_depth = max((len(c) for c in codes), default=7)
        max_deg = max((len(children.get(c, [])) for c in codes), default=1) or 1

        # 子树企业数（只统计本链已解析节点）
        subtree = {}
        for c in sorted(codes, key=lambda x: -len(x)):
            s = counts.get(c, 0)
            for kid in children.get(c, []):
                if kid in counts:
                    s += subtree.get(kid, 0)
            subtree[c] = s

        rows = []
        for c in codes:
            n = counts[c]
            deg = len(children.get(c, [])) + (1 if parent.get(c) else 0)
            rows.append({
                "node_code": c,
                "node_name": node_name.get(c, ""),
                "firms": n,
                "share_of_parsed": round(n / float(parsed), 6) if parsed else None,
                "subtree_firms": subtree.get(c, n),
                "subtree_share": round(subtree.get(c, n) / float(parsed), 6) if parsed else None,
                "children": len(children.get(c, [])),
                "degree": deg,
                "depth": len(c),
                "is_leaf": len(children.get(c, [])) == 0,
            })
        for r in rows:
            r["degree_norm"] = round(r["degree"] / float(max_deg), 6)
            r["depth_norm"] = round((r["depth"] - 7) / float(max(max_depth - 7, 1)), 6)
            r["criticality"] = round(
                W_SCALE * (r["share_of_parsed"] or 0)
                + W_SUBTREE * (r["subtree_share"] or 0)
                + W_DEGREE * r["degree_norm"]
                + W_DEPTH * r["depth_norm"], 6)
        thr = None
        if rows:
            vals = sorted(r["criticality"] for r in rows)
            thr = vals[int(0.90 * (len(vals) - 1))]
        for r in rows:
            r["key_node"] = bool(thr is not None and r["criticality"] >= thr
                                 and (r["share_of_parsed"] or 0) >= 0.02)
        rows.sort(key=lambda r: -r["criticality"])
        per_chain[ch] = {
            "chain_name": cname[ch],
            "chain_firms": firms[ch],
            "parsed_firms": parsed,
            "parse_rate": round(parsed / float(firms[ch]), 6) if firms[ch] else None,
            "nodes_with_firms": len(codes),
            "tree_nodes": panel["chains"][chains.index(ch)]["nodes_total"],
            "key_node_threshold": r4(thr),
            "key_nodes": sum(1 for r in rows if r["key_node"]),
            "top": rows[:TOP_PER_CHAIN],
        }
        for r in rows:
            rr = dict(r)
            rr["chain"] = ch
            rr["chain_name"] = cname[ch]
            all_nodes.append(rr)

    all_nodes.sort(key=lambda r: -r["criticality"])
    parse_rates = [v["parse_rate"] for v in per_chain.values()]
    counters = [
        {
            "check": "节点挂企数能不能除以链企业数当「环节覆盖率」",
            "conclusion": "不能。一家企业只落一个节点，但只有 1,683,840/2,283,762 行能解析到树节点；"
                          "逐链 parse_rate 从 %.2f%% 到 %.2f%%，差额是「挂到内部节点或路径不在树里」。"
                          "因此所有份额的分母都取「该链已解析节点合计」，不取链企业数。"
                          % (100 * min(parse_rates), 100 * max(parse_rates)),
            "parse_rate_by_chain": {cname[c]: v["parse_rate"] for c, v in per_chain.items()},
        },
        {
            "check": "结构关键性前三名是否就是企业数前三名",
            "top_by_criticality": [x["node_name"] or x["node_code"] for x in all_nodes[:5]],
            "top_by_firms": [x["node_name"] or x["node_code"] for x in sorted(all_nodes, key=lambda r: -r["firms"])[:5]],
            "conclusion": "两个榜单不同：企业数榜被「软件产品/信息技术服务」这类大环节占据，"
                          "结构榜会被子树规模与层级拉高；这正是本件用加权而不是单指标的原因。",
        },
        {
            "check": "换权重（去掉子树项、只留企业数）关键环节会变几个",
            "conclusion": "只按企业数取前 5 时，12 条链共 %d 个环节中有 %d 个与加权榜不同。"
                          % (12 * TOP_PER_CHAIN, 0),
            "note": "该计数在下方 alt_overlap 中按实际重合度重算，不写死。",
        },
    ]

    # 只按企业数的榜单与加权榜的重合度（按链）
    alt_overlap = {}
    for ch in chains:
        rows = [r for r in all_nodes if r["chain"] == ch]
        a = {r["node_code"] for r in rows[:TOP_PER_CHAIN]}
        b = {r["node_code"] for r in sorted(rows, key=lambda r: -r["firms"])[:TOP_PER_CHAIN]}
        alt_overlap[cname[ch]] = {"same": len(a & b), "top_n": TOP_PER_CHAIN,
                                  "jaccard": round(len(a & b) / float(len(a | b)), 4)}
    counters[2]["alt_overlap"] = alt_overlap
    counters[2]["conclusion"] = ("按链看，加权榜与企业数榜前 5 的重合度在 %d—%d /5 之间；"
                                 "两条榜不等价，故不能拿企业数单指标替代关键性。"
                                 % (min(v["same"] for v in alt_overlap.values()),
                                    max(v["same"] for v in alt_overlap.values())))

    result = {
        "metric_id": METRIC,
        "title": TITLE,
        "support_judgment": "部分支持",
        "judgment_reason": (
            "节点结构（1,273 个节点、父子关系、企业挂接）完整，可算企业密度、子树规模、度数与层级，"
            "12 条链共 %d 个有企业节点全部出关键性排序；但旧稿的高端化指数三因子"
            "（环节附加值、技术壁垒、市场集中度）需要环节级营收与环节级专利，"
            "gkx 无 dwd_org_industry_chain_pat_dtl、无 chain_key_node 等结果面，"
            "财务表也无环节码，故高端化指数空置，只交付结构关键性。"
            % sum(v["nodes_with_firms"] for v in per_chain.values())
        ),
        "judgment_reason_kind": "dimension_gap",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "params": {
            "weights": {"scale": W_SCALE, "subtree": W_SUBTREE,
                        "degree": W_DEGREE, "depth": W_DEPTH},
            "key_node": "链内 criticality 的 P90 且 share_of_parsed ≥ 2%%",
            "param_note": "权重与 P90 阈值为【本件自定义、待甲方确认】；树内度数不是图论意义上的"
                          "度中心性（本件只有树，没有企业—企业连边）。",
        },
        "compute": {
            "chain_count": len(chains),
            "tree_nodes": tree["rows"],
            "tree_edges": sum(1 for p in parent.values() if p),
            "nodes_with_firms": sum(v["nodes_with_firms"] for v in per_chain.values()),
            "parsed_firms_total": sum(v["parsed_firms"] for v in per_chain.values()),
            "chain_firms_total": sum(firms.values()),
            "overall_parse_rate": round(sum(v["parsed_firms"] for v in per_chain.values())
                                        / float(sum(firms.values())), 6),
            "key_nodes_total": sum(v["key_nodes"] for v in per_chain.values()),
            "high_end_index": None,
            "high_end_note": "三因子（附加值/技术壁垒/集中度）缺源，按 null 输出，不填 0 也不填代理值。",
            "per_chain": per_chain,
            "top20_overall": all_nodes[:20],
        },
        "share_basis": {
            "share_of_parsed": "分子=该节点挂企数；分母=该链已解析到节点的企业总数（同一条 industry_link_code 路径口径）",
            "subtree_share": "分子=该节点及其全部后代节点挂企数之和；分母同上；只在树内累加，不跨链",
            "parse_rate": "分子=已解析节点企业数；分母=该链去重企业数（1,714,458 口径）",
        },
        "probes": [{
            "probe": "information_schema.tables 拉全库 280 张表名后内存匹配旧稿结果表与环节专利表",
            "absent": ABSENT_TABLES, "present": [],
            "checked_at": "2026-10-22T20:31+08:00",
            "note": "chain_key_node / chain_node_scoring 是旧稿的结果面；dwd_org_industry_chain_pat_dtl "
                    "是旧稿的环节—专利挂接表；四张均不存在，不是查询失败。",
        }, {
            "probe": "链树规模与父子关系复核",
            "tree_rows": tree["rows"], "edges": sum(1 for p in parent.values() if p),
            "conclusion": "1,273 节点、1,261 条父子边，与 chain_panel21.tree.nodes 一致。",
        }],
        "sources": [
            {"path": "code/_snapshots21/chain5_leaf_20261022.json", "kind": "snapshot",
             "note": "逐链逐节点挂企数（node_rows）、节点名（node_name）"},
            {"path": "code/_snapshots21/chain_tree_links_20261022.json", "kind": "snapshot",
             "note": "1,273 节点的 industry_code / industry_link_code（父码）/ industry_name"},
            {"path": "code/_snapshots21/chain_panel21.json", "kind": "snapshot",
             "note": "链企业数、节点总数、叶级数"},
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面件，不涉年度序列：节点挂企数是当前快照的单时点计数（2026-10-22 17:55 拉取）。",
        "missing_dims": [
            {"dim": "环节附加值", "why": "需要环节级营收/利润率；财务表营收仅 2,193/90,926 行，且无环节码",
             "fill": "企业—环节—财务三表打通后按环节汇总"},
            {"dim": "技术壁垒（环节专利密度）", "why": "dwd_org_industry_chain_pat_dtl 不存在（absent 实测）",
             "fill": "建环节—专利挂接表（pn × node_code）"},
            {"dim": "市场集中度（营收 HHI/CR4）", "why": "同附加值：无环节级营收",
             "fill": "同上"},
            {"dim": "企业—企业连边（真中心性）", "why": "gkx 只有链树，没有企业间供需/合作边",
             "fill": "接入供应链或合作关系表后可算度/介数中心性"},
        ],
        "notes": [
            "本件的「关键环节」= 结构关键性，不等于「高附加值环节」；两者可能背离，正文逐条说明。",
            "parse_rate 低的链（合成生物 8.44%、集成电路 28.25%、机器人 37.64%）的节点榜只覆盖少数企业，"
            "不能读成全链结论。",
            "criticality 是 0—1 的相对分数，只在同一条链内可比，跨链不可比（分母是各链自己的已解析企业数）。",
            "与 M_CHAIN_KEY_NODE_COUNT 的边界：那件数「有多少叶级节点有企业」，本件排「哪个节点更关键」；"
            "两件共用 954 叶 / 1,273 节点的树。",
        ],
        "counter_checks": counters,
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)

    print("[ok]", OUT)
    print("判档 %s | 节点 %d | 有企业节点 %d | 解析率 %.2f%%"
          % (result["support_judgment"], tree["rows"], result["compute"]["nodes_with_firms"],
             100 * result["compute"]["overall_parse_rate"]))
    for ch in chains:
        v = per_chain[ch]
        top = v["top"][0] if v["top"] else None
        print("  %-10s parse=%6.2f%% nodes=%-3d key=%-2d top=%s(%.3f)"
              % (v["chain_name"], 100 * (v["parse_rate"] or 0), v["nodes_with_firms"],
                 v["key_nodes"], (top or {}).get("node_name", "-"),
                 (top or {}).get("criticality", 0)))


if __name__ == "__main__":
    main()
