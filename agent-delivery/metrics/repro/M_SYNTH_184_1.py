#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SYNTH_184_1 区域产业创新人才综合评价模型 —— gkx 重建版（20261022）。

王惠口径：四维（创新人才数量 / 学历结构 / 年龄结构 / 成果产出），
维内子项极值归一等权，四维等权，0—100。

本版相对旧版（`_quarantine/20261022_demo_helper/code/M_SYNTH_184_1.py`）的实质改动：
  1. 旧版 `from _b6_engine import conn` 连的是 111.198.38.90 上的演示库；
     本脚本零数据库连接，只读本目录 `code/_snapshots21/`（来源见 `_synth18x_common.SOURCES`）。
  2. 评价集从「深/京/沪/广」改为「深/广/莞/惠」：gkx 企业底册里北京 163 行、上海 16 行，
     占 0.09%，按底册归城撑不起城市级分子；四市占 99.82%（DATA_FACTS §3.8）。
  3. 旧版用 `hit_city()`（城市名前两字）归城；本版用「城市名 → 高校白名单 → 机构串」三级规则，
     全表 21,316 位学者里能判出城市的是 17,118 位（80.31%），其中落四市 1,174 位（5.51%）。
     四城占比低不是归城失败，而是这张学者表以高校院所为骨架（北京 2,727 / 上海 1,509 /
     南京 1,306），深圳 247 位明显低于其实际人才体量——企业研发人才不在这张表里。
  4. 数量维的研发人员子项在 gkx 上仍不可算（`development_employee` 0/90,926 非空），
     记空不进分母，与旧版一致，但**分母不再是演示库**。

