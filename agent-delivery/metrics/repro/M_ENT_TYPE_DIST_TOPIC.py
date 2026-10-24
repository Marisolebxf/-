#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_TYPE_DIST_TOPIC 重点企业类型分布（20261021 改源版）。

口径正本：gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_TYPE_DIST_TOPIC.md
  先 M_ENT_KEY_TOTAL（专利总量 >=50）取名单，再按招标四类
  foreign / high_tech / sme / listed 分组，出 COUNT + 占比 + 环比。

本件只读快照，不连数据库：
  - 名单代理用 star_roster_gkx_20261021.json（4,561 家，授权 >=50）；
  - high_tech / sme 走 tech_tags_20261021.json；listed 走 dwd_org_stock_base 的 org_id 集合；
  - foreign 无 tag_code，只有工商登记类型文本（org_type），作旁证不作主口径；
  - 无 stat_year，环比不可算。
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _w13e3_common as C

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "M_ENT_TYPE_DIST_TOPIC_out.json")
ID = "M_ENT_TYPE_DIST_TOPIC"


def main():
    t = C.type_panel()
    probe = C.load("w13e3_probe_20261023.json")
    ch = C.chain_panel()
    n = t["roster_n"]

    types = [
        {"tag_code": "high_tech", "name": "高新技术企业", "n": t["high_tech_n"],
         "share_pct": C.pct(t["high_tech_n"], n, 2), "source": "dwd_org_tech_tag（org_tag 含「高新技术企业」）",
         "available": True},
        {"tag_code": "sme", "name": "科技型中小企业", "n": t["sme_n"],
         "share_pct": C.pct(t["sme_n"], n, 2), "source": "dwd_org_tech_tag（org_tag 含「科技型中小企业」；calc-logic 的 sme 类）",
         "available": True},
        {"tag_code": "listed", "name": "上市企业", "n": t["listed_n"],
         "share_pct": C.pct(t["listed_n"], n, 2), "source": "dwd_org_stock_base（org_id 命中；含申报稿/终止，非仅正常上市）",
         "available": True},
        {"tag_code": "foreign", "name": "外资企业", "n": 0,
         "share_pct": 0.0, "source": "无 tag_code；仅 org_type 工商登记类型，226 家为文本旁证",
         "available": False, "text_proxy_n": t["foreign_orgtype_n"],
         "text_proxy_share_pct": C.pct(t["foreign_orgtype_n"], n, 2)},
    ]

    overlap = [
        {"pair": "high_tech ∩ sme", "n": t["hi_sme"], "pct_of_roster": C.pct(t["hi_sme"], n, 2)},
        {"pair": "high_tech ∩ listed", "n": t["hi_listed"], "pct_of_roster": C.pct(t["hi_listed"], n, 2)},
        {"pair": "sme ∩ listed", "n": t["sme_listed"], "pct_of_roster": C.pct(t["sme_listed"], n, 2)},
        {"pair": "high_tech ∩ sme ∩ listed", "n": t["all3"], "pct_of_roster": C.pct(t["all3"], n, 2)},
    ]

    result = {
        "key_list": {
            "declared": "M_ENT_KEY_TOTAL：专利总量 >= 50 的重点企业",
            "implemented": "star_roster_gkx_20261021：授权 >= 50 的明星企业 4,561 家",
            "n": n,
            "grant_min": t["roster_grant_min"],
            "grant_sum": t["roster_grant_sum"],
            "key_total_ge50_assignees": t["key_total_ge50"],
            "key_total_minus_roster": (t["key_total_ge50"] - n) if t["key_total_ge50"] else None,
            "why_substituted": "KEY_TOTAL 的 6,917 是受让人口径（总量 >=50），含高校院所且未全部映射 org_id；"
                                "名单要按 org_id 与标签/上市主档连接，故用已交付的 4,561 家名单代理。",
        },
        "types": types,
        "four_type_sum": t["high_tech_n"] + t["sme_n"] + t["listed_n"] + t["foreign_orgtype_n"],
        "four_type_sum_pct": t["sum_four_pct"],
        "non_exclusive_note": "四类不是互斥分类：一企可同时是高企、科技型中小、上市、外资；计位和可以超过名单家数。",
        "overlap": overlap,
        "union_three_available": t["union3"],
        "union_three_share_pct": C.pct(t["union3"], n, 2),
        "none_three": t["none3"],
        "none_three_share_pct": C.pct(t["none3"], n, 2),
        "extra_tags_not_in_four": {
            "专精特新": {"n": t["zx_n"], "share_pct": C.pct(t["zx_n"], n, 2)},
            "小巨人": {"n": t["little_giant_n"], "share_pct": C.pct(t["little_giant_n"], n, 2)},
            "创新型中小企业": {"n": t["innovative_n"], "share_pct": C.pct(t["innovative_n"], n, 2)},
            "note": "这三类不在本条四类里；小巨人是专精特新的子集，不能与四类相加。",
        },
        "micro_size_probe": {
            "n": t["micro_n"],
            "share_pct": C.pct(t["micro_n"], n, 2),
            "unknown_size_n": t["unknown_size_n"],
            "source": "dwd_org_base_info.org_size ∈ {小型, 微型}",
            "usable_for_this_metric": False,
            "why": "calc-logic 明令禁止用 org_size 替代 sme；本条 sme 是「科技型中小企业」标签，"
                   "与需规原文「小微（注册资本+员工人数）」不是同一个分类。此探针只用于量化口径差异，不参与四类计数。",
            "base_level_n": 125477,
            "base_level_share_pct": 66.35,
        },
        "stat_year_available": False,
        "yoy_available": False,
        "yoy_note": "标签表无 stat_year，名单是单期快照；上年同格不存在，环比记空，不按 0 摊入。",
        "tag_table": {
            "rows": 202424,
            "orgs": t["tag_orgs"],
            "note": "dwd_org_tech_tag 202,424 行 / 32,322 家；标签是多值，非互斥。",
        },
        "listed_source": {
            "stock_base_rows": t["stock_base_rows"],
            "stock_base_orgs": t["stock_base_orgs"],
            "stock_type_dist": t["stock_type_dist"],
            "listing_status_dist": t["listed_status_dist"],
            "normal_listed_rows": t["listed_status_dist"].get("正常上市"),
            "note": "975 家是 stock_base 去重主体；其中正常上市 646 行，申报稿 310、终止 35、*ST/ST 22。"
                    "本件 listed 取 975 家集合与名单的交集 425 家，未再按状态细分。",
        },
        "foreign_proxy": {
            "tag_code_available": False,
            "gkx_column_hits": {
                "foreign_investment": probe["A_schema_scan"]["columns"]["column_hits"]["foreign_investment"],
                "is_foreign": probe["A_schema_scan"]["columns"]["column_hits"]["is_foreign"],
            },
            "org_type_text_n": t["foreign_orgtype_n"],
            "org_type_text_share_pct": C.pct(t["foreign_orgtype_n"], n, 2),
            "text_keywords": ["外商投资", "中外合资", "中外合作", "外国"],
            "usable_as_tag": False,
            "why": "org_type 是工商登记企业类型，不是 foreign 标签；可作旁证，不能与 high_tech/sme/listed 同权。",
        },
        "industry_filter": {
            "declared": "选产业经 enterprise_industry_chain",
            "local_name_match_rows": ch["base_matched_names"],
            "local_name_match_share_pct": ch["base_matched_share_pct"],
            "note": "名单内的产业过滤需按 credit_code 连接链归属表；本地快照只能按名对齐 11.63%。",
        },
        "roster_city_top": {},
    }

    # 名单城市分布（底册城市字段）
    from collections import Counter
    roster = C.load("star_roster_gkx_20261021.json")["rows"]
    cc = Counter((r.get("city") or "（空）") for r in roster)
    result["roster_city_top"] = [{"city": k, "n": v, "share_pct": C.pct(v, n, 2)}
                                 for k, v in cc.most_common(10)]

    out = {
        "metric_id": ID,
        "metric_name": "重点企业类型分布",
        "script": ID + ".py",
        "as_of": C.AS_OF,
        "source": {
            "db": C.DB_GKX,
            "snapshots": [
                "code/_snapshots21/star_roster_gkx_20261021.json",
                "code/_snapshots21/tech_tags_20261021.json",
                "code/_snapshots21/base_20261021.json",
                "code/_snapshots21/chain_firm_index_20261023.json",
                "code/_snapshots21/w13e3_probe_20261023.json",
                "code/M_ENT_KEY_TOTAL_out.json",
            ],
        },
        "calc_logic_ref": "gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_TYPE_DIST_TOPIC.md",
        "support_judgment": "部分支持",
        "verdict_kind": "proxy_constructed",
        "four_judgment": {
            "表结构直接支持（开发库+三方库）": "否：两库均无重点企业类型分布结果表",
            "表数据直接支持（开发库+三方库）": "否：无结果表",
            "依赖表结构支持（开发库/三方库）": "部分：gkx 有 tech_tag 与 stock_base；无 foreign tag_code；名单需另建",
            "依赖表数据支持（开发库/三方库）": "是（高企/科技型中小/上市三类）/否（外资标签、年度、完整产业过滤）：4,561 家名单内三类均可算",
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "本件是单期截面：名单与标签均无 stat_year，环比没有上年格。"
                            "used/missing 为空，不是把缺年按 0 摊入；同比按空处理。",
        "result": result,
        "notes": [
            "名单代理是授权 >=50 的 4,561 家，不是 KEY_TOTAL 的 6,917 个受让人；差异在 §二 写明。",
            "四类非互斥：计位和 5,118 超过名单 4,561，禁止把四类相加当总数。",
            "listed 取 stock_base 主体集合（含申报稿/终止），不是「仅正常上市」。",
            "foreign 只有 org_type 文本旁证 226 家，无 tag_code，故该维判缺。",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote", OUT)
    print("roster", n, "high", t["high_tech_n"], "sme", t["sme_n"], "listed", t["listed_n"],
          "foreign_proxy", t["foreign_orgtype_n"], "union3", t["union3"], "none", t["none3"])
    print("sum_four", result["four_type_sum"], result["four_type_sum_pct"])


if __name__ == "__main__":
    main()
