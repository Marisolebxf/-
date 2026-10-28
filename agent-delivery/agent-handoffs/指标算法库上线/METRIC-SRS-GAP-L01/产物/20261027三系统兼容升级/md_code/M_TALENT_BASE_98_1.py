#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_TALENT_BASE_98_1 —— 人才基础指标模型构建（TALENT 基础指标 / SRS 序号 98）

需求四族：D1 人才分布、D2 人才机构分布、D3 人才领域分布、D4 人才供给数量。
本件是**分组计数族**，不是打分族：输出四张分组统计表 + 覆盖率，不做加权合成。

三处必须写在明面上的口径边界：
  1. 「人才」= `gkx.dwd_scholar` 的 21,316 名学者（商业人才库/企业研发人员不在库内）；
  2. D1/D2 的地理归属靠机构名 → 高校名录/企业底册，覆盖率 89.1%（有机构名者）；
  3. D3/D4 是**独立表口径**：`research_direction` 与 `education_background` 的 scholar_id
     与主档只有 9.3% 交集且无姓名列，无法与 D1/D2 交叉（出不了「某省博士数」）。

数据全部来自 `_snapshots21/probe_talent21_20261022.json` + `base_20261021.json`，零 SQL。
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _talent21_common import (  # noqa: E402
    base_year_block, edu, loc, research, scholars, st, talent, write_out,
)

METRIC = "M_TALENT_BASE_98_1"


def norm_degree(r: dict) -> str:
    """学历中英双语归一（中文缺译 9,825 行，单靠中文列会把 22.4% 打成未知）。"""
    zh = r["deg_zh"]
    en = (r["deg_en"] or "").lower()
    if "博士后" in zh:
        return "其他"
    if "博士" in zh or "phd" in en or "doctor" in en:
        return "博士"
    if "硕士" in zh or "master" in en:
        return "硕士"
    if "学士" in zh or "本科" in zh or "bachelor" in en:
        return "学士"
    if not zh and not r["deg_en"]:
        return "未知"
    return "其他"


