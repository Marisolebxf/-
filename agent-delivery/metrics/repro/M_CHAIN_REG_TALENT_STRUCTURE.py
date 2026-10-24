#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_REG_TALENT_STRUCTURE 人才结构（区域）（20261021 改源版）

需求语境：区域产业指数模型 → 学术生态竞争力 → 「人才结构」。
20261019 判「完全不支持」的理由是「人才结构无面，ADS 只有人才总量」。改源到 gkx 后
表是齐的（学者 21,316 / 学历 43,766 / 研究方向 20,030 / 头衔 20,030 / 工作经历 57,117），
**但四张附表与主表的 scholar_id 是两个 ID 空间**：学历 15,851 个 ID 只有 1,753 个（8.2%）
能在 `dwd_scholar` 找到，研究方向 8.7%、头衔 8.7%、论文关系 9.2%。

因此本脚本只做三件事，并把「为什么不能出链×城学历结构」算成可核查的数字：
  1. 主表学者按机构落 4 市（1,202 人，5.6%），给出市域层面的规模与影响力结构；
  2. 学历表独立分布（15,851 人，无机构字段 → 不可落城）；
  3. 主表 ∩ 学历表 = 1,753 人，其中落 4 市仅 119 人 → 学历结构的分母不足，禁用。

输出：code/M_CHAIN_REG_TALENT_STRUCTURE_out.json
"""
from __future__ import annotations

import time
from collections import Counter, defaultdict

from _reg5_common import (CHAIN_AXIS, CHAIN_CN, CITY4, degree_bucket, match_org, pct, probe3,
                          stats, write_out)

MID = "M_CHAIN_REG_TALENT_STRUCTURE"
RANK = {"博士": 3, "硕士": 2, "学士": 1, "其他": 0}


def main() -> None:
    t0 = time.time()
    p3 = probe3()
    scholars = p3["scholar_min"]["rows"]        # scholar_id, name, org, papers, cites, h
    degree = p3["degree_min"]["rows"]
    direction = p3["direction_min"]["rows"]
    talent = p3["talent_min"]["rows"]
    degree_dist = __import__("_reg5_common")._load("reg5_probe_20261021.json", {})["queries"]["degree_dist"]["rows"]

    dmap = defaultdict(list)
    for sid, d in degree:
        dmap[sid].append(d)
    dmatch = set(dmap)

    city_of, kind_ct = {}, Counter()
    matched_any = 0
    for sid, nm, org, pn, cn, h in scholars:
        c, k = match_org(org)
        if c:
            matched_any += 1
            kind_ct[k] += 1
        if c in CITY4:
            city_of[sid] = c

    city_scholars = Counter(city_of.values())
    city_degree = Counter()
    city_degree_rank = defaultdict(dict)
    for sid, c in city_of.items():
        ds = dmap.get(sid)
        if not ds:
            continue
        b = degree_bucket(ds)
        city_degree[(c, b)] += 1
        city_degree_rank[c][sid] = b

    city_impact = {}
    for c in CITY4:
        rows = [r for r in scholars if city_of.get(r[0]) == c]
        h = [int(r[5] or 0) for r in rows]
        city_impact[c] = {
            "scholars": len(rows),
            "papers_sum": sum(int(r[3] or 0) for r in rows),
            "citations_sum": sum(int(r[4] or 0) for r in rows),
            "h_median": round(sorted(h)[len(h) // 2], 2) if h else None,
            "h_ge_10": sum(1 for x in h if x >= 10),
            "h_ge_30": sum(1 for x in h if x >= 30),
            "with_degree": sum(1 for r in rows if r[0] in dmatch),
            "degree_share_pct": pct(sum(1 for r in rows if r[0] in dmatch), len(rows)),
            "degree_buckets": {b: city_degree[(c, b)] for b in ("博士", "硕士", "学士", "其他")},
        }

    # 学历表独立分布（按人取最高）
    best = {}
    for sid, d in degree:
        b = degree_bucket([d])
        if sid not in best or RANK[b] > RANK[best[sid]]:
            best[sid] = b
    deg_dist = Counter(best.values())
    deg_total = sum(deg_dist.values())

    names = {r[0] for r in scholars}
    dset = {r[0] for r in degree}
    dirset = {r[0] for r in direction}
    tset = {r[0] for r in talent}
    acad = [sid for sid, a in talent if int(a or 0) == 1]
    acad_in4 = [s for s in acad if s in city_of]

    # 研究方向 → 链（代理，仅量化可用性，不进主值）
    kw = {
        "INB1306": ["software", "information service"], "INB1309": ["artificial intelligence", "machine learning", "deep learning"],
        "INB1333": ["consumer electronic", "display"], "INB1502": ["digital media", "cultural", "animation"],
        "INB2505": ["synthetic biology", "biomanufacturing", "metabolic engineering"],
        "INB1204": ["robotic", "manipulator"], "INB1303": ["semiconductor", "integrated circuit", "wafer"],
        "INB1323": ["sensor", "sensing"], "INB1354": ["embodied", "humanoid"],
        "INB1209": ["autonomous vehicle", "connected vehicle", "lidar"], "INB1236": ["uav", "drone", "low-altitude"],
        "INB2503": ["biomedical", "cancer", "clinical", "pharmac", "genomic"],
    }
    dir_chain = {}
    for sid, f in direction:
        fl = (f or "").lower()
        hit = [ch for ch, ks in kw.items() if any(k in fl for k in ks)]
        if hit:
            dir_chain[sid] = hit
    dir_cells = Counter()
    deg_cells = Counter()
    for sid, chs in dir_chain.items():
        c = city_of.get(sid)
        if c:
            for ch in chs:
                dir_cells[(ch, c)] += 1
                if sid in dmatch:
                    deg_cells[(ch, c)] += 1

    matrix = []
    for ch in CHAIN_AXIS:
        row = {"chain": ch, "chain_name": CHAIN_CN[ch], "cells": {}}
        for c in CITY4:
            row["cells"][c] = {
                "scholars_by_research_direction": dir_cells.get((ch, c), 0),
                "scholars_in_city": dir_cells.get((ch, c), 0),
                "degree_records_in_city": deg_cells.get((ch, c), 0),
            }
        matrix.append(row)

    payload = {
        "metric_id": MID,
        "metric_name": "人才结构（区域）",
        "date": "2026-10-22",
        "formula_owner": "徐滕强（CHAIN 域 calc-logic，仅给指标名）",
        "source": ("gkx.dwd_scholar(21,316) + dwd_scholar_education_background(43,766) + "
                   "dwd_scholar_research_direction(20,030) + dwd_scholar_talent_flag(20,030)"),
        "region_axis": CITY4,
        "chain_axis": len(CHAIN_AXIS),
        "city_scholars": {c: city_scholars.get(c, 0) for c in CITY4},
        "city_impact": city_impact,
        "degree_distribution_standalone": {
            "scholars": deg_total,
            "buckets": dict(deg_dist),
            "shares_pct": {k: pct(v, deg_total) for k, v in deg_dist.items()},
            "note": "学历表无机构/城市字段，只能给全国分布，不能落 4 市。",
        },
        "matrix": matrix,
        "matrix_note": ("矩阵内 scholars_in_city 是**链归属后**的人数（研究方向英文词代理），"
                        "不是市域学者总量；市域总量见 city_scholars。链维度只有 14/48 单元非零，"
                        "degree_records_in_city 进一步按主表∩学历表收敛，多数单元为 0。"),
        "probes": {
            "scholars_total": len(scholars),
            "scholars_with_org": sum(1 for r in scholars if (r[2] or "").strip()),
            "scholars_org_matched": matched_any,
            "scholars_org_matched_pct": pct(matched_any, len(scholars)),
            "org_match_kind": dict(kind_ct),
            "scholars_in_city4": sum(city_scholars.values()),
            "scholars_in_city4_pct": pct(sum(city_scholars.values()), len(scholars)),
            "degree_rows": 43766,
            "degree_distinct_ids": len(dset),
            "scholar_degree_overlap": len(names & dset),
            "scholar_degree_overlap_pct": pct(len(names & dset), len(names)),
            "direction_distinct_ids": len(dirset),
            "scholar_direction_overlap": len(names & dirset),
            "scholar_direction_overlap_pct": pct(len(names & dirset), len(names)),
            "talent_distinct_ids": len(tset),
            "scholar_talent_overlap": len(names & tset),
            "scholar_talent_overlap_pct": pct(len(names & tset), len(names)),
            "academicians": len(acad),
            "academicians_in_city4": len(acad_in4),
            "city4_with_degree": sum(city_impact[c]["with_degree"] for c in CITY4),
            "city4_degree_share_pct": pct(sum(city_impact[c]["with_degree"] for c in CITY4),
                                          sum(city_scholars.values())),
            "direction_chain_cells_nonzero": sum(1 for ch in CHAIN_AXIS for c in CITY4 if dir_cells[(ch, c)]),
            "degree_raw_dist_top": degree_dist[:12],
        },
        "support_judgment": {
            "data_support_level": "完全不支持",
            "reason": (
                f"人才结构的核心是「链上人才按学历/职称分层」，但两跳都断：其一，学历表 15,851 个 scholar_id "
                f"与主表 21,316 个只有 {len(names & dset):,} 个（{pct(len(names & dset), len(names))}%）能对上，"
                f"研究方向与头衔同样只有 8.7%，四张附表实际是另一个学者宇宙；其二，能落 4 市的主表学者仅 "
                f"{sum(city_scholars.values()):,} 人（{pct(sum(city_scholars.values()), len(scholars))}%），"
                f"其中同时有学历记录的只有 {sum(city_impact[c]['with_degree'] for c in CITY4)} 人，"
                f"不足以支撑任何市域学历分布；其三，学者机构以高校为主，与产业链标签无挂接，链维只能靠研究方向英文词代理，"
                f"48 个单元里仅 {sum(1 for ch in CHAIN_AXIS for c in CITY4 if dir_cells[(ch, c)])} 个非零。"
                f"结构与数据均不构成可算闭环，故维持完全不支持。"
            ),
            "criteria": {"scholars": len(scholars), "scholar_degree_overlap_pct": pct(len(names & dset), len(names)),
                         "scholar_direction_overlap_pct": pct(len(names & dirset), len(names)),
                         "city4_scholars": sum(city_scholars.values()),
                         "city4_with_degree": sum(city_impact[c]["with_degree"] for c in CITY4),
                         "chain_cells_nonzero": sum(1 for ch in CHAIN_AXIS for c in CITY4 if dir_cells[(ch, c)])},
        },
        "notes": [
            "四张学者附表（学历/研究方向/头衔/论文关系）与主表 scholar_id 交集 8.2%—9.2%，"
            "这是主键不统一，不是抽样；任何跨表人口统计都会把分母打掉九成。",
            "主表 `scholar_org_id` 21,316 行**全为空串**，机构归属只能用 `scholar_org_name_zh` 文本匹配，"
            "精确命中 16,120、前缀命中 2,192、城市词兜底 29，仍余 2,488 条匹配不上。",
            "学者总体以高校/中科院为主（机构 TOP：中国科学院 728、上海交通大学 703、北京大学 364），"
            "4 市只占 5.6%，这是全国学者库的结构，不是深圳都市圈的人才结构。",
            "研究方向字段是英文短语（如 Synthetic Biology;Enzyme Engineering），可做链领域代理，"
            "但一个学者可命中多条链，且只覆盖 8.7% 主表人口，**不进入任何正式值**。",
            "`dwd_scholar_work_experience` 57,117 行同样存在 ID 空间问题（20,028 个 ID），未计入本指标。",
            "替代路线见 §四：若甲方能把学者主键统一，或给学历表补机构/城市字段，本指标可立即升级为部分支持。",
        ],
        "elapsed_sec": round(time.time() - t0, 2),
    }
    write_out(MID, payload)
    print("scholars", len(scholars), "org matched", matched_any, "in4", sum(city_scholars.values()))
    print("degree overlap", len(names & dset), "city4 degree", sum(city_impact[c]["with_degree"] for c in CITY4))
    print("degree dist", dict(deg_dist), "academicians", len(acad), "in4", len(acad_in4))
    print("dir cells nonzero", payload["probes"]["direction_chain_cells_nonzero"])


if __name__ == "__main__":
    main()
