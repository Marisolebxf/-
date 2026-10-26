#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""专利影响力（M_INNOV_PATENT_INFLUENCE）——A-22 批复现脚本。

口径来源：metrics/calc-logic/INNOV/M_INNOV_PATENT_INFLUENCE.md（王惠，seed v1）
  「以被引次数为主、专利价值为辅，取值 0—100；二维 0.80/0.20，缺测维重归一。」
  D1 被引次数：dwd_patent_cited.cited_by_nums（**被他引**，不是本专利参考文献数）
  D2 专利价值：dwd_patent.value

取数约束（派单书 v5）：专利数字一条 SQL 都不发。本脚本**零 SQL**，只读四份本地缓存：
  1) _snapshots21/probe_infl_20261022/patent_cited.json
       2026-10-22 由 code/_probe_infl_data.py 一次性拉取（20,515 行，1.4 秒）
  2) _snapshots21/patent_scan_20261021.pkl
       blake2b(pn) → (city, year) 集合（2,562,101 个 pn）+ value_2024（申请人 → 2024 价值合计）
  3) _snapshots_gkx21/sz_patent_rows_gkx.json
       dwd_patent 全表按 (city, 申请人) 分组后的 value 填充计数（2,940,012 行口径）
  4) _snapshots21/patent_panel_innov_20261021.json
       全量面板 2,939,895 行的年/国别分布（只取行数与年份）

⚠ 语义红线（DATA_FACTS §3.17）：chain_intl 的 name_patent[nm][1] 是 WO/PCT 件数，
  不是授权数；授权数只能读 star_applicant_agg_gkx.json 的 agg[nm][1]。本脚本不用授权数，
  凡出现「授权」一律标注来源。

