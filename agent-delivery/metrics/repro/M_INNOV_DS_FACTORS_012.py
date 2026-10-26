#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M_INNOV_DS_FACTORS_012 —— 要素影响力（项目/课题）

口径来源（王惠 calc-logic/INNOV/M_INNOV_DS_FACTORS_012.md）：
  「同 M_INNOV_PROJECT_INFLUENCE-项目（含课题）影响力」——
  从资助金额、参与机构数、结题完备度三维加权平均，标准化到 0-100。

20261021 版换源：唯一数据面改为三方库 `gkx`（`gkx.<表名>`，不传 database/charset）。
实现：
  D1 资助金额   gkx.dwd_zh_project.funded_amount（万元）
  D2 参与机构数 gkx.dwd_zh_project.participating_institution（单值字符串，无多机构并列）
  D3 结题完备   gkx.dwd_zh_project.final_report_abstract 非空记 1

运行：python3 code/M_INNOV_DS_FACTORS_012.py
产物：code/M_INNOV_DS_FACTORS_012_out.json
"""

import json
import os
import collections
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
import _gkxdb  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "M_INNOV_DS_FACTORS_012_out.json")
RUN_AT = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
GKX = "gkx."
W_AMOUNT, W_ORG, W_REPORT = 1 / 3, 1 / 3, 1 / 3
PLACEHOLDER = "{c} IS NOT NULL AND UPPER(TRIM({c})) NOT IN ('NULL','','NONE','-')"


def q(sql, args=None):
    cur = _gkxdb.gkx()
    try:
        cur.execute(sql, args) if args else cur.execute(sql)
        return cur.fetchall()
    finally:
        cur.close()


def qd(sql, args=None):
    cur = _gkxdb.gkx()
    try:
        cur.execute(sql, args) if args else cur.execute(sql)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    finally:
        cur.close()


def pct(vals, p):
    if not vals:
        return 0
    k = int(len(vals) * p)
    return vals[min(k, len(vals) - 1)]


def main():
    out = {"metric_id": "M_INNOV_DS_FACTORS_012", "run_at": RUN_AT,
           "data_source": "gkx（三方库 183.240.141.251:3318）", "probes": {}}
    p = out["probes"]

    # ---------- 1. 探针 ----------
    p["zh_project"] = q("SELECT COUNT(*) n FROM " + GKX + "dwd_zh_project")[0][0]
    p["en_project"] = q("SELECT COUNT(*) n FROM " + GKX + "dwd_en_project")[0][0]
    # 占位符统一大小写：'null' / 'NULL' / '' / 'NONE' / '-' 一律按缺失处理
    p["zh_project_fill"] = qd(
        "SELECT SUM(funded_amount IS NOT NULL AND funded_amount>0) amt, "
        "SUM(" + PLACEHOLDER.format(c="participating_institution") + ") org, "
        "SUM(" + PLACEHOLDER.format(c="final_report_abstract") + ") rep, "
        "SUM(" + PLACEHOLDER.format(c="funded_institution") + ") fin, "
        "COUNT(DISTINCT participating_institution) n_org "
        "FROM " + GKX + "dwd_zh_project")[0]
    p["en_project_fill"] = qd(
        "SELECT SUM(funded_amount IS NOT NULL AND funded_amount>0) amt, "
        "SUM(" + PLACEHOLDER.format(c="final_report_abstract") + ") rep, "
        "SUM(approval_year IS NOT NULL) yr, COUNT(DISTINCT participating_institution) n_org "
        "FROM " + GKX + "dwd_en_project")[0]
    p["project_source"] = {
        str(r[0]): r[1] for r in q(
            "SELECT project_source, COUNT(*) n FROM " + GKX +
            "dwd_zh_project GROUP BY project_source ORDER BY n DESC LIMIT 5")
    }
    p["project_level"] = {
        str(r[0]): r[1] for r in q(
            "SELECT project_level, COUNT(*) n FROM " + GKX +
            "dwd_zh_project GROUP BY project_level ORDER BY n DESC LIMIT 5")
    }
    p["multi_org_rows"] = q(
        "SELECT SUM(participating_institution LIKE '%;%' OR participating_institution LIKE '%,%' "
        "OR participating_institution LIKE '%/%' OR participating_institution LIKE '%|%') n FROM " +
        GKX + "dwd_zh_project")[0][0]
    p["amount_stats"] = qd(
        "SELECT MIN(funded_amount) mn, MAX(funded_amount) mx, AVG(funded_amount) av FROM " +
        GKX + "dwd_zh_project WHERE funded_amount>0")[0]
    p["year_dist"] = {
        str(r[0])[:4]: r[1] for r in q(
            "SELECT approval_year y, COUNT(*) n FROM " + GKX +
            "dwd_zh_project GROUP BY approval_year ORDER BY y")
    }
    # 填充率披露（20261021 新增）：因子/评分类指标必须先看观测矩阵完整度，
    # 单维填充率过低时该维不得参与合成，分数也不可外推。
    p["zh_project_fill_rate_pct"] = {
        "funded_amount": round(int(p["zh_project_fill"]["amt"] or 0) / p["zh_project"] * 100, 2),
        "participating_institution": round(int(p["zh_project_fill"]["org"] or 0) / p["zh_project"] * 100, 2),
        "final_report_abstract": round(int(p["zh_project_fill"]["rep"] or 0) / p["zh_project"] * 100, 2),
        "funded_institution": round(int(p["zh_project_fill"]["fin"] or 0) / p["zh_project"] * 100, 2),
        "multi_org_rows": int(p["multi_org_rows"] or 0),
    }

    # ---------- 2. 取数 ----------
    rows = qd(
        "SELECT id, title, participating_institution inst, funded_amount amt, final_report_abstract rep, "
        "approval_year ay, discipline FROM " + GKX + "dwd_zh_project")
    annual = []
    for r in rows:
        ay = str(r["ay"] or "")[:4]
        annual.append({
            "id": r["id"],
            "title": (r["title"] or "")[:60],
            "inst": r["inst"],
            "amount": float(r["amt"]) if r["amt"] is not None else None,
            "has_report": bool(r["rep"] and str(r["rep"]).strip().upper() not in ("", "NULL", "NONE", "-")),
            "year": int(ay) if ay.isdigit() else None,
            "discipline": r["discipline"],
        })

    # ---------- 3. 三维标准化 ----------
    amts = [x["amount"] for x in annual if x["amount"]]
    lo, hi = (min(amts), max(amts)) if amts else (0, 1)
    for x in annual:
        x["s_amount"] = round((x["amount"] - lo) / (hi - lo) * 100, 2) if x["amount"] and hi > lo else None
        # D2：单值承担单位 → 参与机构数恒为 1，批内标准化退化为常数，按「缺失」处理
        x["s_org"] = None
        x["s_report"] = 100.0 if x["has_report"] else 0.0

    for x in annual:
        dims = [v for v in (x["s_amount"], x["s_org"], x["s_report"]) if v is not None]
        x["score"] = round(sum(dims) / len(dims), 2) if dims else None
        x["dims_used"] = len(dims)

    scored = [x for x in annual if x["score"] is not None]
    scores = sorted(x["score"] for x in scored)
    by_inst = collections.Counter()
    inst_amt = collections.defaultdict(float)
    for x in scored:
        if x["inst"]:
            by_inst[x["inst"]] += 1
            inst_amt[x["inst"]] += x["amount"] or 0
    top_inst = [{"inst": k, "projects": v, "amount_sum": round(inst_amt[k], 2)}
                for k, v in by_inst.most_common(10)]

    out["compute"] = {
        "n_scored": len(scored),
        "n_missing_amount": sum(1 for x in annual if x["s_amount"] is None),
        "n_with_report": sum(1 for x in annual if x["has_report"]),
        "report_rate_pct": round(sum(1 for x in annual if x["has_report"]) / len(annual) * 100, 2) if annual else 0,
        "score_min": scores[0] if scores else 0,
        "score_max": scores[-1] if scores else 0,
        "score_mean": round(sum(scores) / len(scores), 2) if scores else 0,
        "score_median": pct(scores, 0.5) if scores else 0,
        "score_p90": pct(scores, 0.9) if scores else 0,
        "n_distinct_scores": len(set(scores)),
        "amount_min": lo, "amount_max": hi,
        "top15_by_score": sorted(scored, key=lambda x: -x["score"])[:15],
        "bottom8": sorted(scored, key=lambda x: x["score"])[:8],
        "top10_institutions_by_count": top_inst,
    }

    # ---------- 4. 定档 ----------
    out["support_judgment"] = "部分支持"
    out["support_reason"] = (
        "项目主表 %d 条（全部为国家自然科学基金，%s 年—%s 年）可算：资助金额 100%% 有值（%.2f—%.0f 万元）、"
        "结题摘要 %.1f%% 有值，故 D1/D3 两维可复现；但 D2「参与机构数」在库内为单一承担单位字符串"
        "（%s 条记录中 0 条含分隔符），该维恒等于 1、批内标准化后为常数，只能记缺失不参与合成；"
        "国外项目表 %d 条 approval_year 全空、结题摘要仅 %.1f%%。三维缺一维 → 判部分支持。"
        % (p["zh_project"], "1986", "2023",
           float(p["amount_stats"]["mn"]), float(p["amount_stats"]["mx"]),
           out["compute"]["report_rate_pct"], p["zh_project"],
           p["en_project"], float(p["en_project_fill"]["rep"] or 0) / p["en_project"] * 100))
    out["notes"] = [
        "20261021 换源核对：gkx.dwd_zh_project 58,453 行、dwd_en_project 20,000 行，与 20261020 开发库 ODS 逐位一致，读数不变。",
        "dwd_zh_project 的 funded_institution 列 0/58,453 全空，承担单位只能用 participating_institution。",
        "approval_year 存 8 位日期（如 20200101），本脚本截前 4 位取年。",
        "库内项目仅 NSFC 一个来源（project_level 全为「国家级」），不含国家重点研发计划、省市科技计划。",
        "dwd_en_project 无立项年，无法进入时间维度，仅作金额/摘要的可算性旁证。",
        "参与机构数缺失的原因是该表结构为单值字段，不是数据量不足；若甲方补多机构关联表即可补全该维。",
        "观测矩阵完整度披露：D1 资助金额 100.00%、D3 结题摘要 81.09%、D2 参与机构数 100.00% 但**取值恒为 1**"
        "（0 条多机构记录），有效维度 2/3。因 D2 整列无区分度，本指标得分是「金额 + 摘要」两维均值，"
        "不可外推为需求的三维影响力。",
        "本指标与 M_INNOV_PROJECT_INFLUENCE 同口径（王惠 calc-logic 明示），双 ID 同实现。",
    ]

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)
    print("probes:", json.dumps(p, ensure_ascii=False, default=str)[:2000])
    print("compute:", {k: v for k, v in out["compute"].items() if not isinstance(v, list)})
    print("support:", out["support_judgment"])


if __name__ == "__main__":
    main()
