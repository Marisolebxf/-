#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_UNIV_NEW —— 高校新建与人才新增（SRS 92/93）。

两条线：
  1. 机构线：高校名录 `dwd_org_heis_info` 3,501 行 → 去重校名、`est_year` 覆盖、
     「新建校」= 建校年 ≥ 2016；深圳高校单列（city=深圳市）。
  2. 人才线：中文论文面板 100,900 篇（a25）→ 2021—2025 年作者单位含「深圳」的论文与作者；
     面板 2024 年占 32.09%（32,379 篇），是抽样结构异常，不能直接算「新增」；
     因此「新作者」= 该年在深圳单位发文、且在该年之前所有年份从未出现的姓名；
     2024 因抽样异常不进入趋势，主报 2025 年（784 人），2021—2023 作对照。
注意：论文面板只含中文论文，英文论文与预印本不在内；作者同名未消歧。
零 SQL；产物 code/M_TALENT_UNIV_NEW_out.json。
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import _talent10_common as C  # noqa: E402

METRIC = "M_TALENT_UNIV_NEW"
Y0, Y1 = 2021, 2025


def main() -> None:
    heis = C.heis_rows()
    names = [h[0] for h in heis if h[0]]
    uniq = sorted(set(names))
    est = {}
    for h in heis:
        if h[0] and h[3]:
            est.setdefault(h[0], int(h[3]))
    levels = Counter(h[5] for h in heis if len(h) > 5 and h[5])
    prov = Counter(h[1] for h in heis if h[1])
    new = sorted([(y, n) for n, y in est.items() if y >= 2016], key=lambda x: (-x[0], x[1]))
    sz_rows = [h for h in heis if len(h) > 2 and h[2] == "深圳市"]
    sz_names = sorted({h[0] for h in sz_rows if h[0]})

    papers = C.load("a25_paper_panel.json")["paper"]
    first: dict[str, int] = {}
    sz_year = Counter()
    sz_uni = Counter()
    sz_authors = set()
    sz_author_year = defaultdict(set)
    sz_paper_ids = []
    parsed = 0
    for p in papers:
        try:
            auth = json.loads(p.get("author_info_list") or "[]")
        except Exception:
            continue
        parsed += 1
        y = int(p["y"]) if str(p.get("y", "")).isdigit() else None
        nm_inst = [((a.get("zh_name") or "").strip(), a.get("institution") or "") for a in auth]
        for nm, inst in nm_inst:
            if nm and y and (nm not in first or y < first[nm]):
                first[nm] = y
        if not y or not (Y0 <= y <= Y1):
            continue
        hit = [(nm, inst) for nm, inst in nm_inst if "深圳" in inst]
        if not hit:
            continue
        sz_paper_ids.append(p["id"])
        sz_year[y] += 1
        for nm, inst in hit:
            if nm:
                sz_authors.add(nm)
                sz_author_year[y].add(nm)
            for u in sz_names:
                if u and u in inst:
                    sz_uni[u] += 1
                    break
    new_by_year = {y: sum(1 for n in s2 if first.get(n, 9999) >= y)
                   for y, s2 in sz_author_year.items() if y != 2024}

    payload = {
        "support_judgment": "部分支持",
        "base_years_used": [2021, 2025],
        "base_years_missing": [2016, 2017, 2018, 2019, 2020],
        "base_years_note": f"论文侧只取 {Y0}—{Y1} 五年（面板覆盖到 2025）；「新建校」用建校年"
                           "≥2016 判定，但没有 2016—2020 的作者首发序列，算不出「新校带来的净增」"
                           "相对基期；新增作者是「面板内首次出现」，不等于人生第一次发文",
        "scope": {"heis_rows": len(heis), "unique_universities": len(uniq),
                  "paper_panel": len(papers), "paper_parsed": parsed,
                  "window": [Y0, Y1], "unit_org": "校名去重", "unit_talent": "作者姓名"},
        "universities": {"rows": len(heis), "unique": len(uniq),
                         "est_year_filled": len(est),
                         "est_year_share": C.share(len(est), len(uniq)),
                         "level_dist": [{"level": k, "n": v} for k, v in levels.most_common()],
                         "province_top": [{"prov": k, "n": v} for k, v in prov.most_common(12)],
                         "new_since_2016": len(new),
                         "new_list_top": [{"name": n, "est_year": y} for y, n in new[:30]],
                         "shenzhen": {"n": len(sz_names), "names": sz_names,
                                      "with_est_year": [{"name": n, "est_year": est.get(n)}
                                                        for n in sz_names]}},
        "papers": {"sz_papers": len(sz_paper_ids), "sz_papers_distinct": len(set(sz_paper_ids)),
                   "year_series": [{"year": y, "n": n} for y, n in sorted(sz_year.items())],
                   "sz_authors_distinct": len(sz_authors),
                   "authors_by_year": [{"year": y, "n": len(s2)}
                                       for y, s2 in sorted(sz_author_year.items())],
                   "new_authors_by_year": [{"year": y, "n": n}
                                           for y, n in sorted(new_by_year.items())],
                   "new_authors_2025": new_by_year.get(2025, 0),
                   "new_share_2025": C.share(new_by_year.get(2025, 0), len(sz_author_year.get(2025, []))),
                   "excluded_year": 2024,
                   "excluded_note": "2024 年论文 32,379 篇（占面板 32.09%），是抽样异常，"
                                    "不进入趋势比较；但 2024 仍计入「是否首次出现」的基期，"
                                    "否则 2025 年会把 2024 才出现的作者误判为新增",
                   "by_university": [{"university": k, "papers": v}
                                     for k, v in sz_uni.most_common()]},
        "data_quality": {
            "heis_est_year": f"3,501 行里只有 {len(est)} 个校名有建校年（{C.share(len(est), len(uniq))}%），"
                             "且 est_year 是「现校名成立年」，合并/更名院校会显得很新",
            "new_definition": "「新建校」只按 est_year≥2016；没有招生规模/首届毕业年，"
                              "不能区分「新设」与「更名/合并」",
            "paper_scope": "a25 面板只含中文论文 100,900 篇，深圳高校的英文产出（占比更高）不在内，"
                           "论文数与作者数都偏低",
            "author_disambig": "作者按姓名字符串去重，同名不同人会被合并；「首次出现」因此偏保守",
            "affiliation": "单位串含「深圳」即计入，含「哈尔滨工业大学(深圳)」等分支校区；"
                           "不含仅写「深圳」之外的简称",
            "no_enrollment": "无招生人数、毕业生数、教师编制，指标只能反映「论文侧活跃作者」",
        },
        "diff_vs_old_draft": {
            "old": "旧稿 2,933 所高校、深圳 11 所、2021—2025 深圳论文 579 篇、新增作者 1,050 人",
            "now": f"{len(uniq):,} 所、深圳 {len(sz_names)} 所、深圳单位论文 "
                   f"{len(set(sz_paper_ids)):,} 篇、窗口内作者 {len(sz_authors):,} 人，"
                   f"2025 年新作者 {new_by_year.get(2025, 0):,} 人（占当年作者 "
                   f"{C.share(new_by_year.get(2025,0), len(sz_author_year.get(2025,[])))}%）",
            "why": "旧稿的 579 篇只统计「深圳高校」为第一单位；本件统计「任一作者单位含深圳」，"
                   "含合作论文、院所与医院，因此篇数高一个量级。新作者旧稿 1,050，本件 2025 年 "
                   f"{new_by_year.get(2025,0):,}，差额来自基期口径（旧稿用 2021—2025 全窗口首次出现）"
                   "与姓名消歧",
        },
        "findings": [
            f"高校名录 {len(heis):,} 行、去重 {len(uniq):,} 所，建校年覆盖 {len(est):,} 所"
            f"（{C.share(len(est), len(uniq))}%），2016 年后建校 {len(new)} 所",
            f"深圳高校 {len(sz_names)} 所；2021—2025 深圳单位论文 {len(set(sz_paper_ids)):,} 篇、"
            f"作者 {len(sz_authors):,} 人；2025 年新作者 {new_by_year.get(2025, 0):,} 人"
            f"（占当年 {len(sz_author_year.get(2025, []))} 位作者的 "
            f"{C.share(new_by_year.get(2025, 0), len(sz_author_year.get(2025, [])))}%）",
            f"论文最多的深圳高校：{sz_uni.most_common(1)[0][0] if sz_uni else '无'}"
            f"（{sz_uni.most_common(1)[0][1] if sz_uni else 0} 篇，按单位串命中）",
        ],
    }
    C.write(METRIC, payload)
    print("heis", len(heis), len(uniq), len(est), "new", len(new), new[:5])
    print("levels", levels.most_common(), "prov", prov.most_common(5))
    print("sz unis", len(sz_names), sz_names, [(n, est.get(n)) for n in sz_names])
    print("sz papers", len(sz_paper_ids), len(set(sz_paper_ids)), "authors", len(sz_authors))
    print("sz year", sorted(sz_year.items()))
    print("authors by year", {y: len(s2) for y, s2 in sorted(sz_author_year.items())})
    print("new by year", sorted(new_by_year.items()))
    print("sz uni", sz_uni.most_common(10))


if __name__ == "__main__":
    main()
