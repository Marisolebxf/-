#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_INNOV_TINN_PATENT_COUNT 专利数量
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_INNOV_TINN_PATENT_COUNT.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_INNOV_TINN_PATENT_COUNT · 专利数量（判：部分支持）

口径真源：`metrics/calc-logic/INNOV/M_INNOV_TINN_PATENT_COUNT` 并入 TINN_COMPOSITE 的
「专利数量（规模）」维：一行一个 IPC4，含申请量与授权量。

零 SQL：申请量取全表面板 `patent_panel_innov_20261021.json`（2,939,895 行，100% 扫描）；
授权量只有全域口径（`star_applicant_agg_gkx.json` 的 `agg[nm][1]` 合计 2,140,420），
**不能按 IPC4 拆**，故本文件只交付申请量维 + 全域授权率，并按此降档。

运行：python3 code/M_INNOV_TINN_PATENT_COUNT.py
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _tail21_common as T  # noqa: E402

MID = "M_INNOV_TINN_PATENT_COUNT"
TOTAL_ROWS = 2_939_895


def main() -> None:
    panel = json.loads((T.SNAP / "patent_panel_innov_20261021.json").read_text(encoding="utf-8"))
    iy = panel["ipc_year"]                       # "year|IPC4" -> 件数
    year_all = {int(k): int(v) for k, v in panel["year_all"].items()}
    ipc_all = {k: int(v) for k, v in panel["ipc_all"].items()}

    per: dict[str, dict[int, int]] = {}
    for k, n in iy.items():
        y, _, ipc = k.partition("|")
        per.setdefault(ipc, {})[int(y)] = int(n)
    ipc_sum = sum(sum(v.values()) for v in per.values())

    agg = json.loads((T.SNAP / "star_applicant_agg_gkx.json").read_text(encoding="utf-8"))["agg"]
    pub_total = sum(v[0] for v in agg.values())
    grant_total = sum(v[1] for v in agg.values())

    # 域排名：以 2021—2024 四年合计（2025/2026 不完整，不进排名分母）
    real_years = [2021, 2022, 2023, 2024]
    tot24 = sum(v.get(2024, 0) for v in per.values()) or 1
    hhi = sum((v.get(2024, 0) / tot24) ** 2 for v in per.values())
    window_rows = sum(year_all[y] for y in real_years)
    window_tagged = sum(sum(v.get(y, 0) for y in real_years) for v in per.values())
    ranking = sorted(per.items(), key=lambda kv: -sum(kv[1].get(y, 0) for y in real_years))
    rows = []
    for ipc, ser in ranking[:40]:
        c21, c24 = ser.get(2021, 0), ser.get(2024, 0)
        rows.append({
            "ipc4": ipc,
            "n_2021": c21, "n_2022": ser.get(2022, 0), "n_2023": ser.get(2023, 0),
            "n_2024": c24, "n_2025": None, "n_2026": None,
            "sum_2021_2024": sum(ser.get(y, 0) for y in real_years),
            "growth_2021_2024_pct": round(100 * (c24 - c21) / c21, 2) if c21 else None,
            "cagr_2021_2024_pct": round(100 * ((c24 / c21) ** (1 / 3) - 1), 2) if c21 else None,
            "share_2024_pct": round(100 * c24 / tot24, 3),
        })

    res = {
        "metric_id": MID,
        "metric_name": "专利数量",
        "support_judgment": "部分支持",
        "object": "技术领域（IPC 主分类前 4 位）× 申请年",
        "verdict_reason": (
            "申请量维完全可算（全表面板 2,939,895 行，IPC4×年 2,456 格）；"
            "授权量维无法按 IPC4 拆——库内只有全域授权数 2,140,420（授权率 72.81%）与"
            "按申请人的授权数，没有任何缓存带「IPC4×年×授权」。要拆必须对 294 万行主表按 "
            "granted_number 做全表聚合，实测该类查询 600 秒断连（DATA_FACTS §3.6/§3.12），故不执行。"
            "两个子项缺一，按档位定义落「部分支持」"),
        "data_source": "code/_snapshots21/patent_panel_innov_20261021.json（全量 2,939,895 行）；"
                       "star_applicant_agg_gkx.json（授权数合计）",
        "sql_count": 0,
        "probe": {
            "patent_rows": TOTAL_ROWS,
            "panel_rows": panel["rows"],
            "panel_chunks": panel["chunks"],
            "panel_partial": panel["rows"] < TOTAL_ROWS,
            "ipc4_distinct": len(per),
            "ipc_year_cells": len(iy),
            "ipc_all_rows_all_years": sum(ipc_all.values()),
            "ipc_year_window": panel["window"],
            "ipc_tagged_rows_window": window_tagged,
            "ipc_window_rows": window_rows,
            "ipc_tagged_pct_window": round(100 * window_tagged / window_rows, 2),
            "ipc_untagged_rows_window": window_rows - window_tagged,
            "ipc_2025_2026_breakdown": "面板未采（window 仅 2021—2024），2025/2026 的 IPC4 序列不可从缓存取",
            "applicants": len(agg),
            "grant_total": grant_total,
            "grant_rate_pct": round(100 * grant_total / pub_total, 2),
            "hhi_2024_ipc4": round(hhi, 4),
            "effective_domains_2024": round(1 / hhi, 1),
        },
        "year_all": {str(k): v for k, v in sorted(year_all.items())},
        "type_by_year": {str(k): v for k, v in sorted(panel["year_all"].items())},
        "top_ipc4": rows,
        "growth": {
            "base_window": [2021],
            "end_year": 2024,
            "note": "库内专利只覆盖 2021—2026；2021 是唯一可用基线年，故 CAGR 分母只有 2021 单年，"
                    "不是五年均值。2025（440,401）与 2026（74,810）为不完整年，不进增速",
        },
        "base_years_used": [2021, 2022, 2023, 2024],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_year_block": T.base_year_block(
            [2021, 2022, 2023, 2024], [2017, 2018, 2019, 2020],
            "gkx.dwd_patent 的 apdt_year 只有 2021—2026；2017—2020 零行，任何「五年基线」都不成立，"
            "CAGR 分母只能用 2021 单年"),
        "coverage": {
            "apply_dim": "全量：面板 2,939,895/2,939,895 = 100%",
            "ipc_dim": f"2021—2024 窗口内主分类 IPC4 已标注 {window_tagged:,}/{window_rows:,} = "
                       f"{round(100 * window_tagged / window_rows, 2)}%；全表（含 2025/2026）"
                       f"{sum(ipc_all.values()):,}/{TOTAL_ROWS:,} = "
                       f"{round(100 * sum(ipc_all.values()) / TOTAL_ROWS, 2)}%",
            "grant_dim": "仅全域（2,140,420 件 / 72.81%），无 IPC4 拆分",
            "year_dim": "2021—2026 六档，其中 2025/2026 不完整",
        },
        "gaps": [
            "授权量不可按 IPC4 拆：需供应方提供 IPC4×年×授权号非空的聚合结果表",
            f"2021—2024 窗口内 {window_rows - window_tagged:,} 行无主分类 IPC（"
            f"{round(100 * (window_rows - window_tagged) / window_rows, 2)}%），按 IPC4 排名时分母不是全表",
            "2025/2026 的 IPC4×年明细不在面板 window 内，只有全表 IPC4 合计",
            "2017—2020 零行，无法做五年趋势或五年基线",
            "2025（440,401）与 2026（74,810）为截断年，不能与 2021—2024 直接同比",
        ],
        "repair_requirements": [
            "补 IPC4×年×授权量结果表（或给 dwd_patent.apdt_year/main_classification_ipcr 建联合索引）",
            "补 2020 及以前年度的专利行，才能支撑五年基线",
        ],
    }
    T.write_out(MID, res)
    print(json.dumps(res["probe"], ensure_ascii=False, indent=1))
    print(rows[:5])


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
    out_json = here / "M_INNOV_TINN_PATENT_COUNT_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_INNOV_TINN_PATENT_COUNT.py 等价）
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
        "metric_id": "M_INNOV_TINN_PATENT_COUNT",
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