产物：code/M_INNOV_PATENT_INFLUENCE_out.json
"""
from __future__ import annotations

import hashlib
import json
import pickle
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from _innov_gkx21_common import dist, norm01, pct, write_out

METRIC = "M_INNOV_PATENT_INFLUENCE"
SNAP = HERE / "_snapshots21"
PROBE = SNAP / "probe_infl_20261022"


def h64(pn):
    """与 _patent_scan_20261021.py 完全一致的稳定哈希（blake2b-64）。"""
    return int.from_bytes(hashlib.blake2b(str(pn).encode(), digest_size=8).digest(), "big")


def bucket(n):
    if n == 0:
        return "0"
    if n == 1:
        return "1"
    if n <= 3:
        return "2-3"
    if n <= 5:
        return "4-5"
    if n <= 10:
        return "6-10"
    if n <= 20:
        return "11-20"
    return ">20"


def main():
    # ---------------- 1. 被引副表 ----------------
    d = json.loads((PROBE / "patent_cited.json").read_text(encoding="utf-8"))
    ix = {c: i for i, c in enumerate(d["columns"])}
    rows = d["rows"]
    pns = [r[ix["pn"]] for r in rows]
    cited = [int(r[ix["cited_by_nums"]] or 0) for r in rows]
    refc = [int(r[ix["reference_cited_count"]] or 0) for r in rows]
    nonp = [int(r[ix["non_patent_count"]] or 0) for r in rows]

    panel = json.loads((SNAP / "patent_panel_innov_20261021.json").read_text(encoding="utf-8"))
    panel_rows = int(panel["rows"])
    year_all = {int(k): int(v) for k, v in panel["year_all"].items()}

    dup_rows = len(rows) - len(set(pns))
    pos = [c for c in cited if c > 0]
    bib = {
        "rows": len(rows),
        "distinct_pn": len(set(pns)),
        "duplicate_pn_rows": dup_rows,
        "cited_by": {
            "nonnull": len(cited), "gt0": len(pos),
            "gt0_rate": round(len(pos) / len(cited), 4),
            "sum": sum(cited), "mean": round(statistics.mean(cited), 4),
            "median": statistics.median(cited), "max": max(cited),
            "p90": pct(cited, 0.90), "p99": pct(cited, 0.99),
            "buckets": {k: sum(1 for c in cited if bucket(c) == k)
                        for k in ["0", "1", "2-3", "4-5", "6-10", "11-20", ">20"]},
        },
        "reference_cited": {"gt0": sum(1 for c in refc if c > 0), "max": max(refc),
                            "sum": sum(refc),
                            "note": "本专利引用的专利文献数，王惠明确「不用本专利参考文献数」当被引"},
        "non_patent": {"gt0": sum(1 for c in nonp if c > 0), "sum": sum(nonp)},
    }

    # ---------------- 2. 与 294 万件主库的挂接率（本地哈希 join） ----------------
    pk = pickle.loads((SNAP / "patent_scan_20261021.pkl").read_bytes())
    cy_pn = pk["city_year_pn"]
    h2 = {}
    for (city, year), s in cy_pn.items():
        for x in s:
            h2.setdefault(x, (city, year))
    hit_rows = 0
    hit_year, hit_city = {}, {}
    for pn in pns:
        k = h2.get(h64(pn))
        if k:
            hit_rows += 1
            hit_year[k[1]] = hit_year.get(k[1], 0) + 1
            hit_city[k[0]] = hit_city.get(k[0], 0) + 1
    hit_distinct = sum(1 for pn in set(pns) if h64(pn) in h2)
    linked_cited = [int(r[ix["cited_by_nums"]] or 0) for r in rows if h64(r[ix["pn"]]) in h2]
    link = {
        "panel_pn_universe": sum(len(s) for s in cy_pn.values()),
        "panel_city_year_cells": len(cy_pn),
        "cited_rows_matched": hit_rows,
        "cited_rows_match_rate": round(hit_rows / len(rows), 4),
        "cited_distinct_matched": hit_distinct,
        "cited_distinct_match_rate": round(hit_distinct / len(set(pns)), 4),
        "by_year": dict(sorted(hit_year.items())),
        "by_city": dict(sorted(hit_city.items(), key=lambda kv: -kv[1])),
        "linked_cited": {"n": len(linked_cited), "gt0": sum(1 for c in linked_cited if c > 0),
                         "sum": sum(linked_cited), "max": max(linked_cited) if linked_cited else 0,
                         "mean": round(statistics.mean(linked_cited), 3) if linked_cited else None},
        "expected_if_random": ("若这 2 万件是主库的随机子集，按 2,562,101/2,939,895=87.15% 的"
                               "城市可归属率应有约 17,400 件命中；实测仅 " + str(hit_distinct) + " 件"),
    }

    # ---------------- 3. 价值维（全表口径） ----------------
    sz = json.loads((HERE / "_snapshots_gkx21" / "sz_patent_rows_gkx.json").read_text(encoding="utf-8"))
    groups = sz["groups"]
    v_rows = sum(v["n"] for v in groups.values())
    v_filled = sum(v["value_filled"] for v in groups.values())
    v_sum = sum(v["value_sum"] for v in groups.values())
    v_n = sum(v["value_n"] for v in groups.values())
    per_name = []
    for nm_key, v in groups.items():
        nm = nm_key.split("\x01")[-1]
        if v["value_n"]:
            per_name.append((nm, v["value_n"], v["value_sum"], v["value_sum"] / v["value_n"], v["n"]))
    value_dim = {
        "rows_counted": v_rows,
        "row_duplication_note": ("2,940,012 = dwd_patent 2,939,895 + 117 行重名重复计数"
                                 "（DATA_FACTS §3.5 的 47 组重名）"),
        "value_filled": v_filled,
        "value_fill_rate": round(v_filled / v_rows, 4),
        "value_sum": round(v_sum, 2),
        "value_mean_per_filled_patent": round(v_sum / v_n, 2) if v_n else None,
        "n_applicants_with_value": len(per_name),
        "per_applicant_mean_value": dist([p[3] for p in per_name]),
        "top10_by_value_sum": [
            {"name": p[0], "patents": p[4], "value_filled": p[1],
             "value_sum": round(p[2], 2)} for p in
            sorted(per_name, key=lambda x: -x[2])[:10]],
    }

    v2024 = pk.get("value_2024") or {}
    value_2024 = {
        "n_applicants": len(v2024),
        "sum": round(sum(v2024.values()), 2),
        "mean": round(statistics.mean(v2024.values()), 2) if v2024 else None,
        "max": round(max(v2024.values()), 2) if v2024 else None,
        "top10": [{"name": k, "value_sum": round(v, 2)}
                  for k, v in sorted(v2024.items(), key=lambda kv: -kv[1])[:10]],
        "note": "只覆盖 2024 单年，且仅含名称可归到 6 城的申请人；不能当多前年基线",
    }

    # ---------------- 4. 打分 ----------------
    # V1 王惠原式：0.8*norm(被引) + 0.2*norm(价值)；2 万件样本与价值维无法按 pn 对齐
    #（挂接率 1.78%，见上），价值维只能判缺测 → 重归一到 1.0*norm(被引)。
    n_cited = norm01(cited)
    score_v1 = [100 * x for x in n_cited]
    # 百分位版（对 55 次的长尾更稳健）
    order = sorted(range(len(cited)), key=lambda i: cited[i])
    pctile = [0.0] * len(cited)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and cited[order[j + 1]] == cited[order[i]]:
            j += 1
        avg = (i + j) / 2 / max(len(order) - 1, 1)
        for k in range(i, j + 1):
            pctile[order[k]] = avg
        i = j + 1
    score_pct = [100 * x for x in pctile]

    top = sorted(zip(pns, cited, refc, score_v1), key=lambda x: (-x[1], x[0]))[:10]

    payload = {
        "metric_id": METRIC,
        "metric_name": "专利影响力",
        "support_judgment": "部分支持",
        "run_at": "2026-10-22",
        "db": "gkx@183.240.141.251:3318（专利零 DB：非专利表读快照；专利数字全部读缓存）",
        "corpus": {"panel_rows": panel_rows, "year_all": dict(sorted(year_all.items())),
                   "cited_sample_rows": len(rows)},
        "citation_dim": bib,
        "linkage": link,
        "value_dim": value_dim,
        "value_dim_2024": value_2024,
        "score": {
            "formula_wanghui": "S=100*(0.80*norm(被引次数)+0.20*norm(专利价值))，缺测维重归一",
            "formula_executed": "S=100*norm(被引次数)（价值维与样本无法按 pn 对齐 → 判缺测，权重 0.20 重归一）",
            "v1_minmax": dist(score_v1),
            "v1_percentile": dist(score_pct),
            "n_scored": len(score_v1),
            "top10": [{"pn": t[0], "cited_by_nums": t[1], "reference_cited_count": t[2],
                       "score": round(t[3], 2)} for t in top],
        },
        "coverage_chain": {
            "sample_vs_corpus": round(len(set(pns)) / panel_rows, 6),
            "linked_vs_sample": round(hit_distinct / len(set(pns)), 4),
            "attributable_vs_corpus": round(hit_distinct / panel_rows, 8),
            "note": ("被引副表 2 万件 → 与主库按 pn 可对上 355 件 → 占 294 万件语料 0.0121%。"
                     "这条链条决定了「专利影响力」当前只能做样本级分布，不能做全库排名。"),
        },
        "base_years_used": sorted(hit_year.keys()),
        "base_years_missing": [2017, 2018, 2019, 2020, 2024, 2025, 2026],
        "base_years_note": ("dwd_patent 的 apdt_year 只有 2021—2026（2017—2020 零行）；"
                            "被引样本能挂到年份的只有 2021—2023 三年（237/111/12 件），"
                            "2024—2026 挂接为 0。任何「前 N 年基线」在专利侧只能用 2021—2023，"
                            "不得把缺失年按 0 摊进分母。"),
        "gaps": [
            "被引副表只覆盖 2 万件专利（占主库 0.68%），且仅 1.78% 能与主库 pn 对齐；"
            "本库 294 万件专利中 99.99% 没有被引记录，不能按 0 处理（0 是「未被引」还是「未采集」无法区分）。",
            "专利价值 value 全表填充 67.85%，但被引副表里没有 value 列、两表无法按 pn 连接，"
            "王惠 0.20 权重的价值维在本脚本中只能判缺测。",
            "被引副表 20,515 行只有 20,000 个不同 pn（515 行重复），重复行按 1 件计会影响均值。",
            "无 SEP / 标准必要专利字段，seed 备注里的「SEP 为辅」无法落地。",
        ],
    }
    p = write_out(METRIC, payload)
    print(json.dumps({"wrote": str(p), "cited": payload["citation_dim"]["cited_by"],
                      "linkage": payload["linkage"],
                      "value_fill": value_dim["value_fill_rate"]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
