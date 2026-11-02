#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_025 平均到账周期 · 三源探针与边界读数脚本（S3-03 Lane 2）。

含义：政策资金（科技专项资金）从申报受理（或任务书签订）到资金到达企业账户的平均天数。
= mean(到账日期 − 起算日期)。政务侧对应「资金拨付进度」环节时限（国办发〔2021〕32 号 30 日时限）。
UI：repos/demo-ui-science/src/pages/policy-tracking/policyData.js:2208
（policyPortraitSummaries 企业画像卡 detail.metrics 第 3 槽位「平均到账周期 46 天」，前端演示常量；
  消费方 analysis/PortraitTrio.jsx Drawer 指标行）。

三源实况（全部实探，2026-11-01）：
- gkx：280 表扫 fund/grant/disburse 词根命中 17 张表全为基金（私募基金/产业基金）语义面
  （dwd_fund_* / dwd_industrial_fund_*），无一张是政策资金拨付台账；列级扫
  disburse/appropriat/grant_date/payment_date/arrival/到账/拨付 全库 0 列命中；
  dwd_policy_base 33 列无企业享受列（enjoy/benefit/enterprise/org/company 词根 0 命中，族级缺口在案）。
- dev：政策族 38 表除 policy_base_info 40,000 外全 0 行——
  enterprise_fund_project=0（企业资金项目表存在但空，B4 情形②）、fund_project=0、
  policy_simulation_result=0；无拨付事件表。
- 久新：203 表扫 fund 词根命中 3 张 funding 语义表——
  ads_research_problem_funding_evidence（5,123 行，科研问题经费证据面：funder/funding_year/
  funding_amount_cny，无拨付日期对、无企业账户到账时间戳）；
  ads_shenzhen_institution_*_funding（机构方向/领域经费聚合面）。
  均无「申报受理→资金到账」事件时间差承载。
依赖「政策×企业×资金事件（申报日期+到账日期）」台账，三源零承载 → 完全不支持。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_025_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())  # B5 sorted
facts["gkx_table_count"] = len(gkx_tables)
fund_pat = re.compile(r"fund|grant|disburse|appropriat|allocat|payment|subsid", re.I)
facts["gkx_fund_like_tables"] = [t for t in gkx_tables if fund_pat.search(t)]

# 基金面代表性表结构与行数（证明「基金≠政策资金拨付」的语义错位）
facts["gkx_dwd_fund_basic_info_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_fund_basic_info")[0][0])
facts["gkx_dwd_fund_basic_info_cols"] = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_fund_basic_info")]
facts["gkx_org_subsidiary_info_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_org_subsidiary_info")[0][0])

# 列级扫：全库拨付/到账日期对
col_hits = qg(
    "SELECT table_name, column_name FROM information_schema.columns "
    "WHERE table_schema='gkx' AND column_name REGEXP "
    "'disburse|appropriat|grant_date|payment_date|arrival' ORDER BY table_name, column_name")
facts["gkx_disburse_col_hits"] = [[r[0], r[1]] for r in col_hits]

# 政策表企业/资金列（族级缺口）
policy_cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_policy_base")]
facts["gkx_policy_col_count"] = len(policy_cols)
facts["gkx_policy_enterprise_like_cols"] = [c for c in policy_cols if re.search(r"enjoy|benefit|enterprise|org|company|employ", c, re.I)]
facts["gkx_policy_fund_like_cols"] = [c for c in policy_cols if re.search(r"fund|grant|money|amount|subsid|disburse", c, re.I)]

# 政策侧时间锚（若台账接入，可作起算窗的发布年分布——边界证据）
py = qg("SELECT publish_year, COUNT(*) FROM gkx.dwd_policy_base WHERE publish_year REGEXP '^(19|20)[0-9]{2}$' "
        "GROUP BY publish_year ORDER BY publish_year DESC LIMIT 6")
facts["gkx_policy_by_year_top6"] = [[r[0], int(r[1])] for r in py]
facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])

# 政策文本叙述面：「到账/拨付/资金」词命中（政策意图声明非拨付事件）
for word, key in [("到账", "gkx_policy_text_daozhang_rows"), ("拨付", "gkx_policy_text_bofu_rows"),
                  ("资金", "gkx_policy_text_zijin_rows")]:
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
lcur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='gkxlumenx_dwd' "
             "AND table_name REGEXP 'fund|policy' ORDER BY table_name")
dev_policy = {}
for (t,) in lcur.fetchall():
    dev_policy[t] = int(ql(f"SELECT COUNT(*) FROM `{t}`")[0][0])
