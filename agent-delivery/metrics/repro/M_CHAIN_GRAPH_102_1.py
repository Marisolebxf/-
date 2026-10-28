#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""产业实体识别构建（M_CHAIN_GRAPH_102_1）—— 六类实体规模与链挂接，自包含。

实体类别按需求口名的六类（旧稿 §2.2 同名单）：
    企业、高等院校、科研机构、人才、政策、专利。
六类源表行数取 gkx 的 COUNT(*) 实测（2026-10-22，见 _work_gkx21/GKX_INVENTORY.json），
本脚本只读本地快照与常量，不连库。

链挂接只对「企业」和「专利」成立：
    企业 → 标签表 industry_code；专利 → 申请人名称经标签表 names 桥回链。
高校、科研机构、人才、政策四类没有链级关系面（无 chain_id / industry_code 列），
因此只报总量、不报链级值，链挂接覆盖率为 2/6。

产物：entities[] 六类规模；chain_link 挂接率；chains[] 该链企业+专利实体数。

运行：cd code && python3 M_CHAIN_GRAPH_102_1.py
产物：code/M_CHAIN_GRAPH_102_1_out.json（覆盖写）
"""
from __future__ import annotations

import json
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_GRAPH_102_1_out.json")

BASE_USED = []
BASE_MISSING = []
BASE_NOTE = '截面指标：统计当前存量，不设年度分母。'

SOURCES = [
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_org_base_info", "rows": 189116,
     "snapshot": "code/_snapshots21/base_20261021.json"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_org_heis_info", "rows": 3501, "snapshot": None},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_research_institute_base_info", "rows": 2074, "snapshot": None},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_scholar", "rows": 21316, "snapshot": None},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_policy_base", "rows": 20000,
     "snapshot": "code/_snapshots21/policy_base_20261021.json"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_patent", "rows": 2939895,
     "snapshot": "code/_snapshots21/patent_panel_innov_20261021.json"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_org_industry_tags", "rows": 2283762,
     "snapshot": "code/_snapshots21/chain_panel21.json"},
]

# gkx COUNT(*) 实测（2026-10-22，GKX_INVENTORY.json 同值）
ENTITY_ROWS = [
    ("企业", 189116, True, "gkx.dwd_org_base_info", "属性完整底册；另有 2,283,762 行标签企业可挂链"),
    ("高等院校", 3501, False, "gkx.dwd_org_heis_info", "无 chain_id / industry_code 列"),
    ("科研机构", 2074, False, "gkx.dwd_research_institute_base_info", "无 chain_id / industry_code 列"),
    ("人才", 21316, False, "gkx.dwd_scholar", "机构名字段可做弱挂接，但无链码"),
    ("政策", 20000, False, "gkx.dwd_policy_base", "无 industry_code 列（字段清单实测）"),
    ("专利", 2939895, True, "gkx.dwd_patent", "申请人名称经标签表 names 桥回链"),
]


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    t0 = time.time()
    panel = load("chain_panel21.json")
    chains = panel["chains"]
    base = load("base_20261021.json")

    # 底册六字段填充率（企业实体的属性完整度，全部由快照现算）
    cols = ["org_id", "credit_code", "name", "province", "city", "year"]
    attr_fill = {}
    for i, c in enumerate(cols):
        n = sum(1 for r in base if r[i] not in (None, "", "NULL", "None"))
        attr_fill[c] = {"filled": n, "total": len(base), "rate": round(n / len(base), 6)}

    entities = [
        {"entity": e, "rows": n, "chain_linkable": lk, "source": src, "note": note}
        for e, n, lk, src, note in ENTITY_ROWS
    ]
    total_entities = sum(e["rows"] for e in entities)
    linkable = [e["entity"] for e in entities if e["chain_linkable"]]

    tag_rows = 2283762
    firms_attributed = sum(c["firms"] for c in chains)
    patents_attributed = sum(c.get("patents", 0) for c in chains)
    patent_firms = sum(c.get("patent_firms", 0) for c in chains)

    rows = []
    for c in chains:
        rows.append({
            "chain": c["chain"], "name": c["name"],
            "value": c["firms"] + c.get("patents", 0),
            "firms": c["firms"], "patents": c.get("patents", 0),
            "patent_firms": c.get("patent_firms", 0),
            "nonleaf": None, "leaves": None, "l1": None,
        })
    rows.sort(key=lambda r: -r["value"])

    chain_link = {
        "enterprise": {
            "universe": tag_rows, "attributed": firms_attributed,
            "rate": round(firms_attributed / tag_rows, 6),
            "note": "按 industry_code 首个 INB 码归链（互斥口径），故小于关联口径的 2,464,659 链位",
        },
        "patent": {
            "universe": 2939895, "attributed": patents_attributed,
            "rate": round(patents_attributed / 2939895, 6),
            "patent_firms": patent_firms,
            "note": "申请人名称必须先在标签表出现才能桥回链；未出现的长尾申请人不计入",
        },
        "unlinkable": ["高等院校", "科研机构", "人才", "政策"],
        "linkable_classes": len(linkable),
        "classes": len(entities),
    }

    headline = {
        "value": total_entities,
        "unit": "条实体记录（六类源表合计）",
        "entity_classes": len(entities),
        "chain_linkable_classes": len(linkable),
        "enterprise_rows": 189116,
        "tagged_enterprise_rows": tag_rows,
    }
    facts = [
        {"label": "六类实体合计", "value": f"{total_entities:,}"},
        {"label": "可挂链实体类", "value": f"{len(linkable)}/{len(entities)}"},
        {"label": "企业主档 / 标签企业", "value": f"189,116 / {tag_rows:,}"},
        {"label": "企业挂链率", "value": f"{chain_link['enterprise']['rate']*100:.2f}%"},
        {"label": "专利挂链率", "value": f"{chain_link['patent']['rate']*100:.2f}%"},
    ]

    out = {
        "metric_id": "M_CHAIN_GRAPH_102_1",
        "metric_name": "产业实体识别构建",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": (
            "六类实体在 gkx 均有源表且量足（3,175,902 条：企业 189,116、高校 3,501、"
            "科研机构 2,074、人才 21,316、政策 20,000、专利 2,939,895）；但只有企业与专利"
            "存在链级挂接面（企业走 industry_code、专利走申请人名称桥，挂链率 75.07% / 38.35%），"
            "高校、科研机构、人才、政策四类没有 chain_id 或 industry_code，"
            "链挂接只能覆盖 2/6，故判部分支持。"
        ),
        "sources": SOURCES,
        "base_years_used": BASE_USED,
        "base_years_missing": BASE_MISSING,
        "base_years_note": BASE_NOTE,
        "headline": headline,
        "facts": facts,
        "entities": entities,
        "attr_fill": attr_fill,
        "chain_link": chain_link,
        "chains": rows,
        "method_steps": [
            "按需求口名的六类实体逐一盘点 gkx 源表行数（COUNT(*) 实测）",
            "计算企业实体的六字段属性填充率（底册 189,116 行）",
            "对企业按标签表 industry_code 归链、对专利按申请人名称桥回链",
            "四类无链级关系面的实体只报总量，不计入链挂接覆盖",
            "输出六类实体规模、链挂接率与逐链实体数",
        ],
        "population": {
            "defined_as": "gkx 六类实体源表可识别行数",
            "entities": entities,
            "chain_linkable": linkable,
        },
        "compute": {
            "formula": "COUNT(*) per entity class；链级 = 企业 + 专利",
            "chain_link_rule": "企业走 industry_code 首码，专利走申请人名称桥",
            "excluded_from_chain": ["高等院校", "科研机构", "人才", "政策"],
        },
        "gaps": [
            "高校、科研机构、人才、政策四类无链级关系面：只能给实体总量，不能给逐链值",
            "专利挂链依赖申请人名称与标签表names交集，2,939,895 件中只有 1,127,340 件（38.35%）可归链",
            "底册 189,116 家只覆盖标签企业 2,283,762 家的 8.28%，属性完整度只在底册子集内成立",
            "实体识别结果发布面（旧稿所述 512 行）在 gkx 无对应表，本件只验原料侧，不验成品库",
        ],
        "difference_vs_old_draft": {
            "old_source": "演示库实体关系表（表名前缀 demo_，主机 111.198.38.90）512 行 + 旧脚本静态常量",
            "old_note": "旧稿把六类写成企业/高校/科研机构/人才/政策/专利，但把链级值折算成企业+专利+资讯，实体类别与链级口径混用",
            "now_source": "gkx 六表 COUNT(*) 实测 + code/_snapshots21/chain_panel21.json",
            "direction": "本件链级值只含企业与专利（两类有链键），不再把资讯计入实体；总量 3,175,902 与旧稿 317 万一致",
        },
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("[ok]", "M_CHAIN_GRAPH_102_1", json.dumps(headline, ensure_ascii=False),
          "chains", len(rows), "linkable", len(linkable), "sec", round(time.time() - t0, 2))


if __name__ == "__main__":
    main()
