#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_INNOV_PG_PROJECT 项目支持
# 【维护者】唐绍祖
# 【适用系统】科技专题系统 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_INNOV_PG_PROJECT.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_INNOV_PG_PROJECT —— 项目支持（三方库 gkx 版）。

口径：`gkx.dwd_zh_project` 58,453 条项目记录 × 6 个统计格（类型/机构/时间/学科/数量/金额）
+ 1 个打分（学科支持度 = 0.5×项目数百分位 + 0.5×金额百分位）+ 1 个覆盖度量（实施效果）。
共 6 条 SQL，全部打在小表（58,453 / 20,133 行），单条限时 60 秒。
"""
from __future__ import annotations

import time
from pathlib import Path

import _gkxdb as D
import _plan21_common as C

METRIC = "M_INNOV_PG_PROJECT"
T0 = time.time()


def q(sql: str, args=None) -> list[tuple]:
    cur = D.gkx()
    try:
        cur.execute("SET SESSION max_execution_time=60000")
        cur.execute(sql, args or ())
        return list(cur.fetchall())
    finally:
        cur.close()


def main() -> None:
    # 1) 盘子与填充率 -------------------------------------------------------
    n, amt_ok, disc_ok, prov_ok, inst_ok, part_ok = q("""
        SELECT COUNT(*), SUM(funded_amount>0),
               SUM(discipline IS NOT NULL AND discipline<>'' AND UPPER(TRIM(discipline)) NOT IN ('NULL','NONE','-')),
               SUM(funded_province IS NOT NULL AND funded_province<>'' AND UPPER(TRIM(funded_province)) NOT IN ('NULL','NONE','-')),
               SUM(funded_institution IS NOT NULL AND funded_institution<>'' AND UPPER(TRIM(funded_institution)) NOT IN ('NULL','NONE','-')),
               SUM(participating_institution IS NOT NULL AND participating_institution<>'')
        FROM gkx.dwd_zh_project""")[0]
    n, amt_ok, disc_ok, prov_ok, inst_ok, part_ok = int(n), int(amt_ok), int(disc_ok), int(prov_ok), int(inst_ok), int(part_ok)

    # 2) 类型 ---------------------------------------------------------------
    cat = q("""SELECT fund_category, COUNT(*), SUM(funded_amount), AVG(funded_amount)
               FROM gkx.dwd_zh_project GROUP BY 1 ORDER BY 2 DESC""")
    total_amt = sum(float(r[2] or 0) for r in cat)

    # 3) 机构 / 层级 --------------------------------------------------------
    src = q("""SELECT project_source, project_level, COUNT(*)
               FROM gkx.dwd_zh_project GROUP BY 1,2 ORDER BY 3 DESC""")

    # 4) 年份 ---------------------------------------------------------------
    yrow = q("""SELECT LEFT(CAST(approval_year AS CHAR),4) y, COUNT(*), SUM(funded_amount)
                FROM gkx.dwd_zh_project GROUP BY 1 ORDER BY 1""")
    years = [(int(r[0]), int(r[1]), float(r[2] or 0)) for r in yrow if r[0] and r[0].isdigit()]
    ymap = {y: (c, a) for y, c, a in years}

    # 5) 学科 ---------------------------------------------------------------
    disc = q("""SELECT SUBSTRING_INDEX(discipline,'-',1) major, COUNT(*), SUM(funded_amount)
                FROM gkx.dwd_zh_project
                WHERE discipline IS NOT NULL AND discipline<>''
                  AND UPPER(TRIM(discipline)) NOT IN ('NULL','NONE','-')
                GROUP BY 1 ORDER BY 2 DESC""")
    names = [r[0] for r in disc]
    ns = [int(r[1]) for r in disc]
    amts = [float(r[2] or 0) for r in disc]
    pn, pa = C.rank_pct([float(x) for x in ns]), C.rank_pct(amts)
    disc_rows = [
        {"discipline": names[i], "n": ns[i], "amount_wan": round(amts[i], 1),
         "avg_wan": round(amts[i] / ns[i], 1) if ns[i] else None,
         "pct_n": pn[i], "pct_amount": pa[i], "support_score": round(0.5 * pn[i] + 0.5 * pa[i], 2)}
        for i in range(len(names))
    ]
    disc_rows.sort(key=lambda r: -r["support_score"])

    # 6) 实施效果覆盖 -------------------------------------------------------
    prj, with_out, journals, patents, awards, total_out = q("""
        SELECT COUNT(*), SUM(o.id IS NOT NULL),
               SUM(o.journal_articles_count), SUM(o.patents_count),
               SUM(o.awards_count), SUM(o.total_outputs)
        FROM gkx.dwd_zh_project p
        LEFT JOIN gkx.dwd_zh_project_output o ON o.id=p.id""")[0]
    prj, with_out = int(prj), int(with_out or 0)

    n_recent = sum(c for y, c, _ in years if y >= 2020)  # 用四位年比较，避开 YYYYMMDD 整数比较失效
    year_used = [y for y, c, _ in years if c > 0]
    year_missing = [y for y in range(2024, 2027)]

    out = {
        "metric_id": METRIC,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "db": {"host": "183.240.141.251:3318", "schema": "gkx", "tables": ["dwd_zh_project", "dwd_zh_project_output"]},
        "support_judgment": "部分支持",
        "judgment_reason": (
            "数量/金额/类型/学科四格完整（58,453 条、2,529,097.1 万元、8 类、119 个一级学科），"
            "但需求明列的「产业项目」0 条、资助机构与项目层级各只有 1 个取值（维度退化）、"
            "funded_province/funded_institution 整列为空（0 填充）、时间在 2021 年截断、"
            "实施效果只覆盖 34.33% 且奖励合计为 0"
        ),
        "base": {"n_projects": n, "amount_wan": round(total_amt, 1),
                 "avg_wan": round(total_amt / n, 2) if n else None},
        "fill": {"funded_amount_gt0": amt_ok, "discipline": disc_ok, "funded_province": prov_ok,
                 "funded_institution": inst_ok, "participating_institution": part_ok,
                 "participation_rate": round(part_ok / n, 4) if n else None,
                 "discipline_rate": round(disc_ok / n, 4) if n else None},
        "dim_category": [{"category": r[0], "n": int(r[1]), "amount_wan": round(float(r[2] or 0), 1),
                          "avg_wan": round(float(r[3] or 0), 2),
                          "share_n": round(int(r[1]) / n, 4),
                          "share_amount": round(float(r[2] or 0) / total_amt, 4)} for r in cat],
        "dim_source": [{"source": r[0], "level": r[1], "n": int(r[2])} for r in src],
        "n_source_values": len({r[0] for r in src}),
        "n_level_values": len({r[1] for r in src}),
        "dim_year": [{"year": y, "n": c, "amount_wan": round(a, 1)} for y, c, a in years],
        "n_recent_ge_2020": n_recent,
        "discipline_support": {
            "n_disciplines": len(disc_rows),
            "formula": "support = 0.5*pct(n) + 0.5*pct(amount)",
            "distribution": C.st([r["support_score"] for r in disc_rows]),
            "top10": disc_rows[:10],
            "bottom5": disc_rows[-5:],
        },
        "effect": {"projects": prj, "with_output": with_out,
                   "coverage": round(with_out / prj, 4) if prj else None,
                   "sum_journal_articles": int(journals or 0), "sum_patents": int(patents or 0),
                   "sum_awards": int(awards or 0), "sum_total_outputs": int(total_out or 0),
                   "avg_journal_per_covered": round(float(journals or 0) / with_out, 2) if with_out else None,
                   "avg_patent_per_covered": round(float(patents or 0) / with_out, 2) if with_out else None,
                   "sum_awards_note": "产出表 awards_count 合计为 0，是字段未采集，不是「没有获奖」"},
        "base_years": C.base_year_block(
            used=[min(year_used), max(year_used)] if year_used else [],
            missing=year_missing,
            note="项目年表覆盖 1986—2023；2024—2026 无记录（录入停摆），任何「近年项目强度」不得把这三年按 0 摊入分母。"),
        "sql_count": 6,
        "elapsed_sec": None,
    }
    out["elapsed_sec"] = round(time.time() - T0, 1)
    C.write_out(METRIC, out)
    print(f"n={n} amount={total_amt:.1f}wan cat={len(cat)} disc={len(disc_rows)} cover={with_out}/{prj} in {out['elapsed_sec']}s")


if __name__ == "__main__":
    main()


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题系统', '科技信息展示系统']

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
    out_json = here / "M_INNOV_PG_PROJECT_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_INNOV_PG_PROJECT.py 等价）
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
        "metric_id": "M_INNOV_PG_PROJECT",
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
