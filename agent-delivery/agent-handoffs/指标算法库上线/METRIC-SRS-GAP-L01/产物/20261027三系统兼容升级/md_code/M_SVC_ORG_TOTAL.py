#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_SVC_ORG_TOTAL 入库服务机构总数
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D5 表述级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_SVC_ORG_TOTAL.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""入库服务机构总数（M_SVC_ORG_TOTAL）—— gkx 口径，自包含。

数据源（只读落盘快照，零 SQL、零 demo）：
    code/_snapshots21/svc21_facts_20261022.json
        source: gkx @183.240.141.251:3318（gkx_reader_zp，只读）
        pool  = gkx.dwd_org_org_product_info（45,011 行 / 44,153 个 org_id）
    code/_snapshots21/base_20261021.json
        gkx.dwd_org_base_info 189,116 行（org_id / 信用码 / 名称 / 省 / 市 / 成立年）

口径：服务机构池 = 有经营范围文本的机构，按 org_id 去重计数。
      不数卡面、不数事实面、不数 ODS 全量（底册 189,116 是上游原料）。
产出：code/M_SVC_ORG_TOTAL_out.json（覆盖写）
运行：cd code && python3 M_SVC_ORG_TOTAL.py
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
BASE = os.path.join(SNAP, "base_20261021.json")
OUT = os.path.join(HERE, "M_SVC_ORG_TOTAL_out.json")


def main() -> None:
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    base = json.load(open(BASE, encoding="utf-8"))
    pool = f["pool"]
    pop = f["population"]
    bmap = {r[0]: r for r in base}

    ids = list(pool.keys())
    n_pool = len(ids)
    joined = [o for o in ids if o in bmap]
    unknown = n_pool - len(joined)

    city = Counter(v["city"] or "（空）" for v in pool.values())
    prov = Counter(v["prov"] or "（空）" for v in pool.values())
    size = Counter((f["base_fields"].get(o) or {}).get("size") or "未知" for o in ids)
    ind = Counter((f["base_fields"].get(o) or {}).get("ind") or "（空）" for o in ids)

    sz = sum(1 for o in ids if pool[o]["city"] == "深圳市")
    outside = n_pool - sz

    out = {
        "metric_id": "M_SVC_ORG_TOTAL",
        "metric_name": "入库服务机构总数",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "完全转换支持",
        "judgment_reason": (
            "gkx 无 svc_org_circle，但 dwd_org_org_product_info 有 45,011 行经营范围文本、"
            "按 org_id 去重得 44,153 家；与底册 189,116 行回联命中 44,132 家（99.95%）。"
            "人口结构+当前数据量均足，现在即可经转换得到唯一键计数"),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_org_product_info", "rows": pop["product_info_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_base_info", "rows": pop["base_all"],
             "snapshot": "code/_snapshots21/base_20261021.json"},
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "截面指标：总数是「当前在池」的唯一键计数，不含年度分母。"
            "成立年分布仅作披露（见 M_SVC_NEW_CNT），不参与本件计数。"),
        "population": {
            "defined_as": "gkx.dwd_org_org_product_info 中有 main_activities 文本的机构，按 org_id 去重",
            "product_info_rows": pop["product_info_all"],
            "distinct_org_id": n_pool,
            "service_text_rows": pop["service_any_hit"],
            "join_base_rows": len(joined),
            "join_base_rate": round(len(joined) / n_pool, 6),
            "not_in_base": unknown,
            "shenzhen": sz,
            "outside_shenzhen": outside,
            "shenzhen_share": round(sz / n_pool, 6),
        },
        "city_dist": [[c, n] for c, n in city.most_common(10)],
        "prov_dist": [[p, n] for p, n in prov.most_common(10)],
        "size_dist": [[k, v] for k, v in size.most_common()],
        "industry_top": [[k, v] for k, v in ind.most_common(10)],
        "probe": {
            "text_len_median": sorted(v["len"] for v in pool.values())[n_pool // 2],
            "text_len_p90": sorted(v["len"] for v in pool.values())[int(n_pool * 0.9)],
            "text_len_max": max(v["len"] for v in pool.values()),
            "base_rows": len(base),
            "base_distinct_name": len({r[2] for r in base}),
            "name_dup_rows": len(base) - len({r[2] for r in base}),
            "rows_per_org": round(pop["product_info_all"] / n_pool, 3),
        },
        "audit_chain": {
            "downstream_population_anchor": n_pool,
            "stage_multiplicity_sum": sum(len(v["stages"]) for v in pool.values()),
            "stage_union_orgs": sum(1 for v in pool.values() if v["stages"]),
            "note": ("同域各件的人口分母一律取 44,153；六环节多命中合计 60,673、"
                     "环节去重 34,578 是环节维的两个派生量，不是另一个机构池"),
        },
        "difference_vs_old_draft": {
            "population": "旧稿 43,296（演示库 svc_org_circle）→ 本件 44,153（gkx 经营范围机构）",
            "shenzhen": "旧稿 14,033 → 本件 25,597",
            "reason": ("换源后人口由「人工圈定名单」变为「有经营范围文本的 gkx 机构」，"
                       "池子更大且深圳占比更高；两版分母不可直接比较绝对数"),
        },
        "gaps": {
            "curated_list": "gkx 无人工认定的服务机构名录；本件人口是经营范围代理，含制造企业与高校",
            "exit_side": "无注销/吊销事件流，无法给出净新增",
        },
        "compute": {"status": "ok", "elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("total=%d join_base=%d sz=%d -> %s" % (n_pool, len(joined), sz, OUT))


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
    out_json = here / "M_SVC_ORG_TOTAL_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_SVC_ORG_TOTAL.py 等价）
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
        "metric_id": "M_SVC_ORG_TOTAL",
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
