#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_TECH_LIFE_STAGE 技术发展阶段
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_TECH_LIFE_STAGE.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_TECH_LIFE_STAGE —— 技术生命周期阶段（萌芽 / 成长 / 成熟 / 衰退）。

口径（单一，深圳）：
  - 主体 = 深圳市申请人（`dwd_org_base_info.name_cn` 归属到「深圳市」的 77,846 个名称）；
  - 件数 = 申请年 2021—2024、按 pn 去重、IPC 主分类前 4 位（`patent_scan_20261021.pkl`）；
  - 分母 = 每个 IPC4 域自身的 2021 年与 2023 年件数，不跨城、不跨域；
  - 全国件数只在一张「参照表」里出现（LQ 分母），不进入任何阶段判定。

零 SQL：只读 _snapshots21 / _snapshots_gkx21 授权缓存。
基期：2017—2020 在 dwd_patent 为零行（DATA_FACTS_gkx21 §3.13），只允许 2021 起算。
"""
from __future__ import annotations

import collections
import statistics

import _tech21_scope as sc
from _tech21_common import IPC_LABEL

METRIC = "M_TECH_LIFE_STAGE"
YEARS = [2021, 2022, 2023, 2024]

# 2025.01 版 IPC 新码（半导体族从 H01L 迁入），增长率不可与旧码直接比较
NEW_CODES = {"H10B", "H10D", "H10F", "H10H", "H10K", "H10N", "H10P", "H10W"}


def build_panel():
    cell, _ = sc.load_sz_ipc()
    domains = {d for (d, y) in cell}
    panel = {d: {y: int(cell.get((d, y), 0)) for y in YEARS} for d in domains}
    return panel


def classify(v):
    """四阶段判定（顺序即优先级：萌芽 > 衰退 > 成长 > 成熟）。"""
    n21, n22, n23, n24 = v[2021], v[2022], v[2023], v[2024]
    g_total = (n24 - n21) / n21 if n21 else None
    g_near = (n24 - n23) / n23 if n23 else None
    if g_total is None or g_near is None:
        return "缺基期", g_total, g_near
    if g_total >= 1.00 and n21 < 500 and n24 < 1500:
        return "萌芽", g_total, g_near
    if g_total <= -0.20 or g_near <= -0.20:
        return "衰退", g_total, g_near
    if g_total >= 0.20 and g_near > 0:
        return "成长", g_total, g_near
    return "成熟", g_total, g_near


def main():
    panel = build_panel()
    nat_cell, nat_year = sc.load_nat_ipc()
    sz_year = collections.Counter()
    for d, v in panel.items():
        for y in YEARS:
            sz_year[y] += v[y]

    qualified = sorted([d for d, v in panel.items() if v[2024] >= 100])
    rows = []
    for d in qualified:
        v = panel[d]
        stage, g_total, g_near = classify(v)
        lq = None
        if nat_cell.get((d, 2024)):
            lq = ((v[2024] / sz_year[2024]) /
                  (nat_cell[(d, 2024)] / nat_year[2024]))
        rows.append({
            "ipc4": d, "label": IPC_LABEL.get(d, ""), "n": [v[y] for y in YEARS],
            "g_total": None if g_total is None else round(g_total, 4),
            "g_near": None if g_near is None else round(g_near, 4),
            "stage": stage, "lq_2024": None if lq is None else round(lq, 4),
            "new_code": d in NEW_CODES,
        })

    dist = collections.Counter(r["stage"] for r in rows)
    by_stage = {}
    for st in ("萌芽", "成长", "成熟", "衰退"):
        sub = [r for r in rows if r["stage"] == st]
        lqs = [r["lq_2024"] for r in sub if r["lq_2024"] is not None]
        by_stage[st] = {
            "domains": len(sub),
            "share": round(len(sub) / len(rows), 4),
            "n2024": sum(r["n"][3] for r in sub),
            "n2024_share": round(sum(r["n"][3] for r in sub) / sz_year[2024], 4),
            "lq_median": round(statistics.median(lqs), 4) if lqs else None,
            "new_codes": sorted(r["ipc4"] for r in sub if r["new_code"]),
        }

    def top(key, reverse, k=15):
        pool = [r for r in rows if r[key] is not None]
        pool.sort(key=lambda r: r[key], reverse=reverse)
        return [{"ipc4": r["ipc4"], "label": r["label"], "stage": r["stage"],
                 "n2021": r["n"][0], "n2024": r["n"][3],
                 "g_total": r["g_total"], "g_near": r["g_near"],
                 "lq_2024": r["lq_2024"], "new_code": r["new_code"]}
                for r in pool[:k]]

    # 规模分层 × 阶段交叉
    bands = [(100, 499), (500, 999), (1000, 4999), (5000, 10 ** 9)]
    cross = []
    for lo, hi in bands:
        sub = [r for r in rows if lo <= r["n"][3] <= hi]
        c = collections.Counter(r["stage"] for r in sub)
        cross.append({"band": f"{lo}-{hi if hi < 10**9 else 'max'}", "domains": len(sub),
                      "萌芽": c["萌芽"], "成长": c["成长"], "成熟": c["成熟"], "衰退": c["衰退"]})

    # 新码剔除后的敏感性
    no_new = [r for r in rows if not r["new_code"]]
    new_share = collections.Counter(r["stage"] for r in rows if r["new_code"])
    sens = {
        "all": dict(dist),
        "excl_new_codes": dict(collections.Counter(r["stage"] for r in no_new)),
        "new_code_domains": len([r for r in rows if r["new_code"]]),
        "new_code_stage": dict(new_share),
    }

    # 全国参照（只做 LQ 分母，单独成表）
    nat_ref = {str(y): nat_year[y] for y in YEARS}
    sz_ref = {str(y): sz_year[y] for y in YEARS}

    payload = {
        "metric_id": METRIC,
        "generated_at": "2026-10-22",
        "scope": "深圳",
        "scope_statement": (
            "本件唯一分母是深圳：域件数、阶段判定、规模分层全部只用深圳市申请人的"
            "2021—2024 申请年件数。全国件数只在 §2.6 的 LQ 参照表出现，作 LQ 分母，"
            "不进入任何阶段规则，也不与深圳件数同列相加。"
        ),
        "main_db": "gkx @ 183.240.141.251:3318 (gkx_reader_zp, read-only)",
        "sql_count": 0,
        "base_years_used": YEARS,
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": (
            "dwd_patent.apdt_year 只有 2021—2026，2017—2020 零行；因此基期只能取 2021，"
            "四年窗口为 2021—2024。2025（440,401 件）与 2026（74,810 件）是采集残年，"
            "不进入增长分母；缺失年不按 0 摊入任何均值。"
        ),
        "input": {
            "sz_patent": "code/_snapshots21/patent_scan_20261021.pkl",
            "nat_patent": "code/_snapshots21/patent_panel_innov_20261021.json",
            "sz_applicants": "code/_snapshots_gkx21/sz_patent_city_name_gkx.json",
        },
        "reused_from": "_tech21_scope.py（共用离线取数层，零 SQL）",
        "thresholds": {
            "sample_gate_n2024": 100,
            "sprout": "g_total>=1.00 且 n2021<500 且 n2024<1500",
            "decline": "g_total<=-0.20 或 g_near<=-0.20",
            "growth": "g_total>=0.20 且 g_near>0",
            "mature": "其余",
            "rule_order": "萌芽 > 衰退 > 成长 > 成熟（互斥）",
        },
        "panel": {
            "sz_domains_all": len(panel),
            "sz_domains_2024": len([d for d, v in panel.items() if v[2024] > 0]),
            "qualified_domains": len(rows),
            "sz_year_total": sz_ref,
            "nat_year_total": nat_ref,
        },
        "stage_distribution": by_stage,
        "top_growth": top("g_total", True, 15),
        "top_decline": top("g_total", False, 15),
        "top_near_growth": top("g_near", True, 10),
        "top_near_decline": top("g_near", False, 10),
        "size_band_cross": cross,
        "sensitivity": sens,
        "domains": rows,
        "support_judgment": {
            "data_support_level": "部分支持",
            "structure_support": "部分",
            "data_support": "部分",
            "reason": (
                "四年申请年面板可复算四阶段形态（238 域），但生命周期需要技术替代关系、"
                "法律状态与更长序列；库内 patent 只有主分类、无替代关系，2017—2020 零行，"
                "被引覆盖 0.70%，因此只能交付「申请量形态阶段」，不能交付技术生命周期本体。"
            ),
        },
        "headline": {
            "qualified": len(rows),
            "sprout": dist["萌芽"], "growth": dist["成长"],
            "mature": dist["成熟"], "decline": dist["衰退"],
            "sprout_new_codes": len(by_stage["萌芽"]["new_codes"]),
            "sz_total_2024": sz_year[2024],
            "sz_total_2021": sz_year[2021],
            "sz_change_2021_2024": round((sz_year[2024] - sz_year[2021]) / sz_year[2021], 4),
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
    out_json = here / "M_TECH_LIFE_STAGE_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_TECH_LIFE_STAGE.py 等价）
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
        "metric_id": "M_TECH_LIFE_STAGE",
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
