#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ORG_DEEP_155_1 · 科研机构扶持推荐模型（ORG 域）

需求锚点：bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/科研机构/深度分析.md 序号 155
  「多维度指标体系对科研机构进行定量化评估，涵盖科研成果水平、科研经费使用效率、人才队伍结构，
    为每个指标设定阈值，判定机构是否达到扶持标准，综合计算生成扶持推荐指数，
    用于衡量机构扶持优先级。」输出：扶持推荐指数 / 机构排名列表与分析。

本件口径（零 SQL）：
  C 成果水平   = pct_rank(log1p(近五年论文 + 2×专利授权 + 2×近五年项目 + 3×专利受让))
  E 经费效率   = pct_rank(近五年产出当量 / 项目经费万元 × 100)       —— 仅 53 家有经费
  T 人才结构   = pct_rank(log1p(学者数×3 + 工作经历人数) + h 均值/20) —— 仅 29 家有学者
  index = (0.45C + 0.30E + 0.25T) / Σ可用权重
  扶持标准 = C ≥ P75 且 E ≥ P50 且 T ≥ P50（三维都必须可得，缺一维即「无法判定」而不是「不达标」）

与 154 的关系：154 是「引入」（池 = 省内非深 1,060 家），155 是「扶持」（池 = 全部 2,074 家，
含深圳 1,014 家）。两者共用权重思路，但分母、阈值与语义不同，不能互相替代。

硬约束（必须披露，与派单书 §7 的 ORG 族硬缺口一致）：
  - 机构底册与工商注册库零交集：`dwd_org_annual_financial_info` 对 2,074 家命中 0 行，
    所以「营业收入 / 研发投入 / 研发人员数」三项全不可得，经费只能用项目资助额代替。
  - `development_employee`（研发人员数）整列为空，人才结构只能用学者库（29 家 / 145 人）。
  - 成果维的专利只有存量与授权数，没有年度序列；论文 2024 年为采集口径尖峰。
