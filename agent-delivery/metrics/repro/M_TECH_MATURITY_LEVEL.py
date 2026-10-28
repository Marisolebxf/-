#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_TECH_MATURITY_LEVEL 技术成熟度
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D2 口径级分歧（本件复核为可兼容·配置型） ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_TECH_MATURITY_LEVEL.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_TECH_MATURITY_LEVEL —— 技术成熟度等级（L1—L5，深圳口径）。

口径（单一，深圳）：
  - 域 = IPC 主分类前 4 位；样本门槛 n2024 >= 100 件；
  - 件数、申请人、发明件数全部只取「深圳市申请人」；
  - 授权数按「申请人域内专利份额 × 该申请人全期授权数」分摊到域，
    不是专利级逐件授权标记（库内无 pn 级授权位，详见 §三 D2）；
  - 全国件数不参与任何分母，本件不出现全国列。

五维得分（0—100，绝对锚点，非分位），特征层见 `_tech21_domainfeat.py`：
  S1 规模 25%   n2024 的对数刻度，100 件=0，10,000 件=100
  S2 授权 25%   分摊全期授权比，0.50=0，0.90=100
  S3 发明 15%   分摊发明占比，0.15=0，0.70=100
  S4 集中 15%   申请人 HHI 的对数刻度，50=0，1,000=100
  S5 稳定 20%   近端增长 |g| 越小越高，|g|>=0.50 记 0

