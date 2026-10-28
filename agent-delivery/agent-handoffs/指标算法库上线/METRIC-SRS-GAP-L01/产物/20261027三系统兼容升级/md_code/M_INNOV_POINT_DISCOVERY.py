#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""创新点发现（M_INNOV_POINT_DISCOVERY）——A-25 批 · 三方库 gkx 版。

王惠口径（calc-logic INNOV V1.5-20260829）：
  词条 = 专利关键词 / 中文论文关键词 / IPC 前 4 位；
  突现强度 burst = (近 3 年年均 − 前 5 年年均) / max(前 5 年年均, 1)；
  新主题 is_new = 首次出现年 ≥ T−2；
  候选 = (burst ≥ 1 或 is_new) 且 近窗合计件数 ≥ 3；一行一个词条，不是 0—100 分。

取数（零全表扫，全部读缓存）：
  IPC4 × 年      全量 2,420,915 件 → `patent_ipc4_year_20261021.json`
  专利关键词     主键切片 200,000 行（6.80%）→ `a25_patent_sample.json`
  论文关键词     分类表 20,048 篇（19.87%）→ `a25_paper_panel.json`

基窗纪律（DATA_FACTS §3.16）：`dwd_patent.apdt_year` 只有 2021—2026，基窗 2017—2021
实际只有 2021 一年；脚本对每条词条输出 `base_years_used` / `base_years_missing`，
均值只除真实年数，不把缺失年按 0 摊进分母。论文侧 2017—2021 完整。

产物：code/M_INNOV_POINT_DISCOVERY_out.json
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import _a25_common as C

METRIC = "M_INNOV_POINT_DISCOVERY"
T = C.T_YEAR
RECENT = C.RECENT
BASE = C.BASE
MIN_RECENT = 3


def score_terms(counts: dict, available, top_n: int, kind: str) -> dict:
    rows = []
    for term, yc in counts.items():
        st = C.window_stats(yc, BASE, RECENT, available)
        if st["recent_total"] < MIN_RECENT:
            continue
        st["is_new"] = 1 if (st["t0"] is not None and st["t0"] >= T - 2) else 0
        st["candidate"] = 1 if (st["burst"] >= 1 or st["is_new"]) else 0
        st["term"] = term
        st["point_type"] = kind
        st["year_counts"] = {str(y): yc[y] for y in sorted(yc)}
        rows.append(st)
    cand = [r for r in rows if r["candidate"]]
    cand.sort(key=lambda r: (-r["burst"], -r["recent_total"]))
    return {
        "n_terms_scored": len(rows),
        "n_candidates": len(cand),
        "n_new": sum(1 for r in rows if r["is_new"]),
        "n_base_mean_zero": sum(1 for r in cand if r["b_mean"] <= 0),
        "n_genuine_burst": sum(1 for r in cand if r["b_mean"] > 0 and r["burst"] >= 1),
        "burst_dist": C.dist([r["burst"] for r in rows]),
        "recent_total_dist": C.dist([r["recent_total"] for r in cand]) if cand else {"n": 0},
        "top": cand[:top_n],
    }


MIGRATION_CODES = ("H10", "B64U")   # 2023 IPC 改版新增/迁移的小类族（H01L→H10x、B64C→B64U）


def paper_id_join() -> dict:
    """论文分类表与论文主表的 id 对账（决定论文关键词有没有「年份」可用）。"""
    return C.paper_id_join()


def migration_audit(tp, years_pat) -> dict:
    """IPC4 候选里有多少是「码迁移」而非真实技术突现。"""
    rows = []
    for term, yc in tp["ipc"].items():
        st = C.window_stats(yc, BASE, RECENT, years_pat)
        if st["recent_total"] < MIN_RECENT:
            continue
        isn = 1 if (st["t0"] is not None and st["t0"] >= T - 2) else 0
        if not (st["burst"] >= 1 or isn):
            continue
        st["term"] = term
        rows.append(st)
    rows.sort(key=lambda r: -r["burst"])
    mig = [r for r in rows if r["term"].startswith(MIGRATION_CODES)]
    rest = [r for r in rows if not r["term"].startswith(MIGRATION_CODES)]
    return {
        "n_candidates": len(rows),
        "n_migration": len(mig),
        "migration_codes": [r["term"] for r in mig],
        "n_after_exclusion": len(rest),
        "top_after_exclusion": [(r["term"], r["burst"], r["recent_total"]) for r in rest[:10]],
        "note": "H10x 是 2023 版 IPC 从 H01L 拆出的半导体小类族，B64U 从 B64C 拆出；"
                "H01L 同期从 6,789 件降到 4,097 件、B64C 从 569 件降到 180 件，属编码迁移不是技术突现",
    }


