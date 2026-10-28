#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_DS_09_RESEARCH_003 竞争情报等级 — 20261021 换源复现脚本

口径（王惠，calc-logic/INNOV/M_INNOV_RES_CI_LEVEL.md）：
  竞争情报分值 = 研究领域重叠度 × 100；等级复用 GRADE 的同一阈值（P70 / P30）
  输出企业对矩阵（对角 = 100）。

数据面（20261021）：复用 002 在**三方库 gkx** 上重建的特征缓存
  `_snapshots21/research_feature_cache_20261021.json`（三维 Jaccard + 全部企业对 overlap）。
  缓存底层表：gkx.dwd_patent / dwd_org_base_info / dwd_scholar / dwd_zh_author。

产物：M_INNOV_DS_09_RESEARCH_003_out.json
"""
import json
import time
from pathlib import Path
from statistics import mean, median

import _gkxdb
import _inn_res21_common as C

HERE = Path(__file__).parent
MID = "M_INNOV_DS_09_RESEARCH_003"
DB = "gkx@183.240.141.251:3318"
CACHE_NAME = "research_feature_cache_20261021.json"
MATRIX_FIRMS = 8


def main():
    t0 = time.time()
    c = C.load_cache(CACHE_NAME)
    if not c:
        raise SystemExit("缺少特征缓存，请先运行 M_INNOV_DS_09_RESEARCH_002.py")
    out = {"metric_id": MID, "name": "竞争情报等级", "formula_owner": "王惠",
           "run_at": time.strftime("%Y-%m-%d %H:%M:%S"),
           "cache_built_at": c["built_at"], "db": DB,
           "probes": {}, "score_distribution": {}, "grades": {}, "top10": [],
           "matrix": {}, "disclosures": [], "support_judgment": None}

    # ---------- 1. 行数探针（库存行数，独立于缓存） ----------
    inv = C.inventory()
    for t in ["dwd_patent", "dwd_org_base_info", "dwd_scholar", "dwd_zh_author"]:
        out["probes"][t] = int(inv[t]["rows"])
    out["probes"]["cache_universe"] = len(c["names"])
    out["probes"]["cache_pairs"] = len(c["pairs"])
    out["probes"]["db"] = DB

    # ---------- 2. 竞争情报分值 = overlap × 100 ----------
    p70, p30 = c["thresholds"]["p70_all_pairs"], c["thresholds"]["p30_all_pairs"]
    pairs = []
    for p in c["pairs"]:
        if p["overlap"] is None:
            continue
        s = round(p["overlap"] * 100, 2)
        pairs.append({"a": p["a"], "b": p["b"], "ci_score": s,
                      "ipc_jac": p["ipc_jac"], "kw_jac": p["kw_jac"],
                      "scholar_jac": p["scholar_jac"], "n_dims": p["n_dims"],
                      "grade": "高" if p["overlap"] >= p70 else ("中" if p["overlap"] >= p30 else "低")})
    scores = [p["ci_score"] for p in pairs]
    g = {"高": 0, "中": 0, "低": 0}
    for p in pairs:
        g[p["grade"]] += 1
    out["grades"] = g
    out["thresholds"] = {"p70_overlap": p70, "p30_overlap": p30,
                         "ci_high_cut": round(p70 * 100, 2), "ci_low_cut": round(p30 * 100, 2)}
    out["score_distribution"] = {
        "n_pairs": len(pairs), "min": min(scores), "max": max(scores),
        "mean": round(mean(scores), 2), "median": round(median(scores), 2),
        "p10": round(C.pct(scores, 0.10), 2), "p50": round(C.pct(scores, 0.50), 2),
        "p90": round(C.pct(scores, 0.90), 2), "p99": round(C.pct(scores, 0.99), 2),
        "n_dims_mean": round(mean([p["n_dims"] for p in pairs]), 2)}
    out["top10"] = sorted(pairs, key=lambda x: -x["ci_score"])[:10]
    out["bottom5"] = sorted(pairs, key=lambda x: x["ci_score"])[:5]

    # ---------- 3. 企业对矩阵（前 8 家，对角 100） ----------
    top_firms = c["names"][:MATRIX_FIRMS]
    idx = {n: i for i, n in enumerate(top_firms)}
    mat = [[100.0 if i == j else None for j in range(len(top_firms))]
           for i in range(len(top_firms))]
    for p in pairs:
        if p["a"] in idx and p["b"] in idx:
            i, j = idx[p["a"]], idx[p["b"]]
            mat[i][j] = mat[j][i] = p["ci_score"]
    out["matrix"] = {"firms": top_firms, "ci_score": mat,
                     "note": "对角=100 是矩阵可视化的占位约定，不代表「自身竞争度为满分」"}

    # ---------- 4. 企业级竞争强度（平均情报分值） ----------
    agg = {n: [] for n in c["names"]}
    for p in pairs:
        agg[p["a"]].append(p["ci_score"])
        agg[p["b"]].append(p["ci_score"])
    out["firm_level"] = sorted(
        [{"firm": n, "patents": c["patents"][n], "city": c["org"][n]["city"],
          "n_partners": len(v), "avg_ci": round(mean(v), 2),
          "max_ci": round(max(v), 2)} for n, v in agg.items() if v],
        key=lambda x: -x["avg_ci"])[:20]

    n_sch = sum(1 for n in c["names"] if c["scholar"].get(n))
    out["disclosures"] = list(c.get("disclosures", [])) + [
        "竞争情报分值与等级完全由研究领域重叠度换算（×100 + 同一 P70/P30 阈值），"
        "不含市场份额、价格、渠道等传统竞争情报维度——库内无对手方交易与价格数据",
        "阈值 P70/P30 是王惠口径的分位切点，属可配置参数；页面调整阈值会改变高/中/低计数",
        "学者维仅覆盖 %d/%d 家企业，两维（IPC4+关键词）样本对占多数（n_dims_mean=%s），"
        "故分值主要由技术分类与关键词重合驱动"
        % (n_sch, len(c["names"]), out["score_distribution"]["n_dims_mean"]),
        "dwd_org_base_info 99.82% 集中在广东，本矩阵的企业集为深圳都市圈样本，不构成全国竞争格局结论",
    ]
    out["support_judgment"] = {
        "level": "部分支持",
        "reason": "分值与等级可对 " + str(len(pairs)) + " 个企业对现算并给出矩阵，但"
                  "（1）学者维覆盖率过低（%d/%d）、（2）论文→企业机构边仅 %d 篇，"
                  "（3）竞争情报仅含研究领域重合这一维度，缺市场/交易数据；"
                  "按 §〇「始终有部分依赖维得不到足够数据」判部分支持。"
                  % (n_sch, len(c["names"]), sum(c["papers"].values())),
    }
    out["runtime_sec"] = round(time.time() - t0, 2)
    dest = C.write_out(MID, out)
    print("saved", dest, "pairs", len(pairs), "grades", g)


if __name__ == "__main__":
    main()
