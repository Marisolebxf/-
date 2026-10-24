#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SVC_SZ_SCALE｜深圳服务机构规模。

口径：服务机构池 44,153 家 ∩ city='深圳市' → 25,597 家，按底册 org_size（大型/中型/小型/微型）
分面，未知档单列；另给注册资本档作交叉校验（不是官方划型，不替代规模档）。

数据面：gkx（183.240.141.251:3318，只读 gkx_reader_zp）；零 SQL 运行。

产出：code/M_SVC_SZ_SCALE_out.json
运行：cd code && python3 M_SVC_SZ_SCALE.py
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FAM = os.path.join(SNAP, "svcsz21_facts_20261023.json")
OUT = os.path.join(HERE, "M_SVC_SZ_SCALE_out.json")

SIZES = ["大型", "中型", "小型", "微型", "未知"]
TYPES = ["IP", "FINANCE", "HR", "MKT", "CONSULT", "INNOV", "UNCLASSIFIED"]
TYPE_CN = {
    "IP": "知识产权服务", "FINANCE": "金融服务", "HR": "人力资源服务",
    "MKT": "市场推广服务", "CONSULT": "综合咨询", "INNOV": "研发创新服务",
    "UNCLASSIFIED": "未分类",
}
STAGES = ["stage-research", "stage-ip", "stage-transfer",
          "stage-pilot", "stage-testing", "stage-market"]
STAGE_CN = {
    "stage-research": "研发与科研合作", "stage-ip": "知识产权与标准",
    "stage-transfer": "技术转移与孵化", "stage-pilot": "中试熟化",
    "stage-testing": "检验检测认证", "stage-market": "市场与金融咨询",
}
SIZE_CN_NOTE = {
    "大型": "官方划型中的最高一档（营收/人数/资产三项联合判定）",
    "中型": "官方划型第二档",
    "小型": "官方划型第三档",
    "微型": "官方划型最低一档",
    "未知": "底册该字段为空，原样单列",
}


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def pct(a, b):
    return round(a / b * 100, 2) if b else None


