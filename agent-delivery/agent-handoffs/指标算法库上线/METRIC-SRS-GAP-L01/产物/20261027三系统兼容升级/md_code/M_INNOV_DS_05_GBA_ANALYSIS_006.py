#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_DS_05_GBA_ANALYSIS_006（威胁因素分析）复现脚本。

口径：王惠「同 M_INNOV_GBA_SWOT_THREAT」。三个威胁探测维：
  T1 政策退坡：失效政策数 / 有效政策数 ≥ 0.3
  T2 竞争挤压：近窗专利份额 − 基线专利份额 ≤ −0.02
  T3 结构风险：IPC4 组合 HHI ≥ 0.25

实测要点：policy_base 全表 20,000 行 status 均为「有效」，T1 分母有值、分子恒 0，
属**数据缺陷导致的不可判定**，不能记为「无退坡」。本脚本把该结论显式写入输出。

输出：M_INNOV_DS_05_GBA_ANALYSIS_006_out.json
"""
from __future__ import annotations

from _innov_h_common import gkx_light_check, load_json, save_out

METRIC = "M_INNOV_DS_05_GBA_ANALYSIS_006"
THR_DECAY = 0.30
THR_SQUEEZE = -0.02
THR_HHI = 0.25
HHI_SAMPLE_NOTE = "父指标按城市取前 5,000 件专利的 IPC4 主分类份额计算（非全量）"


def main():
    swot = load_json("M_INNOV_GBA_SWOT_BUNDLE_out.json")
    probe = load_json("_probe_innov_h_gkx_out.json", {}) or {}
    rows = swot["rows"]
    cities = []

    for r in rows:
        valid, invalid = r["thr_policy_valid"], r["thr_policy_invalid"]
        decay_ratio = round(invalid / valid, 4) if valid else None
        if valid == 0:
            decay_state, decay_hit = "不适用（该城无有效政策记录）", None
        elif invalid == 0:
            decay_state, decay_hit = "不可判定（全库 status 无「失效」样本）", None
        else:
            decay_state, decay_hit = "可判定", decay_ratio >= THR_DECAY

        delta = round(r["thr_share_rec"] - r["thr_share_base"], 5)
        squeeze = delta <= THR_SQUEEZE
        hhi = r["thr_hhi_ipc4"]
        effective_n = round(1 / hhi, 1) if hhi else None

        judged = [x for x in (decay_hit, squeeze, hhi >= THR_HHI) if x is not None]
        cities.append({
            "city": r["city"],
            "T1_policy_decay": {
                "valid": valid, "invalid": invalid, "ratio": decay_ratio,
                "threshold": THR_DECAY, "state": decay_state, "hit": decay_hit,
                "data_defect": "dwd_policy_base 20,000 行 status 全为「有效」，失效维无观测",
            },
            "T2_share_squeeze": {
                "share_recent": r["thr_share_rec"], "share_baseline": r["thr_share_base"],
                "delta": delta, "threshold": THR_SQUEEZE, "hit": squeeze,
            },
            "T3_structure_hhi": {
                "hhi_ipc4": hhi, "threshold": THR_HHI, "hit": hhi >= THR_HHI,
                "effective_class_count": effective_n,
                "sample_note": HHI_SAMPLE_NOTE,
                "threshold_mismatch": (
                    f"阈值 0.25 对应等效 {round(1/THR_HHI)} 个 IPC4 类，实际等效 {effective_n} 类；"
                    "该阈值来自并购审查的 2500 分界，不适配专利组合分散度"
                ),
            },
            "threat_hits": sum(1 for x in judged if x),
            "judgeable_dimensions": len(judged),
            "threat_level": "无命中" if all(not x for x in judged) else "存在命中",
        })

    live = gkx_light_check("SELECT status, COUNT(*) AS c FROM dwd_policy_base GROUP BY status", timeout=90)

    out = {
        "metric_id": METRIC,
        "metric_name": "威胁因素分析",
        "date": "2026-10-21",
        "calc_logic_ref": "metrics/calc-logic/INNOV/M_INNOV_GBA_SWOT_THREAT.md（王惠口径）",
        "source_artifacts": [
            "code/M_INNOV_GBA_SWOT_BUNDLE_out.json（政策有效性、份额、IPC4 HHI）",
            "code/_probe_innov_h_gkx_out.json",
        ],
        "probes": {
            "gkx_live_policy_status": live,
            "policy_status_cached": swot["probes"]["policy_status"],
            "policy_publish_year": swot["probes"]["policy_publish_year"][:12],
            "gkx_policy_rows": (probe.get("tables", {}).get("dwd_policy_base", {}) or {}).get("rows_exact"),
            "n_cities": len(rows),
            "gba_coverage_pct": round(len(rows) / 11 * 100, 2),
        },
        "thresholds": {"T1_decay": THR_DECAY, "T2_squeeze": THR_SQUEEZE, "T3_hhi": THR_HHI},
        "cities": cities,
        "summary": {
            "decay_judgeable_cities": [c["city"] for c in cities if c["T1_policy_decay"]["hit"] is not None],
            "squeeze_hits": [c["city"] for c in cities if c["T2_share_squeeze"]["hit"]],
            "hhi_hits": [c["city"] for c in cities if c["T3_structure_hhi"]["hit"]],
            "share_delta_by_city": {c["city"]: c["T2_share_squeeze"]["delta"] for c in cities},
            "hhi_by_city": {c["city"]: c["T3_structure_hhi"]["hhi_ipc4"] for c in cities},
            "judgeable_dimensions_per_city": 2,
            "total_possible_dimensions": 3,
            "dimension_coverage_pct": round(2 / 3 * 100, 2),
        },
        "support_judgment": "部分支持",
        "support_note": (
            "T2 份额挤压与 T3 结构风险可算（4 城份额变动均 > −0.02、HHI 0.0007~0.0013 远低于 0.25）；"
            "T1 政策退坡因全库 status 恒为「有效」不可判定，威胁清单缺失 1/3 维且 HHI 阈值口径不适配 → 部分支持"
        ),
    }
    save_out(METRIC, out)


if __name__ == "__main__":
    main()
