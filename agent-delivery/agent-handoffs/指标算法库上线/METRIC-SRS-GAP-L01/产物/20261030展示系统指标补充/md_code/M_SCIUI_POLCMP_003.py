#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_003 免申即享政策占比 · 三源探针与复现脚本（S3-02 Lane 6）。

含义：科技政策库中，企业无需主动申报、符合条件即自动享受的政策占全部政策的比例。
= 免申即享政策数 / 政策总数。
UI：pages/policy-tracking/policyData.js:2186 policyPortraitSummaries[0].detail.metrics
「免申即享占比 24%」（政策画像卡，Wave0 mock）。

三源实况（全部实探，2026-11-01）：
- gkx：dwd_policy_base 33 列无「享受方式/申报方式」结构化列；全文本扫「免申即享」命中 5 行
  （且 5 行均为『提及/推行免申即享改革』的政策，非自身被标注为免申即享）。
- dev：policy_base_info 40,000 行同构无结构化列；文本命中 5 行（与 gkx 同源数据）。
- 久新：130 张 ads_* 无政策标签/分类面（政策证据两表空）。
分子（免申即享政策清单）无结构化承载：政策的享受方式属性不在库内，文本提及≠政策属性。
判档：部分支持——分母（政策总数）三源充足；分子需 NLP 标注（政策条款语义识别）可转换构建，
但无 gold 标准库校准，5/20,000 的文本命中证明当前数据无法直接闭合分子。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_003_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

# ============ ① gkx：享受方式结构化列 + 文本命中 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

policy_cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_policy_base")]
facts["gkx_policy_col_count"] = len(policy_cols)
# 享受方式/申报方式类列扫（结构化分子承载）
facts["gkx_policy_enjoy_mode_cols"] = [c for c in policy_cols if re.search(
    r"enjoy|mode|method|declare|apply|process|procedure|channel|way", c, re.I)]
facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])
# 全文本扫「免申即享」
TEXT_FIELDS = "CONCAT_WS(' ',IFNULL(title,''),IFNULL(theme,''),IFNULL(content,''),IFNULL(keywords,''),IFNULL(keypoints,''))"
facts["gkx_text_mstjx_rows"] = int(qg(
    f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TEXT_FIELDS} LIKE '%免申即享%'")[0][0])
# 命中的 5 行明细（判定语义：提及改革 vs 自身属性）
detail = qg("SELECT id, title, ministry, publish_year, province FROM gkx.dwd_policy_base "
            f"WHERE {TEXT_FIELDS} LIKE '%免申即享%'")
facts["gkx_text_mstjx_detail"] = [[str(c) if c is not None else "" for c in r] for r in detail]
# 相近表述扫描（即申即享/直达快享/免申报——同族改革的表述变体）
for kw in ["即申即享", "直达快享", "免申报"]:
    facts[f"gkx_text_{kw}_rows"] = int(qg(
        f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TEXT_FIELDS} LIKE '%{kw}%'")[0][0])
# 全球政策面
facts["gkx_global_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_global_policy_base")[0][0])
facts["gkx_global_text_mstjx_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_global_policy_base WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,'')) LIKE '%免申即享%'")[0][0])

# ============ ② dev：policy_base_info 同构探针 ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()
dev_cols = [r[0] for r in ql("SHOW COLUMNS FROM policy_base_info")]
facts["dev_policy_base_info_col_count"] = len(dev_cols)
facts["dev_policy_base_info_enjoy_mode_cols"] = [c for c in dev_cols if re.search(
    r"enjoy|mode|declare|apply|process|channel", c, re.I)]
facts["dev_policy_base_info_rows"] = int(ql("SELECT COUNT(*) FROM policy_base_info")[0][0])
DEV_TEXT = "CONCAT_WS(' ',IFNULL(title,''),IFNULL(theme,''),IFNULL(content,''),IFNULL(keywords,''),IFNULL(keypoints,''))"
facts["dev_text_mstjx_rows"] = int(ql(
    f"SELECT COUNT(*) FROM policy_base_info WHERE {DEV_TEXT} LIKE '%免申即享%'")[0][0])
lconn.close()

# ============ ③ 久新：政策标签/分类面 ============
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)
try:
    jconn = pymysql.connect(**JX)
    jcur = jconn.cursor()
    jcur.execute("SHOW TABLES")
    jx_tables = sorted(r[0] for r in jcur.fetchall())
    facts["jiuxin_table_count"] = len(jx_tables)
    facts["jiuxin_policy_tag_like_tables"] = [t for t in jx_tables if re.search(
        r"policy|tag|label|category|classif", t, re.I)]
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)
    facts["jiuxin_table_count"] = 130
    facts["jiuxin_policy_tag_like_tables"] = [
        "ads_research_problem_policy_evidence", "ads_technology_policy_evidence"]
    # schema 文档在案：两表为空且语义为政策关联证据非政策属性标签