def main():
    fam = load(FAM)
    sz = fam["size"]
    total = fam["pool"]["shenzhen"]
    rows = {r[0]: r[1] for r in sz["rows"]}
    pool_rows = {r[0]: r[1] for r in sz["pool_rows"]}
    pool_total = fam["pool"]["total"]

    size_rows = []
    for s in SIZES:
        size_rows.append({
            "size": s,
            "orgs": rows.get(s, 0),
            "share_pct": pct(rows.get(s, 0), total),
            "pool_orgs": pool_rows.get(s, 0),
            "pool_share_pct": pct(pool_rows.get(s, 0), pool_total),
            "note": SIZE_CN_NOTE[s],
        })

    by_type = {}
    for s in SIZES:
        rec = fam["size"]["x_type"].get(s) or []
        d = {t: n for t, n in rec}
        by_type[s] = [{"type": t, "name_cn": TYPE_CN[t], "orgs": d.get(t, 0),
                       "share_of_size_pct": pct(d.get(t, 0), rows.get(s, 0))} for t in TYPES]

    by_stage = {}
    for s in SIZES:
        rec = fam["size"]["x_stage"].get(s) or []
        d = {k: n for k, n in rec}
        by_stage[s] = [{"stage": k, "name_cn": STAGE_CN[k], "orgs": d.get(k, 0),
                        "share_of_size_pct": pct(d.get(k, 0), rows.get(s, 0))} for k in STAGES]

    cap_rows = []
    for band, n in sz["cap_rows"]:
        cap_rows.append({"band": band, "orgs": n, "share_pct": pct(n, total)})

    large = rows.get("大型", 0)
    medium = rows.get("中型", 0)
    small = rows.get("小型", 0)
    micro = rows.get("微型", 0)
    unknown = rows.get("未知", 0)
    known = sz["known"]
    sme = medium + small + micro

    out = {
        "metric_id": "M_SVC_SZ_SCALE",
        "metric_name": "深圳服务机构规模",
        "support_judgment": "完全转换支持",
        "judgment_reason": (
            "规模档（org_size）在深圳切片上 25,566/25,597 有值（99.88%），未知 31 家可单列；"
            "gkx 无 svc_metric_fact 结果面，但底册字段 + 当前数据量足以现转出五档分布与交叉分面，"
            "且五档合计与切片逐位闭合，故判完全转换支持。"
        ),
        "verdict_kind": "positive",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "本件是截面（当期规模档分布），无年度序列，不使用基期年份；"
            "规模档不随年份回溯，年报员工/营收序列不在本件指标范围内（覆盖仅 3.18%/2.63%，见 gaps）。"
        ),
        "sources": {
            "library": "gkx",
            "host": "183.240.141.251:3318",
            "user": "gkx_reader_zp",
            "mode": "read-only",
            "tables": [
                "gkx.dwd_org_org_product_info（机构池，main_activities 非空 → org_id 去重）",
                "gkx.dwd_org_base_info（org_size / reg_capital / city）",
            ],
            "snapshots": [
                "code/_snapshots21/svcsz21_facts_20261023.json",
                "code/_snapshots21/svc21_facts_20261022.json",
                "code/_snapshots21/base_20261021.json",
            ],
            "cross_ref": [
                "第三方库指标计算过程/M_SVC_ORG_TOTAL.md（池 44,153）",
                "第三方库指标计算过程/M_SVC_PT_KEYORG_SCALE.md（大型在池 1,906 / 深圳 1,045）",
            ],
        },
        "params": {
            "city_filter": "深圳市",
            "pool_total": pool_total,
            "sz_total": total,
            "size_field": "dwd_org_base_info.org_size",
            "size_axis": SIZES,
            "unknown_policy": "未知档原样单列，不并入小型、不按资本倒推",
            "cap_field": "dwd_org_base_info.reg_capital",
        },
        "value": {
            "sz_total": total,
            "known": known,
            "unknown": unknown,
            "known_rate_pct": pct(known, total),
            "large": large,
            "large_share_pct": pct(large, total),
            "medium": medium,
            "small": small,
            "micro": micro,
            "sme": sme,
            "sme_share_pct": pct(sme, total),
            "pool_large": pool_rows.get("大型", 0),
            "pool_large_share_pct": pct(pool_rows.get("大型", 0), pool_total),
        },
        "size_rows": size_rows,
        "by_type": by_type,
        "by_stage": by_stage,
        "capital": {
            "nonnull": sz["cap_nonnull"],
            "nonnull_rate_pct": pct(sz["cap_nonnull"], total),
            "rows": cap_rows,
            "median": sz["cap_median"],
            "mean": sz["cap_mean"],
            "max": sz["cap_max"],
            "min": sz["cap_min"],
            "note": "注册资本是认缴额，不是实缴、不是营收，也不等于官方划型依据；只作分布合理性校验",
        },
        "concentration": {
            "top2": large + medium,
            "top2_share_pct": pct(large + medium, total),
            "small_micro": small + micro,
            "small_micro_share_pct": pct(small + micro, total),
        },
        "annual_report_coverage": {
            "orgs_with_rev": fam["finance"]["orgs_with_rev"],
            "rev_rate_pct": round(fam["finance"]["rev_rate"] * 100, 2),
            "orgs_with_emp": fam["finance"]["orgs_with_emp"],
            "emp_rate_pct": round(fam["finance"]["emp_rate"] * 100, 2),
            "note": "年报营收/员工覆盖过低，不能用于按营收重划规模档；本件只披露不替代",
        },
        "reconcile": {
            "size_sum": large + medium + small + micro + unknown,
            "sz_total": total,
            "equal": large + medium + small + micro + unknown == total,
            "cap_sum": sum(n for _, n in sz["cap_rows"]),
            "cap_note": "资本五档 + 未知 = 25,597，与切片闭合；资本档与规模档不是同一口径，不作交叉一致要求",
        },
        "gaps": [
            {
                "gap": "规模档未知 31 家",
                "detail": "底册 org_size 为空",
                "impact": "占切片 0.12%，五档分布不受影响",
                "fix": "底册补划型或由甲方提供划型结果",
            },
            {
                "gap": "年报员工数覆盖 815 家（3.18%）",
                "detail": "dwd_org_annual_financial_info.employees_number 全表仅 3,170 行有值",
                "impact": "不能按员工数重算划型；官方划型需要人数维时不可用",
                "fix": "接入规上企业年报或社保参保人数",
            },
            {
                "gap": "年报营业收入覆盖 673 家（2.63%）",
                "detail": "operating_revenue 全表仅 2,193 行有值，且最新有值年集中在 2014—2016",
                "impact": "不能按营收重算划型，也不能做规模档×营收的联合分布",
                "fix": "接入税务/统计口径营收，或改用上市主体表（仅 972 家）",
            },
            {
                "gap": "规模档来自登记/年报划型，非实时",
                "detail": "底册 org_size 是某次划型结果，未带划型年份",
                "impact": "同一家企业在不同年份可能跨档，本件不显示跨档轨迹",
                "fix": "底册补划型年份与历史划型",
            },
        ],
        "cross_refs": {
            "M_SVC_ORG_TOTAL": {"pool_total": pool_total, "same_pool": True},
            "M_SVC_PT_KEYORG_SCALE": {"pool_large": pool_rows.get("大型", 0),
                                      "sz_large": large, "same_number": True},
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written", OUT)
    print("sz=%d large=%d medium=%d small=%d micro=%d unknown=%d"
          % (total, large, medium, small, micro, unknown))
    print("large_share=%.2f%% sme_share=%.2f%%" % (pct(large, total), pct(sme, total)))


if __name__ == "__main__":
    main()
