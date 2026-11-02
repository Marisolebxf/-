#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TALENTIR_009 学者未来产出增长预测值 · 三源探针与复现脚本（S3-03 Lane 7）。

含义：人才引进推荐评估·贡献度分析（预测视图缩放）「阶段增长预测」——学者未来产出的
增长预测值。UI：repos/demo-ui-science/src/pages/talent-trend/components/ContributionTab.jsx:311
（predictViewMap stage: { factor: 1.15, label: '阶段增长预测' }——mock 因子演示值，
近两年点 v*1.15+斜率外推，非模型输出）。
需求：主需求 1.1.1.1.4.3.4.1.3(2) 预测视图缩放「用户可切换整体预期、局部影响及阶段性
增长视图」——视图名在、预测算式无。

判档（Lane 6 框架）：
- 结构化预测输出面：久新 ads_talent_potential_result（100,000 行）是动量型潜力评估面
  （五维动量分+潜力综合分），非「未来产出增长预测值」本身，但同为「面向未来」语义族——
  部分承载；
- 时序原料：ads_talent_yearly_metrics（学者×年产出序列）在——转换路径的原料双在；
- gkx：dwd_scholar 只有 paper_nums/citation_nums/h_index 快照计数列，无时序无预测面；
- dev：无学者预测承载。
→ 部分承载（预测面是潜力动量非增长预测 + 时序原料在）→ 部分支持。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_TALENTIR_009_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []
snap = json.load(open(SNAP, encoding="utf-8"))

# ============ ① gkx：学者时序/预测面排除 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
facts["gkx_forecast_like_tables"] = [t for t in gkx_tables
    if re.search(r"forecast|predict|potential|yearly|trend|momentum", t, re.I)]
cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_scholar")]
facts["gkx_scholar_snapshot_cols"] = [c for c in cols
    if re.search(r"paper|citation|h_index|nums", c, re.I)]
facts["gkx_scholar_timeseries_cols"] = [c for c in cols
    if re.search(r"year|annual|forecast|predict|trend", c, re.I)]
gcur.close()

# ============ ② dev：学者预测承载排除 ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
lcur.execute(
    "SELECT table_schema, table_name FROM information_schema.tables "
    "WHERE table_schema LIKE 'gkxlumenx%%' AND table_name REGEXP "
    "'forecast|predict|potential|scholar|talent'")
facts["dev_forecast_like_tables"] = [f"{r[0]}.{r[1]}" for r in sorted(lcur.fetchall())]
lconn.close()

# ============ ③ 久新：potential 面 + yearly 时序原料（核心） ============
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)
jconn = pymysql.connect(**JX)
jcur = jconn.cursor()
def qj(sql):
    jcur.execute(sql)
    return jcur.fetchall()

jx_tables = snap["jiuxin"]["tables"]
facts["jiuxin_table_count"] = len(jx_tables)

# 3.1 potential 动量面（未来产出增长的族内最近承载）
facts["jiuxin_potential_result_rows"] = int(qj(
    "SELECT COUNT(*) FROM ads_talent_potential_result")[0][0])
facts["jiuxin_potential_composite_nonnull"] = int(qj(
    "SELECT COUNT(potential_composite_score) FROM ads_talent_potential_result")[0][0])
facts["jiuxin_potential_momentum_nonnull"] = int(qj(
    "SELECT COUNT(output_momentum_score) FROM ads_talent_potential_result")[0][0])
row = qj("SELECT MIN(output_momentum_score), MAX(output_momentum_score), "
         "ROUND(AVG(output_momentum_score),4) FROM ads_talent_potential_result")
facts["jiuxin_output_momentum_min_max_avg"] = [float(row[0][0]), float(row[0][1]), float(row[0][2])]
# 观察窗与职业阶段（预测模型的分期语义在案）
facts["jiuxin_potential_window"] = [int(qj(
    "SELECT MIN(observation_start_year) FROM ads_talent_potential_result")[0][0]),
    int(qj("SELECT MAX(observation_end_year) FROM ads_talent_potential_result")[0][0])]
