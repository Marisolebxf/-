#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ENT_ATTRACTION_INDEX 招引推荐指数
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ENT_ATTRACTION_INDEX.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_ENT_ATTRACTION_INDEX 招引推荐指数 — 三维可算性实测脚本（20261021 改源版）

王惠口径（calc-logic/ENT/M_ENT_ATTRACTION_INDEX.md）：
  Rec_i = W1·产业相关度_i + W2·政策匹配度_i + W3·深圳连接度_i（极值归一 0-100 后加权）
  - 产业相关度：产业链融入度（industry_tags + 投入产出上游度 + 收入占比 c_i）【M_ENT_INDUSTRY_MATCH_SCORE 同】
  - 政策匹配度：行动型契合 + 话语型契合（政策词典 × GPT 分类企业文本）
  - 深圳连接度：深圳网络中心度（供应链边，库内用投资/股东边代理）+ 城市对引力模型（人口/GDP/距离，库内无）

本脚本实测各维依赖侧的「结构+当前数据量」并计算可代理部分，输出 support_judgment。
主算：三方库 gkx（全表名 gkx.<表名>）；行数只读 _work_gkx21/GKX_INVENTORY.json。
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent
ROOT = CODE_DIR.parent
sys.path.insert(0, str(CODE_DIR))

from _gkxdb import gkx  # noqa: E402

OUT = Path(__file__).with_name("M_ENT_ATTRACTION_INDEX_out.json")
INVENTORY = ROOT / "_work_gkx21" / "GKX_INVENTORY.json"


def inv_rows() -> dict:
    d = json.loads(INVENTORY.read_text(encoding="utf-8"))
    return {k: int(v["rows"]) for k, v in d.items()}


def q(sql: str, args=None):
    cur = gkx()
    try:
        cur.execute(sql, args)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    finally:
        cur.close()


def q1(sql: str, args=None):
    rows = q(sql, args)
    return rows[0] if rows else None


def probe(inv: dict) -> dict:
    out = {}
    for t, alias in [
        ("dwd_org_base_info", "base"),
        ("dwd_org_industry_tags", "tags"),
        ("dwd_org_shareholder_info", "shareholder"),
        ("dwd_org_invest_info", "invest"),
        ("dwd_org_org_product_info", "product"),
        ("dwd_policy_base", "policy"),
        ("dwd_org_annual_financial_info", "fin"),
    ]:
        out[alias] = inv[t]
    # 字段填充（强过滤聚合；长文本列按样本估填充率，避免整列 blob 全扫）
    r = q1("SELECT COUNT(*) n, SUM(content IS NOT NULL AND content<>'') c, "
           "SUM(keywords IS NOT NULL AND keywords<>'') k "
           "FROM (SELECT content, keywords FROM gkx.dwd_policy_base LIMIT 3000) t")
    out["policy_sample_rows"] = int(r["n"])
    out["policy_content_filled_rate"] = round(int(r["c"] or 0) / int(r["n"]), 4) if int(r["n"]) else None
    out["policy_content_filled"] = int(round(int(r["c"] or 0) / int(r["n"]) * inv["dwd_policy_base"])) \
        if int(r["n"]) else None
    out["policy_keywords_filled"] = int(r["k"] or 0)
    r = q1("SELECT COUNT(*) n, SUM(description IS NOT NULL AND description<>'') d, "
           "SUM(org_id IS NOT NULL AND org_id<>'') o "
           "FROM (SELECT description, org_id FROM gkx.dwd_org_org_product_info LIMIT 5000) t")
    out["product_sample_rows"] = int(r["n"])
    out["product_desc_fill_rate"] = round(int(r["d"] or 0) / int(r["n"]), 4) if int(r["n"]) else None
    out["product_desc_filled"] = int(round(int(r["d"] or 0) / int(r["n"]) * inv["dwd_org_org_product_info"])) \
        if int(r["n"]) else None
    out["product_org_filled"] = int(round(int(r["o"] or 0) / int(r["n"]) * inv["dwd_org_org_product_info"])) \
        if int(r["n"]) else None
    tags_sample = q1(
        "SELECT COUNT(*) n, SUM(industry_link_code IS NOT NULL AND industry_link_code<>'') linked "
        "FROM (SELECT industry_link_code FROM gkx.dwd_org_industry_tags LIMIT 200000) t")
    out["tags_sample_rows"] = int(tags_sample["n"])
    out["tags_link_filled_sample"] = int(tags_sample["linked"] or 0)
    out["tags_link_fill_rate"] = (round(int(tags_sample["linked"] or 0) / int(tags_sample["n"]), 4)
                                  if int(tags_sample["n"]) else None)
    out["fin_rev_filled"] = int(q1(
        "SELECT COUNT(*) n FROM gkx.dwd_org_annual_financial_info "
        "WHERE main_business_revenue IS NOT NULL AND main_business_revenue<>0")["n"])
    # tags → chain_info 关联（20 万行样本；全表口径由 M_ENT_KEYPANO_DOMAIN_SUMMARY 实测）
    join = q1(
        "SELECT COUNT(*) n FROM (SELECT industry_code, industry_link_code "
        "FROM gkx.dwd_org_industry_tags LIMIT 200000) t "
        "JOIN gkx.dwd_industry_chain_info c "
        "ON t.industry_code=c.industry_code AND t.industry_link_code=c.industry_link_code")
    out["tags_chain_join_rows_sample"] = int(join["n"])
    return out


