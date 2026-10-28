#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_SVC_PT_CHAIN_NODE_ORG 产业链节点服务机构数
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_SVC_PT_CHAIN_NODE_ORG.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""产业链节点服务机构数（M_SVC_PT_CHAIN_NODE_ORG）—— gkx 口径，自包含。

钉版语义（calc-logic 0.2.0）：产业分面 × 环节分面全组合常备、格内 COUNT(DISTINCT org_id)、
空格显「暂无供给机构」不伪造。换源后的两张分面表：

    产业分面 = gkx.dwd_org_industry_tags.industry_name（经 company_name 对齐到池）
               12 个产业名（软件与信息服务/智能终端/人工智能/具身智能/机器人/集成电路/
               数字创意/传感器/合成生物/智能网联汽车/生物医药/低空经济）
    环节分面 = CT-SVC-PT-01 六站（research/ip/transfer/pilot/testing/market），
               由 pool[*].stages（经营范围词表命中）给出

三个必须披露的口径事实：
  1. 产业轴换词典：旧稿 15 集群目录在 gkx 无对应表；本件改用 tags 的产业名词表，且覆盖率 40.58%。
  2. 环节轴是词表代理：正式「机构×产业×环节服务记录」成员表（SVC-P0-3）在 gkx 与 live 均不存在。
  3. 两轴交叉是「代理×代理」：格值只能读作「同时命中产业词与环节词的机构数」，不是服务事实。

格值口径：cell(i,s) = |{org : i ∈ industries(org) 且 s ∈ stages(org)}|，
          边际 industry 与 stage 均另给，供与 M_SVC_PT_SZ_FIELD_DIST / 
          M_SVC_CHAIN_SEGMENT_ORG_COUNT 对账。

数据源（只读快照，零 SQL）：
    code/_snapshots21/svc21_facts_20261022.json    pool（stages）
    code/_snapshots21/svc21_pt_axis_20261022.json  pool_tags（industries）+ meta

产出：code/M_SVC_PT_CHAIN_NODE_ORG_out.json
运行：cd code && python3 M_SVC_PT_CHAIN_NODE_ORG.py
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
AXIS = os.path.join(SNAP, "svc21_pt_axis_20261022.json")
OUT = os.path.join(HERE, "M_SVC_PT_CHAIN_NODE_ORG_out.json")

STAGES = [("stage-research", "研发与科研合作"), ("stage-ip", "知识产权与标准"),
          ("stage-transfer", "技术转移与孵化"), ("stage-pilot", "中试熟化"),
          ("stage-testing", "检测认证"), ("stage-market", "市场化服务")]


