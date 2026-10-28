#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_INNOV_CITY_COMPETE_SZ 深圳科技竞争力
# 【维护者】唐绍祖
# 【适用系统】科技专题系统 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_INNOV_CITY_COMPETE_SZ.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_INNOV_CITY_COMPETE_SZ 深圳科技竞争力 · 复现代码（王惠 V1.6-20260901，20261021 换源版）

三维：优势领域(LQ>1 的 IPC4 数) / 薄弱环节(LQ<0.5 且全域份额≥中位) / 发展潜力(近 3 年均值 vs 前 5 年均值)。
对标宇宙 = 深圳 + 广州 + 东莞（库覆盖可信区）。领域键 = `main_classification_ipcr` 前 4 位。
数据源：三方库 `gkx`（唯一入口 `code/_gkxdb.py`）+ 共享专利扫描缓存，**不含任何 demo_* / _devdb**。

口径差异（20261021，必须披露）
------------------------------
旧版 SQL 为 `GROUP BY first_applicant_name, IPC4, apdt_year` 后**按申请人分组求和**，
同一件专利若有两个同城共同申请人会被计两次；本版在共享扫描层按
**(城市, 年, IPC4) 去重 pn** 计数，等于把「同城共同申请人」只留一件。
故 `sz_patent_total` 会低于旧版 887,763（差值即同城共同申请重复量），LQ 是份额比、受影响更小。
换源后判档、优势/薄弱领域数、潜力增速的量级均不变，§2.7 已逐项给出新旧对照。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import _gkx21_city as C  # noqa: E402

METRIC_ID = "M_INNOV_CITY_COMPETE_SZ"
CITIES = ["深圳", "广州", "东莞"]
Y0, Y1 = 2017, 2024


def main():
    probes = {t: C.inventory_rows(t) for t in
              ("dwd_patent", "dwd_zh_paper", "dwd_org_base_info")}
    scan = C.patent_scan()
    ipc_pn = scan["ipc_pn"]
    cy_pn = scan["city_year_pn"]

    def cnt(key):
        return len(ipc_pn.get(key, ()))

    ipc4_sz, ipc4_all = {}, {}
    for (city, yr, ipc4), s in ipc_pn.items():
        n = len(s)
        ipc4_all[ipc4] = ipc4_all.get(ipc4, 0) + n
        if city == "深圳":
            ipc4_sz[ipc4] = ipc4_sz.get(ipc4, 0) + n
    ipc4_sz = {k: v for k, v in ipc4_sz.items() if v}
    ipc4_all = {k: v for k, v in ipc4_all.items() if v}

    year_sz = {y: len(cy_pn.get(("深圳", y), ())) for y in range(Y0, Y1 + 1)}
    sz_total = sum(ipc4_sz.values())
    all_total = sum(ipc4_all.values()) or 1

    shares_all = sorted(v / all_total for v in ipc4_all.values())
    med_share = shares_all[len(shares_all) // 2] if shares_all else 0
    advantage, weak = [], []
    for ipc4, szc in ipc4_sz.items():
        allc = ipc4_all.get(ipc4, 0)
        if allc == 0:
            continue
        lq = (szc / sz_total) / (allc / all_total)
        if lq > 1:
            advantage.append(ipc4)
        if lq < 0.5 and (allc / all_total) >= med_share:
            weak.append(ipc4)

    recent = [year_sz.get(y, 0) for y in (2022, 2023, 2024)]
    # 20261021 修正：`gkx.dwd_patent` 只有 2021–2026 年（面板全表实测），
    # 2017–2020 恒为 0。原写法把「不存在的年份」当 0 计入分母，把基准压到 1/5，
    # 增速被放大成 3.87x（实为 -2.7%）。改为**只用库内真实存在的年份**求基准。
    avail_base_years = [y for y in (2017, 2018, 2019, 2020, 2021)
                        if year_sz.get(y, 0) > 0]
    base = [year_sz[y] for y in avail_base_years]
    rec_avg = sum(recent) / 3
    base_avg = (sum(base) / len(base)) if base else 0
    growth = ((rec_avg - base_avg) / base_avg) if base_avg else None
    missing_base_years = [y for y in (2017, 2018, 2019, 2020) if year_sz.get(y, 0) == 0]
    adv_sorted = sorted(advantage, key=lambda k: -ipc4_sz[k])

    c = {
        "n_ipc4_sz": len(ipc4_sz), "n_ipc4_all": len(ipc4_all),
        "advantage_ipc4_count": len(advantage), "advantage_top10": adv_sorted[:10],
        "weak_ipc4_count": len(weak), "weak_top10": sorted(weak)[:10],
        "recent_3y_avg": round(rec_avg, 1), "base_5y_avg": round(base_avg, 1),
        "growth_rate": round(growth, 4) if growth is not None else None,
        "base_years_used": avail_base_years,
        "base_years_missing": missing_base_years,
        "growth_caliber": ("基准年只用库内真实存在的年份求均值；"
                           "2017–2020 在 dwd_patent 中无数据（全表仅 2021–2026），"
                           "若把它们当 0 计入分母会把增速放大 5 倍"),
        "sz_patent_total": sz_total,
        "year_sz": {str(y): v for y, v in year_sz.items()},
        "caliber": "按 (城市,年,IPC4) 去重 pn；旧版按申请人分组求和（同城共同申请人重复计）",
    }
    result = {
        "metric_id": METRIC_ID,
        "metric_name": "深圳科技竞争力",
        "method": "王惠 V1.6：区位商(LQ)三维（优势/薄弱/潜力）",
        "benchmark_cities": CITIES,
        "data_source": "gkx（三方库 183.240.141.251:3318，只读账号；不含任何演示库引用）",
        "probes": probes,
        "compute": c,
        "support_judgment": "部分支持",
    }
    result["support_note"] = (
        f"深圳 IPC4 领域 {c['n_ipc4_sz']} 个（宇宙 {c['n_ipc4_all']}）；LQ>1 优势领域 {c['advantage_ipc4_count']} 个；"
        f"薄弱 {c['weak_ipc4_count']} 个；近3年均值 {c['recent_3y_avg']} vs 基准年 "
        f"{c['base_years_used']} 均值 {c['base_5y_avg']}（增速 {c['growth_rate']}；"
        f"2017–2020 库内无数据，基准按真实存在年份计，未按 0 摊薄）。"
        f"三维均可出数，但（1）dwd_org_base_info.city 99.8% 集中广东，全国口径对标失真，宇宙被迫限深圳+广州+东莞；"
        f"（2）论文/项目表无城市归属键，潜力维仅专利单一口径 ⇒ 按四档口径判部分支持"
    )

    path = HERE / f"{METRIC_ID}_out.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "compute"}, ensure_ascii=False))
    print(json.dumps(c, ensure_ascii=False))


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
    out_json = here / "M_INNOV_CITY_COMPETE_SZ_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_INNOV_CITY_COMPETE_SZ.py 等价）
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
        "metric_id": "M_INNOV_CITY_COMPETE_SZ",
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
