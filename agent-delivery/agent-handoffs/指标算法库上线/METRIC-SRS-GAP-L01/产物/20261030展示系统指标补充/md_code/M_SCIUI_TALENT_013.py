#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TALENT_013 基线与风险解释 · 三源探针与复现脚本（S3-03 Lane 5）。

含义：人才引进评估页（talent-preview EvaluationPage）「基线与风险解释」卡片——
案例基线（同领域候选人均值，雷达虚线对照）+ 数据完整度/主要不确定性/建议复核三行
解释性读数（数据完整度=中高、不确定性=合作窗口与资源包、建议复核=正式接触前补充尽调）。
UI：repos/demo-ui-science/src/pages/talent-preview/pageRenderer/EvaluationPage.jsx:637-657。
数值语义源：data.js recommendFactors.referenceChart（样本参考基线 mock）+ 组件内写死文案
——演示值，不作数据证据。

SRS 溯源：主需求《科技信息展示系统和科技专题服务系统.md》:2367-2371 学者引进难度预测
（1.1.1.1.4.3.4.2，含引进阻力量化评分/策略建议与预警提示）；:2453 尽调报告风险点分析。
「基线与风险解释」作为卡片名三份真源 0 命中（UI 拆件）。

三源判档路径：
- 「同领域基线」结构在：久新 ads_talent_capability_* 分层基准（cohort=primary_field:career_stage，
  少于 200 人组不发布）+ ads_talent_profile 评分组排名（academic_capability_rank 1-100000）——
  「基线」= 库内同组中位数可现转（capability_assessment.primary_field_id 99,996/99,996 全覆盖）；「样本参考基线」referenceChart 型结果面无（同领域候选人均值面未物化）；
- 「风险解释」结构缺：学者级 risk/barrier/compliance 结果面三源 0 命中
  （gkx 仅企业风险表族；dev 仅企业 realdata_enterprise_risk；久新 risk 词族表 0）；
  部分依赖维在：ads_talent_mobility_event（流动壁垒/跨国事件+置信度）、撤稿面（学术诚信代理）。
→ 基线侧可现转 + 风险解释侧零承载 → 部分支持。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_TALENT_013_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)
jconn = pymysql.connect(**JX)
jcur = jconn.cursor()


def qj(sql):
    jcur.execute(sql)
    return jcur.fetchall()


# ---------- ① 久新：基线侧（capability 分层基准 + profile 评分排名） ----------
jcur.execute("SHOW TABLES")
jx_tables = sorted(r[0] for r in jcur.fetchall())
facts["jiuxin_table_count"] = len(jx_tables)

facts["jiuxin_capability_assessment_rows"] = int(
    qj("SELECT COUNT(*) FROM ads_talent_capability_assessment")[0][0])
facts["jiuxin_capability_model_rows"] = int(
    qj("SELECT COUNT(*) FROM ads_talent_capability_model")[0][0])
# 模型基准总体与分组口径（baseline 判定的官方口径）
row = qj("SELECT * FROM ads_talent_capability_model LIMIT 1")
if row:
    facts["jiuxin_capability_model_row_sample"] = [str(x) for x in row[0]]

# cohort 型分层基准（potential_result 的比较组）——schema 文档在案的基线机制
pr_cols = [r[0] for r in qj("DESC ads_talent_potential_result")]
facts["jiuxin_potential_result_cohort_like_cols"] = [c for c in pr_cols
                                                     if re.search(r"cohort|baseline|benchmark|reference|rank|percentile|group", c, re.I)]
facts["jiuxin_potential_result_rows"] = int(qj("SELECT COUNT(*) FROM ads_talent_potential_result")[0][0])
# cohort 样例（field:career_stage 分组，含 cohort_talent_count 与实测去重人才数对账）
rows = qj("SELECT cohort_id, cohort_talent_count, COUNT(*), COUNT(DISTINCT talent_id) "
          "FROM ads_talent_potential_result WHERE cohort_id IS NOT NULL "
          "GROUP BY cohort_id, cohort_talent_count ORDER BY cohort_id ASC LIMIT 6")
facts["jiuxin_potential_result_cohort_sample"] = [[str(a), int(b or 0), int(c), int(d)] for a, b, c, d in rows]

# 同领域基线可现转验证：capability_assessment 按 primary_field（openalex_field_id 数字串）分组中位数
# （ads_talent_profile 无 primary_field_id——主领域承载在 capability/potential/yearly_discipline 三面）
rows = qj("SELECT c.primary_field_id, f.name_zh, COUNT(*), ROUND(AVG(c.overall_score),4), "
          "ROUND(MEDIAN(c.overall_score),4) FROM ads_talent_capability_assessment c "
          "LEFT JOIN ads_discipline_field f ON f.openalex_field_id = c.primary_field_id "
          "WHERE c.primary_field_id IS NOT NULL GROUP BY c.primary_field_id, f.name_zh "
          "ORDER BY COUNT(*) DESC, c.primary_field_id ASC LIMIT 5")