零 SQL：只读 _snapshots21 / _snapshots_gkx21 授权缓存。
"""
from __future__ import annotations

import collections
import statistics

import _tech21_scope as sc
import _tech21_domainfeat as feat

METRIC = "M_TECH_MATURITY_LEVEL"
YEARS = feat.YEARS


def main():
    rows, meta = feat.build()
    rows = sorted(rows, key=lambda r: -r["maturity_score"])
    dist = collections.Counter(r["maturity_level"] for r in rows)
    by_level = {}
    for lv in ("L1", "L2", "L3", "L4", "L5"):
        sub = [r for r in rows if r["maturity_level"] == lv]
        by_level[lv] = {
            "domains": len(sub),
            "share": round(len(sub) / len(rows), 4),
            "n2024": sum(r["n2024"] for r in sub),
            "n2024_share": round(sum(r["n2024"] for r in sub) / meta["qualified_total_2024"], 4),
            "score_range": [min((r["maturity_score"] for r in sub), default=None),
                            max((r["maturity_score"] for r in sub), default=None)],
            "examples": [r["ipc4"] for r in sub[:6]],
        }

    scores = [r["maturity_score"] for r in rows]
    tight = [r for r in rows if r["maturity_level"] in ("L4", "L5")]
    loose = [r for r in rows if r["maturity_level"] in ("L1", "L2")]

    payload = {
        "metric_id": METRIC,
        "generated_at": "2026-10-22",
        "scope": "深圳",
        "scope_statement": (
            "本件唯一分母是深圳：域件数、申请人数、发明件数、授权分摊全部只落在"
            "深圳市申请人上。全国件数不参与任何分母，正文不出现「全国成熟度」列；"
            "因此本件的等级是「深圳样本内等级」，不是全国技术就绪度。"
        ),
        "main_db": "gkx @ 183.240.141.251:3318 (gkx_reader_zp, read-only)",
        "sql_count": 0,
        "base_years_used": YEARS,
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": (
            "专利年序列只遍历库内真实存在的 2021—2024 四年（2025/2026 为采集残年，"
            "不进入稳定性分母）；2017—2020 在 dwd_patent 零行，未按 0 补入任何均值或斜率。"
            "授权与发明件数是全期累计值（非逐年年份队列），因此 S2/S3 是「跨期平均」，"
            "不是 2024 单年队列授权率。"
        ),
        "input": {
            "sz_patent": "code/_snapshots21/patent_scan_20261021.pkl",
            "ipc_by_name": "code/_snapshots21/patent_ipc4_by_name_20261021.json",
            "applicant_agg": "code/_snapshots21/star_applicant_agg_gkx.json",
            "sz_applicants": "code/_snapshots_gkx21/sz_patent_city_name_gkx.json",
        },
        "reused_from": "_tech21_domainfeat.py（域特征层，零 SQL）",
        "alloc_meta": {
            "agg_table_rows": meta["agg_table_rows"],
            "agg_names": meta["agg_names"],
            "sz_applicants": meta["sz_applicants"],
            "ipc_by_name_rows": meta["ipc_by_name_rows"],
            "method": "域授权=Σ_申请人(域内件数/该申请人全期件数×该申请人全期授权数)",
            "assumption": "同一申请人在各 IPC4 域的授权率相同；该假设无法用现有缓存逐件校验",
            "zero_grant_applicants": "agg 中授权数为 0 的申请人按 0 计入，不剔除",
        },
        "weights": feat.WEIGHTS,
        "level_cuts": feat.LEVEL_CUTS,
        "panel": {
            "sz_domains_all": meta["sz_domains_all"],
            "qualified_domains": meta["qualified"],
            "qualified_n2024_sum": meta["qualified_total_2024"],
            "sz_all_n2024": meta["sz_total_2024"],
            "qualified_coverage_2024": round(meta["qualified_total_2024"] / meta["sz_total_2024"], 4),
            "sz_year_total": meta["sz_year_total"],
        },
        "level_distribution": by_level,
        "score_stats": {
            "min": round(min(scores), 2), "max": round(max(scores), 2),
            "mean": round(statistics.mean(scores), 2),
            "median": round(statistics.median(scores), 2),
            "quartiles": [round(x, 2) for x in statistics.quantiles(scores, n=4)],
        },
        "top20": [{"ipc4": r["ipc4"], "label": r["label"], "n2024": r["n2024"],
                   "score": r["maturity_score"], "level": r["maturity_level"],
                   "grant_ratio": r["grant_ratio"], "invention_share": r["invention_share"],
                   "hhi": r["hhi"], "parts": r["maturity_parts"]} for r in rows[:20]],
        "bottom20": [{"ipc4": r["ipc4"], "label": r["label"], "n2024": r["n2024"],
                      "score": r["maturity_score"], "level": r["maturity_level"],
                      "grant_ratio": r["grant_ratio"], "invention_share": r["invention_share"],
                      "hhi": r["hhi"], "parts": r["maturity_parts"]} for r in rows[-20:]],
        "high_maturity_examples": [{"ipc4": r["ipc4"], "label": r["label"],
                                    "score": r["maturity_score"], "level": r["maturity_level"],
                                    "n2024": r["n2024"], "grant_ratio": r["grant_ratio"],
                                    "hhi": r["hhi"]} for r in tight[:8]],
        "low_maturity_examples": [{"ipc4": r["ipc4"], "label": r["label"],
                                   "score": r["maturity_score"], "level": r["maturity_level"],
                                   "n2024": r["n2024"], "grant_ratio": r["grant_ratio"],
                                   "hhi": r["hhi"]} for r in loose[-8:]],
        "domains": rows,
        "support_judgment": {
            "data_support_level": "部分支持",
            "structure_support": "部分",
            "data_support": "部分",
            "reason": (
                "五维里规模、授权比、发明占比、集中度、稳定性都有结构，但成熟度的核心证据"
                "（技术就绪度 TRL、被引、标准/中试、市场渗透）在本库不存在：被引表仅 20,515 行"
                "（覆盖 0.70%），无 TRL、无技术标准表；授权数只能按申请人份额分摊、无 pn 级"
                "授权位。故只能交付「专利形态五级」，不是 TRL 1—9。"
            ),
        },
    }
    sc.write_out(METRIC, payload)


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
    out_json = here / "M_TECH_MATURITY_LEVEL_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_TECH_MATURITY_LEVEL.py 等价）
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
        "metric_id": "M_TECH_MATURITY_LEVEL",
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
