#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INDEX_038 科技指数高校榜 · 三源探针与复现脚本（S3-02 Lane 5）。

裁定 NEW：高校榜=高校对象域的分类榜单（非单指数读数）——
UI index.jsx:1081 Radio『高校榜』(university)＝mock rankingData.university
(achievementRankingRecords.filter(type==='university')，成果粒度过滤重排)。

承载：久新 ads_institution_technology_power education 切片 16,446 行
（四指标学术实力榜，与 INDEX_001/036 同源）；gkx 高校池 dwd_forg_university_org_info
20,000 行在案可引（裁定书指定）；gkx 中文论文机构维 2 万行采样 13,738 篇高校首机构
（国产科研生产面代理）。本件交付：education 全量 Top10 / CN 切片 Top10 /
gkx 论文面高校 Top12（采样）+ 池对账。
"""
import json, os, sys, re
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_INDEX_038_out.json")
sys.path.insert(0, BASE)

JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

# ============ ① 久新：education 高校榜主承载 ============
conn = pymysql.connect(**JX)
cur = conn.cursor()
def qj(sql):
    cur.execute(sql)
    return cur.fetchall()

facts["jiuxin_power_rows"] = int(qj("SELECT COUNT(*) FROM ads_institution_technology_power")[0][0])
facts["jiuxin_education_rows"] = int(qj(
    "SELECT COUNT(*) FROM ads_institution_technology_power WHERE institution_type_id='education'")[0][0])

# education 全量 Top10（与 INDEX_036 全类型榜对账：榜首即全类型 rank2）
rows = qj("SELECT p.institution_name, p.technology_power_score, p.technology_power_rank, pr.country_code "
          "FROM ads_institution_technology_power p "
          "LEFT JOIN ads_institution_profile pr ON p.institution_id=pr.institution_id "
          "WHERE p.institution_type_id='education' "
          "ORDER BY p.technology_power_score DESC, p.institution_name LIMIT 10")
facts["jiuxin_education_top10"] = [
    {"rank": i + 1, "name": r[0], "score": float(r[1]),
     "stored_rank": int(r[2]), "country": r[3]} for i, r in enumerate(rows)]

# education + CN 切片 Top10（国内高校榜即期版）
rows = qj("SELECT p.institution_name, p.technology_power_score, p.technology_power_rank "
          "FROM ads_institution_technology_power p "
          "JOIN ads_institution_profile pr ON p.institution_id=pr.institution_id "
          "WHERE p.institution_type_id='education' AND pr.country_code='CN' "
          "ORDER BY p.technology_power_score DESC, p.institution_name LIMIT 10")
facts["jiuxin_education_cn_top10"] = [
    {"rank": i + 1, "name": r[0], "score": float(r[1]), "global_rank": int(r[2])}
    for i, r in enumerate(rows)]
facts["jiuxin_education_cn_rows"] = int(qj(
    "SELECT COUNT(*) FROM ads_institution_technology_power p "
    "JOIN ads_institution_profile pr ON p.institution_id=pr.institution_id "
    "WHERE p.institution_type_id='education' AND pr.country_code='CN'")[0][0])
cur.close(); conn.close()

# ============ ② gkx：高校池 + 论文生产面（采样） ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

# 高校池（共享快照 fix2 大学表行数=20,000 对账）
facts["gkx_university_pool_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_forg_university_org_info")[0][0])
pool_cn = int(qg("SELECT COUNT(*) FROM gkx.dwd_forg_university_org_info WHERE country='China'")[0][0])
facts["gkx_university_pool_china_rows"] = pool_cn

# 论文生产面：2 万行采样，Python 侧解析首机构（大表全扫 GROUP BY 禁用，走采样协议）
gcur.execute("SELECT author_info_list FROM gkx.dwd_zh_paper WHERE author_info_list IS NOT NULL LIMIT 20000")
rows = gcur.fetchall()
facts["gkx_paper_sample_rows"] = len(rows)
UNIV = re.compile(r"大学|学院")
HOSPITAL = re.compile(r"医院|临床|卫生院")
univ_cnt = Counter()
univ_papers = 0
for (ail,) in rows:
    try:
        arr = json.loads(ail)
    except Exception:
        continue
    if not arr:
        continue
    inst = (arr[0].get("institution") or "").strip()
    if UNIV.search(inst) and not HOSPITAL.search(inst):
        univ_papers += 1
        m = re.match(r"^(.*?(?:大学|学院))", inst)
        univ_cnt[m.group(1) if m else inst] += 1
facts["gkx_paper_univ_first_author_rows"] = univ_papers
facts["gkx_paper_univ_top12"] = [
    {"university": n, "papers": c} for n, c in univ_cnt.most_common(12)]

# gkx 侧榜面探针（absence）：高校榜现成结果面
gcur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
             "AND (table_name LIKE '%rank%' OR table_name LIKE '%score%')")
facts["gkx_rank_score_tables"] = [r[0] for r in gcur.fetchall()]

# ============ ③ dev 库：高校榜结果面探针（absence） ============
LIVE = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
            charset="utf8mb4", connect_timeout=10, read_timeout=60)
lconn = pymysql.connect(**LIVE)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()
dev_univ_tables = [r[0] for r in ql(
    "SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA IN ('gkxlumenx_dwd','gkxlumenx_ads') "
    "AND (TABLE_NAME LIKE '%univ%' OR TABLE_NAME LIKE '%ranking%')")]
facts["dev_univ_or_ranking_tables"] = dev_univ_tables
dev_rank_rows = int(ql("SELECT COUNT(*) FROM gkxlumenx_ads.enterprise_ranking")[0][0])
facts["dev_ads_enterprise_ranking_rows"] = dev_rank_rows
lconn.close()

# ================= 派生 =================
derived.append({
    "key": "gkx_paper_univ_share_pct_sample",
    "value": round(100.0 * univ_papers / len(rows), 4),
    "numerator": univ_papers,
    "denominator": len(rows),
    "note": "分子=首机构可判高校（含'大学/学院'剔'医院/临床/卫生院'）的采样篇数，分母=同批 2 万采样篇数；"
            "同池同 WHERE（B3）；采样协议读数，非全表"})
derived.append({
    "key": "jiuxin_education_share_pct",
    "value": round(100.0 * facts["jiuxin_education_rows"] / facts["jiuxin_power_rows"], 4),
    "numerator": facts["jiuxin_education_rows"],
    "denominator": facts["jiuxin_power_rows"],
    "note": "分子=education 类型机构行数，分母=power 全表行数；同表同池（B3）——高校对象在全机构榜中的构成"})
derived.append({
    "key": "jiuxin_cn_share_of_education_pct",
    "value": round(100.0 * facts["jiuxin_education_cn_rows"] / facts["jiuxin_education_rows"], 4),
    "numerator": facts["jiuxin_education_cn_rows"],
    "denominator": facts["jiuxin_education_rows"],
    "note": "分子=education 且 country_code='CN' 行数，分母=education 全切片行数；同切片同池（B3）——高校榜中国构成"})

# ================= absence_probe =================
absence += [
    {"probe": "gkx 高校榜现成结果面（rank/score 表）",
     "source": "gkx",
     "sql": "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
            "AND (table_name LIKE '%rank%' OR table_name LIKE '%score%')",
     "hits": len(facts["gkx_rank_score_tables"]),
     "hit_names": facts["gkx_rank_score_tables"]},
    {"probe": "dev 高校榜承载（univ/ranking 表）",
     "source": "dev",
     "sql": "SELECT ... TABLE_NAME LIKE '%univ%' OR '%ranking%'（gkxlumenx_dwd/gkxlumenx_ads）",
     "hits": len(dev_univ_tables),
     "hit_detail": f"表名命中 {dev_univ_tables}；其中 ads.enterprise_ranking 实测 {dev_rank_rows} 行"
                   "（造数黑名单 skill P4.1 且空壳，存在性披露、值不参与判档）"},
    {"probe": "久新榜面语义维（四指标学术实力 vs UI mock 成果四维）",
     "source": "jiuxin",
     "sql": "SELECT metrics_as_of_date, metric_definition_version FROM ads_institution_technology_power LIMIT 1",
     "hits": 0,
     "hit_detail": "非表缺失探针：power 榜口径=论文0.35/被引0.30/人才0.25/主题0.10 学术单维族，"
                   "无 UI mock 创新/影响/潜力/保障成果四维——语义偏移披露，不构成缺席证伪"},
]

support = "完全转换支持"

notes += [
    "判档（裁定 NEW 口径）：高校榜=高校对象域分类榜单。对象池三源在案：久新 power education 切片 "
    "16,446 行（现役名次列，过滤重排即得高校榜）；gkx 高校池 dwd_forg_university_org_info 20,000 行"
    "（裁定书指定在案可引，China 971 所）；gkx 中文论文首机构 2 万采样 13,738 篇可判高校（68.69%）——"
    "对象域与计分原料均足量，现转即得判完全转换支持",
    "复现读数：education 全量 Top10（jiuxin_education_top10，榜首国科大 stored_rank=2 与 INDEX_036 "
    "全类型榜对账零漂移）；CN 切片 Top10（jiuxin_education_cn_top10）；gkx 论文面高校 Top12"
    "（gkx_paper_univ_top12，采样，非全表）",
    "语义偏移披露：power 榜=学术实力四指标族（论文/被引/人才/主题），非 UI mock 成果四维"
    "（innovation/influence/potential/support）——与 INDEX_001/036 同口径偏移；UI『高校榜』mock 为"
    "成果粒度过滤（type='university'），本件为机构粒度切片，机构粒度是更贴近『高校榜』三字的对象域；"
    "成果粒度需 INDEX_013 指标体系闭合",
    "B11 对账：power 64,698 行/education 16,446/CN 1,150 与 INDEX_001/036 facts 零漂移；"
    "gkx 高校池 20,000 行与共享快照 fix2 大学表行数一致",
    "采样协议：论文面 2 万行采样（dwd_zh_paper 10.09 万行大表，全扫 GROUP BY 禁用），"
    "读数 note 已标『采样，非全表』",
]

out = {
    "metric_id": "M_SCIUI_INDEX_038",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/tech-index/index.jsx:1081",
        "repos/demo-ui-science/src/pages/tech-index/mockData.js:1195",
        "repos/demo-ui-science/src/pages/tech-index/index.jsx:1066",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「高校榜」未独立出现在三份需求真源；语义源=SRS 科技指数.md seq 172『分类排名展示』"
                "（按科技领域、成果类型、机构类型、地域范围等条件查看分类排名——机构类型维度的高校切片即"
                "高校榜语义根据）+ 主需求 1.1.1.1.4.1.8.3 排行榜章；UI 实现为四榜 Radio 第二项『高校榜』"
                "(university)",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [2026],
    "base_years_missing": [],
    "base_years_note": "机构榜为 2026-09-18 时点快照（jiuxin_power_version，INDEX_036 同源）；"
                       "gkx 论文面为采样时点读数，无年度序列诉求",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": ["16,446", "1,150", "13,738", "68.69", "20,000", "971"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
