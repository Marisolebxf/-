#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_SVC_PT_SZ_REGION_ORG 深圳机构区域分布
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统
# 【差异分级】D5 表述级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_SVC_PT_SZ_REGION_ORG.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""深圳机构区域分布（M_SVC_PT_SZ_REGION_ORG）—— gkx 口径，自包含。

口径（calc-logic 0.2.0：区级源＝底册 area，按行政区名分组计数，未分配常显禁剔除）：
    切片 = 服务机构池 ∩ city='深圳市'（与 M_SVC_PT_SZ_TOTAL 同池同数）
    区轴 = 底册 area（已规范到「区」级全称）
    计数 = COUNT(DISTINCT org_id) GROUP BY area
    对账 = Σ 已分配区 + 未分配 = 切片值

数据源（只读快照，零 SQL）：
    code/_snapshots21/svc21_facts_20261022.json   pool（city）+ base_fields（area）

产出：code/M_SVC_PT_SZ_REGION_ORG_out.json
运行：cd code && python3 M_SVC_PT_SZ_REGION_ORG.py
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
OUT = os.path.join(HERE, "M_SVC_PT_SZ_REGION_ORG_out.json")

# 深圳市 9 个行政区（含新区/功能区归并的常显目录；未分配单列）
SZ_DISTRICTS = ["南山区", "福田区", "罗湖区", "宝安区", "龙岗区",
                "龙华区", "坪山区", "光明区", "盐田区", "大鹏新区"]


def main():
    t0 = time.time()
    fact = json.load(open(FACTS, encoding="utf-8"))
    pool, bf = fact["pool"], fact["base_fields"]
    sz = [o for o, v in pool.items() if v.get("city") == "深圳市"]
    n = len(sz)

    area = Counter((bf.get(o) or {}).get("area") or "" for o in sz)
    rows = []
    for d in SZ_DISTRICTS:
        c = area.get(d, 0)
        rows.append({"area": d, "org_count": c, "share_of_sz": round(c / n, 6)})
    unassigned = area.get("", 0)
    rows.append({"area": "（未分配）", "org_count": unassigned,
                 "share_of_sz": round(unassigned / n, 6)})
    other = {k: c for k, c in area.items() if k and k not in SZ_DISTRICTS}
    area_sum = sum(r["org_count"] for r in rows) + sum(other.values())

    out = {
        "metric_id": "M_SVC_PT_SZ_REGION_ORG",
        "metric_name": "深圳机构区域分布",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "完全转换支持",
        "judgment_reason": (
            "深圳切片的区级分布可现转且闭合：切片 %d 家，9 个行政区＋未分配 %d＋区外/异名 %d "
            "＝%d（与 M_SVC_PT_SZ_TOTAL 同池同数）；区字段非空率 %.2f%%，未分配单列不剔除"
            % (n, unassigned, sum(other.values()), area_sum,
               100.0 * (n - unassigned) / n)),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_base_info(area, city) 经 pool 驱动",
             "rows": fact["population"]["base_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_org_product_info（池人口）",
             "rows": fact["population"]["product_info_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面指标：区级分布是当前时点存量的空间切分，不含年度分母；"
                            "切片总量与成立年序列由 M_SVC_PT_SZ_TOTAL 承担。"),
        "population": {"shenzhen_orgs": n, "pool_orgs": len(pool),
                       "share_of_pool": round(n / len(pool), 6)},
        "district_rows": rows,
        "district_total": area_sum,
        "sum_equals_sz_total": area_sum == n,
        "structure_tiers": {
            "top_three": sum(r["org_count"] for r in rows if r["area"] in ("南山区", "宝安区", "龙岗区")),
            "primary_two": sum(r["org_count"] for r in rows if r["area"] in ("南山区", "宝安区")),
            "mid_three": sum(r["org_count"] for r in rows if r["area"] in ("龙岗区", "福田区", "龙华区")),
            "outer_five": sum(r["org_count"] for r in rows if r["area"] in ("光明区", "罗湖区", "坪山区", "盐田区", "大鹏新区")),
            "futian_luohu": sum(r["org_count"] for r in rows if r["area"] in ("福田区", "罗湖区")),
        },
        "coverage": {
            "area_nonnull": n - unassigned,
            "area_nonnull_rate": round((n - unassigned) / n, 6),
            "districts_listed": len(SZ_DISTRICTS),
            "districts_with_value": sum(1 for r in rows[:-1] if r["org_count"] > 0),
            "other_labels": [[k, c] for k, c in sorted(other.items(), key=lambda x: -x[1])],
        },
        "difference_vs_old_draft": {
            "population": "旧稿切片 14,033（演示库圈定池）→ 本件切片 %d（gkx 经营范围池）" % n,
            "district": ("旧稿 南山 3,655 / 宝安 2,850 / 龙岗 2,039 / 福田 1,829 / 龙华 1,795 / "
                         "光明 798 / 罗湖 553 / 坪山 388 / 盐田 121 / 未分配 5 → 本件见 district_rows"),
            "shape": "区级排序方向一致（南山、宝安、龙岗居前），绝对数随池放大；未分配从 5 升到 %d"
                     % unassigned,
        },
        "compute": {"status": "ok", "elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("sz=%d rows=%s sum=%d ok=%s other=%s"
          % (n, [(r["area"], r["org_count"]) for r in rows], area_sum,
             area_sum == n, other))
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
    out_json = here / "M_SVC_PT_SZ_REGION_ORG_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_SVC_PT_SZ_REGION_ORG.py 等价）
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
        "metric_id": "M_SVC_PT_SZ_REGION_ORG",
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
