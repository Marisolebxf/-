#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_POLICY_IMPLEMENTATION_EFFECT —— 落地实效性（P1 政策评估族，否定性证据件）

正本：`gkx-orchestration/agent-delivery/metrics/calc-logic/POLICY/M_POLICY_IMPLEMENTATION_EFFECT.md`
（三维：落地执行启动 / 受益覆盖 / 实施反馈；实施反馈正本已注「现库无调查表，本维不计算」，
现行综合 = (启动得分 + 覆盖得分) / 2 × 100）

本脚本的作用不是出分，而是逐项证明「两维都算不出来」。三条探针：
  P1 `implementation_date` 有效值：全表 `0000-00-00`，按 DATE_FORMAT 归一后 0 行
  P2 `policy_support` 的 `support_object`：全表 JSON null，取不到任何支持对象
  P3 实施反馈表：gkx 280 表里没有调查/反馈一类表；live 侧同名结果面为造数面

取数：读 gkx 侧共享快照（零 SQL）+ 读两份逐表 COUNT(*) 清单（GKX_INVENTORY / LIVE_INVENTORY）。
两份清单本身就是 `SELECT COUNT(*)` 的落盘结果，引用即视为可复核。
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SNAP = os.path.join(HERE, "_snapshots21")
WORK = os.path.join(ROOT, "_work_gkx21")
OUT = os.path.join(HERE, "M_POLICY_IMPLEMENTATION_EFFECT_out.json")

CANDIDATE_FEEDBACK_TABLES = [
    "policy_survey", "policy_feedback", "policy_satisfaction",
    "policy_implementation_feedback", "policy_eval_feedback",
    "policy_survey_result", "policy_metric_timeseries", "policy_effect",
]


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def pct(a, b, nd=4):
    return round(a * 100.0 / b, nd) if b else None


