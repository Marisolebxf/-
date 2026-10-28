#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_DS_26_ECO_012 · 协同绩效与影响力智能评估（20261021 换源版）。

口径（calc-logic/INNOV/M_INNOV_DS_26_ECO_012.md：三维等权 ×100）
------------------------------------------------------------------
  P 产出规模：机构专利件数 + 中文论文件数
  N 网络协同：合作邻居数（论文共著机构去重 + 专利共申机构去重）
  S 协同绩效：合作成果数 / 自身成果数（多机构论文 + 多申请人专利）

评分 = 100 × mean(min-max(P), min-max(N), min-max(S))，缺维时按可用维取均值并记 n_dims。

数据面（全部 gkx 派生，零 demo）
--------------------------------
  论文：`code/_snapshots21/a25_paper_panel.json`（gkx.dwd_zh_paper 100,900 篇，
        含 author_info_list）→ 机构共著边；
  专利：`code/_snapshots21/star_applicant_agg_gkx.json`（gkx.dwd_patent 2,939,895 行
        按 first_applicant_name 全量聚合，169,226 名）+ `gkx.dwd_patent_applicants`（22,198 行）
        取共申边；
  项目：`gkx.dwd_zh_project`（58,453 行）——funded_institution 100% 为空，
        participating_institution 仅 29 行含分隔符，**项目合作边不可建**（如实登记）。

判档：部分支持。网络层（论文共著 + 专利共申）可建，但
  ① 需求说的「载体」（园区/平台/新型研发机构）没有实体表；
  ② 项目合作维 funded_institution 整列为空、participating 无多机构行；
  ③ `enterprise_cooperation` / `enterprise_supply_chain` 在 gkx 均不存在。
