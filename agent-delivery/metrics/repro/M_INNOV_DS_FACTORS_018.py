#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M_INNOV_DS_FACTORS_018 · 监测趋势预测（对齐 M_INNOV_FACTOR_FORECAST）
王惠口径：会议 / 项目 / 专利 / 期刊年度件数时序，满 8 期用 Holt 线性趋势，
          年预 2 期，件数不为负，输出点预测与约 80% 区间（不是 0-100 分）。

数据面：三方库 gkx（只读）+ 专利面板离线缓存。
  gkx.dwd_zh_paper.cover_year_start
  gkx.dwd_zh_project.approval_year
  gkx.dwd_en_project.approval_year（全空）
  gkx.dwd_zh_journal.founding_time（仅做截断诊断）
  专利年度件数：code/_snapshots21/patent_panel_innov_20261021.json 的 year_all
                （全量 2,939,895 行面板，禁止再对 dwd_patent 写 GROUP BY apdt_year）

输出：code/M_INNOV_DS_FACTORS_018_out.json
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "M_INNOV_DS_FACTORS_018_out.json")


def holt(y, alpha, beta, h=2):
    l = y[0]
    b = y[1] - y[0]
    fit = [None]
    sse = 0.0
    resid = []
    for t in range(1, len(y)):
        yhat = l + b
        e = y[t] - yhat
        fit.append(yhat)
        sse += e * e
        resid.append(e)
        l_new = alpha * y[t] + (1 - alpha) * (l + b)
        b_new = beta * (l_new - l) + (1 - beta) * b
        l, b = l_new, b_new
    fc = [max(0.0, l + b * k) for k in range(1, h + 1)]
    return {"sse": sse, "fit": fit, "resid": resid, "forecast": fc,
            "level": l, "trend": b}


def fit_best(y, h=2):
    best = None
    for ai in range(1, 20):
        for bi in range(1, 20):
            a, b = ai / 20.0, bi / 20.0
            m = holt(y, a, b, h)
            if best is None or m["sse"] < best[0]["sse"]:
                best = (m, a, b)
    m, a, b = best
    n = len(y)
    sigma = math.sqrt(m["sse"] / max(1, n - 2))
    iv = [[max(0.0, f - 1.28 * sigma * math.sqrt(k + 1)),
           f + 1.28 * sigma * math.sqrt(k + 1)]
          for k, f in enumerate(m["forecast"])]
    return {"alpha": round(a, 3), "beta": round(b, 3),
            "level": round(m["level"], 2), "trend": round(m["trend"], 2),
            "sigma": round(sigma, 3),
            "forecast": [round(x, 1) for x in m["forecast"]],
            "interval80": [[round(lo, 1), round(hi, 1)] for lo, hi in iv],
            "fit": [None if x is None else round(x, 1) for x in m["fit"]],
            "sse": round(m["sse"], 2)}


def mape(actual, pred):
    pairs = [(a, p) for a, p in zip(actual, pred) if a]
    return round(100.0 * sum(abs(a - p) / a for a, p in pairs) / len(pairs), 2) if pairs else None


res = {
    "metric_id": "M_INNOV_DS_FACTORS_018",
    "name": "监测趋势预测",
    "aligned_to": "M_INNOV_FACTOR_FORECAST",
    "data_plane": "gkx（183.240.141.251:3318）",
    "probe_time": "2026-10-22",
}
cur = gkx()
cur.execute("SET SESSION max_execution_time=120000")

# ---------------------------------------------------------------- 序列探测
res["probes"] = {}
cur.execute("""SELECT cover_year_start, COUNT(*) FROM gkx.dwd_zh_paper
               WHERE cover_year_start IS NOT NULL GROUP BY cover_year_start
               ORDER BY cover_year_start""")
res["probes"]["paper_year"] = [[int(float(y)), int(c)] for y, c in cur.fetchall()]
cur.execute("""SELECT cover_year_start, COUNT(*) FROM gkx.dwd_en_paper
               WHERE cover_year_start IS NOT NULL GROUP BY cover_year_start
               ORDER BY cover_year_start""")
