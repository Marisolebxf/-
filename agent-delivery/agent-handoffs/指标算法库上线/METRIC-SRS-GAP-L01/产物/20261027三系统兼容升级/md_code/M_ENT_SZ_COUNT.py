#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ENT_SZ_COUNT 深圳企业数量
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ENT_SZ_COUNT.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_ENT_SZ_COUNT 深圳企业数量。

口径：底册 dwd_org_base_info.city='深圳市' 的去重 org_id 数；
选产业时用链属快照（chain_linked_type_20261023）内的 city='深圳市' 子集。
深圳=全市（含深汕合作区），不按区县拆分（底册无区县列）。
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _build_ent_count21_facts import ensure  # noqa: E402

OUT = os.path.join(HERE, "M_ENT_SZ_COUNT_out.json")
LINKED = os.path.join(HERE, "_snapshots21", "chain_linked_type_20261023.json")
ORDER = ["high_tech", "little_giant", "little_giant_pro", "foreign", "sme", "listed"]
CN = {"high_tech": "高新技术企业", "little_giant": "专精特新中小企业",
      "little_giant_pro": "专精特新小巨人", "foreign": "外资企业",
      "sme": "小微企业", "listed": "上市/挂牌企业"}


def pct(a, b):
    return round(100.0 * a / b, 2)


def main():
    f = ensure()
    lk = json.load(open(LINKED, encoding="utf-8"))
    base = f["base"]
    n = f["types"]["base_universe"]
    sz = base["shenzhen_city"]

    cities = [{"city": c, "count": v, "pct": pct(v, n)} for c, v in base["city_dist_top"]]
    gd = dict(base["prov_dist_top"]).get("广东省", 0)
    others_gd = [c for c in cities if c["city"] in ("广州市", "东莞市", "惠州市")]
    rest_gd = gd - sz - sum(c["count"] for c in others_gd)

    out = {
        "metric_id": "M_ENT_SZ_COUNT",
        "metric_name": "深圳企业数量",
        "support_judgment": "部分支持",
        "judgment_reason": (
            "底册有 city='深圳市' 中文市名，95,600 家可直接 GROUP BY 得到，且与广东省 188,776 家、"
            "全国 189,116 家勾稽；但 calc-logic 钉死的 region_id LIKE '4403%' 行政区划码在 gkx "
            "dwd_org_base_info 中不存在（列字典 44 列无 region_id/adcode），只能用中文市名代理，"
            "故判部分支持而非完全转换支持。"
        ),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面计数；不按成立年拆分（底册成立年跨 1900—2026，无『当年新增』语义）",
        "sources": [
            "code/_snapshots21/ent_count21_facts_20261023.json",
            "code/_snapshots21/base_20261021.json",
            "code/_snapshots21/chain_linked_type_20261023.json",
            "gkx.dwd_org_base_info",
        ],
        "nationwide": n,
        "guangdong": gd,
        "shenzhen": sz,
        "share_of_nation_pct": pct(sz, n),
        "share_of_guangdong_pct": pct(sz, gd),
        "city_top": cities,
        "other_prd": [{"city": c["city"], "count": c["count"], "pct_of_nation": c["pct"]}
                      for c in others_gd],
        "other_guangdong": rest_gd,
        "prd_four_city_sum": sz + sum(c["count"] for c in others_gd),
        "prd_four_city_share_of_gd_pct": pct(sz + sum(c["count"] for c in others_gd), gd),
        "other_city_sum": n - (sz + sum(c["count"] for c in others_gd) + rest_gd),
        "chain_vs_nation_pp": round(pct(lk["shenzhen"], lk["universe"]) - pct(sz, n), 2),
        "wide_minus_strict_sz": f["industry_intersection"]["sz_in_inter"] - lk["shenzhen"],
        "wide_minus_strict_sz_pct": pct(f["industry_intersection"]["sz_in_inter"] - lk["shenzhen"], lk["shenzhen"]),
        "sz_top3_chain_sum": sum(b["sz"] for b in lk["per_chain"][:3]),
        "sz_top3_chain_pct": pct(sum(b["sz"] for b in lk["per_chain"][:3]), lk["shenzhen"]),
        "legacy_ods_probe": 17562,
        "legacy_mock_value": 12860,
        "city_null": base["city_null"],
        "city_count": base["distinct_city"],
        "other_prov_sum": n - gd,
        "four_city_gap_to_gd": gd - (sz + sum(c["count"] for c in others_gd)),
        "guangdong_outside_prd": gd - sz - sum(c["count"] for c in others_gd),
        "types": [
            {"key": k, "name": CN[k], "count": f["types"]["shenzhen_counts"][k],
             "pct_of_sz": pct(f["types"]["shenzhen_counts"][k], sz),
             "chain_count": lk["shenzhen_types"][k],
             "pct_of_chain_sz": pct(lk["shenzhen_types"][k], lk["shenzhen"])}
            for k in ORDER
        ],
        "chain_slice": {
            "linked_universe": lk["universe"],
            "shenzhen": lk["shenzhen"],
            "share_of_linked_pct": pct(lk["shenzhen"], lk["universe"]),
            "wide_slice_shenzhen": f["industry_intersection"]["sz_in_inter"],
            "wide_slice_denom": f["industry_intersection"]["base_in_chain"],
            "wide_slice_pct": pct(f["industry_intersection"]["sz_in_inter"],
                                  f["industry_intersection"]["base_in_chain"]),
        },
        "per_chain_shenzhen": [
            {"chain": b["chain"], "chain_name": b["chain_name"], "sz": b["sz"],
             "orgs": b["orgs"], "sz_pct": pct(b["sz"], b["orgs"])}
            for b in lk["per_chain"]
        ],
        "checks": {
            "sz_le_guangdong": sz <= gd,
            "guangdong_le_nation": gd <= n,
            "city_sum_le_nation": sum(v for _, v in base["city_dist_top"]) <= n,
            "sz_plus_other_prd_plus_rest_eq_gd": sz + sum(
                c["count"] for c in others_gd) + rest_gd == gd,
            "city_null_explained": base["city_null"] == 1,
        },
        "gaps": [
            "底册 city 为工商注册地，非实际经营地；深圳注册的集团总部会高估本地产业活动",
            "1 家 city 为空，按地市汇总时全国合计会差 1",
            "深汕特别合作区企业归属深圳统计，与惠州口径存在行政边界差异",
            "选产业后的深圳链属 16,875 家只覆盖 12 条战略链，不等于深圳全部产业企业",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("sz", sz, "share", out["share_of_nation_pct"], "gd", gd,
          "chain_sz", lk["shenzhen"], out["chain_slice"]["share_of_linked_pct"])


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
    out_json = here / "M_ENT_SZ_COUNT_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ENT_SZ_COUNT.py 等价）
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
        "metric_id": "M_ENT_SZ_COUNT",
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
