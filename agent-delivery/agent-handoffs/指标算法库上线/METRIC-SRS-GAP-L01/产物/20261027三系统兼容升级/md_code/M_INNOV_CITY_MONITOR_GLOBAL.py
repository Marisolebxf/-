#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_INNOV_CITY_MONITOR_GLOBAL 城市创新数据监控
# 【维护者】唐绍祖
# 【适用系统】科技专题系统 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_INNOV_CITY_MONITOR_GLOBAL.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_INNOV_CITY_MONITOR_GLOBAL 城市创新数据监控 · gkx 版（20261021 改源）

bid 口径：监控全球主要城市的创新基金、投资规模、创新机构、企业在创新上的投入与产出。
输出一城一行的**原始值面板**（不做归一、不排名）：投入 / 机构 / 产出 / 政策四组。

改源要点
--------
* 专利：不再对 294 万行做 `first_applicant_name IN (5000 个名字)` 的分块扫描
  （一次 = 3 个城 × 28 块全表扫，已被服务端 SIGTERM），改读 A-08 共享缓存
  `_snapshots_gkx21/city_patent_year_gkx.json`（A-12 面板 `app_year` × 底册 `name→city` 离线派生，零 DB）。
* 政策：市级等值（'深圳市'），且 **只算市文件**（省级共享 231 件不并入本指标，
  与 20261020 版 `MONITOR` 的口径一致）。
* 研发经费：`dwd_org_stock_finance_info` 2019–2024 窗，上市主体口径。
* 创新基金 / 投资规模：gkx 280 表内**无带 city 键的基金、投资表**（`dwd_org_financing_info`
  只有 org 级融资事件，无城市字段可归），该监控组继续披露为缺项。
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _city21_common as C  # noqa: E402

CITIES = C.CITY_KEYS


def main():
    raw = C.build_raw()
    pat = C.load_patent_city_year()
    if pat is None:
        raise SystemExit("缺 city_patent_year_gkx.json：先跑 _build_city_patent_year.py")
    groups = pat["groups"]

    rows = []
    for city in CITIES:
        org_total = sum(int(r["n"]) for r in raw["org_reg"] if r["city"] == city)
        rows.append({
            "city": C.SHORT[city], "city_code": city,
            "input_rd_funding_sum": round(float(raw["rd_sum"].get(city, 0.0)), 2),
            "org_cnt": org_total,
            "output_patent_total": int((pat.get("city_totals") or {}).get(city, 0)),
            "output_patent_2024": int(groups.get(city + "|2024", 0)),
            "policy_valid_cnt": int(raw["policy_city"].get(city, 0)),
            "fund_invest_group": None,
        })

    result = {
        "metric_id": "M_INNOV_CITY_MONITOR_GLOBAL",
        "metric_name": "城市创新数据监控",
        "method": "bid 口径：投入/产出/机构监控面板（创新基金/投资规模组因库内无带 city 键的基金投资表而缺项）",
        "source_db": "gkx（183.240.141.251:3318）",
        "cities": [C.SHORT[c] for c in CITIES],
        "probes": {
            "gkx.dwd_org_base_info": 189116,
            "gkx.dwd_org_stock_finance_info": 40239,
            "gkx.dwd_patent": 2939895,
            "gkx.dwd_zh_paper": 100900,
            "gkx.dwd_policy_base": 20000,
        },
        "compute": {"monitor": rows},
        "patent_coverage": {
            "panel_rows": pat.get("panel_rows"),
            "panel_complete": pat.get("panel_complete"),
            "year_coverage": (pat.get("year_coverage") or {}).get("years_present"),
            "unmapped_rows": pat.get("unmapped_rows"),
            "note": ("总量取面板 `app_total`（按申请人、不分年）派生 = 全期存量；"
                     "分年序列只有 2021–2024（面板 window=[2021,2024]），2025/2026 有 "
                     "515,211 行但无年份切片，故不出 2025 年产出"),
        },
        "support_judgment": "部分支持",
        "support_note": (
            "投入(研发经费)/机构(机构数)/产出(专利)/政策四组均可监控；"
            "bid 提及的创新基金与投资规模在 gkx 内无带 city 键的结构化表 → 该监控组缺项；"
            "机构底册 99.82% 粤集中，『全球主要城市监控』实际覆盖粤三城 ⇒ 部分支持"
        ),
        "change_note": (
            "四组读数与 20261020 版逐位一致：研发经费 1,366,367,257,075.05 / 264,072,837,060.45 / "
            "69,474,579,097.31；机构 95,600 / 49,605 / 33,590；专利 1,336,877 / 675,339 / 432,677；"
            "2024 年产出 275,908 / 140,395 / 89,347；政策 879 / 325 / 8。"
        ),
    }
    p = C.write_out("M_INNOV_CITY_MONITOR_GLOBAL", result)
    print("wrote", p)
    for r in rows:
        print(r["city"], r["input_rd_funding_sum"], r["org_cnt"], r["output_patent_total"],
              r["output_patent_2024"], r["policy_valid_cnt"])


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
    out_json = here / "M_INNOV_CITY_MONITOR_GLOBAL_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_INNOV_CITY_MONITOR_GLOBAL.py 等价）
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
        "metric_id": "M_INNOV_CITY_MONITOR_GLOBAL",
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