res["probes"]["en_paper_year"] = [[int(float(y)), int(c)] for y, c in cur.fetchall()]
cur.execute("""SELECT CAST(approval_year/10000 AS UNSIGNED), COUNT(*)
               FROM gkx.dwd_zh_project WHERE approval_year IS NOT NULL
               GROUP BY CAST(approval_year/10000 AS UNSIGNED)
               ORDER BY 1""")
res["probes"]["project_year"] = [[int(y), int(c)] for y, c in cur.fetchall()]
cur.execute("SELECT SUM(approval_year IS NULL), COUNT(*) FROM gkx.dwd_en_project")
r = cur.fetchone()
res["probes"]["en_project_null_year"] = {"nulls": int(r[0] or 0), "n": int(r[1])}
cur.execute("""SELECT YEAR(founding_time), COUNT(*) FROM gkx.dwd_zh_journal
               WHERE founding_time IS NOT NULL GROUP BY YEAR(founding_time)
               ORDER BY 1""")
res["probes"]["journal_founding"] = [[int(y), int(c)] for y, c in cur.fetchall()]

# 专利年度：面板缓存（全量 100%）
panel = json.load(open(os.path.join(HERE, "_snapshots21", "patent_panel_innov_20261021.json"),
                       encoding="utf-8"))
pat_year = sorted((int(y), int(c)) for y, c in panel["year_all"].items())
res["probes"]["patent_year"] = pat_year
res["probes"]["patent_panel_coverage"] = {
    "rows": panel["rows"], "chunks": panel["chunks"],
    "source": panel["source"], "note": "全量面板，禁止再对 dwd_patent 写 GROUP BY apdt_year"}

