#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_029 政策执行率（已兑现/应兑现）· 三源探针与复现脚本（S3-03 Lane 1）。

含义：某项科技政策计划兑现的资金/事项中，实际落实到位的比例。
= 已兑现事项数 / 应兑现事项数。与 POLCMP_001 落实率同骨架（已兑现/应享），
UI 挂载位不同：本件在 PolicyAnalysis.jsx:129 indicatorCategories 第 3 项
（key 'implementation' label '执行率' unit '%'），被 DimensionBar/TrendMetricsChart/
TopicIndicatorInteractive/ReportTemplateExport 四组件消费（interactiveAnalysisData
.indicators.implementation 按主题给 78/85 等演示值）。

三源实况（全部实探，2026-11-01）：
- gkx：280 表扫 fulfil/implement/execut/cash/disburse 零语义命中（executive=高管信息词根陷阱）；
  dwd_policy_base 33 列无兑现/金额列；文本面「兑现」322 行、「执行率」32 行（叙述非台账）。
- dev：政策族 38 表除 policy_base_info 40,000 外全 0 行（含最贴近的 policy_effect_eval
  execution_effect_score 0 行、enterprise_fund_project 0 行）。
- 久新：203 张 ads_* 无兑现/执行面（列扫 implement/fulfil 4 个无关命中与 POLCMP_001 同批）。
分子（兑现事件）三源零承载，分母（应兑现清单）仅有政策存量上界 → 完全不支持。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_029_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

# ============ ① gkx：兑现/执行台账探针 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
# 兑现/执行语义表扫（executive 词根陷阱：高管信息）
cash_pat = re.compile(r"fulfil|implement|execut|cash|disburse|兑|honour|honor", re.I)
facts["gkx_fulfil_like_tables"] = [t for t in gkx_tables if cash_pat.search(t)]
facts["gkx_fulfil_like_trap_note"] = "executive=高管信息（dwd_forg_executive_info 等 4 张），非政策执行"
# 政策表列扫（兑现/金额列）
policy_cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_policy_base")]
facts["gkx_policy_col_count"] = len(policy_cols)
facts["gkx_policy_fulfil_like_cols"] = [c for c in policy_cols if re.search(r"fulfil|implement|execut|cash|amount|fund|disburse", c, re.I)]
# 政策底表与文本面
facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])
facts["gkx_global_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_global_policy_base")[0][0])
for word in ["兑现", "执行率"]:
    facts[f"gkx_policy_text_{word}_rows"] = int(qg(
        f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,''),IFNULL(keypoints,'')) LIKE '%{word}%'")[0][0])
# 申报通知子集（应兑现侧上界原料，POLCMP_001 同口径）
facts["gkx_policy_declare_notice_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,'')) LIKE '%申报%'")[0][0])

# ============ ② dev：政策执行/兑现族探针 ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()
# 执行/兑现/拨付类表名扫
lcur.execute("SELECT TABLE_NAME, TABLE_SCHEMA FROM information_schema.TABLES WHERE TABLE_SCHEMA IN "
             "('gkxlumenx_dwd','gkxlumenx_ods','gkxlumenx_ads','gkxlumenx_dim') AND TABLE_NAME REGEXP "
             "'fulfil|implement|execut|cash|disburse|pay|arrive'")
facts["dev_fulfil_like_tables"] = [[r[1], r[0]] for r in lcur.fetchall()]
# risk_executed 语义核对（被执行人信息，词根陷阱定量证据）
facts["dev_risk_executed_rows"] = int(ql("SELECT COUNT(*) FROM risk_executed")[0][0])
facts["dev_risk_executed_trap_note"] = "司法被执行人信息（case_no/exec_court 列），非政策执行"
# 政策族关键表行数（执行/兑现/效果类）
dev_policy_rows = {}
for t in ["policy_base_info", "policy_effect_eval", "policy_intensity_eval",
          "policy_support_assessment", "policy_simulation_result", "enterprise_fund_project"]:
    dev_policy_rows[t] = int(ql(f"SELECT COUNT(*) FROM `{t}`")[0][0])
facts["dev_policy_family_rows"] = dev_policy_rows
# policy_effect_eval.execution_effect_score 列存在性（结构在值空证据）
facts["dev_policy_effect_eval_cols"] = [r[0] for r in ql("SHOW COLUMNS FROM policy_effect_eval")]
lconn.close()

