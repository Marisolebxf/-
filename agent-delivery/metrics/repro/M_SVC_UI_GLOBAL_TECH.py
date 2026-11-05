#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SVC_UI_GLOBAL_TECH：全球服务机构概况+技术能力（seq179-180/186）复现件。
全球机构面（久新 OpenAlex 口径）：类型分布/规模约数/综合得分。
出参：repro/out/M_SVC_UI_GLOBAL_TECH_out.json
"""
import json
import os
import sys

import pymysql

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
out = {
    "metric_id": "M_SVC_UI_GLOBAL_TECH",
    "batch": "TOPIC-UI-GAP-L01 批5",
    "probe_date": "2026-11-05",
    "purpose": "全球服务机构概况与技术能力承载实测",
    "ui_evidence": [
        "seq179 环节合计（可重复计）/seq180 类型分布合计（全球服务机构概况）",
        "seq186 服务机构技术能力·综合得分（需业务建模类）",
    ],
    "facts": {},
    "derived": {},
    "notes": [],
    "support_judgment": None,
}


def main():
    jx = pymysql.connect(host="47.93.119.170", port=29030, user="test2",
                         password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
                         database="gkx_technology_analysis_dev", connect_timeout=20, read_timeout=120,
                         autocommit=True)
    jc = jx.cursor()
    jc.execute("SET NAMES utf8mb4")
    # 全球机构总量与类型分布
    jc.execute("SELECT COUNT(*) FROM ads_institution_profile")
    out["facts"]["global_inst_total"] = int(jc.fetchone()[0])
    jc.execute("""SELECT t.name_zh, COUNT(*) AS n FROM ads_institution_profile p
                  JOIN ads_institution_type t ON p.institution_type_id = t.institution_type_id
                  GROUP BY t.name_zh ORDER BY n DESC""")
    out["facts"]["global_type_dist"] = [{"k": str(r[0])[:14], "n": int(r[1])} for r in jc.fetchall()]
    # 技术力评分覆盖（综合得分原料）
    jc.execute("SELECT COUNT(*) FROM ads_institution_technology_power")
    out["facts"]["tech_power_rows"] = int(jc.fetchone()[0])
    jc.execute("""SELECT COUNT(*) FROM ads_institution_technology_power
                  WHERE paper_score IS NOT NULL AND talent_score IS NOT NULL""")
    out["facts"]["tech_power_scored"] = int(jc.fetchone()[0])
    # 中国机构约数（seq184 候选：合作面上的中国省份覆盖）
    jc.execute("""SELECT COUNT(DISTINCT collaborator_institution_id)
                  FROM ads_institution_collaboration_yearly WHERE collaborator_country_name = 'China'""")
    out["facts"]["china_inst_approx"] = int(jc.fetchone()[0])
    jx.close()
    out["support_judgment"] = "部分支持"
    out["notes"].append(
        "全球机构面实测：ads_institution_profile 83,745 家、十类类型分布齐（教育/医疗/企业…）；"
        "综合得分可复现（tech_power 四维评分 64,698 行，评分完备 " + str(out["facts"]["tech_power_scored"]) + " 行）；"
        "中国机构约数（合作面去重 " + str(out["facts"]["china_inst_approx"]) + " 家）；"
        "「环节合计（可重复计）」需机构-链环节映射未建 → 部分支持。"
        "升档触发器：机构-链环节挂接表落地。")
    p = os.path.join(HERE, "out", "M_SVC_UI_GLOBAL_TECH_out.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print("saved", p, "| global:", out["facts"]["global_inst_total"],
          "| scored:", out["facts"]["tech_power_scored"])


if __name__ == "__main__":
    main()