输出：`code/M_SYNTH_184_1_out.json`
"""
from __future__ import annotations

import collections
import json
import os
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, HERE)
import _synth18x_common as S  # noqa: E402

METRIC = "M_SYNTH_184_1"

# 王惠四维的子项构成；None 表示该子项在 gkx 上不可算（记空，不进分母）
DIMS = collections.OrderedDict([
    ("D1_创新人才数量", ["学者存量", "企业研发人员"]),
    ("D2_学历结构", ["硕博学者占比"]),
    ("D3_年龄结构", ["青年学者占比"]),
    ("D4_成果产出", ["论文+H指数", "机构对齐授权专利", "专利转移", "院士数"]),
])

SUB_UNAVAILABLE = {
    "企业研发人员": "dwd_org_annual_financial_info.development_employee 全表 90,926 行、"
              "非空 0 行（SUM(col IS NOT NULL)=0，DATA_FACTS §3.10）；"
              "该列存在、SQL 不报错、安静返回空，故数量维退化为「学者存量」单子项",
}

# 能算出、但不进指数的子项（比率 + 极小样本 → 差异不显著，min-max 会造出伪区分度）
SUB_DEGENERATE = {
    "硕博学者占比": "只有深穗两城有学位记录（深圳 39/39 = 100.00%、广州 75/77 = 97.40%），"
               "Fisher 精确检验 p=0.5498；2.60 个百分点被批内 min-max 拉成 0 对 100，"
               "整维只剩两城、且差异不可区分，故整维不入指数",
    "青年学者占比": "只有深穗两城有履历记录（深圳 5/37 = 13.51%、广州 11/66 = 16.67%），"
               "Fisher 精确检验 p=0.7816；且「从业年限 < 10 年」本身就是年龄代理，"
               "两层代理叠加后不构成可发布读数，故整维不入指数",
}


def transfer_by_city():
    """2024 专利转移：转移前权利人按城市归并（1/k 摊权），返回 {city: 件数} 与未归属名数。"""
    rows = S._load("cityfam_transfer_2024_20261021.json")
    by = collections.Counter()
    unmapped = 0
    for r in rows:
        try:
            names = json.loads(r[1]) if isinstance(r[1], str) else (r[1] or [])
        except Exception:
            names = []
        for a in names if isinstance(names, list) else []:
            nm = (a.get("name") or "").strip() if isinstance(a, dict) else ""
            if not nm:
                continue
            c = S.org_city(nm)
            if c in S.CITIES:
                by[c] += 1
            else:
                w = S.name_city_weights(nm)
                if w:
                    for cc, k in w.items():
                        by[cc] += k
                else:
                    unmapped += 1
    return {"by_city": dict(by), "n_rows": len(rows), "unmapped_names": unmapped}


def main():
    sb = S.scholar_by_city()
    g = S.grants2024()
    tr = transfer_by_city()

    raw = {
        "学者存量": {c: sb["n"].get(c, 0) for c in S.CITIES},
        "企业研发人员": {c: None for c in S.CITIES},
        "硕博学者占比": {c: (round(sb["grad_ratio"][c] * 100.0, 4)
                       if sb["grad_ratio"].get(c) is not None else None) for c in S.CITIES},
        "青年学者占比": {c: (round(sb["young_ratio"][c] * 100.0, 4)
                       if sb["young_ratio"].get(c) is not None else None) for c in S.CITIES},
        "论文+H指数": {c: sb["paper_h"].get(c, 0) for c in S.CITIES},
        "机构对齐授权专利": {c: round(g["by_city"].get(c, 0)) for c in S.CITIES},
        "专利转移": {c: tr["by_city"].get(c, 0) for c in S.CITIES},
        "院士数": {c: sb["academician"].get(c, 0) for c in S.CITIES},
    }

    norm = {k: S.mm(v) for k, v in raw.items()}
    dim_scores, dim_detail = collections.OrderedDict(), collections.OrderedDict()
    for d, subs in DIMS.items():
        use = [s for s in subs if s not in SUB_DEGENERATE]
        dim_scores[d] = {c: S.wmean([norm[s].get(c) for s in use]) for c in S.CITIES}
        dim_detail[d] = {c: {s: norm[s].get(c) for s in subs} for c in S.CITIES}

    n_dims = {c: sum(1 for d in DIMS if dim_scores[d][c] is not None) for c in S.CITIES}
    MIN_DIMS = 2
    index = {c: (S.wmean([dim_scores[d][c] for d in DIMS]) if n_dims[c] >= MIN_DIMS else None)
             for c in S.CITIES}
    rank = sorted([c for c in S.CITIES if index[c] is not None], key=lambda x: -index[x])

    # ---- 敏感性：四条替代口径，全部现算，供 MD §5.4 引用 ----
    d4_noacad = {c: S.wmean([norm["论文+H指数"][c], norm["机构对齐授权专利"][c],
                             norm["专利转移"][c]]) for c in S.CITIES}
    four_dims = {c: S.wmean([S.wmean([norm[s].get(c) for s in subs]) for subs in DIMS.values()])
                 for c in S.CITIES}
    sensitivity = {
        "四维全上_含退化子项": four_dims,
        "去掉院士子项": {c: S.wmean([dim_scores["D1_创新人才数量"][c], d4_noacad[c]])
                   for c in S.CITIES},
        "只留数量维": dim_scores["D1_创新人才数量"],
        "只留成果维": dim_scores["D4_成果产出"],
    }

    # ---- 参考面：全表学者城市分布（不进指数，只用来解释样本偏置）----
    sch_all = S.scholars()
    city_cnt = collections.Counter(s["city"] for s in sch_all)
    aux = {
        "scholars_total": len(sch_all),
        "scholar_top_cities": [[k, v] for k, v in city_cnt.most_common(10)],
        "org_rows_4city": sum(S.org_totals()["count"][c] for c in S.CITIES),
        "org_other_rows": S.org_totals()["n_rows"] - sum(S.org_totals()["count"][c]
                                                        for c in S.CITIES),
    }

    out = {
        "metric_id": METRIC,
        "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "source": "gkx @ 183.240.141.251:3318（gkx_reader_zp 只读），经 _snapshots21/ 落盘快照读取；"
                  "本脚本零数据库连接",
        "evaluation_set": S.CITIES,
        "excluded_cities": {
            "北京市": "企业底册 163 行（0.09%），专利申请人按底册归城无法支撑城市级分子",
            "上海市": "企业底册 16 行（0.01%），同上",
        },
        "stat_year": S.T_YEAR,
        "raw": raw,
        "norm_0_100": norm,
        "dim_scores": dim_scores,
        "dim_detail_norm": dim_detail,
        "n_dims_available": n_dims,
        "min_dims_for_index": MIN_DIMS,
        "index_0_100": {c: (round(index[c], 1) if index[c] is not None else None)
                        for c in S.CITIES},
        "rank": rank,
        "dims_definition": {k: v for k, v in DIMS.items()},
        "sub_unavailable": SUB_UNAVAILABLE,
        "sub_degenerate_excluded": SUB_DEGENERATE,
        "sensitivity": sensitivity,
        "aux": aux,
        "coverage": {
            "org_rows": S.org_totals()["n_rows"],
            "org_city_rows": {c: S.org_totals()["count"][c] for c in S.CITIES},
            "org_4city_share_pct": round(sum(S.org_totals()["count"][c] for c in S.CITIES)
                                         / S.org_totals()["n_rows"] * 100, 2),
            "org_dup_names": S.org_totals()["n_dup_names"],
            "policy_rows": S.policy_stats()["total_rows"],
            "policy_rows_4city": sum(S.policy_stats()["n"].values()),
        },
        "samples": {
            "scholars_total": len(S.scholars()),
            "scholars_attributed": S.scholar_attributed(),
            "scholars_attributed_pct": round(S.scholar_attributed() / len(S.scholars()) * 100, 2),
            "scholars_4city": sb["total_n"],
            "scholars_4city_share_pct": round(sb["total_n"] / len(S.scholars()) * 100, 2),
            "degree_records_4city": sum(sb["with_degree"].values()),
            "grad_records_4city": sb["total_grad"],
            "workexp_records_4city": sum(sb["with_exp"].values()),
            "academician_total_table": 112,
            "academician_4city": sb["total_academician"],
            "grants2024_total_rows": round(g["total"]),
            "grants2024_unmapped": round(g["unmapped"]),
            "grants2024_unmapped_pct": round(g["unmapped"] / g["total"] * 100, 2) if g["total"] else None,
            "transfers2024_rows": tr["n_rows"],
            "transfers2024_4city": sum(tr["by_city"].values()),
            "transfers2024_unmapped_names": tr["unmapped_names"],
        },
        "params": {
            "normalization": "维内子项批内 min-max（跨四城）；单子项全同或单点 → None",
            "dim_weight": "维内子项等权（缺子项不进分母）",
            "index": "四维等权；可算维数 < 2 不出指数",
            "young_threshold": "从业年限 < 10 年（2026 − 履历最早 start 年）",
            "age_proxy": "无出生年字段，用最早任职年代理（王惠原文规定的代理口径）",
        },
        "support_judgment": "部分支持",
        "support_reason": (
            "四维里两维出数：数量维（四市学者 1,174 人，深 247 / 广 918 / 莞 9 / 惠 0）"
            "与成果维（2024 授权 270,110 件、转移 172 件、论文+H 126,251、院士 6 人）"
            "都有真实非零读数且逐项可复现；但另外两维不可用：①数量维的企业研发人员分母整列为空"
            "（0/90,926 非空）；②学历维与年龄维只有深穗两城有样本（学位记录 116 条、履历记录 "
            "103 条），且两城差异用 Fisher 精确检验 p=0.5498 / 0.7816，统计上不可区分——"
            "能算出但不构成可发布读数，整维不入指数。四维只有两维可算，判部分支持"),
        "note": "旧版读数（广 52.2 / 深 35.0 / 北 33.9 / 上 33.1）来自演示库，评价集含京沪，"
                "与本版不可直接比较；逐项差异见 MD §〇.2。",
    }
    out.update(S.base_block(
        [S.T_YEAR],
        [y for y in S.PATENT_YEARS if y != S.T_YEAR],
        "本指标是 2024 年截面：专利授权与转移取 2024（库内真实年份 2021—2026，"
        "2017—2020 零行，§3.16）；学者、学历、履历、院士为存量/生涯累计，无年份分母。"
        "2025/2026 进 missing 是因为不是本批统计年（2025 公开滞后、2026 为残年），"
        "不是因为缺失被摊成 0。"))
    S.write_out(METRIC, out)
    print("index", out["index_0_100"], "rank", rank, "n_dims", n_dims)


if __name__ == "__main__":
    main()
