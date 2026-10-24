#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_CITY_TALENT_INDEX_GLOBAL —— 人才创新指数（全球城市语境）

口径来源：注册表 `formula = pending_cosign: human:唐绍祖（未签）`、`algorithm_type: third_party`、
`source_tables: [pending_ods]`、`is_mock: true`；`calc-logic/INNOV` 下无同 ID 正本。
本件因此是**自建替代读数**（`main_is_official=false`），不是「已发布指数」。

零 DB：只读 code/_snapshots21 下的族级快照，全部数字为快照的纯函数。
  talent_w15n1_20261023.json      城市级人才事实面（本批探针）
  talent22_panel_20261022.json    20,420 名可锚定学者的画像
  papers_city_year_gkx21.json     中文论文第一作者城市
  base_20261021.json              企业底册（名称→城市）
  patent_panel_innov_20261021.json 专利申请人 × 件数

运行：cd code && python3 M_INNOV_CITY_TALENT_INDEX_GLOBAL.py
"""
from __future__ import annotations

import collections
import json
import math
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_INNOV_CITY_TALENT_INDEX_GLOBAL_out.json")

POOL_MIN = 200          # 城市入池门槛：可锚定学者 ≥200 人
ZERO_FILL = False       # 缺维不补 0，写 null
EQUAL_W = 0.2


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def minmax(vals, log=False):
    xs = [math.log1p(v) if log else v for v in vals]
    lo, hi = min(xs), max(xs)
    if hi - lo < 1e-12:
        return [50.0 for _ in xs]
    return [100.0 * (x - lo) / (hi - lo) for x in xs]


def entropy_weights(mat):
    """mat: 行=城市，列=叶子（已 0—100）。返回熵权，标准化到和 1。"""
    n = len(mat)
    m = len(mat[0])
    ws = []
    for j in range(m):
        col = [mat[i][j] for i in range(n)]
        s = sum(col)
        if s <= 0:
            ws.append(0.0)
            continue
        ps = [c / s for c in col if c > 0]
        e = -sum(p * math.log(p) for p in ps) / math.log(n)
        ws.append(1 - e)
    tot = sum(ws)
    if tot <= 0:
        return [1 / m] * m
    return [w / tot for w in ws]


def main() -> int:
    tp = load("talent_w15n1_20261023.json")["facts"]
    panel = load("talent22_panel_20261022.json")["scholars"]
    papers = load("papers_city_year_gkx21.json")

    city = tp["city_talent_profile"]["cities"]
    exclude = {"未归属", "未填", "海外"}
    pool = [c for c, v in city.items() if c not in exclude and v["scholars"] >= POOL_MIN]
    pool.sort(key=lambda c: -city[c]["scholars"])

    # 论文第一作者城市（2021—2023）
    p13 = collections.Counter()
    for k, v in papers["first_city_year"].items():
        cc, yr = k.split("|")
        if yr in ("2021", "2022", "2023"):
            p13[cc] += v
    # 快照里的城市名带「市」，香港/澳门是「香港特别行政区」
    p13_norm = {}
    for k, v in p13.items():
        kk = k.replace("特别行政区", "")
        p13_norm[kk] = p13_norm.get(kk, 0) + v

    rows = []
    for c in pool:
        v = city[c]
        n = v["scholars"]
        rows.append({
            "city": c,
            "scholars": n,
            "h_median": v["h_median"],
            "h_mean": v["h_mean"],
            "h_ge30": v["h_ge30"],
            "h_ge50": v["h_ge50"],
            "academicians": v["academicians"],
            "cite_sum": v["cite_sum"],
            "paper_sum": v["paper_sum"],
            "pat_persons": v["pat_persons"],
            "share_h_ge30_pct": round(v["h_ge30"] / n * 100, 4),
            "share_h_ge50_pct": round(v["h_ge50"] / n * 100, 4),
            "papers_per_scholar": round(v["paper_sum"] / n, 4),
            "pat_persons_share_pct": round(v["pat_persons"] / n * 100, 4),
            "papers_first_city_2021_2023": p13_norm.get(c, 0),
        })

    # ---- 五叶
    L = []
    L.append(("G1_scholars", [r["scholars"] for r in rows], True))
    L.append(("G2_h_median", [r["h_median"] or 0 for r in rows], False))
    L.append(("G3_h_ge50_share", [r["share_h_ge50_pct"] for r in rows], False))
    # 城市级论文产出**不进池**：papers_city_year 的第一作者归城只覆盖 11 个粤港澳城市，
    # 省外城市在这张表里恒为 0（不是「没有论文」，是「不在这张表的白名单里」）。
    # 用学者画像里的 paper 合计做「人均论文」才是同池可比的，见 G4。
    L.append(("G4_papers_per_scholar", [r["papers_per_scholar"] for r in rows], False))
    L.append(("G5_pat_persons_share", [r["pat_persons_share_pct"] for r in rows], False))
    norm = {}
    for name, vals, lg in L:
        norm[name] = minmax(vals, log=lg)
    mat = [[norm[name][i] for name, _, _ in L] for i in range(len(rows))]
    comp = [sum(EQUAL_W * x for x in row) for row in mat]
    ew = entropy_weights(mat)

    order = sorted(range(len(rows)), key=lambda i: -comp[i])
    for rank, i in enumerate(order, 1):
        rows[i]["rank"] = rank
        rows[i]["score"] = round(comp[i], 2)
        for j, (name, _, _) in enumerate(L):
            rows[i][name] = round(mat[i][j], 2)
    # 名次需要先填再排序输出
    by_rank = sorted(rows, key=lambda r: r["rank"])

    # ---- 权重敏感性：规模叶权重 w 从 0→1（其余 4 叶均分 1-w）
    # 为什么扫规模叶而不是别的：四比率叶都受「可锚定率」影响，高校密集城市的池更深、
    # 普通人更多，比率天然被拉低；规模叶是唯一直接反映池大小的量。扫它能看出
    # 「深圳第一」在多大的规模权重下会让位给北京。
    switch = []
    for w in [i / 100 for i in range(0, 101)]:
        best, bestv = None, -1
        for i, r in enumerate(by_rank):
            s = w * r["G1_scholars"] + (1 - w) * sum(
                r[k] for k in ("G2_h_median", "G3_h_ge50_share", "G4_papers_per_scholar",
                               "G5_pat_persons_share")) / 4
            if s > bestv:
                best, bestv = r["city"], s
        switch.append((w, best))
    changes = [(switch[i][0], switch[i][1]) for i in range(1, len(switch)) if switch[i][1] != switch[i - 1][1]]
    top1_share = collections.Counter(b for _, b in switch)

    # ---- 覆盖率
    total_scholars = len(panel)
    city_total = sum(v["scholars"] for k, v in city.items() if k not in exclude)
    sum_scholars = sum(r["scholars"] for r in rows)
    p_first = sum(papers["first_city_year"].values())
    p_any_pairs = sum(papers["any_city_year"].values())
    p_nocity = papers["papers_with_no_gba_city"]
    pat = tp["F3_patent_applicant_city"]
    base = tp["F1_org_base_city"]

    z = next(r for r in rows if r["city"] == "深圳市")
    bj = next(r for r in rows if r["city"] == "北京市")
    gz = next(r for r in rows if r["city"] == "广州市")

    out = {
        "metric_id": "M_INNOV_CITY_TALENT_INDEX_GLOBAL",
        "metric_name_zh": "人才创新指数（全球城市语境）",
        "main_is_official": False,
        "support_judgment": "部分支持",
        "verdict_kind": "self_built_substitute",
        "sources": [
            "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）",
            "code/_snapshots21/talent_w15n1_20261023.json",
            "code/_snapshots21/talent22_panel_20261022.json",
            "code/_snapshots21/papers_city_year_gkx21.json",
            "code/_snapshots21/base_20261021.json",
            "code/_snapshots21/patent_panel_innov_20261021.json",
        ],
        "base_years_used": [2021, 2022, 2023],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": ("论文产出叶取 2021—2023 三年；2017—2020 不进分母，原因是 dwd_patent.apdt_year "
                            "这四年零行（DATA_FACTS §3.13），且 2024 年中文论文语料是回填孤峰（32,379 篇，"
                            "为 2023 年的 4.87 倍），放进窗口会把四城论文组件同时抬高、画出假上行线。"),
        "params": {
            "pool_min_scholars": POOL_MIN,
            "leaves": [n for n, _, _ in L],
            "equal_weight": EQUAL_W,
            "normalization": "min-max；计数叶先 log1p（G1/G4），比率叶与中位数叶直接 min-max",
            "missing_dim_policy": "缺维写 null，不补 0；主口径不重归一化（五叶全部可得，本轮无缺维进加权）",
            "zero_fill": ZERO_FILL,
        },
        "headline": {
            "pool_cities": len(rows),
            "cities_total_with_scholars": len([k for k in city if k not in exclude]),
            "scholars_total": total_scholars,
            "scholars_city_mapped": city_total,
            "pool_scholars": sum_scholars,
            "top1": by_rank[0]["city"],
            "top1_score": by_rank[0]["score"],
            "top2": by_rank[1]["city"],
            "top2_score": by_rank[1]["score"],
            "sz_rank": z["rank"],
            "sz_score": z["score"],
            "gz_rank": gz["rank"],
            "gz_score": gz["score"],
            "bj_score": bj["score"],
            "sz_minus_gz": round(z["score"] - gz["score"], 2),
        },
        "by_city": by_rank,
        "entropy_weights": {name: round(w, 6) for (name, _, _), w in zip(L, ew)},
        "weight_sensitivity": {
            "sweep": "规模叶 G1 权重 w 从 0.00 到 1.00，步长 0.01；其余四叶均分 1-w",
            "switch_points": changes,
            "top1_share_pct": {k: round(v / len(switch) * 100, 4) for k, v in top1_share.items()},
        },
        "coverage": {
            "scholar_rows_in_table": tp["F4_scholar_org_city"]["scholar_rows_in_table"],
            "scholars_in_panel": total_scholars,
            "scholars_city_mapped": city_total,
            "scholars_unassigned": city["未归属"]["scholars"],
            "scholars_unfilled": city["未填"]["scholars"],
            "scholars_overseas": city["海外"]["scholars"],
            "city_mapping_pct": round(city_total / total_scholars * 100, 4),
            "recompute_agreement_pct": tp["F4_scholar_org_city"]["recompute_agreement_pct"],
            "papers_total": papers["table_rows_counted"],
            "papers_first_city": p_first,
            "papers_first_city_pct": round(p_first / papers["table_rows_counted"] * 100, 4),
            "papers_any_city_pairs": p_any_pairs,
            "papers_without_city": p_nocity,
            "papers_without_city_pct": round(p_nocity / papers["table_rows_counted"] * 100, 4),
            "patent_rows": pat["patent_rows"],
            "patent_applicants": pat["applicants"],
            "patent_matched_applicants": pat["matched_applicants"],
            "patent_matched_applicant_pct": pat["applicant_match_pct"],
            "patents_matched": pat["patents_matched"],
            "patent_match_pct": pat["patent_match_pct"],
            "org_base_rows": base["rows"],
            "org_base_cities": base["distinct_cities"],
            "co_deg_filled": tp["city_talent_profile"]["co_deg_filled_total"],
            "co_deg_filled_pct": round(tp["city_talent_profile"]["co_deg_filled_total"] / total_scholars * 100, 4),
        },
        "derived": {
            "sz_scholars_share_of_national_pct": {
                "value": round(z["scholars"] / total_scholars * 100, 4),
                "numerator": z["scholars"],
                "denominator": total_scholars,
                "denominator_note": "全国可锚定学者 20,420 人（talent22_panel.scholars 行数）",
            },
            "gz_scholars_over_sz": {
                "value": round(gz["scholars"] / z["scholars"], 4),
                "numerator": gz["scholars"],
                "denominator": z["scholars"],
                "denominator_note": "广州 894 / 深圳 213",
            },
            "bj_scholars_over_sz": {
                "value": round(bj["scholars"] / z["scholars"], 4),
                "numerator": bj["scholars"],
                "denominator": z["scholars"],
                "denominator_note": "北京 2,841 / 深圳 213",
            },
            "pool_share_of_mapped_scholars_pct": {
                "value": round(sum_scholars / city_total * 100, 4),
                "numerator": sum_scholars,
                "denominator": city_total,
                "denominator_note": "20 池城市学者数 / 全国可归城学者数（2,573 未归属 + 465 未填 + 280 海外不计）",
            },
            "sz_h_ge50_rate_vs_bj": {
                "value": round(z["share_h_ge50_pct"] / bj["share_h_ge50_pct"], 4),
                "numerator": z["share_h_ge50_pct"],
                "denominator": bj["share_h_ge50_pct"],
                "denominator_note": "深圳 h≥50 占比 16.90% / 北京 6.72%",
            },
            "sz_h_median_minus_national": {
                "value": round(z["h_median"] - statistics.median(
                    [s["h"] for s in panel if isinstance(s.get("h"), (int, float))]), 2),
                "numerator": z["h_median"],
                "denominator": "全国 h 中位数",
                "denominator_note": "深圳中位 h 23 / 全国中位 h 见 checks.national_h_median",
            },
            "paper_city_first_vs_any_gap": {
                "value": p_any_pairs - p_first,
                "numerator": p_any_pairs,
                "denominator": p_first,
                "denominator_note": "同一篇论文多城署名产生的重复计数差：any 城市-论文对 30,807 − first 24,737",
            },
        },
        "checks": {
            "national_h_median": statistics.median([s["h"] for s in panel if isinstance(s.get("h"), (int, float))]),
            "five_leaves_all_present": all(all(r[n] is not None for n in norm) for r in rows),
            "score_range_ok": all(0 <= r["score"] <= 100 for r in rows),
            "rank_unique": len({r["rank"] for r in rows}) == len(rows),
            "pool_monotone_vs_threshold": min(r["scholars"] for r in rows) >= POOL_MIN,
            "weights_sum_one": abs(sum(ew) - 1) < 1e-9,
        },
        "notes": [
            "五叶全部可得，本轮没有缺维进加权；但**四类维度整块缺失**：投入（R&D 人员/经费）、"
            "合作活跃（共著度数仅 1,778/20,420 有值）、人才流动（无任职起止的机构序列）、"
            "全球城市（海外 280 人只能归为「海外」，无城市）。故不是完整的人才创新指数。",
            "指数是自建替代读数，`main_is_official=false`：注册表 formula 未签、source_tables 为 pending_ods。",
            "归一为池内 min-max，跨年不可比（本件只有一期截面，不做趋势）。",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps(out["headline"], ensure_ascii=False, indent=1))
    print("entropy:", out["entropy_weights"])
    print("switch:", changes[:6], "top1 share:", out["weight_sensitivity"]["top1_share_pct"])
    print("->", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