"""
from __future__ import annotations

import math
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _org_deep21_common as OC  # noqa: E402

MID = "M_ORG_DEEP_155_1"
RECENT = [2021, 2022, 2023, 2024, 2025]


def sum_years(d, years):
    return sum(int(v) for y, v in (d or {}).items() if str(y).isdigit() and int(y) in years)


def main() -> None:
    panel = OC.load_panel()
    inst = panel["institutions"]
    probe = OC.load_probe()

    rows = []
    for x in inst:
        p5 = sum_years(x.get("papers_year"), RECENT)
        j5 = sum_years(x.get("projects_year"), RECENT)
        out_raw = p5 + 2 * x["patent_grant"] + 2 * j5 + 3 * x["transfer_in"]
        fund = float(x.get("project_fund") or 0)
        t_raw = (math.log1p(x["scholars"] * 3 + x["people"])
                 + (x["h_mean"] or 0) / 20.0) if x["scholars"] else None
        rows.append({
            "name": x["name"], "city": x["city"], "org_type": x["org_type"],
            "inc_year": x.get("inc_year"), "capital_wan": x.get("registered_capital"),
            "papers_5y": p5, "projects_5y": j5, "patents": x["patents"],
            "patent_grant": x["patent_grant"], "transfer_in": x["transfer_in"],
            "projects": x["projects"], "fund_wan": round(fund, 1),
            "scholars": x["scholars"], "people": x["people"],
            "h_mean": x["h_mean"], "academicians": x["academicians"],
            "C_raw": math.log1p(out_raw),
            "E_raw": (out_raw / fund * 100) if fund > 0 else None,
            "T_raw": t_raw,
            "output_eq": out_raw,
        })

    avC = [r for r in rows if r["C_raw"] > 0]
    avE = [r for r in rows if r["E_raw"] is not None]
    avT = [r for r in rows if r["T_raw"] is not None]
    # pct_rank 一次性算，避免 O(n²)
    for key, subset, label in (("C", avC, "C_raw"), ("E", avE, "E_raw"), ("T", avT, "T_raw")):
        pr = OC.pct_rank([q[label] for q in subset])
        for q, v in zip(subset, pr):
            q[key] = round(v, 1)

    W = {"C": .45, "E": .30, "T": .25}
    for r in rows:
        parts = [(r[k], W[k]) for k in ("C", "E", "T") if r.get(k) is not None]
        wsum = sum(w for _, w in parts)
        r["index"] = round(sum(v * w for v, w in parts) / wsum, 2) if wsum else None
        r["n_dims"] = len(parts)

    scored = [r for r in rows if r["index"] is not None]
    scored.sort(key=lambda r: -r["index"])
    c75 = sorted(r["C"] for r in avC)[int(len(avC) * .75)]
    e50 = sorted(r["E"] for r in avE)[int(len(avE) * .50)]
    t50 = sorted(r["T"] for r in avT)[int(len(avT) * .50)]

    rec = [r for r in scored if r.get("C", 0) >= c75 and r.get("E") is not None and r["E"] >= e50
           and r.get("T") is not None and r["T"] >= t50]
    undecidable = [r for r in scored if r.get("C", 0) >= c75
                   and (r.get("E") is None or r.get("T") is None)]

    # 权重敏感性（只在三维齐全的机构上比较）
    full = [r for r in rows if r["n_dims"] == 3]
    base_rank = {r["name"]: r["index"] for r in full}
    sens = []
    for label, Wx in (("0.45/0.30/0.25（基准）", W),
                      ("成果优先 0.60/0.20/0.20", {"C": .60, "E": .20, "T": .20}),
                      ("效率优先 0.30/0.50/0.20", {"C": .30, "E": .50, "T": .20}),
                      ("人才优先 0.30/0.20/0.50", {"C": .30, "E": .20, "T": .50})):
        vals = [(r["name"], round(sum(r[k] * Wx[k] for k in ("C", "E", "T")), 2)) for r in full]
        vals.sort(key=lambda t: -t[1])
        sens.append({"weights": label,
                     "spearman_vs_base": OC_spearman([base_rank[n] for n, _ in vals], [v for _, v in vals]),
                     "top5": [n for n, _ in vals[:5]]})

    def card(r):
        return {"name": r["name"], "city": r["city"], "org_type": r["org_type"],
                "index": r["index"], "C": r.get("C"), "E": r.get("E"), "T": r.get("T"),
                "n_dims": r["n_dims"],
                **{k: r[k] for k in ("papers_5y", "projects_5y", "patent_grant", "transfer_in",
                                     "fund_wan", "projects", "scholars", "people", "h_mean",
                                     "academicians", "inc_year", "capital_wan")}}

    idx_vals = [r["index"] for r in scored]
    out = {
        "metric_id": MID,
        "metric_name": "科研机构扶持推荐模型",
        "domain": "ORG / 科研机构深度分析（序号 155）",
        "formula_owner": "AI-20261022（推测定义，wanghui=false）",
        "support_judgment": "部分支持",
        **OC.base_years(
            RECENT, [2017, 2018, 2019, 2020],
            "成果维取 2021—2025 五年窗口；专利为存量（库内 2021—2026，2017—2020 零行，"
            "缺失年不按 0 摊入）；2026 为残年不计入。经费为项目全周期累计资助额，与五年产出窗口"
            "并不对齐，这一点已在正文披露，只用于同口径排序。"),
        "inputs": {
            "org_roster": "gkx.dwd_research_institute_base_info 2,074 家",
            "outputs": "org_family_panel_20261021.json（papers_year / projects_year / 专利存量与授权）",
            "funding": "gkx.dwd_zh_project.funded_amount（58,452 行，机构匹配 581 项 / 53 家）",
            "talent": "gkx.dwd_scholar（21,316 人）+ dwd_scholar_work_experience（45,461 行）",
            "financial_table": "gkx.dwd_org_annual_financial_info 90,926 行（对底册命中 0 行）",
        },
        "coverage": {
            "institutes": len(rows),
            "with_output": len(avC),
            "with_funding": len(avE),
            "with_talent": len(avT),
            "with_all_three": len(full),
            "with_two_dims": sum(1 for r in rows if r["n_dims"] == 2),
            "rank_pool_2plus": sum(1 for r in rows if r["n_dims"] >= 2),
            "zero_all": sum(1 for r in rows if r["n_dims"] == 0),
            "scored": len(scored),
        },
        "dims": {
            "weights": W,
            "C": "pct_rank(log1p(近五年论文 + 2×专利授权 + 2×近五年项目 + 3×专利受让))",
            "E": "pct_rank(近五年产出当量 / 项目经费万元 × 100)",
            "T": "pct_rank(log1p(学者数×3 + 工作经历人数) + h 均值/20)",
            "E_caveat": "分子是 2021—2025 产出，分母是 1986—2023 项目累计资助额；"
                        "分母越厚的老所效率会被系统性压低，只能作同口径相对排序。",
            "T_caveat": "学者库对底册只命中 29 家 / 145 人；院士标记全库 112 人，底册只命中 1 人。",
        },
        "thresholds": {"C_p75": c75, "E_p50": e50, "T_p50": t50,
                       "rule": "C≥P75 且 E≥P50 且 T≥P50；缺维记「无法判定」，不记「不达标」。"},
        "index_dist": OC.dist(idx_vals),
        "top30": [card(r) for r in scored[:30]],
        "rank_2plus": [card(r) for r in scored if r["n_dims"] >= 2][:30],
        "full_dim_ranking": [card(r) for r in scored if r["n_dims"] == 3],
        "rank_note": "281 家有分：216 家只有成果维（C），50 家两维，15 家三维齐全。"
                     "只有一维的机构指数等于 C 的分位，不构成「扶持优先级」，"
                     "故主排名表只用 ≥2 维的 65 家，可判定池只用三维齐全的 15 家。",
        "recommended": [card(r) for r in rec],
        "undecidable": {
            "n": len(undecidable),
            "reason": "成果已达 P75，但经费效率或人才结构缺数据，无法判定是否达扶持标准。",
            "examples": [card(r) for r in undecidable[:20]],
        },
        "city_stat": {
            c: {"n": len([r for r in scored if r["city"] == c]),
                "in_recommended": len([r for r in rec if r["city"] == c]),
                "index_mean": round(sum(r["index"] for r in scored if r["city"] == c)
                                    / max(1, len([r for r in scored if r["city"] == c])), 2)}
            for c in ["深圳市", "广州市", "东莞市", "惠州市"]
        },
        "org_type_stat": {
            t: {"n": len([r for r in scored if r["org_type"] == t]),
                "in_recommended": len([r for r in rec if r["org_type"] == t])}
            for t in sorted({r["org_type"] for r in scored})
        },
        "sensitivity": sens,
        "limits": [
            "年报财务表对底册 2,074 家命中 0 行（org_id 与 external_id 均零交集），"
            "营业收入/资产/研发投入/研发人员四项全部不可得。",
            "`dwd_org_annual_financial_info.development_employee` 整列为空（90,926 行为 0 非空），"
            "研发人员数不可算。",
            "经费只能取项目资助额（53 家 / 581 项 / 27,908.2 万元），不含横向经费、财政拨款、"
            "单位自有资金，不能代表机构总研发经费。",
            "人才结构只覆盖 29 家（1.40%），且学者库以论文作者为主，医院/院所临床与工程人员不在内。",
            "无「扶持结果」标签（过去扶持了谁、效果如何），阈值是规则阈值，不是训练出来的分界线。",
        ],
        "probes": {k: probe.get(k) for k in ("fin_rows", "chg_head", "inst_fill")},
    }
    path = OC.write_out(out, MID)
    print("wrote", path)
    print("coverage", out["coverage"])
    print("thresholds", out["thresholds"])
    print("dist", out["index_dist"])
    print("rec", len(rec), [(r["name"], r["index"]) for r in rec[:10]])
    print("undecidable", len(undecidable))
    print("sens", [(s["weights"], s["spearman_vs_base"]) for s in sens])


def OC_spearman(a, b):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    ra, rb = ranks(a), ranks(b)
    ma, mb = sum(ra) / len(ra), sum(rb) / len(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    da = sum((x - ma) ** 2 for x in ra) ** .5
    db = sum((y - mb) ** 2 for y in rb) ** .5
    return round(num / (da * db), 4) if da and db else None


if __name__ == "__main__":
    main()
