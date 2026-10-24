#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ORG_SZ_STATUS · 深圳科研机构现状解读（gkx 口径重建件，零 SQL）

需求锚点：产品需求 §1.1.1.2.4.2.4.4（深圳科研机构现状分析 / 评价框架配置 / 现状解读）

口径（照抄旧稿的「七维记分卡 + 省内四城对标 + 可得权重归一」）：
  D1 规模        = 机构家数
  D2 结构均衡    = (1 − Σ 机构类型份额²) × 100         （1-HHI，仅描述分散度）
  D3 成长        = 2021—2025 年登记新增家数
  D4 产出        = 有专利机构的专利件数均值
  D5 经费        = 有国基金项目机构的资助额均值（万元）
  D6 人才        = 有学者记录机构的学者数均值
  D7 领域覆盖    = 有任一证据（专利/论文/项目/学者）的机构占比
  维度分 = (值 − 0) / (四城最大值 − 0) × 100；标签 ≥90 优势 / 60—90 持平 / <60 短板
  综合现状指数 = Σ(权重×维度分) / Σ(可得维权重)（缺维不记 0、不进分母）

与旧稿的差异（一句话）：
  旧稿跑在演示库连接器 `_org_common.connect_ods()` 上，本件不 import 任何 helper，
  全部读本目录 gkx 落盘快照；「经费」维从国家自然科学基金资助额代理，仍不是全口径科研经费；
  「人才」维只覆盖 29/2,074 家，「领域」维不再用产业标签（技术标签仅命中 1 家），
  改为「有无证据」，产业切片降为缺口披露。

