#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_TALENT_INDUSTRY_SCORE —— 人才产业力指数（TALENT 展示面 §1.1.1.2.4.2.5.8）

口径：需求四维（产业关联论文 IND 0.35 / 学术深度 H 0.25 / 专利产出 PAT 0.20 /
产学研触点 LINK 0.20，权重为派单给定）。打分池 = gkx.dwd_scholar 全池有姓名者（20,420 名）。

产业方向按《深圳市「20+8」产业集群》21 类建立中英双语关键词字典（见 _talent21_common.CLUSTERS），
论文命中走「关键词 + 标题」双字段，作者记录先做「姓名 + 机构前缀」双锚定再计簇，
避免同名把他人论文算到本人头上。四维缺一维按可得维重归一分母，不补 0。

零 SQL、零 demo 表：纸面数据读 `_snapshots21/a25_paper_panel.json`（100,900 篇全量解析），
专利读 `_snapshots21/patent_inventor_counts_gkx.json`。
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _talent21_common import (  # noqa: E402
    CLUSTERS, anchored_papers, is_enterprise, is_sz, log_minmax, name_dup,
    name_papers, paper_clusters, paper_insts, patent_of, scholars, spearman, st, work, write_out,
)

METRIC = "M_TALENT_INDUSTRY_SCORE"
W = {"IND": 0.35, "H": 0.25, "PAT": 0.20, "LINK": 0.20}


def tier_of(x: float) -> str:
    return "产业强关联" if x >= 60 else ("产业中关联" if x >= 30 else "产业弱关联")