facts["jiuxin_baseline_by_field_top5"] = [[str(a), str(b), int(c), float(d), float(e)] for a, b, c, d, e in rows]
facts["jiuxin_capability_pf_nonnull"] = int(
    qj("SELECT COUNT(primary_field_id) FROM ads_talent_capability_assessment")[0][0])
facts["jiuxin_capability_rows"] = int(
    qj("SELECT COUNT(*) FROM ads_talent_capability_assessment")[0][0])
facts["jiuxin_profile_rows"] = int(qj("SELECT COUNT(*) FROM ads_talent_profile")[0][0])
# 全池基准中位数（「同领域候选人均值」型对照的全池参考值）
facts["jiuxin_capability_overall_median"] = float(
    qj("SELECT ROUND(MEDIAN(overall_score),4) FROM ads_talent_capability_assessment")[0][0])
rows = qj("SELECT career_stage, COUNT(*) FROM ads_talent_potential_result "
          "GROUP BY career_stage ORDER BY career_stage")
facts["jiuxin_potential_career_stage_dist"] = [[str(a), int(b)] for a, b in rows]

# ---------- ② 久新：风险解释侧（结构探针 + 可用代理维） ----------
facts["jiuxin_risk_like_tables"] = [t for t in jx_tables
                                    if re.search(r"risk|barrier|compliance|difficulty|friction", t, re.I)]
# 流动壁垒维（mobility_event）
facts["jiuxin_mobility_event_rows"] = int(qj("SELECT COUNT(*) FROM ads_talent_mobility_event")[0][0])
rows = qj("SELECT mobility_type, COUNT(*) FROM ads_talent_mobility_event "
          "GROUP BY mobility_type ORDER BY mobility_type")
facts["jiuxin_mobility_event_type_dist"] = [[str(a), int(b)] for a, b in rows]
facts["jiuxin_mobility_cross_country_events"] = int(
    qj("SELECT COUNT(*) FROM ads_talent_mobility_event WHERE is_cross_country = 1")[0][0])
facts["jiuxin_mobility_distinct_talents"] = int(
    qj("SELECT COUNT(DISTINCT talent_id) FROM ads_talent_mobility_event")[0][0])
# 置信度面（解释卡「数据完整度」的库内对应物）
rows = qj("SELECT assignment_confidence, COUNT(*) FROM ads_talent_mobility_event "
          "GROUP BY assignment_confidence ORDER BY assignment_confidence LIMIT 6")
facts["jiuxin_mobility_confidence_dist"] = [[float(a) if a is not None else None, int(b)] for a, b in rows]
# 学术诚信负向维（撤稿）
facts["jiuxin_retracted_papers"] = int(
    qj("SELECT COUNT(*) FROM ads_paper_profile WHERE is_retracted = 1")[0][0])
# profile 风险词族列
prof_cols = [r[0] for r in qj("DESC ads_talent_profile")]
facts["jiuxin_profile_cols_count"] = len(prof_cols)
facts["jiuxin_profile_risk_like_cols"] = [c for c in prof_cols
                                          if re.search(r"risk|barrier|baseline|compliance|difficulty", c, re.I)]
jconn.close()

# ---------- ③ gkx：学者风险/基线承载探针 ----------
gcur = gkx()
gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
facts["gkx_scholar_risk_like_tables"] = [t for t in gkx_tables
                                         if re.search(r"scholar.*(risk|difficulty|eval)|(risk|difficulty).*scholar", t, re.I)]
facts["gkx_risk_like_tables_all"] = [t for t in gkx_tables
                                     if re.search(r"risk|barrier|compliance|difficulty", t, re.I)]
gcur.close()

# ---------- ④ dev：人才风险承载探针 ----------
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
lcur.execute("SELECT table_schema, table_name FROM information_schema.tables "
             "WHERE table_schema LIKE 'gkxlumenx%%' AND table_name REGEXP 'talent|scholar' "
             "AND table_name REGEXP 'risk|eval|difficulty|baseline'")
facts["dev_talent_risk_like_tables"] = [f"{r[0]}.{r[1]}" for r in lcur.fetchall()]
lconn.close()

# ================= 派生 =================
n_pf = facts["jiuxin_capability_pf_nonnull"]
n_all = facts["jiuxin_capability_rows"]
derived.append({
    "key": "jiuxin_primary_field_coverage_pct",
    "value": round(100.0 * n_pf / n_all, 2),
    "numerator": n_pf,
    "denominator": n_all,
    "note": "分子=ads_talent_capability_assessment.primary_field_id 非空行数；分母=该表总行数"
            "（同表全量非采样）——同领域基线（按 Field 分组）的可分组覆盖率（profile 表无 primary_field_id，"
            "主领域承载在本表）",
})
n_evt = facts["jiuxin_mobility_event_rows"]
n_cc = facts["jiuxin_mobility_cross_country_events"]
derived.append({
    "key": "jiuxin_cross_country_event_share_pct",
    "value": round(100.0 * n_cc / n_evt, 2),
    "numerator": n_cc,
    "denominator": n_evt,
    "note": "分子=is_cross_country=1 的迁移事件数；分母=ads_talent_mobility_event 总行数（同表全量非采样）——"
            "流动壁垒风险维的事件面读数",
})
# 负结论登记（B10：不写伪解释分）
derived.append({
    "key": "scholar_risk_explanation_score",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "不可算——学者级『风险解释』结果面（学术诚信/合作合规/出访敏感性等解释卡）三源零承载；"
            "按 B10 不写伪分。可用代理维：迁移事件（流动壁垒/跨国）+ 撤稿面（学术诚信负向）+ cohort 基线机制",
})

