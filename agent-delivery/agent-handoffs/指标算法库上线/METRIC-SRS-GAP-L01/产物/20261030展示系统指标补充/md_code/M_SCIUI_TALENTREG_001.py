#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TALENTREG_001 代表性成果（卡片式统计） · 三源探针与复现脚本（S3-03 Lane 5）。

含义：重点科技人才画像·基础画像（信息展示方式→卡片式展示，1.1.1.1.4.3.3.1.1(3)）的
「代表性成果（卡片式统计）」卡——论文/著作/专利/科研项目四 StatCard
（各带 total + 被引/授权/经费 sub）+ 代表成果卡片列表（title/venue/year/citations）。
UI：repos/demo-ui-science/src/pages/talent-trend/components/ProfileBasicPanel.jsx:301-347。
数值语义源：data.js:828-866（papers/books/patents/projects 全 random mock）。

SRS 溯源：主需求 :1895-1907 信息展示方式（卡片式展示「结构化卡片形式呈现，美观直观，便于快速浏览与对比」）
+ :1463/:2271 代表性成果展示语境；「代表性成果（卡片式统计）」卡片名本身 0 命中（UI 拆件）。

三源判档路径：
- 核心承载在久新：ads_talent_research_achievement（代表成果 Top10 快照面 902,667 行——
  schema 文档明载「每名人才按 cited_by_count DESC... 取 Top 10」确定性排序）——
  实测 achievement_type 仅 paper 一种（902,667 行），patent/project/award 型 0 行；
- 论文/专利/被引计数腿：ads_talent_profile.paper_count/citations_count/h_index/patent_grant_count
  现成直查；项目腿：ads_talent_project 关联面 7,702,366 行（与 profile.project_count 同读数互证）；
- 「著作」卡三源零承载：jiuxin book 词族表 0 + profile book 词族列 0 + gkx 无论文-书型区分
  （dwd_scholar 无 book 列；OpenAlex 体系 book/book-chapter 属 work type，久新 paper_profile 未区分类型）；
- 「国家级/国际」与「经费万元」结构三源无（Grant 维度未发布；talent_project 仅关系面无分级/经费列）。
→ 三腿现成（论文/专利/代表成果卡）+ 项目腿存在性在 + 著作腿零承载 → 部分支持（口径 A 论文专利代表作可交付）。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_TALENTREG_001_out.json")
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


jcur.execute("SHOW TABLES")
jx_tables = sorted(r[0] for r in jcur.fetchall())
facts["jiuxin_table_count"] = len(jx_tables)

# ---------- ① 代表成果快照面（核心承载） ----------
facts["jiuxin_research_achievement_rows"] = int(
    qj("SELECT COUNT(*) FROM ads_talent_research_achievement")[0][0])
facts["jiuxin_achievement_talents"] = int(
    qj("SELECT COUNT(DISTINCT talent_id) FROM ads_talent_research_achievement")[0][0])
rows = qj("SELECT achievement_type, COUNT(*) FROM ads_talent_research_achievement "
          "GROUP BY achievement_type ORDER BY COUNT(*) DESC, achievement_type ASC")
facts["jiuxin_achievement_type_dist"] = [[str(a), int(b)] for a, b in rows]
# Top10 覆盖验证：人均成果数
derived.append({
    "key": "jiuxin_achievement_per_talent_avg",
    "value": round(facts["jiuxin_research_achievement_rows"] / facts["jiuxin_achievement_talents"], 2),
    "numerator": facts["jiuxin_research_achievement_rows"],
    "denominator": facts["jiuxin_achievement_talents"],
    "note": "分子=ads_talent_research_achievement 总行数；分母=有代表成果的人才去重数（同表同 WHERE 池）——"
            "schema 口径每人才 Top 10，人均读数应 ≈10",
})

# ---------- ② 计数腿：profile 现成列 ----------
prof_cols = [r[0] for r in qj("DESC ads_talent_profile")]
facts["jiuxin_profile_rows"] = int(qj("SELECT COUNT(*) FROM ads_talent_profile")[0][0])
for col in ["paper_count", "citations_count", "h_index", "patent_grant_count",
            "patent_family_count", "project_count"]:
    if col in prof_cols:
        n = int(qj(f"SELECT COUNT(`{col}`) FROM ads_talent_profile")[0][0])
        s = int(qj(f"SELECT COALESCE(SUM(`{col}`),0) FROM ads_talent_profile")[0][0])
        facts[f"jiuxin_profile_{col}_nonnull"] = n
        facts[f"jiuxin_profile_{col}_sum"] = s
