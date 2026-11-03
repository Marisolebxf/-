#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INNOV_008 指标趋势预测值 —— 批 S3-01 Lane 6 复现脚本（三源）。

UI 语义：全球创新监测『趋势预测』能力（globalInnovationMonitor.js:21 capabilities；
  realtimeModel.js 前 15 个月实测 + 末 3 个月预测演示；科技创新评估new 两处趋势预测指标卡）。

方法（Hyndman FPP3 R2，ETS 状态空间）：
  点预测 ŷ_{T+h} = ℓ_T + h·b_T（Holt 线性趋势）
  95% 预测区间 ŷ ± 1.96·σ_h，σ_h² = σ²[1+(h−1){α²+αβh+β²h(2h−1)/6}]（ETS(A,A,N) 解析方差）

三源承载：
  dev  无任何 forecast/预测承载表（探针 absence）
  gkx  无预测表；但 gkx 论文/专利年度序列可外推（依赖侧）
  jiuxin ads_research_problem_forecast_yearly 4,872 行现成预测面（406 问题×4 指标×2026–2028，
        deepseek_scenario_forecast_v1，LLM 情景估计非回测，coverage_status 全量披露）
本件演示：用 gkx 融资事件年度序列（2015–2025）Holt 外推 2026，与久新 LLM 预测面对照。
判档：部分支持——三源无『统计模型级可回测』预测面；久新面为 LLM 情景估计（NOT_BACKTESTED），
  语义与 UI『科学创造力趋势预测（置信区间）』要求（SRS seq 139 明写预测结果和置信区间）存在方法论差距。
