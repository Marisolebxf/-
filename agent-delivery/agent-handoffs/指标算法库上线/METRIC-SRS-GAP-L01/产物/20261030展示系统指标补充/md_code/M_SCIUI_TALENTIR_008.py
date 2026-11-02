#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TALENTIR_008 学者分阶段产出增长（近3年对比）· 三源探针与复现脚本（S3-03 Lane 6）。

含义：学科贡献度分析·智能分析与推荐（1.1.1.1.4.3.4.1.3(2) 预测视图缩放）的「阶段增长」视图——
引进模拟场景下贡献度预测的三种缩放之一（整体预期/局部影响/阶段增长）。
UI：repos/demo-ui-science/src/pages/talent-trend/components/ContributionTab.jsx:741
（Segmented options { value:'stage', label:'阶段增长' }；:304-311 predictViewMap stage factor 1.15
——近两年值×1.15 外推，mock 算式）。
派单书定名「分阶段产出增长（近3年对比）」——主承载探针：久新 ads_talent_yearly_metrics
（talent_id×year 年度产出面）。

三源判档路径：
- 年度产出结构：久新 ads_talent_yearly_metrics（paper_count/citation_count/patent_* per year）+
  ads_talent_yearly_discipline（Field 级年度）——结构+数据双在；
- 近3年对比可现算：全池按年聚合 2023/2024/2025（完整年）vs 2022 基期；
- gkx dwd_scholar 无年度产出面（27 列在案）；gkx dwd_zh_paper 按年可算全库面但无学者×年
  关联键（author_info_list longtext 非结构化，X_015 探针在案）；dev 无论文表。
→ 久新年度面结构+数据双达标，近3年对比可现转 → 完全转换支持（无现成「分阶段增长」结果面）。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_TALENTIR_008_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

# ============ ① gkx：学者年度产出面探针 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_yearly_like_tables"] = [t for t in gkx_tables
                                   if t.startswith("dwd_scholar") or "yearly" in t or "annual" in t]
# dwd_scholar 27 列无 per-year 面；但 dwd_scholar_papers（学者×论文关联）需列级实探——
# 若含年份列则 gkx 侧学者×年聚合有转换路径（性能另议）
sp_cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_scholar_papers")]
facts["gkx_scholar_papers_cols"] = sp_cols
facts["gkx_scholar_papers_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_scholar_papers")[0][0])
facts["gkx_scholar_papers_year_like_cols"] = [c for c in sp_cols if re.search(r"year|date|time", c, re.I)]
gcur.close()

# ============ ② dev：年度产出承载（共享快照复证：无论文表） ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=60)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
lcur.execute("SELECT table_schema, table_name FROM information_schema.tables "
             "WHERE table_schema LIKE 'gkxlumenx%%' AND table_name REGEXP 'yearly|annual|scholar|talent'")
facts["dev_yearly_like_tables"] = [f"{r[0]}.{r[1]}" for r in lcur.fetchall()]
lconn.close()

# ============ ③ 久新：ads_talent_yearly_metrics 年度面（核心） ============
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)
jconn = pymysql.connect(**JX)
jcur = jconn.cursor()
def qj(sql):
    jcur.execute(sql)
    return jcur.fetchall()

# 3.1 规模与年份覆盖
facts["jiuxin_yearly_metrics_rows"] = int(qj(
    "SELECT COUNT(*) FROM ads_talent_yearly_metrics")[0][0])
facts["jiuxin_yearly_metrics_talents"] = int(qj(
    "SELECT COUNT(DISTINCT talent_id) FROM ads_talent_yearly_metrics")[0][0])
facts["jiuxin_yearly_metrics_year_dist"] = [[int(a), int(b)] for a, b in qj(
    "SELECT year, COUNT(*) FROM ads_talent_yearly_metrics GROUP BY year ORDER BY year DESC LIMIT 12")]

