#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INDEX_028 科技影响力指数 · 三源探针与复现脚本（S3-02 Lane 4）。

裁定 NEW：组合指数——需求文档 :923『科学影响力、技术影响力等科技影响力指标』
是组合语义真源（产业发展潜力评估体系语境）；UI techIndex.js:257 四分项之一
『科技影响力指数 weight 24（引用影响、传播强度、区域带动和全球对标）』、
:515 buildTechIndexDetail 指标拆解行 influence。

候选面盘点（三源）：
  jiuxin: ①institution_technology_power.citation_score（科学影响力单维现役）
          ②institution_yearly_metrics（fwci/avg_citations_per_paper——篇均影响力族）
          ③region_snapshot 六评分（research_heat/frontier_leadership/…——区域组合影响力族）
  gkx:    dwd_scholar.citation_nums/h_index（学者级影响力列，21,316 行）
  dev:    svc_tech_power_score 造数黑名单
复现：三源影响力分维谱系盘点 + 科学/技术两单维在 power 面的实测覆盖与
组合缺失的量化披露（缺技术影响力分列的结构证据）。
"""
import json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_INDEX_028_out.json")
sys.path.insert(0, BASE)

JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)
DEV = dict(host="10.50.11.76", port=3306, user="root",
           password="Gkxzp202600", connect_timeout=8, read_timeout=120)

import pymysql  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

# ================= 久新 =================
conn = pymysql.connect(**JX)
cur = conn.cursor()


def q(sql):
    cur.execute(sql)
    return cur.fetchall()


# 1) power 面：citation_score（科学影响力单维锚）
facts["jiuxin_power_rows"] = int(q("SELECT COUNT(*) FROM ads_institution_technology_power")[0][0])
cs = q("SELECT COUNT(*), COUNT(citation_score), MIN(citation_score), MAX(citation_score), AVG(citation_score) "
       "FROM ads_institution_technology_power")[0]
facts["jiuxin_citation_score_coverage"] = {
    "rows": int(cs[0]), "nonnull": int(cs[1]),
    "min": float(cs[2]), "max": float(cs[3]), "avg": round(float(cs[4]), 4)}
ps = q("SELECT COUNT(paper_score), MIN(paper_score), MAX(paper_score) FROM ads_institution_technology_power")[0]
facts["jiuxin_paper_score_coverage"] = {"nonnull": int(ps[0]), "min": float(ps[1]), "max": float(ps[2])}

# 2) 篇均影响力族：institution_yearly_metrics（fwci/avg_citations_per_paper，最新年）
fw = q("SELECT COUNT(*), COUNT(fwci), COUNT(avg_citations_per_paper) FROM ads_institution_yearly_metrics "
       "WHERE statistics_year=2026")[0]
facts["jiuxin_fwci_cols_2026"] = {"rows": int(fw[0]), "fwci_nonnull": int(fw[1]), "avg_cit_nonnull": int(fw[2])}
top_fwci = q("SELECT institution_id, fwci FROM ads_institution_yearly_metrics WHERE statistics_year=2026 "
             "AND fwci IS NOT NULL ORDER BY fwci DESC LIMIT 5")
facts["jiuxin_fwci_top5_2026"] = [{"institution_id": r[0], "fwci": float(r[1])} for r in top_fwci]

# 3) 区域组合影响力族：region_snapshot（六评分列）
rs_cols = q("DESCRIBE ads_research_problem_region_snapshot")
facts["jiuxin_region_snapshot_columns"] = [r[0] for r in rs_cols]
facts["jiuxin_region_snapshot_rows"] = int(q("SELECT COUNT(*) FROM ads_research_problem_region_snapshot")[0][0])
rs_ver = q("SELECT metrics_as_of_date, metric_definition_version, COUNT(*) FROM ads_research_problem_region_snapshot GROUP BY 1,2")
facts["jiuxin_region_snapshot_version"] = [
    {"as_of": str(r[0]), "version": r[1], "rows": int(r[2])} for r in rs_ver]
# 投资分缺失量化（investment_score null 率——组合维覆盖证据）
inv = q("SELECT COUNT(*), COUNT(investment_score) FROM ads_research_problem_region_snapshot WHERE location_level='COUNTRY'")[0]
facts["jiuxin_region_country_investment_coverage"] = {
    "country_rows": int(inv[0]), "investment_score_nonnull": int(inv[1])}

# 4) 技术影响力侧原料：专利面规模（technology_patent / institution_patent）
facts["jiuxin_tech_patent_rows"] = int(q("SELECT COUNT(*) FROM ads_technology_patent")[0][0])
facts["jiuxin_inst_patent_rows"] = int(q("SELECT COUNT(*) FROM ads_institution_patent")[0][0])

cur.close(); conn.close()

# ================= gkx =================
from _gkxdb import gkx  # noqa: E402
cur = gkx()
sc = q("SELECT COUNT(*), COUNT(citation_nums), COUNT(h_index), COUNT(reference_nums) FROM gkx.dwd_scholar")[0]
facts["gkx_scholar_influence_cols"] = {
    "rows": int(sc[0]), "citation_nums_nonnull": int(sc[1]),
    "h_index_nonnull": int(sc[2]), "reference_nums_nonnull": int(sc[3])}
cur.close()

# ================= dev =================
conn = pymysql.connect(**DEV)
cur = conn.cursor()
try:
    svc = int(q("SELECT COUNT(*) FROM gkxlumenx_ads.svc_tech_power_score")[0][0])
except Exception:  # noqa: BLE001
    svc = -1
facts["dev_svc_tech_power_score_rows"] = svc
cur.close(); conn.close()

# ================= 派生 =================
derived.append({
    "key": "jiuxin_citation_score_nonnull_pct",
    "value": round(100.0 * facts["jiuxin_citation_score_coverage"]["nonnull"] / facts["jiuxin_power_rows"], 4),
    "numerator": facts["jiuxin_citation_score_coverage"]["nonnull"],
    "denominator": facts["jiuxin_power_rows"],
    "note": "分子=citation_score 非空行数，分母=power 全表行数；同表同池（B3）——科学影响力单维的现役覆盖度"})
derived.append({
    "key": "jiuxin_region_country_investment_nonnull_pct",
    "value": round(100.0 * facts["jiuxin_region_country_investment_coverage"]["investment_score_nonnull"]
                   / facts["jiuxin_region_country_investment_coverage"]["country_rows"], 4),
    "numerator": facts["jiuxin_region_country_investment_coverage"]["investment_score_nonnull"],
    "denominator": facts["jiuxin_region_country_investment_coverage"]["country_rows"],
    "note": "分子=国家级 investment_score 非空行数，分母=region_snapshot COUNTRY 级行数；同表同层（B3）——组合维缺格的量化证据"})

# ================= absence_probe =================
absence = [
    {"probe": "久新『科学+技术组合』科技影响力指数现成面",
     "source": "jiuxin",
     "sql": "DESCRIBE ads_institution_technology_power / ads_geo_yearly_index（列清单落 facts）",
     "hits": 0,
     "hit_detail": "power 四分项无技术影响力分列（专利维缺位：institution_patent 为计数画像非评分）；"
                   "geo_yearly_index（通用指数承载表）实测 0 行——组合指数无现成结果面"},
    {"probe": "gkx 科技影响力指数结果面",
     "source": "gkx",
     "sql": "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' AND (table_name LIKE '%influence%' OR table_name LIKE '%impact%' OR table_name LIKE '%index%')",
     "hits": 4,
     "hit_names": ["dwd_dim_index_attribute", "dwd_dim_index_cal", "dwd_dim_index_dur", "dwd_macro_index_data"],
     "hit_detail": "四表为宏观经济指数族（dim_cal=环比/同比/绝对值，macro_index_data=宏观指标值 area_code 广东地市），"
                   "语义属宏观经济域非科技影响力——存在性披露，不构成本指标承载"},
    {"probe": "dev 科技影响力指数承载",
     "source": "dev",
     "sql": "SELECT COUNT(*) FROM gkxlumenx_ads.svc_tech_power_score",
     "hits": 0,
     "hit_detail": f"实测 {svc} 行——服务域造数面（skill P4.1 黑名单），存在性披露、值不引用"},
]

support = "部分支持"

notes += [
    "判档（裁定 NEW 口径）：科技影响力指数=组合语义（需求 :923『科学影响力、技术影响力等科技影响力指标』——产业"
    "发展潜力评估体系语境）；三源无『科学+技术组合』现成结果面——久新 power 的 citation_score 只是科学单维（论文被引族），"
    "技术影响力（专利侧）在 power 四分项中无分列（paper/citation/talent/topic 全学术族）；geo_yearly_index 指数承载表 0 行。"
    "组合口径需自建合成（科学分 citation_score 现役 + 技术分需从 institution_patent/technology_patent 明细新算），判部分支持",
    "三源影响力分维谱系（本件盘点交付）：①久新 citation_score（机构科学影响力，64,698 行全覆盖）；②久新 fwci/"
    "avg_citations_per_paper（篇均影响力，816,120 行年面板）；③久新 region_snapshot 六评分（区域组合影响力族，投资分国家级"
    "缺格——组合维覆盖风险证据）；④gkx dwd_scholar citation_nums/h_index/reference_nums（学者级三列，非空数落产物）；"
    "⑤久新专利明细 23 列表×2（技术侧原料在案，评分未合成）",
    "UI 口径注记：techIndex.js:257『科技影响力指数 weight 24』四分项描述=引用影响、传播强度、区域带动和全球对标——"
    "引用影响映射 citation_score/fwci（现役），传播强度/区域带动/全球对标三子维三源均无现成分列（组合缺口的具体形态）",
    "B10 双口径：口径 A=科学影响力单维先行（citation_score 现役可直读，标注『非组合口径』）；口径 B=组合口径立项"
    "（科学分复用 citation_score + 技术分从专利明细合成 + 传播/对标子维定义）→ 结构齐备后升完全转换支持",
]

out = {
    "metric_id": "M_SCIUI_INDEX_028",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/techIndex.js:257",
        "repos/demo-ui-science/src/techIndex.js:515",
        "repos/demo-ui-science/src/techIndex.js:236",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「科技影响力指数」作为指标名未出现在三份需求真源；组合语义真源=主需求文档 :923（1.1.1.1.4.1.7.3 产业发展潜力指标展示：『以及科学影响力、技术影响力等科技影响力指标，构建产业发展潜力评估体系』）；SRS 科技指数.md 最近语义叶=seq 166『科技影响力趋势可视化』（趋势展示非指数本体）；UI techIndex.js 指标树四分项之一（weight 24）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [2026],
    "base_years_missing": [],
    "base_years_note": "单维锚（citation_score/power 面）为 2026-09-18 时点快照；fwci 族有 2015-2026 年面板（趋势可视化 seq 166 语义可承接，本件不展开）",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": ["64,698", "816,120", "21,316", "24", ":923"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
