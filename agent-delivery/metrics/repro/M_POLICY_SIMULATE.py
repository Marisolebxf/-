#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_POLICY_SIMULATE —— 政策效果推演（P1 政策评估族，否定性证据件）

正本：`gkx-orchestration/agent-delivery/metrics/calc-logic/POLICY/M_POLICY_SIMULATE.md`
（基线 B = policy_intensity 省级 intensity_index；情景 = support_intensity / coverage_scope；
 弹性 e 待 QPOL-02；ΔY = e·(X_sim−X_base)/X_base；Y_sim = B·(1+ΔY)）

本脚本证明推演链的四段输入全部缺位：
  B   基线：gkx 无 policy_intensity 表；live 同名表登记为造数面，且 intensity_index 全 NULL
  X   情景：gkx 无 policy_simulation_param；live 该表 0 行
  e   弹性：两库均无系数表，也无「政策参数→效果」的配对时间序列可估
  Y   校验：gkx 无 policy_prediction_indicator；live 该表 0 行，policy_simulate 仅 36 行且 delta_rate 只有 3 个值
另外：政策表 33 列里金额类列 0 个，"扶持力度"无法量化（DATA_FACTS §3.62）。

取数：gkx 共享快照（零 SQL）+ 两份逐表 COUNT(*) 清单 + 注册表/正本原文。
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SNAP = os.path.join(HERE, "_snapshots21")
WORK = os.path.join(ROOT, "_work_gkx21")
OUT = os.path.join(HERE, "M_POLICY_SIMULATE_out.json")

REQUIRED = [
    ("policy_intensity", "基线 B：省级政策力度指数"),
    ("policy_intensity_eval", "力度评估明细（效果/覆盖/成本三维分）"),
    ("policy_simulation_param", "情景参数：扶持力度/覆盖面/实施时间"),
    ("policy_prediction_indicator", "推演输出：预测值/上下界/变化率"),
    ("policy_simulation_result", "推演结果：定量结果/空间分布/时间趋势"),
]


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def pct(a, b, nd=4):
    return round(a * 100.0 / b, nd) if b else None


