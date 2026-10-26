#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SYNTH_182_1 区域科技创新成果综合评价模型 —— gkx 换源复现（20261022）。

口径（王惠）：三维（基础科学 / 应用科技 / 科研机构），维内两子项批内极值归一、
维内等权、三维等权、缺维记空不补 0。评价集改为 gkx 可归属的深圳都市圈四城
（深圳/广州/东莞/惠州）：底册 99.82% 落在这四市，北京/上海专利申请人无法归属。

数据面（零专利 SQL）：
  论文/被引  a25_paper_panel.json（100,900 篇）× probe_a26_20261022.json（20,031 条被引）
  专利授权   patent_2024_by_name_20261021.json → 底册 name→city（重名 1/k）
  高价值     同上 × patent_scan_20261021.pkl 的 value_2024，阈值 = 申请人级 P90
  专利转移   cityfam_transfer_2024_20261021.json（7,711 条）
  科研机构   probe_synth21.json（2,074 行，仅深/广/莞/惠）
输出：M_SYNTH_182_1_out.json
"""
from __future__ import annotations

import collections
import json
import statistics

import _synth21_common as S

MID = "M_SYNTH_182_1"
WINDOW = (2021, 2022, 2023, 2024)


def p70_citation() -> tuple[float, dict]:
    """保留被引表的口径记录：20,031 条被引记录只覆盖抽样面板的 782 篇（0.78%），
    因此被引不能做城市级指标；这里只输出其分布供「数据可得性」章节引用。"""
    rows = S._load("probe_a26_20261022.json")["zh_citation"]["rows"]
    vals = sorted(int(r[1] or 0) for r in rows)
    p70 = float(vals[int(len(vals) * 0.7)]) if vals else 0.0
    ids = {str(r[0]) for r in rows}
    hit = sum(1 for p in S.papers() if p["id"] in ids)
    return p70, {"n": len(vals), "min": vals[0] if vals else 0,
                 "max": vals[-1] if vals else 0,
                 "median": statistics.median(vals) if vals else 0,
                 "matched_papers_in_panel": hit}


def basic_dim() -> dict:
    p70, cstat = p70_citation()
    ji = S.journal_impact()
    thr = ji["p90"]
    papers = [p for p in S.papers() if p["year"] in WINDOW]
    n_city = collections.Counter()
    hq = collections.Counter()
    matched = collections.Counter()
    for p in papers:
        imp = ji["map"].get(p["journal"])
        for c in p["cities"]:
            n_city[c] += 1
            if imp is not None:
                matched[c] += 1
                if imp >= thr:
                    hq[c] += 1
    score = {}
    for c in S.CITIES:
        score[c] = S.wmean([S.mm(n_city).get(c), S.mm(hq).get(c)])
    ref = {}
    for c in S.REF_CITIES:
        ref[c] = {"papers": n_city.get(c, 0), "hq_journal_papers": hq.get(c, 0)}
    return {
        "journal_p90_avg_cite": thr, "journal_universe": ji["n_journals"],
        "journal_median_avg_cite": ji["median"],
        "citation_probe": cstat, "citation_p70": p70,
        "window": list(WINDOW),
        "papers_in_window": len(papers),
        "papers_city_attributable": sum(1 for p in papers if p["cities"]),
        "papers": {c: n_city.get(c, 0) for c in S.CITIES},
        "papers_with_journal": {c: matched.get(c, 0) for c in S.CITIES},
        "hq_journal_papers": {c: hq.get(c, 0) for c in S.CITIES},
        "sub_scores": {"papers": S.mm({c: n_city.get(c, 0) for c in S.CITIES}),
                       "hq": S.mm({c: hq.get(c, 0) for c in S.CITIES})},
        "score": score, "ref_cities": ref,
    }


def applied_dim() -> dict:
    g = S.grants2024_by_city()
    v = S.value2024()
    vals = sorted(float(x) for x in v.values() if x)
    p90 = vals[int(len(vals) * 0.9)] if vals else 0.0
    hv = S.high_value2024_by_city(p90)
    tr = S.transfer2024_by_city()
    hv_score = S.mm({c: hv["by_city"].get(c, 0) for c in S.CITIES})
    tr_score = S.mm({c: tr["by_city"].get(c, 0) for c in S.CITIES})
    score = {c: S.wmean([hv_score.get(c), tr_score.get(c)]) for c in S.CITIES}
    return {
        "threshold_value_p90": p90, "value_universe": hv["value_universe"],
        "grants_2024": {c: round(g["by_city"].get(c, 0)) for c in S.CITIES},
        "grants_unmapped": round(g["unmapped"]), "grants_total": round(g["total"]),
        "hv_patents_2024": {c: round(hv["by_city"].get(c, 0)) for c in S.CITIES},
        "hv_applicants": hv["n_hv_names"], "hv_grants_total": round(hv["n_hv_grants"]),
        "transfers_2024": {c: round(tr["by_city"].get(c, 0)) for c in S.CITIES},
        "transfers_total_rows": tr["n_transfers"],
        "sub_scores": {"hv": hv_score, "transfer": tr_score},
        "score": score,
    }


def institute_dim() -> dict:
    inst = S.institutes()
    stock = collections.Counter(i["city"] for i in inst)
    names = {i["name"]: i["city"] for i in inst if i["name"]}
    p24 = S.patent2024()
    grants = collections.Counter()
    for nm, city in names.items():
        if nm in p24:
            grants[city] += float(p24[nm][1] or 0)
    tr = S._load("cityfam_transfer_2024_20261021.json") or []
    trc = collections.Counter()
    for r in tr:
        try:
            lst = json.loads(r[1]) if isinstance(r[1], str) else []
        except Exception:
            lst = []
        for a in lst if isinstance(lst, list) else []:
            nm = (a.get("name") or "").strip() if isinstance(a, dict) else ""
            if nm in names:
                trc[names[nm]] += 1
    ratio, sub = {}, {}
    for c in S.CITIES:
        g = grants.get(c, 0)
        ratio[c] = round(trc.get(c, 0) / g, 4) if g else None
    sub = {"stock": S.mm({c: stock.get(c, 0) for c in S.CITIES}),
           "grants": S.mm({c: grants.get(c, 0) for c in S.CITIES})}
    score = {c: S.wmean([sub["stock"].get(c), sub["grants"].get(c)]) for c in S.CITIES}
    return {"stock": {c: stock.get(c, 0) for c in S.CITIES},
            "inst_grants_2024": {c: round(grants.get(c, 0)) for c in S.CITIES},
            "inst_transfers_2024": {c: trc.get(c, 0) for c in S.CITIES},
            "transfer_ratio_context": ratio, "sub_scores": sub, "score": score,
            "names_matched": sum(1 for n in names if n in p24)}


def main() -> None:
    d1, d2, d3 = basic_dim(), applied_dim(), institute_dim()
    index, n_dims = {}, {}
    for c in S.CITIES:
        parts = [d1["score"].get(c), d2["score"].get(c), d3["score"].get(c)]
        parts = [p for p in parts if p is not None]
        n_dims[c] = len(parts)
        # 至少两维才出指数：单维均值不是可比的综合指数（本批京沪即因此记空）
        index[c] = S.wmean(parts) if len(parts) >= 2 else None
    rank = sorted([c for c in S.CITIES if index[c] is not None],
                  key=lambda c: -index[c])

    out = {
        "metric_id": MID,
        "metric_name": "区域科技创新成果综合评价模型",
        "generated_at": "2026-10-22",
        "db": "gkx（三方库 183.240.141.251:3318，只读）",
        "evaluation_set": S.CITIES,
        "evaluation_set_reason": ("gkx 企业底册 189,116 行中 99.82% 落在深圳/广州/东莞/惠州，"
                                  "专利申请人按底册归城只能覆盖这四市；北京/上海申请人落入"
                                  "「未归属」桶（2024 年 40,888 件授权），故不进综合指数，"
                                  "只出论文维参考读数。"),
        "year": S.T_YEAR,
        "dims": {"D1_basic_science": d1, "D2_applied_tech": d2, "D3_institute": d3},
        "dim_scores": {
            "D1": d1["score"], "D2": d2["score"], "D3": d3["score"],
        },
        "n_dims_available": n_dims,
        "index_0_100": index,
        "rank": rank,
        "min_dims_for_index": 2,
        "support_judgment": "部分支持",
        "support_reason": (
            "三维在深莞惠广四城全部可算且非退化（论文/被引、2024 授权与高价值代理、"
            "机构存量与转化率均有量）；但①评价集被迫收缩到深圳都市圈：专利申请人"
            "按底册归城时北京/上海不可归属（2024 年 40,888 件授权未归属），跨省横比"
            "在本数据面上不成立；②科研机构底册 2,074 行只覆盖深广莞惠，京沪零行；"
            "③高价值专利只能用申请人级 value P90 代理，无法对齐国知局四要件；"
            "④论文城市归属仅 47.4% 可判（机构串含城市名或白名单高校）。"
            "两条以上依赖维结构性不可得，判部分支持。"),
        "note": ("专利授权取 2024 年（完整年），专利库只有 2021–2026；高价值阈值 = "
                 "申请人 2024 年最高 value 的批内 P90（%s），不是逐件 value≥P70；"
                 "转移为 2024 年同库内权利转移记录，口径窄于官方备案。" % d2["threshold_value_p90"]),
    }
    out.update(S.base_year_block(
        WINDOW, [2017, 2018, 2019, 2020],
        "论文窗口 2021–2024（4 个真实年份）；专利授权与转移为 2024 单年；"
        "专利库 2017–2020 零行，故这四年不进任何分母；2025 年库内件数回落、2026 为残年，均不取。"))
    S.write_out(MID, out)
    print(json.dumps({"index": index, "rank": rank, "D1": d1["score"],
                      "D2": d2["score"], "D3": d3["score"]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