# 著作腿排除探针（列级）
facts["jiuxin_profile_book_like_cols"] = [c for c in prof_cols if re.search(r"book|monograph", c, re.I)]

# ---------- ③ 著作腿表级排除 ----------
facts["jiuxin_book_like_tables"] = [t for t in jx_tables if re.search(r"book|monograph", t, re.I)]

# ---------- ④ 项目腿：talent_project 关联面（experience.project_ids 实测全空） ----------
if "ads_talent_project" in jx_tables:
    facts["jiuxin_talent_project_rows"] = int(qj("SELECT COUNT(*) FROM ads_talent_project")[0][0])
    facts["jiuxin_talent_project_talents"] = int(
        qj("SELECT COUNT(DISTINCT talent_id) FROM ads_talent_project")[0][0])
    rows = qj("SELECT is_lead, COUNT(*) FROM ads_talent_project GROUP BY is_lead ORDER BY is_lead")
    facts["jiuxin_talent_project_is_lead_dist"] = [[int(a) if a is not None else None, int(b)] for a, b in rows]
facts["jiuxin_experience_with_projects"] = int(
    qj("SELECT COUNT(*) FROM ads_talent_experience WHERE project_ids IS NOT NULL "
       "AND ARRAY_SIZE(project_ids) > 0")[0][0])
# project/award/patent 型成果行数（在 type_dist 已含，单独点名）
for tp in ["project", "award", "patent", "paper"]:
    n = int(qj(f"SELECT COUNT(*) FROM ads_talent_research_achievement WHERE achievement_type = '{tp}'")[0][0])
    facts[f"jiuxin_achievement_{tp}_rows"] = n
# 代表成果卡字段完整性（title/venue/year/cited_by_count 非空）
for col in ["title", "venue", "year", "cited_by_count"]:
    n = int(qj(f"SELECT COUNT(`{col}`) FROM ads_talent_research_achievement")[0][0])
    facts[f"jiuxin_achievement_{col}_nonnull"] = n
jconn.close()

# ---------- ⑤ gkx：成果承载探针 ----------
gcur = gkx()
gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
facts["gkx_achievement_like_tables"] = [t for t in gkx_tables
                                        if re.search(r"achievement|award|honor|representative", t, re.I)]
gcur.execute("SHOW COLUMNS FROM gkx.dwd_scholar")
scholar_cols = [r[0] for r in gcur.fetchall()]
facts["gkx_scholar_achievement_cols"] = [c for c in scholar_cols
                                         if re.search(r"paper|citation|h_index|patent|book|project|reference", c, re.I)]
gcur.close()

# ---------- ⑥ dev：成果承载探针 ----------
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
lcur.execute("SELECT table_schema, table_name FROM information_schema.tables "
             "WHERE table_schema LIKE 'gkxlumenx%%' AND table_name REGEXP 'achievement|award'")
facts["dev_achievement_like_tables"] = [f"{r[0]}.{r[1]}" for r in lcur.fetchall()]
lconn.close()

# ================= 派生（补：覆盖率） =================
n_paper = facts.get("jiuxin_profile_paper_count_nonnull", 0)
n_prof = facts["jiuxin_profile_rows"]
derived.append({
    "key": "jiuxin_paper_count_coverage_pct",
    "value": round(100.0 * n_paper / n_prof, 2),
    "numerator": n_paper,
    "denominator": n_prof,
    "note": "分子=ads_talent_profile.paper_count 非空行数；分母=profile 总行数（同表全量非采样）——"
            "论文计数卡的覆盖率",
})
n_ach_tal = facts["jiuxin_achievement_talents"]
derived.append({
    "key": "jiuxin_achievement_talent_coverage_pct",
    "value": round(100.0 * n_ach_tal / n_prof, 2),
    "numerator": n_ach_tal,
    "denominator": n_prof,
    "note": "分子=有代表成果快照的人才数；分母=profile 总行数（同池 100,000）——代表成果卡覆盖面",
})