def main() -> None:
    sch = [s for s in scholars() if s["name"]]
    n = len(sch)

    # ---------------- IND：产业关联论文（姓名+机构双锚定） ----------------
    ind_cnt: dict[str, int] = {}
    cl_papers: dict[str, Counter] = {}
    cl_names: dict[str, list[str]] = {c: [] for c in CLUSTERS}
    all_papers = 0
    anchor_papers_total = 0
    for s in sch:
        ps = anchored_papers(s)
        anchor_papers_total += len(ps)
        cc: Counter = Counter()
        for p in ps:
            cl = paper_clusters(p["pid"], p["kw"], p["ti"])
            for c in cl:
                cc[c] += 1
                cl_names[c].append(s["name"])
        ind_cnt[s["sid"]] = sum(cc.values())
        cl_papers[s["sid"]] = cc
        all_papers += len(ps)

    # ---------------- H / PAT ----------------
    zh = log_minmax([s["h"] for s in sch])
    pat: dict[str, tuple[int | None, str]] = {s["sid"]: patent_of(s) for s in sch}
    pat_vals = [v for v, _ in pat.values() if v is not None]
    pz = log_minmax([float(v) for v in pat_vals]) if pat_vals else []
    pat_scale = dict(zip([s["sid"] for s in sch if pat[s["sid"]][0] is not None], pz))

    # ---------------- LINK：产学研触点 ----------------
    wx = work()
    w_sids = {r["sid"] for r in wx}
    ent_work = {r["sid"] for r in wx if r["org"] and is_enterprise(r["org"])}
    ent_paper: set[str] = set()
    sz_paper: set[str] = set()
    for s in sch:
        ps = anchored_papers(s)
        insts = set()
        for p in ps:
            insts.update(paper_insts().get(p["pid"], []))
        if any(inst and is_enterprise(inst) for inst in insts):
            ent_paper.add(s["sid"])
        if any(inst and is_sz(inst) for inst in insts):
            sz_paper.add(s["sid"])

    # ---------------- 合成 ----------------
    zind = log_minmax([float(ind_cnt[s["sid"]]) for s in sch])
    score: list[float] = []
    comp: dict[str, dict[str, float | None]] = {}
    tag_counter: Counter = Counter()
    dims_hist: Counter = Counter()
    link_bits_hist: Counter = Counter()
    for i, s in enumerate(sch):
        sid = s["sid"]
        bits = [1.0 if sid in ent_work else 0.0,
                1.0 if sid in ent_paper else 0.0,
                1.0 if sid in sz_paper else 0.0]
        link = sum(bits) / 3 if sid in w_sids or sid in ent_paper or sid in sz_paper else None
        if link is not None:
            link_bits_hist[int(sum(bits))] += 1
        c = {"IND": zind[i], "H": zh[i], "PAT": pat_scale.get(sid), "LINK": link}
        comp[sid] = c
        pv = pat[sid]
        tag_counter[pv[1]] += 1
        pairs = [(W[k], v) for k, v in c.items() if v is not None]
        dims_hist[len(pairs)] += 1
        den = sum(w for w, _ in pairs)
        score.append(100 * sum(w * float(v) for w, v in pairs) / den if den else 0.0)

    order = sorted(range(n), key=lambda i: (-score[i], sch[i]["sid"]))

    def row(i: int) -> dict:
        s = sch[i]
        cc = cl_papers[s["sid"]]
        return {"rank": 0, "name": s["name"], "org": s["org"], "score": round(score[i], 2),
                "comp": {k: (round(float(v), 2) if v is not None else None) for k, v in comp[s["sid"]].items()},
                "dims": sum(1 for v in comp[s["sid"]].values() if v is not None),
                "papers": s["paper"], "h": s["h"],
                "ind_papers": ind_cnt[s["sid"]],
                "anchor_papers": len(anchored_papers(s)),
                "patent": pat[s["sid"]][0] if comp[s["sid"]]["PAT"] is not None else None,
                "clusters": [c for c, _ in cc.most_common(3)],
                "name_dup": name_dup().get(s["name"], 1),
                "sz_link": s["sid"] in sz_paper or is_sz(s["org"])}

    top15 = [row(i) for i in order[:15]]
    for k, r in enumerate(top15, 1):
        r["rank"] = k

    # ---------------- 簇级汇总 ----------------
    cl_rows = []
    for c in CLUSTERS:
        mem = [i for i in range(n) if cl_papers[sch[i]["sid"]].get(c, 0) > 0]
        if not mem:
            cl_rows.append({"cluster": c, "n": 0, "mean_score": None, "top5": []})
            continue
        mem.sort(key=lambda i: -score[i])
        cl_rows.append({
            "cluster": c,
            "n": len(mem),
            "mean_score": round(sum(score[i] for i in mem) / len(mem), 2),
            "sz_members": sum(1 for i in mem if is_sz(sch[i]["org"])),
            "top5": [{"name": sch[i]["name"], "org": sch[i]["org"], "score": round(score[i], 2),
                      "cluster_papers": cl_papers[sch[i]["sid"]][c]} for i in mem[:5]],
        })
    cl_rows.sort(key=lambda r: -r["n"])

    hist: dict[str, int] = {}
    for x in score:
        b = min(90, int(x // 10) * 10)
        hist[f"{b}-{b+10}"] = hist.get(f"{b}-{b+10}", 0) + 1
    hist = {k: hist[k] for k in sorted(hist, key=lambda s: int(s.split("-")[0]))}
    tiers = Counter(tier_of(x) for x in score)

    # ---------------- 敏感性 ----------------
    sens = []
    for dim in W:
        wts = dict(W)
        wts[dim] *= 2
        s2 = []
        for s in sch:
            pairs = [(wts[k], v) for k, v in comp[s["sid"]].items() if v is not None]
            den = sum(w for w, _ in pairs)
            s2.append(100 * sum(w * float(v) for w, v in pairs) / den if den else 0.0)
        o2 = sorted(range(n), key=lambda i: -s2[i])
        sens.append({"shift": f"{dim}×2",
                     "top10_overlap": len({sch[i]["sid"] for i in order[:10]}
                                          & {sch[i]["sid"] for i in o2[:10]}),
                     "tier_cross_rate_pct": round(100 * sum(
                         1 for i in range(n) if tier_of(score[i]) != tier_of(s2[i])) / n, 2),
                     "spearman": spearman(score, s2)})

    # 备选口径：论文簇改用「仅姓名匹配」（放大同名风险）→ 看排序是否稳
    ind2: dict[str, int] = {}
    for s in sch:
        cc = 0
        for p in name_papers(s):
            cc += 1 if paper_clusters(p["pid"], p["kw"], p["ti"]) else 0
        ind2[s["sid"]] = cc
    zind2 = log_minmax([float(ind2[s["sid"]]) for s in sch])
    s3 = []
    for i, s in enumerate(sch):
        c = dict(comp[s["sid"]])
        c["IND"] = zind2[i]
        pairs = [(W[k], v) for k, v in c.items() if v is not None]
        den = sum(w for w, _ in pairs)
        s3.append(100 * sum(w * float(v) for w, v in pairs) / den if den else 0.0)

    payload = {
        "metric": METRIC,
        "support_judgment": "部分支持",
        "support_reason": "四维中 IND/H/PAT 三维可直接算，LINK 维只能由「企业任职履历 / 企业合作论文 / "
                          "深圳机构合作论文」三个 0/1 信号拼装，需求原意中的横向课题经费、技术转让、"
                          "企业委托合同三列在 gkx 全库不存在（见 §三 表级清单）→ 部分支持。",
        "base_years": {"base_years_used": [], "base_years_missing": [],
                       "note": "截面指数，不涉基期与 CAGR；§3.16 两项按空集申报。"},
        "method": {
            "weights": W,
            "normalization": "IND/PAT：log1p→全池 min-max；H：log1p→全池 min-max；LINK：三信号等权均值",
            "tier_cuts": [60, 30],
            "tier_names": ["产业强关联", "产业中关联", "产业弱关联"],
            "pool": "gkx.dwd_scholar 有姓名全池",
            "cluster_dict": {"n_clusters": len(CLUSTERS), "names": list(CLUSTERS)},
            "missing_rule": "缺维不补 0，按可得维重归一分母",
        },
        "coverage": {
            "scholars": n,
            "anchor_papers_total": anchor_papers_total,
            "scholars_with_anchor_papers": sum(1 for s in sch if anchored_papers(s)),
            "scholars_with_ind_papers": sum(1 for v in ind_cnt.values() if v > 0),
            "ind_papers_total": sum(ind_cnt.values()),
            "dims_hist": {str(k): v for k, v in sorted(dims_hist.items())},
            "patent_tags": dict(tag_counter),
            "patent_scale_pool": len(pat_vals),
            "link_bits_hist": {str(k): v for k, v in sorted(link_bits_hist.items())},
            "link_nonnull": sum(1 for s in sch if comp[s["sid"]]["LINK"] is not None),
            "ent_work": len(ent_work & {s["sid"] for s in sch}),
            "ent_paper": len(ent_paper),
            "sz_paper_link": len(sz_paper),
            "work_rows": len(wx),
        },
        "dist": {k: st([float(comp[s["sid"]][k]) for s in sch if comp[s["sid"]][k] is not None]) for k in W},
        "score_stats": st(score),
        "distinct_scores": len({round(x, 2) for x in score}),
        "hist": hist,
        "tiers": dict(tiers),
        "top15": top15,
        "clusters": cl_rows,
        "cluster_member_overlap_note": "同一学者可同时命中多个簇（一篇论文含多组关键词），簇级 n 不可加总。",
        "sensitivity": {"weight_shift": sens, "name_only_ind": {
            "spearman": round(spearman(score, s3), 4),
            "top10_overlap": len({sch[i]["sid"] for i in order[:10]}
                                 & {sch[i]["sid"] for i in sorted(range(n), key=lambda i: -s3[i])[:10]}),
            "note": "备选口径把论文簇改为纯姓名匹配（不限机构），同名风险上升，仅作稳健性对照。",
        }},
        "integrity": {
            "h_gt_paper": sum(1 for s in sch if s["h"] > s["paper"]),
            "note": "论文簇只统计「姓名+机构前缀」双锚定记录；仅姓名匹配的簇不计入主口径。",
        },
        "probes": {"sql_count": 0,
                   "source": "_snapshots21/a25_paper_panel.json + patent_inventor_counts_gkx.json + probe_talent21_20261022.json"},
    }
    write_out(METRIC, payload)
    print("pool", n, "anchor papers", anchor_papers_total, "ind total", sum(ind_cnt.values()))
    print("tiers", dict(tiers), "dims", dict(dims_hist), "patent", dict(tag_counter))
    print("score", st(score))
    print("top5", [(r["name"], r["score"], r["clusters"]) for r in top15[:5]])
    print("clusters", [(r["cluster"], r["n"]) for r in cl_rows[:8]])
    print("sens", json.dumps(sens, ensure_ascii=False))


if __name__ == "__main__":
    main()