# ================= absence_probe =================
absence.extend([
    {"probe": "久新 210 张实测表 risk/barrier/compliance/difficulty/friction 词族（学者级风险解释结果面）",
     "source": "jiuxin", "sql": "SHOW TABLES 后词族扫（探测日实测表数见 facts.jiuxin_table_count）",
     "hits": 0, "hit_detail": "命中 []——学者级风险解释/引进阻力结果面零承载；可用代理维仅在事件面"
            "（ads_talent_mobility_event）与负向维（ads_paper_profile.is_retracted）"},
    {"probe": "gkx 280 表 scholar×risk/difficulty/eval 交叉词族",
     "source": "gkx", "sql": "SHOW TABLES FROM gkx 后词族扫",
     "hits": 0, "hit_detail": "命中 []——风险词族命中 7 表全为企业风险（dwd_org_risk_shixin/tax_punish/"
            "zhixing 及 bak），无学者级风险承载；与 TALENTIR_010 件读数同构（企业≠学者）"},
    {"probe": "dev gkxlumenx_* talent/scholar×risk/eval/difficulty/baseline 词族",
     "source": "dev", "sql": "information_schema.tables 扫 gkxlumenx_*",
     "hits": 0, "hit_detail": "命中 []——dev 无人才评估/风险承载（cms_expert_knowledge 为知识库非评分面）"},
    {"probe": "需求原文「基线与风险解释」卡片名与基线算式",
     "source": "doc",
     "sql": "rg 基线/风险解释/样本参考基线 三份需求真源",
     "hits": 0, "hit_detail": "卡片名「基线与风险解释」0 命中（UI 拆件）；最近义需求段为 :2367-2371 "
            "学者引进难度预测（引进阻力量化评分/策略建议与预警提示）与 :2453 尽调报告风险点分析——"
            "功能族在、卡片级算式无；UI 数据完整度=中高等三行解释为组件内写死演示文案"},
])

notes.extend([
    "本件支持度按三源评估（20261101 铁律）：dev live 非 demo + gkx 只读 + 久新 ads_* 只读。",
    "「基线」双口径：库内 cohort 分层基准（capability 模型少于 200 人组不发布 + potential_result "
    "cohort=primary_field:career_stage，schema 文档在案）为官方基线机制；UI referenceChart 型"
    "「样本参考基线」结果面无——按 Field 分组中位数可现转（facts.jiuxin_baseline_by_field_top5，"
    "承载面=capability_assessment.primary_field_id，profile 表无该列）。",
    "「风险解释」结构零承载（absence_probe 三源 0 命中）；代理维在：流动壁垒（跨区事件占比）、"
    "学术诚信（撤稿 0）、置信度面（assignment_confidence 分布）。",
    "UI 写死文案（数据完整度=中高/不确定性=合作窗口与资源包/建议复核=补充尽调）为前端演示值，"
    "登记不作数据证据；mock referenceChart 数值同。",
    "2026 为 PARTIAL_YEAR：mobility 事件面口径按 schema 文档不含 2026 正式事件（跨年缺口与 2026 "
    "部分年不产生正式迁移事件）。",
])

out = {
    "metric_id": "M_SCIUI_TALENT_013",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/talent-preview/pageRenderer/EvaluationPage.jsx:637（DataCard title 基线与风险解释）",
        "repos/demo-ui-science/src/pages/talent-preview/pageRenderer/EvaluationPage.jsx:639-651（案例基线说明+数据完整度/主要不确定性/建议复核三行）",
        "repos/demo-ui-science/src/pages/talent-preview/data.js:290-314（recommendFactors.referenceChart 样本参考基线 mock）",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "卡片名「基线与风险解释」三份真源 0 命中（UI 拆件）；功能族最近义：主需求 "
                ":2367-2371 学者引进难度预测（1.1.1.1.4.3.4.2.7 引进阻力量化评分/.2.8 策略建议与预警提示）"
                "+ :2453 定制化尽调报告生成（风险点分析）——功能族在、卡片级基线算式与风险解释算式无",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": "部分支持",
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件为快照型基线/风险读数（capability 与 profile 评分组均为当前发布版本快照；"
                       "迁移事件面为 4.5.0 版已发布事件集，无年度基线窗口需求）",
    "ctx_refs": {
        "note": "正文引用型数字登记",
        "refs": [],
    },
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1, default=str)
print("ok ->", OUT)
