#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_024 就业率变化（政策后较政策前）· 三源探针与边界读数脚本（S3-03 Lane 1）。

含义：目标区域/群体在政策实施前后的就业率（或就业规模代理）变化，单位 pp（百分点）。
= 就业率(政策后窗口) − 就业率(政策前窗口)。仿真语境下是推演输出指标。
UI：repos/demo-ui-science/src/pages/policy-tracking/policyData.js:711
（simulationIndicators 第 3 项 employmentChange '就业率变化' unit 'pp'，Bid 标注；
  消费方 simulation/sharedCharts.jsx:26/95/144 雷达与对比条形）。

三源实况（全部实探，2026-11-01）：
- gkx：280 表无就业率/社保/劳动力调查承载（recruit 798 万行是岗位需求发布面非在岗就业面）；
  dwd_org_annual_financial_info.employees_number 3,170 行非零（648 家有 ≥2 年序列）——
  是企业用工规模的窄面代理，且与政策零关联（政策表 33 列无企业/享受列）。
- dev：enterprise_recruit 1,000 行（gkx 同构子集）；政策族 38 表除 policy_base_info 40,000 外全 0 行；
  无 employment/社保类结果表。
- 久新：203 张 ads_* 无就业/雇佣面（列扫 orcid_employment_count 是学者 ORCID 履历计数非就业率）。
分子分母依赖「政策×企业×期」兑现台账 + 区域就业统计（劳动力调查/社保），三源零承载 → 完全不支持。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_024_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

# ============ ① gkx：就业面与政策关联探针 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
# 就业/社保/劳动力语义表扫
employ_pat = re.compile(r"employ|hiring|recruit|job|labor|social|staff|salary|wage|unemploy", re.I)
facts["gkx_employ_like_tables"] = [t for t in gkx_tables if employ_pat.search(t)]
# 招聘表（唯一就业语义邻接表）：结构 + 行数 + 语义边界
facts["gkx_recruit_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_org_recruit_info")[0][0])
facts["gkx_recruit_cols"] = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_org_recruit_info")]
# 招聘 20 万采样：年度分布 + hiring_number 质量（采样，非全表）
sample = qg("SELECT SUBSTR(release_date,1,4) y, COUNT(*) c, SUM(hiring_number IS NOT NULL AND hiring_number>0) hn "
            "FROM (SELECT release_date, hiring_number FROM gkx.dwd_org_recruit_info LIMIT 200000) t "
            "WHERE release_date REGEXP '^20[0-9]{2}' GROUP BY y ORDER BY y DESC LIMIT 6")
facts["gkx_recruit_by_year_200k_sample"] = [[r[0], int(r[1]), int(r[2] or 0)] for r in sample]
# 企业用工规模窄面代理：employees_number
facts["gkx_fin_emp_nonzero_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_org_annual_financial_info WHERE employees_number IS NOT NULL AND employees_number != 0")[0][0])
facts["gkx_orgs_with_2plus_emp_years"] = int(qg(
    "SELECT COUNT(*) FROM (SELECT org_id FROM gkx.dwd_org_annual_financial_info "
    "WHERE employees_number IS NOT NULL AND employees_number != 0 GROUP BY org_id "
    "HAVING COUNT(DISTINCT year)>=2) t")[0][0])
# 政策侧锚点：publish_year 分布（政策前/后窗口的政策存量结构）
py = qg("SELECT publish_year, COUNT(*) FROM gkx.dwd_policy_base WHERE publish_year REGEXP '^(19|20)[0-9]{2}$' "
        "GROUP BY publish_year ORDER BY publish_year DESC LIMIT 6")
facts["gkx_policy_by_year_top6"] = [[r[0], int(r[1])] for r in py]
facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])
# 政策表企业/享受列扫描（政策×企业关联缺失）
policy_cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_policy_base")]
facts["gkx_policy_col_count"] = len(policy_cols)
facts["gkx_policy_enterprise_like_cols"] = [c for c in policy_cols if re.search(r"enjoy|benefit|enterprise|org|company|employ", c, re.I)]
# 政策文本就业词命中（叙述面边界）
facts["gkx_policy_text_jiuye_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,''),IFNULL(keypoints,'')) LIKE '%就业%'")[0][0])

# ============ ② dev：就业面与政策族探针 ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()
# 就业类表扫（dwd/ods/ads/dim 四 schema）
lcur.execute("SELECT TABLE_NAME, TABLE_SCHEMA FROM information_schema.TABLES WHERE TABLE_SCHEMA IN "
             "('gkxlumenx_dwd','gkxlumenx_ods','gkxlumenx_ads','gkxlumenx_dim') AND TABLE_NAME REGEXP "
             "'employ|hiring|recruit|job|labor|social'")
