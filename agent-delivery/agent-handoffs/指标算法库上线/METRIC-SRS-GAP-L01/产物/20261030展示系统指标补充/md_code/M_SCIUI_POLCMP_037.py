#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_037 政策申报通过率 · 三源探针与复现脚本（S3-03 Lane 1）。

含义：企业向政策申报扶持事项的获批比例 = 通过（获批）申报数 / 提交申报总数。
UI：repos/demo-ui-science/src/pages/policy-tracking/policyData.js:2207
（policyPortraitSummaries[1] 企业画像卡 detail.metrics[1]
  { label: '申报通过率', value: '63%' }；同卡四读数：惠及企业数 1.28 万家/申报通过率 63%/
  平均到账周期 46 天/复购续享率 54%；消费方 analysis/PortraitTrio.jsx 三画像卡区）。

三源实况（全部实探，2026-11-01）：
- gkx：280 表扫 declare/apply/approv/exam/review 零政策申报语义命中（dwd_patent_applicants
  是专利申请人）；dwd_policy_base 33 列无申报/审批状态列；文本面「申报」5,405 行/
  「通过率」13 行（叙述非流水）。
- dev：四 schema 无申报/审批工单表；政策族 38 表除 policy_base_info 40,000 外全 0 行。
- 久新：203 张 ads_* 无申报/审批面（列扫 approved_* 是科研问题发布审核语境）。
分子（获批申报数）分母（提交申报数）同源于「企业×政策×申报工单」流水，三源零承载 → 完全不支持。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_037_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

# ============ ① gkx：申报/审批流水探针 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
# 申报/审批语义表扫
apply_pat = re.compile(r"declare|apply|applic|approv|exam|review|audit|submit", re.I)
facts["gkx_apply_like_tables"] = [t for t in gkx_tables if apply_pat.search(t)]
# 申请人表语义核对（专利申请人陷阱）
if "dwd_patent_applicants" in facts["gkx_apply_like_tables"]:
    facts["gkx_patent_applicants_cols"] = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_patent_applicants")]
    facts["gkx_patent_applicants_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_patent_applicants")[0][0])
# 政策表申报/审批列扫
policy_cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_policy_base")]
facts["gkx_policy_col_count"] = len(policy_cols)
facts["gkx_policy_apply_like_cols"] = [c for c in policy_cols if re.search(r"declare|apply|approv|exam|review|audit|status", c, re.I)]
# 政策底表与文本面
facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])
for word, tag in [("申报", "shenbao"), ("通过率", "tongguolv"), ("受理", "shouli"), ("评审", "pingshen")]:
    facts[f"gkx_policy_text_{tag}_rows"] = int(qg(
        f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,''),IFNULL(keypoints,'')) LIKE '%{word}%'")[0][0])
# 「通过率+数字」表述（文本中可抽取的具名读数边界）
facts["gkx_policy_text_tongguolv_with_number_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE content LIKE '%通过率%' "
    "AND content REGEXP '通过率[^。]{0,15}[0-9]+\.?[0-9]*%?'")[0][0])

# ============ ② dev：申报/审批工单探针 ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()
lcur.execute("SELECT TABLE_NAME, TABLE_SCHEMA FROM information_schema.TABLES WHERE TABLE_SCHEMA IN "
             "('gkxlumenx_dwd','gkxlumenx_ods','gkxlumenx_ads','gkxlumenx_dim') AND TABLE_NAME REGEXP "
             "'declare|apply|applic|approv|exam|review|audit|submit'")
facts["dev_apply_like_tables"] = [[r[1], r[0]] for r in lcur.fetchall()]
dev_policy_rows = {}
for t in ["policy_base_info", "policy_effect_eval", "policy_search_record", "enterprise_fund_project"]:
    dev_policy_rows[t] = int(ql(f"SELECT COUNT(*) FROM `{t}`")[0][0])
facts["dev_policy_family_rows"] = dev_policy_rows
lconn.close()

# ============ ③ 久新：申报/审批面探针 ============
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
    facts["jiuxin_apply_like_tables"] = [t for t in jx_tables if apply_pat.search(t)]
    # 审批语义列扫
    target_cols = re.compile(r"approv|apply|declare|submit|accept|reject", re.I)
    col_hits = {}
    for t in jx_tables:
        try:
            cols = [r[0] for r in qj(f"DESC `{t}`")]
            m = [c for c in cols if target_cols.search(c)]
            if m:
                col_hits[t] = m
        except Exception:  # noqa: BLE001
            pass
    facts["jiuxin_apply_like_cols"] = col_hits
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)
    notes.append("久新连接失败按未取证登记（B4：连接失败≠0 行），不参与判档数字")

# ================= 派生（骨架读数，非指标值） =================
derived.append({
    "key": "gkx_policy_text_shenbao_share_pct",
    "value": round(100.0 * facts["gkx_policy_text_shenbao_rows"] / facts["gkx_policy_rows"], 4),
    "numerator": facts["gkx_policy_text_shenbao_rows"],
    "denominator": facts["gkx_policy_rows"],
    "note": "分子=文本含「申报」的政策行数（title+content+keypoints 拼串 LIKE），分母=gkx.dwd_policy_base "
            "全表 20,000 行；同表同池（B3）；语义=申报类政策叙述覆盖面（政策要求企业怎么申报），"
            "不是企业申报行为流水",
})
derived.append({
    "key": "gkx_policy_text_tongguolv_share_pct",
    "value": round(100.0 * facts["gkx_policy_text_tongguolv_rows"] / facts["gkx_policy_rows"], 4),
    "numerator": facts["gkx_policy_text_tongguolv_rows"],
    "denominator": facts["gkx_policy_rows"],
    "note": "分子=文本含「通过率」的政策行数，分母=全表 20,000；同表同池（B3）；"
            "语义=通过率一词在政策文本的出现面（多为评审规则自述），不是实测通过率",
})

