#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SVC_PT_SZ_TYPE_DIST 深圳服务机构类型分布（W14-S2）。

数据面：只读 code/_snapshots21/svc21_rec_20261023.json 与
        code/_snapshots21/svc21_pt_axis_20261022.json（零 DB）。
口径：机构本体三类字典（企业/高校/科研院所），全集展示，不并入「其他」。

本件保留两套读数并逐条披露差异：
  A. 法定规则（科研院所 → 高校 → 企业）落在 city='深圳市' 切片：25,589 / 8 / 0；
  B. 名称清洗后（剔除两家名称含「深圳大学」的公司法人）：25,591 / 6 / 0；
  C. 科研院所 21 家 city 全空，其中 9 家名称带「深圳」——若按名称补切，深圳总数会变 25,606，
     与 S1 批 25,597 冲突，故本件不补切，只披露。

运行：cd code && python3 M_SVC_PT_SZ_TYPE_DIST.py
产出：code/M_SVC_PT_SZ_TYPE_DIST_out.json
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FAMILY = os.path.join(SNAP, "svc21_rec_20261023.json")
AXIS = os.path.join(SNAP, "svc21_pt_axis_20261022.json")
OUT = os.path.join(HERE, "M_SVC_PT_SZ_TYPE_DIST_out.json")


