#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""创新点价值评估（M_INNOV_POINT_VALUE）——A-25 批 · 三方库 gkx 版。

王惠口径（calc-logic INNOV V1.5-20260829）：
  对象 = `M_INNOV_POINT_DISCOVERY` 输出的候选词条（同一主键，不另造）；
  三维：新颖性 1/(1+T−t0)、影响潜力（关联成果被引合计）、成熟度（授权专利 / 专利数）；
  同一 point_type 内极值归一等权 ×100；缺测维不补 0，剩余维按比例重归一。

本库落地（先实测后定档）：
  新颖性    ✅ 依赖词条首现年（专利侧只有 2021—2026，见 DISCOVERY 的基窗缺口）
  影响潜力  ⚠️ 论文侧可用（`dwd_zh_paper_citation` 20,031 篇）；专利侧不可用——
              `dwd_patent_cited` 20,515 行里只有 467 行能按 `patent_id` 连上主表（2.28%），
              主键不同源，词条级专利被引无法成立
  成熟度    ✅ 专利关键词/IPC4 用主键切片（6.80%）的 `granted_number` 非空占比；
              论文侧无「授权」概念 → 缺测

产物：code/M_INNOV_POINT_VALUE_out.json
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import _a25_common as C

METRIC = "M_INNOV_POINT_VALUE"
T = C.T_YEAR
MIN_RECENT = 3
MIN_PAT = 30


def candidates(counts: dict, available, kind: str):
    out = []
    for term, yc in counts.items():
        st = C.window_stats(yc, C.BASE, C.RECENT, available)
        if st["recent_total"] < MIN_RECENT:
            continue
        st["is_new"] = 1 if (st["t0"] is not None and st["t0"] >= T - 2) else 0
        if not (st["burst"] >= 1 or st["is_new"]):
            continue
        st["term"] = term
        st["point_type"] = kind
        out.append(st)
    return out