运行：cd code && python3 M_ORG_SZ_STATUS.py
产物：code/M_ORG_SZ_STATUS_out.json
"""
from __future__ import annotations

import json
import os
import statistics
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")

MID = "M_ORG_SZ_STATUS"
CITIES = ("深圳市", "广州市", "东莞市", "惠州市")
CITY_SHORT = {"深圳市": "深圳", "广州市": "广州", "东莞市": "东莞", "惠州市": "惠州"}

DIMS = [
    ("D1", "规模", "创新资源", 0.15),
    ("D2", "结构均衡", "组织发展环境", 0.10),
    ("D3", "成长", "研发活动", 0.15),
    ("D4", "产出", "创新产出", 0.20),
    ("D5", "经费", "研发活动", 0.15),
    ("D6", "人才", "创新资源", 0.15),
    ("D7", "证据覆盖", "组织发展环境", 0.10),
]
KEY = {"D1": "d1_scale", "D2": "d2_structure", "D3": "d3_growth", "D4": "d4_output",
       "D5": "d5_funding", "D6": "d6_talent", "D7": "d7_coverage"}


# ------------------------------------------------- 统计工具（内联自 _org_deep21_common.py）
def dist(vals):
    if not vals:
        return {"n": 0}
    s = sorted(vals)
    n = len(s)
    return {"n": n, "min": round(s[0], 2), "p25": round(s[int(n * .25)], 2),
            "median": round(statistics.median(s), 2), "mean": round(sum(s) / n, 2),
            "p75": round(s[int(n * .75)], 2), "p90": round(s[int(n * .9)], 2),
            "max": round(s[-1], 2)}


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    panel = load("org_family_panel_20261021.json")
    reg = load("org_reg_gkx21.json")
    inst = panel["institutions"]
    reg_by_id = {r["org_id"]: r for r in reg["rows"]}
    sz = [i for i in inst if i["city"] == "深圳市"]

    # ---------------- 1. 城市级维度值
    def city_vals(city):
        sub = [i for i in inst if i["city"] == city]
        n = len(sub)
        pat = [i["patents"] for i in sub if i["patents"] > 0]
        proj = [i["project_fund"] for i in sub if i["projects"] > 0]
        sch = [i["scholars"] for i in sub if i["scholars"] > 0]
        hh = [i["h_mean"] for i in sub if i["h_mean"] is not None]
        covered = sum(1 for i in sub
                      if i["patents"] > 0 or i["papers"] > 0 or i["projects"] > 0 or i["scholars"] > 0)
        new5 = sum(1 for i in sub if i.get("inc_year") and 2021 <= int(i["inc_year"]) <= 2025)
        tc = Counter(i.get("org_type") or "(空)" for i in sub)
        d2 = round((1 - sum((v / n) ** 2 for v in tc.values())) * 100, 2) if n else None
        return {
            "n": n,
            "d1_scale": n,
            "d2_structure": d2,
            "d2_types": dict(tc.most_common()),
            "d3_growth": new5,
            "d4_output": round(sum(pat) / len(pat), 2) if pat else None,
            "d4_output_patents": sum(pat),
            "d4_active": len(pat),
            "d5_funding": round(sum(proj) / len(proj), 2) if proj else None,
            "d5_projects": sum(i["projects"] for i in sub),
            "d5_inst": len(proj),
            "d6_talent": round(sum(sch) / len(sch), 2) if sch else None,
            "d6_scholars": sum(sch),
            "d6_inst": len(sch),
            "d6_avg_h": round(sum(hh) / len(hh), 2) if hh else None,
            "d7_coverage": round(covered / n * 100, 2) if n else None,
            "covered_orgs": covered,
        }

    cv = {c: city_vals(c) for c in CITIES}

    # ---------------- 2. 记分卡
    def score(v, best, worst=0.0):
        if v is None or best is None or best == worst:
            return None
        return round((v - worst) / (best - worst) * 100, 1)

    card = []
    for code, name, frame, w in DIMS:
        key = KEY[code]
        vals = {c: cv[c].get(key) for c in CITIES}
        avail = {c: v for c, v in vals.items() if v is not None}
        best = max(avail.values()) if avail else None
        szv = vals["深圳市"]
        sc = score(szv, best)
        rank = None
        if szv is not None and avail:
            rank = sorted(avail.values(), reverse=True).index(szv) + 1
        card.append({
            "code": code, "dim": name, "frame": frame, "weight": w,
            "sz_value": szv,
            "peer_values": {CITY_SHORT[c]: vals[c] for c in CITIES if c != "深圳市"},
            "best_city": max(avail, key=avail.get) if avail else None,
            "score": sc, "rank_in_4": rank,
            "label": None if sc is None else ("优势" if sc >= 90 else ("持平" if sc >= 60 else "短板")),
        })

    avail_w = sum(d["weight"] for d in card if d["score"] is not None)
    composite = {
        "index": round(sum(d["weight"] * d["score"] for d in card if d["score"] is not None)
                       / avail_w, 1) if avail_w else None,
        "weights_available": round(avail_w, 2),
        "dims_available": sum(1 for d in card if d["score"] is not None),
        "dims_total": len(DIMS),
        "missing_dims": [d["dim"] for d in card if d["score"] is None],
    }

    # ---------------- 3. 深圳结构画像
    cap = [reg_by_id[i["org_id"]]["capital_wan"] for i in sz
           if reg_by_id.get(i["org_id"], {}).get("capital_wan")]
    sz_profile = {
        "n": len(sz),
        "by_type": dict(Counter(i.get("org_type") or "(空)" for i in sz).most_common()),
        "by_year_recent": {str(y): sum(1 for i in sz if str(i.get("inc_year")) == str(y))
                           for y in range(2015, 2027)},
        "capital_pos": len(cap),
        "capital_median_wan": round(statistics.median(cap), 1) if cap else None,
        "capital_max_wan": round(max(cap), 1) if cap else None,
        "capital_dist": dist(cap),
        "geo_fill": sum(1 for i in sz if reg_by_id.get(i["org_id"], {}).get("address")),
        "reg_status": dict(Counter(reg_by_id.get(i["org_id"], {}).get("reg_status")
                                   for i in sz).most_common()),
        "name_pattern": dict(Counter(
            ("研究院" if "研究院" in i["name"] else
             "研究所" if "研究所" in i["name"] else
             "研究中心" if "研究中心" in i["name"] else
             "实验室" if "实验室" in i["name"] else
             "大学/学院" if ("大学" in i["name"] or "学院" in i["name"]) else "其他")
            for i in sz).most_common()),
    }

    # ---------------- 4. 机构级画像
    prof = []
    for i in sz:
        ev = sum([1 if i["patents"] > 0 else 0, 1 if i["papers"] > 0 else 0,
                  1 if i["projects"] > 0 else 0, 1 if i["scholars"] > 0 else 0])
        prof.append({
            "org_id": i["org_id"], "name": i["name"],
            "org_type": i.get("org_type"), "inc_year": i.get("inc_year"),
            "patents": i["patents"], "patent_grant": i["patent_grant"],
            "papers": i["papers"], "projects": i["projects"],
            "project_fund_wan": round(i["project_fund"], 2), "scholars": i["scholars"],
            "evidence_dims": ev,
        })
    institute_profile = {
        "n": len(prof),
        "evidence_dims_dist": {str(k): sum(1 for r in prof if r["evidence_dims"] == k)
                               for k in range(5)},
        "no_evidence": sum(1 for r in prof if r["evidence_dims"] == 0),
        "top20_by_patent": sorted([r for r in prof if r["patents"] > 0],
                                  key=lambda r: -r["patents"])[:20],
        "top10_by_funding": sorted([r for r in prof if r["project_fund_wan"] > 0],
                                   key=lambda r: -r["project_fund_wan"])[:10],
        "top10_by_paper": sorted([r for r in prof if r["papers"] > 0],
                                 key=lambda r: -r["papers"])[:10],
    }

    # ---------------- 5. 缺口量化
    szv = cv["深圳市"]
    coverage_pct = {
        "patents": round(szv["d4_active"] / szv["n"] * 100, 2),
        "projects": round(szv["d5_inst"] / szv["n"] * 100, 2),
        "scholars": round(szv["d6_inst"] / szv["n"] * 100, 2),
        "any_evidence": szv["d7_coverage"],
    }

    payload = {
        "metric_id": MID,
        "metric_name": "深圳科研机构现状解读",
        "domain": "TOPIC-ORG / 深圳科研机构现状分析",
        "support_judgment": "部分支持",
        "support_reason": (
            f"规模/结构/成长三维在 {szv['n']} 家深圳机构上可直接计算，四城同口径可比；"
            f"产出/经费/人才三维只对有证据子集可算：专利 {szv['d4_active']} 家、"
            f"国基金 {szv['d5_inst']} 家、学者 {szv['d6_inst']} 家，分别占深圳机构 "
            f"{coverage_pct['patents']}% / {coverage_pct['projects']}% / {coverage_pct['scholars']}%，"
            "且经费只是 NSFC 资助额、不是全口径科研经费；需求要求的「在该产业」切片无法闭合"
            "（机构×产业领域标签仅命中 1 家），只能给城市级总体现状。"
        ),
        "generated_at": "2026-10-22",
        "main_db": "gkx @ 183.240.141.251:3318（gkx_reader_zp，只读）",
        "sql_count": 0,
        "sources": [
            "code/_snapshots21/org_family_panel_20261021.json（2,074 家；专利/论文/项目/学者/转让/政策全在面板）",
            "code/_snapshots21/org_reg_gkx21.json（登记日期/开办资金/登记状态/地址）",
        ],
        "base_years_used": [2021, 2022, 2023, 2024, 2025],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": (
            "成长维只取 2021—2025 登记年（2026 为残年，不进分母）；专利件数为存量口径，"
            "库内申请年只覆盖 2021—2026，2017—2020 零行，未按 0 摊入。项目/论文/学者为截面总量，"
            "不设年度基期。"
        ),
        "probes": {
            "institute_total": len(inst),
            "sz_total": len(sz),
            "panel_coverage": panel.get("coverage", {}),
            "reg_rows": len(reg["rows"]),
            "capital_filled": sum(1 for r in reg["rows"] if r.get("capital_wan")),
        },
        "city_values": cv,
        "d2_note": ("结构均衡度 = (1 − Σ 机构类型份额²) × 100（1-HHI）；"
                    "仅描述类型分散程度，数值高不代表绩效好，也不表示事业单位占比越高越优。"
                    "深圳 1,014 家里民办非企业单位占比最高，是该市登记结构的特征，不是质量判据。"),
        "scorecard": card,
        "composite": composite,
        "sz_profile": sz_profile,
        "institute_profile": institute_profile,
        "coverage_pct": coverage_pct,
        "gaps": [
            "经费维：dwd_org_annual_financial_info 的研发费用列整列为空（§3.10），只能用 dwd_zh_project 的 NSFC 资助额代理，覆盖 53/2,074；",
            "人才维：dwd_scholar 21,316 人仅 147 人匹配到底册 29 家机构，深圳 2.86%，不能代表人才队伍；",
            "产出维：专利匹配靠申请人名称精确命中，219/2,074（10.56%），无统一社会信用代码列；",
            "产业切片：技术标签 32,322 家只命中 1 家，链标签 credit_code 与底册交集 3.5%（§3.1），无法按产业出报告；",
            "经济社会价值维（专利转让/技术合同）只有 10 家机构有转让记录，不构成城市级指标；",
            "底册 99.82% 在深圳都市圈（深圳+广州+东莞+惠州=188,774/189,116），省外 342 家，不能作全国对标。",
        ],
    }

    out = os.path.join(HERE, f"{MID}_out.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)

    print("wrote", os.path.basename(out))
    print("composite", composite)
    for d in card:
        print(f"  {d['code']} {d['dim']:<6} sz={d['sz_value']} best={d['best_city']} "
              f"score={d['score']} rank={d['rank_in_4']} {d['label']}")
    print("city n", {CITY_SHORT[c]: cv[c]["n"] for c in CITIES})
    print("coverage", coverage_pct)


if __name__ == "__main__":
    main()
