#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""政策时效（M_POLICY_VALIDITY_RATE）——负结论件：只证明「不可算」，不产出伪指标值。

注册表公式：
    COUNT(status=1 AND (expire_date IS NULL OR expire_date>=today)) / COUNT(*) * 100

实测（2026-10-23，`policy_struct_20261023.json`）：
  - `status` 20,000 行全为字符串「有效」，无第二个取值 → 条件一恒真；
  - `expire_date` 全表 0 行有值（`DATE_FORMAT` 后仍是 NULL，且无 '0000-00-00'）→ 条件二恒真；
  - 两条恒真条件相乘，结果必然是 100.00%，与数据无关。

因此本件判 **完全不支持**，产物里 `registered_metric_value` 置 null，
只保留 `constructive_validity_rate_pct=100.0` 作为「构造性恒真」的证据，
并给出 `verdict_kind="negative_evidence"`（派单书 v6 §七第 2 条：
判「完全不支持」的件必须有专门证明「为什么不可算」的脚本与产物）。

输入：code/_snapshots21/policy_struct_20261023.json
输出：code/M_POLICY_VALIDITY_RATE_out.json
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).parent
STRUCT = HERE / "_snapshots21" / "policy_struct_20261023.json"
DIMS = HERE / "_snapshots21" / "policy_dims_20261023.json"
OUT = HERE / "M_POLICY_VALIDITY_RATE_out.json"

METRIC = "M_POLICY_VALIDITY_RATE"