def main():
    t0 = time.time()
    fact = json.load(open(FACTS, encoding="utf-8"))
    ax = json.load(open(AXIS, encoding="utf-8"))
    pool, tags = fact["pool"], ax["pool_tags"]
    meta = ax["pool_tags_meta"]
    n = len(pool)

    inds = [a for a, _c in meta["industry_dist"] if a]
    stage_ids = [s for s, _ in STAGES]

    # ---------------- 交叉格
    cells = {i: {s: 0 for s in stage_ids} for i in inds}
    ind_margin = Counter()
    stage_margin = Counter()
    both = 0
    tagged = 0
    for o, v in pool.items():
        st = [s for s in (v.get("stages") or []) if s in stage_ids]
        ind = tags.get(o) or []
        if ind:
            tagged += 1
        if ind and st:
            both += 1
        for i in ind:
            if i not in cells:
                continue
            ind_margin[i] += 1
            for s in st:
                cells[i][s] += 1
        for s in st:
            stage_margin[s] += 1

    cell_rows = []
    for i in inds:
        row = {"industry": i, "industry_margin": ind_margin.get(i, 0)}
        for s in stage_ids:
            row[s] = cells[i][s]
        row["row_sum"] = sum(cells[i][s] for s in stage_ids)
        cell_rows.append(row)

    stage_rows = [{"stage_id": s, "stage_name": nm, "org_count": stage_margin.get(s, 0),
                   "count_source": "keyword_proxy"} for s, nm in STAGES]

    nonzero = sum(1 for i in inds for s in stage_ids if cells[i][s] > 0)
    grid = len(inds) * len(stage_ids)
    tops = sorted(((cells[i][s], i, s) for i in inds for s in stage_ids), reverse=True)[:10]

    out = {
        "metric_id": "M_SVC_PT_CHAIN_NODE_ORG",
        "metric_name": "产业链节点服务机构数",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": (
            "产业×环节交叉格可出数（%d 个产业 × 6 环节 = %d 格，其中 %d 格非零），"
            "但两张分面都是代理：环节轴的正式成员表（机构×产业×环节服务记录，SVC-P0-3）"
            "在 gkx 与 live 均不存在，产业轴覆盖率只有 40.58%% 且换了词典 → 部分支持"
            % (len(inds), grid, nonzero)),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_industry_tags(industry_name)",
             "rows": meta["rows_scanned"],
             "snapshot": "code/_snapshots21/svc21_pt_axis_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_org_product_info(main_activities 六环节词表)",
             "rows": fact["population"]["product_info_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面宽表：产业×环节交叉计数是当前存量的预统计，不含年度分母；"
                            "tags 表与经营范围词表都没有可用的服务记录年份，本件不做年度序列"
                            "（补 0 会把未采集年当零供给）。"),
        "population": {
            "pool_orgs": n,
            "industry_tagged": tagged,
            "industry_tag_coverage": round(tagged / n, 6),
            "stage_hit": sum(1 for v in pool.values() if v.get("stages")),
            "both_axes_hit": both,
            "both_axes_share": round(both / n, 6),
        },
        "axes": {
            "industry_axis": {
                "dictionary": "gkx.dwd_org_industry_tags.industry_name（20+8 产业集群词表）",
                "values": inds,
                "values_total": len(inds),
                "coverage_of_pool": meta["coverage_of_pool"],
                "multi_value": "经理解析为数组，一家可命中多产业（tags 行本身也是数组字面量）",
            },
            "stage_axis": {
                "dictionary": "CT-SVC-PT-01 六站（钉版）",
                "values": stage_ids,
                "count_source": "keyword_proxy（main_activities 词表）",
                "coverage_of_pool": round(sum(1 for v in pool.values() if v.get("stages")) / n, 6),
            },
        },
        "cell_rows": cell_rows,
        "grid": {"industries": len(inds), "stages": len(stage_ids), "cells": grid,
                 "nonzero": nonzero, "zero": grid - nonzero,
                 "margin_sum": sum(stage_margin.values())},
        "stage_rows": stage_rows,
        "top_cells": [{"industry": i, "stage_id": s, "org_count": c} for c, i, s in tops],
        "stage_margin_vs_segment_metric": {
            "note": ("stage_rows 的边际应与 M_SVC_CHAIN_SEGMENT_ORG_COUNT 的六环节计数一致"
                     "（同一份 pool/stages 快照）；若不一致，说明该件换了池或换了词表。"),
            "rows": [[r["stage_id"], r["org_count"]] for r in stage_rows],
        },
        "missing_structure": {
            "needed": "机构×产业×环节服务记录（成员事实表，SVC-P0-3）",
            "existing": "gkx/live 均无该表；两轴只能用词表代理",
            "impact": ("格值是「同时命中两个词表」的机构数，不是「在该产业该环节提供服务」的事实；"
                       "0 格既可能是真空白，也可能是词根未覆盖，页面须标注「代理口径」"),
        },
        "difference_vs_old_draft": {
            "population": "旧稿 43,296（演示库圈定池）→ 本件 44,153（gkx 经营范围实体）",
            "industry_axis": "旧稿 15 集群（CL-SEI/CL-FUT，五跳链 100% 上链）→ 本件 12 个产业名（tags 覆盖率 40.58%）",
            "stage_counts": "旧稿词表代理 {0,151,3,2,412,8} → 本件 %s"
                            % {r["stage_id"]: r["org_count"] for r in stage_rows},
            "reason": ("旧稿的窄词表只认「委托研发/联合攻关/大设施/算力服务」四词，gkx 实测这四词零命中；"
                       "本件扩了显名服务词，研发与转移环节因此从个位数放大到万级，"
                       "这不是数据变多，是词表口径变宽——两版数字不可直接比较"),
        },
        "compute": {"status": "ok", "elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("inds=%d grid=%d nonzero=%d both=%d tagged=%d"
          % (len(inds), grid, nonzero, both, tagged))
    print("stages", {r["stage_id"]: r["org_count"] for r in stage_rows})
    print("top cells", [(t["industry"], t["stage_id"], t["org_count"]) for t in out["top_cells"][:5]])
    print("->", OUT)


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
    out_json = here / "M_SVC_PT_CHAIN_NODE_ORG_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_SVC_PT_CHAIN_NODE_ORG.py 等价）
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
        "metric_id": "M_SVC_PT_CHAIN_NODE_ORG",
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
