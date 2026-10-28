#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_SVC_SZ_DISTRICT｜深圳服务机构分布（区级分面）。

口径：服务机构池 44,153 家 ∩ city='深圳市' → 25,597 家，按底册行政区（area）分面，
未分配单列。池规则见 M_SVC_ORG_TOTAL.md §2.2，本件不重定义池。

数据面：gkx（183.240.141.251:3318，只读 gkx_reader_zp）；零 SQL 运行，
只读 code/_snapshots21/ 下落盘快照。

产出：code/M_SVC_SZ_DISTRICT_out.json
运行：cd code && python3 M_SVC_SZ_DISTRICT.py
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FAM = os.path.join(SNAP, "svcsz21_facts_20261023.json")
OUT = os.path.join(HERE, "M_SVC_SZ_DISTRICT_out.json")

TYPES = ["IP", "FINANCE", "HR", "MKT", "CONSULT", "INNOV", "UNCLASSIFIED"]
TYPE_CN = {
    "IP": "知识产权服务", "FINANCE": "金融服务", "HR": "人力资源服务",
    "MKT": "市场推广服务", "CONSULT": "综合咨询", "INNOV": "研发创新服务",
    "UNCLASSIFIED": "未分类",
}
SIZES = ["大型", "中型", "小型", "微型", "未知"]
STAGES = ["stage-research", "stage-ip", "stage-transfer",
          "stage-pilot", "stage-testing", "stage-market"]
STAGE_CN = {
    "stage-research": "研发与科研合作", "stage-ip": "知识产权与标准",
    "stage-transfer": "技术转移与孵化", "stage-pilot": "中试熟化",
    "stage-testing": "检验检测认证", "stage-market": "市场与金融咨询",
}
# 深圳市 10 个行政区（含大鹏新区）。快照里没有出现的区按 0 行披露，不猜。
SZ_DISTRICTS = ["南山区", "宝安区", "龙岗区", "福田区", "龙华区",
                "光明区", "罗湖区", "坪山区", "盐田区", "大鹏新区"]


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def pct(a, b):
    return round(a / b * 100, 2) if b else None