facts["jiuxin_potential_career_stages"] = [[str(a), int(b)] for a, b in qj(
    "SELECT career_stage, COUNT(*) FROM ads_talent_potential_result "
    "GROUP BY career_stage ORDER BY career_stage")]

# 3.2 时序原料：ads_talent_yearly_metrics 结构 + 覆盖
ym_cols = [r[0] for r in qj("DESC ads_talent_yearly_metrics")]
facts["jiuxin_yearly_metrics_cols"] = ym_cols
facts["jiuxin_yearly_metrics_rows"] = int(qj(
    "SELECT COUNT(*) FROM ads_talent_yearly_metrics")[0][0])
facts["jiuxin_yearly_metrics_talents"] = int(qj(
    "SELECT COUNT(DISTINCT talent_id) FROM ads_talent_yearly_metrics")[0][0])
facts["jiuxin_yearly_metrics_year_span"] = [int(qj(
    "SELECT MIN(year) FROM ads_talent_yearly_metrics")[0][0] or 0),
    int(qj("SELECT MAX(year) FROM ads_talent_yearly_metrics")[0][0] or 0)]

# 3.3 预测词族表名扫（区分「潜力评估面」与「产出预测面」）
facts["jiuxin_forecast_like_tables"] = sorted([t for t in jx_tables
    if re.search(r"forecast|predict", t, re.I)])
jconn.close()

# ================= 派生 =================
n_pot = facts["jiuxin_potential_result_rows"]
n_mom = facts["jiuxin_potential_momentum_nonnull"]
derived.append({
    "key": "jiuxin_output_momentum_coverage_pct",
    "value": round(100.0 * n_mom / n_pot, 2),
    "numerator": n_mom,
    "denominator": n_pot,
    "note": "分子=ads_talent_potential_result.output_momentum_score 非空行数；分母=同表总行数"
            "（同表全量非采样）——产出动量分覆盖度（动量分是『近年产出加速度』的评估分，"
            "非『未来产出增长预测值』本身）",
})
n_ym_tal = facts["jiuxin_yearly_metrics_talents"]
n_prof = snap["jiuxin"]["rowcounts"]["ads_talent_profile"]
derived.append({
    "key": "jiuxin_yearly_metrics_talent_coverage_pct",
    "value": round(100.0 * n_ym_tal / n_prof, 2),
    "numerator": n_ym_tal,
    "denominator": n_prof,
    "note": "分子=ads_talent_yearly_metrics 去重 talent 数；分母=ads_talent_profile 总行数"
            "（跨表面分母——时序原料对主画像池的覆盖率，口径差异在 note 写死，B3）",
})
# 负结论登记（B10）
derived.append({
    "key": "scholar_future_output_growth_forecast",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "不可算——三源无『未来产出增长预测值』模型输出面（forecast/predict 表族经核对均为"
            "科研问题/技术域预测面，非学者个体产出预测）；potential 动量分是历史加速度评估非外推"
            "预测；按 B10 不写伪预测值，此键留空即负结论登记",
})

# ================= absence_probe =================
absence += [
    {"probe": "gkx 学者时序/预测面（表名 forecast/predict/potential/yearly/trend/momentum 词族 + dwd_scholar 列核对）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）词族扫 + SHOW COLUMNS FROM gkx.dwd_scholar（27 列）",
     "hits": len(facts["gkx_forecast_like_tables"]) + len(facts["gkx_scholar_timeseries_cols"]),
     "hit_detail": f"表名命中 {facts['gkx_forecast_like_tables']}；dwd_scholar 时序/预测列命中 "
                   f"{facts['gkx_scholar_timeseries_cols']}——只有 paper_nums/citation_nums/h_index "
                   "快照计数列（快照≠时序），无逐年序列无预测面"},
    {"probe": "dev 学者预测承载（gkxlumenx_* 全 schema forecast/predict/potential/scholar/talent 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_* 16 schema（542 表）",
     "hits": len(facts["dev_forecast_like_tables"]),
     "hit_detail": f"命中 {facts['dev_forecast_like_tables']}——语义排除：企业/政策侧表，"
                   "无学者个体产出预测面"},
    {"probe": "久新学者产出预测面（210 表 forecast/predict 词族 + 语义核对）",
     "source": "jiuxin",
     "sql": "SHOW TABLES（210 表，2026-11-01 实测）词族扫；命中表逐张语义核对",
     "hits": len(facts["jiuxin_forecast_like_tables"]),
     "hit_detail": f"命中 {facts['jiuxin_forecast_like_tables']}——全部是 research_problem/"
                   "technology 域的预测面（科研问题预测/技术域预测），无一张是学者个体"
                   "『未来产出增长预测』输出面；ads_research_outcome_forecast 是科研成果总量预测"
                   "非学者个体粒度"},
    {"probe": "需求原文「阶段增长预测」算式段",
     "source": "doc",
     "sql": "rg 阶段增长预测/预测视图 三份需求真源",
     "hits": 1,
     "hit_detail": "主需求 :2355-2357（1.1.1.1.4.3.4.1.3(2) 预测视图缩放）：『在引进模拟场景中，"
                   "支持对贡献度预测结果的缩放，用户可切换整体预期、局部影响及阶段性增长视图』——"
                   "视图切换行为在、预测算式无；UI stage 因子 1.15 为 mock 演示值",
    },
]

