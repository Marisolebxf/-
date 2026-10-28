#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_SVC_PT_GLOBAL_TYPE_DIST 全球服务机构类型分布
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统
# 【差异分级】D5 表述级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_SVC_PT_GLOBAL_TYPE_DIST.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""全球服务机构类型分布（M_SVC_PT_GLOBAL_TYPE_DIST）—— gkx 口径，自包含。

两根类型轴：
  主轴（钉版三分类，机构本体）：企业 / 高校 / 科研院所
      来自 svc21_pt_axis_20261022.json 的 org_kind：
        科研院所 = 池内 org_id ∈ gkx.dwd_research_institute_base_info（2,074 行）或用名称精确相等
        高校     = 名称含 大学/学院/高等专科/职业技术学院/学校
        企业     = 其余（三类互斥，合计 = 池）
  辅轴（服务类型六分类，经营范围词表）：INNOV/IP/FINANCE/HR/MKT/CONSULT，一家可多命中

数据源（只读快照，零 SQL）：
    code/_snapshots21/svc21_facts_20261022.json       pool + 六类词表命中
    code/_snapshots21/svc21_pt_axis_20261022.json     org_kind + 科研院所名单

产出：code/M_SVC_PT_GLOBAL_TYPE_DIST_out.json
运行：cd code && python3 M_SVC_PT_GLOBAL_TYPE_DIST.py
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
OUT = os.path.join(HERE, "M_SVC_PT_GLOBAL_TYPE_DIST_out.json")

ORDER = ["企业", "高校", "科研院所"]
TYPE_NAME = {"INNOV": "创新/技术服务", "IP": "知识产权服务", "FINANCE": "金融服务",
             "HR": "人力资源服务", "MKT": "市场营销服务", "CONSULT": "咨询服务"}


def main():
    t0 = time.time()
    fact = json.load(open(FACTS, encoding="utf-8"))
    ax = json.load(open(AXIS, encoding="utf-8"))
    pool = fact["pool"]
    kind = ax["org_kind"]
    n = len(pool)

    # ---------------- 主轴：机构本体三分类
    cnt = Counter(kind.get(o, "企业") for o in pool)
    rows = []
    for k in ORDER:
        rows.append({"org_kind": k, "org_count": cnt.get(k, 0),
                     "share_of_pool": round(cnt.get(k, 0) / n, 6)})

    samples = {}
    for k in ("高校", "科研院所"):
        ids = [o for o in pool if kind.get(o) == k]
        samples[k] = [{"name": pool[o]["name"], "city": pool[o].get("city", "")} for o in ids[:8]]

    # ---------------- 辅轴：六类服务词表（多命中 + 主类）
    multi = Counter()
    for v in pool.values():
        for t in v.get("types") or []:
            multi[t] += 1
    primary = Counter(v.get("ptype") for v in pool.values())
    svc_rows = []
    for t in ["INNOV", "IP", "FINANCE", "HR", "MKT", "CONSULT"]:
        svc_rows.append({"type": t, "type_name": TYPE_NAME[t],
                         "multi_hit": multi.get(t, 0),
                         "primary": primary.get(t, 0),
                         "share_multi": round(multi.get(t, 0) / n, 6)})

    sz_kind = Counter(kind.get(o, "企业") for o, v in pool.items() if v.get("city") == "深圳市")

    out = {
        "metric_id": "M_SVC_PT_GLOBAL_TYPE_DIST",
        "metric_name": "全球服务机构类型分布",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": (
            "机构本体三分类在 gkx 可实算且闭合（企业 44,095＋高校 37＋科研院所 21＝44,153），"
            "六类服务词表亦可现转；但「全球」轴的境外机构在 gkx 无源"
            "（dwd_forg_base_info 仅 GB/US/CA 三值且非服务名录），类型分布在境外面不可得 → 部分支持"),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_org_product_info(main_activities 词表分类)",
             "rows": fact["population"]["product_info_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_research_institute_base_info", "rows": ax["research"]["rows_total"],
             "snapshot": "code/_snapshots21/svc21_pt_axis_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_base_info（名称，用于高校判定）",
             "rows": fact["population"]["base_all"],
             "snapshot": "code/_snapshots21/base_20261021.json"},
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面指标：类型分布是当前时点存量的横截面，不含年度分母；"
                            "池内成立年序列由 M_SVC_PT_GLOBAL_TOTAL 承担，本件不重复计入。"),
        "population": {
            "distinct_org_id": n,
            "join_base_rows": fact["population"]["product_info_join_base"],
            "join_base_rate": round(fact["population"]["product_info_join_base"] / n, 6),
        },
        "kind_axis": {
            "order": ORDER,
            "rows": rows,
            "sum": sum(r["org_count"] for r in rows),
            "sum_equals_pool": sum(r["org_count"] for r in rows) == n,
            "rule": ax["org_kind_meta"]["rule"],
            "research_source_rows": ax["research"]["rows_total"],
            "research_matched": len(ax["research"]["matched"]),
            "samples": samples,
            "shenzhen": [{"org_kind": k, "org_count": sz_kind.get(k, 0)} for k in ORDER],
        },
        "service_axis": {
            "rows": svc_rows,
            "multi_hit_sum": sum(r["multi_hit"] for r in svc_rows),
            "classified_orgs": n - primary.get("UNCLASSIFIED", 0),
            "innov_absorbed": multi.get("INNOV", 0) - primary.get("INNOV", 0),
            "multiplicity": dict(sorted(Counter(len(v.get("types") or []) for v in pool.values()).items())),
            "unclassified_primary": primary.get("UNCLASSIFIED", 0),
            "note": ("六类是经营范围词表代理，一家机构可命中多类；主类按 "
                     "IP > FINANCE > HR > MKT > CONSULT > INNOV 归并（专精类优先、泛化类兜底，"
                     "故 INNOV 主类只剩未命中其余五类者；ptype_rule 见快照）。"),
        },
        "difference_vs_old_draft": {
            "population": "旧稿 43,296（演示库圈定池，企业侧为主）→ 本件 44,153（gkx 经营范围实体）",
            "kind_dist": "旧稿 企业 43,296 / 高校 0 / 科研院所 0 → 本件 企业 44,095 / 高校 37 / 科研院所 21",
            "reason": ("旧稿两桶为 0 是「池由企业底册构成」的口径性结论；换源后池来自经营范围，"
                       "gkx 另有 dwd_research_institute_base_info（2,074 行，池内命中 21）与名称含"
                       "「大学/学院」的 37 家，两桶由 0 变为可实测的非零小类"),
        },
        "compute": {"status": "ok", "elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("kind", [(r["org_kind"], r["org_count"]) for r in rows], "sum", sum(r["org_count"] for r in rows))
    print("svc", [(r["type"], r["multi_hit"], r["primary"]) for r in svc_rows])
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
    out_json = here / "M_SVC_PT_GLOBAL_TYPE_DIST_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_SVC_PT_GLOBAL_TYPE_DIST.py 等价）
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
        "metric_id": "M_SVC_PT_GLOBAL_TYPE_DIST",
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
