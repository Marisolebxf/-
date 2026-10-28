#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_SUPPLY_STRUCT_TOPIC 供应链结构指标（20261021 改源版，否定性探针）。

口径来源：项目内 AI-20261016 补齐的图论定义（calc-logic 同 ID 正本在 20261021 注册表为 null）；
需求原文只给五个子指标名：供应商数量、供应商间距离、供应商稳定性、供应链密度、关系紧密度。

本件不计算指标，只证明「为什么不可算」：
  gkx 280 表无供应链边表、无 supplier 列；live 边表存在但 0 行；
  招投标共现 98.89% 的项目只有 1 家中标，不能构成有方向的供应边。
产物 verdict_kind = negative_evidence。
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _w13e3_common as C

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "M_ENT_SUPPLY_STRUCT_TOPIC_out.json")
ID = "M_ENT_SUPPLY_STRUCT_TOPIC"


def main():
    probe = C.load("w13e3_probe_20261023.json")
    cols = C.load("gkx_columns_20261023.json")
    bid = probe["E_bid"]
    live = probe["F_live"]
    scan = probe["A_schema_scan"]

    invest_rows = cols["tables"]["dwd_org_invest_info"]["rows"]
    shareholder_rows = cols["tables"]["dwd_org_shareholder_info"]["rows"]
    bid_rows = cols["tables"]["dwd_bid_win_candidate_out"]["rows"]

    submetrics = [
        {
            "name": "供应商数量",
            "graph_definition": "供应边集合中，以目标企业为终点的不同上游 org 数",
            "status": "不可算",
            "reason": "无供应边表；investment/shareholder 边是股权与投资关系，方向与语义都不是供应。",
        },
        {
            "name": "供应商间距离",
            "graph_definition": "供应子图上供应商两两之间的最短路径长度",
            "status": "不可算",
            "reason": "无供应边表，图不存在；招投标共现图为无向二部图，且 98.89% 项目只有 1 家中标。",
        },
        {
            "name": "供应商稳定性",
            "graph_definition": "同一供应边在相邻年度的存续/中断比例",
            "status": "不可算",
            "reason": "既无供应边，也无边的业务起止时间；单期快照无法构造面板。",
        },
        {
            "name": "供应链密度",
            "graph_definition": "E / (N(N-1))，N 为节点数、E 为有向边数",
            "status": "不可算",
            "reason": "E 与 N 都不存在；不能用投资边替代，否则密度含义变成股权网络密度。",
        },
        {
            "name": "关系紧密度",
            "graph_definition": "供应边权重（交易额/合作强度）的均值或分位",
            "status": "不可算",
            "reason": "无供应边权字段；演示表的 relation_strength 是随机小数，20261021 口径已排除演示面。",
        },
    ]

    result = {
        "submetrics": submetrics,
        "n_submetrics": len(submetrics),
        "n_computable": 0,
        "gkx_side": {
            "n_tables": scan["tables"]["n_tables"],
            "n_columns": scan["columns"]["n_columns"],
            "table_name_hits_supply": scan["tables"]["table_name_hits"]["supply"],
            "supplier_column": scan["columns"]["column_hits"]["supplier"],
            "supplier_org_id_column": scan["columns"]["column_hits"]["supplier_org_id"],
            "n_supply_columns": scan["columns"]["n_supply_columns"],
            "only_purchase_like_column": {
                "table": "dwd_bid_base_out",
                "column": "estimated_purchasing_time",
                "semantics": "招标预计采购时间，不是供应商关系",
            },
            "supply_edge_table_exists": False,
        },
        "live_side": {
            "n_tables": live["n_tables"],
            "table_name_hits_supply": live["table_name_hits"]["supply"],
            "enterprise_supply_chain_rows": live["exact_counts"].get("gkxlumenx_dwd.enterprise_supply_chain"),
            "enterprise_industry_chain_rows": live["exact_counts"].get("gkxlumenx_dwd.enterprise_industry_chain"),
            "enterprise_base_rows": live["exact_counts"].get("gkxlumenx_dwd.enterprise_base"),
            "industry_chain_rows": live["exact_counts"].get("gkxlumenx_dwd.industry_chain"),
        },
        "edge_substitutes": {
            "dwd_org_invest_info_rows": invest_rows,
            "dwd_org_shareholder_info_rows": shareholder_rows,
            "usable_as_supply_edge": False,
            "why": "投资与股权是所有权关系，不能推出「谁向谁供货」；方向、金额语义、时间粒度都对不上。",
        },
        "bid_proxy": {
            "rows": bid["rows"],
            "projects": bid["projects"],
            "distinct_org": bid["distinct_org"],
            "project_size_dist": bid["project_size_dist"],
            "single_winner_projects": bid["single_winner_projects"],
            "single_winner_share_pct": bid["single_winner_share_pct"],
            "pairable_projects": bid["pairable_projects"],
            "max_project_size": bid["max_project_size"],
            "usable_as_supply_edge": False,
            "why": "共同中标是无向共现，不是上下游；可配对项目仅 328 个，且最大项目 2,302 条会把共现图拉成星形。",
        },
        "old_20261020_contrast": {
            "old_verdict": "部分支持",
            "old_source": "演示库 enterprise_supply_chain 85,791 行 / 123,294 节点",
            "why_dropped": "20261021 口径只允许开发库 + gkx、仅排除演示面；演示边表不能作为证据，"
                            "而 gkx 无替代表、live 边表 0 行，故从「可算不可信」降为「不可算」。",
        },
        "recompute_recipe_if_data_arrives": {
            "required_columns": ["supplier_org_id", "buyer_org_id", "relation_type",
                                 "trade_amount", "start_date", "end_date", "source"],
            "min_rows": "至少覆盖 10% 的底册企业且每家 >=2 条供应边，才能谈度分布与距离",
            "target_table": "dwd_org_supply_chain（建议）",
        },
    }

    out = {
        "metric_id": ID,
        "metric_name": "供应链结构指标",
        "script": ID + ".py",
        "as_of": C.AS_OF,
        "source": {
            "db": C.DB_GKX + "；live 开发库只读复核",
            "snapshots": [
                "code/_snapshots21/w13e3_probe_20261023.json",
                "code/_snapshots21/gkx_columns_20261023.json",
            ],
        },
        "calc_logic_ref": None,
        "calc_logic_note": "无同 ID 正本；注册表 calc_logic 为 null。公式来自项目内 AI-20261016 补齐的五项图论定义，"
                            "本件不把它冒充王惠口径。",
        "support_judgment": "完全不支持",
        "verdict_kind": "negative_evidence",
        "four_judgment": {
            "表结构直接支持（开发库+三方库）": "否：gkx 无供应链边表/列；live 有 enterprise_supply_chain 结构",
            "表数据直接支持（开发库+三方库）": "否：live 边表 0 行",
            "依赖表结构支持（开发库/三方库）": "否：gkx 无 supplier/supply 列；live 边表结构在但无数据",
            "依赖表数据支持（开发库/三方库）": "否：投资 46,967 / 股权 400,286 条均非供应边；招投标可配对 328 个项目",
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "本件不进入数值计算，没有年度序列与基期分母；used/missing 为空。"
                            "这不是「缺年按 0 摊入」，而是供应边这一层在源上不存在。",
        "result": result,
        "notes": [
            "判完全不支持，不是判部分支持：没有任何一条可算的供应边，五个子指标全部无定义域。",
            "招投标共现只能做旁证，不能当供应边：无方向、98.89% 单中标、可配对项目 328 个。",
            "演示库的 85,791 条边不再作为证据；20261021 支持度面只含开发库与 gkx。",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote", OUT)
    print("gkx supply tables", result["gkx_side"]["table_name_hits_supply"],
          "live rows", result["live_side"]["enterprise_supply_chain_rows"])
    print("bid", bid["rows"], bid["projects"], bid["single_winner_share_pct"], bid["pairable_projects"])


if __name__ == "__main__":
    main()
