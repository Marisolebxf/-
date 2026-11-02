#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_055 企业创新积分（积分制评价） · 三源探针与登记脚本（S3-03 Lane 4）。

含义：科技政策跟踪·政策知识图谱（PC-05 智能政策拆解）语境下，政策关系图谱的实体节点——
「创新积分」（category 关联政策，policyPcData.js:490 entities e3；:450 summary 明列
「强化创新积分、政府采购与产业链配套」）。export l3 挂「首台套保险补贴＞创新积分」，
mean 自认「评判框架需要立项调研后才能确定」（裁定 NEW：需求文档 0 命中，积分制口径全新）。
权威锚：科技部火炬中心《企业创新积分制工作指引 1.0》（R1，2022）与《创新积分制工作
指引（全国试行版）》（R2，2024，gov.cn）——3 类一级 18 个二级指标，分初创/成长/稳定
三期权重，百分制。

三源实况（全部实探，2026-11-01）：
- 企业创新积分结果面：三源零承载——gkx 280 表扫 credit/score/point/quant 0 语义命中；
  dev 62 张 enterprise 族中 enterprise_score/enterprise_ranking 等评分表属已禁引造数面
  （批次 svcmodels_*，skill P4.1 在案）；无「创新积分」结果表。
- 积分输入维（18 指标映射）：火炬 18 指标中研发费用/营收/研发强度/科技人员占比等
  财务与人员维三源无企业级结构化承载（gkx 无企业财务表；dev enterprise_forg_finance_history
  仅海外样本 51 行；recruit 1,000 行样例级）；专利维有量（gkx dwd_patent 2,939,895——
  但「与主营业务相关」过滤维无承载）。
- 久新：210 张 ads_* 扫 enterprise/score/point/credit 0 命中（无企业面）。
判档：完全不支持（积分制评价框架未立项 + 结果面零承载 + 18 指标输入维多数无企业级
结构化数据——财务/人员/主营业务关联维全缺，专利维可部分映射但「与主营业务相关」
过滤不可实现）。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_055_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []


def _ser(v):
    from decimal import Decimal
    import datetime as _dt
    if isinstance(v, Decimal):
        return float(v)
    if isinstance(v, (_dt.date, _dt.datetime)):
        return str(v)
    return v


# ============ ① gkx：企业创新积分结果面 + 输入维盘点 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
# 积分/评分类表名扫
facts["gkx_score_point_tables_raw"] = [t for t in gkx_tables if re.search(
    r"score|point|credit|quant|rating|grade", t, re.I)]
# 企业面盘点（gkx 是否有企业主体/财务/人员表）
facts["gkx_enterprise_like_tables"] = [t for t in gkx_tables if re.search(
    r"enterprise|company|firm|org_base|org_fund", t, re.I)]
# 专利维（18 指标中发明专利/PCT 两维的原料——与主营业务相关性过滤不可行的证据）
facts["gkx_patent_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_patent")[0][0])
# 政策文本「创新积分」叙述面（政策提及该工具的证据）
TF = ("CONCAT_WS(' ',IFNULL(title,''),IFNULL(theme,''),IFNULL(content,''),"
      "IFNULL(keywords,''),IFNULL(keypoints,''))")
facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])
facts["gkx_text_cxjf_rows"] = int(qg(
    f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TF} LIKE '%创新积分%'")[0][0])
facts["gkx_text_jfz_rows"] = int(qg(
    f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TF} LIKE '%积分制%'")[0][0])
rows = qg(f"SELECT id, title, publish_year FROM gkx.dwd_policy_base "
          f"WHERE {TF} LIKE '%创新积分%' OR title LIKE '%积分制%' LIMIT 8")
facts["gkx_text_cxjf_sample"] = [[_ser(c) if c is not None else "" for c in r] for r in rows]
# 全球面对照
facts["gkx_global_text_cxjf_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_global_policy_base WHERE CONCAT_WS(' ',"
    "IFNULL(title,''),IFNULL(content,'')) LIKE '%创新积分%'")[0][0])
gcur.close()

# ============ ② dev：企业评分面甄别 + 18 指标输入维映射 ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
# 企业底册与输入维候选（真实面）
for t, key in [("enterprise_base", "dev_enterprise_base_rows"),
               ("enterprise_extra", "dev_enterprise_extra_rows"),
               ("enterprise_forg_finance_history", "dev_enterprise_forg_finance_history_rows"),
               ("enterprise_recruit", "dev_enterprise_recruit_rows"),
               ("enterprise_financing", "dev_enterprise_financing_rows"),
               ("enterprise_patent_org_rel", "dev_enterprise_patent_org_rel_rows"),
               ("enterprise_qualification_matrix", "dev_enterprise_qualification_matrix_rows"),
               ("enterprise_year_stat", "dev_enterprise_year_stat_rows")]:
    try:
        lcur.execute(f"SELECT COUNT(*) FROM {t}")
        facts[key] = int(lcur.fetchone()[0])
    except Exception as e:  # noqa: BLE001
        facts[key] = f"no-table: {str(e)[:50]}"
# 评分/排名面（禁引甄别——skill P4.1 造数清单）
lcur.execute("SELECT COUNT(*) FROM gkxlumenx_ads.enterprise_score")
facts["dev_ads_enterprise_score_rows"] = int(lcur.fetchone()[0])
lcur.execute("SHOW COLUMNS FROM gkxlumenx_ads.enterprise_score")
facts["dev_ads_enterprise_score_cols"] = [r[0] for r in lcur.fetchall()]
# 财务面列级（研发费用/营收承载候选——18 指标核心输入）
lcur.execute("SHOW COLUMNS FROM enterprise_forg_finance_history")
facts["dev_forg_finance_cols"] = [r[0] for r in lcur.fetchall()]
lconn.close()

# ============ ③ 久新：企业创新积分面 ============
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
    facts["jiuxin_enterprise_tables"] = [t for t in jx_tables if re.search(
        r"enterprise|company|firm", t, re.I)]
    facts["jiuxin_score_point_tables"] = [t for t in jx_tables if re.search(
        r"score|point|credit|innovation", t, re.I)]
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)[:120]

# ============ 派生与登记 ============
# 叙述面派生比（同基相除：分子=「创新积分」命中行，分母=gkx 政策全表）
derived.append({
    "key": "cxjf_mention_share_pct",
    "value": round(facts["gkx_text_cxjf_rows"] / facts["gkx_policy_rows"] * 100, 3),
    "numerator": facts["gkx_text_cxjf_rows"],
    "denominator": facts["gkx_policy_rows"],
    "note": "「创新积分」叙述面占 gkx 政策全表比（工具提及度指示器，非积分评价承载）",
})
# 负结论登记键
derived.append({
    "key": "enterprise_innovation_score",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "不可算——积分制评价框架未立项（裁定 NEW）+ 结果面零承载 + 18 指标输入维"
            "（研发费用/营收/研发强度/科技人员占比/主营业务相关专利等）无企业级结构化"
            "数据；dev enterprise_score 等评分表属禁引造数面（skill P4.1 批次甄别在案）",
})

absence = [
    {"probe": "gkx 积分/评分类表",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）扫 score/point/credit/quant/rating/grade + "
            "企业主体/财务表",
     "hits": 0,
     "hit_detail": "无企业创新积分结果表；企业面仅 org 族底册（dwd_org_base_info 等），"
                   "无企业级研发费用/营收/人员结构化表（18 指标核心输入无承载）"},
    {"probe": "dev 评分面甄别与输入维",
     "source": "dev",
     "sql": "COUNT：enterprise_base/extra/forg_finance_history/recruit/patent_org_rel + "
            "gkxlumenx_ads.enterprise_score（禁引甄别）",
     "hits": 0,
     "hit_detail": "企业底册 enterprise_base 269,511 行真实；但财务面 forg_finance_history "
                   "仅 51 行（海外样本）、recruit 1,000 行（样例级）；ads.enterprise_score "
                   "等评分表属 svcmodels_* 造数批次（skill P4.1 禁引清单），不得作积分"
                   "承载——真实输入维不足以跑 18 指标模型"},
    {"probe": "久新企业/积分面",
     "source": "jiuxin",
     "sql": "SHOW TABLES（实测 210 张，探测日 2026-11-01）扫 enterprise/company/firm/"
            "score/point/credit/innovation",
     "hits": 0,
     "hit_detail": "enterprise/company/firm 词根 0 命中（久新无企业面）；score/point/"
                   "credit 词根 0 命中；innovation 词根 0 命中——分析仓是企业缺位的"
                   "人才/技术/文献面"},
    {"probe": "需求文档定义",
     "source": "doc",
     "sql": "rg 创新积分/积分制 主需求 + SRS 政策族四文件 + 核增 17 叶",
     "hits": 0,
     "hit_detail": "三份需求真源 0 命中（父代理裁定 NEW：积分制口径全新）；UI "
                   "policyPcData.js:490 图谱实体节点 e3「创新积分」（关联政策类目）与 "
                   ":450 summary 是唯一实证——实体节点是图谱展示位非积分评价定义；"
                   "export mean 自认评判框架需立项调研；候选「学术合作评分」不同物"},
]

