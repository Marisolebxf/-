#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_POLICY_INTENSITY_SCORE 政策力度评分 —— gkx 复现（2026-10-23）

口径（calc-logic/POLICY/M_POLICY_INTENSITY_SCORE.md，QPOL-02 未签）：
    单条政策三维五项：
      效果维  I(implementation_date 非空) / I(support_way 至少 1 条非空)
      覆盖维  COUNT(DISTINCT support_object) / I(district 非空)
      成本维  I(support_behavior 至少 1 条非空)（正本明写「无金额不编造拨款」）
    合成 = 各维截面 min-max → 缺维不进平均 → 等权 → ×100。

本件是「单政策版」，与同批已交付的 M_POLICY_INTENSITY_INDEX（城市版）读同一批字段、
判同一个档：五项里四项为 0，三维里两维整块为空，只剩「区县落地标记」一项，
0 个完整维。按正本「缺维不进平均」，可进平均的维集合为空 → 不出分。

因此本脚本是**否定性证据探针**（verdict_kind="negative_evidence"）：
它不产出任何分数，只产出「为什么不能出分」的五项计数、字段类型、以及
「政策表里连金额列都没有」的列级证据。gate 对「完全不支持」档要求 py + out.json，
本文件即该要求下的证据面。

输入：code/_snapshots21/policy_struct_20261023.json（elements / validity 两段）
      code/_snapshots21/policy_text_20261023.json（district 不在其中，仅用于核对总行数）
      code/_snapshots21/policy_base_20261021.json（district / city / level）
输出：code/M_POLICY_INTENSITY_SCORE_out.json
"""
from __future__ import annotations

import collections
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_POLICY_INTENSITY_SCORE_out.json"

NULLS = ("__NULL__", "NULL", "")


def main() -> int:
    struct = json.load(open(SNAP / "policy_struct_20261023.json", encoding="utf-8"))
    base = json.load(open(SNAP / "policy_base_20261021.json", encoding="utf-8"))
    el = struct["elements"]
    va = struct["validity"]
    n = struct["rows"]

    district_rows = [r for r in base if (r.get("district") or "") not in NULLS]
    district_vals = collections.Counter(r.get("district") for r in district_rows)
    by_city = collections.Counter(r.get("city") for r in district_rows)

    subitems = [
        {"dim": "效果", "item": "实施日完备率", "field": "implementation_date",
         "nonnull": va["implementation_date_nonnull"], "denominator": n, "computable": False,
         "evidence": "全表 20,000 行取值为 0000-00-00（date 列的非 NULL 零值），COUNT(col) 会给 20,000 的假象，"
                     "按 DATE_FORMAT 归一后有效日期 0 行"},
        {"dim": "效果", "item": "支持方式完备率", "field": "policy_support.support_way",
         "nonnull": el["support_way_rows"], "denominator": n, "computable": False,
         "evidence": "policy_support 20,000 行 JSON_TYPE='NULL'；JSON_LENGTH(null) 返回 1，不能用它判空"},
        {"dim": "覆盖", "item": "支持对象种类数", "field": "policy_support.support_object",
         "nonnull": el["support_object_rows"], "denominator": n, "computable": False,
         "evidence": "同上，JSON null，子键无法读取"},
        {"dim": "覆盖", "item": "区县落地标记", "field": "district",
         "nonnull": el["district_nonnull"], "denominator": n, "computable": True,
         "evidence": "1,165 行有值、872 行是字面 'NULL'；有值的集中在少数城市，且区名取值只有少数几种"},
        {"dim": "成本", "item": "扶持行为完备率", "field": "policy_support.support_behavior",
         "nonnull": el["support_behavior_rows"], "denominator": n, "computable": False,
         "evidence": "JSON null；且表内无任何金额列，不能用金额顶替（见 amount_columns_probe）"},
    ]

    dims = [
        {"dim": "效果", "items": 2, "computable_items": 0, "full": False},
        {"dim": "覆盖", "items": 2, "computable_items": 1, "full": False},
        {"dim": "成本", "items": 1, "computable_items": 0, "full": False},
    ]

    out = {
        "metric_id": "M_POLICY_INTENSITY_SCORE",
        "verdict_kind": "negative_evidence",
        "support_judgment": "完全不支持",
        "publishable": False,
        "registered_metric_value": None,
        "headline": {
            "policy_total": n,
            "sub_items_total": 5,
            "sub_items_computable": 1,
            "dims_total": 3,
            "dims_full": 0,
            "dims_empty": 2,
            "score": None,
            "reason": ("按正本「缺维不进平均」，可进平均的完整维为 0 个 → 分数不存在。"
                       "三项里两项整块为空（效果、成本），覆盖维只剩区县标记一项。"),
        },
        "sub_items": subitems,
        "dims": dims,
        "district_probe": {
            "rows_with_district": len(district_rows),
            "rows_without_district": n - len(district_rows),
            "distinct_district_values": len(district_vals),
            "top_values": district_vals.most_common(10),
            "rows_by_city": by_city.most_common(10),
            "note": ("区县字段只有 1,165 行有值（5.825%），且取值集中在少数城市；"
                     "把它当作「政策落到区县」的唯一证据，等于让 94.175% 的政策恒取 0"),
        },
        "validity_probe": {
            "status_dist": va["status_dist"],
            "expire_date_nonnull": va["expire_date_nonnull"],
            "implementation_date_nonnull": va["implementation_date_nonnull"],
            "note": "status 单值「有效」+ expire_date 全空 → 「有效」条件恒真，不构成任何区分度",
        },
        "amount_columns_probe": {
            "policy_table_columns": 33,
            "amount_like_columns_in_policy_tables": 0,
            "amount_like_columns_in_gkx": 123,
            "scope": "123 个金额类列全部落在 dwd_bid_* 招标表；dwd_policy_base 33 列里没有任何金额/资金/补贴列",
            "rule": "无源维度置 null，不置 0；不得自造「资金强度」",
        },
        "result_surface_absent": {
            "gkx_policy_tables": ["dwd_policy_base", "dwd_policy_base_bak_20260923",
                                  "dwd_global_policy_base", "dwd_global_policy_base_bak_20260923"],
            "ads_policy_intensity": "不存在（gkx 只有 dwd_* 层）",
            "note": "注册表 source_tables 写的是 ads.policy_intensity，该表在 gkx 侧不存在",
        },
        "probes": {
            "support_json_type_dist": el["support_json_type_dist"],
            "support_way_rows": el["support_way_rows"],
            "support_object_rows": el["support_object_rows"],
            "support_behavior_rows": el["support_behavior_rows"],
            "district_nonnull": el["district_nonnull"],
            "implementation_date_nonnull": va["implementation_date_nonnull"],
        },
        "reused_from": "code/_snapshots21/policy_struct_20261023.json",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面件：本件不出分、不设基期。政策池为 20,000 条存量全表；"
                            "若将来补数后要按年出分，须先解决 2023/2024 的采集断档，"
                            "否则「某年力度为 0」会是断档而不是真实归零。"),
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("support_judgment", "headline")},
                     ensure_ascii=False, indent=1))
    print(json.dumps(out["district_probe"], ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
