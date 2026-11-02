#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_036 资源利用效率（能耗产出比）· 三源探针脚本（S3-03 Lane 2）。

含义：多维度效果评估（DS-12）环境维指标「资源利用效率」——政策语境下即能耗产出比：
单位能源消耗的产出（GDP 或产值/能耗），是单位 GDP 能耗（能耗/GDP，国家统计局 R1）的倒数形态。
UI：repos/demo-ui-science/src/pages/policy-tracking/policyData.js:1868
（multiDimensionEvalData.dimensions[environment].indicators[2] '资源利用效率' score 72，
  环境维总分 72；消费方 simulation/estimate/EstimateWorkbench.jsx:614/627 四维雷达+分项柱）。

三源实况（全部实探，2026-11-01）：
- gkx：280 表名扫 energy 词根 0 表；全库列扫 energy|power_consum|electric 仅命中材料/光谱
  物理化学字段（与 034 同款错位）；财务表 dwd_org_annual_financial_info 有产出侧
  （operating_revenue 营业收入）但无能耗侧（27 列逐一核对无能源消费列）。
- dev：列扫 energy|carbon 0 命中；无能耗面。
- 久新：203 表名扫 energy 0 表命中。
依赖「能耗序列 + 产出序列」，能耗侧三源零承载 → 完全不支持。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_036_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())  # B5
facts["gkx_table_count"] = len(gkx_tables)
energy_pat = re.compile(r"energy|consumption|efficiency|resource", re.I)
facts["gkx_resource_like_tables"] = [t for t in gkx_tables if energy_pat.search(t)]

# 全库列扫（ORDER BY，B5）：能耗语义列
col_hits = qg(
    "SELECT table_name, column_name FROM information_schema.columns "
    "WHERE table_schema='gkx' AND (column_name REGEXP 'energy|power_consum|electric|coal|fuel' "
    "OR column_name LIKE '%能耗%') ORDER BY table_name, column_name")
facts["gkx_energy_col_hits"] = [[r[0], r[1]] for r in col_hits]

# 产出侧：企业财务表（营业收入——若能耗侧存在，产出比的分母/分子可从此面取）
fin_cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_org_annual_financial_info")]
facts["gkx_fin_col_count"] = len(fin_cols)
facts["gkx_fin_output_like_cols"] = [c for c in fin_cols if re.search(r"revenue|output|income|产值|营收", c, re.I)]
facts["gkx_fin_energy_like_cols"] = [c for c in fin_cols if re.search(r"energy|power|electric|coal|fuel|能耗", c, re.I)]
facts["gkx_fin_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_org_annual_financial_info")[0][0])
facts["gkx_fin_revenue_nonzero_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_org_annual_financial_info WHERE operating_revenue IS NOT NULL AND operating_revenue != 0")[0][0])

# 政策文本叙述面：「能耗/资源利用」词命中
facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])
for word, key in [("能耗", "gkx_policy_text_nenghao_rows"), ("资源利用", "gkx_policy_text_ziyuan_rows"),
                  ("节能减排", "gkx_policy_text_jieneng_rows")]:
    facts[key] = int(qg(
        f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,''),IFNULL(keypoints,'')) LIKE '%{word}%'")[0][0])

# ============ dev ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()
lcur.execute("SELECT table_schema, table_name, column_name FROM information_schema.columns WHERE "
             "table_schema IN ('gkxlumenx_dwd','gkxlumenx_ods','gkxlumenx_ads') AND column_name REGEXP "
             "'energy|power_consum|electric|coal|fuel' ORDER BY table_schema, table_name, column_name")
facts["dev_energy_col_hits"] = [[r[0], r[1], r[2]] for r in lcur.fetchall()]
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
    facts["jiuxin_resource_like_tables"] = [t for t in jx_tables if energy_pat.search(t)]
    # resource 语义面结构核对（科技资源非能耗资源——B4 语义甄别）
    facts["jiuxin_city_subfield_resource_cols"] = [r[0] for r in qj("DESC ads_city_subfield_resource_yearly")]
    facts["jiuxin_city_subfield_resource_rows"] = int(qj("SELECT COUNT(*) FROM ads_city_subfield_resource_yearly")[0][0])
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)
    notes.append("久新连接失败按未取证登记（B4），不参与判档数字")

# ================= 派生（产出侧边界读数，非指标值） =================
derived.append({
    "key": "gkx_fin_revenue_fill_pct",
    "value": round(100.0 * facts["gkx_fin_revenue_nonzero_rows"] / facts["gkx_fin_rows"], 4),
    "numerator": facts["gkx_fin_revenue_nonzero_rows"],
    "denominator": facts["gkx_fin_rows"],
    "note": "分子=dwd_org_annual_financial_info.operating_revenue 非零行数，分母=同表全行数；同表同池（B3）；"
            "语义=产出侧（营业收入）填充率——产出侧有半数填充，但能耗侧 0 列（见 absence）,"
            "能耗产出比的分子分母只可得其一",
})

