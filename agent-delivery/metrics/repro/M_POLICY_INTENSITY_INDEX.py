#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""政策力度指数（M_POLICY_INTENSITY_INDEX）——负结论件：证明三维口径不可算。

注册口径（`calc-logic/POLICY/M_POLICY_INTENSITY_INDEX.md`）：
  按城市从效果、覆盖、成本三维评定，0—100。五个三级指标：
    效果维：实施日完备占比（implementation_date 非空 / N_c）
            支持方式完备占比（policy_support.support_way 非空 / N_c）
    覆盖维：支持对象种类数（DISTINCT support_object）
            区县去重数（DISTINCT district）
    成本维：扶持行为完备占比（policy_support.support_behavior 非空 / N_c）
  各维截面 min-max 后等权 ×100；缺维不补 0、不进平均；全样本同值取 0.5。

实测（2026-10-23）：
  - implementation_date 有值 0 / 20,000；
  - policy_support 20,000 行全是 JSON null，support_way / support_object /
    support_behavior 三个键一个都不存在（`JSON_LENGTH` 对 JSON null 返回 1，不能拿来判空）；
  - district 有值 1,165 / 20,000（5.825%）。
五个三级指标里四个恒为 0，唯一有值的「区县去重数」是覆盖维的一半。
按 calc-logic，缺维不补 0 但也不进平均 → 三维平均只剩「覆盖维的区县去重数」，
那不是「政策力度」，是本件不能把它包装成指数发布的原因。

判定：**完全不支持**（关键依赖字段结构在、数据不在；无任何可算闭环）。
产物 `verdict_kind="negative_evidence"`，`registered_metric_value=null`。

输入：code/_snapshots21/policy_struct_20261023.json
输出：code/M_POLICY_INTENSITY_INDEX_out.json
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).parent
STRUCT = HERE / "_snapshots21" / "policy_struct_20261023.json"
DIMS = HERE / "_snapshots21" / "policy_dims_20261023.json"
OUT = HERE / "M_POLICY_INTENSITY_INDEX_out.json"

METRIC = "M_POLICY_INTENSITY_INDEX"

# 参与对比的城市篮（与 M_POLICY_INDUSTRY_FIT 共用，便于两件对账）
BASKET = ["深圳市", "北京市", "上海市", "广州市", "杭州市", "南京市",
          "合肥市", "成都市", "武汉市", "西安市"]


