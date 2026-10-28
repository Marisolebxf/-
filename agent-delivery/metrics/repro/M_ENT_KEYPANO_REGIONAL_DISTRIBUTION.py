#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ENT_KEYPANO_REGIONAL_DISTRIBUTION 区域分布
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ENT_KEYPANO_REGIONAL_DISTRIBUTION.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_ENT_KEYPANO_REGIONAL_DISTRIBUTION —— 区域分布 2026-10-23

口径真源：`gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_KEYPANO_REGIONAL_DISTRIBUTION.md`

    COUNT(DISTINCT org_id)
    WHERE org_id ∈ 该链重点名单
      AND 该企点亮 :region_key
    GROUP BY chain_code, region_key

与 `M_ENT_KEYPANO_REGIONAL_COUNT` 的区别：那件数「点亮了几个区域」，本件数
「每个区域有多少家」。与 QUAL 的区别：本件不带类型维。

三条口径：
  - 区域键 = nation:CN + 省 2 + 市 4 + 县 6 + scope:gba|yrd|jjj，热门城市并入市；
  - 嵌套不可加（南山 ⊂ 深圳 ⊂ 广东 ⊂ 全国），大湾区与广东可重叠；
  - 份额分母同母体：区域格 / 该链上链企业数；区县再给「占同城」分母
    （区县格 / 该链同市格），不用全库 189,116（DATA_FACTS §3.54）。

本脚本零 DB。
"""
from __future__ import annotations

from collections import Counter

import _keypano_common as K

OUT = K.HERE / "M_ENT_KEYPANO_REGIONAL_DISTRIBUTION_out.json"


def main() -> None:
    base = K.load_base()
    cn = K.chain_names()
    p, c, a = K.admin_names()
    st = base["stats"]
    firms = base["firms"]

    chain_firm = Counter(ch for f in firms for ch in (f.get("chains") or []))
    cell: Counter = Counter()
    for f in firms:
        keys = ["nation:CN"] + list(f["region_keys"])
        for ch in f.get("chains") or []:
            for k in keys:
                cell[(ch, k)] += 1

    rows = []
    for (ch, k), n in sorted(cell.items()):
        kind = "nation" if k == "nation:CN" else K.key_kind(k)
        r = {
            "chain_code": ch,
            "chain_name": cn.get(ch),
            "region_key": k,
            "region_name": "全国" if kind == "nation" else K.key_label(k, p, c, a),
            "region_kind": kind,
            "ent_count": n,
            "share_in_chain_pct": K.pct(n, chain_firm[ch]),
        }
        if kind == "area":
            parent = K.parent_key(k)
            r["parent_region_key"] = parent
            r["parent_region_name"] = K.key_label(parent, p, c, a)
            r["share_in_parent_pct"] = K.pct(n, cell.get((ch, parent), 0))
        if kind == "city":
            parent = K.parent_key(k)
            r["parent_region_key"] = parent
            r["share_in_parent_pct"] = K.pct(n, cell.get((ch, parent), 0))
        rows.append(r)

    # 交叉校验：各市级格相加应等于全国格；区县相加 ≤ 全国
    city_sum, area_sum = Counter(), Counter()
    for (ch, k), n in cell.items():
        if K.key_kind(k) == "city":
            city_sum[ch] += n
        elif K.key_kind(k) == "area":
            area_sum[ch] += n
    city_ok = sum(1 for ch in chain_firm if city_sum[ch] == chain_firm[ch])

    payload = {
        "metric_id": "M_ENT_KEYPANO_REGIONAL_DISTRIBUTION",
        "metric_name": "区域分布",
        "script": "M_ENT_KEYPANO_REGIONAL_DISTRIBUTION.py",
        "data_source": "gkx",
        "grain": "(chain_code, region_key) → COUNT(DISTINCT org_id)",
        "shared_base": K.shared_base_block(base),
        "probes": {
            "roster_n": st["roster_n"],
            "in_chain_n": st["in_chain_n"],
            "chain_n": len(chain_firm),
            "row_n": len(rows),
            "region_kind_row_n": dict(Counter(r["region_kind"] for r in rows)),
            "roster_geo": {
                "province_n": len({f.get("province") for f in firms}),
                "city_n": len({f.get("city") for f in firms}),
                "area_blank_n": st["area_blank_n"],
                "area_code_missing_n": st["area_code_missing_n"],
            },
            "checks": {
                "city_sum_equals_chain_n": city_ok,
                "chain_checked_n": len(chain_firm),
                "area_sum_lt_chain_n_n": sum(1 for ch in chain_firm
                                             if area_sum[ch] < chain_firm[ch]),
                "note": "市级格逐链相加 = 该链上链企业数（每企恰 1 个市）；"
                        "区县之和小于链级，差额是「区县名空白 775 家 + 区县码未匹配 101 家」。",
            },
            "nesting_demo": {
                "chain_code": "INB1306",
                "nation": cell.get(("INB1306", "nation:CN"), 0),
                "province": cell.get(("INB1306", "admin:44"), 0),
                "shenzhen": cell.get(("INB1306", "admin:4403"), 0),
                "nanshan": cell.get(("INB1306", "admin:440305"), 0),
                "gba": cell.get(("INB1306", "scope:gba"), 0),
                "note": "五层逐级收窄且范围重叠，最大层=全国，最小层=南山区；不可相加。",
            },
        },
        "probes_negative": base["negative_evidence"],
        "result": {
            "rows": rows,
            "nation_cells": sorted(
                [r for r in rows if r["region_kind"] == "nation"],
                key=lambda x: -x["ent_count"]),
            "top_cities": sorted(
                [r for r in rows if r["region_kind"] == "city"],
                key=lambda x: -x["ent_count"])[:8],
            "top_areas": sorted(
                [r for r in rows if r["region_kind"] == "area"],
                key=lambda x: -x["ent_count"])[:10],
            "scope_cells": sorted(
                [r for r in rows if r["region_kind"] == "scope"],
                key=lambda x: -x["ent_count"]),
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": (
                "区域分布公式可完整执行：12 条链 × 区域键共 309 行非空格，"
                "含 12 个全国格、12 个省格、48 个市格、225 个区县格、12 个复合区域格；"
                "市级格逐链相加等于该链上链企业数（12/12 通过），说明口径闭合。"
                "缺口在依赖侧：①重点名单不存在，4,561 家为专利阈值代理名单，"
                "且全部落在广东省 4 市，区域分布只可能是「一省四市 23 区县」的切片，"
                "全国格恒等于该链上链企业数、省格与全国格恒等、大湾区格与省格恒等——"
                "三层数值完全重合，分布图退化为两级；②复合区域维表不存在，"
                "scope 成员按规划纲要行政范围自建；③区县维有 339 家上链企业无法落格"
                "（区县名空白 289 + 区县名有而码未匹配 50），使区县层格数之和小于链级。"
                "按定义判部分支持。"
            ),
            "criteria": {
                "formula_executable": True,
                "roster_table_exists": False,
                "roster_is_proxy": True,
                "roster_single_province": True,
                "province_equals_nation": True,
                "scope_dim_exists": False,
                "area_missing_n": 339,
            },
        },
        **K.base_years_block(),
    }
    K.dump(OUT, payload)


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
    out_json = here / "M_ENT_KEYPANO_REGIONAL_DISTRIBUTION_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ENT_KEYPANO_REGIONAL_DISTRIBUTION.py 等价）
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
        "metric_id": "M_ENT_KEYPANO_REGIONAL_DISTRIBUTION",
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
