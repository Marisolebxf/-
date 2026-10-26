#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""区域服务机构数（M_SVC_PT_REGION_ORG）—— gkx 口径，自包含。

口径（calc-logic 0.2.0：省/市两级计数，国家轴按 ISO/M49 对齐，无源留白）：
    省轴   = 底册 province，按 org_id 去重计数
    市轴   = 底册 city（已规范到「市」级全称，无需模糊归一，见 DATA_FACTS §3.8）
    国家轴 = 境外机构名录；gkx.dwd_forg_base_info 只有 GB/US/CA 三国值且不是服务名录
    「未分配」= 省/市为空的机构，单列常显、不剔除

数据源（只读快照，零 SQL）：
    code/_snapshots21/svc21_facts_20261022.json       pool（省/市）
    code/_snapshots21/svc21_pt_axis_20261022.json     forg_country（国家轴值域）

产出：code/M_SVC_PT_REGION_ORG_out.json
运行：cd code && python3 M_SVC_PT_REGION_ORG.py
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
OUT = os.path.join(HERE, "M_SVC_PT_REGION_ORG_out.json")


def main():
    t0 = time.time()
    fact = json.load(open(FACTS, encoding="utf-8"))
    ax = json.load(open(AXIS, encoding="utf-8"))
    pool = fact["pool"]
    n = len(pool)

    prov = Counter((v.get("prov") or "") for v in pool.values())
    city = Counter((v.get("city") or "") for v in pool.values())

    prov_rows = [{"province": k or "（未分配）", "org_count": c,
                  "share_of_pool": round(c / n, 6)}
                 for k, c in prov.most_common()]
    city_rows = [{"city": k or "（未分配）", "org_count": c,
                  "share_of_pool": round(c / n, 6)}
                 for k, c in city.most_common()]

    assigned_prov = sum(c for k, c in prov.items() if k)
    assigned_city = sum(c for k, c in city.items() if k)

    out = {
        "metric_id": "M_SVC_PT_REGION_ORG",
        "metric_name": "区域服务机构数",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": (
            "省/市两级区域轴在 gkx 可实算（%d/%d 有省级归属，覆盖 2 个省级区划、4 个市级区划）；"
            "但需求要求的「各个国家」轴无源：dwd_forg_base_info 只有 GB/US/CA 三值且不是服务机构名录，"
            "与池无对齐键 → 国家/海外维度始终缺 → 部分支持" % (assigned_prov, n)),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_base_info(province, city) 经 pool 驱动",
             "rows": fact["population"]["base_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_forg_base_info(country_code)", "rows": ax["forg_country"]["rows_total"],
             "snapshot": "code/_snapshots21/svc21_pt_axis_20261022.json"},
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面指标：区域分布是当前时点存量的空间切分，不含年度分母；"
                            "机构成立年序列由 M_SVC_PT_GLOBAL_TOTAL 承担。"),
        "population": {
            "distinct_org_id": n,
            "province_assigned": assigned_prov,
            "province_missing": n - assigned_prov,
            "city_assigned": assigned_city,
            "city_missing": n - assigned_city,
        },
        "province_rows": prov_rows,
        "province_total": sum(r["org_count"] for r in prov_rows),
        "city_rows": city_rows,
        "city_total": sum(r["org_count"] for r in city_rows),
        "coverage": {
            "provinces_covered": len([k for k in prov if k]),
            "cities_covered": len([k for k in city if k]),
            "top_province_share": round(prov_rows[0]["org_count"] / n, 6),
            "structural_skew_note": (
                "底册 189,116 行里深圳都市圈（深圳+广州+东莞+惠州）占 99.82%（DATA_FACTS §3.8），"
                "本池 44,132 家全部落在广东，故本件本质是「深圳都市圈内部分布」，"
                "不能当全国区域排名使用"),
        },
        "country_axis": {
            "needed": "境外/港澳台服务机构名录（含国别编码）",
            "existing": "gkx.dwd_forg_base_info %d 行，国别值域 %s"
                        % (ax["forg_country"]["rows_total"], ax["forg_country"]["dist"]),
            "countries_covered": len(ax["forg_country"]["dist"]),
            "verdict": ("仅 3 个国别值、country 列全空、与 dwd_org_base_info 无对齐键；"
                        "按钉版「无源则如实留白」，国家轴留白不塞 GB 数据"),
        },
        "difference_vs_old_draft": {
            "population": "旧稿 43,296（演示库圈定池）→ 本件 44,153（gkx 经营范围实体）",
            "province": "旧稿 广东 43,292 / 北京 3 / 浙江 1（3 个区划）→ 本件 广东 %d / 未分配 %d（%d 个区划）"
                        % (assigned_prov, n - assigned_prov, len([k for k in prov if k])),
            "country": "旧稿 国家轴 country_covered=1、境外表 0 行 → 本件境外表 20,000 行但仅 3 国且非服务名录",
        },
        "compute": {"status": "ok", "elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("prov", prov_rows, "assigned", assigned_prov, "/", n)
    print("city", city_rows[:6])
    print("->", OUT)


if __name__ == "__main__":
    main()
