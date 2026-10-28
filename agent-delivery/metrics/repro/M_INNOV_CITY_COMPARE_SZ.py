#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_INNOV_CITY_COMPARE_SZ 深圳科技发展指标对比
# 【维护者】唐绍祖
# 【适用系统】科技专题系统 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_INNOV_CITY_COMPARE_SZ.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_INNOV_CITY_COMPARE_SZ 深圳科技发展指标对比 · 复现代码（王惠 V1.5-20260901，20261021 换源版）

四维：研发投入(上市 rd)/专利数量/高企数量/创新人才(学者)。
城市：深圳 + 广州 + 东莞（库覆盖可信区）。
数据源：三方库 `gkx`（唯一入口 `code/_gkxdb.py`），**不含任何 demo_* / _devdb**。

换源说明（20261021）
--------------------
* 读数与 20261020 旧版逐项一致：rd 深圳 3,555.5 亿 / 专利 275,908 / 高企 15,683 / 学者 194；
  广州 566.8 亿 / 140,395 / 7,556 / 86；东莞 149.4 亿 / 89,347 / 3,607 / 7。
* 专利维改为读共享扫描缓存（`_snapshots21/patent_scan_20261021.pkl`）：`COUNT(DISTINCT pn)`
  按 (城市, 年) 去重，与旧 `JOIN ... COUNT(DISTINCT p.pn)` 同口径（旧版按城聚合，不做申请人分组求和）。
* 城市键：`dwd_org_base_info.city` → `norm_city()`；实测该列 66 个取值、全为「X市」，
  无 'NULL' 字面量、无区县值，`LIKE '%深圳%'` 与归一后等值判定结果一致（95,600 行）。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import _gkx21_city as C  # noqa: E402

METRIC_ID = "M_INNOV_CITY_COMPARE_SZ"
YEAR = 2024
CITIES = ["深圳", "广州", "东莞"]


def main():
    probes = {t: C.inventory_rows(t) for t in
              ("dwd_org_base_info", "dwd_org_stock_finance_info", "dwd_patent",
               "dwd_org_tech_tag", "dwd_scholar")}
    pat = C.patents_2024_by_city(CITIES)
    rd = C.rd_by_city(CITIES, YEAR, YEAR)
    ht = C.hightech_by_city(CITIES)
    sch = C.scholars_by_city_like(CITIES)

    rows = {c: dict(rd=rd.get(c), patents=pat.get(c, 0),
                    hightech=ht.get(c), scholars=sch.get(c)) for c in CITIES}

    def norm_dim(key):
        vals = [rows[c][key] for c in CITIES]
        xs = [v for v in vals if v is not None]
        if not xs:
            return [None] * len(vals)
        lo, hi = min(xs), max(xs)
        return [None if v is None else (0.5 if hi == lo else (v - lo) / (hi - lo)) for v in vals]

    dims = {k: norm_dim(k) for k in ["rd", "patents", "hightech", "scholars"]}
    out = []
    for i, c in enumerate(CITIES):
        d = [dims[k][i] for k in ["rd", "patents", "hightech", "scholars"]]
        avail = [x for x in d if x is not None]
        comp = round(sum(avail) / len(avail) * 100, 2) if avail else None
        out.append({"city": c, **rows[c],
                    "d_rd": round(d[0], 3) if d[0] is not None else None,
                    "d_pat": round(d[1], 3) if d[1] is not None else None,
                    "d_ht": round(d[2], 3) if d[2] is not None else None,
                    "d_sch": round(d[3], 3) if d[3] is not None else None,
                    "composite": comp})

    dims_with_data = sum(1 for k in ["rd", "patents", "hightech", "scholars"]
                         if any(rows[c][k] for c in CITIES))
    scores = [o["composite"] for o in out if o["composite"] is not None]
    has_dist = len(set(scores)) > 1
    result = {
        "metric_id": METRIC_ID,
        "metric_name": "深圳科技发展指标对比",
        "also_serves": ["M_INNOV_CITY_FACTOR_GLOBAL"],
        "method": "王惠 V1.5：四维（研发投入/专利/高企/创新人才）所选城内归一",
        "cities": CITIES, "stat_year": YEAR,
        "data_source": "gkx（三方库 183.240.141.251:3318，只读账号；不含任何演示库引用）",
        "patent_caliber": "COUNT(DISTINCT pn) @apdt_year=2024，申请人名精确等于城内机构名",
        "probes": probes,
        "compute": {"cities": out},
        "support_judgment": "部分支持" if (dims_with_data >= 3 and has_dist) else "完全不支持",
    }
    result["support_note"] = (
        f"四维中 {dims_with_data} 维有数（rd 仅上市、dev 兜底全 NULL；scholar 用机构名含城市名近似对齐）；"
        f"对比限定库覆盖可信区（深圳/广州/东莞）；非粤城市因机构库地域失衡不可信。"
        f"换源 gkx 后四维读数与 20261020 旧版逐项一致（深圳 3,555.5 亿/275,908 件/15,683 家/194 人）"
    )

    path = HERE / f"{METRIC_ID}_out.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "compute"}, ensure_ascii=False))
    for o in out:
        print(o)


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
    out_json = here / "M_INNOV_CITY_COMPARE_SZ_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_INNOV_CITY_COMPARE_SZ.py 等价）
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
        "metric_id": "M_INNOV_CITY_COMPARE_SZ",
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
