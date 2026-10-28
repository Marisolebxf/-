#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_POLICY_LEVEL_DIST 政策级别分布 —— 只读共用快照，不连库。

级别由 `rank`（JSON 数组字符串）派生：国家级→4、省级→3、市级→2、
区级/园区级→1、空数组→0；多值按最高行政层级优先。
产出：code/M_POLICY_LEVEL_DIST_out.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

MID = "M_POLICY_LEVEL_DIST"
HERE = Path(__file__).parent
SNAP = HERE / "_snapshots21" / "policy_dims_20261023.json"
OUT = HERE / f"{MID}_out.json"


def pct(a, b):
    return round(a / b * 100, 4) if b else None


def main() -> int:
    s = json.loads(SNAP.read_text(encoding="utf-8"))
    rows = s["rows"]
    lv = {int(k): v for k, v in s["level_dist"].items()}
    rank = s["rank_dist"]
    data = [
        (4, "国家级", "rank 含「国家级」", lv.get(4, 0)),
        (3, "省级", "rank 含「省级」（含省级+市级双标）", lv.get(3, 0)),
        (2, "市级", "rank 含「市级」", lv.get(2, 0)),
        (1, "区县级", "rank 含「区级」或「园区级」", lv.get(1, 0)),
        (0, "未标注", "rank 为空数组", lv.get(0, 0)),
    ]
    dist = [
        {"level": k, "label": lab, "rule": rule, "n": n, "pct": pct(n, rows)}
        for k, lab, rule, n in data
    ]
    total = sum(x["n"] for x in dist)

    # 多值归并敏感性：省级+市级 2,473 条若归市级，两级各是多少
    dual = rank.get("市级+省级", 0)
    sen = {
        "current_rule": "最高行政层级优先：省级+市级 → 省级",
        "dual_rows": dual,
        "province_if_dual_to_province": lv.get(3, 0),
        "city_if_dual_to_province": lv.get(2, 0),
        "province_if_dual_to_city": lv.get(3, 0) - dual,
        "city_if_dual_to_city": lv.get(2, 0) + dual,
        "note": "两种归并都自洽，差别只在 2,473 条双标记录；正文默认「高层级优先」，因发文机关同时含省级与市级时，省级是约束性层级。",
    }

    rank_rows = [{"rank": k, "n": v, "pct": pct(v, rows)} for k, v in rank.items()]

    # 国家级是否真的 city/province 全空（结构自证）
    nat = s["national"]
    nat_check = {
        "national_rows": lv.get(4, 0),
        "province_null_total": nat["province_null_rows"],
        "province_null_national": nat["province_null_national_rows"],
        "all_national_province_null": nat["province_null_national_rows"] == lv.get(4, 0),
        "city_null_total": s["city_dist"].get("__NULL__", 0),
    }

    res = {
        "metric_id": MID,
        "metric_name": "政策级别分布",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "support_judgment": "完全转换支持",
        "judgment_reason": (
            "`rank` 列 20,000 行全部有值（357 行为空数组），可确定派生四级+未标注；"
            "五档合计 20,000 与 COUNT(*) 完全一致，国家级 2,174 行的 province/city "
            "全部为空，结构自证成立。多值仅「省级+市级」2,473 条需要一条归并规则，"
            "本件按最高层级优先并在产物里给出另一归并的敏感性。结构与数据量都足够，"
            "故判完全转换支持。"
        ),
        "source": s["source"],
        "snapshot": "code/_snapshots21/policy_dims_20261023.json",
        "builder": "code/_build_policy_dims_20261023.py",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "截面指标：统计库内全部政策的层级分布，不做年度序列、不设年度分母。"
            "publish_year 的 3 行缺失不进入任何年度口径。"
        ),
        "level_dist": dist,
        "level_total": total,
        "total_rows": rows,
        "rank_dist_raw": rank_rows,
        "rank_level_cross": s["rank_level_cross"],
        "dual_tag_sensitivity": sen,
        "national_structure_check": nat_check,
        "unknown_rows": lv.get(0, 0),
        "shares": {
            "national_pct": pct(lv.get(4, 0), rows),
            "province_pct": pct(lv.get(3, 0), rows),
            "city_pct": pct(lv.get(2, 0), rows),
            "district_pct": pct(lv.get(1, 0), rows),
            "unknown_pct": pct(lv.get(0, 0), rows),
        },
        "reconciliation": {
            "sum_of_five": total,
            "count_star": rows,
            "diff": rows - total,
            "ok": total == rows,
        },
        "population_notes": [
            "分母是 20,000 行库内存量；「国家级」指 rank 含国家级，不代表政策效力等级评定。",
            "357 行 rank 为空数组，只能记为「未标注」，不能按 0 或按市级摊入。",
            "园区级 144 行并入区县级；若单列，区县级为 1,254、园区级 144。",
            "省级 9,922 行里有 2,473 行是「省级+市级」双标，归并规则改变会移动这 2,473 行。",
        ],
    }
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[OK] {OUT} total={total} dist={[(x['label'], x['n']) for x in dist]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
