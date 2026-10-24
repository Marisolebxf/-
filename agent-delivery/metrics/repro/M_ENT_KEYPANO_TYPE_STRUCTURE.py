#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_KEYPANO_TYPE_STRUCTURE 企业类型分布（零 DB，族级快照重算）。

口径（calc-logic COVER-STAT-L01）：
  每个 (chain_code, node_stage, tag_code) 格子里，六类标签各有多少家重点企业。
  一企可进多类，六类不可相加；区域维不属于本件。

成员面与 `M_ENT_KEYPANO_TYPE_COUNT` 共用 `keypano_base_20261023.json`（4,561 家）。
链级结果与同族 `M_ENT_KEYPANO_QUAL_DISTRIBUTION_out.json` 的 `chain_tag_matrix`
逐对比对，确保同一母体在不同切法下不漂移。
"""
from __future__ import annotations

import json
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "_snapshots21", "keypano_base_20261023.json")
PROBE = os.path.join(HERE, "_snapshots21", "ent_keypano_type_probe_20261023.json")
QUAL = os.path.join(HERE, "M_ENT_KEYPANO_QUAL_DISTRIBUTION_out.json")
OUT = os.path.join(HERE, "M_ENT_KEYPANO_TYPE_STRUCTURE_out.json")

TAGS = [
    ("foreign", "外资", "foreign_proxy"),
    ("high_tech", "高新", "high_tech"),
    ("sme", "小微（科技型中小企业代理）", "sme"),
    ("listed", "上市", "listed_proxy"),
    ("little_giant", "专精特新", "little_giant"),
    ("little_giant_pro", "小巨人", "little_giant_pro"),
]
STAGES = [("up", "上游"), ("mid", "中游"), ("down", "下游")]
CHAIN_NAME = {
    "INB1204": "机器人", "INB1209": "智能网联汽车", "INB1236": "低空经济",
    "INB1303": "集成电路", "INB1306": "软件与信息服务", "INB1309": "人工智能",
    "INB1323": "传感器", "INB1333": "智能终端", "INB1354": "具身智能",
    "INB1502": "数字创意", "INB2503": "生物医药", "INB2505": "合成生物",
}


def pct(a, b):
    return round(a / b * 100, 4) if b else 0.0


def main():
    kb = json.load(open(BASE, encoding="utf-8"))
    probe = json.load(open(PROBE, encoding="utf-8"))
    firms = kb["firms"]
    by_id = {f["org_id"]: f for f in firms}
    chains = sorted(CHAIN_NAME)

    cell_members = defaultdict(set)
    for f in firms:
        for c, stages in f["chain_stages"].items():
            for s in set(stages):
                cell_members[(c, s)].add(f["org_id"])

    # 216 行：36 格 × 6 类（空行保留，符合「无行当 0」）
    rows = []
    for c in chains:
        for s, s_cn in STAGES:
            members = cell_members.get((c, s), set())
            for code, name, flag in TAGS:
                ids = {oid for oid in members if by_id[oid][flag]}
                rows.append({
                    "chain_code": c,
                    "chain_name": CHAIN_NAME[c],
                    "node_stage": s,
                    "node_stage_cn": s_cn,
                    "tag_code": code,
                    "tag_name": name,
                    "ent_count": len(ids),
                    "cell_firm_n": len(members),
                    "share_in_cell_pct": pct(len(ids), len(members)),
                })

    # 链级矩阵 12 × 6：denominator = 该链去重企业数（不是 4,561）
    chain_tag = []
    for c in chains:
        cf = [f for f in firms if c in f["chains"]]
        row = {"chain_code": c, "chain_name": CHAIN_NAME[c],
               "chain_firm_n": len(cf)}
        for code, name, flag in TAGS:
            n = sum(1 for f in cf if f[flag])
            row[code] = n
        row["tag_union_firm_n"] = sum(1 for f in cf if any(f[fl] for _, _, fl in TAGS))
        row["tag_sum"] = sum(row[code] for code, _, _ in TAGS)
        row["overlap_ratio"] = round(row["tag_sum"] / row["tag_union_firm_n"], 4) \
            if row["tag_union_firm_n"] else 0.0
        chain_tag.append(row)

    # 链位级矩阵 3 × 6：denominator = 该链位去重企业数
    stage_tag = []
    for s, s_cn in STAGES:
        sf = [f for f in firms if s in f["stages"]]
        row = {"node_stage": s, "node_stage_cn": s_cn,
               "stage_firm_n": len(sf)}
        for code, name, flag in TAGS:
            row[code] = sum(1 for f in sf if f[flag])
        row["tag_union_firm_n"] = sum(1 for f in sf if any(f[fl] for _, _, fl in TAGS))
        row["tag_sum"] = sum(row[code] for code, _, _ in TAGS)
        stage_tag.append(row)

    # 全名单矩阵 6 类 + 两两共现（解释「覆盖数为何饱和」）
    roster_counts = {code: sum(1 for f in firms if f[flag])
                     for code, _, flag in TAGS}
    co = []
    for a, an, af in TAGS:
        for b, bn, bf in TAGS:
            n = sum(1 for f in firms if f[af] and f[bf])
            co.append({"tag_a": a, "tag_b": b, "both_n": n,
                       "jaccard": round(n / (roster_counts[a] + roster_counts[b] - n), 4)
                       if roster_counts[a] + roster_counts[b] - n else 0.0})

    # 非零格 TOP
    nz = [r for r in rows if r["ent_count"] > 0]
    top = sorted(nz, key=lambda r: (-r["ent_count"], r["chain_code"]))[:15]
    thin = sorted([r for r in rows if 0 < r["ent_count"] <= 2],
                  key=lambda r: (r["ent_count"], r["chain_code"]))[:15]

    # 与 QUAL 的 chain_tag_matrix 对账（同一母体的两种切法）
    qual_check = {"qual_file_exists": os.path.exists(QUAL), "pair_checked_n": 0,
                  "mismatch_n": 0, "mismatch_examples": []}
    if os.path.exists(QUAL):
        q = json.load(open(QUAL, encoding="utf-8"))
        qm = {r["chain_code"]: r for r in q["result"]["chain_tag_matrix"]}
        for r in chain_tag:
            qr = qm.get(r["chain_code"])
            if not qr:
                continue
            for code, _, _ in TAGS:
                qual_check["pair_checked_n"] += 1
                if int(qr.get(code, -1)) != int(r[code]):
                    qual_check["mismatch_n"] += 1
                    if len(qual_check["mismatch_examples"]) < 6:
                        qual_check["mismatch_examples"].append(
                            {"chain": r["chain_code"], "tag": code,
                             "this": r[code], "qual": qr.get(code)})
        qual_check["chain_firm_mismatch_n"] = sum(
            1 for r in chain_tag
            if int(qm.get(r["chain_code"], {}).get("chain_firm_n", -1)) != r["chain_firm_n"])

    # 格内「六类之和 / 格内企业数」——重叠度
    overlap_cells = []
    for c in chains:
        for s, s_cn in STAGES:
            members = cell_members.get((c, s), set())
            if not members:
                continue
            ssum = sum(1 for oid in members for _, _, fl in TAGS if by_id[oid][fl])
            overlap_cells.append({
                "chain_code": c, "chain_name": CHAIN_NAME[c],
                "node_stage": s, "node_stage_cn": s_cn,
                "cell_firm_n": len(members), "tag_sum": ssum,
                "tag_per_firm": round(ssum / len(members), 4),
            })
    overlap_cells.sort(key=lambda x: (-x["tag_per_firm"], x["chain_code"]))

    # 派生比值：分子分母都取本件产物内的同名字段，正文只引用这里的结果
    roster_union_n = sum(1 for f in firms if any(f[fl] for _, _, fl in TAGS))
    roster_sum_n = sum(roster_counts.values())
    pair_n = {(x["tag_a"], x["tag_b"]): x["both_n"] for x in co}
    stage_by_code = {r["node_stage"]: r for r in stage_tag}
    max_row = top[0] if top else None
    derived = {
        "tag_sum_roster_n": roster_sum_n,
        "tag_union_roster_n": roster_union_n,
        "tag_per_union_firm": round(roster_sum_n / roster_union_n, 4) if roster_union_n else 0.0,
        "tag_per_union_firm_formula": "tag_sum_roster_n / tag_union_roster_n",
        "little_giant_in_high_tech_n": pair_n.get(("high_tech", "little_giant"), 0),
        "little_giant_in_high_tech_share_of_little_giant_pct": pct(
            pair_n.get(("high_tech", "little_giant"), 0), roster_counts.get("little_giant", 0)),
        "little_giant_pro_in_high_tech_n": pair_n.get(("high_tech", "little_giant_pro"), 0),
        "little_giant_pro_in_high_tech_share_of_little_giant_pro_pct": pct(
            pair_n.get(("high_tech", "little_giant_pro"), 0), roster_counts.get("little_giant_pro", 0)),
        "stage_high_tech_share_pct": {
            s: pct(r["high_tech"], r["stage_firm_n"]) for s, r in stage_by_code.items()
        },
        "counterexample_max_row_over_roster_pct": pct(max_row["ent_count"], len(firms)) if max_row else 0.0,
        "denominator_note": "tag_per_union_firm 的分母是六类去重并集 tag_union_roster_n；"
                            "stage_high_tech_share_pct 的分母是该链位去重企业数 stage_firm_n；"
                            "little_giant_* 的分母是该类在名单内的家数；"
                            "counterexample_* 是错误分母（4,561 家名单）示例，仅用于陷阱说明。",
    }

    doc = {
        "metric_id": "M_ENT_KEYPANO_TYPE_STRUCTURE",
        "metric_name": "企业类型分布（当前链位）",
        "script": "M_ENT_KEYPANO_TYPE_STRUCTURE.py",
        "data_source": "gkx @ 183.240.141.251:3318（只读）",
        "grain": "(chain_code, node_stage, tag_code) -> COUNT(DISTINCT org_id)",
        "shared_base": {
            "snapshot": "code/_snapshots21/keypano_base_20261023.json",
            "roster_n": len(firms),
            "roster_rule": kb["roster_rule"],
            "in_chain_n": kb["stats"]["in_chain_n"],
            "with_stage_n": kb["stats"]["with_stage_n"],
            "chain_n": len(chains),
            "cell_n": kb["stats"]["chain_stage_cell_n"],
            "member_row_n": kb["stats"]["chain_stage_pair_n"],
            "scan_rows": kb["stats"]["scan_rows"],
            "scan_bad_credit_rows": kb["stats"]["scan_bad_credit_rows"],
        },
        "probes": {
            "roster_n": len(firms),
            "tag_n": len(TAGS),
            "row_universe_n": 12 * 3 * 6,
            "row_nonzero_n": len(nz),
            "row_zero_n": 216 - len(nz),
            "row_nonzero_pct": pct(len(nz), 216),
            "row_zero_pct": pct(216 - len(nz), 216),
            "mean_tags_per_firm_in_cells": round(
                sum(x["tag_sum"] for x in overlap_cells) /
                sum(x["cell_firm_n"] for x in overlap_cells), 4) if overlap_cells else 0.0,
            "roster_tag_totals": {code: {"name": name, "firm_n": roster_counts[code],
                                         "share_in_roster_pct": pct(roster_counts[code], len(firms))}
                                  for code, name, _ in TAGS},
            "tag_union_roster_n": sum(1 for f in firms if any(f[fl] for _, _, fl in TAGS)),
            "tag_sum_roster_n": sum(roster_counts.values()),
            "cell_tag_sum": sum(r["ent_count"] for r in rows),
            "chain_tag_sum": sum(r["tag_sum"] for r in chain_tag),
            "stage_tag_sum": sum(r["tag_sum"] for r in stage_tag),
            "max_row": top[0] if top else None,
            "top_rows": top,
            "thin_rows": thin,
            "overlap_cells_top": overlap_cells[:5],
            "overlap_cells_bottom": overlap_cells[-5:],
            "cooccurrence": co,

            "qual_cross_check": qual_check,
            "field_basis": {
                "foreign": "tech_tag 外资/港澳台投资类标签（proxy）",
                "high_tech": "高新技术企业（含国家级/曾获）",
                "sme": "科技型中小企业（不含曾获/待复核）",
                "listed": "上市/挂牌（proxy）",
                "little_giant": "专精特新中小企业（含省级）",
                "little_giant_pro": "专精特新小巨人（含国家级）",
            },
        },
        "derived": derived,
        "probes_negative": {
            "blocking_table_exist_gkx": probe["gkx"]["blocking_exist"],
            "live_counts_DWD": probe["live"]["DWD"]["counts"],
            "live_counts_ADS": probe["live"]["ADS"]["counts"],
            "substitute": probe["negative_evidence"]["substitute"],
            "gkx_side": probe["negative_evidence"]["gkx_side"],
            "live_side": probe["negative_evidence"]["live_side"],
            "note": "六类 tag_code 的原始字典（tag_dict）在两库均不可用；本件用 55 个真实标签"
                    "按关键词归并出六类，属转换口径，不是库内 tag_code 直读。",
        },
        "result": {
            "node_type_rows": rows,
            "chain_tag_matrix": chain_tag,
            "stage_tag_matrix": stage_tag,
        },
        "support_judgment": "部分支持",
        "verdict_kind": "proxy_partial",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面件：六类标签是当前时点认定状态，无年度键；"
                           "不设基期，不得用 created_time 反推年度。",
        "sources": [
            "code/_snapshots21/keypano_base_20261023.json",
            "code/_snapshots21/ent_keypano_type_probe_20261023.json",
            "code/M_ENT_KEYPANO_QUAL_DISTRIBUTION_out.json",
            "gkx.dwd_org_tech_tag (202,424 rows / 55 tags)",
            "gkx.dwd_org_industry_tags (2,283,762 rows)",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    print("wrote", OUT)
    print("rows", len(rows), "nonzero", len(nz), "zero", 216 - len(nz))
    print("top", top[0])
    print("qual_check", qual_check)


if __name__ == "__main__":
    main()
