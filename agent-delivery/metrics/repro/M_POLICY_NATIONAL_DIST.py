#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_POLICY_NATIONAL_DIST 全国政策分布 —— 只读共用快照，不连库。

按 `province` 归集到省级行政区；`province` 为字面 'NULL' 的 2,524 行单列，
其中 2,174 行是国家级政策（level=4，按定义不归属任何省），另 350 行是未归省。
产出：code/M_POLICY_NATIONAL_DIST_out.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

MID = "M_POLICY_NATIONAL_DIST"
HERE = Path(__file__).parent
SNAP = HERE / "_snapshots21" / "policy_dims_20261023.json"
OUT = HERE / f"{MID}_out.json"


def pct(a, b):
    return round(a / b * 100, 4) if b else None


def main() -> int:
    s = json.loads(SNAP.read_text(encoding="utf-8"))
    rows = s["rows"]
    prov = s["province_dist"]
    nat = s["national"]
    null_rows = prov.get("__NULL__", 0)
    attributed = rows - null_rows
    real = [(k, v) for k, v in prov.items() if k != "__NULL__"]
    real.sort(key=lambda x: -x[1])

    province_rows = [
        {"province": k, "n": v,
         "pct_of_total": pct(v, rows),
         "pct_of_attributed": pct(v, attributed),
         "rank": i + 1}
        for i, (k, v) in enumerate(real)
    ]
    top5 = sum(v for _, v in real[:5])
    top10 = sum(v for _, v in real[:10])
    hhi = round(sum((v / attributed) ** 2 for _, v in real), 6)

    non_national = rows - nat["level4_rows"]
    res = {
        "metric_id": MID,
        "metric_name": "全国政策分布",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "support_judgment": "完全转换支持",
        "judgment_reason": (
            "`province` 列 17,476 行有值（87.38%），覆盖 31 个省级行政区；"
            "未归省的 2,524 行里 2,174 行是国家级政策（level=4，按定义不属于任何省），"
            "剩下 350 行（占省级及以下政策的 1.9634%）未填省份。"
            "省级分布现在即可按 province 分组生成，结构与数据量都足够；"
            "国家级单列、未归省单列后合计回到 20,000，故判完全转换支持。"
        ),
        "source": s["source"],
        "snapshot": "code/_snapshots21/policy_dims_20261023.json",
        "builder": "code/_build_policy_dims_20261023.py",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "截面指标：统计库内政策按省的存量分布，不设年度分母、不做年度增速。"
            "publish_year 缺 3 行，不影响省级分组。"
        ),
        "headline": {
            "province_attributed_rows": attributed,
            "province_units_present": nat["provinces_present"],
            "province_null_rows": null_rows,
            "province_null_pct_of_total": pct(null_rows, rows),
            "national_rows": nat["level4_rows"],
            "non_national_rows": non_national,
            "non_national_unattributed_pct": pct(nat["province_null_non_national_rows"], non_national),
        },
        "province_dist": province_rows,
        "null_bucket": {
            "rows": null_rows,
            "pct_of_total": pct(null_rows, rows),
            "national_level4_rows": nat["province_null_national_rows"],
            "non_national_rows": nat["province_null_non_national_rows"],
            "beijing_city_without_province": nat["beijing_city_without_province"],
            "other_unattributed_rows": nat["province_null_non_national_rows"] - nat["beijing_city_without_province"],
            "beijing_undercount_pct": pct(nat["beijing_city_without_province"], s["city_dist"].get("北京市", 1)),
            "note": "国家级 2,174 行按定义不归省；其余 350 行里 336 行 city=北京市（北京市科委/中关村管委会来源），只有 14 行既无省也无有效市。",
        },
        "coverage": {
            "total_rows": rows,
            "attributed_rows": attributed,
            "attributed_pct": pct(attributed, rows),
            "non_national_attributed_pct": pct(attributed, non_national),
            "standard_units": nat["standard_units"],
            "units_present": nat["provinces_present"],
            "missing_units": nat["missing_standard_units"],
            "missing_units_note": "港澳台不在本库采集范围；不是「政策为零」，是「无记录」。",
        },
        "concentration": {
            "top5_rows": top5,
            "top5_pct_of_attributed": pct(top5, attributed),
            "top10_rows": top10,
            "top10_pct_of_attributed": pct(top10, attributed),
            "hhi": hhi,
            "uniform_hhi": round(1 / len(real), 6),
            "note": "HHI 按 17,476 条已归省记录计算，不含未归省桶；31 个省级单位的均匀分布 HHI 约为 0.0323。",
        },
        "cross_checks": {
            "sum_provinces_plus_null": sum(v for _, v in real) + null_rows,
            "expected": rows,
            "ok": sum(v for _, v in real) + null_rows == rows,
            "guangdong_rows": prov.get("广东省", 0),
            "shenzhen_rows": s["sz"]["city_rows"],
            "shenzhen_share_of_guangdong_pct": s["sz"]["share_of_guangdong_pct"],
        },
        "population_notes": [
            "使用 20,000 作分母时，必须有 12.62% 的『未归省』桶；只用 17,476 算占比等于把国家级政策排除，两种分母不可混用。",
            "北京在 province 字段是 1,932 条，但 city 字段是 2,268 条——差额 336 条是 province 未填的北京市级政策，省级排名会低估北京 14.82%（336/2,268）。",
            "国家级 2,174 条 city/province 全空，不能按「中央所在地=北京」摊进北京。",
            "港澳台 3 个单位在库内零记录，不能在地图上涂成 0 政策；应标『无采集』。",
        ],
    }
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[OK] {OUT} provinces={len(province_rows)} attributed={attributed} cr5={res['concentration']['top5_pct_of_attributed']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
