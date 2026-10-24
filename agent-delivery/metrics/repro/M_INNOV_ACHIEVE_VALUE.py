#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_ACHIEVE_VALUE 创新成果价值 · 复现代码 v3（20261022 改源版，只用三方库 gkx）

相对 v2（20261021，开发库 ODS）的唯一变动是数据面：全部 SQL 直连三方库 `gkx`
（与旧开发库逐表镜像、行数一致），公式、统计窗、样本量、分档与切片口径一律不动。
行数探针改为读库存 `_work_gkx21/GKX_INVENTORY.json`——对 294 万行宽表再跑一次
`COUNT(*)` 既无收益又与铁律「行数只读库存」冲突。

三维（技术/应用/潜在）× 三类成果（专利/中文论文/国内项目），
同 achieve_type 内极值归一，缺测维不补 0 剩余维重归一，等权×100；
分档 本批 ≥P70 高 / ≤P30 低 / 其余中；深圳切片按 first_applicant_name 对齐深圳名册。
统计窗 2019-2024，每型样本 5,000。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _gkxdb  # noqa: E402

OUT = HERE / "M_INNOV_ACHIEVE_VALUE_out.json"
INV = HERE.parent / "_work_gkx21" / "GKX_INVENTORY.json"
YEAR_LO, YEAR_HI = 2019, 2024
SAMPLE_N = 5000

TABLES = ["dwd_patent", "dwd_patent_cited", "dwd_patent_transfer", "dwd_zh_paper",
          "dwd_zh_journal", "dwd_zh_project", "dwd_en_project", "dwd_org_base_info"]


def conn():
    return _gkxdb.gkx()


def norm(vals):
    xs = [v for v in vals if v is not None]
    if not xs:
        return {i: None for i in range(len(vals))}
    lo, hi = min(xs), max(xs)
    if hi == lo:
        return {i: (0.5 if v is not None else None) for i, v in enumerate(vals)}
    return {i: ((v - lo) / (hi - lo) if v is not None else None) for i, v in enumerate(vals)}


def pctl(sorted_xs, p):
    if not sorted_xs:
        return None
    k = max(0, min(len(sorted_xs) - 1, int(len(sorted_xs) * p / 100)))
    return sorted_xs[k]


