#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_SVC_PT_KEYORG_SCALE 重点机构规模档案值
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_SVC_PT_KEYORG_SCALE.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""重点机构规模档案值（M_SVC_PT_KEYORG_SCALE）—— gkx 口径，自包含。

钉版契约（calc-logic 0.2.0，2026-08-28 锁版）：逐机构读档案三格
    规模档 org_size / 员工数 employees_number / 营业收入 operating_revenue
不做聚合、不出 fact/series/dist、无值显「—（未披露）」、禁显 0、禁注册资本顶充人数。

换源后的两处调整（均在正文披露）：
  1. 重点机构名单在 gkx 无源（钉版把名单遴选归 Q-SVCCHAIN-01，未交付）。
     本件用「池内 org_size='大型'」作**代理名单**（1,906 家），并另给「年报营收 Top50」
     作交叉视角；代理名单不是正式名单，不得当作遴选结论。
  2. 员工数与营业收入只能从 gkx.dwd_org_annual_financial_info（企业年报）取
     「最近一个有值年」，缺失留 null（不写 0）；覆盖率为实测值，不按池外推。

数据源（只读快照，零 SQL）：
    code/_snapshots21/svc21_facts_20261022.json   base_fields(org_size) + finance(emp/rev)
    code/_snapshots21/svc21_pt_axis_20261022.json base_extra(org_type, currency)

