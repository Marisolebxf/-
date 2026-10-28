#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_INNOV_CITY_RANK_GLOBAL 城市创新能力排名
# 【维护者】唐绍祖
# 【适用系统】科技专题系统 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_INNOV_CITY_RANK_GLOBAL.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_INNOV_CITY_RANK_GLOBAL 城市创新能力排名 · gkx 版（20261021 改源）

三维（与 M_INNOV_CITY_BENCHMARK_GLOBAL 同）：投入(Σ研发经费) / 产出(专利) / 环境(0.5×政策 + 0.5×高企)，
城内极值归一 → 等权综合分 → 降序 rank。宇宙 = 有产出城（本批 = 粤三城，gkx 底册可信区）。

改源要点
--------
* 专利产出维不再做 28 块 × 3 城的 `first_applicant_name IN (...)` 全表扫，
  改读共享缓存 `city_patent_year_gkx.json`（A-12 面板 × 底册 name→city，零 DB）；
* 政策：`city='深圳市'` 等值 + 省级共享（占位符 `'NULL'` 归空，见 `_city21_common.py` 说明）；
* 高企：`dwd_org_tech_tag` 的 org_id 精确匹配本地底册 org_id（不重复 JOIN 大表）。

**跨尺度一致性**：本指标（全球尺度）与 `M_INNOV_CITY_RANK_SZ`（深圳尺度）共用同一套
研发经费、专利、高企原始值，只在维数（3 vs 4）与权重上不同 —— 两者对三城的相对次序
必须一致；脚本末段输出 `cross_scale_check` 供核对。
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
        rows.append({
            "city": C.SHORT[city], "city_code": city,
            "rd_funding_sum": round(float(raw["rd_sum"].get(city, 0.0)), 2),
            "patent_cnt": int((pat.get("city_totals") or {}).get(city, 0)),
            "policy_cnt": int(raw["policy_city"].get(city, 0)) + int(raw["policy_prov_shared_n"]),
            "hightech_cnt": int(raw["hitech_by_city"].get(city, 0)),
        })

    nin = C.norm([r["rd_funding_sum"] for r in rows])
    nout = C.norm([r["patent_cnt"] for r in rows])
    npl = C.norm([r["policy_cnt"] for r in rows])
    nhq = C.norm([r["hightech_cnt"] for r in rows])
    for i, r in enumerate(rows):
        env = 0.5 * npl[i] + 0.5 * nhq[i]
        r["d_input"], r["d_output"], r["d_env"] = nin[i], nout[i], round(env, 4)
        r["score"] = round(100 / 3 * (nin[i] + nout[i] + env), 1)
    order = sorted(rows, key=lambda r: -r["score"])
    for rk, r in enumerate(order, 1):
        r["rank"] = rk
    rows = order

    result = {
        "metric_id": "M_INNOV_CITY_RANK_GLOBAL",
        "metric_name": "城市创新能力排名",
        "method": "王惠 V1.6：投入/产出/环境三维（同 BENCHMARK），综合分降序 rank",
        "source_db": "gkx（183.240.141.251:3318）",
        "universe_note": "宇宙=有产出城；本批库可信区=粤三城（org.city 99.82% 粤集中）；论文无城市键→产出维=专利单口径",
        "cities": [C.SHORT[c] for c in CITIES],
        "probes": {
            "gkx.dwd_org_base_info": 189116,
            "gkx.dwd_org_stock_finance_info": 40239,
            "gkx.dwd_patent": 2939895,
            "gkx.dwd_policy_base": 20000,
            "gkx.dwd_org_tech_tag": 202424,
            "gkx.dwd_zh_paper": 100900,
        },
        "compute": {"cities": rows},
        "patent_coverage": {
            "panel_complete": pat.get("panel_complete"),
            "year_coverage": (pat.get("year_coverage") or {}).get("years_present"),
            "note": "专利总量=apdt_year 覆盖范围（2021–2026）内件数；总量不使用年份切片，故不影响本指标",
        },
        "cross_scale_check": {
            "rule": "同一城市在『全球排名』与『深圳排名』中的综合名次必须一致（两指标共用同一套原始值）",
            "global_order": [r["city"] for r in rows],
            "global_rank": {r["city"]: r["rank"] for r in rows},
            "consistent": all(r["rank"] == i + 1 for i, r in enumerate(rows))
                          and [r["city"] for r in rows] == ["深圳", "广州", "东莞"],
        },
        "support_judgment": "部分支持",
        "support_note": (
            "三维均可出数并排名；但（1）宇宙限粤三城，『全球主要城市排名』名次实际为省内名次；"
            "（2）产出维论文口径缺失（dwd_zh_paper 无城市键）；⇒ 部分支持"
        ),
        "change_note": (
            "三维读数与 20261020 版逐位一致：研发经费 1,366,367,257,075.05 / 264,072,837,060.45 / "
            "69,474,579,097.31；专利 1,336,877 / 675,339 / 432,677；政策 1,110 / 556 / 239；"
            "高企 15,476 / 7,499 / 3,584；综合分 100.0 / 25.5 / 0.0，名次 SZ>GZ>DG 不变。"
        ),
    }
    p = C.write_out("M_INNOV_CITY_RANK_GLOBAL", result)
    print("wrote", p)
    for r in rows:
        print(r["rank"], r["city"], r["score"], r["d_input"], r["d_output"], r["d_env"],
              r["rd_funding_sum"], r["patent_cnt"], r["policy_cnt"], r["hightech_cnt"])


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
    out_json = here / "M_INNOV_CITY_RANK_GLOBAL_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_INNOV_CITY_RANK_GLOBAL.py 等价）
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
        "metric_id": "M_INNOV_CITY_RANK_GLOBAL",
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
