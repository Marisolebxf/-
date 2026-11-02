#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_042 空间协同指数 · 三源探针脚本（S3-03 Lane 2）。

含义：政策效果推演（simulationIndicators）第 4 槽位「空间协同指数」（分，0-100）——
政策实施后目标区域与周边区域的空间协同水平综合评价分（需业务建模类）。
权威参照：京津冀区域协同发展指数（国家统计局 R1/R2——5 领域 43 三级指标加权合成，
基期 2014=100）；政策协同的央地/区域耦合协调度模型（R3）。
UI：repos/demo-ui-science/src/pages/policy-tracking/policyData.js:712
（simulationIndicators[3] 'spatialIndex' '空间协同指数' unit '分' baseline 72 target 88，
  Bid 标注注释 :708；三情景 results 92/84/68 @ :723/:731/:739；消费方 sharedCharts.jsx 雷达+对比条形）。

三源实况（全部实探，2026-11-01）：
- gkx：280 表扫无空间协同/区域协同结果面；政策表 33 列无企业/区域交互列；
  区域词根表仅行政区划维表（dwd_dim_admin_area 20,000）与主营业务构成区域表。
- dev：政策族 38 表除 policy_base_info 40,000 外全 0 行；regional_policy_compare=0。
- 久新：机构协同网络面体量巨大且真实（ads_institution_collaboration_yearly 14,380,246 行——
  机构×合作机构×年 共同论文/专利/项目计数，is_cross_region_collaboration 跨区协同标志列在！
  subfield 版 23,363,790 行）——但这是科研合作协同面，非「政策实施后区域空间协同」；
  政策证据面 0 行（ads_technology_policy_evidence=0）。
依赖「政策×区域×区域交互（要素流动/产业协作）」面，三源零承载 → 完全不支持。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_042_out.json")
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
syn_pat = re.compile(r"synerg|collaborat|coop|cooper|joint|cross_region|spatial", re.I)
facts["gkx_synergy_like_tables"] = [t for t in gkx_tables if syn_pat.search(t)]
region_pat = re.compile(r"region|province|city|district|geo|area|spatial", re.I)
facts["gkx_region_like_tables"] = [t for t in gkx_tables if region_pat.search(t)]

# 政策表区域交互列（政策×区域×区域——协同指数的交互维）
policy_cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_policy_base")]
facts["gkx_policy_col_count"] = len(policy_cols)
facts["gkx_policy_geo_cols"] = [c for c in policy_cols if re.search(r"province|city|district|region|area|geo|zone|spatial|synerg|collab", c, re.I)]
facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])

# 行政区划维表（空间基准承载）
facts["gkx_admin_area_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_dim_admin_area")[0][0])
facts["gkx_admin_area_cols"] = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_dim_admin_area")]

# 政策文本叙述面：「协同」词命中（政策意图声明非协同结果）
facts["gkx_policy_text_xietong_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,''),IFNULL(keypoints,'')) LIKE '%协同%'")[0][0])

# ============ dev ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()
lcur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='gkxlumenx_dwd' "
             "AND table_name REGEXP 'policy|region|synerg|collab' ORDER BY table_name")
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
    facts["jiuxin_synergy_like_tables"] = [t for t in jx_tables if syn_pat.search(t)]
    # 机构协同网络面（区域协同的真实候选——结构核对）
    facts["jiuxin_inst_collab_yearly_rows"] = int(qj("SELECT COUNT(*) FROM ads_institution_collaboration_yearly")[0][0])
    facts["jiuxin_inst_collab_yearly_cols"] = [r[0] for r in qj("DESC ads_institution_collaboration_yearly")]
    # 跨区协同标志实测（若可算，这是区域协同的代理面规模证明）
    try:
        facts["jiuxin_inst_collab_cross_region_rows"] = int(qj(
            "SELECT COUNT(*) FROM ads_institution_collaboration_yearly WHERE is_cross_region_collaboration = 1")[0][0])
    except Exception as e:  # noqa: BLE001
        facts["jiuxin_inst_collab_cross_region_note"] = str(e)
    # 政策证据面（政策侧协同交互的政策维候选）
    facts["jiuxin_tech_policy_evidence_rows"] = int(qj("SELECT COUNT(*) FROM ads_technology_policy_evidence")[0][0])
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)
    notes.append("久新连接失败按未取证登记（B4），不参与判档数字")

