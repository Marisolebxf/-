#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_017 指标同比变化率 — 三源探针 + 久新年度面实算同比 + UI 公式/mock 复现 + 判档产物
UI 挂载（三点）：
  ① graphInteractionState.js:210-250 getGraphMetricComparisonMode——同比/较前周期模式判定器：
    单年（start==end）→ label=同比，displayLabel=同比{start-1}；
    区间 → 较{对照区间}；公式 '(当前周期值 - 对照周期值) / 对照周期值'（:228）；默认框 2020-2026
  ② InnovationEcosystemNewPage.jsx:138 quarterlyOption legend ['季度新增','同比'] + :164 quarterlyYoy 折线（y 轴 %）
  ③ 同页 yearlyOption :204 yoy 年度同比线；:297 talentStats trend yoy；:452/:636 表格 yoy 列
mock：mockData.js carrierTrend——yearlyNew [26,31,35,39,46]（2021-2025）/ yoy [null,.192,.129,.114,.179]（自洽）；
     quarterlyNew/quarterlyYoy 2024Q1-2026Q2（季度同比，首年 4 个 null 无对照）；
     regionStats 14 区县 yoy。对象=孵化载体（孵化器/加速器/众创空间/新型研发机构）。
三源：载体面词族（carrier/incubat/载体/孵化）——jiuxin/gkx/dev；同比原料=年度双期值——
     久新 ads_geo_yearly_metrics 城市×年度（2000-2026）真数据可实算同比。
判档：部分支持——同比公式平凡且年度双期原料久新真承载（深圳论文 2025 同比实测可算）；
     但 UI 具体对象（孵化载体）三源无面、季度粒度久新无（statistics_year 年级）。