cur.execute("SELECT COUNT(*) FROM gkx.dwd_zh_journal WHERE publication_type LIKE '%会议%'")
zh_conf = int(cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM gkx.dwd_en_journal WHERE publication_type LIKE '%onference%'")
en_conf = int(cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM gkx.dwd_zh_paper WHERE publication_type LIKE '%会议%'")
zhp_conf = int(cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM gkx.dwd_en_paper WHERE publication_type LIKE '%onference%'")
enp_conf = int(cur.fetchone()[0])
res["probes"]["conference_rows"] = {"zh_journal": zh_conf, "en_journal": en_conf,
                                    "zh_paper": zhp_conf, "en_paper": enp_conf}


def series(rows, ymin, ymax):
    m = dict(rows)
    ys = [y for y in sorted(m) if ymin <= y <= ymax]
    return ys, [m[y] for y in ys]


# 窗口裁剪（三条硬规则：剔除未完整当年 / 截断段 / 异常尖峰）
PAPER_W = (2016, 2023)
PROJ_W = (2012, 2020)
JOUR_W = (1995, 2015)

py, pv = series(res["probes"]["paper_year"], *PAPER_W)
jy, jv = series(res["probes"]["project_year"], *PROJ_W)
oy, ov = series(res["probes"]["journal_founding"], *JOUR_W)
pat_y = [y for y, _ in pat_year]

res["compute"] = {"series_used": {}, "skipped": {}}

# 基期披露（派单书铁律 5 / DATA_FACTS §3.16）：三源窗口不同，逐源列出，不合并成一个笼统的"基期"。
# 两个列表只表达"实际参与拟合的年份区间"，缺失年一律不补 0——本件做的是外推，
# 若把未覆盖年份按 0 摊进序列，会把"入湖截断"读成"断崖下跌"再外推。
res["base_years_used"] = [PAPER_W[0], PAPER_W[1]]
res["base_years_used_by_source"] = {
    "中文论文年度件数": list(PAPER_W),
    "中文项目年度件数": list(PROJ_W),
    "期刊创办年度件数": list(JOUR_W),
}
res["base_years_missing"] = []
res["base_years_note"] = (
    "论文窗口 2016—2023、项目窗口 2012—2020、期刊创办 1995—2015，三源分别裁剪后才拟合；"
    "窗口外年份不补 0（专利年度件数因 apdt_year 只有 2021—2026、有效期数不足 8 期，已整段不做外推）；"
    "期刊创办序列 2016 起为入湖截断（5/10/4/1/1/1/1/2），故只保留窗口内结果、不纳入正式预测。")

for tag, ys, vs in [("中文论文年度件数", py, pv), ("中文项目年度件数", jy, jv)]:
    if len(vs) < 8:
        res["compute"]["skipped"][tag] = f"有效期数 {len(vs)} < 8，按王惠口径不做外推"
        continue
    hold = fit_best(vs[:-2], h=2)
    test_mape = mape(vs[-2:], hold["forecast"])
    full = fit_best(vs, h=2)
    res["compute"]["series_used"][tag] = {
        "years": ys, "values": vs, "n_periods": len(vs),
        "holdout": {"train_n": len(vs) - 2, "test_years": ys[-2:], "test_actual": vs[-2:],
                    "test_pred": hold["forecast"], "mape_pct": test_mape,
                    "alpha": hold["alpha"], "beta": hold["beta"]},
        "full_fit": full,
        "forecast_years": [ys[-1] + 1, ys[-1] + 2],
    }

if len(ov) >= 8:
    h2 = fit_best(ov[:-2], h=2)
    res["compute"]["skipped"]["期刊创办年度件数"] = {
        "reason": "1995—2015 可拟合，但 2016 后逐年 5/10/4/1/1/1/1/2，属入湖截断而非真实下降；"
                  "对截断序列外推会系统性高估，故不纳入正式预测",
        "window": [oy[0], oy[-1]], "values_tail": ov[-8:],
        "holdout_mape_pct": mape(ov[-2:], h2["forecast"]),
    }

res["compute"]["skipped"]["专利年度件数"] = {
    "reason": f"gkx.dwd_patent.apdt_year 仅 {len(pat_y)} 个年度（{pat_y[0]}—{pat_y[-1]}），"
              "未满 8 期，且 2025/2026 未采完，无法按王惠口径做 Holt 外推",
    "years": pat_y, "values": [c for _, c in pat_year],
}
res["compute"]["skipped"]["会议年度件数"] = {
    "reason": "全库无会议类出版物（四张表的 publication_type 均无会议枚举），期数为 0",
    "detail": res["probes"]["conference_rows"],
}
res["compute"]["skipped"]["英文项目年度件数"] = {
    "reason": f"dwd_en_project.approval_year 全空（{res['probes']['en_project_null_year']['nulls']}"
              f"/{res['probes']['en_project_null_year']['n']}），无法按年聚合",
}

# ---------------------------------------------------------------- 定档
res["dimension_status"] = {
    "会议序列": {"periods": 0, "status": "不可用（无会议类实体）"},
    "中文项目序列": {"periods": len(jv), "window": list(PROJ_W), "status": "可用"},
    "专利序列": {"periods": len(pat_y), "status": "不可用（仅 6 期，<8，且末两年未采完）"},
    "中文论文序列": {"periods": len(pv), "window": list(PAPER_W), "status": "可用"},
    "期刊创办序列": {"periods": len(ov), "status": "不可用（2016 后入湖截断）"},
}
ok = list(res["compute"]["series_used"])
res["support_judgment"] = "部分支持"
res["judgment_reason"] = (
    "王惠口径要求对会议 / 项目 / 专利 / 期刊四类要素年度件数做短期外推，gkx 实际可建"
    f" ≥8 期且未截断的序列只有 {len(ok)} 条（中文论文、中文项目）；会议类实体 0 条、"
    "专利仅 6 期、期刊创办数 2016 年后入湖截断、英文项目无年份。"
    "Holt 可跑通并给出点预测与 80% 区间，但覆盖不到四类要素，故判部分支持。"
)
res["computable_subset"] = {
    "series_available": ok,
    "method": "Holt 线性趋势（α/β 网格寻优），年预 2 期，区间 ±1.28σ√h"}
res["thresholds"] = {"min_periods": 8, "horizon": 2, "interval": "80%",
                     "non_negative": True}

cur.close()
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1, default=str)

print("conference:", json.dumps(res["probes"]["conference_rows"], ensure_ascii=False))
print("paper series:", py, pv)
print("project series:", jy, jv)
print(json.dumps(res["compute"]["series_used"], ensure_ascii=False, default=str)[:2200])
print("skipped:", json.dumps(res["compute"]["skipped"], ensure_ascii=False, default=str)[:900])
print("->", OUT)
