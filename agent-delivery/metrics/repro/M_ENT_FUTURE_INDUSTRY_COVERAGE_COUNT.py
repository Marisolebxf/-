#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT 覆盖未来产业数（零 DB，族级快照重算）。

目标口径（calc-logic COVER-STAT-L01 / E-32）：
  当前企业集合落到的 5 个未来产业集群 `cluster_id` 去重数，值域 0..5。
  `industry_cluster.cluster_group='fut'` 是唯一判定入口。

实测：`industry_cluster` / `industry_cluster_map` 在 gkx 与 live 均无此表（探针
`ent_future_cluster_probe_20261023.json`），cluster 列 0 个。本件只能用 12 条链
按链名语义做「未来类目代理」，上限 4/5；代理映射写进产物，便于甲方逐条否决。
"""
from __future__ import annotations

import json
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PROBE = os.path.join(HERE, "_snapshots21", "ent_future_cluster_probe_20261023.json")
BASE = os.path.join(HERE, "_snapshots21", "keypano_base_20261023.json")
OUT = os.path.join(HERE, "M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT_out.json")

PROXY = {
    "CL-FUT-01": ("未来制造", ["INB1204", "INB1354", "INB1333", "INB1323", "INB1209"]),
    "CL-FUT-02": ("未来信息", ["INB1309", "INB1306", "INB1303", "INB1502"]),
    "CL-FUT-03": ("未来能源", []),
    "CL-FUT-04": ("未来空间", ["INB1236"]),
    "CL-FUT-05": ("未来健康", ["INB2503", "INB2505"]),
}


def pct(a, b):
    return round(a / b * 100, 4) if b else 0.0


def main():
    probe = json.load(open(PROBE, encoding="utf-8"))
    kb = json.load(open(BASE, encoding="utf-8"))
    firms = kb["firms"]
    idx = json.load(open(os.path.join(HERE, "_snapshots21",
                                      "chain_firm_index_20261023.json"), encoding="utf-8"))
    chain_firms = idx["chain_firms"]
    chain_name = idx["chain_name"]

    # 企业 -> 未来类目集合（按链代理）
    firm_cats = {}
    for f in firms:
        cats = set()
        for c in f["chains"]:
            for cid, (_, chains) in PROXY.items():
                if c in chains:
                    cats.add(cid)
        firm_cats[f["org_id"]] = cats

    covered = set()
    for cats in firm_cats.values():
        covered |= cats
    covered = sorted(covered)

    cat_rows = []
    for cid, (name, chains) in PROXY.items():
        ros_pairs = sum(1 for f in firms for c in f["chains"] if c in chains)
        ros_firms = sum(1 for f in firms if any(c in chains for c in f["chains"]))
        pop_pairs = sum(int(chain_firms.get(c, 0)) for c in chains)
        cat_rows.append({
            "cluster_id": cid,
            "cluster_name": name,
            "proxy_chains": chains,
            "proxy_chain_names": [chain_name.get(c, c) for c in chains],
            "roster_firm_n": ros_firms,
            "roster_firm_chain_pairs": ros_pairs,
            "population_firm_chain_pairs": pop_pairs,
            "covered_by_roster": cid in covered,
            "covered_by_population": pop_pairs > 0,
            "has_proxy_chain": len(chains) > 0,
        })

    dist = Counter(len(c) for c in firm_cats.values())
    dist_rows = [{"category_n": k, "firm_n": dist.get(k, 0),
                  "firm_pct": pct(dist.get(k, 0), len(firms))} for k in range(6)]

    # 稳健性：逐个剔除一条代理链，看覆盖类目是否仍为 4
    sens = []
    for cid, (name, chains) in PROXY.items():
        for drop in chains:
            remaining = set()
            for f in firms:
                for c in f["chains"]:
                    if c == drop:
                        continue
                    for cid2, (_, ch2) in PROXY.items():
                        if c in ch2:
                            remaining.add(cid2)
            sens.append({"dropped_chain": drop, "dropped_chain_name": chain_name.get(drop),
                         "covered_category_n": len(remaining)})
    sens_min = min((x["covered_category_n"] for x in sens), default=0)

    # 王惠 v5.1 的 8 类口径（REGEXP on industry_name；库内 industry_name 只有 12 个链名）
    import re as _re
    WH = [
        ("生物制造", r"合成生物|生物制造|生物工程|细胞工厂|基因工程"),
        ("物理智能", r"机器人|具身智能|物理智能|人形机器人"),
        ("光计算与光载信息", r"光载信息|光通信|光计算|光子|硅光|光芯片|光电"),
        ("第六代移动通信", r"未来网络|6G|通信|卫星互联网|太赫兹"),
        ("脑科学与脑机工程", r"脑机|脑科学|神经|类脑"),
        ("量子科技", r"量子"),
        ("未来能源", r"新能源|氢能|储能|燃料电池|固态电池|核聚变|核电"),
        ("深海矿产", r"深海|深地|海洋|海洋工程|水下"),
    ]
    wh_rows = []
    for nm, pat in WH:
        hit = [c for c in chain_name.values() if c and _re.search(pat, c)]
        hit_codes = [c for c, n in chain_name.items() if n and _re.search(pat, n)]
        wh_rows.append({"category": nm, "matched_chain_names": hit,
                        "matched_chain_codes": hit_codes,
                        "roster_firm_n": sum(1 for f in firms if any(c in hit_codes for c in f["chains"])),
                        "covered": bool(hit_codes)})
    wh_covered = [x["category"] for x in wh_rows if x["covered"]]

    # 派生比值：分子分母都取本件产物内的同名字段，正文只引用这里的结果
    fut_make = next(r for r in cat_rows if r["cluster_id"] == "CL-FUT-01")
    fut_space = next(r for r in cat_rows if r["cluster_id"] == "CL-FUT-04")
    derived = {
        "enterprise_set_with_future_n": len(firms) - dist.get(0, 0),
        "enterprise_set_with_future_pct": pct(len(firms) - dist.get(0, 0), len(firms)),
        "low_altitude_roster_firm_n": fut_space["roster_firm_n"],
        "low_altitude_share_of_roster_pct": pct(fut_space["roster_firm_n"], len(firms)),
        "sensitivity_min_covered_category_n": sens_min,
        "sensitivity_min_covered_ratio_pct": pct(sens_min, 5),
        "counterexample_fut_make_over_roster_pct": pct(fut_make["roster_firm_n"], len(firms)),
        "denominator_note": "enterprise_set_with_future_pct / low_altitude_share_of_roster_pct 的分母是名单 4,561 家；"
                            "sensitivity_min_covered_ratio_pct 的分母是目录 5 类；"
                            "counterexample_* 是错误分母示例（用 4,561 做类级分母），仅用于陷阱说明。",
    }

    # 分母说明：5 是目录类目数，不是企业数；企业侧分母另列
    doc = {
        "metric_id": "M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT",
        "metric_name": "覆盖未来产业数",
        "script": "M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT.py",
        "data_source": "gkx @ 183.240.141.251:3318（只读）",
        "grain": "enterprise_set -> COUNT(DISTINCT future_category_id)",
        "shared_base": {
            "snapshot": "code/_snapshots21/keypano_base_20261023.json",
            "roster_n": len(firms),
            "in_chain_n": kb["stats"]["in_chain_n"],
            "with_stage_n": kb["stats"]["with_stage_n"],
            "chain_n": 12,
            "chain_firm_pairs": idx["stats"]["rows"] - idx["stats"]["empty_link_rows"]
                               - idx["stats"]["bad_credit_rows"],
            "scan_rows": idx["stats"]["rows"],
            "scan_bad_credit_rows": idx["stats"]["bad_credit_rows"],
        },
        "probes": {
            "enterprise_set_n": len(firms),
            "enterprise_set_with_future_n": sum(1 for c in firm_cats.values() if c),
            "covered_category_n": len(covered),
            "covered_category_ids": covered,
            "catalog_category_n": 5,
            "coverage_ratio_pct": pct(len(covered), 5),
            "missing_category": [cid for cid in PROXY if cid not in covered],
            "missing_reason": "CL-FUT-03 未来能源在 12 条链里没有对应链（链目录无能源链），"
                              "不是企业没覆盖，是目录无入口",
            "firm_category_distribution": dist_rows,
            "category_rows": cat_rows,
            "roster_chain_pair_n": sum(r["roster_firm_chain_pairs"] for r in cat_rows),
            "population_chain_firm_pairs": sum(int(v) for v in chain_firms.values()),
            "population_covered_category_n": sum(1 for r in cat_rows if r["covered_by_population"]),
            "sensitivity_drop_one_chain": {
                "tested_n": len(sens),
                "min_covered_category_n": sens_min,
                "rows": sens,
            },

            "wanghui_8_categories": {
                "rule": "王惠 v5.1：对 industry_name 做 REGEXP 归到深圳 20+8 的 8 个未来产业",
                "category_rows": wh_rows,
                "covered_n": len(wh_covered),
                "covered_list": wh_covered,
                "catalog_n": 8,
            },
            "denominator_note": "覆盖率的分子=命中的未来类目数，分母=目录类目数 5；"
                                "4,561 是企业底册，只用于企业侧家数，不作类目覆盖率分母。",
        },
        "derived": derived,
        "probes_negative": {
            "gkx_side": probe["negative_evidence"]["gkx_side"],
            "live_side": probe["negative_evidence"]["live_side"],
            "blocking_table_exist_gkx": probe["db"]["blocking_exist"],
            "cluster_named_columns_gkx": probe["db"]["cluster_columns"],
            "live_counts": probe["db"]["live"],
            "substitute": "12 条链 + 链名语义映射（本报告自拟），无 cluster_id / cluster_group 字段",
            "conclusion": probe["negative_evidence"]["conclusion"],
        },
        "result": {
            "category_rows": cat_rows,
            "firm_category_distribution": dist_rows,
            "covered_category_n": len(covered),
            "coverage_ratio_pct": pct(len(covered), 5),
        },
        "support_judgment": "部分支持",
        "verdict_kind": "negative_evidence",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面件：企业集合与链标签均为当前时点，无年度键；不设基期。",
        "sources": [
            "code/_snapshots21/ent_future_cluster_probe_20261023.json",
            "code/_snapshots21/keypano_base_20261023.json",
            "code/_snapshots21/chain_firm_index_20261023.json",
            "gkx.dwd_org_industry_tags (2,283,762 rows)",
            "gkx.dwd_industry_chain_info (1,273 rows, 12 roots)",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    print("wrote", OUT)
    print("covered", len(covered), covered, "ratio", doc["probes"]["coverage_ratio_pct"])
    print("dist", dist_rows)
    print("sens_min", sens_min)


if __name__ == "__main__":
    main()
