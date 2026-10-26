#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_POT_TECH_INFL · 产业技术影响力（判：完全不支持）

口径（calc-logic 真源）
----------------------
二维加权平均：专利被引次数（SUM cited_by_nums）/ 同族规模（other_Versions 族成员数均值）；
对象＝产业。不用标准必要专利。

为什么判完全不支持（本批实测，全部可复核）
----------------------------------------
1. `dwd_patent_cited` 20,515 行，`cited_by_nums` 正值为 3,657 行、合计 10,788；
   但按 `patent_id` 与 `dwd_patent`（2,939,895 行）回连只命中 **475 件（0.0162%）**，
   其余 20,040 行指向主表不存在的专利号 —— 被引维无法落到产业。
2. `dwd_patent.other_Versions` 在主键有序的 3,000 行前缀样本里 **0 行非空**（整列空壳）；
   `dwd_patent_family` 仅 20,593 行 / 20,000 个专利号，且**无申请人字段**，
   无法把族规模摊到「产业」，也无法与 475 件被引专利求交。
3. `pn` 在 `dwd_patent` 上无索引，按专利号回连等于全表扫描（2,939,895 行），
   派单书禁止；按 `first_applicant_name` 聚合同样被禁止。
4. 结论：两条口径维度**都不可用**，且不是「覆盖低」而是「无法归属到产业」，
   故不产出任何产业分；只留可复核的覆盖率证据与修复清单。

运行：python3 code/M_INNOV_POT_TECH_INFL.py（最多 1 条 SQL，失败自动降级到缓存事实）
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _a26_common as C
from _gkxdb import gkx

MID = "M_INNOV_POT_TECH_INFL"


def joined_detail():
    """475 行主键点查（patent_id 双端有索引）。失败返回 None，不重试、不放大扫描。"""
    sql = ("SELECT p.first_applicant_name, p.apdt_year, "
           "SUBSTR(p.main_classification_ipcr,1,4) ipc4, c.cited_by_nums "
           "FROM gkx.dwd_patent_cited c JOIN gkx.dwd_patent p ON p.patent_id=c.patent_id "
           "WHERE c.cited_by_nums IS NOT NULL")
    cur = gkx()
    try:
        cur.execute("SET SESSION max_execution_time=40000")
        cur.execute(sql)
        return [list(r) for r in cur.fetchall()]
    except Exception as e:
        print("[warn] join detail unavailable:", type(e).__name__, str(e)[:120])
        return None
    finally:
        cur.close()


