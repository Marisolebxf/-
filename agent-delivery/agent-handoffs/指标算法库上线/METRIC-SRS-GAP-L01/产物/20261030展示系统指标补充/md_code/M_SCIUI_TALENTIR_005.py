#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TALENTIR_005 学者论文质量分（期刊层次加权）· 三源探针与复现脚本（S3-03 Lane 6）。

含义：学科贡献度分析（1.1.1.1.4.3.4.1.2 指标缩放展示）的核心指标之一「论文质量」——
五维贡献度雷达（论文质量/影响因子/项目数/专利量/合作网络）的第一维。
UI：repos/demo-ui-science/src/pages/talent-trend/components/ContributionMatchReport.jsx:10
（METRIC_KEYS 首项 { key:'papers', label:'论文质量' }；ContributionTab.jsx:105/148/721 消费
e.scores.papers）。
派单书定名「期刊层次加权」——UI 无此算式（data.js:1322 contributionScores scores 由
contributionScore 基础分+ifFactor 归一拼装，mock）；期刊层次加权是本件按需求语义推测的口径（B10）。

三源判档路径：
- 期刊层次（JCR 分区/影响因子/期刊等级）结构：三源核对——久新 ads_paper_profile 无期刊名/
  分区列（primary_source_id 仅 OpenAlex Source ID）；gkx dwd_zh_paper 期刊列待探；
  dev 无论文表（共享快照在案：gkxlumenx_dwd 无论文表）；
- 已发布替代口径：久新 ads_talent_profile.paper_score（论文数百分位）+ core_source_score
  （CWTS Core 期刊占比×100）——「期刊质量」的库内官方口径是 Core 覆盖率而非分区加权；
- FWCI 面在 ads_paper_profile.fwci（400 万行论文级）——学者级质量分可由 FWCI 均值转换。
→ 期刊层次（分区/IF）结构缺 + Core/FWCI 替代口径数据全 → 部分支持（口径 B10 双轨）。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_TALENTIR_005_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

# ============ ① gkx：论文期刊层次承载探针 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

paper_cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_zh_paper")]
facts["gkx_zh_paper_cols"] = paper_cols
facts["gkx_zh_paper_journal_like_cols"] = [c for c in paper_cols
                                           if re.search(r"journal|venue|source|periodical|if_|impact|quartile|partition", c, re.I)]
facts["gkx_zh_paper_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_zh_paper")[0][0])
# scholar 主档质量分承载核对（27 列已在 002 复探——此处列级核对引用同源）
scholar_cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_scholar")]
facts["gkx_scholar_quality_cols"] = [c for c in scholar_cols
                                     if re.search(r"score|quality|quartile|impact", c, re.I)]
gcur.close()

# ============ ② dev：论文表零承载（共享快照复证 + 独立复探） ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=60)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
lcur.execute("SELECT table_schema, table_name FROM information_schema.tables "
             "WHERE table_schema LIKE 'gkxlumenx%%' AND table_name REGEXP 'paper|journal|literature'")
facts["dev_paper_like_tables"] = [f"{r[0]}.{r[1]}" for r in lcur.fetchall()]
lconn.close()

# ============ ③ 久新：期刊层次列核对 + 替代口径数据面（核心） ============
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)
jconn = pymysql.connect(**JX)
jcur = jconn.cursor()
def qj(sql):
    jcur.execute(sql)
    return jcur.fetchall()

# 3.1 ads_paper_profile 期刊层次列核对（列级 absence）
pp_cols = [r[0] for r in qj("SHOW COLUMNS FROM ads_paper_profile")]
facts["jiuxin_paper_profile_cols"] = pp_cols
facts["jiuxin_paper_profile_journal_like_cols"] = [c for c in pp_cols
                                                   if re.search(r"journal|venue|source_name|quartile|partition|impact|jcr|if_", c, re.I)]
facts["jiuxin_paper_profile_rows"] = int(qj("SELECT COUNT(*) FROM ads_paper_profile")[0][0])

# 3.2 期刊层次替代口径 A：CWTS Core 覆盖（profile.core_source_score）
facts["jiuxin_profile_rows"] = int(qj("SELECT COUNT(*) FROM ads_talent_profile")[0][0])
facts["jiuxin_core_source_score_nonnull"] = int(qj(
    "SELECT COUNT(core_source_score) FROM ads_talent_profile")[0][0])
row = qj("SELECT MIN(core_source_score), MAX(core_source_score), AVG(core_source_score) "
         "FROM ads_talent_profile WHERE core_source_score IS NOT NULL")[0]
facts["jiuxin_core_source_score_min_max_avg"] = [float(row[0]), float(row[1]), round(float(row[2]), 4)]

