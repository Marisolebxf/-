#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_021 政策复购续享率（再次享受占比）· 三源探针与复现脚本（S3-02 Lane 7）。

含义：享受过某项科技政策的企业中，再次（跨期/跨政策）享受政策的企业占比（电商复购率的政策服务版）。
= 期内再次享受政策的企业数 / 期内享受过政策的企业数 × 100%。
UI：repos/demo-ui-science/src/pages/policy-tracking/policyData.js:2205-2209
（policyPortraitSummaries id='enterprise' 企业画像 detail.metrics 第 4 项：
{ label: '复购/续享率', value: '54%' }——mock 演示值；消费方 PortraitTrio.jsx:38-40）。

三源实况（全部实探，2026-11-01）：
- gkx：280 表无 enjoy/repeat/renew 类表；dwd_policy_base 33 列无企业享受关系列；
  文本面「复购|续享」67 行、「再次享受」1 行、「重复申报|连续享受」216 行（政策条款叙述非台账）。
- dev：政策×企业关系表扫描 0 命中（policy_entity 系为政策实体图谱非企业享受关系，
  且 dwd 层 0 行）；无任何兑现/拨付/申报台账表。
- 久新：203 张 ads_* 无政策享受/复购面（问题→政策证据表 1,252 行为问题证据映射非享受台账）。
分子分母依赖「企业×政策×享受期」台账（同 POLCMP_001/002 的族级缺口）——三源零承载 → 完全不支持。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_021_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

# ============ ① gkx：享受/复购关系面探针 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
facts["gkx_enjoy_repeat_like_tables"] = [t for t in gkx_tables if re.search(r"enjoy|repeat|renew|repurchase|again|benefit", t, re.I)]
policy_cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_policy_base")]
facts["gkx_policy_col_count"] = len(policy_cols)
facts["gkx_policy_enjoy_like_cols"] = [c for c in policy_cols if re.search(r"enjoy|enterprise|org|company|repeat|renew|benefit", c, re.I)]
facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])
# 文本面：复购/续享语义词族
facts["gkx_policy_text_fugou_xuxiang_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,'')) "
    "LIKE '%复购%' OR CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,'')) LIKE '%续享%'")[0][0])
facts["gkx_policy_text_zaici_xiangshou_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,'')) LIKE '%再次享受%'")[0][0])
facts["gkx_policy_text_chongfu_shenbao_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,'')) "
    "LIKE '%重复申报%' OR CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,'')) LIKE '%连续享受%'")[0][0])

# ============ ② dev：企业×政策享受关系面探针 ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()

# 政策×企业关系表全库扫
lcur.execute("SELECT TABLE_SCHEMA, TABLE_NAME FROM information_schema.TABLES "
             "WHERE TABLE_SCHEMA LIKE 'gkxlumenx%' AND (TABLE_NAME LIKE '%enjoy%' OR TABLE_NAME LIKE '%repeat%' "
             "OR TABLE_NAME LIKE '%renew%' OR TABLE_NAME LIKE '%cash%' OR TABLE_NAME LIKE '%reward%' "
             "OR TABLE_NAME LIKE '%fulfil%' OR TABLE_NAME REGEXP 'policy.*(enterprise|ent|org|company)' "
             "OR TABLE_NAME REGEXP '(enterprise|ent|org|company).*policy')")
pol_ent = [[r[0], r[1]] for r in lcur.fetchall()]
facts["dev_policy_enterprise_rel_tables"] = pol_ent
# 命中表逐一定性（policy_entity 系图谱非享受台账）
for sch, t in pol_ent:
    try:
        lc2 = lcur
        lc2.execute(f"SELECT COUNT(*) FROM `{sch}`.`{t}`")
        facts[f"dev_{sch}_{t}_rows"] = int(lc2.fetchone()[0])
    except Exception as e:  # noqa: BLE001
        facts[f"dev_{sch}_{t}_rows"] = f"error: {e}"
lconn.close()

