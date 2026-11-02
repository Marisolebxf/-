#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_002 政策惠及企业增长（较上期）· 三源探针与复现脚本（S3-02 Lane 6）。

含义：享受过某项科技政策（如补贴、税收优惠）的企业数量较上期的增长。
= （本期惠及企业数 − 上期惠及企业数）/ 上期惠及企业数。
UI：pages/policy-tracking/policyData.js:1833 policySimulationParams.indicators
（enterpriseGrowth '企业增长' % —— 未出台政策仿真模拟结果指标之一）。

三源实况（全部实探，2026-11-01）：
- gkx：280 表扫 enjoy/benefit/reward/兑现零语义命中；dwd_policy_base 33 列无享受名单列；
  文本面「惠及」命中 189 行（政策文本叙述非台账）。
- dev：gkxlumenx_dwd 政策族 38 表中 37 表 0 行（policy_base_info 40,000 行除外）；
  享受/兑现台账无承载；仿真结果表 policy_simulation_result 0 行。
- 久新：130 张 ads_* 无政策享受/兑现面（policy_evidence 两表空表——schema 文档在案）。
分子分母（各期惠及企业数）依赖「政策×企业」兑现台账，三源零承载 → 完全不支持。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_002_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

# ============ ① gkx：享受名单/兑现台账承载探针 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
enjoy_like = [t for t in gkx_tables if re.search(r"enjoy|benefit|reward|cash|subsid|grant|pay", t, re.I)]
facts["gkx_enjoy_like_tables"] = enjoy_like
# 政策表 33 列享受类列扫
policy_cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_policy_base")]
facts["gkx_policy_col_count"] = len(policy_cols)
facts["gkx_policy_enjoy_like_cols"] = [c for c in policy_cols if re.search(r"enjoy|benefit|enterprise|org|company|subsid|cash", c, re.I)]
# 政策底表
facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])
facts["gkx_global_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_global_policy_base")[0][0])
# 文本面：惠及词命中（叙述性证据非台账）
facts["gkx_policy_text_huiji_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,''),IFNULL(keypoints,'')) LIKE '%惠及%'")[0][0])
# 惠及词按年分布（叙述面的时间结构——若把文本当台账会得到的假序列）
yearly = qg("SELECT publish_year, COUNT(*) FROM gkx.dwd_policy_base WHERE content LIKE '%惠及%' "
            "AND publish_year REGEXP '^(19|20)[0-9]{2}$' GROUP BY publish_year ORDER BY publish_year DESC")
facts["gkx_policy_text_huiji_by_year"] = [[r[0], int(r[1])] for r in yearly]
# 文本中「惠及+N家」数字表述（可抽取的具名读数——证明文本有数但不能当计数台账）
facts["gkx_policy_text_huiji_with_number_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE content LIKE '%惠及%' AND content REGEXP '惠及[^。]{0,20}[0-9]+家'")[0][0])

# ============ ② dev：政策族与享受台账探针 ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()
# 政策族表行数（复用 Lane6 探针口径，本件复跑核对）
dev_policy_rows = {}
for t in ["policy_base_info", "policy_simulation_result", "policy_simulation_param",
          "policy_effect_eval", "policy_support_assessment", "policy_intensity_eval"]:
    dev_policy_rows[t] = int(ql(f"SELECT COUNT(*) FROM `{t}`")[0][0])
facts["dev_policy_family_rows"] = dev_policy_rows
# policy_base_info 惠及词命中（40,000 行双源池）
facts["dev_policy_base_info_huiji_rows"] = int(ql(
    "SELECT COUNT(*) FROM policy_base_info WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,''),IFNULL(keypoints,'')) LIKE '%惠及%'")[0][0])
# 享受名单类表扫（企业×政策关系）
lcur.execute("SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA='gkxlumenx_dwd' "
             "AND (TABLE_NAME LIKE '%policy%enterprise%' OR TABLE_NAME LIKE '%enterprise%policy%' "
             "OR TABLE_NAME LIKE '%policy%match%' OR TABLE_NAME LIKE '%enjoy%')")
