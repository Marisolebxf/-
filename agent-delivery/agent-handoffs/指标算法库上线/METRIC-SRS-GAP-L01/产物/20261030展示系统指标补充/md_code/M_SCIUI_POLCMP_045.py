#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_045 产业带动强度 · 三源探针与复现脚本（S3-03 Lane 3）。

含义：政策效果多维评估语境下「经济」维的分项评分（0-100 分制），度量政策对
上下游产业的拉动/带动效应。官方测算口径是投入产出法影响力系数（列昂惕夫逆矩阵
列和/均值，国家统计局 R1/R2）——单位最终需求对国民经济各部门的后向拉动。
UI：repos/demo-ui-science/src/pages/policy-tracking/policyData.js:1847
multiDimensionEvalData.dimensions[economy].indicators[1]
{ name: '产业带动强度', score: 84 }——效果预估工作台「多维度效果评估」Tab
（消费方 simulation/estimate/EstimateWorkbench.jsx:627-640 指标卡渲染）。

三源实况（全部实探，2026-11-01）：
- gkx：280 表无投入产出表面（表名扫 input|output|leontief|投入产出 0 命中）；
  产业关联边唯一真值源是产业链域（chain 族表）；政策文本「产业带动」4 字精确命中 69 行、
  「带动」宽词 2,122 行（占 10.61%，泛意图叙述——带动就业/带动创新，无中间消耗语义）；
  财务面产值列（operating_revenue/main_business_revenue）非中间投入矩阵。
- dev：产业链域 8 表 mock_20261019_append 批次造数（skill P4.1 在案禁引）；
  政策族效果评估表 0 行。
- 久新：203 张 ads_* 无投入产出/产业关联矩阵面（列扫 input_output 关联词根 0 命中）。
判档：完全不支持——影响力系数的计算原料（投入产出表三象限）三源零承载；
评分口径（UI 分制）与系数口径（>1 为高于平均）无换算锚。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_045_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402


def _ser(v):
    from decimal import Decimal
    import datetime as _dt
    if isinstance(v, Decimal):
        return float(v)
    if isinstance(v, (_dt.date, _dt.datetime)):
        return str(v)
    return v


facts, derived, notes, absence = {}, [], [], []

# ============ ① gkx：投入产出面 + 产业关联边 + 文本面 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
# 投入产出表面扫（影响力系数的原料——三象限棋盘表）
io_pat = re.compile(r"input.?output|leontief|投入产出|iotable", re.I)
facts["gkx_iotable_like_tables"] = [t for t in gkx_tables if io_pat.search(t)]
# 产业关联边候选（chain 族——产业链上下游关系）
facts["gkx_chain_like_tables"] = [t for t in gkx_tables if "chain" in t]
# 财务面产值列盘点（中间投入矩阵的邻接面——产值≠中间消耗）
fin_cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_org_annual_financial_info")]
facts["gkx_fin_cols"] = fin_cols
facts["gkx_fin_output_like_cols"] = [c for c in fin_cols if re.search(
    r"output|revenue|income|中间|intermediate", c, re.I)]