facts["dev_employ_like_tables"] = sorted([[r[1], r[0]] for r in lcur.fetchall()])
# enterprise_recruit 结构与行数（gkx 同构子集）
facts["dev_enterprise_recruit_rows"] = int(ql("SELECT COUNT(*) FROM enterprise_recruit")[0][0])
facts["dev_enterprise_recruit_cols"] = [r[0] for r in ql("SHOW COLUMNS FROM enterprise_recruit")]
# 政策族关键表行数（兑现/执行/仿真类全 0）
dev_policy_rows = {}
for t in ["policy_base_info", "policy_effect_eval", "policy_simulation_result", "enterprise_fund_project"]:
    dev_policy_rows[t] = int(ql(f"SELECT COUNT(*) FROM `{t}`")[0][0])
facts["dev_policy_family_rows"] = dev_policy_rows
lconn.close()

# ============ ③ 久新：就业/雇佣面探针 ============
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
    jx_tables = sorted(r[0] for r in jcur.fetchall())
    facts["jiuxin_table_count"] = len(jx_tables)
    facts["jiuxin_employ_like_tables"] = [t for t in jx_tables if employ_pat.search(t)]
    # 列级扫：唯一 employment 命中列的语义核对
    facts["jiuxin_employment_col_hits"] = {"ads_talent_yearly_location.orcid_employment_count":
        "学者 ORCID 雇佣履历计数（0:108,319 / 1:96,102 / 2:6,520），非区域就业率"}
    facts["jiuxin_talent_yearly_location_rows"] = int(qj("SELECT COUNT(*) FROM ads_talent_yearly_location")[0][0])
    emp_dist = qj("SELECT orcid_employment_count, COUNT(*) FROM ads_talent_yearly_location "
                  "GROUP BY orcid_employment_count ORDER BY 2 DESC LIMIT 5")
    facts["jiuxin_orcid_employment_dist"] = [[int(r[0]), int(r[1])] for r in emp_dist]
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)
    notes.append("久新连接失败按未取证登记（B4：连接失败≠0 行），不参与判档数字")

# ================= 派生（骨架读数，非指标值） =================
rec = {y: c for y, c, _ in facts["gkx_recruit_by_year_200k_sample"]}
if "2025" in rec and "2024" in rec:
    derived.append({
        "key": "gkx_recruit_2025_yoy_pct_200k_sample",
        "value": round(100.0 * (rec["2025"] - rec["2024"]) / rec["2024"], 4),
        "numerator": rec["2025"] - rec["2024"],
        "denominator": rec["2024"],
        "note": "分子=2025−2024 采样岗位发布条数差，分母=2024 采样条数；同表同采样池（B3）；"
                "语义=岗位需求发布量同比（供给意愿面），不是就业率变化——岗位发布≠在岗就业，"
                "登记此键仅为证明「政策前后差分」结构在数据面如何被错误代理",
    })
derived.append({
    "key": "gkx_policy_text_jiuye_share_pct",
    "value": round(100.0 * facts["gkx_policy_text_jiuye_rows"] / facts["gkx_policy_rows"], 4),
    "numerator": facts["gkx_policy_text_jiuye_rows"],
    "denominator": facts["gkx_policy_rows"],
    "note": "分子=文本含「就业」的政策行数（title+content+keypoints 拼串 LIKE），分母=gkx.dwd_policy_base "
            "全表 20,000 行；同表同池（B3）；语义=叙述覆盖面，不是就业率",
})

