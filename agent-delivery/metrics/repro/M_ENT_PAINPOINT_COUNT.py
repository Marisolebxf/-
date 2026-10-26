#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_PAINPOINT_COUNT · 企业痛点数量（gkx 单库代理版）

定义
----
企业痛点数量 = 该企业在风险类表里的记录条数之和。六类痛点对应六张真实表：
  经营异常（dwd_org_company_abnormal）、严重违法（dwd_org_company_illegal）、
  行政处罚（dwd_org_company_punish）、失信被执行（dwd_org_risk_shixin）、
  被执行人（dwd_org_risk_zhixing）、税务处罚（dwd_org_risk_tax_punish）。

一个必须说清的限制
------------------
`enterprise_diagnosis`（痛点诊断结果面）在 gkx 不存在（source_absent，见
TABLE_ABSENCE_EVIDENCE §enterprise_diagnosis）。本件从原始风险表直接计数，
只能取「头部样本」：每张表按 org_id 分组后只落盘记录数前 3,000—5,000 个主体
（全量分组要把 6 张表 70 万行全部拉回，单次查询超时）。因此：
  - 每类痛点的**全库记录数与涉及企业数**是真值（聚合查询，见 totals）；
  - 逐企业痛点数量只有**头部榜**，不是全量分布，不能拿它算中位数。

输出：code/M_ENT_PAINPOINT_COUNT_out.json
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_ENT_PAINPOINT_COUNT_out.json"
METRIC = "M_ENT_PAINPOINT_COUNT"

SRC_LABEL = {"abnormal": "经营异常", "illegal": "严重违法", "punish": "行政处罚",
             "shixin": "失信被执行", "zhixing": "被执行人", "tax_punish": "税务处罚"}

TYPE_LABEL = {
    "dwd_org_company_abnormal": "经营异常",
    "dwd_org_company_illegal": "严重违法",
    "dwd_org_company_punish": "行政处罚",
    "dwd_org_risk_shixin": "失信被执行",
    "dwd_org_risk_zhixing": "被执行人",
    "dwd_org_risk_tax_punish": "税务处罚",
}


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def main() -> None:
    agg = load("pain_risk_counts_20261022.json")["rows"]
    per_type_total = {SRC_LABEL[r[0]]: {"records": r[1], "orgs": r[2]} for r in agg}

    extra = load("pain_org_extra_20261022.json")["tables"]
    per_org = defaultdict(lambda: defaultdict(int))
    samples = {}
    for table, blk in extra.items():
        label = TYPE_LABEL.get(table, table)
        if not blk.get("ok"):
            continue
        samples[label] = len(blk["rows"])
        for org_id, n in blk["rows"]:
            per_org[org_id][label] += n

    name_of = {r[0]: r[1] for r in load("star_base_rows_gkx.json")}
    city_of = {r[0]: r[3] for r in load("star_base_rows_gkx.json")}

    ranked = sorted(((oid, d) for oid, d in per_org.items()),
                    key=lambda x: -sum(x[1].values()))[:50]
    rows = []
    for i, (oid, d) in enumerate(ranked, 1):
        rows.append({"rank": i, "org_id": oid, "name": name_of.get(oid),
                     "city": city_of.get(oid), "painpoint_count": sum(d.values()),
                     "by_type": dict(d)})

    total_records = sum(v["records"] for v in per_type_total.values())
    total_orgs = sum(v["orgs"] for v in per_type_total.values())

    out = {
        "metric_id": METRIC,
        "metric_name": "企业痛点数量",
        "data_source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）",
        "formula": "painpoint_count_i = Σ_t COUNT(records) WHERE org_id=i，t ∈ 六类风险表",
        "blocking_tables": {
            "enterprise_diagnosis": {
                "triage": "source_absent",
                "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §enterprise_diagnosis",
            }
        },
        "proxy_path": "六张风险原始表按 org_id 直接计数，替代痛点诊断结果面",
        "proxy_deviation": "只有合规/司法/行政类痛点，不含经营痛点（现金流/人才流失/供应链）与舆情痛点；逐企业明细只取头部样本（每表前 3,000—5,000 主体），全库记录数与涉及企业数是真值，逐企业分布是截断的",
        "totals": {
            "records_all_types": total_records,
            "org_type_pairs": total_orgs,
            "by_type": per_type_total,
            "head_sample_sizes": samples,
            "orgs_in_head_union": len(per_org),
        },
        "type_weights_note": "六类等权计数：一条行政处罚与一条被执行记录都记 1 个痛点。若甲方要按严重度加权（失信>处罚>异常），需给出权重表，本件不自行设定",
        "top50": rows,
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": "enterprise_diagnosis 结果面不存在，但痛点的六类原始表都是真表真数：经营异常 5,862 条、严重违法 247 条、行政处罚 65,997 条、失信 76,035 条、被执行 550,334 条、税务处罚 528 条，合计 69.9 万条、覆盖 35,000 家以上主体。逐企业计数可直接 GROUP BY org_id 得到，故判部分支持；缺口是痛点类型只覆盖合规侧（无经营/舆情痛点），且逐企业明细受查询时限限制只落头部样本。",
            "criteria": {
                "result_table_exists": False,
                "risk_tables_present": 6,
                "records_all_types": total_records,
                "head_only": True,
                "proxy_used": True,
            },
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "六张风险表都是事件流水，本件数的是「截至抓取时点的累计条数」，不是年度新增，故无基期年份；表内带发生日期，若要做年增量需另建按年聚合（本件未做，避免把累计当年度）。",
        "sources": [
            {"path": "code/_snapshots21/pain_risk_counts_20261022.json",
             "table": "gkx.dwd_org_company_abnormal 等 6 张", "rows": 699532,
             "role": "全库记录数与涉及企业数（真值）"},
            {"path": "code/_snapshots21/pain_org_extra_20261022.json",
             "table": "同上 6 张", "rows": 16553,
             "role": "逐企业头部计数（截断样本）"},
            {"path": "code/_snapshots21/star_base_rows_gkx.json",
             "table": "gkx.dwd_org_base_info", "rows": 189116,
             "role": "org_id→企业名/城市"},
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[OK] {METRIC} -> {OUT.name} records={total_records} head_orgs={len(per_org)}")
    for r in rows[:5]:
        print("  ", r["rank"], (r["name"] or r["org_id"])[:20], r["painpoint_count"], r["by_type"])


if __name__ == "__main__":
    main()
