#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_SZ_ADVANTAGE_SCORE · 深圳优势评分（四城对标，2026-10-21）

王惠口径（M_CHAIN_SZ_ADVANTAGE_SCORE V2-20260824）：
  四维 = 企业(数量/规模/质量各 1/3)、专利(数量)、政策(数量)、人才(数量/水平各 1/2)
  每个三级在默认对标集合 C={北京,上海,广州,深圳} 上 min-max 至 0–100，四维各 0.25 合成。

本实现的现实约束（全部披露）：
  * 默认对标集合 C 在开发库中无法成立：底册北京仅 163 家、上海仅 16 家，
    可比的只有深圳/广州/东莞/惠州四城 → 本报告按四城对标，禁止称「全国对标/全国排名」；
  * 政策维：policy_base 的 keywords/keypoints 全 NULL，只能用 title 字面命中，12 链合计仅 15 条；
  * 人才维：链上高校/科研机构（tags.company_name ∩ 深圳机构名）= 0 行，链级人才无法算。

输入：_snapshots/sz_chain_matrix_20261021.json
输出：code/M_CHAIN_SZ_ADVANTAGE_SCORE_out.json
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _sz5_common as S  # noqa: E402

METRIC = "M_CHAIN_SZ_ADVANTAGE_SCORE"
NAME = "深圳优势评分"
PAT_NOTE = ("专利数来自 _snapshots/chain_h_stream_20261021.json 的 pat_city_chain："
            "200,000 件专利样本（占 293.99 万件的 6.80%）、61,229 个申请人名，"
            "按链上企业 company_name 字面匹配后归集到四城，是抽样计数而非全量。")


