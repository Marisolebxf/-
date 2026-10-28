#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_TALENT_DS_16_TALENT_RECRUIT_010 —— 引进阻力量化评分。

需求：量化「把一名人才引进到深圳」的阻力，输出 0—100 评分与分档，供招引优先级排序。
需求未给因子。本文只取库内真实可测的四类阻力，缺一类就明说：

  R1 学术势能阻力（0.35）：h 指数与引用越高，越难被单点引进（议价能力强）。
     用学术力 K（0—100，20,420 人全覆盖）同向代理。
  R2 地理距离阻力（0.25）：现机构在深圳=0；广东省内非深圳=50；省外=100；
     机构城市未归属=100。深圳履历/学历可把 100 降到 70（有连接、阻力略低）。
  R3 流动惯性阻力（0.20）：履历表工作段数越少，越久未动，阻力越高。
     inertia = 100 × (1 − min((工作段数−1)/4, 1))；无履历数据=None。
  R4 头衔阻力（0.20）：`dwd_scholar_talent_flag.academician=1` 记 100，否则 0。
     院士 112 人，面板命中 80 人（talent_flag 与主档 scholar_id 直连）。

  缺：薪酬期望、家庭随迁、语言、签证/国籍、住房——全库 0 字段（见 005/006/013 的探针）。
  因此这是「四维可测阻力」，不是需求原意的「全阻力」。判 **部分支持**。

  权重 0.35/0.25/0.20/0.20，缺失维按剩余权重归一。阈值取 20,420 人内部 p90/p70/p40。

零 SQL：读 `code/_snapshots21/talent22_panel_20261022.json`。
产物：`code/M_TALENT_DS_16_TALENT_RECRUIT_010_out.json`。
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import _talent22_common as C  # noqa: E402

METRIC = "M_TALENT_DS_16_TALENT_RECRUIT_010"


def geo_resistance(r: dict) -> int:
    if r["city"] == "深圳市" or "深圳" in (r["org"] or ""):
        return 0
    if r["prov"] == "广东省":
        return 50
    if r["city"] == "未归属":
        return 100
    if r["work_sz"] or r["edu_sz"]:
        return 70
    return 100


def main() -> None:
    rs = C.rows()
    k, d1, d2 = C.academic_k(rs)
    score, parts_n = [], []
    dims = {"academic": [], "geo": [], "inertia": [], "title": []}
    for i, r in enumerate(rs):
        geo = geo_resistance(r)
        title = 100 if r["acad"] else 0
        parts = [(0.35, k[i]), (0.25, geo), (0.20, title)]
        inertia = None
        if r["work_filled"] > 0:
            inertia = 100 * (1 - min(max(r["work_n"] - 1, 0) / 4, 1))
            parts.append((0.20, inertia))
        w = sum(p[0] for p in parts)
        score.append(round(sum(p[0] * p[1] for p in parts) / w, 4))
        parts_n.append(len(parts))
        dims["academic"].append(k[i])
        dims["geo"].append(geo)
        dims["title"].append(title)
        if inertia is not None:
            dims["inertia"].append(inertia)

    cs = C.cuts(score)
    tiers = Counter(C.tier(s, cs) for s in score)
    top = C.top(rs, score, 30, extra=lambda j: {
        "academic": k[j], "geo": geo_resistance(rs[j]),
        "title": 100 if rs[j]["acad"] else 0,
        "work_n": rs[j]["work_n"], "acad": rs[j]["acad"],
        "dims": parts_n[j]})
    # 同名多 scholar_id 只留最高分（如刘忠范两行），否则榜上同一人被排两次
    seen, dedup = set(), []
    for x in top:
        if x["name"] in seen:
            continue
        seen.add(x["name"])
        dedup.append(x)
    for i, x in enumerate(dedup, 1):
        x["rank"] = i
    top = dedup

    payload = {
        "metric": METRIC,
        "title": "引进阻力量化评分",
        "support_judgment": "部分支持",
        "support_reason": (
            f"学术势能（{len(rs):,} 全覆盖）、地理距离（全覆盖）、流动惯性（{len(dims['inertia']):,} 人有履历）、"
            "头衔阻力（80 名院士在面板）四维可算；但薪酬期望、家庭、语言、签证四类阻力"
            "在 gkx 全库 0 字段，评分只覆盖「可测阻力」，不能当全阻力使用。"
        ),
        "method": {
            "r1": "学术势能 = 学术力 K（h 与引用 log-minmax 各半），权重 0.35",
            "r2": "地理距离：深圳 0 / 广东省内 50 / 省外 100 / 未归属 100；有深圳履历或学历的省外 70；权重 0.25",
            "r3": "流动惯性 = 100×(1−min((工作段数−1)/4,1))；无履历 None；权重 0.20",
            "r4": "头衔 = 院士 100 / 其他 0；权重 0.20",
            "weights": "0.35 / 0.25 / 0.20 / 0.20（缺失维归一）",
            "thresholds": {"p90": cs[0], "p70": cs[1], "p40": cs[2]},
            "no_zero_fill": "无履历者 R3=None，不按「从没动过」补 0；未归属城市按省外计，不补 0",
        },
        "coverage": {
            "scholars": len(rs),
            "with_inertia": len(dims["inertia"]),
            "academician_in_panel": sum(1 for r in rs if r["acad"]),
            "academician_total": 112,
            "in_sz": sum(1 for r in rs if r["city"] == "深圳市" or "深圳" in (r["org"] or "")),
            "guangdong_non_sz": sum(1 for r in rs if r["prov"] == "广东省"
                                    and r["city"] != "深圳市" and "深圳" not in (r["org"] or "")),
            "outside_guangdong": sum(1 for r in rs if r["prov"] not in ("广东省", "未归属")),
            "unknown_city": sum(1 for r in rs if r["city"] == "未归属"),
            "dims3": sum(1 for x in parts_n if x == 3),
            "dims4": sum(1 for x in parts_n if x == 4),
        },
        "dims": {kk: C.dist(v) for kk, v in dims.items()},
        "dist": {"score": C.dist(score)},
        "thresholds": {"p90": cs[0], "p70": cs[1], "p40": cs[2]},
        "tiers": {t: tiers.get(t, 0) for t in "ABCD"},
        "top30": top,
        "missing_barriers": [
            {"dim": "薪酬期望", "evidence": "salary|wage|compensation 0 列（37 个 cost 列均为企业分部财务）"},
            {"dim": "家庭随迁", "evidence": "无 spouse/child/family 字段"},
            {"dim": "语言", "evidence": "13 个 language 列均为论文/文档语种，无个人能力等级"},
            {"dim": "签证 / 国籍", "evidence": "nationality|visa|passport|residence_permit 0 列"},
            {"dim": "住房 / 安家", "evidence": "无 housing/settlement/allowance 字段"},
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面评分：学术力为生涯累计，地理为当前机构，头衔为当前标识；"
                            "仅流动惯性用履历段数（全时段），无年度窗口，故无基期。"),
        "probes": {"sql_count": 0, "patent_sql": 0,
                   "source": "gkx @ 183.240.141.251:3318（快照派生）"},
        "reused_from": ("code/_snapshots21/talent22_panel_20261022.json + "
                        "code/_snapshots21/talent_flag_20261022.json"),
    }
    C.write(METRIC, payload)
    print("coverage", payload["coverage"])
    print("dist", payload["dist"]["score"], "cuts", cs)
    print("top5", [(x["name"], x["org"], x["score"], x["acad"]) for x in top[:5]])


if __name__ == "__main__":
    main()