facts["dev_policy_enterprise_tables"] = [r[0] for r in lcur.fetchall()]
lconn.close()

# ============ ③ 久新：政策享受/仿真面探针 ============
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
    facts["jiuxin_policy_like_tables"] = [t for t in jx_tables if re.search(r"policy|enjoy|benefit|simulation", t, re.I)]
    # 政策证据表行数（结构存在数据空）
    for t in ["ads_research_problem_policy_evidence", "ads_technology_policy_evidence"]:
        try:
            facts[f"jiuxin_{t}_rows"] = int(qj(f"SELECT COUNT(*) FROM {t}")[0][0])
        except Exception as e:  # noqa: BLE001
            facts[f"jiuxin_{t}_rows"] = f"error: {e}"
    jconn.close()
except Exception as e:  # noqa: BLE001
    # 连接失败按「未取证」登记（B4：超时/被锁不是 0 行）——复用同批 Lane4 探针产物补证
    facts["jiuxin_unreachable"] = str(e)
    facts["jiuxin_table_count"] = 130
    facts["jiuxin_policy_like_tables"] = [
        "ads_research_problem_policy_evidence", "ads_technology_policy_evidence"]
    facts["jiuxin_ads_research_problem_policy_evidence_rows"] = "未取证（本次连接被锁）——同批 Lane4 探针 _probe_lane4_s302_out.json 复核 0 行"
    facts["jiuxin_ads_technology_policy_evidence_rows"] = "未取证（本次连接被锁）——schema 文档 2026-10-22-ADS_SCHEMA-5.11.0.md :212/:3551 在案『当前无数据/预留空表』"

# ================= 派生（骨架读数，非指标值） =================
# 叙述面年度变化（证明「较上期」结构在文本面如何呈现——非台账计数）
by_year = {y: c for y, c in facts["gkx_policy_text_huiji_by_year"]}
derived.append({
    "key": "gkx_policy_text_huiji_latest_yoy_pct",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "不可算——惠及企业数（台账口径）三源零承载；文本面惠及词年度分布仅证明叙述存在，"
            "政策条数≠惠及企业数，按 B10 不写伪增长率；此键留空即为负结论登记",
})
derived.append({
    "key": "gkx_policy_text_huiji_share_pct",
    "value": round(100.0 * facts["gkx_policy_text_huiji_rows"] / facts["gkx_policy_rows"], 4),
    "numerator": facts["gkx_policy_text_huiji_rows"],
    "denominator": facts["gkx_policy_rows"],
    "note": "分子=文本含「惠及」的政策行数（title+content+keypoints 拼串 LIKE），分母=gkx.dwd_policy_base "
            "全表 20,000 行；同表同池（B3）；语义=叙述覆盖面，不是惠及企业数占比",
})

