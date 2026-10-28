#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_DS_06_CARRIER_003（创新价值排名）复现脚本。

口径：王惠 V1.5-20260830「深圳创新载体创新价值排名」——
  技术价值 = 专利 value 合计 + 期刊 impact_score 合计
  应用价值 = 专利转移件数 + 论文下载量
  潜在影响力 = 专利被引合计 + 论文被引合计
  三维在深圳批内极值归一、等权平均 ×100、降序排名（统计年 2024）。

本脚本复用父指标同日实测产物 M_INNOV_CARRIER_VALUE_RANK_SZ_out.json（不重跑重查询），
对评分口径做可复算的解剖：覆盖度、缺测维 0.5 填充导致的分数地板、维度单维上限、
Top10 分数分解反解，并给出去掉缺测维的敏感性对照。

输出：M_INNOV_DS_06_CARRIER_003_out.json
"""
from __future__ import annotations

from _innov_h_common import gkx_light_check, load_json, pct, row_count, row_count_source, save_out

METRIC = "M_INNOV_DS_06_CARRIER_003"


def main():
    parent = load_json("M_INNOV_CARRIER_VALUE_RANK_SZ_out.json")
    probe = load_json("_probe_innov_h_gkx_out.json", {}) or {}
    c = parent["compute"]
    cov = c["dim_coverage"]
    st = c["stats"]
    n = c["n_sz_carriers"]

    # 缺测维 0.5 填充的分数地板：pot 全 0 → norm 分支 hi==lo → 0.5
    floor_score = round(0.5 / 3 * 100, 2)
    dims_effective = {
        "tech": {"covered": cov["tech_patent_value"], "pct": pct(cov["tech_patent_value"], n)},
        "app": {"covered": cov["app_transfer_or_dl"], "pct": pct(cov["app_transfer_or_dl"], n)},
        "pot": {"covered": cov["pot_cited"], "pct": pct(cov["pot_cited"], n)},
    }
    dims_per_carrier = (cov["tech_patent_value"] + cov["app_transfer_or_dl"] + cov["pot_cited"]) / n
    dimension_coverage_pct = round(dims_per_carrier / 3 * 100, 2)

    # Top10 分数反解：score = mean(avail)*100；pot 恒 0 → norm 0.5；app 仅 1 家有值（max=2）
    top = []
    for t in c["top10"]:
        has_tech = t["tech"] is not None
        a_norm = 1.0 if t["app"] and t["app"] > 0 else 0.0
        implied = round(3 * t["score"] / 100 - a_norm - 0.5, 4)
        counter = None
        if has_tech and a_norm == 0:
            counter = 100.0          # 仅技术维 → 单维归一即 100
        top.append({
            "rank": t["rank"], "name": t["name"],
            "tech_raw": t["tech"], "app_raw": t["app"], "pot_raw": t["pot"],
            "score": t["score"],
            "tech_norm_implied": implied if has_tech else None,
            "dimensions_available": (1 if has_tech else 0) + (1 if a_norm else 0) + 1,
            "counterfactual_score_excl_missing_pot": counter,
        })

    # 榜单有效性
    n_valid = st["n"]
    n_unranked = n - n_valid
    dropped_pct = pct(n_unranked, n)

    live = gkx_light_check(
        "SELECT (SELECT COUNT(*) FROM dwd_zh_journal) AS zh_journal,"
        " (SELECT COUNT(*) FROM dwd_en_journal) AS en_journal,"
        " (SELECT COUNT(*) FROM dwd_patent_cited) AS patent_cited")

    out = {
        "metric_id": METRIC,
        "metric_name": "创新价值排名",
        "date": "2026-10-21",
        "calc_logic_ref": "metrics/calc-logic/INNOV/M_INNOV_CARRIER_VALUE_RANK_SZ.md（王惠 V1.5-20260830）",
        "stat_year": parent["stat_year"],
        "source_artifacts": [
            "code/M_INNOV_CARRIER_VALUE_RANK_SZ_out.json（父指标实测：2000 载体、538 入榜、Top10）",
            "code/_probe_innov_h_gkx_out.json（专利/论文/期刊/被引表规模）",
        ],
        "probes": {
            "gkx_live_counts": live,
            "parent_demo_counts": parent["probes"],
            "gkx_patent_rows": row_count(probe, "dwd_patent"),
            "gkx_patent_cited_rows": row_count(probe, "dwd_patent_cited"),
            "gkx_patent_transfer_rows": row_count(probe, "dwd_patent_transfer"),
            "gkx_zh_paper_rows": row_count(probe, "dwd_zh_paper"),
            "gkx_zh_paper_citation_rows": row_count(probe, "dwd_zh_paper_citation"),
            "row_count_source": {
                t: row_count_source(probe, t) for t in
                ["dwd_patent", "dwd_patent_cited", "dwd_patent_transfer", "dwd_zh_paper", "dwd_zh_paper_citation"]
            },
            "patent_cited_coverage_pct_of_patent": round(
                (row_count(probe, "dwd_patent_cited") or 0)
                / max(row_count(probe, "dwd_patent") or 1, 1) * 100, 3),
        },
        "compute": {
            "n_sz_carriers": n,
            "n_ranked": n_valid,
            "n_unranked_no_value": n_unranked,
            "unranked_pct": dropped_pct,
            "dim_coverage": dims_effective,
            "avg_available_dimensions_per_carrier": round(dims_per_carrier, 3),
            "dimension_coverage_pct": dimension_coverage_pct,
            "score_floor_from_missing_dim_fill": floor_score,
            "stats": st,
            "top10": top,
            "score_formula": "score = mean(可用维归一值) × 100；缺测维按 0.5 参与平均（hi==lo 分支）",
        },
        "findings": {
            "floor_matches_stats_min": abs(st["min"] - floor_score) < 0.01,
            "pot_dim_all_zero": cov["pot_cited"] == 0,
            "tech_only_max_score": round((1.0 + 0.5) / 3 * 100, 2),
            "two_dim_max_score": 75.0,
            "rank1_has_no_tech_value": c["top10"][0]["tech"] is None,
            "rank1_score_breakdown": "技术维缺测(不计入) + 应用维 2 次下载(归一 1.0) + 潜在维全 0 被填 0.5 → 均值 0.75 → 75 分",
            "rank2_raw_tech": c["top10"][1]["tech"],
            "rank2_score": c["top10"][1]["score"],
            "comparability_break": "有技术维者上限 50 分（技术1.0+应用0+潜在0.5），无技术维而有下载者可达 75 分 → 缺维越多反而越占优",
        },
        "support_judgment": "部分支持",
        "support_note": (
            f"深圳载体 {n} 家，仅 {n_valid} 家（{pct(n_valid, n)}%）进入排名；技术维覆盖 {cov['tech_patent_value']} 家、"
            f"应用维 {cov['app_transfer_or_dl']} 家、潜在维 {cov['pot_cited']} 家；三维等权退化为技术维单维排序，"
            "且缺测维 0.5 填充导致「无数据者得中位分」的排序失真 → 部分支持"
        ),
    }
    save_out(METRIC, out)


if __name__ == "__main__":
    main()
