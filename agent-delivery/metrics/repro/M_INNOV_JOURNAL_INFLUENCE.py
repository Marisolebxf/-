#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_JOURNAL_INFLUENCE · 期刊影响力（gkx 换源版）

王惠口径（V1.3-20260829）：
  期刊影响力 = (0.5*norm(影响指数) + 0.25*norm(发文量) + 0.25*norm(被引量)) × 100
  入集：dwd_zh_journal / dwd_en_journal 按 publication_id 去重；缺测维不补 0，剩余维重归一。

gkx 实测（2026-10-22 复核，与 20261020 的 demo 结论一致）：
  - impact_score：中文刊 0/2,796、英文刊 0/605 全部为 NULL → 影响指数维整维缺失。
    这是本指标必须降档的**硬约束**，不是可插补的偶发空值。
  - 中文刊 cite_nums 2,796/2,796 有值；英文刊无 cite_nums 列。
  - paper_nums 与库内论文回连 0/2,796 相等（最大 650,715 > 全库中文论文 100,900）
    → 刊库累计口径，非统计年口径。
  - 引文代理：篇均被引 = 库内被引合计 / 库内论文数（dwd_zh_paper_citation，20,031 篇）。

只读 gkx 三方库，不引用任何演示库或开发库旁路。
输出：code/M_INNOV_JOURNAL_INFLUENCE_out.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _gkxdb  # noqa: E402

OUT = HERE / "M_INNOV_JOURNAL_INFLUENCE_out.json"


def q(sql):
    cur = _gkxdb.gkx()
    try:
        cur.execute(sql)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]
    finally:
        cur.close()


def q1(sql):
    r = q(sql)
    return r[0] if r else None


def f(x):
    try:
        return float(x) if x is not None else None
    except Exception:
        return None


