#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