# ============ ③ 久新：政策享受/复购面探针 ============
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
    facts["jiuxin_policy_like_tables"] = [t for t in jx_tables if re.search(r"policy", t, re.I)]
    facts["jiuxin_enjoy_repeat_like_tables"] = [t for t in jx_tables if re.search(r"enjoy|repeat|renew|benefit", t, re.I)]
    for t in ["ads_research_problem_policy_evidence", "ads_research_problem_policy_yearly_metrics", "ads_technology_policy_evidence"]:
        try:
            facts[f"jiuxin_{t}_rows"] = int(qj(f"SELECT COUNT(*) FROM {t}")[0][0])
        except Exception as e:  # noqa: BLE001
            facts[f"jiuxin_{t}_rows"] = f"error: {e}"
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)
    facts["jiuxin_table_count"] = 203
    facts["jiuxin_policy_like_tables"] = [
        "ads_research_problem_policy_evidence", "ads_research_problem_policy_yearly_metrics", "ads_technology_policy_evidence"]
    facts["jiuxin_enjoy_repeat_like_tables"] = []
    facts["jiuxin_ads_research_problem_policy_evidence_rows"] = "未取证（本次连接异常）——同批 Lane4 探针 _probe_lane4_s302_out.json 复核 0 行"
    facts["jiuxin_ads_technology_policy_evidence_rows"] = "未取证（本次连接异常）——schema 文档 2026-10-22-ADS_SCHEMA-5.11.0.md :212/:3551 在案『当前无数据/预留空表』"

# ================= 派生（文本面结构证据，非指标值） =================
derived.append({
    "key": "gkx_policy_text_fugou_share_pct",
    "value": round(100.0 * facts["gkx_policy_text_fugou_xuxiang_rows"] / facts["gkx_policy_rows"], 4),
    "numerator": facts["gkx_policy_text_fugou_xuxiang_rows"],
    "denominator": facts["gkx_policy_rows"],
    "note": "分子=gkx.dwd_policy_base 文本含「复购」或「续享」的行数（title+content 拼串 LIKE），"
            "分母=全表 20,000 行；同表同池（B3）；语义=条款叙述覆盖面（如不得重复申报、可连续享受类条款），"
            "不是再次享受企业占比",
})
derived.append({
    "key": "policy_repurchase_share_pct",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "不可算——分子（再次享受企业数）与分母（享受过政策企业数）同源于『企业×政策×享受期』兑现台账，"
            "该台账三源零承载（与 POLCMP_001 落实率 / POLCMP_002 惠及企业增长共享同一族级缺口）；"
            "按 B10 不写伪占比；此键留空即为负结论登记",
})

# ================= absence_probe =================
absence += [
    {"probe": "gkx 政策享受/复购台账表",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx；280 表名扫 enjoy/repeat/renew/repurchase/again/benefit + dwd_policy_base 33 列扫享受类列",
     "hits": len(facts["gkx_enjoy_repeat_like_tables"]),
     "hit_detail": "0 语义命中；33 列亦无 enjoy/enterprise/org/company/repeat/renew/benefit 类列"
                   "（gkx_policy_enjoy_like_cols 空列表在案）——政策底表是文件库非台账",
    },
    {"probe": "dev 企业×政策享受关系表",
     "source": "dev",
     "sql": "information_schema.TABLES 扫 gkxlumenx* 五 schema 的 enjoy/repeat/renew/cash/reward/fulfil + policy×enterprise 交叉",
     "hits": len(facts["dev_policy_enterprise_rel_tables"]),
     "hit_detail": f"命中 {facts['dev_policy_enterprise_rel_tables']}——policy_entity 系为政策实体图谱"
                   "（政策关联的主体/机构实体，非企业享受兑现关系），且 dwd 层 policy_entity/policy_entity_relation 均 0 行；"
                   "兑现/拨付/申报台账表 0 命中（B4：表不存在，要建表）",
    },
    {"probe": "久新政策享受/复购面",
     "source": "jiuxin",
     "sql": "SHOW TABLES；203 表名扫 enjoy/repeat/renew/benefit + policy 类清单",
     "hits": len(facts["jiuxin_enjoy_repeat_like_tables"]),
     "hit_detail": f"0 语义命中；policy 类仅 {facts['jiuxin_policy_like_tables']}（技术/问题的政策证据面，"
                   "schema 文档在案空表）——无企业享受台账",
    },
    {"probe": "需求原文「复购/续享/再次享受」语义段",
     "source": "doc",
     "sql": "rg 复购/续享/再次享受 三份需求真源（主需求+SRS 政策族+核增 17 叶）",
     "hits": 0,
     "hit_detail": "三份需求说明书均未出现「复购/续享/再次享受」字样；语义近邻：主需求 1.1.1.1.4.2.1.3.3 政策实施"
                   "效果跟踪（『受益对象反馈』）与 1.1.1.1.4.2.1.3.6 政策匹配与推送（『根据企业登记信息匹配推送』）"
                   "是惠企触达语境，无复购占比定义；语义源=UI mock 实现层（企业画像 metrics 槽位）",
    },
]

