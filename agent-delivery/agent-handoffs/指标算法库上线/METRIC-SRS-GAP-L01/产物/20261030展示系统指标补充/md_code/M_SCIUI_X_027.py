#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_X_027 主体总产值（年）—— 三源探针 + 复现脚本（批 S3-02，Lane 2）。

UI 挂载（实查）：
  repos/demo-ui-science/src/pages/tech-innovation-evaluation-new/TechInnovationEvaluationNewPage.jsx:835/:839
    政策优化建议>系统仿真模型过程>总产值（mock 序列读数，亿元口径）
  旧版 TechInnovationEvaluationPage.tsx:2477 outputOption series 总产值 2019-2025
    scaleNums([1200,1320,1450,1580,1710,1860,2010], vol) —— 演示值，不参与支持度结论

需求原文（:935 / SRS seq 148）：「收集并统计特定产业的总产值、增加值、利润等经济指标，
用户可按时间范围、地域、企业类型等维度查看产业产值情况」——真实经济指标语义（批派单书
特殊背景 §0.2 明文：专利/论文代理口径仅对照面，不得当主口径）。

三源产值面：
  ① 开发库：enterprise_finance_history 40,239 行（972 机构×1989-2026，revenue 现成，
     26,911 行营收正）——主承载候选；ods.dwd_org_annual_financial_info 90,926 行同构（gkx 镜像）
  ② gkx：dwd_org_annual_financial_info 90,926 行 8,127 机构（operating_revenue 2,191 行正）
     ——对照面：量级更大但营收覆盖更稀
  ③ 久新：203 表无企业营收/产值面（SHOW TABLES 全清单语义过滤 0 命中）

复现口径（B10 双口径）：
  口径 A（开发库企业营收聚合·主口径）：enterprise_finance_history.revenue 按年求和
  口径 B（gkx 对照面）：dwd_org_annual_financial_info.operating_revenue 按年求和
