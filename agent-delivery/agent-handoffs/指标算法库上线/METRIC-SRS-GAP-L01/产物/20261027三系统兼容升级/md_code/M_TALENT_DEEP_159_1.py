#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_TALENT_DEEP_159_1 —— 深圳重点人才优势和短板分析模型（TALENT 深度分析第 159 号）

需求语义：用深圳人才数据与全国（对标城市）对比，从多维度识别深圳重点人才的优势领域与短板，
输出优势清单、短板报告与改进建议。需求列的评价维度是「技能匹配度、招聘难度、薪资水平、发展前景」，
但没有给对比口径、归一方法与优劣势判定规则。

本文口径（零 SQL）：
  1. 区域：`dwd_scholar.scholar_org_name_zh` 经五级地名归属（高校名录 → 企业底册 → 前缀 →
     城市关键词 → 海外），取深圳市 / 北京市 / 上海市 / 其他 / 海外。
  2. 五维画像：规模（人数）、影响力（h 中位/均值）、产出（论文中位）、顶才（h≥50 占比、
     Top1% 门槛）、帽子（可挂主档的院士数）。
  3. 领域维：学者中文论文（姓名+机构双锚定）→ 20+8 集群，按**区位商 LQ** 判优势/短板：
     LQ = (深圳该簇学者/深圳学者) ÷ (全国该簇学者/全国学者)。
     LQ≥1.2 且深圳人数≥5 记优势；LQ≤0.8 且全国人数≥30 记短板。
  4. 市场供需四维（技能匹配/招聘难度/薪资/前景）库内无源（`dwd_job` 10 行、无薪资列），
     显式不交付，不用代理硬凑。

