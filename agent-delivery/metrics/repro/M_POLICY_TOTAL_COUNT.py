#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_POLICY_TOTAL_COUNT 政策总数 —— 只读共用快照，不连库。

数据源：code/_snapshots21/policy_dims_20261023.json（由 _build_policy_dims_20261023.py
一次窄投影扫描 gkx.dwd_policy_base 产出，五件共用）。
产出：code/M_POLICY_TOTAL_COUNT_out.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

MID = "M_POLICY_TOTAL_COUNT"
HERE = Path(__file__).parent
SNAP = HERE / "_snapshots21" / "policy_dims_20261023.json"
OUT = HERE / f"{MID}_out.json"


def pct(a, b):
    return round(a / b * 100, 4) if b else None


def main() -> int:
    s = json.loads(SNAP.read_text(encoding="utf-8"))
    rows = s["rows"]
    lv = {int(k): v for k, v in s["level_dist"].items()}
    prov = s["province_dist"]
    city = s["city_dist"]
    type_dist = s["type_dist"]
    year_dist = s["publish_year_dist"]

    prov_null = prov.get("__NULL__", 0)
    city_null = city.get("__NULL__", 0)
    type_null = type_dist.get("__NULL__", 0)
    year_null = year_dist.get("__NULL__", 0)
    prov_attr = rows - prov_null
    city_attr = rows - city_null
    type_attr = rows - type_null
    year_attr = rows - year_null

    level_rows = [
        {"level": 4, "label": "国家级", "n": lv.get(4, 0), "pct": pct(lv.get(4, 0), rows)},
        {"level": 3, "label": "省级（含省级+市级）", "n": lv.get(3, 0), "pct": pct(lv.get(3, 0), rows)},
        {"level": 2, "label": "市级", "n": lv.get(2, 0), "pct": pct(lv.get(2, 0), rows)},
        {"level": 1, "label": "区县级（含园区级）", "n": lv.get(1, 0), "pct": pct(lv.get(1, 0), rows)},
        {"level": 0, "label": "未标注", "n": lv.get(0, 0), "pct": pct(lv.get(0, 0), rows)},
    ]
    level_sum = sum(x["n"] for x in level_rows)

    est = s["known_estimate"]["information_schema_table_rows"]
    delta = rows - est

    res = {
        "metric_id": MID,
        "metric_name": "政策总数",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "support_judgment": "完全转换支持",
        "judgment_reason": (
            "底表 gkx.dwd_policy_base 的 COUNT(*) 与 COUNT(DISTINCT id) 都是 20,000，"
            "is_deleted 全为 0，主键无重复；层级、省份、城市、类型、年份五条切分口径"
            "都能在同一份底数上闭合（层级合计 20,000、省份 17,476+2,524、城市 10,294+9,706）。"
            "没有现成汇总表，但结构（主键+分类字段）与数据量都已足够，现在即可转换生成，"
            "故判完全转换支持。"
        ),
        "source": s["source"],
        "snapshot": "code/_snapshots21/policy_dims_20261023.json",
        "builder": "code/_build_policy_dims_20261023.py",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "截面指标：统计库内存量政策总数，不设年度分母、不做年度增速。"
            "publish_year 覆盖 1981—2024（非空 19,997 行，缺 3 行），"
            "2025/2026 零行；本件不把缺失年份按 0 摊入任何均值。"
        ),
        "headline": {
            "policy_total": rows,
            "distinct_id": s["distinct_id"],
            "is_deleted_nonzero": s["is_deleted_nonzero"],
        },
        "counts": {
            "policy_total": rows,
            "distinct_id": s["distinct_id"],
            "national_rows": lv.get(4, 0),
            "shenzhen_rows": s["sz"]["city_rows"],
            "guangdong_rows": prov.get("广东省", 0),
            "province_attributed_rows": prov_attr,
            "province_null_rows": prov_null,
            "city_attributed_rows": city_attr,
            "city_null_rows": city_null,
            "type_attributed_rows": type_attr,
            "type_null_rows": type_null,
            "publish_year_attributed_rows": year_attr,
            "publish_year_null_rows": year_null,
            "status_youxiao_rows": s["status_dist"].get("有效", 0),
            "bad_zero_date_rows": s["date_range"]["bad_zero_date_rows"],
        },
        "level_dist": level_rows,
        "level_sum": level_sum,
        "cross_checks": [
            {"name": "层级五档合计", "value": level_sum, "expected": rows, "ok": level_sum == rows},
            {"name": "省份：已归属 + 未归属", "value": prov_attr + prov_null, "expected": rows,
             "ok": prov_attr + prov_null == rows},
            {"name": "城市：已归属 + 未归属", "value": city_attr + city_null, "expected": rows,
             "ok": city_attr + city_null == rows},
            {"name": "类型：有值 + 字面 NULL", "value": type_attr + type_null, "expected": rows,
             "ok": type_attr + type_null == rows},
            {"name": "年份：有值 + 缺值", "value": year_attr + year_null, "expected": rows,
             "ok": year_attr + year_null == rows},
        ],
        "shares": {
            "national_pct_of_total": pct(lv.get(4, 0), rows),
            "shenzhen_pct_of_total": s["sz"]["share_of_total_pct"],
            "shenzhen_pct_of_guangdong": s["sz"]["share_of_guangdong_pct"],
            "province_null_pct_of_total": pct(prov_null, rows),
            "city_null_pct_of_total": pct(city_null, rows),
            "type_null_pct_of_total": pct(type_null, rows),
            "publish_year_null_pct_of_total": pct(year_null, rows),
        },
        "size_trap": {
            "information_schema_table_rows": est,
            "count_star_actual": rows,
            "delta": delta,
            "delta_pct": pct(delta, rows),
            "note": "table_rows 是 InnoDB 采样估算，偏差 +1,192 行（5.96%）；表规模一律用 COUNT(*)（DATA_FACTS §3.56）。",
        },
        "date_range": s["date_range"],
        "shenzhen_alt_count": {
            "city_field_rows": s["sz"]["city_rows"],
            "title_hit_rows": s["sz"]["title_hit_rows"],
            "city_or_title_rows": s["sz"]["city_or_title_rows"],
            "note": "city 精确匹配 879 是正式口径；标题命中 651 更少，二者并集 887（8 条仅标题提深圳）。",
        },
        "population_notes": [
            "分母是 20,000 行库内存量，不是全国政策总量；库内采集范围不等于政策发布总量。",
            "城市字段 9,706 行为字面 'NULL'，占比 48.53%：任何城市级占比都必须说明这半边不是有效城市。",
            "省份字段 2,524 行为字面 'NULL'，其中 2,174 行是国家级政策（level=4），按定义不归属任何省。",
            "status 20,000 行恒为「有效」，不能用它筛选现行有效政策。",
            "publish_year 缺 3 行、日期有 3 行 0000-00-00，三者是同一批省级记录。",
        ],
    }
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[OK] {OUT} total={rows} level_sum={level_sum}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