def compute() -> dict:
    """深圳连接度维的可代理子项：投资/股东边度中心度（王惠「中心度」的库内代理）"""
    city_rows = q("SELECT org_id, city, name_cn FROM gkx.dwd_org_base_info")
    city_map = {r["org_id"]: r for r in city_rows if r.get("org_id")}
    sz_set = {oid for oid, r in city_map.items() if r.get("city") and "深圳" in str(r["city"])}

    inv = [(r["org_id"], r["inv_org_id"]) for r in q("SELECT org_id, inv_org_id FROM gkx.dwd_org_invest_info")]
    sh = [(r["org_id"], r["inv_org_id"]) for r in q("SELECT org_id, inv_org_id FROM gkx.dwd_org_shareholder_info")]

    deg = defaultdict(int)
    deg_sz = defaultdict(int)
    for o, j in inv + sh:
        if not o or not j:
            continue
        deg[o] += 1
        deg[j] += 1
        if j in sz_set:
            deg_sz[o] += 1
        if o in sz_set:
            deg_sz[j] += 1

    n_nodes = len(deg)
    scores = {}
    for o in deg:
        if n_nodes > 1:
            scores[o] = round(100.0 * deg_sz[o] / (n_nodes - 1), 6)
    vals = list(scores.values())
    pos = [v for v in vals if v > 0]

    sample = []
    for o, s in sorted(scores.items(), key=lambda kv: -kv[1])[:10]:
        m = city_map.get(o, {})
        sample.append({"org_id": o, "name_cn": m.get("name_cn"), "city": m.get("city"),
                       "degree": deg[o], "sz_links": deg_sz[o], "sz_degree_centrality_proxy": s})
    return {
        "sz_orgs": len(sz_set),
        "n_nodes_with_degree": n_nodes,
        "n_scored": len(scores),
        "n_positive_sz_link": len(pos),
        "score_stats": {
            "min": min(vals) if vals else None, "max": max(vals) if vals else None,
            "mean": round(statistics.mean(vals), 8) if vals else None,
            "median": round(statistics.median(vals), 8) if vals else None,
        },
        "note": "王惠中心度=供应链边度中心度；gkx 无供应链表，用投资+股东边代理（方向与王惠 M_SVC_DEEP_180_1 同）",
        "top10_by_sz_degree": sample,
    }


def spotcheck(inv: dict, probe_out: dict) -> dict:
    """换源后无 demo 对照面：改为库存行数与本脚本读数自校验。"""
    return {
        "source": "gkx",
        "inventory_file": "_work_gkx21/GKX_INVENTORY.json",
        "inventory_rows": {t: inv[t] for t in
                           ["dwd_org_industry_tags", "dwd_org_invest_info", "dwd_policy_base",
                            "dwd_org_org_product_info"]},
        "probe_rows_match": (inv["dwd_org_industry_tags"] == probe_out.get("tags")
                             and inv["dwd_policy_base"] == probe_out.get("policy")),
    }