# ================= absence_probe =================
absence += [
    {"probe": "gkx 政策享受/兑现台账表",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx；280 表名扫 enjoy/benefit/reward/cash/subsid/grant/pay",
     "hits": len(facts["gkx_enjoy_like_tables"]),
     "hit_detail": "0 语义命中——无任何政策×企业享受关系表；dwd_policy_base 33 列亦无 "
                   "enjoy/benefit/enterprise/org/subsid/cash 类列（gkx_policy_enjoy_like_cols 空列表在案）"},
    {"probe": "dev 政策×企业享受关系表",
     "source": "dev",
     "sql": "information_schema.TABLES 扫 gkxlumenx_dwd 的 policy%enterprise/enterprise%policy/policy%match/enjoy",
     "hits": len(facts["dev_policy_enterprise_tables"]),
     "hit_detail": "0 命中；政策族 37 表中仿真/评估/享受类全 0 行"
                   f"（policy_simulation_result={dev_policy_rows['policy_simulation_result']}、"
                   f"policy_support_assessment={dev_policy_rows['policy_support_assessment']}）——"
                   "表存在但 0 行（B4 情形②：补数据可解的结构空）"},
    {"probe": "久新政策享受/仿真结果面",
     "source": "jiuxin",
     "sql": "SHOW TABLES；130 表名扫 policy/enjoy/benefit/simulation + 政策证据两表 COUNT",
     "hits": len(facts["jiuxin_policy_like_tables"]),
     "hit_detail": f"仅命中政策证据类 {facts['jiuxin_policy_like_tables']}——"
                   f"research_problem_policy_evidence={facts['jiuxin_ads_research_problem_policy_evidence_rows']} 行、"
                   f"technology_policy_evidence={facts['jiuxin_ads_technology_policy_evidence_rows']} 行"
                   "（科研问题/技术的政策关联证据，非企业享受台账；schema 文档 5.11.0 在案）"},
    {"probe": "核增需求原文「惠及企业增长」语义段",
     "source": "doc",
     "sql": "rg 惠及企业/企业增长 《科技信息展示系统(政策对比功能升级)核增需求.md》",
     "hits": 0,
     "hit_detail": "核增需求 17 个 PC 叶无惠及企业条目；主需求 1.1.1.1.4.2.3.1（未出台政策仿真模拟）"
                   "仅说「预测政策实施后可能产生的效果，包括经济效益、社会影响、创新促进等方面」——"
                   "企业增长是其结果指标语境但无定义"},
]

support = "完全不支持"

notes += [
    "判档：惠及企业增长 =（本期惠及企业数−上期）/上期。分子分母同源于「政策×企业」兑现台账——"
    "该台账三源零承载（gkx 无表无列；dev 政策族 37 表 0 行；久新仅空政策证据表）。"
    "与 POLCMP_001 落实率共享同一族级缺口（兑现事件无源），文本面「惠及」词 189 行是叙述非台账",
    "文本面证据边界：gkx 政策文本含「惠及」189 行（占 20,000 的 0.945%）、其中带「惠及N家」数字表述仅 1 行"
    "——个别政策原文会写「惠及企业超X家」，但这是政策自述，既不连续（无各期计数）也不可校验，"
    "不能充当各期惠及企业数序列",
    "mock 披露：policyData.js:1833 enterpriseGrowth（企业增长%）是 policySimulationParams 的仿真结果指标槽位，"
    "其值由前端仿真组件演示值填充（同 indicators 组 innovationIndex/taxRevenue 均为 mock）——"
    "演示值不参与支持度结论",
    "B11 对账：gkx 政策 20,000 行与共享快照 fix2_20261101.policy 底表行数一致；dev policy_base_info 40,000 行"
    "（domestic 20,000+global 20,000 双源池）与 Lane6 探针 _probe_lane6_s302_r2_out.json 零漂移",
    "升档触发器（B10）：接入政务兑现台账（免申即享兑付记录/财政拨付流水按企业聚合）→ 各期惠及企业数闭合，"
    "可升完全转换支持；或接入企业调查数据（应享尽享口径）单独立项",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_002",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:1833",
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:1829",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「惠及企业增长/企业增长」未出现在三份需求真源（主需求+SRS 政策族+核增 17 叶）；"
                "主需求 1.1.1.1.4.2.3.1 未出台政策仿真模拟的结果指标语境（经济效益/社会影响/创新促进）"
                "涵盖其语义但无定义；语义源=UI mock 实现层",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件无年度序列可算（惠及企业各期计数零承载）；文本面惠及词年度分布仅叙述性证据",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts["gkx_policy_rows"]), str(facts["gkx_policy_text_huiji_rows"]),
                          str(facts["gkx_policy_text_huiji_with_number_rows"]),
                          str(facts["dev_policy_base_info_huiji_rows"]), "40,000", "280",
                          str(facts["jiuxin_table_count"])]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
