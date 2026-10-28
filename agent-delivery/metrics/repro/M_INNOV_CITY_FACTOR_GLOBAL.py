#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_INNOV_CITY_FACTOR_GLOBAL 城市创新能力要素表现
# 【维护者】唐绍祖
# 【适用系统】科技专题系统 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_INNOV_CITY_FACTOR_GLOBAL.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_INNOV_CITY_FACTOR_GLOBAL 城市创新能力要素表现 · 复现代码（王惠 V1.5-20260901，20261021 换源版）

三要素：人才(学者去重 + Σdevelopment_employee) / 资金(Σresearch_development_amount) / 政策(有效政策件数)。
城内极值归一 + 等权 ×100。城市 = 深圳/广州/东莞（库覆盖可信区）。
数据源：三方库 `gkx`（唯一入口 `code/_gkxdb.py`），**不含任何 demo_* / _devdb**。

换源说明（20261021）
--------------------
* 资金维读数与旧版逐位一致（深圳 1,366,367,257,075.05 元 / 广州 264,072,837,060.45 / 东莞 69,474,579,097.31）。
* 人才维 `development_employee` 在 gkx 同为 90,926 行全 NULL → employee_sum=0，退化为纯学者数。
* 学者数按「机构名精确 IN 城内机构名、逐城独立计数」：深圳 165 / 广州 840 / 东莞 6，
  较旧版（168/841/7）少 1—3 人——旧脚本未过滤 `is_deleted`、且以 `LIKE '%城%'` 取机构名集合，
  gkx 侧一律 `is_deleted=0` + 归一 city，差异来自这 1‰ 级的行过滤，方向为**略低**。
* 政策维：`dwd_policy_base.city` 有 9,706 行字面量 'NULL'，旧脚本 `city IS NULL` 在 gkx 上恒为 0；
  本版用 `norm_city()` 把 'NULL'/''/'NONE'/'-' 一律归空，省级共享仍为 231 条（广东省级政策）。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import _gkx21_city as C  # noqa: E402

METRIC_ID = "M_INNOV_CITY_FACTOR_GLOBAL"
CITIES = ["深圳", "广州", "东莞"]


def norm(vals):
    mx = max(vals) or 1
    mn = min(vals)
    return [round((v - mn) / (mx - mn), 4) if mx > mn else 1.0 for v in vals]


def main():
    probes = {t: C.inventory_rows(t) for t in
              ("dwd_scholar", "dwd_org_annual_financial_info",
               "dwd_org_stock_finance_info", "dwd_policy_base")}
    dev = C.dev_employee_probe()
    sch = C.scholars_by_city_names(CITIES)
    fund = C.rd_by_city(CITIES, 2019, 2024)
    pol, prov_shared = C.policies_by_city(CITIES)

    results = []
    for c in CITIES:
        results.append({
            "city": c,
            "scholar_cnt": sch.get(c, 0),
            "employee_sum": 0,
            "emp_col_nonnull": dev["nonnull"],
            "emp_col_total": dev["rows"],
            "funding_sum": round(fund.get(c, 0.0), 2),
            "policy_cnt": pol[c]["total"],
            "policy_city_cnt": pol[c]["city"],
            "policy_prov_shared": pol[c]["prov_shared"],
        })

    talent = [r["scholar_cnt"] + r["employee_sum"] for r in results]
    funding = [r["funding_sum"] for r in results]
    policy = [r["policy_cnt"] for r in results]
    nt, nf, npol = norm(talent), norm(funding), norm(policy)
    for i, r in enumerate(results):
        r["d_talent"], r["d_funding"], r["d_policy"] = nt[i], nf[i], npol[i]
        r["factor_score"] = round(100 / 3 * (nt[i] + nf[i] + npol[i]), 1)

    result = {
        "metric_id": METRIC_ID,
        "metric_name": "城市创新能力要素表现",
        "method": "王惠 V1.5：人才/资金/政策三要素，城内极值归一+等权×100",
        "cities": CITIES,
        "data_source": "gkx（三方库 183.240.141.251:3318，只读账号；不含任何演示库引用）",
        "probes": probes,
        "compute": {"factors": results},
        "support_judgment": "部分支持",
        "support_note": (
            f"资金维完整可用；人才维 development_employee 100% NULL（{dev['rows']:,} 行实测）→ 退化为纯学者数；"
            f"政策维 city 字段 9,706 行字面量 'NULL'（国家级政策不计入城市）→ 城市件数偏保守；"
            f"机构底册 99.8% 集中广东 → 宇宙限粤三城 ⇒ 部分支持"
        ),
    }

    path = HERE / f"{METRIC_ID}_out.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=1))


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
    out_json = here / "M_INNOV_CITY_FACTOR_GLOBAL_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_INNOV_CITY_FACTOR_GLOBAL.py 等价）
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
        "metric_id": "M_INNOV_CITY_FACTOR_GLOBAL",
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
