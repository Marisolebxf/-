#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_PHASE_DETERMINATION · 产业链阶段判定（20261021 换源版）

旧稿公式（照抄）
----------------
输入 M_CHAIN_STAGE_SCORE 的 0—100 阶段分，按**等频三分**给 12 条链贴阶段：
  score 前 1/3 → 成长期；中间 1/3 → 成熟期；后 1/3 → 衰退期。
旧稿另设阈值法（<40 衰退 / 40—60 成熟 / ≥60 成长）作敏感性。

换源后的硬事实
--------------
1. 不重算阶段分，直接读同目录上游产物 `M_CHAIN_STAGE_SCORE_out.json`
   （该件已换源到 gkx.dwd_org_industry_tags ⋈ dwd_org_annual_financial_info）。
2. 上游 12 条链里只有 8 条四个维度全测到；低空经济、生物医药 4 维全空、
   分数恒为 50，等频三分会把它们机械地放进「成熟期」。本件对
   `n_dims_measured <= 2` 的链同时给出 `phase_mechanical`（机械分段）与
   `phase_final = 不可判定（数据不足）`，不把空值包装成结论。
3. 上游分数随统计年剧烈翻转（人工智能 79.50→12.26、集成电路 71.38→32.85），
   本件以 2025 为主口径、2024 为敏感性，逐年比对阶段翻转数，不掩盖不稳定性。

输出：`code/M_CHAIN_PHASE_DETERMINATION_out.json`
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
UP = HERE / "M_CHAIN_STAGE_SCORE_out.json"
OUT = HERE / "M_CHAIN_PHASE_DETERMINATION_out.json"
METRIC = "M_CHAIN_PHASE_DETERMINATION"
NAME = "产业链阶段判定"
PHASES = ["成长期", "成熟期", "衰退期"]
MIN_DIMS = 3  # >=3 维实测才认为阶段可判定


def tercile(chains):
    """等频三分：按 score 降序，前三/中四/后五？——12 条严格四四四。"""
    ordered = sorted(chains, key=lambda c: (-c["score"], c["industry_code"]))
    n = len(ordered)
    out = {}
    for i, c in enumerate(ordered):
        idx = min(2, int(i * 3 / n))
        out[c["industry_code"]] = PHASES[idx]
    return out, ordered


def threshold_phase(score):
    if score >= 60:
        return "成长期"
    if score >= 40:
        return "成熟期"
    return "衰退期"


