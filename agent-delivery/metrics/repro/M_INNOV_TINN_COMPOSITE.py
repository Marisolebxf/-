#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_TINN_COMPOSITE · 技术创新力综合评估（判：部分支持）

口径真源：`metrics/calc-logic/INNOV/M_INNOV_TINN_COMPOSITE.md`（V1.5-20260901）
三维：专利数量（申请量/授权量）· 专利质量（5 子项）· 技术市场潜力（5 子项），
默认三维等权，一行一个 IPC4，0—100。

本批实际情况
------------
* 规模维：申请量全量可算（面板 2,939,895 行，IPC4×年 2021—2024）；授权量只有全域 2,140,420。
* 质量维、市场维：同批 TINN_PATENT_QUALITY / TINN_MARKET 已判完全不支持（五维均无法落到 IPC4）。
* 按 calc-logic「缺测维不补 0，剩余维权重重归一」，本脚本**只交付规模维**，
  并把权重显式写成 {规模:1.0, 质量:0.0, 市场:0.0}，产物字段名用 `size_only_score`，
  **不得**对外当作「技术创新力综合得分」使用。

运行：python3 code/M_INNOV_TINN_COMPOSITE.py（零 SQL）
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _tail21_common as T  # noqa: E402

MID = "M_INNOV_TINN_COMPOSITE"
TOTAL = 2_939_895
REAL_YEARS = [2021, 2022, 2023, 2024]


def norm(vals: list[float]) -> list[float]:
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return [50.0] * len(vals)
    return [round(100 * (v - lo) / (hi - lo), 2) for v in vals]


