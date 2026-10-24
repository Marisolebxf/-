#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""深圳机构产业领域分布（M_SVC_PT_SZ_FIELD_DIST）—— gkx 口径，自包含。

口径（calc-logic 0.2.0：领域轴预设目录全集常显、未分配常显禁剔除；本件换源后改轴）：
    切片   = 服务机构池 ∩ city='深圳市'
    领域轴 = gkx.dwd_org_industry_tags.industry_name（经 company_name 精确对齐到池）
             值域是「深圳 20+8 产业集群」口径的 12 个产业名：
             软件与信息服务 / 智能终端 / 人工智能 / 具身智能 / 机器人 / 集成电路 /
             数字创意 / 传感器 / 合成生物 / 智能网联汽车 / 生物医药 / 低空经济
    计数   = COUNT(DISTINCT org_id) GROUP BY 产业名（一家可命中多产业，同时给多命中与去重两个分母）
    未分配 = 切片内未在 tags 表对齐到的机构，单列常显

与旧稿的实质差异：旧稿的领域轴是项目内 15 集群目录（CL-SEI-01～10 + CL-FUT-01～05），
gkx 没有这套目录表，但有另一套产业词表（20+8）。本件**不把两套轴互相折算**，
而是如实换轴并披露：轴名不同、粒度不同、覆盖只有 40.58%，因此判档不抬。

数据源（只读快照，零 SQL）：
    code/_snapshots21/svc21_facts_20261022.json       pool（city）
    code/_snapshots21/svc21_pt_axis_20261022.json     pool_tags + pool_tags_meta

产出：code/M_SVC_PT_SZ_FIELD_DIST_out.json
运行：cd code && python3 M_SVC_PT_SZ_FIELD_DIST.py
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
AXIS = os.path.join(SNAP, "svc21_pt_axis_20261022.json")
OUT = os.path.join(HERE, "M_SVC_PT_SZ_FIELD_DIST_out.json")


def main():
    t0 = time.time()
    fact = json.load(open(FACTS, encoding="utf-8"))
    ax = json.load(open(AXIS, encoding="utf-8"))
    pool, bf = fact["pool"], fact["base_fields"]
    tags = ax["pool_tags"]
    meta = ax["pool_tags_meta"]

    sz = [o for o, v in pool.items() if v.get("city") == "深圳市"]
    n = len(sz)
    matched = [o for o in sz if tags.get(o)]
    cnt = Counter()
    multi = Counter()
    for o in matched:
        arr = tags.get(o) or []
        multi[len(arr)] += 1
        for a in arr:
            cnt[a] += 1

    rows = []
    for name, c in cnt.most_common():
        rows.append({"field": name, "org_count": c, "share_of_sz": round(c / n, 6),
                     "share_of_matched": round(c / len(matched), 6) if matched else None})
    unassigned = n - len(matched)

    out = {
        "metric_id": "M_SVC_PT_SZ_FIELD_DIST",
        "metric_name": "深圳机构产业领域分布",
        "support_judgment": "部分支持",
        "judgment_reason": (
            "深圳切片的产业领域分布可出数（%d/%d 家对齐到产业词表，12 个产业名、"
            "多命中 %d 家次），但领域轴换了一套字典（旧稿 15 集群目录在 gkx 无表，"
            "改用 tags 的「20+8 产业集群」词表），且覆盖率只有 %.2f%%、"
            "未对齐的 %d 家只能单列 → 维度不完整 → 部分支持"
            % (len(matched), n, sum(cnt.values()), 100.0 * len(matched) / n, unassigned)),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_industry_tags(company_name, industry_name)",
             "rows": meta["rows_scanned"],
             "snapshot": "code/_snapshots21/svc21_pt_axis_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_org_product_info（池人口）+ dwd_org_base_info(city)",
             "rows": fact["population"]["product_info_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面指标：产业领域分布是当前存量的横截面切分，不含年度分母；"
                            "tags 表无年份列，本件刻意不做年度序列（补 0 会把未采集年当零供给）。"),
        "population": {
            "pool_orgs": len(pool),
            "shenzhen_orgs": n,
            "tag_matched": len(matched),
            "tag_unassigned": unassigned,
            "tag_coverage": round(len(matched) / n, 6),
            "pool_tagged": meta["rows_matched"],
            "pool_tag_coverage": meta["coverage_of_pool"],
            "rows_scanned": meta["rows_scanned"],
        },
        "field_rows": rows,
        "fields_total": len(rows),
        "multi_hit_org_hits": sum(cnt.values()),
        "multiplicity": {str(k): v for k, v in sorted(multi.items())},
        "axis_substitution": {
            "old_axis": "项目内 15 集群目录（CL-SEI-01～10 + CL-FUT-01～05，POLICY_VERSION sz-10+5-2026）",
            "new_axis": "gkx.dwd_org_industry_tags.industry_name 的「20+8 产业集群」词表（12 个有值产业）",
            "mapping": None,
            "why_no_mapping": ("两套轴无权威对照表：旧轴是项目自建集群码，新轴是产业名文本；"
                               "强行按名称相似映射会把「人工智能」并进「新一代信息技术」这类"
                               "一对多关系做成一对一，产生不可复核的口径损失。故本件只换轴、不折算。"),
            "impact": "同一切片在两个轴下的分档不可直接比大小，只能比「集中度」这类结构量",
        },
        "difference_vs_old_draft": {
            "population": "旧稿输出人口为全池 43,296（未切深圳）→ 本件严格切深圳 %d 家" % n,
            "axis": "旧稿 15 集群（10 个有命中，CL-SEI-01/CL-FUT-02 各 43,296 为字典性全量默认映射）→ 本件 12 个产业名、最大 8,242（软件与信息服务）",
            "unassigned": "旧稿未分配桶为 −44,916（未归并导致）→ 本件未分配 %d（覆盖率 %.2f%%）"
                          % (unassigned, 100.0 * len(matched) / n),
        },
        "compute": {"status": "ok", "elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("sz=%d matched=%d (%.2f%%) unassigned=%d fields=%d"
          % (n, len(matched), 100.0 * len(matched) / n, unassigned, len(rows)))
    print("top", [(r["field"], r["org_count"]) for r in rows[:5]])
    print("->", OUT)


if __name__ == "__main__":
    main()
