#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TECH_MATURITY_LEVEL —— 技术成熟度等级（L1—L5，深圳口径）。

口径（单一，深圳）：
  - 域 = IPC 主分类前 4 位；样本门槛 n2024 >= 100 件；
  - 件数、申请人、发明件数全部只取「深圳市申请人」；
  - 授权数按「申请人域内专利份额 × 该申请人全期授权数」分摊到域，
    不是专利级逐件授权标记（库内无 pn 级授权位，详见 §三 D2）；
  - 全国件数不参与任何分母，本件不出现全国列。

五维得分（0—100，绝对锚点，非分位），特征层见 `_tech21_domainfeat.py`：
  S1 规模 25%   n2024 的对数刻度，100 件=0，10,000 件=100
  S2 授权 25%   分摊全期授权比，0.50=0，0.90=100
  S3 发明 15%   分摊发明占比，0.15=0，0.70=100
  S4 集中 15%   申请人 HHI 的对数刻度，50=0，1,000=100
  S5 稳定 20%   近端增长 |g| 越小越高，|g|>=0.50 记 0

零 SQL：只读 _snapshots21 / _snapshots_gkx21 授权缓存。
"""
from __future__ import annotations

import collections
import statistics

import _tech21_scope as sc
import _tech21_domainfeat as feat

METRIC = "M_TECH_MATURITY_LEVEL"
YEARS = feat.YEARS


def main():
    rows, meta = feat.build()
    rows = sorted(rows, key=lambda r: -r["maturity_score"])
    dist = collections.Counter(r["maturity_level"] for r in rows)
    by_level = {}
    for lv in ("L1", "L2", "L3", "L4", "L5"):
        sub = [r for r in rows if r["maturity_level"] == lv]
        by_level[lv] = {
            "domains": len(sub),
            "share": round(len(sub) / len(rows), 4),
            "n2024": sum(r["n2024"] for r in sub),
            "n2024_share": round(sum(r["n2024"] for r in sub) / meta["qualified_total_2024"], 4),
            "score_range": [min((r["maturity_score"] for r in sub), default=None),
                            max((r["maturity_score"] for r in sub), default=None)],
            "examples": [r["ipc4"] for r in sub[:6]],
        }

    scores = [r["maturity_score"] for r in rows]
    tight = [r for r in rows if r["maturity_level"] in ("L4", "L5")]
    loose = [r for r in rows if r["maturity_level"] in ("L1", "L2")]

    payload = {
        "metric_id": METRIC,
        "generated_at": "2026-10-22",
        "scope": "深圳",
        "scope_statement": (
            "本件唯一分母是深圳：域件数、申请人数、发明件数、授权分摊全部只落在"
            "深圳市申请人上。全国件数不参与任何分母，正文不出现「全国成熟度」列；"
            "因此本件的等级是「深圳样本内等级」，不是全国技术就绪度。"
        ),
        "main_db": "gkx @ 183.240.141.251:3318 (gkx_reader_zp, read-only)",
        "sql_count": 0,
        "base_years_used": YEARS,
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": (
            "专利年序列只遍历库内真实存在的 2021—2024 四年（2025/2026 为采集残年，"
            "不进入稳定性分母）；2017—2020 在 dwd_patent 零行，未按 0 补入任何均值或斜率。"
            "授权与发明件数是全期累计值（非逐年年份队列），因此 S2/S3 是「跨期平均」，"
            "不是 2024 单年队列授权率。"
        ),
        "input": {
            "sz_patent": "code/_snapshots21/patent_scan_20261021.pkl",
            "ipc_by_name": "code/_snapshots21/patent_ipc4_by_name_20261021.json",
            "applicant_agg": "code/_snapshots21/star_applicant_agg_gkx.json",
            "sz_applicants": "code/_snapshots_gkx21/sz_patent_city_name_gkx.json",
        },
        "reused_from": "_tech21_domainfeat.py（域特征层，零 SQL）",
        "alloc_meta": {
            "agg_table_rows": meta["agg_table_rows"],
            "agg_names": meta["agg_names"],
            "sz_applicants": meta["sz_applicants"],
            "ipc_by_name_rows": meta["ipc_by_name_rows"],
            "method": "域授权=Σ_申请人(域内件数/该申请人全期件数×该申请人全期授权数)",
            "assumption": "同一申请人在各 IPC4 域的授权率相同；该假设无法用现有缓存逐件校验",
            "zero_grant_applicants": "agg 中授权数为 0 的申请人按 0 计入，不剔除",
        },
        "weights": feat.WEIGHTS,
        "level_cuts": feat.LEVEL_CUTS,
        "panel": {
            "sz_domains_all": meta["sz_domains_all"],
            "qualified_domains": meta["qualified"],
            "qualified_n2024_sum": meta["qualified_total_2024"],
            "sz_all_n2024": meta["sz_total_2024"],
            "qualified_coverage_2024": round(meta["qualified_total_2024"] / meta["sz_total_2024"], 4),
            "sz_year_total": meta["sz_year_total"],
        },
        "level_distribution": by_level,
        "score_stats": {
            "min": round(min(scores), 2), "max": round(max(scores), 2),
            "mean": round(statistics.mean(scores), 2),
            "median": round(statistics.median(scores), 2),
            "quartiles": [round(x, 2) for x in statistics.quantiles(scores, n=4)],
        },
        "top20": [{"ipc4": r["ipc4"], "label": r["label"], "n2024": r["n2024"],
                   "score": r["maturity_score"], "level": r["maturity_level"],
                   "grant_ratio": r["grant_ratio"], "invention_share": r["invention_share"],
                   "hhi": r["hhi"], "parts": r["maturity_parts"]} for r in rows[:20]],
        "bottom20": [{"ipc4": r["ipc4"], "label": r["label"], "n2024": r["n2024"],
                      "score": r["maturity_score"], "level": r["maturity_level"],
                      "grant_ratio": r["grant_ratio"], "invention_share": r["invention_share"],
                      "hhi": r["hhi"], "parts": r["maturity_parts"]} for r in rows[-20:]],
        "high_maturity_examples": [{"ipc4": r["ipc4"], "label": r["label"],
                                    "score": r["maturity_score"], "level": r["maturity_level"],
                                    "n2024": r["n2024"], "grant_ratio": r["grant_ratio"],
                                    "hhi": r["hhi"]} for r in tight[:8]],
        "low_maturity_examples": [{"ipc4": r["ipc4"], "label": r["label"],
                                   "score": r["maturity_score"], "level": r["maturity_level"],
                                   "n2024": r["n2024"], "grant_ratio": r["grant_ratio"],
                                   "hhi": r["hhi"]} for r in loose[-8:]],
        "domains": rows,
        "support_judgment": {
            "data_support_level": "部分支持",
            "structure_support": "部分",
            "data_support": "部分",
            "reason": (
                "五维里规模、授权比、发明占比、集中度、稳定性都有结构，但成熟度的核心证据"
                "（技术就绪度 TRL、被引、标准/中试、市场渗透）在本库不存在：被引表仅 20,515 行"
                "（覆盖 0.70%），无 TRL、无技术标准表；授权数只能按申请人份额分摊、无 pn 级"
                "授权位。故只能交付「专利形态五级」，不是 TRL 1—9。"
            ),
        },
    }
    sc.write_out(METRIC, payload)


if __name__ == "__main__":
    main()
