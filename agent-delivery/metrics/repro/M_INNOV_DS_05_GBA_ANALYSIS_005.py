#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_DS_05_GBA_ANALYSIS_005（机会因素分析）复现脚本。

口径：王惠「同 M_INNOV_GBA_SWOT_OPPORTUNITY」。三个机会探测维：
  O1 政策窗口：近窗(2022-2024)年均政策数 / 基线(2015-2021)年均政策数 ≥ 1.5
  O2 新兴技术：IPC4 近窗相对基线「突现」（父指标用 base=0 & rec≥3 的宽松判定）
  O3 区域外溢合作：跨城联合申请（需 applicants 明细）

本脚本对 O1 独立重算（年均化），对 O2 做方法学复检（抽样统计 base=0 占比、
按 Kleinberg 式严格阈值重判），对 O3 记录缺测。产物复用父指标 bundle。

输出：M_INNOV_DS_05_GBA_ANALYSIS_005_out.json
"""
from __future__ import annotations

from _innov_h_common import gkx_light_check, load_json, row_count, row_count_source, save_out

METRIC = "M_INNOV_DS_05_GBA_ANALYSIS_005"
REC_YEARS = 3      # 2022, 2023, 2024
BASE_YEARS = 7     # 2015-2021
THR_POLICY = 1.5
THR_BURST_STRICT_RATIO = 5.0
THR_BURST_STRICT_BASE = 3


def main():
    swot = load_json("M_INNOV_GBA_SWOT_BUNDLE_out.json")
    probe = load_json("_probe_innov_h_gkx_out.json", {}) or {}
    rows = swot["rows"]

    cities = []
    burst_sample_total = 0
    burst_sample_base0 = 0
    strict_hits = 0

    for r in rows:
        rec, base = r["opp_policy_rec"], r["opp_policy_base"]
        rec_ann = round(rec / REC_YEARS, 4)
        base_ann = round(base / BASE_YEARS, 4)
        # 王惠原式：近窗有效政策件数 / max(基线年均, 1)（分子未年均化）
        wanghui_ratio = round(rec / max(base_ann, 1), 4)
        ratio = round(rec_ann / base_ann, 4) if base_ann else None   # 年均/年均（量纲一致）
        window = wanghui_ratio >= THR_POLICY

        # O2 方法学复检：抽样突现项中 base=0 的占比 + 严格阈值命中数
        sample = r["opp_emerging_sample"]
        b0 = sum(1 for x in sample if x["base"] == 0)
        strict = sum(1 for x in sample
                     if x["base"] >= THR_BURST_STRICT_BASE
                     and x["rec"] / x["base"] >= THR_BURST_STRICT_RATIO)
        burst_sample_total += len(sample)
        burst_sample_base0 += b0
        strict_hits += strict

        hits = int(window) + int(r["opp_emerging_tech_cnt"] > 0) + int(bool(r["opp_spillover"]))
        cities.append({
            "city": r["city"],
            "O1_policy": {
                "rec_count": rec, "rec_annual": rec_ann,
                "base_count": base, "base_annual": base_ann,
                "wanghui_ratio": wanghui_ratio,
                "annualized_ratio": ratio,
                "threshold": THR_POLICY, "hit": window,
                "note": "王惠原式分子为近窗 3 年累计件数、分母为基线年均件数，量纲不一致；"
                        "annualized_ratio 为量纲对齐后的敏感性对照，两口径在 4 城均未达 1.5",
            },
            "O2_emerging": {
                "parent_burst_cnt": r["opp_emerging_tech_cnt"],
                "sample": sample,
                "sample_base0_cnt": b0,
                "sample_base0_pct": round(b0 / len(sample) * 100, 1) if sample else None,
                "strict_threshold": f"base≥{THR_BURST_STRICT_BASE} 且 rec/base≥{THR_BURST_STRICT_RATIO}",
                "strict_hits_in_sample": strict,
                "usable": False,
                "note": "父口径 base=0&rec≥3 会把「近窗新出现的小类」判为突现；严格阈值在抽样中命中 0",
            },
            "O3_spillover": {"value": r["opp_spillover"], "measurable": False,
                             "reason": "dwd_patent 无 applicants 列；dwd_patent_applicants 仅 25,753 行（覆盖 0.96%）"},
            "opportunity_hits": hits,
            "opportunity_score_0_100": round(hits / 3 * 100, 2),
            "usable_dimensions": 1,
        })

    live = gkx_light_check("SELECT COUNT(*) AS c FROM dwd_policy_base")

    out = {
        "metric_id": METRIC,
        "metric_name": "机会因素分析",
        "date": "2026-10-21",
        "calc_logic_ref": "metrics/calc-logic/INNOV/M_INNOV_GBA_SWOT_OPPORTUNITY.md（王惠口径）",
        "source_artifacts": [
            "code/M_INNOV_GBA_SWOT_BUNDLE_out.json（政策年度分布、IPC4 突现抽样、外溢占位）",
            "code/M_INNOV_GBA_INDEX_BUNDLE_out.json",
            "code/_probe_innov_h_gkx_out.json",
        ],
        "probes": {
            "gkx_live_count_policy": live,
            "policy_publish_year": swot["probes"]["policy_publish_year"][:12],
            "policy_status_all_valid": swot["probes"]["policy_status"],
            "gkx_applicants_rows": row_count(probe, "dwd_patent_applicants"),
            "gkx_patent_rows": row_count(probe, "dwd_patent"),
            "applicants_coverage_pct_of_patent": round(
                (row_count(probe, "dwd_patent_applicants") or 0)
                / max(row_count(probe, "dwd_patent") or 1, 1) * 100, 3),
            "row_count_source": {
                "dwd_patent_applicants": row_count_source(probe, "dwd_patent_applicants"),
                "dwd_patent": row_count_source(probe, "dwd_patent"),
            },
            "n_cities": len(rows),
            "gba_coverage_pct": round(len(rows) / 11 * 100, 2),
        },
        "windows": {"recent": "2022-2024", "baseline": "2015-2021",
                    "recent_years": REC_YEARS, "baseline_years": BASE_YEARS},
        "method_recheck": {
            "burst_sample_total": burst_sample_total,
            "burst_sample_base0": burst_sample_base0,
            "burst_sample_base0_pct": round(burst_sample_base0 / burst_sample_total * 100, 1) if burst_sample_total else None,
            "strict_hits_in_sample": strict_hits,
            "conclusion": "突现判定混入 base=0 的新增小类，且严格阈值在 20 个抽样项中 0 命中 → O2 计数不可直接消费",
        },
        "cities": cities,
        "summary": {
            "policy_window_hits": [c["city"] for c in cities if c["O1_policy"]["hit"]],
            "policy_ratio_by_city": {c["city"]: c["O1_policy"]["wanghui_ratio"] for c in cities},
            "policy_ratio_annualized_by_city": {c["city"]: c["O1_policy"]["annualized_ratio"] for c in cities},
            "policy_window_hits_annualized": [c["city"] for c in cities
                                              if c["O1_policy"]["annualized_ratio"] is not None
                                              and c["O1_policy"]["annualized_ratio"] >= THR_POLICY],
            "spillover_measurable": False,
            "usable_dimensions_per_city": 1,
            "total_possible_dimensions": 3,
            "dimension_coverage_pct": round(1 / 3 * 100, 2),
        },
        "support_judgment": "部分支持",
        "support_note": (
            "三维仅 O1 政策窗口可独立复核（4 城全部 <1.5，0 命中）；O2 计数可产出但方法缺陷导致"
            "「突现」失真；O3 外溢合作因 applicants 覆盖 0.96% 完全缺测 → 机会清单实质只剩 1/3 维 → 部分支持"
        ),
    }
    save_out(METRIC, out)


if __name__ == "__main__":
    main()
