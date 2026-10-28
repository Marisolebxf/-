#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_SYNTH_189_1 区域创新要素领域综合评价模型 —— gkx 换源复现（20261022）。

五维（对应王惠口径「各维度内指标加权 → 五维得分 → 汇总指数」）：
  D1 人才要素   学者数 + 博士学位学者数（按机构串归城）
  D2 研发投入   2024 年上市主体研发费用（亿元）+ 有研发支出的上市主体数
  D3 产业主体   企业底册数 + 国家级高新技术企业数
  D4 技术领域   专精特新中小企业数 + 科技型中小企业数
  D5 创新载体   科研机构数 + 普通高校数

维内两子项批内极值归一、维内等权、五维等权；某维数据不足记 null，不补 0。
评价集 = 深圳/广州/东莞/惠州（底册 99.82%，见 DATA_FACTS §3.8），京沪不出分。
输出：M_SYNTH_189_1_out.json
"""
from __future__ import annotations

import collections
import json

import _synth21_common as S

MID = "M_SYNTH_189_1"
YEAR = 2024
MIN_SCHOLARS = 30          # 低于此数视为学者表覆盖不足，该维记 null 而非 0


def d1_talent() -> dict:
    sc = S.scholars()
    deg = S.scholar_degrees()
    n = collections.Counter()
    phd = collections.Counter()
    master = collections.Counter()
    for s in sc:
        c = s["city"]
        if c not in S.CITIES:
            continue
        n[c] += 1
        d = deg.get(s["id"], "其他")
        if d == "博士":
            phd[c] += 1
        elif d == "硕士":
            master[c] += 1
    raw = {c: n.get(c, 0) for c in S.CITIES}
    raw_phd = {c: phd.get(c, 0) for c in S.CITIES}
    coverage_ok = {c: raw[c] >= MIN_SCHOLARS for c in S.CITIES}
    sub = {"scholars": S.mm(raw), "phd": S.mm(raw_phd)}
    score = {}
    for c in S.CITIES:
        score[c] = S.wmean([sub["scholars"].get(c), sub["phd"].get(c)]) if coverage_ok[c] else None
    return {"scholars": raw, "phd_scholars": raw_phd,
            "master_scholars": {c: master.get(c, 0) for c in S.CITIES},
            "coverage_ok": coverage_ok, "min_scholars": MIN_SCHOLARS,
            "scholar_universe": len(sc),
            "scholar_unmapped": sum(1 for s in sc if not s["city"]),
            "sub_scores": sub, "score": score}


def d2_rd() -> dict:
    rd = S.rd_by_city()
    amt = {c: rd["by_city_2024_yi"].get(c) for c in S.CITIES}
    orgs = {c: rd["orgs_by_city"].get(c) for c in S.CITIES}
    sub = {"amount_yi": S.mm(amt), "orgs": S.mm(orgs)}
    score = {c: S.wmean([sub["amount_yi"].get(c), sub["orgs"].get(c)]) for c in S.CITIES}
    return {"year": YEAR, "amount_yi": amt, "orgs": orgs,
            "orgs_total": rd["orgs_total"], "sub_scores": sub, "score": score,
            "source_rule": rd["source_rule"], "anomaly": rd["anomaly"]}


def d3_entities() -> dict:
    tot = S.base()["city_tot"]
    ent = {c: tot.get(c, 0) for c in S.CITIES}
    ht = S.hightech_by_city()
    htc = {c: ht.get(c, 0) for c in S.CITIES}
    sub = {"enterprises": S.mm(ent), "hightech": S.mm(htc)}
    score = {c: S.wmean([sub["enterprises"].get(c), sub["hightech"].get(c)]) for c in S.CITIES}
    return {"enterprises": ent, "hightech": htc,
            "hightech_total": sum(ht.values()),
            "hightech_share": {c: round(htc[c] / ent[c], 4) if ent[c] else None for c in S.CITIES},
            "sub_scores": sub, "score": score}


def d4_tech() -> dict:
    zjx = S.tag_counts_by_city("专精特新")
    kzx = S.tag_counts_by_city("科技型中小企业")
    a = {c: zjx.get(c, 0) for c in S.CITIES}
    b = {c: kzx.get(c, 0) for c in S.CITIES}
    sub = {"srdi": S.mm(a), "sme": S.mm(b)}
    score = {c: S.wmean([sub["srdi"].get(c), sub["sme"].get(c)]) for c in S.CITIES}
    ipc = S.ipc_breadth_by_city()
    return {"srdi": a, "sme": b, "sub_scores": sub, "score": score,
            "ipc_breadth_context": {c: ipc.get(c) for c in S.CITIES}}


def d5_carriers() -> dict:
    inst = collections.Counter(i["city"] for i in S.institutes())
    rows = (S.probe_talent().get("heis", {}) or {}).get("rows") or []
    uni = collections.Counter(str(r[2]).strip() for r in rows)
    benke = collections.Counter(str(r[2]).strip() for r in rows if str(r[4]).strip() == "本科")
    a = {c: inst.get(c, 0) for c in S.CITIES}
    b = {c: uni.get(c, 0) for c in S.CITIES}
    sub = {"institutes": S.mm(a), "universities": S.mm(b)}
    score = {c: S.wmean([sub["institutes"].get(c), sub["universities"].get(c)]) for c in S.CITIES}
    return {"institutes": a, "universities": b,
            "universities_benke": {c: benke.get(c, 0) for c in S.CITIES},
            "university_rows": len(rows), "sub_scores": sub, "score": score}


def main() -> None:
    dims = {"D1_talent": d1_talent(), "D2_rd": d2_rd(), "D3_entities": d3_entities(),
            "D4_tech": d4_tech(), "D5_carriers": d5_carriers()}
    index, nd = {}, {}
    for c in S.CITIES:
        parts = [dims[k]["score"].get(c) for k in dims]
        parts = [p for p in parts if p is not None]
        nd[c] = len(parts)
        index[c] = S.wmean(parts) if len(parts) >= 3 else None
    rank = sorted([c for c in S.CITIES if index[c] is not None], key=lambda c: -index[c])

    out = {
        "metric_id": MID,
        "metric_name": "区域创新要素领域综合评价模型",
        "generated_at": "2026-10-22",
        "db": "gkx（三方库 183.240.141.251:3318，只读）",
        "evaluation_set": S.CITIES,
        "evaluation_set_reason": ("企业底册 189,116 行中 188,774 行（99.82%）落在深/广/莞/惠；"
                                  "本科室要素表（高企、专精特新、研发费用）全部依赖底册 org_id 归城，"
                                  "因此评价集只能是这四市。"),
        "year": YEAR,
        "dim_weights": {k: 1 / len(dims) for k in dims},
        "dims": dims,
        "dim_scores": {k: dims[k]["score"] for k in dims},
        "n_dims_available": nd,
        "index_0_100": index,
        "rank": rank,
        "min_dims_for_index": 3,
        "support_judgment": "部分支持",
        "support_reason": (
            "五维中四维（投入/主体/技术/载体）在四城均有真实非零读数，且互不重复取数；"
            "但人才维只有深圳（247 位）、广州（918 位）达到可评分门槛，东莞 9 位、惠州 0 位，"
            "属学者表覆盖不足而非真实为零，故这两城人才维记 null（不补 0），指数由其余四维等权；"
            "研发投入只能取上市主体（856 家，占底册 0.45%），不是全口径 R&D；"
            "惠州 2024 年研发费用 175.39 亿元、较 2022 年 48.91 亿元增 258%，与 2023 年"
            "166.37 亿元的跳升需按主体核对（惠州 24 家上市主体里 1 家即可主导），已在 §三 披露。"),
        "note": ("维内两子项批内极值归一后等权；五维等权；某城某维覆盖不足记 null。"
                 "「专精特新」「科技型中小企业」取机构技术标签表命中的去重企业数（同一企业多标签只计一次）。"),
    }
    out.update(S.base_year_block(
        [YEAR], [],
        "研发费用取 2024 年 12 月累计值（1 个真实年份，来源 gba_rd_20261021.json，"
        "2019–2024 连续可用但本指标只用 2024）；企业底册、高企、专精特新、机构、高校、"
        "学者均为截面存量，无跨年分母，故 base_years_missing 为空。"))
    S.write_out(MID, out)
    print(json.dumps({"index": index, "rank": rank,
                      "dims": {k: dims[k]["score"] for k in dims}}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
