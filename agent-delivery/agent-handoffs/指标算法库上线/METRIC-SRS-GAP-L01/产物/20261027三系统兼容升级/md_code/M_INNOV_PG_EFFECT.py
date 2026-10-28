#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""政策实施效果（M_INNOV_PG_EFFECT）——零 SQL 复算。

王惠 V1.6 口径：专利增幅 / 论文增幅 / 项目增幅，近 3 年均值 vs 前 5 年均值，
增幅 = (近窗均值 − 基线均值) / max(基线均值, 1)。

本库实测的三条硬约束：
  1) 专利 apdt_year 只有 2021—2026，基线年 2016—2020 一行都没有 → 专利增幅不可算；
  2) 论文 2014 起语料爬坡，2014—2018 的基线显著偏低，增幅对窗口极敏感；
  3) 项目 2021 年起录入停摆（2021 2,339、2022 58、2023 6），T=2021 的窗口被截断。
因此本脚本对 T=2020 / 2021 / 2023 三个窗口全部出数，把窗口敏感性直接量化，
并另出四城截面：政策存量密度 × 专利产出增速（n=4，只作方向核对，不作因果识别）。

输入：code/_snapshots21/pg_probe2_20261021.json      论文/项目年度序列
      code/_snapshots21/pg_policy_rows_20261021.json  政策城市/年份
      code/_snapshots_gkx21/city_patent_year_gkx.json 城市×年专利件数
      code/_snapshots21/base_20261021.json            企业底册（城市企业数）
产物：code/M_INNOV_PG_EFFECT_out.json
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
SNAP_GKX = os.path.join(HERE, "_snapshots_gkx21")
OUT = os.path.join(HERE, "M_INNOV_PG_EFFECT_out.json")
METRIC_ID = "M_INNOV_PG_EFFECT"
FOUR = ["深圳市", "广州市", "东莞市", "惠州市"]
PLACEHOLDER = {"NULL", "", "NONE", "-"}


def growth(series, T):
    recent = [T - 2, T - 1, T]
    base = [T - 7, T - 6, T - 5, T - 4, T - 3]
    r_vals = [series.get(y, 0) for y in recent]
    b_vals = [series.get(y, 0) for y in base]
    r_avg = sum(r_vals) / len(r_vals)
    b_avg = sum(b_vals) / len(b_vals)
    # §3.16：分母只取真实存在（>0）的年份；缺失年不按 0 摊进分母
    used = [y for y in base if series.get(y, 0) > 0]
    b_avg_real = (sum(series[y] for y in used) / len(used)) if used else 0.0
    return {
        "T": T, "recent_years": recent, "base_years": base,
        "recent_values": r_vals, "base_values": b_vals,
        "recent_avg": round(r_avg, 2), "base_avg": round(b_avg, 2),
        "growth_pct": round(100 * (r_avg - b_avg) / max(b_avg, 1), 2),
        "base_years_used": used, "base_years_missing": [y for y in base if y not in used],
        "base_avg_real_years_only": round(b_avg_real, 2),
        "growth_pct_real_years_only": round(100 * (r_avg - b_avg_real) / max(b_avg_real, 1), 2) if used else None,
    }


def spearman(x, y):
    """秩相关；n=4 时仅作方向核对。"""
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0] * len(v)
        for pos, i in enumerate(order):
            r[i] = pos + 1
        return r
    rx, ry = ranks(x), ranks(y)
    n = len(x)
    d2 = sum((a - b) ** 2 for a, b in zip(rx, ry))
    return round(1 - 6 * d2 / (n * (n * n - 1)), 4)


