#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_CHAIN_LAYOUT_PRIORITY_SCORE 布局优先级评分
# 【维护者】唐绍祖
# 【适用系统】科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_CHAIN_LAYOUT_PRIORITY_SCORE.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_CHAIN_LAYOUT_PRIORITY_SCORE 布局优先级评分 — 王惠四指标 gkx 实测（20261021 改源版）

口径（王惠 calc-logic v0.2.0）：
  产业增长维 =（行业增长率 + 市场占有率）/2；产业竞争力维 =（技术创新能力 + 产业规模）/2；
  总分为两维加权（默认各 0.5），各指标先极值归一化到 0–100。

数据源（20261021 改源）：全部直连三方库 gkx，不再经旧版开发库连接
  D1 行业增长率：`gkx.dwd_org_annual_financial_info`（年报营收，2023/2024 同链合计）
  D2 市场占有率：定义为「深圳该产业产值 ÷ 全国该产业产值」——实测分母不可得；
     另算「深圳/本链合计」替代值，仅用于展示偏差，不并入主分；
  D3 技术创新能力：`gkx.dwd_org_stock_finance_info`（2024 年报期 occur_period='202412'）研发 ÷ 营收；
  D4 产业规模：链上企业年报营收合计；
  E 空间可行性维：gkx 无土地/园区/载体面积表（information_schema 现查），该维为零。

