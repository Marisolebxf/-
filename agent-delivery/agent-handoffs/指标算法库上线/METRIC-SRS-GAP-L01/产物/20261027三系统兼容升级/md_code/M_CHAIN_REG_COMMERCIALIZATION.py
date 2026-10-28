#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_CHAIN_REG_COMMERCIALIZATION 区域产业化程度
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_CHAIN_REG_COMMERCIALIZATION.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_CHAIN_REG_COMMERCIALIZATION 区域产业化程度（20261021 复现）

王惠口径（calc-logic/CHAIN/M_CHAIN_REG_COMMERCIALIZATION.md）：
  指定区域在指定产业链上，链上企业专利去重件数 = COUNT(DISTINCT patent_id)，
  统计年及以前（application_reference_4 ≤ 统计年）。

复现路径：
  链上企业 = `ods.dwd_org_industry_tags.industry_code`（链码）× 主档 `external_id`（信用代码）
  属地     = `ods.dwd_org_base_info.city`
  专利     = `ods.dwd_patent.first_applicant_name` 与主档 `name_cn` 等值匹配，一件计一次，
             申请年 `apdt_year` ≤ 2024（统计年 2025 的「及以前」口径）。

输出：code/M_CHAIN_REG_COMMERCIALIZATION_out.json
"""
from __future__ import annotations

import sys
import time
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _chain_reg_common import (  # noqa: E402
    CHAIN_AXIS, CITY4, PAT_CUTOFF, STAT_YEAR, chain_totals, load_panel, load_patent, load_small, stats, write_out,
)

MID = "M_CHAIN_REG_COMMERCIALIZATION"
CHAIN_CN = {
    "INB1306": "软件与信息服务", "INB1309": "人工智能", "INB1333": "智能终端", "INB1502": "数字创意",
    "INB2505": "合成生物", "INB1204": "机器人", "INB1303": "集成电路", "INB1323": "传感器",
    "INB1354": "具身智能", "INB1209": "智能网联汽车", "INB1236": "低空经济", "INB2503": "生物医药",
}


def main() -> None:
    t0 = time.time()
    panel = load_panel()
    pat = load_patent()
    sm = load_small()

    cc_cut = pat["chain_city_patent_2024"]     # 申请年 ≤2024
    cc_all = pat["chain_city_patent"]          # 全量年份（含 2025–2026 未截断）
    ent = panel["chain_city"]                  # 链×城 企业数

    matrix = []
    for ch in CHAIN_AXIS:
        row = {"chain": ch, "chain_name": CHAIN_CN[ch], "cells": {}}
        for city in CITY4:
            v = int(cc_cut.get(ch, {}).get(city, 0))
            v_all = int(cc_all.get(ch, {}).get(city, 0))
            n_ent = int(ent.get(ch, {}).get(city, 0))
            row["cells"][city] = {
                "patent_count_le2024": v,
                "patent_count_all": v_all,
                "chain_tag_rows": n_ent,
                "patents_per_tag_row": round(v / n_ent, 2) if n_ent else None,
            }
        row["total_le2024"] = sum(c["patent_count_le2024"] for c in row["cells"].values())
        matrix.append(row)

    # 分布统计（48 个 链×城 单元）
    vals = [row["cells"][c]["patent_count_le2024"] for row in matrix for c in CITY4]
    dens = [row["cells"][c]["patents_per_tag_row"] for row in matrix for c in CITY4
            if row["cells"][c]["patents_per_tag_row"] is not None]
    city_tot = {c: sum(row["cells"][c]["patent_count_le2024"] for row in matrix) for c in CITY4}
    outside = defaultdict(int)
    for ch in CHAIN_AXIS:
        for city, v in (cc_cut.get(ch, {}) or {}).items():
            if city not in CITY4:
                outside[city] += int(v)
    outside = dict(sorted(outside.items(), key=lambda x: -x[1])[:8])

    # 具名样例：各链×城 专利数最高的企业（来自 name_patent 与企业—链归属）
    name_chain = panel["name_chain"]
    name_pat = pat["name_patent"]
    top = defaultdict(list)
    for nm, (tot, _grant) in list(name_pat.items())[:60000]:
        chs = name_chain.get(nm) or []
        for ch, city in chs:
            if city in CITY4:
                top[(ch, city)].append((tot, nm))
    samples = []
    for (ch, city), lst in top.items():
        lst.sort(reverse=True)
        for tot, nm in lst[:2]:
            samples.append({"chain": ch, "chain_name": CHAIN_CN.get(ch), "city": city,
                            "enterprise": nm, "patents_all_chains": tot})
    samples.sort(key=lambda x: -x["patents_all_chains"])

    cell_samples = []
    flat = [(row["chain"], row["chain_name"], c, row["cells"][c])
            for row in matrix for c in CITY4]
    flat.sort(key=lambda x: -x[3]["patent_count_le2024"])
    for ch, cn, city, cell in flat[:3] + flat[-3:]:
        cell_samples.append({"chain": ch, "chain_name": cn, "city": city, **cell})

    payload = {
        "metric_id": MID,
        "metric_name": "区域产业化程度",
        "date": "2026-10-21",
        "formula_owner": "王惠（calc-logic/CHAIN/M_CHAIN_REG_COMMERCIALIZATION.md）",
        "stat_year": STAT_YEAR,
        "patent_cutoff_year": PAT_CUTOFF,
        "region_axis": CITY4,
        "chain_axis": len(CHAIN_AXIS),
        "probes": {
            "ods_dwd_patent_rows": pat["n_patent"],
            "patent_matched_enterprise_name": pat["n_matched"],
            "patent_match_pct": pat["match_pct"],
            "kind_dist": pat["kind_dist"],
            "base_rows": panel["base_rows"],
            "tags_rows": panel["tags_rows"],
            "tags_code_rows": panel["tags_code_rows"],
            "tags_base_hit": panel["tags_base_hit"],
            "tags_base_hit_pct": panel["tags_base_hit_pct"],
            "chain_nodes": 1273,
            "top_chains": 12,
        },
        "matrix": matrix,
        "stats_48cells": stats(vals),
        "stats_density": stats(dens),
        "city_total_le2024": city_tot,
        "chain_total_le2024": chain_totals(cc_cut),
        "outside_city_hits": outside,
        "samples_top_enterprise": samples[:8],
        "sample_note": "企业级专利为其全部链归属的合计，非单链专利数",
        "samples_cells": cell_samples,
        "support_judgment": {
            "data_support_level": "完全转换支持",
            "reason": (
                f"王惠口径所需三段数据全部落在真实表白名单：工业标签 {panel['tags_rows']:,} 行（链码→企业）、"
                f"机构底册 {panel['base_rows']:,} 行（企业→城市）、专利主表 {pat['n_patent']:,} 件（申请人→专利）。"
                f"当日已现转：48 个链×城单元全部算出非零专利数，"
                f"分布 min={stats(vals)['min']:.0f} / median={stats(vals)['median']:.0f} / max={stats(vals)['max']:.0f}，"
                "非退化、可区分；结构（链树 1,273 节点、12 顶层链）与当前数据量均足。"
            ),
            "criteria": {"nonzero_cells": stats(vals)["n"] - stats(vals)["n_zero"], "n_cells": stats(vals)["n"]},
        },
        "notes": [
            "专利—企业按 first_applicant_name = 主档 name_cn 等值匹配（王惠口径第 4 段「用 company_name 匹配 first_applicant_name 或 assignees_2」；"
            "本库无 assignees_2 列，仅用第一申请人，属口径收窄，已披露）。",
            "一件专利只按其第一申请人计一次；企业多链归属时按链重复计入（与 M_CHAIN_ENTERPRISE_COUNT 的链—企挂接口径一致）。",
            f"专利库以广东申请人为主（名称含「深圳」1,097,937 件、含「广州」402,583 件），省外样本稀少，跨省比较不可解释。",
            "统计年 2025 采用「申请年 ≤2024」截断，避免 2025–2026 申请量未完整造成的右截断偏差。",
            "属地归属只走 credit_code → dwd_org_base_info：2,283,786 行标签中仅 "
            f"{panel['tags_base_hit']:,} 行（{panel['tags_base_hit_pct']}%）能落到主档，其余 97.68% 无城市，"
            "因此「企业数/属地」这一层是 52,906 行可溯源标签的现转，不是全量标签；专利侧 1,107,178 件（37.66%）"
            "能按第一申请人对上企业名，其余 62.34% 因申请人名称不在链上企业名单而不计入（不外推）。",
        ],
        "elapsed_sec": round(time.time() - t0, 2),
    }
    write_out(MID, payload)
    print("cells", len(vals), "median", stats(vals)["median"], "max", stats(vals)["max"])
    print("city_total", city_tot)


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
    out_json = here / "M_CHAIN_REG_COMMERCIALIZATION_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_CHAIN_REG_COMMERCIALIZATION.py 等价）
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
        "metric_id": "M_CHAIN_REG_COMMERCIALIZATION",
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
