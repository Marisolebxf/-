#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_SCIINDEX_VALUE · 科技指数值（含区域分布读数）。

口径（本件自拟，注册表 formula 为 pending_cosign、无同 ID 正本）：
  对象 = 地级市 × 年；组件 = 论文产出 P（第一作者单位归城）+ 专利产出 T（申请人→底册城市）；
  组件归一 = 100·log1p(x)/log1p(max_pool)；指数 = 0.5·P + 0.5·T，取值 0—100；
  窗口 = 2021—2023（专利「申请人-年」只有 2021—2024，论文 2024 为语料回填孤峰，故 2024 剔除）。

数据面：gkx（183.240.141.251:3318 只读）现拉论文 + 既有主键分块专利面板；零 demo 依赖。
运行：`cd code && python3 M_INNOV_SCIINDEX_VALUE.py`
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import _innov21_common as C  # noqa: E402

OUT = HERE / "M_INNOV_SCIINDEX_VALUE_out.json"
YEARS = (2021, 2022, 2023)
CITY_SHORT = {"深圳市": "深圳", "广州市": "广州", "东莞市": "东莞", "惠州市": "惠州"}


def idx100(values):
    hi = max(math.log1p(v) for v in values) or 1
    return [round(100 * math.log1p(v) / hi, 2) for v in values]


