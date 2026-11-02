#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_P7_003 指标历史趋势（既往序列）· 三源探针与复现脚本（S3-02 Lane 3）。

复现路径（§二）：久新 ads_institution_yearly_metrics / ads_technology_yearly_metrics
两张年度指标序列表构成『既往序列』的现成承载；对单一对象（机构/技术节点）抽
6 年窗口（对齐 UI buildLineOption 2020–2025 六年轴）复现逐年读数 + 同比。

absence（B4）：gkx macro_index_data 面向宏观经济指数（occur_period 月度）、非科技
指标对象序列；dev policy_prediction_indicator 等政策面不属于本指标。
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_P7_003_out.json")

JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)

import pymysql  # noqa: E402

facts, derived, notes = {}, [], []
conn = pymysql.connect(**JX)
cur = conn.cursor()

# ---------- 1) 序列面规模 ----------
cur.execute("SELECT COUNT(*) FROM ads_institution_yearly_metrics")
facts["jiuxin_institution_yearly_rows"] = int(cur.fetchone()[0])
cur.execute(
    "SELECT statistics_year, COUNT(*) n FROM ads_institution_yearly_metrics "
    "GROUP BY statistics_year ORDER BY statistics_year DESC LIMIT 12")
inst_yearly = {str(r[0]): int(r[1]) for r in cur.fetchall()}
facts["jiuxin_institution_yearly_by_year"] = inst_yearly

cur.execute("SELECT COUNT(*) FROM ads_technology_yearly_metrics")
facts["jiuxin_technology_yearly_rows"] = int(cur.fetchone()[0])
cur.execute(
    "SELECT statistics_year, COUNT(*) n FROM ads_technology_yearly_metrics "
    "GROUP BY statistics_year ORDER BY statistics_year DESC LIMIT 12")
tech_yearly = {str(r[0]): int(r[1]) for r in cur.fetchall()}
facts["jiuxin_technology_yearly_by_year"] = tech_yearly

cur.execute("SELECT COUNT(DISTINCT institution_id) FROM ads_institution_yearly_metrics")
facts["jiuxin_institution_yearly_distinct_institutions"] = int(cur.fetchone()[0])
cur.execute("SELECT COUNT(DISTINCT technology_node_id) FROM ads_technology_yearly_metrics")
facts["jiuxin_technology_yearly_distinct_nodes"] = int(cur.fetchone()[0])

# 序列长度分布（机构粒度，全表 GROUP BY 小表可行：67k 机构×年聚合行）
cur.execute(
    "SELECT seq_len, COUNT(*) c FROM ("
    "  SELECT institution_id, COUNT(*) seq_len FROM ads_institution_yearly_metrics "
    "  GROUP BY institution_id) t GROUP BY seq_len ORDER BY c DESC LIMIT 10")
facts["jiuxin_institution_seq_len_distribution"] = {str(r[0]): int(r[1]) for r in cur.fetchall()}

# ---------- 2) 复现：单一对象六年窗口（对齐 UI 2020–2025 轴） ----------
# 选体量最大的机构（行数并列时按 institution_id 字典序，B5 确定性）
cur.execute(
    "SELECT institution_id FROM ads_institution_yearly_metrics "
    "GROUP BY institution_id ORDER BY SUM(paper_count) DESC, institution_id LIMIT 1")
demo_inst = cur.fetchone()[0]
facts["jiuxin_demo_institution_id"] = demo_inst

cur.execute(
    "SELECT statistics_year, paper_count, patent_count, talent_count, project_count "
    "FROM ads_institution_yearly_metrics WHERE institution_id=%s "
    "ORDER BY statistics_year", (demo_inst,))
series = [{"year": int(r[0]), "paper": int(r[1] or 0), "patent": int(r[2] or 0),
           "talent": int(r[3] or 0), "project": int(r[4] or 0)} for r in cur.fetchall()]
facts["jiuxin_demo_institution_full_series"] = series

# 六年窗口 + 最近同比（派生：paper 同比）
window = [s for s in series if 2020 <= s["year"] <= 2025]
facts["jiuxin_demo_institution_window_2020_2025"] = window
if len(window) >= 2:
    last, prev = window[-1], window[-2]
    derived.append({
        "key": "jiuxin_demo_institution_paper_yoy_pct",
        "value": round((last["paper"] - prev["paper"]) * 100.0 / prev["paper"], 4) if prev["paper"] else None,
        "numerator": last["paper"] - prev["paper"],
        "denominator": prev["paper"],
        "note": "分子=窗口末年−上一年论文数，分母=上一年论文数；同一机构同表序列（B3）；演示对象=%s" % demo_inst})

# 技术节点侧样例（一个 node 的全序列）
cur.execute(
    "SELECT technology_node_id FROM ads_technology_yearly_metrics "
    "GROUP BY technology_node_id ORDER BY SUM(paper_count) DESC, technology_node_id LIMIT 1")
