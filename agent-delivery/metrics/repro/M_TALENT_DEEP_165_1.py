#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_TALENT_DEEP_165_1 —— 人才培养布局（TALENT 深度分析第 165 号）

需求原文（算法库 srs 序号 165）：识别重点技术方向的培养对象，输出「人才筛选 + 方向匹配 +
潜力评估 + 分层培养建议」。

需求未给公式与权重。本文口径：
  池 = 当前机构在深的学者 237 人（city=深圳市 / 机构名含深圳）
  评分只对 68 人成立：必须同时有「学术力」与「方向相关性或成长信号」——
    仅有生涯累计引用 + 机构专利、既无聚类方向又无论文轨迹的 169 人**不评分**
    （不谈方向就谈布局没有意义），在附录里单列。
  D1 学术力 = 成果数量 0.5 + 学术影响力 0.5（20+8 聚类关键词在中文论文题目/摘要中命中数，
              论文侧统计，不代表学者本人全部产出）
  D2 方向相关性 = 0.5 + 0.5 × log1p(命中聚类数)/log1p(max)，只对 59 人有值
  D3 成长信号 = 0.6 × 职业早期（首篇锚定论文 ≥ 2018）+ 0.4 × 近端活跃（末篇 ≥ 2024），
              只对 np≥3 的 32 人有值。**不用「近三年论文占比」**：面板 2024 年 21,228 篇是
              其他年份（约 4,100 篇）的 5 倍，是物化批次伪影，会把所有人算成「近年爆发」。
  D4 产业支撑 = 所属机构专利件数（log-minmax），210 人有值；高校/院所专利计入，
              因此这是「机构技术产出」，不是「个人成果转化」。
  权重 0.30 / 0.30 / 0.20 / 0.20（缺失维按剩余权重归一）。
  阈值：120 人内 p90 / p70 / p40 切 A/B/C/D，分档只表示「本池内相对位置」。

