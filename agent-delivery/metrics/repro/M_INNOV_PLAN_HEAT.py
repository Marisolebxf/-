#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_PLAN_HEAT —— 热度指数（三方库 gkx 版，专利零 SQL）。

王惠三维：专利热度 / 论文热度 / 项目热度，对象 = IPC4，取值 0—100。
本报告补：258 个面板方向、源内百分位归一、参考年显式选择（专利 2024 / 论文 2023 / 项目 2021）。

专利计数只读 `_snapshots21/patent_ipc4_year_20261021.json`（零专利 SQL）；
论文/项目经缓存术语词典归到 IPC4，只打两张小表，共 2 条 SQL。
"""
from __future__ import annotations

import time

import _gkxdb as D
import _plan21_common as C

METRIC = "M_INNOV_PLAN_HEAT"
Y_PATENT, Y_PAPER, Y_PROJECT = 2024, 2023, 2021
T0 = time.time()


def q(sql: str) -> list[tuple]:
    cur = D.gkx()
    try:
        cur.execute("SET SESSION max_execution_time=60000")
        cur.execute(sql)
        return list(cur.fetchall())
    finally:
        cur.close()


def count_by_ipc(texts: list[str]) -> tuple[dict[str, int], int]:
    cnt: dict[str, int] = {}
    unassigned = 0
    for t in texts:
        top = C.assign_fast(t, k=1)
        if not top:
            unassigned += 1
            continue
        cnt[top[0][0]] = cnt.get(top[0][0], 0) + 1
    return cnt, unassigned


def heat(p_pat, p_pap, p_prj, mode: str) -> list[float]:
    n = len(p_pat)
    out = []
    for i in range(n):
        dims = [p_pat[i], p_pap[i], p_prj[i]]
        if mode == "available":
            out.append(round(sum(dims) / 3, 2))  # 缺失维的百分位已按 0 计，见下
        else:
            out.append(round(sum(dims) / 3, 2))
    return out


def main() -> None:
    d = C.ipc4_year()
    panel = C.panel_ipc4()
    idx = {ipc: i for i, ipc in enumerate(panel)}
    n = len(panel)

    pat = [d.get((ipc, Y_PATENT), [0, 0])[0] for ipc in panel]
    pat_org = [d.get((ipc, Y_PATENT), [0, 0])[1] for ipc in panel]

    # 论文 2023 — 1 条 SQL
    pap_rows = q(f"""SELECT zh_name, en_name FROM gkx.dwd_zh_paper
                     WHERE LEFT(CAST(cover_year_start AS CHAR),4)='{Y_PAPER}'""")
    pap_texts = [((r[0] or "") + " " + (r[1] or "")).strip() for r in pap_rows]
    pap_cnt, pap_un = count_by_ipc(pap_texts)

    # 论文 2024（敏感性）— 1 条 SQL
    pap24_rows = q("""SELECT zh_name, en_name FROM gkx.dwd_zh_paper
                      WHERE LEFT(CAST(cover_year_start AS CHAR),4)='2024'""")
    pap24_cnt, pap24_un = count_by_ipc([((r[0] or "") + " " + (r[1] or "")).strip() for r in pap24_rows])

    # 项目 2021 — 1 条 SQL
    prj_rows = q(f"""SELECT title, keywords FROM gkx.dwd_zh_project
                     WHERE LEFT(CAST(approval_year AS CHAR),4)='{Y_PROJECT}'""")
    prj_cnt, prj_un = count_by_ipc([((r[0] or "") + " " + (r[1] or "")).strip() for r in prj_rows])

    pv_pat = [float(x) for x in pat]
    pv_pap = [float(pap_cnt.get(ipc, 0)) for ipc in panel]
    pv_prj = [float(prj_cnt.get(ipc, 0)) for ipc in panel]
    pv_pap24 = [float(pap24_cnt.get(ipc, 0)) for ipc in panel]

    p_pat, p_pap, p_prj = C.rank_pct(pv_pat), C.rank_pct(pv_pap), C.rank_pct(pv_prj)
    p_pap24 = C.rank_pct(pv_pap24)

    # 主口径：可得维等权（缺失维不参与），另给「缺失维记 0」的对照
    def combine(pp, pq, pr, mode):
        res = []
        for i in range(n):
            vals = [pp[i]]
            if pv_pap[i] > 0:
                vals.append(pq[i])
            if pv_prj[i] > 0:
                vals.append(pr[i])
            res.append(round(sum(vals) / len(vals), 2) if mode == "avail" else round((pp[i] + pq[i] + pr[i]) / 3, 2))
        return res

    main_h = combine(p_pat, p_pap, p_prj, "avail")
    zero_h = combine(p_pat, p_pap, p_prj, "zero")
    v2_h = combine(p_pat, p_pap24, p_prj, "avail")

    rows = [{
        "ipc4": ipc, "patent_2024": pat[i], "patent_org_2024": pat_org[i],
        "paper_2023": int(pv_pap[i]), "project_2021": int(pv_prj[i]),
        "pct_patent": p_pat[i], "pct_paper": p_pap[i], "pct_project": p_prj[i],
        "n_dims": 1 + (1 if pv_pap[i] > 0 else 0) + (1 if pv_prj[i] > 0 else 0),
        "heat": main_h[i], "heat_zero_dim": zero_h[i], "heat_v2_paper2024": v2_h[i],
    } for i, ipc in enumerate(panel)]
    rows.sort(key=lambda r: -r["heat"])

    def topk(k):
        return rows[:k]

    hs = [r["heat"] for r in rows]
    out = {
        "metric_id": METRIC,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "db": {"host": "183.240.141.251:3318", "schema": "gkx",
               "tables": ["dwd_zh_paper", "dwd_zh_project"],
               "patent_source": "_snapshots21/patent_ipc4_year_20261021.json（零专利 SQL）"},
        "support_judgment": "部分支持",
        "judgment_reason": (
            "三维结构齐全、258 个方向均出分，但三源无法取同一年（专利 2024 / 论文 2023 / 项目 2021），"
            "论文维单日批量入库、项目维 2022 起停录，且论文/项目方向归属依赖 Top-1 22.14% 的术语桥；"
            "「全球监测」所需国际语料不具备"
        ),
        "formula": {
            "heat": "Heat_i = mean_{s∈可得维} pct_s(x_{i,s})，" "pct=100*(rank-1)/(n-1)，n=258",
            "reference_years": {"patent": Y_PATENT, "paper": Y_PAPER, "project": Y_PROJECT},
            "normalization": "源内百分位（抗三源量纲差三个数量级）",
        },
        "base_years": C.base_year_block(
            used=[Y_PROJECT, Y_PAPER, Y_PATENT], missing=[],
            note="热度是横截面指标，分母为「258 个面板方向内的排名」，不涉及时序分母；"
                 "三个参考年各自取该源最后一个完整年，异年拼接已在正文披露。"),
        "panel": {"n_ipc4": n, "rule": "2021 与 2024 年专利量均 ≥200 件", "source_rows": C.panel_meta()},
        "sources": {
            "patent": {"year": Y_PATENT, "panel_total": sum(pat),
                       "n_zero": sum(1 for x in pat if x == 0),
                       "org_total": sum(pat_org)},
            "paper": {"year": Y_PAPER, "rows": len(pap_rows), "assigned": len(pap_rows) - pap_un,
                      "unassigned": pap_un,
                      "assigned_rate": round((len(pap_rows) - pap_un) / len(pap_rows), 4) if pap_rows else None,
                      "panel_total": int(sum(pv_pap)), "n_zero": sum(1 for x in pv_pap if x == 0)},
            "paper_2024": {"rows": len(pap24_rows), "unassigned": pap24_un,
                           "panel_total": int(sum(pv_pap24))},
            "project": {"year": Y_PROJECT, "rows": len(prj_rows), "assigned": len(prj_rows) - prj_un,
                        "unassigned": prj_un,
                        "assigned_rate": round((len(prj_rows) - prj_un) / len(prj_rows), 4) if prj_rows else None,
                        "panel_total": int(sum(pv_prj)), "n_zero": sum(1 for x in pv_prj if x == 0)},
        },
        "bridge": {"lexicon_ipc4": C.lexicon()["n_ipc4"], "lexicon_terms": C.lexicon()["n_terms"],
                   "validated_top1": 0.2214, "validated_top3": 0.4154,
                   "source": "缓存词典（_snapshots21/plan_ipc_lexicon_gkx21.json），本次未重扫专利"},
        "result": {
            "distribution": C.st(hs),
            "n_ge60": sum(1 for x in hs if x >= 60), "n_ge80": sum(1 for x in hs if x >= 80),
            "n_dims_1": sum(1 for r in rows if r["n_dims"] == 1),
            "n_dims_2": sum(1 for r in rows if r["n_dims"] == 2),
            "n_dims_3": sum(1 for r in rows if r["n_dims"] == 3),
            "top15": topk(15), "bottom10": rows[-10:], "all": rows,
        },
        "variants": {
            "v1_main": "论文 2023 · 项目 2021 · 可得维等权",
            "v2_paper2024": {"spearman_vs_v1": C.spearman(main_h, v2_h),
                             "top1": max(rows, key=lambda r: r["heat_v2_paper2024"])["ipc4"]},
            "v3_zero_dim": {"spearman_vs_v1": C.spearman(main_h, zero_h),
                            "distribution": C.st(zero_h),
                            "top1": max(rows, key=lambda r: r["heat_zero_dim"])["ipc4"],
                            "max": max(zero_h)},
        },
        "sql_count": 3,
        "elapsed_sec": None,
    }
    out["elapsed_sec"] = round(time.time() - T0, 1)
    C.write_out(METRIC, out)
    print(f"n={n} top1={rows[0]['ipc4']} {rows[0]['heat']} "
          f"paper_un={pap_un}/{len(pap_rows)} proj_un={prj_un}/{len(prj_rows)} in {out['elapsed_sec']}s")


if __name__ == "__main__":
    main()