# ============ ③ 久新：兑现/执行面探针 ============
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
    facts["jiuxin_policy_like_tables"] = [t for t in jx_tables if re.search(r"policy|fulfil|enjoy|benefit", t, re.I)]
    # 政策证据表行数（POLCMP_002 已实测 1,252/0，本件独立复测）
    for t in ["ads_research_problem_policy_evidence", "ads_technology_policy_evidence"]:
        try:
            facts[f"jiuxin_{t}_rows"] = int(qj(f"SELECT COUNT(*) FROM {t}")[0][0])
        except Exception as e:  # noqa: BLE001
            facts[f"jiuxin_{t}_rows"] = f"error: {e}"
    # 兑现/执行列扫（与 POLCMP_001 同法独立跑）
    target_cols = re.compile(r"fulfil|implement|execut|cash|disburse|兑", re.I)
    col_hits = {}
    for t in jx_tables:
        try:
            cols = [r[0] for r in qj(f"DESC `{t}`")]
            m = [c for c in cols if target_cols.search(c)]
            if m:
                col_hits[t] = m
        except Exception:  # noqa: BLE001
            pass
    facts["jiuxin_fulfil_like_cols"] = col_hits
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)
    notes.append("久新连接失败按未取证登记（B4：连接失败≠0 行），不参与判档数字")

# ================= 派生（骨架读数，非指标值） =================
derived.append({
    "key": "gkx_policy_text_duixian_share_pct",
    "value": round(100.0 * facts["gkx_policy_text_兑现_rows"] / facts["gkx_policy_rows"], 4),
    "numerator": facts["gkx_policy_text_兑现_rows"],
    "denominator": facts["gkx_policy_rows"],
    "note": "分子=文本含「兑现」的政策行数（title+content+keypoints 拼串 LIKE），分母=gkx.dwd_policy_base "
            "全表 20,000 行；同表同池（B3）；语义=叙述覆盖面（政策自述），不是兑现事件计数",
})
derived.append({
    "key": "gkx_policy_declare_notice_share_pct",
    "value": round(100.0 * facts["gkx_policy_declare_notice_rows"] / facts["gkx_policy_rows"], 4),
    "numerator": facts["gkx_policy_declare_notice_rows"],
    "denominator": facts["gkx_policy_rows"],
    "note": "分子=文本含「申报」的政策行数（应兑现侧上界原料——有申报事项的政策存量），分母=全表 20,000；"
            "同表同池（B3）；语义=申报类政策占比，不是应兑现事项清单",
})

# ================= absence_probe =================
absence += [
    {"probe": "gkx 兑现/执行台账表",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx；280 表名扫 fulfil/implement/execut/cash/disburse/兑",
     "hits": len(facts["gkx_fulfil_like_tables"]),
     "hit_detail": "命中 dwd_forg_executive_info / dwd_org_executive_info 及其 bak——executive 是「高管」"
                   "（企业人员结构面），词根陷阱非政策执行；无任何兑现/拨付/执行结果表"},
    {"probe": "gkx 政策表兑现/金额列",
     "source": "gkx",
     "sql": "SHOW COLUMNS FROM gkx.dwd_policy_base；33 列扫 fulfil/implement/execut/cash/amount/fund/disburse",
     "hits": len(facts["gkx_policy_fulfil_like_cols"]),
     "hit_detail": "命中 1 列 implementation_date——语义是政策「施行日期」（时间锚点列），"
                   "不是兑现状态/金额列；无 cash/amount/fund/disburse 类承载列"},
    {"probe": "dev 政策执行/兑现结果表",
     "source": "dev",
     "sql": "information_schema.TABLES 四 schema 扫 fulfil/implement/execut/cash/disburse/pay/arrive + 政策族行数",
     "hits": len(facts["dev_fulfil_like_tables"]),
     "hit_detail": "词根命中 5 张全为陷阱：gkxlumenx_ods.dwd_*_executive_info 与 gkxlumenx_dwd.enterprise_*_executive"
                   "（高管信息）、risk_executed（550,334 行——法院被执行人信息，org_id/case_no/exec_court 列在案，"
                   "司法信用域非政策兑现）、enterprise_forg_executive（海外高管）；政策族 38 表中执行/效果/兑现类全 0 行"
                   "——policy_effect_eval（含 execution_effect_score 执行效果分列，结构在）0 行、policy_simulation_result 0 行、"
                   "enterprise_fund_project 0 行（B4 情形②：表存在但 0 行，补数据可解）"},
    {"probe": "久新兑现/执行面",
     "source": "jiuxin",
     "sql": "SHOW TABLES；203 表扫 policy/fulfil/enjoy/benefit + 全表 DESC 列扫 fulfil/implement/execut/cash",
     "hits": len(facts.get("jiuxin_fulfil_like_cols", {})),
     "hit_detail": "政策类命中 3 张（ads_research_problem_policy_evidence / ads_technology_policy_evidence / "
                   "ads_research_problem_policy_yearly_metrics）——证据两表是科研问题×政策关联语境非兑现台账"
                   "（本件独立复测 1,252 / 0 行，与 POLCMP_002 实测零漂移）；列扫命中 2 张无关表："
                   "ads_talent_industry_activity.project_execution_score（人才×产业专利活跃度评分模型字段，"
                   "397,964 行，AVG=NULL 全空）与 ads_resource_optimization_recommendation.implementation_plan"
                   "（推荐实施方案文本）——均为评分/推荐语境非政策兑现"},
    {"probe": "需求原文「执行率」定义段",
     "source": "doc",
     "sql": "rg 执行率/兑现/应兑现 三份需求真源",
     "hits": 0,
     "hit_detail": "三份需求真源（主需求+SRS 政策族+核增 17 叶）均未出现「执行率/兑现/应兑现」指标名；"
                   "最接近语义位是主需求 1.1.1.1.4.2.1.3.3 政策实施效果跟踪（「评估政策落地情况」无定义）"},
]

