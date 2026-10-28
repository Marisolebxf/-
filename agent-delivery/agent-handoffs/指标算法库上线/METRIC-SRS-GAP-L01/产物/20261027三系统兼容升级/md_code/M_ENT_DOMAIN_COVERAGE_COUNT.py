#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ENT_DOMAIN_COVERAGE_COUNT 覆盖领域数
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ENT_DOMAIN_COVERAGE_COUNT.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_ENT_DOMAIN_COVERAGE_COUNT 覆盖领域数（20261021 改源版）。

口径正本：gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_DOMAIN_COVERAGE_COUNT.md
  COUNT(DISTINCT cluster_id) over industry_cluster_map（15 集群）。
王惠正本：（王惠正本已并入 calc-logic 入库件）

本件只读 code/_snapshots21/ 的落盘快照，不连数据库。
15 集群目录与 industry_cluster_map 在 gkx 与 live 均不存在（见探针），
故按 12 条产业链根码做代理口径，并给出「链→集群」不可映射的证据。
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _w13e3_common as C

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "M_ENT_DOMAIN_COVERAGE_COUNT_out.json")
ID = "M_ENT_DOMAIN_COVERAGE_COUNT"


def main():
    probe = C.load("w13e3_probe_20261023.json")
    tree = C.load("chain_tree_20261021.json")
    ch = C.chain_panel()
    base = C.base_panel()

    # 15 集群目录证据
    gkx_tables = probe["A_schema_scan"]["tables"]
    gkx_cols = probe["A_schema_scan"]["columns"]
    live = probe["F_live"]
    live_hits = live["table_name_hits"]["cluster"]
    live_exact = live["exact_counts"]

    roots = sorted(ch["firms"].keys())
    coverage_examples = {}
    for city in ["深圳市", "广州市", "东莞市", "惠州市", "北京市", "上海市", "杭州市", "成都市"]:
        n = ch["city_coverage"].get(city)
        if n is not None:
            coverage_examples[city] = n

    low_examples = {}
    for city, n in ch["city_coverage"].items():
        if n <= 6 and len(low_examples) < 8:
            low_examples[city] = {"coverage": n, "firms": ch["city_total"].get(city, 0)}

    # 按链覆盖的「链目录规模」与「声明目录规模」并列，不做伪映射
    nominal = C.pct(ch["n_chains"], 15, 2)

    result = {
        "declared_domain_catalog": {
            "name": "industry_cluster（10 战新 + 5 未来）",
            "n_declared": 15,
            "catalog_available_in_gkx": False,
            "catalog_available_in_live": False,
            "evidence": {
                "gkx_tables_matching_cluster": gkx_tables["table_name_hits"]["cluster"],
                "gkx_n_tables": gkx_tables["n_tables"],
                "gkx_cluster_id_columns": gkx_cols["column_hits"]["cluster_id"],
                "gkx_cluster_name_columns": gkx_cols["column_hits"]["cluster_name"],
                "gkx_n_cluster_columns": gkx_cols["n_cluster_columns"],
                "live_tables_matching_cluster": live_hits,
                "live_industry_cluster": live_exact.get("gkxlumenx_dim.industry_cluster"),
                "live_industry_cluster_map": live_exact.get("gkxlumenx_dim.industry_cluster_map"),
            },
        },
        "proxy_domain_catalog": {
            "name": "dwd_industry_chain_info 产业链根码 12 条",
            "n_chains": ch["n_chains"],
            "roots": roots,
            "chain_names": {k: C.load("chain_firm_index_20261023.json")["chain_name"][k] for k in roots},
            "tree_rows": len(tree) if isinstance(tree, list) else (tree.get("n_nodes") or 0),
            "tree_has_inb17_or_inb18": probe["B_chain_info"]["has_inb17"] + probe["B_chain_info"]["has_inb18"],
            "tag_distinct_industry_code": probe["C_chain_code_universe"]["distinct_industry_code"],
            "tag_has_inb17_or_inb18": probe["C_chain_code_universe"]["any_inb17_or_inb18"],
        },
        "nominal_chain_vs_declared_pct": nominal,
        "nominal_ratio_comparable": False,
        "nominal_ratio_note": "12 条链与 15 个集群没有码级映射，12/15 只表示两个目录的规模比，不是覆盖率。",
        "universe": {
            "tag_rows": ch["stats"].get("rows", 2283762),
            "bad_credit_rows": ch["stats"].get("bad_credit_rows", 2),
            "empty_link_rows": ch["stats"].get("empty_link_rows", 569303),
            "linked_firms_clean": ch["total"],
            "multi_code_rows": ch["stats"].get("multi_chain_rows", 131978),
            "multi_code_row_share_pct": C.pct(ch["stats"].get("multi_chain_rows", 131978),
                                              ch["stats"].get("rows", 2283762), 2),
        },
        "coverage_by_set": {
            "全国链属企业": {"n_firms": ch["total"], "coverage": ch["n_chains"]},
            "明星名单可对齐子集": {"n_firms": ch["roster_matched_rows"],
                                    "coverage": len(ch["roster_chain"]),
                                    "match_share_pct": ch["roster_matched_share_pct"]},
            "底册专利名可对齐子集": {"n_firms": ch["base_matched_names"],
                                        "coverage": len(ch["base_chain"]),
                                        "match_share_pct": ch["base_matched_share_pct"]},
            "深圳市": {"n_firms": ch["city_total"].get("深圳市", 0), "coverage": ch["city_coverage"].get("深圳市")},
            "广州市": {"n_firms": ch["city_total"].get("广州市", 0), "coverage": ch["city_coverage"].get("广州市")},
            "东莞市": {"n_firms": ch["city_total"].get("东莞市", 0), "coverage": ch["city_coverage"].get("东莞市")},
            "惠州市": {"n_firms": ch["city_total"].get("惠州市", 0), "coverage": ch["city_coverage"].get("惠州市")},
        },
        "city_coverage_examples": coverage_examples,
        "low_coverage_cities": low_examples,
        "city_coverage_dist": ch["city_coverage_dist"],
        "n_cities_evaluated": ch["n_cities"],
        "n_cities_full_12": ch["n_cities_full"],
        "city_full_12_share_pct": C.pct(ch["n_cities_full"], ch["n_cities"], 2),
        "chain_firms": ch["firms"],
        "chain_share_pct": ch["shares_pct"],
        "hhi": ch["hhi"],
        "top1_chain_pct": ch["top1_pct"],
        "top3_chain_pct": ch["top3_pct"],
        "per_firm": {
            "rule": "industry_code 首个 INB 链根；一家企业一个链根",
            "n_firms": ch["total"],
            "coverage_value": 1,
            "distribution": {"1": ch["total"]},
            "multi_code_rows_dropped": ch["stats"].get("multi_chain_rows", 131978),
        },
        "base": {
            "n_rows": base["n_rows"],
            "n_province": base["n_province"],
            "n_city": base["n_city"],
        },
        "five_cluster_names_with_chain_homonym": [
            "人工智能", "智能终端", "软件与信息服务", "生物医药", "合成生物"
        ],
        "cluster_to_chain_mapping": {
            "mapped_by_code": 0,
            "mapped_by_exact_name": 0,
            "homonym_only": 5,
            "note": "同名词不能当映射：无 cluster_id、无 map 表，同名词的成员范围也未核。",
        },
    }

    out = {
        "metric_id": ID,
        "metric_name": "覆盖领域数",
        "script": ID + ".py",
        "as_of": C.AS_OF,
        "source": {
            "db": C.DB_GKX,
            "snapshots": [
                "code/_snapshots21/chain_firm_index_20261023.json",
                "code/_snapshots21/chain_tree_20261021.json",
                "code/_snapshots21/base_20261021.json",
                "code/_snapshots21/star_roster_gkx_20261021.json",
                "code/_snapshots21/w13e3_probe_20261023.json",
            ],
        },
        "calc_logic_ref": "gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_DOMAIN_COVERAGE_COUNT.md",
        "（正本见本目录 M_ENT_DOMAIN_COVERAGE_COUNT.md / calc-logic 入库件）",
        "support_judgment": "部分支持",
        "verdict_kind": "proxy_constructed",
        "four_judgment": {
            "表结构直接支持（开发库+三方库）": "否：两库均无「覆盖领域数」结果面；gkx 无 cluster/结果表，live 无结果表",
            "表数据直接支持（开发库+三方库）": "否：15 集群目录无数据载体",
            "依赖表结构支持（开发库/三方库）": "部分：企业↔链结构在 gkx（dwd_org_industry_tags），15 集群 dim 与 map 两库均无",
            "依赖表数据支持（开发库/三方库）": "是（降维后）：链属企业 1,714,457 家可算 12 链覆盖；集群维不可算",
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "本件是截面计数：链归属表无 stat_year 字段，输出的是当日快照上的集合覆盖数，"
                            "不存在年度分母，故 used/missing 为空；不是把缺年按 0 摊入。",
        "result": result,
        "extra_probes": {
            "tags_created_time_distinct": "单一批次（2026-08-27），无年度键",
            "chain_info_level_dist": probe["B_chain_info"]["level_dist"],
            "chain_info_root_count": probe["B_chain_info"]["root_7_count"],
            "live_nonempty_tables": live.get("nonempty_tables"),
            "live_enterprise_industry_chain_rows": live_exact.get("gkxlumenx_dwd.enterprise_industry_chain"),
        },
        "notes": [
            "15 集群目录（10 战新 + 5 未来）在 gkx 280 表中 0 命中，live 侧 industry_cluster / industry_cluster_map 直接不存在。",
            "gkx 的 industry_code 只出现 12 个链根码，没有 INB1701—1710 / INB1801—1805，因此无法用链码反推集群。",
            "代理口径只回答「这批企业覆盖了几条产业链」，不能回答「覆盖了几个 15 集群」。",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote", OUT)
    print("linked", ch["total"], "chains", ch["n_chains"], "cities_full", ch["n_cities_full"],
          "roster_matched", ch["roster_matched_rows"], "base_matched", ch["base_matched_names"])
    print("coverage examples", coverage_examples)


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
    out_json = here / "M_ENT_DOMAIN_COVERAGE_COUNT_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ENT_DOMAIN_COVERAGE_COUNT.py 等价）
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
        "metric_id": "M_ENT_DOMAIN_COVERAGE_COUNT",
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
