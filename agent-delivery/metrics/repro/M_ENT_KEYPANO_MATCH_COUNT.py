#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_KEYPANO_MATCH_COUNT —— 匹配企业数 2026-10-23

口径真源：`gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_KEYPANO_MATCH_COUNT.md`

    COUNT(DISTINCT org_id)
    WHERE org_id ∈ 重点企业名单
      AND 该企上了该链且 chain 的 node_stage 匹配
    GROUP BY chain_code, node_stage

三条硬约束（正本原文）：
  1. 同一企业同一格多节点 → 去重后仍计 1；跨链各计各的。
  2. 链级合计另 GROUP BY chain_code 再去重；**禁止把各链位 match_count 相加**
     （一企可能跨上中下游）。
  3. 选链 / 选链位 / is_published 都不进口径。

本脚本零 DB，只读共用快照。
产物：code/M_ENT_KEYPANO_MATCH_COUNT_out.json
"""
from __future__ import annotations

from collections import Counter, defaultdict

import _keypano_common as K

OUT = K.HERE / "M_ENT_KEYPANO_MATCH_COUNT_out.json"


def main() -> None:
    base = K.load_base()
    cn = K.chain_names()
    st = base["stats"]
    rows = K.member_rows(base)

    cell = Counter((r["chain_code"], r["node_stage"]) for r in rows)
    per_chain = defaultdict(set)
    per_stage = defaultdict(set)
    for r in rows:
        per_chain[r["chain_code"]].add(r["org_id"])
        per_stage[r["node_stage"]].add(r["org_id"])

    cells = []
    for chain in sorted(per_chain):
        for stage in ("up", "mid", "down"):
            cells.append({
                "chain_code": chain,
                "chain_name": cn.get(chain),
                "node_stage": stage,
                "node_stage_cn": K.STAGE_CN[stage],
                "match_count": cell.get((chain, stage), 0),
                "chain_match_count": len(per_chain[chain]),
                "share_in_chain_pct": K.pct(cell.get((chain, stage), 0), len(per_chain[chain])),
            })

    sum_cells = sum(x["match_count"] for x in cells)
    distinct = len({r["org_id"] for r in rows})
    chain_sum = sum(len(v) for v in per_chain.values())
    stage_sum = sum(len(v) for v in per_stage.values())

    # 交叉校验：所有链位格相加 / 去重企业数 = 平均每人挂几格
    inflation = round(sum_cells / distinct, 4) if distinct else 0.0

    payload = {
        "metric_id": "M_ENT_KEYPANO_MATCH_COUNT",
        "metric_name": "匹配企业数",
        "script": "M_ENT_KEYPANO_MATCH_COUNT.py",
        "data_source": "gkx",
        "grain": "(chain_code, node_stage) → COUNT(DISTINCT org_id)",
        "shared_base": K.shared_base_block(base),
        "probes": {
            "roster_n": st["roster_n"],
            "in_chain_n": st["in_chain_n"],
            "in_chain_pct": st["in_chain_pct"],
            "with_stage_n": st["with_stage_n"],
            "cell_n": len(cell),
            "cell_universe_n": len(per_chain) * 3,
            "empty_cell_n": len(per_chain) * 3 - len(cell),
            "empty_cells": [
                {"chain_code": c, "chain_name": cn.get(c), "node_stage": s,
                 "node_stage_cn": K.STAGE_CN[s]}
                for c in sorted(per_chain) for s in ("up", "mid", "down")
                if cell.get((c, s), 0) == 0
            ],
            "sum_of_cells": sum_cells,
            "distinct_firm_n": distinct,
            "cell_to_firm_ratio": inflation,
            "chain_level_sum": chain_sum,
            "chain_level_sum_pct_of_roster": K.pct(chain_sum, st["roster_n"]),
            "stage_level": [
                {"node_stage": s, "node_stage_cn": K.STAGE_CN[s],
                 "firm_n": len(per_stage[s]),
                 "share_in_roster_pct": K.pct(len(per_stage[s]), st["roster_n"])}
                for s in ("up", "mid", "down")
            ],
            "stage_level_sum": stage_sum,
            "stage_overlap_n": stage_sum - distinct,
            "max_cell": max(cells, key=lambda x: x["match_count"]),
            "min_nonzero_cell": min((x for x in cells if x["match_count"]),
                                    key=lambda x: x["match_count"]),
            "multi_chain_firm_n": st["multi_chain_n"],
            "roster_province_n": len({f.get("province") for f in base["firms"]}),
            "roster_city_n": len({f.get("city") for f in base["firms"]}),
        },
        "probes_negative": base["negative_evidence"],
        "result": {
            "cells": cells,
            "chain_level": [
                {"chain_code": k, "chain_name": cn.get(k), "match_count": len(v),
                 "share_in_roster_pct": K.pct(len(v), st["roster_n"])}
                for k, v in sorted(per_chain.items(), key=lambda x: -len(x[1]))
            ],
            "top_cells": sorted(cells, key=lambda x: -x["match_count"])[:10],
            "anti_pattern": {
                "wrong_total": sum_cells,
                "right_total": distinct,
                "why": "31 个链位格相加得 5,196，是「人×链位」；去重企业只有 2,105 家。"
                       "一企可跨链、也可在同一链的上中下游各挂一次，故格子不可加。",
            },
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": (
                "COUNT 本身可以算完：上链边 2,283,762 行在，按 chain×node_stage 去重出 31 个非空格，"
                "去重企业 2,105 家、格内合计 5,196 人次；链级去重 12 条、合计 4,464 对。"
                "但分子两端都不是库里的现成事实：①重点名单不存在——280 张表八个名单模式"
                "扫描只命中新闻表，只能用专利授权≥50 的 4,561 家代理，命中率 50.2302% 是"
                "「代理名单的上链率」，不是「重点企业上链率」；②链位不存在——"
                "industry_tags 无 node_stage、chain_info.level 全 0，上中下游是自建映射。"
                "两维都靠自建，故判部分支持。"
            ),
            "criteria": {
                "count_formula_executable": True,
                "roster_table_exists": False,
                "roster_is_proxy": True,
                "node_stage_column_exists": False,
                "stage_is_self_mapped": True,
                "cells_additive": False,
            },
        },
        **K.base_years_block(),
    }
    K.dump(OUT, payload)


if __name__ == "__main__":
    main()
