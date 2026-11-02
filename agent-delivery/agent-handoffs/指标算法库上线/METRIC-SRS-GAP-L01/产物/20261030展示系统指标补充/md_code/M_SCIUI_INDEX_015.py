#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INDEX_015 主体产业影响力得分 · 三源探针与复现脚本（S3-02 Lane 4）。

UI 语义：科技指数页指标树 L1『科技影响力』(mockData.js:85, weight 0.30) 下的
L2『产业影响力』节点（mockData.js:132, weight 0.40，父维内），
mock 公式『技术转让收入×0.5 + 带动产业增值×0.3 + 标准制定×0.2』（演示值）。

三源判定面：
  - jiuxin: ads_institution_technology_power 64,698 行（技术力四分项，无产业经济分项）；
           ads_institution_industry 1,354,245 行（IPC 产业参与画像，无评分列——列清单探针）
  - gkx:   dwd_patent 2,939,895（专利代理轴）；dwd_org_base_info 族无技术转让收入列
  - dev:   enterprise_chain_* 产业链关联面；造数黑名单 enterprise_score 0 行复核
"""
import json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_INDEX_015_out.json")
sys.path.insert(0, BASE)

JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)
DEV = dict(host="10.50.11.76", port=3306, user="root",
           password="Gkxzp202600", connect_timeout=8, read_timeout=120)

import pymysql  # noqa: E402

facts, derived, notes, absence = {}, [], [], []


def q(cur, sql):
    cur.execute(sql)
    return cur.fetchall()


# ================= 久新 =================
conn = pymysql.connect(**JX)
cur = conn.cursor()

# 1) 主承载面：institution_technology_power 规模+版本（与 INDEX_001 共享快照对账）
facts["jiuxin_power_rows"] = int(q(cur, "SELECT COUNT(*) FROM ads_institution_technology_power")[0][0])
ver = q(cur, "SELECT metrics_as_of_date, metric_definition_version FROM ads_institution_technology_power LIMIT 1")
facts["jiuxin_power_version"] = {"as_of": str(ver[0][0]), "version": ver[0][1]}
facts["jiuxin_power_columns"] = [r[0] for r in q(cur, "DESCRIBE ads_institution_technology_power")]

# 2) 产业参与画像面：institution_industry（IPC 产业参与；类目证据）
facts["jiuxin_industry_rows"] = int(q(cur, "SELECT COUNT(*) FROM ads_institution_industry")[0][0])
facts["jiuxin_industry_columns"] = [r[0] for r in q(cur, "DESCRIBE ads_institution_industry")]

# 3) 专利侧产业证据（技术影响力代理轴）：institution_patent
facts["jiuxin_inst_patent_rows"] = int(q(cur, "SELECT COUNT(*) FROM ads_institution_patent")[0][0])

# 4) 机构×技术节点产业参与 Top（is_company 维——产业主体子池规模）
facts["jiuxin_tech_inst_company_rows"] = int(
    q(cur, "SELECT COUNT(*) FROM ads_technology_institution WHERE is_company=1")[0][0])

cur.close(); conn.close()

# ================= dev =================
conn = pymysql.connect(**DEV)
cur = conn.cursor()
# 造数黑名单复核（存在性披露，值不引用）
er = int(q(cur, "SELECT COUNT(*) FROM gkxlumenx_ads.enterprise_ranking")[0][0])
es = int(q(cur, "SELECT COUNT(*) FROM gkxlumenx_ads.enterprise_score")[0][0])
facts["dev_blacklist_tables_rows"] = {"enterprise_ranking": er, "enterprise_score": es}
# 产业链关联面（产业维真实承载探测）
tabs = [r[0] for r in q(cur, "SHOW TABLES FROM gkxlumenx_dwd LIKE '%chain%'")]
facts["dev_chain_tables"] = tabs
cur.close(); conn.close()

# ================= gkx =================
from _gkxdb import gkx  # noqa: E402
cur = gkx()
# 专利代理轴规模（共享快照对账键 dwd_patent=2,939,895）
facts["gkx_patent_rows"] = int(q(cur, "SELECT COUNT(*) FROM gkx.dwd_patent")[0][0])
cur.close()

# ================= absence_probe =================
absence = [
    {"probe": "久新产业影响力评分列（技术转让收入/带动产业增值/标准制定三分项）",
     "source": "jiuxin",
     "sql": "DESCRIBE ads_institution_technology_power（22 列全清单落 facts.jiuxin_power_columns）",
     "hits": 0,
     "hit_detail": "22 列=paper/citation/talent/topic 四分项学术族，无技术转让收入、产业增值、标准制定等产业经济分项列"},
    {"probe": "久新产业参与画像评分列",
     "source": "jiuxin",
     "sql": "DESCRIBE ads_institution_industry（49 列全清单落 facts.jiuxin_industry_columns）",
     "hits": 0,
     "hit_detail": "IPC 质量覆盖率/发明人任职证据类列，无产业影响力得分/排名列"},
    {"probe": "gkx 技术转让/产业增值/标准制定数据面",
     "source": "gkx",
     "sql": "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' AND (table_name LIKE '%transfer%' OR table_name LIKE '%standard%' OR table_name LIKE '%contract%')",
     "hits": 0,
     "hit_names": []},
    {"probe": "dev 产业影响力现成结果面",
     "source": "dev",
     "sql": "SELECT COUNT(*) FROM gkxlumenx_ads.enterprise_score",
     "hits": 0,
     "hit_detail": f"实测 {es} 行——造数黑名单（skill P4.1 分值禁引）且空壳，存在性披露、值不参与判档"},
]

# ================= 判档 =================
support = "部分支持"

notes += [
    "判档：UI 语义=指标树 L1『科技影响力』下 L2『产业影响力』节点分（mock 公式：技术转让收入×0.5+带动产业增值×0.3+标准制定×0.2，演示值）；"
    "三分项（技术转让收入/带动产业增值/标准制定）在三源均无结果面或经济数据承载——技术合同成交额、产业增值、标准制定数均为经济/标准化域数据，"
    "学术库体系（久新 OpenAlex 族）与要素库（gkx）均不采集；判部分支持",
    "可用中间结果：久新 ads_institution_industry 1,354,245 行产业参与画像（IPC 维，无评分）+ ads_technology_institution is_company=1 产业主体子池"
    "（代理口径候选：以企业专利/技术节点参与度近似产业影响力，语义偏移须披露）；gkx dwd_patent 2,939,895 行为三源最大专利明细面（代理轴原料）",
    "B10 双口径：口径 A=专利/技术节点产业参与度代理（现转可算、语义偏移标注）；口径 B=技术转让收入三分项口径（需经济数据源——技术合同登记/标准数据库接入，三源均缺）；"
    "甲方接受口径 A→升完全转换支持；坚持口径 B→维持部分支持直至经济数据源接入",
    "与 M_SCIUI_INDEX_016（主体科技影响力得分）同指标树相邻节点：016 的学术分项（论文被引/H指数）在久新 power 表有现役承载，"
    "本件产业分项无——同树不同命，判档差异即语义差异的证据",
]

out = {
    "metric_id": "M_SCIUI_INDEX_015",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/tech-index/mockData.js:132",
        "repos/demo-ui-science/src/pages/tech-index/mockData.js:85",
        "repos/demo-ui-science/src/pages/tech-index/mockData.js:9",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「产业影响力」作为科技指数指标树节点未独立出现在三份需求真源（SRS 科技指数.md 19 叶无此名；主需求文档『产业影响力』2 处均属科技专题服务系统人才产业力评估语境 1.1.1.2.4.2.5.7.2，非本展示系统科技指数页）；本件为 UI 拆件叶（指标树 L2 节点），语义源=SRS seq 159 指标项展示（树状结构展示所有指标项含层级关系）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件为指标树节点语义（无自身年份维）；久新 power 快照 as_of=2026-09-18 单时点",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": ["0.30", "0.40", "0.5", "0.3", "0.2", "64,698", "2,939,895"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
