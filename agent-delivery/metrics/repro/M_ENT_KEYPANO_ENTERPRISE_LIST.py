#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ENT_KEYPANO_ENTERPRISE_LIST 企业清单
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ENT_KEYPANO_ENTERPRISE_LIST.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_ENT_KEYPANO_ENTERPRISE_LIST —— 企业清单（当前链位）2026-10-23

口径真源：`gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_KEYPANO_ENTERPRISE_LIST.md`
  成员 = (org_id, chain_code, node_stage)
  WHERE org_id ∈ 重点名单 AND 上了该链且 node_stage 匹配
「二次 STAT」：输出成员行，不是 COUNT。名称/区域/资质只在查询时 JOIN，不进主键。

本脚本只读 `code/_snapshots21/keypano_base_20261023.json`（由
`_build_keypano_base_20261023.py` 连库扫一次 + `_enrich_keypano_base_20261023.py`
离线补维），零 DB 访问。

产物：
  code/M_ENT_KEYPANO_ENTERPRISE_LIST_out.json          汇总 + 31 个格子的分布
  code/_snapshots21/keypano_enterprise_list_20261023.json  5,196 行成员明细（旁挂）
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

import _keypano_common as K

OUT = K.HERE / "M_ENT_KEYPANO_ENTERPRISE_LIST_out.json"
SIDE = K.SNAP / "keypano_enterprise_list_20261023.json"


def main() -> None:
    base = K.load_base()
    cn = K.chain_names()
    p, c, a = K.admin_names()
    st = base["stats"]
    rows = K.member_rows(base)

    cell = Counter((r["chain_code"], r["node_stage"]) for r in rows)
    chain_level = Counter(r["chain_code"] for r in rows)
    chain_distinct = defaultdict(set)
    for r in rows:
        chain_distinct[r["chain_code"]].add(r["org_id"])
    chain_distinct_n = {k: len(v) for k, v in chain_distinct.items()}
    firm_chains = Counter(cn_ for f in base["firms"] for cn_ in f.get("chains") or [])

    # 成员明细旁挂（进 out.json 会把产物撑到 1 MB 以上，数字反而难审计）
    side = {
        "metric_id": "M_ENT_KEYPANO_ENTERPRISE_LIST",
        "grain": "org_id + chain_code + node_stage",
        "row_n": len(rows),
        "rows": rows,
    }
    K.dump(SIDE, side)

    cells = []
    for chain in sorted(firm_chains):
        for stage in ("up", "mid", "down"):
            n = cell.get((chain, stage), 0)
            cells.append({
                "chain_code": chain,
                "chain_name": cn.get(chain),
                "node_stage": stage,
                "node_stage_cn": K.STAGE_CN[stage],
                "member_n": n,
                "chain_member_firm_n": chain_distinct_n.get(chain, 0),
                "share_in_chain_pct": K.pct(n, chain_distinct_n.get(chain, 0)),
            })

    # 一家企业可能在同一链的上游与下游各挂一个节点 → 链位行数之和 ≠ 链级去重数
    sum_cells = sum(x["member_n"] for x in cells)
    distinct_firms = len({r["org_id"] for r in rows})
    multi_stage_firms = sum(
        1 for f in base["firms"]
        if any(len(v) > 1 for v in (f.get("chain_stages") or {}).values())
    )

    payload = {
        "metric_id": "M_ENT_KEYPANO_ENTERPRISE_LIST",
        "metric_name": "企业清单（当前链位）",
        "script": "M_ENT_KEYPANO_ENTERPRISE_LIST.py",
        "data_source": "gkx",
        "grain": "(org_id, chain_code, node_stage)",
        "shared_base": K.shared_base_block(base),
        "probes": {
            "roster_n": st["roster_n"],
            "roster_in_base_n": st["roster_in_base_n"],
            "in_chain_n": st["in_chain_n"],
            "in_chain_pct": st["in_chain_pct"],
            "with_l1_n": st["with_l1_n"],
            "with_stage_n": st["with_stage_n"],
            "in_chain_without_stage_n": st["in_chain_n"] - st["with_stage_n"],
            "member_row_n": len(rows),
            "member_firm_n": distinct_firms,
            "member_chain_n": len(firm_chains),
            "member_cell_n": len(cell),
            "cell_universe_n": len(firm_chains) * 3,
            "empty_cell_n": len(firm_chains) * 3 - len(cell),
            "multi_stage_firm_n": multi_stage_firms,
            "sum_of_cells": sum_cells,
            "chain_pair_n": sum(chain_distinct_n.values()),
            "member_row_minus_pair_n": len(rows) - sum(chain_distinct_n.values()),
            "stage_firm_n": dict(sorted(
                ((s, sum(1 for f in base["firms"]
                         if s in set(sum((f.get("chain_stages") or {}).values(), []))))
                 for s in ("up", "mid", "down")))),
            "cell_dist": {
                "max": max((x["member_n"] for x in cells), default=0),
                "min_nonzero": min((x["member_n"] for x in cells if x["member_n"]), default=0),
                "median_nonzero": sorted(x["member_n"] for x in cells if x["member_n"])[
                    len([x for x in cells if x["member_n"]]) // 2] if any(x["member_n"] for x in cells) else 0,
            },
            "roster_province_n": len({f.get("province") for f in base["firms"]}),
            "roster_city_n": len({f.get("city") for f in base["firms"]}),
            "roster_province_top": Counter(f.get("province") for f in base["firms"]).most_common(5),
            "roster_city_top": Counter(f.get("city") for f in base["firms"]).most_common(8),
        },
        "probes_negative": base["negative_evidence"],
        "result": {
            "cells": cells,
            "chain_level": [
                {"chain_code": k, "chain_name": cn.get(k),
                 "member_firm_n": chain_distinct_n.get(k, 0),
                 "member_row_n": chain_level[k],
                 "share_in_roster_pct": K.pct(chain_distinct_n.get(k, 0), st["roster_n"])}
                for k, v in sorted(chain_level.items(), key=lambda x: -x[1])
            ],
            "top_cells": sorted(
                [x for x in cells if x["member_n"]],
                key=lambda x: -x["member_n"])[:10],
            "sample_rows": rows[:10],
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": (
                "成员表结构可算：上链边（dwd_org_industry_tags，2,283,762 行）在，"
                "链位可由一级环节码映射，区域/资质只在查询时 JOIN，公式可完整执行，"
                "实出 31 个链×链位格、5,196 行成员、2,105 家企业。但两条依赖不可靠："
                "①名单是代理——gkx 280 张表按 keypano/key_/important/focus/star/honor/"
                "roster 八个模式扫描只命中 dwd_org_important_news_info（新闻表，非名单），"
                "没有「重点企业」名单表，只能用专利授权≥50 的 4,561 家代理；"
                "②链位是自建映射——dwd_org_industry_tags 15 列无 node_stage，"
                "dwd_industry_chain_info.level 1,273 行全 0，只能把 41 个一级环节手工"
                "归到上/中/下游。名单与链位两维都不在库里，故判部分支持，不抬档。"
            ),
            "criteria": {
                "roster_table_exists": False,
                "roster_is_proxy": True,
                "node_stage_column_exists": False,
                "stage_is_self_mapped": True,
                "chain_edges_ready": True,
                "region_id_column_exists": False,
            },
        },
        **K.base_years_block(),
    }
    K.dump(OUT, payload)


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
    out_json = here / "M_ENT_KEYPANO_ENTERPRISE_LIST_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ENT_KEYPANO_ENTERPRISE_LIST.py 等价）
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
        "metric_id": "M_ENT_KEYPANO_ENTERPRISE_LIST",
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
