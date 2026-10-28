#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ENT_TYPE_COUNT 各类型企业数
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ENT_TYPE_COUNT.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_ENT_TYPE_COUNT 企业分类型数量（高企/专精特新/小巨人/外资/小微/上市）。

六类口径（calc-logic + wanghui 正本对齐，详见 MD §1.3）：
  high_tech       dwd_org_tech_tag.org_tag 含「高新技术企业」（三变体，org_id 去重）
  little_giant    org_tag 含「专精特新中小企业」
  little_giant_pro org_tag 含「专精特新小巨人」
  foreign         dwd_org_base_info.org_type 含 外商投资/中外合资/中外合作/外资/港澳台/外国
  sme             dwd_org_base_info.org_size ∈ {小型, 微型}
  listed          dwd_org_base_info.listing_status 非空
零 SQL：读 ent_count21_facts 快照 + tech_tags 快照。
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _build_ent_count21_facts import ensure, load_raw, has_tag, is_foreign  # noqa: E402

OUT = os.path.join(HERE, "M_ENT_TYPE_COUNT_out.json")
TAGS = os.path.join(HERE, "_snapshots21", "tech_tags_20261021.json")
BASE = os.path.join(HERE, "_snapshots21", "base_20261021.json")
ORDER = ["high_tech", "little_giant", "little_giant_pro", "foreign", "sme", "listed"]
CN = {"high_tech": "高新技术企业", "little_giant": "专精特新中小企业",
      "little_giant_pro": "专精特新小巨人", "foreign": "外资企业",
      "sme": "小微企业", "listed": "上市/挂牌企业"}