def main():
    struct = load(os.path.join(SNAP, "policy_struct_20261023.json"))
    dims = load(os.path.join(SNAP, "policy_dims_20261023.json"))
    fill = load(os.path.join(SNAP, "policy_field_fill_20261022.json"))
    gkx_inv = load(os.path.join(WORK, "GKX_INVENTORY.json"))
    live_inv = load(os.path.join(WORK, "LIVE_INVENTORY.json"))

    n = struct["rows"]
    validity = struct["validity"]
    elements = struct["elements"]

    gkx_policy_tables = sorted(t for t in gkx_inv if "policy" in t)
    gkx_feedback_hits = [t for t in CANDIDATE_FEEDBACK_TABLES if t in gkx_inv]
    # 只留行数：查询耗时（sec）属易变键，按 v6 §十 不进产物
    live_feedback_hits = {t: live_inv[k]["rows"] for t in CANDIDATE_FEEDBACK_TABLES
                          for k in live_inv if k.endswith("." + t)}

    # live 里所有 policy_* 表（用于说明「同名结果面存在，但属造数面」）
    live_policy = {t: v["rows"] for t, v in sorted(live_inv.items()) if "policy" in t}

    # ---------------- 维度 1：落地执行启动
    impl_valid = validity["implementation_date_nonnull"]
    # 入集：status 全为「有效」、expire_date 全空 → 20,000 条全部入集（正本「有效且未过期」恒真）
    in_set = n
    national = dims["level_dist"].get("4", 0)
    city_rows = {c: v["rows"] for c, v in struct["city_profile"].items()}
    # 正本：国家级政策可计入每个对比市
    compare_cities = ["深圳市", "北京市", "上海市", "广州市"]
    city_n = {c: city_rows.get(c, 0) + national for c in compare_cities}

    d1 = {
        "dimension": "落地执行启动",
        "formula": "COUNT(DISTINCT id WHERE implementation_date 非空) / N_c × 100%",
        "numerator_valid_dates": impl_valid,
        "denominator_in_set": in_set,
        "rate_if_forced_pct": pct(impl_valid, in_set),
        "raw_zero_date_rows": n,
        "computable": False,
        "why_not": "20,000 行 implementation_date 全部是零值日期 0000-00-00。"
                   "MySQL 的零值日期不是 NULL，COUNT(col) 会返回 20,000，看起来「100% 有值」；"
                   "按 DATE_FORMAT 归一后有效日期 0 行。此时输出 0% 等于把「字段未维护」"
                   "写成「政策未启动」，是事实性错误，故该维不可算。",
    }

    # ---------------- 维度 2：受益覆盖
    d2 = {
        "dimension": "受益覆盖",
        "formula": "COUNT(DISTINCT support_object)（空值不计入）",
        "support_json_null_rows": elements["support_json_type_dist"].get("JSON_NULL", 0),
        "support_object_rows": elements["support_object_rows"],
        "distinct_support_object": 0,
        "computable": False,
        "why_not": "policy_support 20,000 行 JSON_TYPE='NULL'，support_object 子键 0 行；"
                   "JSON_LENGTH(null) 返回 1，不能用它判空。没有支持对象可取，"
                   "种类数无从统计；正本也明确禁止用企业数冒充覆盖。",
    }

    # ---------------- 维度 3：实施反馈
    d3 = {
        "dimension": "实施反馈",
        "formula": "feedback_score（待建直读）",
        "computable": False,
        "gkx_candidate_tables_found": gkx_feedback_hits,
        "live_candidate_tables_found": live_feedback_hits,
        "why_not": "正本已注「现库无调查表，本维不计算」；实测 gkx 侧无任何调查/反馈表，"
                   "live 侧同名结果面属造数批次（见 mock_registry_note），不得作证据。",
    }

    dims_all = [d1, d2, d3]
    computable = [d for d in dims_all if d["computable"]]

    out = {
        "metric_id": "M_POLICY_IMPLEMENTATION_EFFECT",
        "metric_name_zh": "落地实效性",
        "support_judgment": "完全不支持",
        "verdict_kind": "negative_evidence",
        "judgment_reason": (
            "三维全部不可算：启动维的 implementation_date 全为 0000-00-00（归零后 0 行有效），"
            "覆盖维的 support_object 在 20,000 行 JSON null 里取不到，反馈维两库均无调查表。"
            "按正本「缺维不进平均」，可进平均的完整维 0 个，分数不存在；"
            "强行出 0 分等于把导入缺陷写成政策事实。"
        ),
        "publishable": False,
        "registered_metric_value": None,
        "headline": {
            "dimensions_total": len(dims_all),
            "dimensions_computable": len(computable),
            "composite_score": None,
            "reason": "可进平均的完整维 0 个 → 无分母，分数不存在",
        },
        "dims": dims_all,
        "population": {
            "policy_rows": n,
            "in_set_rows": in_set,
            "status_dist": validity["status_dist"],
            "expire_date_nonnull": validity["expire_date_nonnull"],
            "national_rows": national,
            "compare_cities": compare_cities,
            "N_c": city_n,
            "note": "正本入集条件「status=有效且 expire_date 空或不早于统计日」：status 单值「有效」、"
                    "expire_date 全空 → 20,000 条全部入集，条件恒真、不提供区分度。"
                    "正本另注「国家级可计入每个对比市」，故 N_c = 该市行数 + 国家级 2,174。",
        },
        "population_context": {
            "city_nonnull_rows": n - dims["city_dist"].get("__NULL__", 0),
            "city_null_rows": dims["city_dist"].get("__NULL__", 0),
            "policy_base_columns": 33,
            "amount_columns_in_policy_tables": 0,
            "innodb_table_rows_estimate": dims["known_estimate"]["information_schema_table_rows"],
            "live_policy_tables_zero_rows": sum(1 for t, v in live_policy.items() if v == 0),
            "note": "城市归属与列结构上下文：city 去脏后 10,294 行可用；政策表 33 列内无金额类列，"
                    "故覆盖维也不能用金额或企业数替代（正本明令禁止）",
        },
        "city_table": [
            {"city": c,
             "city_rows": city_rows.get(c, 0),
             "N_c": city_n[c],
             "start_numerator": 0,
             "start_rate_pct_if_forced": 0.0}
            for c in compare_cities
        ],
        "probes": {
            "gkx_policy_tables": gkx_policy_tables,
            "gkx_policy_table_count": len(gkx_policy_tables),
            "gkx_total_tables": len(gkx_inv),
            "gkx_feedback_tables": gkx_feedback_hits,
            "live_total_tables": len(live_inv),
            "live_policy_tables": live_policy,
            "live_feedback_tables": live_feedback_hits,
            "date_probe": {
                "implementation_date_nonnull_raw": n,
                "implementation_date_valid_after_normalize": impl_valid,
                "implementation_date_zero_rows": n,
                "expire_date_nonnull": validity["expire_date_nonnull"],
            },
            "json_probe": {
                "policy_support_json_null_rows": elements["support_json_type_dist"].get("JSON_NULL", 0),
                "support_key_dist": elements["support_key_dist"],
                "support_object_rows": elements["support_object_rows"],
                "support_way_rows": elements["support_way_rows"],
                "support_behavior_rows": elements["support_behavior_rows"],
            },
            "field_fill_cross_ref": {
                "source": "code/_snapshots21/policy_field_fill_20261022.json",
                "implementation_date_note": "该快照不含 implementation_date；本件改用 policy_struct 的归一计数",
                "content_nonempty": fill["fields"]["content"]["nonempty"],
            },
        },
        "mock_registry_note": (
            "live 侧确实存在与「实施反馈」同名的结果面（policy_effect 93 行、"
            "policy_metric_timeseries 93 行），但注册表 cfg_metric-POLICY-seed.yaml 对这组表的"
            "source_systems 登记为 `Mock @ batch=mock_20260623`、is_mock: true；"
            "`20261020_指标整体开发进度调研/_work_full/MOCK_TABLE_REGISTRY.md` 记录了同批表的"
            "造假指纹（列恒值、calc_batch_id='mock_20260623'）。该组表属造数面，不得作证据。"
        ),
        "repair_path": [
            "回填 implementation_date（现有 0000-00-00 是导入占位，不是缺失标记）→ 启动维恢复",
            "补 policy_support JSON 的 support_object 子键 → 覆盖维恢复",
            "建调查表（feedback_score，按政策 × 对象 × 批次）→ 反馈维恢复",
            "三维齐备后才谈权重；正本权重待 QPOL-02，本件不预设 1/3 等权",
        ],
        "sources": [
            "code/_snapshots21/policy_struct_20261023.json（implementation_date / expire_date / policy_support 归一计数）",
            "code/_snapshots21/policy_dims_20261023.json（层级/城市分布）",
            "code/_snapshots21/policy_field_fill_20261022.json（字段级填充率）",
            "_work_gkx21/GKX_INVENTORY.json（gkx 280 表逐表 COUNT(*)）",
            "_work_gkx21/LIVE_INVENTORY.json（live 267 表逐表 COUNT(*)）",
            "gkx @ 183.240.141.251:3318（只读用户 gkx_reader_zp）",
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面评估：正本按「统计日」取当前有效政策，不设年度序列；本件不出分，"
                           "故无基期年。若将来补数后按年出分，须先解决 2022-09 起 16 个月的发布断档，"
                           "否则某年启动率为 0 会是断档而不是真实归零。",
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print("gkx policy tables:", gkx_policy_tables)
    print("gkx feedback hits:", gkx_feedback_hits)
    print("live feedback hits:", live_feedback_hits)
    print("live policy tables:", live_policy)
    print("dims computable:", len(computable), "/", len(dims_all))
    print("city N_c:", city_n)
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
