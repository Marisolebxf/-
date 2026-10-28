#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_INNOV_PLAN_GROWTH 增长速度
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_INNOV_PLAN_GROWTH.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
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


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题服务算法库', '科技专题系统', '科技信息展示系统']

# 缺省参数：三系统可传子集；快照/探针粒度上不可再分的参数会在 assumptions 显式声明
COMPAT_DEFAULTS = {
    "start_date": None,        # 算法库/展示常传；缺省 → 基线口径窗口（产物 base_years_*）
    "end_date": None,          # 同上；缺省 → 基线口径窗口
    "region": None,            # 地域过滤；缺省 → 全区域（基线口径）
    "industry_tag": None,      # 链/领域标签；缺省 → 全量（基线口径）
    "weights": None,           # 维度权重（模型型指标）；缺省 → 基线内置权重（Q014 类未定项不擅自赋值）
    "dims": None,              # 维度子集（模型型指标）；缺省 → 基线全维度
    "format": None,            # "detail"/"display"；缺省 → 两段都返回
}


def compute(params=None):
    """三系统统一入口：执行基线 main() 的计算逻辑，读取其产物并附兼容元数据返回。

    返回 dict：
      value / detail   : 主值与明细（透传基线产物 headline/stats，数值逐位=基线）
      display          : 展示系统友好结构（headline 精简 + 明细首层序列化）
      assumptions      : 本次运行采用的缺省假设（缺参时非空，前端可提示）
      applicable_systems / params_effective / metric_id / metric_name / generated_at
    典型调用：
      算法库  : compute({"start_date": ..., "end_date": ..., "region": ...})   全参
      专题系统: compute({}) 或 compute({"industry_tag": "..."})               少传参
      展示系统: compute({"format": "display"})                                只要展示段
    """
    import importlib.util, json as _json, time as _time
    from pathlib import Path as _Path

    p_in = dict(params or {})
    eff = {**COMPAT_DEFAULTS, **{k: v for k, v in p_in.items() if v is not None}}
    assumptions = []
    for k, v in eff.items():
        if v is not None and k in ("start_date", "end_date", "region", "industry_tag", "weights", "dims"):
            assumptions.append(f"{k}={v!r} 已接收：本件快照/探针粒度为基线口径，参数生效范围见同名 md「入参兼容策略」"
                               "（不可再分时返回基线口径值并在此声明）")
    assumptions.append("本件为 20261021 基线口径包装（兼容层不改数学定义）；三系统主值同源")

    t0 = _time.time()
    here = _Path(__file__).resolve().parent
    out_json = here / "M_INNOV_PLAN_GROWTH_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_INNOV_PLAN_GROWTH.py 等价）
        run_baseline()
    data = _json.loads(out_json.read_text(encoding="utf-8"))

    headline = data.get("headline") or {}
    value = headline.get("value") if isinstance(headline, dict) and "value" in headline else None
    if value is None and isinstance(headline, dict):
        value = next((headline[k] for k in ("total_le2024", "total", "sz_total", "score", "index", "n", "count")
                      if k in headline and isinstance(headline[k], (int, float))), None)
    if value is None:   # 无 headline 结构的产物：从顶层常见键提取（KPI/分布型）
        for k in ("total", "value", "n_total", "count", "org_total", "sz_total", "sum", "amount"):
            v = data.get(k)
            if isinstance(v, (int, float)):
                value = v
                break
            if isinstance(v, dict):
                for kk in ("total", "value", "n", "sz"):
                    if isinstance(v.get(kk), (int, float)):
                        value = v[kk]
                        break
                if value is not None:
                    break
    if value is None:   # 探针/分布型产物：从 population / audit_chain / probe 找主计数
        for sec in ("population", "audit_chain", "probe", "stats"):
            v = data.get(sec)
            if isinstance(v, dict):
                for kk in ("distinct_org_id", "total", "n", "count", "org_count", "rows",
                           "filled", "polar_rows", "chain_members_total"):
                    if isinstance(v.get(kk), (int, float)):
                        value = v[kk]
                        break
            if value is not None:
                break
    if value is None:   # 兜底声明：无单一主值（分布/明细型产物），value=None 属正常而非错误
        assumptions.append("本件为分布/明细型产物（无单一主值键），value=None；调用方请消费 detail/display 段")
    detail = {k: data[k] for k in ("stats", "facts", "population", "rule", "support_judgment",
                                   "base_years_used", "base_years_missing", "sources") if k in data}
    display = {"headline": headline, "rows_preview": None}
    for k in ("chains", "rows", "items", "list", "ranking", "detail_list"):
        if isinstance(data.get(k), list):
            display["rows_preview"] = {"key": k, "n": len(data[k]), "sample": data[k][:5]}
            break
    if eff.get("format") == "display":
        detail = {"support_judgment": data.get("support_judgment")}
    return {
        "metric_id": "M_INNOV_PLAN_GROWTH",
        "metric_name": data.get("metric_name"),
        "applicable_systems": APPLICABLE,
        "params_effective": eff,
        "assumptions": assumptions,
        "value": value,
        "detail": detail,
        "display": display,
        "generated_at": _time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_sec": round(_time.time() - t0, 2),
        "baseline_generated_at": data.get("generated_at"),
    }


def run_baseline():
    """原样执行基线 main()（兼容层调用；产物 _out.json 由基线逻辑写盘，铁律：产物只由脚本产出）。"""
    main()  # noqa: F821  ← 基线入口（上方原代码定义）