def main():
    fam = json.load(open(FAMILY, encoding="utf-8"))
    axis = json.load(open(AXIS, encoding="utf-8"))
    t = fam["type_axis"]
    pop = fam["pool"]

    rows = {k: v for k, v in t["sz_kind_rows"]}
    strict = {k: v for k, v in t["sz_kind_rows_strict"]}
    total = t["sz_total"]

    out = {
        "metric_id": "M_SVC_PT_SZ_TYPE_DIST",
        "metric_name": "深圳服务机构类型分布",
        "support_judgment": "部分支持",
        "verdict_kind": "partial_constructible",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "截面指标：口径时点为快照 code/_snapshots21/svc21_facts_20261022.json（"
            "dwd_org_org_product_info + dwd_org_base_info 重建池）。不按年度出数，故 used / missing 均为空表；"
            "机构类型取底册当前登记状态，不是某年快照。"
        ),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "mode": "read-only",
             "tables": ["dwd_org_org_product_info", "dwd_org_base_info",
                        "dwd_research_institute_base_info"],
             "snapshot": "code/_snapshots21/svc21_rec_20261023.json",
             "upstream": fam["source"]["upstream"]},
        ],
        "params": {
            "axis": "机构本体三类字典：企业 / 高校 / 科研院所",
            "classification_rule": t["rule"],
            "slice": "city='深圳市'（dwd_org_base_info.city 精确等值）",
            "no_other_bucket": "三类互斥且合计 = 池；不设「其他」桶，不把业务六类混入本体类型",
            "portal_note": "门户环图口径；gkx 无 svc_org_circle / svc_metric_fact 承载表",
        },
        "population": {
            "total": pop["total"],
            "sz": total,
            "sz_share_of_pool_pct": round(total / pop["total"] * 100, 4),
            "external": pop["external"],
            "unassigned_city": pop["unassigned_city"],
            "city_rows": pop["city_rows"],
        },
        "value": {
            "sz_type_rows": t["sz_kind_rows"],
            "sz_type_rows_dict": rows,
            "sz_total": total,
            "sz_unknown": t["sz_kind_unknown"],
            "sum_check": sum(rows.values()),
            "share_pct": {k: round(v / total * 100, 4) for k, v in rows.items()},
            "strict_rows": t["sz_kind_rows_strict"],
            "strict_dict": strict,
            "strict_sum_check": sum(strict.values()),
            "strict_share_pct": {k: round(v / total * 100, 4) for k, v in strict.items()},
            "hypothetical_with_research": total + t["research_sz_by_name_n"],
        },
        "global_compare": {
            "pool_type_rows": t["pool_kind_rows"],
            "pool_total": pop["total"],
            "pool_share_pct": {k: round(v / pop["total"] * 100, 4) for k, v in t["pool_kind_rows"]},
        },
        "university": {
            "rows": rows.get("高校", 0),
            "names": t["sz_university_names"],
            "false_positive_names": t["sz_university_false_positive"],
            "false_positive_n": len(t["sz_university_false_positive"]),
            "clean_rows": strict.get("高校", 0),
            "clean_names": [n for n in t["sz_university_names"]
                            if n not in t["sz_university_false_positive"]],
            "note": "名称含「大学」的公司法人被规则误收：深圳大学城创意园投资管理有限公司、深圳大学建筑设计研究院有限公司",
        },
        "research": {
            "pool_rows": t["research_total"],
            "city_blank": t["research_city_blank"],
            "city_rows": t["research_city_rows"],
            "sz_slice_rows": rows.get("科研院所", 0),
            "sz_by_name": t["research_sz_by_name"],
            "sz_by_name_n": t["research_sz_by_name_n"],
            "all_names": t["research_names"],
            "note": ("21 家科研院所的 city 与 prov 均为空串；按 city 切片深圳 0 家。"
                     "9 家名称含「深圳」，若按名称补切，深圳总数 25,597 → 25,606，与 S1 批同池同数冲突，"
                     "本件不补切，只把冲突摊开。"),
        },
        "district_matrix": t["district_kind"],
        "raw_org_type_top": t["org_type_raw_top"],
        "currency_top": t["ccy_top"],
        "gaps": [
            {"gap": "科研院所城市字段", "detail": "21 家 city / prov 全空", "impact": "深圳切片恒 0，不能与高校/企业同轴比较"},
            {"gap": "高校名称规则", "detail": "2 家公司法人名称含「深圳大学」被误收", "impact": "高校数 8 虚高，清洗后 6"},
            {"gap": "门户结果面", "detail": "gkx 280 表 0 张 svc_org_circle / svc_metric_fact", "impact": "无法复现门户环图的预聚合值"},
            {"gap": "机构类型主数据", "detail": "底册 org_type 是工商登记类型（有限责任公司/股份有限公司），不是本体三类", "impact": "三类轴只能由名称 + 科研院所名录重建"},
        ],
        "conclusion": {
            "publishable_rows": {"企业": rows.get("企业"), "高校": strict.get("高校"), "科研院所": 0},
            "must_disclose": "企业 25,591 / 高校 6 / 科研院所 0（清洗后）；法定规则读数 25,589 / 8 / 0 并列披露",
            "not_publishable": "科研院所非 0 的深圳环图、任何把 9 家名称含深圳的院所补进 slice 的版本",
        },
        "calc_logic_baseline": {
            "path": "gkx-orchestration/agent-delivery/metrics/calc-logic/SVC/M_SVC_PT_SZ_TYPE_DIST.md",
            "version": "v0.2.1",
            "pool": 43296,
            "sz": 14033,
            "says_sz_university": 0,
            "says_sz_research": 0,
            "note": "正本现网事实写「全池只有企业一类、高校 0、科研院所 0」，深圳切片真数 14,033；本件按 org_product_info 重建池得 44,153 / 25,597，高校 8、院所 0。差异见正文 §3.3。",
        },
        "cross_refs": {
            "calc_logic": "gkx-orchestration/agent-delivery/metrics/calc-logic/SVC/M_SVC_PT_SZ_TYPE_DIST.md",
            "wanghui": None,
            "sibling": ["M_SVC_PT_SZ_TOTAL", "M_SVC_PT_GLOBAL_TYPE_DIST", "M_SVC_TYPE_DIST_QUERY"],
            "axis_snapshot": "code/_snapshots21/svc21_pt_axis_20261022.json",
            "axis_meta": axis["org_kind_meta"],
        },
    }

    with open(OUT, "w", encoding="utf-8") as fo:
        json.dump(out, fo, ensure_ascii=False, indent=1)
    print("written", OUT)
    print("rows", rows, "sum", out["value"]["sum_check"], "strict", strict)
    print("research blank", t["research_city_blank"], "sz by name", t["research_sz_by_name_n"])
    print("district", t["district_kind"])


if __name__ == "__main__":
    main()
