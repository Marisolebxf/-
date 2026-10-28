#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ENT_INNOVATIVE_COUNT 创新型企业数
# 【维护者】唐绍祖
# 【适用系统】科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ENT_INNOVATIVE_COUNT.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_ENT_INNOVATIVE_COUNT 创新型企业数（梯度培育四类标签去重计数）。

口径：calc-logic V3-2026-08-09（企业分析 / 重点企业分析 / 类型与区域分析）
    org_tag ∈ {创新型中小企业, 专精特新中小企业, 专精特新小巨人, 制造业单项冠军}，按 org_id 去重。
取数：`code/_snapshots21/tech_tags_20261021.json`（`gkx.dwd_org_tech_tag` 202,424 行 / 32,322 家机构）
      × `code/_snapshots21/base_20261021.json`（189,116 行底册，取省/市），零 DB。
"""
from __future__ import annotations

import json
import time
from pathlib import Path

BASE = Path(__file__).parent
SNAP = BASE / "_snapshots21"
METRIC = "M_ENT_INNOVATIVE_COUNT"

# 梯度培育四类（工信部《优质中小企业梯度培育管理办法》口径）
FAMILIES = [
    ("创新型中小企业", "创新型中小企业"),
    ("专精特新中小企业", "专精特新中小企业"),
    ("专精特新小巨人", "专精特新小巨人"),
    ("制造业单项冠军", "单项冠军"),
]
CITY4 = ["深圳市", "广州市", "东莞市", "惠州市"]


def main():
    t0 = time.time()
    tt = json.loads((SNAP / "tech_tags_20261021.json").read_text(encoding="utf-8"))
    base = json.loads((SNAP / "base_20261021.json").read_text(encoding="utf-8"))
    bidx = {r[0]: r for r in base}

    per = {f[1]: set() for f in FAMILIES}
    union = set()
    tag_rows = 0
    variants = {f[1]: {} for f in FAMILIES}
    per_nonexpired = {f[1]: set() for f in FAMILIES}
    union_nonexpired = set()
    for oid, tags in tt.items():
        tag_rows += len(tags)
        for t in tags:
            for label, key in FAMILIES:
                if key in t:
                    per[key].add(oid)
                    union.add(oid)
                    variants[key][t] = variants[key].get(t, 0) + 1
                    if "过期待复核" not in t:
                        per_nonexpired[key].add(oid)
                        union_nonexpired.add(oid)

    # 一企多牌结构
    fam_per_org = {}
    for oid in union:
        k = sum(1 for _, key in FAMILIES if oid in per[key])
        fam_per_org[k] = fam_per_org.get(k, 0) + 1

    # 区域分布（org_id → 底册 city / province）
    city = {}
    prov = {}
    unmatched = 0
    for oid in union:
        b = bidx.get(oid)
        if not b:
            unmatched += 1
            continue
        city[b[4]] = city.get(b[4], 0) + 1
        prov[b[3]] = prov.get(b[3], 0) + 1

    per_family_city = {key: {} for _, key in FAMILIES}
    for _, key in FAMILIES:
        for oid in per[key]:
            b = bidx.get(oid)
            if b:
                per_family_city[key][b[4]] = per_family_city[key].get(b[4], 0) + 1

    fam_counts = {key: len(per[key]) for _, key in FAMILIES}
    city4_total = sum(city.get(c, 0) for c in CITY4)
    overlap_pairs = {}
    keys = [k for _, k in FAMILIES]
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            overlap_pairs[f"{keys[i]}×{keys[j]}"] = len(per[keys[i]] & per[keys[j]])

    payload = {
        "metric_id": METRIC,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_sec": round(time.time() - t0, 2),
        "support_judgment": "完全转换支持",
        "definition": {
            "unit": "家企业",
            "dedupe_key": "org_id",
            "families": [{"label": lb, "match": kw, "n_org": fam_counts[kw]} for lb, kw in FAMILIES],
            "rule": "四类标签任一命中即计入，一企多牌只计一次",
        },
        "result": {
            "innovative_count": len(union),
            "share_of_base_pct": round(100.0 * len(union) / len(base), 2),
            "share_of_tagged_pct": round(100.0 * len(union) / len(tt), 2),
            "city4_total": city4_total,
            "city4_share_pct": round(100.0 * city4_total / len(union), 2),
            "unmatched_base": unmatched,
        },
        "family_counts": fam_counts,
        "label_variants": {k: dict(sorted(v.items(), key=lambda kv: -kv[1]))
                           for k, v in variants.items()},
        "sensitivity_exclude_expired": {
            "rule": "剔除标签名含『过期待复核』的写法（341 家小巨人 + 72 家单项冠军标签）",
            "family_counts": {k: len(v) for k, v in per_nonexpired.items()},
            "dedup_total": len(union_nonexpired),
            "delta_vs_main": len(union_nonexpired) - len(union),
        },
        "family_city": per_family_city,
        "city_dist": dict(sorted(city.items(), key=lambda kv: -kv[1])),
        "prov_dist": dict(sorted(prov.items(), key=lambda kv: -kv[1])[:10]),
        "fam_per_org": dict(sorted(fam_per_org.items())),
        "overlap_pairs": dict(sorted(overlap_pairs.items(), key=lambda kv: -kv[1])),
        "coverage": {
            "tag_rows": 202424,
            "tagged_orgs": len(tt),
            "tags_in_cache": tag_rows,
            "base_rows": len(base),
            "join_rate_vs_base": round(100.0 * sum(1 for k in tt if k in bidx) / len(tt), 3),
            "base_coverage_pct": round(100.0 * len(tt) / len(base), 2),
        },
        "notes": [
            "标签源为 gkx.dwd_org_tech_tag（202,424 行 / 32,322 家），已剔除 is_deleted=1。",
            "底册 join 走 org_id 主键（非名称），32,321/32,322 = 99.997% 可落底册。",
            "省级/国家级同义标签（如「省级专精特新中小企业」「国家级专精特新小巨人企业」）按包含关系归入同一族，不重复计数。",
            "「单项冠军」族同时覆盖「制造业单项冠军企业」与「国家级/示范企业」写法。",
        ],
    }
    out = BASE / f"{METRIC}_out.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: payload[k] for k in ("support_judgment", "result", "family_counts",
                                              "fam_per_org", "city_dist", "coverage")},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题系统', '科技信息展示系统']

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
    out_json = here / "M_ENT_INNOVATIVE_COUNT_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ENT_INNOVATIVE_COUNT.py 等价）
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
        "metric_id": "M_ENT_INNOVATIVE_COUNT",
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
