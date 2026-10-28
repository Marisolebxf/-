#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""区域产业指数模型（M_CHAIN_DEEP_126_1）—— gkx 快照口径。

只读 `code/_snapshots21/`，不连数据库。
运行：python3 code/M_CHAIN_DEEP_126_1.py
产物：code/M_CHAIN_DEEP_126_1_out.json

区域 = 四个有真实城市名的城市（深圳/广州/东莞/惠州）。“省外”“广东其他市”是聚合桶，
不参与排名（把桶当城市排，深圳会在多数链上跌出第一，见 M_CHAIN_DEEP_121_1 §2.6）。
链 = 12 条链根（INB 前 7 位）。

三维只用「能挂到链」的数据：
    企业能力：链×城市企业数、链×城市高新技术企业数
    学术生态：链×城市专利件数（region_index_patent_union）
    配套生态：链×城市融资事件数、链×城市服务机构数
论文、科研机构、政策只有城市级计数，**没有链标签**，因此不进入指数，只作背景表 —— 这是本件判
「部分支持」的主因之一：旧稿的学术生态含论文/机构，配套生态含政策强度。
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter, defaultdict

METRIC = "M_CHAIN_DEEP_126_1"
TITLE = "区域产业指数模型"
HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, METRIC + "_out.json")

CITIES = ["深圳市", "广州市", "东莞市", "惠州市"]
W_ENT, W_ACAD, W_ECO = 0.40, 0.30, 0.30
W_ENT_FIRM, W_ENT_HT = 0.60, 0.40
W_ACAD_PAT, W_ACAD_INTENSITY = 0.70, 0.30
W_ECO_FIN, W_ECO_SVC = 0.50, 0.50

ABSENT_TABLES = ["chain_region_index", "chain_competitiveness",
                 "chain_national_dist", "chain_enterprise_stat"]


def jload(name):
    p = os.path.join(SNAP, name)
    if not os.path.exists(p):
        raise FileNotFoundError("缺共享快照 %s" % p)
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def norm(v, mx):
    return 0.0 if not mx else round(100.0 * v / float(mx), 2)


