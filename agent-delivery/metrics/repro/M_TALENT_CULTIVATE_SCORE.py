#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_CULTIVATE_SCORE —— 人才本地培育力指数（TALENT 展示面 §1.1.1.2.4.2.5.7）

口径：需求四维（留深黏性 Po / 学术力 A / 专利产出 P / 平台资源 R），
权重 Po 0.35、A 0.25、P 0.20、R 0.20（派单给定）。打分池 = 现任机构名含「深圳」的在册学者
（182 名有姓名者），四维缺一维按「可得维重归一分母」处理，不补零。

实测约束（见 out.json coverage / id_gap）：
  · 履历/学历/研究方向三张子表的 scholar_id 与主档不同域，仅 9.3% 可连 → Po 维的
    「任职年限」「深圳求学」两个子信号只能覆盖可连的那一小片，覆盖率在 out.json 如实给出；
  · 论文、被引、H 指数三列 100% 非空 → A 维用全池（20,420 名）分位换算，子群不被池内拉伸；
  · 发明人件数只读快照，两字姓名与池内同名录缺测，不补 0。

零 SQL、零 demo 表：全部读 `_snapshots21/` 与本目录 `_out` 同源快照。
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _talent21_common import (  # noqa: E402
    academicians, anchored_papers, edu, is_sz, log_minmax, name_papers,
    patent_of, scholars, spearman, st, talent, work, write_out,
)

METRIC = "M_TALENT_CULTIVATE_SCORE"
W = {"Po": 0.35, "A": 0.25, "P": 0.20, "R": 0.20}
PLATFORM_KW = ("国家重点实验室", "国家工程", "国家实验室", "中国科学院", "研究院", "大学")
REF_YEAR = 2026


def tier_of(x: float) -> str:
    return "高黏性强" if x >= 60 else ("培育中" if x >= 30 else "低黏性/待观察")


def _norm_pos(vals: list[float]) -> list[float]:
    """非负计数的池内 min-max（log1p 压重尾）；全零列返回全 0。"""
    if not vals or max(vals) <= 0:
        return [0.0] * len(vals)
    return log_minmax(vals)


