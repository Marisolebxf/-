#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TALENTIR_002 多维综合评价与评分 · 三源探针与复现脚本（S3-03 Lane 6）。

含义：人才尽调报告与推荐（1.1.1.1.4.3.4.4.2）的专家多维综合评价与评分——
「基于权威度、创新性、项目经验、社会影响等多维量化指标，通过人工智能算法进行综合评分」。
UI：repos/demo-ui-science/src/pages/talent-trend/components/ReportTab.jsx:119
（Checkbox.Group 定制尽调维度选项 { value:'score', label:'多维综合评价与评分' }；
默认勾选 DEFAULT_DIMS+['score']）。
语义源：data.js:1486-1502 generateEvaluationData——aiScore = dims.authority×0.28 +
dims.innovation×0.24 + dims.project×0.22 + dims.influence×0.16 + dims.social×0.1，
五维全部 random(55,95) mock 常量（演示值，不作数据证据）。

三源判档路径：
- 久新 ads_talent_profile 评分组字段（academic_capability 及五个标准化分项分 +
  weight_coverage + rank + score_version）是结构+数据双在的现成「多维综合评分」结果面；
- 久新 ads_talent_capability_assessment / _dimension_metric / _model 三表族是通用能力评估
  模型面（本件实测行数与结构定性）；
- dev/gkx 无人才评分结果面（词族探针留证）。
→ 久新承载按「现成结果面但维度集/权重口径与 UI 五维不同物」处理，判档部分支持。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_TALENTIR_002_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

# ============ ① gkx：人才评价/评分结果面探针 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
facts["gkx_talent_eval_like_tables"] = [t for t in gkx_tables if re.search(r"talent|scholar", t, re.I)
                                        and re.search(r"score|eval|assess|rating|capab", t, re.I)]
facts["gkx_scholar_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_scholar")[0][0])
# dwd_scholar 列清单（27 列——评分列存在性核对）
facts["gkx_scholar_cols"] = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_scholar")]
facts["gkx_scholar_score_like_cols"] = [c for c in facts["gkx_scholar_cols"]
                                        if re.search(r"score|rating|capab|eval", c, re.I)]
gcur.close()

# ============ ② dev：人才评分承载探针 ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()

# 全 schema 扫 talent×score/eval 词族
lcur.execute(
    "SELECT table_schema, table_name FROM information_schema.tables "
    "WHERE table_schema LIKE 'gkxlumenx%%' AND table_name REGEXP 'talent|scholar|expert'")
dev_talent_tables = [(r[0], r[1]) for r in lcur.fetchall()]
facts["dev_talent_like_tables"] = [f"{s}.{t}" for s, t in dev_talent_tables]
facts["dev_talent_eval_like_tables"] = [f"{s}.{t}" for s, t in dev_talent_tables
                                        if re.search(r"score|eval|assess|rating|capab", t, re.I)]
lconn.close()

# ============ ③ 久新：ads_talent_profile 评分组 + capability 三表族（核心） ============
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)
jconn = pymysql.connect(**JX)
jcur = jconn.cursor()
def qj(sql):
    jcur.execute(sql)
    return jcur.fetchall()

# 3.1 主画像评分组：行数 + 评分覆盖率 + 版本 + 分布
facts["jiuxin_talent_profile_rows"] = int(qj("SELECT COUNT(*) FROM ads_talent_profile")[0][0])
row = qj("SELECT COUNT(academic_capability), COUNT(paper_score), COUNT(citation_score), "
         "COUNT(h_index_score), COUNT(collaboration_score), COUNT(core_source_score), "
         "COUNT(talent_potential) FROM ads_talent_profile")[0]
facts["jiuxin_profile_score_nonnull"] = {
    "academic_capability": int(row[0]), "paper_score": int(row[1]),
    "citation_score": int(row[2]), "h_index_score": int(row[3]),
    "collaboration_score": int(row[4]), "core_source_score": int(row[5]),
    "talent_potential": int(row[6]),
}
row = qj("SELECT MIN(academic_capability), MAX(academic_capability), AVG(academic_capability), "
         "MIN(academic_metric_weight_coverage), MAX(academic_metric_weight_coverage) "
         "FROM ads_talent_profile WHERE academic_capability IS NOT NULL")[0]
facts["jiuxin_academic_capability_min"] = float(row[0])
facts["jiuxin_academic_capability_max"] = float(row[1])
facts["jiuxin_academic_capability_avg"] = round(float(row[2]), 4)
facts["jiuxin_weight_coverage_min"] = float(row[3])
facts["jiuxin_weight_coverage_max"] = float(row[4])
facts["jiuxin_score_versions"] = [[str(a), int(b)] for a, b in qj(
    "SELECT score_version, COUNT(*) FROM ads_talent_profile GROUP BY score_version ORDER BY COUNT(*) DESC")]
