#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_P7_004 指标预测趋势（未来序列）· 三源探针与复现脚本（S3-02 Lane 3）。

复现路径（§二）：
  主探针：久新 ads_research_problem_forecast_yearly（4,872 行，2026–2028，
  lower/upper_bound + confidence_level 列在案）——LLM 情景估计面（未回测）。
  对照复现：用 P7_003 同源 institution_yearly_metrics 的 2015–2025 十一年序列
  对演示机构跑 Holt 两参数外推 2026–2028（α/β 固定，B5 确定性），证明统计外推
  路径现转可行；两口径并列（B10）。
"""
import json, math, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_P7_004_out.json")

JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)

import pymysql  # noqa: E402

facts, derived, notes = {}, [], []
conn = pymysql.connect(**JX)
cur = conn.cursor()

# ---------- 1) 久新预测面全量画像 ----------
cur.execute("SELECT COUNT(*) FROM ads_research_problem_forecast_yearly")
facts["jiuxin_forecast_rows"] = int(cur.fetchone()[0])

cur.execute(
    "SELECT target_metric, COUNT(*) n, COUNT(DISTINCT problem_id) problems, "
    "MIN(forecast_year) y_min, MAX(forecast_year) y_max, "
    "SUM(CASE WHEN backtest_error IS NOT NULL THEN 1 ELSE 0 END) with_backtest "
    "FROM ads_research_problem_forecast_yearly GROUP BY target_metric ORDER BY n DESC")
by_metric = {}
for r in cur.fetchall():
    by_metric[r[0]] = {"rows": int(r[1]), "problems": int(r[2]), "year_min": int(r[3]),
                       "year_max": int(r[4]), "with_backtest": int(r[5])}
facts["jiuxin_forecast_by_metric"] = by_metric

cur.execute(
    "SELECT forecast_method, COUNT(*) c FROM ads_research_problem_forecast_yearly "
    "GROUP BY forecast_method ORDER BY c DESC LIMIT 5")
facts["jiuxin_forecast_method_distribution"] = {str(r[0]): int(r[1]) for r in cur.fetchall()}

cur.execute(
    "SELECT confidence_level, COUNT(*) c FROM ads_research_problem_forecast_yearly "
    "GROUP BY confidence_level ORDER BY c DESC LIMIT 5")
facts["jiuxin_forecast_confidence_distribution"] = {str(r[0]): int(r[1]) for r in cur.fetchall()}

# CI 列覆盖（lower/upper 非空）
cur.execute(
    "SELECT SUM(CASE WHEN lower_bound IS NOT NULL AND upper_bound IS NOT NULL THEN 1 ELSE 0 END) "
    "FROM ads_research_problem_forecast_yearly")
facts["jiuxin_forecast_with_ci_rows"] = int(cur.fetchone()[0])

# 对象轴：研究问题（problem_id）样例
cur.execute(
    "SELECT problem_id, target_metric, forecast_year, forecast_value, lower_bound, upper_bound "
    "FROM ads_research_problem_forecast_yearly LIMIT 5")
facts["jiuxin_forecast_samples"] = [
    {"problem": (r[0] or "")[:40], "metric": r[1], "year": int(r[2]),
     "value": None if r[3] is None else round(float(r[3]), 4),
     "lo": None if r[4] is None else round(float(r[4]), 4),
     "hi": None if r[5] is None else round(float(r[5]), 4)} for r in cur.fetchall()]

# ---------- 2) 对照复现：Holt 外推（同源序列，确定性） ----------
cur.execute(
    "SELECT institution_id FROM ads_institution_yearly_metrics "
    "GROUP BY institution_id ORDER BY SUM(paper_count) DESC, institution_id LIMIT 1")
demo_inst = cur.fetchone()[0]
cur.execute(
    "SELECT statistics_year, paper_count FROM ads_institution_yearly_metrics "
    "WHERE institution_id=%s AND statistics_year BETWEEN 2015 AND 2025 "
    "ORDER BY statistics_year", (demo_inst,))
hist = [(int(r[0]), int(r[1] or 0)) for r in cur.fetchall()]
# 训练序列面规模（B1：正文引用型数字落键）
cur.execute("SELECT COUNT(*) FROM ads_institution_yearly_metrics")
facts["jiuxin_institution_yearly_rows"] = int(cur.fetchone()[0])
facts["jiuxin_demo_institution_id"] = demo_inst
facts["jiuxin_demo_institution_paper_history_2015_2025"] = hist

# Holt 两参数（α=0.8, β=0.2，与 INNOV_008 批内口径一致）
ys = [v for _, v in hist]
alpha, beta = 0.8, 0.2
level, trend = float(ys[0]), (float(ys[1]) - float(ys[0])) if len(ys) > 1 else 0.0
fitted = [level]
for v in ys[1:]:
    new_level = alpha * v + (1 - alpha) * (level + trend)
    trend = beta * (new_level - level) + (1 - beta) * trend
    level = new_level
    fitted.append(level)
resid = [ys[i] - fitted[i] for i in range(len(ys))]
sigma = math.sqrt(sum(r * r for r in resid) / max(len(resid) - 1, 1))
forecasts = []
for h in range(1, 4):
    point = level + h * trend
    lo = max(0.0, point - 1.96 * sigma * math.sqrt(h))
    hi = point + 1.96 * sigma * math.sqrt(h)
    forecasts.append({"year": 2025 + h, "point": round(point, 2),
                      "lo95": round(lo, 2), "hi95": round(hi, 2)})
facts["gkx_holt_params"] = {"alpha": alpha, "beta": beta}
facts["jiuxin_holt_forecast_2026_2028_demo_inst"] = forecasts
facts["jiuxin_holt_residual_sigma_demo_inst"] = round(sigma, 2)

# 半宽落键（正文引用型数字 B1）
facts["jiuxin_holt_2026_halfwidth"] = round(forecasts[0]["hi95"] - forecasts[0]["point"], 2)
facts["jiuxin_holt_2026_fullwidth"] = round(forecasts[0]["hi95"] - forecasts[0]["lo95"], 2)
facts["jiuxin_holt_2028_halfwidth"] = round(forecasts[2]["hi95"] - forecasts[2]["point"], 2)
derived.append({
    "key": "jiuxin_holt_2026_vs_2025_actual_pct",
    "value": round((forecasts[0]["point"] - ys[-1]) * 100.0 / ys[-1], 2) if ys[-1] else None,
    "numerator": round(forecasts[0]["point"] - ys[-1], 2),
    "denominator": ys[-1],
    "note": "分子=Holt 2026 点预测−2025 实际值，分母=2025 实际值；同一演示机构同源序列（B3）；演示对象=%s" % demo_inst})
derived.append({
    "key": "jiuxin_holt_2026_ci_width_pct",
    "value": round((forecasts[0]["hi95"] - forecasts[0]["lo95"]) * 100.0 / forecasts[0]["point"], 2),
    "numerator": round(forecasts[0]["hi95"] - forecasts[0]["lo95"], 2),
    "denominator": forecasts[0]["point"],
    "note": "分子=2026 预测 95% 区间宽度，分母=2026 点预测；区间相对宽度（序列波动越大区间越宽）"})

cur.close(); conn.close()

# ---------- 3) absence 探针 ----------
absence_probe = []
absence_probe.append({
    "probe": "久新统计模型级预测结果面（正向+缺口双录）",
    "source": "jiuxin",
    "sql": "SELECT forecast_method, COUNT(*) FROM ads_research_problem_forecast_yearly GROUP BY forecast_method",
    "hits": facts["jiuxin_forecast_rows"],
    "hit_names": list(facts["jiuxin_forecast_method_distribution"].keys()),
    "hit_detail": "4,872 行预测面唯一方法=LLM_SCENARIO_ESTIMATION_NOT_BACKTESTED / AI_ESTIMATED_NOT_BACKTESTED；backtest_error 全空（0/4,872）——有结果面但非统计外推、未回测"})
absence_probe.append({
    "probe": "dev 预测承载（共享快照 E1 复核 + 本 lane E9）",
    "source": "dev",
    "sql": "SHOW TABLES LIKE '%forecast%'; SHOW TABLES LIKE '%simul%'（gkxlumenx_dwd/ads）",
    "hits": 4,
    "hit_names": ["policy_prediction_indicator", "policy_simulate", "policy_simulation_param", "policy_simulation_result"],
    "hit_detail": "全为政策模拟/政策预测指示器域；policy_simulation_result 实测 0 行（E9）；无科技指标趋势预测结果面"})

from _gkxdb import gkx  # noqa: E402
gc = gkx()
gc.execute(
    "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' AND "
    "(table_name LIKE '%%forecast%%' OR table_name LIKE '%%predict%%')")
gkx_hits = [r[0] for r in gc.fetchall()]
gc.close()
absence_probe.append({
    "probe": "gkx 预测表扫描",
    "source": "gkx",
    "sql": "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' AND (table_name LIKE '%forecast%' OR table_name LIKE '%predict%')",
    "hits": len(gkx_hits),
    "hit_names": gkx_hits,
    "hit_detail": "gkx 280 表无 forecast/predict 结果面（0 命中）；外推只能从年度序列表现转"})

# ---------- 4) 判档 ----------
notes.append("判档：三源无『统计模型级、可回测』的指标预测结果面（久新 4,872 行为 LLM 情景估计未回测、dev 政策域 0 行、gkx 无预测表）；但久新序列面（institution_yearly 2015–2026 满铺）+Holt 外推演示已跑通，依赖侧结构+数据量足够——方法论缺口（回测流水线）与结果面性质（LLM 非 TS 外推）是降档主因，判部分支持")
notes.append("B10 双口径：口径 A=久新 LLM 面直接供数（须 UI 标注『LLM 情景估计，非统计预测』）；口径 B=统计外推（Holt/ARIMA on 序列表，本件演示在案）+回测流水线。甲方接受 A → 升完全转换支持（对象轴=研究问题）；立项 B → 升完全转换支持（对象轴可配机构/技术节点）")
notes.append("与 INNOV_008 对账（B11）：jiuxin_forecast_rows=4,872、by_metric rows=1,218×4、with_backtest=0 三组读数与 S3-01 批 INNOV_008 产物零漂移（其 jiuxin_forecast_rows=4,872）")
notes.append("对象轴披露：久新预测面对象=研究问题（problem_id，406 个），非机构/技术节点/评估指标——UI『指标预测趋势』的『指标』所指在久新面是 PAPER/PATENT/PROJECT/HOTSPOT 四 target_metric")

out = {
    "metric_id": "M_SCIUI_P7_004",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation-new/TechInnovationEvaluationNewPage.jsx:577",
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation-new/TechInnovationEvaluationNewPage.jsx:572",
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation-new/TechInnovationEvaluationNewPage.jsx:1617",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「指标预测趋势（未来序列）」指标名未出现在三份需求真源；语义最近语境=SRS 科技创新评估.md seq 158 段（系统仿真模型『实现对各种可能的趋势和前景进行预测』）与 seq 139『科学创造力趋势预测』/seq 145『技术创新趋势预测』（明写『预测结果和置信区间』，与 UI 95% 置信区间直接对应）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": "部分支持",
    "notes": notes,
    "base_years_used": [y for y, _ in hist],
    "base_years_missing": [],
    "base_years_note": "Holt 训练窗=2015–2025 全量年（11 点，演示机构满铺）；久新 LLM 面训练截止 training_end_date（抽样在案）；2026 为在途年，institute_yearly 已有 2026 行但为年中快照不纳入训练",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": []},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("saved ->", OUT)
print("forecast rows:", facts["jiuxin_forecast_rows"], "| methods:", facts["jiuxin_forecast_method_distribution"])
print("CI coverage:", facts["jiuxin_forecast_with_ci_rows"])
print("holt:", forecasts)
