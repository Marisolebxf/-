#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_POLICY_SZ_DIST 深圳政策分布 —— 只读共用快照，不连库。

深圳用 `city='深圳市'` 精确匹配（不用 LIKE '%深圳%'，避免标题提及被误计）。
需求要的是「深圳各区分布」，但 `district` 在深圳 879 条里 872 条为字面 'NULL'，
区级维度不可用；本件交付「市级总量 + 层级/文种/年份结构」，区级只列 7 条实测。
产出：code/M_POLICY_SZ_DIST_out.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

MID = "M_POLICY_SZ_DIST"
HERE = Path(__file__).parent
SNAP = HERE / "_snapshots21" / "policy_dims_20261023.json"
OUT = HERE / f"{MID}_out.json"


def pct(a, b):
    return round(a / b * 100, 4) if b else None


def main() -> int:
    s = json.loads(SNAP.read_text(encoding="utf-8"))
    rows = s["rows"]
    sz = s["sz"]
    n = sz["city_rows"]

    district_rows = [
        {"district": k, "n": v, "pct_of_sz": pct(v, n)}
        for k, v in sz["district_dist"].items()
    ]
    rank_rows = [{"rank": k, "n": v, "pct_of_sz": pct(v, n)}
                 for k, v in sz["rank_dist"].items()]
    level_rows = [{"level": int(k), "n": v, "pct_of_sz": pct(v, n)}
                  for k, v in sorted(sz["level_dist"].items(), key=lambda x: -int(x[0]))]
    type_rows = [{"type": k, "n": v, "pct_of_sz": pct(v, n)}
                 for k, v in sz["type_dist"].items()]
    year_rows = [{"year": k, "n": v, "pct_of_sz": pct(v, n)}
                 for k, v in sz["publish_year_dist"].items()]
    real_years = [int(k) for k in sz["publish_year_dist"] if k != "__NULL__"]
    latest_year = max(real_years) if real_years else None

    city = s["city_dist"]
    res = {
        "metric_id": MID,
        "metric_name": "深圳政策分布",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "support_judgment": "部分支持",
        "judgment_reason": (
            "深圳总量可算：city='深圳市' 879 条，占全库 4.395%、占广东 54.5285%；"
            "层级、文种、年份结构也可算。但需求要的「深圳各区分布」不可算——"
            "879 条里 district 为字面 'NULL' 的有 872 条（99.2048%），只有盐田 4、"
            "光明 1、南山 1、大鹏新区 1 共 7 条有区县。区级维度始终缺数据，故判部分支持。"
        ),
        "source": s["source"],
        "snapshot": "code/_snapshots21/policy_dims_20261023.json",
        "builder": "code/_build_policy_dims_20261023.py",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "截面指标：统计库内深圳政策存量，不做年度增速、不设年度分母。"
            "深圳 publish_year 实测 2000—2022，2023/2024 零行；2025/2026 零行，"
            "不把这些年份按 0 摊入任何均值。"
        ),
        "headline": {
            "shenzhen_rows": n,
            "share_of_total_pct": sz["share_of_total_pct"],
            "share_of_guangdong_pct": sz["share_of_guangdong_pct"],
            "district_missing_rows": sz["district_missing_rows"],
            "district_missing_pct": pct(sz["district_missing_rows"], n),
            "latest_year": latest_year,
        },
        "counts": {
            "total_rows": rows,
            "shenzhen_rows": n,
            "guangdong_rows": s["province_dist"].get("广东省", 0),
            "beijing_rows": city.get("北京市", 0),
            "shanghai_rows": city.get("上海市", 0),
            "tianjin_rows": city.get("天津市", 0),
            "district_observed_rows": n - sz["district_missing_rows"],
            "title_hit_rows": sz["title_hit_rows"],
            "city_or_title_rows": sz["city_or_title_rows"],
        },
        "shape": {
            "district_kinds": len(district_rows),
            "rank_kinds": len(rank_rows),
            "type_kinds": len(type_rows),
            "year_kinds": len(year_rows),
            "ministry_top_n": len(sz["ministry_top10"]),
        },
        "district_dist": district_rows,
        "rank_dist": rank_rows,
        "level_dist": level_rows,
        "type_dist": type_rows,
        "publish_year_dist": year_rows,
        "ministry_top10": sz["ministry_top10"],
        "date_range": {
            "min_publish_date": sz["min_publish_date"],
            "max_publish_date": sz["max_publish_date"],
            "latest_year": latest_year,
            "year_2023_rows": sz["publish_year_dist"].get("2023", 0),
            "year_2024_rows": sz["publish_year_dist"].get("2024", 0),
        },
        "name_matching": {
            "city_field_rows": n,
            "title_hit_rows": sz["title_hit_rows"],
            "city_or_title_rows": sz["city_or_title_rows"],
            "title_only_rows": sz["city_or_title_rows"] - n,
            "note": "正式口径用 city 精确匹配；标题只命中 651 条，比 city 少 228 条，说明『标题未写深圳』不等于『不是深圳政策』。并集 887 条，多出的 8 条是仅标题提深圳、city 为 NULL 的记录，不纳入正式口径。",
        },
        "population_notes": [
            "分母有两个：占全库用 20,000（深圳 4.395%）；占广东用 1,612（深圳 54.5285%）。两个分母含义不同，不可混用。",
            "district 的 872 条字面 'NULL' 不是 SQL NULL，`IS NULL` 查不到，必须按字面值过滤。",
            "2023/2024 在深圳切片里零行，是采集断档，不是深圳停止发文；不得据此写『政策归零』。",
            "深圳 879 条里没有一条国家级（level=4）；国家级政策 city 全空，不能算进深圳。",
        ],
    }
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[OK] {OUT} sz={n} districts={len(district_rows)} latest={latest_year}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
