#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_RECOMMEND_COUNT · 推荐企业数（20261021 换源版）

旧稿公式（照抄）
----------------
招引推荐企业数 = COUNT(DISTINCT org_id) WHERE attraction_index >= 70
培育推荐企业数 = COUNT(DISTINCT org_id) WHERE cultivation_index >= 70
两场景不合并；无分企业不进分子（不按 0 分处理）；只国内；阈值 70 可参数化。

换源后的硬事实
--------------
1. 招引指数可复算：`dwd_org_base_info`（95,600 家，city 定深圳）+
   `dwd_org_invest_info`（46,967 边）+ `dwd_org_shareholder_info`（400,286 边）。
   上游 `M_ENT_ATTRACTION_INDEX_out.json` 只落了 top10，本件重新算全量度中心度，
   并核对最大值与上游一致（0.561416），证明同一公式。
2. **标度不对**：上游分数是 `100×deg_sz/(n-1)`，分母是 95,652 个节点，
   最大值只有 0.561416，不是 0—100。阈值 70 在原始标度上永远不可达，
   直接计数恒为 0。本件同时给三种读数：
     strict_raw      = count(score_raw >= 70)            → 0（标度未达标）
     rescaled_max100 = count(score_raw/max*100 >= 70)    → 按最大值拉到 0—100
     top_decile      = 仅供对照，**不作为口径**（口径禁止 TOP N 冒充 70）
3. 培育指数**没有企业级分数**：上游 `_out.json` 只有三维成熟度评估，
   没有 compute、没有 scores；故培育推荐企业数 = null（不可计算），不是 0。

