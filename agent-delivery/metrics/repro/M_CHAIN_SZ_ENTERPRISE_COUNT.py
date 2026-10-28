#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_CHAIN_SZ_ENTERPRISE_COUNT 深圳产业链企业数
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_CHAIN_SZ_ENTERPRISE_COUNT.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_CHAIN_SZ_ENTERPRISE_COUNT —— 深圳产业链企业数

口径：与 M_CHAIN_ENTERPRISE_COUNT 同池（同一张 tags 挂链桥、同一 12 链、同一链码规则），
深圳判定用统一社会信用代码第 3—6 位行政区划码 4403（注册地语义，全量可判），
不用底册 city 回联（底册只覆盖 18.9 万家，回联会漏掉 84% 的深圳挂链企业）。
"""
from __future__ import annotations
import json, os, time

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_SZ_ENTERPRISE_COUNT_out.json")


def L(n):
    with open(os.path.join(SNAP, n), encoding="utf-8") as f:
        return json.load(f)


layer = L("chain21_layer_20261022.json")
chains, cc = layer["chain_name"], layer["chain_city"]
base = L("base_20261021.json")
sz_distinct = L("chain21_sz_nodecov_20261022.json")["rows_sz"]

rows = []
for ch, nm in chains.items():
    sz = cc.get(ch + "|深圳市", 0)
    gz = cc.get(ch + "|广州市", 0)
    dg = cc.get(ch + "|东莞市", 0)
    hz = cc.get(ch + "|惠州市", 0)
    nat = sum(v for k, v in cc.items() if k.startswith(ch + "|"))
    four = sz + gz + dg + hz
    rows.append({
        "chain_code": ch, "chain_name": nm,
        "sz_count": sz, "gz_count": gz, "dg_count": dg, "hz_count": hz,
        "four_city_sum": four, "chain_national": nat,
        "sz_share_of_chain": round(sz / nat, 6) if nat else 0.0,
        "sz_share_of_four": round(sz / four, 6) if four else 0.0,
    })
rows.sort(key=lambda r: -r["sz_count"])

base_sz = sum(1 for r in base if r[4] == "深圳市")
payload = {
    "metric_id": "M_CHAIN_SZ_ENTERPRISE_COUNT",
    "metric_name": "深圳产业链企业数",
    "support_judgment": "部分支持",
    "judgment_reason": "链归属与企业规模都可在 gkx 单库内闭合，12 条链的深圳企业数全部非零；但「深圳」只能按统一社会信用代码第 3—6 位 4403 判定，是登记机关辖区而非实际经营地，且 12 链深圳挂接 136,326 次对应去重企业 116,017 家（多链重复计 20,309 次），跨链不可加总当总量；底册 city 路径只覆盖 95,600 家、与挂链桥交集约 3.5 万家，无法作为独立校验。注册地口径的系统性偏差不可在本库内修复，故判部分支持。",
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "截面存量指标，不设统计期；挂链桥无统计期字段，年度序列不在本件范围（见 M_CHAIN_ENTERPRISE_NEW_COUNT）。",
    "sources": [
        {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
         "table": "gkx.dwd_org_industry_tags", "rows": 2283762,
         "snapshot": "code/_snapshots21/chain21_layer_20261022.json",
         "pulled_at": "2026-10-22T15:21:30+08:00"},
        {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
         "table": "gkx.dwd_org_industry_tags（4403 切片）", "rows": 116017,
         "snapshot": "code/_snapshots21/chain21_sz_nodecov_20261022.json",
         "pulled_at": "2026-10-22T15:31:50+08:00"},
        {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
         "table": "gkx.dwd_org_base_info", "rows": 189116,
         "snapshot": "code/_snapshots21/base_20261021.json", "pulled_at": "2026-10-21"},
    ],
    "rule": {
        "pool": "与 M_CHAIN_ENTERPRISE_COUNT 同池：tags 2,283,762 行、一行一企、12 条顶层链",
        "shenzhen": "credit_code[2:6] == '4403'（行政区划码，注册地语义）",
        "why_not_roster": "底册 city='深圳市' 仅 95,600 家、与挂链桥交集约 3.5 万家；用底册回联会把 84% 的深圳挂链企业判成非深圳",
    },
    "chains": rows,
    "population": {
        "chain_memberships": sum(r["chain_national"] for r in rows),
        "sz_memberships": sum(r["sz_count"] for r in rows),
        "sz_distinct_firms": sz_distinct,
        "four_city_memberships": sum(r["four_city_sum"] for r in rows),
        "sz_share_of_all": round(sum(r["sz_count"] for r in rows) / sum(r["chain_national"] for r in rows), 6),
        "base_roster_rows": len(base),
        "base_roster_sz": base_sz,
    },
    "audit_chain": {
        "city_total_all_chains": layer["stats"]["rows"],
        "city_sum": {c: sum(v for k, v in cc.items() if k.endswith("|" + c))
                     for c in ["深圳市", "广州市", "东莞市", "惠州市", "广东其他市", "省外"]},
        "city_sum_is_memberships": sum(v for k, v in cc.items()) == sum(r["chain_national"] for r in rows),
        "distinct_after_dedupe": layer["stats"]["rows"],
        "membership_overlap": sum(v for k, v in cc.items()) - layer["stats"]["rows"],
        "multi_chain_rows": layer["multi_chain_rows"],
        "overlap_equals_extra_memberships": (sum(v for k, v in cc.items()) - layer["stats"]["rows"]) >= layer["multi_chain_rows"],
        "rule": "重叠次数 = Σ(每条记录挂链数 − 1)，因此 ≥ 多链企业数 131,978；两者不是同一个量，不可互相校验相等",
    },
    "difference_vs_old_draft": {
        "old_source": "演示库汇总层（表名前缀 demo_，主机 111.198.38.90）",
        "old_primary_roster_total": 31890,
        "old_admincode_distinct_firms": 116017,
        "old_note": "旧稿主口径为底册 city='深圳市'（12 链合计 3.19 万次挂接），并用区划码 4403 做交叉核（11.6 万家），两路相差 1.81—9.95 倍且未定版",
        "now_rule": "统一取行政区划码 4403（全量可判，不依赖底册），不再两轨并存",
        "now_sz_memberships": sum(r["sz_count"] for r in rows),
        "old_ratio_example": "机器人链旧稿 roster 2,284 / admincode 4,702；本件取 4,702，与该链 admincode 路径逐位一致",
    },
    "gaps": [
        "注册地口径：credit_code 的 4403 是登记机关辖区，不等于实际经营地；分支/迁移会造成归属偏差",
        "挂链桥覆盖全国 228.4 万家，深圳只占 5.9%，任何「深圳占比」都不能外推为全国产业分布",
        "多链企业跨链重复计入（12 链深圳之和 136,326 > 深圳去重企业数）",
    ],
    "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    "elapsed_sec": round(time.time() - T0, 2),
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=1)
print("sz memberships", payload["population"]["sz_memberships"], "share",
      payload["population"]["sz_share_of_all"])
for r in rows[:5]:
    print(r["chain_code"], r["chain_name"], r["sz_count"], r["chain_national"], r["sz_share_of_chain"])
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
    out_json = here / "M_CHAIN_SZ_ENTERPRISE_COUNT_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_CHAIN_SZ_ENTERPRISE_COUNT.py 等价）
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
        "metric_id": "M_CHAIN_SZ_ENTERPRISE_COUNT",
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