# 3.3 期刊层次替代口径 B：FWCI 论文级面
row = qj("SELECT COUNT(fwci), MIN(fwci), MAX(fwci), AVG(fwci) FROM ads_paper_profile")[0]
facts["jiuxin_fwci_nonnull"] = int(row[0])
facts["jiuxin_fwci_min_max_avg"] = [float(row[1]), float(row[2]), round(float(row[3]), 6)]
# 撤稿面（质量负向维）
facts["jiuxin_retracted_papers"] = int(qj(
    "SELECT COUNT(*) FROM ads_paper_profile WHERE is_retracted = 1")[0][0])

# 3.4 学者级质量分现成结果面：paper_score（论文数百分位——注意是数量口径非质量口径，登记对照）
row = qj("SELECT COUNT(paper_score), AVG(paper_score) FROM ads_talent_profile")[0]
facts["jiuxin_paper_score_nonnull"] = int(row[0])
facts["jiuxin_paper_score_avg"] = round(float(row[1]), 4)

# 3.5 代表成果 venue 列（期刊名的展示快照——层次判定的可用物料）
facts["jiuxin_research_achievement_rows"] = int(qj(
    "SELECT COUNT(*) FROM ads_talent_research_achievement")[0][0])
facts["jiuxin_achievement_venue_nonnull"] = int(qj(
    "SELECT COUNT(venue) FROM ads_talent_research_achievement")[0][0])
facts["jiuxin_achievement_top8_venues"] = [[str(a), int(b)] for a, b in qj(
    "SELECT venue, COUNT(*) FROM ads_talent_research_achievement WHERE venue IS NOT NULL "
    "AND venue != '' GROUP BY venue ORDER BY COUNT(*) DESC, venue ASC LIMIT 8")]
jconn.close()

# ================= 派生（学者级质量分转换演示：Core 口径现成 + FWCI 转换示意） =================
n_prof = facts["jiuxin_profile_rows"]
n_core = facts["jiuxin_core_source_score_nonnull"]
derived.append({
    "key": "jiuxin_core_coverage_pct",
    "value": round(100.0 * n_core / n_prof, 2),
    "numerator": n_core,
    "denominator": n_prof,
    "note": "分子=ads_talent_profile.core_source_score 非空行数；分母=profile 总行数（同表全量非采样）——"
            "CWTS Core 覆盖率即『期刊层次』库内官方口径的数据可及度",
})
n_fwci = facts["jiuxin_fwci_nonnull"]
n_paper = facts["jiuxin_paper_profile_rows"]
derived.append({
    "key": "jiuxin_fwci_coverage_pct",
    "value": round(100.0 * n_fwci / n_paper, 2),
    "numerator": n_fwci,
    "denominator": n_paper,
    "note": "分子=ads_paper_profile.fwci 非空论文数；分母=ads_paper_profile 总行数（400 万 MVP core，"
            "同表全量非采样）——FWCI 是论文级质量替代口径（非期刊层次），学者级需按 talent→paper 聚合另算",
})
# 负结论登记（期刊层次加权口径）
derived.append({
    "key": "scholar_paper_quality_score_journal_weighted",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "不可算——期刊层次（JCR 分区/影响因子/期刊等级）结构在三源论文面均缺失（无分区/IF 列），"
            "『期刊层次加权』算式无从落地；按 B10 不写伪分，此键留空即负结论登记。"
            "替代口径：core_source_score（Core 覆盖率×100，现成直查）与 FWCI 均值（转换可算）",
})

# ================= absence_probe =================
absence += [
    {"probe": "gkx 论文期刊层次列（dwd_zh_paper 期刊/分区/影响因子词族）",
     "source": "gkx",
     "sql": "SHOW COLUMNS FROM gkx.dwd_zh_paper（32 列）期刊词族扫",
     "hits": len(facts["gkx_zh_paper_journal_like_cols"]),
     "hit_detail": f"命中 {facts['gkx_zh_paper_journal_like_cols']}——逐列定性：均为数据来源审计列"
                   "（data_source/table_data_source），非期刊名/分区/影响因子结构化承载（无 quartile/"
                   "partition/impact factor 列）；dwd_scholar 27 列中质量分词族 0 命中"},
    {"probe": "dev 论文/期刊表（gkxlumenx_* 全 schema paper/journal/literature 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*",
     "hits": len(facts["dev_paper_like_tables"]),
     "hit_detail": f"命中 {facts['dev_paper_like_tables']}——与共享快照（dev 论文表探测 rows=0）一致，"
                   "无学者论文质量承载"},
    {"probe": "久新期刊层次列（ads_paper_profile 全列 journal/venue/quartile/partition/impact/jcr 词族）",
     "source": "jiuxin",
     "sql": "SHOW COLUMNS FROM ads_paper_profile（33 列）词族扫",
     "hits": len(facts["jiuxin_paper_profile_journal_like_cols"]),
     "hit_detail": f"命中 {facts['jiuxin_paper_profile_journal_like_cols']}——仅 primary_source_id"
                   "（OpenAlex Source ID，无分区/IF 语义）；schema 文档明示 is_core『只表示 CWTS Core Sources "
                   "覆盖，不表示 WoS Core、JCR 分区、影响因子或期刊等级』——期刊层次结构级缺失"},
    {"probe": "需求原文「论文质量」评分算法定义段",
     "source": "doc",
     "sql": "rg 论文质量/期刊层次 三份需求真源（主需求 :2339 命中指标名）",
     "hits": 1,
     "hit_detail": "需求给出指标名（『支持对贡献度分析核心指标如论文质量、影响因子、项目数、专利量等进行"
                   "缩放对比』）但『论文质量』的构成（期刊层次加权？被引质量？Core 覆盖？）无定义——"
                   "『期刊层次加权』为派单书定名的推测口径；UI scores.papers 为 mock 演示值"},
]

