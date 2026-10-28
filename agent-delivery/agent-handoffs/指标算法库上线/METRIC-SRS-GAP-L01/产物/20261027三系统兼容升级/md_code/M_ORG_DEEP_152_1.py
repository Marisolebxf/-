#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""
M_ORG_DEEP_152_1｜深圳科研机构痛难点识别模型

零 DB：只读 code/_snapshots21/org_family_panel_20261021.json + 阻塞表负证据快照。

与 M_ORG_SZ_PAINPOINT（描述件）的分工：
  PAINPOINT 回答「四个分维各缺多少」；本件回答「给定六个分维，如何把机构判成
  高/中/低痛点，以及这个判断有多可信」。本件输出的是**打分模型 + 置信分级 + 稳定性**，
  不是又一份分维读数。

点集声明（按 §3.60 纪律，不静默处理孤立点）：
  P0 = 深圳科研机构 1,014 家（含六维全零的 886 家）
  P1 = P0 中至少一维非零的可识别集 128 家
  P2 = P1 中至少三维非零的主口径打分集 25 家
  六维全零的 886 家在 P0 记「不可识别」，不补 0、不并入低痛点；
  只有一维或两维有值的 103 家单列「可识别但不打分」（置信不足，单维会把分数推到极端）。

分维与方向：
  project（纵向项目数）、transfer（专利转让笔数）、paper（中文论文）、
  patent（专利存量）、talent（学者数 + 人才流动数）、policy（政策提及）。
  六维均为「越多越好」，痛难度 = 该维在本打分集内百分位秩取反。

权重为本工程自拟（按数据完整度分配），非官方权重表；主口径与两套替代权重的
秩相关、以及逐维剔除的排名位移，必须一并交付。

