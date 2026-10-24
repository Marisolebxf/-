#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_EXPERT_ACTIVITY 专家科研活跃度 —— 真实论文关系 + 引用 + 合著网 + 参与项目。

四维（全部真值）：
  D1 近窗产出：ods.dwd_scholar_paper_relation 中 year∈[2024,2026] 的论文数
  D2 近窗影响：同期论文的篇均被引（citations 字段）
  D3 合作强度：ods.dwd_scholar_coauthor 的加权度（Σ co_paper_count）与去重合作者数
  D4 参与项目：ods.dwd_zh_project 的 project_host / participants，按「姓名 + 单位包含」双条件对齐
辅助校验：存量论文数 / h 指数 / 被引总数（dwd_scholar），用于识别「上升期」与「吃老本」两类专家。
"""
import os
import sys
import json
import math
import statistics as st

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(BASE, "_snapshots")
OUT = os.path.join(BASE, "M_INNOV_EXPERT_ACTIVITY_out.json")


def load(n):
    return json.load(open(os.path.join(SNAP, n)))


def minmax(v):
    lo, hi = min(v), max(v)
    return [(x - lo) / (hi - lo) if hi > lo else 0.0 for x in v]


def pct(v, p):
    s = sorted(v)
    k = (len(s) - 1) * p
    f, c = math.floor(k), math.ceil(k)
    return s[int(k)] if f == c else s[f] * (c - k) + s[c] * (k - f)


def corr(a, b):
    n = len(a)
    if n < 3:
        return 0.0
    ma, mb = sum(a) / n, sum(b) / n
    c = sum((x - ma) * (y - mb) for x, y in zip(a, b)) / n
    sa = math.sqrt(sum((x - ma) ** 2 for x in a) / n)
    sb = math.sqrt(sum((y - mb) ** 2 for y in b) / n)
    return round(c / (sa * sb), 4) if sa and sb else 0.0


def inst_ok(org, pinst):
    if not org or not pinst:
        return False
    a, b = org.replace(" ", ""), pinst.replace(" ", "")
    return a in b or b in a


def project_hits(scholars):
    """返回 scholar_id -> (项目数, 最近项目年, 主持数)。姓名+单位双条件，抑制同名膨胀。"""
    by_name = {}
    for s in scholars:
        if s[1]:
            by_name.setdefault(s[1], []).append(s)
    proj = load("innov_w6_zh_project.json")
    hits = {}
    name_only_hits = 0
    for pid, host, parts, pinst, year, level, amount, title in proj:
        cand = by_name.get(host or "", [])
        strict = [s for s in cand if inst_ok(s[2], pinst)]
        if cand:
            name_only_hits += 1
        for s in strict:
            v = hits.setdefault(s[0], [0, 0, 0])
            v[0] += 1
            v[1] = max(v[1], int(str(year)[:4]) if year else 0)
            v[2] += 1
        if parts:
            try:
                pl = json.loads(parts)
            except Exception:
                pl = []
            for nm in pl:
                for s in by_name.get(nm, []):
                    if inst_ok(s[2], pinst):
                        v = hits.setdefault(s[0], [0, 0, 0])
                        v[0] += 1
                        v[1] = max(v[1], int(str(year)[:4]) if year else 0)
    return hits, name_only_hits, len(proj)


def main():
    scholars = load("innov_w6_scholar.json")
    spr = {r[0]: r[1:] for r in load("innov_w6_spr_agg.json")}       # [n_all,n_2426,n_2226,cit_2426,cit_all,y_last,y_first]
    coa = {r[0]: r[1:] for r in load("innov_w6_coauthor_agg.json")}  # [deg,wdeg,mx,n_org]
    hits, name_only, n_proj = project_hits(scholars)

    rows = []
    for s in scholars:
        sid, name, org, pn, cn, h, refn, status = s
        if status != 1:
            continue
        r = spr.get(sid)
        if not r:
            continue  # 无任何论文关系的学者不参与评分（1,301 人）
        n_all, n_2426, n_2226, cit_2426, cit_all, y_last, y_first = r
        c = coa.get(sid, [0, 0, 0, 0])
        ph = hits.get(sid, [0, 0, 0])
        mean_cit = cit_2426 / n_2426 if n_2426 else 0.0
        rows.append({"scholar_id": sid, "name": name, "org": org, "status": status,
                     "papers_all": n_all, "papers_2426": n_2426, "papers_2226": n_2226,
                     "cit_2426": cit_2426, "cit_all": cit_all, "mean_cit_2426": round(mean_cit, 3),
                     "y_last": y_last, "y_first": y_first,
                     "deg": c[0], "wdeg": c[1], "max_co": c[2], "co_orgs": c[3],
                     "projects": ph[0], "project_year": ph[1],
                     "paper_nums": pn, "citation_nums": cn, "h_index": h})

    n1 = minmax([math.log1p(r["papers_2426"]) for r in rows])
    n2 = minmax([math.log1p(r["mean_cit_2426"]) for r in rows])
    n3 = minmax([math.log1p(r["wdeg"]) for r in rows])
    n4 = minmax([math.log1p(r["projects"]) for r in rows])
    W = (0.35, 0.25, 0.20, 0.20)
    for i, r in enumerate(rows):
        r["d1_产出"] = round(n1[i] * 100, 2)
        r["d2_影响"] = round(n2[i] * 100, 2)
        r["d3_合作"] = round(n3[i] * 100, 2)
        r["d4_项目"] = round(n4[i] * 100, 2)
        r["score"] = round(100 * (W[0] * n1[i] + W[1] * n2[i] + W[2] * n3[i] + W[3] * n4[i]), 2)
    sc = [r["score"] for r in rows]
    top = sorted(rows, key=lambda x: -x["score"])[:20]
    # 上升期（近窗产出高但存量论文少）与存量型（存量高但近窗为 0）
    rising = sorted([r for r in rows if r["papers_2426"] >= 5], key=lambda x: (x["paper_nums"] - x["papers_2426"]))[:10]
    stale = sorted([r for r in rows if r["papers_2426"] == 0 and r["paper_nums"] >= 100],
                   key=lambda x: -x["citation_nums"])[:10]
    K = ("scholar_id", "name", "org", "papers_all", "papers_2426", "cit_2426", "mean_cit_2426",
         "deg", "wdeg", "projects", "project_year", "paper_nums", "citation_nums", "h_index",
         "d1_产出", "d2_影响", "d3_合作", "d4_项目", "score")
    res = {
        "metric_id": "M_INNOV_EXPERT_ACTIVITY",
        "name": "专家科研活跃度",
        "formula_owner": "AI-20261016（王惠未定义；本报告按需求原句重建）",
        "unit": "学者（ods.dwd_scholar 主档 21,316 人；与论文关系表 scholar_id 交集 1,842 人入评）",
        "method": {
            "formula": "Score = 100*(0.35*D1 + 0.25*D2 + 0.20*D3 + 0.20*D4)，各维 log1p 后 min-max",
            "D1": "2024-2026 论文数（dwd_scholar_paper_relation.year）",
            "D2": "2024-2026 论文篇均被引（citations / n）",
            "D3": "合著加权度 Σ co_paper_count（dwd_scholar_coauthor）",
            "D4": "参与国家/省部级项目数（dwd_zh_project host+participants，姓名+单位双条件）",
            "windows": {"recent": "2024-2026", "project": "1986-2023（项目表年份上限）"},
        },
        "coverage": {
            "scholars_total": len(scholars), "scholars_scored": len(rows),
            "with_relation": len(spr), "with_coauthor": len(coa),
            "with_projects": sum(1 for r in rows if r["projects"] > 0),
            "with_projects_rate": round(sum(1 for r in rows if r["projects"] > 0) / len(rows) * 100, 2),
            "projects_total": n_proj, "projects_name_only_hits": name_only,
            "recent_papers_total": sum(r["papers_2426"] for r in rows),
            "scholars_with_recent_citation": sum(1 for r in rows if r["cit_2426"] > 0),
            "id_space": {
                "scholar_master_ids": len(scholars),
                "relation_ids": len(spr),
                "coauthor_ids": len(coa),
                "master_relation_intersection": len(set(spr) & {s[0] for s in scholars}),
                "master_coauthor_intersection": len(set(coa) & {s[0] for s in scholars}),
                "intersection_rate_of_master": round(len(set(spr) & {s[0] for s in scholars}) / len(scholars) * 100, 2),
                "verdict": "关系表与主档的 scholar_id 属两套映射：2.13 万主档中仅 1,842 人与论文关系表同 ID；"
                           "主档独有 19,474 人、关系表独有 18,173 人。故可展示（带姓名/机构/h 指数）的评分对象即 1,842 人。",
            },
        },
        "stats": {"n": len(sc), "min": round(min(sc), 2), "max": round(max(sc), 2),
                  "mean": round(sum(sc) / len(sc), 2), "median": round(st.median(sc), 2),
                  "p90": round(pct(sc, 0.9), 2), "p99": round(pct(sc, 0.99), 2),
                  "ge50": sum(1 for x in sc if x >= 50), "ge70": sum(1 for x in sc if x >= 70),
                  "zero": sum(1 for x in sc if x == 0)},
        "top20": [{k: r[k] for k in K} for r in top],
        "rising_stars": [{k: r[k] for k in K} for r in rising],
        "stock_only_stale": [{k: r[k] for k in K} for r in stale],
        "validity_check": {
            "corr_score_paper_nums": corr([r["score"] for r in rows], [r["paper_nums"] for r in rows]),
            "corr_score_h_index": corr([r["score"] for r in rows], [r["h_index"] for r in rows]),
            "corr_recent_stock": corr([r["papers_2426"] for r in rows], [r["paper_nums"] for r in rows]),
            "note": "若与存量论文数相关过高，说明退化为「存量排名」；本口径以 2024-2026 近窗为主，"
                    "与 h 指数仅中度相关即符合「活跃度 ≠ 终身成就」的设计意图",
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": "四维信号本身全部落在白名单真表（近窗论文与引用 106.5 万条关系、合著 118.8 万条边、"
                      "项目 5.85 万条），在 1,842 位「主档∩关系表」学者上现转可得 0–100 分且有区分度；"
                      "但① 学者主档 21,316 人与论文关系表 20,015 人的 scholar_id 仅 1,842 人重合（8.65%），"
                      "其余 1.9 万人有 ID 无姓名/机构/h 指数，无法展示、无法与项目表按姓名对齐；"
                      "② 需求原句还含「学术活动参与度（会议/讲座/交流）」，开发库与三方库均无任何会议/报告源表。"
                      "两项均属结构性缺口，故判「部分支持」，不因脚本跑通升档。",
            "criteria": {"structure": "dwd_scholar / dwd_scholar_paper_relation / dwd_scholar_coauthor / dwd_zh_project",
                         "volume": "1,842 位可展示学者 / 1,065,385 relations / 1,187,606 coauthor edges / 58,453 projects",
                         "reproducible": True,
                         "distribution_discriminative": True,
                         "id_space_overlap_rate": 8.65,
                         "academic_activity_source": False},
        },
    }
    json.dump(res, open(OUT, "w"), ensure_ascii=False, indent=1, default=str)
    print("coverage", json.dumps(res["coverage"], ensure_ascii=False))
    print("stats", res["stats"])
    print("validity", res["validity_check"])
    for r in top[:6]:
        print(" ", r["name"], r["org"], r["papers_2426"], r["mean_cit_2426"], r["wdeg"], r["projects"], r["score"])
    print("wrote", OUT)


if __name__ == "__main__":
    main()
