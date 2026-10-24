#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_PLAN_DIRECTION_ALERT —— 潜在科技发展方向预警（三方库 gkx 版）。

王惠口径：IPC4 为方向主键，六源（专利/论文/项目/人才/产业/政策）近窗相对基线增速加权得 F，
F≥1 且两源 g>0 → 2 级；F≥0.5 → 1 级；否则 0 级。

本库现实：专利/产业（活跃申请机构）来自面板缓存（零专利 SQL）；论文、项目、政策可经缓存术语桥
归到 IPC4 但年度不可比；人才源无「学者→IPC4」映射。故并列交付：
  A 套 = 王惠原式字面执行（可用五源等权），用于证明规则在本库失效；
  B 套 = 仅保留通过信息量检验的专利 + 产业，源内百分位 + P90/P75 分级。

SQL 预算：论文 / 项目 / 政策 / 人才形态共 4 条，全部小表。
"""
from __future__ import annotations

import time

import _gkxdb as D
import _plan21_common as C

METRIC = "M_INNOV_PLAN_DIRECTION_ALERT"
T0 = time.time()

# 各源窗口（王惠未规定，本报告按各源最后一个稳定期选取）
WIN = {
    "patent": ([2021, 2022], [2023, 2024]),
    "paper": ([2021, 2022], [2023, 2024]),
    "project": ([2019, 2020], [2022, 2023]),
    "industry": ([2021, 2022], [2023, 2024]),
    "policy": ([2019, 2020], [2021, 2022]),
}


def q(sql: str) -> list[tuple]:
    cur = D.gkx()
    try:
        cur.execute("SET SESSION max_execution_time=60000")
        cur.execute(sql)
        return list(cur.fetchall())
    finally:
        cur.close()


def g(base_vals: list[float], recent_vals: list[float]) -> float:
    b = sum(base_vals) / len(base_vals)
    r = sum(recent_vals) / len(recent_vals)
    return round((r - b) / max(b, 1.0), 4)


def assign_counts(rows, text_fn) -> tuple[dict[str, int], int]:
    cnt: dict[str, int] = {}
    un = 0
    for r in rows:
        top = C.assign_fast(text_fn(r), k=1)
        if not top:
            un += 1
            continue
        cnt[top[0][0]] = cnt.get(top[0][0], 0) + 1
    return cnt, un


def main() -> None:
    d = C.ipc4_year()
    panel = C.panel_ipc4()
    n = len(panel)

    # ---- 专利 / 产业（缓存，零 SQL）----
    pat_g, ind_g = [], []
    for ipc in panel:
        pat_g.append(g([d.get((ipc, y), [0, 0])[0] for y in WIN["patent"][0]],
                       [d.get((ipc, y), [0, 0])[0] for y in WIN["patent"][1]]))
        ind_g.append(g([d.get((ipc, y), [0, 0])[1] for y in WIN["industry"][0]],
                       [d.get((ipc, y), [0, 0])[1] for y in WIN["industry"][1]]))

    # ---- 论文（1 条 SQL，2021—2024）----
    pap_rows = q("""SELECT LEFT(CAST(cover_year_start AS CHAR),4) y, zh_name, en_name
                    FROM gkx.dwd_zh_paper
                    WHERE LEFT(CAST(cover_year_start AS CHAR),4) IN ('2021','2022','2023','2024')""")
    pap_by_year: dict[int, dict[str, int]] = {y: {} for y in (2021, 2022, 2023, 2024)}
    pap_un = 0
    for r in pap_rows:
        y = int(r[0])
        top = C.assign_fast(((r[1] or "") + " " + (r[2] or "")).strip(), k=1)
        if not top:
            pap_un += 1
            continue
        m = pap_by_year[y]
        m[top[0][0]] = m.get(top[0][0], 0) + 1
    pap_g = [g([pap_by_year[y].get(ipc, 0) for y in WIN["paper"][0]],
               [pap_by_year[y].get(ipc, 0) for y in WIN["paper"][1]]) for ipc in panel]

    # ---- 项目（1 条 SQL，2019/2020/2022/2023）----
    prj_rows = q("""SELECT LEFT(CAST(approval_year AS CHAR),4) y, title, keywords
                    FROM gkx.dwd_zh_project
                    WHERE LEFT(CAST(approval_year AS CHAR),4) IN ('2019','2020','2022','2023')""")
    prj_by_year: dict[int, dict[str, int]] = {y: {} for y in (2019, 2020, 2022, 2023)}
    prj_un = 0
    for r in prj_rows:
        y = int(r[0])
        top = C.assign_fast(((r[1] or "") + " " + (r[2] or "")).strip(), k=1)
        if not top:
            prj_un += 1
            continue
        m = prj_by_year[y]
        m[top[0][0]] = m.get(top[0][0], 0) + 1
    prj_g = [g([prj_by_year[y].get(ipc, 0) for y in WIN["project"][0]],
               [prj_by_year[y].get(ipc, 0) for y in WIN["project"][1]]) for ipc in panel]

    # ---- 政策（1 条 SQL，2019—2022；publish_year 有 'NULL' 字面量，显式排除）----
    pol_rows = q("""SELECT publish_year, title FROM gkx.dwd_policy_base
                    WHERE publish_year IN ('2019','2020','2021','2022')""")
    pol_by_year: dict[int, dict[str, int]] = {y: {} for y in (2019, 2020, 2021, 2022)}
    pol_un = 0
    for r in pol_rows:
        y = int(str(r[0]))
        top = C.assign_fast(str(r[1] or ""), k=1)
        if not top:
            pol_un += 1
            continue
        m = pol_by_year[y]
        m[top[0][0]] = m.get(top[0][0], 0) + 1
    pol_g = [g([pol_by_year[y].get(ipc, 0) for y in WIN["policy"][0]],
               [pol_by_year[y].get(ipc, 0) for y in WIN["policy"][1]]) for ipc in panel]

    # ---- 人才源形态（1 条 SQL，证明 ID 宇宙不通）----
    sch = q("""SELECT (SELECT paper_id FROM gkx.dwd_scholar_paper_relation LIMIT 1) rel_paper_id,
                      (SELECT id FROM gkx.dwd_zh_paper LIMIT 1) zh_paper_id,
                      (SELECT fields FROM gkx.dwd_scholar_research_direction LIMIT 1) rd_fields""")[0]
    talent = {
        "status": "不可得",
        "rel_paper_id_sample": str(sch[0]),
        "zh_paper_id_sample": str(sch[1]),
        "relation_id_type": "bigint（19,291,301 形态）",
        "zh_paper_id_type": "varchar（27 位 00002EG… 形态）",
        "research_direction_sample": str(sch[2])[:120],
        "reason": "既无「学者→IPC4」映射表，两套论文 ID 宇宙也不互通（bigint vs 27 位字符串），"
                  "且 research_direction 为英文自由文本、与中文 IPC4 词典不同源；按两跳停记缺口，不做代理。",
    }

    # ---- A 套：王惠原式字面执行（五源可得，等权）----
    srcs = {"patent": pat_g, "paper": pap_g, "project": prj_g, "industry": ind_g, "policy": pol_g}
    F = [round(sum(srcs[s][i] for s in srcs) / len(srcs), 4) for i in range(n)]
    lvl_a = []
    for i in range(n):
        pos = sum(1 for s in srcs if srcs[s][i] > 0)
        lvl_a.append(2 if (F[i] >= 1 and pos >= 2) else (1 if F[i] >= 0.5 else 0))

    def diag(v):
        s = C.st(v)
        s["iqr"] = round((C.pct(v, 0.75) or 0) - (C.pct(v, 0.25) or 0), 4)
        s["pos_share"] = round(sum(1 for x in v if x > 0) / len(v), 4)
        s["informative"] = bool(s["iqr"] > 0.05 and 0.1 < s["pos_share"] < 0.9)
        return s

    diag_a = {s: diag(srcs[s]) for s in srcs}
    diag_a["talent"] = {"status": "不可得"}
    corr = {s: C.spearman(F, srcs[s]) for s in srcs}

    rows_a = [{"ipc4": panel[i], "F": F[i], "level": lvl_a[i],
               **{s: srcs[s][i] for s in srcs}} for i in range(n)]
    rows_a.sort(key=lambda r: -r["F"])
    warned = [r for r in rows_a if r["level"] >= 1]
    warned_neg_patent = [r for r in warned if r["patent"] < 0]

    # ---- B 套：仅专利 + 产业，源内百分位 + P90/P75 ----
    keep = [s for s in ("patent", "industry") if diag_a[s]["informative"]]
    pcts = {s: C.rank_pct([float(x) for x in srcs[s]]) for s in keep}
    Fb = [round(sum(pcts[s][i] for s in keep) / len(keep), 2) for i in range(n)]
    p90, p75 = C.pct(Fb, 0.90), C.pct(Fb, 0.75)
    pat24 = [d.get((ipc, 2024), [0, 0])[0] for ipc in panel]
    lvl_b = []
    for i in range(n):
        if Fb[i] >= p90 and pat24[i] >= 1000:
            lvl_b.append(2)
        elif Fb[i] >= p75:
            lvl_b.append(1)
        else:
            lvl_b.append(0)
    rows_b = [{"ipc4": panel[i], "F": Fb[i], "level": lvl_b[i], "patent_g": pat_g[i],
               "industry_g": ind_g[i], "patent_2024": pat24[i]} for i in range(n)]
    rows_b.sort(key=lambda r: -r["F"])

    out = {
        "metric_id": METRIC,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "db": {"host": "183.240.141.251:3318", "schema": "gkx",
               "tables": ["dwd_zh_paper", "dwd_zh_project", "dwd_policy_base", "dwd_scholar_paper_relation",
                          "dwd_zh_paper（id 形态）", "dwd_scholar_research_direction"],
               "patent_source": "_snapshots21/patent_ipc4_year_20261021.json（零专利 SQL）"},
        "support_judgment": "部分支持",
        "judgment_reason": (
            "六源中仅专利与产业可用且同出 dwd_patent（不独立）；论文单日回填、项目与政策 2022 起停录、"
            "人才无映射。A 套字面执行可跑但 F 的方差被论文维垄断，B 套收缩为两源后仍只能算「原型」"
        ),
        "formula": {
            "wanghui": "F=mean(g_s)；g_s=(近窗年均值-基期年均值)/max(基期年均值,1)；"
                       "level=2 if F>=1 且两源g>0, 1 if F>=0.5, else 0",
            "windows": {k: {"base": v[0], "recent": v[1]} for k, v in WIN.items()},
            "weights_assumed": "A 套五源等权（王惠未给权重）；B 套两源等权",
        },
        "base_years": C.base_year_block(
            used=sorted({y for v in WIN.values() for y in v[0]}),
            missing=[2016, 2017, 2018],
            note="各源窗口不同，基线年按源显式列出；专利/论文/产业基线为 2021—2022（2016—2020 在 dwd_patent 无行），"
                 "项目/政策因停录前移至 2019—2020。缺失年不得按 0 摊入分母。"),
        "panel": {"n_ipc4": n, "rule": "2021 与 2024 年专利量均 ≥200 件", "source_rows": C.panel_meta()},
        "talent": talent,
        "source_diagnostics": diag_a,
        "f_correlation": corr,
        "result_A_literal": {
            "level_counts": {"0": lvl_a.count(0), "1": lvl_a.count(1), "2": lvl_a.count(2)},
            "F_distribution": C.st(F),
            "n_warned": len(warned),
            "n_warned_patent_negative": len(warned_neg_patent),
            "share_warned_patent_negative": round(len(warned_neg_patent) / len(warned), 4) if warned else None,
            "top10_by_F": rows_a[:10],
            "all": rows_a,
        },
        "result_B_recommended": {
            "sources_kept": keep,
            "sources_dropped": [s for s in srcs if s not in keep] + ["talent"],
            "thresholds": {"p90": p90, "p75": p75, "min_patent_2024_for_level2": 1000},
            "level_counts": {"0": lvl_b.count(0), "1": lvl_b.count(1), "2": lvl_b.count(2)},
            "F_distribution": C.st(Fb),
            "patent_vs_industry_spearman": C.spearman(pat_g, ind_g),
            "top15": rows_b[:15],
            "all": rows_b,
        },
        "sql_count": 4,
        "elapsed_sec": None,
    }
    out["elapsed_sec"] = round(time.time() - T0, 1)
    C.write_out(METRIC, out)
    print("A levels", out["result_A_literal"]["level_counts"], "B levels", out["result_B_recommended"]["level_counts"],
          "corrF_paper", corr["paper"], f"{out['elapsed_sec']}s")


if __name__ == "__main__":
    main()