def main() -> None:
    t0 = time.time()
    probe = json.load(open(os.path.join(SNAP, "pg_probe2_20261021.json"), encoding="utf-8"))
    pol = json.load(open(os.path.join(SNAP, "pg_policy_rows_20261021.json"), encoding="utf-8"))
    cpat = json.load(open(os.path.join(SNAP_GKX, "city_patent_year_gkx.json"), encoding="utf-8"))
    base = json.load(open(os.path.join(SNAP, "base_20261021.json"), encoding="utf-8"))

    paper = {int(y): n for y, n in probe["paper_year"]}
    project = {int(str(y)[:4]): n for y, n, amt, fin in probe["proj_year"]}
    patent = {int(y): n for y, n in probe["policy_year"]} if "policy_year" in probe else {}

    # 专利年序列：面板全量口径（2021—2026），2026 为残年
    panel_year = cpat["year_coverage"]["year_all"]
    patent_series = {int(y): int(n) for y, n in panel_year.items()}

    for r in pol:
        r["city"] = "" if str(r.get("city", "")).upper() in PLACEHOLDER else str(r["city"]).strip()
        y = str(r.get("publish_year") or "")
        r["yr"] = int(y) if y.isdigit() else None

    # ---------- 1. 王惠三维 ----------
    windows = [2020, 2021, 2023]
    paper_g = [growth(paper, T) for T in windows]
    project_g = [growth(project, T) for T in windows]

    patent_dim = {
        "usable": False,
        "reason": "gkx.dwd_patent.apdt_year 仅覆盖 2021—2026（2017—2020 零行），基线年 2016—2020 在库内不存在，任何增幅分母都无真实年份可用",
        "years_present": sorted(patent_series),
        "year_counts": patent_series,
        "recent_3y_avg_2021_2023": round(sum(patent_series.get(y, 0) for y in (2021, 2022, 2023)) / 3, 1),
        "base_5y_avg_2016_2020": None,
        "base_years_used": [],
        "base_years_missing": [2016, 2017, 2018, 2019, 2020],
    }

    # ---------- 2. 四城截面：政策存量密度 × 专利产出 ----------
    firms = Counter(b[4] for b in base)
    groups = cpat["groups"]
    pat_city_year = defaultdict(dict)
    for k, v in groups.items():
        c, y = k.split("|")
        pat_city_year[c][int(y)] = v

    panel = []
    for c in FOUR:
        p_all = sum(1 for r in pol if r["city"] == c)
        p_2020 = sum(1 for r in pol if r["city"] == c and r["yr"] and r["yr"] <= 2020)
        pat_2021 = pat_city_year[c].get(2021, 0)
        pat_2024 = pat_city_year[c].get(2024, 0)
        pat_sum = sum(pat_city_year[c].get(y, 0) for y in (2021, 2022, 2023, 2024))
        panel.append({
            "city": c,
            "firms": firms.get(c, 0),
            "policy_all": p_all,
            "policy_le_2020": p_2020,
            "policy_per_1000_firms": round(1000 * p_2020 / firms.get(c, 1), 3),
            "patent_2021_2024": pat_sum,
            "patent_per_firm": round(pat_sum / firms.get(c, 1), 3),
            "patent_growth_2021_to_2024_pct": round(100 * (pat_2024 - pat_2021) / max(pat_2021, 1), 2),
        })

    rho = spearman([x["policy_per_1000_firms"] for x in panel],
                   [x["patent_growth_2021_to_2024_pct"] for x in panel])
    rho_level = spearman([x["policy_per_1000_firms"] for x in panel],
                         [x["patent_per_firm"] for x in panel])

    result = {
        "metric_id": METRIC_ID,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "data_source": "gkx.dwd_zh_paper / dwd_zh_project / dwd_patent 面板 @ 183.240.141.251:3318（快照复算，零 SQL）",
        "support_judgment": "部分支持",
        "formula": "growth = (mean(T-2..T) − mean(T-7..T-3)) / max(base,1)；专利维不可算，论文/项目维按窗口敏感性披露",
        "dimensions": {
            "patent": patent_dim,
            "paper": {"usable": True, "windows": paper_g},
            "project": {"usable": True, "windows": project_g},
        },
        "chosen_window": {
            "paper_T": 2021,
            "project_T": 2020,
            "reason": "论文取语料成熟且避开 2024 回填峰（2024 单年 32,379 条为异常）；项目取录入停摆前最后完整年 2020",
            "base_years_used_paper": paper_g[1]["base_years_used"],
            "base_years_missing_paper": paper_g[1]["base_years_missing"],
            "base_years_used_project": project_g[0]["base_years_used"],
            "base_years_missing_project": project_g[0]["base_years_missing"],
        },
        "city_panel": panel,
        "rank_correlation": {
            "spearman_policy_density_vs_patent_growth": rho,
            "spearman_policy_density_vs_patent_per_firm": rho_level,
            "n": len(panel),
            "verdict": "n=4，方向核对用；不构成因果识别（无对照城市、无政策金额、无实施时点、无企业级面板键）",
        },
        "identification_gaps": [
            "政策表无『受益企业/受助项目』字段，policy_id 与 org_id 之间没有任何关联键，企业级面板对齐不可实现",
            "政策表无资金规模、无实施起止日期，只有发布日期，无法构造 treatment intensity 与时点",
            "专利面板 2021 起，政策语料 2021 止，两者仅一年重叠，无法构造 policy→outcome 的滞后窗口",
            "四城为批内全样本，无对照城市、无平行趋势检验，任何增幅都不能归因于政策",
            "论文/项目增幅对窗口极敏感（论文 +78.58%/+41.54%/+8.98%，项目 +18.46%/−5.65%/−82.41%），说明增幅主要由语料覆盖变化驱动",
        ],
        "runtime_sec": None,
    }

    print(f"[{METRIC_ID}]")
    for x in paper_g:
        print(f"  paper T={x['T']}: recent {x['recent_avg']} base {x['base_avg']} -> {x['growth_pct']}%")
    for x in project_g:
        print(f"  project T={x['T']}: recent {x['recent_avg']} base {x['base_avg']} -> {x['growth_pct']}%")
    print("  专利维: 不可算（仅有 2021+）")
    print("  四城面板:", [(x["city"], x["policy_per_1000_firms"], x["patent_growth_2021_to_2024_pct"]) for x in panel])
    print("  Spearman(政策密度, 专利增速) =", rho, "; (政策密度, 专利/企业) =", rho_level)

    result["runtime_sec"] = round(time.time() - t0, 3)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print(f"saved {OUT} ({result['runtime_sec']}s)")


if __name__ == "__main__":
    main()
