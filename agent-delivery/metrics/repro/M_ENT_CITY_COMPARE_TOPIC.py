#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_CITY_COMPARE_TOPIC · 多城市企业群对标值（gkx 单库代理版）

要做什么
--------
需求原文：「将深圳企业群与北京、上海、苏州等城市对比，计算平均技术力、商业力、
企业密度等指标，用户可识别优势与短板」。本指标是三类对标值的容器，不合成总分。

数据事实与一个硬约束
--------------------
`tech_power` / `biz_power` 两张评分结果面在 gkx 都不存在（source_absent，见
TABLE_ABSENCE_EVIDENCE 对应两节）。更关键的是**对标城市不在底册里**：
`dwd_org_base_info` 189,116 家中深圳 95,600、广州 49,605、东莞 33,590、惠州 9,979，
北京只有 163 家、上海 16 家、苏州 0 家。也就是说需求点名的三个对标城市，
本库没有可比样本——不是算法问题，是底册覆盖问题。

本件因此只出「深圳都市圈四市」的对标值，并把北京/上海/苏州的样本量原样列出，
供读者判断「为什么这三个城市进不了对标表」。技术力用专利三维分代理，商业力
无代理（不造），企业密度缺行政区面积分母（只有企业数，不出密度）。

输出：code/M_ENT_CITY_COMPARE_TOPIC_out.json
"""
from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_ENT_CITY_COMPARE_TOPIC_out.json"
METRIC = "M_ENT_CITY_COMPARE_TOPIC"

TARGETS = ["深圳市", "北京市", "上海市", "苏州市", "广州市", "东莞市", "惠州市"]


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def main() -> None:
    base = load("base_20261021.json")
    city_of = defaultdict(int)
    org_city = {}
    for r in base:
        city_of[r[4]] += 1
        org_city[r[0]] = r[4]

    ipc = defaultdict(set)
    pat = defaultdict(int)
    for ipc4, name, c in load("patent_ipc4_by_name_20261021.json"):
        ipc[name].add(ipc4)
        pat[name] += c
    apply24 = {n: int(v[0]) for n, v in load("patent_2024_by_name_20261021.json").items()
               if isinstance(v, list) and v}

    names = [n for n in ipc if pat[n] > 0]
    logs = {n: math.log1p(pat[n]) for n in names}
    brd = {n: len(ipc[n]) for n in names}
    rec = {n: apply24.get(n, 0) / pat[n] for n in names}

    def norm(d):
        lo, hi = min(d.values()), max(d.values())
        span = (hi - lo) or 1.0
        return {k: (v - lo) / span for k, v in d.items()}

    n1, n2, n3 = norm(logs), norm(brd), norm(rec)
    score = {n: 0.5 * n1[n] + 0.3 * n2[n] + 0.2 * n3[n] for n in names}
    name_city = {}
    for r in base:
        name_city[r[2]] = r[4]

    tech = defaultdict(list)
    patents = defaultdict(int)
    for n, s in score.items():
        c = name_city.get(n)
        if c:
            tech[c].append(s)
            patents[c] += pat[n]

    edges = load("ent_edges_20261021.json")
    inv_deg = defaultdict(int)
    for src, dst in edges["invest"]:
        inv_deg[org_city.get(src)] += 1
    for src, dst in edges["shareholder"]:
        inv_deg[org_city.get(src)] += 1

    tagged = defaultdict(int)
    for name, ch in load("chain21_layer_20261022.json")["names"].items():
        c = name_city.get(name)
        if c:
            tagged[c] += 1

    rows = []
    for c in TARGETS:
        n = city_of.get(c, 0)
        rows.append({
            "city": c, "orgs": n,
            "orgs_with_patent": len(tech.get(c, [])),
            "patents": patents.get(c, 0),
            "avg_tech_power": round(sum(tech[c]) / len(tech[c]), 4) if tech.get(c) else None,
            "invest_edges": inv_deg.get(c, 0),
            "invest_per_1k_orgs": round(inv_deg.get(c, 0) / n * 1000, 2) if n else None,
            "chain_tagged_orgs": tagged.get(c, 0),
            "chain_coverage": round(tagged.get(c, 0) / n, 4) if n else None,
            "comparable": n >= 1000,
        })

    comparable = [r for r in rows if r["comparable"]]
    sz = next(r for r in rows if r["city"] == "深圳市")
    topics = []
    for dim, key, higher_better, label in [
        ("技术力", "avg_tech_power", True, "平均技术力（专利三维）"),
        ("企业规模", "orgs", True, "企业底册数量"),
        ("专利强度", "patents", True, "专利总量"),
        ("投资活跃度", "invest_per_1k_orgs", True, "每千家企业的投资/股东关系边数"),
        ("链覆盖", "chain_coverage", True, "有链标签企业占比"),
    ]:
        vals = [(r["city"], r[key]) for r in comparable if r.get(key) is not None]
        if not vals:
            continue
        best = max(vals, key=lambda x: x[1])
        worst = min(vals, key=lambda x: x[1])
        topics.append({
            "dimension": dim, "label": label,
            "shenzhen": sz.get(key),
            "best_city": best[0], "best_value": best[1],
            "worst_city": worst[0], "worst_value": worst[1],
            "gap_to_best": round(sz.get(key) - best[1], 4) if sz.get(key) is not None else None,
            "topic": ("深圳领先" if best[0] == "深圳市" else f"深圳落后 {best[0]}")
                     + f"（{label} {sz.get(key)} vs {best[1]}）",
        })

    out = {
        "metric_id": METRIC,
        "metric_name": "多城市企业群对标值",
        "data_source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）+ code/_snapshots21/ 落盘快照",
        "formula": "city_value = GROUP BY city 的均值/计数；技术力=专利三维分均值；投资活跃度=关系边/千家企业",
        "blocking_tables": {
            "tech_power": {"triage": "source_absent",
                           "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §tech_power"},
            "biz_power": {"triage": "source_absent",
                          "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §biz_power"},
        },
        "proxy_path": "专利三维分（技术力）+ 关系边密度（投资活跃度）+ 标签覆盖率（链覆盖）",
        "proxy_deviation": "商业力维无任何代理（不造）；企业密度缺行政区面积分母，只出企业数；需求点名的北京/上海/苏州在底册只有 163/16/0 家，不可比，故对标表实际只含深圳都市圈四市",
        "benchmark_availability": {
            "targets": TARGETS,
            "orgs_in_base": {r["city"]: r["orgs"] for r in rows},
            "comparable_threshold": 1000,
            "missing_targets": [r["city"] for r in rows if not r["comparable"]],
        },
        "cities": rows,
        "topics": topics,
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": "三类对标值里两类有代理（技术力→专利三维分均值、投资活跃度→关系边密度），企业密度只能出企业数（缺面积分母），商业力整维无源。更硬的约束是对标城市：北京 163 家、上海 16 家、苏州 0 家，需求点名的三个城市在本库不可比，对标只能落在深圳都市圈四市。两维可算、一维缺分母、一维整缺、对标集不完整，判部分支持。",
            "criteria": {
                "target_cities": len(TARGETS),
                "comparable_cities": len(comparable),
                "dims_with_proxy": 2, "dims_missing": 2,
                "proxy_used": True,
            },
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "本件是截面城市对标（当前底册时点），不是年度序列，故无基期年份；底册不带历史版本，无法做「某年对标」。专利侧年份窗口 2021—2024 仅影响专利计数口径，不构成城市对标的基期。",
        "sources": [
            {"path": "code/_snapshots21/base_20261021.json",
             "table": "gkx.dwd_org_base_info", "rows": 189116, "role": "城市归属与企业数"},
            {"path": "code/_snapshots21/patent_ipc4_by_name_20261021.json",
             "table": "gkx.dwd_patent", "rows": 581585, "role": "技术力与专利强度"},
            {"path": "code/_snapshots21/ent_edges_20261021.json",
             "table": "gkx.dwd_org_invest_info + gkx.dwd_org_shareholder_info",
             "rows": 117001, "role": "投资活跃度"},
            {"path": "code/_snapshots21/chain21_layer_20261022.json",
             "table": "gkx.dwd_org_industry_tags", "rows": 36993, "role": "链覆盖率"},
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[OK] {METRIC} -> {OUT.name} comparable={len(comparable)}/{len(TARGETS)}")
    for r in rows:
        print(f"  {r['city']:<5} orgs={r['orgs']:<7} patent_orgs={r['orgs_with_patent']:<6} "
              f"tech={r['avg_tech_power']} inv/k={r['invest_per_1k_orgs']} chain={r['chain_coverage']}")
    for t in topics:
        print("  topic:", t["topic"])


if __name__ == "__main__":
    main()
