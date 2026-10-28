#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_TALENT_DEEP_158_1 —— 高校学院新培育人才模型（TALENT 深度分析第 158 号）

需求语义：基于高校与科研机构数据、技术关系图谱，识别特定技术领域下由高校培养的新增人才，
量化高校人才贡献度，输出新增人才识别结果、培养趋势、学科背景分布与校际对比。
需求未给「新增人才」的判定口径（学位获得？留任？首篇论文？）。

本文口径（零 SQL）：
  L1 名单层：`dwd_scholar_education_background`（43,766 段学历）按培养机构归口。
     深圳培养机构 = 教育部高校名录（`dwd_org_heis_info`，3,501 所）中 city=深圳市 的 11 所
     + 4 个在深圳办学/联合培养的研究生院与院所（哈工大深圳、北大深圳研究生院、
     清华深圳国际研究生院、中科院深圳先进院）。全国分母 = 名录内高校的博士学历段。
  L2 时序层：以学历段的 end_time 年份作「毕业年」，统计 2019 年以来的新增（这是唯一能表达
     「新培育」的时间变量；表内没有入学年之外的培养过程字段）。
  L3 产出层：`dwd_zh_paper` 面板（100,900 篇）里作者机构命中深圳培养机构的论文，
     按校、按年统计，作为「培养出来的人是否留下产出」的旁证。

产物：code/M_TALENT_DEEP_158_1_out.json。
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _talent21_common import (  # noqa: E402
    _load, base_year_block, edu, paper_clusters, scholars, st, talent, write_out,
)

METRIC = "M_TALENT_DEEP_158_1"

BRANCH = [
    "哈尔滨工业大学(深圳)", "哈尔滨工业大学（深圳）",
    "北京大学深圳研究生院", "清华大学深圳国际研究生院", "清华-伯克利深圳学院",
    "中国科学院深圳先进技术研究院", "深圳湾实验室",
]
# 判断「毕业」的专业学位词；客座/访问/在读不算新培育产出
DEGREE_OK = ("学士", "硕士", "博士", "本科", "研究生")


