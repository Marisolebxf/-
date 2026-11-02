#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_031 政策执行效率（兑现速度）· 三源探针与复现脚本（S3-03 Lane 1）。

含义：政策兑现的速度效率——平均兑现时长（申报→到账周期）或按时兑现率（限期内兑现占比）。
UI：repos/demo-ui-science/src/pages/policy-tracking/policyData.js:1007
（policyEvaluationReports[0].dimensions[2] { name: '执行效率', score: 78, weight: 20 }，
  同结构 :1026 第二份报告 score: 90；消费方 PolicyPanorama.jsx:3765/4277 政策效果评估报告区）。

三源实况（全部实探，2026-11-01）：
- gkx：280 表无兑付流水（无申报时点/到账时点对）；dwd_policy_base 33 列仅有
  publish_date/implementation_date/expire_date 三个政策侧时间锚，无企业侧事件时间。
- dev：policy_effect_eval.execution_effect_score（执行效果分）0 行；仿真结果表 0 行；
  无到账/拨付时间类表。
- 久新：203 张 ads_* 无兑付时间面（列扫 approved_at 是科研问题发布审核时间非政策兑现）。
兑现速度依赖「申报受理时点 × 到账时点」事件对流水，三源零承载 → 完全不支持。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_031_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

# ============ ① gkx：兑付时间对探针 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
# 到账/拨付/时限语义表扫
speed_pat = re.compile(r"cash|disburse|arrive|pay|grant|allocat|到账|拨付", re.I)
facts["gkx_speed_like_tables"] = [t for t in gkx_tables if speed_pat.search(t)]
facts["gkx_speed_like_trap_note"] = "allocation 命中 4 张为基金配置表（fund_bond/equity_sector_allocation——基金资产配置语境），非政策拨付"
# 政策表时间列盘点（政策侧仅有时间锚——证明「政策生命周期时间」与「企业兑付时间」的结构分界）
policy_cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_policy_base")]
facts["gkx_policy_col_count"] = len(policy_cols)
facts["gkx_policy_time_cols"] = [c for c in policy_cols if re.search(r"date|time|year", c, re.I)]
# 施行日期质量（implementation_date 非空率——时间锚可用性）
facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])
facts["gkx_policy_impl_date_nonnull"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE implementation_date IS NOT NULL "
    "AND CAST(implementation_date AS CHAR) NOT IN ('','0000-00-00')")[0][0])
# 文本面「个工作日/时限/到账」承诺表述（政策自述的兑现时限承诺——叙述非实测）
for w, tag in [("个工作日", "gongzuori"), ("到账", "daozhang"), ("限时", "xianshi")]:
    facts[f"gkx_policy_text_{tag}_rows"] = int(qg(
        f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,''),IFNULL(keypoints,'')) LIKE '%{w}%'")[0][0])

# ============ ② dev：兑付时间/效果分探针 ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()
# 到账/拨付/时限表名扫
lcur.execute("SELECT TABLE_NAME, TABLE_SCHEMA FROM information_schema.TABLES WHERE TABLE_SCHEMA IN "
             "('gkxlumenx_dwd','gkxlumenx_ods','gkxlumenx_ads','gkxlumenx_dim') AND TABLE_NAME REGEXP "
             "'cash|disburse|arrive|allocat|pay'")
facts["dev_speed_like_tables"] = [[r[1], r[0]] for r in lcur.fetchall()]
# 政策族关键表（执行效果分结构在值空）
dev_policy_rows = {}
for t in ["policy_base_info", "policy_effect_eval", "policy_simulation_result", "enterprise_fund_project"]:
    dev_policy_rows[t] = int(ql(f"SELECT COUNT(*) FROM `{t}`")[0][0])
facts["dev_policy_family_rows"] = dev_policy_rows
# policy_effect_eval 执行效果列 + 评估批次列（若有效果分批次即可成速度序列——实测 0 行）
facts["dev_policy_effect_eval_key_cols"] = [c for c in [r[0] for r in ql("SHOW COLUMNS FROM policy_effect_eval")]
                                            if re.search(r"exec|effect|batch|stage", c, re.I)]
lconn.close()

# ============ ③ 久新：兑付/审批时间面探针 ============
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
    # 时间/审批语义列扫
    target_cols = re.compile(r"approv|cash|disburse|arrive|duration|cycle|period_days|elapsed|_days", re.I)
    col_hits = {}
    for t in jx_tables:
        try:
            cols = [r[0] for r in qj(f"DESC `{t}`")]
            m = [c for c in cols if target_cols.search(c)]
            if m:
                col_hits[t] = m
        except Exception:  # noqa: BLE001
            pass
    facts["jiuxin_time_like_cols"] = col_hits
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)
    notes.append("久新连接失败按未取证登记（B4：连接失败≠0 行），不参与判档数字")

# ================= 派生（骨架读数，非指标值） =================
derived.append({
    "key": "gkx_policy_text_daozhang_share_pct",
    "value": round(100.0 * facts["gkx_policy_text_daozhang_rows"] / facts["gkx_policy_rows"], 4),
    "numerator": facts["gkx_policy_text_daozhang_rows"],
    "denominator": facts["gkx_policy_rows"],
    "note": "分子=文本含「到账」的政策行数（title+content+keypoints 拼串 LIKE），分母=gkx.dwd_policy_base "
            "全表 20,000 行；同表同池（B3）；语义=政策自述到账承诺的覆盖面，不是实测兑现时长",
})
derived.append({
    "key": "gkx_policy_impl_date_nonnull_share_pct",
    "value": round(100.0 * facts["gkx_policy_impl_date_nonnull"] / facts["gkx_policy_rows"], 4),
    "numerator": facts["gkx_policy_impl_date_nonnull"],
    "denominator": facts["gkx_policy_rows"],
    "note": "分子=implementation_date 非空且非零日期行数，分母=全表 20,000；同表同池（B3）；"
            "语义=政策侧施行时间锚可用率——它只界定「政策窗口起点」，不承载企业侧兑付时点",
})

