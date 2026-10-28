#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_TALENT_DEEP_162_1 —— 人才学术力评估模型（TALENT 深度分析第 162 号）

需求原文（算法库 srs 序号 162）：以「学术成果数量 / 学术影响力 / 专业技能水平」三维
加阈值分级，加权生成人才学术力指数，输出指数 + 分级 + 报告。

需求未给公式、未给权重、未给阈值。本文口径：
  D1 成果数量   = `dwd_scholar.paper_nums`（生涯累计，21,316 行 100% 非空）
  D2 学术影响力 = `dwd_scholar.citation_nums`（生涯累计，100% 非空）
  D3 专业技能水平（代理） = 姓名 + 机构 6 字前缀双锚定的中文论文所命中的
        「深圳 20+8」产业簇个数（`_build_talent22_panel.py` 已落盘），
        只有 13,955 名有可锚定论文的学者才有值；无锚定论文者 D3 = None，**不补 0**。
  权重 0.40 / 0.35 / 0.25；三列都做 log1p 后池内 min-max。

**两榜制（关键）**：D3 缺失的 6,465 人若按剩余权重归一（0.40/0.35），会因「少了
0.25 的拉低项」而系统性占优——实测首版 top20 里 15 人是 dims=2，第一名唐本忠
（paper 2,411 / cite 257,865）正是没有锚定论文的人。这不是学术力强，是分母少了一项。
因此本版把两群人**分榜打分、分榜定档**：
  - 三维榜 13,955 人：0.40/0.35/0.25，阈值取本榜 p90/p70/p40；
  - 二维榜 6,465 人：0.5333/0.4667，阈值取本榜 p90/p70/p40；
  - 两榜分数不可直接比较，`track` 字段必须与分数一起读。
  D3 的价值在「方向广度」，不在「水平高低」；二维榜回答「只看产出与影响谁靠前」。