def compute() -> dict:
    m = S.load_matrix()
    rows = []
    for c, nm in S.chains(m):
        # 企业维三级
        cnt = {city: m["ent_city_base"][c][city] for city in S.CITY4}
        rev = {city: m["revenue"]["by_chain_city_yi"][c][city] for city in S.CITY4}
        inten = {city: (m["rd"]["by_chain_city"][c][city]["intensity_pct"] or 0.0) for city in S.CITY4}
        sc, _ = S.minmax(cnt)
        sr, _ = S.minmax(rev)
        si, _ = S.minmax(inten)
        ent_dim = {city: round((sc[city] + sr[city] + si[city]) / 3, 2) for city in S.CITY4}

        # 专利维
        pat = {city: int(m["patent"]["by_chain_city"].get(c, {}).get(city, 0)) for city in S.CITY4}
        pat_dim, pat_meta = S.minmax(pat)

        # 政策维（title 字面命中）
        pol = {city: int(m["policy_title_hits"][c][city]) for city in S.CITY4}
        pol_total = sum(pol.values())
        pol_dim, pol_meta = S.minmax(pol) if pol_total >= 3 else (None, {"insufficient": True, "total": pol_total})

        # 人才维：链级不可得
        tal_dim = None

        avail = {"企业": ent_dim, "专利": pat_dim}
        sz_avail = round(sum(d[city] for d in avail.values() for city in [ "深圳市"]) / len(avail), 2)

        full = {}
        for city in S.CITY4:
            parts = [ent_dim[city], pat_dim[city]]
            if pol_dim:
                parts.append(pol_dim[city])
            parts += [50.0] * (4 - len(parts))  # 缺维按王惠「全体相同取 50」降级填充
            full[city] = round(sum(parts) / 4, 2)

        rows.append({
            "industry_code": c, "industry_name": nm,
            "dims": {"企业": ent_dim, "专利": pat_dim, "政策": pol_dim, "人才": tal_dim},
            "sz_score_available_dims": sz_avail,
            "sz_score_wanghui4_filled": full["深圳市"],
            "city_scores_available": {city: round(sum(d[city] for d in avail.values()) / len(avail), 2)
                                      for city in S.CITY4},
            "city_scores_wanghui4": full,
            "sz_rank_available": 1 + sum(1 for city in S.CITY4
                                         if round(sum(d[city] for d in avail.values()) / len(avail), 2) > sz_avail),
            "sz_rank_wanghui4": 1 + sum(1 for city in S.CITY4 if full[city] > full["深圳市"]),
            "raw": {"count": cnt, "revenue_yi": rev, "rd_intensity_pct": inten, "patent_sample": pat,
                    "policy_title": pol},
            "meta": {"patent": pat_meta, "policy": pol_meta,
                     "policy_available": pol_dim is not None, "talent_available": False},
        })
    rows.sort(key=lambda r: -r["sz_score_available_dims"])

    avail_scores = [r["sz_score_available_dims"] for r in rows]
    full_scores = [r["sz_score_wanghui4_filled"] for r in rows]
    rank_a = [r["sz_rank_available"] for r in rows]
    rank_w = [r["sz_rank_wanghui4"] for r in rows]
    n_pol_avail = sum(1 for r in rows if r["meta"]["policy_available"])
    rep = {
        "metric_id": METRIC, "metric_name": NAME, "date": "2026-10-21",
        "calc_logic_ref": "metrics/calc-logic/CHAIN/M_CHAIN_SZ_ADVANTAGE_SCORE.md (V2-20260824)",
        "formula": ("每三级在四城集合 min-max 至 0–100；企业维=(数量+规模+质量)/3；"
                    "可得维口径 =（企业+专利）等权；王惠满配口径 =0.25×(企业+专利+政策+人才)，缺维填 50"),
        "benchmark_set": {"cities": S.CITY4, "n": 4,
                          "why_not_beijing_shanghai": "底册北京 163 家、上海 16 家，与深圳 95,600 家不可比；"
                                                      "四城对标是本库唯一可解释的截面"},
        "per_chain": rows,
        "stats_sz_available": S.stats(avail_scores),
        "stats_sz_wanghui4": S.stats(full_scores),
        "rank_available": {k: rank_a.count(k) for k in sorted(set(rank_a))},
        "rank_wanghui4": {k: rank_w.count(k) for k in sorted(set(rank_w))},
        "rank_change": sum(1 for a, b in zip(rank_a, rank_w) if a != b),
        "corr_available_vs_wanghui4": S.spearman(avail_scores, full_scores),
        "dim_availability": {
            "企业": {"available": True, "caveat": "规模维营收覆盖 0.65% 底册企业，质量维 876 家上市企业"},
            "专利": {"available": True, "caveat": PAT_NOTE},
            "政策": {"available": n_pol_avail == 12, "chains_with_signal": n_pol_avail,
                     "caveat": "keywords/keypoints 全 NULL，仅 title 字面命中；12 链合计 15 条，远不足以度量政策强度"},
            "人才": {"available": False,
                     "caveat": "链上高校/科研机构挂链 0 行；城市级学者仅 199 人（深圳），且学位表与主档 ID 交集 8.69%"},
        },
    }
    rep["support_judgment"] = {
        "data_support_level": "部分支持",
        "reason": ("四维中只有企业维与专利维可算（企业维仍受营收 0.65%、研发 876 家稀疏所限；"
                   "专利维为 6.80% 抽样），政策维 10/12 链无任何命中、人才维链级完全无数据；"
                   "按 §〇「始终有部分依赖维得不到足够数据」判『部分支持』。"
                   "另：需求原文要求『深圳与全国产业数据对比』，本库省外样本 0.18%，全国对标不可实现。"),
        "criteria": {"dims_available": 2, "dims_required": 4,
                     "policy_chains_with_signal": n_pol_avail,
                     "talent_chain_rows": m["talent_institute_on_chain_sz"][0]["n"],
                     "benchmark_cities": 4},
    }
    rep["elapsed_sec"] = None
    return rep


def main():
    t0 = time.time()
    rep = compute()
    rep["elapsed_sec"] = round(time.time() - t0, 1)
    S.write_out(METRIC, rep)
    print("available stats", rep["stats_sz_available"], "ranks", rep["rank_available"])
    print("wanghui4 stats", rep["stats_sz_wanghui4"], "ranks", rep["rank_wanghui4"],
          "changed", rep["rank_change"], "corr", rep["corr_available_vs_wanghui4"])
    for r in rep["per_chain"]:
        print(f"  {r['industry_name']:10s} avail={r['sz_score_available_dims']:6.2f} r={r['sz_rank_available']} "
              f"| wh4={r['sz_score_wanghui4_filled']:6.2f} r={r['sz_rank_wanghui4']} "
              f"| ent={r['dims']['企业']['深圳市']:.1f} pat={r['dims']['专利']['深圳市']:.1f}")


if __name__ == "__main__":
    main()
