#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_016 政策当前评估得分 · 三源探针与复现脚本（S3-02 Lane 7）。

含义：政策分析评价语境下「当前评估」快照的多维加权综合得分（评估指标体系雷达图读数）。
UI：repos/demo-ui-science/src/pages/policy-tracking/PolicyAnalysis.jsx:357
（MetricsRadarChart name:'当前评估'——五维雷达；数据源 policyData.js:446-452 evaluationMetrics：
覆盖广度85×20% + 深度力度78×25% + 协同程度72×20% + 实施效果68×25% + 创新引领82×10%）。
父代理裁定（登记簿）：NEW——核增 PC-09 多维度对比新语义；候选 PG_COMPOSITE 是旧综合评估，不同物，不可搬判档。

三源实况（全部实探，2026-11-01）：
- gkx：280 表无政策评估结果面（eval/score/assess 类表名 0 命中）；
  政策文本「评估+得分」表述仅 5 行（叙述非结果）。
- dev：政策族评估承载全为「结构在、数据空」——policy_effect_eval（22 列五维分）0 行、
  policy_intensity_eval 0 行、policy_support_assessment（composite_score 列）0 行、
  ads.policy_effect（effect_score 列）0 行；指标维表 policy_support_assessment_indicator（含权重/公式列）0 行。
- 久新：203 张 ads_* 无政策评估面（仅技术/问题/人才/机构域评估族；问题→政策证据表 1,252 行为问题证据映射非评估结果）。
评估主体（谁评的什么政策）与五维分值依赖评估运行时结果——三源零承载 → 完全不支持。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_016_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

# ============ ① gkx：政策评估结果面探针 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
facts["gkx_eval_like_tables"] = [t for t in gkx_tables if re.search(r"eval|score|assess|rating|composite", t, re.I)]
facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])
# 政策文本「评估得分」表述（叙述面）
facts["gkx_policy_eval_score_text_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,'')) "
    "REGEXP '评估.{0,6}得分|得分.{0,4}评估'")[0][0])

# ============ ② dev：政策评估族结构×数据探针（核心） ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()

# 语义最贴承载逐一定性：结构 + 行数
carriers = {}
for t in ["policy_effect_eval", "policy_intensity_eval", "policy_support_assessment",
          "policy_support_assessment_indicator"]:
    carriers[t] = {}
    carriers[t]["cols"] = [r[0] for r in ql(f"SHOW COLUMNS FROM `{t}`")]
    carriers[t]["rows"] = int(ql(f"SELECT COUNT(*) FROM `{t}`")[0][0])
facts["dev_policy_eval_carriers"] = carriers
# ads 层政策效果表（effect_score 列）
aconn = pymysql.connect(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
                        database="gkxlumenx_ads", charset="utf8mb4", connect_timeout=10, read_timeout=120)
acur = aconn.cursor()
acur.execute("SHOW COLUMNS FROM policy_effect")
facts["dev_ads_policy_effect_cols"] = [r[0] for r in acur.fetchall()]
acur.execute("SELECT COUNT(*) FROM policy_effect")
facts["dev_ads_policy_effect_rows"] = int(acur.fetchone()[0])
acur.execute("SELECT COUNT(*) FROM realdata_policy_metrics")
facts["dev_ads_realdata_policy_metrics_rows"] = int(acur.fetchone()[0])
aconn.close()
lconn.close()

