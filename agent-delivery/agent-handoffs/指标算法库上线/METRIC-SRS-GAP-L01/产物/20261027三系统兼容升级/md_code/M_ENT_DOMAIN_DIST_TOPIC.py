#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ENT_DOMAIN_DIST_TOPIC 企业领域分布
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ENT_DOMAIN_DIST_TOPIC.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_ENT_DOMAIN_DIST_TOPIC 企业领域分布（20261021 改源版）。

口径正本：gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_DOMAIN_DIST_TOPIC.md
  stat_year × cluster_id COUNT + 同比，cluster 来自 industry_cluster_map（15）。

本件只读快照，不连数据库。15 集群与 map 两库均无，改按 12 条产业链根码出分布；
链归属表无 stat_year，同比不可算，输出为单期快照分布。
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _w13e3_common as C

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "M_ENT_DOMAIN_DIST_TOPIC_out.json")
ID = "M_ENT_DOMAIN_DIST_TOPIC"


def main():
    probe = C.load("w13e3_probe_20261023.json")
    idx = C.load("chain_firm_index_20261023.json")
    ch = C.chain_panel()
    tags = C.load("tech_tags_20261021.json")

    names = idx["chain_name"]
    cities = idx["chain_city"]
    provs = idx["chain_prov"]

    rows = []
    for code in C.CHAIN_ORDER:
        n = ch["firms"][code]
        top_city = sorted(cities[code].items(), key=lambda kv: -kv[1])[:5]
        top_prov = sorted(provs[code].items(), key=lambda kv: -kv[1])[:3]
        rows.append({
            "rank": len(rows) + 1,
            "chain_code": code,
            "chain_name": names[code],
            "org_cnt": n,
            "share_pct": ch["shares_pct"][code],
            "n_cities": len([k for k, v in cities[code].items() if k != "未匹配" and v > 0]),
            "n_provinces": len([k for k, v in provs[code].items() if k != "未匹配" and v > 0]),
            "top_cities": [{"city": k, "n": v} for k, v in top_city],
            "top_provinces": [{"province": k, "n": v} for k, v in top_prov],
        })

    city_total = ch["city_total"]
    city_rows = [{"city": k, "n": v, "share_pct": C.pct(v, ch["total"], 4)}
                 for k, v in list(city_total.items())[:12] if k != "未匹配"]
    prov_rows = [{"province": k, "n": v, "share_pct": C.pct(v, ch["total"], 4)}
                 for k, v in list(ch["prov_total"].items())[:12] if k != "未匹配"]

    base_rows = [{"chain_code": k, "org_cnt": v,
                  "share_pct": C.pct(v, ch["base_matched_names"], 2)}
                 for k, v in sorted(ch["base_chain"].items(), key=lambda kv: -kv[1])]
    roster_rows = [{"chain_code": k, "org_cnt": v,
                    "share_pct": C.pct(v, ch["roster_matched_rows"], 2)}
                   for k, v in sorted(ch["roster_chain"].items(), key=lambda kv: -kv[1])]

    result = {
        "stat_year_available": False,
        "stat_year_evidence": {
            "tag_table_columns": ["dwd_id", "industry_link_code", "industry_link_name",
                                  "industry_code", "industry_name", "company_name",
                                  "credit_code", "created_time", "updated_time"],
            "has_stat_year_column": False,
            "created_time_distinct": 1,
            "created_time_value": "2026-08-27",
            "note": "链归属表只有入库时间，没有批次自然年；无法构造 stat_year × chain 面板。",
        },
        "yoy_available": False,
        "yoy_note": "同比要求同一领域键的上年计数；本件只有单期快照，上年格不存在，按口径记空而不是按 0。",
        "domain_key": "industry_code 链根（12 条）",
        "domain_key_declared": "industry_cluster_map.cluster_id（15 个）",
        "domain_key_substituted": True,
        "chain_dist": rows,
        "chain_total": ch["total"],
        "top1_share_pct": ch["top1_pct"],
        "top3_share_pct": ch["top3_pct"],
        "hhi": ch["hhi"],
        "n_chains": ch["n_chains"],
        "city_dist_top12": city_rows,
        "province_dist_top12": prov_rows,
        "city_matched": ch["stats"].get("city_matched"),
        "city_unmatched": ch["city_unmatched"],
        "city_matched_pct": C.pct(ch["stats"].get("city_matched", 0), ch["total"], 4),
        "base_name_matched": {
            "n_firms": ch["base_matched_names"],
            "match_share_pct": ch["base_matched_share_pct"],
            "dist": base_rows,
            "note": "底册只有能按企业名对上专利申请人名的子集可落链，不是底册全量。",
        },
        "roster_name_matched": {
            "n_firms": ch["roster_matched_rows"],
            "match_share_pct": ch["roster_matched_share_pct"],
            "dist": roster_rows,
        },
        "l1_path_top12": ch["l1_top"],
        "l1_note": "一级环节 l1_firms 是路径家次（一家企业可落多个环节），不能当企业去重数，也不能除以链企业数。",
        "cluster_dimension": {
            "declared_n": 15,
            "available_n": 0,
            "gkx_cluster_tables": probe["A_schema_scan"]["tables"]["table_name_hits"]["cluster"],
            "gkx_cluster_columns": probe["A_schema_scan"]["columns"]["n_cluster_columns"],
            "live_cluster_tables": probe["F_live"]["table_name_hits"]["cluster"],
            "live_industry_cluster": probe["F_live"]["exact_counts"].get("gkxlumenx_dim.industry_cluster"),
            "live_industry_cluster_map": probe["F_live"]["exact_counts"].get("gkxlumenx_dim.industry_cluster_map"),
        },
        "tech_tag_context": {
            "orgs": len(tags),
            "note": "技术标签不是领域键，只用于说明企业侧还有另一套分类，不可替代 cluster_id。",
        },
    }

    out = {
        "metric_id": ID,
        "metric_name": "企业领域分布",
        "script": ID + ".py",
        "as_of": C.AS_OF,
        "source": {
            "db": C.DB_GKX,
            "snapshots": [
                "code/_snapshots21/chain_firm_index_20261023.json",
                "code/_snapshots21/chain_tree_20261021.json",
                "code/_snapshots21/base_20261021.json",
                "code/_snapshots21/star_roster_gkx_20261021.json",
                "code/_snapshots21/tech_tags_20261021.json",
                "code/_snapshots21/w13e3_probe_20261023.json",
            ],
        },
        "calc_logic_ref": "gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_DOMAIN_DIST_TOPIC.md",
        "support_judgment": "部分支持",
        "verdict_kind": "proxy_constructed",
        "four_judgment": {
            "表结构直接支持（开发库+三方库）": "否：两库均无 enterprise_domain_year_dist 结果表",
            "表数据直接支持（开发库+三方库）": "否：无结果表，且无 stat_year",
            "依赖表结构支持（开发库/三方库）": "部分：gkx 有企业↔链结构，无 15 集群 map；无年度键",
            "依赖表数据支持（开发库/三方库）": "是（单期）/否（年度）：链归属 1,714,457 家可出 12 链分布，年度与同比不可算",
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "本件无年度键：链归属表没有 stat_year，created_time 只有单一批次。"
                            "因此既没有「进入分母的年份」，也没有「缺哪一年」，used/missing 为空；"
                            "同比按「上年格不存在」记空，不按 0 摊入。",
        "result": result,
        "notes": [
            "12 链分布不是 15 集群分布：码级映射不存在，同名词只有 5 个且成员范围未核。",
            "链归属表 24.93% 的行为空数组（569,303 行），这些企业不进任何链的分子。",
            "一级环节是路径家次，不是企业去重数；本件不用它做分母或覆盖率。",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote", OUT)
    print("total", ch["total"], "top1", ch["top1_pct"], "top3", ch["top3_pct"])
    for r in rows:
        print(r["rank"], r["chain_name"], r["org_cnt"], r["share_pct"])


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
    out_json = here / "M_ENT_DOMAIN_DIST_TOPIC_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ENT_DOMAIN_DIST_TOPIC.py 等价）
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
        "metric_id": "M_ENT_DOMAIN_DIST_TOPIC",
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
