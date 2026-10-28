#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""
M_INNOV_DS_FACTORS_014 · 要素影响力（专利侧，对齐 M_INNOV_PATENT_INFLUENCE）
王惠口径：被引次数 0.80 + 专利价值 0.20，缺测维重归一，取值 0-100。

数据面：三方库 gkx（183.240.141.251:3318），只读：
  1) gkx.dwd_patent_cited 规模/分位（20,515 行小表）
  2) gkx.dwd_patent_cited 全量（patent_id / pn / cited_by_nums，2 万行）
  3) gkx.dwd_patent 按 patent_id 批量点查（唯一索引，300 个一包）
  4) gkx.dwd_patent 按 pn 批量点查（普通索引，第二键互证）

**不做大表 JOIN**：`cited ⋈ patent` 的明细 JOIN 实测被优化器退化成扫 294 万行，
被 120s 语句上限掐断（errno 3024）；改为「小表入内存 + 主键 IN 批量点查」，
语句上限放宽到 600s，绝不用 `max_execution_time=0`。

对 2,939,895 行的 dwd_patent 不发任何聚合：主表总量读面板缓存，
价值分布读 _snapshots21/patent_value_agg_gkx.json（按 dwd_id 分块 GROUP BY
的全表缓存，非采样）。

输出：code/M_INNOV_DS_FACTORS_014_out.json
"""
import json
import math
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "M_INNOV_DS_FACTORS_014_out.json")
SNAP = os.path.join(HERE, "_snapshots21")
VALUE_CACHE = os.path.join(SNAP, "patent_value_agg_gkx.json")
PANEL_CACHE = os.path.join(SNAP, "patent_panel_innov_20261021.json")

# 归一化端点：价值取库内实测 min/max（3,000—774 万），被引取 cited_by_nums 实测 max
LO, HI = 3000.0, 7740000.0
LOG_LO, LOG_HI = math.log10(LO), math.log10(HI)


def s_value(v):
    """专利价值对数 min-max 到 0-100（价值跨 3 个半数量级，线性会压死长尾）"""
    if v is None:
        return None
    v = float(v)
    if v <= 0:
        return None
    return max(0.0, min(100.0, 100.0 * (math.log10(v) - LOG_LO) / (LOG_HI - LOG_LO)))


def s_cited(c, cap):
    if c is None or cap <= 0:
        return None
    return max(0.0, min(100.0, 100.0 * float(c) / cap))


def combine(sv, sc):
    """王惠口径 0.80/0.20，缺测维重归一；返回 (分数, 有效维数)"""
    dims = [(0.80, sc), (0.20, sv)]
    live = [(w, s) for w, s in dims if s is not None]
    if not live:
        return None, 0
    wsum = sum(w for w, _ in live)
    return sum(w * s for w, s in live) / wsum, len(live)


def q1(cur, sql):
    cur.execute(sql)
    row = cur.fetchone()
    return row[0] if row else None


res = {
    "metric_id": "M_INNOV_DS_FACTORS_014",
    "name": "要素影响力（专利侧）",
    "aligned_to": "M_INNOV_PATENT_INFLUENCE",
    "data_plane": "gkx（183.240.141.251:3318）",
    "probe_time": "2026-10-22",
    "formula": "S = (0.80*S_cited + 0.20*S_value) / Σw，缺测维重归一",
}

# ---------------------------------------------------------------- 价值维（离线全表缓存）
for p in (VALUE_CACHE, PANEL_CACHE):
    if not os.path.exists(p):
        raise SystemExit(f"缺少缓存 {p}")
vc = json.load(open(VALUE_CACHE, encoding="utf-8"))
panel = json.load(open(PANEL_CACHE, encoding="utf-8"))
year_all = {int(k): int(v) for k, v in panel["year_all"].items()}
n_pat = int(panel["rows"])
n_value = int(vc["n_nonnull"])
hist_scores = [(float(b), int(c)) for b, c in vc["histogram_score_5pt"]]
zero_bucket = sum(c for b, c in hist_scores if b == 0.0)
top3_share = 100.0 * sum(t["count"] for t in vc["top_by_count"][:3]) / n_value

res["probes"] = {
    "patent_rows": n_pat,
    "patent_rows_source": "patent_panel_innov_20261021.json（全库面板，非本次查询）",
    "value_nonnull": n_value,
    "value_fill_pct": round(100.0 * n_value / n_pat, 4),
    "value_source": vc["source"],
    "value_blocks": vc["blocks"],
}
res["compute"] = {}
res["compute"]["value_dim"] = {
    "n": n_value,
    "min": vc["min"], "max": vc["max"],
    "mean": vc["mean"], "std": vc["std"], "median_value": vc["median_value"],
    "distinct_values": vc["n_distinct_value"],
    "top_by_count": vc["top_by_count"][:8],
    "histogram_score_5pt": [[b, c] for b, c in hist_scores],
}
res["compute"]["value_degeneracy"] = {
    "zero_bucket_share_pct": round(100.0 * zero_bucket / n_value, 2),
    "top3_value_share_pct": round(top3_share, 2),
    "distinct_values": vc["n_distinct_value"],
    "score_mean": vc.get("score_stats", {}).get("mean"),
    "score_std": vc.get("score_stats", {}).get("std"),
    "score_median": vc.get("score_stats", {}).get("median"),
    "score_p90": vc.get("score_stats", {}).get("p90"),
    "score_stats_note": vc.get("score_stats", {}).get("note"),
    "meaning": "价值列为分档估值而非连续值：前三档占非空行七成，归一到 0-100 后八成落在 0-5 分",
}

cur = gkx()
# 上限 10 分钟：不用 0（0 会让单条语句无限等，挂住共享实例且无法断点续跑）
cur.execute("SET SESSION max_execution_time=600000")

# ---------------------------------------------------------------- 被引维（5 条 SQL 全部落在 2 万行小表）
cur.execute("SELECT COUNT(*), SUM(cited_by_nums>0), MIN(cited_by_nums), "
            "MAX(cited_by_nums), AVG(cited_by_nums), STDDEV(cited_by_nums) "
            "FROM gkx.dwd_patent_cited")
n_cited, n_pos, mn, mx, av, sd = cur.fetchone()
n_cited, n_pos = int(n_cited), int(n_pos or 0)
CITED_MAX = float(mx or 55)
res["probes"]["patent_cited_rows"] = n_cited
res["probes"]["cited_positive"] = n_pos
res["probes"]["cited_stats"] = {
    "min": int(mn), "max": int(mx), "mean": round(float(av), 4), "std": round(float(sd), 4)}

# 回连主表：不做大表 JOIN（优化器会退化成扫 294 万行，实测被 120s 上限掐断），
# 改为「小表全量入内存 + 主键 IN 批量点查」。patent_id 有唯一索引、pn 有普通索引。
cur.execute("SELECT patent_id, pn, cited_by_nums FROM gkx.dwd_patent_cited")
cited_rows = cur.fetchall()


def batched(seq, n=300):
    seq = list(seq)
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


pat_ids = sorted({r[0] for r in cited_rows if r[0]})
cited_pns = sorted({r[1] for r in cited_rows if r[1]})

main_by_id = {}
for chunk in batched(pat_ids):
    ph = ",".join(["%s"] * len(chunk))
    cur.execute(
        "SELECT patent_id, pn, first_applicant_name, apdt_year, value "
        "FROM gkx.dwd_patent WHERE patent_id IN (" + ph + ")", chunk)
    for pid, pn, app, y, v in cur.fetchall():
        main_by_id[pid] = (pn, app, y, v)

pn_hit = set()
for chunk in batched(cited_pns):
    ph = ",".join(["%s"] * len(chunk))
    cur.execute("SELECT pn FROM gkx.dwd_patent WHERE pn IN (" + ph + ")", chunk)
    pn_hit.update(r[0] for r in cur.fetchall())

join_rows_pid = sum(1 for r in cited_rows if r[0] in main_by_id)
res["probes"]["cited_join_patent_id"] = join_rows_pid
res["probes"]["cited_join_patent_id_unique"] = len(main_by_id)
res["probes"]["cited_join_pn"] = sum(1 for r in cited_rows if r[1] in pn_hit)
n_join = join_rows_pid
res["probes"]["cited_coverage_pct"] = round(100.0 * n_join / n_pat, 6)

two_dim = []
for pid, cpn, cited in cited_rows:
    if cited is None or pid not in main_by_id:
        continue
    pn, applicant, year, value = main_by_id[pid]
    sc = s_cited(cited, CITED_MAX)
    sv = s_value(value)
    score, k = combine(sv, sc)
    if score is None:
        continue
    two_dim.append({
        "patent_id": pid, "pn": pn or cpn, "applicant": applicant, "year": year,
        "value": float(value) if value is not None else None,
        "cited": int(cited),
        "s_cited": round(sc, 2),
        "s_value": (round(sv, 2) if sv is not None else None),
        "score": round(score, 2), "n_dims": k,
    })
two_dim.sort(key=lambda x: (-x["score"], x["pn"] or ""))
scores2 = [x["score"] for x in two_dim]
res["compute"]["two_dim_subset"] = {
    "n": len(two_dim),
    "mean": round(statistics.mean(scores2), 3) if scores2 else None,
    "median": round(statistics.median(scores2), 3) if scores2 else None,
    "min": min(scores2) if scores2 else None,
    "max": max(scores2) if scores2 else None,
    "n_with_cited_positive": sum(1 for x in two_dim if x["cited"] > 0),
    "n_with_value": sum(1 for x in two_dim if x["s_value"] is not None),
    "top10": two_dim[:10],
    "bottom5": two_dim[-5:],
}

# ---------------------------------------------------------------- 分年覆盖（由 475 行结果直接汇总）
cited_by_year = {}
for x in two_dim:
    if x["year"] is not None:
        cited_by_year[int(x["year"])] = cited_by_year.get(int(x["year"]), 0) + 1
res["compute"]["coverage_by_year"] = [
    {"year": y, "patents": year_all[y],
     "cited_joinable": cited_by_year.get(y, 0),
     "join_pct": round(100.0 * cited_by_year.get(y, 0) / year_all[y], 6)}
    for y in sorted(year_all)
]
res["compute"]["year_all"] = {str(k): v for k, v in sorted(year_all.items())}

# ---------------------------------------------------------------- 定档
res["dimension_status"] = {
    "D1_cited_by_nums": {
        "weight": 0.80, "table": "gkx.dwd_patent_cited(cited_by_nums)",
        "rows": n_cited, "joinable_to_patent": n_join,
        "joinable_unique_patents": len(main_by_id),
        "coverage_pct": res["probes"]["cited_coverage_pct"],
        "status": "不可用（覆盖率 0.0162%，占 0.80 权重的维度无法参与全库计算）",
    },
    "D2_patent_value": {
        "weight": 0.20, "table": "gkx.dwd_patent(value)",
        "filled": n_value, "fill_pct": res["probes"]["value_fill_pct"],
        "distinct_values": vc["n_distinct_value"],
        "status": "可用但高度退化（67.85% 填充；362 档取值；81.95% 落在 0-5 分桶）",
    },
}
res["support_judgment"] = "部分支持"
res["judgment_reason"] = (
    "专利影响力按王惠口径为「被引 0.80 + 价值 0.20」，占 0.80 权重的被引维在 gkx 上"
    f"仅 {n_join} 行（{len(main_by_id)} 件不同专利）可与主表对齐（覆盖 {res['probes']['cited_coverage_pct']}%），"
    "按缺测维重归一后退化为「专利价值单维分」，可批量产出但语义已不是影响力；"
    f"价值维虽 {res['probes']['value_fill_pct']}% 填充，但只有 {vc['n_distinct_value']} 个取值、"
    f"{res['compute']['value_degeneracy']['zero_bucket_share_pct']}% 落在 0-5 分桶，区分度不足。"
    "故判部分支持：价值维可算（199.48 万件），被引维缺口需甲方补 dwd_patent_cited 全量并与主表统一 ID。"
)
res["computable_subset"] = {
    "value_only": n_value,
    "two_dim": len(two_dim),
    "reweighted_formula": "S = 0.80*S_cited + 0.20*S_value（两维齐备时）；仅价值时 S = S_value",
}
res["thresholds"] = {
    "S_value_lo": vc["min"], "S_value_hi": vc["max"], "S_cited_max": CITED_MAX,
    "meaning": "0=库内最低价值/零被引；100=库内最高价值/最高被引",
}

cur.close()
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1, default=str)

print(json.dumps({"probes": res["probes"], "value_degeneracy": res["compute"]["value_degeneracy"],
                   "dimension_status": res["dimension_status"],
                   "support_judgment": res["support_judgment"]},
                 ensure_ascii=False, indent=1, default=str)[:2400])
print("two_dim:", json.dumps({k: v for k, v in res["compute"]["two_dim_subset"].items()
                              if k not in ("top10", "bottom5")}, ensure_ascii=False))
print("coverage_by_year:", json.dumps(res["compute"]["coverage_by_year"], ensure_ascii=False))
print("->", OUT)