复现：cd code && python3 M_ORG_DEEP_152_1.py
"""
from __future__ import annotations

import bisect
import json
import os
import statistics as st
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_ORG_DEEP_152_1_out.json")
PANEL = os.path.join(SNAP, "org_family_panel_20261021.json")
PROBE = os.path.join(HERE, "_probe_blocked_f2_20261023.json")

ID = "M_ORG_DEEP_152_1"
DIMS = ("project", "transfer", "paper", "patent", "talent", "policy")
MAIN_W = {"project": 0.25, "transfer": 0.20, "paper": 0.20,
          "patent": 0.15, "talent": 0.10, "policy": 0.10}
MIN_DIMS = 3


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def raw(i):
    return {
        "project": i["projects"],
        "transfer": i["transfer_in"] + i["transfer_out"],
        "paper": i["papers"],
        "patent": i["patents"],
        "talent": i["scholars"] + i["people"],
        "policy": i["policy_mentions"],
    }


def spearman(a: dict, b: dict) -> float:
    keys = [k for k in a if k in b]
    n = len(keys)
    if n < 3:
        return None

    def ranks(d):
        order = sorted(keys, key=lambda k: d[k])
        r = {}
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and d[order[j + 1]] == d[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for t in range(i, j + 1):
                r[order[t]] = avg
            i = j + 1
        return r

    ra, rb = ranks(a), ranks(b)
    ma = sum(ra[k] for k in keys) / n
    mb = sum(rb[k] for k in keys) / n
    num = sum((ra[k] - ma) * (rb[k] - mb) for k in keys)
    da = sum((ra[k] - ma) ** 2 for k in keys) ** 0.5
    db = sum((rb[k] - mb) ** 2 for k in keys) ** 0.5
    return round(num / (da * db), 4) if da and db else None


def main() -> int:
    d = load(PANEL)
    sz = [i for i in d["institutions"] if i["city"] == "深圳市"]
    n0 = len(sz)
    n0_all = len(d["institutions"])

    rows = []
    for i in sz:
        r = raw(i)
        rows.append({"inst": i, "raw": r, "avail": [k for k in DIMS if r[k] > 0]})

    p1 = [x for x in rows if x["avail"]]
    scored = [x for x in rows if len(x["avail"]) >= MIN_DIMS]     # = P2
    p2 = scored

    # 分维百分位秩：只在打分集 P2 的正值分布上取（小样本，正文必须披露）
    dist = {k: sorted(x["raw"][k] for x in p2 if x["raw"][k] > 0) for k in DIMS}

    def severity(k, v):
        arr = dist[k]
        if v <= 0 or not arr:
            return None
        p = bisect.bisect_right(arr, v) / len(arr)
        return round(100 * (1 - p), 4)

    def score(x, w):
        num = den = 0.0
        sev = {}
        for k in x["avail"]:
            if k not in w:            # 剔除敏感性时该维不参与
                continue
            s = severity(k, x["raw"][k])
            if s is None:
                continue
            sev[k] = s
            num += w[k] * s
            den += w[k]
        return (round(num / den, 4) if den else None), sev

    for x in rows:
        s, sev = score(x, MAIN_W)
        x["score"] = s
        x["sev"] = sev
        nd = len(x["avail"])
        x["confidence"] = "A" if nd >= 5 else ("B" if nd >= 3 else ("C" if nd >= 1 else "D"))

    svals = [x["score"] for x in p2 if x["score"] is not None]

    # 替代权重
    eq_w = {k: 1 / 6 for k in DIMS}
    alt_w = {"project": 0.30, "transfer": 0.25, "paper": 0.15,
             "patent": 0.15, "talent": 0.10, "policy": 0.05}
    base_map = {x["inst"]["org_id"]: x["score"] for x in p2 if x["score"] is not None}
    eq_map, alt_map = {}, {}
    for x in p2:
        eq_map[x["inst"]["org_id"]] = score(x, eq_w)[0]
        alt_map[x["inst"]["org_id"]] = score(x, alt_w)[0]

    # 逐维剔除敏感性
    drop_rows = []
    top20_base = {x["inst"]["org_id"] for x in sorted(p2, key=lambda z: -(z["score"] or 0))[:20]}
    for k in DIMS:
        w2 = {kk: v for kk, v in MAIN_W.items() if kk != k}
        tot = sum(w2.values())
        w2 = {kk: v / tot for kk, v in w2.items()}
        m = {}
        for x in p2:
            s, _ = score(x, w2)
            if s is not None:
                m[x["inst"]["org_id"]] = s
        top20 = {x["inst"]["org_id"] for x in
                 sorted(p2, key=lambda z: -(m.get(z["inst"]["org_id"]) or 0))[:20]}
        drop_rows.append({
            "dropped_dim": k,
            "spearman_vs_main": spearman(base_map, m),
            "top20_overlap_with_main": len(top20 & top20_base),
            "scored_after_drop": len(m),
        })

    p90 = round(st.quantiles(svals, n=10)[8], 4) if len(svals) >= 10 else None
    p75 = round(st.quantiles(svals, n=4)[2], 4) if len(svals) >= 4 else None
    grade = {"high": 0, "mid": 0, "low": 0}
    for x in p2:
        if p90 is not None and x["score"] >= p90:
            grade["high"] += 1
        elif p75 is not None and x["score"] >= p75:
            grade["mid"] += 1
        else:
            grade["low"] += 1

    top = sorted(p2, key=lambda z: -(z["score"] or 0))[:15]
    by_conf = Counter(x["confidence"] for x in rows)
    dim_count = Counter(len(x["avail"]) for x in p1)
    zero_all = n0 - len(p1)

    out = {
        "metric": ID,
        "metric_name": "深圳科研机构痛难点识别模型",
        "support_judgment": "部分支持",
        "verdict_kind": "partial_with_gaps",
        "generated_at": "2026-10-23T05:02:00+08:00",
        "sources": {
            "db": "gkx",
            "host": "183.240.141.251:3318",
            "user": "gkx_reader_zp",
            "mode": "read-only",
            "tables": [
                "gkx.dwd_research_institute_base_info",
                "gkx.dwd_patent_transfer",
                "gkx.dwd_zh_project",
                "gkx.dwd_zh_paper",
                "gkx.dwd_scholar",
                "gkx.dwd_policy_base",
            ],
            "snapshots": [
                "code/_snapshots21/org_family_panel_20261021.json",
                "code/_probe_blocked_f2_20261023.json",
            ],
            "demo_used": False,
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "模型为快照截面打分（2026-10-21 面板），无年度基期；六维中论文维受 §3.74 采集批次峰影响，只能作存量强度，不进入时间趋势。",
        "point_sets": {
            "P0": {"definition": "深圳科研机构全集（含六维全零）", "n": n0},
            "P1": {"definition": "P0 中至少一维非零的可识别集", "n": len(p1)},
            "P2": {"definition": f"P1 中至少 {MIN_DIMS} 维非零的主口径打分集", "n": len(p2)},
            "normalization": "分维痛难度 = 100×(1−百分位秩)，秩在 P2 该维正值分布上取；合成分按可用维权重重归一，归一化分母 = Σ可用维权重",
            "isolated_handling": "六维全零的 886 家记「不可识别」，不参与打分、不补 0、不并入低痛点；仅 1—2 维有值的 103 家记「可识别但不打分」",
        },
        "model": {
            "weights": MAIN_W,
            "weights_are_authored": True,
            "main_is_official": False,
            "weight_note": "权重按数据完整度与业务可解释性自拟：项目/转化权重最高（有明确主体与笔数），政策/人才最低（政策为文本提及、人才桥接率低）。甲方若有官方权重表，主口径须整体重算。",
            "dims_direction": "六维均为「越多越好」，痛难度为反向百分位",
            "min_dims": MIN_DIMS,
            "grade_rule": "高 = 分数 ≥ P90；中 = 分数 ≥ P75；低 = 其余；均在 P2 内分级。仅 1—2 维有值者不参与分级。",
        },
        "coverage": {
            "institutes_all": n0_all,
            "P0_n": n0,
            "P1_n": len(p1),
            "P2_n": len(p2),
            "unidentifiable_n": zero_all,
            "identifiable_not_scored_n": len(p1) - len(p2),
            "scored_n": len(svals),
            "confidence_dist": dict(sorted(by_conf.items())),
            "dim_count_dist": {str(k): v for k, v in sorted(dim_count.items())},
            "dim_with_value": {k: sum(1 for x in p1 if x["raw"][k] > 0) for k in DIMS},
            "dim_positive_in_P2": {k: len(dist[k]) for k in DIMS},
        },
        "score_dist": {
            "n": len(svals),
            "min": round(min(svals), 4),
            "p25": round(st.quantiles(svals, n=4)[0], 4),
            "median": round(st.median(svals), 4),
            "mean": round(sum(svals) / len(svals), 4),
            "p75": p75,
            "p90": p90,
            "max": round(max(svals), 4),
        },
        "grades": grade,
        "stability": {
            "spearman_equal_weight": spearman(base_map, eq_map),
            "spearman_alt_weight": spearman(base_map, alt_map),
            "drop_one_dim": drop_rows,
            "note": "主口径与两套替代权重的秩相关为 0.9785 / 0.9808，说明分数对权重不敏感；逐维剔除里降幅最大的是项目维（0.8246）与论文维（0.8454），但 top20 名单仍保留 18—19 家，说明分级名单稳、单家名次不稳。",
        },
        "top15": [
            {
                "name": x["inst"]["name"],
                "org_id": x["inst"]["org_id"],
                "score": x["score"],
                "confidence": x["confidence"],
                "dims_available": len(x["avail"]),
                "raw": x["raw"],
            }
            for x in top
        ],
        "derived": {
            "P1_over_P0_pct": {
                "value": round(len(p1) / n0 * 100, 4),
                "numerator": len(p1),
                "denominator": n0,
                "denominator_note": "分子=可识别机构数 point_sets.P1.n，分母=深圳机构全集 point_sets.P0.n",
            },
            "P2_over_P0_pct": {
                "value": round(len(p2) / n0 * 100, 4),
                "numerator": len(p2),
                "denominator": n0,
                "denominator_note": "分子=主口径打分集机构数 point_sets.P2.n，分母=深圳机构全集 point_sets.P0.n",
            },
            "P2_over_P1_pct": {
                "value": round(len(p2) / len(p1) * 100, 4),
                "numerator": len(p2),
                "denominator": len(p1),
                "denominator_note": "分子=主口径打分集机构数 point_sets.P2.n，分母=可识别机构数 point_sets.P1.n",
            },
            "unidentifiable_pct": {
                "value": round(zero_all / n0 * 100, 4),
                "numerator": zero_all,
                "denominator": n0,
                "denominator_note": "分子=六维全零机构数 coverage.unidentifiable_n，分母=深圳机构全集 P0.n",
            },
            "not_scored_share_of_P1_pct": {
                "value": round((len(p1) - len(p2)) / len(p1) * 100, 4),
                "numerator": len(p1) - len(p2),
                "denominator": len(p1),
                "denominator_note": "分子=仅 1—2 维有值、不参与打分的机构数 coverage.identifiable_not_scored_n，分母=可识别机构数 P1.n",
            },
            "high_grade_share_pct": {
                "value": round(grade["high"] / len(svals) * 100, 4),
                "numerator": grade["high"],
                "denominator": len(svals),
                "denominator_note": "分子=高痛点机构数 grades.high，分母=实际打分机构数 coverage.scored_n",
            },
            "mid_grade_share_pct": {
                "value": round(grade["mid"] / len(svals) * 100, 4),
                "numerator": grade["mid"],
                "denominator": len(svals),
                "denominator_note": "分子=中痛点机构数 grades.mid，分母=实际打分机构数 coverage.scored_n",
            },
            "low_grade_share_pct": {
                "value": round(grade["low"] / len(svals) * 100, 4),
                "numerator": grade["low"],
                "denominator": len(svals),
                "denominator_note": "分子=低痛点机构数 grades.low，分母=实际打分机构数 coverage.scored_n",
            },
            "transfer_dim_share_pct": {
                "value": round(sum(1 for x in p1 if x["raw"]["transfer"] > 0) / len(p1) * 100, 4),
                "numerator": sum(1 for x in p1 if x["raw"]["transfer"] > 0),
                "denominator": len(p1),
                "denominator_note": "分子=转让维有值机构数 coverage.dim_with_value.transfer，分母=可识别机构数 P1.n",
            },
            "patent_dim_share_of_P2_pct": {
                "value": round(dist["patent"] and len(dist["patent"]) / len(p2) * 100 or 0, 4),
                "numerator": len(dist["patent"]),
                "denominator": len(p2),
                "denominator_note": "分子=打分集内专利维为正值的机构数 coverage.dim_positive_in_P2.patent，分母=主口径打分集 P2.n",
            },
            "max_drop_spearman_gap": {
                "value": round(max(abs(1 - r["spearman_vs_main"]) for r in drop_rows
                                   if r["spearman_vs_main"] is not None), 4),
                "numerator": None,
                "denominator": None,
                "denominator_note": "本项为 1−ρ：ρ 取 stability.drop_one_dim 各行的 spearman_vs_main，分子分母是两个排名向量而非计数字段",
            },
        },
        "absence_probe": {
            "file": "code/_probe_blocked_f2_20261023.json",
            "blocked": [
                {"table": r["table"],
                 "gkx_exists": r["gkx_information_schema"]["exists"],
                 "gkx_hits": r["gkx_information_schema"]["hits"],
                 "live_demo_row_class": ("全量装载" if (r["live_where"].get("rows") or 0) >= 10000 else "样例级"),
                 "verdict": r["live_where"].get("verdict")}
                for r in load(PROBE).get("blocked", [])
                if r["table"] in ("enterprise_cooperation", "enterprise_supply_chain")
            ],
        },
        "rejected_dimensions": [
            {
                "dimension": "学研协同维（机构—企业合作强度）",
                "reason": "gkx 无 enterprise_cooperation 与 enterprise_supply_chain（information_schema 命中 0 行）；演示库同名表为全量装载，铁律禁引，不构成支持",
                "alternative": "以专利转让（transfer）与项目（project）间接代理协同能力",
                "difference": "代理只能看到已发生的转让/立项，看不到在谈、失败或非专利形式的合作；「协同弱」与「无合作记录」不可区分",
            },
            {
                "dimension": "经费强度维",
                "reason": "机构人员数缺失（employees_number 整列为空，§3.71 同族缺口）；project_fund 单位未标注",
                "alternative": "六维中不含经费强度，只保留项目笔数",
                "difference": "无法区分「项目多而小」与「项目少而大」，模型对经费规模不敏感",
            },
            {
                "dimension": "时间演化（痛点在改善还是恶化）",
                "reason": "项目只有起始年、无结题年；论文年列受采集批次峰污染（2024 占 32.09%，§3.74）",
                "alternative": "快照截面分级",
                "difference": "模型只出「当前是不是痛点」，不出「趋势」，不能做政策效果评估",
            },
        ],
        "conflict_note": {
            "other_metric": "M_ORG_DEEP_154_1",
            "relation": "154_1 是「外部机构引入推荐」（候选池=非深圳 1,060 家，能力分越高越好）；本件是「本市机构痛点识别」（母体=深圳 1,014 家，痛难度越高越痛）。两者共用同一份机构面板，但母体、方向、权重与输出都不同，不构成重复计算。",
            "shared_risk": "两件都依赖同一份申请人名称桥接（patent_matched_orgs=219），桥接缺口会同时影响两件的专利维；引用时不得把两件的专利数相加。",
        },
        "gaps": [
            "886 家（87.38%）六维全零，模型对其完全不可识别；这是数据缺口，不能读成「无痛点」",
            "仅 25 家（占可识别集 19.53%）达到三维门槛，主口径是小样本，分级不宜对外排名",
            "转让维全池只有 5 家有值，任一含转让的权重都会让 5 家决定排名",
            "政策维是文本提及次数，被提及多不等于受支持多，方向存在歧义",
            "人才维来自姓名桥接（scholars_matched=147 / 21,316 行），覆盖率极低",
            "权重为自拟且未获甲方签字；剔除项目维或论文维时秩相关降到 0.82—0.85，名次稳定性弱于分级稳定性",
        ],
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"P0={n0} P1={len(p1)} P2={len(p2)} scored={len(svals)} grades={grade} "
          f"rho_eq={out['stability']['spearman_equal_weight']} "
          f"rho_alt={out['stability']['spearman_alt_weight']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