零 SQL、零专利查询：输入全部是本目录 `code/_snapshots21/` 下的 gkx 快照。
产物：`code/M_TALENT_DEEP_162_1_out.json`。
"""
from __future__ import annotations

import statistics
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import _talent21_common as T  # noqa: E402
import _talent22_common as C  # noqa: E402

METRIC = "M_TALENT_DEEP_162_1"
W = (0.40, 0.35, 0.25)


def main() -> None:
    rs = C.rows()
    k2, d1, d2 = C.academic_k(rs)
    idx = [i for i, r in enumerate(rs) if r["np"] > 0]
    vals = [len(rs[i]["cl"]) for i in idx]
    d3 = T.log_minmax(vals)
    m3 = dict(zip(idx, d3))

    score, track = [None] * len(rs), [0] * len(rs)
    for i in range(len(rs)):
        if i in m3:
            score[i] = round(100 * (W[0] * d1[i] + W[1] * d2[i] + W[2] * m3[i]), 4)
            track[i] = 3
        else:
            score[i] = round(100 * ((W[0] * d1[i] + W[1] * d2[i]) / (W[0] + W[1])), 4)
            track[i] = 2

    s3 = [score[i] for i in range(len(rs)) if track[i] == 3]
    s2 = [score[i] for i in range(len(rs)) if track[i] == 2]
    cs3, cs2 = C.cuts(s3), C.cuts(s2)
    tier3 = Counter(C.tier(score[i], cs3) for i in range(len(rs)) if track[i] == 3)
    tier2 = Counter(C.tier(score[i], cs2) for i in range(len(rs)) if track[i] == 2)

    # 院士校验：分榜内分位
    acad = T.academicians()
    pool_sids = {r["sid"] for r in rs}
    acad_hit = sorted(acad & pool_sids)
    acad_scores = [score[i] for i, r in enumerate(rs) if r["sid"] in acad]
    pct = {}
    for tr, cut_list in ((3, s3), (2, s2)):
        order = sorted((score[i] for i in range(len(rs)) if track[i] == tr))
        for i in range(len(rs)):
            if track[i] == tr:
                lo, hi = 0, len(order)
                while lo < hi:
                    mid = (lo + hi) // 2
                    if order[mid] < score[i]:
                        lo = mid + 1
                    else:
                        hi = mid
                pct[i] = round(100 * lo / max(len(order) - 1, 1), 2)
    acad_pct = [pct[i] for i, r in enumerate(rs) if r["sid"] in acad]
    top100_sids = {rs[i]["sid"] for i in sorted(
        range(len(rs)), key=lambda i: (-(C.tier(score[i], cs3 if track[i] == 3 else cs2) == "A"),
                                       -pct[i]))[:100]}
    top100_acad = len(top100_sids & acad)

    def topn(tr: int, n: int) -> list[dict]:
        cand = [i for i in range(len(rs)) if track[i] == tr]
        cand.sort(key=lambda i: -score[i])
        return [{"rank": n0 + 1, "name": rs[i]["name"], "org": rs[i]["org"],
                 "city": rs[i]["city"], "score": score[i], "h": rs[i]["h"],
                 "cite": rs[i]["cite"], "paper": rs[i]["paper"],
                 "np": rs[i]["np"], "clusters": len(rs[i]["cl"]), "track": tr}
                for n0, i in enumerate(cand[:n])]

    sz = [(score[i], rs[i]) for i in range(len(rs)) if rs[i]["city"] == "深圳市"]
    sz.sort(key=lambda x: -x[0])
    sz_branch = sum(1 for r in rs if r["city"] != "深圳市" and "深圳" in r["org"])

    payload = {
        "metric": METRIC,
        "support_judgment": "部分支持",
        "support_reason": (
            "成果数量与学术影响力两维在 20,420 名有姓名学者上 100% 可算；第三维「专业技能水平」"
            "只能代理：`dwd_scholar_research_direction` 与主档 scholar_id 只有 1,793 个交集"
            "（8.78%），本文改用姓名+机构双锚定的中文论文簇，覆盖 13,955 人（68.33%），"
            "仍有 6,465 人没有第三维；且「簇个数」是产业领域广度，不是技能水平本身 → 部分支持。"
        ),
        "method": {
            "dims": ["成果数量 paper_nums", "学术影响力 citation_nums", "领域广度 = 20+8 簇个数"],
            "weights": {"paper": 0.40, "cite": 0.35, "breadth": 0.25},
            "normalize": "log1p → 池内 min-max",
            "two_track": ("D3 有值者走三维榜（0.40/0.35/0.25，13,955 人）；D3 缺失者走二维榜"
                          "（0.5333/0.4667，6,465 人），两榜各自定阈值，分数不可跨榜比较"),
            "thresholds_3d": {"p90": cs3[0], "p70": cs3[1], "p40": cs3[2]},
            "thresholds_2d": {"p90": cs2[0], "p70": cs2[1], "p40": cs2[2]},
            "tiers": "榜内 A≥p90 / B≥p70 / C≥p40 / D<p40",
            "no_zero_fill": "D3 无锚定论文 → None，不写 0；也不与三维榜混排",
            "window": "生涯累计截面（无年度窗口）",
        },
        "pool": {"scholars": len(rs), "named": len(rs), "dims3": len(s3), "dims2": len(s2),
                 "cluster_tagged": sum(1 for r in rs if r["cl"]), "anchored": len(idx)},
        "dist": {"all": C.dist(score), "track3": C.dist(s3), "track2": C.dist(s2)},
        "d1": C.dist([r["paper"] for r in rs]),
        "d2": C.dist([r["cite"] for r in rs]),
        "d3": C.dist(vals),
        "thresholds": {"track3": {"p90": cs3[0], "p70": cs3[1], "p40": cs3[2]},
                       "track2": {"p90": cs2[0], "p70": cs2[1], "p40": cs2[2]}},
        "tiers": {"track3": {t: tier3.get(t, 0) for t in "ABCD"},
                  "track2": {t: tier2.get(t, 0) for t in "ABCD"}},
        "top20": topn(3, 20),
        "top20_track2": topn(2, 20),
        "sz_top10": [{"name": r["name"], "org": r["org"], "score": round(s, 4), "h": r["h"],
                      "cite": r["cite"], "clusters": len(r["cl"])} for s, r in sz[:10]],
        "sz_slice": {"n": len(sz), "anchored": sum(1 for _, r in sz if r["np"] > 0),
                     "cluster_tagged": sum(1 for _, r in sz if r["cl"]),
                     "branch_campus_excluded": sz_branch,
                     "note": "地名归属（city=深圳市）213 人；机构名含深圳 182 人；另 24 名分校/分支"
                             "机构人员（如哈工大深圳）地名归属在外地，未计入本切片。"},
        "academician_check": {
            "flag_rows": len(acad), "attached": len(acad_hit),
            "attach_pct": round(100 * len(acad_hit) / len(acad), 2),
            "score_median": round(statistics.median(acad_scores), 4) if acad_scores else None,
            "pct_median": round(statistics.median(acad_pct), 2) if acad_pct else None,
            "top100_hits": top100_acad, "top100_pct": round(100 * top100_acad / 100, 2),
        },
        "id_gap": {"rd_rows": len(T.research()), "rd_joined": sum(1 for r in rs if r["rd"]),
                   "rd_join_pct": round(100 * sum(1 for r in rs if r["rd"]) / len(rs), 2)},
        "corr": {"spearman_k_h": T.spearman(score, [r["h"] for r in rs]),
                 "spearman_d1_d2": T.spearman([r["paper"] for r in rs],
                                              [r["cite"] for r in rs])},
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面口径：三维均取生涯累计值（paper_nums / citation_nums / 双锚定论文簇），"
                            "不含年度窗口，也不做任何跨年基准或增长率，故无基期年份。"
                            "`dwd_scholar` 本身没有年份字段，论文面板的年度信息只用于 165 的潜力维，"
                            "不参与本件打分。"),
        "probes": {"sql_count": 0, "patent_sql": 0,
                   "source": "gkx @ 183.240.141.251:3318（快照派生，零 SQL）",
                   "panel": "code/_snapshots21/talent22_panel_20261022.json"},
        "reused_from": "code/_snapshots21/talent22_panel_20261022.json（由 code/_build_talent22_panel.py 生成）",
    }
    C.write(METRIC, payload)
    print("dist3", payload["dist"]["track3"], "cuts3", cs3)
    print("dist2", payload["dist"]["track2"], "cuts2", cs2)
    print("tiers", payload["tiers"])
    print("top5_3d", [(x["name"], x["score"]) for x in payload["top20"][:5]])
    print("top5_2d", [(x["name"], x["score"]) for x in payload["top20_track2"][:5]])


if __name__ == "__main__":
    main()
