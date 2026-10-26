#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_GRAPH_110_1 —— 人才实体图谱（SRS 69/70/71 的图谱侧）。

两个宇宙必须分开报，禁止交叉相除：
  A 身份宇宙 = `dwd_scholar` 21,316 行（姓名/机构/ORCID）；
  B 属性宇宙 = talent_flag / work_experience / education_background / research_direction
    的 scholar_id 去重 20,030 人（学位/职称/方向/履历）；
  A∩B = 1,858 人（占 A 8.72%、占 B 9.28%）。七维齐全只能在交集内计算。
零 SQL；产物 code/M_TALENT_GRAPH_110_1_out.json。
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import _talent10_common as C  # noqa: E402

METRIC = "M_TALENT_GRAPH_110_1"
NOW = 2026


def career_years() -> dict[str, int]:
    d: dict[str, int] = {}
    for w in C.work():
        y = w["y0"]
        if not y or y < 1950:
            continue
        d[w["sid"]] = min(d.get(w["sid"], 9999), int(y))
    return {s: NOW - y for s, y in d.items()}


def band(y: int | None) -> str:
    if y is None:
        return "未知"
    if y < 5:
        return "<5 年"
    if y < 10:
        return "5—10 年"
    if y < 20:
        return "10—20 年"
    return "≥20 年"


