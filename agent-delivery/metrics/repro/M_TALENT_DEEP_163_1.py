#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_DEEP_163_1 —— 人才产业力评估模型（TALENT 深度分析第 163 号）

需求原文（算法库 srs 序号 163）：以「企业影响力 / 产业覆盖度 / 媒体知名度」三类核心指标
加阈值，加权生成人才产业力指数，衡量企业的人才资源整合与输出能力。

需求未给公式、未给权重、未给对象口径。本文口径（**对象 = 深圳企业**，不是学者个人）：
  U  对象池 = `base_20261021.json` 中 city=深圳市、名称含「公司/集团/厂/有限/股份」、
      且出现在 `star_applicant_agg_gkx.json`（169,226 名申请人）里的企业（去重）。
      共 77,529 家，专利合计 1,300,219 件（= 深圳企业专利，占全库 44.23%）。
  D1 企业影响力 = 申请人专利件数（`agg[name][0]`，全量 2,939,895 件逐位对齐）。
  D2 产业覆盖度 = 该企业覆盖的 IPC 小类数（`patent_ipc4_by_name_20261021.json`，
      134,152 个申请人有 IPC 归属，占 169,226 的 79.29%；对象池覆盖 59,645 家 = 76.93%）。
  D3 媒体知名度 = `dwd_org_important_news_info` 按企业名精确计数的新闻条数，
      **只对专利 TOP60 企业取数**（58 家命中）；新闻含转载/重复，只能作相对声量。
  权重 0.40 / 0.30 / 0.30；D2 缺失按 0.40 归一（dims=1），D3 只作头部叠加层，
  全池分数用 D1+D2 两维（0.40/0.30 归一），头部 58 家另给三维分，**不混排**。

阈值：全池 p90 / p70 / p40 切 A/B/C/D。