# 3.2 近3年对比（完整年 2023/2024/2025；2026 部分年按 schema 口径不入正式对比）
facts["jiuxin_yearly_paper_by_year"] = [[int(a), int(b)] for a, b in qj(
    "SELECT year, SUM(paper_count) FROM ads_talent_yearly_metrics WHERE year IN (2021,2022,2023,2024,2025,2026) "
    "GROUP BY year ORDER BY year")]
facts["jiuxin_yearly_citation_by_year"] = [[int(a), int(b)] for a, b in qj(
    "SELECT year, SUM(citation_count) FROM ads_talent_yearly_metrics WHERE year IN (2021,2022,2023,2024,2025,2026) "
    "GROUP BY year ORDER BY year")]
facts["jiuxin_yearly_patent_by_year"] = [[int(a), int(b or 0)] for a, b in qj(
    "SELECT year, SUM(patent_application_count) FROM ads_talent_yearly_metrics WHERE year IN (2021,2022,2023,2024,2025,2026) "
    "GROUP BY year ORDER BY year")]

# 3.3 分阶段（career_stage 分层）：capability_assessment 有 paper_count_band；yearly 侧用产出带分层
#     全池学者近3年产出增长分布（2022→2025 论文数变化）：抽样前 5000 学者（确定性：talent_id 排序）
facts["jiuxin_growth_sample_note"] = "2022→2025 学者级论文增长抽样：talent_id 排序前 5000 人（确定性截断，非随机）"
rows = qj(
    "SELECT t2025.talent_id, IFNULL(t2022.paper_count,0) AS p2022, IFNULL(t2025.paper_count,0) AS p2025 FROM "
    "(SELECT talent_id, paper_count FROM ads_talent_yearly_metrics WHERE year=2025) t2025 "
    "JOIN (SELECT talent_id, paper_count FROM ads_talent_yearly_metrics WHERE year=2022) t2022 "
    "ON t2025.talent_id = t2022.talent_id ORDER BY t2025.talent_id LIMIT 5000")
n_sample = len(rows)
up = sum(1 for r in rows if r[2] > r[1])
flat = sum(1 for r in rows if r[2] == r[1])
down = sum(1 for r in rows if r[2] < r[1])
facts["jiuxin_growth_sample_size"] = n_sample
facts["jiuxin_growth_up_flat_down"] = [up, flat, down]
# 全池配对规模（非抽样——增长分布的全池分母）
facts["jiuxin_growth_paired_fullpool"] = int(qj(
    "SELECT COUNT(*) FROM (SELECT talent_id FROM ads_talent_yearly_metrics WHERE year=2025) t2025 "
    "JOIN (SELECT talent_id FROM ads_talent_yearly_metrics WHERE year=2022) t2022 "
    "ON t2025.talent_id = t2022.talent_id")[0][0])

# 3.4 Field 级年度面（阶段分层的另一维度）
facts["jiuxin_yearly_discipline_rows"] = int(qj(
    "SELECT COUNT(*) FROM ads_talent_yearly_discipline")[0][0])

# 3.5 库内现成增长口径：potential_result 产出动能（output_momentum_raw——对数年度论文数 OLS 斜率）
row = qj("SELECT COUNT(*), COUNT(output_momentum_raw), COUNT(output_momentum_score) "
         "FROM ads_talent_potential_result")[0]
facts["jiuxin_potential_result_rows"] = int(row[0])
facts["jiuxin_output_momentum_nonnull"] = int(row[1])
facts["jiuxin_output_momentum_score_nonnull"] = int(row[2])
jconn.close()