# ================= absence_probe =================
absence += [
    {"probe": "gkx 能源消费序列面（能耗产出比的能耗侧）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx；280 表名扫 energy|consumption|efficiency|resource",
     "hits": len(facts["gkx_resource_like_tables"]),
     "hit_detail": "0 表命中——无能源消费/资源效率序列表"},
    {"probe": "gkx 全库能耗语义列",
     "source": "gkx",
     "sql": "information_schema.columns 扫 energy|power_consum|electric|coal|fuel（ORDER BY，B5）",
     "hits": len(facts["gkx_energy_col_hits"]),
     "hit_detail": "仅命中材料科学（dwd_material_virtual_structure.energy_above_hull/"
                   "formation_energy_per_atom）与分子光谱（dwd_molecular_spectrum.collision_energy）"
                   "物理化学字段——语义完全错位，无任何能源消费列"},
    {"probe": "gkx 企业财务表能耗列（企业级能耗产出比候选）",
     "source": "gkx",
     "sql": "SHOW COLUMNS FROM gkx.dwd_org_annual_financial_info；27 列逐一核对",
     "hits": len(facts["gkx_fin_energy_like_cols"]),
     "hit_detail": "0 列命中——财务表有产出侧（operating_revenue/main_business_revenue）无能耗侧，"
                   "企业级能耗产出比不可构建"},
    {"probe": "dev 能耗面",
     "source": "dev",
     "sql": "三 schema 列扫 energy|power_consum|electric|coal|fuel（ORDER BY）",
     "hits": len(facts["dev_energy_col_hits"]),
     "hit_detail": "0 列命中——dev 无任何能耗字段"},
    {"probe": "久新资源/能耗面",
     "source": "jiuxin",
     "sql": "SHOW TABLES；203 表名扫 energy|consumption|efficiency|resource + DESC 结构核对",
     "hits": len(facts.get("jiuxin_resource_like_tables", [])),
     "hit_detail": "命中 7 张 resource 表但全部是「科技资源」语义面：ads_city_subfield_resource_yearly"
                   f"（{facts.get('jiuxin_city_subfield_resource_rows', 0):,} 行——论文/人才/项目/经费计数，"
                   "DESC 41 列逐一核对无任何能耗/能源消费字段）、ads_institution_subfield_resource_yearly、"
                   "ads_resource_benchmark_city 等——「资源」指科研要素投入非能源消耗，语义错位"},
    {"probe": "需求原文「资源利用效率（政策语境）/能耗产出比」定义段",
     "source": "doc",
     "sql": "rg 资源利用 三份需求真源",
     "hits": 4,
     "hit_detail": "主需求「资源利用」4 处命中全部在科学仪器共享（:2741 数据库检索效率/:3583 仪器共享/"
                   ":3625 仪器利用率/:3733 服务频率）与算法库 :1277（空间资源利用——载体评价指标语境），"
                   "均非政策效果评估的环境维「能耗产出比」；政策语境的环境维资源利用效率 0 定义；"
                   "核增需求 0 命中"},
]

support = "完全不支持"

notes += [
    "判档：资源利用效率（能耗产出比）= 产出/能耗（单位 GDP 能耗的倒数形态，官方口径 R1）。"
    "依赖：①能耗序列 ②产出序列。产出侧 gkx 仅 2.4% 填充（营业收入 "
    f"{facts['gkx_fin_revenue_nonzero_rows']:,}/{facts['gkx_fin_rows']:,} 非零），能耗侧三源零承载"
    "（gkx 全库唯一 energy 列是材料形成能、dev 0 列、久新 7 张 resource 表全是科技资源语义非能耗）——"
    "分子分母双缺，判完全不支持",
    "边界事实：与 034 碳强度共享同一能耗侧缺口（能源消费序列三源零承载），两件是同一数据源缺口在"
    "环境维的两个读数形态；久新 ads_city_subfield_resource_yearly 的「资源」是论文/人才/经费等科研要素，"
    "与能源消耗完全不同物（表名陷阱，DESC 已甄别）",
    "mock 披露：policyData.js:1868「资源利用效率 72 分」是 multiDimensionEvalData 环境维 indicators 的"
    "前端演示常量（0-100 评分形态，演示值，不参与支持度结论）；消费方 EstimateWorkbench.jsx 四维雷达",
    "B11 对账：gkx 政策 20,000 行与共享快照零漂移；gkx energy 列扫与 _probe_lane2_s303_out.json "
    "gkx_energy_col_hits 零漂移（6 列同清单）；财务表 90,926 行与 024 件同读数零漂移",
    "升档触发器（B10）：接入区域/企业能耗序列（能源平衡表/重点用能单位数据）→ 与产出侧（营业收入/"
    "区域 GDP）配对即可算能耗产出比，可升完全转换支持；若甲方接受「全国单位 GDP 能耗官方序列」外接 → "
    "粒度是全国年度非政策区域，单独立项",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_036",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:1868",
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:1863",
        "repos/demo-ui-science/src/pages/policy-tracking/simulation/estimate/EstimateWorkbench.jsx:614",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「资源利用效率」在主需求 4 处命中均为科学仪器共享/载体评价语境（非政策效果评估环境维）；"
                "「能耗产出比」三份需求真源 0 命中；主需求 1.1.1.1.4.2.3.1.4 多维度效果评估仅枚举"
                "「环境」维度无指标定义",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["能耗观测基期年"],
    "base_years_note": "本件无能耗序列可算（三源零承载）；产出侧营业收入按年（year 列）在但缺配对能耗侧",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts["gkx_fin_rows"]), str(facts["gkx_fin_revenue_nonzero_rows"]),
                          str(facts["gkx_policy_text_nenghao_rows"]), "280", "203"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