零 SQL：全部读 `code/_snapshots21/`。
产物：`code/M_TALENT_DEEP_165_1_out.json`。
"""
from __future__ import annotations

import math
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import _talent21_common as T  # noqa: E402
import _talent22_common as C  # noqa: E402

METRIC = "M_TALENT_DEEP_165_1"


def main() -> None:
    rs = C.rows()
    k, d1, d2 = C.academic_k(rs)
    agg = C.org_patent()
    orgpat = {r["sid"]: agg.get(r["org"], (None, None))[0] for r in rs}

    # 在深 = 当前机构在深圳（city=深圳市 或机构名含深圳）；不含仅有深圳履历/学历的外地学者
    pool = [i for i, r in enumerate(rs) if C.is_sz(r)]
    maxcl = max(len(rs[i]["cl"]) for i in pool)
    withpat = [i for i in pool if orgpat[rs[i]["sid"]] is not None]
    pv = [orgpat[rs[i]["sid"]] for i in withpat]
    plo, phi = min(pv), max(pv)
    ipat = {i: (math.log1p(orgpat[rs[i]["sid"]]) - math.log1p(plo)) /
                (math.log1p(phi) - math.log1p(plo)) for i in withpat}

    scored, thin = [], []
    for i in pool:
        r = rs[i]
        early = 1.0 if (r["y0"] and r["y0"] >= 2018) else 0.0
        active = 1.0 if (r["y1"] and r["y1"] >= 2024) else 0.0
        rel = T_ = None
        if r["cl"]:
            rel = 100 * (0.5 + 0.5 * math.log1p(len(r["cl"])) / math.log1p(maxcl))
        if r["np"] >= 3:  # 1—2 篇锚定论文不足以判「早期/活跃」，避免单篇即满分
            T_ = 100 * (0.6 * early + 0.4 * active)
        if rel is None and T_ is None:
            thin.append(i)
            continue
        parts = [(0.30, k[i])]
        if rel is not None:
            parts.append((0.30, rel))
        if T_ is not None:
            parts.append((0.20, T_))
        if i in ipat:
            parts.append((0.20, 100 * ipat[i]))
        w = sum(p[0] for p in parts)
        scored.append({"i": i, "score": round(sum(p[0] * p[1] for p in parts) / w, 4),
                       "dims": len(parts), "K": k[i], "rel": rel, "pot": T_,
                       "I": (100 * ipat[i]) if i in ipat else None,
                       "early": int((r["y0"] or 0) >= 2018) if r["np"] else None,
                       "active": int((r["y1"] or 0) >= 2024) if r["np"] else None})

    sc_sorted = sorted(scored, key=lambda x: -x["score"])
    cs = C.cuts([x["score"] for x in scored])
    tiers = Counter(C.tier(x["score"], cs) for x in scored)

    # top 列表按 (姓名, 机构) 去重——dwd_scholar 同一人可能有两行
    seen, top = set(), []
    for x in sc_sorted:
        r = rs[x["i"]]
        key = r["name"]  # 同名多行（不同 sid / 机构写法）只留最高分
        if key in seen:
            continue
        seen.add(key)
        top.append({"name": r["name"], "org": r["org"], "city": r["city"],
                    "score": x["score"], "K": x["K"],
                    "rel": x["rel"], "pot": x["pot"], "I": x["I"],
                    "np": r["np"], "nsz": r["nsz"], "clusters": len(r["cl"]),
                    "y0": r["y0"], "y1": r["y1"], "dims": x["dims"]})
        if len(top) >= 30:
            break

    payload = {
        "metric": METRIC,
        "support_judgment": "部分支持",
        "support_reason": (
            "方向匹配（59 人有 20+8 聚类命中）、成长信号（32 人 np≥3 有首末年份）、"
            "学术力（237 人全覆盖）、产业支撑（210 人有机构专利）四维可算；但「培养布局」"
            "要求的培养项目/平台/经费/导师数据在 gkx 全缺（人才工程表只有称号与年份、无对象级"
            "培养措施），聚类方向来自论文题目关键词共现而非官方技术目录 → 部分支持。"
        ),
        "method": {
            "pool": "当前机构在深的学者 237 人（city=深圳市 / 机构名含深圳），不含仅有深圳履历/学历的外地学者",
            "d1": "学术力 = 0.5*log-minmax(paper_nums) + 0.5*log-minmax(citation_nums)",
            "d2": "方向相关性 = 0.5+0.5*log1p(聚类命中数)/log1p(max)，59 人有值",
            "d3": "成长信号 = 0.6*首篇≥2018 + 0.4*末篇≥2024，仅 np≥3 者有值（1—2 篇不判潜力）",
            "d4": "产业支撑 = 所属机构专利件数 log-minmax，210 人有值",
            "weights": "0.30 / 0.30 / 0.20 / 0.20（缺失维归一）",
            "scored_rule": "必须同时具备学术力与（方向相关性 或 成长信号）；两者皆无者不评分",
            "thresholds": {"p90": cs[0], "p70": cs[1], "p40": cs[2]},
            "dedup": "top 列表按姓名去重，同人两行只留最高分（如李清泉两行机构写法不同）",
            "no_zero_fill": "无聚类/无论文/无机构专利的分量一律 None，按剩余权重归一",
        },
        "pool": {"in_sz": len(pool), "scored": len(scored), "thin_not_scored": len(thin),
                 "with_cluster": sum(1 for i in pool if rs[i]["cl"]),
                 "with_paper": sum(1 for i in pool if rs[i]["np"] > 0),
                 "with_org_patent": len(withpat),
                 "dims4": sum(1 for x in scored if x["dims"] == 4),
                 "dims3": sum(1 for x in scored if x["dims"] == 3),
                 "dims2": sum(1 for x in scored if x["dims"] == 2),
                 "early_career": sum(1 for x in scored if x["early"] == 1),
                 "still_active": sum(1 for x in scored if x["active"] == 1)},
        "dist": {"score": C.dist([x["score"] for x in scored]),
                 "K": C.dist([x["K"] for x in scored]),
                 "rel": C.dist([x["rel"] for x in scored if x["rel"] is not None]),
                 "pot": C.dist([x["pot"] for x in scored if x["pot"] is not None]),
                 "I": C.dist([x["I"] for x in scored if x["I"] is not None])},
        "thresholds": {"p90": cs[0], "p70": cs[1], "p40": cs[2]},
        "tiers": {t: tiers.get(t, 0) for t in "ABCD"},
        "top30": top,
        "thin_names": [{"name": rs[i]["name"], "org": rs[i]["org"],
                        "cite": rs[i]["cite"], "paper": rs[i]["paper"]} for i in thin[:20]],
        "base_years_used": [2024, 2025],
        "base_years_missing": [2026],
        "base_years_note": (
            "成长信号的「近端活跃」用末篇锚定论文 ≥2024，落 2024—2025 两年；2026 为残年"
            "（仅 1,432 篇且年份未走完），不进窗口、不按 0 摊入。首篇年份取全时段，只做"
            "「是否 ≥2018」的二值判断，不参与年度分母。面板 2024 年 21,228 篇是其他年份的"
            "5 倍（物化批次伪影），故不采用「近三年占比」这类会被 2024 拉满的口径。"
            " 产业支撑维为机构专利 2021—2026 窗口（专利表无 2017—2020 行），与成长信号不同源。"
        ),
        "probes": {"sql_count": 0, "patent_sql": 0,
                   "source": "gkx @ 183.240.141.251:3318（快照派生，零 SQL）"},
        "reused_from": "code/_snapshots21/talent22_panel_20261022.json（由 code/_build_talent22_panel.py 生成）",
    }
    C.write(METRIC, payload)
    print("pool", payload["pool"])
    print("dist", payload["dist"]["score"], "cuts", cs)
    print("top5", [(x["name"], x["org"], x["score"], x["clusters"], x["np"]) for x in top[:5]])


if __name__ == "__main__":
    main()
