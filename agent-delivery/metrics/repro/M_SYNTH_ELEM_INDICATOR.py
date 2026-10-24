#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SYNTH_ELEM_INDICATOR —— 要素分项指标值与得分（L0 叶子台账）。

族内第二件（第一件是面板 `_build_synth_elem_panel.py`）。本脚本不连库，只读族级
面板 `code/_snapshots21/synth_elem_panel_20261023.json`，把 17 个类型叶子 + 10 个
领域叶子的原值、归一得分、可用状态摊开，并统计「17 个叶子里几个能进加权」。

运行：cd code && python3 M_SYNTH_ELEM_INDICATOR.py
输出：code/M_SYNTH_ELEM_INDICATOR_out.json
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
PANEL = os.path.join(HERE, "_snapshots21", "synth_elem_panel_20261023.json")
OUT = os.path.join(HERE, "M_SYNTH_ELEM_INDICATOR_out.json")
CST = timezone(timedelta(hours=8))

with open(PANEL, encoding="utf-8") as f:
    P = json.load(f)

CITIES = P["regions"]
LEAVES = P["leaves"]
DLEAVES = P["domain_leaves"]


def distinct_scores(lf):
    vals = [v for v in (lf.get("z") or {}).values() if v is not None]
    return len(set(vals))


def state_stats(leaves):
    st = {}
    for lf in leaves:
        st.setdefault(lf["state"], []).append(lf["id"])
    return {
        "leaf_total": len(leaves),
        "ok": len(st.get("ok", [])),
        "proxy": len(st.get("proxy", [])),
        "degenerate": len(st.get("degenerate", [])),
        "insufficient": len(st.get("insufficient", [])),
        "missing": len(st.get("missing", [])),
        "by_state": st,
    }


type_cov = state_stats(LEAVES)
dom_cov = state_stats(DLEAVES)
weighted_ids = [i for d in P["type"]["dims"].values() for i in d["weighted_leaf_ids"]]
dom_weighted_ids = [i for d in P["domain"]["dims"].values() for i in d["weighted_leaf_ids"]]

# 归一分辨率：4 城极值归一后每个叶子最多 4 个不同得分，必有 100 与 0
res = {lf["id"]: distinct_scores(lf) for lf in LEAVES + DLEAVES}
res_hist = {}
for v in res.values():
    res_hist[str(v)] = res_hist.get(str(v), 0) + 1

ledger = []
for lf in LEAVES:
    raw = lf["raw"]
    vals = [v for v in raw.values() if v is not None]
    ledger.append({
        "id": lf["id"],
        "name": lf["name"],
        "dim": lf["dim"],
        "structure": lf["structure"],
        "unit": lf["unit"],
        "state": lf["state"],
        "raw": raw,
        "z": lf["z"],
        "min": min(vals) if vals else None,
        "max": max(vals) if vals else None,
        "distinct_scores": res[lf["id"]],
        "source": lf["source"],
        "note": lf["note"],
    })

dledger = []
for lf in DLEAVES:
    raw = lf["raw"]
    vals = [v for v in raw.values() if v is not None]
    dledger.append({
        "id": lf["id"],
        "name": lf["name"],
        "dim": lf["dim"],
        "state": lf["state"],
        "raw": raw,
        "z": lf["z"],
        "min": min(vals) if vals else None,
        "max": max(vals) if vals else None,
        "distinct_scores": res[lf["id"]],
        "source": lf["source"],
        "note": lf["note"],
    })

downstream = {
    "type_dims": {d: {"n": v["n"], "leaf_ids": v["weighted_leaf_ids"]}
                  for d, v in P["type"]["dims"].items()},
    "level_structs": {d: {"n": v["n"], "leaf_ids": v["weighted_leaf_ids"]}
                      for d, v in P["level"]["structures"].items()},
    "domain_dims": {d: {"n": v["n"], "leaf_ids": v["weighted_leaf_ids"]}
                    for d, v in P["domain"]["dims"].items()},
}

gaps = [{
    "id": lf["id"], "name": lf["name"], "dim": lf["dim"], "state": lf["state"],
    "source": lf["source"], "note": lf["note"],
} for lf in LEAVES + DLEAVES if lf["state"] in ("missing", "insufficient", "degenerate")]

