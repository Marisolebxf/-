#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_FLOW_TRACK —— 人才流动轨迹（SRS 78/79/80）。

口径：
  段 = `dwd_scholar_work_experience` 一行（机构 + 起年 + 止年，止年空按 2026）；
  一次「流动」= 同一 scholar_id 相邻两段，机构串不同，且后段起年 ≥ 前段止年
  （允许同年衔接）；同机构相邻段记「内部晋升/续聘」，不计流动。
  城际流动只统计两端都能定位且城市不同的记录；分母单列。
零 SQL；产物 code/M_TALENT_FLOW_TRACK_out.json。
"""
from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import _talent10_common as C  # noqa: E402

METRIC = "M_TALENT_FLOW_TRACK"
NOW = 2026


def main() -> None:
    W = C.work()
    by = defaultdict(list)
    for w in W:
        o = (w["org"] or "").strip()
        y0 = w["y0"]
        if not o or not y0:
            continue
        by[w["sid"]].append((int(y0), int(w["y1"] or NOW), o, w["pos"] or "", bool(w["cur"])))

    multi = {s: v for s, v in by.items() if len(v) >= 2}
    trans = []      # (sid, y, org_from, org_to, city_from, city_to, dom)
    internal = 0
    dropped_overlap = 0
    p = C.panel()["scholars"]
    dom_of = {r["sid"]: (r["cl"][0] if r["cl"] else "未标注") for r in p}
    for sid, segs in multi.items():
        segs = sorted(segs)
        for a, b in zip(segs, segs[1:]):
            if b[0] < a[1]:
                dropped_overlap += 1
                continue
            if a[2] == b[2]:
                internal += 1
                continue
            ca = C.loc2(a[2])[1]
            cb = C.loc2(b[2])[1]
            trans.append((sid, b[0], a[2], b[2], ca, cb, dom_of.get(sid, "未标注")))

    n_from = len({t[0] for t in trans})
    both_located = [t for t in trans if "未" not in t[4] and "未" not in t[5]]
    unassigned_org = Counter(o for t in trans for o in (t[2], t[3]) if "未" in C.loc2(o)[1])
    city_tr = [t for t in trans if t[4] not in ("未归属", "未填")
               and t[5] not in ("未归属", "未填") and t[4] != t[5]]
    year = Counter(t[1] for t in trans if 1990 <= t[1] <= NOW)
    city_edges = Counter((t[4], t[5]) for t in city_tr)
    org_edges = Counter((t[2], t[3]) for t in trans)
    dom_edges = defaultdict(lambda: [0, 0])
    for t in trans:
        dom_edges[t[6]][1 if t[5] == "深圳市" else 0] += 1

    sz_in = [t for t in trans if t[5] == "深圳市" and t[4] != "深圳市"]
    sz_out = [t for t in trans if t[4] == "深圳市" and t[5] != "深圳市"]
    sz_in_by_city = Counter(t[4] for t in sz_in)
    sz_out_by_city = Counter(t[5] for t in sz_out)  # 目的地城市
    sz_dom = Counter(t[6] for t in sz_in)

    def pairs(cnt, k=15):
        return [{"from": a, "to": b, "n": n} for (a, b), n in cnt.most_common(k)]

    top_orgs = [o for o, _ in Counter(t[2] for t in trans).most_common(12)]
    org_matrix = []
    for a in top_orgs:
        for b in top_orgs:
            if a != b and org_edges.get((a, b)):
                org_matrix.append({"from": a, "to": b, "n": org_edges[(a, b)]})

    payload = {
        "support_judgment": "部分支持",
        "base_years_used": [1990, 2026],
        "base_years_missing": [2021, 2022, 2023],
        "base_years_note": "履历起止年覆盖 1950s—2026，但招聘/流动的宏观基期（2021—2023 三年"
                           "对比）没有同期快照；本件只做「全历史轨迹」一张截面，不做逐年净流入率。"
                           "「止年空」一律按 2026（当前）处理，会低估 2026 年之后的流出",
        "scope": {"universe": "dwd_scholar_work_experience 57,117 行",
                  "unit": "一次机构变更（相邻两段）",
                  "denominator_movers": n_from,
                  "denominator_transitions": len(trans),
                  "denominator_city": len(city_tr)},
        "coverage": {"work_rows": len(C.work()), "scholars_with_work": len(by),
                     "scholars_multi_segment": len(multi),
                     "movers": n_from, "transitions": len(trans),
                     "internal_moves": internal, "overlap_dropped": dropped_overlap,
                     "city_transitions": len(city_tr),
                     "city_share": C.share(len(city_tr), len(trans)),
                     "year_min": min(year) if year else None,
                     "year_max": max(year) if year else None,
                     "org_filled_pct": round(100.0 * sum(1 for w in W if (w["org"] or "").strip()) / len(W), 2),
                     "start_filled_pct": round(100.0 * sum(1 for w in W if w["y0"]) / len(W), 2),
                     "end_filled_pct": round(100.0 * sum(1 for w in W if w["y1"]) / len(W), 2),
                     "position_filled_pct": round(100.0 * sum(1 for w in W if (w["pos"] or "").strip()) / len(W), 2),
                     "seg_city_unassigned": len(trans) - len(both_located),
                     "trans_both_located": len(both_located)},
        "year_series": [{"year": y, "n": n} for y, n in sorted(year.items())],
        "org_edges": pairs(org_edges, 25),
        "org_matrix_top12": org_matrix,
        "city_edges": pairs(city_edges, 25),
        "unassigned_org_top": [{"org": o, "n": n} for o, n in unassigned_org.most_common(10)],
        "shenzhen": {"inflow": len(sz_in), "outflow": len(sz_out),
                     "net": len(sz_in) - len(sz_out),
                     "in_by_city": [{"city": k, "n": v} for k, v in sz_in_by_city.most_common(12)],
                     "out_by_city": [{"city": k, "n": v} for k, v in sz_out_by_city.most_common(12)],
                     "in_by_domain": [{"domain": k, "n": v} for k, v in sz_dom.most_common()],
                     "note": "深圳口径 = loc2 判定的深圳市机构；分支校区已修正"},
        "domain_flows": [{"domain": d, "n": sum(v), "to_sz": v[1]}
                         for d, v in sorted(dom_edges.items(), key=lambda x: -sum(x[1]))],
        "data_quality": {
            "overlap": f"{dropped_overlap} 对相邻段时间重叠（后段起年早于前段止年），已丢弃，"
                       "多数是同一单位多岗位/兼职并行",
            "same_org": f"{internal} 对同机构相邻段计入内部晋升，不计流动",
            "no_reason": "库内无离职原因/去向类型字段，流动只有「机构→机构」，无法区分主动跳槽与调动",
            "no_salary": "无薪酬字段，流动的「拉力」不可量化",
            "right_censor": "在职（cur=1）者止年按 2026 计，未来流出未知",
        },
        "diff_vs_old_draft": {
            "old": "旧稿 9,281 人可追踪、18,713 次机构变更、1,149 次城际迁移、深圳净流入 +19",
            "now": f"{len(multi):,} 人有 ≥2 段、{len(trans):,} 次机构变更、"
                   f"{len(city_tr):,} 次城际迁移、深圳净流入 {len(sz_in)-len(sz_out):+d}",
            "why": "同一份履历快照，差异来自两处：①本件要求「后段起年 ≥ 前段止年」，丢弃重叠段；"
                   "②城际只算两端均可定位者。旧稿把未归属当同城处理，因此城际次数偏高",
        },
        "findings": [
            f"{len(multi):,} 人有 2 段及以上履历，其中 {n_from:,} 人至少换过一次机构，"
            f"共 {len(trans):,} 次变更（人均 {round(len(trans)/n_from, 2)} 次）",
            f"城际迁移 {len(city_tr):,} 次（占全部变更 {C.share(len(city_tr), len(trans))}%），"
            f"深圳流入 {len(sz_in)} / 流出 {len(sz_out)} / 净 {len(sz_in)-len(sz_out):+d}",
            f"最大流向：{city_edges.most_common(1)[0][0][0]} → {city_edges.most_common(1)[0][0][1]}"
            f"（{city_edges.most_common(1)[0][1]} 次）",
        ],
    }
    C.write(METRIC, payload)
    print("coverage", payload["coverage"])
    print("sz", payload["shenzhen"]["inflow"], payload["shenzhen"]["outflow"])
    print("city top", payload["city_edges"][:5])
    print("org top", payload["org_edges"][:5])
    print("years", payload["year_series"][-6:])


if __name__ == "__main__":
    main()
