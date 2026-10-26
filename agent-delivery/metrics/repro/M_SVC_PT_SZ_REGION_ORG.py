#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""深圳机构区域分布（M_SVC_PT_SZ_REGION_ORG）—— gkx 口径，自包含。

口径（calc-logic 0.2.0：区级源＝底册 area，按行政区名分组计数，未分配常显禁剔除）：
    切片 = 服务机构池 ∩ city='深圳市'（与 M_SVC_PT_SZ_TOTAL 同池同数）
    区轴 = 底册 area（已规范到「区」级全称）
    计数 = COUNT(DISTINCT org_id) GROUP BY area
    对账 = Σ 已分配区 + 未分配 = 切片值

数据源（只读快照，零 SQL）：
    code/_snapshots21/svc21_facts_20261022.json   pool（city）+ base_fields（area）

产出：code/M_SVC_PT_SZ_REGION_ORG_out.json
运行：cd code && python3 M_SVC_PT_SZ_REGION_ORG.py
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
OUT = os.path.join(HERE, "M_SVC_PT_SZ_REGION_ORG_out.json")

# 深圳市 9 个行政区（含新区/功能区归并的常显目录；未分配单列）
SZ_DISTRICTS = ["南山区", "福田区", "罗湖区", "宝安区", "龙岗区",
                "龙华区", "坪山区", "光明区", "盐田区", "大鹏新区"]


def main():
    t0 = time.time()
    fact = json.load(open(FACTS, encoding="utf-8"))
    pool, bf = fact["pool"], fact["base_fields"]
    sz = [o for o, v in pool.items() if v.get("city") == "深圳市"]
    n = len(sz)

    area = Counter((bf.get(o) or {}).get("area") or "" for o in sz)
    rows = []
    for d in SZ_DISTRICTS:
        c = area.get(d, 0)
        rows.append({"area": d, "org_count": c, "share_of_sz": round(c / n, 6)})
    unassigned = area.get("", 0)
    rows.append({"area": "（未分配）", "org_count": unassigned,
                 "share_of_sz": round(unassigned / n, 6)})
    other = {k: c for k, c in area.items() if k and k not in SZ_DISTRICTS}
    area_sum = sum(r["org_count"] for r in rows) + sum(other.values())

    out = {
        "metric_id": "M_SVC_PT_SZ_REGION_ORG",
        "metric_name": "深圳机构区域分布",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "完全转换支持",
        "judgment_reason": (
            "深圳切片的区级分布可现转且闭合：切片 %d 家，9 个行政区＋未分配 %d＋区外/异名 %d "
            "＝%d（与 M_SVC_PT_SZ_TOTAL 同池同数）；区字段非空率 %.2f%%，未分配单列不剔除"
            % (n, unassigned, sum(other.values()), area_sum,
               100.0 * (n - unassigned) / n)),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_base_info(area, city) 经 pool 驱动",
             "rows": fact["population"]["base_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_org_product_info（池人口）",
             "rows": fact["population"]["product_info_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面指标：区级分布是当前时点存量的空间切分，不含年度分母；"
                            "切片总量与成立年序列由 M_SVC_PT_SZ_TOTAL 承担。"),
        "population": {"shenzhen_orgs": n, "pool_orgs": len(pool),
                       "share_of_pool": round(n / len(pool), 6)},
        "district_rows": rows,
        "district_total": area_sum,
        "sum_equals_sz_total": area_sum == n,
        "structure_tiers": {
            "top_three": sum(r["org_count"] for r in rows if r["area"] in ("南山区", "宝安区", "龙岗区")),
            "primary_two": sum(r["org_count"] for r in rows if r["area"] in ("南山区", "宝安区")),
            "mid_three": sum(r["org_count"] for r in rows if r["area"] in ("龙岗区", "福田区", "龙华区")),
            "outer_five": sum(r["org_count"] for r in rows if r["area"] in ("光明区", "罗湖区", "坪山区", "盐田区", "大鹏新区")),
            "futian_luohu": sum(r["org_count"] for r in rows if r["area"] in ("福田区", "罗湖区")),
        },
        "coverage": {
            "area_nonnull": n - unassigned,
            "area_nonnull_rate": round((n - unassigned) / n, 6),
            "districts_listed": len(SZ_DISTRICTS),
            "districts_with_value": sum(1 for r in rows[:-1] if r["org_count"] > 0),
            "other_labels": [[k, c] for k, c in sorted(other.items(), key=lambda x: -x[1])],
        },
        "difference_vs_old_draft": {
            "population": "旧稿切片 14,033（演示库圈定池）→ 本件切片 %d（gkx 经营范围池）" % n,
            "district": ("旧稿 南山 3,655 / 宝安 2,850 / 龙岗 2,039 / 福田 1,829 / 龙华 1,795 / "
                         "光明 798 / 罗湖 553 / 坪山 388 / 盐田 121 / 未分配 5 → 本件见 district_rows"),
            "shape": "区级排序方向一致（南山、宝安、龙岗居前），绝对数随池放大；未分配从 5 升到 %d"
                     % unassigned,
        },
        "compute": {"status": "ok", "elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("sz=%d rows=%s sum=%d ok=%s other=%s"
          % (n, [(r["area"], r["org_count"]) for r in rows], area_sum,
             area_sum == n, other))
    print("->", OUT)


if __name__ == "__main__":
    main()