产物：code/M_TALENT_DEEP_159_1_out.json。
"""
from __future__ import annotations

import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _talent21_common import (  # noqa: E402
    academicians, anchored_papers, clusters_of, loc, paper_clusters, pctl, scholars, st, write_out,
)

METRIC = "M_TALENT_DEEP_159_1"
REGIONS = ("深圳市", "北京市", "上海市")


def region_of(org: str) -> str:
    c = loc(org)[1]
    if c in REGIONS:
        return c
    if c == "海外":
        return "海外"
    return "其他"


def main() -> None:
    sch = [s for s in scholars() if s["name"]]
    buckets: dict[str, list[dict]] = defaultdict(list)
    for s in sch:
        buckets[region_of(s["org"])].append(s)

    profile = {}
    for reg in ("深圳市", "北京市", "上海市", "其他"):
        arr = buckets.get(reg, [])
        if not arr:
            profile[reg] = None
            continue
        hs = [s["h"] for s in arr]
        ps = [s["paper"] for s in arr]
        cs = [s["cite"] for s in arr]
        top1n = max(1, int(len(arr) * 0.01))
        profile[reg] = {
            "n": len(arr),
            "h_median": statistics.median(hs),
            "h_mean": round(statistics.mean(hs), 2),
            "h_p90": pctl(hs, 0.90),
            "paper_median": statistics.median(ps),
            "paper_mean": round(statistics.mean(ps), 2),
            "cite_median": statistics.median(cs),
            "h_ge50": sum(1 for x in hs if x >= 50),
            "h_ge50_rate_pct": round(100 * sum(1 for x in hs if x >= 50) / len(arr), 2),
            "top1_h_min": sorted(hs, reverse=True)[top1n - 1],
        }

    acad = academicians()
    acad_by_reg = Counter(region_of(s["org"]) for s in sch if s["sid"] in acad)
    for reg in profile:
        if profile[reg]:
            profile[reg]["academicians_matched"] = acad_by_reg.get(reg, 0)

    # ---- 领域维：姓名+机构双锚定论文判簇 → 区位商 ----
    cov = 0
    per_reg_cluster: dict[str, Counter] = defaultdict(Counter)
    per_cluster_total = Counter()
    per_reg_n = Counter()
    sz_h_by_cluster: dict[str, list[int]] = defaultdict(list)
    for s in sch:
        papers = anchored_papers(s)
        if not papers:
            continue
        cov += 1
        reg = region_of(s["org"])
        per_reg_n[reg] += 1
        tags: list[str] = []
        for p in papers:
            tags.extend(paper_clusters(p["pid"], p["kw"], p["ti"]))
        cl = sorted(set(clusters_of(tags))) if tags else []
        for c in cl:
            per_reg_cluster[reg][c] += 1
            per_cluster_total[c] += 1
            if reg == "深圳市":
                sz_h_by_cluster[c].append(s["h"])

    n_all = cov
    n_sz = per_reg_n["深圳市"]
    lq_rows = []
    for c, tot in per_cluster_total.items():
        nsz = per_reg_cluster["深圳市"].get(c, 0)
        if not n_sz or not n_all:
            continue
        share_sz = nsz / n_sz
        share_all = tot / n_all
        lq = share_sz / share_all if share_all else None
        lq_rows.append({"cluster": c, "n_sz": nsz, "n_all": tot,
                        "share_sz_pct": round(100 * share_sz, 2),
                        "share_all_pct": round(100 * share_all, 2),
                        "lq": round(lq, 3) if lq else None,
                        "h_median_sz": statistics.median(sz_h_by_cluster[c]) if nsz else None})
    strengths = sorted([r for r in lq_rows if r["lq"] and r["lq"] >= 1.2 and r["n_sz"] >= 5],
                       key=lambda x: -x["lq"])[:10]
    weaknesses = sorted([r for r in lq_rows if r["lq"] and r["lq"] <= 0.8 and r["n_all"] >= 30],
                        key=lambda x: x["lq"])[:10]

    sz = profile["深圳市"]
    bj = profile["北京市"]
    sh = profile["上海市"]
    payload = {
        "metric": METRIC,
        "support_judgment": "部分支持",
        "support_reason": (
            "学者画像五维（规模/影响力/产出/顶才/帽子）在 gkx.dwd_scholar 21,316 行上可全量现转，"
            "领域维可用 13,955 名学者的双锚定论文判簇、按区位商给出优势/短板，诊断骨架成立；"
            "但需求点名的技能匹配度、招聘难度、薪资水平、发展前景四项市场供需维在库内完全无源"
            "（dwd_job 仅 10 行、无薪资字段），对标口径也只有学者库（全国样本实为都市圈 + 京沪）"
            "→ 部分支持。"),
        "method": {
            "region": "五级地名归属：高校名录 → 企业底册 → 前缀 → 城市关键词 → 海外",
            "dims": ["规模", "影响力", "产出", "顶才", "帽子"],
            "domain": "姓名+机构双锚定中文论文 → 20+8 集群 → 区位商 LQ",
            "strength_rule": "LQ≥1.2 且深圳该簇学者≥5",
            "weakness_rule": "LQ≤0.8 且全国该簇学者≥30",
            "market_legs": "不交付（无招聘/薪资/技能字段）",
        },
        "profile": profile,
        "sz_vs": {
            "n_ratio_vs_bj": round(sz["n"] / bj["n"], 4),
            "n_ratio_vs_sh": round(sz["n"] / sh["n"], 4),
            "h_median_gap_vs_bj": round(sz["h_median"] - bj["h_median"], 1),
            "h_median_gap_vs_sh": round(sz["h_median"] - sh["h_median"], 1),
            "h_ge50_rate_gap_vs_bj_pp": round(sz["h_ge50_rate_pct"] - bj["h_ge50_rate_pct"], 2),
            "h_ge50_rate_gap_vs_sh_pp": round(sz["h_ge50_rate_pct"] - sh["h_ge50_rate_pct"], 2),
            "top1_gap_vs_bj": sz["top1_h_min"] - bj["top1_h_min"],
            "top1_gap_vs_sh": sz["top1_h_min"] - sh["top1_h_min"],
            "academician_gap_vs_bj": sz["academicians_matched"] - bj["academicians_matched"],
            "academician_gap_vs_sh": sz["academicians_matched"] - sh["academicians_matched"],
        },
        "domain": {
            "covered_scholars": cov,
            "coverage_pct": round(100 * cov / len(sch), 2),
            "shenzhen_covered": n_sz,
            "region_covered": dict(per_reg_n),
            "clusters": len(lq_rows),
            "lq_rows": sorted(lq_rows, key=lambda x: -(x["lq"] or 0)),
            "strengths": strengths,
            "weaknesses": weaknesses,
        },
        "market_gap": {
            "job_rows": 10,
            "dims_missing": ["技能匹配度", "招聘难度", "薪资水平", "发展前景"],
            "note": "`gkx.dwd_job` 全表 10 行（境外药企样例），无薪资、无技能标签、无投递日志；"
                    "四项市场维一律不交付，不做代理。",
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面口径：五维画像取三列生涯累计值（h / citation_nums / paper_nums），"
                            "领域维取双锚定论文全时段（不做年度截断），因此无基期与增速。"
                            "刻意不构造「近 N 年」窗口，避免把 2024 年的采集堆积读成增长（见 158 的年度分布）。"),
        "probes": {"sql_count": 0,
                   "source": "gkx.dwd_scholar + dwd_scholar_talent_flag + dwd_zh_paper 三份快照"},
        "reused_from": [],
    }
    write_out(METRIC, payload)


if __name__ == "__main__":
    main()
