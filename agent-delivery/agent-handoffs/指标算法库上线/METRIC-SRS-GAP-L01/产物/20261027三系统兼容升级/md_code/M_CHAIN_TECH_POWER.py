#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_CHAIN_TECH_POWER 技术能力
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_CHAIN_TECH_POWER.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_CHAIN_TECH_POWER · 技术能力（链技术力）（gkx 单库代理版）

王惠三维框架（旧稿沿用）
------------------------
技术力 = (D1 专利规模 + D2 断链壁垒 + D3 成熟度) / 3，等权，min-max 归一到 0—1。
  D1 专利规模：链内企业专利总量取 log 后 min-max
  D2 断链壁垒：1 − K 节点覆盖率（关键环节无人覆盖 = 技术空白）
  D3 成熟度：近一年（2024）申请量 / 全期申请量（专利存量的「新鲜度」）

数据事实
--------
`tech_power` 结果面在 gkx 不存在（source_absent，见 TABLE_ABSENCE_EVIDENCE §tech_power）。
D1/D3 用 `dwd_patent`（2,939,895 行，2021—2026 窗口）按申请人名聚合的落盘快照；
D2 用 `dwd_org_industry_tags` × `dwd_industry_chain_info` 的深圳 K 覆盖快照。
D2 只有深圳口径（全国 K 覆盖没有落盘），已在 proxy_deviation 披露。

输出：code/M_CHAIN_TECH_POWER_out.json
"""
from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_CHAIN_TECH_POWER_out.json"
METRIC = "M_CHAIN_TECH_POWER"


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def minmax(vals):
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return [0.5 for _ in vals]
    return [(v - lo) / (hi - lo) for v in vals]


def main() -> None:
    name2chain = load("chain21_layer_20261022.json")["names"]
    roots = {c["chain"]: c["name"] for c in load("chain_panel21.json")["chains"]}

    pat = defaultdict(int)
    ipc = defaultdict(set)
    for ipc4, name, c in load("patent_ipc4_by_name_20261021.json"):
        ch = name2chain.get(name)
        if not ch:
            continue
        pat[ch] += c
        ipc[ch].add(ipc4)

    p24 = load("patent_2024_by_name_20261021.json")
    apply24 = defaultdict(int)
    for name, v in p24.items():
        ch = name2chain.get(name)
        if ch and isinstance(v, list) and v:
            apply24[ch] += int(v[0])

    cov = load("chain21_sz_nodecov_20261022.json")["chains"]

    base = []
    for code in sorted(roots):
        k = cov.get(code, {})
        k_nodes = k.get("K_nodes", 0)
        k_cov = k.get("k_covered", 0)
        gap = round(1 - k_cov / k_nodes, 4) if k_nodes else None
        base.append({
            "chain": code, "chain_name": roots[code],
            "patents": pat.get(code, 0), "ipc4_breadth": len(ipc.get(code, ())),
            "patents_2024_apply": apply24.get(code, 0),
            "recency": round(apply24.get(code, 0) / pat[code], 4) if pat.get(code) else None,
            "k_nodes": k_nodes, "k_covered": k_cov, "uncov_share": gap,
        })

    d1 = minmax([math.log1p(r["patents"]) for r in base])
    d2 = [r["uncov_share"] if r["uncov_share"] is not None else 0.0 for r in base]
    d3 = minmax([r["recency"] if r["recency"] is not None else 0.0 for r in base])
    for i, r in enumerate(base):
        r["d1_patent_scale"] = round(d1[i], 4)
        r["d2_barrier"] = round(d2[i], 4)
        r["d3_recency"] = round(d3[i], 4)
        r["tech_power"] = round((d1[i] + d2[i] + d3[i]) / 3, 4)
    base.sort(key=lambda r: -r["tech_power"])
    for i, r in enumerate(base, 1):
        r["rank"] = i

    total_pat = sum(r["patents"] for r in base)
    out = {
        "metric_id": METRIC,
        "metric_name": "技术能力（链技术力）",
        "data_source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）+ code/_snapshots21/ 落盘快照",
        "formula": "tech_power = (D1专利规模 + D2断链壁垒 + D3近一年申请占比) / 3，各维 min-max 归一",
        "blocking_tables": {
            "tech_power": {
                "triage": "source_absent",
                "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §tech_power",
            }
        },
        "proxy_path": "dwd_patent 按申请人名聚合（D1/D3）+ 深圳 K 节点覆盖（D2）",
        "proxy_deviation": "D2 只有深圳口径的 K 覆盖（全国环节覆盖未落盘），12 链的壁垒分实际是「深圳缺环率」；D1/D3 只统计能按名挂链的企业（36,993/189,116），链内专利总量是下限",
        "weights": {"d1": 1 / 3, "d2": 1 / 3, "d3": 1 / 3,
                    "note": "等权为项目默认值，甲方未裁定权重"},
        "totals": {"patents_12_chains": total_pat, "patent_table_rows": 2939895,
                   "chains": len(base), "equal_weight": True},
        "chains": base,
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": "tech_power 结果面不存在，但三维里有二维半可用：专利规模与近一年申请占比都能从 dwd_patent 的 2,939,895 行按申请人名聚合出来（12 链合计专利见 totals），断链壁垒可以用 K 节点未覆盖率算，但只有深圳口径。权重是等权默认值、甲方未裁定。结构与数据都够跑，缺的是全国 K 覆盖与官方权重，判部分支持。",
            "criteria": {
                "result_table_exists": False,
                "dims_total": 3,
                "dims_full": 2,
                "dims_partial": 1,
                "patent_rows": 2939895,
                "proxy_used": True,
            },
        },
        "base_years_used": [2021, 2022, 2023, 2024],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": "专利表 apdt_year 只有 2021—2026，2017—2020 零行（DATA_FACTS 陷阱 3.13），所以「近一年占比」的分母是 2021—2024 全期申请，不是十年存量；2025/2026 为不完整年，不进分母。",
        "sources": [
            {"path": "code/_snapshots21/patent_ipc4_by_name_20261021.json",
             "table": "gkx.dwd_patent", "rows": 581585,
             "role": "企业×IPC4 专利计数（D1 与 IPC 广度）"},
            {"path": "code/_snapshots21/patent_2024_by_name_20261021.json",
             "table": "gkx.dwd_patent", "rows": 60009,
             "role": "企业 2024 申请/授权（D3 新鲜度）"},
            {"path": "code/_snapshots21/chain21_sz_nodecov_20261022.json",
             "table": "gkx.dwd_org_industry_tags × gkx.dwd_industry_chain_info",
             "rows": 116017, "role": "深圳 K 节点覆盖（D2）"},
            {"path": "code/_snapshots21/chain21_layer_20261022.json",
             "table": "gkx.dwd_org_industry_tags", "rows": 36993,
             "role": "企业名→链映射"},
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[OK] {METRIC} -> {OUT.name} total_pat={total_pat}")
    for r in base:
        print(f"  #{r['rank']:<2} {r['chain']} {r['chain_name'][:8]:<8} pat={r['patents']:<7} "
              f"ipc={r['ipc4_breadth']:<3} rec={r['recency']} uncov={r['uncov_share']} "
              f"-> {r['tech_power']}")


if __name__ == "__main__":
    main()


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题服务算法库', '科技信息展示系统']

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
    out_json = here / "M_CHAIN_TECH_POWER_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_CHAIN_TECH_POWER.py 等价）
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
        "metric_id": "M_CHAIN_TECH_POWER",
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
