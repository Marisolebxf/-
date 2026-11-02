#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TALENTPF_003 学者研究方向总体分布（领域构成） · 三源探针与复现脚本（S3-03 Lane 5）。

含义：重点科技人才画像·研究领域图谱（1.1.1.1.4.3.3.6）的「学者研究方向总体分布」——
UI 上是 ProfileFieldMapPanel 顶部 DRILL_LEVELS 第一级「总体方向」（overview）+
主题演化面积图的堆叠形态：按领域（label）堆叠各年份 count，构成学者研究方向的全景构成。
UI：repos/demo-ui-science/src/pages/talent-trend/components/ProfileFieldMapPanel.jsx:9（DRILL_LEVELS[0]）。
数值语义源：data.js:904-908 researchEvolution（fields × 2020-2026 年 × random count mock）。

SRS 溯源：主需求 :2241-2251 研究领域图谱（.6.1 研究领域分层展示(1) 多级展开：
「支持从专家总体研究方向逐级深入细分学科领域、核心关键词及不同阶段关注点」）——
「总体研究方向」需求明列，本件=其分布/构成面。「领域构成」作为定名 0 命中。

三源判档路径（领域分布主战场走久新学科面）：
- 层级体系：OpenAlex 四级 domain→field→subfield→topic（久新 ads_discipline_* 维表），
  capability/potential 主领域 + yearly_discipline（talent×year×field 聚合面）双承载
  （ads_talent_profile 无 primary_field_id——主领域在 capability_assessment/potential_result）；
- 总体分布双口径：口径 A=人才×Field 去重构成（yearly_discipline 按 field 计数）；
  口径 B=Primary Field 构成（每人才每年唯一主领域，is_primary_discipline=1）——两口径读数均现转；
- gkx 零承载：dwd_scholar 无 field 列（27 列词族 0 命中）、dwd_scholar_papers 无 field 列、
  talent×field 词族表 0；
- dev 零承载：talent/field 词族表仅代码生成器元数据表（gen_field_type），非业务面。
→ 领域构成结构+数据双达标（久新）+ 维表映射完整 → 完全转换支持（无现成「构成分布」结果面，
   一条 GROUP BY 即得；gkx/dev 无承载不影响——三源中久新即数据源）。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_TALENTPF_003_out.json")
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

# ---------- ① 学科维表（OpenAlex 四级） ----------
for t in ["ads_discipline_domain", "ads_discipline_field", "ads_discipline_subfield", "ads_discipline_topic"]:
    if t in jx_tables:
        facts[f"jiuxin_{t}_rows"] = int(qj(f"SELECT COUNT(*) FROM {t}")[0][0])
# field 维表样例（分布读数的领域名物料）
rows = qj("SELECT field_id, name_zh, name_en FROM ads_discipline_field ORDER BY field_id ASC LIMIT 5")
facts["jiuxin_field_dim_sample5"] = [[str(a), str(b), str(c)] for a, b, c in rows]

# ---------- ② 主领域构成（口径 B：人才级 Primary Field，承载面=potential_result） ----------
# 注：ads_talent_profile 无 primary_field_id——人才级主领域承载在 ads_talent_potential_result
# （fld_* 哈希 ID，与 yearly_discipline.field_id 同 ID 体系可直接 JOIN）
prof_cols = [r[0] for r in qj("DESC ads_talent_profile")]
facts["jiuxin_profile_rows"] = int(qj("SELECT COUNT(*) FROM ads_talent_profile")[0][0])
facts["jiuxin_profile_primary_field_id_nonnull"] = 0  # 实测列不存在，登记 0 并在 note 披露
facts["jiuxin_potential_result_rows"] = int(
    qj("SELECT COUNT(*) FROM ads_talent_potential_result")[0][0])
facts["jiuxin_potential_pf_nonnull"] = int(
    qj("SELECT COUNT(primary_field_id) FROM ads_talent_potential_result")[0][0])
rows = qj("SELECT p.primary_field_id, f.name_zh, COUNT(*) FROM ads_talent_potential_result p "
          "LEFT JOIN ads_discipline_field f ON f.field_id = p.primary_field_id "
          "WHERE p.primary_field_id IS NOT NULL "
          "GROUP BY p.primary_field_id, f.name_zh ORDER BY COUNT(*) DESC, p.primary_field_id ASC LIMIT 12")
facts["jiuxin_potential_primary_field_top12"] = [[str(a), str(b), int(c)] for a, b, c in rows]

# ---------- ③ yearly_discipline 年度面（口径 A：人才×年×Field 构成 + 主题演化图数据源） ----------
facts["jiuxin_yearly_discipline_rows"] = int(
    qj("SELECT COUNT(*) FROM ads_talent_yearly_discipline")[0][0])
facts["jiuxin_yearly_discipline_talents"] = int(
    qj("SELECT COUNT(DISTINCT talent_id) FROM ads_talent_yearly_discipline")[0][0])