输出：M_CHAIN_LAYOUT_PRIORITY_SCORE_out.json
"""
from __future__ import annotations

import sys
import time
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _gkx21_common import (ROOTS, chain_names, ent_chain_map, load_cache, minmax,  # noqa: E402
                          num, org_index, q, q1, save_cache, stats, write_out)

METRIC = "M_CHAIN_LAYOUT_PRIORITY_SCORE"
NAME = "布局优先级评分"
CODES = {c: n for c, n in chain_names().items() if c in ROOTS}


def fin_rows():
    """链×年 年报聚合 + 深圳切片 + 上市研发，全部由 gkx 现算并缓存。

    结构对齐旧版 chain_lm_fin 快照：{fin:[{code,year,n_ent,n_emp,emp_sum,n_rev,rev_sum,
    n_prof,prof_sum}], sz:[{code,sz_rev,all_rev,sz_n}], rd:[{code,n,n_org,n_rd,rd_sum,rev_sum}]}
    """
    d = load_cache("chain_lm_fin_20261021.json")
    if d is not None:
        return d

    oi = org_index()            # org_id -> [org_id, credit, name, prov, city]
    ec = ent_chain_map()        # credit -> [chains]

    annual = q("SELECT org_id, year, operating_revenue, employees_number, pure_profit "
               "FROM gkx.dwd_org_annual_financial_info WHERE is_deleted=0")
    agg = defaultdict(lambda: {"n_ent": 0, "n_emp": 0, "emp_sum": 0.0, "n_rev": 0,
                               "rev_sum": 0.0, "n_prof": 0, "prof_sum": 0.0})
    sz = defaultdict(lambda: {"sz_rev": 0.0, "all_rev": 0.0, "sz_n": 0})
    for org_id, year, rev, emp, prof in annual:
        meta = oi.get(org_id)
        credit = meta[1] if meta else None
        city = meta[4] if meta else None
        y = int(year) if year is not None else None
        rv = num(rev)
        for ch in ec.get(credit or "", []):
            k = (ch, y)
            a = agg[k]
            a["n_ent"] += 1
            if num(emp) > 0:
                a["n_emp"] += 1
            a["emp_sum"] += num(emp)
            if rv > 0:
                a["n_rev"] += 1
            a["rev_sum"] += rv
            if num(prof) > 0:
                a["n_prof"] += 1
            a["prof_sum"] += num(prof)
            if y == 2024:
                sz[ch]["all_rev"] += rv
                if city == "深圳市":
                    sz[ch]["sz_rev"] += rv
                    if rv > 0:
                        sz[ch]["sz_n"] += 1

    fin = []
    for (ch, y), a in sorted(agg.items(), key=lambda x: (x[0][0], x[0][1] or 0)):
        fin.append({"code": ch, "year": y, **{k: round(v, 4) if isinstance(v, float) else v
                                              for k, v in a.items()}})

    stock = q("SELECT org_id, external_id, research_development_amount, operating_revenue "
              "FROM gkx.dwd_org_stock_finance_info WHERE is_deleted=0 AND occur_period='202412'")
    rd = defaultdict(lambda: {"n": 0, "orgs": set(), "n_rd": 0, "rd_sum": 0.0, "rev_sum": 0.0})
    for org_id, ext, rd_amt, rev in stock:
        credit = ext or (oi.get(org_id) or [None, None])[1]
        for ch in ec.get(credit or "", []):
            r = rd[ch]
            r["n"] += 1
            r["orgs"].add(ext or org_id)
            if num(rd_amt) > 0:
                r["n_rd"] += 1
            r["rd_sum"] += num(rd_amt)
            r["rev_sum"] += num(rev)
    rd_rows = [{"code": ch, "n": r["n"], "n_org": len(r["orgs"]), "n_rd": r["n_rd"],
                "rd_sum": round(r["rd_sum"], 4), "rev_sum": round(r["rev_sum"], 4)}
               for ch, r in sorted(rd.items())]

    d = {"source": "gkx.dwd_org_annual_financial_info + gkx.dwd_org_stock_finance_info 现算 20261021",
         "fin": fin, "sz": [{"code": c, **v} for c, v in sorted(sz.items())], "rd": rd_rows}
    save_cache("chain_lm_fin_20261021.json", d)
    return d


def main():
    t0 = time.time()
    rep = {
        "metric_id": METRIC,
        "metric_name": NAME,
        "date": "2026-10-21",
        "calc_logic_ref": "gkx-orchestration/agent-delivery/metrics/calc-logic/CHAIN/M_CHAIN_LAYOUT_PRIORITY_SCORE.md",
        "data_source": {
            "engine": "三方库 gkx（183.240.141.251:3318），唯一连库入口 code/_gkxdb.py",
            "tables": ["gkx.dwd_org_base_info", "gkx.dwd_org_annual_financial_info",
                       "gkx.dwd_org_stock_finance_info", "gkx.dwd_org_industry_tags"],
            "note": "旧版经开发库专用连接取数；本版全部改直连 gkx，四指标公式与缺维处理未改",
        },
        "weights": {"W1_growth": 0.5, "W2_competitiveness": 0.5,
                    "note": "calc-logic 原文：维度权重可采用等权重，也可自行制定；需求未给权重。"},
    }

    base = q1("SELECT COUNT(*) n, SUM(city LIKE '%%深圳%%') sz FROM gkx.dwd_org_base_info WHERE is_deleted=0")
    prov = q("SELECT province, COUNT(*) n FROM gkx.dwd_org_base_info WHERE is_deleted=0 "
             "GROUP BY province ORDER BY n DESC LIMIT 3")
    stock = q1("SELECT COUNT(*) n, COUNT(DISTINCT external_id) orgs, "
               "SUM(research_development_amount>0) rd_pos "
               "FROM gkx.dwd_org_stock_finance_info WHERE occur_period='202412'")
    tables = [r[0] for r in q(
        "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
        "AND (table_name LIKE '%%land%%' OR table_name LIKE '%%park%%' OR table_name LIKE '%%carrier%%')")]
    rep["probes"] = {
        "dwd_org_base_info_rows": int(base[0]),
        "sz_rows": int(num(base[1])),
        "top_provinces": [{"province": p, "n": int(n)} for p, n in prov],
        "stock_finance_202412": {"rows": int(stock[0]), "orgs": int(stock[1]),
                                 "rd_pos": int(num(stock[2]))},
        "land_park_carrier_tables_in_gkx": tables,
        "national_stat_table": None,
    }

    d = fin_rows()
    by_chain = {}
    for r in d["fin"]:
        by_chain.setdefault(r["code"], {})[int(r["year"])] = r
    sz = {r["code"]: r for r in d["sz"]}
    rd = {r["code"]: r for r in d["rd"]}

    raw = {c2: {"D1": None, "D2": None, "D3": None, "D4": None} for c2 in CODES}
    aux = {}
    for c2 in CODES:
        fy = by_chain.get(c2, {})
        cur, prv = fy.get(2024), fy.get(2023)
        if cur and prv and num(cur.get("rev_sum")) > 0 and num(prv.get("rev_sum")) > 0:
            raw[c2]["D1"] = num(cur["rev_sum"]) / num(prv["rev_sum"]) - 1
        if cur and num(cur.get("rev_sum")) > 0:
            raw[c2]["D4"] = num(cur["rev_sum"])
        r = rd.get(c2)
        if r and num(r.get("rev_sum")) > 0 and num(r.get("rd_sum")) > 0:
            raw[c2]["D3"] = num(r["rd_sum"]) / num(r["rev_sum"])
        s = sz.get(c2) or {}
        aux[c2] = {
            "sz_rev": num(s.get("sz_rev")),
            "all_rev_2024": num(s.get("all_rev")),
            "sz_enterprises_with_rev": int(num(s.get("sz_n"))),
            "sz_share_of_chain": (num(s.get("sz_rev")) / num(s.get("all_rev"))
                                  if num(s.get("all_rev")) > 0 else None),
            "rd_orgs_2024": int(num((rd.get(c2) or {}).get("n_org"))),
            "n_rev_enterprises_2024": int(num((cur or {}).get("n_rev"))),
        }

    # 主分：D2 结构性不可得，按「缺失维不计权」处理（并在正文声明与王惠原式不同）
    z = {k: minmax_dict({c2: raw[c2][k] for c2 in CODES}) for k in ("D1", "D3", "D4")}
    rows = []
    for c2 in CODES:
        growth = [(z["D1"][c2] * 100) if c2 in z["D1"] else None]
        comp = [z["D3"][c2] * 100, z["D4"][c2] * 100] if c2 in z["D3"] and c2 in z["D4"] else None
        dims = []
        if growth[0] is not None:
            dims.append(growth[0])
        if comp:
            dims.append(sum(comp) / 2)
        score_3d = round(sum(dims) / len(dims), 2) if dims else None
        rows.append({
            "industry_code": c2, "industry_name": CODES[c2],
            "D1_growth": None if raw[c2]["D1"] is None else round(raw[c2]["D1"], 4),
            "D2_market_share": None,
            "D3_rd_intensity": None if raw[c2]["D3"] is None else round(raw[c2]["D3"], 4),
            "D4_scale_yuan": None if raw[c2]["D4"] is None else round(raw[c2]["D4"], 0),
            "score_3d_without_D2": score_3d,
            "n_dims_measured": len(dims),
            **aux[c2],
        })

    scored = [r["score_3d_without_D2"] for r in rows if r["score_3d_without_D2"] is not None]
    rep["compute"] = {
        "rows": rows,
        "dim_coverage": {
            "D1_growth_measured": sum(1 for c2 in CODES if raw[c2]["D1"] is not None),
            "D2_market_share_measured": 0,
            "D3_rd_measured": sum(1 for c2 in CODES if raw[c2]["D3"] is not None),
            "D4_scale_measured": sum(1 for c2 in CODES if raw[c2]["D4"] is not None),
            "chains_all_present_dims": sum(1 for r in rows if r["n_dims_measured"] == 2),
        },
        "score_stats": {
            "min": min(scored), "max": max(scored),
            "n_scored": len(scored), "distinct": len(set(scored)),
        },
        "d2_verdict": {
            "definition": "深圳该产业产值 ÷ 全国该产业产值",
            "numerator": "深圳链上企业 2024 年报营收：0–4 家/链，5 条链为 0",
            "denominator": "全国该产业产值：库内无承载；gkx.dwd_org_base_info 99.82% 在广东，省外仅 339 家，不能当全国",
            "conclusion": "分母不存在 → D2 无法计算，主分只能按 3 个指标重算，已非王惠原式。",
        },
        "spatial_dimension": {
            "land_park_carrier_tables": rep["probes"]["land_park_carrier_tables_in_gkx"],
            "cross_ref": "M_INNOV_KEYD_LAND（判完全不支持：用地面积列在全资产中不存在）",
            "conclusion": "布局=招商/选址类决策，但空间可行性维在 gkx 亦为零，优先级评分只是产业侧排序。",
        },
    }

    rep["support_judgment"] = {
        "data_support_level": "部分支持",
        "reason": (
            "四指标中 D1/D3/D4 可实测（D3 覆盖 972 家上市公司，2024 年报期 750 条），"
            "但 D2 市场占有率的分母『全国该产业产值』在开发库与三方库均无承载，"
            "且企业底册 99.82% 在广东，无法构造全国分母；空间可行性维（土地/园区/载体面积）同样为零。"
            "四维中一维结构性不可得 + 一维为零 → 按 §〇 判部分支持。"
        ),
        "criteria": {
            "D1_measured": rep["compute"]["dim_coverage"]["D1_growth_measured"],
            "D2_measured": 0,
            "D3_measured": rep["compute"]["dim_coverage"]["D3_rd_measured"],
            "D4_measured": rep["compute"]["dim_coverage"]["D4_scale_measured"],
            "n_scored": rep["compute"]["score_stats"]["n_scored"],
        },
    }
    rep["elapsed_sec"] = round(time.time() - t0, 1)
    write_out(METRIC, rep)
    print(rep["compute"]["dim_coverage"])
    print([(r["industry_name"], r["score_3d_without_D2"], r["D3_rd_intensity"]) for r in rows])


def minmax_dict(vals: dict) -> dict:
    """None 不参与极值；全部相同 → 0.5。"""
    present = {k: v for k, v in vals.items() if v is not None}
    if not present:
        return {}
    lo, hi = min(present.values()), max(present.values())
    if hi - lo <= 1e-12:
        return {k: 0.5 for k in present}
    return {k: (v - lo) / (hi - lo) for k, v in present.items()}


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
    out_json = here / "M_CHAIN_LAYOUT_PRIORITY_SCORE_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_CHAIN_LAYOUT_PRIORITY_SCORE.py 等价）
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
        "metric_id": "M_CHAIN_LAYOUT_PRIORITY_SCORE",
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