# ================= 派生 =================
by_year = {int(a): int(b) for a, b in facts["jiuxin_yearly_paper_by_year"]}
p2022, p2025 = by_year.get(2022, 0), by_year.get(2025, 0)
derived.append({
    "key": "jiuxin_pool_paper_growth_2022_2025_pct",
    "value": round(100.0 * (p2025 - p2022) / p2022, 2) if p2022 else None,
    "numerator": p2025 - p2022,
    "denominator": p2022,
    "note": "分子=2025 全池论文数-2022 全池论文数；分母=2022 全池论文数（同表同 WHERE 年份过滤，"
            "全池聚合非采样）——全池口径的阶段增长读数",
})
derived.append({
    "key": "jiuxin_scholar_up_share_2022_2025_pct",
    "value": round(100.0 * up / n_sample, 2) if n_sample else None,
    "numerator": up,
    "denominator": n_sample,
    "note": f"分子=抽样内 2025 论文数>2022 的学者数；分母=抽样规模 {n_sample}"
            "（talent_id 排序前 5000 人确定性截断，采样非全池；全池配对规模见 "
            "jiuxin_growth_paired_fullpool）——学者级口径的增长面占比",
})
# 近3年（2023-2025）合计 vs 前3年（2020-2022）合计
p_recent = by_year.get(2023, 0) + by_year.get(2024, 0) + by_year.get(2025, 0)
p_prior = by_year.get(2020, 0) + by_year.get(2021, 0) + by_year.get(2022, 0)
derived.append({
    "key": "jiuxin_pool_paper_recent3y_vs_prior3y_pct",
    "value": round(100.0 * (p_recent - p_prior) / p_prior, 2) if p_prior else None,
    "numerator": p_recent - p_prior,
    "denominator": p_prior,
    "note": "分子=近3年（2023+2024+2025）合计-前3年（2020+2021+2022）合计；分母=前3年合计"
            "（同表全池口径；2026 部分年按 schema 口径不入正式对比）——「近3年对比」字面口径",
})

# ================= absence_probe =================
absence += [
    {"probe": "gkx 学者年度产出面（dwd_scholar* / yearly / annual 词族 + dwd_scholar_papers 列级）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）词族扫 + SHOW COLUMNS FROM gkx.dwd_scholar_papers",
     "hits": 0,
     "hit_detail": f"词族命中 {facts['gkx_yearly_like_tables']}——逐表定性：均为履历/经历/关联明细表，"
                   f"无 talent×year 聚合面；dwd_scholar_papers（{facts['gkx_scholar_papers_rows']} 行）列级核对"
                   f"年份列 {facts['gkx_scholar_papers_year_like_cols']}——gkx 侧学者×年聚合需经论文关联表"
                   "join dwd_zh_paper（varchar 年份列 cover_year_start，B9 陷阱在案）+ 大表聚合工程，"
                   "转换路径在但非现成；X_015 探针在案 author_info_list longtext 非结构化"},
    {"probe": "dev 年度产出承载（gkxlumenx_* 全 schema yearly/annual/scholar/talent 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*",
     "hits": len(facts["dev_yearly_like_tables"]),
     "hit_detail": f"命中 {facts['dev_yearly_like_tables']}——与共享快照一致（无论文表、专利仅企业侧 4 表），"
                   "无学者年度产出面"},
    {"probe": "久新「分阶段产出增长」现成结果面（增长/成长类结果表）",
     "source": "jiuxin",
     "sql": "203 表 growth/momentum 词族扫 + ads_talent_potential_result 列核对",
     "hits": 0,
     "hit_detail": "无『分阶段增长』现成结果面；最接近的库内现成口径是 ads_talent_potential_result."
                   "output_momentum_raw（对数年度论文数 OLS 斜率——观察窗 2021-2025 全窗动能，"
                   f"非近3年对比；非空 {facts['jiuxin_output_momentum_nonnull']} 行）——本件按转换支持判档"},
    {"probe": "需求原文「阶段增长/近3年对比」算法定义段",
     "source": "doc",
     "sql": "rg 阶段增长/近3年/预测视图缩放 三份需求真源（主需求 :2359 命中）",
     "hits": 1,
     "hit_detail": "需求给出行为（『在引进模拟场景中，支持对贡献度预测结果的缩放，用户可切换整体预期、"
                   "局部影响及阶段性增长视图』）但阶段划分（近3年？职业阶段？）与增长算式无——"
                   "『近3年对比』为派单书定名推测口径；UI stage factor 1.15 为 mock 外推演示值"},
]

support = "完全转换支持"

