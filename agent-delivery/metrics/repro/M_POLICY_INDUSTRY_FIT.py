#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""产业适配性（M_POLICY_INDUSTRY_FIT）——只读快照。

正本口径：`gkx-orchestration/agent-delivery/metrics/calc-logic/POLICY/M_POLICY_INDUSTRY_FIT.md`
  入集：国内政策库全部「有效」政策（本库 status 恒真、expire_date 全空 → 等价全表 20,000）；
        对比单位是城市；**国家级政策可计入每个对比市**。
  三维：
    匹配   = N_c / M_c × 100%      （M_c = 该市全部有效政策数，禁止 N_c/N_c）
    覆盖   = 被点到的环节数 / 该链环节总数 × 100%
    细分   = 点到环节名的政策数 / N_c × 100%
  合成：各维截面 min-max 到 [0,1]，缺维不进平均，等权 ×100；N<3 标「样本不足」。

本件的两处落地约束（都写进 MD §2.5，不藏在脚本里）：
  1. 「点到」= `title`/`keywords`/`keypoints`/`theme` 子串命中；实测后三个字段全空，
     等价于只判 `title`。
  2. 细分维的分子（点到环节名的政策数）与本维分母 N_c（点到链名的政策数）不是同一母体：
     环节名匹配不做链锚定，分子可能大于分母。按 DATA_FACTS §3.54，凡分子>分母的格子
     该维一律判「母体不一致、不进平均」，不修改分子去凑比率。

输入：code/_snapshots21/policy_industry_20261023.json
      code/_snapshots21/policy_struct_20261023.json
输出：code/M_POLICY_INDUSTRY_FIT_out.json
"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

HERE = Path(__file__).parent
IND = HERE / "_snapshots21" / "policy_industry_20261023.json"
STRUCT = HERE / "_snapshots21" / "policy_struct_20261023.json"
OUT = HERE / "M_POLICY_INDUSTRY_FIT_out.json"

METRIC = "M_POLICY_INDUSTRY_FIT"
BASKET = ["深圳市", "北京市", "上海市", "广州市", "杭州市", "南京市",
          "合肥市", "成都市", "武汉市", "西安市"]


def minmax(vals: list[float]) -> list[float]:
    lo, hi = min(vals), max(vals)
    if hi - lo < 1e-12:
        return [0.5 for _ in vals]
    return [(v - lo) / (hi - lo) for v in vals]