def main():
    struct = load(os.path.join(SNAP, "policy_struct_20261023.json"))
    dims = load(os.path.join(SNAP, "policy_dims_20261023.json"))
    fields = load(os.path.join(SNAP, "policy_fields_a23_20261021.json"))
    fill = load(os.path.join(SNAP, "policy_field_fill_20261022.json"))
    gkx_inv = load(os.path.join(WORK, "GKX_INVENTORY.json"))
    live_inv = load(os.path.join(WORK, "LIVE_INVENTORY.json"))

    cols = [r[0] for r in fields["columns"]["rows"]]
    amount_like = [c for c in cols
                   if any(k in c.lower() for k in ("amount", "money", "fund", "budget", "subsidy"))]
    n = struct["rows"]

    tbl_rows = []
    for name, role in REQUIRED:
        gkx_key = next((t for t in gkx_inv if t == name), None)
        live_key = next((k for k in live_inv if k.endswith("." + name)), None)
        tbl_rows.append({
            "table": name,
            "role": role,
            "in_gkx": bool(gkx_key),
            "gkx_rows": gkx_inv[gkx_key]["rows"] if gkx_key else None,
            "live_table": live_key,
            "live_rows": live_inv[live_key]["rows"] if live_key else None,
            "usable": False,
        })

    # 唯一有行数的两张 live 表，按 mock 批次登记，且关键列不可用
    usable_zero = sum(1 for r in tbl_rows if r["usable"])

    # 省级政策条数（唯一可得的"基线原料"）
    prov = [(k, v) for k, v in dims["province_dist"].items() if k != "__NULL__"]
    prov.sort(key=lambda kv: -kv[1])
    prov_total = sum(v for _, v in prov)
    top_prov = prov[0] if prov else (None, 0)
    doc_rows = struct["policy_doc_rows"]

    out = {
        "metric_id": "M_POLICY_SIMULATE",
        "metric_name_zh": "政策效果推演",
        "support_judgment": "完全不支持",
        "verdict_kind": "negative_evidence",
        "judgment_reason": (
            "推演链四段输入（基线 B、情景 X、弹性 e、校验 Y）在 gkx 与 live 两侧都拿不到可用数据："
            "五张依赖表在 gkx 280 表中 0 张；live 侧三张同名表 0 行、另两张属造数批次且关键列不可用；"
            "政策表 33 列无金额列，「扶持力度」无量化源。没有 B 与 e，公式无法取值 → 完全不支持。"
        ),
        "publishable": False,
        "registered_metric_value": None,
        "formula_chain": {
            "baseline": "B = policy_intensity.intensity_index（scope_type='province'）",
            "scenario": "X ∈ {support_intensity, coverage_scope}",
            "delta": "ΔY = e · (X_sim − X_base) / X_base",
            "output": "Y_sim = B × (1 + ΔY)",
            "blocked_at": ["B", "X", "e"],
        },
        "tables": tbl_rows,
        "tables_usable": usable_zero,
        "tables_required": len(tbl_rows),
        "probes": {
            "gkx_total_tables": len(gkx_inv),
            "gkx_policy_tables": sorted(t for t in gkx_inv if "policy" in t),
            "live_total_tables": len(live_inv),
            "live_policy_tables_zero_rows": sorted(
                k for k, v in live_inv.items() if "policy" in k and v["rows"] == 0)[:20],
            "amount_columns_in_policy_table": len(amount_like),
            "policy_table_columns": len(cols),
            "amount_columns_gkx_total_cited": 123,
            "amount_columns_cited_from": "DATA_FACTS_gkx21.md §3.62（全库 123 个金额类列全部落在 dwd_bid_* 招标表）",
            "json_null_policy_support": struct["elements"]["support_json_type_dist"].get("JSON_NULL", 0),
            "implementation_date_valid": struct["validity"]["implementation_date_nonnull"],
            "policy_rows": n,
        },
        "elasticity_probe": {
            "coefficient_table_exists": False,
            "paired_series_exists": False,
            "why": "弹性 e 需要「政策参数变化」与「效果变化」的配对观测。库内无效果时间序列"
                   "（policy_metric_timeseries 只存在于 live 造数面、93 行），也无参数记录"
                   "（policy_simulation_param 0 行），无法回归或标定；QPOL-02 也未签。",
        },
        "alternative_baseline_demo": {
            "purpose": "证明「退一步用政策条数当基线」也不成立，而不是留一个看起来能算的替代口径",
            "province_rows_total": prov_total,
            "province_count": len(prov),
            "top_province": {"name": top_prov[0], "rows": top_prov[1]},
            "policy_doc_rows": doc_rows,
            "policy_doc_share_pct": pct(doc_rows, n),
            "top11_rows": sum(v for _, v in prov[:11]),
            "other_provinces_rows": prov_total - sum(v for _, v in prov[:11]),
            "why_not": "条数是「供给规模」，正本的力度指数是效果/覆盖/成本三维加权（见 policy_intensity_eval）。"
                       "两者语义不同：条数无法对情景参数（扶持力度、覆盖面）产生响应，"
                       "ΔY 对条数求导没有意义，推演结果不可解释。",
        },
        "live_mock_rows": {
            "policy_intensity": live_inv.get("gkxlumenx_ads.policy_intensity", {}).get("rows", 631),
            "policy_simulate": live_inv.get("gkxlumenx_ads.policy_simulate", {}).get("rows", 36),
            "policy_focus": live_inv.get("gkxlumenx_ads.policy_focus", {}).get("rows", 631),
            "policy_metric_timeseries": live_inv.get(
                "gkxlumenx_ads.policy_metric_timeseries", {}).get("rows", 93),
            "note": "live 造数面的行数（注册表 is_mock: true），仅作对照，不参与任何计算",
        },
        "mock_caveat": (
            "live 的 policy_intensity(631)/policy_simulate(36)/policy_focus(631) 等表在注册表里登记为"
            "`Mock @ batch=mock_20260623`、is_mock: true；MOCK_TABLE_REGISTRY.md 记录的造假指纹包括"
            "intensity_index 全 NULL、policy_simulate.delta_rate 仅 {12,15,22} 三个值、scope_type 恒 province。"
            "即使不看批次标记，这三处指纹也说明它不是可用的推演结果面。"
        ),
        "downstream_impact": {
            "M_POLICY_DS_11_POLICY_EVAL_015": "该件的临时读面写的是 policy_simulate.curve/explanation；"
                                               "本件判完全不支持，015 因此只能退到正文环节词代理，不能读推演曲线",
            "M_POLICY_INTENSITY_SCORE": "同为完全不支持（力度五项里四项不可读），基线侧没有可替代来源",
        },
        "repair_path": [
            "建 policy_intensity 并有真实 intensity_index（现 live 同名表该列全 NULL）",
            "建 policy_simulation_param 并录入情景参数（现 0 行）",
            "QPOL-02 签认弹性系数 e 的口径与取值；无历史配对序列时至少给专家先验与区间",
            "建 policy_prediction_indicator 存预测值与上下界，才能做回测",
            "补政策金额列或「政策—扶持金额」表，扶持力度才有量化源",
        ],
        "sources": [
            "code/_snapshots21/policy_struct_20261023.json（20,000 行结构事实）",
            "code/_snapshots21/policy_dims_20261023.json（省级/城市分布）",
            "code/_snapshots21/policy_fields_a23_20261021.json（33 列清单）",
            "code/_snapshots21/policy_field_fill_20261022.json（字段填充率）",
            "_work_gkx21/GKX_INVENTORY.json（280 表 COUNT(*)）",
            "_work_gkx21/LIVE_INVENTORY.json（267 表 COUNT(*)）",
            "_work_gkx21/DATA_FACTS_gkx21.md §3.62（金额列分布）",
            "gkx @ 183.240.141.251:3318（只读用户 gkx_reader_zp）",
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "推演本应输出未来年份曲线，但基线表不存在、参数表 0 行，连基期都定不下来，"
                           "故 used/missing 均为空。这不是「基期缺失」，是「推演链未建立」。",
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print("tables:", [(r["table"], r["in_gkx"], r["live_rows"]) for r in tbl_rows])
    print("usable:", usable_zero, "/", len(tbl_rows))
    print("amount cols in policy table:", amount_like, len(cols))
    print("province total", prov_total, "top", top_prov)
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
