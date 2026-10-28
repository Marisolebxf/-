#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_TALENT_DS_16_TALENT_RECRUIT_025 —— 团队组合与协同分析。

需求：分析团队的人员组合与协同效应，输出团队协同度、互补组合建议。
判定：**部分支持**。
  可算：当前机构在深的 237 名学者里 67 人有 20+8 技术聚类命中，可按机构组成团队，算
    - 方向覆盖（团队命中的不同聚类数 / 在深池命中的 16 个聚类）
    - 方向重叠（成员聚类集合的两两 Jaccard 均值，越高越同质）
    - 引用均衡（1 − 基尼系数，越高越均衡）
    - 合作证据（同机构内部 coauthor 边 / 可能边数）
  不可算：团队产出、项目共担、角色分工、年龄/职级——全库无字段；论文关键词只有
    人数很少，无法做「技能互补」的细粒度匹配；coauthor 边在深圳机构内部只有个位数，
    密度不足 0.4%，不足以支撑「协同效应」的因果结论。
  因此本件输出的是「组合结构指标」，不是「团队绩效预测」。

口径：
  团队 = 当前机构在深、人数 ≥3 的学者；机构别名归一（哈工大深圳 3 种写法合并为 1 队）。
  协同结构分 = 0.45×方向覆盖 + 0.30×(1−方向重叠) + 0.25×引用均衡，均归一到 0—100。
  互补组合 = 同机构、聚类集合不相交、且无既有合著边的两人，按 min(K) 与并集覆盖排序。