facts["jiuxin_yearly_discipline_years"] = [int(r[0]) for r in qj(
    "SELECT statistics_year FROM ads_talent_yearly_discipline GROUP BY statistics_year ORDER BY statistics_year")]
# 口径 A 分布（人才×Field 去重行）
rows = qj("SELECT field_id, COUNT(*) FROM ads_talent_yearly_discipline GROUP BY field_id "
          "ORDER BY COUNT(*) DESC, field_id ASC LIMIT 12")
facts["jiuxin_yd_talentyear_by_field_top12"] = [[str(a), int(b)] for a, b in rows]
# 口径 B 分布（Primary Field 年度形态）
rows = qj("SELECT field_id, COUNT(*) FROM ads_talent_yearly_discipline "
          "WHERE is_primary_discipline = 1 GROUP BY field_id ORDER BY COUNT(*) DESC, field_id ASC LIMIT 12")
facts["jiuxin_yd_primary_by_field_top12"] = [[str(a), int(b)] for a, b in rows]
# 2025 完整年切片（演化面积图的最近完整年）
rows = qj("SELECT field_id, SUM(paper_count), SUM(cited_by_count) FROM ads_talent_yearly_discipline "
          "WHERE statistics_year = 2025 GROUP BY field_id ORDER BY SUM(paper_count) DESC, field_id ASC LIMIT 12")
facts["jiuxin_yd_2025_field_papers_cites_top12"] = [[str(a), int(b), int(c)] for a, b, c in rows]
facts["jiuxin_yd_2025_rows"] = int(
    qj("SELECT COUNT(*) FROM ads_talent_yearly_discipline WHERE statistics_year = 2025")[0][0])

# ---------- ④ topic_profile（更细粒度构成的可选面） ----------
if "ads_talent_topic_profile" in jx_tables:
    facts["jiuxin_topic_profile_rows"] = int(qj("SELECT COUNT(*) FROM ads_talent_topic_profile")[0][0])
    facts["jiuxin_topic_profile_talents"] = int(
        qj("SELECT COUNT(DISTINCT talent_id) FROM ads_talent_topic_profile")[0][0])
jconn.close()

# ---------- ⑤ gkx：学者领域承载探针 ----------
gcur = gkx()
gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
facts["gkx_talent_field_like_tables"] = [t for t in gkx_tables
                                         if re.search(r"scholar.*(field|keyword|topic|discipline)|"
                                                      "(field|keyword|topic|discipline).*scholar", t, re.I)]
gcur.execute("SHOW COLUMNS FROM gkx.dwd_scholar")
scholar_cols = [r[0] for r in gcur.fetchall()]
facts["gkx_scholar_field_like_cols"] = [c for c in scholar_cols
                                        if re.search(r"field|discipline|topic|keyword|direction", c, re.I)]
gcur.execute("SHOW COLUMNS FROM gkx.dwd_scholar_papers")
sp_cols = [r[0] for r in gcur.fetchall()]
facts["gkx_scholar_papers_field_like_cols"] = [c for c in sp_cols
                                               if re.search(r"field|keyword|topic", c, re.I)]
gcur.close()

# ---------- ⑥ dev：领域承载探针 ----------
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
lcur.execute("SELECT table_schema, table_name FROM information_schema.tables "
             "WHERE table_schema LIKE 'gkxlumenx%%' AND table_name REGEXP 'field|keyword|topic|discipline'")
facts["dev_field_like_tables"] = [f"{r[0]}.{r[1]}" for r in lcur.fetchall()]
lconn.close()

# ================= 派生 =================
# 口径 B 覆盖率（承载面=potential_result.primary_field_id）
n_pf = facts["jiuxin_potential_pf_nonnull"]
n_pr = facts["jiuxin_potential_result_rows"]
derived.append({
    "key": "jiuxin_primary_field_coverage_pct",
    "value": round(100.0 * n_pf / n_pr, 2),
    "numerator": n_pf,
    "denominator": n_pr,
    "note": "分子=ads_talent_potential_result.primary_field_id 非空行数；分母=该表总行数（同表全量非采样）——"
            "主领域构成的覆盖率（profile 表无 primary_field_id，人才级主领域承载在 potential_result）",
})
# 口径 A Top1 领域占比（构成读数样例）
ta = facts["jiuxin_yd_talentyear_by_field_top12"]
tot_a = sum(int(x[1]) for x in ta)
# 全量分母（非仅 Top12）：talent×year×field 总行数
tot_all = facts["jiuxin_yearly_discipline_rows"]
top1 = int(ta[0][1]) if ta else 0
derived.append({
    "key": "jiuxin_yd_top1_field_share_pct",
    "value": round(100.0 * top1 / tot_all, 2),
    "numerator": top1,
    "denominator": tot_all,
    "note": "分子=口径 A（人才×年×Field 行）Top1 领域行数；分母=ads_talent_yearly_discipline 总行数"
            "（同表全量非采样）——领域构成的头部集中度",
})
# 口径 B Top1 占比
tb = facts["jiuxin_yd_primary_by_field_top12"]
top1b = int(tb[0][1]) if tb else 0
derived.append({
    "key": "jiuxin_yd_primary_top1_field_share_pct",
    "value": round(100.0 * top1b / tot_all, 2),
    "numerator": top1b,
    "denominator": tot_all,
    "note": "分子=口径 B（is_primary_discipline=1）Top1 领域行数；分母=ads_talent_yearly_discipline 总行数"
            "（同表全量非采样）——主领域构成的头部集中度（与口径 A 同分母可对比）",
})

