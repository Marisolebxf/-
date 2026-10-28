#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_REG_PAPERS 高校论文（区域）（20261021 改源版）

需求语境：区域产业指数模型 → 学术生态竞争力 → 「区域论文数」。
原口径只有指标名，没有公式；本报告采用可核查的最小定义：
  某链在某市的论文数 = 统计窗内、至少 1 位作者机构落在该市、且标题/关键词命中该链领域词的
  中文期刊论文数（一篇可命中多条链）。

数据面（全部 gkx）：
  `gkx.dwd_zh_paper` 100,900 行 —— author_info_list 100% 非空，含 institution 字段；
  `gkx.dwd_zh_paper_classification` 20,048 行 —— 学科分类与关键词；
  机构→城市：`dwd_org_heis_info` 3,501 + `dwd_research_institute_base_info` 2,074 +
  `dwd_org_base_info` 189,116，本地最长前缀匹配（不连库 JOIN）。

派生缓存在 `_build_reg5_papers.py` 里一次落盘，本脚本只做聚合，可反复复算。

输出：code/M_CHAIN_REG_PAPERS_out.json
"""
from __future__ import annotations

import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

from _reg5_common import CHAIN_AXIS, CHAIN_CN, CITY4, SNAP, _load, pct, stats, write_out

MID = "M_CHAIN_REG_PAPERS"
AGG = "reg5_papers_agg_20261021.json"


def load_agg():
    d = _load(AGG)
    if d:
        return d
    subprocess.run([sys.executable, str(Path(__file__).parent / "_build_reg5_papers.py")], check=True)
    d = _load(AGG)
    if not d:
        raise SystemExit("论文派生缓存构建失败")
    return d


def main() -> None:
    t0 = time.time()
    agg = load_agg()
    papers = agg["papers"]          # [year, [city...], [chain...], is_university]
    meta = agg["meta"]

    city_year = Counter()
    city_year_uni = Counter()
    chain_city = Counter()
    chain_city_uni = Counter()
    chain_city_5y = Counter()
    city_total = Counter()
    year_hist = Counter()
    inst_papers = Counter()

    for y, cities, chains, is_uni in papers:
        if y:
            year_hist[y] += 1
        for c in cities:
            city_total[c] += 1
            if y:
                city_year[(c, y)] += 1
                if is_uni:
                    city_year_uni[(c, y)] += 1
            for ch in chains:
                chain_city[(ch, c)] += 1
                if is_uni:
                    chain_city_uni[(ch, c)] += 1
                if y and 2021 <= y <= 2025:
                    chain_city_5y[(ch, c)] += 1

    matrix = []
    for ch in CHAIN_AXIS:
        row = {"chain": ch, "chain_name": CHAIN_CN[ch], "cells": {}}
        for c in CITY4:
            k = (ch, c)
            row["cells"][c] = {
                "papers_labeled": chain_city.get(k, 0),
                "papers_labeled_university": chain_city_uni.get(k, 0),
                "papers_labeled_2021_2025": chain_city_5y.get(k, 0),
                "papers_all_disciplines_in_city": city_total.get(c, 0),
                "share_of_city_papers_pct": pct(chain_city.get(k, 0), city_total.get(c, 0)),
            }
        matrix.append(row)

    vals = [row["cells"][c]["papers_labeled"] for row in matrix for c in CITY4]
    vals5 = [row["cells"][c]["papers_labeled_2021_2025"] for row in matrix for c in CITY4]
    flat = sorted(((row["chain_name"], c, row["cells"][c]["papers_labeled"],
                    row["cells"][c]["papers_labeled_2021_2025"])
                   for row in matrix for c in CITY4), key=lambda x: -x[2])

    year_series = {c: {y: city_year[(c, y)] for y in range(2015, 2027)} for c in CITY4}
    uni_series = {c: {y: city_year_uni[(c, y)] for y in range(2015, 2027)} for c in CITY4}
    peak_year = max(year_hist, key=year_hist.get)

    payload = {
        "metric_id": MID,
        "metric_name": "高校论文（区域）",
        "date": "2026-10-22",
        "formula_owner": "徐滕强（CHAIN 域 calc-logic，仅给指标名与统计口径）",
        "formula": "Papers(c,r)=Σ_p 1{机构(p)∩r≠∅ ∧ chain_token(p)=c}，一篇可命中多条链",
        "stat_year": 2025,
        "region_axis": CITY4,
        "chain_axis": len(CHAIN_AXIS),
        "matrix": matrix,
        "city_totals": {c: city_total.get(c, 0) for c in CITY4},
        "city_year_all": year_series,
        "city_year_university": uni_series,
        "chain_city_total_by_chain": {row["chain_name"]: sum(row["cells"][c]["papers_labeled"] for c in CITY4)
                                      for row in matrix},
        "probes": {
            "papers_total": meta["papers_total"],
            "university_papers": meta["university_papers"],
            "university_pct": meta["university_pct"],
            "city_matched": meta["city_matched"],
            "city_matched_pct": meta["city_matched_pct"],
            "chain_labeled": meta["chain_labelled"],
            "chain_label_pct": meta["chain_label_pct"],
            "chain_from_keywords": meta["chain_from_keywords"],
            "chain_from_title": meta["chain_from_title"],
            "keywords_rows": meta["keywords_rows"],
            "year_min": meta["year_min"],
            "year_max": meta["year_max"],
            "peak_year": peak_year,
            "peak_year_rows": year_hist[peak_year],
            "peak_year_share_pct": pct(year_hist[peak_year], meta["papers_total"]),
            "inst_unmatched_top": meta["inst_unmatched_top"][:10],
            "cells_nonzero": sum(1 for v in vals if v),
            "cells_nonzero_5y": sum(1 for v in vals5 if v),
            "n_cells": 48,
        },
        "stats_chain_cell_papers": stats(vals),
        "stats_chain_cell_papers_2021_2025": stats(vals5),
        "top10_cells": [{"chain": a, "city": b, "papers": v, "papers_2021_2025": w}
                        for a, b, v, w in flat[:10]],
        "bottom10_cells": [{"chain": a, "city": b, "papers": v, "papers_2021_2025": w}
                           for a, b, v, w in flat[-10:]],
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": (
                f"区域维闭合：100,900 篇中文论文的作者机构串 100% 非空，"
                f"{meta['city_matched']:,} 篇（{meta['city_matched_pct']}%）至少 1 位作者机构可落到 4 市，"
                f"高校论文 {meta['university_papers']:,} 篇（{meta['university_pct']}%）；"
                f"链维只能靠标题/分类关键词代理，命中 {meta['chain_labelled']:,} 篇（{meta['chain_label_pct']}%），"
                f"48 个链×城单元 {sum(1 for v in vals if v)}/48 非零，但 4 个单元为 0 且论文数区间 "
                f"{min(vals)}—{max(vals):,} 跨三个数量级。"
                f"因为论文表没有任何产业链字段、机构也没有链码，链归属是文本代理而非数据字段，"
                f"且 2024 年论文占全表 {pct(year_hist.get(2024, 0), meta['papers_total'])}%（采集偏斜），"
                f"不能当作年度趋势，故判部分支持。"
            ),
            "criteria": {"papers_total": meta["papers_total"],
                         "city_matched_pct": meta["city_matched_pct"],
                         "chain_label_pct": meta["chain_label_pct"],
                         "n_cells": 48, "cells_nonzero": sum(1 for v in vals if v),
                         "n_distinct": len(set(vals))},
        },
        "notes": [
            "链归属为「标题 + 学科关键词」代理，不是库表字段：一篇论文可同时命中多条链（如「机器人+人工智能」），"
            "链级合计大于论文总数，不能跨链加总。",
            "机构落城用最长前缀匹配（高校名录 + 科研院所 + 企业底册），匹配不上的多为中央部委院所与外地单位；"
            "未匹配清单见 probes.inst_unmatched_top，不按城市猜测回填。",
            "2024 年 32,379 篇、占全表 32.1%，而 2021—2023 年每年约 6,300—6,800 篇，"
            "这是采集批次偏斜而非发文量突变，故正文只给「存量 + 2021—2025 窗」，不画年度趋势线。",
            "「高校论文」按作者机构是否命中高校名录判定（77.0%），医院/企业/院所论文不剔除但单独可查。",
            "论文下载量 `download_num` 整列为 0、期刊影响因子 `impact_score` 整列为空，故不做任何影响力加权。",
        ],
        "elapsed_sec": round(time.time() - t0, 2),
    }
    write_out(MID, payload)
    print("papers", meta["papers_total"], "city matched", meta["city_matched"], "chain labeled", meta["chain_labelled"])
    print("cells", payload["stats_chain_cell_papers"], "nonzero", payload["probes"]["cells_nonzero"])
    print("city totals", payload["city_totals"])
    print("peak year", peak_year, year_hist[peak_year])


if __name__ == "__main__":
    main()