def main():
    f = ensure()
    types = f["types"]
    base_n = types["base_universe"]
    counts = types["counts"]

    tech = json.load(open(TAGS, encoding="utf-8"))
    base = json.load(open(BASE, encoding="utf-8"))
    raw = load_raw()
    attrs = {r[0]: (r[1], r[2], r[3]) for r in raw["base_attrs"]}

    def flag(oid):
        ot, sz, ls = attrs[oid]
        tg = tech.get(oid, [])
        return {
            "high_tech": has_tag(tg, "高新技术企业"),
            "little_giant": has_tag(tg, "专精特新中小企业"),
            "little_giant_pro": has_tag(tg, "专精特新小巨人"),
            "foreign": is_foreign(ot, True),
            "sme": sz in ("小型", "微型"),
            "listed": ls not in (None, ""),
        }

    flags = {r[0]: flag(r[0]) for r in base}
    pairs = {}
    for i, a in enumerate(ORDER):
        for b in ORDER[i + 1:]:
            pairs[f"{a}∩{b}"] = sum(1 for o, fl in flags.items() if fl[a] and fl[b])
    triple_ht_lg = sum(1 for fl in flags.values()
                       if fl["high_tech"] and fl["little_giant"] and fl["little_giant_pro"])
    none_of = sum(1 for fl in flags.values() if not any(fl.values()))

    variants = {}
    for needle in ("高新技术企业", "专精特新", "小巨人"):
        c = {}
        for v in tech.values():
            for t in v:
                if needle in t:
                    c[t] = c.get(t, 0) + 1
        variants[needle] = sorted(c.items(), key=lambda kv: -kv[1])

    sz_counts = types["shenzhen_counts"]
    tsum = sum(counts[k] for k in ORDER)
    out = {
        "metric_id": "M_ENT_TYPE_COUNT",
        "metric_name": "企业分类型数量",
        "support_judgment": "部分支持",
        "judgment_reason": (
            "六类中四类（高企/专精特新/小巨人/小微）表结构+表数据直接可算；"
            "外资类 org_type 是工商登记类型自由文本，需关键词口径且含港澳台；"
            "上市类底册 listing_status 仅 1,971 家、dwd_org_stock_base 只覆盖 A/B 股 975 家，"
            "缺港股/美股/新三板，六类口径不等权，合计不可当『企业总数』使用。"
        ),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面资质计数，无年度序列；资质本身有授予年（高企 3 年有效），"
                            "但 gkx 标签表无生效/失效日期列，故不拆年份",
        "sources": [
            "code/_snapshots21/ent_count21_facts_20261023.json",
            "code/_snapshots21/tech_tags_20261021.json",
            "code/_snapshots21/base_20261021.json",
            "gkx.dwd_org_tech_tag",
            "gkx.dwd_org_base_info",
            "gkx.dwd_org_stock_base",
        ],
        "universe": base_n,
        "chain_linked_universe": sum(r["in_base"] for r in f["chain"]["per_chain"]),
        "types": [
            {"key": k, "name": CN[k], "count": counts[k],
             "ratio_of_base": types["ratio_of_base"][k],
             "ratio_pct": round(100 * types["ratio_of_base"][k], 2),
             "shenzhen": sz_counts[k],
             "shenzhen_ratio_pct": round(100 * types["shenzhen_ratio"][k], 2),
             "definition": types["definitions"][k]}
            for k in ORDER
        ],
        "type_sum": tsum,
        "base_ratio_sum_pct": round(100 * tsum / base_n, 2),
        "covered_orgs": base_n - none_of,
        "coverage_pct": round(100 * (base_n - none_of) / base_n, 2),
        "shenzhen_vs_nation_pp": {
            k: round(100 * (sz_counts[k] / types["shenzhen_universe"]
                            - counts[k] / base_n), 2) for k in ORDER
        },
        "listed_not_in_stock": counts["listed"] - f["listed"]["stock_distinct_org"],
        "foreign_excl_hmt_pct": round(100 * f["org_type"]["foreign_excl_hmt"] / base_n, 2),
        "foreign_incl_minus_excl": f["org_type"]["foreign_incl_hmt"] - f["org_type"]["foreign_excl_hmt"],
        "type_sum_note": f"六类互有重叠且口径不等权，求和 {tsum} 不是企业数（底册 {base_n}）",
        "overlap": {"pairs": pairs, "high_tech_little_giant_lgp": triple_ht_lg,
                    "none_of_six": none_of},
        "tag_variants": variants,
        "tag_coverage": f["tech_tag"],
        "tag_share_pct": round(100 * f["tech_tag"]["share_of_base"], 2),
        "tagged_orgs": f["tech_tag"]["orgs"],
        "untagged_orgs": base_n - f["tech_tag"]["orgs"],
        "org_size": f["org_size"],
        "foreign_detail": f["org_type"],
        "listed_detail": f["listed"],
        "shenzhen_universe": types["shenzhen_universe"],
        "checks": {
            "sme_eq_small_plus_micro": f["org_size"]["sme_small_micro"]
            == dict(f["org_size"]["dist"])["小型"] + dict(f["org_size"]["dist"])["微型"],
            "listed_eq_region_snapshot": f["listed"]["listing_status_nonempty"]
            == f["listed"]["listing_status_snapshot_nonempty"],
            "high_tech_eq_variant_union": counts["high_tech"] == len(
                [1 for v in tech.values() if has_tag(v, "高新技术企业")]),
        },
        "gaps": [
            "外资口径含港澳台（10,417），剔除港澳台后 3,307，两口径差 7,110 家须在报表注明",
            "上市口径 listing_status 非空 1,971 vs stock_base 975，差额 996 家为挂牌/非 A/B 股，无法拆分市场",
            "org_size 有 46,897 家『未知』+287 家『-』，小微 125,477 是下限而非全量",
            "标签表无资质有效期，高企/专精特新为『历史获得』累计口径，非当前有效存量",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("counts", counts, "sum", out["type_sum"], "none_of_six", none_of)


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
    out_json = here / "M_ENT_TYPE_COUNT_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ENT_TYPE_COUNT.py 等价）
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
        "metric_id": "M_ENT_TYPE_COUNT",
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