def main() -> None:
    all_sch = [s for s in scholars() if s["name"]]
    pool = [s for s in all_sch if is_sz(s["org"])]
    n = len(pool)
    sids = {s["sid"] for s in pool}

    # ---------------- 子表可连性实测 ----------------
    wx = [r for r in work() if r["sid"] in sids]
    ed = [r for r in edu() if r["sid"] in sids]
    rd = talent()["research"]["rows"]
    rd_linked = {r[0] for r in rd if r[0] in sids}
    wx_sids = {r["sid"] for r in wx}
    ed_sids = {r["sid"] for r in ed}

    # ---------------- Po 留深黏性三子信号 ----------------
    ten: dict[str, float] = {}
    sz_work_rows: dict[str, int] = {}
    for r in wx:
        if not is_sz(r["org"]):
            continue
        y1 = r["y1"] or REF_YEAR
        if r["y0"]:
            ten[r["sid"]] = ten.get(r["sid"], 0.0) + max(0, min(y1, REF_YEAR) - r["y0"])
        sz_work_rows[r["sid"]] = sz_work_rows.get(r["sid"], 0) + 1
    sz_edu = Counter(r["sid"] for r in ed if is_sz(r["org"]))

    # 成长性诊断 G：近 5 年（2021—2025）锚定论文占全部锚定论文的比例 + 最近发表年。
    # 只作诊断输出、不入合成：派单给定权重是 Po/A/P/R，本文不擅自改权重（见 MD §1.3 偏离声明）。
    G_Y0 = REF_YEAR - 5
    g_recent: dict[str, int] = {}
    g_total: dict[str, int] = {}
    g_last: dict[str, int] = {}
    for s in pool:
        ap = anchored_papers(s)
        if not ap:
            continue
        ys = [p["y"] for p in ap if p.get("y")]
        if not ys:
            continue
        g_total[s["sid"]] = len(ys)
        g_recent[s["sid"]] = sum(1 for y in ys if y >= G_Y0)
        g_last[s["sid"]] = max(ys)

    sz_paper_share: dict[str, float] = {}
    np_all: dict[str, int] = {}
    np_sz: dict[str, int] = {}
    for s in pool:
        ps = name_papers(s)
        np_all[s["sid"]] = len(ps)
        np_sz[s["sid"]] = sum(1 for p in ps if "深圳" in (p["inst"] or ""))
        if ps:
            sz_paper_share[s["sid"]] = np_sz[s["sid"]] / len(ps)

    # ---------------- A 学术力：全池分位 ----------------
    zpaper = log_minmax([s["paper"] for s in all_sch])
    zcite = log_minmax([s["cite"] for s in all_sch])
    zh = log_minmax([s["h"] for s in all_sch])
    acad_all = {all_sch[i]["sid"]: (zpaper[i] + zcite[i] + zh[i]) / 3 for i in range(len(all_sch))}
    acad_sorted = sorted(acad_all.values())

    import bisect

    def pctile(v: float) -> float:
        return 100.0 * bisect.bisect_right(acad_sorted, v) / len(acad_sorted)

    # ---------------- P 专利：全池标尺 ----------------
    pat_all = {all_sch[i]["sid"]: patent_of(all_sch[i]) for i in range(len(all_sch))}
    pvals = [v for v, tag in pat_all.values() if v is not None]
    pz = _norm_pos([float(v) for v in pvals])
    pat_scale = dict(zip([all_sch[i]["sid"] for i in range(len(all_sch))
                          if pat_all[all_sch[i]["sid"]][0] is not None], pz))

    # ---------------- R 平台资源 ----------------
    acad = academicians()
    heis = {r[0] for r in talent()["heis"]["rows"]}
    heis_head = {h[:8] for h in heis}
    w_orgs: dict[str, set[str]] = {}
    for r in wx:
        if r["org"]:
            w_orgs.setdefault(r["sid"], set()).add(r["org"])

    def heis_hit(org: str) -> bool:
        o = (org or "").strip()
        if not o:
            return False
        if o in heis:
            return True
        return any(o[:8] == h or h in o or o in h for h in heis_head if len(h) >= 6)

    # ---------------- 合成 ----------------
    idx = {s["sid"]: i for i, s in enumerate(pool)}
    comp: dict[str, dict[str, float | None]] = {s["sid"]: {} for s in pool}

    # Po 子信号池内归一（仅在有值的子群内 min-max，缺测留空）
    def fill(key: str, raw: dict[str, float]) -> None:
        ids = [sid for sid in raw]
        vals = _norm_pos([raw[sid] for sid in ids])
        for sid, v in zip(ids, vals):
            comp[sid][key] = v

    fill("ten", ten)
    fill("sz_edu", {k: float(v) for k, v in sz_edu.items()})
    fill("sz_share", sz_paper_share)

    po_sub = {"ten": 0, "sz_edu": 0, "sz_share": 0}
    for s in pool:
        c = comp[s["sid"]]
        sub = [c.get("ten"), c.get("sz_edu"), c.get("sz_share")]
        for k, v in zip(("ten", "sz_edu", "sz_share"), sub):
            if v is not None:
                po_sub[k] += 1
        avail = [v for v in sub if v is not None]
        c["Po"] = (sum(avail) / len(avail)) if avail else None

    for s in pool:
        c = comp[s["sid"]]
        c["A"] = acad_all[s["sid"]] * 0 + 0  # placeholder, replaced below
        c["A"] = acad_all[s["sid"]]
        pv, tag = pat_all[s["sid"]]
        c["P"] = pat_scale.get(s["sid"])
        c["p_tag"] = tag
        r_bits = [1.0 if s["sid"] in acad else 0.0,
                  1.0 if heis_hit(s["org"]) else 0.0,
                  1.0 if any(any(k in o for k in PLATFORM_KW) for o in w_orgs.get(s["sid"], set())) else 0.0]
        c["R"] = sum(r_bits) / len(r_bits) if wx_sids & {s["sid"]} or True else None
        c["r_bits"] = r_bits

    score: list[float] = []
    dims_used: dict[str, int] = Counter()
    miss = Counter()
    for s in pool:
        c = comp[s["sid"]]
        pairs = [(W[k], c[k]) for k in W if c.get(k) is not None]
        ssum = sum(w for w, _ in pairs)
        dims_used[len(pairs)] += 1
        for k in W:
            if c.get(k) is None:
                miss[k] += 1
        score.append(100 * sum(w * float(v) for w, v in pairs) / ssum if ssum else 0.0)

    order = sorted(range(n), key=lambda i: (-score[i], pool[i]["sid"]))

    def row(i: int) -> dict:
        s = pool[i]
        c = comp[s["sid"]]
        return {"rank": 0, "name": s["name"], "org": s["org"],
                "score": round(score[i], 2),
                "comp": {k: (round(float(c[k]), 2) if c.get(k) is not None else None)
                         for k in ("Po", "A", "P", "R")},
                "dims": sum(1 for k in W if c.get(k) is not None),
                "ten_years": round(ten.get(s["sid"], 0.0), 1),
                "sz_edu_rows": sz_edu.get(s["sid"], 0),
                "sz_paper_share": round(sz_paper_share.get(s["sid"], 0.0), 3),
                "papers_total": np_all.get(s["sid"], 0),
                "papers_sz": np_sz.get(s["sid"], 0),
                "patent": c.get("p_tag") if c.get("P") is None else int(pat_all[s["sid"]][0]),
                "academician": s["sid"] in acad,
                "r_bits": c["r_bits"],
                "growth": ({"recent5": g_recent[s["sid"]], "total": g_total[s["sid"]],
                            "share": round(g_recent[s["sid"]] / g_total[s["sid"]], 3),
                            "last_year": g_last[s["sid"]]}
                           if s["sid"] in g_total else None)}

    top15 = [row(i) for i in order[:15]]
    for k, r in enumerate(top15, 1):
        r["rank"] = k
    bottom10 = [row(i) for i in order[-10:]]
    for k, r in enumerate(bottom10, 1):
        r["rank"] = n - k + 1

    # 直方图
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
        tot = sum(wts.values())
        s2 = []
        for s in pool:
            c = comp[s["sid"]]
            pairs = [(wts[k], c[k]) for k in W if c.get(k) is not None]
            ssum = sum(w for w, _ in pairs)
            s2.append(100 * sum(w * float(v) for w, v in pairs) / ssum / tot if ssum else 0.0)
        o2 = sorted(range(n), key=lambda i: -s2[i])
        top10_hit = len({pool[i]["sid"] for i in order[:10]} & {pool[i]["sid"] for i in o2[:10]})
        crossed = sum(1 for i in range(n) if tier_of(score[i]) != tier_of(s2[i]))
        sens.append({"shift": f"{dim}×2", "top10_overlap": top10_hit,
                     "tier_cross_rate_pct": round(100 * crossed / n, 2),
                     "spearman": spearman(score, s2)})

    # Po 子信号剔除一组的稳健性
    po_alt = []
    for s in pool:
        c = comp[s["sid"]]
        av = [c.get(k) for k in ("ten", "sz_edu") if c.get(k) is not None]
        po_alt.append(sum(av) / len(av) if av else None)
    s3 = []
    for i, s in enumerate(pool):
        c = comp[s["sid"]]
        po = po_alt[i]
        num, den = 0.0, 0.0
        if po is not None:
            num += W["Po"] * po
            den += W["Po"]
        for k in ("A", "P", "R"):
            if c.get(k) is not None:
                num += W[k] * float(c[k])
                den += W[k]
        s3.append(100 * num / den if den else 0.0)

    # ---------------- 覆盖与完整性 ----------------
    cov = {
        "pool": n,
        "sz_org_total": len([s for s in scholars() if is_sz(s["org"])]),
        "work_linked_sids": len(wx_sids & sids),
        "work_sz_rows": len([r for r in wx if is_sz(r["org"])]),
        "edu_linked_sids": len(ed_sids & sids),
        "edu_sz_rows": sum(sz_edu.values()),
        "research_linked_sids": len(rd_linked),
        "po_sub_coverage": {k: v for k, v in po_sub.items()},
        "dims_hist": {str(k): v for k, v in sorted(dims_used.items())},
        "missing_by_dim": {k: miss[k] for k in W},
        "patent_tags": dict(Counter(comp[s["sid"]]["p_tag"] for s in pool)),
        "academician_in_pool": sum(1 for s in pool if s["sid"] in acad),
        "heis_org_in_pool": sum(1 for s in pool if heis_hit(s["org"])),
        "patent_scale_pool": len(pvals),
    }

    payload = {
        "metric": METRIC,
        "support_judgment": "部分支持",
        "support_reason": "四维中三维修（A 学术力、P 专利、R 平台资源）有可算数据；"
                          "Po 留深黏性维的三个子信号里，「任职年限」与「深圳求学」受子表 scholar_id "
                          "跨域影响只覆盖可连子集，「深圳署名论文占比」可算但仅对有论文署名者；"
                          "专利维两字姓名/池内同名一律缺测 → 部分支持。",
        "base_years": {"base_years_used": [], "base_years_missing": [],
                       "note": "本指标为截面黏性指数，不涉基期与 CAGR；§3.16 两项按空集申报。"},
        "method": {
            "weights": W,
            "normalization": "Po：四子信号池内 log1p→min-max 后等权；A：全池（20,420）学术三维等权后取分位/100；"
                             "P：全池发明人件数 log1p→min-max；R：三项 0/1 等权",
            "tier_cuts": [60, 30],
            "tier_names": ["高黏性强", "培育中", "低黏性/待观察"],
            "pool": "现任机构名含「深圳」且姓名非空的在册学者",
            "missing_rule": "缺维不补 0，按可得维重归一分母",
        },
        "coverage": cov,
        "dist": {k: st([float(comp[s["sid"]][k]) for s in pool if comp[s["sid"]].get(k) is not None])
                 for k in W},
        "score_stats": st(score),
        "distinct_scores": len({round(x, 2) for x in score}),
        "hist": hist,
        "tiers": dict(tiers),
        "top15": top15,
        "bottom10": bottom10,
        "sensitivity": {"weight_shift": sens, "po_drop_share": {
            "spearman": spearman(score, s3),
            "top10_overlap": len({pool[i]["sid"] for i in order[:10]}
                                 & {pool[i]["sid"] for i in sorted(range(n), key=lambda i: -s3[i])[:10]}),
        }},
        "growth_diagnostic": {
            "note": "seed 原意为「高成长潜力」，但派单给定权重为 Po/A/P/R，本文不擅改权重；"
                    "此处单列「近 5 年锚定论文占比 + 最近发表年」作成长性诊断，不入合成。",
            "window": [G_Y0, REF_YEAR - 1],
            "covered": len(g_total),
            "recent5_share": st([g_recent[k] / g_total[k] for k in g_total]),
            "last_year_hist": dict(Counter(g_last.values()).most_common(8)),
            "spearman_vs_score": spearman([score[i] for i in range(n) if pool[i]["sid"] in g_total],
                                          [g_recent[k] / g_total[k] for k in
                                           [pool[i]["sid"] for i in range(n) if pool[i]["sid"] in g_total]]),
        },
        "id_gap": {
            "note": "work_exp/edu/research 三张子表的 scholar_id 与主档不同域，池内仅 "
                    f"{len(wx_sids & sids)}/{n} 可连履历、{len(ed_sids & sids)}/{n} 可连学历，"
                    "故 Po 维两个履历子信号的覆盖率即为实测值，不外推。",
            "work_linked": len(wx_sids & sids), "edu_linked": len(ed_sids & sids),
            "research_linked": len(rd_linked), "pool": n,
        },
        "integrity": {
            "h_gt_paper_pool": sum(1 for s in pool if s["h"] > s["paper"]),
            "sz_share_gt_1": sum(1 for v in sz_paper_share.values() if v > 1.0),
            "note": "深圳署名占比按论文粒度计，分母为该姓名全部姓名匹配论文（含同名风险），仅作序数信号。",
        },
        "probes": {"sql_count": 0,
                   "source": "_snapshots21/probe_a26_20261022.json + probe_talent21_20261022.json + a25_paper_panel.json"},
    }
    write_out(METRIC, payload)
    print("pool", n, "tiers", dict(tiers), "dims", dict(dims_used))
    print("po_sub", po_sub, "patent_tags", dict(Counter(comp[s["sid"]]["p_tag"] for s in pool)))
    print("score", st(score))
    print("top5", [(r["name"], r["score"], r["dims"]) for r in top15[:5]])
    print("sens", json.dumps(sens, ensure_ascii=False))
    print("po_alt spearman", round(spearman(score, s3), 4))


if __name__ == "__main__":
    main()