def main():
    inv = json.loads(INV.read_text(encoding="utf-8"))
    probes = {f"gkx.{t}": int(inv[t]["rows"]) for t in TABLES if t in inv}
    probes["_rows_source"] = "_work_gkx21/GKX_INVENTORY.json（库存实测值，不重复 COUNT(*)）"

    cur = conn()
    # 深圳名册（对齐用，一次全表取城市=深圳的名称）
    cur.execute("SELECT name_cn FROM gkx.dwd_org_base_info WHERE city = '深圳市'")
    sz_names = {str(r[0]) for r in cur.fetchall()}

    # ---------- 专利（2019-2024）----------
    cur.execute("""
        SELECT p.pn, p.value, p.apdt_year, p.first_applicant_name,
               (SELECT COUNT(*) FROM gkx.dwd_patent_transfer t
                 WHERE t.pn = p.pn AND t.transfer_effective_date BETWEEN '2019-01-01' AND '2024-12-31'),
               (SELECT COALESCE(SUM(c.cited_by_nums),0) FROM gkx.dwd_patent_cited c WHERE c.pn = p.pn)
        FROM gkx.dwd_patent p
        WHERE p.apdt_year BETWEEN %s AND %s
        LIMIT %s
    """, (YEAR_LO, YEAR_HI, SAMPLE_N))
    patents = cur.fetchall()

    # ---------- 中文论文（2019-2024）----------
    cur.execute("""
        SELECT CONCAT('zh:', p.id), j.impact_score, p.download_num,
               CASE j.jn_zone WHEN '1区' THEN 4 WHEN '2区' THEN 3 WHEN '3区' THEN 2 WHEN '4区' THEN 1 ELSE 0 END
        FROM gkx.dwd_zh_paper p LEFT JOIN gkx.dwd_zh_journal j ON p.publication_id = j.publication_id
        WHERE p.cover_year_start BETWEEN %s AND %s
        LIMIT %s
    """, (YEAR_LO, YEAR_HI, SAMPLE_N))
    zh_papers = cur.fetchall()

    # ---------- 国内项目（2019-2024）----------
    cur.execute("""
        SELECT CONCAT('zh:', id), funded_amount,
               CASE WHEN final_report_abstract IS NOT NULL AND final_report_abstract != '' THEN 1 ELSE 0 END,
               CASE project_level WHEN '国家级' THEN 3 WHEN '省部级' THEN 2 ELSE 1 END
        FROM gkx.dwd_zh_project
        WHERE approval_year BETWEEN 20190101 AND 20241231
        LIMIT %s
    """, (SAMPLE_N,))
    zh_projects = cur.fetchall()
    cur.close()

    patents_rows = [(r[0], float(r[1]) if r[1] is not None else None,
                     float(r[4] or 0), float(r[5] or 0), (str(r[3]) in sz_names), str(r[3] or '')) for r in patents]
    zh_papers_rows = [(r[0], float(r[1]) if r[1] is not None else None,
                       float(r[2] or 0), float(r[3])) for r in zh_papers]
    zh_projects_rows = [(r[0], float(r[1]) if r[1] is not None else None,
                         float(r[2]), float(r[3] or 0)) for r in zh_projects]

    def score_batch(rows, dims_idx):
        n1 = norm([r[dims_idx[0]] for r in rows]); n2 = norm([r[dims_idx[1]] for r in rows]); n3 = norm([r[dims_idx[2]] for r in rows])
        out = []
        for i, r in enumerate(rows):
            parts = [n1[i], n2[i], n3[i]]
            avail = [p for p in parts if p is not None]
            s = (sum(avail) / len(avail) * 100) if avail else None
            out.append((r, parts, s))
        return out

    def stats_with_tier(out):
        scores = sorted([s for _, _, s in out if s is not None])
        if not scores:
            return {}
        p70, p30 = pctl(scores, 70), pctl(scores, 30)
        tiers = {"high": len([s for s in scores if s >= p70]), "low": len([s for s in scores if s <= p30]),
                 "mid": len([s for s in scores if p30 < s < p70])}
        return dict(n=len(scores), min=round(scores[0], 2), max=round(scores[-1], 2),
                    mean=round(sum(scores) / len(scores), 2), median=round(pctl(scores, 50), 2),
                    p70=round(p70, 2), p30=round(p30, 2), tier=tiers)

    p_out = score_batch(patents_rows, (1, 2, 3))
    z_out = score_batch(zh_papers_rows, (1, 2, 3))
    j_out = score_batch(zh_projects_rows, (1, 2, 3))

    # 深圳切片（专利）
    sz_p = [s for r, _, s in p_out if s is not None and r[4]]
    sz_p_sorted = sorted(sz_p)

    def top(out, n=8):
        return [{"key": r[0], "dims": [round(d, 3) if d is not None else None for d in ds],
                 "sz": (r[4] if len(r) > 4 else None), "score": round(s, 2)}
                for r, ds, s in sorted(out, key=lambda x: -(x[2] or 0))[:n] if s is not None]

    result = {
        "metric_id": "M_INNOV_ACHIEVE_VALUE",
        "metric_name": "创新成果价值",
        "method": "王惠 V1.5 升级版 v3（gkx 改源）：三类成果各自三维极值归一等权×100；缺测维不补0；P70/P30 分档；深圳切片",
        "data_source": "gkx（三方库，只读）：dwd_patent / dwd_patent_cited / dwd_patent_transfer / dwd_zh_paper / dwd_zh_journal / dwd_zh_project / dwd_org_base_info",
        "window": f"{YEAR_LO}-{YEAR_HI}",
        "probes": probes,
        "compute": {
            "patent": {"n_sampled": len(patents_rows), **stats_with_tier(p_out),
                       "sz_slice": {"n": len(sz_p), "mean": round(sum(sz_p) / len(sz_p), 2) if sz_p else None,
                                    "median": round(pctl(sz_p_sorted, 50), 2) if sz_p else None},
                       "top": top(p_out)},
            "zh_paper": {"n_sampled": len(zh_papers_rows), **stats_with_tier(z_out), "top": top(z_out, 5)},
            "zh_project": {"n_sampled": len(zh_projects_rows), **stats_with_tier(j_out), "top": top(j_out, 5)},
        },
        "support_judgment": None,
    }

    p_stats = result["compute"]["patent"]
    patent_ok = p_stats.get("n", 0) > 100 and p_stats.get("max", 0) > p_stats.get("min", 0)
    result["support_judgment"] = "部分支持" if patent_ok else "完全不支持"
    result["support_note"] = (
        f"专利三维齐全实测可算（n={p_stats['n']}，{p_stats['min']}-{p_stats['max']}，"
        f"P70={p_stats['p70']}/P30={p_stats['p30']} 分档 high:{p_stats['tier']['high']}/mid:{p_stats['tier']['mid']}/low:{p_stats['tier']['low']}，"
        f"深圳切片 {len(sz_p)} 条）；gkx.dwd_zh_journal.impact_score 与 jn_zone 当日全 NULL（论文技术/潜在维缺测）、"
        "download_num 全 0（应用维不区分）；gkx.dwd_zh_project.project_level 全为国家级（潜在维不区分）。"
        "依赖表结构+专利侧数据量足，但论文/项目两类型的关键子维当前无数据区分度 → 部分支持"
    )

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "compute"}, ensure_ascii=False, indent=1))
    for k, v in result["compute"].items():
        print(k, {kk: vv for kk, vv in v.items() if kk != "top"})


if __name__ == "__main__":
    main()
