#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""项目（含课题）影响力（M_INNOV_PROJECT_INFLUENCE）——A-22 批复现脚本。

口径来源：metrics/calc-logic/INNOV/M_INNOV_PROJECT_INFLUENCE.md（王惠，seed v1）
  「从资助金额、参与机构数、结题完备度综合，取值 0—100；采用加权平均。」

落地口径（王惠未给权重，本报告取**等权 1/3**，缺测维重归一并显式披露）：
  D1 资助金额   dwd_zh_project.funded_amount / dwd_en_project.funded_amount（万元）
  D2 参与机构数 dwd_zh_project.participating_institution（+ funded_institution 兜底）
  D3 结题完备   final_report_abstract 非空记 1，否则 0

数据入口：只读本目录 _snapshots21/probe_infl_20261022/ 下 2026-10-22 的小表快照
（dwd_zh_project 58,453 / dwd_en_project 20,000 / dwd_zh_project_output 20,133），
**本脚本零 SQL**，可直接复现；快照由 code/_probe_infl_data.py 一次性拉取。

产物：code/M_INNOV_PROJECT_INFLUENCE_out.json
"""
from __future__ import annotations

import json
import math
import re
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from _innov_gkx21_common import dist, norm01, pct, write_out

METRIC = "M_INNOV_PROJECT_INFLUENCE"
SNAP = HERE / "_snapshots21" / "probe_infl_20261022"

SEP = re.compile(r"[;,；，、/]")


def load(name):
    d = json.loads((SNAP / f"{name}.json").read_text(encoding="utf-8"))
    ix = {c: i for i, c in enumerate(d["columns"])}
    return d["rows"], ix, d


def fnum(x):
    if x is None or x == "":
        return None
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def n_institutions(raw):
    """参与机构去重数。字段是单值依托单位；有分隔符时按分隔符展开。"""
    s = (raw or "").strip()
    if not s:
        return 0
    parts = [p.strip() for p in SEP.split(s) if p.strip()]
    return len(set(parts)) if parts else 0


def spearman(xs, ys):
    n = len(xs)
    if n < 3:
        return None

    def rank(v):
        order = sorted(range(n), key=lambda i: v[i])
        r = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r

    rx, ry = rank(xs), rank(ys)
    mx, my = statistics.mean(rx), statistics.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return round(num / den, 4) if den else None


def main():
    zh, zx, zh_meta = load("zh_project")
    en, ex, en_meta = load("en_project")
    out_rows, ox, out_meta = load("zh_project_output")

    # ---------------- 国内项目：逐维可得性 ----------------
    amt = [fnum(r[zx["funded_amount"]]) for r in zh]
    amt_pos = [a for a in amt if a is not None]
    fra = [r[zx["fra_len"]] or 0 for r in zh]
    part = [n_institutions(r[zx["participating_institution"]]) for r in zh]
    inst_raw = [r[zx["participating_institution"]] for r in zh]
    fund_inst = [r[zx["funded_institution"]] for r in zh]
    years = [int(r[zx["approval_year"]]) // 10000 for r in zh]
    out_ids = {r[ox["id"]] for r in out_rows}
    zh_ids = {r[zx["id"]] for r in zh}

    zh_dim = {
        "rows": len(zh),
        "funded_amount": {
            "nonnull": len(amt_pos), "null": len(amt) - len(amt_pos),
            "min": round(min(amt_pos), 2), "max": round(max(amt_pos), 2),
            "mean": round(statistics.mean(amt_pos), 2),
            "median": round(statistics.median(amt_pos), 2),
            "p10": pct(amt_pos, 0.10), "p90": pct(amt_pos, 0.90),
            "n_distinct": len(set(amt_pos)),
            "unit": "万元（decimal(18,2)；中位 30、最大 920，与 NSFC 面上项目量级吻合）",
        },
        "participating_institution": {
            "nonnull": sum(1 for x in inst_raw if (x or "").strip()),
            "n_distinct": len({(x or "").strip() for x in inst_raw if (x or "").strip()}),
            "rows_with_separator": sum(1 for x in inst_raw if x and SEP.search(x)),
            "inst_count_dist": {str(k): v for k, v in
                                sorted({c: part.count(c) for c in set(part)}.items())},
        },
        "funded_institution": {
            "nonnull": sum(1 for x in fund_inst if (x or "").strip()),
            "note": "整列为空，无法用「受资助机构」兜底参与机构数",
        },
        "final_report_abstract": {
            "nonnull_by_length": sum(1 for x in fra if x),
            "rate": round(sum(1 for x in fra if x) / len(fra), 4),
            "max_len": max(fra),
            "n_distinct_len": len(set(fra)),
        },
        "completion_status": {"nonnull": 0, "note": "整列为空（completion_status / project_status 均空）"},
        "approval_year": {"min": min(years), "max": max(years),
                          "n_distinct": len(set(years)),
                          "n_2022_plus": sum(1 for y in years if y >= 2022)},
    }

    # 年序列
    yr_cnt = {}
    for y in years:
        yr_cnt[y] = yr_cnt.get(y, 0) + 1
    yr_cnt = dict(sorted(yr_cnt.items()))

    # ---------------- 国外项目 ----------------
    eamt = [fnum(r[ex["funded_amount"]]) for r in en]
    eamt_pos = [a for a in eamt if a not in (None, 0)]
    efra = [r[ex["fra_len"]] or 0 for r in en]
    epart = [n_institutions(r[ex["participating_institution"]]) for r in en]
    eyear = [r[ex["approval_year"]] for r in en]
    en_dim = {
        "rows": len(en),
        "funded_amount": {"nonnull_nonzero": len(eamt_pos), "zero": sum(1 for a in eamt if a == 0),
                          "min": round(min(eamt_pos), 2), "max": round(max(eamt_pos), 2),
                          "mean": round(statistics.mean(eamt_pos), 2),
                          "median": round(statistics.median(eamt_pos), 2),
                          "n_distinct": len(set(eamt_pos))},
        "participating_institution": {"n_distinct": len({(r[ex["participating_institution"]] or "").strip() for r in en}),
                                      "max_inst_count": max(epart)},
        "final_report_abstract": {"nonnull_by_length": sum(1 for x in efra if x),
                                  "rate": round(sum(1 for x in efra if x) / len(efra), 4)},
        "approval_year": {"nonnull": sum(1 for x in eyear if x not in (None, "")),
                          "note": "DATE 型且含 '0000-00-00' 空串，20,000 行全读为 NULL；按年不可算"},
        "funded_country_n_distinct": len({r[ex["funded_country"]] for r in en}),
    }

    # ---------------- 项目产出（第三方补充维，不入王惠口径） ----------------
    tot = [r[ox["total_outputs"]] for r in out_rows if r[ox["total_outputs"]] is not None]
    out_dim = {
        "rows": len(out_rows),
        "matched_project_ids": len(out_ids & zh_ids),
        "coverage_of_zh_projects": round(len(out_ids & zh_ids) / len(zh_ids), 4),
        "total_outputs_nonzero": sum(1 for x in tot if x),
        "total_outputs_max": max(tot),
        "journal_articles_nonzero": sum(1 for r in out_rows if r[ox["journal_articles_count"]]),
        "patents_nonzero": sum(1 for r in out_rows if r[ox["patents_count"]]),
        "degree_papers_nonzero": sum(1 for r in out_rows if r[ox["degree_papers_count"]]),
        "awards_nonzero": sum(1 for r in out_rows if r[ox["awards_count"]]),
    }

    # ---------------- 打分 ----------------
    # V1 严格三维（参与机构数按字面计数）
    n_amt = norm01(amt_pos)
    n_part = norm01(part)
    n_done = norm01([1 if x else 0 for x in fra])
    v1 = [100 * (a + p + d) / 3 for a, p, d in zip(n_amt, n_part, n_done)]

    # V2 参与机构数判缺测 → 0.5/0.5 重归一
    v2 = [100 * (0.5 * a + 0.5 * d) for a, d in zip(n_amt, n_done)]

    # 对数金额版（金额长尾，min-max 会把 90% 项目压到低位）
    log_amt = [math.log1p(a) for a in amt_pos]
    n_log = norm01(log_amt)
    v3 = [100 * (0.5 * a + 0.5 * d) for a, d in zip(n_log, n_done)]

    rows_scored = []
    for i, r in enumerate(zh):
        rows_scored.append({
            "id": r[zx["id"]],
            "year": years[i],
            "funded_amount": amt_pos[i],
            "inst_count": part[i],
            "has_final_report": bool(fra[i]),
            "score_v2": round(v2[i], 2),
            "score_v1": round(v1[i], 2),
            "score_v3_logamt": round(v3[i], 2),
        })
    top = sorted(rows_scored, key=lambda x: (-x["score_v2"], -x["funded_amount"]))[:10]

    # 机构维：按 participating_institution 汇总（本表为单值依托单位）
    inst_amt = {}
    for r, a in zip(zh, amt_pos):
        nm = (r[zx["participating_institution"]] or "").strip()
        if not nm:
            continue
        rec = inst_amt.setdefault(nm, [0, 0.0, 0])
        rec[0] += 1
        rec[1] += a
        rec[2] += 1 if (r[zx["fra_len"]] or 0) else 0
    top_inst = sorted(inst_amt.items(), key=lambda kv: -kv[1][0])[:10]

    # 学科/类别
    cat = {}
    for r in zh:
        c = (r[zx["fund_category"]] or "").strip() or "空"
        cat[c] = cat.get(c, 0) + 1
    disc = {}
    for r in zh:
        d = (r[zx["discipline"]] or "").strip()
        if d:
            disc[d] = disc.get(d, 0) + 1

    # 英文项目单独归一（金额量纲与国内差 4 个数量级，绝不能与国内同表归一）
    en_done = [1 if x else 0 for x in efra]
    en_pairs = [(a, d) for a, d in zip(eamt, en_done) if a not in (None, 0)]
    en_amt_pos = [p[0] for p in en_pairs]
    en_done_pos = [p[1] for p in en_pairs]
    en_norm_amt = norm01(en_amt_pos)
    en_norm_done = norm01(en_done_pos)
    en_score = [round(100 * (0.5 * a + 0.5 * d), 2)
                for a, d in zip(en_norm_amt, en_norm_done)]

    payload = {
        "metric_id": METRIC,
        "en_score": {
            "n_scored": len(en_score),
            "stats": dist(en_score),
            "formula": "S=100*(0.5*norm(金额)+0.5*结题完备)，英文项目独立归一",
            "currency_note": ("英文项目 funded_amount 中位 204,582、最大 3.40 亿，与国内项目"
                              "（中位 30、最大 920，万元）差 4 个数量级，量纲未统一；"
                              "中英文项目不得放进同一张归一表，否则中文项目会被整体压到 0。"),
        },
        "metric_name": "项目（含课题）影响力",
        "support_judgment": "部分支持",
        "run_at": "2026-10-22",
        "db": "gkx@183.240.141.251:3318（只读快照，脚本零 SQL）",
        "snapshot": {
            "dir": "_snapshots21/probe_infl_20261022",
            "files": ["zh_project.json", "en_project.json", "zh_project_output.json"],
            "pulled_at": "2026-10-22T10:39+08:00",
            "rows": {"zh_project": zh_meta["n"], "en_project": en_meta["n"],
                     "zh_project_output": out_meta["n"]},
        },
        "dimension_fill": {"zh": zh_dim, "en": en_dim, "output": out_dim},
        "year_series_zh": yr_cnt,
        "fund_category_zh": dict(sorted(cat.items(), key=lambda kv: -kv[1])),
        "discipline_top_zh": dict(sorted(disc.items(), key=lambda kv: -kv[1])[:10]),
        "institution_top_zh": [
            {"name": k, "projects": v[0], "funded_amount_sum": round(v[1], 2),
             "with_final_report": v[2]} for k, v in top_inst],
        "score": {
            "formula_v1_strict3": "S=100*(norm(金额)+norm(参与机构数)+norm(结题完备))/3",
            "formula_v2_missing_renorm": "S=100*(0.5*norm(金额)+0.5*结题完备)（参与机构数判缺测）",
            "formula_v3_log_amount": "S=100*(0.5*norm(ln(1+金额))+0.5*结题完备)",
            "v1": dist(v1), "v2": dist(v2), "v3": dist(v3),
            "spearman_v2_vs_v3": spearman(v2, v3),
            "top10_v2": top,
            "n_scored": len(v2),
        },
        "base_years_used": [y for y in yr_cnt if y <= 2021 and yr_cnt[y] >= 50],
        "base_years_missing": [2022, 2023, 2024, 2025, 2026],
        "base_years_note": ("dwd_zh_project 的 approval_year 覆盖 1986—2023，但 2022 仅 58 条、"
                            "2023 仅 6 条，2024—2026 无记录；任何「前 N 年均值 / CAGR」只能用 "
                            "1986—2021 这段真实年份做分母，2022 起三年不得按 0 摊入。"),
        "gaps": [
            "参与机构数维不可算：participating_institution 为单值依托单位（1,593 个不同值，仅 29 行含分隔符），"
            "funded_institution 整列为空，无法还原「参与机构去重数」。",
            "结题状态列（completion_status / project_status）整列为空，结题完备只能用 final_report_abstract 长度代理。",
            "英文项目 approval_year 全为 NULL（DATE 列含 '0000-00-00'），20,000 条无法进入年窗口。",
            "项目产出表仅覆盖 34.3% 的国内项目，且 degree_papers/awards/reports/other 四列全为 0。",
            "中文项目 100% 为国家自然科学基金（project_source 单一取值），不能代表全部科技项目。",
        ],
    }
    p = write_out(METRIC, payload)
    print(json.dumps({"wrote": str(p), "v2": payload["score"]["v2"],
                      "v3": payload["score"]["v3"],
                      "spearman_v2_v3": payload["score"]["spearman_v2_vs_v3"]},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