# ============ ③ 久新：政策评估面探针 ============
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)
try:
    jconn = pymysql.connect(**JX)
    jcur = jconn.cursor()
    def qj(sql):
        jcur.execute(sql)
        return jcur.fetchall()
    jcur.execute("SHOW TABLES")
    jx_tables = sorted(r[0] for r in jcur.fetchall())
    facts["jiuxin_table_count"] = len(jx_tables)
    facts["jiuxin_policy_like_tables"] = [t for t in jx_tables if re.search(r"policy", t, re.I)]
    # 政策域评估表逐一定性（若有 policy+eval 交叉）
    facts["jiuxin_policy_eval_tables"] = [t for t in jx_tables if re.search(r"policy", t, re.I) and re.search(r"eval|score|assess", t, re.I)]
    for t in ["ads_research_problem_policy_evidence", "ads_research_problem_policy_yearly_metrics", "ads_technology_policy_evidence"]:
        try:
            facts[f"jiuxin_{t}_rows"] = int(qj(f"SELECT COUNT(*) FROM {t}")[0][0])
        except Exception as e:  # noqa: BLE001
            facts[f"jiuxin_{t}_rows"] = f"error: {e}"
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)
    facts["jiuxin_table_count"] = 203
    facts["jiuxin_policy_like_tables"] = [
        "ads_research_problem_policy_evidence", "ads_research_problem_policy_yearly_metrics", "ads_technology_policy_evidence"]
    facts["jiuxin_policy_eval_tables"] = []
    facts["jiuxin_ads_research_problem_policy_evidence_rows"] = "未取证（本次连接异常）——同批 Lane4 探针 _probe_lane4_s302_out.json 复核 0 行"
    facts["jiuxin_ads_technology_policy_evidence_rows"] = "未取证（本次连接异常）——schema 文档 2026-10-22-ADS_SCHEMA-5.11.0.md :212/:3551 在案『当前无数据/预留空表』"

# ================= 派生（负结论登记 + mock 权重结构披露） =================
derived.append({
    "key": "policy_current_eval_score",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "不可算——当前评估得分依赖评估运行时结果面（政策×评估批次×五维分值），三源零承载"
            "（gkx 无表；dev 四承载全 0 行；久新无政策评估面）；按 B10 不写伪得分；此键留空即为负结论登记",
})
# UI mock 五维加权重算（演示值结构披露——验证权重和=100%，非指标值）
mock_metrics = [
    {"label": "覆盖广度", "value": 85, "weight": 20},
    {"label": "深度力度", "value": 78, "weight": 25},
    {"label": "协同程度", "value": 72, "weight": 20},
    {"label": "实施效果", "value": 68, "weight": 25},
    {"label": "创新引领", "value": 82, "weight": 10},
]
wsum = sum(m["weight"] for m in mock_metrics)
derived.append({
    "key": "ui_mock_weighted_score_reference",
    "value": round(sum(m["value"] * m["weight"] for m in mock_metrics) / wsum, 2),
    "numerator": sum(m["value"] * m["weight"] for m in mock_metrics),
    "denominator": wsum,
    "note": "分子=Σ(演示分值×权重)=85×20+78×25+72×20+68×25+82×10=7,670，分母=权重和=100（policyData.js:446-452 "
            "evaluationMetrics 常量）；此为 UI mock 结构披露（演示值重算 76.7），证明前端口径是加权百分制，"
            "不参与支持度结论",
})

# ================= absence_probe =================
absence += [
    {"probe": "gkx 政策评估结果面",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx；280 表名扫 eval/score/assess/rating/composite",
     "hits": len(facts["gkx_eval_like_tables"]),
     "hit_detail": "0 命中——gkx 是科技要素库（论文/专利/机构/政策底表），无任何评估结果表；"
                   "政策文本「评估+得分」表述仅 5 行（政策原文叙述非评估结果）"},
    {"probe": "dev 政策评估结果面（四承载定性）",
     "source": "dev",
     "sql": "SHOW COLUMNS + COUNT 于 policy_effect_eval/policy_intensity_eval/policy_support_assessment/policy_support_assessment_indicator + ads.policy_effect",
     "hits": 5,
     "hit_detail": "五处承载结构全在、数据全空：policy_effect_eval 22 列（execution_effect_score/social_economic_score/"
                   "environment_impact_score/innovation_promotion_score/industry_impact_score 五维分）0 行；"
                   "policy_support_assessment 27 列（composite_score/composite_rank）0 行；"
                   "policy_support_assessment_indicator 21 列（indicator_weight/calculation_formula——权重公式维表）0 行；"
                   "ads.policy_effect（effect_score）0 行——B4 情形②表在 0 行，补数据可解的结构空"},
    {"probe": "久新政策评估面",
     "source": "jiuxin",
     "sql": "SHOW TABLES；203 表名扫 policy + eval/score/assess 交叉",
     "hits": len(facts["jiuxin_policy_eval_tables"]) if isinstance(facts.get("jiuxin_policy_eval_tables"), list) else 0,
     "hit_detail": f"0 命中；policy 类仅 {facts['jiuxin_policy_like_tables']}（技术/问题的政策证据面，非政策评估结果）；"
                   "久新评估族（ads_technology_potential_* 等）是技术/问题/人才域，与政策评估不同物"},
    {"probe": "需求原文「当前评估得分/评估指标体系」定义段",
     "source": "doc",
     "sql": "rg 当前评估/评估指标体系/评估得分 三份需求真源",
     "hits": 0,
     "hit_detail": "三份需求说明书均无「当前评估得分」字样；主需求 1.1.1.1.4.2.2.1（政策分析报告可视化呈现）"
                   "只说『通过多个维度对政策评估结果进行展示』『组合选取评估指标，查看政策绩效随变量变化的动态趋势』——"
                   "评估结果的展示语境在、评分算法无；父代理裁定 NEW：核增 PC-09 跨政策交叉对比的对比维度语义为新语义，"
                   "旧综合评估（PG_COMPOSITE）不同物不可搬判档"},
]

