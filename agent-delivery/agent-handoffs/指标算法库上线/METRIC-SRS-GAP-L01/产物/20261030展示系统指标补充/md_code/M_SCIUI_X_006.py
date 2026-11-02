#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_X_006 技术创新空间分布 —— 三源探针 + 复现脚本（批 S3-02，Lane 2）。

UI 挂载（实查）：
  repos/demo-ui-science/src/pages/tech-innovation-evaluation/TechInnovationEvaluationPage.tsx:3699-3705
    {techSub === 'spatial' ? <Panel title="技术创新空间分布"
      subtitle="区域排名与热力分布定位创新地域集中度和外溢不足。">…热力图+区域排名双图
  数据源 :1508-1529 spatialRegionRows —— 深圳九区（SHENZHEN_DISTRICT_OPTIONS），
    value = clamp(42..99, round((66 + hashLift + selectedLift + positionLift) × volumeScale))
    —— 全演示值（mock），不参与支持度结论
  同页 :2963 ['spatial','技术创新空间分布'] 子 Tab；:2144 专利数量统计 region 维复用同 rows

三源：
  ① 开发库：enterprise_base 269,511 行含 province/city/district 区级列（深圳 95,600）；
     专利 4 表 3 空 + org_rel 969 行纯关系（无专利计数）→ 专利×区级链断
  ② gkx：dwd_patent 2,939,895 行 55 列无省市列（唯一地域列 country/country_code 100% CN）；
     申请人名采样 2,000 行仅 21 行带「省」字前缀 → 省份解析不可行
  ③ 久新：ads_sz_gkx_industry_cluster 15 集群（深圳战新+未来产业，patent_count 现成）；
     ads_geo_yearly_metrics 171,736 行无专利列（共享快照+DESC 实查）；机构专利分析面
     resolution 覆盖率 1.93%（INNOV_001 在案）

复现口径（B10 双口径）：
  口径 A（区级企业密度·开发库现转）：enterprise_base 深圳九区计数 → 区排名 + 热力值
  口径 B（产业集群专利分布·久新现转）：sz_gkx_industry_cluster.patent_count 集群榜
"""
import json
import os
import sys

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=30, read_timeout=600)
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           connect_timeout=20, read_timeout=180)

facts = {}
absence_probe = []


def q1(cur, sql):
    cur.execute(sql)
    r = cur.fetchone()
    return int(r[0]) if r else 0


# ================================================================ ① 开发库（口径 A 主源）
dev = pymysql.connect(**DEV)
dc = dev.cursor()

facts["dev_enterprise_base_rows"] = 269511  # 探针 e-dev 实测（B11 零漂移 assert）
assert q1(dc, "SELECT COUNT(*) FROM gkxlumenx_dwd.enterprise_base") == facts["dev_enterprise_base_rows"]

# 深圳九区企业计数（区排名主读数）
dc.execute(
    "SELECT district, COUNT(*) c FROM gkxlumenx_dwd.enterprise_base "
    "WHERE city LIKE '%深圳%' AND district IS NOT NULL AND district!='' "
    "GROUP BY district ORDER BY c DESC")
district_rows = [{"district": r[0], "enterprises": int(r[1])} for r in dc.fetchall()]
facts["dev_shenzhen_district_enterprises"] = district_rows
facts["dev_shenzhen_enterprises_total"] = sum(r["enterprises"] for r in district_rows)

# 热力值（min-max 42-99 对齐 UI 色标区间，纯展示层归一）
vals = [r["enterprises"] for r in district_rows]
lo, hi = min(vals), max(vals)
for r in district_rows:
    r["heatmap_42_99"] = round(42 + (r["enterprises"] - lo) / (hi - lo) * (99 - 42), 2) if hi > lo else 42.0

# 集中度：Top1/Top3 区占深圳企业比重（B3 分母=深圳九区合计，同源）
top1 = district_rows[0]["enterprises"]
top3 = sum(r["enterprises"] for r in district_rows[:3])
total = facts["dev_shenzhen_enterprises_total"]

# 开发库专利×区级断链 absence 探针（三源铁律：负结论留证）
for tbl in ["enterprise_patent_detail", "enterprise_patent_history", "enterprise_chain_patent"]:
    absence_probe.append({
        "probe": f"开发库专利表 {tbl} 行数（专利×区级链路）",
        "source": "dev",
        "sql": f"SELECT COUNT(*) FROM gkxlumenx_dwd.{tbl}",
        "hits": q1(dc, f"SELECT COUNT(*) FROM gkxlumenx_dwd.{tbl}"),
    })
absence_probe.append({
    "probe": "开发库 enterprise_patent_org_rel 行数（969 行纯关系无计数）",
    "source": "dev",
    "sql": "SELECT COUNT(*) FROM gkxlumenx_dwd.enterprise_patent_org_rel",
    "hits": q1(dc, "SELECT COUNT(*) FROM gkxlumenx_dwd.enterprise_patent_org_rel"),
})
dev.close()

# ================================================================ ② gkx（absence 留证）
from _gkxdb import gkx  # noqa: E402

gc = gkx()
# 55 列无省市列（探针 a 已全列在案），此处数据级复证：country_code 采样分布
gc.execute(
    "SELECT country_code, COUNT(*) c FROM (SELECT country_code FROM gkx.dwd_patent "
    "WHERE country_code IS NOT NULL LIMIT 200000) t GROUP BY country_code ORDER BY c DESC LIMIT 5")
cc_rows = [{"country_code": r[0], "sample_rows": int(r[1])} for r in gc.fetchall()]
facts["gkx_patent_countrycode_sample_top5"] = cc_rows
facts["gkx_patent_rows_total"] = 2939895  # 共享快照 dims.gkx[2]（B11）
absence_probe.append({
    "probe": "gkx dwd_patent 55 列省市/地址列存在性（探针 a 全列清单 0 命中）",
    "source": "gkx",
    "sql": "SELECT column_name FROM information_schema.columns WHERE table_schema='gkx' "
           "AND table_name='dwd_patent' AND (column_name LIKE '%prov%' OR column_name LIKE "
           "'%city%' OR column_name LIKE '%addr%' OR column_name LIKE '%region%' "
           "OR column_name LIKE '%district%')",
    "hits": 0,
})
absence_probe.append({
    "probe": "gkx 专利申请人名省份前缀解析率（采样 2,000，探针 b）",
    "source": "gkx",
    "sql": "SELECT … REGEXP '省|市' … FROM (SELECT first_applicant_name FROM gkx.dwd_patent "
           "LIMIT 2000) t —— 采样，非全表；命中 21 行含「广东」等前缀",
    "hits": 21,
})
gc.close()

# ================================================================ ③ 久新（口径 B 主源）
jx = pymysql.connect(**JX)
jc = jx.cursor()

facts["jiuxin_sz_cluster_rows"] = q1(jc, "SELECT COUNT(*) FROM ads_sz_gkx_industry_cluster")
jc.execute(
    "SELECT cluster_code, cluster_name_zh, `group_name`, patent_count, "
    "fractional_patent_count, industry_member_count FROM ads_sz_gkx_industry_cluster "
    "ORDER BY patent_count DESC")
cluster_rows = [
    {"cluster_code": r[0], "cluster_name_zh": r[1], "group_name": r[2],
     "patent_count": int(r[3] or 0), "fractional_patent_count": float(r[4] or 0),
     "industry_member_count": int(r[5] or 0)}
    for r in jc.fetchall()]
facts["jiuxin_sz_clusters"] = cluster_rows
facts["jiuxin_sz_patent_total"] = sum(r["patent_count"] for r in cluster_rows)

# 久新 geo 表无专利列 absence（DESC 实查在 _probe_lane2_s302d：paper/project/talent/institution/mobility）
absence_probe.append({
    "probe": "久新 ads_geo_yearly_metrics 专利列存在性（DESC 13 列实查）",
    "source": "jiuxin",
    "sql": "DESC ads_geo_yearly_metrics —— paper_count/project_count/talent_count/"
           "institution_count/new_institution_count/inbound_talent_count 等，无 patent 列",
    "hits": 0,
})
jx.close()

# ================================================================ 派生与产物
derived = [
    {"key": "dev_top1_district_share_pct", "value": round(top1 / total * 100, 2),
     "numerator": top1, "denominator": total,
     "note": "分子=宝安区企业数，分母=深圳九区企业合计（同表同源计数）"},
    {"key": "dev_top3_district_share_pct", "value": round(top3 / total * 100, 2),
     "numerator": top3, "denominator": total,
     "note": "分子=前三区（宝安/龙岗/南山）企业数和，分母=深圳九区企业合计（同表同源）"},
    {"key": "jiuxin_top1_cluster_patent_share_pct", "value": round(
        cluster_rows[0]["patent_count"] / facts["jiuxin_sz_patent_total"] * 100, 2),
     "numerator": cluster_rows[0]["patent_count"],
     "denominator": facts["jiuxin_sz_patent_total"],
     "note": "分子=新一代信息技术集群专利数，分母=15 集群专利合计（同表同源）"},
]

out = {
    "metric_id": "M_SCIUI_X_006",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation/TechInnovationEvaluationPage.tsx:3699",
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation/TechInnovationEvaluationPage.tsx:1508",
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation/TechInnovationEvaluationPage.tsx:2963",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "《科技创新评估.md》seq 144（excel_row 147）「技术创新空间分布」同名命中，功能描述原文见附录 A；"
                "需求主文档 :905-907 同文复述。UI 挂载组件为科技创新评估页技术创新力指标展示>空间分布子 Tab。",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": "部分支持",
    "notes": [
        "本件支持度按「开发库 + 三方库（gkx）+ 久新库（jiuxin_warehouse）」三源评估（20261101 三源铁律）。",
        "UI spatialRegionRows 九区 value 42-99 与申请量×4.2 均为演示值（mock），不参与支持度结论。",
        "专利×区级链路在开发库断链：enterprise_patent_detail/history/chain_patent 三表 0 行，"
        "org_rel 969 行纯关系无计数值——区级读数现转只能用企业密度代理（口径 A）。",
        "gkx 专利 293.99 万行无省市列且 country_code 采样 100% CN（受理局维度无区域区分度），"
        "申请人名省份解析采样命中率约 1%（21/2000，采样非全表），不可作区域维。",
        "口径 A 是「企业空间分布」非「技术创新空间分布」——语义降级披露：密度代理 ≠ 专利产出分布。",
        "口径 B 集群维度与 UI 区级维度不同物（集群≠行政区），作产业视角对照面。",
        "derived 三比分子分母均同表同源（B3）。",
    ],
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件为截面空间分布读数（区/集群粒度），产物无年度键、无时序分母，"
                       "不存在基期年缺口；专利申请年序列在 gkx 有 apdt_year 但区域链断，"
        "未构成可用年谱，不属「缺年按 0 摊入」情形。",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "3699", "1508", "2963", "144", "147", "269511", "95600", "95,600", "42", "99",
        "4.2", "2000", "2939895", "2,939,895", "171736", "1.93", "905", "907",
    ]},
}
with open(os.path.join(HERE, "M_SCIUI_X_006_out.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("M_SCIUI_X_006 out.json written:",
      "districts", len(district_rows), "clusters", len(cluster_rows))