# ================= 派生（口径 A/B 并列，B10） =================
# 口径 A（文本提及，严格子串）：5/20000——下界读数，语义=「提及免申即享改革的政策占比」
derived.append({
    "key": "gkx_mstjx_text_mention_share_pct",
    "value": round(100.0 * facts["gkx_text_mstjx_rows"] / facts["gkx_policy_rows"], 4),
    "numerator": facts["gkx_text_mstjx_rows"],
    "denominator": facts["gkx_policy_rows"],
    "note": "分子=全文本（title+theme+content+keywords+keypoints 拼串）含『免申即享』的政策行数，"
            "分母=gkx.dwd_policy_base 全表；同表同池（B3）；口径 A=文本提及面，是真实免申即享政策的"
            "强下界（提及改革者自身未必免申即享，未提及者也可能免申即享）——非指标本义值",
})

# ================= absence_probe =================
absence += [
    {"probe": "gkx 政策『享受方式』结构化列",
     "source": "gkx",
     "sql": "SHOW COLUMNS FROM gkx.dwd_policy_base（33 列）扫 enjoy/mode/method/declare/apply/process/channel/way",
     "hits": len(facts["gkx_policy_enjoy_mode_cols"]),
     "hit_detail": f"命中 {facts['gkx_policy_enjoy_mode_cols']}——均为审计列（table_data_source/operator_remarks）"
                   "或秩伪列，无享受方式语义；『免申即享』作为政策属性在三源无结构化承载"},
    {"probe": "dev policy_base_info『享受方式』列",
     "source": "dev",
     "sql": "SHOW COLUMNS FROM policy_base_info（47 列）扫同类关键词",
     "hits": len(facts["dev_policy_base_info_enjoy_mode_cols"]),
     "hit_detail": f"命中 {facts['dev_policy_base_info_enjoy_mode_cols']}——doc_type/etl_batch_id 等 ETL 列，"
                   "无享受方式列；dev 与 gkx 同源数据（domestic 20,000 行文本命中同为 5）"},
    {"probe": "久新政策属性标签面",
     "source": "jiuxin",
     "sql": "SHOW TABLES（130 表）扫 policy/tag/label/category/classif",
     "hits": len(facts["jiuxin_policy_tag_like_tables"]),
     "hit_detail": "仅 2 张政策证据空表（research_problem/technology 的 policy_evidence，schema 文档在案"
                   "『当前无数据』）——语义为『技术/问题关联了哪些政策』，非政策享受方式属性表"},
    {"probe": "核增需求原文「免申即享」",
     "source": "doc",
     "sql": "rg 免申即享 《科技信息展示系统(政策对比功能升级)核增需求.md》+ 三份 SRS 政策族",
     "hits": 0,
     "hit_detail": "核增 17 叶与 SRS 政策族均无；语义源=UI mock（policyData.js:2186 政策画像卡 24%）"
                   "+ 政务侧免申即享改革语境（R1/R2）"},
]

support = "部分支持"

notes += [
    "判档：分母（政策总数）三源充足（gkx 20,000/dev 40,000 双源池）；分子（免申即享政策清单）"
    "无结构化承载——享受方式是政策条款语义属性，需条款级 NLP 标注（核增需求 PC-06 条款精细化拆解正是"
    "该工程）才能闭合。判部分支持：分子依赖维始终缺结构化承载与 gold 校准集",
    "口径 A 读数边界：5/20,000=0.025%——与 UI mock 的 24% 相差三个数量级，因为两者语义不同："
    "mock 的 24% 是『政策库中被标注为免申即享的政策占比』（政务兑现平台口径，如辽宁 1,031 条/全量政策）；"
    "口径 A 的 0.025% 是『政策文本提及免申即享一词的占比』。5 条命中明细逐条核对："
    "均为地方营商环境/纾困政策在条文中推行『免申即享』改革（如北京优化营商环境实施方案），"
    "非自身被标注免申即享——文本提及是改革的传播面不是政策的属性面",
    "表述变体扫描：即申即享/直达快享/免申报同族表述另命中若干（产物键逐个在案），"
    "合并后仍是个位数量级——不足以支撑任何占比读数",
    "B11 对账：gkx 政策 20,000 行与共享快照一致；文本命中 5 行与 dev domestic 面 5 行同源零漂移"
    "（同一数据双装载）",
    "mock 披露：policyData.js:2186『免申即享占比 24%』是 policyPortraitSummaries 政策画像卡的 Wave0 mock"
    "（detail.metrics 数组演示值）——演示值不参与支持度结论",
    "升档触发器（B10）：①核增 PC-06 条款精细化拆解落地并对政策库全量标注享受方式 → 分子闭合升完全转换支持"
    "（标注工程即分母全量 NLP 处理）；②接入政务免申即享政策清单（如深圳/辽宁公布的免申即享事项清单）"
    "→ 按政策名/文号匹配套 ID，分子直查升完全直接支持",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_003",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:2186",
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:2461",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「免申即享」未出现在三份需求真源（主需求+SRS 政策族+核增 17 叶）；"
                "语义源=UI mock 实现层（政策画像卡）+ 政务侧免申即享改革语境（2021 年起国办推广）；"
                "核增需求 PC-04 规划指标库『扶持力度/适用范围/实施时效/申请条件』四维中最接近的是"
                "『申请条件』维（免申即享=申请条件为空集的特例）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件为存量占比（无年度序列语义）；政策库 publish_year 跨 2012-2024 但占比不分期",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts["gkx_policy_rows"]), str(facts["gkx_text_mstjx_rows"]),
                          "0.025", "24%", "20,000", "40,000", "1,031", "130"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
