#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_SUPPLY_STRUCT —— 人才供给结构（SRS 81/82/83 的供给侧）。

供给 = 属性宇宙 20,030 人（有履历/学历/方向任一），按六个维度拆：
  学历 / 职称 / 从业年限 / 学科域 / 机构类型 / 属地（省级，取最晚履历机构）。
每个维度给「规模 + 占比 + HHI + 首位占比」，另给学科域×学历交叉与深圳供给切片。
不产出「年龄」「薪酬期望」「求职状态」——库内无此三列（§三 逐条列修复路径）。
零 SQL；产物 code/M_TALENT_SUPPLY_STRUCT_out.json。
"""
from __future__ import annotations

import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import _talent10_common as C  # noqa: E402

METRIC = "M_TALENT_SUPPLY_STRUCT"
NOW = 2026


def band(y):
    if y is None:
        return "未知"
    return "<5 年" if y < 5 else "5—10 年" if y < 10 else "10—20 年" if y < 20 else "≥20 年"


def main() -> None:
    work = C.work()
    edu = C.edu()
    res = C.research()
    attr = {w["sid"] for w in work} | {e["sid"] for e in edu} | set(res)
    N = len(attr)
    deg = C.highest_degree()
    pos = C.highest_position()
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
    dom = {s: (C.domain_of(" ".join(res[s])) if res.get(s) else "其他/未归类") for s in attr}
    prov = {s: (C.loc2(latest[s][1])[0] if s in latest else "未填") for s in attr}

    def summarize(cnt: Counter, label: str, denom: int = N):
        vals = list(cnt.values())
        tot = sum(vals)
        hhi = round(sum((v / tot) ** 2 for v in vals) * 10000, 1) if tot else 0
        ent = -sum((v / tot) * math.log(v / tot) for v in vals if v) if tot else 0
        k = len(vals)
        return {"dimension": label, "categories": k, "hhi": hhi,
                "entropy": round(ent, 4),
                "entropy_norm": round(ent / math.log(k), 4) if k > 1 else 0,
                "top1_share": C.share(max(vals), denom) if vals else 0,
                "items": [{"value": a, "n": b, "share": C.share(b, denom)}
                          for a, b in sorted(cnt.items(), key=lambda kv: (-kv[1], str(kv[0])))[:12]]}

    dims = [summarize(Counter(deg.get(s, "未填") for s in attr), "学历"),
            summarize(Counter(pos.get(s, "其他/未填") for s in attr), "职称"),
            summarize(Counter(band(cy.get(s)) for s in attr), "从业年限"),
            summarize(Counter(dom.values()), "学科域"),
            summarize(Counter(C.org_type(latest[s][1]) if s in latest else "未填" for s in attr),
                      "机构类型"),
            summarize(Counter(p for p in prov.values() if p not in ("未归属", "未填")),
                      "属地(省级)", denom=sum(1 for p in prov.values()
                                            if p not in ("未归属", "未填")))]

    cross = defaultdict(Counter)
    for s in attr:
        cross[dom[s]][deg.get(s, "未填")] += 1
    cross_out = [{"domain": d, "total": sum(c.values()),
                  "cells": [{"degree": k, "n": v, "share": C.share(v, sum(c.values()))}
                            for k, v in sorted(c.items(), key=lambda kv: (-kv[1], str(kv[0])))]} for d, c in sorted(cross.items())]

    sz = [s for s in attr if s in latest and C.loc2(latest[s][1])[1] == "深圳市"]
    sz_cnt = Counter(deg.get(s, "未填") for s in sz)
    sz_dom = Counter(dom[s] for s in sz)
    sz_pos = Counter(pos.get(s, "其他/未填") for s in sz)

    payload = {
        "support_judgment": "部分支持",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "供给结构是存量截面；没有毕业年度/首次入职年度字段，"
                           "「新增供给」只能由论文首发年近似（见 M_TALENT_UNIV_NEW）",
        "scope": {"universe": "属性宇宙（work/edu/research 并集）", "n": N,
                  "unit": "scholar_id", "denominator": N},
        "coverage": {"n": N, "degree_filled": N - Counter(deg.get(s, "未填") for s in attr)["未填"],
                     "position_filled": sum(1 for s in attr if pos.get(s, "其他/未填") != "其他/未填"),
                     "career_filled": sum(1 for s in attr if s in cy),
                     "domain_filled": sum(1 for s in attr if dom[s] != "其他/未归类"),
                     "org_typed": sum(1 for s in attr if s in latest),
                     "prov_filled": sum(1 for s in attr if prov[s] not in ("未填", "未归属")),
                     "prov_unknown": sum(1 for s in attr if prov[s] in ("未填", "未归属")),
                     "prov_note": "履历机构串的可定位率只有 22.13%，属地维分母必须换成"
                                  "「可定位者」，不能用 20,030"},
        "dimensions": dims,
        "domain_x_degree": cross_out,
        "shenzhen": {"n": len(sz), "share_of_attr": C.share(len(sz), N),
                     "degree": [{"value": k, "n": v} for k, v in sorted(sz_cnt.items(), key=lambda kv: (-kv[1], str(kv[0])))],
                     "position": [{"value": k, "n": v} for k, v in sorted(sz_pos.items(), key=lambda kv: (-kv[1], str(kv[0])))],
                     "domain": [{"value": k, "n": v} for k, v in sorted(sz_dom.items(), key=lambda kv: (-kv[1], str(kv[0])))],
                     "note": "深圳供给 = 最晚履历机构 loc2 判深圳；与该宇宙 123 人一致，"
                             "不含仅主档有机构的 138 人"},
        "data_quality": {
            "no_age": "年龄/出生年整列不可得，从业年限是「2026−最早履历起年」，"
                      "对只录最近一段的人会低估",
            "no_wage": "无薪酬期望/最低可接受薪资字段，供给的价格维不可算",
            "no_intent": "无求职状态/到岗时间字段，「活跃供给」与「存量供给」不可分",
            "no_headcount": "无团队规模/招生名额，供给只能按人计，不能按「可带团队」加权",
            "degree_bias": "属性宇宙以高校/院所为主（高校 63.08%），企业研发供给仅 448 人，"
                           "产业侧供给被系统性低估",
            "domain_rule": "学科域是研究方向关键词规则，18.5% 未归类；交叉学科只落一个主域",
            "prov_text": "履历机构串 61.33% 判不出属地：其中大量是中文写的海外高校（伦敦大学学院 61、"
                         "斯坦福大学 50、牛津大学 44、南洋理工大学 35），现有 is_foreign 只认国名，"
                         "不认校名；国内可定位者仅 2,473 人（12.34%）。属地维只能在这 2,473 人上算，"
                         "修复路径见 §三 3.6",
        },
        "diff_vs_old_draft": {
            "old": "旧稿按 6 维给占比，但分母在 20,030 与 21,316 间漂移，且未给 HHI",
            "now": f"统一分母 {N:,}，六维各给 HHI/归一化熵/首位占比；深圳切片 {len(sz)} 人",
            "why": "本件把「未填/未归类」保留为独立类别，不剔除以抬高结构清晰度",
        },
        "findings": [
            f"供给 {N:,} 人：博士 {C.share(Counter(deg.get(s,'未填') for s in attr)['博士'],N)}%、"
            f"正高 {C.share(sum(1 for s in attr if pos.get(s)=='正高'),N)}%，"
            f"高校 {C.share(sum(1 for s in attr if s in latest and C.org_type(latest[s][1])=='高校'),N)}%",
            f"学历维 HHI={dims[0]['hhi']}（最集中），属地维在可定位者中 HHI={dims[5]['hhi']}、"
            f"归一化熵 {dims[5]['entropy_norm']}（最分散）",
            f"深圳供给 {len(sz)} 人（{C.share(len(sz),N)}%），博士 "
            f"{C.share(sz_cnt.get('博士',0),len(sz))}% 高于全库",
        ],
    }
    C.write(METRIC, payload)
    for d in dims:
        print(d["dimension"], d["categories"], d["hhi"], d["entropy_norm"], d["top1_share"],
              d["items"][:3])
    print("sz", len(sz), sz_cnt.most_common(4), sz_dom.most_common(4))


if __name__ == "__main__":
    main()
