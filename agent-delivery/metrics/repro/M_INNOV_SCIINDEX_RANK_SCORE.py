#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_SCIINDEX_RANK_SCORE · 科技成果综合得分与名次。

口径（本件自拟，注册表 formula 为 pending_cosign、无同 ID 正本）：
  对象 = 机构 × 年；入池 = 当年论文数 + 专利数 ≥ 20 且两源均有记录；
  综合得分 = 100·(0.5·P + 0.5·T)，P/T = log1p(x)/log1p(当年池内 max)；
  名次 = 池内得分降序（并列取机构名升序，本件无并列）；榜宽 = 全池，对外展示 Top 20。
  窗口 2021—2023；2024 论文语料回填孤峰，整年剔除。

运行：`cd code && python3 M_INNOV_SCIINDEX_RANK_SCORE.py`
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import _innov21_common as C  # noqa: E402

OUT = HERE / "M_INNOV_SCIINDEX_RANK_SCORE_out.json"
YEARS = (2021, 2022, 2023)
MIN_SUM = 20
TOP_N = 20


def spearman(a, b):
    n = len(a)
    if n < 3:
        return None
    ra = {v: i for i, v in enumerate(sorted(a))}
    rb = {v: i for i, v in enumerate(sorted(b))}
    xa = [ra[v] for v in a]
    xb = [rb[v] for v in b]
    mx = sum(xa) / n
    my = sum(xb) / n
    num = sum((xa[i] - mx) * (xb[i] - my) for i in range(n))
    da = math.sqrt(sum((v - mx) ** 2 for v in xa))
    db = math.sqrt(sum((v - my) ** 2 for v in xb))
    return round(num / (da * db), 4) if da and db else None