输出：`code/M_ENT_RECOMMEND_COUNT_out.json`
"""
from __future__ import annotations

import json
import statistics
import time
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent

ATTR = HERE / "M_ENT_ATTRACTION_INDEX_out.json"
CULT = HERE / "M_ENT_CULTIVATION_INDEX_out.json"
ORGBASE = HERE / "_snapshots21" / "cityfam_orgbase_20261021.json"
EDGES = HERE / "_snapshots21" / "ent_edges_20261021.json"
OUT = HERE / "M_ENT_RECOMMEND_COUNT_out.json"
METRIC = "M_ENT_RECOMMEND_COUNT"
NAME = "推荐企业数"
THRESHOLD = 70.0


def main() -> None:
    t0 = time.time()
    attr = json.loads(ATTR.read_text(encoding="utf-8"))
    cult = json.loads(CULT.read_text(encoding="utf-8"))
    base = json.loads(ORGBASE.read_text(encoding="utf-8"))
    edges = json.loads(EDGES.read_text(encoding="utf-8"))

    city = {r[0]: (r[2] or "") for r in base if r[0]}
    name = {r[0]: (r[1] or "") for r in base if r[0]}
    sz = {o for o, c in city.items() if "深圳" in c}

    inv = edges["invest"]
    sh = edges["shareholder"]
    deg = defaultdict(int)
    deg_sz = defaultdict(int)
    for o, j in list(inv) + list(sh):
        if not o or not j:
            continue
        deg[o] += 1
        deg[j] += 1
        if j in sz:
            deg_sz[o] += 1
        if o in sz:
            deg_sz[j] += 1
    n_nodes = len(deg)
    scores = {o: 100.0 * deg_sz[o] / (n_nodes - 1) for o in deg} if n_nodes > 1 else {}
    vals = sorted(scores.values())
    vmax = max(vals) if vals else None

    declared = attr["compute"]["score_stats"]["max"]
    strict = [o for o, s in scores.items() if s >= THRESHOLD]
    rescaled = {o: (s / vmax * 100 if vmax else 0) for o, s in scores.items()}
    resc_hit = sorted([(o, s) for o, s in rescaled.items() if s >= THRESHOLD],
                      key=lambda kv: -kv[1])
    top10 = sorted(scores.items(), key=lambda kv: -kv[1])[:10]
    top10_resc = [(o, round(rescaled[o], 2)) for o, _ in top10]

    above = {t: sum(1 for v in vals if v >= t) for t in (0.1, 0.2, 0.3, 0.4, 0.5, 0.7)}
    cult_has_scores = "compute" in cult or "scores" in cult

    report = {
        "metric_id": METRIC,
        "metric_name": NAME,
        "date": "2026-10-22",
        "data_source": (
            "gkx @ 183.240.141.251:3318（只读）：dwd_org_base_info + dwd_org_invest_info + "
            "dwd_org_shareholder_info；上游 M_ENT_ATTRACTION_INDEX_out.json / "
            "M_ENT_CULTIVATION_INDEX_out.json"
        ),
        "formula": "count(DISTINCT org_id) WHERE index >= 70；招引/培育分开，不 UNION；无分不进分子",
        "threshold": THRESHOLD,
        "scale_finding": {
            "declared_max": declared,
            "recomputed_max": round(vmax, 6) if vmax else None,
            "max_match": (abs(declared - vmax) < 1e-5) if vmax is not None else None,
            "declared_scale": "0—1（实际是 100×deg/(n−1)，n=95,652）",
            "required_scale": "0—100",
            "strict_threshold_reachable": bool(vmax and vmax >= THRESHOLD),
            "rescaled_threshold_raw": round(0.7 * vmax, 6) if vmax else None,
        },
        "attraction": {
            "count_strict_raw": len(strict),
            "count_rescaled_max100": len(resc_hit),
            "rescaled_hits": [[o, name.get(o, ""), round(s, 2)] for o, s in resc_hit],
            "n_nodes": n_nodes,
            "n_sz_orgs": len(sz),
            "n_positive": sum(1 for v in vals if v > 0),
            "score_stats_raw": {
                "min": round(vals[0], 6) if vals else None,
                "max": round(vals[-1], 6) if vals else None,
                "mean": round(statistics.mean(vals), 8) if vals else None,
                "median": round(statistics.median(vals), 8) if vals else None,
            },
            "count_above_raw": above,
            "top10_raw": [[o, name.get(o, ""), round(s, 6), deg[o], deg_sz[o]] for o, s in top10],
            "top10_rescaled": top10_resc,
            "top_decile_count_for_reference_only": max(1, n_nodes // 10),
        },
        "cultivation": {
            "index_has_enterprise_scores": cult_has_scores,
            "count": None,
            "reason": (
                "上游 M_ENT_CULTIVATION_INDEX_out.json 无 compute/scores 字段，"
                "只做了产业相关度/政策匹配度/企业潜力三维成熟度评估；"
                "没有企业级分数就不能过阈，null ≠ 0。"
            ),
        },
        "primary_result": {
            "attraction_recommend_count": len(strict),
            "cultivation_recommend_count": None,
            "read_as": (
                "招引 0 是「标度未达 70」的可计算空值；若把最大值线性拉到 100，"
                f"有 {len(resc_hit)} 家过线。培育为 null，表示上游未出分，"
                "不得读成「没有可培育企业」。"
            ),
            "publishable": False,
        },
        "probes": {
            "base_orgs": len(base),
            "invest_edges": len(inv),
            "shareholder_edges": len(sh),
            "n_nodes_with_degree": n_nodes,
            "declared_n_scored": attr["compute"].get("n_scored"),
            "declared_max": declared,
            "recomputed_max": round(vmax, 6) if vmax else None,
            "elapsed_sec": round(time.time() - t0, 1),
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": (
                f"计数链路可跑通：{n_nodes:,} 个节点有度中心度，去重键 org_id 齐备，"
                f"重算最大值 {round(vmax,6) if vmax else '—'} 与上游 {declared} 一致；"
                f"但阈值 70 在原始 0—1 标度上不可达（最大 {round(vmax,4) if vmax else '—'}），"
                f"严格计数只能得 0；按最大值拉到 0—100 才有 {len(resc_hit)} 家过线，"
                "这一步是标度修复、需甲方确认；"
                "培育指数完全没有企业级分数，只能输出 null。"
                "上游只覆盖有投资/股东边的企业，未建边的企业不参与，属覆盖缺口。"
                "故判部分支持，且拒绝把 0 当业务结论。"
            ),
            "criteria": {
                "count_logic_executable": True,
                "dedup_key_present": True,
                "attraction_scores_available": True,
                "cultivation_scores_available": cult_has_scores,
                "threshold_reachable_raw": bool(vmax and vmax >= THRESHOLD),
                "rescaled_hits": len(resc_hit),
                "publishable": False,
            },
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "本指标是截面阈值计数：度中心度由当前投资/股东边一次性算出，"
            "上游指数与口径均无年度键、无年份窗口，不存在年度分母；"
            "used/missing 为空表示无年度基期，不是「缺年按 0 摊入」。"
        ),
        "sources": [
            {"table": "gkx.dwd_org_base_info", "rows": len(base), "role": "深圳企业集合"},
            {"table": "gkx.dwd_org_invest_info", "rows": len(inv), "role": "投资边"},
            {"table": "gkx.dwd_org_shareholder_info", "rows": len(sh), "role": "股东边"},
            {"path": "code/M_ENT_ATTRACTION_INDEX_out.json", "role": "上游招引指数（top10 + 统计量）"},
            {"path": "code/M_ENT_CULTIVATION_INDEX_out.json", "role": "上游培育指数（无企业分）"},
        ],
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print("nodes", n_nodes, "max", vmax, "declared", declared,
          "strict", len(strict), "rescaled", len(resc_hit))
    print("resc hits", [(o, name.get(o, ""), round(s, 2)) for o, s in resc_hit])
    print("elapsed", round(time.time() - t0, 1))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