support = "完全不支持"

notes = [
    "判档：三层缺叠加——①评价框架未立项（裁定 NEW，火炬 18 指标体系是权威参照但甲方"
    "未裁定量纲/权重/分期）；②结果面零承载（三源无企业创新积分表；dev ads.enterprise_score "
    "属 svcmodels_* 造数批次禁引，skill P4.1 在案——innovation_score 与真实专利数 r=-0.0532 "
    "无关的硬实证）；③输入维不足（火炬 18 指标中研发费用/营收/研发强度/科技人员占比/"
    "高新产品收入/研究生占比/加计扣除减免额等财务人员维无企业级结构化数据：gkx 无企业"
    "财务表、dev forg_finance_history 仅 51 行海外样本）",
    "18 指标映射盘点（火炬指引 R1/R2）：技术创新 7 项中仅专利 2 项（发明专利/PCT）有"
    "原料（gkx dwd_patent 2,939,895 行）——但「与主营业务相关」过滤维无承载（专利表"
    "无企业主营业务关联字段），技术合同成交额 1 项部分可探（gkx 有 contract 类表需另"
    "核）；成长经营 6 项全缺（财务维）；辅助 5 项中融资额 1 项有量（dwd_org_financing_info "
    "25,654 行/enterprise_financing 25,654 行）、应届毕业生与平台/奖励/项目 4 项缺。"
    "可映射指标约 3/18，权重合计不足 20%——即便框架立项，输入面也撑不起积分模型",
    "政策文本叙述面：「创新积分」全文命中 2 行、「积分制」20 行（title 层 1 行）——"
    "提及度极低（0.01%），且均为提及面非条款量化面；全球面「创新积分」0 命中（域外无"
    "此政策工具，与 POLCMP_009 加计扣除全球面 0 命中同型）",
    "UI mock 披露：policyPcData.js:490 实体节点 { id: 'e3', name: '创新积分', category: "
    "'关联政策' } 与 :450 summary「强化创新积分、政府采购与产业链配套」是 PC 端图谱"
    "演示数据（演示值不参与支持度结论）——图谱把「创新积分」画成政策关联实体（一条边"
    "的目标节点），不是积分评价功能的展示位；export l3「首台套保险补贴＞创新积分」"
    "层级是拆件归属误差（首台套是同政策另一条款），登记不改判",
    "升档触发器（B10）：①甲方裁定采用火炬 18 指标框架（或其子集）+ 企业级财务/人员"
    "数据源接入（税务/统计/工商年报外部源）→ 输入维闭合后升完全转换支持；②若接受"
    "「专利+融资」双维降维积分（约 3/18 指标，权重不足 20%）→ 语义降为「创新活跃度"
    "代理分」，须更名交付并披露降维；③政务侧积分制平台数据（火炬中心全国企业创新积分"
    "管理平台）对接是最准路径，单独立项",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_055",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/policyPcData.js:490",
        "repos/demo-ui-science/src/pages/policy-tracking/policyPcData.js:450",
        "repos/demo-ui-science/src/pages/policy-tracking/PolicyPcPages.jsx:578",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份需求真源 0 命中（裁定 NEW：积分制口径全新，候选学术合作评分不同物）；"
                "UI 图谱实体节点 e3（关联政策类目）是唯一实证；export 自认评判框架需"
                "立项调研",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "积分评价无年度序列（框架未立项、结果面零承载）",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts.get("gkx_text_cxjf_rows", "")),
                          str(facts.get("gkx_text_jfz_rows", "")),
                          str(facts.get("gkx_patent_rows", "")),
                          str(facts.get("jiuxin_table_count", "")),
                          "18", "3"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", OUT)
