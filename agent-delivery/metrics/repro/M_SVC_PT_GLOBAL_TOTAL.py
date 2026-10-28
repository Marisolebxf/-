#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_SVC_PT_GLOBAL_TOTAL 全球服务机构总数
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统
# 【差异分级】D5 表述级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_SVC_PT_GLOBAL_TOTAL.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""全球服务机构总数（M_SVC_PT_GLOBAL_TOTAL）—— gkx 口径，自包含。

数据源（只读落盘快照，零 SQL、零 demo）：
    code/_snapshots21/svc21_facts_20261022.json
        source: gkx @183.240.141.251:3318（gkx_reader_zp，只读）
        pool  = gkx.dwd_org_org_product_info（45,011 行 / 44,153 个 org_id）
    code/_snapshots21/base_20261021.json          底册 189,116 行（城市/省/成立年）
    code/_snapshots21/svc21_pt_axis_20261022.json 海外国别值域（dwd_forg_base_info）

口径（沿用 calc-logic 0.2.0 的「存量值 + 成立年累积序列」骨架，人口换源）：
    值      = COUNT(DISTINCT org_id) over 服务机构池（时点存量，含无成立年者）
    序列    = 按底册 incorporation_year 的累积存量 Sn = sum_{y<=n} births_y
              （births-only：gkx 无注销/死亡字段，只增不减，正文披露）
    年份    = 只遍历库内真实存在的年（1951—2025），缺失年不补 0（DATA_FACTS §3.16）
    海外    = dwd_forg_base_info 20,000 行但只有 GB/US/CA 三国且非服务名录 → 增量项

产出：code/M_SVC_PT_GLOBAL_TOTAL_out.json（覆盖写）
运行：cd code && python3 M_SVC_PT_GLOBAL_TOTAL.py
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
BASE = os.path.join(SNAP, "base_20261021.json")
AXIS = os.path.join(SNAP, "svc21_pt_axis_20261022.json")
OUT = os.path.join(HERE, "M_SVC_PT_GLOBAL_TOTAL_out.json")


def main():
    t0 = time.time()
    fact = json.load(open(FACTS, encoding="utf-8"))
    base = json.load(open(BASE, encoding="utf-8"))
    ax = json.load(open(AXIS, encoding="utf-8"))
    pool = fact["pool"]
    bmap = {r[0]: r for r in base}

    n_pool = len(pool)
    sz = [o for o, v in pool.items() if v.get("city") == "深圳市"]
    joined = sum(1 for o in pool if o in bmap)

    # ---------------- 成立年累积序列（只遍历真实年份）
    births = Counter(v["inc_year"] for v in pool.values() if v.get("inc_year"))
    years = sorted(births)
    lo, hi = years[0], years[-1]
    missing = [y for y in range(lo, hi + 1) if y not in births]
    acc, series = 0, []
    for y in range(lo, hi + 1):
        acc += births.get(y, 0)
        series.append([y, acc])
    no_year = sum(1 for v in pool.values() if not v.get("inc_year"))
    last_year, last_val = series[-1]

    # ---------------- 海外轴（值域证据，不是名录）
    forg = ax["forg_country"]

    out = {
        "metric_id": "M_SVC_PT_GLOBAL_TOTAL",
        "metric_name": "全球服务机构总数",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": (
            "境内口径的存量值与成立年累积序列均可现转（池 44,153 家、可回查率 99.95%、"
            "64 个有值年份、期末 44,132＋无年份 21＝池全对账）；"
            "但「全球」所需的境外服务机构名录在 gkx 无源——dwd_forg_base_info 20,000 行只有 "
            "GB/US/CA 三个国别值且与服务机构池无对齐键，故海外轴无法并入 → 部分支持"),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_org_product_info", "rows": fact["population"]["product_info_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_base_info（省/市/成立年）", "rows": fact["population"]["base_all"],
             "snapshot": "code/_snapshots21/base_20261021.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_forg_base_info（国别值域）", "rows": forg["rows_total"],
             "snapshot": "code/_snapshots21/svc21_pt_axis_20261022.json"},
        ],
        "base_years_used": [lo, hi],
        "base_years_missing": missing,
        "base_years_note": (
            "存量序列按成立年累积，库内真实有出生记录的年份为 %d—%d（%d 个有值年）；"
            "区间内 %d 个年份零出生（不补 0、不进分母），无成立年的 %d 家机构计入存量值"
            "但不进序列（值−序列期末＝%d，口径差而非缺失）。%d 年之后无出生记录是底册"
            "登记滞后所致，不解读为「新增归零」。"
            % (lo, hi, len(years), len(missing), no_year, n_pool - last_val, hi)),
        "population": {
            "defined_as": ("gkx.dwd_org_org_product_info 中 is_deleted=0 且有 main_activities 的机构，"
                           "按 org_id 去重"),
            "product_info_rows": fact["population"]["product_info_all"],
            "distinct_org_id": n_pool,
            "join_base_rows": joined,
            "join_base_rate": round(joined / n_pool, 6),
            "shenzhen_orgs": len(sz),
            "shenzhen_share": round(len(sz) / n_pool, 6),
        },
        "value_domestic": n_pool,
        "series": {
            "periods": len(series),
            "first_year": lo,
            "last_year": last_year,
            "last_value": last_val,
            "coverage_years": len(years),
            "by_year": series,
        },
        "reconcile": {
            "with_incorporation_year": last_val,
            "without_incorporation_year": no_year,
            "sum_equals_pool": last_val + no_year == n_pool,
            "delta_value_minus_series": n_pool - last_val,
        },
        "oversea_axis": {
            "needed": "境外/港澳台服务机构名录（含 org 标识与国别）",
            "existing": "gkx.dwd_forg_base_info %d 行，国别值域 %s"
                        % (forg["rows_total"], forg["dist"]),
            "verdict": ("不是服务机构名录：只有 GB/US/CA 三值、country 列全空，"
                        "且与 dwd_org_base_info 无可用对齐键 → 海外不能并入总量"),
            "impact": "本值是全球总量的下界（境内全量），页面须标「境内口径」",
        },
        "difference_vs_old_draft": {
            "population": "旧稿 43,296（演示库人工圈选名单）→ 本件 44,153（gkx 经营范围实体，按 org_id 去重）",
            "series": "旧稿 49 期（1978—2026，演示库 ADS 序列面）→ 本件 64 个有值年（1951—2025，底册成立年实算）",
            "oversea": "旧稿「境外表 0 行」→ 本件「境外表 20,000 行但只有 3 国且非服务名录」：结论同向、原因不同",
        },
        "compute": {"status": "ok", "elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("pool=%d sz=%d join=%d (%.2f%%) series=%d期 %d—%d 期末=%d 无年份=%d"
          % (n_pool, len(sz), joined, 100.0 * joined / n_pool, len(series), lo, hi,
             last_val, no_year))
    print("->", OUT)


if __name__ == "__main__":
    main()


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题服务算法库', '科技专题系统']

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
    out_json = here / "M_SVC_PT_GLOBAL_TOTAL_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_SVC_PT_GLOBAL_TOTAL.py 等价）
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
        "metric_id": "M_SVC_PT_GLOBAL_TOTAL",
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
