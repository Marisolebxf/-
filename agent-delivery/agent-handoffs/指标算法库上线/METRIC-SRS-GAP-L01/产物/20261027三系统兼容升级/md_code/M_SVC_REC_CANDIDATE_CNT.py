#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_SVC_REC_CANDIDATE_CNT 候选机构数（W14-S2，注册表已废止）。

本件不计算任何"指标值"，只交付否定性证据：
  1) gkx 280 表 0 张 svc_* / service / recommend / circle / card 表；
  2) 全库 1,285 个列名里 0 个 svc_type / service_type；
  3) 唯一带 candidate 的两张表是「中标候选人」，与服务机构候选无关；
  4) 同一"候选"语义在 9 种筛选条件下给出 9 个不同的 N，证明它是 results.length；
  5) 注册表 lifecycle=retired、formula=无。

运行：cd code && python3 M_SVC_REC_CANDIDATE_CNT.py
产出：code/M_SVC_REC_CANDIDATE_CNT_out.json
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FAMILY = os.path.join(SNAP, "svc21_rec_20261023.json")
OUT = os.path.join(HERE, "M_SVC_REC_CANDIDATE_CNT_out.json")


def main():
    fam = json.load(open(FAMILY, encoding="utf-8"))
    c = fam["candidate"]
    pop = fam["pool"]

    ladder = [{"condition": k, "n": v} for k, v in c["filters"]]
    ns = [x["n"] for x in ladder]

    out = {
        "metric_id": "M_SVC_REC_CANDIDATE_CNT",
        "metric_name": "候选机构数",
        "support_judgment": "完全不支持",
        "verdict_kind": "negative_evidence",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "本件不是年度指标，无基期：注册表 2026-10-13 已判 retired，指标身份被撤销。"
            "正文给的是表结构/列名证据与筛选条件阶梯，不是某年的统计值，故 used / missing 均为空表。"
        ),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "mode": "read-only",
             "tables": ["information_schema.tables", "information_schema.columns"],
             "snapshot": "code/_snapshots21/gkx_columns_20261023.json",
             "note": "全库表/列字典由 information_schema 落盘，280 表 6,312 列"},
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "mode": "read-only",
             "tables": ["dwd_org_org_product_info", "dwd_org_base_info",
                        "dwd_org_annual_financial_info", "dwd_patent"],
             "snapshot": "code/_snapshots21/svc21_rec_20261023.json"},
        ],
        "registry": {
            "lifecycle": c["registry_lifecycle"],
            "formula": c["registry_formula"],
            "calc_logic": "gkx-orchestration/agent-delivery/metrics/calc-logic/SVC/M_SVC_REC_CANDIDATE_CNT.md",
            "page_semantics": "招引/培育页「共 N 家候选」= 当前筛选条件下 results.length，随筛选实时变",
        },
        "probe": {
            "gkx_tables": c["gkx_tables"],
            "gkx_columns": c["gkx_columns"],
            "svc_like_tables": c["svc_like_tables"],
            "svc_like_tables_n": len(c["svc_like_tables"]),
            "candidate_like_tables": c["candidate_like_tables"],
            "candidate_like_note": "两张均为 dwd_bid_win_candidate_out（中标候选人），与服务机构候选无关",
            "svc_type_columns": c["svc_type_columns"],
            "svc_type_columns_n": len(c["svc_type_columns"]),
            "column_index_names": 1285,
            "svc_metric_tables": 0,
            "settlement": "结构面与结果面均不存在；不存在可被 COUNT 的候选集合表",
        },
        "filter_ladder": ladder,
        "filter_ladder_n": len(ladder),
        "n_min": min(ns),
        "n_max": max(ns),
        "n_span": max(ns) - min(ns),
        "reading": (
            "同一句「候选机构」在 9 种筛选条件下得到 9 个 N，最小 531（外部三市有营收年报）、"
            "最大 25,597（深圳全部），跨度 25,066。任何单一 N 都只是某个筛选组合的结果集长度，"
            "不是可预聚合、可跨期比较的指标。"
        ),
        "population_context": {
            "total": pop["total"],
            "sz": pop["sz"],
            "external": pop["external"],
            "unassigned_city": pop["unassigned_city"],
            "city_rows": pop["city_rows"],
        },
        "gaps": [
            {"gap": "候选集合定义", "detail": "产业方向 × 机构类型 × 服务环节 × 规模 的组合未收敛",
             "impact": "N 随组合变化，无唯一值"},
            {"gap": "候选池成员表", "detail": "gkx 280 表无 svc_org_circle / svc_org_card / svc_metric_fact",
             "impact": "无法把「候选」物化成可复算集合"},
        ],
        "conclusion": {
            "publishable": False,
            "reason": "指标身份已于 2026-10-13 撤销；页面可继续显示「共 N 家」，但不得挂 MetricSpecCard、不得灌 svc_metric_*",
            "replacement": "如甲方确需「候选规模」，应另立查询态口径卡（参照 M_SVC_TYPE_DIST_QUERY 的六要素写法），不要复活本 ID",
        },
        "cross_refs": {
            "calc_logic": "gkx-orchestration/agent-delivery/metrics/calc-logic/SVC/M_SVC_REC_CANDIDATE_CNT.md",
            "wanghui": None,
            "sibling": ["M_SVC_TYPE_DIST_QUERY", "M_SVC_REC_ATTRACT_SCORE"],
        },
    }

    with open(OUT, "w", encoding="utf-8") as fo:
        json.dump(out, fo, ensure_ascii=False, indent=1)
    print("written", OUT)
    print("tables", out["probe"]["gkx_tables"], "svc_like", out["probe"]["svc_like_tables_n"],
          "candidate", out["probe"]["candidate_like_tables"],
          "svc_type_cols", out["probe"]["svc_type_columns_n"])
    print("ladder", [(x["condition"], x["n"]) for x in ladder])


if __name__ == "__main__":
    main()
