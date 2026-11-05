#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_B5_SVC_BATCH_PROBE：批5（产业服务链分析块 seq75-92 共 18 项）三源探针。
结构面：live gkxlumenx_ads 10 张 svc_* 预构表（结构齐/数据空=待灌）；gkx 科技机构/专利/项目原料面实测。
出参：repro/out/M_B5_SVC_BATCH_PROBE_out.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx, live  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "out", "M_B5_SVC_BATCH_PROBE_out.json")
out = {
    "metric_id": "M_B5_SVC_BATCH_PROBE",
    "batch": "TOPIC-UI-GAP-L01 批5",
    "probe_date": "2026-11-05",
    "purpose": "产业服务链分析块（seq75-92）三源探针：svc_ads 结构面 + gkx 原料面",
    "ui_evidence": [
        "live 30892 产业服务链分析（seq75-92）：服务机构产业领域分析/技术力评估/服务链图谱/引入与培育推荐/服务链专题服务",
        "页面证据 SvcOrgCoverageBoard.vue:L215、SvcOrgCapabilityBoard.vue:L345、ServiceChainAnalysisWorkspace.vue:L723、svcRecommendAttractWorkspace.ts:L18-25、ServicePortalShell.vue:L22-23",
    ],
    "facts": {"svc_ads_tables": {}, "gkx_raw": {}},
    "notes": [],
}


def main():
    # ① live ads 十张 svc 预构表（结构）
    conn = live("ADS")
    with conn.cursor() as c:
        for t in ["svc_attraction_recommend", "svc_chain_gap", "svc_cultivation_recommend",
                  "svc_metric_dist", "svc_metric_fact", "svc_metric_series",
                  "svc_org_card", "svc_region_dist", "svc_relation_chain", "svc_tech_power_score"]:
            c.execute(f"SELECT COUNT(*) AS n FROM `{t}`")
            n = int(c.fetchone()["n"])
            c.execute(f"SHOW COLUMNS FROM `{t}`")
            cols = [r["Field"] for r in c.fetchall()]
            out["facts"]["svc_ads_tables"][t] = {"rows": n, "cols_n": len(cols), "cols": cols}
    conn.close()
    # ② gkx 原料面
    cur = gkx()
    g = out["facts"]["gkx_raw"]
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_forg_research_org_info")
    g["research_org_rows"] = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_forg_research_org_info WHERE country = 'China'")
    g["research_org_china"] = int(cur.fetchone()[0])
    cur.execute("""SELECT org_type, COUNT(*) AS n FROM gkx.dwd_forg_research_org_info
                   WHERE org_type IS NOT NULL AND LOWER(org_type) NOT IN ('','null','nan','none')
                   GROUP BY org_type ORDER BY n DESC LIMIT 8""")
    g["research_org_type"] = [{"k": str(r[0])[:18], "n": int(r[1])} for r in cur.fetchall()]
    cur.execute("""SELECT city, COUNT(*) AS n FROM gkx.dwd_forg_research_org_info
                   WHERE country='China' AND city IS NOT NULL AND LOWER(city) NOT IN ('','null','nan','none')
                   GROUP BY city ORDER BY n DESC LIMIT 6""")
    g["research_org_china_city"] = [{"k": str(r[0])[:12], "n": int(r[1])} for r in cur.fetchall()]
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_forg_university_org_info")
    g["university_rows"] = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_forg_executive_info")
    g["forg_executive_rows"] = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_zh_project")
    g["zh_project_rows"] = int(cur.fetchone()[0])
    cur.execute("""SELECT COUNT(*), SUM(funded_amount) FROM gkx.dwd_zh_project
                   WHERE funded_amount IS NOT NULL AND funded_amount > 0""")
    r = cur.fetchone()
    g["zh_project_funded_n"], g["zh_project_funded_sum_wan"] = int(r[0]), round(float(r[1]), 2)
    cur.execute("""SELECT approval_year, COUNT(*) AS n FROM gkx.dwd_zh_project
                   WHERE approval_year IS NOT NULL GROUP BY approval_year ORDER BY n DESC LIMIT 5""")
    g["zh_project_year_top"] = [{"k": str(r[0])[:10], "n": int(r[1])} for r in cur.fetchall()]
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_patent_applicants")
    g["patent_applicants_rows"] = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(DISTINCT patent_id) FROM gkx.dwd_patent_applicants")
    g["patent_with_applicants"] = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_patent")
    g["patent_total"] = int(cur.fetchone()[0])
    cur.execute("""SELECT COUNT(*) FROM (
                     SELECT patent_id FROM gkx.dwd_patent_applicants
                     GROUP BY patent_id HAVING COUNT(DISTINCT name) > 1) t""")
    g["joint_patents_all"] = int(cur.fetchone()[0])
    cur.execute("""SELECT COUNT(DISTINCT name) FROM gkx.dwd_patent_applicants WHERE name LIKE %s""", ("%深圳%",))
    g["sz_patent_applicant_orgs"] = int(cur.fetchone()[0])
    cur.execute("""SELECT COUNT(*) FROM (
                     SELECT patent_id FROM gkx.dwd_patent_applicants
                     WHERE patent_id IN (SELECT patent_id FROM gkx.dwd_patent_applicants WHERE name LIKE %s)
                     GROUP BY patent_id HAVING COUNT(DISTINCT name) > 1) t""", ("%深圳%",))
    g["joint_patents_sz_involved"] = int(cur.fetchone()[0])
    cur.execute("""SELECT org_tag, COUNT(DISTINCT org_id) AS n FROM gkx.dwd_org_tech_tag
                   WHERE org_tag IN ('工程技术研究中心','企业技术中心','国家级专精特新小巨人企业','专精特新小巨人企业')
                   GROUP BY org_tag ORDER BY n DESC""")
    g["svc_like_tags"] = [{"k": str(r[0])[:16], "n": int(r[1])} for r in cur.fetchall()]
    cur.close()
    out["notes"].append(
        "结构面核心发现：live gkxlumenx_ads 十张 svc_* 预构表结构齐（attraction_recommend/cultivation_recommend/"
        "tech_power_score/relation_chain/region_dist/metric_fact/…）但实测全部 0 行——待灌数（须走 ods_sync/灌数审批，本次未写库）；"
        "gkx 原料面实测：科研机构 20,000（中国 1,843，facility 7,329/education 3,360）、高校 20,000、"
        "国家自然基金项目 58,453（金额合计 252.91 万万=252.9 亿?按万元口径落产物）、专利申请人 28,964 行（联合专利 6,477 件、深圳涉 45 件）。")
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("saved", OUT_PATH)
    for t, v in out["facts"]["svc_ads_tables"].items():
        print(f"  {t}: {v['rows']} rows / {v['cols_n']} cols")


if __name__ == "__main__":
    main()