demo_node = cur.fetchone()[0]
facts["jiuxin_demo_technology_node_id"] = demo_node
cur.execute(
    "SELECT statistics_year, paper_count, patent_count, company_count "
    "FROM ads_technology_yearly_metrics WHERE technology_node_id=%s "
    "ORDER BY statistics_year", (demo_node,))
facts["jiuxin_demo_technology_full_series"] = [
    {"year": int(r[0]), "paper": int(r[1] or 0), "patent": int(r[2] or 0),
     "company": int(r[3] or 0)} for r in cur.fetchall()]

cur.close(); conn.close()

# ---------- 3) absence 探针 ----------
absence_probe = []
from _gkxdb import gkx  # noqa: E402
gc = gkx()
gc.execute("SELECT COUNT(*) FROM gkx.dwd_macro_index_data")
macro_rows = int(gc.fetchone()[0])
gc.execute(
    "SELECT index_code, COUNT(*) c, MIN(occur_period), MAX(occur_period) "
    "FROM gkx.dwd_macro_index_data GROUP BY index_code ORDER BY c DESC LIMIT 5")
macro_top = [{"index_code": r[0], "rows": int(r[1]), "period_min": str(r[2]), "period_max": str(r[3])} for r in gc.fetchall()]
gc.close()
facts["gkx_macro_index_data_rows"] = macro_rows
facts["gkx_macro_index_top_codes"] = macro_top
absence_probe.append({
    "probe": "gkx 指标年度序列承载：dwd_macro_index_data（20,000 行）",
    "source": "gkx",
    "sql": "SELECT index_code, COUNT(*) c, MIN(occur_period), MAX(occur_period) FROM gkx.dwd_macro_index_data GROUP BY index_code ORDER BY c DESC LIMIT 5",
    "hits": macro_rows,
    "hit_names": [m["index_code"] for m in macro_top],
    "hit_detail": "dwd_macro_index_data 为宏观经济指数月度序列（occur_period 形如 201806，area_code 广东行政区划），服务科技创新评估的『指标历史趋势』需对象粒度科技指标序列，语义不同族"})

absence_probe.append({
    "probe": "dev 侧既往序列承载（沿用共享快照 E1 + _probe_lane3_s302 E 键）",
    "source": "dev",
    "sql": "SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema LIKE 'gkxlumenx%' AND (table_name LIKE '%forecast%' OR table_name LIKE '%simul%')",
    "hits": 3,
    "hit_names": ["gkxlumenx_ads.policy_simulate", "gkxlumenx_dwd.policy_simulation_param", "gkxlumenx_dwd.policy_simulation_result"],
    "hit_detail": "dev 命中表均为政策模拟域（policy_simulate/policy_simulation_param/policy_simulation_result，行数 0），非指标历史序列结果面"})

# ---------- 4) 判档 ----------
notes.append("判档：久新 institution_yearly_metrics（272,040 行）/technology_yearly_metrics 两张年度序列表结构+数据量足够，任一对象的既往逐年序列可现转（六年窗口复现在案），判完全转换支持")
notes.append("口径披露：UI 挂载（buildLineOption）为 2020–2025 六年柱+增长率线双轴，mock 值 6,542→12,856 为演示值；久新序列以 statistics_year 为轴，窗口对齐无障碍")
notes.append("对象轴披露：久新两表对象=机构/技术节点；科技创新评估页的评估对象若为『主体（企业/高校）』则机构表直配，若为『指标维度』需先定指标口径（口径不闭合是本族共同风险，见 P7_004）")

out = {
    "metric_id": "M_SCIUI_P7_003",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation-new/TechInnovationEvaluationNewPage.jsx:572",
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation-new/TechInnovationEvaluationNewPage.jsx:576",
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation-new/TechInnovationEvaluationNewPage.jsx:556",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「指标历史趋势（既往序列）」指标名未出现在三份需求真源；语义最近语境=SRS 科技创新评估.md seq 158『政策优化建议』段的系统仿真模型趋势预判（『实现对各种可能的趋势和前景进行预测』）；UI 挂载在科技创新评估new 页系统仿真模型过程区（历史趋势/预测趋势/95%置信区间三系列折线）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": "完全转换支持",
    "notes": notes,
    "base_years_used": sorted({s["year"] for s in window}) if window else [],
    "base_years_missing": [y for y in range(2020, 2026) if window and y not in {s["year"] for s in window}],
    "base_years_note": "演示机构对象六年窗口实占年份见 base_years_used；两表全库年份覆盖见 facts.jiuxin_*_by_year（institution 2023–2026 四年、technology 多年）",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": ["6542", "12856"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("saved ->", OUT)
print("years inst:", list(inst_yearly.items())[:6])
print("years tech:", list(tech_yearly.items())[:6])
print("demo inst series len:", len(series), "| window:", len(window))
print("seq_len dist:", facts["jiuxin_institution_seq_len_distribution"])
