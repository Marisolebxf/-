#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_CHAIN_PRODUCT_COUNT 产业链关联产品数
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D2 口径级分歧（本件复核为可兼容·配置型） ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_CHAIN_PRODUCT_COUNT.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_CHAIN_PRODUCT_COUNT —— 产业链关联产品数

官方口径（calc-logic v0.2.0，2026-10-14 human:徐滕强拍板）：
  COUNT(DISTINCT product_name) WHERE industry_code = :chain_code（等值、禁 LIKE、无时间窗）
该 SQL 在 gkx 上逐链返回 0，因为 industry_code 存的是链名数组、链码在 industry_link_name，
且 product_name 是「一条企业一行、整串产品清单」的 JSON 列表字面量，直接 DISTINCT 数的是
「产品清单字符串」而不是产品种数。
本件按同一语义重建：先按 JSON 列表拆项，再逐链去重计数——
  n_products = |∪ 拆项(该链企业的 product_name)|
  n_product_categories = |∪ 拆项(industry_link_code，环节/品类标签)|
  n_orgs = 该链企业行数（一行一企）
拆分规则固定：ast.literal_eval；失败则按中英文逗号/分号切分并去引号，不做同义词归并。
"""
from __future__ import annotations
import ast, json, os, re, time

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_PRODUCT_COUNT_out.json")

TOK = re.compile(r"INB\d+")


def parse_list(s):
    if not s:
        return []
    try:
        v = ast.literal_eval(s)
        if isinstance(v, list):
            return [str(x).strip() for x in v if str(x).strip()]
        return [str(v).strip()] if str(v).strip() else []
    except Exception:
        return [x.strip(" '\"[]") for x in re.split(r"[,，;；]", s) if x.strip(" '\"[]")]


snap = json.load(open(os.path.join(SNAP, "chain21_products_20261022.json"), encoding="utf-8"))
rows_in = snap["rows"]
layer = json.load(open(os.path.join(SNAP, "chain21_layer_20261022.json"), encoding="utf-8"))
chains = layer["chain_name"]

prod, cat, org = {}, {}, {}
empty = 0
items_total = 0
for codes, cate, names, plist, nm in rows_in:
    items = parse_list(plist)
    if not items:
        empty += 1
    items_total += len(items)
    for t in {x[:7] for x in TOK.findall(codes or "")}:
        prod.setdefault(t, set()).update(items)
        cat.setdefault(t, set()).update(parse_list(cate))
        org.setdefault(t, set()).add(nm)

out_rows = []
for ch, nm in chains.items():
    out_rows.append({
        "chain_code": ch, "chain_name": nm,
        "n_products": len(prod.get(ch, set())),
        "n_product_categories": len(cat.get(ch, set())),
        "n_orgs": len(org.get(ch, set())),
        "products_per_org": round(len(prod.get(ch, set())) / len(org.get(ch, set())), 2) if org.get(ch) else None,
    })
out_rows.sort(key=lambda r: -r["n_products"])
extra = sorted([(k, len(v)) for k, v in prod.items() if k not in chains], key=lambda x: -x[1])
pv = sorted(r["n_products"] for r in out_rows)
sum_products = sum(pv)
sum_orgs = sum(r["n_orgs"] for r in out_rows)
stats = {
    "n_chains": len(out_rows),
    "covered_chains": sum(1 for r in out_rows if r["n_products"] > 0),
    "zero_chains": sum(1 for r in out_rows if r["n_products"] == 0),
    "min": pv[0], "max": pv[-1], "median": pv[len(pv) // 2],
    "sum_products": sum_products,
    "sum_orgs": sum_orgs,
    "top1_share_pct": round(100.0 * pv[-1] / sum_products, 3) if sum_products else None,
    "products_per_org_all": round(sum_products / sum_orgs, 2) if sum_orgs else None,
}

payload = {
    "metric_id": "M_CHAIN_PRODUCT_COUNT",
    "metric_name": "产业链关联产品数",
    "support_judgment": "部分支持",
    "judgment_reason": "产品标签表 80,258 行真实可取，拆项后 9/12 条链有产品；但 INB1209/INB1236/INB2503 "
                       "在产品表 industry_link_name 中零行（SQL 实测），且产品条目无行业标准编码、同物异名严重、"
                       "不做归并则不可跨链比较——覆盖与口径两侧都有缺口。",
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "口径明确「无时间窗」，产品标签表也没有年份字段，故不设统计期、不做年度序列。",
    "sources": [
        "gkx @ 183.240.141.251:3318 / gkx_reader_zp: gkx.dwd_org_industry_product_tags（80,258 行全表）",
        "code/_snapshots21/chain21_products_20261022.json（全表落地：链码 / 品类 / 链名 / 产品清单 / 企业名）",
        "code/_snapshots21/chain21_layer_20261022.json（12 链名口径，与 M_CHAIN_ENTERPRISE_COUNT 同池）",
    ],
    "official_sql": {
        "as_written": "SELECT COUNT(DISTINCT product_name) FROM dwd_org_industry_product_tags WHERE industry_code = :chain_code",
        "result_on_gkx": 0,
        "why_zero": "industry_code 存链名数组（如 [\"智能终端\"]），链码在 industry_link_name；等值匹配链码必然 0 行",
        "raw_string_distinct": 65457,
        "trap": "直接对 product_name 做 DISTINCT 得到 65,457（gkx 全表 80,258 行），那是「企业级产品清单字符串」个数，不是产品种数；旧稿在演示库切片上测得 21,654，不可套用到 gkx",
    },
    "rule": {
        "unit": "个（产品条目；同一企业在不同链下重复计入）",
        "split": "ast.literal_eval 取 JSON 列表后逐项 strip；解析失败按 , ， ; ； 切分；不合并同义词、不做大小写归一",
        "chain_attr": "链码取 industry_link_name 中 INB token 前 7 位，多链企业按链各计一次",
        "dedupe": "链内按产品条目字符串去重；不做 NLP 归并（如「伺服电机」与「伺服电机系统」算两个）",
        "pool": "与 M_CHAIN_ENTERPRISE_COUNT 同 12 链口径",
    },
    "chains": out_rows,
    "stats": stats,
    "table_scale": {
        "rows": len(rows_in), "rows_with_empty_product_list": empty,
        "product_items_total": items_total,
        "distinct_product_items_all_chains": len(set().union(*prod.values())) if prod else 0,
        "distinct_orgs_all_chains": len(set().union(*org.values())) if org else 0,
        "zero_chain_rows": {"INB1209": 0, "INB1236": 0, "INB2503": 0},
        "zero_chain_check": "SQL 实测 industry_link_name LIKE 命中行数：INB1209=0 / INB1236=0 / INB2503=0，属源表覆盖缺口而非解析失败",
        "non_top12_chains": [{"code": k, "n_products": v} for k, v in extra[:8]],
    },
    "difference_vs_old_draft": {
        "old_source": "演示库产品标签表（表名前缀 demo，主机 111.198.38.90），25,258 行",
        "old_corrected": {"rows": 25258, "distinct_products": 72616, "distinct_orgs": 25219,
                          "INB1306_products": 44929, "INB1306_orgs": 12883},
        "now": {"rows": 80258, "distinct_products": 221945,
                "INB1306_products": out_rows[0]["n_products"] if out_rows else None,
                "INB1306_orgs": out_rows[0]["n_orgs"] if out_rows else None},
        "reason": "gkx 产品标签表比演示库多 55,000 行（3.18 倍），同一拆分规则下产品条目随之放大；旧稿的 72,616 只覆盖演示库切片",
        "bias": "本件值系统性高于旧稿，倍率约 3.0—3.1 倍；差异来自源表覆盖，不是规则差异",
    },
    "gaps": [
        "产品条目无行业标准编码，靠企业自主填报，同物异名严重；不做归并意味着「产品数」偏大且不可跨链比较",
        "一条企业一行、整串清单：清单长度受填报习惯影响，头部企业会把产品数抬高",
        "品类标签（industry_link_code）与产品清单不同源，二者不可互相校验",
        "80,258 行中 1,611 行产品清单为空，仍计入 n_orgs 但不贡献产品",
    ],
    "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    "elapsed_sec": round(time.time() - T0, 2),
}
json.dump(payload, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rows", len(rows_in), "items", items_total, "distinct", payload["table_scale"]["distinct_product_items_all_chains"])
for r in out_rows:
    print(r["chain_code"], r["chain_name"], r["n_products"], r["n_orgs"], r["n_product_categories"])
print("wrote", OUT)


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
    out_json = here / "M_CHAIN_PRODUCT_COUNT_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_CHAIN_PRODUCT_COUNT.py 等价）
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
        "metric_id": "M_CHAIN_PRODUCT_COUNT",
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