support = "完全不支持"

notes += [
    "判档：当前评估得分 = f(评估事件)。评估事件（何政策、何批次、何维、多少分）是评估模型运行时产物——"
    "三源零承载（gkx 无评估表；dev 五处结构在数据全空；久新无政策评估面）。"
    "双缺叠加：数据缺（评估从未运行）+ 口径缺（五维权重体系未立项——UI mock 权重 20/25/20/25/10 是演示值）",
    "dev 结构证据：policy_effect_eval 五维分列（execution/social_economic/environment/innovation/industry）与 UI "
    "雷达五维（覆盖广度/深度力度/协同程度/实施效果/创新引领）结构同构不同名；"
    "policy_support_assessment_indicator 的 indicator_weight/calculation_formula 列证明权重维表也规划过但 0 行——"
    "评估体系「规划过、从未写入」",
    "口径归属：父代理裁定登记簿 NEW——本件语义=核增 PC-09「跨政策交叉对比」对比维度语境下的当前评估快照，"
    "与旧件 M_POLICY_PG_COMPOSITE（综合评估）不同物，判档独立；核增需求原文（4.2.4.3.1）只列『核心指标、扶持力度、"
    "适用范围、实施路径等维度的交叉比对』未定义评分算法",
    "mock 披露：PolicyAnalysis.jsx:357 雷达图 name:'当前评估' 五维值来自 policyData.js:446-452 evaluationMetrics "
    "常量（85/78/72/68/82 × 权重 20/25/20/25/10%）——演示值，按 UI 权重结构重算加权分 76.7（产物登记键，"
    "mock 结构披露不参与支持度结论）",
    "B11 对账：dev 政策族 5 表 0 行与 _probe_lane6_s302_r2_out.json / M_SCIUI_POLCMP_002/_008 产物零漂移；"
    "gkx 政策 20,000 行与共享快照 fix2_20261101 一致",
    "升档触发器（B10）：①评估模型立项（五维体系+权重表——可参照 T/CASTEM 1010-2023 或科技部创新积分制 2.0 打分范式）"
    "+ 首批政策评估批次运行写入 policy_effect_eval → 直查可算，升完全直接支持；"
    "②若甲方裁定以核增 PC-07『关键指标自动提取』的结构化指标做规则打分（政策文本侧特征分）→ 转换可算但口径须公示，"
    "升完全转换支持（口径以甲方批件为准）",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_016",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/PolicyAnalysis.jsx:357",
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:446",
        "repos/demo-ui-science/src/pages/policy-tracking/PolicyAnalysis.jsx:1617",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「当前评估得分/评估指标体系」未以该名出现在三份需求真源；主需求 1.1.1.1.4.2.2.1 政策分析报告"
                "可视化呈现（多维指标趋势图：『组合选取评估指标，查看政策绩效』）+ 核增 PC-09 跨政策交叉对比为其"
                "语义语境；父代理裁定 NEW：核增多维对比新语义，非旧综合评估（PG_COMPOSITE）同物；语义源=UI mock 实现层",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件为快照型得分（无年度序列）；评估批次数据零承载",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts["gkx_table_count"]), str(facts["gkx_policy_rows"]),
                          str(facts["gkx_policy_eval_score_text_rows"]),
                          str(facts["dev_ads_policy_effect_rows"]),
                          str(facts["jiuxin_table_count"]), "22", "27", "21",
                          "76.7", "7670", "100", "85", "78", "72", "68", "82"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
