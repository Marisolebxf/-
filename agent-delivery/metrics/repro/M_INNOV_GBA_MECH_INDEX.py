#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_GBA_MECH_INDEX · 湾区创新机制指数（20261021 版，gkx 单库）

王惠 V1.5 三子项（缺测维不补 0，剩余权重归一）：
  联合专利 = 多申请人专利 COUNT(DISTINCT pn)
  合作项目 = 多机构项目 COUNT(DISTINCT id)
  成果转化 = 转移专利数 / 该城专利件数
  mech_index = (norm(联合) + norm(合作) + norm(转化)) / 3 × 100

本库实测：三子项**全部无法按定义计算**，原因各不相同（缺列 / 整列为空 / 封闭抽样）：
  联合专利：dwd_patent 无 applicants 列；dwd_patent_applicants 是 20,000 个 pn 的封闭抽样
            （占主表 0.68%），且共申请人名与底册精确对齐率 1.51%
  合作项目：dwd_zh_project.funded_institution 58,453 行**整列为空**；
            participating_institution 是单机构名（含分隔符仅 29 行 = 0.05%）
  成果转化：dwd_patent_transfer 也是 20,000 个 pn 的封闭抽样，权利人名称对齐率 2.07%
故本脚本只输出**不可算证明**与样本内读数（标记 sample_only），不合成指数。
"""
from __future__ import annotations

import json

import _gba21_common as G

METRIC = "M_INNOV_GBA_MECH_INDEX"


def _applicant_rows():
    """28,964 行共申请人表（小表，一次取回并落缓存；不碰 dwd_patent）。"""
    cache = G.load("gba_applicant_rows_20261021.json")
    if cache is not None:
        return [(r[0], r[1]) for r in cache]
    cur = G._gkxdb.gkx()
    try:
        cur.execute("SET SESSION max_execution_time=120000")
        cur.execute("SELECT pn, name FROM gkx.dwd_patent_applicants")
        rows = cur.fetchall()
    finally:
        cur.close()
    G.save("gba_applicant_rows_20261021.json", [list(r) for r in rows])
    return rows


def main():
    pat = G.patents()
    pr1 = G.load("gba_probe_20261021.json")["probes"]
    pr2 = G.load("gba_probe2_20261021.json")
    wa, _ = G.name_area_weights()
    name_city = {}
    for nm, lst in wa.items():
        # 一名多行时按权重汇总，主城取权重最大者（仅用于「是否可对齐」的判定）
        best = max(lst, key=lambda x: x[2])
        name_city[nm] = best[0]

    # ---- 联合专利：封闭抽样内读数 ----
    rows = _applicant_rows()
    by_pn = {}
    for pn, nm in rows:
        by_pn.setdefault(pn, set()).add((nm or "").strip())
    multi = {pn: names for pn, names in by_pn.items() if len(names) >= 2}
    joint_by_city = {c: 0 for c in G.CITY4}
    joint_matched = 0
    for pn, names in multi.items():
        hit = {name_city[n] for n in names if n in name_city}
        if hit:
            joint_matched += 1
            for c in hit:
                if c in joint_by_city:
                    joint_by_city[c] += 1

    # ---- 成果转化：封闭抽样内读数（按 pn 去重，一件专利可命中多城则各计一次）----
    tr = G.load("gba_transfer_rows_20261021.json") or []
    tr_sets = {c: set() for c in G.CITY4}
    for rec in tr:
        for nm in (rec.get("before") or []) + (rec.get("after") or []):
            c = name_city.get(nm.strip())
            if c in G.CITY4:
                tr_sets[c].add(rec["pn"])
    tr_by_city = {c: len(v) for c, v in tr_sets.items()}
    tr_matched = len(set().union(*tr_sets.values())) if tr_sets else 0

    sample_only = {
        "joint_patent": {
            "sample_pn": len(by_pn), "sample_multi_applicant_pn": len(multi),
            "matched_pn": joint_matched,
            "by_city": joint_by_city,
            "coverage_of_main_table": round(len(by_pn) / G.PAT_TOTAL, 5),
            "name_match_rate": pr2["applicants_name"]["exact_hit_rate"],
            "verdict": "sample_only（0.68% 封闭抽样 + 1.51% 名称对齐，不能外推为全库联合专利）",
        },
        "coop_project": {
            "rows": pr1["project"]["rows"],
            "funded_institution_empty": pr1["project"]["no_funded_institution"],
            "funded_institution_empty_pct": 1.0,
            "multi_institution_rows": 29,
            "multi_institution_pct": round(29 / pr1["project"]["rows"], 5),
            "by_city": {c: 0 for c in G.CITY4},
            "verdict": "structurally_unavailable（『≥2 机构』的分母字段整列为空）",
        },
        "transfer": {
            "sample_pn": len({r["pn"] for r in tr}), "matched_pn": tr_matched,
            "by_city": tr_by_city,
            "coverage_of_main_table": round(len({r["pn"] for r in tr}) / G.PAT_TOTAL, 5),
            "name_match_rate": pr2["transfer_name"]["exact_hit_rate"],
            "verdict": "sample_only（0.68% 封闭抽样 + 2.07% 名称对齐，不能作转化率分子）",
        },
    }

    # ---- 按定义尝试一次：三子项可得数 ----
    attempts = {}
    for c in G.CITY4:
        attempts[c] = {
            "joint_patent_cnt": None,
            "coop_project_cnt": None,
            "patent_transfer_cnt": None,
            "mech_index": None,
            "blocked_by": ["联合专利: 共申请人表仅 0.68% 抽样",
                           "合作项目: funded_institution 整列为空",
                           "成果转化: 转移表仅 0.68% 抽样"],
        }

    result = {
        "metric_id": METRIC,
        "name": "创新机制指数（湾区）",
        "formula_owner": "王惠（V1.5-20260830，口径保真登记；本版不产出指数值）",
        "asof": "2026-10-22",
        "formula": "mech_index = (norm(joint) + norm(coop) + norm(transfer_rate)) / 3 × 100；缺测维不补 0，剩余权重归一",
        "rows": [{"city": c, **attempts[c]} for c in G.CITY4],
        "subitems_computable": 0,
        "subitems_total": 3,
        "sample_only_readings": sample_only,
        "denominator_patents_2021_24": pat["city_total"],
        "why_not_partial": (
            "王惠指数的定义是三个子项各自归一后的等权平均；本库三个子项的可算数都是 0 项，"
            "剩余权重归一会得到空集。样本内读数（联合 6,477 个多申请人 pn 中能对齐到四城的仅 %d 个）"
            "只覆盖主表 0.68%%，把它当城市指标等于用千分之七的样本冒充全库，属造数级误用，"
            "故不降为部分支持。" % joint_matched
        ),
        "upgrade_path": [
            "dwd_patent 补 applicants 全申请人列，或 dwd_patent_applicants 全量回填（现 28,964 行 / 20,000 pn）",
            "dwd_zh_project.funded_institution 回填（现 58,453 行全空），participating_institution 改为多值结构",
            "dwd_patent_transfer 全量（现 22,809 行 / 20,000 pn）并补机构外键，替代名称匹配",
            "建立「专利申请人名 → 统一社会信用代码」映射表，把当前 1.51% / 2.07% 的对齐率提到可用水平",
        ],
        "probes": {
            "patent_table_rows": G.PAT_TOTAL,
            "applicants_rows": pr1["applicants"]["rows"],
            "applicants_distinct_pn": pr1["applicants"]["distinct_pn"],
            "applicants_multi_pn": len(multi),
            "applicants_name_match_rate": pr2["applicants_name"]["exact_hit_rate"],
            "transfer_rows": pr1["transfer"]["rows"],
            "transfer_distinct_pn": pr1["transfer"]["distinct_pn"],
            "transfer_name_match_rate": pr2["transfer_name"]["exact_hit_rate"],
            "transfer_pn_with_any_match": pr2["transfer_name"]["pn_either_match"],
            "project_rows": pr1["project"]["rows"],
            "project_funded_institution_empty": pr1["project"]["no_funded_institution"],
            "project_multi_institution_rows": 29,
            "project_year_range": pr1["project"]["year_range"],
        },
        "support_judgment": "完全不支持",
        "support_reason": (
            "三个子项全部无法按定义计算：联合专利缺 applicants 列且共申请人表仅 20,000 个 pn 的封闭抽样"
            "（0.68%，名称对齐 1.51%）；合作项目的 funded_institution 58,453 行整列为空、"
            "participating_institution 单值（可拆多机构仅 29 行）；成果转化表同为 20,000 pn 抽样"
            "（名称对齐 2.07%）。0/3 子项可算，指数无定义域 → 完全不支持"
        ),
    }
    G.write_out(METRIC, result)
    print("joint sample", len(by_pn), "multi", len(multi), "matched", joint_matched, joint_by_city)
    print("transfer sample", len({r['pn'] for r in tr}), "matched", tr_matched, tr_by_city)
    print("support", result["support_judgment"])


if __name__ == "__main__":
    main()
