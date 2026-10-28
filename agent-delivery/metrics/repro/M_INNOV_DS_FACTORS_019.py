#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""监测异常点识别（M_INNOV_DS_FACTORS_019）——要素类镜像条目。

本 ID 在 `metrics/calc-logic/INNOV/M_INNOV_DS_FACTORS_019.md` 里只有一句话：
「同 M_INNOV_FACTOR_ANOMALY-监测异常点识别」，源表字段与计算逻辑全部指向后者。
因此本脚本不是第二套算法，而是**同一套算法 + 镜像自证**：

  1. 直接复用 M_INNOV_FACTOR_ANOMALY.py 的 build_series() / run_all()（同源同参）；
  2. 额外产出「镜像一致性核对」：逐序列、逐口径比对两次读数，必须逐位相等；
  3. 额外产出「DS 侧映射表」：把 DS 条目声明的数据类型（专利/论文/机构/学者）
     逐项映射到实际落地的序列，并标注哪一项没落地（专利序列长度不足）。

专利件数仍然零 DB（读面板缓存），其余序列只扫小表。
产物：code/M_INNOV_DS_FACTORS_019_out.json
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from _innov_gkx21_common import write_out

METRIC = "M_INNOV_DS_FACTORS_019"
BASE = "M_INNOV_FACTOR_ANOMALY"

anomaly = importlib.import_module(BASE)


def main():
    series = anomaly.build_series()
    results = anomaly.run_all(series)

    # ---------- 镜像一致性：与正式条目的缓存逐序列、逐口径比对 ----------
    cached = anomaly.load_cache(anomaly.SERIES_CACHE)
    mirror_check = []
    if cached:
        by_key = {r["key"]: r for r in cached["series"]}
        for r in results:
            base = by_key.get(r["key"])
            if base is None:
                mirror_check.append({"key": r["key"], "identical": False, "why": "baseline 缺该序列"})
                continue
            per_mode = {}
            for m, rec in r["modes"].items():
                brec = base.get("modes", {}).get(m, {})
                per_mode[m] = (
                    rec.get("n_anomalies") == brec.get("n_anomalies")
                    and rec.get("n_mutations") == brec.get("n_mutations")
                    and [a["year"] for a in rec.get("anomalies", [])]
                    == [a["year"] for a in brec.get("anomalies", [])]
                )
            mirror_check.append({"key": r["key"], "per_mode": per_mode,
                                 "identical": all(per_mode.values()) if per_mode else False})
    all_same = all(x["identical"] for x in mirror_check) if mirror_check else None

    # ---------- DS 条目声明的输入 → 实际序列 ----------
    ds_map = [
        {"declared": "专利 apdt_year 按年聚合（IPC 领域切片）",
         "actual_series": "patent_year",
         "landed": False,
         "why": "gkx.dwd_patent 的 apdt_year 仅 2021—2026 共 6 期，长度 < 8，按口径不进入检测"},
        {"declared": "中文论文 cover_year_start 按年聚合",
         "actual_series": "zh_paper_year",
         "landed": True,
         "why": "1980—2025 共 46 期，可检测"},
        {"declared": "机构按年存量（dwd_org_base_info 入集）",
         "actual_series": "org_reg_year",
         "landed": True,
         "why": "底册无「存量快照年」，只能用 incorporation_year 作新设年度序列；存量口径不可得"},
        {"declared": "学者存量（dwd_scholar.paper_nums/h_index）",
         "actual_series": "scholar_rel_year",
         "landed": False,
         "why": "dwd_scholar 是截面表（无按年存量），落地为学者-论文关系条数，语义已变"},
        {"declared": "英文论文 cover_year_start（定义源表含 dwd_en_paper）",
         "actual_series": None,
         "landed": False,
         "why": "dwd_en_paper 仅 1,387 行，18 个年份档，2026 年 1,222 篇（88%）为残年堆积，不足以成序列"},
        {"declared": "项目立项年（定义未列，本批补充）",
         "actual_series": "project_year",
         "landed": True,
         "why": "1986—2023 共 38 期，作对照序列"},
    ]

    eligible = [r for r in results if r["eligible"]]
    hit_summary = [{"key": r["key"],
                    "hits": [{"year": a["year"], "value": a["value"], "score": a["score"],
                              "direction": a["direction"]}
                             for a in r["modes"]["yoy_floor"]["anomalies"]],
                    "mutations": [{"year": x["year"], "delta": x["delta"]}
                                  for x in r["modes"]["yoy_floor"]["mutations"]]}
                   for r in eligible if r["modes"]["yoy_floor"]["anomalies"]]

    payload = {
        "metric_id": METRIC,
        "metric_name": "监测异常点识别（DS_FACTORS 镜像条目）",
        "mirror_of": BASE,
        "data_support_level": "部分支持",
        "run_at": "2026-10-22",
        "db": "gkx@183.240.141.251:3318（专利序列零 DB，读面板缓存）",
        "params": {"threshold": anomaly.THRESH_ANOM,
                   "mutation_mult": anomaly.MUT_MULT,
                   "min_len": anomaly.MIN_LEN,
                   "rolling_window": anomaly.ROLL_WIN},
        "modes": ["levels（口径原式）", "rolling（滚动中枢）", "yoy（同比）",
                  "yoy_floor（同比+物质性门槛，推荐）"],
        "recommended_mode": "yoy_floor",
        "mirror_check": mirror_check,
        "mirror_all_identical": all_same,
        "ds_input_map": ds_map,
        "series": results,
        "summary": {
            "n_series_total": len(results),
            "n_series_eligible": len(eligible),
            "n_declared_inputs": len(ds_map),
            "n_inputs_landed": sum(1 for x in ds_map if x["landed"]),
            "yoy_floor_hits": hit_summary,
            "n_hits": sum(len(h["hits"]) for h in hit_summary),
            "level_share_max": max((r["modes"]["levels"].get("anomaly_share", 0)
                                    for r in eligible), default=0),
        },
        "gaps": [
            "六类声明输入里只有三类按原语义落地：专利 6 期 < 8、学者无按年存量、英文论文 1,387 行（88% 堆在 2026）三项未落地。",
            "英文论文仅 1,387 行且 88% 堆在 2026，不能成序列。",
            "IPC 领域切片未实施：专利序列本身不合格，切片后每格更薄，切了也不满足 ≥8 期。",
            "口径原式（全序列中枢）在中文论文序列上命中 19/46，已判定退化，不能直接出结论。",
            "孤立森林备选算法未实施（无标签、单变量年序列，MAD 已足够）。",
        ],
    }
    write_out(METRIC, payload)
    print(f"mirror_all_identical={all_same}  inputs_landed="
          f"{payload['summary']['n_inputs_landed']}/{len(ds_map)}  hits={payload['summary']['n_hits']}")
    for h in hit_summary:
        print(h["key"], [x["year"] for x in h["hits"]])


if __name__ == "__main__":
    main()
