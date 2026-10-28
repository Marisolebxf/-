#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_TALENT_DEEP_164_1 —— 招入人才推荐模型（TALENT 深度分析第 164 号）

需求原文（算法库 srs 序号 164）：以「学术力 / 产业力 / 产品匹配度 / 深圳连接度」四维
加阈值，加权生成招引人才推荐指数，输出指数 + 优选排序清单 + 匹配分析报告。

需求未给公式与权重。本文口径：
  候选池 = 当前机构不在深圳的 20,183 名有姓名学者（city≠深圳市 且机构名不含「深圳」，
           把哈工大深圳、港中大深圳等分校人员排除在「外部候选人」之外）。
  D1 学术力 = 成果数量 0.5 + 学术影响力 0.5（log1p+min-max，20,183 人全覆盖）
  D2 产业力 = 所属机构专利件数（申请人聚合精确匹配，17,105 人有值；
              高校/院所的专利也计入，因此这是「机构技术产出规模」而不是企业营收）
  D4 深圳连接度 = 0.6 × 深圳合著强度 + 0.4 × 深圳履历/学历（0/1）
      深圳合著强度 = 该学者可锚定中文论文中「作者机构含深圳」的篇数 / 锚定论文数，
      再在候选池内 log1p+min-max；无锚定论文者该分量 None（不补 0），只用履历分量。
  D3 产品匹配度 = **缺**：`dwd_org_recruit_info` 只有岗位名/工作地/发布日期，无学历、技能、
      薪资要求；`dwd_org_industry_product_tags` 的 credit_code 与机构底册只有 3.5% 交集
      （DATA_FACTS §3.1），无法把候选人的研究与产品/岗位做逐人匹配。
权重 0.40 / 0.30 / 0.30（D3 缺失，按剩余三维归一）。

阈值：候选池 p90 / p70 / p40 切 A/B/C/D。

零 SQL：全部读 `code/_snapshots21/`。
产物：`code/M_TALENT_DEEP_164_1_out.json`。
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

METRIC = "M_TALENT_DEEP_164_1"


