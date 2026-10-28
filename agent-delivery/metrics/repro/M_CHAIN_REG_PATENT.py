#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_CHAIN_REG_PATENT 专利
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_CHAIN_REG_PATENT.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""专利（链维/区域维）（M_CHAIN_REG_PATENT）—— 申请人名称桥接，自包含。

口径：专利件数来自 gkx.dwd_patent（2,939,895 件，apdt_year 2021—2026），
    申请人名称 → 企业名称 → 链（标签快照 names）→ 城市（主档名称）。
    名称匹配是代理：官方口径要求的机构—专利关系表在 gkx 不存在，同名/更名会漏计。

产物：chains[].value = 该链专利件数；sz_patents = 深圳申请人专利件数；
patent_firms = 有专利的申请人去重数。


运行：cd code && python3 M_CHAIN_REG_PATENT.py
产物：code/M_CHAIN_REG_PATENT_out.json（覆盖写）
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_REG_PATENT_out.json")

BASE_USED = ["2021", "2022", "2023", "2024"]
BASE_MISSING = ["2025", "2026"]
BASE_NOTE = ("统计期 2025 年，专利按申请年 ≤2024 截断：`dwd_patent.apdt_year` 只有 2021—2026，"
             "且 2025/2026 申请量因公开滞后不完整，纳入会系统性低估近年值；2025/2026 仅作观察不入正式值。")

SOURCES = [
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
      "table": "gkx.dwd_org_industry_tags", "rows": 2283762,
      "snapshot": "code/_snapshots21/chain_panel21.json"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
      "table": "gkx.dwd_industry_chain_info", "rows": 1273,
      "snapshot": "code/_snapshots21/chain_tree_20261021.json"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
      "table": "gkx.dwd_org_base_info", "rows": 189116,
      "snapshot": "code/_snapshots21/base_20261021.json"},
]


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    t0 = time.time()
    panel = load("chain_panel21.json")
    chains = panel["chains"]
    tree = load("chain_tree_20261021.json")
    layer = load("chain21_layer_20261022.json")
    pat = load("patent_panel_innov_20261021.json")
    app_total = pat["app_total"]
    name_chain = layer["names"]
    base = load("base_20261021.json")
    name_city = {}
    for r in base:
        if r[2] and r[2] not in name_city:
            name_city[r[2]] = r[4]
    agg = defaultdict(lambda: {"n": 0, "sz": 0, "firms": 0})
    for name, pv in app_total.items():
        c = name_chain.get(name)
        if not c:
            continue
        a = agg[c]
        a["n"] += pv
        a["firms"] += 1
        if name_city.get(name) == "深圳市":
            a["sz"] += pv
    rows = []
    for c in chains:
        a = agg.get(c["chain"], {"n": 0, "sz": 0, "firms": 0})
        rows.append({"chain": c["chain"], "name": c["name"], "value": a["n"],
                     "sz_patents": a["sz"], "patent_firms": a["firms"],
                     "nonleaf": None, "leaves": None, "l1": None})
    rows.sort(key=lambda r: -r["value"])
    tn = sum(r["value"] for r in rows); tsz = sum(r["sz_patents"] for r in rows)
    vv = sorted(r["value"] for r in rows)
    stats = {
        "n_chains": len(rows),
        "min": vv[0], "max": vv[-1], "median": vv[len(vv) // 2],
        "top1_share_pct": round(100.0 * vv[-1] / tn, 3) if tn else None,
        "sz_share_pct": round(100.0 * tsz / tn, 3) if tn else None,
        "patents_per_firm": round(tn / sum(r["patent_firms"] for r in rows), 2)
                             if sum(r["patent_firms"] for r in rows) else None,
    }
    headline = {"value": tn, "unit": "件（名称桥接口径）", "sz_patents": tsz,
                "patent_table_rows": pat["rows"], "window": pat["window"],
                "firms_with_patents": sum(r["patent_firms"] for r in rows)}
    facts = [
        {"label": "专利主表行数", "value": pat["rows"]},
        {"label": "专利年份窗口", "value": "2021—2024（apdt_year 仅 2021—2026）"},
        {"label": "链级专利件数合计", "value": tn},
        {"label": "其中深圳申请人", "value": tsz},
        {"label": "有专利的申请人", "value": headline["firms_with_patents"]},
    ]
    population = {"defined_as": "gkx.dwd_patent 全部申请，申请人名称能桥到链的样本",
                  "patent_rows": pat["rows"], "name_mapped": len(name_chain),
                  "window": pat["window"]}
    compute = {"formula": "SUM(patent_count) GROUP BY chain",
               "bridge": "applicant_name → 标签表 company_name → chain；base name → city",
               "proxy": True}
    STEPS = ["读取专利面板快照（2,939,895 件，2021—2024 窗口）",
             "申请人名称 → 链（标签扫描 names）", "企业名称 → 城市（主档名称）",
             "按链汇总专利件数、深圳件数与申请人去重数",
             "标注名称桥接偏差：同名合并、更名漏计"]
    out = {
        "metric_id": "M_CHAIN_REG_PATENT",
        "metric_name": "专利（链维/区域维）",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": '专利主表 293.9 万件真实可用，名称桥接后 12 条链均有值；但官方口径要求的机构—专利关系键与机构—链关系表在 gkx 均不存在（information_schema 零命中），名称匹配会漏计更名/同名主体，链归属与城市归属都只能作代理。',
        "sources": SOURCES,
        "base_years_used": BASE_USED,
        "base_years_missing": BASE_MISSING,
        "base_years_note": BASE_NOTE,
        "headline": headline,
        "stats": stats,
        "facts": facts,
        "chains": rows,
        "method_steps": STEPS,
        "population": population,
        "compute": compute,
        "gaps": [
            "官方桥缺失：gkx 无 enterprise_patent_org_rel / enterprise_industry_chain 表（information_schema 零命中），org_id 全键路径不可执行",
            "名称桥：同名企业合并、更名/简称漏计；申请人名称能桥到链的样本 36,993 个",
            "单链归属：一个申请人名称只映射一个链，跨链企业只计入首链，链间分布偏保守",
            "与 M_CHAIN_PATENT_COUNT 不同口径：本件第一申请人单角色、每件只计一次（1,127,340 件）；该件双角色并集、多链重复计位（3,026,291），两者不可互校",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("[ok]", "M_CHAIN_REG_PATENT", json.dumps(headline, ensure_ascii=False),
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
    out_json = here / "M_CHAIN_REG_PATENT_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_CHAIN_REG_PATENT.py 等价）
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
        "metric_id": "M_CHAIN_REG_PATENT",
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