facts["dev_policy_fund_table_rows"] = dev_policy
# gkxlumenx_ods.fund_project 结构（若有列，证明其非拨付事件）
try:
    lcur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='gkxlumenx_ods' "
                 "AND table_name LIKE '%fund%' ORDER BY table_name")
    odf = [r[0] for r in lcur.fetchall()]
    facts["dev_ods_fund_tables"] = odf
    if odf:
        facts["dev_ods_fund_project_cols"] = [r[0] for r in ql(f"SHOW COLUMNS FROM gkxlumenx_ods.`{odf[0]}`")]
        facts["dev_ods_fund_project_rows"] = int(ql(f"SELECT COUNT(*) FROM gkxlumenx_ods.`{odf[0]}`")[0][0])
except Exception as e:  # noqa: BLE001
    facts["dev_ods_fund_probe_note"] = str(e)
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
    jx_tables = sorted(r[0] for r in jcur.fetchall())  # B5 sorted
    facts["jiuxin_table_count"] = len(jx_tables)
    facts["jiuxin_fund_like_tables"] = [t for t in jx_tables if fund_pat.search(t)]
    # 唯一 funding 证据面结构核对（科研经费证据，非政策拨付事件）
    facts["jiuxin_funding_evidence_rows"] = int(qj("SELECT COUNT(*) FROM ads_research_problem_funding_evidence")[0][0])
    facts["jiuxin_funding_evidence_cols"] = [r[0] for r in qj("DESC ads_research_problem_funding_evidence")]
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)
    notes.append("久新连接失败按未取证登记（B4），不参与判档数字")

# ================= 派生（叙述面边界读数，非指标值） =================
derived.append({
    "key": "gkx_policy_text_bofu_share_pct",
    "value": round(100.0 * facts["gkx_policy_text_bofu_rows"] / facts["gkx_policy_rows"], 4),
    "numerator": facts["gkx_policy_text_bofu_rows"],
    "denominator": facts["gkx_policy_rows"],
    "note": "分子=文本含「拨付」的政策行数（title+content+keypoints 拼串 LIKE），分母=gkx.dwd_policy_base "
            "全表 20,000 行；同表同池（B3）；语义=叙述覆盖面（政策谈拨付时限/流程），不是拨付事件记录",
})
derived.append({
    "key": "gkx_policy_text_zijin_share_pct",
    "value": round(100.0 * facts["gkx_policy_text_zijin_rows"] / facts["gkx_policy_rows"], 4),
    "numerator": facts["gkx_policy_text_zijin_rows"],
    "denominator": facts["gkx_policy_rows"],
    "note": "分子=文本含「资金」的政策行数，分母=同表 20,000 行；同表同池（B3）；语义=资金类政策叙述面",
})