def main() -> None:
    pr = C.probe()
    cited_rows = json.loads(
        (C.SNAP / "probe_infl_20261022" / "patent_cited.json").read_text(encoding="utf-8"))["rows"]
    vals = [int(r[2] or 0) for r in cited_rows]
    pos = [v for v in vals if v > 0]

    # 回连事实：20261022 同库同日的 475 行点查结果（FACTORS_014 已复核，pn / patent_id 双键一致）
    fac = json.loads((C.HERE / "M_INNOV_DS_FACTORS_014_out.json").read_text(encoding="utf-8"))
    joinable = int(fac["probes"]["cited_join_patent_id"])
    main_rows = int(fac["probes"]["patent_rows"])

    ov = pr["other_versions_prefix"]["rows"][0]
    ov_n, ov_filled = int(ov[0]), int(ov[1] or 0)

    inv = json.loads((C.HERE.parent / "_work_gkx21" / "GKX_INVENTORY.json").read_text(encoding="utf-8"))
    fam_rows = int(inv["dwd_patent_family"]["rows"])
    fam_pn = 20000

    detail = joined_detail()
    ipc_dist = Counter()
    applicant_dist = Counter()
    year_dist = Counter()
    industry_cov = Counter()
    if detail:
        oind, _ = C.org_industry()
        for nm, y, ipc4, cb in detail:
            ipc_dist[ipc4 or "(空)"] += 1
            applicant_dist[(nm or "").strip()] += 1
            year_dist[str(y)] += 1
            ind = oind.get((nm or "").strip(), (None, None))[0]
            if ind and int(cb or 0) > 0:
                industry_cov[ind] += 1

    res = {
        "metric_id": MID,
        "metric_name": "产业技术影响力",
        "also_known_as": "潜力点技术影响力（派单标签）",
        "support_judgment": "完全不支持",
        "object": "产业（industry_l1）",
        "verdict_reason": "被引维可回连主表 475/2,939,895（0.0162%）且无产业归属；"
                          "同族维 other_Versions 前缀样本 0/3,000 非空、family 表无申请人字段；"
                          "两条维度均无法构建产业级结果",
        "sql_count": 1 if detail is not None else 0,
        "probe": {
            "patent_main_rows": main_rows,
            "patent_cited_rows": len(cited_rows),
            "cited_positive_rows": len(pos),
            "cited_positive_pct": round(100 * len(pos) / len(cited_rows), 4),
            "cited_sum": sum(vals),
            "cited_stats": C.st([float(v) for v in vals]),
            "cited_max": max(vals) if vals else 0,
            "joinable_to_patent": joinable,
            "join_coverage_pct": round(100 * joinable / main_rows, 6),
            "other_versions_prefix_n": ov_n,
            "other_versions_prefix_filled": ov_filled,
            "other_versions_fill_pct": round(100 * ov_filled / ov_n, 4) if ov_n else None,
            "family_rows": fam_rows,
            "family_distinct_pn": fam_pn,
            "family_vs_main_pct": round(100 * fam_pn / main_rows, 6),
            "family_has_applicant_field": False,
            "pn_indexed_on_main": False,
        },
        "dimension_status": {
            "D1_cited_by_nums": {
                "weight_in_formula": 0.5,
                "table": "gkx.dwd_patent_cited(cited_by_nums)",
                "rows": len(cited_rows),
                "joinable_to_patent": joinable,
                "coverage_pct": round(100 * joinable / main_rows, 6),
                "status": "不可用：回连率 0.0162%，产业归属无从谈起",
            },
            "D2_family_size": {
                "weight_in_formula": 0.5,
                "table": "gkx.dwd_patent(other_Versions) / gkx.dwd_patent_family",
                "prefix_sample": [ov_n, ov_filled],
                "family_rows": fam_rows,
                "status": "不可用：主表字段整列为空壳；family 表无申请人字段且只有 2 万行",
            },
        },
        "joined_diagnostic": {
            "n": len(detail) if detail else None,
            "ipc4_top": ipc_dist.most_common(15) if detail else None,
            "applicant_top": applicant_dist.most_common(15) if detail else None,
            "year_dist": dict(sorted(year_dist.items())) if detail else None,
            "industries_with_positive_cited": dict(industry_cov) if detail else None,
            "note": "即使把 475 件全部用上，也分散在数十个申请人/年份/IPC4 上，"
                    "单一产业不足 30 件，无法形成可解释的产业分",
        },
        "repair_requirements": [
            "补齐 dwd_patent_cited 全量（当前 20,515 行 vs 主表 2,939,895 行），并与 dwd_patent 统一 ID",
            "给 dwd_patent_cited 增加 first_applicant_name 或 applicant_id，避免回连主表",
            "给 dwd_patent.pn 建索引（当前无 pn 索引，任何按专利号回连都是全表扫描）",
            "补齐 dwd_patent.other_Versions 或提供 dwd_patent_family 全量 + 申请人字段",
        ],
        "base_year_block": C.base_year_block(
            [], [], "被引表无申请年字段且回连率 0.0162%，无法构造任何年度分母"),
        "gaps": [
            "dwd_patent_cited 仅覆盖主表 0.0162%",
            "dwd_patent.other_Versions 在前缀样本中 100% 空",
            "dwd_patent_family 仅 2 万行且无申请人字段",
            "pn 无索引，禁止按专利号回连 294 万行主表",
        ],
    }
    C.write_out(MID, res)
    print(json.dumps({k: res[k] for k in ("support_judgment", "probe", "dimension_status")},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
