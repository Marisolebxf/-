#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""技术产品成熟度（M_INNOV_POT_MATURITY）——A-25 批 · 三方库 gkx 版。

王惠口径（calc-logic INNOV V1.5-20260901）：
  对象 = IPC 前 4 位；三维 = 授权比例 / 发明占比 / 市场渗透；同批领域内极值归一后等权 ×100；
  阶段标签由三维组合给出（成熟/成长/导入/衰退）。

本库落地情况（先实测后定档）：
  授权比例  ✅ 主键切片 200,000 行（6.80%）按 IPC4 计「granted_number 非空 / 件数」
  发明占比  ✅ 同一切片按 kind ∈ {A, B} 计
  市场渗透  ❌ `dwd_patent_transfer` 只有 22,809 行 / 20,000 个 pn（占 2,939,895 的 0.68%），
             且 `pn` 无索引、主表按 pn 关联要全表扫（禁），无法落到 IPC4 → 该维缺测，不补 0

全量口径校验：授权率的分母用 `star_applicant_agg_gkx.json` 的 [件数, 授权数]
（合计 2,939,895 / 2,140,420 = 72.80%），与本切片读数对照，用来说明切片是否有偏。

产物：code/M_INNOV_POT_MATURITY_out.json
"""
from __future__ import annotations

import json
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import _a25_common as C

METRIC = "M_INNOV_POT_MATURITY"
MIN_FULL = 3000      # 全量件数门槛：低于此值的 IPC4 授权率方差过大
MIN_SAMPLE = 200     # 切片件数门槛
T = C.T_YEAR


def build_units():
    agg = C.applicant_agg()
    full_grant = sum(v[1] for v in agg.values())
    full_cnt = sum(v[0] for v in agg.values())

    meta, rows = C.sample()
    per = {}
    for r in rows:
        ipc = C.ipc4_of(r["main_classification_ipcr"])
        if not ipc:
            continue
        y = r["apdt_year"]
        try:
            y = int(y)
        except Exception:
            y = None
        d = per.setdefault(ipc, {"n": 0, "grant": 0, "inv": 0, "years": Counter()})
        d["n"] += 1
        if r["granted_number"]:
            d["grant"] += 1
        if r["kind"] in ("A", "B"):
            d["inv"] += 1
        if y:
            d["years"][y] += 1

    ipc_full = C.ipc_year_full()
    units = []
    for ipc, d in per.items():
        if d["n"] < MIN_SAMPLE:
            continue
        fy = ipc_full.get(ipc, {})
        n_all = sum(fy.get(y, 0) for y in (2021, 2022, 2023, 2024))
        if n_all < MIN_FULL:
            continue
        g = None
        if fy.get(2022, 0) > 0 and fy.get(2024, 0) > 0:
            g = (fy[2024] / fy[2022]) ** 0.5 - 1
        g3 = None
        if fy.get(2021, 0) > 0 and fy.get(2024, 0) > 0:
            g3 = (fy[2024] / fy[2021]) ** (1 / 3) - 1
        units.append({
            "ipc4": ipc,
            "full_n_2021_2024": n_all,
            "full_by_year": {str(y): fy.get(y, 0) for y in (2021, 2022, 2023, 2024, 2025, 2026)},
            "sample_n": d["n"],
            "grant_n": d["grant"],
            "inv_n": d["inv"],
            "grant_ratio": round(d["grant"] / d["n"], 4),
            "inv_ratio": round(d["inv"] / d["n"], 4),
            "g_2022_2024": round(g, 4) if g is not None else None,
            "g_2021_2024": round(g3, 4) if g3 is not None else None,
            "sample_year_counts": {str(k): v for k, v in sorted(d["years"].items())},
        })
    return units, {"sample_rows": len(rows), "sample_share": meta["share"],
                   "full_grant": full_grant, "full_cnt": full_cnt,
                   "full_grant_ratio": round(full_grant / full_cnt, 4)}


def main():
    units, cov = build_units()
    if len(units) < 2:
        raise SystemExit("units < 2, cannot normalize")

    gr = [u["grant_ratio"] for u in units]
    iv = [u["inv_ratio"] for u in units]
    nm_gr = C.minmax(gr)
    nm_iv = C.minmax(iv)

    for u, a, b in zip(units, nm_gr, nm_iv):
        u["score"] = round((a + b) / 2, 2)
        u["n_dims"] = 2
        u["missing_dims"] = ["market_penetration"]

    med_gr = C.dist(gr)["median"]
    med_iv = C.dist(iv)["median"]
    p30_gr = C.dist(gr)["p30"]

    # 阶段判定（王惠只给「三维组合」，未给阈值；此处阈值显式写出，先判平台期再判方向）：
    #   成熟 = 授权比例 ≥ 中位 且 发明占比 ≥ 中位 且 |g| < 0.10（授权结构好、增速接近平台）
    #   成长 = g ≥ +10%（技术活动在扩张）
    #   导入 = 授权比例 < 30 分位（授权结构尚未成形）
    #   衰退 = g < 0（其余单元中技术活动收缩）
    # 旧版把「其余」一律归成长，导致 20 个负增长单元被标成成长，已改掉。
    for u in units:
        g = u["g_2022_2024"]
        if (u["grant_ratio"] >= med_gr and u["inv_ratio"] >= med_iv
                and (g is None or abs(g) < 0.10)):
            stage = "成熟"
        elif g is not None and g >= 0.10:
            stage = "成长"
        elif u["grant_ratio"] < p30_gr:
            stage = "导入"
        elif g is not None and g < 0:
            stage = "衰退"
        else:
            stage = "成长"
        u["stage"] = stage

    units.sort(key=lambda u: -u["score"])
    stage_dist = Counter(u["stage"] for u in units)
    scores = [u["score"] for u in units]
    sample_grant = sum(u["grant_n"] for u in units) / sum(u["sample_n"] for u in units)
    sample_inv = sum(u["inv_n"] for u in units) / sum(u["sample_n"] for u in units)

    out = {
        "metric_id": METRIC,
        "metric_name": "技术产品成熟度",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "definition": ("IPC4 级 0—100 成熟度：授权比例与发明占比同批极值归一后等权；"
                       "市场渗透维因转移表不可落 IPC4 缺测，不补 0"),
        "statistical_year": T,
        "formula": "score = 100 × mean(minmax(grant_ratio), minmax(inv_ratio))",
        "data_source": ("gkx.dwd_patent 主键切片 200,000 行（6.80%）+ "
                        "patent_ipc4_year_20261021.json 全量年度件数"),
        "probes": cov,
        "coverage": {
            "n_units": len(units),
            "min_full_n": MIN_FULL,
            "min_sample_n": MIN_SAMPLE,
            "sample_grant_ratio": round(sample_grant, 4),
            "sample_inv_ratio": round(sample_inv, 4),
            "full_grant_ratio": cov["full_grant_ratio"],
            "grant_gap_pp": round(100 * (sample_grant - cov["full_grant_ratio"]), 2),
            "market_penetration": {
                "available": False,
                "reason": ("dwd_patent_transfer 22,809 行 / 20,000 个 pn（0.68%），"
                           "pn 无索引，无法与 IPC4 关联；不得用 0 顶替"),
                "transfer_rows": 22809,
                "transfer_pn": 20000,
                "coverage_vs_patents": round(20000 / 2939895, 5),
            },
        },
        "result": {
            "score_dist": C.dist(scores),
            "grant_ratio_dist": C.dist(gr),
            "inv_ratio_dist": C.dist(iv),
            "stage_dist": dict(stage_dist),
            "median_grant": med_gr,
            "median_inv": med_iv,
            "p30_grant": p30_gr,
            "units": units,
        },
        "support_judgment": "部分支持",
        "reasons": [
            "授权比例与发明占比两维可算，%d 个 IPC4 单元全部有值，同批极值归一可直接执行；" % len(units),
            "市场渗透维整维缺测：转移表只有 2 万个 pn（0.68%），且无法落到 IPC4，按王惠「缺测维不补 0、剩余维重归一」处理，本指标只交付 2/3 维；",
            "授权比例与发明占比来自 6.80% 主键切片而非全量：切片整体授权率 72.89% 与全量 72.81% 只差 +0.08 个百分点（切片本身无偏），但保留下来的 147 个 IPC4 大单元合计授权率 66.12%，低于全库 6.69 个百分点，说明大单元（传统制造与通信）授权结构弱于小单元，单元级仍有抽样与选择误差；",
            "阶段标签依赖近窗增速（2022→2024，k=2），库内只有 2021—2026，无法按公式取更长窗口。",
        ],
    }

    p = HERE / f"{METRIC}_out.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print("written", p)
    print("units", len(units), "score", out["result"]["score_dist"])
    print("stage", dict(stage_dist), "grant", round(sample_grant, 4), "full", cov["full_grant_ratio"])


if __name__ == "__main__":
    main()
