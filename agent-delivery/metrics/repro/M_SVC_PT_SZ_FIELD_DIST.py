#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_SVC_PT_SZ_FIELD_DIST 深圳机构产业领域分布
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统
# 【差异分级】D5 表述级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_SVC_PT_SZ_FIELD_DIST.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""深圳机构产业领域分布（M_SVC_PT_SZ_FIELD_DIST）—— gkx 口径，自包含。

口径（calc-logic 0.2.0：领域轴预设目录全集常显、未分配常显禁剔除；本件换源后改轴）：
    切片   = 服务机构池 ∩ city='深圳市'
    领域轴 = gkx.dwd_org_industry_tags.industry_name（经 company_name 精确对齐到池）
             值域是「深圳 20+8 产业集群」口径的 12 个产业名：
             软件与信息服务 / 智能终端 / 人工智能 / 具身智能 / 机器人 / 集成电路 /
             数字创意 / 传感器 / 合成生物 / 智能网联汽车 / 生物医药 / 低空经济
    计数   = COUNT(DISTINCT org_id) GROUP BY 产业名（一家可命中多产业，同时给多命中与去重两个分母）
    未分配 = 切片内未在 tags 表对齐到的机构，单列常显

与旧稿的实质差异：旧稿的领域轴是项目内 15 集群目录（CL-SEI-01～10 + CL-FUT-01～05），
gkx 没有这套目录表，但有另一套产业词表（20+8）。本件**不把两套轴互相折算**，
而是如实换轴并披露：轴名不同、粒度不同、覆盖只有 40.58%，因此判档不抬。

数据源（只读快照，零 SQL）：
    code/_snapshots21/svc21_facts_20261022.json       pool（city）
    code/_snapshots21/svc21_pt_axis_20261022.json     pool_tags + pool_tags_meta

产出：code/M_SVC_PT_SZ_FIELD_DIST_out.json
运行：cd code && python3 M_SVC_PT_SZ_FIELD_DIST.py
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
OUT = os.path.join(HERE, "M_SVC_PT_SZ_FIELD_DIST_out.json")


def main():
    t0 = time.time()
    fact = json.load(open(FACTS, encoding="utf-8"))
    ax = json.load(open(AXIS, encoding="utf-8"))
    pool, bf = fact["pool"], fact["base_fields"]
    tags = ax["pool_tags"]
    meta = ax["pool_tags_meta"]

    sz = [o for o, v in pool.items() if v.get("city") == "深圳市"]
    n = len(sz)
    matched = [o for o in sz if tags.get(o)]
    cnt = Counter()
    multi = Counter()
    for o in matched:
        arr = tags.get(o) or []
        multi[len(arr)] += 1
        for a in arr:
            cnt[a] += 1

    rows = []
    for name, c in cnt.most_common():
        rows.append({"field": name, "org_count": c, "share_of_sz": round(c / n, 6),
                     "share_of_matched": round(c / len(matched), 6) if matched else None})
    unassigned = n - len(matched)

    out = {
        "metric_id": "M_SVC_PT_SZ_FIELD_DIST",
        "metric_name": "深圳机构产业领域分布",
        "support_judgment": "部分支持",
        "judgment_reason": (
            "深圳切片的产业领域分布可出数（%d/%d 家对齐到产业词表，12 个产业名、"
            "多命中 %d 家次），但领域轴换了一套字典（旧稿 15 集群目录在 gkx 无表，"
            "改用 tags 的「20+8 产业集群」词表），且覆盖率只有 %.2f%%、"
            "未对齐的 %d 家只能单列 → 维度不完整 → 部分支持"
            % (len(matched), n, sum(cnt.values()), 100.0 * len(matched) / n, unassigned)),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_industry_tags(company_name, industry_name)",
             "rows": meta["rows_scanned"],
             "snapshot": "code/_snapshots21/svc21_pt_axis_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_org_product_info（池人口）+ dwd_org_base_info(city)",
             "rows": fact["population"]["product_info_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面指标：产业领域分布是当前存量的横截面切分，不含年度分母；"
                            "tags 表无年份列，本件刻意不做年度序列（补 0 会把未采集年当零供给）。"),
        "population": {
            "pool_orgs": len(pool),
            "shenzhen_orgs": n,
            "tag_matched": len(matched),
            "tag_unassigned": unassigned,
            "tag_coverage": round(len(matched) / n, 6),
            "pool_tagged": meta["rows_matched"],
            "pool_tag_coverage": meta["coverage_of_pool"],
            "rows_scanned": meta["rows_scanned"],
        },
        "field_rows": rows,
        "fields_total": len(rows),
        "multi_hit_org_hits": sum(cnt.values()),
        "multiplicity": {str(k): v for k, v in sorted(multi.items())},
        "axis_substitution": {
            "old_axis": "项目内 15 集群目录（CL-SEI-01～10 + CL-FUT-01～05，POLICY_VERSION sz-10+5-2026）",
            "new_axis": "gkx.dwd_org_industry_tags.industry_name 的「20+8 产业集群」词表（12 个有值产业）",
            "mapping": None,
            "why_no_mapping": ("两套轴无权威对照表：旧轴是项目自建集群码，新轴是产业名文本；"
                               "强行按名称相似映射会把「人工智能」并进「新一代信息技术」这类"
                               "一对多关系做成一对一，产生不可复核的口径损失。故本件只换轴、不折算。"),
            "impact": "同一切片在两个轴下的分档不可直接比大小，只能比「集中度」这类结构量",
        },
        "difference_vs_old_draft": {
            "population": "旧稿输出人口为全池 43,296（未切深圳）→ 本件严格切深圳 %d 家" % n,
            "axis": "旧稿 15 集群（10 个有命中，CL-SEI-01/CL-FUT-02 各 43,296 为字典性全量默认映射）→ 本件 12 个产业名、最大 8,242（软件与信息服务）",
            "unassigned": "旧稿未分配桶为 −44,916（未归并导致）→ 本件未分配 %d（覆盖率 %.2f%%）"
                          % (unassigned, 100.0 * len(matched) / n),
        },
        "compute": {"status": "ok", "elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("sz=%d matched=%d (%.2f%%) unassigned=%d fields=%d"
          % (n, len(matched), 100.0 * len(matched) / n, unassigned, len(rows)))
    print("top", [(r["field"], r["org_count"]) for r in rows[:5]])
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
    out_json = here / "M_SVC_PT_SZ_FIELD_DIST_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_SVC_PT_SZ_FIELD_DIST.py 等价）
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
        "metric_id": "M_SVC_PT_SZ_FIELD_DIST",
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
