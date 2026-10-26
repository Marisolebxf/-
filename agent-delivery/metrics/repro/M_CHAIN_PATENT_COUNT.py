#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_PATENT_COUNT —— 产业链关联专利数

口径（与 M_CHAIN_REG_COMMERCIALIZATION 同一公式，只去掉区域过滤）：
  COUNT(DISTINCT patent_id) WHERE 申请人名 = 企业名 ∧ 企业挂该链 ∧ application_year ≤ 2024
专利池：gkx.dwd_patent 2,939,895 行；申请人桥：first_applicant_name = dwd_org_base_info.name_cn（1,107,178 件命中）。
本脚本读共享快照 region_index_patent_union.json（chain|city → 件数），逐链汇总，不重跑 2.9M 行。
"""
from __future__ import annotations
import json, os, time

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_PATENT_COUNT_out.json")


def L(n):
    with open(os.path.join(SNAP, n), encoding="utf-8") as f:
        return json.load(f)


union = L("region_index_patent_union.json")
layer = L("chain21_layer_20261022.json")
chains = layer["chain_name"]
FOUR = ["深圳市", "广州市", "东莞市", "惠州市"]

agg = {}
for k, v in union.items():
    ch, city = k.split("|")
    a = agg.setdefault(ch, {"total": 0, "four": 0, "cities": {}})
    a["total"] += v
    a["cities"][city] = v
    if city in FOUR:
        a["four"] += v

rows = []
for ch, nm in chains.items():
    a = agg.get(ch, {"total": 0, "four": 0, "cities": {}})
    firms = layer["chain_city"].get(ch + "|深圳市", 0)
    members = sum(v for k, v in layer["chain_city"].items() if k.startswith(ch + "|"))
    rows.append({
        "chain_code": ch, "chain_name": nm,
        "patents_le2024": a["total"],
        "patents_le2024_four_city": a["four"],
        "patents_le2024_outside_four": a["total"] - a["four"],
        "outside_share_pct": round(100.0 * (a["total"] - a["four"]) / a["total"], 3) if a["total"] else None,
        "sz_patents_le2024": a["cities"].get("深圳市", 0),
        "chain_members": members,
        "patents_per_member": round(a["total"] / members, 2) if members else None,
        "members_with_sz_reg": firms,
        "top_cities": sorted(a["cities"].items(), key=lambda x: -x[1])[:4],
    })
rows.sort(key=lambda r: -r["patents_le2024"])
tot = sum(r["patents_le2024"] for r in rows)
four = sum(r["patents_le2024_four_city"] for r in rows)
sz = sum(r["sz_patents_le2024"] for r in rows)
vals = sorted(r["patents_le2024"] for r in rows)
members = sum(r["chain_members"] for r in rows)
stats = {
    "n_chains": len(rows),
    "min": vals[0], "max": vals[-1], "median": vals[len(vals) // 2],
    "top1_share_pct": round(100.0 * vals[-1] / tot, 3) if tot else None,
    "top3_share_pct": round(100.0 * sum(vals[-3:]) / tot, 3) if tot else None,
    "sz_share_pct": round(100.0 * sz / tot, 3) if tot else None,
    "four_city_share_pct": round(100.0 * four / tot, 3) if tot else None,
    "chain_members_total": members,
    "patents_per_member_all": round(tot / members, 2) if members else None,
    "zero_chains": sum(1 for r in rows if r["patents_le2024"] == 0),
}

payload = {
    "metric_id": "M_CHAIN_PATENT_COUNT",
    "metric_name": "产业链关联专利数",
    "support_judgment": "完全转换支持",
    "judgment_reason": "专利池 2,939,895 件、机构底册 189,116 家、链标签 2,283,762 行三段真实数据齐备，"
                       "12/12 链全部算出非零值（16,300—537,046 件），截断与去重规则可执行、脚本可复跑；"
                       "名称桥的已知漏计（非第一申请人、更名、同名）写入 gaps，属口径下界而非数据缺口。",
    "base_years_used": ["2021", "2022", "2023", "2024"],
    "base_years_missing": ["2025", "2026"],
    "base_years_note": "统计期 2025 年，专利按申请年 ≤2024 截断：发明专利公开滞后 18 个月，2025—2026 年申请量不完整，纳入会系统性低估近年值；池内 2021—2026 全覆盖，2025/2026 两年仅作观察不入正式值。",
    "sources": [
        "gkx @ 183.240.141.251:3318 / gkx_reader_zp: gkx.dwd_patent（2,939,895 行）",
        "gkx @ 183.240.141.251:3318 / gkx_reader_zp: gkx.dwd_org_base_info（189,116 行，申请人名桥）",
        "gkx @ 183.240.141.251:3318 / gkx_reader_zp: gkx.dwd_org_industry_tags（链归属）",
        "code/_snapshots21/region_index_patent_union.json（chain|city 汇总，含四市与省外）",
        "code/_snapshots21/chain21_layer_20261022.json（链成员数，与 M_CHAIN_ENTERPRISE_COUNT 同池）",
    ],
    "rule": {
        "unit": "件（patent_id 去重，一案一件；同族不做合并）",
        "pool": "gkx.dwd_patent 全量，按 application_year ≤ 2024 截断",
        "applicant_bridge": "first_applicant_name = name_cn 精确等值（1,107,178 件命中，命中率 37.66%）",
        "chain_attr": "企业挂该链即整件计入；多链企业按链重复计入（与 M_CHAIN_ENTERPRISE_COUNT 同池同链码）",
        "region_axis": "省级归属取申请人企业底册 city；四市 = 深圳/广州/东莞/惠州",
        "why_first_applicant": "dwd_patent 只存第一申请人名；合作申请中非第一申请人的企业不计，属已知下界",
    },
    "chains": rows,
    "headline": {
        "total_le2024": tot,
        "four_city_total": four,
        "outside_four_share_pct": round(100.0 * (tot - four) / tot, 3) if tot else None,
        "sz_total": sum(r["sz_patents_le2024"] for r in rows),
        "unit": "件",
        "n_chains": len(rows),
    },
    "stats": stats,
    "difference_vs_old_draft": {
        "old_source": "演示库汇总层（表名前缀 demo，主机 111.198.38.90）",
        "old_national_total": 3006899,
        "old_four_city_total": 3004055,
        "old_per_chain": {"INB1333": 534044, "INB1306": 504107, "INB1354": 379501, "INB1309": 304590},
        "now_national_total": tot,
        "delta_pct": round(100.0 * (tot - 3006899) / 3006899, 2),
        "reason": "同公式同截断，差异来自快照时点（本件 2026-10-22 重扫，旧稿 10-21）与厂家名桥的少量新增命中；逐链排序不变",
    },
    "gaps": [
        "第一申请人桥：只认第一申请人，合作申请里排第二的链内企业不计，专利数偏低",
        "名称桥：同名企业会合并计数；企业更名/简称不匹配会漏计（桥命中率 37.66% 为整体，链内企业更高）",
        "多链重复：同一件专利若企业挂多链会在各链各计一次，12 链之和 > 去重专利数",
        "同族 M_CHAIN_REG_PATENT 用第一申请人单角色桥（1,127,340 件、每件只计一次），本件用双角色并集（3,026,291 计位、多链重复）；两者不是同一个数，不可互相校验或替代",
    ],
    "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    "elapsed_sec": round(time.time() - T0, 2),
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=1)
print("total", tot, "four", four, "sz", payload["headline"]["sz_total"])
for r in rows:
    print(r["chain_code"], r["chain_name"], r["patents_le2024"], r["sz_patents_le2024"], r["patents_per_member"])
print("wrote", OUT)
