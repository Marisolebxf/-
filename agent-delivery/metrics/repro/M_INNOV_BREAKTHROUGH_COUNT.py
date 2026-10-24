#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_BREAKTHROUGH_COUNT 重大成果突破数 · 复现代码（20261022 改源版，只用三方库 gkx）

口径：突破 = 高影响尾部计数——专利被引 P90 或价值 P90；论文挂 1 区刊；项目国家级。
非专利组合仅单一维度即入计（OR 逻辑），反映「任一维度突破」。
年窗 2020-2024（与 20261020 版一致，未改动）。

改源说明（20261021 版唯一变动）：数据面由开发库 ODS 换成三方库 `gkx`（逐表镜像、
行数一致）；判据阈值、OR 逻辑、抽样规模与年窗一律不动。表行数探针改为读库存
`_work_gkx21/GKX_INVENTORY.json`，不重复对 294 万行宽表做 `COUNT(*)`。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _gkxdb  # noqa: E402

OUT = HERE / "M_INNOV_BREAKTHROUGH_COUNT_out.json"
INV = HERE.parent / "_work_gkx21" / "GKX_INVENTORY.json"
YEAR_LO, YEAR_HI = 2020, 2024
PERC = 90

TABLES = ["dwd_patent", "dwd_patent_cited", "dwd_zh_paper", "dwd_zh_journal",
          "dwd_zh_project", "dwd_en_project", "dwd_en_paper"]


def qd(sql, args=None):
    cur = _gkxdb.gkx()
    try:
        cur.execute(sql, args) if args else cur.execute(sql)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    finally:
        cur.close()


def pct(vals, p):
    if not vals:
        return None
    s = sorted(vals)
    k = max(0, min(len(s) - 1, int(len(s) * p / 100)))
    return s[k]