def main() -> None:
    rs = C.rows()
    k, d1, d2 = C.academic_k(rs)
    agg = C.org_patent()
    orgpat = {r["sid"]: (agg.get(r["org"], (None, None))[0]) for r in rs}

    pool_idx = [i for i, r in enumerate(rs)
                if r["city"] != "深圳市" and "深圳" not in (r["org"] or "")]
    # 深圳合著强度（只在有锚定论文的人里归一）
    anc = [i for i in pool_idx if rs[i]["np"] > 0]
    share = {i: rs[i]["nsz"] / rs[i]["np"] for i in anc}
    lo, hi = min(share.values()), max(share.values())
    lpaper = {i: (share[i] - lo) / (hi - lo) if hi > lo else 0.5 for i in anc}
    # 机构产业力归一（全池）
    withpat = [i for i in range(len(rs)) if orgpat[rs[i]["sid"]] is not None]
    pv = [orgpat[rs[i]["sid"]] for i in withpat]
    plo, phi = min(pv), max(pv)
    d2n = {i: (math.log1p(orgpat[rs[i]["sid"]]) - math.log1p(plo)) /
              (math.log1p(phi) - math.log1p(plo)) for i in withpat}

    score, dims, conn = [], [], []
    for i in pool_idx:
        r = rs[i]
        hist = 1.0 if (r["work_sz"] or r["edu_sz"]) else 0.0
        # 无锚定论文者：合著分量未观测，记 0（不等于无连接），只保留履历分量的 0.4 上限
        L = (0.6 * lpaper[i] + 0.4 * hist) if i in lpaper else 0.4 * hist
        parts = [(0.40, k[i]), (0.30, 100 * L)]
        if i in d2n:
            parts.append((0.30, 100 * d2n[i]))
        w = sum(p[0] for p in parts)
        score.append(round(sum(p[0] * p[1] for p in parts) / w, 4))
        dims.append(len(parts))
        conn.append(round(L, 4))
    cs = C.cuts(score)
    tiers = Counter(C.tier(s, cs) for s in score)

    pool_rows = [rs[i] for i in pool_idx]
    top = C.top(pool_rows, score, 30, extra=lambda j: {
        "K": k[pool_idx[j]], "conn": conn[j],
        "nsz": pool_rows[j]["nsz"], "np": pool_rows[j]["np"],
        "hist_sz": pool_rows[j]["work_sz"] + pool_rows[j]["edu_sz"],
        "org_pat": orgpat[pool_rows[j]["sid"]], "dims": dims[j]})
    conn_top = sorted(range(len(pool_idx)), key=lambda j: -conn[j])[:10]

    payload = {
        "metric": METRIC,
        "support_judgment": "部分支持",
        "support_reason": (
            "学术力（20,183 人全覆盖）、产业力（机构专利 17,105 人 = 84.75%）、深圳连接度"
            "（合著 465 人 / 履历 19 人）三维可算，但需求点名的「产品匹配度」没有数据：招聘表"
            "只有岗位名与工作地、无技能要求，产品标签表的 credit_code 与机构底册只有 3.5% 交集，"
            "无法逐人匹配；深圳连接度有合著信号的人只占 2.30% → 部分支持。"
        ),
        "method": {
            "pool": "当前机构不在深圳的有姓名学者（city≠深圳市 且机构名不含深圳）",
            "d1": "学术力 = 0.5*log-minmax(paper_nums) + 0.5*log-minmax(citation_nums)",
            "d2": "产业力 = 所属机构专利件数（申请人聚合精确匹配，org 不在聚合里则缺失）",
            "d4": "深圳连接度 = 0.6*深圳合著强度 + 0.4*深圳履历/学历；无锚定论文者合著记 0，连接度上限 0.4",
            "d3": "产品匹配度：缺（无岗位技能要求、无产品标签可对齐）",
            "weights": "0.40 / 0.30 / 0.30（D3 缺，剩余三维归一）",
            "thresholds": {"p90": cs[0], "p70": cs[1], "p40": cs[2]},
            "no_zero_fill": "无锚定论文的合著分量按未观测记 0（已在正文披露不等于无连接）；机构不在聚合里 D2 缺失，按剩余权重归一",
        },
        "pool": {"candidates": len(pool_idx), "with_org_patent": sum(1 for j in range(len(pool_idx))
                                                                     if pool_idx[j] in d2n),
                 "with_paper": len(anc), "with_sz_paper": sum(1 for i in anc if rs[i]["nsz"] > 0),
                 "with_sz_history": sum(1 for i in pool_idx if rs[i]["work_sz"] or rs[i]["edu_sz"]),
                 "with_any_signal": sum(1 for j in range(len(pool_idx)) if conn[j] > 0),
                 "strong_signal": sum(1 for j in range(len(pool_idx)) if conn[j] > 0.4),
                 "dims3": sum(1 for x in dims if x == 3), "dims2": sum(1 for x in dims if x == 2)},
        "dist": {"score": C.dist(score), "conn": C.dist(conn), "K": C.dist([k[i] for i in pool_idx])},
        "thresholds": {"p90": cs[0], "p70": cs[1], "p40": cs[2]},
        "tiers": {t: tiers.get(t, 0) for t in "ABCD"},
        "top30": top,
        "sz_connection_top10": [{"name": pool_rows[j]["name"], "org": pool_rows[j]["org"],
                                 "conn": conn[j], "nsz": pool_rows[j]["nsz"],
                                 "np": pool_rows[j]["np"],
                                 "hist_sz": pool_rows[j]["work_sz"] + pool_rows[j]["edu_sz"]}
                                for j in conn_top],
        "candidate_cities": Counter(r["city"] for r in pool_rows).most_common(12),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面口径：学术力取生涯累计两列，深圳连接度取全时段合著与履历，"
                            "不含年度窗口，故无基期年份。合著信号来自中文论文面板（1980—2026），"
                            "但本件不按年切分、不做增速，2017—2020 不参与任何分母。"),
        "probes": {"sql_count": 0, "patent_sql": 0,
                   "source": "gkx @ 183.240.141.251:3318（快照派生，零 SQL）"},
        "reused_from": "code/_snapshots21/talent22_panel_20261022.json（由 code/_build_talent22_panel.py 生成）",
    }
    C.write(METRIC, payload)
    print("pool", payload["pool"])
    print("dist", payload["dist"]["score"], "cuts", cs)
    print("top5", [(x["name"], x["score"], x["conn"]) for x in top[:5]])


if __name__ == "__main__":
    main()
