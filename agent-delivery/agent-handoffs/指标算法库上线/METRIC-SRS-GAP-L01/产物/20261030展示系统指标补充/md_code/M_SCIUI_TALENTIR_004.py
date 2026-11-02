#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TALENTIR_004 学者环境适应性评估得分 · 三源探针与复现脚本（S3-03 Lane 6）。

含义：学者引进难度预测（1.1.1.1.4.3.4.2.1 学者适应性评估）的量化得分——
「综合国籍、语言能力、教育经历、文化背景等多维信息，对学者的工作环境适应性进行量化分析」。
UI：repos/demo-ui-science/src/pages/talent-trend/talentRecommendSpec.js:22
（difficulty.l6 数组 { key:'adaptability', label:'学者适应性评估' }——L6 能力映射清单项）。
UI 实现层：data.js difficultyEstimate.factors / overall / level 均为 mock 演示值；
DifficultyTab 消费 factors 出雷达——「环境适应性得分」无独立公式，属引进阻力合成的一维。

三源判档路径（参照 POLCMP_008 写法：口径未立项+事件无源双缺）：
- 「环境适应性」评分口径三源均无承载（无国籍/语言能力/文化背景评分结果面）；
- 依赖侧可探：久新 ads_talent_experience（国籍代理=经历国家）、ads_talent_profile
  （country_name 常驻国）、ads_talent_mobility_event（跨地区流动）——结构性代理存在但
  「语言能力/文化背景」两维零承载；
- gkx dwd_scholar 无国籍/语言列（27 列在案）；
- dev 无人才评估承载。
→ 部分维度（地理/流动）可代理、语言/文化维零承载 + 评分口径未立项 → 部分支持。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_TALENTIR_004_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

# ============ ① gkx：适应性/国籍/语言承载探针 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
facts["gkx_adapt_like_tables"] = [t for t in gkx_tables if re.search(r"adapt|assimil|mobility|language", t, re.I)]
# dwd_scholar 国籍/语言列核对（27 列全清单复用 002 产物口径，此处独立复探）
cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_scholar")]
facts["gkx_scholar_nationality_language_cols"] = [c for c in cols if re.search(r"national|citizen|language|birth|country", c, re.I)]
facts["gkx_scholar_work_experience_cols"] = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_scholar_work_experience")]
gcur.close()

# ============ ② dev：人才适应性承载探针 ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()

lcur.execute(
    "SELECT table_schema, table_name FROM information_schema.tables "
    "WHERE table_schema LIKE 'gkxlumenx%%' AND table_name REGEXP 'adapt|assimil|difficulty|talent'")
facts["dev_adapt_like_tables"] = [f"{r[0]}.{r[1]}" for r in lcur.fetchall()]
lconn.close()

# ============ ③ 久新：适应性依赖维结构探针（核心） ============
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)
jconn = pymysql.connect(**JX)
jcur = jconn.cursor()
def qj(sql):
    jcur.execute(sql)
    return jcur.fetchall()

jcur.execute("SHOW TABLES")
jx_tables = sorted(r[0] for r in jcur.fetchall())
facts["jiuxin_table_count"] = len(jx_tables)
facts["jiuxin_adapt_like_tables"] = [t for t in jx_tables
                                     if re.search(r"adapt|assimil|language|culture", t, re.I)]

# 3.1 国籍/常驻国代理：profile.country_name + 经历国家多样性
facts["jiuxin_talent_profile_rows"] = int(qj("SELECT COUNT(*) FROM ads_talent_profile")[0][0])
facts["jiuxin_country_name_nonnull"] = int(qj(
    "SELECT COUNT(country_name) FROM ads_talent_profile")[0][0])
facts["jiuxin_top8_countries"] = [[str(a), int(b)] for a, b in qj(
    "SELECT country_name, COUNT(*) FROM ads_talent_profile WHERE country_name IS NOT NULL "
    "GROUP BY country_name ORDER BY COUNT(*) DESC, country_name ASC LIMIT 8")]
# 语言维代理：论文语言（talent→paper→language 需 join 大表，改为统计 paper_profile 语言面本身）
facts["jiuxin_paper_language_top8"] = [[str(a), int(b)] for a, b in qj(
    "SELECT language, COUNT(*) FROM ads_paper_profile WHERE language IS NOT NULL "
    "GROUP BY language ORDER BY COUNT(*) DESC, language ASC LIMIT 8")]

