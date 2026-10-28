#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ENT_TYPE_MATCH_COUNT 匹配企业总数
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ENT_TYPE_MATCH_COUNT.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_ENT_TYPE_MATCH_COUNT 企业分类型匹配数量（选产业 ∩ 选类型）。

口径：COUNT(DISTINCT org_id) WHERE 链属(industry_link_code 非空, 12 条战略链)
      AND 企业类型 ∈ 选中集合。
链归属：industry_code 首个 INB 前 7 位；一家只挂一条链（multi_chain_orgs=0），
故多选产业可直接相加，不产生重复计数。
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _build_ent_count21_facts import ensure  # noqa: E402

OUT = os.path.join(HERE, "M_ENT_TYPE_MATCH_COUNT_out.json")
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
    ln = lk["universe"]
    lc = lk["types"]

    rows = [{"key": k, "name": CN[k], "count": lc[k], "denom": ln,
             "pct": pct(lc[k], ln),
             "shenzhen": lk["shenzhen_types"][k],
             "shenzhen_pct": pct(lk["shenzhen_types"][k], lk["shenzhen"])}
            for k in ORDER]

    matrix = []
    for b in lk["per_chain"]:
        matrix.append({
            "chain": b["chain"], "chain_name": b["chain_name"], "orgs": b["orgs"],
            "sz": b["sz"],
            "types": {k: b["types"][k] for k in ORDER},
            "type_pct": {k: pct(b["types"][k], b["orgs"]) for k in ORDER},
        })

    out = {
        "metric_id": "M_ENT_TYPE_MATCH_COUNT",
        "metric_name": "企业分类型匹配数量",
        "support_judgment": "部分支持",
        "judgment_reason": (
            f"12 条战略链真链属 {ln:,} 家在底册内，与六类资质同源可交，"
            "链×类型矩阵 12×6 全部有数；但产业侧只有『链属』没有『非链属但属该产业』，"
            "标签表 7,015 家只挂顶层链无细分链被排除，且链标签来自 dwd_org_industry_tags "
            "单一表、无第二来源校验，故判部分支持。"
        ),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面交叉计数，无年度序列；不设基期",
        "sources": [
            "code/_snapshots21/chain_linked_type_20261023.json",
            "code/_snapshots21/chain_org_agg_20261022.json",
            "code/_snapshots21/ent_count21_facts_20261023.json",
            "code/_probe_linked_chain_strict.py",
            "gkx.dwd_org_industry_tags",
            "gkx.dwd_org_base_info",
            "gkx.dwd_org_tech_tag",
        ],
        "universe": ln,
        "universe_rule": "底册 credit_code ∈ 产业标签信用码 AND industry_link_code 非空；"
                         "链 = SUBSTRING(industry_code, LOCATE('INB', industry_code), 7)",
        "rows": rows,
        "matrix": matrix,
        "chain_union": {
            "sum_chain_orgs": lk["sum_chain_orgs"],
            "distinct_orgs": ln,
            "multi_chain_orgs": lk["multi_chain_orgs"],
            "additive": lk["multi_chain_orgs"] == 0,
            "wide_membership": f["industry_intersection"]["base_in_chain"],
            "unlinked_in_table": f["industry_intersection"]["base_in_chain"] - ln,
        },
        "overlap_pairs": lk["overlap_pairs"],
        "union_examples": {
            "high_tech|little_giant": lc["high_tech"] + lc["little_giant"]
            - lk["overlap_pairs"]["high_tech∩little_giant"],
            "foreign|sme": lc["foreign"] + lc["sme"] - lk["overlap_pairs"]["foreign∩sme"],
            "high_tech|sme": lc["high_tech"] + lc["sme"] - lk["overlap_pairs"]["high_tech∩sme"],
        },
        "sz_strict": lk["shenzhen"],
        "sz_wide": f["industry_intersection"]["sz_in_inter"],
        "none_of_six": lk["none_of_six"],
        "type_sum": lk["type_sum"],
        "duplicate_rate_pct": lk["duplicate_rate_pct"],
        "foreign_excl_hmt": lk["foreign_excl_hmt"],
        "shenzhen_vs_nation_pp": {
            k: round(100 * (lk["shenzhen_types"][k] / lk["shenzhen"]
                            - lc[k] / ln), 2) for k in ORDER
        },
        "naive_sums": {
            "high_tech+little_giant": lc["high_tech"] + lc["little_giant"],
            "software+ai_chain_orgs": 9335 + 4860,
            "six_type_sum": lk["type_sum"],
        },
        "parent_union": f["total"]["union"],
        "wide_scope_reference": {
            "denom": f["industry_intersection"]["base_in_chain"],
            "types": f["industry_intersection"]["type_counts"],
            "note": "宽口径=产业表全表信用码 ∩ 底册（含 7,015 家无细分链），仅作敏感性对照，不作发布值",
        },
        "checks": {
            "per_chain_sum_eq_universe": lk["sum_chain_orgs"] == ln,
            "matrix_sum_eq_type_total": all(
                sum(b["types"][k] for b in lk["per_chain"]) == lc[k] for k in ORDER),
            "sz_le_universe": lk["shenzhen"] <= ln,
            "agg_alignment": lk["check_all_equal"],
        },
        "gaps": [
            "7,015 家只有顶层链、无细分链的企业被排除；宽口径 35,046 与本口径 28,031 差 7,015",
            "链标签单表来源，无工商/专利侧二次校验，链归属可能有误挂",
            "国外主档无产业链上链表，选产业时国外 20,000 家整体缺席",
            "六类重叠（如高企∩专精特新 7,8xx 家），多选类型时并集<求和",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("universe", ln, "rows", [(r["key"], r["count"], r["pct"]) for r in rows])


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
    out_json = here / "M_ENT_TYPE_MATCH_COUNT_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ENT_TYPE_MATCH_COUNT.py 等价）
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
        "metric_id": "M_ENT_TYPE_MATCH_COUNT",
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
