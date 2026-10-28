#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_TECH_HEAT_QUERY · 查询结果·技术热度（20261022 三方库版）

口径（单一，深圳）：
  规模与年度分布的分母是深圳（IPC4 主分类归属性件数，2021—2024）；
  术语命中率来自 code/_snapshots21/anchor_kw_20261021.json 的「40 个 IPC4 × 各 3,000 件」
  关键词抽样（全国词表），只用于估计「域内命中率」，不进入深圳分母，两张表分开列。

计算：
  1) 查询 q → 各域命中率 rate(ipc) = 含 q 的样本文档数 / 该域有效文档数；
  2) 结果集子术语 TF / Share / HHI（在含 q 的样本文档内统计，剔除 q 本身）；
  3) 深圳估算命中件数 = Σ_ipc rate(ipc) × 深圳该域当年件数（逐年 2021—2024）；
  4) 0 命中查询给出兜底建议词（子串回退），用于搜索空结果引导。

零 SQL：只读两个授权缓存。

运行：cd code && python3 M_TECH_HEAT_QUERY.py
"""
from __future__ import annotations

import collections
import json
import os
import pickle
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _tech21_scope as S  # noqa: E402

MID = "M_TECH_HEAT_QUERY"
QUERIES = ["人工智能", "机器学习", "机器人", "新能源", "芯片", "半导体", "无人机", "生物医药", "大模型"]
TOP_N = 20


def load_anchor():
    """40 个 IPC4 × 3,000 件关键词抽样 → {ipc: [term list, ...]}（None 已剔除）。"""
    raw = S._load(S.SNAP / "anchor_kw_20261021.json")
    parsed, none_rows, bad_rows = {}, 0, 0
    for ipc, lst in raw.items():
        out = []
        for s in lst:
            if s is None:
                none_rows += 1
                continue
            try:
                arr = json.loads(s)
            except Exception:  # noqa: BLE001
                bad_rows += 1
                continue
            if not arr:
                none_rows += 1
                continue
            out.append([str(t).strip() for t in arr if str(t).strip()])
        parsed[ipc] = out
    return parsed, none_rows, bad_rows


def load_sz_cells():
    with open(S.SNAP / "patent_scan_20261021.pkl", "rb") as f:
        raw = pickle.load(f)
    cell = collections.Counter()
    for (city, y, ipc), pns in raw["ipc_pn"].items():
        if city != "深圳" or int(y) not in S.COMPLETE_YEARS:
            continue
        cell[(ipc, int(y))] = len(pns)
    return cell


def run_query(q, parsed, sz):
    per_ipc, docs_total = {}, 0
    term_tf = collections.Counter()
    year_est = collections.Counter()
    for ipc, docs in parsed.items():
        hit = [d for d in docs if q in d]
        if not hit:
            continue
        per_ipc[ipc] = len(hit)
        docs_total += len(hit)
        for d in hit:
            for t in set(d):
                if t != q:
                    term_tf[t] += 1
        rate = len(hit) / len(docs) if docs else 0.0
        for y in S.COMPLETE_YEARS:
            est = rate * sz.get((ipc, y), 0)
            if est:
                year_est[y] += est
    # 2024 年件数还原的逐域拆解（正文引用「低命中率×巨域」现象时对得上账）
    decomp = []
    for ipc, hit in per_ipc.items():
        rate = hit / len(parsed[ipc]) if parsed[ipc] else 0.0
        est = rate * sz.get((ipc, 2024), 0)
        if est:
            decomp.append({"ipc4": ipc, "rate": round(rate, 6),
                           "sz_2024": sz.get((ipc, 2024), 0), "est_2024": round(est, 1)})
    decomp.sort(key=lambda r: -r["est_2024"])
    est_total_2024 = sum(r["est_2024"] for r in decomp) or 1.0
    for r in decomp:
        r["share_of_est"] = round(r["est_2024"] / est_total_2024, 4)

    total_tf = sum(term_tf.values())
    shares = {t: c / total_tf for t, c in term_tf.items()} if total_tf else {}
    hhi = sum(v * v for v in shares.values())
    top_terms = [{"term": t, "tf": c, "share": round(c / total_tf, 6) if total_tf else 0.0}
                 for t, c in term_tf.most_common(TOP_N)]
    return {
        "query": q,
        "n_docs_sample": docs_total,
        "n_ipc_hit": len(per_ipc),
        "top_ipc": [{"ipc4": k, "docs": v, "rate": round(v / len(parsed[k]), 6)}
                    for k, v in sorted(per_ipc.items(), key=lambda kv: -kv[1])[:10]],
        "distinct_terms": len(term_tf),
        "total_tf": total_tf,
        "mean_terms_per_doc": round(total_tf / docs_total, 4) if docs_total else 0.0,
        "tf_hhi": round(hhi, 6),
        "top_terms": top_terms,
        "year_est_sz": {str(y): round(year_est[y], 1) for y in S.COMPLETE_YEARS},
        "year_est_total": round(sum(year_est.values()), 1),
        "est_top_2024": decomp[:6],
    }


def fallback(q, vocab):
    """0 命中兜底：用 2 字子串在词表里回退，给出可比候选词（产品侧空结果引导）。"""
    frags = {q[i:i + 2] for i in range(len(q) - 1)} or {q}
    cand = collections.Counter()
    for t, c in vocab.items():
        if any(f in t for f in frags):
            cand[t] += c
    return [{"term": t, "freq": c} for t, c in cand.most_common(8)]


def main():
    parsed, none_rows, bad_rows = load_anchor()
    sz = load_sz_cells()
    vocab = collections.Counter()
    for docs in parsed.values():
        for d in docs:
            for t in set(d):
                vocab[t] += 1

    results = []
    for q in QUERIES:
        r = run_query(q, parsed, sz)
        if r["n_docs_sample"] == 0:
            r["fallback_terms"] = fallback(q, vocab)
        results.append(r)

    ok = [r for r in results if r["n_docs_sample"] > 0]
    zero = [r["query"] for r in results if r["n_docs_sample"] == 0]

    sz_year = collections.Counter()
    for (ipc, y), n in sz.items():
        sz_year[y] += n

    payload = {
        "metric_id": MID,
        "generated_at": "2026-10-22",
        "main_db": "gkx @ 183.240.141.251:3318 (gkx_reader_zp, read-only)",
        "sql_count": 0,
        "caliber": {
            "subject": "深圳（规模与年度分布的分母）",
            "denominator": "深圳 IPC4 主分类归属性件数 2021—2024",
            "sample_role": "40 个 IPC4 × 3,000 件的 keywords 抽样（全国词表），只估域内命中率",
            "match": "JSON 元素精确匹配（不是子串匹配）",
            "tf_definition": "含该术语的命中样本件数（每件每术语计一次）",
            "excluded": "查询词本身从热度榜剔除，单列为查询锚点",
        },
        "base_years_used": list(S.COMPLETE_YEARS),
        "base_years_missing": list(S.MISSING_BASE_YEARS),
        "base_years_note": (
            "年度估算只覆盖库内真实存在的 2021—2024；2017—2020 在 dwd_patent 零行，"
            "不补零、不外推；2025/2026 属采集残年，不进年度矩阵。"),
        "inputs": [
            {"path": "code/_snapshots21/anchor_kw_20261021.json",
             "what": "40 个 IPC4 × 3,000 件 keywords 抽样（120,000 行位）",
             "source": "gkx.dwd_patent @ 183.240.141.251:3318，按 IPC4 分层取 2026-10-22 08:00 前完成"},
            {"path": "code/_snapshots21/patent_scan_20261021.pkl",
             "what": "深圳×年×IPC4 去重 pn 集合（年度与规模分母）",
             "source": "gkx.dwd_patent @ 183.240.141.251:3318，2026-10-21 21:30–23:50 产出"},
        ],
        "coverage": {
            "sample_ipc4": len(parsed),
            "sample_docs": sum(len(v) for v in parsed.values()),
            "null_keyword_rows": none_rows,
            "bad_json_rows": bad_rows,
            "vocab_terms": len(vocab),
            "sz_by_year": {str(y): sz_year[y] for y in S.COMPLETE_YEARS},
        },
        "queries": results,
        "summary": {
            "n_queries": len(results),
            "n_hit": len(ok),
            "n_zero": len(zero),
            "zero_queries": zero,
            "max_docs": max((r["n_docs_sample"] for r in ok), default=0),
            "min_hhi": min((r["tf_hhi"] for r in ok), default=0.0),
            "max_hhi": max((r["tf_hhi"] for r in ok), default=0.0),
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": ("「子标签出现频次 + 出现时间」两要素在专利关键词侧可算（9 个查询里 7 个非空、"
                       "TF/HHI/年度矩阵齐备）；需求另点名的资讯侧三项（资讯数量、发布时间、阅读量）"
                       "在库内零承载，故落部分支持。"),
        },
    }
    S.write_out(MID, payload)
    print(json.dumps({"hit": len(ok), "zero": zero,
                      "docs": {r["query"]: r["n_docs_sample"] for r in results}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