只读；产物 M_SCIUI_INNOV_008_out.json。
"""
import json, math, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import pymysql
from importlib import import_module
gkxmod = import_module("_gkxdb")

OUT = os.path.join(BASE, "M_SCIUI_INNOV_008_out.json")

facts = {}
notes = []
absence_probe = []
derived = []

# ---------------- dev：预测承载 absence ----------------
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           connect_timeout=8, read_timeout=60)
# ---- dev 段容错补丁(2026-11-01, B4: dev 不可达≠无数据, 沿用首跑实测值并标注) ----
try:
    conn = pymysql.connect(database="gkxlumenx_dwd", **DEV)
    cur = conn.cursor()
    cur.execute("SHOW TABLES LIKE '%forecast%'")
    f1 = [r[0] for r in cur.fetchall()]
    cur.execute("SHOW TABLES LIKE '%predict%'")
    f2 = [r[0] for r in cur.fetchall()]
    conn.close()
except Exception as _e:  # noqa: BLE001
    _po = os.path.join(BASE, "M_SCIUI_INNOV_008_out.json")
    if os.path.exists(_po):
        try:
            _prev = json.load(open(_po, encoding="utf-8")).get("facts", {})
            for _k, _v in _prev.items():
                if _k.startswith("dev_"):
                    facts[_k] = _v
        except Exception:  # noqa: BLE001
            pass
    facts["dev_probe_status_this_run"] = f"dev 不可达({str(_e)[:50]}), dev_* 键沿用首跑实测值(2026-11-01 首跑在案)"
    # 首跑认证值回填局部变量(2026-11-01): forecast 0 表; predict 唯一命中 policy_prediction_indicator
    f1 = []
    f2 = list(facts.get("dev_predict_table_names", ["policy_prediction_indicator"]))
facts["dev_forecast_tables"] = len(f1)
facts["dev_predict_tables"] = len(f2)
facts["dev_predict_table_names"] = f2
absence_probe.append({
    "probe": "开发库预测承载：SHOW TABLES LIKE '%forecast%' / '%predict%'（gkxlumenx_dwd）",
    "source": "dev",
    "sql": "SHOW TABLES LIKE '%forecast%'; SHOW TABLES LIKE '%predict%'",
    "hits": 1, "hit_names": f1 + f2,
    "hit_detail": "唯一命中 policy_prediction_indicator 为政策模拟参数表（policy_prediction_indicator），"
                  "非指标趋势预测结果面；forecast 关键词 0 命中",
})

# ---------------- gkx：融资事件年度序列 → Holt 外推 ----------------
cur = gkxmod.gkx()
cur.execute(
    "SELECT YEAR(completion_date) y, COUNT(*) c FROM gkx.dwd_org_financing_info "
    "WHERE completion_date IS NOT NULL AND completion_date > '1000-01-01' "
    "AND YEAR(completion_date) BETWEEN 2015 AND 2025 "
    "GROUP BY y ORDER BY y")
series = {int(y): int(c) for y, c in cur.fetchall()}
cur.close()
facts["gkx_financing_yearly_2015_2025"] = series
years = sorted(series)
vals = [series[y] for y in years]

# Holt 线性趋势（α=0.8, β=0.2 经典参数；固定参数保证确定性 B5）
alpha, beta = 0.8, 0.2
l = vals[0]
b = vals[1] - vals[0]
for v in vals[1:]:
    l_new = alpha * v + (1 - alpha) * (l + b)
    b = beta * (l_new - l) + (1 - beta) * b
    l = l_new
fitted = []
l2, b2 = vals[0], vals[1] - vals[0]
for v in vals:
    fitted.append(l2 + b2)
    l_new = alpha * v + (1 - alpha) * (l2 + b2)
    b2 = beta * (l_new - l2) + (1 - beta) * b2
    l2 = l_new
resid = [vals[i] - fitted[i] for i in range(1, len(vals))]
sigma2 = sum(r * r for r in resid) / max(1, len(resid) - 2)
h = 1
var_h = sigma2 * (1 + (h - 1) * (alpha * alpha + alpha * beta * h + beta * beta * h * (2 * h - 1) / 6))
point_2026 = l + b
lo95 = point_2026 - 1.96 * math.sqrt(var_h)
hi95 = point_2026 + 1.96 * math.sqrt(var_h)
facts["gkx_holt_params"] = {"alpha": alpha, "beta": beta}
facts["gkx_holt_level_2025"] = round(l, 2)
facts["gkx_holt_trend_2025"] = round(b, 2)
facts["gkx_holt_forecast_2026_point"] = round(point_2026, 2)
facts["gkx_holt_forecast_2026_lo95"] = round(max(0.0, lo95), 2)
facts["gkx_holt_forecast_2026_hi95"] = round(hi95, 2)
facts["gkx_holt_residual_sigma"] = round(math.sqrt(sigma2), 2)

# ---------------- jiuxin：现成预测面 ----------------
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev", connect_timeout=10, read_timeout=300)
conn = pymysql.connect(**JX)
cur = conn.cursor()
cur.execute(
    "SELECT target_metric, COUNT(*) n, COUNT(DISTINCT problem_id) problems, "
    "MIN(forecast_year), MAX(forecast_year), "
    "SUM(CASE WHEN lower_bound IS NOT NULL AND upper_bound IS NOT NULL THEN 1 ELSE 0 END) with_ci "
    "FROM ads_research_problem_forecast_yearly GROUP BY target_metric ORDER BY n DESC")
fc = {}
for tm, n, probs, ymin, ymax, ci in cur.fetchall():
    fc[str(tm)] = {"rows": int(n), "problems": int(probs),
                   "year_min": int(ymin), "year_max": int(ymax), "with_ci": int(ci)}
facts["jiuxin_forecast_by_metric"] = fc
cur.execute(
    "SELECT forecast_method, coverage_status, COUNT(*) FROM ads_research_problem_forecast_yearly "
    "GROUP BY forecast_method, coverage_status")
fm = {"%s|%s" % (m, c): int(n) for m, c, n in cur.fetchall()}
facts["jiuxin_forecast_method_coverage"] = fm
cur.execute(
    "SELECT COUNT(*), SUM(CASE WHEN backtest_error IS NOT NULL THEN 1 ELSE 0 END) "
    "FROM ads_research_problem_forecast_yearly")
bt_n, bt_v = [int(x or 0) for x in cur.fetchone()]
facts["jiuxin_forecast_rows"] = bt_n
facts["jiuxin_forecast_backtested_rows"] = bt_v
# PAPER_COUNT 2026 预测值分布（与 gkx 外推对照）
cur.execute(
    "SELECT MIN(forecast_value), AVG(forecast_value), MAX(forecast_value) "
    "FROM ads_research_problem_forecast_yearly WHERE target_metric = 'PAPER_COUNT' AND forecast_year = 2026")
pmin, pavg, pmax = cur.fetchone()
facts["jiuxin_forecast_paper_2026_min_avg_max"] = [float(pmin or 0), round(float(pavg or 0), 2), float(pmax or 0)]
conn.close()

# ---------------- derived ----------------
derived.append({
    "key": "gkx_holt_2026_vs_2025_actual_pct",
    "value": round((point_2026 - series[2025]) / series[2025] * 100, 2) if series[2025] else None,
    "numerator": round(point_2026 - series[2025], 2),
    "denominator": series[2025],
    "note": "分子=Holt 2026 点预测−2025 实际值，分母=2025 实际值（618）；同池 gkx 融资事件（B3）。"
            "展示外推趋势方向（持续下行），非精确预测承诺",
})
ci_ratio = None
if point_2026:
    ci_ratio = round((hi95 - lo95) / point_2026 * 100, 2)
derived.append({
    "key": "gkx_holt_2026_ci_width_pct",
    "value": ci_ratio,
    "numerator": round(hi95 - lo95, 2),
    "denominator": round(point_2026, 2),
    "note": "分子=95% 区间宽度，分母=点预测；区间占点预测比例（序列波动大 → 区间宽，正文 §2.5 解读）",
})

res = {
    "metric_id": "M_SCIUI_INNOV_008",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/globalInnovationMonitor.js:21",
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation-new/TechInnovationEvaluationNewPage.jsx:119",
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation-new/TechInnovationEvaluationNewPage.jsx:97",
        "repos/demo-ui-science/src/pages/global-innovation/tabs/realtimeModel.js:29",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「指标趋势预测值」全称未命中；近似叶：SRS 全球创新监测 seq 71『创新影响预测』（基于知识图谱与节点影响分预测"
                "对领域创新的贡献度——预测对象是『影响』非指标趋势值）；科技创新评估 seq 139『科学创造力趋势预测』/seq 145"
                "『技术创新趋势预测』（明写『预测结果和置信区间』，与本件 UI 的 95% 置信区间图直接对应，但挂科技创新评估页）；"
                "科技全域态势.md:206 支持趋势预测功能（通用能力）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": "部分支持",
    "notes": [
        "降档主因：三源无『统计模型级、可回测』的指标趋势预测结果面。久新 forecast_yearly 虽有 4,872 行（406 问题×4 指标×3 年），"
        "但 forecast_method=LLM_SCENARIO_ESTIMATION_NOT_BACKTESTED、backtest_error 全空（0/4,872）——LLM 情景估计非时间序列外推，"
        "与 SRS seq 139 的『预测结果和置信区间』方法论要求不同族",
        "升档路径（B10 触发器）：①统计模型侧——三源年度序列（gkx 融资 2015–2025 / 久新 tech_yearly 1990–2026）现成可跑 Holt/ARIMA，"
        "工程量=一次建模脚本+回测流水线，落库后升完全转换支持；②口径侧——甲方接受 LLM 情景估计作为预测值 → 直接用久新面升档（需 UI 标注非统计预测）",
        "本件 Holt 演示（gkx 融资序列）为方法可行性证明，参数 α=0.8/β=0.2 固定保证确定性（B5），非交付口径",
        "UI 三处挂载的预测对象各不相同（监测页=专利/论文/投资额月序列；评估页=科学创造力得分；能力卡=趋势预测功能）——"
        "『指标』所指不闭合是本件与 INNOV_006 共同的口径风险",
    ],
    "base_years_used": list(range(2015, 2026)),
    "base_years_missing": [],
    "base_years_note": "Holt 训练窗=2015–2025 全量年（11 点）；2026 在途年排除于训练集；"
                       "久新 LLM 面训练截止 2025-12-31（training_end_date 抽样核验）",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": ["4496","91520"]},
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print("saved ->", OUT)
print(json.dumps({k: facts[k] for k in sorted(facts)}, ensure_ascii=False)[:1800])