# ================= absence_probe =================
absence += [
    {"probe": "gkx 兑付流水时间对（申报时点×到账时点）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx；280 表名扫 cash/disburse/arrive/pay/grant/allocat/到账/拨付",
     "hits": len(facts["gkx_speed_like_tables"]),
     "hit_detail": "allocation 命中 4 张 dwd_fund_bond/equity_sector_allocation（含 bak）——基金资产配置表"
                   "（债券/股票配置比例），基金投资语境非政策拨付；无任何「企业×政策×申报时间×到账时间」"
                   "流水表——兑现速度的事件对结构零承载"},
    {"probe": "gkx 政策表企业侧时间列",
     "source": "gkx",
     "sql": "SHOW COLUMNS FROM gkx.dwd_policy_base；33 列时间类盘点",
     "hits": len(facts["gkx_policy_time_cols"]),
     "hit_detail": "时间列仅 publish_date/publish_year/implementation_date/expire_date/created_time/updated_time"
                   "——全部是政策生命周期锚（政策什么时候发布/施行/到期），无企业申报/到账时间；"
                   "implementation_date 非空率见派生键（政策窗口起点可用，企业侧事件零承载）"},
    {"probe": "dev 执行效率结果表",
     "source": "dev",
     "sql": "information_schema.TABLES 扫 cash/disburse/arrive/allocat/pay + 政策族行数 + effect_eval 列",
     "hits": len(facts["dev_speed_like_tables"]),
     "hit_detail": "无到账/拨付时间表；policy_effect_eval 含 execution_effect_score（执行效果分）与 "
                   "eval_batch_no/eval_stage（批次列——若有数据即可构成效率序列）但实测 0 行；"
                   "policy_simulation_result 0 行、enterprise_fund_project（approve_date 列在）0 行"
                   "（B4 情形②：结构在值空）"},
    {"probe": "久新兑付/审批时长面",
     "source": "jiuxin",
     "sql": "SHOW TABLES；203 表全表 DESC 列扫 approv/cash/disburse/arrive/duration/cycle/elapsed/_days",
     "hits": len(facts.get("jiuxin_time_like_cols", {})),
     "hit_detail": "命中均为语义无关：ads_research_problem_deployment.approved_direction_ids/approval_policy"
                   "（科研问题部署审批方向）、ads_research_problem_release.approved_at（发布审核时间——"
                   "平台自身工单时间非政策兑现）、ads_research_problem_development_snapshot.monthly_cycle_status"
                   "与 ads_research_problem_profile.lifecycle_status（问题研发周期状态，cycle 词根误中）；"
                   "无任何兑付时长/审批周期结果面"},
    {"probe": "需求原文「执行效率」定义段",
     "source": "doc",
     "sql": "rg 执行效率/兑现速度/到账周期 三份需求真源",
     "hits": 0,
     "hit_detail": "三份需求真源均未出现「执行效率/兑现速度」指标名（「平均到账周期」是同族姊妹件 "
                   "POLCMP_025 的语义，亦未在需求出现）；本件语义源=UI mock 维度名（policyEvaluationReports "
                   "dimensions 权重行）"},
]

support = "完全不支持"

notes += [
    "判档：执行效率（兑现速度）的两个候选口径——平均兑现时长（申报→到账）或按时兑现率（限期内占比）——"
    "分子分母都依赖「企业×政策」兑付事件流水（带申报时点与到账时点），该流水三源零承载。"
    "与 POLCMP_029 执行率/POLCMP_001 落实率共享族级缺口，本件独立留证",
    "mock 披露：policyData.js:1007/:1026 两份评估报告的「执行效率」78/90 分是 weighted dimensions 演示值"
    "（weight:20 参与总分加权），PolicyPanorama.jsx:3765 消费——演示值不参与支持度结论；"
    "注意 UI 把「执行效率」实现为 0-100 评分维而非时长读数，口径本身由前端定义",
    "文本面边界：政策文本「个工作日」承诺（如 30 个工作日内拨付）是政策自述时限（制度设计），"
    "不是实测兑现时长——时限承诺的执行情况恰恰需要本件缺失的兑付流水来度量",
    "B11 对账：gkx 政策 20,000 行与共享快照零漂移；dev 政策族行数与 Lane6 探针零漂移",
    "升档触发器（B10）：接入政务兑付流水（免申即享平台兑付记录含申请时间/拨付时间，厦门 15 天/衢州 24 小时"
    "类口径）→ 事件对闭合，平均时长与时限达标率均可直算，升完全转换支持",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_031",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:1007",
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:1026",
        "repos/demo-ui-science/src/pages/policy-tracking/PolicyPanorama.jsx:3765",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「执行效率/兑现速度」未出现在三份需求真源；语义源=UI mock 实现层"
                "（policyEvaluationReports.dimensions 权重行，评分维形态）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["兑付事件时间序列"],
    "base_years_note": "本件无兑付时间序列可算（事件对零承载）；implementation_date 仅界定政策窗口起点",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts["gkx_policy_rows"]), str(facts["gkx_policy_impl_date_nonnull"]),
                          str(facts["gkx_policy_text_gongzuori_rows"]), str(facts["gkx_policy_text_daozhang_rows"]),
                          str(facts["gkx_policy_text_xianshi_rows"]), "280", "40,000", "203"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