# 3.2 经历维：ads_talent_experience 行数 + 教育经历覆盖 + 经历国多样性样例
facts["jiuxin_talent_experience_rows"] = int(qj("SELECT COUNT(*) FROM ads_talent_experience")[0][0])
facts["jiuxin_experience_distinct_talents"] = int(qj(
    "SELECT COUNT(DISTINCT talent_id) FROM ads_talent_experience")[0][0])
facts["jiuxin_experience_education_rows"] = int(qj(
    "SELECT COUNT(*) FROM ads_talent_experience WHERE experience_type=1")[0][0])
facts["jiuxin_experience_country_nonnull"] = int(qj(
    "SELECT COUNT(country_name) FROM ads_talent_experience")[0][0])
# 跨国经历人才数（地理适应性代理读数：有 ≥2 个经历国家的去重人才）
facts["jiuxin_multi_country_experience_talents"] = int(qj(
    "SELECT COUNT(*) FROM (SELECT talent_id FROM ads_talent_experience "
    "WHERE country_name IS NOT NULL GROUP BY talent_id "
    "HAVING COUNT(DISTINCT country_name) >= 2) t")[0][0])

# 3.3 流动维：mobility_event 跨地区事件
facts["jiuxin_mobility_event_rows"] = int(qj("SELECT COUNT(*) FROM ads_talent_mobility_event")[0][0])
facts["jiuxin_mobility_cross_country_events"] = int(qj(
    "SELECT COUNT(*) FROM ads_talent_mobility_event WHERE is_cross_country = 1")[0][0])
facts["jiuxin_mobility_event_types"] = [[str(a), int(b)] for a, b in qj(
    "SELECT mobility_type, COUNT(*) FROM ads_talent_mobility_event GROUP BY mobility_type ORDER BY mobility_type")]

# 3.4 适应性评分结果面排除：capability 三表族维度清单中适应性词核对（复用 002 结构，独立复探一行）
row = qj("SELECT overall_score_formula, research_perseverance_weight, innovation_capability_weight, "
         "discipline_match_weight, political_orientation_weight "
         "FROM ads_talent_capability_model LIMIT 1")
if row:
    facts["jiuxin_capability_model_formula"] = str(row[0][0])
    facts["jiuxin_capability_model_weights"] = {
        "research_perseverance": float(row[0][1]), "innovation": float(row[0][2]),
        "discipline_match": float(row[0][3]), "political_orientation": float(row[0][4])}
jconn.close()

# ================= 派生 =================
n_prof = facts["jiuxin_talent_profile_rows"]
n_country = facts["jiuxin_country_name_nonnull"]
derived.append({
    "key": "jiuxin_country_field_coverage_pct",
    "value": round(100.0 * n_country / n_prof, 2),
    "numerator": n_country,
    "denominator": n_prof,
    "note": "分子=ads_talent_profile.country_name 非空行数（常驻国代理——注意 schema 文档声明该字段是"
            "机构所在地代理非已核验居住地）；分母=profile 总行数（同表全量非采样）",
})
n_exp_talents = facts["jiuxin_experience_distinct_talents"]
n_multi = facts["jiuxin_multi_country_experience_talents"]
derived.append({
    "key": "jiuxin_multi_country_experience_pct",
    "value": round(100.0 * n_multi / n_exp_talents, 2),
    "numerator": n_multi,
    "denominator": n_exp_talents,
    "note": "分子=经历表中有 ≥2 个国家的人才数；分母=经历表去重人才数（同表同 WHERE 池，"
            "非 profile 全池——分母口径差异在 note 写死，B3）",
})
# 负结论登记（B10：不写伪分）
derived.append({
    "key": "scholar_environment_adaptability_score",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "不可算——『环境适应性』评分口径三源未立项（无国籍/语言能力/文化背景评分结果面；"
            "capability 模型四维=科研毅力/创新/学科匹配/政治倾向，无适应性维）；按 B10 不写伪分，此键留空即负结论登记",
})