零 SQL：企业底册、申请人聚合、IPC 缓存、新闻头部快照全部在本目录 `code/_snapshots21/`。
产物：`code/M_TALENT_DEEP_163_1_out.json`。
"""
from __future__ import annotations

import json
import math
import statistics
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import _talent21_common as T  # noqa: E402
import _talent22_common as C  # noqa: E402

METRIC = "M_TALENT_DEEP_163_1"
ENT_KW = ("公司", "集团", "厂", "有限", "股份")


def main() -> None:
    base = json.loads((T.SNAP / "base_20261021.json").read_text(encoding="utf-8"))
    agg = T.applicant_agg()
    ipc: dict[str, set] = {}
    for ipc4, name, _cnt in json.loads(
            (T.SNAP / "patent_ipc4_by_name_20261021.json").read_text(encoding="utf-8")):
        ipc.setdefault(name, set()).add(ipc4)
    news = json.loads((T.SNAP / "talent22_news_top_20261022.json").read_text(encoding="utf-8"))

    # 对象池（按名称去重；底册 47 个重名会重复，必须先 set）
    names = sorted({r[2] for r in base
                    if r[4] == "深圳市" and r[2] and any(k in r[2] for k in ENT_KW)
                    and r[2] in agg})
    pat = [agg[n][0] for n in names]
    d1 = T.log_minmax(pat)
    idx2 = [i for i, n in enumerate(names) if n in ipc]
    vals2 = [len(ipc[names[i]]) for i in idx2]
    d2 = dict(zip(idx2, T.log_minmax(vals2)))

    score2: list[float | None] = [None] * len(names)
    dims2: list[int] = [0] * len(names)
    for i in range(len(names)):
        if i in d2:
            score2[i] = round(100 * (0.40 * d1[i] + 0.30 * d2[i]) / 0.70, 4)
            dims2[i] = 2
        else:
            score2[i] = round(100 * d1[i], 4)
            dims2[i] = 1
    cs = C.cuts([s for s in score2 if s is not None])
    tiers = Counter(C.tier(s, cs) for s in score2 if s is not None)

    # 头部 58 家的三维分（新闻只在头部有）
    head = []
    nvals = [x["news"] for x in news["items"] if x["news"] is not None]
    nlo, nhi = min(nvals), max(nvals)
    for x in news["items"]:
        if x["news"] is None or x["name"] not in names:
            continue
        i = names.index(x["name"])
        d3 = (math.log1p(x["news"]) - math.log1p(nlo)) / (math.log1p(nhi) - math.log1p(nlo))
        full = 100 * (0.40 * d1[i] + 0.30 * d2[i] + 0.30 * d3)
        head.append({"name": x["name"], "score3": round(full, 4),
                     "score2": score2[i], "pat": x["pat"], "grant": x["grant"],
                     "ipc4": len(ipc.get(x["name"], ())), "news": x["news"],
                     "d1": round(d1[i], 4), "d2": round(d2.get(i, 0), 4), "d3": round(d3, 4)})
    head.sort(key=lambda z: -z["score3"])

    top2 = C.top([{"name": n, "org": n, "city": "深圳市"} for n in names], score2, 20,
                 extra=lambda i: {"pat": pat[i], "ipc4": len(ipc.get(names[i], ())),
                                  "dims": dims2[i]})

    payload = {
        "metric": METRIC,
        "support_judgment": "部分支持",
        "support_reason": (
            "企业影响力（专利件数）与产业覆盖度（IPC 小类数）在 77,529 家深圳企业上可算，"
            "两维相关系数 0.78；但媒体知名度只能在专利 TOP60 的 58 家上取数（新闻表 1,668,414 行"
            "按名称计数需逐名过滤，全池 7.7 万家不可行），且新闻条数含转载/重复、无情感与去重，"
            "只能作头部相对声量；IPC 缓存覆盖 76.93%、深大等机构口径偏低 → 部分支持。"
        ),
        "method": {
            "unit": "深圳企业（base city=深圳市 + 名称含公司/集团/厂/有限/股份 + 申请人聚合有记录）",
            "d1": "申请人专利件数 agg[name][0]（全量 2,939,895 件逐位对齐）",
            "d2": "覆盖 IPC 小类数（patent_ipc4_by_name 缓存，134,152 名申请人 = 79.29%）",
            "d3": "新闻条数（dwd_org_important_news_info 按名称精确计数，仅 TOP60 专利企业）",
            "weights": "D1 0.40 / D2 0.30 / D3 0.30；全池两维按 0.40/0.30 归一；头部另算三维，不混排",
            "normalize": "log1p → 池内 min-max",
            "thresholds": {"p90": cs[0], "p70": cs[1], "p40": cs[2]},
            "news_caveat": "新闻计数含转载与重复；无情感极性、无去重、无事件级去噪",
        },
        "pool": {"enterprises": len(names), "base_rows_sz": sum(1 for r in base if r[4] == "深圳市"),
                 "with_ipc": len(idx2), "with_ipc_pct": round(100 * len(idx2) / len(names), 2),
                 "pat_total": sum(pat), "pat_share_pct": round(100 * sum(pat) / 2939895, 2),
                 "dims2": sum(1 for x in dims2 if x == 2), "dims1": sum(1 for x in dims2 if x == 1)},
        "dist": {"pat": C.dist(pat), "ipc4": C.dist(vals2),
                 "score2": C.dist([s for s in score2 if s is not None])},
        "thresholds": {"p90": cs[0], "p70": cs[1], "p40": cs[2]},
        "tiers": {t: tiers.get(t, 0) for t in "ABCD"},
        "top20": top2,
        "head_media": {"n": len(head), "top15": head[:15],
                       "news_matched": sum(1 for x in news["items"] if x["news"] is not None),
                       "news_missing": [x["name"] for x in news["items"] if x["news"] is None]},
        "corr": {"spearman_pat_ipc": T.spearman([agg[n][0] for n in names if n in ipc],
                                                [len(ipc[n]) for n in names if n in ipc])},
        "base_years_used": [2021, 2022, 2023, 2024, 2025, 2026],
        "base_years_missing": [],
        "base_years_note": ("专利件数是 `dwd_patent` 全表按申请人聚合的结果，而该表只有 2021—2026 的申请年，"
                            "因此这是「2021 年起可观测窗口」的累计，不是企业生涯专利总量；2026 为残年（全表 74,810 件），"
                            "计入但未单独拆年。2017—2020 表中零行（陷阱 3.13），不进分母、不按 0 摊入。"
                            "IPC 覆盖数与新闻条数同为当前快照截面，不做年度增速。"),
        "probes": {"sql_count": 0, "patent_sql": 0,
                   "source": "gkx @ 183.240.141.251:3318（快照派生，零 SQL）",
                   "news_snapshot": "code/_snapshots21/talent22_news_top_20261022.json"},
        "reused_from": "code/_snapshots21/talent22_news_top_20261022.json（由本批新闻探针落盘）",
    }
    C.write(METRIC, payload)
    print("pool", payload["pool"])
    print("dist", payload["dist"])
    print("head top5", [(x["name"], x["score3"]) for x in head[:5]])
    print("top2", [(x["name"], x["score"]) for x in top2[:5]])


if __name__ == "__main__":
    main()
