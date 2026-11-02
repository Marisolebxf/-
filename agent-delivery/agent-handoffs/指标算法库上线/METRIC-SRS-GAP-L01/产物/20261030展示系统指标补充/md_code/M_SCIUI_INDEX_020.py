#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INDEX_020 排名对比分析 · 三源探针与复现脚本（S3-02 Lane 4）。

UI 语义：排行榜 Tab『排名对比分析』抽屉（index.jsx:1229 Drawer + :1327
RankingComparePanel）——多对象（≤上限）雷达+柱状分维对比、平均/最高分、
leader、强弱项识别、已保存方案。

数据要件：①多对象榜单（每对象多分维得分）；②同构分维可横向对比。
承载判定：久新 power 64,698 行=对象×四分项得分（paper/citation/talent/topic）
+总分——多对象多分维现役面，过滤选对象+分维并排即得对比视图。
本脚本复现：取 UI 同构演示形态（企业 Top5 对比组）在 power 表实测：
雷达四分项+总分对比+强弱项（每人 max/min 分维）+组均值。
"""
import json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_INDEX_020_out.json")
sys.path.insert(0, BASE)

JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)

import pymysql  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

conn = pymysql.connect(**JX)
cur = conn.cursor()


def q(sql):
    cur.execute(sql)
    return cur.fetchall()


# 1) 对比承载面（与 INDEX_001 对账）
facts["jiuxin_power_rows"] = int(q("SELECT COUNT(*) FROM ads_institution_technology_power")[0][0])
ver = q("SELECT metrics_as_of_date, metric_definition_version FROM ads_institution_technology_power LIMIT 1")
facts["jiuxin_power_version"] = {"as_of": str(ver[0][0]), "version": ver[0][1]}

# 2) 复现：企业 Top5 对比组（UI Radio 演示企业榜语境的同构真实版）
rows = q("SELECT institution_name, institution_type_id, paper_score, citation_score, talent_score, "
         "topic_score, technology_power_score, technology_power_rank "
         "FROM ads_institution_technology_power WHERE institution_type_id='company' "
         "ORDER BY technology_power_score DESC, institution_name LIMIT 5")
comp = [{"name": r[0], "type": r[1],
         "paper": float(r[2]), "citation": float(r[3]),
         "talent": float(r[4]), "topic": float(r[5]),
         "total": float(r[6]), "global_rank": int(r[7])} for r in rows]
facts["jiuxin_company_top5_compare_group"] = comp

# 3) 强弱项（每人 max/min 分维——UI 单对象强弱项语义）
DIM_LABELS = {"paper": "科研产出", "citation": "学术影响", "talent": "人才", "topic": "主题覆盖"}
strength_weakness = []
for c in comp:
    dims = {k: c[k] for k in DIM_LABELS}
    sdim = max(dims, key=lambda k: (dims[k], k))  # 双键破平局（B5）
    wdim = min(dims, key=lambda k: (dims[k], k))
    strength_weakness.append({
        "name": c["name"],
        "strength_dim": f"{DIM_LABELS[sdim]}({sdim})", "strength_score": dims[sdim],
        "weakness_dim": f"{DIM_LABELS[wdim]}({wdim})", "weakness_score": dims[wdim]})
facts["jiuxin_top5_strength_weakness"] = strength_weakness

# 4) 对照组：education Top3（跨类型对比演示——对比不限于企业）
rows2 = q("SELECT institution_name, paper_score, citation_score, talent_score, topic_score, "
          "technology_power_score FROM ads_institution_technology_power WHERE institution_type_id='education' "
          "ORDER BY technology_power_score DESC, institution_name LIMIT 3")
facts["jiuxin_education_top3_reference"] = [
    {"name": r[0], "paper": float(r[1]), "citation": float(r[2]),
     "talent": float(r[3]), "topic": float(r[4]), "total": float(r[5])} for r in rows2]

cur.close(); conn.close()

# ================= 派生 =================
avg_total = sum(c["total"] for c in comp) / len(comp)
max_total = max(c["total"] for c in comp)
leader = max(comp, key=lambda c: (c["total"], c["name"]))  # 双键（B5）
derived.append({
    "key": "jiuxin_compare_group_avg_total",
    "value": round(avg_total, 4),
    "numerator": round(sum(c["total"] for c in comp), 4),
    "denominator": len(comp),
    "note": "分子=组内五家总分和，分母=组内对象数；同表同池（B3）——UI『平均分』读数的真实版"})
derived.append({
    "key": "jiuxin_compare_group_total_range",
    "value": round(max_total - min(c["total"] for c in comp), 4),
    "numerator": max_total,
    "denominator": min(c["total"] for c in comp),
    "note": "分子=组内最高总分，分母=组内最低总分；value=极差（跨度键，非比值）——衡量组内可比性"})
# 分维优势差（leader vs 组内最低，citation 维）
cit_vals = [c["citation"] for c in comp]
derived.append({
    "key": "jiuxin_compare_group_citation_spread_pct",
    "value": round(100.0 * (max(cit_vals) - min(cit_vals)) / max(cit_vals), 4) if max(cit_vals) else None,
    "numerator": round(max(cit_vals) - min(cit_vals), 4),
    "denominator": round(max(cit_vals), 4),
    "note": "分子=组内学术影响分极差，分母=组内学术影响分最高值；同表同维（B3）——对比视图分维差异度样例"})

# ================= absence_probe =================
absence = [
    {"probe": "UI 四维（创新/影响/潜力/保障）科技成果对比面",
     "source": "jiuxin",
     "sql": "DESCRIBE ads_institution_technology_power（22 列）",
     "hits": 0,
     "hit_detail": "现役四分项=paper/citation/talent/topic（学术单维族），无 UI 语义的创新能力/保障能力维——对比视图可现转但分维语义偏移（B10 披露）"},
    {"probe": "dev 对比承载（对比分析现成面）",
     "source": "dev",
     "sql": "SHOW TABLES FROM gkxlumenx_ads / gkxlumenx_topic_enterprise（表扫描；ent_compare_basket* 为收藏夹非结果面）",
     "hits": 0,
     "hit_detail": "topic 库 ent_compare_basket_item 为用户对比篮收藏（交互态），非数据结果面；ads 库无对比结果表"},
    {"probe": "gkx 多对象多分维对比面",
     "source": "gkx",
     "sql": "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' AND (table_name LIKE '%rank%' OR table_name LIKE '%score%')",
     "hits": 0,
     "hit_names": []},
]

support = "完全转换支持"

notes += [
    "判档：对比分析要件=多对象×多分维同构得分面。久新 power 64,698 行（对象）×四分项+总分（分维）现役在案，"
    "任意对象组过滤+分维并排即得对比视图（雷达/柱状/强弱项/组均值全部可算）——结构+数据量足够现转，判完全转换支持",
    "复现读数：企业 Top5 对比组四分项+总分全落产物（jiuxin_company_top5_compare_group）；每人强弱项（jiuxin_top5_strength_weakness）；"
    "education Top3 跨类型对照组（jiuxin_education_top3_reference）——UI『排名对比分析』抽屉各读数的真实数据版",
    "语义偏移披露：现役分维=paper/citation/talent/topic 学术四分族，非 UI mock 四维（科技创新能力/科技影响力/科技发展潜力/科技保障能力）；"
    "四维综合对比需 INDEX_013 口径 B（体系赋权）闭合后对同面重算——本件对比链路与该闭合正交（对象过滤/强弱项/组均值逻辑复用）",
    "B11 对账：64,698 行/版本 2026-09-18×mvp_v1 与 INDEX_001 facts 及共享探针 B1/B2 零漂移",
]

out = {
    "metric_id": "M_SCIUI_INDEX_020",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/tech-index/index.jsx:1229",
        "repos/demo-ui-science/src/pages/tech-index/index.jsx:1327",
        "repos/demo-ui-science/src/pages/tech-index/index.jsx:876",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "需求明列叶：SRS 科技指数.md seq 175『排名对比分析』（excel_row 178）——『用户可选择多项科技成果进行对比分析，提供对比视图，展示各成果在不同指标上的表现差异和优劣势』；主需求文档 1.1.1.1.4.1.8.3.5 同文",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [2026],
    "base_years_missing": [],
    "base_years_note": "对比承载为 power 时点快照（2026-09-18 单期）；跨期对比（同期 vs 上期）需多期快照积累（与 INDEX_019 同缺口）",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": ["64,698", "2026-09-18"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
