#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_STRUCT_QUERY —— 人才结构查询（SRS 64/65/66 的结构侧）。

结构维（属性宇宙 20,030 人）：最高学位 / 最高职称 / 从业年限 / 学科域 / 机构类型。
  · 最高学位：education_background 全量取最高（博士后>博士>硕士>学士>专科）；
  · 最高职称：work_experience.position 取最高（正高>副高>中级>其他）；
  · 从业年限：2026 − 最早履历起年（年龄整列不可得，见 §三 3.5）；
  · 学科域：research_direction 十域规则；  · 机构类型：最晚一段履历的机构 + 五分类。
院士：talent_flag 112 个 id（与主档交集 80），单列头衔维，不参与学术力加权。
零 SQL；产物 code/M_TALENT_STRUCT_QUERY_out.json。
"""
from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import _talent10_common as C  # noqa: E402

METRIC = "M_TALENT_STRUCT_QUERY"
NOW = 2026


def band(y):
    if y is None:
        return "未知"
    return "<5 年" if y < 5 else "5—10 年" if y < 10 else "10—20 年" if y < 20 else "≥20 年"


def main() -> None:
    work = C.work()
    edu = C.edu()
    res = C.research()
    deg = C.highest_degree()
    pos = C.highest_position()
    attr = {w["sid"] for w in work} | {e["sid"] for e in edu} | set(res)
    N = len(attr)

    latest = {}
    for w in work:
        if not w["org"]:
            continue
        key = (w["y1"] or w["y0"] or 0, 1 if w["cur"] else 0)
        if w["sid"] not in latest or key > latest[w["sid"]][0]:
            latest[w["sid"]] = (key, w["org"])
    cy = {}
    for w in work:
        if w["y0"] and w["y0"] >= 1950:
            cy[w["sid"]] = min(cy.get(w["sid"], 9999), int(w["y0"]))
    cy = {s: NOW - y for s, y in cy.items()}

    def dist(cnt, key, denom=N):
        return [{key: k, "n": v, "share": C.share(v, denom)} for k, v in sorted(cnt.items(), key=lambda kv: (-kv[1], str(kv[0])))]

    dvals = Counter(deg.get(s, "未填") for s in attr)
    pvals = Counter(pos.get(s, "其他/未填") for s in attr)
    cvals = Counter(band(cy.get(s)) for s in attr)
    dom = {}
    for s in attr:
        ds = res.get(s) or []
        dom[s] = C.domain_of(" ".join(ds)) if ds else "其他/未归类"
    mvals = Counter(dom.values())
    otype = {s: (C.org_type(v[1]) if s in latest else "未填") for s, v in latest.items()}
    ovals = Counter(otype.get(s, "未填") for s in attr)

    def cross(a: dict, b: dict):
        m = Counter((a.get(s, "未填"), b.get(s, "未填")) for s in attr)
        out = defaultdict(list)
        for (x, y), n in m.items():
            out[x].append({"key": y, "n": n, "share_in_row": C.share(n, sum(
                v for (xx, yy), v in m.items() if xx == x))})
        return [{"row": k, "cells": sorted(v, key=lambda z: (-z["n"], z["key"])),
                 "total": sum(c["n"] for c in v)} for k, v in sorted(out.items())]

    acad = set(C.load("talent_flag_20261022.json")["scholar_ids"])
    ac_deg = Counter(deg.get(s, "未填") for s in acad)
    ac_pos = Counter(pos.get(s, "其他/未填") for s in acad)
    ac_dom = Counter(dom.get(s, "其他/未归类") for s in acad)
    ac_org = Counter(C.org_type(latest[s][1]) for s in acad if s in latest)

    sz_attr = [s for s in attr if s in latest and C.loc2(latest[s][1])[1] == "深圳市"]
    sz_panel = [r for r in C.rows() if r["city"] == "深圳市"]
    sz_deg = Counter(deg.get(s, "未填") for s in sz_attr)

    payload = {
        "support_judgment": "完全转换支持",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "属性结构截面；学位/职称/方向无年度字段，只能看当前存量。"
                           "「从业年限」用 2026−最早履历起年，止年空的在职者不截断",
        "scope": {"universe": "属性宇宙（work/edu/research 并集）", "n": N,
                  "master_universe": 21316, "intersection_master": 1858,
                  "unit": "scholar_id"},
        "coverage": {"n": N, "degree_filled": N - dvals.get("未填", 0),
                     "position_filled": N - pvals.get("其他/未填", 0),
                     "career_filled": sum(1 for s in attr if s in cy),
                     "domain_filled": N - mvals.get("其他/未归类", 0),
                     "org_typed": sum(1 for s in attr if otype.get(s, "未填") != "未填"),
                     "academicians": len(acad), "academicians_in_master": len(acad & {
                         r[0] for r in C.scholars_all()})},
        "degree": dist(dvals, "value"),
        "position": dist(pvals, "value"),
        "career_band": dist(cvals, "band"),
        "domain": dist(mvals, "domain"),
        "org_type": dist(ovals, "type"),
        "cross": {"degree_x_position": cross(deg, pos),
                  "degree_x_career": cross(deg, {s: band(cy.get(s)) for s in attr}),
                  "domain_x_degree": cross(dom, deg),
                  "orgtype_x_degree": cross(otype, deg)},
        "academician_profile": {
            "n": len(acad),
            "degree": [{"value": k, "n": v} for k, v in sorted(ac_deg.items(), key=lambda kv: (-kv[1], str(kv[0])))],
            "position": [{"value": k, "n": v} for k, v in sorted(ac_pos.items(), key=lambda kv: (-kv[1], str(kv[0])))],
            "domain": [{"value": k, "n": v} for k, v in sorted(ac_dom.items(), key=lambda kv: (-kv[1], str(kv[0])))],
            "org_type": [{"value": k, "n": v} for k, v in sorted(ac_org.items(), key=lambda kv: (-kv[1], str(kv[0])))],
            "caveat": "112 个 id 全部来自 talent_flag；与主档 21,316 交集仅 80，"
                      "院士的机构/论文指标只能在这 80 人上算"},
        "shenzhen": {"attr_scholars": len(sz_attr), "panel_scholars": len(sz_panel),
                     "degree": [{"value": k, "n": v} for k, v in sorted(sz_deg.items(), key=lambda kv: (-kv[1], str(kv[0])))],
                     "note": "两个数分母不同：attr 侧按最晚履历机构判深圳（含库外 id），"
                             "panel 侧按主档机构判深圳；不能相加"},
        "data_quality": {
            "career_not_age": "年龄/出生年整列不可得；从业年限会随「最早一段履历」记录完整度变化，"
                              "不能当年龄用（有人只录了最近一段）",
            "degree_rank": "学历表 43,766 行含多段学位，取最高；医学硕士/工程硕士等专业学位"
                           "统一归「硕士」，不细分",
            "position_rank": "职称只在履历段上有值，36.68% 落在「其他/未填」；"
                            "「高级工程师」按规则归副高，可能与企业职称体系不一致",
            "domain_rule": "十域是关键词规则，全部研究方向拼接后分类；"
                          "多学科交叉者只落一个主域，会低估交叉",
            "org_type": "机构类型按名称 + 高校名录五分类，企业字段只有 74 个机构 81 人",
            "two_universes": "本件全部在 20,030 属性宇宙，不能与 21,316 主档的覆盖率直接比",
        },
        "diff_vs_old_draft": {
            "old": "旧稿写博士 15,754 / 硕士 1,564 / 正高 9,809 / 副高 1,443（分母混杂）",
            "now": f"博士 {dvals.get('博士',0):,} / 硕士 {dvals.get('硕士',0):,} / "
                   f"正高 {pvals.get('正高',0):,} / 副高 {pvals.get('副高',0):,}（分母统一 20,030）",
            "why": "旧稿的分母在 21,316 与 20,030 间切换；本件统一到属性宇宙，并把"
                   "「其他/未填」显式保留，不剔除以抬高占比",
        },
        "findings": [
            f"属性宇宙 {N:,} 人：博士 {dvals.get('博士',0):,}（{C.share(dvals.get('博士',0),N)}%）、"
            f"硕士 {dvals.get('硕士',0):,}（{C.share(dvals.get('硕士',0),N)}%）",
            f"正高 {pvals.get('正高',0):,}（{C.share(pvals.get('正高',0),N)}%），"
            f"「其他/未填」{pvals.get('其他/未填',0):,}（{C.share(pvals.get('其他/未填',0),N)}%）"
            "——职称维是三档里最弱的",
            f"从业 ≥20 年 {cvals.get('≥20 年',0):,} 人、10—20 年 {cvals.get('10—20 年',0):,} 人；"
            f"深圳属性侧 {len(sz_attr)} 人、主档侧 {len(sz_panel)} 人",
        ],
    }
    C.write(METRIC, payload)
    print("N", N, "deg", dvals.most_common(), "pos", pvals.most_common())
    print("career", cvals.most_common())
    print("domain", mvals.most_common())
    print("org", ovals.most_common())
    print("acad", len(acad), sorted(ac_deg.items(), key=lambda kv: (-kv[1], str(kv[0]))), sorted(ac_pos.items(), key=lambda kv: (-kv[1], str(kv[0]))))
    print("sz", len(sz_attr), len(sz_panel), sorted(sz_deg.items(), key=lambda kv: (-kv[1], str(kv[0]))))
    print("cross rows", [(x["row"], x["total"]) for x in payload["cross"]["degree_x_position"]])


if __name__ == "__main__":
    main()