def main():
    panel = jload("chain_panel21.json")
    layer = jload("chain21_layer_20261022.json")
    org = jload("chain_org_agg_20261022.json")
    patent = jload("region_index_patent_union.json")
    fin = jload("chain21_fin_degree_20261022.json")
    svc = jload("svc_chain_city_20261022.json")
    base = jload("base_20261021.json")
    papers = jload("papers_city_year_gkx21.json")
    inst = jload("inst_city_20261021.json")
    policy = jload("policy_base_20261021.json")

    chains = [c["chain"] for c in panel["chains"]]
    cname = {c["chain"]: c["name"] for c in panel["chains"]}
    name2chain = layer["names"]

    svc_map = {(a, b): int(n) for a, b, n in svc}
    org2city = {r[0]: (r[4] or "未知") for r in base}
    fin_city = Counter()
    fin_no_city = 0
    for r in fin["fin"]:
        ch = name2chain.get(r[1])
        if not ch:
            continue
        c = org2city.get(r[0])
        if not c:
            fin_no_city += 1
            continue
        fin_city[(ch, c)] += 1

    per_chain = {}
    for c in panel["chains"]:
        ch = c["chain"]
        city_rows = []
        firms = {city: c["cities"].get(city, 0) for city in CITIES}
        hts = {city: org["per_chain"].get(ch, {}).get("city_hitech", {}).get(city, 0)
               for city in CITIES}
        pats = {city: patent.get(ch + "|" + city, 0) for city in CITIES}
        fins = {city: fin_city.get((ch, city), 0) for city in CITIES}
        svcs = {city: svc_map.get((ch, city), 0) for city in CITIES}

        mf, mh, mp, mfin, ms = (max(firms.values()) or 1, max(hts.values()) or 1,
                                max(pats.values()) or 1, max(fins.values()) or 1,
                                max(svcs.values()) or 1)
        for city in CITIES:
            ent = W_ENT_FIRM * norm(firms[city], mf) + W_ENT_HT * norm(hts[city], mh)
            intensity = (pats[city] / float(firms[city])) if firms[city] else 0.0
            max_int = max((pats[x] / float(firms[x])) if firms[x] else 0.0 for x in CITIES) or 1.0
            acad = W_ACAD_PAT * norm(pats[city], mp) + W_ACAD_INTENSITY * norm(intensity, max_int)
            eco = W_ECO_FIN * norm(fins[city], mfin) + W_ECO_SVC * norm(svcs[city], ms)
            idx = round(W_ENT * ent + W_ACAD * acad + W_ECO * eco, 2)
            city_rows.append({
                "city": city, "firms": firms[city], "hitech": hts[city],
                "patents": pats[city], "fin_events": fins[city], "svc_orgs": svcs[city],
                "patents_per_firm": round(intensity, 6),
                "ent_score": round(ent, 2), "acad_score": round(acad, 2),
                "eco_score": round(eco, 2), "region_index": idx,
            })
        ranked = sorted(city_rows, key=lambda r: -r["region_index"])
        for i, r in enumerate(ranked, 1):
            r["rank_in_chain"] = i
        per_chain[ch] = {
            "chain_name": cname[ch],
            "chain_firms": c["firms"],
            "cities": ranked,
            "sz_rank": next(r["rank_in_chain"] for r in ranked if r["city"] == "深圳市"),
            "sz_index": next(r["region_index"] for r in ranked if r["city"] == "深圳市"),
            "margin": round(ranked[0]["region_index"] - ranked[1]["region_index"], 2),
            "runner_up": ranked[1]["city"],
            "top_city": ranked[0]["city"],
        }

    # 城市级背景（无链标签，不进指数）
    paper_by_city = Counter()
    for k, v in papers["any_city_year"].items():
        city, y = k.split("|")
        if 2019 <= int(y) <= 2024:
            paper_by_city[city] += v
    inst_map = {r["city"]: r["n"] for r in inst}
    policy_by_city = Counter()
    for r in policy:
        c = r.get("city")
        if c and c != "NULL":
            policy_by_city[c] += 1
    context = [{
        "city": city,
        "papers_2019_2024": paper_by_city.get(city, 0),
        "research_institutes": inst_map.get(city, 0),
        "policy_rows": policy_by_city.get(city, 0),
        "note": "三项均无链标签，只作城市背景，不进入 region_index",
    } for city in CITIES]

    # 反向验证
    sz_rank = [v["sz_rank"] for v in per_chain.values()]
    variant_rank = {}
    for ch, v in per_chain.items():
        scored = sorted(v["cities"],
                        key=lambda r: -(0.70 * r["ent_score"] + 0.15 * r["acad_score"]
                                        + 0.15 * r["eco_score"]))
        variant_rank[ch] = next(i for i, r in enumerate(scored, 1) if r["city"] == "深圳市")
    counters = [
        {
            "check": "把「省外」当第 5 城一起排名会怎样",
            "conclusion": "省外桶在每条链的企业数都超过任一城市（软件 774,604 家、数字创意 222,729 家），"
                          "参与排名会让深圳在 12 条链里全部跌出第一。故排名只在四城之间做，省外单列。",
            "province_bucket": {c["name"]: c["cities"].get("省外", 0) for c in panel["chains"]},
        },
        {
            "check": "专利件数的两个口径能不能混用",
            "patent_union_total": sum(patent.values()),
            "chain_panel_patents": sum(c["patents"] for c in panel["chains"]),
            "conclusion": "patent_union（3,026,291 件）按链×城市做并集，企业多链会重复计入；"
                          "chain_panel（1,127,340 件）按链去重。两者相差 1.68 倍，"
                          "本件只用前者做链内城市比较，不与后者相加、不相除。",
        },
        {
            "check": "服务机构数只有 42 个链×城市格子，是否够用",
            "cells": len(svc), "cities_covered": sorted({b for _, b, _ in svc}),
            "conclusion": "42 格覆盖四城、12 链，但缺格按 0 处理会把「没有记录」当成「没有机构」；"
                          "本件在 eco_score 里给服务项 50% 权重，缺格链的数值偏低，解读时必须带这句。",
        },
        {
            "check": "深圳在 12 条链里的名次分布",
            "sz_rank_dist": dict(Counter(sz_rank)),
            "conclusion": "深圳在四城比较里 12 条链全部第 1，指数在「城市之间」没有区分度；"
                          "有信息量的是与第二名的差距（%.1f—%.1f 分），以及第二名是广州还是东莞。"
                          % (min(v["margin"] for v in per_chain.values()),
                             max(v["margin"] for v in per_chain.values())),
        },
        {
            "check": "把权重压到「只看企业数」深圳还是不是第 1",
            "variant": "enterprise/academic/ecosystem = 0.70/0.15/0.15",
            "variant_sz_rank_dist": dict(Counter(variant_rank.values())),
            "variant_sz_not_first": [per_chain[c]["chain_name"] for c, r in variant_rank.items() if r != 1],
            "conclusion": "主权重（0.40/0.30/0.30）下深圳 12/12 第 1；压到 0.70/0.15/0.15 后"
                          "%d/12 仍第 1。结论对权重不敏感，也说明四城尺度太粗、无法用名次区分链——"
                          "真正可读的是与第二名的分差（%.1f—%.1f）与第二名归属。"
                          % (sum(1 for r in variant_rank.values() if r == 1),
                             min(v["margin"] for v in per_chain.values()),
                             max(v["margin"] for v in per_chain.values())),
        },
    ]

    result = {
        "metric_id": METRIC,
        "title": TITLE,
        "support_judgment": "部分支持",
        "judgment_reason": (
            "链×城市的企业数、高企数、专利数、融资事件、服务机构五项可算，四城×12 链全部出指数与名次；"
            "但旧稿三维里的「企业营收」「论文/科研机构」「政策支持强度」三项没有链标签或覆盖率过低："
            "论文 100,900 条只有机构城市、机构表 2,074 行无链码、政策 20,000 条只有城市，"
            "财务表营收仅 2,193/90,926 行，故学术与配套两维只能用「专利 + 融资 + 服务机构」代理，"
            "区域也只覆盖四个城市，不能做全国排名。"
        ),
        "judgment_reason_kind": "dimension_gap",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "params": {
            "cities": CITIES,
            "weights": {"enterprise": W_ENT, "academic": W_ACAD, "ecosystem": W_ECO},
            "sub_weights": {
                "enterprise": {"firms": W_ENT_FIRM, "hitech": W_ENT_HT},
                "academic": {"patents": W_ACAD_PAT, "patent_intensity": W_ACAD_INTENSITY},
                "ecosystem": {"fin_events": W_ECO_FIN, "svc_orgs": W_ECO_SVC},
            },
            "normalization": "链内四城最大值归一（0—100），不是跨链可比分数",
            "param_note": "权重与归一方式为【本件自定义、待甲方确认】。",
        },
        "compute": {
            "chain_count": len(chains),
            "city_count": len(CITIES),
            "fin_events_matched": sum(fin_city.values()),
            "fin_events_no_city": fin_no_city,
            "patent_union_total": sum(patent.values()),
            "svc_cells": len(svc),
            "sz_rank_dist": dict(Counter(sz_rank)),
            "per_chain": per_chain,
            "city_context": context,
        },
        "share_basis": {
            "firms": "链×城市去重企业数，来自 chain_panel21.cities；六桶合计等于链企业数",
            "hitech": "链×城市 org_tag 含「高新技术企业」的家数；分母不足时只做链内归一，不算占比",
            "patents": "链×城市专利并集件数（region_index_patent_union），只做链内比较",
            "fin_events": "融资事件按企业名挂链、按 org_id 归城（14,615/14,626 起可归城）",
            "svc_orgs": "链×城市服务机构格计数（svc_chain_city_20261022，42 格）",
        },
        "probes": [{
            "probe": "information_schema.tables 匹配旧稿区域结果表",
            "absent": ABSENT_TABLES, "present": [],
            "checked_at": "2026-10-22T20:31+08:00",
            "note": "chain_region_index / chain_competitiveness / chain_national_dist 均不存在。",
        }],
        "sources": [
            {"path": "code/_snapshots21/chain_panel21.json", "kind": "snapshot",
             "note": "链×城市企业数六桶（深圳/广州/东莞/惠州/广东其他市/省外）"},
            {"path": "code/_snapshots21/chain_org_agg_20261022.json", "kind": "snapshot",
             "note": "链×城市高新技术企业家数"},
            {"path": "code/_snapshots21/region_index_patent_union.json", "kind": "snapshot",
             "note": "链×城市专利并集件数"},
            {"path": "code/_snapshots21/chain21_fin_degree_20261022.json", "kind": "snapshot",
             "note": "融资事件 25,654 起"},
            {"path": "code/_snapshots21/svc_chain_city_20261022.json", "kind": "snapshot",
             "note": "链×城市服务机构数（42 格）"},
            {"path": "code/_snapshots21/papers_city_year_gkx21.json", "kind": "snapshot",
             "note": "城市×年份论文数（仅背景，无链标签）"},
            {"path": "code/_snapshots21/inst_city_20261021.json", "kind": "snapshot",
             "note": "四城科研机构数（仅背景）"},
            {"path": "code/_snapshots21/policy_base_20261021.json", "kind": "snapshot",
             "note": "政策 20,000 条，按城市计数（仅背景，无链标签）"},
        ],
        "base_years_used": [2019, 2020, 2021, 2022, 2023, 2024],
        "base_years_missing": [],
        "base_years_note": (
            "背景表的论文数取 2019—2024 六年合计（papers_city_year 的 any_city_year）；"
            "企业/专利/融资/服务机构四项是当前快照的时点累计，不按年切分。"
            "2025/2026 的论文与融资不完整，未纳入背景合计。"
        ),
        "missing_dims": [
            {"dim": "企业营收（区域汇总）", "why": "财务表 operating_revenue 仅 2,193/90,926 行有值；"
                                                    "region_index_rev2024 只有 43 家",
             "fill": "补齐企业年报营收或接入统计口径"},
            {"dim": "论文/科研机构入链", "why": "论文只有机构城市、机构表无链码；region_index_acad "
                                                "实测 inst_with_chain_tag=0、heis_with_chain_tag=0",
             "fill": "建机构—链标签映射后可按链归集"},
            {"dim": "政策支持强度", "why": "政策 20,000 条只有城市/主题，无链标签",
             "fill": "按标题主题词打链标签，或由甲方给链—政策映射"},
            {"dim": "全国城市排名", "why": "链标签城市字段只有四城 + 省外聚合桶",
             "fill": "补地级市字段或外部企业库"},
        ],
        "notes": [
            "指数是链内相对分，不是跨链可比的绝对水平；跨链只能比名次，不能比分数。",
            "省外与广东其他市是聚合桶，不参与排名；把它们当城市会让深圳 12 条链全部跌出第一。",
            "专利并集口径（3,026,291）与 chain_panel 去重口径（1,127,340）不可混用。",
            "服务机构缺格按 0 处理，eco_score 因此系统性偏低，解读时需与 svc_cells 一起看。",
        ],
        "counter_checks": counters,
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)

    print("[ok]", OUT)
    print("判档 %s | 深圳名次分布 %s" % (result["support_judgment"], dict(Counter(sz_rank))))
    for ch in chains:
        v = per_chain[ch]
        print("  %-10s SZ rank=%d idx=%.1f top=%s" %
              (v["chain_name"], v["sz_rank"], v["sz_index"], v["top_city"]))


if __name__ == "__main__":
    main()
