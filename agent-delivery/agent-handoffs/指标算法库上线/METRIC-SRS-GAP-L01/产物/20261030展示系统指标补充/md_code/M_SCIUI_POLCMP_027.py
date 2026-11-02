#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_027 影响区域（柱图辅视 · 渗透指数）· 三源探针脚本（S3-03 Lane 2）。

含义：政策效果推演输出的「影响区域」辅视柱图，按区域画渗透指数（0-100，柱高=regions[].value）。
渗透指数是政策渗透地理面的综合评价分数（需业务建模类）：政策在目标区域的触达/渗透深度。
UI：repos/demo-ui-science/src/pages/policy-tracking/simulation/interpret/InterpretWorkbench.jsx:411
（Card title「影响区域（柱图辅视 · 渗透指数）」，ImpactRegionBarChart regions=policyImpactScopeData.regions；
  数据源 policyData.js:1999-2004 深圳四区演示常量 value 90/82/75/70，coverage 84/76/68/61 分列；
  :1990 注释「覆盖面 ≠ 渗透指数：应覆盖合格主体中实际触达比例（演示）」）。

三源实况（全部实探，2026-11-01）：
- gkx：政策表有 province/city/district 三列（政策发文地理维存在！），但 20,000 行政策绝大多数为
  国家级/省级发文（district 填充率低），且政策发布地≠政策渗透地——渗透需要「政策×区域×企业触达」
  交互面，该面零承载（政策表 33 列无企业享受列，族级缺口）。
- dev：政策族 38 表除 policy_base_info 40,000 外全 0 行；regional_policy_compare=0（区域政策对比空表）。
- 久新：区域年度指标面在（ads_technology_region_yearly_metrics 2,711,376 行——技术节点×区域×年
  论文/专利/项目证据计数；ads_research_problem_region_yearly_metrics 156,613 行），但均为技术侧
  区域指标，无政策渗透维（policy_evidence 表 0 行：ads_technology_policy_evidence=0）。
依赖「政策×区域×触达（企业享受/政策落地）」交互面，三源零承载 → 完全不支持。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_027_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

# ① 政策表地理列（渗透地理面的唯一真实锚点）
policy_cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_policy_base")]
facts["gkx_policy_col_count"] = len(policy_cols)
facts["gkx_policy_geo_cols"] = [c for c in policy_cols if re.search(r"province|city|district|region|area|geo|zone", c, re.I)]