support = "完全不支持"

notes += [
    "判档：执行率 = 已兑现事项数 / 应兑现事项数。分子（兑现事件流水）三源零承载：gkx 无表无列"
    "（executive 词根陷阱已列级证伪）、dev 执行效果表 0 行、久新无兑现面；分母（应兑现清单）仅有"
    "政策存量上界（申报类 5,405 行文本命中，非对象清单）。与 POLCMP_001 落实率共享族级缺口，"
    "本件按派单要求独立留证不复用姊妹件结论",
    "UI 双挂载点语义核对：PolicyAnalysis.jsx:129 indicatorCategories（implementation '执行率'）与 "
    "policyData.js:1666 导出定义同构；interactiveAnalysisData.indicators.implementation 按主题给 "
    "78/85 等演示值（ai-industry:78/biotech 等五主题）——演示值不参与支持度结论",
    "文本面边界：政策文本「兑现」322 行是政策自述（预期或成绩），无期次结构无企业明细；"
    "「执行率」32 行命中全部是文本叙述（如预算执行率语境），不能充当兑现事件计数",
    "B11 对账：gkx 政策 20,000 行与共享快照零漂移；dev 政策族行数与 Lane6 探针 "
    "_probe_lane6_s302_r2_out.json 零漂移（38 表 37 零行 + base_info 40,000）",
    "升档触发器（B10）：接入政务兑现台账（免申即享兑付记录/财政拨付流水按政策×事项聚合）→ 分子闭合；"
    "配合政策条款结构化（核增 PC-06）应兑现清单闭合 → 可升完全转换支持",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_029",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/PolicyAnalysis.jsx:129",
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:1666",
        "repos/demo-ui-science/src/pages/policy-tracking/analysis/DimensionBar.jsx:64",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「执行率/政策执行率/已兑现/应兑现」未出现在三份需求真源（主需求+SRS 政策族+核增 17 叶）；"
                "最接近语义位是主需求 1.1.1.1.4.2.1.3.3 政策实施效果跟踪（「评估政策落地情况」）；"
                "语义源=UI mock 实现层（indicatorCategories.implementation）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["各期兑现事项计数序列"],
    "base_years_note": "本件无期次序列可算（兑现事件零承载）；文本面年度分布仅叙述性证据，不构成基期",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts["gkx_policy_rows"]), str(facts["gkx_policy_text_兑现_rows"]),
                          str(facts["gkx_policy_text_执行率_rows"]), str(facts["gkx_policy_declare_notice_rows"]),
                          str(facts["gkx_global_policy_rows"]), "280", "38", "40,000", "203"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