def main():
    years_pat = sorted({y for yc in C.ipc_year_full().values() for y in yc})
    p_year_all = C.paper_year_all()
    years_paper = sorted(y for y in p_year_all if p_year_all[y] > 0)
    tp = C.term_panel()

    out = {
        "metric_id": METRIC,
        "metric_name": "创新点发现",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "definition": ("词条级突现检测：burst=(近窗年均−基窗年均)/max(基窗年均,1)，"
                       "is_new=首次出现年≥T−2，候选=(burst≥1 或 is_new)且近窗件数≥3"),
        "statistical_year": T,
        "windows": {"base": list(BASE), "recent": list(RECENT)},
        "data_source": ("gkx.dwd_patent（IPC4 全量缓存 + 关键词主键切片 6.80%）、"
                        "gkx.dwd_zh_paper_classification（20,048 篇）"),
        "probes": {},
        "result": {},
        "support_judgment": None,
        "reasons": [],
    }

    # ---- 探针口径（读到什么、缺什么）----
    ss = C.sample_stats()
    out["probes"] = {
        "ipc_full": {
            "patents_with_ipc": sum(sum(v.values()) for v in tp["ipc"].values()),
            "n_ipc4": len(tp["ipc"]),
            "years": years_pat,
        },
        "patent_sample": {
            "rows": ss["n"], "share": ss["meta"]["share"],
            "kw_share": ss["kw_share"], "ipc_share": ss["ipc_share"],
            "grant_rate": ss["grant_rate"], "year_dist": ss["year_dist"],
        },
        "paper_keywords": {
            "papers_classified": len(C.papers()),
            "papers_total": sum(p_year_all.values()),
            "share": round(len(C.papers()) / max(sum(p_year_all.values()), 1), 4),
            "years": years_paper[-10:],
            "year_counts": {str(y): p_year_all[y] for y in years_paper if y >= 2015},
        },
        "patent_year_full": {str(y): n for y, n in sorted(C.year_full().items())},
        "paper_id_join": paper_id_join(),
        "ipc4_migration": migration_audit(tp, years_pat),
    }

    # ---- 三类词条 ----
    ipc_res = score_terms(tp["ipc"], years_pat, 40, "ipc4")
    kwp_res = score_terms(tp["kwp"], years_pat, 40, "keyword_patent")
    kwa_res = score_terms(tp["kwa"], years_paper, 40, "keyword_paper")
    out["result"] = {"ipc4": ipc_res, "keyword_patent": kwp_res, "keyword_paper": kwa_res}

    # ---- 敏感性：把 T 推到 2025（近窗 2023—2025），看 IPC4 候选排序是否稳定 ----
    def rank_for(t_recent, t_base):
        m = {}
        for term, yc in tp["ipc"].items():
            st = C.window_stats(yc, t_base, t_recent, years_pat)
            if st["recent_total"] < MIN_RECENT:
                continue
            m[term] = st["burst"]
        return m
    a = rank_for(RECENT, BASE)
    b = rank_for((2023, 2024, 2025), BASE)
    common = [k for k in a if k in b]
    rho = C.spearman([a[k] for k in common], [b[k] for k in common]) if len(common) > 10 else None
    out["sensitivity"] = {
        "primary_window": {"recent": list(RECENT), "n": len(a)},
        "alt_window": {"recent": [2023, 2024, 2025], "n": len(b)},
        "n_common": len(common),
        "spearman_burst": rho,
        "note": "2025 年入库 440,401 件（低于 2023/2024 的 60 万级），含公开滞后，仅作敏感性对照",
    }

    # ---- 判档 ----
    out["support_judgment"] = "部分支持"
    out["reasons"] = [
        "IPC4 词条为全量（2,420,915 件有 IPC），burst 与 is_new 可直接算，该点类型完全可执行；",
        "专利关键词只有主键切片 6.80%（200,000/2,939,895），全表扫被禁（apdt_year/keywords 无索引，"
        "GROUP BY 会跑满 600 秒断连），词条级件数是样本口径，不可外推为全量；",
        "专利基窗 2017—2020 在库内零行，burst 的分母只取 2021 一年（base_years_used=[2021]），"
        "与公式的「前 5 年均值」不等价，且「新主题」无法区分「2022 年才出现」与「2017—2020 有、2021 没有」；",
        "论文关键词只覆盖分类表 20,048 篇（19.87%），其中只有 799 篇的 id 能对上 `dwd_zh_paper` 拿到年份"
        "（id 连通率 3.99%），其余 19,249 篇无时间轴，论文侧实际只剩 2 个候选词条，不足以成维；",
        "IPC4 候选中有 6 个来自 2023 版 IPC 改版的小类族（H10F/H10H/H10D/H10W/H10B 与 B64U），"
        "同期 H01L 由 6,789 件降到 4,097 件、B64C 由 569 件降到 180 件，属编码迁移而非技术突现，须单列剔除项；",
    ]
    out["readme"] = {
        "ipc4_note": "burst 的分母为 2021 年单年均值；base_years_used 逐条写在候选行内",
        "keyword_note": "专利关键词件数为 6.80% 切片计数，比值（burst）可用，绝对件数不可外推",
        "paper_note": "论文侧基窗 2017—2021 完整，is_new 判断比专利侧可靠",
    }

    p = HERE / f"{METRIC}_out.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print("written", p)
    for k, v in out["result"].items():
        print(k, "scored", v["n_terms_scored"], "cand", v["n_candidates"], "new", v["n_new"],
              "burst_med", v["burst_dist"].get("median"))
    print("sens spearman", out["sensitivity"]["spearman_burst"], "n", out["sensitivity"]["n_common"])


if __name__ == "__main__":
    main()