def main():
    tp = C.term_panel()
    years_pat = sorted({y for yc in tp["ipc"].values() for y in yc})
    p_years = {y: n for y, n in C.paper_year_all().items() if n > 0}
    years_paper = sorted(p_years)
    ss = C.sample_stats()

    # 专利侧切片：IPC4 与关键词的授权分母
    grant_ipc, n_ipc, grant_kw, n_kw = {}, {}, {}, {}
    meta, rows = C.sample()
    for r in rows:
        g = 1 if r["granted_number"] else 0
        ipc = C.ipc4_of(r["main_classification_ipcr"])
        if ipc:
            n_ipc[ipc] = n_ipc.get(ipc, 0) + 1
            grant_ipc[ipc] = grant_ipc.get(ipc, 0) + g
        for t in C.parse_kw(r["keywords"]):
            t = t.lower() if t.isascii() else t
            n_kw[t] = n_kw.get(t, 0) + 1
            grant_kw[t] = grant_kw.get(t, 0) + g

    sets = {
        "ipc4": candidates(tp["ipc"], years_pat, "ipc4"),
        "keyword_patent": candidates(tp["kwp"], years_pat, "keyword_patent"),
        "keyword_paper": candidates(tp["kwa"], years_paper, "keyword_paper"),
    }

    result = {}
    for kind, cands in sets.items():
        for r in cands:
            r["novelty"] = round(1.0 / (1 + max(T - (r["t0"] or T), 0)), 4)
            if kind == "keyword_paper":
                r["influence"] = round(tp["kwa_cite"].get(r["term"], 0.0), 2)
                r["maturity"] = None
                r["patent_n"] = None
            else:
                r["influence"] = None
                den = n_ipc.get(r["term"], 0) if kind == "ipc4" else n_kw.get(r["term"], 0)
                num = grant_ipc.get(r["term"], 0) if kind == "ipc4" else grant_kw.get(r["term"], 0)
                if den >= MIN_PAT:
                    r["maturity"] = round(num / den, 4)
                    r["patent_n"] = den
                else:
                    r["maturity"] = None
                    r["patent_n"] = den
        nov = [r["novelty"] for r in cands]
        inf = [r["influence"] for r in cands if r["influence"] is not None]
        mat = [r["maturity"] for r in cands if r["maturity"] is not None]
        nov_n = C.minmax(nov) if nov else []
        inf_map = dict(zip([r["term"] for r in cands if r["influence"] is not None],
                           C.minmax(inf) if inf else []))
        mat_map = dict(zip([r["term"] for r in cands if r["maturity"] is not None],
                           C.minmax(mat) if mat else []))
        for r, nv in zip(cands, nov_n):
            parts = [nv]
            r["novelty_n"] = round(nv, 2)
            r["influence_n"] = round(inf_map.get(r["term"], 0), 2) if r["term"] in inf_map else None
            r["maturity_n"] = round(mat_map.get(r["term"], 0), 2) if r["term"] in mat_map else None
            if r["influence_n"] is not None:
                parts.append(r["influence_n"])
            if r["maturity_n"] is not None:
                parts.append(r["maturity_n"])
            r["n_dims"] = len(parts)
            r["value_score"] = round(sum(parts) / len(parts), 2)
        cands.sort(key=lambda r: (-r["value_score"], -r["recent_total"]))
        comp = [r for r in cands if r["n_dims"] >= 2]
        comp.sort(key=lambda r: (-r["value_score"], -r["recent_total"]))
        result[kind] = {
            "n_candidates": len(cands),
            "n_with_influence": len(inf),
            "n_with_maturity": len(mat),
            "n_comparable_2d": len(comp),
            "comparable_value_dist": C.dist([r["value_score"] for r in comp]) if comp else {"n": 0},
            "comparable_top": comp[:20],
            "value_dist": C.dist([r["value_score"] for r in cands]),
            "novelty_dist": C.dist(nov),
            "influence_dist": C.dist(inf) if inf else {"n": 0},
            "maturity_dist": C.dist(mat) if mat else {"n": 0},
            "top": cands[:40],
        }

    cited = C.facts()["cited_rows"][0]
    link = C.facts()["cited_link"][0]["n"]

    out = {
        "metric_id": METRIC,
        "metric_name": "创新点价值评估",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "definition": ("候选词条的三维价值分：新颖性 1/(1+T−t0)、影响潜力（关联成果被引合计）、"
                       "成熟度（授权专利/专利数）；同 point_type 内极值归一，缺测维重归一"),
        "statistical_year": T,
        "data_source": ("gkx.dwd_patent 主键切片 6.80%（授权）、dwd_zh_paper_citation 20,031 篇（被引）、"
                        "dwd_patent_cited 20,515 行（仅 467 行可连主表）"),
        "probes": {
            "patent_sample": {"rows": ss["n"], "share": ss["meta"]["share"],
                              "grant_rate": ss["grant_rate"], "kw_share": ss["kw_share"]},
            "patent_cited": {"rows": cited["n"], "pos": cited["pos"], "max": cited["mx"],
                             "mean": round(float(cited["av"]), 4),
                             "linked_to_patent": link,
                             "link_rate": round(link / cited["n"], 4)},
            "paper_citation": {"papers": len(C.papers()),
                               "source_rows": 20031,
                               "share_of_zh_paper": round(20031 / 100900, 4)},
            "paper_id_join": C.paper_id_join(),
        },
        "result": result,
        "support_judgment": "部分支持",
        "reasons": [
            "新颖性、成熟度两维可算（成熟度限专利侧，来自 6.80% 主键切片，分母<30 的词条判缺测）；",
            "影响潜力在专利侧不可用：`dwd_patent_cited` 与主表 `patent_id` 不同源，20,515 行只有 467 行（2.28%）可连，"
            "词条级专利被引不成立；论文侧被引表 20,031 行虽 100% 挂在分类表 id 上，但分类表只有 799 行能对上论文主表拿年份，"
            "真正有「年份 + 被引」的论文只有 799 篇（0.79%）；",
            "候选词条受 DISCOVERY 的基窗缺口约束（专利 2017—2020 零行），专利侧词条的「新」与「突现」都只有 2021 年作基线；",
            "论文侧词条没有授权概念，成熟度恒缺测，价值分实际是「新颖性 + 被引」两维。",
        ],
    }
    p = HERE / f"{METRIC}_out.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print("written", p)
    for k, v in result.items():
        print(k, "cand", v["n_candidates"], "inf", v["n_with_influence"],
              "mat", v["n_with_maturity"], "med", v["value_dist"].get("median"))


if __name__ == "__main__":
    main()