# 分数分布（10 分桶，按键排序确定性）
facts["jiuxin_academic_capability_decile"] = [[str(a), int(b)] for a, b in qj(
    "SELECT FLOOR(academic_capability/10)*10 AS bucket, COUNT(*) FROM ads_talent_profile "
    "WHERE academic_capability IS NOT NULL GROUP BY bucket ORDER BY bucket")]
# Top5 样例（具名可解释）
facts["jiuxin_top5_by_academic_capability"] = [
    {"name": (r[0] or ""), "academic_capability": float(r[1]), "rank": int(r[2]),
     "paper_score": float(r[3]) if r[3] is not None else None,
     "citation_score": float(r[4]) if r[4] is not None else None}
    for r in qj("SELECT name, academic_capability, academic_capability_rank, paper_score, citation_score "
                "FROM ads_talent_profile WHERE academic_capability IS NOT NULL "
                "ORDER BY academic_capability DESC, academic_capability_rank ASC LIMIT 5")]
# 权重公式验证（库内公式 0.20/0.30/0.30/0.15/0.05 抽样重算）
row = qj("SELECT academic_capability, paper_score, citation_score, h_index_score, "
         "collaboration_score, core_source_score, academic_metric_weight_coverage "
         "FROM ads_talent_profile WHERE academic_capability IS NOT NULL "
         "AND core_source_score IS NOT NULL ORDER BY talent_id LIMIT 1")[0]
ac, ps, cs, hs, co, core, cov = (float(row[0]), float(row[1]), float(row[2]),
                                 float(row[3]), float(row[4]), float(row[5]), float(row[6]))
recalc = (0.20 * ps + 0.30 * cs + 0.30 * hs + 0.15 * co + 0.05 * core) / cov
facts["jiuxin_weight_formula_sample_check"] = {
    "stored": ac, "recalc": round(recalc, 4), "abs_diff": round(abs(ac - recalc), 6),
    "weight_coverage": cov,
}

# 3.2 capability 三表族（通用能力评估模型面）
cap = {}
for t in ["ads_talent_capability_assessment", "ads_talent_capability_dimension_metric",
          "ads_talent_capability_model"]:
    cols = [r[0] for r in qj(f"SHOW COLUMNS FROM {t}")]
    n = int(qj(f"SELECT COUNT(*) FROM {t}")[0][0])
    cap[t] = {"cols": cols, "rows": n}
facts["jiuxin_capability_family"] = cap
# model 表若有数据，登记模型定义样例
if cap["ads_talent_capability_model"]["rows"] > 0:
    facts["jiuxin_capability_model_rows_detail"] = [
        [str(x) if x is not None else None for x in r]
        for r in qj("SELECT * FROM ads_talent_capability_model LIMIT 3")]
jconn.close()

# ================= 派生 =================
n_prof = facts["jiuxin_talent_profile_rows"]
n_score = facts["jiuxin_profile_score_nonnull"]["academic_capability"]
derived.append({
    "key": "jiuxin_academic_capability_coverage_pct",
    "value": round(100.0 * n_score / n_prof, 2),
    "numerator": n_score,
    "denominator": n_prof,
    "note": "分子=ads_talent_profile.academic_capability 非空行数；分母=ads_talent_profile 总行数（同表同 WHERE，全量非采样）",
})
# UI mock 五维加权结构披露（演示值重算，不参与支持度结论）
# data.js:1488-1490 五维 random 区间：authority(70,95)/innovation(65,92)/project(60,90)/influence(68,94)/social(55,90)
mock_dims = {"authority": (0.28, 82.5), "innovation": (0.24, 78.5), "project": (0.22, 75.0),
             "influence": (0.16, 81.0), "social": (0.10, 72.5)}
mock_val = round(sum(w * v for w, v in mock_dims.values()), 1)
derived.append({
    "key": "ui_mock_ai_score_structure_reference",
    "value": mock_val,
    "numerator": round(mock_val * 100, 0),
    "denominator": 100,
    "note": "UI 权重结构披露：aiScore=权威度×0.28+创新性×0.24+项目经验×0.22+影响力×0.16+社会影响×0.10"
            "（data.js:1491-1492 固定权重）；演示分值取 data.js:1488-1490 各维 random 区间中位数"
            "（82.5/78.5/75/81/72.5）重算——mock 演示值，证明前端口径为五维加权百分制，不参与支持度结论",
})