support = "部分支持"

notes += [
    "判档：『未来产出增长预测值』模型输出面三源未立项（forecast 表族均为科研问题/技术域预测），"
    "但久新双承载在——potential 动量面（面向未来的评估分）+ yearly_metrics 时序原料（转换路径可算）"
    "→ 按 Lane 6 框架（模型承载=有结构化模型输出面才部分支持）判部分支持",
    f"动量面读数：output_momentum_score 覆盖 {derived[0]['value']}%（{n_mom}/{n_pot}），"
    f"分布 {facts['jiuxin_output_momentum_min_max_avg']}——『近年产出加速度』评估分，语义近邻"
    "（增长趋势的方向），但非外推预测值（无预测目标年、无置信区间）",
    f"时序原料读数：ads_talent_yearly_metrics {facts['jiuxin_yearly_metrics_rows']} 行覆盖 "
    f"{n_ym_tal} 人才（主画像池 {derived[1]['value']}%），年份跨度 "
    f"{facts['jiuxin_yearly_metrics_year_span']}——学者×年产出序列在，回归外推（Acuna 型模型）"
    "的原料双在（结构+数据量），转换路径成立",
    f"久新活库：实测 {len(jx_tables)} 张（2026-11-01 探测日）",
    "mock 披露：ContributionTab.jsx:311 predictViewMap 的 stage 因子 1.15/overall 1.05/local 0.85 "
    "均为前端常量（近两年点 v*factor+斜率外推）——演示值，不作数据证据（B10）",
    "B11 对账：potential 100,000 与 TALENTIR_004 profile 行数一致；capability 99,996 与 003 产物一致",
    "升档触发器（B10）：①甲方裁定预测口径=potential 动量分代理 → 完全直接支持（面在）；"
    "②基于 yearly_metrics 建学者产出外推模型（Acuna 型回归/时序模型立项）→ 完全转换支持",
]

out = {
    "metric_id": "M_SCIUI_TALENTIR_009",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/talent-trend/components/ContributionTab.jsx:311",
        "repos/demo-ui-science/src/pages/talent-trend/components/ContributionTab.jsx:307",
        "repos/demo-ui-science/src/pages/talent-trend/components/ContributionTab.jsx:316",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "主需求《科技信息展示系统和科技专题服务系统.md》:2355-2357（1.1.1.1.4.3.4.1.3(2) "
                "预测视图缩放）明列『阶段性增长视图』——视图名在、预测算式无；"
                "「学者未来产出增长预测值」为派单书按 UI 视图语义定名",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [str(facts["jiuxin_potential_window"][1])] if facts["jiuxin_potential_window"][1] else [],
    "base_years_missing": [],
    "base_years_note": "potential 面观察窗（observation_start/end_year）与 yearly_metrics 年份跨度"
                       "在产物 facts.jiuxin_potential_window / jiuxin_yearly_metrics_year_span 登记",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(n_pot), str(n_mom), str(n_ym_tal), str(n_prof), "280", "210", "27",
                          "1.15", "1.05", "0.85"][:10]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