def main() -> None:
    sch = scholars()
    n_all = len(sch)
    with_org = [s for s in sch if s["org"]]

    # ---------------- D1 人才分布（机构属地 → 省/市）----------------
    prov = Counter()
    city = Counter()
    method = Counter()
    for s in with_org:
        p, c, how = loc(s["org"])
        prov[p] += 1
        city[c] += 1
        method[how] += 1
    assigned = sum(v for k, v in prov.items() if k not in ("未归属", "未填", "海外"))
    d1 = {
        "n_scholars": n_all,
        "with_org_name": len(with_org),
        "assigned": assigned,
        "assigned_pct_of_all": round(100 * assigned / n_all, 2),
        "assigned_pct_of_with_org": round(100 * assigned / len(with_org), 2),
        "unassigned": prov["未归属"],
        "foreign": prov["海外"],
        "method": dict(method),
        "top_provinces": [{"province": k, "n": v} for k, v in prov.most_common(15)
                          if k not in ("未归属", "海外", "未填")],
        "top_cities": [{"city": k, "n": v} for k, v in city.most_common(12)
                       if k not in ("未归属", "海外", "未填")],
        "n_provinces": len([k for k in prov if k not in ("未归属", "海外", "未填")]),
        "growth": None,
        "growth_note": "D1 为截面存量，库内无「人才首次建档年」，无法算省域环比；"
                       "强行用毕业年推算会在 §3.16 意义上制造缺失年分母，故不出增长率。",
    }

    # ---------------- D2 人才机构分布 ----------------
    org_cnt = Counter(s["org"] for s in with_org)
    heis = {r[0]: r for r in talent()["heis"]["rows"] if r[0]}
    org_prov = Counter()
    org_type = Counter()
    for o in org_cnt:
        p, _c, how = loc(o)
        org_prov[p if p != "未填" else "未归属"] += 1
        if o in heis:
            org_type[heis[o][3] or "高校（未标层次）"] += 1
        elif how in ("base_exact", "base_prefix"):
            org_type["企业/其他法人"] += 1
        elif how in ("city_kw", "foreign"):
            org_type["未入名录（机构名可属地）"] += 1
        else:
            org_type["未识别"] += 1
    d2 = {
        "n_distinct_orgs": len(org_cnt),
        "n_heis_matched": len([o for o in org_cnt if o in heis]),
        "top_orgs": [{"org": k, "n": v} for k, v in org_cnt.most_common(15)],
        "province_org_counts": [{"province": k, "n_orgs": v} for k, v in org_prov.most_common(12)
                                if k not in ("未归属",)],
        "type_break": dict(org_type),
        "growth": None,
        "growth_note": "机构档无建档时间戳，机构数环比不可算（旧版用毕业年代理，本版不再沿用）。",
    }

    # ---------------- D3 人才领域分布（独立表口径）----------------
    rd = research()
    tag_cnt = Counter()
    multi = 0
    for sid, ts in rd.items():
        tag_cnt.update(ts)
        if len(ts) > 1:
            multi += 1
    d3 = {
        "n_rows": len(talent()["research"]["rows"]),
        "n_scholars_with_fields": len(rd),
        "n_tags": len(tag_cnt),
        "tag_hits": sum(tag_cnt.values()),
        "multi_value_scholars": multi,
        "multi_value_pct": round(100 * multi / len(rd), 2) if rd else None,
        "top_tags": [{"tag": k, "n": v} for k, v in tag_cnt.most_common(20)],
        "tags_ge_100": sum(1 for v in tag_cnt.values() if v >= 100),
        "tags_eq_1": sum(1 for v in tag_cnt.values() if v == 1),
        "growth": None,
        "growth_note": "research_direction 无年份列，领域环比增长率不可算；且该表 scholar_id 与主档"
                       "仅 9.3% 可连，无法按省/机构切片。",
    }

    # ---------------- D4 人才供给数量（学位 × 毕业年）----------------
    E = edu()
    deg = Counter(norm_degree(r) for r in E)
    yrs = Counter(r["y1"] for r in E if r["y1"])
    series = []
    for y in range(2010, 2027):
        row = {"year": y}
        for d in ("博士", "硕士", "学士", "其他", "未知"):
            row[d] = sum(1 for r in E if r["y1"] == y and norm_degree(r) == d)
        row["total"] = sum(row[d] for d in ("博士", "硕士", "学士", "其他", "未知"))
        series.append(row)
    d4 = {
        "n_rows": len(E),
        "n_scholars": len({r["sid"] for r in E}),
        "degree_counts": dict(deg),
        "degree_sum_check": sum(deg.values()),
        "rows_with_year": sum(v for v in yrs.values()),
        "rows_without_year": len(E) - sum(v for v in yrs.values()),
        "year_series": series,
        "last_complete_year": 2024,
        "partial_years": {"2025": yrs.get(2025, 0), "2026": yrs.get(2026, 0)},
        "base_years": base_year_block(
            [2015, 2024], [],
            "仅取 2015 与 2024 两个完整年对比；2025/2026 为残年不计入任何分母。"
            "注意该序列是「存量学者的毕业年回溯」，不是当年全口径毕业生流量。"),
        "y2015": sum(1 for r in E if r["y1"] == 2015 and norm_degree(r) == "博士"),
        "y2024": sum(1 for r in E if r["y1"] == 2024 and norm_degree(r) == "博士"),
        "zh_missing_en_available": sum(1 for r in E if not r["deg_zh"] and r["deg_en"]),
    }

    payload = {
        "metric": METRIC,
        "support_judgment": "部分支持",
        "support_reason": "四族分组计数都能出数（学者 21,316、机构 2,108、方向标签 97,249、学历行 43,766），"
                          "但三处硬缺口始终存在：①「人才」只有学者口径，企业研发人员/技能人才无表；"
                          "② D4 是存量学者学历回溯，不是学科×年份的官方供给流量，且无学科码；"
                          "③ D3/D4 的 scholar_id 与主档仅 9.3% 可连，四族不能交叉切片、D2/D3 无年份列"
                          "故增长率不可算 → 部分支持。",
        "method": {
            "type": "分组计数（entity × attribute × time），无加权合成",
            "D1": "学者现机构名 → 高校名录/企业底册/城市关键词 → 省·市",
            "D2": "现机构名去重 → 机构数；高校名录取 univ_type；其余按底册/未识别归类",
            "D3": "research_direction.fields 分号拆分展开后按标签计数",
            "D4": "education_background 学位双语归一 × 毕业年计数",
            "sql_count": 0,
        },
        "D1": d1, "D2": d2, "D3": d3, "D4": d4,
        "id_gap": {
            "work_exp_overlap": 1856, "work_exp_rows": 20028,
            "edu_overlap": 1853, "edu_rows": 20025,
            "research_overlap": 1853, "research_rows": 19514,
            "by_id_key": 1509,
            "note": "三张子表无姓名列，无法二次桥接；改用 dwd_scholar.id 连只有 1,509 行，故不采用。",
        },
        "probes": {"source": "_snapshots21/probe_talent21_20261022.json; base_20261021.json",
                   "sec": {"work_exp": 2.69, "edu": 0.88, "research": 4.43, "heis": 0.7}},
    }
    write_out(METRIC, payload)
    print("D1 assigned", d1["assigned"], "D2 orgs", d2["n_distinct_orgs"],
          "D3 tags", d3["n_tags"], "D4 rows", d4["n_rows"])


if __name__ == "__main__":
    main()