# ================= absence_probe =================
absence += [
    {"probe": "gkx 就业率/社保/劳动力调查结果面",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx；280 表名扫 employ/hiring/recruit/job/labor/social/staff/salary/wage/unemploy",
     "hits": len(facts["gkx_employ_like_tables"]),
     "hit_detail": "命中 dwd_org_recruit_info（7,981,643 行岗位发布面——企业用工需求的供给侧发布，"
                   "无在岗/离职/失业字段，不能推出就业率）与 dwd_job（10 行样例表，BioNTech/GSK 岗位页"
                   "结构测试数据，B4 情形③样例级）；无任何就业率/社保缴纳/劳动力调查结果表"},
    {"probe": "gkx 政策×企业享受关系（政策后受惠群体界定）",
     "source": "gkx",
     "sql": "SHOW COLUMNS FROM gkx.dwd_policy_base；33 列扫 enjoy/benefit/enterprise/org/company/employ",
     "hits": len(facts["gkx_policy_enterprise_like_cols"]),
     "hit_detail": "0 列命中（gkx_policy_enterprise_like_cols 空列表在案）——政策表无企业名单列，"
                   "「政策后受惠企业群」无法界定，前后对比缺处理组"},
    {"probe": "dev 就业类结果表",
     "source": "dev",
     "sql": "information_schema.TABLES 四 schema 扫 employ/hiring/recruit/job/labor/social",
     "hits": len(facts["dev_employ_like_tables"]),
     "hit_detail": "仅 gkxlumenx_dwd.enterprise_recruit（1,000 行，gkx 招聘表同构子集）与 "
                   "gkxlumenx_ods.dwd_org_recruit_info（同源镜像）——均为岗位发布面非就业率面；"
                   "政策族兑现/执行类表全 0 行（policy_effect_eval/policy_simulation_result/enterprise_fund_project）"},
    {"probe": "久新就业/雇佣结果面",
     "source": "jiuxin",
     "sql": "SHOW TABLES；203 表名扫同词典 + 全表 DESC 列扫 employment",
     "hits": 1,
     "hit_detail": "唯一列命中 ads_talent_yearly_location.orcid_employment_count——学者 ORCID 履历中的雇佣记录"
                   "条数计数（211,678 行中 0 条:108,319 / 1 条:96,102），是学者画像字段非区域就业率；"
                   "无任何就业率/雇佣人数结果面"},
    {"probe": "需求原文「就业率变化」定义段",
     "source": "doc",
     "sql": "rg 就业率 三份需求真源",
     "hits": 1,
     "hit_detail": "主需求 1.1.1.1.4.2.3.1.3 区域经济发展空间模拟：「包括GDP增长、产业结构变化、就业率变化等指标」"
                   "——指标名被枚举但无定义（无窗口、无统计口径、无处理组界定）；核增需求与算法库 0 命中"},
]

support = "完全不支持"

notes += [
    "判档：就业率变化 = 就业率(政策后) − 就业率(政策前)。依赖三件：①区域/群体就业率序列（劳动力调查或社保口径）"
    "②政策实施时点窗口 ③受政策影响的处理组界定（政策×企业名单）——①③三源零承载（gkx 无就业率面、dev 无、久新无），"
    "②仅有政策发布年（publish_year varchar）。与 POLCMP_001 落实率共享族级缺口（兑现事件无源）",
    "代理面边界：gkx 招聘表 798 万行是本族唯一大体量就业语义邻接面，但它是岗位需求发布（企业想招多少人），"
    "不是在岗就业（实际雇了多少人）——用发布量差分冒充就业率变化会犯「需求≠存量」的量纲错误；"
    "dwd_org_annual_financial_info.employees_number 3,170 行非零（648 家 ≥2 年）是真实在岗数，"
    "但覆盖面极窄（90,926 行财务面中 3.5%）且与政策零关联，不能构成区域就业率",
    "mock 披露：policyData.js:711 employmentChange（unit 'pp'，baseline 0.8/target 1.5）与 "
    "simulationScenarios 三情景 results（1.8/1.2/0.4 pp）均为前端演示常量——演示值不参与支持度结论",
    "B11 对账：gkx 政策 20,000 行与共享快照 _shared_probe_s3_01_out.json fix2.政策底表行数零漂移；"
    "dev policy_base_info 40,000 与 Lane6 探针 _probe_lane6_s302_r2_out.json 零漂移",
    "升档触发器（B10）：接入区域劳动力调查/社保缴纳序列（就业率闭合）+ 政策×企业兑现台账（处理组闭合）"
    "→ 可升完全转换支持（差分运算本身平凡）；若甲方接受「岗位发布量同比」作代理 → 语义已换（需求≠就业），本件不接受",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_024",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:711",
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:708",
        "repos/demo-ui-science/src/pages/policy-tracking/simulation/sharedCharts.jsx:26",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「就业率变化」在主需求《科技信息展示系统和科技专题服务系统.md》1.1.1.1.4.2.3.1.3 区域经济发展"
                "空间模拟被枚举（「包括GDP增长、产业结构变化、就业率变化等指标」）——指标名出现在需求语境中但"
                "无定义方法（非 SRS 指标条目式命中，按枚举语境登记 named_in_srs=false）；"
                "核增需求《科技信息展示系统(政策对比功能升级)核增需求.md》与《科技专题服务算法库.md》0 命中",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["政策前基期窗口", "政策后观测窗口"],
    "base_years_note": "本件无就业率序列可算（三源零承载）；政策侧 publish_year（varchar）仅能界定政策发布年分布"
                       "（2021:2,120 / 2020:2,402 / 2019:2,035…），不构成就业基期",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts["gkx_recruit_rows"]), str(facts["gkx_policy_rows"]),
                          str(facts["gkx_policy_text_jiuye_rows"]), str(facts["gkx_fin_emp_nonzero_rows"]),
                          str(facts["gkx_orgs_with_2plus_emp_years"]), str(facts["dev_enterprise_recruit_rows"]),
                          "280", "40,000"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
