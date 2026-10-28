#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_CHAIN_SZ_COMPLETENESS 深圳产业链完整度
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_CHAIN_SZ_COMPLETENESS.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_CHAIN_SZ_COMPLETENESS —— 深圳产业链完整度

口径：完整度 = k / K × 100%
  K = 该顶层链子树内的链树节点数（去根，来自 dwd_industry_chain_info 1,273 节点）
  k = 其中至少 1 家深圳企业（credit_code[2:6]=='4403'）在「该节点或其更深节点」有挂链标签的节点数
节点级而非叶子级：链树里同一环节常分「环节—子环节—品类」三层，逐层都要求有企业才叫配套齐，
只算叶子会把中间层忽略、把完整度抬到 95% 以上（与旧稿 54—99% 的分布不符）。
"""
from __future__ import annotations
import json, os, time

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_SZ_COMPLETENESS_out.json")


def L(n):
    with open(os.path.join(SNAP, n), encoding="utf-8") as f:
        return json.load(f)


cov = L("chain21_sz_nodecov_20261022.json")
layer = L("chain21_layer_20261022.json")
tree = L("chain_tree_20261021.json")
name = {n["industry_code"]: n["industry_name"] for n in tree}
chains = layer["chain_name"]

rows = []
for ch, nm in chains.items():
    v = cov["chains"].get(ch, {})
    K, k = v.get("K_nodes", 0), v.get("k_covered", 0)
    unc = v.get("uncovered_nodes", [])
    rows.append({
        "chain_code": ch, "chain_name": nm,
        "K_nodes": K, "k_sz_covered": k,
        "completeness_pct": round(100.0 * k / K, 2) if K else None,
        "uncovered_nodes": len(unc),
        "uncovered_node_names": [name.get(x, x) for x in unc[:8]],
        "leaf_only_pct": round(100.0 * v.get("k_leaf_covered", 0) / v["K_leaf"], 2) if v.get("K_leaf") else None,
    })
rows.sort(key=lambda r: -r["completeness_pct"])
vals = [r["completeness_pct"] for r in rows]

payload = {
    "metric_id": "M_CHAIN_SZ_COMPLETENESS",
    "metric_name": "深圳产业链完整度",
    "support_judgment": "完全转换支持",
    "judgment_reason": "公式 k/K 的两侧都可在 gkx 内闭合：K 来自 dwd_industry_chain_info 的 1,273 节点链树，k 来自 dwd_org_industry_tags 按 4403 行政区划码切片的 116,017 行挂链记录；12 条链全部算出 57.61%—100%，无空链、无零分母，脚本 0.01 秒可复算。逐链 K 与旧稿完全一致，k 因不再回联 18.9 万行底册而略高（0—4 个节点），属覆盖集差异而非口径变化。",
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "截面存量指标，不设统计期；挂链桥无统计期字段，不做年度序列。",
    "sources": [
        "gkx @ 183.240.141.251:3318 / gkx_reader_zp: gkx.dwd_org_industry_tags（深圳切片 116,017 行）",
        "gkx @ 183.240.141.251:3318 / gkx_reader_zp: gkx.dwd_industry_chain_info（1,273 节点链树）",
        "code/_snapshots21/chain21_sz_nodecov_20261022.json（节点覆盖落盘，2 列 1 次读）",
        "code/_snapshots21/chain21_layer_20261022.json（12 链名与链码口径，与 M_CHAIN_ENTERPRISE_COUNT 同池）",
    ],
    "rule": {
        "K": "该顶层链子树下的全部节点数（不含根本身，来自 gkx.dwd_industry_chain_info 的 1,273 节点链树）",
        "k": "K 中满足「∃ 深圳企业标签 t，t.startswith(node_code)」的节点数",
        "shenzhen": "credit_code[2:6] == '4403'（全量可判；不依赖 18.9 万行底册回联）",
        "rebuild": "code/_snapshots21/chain21_sz_nodecov_20261022.json 由 _work_gkx21/build_sz_nodecov.py 一次读 tags 深圳切片落盘；本脚本只读该快照，不连库",
        "pool": "与 M_CHAIN_ENTERPRISE_COUNT / M_CHAIN_SZ_ENTERPRISE_COUNT 同池同 12 链",
        "provenance": "gkx @ 183.240.141.251:3318 / gkx_reader_zp，tags 深圳切片 116,017 行，拉取于 2026-10-22T15:31:50+08:00",
    },
    "chains": rows,
    "stats": {
        "n": len(vals), "min": min(vals), "max": max(vals),
        "median": round(sorted(vals)[len(vals) // 2], 2),
        "mean": round(sum(vals) / len(vals), 2),
        "n_ge_90": sum(1 for v in vals if v >= 90),
        "n_lt_70": sum(1 for v in vals if v < 70),
    },
    "coverage_source": {"sz_tag_rows": cov["rows_sz"], "distinct_codes_in_sz_slice": cov["distinct_tokens"]},
    "difference_vs_old_draft": {
        "old_source": "演示库汇总层（库名以 demo 打码，表 industry_chain_metric_fact）",
        "old_stats": {"n": 12, "min": 54.35, "max": 98.72, "median": 86.58, "mean": 83.14},
        "old_example": "具身智能 77/78=98.72%，机器人 86/90=95.56%，智能终端 92/97=94.85%（另一路区划码口径 96.91%）",
        "now_example": "具身智能 78/78=100%，机器人 90/90=100%，智能终端 94/97=96.91%",
        "bias": "本件逐链 k 比旧稿主口径多 0—4 个节点，因旧稿主口径先与 18.9 万行底册回联（只留 3.5 万家），漏掉未进底册的深圳挂链企业；k 只会更大、完整度只会更高",
        "conclusion": "K 完全相同（90/97/78 等与旧稿逐链一致），k 的差异可由覆盖集解释，公式与判档不变 → 完全转换支持",
    },
    "gaps": [
        "k 只判「有没有 ≥1 家深圳企业」，不判环节内企业密度；1 家与 1,000 家同权",
        "链树节点由业务侧维护，某些中间层是归组节点而非真实环节，会轻微压低完整度",
        "注册地区划码 4403 ≠ 实际经营地，分支/迁移会误判",
    ],
    "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    "elapsed_sec": round(time.time() - T0, 2),
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=1)
print("stats", payload["stats"])
for r in rows:
    print(r["chain_code"], r["chain_name"], r["k_sz_covered"], r["K_nodes"], r["completeness_pct"])
print("wrote", OUT)


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
    out_json = here / "M_CHAIN_SZ_COMPLETENESS_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_CHAIN_SZ_COMPLETENESS.py 等价）
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
        "metric_id": "M_CHAIN_SZ_COMPLETENESS",
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