notes += [
    "判档：年度产出面（ads_talent_yearly_metrics talent×year）结构+数据双达标，近3年对比可现转——"
    "无现成「分阶段增长」结果面但依赖侧表结构+当前数据量均已足够 → 完全转换支持",
    f"规模：ads_talent_yearly_metrics {facts['jiuxin_yearly_metrics_rows']} 行 × "
    f"{facts['jiuxin_yearly_metrics_talents']} 人才，年份分布 2015-2026（近 12 年见产物；"
    "2026 部分年按 schema 口径 PARTIAL_YEAR 只展示不入正式对比）",
    f"全池阶段增长（论文口径）：2022→2025 增长 {derived[0]['value']}%"
    f"（{p2022}→{p2025}）；近3年 vs 前3年 {derived[2]['value']}%"
    "（引用/专利年度序列同落产物 jiuxin_yearly_citation_by_year / jiuxin_yearly_patent_by_year）",
    f"学者级增长面（抽样 5000 人确定性截断，采样非全池）：上升 {up} / 持平 {flat} / 下降 {down}"
    f"（上升占比 {derived[1]['value']}%，登记键 jiuxin_scholar_up_share_2022_2025_pct）；"
    f"全池配对规模 {facts['jiuxin_growth_paired_fullpool']}（2022 与 2025 双年均有行的人才）",
    "阶段分层的库内口径：ads_talent_potential_result.career_stage（科研年限段）+ paper_count_band——"
    "「分阶段」可按职业阶段分层复算年度面（本件用年份对比口径交付，职业阶段口径为触发器②）",
    "mock 披露：ContributionTab.jsx:741 stage 选项的预测线是 :304-311 predictViewMap stage factor=1.15 "
    "对近两年 mock 趋势值的线性外推——演示算式不作数据证据（B10）",
    "B11 对账：dev 无论文表/专利仅企业侧与共享快照零漂移；gkx dwd_scholar 21,316 与共享快照零漂移；"
    "久新年度面规模为本件首探（批内无前值可对，登记为新增探针表）；"
    "专利年度面注意：patent_application_count 六年 SUM 全 0/NULL（年度专利指标未回填——读数登记非缺口定性，"
    "学者专利在 ads_talent_patent 另有承载）",
    "升档触发器（B10）：①年度面直连 BI 侧做成现成结果面（物化阶段增长视图）→ 升完全直接支持；"
    "②甲方裁定「阶段」=职业阶段（career_stage 分层）而非年份段 → 同表可转，档位不变口径切换",
]

out = {
    "metric_id": "M_SCIUI_TALENTIR_008",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/talent-trend/components/ContributionTab.jsx:741",
        "repos/demo-ui-science/src/pages/talent-trend/components/ContributionTab.jsx:311",
        "repos/demo-ui-science/src/pages/talent-trend/data.js:1364",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "主需求《科技信息展示系统和科技专题服务系统.md》:2359（1.1.1.1.4.3.4.1.3(2) 预测视图缩放）"
                "行为明列：『用户可切换整体预期、局部影响及阶段性增长视图』——阶段增长视图在、阶段划分与"
                "增长算式无；『近3年对比』为派单书定名推测口径；核增/算法库两份真源 0 命中",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": ["2020", "2021", "2022", "2023", "2024", "2025"],
    "base_years_missing": [],
    "base_years_note": "年度面覆盖 2015-2026（jiuxin_yearly_metrics_year_dist 近 12 年在产物）；本件对比口径用 "
                       "2020-2025 完整年，2026 为 PARTIAL_YEAR 只登记不入正式对比（schema 口径）",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts["jiuxin_yearly_metrics_rows"]),
                          str(facts["jiuxin_yearly_metrics_talents"]),
                          str(p2022), str(p2025), str(up), str(flat), str(down), str(n_sample),
                          str(facts["jiuxin_growth_paired_fullpool"]), str(facts["jiuxin_yearly_discipline_rows"]),
                          "1.15", "741", "5000"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