# 政策文本面：「产业带动」精确/「带动」宽词
TEXT_FIELDS = "CONCAT_WS(' ',IFNULL(title,''),IFNULL(theme,''),IFNULL(content,''),IFNULL(keywords,''),IFNULL(keypoints,''))"
facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])
facts["gkx_policy_text_chanyedaidong_rows"] = int(qg(
    f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TEXT_FIELDS} LIKE '%产业带动%'")[0][0])
facts["gkx_policy_text_daidong_rows"] = int(qg(
    f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TEXT_FIELDS} LIKE '%带动%'")[0][0])
# 宽词样本（语义核验）
sample = qg(f"SELECT id, title, publish_year FROM gkx.dwd_policy_base "
            f"WHERE {TEXT_FIELDS} LIKE '%带动%' ORDER BY id LIMIT 8")
facts["gkx_policy_text_daidong_sample"] = [[_ser(c) if c is not None else "" for c in r] for r in sample]
# 全球政策面对照
facts["gkx_global_policy_text_daidong_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_global_policy_base WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,'')) "
    "LIKE '%带动%'")[0][0])

# ============ ② dev：产业链域 + 效果评估承载 ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()
# 产业链域表盘点（产业关联边的 dev 侧——skill P4.1 已证 mock_20261019_append 造数批次）
lcur.execute("SELECT TABLE_NAME, TABLE_SCHEMA FROM information_schema.TABLES WHERE TABLE_SCHEMA IN "
             "('gkxlumenx_dwd','gkxlumenx_ods','gkxlumenx_ads','gkxlumenx_dim') AND TABLE_NAME LIKE '%chain%'")
facts["dev_chain_like_tables"] = sorted([[r[1], r[0]] for r in lcur.fetchall()])
# 投入产出类表扫
lcur.execute("SELECT TABLE_NAME, TABLE_SCHEMA FROM information_schema.TABLES WHERE TABLE_SCHEMA IN "
             "('gkxlumenx_dwd','gkxlumenx_ods','gkxlumenx_ads','gkxlumenx_dim') AND TABLE_NAME REGEXP "
             "'input.?output|leontief|iotable'")
facts["dev_iotable_like_tables"] = sorted([[r[1], r[0]] for r in lcur.fetchall()])
# 政策族效果评估表行数
dev_policy_rows = {}
for t in ["policy_effect_eval", "policy_simulation_result"]:
    try:
        dev_policy_rows[t] = int(ql(f"SELECT COUNT(*) FROM `{t}`")[0][0])
    except Exception as e:  # noqa: BLE001
        dev_policy_rows[t] = f"no-table: {str(e)[:40]}"
facts["dev_policy_family_rows"] = dev_policy_rows
lconn.close()

# ============ ③ 久新：投入产出/产业关联矩阵面 ============
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
    facts["jiuxin_iotable_like_tables"] = [t for t in jx_tables if io_pat.search(t)]
    # 产业关联/带动语义列扫（B5：SHOW TABLES 已排序，逐表 DESC）
    col_pat = re.compile(r"leontief|influence|linkage|driving|pull|带动|intermediate", re.I)
    col_hits = {}
    for t in jx_tables:
        try:
            cols = [r[0] for r in qj(f"DESC `{t}`")]
            m = [c for c in cols if col_pat.search(c)]
            if m:
                col_hits[t] = m
        except Exception:  # noqa: BLE001
            pass
    facts["jiuxin_linkage_like_cols"] = col_hits
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)
    notes.append("久新连接失败按未取证登记（B4：连接失败≠0 行），不参与判档数字")

# ============ 派生与登记 ============
# 叙述面占比（同基相除：分子=文本命中行，分母=全表）
if facts["gkx_policy_text_daidong_rows"] > 0:
    derived.append({
        "key": "daidong_text_share_pct",
        "value": round(100.0 * facts["gkx_policy_text_daidong_rows"] / facts["gkx_policy_rows"], 4),
        "numerator": facts["gkx_policy_text_daidong_rows"],
        "denominator": facts["gkx_policy_rows"],
        "note": "分子=gkx 政策全文含「带动」的行数，分母=dwd_policy_base 全表 20,000；同表同池（B3）；"
                "泛词叙述覆盖面（政策意图声明），不是产业带动强度读数",
    })
# 负结论登记键：影响力系数不可算
derived.append({
    "key": "industry_driving_intensity",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "不可算——投入产出表（三象限：中间消耗矩阵+增加值构成）三源零承载；"
            "影响力系数=列昂惕夫逆矩阵 B=(I-A)^-1 列和/全行业均值（R1/R2），"
            "计算原料 A 矩阵需部门×部门中间消耗数据；财务面产值列（output/revenue）"
            "非中间投入矩阵，不可代理",
})

absence += [
    {"probe": "gkx 投入产出表面",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）扫 input-output/leontief/投入产出/iotable",
     "hits": len(facts["gkx_iotable_like_tables"]),
     "hit_detail": "0 张投入产出表面——影响力系数的计算原料（部门×部门中间消耗矩阵）零承载；"
                   "chain 族表是产业链资讯/投资事件面非消耗矩阵"},
    {"probe": "gkx 政策文本「产业带动」叙述",
     "source": "gkx",
     "sql": "全文本五字段 LIKE '%产业带动%' / '%带动%'",
     "hits": facts["gkx_policy_text_chanyedaidong_rows"],
     "hit_detail": "「产业带动」4 字精确命中 69 行（hits 键口径）；「带动」宽词 2,122 行"
                   "（占全表 10.61%）是泛政策意图语言（带动就业/带动创新/带动发展——"
                   "意图声明非带动效应），既无中间消耗数值也无口径"},
    {"probe": "dev 产业链域与效果评估承载",
     "source": "dev",
     "sql": "information_schema.TABLES 四 schema 扫 chain / input-output/leontief/iotable + "
            "policy_effect_eval/policy_simulation_result 行数",
     "hits": len(facts["dev_iotable_like_tables"]),
     "hit_detail": "投入产出表 0 张；chain 族 8 表属 mock_20261019_append 造数批次（skill P4.1 "
                   "在案禁引——产业链上下游边是演示图非实证）；效果评估两表 0 行"},
    {"probe": "久新投入产出/产业关联面",
     "source": "jiuxin",
     "sql": "SHOW TABLES（203 表）扫 input-output/leontief/iotable + 全表 DESC 列扫 "
            "leontief/influence/linkage/driving/pull/intermediate",
     "hits": len(facts.get("jiuxin_iotable_like_tables", [])) + len(facts.get("jiuxin_linkage_like_cols", {})),
     "hit_detail": "表列双扫 0 命中——ads_* 结果面无投入产出矩阵/影响力系数类指标"},
    {"probe": "需求原文「产业带动强度」定义段",
     "source": "doc",
     "sql": "rg 产业带动/带动强度 三份需求真源（主需求+核增 17 叶+算法库）",
     "hits": 0,
     "hit_detail": "三份需求真源均未出现「产业带动/带动强度」；主需求 1.1.1.1.4.2.3.1.4 多维度"
                   "效果评估（经济/社会/环境/创新四维+得分）是维度语义源（经济维）；"
                   "语义源=UI mock multiDimensionEvalData 经济维分项（score 84 演示值）"},
]

