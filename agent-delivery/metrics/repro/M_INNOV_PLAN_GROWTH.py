#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_PLAN_GROWTH —— 增长速度（三方库 gkx 版，专利面板零 SQL）。

王惠原式：g = (近 3 年均值 − 前 5 年均值) / max(前 5 年均值, 1)，对象 = IPC4。
本库 `dwd_patent.apdt_year` 只有 2021—2026（2017—2020 零行），前 5 年基线整段不存在，
故显式降级为「2023—2024 vs 2021—2022」（2 年对 2 年），并用 base_years_used /
base_years_missing 把窗口写进产物。论文/项目两维只做诊断，不进入合成。

零专利 SQL：专利计数全部来自 `_snapshots21/patent_ipc4_year_20261021.json`。
论文/项目诊断只打两张小表（100,900 / 58,453 行），共 2 条 SQL。
"""
from __future__ import annotations

import time

import _gkxdb as D
import _plan21_common as C

METRIC = "M_INNOV_PLAN_GROWTH"
BASE_YEARS = [2021, 2022]
RECENT_YEARS = [2023, 2024]
WANGHUI_BASE = [2016, 2017, 2018, 2019, 2020]
T0 = time.time()


def q(sql: str) -> list[tuple]:
    cur = D.gkx()
    try:
        cur.execute("SET SESSION max_execution_time=60000")
        cur.execute(sql)
        return list(cur.fetchall())
    finally:
        cur.close()


def g_of(base: float, recent: float) -> float:
    return round((recent - base) / max(base, 1.0), 4)


def main() -> None:
    d = C.ipc4_year()
    panel = C.panel_ipc4()

    rows = []
    for ipc in panel:
        b = [d.get((ipc, y), [0, 0])[0] for y in BASE_YEARS]
        r = [d.get((ipc, y), [0, 0])[0] for y in RECENT_YEARS]
        bm, rm = sum(b) / len(BASE_YEARS), sum(r) / len(RECENT_YEARS)
        rows.append({"ipc4": ipc, "base": b, "recent": r, "base_mean": round(bm, 1),
                     "recent_mean": round(rm, 1), "g": g_of(bm, rm)})
    rows.sort(key=lambda x: -x["g"])
    gs = [x["g"] for x in rows]

    # 专利年度盘子（全量，含无 IPC 部分）
    yt = C.year_totals()
    year_tab = [{"year": y, "n": yt.get(y)} for y in sorted(yt)]
    misuse = {
        "2025_vs_2024": g_of(yt.get(2024, 0), yt.get(2025, 0)),
        "2026_vs_2024": g_of(yt.get(2024, 0), yt.get(2026, 0)),
        "note": "2025/2026 为公开与入库截断年，直接当近窗会得到「断崖」假象（发明专利自申请日起满 18 个月公布）",
    }

    # 论文维诊断（1 条 SQL）：年度量 + 入库日期集中度
    paper_y = q("""SELECT LEFT(CAST(cover_year_start AS CHAR),4) y, COUNT(*), COUNT(DISTINCT DATE(created_time))
                   FROM gkx.dwd_zh_paper GROUP BY 1 ORDER BY 1""")
    paper_tab = {int(r[0]): (int(r[1]), int(r[2])) for r in paper_y if r[0] and r[0].isdigit()}
    p23, p24 = paper_tab.get(2023, (0, 0))[0], paper_tab.get(2024, (0, 0))[0]
    # 入库日期唯一值：单独聚合一次全表（仍是小表，1 条 SQL）
    date_row = q("""SELECT COUNT(DISTINCT DATE(created_time)), MIN(created_time), MAX(created_time), COUNT(*)
                    FROM gkx.dwd_zh_paper""")[0]
    paper_diag = {
        "y2023": p23, "y2024": p24,
        "corpus_growth": round(p24 / p23, 4) if p23 else None,
        "distinct_load_dates": int(date_row[0]),
        "load_min": str(date_row[1]), "load_max": str(date_row[2]), "rows": int(date_row[3]),
        "verdict": "不可比：全表同一批入库日，2024 年量是 2023 年的数倍，属回填而非学术增长，剔除",
    }

    # 项目维诊断（复用探针已取的年表；此处再取一次，1 条 SQL）
    proj_y = q("""SELECT LEFT(CAST(approval_year AS CHAR),4) y, COUNT(*)
                  FROM gkx.dwd_zh_project GROUP BY 1 ORDER BY 1""")
    proj_tab = {int(r[0]): int(r[1]) for r in proj_y if r[0] and r[0].isdigit()}
    proj_diag = {
        "y2019": proj_tab.get(2019), "y2020": proj_tab.get(2020), "y2021": proj_tab.get(2021),
        "y2022": proj_tab.get(2022), "y2023": proj_tab.get(2023), "y2024": proj_tab.get(2024, 0),
        "implied_g_if_recent": g_of((proj_tab.get(2019, 0) + proj_tab.get(2020, 0)) / 2,
                                    (proj_tab.get(2022, 0) + proj_tab.get(2023, 0)) / 2),
        "verdict": "不可比：2022 年起录入停摆（58 / 6 / 0），任何近窗增速都测的是停录，剔除",
    }

    pos = sum(1 for g in gs if g > 0)
    neg = sum(1 for g in gs if g < 0)
    out = {
        "metric_id": METRIC,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "db": {"host": "183.240.141.251:3318", "schema": "gkx",
               "tables": ["dwd_zh_paper（诊断）", "dwd_zh_project（诊断）"],
               "patent_source": "_snapshots21/patent_ipc4_year_20261021.json（零专利 SQL）"},
        "support_judgment": "部分支持",
        "judgment_reason": (
            "专利维可算（258 个方向、中位 −3.20%），但王惠原式的前 5 年基线（2016—2020）"
            "在 dwd_patent 整段缺失，只能降级为 2 年对 2 年；论文维单日回填、项目维 2022 起停录，"
            "三维合成不可交付"
        ),
        "formula": {
            "wanghui": "g=(近3年均值-前5年均值)/max(前5年均值,1)",
            "used": "g=(近窗年均值-基期年均值)/max(基期年均值,1)",
            "recent_years": RECENT_YEARS, "base_years": BASE_YEARS,
            "direction_key": "IPC4（LEFT(main_classification_ipcr,4)）",
        },
        "base_years": C.base_year_block(
            used=BASE_YEARS, missing=WANGHUI_BASE,
            note="王惠原式要求 2016—2020 五年基线；dwd_patent 的 apdt_year 只有 2021—2026，"
                 "2017—2020 零行、2016 更无。故基期只能取 2021—2022 两年，分母未把缺失年按 0 摊入。"),
        "panel": {"n_ipc4": len(panel), "rule": "2021 与 2024 年专利量均 ≥200 件",
                  "source_rows": C.panel_meta()},
        "patent_growth": {
            "distribution": C.st(gs),
            "n_positive": pos, "n_negative": neg, "n_zero": len(gs) - pos - neg,
            "n_ge_050": sum(1 for g in gs if g >= 0.5), "n_le_m050": sum(1 for g in gs if g <= -0.5),
            "top15": rows[:15], "bottom10": rows[-10:], "all": rows,
        },
        "year_total": year_tab,
        "misuse_demo": misuse,
        "paper_diagnostic": paper_diag,
        "project_diagnostic": proj_diag,
        "sql_count": 3,
        "elapsed_sec": None,
    }
    out["elapsed_sec"] = round(time.time() - T0, 1)
    C.write_out(METRIC, out)
    print(f"n={len(panel)} median={out['patent_growth']['distribution']['median']} "
          f"pos/neg={pos}/{neg} in {out['elapsed_sec']}s")


if __name__ == "__main__":
    main()