def main():
    inv = json.loads(INV.read_text(encoding="utf-8"))
    probes = {f"gkx.{t}": int(inv[t]["rows"]) for t in TABLES if t in inv}

    # ---- 专利窗内：value + cited（关联子查询，控制窗口）----
    patents = [tuple(r.values()) for r in qd("""
        SELECT p.pn, p.value, p.apdt_year,
               (SELECT COALESCE(SUM(c.cited_by_nums),0) FROM gkx.dwd_patent_cited c WHERE c.pn = p.pn)
        FROM gkx.dwd_patent p
        WHERE p.apdt_year BETWEEN %s AND %s
        LIMIT 20000
    """, (YEAR_LO, YEAR_HI))]

    # ---- 论文：挂刊分区 ----
    zh_papers = [tuple(r.values()) for r in qd("""
        SELECT CONCAT('zh:', p.id),
               CASE j.jn_zone WHEN '1区' THEN 1 WHEN '2区' THEN 2 WHEN '3区' THEN 3 WHEN '4区' THEN 4 ELSE NULL END
        FROM gkx.dwd_zh_paper p LEFT JOIN gkx.dwd_zh_journal j ON p.publication_id = j.publication_id
        WHERE p.cover_year_start BETWEEN %s AND %s
        LIMIT 20000
    """, (YEAR_LO, YEAR_HI))]

    # ---- 项目：级别 ----
    zh_projects = [tuple(r.values()) for r in qd("""
        SELECT CONCAT('zh:', id), project_level
        FROM gkx.dwd_zh_project
        WHERE approval_year BETWEEN 20200101 AND 20241231
        LIMIT 20000
    """)]

    # 分区/级别覆盖检查（小表，允许直查）
    probes["gkx.dwd_zh_journal.jn_zone_nonnull"] = int(
        qd("SELECT COUNT(*) n FROM gkx.dwd_zh_journal WHERE jn_zone IS NOT NULL AND jn_zone != ''")[0]["n"])
    probes["zh_project.level_dist"] = {
        str(r["project_level"]): int(r["n"])
        for r in qd("SELECT project_level, COUNT(*) n FROM gkx.dwd_zh_project GROUP BY project_level LIMIT 8")}
    probes["patent_cited.positive"] = int(
        qd("SELECT COUNT(*) n FROM gkx.dwd_patent_cited WHERE cited_by_nums > 0")[0]["n"])
    probes["_rows_source"] = "_work_gkx21/GKX_INVENTORY.json（库存实测值，不重复 COUNT(*)）"

    # ---- 专利双 P90 ----
    vals = [float(r[1]) for r in patents if r[1] is not None]
    cites = [float(r[3] or 0) for r in patents]
    v_p90 = pct(vals, PERC) or 0
    c_p90 = pct(cites, PERC) or 0
    pat_break = [r for r in patents if (r[1] is not None and float(r[1]) >= v_p90 and v_p90 > 0) or (float(r[3] or 0) >= c_p90 and c_p90 > 0)]
    pat_break_both = [r for r in patents if (r[1] is not None and float(r[1]) >= v_p90 and v_p90 > 0) and (float(r[3] or 0) >= c_p90 and c_p90 > 0)]

    # ---- 论文 1 区 ----
    papers_q1 = [r for r in zh_papers if r[1] == 1]

    # ---- 项目国家级 ----
    proj_nat = [r for r in zh_projects if r[1] and '国家级' in str(r[1])]

    def topn(rows, key=lambda r: 0, n=10):
        return [str(r[0]) for r in sorted(rows, key=lambda r: -key(r))[:n]]

    result = {
        "metric_id": "M_INNOV_BREAKTHROUGH_COUNT",
        "metric_name": "重大成果突破数",
        "method": "高影响尾部计数（OR 逻辑）：专利 value/被引 双 P90；论文 jn_zone=1区；项目 project_level=国家级",
        "data_source": "gkx（三方库只读）：dwd_patent / dwd_patent_cited / dwd_zh_paper / dwd_zh_journal / dwd_zh_project",
        "window": f"{YEAR_LO}-{YEAR_HI}",
        "probes": probes,
        "compute": {
            "patent": {
                "n_sampled": len(patents),
                "value_p90": round(v_p90, 1) if v_p90 else None,
                "cited_p90": c_p90,
                "breakthrough_count": len(pat_break),
                "breakthrough_both_dims": len(pat_break_both),
                "sample_keys": topn(pat_break, key=lambda r: (float(r[1] or 0) + float(r[3] or 0) * 1000)),
            },
            "zh_paper": {
                "n_sampled": len(zh_papers),
                "q1_count": len(papers_q1),
                "zone_coverage": len([r for r in zh_papers if r[1] is not None]),
                "sample_keys": [str(r[0]) for r in papers_q1[:10]],
            },
            "zh_project": {
                "n_sampled": len(zh_projects),
                "national_count": len(proj_nat),
                "sample_keys": [str(r[0]) for r in proj_nat[:10]],
            },
            "total_breakthrough": len(pat_break) + len(papers_q1) + len(proj_nat),
        },
        "support_judgment": None,
    }

    pat_ok = len(patents) >= 100 and len(pat_break) > 0
    result["support_judgment"] = "部分支持" if pat_ok else "完全不支持"
    result["support_note"] = (
        f"专利维可算（n={len(patents)}，双P90 突破 {len(pat_break)} 件）；"
        f"论文维 jn_zone 实测非空 {probes['gkx.dwd_zh_journal.jn_zone_nonnull']} 行但窗内抽样命中 {len([r for r in zh_papers if r[1] is not None])} 条；"
        f"项目维 level_dist={probes['zh_project.level_dist']}；"
        "论文/项目突破判定维度当前数据弱 → 部分支持"
    )

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "compute"}, ensure_ascii=False, indent=1))
    print(json.dumps(result["compute"], ensure_ascii=False, indent=1)[:1800])


if __name__ == "__main__":
    main()
