#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""产业实体关系抽取（M_CHAIN_GRAPH_103_1）—— 按需求六族逐族核，自包含。

需求口名的六族是：产业—技术、产业—企业、产业—人才、产业—科研机构、
产业—服务机构、产业—政策。本件逐族核 gkx 是否有链级关系面，能算的真算：

    ① 产业—企业：tags 表 industry_code 首码归链 → 1,714,458 条（互斥口径）；
    ② 产业—技术：专利申请人名称经 tags 的 names 桥回链 → 29,631 个企业—链对
       （对应专利 1,127,340 件，作为边的属性列出，不重复计入边数）；
    ③ 产业—人才：dwd_scholar 无链码 → 0；
    ④ 产业—科研机构：dwd_research_institute_base_info 无链码 → 0；
    ⑤ 产业—服务机构：gkx 无服务机构主档 → 0；
    ⑥ 产业—政策：dwd_policy_base 无 industry_code（字段清单实测）→ 0。

另附「企业—资本」14,626 条：gkx 有融资事件源、也能桥回链，但它不在需求六族内，
只作补充族列出，不计入六族覆盖率。边数不是「已发布关系库规模」，是当前可抽取量。

产物：families[] 六族；supplementary[] 补充族；chains[] 逐链可抽取边。

运行：cd code && python3 M_CHAIN_GRAPH_103_1.py
产物：code/M_CHAIN_GRAPH_103_1_out.json（覆盖写）
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_GRAPH_103_1_out.json")

BASE_USED = []
BASE_MISSING = []
BASE_NOTE = '截面指标：统计当前存量，不设年度分母。'