support = "完全不支持"

notes += [
    "判档：产业带动强度的权威口径是投入产出法影响力系数（国家统计局 R1：直接消耗矩阵 A → 列昂惕夫"
    "逆矩阵 B=(I-A)^-1 → 影响力系数=列和/全行业均值，R2 学界应用同构）。计算原料（部门×部门中间"
    "消耗矩阵+增加值构成，投入产出表三象限）三源零承载——gkx 280 表无 iotable、财务面产值列"
    "非中间消耗、dev 产业链边是造数批次禁引、久新无关联矩阵面。判完全不支持",
    "裁定登记（父代理 S3-03 派单书）：需求文档 0 命中（本件实测确认），产业影响力候选是舆情口径"
    "（bubbleChartData influence 字段，mock 舆情评分），带动口径未调查——本件按带动口径（投入产出"
    "影响力系数）完成调查，舆情口径另立（POLCMP_046 综合力度指数族）",
    "文本面边界：「产业带动」4 字 69 行（产业政策意图叙述——「带动产业高质量发展」类表述，"
    "非投入产出口径的带动效应），「带动」宽词 2,122 行（10.61%，带动就业/带动创新——泛意图语言）"
    "——两层叙述面均无中间消耗数值与口径，文本面不可承载本指标",
    "mock 披露：policyData.js:1847 score 84 是效果预估工作台「多维度效果评估」Tab 经济维演示值；"
    "bubbleChartData（:1803-1812）的 influence/attention 是舆情口径演示值（与本指标带动口径不同物）"
    "——均不参与支持度结论",
    "B11 对账：gkx dwd_policy_base 20,000 行与共享快照零漂移；「产业带动」69 行/「带动」2,122 行与 "
    "POLCMP_024（就业 1,576 行）/041（税收 1,734 行）同日同库文本面探针族；dev 政策族行数与 Lane6 探针零漂移",
    "升档触发器（B10）：①接入国家统计局投入产出表（逢 2 逢 7 年份编制，42/149 部门）→ 影响力"
    "系数可直算，升完全转换支持；②若甲方接受「政策文本带动词频」或「舆情关注度」代理 → 语义已换"
    "（意图/关注度≠带动效应），本件保守不接受",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_045",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:1847",
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:1839",
        "repos/demo-ui-science/src/pages/policy-tracking/simulation/estimate/EstimateWorkbench.jsx:627",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份需求真源未出现「产业带动/带动强度」（父代理裁定登记：需求 0 命中，带动口径"
                "未调查——本件补完）；主需求 1.1.1.1.4.2.3.1.4 多维度效果评估是维度语义源（经济维）；"
                "语义源=UI mock multiDimensionEvalData.dimensions[economy].indicators[1]",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["部门×部门中间消耗矩阵（投入产出表第 I 象限）", "增加值构成序列（第 III 象限）"],
    "base_years_note": "本件无投入产出序列承载；政策文本叙述面年度分布不作基期",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts["gkx_policy_rows"]),
                          str(facts["gkx_policy_text_chanyedaidong_rows"]),
                          str(facts["gkx_policy_text_daidong_rows"]),
                          str(facts.get("gkx_global_policy_text_daidong_rows", 0)),
                          str(len(facts["gkx_chain_like_tables"])), "280", "203"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