def main() -> None:
    allrows = C.scholars_all()
    master = len(allrows)
    orcid = {r[0]: r[1] for r in C.load("scholar_fill_20261022.json")["rows"]}
    deg = C.highest_degree()
    pos = C.highest_position()
    res = C.research()
    cy = career_years()
    work_sids = {w["sid"] for w in C.work()}
    edu_sids = {e["sid"] for e in C.edu()}
    attr = work_sids | edu_sids | set(res)
    inter = attr & {r[0] for r in allrows}
    dom = {s: (C.domain_of(" ".join(res[s])) if res.get(s) else "其他/未归类")
           for s in attr}

    ident = {
        "姓名": sum(1 for r in allrows if (r[1] or "").strip()),
        "机构": sum(1 for r in allrows if (r[2] or "").strip()),
        "ORCID": sum(1 for r in allrows if orcid.get(r[0])),
    }
    attr_dims = {
        "学位": sum(1 for s in attr if deg.get(s, "未填") != "未填"),
        "职称": sum(1 for s in attr if pos.get(s, "其他/未填") != "其他/未填"),
        "研究方向": sum(1 for s in attr if res.get(s)),
        "从业年限": sum(1 for s in attr if s in cy),
    }
    hook = {
        "姓名": lambda r: bool((r[1] or "").strip()),
        "机构": lambda r: bool((r[2] or "").strip()),
        "ORCID": lambda r: bool(orcid.get(r[0])),
        "学位": lambda r: deg.get(r[0], "未填") != "未填",
        "职称": lambda r: pos.get(r[0], "其他/未填") != "其他/未填",
        "研究方向": lambda r: bool(res.get(r[0])),
        "从业年限": lambda r: r[0] in cy,
    }
    inter_rows = [r for r in allrows if r[0] in inter]
    complete = [r for r in inter_rows if all(f(r) for f in hook.values())]
    inter_fill = {k: sum(1 for r in inter_rows if f(r)) for k, f in hook.items()}
    ident_only = sum(1 for r in allrows if all(hook[k](r) for k in ("姓名", "机构", "ORCID")))

    def dist(cnt, key, denom):
        return [{key: k, "n": v, "share": C.share(v, denom)} for k, v in cnt.most_common()]

    sz = [r for r in allrows if C.is_sz_org(r[2] or "")]
    sz_inter = [r for r in sz if r[0] in inter]
    sz_complete = [r for r in sz_inter if all(f(r) for f in hook.values())]

    payload = {
        "support_judgment": "部分支持",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "实体快照，无时间序列；属性维没有年度切片，无法做「图谱增长」曲线",
        "scope": {"master_universe": master, "attr_universe": len(attr),
                  "intersection": len(inter),
                  "intersection_share_master": C.share(len(inter), master),
                  "intersection_share_attr": C.share(len(inter), len(attr)),
                  "unit": "scholar_id", "edges": ["人—机构", "人—ORCID"]},
        "identity_dims": [{"dim": k, "n": v, "share": C.share(v, master), "missing": master - v}
                          for k, v in ident.items()],
        "attr_dims": [{"dim": k, "n": v, "share": C.share(v, len(attr)),
                       "missing": len(attr) - v} for k, v in attr_dims.items()],
        "intersection": {"n": len(inter), "fill": [
            {"dim": k, "n": v, "share": C.share(v, len(inter))} for k, v in inter_fill.items()],
            "complete_7dim": len(complete),
            "complete_share_intersection": C.share(len(complete), len(inter)),
            "complete_share_master": C.share(len(complete), master)},
        "graph": {"entities": master, "org_nodes": len({(r[2] or "").strip()
                                                        for r in allrows if (r[2] or "").strip()}),
                  "person_org_edges": ident["机构"], "person_orcid_edges": ident["ORCID"],
                  "identity_complete": ident_only,
                  "identity_complete_share": C.share(ident_only, master),
                  "orcid_distinct": len({v for v in orcid.values() if v}),
                  "orcid_dup_values": sum(1 for _, n in Counter(
                      v for v in orcid.values() if v).items() if n > 1),
                  "dup_names": sum(1 for _, n in Counter(
                      (r[1] or "").strip() for r in allrows
                      if (r[1] or "").strip()).items() if n > 1)},
        "degree_dist": dist(Counter(deg.get(s, "未填") for s in attr), "value", len(attr)),
        "position_dist": dist(Counter(pos.get(s, "其他/未填") for s in attr), "value", len(attr)),
        "career_band": dist(Counter(band(cy.get(s)) for s in attr), "band", len(attr)),
        "domain_dist": dist(Counter(dom[s] for s in attr), "domain", len(attr)),
        "shenzhen": {"entities": len(sz), "in_intersection": len(sz_inter),
                     "complete_7dim": len(sz_complete),
                     "complete_share": C.share(len(sz_complete), len(sz_inter)),
                     "note": "深圳实体按机构名判定（含分支校区修正）；属性维只覆盖交集里的 "
                             f"{len(sz_inter)} 人"},
        "data_quality": {
            "two_universes": "A∩B 仅 1,858 人（8.72%），学位/职称/方向/履历在 A 中几乎整列为空；"
                             "本件所有属性维分母固定为 20,030，不与 21,316 相除",
            "orcid_dup": "20,255 条 ORCID 中有 2 个值被多人共用，图谱建边前需人工复核",
            "name_dup": "1,005 个姓名串重复，姓名不能当实体主键，只能用 scholar_id",
            "org_id": "dwd_scholar.scholar_org_id 全空，机构节点按名称串建、无主键，别名未合并",
            "no_age": "年龄/出生年整列不可得；从业年限=2026−最早履历起年，只覆盖 14,832 人，"
                      "且无法区分「求学期间实习」",
        },
        "findings": [
            f"A 宇宙 21,316 人，身份三维（姓名+机构+ORCID）同时有值 {ident_only:,} 人"
            f"（{C.share(ident_only, master)}%）；B 宇宙 {len(attr):,} 人，学位覆盖"
            f"{C.share(attr_dims['学位'], len(attr))}%、职称仅 "
            f"{C.share(attr_dims['职称'], len(attr))}%",
            f"交集 {len(inter):,} 人里七维齐全 {len(complete):,} 人"
            f"（{C.share(len(complete), len(inter))}%），放到 A 宇宙只有 "
            f"{C.share(len(complete), master)}%",
            f"深圳实体 {len(sz)} 人，交集内 {len(sz_inter)} 人，七维齐全仅 {len(sz_complete)} 人",
        ],
    }
    C.write(METRIC, payload)
    print("ident", ident, "attr", attr_dims, "inter", len(inter))
    print("complete", len(complete), C.share(len(complete), len(inter)))
    print("deg", payload["degree_dist"][:5])
    print("pos", payload["position_dist"])
    print("cy", payload["career_band"])
    print("sz", len(sz), len(sz_inter), len(sz_complete))
    print("graph", payload["graph"])


if __name__ == "__main__":
    main()