def minmax(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return []
    lo, hi = min(xs), max(xs)
    if hi == lo:
        return [0.0 for _ in xs]
    return [(x - lo) / (hi - lo) for x in xs]


def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


def spearman(a, b):
    pairs = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    if len(pairs) < 3:
        return None
    ra, rb = ranks([p[0] for p in pairs]), ranks([p[1] for p in pairs])
    n = len(pairs)
    ma, mb = sum(ra) / n, sum(rb) / n
    cov = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    va = sum((x - ma) ** 2 for x in ra) ** 0.5
    vb = sum((y - mb) ** 2 for y in rb) ** 0.5
    return round(cov / (va * vb), 4) if va and vb else None


def dist(xs):
    xs = sorted(x for x in xs if x is not None)
    if not xs:
        return {"n": 0}
    n = len(xs)

    def pct(p):
        k = min(n - 1, max(0, int(round((n - 1) * p))))
        return round(xs[k], 4)

    return {"n": n, "min": round(xs[0], 4), "p10": pct(.10), "p25": pct(.25),
            "p50": pct(.5), "p75": pct(.75), "p90": pct(.9), "p99": pct(.99),
            "max": round(xs[-1], 4), "mean": round(sum(xs) / n, 4),
            "n_distinct": len({round(x, 2) for x in xs})}


res = {
    "metric_id": "M_INNOV_JOURNAL_INFLUENCE",
    "metric_name": "期刊影响力",
    "generated_at": "2026-10-22",
    "formula_owner": "王惠（V1.3-20260829）",
    "data_source": "gkx.dwd_zh_journal / dwd_en_journal / dwd_zh_paper / dwd_zh_paper_citation",
}

# ---------- 1. 入集与三维填充 ----------
zh = q("""SELECT publication_id, zh_name AS nm, publication_type AS pt,
          paper_nums, cite_nums, impact_score FROM gkx.dwd_zh_journal""")
en = q("""SELECT publication_id, en_name AS nm, publication_type AS pt,
          paper_nums, impact_score FROM gkx.dwd_en_journal""")

res["dimension_fill"] = {
    "zh": {"n": len(zh),
           "impact_nonnull": sum(1 for r in zh if r["impact_score"] is not None),
           "paper_nums_nonnull": sum(1 for r in zh if r["paper_nums"] is not None),
           "cite_nums_nonnull": sum(1 for r in zh if r["cite_nums"] is not None)},
    "en": {"n": len(en),
           "impact_nonnull": sum(1 for r in en if r["impact_score"] is not None),
           "paper_nums_nonnull": sum(1 for r in en if r["paper_nums"] is not None),
           "cite_nums_nonnull": 0},
}
res["en_type_dist"] = {}
for r in en:
    res["en_type_dist"][r["pt"]] = res["en_type_dist"].get(r["pt"], 0) + 1

# ---------- 2. 库内真实回连 ----------
real = {r["publication_id"]: int(r["n"]) for r in q("""
    SELECT publication_id, COUNT(*) AS n FROM gkx.dwd_zh_paper
    WHERE publication_id IS NOT NULL GROUP BY publication_id""")}
cit = {r["publication_id"]: {"papers_with_cit": int(r["n"]), "cit_sum": int(r["s"] or 0)}
       for r in q("""SELECT p.publication_id AS publication_id, COUNT(*) AS n, SUM(x.citation_num) AS s
                     FROM gkx.dwd_zh_paper_citation x
                     JOIN gkx.dwd_zh_paper p ON p.id=x.id
                     WHERE p.publication_id IS NOT NULL GROUP BY p.publication_id""")}
zh_ids = {r["publication_id"] for r in zh}

res["real_backlink"] = {
    "journals_with_library_papers": len([k for k, n in real.items() if n > 0 and k in zh_ids]),
    "journals_with_citation_records": len(cit),
    "citation_rows": int(q1("SELECT COUNT(*) AS n FROM gkx.dwd_zh_paper_citation")["n"]),
    "papers_total": int(q1("SELECT COUNT(*) AS n FROM gkx.dwd_zh_paper")["n"]),
    "note": "dwd_zh_paper 100,900 篇中 65,896 篇可挂到期刊；被引记录覆盖 20,031 篇论文",
}

pairs = [(int(r["paper_nums"]), real.get(r["publication_id"], 0)) for r in zh
         if r["paper_nums"] is not None]
equal = sum(1 for a, b in pairs if a == b)
res["paper_nums_consistency"] = {
    "n_pairs": len(pairs),
    "n_equal": equal,
    "equal_rate": round(equal / len(pairs), 4) if pairs else None,
    "spearman_vs_library_count": spearman([a for a, _ in pairs], [b for _, b in pairs]),
    "max_paper_nums": max((a for a, _ in pairs), default=None),
    "library_total_zh_papers": 100900,
    "journals_with_paper_nums_gt_library_total": sum(1 for a, _ in pairs if a > 100900),
    "verdict": "paper_nums 为刊库累计发文口径，与库内统计年论文数不同源（0 本相等）",
}

# ---------- 3. 打分：v1 王惠原式（影响指数缺测 → 两维重归一） ----------
rows = []
for r in zh:
    pn = f(r["paper_nums"]) or 0.0
    cn = f(r["cite_nums"]) or 0.0
    rp = real.get(r["publication_id"], 0)
    cc = cit.get(r["publication_id"], {})
    rows.append({
        "publication_id": r["publication_id"], "name": r["nm"],
        "impact_score": f(r["impact_score"]),
        "paper_nums": pn, "cite_nums": cn,
        "real_papers": rp,
        "real_cited_papers": cc.get("papers_with_cit", 0),
        "real_citation_sum": cc.get("cit_sum", 0),
        "cite_per_paper_dir": round(cn / pn, 6) if pn > 0 else None,
        "cite_per_paper_real": round(cc.get("cit_sum", 0) / rp, 6) if rp > 0 else None,
    })

nB = minmax([r["paper_nums"] for r in rows])
nC = minmax([r["cite_nums"] for r in rows])
for r, b, c2 in zip(rows, nB, nC):
    r["score_v1_2dim"] = round(100 * (0.5 * b + 0.5 * c2), 2)

sub = [r for r in rows if r["real_papers"] > 0 and r["real_cited_papers"] > 0]
nA2 = minmax([r["cite_per_paper_real"] for r in sub])
nB2 = minmax([r["real_papers"] for r in sub])
nC2 = minmax([r["real_citation_sum"] for r in sub])
for r, a, b, c3 in zip(sub, nA2, nB2, nC2):
    r["proxy_impact"] = r["cite_per_paper_real"]
    r["score_v2_proxy3dim"] = round(100 * (0.5 * a + 0.25 * b + 0.25 * c3), 2)

sp_v1_v2 = spearman([r["score_v1_2dim"] for r in sub], [r["score_v2_proxy3dim"] for r in sub])
sp_dir_real = spearman([r["cite_per_paper_dir"] for r in sub], [r["cite_per_paper_real"] for r in sub])

rows.sort(key=lambda x: -x["score_v1_2dim"])
for i, r in enumerate(rows, 1):
    r["rank_v1"] = i
sub.sort(key=lambda x: -x["score_v2_proxy3dim"])

res["score_v1"] = {
    "formula": "0.5*norm(paper_nums) + 0.5*norm(cite_nums)，影响指数维缺测后重归一",
    "n_scored": len(rows),
    "stats": dist([r["score_v1_2dim"] for r in rows]),
    "top15": rows[:15],
    "bottom5": rows[-5:],
}
res["score_v2_proxy"] = {
    "formula": "0.5*norm(篇均被引_库内) + 0.25*norm(库内论文数) + 0.25*norm(库内被引合计)",
    "n_scored": len(sub),
    "coverage_of_journals": round(len(sub) / len(rows), 4) if rows else 0,
    "stats": dist([r["score_v2_proxy3dim"] for r in sub]),
    "top15": sub[:15],
    "spearman_v1_vs_v2": sp_v1_v2,
    "spearman_direct_vs_real_cite_per_paper": sp_dir_real,
    "proxy_precision_note": "代理为篇均被引，非 JCR 影响因子；仅在 20,031 篇有被引记录的论文上可算，"
                            "覆盖期刊 %d/%d（%.1f%%）" % (len(sub), len(rows), 100 * len(sub) / len(rows) if rows else 0),
}

res["en_journals"] = {
    "n": len(en),
    "scored": False,
    "reason": "impact_score 0/605 非空、无 cite_nums 列，仅 paper_nums 一维 → 单维无法构成 0—100 相对分",
    "paper_nums_stats": dist([f(r["paper_nums"]) for r in en if r["paper_nums"] is not None]),
}

res["support_judgment"] = {
    "data_support_level": "部分支持",
    "reasons": [
        "影响指数维（权重 0.50）整维缺失：impact_score 中文刊 0/2,796、英文刊 0/605 非空",
        "被引量维仅中文刊有（cite_nums 2,796/2,796），英文刊无该列 → 英文刊最多一维，不可评分",
        "发文量维可用但口径为刊库累计（paper_nums），与库内统计年论文数 0 本相等，最大 650,715 超全库 100,900",
        "已给出引文代理（篇均被引）并量化代理精度与覆盖率，但代理不是 JCR 影响因子",
    ],
}

OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
print(json.dumps({k: res[k] for k in ("dimension_fill", "paper_nums_consistency", "real_backlink")},
                 ensure_ascii=False, indent=1)[:2500])
print("v1 top5:", [(r["name"], r["score_v1_2dim"], r["paper_nums"], r["cite_nums"]) for r in rows[:5]])
print("v2 n:", len(sub), "sp v1-v2:", sp_v1_v2, "proxy cov:", res["score_v2_proxy"]["coverage_of_journals"])
print("wrote", OUT.name)