# ================= absence_probe =================
absence += [
    {"probe": "gkx 申报/审批工单流水表",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx；280 表名扫 declare/apply/applic/approv/exam/review/audit/submit",
     "hits": len(facts["gkx_apply_like_tables"]),
     "hit_detail": "命中 dwd_patent_applicants（专利申请人表）——专利著录语境的 applicants 词根，"
                   "列结构与行数在案证伪；无任何「企业×政策×申报×审批结论」工单表"},
    {"probe": "gkx 政策表申报/审批状态列",
     "source": "gkx",
     "sql": "SHOW COLUMNS FROM gkx.dwd_policy_base；33 列扫 declare/apply/approv/exam/review/audit/status",
     "hits": len(facts["gkx_policy_apply_like_cols"]),
     "hit_detail": "命中 1 列 status（政策自身效力状态：现行有效/失效等），不是企业申报审批状态；"
                   "无申报数/通过数字段"},
    {"probe": "dev 申报/审批工单表",
     "source": "dev",
     "sql": "information_schema.TABLES 四 schema 扫 declare/apply/applic/approv/exam/review/audit/submit",
     "hits": len(facts["dev_apply_like_tables"]),
     "hit_detail": "仅 gkxlumenx_ods.dwd_patent_applicants（与 gkx 同源镜像，专利申请人陷阱）；"
                   "政策族无申报工单表（policy_search_record 是站内搜索记录 0 行）"},
    {"probe": "久新申报/审批面",
     "source": "jiuxin",
     "sql": "SHOW TABLES；203 表扫同词典 + 全表 DESC 列扫 approv/apply/declare/submit/accept/reject",
     "hits": len(facts.get("jiuxin_apply_like_cols", {})),
     "hit_detail": "表名命中 ads_technology_application_case（技术应用案例库，application=技术采纳语境"
                   "非政策申报）与列命中 ads_research_problem_deployment.approved_direction_ids / "
                   "ads_research_problem_release.approval_policy+approved_at+decision_approval_policy——"
                   "均为久新平台自身「科研问题发布审核」工单语境（问题条目何时过审上线），"
                   "不是政策申报审批；无任何申报通过率结果面"},
    {"probe": "需求原文「申报通过率」定义段",
     "source": "doc",
     "sql": "rg 申报通过率/通过率/获批 三份需求真源",
     "hits": 0,
     "hit_detail": "三份需求真源均未出现「申报通过率」指标名；主需求政策分析评价语境"
                   "（1.1.1.1.4.2.2「呈现企业具体画像」）是企业画像语境位但无该读数定义；"
                   "语义源=UI mock 企业画像卡 metric"},
]

support = "完全不支持"

notes += [
    "判档：申报通过率 = 获批申报数 / 提交申报总数。分子分母同源于「企业×政策×申报工单」流水"
    "（每条含申报主体/政策事项/受理/审批结论），该流水三源零承载——gkx 唯一 apply 类表是专利申请人"
    "（著录字段非审批行为）、dev 无工单表、久新审批列是平台自身发布审核。"
    "与 POLCMP_029/031 共享族级缺口（政务侧申报-审批流水无源），本件独立留证",
    "mock 披露：policyData.js:2207 申报通过率 63% 是企业画像卡（PortraitTrio）演示值，"
    "同卡四读数（1.28 万家/63%/46 天/54%）全部为页内 mock（POLCMP_021/025 姊妹件同池）——"
    "演示值不参与支持度结论；summary 文案「中小微企业申报通过率仍有提升空间」同样是 mock 叙述",
    "文本面边界：「通过率」13 行命中多为评审规则自述（如「评审通过率不低于 90%」是立项要求），"
    "带数字表述仅 4 行——制度设计值不是实测值；「申报」5,405 行是政策教企业怎么申报（流程叙述），"
    "不是企业的申报行为记录",
    "B11 对账：gkx 政策 20,000 行与共享快照零漂移；dev 政策族与 Lane6 探针零漂移",
    "升档触发器（B10）：接入政务申报审批工单（政策申报系统受理-审批闭环记录，黑龙江平台"
    "「申报/审批/兑现」八环节工单口径）→ 分子分母闭合，升完全转换支持；"
    "若采用「政策匹配成功数/推送数」代理 → 语义已换（匹配≠申报），本件不接受",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_037",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:2207",
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:2200",
        "repos/demo-ui-science/src/pages/policy-tracking/analysis/PortraitTrio.jsx:38",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「申报通过率/通过率」未出现在三份需求真源；主需求 1.1.1.1.4.2.2 政策分析评价"
                "（「呈现企业具体画像」）是企业画像语境位但无该读数；语义源=UI mock 实现层",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["各期申报与获批计数序列"],
    "base_years_note": "本件无申报流水可算（工单零承载）；文本面通过率表述是制度设计值非实测序列",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts["gkx_policy_rows"]), str(facts["gkx_policy_text_shenbao_rows"]),
                          str(facts["gkx_policy_text_tongguolv_rows"]),
                          str(facts["gkx_policy_text_tongguolv_with_number_rows"]),
                          str(facts["gkx_patent_applicants_rows"]), "280", "40,000", "203"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