def main() -> int:
    ind = json.loads(IND.read_text(encoding="utf-8"))
    st = json.loads(STRUCT.read_text(encoding="utf-8"))
    ov = ind["overall"]
    level4 = ov["level4_rows"]

    chains_out = []
    for c in ind["chains"]:
        cc = c["chain_code"]
        cells = []
        for city in BASKET:
            city_rows = ind["city_totals"].get(city)
            if city_rows is None:
                continue
            m_c = city_rows + level4                     # 国家级计入每个对比市
            n_city = ind["city_chain_t0"].get(city, {}).get(cc, 0)
            n_nat = ind["national_chain_t0"].get(cc, 0)
            n_c = n_city + n_nat
            if n_c == 0:
                continue
            nodes_hit_city = ind["city_chain_node_cov"].get(city, {}).get(cc, {}).get(
                "nodes_hit", 0)
            node_pol_city = ind["city_chain_node_policy"].get(city, {}).get(cc, 0)
            node_pol_nat = ind["national_chain_node_policy"].get(cc, 0)
            fine_num = node_pol_city + node_pol_nat
            cells.append({
                "city": city,
                "city_rows": city_rows,
                "national_rows": level4,
                "M_c": m_c,
                "N_c_city": n_city,
                "N_c_national": n_nat,
                "N_c": n_c,
                "match_pct": round(n_c / m_c * 100, 4),
                "coverage_num": nodes_hit_city,
                "coverage_den": c["nodes_total"],
                "coverage_pct": round(nodes_hit_city / c["nodes_total"] * 100, 4)
                if c["nodes_total"] else None,
                "fine_num": fine_num,
                "fine_den": n_c,
                "fine_pct": round(fine_num / n_c * 100, 4),
                "fine_basis_ok": fine_num <= n_c,
            })

        rec = {
            "chain_code": cc,
            "chain_name": c["chain_name"],
            "nodes_total": c["nodes_total"],
            "policies_hit_t0": c["policies_hit_t0"],
            "cities_in_matrix": len(cells),
            "cities_with_local_hits": sum(1 for x in cells if x["N_c_city"] > 0),
            "cells": cells,
            "status": None,
            "score_by_city": {},
        }
        if rec["cities_with_local_hits"] < 3:
            rec["status"] = "样本不足（本地命中城市 < 3）"
            rec["dims_used"] = []
        else:
            dims_used = []
            norm = {}
            if len({x["match_pct"] for x in cells}) >= 1:
                dims_used.append("match")
                norm["match"] = minmax([x["match_pct"] for x in cells])
            if len({x["coverage_pct"] for x in cells}) >= 1:
                dims_used.append("coverage")
                norm["coverage"] = minmax([x["coverage_pct"] for x in cells])
            if all(x["fine_basis_ok"] for x in cells):
                dims_used.append("fine")
                norm["fine"] = minmax([x["fine_pct"] for x in cells])
            rec["status"] = "可算"
            rec["dims_used"] = dims_used
            for i, cell in enumerate(cells):
                parts = [norm[d][i] for d in dims_used]
                cell["dims_used"] = dims_used
                cell["score"] = round(sum(parts) / len(parts) * 100, 4) if parts else None
                rec["score_by_city"][cell["city"]] = cell["score"]
        chains_out.append(rec)

    scored = [c for c in chains_out if c["status"] == "可算"]
    out = {
        "metric_id": METRIC,
        "support_judgment": "部分支持",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "截面指标，按城市 × 产业链计，不设年度分母。"
            "入集是库内全部「有效」政策 20,000 条（status 恒真、expire_date 全空，"
            "故「有效」等价于全表）；2023—2024 采集断档不改变截面分母，只在正文说明。"),
        "headline": {
            "policy_total": st["rows"],
            "national_rows": level4,
            "city_rows": ov["city_rows"],
            "city_null_rows": ov["city_null_rows"],
            "chains_total": ind["chain_count"],
            "chains_scored": len(scored),
            "chains_insufficient": len(chains_out) - len(scored),
            "basket_cities": len(BASKET),
            "max_match_pct": max([x["match_pct"] for c in chains_out for x in c["cells"]],
                                 default=None),
            "median_match_pct": round(statistics.median(
                [x["match_pct"] for c in chains_out for x in c["cells"]]), 4)
            if any(c["cells"] for c in chains_out) else None,
            "policies_hit_any_chain": ov["policies_hit_any_t0"],
            "share_any_chain_pct": ov["share_any_t0_pct"],
        },
        "field_support": {
            "fields": ["title", "keywords", "keypoints", "theme"],
            "effective_field": "title",
            "keywords_nonnull": st["elements"]["keywords_nonnull"],
            "keypoints_nonnull": st["elements"]["keypoints_nonnull"],
            "theme_nonnull": st["elements"]["theme_nonnull"],
        },
        "chains": chains_out,
        "national_inclusion": {
            "rule": "国家级政策计入每个对比市（M_c 与 N_c 同时加）",
            "national_rows": level4,
            "national_chain_hits": ind["national_chain_t0"],
            "note": "若只算市级政策，M_c 会小 2,174，match_pct 相应放大；两种口径不可混用",
        },
        "checks": [
            {"name": "N_c ≤ M_c（全部格子）",
             "value": max([x["N_c"] - x["M_c"] for c in chains_out for x in c["cells"]],
                          default=-1),
             "expected": 0,
             "ok": all(x["N_c"] <= x["M_c"] for c in chains_out for x in c["cells"])},
            {"name": "城市行 + 无城市行 = 全表",
             "value": ov["city_rows"] + ov["city_null_rows"],
             "expected": st["rows"], "ok": ov["city_rows"] + ov["city_null_rows"] == st["rows"]},
            {"name": "链级命中政策 ⊆ 全表", "value": ov["policies_hit_any_t0"],
             "expected": st["rows"], "ok": ov["policies_hit_any_t0"] <= st["rows"]},
        ],
        "provenance": {
            "snapshots": ["code/_snapshots21/policy_industry_20261023.json",
                          "code/_snapshots21/policy_struct_20261023.json"],
            "builders": ["code/_build_policy_industry_20261023.py",
                         "code/_build_policy_struct_20261023.py"],
            "calc_logic": ("gkx-orchestration/agent-delivery/metrics/calc-logic/POLICY/"
                           "M_POLICY_INDUSTRY_FIT.md"),
            "source": ind["source"],
        },
        "notes": [
            "20,000 条里 9,706 条无城市（含 2,174 条国家级），城市级分母不能用 20,000。",
            "细分维分子不做链锚定，凡分子>分母的格子该维判母体不一致、不进平均。",
            "1,261 个环节名的字面匹配会命中 2 字通用名，覆盖维因此是上界。",
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[OK] {OUT}")
    print("scored", len(scored), "/", len(chains_out))
    for c in chains_out:
        print(f"  {c['chain_name']:10s} {c['status']} local={c['cities_with_local_hits']} "
              f"dims={c.get('dims_used')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
