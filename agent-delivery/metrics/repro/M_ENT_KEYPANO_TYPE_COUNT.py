#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_KEYPANO_TYPE_COUNT 覆盖企业类型数（零 DB，族级快照重算）。

口径（calc-logic COVER-STAT-L01）：
  每个 (chain_code, node_stage) 格子里，重点名单成员落到的六类标签有几类 >= 1 家。
  返回值域 0..6；一企可进多类，覆盖数不是企业数。

成员面沿用 `keypano_base_20261023.json`（4,561 家专利阈值代理名单）；
六类标签在该快照里已由 `dwd_org_tech_tag` 的 55 个原始标签归并成布尔位。
"""
from __future__ import annotations

import json
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "_snapshots21", "keypano_base_20261023.json")
PROBE = os.path.join(HERE, "_snapshots21", "ent_keypano_type_probe_20261023.json")
OUT = os.path.join(HERE, "M_ENT_KEYPANO_TYPE_COUNT_out.json")

TAGS = [
    ("foreign", "外资", "foreign_proxy"),
    ("high_tech", "高新", "high_tech"),
    ("sme", "小微（科技型中小企业代理）", "sme"),
    ("listed", "上市", "listed_proxy"),
    ("little_giant", "专精特新", "little_giant"),
    ("little_giant_pro", "小巨人", "little_giant_pro"),
]
STAGES = [("up", "上游"), ("mid", "中游"), ("down", "下游")]


def main():
    kb = json.load(open(BASE, encoding="utf-8"))
    probe = json.load(open(PROBE, encoding="utf-8"))
    firms = kb["firms"]
    chain_name = {}
    for f in firms:
        for c in f["chains"]:
            chain_name.setdefault(c, None)
    # 链名从共享快照的 chain_stage 统计键 + 已知 12 链名表取
    known = {
        "INB1204": "机器人", "INB1209": "智能网联汽车", "INB1236": "低空经济",
        "INB1303": "集成电路", "INB1306": "软件与信息服务", "INB1309": "人工智能",
        "INB1323": "传感器", "INB1333": "智能终端", "INB1354": "具身智能",
        "INB1502": "数字创意", "INB2503": "生物医药", "INB2505": "合成生物",
    }
    chains = sorted(known)

    # 建立 (chain, stage) -> 企业集合
    cell_members = defaultdict(set)
    for f in firms:
        for c, stages in f["chain_stages"].items():
            for s in set(stages):
                cell_members[(c, s)].add(f["org_id"])

    by_id = {f["org_id"]: f for f in firms}
    cells = []
    for c in chains:
        for s, s_cn in STAGES:
            members = cell_members.get((c, s), set())
            counts = {code: sum(1 for oid in members if by_id[oid][flag]) for code, _, flag in TAGS}
            cover = sum(1 for v in counts.values() if v > 0)
            cells.append({
                "chain_code": c,
                "chain_name": known[c],
                "node_stage": s,
                "node_stage_cn": s_cn,
                "firm_n": len(members),
                "tag_counts": counts,
                "tag_sum": sum(counts.values()),
                "type_cover_count": cover,
                "empty": len(members) == 0,
                "full_six": cover == 6,
                "zero_type": cover == 0,
                "top_tag": max(counts.items(), key=lambda kv: kv[1])[0] if members else None,
            })

    # 覆盖数分布（36 格全量，含空格）
    dist = Counter(x["type_cover_count"] for x in cells)
    cover_dist = [{"type_cover_count": k, "cell_n": dist.get(k, 0),
                   "cell_pct": round(dist.get(k, 0) / 36 * 100, 4)} for k in range(7)]

    # 链级
    chain_rows = []
    for c in chains:
        cs = [x for x in cells if x["chain_code"] == c]
        nonempty = [x for x in cs if not x["empty"]]
        chain_rows.append({
            "chain_code": c,
            "chain_name": known[c],
            "cell_n": len(nonempty),
            "cover_sum": sum(x["type_cover_count"] for x in cs),
            "cover_mean_nonempty": round(
                sum(x["type_cover_count"] for x in nonempty) / len(nonempty), 4
            ) if nonempty else 0.0,
            "cover_max": max((x["type_cover_count"] for x in cs), default=0),
            "cover_min_nonempty": min((x["type_cover_count"] for x in nonempty), default=0),
            "full_six_cell_n": sum(1 for x in cs if x["full_six"]),
        })

    # 链位级
    stage_rows = []
    for s, s_cn in STAGES:
        ss = [x for x in cells if x["node_stage"] == s]
        ne = [x for x in ss if not x["empty"]]
        stage_rows.append({
            "node_stage": s,
            "node_stage_cn": s_cn,
            "cell_n_nonempty": len(ne),
            "cover_sum": sum(x["type_cover_count"] for x in ss),
            "cover_mean_nonempty": round(
                sum(x["type_cover_count"] for x in ne) / len(ne), 4) if ne else 0.0,
            "full_six_cell_n": sum(1 for x in ss if x["full_six"]),
        })

    nonempty = [x for x in cells if not x["empty"]]
    full = [x for x in cells if x["full_six"]]
    zero = [x for x in cells if x["zero_type"]]
    max_cell = max(nonempty, key=lambda x: x["type_cover_count"]) if nonempty else None
    min_cell = min(nonempty, key=lambda x: x["type_cover_count"]) if nonempty else None

    # 六类在整份名单上的家数（仅用于解释覆盖来源，不作为格内分母）
    roster_tag = {}
    for code, name, flag in TAGS:
        n = sum(1 for f in firms if f[flag])
        roster_tag[code] = {"name": name, "firm_n": n,
                            "share_in_roster_pct": round(n / len(firms) * 100, 4)}
    union_n = sum(1 for f in firms if any(f[fl] for _, _, fl in TAGS))

    # 与链路边的对账：格内成员并集
    member_union = set()
    for members in cell_members.values():
        member_union |= members

    doc = {
        "metric_id": "M_ENT_KEYPANO_TYPE_COUNT",
        "metric_name": "覆盖企业类型数",
        "script": "M_ENT_KEYPANO_TYPE_COUNT.py",
        "data_source": "gkx @ 183.240.141.251:3318（只读）",
        "grain": "(chain_code, node_stage) -> type_cover_count (0..6)",
        "shared_base": {
            "snapshot": "code/_snapshots21/keypano_base_20261023.json",
            "roster_n": len(firms),
            "roster_rule": kb["roster_rule"],
            "in_chain_n": kb["stats"]["in_chain_n"],
            "with_stage_n": kb["stats"]["with_stage_n"],
            "cell_n": kb["stats"]["chain_stage_cell_n"],
            "member_row_n": kb["stats"]["chain_stage_pair_n"],
            "scan_rows": kb["stats"]["scan_rows"],
            "scan_bad_credit_rows": kb["stats"]["scan_bad_credit_rows"],
        },
        "probes": {
            "roster_n": len(firms),
            "tag_code_n": len(TAGS),
            "cell_universe_n": 36,
            "cell_n_nonempty": len(nonempty),
            "cell_n_empty": 36 - len(nonempty),
            "cell_n_full_six": len(full),
            "cell_n_zero_type": len(zero),
            "cover_distribution": cover_dist,
            "cover_sum": sum(x["type_cover_count"] for x in cells),
            "full_six_share_of_nonempty_pct": round(len(full) / len(nonempty) * 100, 4) if nonempty else 0.0,
            "empty_cell_share_pct": round((36 - len(nonempty)) / 36 * 100, 4),
            "cover_mean_nonempty": round(
                sum(x["type_cover_count"] for x in nonempty) / len(nonempty), 4
            ) if nonempty else 0.0,
            "max_cell": max_cell,
            "min_nonempty_cell": min_cell,
            "roster_tag_totals": roster_tag,
            "tag_union_roster_n": union_n,
            "tag_sum_roster_n": sum(v["firm_n"] for v in roster_tag.values()),
            "member_firm_union_n": len(member_union),
            "with_stage_share_pct": round(len(member_union) / len(firms) * 100, 4),
            "tag_union_share_pct": round(union_n / len(firms) * 100, 4),
            "tag_per_union_firm": round(sum(v["firm_n"] for v in roster_tag.values()) / union_n, 4),

            "cell_membership_sum": sum(len(v) for v in cell_members.values()),
            "field_basis": {
                "foreign": "tech_tag 含外资/港澳台投资类标签（proxy）",
                "high_tech": "高新技术企业（含国家级/曾获）",
                "sme": "科技型中小企业（不含曾获/过期待复核）",
                "listed": "上市/挂牌（proxy，来自 base_info listing_status + org_type）",
                "little_giant": "专精特新中小企业（含省级）",
                "little_giant_pro": "专精特新小巨人（含国家级）",
            },
        },
        "probes_negative": {
            "blocking_table_exist_gkx": probe["gkx"]["blocking_exist"],
            "pattern_hits_gkx": probe["gkx"]["pattern_hits"],
            "live_counts": {
                "DWD": probe["live"]["DWD"]["counts"],
                "ADS": probe["live"]["ADS"]["counts"],
                "DIM": probe["live"]["DIM"]["counts"],
            },
            "substitute": probe["negative_evidence"]["substitute"],
            "gkx_side": probe["negative_evidence"]["gkx_side"],
            "live_side": probe["negative_evidence"]["live_side"],
            "note": "enterprise_tag / key_enterprise / enterprise_industry_chain 在 gkx 无表；"
                    "live DWD 同名表 0 行（空壳），ADS key_enterprise 87 行为演示样本，不参与计算。",
        },
        "result": {
            "cells": cells,
            "chain_level": chain_rows,
            "stage_level": stage_rows,
            "cover_distribution": cover_dist,
        },
        "support_judgment": "部分支持",
        "verdict_kind": "proxy_partial",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面件：名单按专利授权累计量一次性截取，链位与标签无年度键；"
                           "不设基期，不得用 created_time 反推年度。",
        "sources": [
            "code/_snapshots21/keypano_base_20261023.json",
            "code/_snapshots21/ent_keypano_type_probe_20261023.json",
            "gkx.dwd_org_industry_tags (2,283,762 rows)",
            "gkx.dwd_org_base_info (189,116 rows)",
            "gkx.dwd_org_tech_tag (202,424 rows / 55 tags)",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    print("wrote", OUT)
    print("cells", len(cells), "nonempty", len(nonempty), "full6", len(full),
          "cover_sum", doc["probes"]["cover_sum"], "mean", doc["probes"]["cover_mean_nonempty"])
    print("dist", cover_dist)


if __name__ == "__main__":
    main()
