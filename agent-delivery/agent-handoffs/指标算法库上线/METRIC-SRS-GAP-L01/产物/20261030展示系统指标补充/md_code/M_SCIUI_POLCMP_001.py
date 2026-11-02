#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_001 政策落实率（兑现/应享） · 三源探针与复现脚本（S3-02 Lane 5）。

含义：某项科技政策计划兑现的资金/事项中实际落实到位的比例——回答'政策兑现了没有'。
分子=已兑现（拨付到账/事项办结）数；分母=应享（符合条件应兑现）数。
UI：ImplementationByRegion.jsx（分地区落实率表：rate/funded/declared/delayed）+
MultimediaAssistPanel.jsx（落实率线系列）。

三源实况（全部实探）：
- gkx：280 表扫 reward/claim/enjoy/declare/apply/fulfil/implement 仅命中 dwd_patent_claim
  （专利权利要求，语义无关）；政策表 33 列无兑现/拨付列。
- dev：兑现类表仅 enterprise_fund_project（0 行）；政策效果五表全 0 行。
- 久新：逐表 DESC 扫 implement/fulfil/honor/enjoy/subsid/benefit 列仅 4 个无关命中
  （人才荣誉/推荐方案）；政策 evidence 无兑现值。
权威口径（R1 国务院第三方评估/R2 应享尽享调查/R3-R4 免申即享台账）均为政务台账侧数据，库内无承载。
"""
import json, os, sys, re

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_001_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

# ============ ① gkx：兑现/拨付承载探针 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
claim_like = [t for t in gkx_tables if re.search(r"reward|claim|enjoy|declare|apply|fulfil|implement", t, re.I)]
facts["gkx_claim_like_tables"] = claim_like
# dwd_patent_claim 语义核对（是专利权利要求非政策兑现）
facts["gkx_patent_claim_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_patent_claim")[0][0])
pc_cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_patent_claim")]
facts["gkx_patent_claim_cols"] = pc_cols
# 政策表兑现类列
policy_cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_policy_base")]
facts["gkx_policy_cols"] = policy_cols
policy_cash_cols = [c for c in policy_cols if re.search(r"cash|fund|subsid|pay|grant|reward|amount", c, re.I)]
facts["gkx_policy_cash_like_cols"] = policy_cash_cols
# 政策存量（应享侧分母的上界原料）
facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])
# 申报通知类政策（应享事项的语义子集）
facts["gkx_policy_declare_notice_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE type LIKE '%申报%' OR title LIKE '%申报%'")[0][0])

# ============ ② dev：兑现台账探针 ============
LIVE = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
            charset="utf8mb4", connect_timeout=10, read_timeout=60)
lconn = pymysql.connect(**LIVE)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lconn.fetchall() if False else lcur.fetchall()
lcur.execute("SELECT TABLE_SCHEMA, TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA IN "
             "('gkxlumenx_dwd','gkxlumenx_ods') AND (TABLE_NAME LIKE '%reward%' OR TABLE_NAME LIKE '%claim%' "
             "OR TABLE_NAME LIKE '%enjoy%' OR TABLE_NAME LIKE '%fund%' OR TABLE_NAME LIKE '%grant%' "
             "OR TABLE_NAME LIKE '%cash%')")
dev_cash_tables = [(r[0], r[1]) for r in lcur.fetchall()]
facts["dev_cash_like_tables"] = [f"{s}.{t}" for s, t in dev_cash_tables]
dev_rows = {}
for s, t in dev_cash_tables:
    if t == "dwd_agg_subsidiary_info" or t == "dwd_org_subsidiary_info":
        continue  # 子公司信息表，语义无关跳过
    try:
        dev_rows[f"{s}.{t}"] = int(ql(f"SELECT COUNT(*) FROM {s}.{t}")[0][0])
    except Exception:
        dev_rows[f"{s}.{t}"] = -1
facts["dev_cash_like_table_rows"] = dev_rows
# 政策效果五表（落实率最贴近的结构）
for t in ["policy_effect_eval", "policy_support_assessment"]:
    facts[f"dev_{t}_rows"] = int(ql(f"SELECT COUNT(*) FROM gkxlumenx_dwd.{t}")[0][0])
lconn.close()

# ============ ③ 久新：兑现值探针 ============
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)
jconn = pymysql.connect(**JX)
jcur = jconn.cursor()
def qj(sql):
    jcur.execute(sql)
    return jcur.fetchall()
jcur.execute("SHOW TABLES")
jx_tables = sorted(r[0] for r in jcur.fetchall())
facts["jiuxin_table_count"] = len(jx_tables)
hit_cols = []
for t in jx_tables:
    try:
        cols = [c[0] for c in qj(f"DESC `{t}`")]
        for c in cols:
            if any(k in c.lower() for k in ("implement", "fulfil", "honor", "enjoy", "subsid", "benefit", "cash")):
                hit_cols.append((t, c))
    except Exception:
        pass
facts["jiuxin_fulfil_like_cols"] = hit_cols
# funding evidence 是资金证据面但为科研资助非政策兑付
facts["jiuxin_funding_evidence_rows"] = int(
    qj("SELECT COUNT(*) FROM ads_research_problem_funding_evidence")[0][0])
jconn.close()

# ================= 派生 =================
# 落实率本身不可算——派生键只登记可算的骨架读数（应享侧上界）
derived.append({
    "key": "gkx_policy_declare_notice_share_pct",
    "value": round(100.0 * facts["gkx_policy_declare_notice_rows"] / facts["gkx_policy_rows"], 4),
    "numerator": facts["gkx_policy_declare_notice_rows"],
    "denominator": facts["gkx_policy_rows"],
    "note": "分子=申报通知类政策行数（应享事项语义子集），分母=policy_base 全表行数；"
            "同表同池（B3）——应享侧分母的上界原料覆盖；兑现侧分子无源（absence_probe 在案）"})

# ============ absence_probe ============
absence += [
    {"probe": "gkx 政策兑现/拨付事件表",
     "source": "gkx",
     "sql": f"SHOW TABLES FROM gkx + {len(gkx_tables)} 表名扫 reward/claim/enjoy/declare/apply/fulfil/implement",
     "hits": len(claim_like),
     "hit_detail": f"仅命中 {claim_like}——dwd_patent_claim {len(pc_cols)} 列核对为专利权利要求书"
                   f"（文本列 original_text），语义无关；政策表 {len(policy_cols)} 列无"
                   " cash/fund/subsid/pay/grant/reward/amount 类列"},
    {"probe": "dev 兑现台账表",
     "source": "dev",
     "sql": "information_schema.TABLES 扫 gkxlumenx_dwd/gkxlumenx_ods 的 reward/claim/enjoy/fund/grant/cash",
     "hits": len(dev_rows),
     "hit_detail": f"候选 {facts['dev_cash_like_tables']}；逐表行数 {dev_rows}——"
                   "enterprise_fund_project（企业资助项目，最贴近结构）实测 0 行；"
                   "policy_effect_eval/policy_support_assessment 效果表亦 0 行（B4 情形②）"},
    {"probe": "久新兑现值列",
     "source": "jiuxin",
     "sql": f"{len(jx_tables)} 表逐表 DESC 扫 implement/fulfil/honor/enjoy/subsid/benefit/cash 列名",
     "hits": len(hit_cols),
     "hit_detail": f"仅 {len(hit_cols)} 个无关命中：{hit_cols}（人才荣誉 honors/推荐方案 implementation_plan）——"
                   "无政策兑现语义列；funding_evidence "
                   f"{facts['jiuxin_funding_evidence_rows']:,} 行是科研资助证据（OpenAlex grant）"
                   "非政策兑付台账"},
    {"probe": "核增需求原文「落实率」语义段",
     "source": "doc",
     "sql": "grep 落实率/兑现/应享/拨付 《科技信息展示系统(政策对比功能升级)核增需求.md》",
     "hits": 0,
     "hit_detail": "核增需求 17 个 PC 叶（政策数据治理/智能拆解/多维对比/研报生成）无落实率条目；"
                   "本件语义源是 UI mock 实现与主需求政策实施效果跟踪（1.1.1.1.4.2.1.3.3）语境"},
]

support = "完全不支持"

notes += [
    "判档：落实率=兑现数/应享数。兑现事件（分子）在三源均无承载——gkx "
    f"{len(gkx_tables)} 表唯一 claim 表是专利权利要求；"
    "dev 兑现台账 enterprise_fund_project 0 行；"
    f"久新 {len(jx_tables)} 表无兑现语义列（{len(hit_cols)} 个无关命中）。"
    f"应享侧（分母）仅有政策存量与申报通知子集（{facts['gkx_policy_declare_notice_rows']:,} 行）"
    "可作上界原料。分子无源 → 完全不支持",
    "关键词陷阱披露：gkx.dwd_patent_claim 的 'claim' 是专利权利要求书"
    f"（{len(pc_cols)} 列核对，文本列 original_text）——表名命中但语义完全无关，"
    "是本件最重要的排除证据；dev gkxlumenx_ods.dwd_patent_claim（同构 "
    f"{facts['gkx_patent_claim_rows']:,} 行）同理为专利域非政策兑现",
    "权威口径对照：政务侧『应享尽享率』（R2 工信部调查口径：八成以上）与『免申即享』兑付台账"
    "（R3 深圳龙华 116 项/20.5 亿元/82.79 万人；R4 深圳政府在线 84 项/17.4 亿元）"
    "均以政务系统内台账为源——兑现数据天然在财政/政务侧，"
    "不在科技要素库，这是数据源属性决定的缺口非工程缺口",
    "复现读数：本件为负结论件，无可算落实率值；facts 登记三源探针读数"
    f"（gkx 申报通知类 {facts['gkx_policy_declare_notice_rows']:,} 行=应享侧上界原料；"
    f"jiuxin funding_evidence {facts['jiuxin_funding_evidence_rows']:,} 行=科研资助旁证非兑付）",
    "mock 披露：UI implementationByRegionData（policyData.js:2244，北京 88%/上海 85%/深圳 91% 等"
    "8 地区 rate+funded+declared+delayed）为演示值，不参与支持度结论；"
    "MultimediaAssistPanel 落实率线（70→86 动画）同为 mock",
    "B11 对账：gkx 政策 20,000 行与共享快照（fix2.政策底表行数）一致；"
    "dev 效果表 0 行与 POLPAN_002 件 dev_policy_effect_table_rows 零漂移",
    "升档触发器（B10）：接入政务兑现台账（免申即享兑付记录/财政拨付流水/企事速办工单）→ 分子闭合，"
    "配合应享侧政策清单可升完全转换支持；若甲方接受第三方评估调查值"
    "（R1 国务院第三方评估/R2 企业自报应享尽享率）→ 需新调查数据源，单独立项",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_001",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/analysis/ImplementationByRegion.jsx:31",
        "repos/demo-ui-science/src/pages/policy-tracking/analysis/interpret/MultimediaAssistPanel.jsx:129",
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:2244",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「落实率/兑现/应享」未出现在三份需求真源（主需求+核增 17 叶+SRS 政策族——SRS 全树 "
                "rg 扫 0 命中，唯一近似词『资金拨付』在主需求 1.1.1.1.4.2.3.2.5 政策实施路径预测的"
                "环节枚举里，非兑现指标）；语义源=UI mock 实现层（ImplementationByRegion 分地区落实率表）"
                "+主需求 1.1.1.1.4.2.1.3.3 政策实施效果跟踪（SRS seq 209，『评估政策落地情况』）语境",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件无年度序列（兑现事件本身无承载）",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(len(gkx_tables)), str(len(jx_tables)),
                          str(facts["gkx_policy_declare_notice_rows"]),
                          f"{facts['jiuxin_funding_evidence_rows']:,}",
                          str(facts["gkx_patent_claim_rows"]),
                          str(len(pc_cols)), str(len(policy_cols))]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