def main() -> None:
    up = json.loads(UP.read_text(encoding="utf-8"))
    cur = up["compute_t2025"]["chains"]
    prev = {c["industry_code"]: c for c in up["compute_t2024"]["chains"]}

    mech, ordered = tercile(cur)
    thr = {c["industry_code"]: threshold_phase(c["score"]) for c in cur}
    for c in cur:
        c["phase_mechanical"] = mech[c["industry_code"]]
        c["phase_threshold"] = thr[c["industry_code"]]
        c["reliable"] = c["n_dims_measured"] >= MIN_DIMS
        c["phase_final"] = c["phase_mechanical"] if c["reliable"] else "不可判定（数据不足）"
        c["score_2024"] = prev.get(c["industry_code"], {}).get("score")
        c["phase_2024_mech"] = None
    mech24, _ = tercile([
        {"industry_code": k, "score": v["score"]} for k, v in prev.items()
    ])
    for c in cur:
        c["phase_2024_mech"] = mech24.get(c["industry_code"])
        c["phase_flip_yoy"] = c["phase_2024_mech"] != c["phase_mechanical"]
        c["score_delta_yoy"] = (
            round(c["score"] - c["score_2024"], 2) if c["score_2024"] is not None else None
        )

    final_counts = {p: sum(1 for c in cur if c["phase_final"] == p) for p in PHASES}
    final_counts["不可判定（数据不足）"] = sum(1 for c in cur if not c["reliable"])
    mech_counts = {p: sum(1 for c in cur if c["phase_mechanical"] == p) for p in PHASES}
    thr_counts = {p: sum(1 for c in cur if c["phase_threshold"] == p) for p in PHASES}

    # 逐链可读输出（按 final 阶段、再按分数降序）
    order_final = {p: i for i, p in enumerate(PHASES + ["不可判定（数据不足）"])}
    chains = sorted(cur, key=lambda c: (order_final[c["phase_final"]], -c["score"]))
    out_chains = []
    for c in chains:
        out_chains.append({
            "industry_code": c["industry_code"],
            "industry_name": c["industry_name"],
            "score_2025": c["score"],
            "score_2024": c["score_2024"],
            "score_delta_yoy": c["score_delta_yoy"],
            "n_dims_measured": c["n_dims_measured"],
            "n_dims_default_0_5": c["n_dims_default_0_5"],
            "phase_mechanical": c["phase_mechanical"],
            "phase_threshold": c["phase_threshold"],
            "phase_2024_mech": c["phase_2024_mech"],
            "phase_flip_yoy": c["phase_flip_yoy"],
            "reliable": c["reliable"],
            "phase_final": c["phase_final"],
        })

    flips = [c for c in out_chains if c["phase_flip_yoy"]]
    report = {
        "metric_id": METRIC,
        "metric_name": NAME,
        "date": "2026-10-22",
        "data_source": (
            "同目录上游 M_CHAIN_STAGE_SCORE_out.json（其源为 gkx @ 183.240.141.251:3318："
            "dwd_org_industry_tags ⋈ dwd_org_annual_financial_info）"
        ),
        "formula": "phase = 按 score 降序等频三分（前 1/3 成长、中 1/3 成熟、后 1/3 衰退）；n_dims_measured<3 → 不可判定",
        "input_contract": {
            "upstream_metric": up["metric_id"],
            "upstream_date": up.get("date"),
            "upstream_score_year": 2025,
            "chains": len(cur),
            "score_min": min(c["score"] for c in cur),
            "score_max": max(c["score"] for c in cur),
            "score_mean": round(sum(c["score"] for c in cur) / len(cur), 2),
            "chains_all4_measured": sum(1 for c in cur if c["n_dims_measured"] == 4),
            "chains_all_default": sum(1 for c in cur if c["n_dims_measured"] == 0),
            "min_dims_for_reliable": MIN_DIMS,
            "upstream_probes": {
                "annual_rows": up["probes"]["dwd_org_annual_financial_info_rows"],
                "total_rev_pos_all_years": up["probes"]["total_rev_pos_all_years"],
                "development_employee_pos": up["probes"]["development_employee_pos"],
                "arch_development_am_pos": up["probes"]["arch_development_am_pos"],
            },
        },
        "phase_counts_mechanical": mech_counts,
        "phase_counts_threshold": thr_counts,
        "phase_counts_final": final_counts,
        "reliable_chains": sum(1 for c in out_chains if c["reliable"]),
        "unreliable_chains": sum(1 for c in out_chains if not c["reliable"]),
        "yoy": {
            "chains_score_changed": sum(1 for c in out_chains if c["score_2025"] != c["score_2024"]),
            "chains_phase_flipped": len(flips),
            "flip_detail": [[c["industry_code"], c["industry_name"], c["phase_2024_mech"],
                             c["phase_mechanical"], c["score_2024"], c["score_2025"]] for c in flips],
            "note": "上游敏感性原文：分数随统计年大幅变动的主因是可比企业集合换人，不是产业真实变化。",
        },
        "method_difference": {
            "mech_vs_threshold_disagree": sum(
                1 for c in out_chains if c["phase_mechanical"] != c["phase_threshold"]),
            "detail": [[c["industry_code"], c["industry_name"], c["score_2025"],
                        c["phase_mechanical"], c["phase_threshold"]] for c in out_chains],
            "note": "等频法强制每段 4 条，阈值法允许空段；两法只在有明确阈值依据时才可互换。",
        },
        "chains": out_chains,
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": (
                f"12 条链都有阶段分，等频三分可直接执行；但只有 "
                f"{sum(1 for c in cur if c['reliable'])}/12 条链实测维度 ≥3，"
                "低空经济/生物医药 4 维全空、分数恒 50，机械分段会把空值送进成熟期；"
                f"跨年阶段翻转 {len(flips)}/12，其中人工智能 79.50→12.26、"
                "集成电路 71.38→32.85，阶段结论对统计年高度敏感；"
                "两套分段法（等频 vs 阈值）结果不一致。故判部分支持，"
                "并把不可判定链单独列出，不硬贴阶段。"
            ),
            "criteria": {
                "chains_total": len(cur),
                "chains_reliable": sum(1 for c in cur if c["reliable"]),
                "chains_all_dims_default": sum(1 for c in cur if c["n_dims_measured"] == 0),
                "phase_flips_yoy": len(flips),
                "methods_agree": sum(1 for c in out_chains if c["phase_mechanical"] == c["phase_threshold"]),
            },
        },
        "base_years_used": [2024, 2025],
        "base_years_missing": [],
        "base_years_note": (
            "主口径 2025、敏感性 2024。上游财务表虽覆盖 2013—2025，但 2025 年营收>0 仅 34 行、"
            "全表累计仅 2,191 行，更早年份样本更薄且企业集合逐年换人，故不把 2013—2023 当可比基期；"
            "这不是缺年补 0，而是明确不采用。"
        ),
        "sources": [
            {"path": "code/M_CHAIN_STAGE_SCORE_out.json", "role": "上游阶段分（2024/2025）"},
            {"path": "code/M_CHAIN_STAGE_SCORE.py", "role": "上游换源脚本"},
            {"table": "gkx.dwd_org_industry_tags", "role": "企业—链标签"},
            {"table": "gkx.dwd_org_annual_financial_info", "role": "年度营收/利润/员工（development_employee 全空）"},
        ],
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print("mech", mech_counts, "final", final_counts, "flips", len(flips))
    for c in out_chains:
        print(c["industry_code"], c["industry_name"], c["score_2025"], c["phase_final"],
              c["phase_mechanical"], "dims", c["n_dims_measured"])
    print("wrote", OUT)


if __name__ == "__main__":
    main()