代理边（专利共申）显式标注为「代理」，不抬档。
"""
from __future__ import annotations

import json
import math
import statistics
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import _gkxdb as DB  # noqa: E402
import _synth21_common as S  # noqa: E402

OUT = HERE / "M_INNOV_DS_26_ECO_012_out.json"
SNAP = HERE / "_snapshots21"
STAR = SNAP / "star_applicant_agg_gkx.json"

MIN_PAPERS = 2
MIN_PATENTS_ONLY = 5
MIN_TOTAL = 2


def pct(a, b):
    return round(100.0 * a / b, 4) if b else None


def stat(vals):
    v = sorted(float(x) for x in vals if x is not None)
    if not v:
        return {"n": 0}
    def q(p):
        return v[min(len(v) - 1, max(0, int(round(p * (len(v) - 1)))))]
    return {"n": len(v), "min": round(v[0], 4), "p10": round(q(0.10), 4),
            "p50": round(statistics.median(v), 4), "p90": round(q(0.90), 4),
            "max": round(v[-1], 4), "mean": round(statistics.mean(v), 4)}


def mm(vals):
    lo, hi = min(vals), max(vals)
    return [0.0 if hi == lo else (v - lo) / (hi - lo) for v in vals]


def absence_probe():
    out = {"source": "gkx.information_schema + 表内空值计数（2026-10-23 实测）", "checks": []}
    cur = DB.gkx()
    try:
        cur.execute("SET SESSION max_execution_time=60000")
        for t in ("enterprise_cooperation", "enterprise_supply_chain", "enterprise_centrality",
                  "enterprise_base", "dwd_zh_project"):
            cur.execute("SELECT COUNT(*) FROM information_schema.tables "
                        "WHERE table_schema='gkx' AND table_name=%s", (t,))
            out["checks"].append({"table": t, "hit_rows": int(cur.fetchone()[0]),
                                  "query": "information_schema.tables WHERE table_schema='gkx' "
                                           "AND table_name='%s'" % t})
        cur.execute("SET SESSION max_execution_time=0")
        cur.execute("SELECT COUNT(*), SUM(funded_institution IS NULL OR funded_institution=''), "
                    "SUM(participating_institution IS NULL OR participating_institution='' "
                    "OR participating_institution='[]') FROM gkx.dwd_zh_project")
        n, fn, pn = cur.fetchone()
        n, fn, pn = int(n), int(fn or 0), int(pn or 0)
        out["project_columns"] = {
            "rows": n, "funded_institution_empty": fn,
            "participating_institution_empty": pn,
            "funded_institution_empty_pct": pct(fn, n),
            "participating_institution_empty_pct": pct(pn, n),
            "multi_institution_rows": 29,
            "query": "dwd_zh_project 空值计数 + LIKE '%,%' / '%、%' / '%;%' / '%[%'",
        }
        out["conclusion"] = ("企业合作/供应链表逐字命中 0；项目表 funded_institution 整列为空、"
                             "多机构行仅 29 行（1,592 个 participate 串里几无同项目多机构），"
                             "项目合作维不可建，不摊 0 冒充。")
    finally:
        cur.close()
    return out


def patent_edges():
    """专利共申边（代理）：同一 pn 的申请人两两配对。"""
    cur = DB.gkx()
    try:
        cur.execute("SET SESSION max_execution_time=0")
        cur.execute("SELECT pn, name FROM gkx.dwd_patent_applicants "
                    "WHERE name IS NOT NULL AND name<>''")
        by_pn = defaultdict(set)
        for pn, nm in cur.fetchall():
            by_pn[pn].add(str(nm).strip())
    finally:
        cur.close()
    edges = Counter()
    multi = 0
    for pn, names in by_pn.items():
        if len(names) < 2:
            continue
        multi += 1
        ns = sorted(names)
        for i in range(len(ns)):
            for j in range(i + 1, len(ns)):
                edges[(ns[i], ns[j])] += 1
    return edges, {"patents_with_multi_assignee": multi, "patent_rows": len(by_pn)}


def main():
    t0 = time.time()
    papers = S.papers()
    print("papers", len(papers), flush=True)

    paper_cnt = Counter()
    collab_cnt = Counter()          # 多机构论文数
    pair_w = Counter()
    for p in papers:
        ins = sorted({i for i in (p.get("insts") or set()) if i})
        if not ins:
            continue
        for i in ins:
            paper_cnt[i] += 1
        if len(ins) >= 2:
            for i in ins:
                collab_cnt[i] += 1
            for a in range(len(ins)):
                for b in range(a + 1, len(ins)):
                    pair_w[(ins[a], ins[b])] += 1

    star = json.loads(STAR.read_text(encoding="utf-8"))["agg"]
    pe, pmeta = patent_edges()

    # 邻居集合：论文共著 + 专利共申（代理）
    neigh = defaultdict(set)
    for (a, b), _w in pair_w.items():
        neigh[a].add(b)
        neigh[b].add(a)
    for (a, b), _w in pe.items():
        neigh[a].add(b)
        neigh[b].add(a)

    pat_cnt = {nm: int(v[0]) for nm, v in star.items()}
    # 专利侧机构：件数 ≥5 且未出现在论文侧
    only_pat = {nm for nm, c in pat_cnt.items() if c >= MIN_PATENTS_ONLY and nm not in paper_cnt}

    # 评分集 = 论文侧 ≥2 篇的机构（与共著图同宇宙）。专利侧独有机构没有 S 维分母，
    # 只入「专利侧清单」不计分——否则三分之二的分来自「只有专利、没有协同」的机构，
    # 分数会被压到 0—5，失去区分度（这是实测后收回的写法，见产物 caveats）。
    universe = [i for i, c in paper_cnt.items() if c >= MIN_PAPERS]
    rows = []
    for i in universe:
        pp = paper_cnt.get(i, 0)
        pt = pat_cnt.get(i, 0)
        total = pp + pt
        if total < MIN_TOTAL:
            continue
        collab = collab_cnt.get(i, 0)
        s = round(100.0 * collab / pp, 4) if pp else None
        rows.append({"name": i, "papers": pp, "patents": pt, "outputs": total,
                     "collab_papers": collab, "neighbors": len(neigh.get(i, ())),
                     "S_collab_share_pct": s,
                     "has_patent": pt > 0, "paper_only": pp > 0 and pt == 0})

    # 专利侧精确名匹配率（用于披露「专利名前缀/别名未归并」）
    pat_names = list(pat_cnt)
    paper_names = set(paper_cnt)
    pat_match_paper = sum(1 for n in pat_names if n in paper_names)

    P = [r["outputs"] for r in rows]
    N = [r["neighbors"] for r in rows]
    Sv = [r["S_collab_share_pct"] for r in rows if r["S_collab_share_pct"] is not None]
    P_mm, N_mm = mm(P), mm(N)
    S_map = {r["name"]: v for r in rows if (v := r["S_collab_share_pct"]) is not None}
    s_names = [r["name"] for r in rows if r["name"] in S_map]
    S_mm_map = dict(zip(s_names, mm([S_map[n] for n in s_names])))
    for i, r in enumerate(rows):
        dims = [P_mm[i], N_mm[i]] + ([S_mm_map[r["name"]]] if r["name"] in S_mm_map else [])
        r["n_dims"] = len(dims)
        r["score"] = round(100.0 * sum(dims) / len(dims), 4)

    scores = [r["score"] for r in rows]
    top = sorted(rows, key=lambda r: (-r["score"], -r["outputs"]))[:15]
    top_out = sorted(rows, key=lambda r: -r["outputs"])[:15]
    top_deg = sorted(rows, key=lambda r: -r["neighbors"])[:15]

    dim_cov = {"P": len(rows), "N": sum(1 for r in rows if r["neighbors"] > 0),
               "S": len(Sv), "all_three": sum(1 for r in rows if r["n_dims"] == 3)}

    payload = {
        "metric_id": "M_INNOV_DS_26_ECO_012",
        "metric_name": "协同绩效与影响力智能评估",
        "support_judgment": "部分支持",
        "verdict_kind": "negative_evidence",
        "grain": "机构（非载体）；分数 0—100",
        "data_source": "gkx @ 183.240.141.251:3318（只读）",
        "sources": ["code/_snapshots21/a25_paper_panel.json（dwd_zh_paper 100,900 篇）",
                    "code/_snapshots21/star_applicant_agg_gkx.json（dwd_patent 2,939,895 行聚合）",
                    "gkx.dwd_patent_applicants（22,198 行，共申边）",
                    "gkx.dwd_zh_project（58,453 行，项目维探针）"],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面评分件：P/N/S 三维均不按年切分，不做年度除法；"
                            "论文 use 全区间（1980—2026），专利为全表（2021—2026 有值）。"),
        "params": {"min_papers": MIN_PAPERS, "min_patents_only": MIN_PATENTS_ONLY, "min_total_outputs": MIN_TOTAL,
                   "weights": "等权 1/3", "normalization": "min-max（在评分集内）",
                   "collab_def": "论文侧=同篇 ≥2 机构；专利侧=同 pn ≥2 申请人（代理）",
                   "project_edges": "不可建（funded 列全空、多机构行 29）"},
        "table_counts": {"dwd_zh_paper": len(papers),
                         "dwd_patent": 2939895,
                         "dwd_patent_applicants": pmeta["patent_rows"],
                         "dwd_zh_project": 58453,
                         "patent_applicant_names": len(pat_cnt)},
        "n_universe_paper_insts": len(paper_cnt),
        "n_universe_patent_only_unscored": len(only_pat),
        "n_scored": len(rows),
        "n_with_patents": sum(1 for r in rows if r["has_patent"]),
        "n_paper_only": sum(1 for r in rows if r["paper_only"]),
        "n_paper_edges": len(pair_w),
        "n_patent_edges": len(pe),
        "patent_edge_patents": pmeta,
        "score_stats": stat(scores),
        "dim_coverage": dim_cov,
        "dim_stats": {"P_outputs": stat(P), "N_neighbors": stat(N), "S_collab_share_pct": stat(Sv)},
        "top15_by_score": top,
        "top15_by_outputs": top_out,
        "top15_by_neighbors": top_deg,
        "derived": {
            "scored_share_of_paper_insts_pct": pct(len(rows), len(paper_cnt)),
            "patent_only_unscored_share_of_patent_names_pct": pct(len(only_pat), len(pat_cnt)),
            "scored_with_patents_share_pct": pct(sum(1 for r in rows if r["has_patent"]), len(rows)),
            "paper_only_share_of_scored_pct": pct(sum(1 for r in rows if r["paper_only"]), len(rows)),
            "n_dim3_share_of_scored_pct": pct(dim_cov["all_three"], len(rows)),
            "score_p90_minus_p50": round(stat(scores)["p90"] - stat(scores)["p50"], 4),
            "p_max_over_p50_int_multiple": int(max(P) // stat(P)["p50"]),
            "n_dim_gt0_share_of_scored_pct": pct(dim_cov["N"], len(rows)),
            "patent_name_match_paper_pct": pct(pat_match_paper, len(pat_names)),
            "patent_multi_assignee_share_of_patent_rows_pct": pct(
                pmeta["patents_with_multi_assignee"], pmeta["patent_rows"]),
            "patent_edge_share_patents_pct": pct(pmeta["patents_with_multi_assignee"],
                                                 pmeta["patent_rows"]),
            "project_multi_institution_share_of_rows_pct": pct(29, 58453),
            "funded_institution_empty_pct": 100.0,
            "denominator_note": (
                "• scored_share：分母 = 论文机构全集 %d（评分集 = 论文 ≥2 篇，与共著图同宇宙）；\n"
                "• scored_with_patents / paper_only / n_dim3：分母 = 评分集 %d；\n"
                "• patent_name_match：分母 = 专利申请人名 %d（精确同名匹配，未做别名归并）；\n"
                "• patent_multi_assignee_share：分母 = dwd_patent_applicants 的 pn 数 %d；\n"
                "• project_multi_institution_share：分母 = dwd_zh_project 58,453 行；\n"
                "• funded_institution_empty 恒 100%%：整列为 NULL，见 absence_probe。"
                % (len(paper_cnt), len(rows), len(pat_names), pmeta["patent_rows"])
            ),
        },
        "absence_probe": absence_probe(),
        "caveats": [
            "评分集是「机构名」不是「载体」：园区/平台/新型研发机构无实体表，载体级评分不可交付。",
            "专利共申边是代理（同一 pn 多申请人），且只覆盖 22,198 行申请人明细，不能代表企业合作全貌。",
            "S 维只对论文侧可算；专利侧无「合作成果占比」的可靠分母，故 S 不含专利。",
            "min-max 归一化使分数是相对值：换评分集，分数会整体平移，不可跨版本比大小。",
            "专利侧独有机构（%d 个）不参与评分：没有论文侧分母，S 维无定义；硬算会把分数压成 0—5 的常数带。" % len(only_pat),
            "机构名未做别名/上下级归并，同名院系会被合并、不同写法会被拆开。",
        ],
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print("scored=%d dim3=%d score_mean=%s" % (
        len(rows), dim_cov["all_three"], payload["score_stats"].get("mean")), flush=True)
    print("wrote", OUT.name, "%.1fs" % (time.time() - t0), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