"""
import json
import os
import sys

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

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

facts["dev_finance_history_rows"] = 40239  # 探针 c 实测（B11 零漂移 assert）
assert q1(dc, "SELECT COUNT(*) FROM gkxlumenx_dwd.enterprise_finance_history") == \
    facts["dev_finance_history_rows"]

facts["dev_finance_orgs"] = q1(
    dc, "SELECT COUNT(DISTINCT org_id) FROM gkxlumenx_dwd.enterprise_finance_history")
facts["dev_finance_orgs_rev_pos"] = q1(
    dc, "SELECT COUNT(*) FROM (SELECT org_id FROM gkxlumenx_dwd.enterprise_finance_history "
        "WHERE revenue IS NOT NULL AND revenue>0 GROUP BY org_id) t")

# 年谱：按年营收和（口径 A 主读数，亿元换算）
dc.execute(
    "SELECT data_year, COUNT(*) c, COUNT(DISTINCT org_id) orgs, "
    "SUM(revenue) tot_rev FROM gkxlumenx_dwd.enterprise_finance_history "
    "WHERE revenue IS NOT NULL AND revenue>0 GROUP BY data_year ORDER BY data_year")
yearly = [{"year": int(r[0]), "rows": int(r[1]), "orgs": int(r[2]),
           "revenue_sum_yuan": float(r[3]),
           "revenue_sum_yi": round(float(r[3]) / 1e8, 2)} for r in dc.fetchall()]
facts["dev_revenue_yearly"] = yearly

# 近三年主体总产值读数（口径 A 主值）
by_year = {r["year"]: r for r in yearly}
facts["dev_total_output_2023_yi"] = by_year.get(2023, {}).get("revenue_sum_yi")
facts["dev_total_output_2024_yi"] = by_year.get(2024, {}).get("revenue_sum_yi")
facts["dev_total_output_2025_yi"] = by_year.get(2025, {}).get("revenue_sum_yi")

# 深圳区级切片（需求「地域」维）
dc.execute(
    "SELECT b.district, COUNT(DISTINCT f.org_id) orgs, SUM(f.revenue)/100000000 rev_yi "
    "FROM gkxlumenx_dwd.enterprise_finance_history f "
    "JOIN gkxlumenx_dwd.enterprise_base b ON f.org_id=b.org_id "
    "WHERE f.data_year=2024 AND f.revenue IS NOT NULL AND f.revenue>0 "
    "AND b.city LIKE '%深圳%' AND b.district IS NOT NULL "
    "GROUP BY b.district ORDER BY rev_yi DESC")
facts["dev_2024_revenue_by_sz_district_yi"] = [
    {"district": r[0], "orgs": int(r[1]), "revenue_yi": float(r[2])} for r in dc.fetchall()]

# 同年同机构多行现象（数据质量披露：dup=4 的 7,694 对是多报表源并存）
dc.execute(
    "SELECT dup_n, COUNT(*) pairs FROM (SELECT org_id, data_year, COUNT(*) dup_n "
    "FROM gkxlumenx_dwd.enterprise_finance_history WHERE revenue IS NOT NULL AND revenue>0 "
    "GROUP BY org_id, data_year) t GROUP BY dup_n ORDER BY dup_n")
facts["dev_dup_pairs_by_n"] = [{"dup_n": int(r[0]), "pairs": int(r[1])} for r in dc.fetchall()]
dev.close()

# ================================================================ ② gkx（对照面）
from _gkxdb import gkx  # noqa: E402

gc = gkx()
facts["gkx_org_financial_rows"] = 90926  # 探针 a 实测（B11）
facts["gkx_org_financial_orgs"] = 8127   # 探针 b 实测（B11）
gc.execute(
    "SELECT COUNT(*) FROM gkx.dwd_org_annual_financial_info "
    "WHERE operating_revenue IS NOT NULL AND operating_revenue>0")
facts["gkx_org_financial_rev_pos_rows"] = int(gc.fetchone()[0])
gc.execute(
    "SELECT COUNT(*) FROM (SELECT org_id FROM gkx.dwd_org_annual_financial_info "
    "WHERE operating_revenue IS NOT NULL AND operating_revenue>0 "
    "GROUP BY org_id HAVING COUNT(DISTINCT year)>=2) t")
facts["gkx_org_financial_orgs_multiyear"] = int(gc.fetchone()[0])
gc.close()

# ================================================================ ③ 久新（absence 留证）
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=30, read_timeout=300)
jx = pymysql.connect(**JX)
jc = jx.cursor()
jc.execute("SHOW TABLES")
all_tables = [r[0] for r in jc.fetchall()]
facts["jiuxin_tables_total"] = len(all_tables)
econ_like = [t for t in all_tables if any(
    k in t.lower() for k in ("company", "economic", "output_value", "revenue",
                             "finance", "finance_history", "gdp"))]
facts["jiuxin_econ_like_tables"] = econ_like
absence_probe.append({
    "probe": "久新企业营收/产值面（SHOW TABLES 203 张全清单 company/economic/output_value/"
             "revenue/finance/gdp 语义过滤）",
    "source": "jiuxin",
    "sql": "SHOW TABLES —— 203 张 ads_* 均为科技要素/评估/推荐面，无企业财务年报面",
    "hits": len(econ_like),
})
jx.close()

# 开发库 absence 注记：无「产业总产值」官方统计结果面（有企业明细可聚合）
absence_probe.append({
    "probe": "开发库产业级总产值结果面（区别于企业明细聚合）",
    "source": "dev",
    "sql": "经济产值类表扫描 9 表 —— enterprise_finance_history（企业年明细）/financing/"
           "forg_finance_history/svc_org_finance_event/ods 财务 4 表，无产业级汇总表",
    "hits": 0,
})

# ================================================================ 派生与产物
r23 = by_year.get(2023, {}).get("revenue_sum_yuan", 0)
r24 = by_year.get(2024, {}).get("revenue_sum_yuan", 0)
r25 = by_year.get(2025, {}).get("revenue_sum_yuan", 0)
derived = [
    {"key": "dev_output_growth_2024_pct", "value": round((r24 - r23) / r23 * 100, 2),
     "numerator": round(r24 - r23, 0), "denominator": r23,
     "note": "分子=2024-2023 营收和差（同表同年谱），分母=2023 营收和；口径 A 聚合值增长"},
    {"key": "dev_output_growth_2025_pct", "value": round((r25 - r24) / r24 * 100, 2),
     "numerator": round(r25 - r24, 0), "denominator": r24,
     "note": "分子=2025-2024 营收和差，分母=2024 营收和（同表同年谱）"},
    {"key": "dev_rev_pos_org_coverage_pct", "value": round(
        facts["dev_finance_orgs_rev_pos"] / facts["dev_finance_orgs"] * 100, 2),
     "numerator": facts["dev_finance_orgs_rev_pos"],
     "denominator": facts["dev_finance_orgs"],
     "note": "分子=有正营收的机构数，分母=财务表全部机构数（同表去重计数）"},
]

out = {
    "metric_id": "M_SCIUI_X_027",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation-new/TechInnovationEvaluationNewPage.jsx:835",
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation-new/TechInnovationEvaluationNewPage.jsx:839",
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation/TechInnovationEvaluationPage.tsx:2477",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "《科技创新评估.md》seq 148（excel_row 151）「产业产值分析」功能命中："
                "「收集并统计特定产业的总产值、增加值、利润等经济指标」；需求主文档 :935 同文。"
                "「主体总产值」为 471 导出 l3「政策优化建议>系统仿真模型过程>总产值」的指标化命名，"
                "「主体」指评估对象（企业/机构），非行政区划全域。",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": "部分支持",
    "notes": [
        "本件支持度按三源评估（20261101 铁律）；产值=真实经济指标语义（批派单书 §0.2）。",
        "主承载在开发库：enterprise_finance_history 40,239 行（972 机构，1989-2026 年谱连续，"
        "营收正 26,911 行覆盖近 100% 机构）——「主体总产值」按口径 A 企业营收和现转。",
        "量级警示：2024 年营收和仅约 15.74 亿元级（972 家内企业样本），与 UI mock 2,010 亿元"
        "差两个数量级——库内是样本库非全域统计，读数须带「972 家样本」限定语。",
        "同年同机构多行现象在案：dup=4 的 7,694 对（多报表源并存），聚合前须按 org×year 去重"
        "规则裁定（本件按全行求和口径 A，去重口径留待裁定，见 §1.6 触发器）。",
        "gkx 对照面 90,926 行 8,127 机构但营收正仅 2,191 行（覆盖率 2.4%）——量级大覆盖稀，"
        "作对照不作主源；久新 203 表无企业营收面（absence 留证）。",
        "「产业总产值」官方口径（统计部门规模工业总产值类）三源均无——只有企业明细可聚合，"
        "产业→企业归属映射（哪 972 家属于哪个产业）未在库内闭合，产业维切片暂不可行。",
        "derived 三比分子分母均同表同源（B3）；year 谱含 2026 年 665 行（在途年，读数勿对外）。",
    ],
    "base_years_used": ["2023", "2024", "2025"],
    "base_years_missing": [],
    "base_years_note": "营收年谱 1989-2026 连续在库（2026 为在途年 665 行已披露）；"
                       "UI mock 2019-2025 七年全在年谱内，无基期缺口；"
                       "「缺年」不适用（非时序比率指标）。",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "835", "839", "2477", "148", "151", "935", "40239", "972", "26911",
        "90926", "8127", "2191", "2.4", "2010", "203", "7694", "665",
    ]},
}
with open(os.path.join(HERE, "M_SCIUI_X_027_out.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("M_SCIUI_X_027 out.json written: yearly", len(yearly),
      "2024_yi", facts["dev_total_output_2024_yi"])
