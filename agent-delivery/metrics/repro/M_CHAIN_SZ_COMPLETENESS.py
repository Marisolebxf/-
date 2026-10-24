#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_SZ_COMPLETENESS —— 深圳产业链完整度

口径：完整度 = k / K × 100%
  K = 该顶层链子树内的链树节点数（去根，来自 dwd_industry_chain_info 1,273 节点）
  k = 其中至少 1 家深圳企业（credit_code[2:6]=='4403'）在「该节点或其更深节点」有挂链标签的节点数
节点级而非叶子级：链树里同一环节常分「环节—子环节—品类」三层，逐层都要求有企业才叫配套齐，
只算叶子会把中间层忽略、把完整度抬到 95% 以上（与旧稿 54—99% 的分布不符）。
"""
from __future__ import annotations
import json, os, time

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_SZ_COMPLETENESS_out.json")


def L(n):
    with open(os.path.join(SNAP, n), encoding="utf-8") as f:
        return json.load(f)


cov = L("chain21_sz_nodecov_20261022.json")
layer = L("chain21_layer_20261022.json")
tree = L("chain_tree_20261021.json")
name = {n["industry_code"]: n["industry_name"] for n in tree}
chains = layer["chain_name"]

rows = []
for ch, nm in chains.items():
    v = cov["chains"].get(ch, {})
    K, k = v.get("K_nodes", 0), v.get("k_covered", 0)
    unc = v.get("uncovered_nodes", [])
    rows.append({
        "chain_code": ch, "chain_name": nm,
        "K_nodes": K, "k_sz_covered": k,
        "completeness_pct": round(100.0 * k / K, 2) if K else None,
        "uncovered_nodes": len(unc),
        "uncovered_node_names": [name.get(x, x) for x in unc[:8]],
        "leaf_only_pct": round(100.0 * v.get("k_leaf_covered", 0) / v["K_leaf"], 2) if v.get("K_leaf") else None,
    })
rows.sort(key=lambda r: -r["completeness_pct"])
vals = [r["completeness_pct"] for r in rows]

payload = {
    "metric_id": "M_CHAIN_SZ_COMPLETENESS",
    "metric_name": "深圳产业链完整度",
    "support_judgment": "完全转换支持",
    "judgment_reason": "公式 k/K 的两侧都可在 gkx 内闭合：K 来自 dwd_industry_chain_info 的 1,273 节点链树，k 来自 dwd_org_industry_tags 按 4403 行政区划码切片的 116,017 行挂链记录；12 条链全部算出 57.61%—100%，无空链、无零分母，脚本 0.01 秒可复算。逐链 K 与旧稿完全一致，k 因不再回联 18.9 万行底册而略高（0—4 个节点），属覆盖集差异而非口径变化。",
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "截面存量指标，不设统计期；挂链桥无统计期字段，不做年度序列。",
    "sources": [
        "gkx @ 183.240.141.251:3318 / gkx_reader_zp: gkx.dwd_org_industry_tags（深圳切片 116,017 行）",
        "gkx @ 183.240.141.251:3318 / gkx_reader_zp: gkx.dwd_industry_chain_info（1,273 节点链树）",
        "code/_snapshots21/chain21_sz_nodecov_20261022.json（节点覆盖落盘，2 列 1 次读）",
        "code/_snapshots21/chain21_layer_20261022.json（12 链名与链码口径，与 M_CHAIN_ENTERPRISE_COUNT 同池）",
    ],
    "rule": {
        "K": "该顶层链子树下的全部节点数（不含根本身，来自 gkx.dwd_industry_chain_info 的 1,273 节点链树）",
        "k": "K 中满足「∃ 深圳企业标签 t，t.startswith(node_code)」的节点数",
        "shenzhen": "credit_code[2:6] == '4403'（全量可判；不依赖 18.9 万行底册回联）",
        "rebuild": "code/_snapshots21/chain21_sz_nodecov_20261022.json 由 _work_gkx21/build_sz_nodecov.py 一次读 tags 深圳切片落盘；本脚本只读该快照，不连库",
        "pool": "与 M_CHAIN_ENTERPRISE_COUNT / M_CHAIN_SZ_ENTERPRISE_COUNT 同池同 12 链",
        "provenance": "gkx @ 183.240.141.251:3318 / gkx_reader_zp，tags 深圳切片 116,017 行，拉取于 2026-10-22T15:31:50+08:00",
    },
    "chains": rows,
    "stats": {
        "n": len(vals), "min": min(vals), "max": max(vals),
        "median": round(sorted(vals)[len(vals) // 2], 2),
        "mean": round(sum(vals) / len(vals), 2),
        "n_ge_90": sum(1 for v in vals if v >= 90),
        "n_lt_70": sum(1 for v in vals if v < 70),
    },
    "coverage_source": {"sz_tag_rows": cov["rows_sz"], "distinct_codes_in_sz_slice": cov["distinct_tokens"]},
    "difference_vs_old_draft": {
        "old_source": "演示库汇总层（库名以 demo 打码，表 industry_chain_metric_fact）",
        "old_stats": {"n": 12, "min": 54.35, "max": 98.72, "median": 86.58, "mean": 83.14},
        "old_example": "具身智能 77/78=98.72%，机器人 86/90=95.56%，智能终端 92/97=94.85%（另一路区划码口径 96.91%）",
        "now_example": "具身智能 78/78=100%，机器人 90/90=100%，智能终端 94/97=96.91%",
        "bias": "本件逐链 k 比旧稿主口径多 0—4 个节点，因旧稿主口径先与 18.9 万行底册回联（只留 3.5 万家），漏掉未进底册的深圳挂链企业；k 只会更大、完整度只会更高",
        "conclusion": "K 完全相同（90/97/78 等与旧稿逐链一致），k 的差异可由覆盖集解释，公式与判档不变 → 完全转换支持",
    },
    "gaps": [
        "k 只判「有没有 ≥1 家深圳企业」，不判环节内企业密度；1 家与 1,000 家同权",
        "链树节点由业务侧维护，某些中间层是归组节点而非真实环节，会轻微压低完整度",
        "注册地区划码 4403 ≠ 实际经营地，分支/迁移会误判",
    ],
    "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    "elapsed_sec": round(time.time() - T0, 2),
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=1)
print("stats", payload["stats"])
for r in rows:
    print(r["chain_code"], r["chain_name"], r["k_sz_covered"], r["K_nodes"], r["completeness_pct"])
print("wrote", OUT)
