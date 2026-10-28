#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_GLOBAL_CASE_MATCH · 全球成功案例匹配（gkx 单库·无案例库版）

定义（王惠表 AI 补漏条目）
--------------------------
给定一条本地产业链，从全球范围找「同构且成功」的案例，输出案例名、所在国家/区域、
案例的产业结构、与本地链的匹配度。三件事缺一不可：案例库、案例的产业结构标签、
「成功」的判定依据。

为什么判「完全不支持」
----------------------
1) 没有任何案例库。全库 280 张表里没有 case / benchmark / best_practice 类表，
   `chain_stage`、`chain_cycle`（本指标在 TABLE_TRIAGE 里挂的两张阻塞表）都不存在。
2) 唯一的「境外」实体是外资企业名录 `dwd_forg_*`（6 张，各 20,000 行，国家以 GB 为主），
   但外资名录与链标签体系**零重叠**：forg_extid_in_tags=0、forg_name_in_tags=0、
   forg_orgid_overlap_base=0。也就是说这 2 万家境外主体挂不上任何一条产业链。
3) 「成功」没有判定依据。库内没有案例级的营收/份额/增长率/存续状态序列，
   无法区分「成功案例」与「普通企业」。
4) 专利侧只有国家码（CN 2,848,905 / WO 89,935 / HK 952 / JP 79 / TW 20 / MO 4），
   能说明「技术产出在哪些国家」，不能构成「区域成功案例」。

按本批规则：无案例库 + 无链归属 + 无成功判据，判完全不支持，只写需求与恢复路径。
不做「拿外资企业当案例」的代理——名录不是案例，没有产业匹配度，也没有成功标签。

输出：code/M_CHAIN_GLOBAL_CASE_MATCH_out.json
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_CHAIN_GLOBAL_CASE_MATCH_out.json"
METRIC = "M_CHAIN_GLOBAL_CASE_MATCH"

REQUIRED = [
    ("case_id", "案例稳定主键"),
    ("case_name", "案例名（区域/集群/企业）"),
    ("country", "所在国家/地区"),
    ("case_chain_code", "案例所属产业链（可多值）"),
    ("case_structure", "案例的产业结构向量（环节占比）"),
    ("success_basis", "成功判据（份额/增速/存续/就业等）"),
    ("success_year", "成功判据对应年份"),
    ("match_score", "与本地链的匹配度"),
    ("source_ref", "案例出处（报告/数据库/文献）"),
]


def main() -> None:
    intl = json.loads((SNAP / "chain_intl_gkx_20261021.json").read_text(encoding="utf-8"))
    inv = json.loads((HERE.parent / "_work_gkx21" / "GKX_INVENTORY.json").read_text(encoding="utf-8"))
    panel = json.loads((SNAP / "chain_panel21.json").read_text(encoding="utf-8"))

    # 全库搜「案例/对标」类表
    kw_tables = {t: v for t, v in inv.items()
                 if any(k in t.lower() for k in ("case", "benchmark", "practice", "best"))}
    # 境外表
    forg_tables = {t: v for t, v in inv.items() if "forg" in t.lower() or "foreign" in t.lower()}

    field_audit = []
    for k, why in REQUIRED:
        field_audit.append({
            "field": k, "why": why,
            "in_gkx": False,
            "note": "全库无案例库，字段无处挂载" if k not in ("country",) else "只有专利国家码，无案例国家",
        })

    out = {
        "metric_id": METRIC,
        "metric_name": "全球成功案例匹配",
        "data_source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）+ code/_snapshots21/ 落盘快照",
        "formula": "match(本地链, 全球案例) = 产业结构余弦相似度 × 成功判据过滤；本件缺案例库与成功判据",
        "blocking_tables": {
            "chain_stage": {"triage": "source_absent",
                            "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §chain_stage"},
            "chain_cycle": {"triage": "source_absent",
                            "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §chain_cycle"},
        },
        "table_search": {
            "inventory_tables": len(inv),
            "case_like_tables": sorted(kw_tables) or [],
            "foreign_like_tables": sorted(forg_tables) or [],
            "trade_like_tables": intl["trade_tables_gkx"],
        },
        "foreign_entities": {
            "forg_rows": intl["forg_rows"],
            "country_dist": intl["forg_country"],
            "industry_class": intl["forg_industry_type"],
            "overlap_with_chain_tags": {
                "forg_extid_in_tags": intl["forg_extid_in_tags"],
                "forg_name_in_tags": intl["forg_name_in_tags"],
                "forg_orgid_overlap_base": intl["forg_orgid_overlap_base"],
            },
        },
        "patent_country": intl["patent_country"],
        "local_chains": [{"chain": c["chain"], "name": c["name"]} for c in panel["chains"]],
        "field_audit": field_audit,
        "why_not_proxy": [
            "外资企业名录不是案例：没有产业匹配度、没有成功判据、没有案例级结果指标",
            "外资名录与链标签零重叠（三项 overlap 全 0），连「案例属于哪条链」都答不出",
            "专利国家码只能说明技术产出国别，不能构成「区域成功案例」",
            "新闻里的「某国某产业成功」是叙述文本，没有结构化产业结构，无法算匹配度",
        ],
        "requirements": {
            "case_library": "案例主表：case_id / 区域 / 国家 / 产业结构向量 / 成功判据 / 年份 / 出处",
            "chain_link": "案例→链的多值映射表（案例侧产业分类需对齐 INB 12 链）",
            "success_rule": "成功判据：全球份额、增速、存续年限、就业/产值中至少两项",
            "acceptance": "每条链至少 5 个可核验案例、每个案例有 ≥1 条出处，才能出匹配度",
        },
        "support_judgment": {
            "data_support_level": "完全不支持",
            "reason": "全库没有案例库（280 张表里 case/benchmark 类为 0），唯一境外实体是外资企业名录 6 张各 2 万行，但它与链标签零重叠（extid/name/orgid 三项命中均为 0），挂不上任何一条链；「成功」没有判据表，案例级营收/份额/增速序列都不存在。案例库、链归属、成功判据三项全缺，无法闭环，判完全不支持。",
            "criteria": {
                "case_library_exists": False,
                "case_chain_link_exists": False,
                "success_rule_exists": False,
                "foreign_entities": 20000,
                "foreign_chain_overlap": 0,
                "proxy_used": False,
            },
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "没有案例库就没有案例年份；本件不产出任何年度序列，used/missing 为空表示「无时间维可挂」，不是「缺年补 0」。",
        "sources": [
            {"path": "code/_snapshots21/chain_intl_gkx_20261021.json",
             "table": "gkx.dwd_forg_* + gkx.dwd_patent", "rows": 120043,
             "role": "境外主体与专利国别取证"},
            {"path": "_work_gkx21/GKX_INVENTORY.json", "rows": 280,
             "role": "全库表清单，确认无案例类表"},
            {"path": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md",
             "role": "§chain_stage / §chain_cycle 证据块"},
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[OK] {METRIC} -> {OUT.name} case_like={len(kw_tables)} "
          f"forg_chain_overlap={intl['forg_name_in_tags']} fields_missing={len(field_audit)}")


if __name__ == "__main__":
    main()
