#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_SVC_TYPE_DIST_QUERY 查询结果·服务类型分布（W14-S2）。

查询态口径卡：对象 = 当前查询命中的 org_id 去重集合，分组 = 六类服务类型 + 未分类，
度量 = COUNT(DISTINCT org_id)，时机 = 查询链路实时分桶，不落 ADS。

本件不产出「全库分布」，只给三组可复算的查询结果示例（深圳全部 / 人工智能标签 /
南山区 / 有专利记录），并在同一集合上并列两种分桶优先级，证明分桶规则未签时
分布会整体换形——这是判「部分支持」的直接证据。

运行：cd code && python3 M_SVC_TYPE_DIST_QUERY.py
产出：code/M_SVC_TYPE_DIST_QUERY_out.json
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FAMILY = os.path.join(SNAP, "svc21_rec_20261023.json")
COLS = os.path.join(SNAP, "gkx_columns_20261023.json")
OUT = os.path.join(HERE, "M_SVC_TYPE_DIST_QUERY_out.json")


def with_pct(rows, n):
    return [{"type": t, "n": v, "pct": round(v / n * 100, 4) if n else None} for t, v in rows]


def main():
    fam = json.load(open(FAMILY, encoding="utf-8"))
    cols = json.load(open(COLS, encoding="utf-8"))
    b = fam["bucket_axis"]
    pop = fam["pool"]
    n_sz = pop["sz"]

    sets = b["demo_query_sets"]
    demo = {}
    for key, nkey in (("all_sz", None), ("industry_ai", "industry_ai_n"),
                      ("district_nanshan", "district_nanshan_n"),
                      ("patent_holders", "patent_holders_n")):
        n = sets[nkey] if nkey else n_sz
        demo[key] = {"n": n, "rows": with_pct(sets[key], n)}

    out = {
        "metric_id": "M_SVC_TYPE_DIST_QUERY",
        "metric_name": "查询结果·服务类型分布",
        "support_judgment": "部分支持",
        "verdict_kind": "query_state",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "查询态指标，无年度基期：度量是当前查询会话命中的 org_id 集合在六类上的即时分桶，"
            "随查询条件实时变，不落 ADS、不预聚合。used / missing 均为空表；"
            "正文给的是若干可复算查询集合的示例分布，不是某年的全库统计。"
        ),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "mode": "read-only",
             "tables": ["dwd_org_org_product_info", "dwd_org_base_info",
                        "dwd_org_industry_tags"],
             "snapshot": "code/_snapshots21/svc21_rec_20261023.json",
             "upstream": fam["source"]["upstream"]},
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "mode": "read-only",
             "tables": ["information_schema.columns"],
             "snapshot": "code/_snapshots21/gkx_columns_20261023.json"},
        ],
        "params": {
            "object": "当前查询命中的服务机构 org_id，去重",
            "measure": "每桶 COUNT(DISTINCT org_id)",
            "timing": "查询链路实时分桶，内存/会话级；不落 ADS",
            "empty_state": "0 命中 → 各类型全 0 / 空图；禁止回退全库分布",
            "bucket_rule_a": b["rule_innov_first"],
            "bucket_rule_b": b["rule_specialty_first"],
            "unclassified_policy": "六类全不中 → UNCLASSIFIED 单列，不并入任一类",
            "forbidden": ["不复用门户全库类型环图", "不复用深圳类型分布", "不复用 M_SVC_INDUSTRY_LAYOUT"],
        },
        "structure_probe": {
            "gkx_tables": cols["n_tables"],
            "gkx_columns": cols["n_columns"],
            "svc_type_columns": fam["candidate"]["svc_type_columns"],
            "svc_type_columns_n": len(fam["candidate"]["svc_type_columns"]),
            "column_index_names": 1285,
            "svc_like_tables": fam["candidate"]["svc_like_tables"],
            "reading": "全库 1,285 个列名无 svc_type / service_type；目标态主数据列不存在，六类只能由经营范围词表重建",
        },
        "value": {
            "sz_total": n_sz,
            "rule_a_rows": with_pct(b["sz_innov_first"], n_sz),
            "rule_b_rows": with_pct(b["sz_specialty_first"], n_sz),
            "rule_a_sum": sum(v for _, v in b["sz_innov_first"]),
            "rule_b_sum": sum(v for _, v in b["sz_specialty_first"]),
            "unclassified_a": b["unclassified"],
            "multi_label_rows": b["multi_label_rows"],
            "multi_label_per_org": b["multi_label_per_org"],
            "multi_label_note": ("同一机构可命中多类，命中行合计 61,864 > 25,597；"
                                 "分桶取首个命中，故两套优先级给出的七行合计都回到 25,597"),
        },
        "pool_reference": {
            "rule_a_rows": with_pct(b["pool_innov_first"], pop["total"]),
            "rule_b_rows": with_pct(b["pool_specialty_first"], pop["total"]),
            "total": pop["total"],
        },
        "demo_query_sets": demo,
        "rule_diff": {
            "INNOV": 1544 - 19879,
            "FINANCE": 6932 - 2131,
            "CONSULT": 9123 - 1774,
            "MKT": 5290 - 486,
            "HR": 1256 - 248,
            "IP": 422 - 49,
            "UNCLASSIFIED": 1030 - 1030,
            "note": "规则 B 减规则 A；正值为 B 更多，负值为 B 更少",
        },
        "shift_reading": (
            "全深圳集合 INNOV 占 77.66%；人工智能标签集合升到 93.87%；南山区降到 79.88%；"
            "有专利集合升到 87.87%。同一套分桶规则下，查询条件一变分布就变，"
            "这正是「查询结果分布」与「全库统计」的分界。"
        ),
        "gaps": [
            {"gap": "svc_type 主数据", "detail": "全库 1,285 列名 0 个 svc_type / service_type",
             "impact": "目标态分桶列不存在，只能用经营范围词表过渡"},
            {"gap": "分桶优先级", "detail": "Q106 未签：INNOV 优先与 IP 优先两套规则",
             "impact": "INNOV 桶 19,879 vs 1,544，CONSULT 桶 1,774 vs 9,123，分布整体换形"},
            {"gap": "ADS 承载", "detail": "gkx 280 表 0 张 svc_metric_fact / svc_org_card",
             "impact": "本编号在 fact / dist 中 0 行是正确态，不能拿预聚合值替代"},
            {"gap": "语义识别", "detail": "经营范围词表是关键词匹配，不是主营业务分类",
             "impact": "未分类 1,030 家（4.02%）；多标签 2.4168 类/家"},
        ],
        "calc_logic_baseline": {
            "path": "gkx-orchestration/agent-delivery/metrics/calc-logic/SVC/M_SVC_TYPE_DIST_QUERY.md",
            "q_id": "Q106",
            "legacy_full_dist_n": 3525,
            "bucket_count": 6,
            "status": "查询态口径卡（2026-10-13 徐滕强选 A；D1 draft，挂 Q106）",
            "note": "正本明文禁止在 0 命中时回退全库 3,525 的六类分布；本件示例集只用于演示分桶规则，不是全库统计。",
        },
        "cross_refs": {
            "calc_logic": "gkx-orchestration/agent-delivery/metrics/calc-logic/SVC/M_SVC_TYPE_DIST_QUERY.md",
            "wanghui": None,
            "sibling": ["M_SVC_REC_CANDIDATE_CNT", "M_SVC_PT_SZ_TYPE_DIST"],
        },
    }

    with open(OUT, "w", encoding="utf-8") as fo:
        json.dump(out, fo, ensure_ascii=False, indent=1)
    print("written", OUT)
    print("ruleA", out["value"]["rule_a_rows"])
    print("ruleB", out["value"]["rule_b_rows"])
    print("sum", out["value"]["rule_a_sum"], out["value"]["rule_b_sum"],
          "multi", out["value"]["multi_label_rows"])
    print("demo", {k: v["n"] for k, v in demo.items()})


if __name__ == "__main__":
    main()