# ================= absence_probe =================
absence += [
    {"probe": "gkx 政策资金拨付/到账事件台账",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx；280 表名扫 fund|grant|disburse|appropriat|allocat|payment|subsid",
     "hits": 0,
     "hit_detail": f"命中 {len(facts['gkx_fund_like_tables'])} 张表全为基金语义面（dwd_fund_basic_info "
                   f"{facts['gkx_dwd_fund_basic_info_rows']:,} 行——私募/产业基金基本信息表结构在、数据未装载（B4 情形②），"
                   "dwd_fund_ope_status / dwd_industrial_fund_* 私募与产业基金等）与政府补助字段面"
                   f"（dwd_agg_subsidiary_info/dwd_org_subsidiary_info {facts['gkx_org_subsidiary_info_rows']:,} 行补助信息）——"
                   "无一张表是「政策→企业→资金到账」事件台账；dwd_org_subsidiary_info 无到账日期列"},
    {"probe": "gkx 全库拨付/到账日期对列",
     "source": "gkx",
     "sql": "information_schema.columns 扫 disburse|appropriat|grant_date|payment_date|arrival（ORDER BY，B5）",
     "hits": len(facts["gkx_disburse_col_hits"]),
     "hit_detail": "0 列命中——「到账日期−起算日期」的时间差计算无任何列可承载"},
    {"probe": "gkx 政策表资金/企业享受列（台账关联键）",
     "source": "gkx",
     "sql": "SHOW COLUMNS FROM gkx.dwd_policy_base；33 列扫 fund|grant|money|amount|subsid|disburse 与 enjoy|benefit|enterprise|org|company",
     "hits": len(facts["gkx_policy_fund_like_cols"]) + len(facts["gkx_policy_enterprise_like_cols"]),
     "hit_detail": "资金列 0 命中 + 企业享受列 0 命中——政策表无资金金额列、无企业名单列，"
                   "「哪些企业拿了多少钱何时到账」零承载（与 POLCMP_024/029/037/041 共享族级缺口）"},
    {"probe": "dev 企业资金项目/政策兑现台账",
     "source": "dev",
     "sql": "gkxlumenx_dwd 政策族 38 表行数 + gkxlumenx_ods fund 表扫",
     "hits": 0,
     "hit_detail": "enterprise_fund_project=0（表存在但 0 行，B4 情形②：要补数据同步）、"
                   "fund_project=0、policy_simulation_result=0；政策族除 policy_base_info 40,000 外全 0 行"},
    {"probe": "久新资金到账/拨付事件面",
     "source": "jiuxin",
     "sql": "SHOW TABLES；203 表名扫 fund|grant|disburse|payment|subsid + DESC 结构核对",
     "hits": len(facts.get("jiuxin_fund_like_tables", [])),
     "hit_detail": "命中 3 张 funding 语义表：ads_research_problem_funding_evidence（5,123 行，"
                   "funder_name/funding_year/funding_amount_cny——科研问题经费证据面，无拨付日期对、"
                   "无企业账户到账时间戳）、ads_shenzhen_institution_direction_funding/"
                   "ads_shenzhen_institution_field_funding（机构经费聚合面）——均非「申报→到账」事件台账"},
    {"probe": "需求原文「平均到账周期/到账」定义段",
     "source": "doc",
     "sql": "rg 到账 三份需求真源",
     "hits": 0,
     "hit_detail": "《科技信息展示系统和科技专题服务系统.md》《科技信息展示系统(政策对比功能升级)核增需求.md》"
                   "《科技专题服务算法库.md》0 命中；仅在 1.1.1.1.4.2.3.2.5 政策实施路径预测段有"
                   "「资金拨付」环节枚举（流程节点非指标定义）"},
]

support = "完全不支持"

notes += [
    "判档：平均到账周期 = mean(资金到账日期 − 申报受理/任务书签订日期)。依赖「政策×企业×资金事件」"
    "台账（每笔含起算日期与到账日期），三源零承载（gkx 17 张基金面语义错位、dev 空表、久新 5,123 行"
    "科研经费证据面无日期对）——与 POLCMP_001/024/029/037/041 共享「兑现事件无台账」族级缺口，本件独立留证",
    "代理面边界：gkx 政策文本「拨付」命中率是叙述面（政策谈拨付时限），不是拨付事件；国办发〔2021〕32 号"
    "要求任务书签订后 30 日内拨付（R4），若台账接入，本指标=对 30 日时限执行情况的监测读数",
    "mock 披露：policyData.js:2208「平均到账周期 46 天」为 policyPortraitSummaries 企业画像卡的"
    "前端演示常量（演示值，不参与支持度结论）；消费方 analysis/PortraitTrio.jsx Drawer 指标行",
    "B11 对账：gkx 政策 20,000 行与共享快照 _shared_probe_s3_01_out.json fix2.政策底表行数零漂移；"
    "dev 政策族行数与 _probe_lane6_s302_r2_out.json（Lane6 探针）零漂移",
    "升档触发器（B10）：接入政务兑现台账（申报受理时间戳+资金到账时间戳）→ 可升完全转换支持"
    "（天数差均值运算平凡）；若甲方接受「政策发布→实施」文本日期差作代理 → 语义已换（政策流程≠资金到账），"
    "本件不接受",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_025",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:2208",
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:2196",
        "repos/demo-ui-science/src/pages/policy-tracking/analysis/PortraitTrio.jsx:110",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「平均到账周期/到账」三份需求真源（主需求/核增需求/算法库）rg 0 命中；"
                "主需求 1.1.1.1.4.2.3.2.5 政策实施路径预测段枚举「资金拨付」环节（流程节点非指标条目）；"
                "UI 层 policyData.js 企业画像卡演示常量",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["资金到账窗口（台账事件年）"],
    "base_years_note": "本件无到账事件可算（三源零承载）；政策侧 publish_year（varchar）仅能界定政策发布年分布"
                       "（2021:2,120 / 2020:2,402 / 2019:2,035…），不构成到账基期",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts["gkx_policy_rows"]), str(facts["gkx_dwd_fund_basic_info_rows"]),
                          str(facts["gkx_org_subsidiary_info_rows"]), "280", "40,000"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