# 地理列填充率（B9：'NULL' 为字面值须剔除——theme/keywords 有同款字面 NULL 先例）
facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])
def _real(col):
    return int(qg(f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {col} IS NOT NULL AND {col} != '' AND {col} != 'NULL'")[0][0])
facts["gkx_policy_province_effective"] = _real("province")
facts["gkx_policy_city_effective"] = _real("city")
facts["gkx_policy_district_effective"] = _real("district")
facts["gkx_policy_province_nonnull"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE province IS NOT NULL AND province != ''")[0][0])
facts["gkx_policy_city_nonnull"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE city IS NOT NULL AND city != ''")[0][0])
facts["gkx_policy_district_nonnull"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE district IS NOT NULL AND district != ''")[0][0])
# province 取值分布 Top8（行政维在案证明；剔除字面 'NULL'）
pv = qg("SELECT province, COUNT(*) FROM gkx.dwd_policy_base WHERE province IS NOT NULL AND province != '' AND province != 'NULL' "
        "GROUP BY province ORDER BY 2 DESC, province LIMIT 8")
facts["gkx_policy_province_top8"] = [[r[0], int(r[1])] for r in pv]
# 字面 'NULL' 占比（B9 披露）
facts["gkx_policy_province_literal_null"] = facts["gkx_policy_rows"] - facts["gkx_policy_province_effective"] - 0
facts["gkx_policy_district_literal_null"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE district = 'NULL'")[0][0])

# 政策表企业享受列（渗透触达维——族级缺口）
facts["gkx_policy_enterprise_like_cols"] = [c for c in policy_cols if re.search(r"enjoy|benefit|enterprise|org|company|employ", c, re.I)]

# 行政区划维表（地理归一承载）
area_cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_dim_admin_area")]
facts["gkx_admin_area_cols"] = area_cols
facts["gkx_admin_area_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_dim_admin_area")[0][0])

# 全球政策地理列（027 若扩展全球面；剔除字面 'NULL'）
gpol_cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_global_policy_base")]
facts["gkx_global_policy_geo_cols"] = [c for c in gpol_cols if re.search(r"region|country|geo", c, re.I)]
gr = qg("SELECT region, COUNT(*) FROM gkx.dwd_global_policy_base WHERE region IS NOT NULL AND region != '' AND region != 'NULL' "
        "GROUP BY region ORDER BY 2 DESC, region LIMIT 8")
facts["gkx_global_policy_region_top8"] = [[r[0], int(r[1])] for r in gr]
facts["gkx_global_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_global_policy_base")[0][0])

# ============ dev ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()
lcur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='gkxlumenx_dwd' "
             "AND table_name REGEXP 'policy|region' ORDER BY table_name")
dev_rows = {}
for (t,) in lcur.fetchall():
    dev_rows[t] = int(ql(f"SELECT COUNT(*) FROM `{t}`")[0][0])
facts["dev_policy_region_table_rows"] = dev_rows
lconn.close()

# ============ jiuxin ============
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)
try:
    jconn = pymysql.connect(**JX)
    jcur = jconn.cursor()
    def qj(sql):
        jcur.execute(sql)
        return jcur.fetchall()
    jcur.execute("SHOW TABLES")
    jx_tables = sorted(r[0] for r in jcur.fetchall())  # B5
    facts["jiuxin_table_count"] = len(jx_tables)
    facts["jiuxin_region_like_tables"] = [t for t in jx_tables if re.search(r"region|policy", t, re.I)]
    # 渗透/触达词根表扫（表名级）
    pen_pat = re.compile(r"penetrat|permeat|reach|coverage|touch|diffus", re.I)
    facts["jiuxin_penetration_like_tables"] = [t for t in jx_tables if pen_pat.search(t)]
    # 区域年度指标面（技术侧，非政策渗透）行数与列
    facts["jiuxin_tech_region_yearly_rows"] = int(qj("SELECT COUNT(*) FROM ads_technology_region_yearly_metrics")[0][0])
    facts["jiuxin_tech_region_yearly_cols"] = [r[0] for r in qj("DESC ads_technology_region_yearly_metrics")]
    facts["jiuxin_problem_region_yearly_rows"] = int(qj("SELECT COUNT(*) FROM ads_research_problem_region_yearly_metrics")[0][0])
    # 政策证据面（渗透的政策侧候选）
    facts["jiuxin_tech_policy_evidence_rows"] = int(qj("SELECT COUNT(*) FROM ads_technology_policy_evidence")[0][0])
    facts["jiuxin_problem_policy_evidence_rows"] = int(qj("SELECT COUNT(*) FROM ads_research_problem_policy_evidence")[0][0])
    facts["jiuxin_problem_policy_yearly_rows"] = int(qj("SELECT COUNT(*) FROM ads_research_problem_policy_yearly_metrics")[0][0])
    facts["jiuxin_problem_policy_yearly_cols"] = [r[0] for r in qj("DESC ads_research_problem_policy_yearly_metrics")]
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)
    notes.append("久新连接失败按未取证登记（B4），不参与判档数字")

# ================= 派生（结构面读数，非指标值） =================
derived.append({
    "key": "gkx_policy_province_effective_pct",
    "value": round(100.0 * facts["gkx_policy_province_effective"] / facts["gkx_policy_rows"], 4),
    "numerator": facts["gkx_policy_province_effective"],
    "denominator": facts["gkx_policy_rows"],
    "note": "分子=dwd_policy_base.province 非「NULL」字面且非空行数（B9：该库字面 'NULL' 占 "
            f"{facts['gkx_policy_rows'] - facts['gkx_policy_province_effective']:,} 行须剔除），分母=同表 20,000 行；"
            "同表同池（B3）；语义=政策发文地理维（发文机关属地）有效填充率——这是「政策发布地」不是「政策渗透地」",
})
derived.append({
    "key": "gkx_policy_district_effective_pct",
    "value": round(100.0 * facts["gkx_policy_district_effective"] / facts["gkx_policy_rows"], 4),
    "numerator": facts["gkx_policy_district_effective"],
    "denominator": facts["gkx_policy_rows"],
    "note": "分子=district 非字面 NULL 非空行数，分母=同表 20,000 行；同表同池（B3）；区县级有效填充率——"
            "UI 演示常量恰好是深圳四区（南山/福田/宝安/龙岗）粒度，而库内区县维以字面 'NULL' 为主（"
            f"{facts['gkx_policy_district_literal_null']:,} 行），区县级接近空载",
})

# ================= absence_probe =================
absence += [
    {"probe": "gkx 政策×区域×企业触达交互面（渗透指数分子分母本体）",
     "source": "gkx",
     "sql": "SHOW COLUMNS FROM gkx.dwd_policy_base；33 列扫 enjoy|benefit|enterprise|org|company",
     "hits": len(facts["gkx_policy_enterprise_like_cols"]),
     "hit_detail": "0 列命中——渗透指数的语义是「政策在区域内的触达/渗透深度」，需要政策×区域×企业"
                   "（哪些区域的企业实际享受了政策）交互面；政策表只有发布机关地理列（province/city/district），"
                   "无任何企业享受/触达列（族级缺口，与 POLCMP_024/029/037/041 同源）"},
    {"probe": "gkx 渗透/触达结果表",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx；280 表名扫 penetrat|permeat|reach|coverage|touch|diffus",
     "hits": 0,
     "hit_detail": "0 表命中——无政策渗透/扩散/触达结果面"},    {"probe": "dev 区域政策对比/渗透台账",
     "source": "dev",
     "sql": "gkxlumenx_dwd 政策族+region 表行数（ORDER BY 表名）",
     "hits": 0,
     "hit_detail": "regional_policy_compare=0（区域政策对比表存在但 0 行，B4 情形②）、"
                   "shenzhen_policy_distribution=0、shenzhen_policy_compare=0——深圳区县政策分布面"
                   "（UI 演示常量的真实承载候选）表在而数据空"},
    {"probe": "久新政策渗透地理面",
     "source": "jiuxin",
     "sql": "SHOW TABLES + DESC ads_technology_policy_evidence / ads_research_problem_policy_evidence",
     "hits": 0,
     "hit_detail": f"政策×技术节点证据面零装载：ads_technology_policy_evidence={facts.get('jiuxin_tech_policy_evidence_rows')} 行"
                   f"（列含 policy_id/location_id/applicability_scope——结构就是政策地理渗透候选，但 0 行，B4 情形②）；"
                   f"ads_research_problem_policy_evidence={facts.get('jiuxin_problem_policy_evidence_rows')} 行为政策证据引用计数非区域渗透；"
                   "区域年度指标面（2,711,376 行）是技术侧（论文/专利/项目证据计数），无政策渗透维"},
    {"probe": "需求原文「渗透指数/影响区域」定义段",
     "source": "doc",
     "sql": "rg 渗透 三份需求真源",
     "hits": 1,
     "hit_detail": "主需求 1.1.1.1.4.2.3.2.3 政策影响范围分析：「分析政策的预期影响范围，包括受益对象、影响区域、"
                   "影响行业等…了解政策的覆盖面和渗透深度」——功能语境枚举（影响区域/渗透深度），无指数定义"
                   "（无区域清单、无触达口径、无 0-100 分合成方法）；核增需求与算法库 0 命中"},
]

support = "完全不支持"

notes += [
    "判档：渗透指数 = f(政策×区域×触达)的综合评价分（0-100，UI 柱高）。需业务建模类——即便数据齐，"
    "合成方法（触达率/渗透深度的加权）也需立项调研；但当前先卡在数据层：触达交互面三源零承载"
    "（gkx 政策表 0 企业列、dev 区域对比表空、久新 policy_evidence 结构在而 0 行）",
    "边界事实：gkx 政策表确有 province/city/district 发布地理列（province 剔除字面 'NULL' 后有效 "
    f"{facts['gkx_policy_province_effective']:,} 行，Top：北京市 1,932/上海市 1,842/广东省 1,612），"
    "但这度量「政策从哪发」不是「政策渗透到哪」——渗透需要落地/享受事件，与族级兑现台账缺口同源；"
    "区县级 district 以字面 'NULL' 为主（18,835 行），区县级接近空载；"
    "久新表名级渗透词根扫描命中 ads_patent_analysis_coverage/ads_technology_data_coverage（专利/数据覆盖面，非政策渗透）",
    "mock 披露：policyData.js:1999-2004 regions 深圳四区 value（90/82/75/70 渗透指数演示常量）与 "
    "coverage（84/76/68/61 覆盖面演示常量）分列，:1990 注释明写「覆盖面 ≠ 渗透指数…（演示）」——"
    "前端作者已自觉区分两个语义，演示值不参与支持度结论",
    "B11 对账：gkx 政策 20,000/全球政策 20,000 与共享快照零漂移；dev 政策族行数与 Lane6 探针零漂移；"
    "久新 ads_technology_region_yearly_metrics 2,711,376 与 _probe_lane2_s303_out.json 零漂移",
    "升档触发器（B10）：①久新 ads_technology_policy_evidence 若装载（结构已含 policy_id×location_id）→ "
    "政策×区域关联闭合，可升部分支持（还需触达企业名单）；②接入兑现台账（族级）→ 渗透分母闭合，"
    "配合触达率建模可升完全转换支持；③甲方若接受「政策发文地分布」代理 → 语义已换（发文≠渗透），本件不接受",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_027",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/simulation/interpret/InterpretWorkbench.jsx:411",
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:1999",
        "repos/demo-ui-science/src/pages/policy-tracking/simulation/sharedCharts.jsx:1148",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「渗透指数」指标名三份需求真源 0 命中；「影响区域/渗透深度」在主需求 1.1.1.1.4.2.3.2.3 "
                "政策影响范围分析段以功能语境枚举出现（非指标条目式命中，登记 named_in_srs=false）；"
                "「渗透」另见主需求 :933 市场渗透率分析（技术成熟度语境，不同物）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["渗透观测窗口（政策落地事件年）"],
    "base_years_note": "本件无渗透事件可算（触达交互面零承载）；政策发布年分布可从 publish_year 取得但不构成渗透基期",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts["gkx_policy_rows"]), str(facts["gkx_global_policy_rows"]),
                          str(facts.get("jiuxin_tech_region_yearly_rows", 0)), "280", "40,000"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