def main():
    t0 = time.time()
    p, pt = C.paper(), C.patent()
    cities = list(C.CORE_CITIES)

    # 论文：第一作者城市 × 年
    paper_city = {}
    for k, v in p["city_year_first"].items():
        city, y = k.rsplit("|", 1)
        paper_city.setdefault(city, {})[int(y)] = v
    # 专利：申请人 → 底册城市 × 年
    pat_city = {}
    for k, v in pt["city_year"].items():
        city, y = k.rsplit("|", 1)
        pat_city.setdefault(city, {})[int(y)] = v

    rows, by_year = [], {}
    for y in YEARS:
        pv = [paper_city.get(c, {}).get(y, 0) for c in cities]
        tv = [pat_city.get(c, {}).get(y, 0) for c in cities]
        pidx, tidx = idx100(pv), idx100(tv)
        scores = [round(0.5 * pidx[i] + 0.5 * tidx[i], 2) for i in range(len(cities))]
        order = sorted(range(len(cities)), key=lambda i: -scores[i])
        rank = {cities[i]: r + 1 for r, i in enumerate(order)}
        year_rows = []
        for i, c in enumerate(cities):
            year_rows.append({
                "city": c, "city_short": CITY_SHORT[c], "year": y,
                "papers": pv[i], "patents": tv[i],
                "paper_index": pidx[i], "patent_index": tidx[i],
                "score": scores[i], "rank": rank[c],
                "paper_rank": sorted(range(len(cities)), key=lambda j: -pv[j]).index(i) + 1,
                "patent_rank": sorted(range(len(cities)), key=lambda j: -tv[j]).index(i) + 1,
                "gap_to_top": round(scores[i] - max(scores), 2),
            })
        year_rows.sort(key=lambda r: r["rank"])
        by_year[str(y)] = year_rows
        rows.extend(year_rows)

    # 名次稳定性：四个城市三年名次是否变化
    rank_path = {c: [next(r["rank"] for r in by_year[str(y)] if r["city"] == c) for y in YEARS]
                 for c in cities}

    # 客观参照权重（熵权法，逐年在四城内算）
    entropy = {}
    for y in YEARS:
        mat = [[paper_city.get(c, {}).get(y, 0), pat_city.get(c, {}).get(y, 0)] for c in cities]
        w = C.entropy_weights(mat)
        entropy[str(y)] = {"paper": round(w[0], 4), "patent": round(w[1], 4)}

    # 权重网格：w_paper 0→1（步长 0.01），看第一名何时换城
    grid = []
    top1_count = {c: 0 for c in cities}
    flips = {}
    for y in YEARS:
        pidx = [r["paper_index"] for r in sorted(by_year[str(y)], key=lambda r: cities.index(r["city"]))]
        tidx = [r["patent_index"] for r in sorted(by_year[str(y)], key=lambda r: cities.index(r["city"]))]
        prev = None
        flips[str(y)] = []
        for k in range(101):
            w = k / 100
            sc = [w * pidx[i] + (1 - w) * tidx[i] for i in range(len(cities))]
            win = cities[max(range(len(cities)), key=lambda i: sc[i])]
            if y == 2023:
                top1_count[win] += 1
            if prev and win != prev:
                flips[str(y)].append({"w_paper": round(w, 2), "from": prev, "to": win})
            prev = win
        grid.append({"year": y, "w_paper": [round(k / 100, 2) for k in range(101)],
                     "winner": [cities[max(range(len(cities)),
                                          key=lambda i: (k / 100) * pidx[i] + (1 - k / 100) * tidx[i])]
                                for k in range(101)]})
    top1_share = {c: round(n / 101, 4) for c, n in top1_count.items()}

    # 覆盖
    p_tot = p["rows"]
    p_mapped = p["city_mapped_total"]
    pat_total_4y = sum(pt["app_year_total"].values())
    coverage = {
        "paper_rows": p_tot,
        "paper_with_inst": p["papers_with_inst"],
        "paper_city_mapped": p_mapped,
        "paper_city_share": C.share(p_mapped, p_tot),
        "paper_city_list": list(p["city_totals"]),
        "inst_distinct": p["inst_distinct"],
        "inst_kept": p["inst_kept"],
        "inst_rows_total": p["inst_rows_total"],
        "inst_other_papers": p["inst_other_papers"],
        "paper_core4_share_of_mapped": C.share(
            sum(p["city_totals"].get(c, 0) for c in cities), p_mapped),
        "patent_app_year_total_4y": pat_total_4y,
        "patent_city_matched": pt["matched_patents"],
        "patent_city_share": C.share(pt["matched_patents"], pat_total_4y),
        "patent_applicants": pt["applicants"],
        "patent_matched_applicants": pt["matched_applicants"],
        "patent_core4_share_of_matched": C.share(
            sum(pt["city_totals"].get(c, 0) for c in cities), pt["matched_patents"]),
        "patent_rows": pt["rows"],
        "patent_auth": pt["auth"],
    }

    # 逐年论文归城率（第一作者城市 / 当年语料）
    year_cov = {}
    for y in (2015, 2019, 2020, 2021, 2022, 2023, 2025):
        tot = p["year_all"].get(str(y), 0)
        mapped = sum(paper_city.get(c, {}).get(y, 0) for c in paper_city)
        year_cov[str(y)] = {"papers": tot, "mapped": mapped, "share": C.share(mapped, tot)}

    av = C.availability()
    out = {
        "metric_id": "M_INNOV_SCIINDEX_VALUE",
        "metric_name": "科技指数值（含区域分布读数）",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "support_judgment": "部分支持",
        "verdict_kind": "computed_with_declared_gap",
        "formula_owner": "注册表 formula = pending_cosign: human:唐绍祖（未签）；"
                         "calc-logic/INNOV 下无同 ID 正本。正本口径为「已发布科技指数数值」，"
                         "本件为自建替代读数",
        "main_is_official": False,
        "weights": {"paper": 0.5, "patent": 0.5},
        "weights_note": "等权：需求只要求「多维度指标 + 权重展示」，未给权重；"
                        "两组均为产出型组件，缺投入/人才/转化维（§四），等权最中性。"
                        "熵权法结果见 entropy_weights，只作客观参照，不替换正算权重。",
        "normalization": "组件 = 100·log1p(x)/log1p(max)，max 取当年四城池内最大值；指数 = 0.5·paper + 0.5·patent",
        "scale": "0—100；当年池内最高城市必然接近 100（专利组件恒为 100，论文组件最高者 100）",
        "years": list(YEARS),
        "excluded_years": {
            "2017—2020": "dwd_patent.apdt_year 四年零行（§3.13）",
            "2024": "论文语料回填孤峰 32,379 篇（2023 年 6,651 篇的 4.87 倍），指数会被抬成虚假上行",
            "2025": "专利申请人分年只到 2024；2025 总量 440,401 为截断年",
            "2026": "残年：专利 74,810、论文 2,989",
        },
        "pool": {"cities": cities,
                 "rule": "四城盘：专利 %.2f%%、论文可归城 %.2f%% 落在这四城"
                         % (100 * sum(pt["city_totals"].get(c, 0) for c in cities) / pt["matched_patents"],
                            100 * sum(p["city_totals"].get(c, 0) for c in cities) / p_mapped)},
        "components": {
            "paper": "dwd_zh_paper 第一作者单位归城（11 城白名单），读 papers_city_year_gkx21.json",
            "patent": "dwd_patent 第一申请人名称 → 底册城市，读主键分块面板 app_year（2021—2024）",
        },
        "by_year": by_year,
        "rows": rows,
        "rank_path": rank_path,
        "rank_stability": {c: (len(set(v)) == 1) for c, v in rank_path.items()},
        "entropy_weights": entropy,
        "top1_share_2023": top1_share,
        "weight_flips": flips,
        "weight_grid": grid,
        "coverage": coverage,
        "paper_city_coverage_by_year": year_cov,
        "availability": av,
        "gaps": [
            "正本口径是「已发布指数数值」（智库后台 Q-TINDEX-01/02 待登），本件是自建双组件"
            "产出指数，数值不等价于官方指数",
            "官方「科技指数」无正本：注册表 formula 未签，本件出的是自拟双组件产出指数",
            "两库均无现成结果面：gkx 无 city_index / carrier_index；旧机 live ADS 同名表为样例级"
            "（city_index 70 行 / 14 城 / weight_version=w_v1.0-demo，indicator_values.source=ods_mock）",
            "论文只有 24,737 篇（24.52%）能按第一作者单位落城，且只覆盖 11 城",
            "专利城市归属依赖「申请人名称 = 底册企业名」等值匹配，覆盖率 87.3%—88.2%（逐年）",
            "指数缺投入/人才/技术交易/成果转化四类维度，只有产出侧两组件",
            "2024 年论文语料断点使「最新一年读数」不可用，对外只能给到 2023",
        ],
        "checks": {
            "weights_sum_to_one": True,
            "index_max_le_100": all(r["score"] <= 100.0001 for r in rows),
            "rank_matches_score": all(
                [r["city"] for r in sorted(by_year[str(y)], key=lambda r: -r["score"])]
                == [r["city"] for r in sorted(by_year[str(y)], key=lambda r: r["rank"])]
                for y in YEARS),
            "component_index_endpoints": all(
                max(r["patent_index"] for r in by_year[str(y)]) == 100.0 for y in YEARS),
            "no_published_surface_used": True,
            "years_complete": len(by_year) == len(YEARS),
        },
        "base_years_used": [2021, 2022, 2023],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": "专利表 2017—2020 零行，分母不含这四年；2024 年论文语料断点、"
                           "2025—2026 专利申请人分年缺失，均出窗口且不按 0 摊入。",
        "sources": [
            "gkx.dwd_zh_paper（100,900 行）",
            "gkx.dwd_patent（2,939,895 行，按公开件计）",
            "code/_snapshots21/innov_bsample_panel_20261023.json",
            "code/_snapshots21/papers_city_year_gkx21.json",
            "code/_snapshots21/patent_panel_innov_20261021.json",
            "code/_snapshots21/base_20261021.json",
        ],
    }
    # ---------- 派生比值（v8 §一：正文出现的比值/占比/倍率/差值必须落产物）
    # 键名带分母；`denominator_note` 写清分子分母各由哪个字段算出，便于逐项复核。
    paper_inst_missing = p_tot - p["papers_with_inst"]
    core4_paper = sum(p["city_totals"].get(c, 0) for c in cities)
    core4_patent = sum(pt["city_totals"].get(c, 0) for c in cities)
    outside_patent = pt["matched_patents"] - core4_patent
    paper_city_year = {c: {str(y): paper_city.get(c, {}).get(y, 0) for y in YEARS} for c in cities}
    paper_city_3y = {c: sum(paper_city_year[c].values()) for c in cities}
    patent_city_year = {c: {str(y): pat_city.get(c, {}).get(y, 0) for y in (2021, 2022, 2023, 2024)}
                        for c in cities}
    patent_city_4y = {c: sum(patent_city_year[c].values()) for c in cities}
    patent_year_total = {str(y): sum(patent_city_year[c][str(y)] for c in cities)
                         for y in (2021, 2022, 2023, 2024)}
    outside_cities = {k: v for k, v in pt["city_totals"].items() if k not in cities}

    out["derived"] = {
        "paper_with_inst_share_of_paper_rows_pct": round(100 * p["papers_with_inst"] / p_tot, 4),
        "paper_without_inst_rows": paper_inst_missing,
        "paper_without_inst_share_of_paper_rows_pct": round(100 * paper_inst_missing / p_tot, 4),
        "paper_core4_share_of_mapped_pct": round(100 * core4_paper / p_mapped, 4),
        "paper_gz_over_sz_2021": round(paper_city["广州市"][2021] / paper_city["深圳市"][2021], 4),
        "paper_max_over_min_2021": round(max(paper_city[c][2021] for c in cities)
                                         / min(paper_city[c][2021] for c in cities), 4),
        "patent_city_match_share_of_app_year_pairs_pct": round(
            100 * pt["matched_patents"] / pat_total_4y, 4),
        "patent_matched_applicant_share_of_applicants_pct": round(
            100 * pt["matched_applicants"] / pt["applicants"], 4),
        "patent_core4_share_of_matched_pct": round(100 * core4_patent / pt["matched_patents"], 4),
        "patent_outside_core4": outside_patent,
        "patent_outside_core4_share_of_matched_pct": round(
            100 * outside_patent / pt["matched_patents"], 4),
        "patent_sz_share_of_core4_2021_pct": round(
            100 * patent_city_year["深圳市"]["2021"] / patent_year_total["2021"], 4),
        "patent_sz_over_hz_2021": round(
            patent_city_year["深圳市"]["2021"] / patent_city_year["惠州市"]["2021"], 4),
        "patent_sz_over_gz_2023": round(
            patent_city_year["深圳市"]["2023"] / patent_city_year["广州市"]["2023"], 4),
        "log1p_patent_sz_2023": round(math.log1p(patent_city_year["深圳市"]["2023"]), 4),
        "log1p_paper_gz_2023": round(math.log1p(paper_city_year["广州市"]["2023"]), 4),
        "patent_over_paper_raw_2023": round(
            patent_city_year["深圳市"]["2023"] / paper_city_year["广州市"]["2023"], 4),
        "log1p_patent_over_paper_2023": round(
            math.log1p(patent_city_year["深圳市"]["2023"])
            / math.log1p(paper_city_year["广州市"]["2023"]), 4),
        "paper_dg_change_2021_2023_pct": round(
            100 * (paper_city_year["东莞市"]["2023"] / paper_city_year["东莞市"]["2021"] - 1), 4),
        "score_gap_gz_minus_sz_2021": round(by_year["2021"][0]["score"] - by_year["2021"][1]["score"], 2),
        "score_gap_gz_minus_sz_2022": round(by_year["2022"][0]["score"] - by_year["2022"][1]["score"], 2),
        "score_gap_gz_minus_sz_2023": round(by_year["2023"][0]["score"] - by_year["2023"][1]["score"], 2),
        "score_gap_dg_minus_hz_2021": round(
            next(r for r in by_year["2021"] if r["city"] == "东莞市")["score"]
            - next(r for r in by_year["2021"] if r["city"] == "惠州市")["score"], 2),
        "score_gap_dg_minus_hz_2023": round(
            next(r for r in by_year["2023"] if r["city"] == "东莞市")["score"]
            - next(r for r in by_year["2023"] if r["city"] == "惠州市")["score"], 2),
        "patent_index_gz_deficit_vs_sz_2023": round(
            100.0 - next(r for r in by_year["2023"] if r["city"] == "广州市")["patent_index"], 2),
        "paper_index_sz_deficit_vs_gz_2023": round(
            100.0 - next(r for r in by_year["2023"] if r["city"] == "深圳市")["paper_index"], 2),
        "denominator_note": (
            "分子分母均为本件字段：paper_with_inst_share＝coverage.paper_with_inst／"
            "coverage.paper_rows；paper_core4_share_of_mapped＝四城 city_paper_year 三年合计／"
            "coverage.paper_city_mapped；patent_city_match_share＝coverage.patent_city_matched／"
            "coverage.patent_app_year_total_4y；patent_core4_share_of_matched＝四城 "
            "city_patent_year 四年合计／coverage.patent_city_matched；"
            "patent_outside_core4＝coverage.patent_city_matched − 四城合计；"
            "log1p_* 为 np 口径 log(1+x)，x 取 city_patent_year／city_paper_year"),
    }
    out["city_paper_year"] = {"by_city": paper_city_year, "sum_3y": paper_city_3y,
                              "total_by_year": {str(y): sum(paper_city_year[c][str(y)] for c in cities)
                                                for y in YEARS},
                              "grand_total_3y": sum(paper_city_3y.values())}
    out["city_patent_year"] = {"by_city": patent_city_year, "sum_4y": patent_city_4y,
                               "total_by_year": patent_year_total,
                               "grand_total_4y": sum(patent_city_4y.values()),
                               "outside_core4_by_city": dict(sorted(outside_cities.items(),
                                                                    key=lambda kv: -kv[1]))}
    out["headline"] = {
        "cities": len(cities), "years": len(YEARS),
        "paper_rows": p_tot, "paper_mapped": p_mapped,
        "paper_share_pct": round(100 * coverage["paper_city_share"], 2),
        "patent_rows": coverage["patent_rows"], "patent_auth": coverage["patent_auth"],
        "patent_4y": pat_total_4y, "patent_matched": coverage["patent_city_matched"],
        "patent_match_pct": round(100 * coverage["patent_city_share"], 2),
        "applicants": coverage["patent_applicants"],
        "matched_applicants": coverage["patent_matched_applicants"],
        "core4_patent_pct": round(100 * coverage["patent_core4_share_of_matched"], 2),
        "core4_paper_pct": round(100 * coverage["paper_core4_share_of_mapped"], 2),
        "index_2023": {r["city_short"]: r["score"] for r in by_year["2023"]},
        "switch_w_2023": flips["2023"][0]["w_paper"] if flips["2023"] else None,
        "gz_minus_sz_2023": round(by_year["2023"][0]["score"] - by_year["2023"][1]["score"], 2),
        "core4_paper_3y": sum(paper_city_3y.values()),
        "patent_outside_core4": outside_patent,
    }
    C.write_out(OUT, out)
    print("[SCIINDEX_VALUE] ->", OUT)
    for y in YEARS:
        print(" ", y, [(r["city_short"], r["score"], r["rank"]) for r in by_year[str(y)]])
    print("  entropy", entropy, "top1_share", top1_share)
    print("  coverage paper", coverage["paper_city_share"], "patent", coverage["patent_city_share"])
    print("  %.1fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