# ================= 派生（叙述/结构面读数，非指标值） =================
derived.append({
    "key": "gkx_policy_text_xietong_share_pct",
    "value": round(100.0 * facts["gkx_policy_text_xietong_rows"] / facts["gkx_policy_rows"], 4),
    "numerator": facts["gkx_policy_text_xietong_rows"],
    "denominator": facts["gkx_policy_rows"],
    "note": "分子=文本含「协同」的政策行数（title+content+keypoints 拼串 LIKE），分母=gkx.dwd_policy_base "
            "全表 20,000 行；同表同池（B3）；语义=协同叙事覆盖面（政策谈区域协同意图），不是协同结果度量",
})
if "jiuxin_inst_collab_cross_region_rows" in facts:
    derived.append({
        "key": "jiuxin_inst_collab_cross_region_share_pct",
        "value": round(100.0 * facts["jiuxin_inst_collab_cross_region_rows"] / facts["jiuxin_inst_collab_yearly_rows"], 4),
        "numerator": facts["jiuxin_inst_collab_cross_region_rows"],
        "denominator": facts["jiuxin_inst_collab_yearly_rows"],
        "note": "分子=is_cross_region_collaboration=1 行数，分母=ads_institution_collaboration_yearly 全表行数；"
                "同表同池（B3）；语义=科研合作对中跨区域合作占比——证明「跨区交互数据本体」在久新存在，"
                "但它是科研协同不是政策实施后的空间协同（语义差一层：无政策归因维）",
    })

# ================= absence_probe =================
absence += [
    {"probe": "gkx 区域协同/空间协同结果面",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx；280 表名扫 synerg|collaborat|coop|cooper|joint|cross_region|spatial",
     "hits": len(facts["gkx_synergy_like_tables"]),
     "hit_detail": "0 表命中——无任何区域协同/空间协同结果面"},
    {"probe": "gkx 政策表区域交互列（政策×区域×区域）",
     "source": "gkx",
     "sql": "SHOW COLUMNS FROM gkx.dwd_policy_base；33 列扫 synerg|collab|joint|cross_region|spatial（含地理列）",
     "hits": len(facts["gkx_policy_geo_cols"]),
     "hit_detail": f"命中 {len(facts['gkx_policy_geo_cols'])} 列全为发布地理列（{','.join(facts['gkx_policy_geo_cols'])}）——"
                   "单值属地字段非区域间交互；协同指数需要「区域A×区域B」的成对交互面（要素流动/产业协作），"
                   "政策表无此结构"},
    {"probe": "dev 区域协同面",
     "source": "dev",
     "sql": "gkxlumenx_dwd 表名扫 policy|region|synerg|collab + 行数（ORDER BY）",
     "hits": 0,
     "hit_detail": "regional_policy_compare=0（区域政策对比表存在但 0 行，B4 情形②）；"
                   "无任何协同/空间交互表"},
    {"probe": "久新政策空间协同面",
     "source": "jiuxin",
     "sql": "SHOW TABLES + DESC ads_institution_collaboration_yearly + ads_technology_policy_evidence 行数",
     "hits": 0,
     "hit_detail": f"科研协同网络在（ads_institution_collaboration_yearly {facts.get('jiuxin_inst_collab_yearly_rows', 0):,} 行，"
                   "is_cross_region_collaboration 跨区标志列在——真实跨区交互数据本体），但：①这是机构科研合作"
                   "（论文/专利/项目共现）非政策实施的空间协同；②政策证据面 "
                   f"ads_technology_policy_evidence={facts.get('jiuxin_tech_policy_evidence_rows', 0)} 行（0 装载）——"
                   "「政策→协同」的归因链零承载"},
    {"probe": "需求原文「空间协同指数」定义段",
     "source": "doc",
     "sql": "rg 空间协同 三份需求真源",
     "hits": 0,
     "hit_detail": "「空间协同指数」三份需求真源 0 命中；主需求 1.1.1.1.4.2.3.1.3 空间模拟段枚举的是"
                   "「GDP增长、产业结构变化、就业率变化」（未含空间协同）；「协同」在主需求另见 "
                   "1.1.1.1.4.2.3.2.4 政策关联分析「把握政策的协同效应」（定性叙述）与产学研协同指数"
                   "（:5211 企业-机构合作语境，不同物）——均非本指标定义"},
]