# ================= absence_probe =================
absence.extend([
    {"probe": "久新实测表 book/monograph 词族（著作卡承载）",
     "source": "jiuxin", "sql": "SHOW TABLES 后词族扫 + DESC ads_talent_profile 列级词族扫",
     "hits": 0, "hit_detail": "命中 []（表级 + profile 列级双零）——著作（图书/专著）计数结构零承载；"
            "OpenAlex 体系 book/book-chapter 属 work type，久新 paper_profile 未做类型区分"},
    {"probe": "久新/需求侧「国家级/国际项目 + 经费万元」结构（科研项目卡细分）",
     "source": "jiuxin", "sql": "DESC ads_talent_project + achievement_type 枚举实测",
     "hits": 0, "hit_detail": "ads_talent_project 关联面在（7,702,366 行，relation_type/is_lead 关系列），"
            "但『国家级/国际』分级与『经费（万元）』列零承载——Grant 维度 schema 标注关联 DWD Grant，"
            "ADS 未发布分级/经费面；achievement_type 实测仅 paper（project/award/patent 型 0 行）"},
    {"probe": "gkx 280 表 achievement/award/honor/representative 词族",
     "source": "gkx", "sql": "SHOW TABLES FROM gkx 后词族扫",
     "hits": 0, "hit_detail": "命中 []——gkx 无代表成果表；dwd_scholar 仅有 paper_nums/citation_nums/"
            "h_index/reference_nums 四计数列（无 patent/book/project 列）"},
    {"probe": "dev gkxlumenx_* achievement/award 词族",
     "source": "dev", "sql": "information_schema.tables 扫 gkxlumenx_*",
     "hits": 2, "hit_detail": "命中 org_achievement_year（gkxlumenx_dwd/ods 各 1）——机构级非学者级，"
            "且为年度计数面非代表成果快照，不构成本件承载"},
    {"probe": "需求原文「代表性成果（卡片式统计）」卡片名",
     "source": "doc", "sql": "rg 代表性成果/卡片式 三份需求真源",
     "hits": 2, "hit_detail": "卡片名整体 0 命中（UI 拆件）；组件行为对应 :1905-1907 卡片式展示"
            "（『将人才信息以结构化卡片形式呈现，美观直观，便于快速浏览与对比』）+ :1463/:2271 "
            "代表性成果展示语境——展示行为在、四卡数值构成算式无"},
])

notes.extend([
    "本件支持度按三源评估（20261101 铁律）：dev live 非 demo + gkx 只读 + 久新 ads_* 只读。",
    "核心承载：ads_talent_research_achievement 902,667 行（人均 ≈10 与 schema『每人才 Top 10』口径互证）；"
    "schema 文档明载 paper 代表成果规则=按 cited_by_count DESC, publication_year DESC NULLS LAST, "
    "work_id ASC 确定性排序取 Top 10——『代表作评价制度』（R1 三评改革『推行代表作评价制度』）的库内落地件。",
    "四卡腿判定：论文卡（paper_count+citations+h_index 现成）/专利卡（patent_grant_count 现成，"
    "非空 6,490 人）/著作卡（零承载）/项目卡（talent_project 关联面在、国家级/国际分级与经费零承载）；"
    "experience.project_ids 实测全空（0 行），项目腿以 ads_talent_project 为准。",
    "venue 列 902,667 行非空 0（TALENTIR_005 件在案）——代表成果卡的 venue/年份行会缺期刊名物料，"
    "卡片渲染需回退 title+year+citations。",
    "UI 四卡数值（data.js:828-866 papers/books/patents/projects 全 random）为 mock 演示值，不作数据证据。",
    "「代表性成果」需求语义在 gkx 侧无论文-成果归属面（dwd_scholar_papers 738,106 行有归属但无代表排序）；"
    "久新是唯一现成代表成果面。",
])

out = {
    "metric_id": "M_SCIUI_TALENTREG_001",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/talent-trend/components/ProfileBasicPanel.jsx:301（InfoCard title 代表性成果（卡片式统计））",
        "repos/demo-ui-science/src/pages/talent-trend/components/ProfileBasicPanel.jsx:305-330（论文/著作/专利/科研项目四 StatCard）",
        "repos/demo-ui-science/src/pages/talent-trend/components/ProfileBasicPanel.jsx:333-346（representative 代表成果卡列表）",
        "repos/demo-ui-science/src/pages/talent-trend/data.js:828-866（papers/books/patents/projects mock 生成器）",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "卡片名「代表性成果（卡片式统计）」三份真源 0 命中（UI 拆件）；组件行为对应主需求 "
                ":1895-1907 基础画像·信息展示方式(3) 卡片式展示；「代表性成果」语义词在 :1463/:2271 "
                "（专家画像多维展示/领域节点浏览）出现——展示行为在、四卡数值构成算式无",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": "部分支持",
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件为快照型计数读数（profile 计数列与 achievement 快照均为当前发布版本），"
                       "无年度基线窗口需求",
    "ctx_refs": {
        "note": "正文引用型数字登记",
        "refs": [],
    },
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1, default=str)
print("ok ->", OUT)