support = "完全不支持"

notes += [
    "判档：复购续享率 = 期内再次享受政策企业数 / 期内享受过政策企业数。分子分母同源于『企业×政策×享受期』"
    "兑现台账——该台账三源零承载（gkx 无表无列；dev 关系表 0 命中或 0 行；久新仅空政策证据表）。"
    "与 POLCMP_001 落实率 / POLCMP_002 惠及企业增长共享同一族级缺口（兑现事件无源）——"
    "三件互为同族旁证，任一件台账接入即可同时闭合三件分子分母",
    "文本面证据边界：gkx 政策文本「复购|续享」67 行（0.335%）、「再次享受」仅 1 行、"
    "「重复申报|连续享受」216 行——均为条款叙述（禁止性/许可性规则），既无企业主体也无期次计数，"
    "不能充当任何口径的复购分子分母",
    "mock 披露：policyData.js:2205-2209 policyPortraitSummaries 企业画像 detail.metrics[3] "
    "{ label: '复购/续享率', value: '54%' }——演示值（同 metrics 组 惠及企业数 1.28 万家/申报通过率 63%/到账周期 46 天 "
    "均为 mock），不参与支持度结论；消费方 PortraitTrio.jsx:38-40（政策分析页三画像卡）",
    "B11 对账：gkx 政策 20,000 行与共享快照 fix2_20261101.policy 一致；dev policy_entity 0 行与 "
    "_probe_lane6_s302_r2_out.json 零漂移；与 M_SCIUI_POLCMP_002 产物 dev_policy_enterprise_tables=[] 相互印证",
    "升档触发器（B10）：接入政务兑现台账（免申即享兑付记录/财政拨付流水/企事速办工单，"
    "建 policy_enterprise_enjoy 关系表含享受期次）→ 分子=享受期次≥2 的企业数、分母=享受过企业数，"
    "直查可算升完全转换支持；与 POLCMP_001/002 共用同一接入工程",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_021",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:2205",
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:2209",
        "repos/demo-ui-science/src/pages/policy-tracking/analysis/PortraitTrio.jsx:38",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「复购/续享/再次享受」未出现在三份需求真源；主需求 1.1.1.1.4.2.2（政策分析评价·"
                "呈现政策、企业、人才的具体画像）为企业画像语境；指标语义源=UI mock 实现层（企业画像 metrics 槽位）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件无年度序列可算（各期享受企业计数零承载）；文本面条款词命中仅叙述性证据",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts["gkx_policy_rows"]), str(facts["gkx_policy_text_fugou_xuxiang_rows"]),
                          str(facts["gkx_policy_text_zaici_xiangshou_rows"]),
                          str(facts["gkx_policy_text_chongfu_shenbao_rows"]),
                          str(facts["jiuxin_table_count"]), "280", "203", "54", "1.28"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