support = "完全不支持"

notes += [
    "判档：空间协同指数 = f(政策×区域×区域交互)的综合评价分（0-100）。需业务建模类——权威范式是"
    "京津冀区域协同发展指数（R1/R2：5 领域 43 三级指标、基期=100、专家赋权加权合成）或央地/区域政策"
    "耦合协调度（R3）。数据前置依赖：①区域清单与空间基准（gkx 行政区划维表 20,000 行在）"
    "②区域间交互序列（要素流动/产业协作——三源均无政策归因版）③政策×区域关联（三源 0 装载）。"
    "②③双缺，判完全不支持",
    "边界事实：久新机构协同网络是本族唯一大体量真实跨区交互面（14,380,246 行，跨区合作占比见派生键），"
    "但它是科研协同（论文/专利共现）——若甲方接受「科研跨区合作密度」作空间协同的代理读数，"
    "语义已换（科研协同≠政策实施的空间协同），须另立件并显式披露口径差",
    "mock 披露：policyData.js:712 spatialIndex（unit '分'，baseline 72/target 88）与三情景 results"
    "（92/84/68）均为前端演示常量（演示值，不参与支持度结论）；与 024 employmentChange 同挂"
    " simulationIndicators 四槽位（Bid 标注），是姊妹件",
    "B11 对账：gkx 政策 20,000 行与共享快照零漂移；dev 政策族行数与 Lane6 探针零漂移；"
    "久新 ads_institution_collaboration_yearly 14,380,246 与 TECHTRK_018/X_015/INNOV_003 产物同读数零漂移"
    "（subfield 版 23,363,790 与 _probe_lane2_s302f_out.json 对齐）",
    "升档触发器（B10）：①接入政策×区域关联（久新 policy_evidence 结构已在，装载即可）+ 区域交互序列"
    "→ 可升部分支持（还需建模立项）；②甲方接受科研协同代理 → 换口径另立件；③按 R1 范式构建"
    "5 领域指标体系需先补齐跨区要素流动数据（交通/贸易/技术合同），工程量大",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_042",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:712",
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:708",
        "repos/demo-ui-science/src/pages/policy-tracking/simulation/sharedCharts.jsx:26",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「空间协同指数」三份需求真源 0 命中；主需求 1.1.1.1.4.2.3.1.3 空间模拟段枚举"
                "「GDP增长、产业结构变化、就业率变化」未含本指标；UI 注释「Bid · …」为前端作者标注；"
                "「协同」在需求文档仅定性叙述（政策协同效应/产学研协同），非本指标定义",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["协同观测基期年（区域交互序列起点）"],
    "base_years_note": "本件无政策空间协同序列可算（交互面政策归因零承载）；京津冀范式基期为 2014=100，"
                       "本库无对应区域交互序列起点",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts["gkx_policy_rows"]), str(facts["gkx_admin_area_rows"]),
                          str(facts.get("jiuxin_inst_collab_yearly_rows", 0)), "280", "40,000"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