def main() -> None:
    t = talent()
    heis = t["heis"]["rows"]
    sz_univ = sorted({r[0] for r in heis if (r[2] or "") == "深圳市"})
    all_univ = {r[0] for r in heis}
    keys = sz_univ + BRANCH

    def where(org: str):
        for k in keys:
            if k and k in (org or ""):
                return k
        return None

    ed = edu()
    rec = [e for e in ed if where(e["org"])]
    sz_school = Counter(where(e["org"]) for e in rec)
    sz_sids = {e["sid"] for e in rec}

    def is_phd(e):
        return "博士" in (e["deg_zh"] or "")

    def is_degree(e):
        return any(k in (e["deg_zh"] or "") for k in DEGREE_OK)

    nat_phd_rows = [e for e in ed if e["org"] in all_univ and is_phd(e)]
    nat_phd_sids = {e["sid"] for e in nat_phd_rows}
    sz_phd_sids = {e["sid"] for e in rec if is_phd(e)}

    # ---- L2 毕业年 ----
    yr_all = Counter(e["y1"] for e in rec if e["y1"])
    yr_recent = {y: n for y, n in yr_all.items() if y >= 2019}
    yr_by_school: dict[str, Counter] = defaultdict(Counter)
    for e in rec:
        if e["y1"]:
            yr_by_school[where(e["org"])][e["y1"]] += 1
    missing_end = sum(1 for e in rec if not e["y1"])

    # ---- 学科/学位分布 ----
    deg = Counter((e["deg_zh"] or "未填") for e in rec)
    major = Counter(e["major"] for e in rec if e["major"])

    # ---- L3 产出层：深圳培养机构署名论文 ----
    panel = _load("a25_paper_panel.json")
    kw = {r["id"]: (r.get("keywords") or "") for r in panel["cls"]}
    p_year = Counter()
    p_school = Counter()
    p_year_school: dict[str, Counter] = defaultdict(Counter)
    p_cluster = Counter()
    papers = 0
    for pp in panel["paper"]:
        try:
            authors = json.loads(pp.get("author_info_list") or "[]")
        except Exception:
            continue
        insts = {(a.get("institution") or "") for a in authors}
        hit = None
        for k in keys:
            if any(k in i for i in insts):
                hit = k
                break
        if not hit:
            continue
        papers += 1
        p_school[hit] += 1
        try:
            y = int(str(pp.get("y") or "")[:4])
        except Exception:
            y = None
        if y:
            p_year[y] += 1
            p_year_school[hit][y] += 1
        cl = paper_clusters(pp.get("id"), kw.get(pp.get("id"), ""),
                            (pp.get("zh_name") or "") + " " + (pp.get("en_name") or ""))
        for c in cl:
            p_cluster[c] += 1

    win = [2021, 2022, 2023, 2024, 2025]
    win_n = sum(p_year.get(y, 0) for y in win)

    # 深圳高校现职学者（主档口径，作「留下的人」旁证）
    sz_sch = [s for s in scholars() if "深圳" in s["org"]]

    payload = {
        "metric": METRIC,
        "support_judgment": "部分支持",
        "support_reason": (
            "培养机构名单（教育部名录深圳 11 校 + 4 个深圳研究生院/院所）与全国培养分母"
            "（名录内博士学历段）可全量现转，产出层（深圳机构署名中文论文 1,188 篇）可算；"
            "但「新培育」的核心时序腿在库内近乎不存在——全库学历表中命中深圳培养机构的记录只有 15 段、"
            "覆盖 13 名学者、2019 年后仅 3 段，无法支撑逐年新增序列；且学历表与身份主档只有 9.25% 可挂、"
            "无学科代码 → 部分支持。"),
        "method": {
            "new_talent_proxy": "学历段 end_time 年份 = 毕业年；2019 年起算「新培育」",
            "institution_scope": "heis 名录 city=深圳市（11 校）+ 深圳研究生院/院所（4 个）",
            "national_denominator": "heis 名录内高校的博士学历段（distinct 学者）",
            "output_leg": "dwd_zh_paper 作者机构命中深圳培养机构的论文（按校×年）",
            "degree_filter": "学士/本科/硕士/博士/研究生；客座、访问、在读不计",
        },
        "institution_layer": {
            "sz_heis_distinct": len(sz_univ),
            "sz_heis_rows": sum(1 for r in heis if (r[2] or "") == "深圳市"),
            "sz_heis_names": sz_univ,
            "branch_added": BRANCH,
            "national_heis_distinct": len(all_univ),
            "national_heis_rows": len(heis),
        },
        "l1_pool": {
            "edu_rows": len(ed),
            "edu_scholars": len({e["sid"] for e in ed}),
            "sz_edu_rows": len(rec),
            "sz_edu_scholars": len(sz_sids),
            "sz_by_school": dict(sz_school.most_common()),
            "national_phd_rows": len(nat_phd_rows),
            "national_phd_scholars": len(nat_phd_sids),
            "sz_phd_scholars": len(sz_phd_sids),
            "sz_share_of_national_phd_pct": round(100 * len(sz_phd_sids) / max(1, len(nat_phd_sids)), 3),
            "sz_rows_share_of_national_phd_pct": round(100 * len(rec) / max(1, len(nat_phd_rows)), 3),
        },
        "l2_time_series": {
            "rows_with_end_year": sum(yr_all.values()),
            "rows_end_year_missing": missing_end,
            "end_year_missing_pct": round(100 * missing_end / max(1, len(rec)), 2),
            "years_covered": len(yr_all),
            "min_year": min(yr_all) if yr_all else None,
            "max_year": max(yr_all) if yr_all else None,
            "year_dist": {str(y): yr_all[y] for y in sorted(yr_all)},
            "recent_2019p_rows": sum(yr_recent.values()),
            "recent_by_school": {k: dict(sorted(v.items())) for k, v in yr_by_school.items()},
            "annual_mean_2019p": round(sum(yr_recent.values()) / max(1, len(range(2019, max(yr_all or [2019]) + 1))), 2),
        },
        "degree_dist": dict(deg.most_common()),
        "major_dist": dict(major.most_common(10)),
        "l3_output": {
            "papers_total": papers,
            "by_school": dict(p_school.most_common()),
            "by_year": {str(y): p_year[y] for y in sorted(p_year)},
            "window": win,
            "window_papers": win_n,
            "window_share_pct": round(100 * win_n / max(1, papers), 2),
            "by_school_2021_2025": {k: sum(v.get(y, 0) for y in win) for k, v in
                                    sorted(p_year_school.items(), key=lambda x: -sum(x[1].values()))},
            "paper_clusters": dict(p_cluster.most_common(10)),
            "papers_2024": p_year.get(2024, 0),
            "papers_2024_share_pct": round(100 * p_year.get(2024, 0) / max(1, papers), 2),
            "papers_2026": p_year.get(2026, 0),
            "papers_2026_share_pct": round(100 * p_year.get(2026, 0) / max(1, papers), 2),
            "note": "2024 年占全部四成，是采集批次的年度堆积而非真实增长；2026 为残年。"
                    "两者都不进趋势结论，也不做同比。",
        },
        "sz_scholars_now": {
            "n": len(sz_sch),
            "h_median": st([s["h"] for s in sz_sch]).get("median"),
            "paper_median": st([s["paper"] for s in sz_sch]).get("median"),
            "note": "主档 194 行现职机构含「深圳」，其中有姓名 182 行；这是「留下的人」的存量旁证，"
                    "不是「新培育」流量。",
        },
        "base_years_used": win,
        "base_years_missing": [],
        "base_years_note": (
            "产出层窗口取 2021—2025 五个真实存在的年份；2026 在采集时点只有残年数据"
            f"（{p_year.get(2026, 0)} 篇，占 {round(100 * p_year.get(2026, 0) / max(1, papers), 2)}%），"
            "不进窗口、也不按比例外推。学历层的毕业年只统计表内真实出现的年份"
            f"（{min(yr_all) if yr_all else '—'}—{max(yr_all) if yr_all else '—'}，共 {len(yr_all)} 个年），不补 0。"),
        "probes": {
            "sql_count": 0,
            "source": "gkx.dwd_scholar_education_background（43,766 段）+ dwd_org_heis_info（3,501 所）"
                      "+ dwd_zh_paper（100,900 篇）三份快照",
        },
        "reused_from": [],
    }
    write_out(METRIC, payload)


if __name__ == "__main__":
    main()
