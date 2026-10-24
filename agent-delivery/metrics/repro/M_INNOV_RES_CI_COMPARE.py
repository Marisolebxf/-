#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_RES_CI_COMPARE · 多企业竞争情报比对（0—100 等级 + 竞争矩阵 + 战略定位图）

口径（calc-logic 真源，需求原文 §9.3.3）
--------------------------------------
1. 竞争情报等级：overlap×100，≥P70 高、P30—P70 中、<P30 低；
2. 竞争矩阵：所选企业两两分值，n×n，对角=100；
3. 战略定位图：横轴=专利数+论文数，纵轴=平均 overlap。
对象＝**多家企业**。备注：派单标签写作「区域竞争力对比（CI=competitiveness index）」，
但 calc-logic 真源与需求原文均为「多企业竞争情报比对」，CI 指 competitive intelligence，
故本交付按企业口径实现；区域口径不在本 ID 的依赖范围内（见 MD §1.1 与 §三）。

数据面
------
与 M_INNOV_RES_OVERLAP 同源（零新增 SQL）：IPC4 集合来自 `patent_ipc4_by_name`，
论文规模来自 `probe_a26_ent_papers`（author_info_list 12 家企业计数，1 次扫描 100,900 行）。

运行：python3 code/M_INNOV_RES_CI_COMPARE.py
"""
from __future__ import annotations

import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _a26_common as C

MID = "M_INNOV_RES_CI_COMPARE"


def level_of(x: float, p30: float, p70: float) -> str:
    if x >= p70:
        return "高"
    if x >= p30:
        return "中"
    return "低"


def main() -> None:
    B = C.overlap_bundle(12)
    names = B["names"]
    rows = B["pairs"]
    pub = {e["name_cn"]: e["pub_cnt"] for e in B["enterprises"]}
    papers = B["papers"]

    # ---- 等级阈值（企业级：12 家的平均 overlap；企业对级：66 对）----
    ent_overlap = {n: round(100 * B["per_enterprise"][n]["avg_overlap"], 2) for n in names}
    ent_vals = [ent_overlap[n] for n in names]
    p30_ent, p70_ent = C.pct(ent_vals, 0.30), C.pct(ent_vals, 0.70)

    pair_vals = [round(100 * r["composite"], 2) for r in rows]
    p30_pair, p70_pair = C.pct(pair_vals, 0.30), C.pct(pair_vals, 0.70)

    ent_rows = []
    for n in names:
        peers = sorted((r for r in rows if n in (r["a"], r["b"])),
                       key=lambda r: -(r["composite"] or 0))
        top3 = [{"partner": (r["b"] if r["a"] == n else r["a"]),
                 "overlap": round(100 * r["composite"], 2),
                 "level": level_of(round(100 * r["composite"], 2), p30_pair, p70_pair)}
                for r in peers[:3]]
        ent_rows.append({
            "enterprise": n,
            "patents": pub[n],
            "papers": papers.get(n, 0),
            "size": pub[n] + papers.get(n, 0),
            "avg_overlap": ent_overlap[n],
            "max_overlap": B["per_enterprise"][n]["max_overlap"],
            "max_partner": B["per_enterprise"][n]["max_partner"],
            "level": level_of(ent_overlap[n], p30_pair, p70_pair),
            "top3": top3,
        })
    ent_rows.sort(key=lambda r: -r["avg_overlap"])

    # ---- 竞争矩阵（对角 100；非对角 composite×100 + 等级）----
    matrix_vals = []
    matrix_level = []
    for i, a in enumerate(names):
        vr, lr = [], []
        for j, b in enumerate(names):
            if i == j:
                vr.append(100.0)
                lr.append("自身")
            else:
                r = next(x for x in rows if {x["a"], x["b"]} == {a, b})
                v = round(100 * r["composite"], 2) if r["composite"] is not None else None
                vr.append(v)
                lr.append(level_of(v, p30_pair, p70_pair) if v is not None else "无数据")
        matrix_vals.append(vr)
        matrix_level.append(lr)

    # ---- 战略定位图：x=规模，y=平均 overlap；以中位数分四象限 ----
    med_size = statistics.median([r["size"] for r in ent_rows])
    med_overlap = statistics.median([r["avg_overlap"] for r in ent_rows])
    map_rows = []
    for r in ent_rows:
        x_hi = r["size"] >= med_size
        y_hi = r["avg_overlap"] >= med_overlap
        quad = ("规模领先·重叠高" if x_hi and y_hi else
                "规模领先·重叠低" if x_hi else
                "规模靠后·重叠高" if y_hi else "规模靠后·重叠低")
        map_rows.append({"enterprise": r["enterprise"], "size": r["size"],
                         "patents": r["patents"], "papers": r["papers"],
                         "avg_overlap": r["avg_overlap"], "quadrant": quad,
                         "level": r["level"]})

    # ---- 竞争对（去重后按重叠降序）----
    pair_rows = []
    for r in sorted(rows, key=lambda x: -(x["composite"] or 0)):
        v = round(100 * r["composite"], 2)
        pair_rows.append({"a": r["a"], "b": r["b"], "overlap": v,
                          "level": level_of(v, p30_pair, p70_pair),
                          "ipc_jaccard": r["ipc_jaccard"], "ipc_inter": r["ipc_inter"],
                          "ipc_union": r["ipc_union"]})

    level_dist = {}
    for r in ent_rows:
        level_dist[r["level"]] = level_dist.get(r["level"], 0) + 1
    # 敏感性：若改用企业自身的 P30/P70（相对分档），等级分布会变成机械的 4/4/4
    rel_level_dist = {}
    for r in ent_rows:
        lv = level_of(r["avg_overlap"], p30_ent, p70_ent)
        rel_level_dist[lv] = rel_level_dist.get(lv, 0) + 1
    pair_level_dist = {}
    for r in pair_rows:
        pair_level_dist[r["level"]] = pair_level_dist.get(r["level"], 0) + 1

    res = {
        "metric_id": MID,
        "metric_name": "多企业竞争情报比对",
        "dispatch_label": "派单标签为「区域竞争力对比（CI=competitiveness index）」",
        "naming_discrepancy": "calc-logic 真源与需求原文 §9.3.3 均为多企业竞争情报比对（CI=competitive "
                              "intelligence），本交付按企业口径；区域口径需另立指标与区域集合",
        "naming_resolution": "已裁定（2026-10-22，用户拍板）：本 ID 保持企业口径不变，"
                             "区域竞争力指数另立 M_INNOV_RES_REGION_CI，两件互不复用分母",
        "support_judgment": "部分支持",
        "object": "企业对企业（明星企业池 Top 12）",
        "generated_from": "与 M_INNOV_RES_OVERLAP 同源：patent_ipc4_by_name + probe_a26 scholar dump + "
                          "probe_a26_ent_papers（论文规模）",
        "sql_count": 0,
        "method": {
            "level": "overlap×100；≥P70 高、P30—P70 中、<P30 低（统一用 66 对的 P30/P70，"
                     "企业级与矩阵同一把尺）",
            "level_thresholds": {
                "primary": {"p30": p30_pair, "p70": p70_pair, "n": len(pair_vals),
                            "scope": "66 对企业对"},
                "enterprise_relative_sensitivity": {"p30": p30_ent, "p70": p70_ent,
                                                    "n": len(ent_vals),
                                                    "note": "仅作敏感性：企业间 43.4—48.2 过于密集，"
                                                            "相对分档会机械地切成 4/4/4"},
            },
            "matrix": "n×n，对角=100；非对角=composite×100",
            "map": "横轴=专利件数+中文论文篇数；纵轴=企业平均 overlap×100；四象限按两轴中位数切分",
            "overlap_reuse": "直接复用研究领域重叠度（同 ID 口径），不另立领域维",
        },
        "universe": {
            "n_enterprises": len(names),
            "names": names,
            "patent_counts": pub,
            "paper_counts": papers,
            "selection": "star_roster（授权≥50、已剔除非企业）按 pub_cnt Top 12",
        },
        "levels": {
            "enterprise": ent_rows,
            "enterprise_level_dist": level_dist,
            "enterprise_level_dist_relative_sensitivity": rel_level_dist,
            "pair_level_dist": pair_level_dist,
            "pairs_high": sum(1 for r in pair_rows if r["level"] == "高"),
            "pairs_mid": sum(1 for r in pair_rows if r["level"] == "中"),
            "pairs_low": sum(1 for r in pair_rows if r["level"] == "低"),
        },
        "matrix": {"labels": names, "values": matrix_vals, "levels": matrix_level},
        "strategic_map": {"x_median_size": med_size, "y_median_overlap": med_overlap,
                          "points": map_rows,
                          "quadrant_counts": {q: sum(1 for r in map_rows if r["quadrant"] == q)
                                              for q in sorted({r["quadrant"] for r in map_rows})}},
        "pairs": pair_rows,
        "coverage": {
            "n_pairs": len(rows),
            "pairs_with_scholar_signal": sum(1 for r in rows if (r["scholar_jaccard"] or 0) > 0),
            "keyword_dim_usable": False,
            "overlap_is_ipc_only": True,
            "ent_with_papers": sum(1 for n in names if papers.get(n, 0) > 0),
            "ent_without_papers": [n for n in names if not papers.get(n, 0)],
            "paper_source_note": "论文篇数=author_info_list 子串命中（含合作署名），非第一单位口径",
        },
        "base_year_block": C.base_year_block(
            [], [], "竞争矩阵为截面比对，无年度分母；专利为全历史并集，论文为库内 100,900 篇切片"),
        "gaps": [
            "重叠度实际只有 IPC 单维：学者维 0/66 对有双端数据，关键词维不可用",
            "IPC4 为小类粒度，12 家大厂两两 Jaccard 全部 ≥0.18，区分度被粒度稀释",
            "论文规模用子串匹配，包含合作署名，且 3 家为 0 篇（荣耀、广州供电局、深圳供电局）",
            "等级阈值只有 12 家企业/66 对，P30/P70 的统计稳定性有限",
        ],
    }
    C.write_out(MID, res)
    print(json.dumps({k: res[k] for k in ("support_judgment", "levels")}, ensure_ascii=False, indent=1)[:2500])
    print("map:", json.dumps(map_rows, ensure_ascii=False, indent=1)[:1500])


if __name__ == "__main__":
    main()
