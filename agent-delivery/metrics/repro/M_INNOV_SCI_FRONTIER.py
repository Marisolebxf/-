#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_SCI_FRONTIER · 科学研究前沿性（判：部分支持）

口径真源：`metrics/calc-logic/INNOV/M_INNOV_SCI_FRONTIER.md`（V1.7-20260902）
四子项：研究前沿（共被引网连通簇）/ 热点方向（关键词共现网）/ 时间演变 / 空间分布。

零 SQL：全部读 `_snapshots21/probe_inn21_texts_20261022.json`（782 条施引论文的
被引列表、799 条关键词、100,900 条论文 id 池）与 `_snapshots21/probe_a26_20261022.json`
（62,002 行作者单位）。

运行：python3 code/M_INNOV_SCI_FRONTIER.py
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _tail21_common as T  # noqa: E402

MID = "M_INNOV_SCI_FRONTIER"


def parse_list(raw) -> list[str]:
    if not raw:
        return []
    try:
        d = json.loads(raw)
    except Exception:
        return []
    if isinstance(d, dict):
        return [str(v) for v in d.values()]
    if isinstance(d, list):
        return [str(v) for v in d]
    return []


def main() -> None:
    d = T.texts()
    cite = T.rows_of(d, "cite_join_rows")
    cls = T.rows_of(d, "class_join_rows")
    pool = {r[0] for r in T.rows_of(d, "paper_rows")}
    au = json.loads((T.SNAP / "probe_a26_20261022.json").read_text(encoding="utf-8"))["zh_author"]["rows"]
    author_city: dict[str, set] = defaultdict(set)
    for pid, inst, aff in au:
        c = T.city_of(inst or "") or T.city_of(aff or "")
        if c:
            author_city[pid].add(c)

    # ---------------- 网 A：共被引 ----------------
    cited_total = 0
    cited_in_pool = 0
    node_w = Counter()
    pairs = Counter()
    for pid, cnum, lst, y in cite:
        ids = parse_list(lst)
        cited_total += len(ids)
        ins = [i for i in ids if i in pool]
        cited_in_pool += len(ins)
        uniq = sorted(set(ids))
        for i in uniq:
            node_w[i] += 1
        for i in range(len(uniq)):
            for j in range(i + 1, len(uniq)):
                pairs[(uniq[i], uniq[j])] += 1
    edges_w2 = sum(1 for v in pairs.values() if v >= 2)
    # 连通分量：只保留 w>=2 的边，且两端都在论文池内（否则节点无年份/关键词/单位）
    adj: dict[str, set] = defaultdict(set)
    for (a, b), w in pairs.items():
        if w >= 2 and a in pool and b in pool:
            adj[a].add(b)
            adj[b].add(a)
    seen = set()
    comps = []
    for n in adj:
        if n in seen:
            continue
        stack, comp = [n], []
        seen.add(n)
        while stack:
            x = stack.pop()
            comp.append(x)
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        comps.append(comp)
    comps.sort(key=len, reverse=True)
    in_pool_w2_edges = sum(1 for (a, b), w in pairs.items() if w >= 2 and a in pool and b in pool)

    # ---------------- 网 B：关键词共现 ----------------
    kw_paper = {}
    for pid, kw, y in cls:
        ks = [k.strip() for k in (str(kw or "")).replace("；", ",").replace(";", ",").split(",")
              if k.strip()]
        kw_paper[pid] = (sorted(set(ks)), T.year_of(y))
    kf = Counter()
    co = Counter()
    for pid, (ks, y) in kw_paper.items():
        for k in ks:
            kf[k] += 1
        for i in range(len(ks)):
            for j in range(i + 1, len(ks)):
                co[(ks[i], ks[j])] += 1
    co_w2 = {k: v for k, v in co.items() if v >= 2}
    deg = Counter()
    for (a, b), w in co_w2.items():
        deg[a] += 1
        deg[b] += 1
    # 词频低于本批中位数的节点删掉（calc-logic 第二步）
    freqs = sorted(kf.values())
    kw_median = freqs[len(freqs) // 2] if freqs else 0
    kept = {k for k, v in kf.items() if v >= max(kw_median, 2)}

    # ---------------- 时间演变 ----------------
    year_all = Counter()
    kw_year: dict[str, Counter] = defaultdict(Counter)
    for pid, (ks, y) in kw_paper.items():
        if y:
            year_all[y] += 1
            for k in ks:
                kw_year[k][y] += 1

    def evolve(k: str) -> dict:
        c = kw_year[k]
        recent = [c.get(y, 0) for y in (2022, 2023, 2024)]
        base = [c.get(y, 0) for y in (2015, 2016, 2017, 2018, 2019)]
        rm = sum(recent) / 3
        bm = sum(base) / 5
        return {"recent_mean": round(rm, 2), "base_mean": round(bm, 2),
                "delta_pct": round(100 * (rm - bm) / max(bm, 1), 1)}

    # ---------------- 空间分布 ----------------
    city_cnt = Counter()
    city_papers = 0
    for pid in kw_paper:
        cs = author_city.get(pid) or set()
        if cs:
            city_papers += 1
            for c in cs:
                city_cnt[c] += 1

    top_kw = [k for k, _ in kf.most_common(15)]
    res = {
        "metric_id": MID,
        "metric_name": "科学研究前沿性",
        "support_judgment": "部分支持",
        "object": "领域主题（论文共被引簇 / 关键词共现词）",
        "verdict_reason": (
            "四子项里只有时间演变与空间分布能出数；研究前沿（共被引连通簇）与热点方向"
            "（关键词共现网）在 w≥2 的留边规则下分别只剩 "
            f"{in_pool_w2_edges} 条池内边与 {len(co_w2)} 条边，网不成立。根因是引文表与关键词表"
            "各自只有 2 万行、且与 100,900 篇论文主表可对齐的只有 782 / 799 篇（0.78%）"),
        "data_source": "gkx.dwd_zh_paper_citation（20,031 行）、dwd_zh_paper_classification（20,048 行）、"
                       "dwd_zh_paper（100,900 行）、dwd_zh_author（62,002 行）",
        "sql_count": 0,
        "sql_note": "全部读 20261022 探针缓存；引文/关键词/作者三表已在探针阶段各查 1 次",
        "probe": {
            "pool_papers": len(pool),
            "citing_papers_with_list": len(cite),
            "classified_papers": len(cls),
            "citing_and_classified": len({r[0] for r in cite} & {r[0] for r in cls}),
            "join_rate_vs_pool_pct": round(100 * len(cite) / len(pool), 3),
            "cited_ids_total": cited_total,
            "cited_ids_in_pool": cited_in_pool,
            "cited_residency_pct": round(100 * cited_in_pool / max(cited_total, 1), 3),
            "co_citation_pairs": len(pairs),
            "co_citation_edges_w2": edges_w2,
            "co_citation_edges_w2_in_pool": in_pool_w2_edges,
            "co_citation_components_in_pool": len(comps),
            "largest_component": len(comps[0]) if comps else 0,
            "keywords_distinct": len(kf),
            "keyword_pairs": len(co),
            "keyword_edges_w2": len(co_w2),
            "keyword_median_freq": kw_median,
            "keyword_nodes_kept": len(kept),
            "papers_with_year": sum(year_all.values()),
            "papers_with_city": city_papers,
            "city_coverage_pct": round(100 * city_papers / max(len(kw_paper), 1), 2),
        },
        "subitem_status": {
            "研究前沿": "不可建：池内 w≥2 共被引边 "
                        f"{in_pool_w2_edges} 条、连通分量 {len(comps)} 个、最大簇 {len(comps[0]) if comps else 0} 篇",
            "热点方向": f"退化：{len(co_w2)} 条 w≥2 共现边、{len(kept)} 个≥中位频次的词，"
                        "拓扑不足以支撑核心热点",
            "时间演变": f"可出数：{len(kw_paper)} 篇有年份，按近窗 2022—2024 vs 基线 2015—2019 计算",
            "空间分布": f"可出数：{city_papers} 篇（{round(100 * city_papers / max(len(kw_paper), 1), 2)}%）"
                        "能按作者单位落到城市",
        },
        "keyword_top15": [{"kw": k, "freq": kf[k], "degree": deg.get(k, 0), **evolve(k)}
                          for k in top_kw],
        "city_top15": T.topn(city_cnt, 15),
        "year_series": {str(y): int(v) for y, v in sorted(year_all.items())},
        "base_years_used": [2015, 2016, 2017, 2018, 2019, 2022, 2023, 2024],
        "base_years_missing": [2025, 2026],
        "base_year_block": T.base_year_block(
            [2015, 2016, 2017, 2018, 2019, 2022, 2023, 2024], [2025, 2026],
            "时间演变用近窗 2022—2024、基线 2015—2019；2025/2026 在 799 篇样本里记录过少，"
            "不进任何分母"),
        "gaps": [
            "引文表 20,031 行仅 782 行能与论文主表对齐（3.90%）",
            "关键词表 20,048 行仅 799 行可对齐（3.99%）",
            "被引列表中 9,391 个被引 id 只有 121 个（1.29%）落在本库论文池内，共被引网无从闭合",
            "英文侧仅 1,387 篇，无法作为第二语料补足",
        ],
        "repair_requirements": [
            "补齐 dwd_zh_paper_citation 到全量（当前 20,031 / 100,900 = 19.9%）并统一 id 域",
            "补齐 dwd_zh_paper_classification 到全量（当前 20,048 / 100,900 = 19.9%）",
            "被引 id 需与本库论文 id 同域，或提供 DOI 级映射表",
        ],
    }
    T.write_out(MID, res)
    print(json.dumps(res["probe"], ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