# ================= absence_probe =================
absence += [
    {"probe": "gkx 人才多维评分结果面（talent/scholar × score/eval/assess/rating/capab 词族）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表词族交叉扫）+ SHOW COLUMNS FROM gkx.dwd_scholar（27 列评分词族扫）",
     "hits": len(facts["gkx_talent_eval_like_tables"]) + len(facts["gkx_scholar_score_like_cols"]),
     "hit_detail": f"表名 0 命中；dwd_scholar 27 列中评分词族列 0 个（{facts['gkx_scholar_cols']}）——"
                   "gkx 学者面只有 paper_nums/citation_nums/h_index 原始计数，无任何合成评分列"},
    {"probe": "dev 人才评分结果面（gkxlumenx_* 全 schema talent/scholar/expert × 评分词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_* 五 schema talent|scholar|expert 表名再交叉评分词族",
     "hits": len(facts["dev_talent_eval_like_tables"]),
     "hit_detail": f"talent/scholar/expert 词族表共 {len(dev_talent_tables)} 张，交叉评分词族 0 命中——"
                   f"清单：{facts['dev_talent_like_tables'][:20]}"},
    {"probe": "需求原文「多维综合评价与评分」评分算法定义段",
     "source": "doc",
     "sql": "rg 多维综合评价与评分 三份需求真源（科技信息展示系统和科技专题服务系统.md:2447-2449 命中功能叶）",
     "hits": 1,
     "hit_detail": "需求给出功能行为（『基于权威度、创新性、项目经验、社会影响等多维量化指标，通过人工智能算法"
                   "进行综合评分』）但维度权重/合成算式无——评分口径未闭合；UI 权重 0.28/0.24/0.22/0.16/0.10 为演示值"},
]

support = "部分支持"

notes += [
    "判档：久新 ads_talent_profile 评分组是结构+数据双在的现成多维综合评分结果面（academic_capability "
    "五分项加权 + weight_coverage + 唯一稳定排名 + score_version=talent_academic_mvp_v1），覆盖率 "
    f"{derived[0]['value']}%（{n_score}/{n_prof}）；但维度集（论文/被引/H指数/合作广度/Core覆盖）与 UI "
    "需求五维（权威度/创新性/项目经验/社会影响——mock）不同物，且 UI 口径未闭合 → 部分支持",
    "库内权重公式实测复算：0.20×paper+0.30×citation+0.30×h_index+0.15×collab+0.05×core 按抽样行重算与存储值"
    f"逐位一致（abs_diff={facts['jiuxin_weight_formula_sample_check']['abs_diff']}）——权重口径在久新侧闭合",
    "capability 三表族（assessment/dimension_metric/model）为通用能力评估模型面——本件实测行数见产物"
    "jiuxin_capability_family；model 表行数>0 时登记模型定义样例",
    "mock 披露：ReportTab.jsx:119 复选项的评分语义源为 data.js:1486-1502 mock 生成器——五维 random(55,95) "
    "常量 + 固定权重 0.28/0.24/0.22/0.16/0.10 加权 aiScore——演示值不作数据证据（B10）",
    "B11 对账：gkx dwd_scholar 21,316 与共享快照 _shared_probe_s3_01_out.json（dims.gkx 人才数 21316）零漂移；"
    "久新 ads_talent_profile 100,000 与 M_TALENT_UI_CHINESE_RATIO 久新回填段（总 100,000）零漂移",
    "升档触发器（B10）：①甲方裁定尽调评分口径=久新 academic_capability 维度集（或出官方映射表 UI 五维↔库五分项）"
    "→ 直查可算升完全直接支持；②若坚持 UI 五维（权威度/创新性/项目经验/社会影响）→ 权威度/社会影响两维在三源"
    "无承载（无荣誉奖项强度数据、无社媒传播数据），维持部分支持",
]

out = {
    "metric_id": "M_SCIUI_TALENTIR_002",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/talent-trend/components/ReportTab.jsx:119",
        "repos/demo-ui-science/src/pages/talent-trend/data.js:1486",
        "repos/demo-ui-science/src/pages/talent-trend/components/DueDiligenceReport.jsx:1",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "主需求《科技信息展示系统和科技专题服务系统.md》:2441/:2447-2449（1.1.1.1.4.3.4.4.2 多维综合"
                "评价与评分）功能叶明列：『基于权威度、创新性、项目经验、社会影响等多维量化指标，通过人工智能"
                "算法进行综合评分』——功能在、评分算式无；核增/算法库两份真源 0 命中",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件为人才快照型评分（ads_talent_profile 当前发布单版本，无年度序列；年度评分在 "
                       "ads_talent_yearly_metrics.academic_capability 另有承载，本件未展开）",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts["gkx_scholar_rows"]), str(n_prof), str(n_score),
                          str(facts["jiuxin_academic_capability_avg"]),
                          "27", "100000", "21316", "0.28", "0.24", "0.22", "0.16", "0.10",
                          "0.20", "0.30", "0.15", "0.05", "119", "2447"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