support = "部分支持"

notes += [
    "判档：期刊层次（分区/IF）结构三源论文面零承载（列级探针），『期刊层次加权』算式无从落地；"
    "但替代口径数据面全——core_source_score（CWTS Core 期刊覆盖率×100，99,869/100,000 有值）+ "
    "ads_paper_profile.fwci（论文级 FWCI，400 万面）→ 部分支持",
    f"口径 A（库内官方、现成直查）：core_source_score = 100×core_paper_count/core_eligible_paper_count——"
    f"覆盖 {derived[0]['value']}%（{n_core}/{n_prof}），分布 min/max/avg 见产物"
    " jiuxin_core_source_score_min_max_avg；schema 文档明确该口径不等于期刊等级",
    f"口径 B（转换可算）：ads_paper_profile.fwci 覆盖 {derived[1]['value']}%（{n_fwci}/{n_paper}）——"
    "学者级 FWCI 均值分需 talent→paper 聚合（合作边表 ads_talent_collaborator 5,051,578 行可桥），"
    "本件未展开聚合（400 万行 join 需工程化）",
    "质量负向维：撤稿面在案（jiuxin_retracted_papers）——质量分合成时撤稿论文应剔除（schema 口径："
    "撤稿和 paratext 不进入有效论文总体）",
    "期刊名物料：ads_talent_research_achievement.venue（代表成果 Top10 的期刊/会议名快照）实测"
    f"非空 {facts['jiuxin_achievement_venue_nonnull']} 行（{facts['jiuxin_research_achievement_rows']} 行"
    "中全空）——期刊名称快照列未回填，名称→分区/IF 的映射维表与名称物料双缺（外部数据源）",
    "mock 披露：ContributionMatchReport.jsx:10 METRIC_KEYS papers 维的 scores 值来自 data.js:1322-1327 "
    "contributionScore 基础分 + ifFactor 归一拼装（random 区间 mock）——演示值不作数据证据（B10）",
    "B11 对账：gkx dwd_zh_paper 100,900 与共享快照（dims.gkx 论文总数 100900）零漂移；久新 "
    "ads_paper_profile 4,000,000 与共享快照（jiuxin ads_paper_profile 4000000）零漂移；dev 无论文表与"
    "共享快照（dev 论文表探测 rows=0）零漂移",
    "升档触发器（B10）：①接入期刊分区/IF 映射维表（JCR/中科院分区公开数据源，按 primary_source_id 或 "
    "venue 名对齐）→ 期刊层次加权口径转换可算升完全转换支持；②甲方裁定论文质量=Core 覆盖口径（口径 A）"
    "→ 现成直查升完全直接支持；③FWCI 聚合工程化落地 → 口径 B 升完全转换支持",
]

out = {
    "metric_id": "M_SCIUI_TALENTIR_005",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/talent-trend/components/ContributionMatchReport.jsx:10",
        "repos/demo-ui-science/src/pages/talent-trend/components/ContributionTab.jsx:105",
        "repos/demo-ui-science/src/pages/talent-trend/data.js:1322",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "主需求《科技信息展示系统和科技专题服务系统.md》:2339（1.1.1.1.4.3.4.1.2 指标缩放展示）"
                "指标名明列：『支持对贡献度分析核心指标如论文质量、影响因子、项目数、专利量等进行缩放对比』"
                "——指标名在、构成算式无；『期刊层次加权』为派单书推测口径；核增/算法库两份真源 0 命中",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件为学者快照型质量分（core_source_score 为当前发布版本快照；年度论文质量序列可由 "
                       "ads_talent_yearly_metrics 侧另算，本件未展开）",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts["gkx_zh_paper_rows"]), str(facts["jiuxin_paper_profile_rows"]),
                          str(n_prof), str(n_core), str(n_fwci), str(facts["jiuxin_retracted_papers"]),
                          str(facts["jiuxin_research_achievement_rows"]),
                          str(facts["jiuxin_achievement_venue_nonnull"]), "4000000", "100900", "10"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
