#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_DS_09_RESEARCH_004 多企业竞争情报比对 — 20261021 换源复现脚本

口径（王惠，calc-logic/INNOV/M_INNOV_RES_CI_COMPARE.md）：
  三维：竞争情报等级 / 竞争矩阵 / 战略定位图。
  - 竞争情报等级：overlap×100，≥P70 高、P30–P70 中、<P30 低（与 003 同阈值）
  - 竞争矩阵：所选企业两两分值 n×n，对角 = 100
  - 战略定位图：横轴 = 规模（专利数 + 论文数），纵轴 = 平均 overlap

数据面（20261021）：复用 002 在**三方库 gkx** 上重建的特征缓存
  `_snapshots21/research_feature_cache_20261021.json`。

产物：M_INNOV_DS_09_RESEARCH_004_out.json
"""
import time
from pathlib import Path
from statistics import mean, median

import _inn_res21_common as C

HERE = Path(__file__).parent
MID = "M_INNOV_DS_09_RESEARCH_004"
DB = "gkx@183.240.141.251:3318"
CACHE_NAME = "research_feature_cache_20261021.json"
MATRIX_FIRMS = 10


def main():
    t0 = time.time()
    c = C.load_cache(CACHE_NAME)
    if not c:
        raise SystemExit("缺少特征缓存，请先运行 M_INNOV_DS_09_RESEARCH_002.py")
    out = {"metric_id": MID, "name": "多企业竞争情报比对", "formula_owner": "王惠",
           "run_at": time.strftime("%Y-%m-%d %H:%M:%S"), "cache_built_at": c["built_at"],
           "db": DB, "probes": {}, "matrix": {}, "positioning": [], "quadrants": {},
           "grade_matrix": {}, "disclosures": [], "support_judgment": None}

    inv = C.inventory()
    for t in ["dwd_patent", "dwd_zh_paper", "dwd_zh_author", "dwd_org_base_info"]:
        out["probes"][t] = int(inv[t]["rows"])
    out["probes"]["cache_universe"] = len(c["names"])
    out["probes"]["db"] = DB

    p70, p30 = c["thresholds"]["p70_all_pairs"], c["thresholds"]["p30_all_pairs"]
    pairs = [p for p in c["pairs"] if p["overlap"] is not None]

    # ---------- 1. 竞争矩阵（前 10 家，对角 100） ----------
    firms = c["names"][:MATRIX_FIRMS]
    idx = {n: i for i, n in enumerate(firms)}
    mat = [[100.0 if i == j else None for j in range(len(firms))] for i in range(len(firms))]
    gmat = [["—" if i == j else None for j in range(len(firms))] for i in range(len(firms))]
    for p in pairs:
        if p["a"] in idx and p["b"] in idx:
            i, j = idx[p["a"]], idx[p["b"]]
            s = round(p["overlap"] * 100, 2)
            mat[i][j] = mat[j][i] = s
            gr = "高" if p["overlap"] >= p70 else ("中" if p["overlap"] >= p30 else "低")
            gmat[i][j] = gmat[j][i] = gr
    out["matrix"] = {"firms": firms, "ci_score": mat, "grade": gmat,
                     "axes_note": "行/列为同一组企业；对角固定 100（自身对自身）"}
    out["probes"]["matrix_pairs"] = len(firms) * (len(firms) - 1) // 2

    # ---------- 2. 战略定位图：规模 × 平均 overlap ----------
    agg = {n: [] for n in c["names"]}
    for p in pairs:
        agg[p["a"]].append(p["overlap"])
        agg[p["b"]].append(p["overlap"])
    pts = []
    for n in c["names"]:
        if not agg[n]:
            continue
        scale = c["patents"][n] + c.get("papers", {}).get(n, 0)
        pts.append({"firm": n, "patents": c["patents"][n],
                    "papers": c.get("papers", {}).get(n, 0), "scale": scale,
                    "avg_overlap": round(mean(agg[n]), 4),
                    "max_overlap": round(max(agg[n]), 4),
                    "n_partners": len(agg[n]),
                    "city": c["org"][n]["city"],
                    "industry_l2": c["org"][n]["industry_l2"]})
    out["positioning"] = sorted(pts, key=lambda x: -x["avg_overlap"])
    s_med = median([p["scale"] for p in pts])
    o_med = median([p["avg_overlap"] for p in pts])
    q = {"高一高": [], "高分散": [], "低一高": [], "低分散": []}
    for p in pts:
        big = p["scale"] >= s_med
        close = p["avg_overlap"] >= o_med
        key = "高一高" if (big and close) else ("高分散" if (big and not close) else
                                               ("低一高" if (close and not big) else "低分散"))
        p["quadrant"] = key
        q[key].append(p["firm"])
    out["quadrants"] = {"median_scale": s_med, "median_avg_overlap": round(o_med, 4),
                        "counts": {k: len(v) for k, v in q.items()},
                        "members": {k: v[:8] for k, v in q.items()}}

    # ---------- 3. 等级统计（与 003 同阈值） ----------
    g = {"高": 0, "中": 0, "低": 0}
    for p in pairs:
        gr = "高" if p["overlap"] >= p70 else ("中" if p["overlap"] >= p30 else "低")
        g[gr] += 1
    out["grade_counts"] = g
    out["thresholds"] = {"p70_overlap": p70, "p30_overlap": p30,
                         "ci_high_cut": round(p70 * 100, 2), "ci_low_cut": round(p30 * 100, 2)}

    n_paper = sum(1 for n in c["names"] if c.get("papers", {}).get(n))
    out["disclosures"] = list(c.get("disclosures", [])) + [
        "「规模」= 专利件数 + 论文篇数；论文按 dwd_zh_author.institution 前缀匹配到企业，"
        "覆盖 %d/%d 家，故对无论文企业规模被低估（以专利为主）" % (n_paper, len(c["names"])),
        "战略定位图的两轴中位数由本批 %d 家企业决定，换一批企业象限归属会变——它是相对定位，不是绝对强弱"
        % len(c["names"]),
        "矩阵取值 = 研究领域重叠度×100，不含市场/价格/渠道维；对角 100 是占位约定，不代表「自身竞争度为 100」",
        "dwd_org_base_info 99.82% 集中在广东，本比对集为深圳都市圈样本，不能外推为全国竞争格局",
    ]
    out["support_judgment"] = {
        "level": "部分支持",
        "reason": "竞争矩阵与战略定位图均可对 " + str(len(pairs)) + " 个企业对现算并输出，"
                  "但（1）学者维覆盖 %d/%d、（2）论文规模维覆盖 %d/%d，"
                  "（3）需求所要求的「战略定位」语义含市场地位，库内无营收/份额数据，"
                  "只能以「规模 × 研究领域平均重合度」代理——属始终有依赖维不足。"
                  % (sum(1 for n in c["names"] if c["scholar"].get(n)), len(c["names"]),
                     n_paper, len(c["names"])),
    }
    out["runtime_sec"] = round(time.time() - t0, 2)
    dest = C.write_out(MID, out)
    print("saved", dest, "quadrants", out["quadrants"]["counts"])


if __name__ == "__main__":
    main()
