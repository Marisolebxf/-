#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_SZ_LIST_TOPIC —— 深圳企业清单与链中角色（W13-E4）

口径（calc-logic 正本）：
  成员 = (org_id, chain_code, node_stage)，深圳 = region_id LIKE '4403%'，角色 = 上/中/下游。
gkx 无 region_id 列，但 credit_code 第 3—8 位就是行政区划码，4403 即深圳市（与
`chain_firm_index_20261023.json` 的 city 口径同源），可等价实现深圳筛选。
链归属取 `industry_code` 首码（§3.55 禁止取 industry_link_code[0]）。
node_stage 全库无字段 → 本件只出「链 × 一级环节」清单，不冒充上中下游（见 §四）。

运行：cd code && python3 M_ENT_SZ_LIST_TOPIC.py
产物：code/M_ENT_SZ_LIST_TOPIC_out.json
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_ENT_SZ_LIST_TOPIC_out.json")

STAGE_ROOTS = ["stage", "segment", "tier", "游", "position"]


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    fam = load("supply_family_20261023.json")
    cols = load("gkx_columns_20261023.json")
    base = load("base_20261021.json")
    tree = load("chain_tree_20261021.json")
    idx = load("chain_firm_index_20261023.json")

    sz = fam["sz_chain"]
    chain_name = fam["chain_meta"]["chain_name"]
    l1_name = fam["chain_meta"]["l1_name"]

    # 深圳底册（本地口径，与链企业口径同一城市键）
    sz_base = sum(1 for r in base if (r[4] or "") == "深圳市")
    # 深圳底册按行政区划码（credit_code[2:8] 前 4 位 = 4403）交叉核对
    sz_base_by_code = sum(1 for r in base if (r[1] or "")[2:6] == "4403")
    # 底册侧挂链覆盖率：两个总体不同（链表 1.71M、底册 189k），必须分开报
    credit_chain = fam["credit_chain_base"]
    sz_base_chain = sum(1 for r in base
                        if (r[4] or "") == "深圳市" and (r[1] or "") in credit_chain)

    # node_stage 字段扫描：全库有没有「上中下游」编码
    stage_hits = []
    for t, meta in cols["tables"].items():
        for c, ty in meta["columns"]:
            lc = c.lower()
            if any(s in lc for s in STAGE_ROOTS):
                stage_hits.append({"table": t, "column": c, "type": ty})
    stage_hits = [h for h in stage_hits if h["table"] != "dwd_dim_admin_area"]

    l1_nodes = []
    for code, cnt in sorted(sz["by_l1"].items(), key=lambda kv: -kv[1]):
        l1_nodes.append({"l1_code": code, "l1_name": l1_name.get(code),
                         "chain": code[:7], "chain_name": chain_name.get(code[:7]),
                         "sz_firms": cnt})

    by_chain = []
    for code, cnt in sorted(sz["by_chain"].items(), key=lambda kv: -kv[1]):
        nat = idx["chain_firms"].get(code, 0)
        by_chain.append({"chain": code, "chain_name": chain_name.get(code),
                         "sz_firms": cnt, "national_firms": nat,
                         "sz_share_pct": round(cnt / nat * 100, 2) if nat else None})

    chain_total = sum(idx["chain_firms"].values())
    out = {
        "metric_id": "M_ENT_SZ_LIST_TOPIC",
        "metric_name": "深圳企业清单与链中角色",
        "support_judgment": "部分支持",
        "judgment_reason": (
            "深圳键与链归属都可等价实现（深圳 92,930 家与已交付链企业快照逐项对上），"
            "但 calc-logic 要求的角色字段 node_stage（上/中/下游）在 gkx 全库 0 字段，"
            "链树只有目录层级与环节名，不能推出上中下游 → 清单可出、角色不可出。"),
        "verdict_kind": "partial_evidence",
        "formula": "members = {(credit_code, chain_code, l1_code) | credit_code[2:6]=4403 AND chain_code != null}",
        "params": {
            "sz_key": "credit_code[2:8] 行政区划码前 4 位 = 4403（等价 calc-logic 的 region_id LIKE '4403%'）",
            "chain_key": "dwd_org_industry_tags.industry_code 首个 INB 码前 7 位（§3.55）",
            "role_key": "无可用的 node_stage 字段；本件以一级环节（industry_link_code 的 9 位码）替代披露，不称上中下游",
            "min_peers": None,
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "本件是链属快照的截面清单（dwd_org_industry_tags 为当前态，无年度分区），"
            "不涉及多期基期；快照抓取日 2026-10-22/23。不把缺失年份按 0 摊入任何分母。"),
        "totals": {
            "sz_chain_firms": sz["total"],
            "sz_firms_multi_l1": sz["multi_l1"],
            "sz_firms_no_l1_within_chain": sz["no_l1"],
            "sz_base_firms_city_name": sz_base,
            "sz_base_firms_credit_prefix": sz_base_by_code,
            "sz_base_firms_with_chain": sz_base_chain,
            "sz_base_chain_cover_pct": round(sz_base_chain / max(1, sz_base) * 100, 2),
            "national_chain_firms": chain_total,
            "sz_share_of_national_chain_pct": round(sz["total"] / max(1, chain_total) * 100, 2),
            "n_chains": len(sz["by_chain"]),
            "n_l1_nodes": len(sz["by_l1"]),
            "crosscheck_chain_firm_index_sz": sz.get("crosscheck_chain_firm_index_sz"),
            "crosscheck_match": sz.get("crosscheck_chain_firm_index_sz") == sz["total"],
        },
        "by_chain": by_chain,
        "by_l1": l1_nodes,
        "district": sz["district"],
        "district_note": (
            "credit_code[2:8] 在深圳全部为 440300（市级登记机关码），本键无法拆到区；"
            "calc-logic 的 region_id 含区级码，本件等价实现只到市级。"),
        "stage_field_scan": {
            "roots": STAGE_ROOTS,
            "n_hits": len(stage_hits),
            "hits": stage_hits[:20],
            "conclusion": ("全库命中 stage/segment/tier/游/position 的列全部属于招投标阶段、"
                           "高管职务、行政区层级等无关字段；链表无上中下游编码。"),
        },
        "stage_fallback": {
            "provided": "一级环节（9 位码，40 个节点）",
            "not_claimed": "上游/中游/下游",
            "why": ("链树 dwd_industry_chain_info 的 level 是目录层级（链—环节—细分环节），"
                    "不是供应链游别；calc-logic 正本明写『禁止节点名顶游』。"),
        },
        "samples": sz["samples"][:60],
        "sources": {
            "db": "gkx @ 183.240.141.251:3318",
            "tables": ["gkx.dwd_org_industry_tags", "gkx.dwd_industry_chain_info",
                       "gkx.dwd_org_base_info"],
            "snapshots": ["code/_snapshots21/supply_family_20261023.json",
                          "code/_snapshots21/chain_firm_index_20261023.json",
                          "code/_snapshots21/base_20261021.json",
                          "code/_snapshots21/chain_tree_20261021.json",
                          "code/_snapshots21/gkx_columns_20261023.json"],
        },
        "generated_at": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps(out["totals"], ensure_ascii=False, indent=1))
    print("stage hits", len(stage_hits), stage_hits[:5])
    print("saved", OUT)


if __name__ == "__main__":
    main()
