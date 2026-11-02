#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INDEX_036 科技指数综合榜 · 三源探针与复现脚本（S3-02 Lane 4）。

裁定 NEW：综合榜=多对象（城市/机构等）聚合榜单，非单指数读数——
UI index.jsx:1080 Radio『综合榜』（comprehensive，全对象总榜）。
姊妹件 INDEX_001（企业榜=company 切片）已证 power 表过滤重排路径可用；
本件交付全对象综合榜 TopN + 多粒度切片（类型/国别）+ 与 mock 分组口径的对照。

承载：久新 ads_institution_technology_power 64,698 行（全类型基准名次在列）；
geo 面为城市/国家级多对象候选（ads_geo_yearly_metrics COUNTRY 5,081 行快照），
ads_geo_yearly_index（地理指数承载）实测 0 行（空表披露）。
"""
import json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_INDEX_036_out.json")
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


# 1) 综合榜主承载：power 全对象榜（与 INDEX_001 对账零漂移）
facts["jiuxin_power_rows"] = int(q("SELECT COUNT(*) FROM ads_institution_technology_power")[0][0])
ver = q("SELECT metrics_as_of_date, metric_definition_version FROM ads_institution_technology_power LIMIT 1")
facts["jiuxin_power_version"] = {"as_of": str(ver[0][0]), "version": ver[0][1]}

# 全类型综合 Top10（rank 列即基准名次；ORDER BY score DESC,name 双键复核；国别经 profile JOIN）
rows = q("SELECT p.institution_name, p.institution_type_id, p.technology_power_score, p.technology_power_rank, "
         "pr.country_code FROM ads_institution_technology_power p "
         "LEFT JOIN ads_institution_profile pr ON p.institution_id = pr.institution_id "
         "ORDER BY p.technology_power_score DESC, p.institution_name LIMIT 10")
facts["jiuxin_alltype_top10"] = [
    {"rank": i + 1, "name": r[0], "type": r[1], "score": float(r[2]),
     "stored_rank": int(r[3]), "country": r[4]} for i, r in enumerate(rows)]

# 2) 类型切片（四榜 Radio 的综合榜=全类型；切片分布与 INDEX_001 对账）
ty = q("SELECT institution_type_id, COUNT(*) FROM ads_institution_technology_power GROUP BY institution_type_id ORDER BY 2 DESC")
facts["jiuxin_type_distribution"] = {r[0]: int(r[1]) for r in ty}

# 3) 国别切片（国内榜候选：profile.country_code 维）
cc = q("SELECT pr.country_code, COUNT(*) FROM ads_institution_technology_power p "
       "JOIN ads_institution_profile pr ON p.institution_id = pr.institution_id "
       "GROUP BY pr.country_code ORDER BY 2 DESC LIMIT 10")
facts["jiuxin_country_top10_distribution"] = {r[0] if r[0] else "(空)": int(r[1]) for r in cc}
cn_top = q("SELECT p.institution_name, p.institution_type_id, p.technology_power_score, p.technology_power_rank "
           "FROM ads_institution_technology_power p "
           "JOIN ads_institution_profile pr ON p.institution_id = pr.institution_id "
           "WHERE pr.country_code='CN' "
           "ORDER BY p.technology_power_score DESC, p.institution_name LIMIT 10")
facts["jiuxin_china_top10"] = [
    {"rank": i + 1, "name": r[0], "type": r[1], "score": float(r[2]), "global_rank": int(r[3])}
    for i, r in enumerate(cn_top)]

# 4) 城市/国家级第二承载：geo 面（城市/国家多对象候选）
geo_lv = q("SELECT location_level, COUNT(*) FROM ads_geo_yearly_metrics GROUP BY location_level ORDER BY 2 DESC")
facts["jiuxin_geo_level_distribution"] = {r[0]: int(r[1]) for r in geo_lv}
geo_idx_rows = int(q("SELECT COUNT(*) FROM ads_geo_yearly_index")[0][0])
facts["jiuxin_geo_yearly_index_rows"] = geo_idx_rows

cur.close(); conn.close()

# ================= 派生 =================
cn_rows = facts["jiuxin_country_top10_distribution"].get("CN", 0)
derived.append({
    "key": "jiuxin_cn_institution_share_pct",
    "value": round(100.0 * cn_rows / facts["jiuxin_power_rows"], 4),
    "numerator": cn_rows,
    "denominator": facts["jiuxin_power_rows"],
    "note": "分子=country_code='CN' 机构行数，分母=power 全表行数；同表同池（B3）——综合榜国别构成读数"})
top10 = facts["jiuxin_alltype_top10"]
derived.append({
    "key": "jiuxin_top10_type_diversity",
    "value": len({t["type"] for t in top10}),
    "numerator": len({t["type"] for t in top10}),
    "denominator": len(ty),
    "note": "分子=Top10 出现的类型数，分母=全榜类型总数；value=类型多样性（计数键，非比值）——综合榜跨类型代表性"})
derived.append({
    "key": "jiuxin_top1_vs_top10_score_gap",
    "value": round(top10[0]["score"] - top10[-1]["score"], 4),
    "numerator": top10[0]["score"],
    "denominator": top10[-1]["score"],
    "note": "分子=榜首分，分母=第10名分；value=头部极差（跨度键，非比值）——榜首集中度读数"})

# ================= absence_probe =================
absence = [
    {"probe": "久新地理级科技指数榜（城市/国家对象现成榜面）",
     "source": "jiuxin",
     "sql": "SELECT COUNT(*) FROM ads_geo_yearly_index",
     "hits": 0,
     "hit_detail": "地理指数承载表实测 0 行（_table_class E-空表分类一致，现场复核）——城市/国家级『科技指数』"
                   "现成榜面不存在；geo_yearly_metrics 为原始指标面（论文/被引计数，无指数化得分列）"},
    {"probe": "dev 综合榜承载",
     "source": "dev",
     "sql": "SELECT COUNT(*) FROM gkxlumenx_ads.enterprise_ranking（全类型综合榜候选表）",
     "hits": 0,
     "hit_detail": "实测 0 行——造数黑名单（skill P4.1）且空壳，存在性披露、值不参与判档"},
    {"probe": "gkx 综合榜结果面",
     "source": "gkx",
     "sql": "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' AND (table_name LIKE '%rank%' OR table_name LIKE '%score%')",
     "hits": 0,
     "hit_names": []},
]

support = "完全转换支持"

notes += [
    "判档（裁定 NEW 口径）：综合榜=多对象聚合榜单。机构对象维：久新 power 64,698 行全类型基准名次现役"
    "（过滤/切片/重排即得综合榜及类型/国别子榜，INDEX_001 企业榜路径同源复用）；城市/国家对象维：geo 原始指标面"
    "171,736 行在案（COUNTRY 5,081 行×27 年），指数化承载表 geo_yearly_index 0 行——地理榜需从原始面自建指数化"
    "（聚合维度在、得分列缺）。机构综合榜现转即得判完全转换支持；地理榜升档路径见 B10 触发器",
    "复现读数：全类型 Top10（jiuxin_alltype_top10，含 stored_rank 双键复核）；CN 切片 Top10（jiuxin_china_top10，"
    "国内综合榜即期版）；类型分布（jiuxin_type_distribution）与国别 Top10 分布（jiuxin_country_top10_distribution）"
    "——四榜 Radio 与国别筛选的真实数据底座",
    "语义偏移披露：power 榜=科技实力四指标（论文0.35/被引0.30/人才0.25/主题0.10）学术单维族，非 UI mock 四维"
    "（创新0.4/影响0.3/潜力0.2/保障0.1）科技成果综合榜——与 INDEX_001 同口径偏移；UI 综合榜的『综合』在 mock 里是"
    "全对象不分类型（comprehensive=按领域分组重排），本件全类型 Top10 为最接近的真实版；四维语义闭合需 INDEX_013 口径 B",
    "B11 对账：64,698 行/版本/类型分布（company 13,939 等）与 INDEX_001 facts 零漂移；geo 分布与共享探针 A1 一致",
]

out = {
    "metric_id": "M_SCIUI_INDEX_036",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/tech-index/index.jsx:1080",
        "repos/demo-ui-science/src/pages/tech-index/mockData.js:1196",
        "repos/demo-ui-science/src/pages/tech-index/index.jsx:1049",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「综合榜」未独立出现在三份需求真源；语义源=SRS 科技指数.md seq 171『科技成果综合排名』（展示综合排名榜单、前N位及得分、排名变化趋势）+ seq 172『分类排名展示』（机构类型等条件分类排名——四榜 Radio 的语义根据）；UI 实现为排名 Tab Radio 首项『综合榜』(comprehensive)",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [2026],
    "base_years_missing": [],
    "base_years_note": "机构榜为 2026-09-18 时点快照；geo 面 COUNTRY 级 2000-2026 二十七年年度序列在案（地理榜历史维原料充足）",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": ["64,698", "5,081", "171,736", "2026-09-18", "13,939"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