"""
import json, os, time
import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(BASE, "_snapshots", "_probe_s306_l1_out.json")
OUT = os.path.join(BASE, "M_SCIUI_KGANALY_017_out.json")
snap = json.load(open(SNAP))
facts = {}

facts["ui_mount"] = ("graphInteractionState.js:210-250 getGraphMetricComparisonMode（:234 同比 label 分支）——"
                     "模式判定器：单年→同比{N-1}；区间→较{对照区间}；:228 公式文本 '(当前-对照)/对照'；"
                     "InnovationEcosystemNewPage.jsx:138 legend ['季度新增','同比']、:164 quarterlyYoy 折线（%轴）、"
                     ":204 年度 yoy 线、:297 人才趋势 yoy、:452/:636 表格 yoy 列")
facts["ui_mock_trend"] = {
    "years": ["2021", "2022", "2023", "2024", "2025"],
    "yearlyNew": [26, 31, 35, 39, 46],
    "yoy": [None, 0.192, 0.129, 0.114, 0.179],
    "quarters": ["2024Q1", "2024Q2", "2024Q3", "2024Q4", "2025Q1", "2025Q2", "2025Q3", "2025Q4", "2026Q1", "2026Q2"],
    "quarterlyNew": [8, 10, 9, 12, 9, 12, 10, 13, 11, 14],
    "quarterlyYoy": [None, None, None, None, 0.125, 0.2, 0.111, 0.083, 0.222, 0.167],
    "note": "对象=孵化载体（mockData.js 孵化器/加速器/众创空间/新型研发机构 28 家样本 + carrierTrend 趋势）",
}

# ---------- mock 自洽校验（yoy vs yearlyNew / quarterlyYoy vs quarterlyNew） ----------
yn = facts["ui_mock_trend"]["yearlyNew"]
yoy_calc = [None] + [round((yn[i] - yn[i - 1]) / yn[i - 1], 3) for i in range(1, len(yn))]
qn = facts["ui_mock_trend"]["quarterlyNew"]
qoy_calc = [None] * 4 + [round((qn[i] - qn[i - 4]) / qn[i - 4], 3) for i in range(4, len(qn))]
mock_selfcheck = {
    "yearly_yoy_recalc": yoy_calc,
    "yearly_match": yoy_calc == facts["ui_mock_trend"]["yoy"],
    "quarterly_yoy_recalc": qoy_calc,
    "quarterly_match": qoy_calc == facts["ui_mock_trend"]["quarterlyYoy"],
    "note": "mock 内部自洽：年同比=连年环比链（31/26-1=0.192…全对）；季同比=同季上年对照（9/8-1=0.125…全对）",
}

# ---------- UI 模式判定器复现（graphInteractionState 移植） ----------
def comparison_mode(time_range):
    try:
        s, e = int(time_range.get("startYear")), int(time_range.get("endYear"))
        has = s is not None and e is not None
    except (TypeError, ValueError):
        has = False
    s = min(s, e) if has else 2020
    e = max(s, e) if has else 2026
    cur = str(e) if s == e else f"{s}-{e}"
    plen = max(1, e - s + 1)
    ce = s - 1
    cs = ce - plen + 1
    comp = str(ce) if cs == ce else f"{cs}-{ce}"
    if time_range.get("startYear") is not None and str(time_range["startYear"]) == str(time_range["endYear"]):
        return {"label": "同比", "displayLabel": f"同比{comp}", "current": cur, "comparison": comp}
    return {"label": "较前周期", "displayLabel": f"较{comp}", "current": cur, "comparison": comp}

facts["ui_mode_repro"] = {
    "single_2026": comparison_mode({"startYear": 2026, "endYear": 2026}),
    "range_2024_2026": comparison_mode({"startYear": 2024, "endYear": 2026}),
    "formula": "(当前周期值 - 对照周期值) / 对照周期值",
    "note": "getGraphMetricComparisonMode 移植：单年→同比{上年}；区间→较{上年区间}；默认框 2020-2026",
}

# ---------- ① dev 载体面词族 ----------
facts["dev_carrier_word_note"] = "dev 542 表词族（carrier/incubat/载体/孵化）无孵化载体面（族级快照+dev 图表面 26 张全 0 行在案）"

# ---------- ② gkx：项目年度分布（同比原料弱承载） ----------
import sys  # noqa: E402
sys.path.insert(0, BASE)
from _gkxdb import gkx  # noqa: E402
gc = gkx()
try:
    gc.execute("SELECT table_name, column_name FROM information_schema.columns WHERE table_schema='gkx' "
               "AND column_name LIKE '%year%' AND table_name LIKE 'dwd%' LIMIT 15")
    facts["gkx_dwd_year_cols"] = [f"{r[0]}.{r[1]}" for r in gc.fetchall()]
except Exception as e:  # noqa: BLE001
    facts["gkx_dwd_year_cols"] = f"ERR {e}"
gc.close()

# ---------- ③ 久新：载体词族 + 年度面同比实算 ----------
def jx_connect(tries=4):
    last = None
    for _ in range(tries):
        try:
            return pymysql.connect(host="47.93.119.170", port=29030, user="test2",
                                           password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
                                           database="gkx_technology_analysis_dev", charset="utf8mb4",
                                           connect_timeout=15, read_timeout=300)
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(15)
    raise last

jx = jx_connect()
jc = jx.cursor()
jc.execute("SHOW TABLES")
jx_tables = sorted(r[0] for r in jc.fetchall())
facts["jiuxin_table_count_live"] = len(jx_tables)
carrier_words = ("incubat", "carrier", "venture", "park")
facts["jiuxin_carrier_word_tables"] = sorted(
    t for t in jx_tables if any(w in t.lower() for w in carrier_words))
# 年度粒度核验：geo_yearly_metrics 是否有季度列
jc.execute("SHOW COLUMNS FROM ads_geo_yearly_metrics")
facts["jiuxin_geo_yearly_time_cols"] = [r[0] for r in jc.fetchall() if "year" in r[0].lower() or "quarter" in r[0].lower() or "month" in r[0].lower()]
# 深圳城市年度同比实算（对象=论文/项目——图度量年度真承载；2026 不完全年披露）
jc.execute("""SELECT m.statistics_year, m.paper_count, m.project_count, m.talent_count, m.institution_count
              FROM ads_geo_yearly_metrics m JOIN ads_location l ON m.location_id=l.location_id
              WHERE l.name_zh='深圳' AND l.location_level='CITY' AND m.statistics_year BETWEEN 2020 AND 2025
              ORDER BY m.statistics_year""")
sz_rows = c_rows = jc.fetchall()
facts["shenzhen_yearly_metrics"] = [list(map(int, r)) for r in sz_rows]
jx.close()

def yoy_series(vals):
    return [None] + [round((vals[i] - vals[i - 1]) / vals[i - 1] * 100, 2) for i in range(1, len(vals))]

years = [r[0] for r in sz_rows]
derived_yoy = {}
for idx, nm in ((1, "paper"), (2, "project"), (3, "talent"), (4, "institution")):
    vals = [int(r[idx]) for r in sz_rows]
    derived_yoy[nm] = yoy_series(vals)
facts["derived_yoy_shenzhen_pct"] = {"years": years, **derived_yoy,
                                     "note": "久新真数据同比（深圳 CITY 2020-2025，公式同 UI：(当-对)/对×100%）；"
                                             "论文 2025 同比 +41.53%、项目 2025 同比 -32.35%（年度波动真实存在）；"
                                             "2026 为不完全年不入算"}

derived = [
    {"name": "mock 自洽校验", "value": mock_selfcheck, "basis": "年同比链/季同比全对——mock 内部公式一致"},
    {"name": "深圳论文同比（久真实算）", "value": derived_yoy["paper"],
     "basis": f"{years} 逐年：5,671→7,395→10,005→12,243→17,596→24,904"},
    {"name": "深圳项目同比（久真实算）", "value": derived_yoy["project"],
     "basis": "同框项目计数同比——负增长年真实存在（2025 -32.35%）"},
]

absence_probe = [
    {"what": "孵化载体面（孵化器/加速器/众创空间/新型研发机构登记）",
     "how": "jiuxin 218 表词族（incubat/carrier/venture/park）+ dev 542 词族 + gkx 280 词族",
     "hits": "0——UI 28 家载体清单为 mock 写死；三源无载体登记面"},
    {"what": "季度粒度指标面（quarterlyYoy 需要 2024Q1-2026Q2 季度值）",
     "how": "久新 ads_geo_yearly_metrics 时间列 SHOW COLUMNS",
     "hits": "仅 statistics_year（年级）——无 quarter/month 列，季度同比无原料"},
    {"what": "dev/gkx 年度同比现成结果面",
     "how": "dev 图表面 26 张全 0 行（族级快照）；gkx 词族（yoy/comparison）+ dwd year 列实查",
     "hits": "0 现成同比面；gkx dwd 层有年度列（dwd_en_project.approval_year/dwd_global_policy_base.year 等 15 列）——可作弱原料 GROUP BY 出年度分布算同比"},
]

support = "部分支持"
out = {"metric_id": "M_SCIUI_KGANALY_017", "metric_name": "指标同比变化率（科技图谱·图交互状态/创新生态·增量趋势）",
       "facts": facts, "derived": derived, "absence_probe": absence_probe, "support_judgment": support,
       "support_rationale": ("同比公式平凡且双期原料久新真承载：城市年度四指标（2000-2026）同比已实算"
                             "（深圳论文 2025 同比 +41.53%）；模式判定器（单年同比/区间较前周期）任意年度面可套用。"
                             "缺口：UI 具体对象=孵化载体（三源无面）+季度粒度（久新仅年级）——"
                             "载体季度同比不可算，年度图度量同比可算"),
       "base_years_used": [2020, 2021, 2022, 2023, 2024, 2025],
       "base_years_missing": [2026],
       "base_years_note": "久新 geo_yearly_metrics 覆盖 2000-2026；2026 为不完全年（截至批处理快照）不入同比算；"
                          "UI mock 基期 2021-2025 年+2024Q1-2026Q2 季"}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done ->", OUT, "| support:", support,
      "| mock yearly match:", mock_selfcheck["yearly_match"],
      "| SZ paper yoy 2025:", derived_yoy["paper"][-1])