# ================= absence_probe =================
absence.extend([
    {"probe": "gkx 280 表 scholar×field/keyword/topic/discipline 交叉词族 + dwd_scholar/dwd_scholar_papers 列级",
     "source": "gkx", "sql": "SHOW TABLES FROM gkx 后词族扫 + SHOW COLUMNS 逐列扫",
     "hits": 0, "hit_detail": "命中 []（表级+两表列级三零）——gkx 学者主档与论文归属表均无学科/领域/"
            "关键词结构化列；学者领域分布需从论文文本（zh_abstract/en_abstract）自建分类，属重工程非现成"},
    {"probe": "dev gkxlumenx_* field/keyword/topic/discipline 词族",
     "source": "dev", "sql": "information_schema.tables 扫 gkxlumenx_*",
     "hits": 4, "hit_detail": "命中 gkxlumenx_ads.topic_burst（主题突发检测面）/ gkxlumenx_dwd."
            "industry_analysis_topics（产业分析主题）/ jimu_report_db_field / gen_field_type（报表与"
            "代码生成器元数据）——前两者为主题级非学者领域面且无人才绑定，后两者为元数据表；均不构成本件承载"},
    {"probe": "需求原文「领域构成/研究方向总体分布」算式",
     "source": "doc", "sql": "rg 总体研究方向/领域构成/研究方向总体分布 三份需求真源",
     "hits": 1, "hit_detail": "「领域构成」定名 0 命中；最近义 :2251 多级展开『支持从专家总体研究方向逐级"
            "深入细分学科领域…』+ :2241『精准提取专家在不同时期关注的关键词、主题领域以及学科交叉点』——"
            "分布/构成行为在（分层展示+分布格局），构成算式（按论文数还是按人才数）无定义，本件双口径并列"},
])

notes.extend([
    "本件支持度按三源评估（20261101 铁律）：dev live 非 demo + gkx 只读 + 久新 ads_* 只读。",
    "领域体系=OpenAlex 四级（domain→field→subfield→topic），久新维表与事实面双在："
    "potential_result.primary_field_id（人才级主领域，fld_* 哈希 ID 与 yearly_discipline 同体系）"
    "+ yearly_discipline（talent×year×field 年度聚合面）；ads_talent_profile 无 primary_field_id。",
    "构成双口径：口径 A=人才×年×Field 去重行构成（演化面积图数据源）；口径 B=Primary Field 构成"
    "（每人才每年唯一主领域，is_primary_discipline=1，schema 明载按 paper_count DESC 确定唯一）——"
    "两口径并列交付，构成算式选型留给口径裁定（B10）。",
    "yearly_discipline 年份含 2026（PARTIAL_YEAR，schema 明示只用于展示不与 2025 形成正式领域迁移事件）——"
    "构成读数按 2025 完整年切片（facts.jiuxin_yd_2025_field_papers_cites_top12）。",
    "与同批 X_015 件对账：subfield 维 252 个（OpenAlex 254 减冻结 2，X_015 读数在案）——本件 field 级"
    "读数与该 subfield 级读数同体系不同层，零漂移。",
    "UI researchEvolution（fields×2020-2026×random count）为 mock 演示值，不作数据证据。",
])

out = {
    "metric_id": "M_SCIUI_TALENTPF_003",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/talent-trend/components/ProfileFieldMapPanel.jsx:9（DRILL_LEVELS[0] overview 总体方向）",
        "repos/demo-ui-science/src/pages/talent-trend/components/ProfileFieldMapPanel.jsx:92-113（areaOption 堆叠面积图按 label 堆叠各年 count）",
        "repos/demo-ui-science/src/pages/talent-trend/data.js:904-908（researchEvolution mock 生成器）",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "需求明列行为：主需求 :2251（1.1.1.1.4.3.3.6.1(1) 多级展开）『支持从专家总体研究方向逐级深入"
                "细分学科领域、核心关键词及不同阶段关注点』+ :2241 领域图谱总述『精准提取专家在不同时期"
                "关注的…主题领域』——「总体研究方向」明列；「领域构成」为派单书定名的构成面口径；核增/算法库 0 命中",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": "完全转换支持",
    "notes": notes,
    "base_years_used": [2025],
    "base_years_missing": [],
    "base_years_note": "构成读数按 2025 完整年切片；2026 为 PARTIAL_YEAR（schema 口径只展示不入正式对比）；"
                       "年度演化序列年份范围见 facts.jiuxin_yearly_discipline_years",
    "ctx_refs": {
        "note": "正文引用型数字登记",
        "refs": [],
    },
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1, default=str)
print("ok ->", OUT)
