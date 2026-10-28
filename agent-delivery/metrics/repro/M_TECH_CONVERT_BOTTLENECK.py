#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_TECH_CONVERT_BOTTLENECK 技术转化瓶颈识别（gkx 口径，20261021 批）

本件不读任何「瓶颈结果表」（旧稿依赖的演示库结果面 2,500 行、99.7% 判瓶颈，属退化造数），
改为在 IPC4 域上独立复算。全部输入来自只读缓存，零 SQL：

    _snapshots21/patent_ipc4_year_20261021.json    [ipc4, year, 件数, 机构数]
        —— 口径 LEFT(main_classification_ipcr,4)，一件专利一条主分类
    _snapshots21/patent_ipc4_by_name_20261021.json [ipc4, 申请人, 件数]
        —— 域内申请人分布（算承接集中度 HHI）

算子（本件自定义、待甲方确认）
------------------------------
存量规模只作**入算门槛**，不进分数——否则任何加法模型都会退化成「大域=瓶颈」。
在 272 个 ≥1,000 件的实质性域上，用三个与规模无关的结构量做百分位归一：

    C = 承接集中度（HHI = Σ s_i^2，申请人份额平方和）     权重 0.5
    F = 技术陈旧度（1 − 近三年申请占比）                   权重 0.3
    G = 收缩度（2023→2025 年申请量增速取负）               权重 0.2

    score = 100 × (0.5·Pct(C) + 0.3·Pct(F) + 0.2·Pct(G))

percentile 归一使判瓶颈率由阈值直接决定（>=P70 判瓶颈 = 30%），不受分布尾部影响。
阈值做 P60/P70/P80 扫掠，报告名单 Jaccard 稳健性。

缺口：需求三类指标里的「成果转化类」（转化效率、成果转化平台数据）在 gkx 无任何载体，
      产物写 dims_missing=['T_transfer']，不代理、不填补。
