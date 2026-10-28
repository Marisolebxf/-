#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_CHAIN_REG_SERVICE_ORG 服务机构
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_CHAIN_REG_SERVICE_ORG.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""区域服务机构（M_CHAIN_REG_SERVICE_ORG）—— 国标行业重建，自包含。

口径：服务机构 = gkx 主档中属于商务服务/科技服务/信息服务等行业的法人（按国标行业门类），
    按链标签挂链、按城市切片。原「服务机构池」表在 gkx 不存在（只有演示产物），
    本件改由主档行业重建，准入规则与原池不等价。

产物：chains[].value = 该链三市服务机构合计；city_counts 给深圳/广州/东莞/惠州分市数。


运行：cd code && python3 M_CHAIN_REG_SERVICE_ORG.py
产物：code/M_CHAIN_REG_SERVICE_ORG_out.json（覆盖写）
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_REG_SERVICE_ORG_out.json")

BASE_USED = []
BASE_MISSING = []
BASE_NOTE = '截面指标：统计当前存量，不设年度分母。'

SOURCES = [
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
      "table": "gkx.dwd_org_industry_tags", "rows": 2283762,
      "snapshot": "code/_snapshots21/chain_panel21.json",
      "pulled_at": "2026-10-22T15:32:34+08:00"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
      "table": "gkx.dwd_industry_chain_info", "rows": 1273,
      "snapshot": "code/_snapshots21/chain_tree_20261021.json"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
      "table": "gkx.dwd_org_base_info（国标行业门类）", "rows": 189116,
      "snapshot": "code/_snapshots21/base_20261021.json"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
      "table": "gkx.dwd_org_base_info × gkx.dwd_org_industry_tags（链×市聚合）", "rows": 1552,
      "snapshot": "code/_snapshots21/svc_chain_city_20261022.json",
      "pulled_at": "2026-10-22T15:26:04+08:00",
      "note": "42 个非空链×市单元；按主档国标行业服务业门类 + 链标签重建，非原 svc_org_circle 池"},
]


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    t0 = time.time()
    panel = load("chain_panel21.json")
    chains = panel["chains"]
    tree = load("chain_tree_20261021.json")
    svc = load("svc_chain_city_20261022.json")
    cell = defaultdict(dict)
    for c, city, n in svc:
        cell[c][city] = n
    rows = []
    for c in chains:
        d = cell.get(c["chain"], {})
        rows.append({"chain": c["chain"], "name": c["name"],
                     "value": sum(d.values()), "city_counts": d,
                     "nonleaf": None, "leaves": None, "l1": None})
    rows.sort(key=lambda r: -r["value"])
    total = sum(r["value"] for r in rows)
    sz = sum(r["city_counts"].get("深圳市", 0) for r in rows)
    CITY_ORDER = ["深圳市", "广州市", "东莞市", "惠州市"]
    city_totals = {c: sum(r["city_counts"].get(c, 0) for r in rows) for c in CITY_ORDER}
    empty_cells = [f"{c['chain']}|{city}" for c in chains for city in CITY_ORDER
                   if city not in cell.get(c["chain"], {})]
    cities = sorted({k for r in rows for k in r["city_counts"]})
    headline = {"value": total, "unit": "家（四市服务机构挂接次数，跨链可重复计）",
                "sz": sz, "cells": len(svc), "cities": CITY_ORDER,
                "city_totals": city_totals,
                "definition": "主档国标行业属服务业的法人，按链标签挂链"}
    facts = [
        {"label": "链×市非空单元", "value": f"{len(svc)}/48"},
        {"label": "服务机构挂接合计", "value": total},
        {"label": "其中深圳", "value": sz},
        {"label": "四市分布", "value": "、".join(f"{k[:-1]} {v}" for k, v in city_totals.items())},
        {"label": "服务机构最多的链", "value": f'{rows[0]["name"]} {rows[0]["value"]}'},
    ]
    population = {"defined_as": "gkx 主档国标行业服务业门类 + 链标签",
                  "cells": len(svc), "cities": cities}
    compute = {"formula": "COUNT(DISTINCT credit_code) GROUP BY chain, city",
               "source_snapshot": "code/_snapshots21/svc_chain_city_20261022.json",
               "rebuild": True}
    STEPS = ["读取已落盘的服务机构×链×市快照（42 个非空单元）",
             "按链汇总三市合计与深圳分市数", "标出空单元（48 格中 6 格为空）",
             "声明重建准入：主档国标行业，不等价于原服务机构池"]
    out = {
        "metric_id": "M_CHAIN_REG_SERVICE_ORG",
        "metric_name": "区域服务机构",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": '服务机构可用主档国标行业重建，42/48 个链×市单元有值；但原服务机构池在 gkx 不存在，重建准入规则与原池不等价，须甲方确认后才能定版。',
        "sources": SOURCES,
        "base_years_used": BASE_USED,
        "base_years_missing": BASE_MISSING,
        "base_years_note": BASE_NOTE,
        "headline": headline,
        "facts": facts,
        "empty_cells": empty_cells,
        "chains": rows,
        "method_steps": STEPS,
        "population": population,
        "compute": compute,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("[ok]", "M_CHAIN_REG_SERVICE_ORG", json.dumps(headline, ensure_ascii=False),
          "chains", len(rows), "sec", round(time.time() - t0, 2))


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
    out_json = here / "M_CHAIN_REG_SERVICE_ORG_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_CHAIN_REG_SERVICE_ORG.py 等价）
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
        "metric_id": "M_CHAIN_REG_SERVICE_ORG",
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
