#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M_INNOV_DS_FACTORS_015 · 要素影响力（期刊侧，对齐 M_INNOV_JOURNAL_INFLUENCE）
王惠口径：影响指数 0.50 + 发文量 0.25 + 被引用量 0.25，缺测维重归一，0-100。

数据面：三方库 gkx（只读）。
  gkx.dwd_zh_journal(publication_id, publication_type, impact_score, paper_nums, cite_nums)
  gkx.dwd_en_journal(publication_id, publication_type, impact_score, paper_nums, citation_rate)
      —— 英文表没有累计被引字段；citation_rate 亦为 0 非空
  gkx.dwd_zh_paper(publication_id) —— 仅用于校核「论文表回退」分支

输出：code/M_INNOV_DS_FACTORS_015_out.json
"""
import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "M_INNOV_DS_FACTORS_015_out.json")


def q1(cur, sql):
    cur.execute(sql)
    return cur.fetchone()


def pct_rank(values):
    """经验分位（0-100），同值取平均秩"""
    order = sorted(range(len(values)), key=lambda i: values[i])
    n = len(values)
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg_rank = (i + j) / 2.0
        for k in range(i, j + 1):
            ranks[order[k]] = 100.0 * avg_rank / (n - 1) if n > 1 else 0.0
        i = j + 1
    return ranks


def score_block(rows, has_cite):
    """按王惠权重合成，缺测维重归一"""
    pv = [float(r[3]) for r in rows]
    r_paper = pct_rank(pv)
    r_cite = pct_rank([float(r[4]) for r in rows]) if has_cite else None
    out = []
    for i, r in enumerate(rows):
        pub_id, name, ptype, paper, cite, loaded = r
        dims = [(0.50, None), (0.25, r_paper[i]),
                (0.25, (r_cite[i] if has_cite else None))]
        live = [(w, s) for w, s in dims if s is not None]
        wsum = sum(w for w, _ in live)
        s = sum(w * v for w, v in live) / wsum if wsum else None
        out.append({
            "publication_id": pub_id, "name": name, "type": ptype,
            "paper_nums": paper,
            "cite_nums": (cite if has_cite else None),
            "actual_papers_loaded": loaded,
            "s_paper": round(r_paper[i], 2),
            "s_cite": (round(r_cite[i], 2) if has_cite else None),
            "n_dims": len(live),
            "score": round(s, 2) if s is not None else None,
        })
    return out


res = {
    "metric_id": "M_INNOV_DS_FACTORS_015",
    "name": "要素影响力（期刊侧）",

    # 基期披露（派单书铁律 5）：期刊侧各维（载文量、基金占比、被引）取库内全量截面，
    # 不做逐年序列，故无基期；字段显式写空，避免被读成"未填"。
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": ("期刊侧指标为 dwd_zh_journal 全量截面汇总（载文量/基金论文占比/被引），"
                        "不构造年度序列，因此不使用基期分母；不存在把缺失年份按 0 摊入分母的情形。"),
    "aligned_to": "M_INNOV_JOURNAL_INFLUENCE",
    "data_plane": "gkx（183.240.141.251:3318）",
    "probe_time": "2026-10-22",
}
cur = gkx()
cur.execute("SET SESSION max_execution_time=120000")

# ---------------------------------------------------------------- 探测
res["probes"] = {}
r = q1(cur, """
 SELECT COUNT(*),
        SUM(impact_score IS NOT NULL AND impact_score>0),
        SUM(paper_nums IS NOT NULL AND paper_nums>0),
        SUM(cite_nums IS NOT NULL AND cite_nums>0),
        MIN(paper_nums), MAX(paper_nums), AVG(paper_nums),
        MIN(cite_nums), MAX(cite_nums), AVG(cite_nums)
 FROM gkx.dwd_zh_journal""")
res["probes"]["zh_journal"] = {
    "n": int(r[0]), "n_impact": int(r[1] or 0), "n_paper": int(r[2] or 0),
    "n_cite": int(r[3] or 0), "pmin": int(r[4]), "pmax": int(r[5]),
    "pav": round(float(r[6]), 2), "cmin": int(r[7]), "cmax": int(r[8]),
    "cav": round(float(r[9]), 2)}

r = q1(cur, """
 SELECT COUNT(*),
        SUM(impact_score IS NOT NULL AND impact_score>0),
        SUM(paper_nums IS NOT NULL AND paper_nums>0),
        SUM(citation_rate IS NOT NULL AND citation_rate>0),
        MIN(paper_nums), MAX(paper_nums), AVG(paper_nums)
 FROM gkx.dwd_en_journal""")
res["probes"]["en_journal"] = {
    "n": int(r[0]), "n_impact": int(r[1] or 0), "n_paper": int(r[2] or 0),
    "n_citation_rate_positive": int(r[3] or 0),
    "pmin": int(r[4]), "pmax": int(r[5]), "pav": round(float(r[6]), 2)}

cur.execute("SELECT publication_type, COUNT(*) FROM gkx.dwd_zh_journal GROUP BY publication_type")
res["probes"]["zh_journal_type"] = [[t, int(c)] for t, c in cur.fetchall()]
cur.execute("SELECT publication_type, COUNT(*) FROM gkx.dwd_en_journal GROUP BY publication_type")
res["probes"]["en_journal_type"] = [[t, int(c)] for t, c in cur.fetchall()]
cur.execute("SELECT publication_type, COUNT(*) FROM gkx.dwd_zh_paper GROUP BY publication_type")
res["probes"]["zh_paper_type"] = [[t, int(c)] for t, c in cur.fetchall()]
cur.execute("SELECT publication_type, COUNT(*) FROM gkx.dwd_en_paper GROUP BY publication_type")
res["probes"]["en_paper_type"] = [[t, int(c)] for t, c in cur.fetchall()]

# 论文表回退校核
cur.execute("""SELECT publication_id, COUNT(*) FROM gkx.dwd_zh_paper
               WHERE publication_id IS NOT NULL GROUP BY publication_id""")
pub_cnt = {pid: int(c) for pid, c in cur.fetchall()}
res["probes"]["zh_paper_distinct_pub"] = len(pub_cnt)
res["probes"]["zh_paper_rows"] = sum(pub_cnt.values())

# ---------------------------------------------------------------- 全量取数（3,401 行）
cur.execute("""SELECT publication_id, publication_type, zh_name, issn,
                      impact_score, paper_nums, cite_nums
               FROM gkx.dwd_zh_journal""")
zh = [(pid, nm, pt, int(p or 0), int(c or 0), pub_cnt.get(pid, 0))
      for pid, pt, nm, issn, imp, p, c in cur.fetchall()]
cur.execute("""SELECT publication_id, publication_type, en_name, zh_name,
                      impact_score, paper_nums
               FROM gkx.dwd_en_journal""")
en = [(pid, (nm or enm), pt, int(p or 0), None, pub_cnt.get(pid, 0))
      for pid, pt, enm, nm, imp, p in cur.fetchall()]

zh_s = score_block(zh, True)
en_s = score_block(en, False)

res["compute"] = {}
for tag, blk in [("zh", zh_s), ("en", en_s)]:
    sc = [x["score"] for x in blk if x["score"] is not None]
    res["compute"][tag] = {
        "n_scored": len(sc),
        "mean": round(statistics.mean(sc), 3) if sc else None,
        "median": round(statistics.median(sc), 3) if sc else None,
        "min": round(min(sc), 3) if sc else None,
        "max": round(max(sc), 3) if sc else None,
        "p10": round(sorted(sc)[int(0.10 * (len(sc) - 1))], 3) if sc else None,
        "p90": round(sorted(sc)[int(0.90 * (len(sc) - 1))], 3) if sc else None,
        "n_distinct_scores": len({round(x, 2) for x in sc}),
    }
    res["compute"][tag + "_top10"] = sorted(
        [x for x in blk if x["score"] is not None], key=lambda x: -x["score"])[:10]
    res["compute"][tag + "_bottom5"] = sorted(
        [x for x in blk if x["score"] is not None], key=lambda x: x["score"])[:5]

all_s = [x["score"] for x in zh_s + en_s if x["score"] is not None]
res["compute"]["pooled"] = {
    "n_scored": len(all_s), "mean": round(statistics.mean(all_s), 3),
    "median": round(statistics.median(all_s), 3),
    "min": min(all_s), "max": max(all_s)}

pairs = [(x["paper_nums"], x["actual_papers_loaded"]) for x in zh_s
         if x["paper_nums"] and x["actual_papers_loaded"]]
if len(pairs) > 10:
    a = [p[0] for p in pairs]
    b = [p[1] for p in pairs]
    ma, mb = statistics.mean(a), statistics.mean(b)
    cov = sum((x - ma) * (y - mb) for x, y in pairs)
    va = sum((x - ma) ** 2 for x in a) ** 0.5
    vb = sum((y - mb) ** 2 for y in b) ** 0.5
    res["compute"]["paper_nums_vs_loaded"] = {
        "n_pairs": len(pairs),
        "pearson_r": round(cov / (va * vb), 4) if va and vb else None,
        "mean_paper_nums": round(ma, 1), "mean_loaded": round(mb, 1),
        "note": "期刊表 paper_nums 为累计发文口径，论文表为已入湖样本，量级差约两个数量级",
    }

# ---------------------------------------------------------------- 定档
res["dimension_status"] = {
    "D1_impact_score": {
        "weight": 0.50,
        "zh_filled": res["probes"]["zh_journal"]["n_impact"],
        "en_filled": res["probes"]["en_journal"]["n_impact"],
        "zh_rows": res["probes"]["zh_journal"]["n"],
        "en_rows": res["probes"]["en_journal"]["n"],
        "status": "完全缺测（中文 0/2796、英文 0/605 非空）——50% 权重的主维无承载",
    },
    "D2_paper_nums": {
        "weight": 0.25,
        "zh_filled": res["probes"]["zh_journal"]["n_paper"],
        "en_filled": res["probes"]["en_journal"]["n_paper"],
        "status": "可用（100% 填充）；但为累计口径，与论文表已入湖样本不一致，需披露",
    },
    "D3_cite_nums": {
        "weight": 0.25, "zh_filled": res["probes"]["zh_journal"]["n_cite"], "en_filled": 0,
        "status": "中文可用；英文无累计被引字段，citation_rate 亦为 0 非空",
    },
}
res["support_judgment"] = "部分支持"
res["judgment_reason"] = (
    "期刊影响力三维中占 0.50 权重的影响指数（impact_score）在 gkx.dwd_zh_journal / "
    "dwd_en_journal 为 0 非空值，属结构性缺测；缺测维重归一后只剩「发文量 0.5 + 累计被引 0.5」，"
    "实际可算 2,796 本中文期刊（英文 605 本退化为发文量单维）。两维均为规模量，"
    "故判部分支持：可出相对排序，不可宣称复现影响指数。"
)
res["computable_subset"] = {
    "zh_journals": res["compute"]["zh"]["n_scored"],
    "en_journals": res["compute"]["en"]["n_scored"],
    "reweighted_formula_zh": "S = 0.5*S_paper + 0.5*S_cite",
    "reweighted_formula_en": "S = S_paper（单维）",
    "normalization": "经验分位秩（0-100），同值取平均秩",
}
res["thresholds"] = {"impact_index": "不可算（全空）", "min_journals": 30,
                     "note": "样本 ≥30 才做分位标准化；本库 2,796 本满足"}

# ---------------------------------------------------------------- 篇均被引变体
cur.execute("""SELECT zh_name, paper_nums, cite_nums FROM gkx.dwd_zh_journal
               WHERE paper_nums > 0 AND cite_nums IS NOT NULL""")
rows = [(nm, int(p), int(c), round(float(c) / float(p), 3))
        for nm, p, c in cur.fetchall() if p and c is not None]
per = sorted(rows, key=lambda t: -t[3])


def _rank(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    rk = [0] * len(xs)
    for j, i in enumerate(order):
        rk[i] = j + 1
    return rk


n_per = len(per)
r_tot = _rank([float(t[2]) for t in per])
r_per = _rank([t[3] for t in per])
d2 = sum((a - b) ** 2 for a, b in zip(r_tot, r_per))
spearman = 1 - 6.0 * d2 / (n_per * (n_per * n_per - 1)) if n_per > 1 else None
per_vals = sorted(t[3] for t in per)
res["variant_per_paper"] = {
    "n": n_per,
    "definition": "篇均被引 = cite_nums / paper_nums（累计口径，非两年影响因子）",
    "top10": [{"name": a, "paper_nums": b, "cite_nums": c, "per_paper": d}
              for a, b, c, d in per[:10]],
    "bottom5": [{"name": a, "paper_nums": b, "cite_nums": c, "per_paper": d}
                for a, b, c, d in per[-5:]],
    "median": round(per_vals[n_per // 2], 3),
    "p90": round(per_vals[int(n_per * 0.9)], 3),
    "max": round(per_vals[-1], 3),
    "spearman_total_vs_per": round(spearman, 4),
    "conclusion": ("累计被引与篇均被引整体正相关，但头部重排剧烈；"
                   "缺测重归一后仅存的发文量+累计被引两维均为规模量，"
                   "合成结果是「体量指数」而非「影响力」。"),
}
by_total = sorted(per, key=lambda t: -t[2])
res["variant_per_paper"]["example_shift"] = [
    {"name": nm,
     "rank_by_total": next(i + 1 for i, x in enumerate(by_total) if x[0] == nm),
     "rank_by_per_paper": next(i + 1 for i, x in enumerate(per) if x[0] == nm)}
    for nm in ["中国医药指南", "安徽农业科学", "中国组织工程研究", "中国法学", "生态学报"]
    if any(x[0] == nm for x in per)
]

cur.close()
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1, default=str)

print(json.dumps(res["probes"], ensure_ascii=False, default=str)[:1800])
print(json.dumps(res["dimension_status"], ensure_ascii=False, indent=1, default=str))
print(json.dumps({k: v for k, v in res["compute"].items() if not k.endswith("top10")},
                 ensure_ascii=False, default=str)[:1200])
print("zh top5:", json.dumps(res["compute"]["zh_top10"][:5], ensure_ascii=False, default=str))
print("variant:", json.dumps({k: v for k, v in res["variant_per_paper"].items()
                              if k not in ("top10", "bottom5")}, ensure_ascii=False))
print("->", OUT)