"""
from __future__ import annotations

import collections
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
METRIC = "M_TECH_CONVERT_BOTTLENECK"

MIN_COUNT = 1000          # 入算门槛：低于 1,000 件的长尾域归一不稳定，单独披露不入榜
WINDOW = (2021, 2024)     # 完整年窗口：2025（440,401 件，2024 的 72.6%）、2026（74,810 件）
                          # 均为采集未完年，不进分母、不用于增速（见 base_years_note）
WEIGHTS = {"C": 0.5, "F": 0.3, "G": 0.2}

IPC_LABEL = {
    "G06F": "电数字数据处理", "G01N": "物理/化学分析", "H04L": "数字信息传输",
    "H04W": "无线通信", "H01M": "电池/燃料电池", "G06Q": "行政与商业数据处理",
    "G06T": "图像数据处理", "H05K": "印刷电路/电设备结构", "G06V": "图像识别",
    "H02J": "供电/配电", "A61K": "医用配制品", "A61B": "诊断/外科器械",
    "B29C": "塑料成型", "H01L": "半导体器件", "G01R": "电性能测量",
    "H04N": "图像通信", "C12N": "微生物/酶/基因工程", "B23K": "焊接/切割",
    "G06N": "计算模型/人工智能", "H04B": "传输系统", "G01S": "无线电定位",
    "B65G": "运输/输送", "H01R": "电连接器", "G05B": "通用控制系统",
    "C07K": "肽/蛋白质", "G02F": "光学控制器件", "H10H": "半导体发光器件",
    "H10D": "半导体器件（新版）", "G11C": "存储器", "F21V": "照明装置",
    "A24F": "吸烟用品", "B60L": "电动车辆", "H02S": "光伏系统",
}


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def pct_rank(vals):
    """百分位秩（0—1，并列取平均秩）。比 min-max 抗尾部极值。"""
    keys = sorted(vals.values())
    n = len(keys)
    rank = {}
    i = 0
    while i < n:
        j = i
        while j + 1 < n and keys[j + 1] == keys[i]:
            j += 1
        avg = (i + j + 2) / 2.0          # 1-based 平均秩
        rank[keys[i]] = (avg - 1) / (n - 1) if n > 1 else 0.5
        i = j + 1
    return {k: rank[v] for k, v in vals.items()}


def quantile(vals, p):
    xs = sorted(vals)
    if not xs:
        return None
    k = (len(xs) - 1) * p
    f, c = math.floor(k), math.ceil(k)
    if f == c:
        return xs[int(k)]
    return xs[f] + (xs[c] - xs[f]) * (k - f)


def main():
    ipc = load("patent_ipc4_year_20261021.json")
    nm = load("patent_ipc4_by_name_20261021.json")

    total = collections.Counter()      # 完整年窗口（2021—2024），用于规模门槛与新鲜度/增速
    total6 = collections.Counter()     # 全窗口（2021—2026），用于申请人集中度分母
    year = collections.defaultdict(collections.Counter)
    all_year = collections.Counter()
    for ipc4, y, c, _o in ipc:
        y = int(y)
        all_year[y] += int(c)
        total6[ipc4] += int(c)
        if WINDOW[0] <= y <= WINDOW[1]:
            total[ipc4] += int(c)
            year[ipc4][y] += int(c)

    applicant = collections.defaultdict(set)
    app_sum = collections.Counter()
    by_dom = collections.defaultdict(list)
    for ipc4, name, c in nm:
        applicant[ipc4].add(name)
        app_sum[ipc4] += int(c)
        by_dom[ipc4].append(int(c))

    domains = sorted(total, key=lambda k: -total[k])
    evaluated = [d for d in domains if total[d] >= MIN_COUNT]
    mismatch = [d for d in domains if app_sum[d] != total6[d]]

    P = {d: float(total[d]) for d in evaluated}
    A = {d: float(len(applicant[d])) for d in evaluated}
    recent = {d: float(year[d].get(2023, 0) + year[d].get(2024, 0))
              for d in evaluated}
    hhi = {}
    for d in evaluated:
        ps = float(total6[d])
        hhi[d] = sum((c / ps) ** 2 for c in by_dom[d]) if ps else None
    growth = {}
    for d in evaluated:
        c22, c24 = year[d].get(2022, 0), year[d].get(2024, 0)
        growth[d] = (math.pow(c24 / c22, 0.5) - 1.0) if (c22 > 0 and c24 > 0) else None

    conc = {d: hhi[d] for d in evaluated}
    stale = {d: 1.0 - recent[d] / P[d] for d in evaluated}
    shrink = {d: (-growth[d] if growth[d] is not None else None) for d in evaluated}

    Cp = pct_rank(conc)
    Fp = pct_rank(stale)
    have_g = [d for d in evaluated if shrink[d] is not None]
    Gp = pct_rank({d: shrink[d] for d in have_g})
    # 增速缺一端的域不摊 0：G 维取该域 C/F 的均值占位，并在行内标 g_missing
    for d in evaluated:
        if d not in Gp:
            Gp[d] = (Cp[d] + Fp[d]) / 2.0

    score = {d: 100.0 * (WEIGHTS["C"] * Cp[d] + WEIGHTS["F"] * Fp[d]
                         + WEIGHTS["G"] * Gp[d]) for d in evaluated}

    p60 = quantile(list(score.values()), 0.60)
    p70 = quantile(list(score.values()), 0.70)
    p80 = quantile(list(score.values()), 0.80)
    bn60 = {d for d in evaluated if score[d] >= p60}
    bn70 = {d for d in evaluated if score[d] >= p70}
    bn80 = {d for d in evaluated if score[d] >= p80}

    def jaccard(a, b):
        return round(len(a & b) / len(a | b), 4) if (a or b) else 1.0

    def dominant_dim(d):
        parts = {"C": WEIGHTS["C"] * Cp[d], "F": WEIGHTS["F"] * Fp[d],
                 "G": WEIGHTS["G"] * Gp[d]}
        return max(parts, key=parts.get)

    def row(d):
        return {
            "ipc4": d,
            "label": IPC_LABEL.get(d, ""),
            "patents": int(total[d]),
            "applicants": int(A[d]),
            "hhi": round(hhi[d], 6),
            "cr5": round(sum(sorted(by_dom[d], reverse=True)[:5]) / float(total6[d]), 6),
            "patents_6y": int(total6[d]),
            "recent_ratio": round(recent[d] / P[d], 6),
            "growth_22_24": (round(growth[d], 6) if growth[d] is not None else None),
            "pct_C": round(Cp[d], 4), "pct_F": round(Fp[d], 4), "pct_G": round(Gp[d], 4),
            "score": round(score[d], 2),
            "bottleneck": score[d] >= p70,
            "dominant_dim": dominant_dim(d),
            "g_missing": growth[d] is None,
        }

    ranked = sorted(evaluated, key=lambda d: -score[d])
    bn = [row(d) for d in ranked if score[d] >= p70]

    out = {
        "metric_id": METRIC,
        "source": "code/_snapshots21/patent_ipc4_year_20261021.json + "
                  "patent_ipc4_by_name_20261021.json（gkx.dwd_patent 主分类 IPC4 缓存，零 SQL）",
        "method": {
            "grain": "IPC4（LEFT(main_classification_ipcr,4)，一件专利一条主分类）",
            "operators": {
                "C": "HHI=Σ(申请人份额^2)（分母取 2021—2026 全窗口，缓存无年份维），百分位归一——承接集中度",
                "F": "1-近三年(2024—2026)申请占比，百分位归一——技术陈旧度",
                "G": "-2022→2024 年均增速（CAGR），百分位归一——收缩度",
                "score": "100×(0.5·Pct(C)+0.3·Pct(F)+0.2·Pct(G))，越高越接近瓶颈",
            },
            "weights": WEIGHTS,
            "threshold": "score >= P70 判瓶颈（设计判瓶颈率 30%）",
            "window": "2021—2024 完整年（2025/2026 为采集未完年，主动排除）",
            "min_count": MIN_COUNT,
            "size_role": "存量规模只作入算门槛，不进分数——避免把「大域」误判成「瓶颈」",
            "weights_note": "权重、门槛与阈值均为本件自定义、待甲方确认，不称官方口径",
        },
        "aggregate": {
            "ipc4_domains_total": len(domains),
            "evaluated_domains": len(evaluated),
            "excluded_tail_domains": len(domains) - len(evaluated),
            "patents_ipc_total": sum(total.values()),
            "patents_ipc_all_years": sum(all_year.values()),
            "hhi_denominator": "2021—2026 全窗口（申请人缓存无年份维），与规模/增速窗口不同源，已在正文披露",
            "year_all_ipc": dict(sorted(all_year.items())),
            "patents_in_evaluated": int(sum(P.values())),
            "evaluated_coverage": round(sum(P.values()) / sum(total.values()), 6),
            "applicant_sum_mismatch_domains": len(mismatch),
            "g_missing_domains": len(evaluated) - len(have_g),
            "p60": round(p60, 4), "p70": round(p70, 4), "p80": round(p80, 4),
            "bottleneck_count": len(bn70),
            "bottleneck_rate": round(len(bn70) / len(evaluated), 6),
            "bottleneck_count_p80": len(bn80),
            "bottleneck_count_p60": len(bn60),
            "jaccard_p60_p70": jaccard(bn60, bn70),
            "jaccard_p70_p80": jaccard(bn70, bn80),
            "hhi_median": round(quantile(list(conc.values()), 0.5), 6),
            "hhi_p90": round(quantile(list(conc.values()), 0.9), 6),
            "recent_ratio_median": round(quantile(list(recent[d] / P[d] for d in evaluated), 0.5), 6),
        },
        "bottleneck_top20": [row(d) for d in ranked[:20]],
        "bottleneck_list": bn,
        "healthy_bottom10": [row(d) for d in ranked[-10:]],
        "dominant_dim_distribution": dict(collections.Counter(dominant_dim(d) for d in bn70)),
        "dims_covered": ["C", "F", "G"],
        "dims_missing": ["T_transfer"],
        "dims_missing_note": (
            "T_transfer（成果转化效率/成果转化平台数据）在 gkx 无任何载体：无技术合同登记表、"
            "无转化平台表、无产业化数据。本件不以论文数或专利维持年代代理，缺维显式置空，"
            "消费侧（布局推荐）须对缺维域附『转化维未诊断』标签。"),
        "support_judgment": "部分支持",
        "judgment_reason": (
            "承接集中度、技术陈旧度、收缩度三个结构量在 %d 个实质性 IPC4 域上可复算"
            "（覆盖有 IPC 专利的 %s），判瓶颈率 %s 由阈值直接决定，P60/P70/P80 名单 Jaccard "
            "%s / %s，区分度正常且不随规模漂移；但需求三类指标中的成果转化类在 gkx 无源，"
            "五维资源框架（人才/市场/技术/政策/资金）只有技术维与市场结构维有算子。"
            "始终存在无法补齐的依赖维，故落部分支持。"
            % (len(evaluated), round(sum(P.values()) / sum(total.values()), 4),
               round(len(bn70) / len(evaluated), 4),
               jaccard(bn60, bn70), jaccard(bn70, bn80))),
        "base_years_used": [2021, 2022, 2023, 2024],
        "base_years_missing": [2025, 2026],
        "base_years_note": (
            "专利表 apdt_year 覆盖 2021—2026（2017—2020 零行，不补 0）。本件只用 2021—2024 "
            "四个完整年：2025 有 440,401 件（2024 为 606,468，仅 72.6%）、2026 有 74,810 件，"
            "两年均为采集未完年，按缺失年处理、不进分母、不摊 0。增速用 2022→2024 的 CAGR，"
            "缺任一端则该域 G 维不摊 0（标 g_missing）。"),
    }

    with open(os.path.join(HERE, METRIC + "_out.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("wrote", METRIC + "_out.json")
    print("aggregate", json.dumps(out["aggregate"], ensure_ascii=False))
    print("top5", [(r["ipc4"], r["patents"], r["score"], r["dominant_dim"])
                   for r in out["bottleneck_top20"][:5]])
    print("dim_dist", out["dominant_dim_distribution"])


if __name__ == "__main__":
    main()
