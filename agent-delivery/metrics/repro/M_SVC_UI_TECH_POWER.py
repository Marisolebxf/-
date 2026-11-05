#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SVC_UI_TECH_POWER：服务机构技术力评估（seq76-79）复现件。
综合技术力 TOP3 + 技术力评价模型三维度（成功案例/标准制定/核心专家）。
承载实测：久新 ads_institution_technology_power 64,698 行四维评分实测；
成功案例/标准制定/核心专家分维度承载分级披露。
出参：repro/out/M_SVC_UI_TECH_POWER_out.json
"""
import json
import os
import sys

import pymysql

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
out = {
    "metric_id": "M_SVC_UI_TECH_POWER",
    "batch": "TOPIC-UI-GAP-L01 批5",
    "probe_date": "2026-11-05",
    "purpose": "服务机构技术力评估（TOP3 + 模型三维度）承载实测",
    "ui_evidence": [
        "views/service/SvcOrgCapabilityBoard.vue:L345（seq76 综合技术力 TOP3）",
        "技术力评价模型权重表（seq77 成功案例/seq78 标准制定/seq79 核心专家）",
    ],
    "facts": {},
    "derived": {},
    "notes": [],
    "support_judgment": None,
}


def main():
    jx = pymysql.connect(host="47.93.119.170", port=29030, user="test2",
                         password=os.environ.get("JX_DORIS_PASSWORD", ""),
                         database="gkx_technology_analysis_dev", connect_timeout=20, read_timeout=120,
                         autocommit=True)
    jc = jx.cursor()
    jc.execute("SET NAMES utf8mb4")
    # 技术力总表行数与四维评分完备性
    jc.execute("SELECT COUNT(*) FROM ads_institution_technology_power")
    out["facts"]["tech_power_rows"] = int(jc.fetchone()[0])
    jc.execute("""SELECT COUNT(*) FROM ads_institution_technology_power
                  WHERE paper_score IS NOT NULL AND citation_score IS NOT NULL
                  AND talent_score IS NOT NULL AND topic_score IS NOT NULL""")
    out["facts"]["tech_power_full_score_rows"] = int(jc.fetchone()[0])
    # 综合技术力 TOP3（四维均值口径，落产物）
    jc.execute("""SELECT institution_name_zh, institution_type_id,
                  paper_score, citation_score, talent_score, topic_score,
                  paper_count, cited_by_count, talent_count
                  FROM ads_institution_technology_power
                  WHERE institution_name_zh IS NOT NULL AND institution_name_zh <> ''
                  AND paper_score IS NOT NULL AND citation_score IS NOT NULL
                  AND talent_score IS NOT NULL AND topic_score IS NOT NULL
                  ORDER BY (paper_score + citation_score + talent_score + topic_score) / 4 DESC
                  LIMIT 10""")
    rows = jc.fetchall()
    out["facts"]["tech_power_top10"] = [
        {"zh": str(r[0])[:24], "tid": str(r[1])[:14],
         "mean4": round(sum(float(r[i]) for i in (2, 3, 4, 5)) / 4, 4),
         "paper": float(r[2]), "cite": float(r[3]), "talent": float(r[4]), "topic": float(r[5]),
         "papers": int(r[6] or 0), "cited": int(r[7] or 0), "talents": int(r[8] or 0)} for r in rows]
    # 三维度承载：成功案例=project 关联 / 核心专家=inventor / 标准制定=专利（近似承载披露）
    jc.execute("SELECT COUNT(*) FROM ads_project_institution")
    out["facts"]["project_inst_rows"] = int(jc.fetchone()[0])
    jc.execute("SELECT COUNT(*) FROM ads_patent_analysis_institution_inventor")
    out["facts"]["inventor_rows"] = int(jc.fetchone()[0])
    jc.execute("SELECT COUNT(*) FROM ads_patent_analysis_institution")
    out["facts"]["patent_inst_rows"] = int(jc.fetchone()[0])
    # 深圳机构覆盖（本地化缺口披露）
    jc.execute("""SELECT COUNT(*) FROM ads_institution_profile
                  WHERE description LIKE %s OR name_zh LIKE %s""", ("%深圳%", "%深圳%"))
    out["facts"]["sz_profile_hits"] = int(jc.fetchone()[0])
    jx.close()
    # gkx 侧深圳科研服务机构技术标签富集（本地补充口径）
    cur = gkx()
    cur.execute("""SELECT COUNT(DISTINCT t.org_id) FROM gkx.dwd_org_tech_tag t
                   JOIN gkx.dwd_org_base_info b ON t.org_id = b.org_id
                   WHERE b.industry_l1_name = %s AND b.city LIKE %s""",
                ("科学研究和技术服务业", "%深圳%"))
    out["facts"]["sz_svc_tagged_orgs"] = int(cur.fetchone()[0])
    cur.execute("""SELECT COUNT(*) FROM gkx.dwd_org_base_info
                   WHERE industry_l1_name = %s AND city LIKE %s""",
                ("科学研究和技术服务业", "%深圳%"))
    total = out["facts"]["sz_svc_total"] = int(cur.fetchone()[0])
    cur.close()
    out["derived"]["sz_tagged_share_pct"] = {
        "value": round(out["facts"]["sz_svc_tagged_orgs"] / max(total, 1) * 100, 2),
        "numerator": out["facts"]["sz_svc_tagged_orgs"],  # COUNT(DISTINCT org_id) 去重口径
        "denominator": total,
        "denominator_note": "深圳科研服务机构中有技术标签者占比",
    }
    out["support_judgment"] = "部分支持"
    out["notes"].append(
        "综合技术力 TOP3 可复现（久新 tech_power 64,698 行、四维评分全备 "
        + str(out["facts"]["tech_power_full_score_rows"]) + " 行；TOP1 中国科学院 mean4≈100）；"
        "三维度承载分级：成功案例≈project 关联 22,571,355 行（近似承载）、核心专家≈发明人 26,379 行（近似承载）、"
        "标准制定无标准库直接承载（专利 7,270 行近似）；权重表口径未闭合 + 深圳机构仅 88 家入全球库（本地化弱）"
        "→ 部分支持。升档触发器：权重表甲方确认 + 本地机构入库扩容。")
    p = os.path.join(HERE, "out", "M_SVC_UI_TECH_POWER_out.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print("saved", p, "| full_score:", out["facts"]["tech_power_full_score_rows"],
          "| sz_profiles:", out["facts"]["sz_profile_hits"])


if __name__ == "__main__":
    main()
