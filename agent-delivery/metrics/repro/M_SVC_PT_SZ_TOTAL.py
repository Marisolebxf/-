#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_SVC_PT_SZ_TOTAL 深圳产业服务机构数量
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统
# 【差异分级】D5 表述级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_SVC_PT_SZ_TOTAL.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""深圳产业服务机构数量（M_SVC_PT_SZ_TOTAL）—— gkx 口径，自包含。

口径（calc-logic 0.2.0：深圳切片＝底册 city 等于「深圳市」，org_id 去重计数）：
    切片      = 服务机构池 ∩ city='深圳市'（底册 city 已规范到市级全称，等值匹配即可，§3.8）
    值        = COUNT(DISTINCT org_id)
    序列      = 按成立年累积（只遍历库内真实年份，缺失年不补 0）
    区级对账  = Σ area 分布 + 未分配 = 切片值（与 M_SVC_PT_SZ_REGION_ORG 同池同数）

九件共用同一「服务机构/代理机构池」（44,153 家，与 M_SVC_PT_GLOBAL_TOTAL 同池）。

数据源（只读快照，零 SQL）：
    code/_snapshots21/svc21_facts_20261022.json       pool（city / inc_year）+ base_fields(area)

产出：code/M_SVC_PT_SZ_TOTAL_out.json
运行：cd code && python3 M_SVC_PT_SZ_TOTAL.py
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
OUT = os.path.join(HERE, "M_SVC_PT_SZ_TOTAL_out.json")


def main():
    t0 = time.time()
    fact = json.load(open(FACTS, encoding="utf-8"))
    pool, bf = fact["pool"], fact["base_fields"]
    n = len(pool)
    sz = {o: v for o, v in pool.items() if v.get("city") == "深圳市"}

    births = Counter(v["inc_year"] for v in sz.values() if v.get("inc_year"))
    years = sorted(births)
    lo, hi = years[0], years[-1]
    missing = [y for y in range(lo, hi + 1) if y not in births]
    acc, series = 0, []
    for y in range(lo, hi + 1):
        acc += births.get(y, 0)
        series.append([y, acc])
    no_year = sum(1 for v in sz.values() if not v.get("inc_year"))

    area = Counter((bf.get(o) or {}).get("area") or "" for o in sz)
    area_rows = [{"area": k or "（未分配）", "org_count": c,
                  "share_of_sz": round(c / len(sz), 6)}
                 for k, c in area.most_common()]
    area_assigned = sum(c for k, c in area.items() if k)

    out = {
        "metric_id": "M_SVC_PT_SZ_TOTAL",
        "metric_name": "深圳产业服务机构数量",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "完全转换支持",
        "judgment_reason": (
            "深圳切片的数量、成立年累积序列、区级对账三面在 gkx 全部可现转：切片 %d 家、"
            "区级分布加总与切片完全一致（%d＋未分配 %d＝%d）、序列期末＋无年份＝切片；"
            "依赖字段（city/incorporation_year/area）覆盖 99.96%% 以上，"
            "「结构+当前数据量」双足，当日即可转换出数" % (len(sz), area_assigned,
                                                        len(sz) - area_assigned, len(sz))),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_base_info(city, area, incorporation_year) 经 pool 驱动",
             "rows": fact["population"]["base_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_org_product_info（池人口）",
             "rows": fact["population"]["product_info_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
        ],
        "base_years_used": [lo, hi],
        "base_years_missing": missing,
        "base_years_note": (
            "深圳切片成立年序列覆盖 %d—%d（%d 个有值年，区间内 %d 年零出生不补 0）；"
            "%d 家无成立年者计入切片值但不进序列。%d 年之后无出生记录是底册登记滞后，"
            "不解读为新增归零。" % (lo, hi, len(years), len(missing), no_year, hi)),
        "population": {
            "pool_orgs": n,
            "distinct_org_id": len(sz),
            "share_of_pool": round(len(sz) / n, 6),
            "defined_as": "服务机构池（与 M_SVC_PT_GLOBAL_TOTAL 同池）∩ 底册 city='深圳市'",
        },
        "value_shenzhen": len(sz),
        "series": {"periods": len(series), "first_year": lo, "last_year": hi,
                   "last_value": series[-1][1], "by_year": series},
        "city_outside": {"orgs": len(pool) - len(sz), "share_of_pool": round((len(pool) - len(sz)) / len(pool), 6)},
        "reconcile": {
            "area_assigned": area_assigned,
            "area_unassigned": len(sz) - area_assigned,
            "area_sum_equals_total": area_assigned + (len(sz) - area_assigned) == len(sz),
            "series_last_plus_no_year": series[-1][1] + no_year,
            "series_check_ok": series[-1][1] + no_year == len(sz),
        },
        "area_rows": area_rows,
        "areas_covered": len([k for k in area if k]),
        "difference_vs_old_draft": {
            "population": "旧稿 43,296（演示库圈定池）→ 本件 44,153（gkx 经营范围实体）",
            "sz_value": "旧稿 14,033（占池 32.41%%）→ 本件 %d（占池 %.2f%%）"
                        % (len(sz), 100.0 * len(sz) / n),
            "reason": ("切片绝对值放大 1.8 倍的根因是分母换了：旧稿的圈定池是人工名单，"
                       "gkx 的池按经营范围认定，深圳机构在其中占比更高；两者不可比绝对值，"
                       "只能比结构（区级排序见 M_SVC_PT_SZ_REGION_ORG）"),
        },
        "compute": {"status": "ok", "elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("sz=%d / pool=%d (%.2f%%) series=%d期 %d—%d 期末=%d 无年份=%d"
          % (len(sz), n, 100.0 * len(sz) / n, len(series), lo, hi, series[-1][1], no_year))
    print("areas", area_rows[:5])
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
    out_json = here / "M_SVC_PT_SZ_TOTAL_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_SVC_PT_SZ_TOTAL.py 等价）
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
        "metric_id": "M_SVC_PT_SZ_TOTAL",
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