零 SQL：读 `code/_snapshots21/talent22_panel_20261022.json`。
产物：`code/M_TALENT_DS_16_TALENT_RECRUIT_025_out.json`。
"""
from __future__ import annotations

import itertools
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import _talent22_common as C  # noqa: E402

METRIC = "M_TALENT_DS_16_TALENT_RECRUIT_025"


def gini(vals: list[float]) -> float | None:
    v = sorted(vals)
    n = len(v)
    s = sum(v)
    if not n or s <= 0:
        return None
    return sum((2 * i - n - 1) * x for i, x in enumerate(v, 1)) / (n * s)


def main() -> None:
    rs = C.rows()
    k, d1, d2 = C.academic_k(rs)
    panel = json.loads((HERE / "_snapshots21" / "talent22_panel_20261022.json")
                       .read_text(encoding="utf-8"))
    edge = set()
    for a, b, _n in panel["pairs"]:
        edge.add((a, b))
        edge.add((b, a))

    # 团队只统计「当前机构在深」的学者；仅有深圳履历/学历、当前在外地者不入团队，
    # 否则会出现「机构在哈尔滨/广州的深圳校友团队」这种伪团队。
    sz = [i for i, r in enumerate(rs) if C.is_sz(r)]

    def canon(org: str) -> str:
        """机构别名归一：哈工大深圳在库内有 3 种写法（10 / 5 / 4 人），不归一会被拆成 3 个队。"""
        o = (org or "").strip()
        if o.startswith("哈尔滨工业大学") and "深圳" in o:
            return "哈尔滨工业大学（深圳）"
        return o
    universe = sorted({c for i in sz for c in rs[i]["cl"]})
    byid = {rs[i]["sid"]: i for i in sz}
    internal_edges = sum(1 for a, b, _n in panel["pairs"]
                         if a in byid and b in byid) // 2

    teams = []
    for org, n in Counter(canon(rs[i]["org"]) for i in sz).most_common():
        if n < 3:
            continue
        idx = [i for i in sz if canon(rs[i]["org"]) == org]
        cls = sorted({c for i in idx for c in rs[i]["cl"]})
        jac = []
        for a, b in itertools.combinations(idx, 2):
            A, B = set(rs[a]["cl"]), set(rs[b]["cl"])
            u = A | B
            if u:
                jac.append(len(A & B) / len(u))
        overlap = round(100 * statistics.mean(jac), 2) if jac else None
        poss = n * (n - 1) / 2
        e = sum(1 for a, b in itertools.combinations(idx, 2)
                if (rs[a]["sid"], rs[b]["sid"]) in edge)
        dens = round(100 * e / poss, 4) if poss else 0.0
        g = gini([float(rs[i]["cite"] or 0) for i in idx])
        balance = round(100 * (1 - g), 2) if g is not None else None
        cov = round(100 * len(cls) / len(universe), 2) if universe else 0.0
        parts = [(0.45, cov)]
        if overlap is not None:
            parts.append((0.30, 100 - overlap))
        if balance is not None:
            parts.append((0.25, balance))
        w = sum(p[0] for p in parts)
        teams.append({
            "org": org, "n": n, "clusters": len(cls), "coverage_pct": cov,
            "overlap_pct": overlap, "coauthor_edges": e, "density_pct": dens,
            "cite_gini": round(g, 4) if g is not None else None, "balance_pct": balance,
            "synergy": round(sum(p[0] * p[1] for p in parts) / w, 4),
            "with_cluster": sum(1 for i in idx if rs[i]["cl"]),
            "median_cite": statistics.median([rs[i]["cite"] or 0 for i in idx]),
        })
    teams.sort(key=lambda x: -x["synergy"])

    # 互补组合：同机构、聚类不相交、无既有合著边
    cands, seen_pair = [], set()
    for org in {t["org"] for t in teams}:
        idx = [i for i in sz if canon(rs[i]["org"]) == org and rs[i]["cl"]]
        for a, b in itertools.combinations(idx, 2):
            A, B = set(rs[a]["cl"]), set(rs[b]["cl"])
            if A & B:
                continue
            if (rs[a]["sid"], rs[b]["sid"]) in edge:
                continue
            union = len(A | B)
            key = tuple(sorted((rs[a]["name"], rs[b]["name"])))
            if key in seen_pair:
                continue
            seen_pair.add(key)
            cands.append({
                "org": org,
                "a": rs[a]["name"], "b": rs[b]["name"],
                "a_clusters": sorted(A), "b_clusters": sorted(B),
                "union_clusters": union,
                "min_K": round(min(k[a], k[b]), 2),
                "a_cite": rs[a]["cite"], "b_cite": rs[b]["cite"],
                "pair_score": round(0.6 * min(k[a], k[b]) + 0.4 * min(union / 4 * 100, 100), 2),
            })
    cands.sort(key=lambda x: -x["pair_score"])

    payload = {
        "metric": METRIC,
        "title": "团队组合与协同分析",
        "support_judgment": "部分支持",
        "support_reason": (
            f"在深 {len(sz)} 名学者中 {sum(1 for i in sz if rs[i]['cl'])} 人有 20+8 聚类"
            f"（可算方向覆盖与重叠）、全池可算引用均衡、coauthor 边 {len(panel['pairs']):,} 条"
            f"可算内部合作密度；但团队产出、项目共担、角色分工、年龄职级全库无字段，"
            f"关键词仅 {sum(1 for i in sz if rs[i]['kws'])}/{len(sz)} 非空，"
            f"深圳机构内部合作边仅 {internal_edges} 条"
            f"（密度 0.0%—{max(t['density_pct'] for t in teams) if teams else 0}%），"
            "协同效应本身无法验证。"
        ),
        "method": {
            "team": f"当前机构在深、人数≥3 的学者团队（机构别名归一，如哈工大深圳 3 种写法合并）；{len(teams)} 个团队 / {sum(t['n'] for t in teams)} 人",
            "coverage": "团队命中不同聚类数 / 在深池 16 个聚类，×100",
            "overlap": "成员两两聚类 Jaccard 均值，×100；无聚类对则不参与",
            "balance": "1 − 引用基尼系数，×100",
            "density": "同机构内部 coauthor 边 / C(n,2)，×100（仅披露，不入分）",
            "synergy": "0.45×覆盖 + 0.30×(1−重叠) + 0.25×均衡，缺失维归一",
            "pair_rule": "同机构、聚类不相交、无既有合著边；pair_score=0.6×min(K)+0.4×min(并集/4,1)×100",
            "no_zero_fill": "无聚类的团队 overlap=None 不入分；引用全 0 时 gini=None，balance=None",
        },
        "coverage": {
            "sz_scholars": len(sz), "with_cluster": sum(1 for i in sz if rs[i]["cl"]),
            "cluster_universe": len(universe), "teams": len(teams),
            "team_members": sum(t["n"] for t in teams),
            "sz_internal_coauthor_edges": internal_edges,
            "sz_pairs_total": len(panel["pairs"]),
            "with_keywords": sum(1 for i in sz if rs[i]["kws"]),
            "max_density_pct": max(t["density_pct"] for t in teams),
        },
        "teams": teams,
        "pairs_top20": cands[:20],
        "dist": {"team_synergy": C.dist([t["synergy"] for t in teams]),
                 "coverage_pct": C.dist([t["coverage_pct"] for t in teams]),
                 "density_pct": C.dist([t["density_pct"] for t in teams])},
        "missing": [
            {"dim": "团队产出（论文/专利/项目）", "evidence": "无 team_id，论文与专利只能回到个人；无法归集到团队"},
            {"dim": "项目共担", "evidence": "无项目成员表；`dwd_bid_*` 是中标的招标项目，无参与人"},
            {"dim": "角色分工", "evidence": "work_experience 只有 position 文本，团队内角色无字段"},
            {"dim": "年龄 / 职级", "evidence": "主档无 birth/age/title 字段；职称只在 position 文本里"},
            {"dim": "技能互补细粒度", "evidence": f"论文关键词仅 {sum(1 for i in sz if rs[i]['kws'])}/{len(sz)} 在深学者非空，无法做技能向量"},
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面口径：聚类来自全时段锚定论文，引用为生涯累计，合作为全时段边；"
                            "不做年度团队存续/流动分析，故无基期。"),
        "probes": {"sql_count": 0, "patent_sql": 0,
                   "source": "gkx @ 183.240.141.251:3318（快照派生）"},
        "reused_from": "code/_snapshots21/talent22_panel_20261022.json（由 code/_build_talent22_panel.py 生成）",
    }
    C.write(METRIC, payload)
    print("coverage", payload["coverage"])
    print("teams", [(t["org"], t["n"], t["synergy"]) for t in teams[:5]])
    print("pairs", [(x["a"], x["b"], x["pair_score"]) for x in cands[:5]])


if __name__ == "__main__":
    main()