def main():
    fam = load(FAM)
    dist = fam["district"]
    total = fam["pool"]["shenzhen"]
    named = dist["named_total"]
    rows = {r[0]: r[1] for r in dist["rows"]}

    district_rows = []
    for name in SZ_DISTRICTS:
        n = rows.get(name, 0)
        district_rows.append({
            "area": name,
            "orgs": n,
            "share_pct": pct(n, named),
            "share_of_sz_pct": pct(n, total),
            "has_rows": name in rows,
        })
    # 快照里出现的区若不在 10 区名单内，单列「异名区」，避免静默丢行。
    extra = [k for k in rows if k not in SZ_DISTRICTS]
    district_rows.append({
        "area": "未分配（area 空）", "orgs": dist["unassigned"],
        "share_pct": None, "share_of_sz_pct": pct(dist["unassigned"], total),
        "has_rows": True,
    })

    by_type = {}
    for name in SZ_DISTRICTS:
        rec = fam["district_type"].get(name) or []
        d = {t: n for t, n in rec}
        by_type[name] = {
            "orgs": rows.get(name, 0),
            "types": [{"type": t, "name_cn": TYPE_CN[t], "orgs": d.get(t, 0),
                       "share_pct": pct(d.get(t, 0), rows.get(name, 0))} for t in TYPES],
            "top_type": max(TYPES, key=lambda t: d.get(t, 0)) if rows.get(name, 0) else None,
        }
    # 未分配格的类型构成
    rec = fam["district_type"].get("未分配") or []
    d = {t: n for t, n in rec}
    by_type["未分配（area 空）"] = {
        "orgs": dist["unassigned"],
        "types": [{"type": t, "name_cn": TYPE_CN[t], "orgs": d.get(t, 0),
                   "share_pct": pct(d.get(t, 0), dist["unassigned"])} for t in TYPES],
        "top_type": max(TYPES, key=lambda t: d.get(t, 0)) if dist["unassigned"] else None,
    }

    by_size = {}
    for name in SZ_DISTRICTS:
        rec = fam["district_size"].get(name) or []
        d = {s: n for s, n in rec}
        by_size[name] = [{"size": s, "orgs": d.get(s, 0),
                          "share_pct": pct(d.get(s, 0), rows.get(name, 0))} for s in SIZES]

    by_stage = {}
    for name in SZ_DISTRICTS:
        rec = fam["district_stage"].get(name) or []
        d = {s: n for s, n in rec}
        by_stage[name] = [{"stage": s, "name_cn": STAGE_CN[s], "orgs": d.get(s, 0),
                           "share_pct": pct(d.get(s, 0), rows.get(name, 0))} for s in STAGES]

    top3_names = [r[0] for r in dist["rows"][:3]]
    top5_names = [r[0] for r in dist["rows"][:5]]

    out = {
        "metric_id": "M_SVC_SZ_DISTRICT",
        "metric_name": "深圳服务机构分布",
        "support_judgment": "完全转换支持",
        "judgment_reason": (
            "gkx 280 表中无 svc_region_dist 等结果面（0 张 svc_*），但底册 area 字段在深圳切片上"
            " 25,587/25,597 有值（99.96%），未分配 10 家可单列，区级合计与切片严格闭合；"
            "结构与数据量均足，当日可经转换出数，故判完全转换支持。"
        ),
        "verdict_kind": "positive",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "本件是截面（当期区级分布），没有年度序列，因此不使用基期年份；"
            "成立年维在 M_SVC_PT_SZ_TOTAL 另件处理，本件不摊年、不补 0。"
        ),
        "sources": {
            "library": "gkx",
            "host": "183.240.141.251:3318",
            "user": "gkx_reader_zp",
            "mode": "read-only",
            "tables": [
                "gkx.dwd_org_org_product_info（机构池，main_activities 非空 → org_id 去重）",
                "gkx.dwd_org_base_info（area / city）",
            ],
            "snapshots": [
                "code/_snapshots21/svcsz21_facts_20261023.json",
                "code/_snapshots21/svc21_facts_20261022.json",
                "code/_snapshots21/base_20261021.json",
            ],
            "cross_ref": [
                "第三方库指标计算过程/M_SVC_ORG_TOTAL.md（池 44,153 定义）",
                "第三方库指标计算过程/M_SVC_PT_SZ_TOTAL.md（深圳切片 25,597）",
                "第三方库指标计算过程/M_SVC_PT_SZ_REGION_ORG.md（同数区级分面，另一验收单元）",
            ],
        },
        "params": {
            "city_filter": "深圳市",
            "pool_total": fam["pool"]["total"],
            "sz_total": total,
            "area_field": "dwd_org_base_info.area",
            "unassigned_policy": "area 空白单列，不按地址解析、不并区",
            "district_axis": "行政区（10 区，含大鹏新区）",
        },
        "value": {
            "districts_with_orgs": len(dist["rows"]),
            "named_total": named,
            "unassigned": dist["unassigned"],
            "total": total,
            "pool_share_pct": pct(total, fam["pool"]["total"]),
        },
        "districts": district_rows,
        "concentration": {
            "hhi": dist["hhi"],
            "hhi_note": "按行政区份额平方和，取值 0—1；本值对应等效区数 1/HHI",
            "effective_districts": round(1 / dist["hhi"], 4) if dist["hhi"] else None,
            "top3_names": top3_names,
            "top3_orgs": dist["top3"],
            "top3_share_pct": round(dist["top3_share"] * 100, 2),
            "top5_names": top5_names,
            "top5_share_pct": round(dist["top5_share"] * 100, 2),
        },
        "by_type": by_type,
        "by_size": by_size,
        "by_stage": by_stage,
        "fill": {
            "area_nonnull": dist["named_total"],
            "area_rate_pct": pct(dist["named_total"], total),
            "unassigned": dist["unassigned"],
            "unassigned_rate_pct": pct(dist["unassigned"], total),
        },
        "reconcile": {
            "district_sum": named + dist["unassigned"],
            "sz_total": total,
            "equal": named + dist["unassigned"] == total,
            "pool_total": fam["pool"]["total"],
            "outside_sz": fam["pool"]["total"] - total,
            "outside_sz_note": "池 44,153 − 深圳 25,597 = 18,556（广州/东莞/惠州/未回联）",
        },
        "extra_areas": extra,
        "districts_zero": [d["area"] for d in district_rows if d["area"] in SZ_DISTRICTS and d["orgs"] == 0],
        "gaps": [
            {
                "gap": "未分配 10 家",
                "detail": "area 空白；不按注册地址解析、不猜测归属",
                "impact": "占切片 0.04%，不改变区级排序",
                "fix": "底册补 area 或由甲方提供注册地址解析结果",
            },
            {
                "gap": "大鹏新区 0 家",
                "detail": "池内该区无机构，是真实 0 行而非缺值",
                "impact": "区级 10 格里 9 格非零、1 格为零",
                "fix": "无需修；展示层按「暂无供给机构」呈现",
            },
            {
                "gap": "无官方服务机构名录",
                "detail": "池是经营范围代理口径，含制造企业与高校",
                "impact": "区级分布反映「有经营范围文本的机构」，不是官方认定名单",
                "fix": "甲方提供名录后替换池并重跑全族十件",
            },
        ],
        "cross_refs": {
            "M_SVC_PT_SZ_REGION_ORG": {
                "same_number": True,
                "note": "两件同池同字段，区级数字逐位一致；差别只在验收单元（SVC-BASIC-A6 vs PORTAL 深圳专题）",
            },
            "M_SVC_PT_SZ_TOTAL": {"sz_total": total, "same_number": True},
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written", OUT)
    print("sz=%d named=%d unassigned=%d hhi=%s" % (total, named, dist["unassigned"], dist["hhi"]))
    print("top3=%s %.2f%%" % (top3_names, dist["top3_share"] * 100))


if __name__ == "__main__":
    main()
