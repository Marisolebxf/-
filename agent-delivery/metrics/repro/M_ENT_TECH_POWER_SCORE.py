#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ENT_TECH_POWER_SCORE 技术力得分
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ENT_TECH_POWER_SCORE.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_ENT_TECH_POWER_SCORE · 企业技术力评分（gkx 单库代理版）

旧稿口径
--------
企业技术力 = 0.5×专利规模 + 0.3×技术领域广度 + 0.2×技术新鲜度，各维 min-max 归一到 0—1。
  D1 专利规模：log1p(专利数)
  D2 广度：IPC4 distinct 数
  D3 新鲜度：2024 年申请量 / 全期申请量

数据事实
--------
`tech_power` 与 `enterprise_score` 两张结果面在 gkx 都不存在（均 source_absent，
见 TABLE_ABSENCE_EVIDENCE 对应两节）。可用的只有专利侧：
`dwd_patent` 按申请人聚合的 581,585 条企业×IPC4 与 60,009 条 2024 申请/授权。
旧稿里「人才、成果转化、研发投入」三维在 gkx 没有任何可挂到企业个体的表，
本件不造这三项，只出专利三维分，并明确标注为「专利技术力」而非完整技术力。

输出：code/M_ENT_TECH_POWER_SCORE_out.json
"""
from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_ENT_TECH_POWER_SCORE_out.json"
METRIC = "M_ENT_TECH_POWER_SCORE"


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def main() -> None:
    ipc = defaultdict(set)
    pat = defaultdict(int)
    for ipc4, name, c in load("patent_ipc4_by_name_20261021.json"):
        ipc[name].add(ipc4)
        pat[name] += c
    apply24 = {n: int(v[0]) for n, v in load("patent_2024_by_name_20261021.json").items()
               if isinstance(v, list) and v}

    names = [n for n in ipc if pat[n] >= 1]
    logs = {n: math.log1p(pat[n]) for n in names}
    brd = {n: len(ipc[n]) for n in names}
    rec = {n: (apply24.get(n, 0) / pat[n] if pat[n] else 0.0) for n in names}

    def norm(d):
        lo, hi = min(d.values()), max(d.values())
        span = (hi - lo) or 1.0
        return {k: (v - lo) / span for k, v in d.items()}

    n1, n2, n3 = norm(logs), norm(brd), norm(rec)
    score = {n: 0.5 * n1[n] + 0.3 * n2[n] + 0.2 * n3[n] for n in names}

    city_of = load("org_name_city_20261021.json")["map"]
    top = sorted(score.items(), key=lambda x: -x[1])[:100]
    rows = [{"rank": i, "name": n, "score": round(s, 4), "patents": pat[n],
             "ipc4_breadth": brd[n], "recency_2024": round(rec[n], 4),
             "city": city_of.get(n)}
            for i, (n, s) in enumerate(top, 1)]

    vals = sorted(score.values())
    def pct(q):
        return round(vals[min(len(vals) - 1, int(q * (len(vals) - 1)))], 4)

    city_scores = defaultdict(list)
    for n, s in score.items():
        c = city_of.get(n)
        if c:
            city_scores[c].append(s)
    city_rows = [{"city": c, "orgs": len(a), "mean_score": round(sum(a) / len(a), 4),
                  "max_score": round(max(a), 4)}
                 for c, a in sorted(city_scores.items(), key=lambda x: -len(x[1]))[:8]]

    out = {
        "metric_id": METRIC,
        "metric_name": "企业技术力评分",
        "data_source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）+ code/_snapshots21/ 落盘快照",
        "formula": "score = 0.5*minmax(log1p(专利数)) + 0.3*minmax(IPC4广度) + 0.2*minmax(2024申请占比)",
        "blocking_tables": {
            "tech_power": {"triage": "source_absent",
                           "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §tech_power"},
            "enterprise_score": {"triage": "source_absent",
                                 "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §enterprise_score"},
        },
        "proxy_path": "dwd_patent 三维（规模/广度/新鲜度）→ 0.5/0.3/0.2 加权",
        "proxy_deviation": "旧稿技术力含「人才、成果转化、研发投入」三维，gkx 无企业级载体，本件只出专利三维，是有偏的：研发投入大但专利少的企业会被低估，代工型专利多的企业会被高估；权重 0.5/0.3/0.2 为项目默认值",
        "coverage": {"orgs_scored": len(names), "orgs_total_base": 189116,
                     "ipc4_name_rows": 581585, "weight": {"d1": 0.5, "d2": 0.3, "d3": 0.2}},
        "distribution": {"p25": pct(0.25), "median": pct(0.5), "p75": pct(0.75),
                         "p90": pct(0.9), "p99": pct(0.99), "max": pct(1.0)},
        "cities": city_rows,
        "top100": rows,
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": "两张结果面（tech_power、enterprise_score）都不存在，旧稿六维里只有专利侧三维能从 dwd_patent 逐企业算出，人才/转化/投入三维在 gkx 没有任何企业级表可挂。专利三维本身结构与量都够（134,152 家企业有专利），可产出完整分布与排名；缺三维意味着分值是「专利技术力」而不是「技术力」，故判部分支持而不是完全转换支持。",
            "criteria": {
                "result_tables": 2, "result_tables_present": 0,
                "dims_total": 6, "dims_computable": 3,
                "orgs_scored": len(names), "proxy_used": True,
            },
        },
        "base_years_used": [2021, 2022, 2023, 2024],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": "专利表只有 2021—2026（2017—2020 零行），D1 分母是全期申请，D3 用 2024 年申请占比；2025/2026 为残年不入分子。人才/转化维不涉及年份，因整维缺失而不存在基期。",
        "sources": [
            {"path": "code/_snapshots21/patent_ipc4_by_name_20261021.json",
             "table": "gkx.dwd_patent", "rows": 581585,
             "role": "企业×IPC4 计数（D1/D2）"},
            {"path": "code/_snapshots21/patent_2024_by_name_20261021.json",
             "table": "gkx.dwd_patent", "rows": 60009,
             "role": "2024 申请量（D3）"},
            {"path": "code/_snapshots21/org_name_city_20261021.json",
             "table": "gkx.dwd_org_base_info", "rows": 189068,
             "role": "企业名→城市"},
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[OK] {METRIC} -> {OUT.name} scored={len(names)} median={out['distribution']['median']}")
    for r in rows[:5]:
        print("  ", r["rank"], r["name"][:20], r["score"], r["patents"], r["ipc4_breadth"])


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
    out_json = here / "M_ENT_TECH_POWER_SCORE_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ENT_TECH_POWER_SCORE.py 等价）
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
        "metric_id": "M_ENT_TECH_POWER_SCORE",
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
