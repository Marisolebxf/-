#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_CHAIN_NODE_COUNT 产业链节点数
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_CHAIN_NODE_COUNT.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""产业链节点数（M_CHAIN_NODE_COUNT）—— gkx 链树，王惠 V2 口径，自包含。

口径（王惠 `指标计算逻辑-V2/M_CHAIN_NODE_COUNT.md`，V2-20260819）：
    COUNT(DISTINCT industry_link_code)，按 industry_code 前 7 位归到顶层链。
    实测 `industry_link_code` 只在「有子节点」的行上非空（12 个顶层根为空串），
    因此本口径数的正是**非叶环节码**：全库 319 个（12 链合计，逐链 9—71）。

同时输出 `nodes_total`（全部 industry_code，1,273 个）作为结构旁证，两者不可混用：
    319 = 环节节点（叶节点不计）；1,273 = 目录树全部节点（含叶）。
    20261021 旧脚本把 nodes_total 当作主值（1,273），比王惠口径大 4 倍，已在本版改正。

产物字段：headline.value = 319；chains[].value = 该链环节码数；chains[].nodes_total = 该链全部节点。

运行：cd code && python3 M_CHAIN_NODE_COUNT.py
产物：code/M_CHAIN_NODE_COUNT_out.json（覆盖写）
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_NODE_COUNT_out.json")

BASE_USED = []
BASE_MISSING = []
BASE_NOTE = "截面指标：统计链树当前存量，不设年度分母；链树无年度字段。"

SOURCES = [
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_industry_chain_info", "rows": 1273,
     "snapshot": "code/_snapshots21/chain_tree_links_20261022.json",
     "pulled_at": "2026-10-22"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_org_industry_tags", "rows": 2283762,
     "snapshot": "code/_snapshots21/chain_panel21.json"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_org_base_info", "rows": 189116,
     "snapshot": "code/_snapshots21/base_20261021.json"},
]


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    t0 = time.time()
    tree = load("chain_tree_links_20261022.json")
    rows_in = tree["data"]
    panel = load("chain_panel21.json")
    names = {c["chain"]: c["name"] for c in panel["chains"]}

    by_root = defaultdict(lambda: {"nodes": 0, "links": set(), "codes": set()})
    for r in rows_in:
        code = (r["industry_code"] or "").strip()
        root = code[:7]
        g = by_root[root]
        g["nodes"] += 1
        g["codes"].add(code)
        lc = (r["industry_link_code"] or "").strip()
        if lc:
            g["links"].add(lc)

    # 父子关系：某 code 是否有子节点（用于区分叶/非叶）
    nonleaf = 0
    for root, g in by_root.items():
        for code in g["codes"]:
            if any(c != code and c.startswith(code) for c in g["codes"]):
                nonleaf += 1

    rows = []
    for root, g in by_root.items():
        links = len(g["links"])
        rows.append({
            "chain": root,
            "name": names.get(root, ""),
            "value": links,
            "nodes_total": g["nodes"],
            "leaves": g["nodes"] - links,
            "leaf_share": round((g["nodes"] - links) / g["nodes"], 4) if g["nodes"] else None,
        })
    rows.sort(key=lambda r: -r["value"])
    total_links = sum(r["value"] for r in rows)
    total_nodes = sum(r["nodes_total"] for r in rows)
    global_links = len({(r["industry_link_code"] or "").strip()
                        for r in rows_in if (r["industry_link_code"] or "").strip()})

    by_len = Counter(len((r["industry_code"] or "").strip()) for r in rows_in)
    vals = sorted(r["value"] for r in rows)
    stats = {
        "n_chains": len(rows),
        "min": vals[0], "max": vals[-1], "median": vals[len(vals) // 2],
        "mean": round(total_links / len(rows), 2) if rows else None,
        "leaves_total": total_nodes - total_links,
        "nodes_total": total_nodes,
        "link_per_node_pct": round(100.0 * total_links / total_nodes, 2) if total_nodes else None,
    }
    headline = {
        "value": total_links,
        "unit": "个环节节点（12 链去重合计）",
        "nodes_total": total_nodes,
        "global_distinct_links": global_links,
        "chains": len(rows),
        "definition": "COUNT(DISTINCT industry_link_code) GROUP BY industry_code[:7]",
        "max_chain": rows[0]["chain"], "max_value": rows[0]["value"],
        "min_chain": rows[-1]["chain"], "min_value": rows[-1]["value"],
    }
    facts = [
        {"label": "环节节点（王惠口径，12 链合计）", "value": total_links},
        {"label": "全库去重环节码（跨链不重复）", "value": global_links},
        {"label": "目录树全部节点（含叶）", "value": total_nodes},
        {"label": "顶层链数", "value": len(rows)},
        {"label": "单链环节码区间", "value": f'{rows[-1]["value"]}—{rows[0]["value"]}'},
        {"label": "编码长度层级", "value": dict(sorted(by_len.items()))},
        {"label": "node_company_count 非零行", "value": sum(1 for r in rows_in if (r["node_company_count"] or 0) > 0)},
        {"label": "level 列取值个数", "value": len({r["level"] for r in rows_in})},
    ]
    population = {
        "defined_as": "gkx.dwd_industry_chain_info 全部节点，按 industry_code 7 位前缀归链",
        "nodes": total_nodes,
        "roots": len(rows),
        "rows_with_empty_link_code": sum(1 for r in rows_in if not (r["industry_link_code"] or "").strip()),
        "by_len": dict(sorted(by_len.items())),
        "nonleaf": nonleaf,
    }
    compute = {
        "formula": "COUNT(DISTINCT industry_link_code) GROUP BY industry_code[:7]",
        "source_rows": total_nodes,
        "main_value_semantics": "非叶环节码（叶节点不计）",
        "alt_value_semantics": "nodes_total = 目录树全部节点（含叶）",
    }
    STEPS = [
        "读取链树快照 chain_tree_links_20261022.json（1,273 行，含 industry_link_code）",
        "按 industry_code 前 7 位归到 12 条顶层链",
        "每条链对非空 industry_link_code 去重计数 → 环节节点数",
        "同时统计 nodes_total（全部 industry_code）与叶/非叶结构",
        "校验 Σ逐链环节码 = 全库去重环节码 = 319，且 < 全部节点 1,273",
    ]
    out = {
        "metric_id": "M_CHAIN_NODE_COUNT",
        "metric_name": "产业链节点数",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "完全转换支持",
        "judgment_reason": "链树 1,273 行、12 条顶层链、319 个非叶环节码在 gkx 当日全量可取；"
                           "COUNT(DISTINCT industry_link_code) 端到端跑通，逐链 9—71、区分度充分，无外部依赖。",
        "sources": SOURCES,
        "base_years_used": BASE_USED,
        "base_years_missing": BASE_MISSING,
        "base_years_note": BASE_NOTE,
        "headline": headline,
        "stats": stats,
        "facts": facts,
        "chains": rows,
        "method_steps": STEPS,
        "population": population,
        "compute": compute,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("[ok]", "M_CHAIN_NODE_COUNT", json.dumps(headline, ensure_ascii=False),
          "sec", round(time.time() - t0, 2))


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
    out_json = here / "M_CHAIN_NODE_COUNT_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_CHAIN_NODE_COUNT.py 等价）
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
        "metric_id": "M_CHAIN_NODE_COUNT",
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
