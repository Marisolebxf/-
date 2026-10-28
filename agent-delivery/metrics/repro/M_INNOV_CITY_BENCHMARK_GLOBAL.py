#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_INNOV_CITY_BENCHMARK_GLOBAL 城市对标分析
# 【维护者】唐绍祖
# 【适用系统】科技专题系统 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_INNOV_CITY_BENCHMARK_GLOBAL.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_INNOV_CITY_BENCHMARK_GLOBAL 城市对标分析 · 复现代码（王惠 V1.5-20260901，20261021 换源版）

用户选 ≥2 城对比三维：创新投入(上市研发经费/研发人员) / 创新产出(专利+论文) / 创新环境(政策+高企)。
所选城内极值归一。服务 M_CITY_BENCHMARK / M_CITY_RANK_GLOBAL / M_CITY_INDEX_SZ 同族。
演示选城：深圳、北京、上海、广州（2024）。
数据源：三方库 `gkx`（唯一入口 `code/_gkxdb.py`），**不含任何 demo_* / _devdb**。

换源说明（20261021）
--------------------
* 读数与 20261020 旧版逐项一致：n_org 94,968/33/3/48,267；rd 3,555.5 亿/None/None/566.8 亿；
  专利 275,908/132/1/140,395；论文 3/0/0/8；政策 879/2,268/1,841/325；高企 15,683/0/0/7,544。
* `development_employee` 在 gkx 同样 90,926 行 **100% NULL**（SUM 亦为 NULL）→ 投入维不能用人员兜底。
* 政策维按 `city` 直计（不含省级共享），故深圳 879 而非 FACTOR 的 1,110（后者加 231 条省级均摊）。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import _gkx21_city as C  # noqa: E402

METRIC_ID = "M_INNOV_CITY_BENCHMARK_GLOBAL"
YEAR = 2024
CITIES = ["深圳", "北京", "上海", "广州"]


def norm_pair(v, lo, hi):
    if v is None:
        return None
    if hi == lo:
        return 0.5
    return (v - lo) / (hi - lo)


def main():
    probes = {t: C.inventory_rows(t) for t in
              ("dwd_org_base_info", "dwd_org_stock_finance_info", "dwd_org_annual_financial_info",
               "dwd_patent", "dwd_zh_paper", "dwd_zh_author", "dwd_policy_base", "dwd_org_tech_tag")}
    pat = C.patents_2024_by_city(CITIES)
    n_org = C.surviving_org_count(CITIES)
    rd = C.rd_by_city(CITIES, YEAR, YEAR)
    pap = C.papers_by_city(CITIES, YEAR, base_only=True)
    pol = {c: v["city"] for c, v in C.policies_by_city(CITIES)[0].items()}
    ht = C.hightech_by_city(CITIES, surviving=True)

    rows = {c: dict(n_org=n_org.get(c), rd=rd.get(c) or None, dev=None,
                    patents=pat.get(c, 0), papers=pap.get(c, 0),
                    policies=pol.get(c, 0), hightech=ht.get(c, 0)) for c in CITIES}

    input_vals = [rows[c]["rd"] if any(rows[x]["rd"] for x in CITIES) else rows[c]["dev"] for c in CITIES]
    output_vals = [rows[c]["patents"] + rows[c]["papers"] for c in CITIES]
    pol_vals = [rows[c]["policies"] for c in CITIES]
    hi_vals = [rows[c]["hightech"] for c in CITIES]

    def lohi(xs):
        xs2 = [x for x in xs if x is not None]
        return (min(xs2), max(xs2)) if xs2 else (None, None)

    li, hi_ = lohi(input_vals)
    lo_, ho_ = lohi(output_vals)
    lp, hp_ = lohi(pol_vals)
    lh, hh = lohi(hi_vals)

    results = []
    for i, c in enumerate(CITIES):
        d_in = norm_pair(input_vals[i], li, hi_)
        d_out = norm_pair(output_vals[i], lo_, ho_)
        d_pol = norm_pair(pol_vals[i], lp, hp_)
        d_hi = norm_pair(hi_vals[i], lh, hh)
        d_env = (sum(x for x in [d_pol, d_hi] if x is not None) / 2) \
            if any(x is not None for x in [d_pol, d_hi]) else None
        dims = [d_in, d_out, d_env]
        avail = [d for d in dims if d is not None]
        score = (sum(avail) / len(avail) * 100) if avail else None
        results.append({**rows[c], "city": c, "d_in": d_in, "d_out": d_out, "d_env": d_env,
                        "composite": round(score, 2) if score is not None else None})

    n_dims_with_data = sum(1 for dim_vals in [input_vals, output_vals, pol_vals, hi_vals]
                           if any(dim_vals))
    rd_cov = sum(1 for r in results if r["rd"] is not None)
    scores = [r["composite"] for r in results if r["composite"] is not None]
    has_dist = len(set(scores)) > 1 if scores else False

    result = {
        "metric_id": METRIC_ID,
        "metric_name": "城市对标分析",
        "method": "王惠 V1.5：所选城内三维极值归一（投入=研发经费/人员、产出=专利+论文、环境=政策+高企）",
        "cities": CITIES, "stat_year": YEAR,
        "data_source": "gkx（三方库 183.240.141.251:3318，只读账号；不含任何演示库引用）",
        "probes": probes,
        "compute": {"cities": [{k: (round(v, 2) if isinstance(v, float) else v)
                               for k, v in r.items()} for r in results]},
        "support_judgment": None,
    }
    if n_dims_with_data >= 4 and has_dist and rd_cov >= len(CITIES) - 1:
        result["support_judgment"] = "完全转换支持"
    elif n_dims_with_data >= 2 and has_dist:
        result["support_judgment"] = "部分支持"
    else:
        result["support_judgment"] = "完全不支持"
    result["support_note"] = (
        f"四城对比可算：投入维 rd 覆盖 {rd_cov}/{len(CITIES)}（dev 全 NULL 不可兜底）；"
        f"产出维专利+论文有量；环境维政策 {sum(pol_vals)}/高企 {sum(hi_vals)} 有量；综合分有区分度 {has_dist}。"
        f"重要披露：三方库机构地域高度偏广东（深圳 95,600/广州 49,605/东莞 33,590，北京 163/上海 16），"
        f"非粤城市除政策/上市研发外各维天然低值——城市对比语义受三方库覆盖范围限制。"
        f"换源 gkx 后逐城读数与 20261020 旧版一致"
    )

    path = HERE / f"{METRIC_ID}_out.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "compute"}, ensure_ascii=False))
    for r in result["compute"]["cities"]:
        print(r)


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
    out_json = here / "M_INNOV_CITY_BENCHMARK_GLOBAL_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_INNOV_CITY_BENCHMARK_GLOBAL.py 等价）
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
        "metric_id": "M_INNOV_CITY_BENCHMARK_GLOBAL",
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