产出：code/M_SVC_PT_KEYORG_SCALE_out.json
运行：cd code && python3 M_SVC_PT_KEYORG_SCALE.py
"""
from __future__ import annotations

import json
import os
import statistics
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
AXIS = os.path.join(SNAP, "svc21_pt_axis_20261022.json")
OUT = os.path.join(HERE, "M_SVC_PT_KEYORG_SCALE_out.json")


def latest(rec, key):
    """最近一个有值年的字段值（不补 0）。返回 (year, value)。"""
    for y in sorted((y for y in rec if y.isdigit()), reverse=True):
        v = rec[y].get(key)
        if v is not None and v != 0:
            return y, v
    return None, None


def dec(value, num, den, note):
    """v8 §一：每个派生值自带分子/分母。value 逐位等于原先的标量表达式。"""
    return {"value": value, "numerator": num, "denominator": den,
            "denominator_note": note}


def main():
    t0 = time.time()
    fact = json.load(open(FACTS, encoding="utf-8"))
    ax = json.load(open(AXIS, encoding="utf-8"))
    pool, bf, fin = fact["pool"], fact["base_fields"], fact["finance"]
    extra = ax["base_extra"]
    n = len(pool)

    # ---------------- 代理名单：org_size = 大型
    key = [o for o in pool if (bf.get(o) or {}).get("size") == "大型"]
    cards = []
    n_emp = n_rev = 0
    emp_years, rev_years = Counter(), Counter()
    for o in key:
        b = bf.get(o) or {}
        ex = extra.get(o) or ["", ""]
        rec = fin.get(o) or {}
        ey, e = latest(rec, "emp")
        ry, r = latest(rec, "rev")
        if e is not None:
            n_emp += 1
            emp_years[ey] += 1
        if r is not None:
            n_rev += 1
            rev_years[ry] += 1
        cards.append({
            "org_id": o, "name": pool[o]["name"], "city": pool[o].get("city", ""),
            "org_size": b.get("size") or None,
            "employees_number": e, "employees_year": ey,
            "operating_revenue": r, "revenue_year": ry,
            "org_type": ex[0] or None, "capital_currency": ex[1] or None,
            "capital": b.get("cap"),
        })

    cards.sort(key=lambda c: (-(c["operating_revenue"] or -1), -(c["employees_number"] or -1)))
    rev_sorted = sorted([c for c in cards if c["operating_revenue"]],
                        key=lambda c: -c["operating_revenue"])
    emp_sorted = sorted([c for c in cards if c["employees_number"]],
                        key=lambda c: -c["employees_number"])
    revs = [c["operating_revenue"] for c in rev_sorted]
    emps = [c["employees_number"] for c in emp_sorted]

    sz_key = sum(1 for c in cards if c["city"] == "深圳市")

    out = {
        "metric_id": "M_SVC_PT_KEYORG_SCALE",
        "metric_name": "重点机构规模档案值",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": (
            "规模档（org_size）在代理名单上 100%% 有值；但员工数只有 %d/%d 家（%.2f%%）、"
            "营业收入只有 %d/%d 家（%.2f%%）在年报里有值，且正式「重点机构名单」在 gkx 无源"
            "（Q-SVCCHAIN-01 未交付）→ 三格中两格量不足、名单本身是代理 → 部分支持"
            % (n_emp, len(key), 100.0 * n_emp / len(key), n_rev, len(key),
               100.0 * n_rev / len(key))),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_base_info(org_size, org_type, registered_capital_value)",
             "rows": fact["population"]["base_all"],
             "snapshot": "code/_snapshots21/svc21_pt_axis_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_annual_financial_info(employees_number, operating_revenue)",
             "rows": fact["finance_meta"]["rows_total"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("档案截面：每格取「最近一个有值年」，不同机构的年份不同，"
                            "不做跨年比较、不把缺失年补 0；年报字段的年份分布见 "
                            "employees_year_dist / revenue_year_dist。"),
        "population": {
            "pool_orgs": n,
            "key_list_proxy": len(key),
            "key_list_proxy_defined_as": "池内底册 org_size='大型'",
            "key_list_official": None,
            "key_list_official_note": "正式名单归 Q-SVCCHAIN-01（技术力 Top），gkx 侧无该名单表",
            "shenzhen_in_proxy": sz_key,
        },
        "field_coverage": {
            "org_size": {"orgs_with_value": len(key), "rate": 1.0,
                         "dist": [[k, c] for k, c in
                                  Counter(c["org_size"] for c in cards).most_common()]},
            "employees_number": {"orgs_with_value": n_emp,
                                 "rate": round(n_emp / len(key), 6),
                                 "year_dist": [[y, c] for y, c in emp_years.most_common(6)]},
            "operating_revenue": {"orgs_with_value": n_rev,
                                  "rate": round(n_rev / len(key), 6),
                                  "year_dist": [[y, c] for y, c in rev_years.most_common(6)]},
        },
        "revenue_stats": {
            "n": len(revs),
            "median": round(statistics.median(revs), 2) if revs else None,
            "max": revs[0] if revs else None,
            "sum": round(sum(revs), 2) if revs else None,
            "unit_note": "gkx.dwd_org_annual_financial_info.operating_revenue 原值单位未在表内声明，按原值直报，不做亿元换算",
        },
        "employee_stats": {
            "n": len(emps),
            "median": statistics.median(emps) if emps else None,
            "max": emps[0] if emps else None,
        },
        "top_by_revenue": rev_sorted[:20],
        "top_by_employees": emp_sorted[:20],
        "derived": {
            "no_employee": dec(
                len(key) - n_emp, len(key) - n_emp, None,
                "计数，无分母：代理名单 1,906 家（池内底册 org_size='大型'）中，年报所有年份员工数"
                "均为空/0 的机构数（1,906 − 有值的 %d 家）；不按 0 填充、不以注册资本顶充" % n_emp),
            "no_revenue": dec(
                len(key) - n_rev, len(key) - n_rev, None,
                "计数，无分母：代理名单 1,906 家中，年报所有年份营业收入均为空/0 的机构数"
                "（1,906 − 有值的 %d 家）；缺失留 null，前端显「—（未披露）」" % n_rev),
        },
        "presentation_contract": {
            "missing_shown_as": "—（未披露）",
            "forbid_zero": True,
            "forbid_capital_as_employees": True,
            "note": "无值一律留 null，前端渲染为「—」；本件不写 0 占位，也不用注册资本顶充人数。",
        },
        "sample_cards": cards[:20],
        "difference_vs_old_draft": {
            "population": "旧稿卡面 43,296 行（演示库 svc_org_card）→ 本件代理名单 1,906 家（gkx org_size=大型）",
            "org_size": "旧稿非空 27,589（63.7%）→ 本件 1,906/1,906（100%，仅代理名单内）",
            "employees": "旧稿卡面真实值∩池=0、年报替代源 408 家（0.94%%）→ 本件 %d 家（%.2f%%）"
                         % (n_emp, 100.0 * n_emp / len(key)),
            "revenue": "旧稿卡面真实值∩池=0、年报替代源 300 家（0.69%%）→ 本件 %d 家（%.2f%%）"
                       % (n_rev, 100.0 * n_rev / len(key)),
            "note": "旧稿卡面的营收/人数为演示造数列，本件不再引用；gkx 年报列是真实字段但覆盖稀疏。",
        },
        "compute": {"status": "ok", "elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("proxy=%d emp=%d (%.2f%%) rev=%d (%.2f%%) sz=%d"
          % (len(key), n_emp, 100.0 * n_emp / len(key), n_rev,
             100.0 * n_rev / len(key), sz_key))
    print("top rev", [(c["name"], c["operating_revenue"]) for c in rev_sorted[:3]])
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
    out_json = here / "M_SVC_PT_KEYORG_SCALE_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_SVC_PT_KEYORG_SCALE.py 等价）
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
        "metric_id": "M_SVC_PT_KEYORG_SCALE",
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