SOURCES = [
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_org_industry_tags", "rows": 2283762,
     "snapshot": "code/_snapshots21/chain_panel21.json"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_patent", "rows": 2939895,
     "snapshot": "code/_snapshots21/patent_panel_innov_20261021.json"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_org_financing_info", "rows": 25654,
     "snapshot": "code/_snapshots21/chain21_fin_degree_20261022.json"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_scholar", "rows": 21316, "snapshot": None},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_research_institute_base_info", "rows": 2074, "snapshot": None},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_policy_base", "rows": 20000,
     "snapshot": "code/_snapshots21/policy_base_20261021.json"},
]


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    t0 = time.time()
    panel = load("chain_panel21.json")
    chains = panel["chains"]
    layer = load("chain21_layer_20261022.json")
    name_chain = layer["names"]
    fin = load("chain21_fin_degree_20261022.json")

    inv_by_chain = Counter()
    fin_events_total = len(fin.get("fin", []))
    for r in fin.get("fin", []):
        c = name_chain.get(r[1])
        if c:
            inv_by_chain[c] += 1

    rows = []
    for c in chains:
        code = c["chain"]
        e_firm = c["firms"]
        e_tech = c.get("patent_firms", 0)
        e_cap = inv_by_chain.get(code, 0)
        rows.append({
            "chain": code, "name": c["name"],
            "value": e_firm + e_tech,
            "industry_firm": e_firm, "industry_tech": e_tech,
            "patents": c.get("patents", 0), "firm_capital_supp": e_cap,
            "nonleaf": None, "leaves": None, "l1": None,
        })
    rows.sort(key=lambda r: -r["value"])

    firm_edges = sum(r["industry_firm"] for r in rows)
    tech_edges = sum(r["industry_tech"] for r in rows)
    cap_edges = sum(r["firm_capital_supp"] for r in rows)

    families = [
        {"family": "产业—企业", "edges": firm_edges, "available": True,
         "source": "gkx.dwd_org_industry_tags（industry_code 首码）",
         "note": "2,283,762 行中 1,714,458 行首码落在 12 条顶层链内（75.07%）"},
        {"family": "产业—技术", "edges": tech_edges, "available": True,
         "source": "gkx.dwd_patent 申请人名称 → tags.names 桥",
         "note": "29,631 个企业—链对；对应专利 1,127,340 件，名称未命中标签表的申请人无法归链"},
        {"family": "产业—人才", "edges": 0, "available": False,
         "source": "gkx.dwd_scholar（21,316 行）", "note": "无 chain_id / industry_code，不能定边"},
        {"family": "产业—科研机构", "edges": 0, "available": False,
         "source": "gkx.dwd_research_institute_base_info（2,074 行）", "note": "无链码，不能定边"},
        {"family": "产业—服务机构", "edges": 0, "available": False,
         "source": "gkx 无服务机构主档", "note": "源表缺失"},
        {"family": "产业—政策", "edges": 0, "available": False,
         "source": "gkx.dwd_policy_base（20,000 行）", "note": "无 industry_code，不能定边"},
    ]
    families_available = sum(1 for f in families if f["available"])
    total_edges = firm_edges + tech_edges

    headline = {
        "value": total_edges,
        "unit": "条可抽取关系边（六族中 2 族）",
        "families_available": families_available,
        "families_required": len(families),
        "firm_edges": firm_edges,
        "tech_edges": tech_edges,
    }
    facts = [
        {"label": "六族中可实现", "value": f"{families_available}/{len(families)}"},
        {"label": "可抽取边合计", "value": total_edges},
        {"label": "产业—企业边", "value": firm_edges},
        {"label": "产业—技术边（企业—链对）", "value": tech_edges},
        {"label": "补充：企业—资本边", "value": cap_edges},
    ]

    out = {
        "metric_id": "M_CHAIN_GRAPH_103_1",
        "metric_name": "产业实体关系抽取",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": (
            "需求点名的六族关系中，只有「产业—企业」（1,714,458 条）与「产业—技术」"
            "（29,631 个企业—链对，经专利申请人名称桥）可由 gkx 现算；"
            "产业—人才、产业—科研机构、产业—服务机构、产业—政策四族在 gkx 均无链码"
            "（源表有行数但没有 chain_id / industry_code），六族只能覆盖 2/6，故判部分支持。"
        ),
        "sources": SOURCES,
        "base_years_used": BASE_USED,
        "base_years_missing": BASE_MISSING,
        "base_years_note": BASE_NOTE,
        "headline": headline,
        "facts": facts,
        "families": families,
        "supplementary": [
            {"family": "企业—资本", "edges": cap_edges, "available": True,
             "source": "gkx.dwd_org_financing_info（25,654 行）被投企业名称→链",
             "note": "不在需求六族内，不计入 2/6 覆盖率；"
                     f"25,654 条融资事件中 {cap_edges} 条被投企业可桥回链"},
            {"family": "企业—地域", "edges": None, "available": False,
             "source": "gkx.dwd_org_base_info.city + credit_code 属地桶",
             "note": "只能给 6 个城市桶，不是城市个数；桶数对每条链恒为 6，不能当边数"},
        ],
        "chains": rows,
        "methods": {
            "family_check": "逐族检查源表是否有链码列；无链码即计 0，不以名称相似度硬凑",
            "edge_unit": "企业—链对（不是事件行）；专利件数只作属性",
            "exclusive_rule": "产业—企业按 industry_code 首个 INB 码归链，12 链求和 1,714,458，"
                              "小于关联口径 2,464,659，差额为多链企业的次级链位",
        },
        "population": {
            "defined_as": "六族关系中 gkx 有链码可定边的实体对",
            "families": families,
            "financing_events": fin_events_total,
        },
        "compute": {
            "formula": "Σ edges per family；families_available = COUNT(available)",
            "families": len(families),
            "missing": [f["family"] for f in families if not f["available"]],
        },
        "gaps": [
            "产业—人才无链码：dwd_scholar 21,316 行只有机构名，不能定「人才—链」边",
            "产业—科研机构无链码：2,074 行院所主档没有 industry_code",
            "产业—政策无链码：政策全表 20,000 行只有标题/发文机关/地区，无产业标签",
            "产业—服务机构源表缺失：gkx 无服务机构主档",
            "产业—技术为名称桥：2,939,895 件专利中只有 1,127,340 件（38.35%）可归链",
            "旧稿所称 217,206 条企业—链边、85,369 条供应边来自演示库关系表，gkx 无同源表，不可复用",
        ],
        "difference_vs_old_draft": {
            "old_source": "演示库关系表（表名前缀 demo_，主机 111.198.38.90）：industry_chain_entity_rel 512 行、enterprise_industry_chain 217,206 行、enterprise_supply_chain 85,369 行",
            "old_note": "旧稿六族里只有「产业—企业」算有源，人才/科研机构/服务机构/政策四族无链级面；"
                        "本件用 gkx 专利名称桥把「产业—技术」补成可算，故覆盖率从 1/6 升到 2/6",
            "now_source": "gkx.dwd_org_industry_tags + gkx.dwd_patent + gkx.dwd_org_financing_info",
            "direction": "本件边数全部来自 gkx 现算；旧稿 217,206 条关系边无法在 gkx 复现，故不可相减",
        },
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("[ok]", "M_CHAIN_GRAPH_103_1", json.dumps(headline, ensure_ascii=False),
          "chains", len(rows), "sec", round(time.time() - t0, 2))


if __name__ == "__main__":
    main()