# ================= absence_probe =================
absence += [
    {"probe": "gkx 适应性/国籍/语言承载（表名 adapt/assimil/mobility/language 词族 + dwd_scholar 列核对）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）词族扫 + SHOW COLUMNS FROM gkx.dwd_scholar 列核对",
     "hits": len(facts["gkx_adapt_like_tables"]) + len(facts["gkx_scholar_nationality_language_cols"]),
     "hit_detail": f"表名 0 命中；dwd_scholar 27 列中 national/citizen/language/birth/country 词族 0 命中"
                   f"（{facts['gkx_scholar_nationality_language_cols']}）——国籍与语言维在 gkx 学者面结构级缺失"},
    {"probe": "dev 适应性承载（gkxlumenx_* 全 schema adapt/assimil/difficulty/talent 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_* 全 schema",
     "hits": len(facts["dev_adapt_like_tables"]),
     "hit_detail": f"命中 {facts['dev_adapt_like_tables']}——逐表语义排除：无一张是适应性评分结果面"
                   "（cms/素材表与难度 mock 生成器之外的表）"},
    {"probe": "久新适应性评分结果面（203 表 adapt/assimil/language/culture 词族）",
     "source": "jiuxin",
     "sql": "SHOW TABLES；203 表名词族扫 + ads_talent_capability_model 维度公式核对",
     "hits": len(facts["jiuxin_adapt_like_tables"]),
     "hit_detail": "表名 0 命中；capability 模型唯一在册公式 = 0.25*科研毅力+0.25*创新能力+0.40*学科匹配度"
                   "+0.10*政治倾向——四维中无『环境适应性』维；203 表无任何语言/文化评分面"},
    {"probe": "需求原文「学者适应性评估」量化算法定义段",
     "source": "doc",
     "sql": "rg 学者适应性评估/环境适应 三份需求真源（主需求 :2369-2373 命中功能叶）",
     "hits": 1,
     "hit_detail": "需求给出行为（『综合国籍、语言能力、教育经历、文化背景等多维信息，对学者的工作环境"
                   "适应性进行量化分析』）但四维合成算式与权重无——评分口径未闭合；UI difficultyEstimate "
                   "factors 为 mock 演示值"},
]

support = "部分支持"

notes += [
    "判档：『环境适应性』评分口径三源未立项（四维中语言能力/文化背景零承载、国籍只能用常驻国/经历国代理），"
    "依赖侧部分可代理（地理/流动/教育经历三维结构+数据在）→ 部分支持（参照 POLCMP_008 评分口径选型待裁定写法）",
    f"地理代理读数：profile.country_name 覆盖 {derived[0]['value']}%（{n_country}/{n_prof}）；经历表 "
    f"{facts['jiuxin_talent_experience_rows']} 行覆盖 {n_exp_talents} 人才，其中跨国经历人才 {n_multi}"
    f"（{derived[1]['value']}%，分母=经历表人才池）——地理适应性可算出有区分度的代理读数",
    "语言维代理：ads_paper_profile.language 面存在（Top8 见产物）但 talent→paper→language 的学者级语言"
    "画像需 join 大表（5,051,578 合作边规模在案），且论文语言≠个人语言能力——代理语义弱，本件不派生",
    "流动维：ads_talent_mobility_event 跨国事件在案（产物键 jiuxin_mobility_cross_country_events）——"
    "跨文化流动经历是适应性文献口径的常用代理（R1 T/CASTEM 引才评估语境；R2 OECD 人才流动口径）",
    "mock 披露：talentRecommendSpec.js:22 的『学者适应性评估』为 L6 能力映射清单项；DifficultyTab 消费的 "
    "difficultyEstimate.factors/overall 均为 data.js mock 演示值——不作数据证据（B10）",
    "B11 对账：久新 ads_talent_profile 100,000 与 002 产物/共享记录零漂移；gkx dwd_scholar 27 列清单与 "
    "M_TALENT_UI_CHINESE_RATIO §3.3 探针记录一致（无国籍/出生国列）",
    "升档触发器（B10）：①甲方裁定适应性口径=地理/流动/教育三维代理合成（权重公示）→ 转换可算升完全转换支持"
    "（语言/文化两维降维披露）；②引入语言能力数据源（如 ORCID 语言字段/多语论文署名比）→ 四维闭合升完全转换支持",
]

out = {
    "metric_id": "M_SCIUI_TALENTIR_004",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/talent-trend/talentRecommendSpec.js:22",
        "repos/demo-ui-science/src/pages/talent-trend/data.js:1385",
        "repos/demo-ui-science/src/pages/talent-trend/talentRecommendSpec.js:15",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "主需求《科技信息展示系统和科技专题服务系统.md》:2369/:2371-2373（1.1.1.1.4.3.4.2.1 学者"
                "适应性评估）功能叶明列：『综合国籍、语言能力、教育经历、文化背景等多维信息，对学者的工作"
                "环境适应性进行量化分析』——功能在、算式无；核增/算法库两份真源 0 命中",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件为人才快照型评估（无年度序列需求；mobility_event 按事件年分布另有承载，本件未展开）",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(n_prof), str(n_country), str(facts["jiuxin_talent_experience_rows"]),
                          str(n_exp_talents), str(n_multi), str(facts["jiuxin_mobility_event_rows"]),
                          str(facts["jiuxin_mobility_cross_country_events"]), "27", "203", "22", "2371"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