out = {
    "metric_id": "M_SYNTH_ELEM_INDICATOR",
    "metric_name": "要素分项指标值与得分",
    "support_judgment": "部分支持",
    "verdict_kind": "positive_with_gaps",
    "judgment_reason": (
        "17 个类型叶子中 7 个直读（ok）、5 个代理（proxy）、1 个退化（degenerate）、"
        "1 个样本不足（insufficient）、3 个无承载（missing），进加权 12 个；"
        "7 个类型维中 6 个可算（创新人才维全缺），5 个领域维中 3 个可算。"
        "缺的部分不是覆盖率低，是列建好未灌数（development_employee 0/90,926）"
        "或全库无此列（空间面积/区域面积），故只能判部分支持。"
    ),
    "base_years_used": [2024],
    "base_years_missing": [],
    "base_years_note": (
        "统计年=2024（专利授权、年报、融资完成日、论文、政策存量五类源里唯一完整的年）。"
        "2021—2023 未入集不是缺数，是本族按要求做单年截面；2025 专利与年报尚未完整、"
        "2026 为残年（专利 74,810 件），均不进分母、不按 0 摊。政策叶子是存量口径，"
        "不带年份——按年截断会把覆盖率打成 0（DATA_FACTS §3.7）。"
    ),
    "sources": [
        "gkx @ 183.240.141.251:3318（只读）",
        "code/_snapshots21/synth_elem_panel_20261023.json（本族面板，2026-10-23 构建）",
        "code/_snapshots21/synth_elem_probe_20261023.json（族级探针）",
        "code/_snapshots21/base_20261021.json",
        "code/_snapshots21/patent2024_scan_20261021.json",
        "code/_snapshots21/papers_city_year_gkx21.json",
        "code/_snapshots21/cityfam_scholars_20261021.json",
        "code/_snapshots21/cityfam_hightech_20261021.json",
        "code/_snapshots21/ent_base_geo_20261022.json",
        "code/_snapshots21/svc21_facts_20261022.json",
        "code/_snapshots21/probe_talent21_20261022.json",
    ],
    "panel_snapshot": "code/_snapshots21/synth_elem_panel_20261023.json",
    "script": "code/M_SYNTH_ELEM_INDICATOR.py",
    "regions": CITIES,
    "stat_year": P["stat_year"],
    "generated_at": datetime.now(CST).isoformat(timespec="seconds"),
    "coverage": {
        "type": type_cov,
        "domain": dom_cov,
        "type_weighted_n": len(weighted_ids),
        "type_weighted_share_pct": round(len(weighted_ids) / len(LEAVES) * 100, 4),
        "domain_weighted_n": len(dom_weighted_ids),
        "domain_weighted_share_pct": round(len(dom_weighted_ids) / len(DLEAVES) * 100, 4),
        "type_dims_available": len(P["type"]["available_dims"]),
        "type_dims_total": 7,
        "domain_dims_available": len(P["domain"]["available_dims"]),
        "domain_dims_total": 5,
    },
    "normalization": {
        "method": "min-max over the 4 in-scope cities, scaled to 0-100",
        "distinct_score_hist": dict(sorted(res_hist.items())),
        "note": "4 城极值归一 => 每个叶子最多 4 个不同得分，且必有一城 100、一城 0；"
                "得分只能读作「本批 4 城内的相对位置」，不是绝对水平。",
    },
    "ledger": ledger,
    "domain_ledger": dledger,
    "downstream": downstream,
    "gaps": gaps,
    "layer_scores": {
        "type_index": P["index"]["type_index"],
        "level_index": P["index"]["level_index"],
        "domain_index": P["index"]["domain_index"],
        "elem_index": P["index"]["elem_index"],
    },
    "checks": {
        "leaf_total_matches_panel": len(LEAVES) == type_cov["leaf_total"] == 17,
        "state_sum_equals_total": (type_cov["ok"] + type_cov["proxy"] + type_cov["degenerate"]
                                   + type_cov["insufficient"] + type_cov["missing"]) == type_cov["leaf_total"],
        "domain_state_sum_equals_total": (dom_cov["ok"] + dom_cov["proxy"] + dom_cov["insufficient"]
                                          + dom_cov["missing"]) == dom_cov["leaf_total"],
        "all_z_in_range": P["checks"]["z_range"],
    },
}

with open(OUT, "w", encoding="utf-8") as fo:
    json.dump(out, fo, ensure_ascii=False, indent=1)

print("[INDICATOR] ->", OUT)
print("  type leaves 17 = ok %d / proxy %d / degenerate %d / insufficient %d / missing %d"
      % (type_cov["ok"], type_cov["proxy"], type_cov["degenerate"],
         type_cov["insufficient"], type_cov["missing"]))
print("  weighted type leaves", len(weighted_ids), "| domain", len(dom_weighted_ids))
print("  checks", out["checks"])