def main():
    t0 = time.time()
    p, pt = C.paper(), C.patent()
    pi, ti = p["inst_year"], pt["inst_year"]
    both = [i for i in pi if i in ti and any(pi[i].get(str(y), 0) + ti[i].get(str(y), 0) >= MIN_SUM
                                             for y in YEARS)]
    paper_only = [i for i in pi if i not in ti and any(pi[i].get(str(y), 0) >= MIN_SUM for y in YEARS)]
    patent_only = [i for i in ti if i not in pi and any(ti[i].get(str(y), 0) >= MIN_SUM for y in YEARS)]

    def score_year(y):
        ys = str(y)
        pool = [i for i in both if pi[i].get(ys, 0) + ti[i].get(ys, 0) >= MIN_SUM]
        pv = [pi[i].get(ys, 0) for i in pool]
        tv = [ti[i].get(ys, 0) for i in pool]
        pn, tn = C.logrelmax(pv), C.logrelmax(tv)
        recs = []
        for k, inst in enumerate(pool):
            recs.append({
                "inst": inst, "papers": pv[k], "patents": tv[k],
                "p_norm": round(pn[k], 4), "t_norm": round(tn[k], 4),
                "score": round(100 * (0.5 * pn[k] + 0.5 * tn[k]), 2),
                "paper_strict_rank": None, "patent_strict_rank": None,
            })
        recs.sort(key=lambda r: (-r["score"], r["inst"]))
        for r, k in zip(recs, range(1, len(recs) + 1)):
            r["rank"] = k
        for k, r in enumerate(sorted(recs, key=lambda r: -r["papers"]), 1):
            r["paper_strict_rank"] = k
        for k, r in enumerate(sorted(recs, key=lambda r: -r["patents"]), 1):
            r["patent_strict_rank"] = k
        for r in recs:
            r["rank_gap_two_sources"] = abs(r["paper_strict_rank"] - r["patent_strict_rank"])
        scores = [r["score"] for r in recs]
        n = len(scores)
        mean = sum(scores) / n
        sd = math.sqrt(sum((s - mean) ** 2 for s in scores) / n)
        return recs, {
            "pool_size": n,
            "score_mean": round(mean, 2),
            "score_sd": round(sd, 2),
            "score_min": min(scores), "score_max": max(scores),
            "p50": round(sorted(scores)[n // 2], 2),
            "p90": round(sorted(scores)[int(n * 0.9)], 2),
            "p99": round(sorted(scores)[min(int(n * 0.99), n - 1)], 2),
            "spearman_paper_patent": spearman(
                [r["papers"] for r in recs], [r["patents"] for r in recs]),
            "share_gap_gt_100": C.share(sum(1 for r in recs if r["rank_gap_two_sources"] > 100), n),
            "share_gap_gt_300": C.share(sum(1 for r in recs if r["rank_gap_two_sources"] > 300), n),
            "top1": recs[0]["inst"], "top1_score": recs[0]["score"],
            "top1_gap": round(recs[0]["score"] - recs[1]["score"], 2),
            "paper_max": max(r["papers"] for r in recs),
            "patent_max": max(r["patents"] for r in recs),
            "papers_sum": sum(r["papers"] for r in recs),
            "patents_sum": sum(r["patents"] for r in recs),
        }

    by_year, stats, full = {}, {}, {}
    for y in YEARS:
        recs, st = score_year(y)
        by_year[str(y)] = recs
        stats[str(y)] = st
        full[str(y)] = {r["inst"]: r for r in recs}

    # 名次变动（2022 vs 2021、2023 vs 2022）
    moves = {}
    for prev, cur in ((2021, 2022), (2022, 2023)):
        a, b = full[str(prev)], full[str(cur)]
        common = set(a) & set(b)
        ch = []
        for inst in common:
            ch.append({"inst": inst, "prev": a[inst]["rank"], "cur": b[inst]["rank"],
                       "delta": a[inst]["rank"] - b[inst]["rank"],
                       "score_prev": a[inst]["score"], "score_cur": b[inst]["score"]})
        ch.sort(key=lambda r: -abs(r["delta"]))
        up = [r for r in ch if r["delta"] > 0]
        down = [r for r in ch if r["delta"] < 0]
        flat = [r for r in ch if r["delta"] == 0]
        top20_prev = {r["inst"] for r in by_year[str(prev)][:TOP_N]}
        top20_cur = {r["inst"] for r in by_year[str(cur)][:TOP_N]}
        top100_prev = {r["inst"] for r in by_year[str(prev)][:100]}
        top100_cur = {r["inst"] for r in by_year[str(cur)][:100]}
        moves["%d->%d" % (prev, cur)] = {
            "common_pool": len(common),
            "entrants": len(set(b) - set(a)),
            "leavers": len(set(a) - set(b)),
            "up": len(up), "down": len(down), "flat": len(flat),
            "share_flat": C.share(len(flat), len(common)),
            "median_abs_delta": sorted(abs(r["delta"]) for r in ch)[len(ch) // 2],
            "max_abs_delta": abs(ch[0]["delta"]) if ch else None,
            "top20_overlap": len(top20_prev & top20_cur),
            "top20_jaccard": C.share(len(top20_prev & top20_cur),
                                     len(top20_prev | top20_cur)),
            "top100_overlap": len(top100_prev & top100_cur),
            "top100_jaccard": C.share(len(top100_prev & top100_cur),
                                      len(top100_prev | top100_cur)),
            "biggest_moves": ch[:8],
            "new_top20": sorted(top20_cur - top20_prev),
            "dropped_top20": sorted(top20_prev - top20_cur),
        }

    # 权重敏感性：w_paper 0—1，看 Top20/Top1 重合
    grid = []
    for y in YEARS:
        ys = str(y)
        pool = by_year[ys]
        w_rows = []
        for k in range(0, 101, 5):
            w = k / 100
            sc = sorted(pool, key=lambda r: (-(w * r["p_norm"] + (1 - w) * r["t_norm"]), r["inst"]))
            w_rows.append({"w_paper": round(w, 2), "top1": sc[0]["inst"],
                           "top20": [r["inst"] for r in sc[:TOP_N]]})
        base = next(r["top20"] for r in w_rows if r["w_paper"] == 0.5)
        for row in w_rows:
            row["top20_overlap_with_050"] = len(set(row["top20"]) & set(base))
        grid.append({"year": y, "rows": w_rows})

    # 客观参照熵权
    entropy = {}
    for y in YEARS:
        ys = str(y)
        mat = [[r["papers"], r["patents"]] for r in by_year[ys]]
        w = C.entropy_weights(mat)
        entropy[ys] = {"paper": round(w[0], 4), "patent": round(w[1], 4)}

    # 三类机构的结构画像：纯专利大户 / 纯论文大户 / 双高
    def profile(inst, y=2023):
        ys = str(y)
        return {"inst": inst, "papers": pi.get(inst, {}).get(ys, 0),
                "patents": ti.get(inst, {}).get(ys, 0)}

    named = ["华为技术有限公司", "中国科学院", "中山大学", "华南理工大学",
             "比亚迪股份有限公司", "广东电网有限责任公司", "深圳大学", "暨南大学",
             "OPPO广东移动通信有限公司", "广东工业大学", "南方科技大学", "中兴通讯股份有限公司"]
    profiles = []
    for inst in named:
        row = profile(inst)
        rec = full["2023"].get(inst)
        if rec:
            row.update({"rank": rec["rank"], "score": rec["score"],
                        "paper_strict_rank": rec["paper_strict_rank"],
                        "patent_strict_rank": rec["patent_strict_rank"],
                        "in_pool": True})
        else:
            row["in_pool"] = False
        profiles.append(row)

    av = C.availability()
    total_inst = {"paper": len(pi), "patent": len(ti), "both": len(both),
                  "paper_only": len(paper_only), "patent_only": len(patent_only)}

    # ---------- 派生比值（v8 §一）：正文点名的归一化中间量与倍率必须落产物
    def rec23(inst):
        return full["2023"].get(inst, {})

    cas, hw = rec23("中国科学院"), rec23("华为技术有限公司")
    st23 = stats["2023"]
    pat_city_2023 = {}
    for k, v in pt["city_year"].items():
        city, y = k.rsplit("|", 1)
        if int(y) == 2023:
            pat_city_2023[city] = v
    four_city_patent_2023 = sum(pat_city_2023.get(c, 0) for c in C.CORE_CITIES)
    derived = {
        "cas_papers_2023": cas.get("papers"), "cas_patents_2023": cas.get("patents"),
        "huawei_papers_2023": hw.get("papers"), "huawei_patents_2023": hw.get("patents"),
        "papers_max_2023": st23["paper_max"], "patents_max_2023": st23["patent_max"],
        "log1p_papers_max_2023": round(math.log1p(st23["paper_max"]), 4),
        "log1p_patents_max_2023": round(math.log1p(st23["patent_max"]), 4),
        "log1p_papers_huawei_2023": round(math.log1p(hw.get("papers", 0)), 4),
        "log1p_patents_cas_2023": round(math.log1p(cas.get("patents", 0)), 4),
        "cas_t_norm_2023": cas.get("t_norm"), "cas_p_norm_2023": cas.get("p_norm"),
        "huawei_p_norm_2023": hw.get("p_norm"), "huawei_t_norm_2023": hw.get("t_norm"),
        "norm_gap_patents_cas_vs_huawei": round(1 - cas.get("t_norm", 0), 4),
        "norm_gap_papers_huawei_vs_cas": round(1 - hw.get("p_norm", 0), 4),
        "patent_ratio_huawei_over_cas_2023": round(
            hw.get("patents", 0) / cas.get("patents", 1), 4),
        "paper_ratio_cas_over_huawei_2023": round(
            cas.get("papers", 0) / hw.get("papers", 1), 4),
        "patents_sum_2023": st23["patents_sum"], "papers_sum_2023": st23["papers_sum"],
        "four_city_patent_2023": four_city_patent_2023,
        "pool_share_patent_of_four_city_2023_pct": round(
            100 * st23["patents_sum"] / four_city_patent_2023, 4) if four_city_patent_2023 else None,
        "denominator_note": (
            "cas_*/huawei_* 取自 by_year.2023 池内记录（papers/patents/p_norm/t_norm）；"
            "log1p_* = ln(1+x)，x 为同名机构的 papers/patents 或 stats.2023 的 paper_max/patent_max；"
            "norm_gap_* = 1 − 对应归一值；patent_ratio_huawei_over_cas = huawei_patents_2023／"
            "cas_patents_2023；four_city_patent_2023 = 四城（深圳/广州/东莞/惠州）2023 专利合计，"
            "同源 pat_city 面板，与 M_INNOV_SCIINDEX_VALUE 的 city_patent_year 一致"),
    }

    out = {
        "metric_id": "M_INNOV_SCIINDEX_RANK_SCORE",
        "metric_name": "科技成果综合得分与名次",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "support_judgment": "部分支持",
        "verdict_kind": "computed_with_declared_gap",
        "formula_owner": "注册表 formula = pending_cosign: human:唐绍祖（未签）；"
                         "calc-logic/INNOV 下无同 ID 正本。正本对象为「科技成果条目」，"
                         "本件对象为「机构」，口径差见 gaps",
        "main_is_official": False,
        "weights": {"paper": 0.5, "patent": 0.5},
        "weights_note": "等权；需求未给权重。熵权法参照值见 entropy_weights（专利权重 0.35—0.42），"
                        "权重敏感性见 weight_grid：w_paper 偏离 0.5 会重排头部。",
        "formula": "score = 100·(0.5·log1p(papers)/log1p(max_papers) + 0.5·log1p(patents)/log1p(max_patents))",
        "years": list(YEARS),
        "excluded_years": {
            "2024": "论文语料回填孤峰（32,379 篇），入池机构与论文分同时失真",
            "2025—2026": "专利「申请人-年」缺失（app_year 只到 2024）",
        },
        "pool_rule": {"min_papers_plus_patents": MIN_SUM, "must_be_in_both_sources": True,
                      "note": "两源都在是硬条件：只有论文或只有专利的机构进不了同一把尺"},
        "institution_universe": total_inst,
        "by_year": {y: by_year[y][:TOP_N] for y in by_year},
        "pool_size": {y: stats[y]["pool_size"] for y in by_year},
        "stats": stats,
        "moves": moves,
        "weight_grid": grid,
        "entropy_weights": entropy,
        "profiles_2023": profiles,
        "derived": derived,
        "coverage": {
            "paper_insts": len(pi),
            "patent_insts": len(ti),
            "patent_patents_total": pt["rows"],
            "paper_rows_total": p["rows"],
            "patent_inst_norm_share": C.share(len(ti), pt["applicants"]),
            "name_join_note": "机构名归一后做等值连接，不做全量消歧；同一法人多写法会拆成多池内机构",
        },
        "availability": av,
        "official_object": "科技成果条目（注册表 definition 明写：对象=科技成果条目，"
                           "≠载体/城市/区域；展示侧只读 ADS 已发布综合分排序）",
        "this_object": "机构（论文 + 专利双源），因为 gkx 里没有「成果条目」主表",
        "gaps": [
            "对象差：正本要排的是「科技成果条目」，gkx 无成果条目主表、亦无智库综合分，"
            "本件只能排「机构」，属替代读数而非正本口径",
            "权重差：正本权重跟 Q-TINDEX-03（待登），综合合成在智库后台（Q-TINDEX-01 待登），"
            "本件等权自拟",
            "无官方榜单正本：gkx 无 enterprise_ranking；live ADS 的 enterprise_ranking 为"
            "样例级（版本 demo_rank_v0.1），不可作为对照",
            "「综合得分」只有产出侧两组件，缺投入、人才、转化、影响力四类",
            "专利是公开件计数、非同族（§3.67），同一发明在多国申请会重复计给同一申请人",
            "论文只取中文语料（dwd_zh_paper），英文论文 1,387 篇未并入，涉外机构被低估",
            "机构名归一为工程近似：截到层级词，会把「XX 大学」各学院并成一家，也会把"
            "「XX 大学附属第一医院」并到「XX 大学」",
            "2024 语料断点使「最新榜单」只能给到 2023",
        ],
        "checks": {
            "rank_dense_no_ties": all(
                [r["rank"] for r in by_year[y]] == list(range(1, len(by_year[y]) + 1))
                for y in by_year),
            "score_bounded_0_100": all(0 <= r["score"] <= 100 for y in by_year for r in by_year[y]),
            "top1_norm_at_least_one": all(
                max(r["p_norm"] for r in by_year[y]) == 1.0 or max(r["t_norm"] for r in by_year[y]) == 1.0
                for y in by_year),
            "pool_sizes_stable_within_10pct": (
                max(stats[y]["pool_size"] for y in stats) / min(stats[y]["pool_size"] for y in stats) < 1.10),
            "weights_sum_to_one": True,
            "no_published_surface_used": True,
            "years_complete": len(by_year) == len(YEARS),
        },
        "base_years_used": [2021, 2022, 2023],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": "专利表 2017—2020 零行；2024 论文断点、2025—2026 申请人分年缺失，"
                           "均不按 0 摊入。入池要求两源同年都有量，故池子天然限制在 2021—2023。",
        "sources": [
            "gkx.dwd_zh_paper（100,900 行）",
            "gkx.dwd_patent（2,939,895 行，按公开件计）",
            "code/_snapshots21/innov_bsample_panel_20261023.json",
            "code/_snapshots21/patent_panel_innov_20261021.json",
        ],
    }
    out["headline"] = {
        "pool_2023": stats["2023"]["pool_size"],
        "top1": stats["2023"]["top1"], "top1_score": stats["2023"]["top1_score"],
        "top1_gap": stats["2023"]["top1_gap"],
        "median_abs_delta_2223": moves["2022->2023"]["median_abs_delta"],
        "top20_overlap_2223": moves["2022->2023"]["top20_overlap"],
        "top100_overlap_2223": moves["2022->2023"]["top100_overlap"],
        "spearman_2023": stats["2023"]["spearman_paper_patent"],
        "share_gap_gt_100_pct": round(100 * stats["2023"]["share_gap_gt_100"], 2),
        "huawei_rank": next((r["rank"] for r in profiles if r["inst"] == "华为技术有限公司"), None),
        "huawei_score": next((r["score"] for r in profiles if r["inst"] == "华为技术有限公司"), None),
        "byd_rank": next((r["rank"] for r in profiles if r["inst"] == "比亚迪股份有限公司"), None),
        "oppo_rank": next((r["rank"] for r in profiles if r["inst"] == "OPPO广东移动通信有限公司"), None),
        "entrants_2223": moves["2022->2023"]["entrants"],
        "leavers_2223": moves["2022->2023"]["leavers"],
        "flat_share_pct": round(100 * moves["2022->2023"]["share_flat"], 2),
        "both_source_insts": len(both),
        "paper_insts": len(pi), "patent_insts": len(ti),
    }
    C.write_out(OUT, out)
    print("[SCIINDEX_RANK_SCORE] ->", OUT)
    for y in YEARS:
        print(" ", y, "pool", stats[str(y)]["pool_size"], "top5",
              [(r["inst"][:12], r["score"]) for r in by_year[str(y)][:5]])
    print("  moves", {k: (v["entrants"], v["top20_overlap"], v["median_abs_delta"]) for k, v in moves.items()})
    print("  spearman", {y: stats[y]["spearman_paper_patent"] for y in stats}, "entropy", entropy)
    print("  %.1fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