def main() -> None:
    panel = json.loads((T.SNAP / "patent_panel_innov_20261021.json").read_text(encoding="utf-8"))
    per: dict[str, dict[int, int]] = {}
    for k, n in panel["ipc_year"].items():
        y, _, ipc = k.partition("|")
        per.setdefault(ipc, {})[int(y)] = int(n)

    agg = json.loads((T.SNAP / "star_applicant_agg_gkx.json").read_text(encoding="utf-8"))["agg"]
    pub_total = sum(v[0] for v in agg.values())
    grant_total = sum(v[1] for v in agg.values())

    items = sorted(((ipc, sum(s.get(y, 0) for y in REAL_YEARS)) for ipc, s in per.items()),
                   key=lambda kv: -kv[1])
    names = [k for k, _ in items]
    sizes = [v for _, v in items]
    scores = norm([float(v) for v in sizes])

    # 敏感性口径：池内百分位。min-max 在重尾计数上会把 90% 领域压到 0—5，
    # 百分位口径用来检验「排序是否依赖归一方式」。
    order = sorted(range(len(sizes)), key=lambda i: (sizes[i], names[i]))
    pct = [0.0] * len(sizes)
    for rank_i, i in enumerate(order):
        pct[i] = round(100 * rank_i / (len(sizes) - 1), 2)

    def spearman(a: list[float], b: list[float]) -> float:
        def ranks(v: list[float]) -> list[float]:
            o = sorted(range(len(v)), key=lambda i: v[i])
            r = [0.0] * len(v)
            for k, i in enumerate(o):
                r[i] = float(k)
            return r
        ra, rb = ranks(a), ranks(b)
        n = len(a)
        ma, mb = sum(ra) / n, sum(rb) / n
        cov = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
        va = sum((x - ma) ** 2 for x in ra) ** 0.5
        vb = sum((y - mb) ** 2 for y in rb) ** 0.5
        return round(cov / (va * vb), 4) if va and vb else 0.0

    rho = spearman([float(x) for x in scores], pct)
    top20 = set(names[:20])
    top20_pct = {names[i] for i in sorted(range(len(pct)), key=lambda i: -pct[i])[:20]}

    rows = []
    for i, (ipc, s) in enumerate(items[:40]):
        c21 = per[ipc].get(2021, 0)
        c24 = per[ipc].get(2024, 0)
        rows.append({
            "ipc4": ipc,
            "apply_2021_2024": s,
            "apply_2024": c24,
            "growth_2021_2024_pct": round(100 * (c24 - c21) / c21, 2) if c21 else None,
            "size_score": scores[i],
            "size_only_score": scores[i],
            "rank": i + 1,
            "quality_score": None,
            "market_score": None,
        })

    res = {
        "metric_id": MID,
        "metric_name": "技术创新力综合评估",
        "support_judgment": "部分支持",
        "object": "技术领域（IPC 主分类前 4 位）",
        "verdict_reason": (
            "三维里只有规模维的申请量半维可算；授权量只有全域口径，质量维与市场维的五维子项"
            "全部无法按 IPC4 归属（见 TINN_PATENT_QUALITY / TINN_MARKET 两份同批结论）。"
            "按「缺测维不补 0、剩余维重归一」只交付规模维分，并显式标注其不是综合分"),
        "data_source": "patent_panel_innov_20261021.json（全量）+ star_applicant_agg_gkx.json（授权合计）",
        "sql_count": 0,
        "weights_declared": {"size": 0.3333, "quality": 0.3333, "market": 0.3334},
        "weights_used": {"size": 1.0, "quality": 0.0, "market": 0.0},
        "weight_note": "口径只写「加权平均」且明示权重由用户自定义（序号 143），未给固定值；本批缺省取三维等权 1/3。"
                       "质量/市场零可算维，按 calc-logic 的重归一规则落到规模维 1.0，属于降级交付，不是口径变更",
        "probe": {
            "patent_rows": TOTAL,
            "panel_rows": panel["rows"],
            "domains_total": len(items),
            "domains_with_2024": sum(1 for _, s in per.items() if s.get(2024, 0) > 0),
            "apply_dim_status": "全量可算（2021—2024 四年，IPC4 已标注 82.87%）",
            "grant_dim_status": f"仅全域 {grant_total:,}/{pub_total:,} = "
                                f"{round(100 * grant_total / pub_total, 2)}%，无 IPC4 拆分",
            "quality_dim_status": "不可算（5/5 子项无法落到 IPC4）",
            "market_dim_status": "不可算（5/5 子项无法落到 IPC4）",
            "size_cronbach_note": "单维分不构成综合指数，内部一致性检验无意义，故不报 Cronbach α",
        },
        "rank_top40": rows,
        "score_distribution": T.st([float(x) for x in scores]),
        "sensitivity": {
            "alt": "池内百分位（rank/(n-1)*100）",
            "spearman_vs_minmax": rho,
            "top20_overlap": len(top20 & top20_pct),
            "note": "min-max 在重尾计数上把 90% 领域压到 5 分以下，百分位口径用于检验排序稳定性",
        },
        "base_years_used": REAL_YEARS,
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_year_block": T.base_year_block(
            REAL_YEARS, [2017, 2018, 2019, 2020],
            "库内专利仅 2021—2026；2017—2020 零行，规模维的四年合计不是五年合计"),
        "gaps": [
            "授权量不可按 IPC4 拆（只有全域 72.81%）",
            "质量维 5 子项全部不可按 IPC4 归属",
            "市场维 5 子项全部不可按 IPC4 归属",
            "2025/2026 的 IPC4 明细不在面板 window 内",
        ],
        "repair_requirements": [
            "优先补齐 IPC4×年×授权量结果表（规模维即可完整）",
            "补齐价值附表并冗余 ipc4 / apdt_year（质量维与市场维同时解锁）",
        ],
        "publish_note": "本产物只能用于「技术领域规模排名」演示；对外发布「技术创新力综合得分」会与口径不符",
    }
    T.write_out(MID, res)
    print(json.dumps(res["probe"], ensure_ascii=False, indent=1))
    print(rows[:3])


if __name__ == "__main__":
    main()