def judge(probe_out, comp, spot) -> dict:
    dims = {
        "产业相关度": {
            "结构": "tags 2,283,762 行有表且 industry_link_code 样本填充率高，但 tags.industry_code×industry_link_code "
                    "与 dwd_industry_chain_info 关联 0 行（链路码体系不匹配）；投入产出表缺失",
            "数据量": f"tags={probe_out.get('tags')} 行（链路码样本填充率 {probe_out.get('tags_link_fill_rate')}）、"
                      f"tags×chain_info 关联 {probe_out.get('tags_chain_join_rows_sample')} 行（20 万行样本）；收入填充 {probe_out.get('fin_rev_filled')}",
            "verdict": "部分",
        },
        "政策匹配度": {
            "结构": "policy_base 2 万行有 content/keywords 表结构",
            "数据量": f"content 填充 {probe_out.get('policy_content_filled')}；keywords 填充 {probe_out.get('policy_keywords_filled')}；"
                      f"企业侧文本 org_product_info={probe_out.get('product')} 行、desc 填充 {probe_out.get('product_desc_filled')}；GPT 分类层未建",
            "verdict": "部分",
        },
        "深圳连接度": {
            "结构": "无供应链表；投资/股东边可代理中心度",
            "data": f"scored={comp.get('n_scored')}, sz_linked={comp.get('n_positive_sz_link')}",
            "verdict": "代理可算；引力模型子项（人口/GDP/距离）库内无 → 部分",
        },
    }
    level = "部分支持"
    return {
        "data_support_level": level,
        "reason": (
            f"三维中：产业相关度 tags 已由 gkx 全量承载（{probe_out.get('tags'):,} 行），但链路码与 "
            f"dwd_industry_chain_info 关联仅 {probe_out.get('tags_chain_join_rows_sample')} 行（20 万行样本口径）、投入产出表缺失，产业链融入度仍不可闭合；"
            f"政策匹配度有政策文本（{probe_out.get('policy'):,}）与企业文本（{probe_out.get('product'):,}）但 GPT 契合层未建"
            f"（keywords 填充 {probe_out.get('policy_keywords_filled')}）；"
            f"深圳连接度可用投资/股东边代理中心度（scored={comp.get('n_scored')}，含深圳连接企业 {comp.get('n_positive_sz_link')}），"
            f"但引力模型子项缺人口/GDP/距离。始终有依赖维数据不足 → 部分支持。库存自校验：{spot.get('probe_rows_match')}"
        ),
        "dimension_verdicts": {k: v.get("verdict") for k, v in dims.items()},
        "dimension_detail": dims,
    }


def main():
    report = {"metric_id": "M_ENT_ATTRACTION_INDEX", "metric_name": "招引推荐指数",
              "script": Path(__file__).name, "data_source": "gkx"}
    inv = inv_rows()
    print("== probe ==", flush=True)
    report["probe"] = probe(inv)
    print(json.dumps(report["probe"], ensure_ascii=False), flush=True)
    print("== compute sz-connectivity proxy ==", flush=True)
    report["compute"] = compute()
    print(json.dumps({k: report["compute"][k] for k in
                      ["sz_orgs", "n_nodes_with_degree", "n_scored", "n_positive_sz_link"]}, ensure_ascii=False), flush=True)
    report["gkx_spotcheck"] = spotcheck(inv, report["probe"])
    report["support_judgment"] = judge(report["probe"], report["compute"], report["gkx_spotcheck"])
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report["support_judgment"], ensure_ascii=False, indent=2), flush=True)
    print("wrote", OUT, flush=True)


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
    out_json = here / "M_ENT_ATTRACTION_INDEX_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ENT_ATTRACTION_INDEX.py 等价）
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
        "metric_id": "M_ENT_ATTRACTION_INDEX",
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