def main() -> int:
    st = json.loads(STRUCT.read_text(encoding="utf-8"))
    dims = json.loads(DIMS.read_text(encoding="utf-8"))
    v = st["validity"]
    rows = st["rows"]
    status_dist = v["status_dist"]

    status_valid = status_dist.get("有效", 0)
    status_other = rows - status_valid
    expire_null = v["expire_date_null"]
    expire_nonnull = v["expire_date_nonnull"]

    # 注册表公式在实测数据上的结果：条件一、条件二都恒真
    constructive = status_valid if expire_nonnull == 0 else None
    constructive_pct = round(constructive / rows * 100, 4) if constructive is not None else None

    out = {
        "metric_id": METRIC,
        "support_judgment": "完全不支持",
        "verdict_kind": "negative_evidence",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "截面指标，不设年度分母。本件不设基期不是因为「不需要时间」，"
            "而是因为失效判定所需的 expire_date 整列为空，任何按年切分都不会改变结论。"),
        "headline": {
            "policy_total": rows,
            "distinct_id": dims["distinct_id"],
            "status_distinct_values": len(status_dist),
            "status_valid_rows": status_valid,
            "status_other_rows": status_other,
            "expire_date_nonnull": expire_nonnull,
            "expire_date_null": expire_null,
            "expire_before_today": v["expire_before_today"],
            "expire_on_or_after_today": v["expire_on_or_after_today"],
            "implementation_date_nonnull": v["implementation_date_nonnull"],
            "registered_metric_value": None,
            "constructive_validity_rate_pct": constructive_pct,
            "constructive_reason": (
                "status 全为「有效」且 expire_date 全空，注册表公式的两个条件同时恒真，"
                "算出来必然是 100.00%，该值不随数据变化，不可作为指标值发布。"),
            "publishable": False,
            "max_measurable_validity_span_days": None,
        },
        "registered_formula": {
            "text": "COUNT(status=1 AND (expire_date IS NULL OR expire_date>=today)) / COUNT(*) * 100",
            "condition_1": "status=1（有效）",
            "condition_2": "expire_date IS NULL OR expire_date>=today",
            "condition_1_measured": f"{status_valid}/{rows} 行为「有效」，其余 {status_other} 行",
            "condition_2_measured": f"expire_date 有值 {expire_nonnull} 行、空 {expire_null} 行",
            "why_not_computable": (
                "两个条件在库内都恒真：条件一把全部行留下，条件二把全部行留下。"
                "公式在数学上可执行、在语义上无判别力——这就是「结构在、数据不在」。"),
        },
        "negative_evidence": [
            {"id": "E1", "dim": "status 取值域", "evidence": dict(status_dist),
             "verdict": f"唯一取值「有效」覆盖 {status_valid}/{rows} 行，无「已废止/已撤销/失效」，"
                        f"不能区分现行有效与失效"},
            {"id": "E2", "dim": "expire_date 填充", "evidence": {
                "nonnull": expire_nonnull, "null": expire_null,
                "expire_min": v["expire_min"], "expire_max": v["expire_max"],
                "expire_before_today": v["expire_before_today"],
                "expire_on_or_after_today": v["expire_on_or_after_today"]},
             "verdict": "整列 0 行有值；既没有「已过期」也没有「未过期」，时效判定无输入"},
            {"id": "E3", "dim": "implementation_date 填充", "evidence": {
                "nonnull": v["implementation_date_nonnull"],
                "null": v["implementation_date_null"]},
             "verdict": "实施日同样整列为空，无法用「实施日 + 有效期」侧算时效"},
            {"id": "E4", "dim": "发布日期可用性", "evidence": {
                "min": st["publish_date"]["min"], "max": st["publish_date"]["max"],
                "null_rows": st["publish_date"]["null_rows"]},
             "verdict": "发布日有值（1981-04-07—2024-02-18），但发布日不是失效日；"
                        "用它推算「已过 N 年即失效」属自造规则，本件不采用"},
            {"id": "E5", "dim": "口径自洽性", "evidence": {
                "expire_before_publish": v["expire_before_publish"]},
             "verdict": "无任何「失效日早于发布日」的行，是因为失效日全空，不是因为数据质量好"},
        ],
        "anomaly_scan": {
            "expire_before_publish": v["expire_before_publish"],
            "implementation_before_publish": v["implementation_before_publish"],
            "bad_publish_date_rows": st["publish_date"]["bad_zero_date_rows"],
            "note": "三项均为 0 行/3 行，前两项为 0 是「列全空」的结果，不能当作一致性通过。",
        },
        "repair_requirements": [
            {"field": "expire_date", "type": "date", "need": "逐条回填失效/截止日期；"
             "长周期规划类政策可留空（语义应为「长期有效」而不是「未知」）"},
            {"field": "invalid_date / abolish_date", "type": "date", "need": "政策被废止、"
             "被新文件替代的实际日期；这是「失效」的主口径，expire_date 只是预设截止日"},
            {"field": "status 值域", "type": "enum", "need": "至少区分 有效 / 已废止 / 已修订 / 未知，"
             "并说明「有效」是否包含「未标注」"},
        ],
        "checks": [
            {"name": "status 全表唯一值", "value": len(status_dist), "expected": 1,
             "ok": len(status_dist) == 1},
            {"name": "expire_date 全空", "value": expire_nonnull, "expected": 0,
             "ok": expire_nonnull == 0},
            {"name": "构造性 100% 与全表行数一致", "value": constructive, "expected": rows,
             "ok": constructive == rows},
        ],
        "provenance": {
            "snapshots": ["code/_snapshots21/policy_struct_20261023.json",
                          "code/_snapshots21/policy_dims_20261023.json"],
            "builders": ["code/_build_policy_struct_20261023.py",
                         "code/_build_policy_dims_20261023.py"],
            "source": dims["source"],
        },
        "notes": [
            "本件不发布任何「有效率」数值；100.00% 只是公式在同一批恒真条件上的算术结果。",
            "expire_date 列在 information_schema 里存在（date 类型），所以问题不是「缺列」，是「缺数」。",
            "2023—2026 采集断档与本指标无关：失效判定缺的是字段值，不是年份。",
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[OK] {OUT}")
    print("status", status_dist, "expire_nonnull", expire_nonnull,
          "constructive", constructive_pct)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