def main() -> int:
    st = json.loads(STRUCT.read_text(encoding="utf-8"))
    dims = json.loads(DIMS.read_text(encoding="utf-8"))
    el = st["elements"]
    v = st["validity"]
    rows = st["rows"]
    prof = st["city_profile"]

    sub = [
        {"dim": "效果", "sub": "实施日完备占比", "field": "implementation_date",
         "nonnull": v["implementation_date_nonnull"], "denominator": rows,
         "computable": v["implementation_date_nonnull"] > 0},
        {"dim": "效果", "sub": "支持方式完备占比", "field": "policy_support.support_way",
         "nonnull": el["support_way_rows"], "denominator": rows,
         "computable": el["support_way_rows"] > 0},
        {"dim": "覆盖", "sub": "支持对象种类数", "field": "policy_support.support_object",
         "nonnull": el["support_object_rows"], "denominator": rows,
         "computable": el["support_object_rows"] > 0},
        {"dim": "覆盖", "sub": "区县去重数", "field": "district",
         "nonnull": el["district_nonnull"], "denominator": rows,
         "computable": el["district_nonnull"] > 0},
        {"dim": "成本", "sub": "扶持行为完备占比", "field": "policy_support.support_behavior",
         "nonnull": el["support_behavior_rows"], "denominator": rows,
         "computable": el["support_behavior_rows"] > 0},
    ]

    dim_status = {}
    for d in ("效果", "覆盖", "成本"):
        mine = [s for s in sub if s["dim"] == d]
        dim_status[d] = {
            "sub_total": len(mine),
            "sub_computable": sum(1 for s in mine if s["computable"]),
            "dim_computable": any(s["computable"] for s in mine),
            "dim_full": all(s["computable"] for s in mine),
        }

    city_rows = []
    for c in BASKET:
        p = prof.get(c)
        if not p:
            continue
        city_rows.append({
            "city": c,
            "policies": p["rows"],
            "implementation_date_rows": p["impl_rows"],
            "support_way_rows": p["support_way_rows"],
            "support_object_rows": p["support_object_rows"],
            "support_behavior_rows": p["support_behavior_rows"],
            "district_distinct": p["district_distinct"],
        })

    out = {
        "metric_id": METRIC,
        "support_judgment": "完全不支持",
        "verdict_kind": "negative_evidence",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "截面指标（按城市），不设年度分母。calc-logic 的入集是「status=有效且未过期」，"
            "但 status 恒真、expire_date 全空（见 M_POLICY_VALIDITY_RATE），"
            "所以本件的入集等价于全表 20,000 行；这不是年份问题。"),
        "headline": {
            "policy_total": rows,
            "cities_total": len(st["city_dist"]) - 1,
            "cities_in_basket": len(city_rows),
            "sub_indicators_total": len(sub),
            "sub_indicators_computable": sum(1 for s in sub if s["computable"]),
            "dims_total": 3,
            "dims_full": sum(1 for d in dim_status.values() if d["dim_full"]),
            "dims_empty": sum(1 for d in dim_status.values() if not d["dim_computable"]),
            "registered_metric_value": None,
            "publishable": False,
            "why": ("五个三级指标四个恒为 0（implementation_date / support_way / "
                    "support_object / support_behavior 全部整列空），"
                    "三维里两维整块不可算；按 calc-logic「缺维不补 0 不进平均」，"
                    "合成后只剩覆盖维的区县去重数，已不构成「政策力度」。"),
        },
        "sub_indicators": sub,
        "dimension_status": dim_status,
        "city_rows": city_rows,
        "negative_evidence": [
            {"id": "E1", "dim": "policy_support JSON 类型",
             "evidence": el["support_json_type_dist"],
             "verdict": "20,000 行全部是 JSON null（小写 null），不是空对象 {}、"
                        "也不是缺列；三个子键无法读取"},
            {"id": "E2", "dim": "support_way / support_object / support_behavior 填充",
             "evidence": {"support_way_rows": el["support_way_rows"],
                          "support_object_rows": el["support_object_rows"],
                          "support_behavior_rows": el["support_behavior_rows"]},
             "verdict": "三个子键命中行数均为 0；效果维与成本维、覆盖维的一半因此不可算"},
            {"id": "E3", "dim": "implementation_date 填充",
             "evidence": {"nonnull": v["implementation_date_nonnull"],
                          "null": v["implementation_date_null"]},
             "verdict": "整列为空，效果维的另一半同样不可算"},
            {"id": "E4", "dim": "district 填充",
             "evidence": {"nonnull": el["district_nonnull"],
                          "null": rows - el["district_nonnull"]},
             "verdict": "仅 1,165 行有区县（5.825%），覆盖维只剩这一半；"
                        "且这 1,165 行集中在深圳等少数城市的区级文件，截面不可比"},
            {"id": "E5", "dim": "金额列",
             "evidence": {"amount_columns_in_table": [],
                          "support_amount_rows": 0},
             "verdict": "表内没有任何扶持金额列（calc-logic 也把 support_amount 列为「待建字段」），"
                        "成本维不能改用金额口径，也不得自造「资金强度」"},
        ],
        "city_level_counts": {
            c: {
                "policies": p["rows"],
                "district_distinct": p["district_distinct"],
            } for c, p in st["city_profile"].items()
        },
        "repair_requirements": [
            {"field": "policy_support.support_way", "need": "按政策逐条抽「支持方式」"
             "（补助/贴息/奖励/税收优惠…），并约定多值编码"},
            {"field": "policy_support.support_object", "need": "抽「支持对象」"
             "（企业/平台/人才/园区…），至少能 DISTINCT 计数"},
            {"field": "policy_support.support_behavior", "need": "抽「扶持行为」"
             "（研发补贴/设备购置/场景开放…）"},
            {"field": "implementation_date", "need": "回填实施日；缺失时应区分"
             "「发布即实施」与「未标注」"},
            {"field": "support_amount", "need": "若甲方坚持成本维用金额，必须先建该字段并逐条抽取；"
             "本表连金额列都没有，不能用正文正则抽（正文与摘要存在三个数量级矛盾的样本）"},
        ],
        "checks": [
            {"name": "policy_support 全为 JSON null",
             "value": el["support_json_type_dist"].get("JSON_NULL", 0),
             "expected": rows, "ok": el["support_json_type_dist"].get("JSON_NULL", 0) == rows},
            {"name": "四个整列空字段合计",
             "value": (v["implementation_date_nonnull"] + el["support_way_rows"]
                       + el["support_object_rows"] + el["support_behavior_rows"]),
             "expected": 0, "ok": (v["implementation_date_nonnull"] + el["support_way_rows"]
                                   + el["support_object_rows"]
                                   + el["support_behavior_rows"]) == 0},
            {"name": "可算子指标数",
             "value": sum(1 for s in sub if s["computable"]), "expected": 1,
             "ok": sum(1 for s in sub if s["computable"]) == 1},
        ],
        "provenance": {
            "snapshots": ["code/_snapshots21/policy_struct_20261023.json",
                          "code/_snapshots21/policy_dims_20261023.json"],
            "builders": ["code/_build_policy_struct_20261023.py",
                         "code/_build_policy_dims_20261023.py"],
            "source": dims["source"],
        },
        "notes": [
            "本件不产出 0—100 的分数；任何这样的分数都只能来自「区县去重数」一项，"
            "会被误读成政策力度。",
            "policy_support 是 JSON 列，JSON_LENGTH(null)=1，用 JSON_LENGTH 判空会得出"
            "「20,000 行全部有值」的错误结论。",
            "20,000 条里有 9,706 条无城市（含 2,174 条国家级），城市级分母不能直接用 20,000。",
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[OK] {OUT}")
    print("sub computable", out["headline"]["sub_indicators_computable"], "/", len(sub))
    print("dims", dim_status)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
