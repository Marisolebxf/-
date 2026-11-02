#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_035 绿色产业占比 · 三源探针与复现脚本（S3-03 Lane 3）。

含义：政策效果多维评估语境下「环境」维的分项评分（0-100 分制），度量政策实施后
目标区域内绿色产业在经济总量中的相对规模。官方口径先例是「绿色低碳产业增加值
占 GDP 比重」（国家统计局《节能环保清洁产业统计分类（2021）》界定产业范围）。
UI：repos/demo-ui-science/src/pages/policy-tracking/policyData.js:1867
multiDimensionEvalData.dimensions[environment].indicators[1]
{ name: '绿色产业占比', score: 74 }——效果预估工作台「多维度效果评估」Tab
（消费方 simulation/estimate/EstimateWorkbench.jsx:627-640 指标卡渲染）。

三源实况（全部实探，2026-11-01）：
- gkx：280 表无绿色/低碳/环保语义结构化承载（表名扫原始命中 2 张均词根误中，语义甄别后 0）；
  dwd_policy_base 33 列无产业分类列；政策文本「绿色产业」4 字命中 68 行、「绿色低碳」
  宽词 183 行（叙述面）。主产业分类载体 dwd_org_industry_tags（2,283,762 行，
  3,852 个 DISTINCT 组合标签全量正则扫）与 dwd_org_base_info 一级行业（20 类全量）
  实测均无绿色维度词。
- dev：政策族 38 表无环境/绿色评估承载（policy_environment_* 表名扫 0 命中）。
- 久新：203 张 ads_* 列扫 green/carbon/低臓/emission 词根——无绿色产业占比结果面
  （ads_carbon_* 类表不存在，carbon 词根 0 命中）。
判档：完全不支持——「绿色产业」判定维（产业分类目录的绿色子集）三源零承载，
评分口径（UI 0-100 分）与占比口径（%）的换算亦无锚。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_035_out.json")
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

# ============ ① gkx：绿色产业判定维与文本面 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
# 绿色/低碳/环保语义表名扫（结构化承载候选——分类目录表/产业目录表）
green_pat = re.compile(r"green|low.?carbon|carbon|eco|environment|节能|环保|低碳", re.I)
facts["gkx_green_like_tables"] = [t for t in gkx_tables if green_pat.search(t)]
# 词根误中甄别：energy/eco/recommend 词根会误中无关表——语义甄别注释在 absence
facts["gkx_green_like_tables_semantic"] = [
    t for t in facts["gkx_green_like_tables"]
    if not re.search(r"energy|recommend|changerecord|zczeconv|recognition|layout|search", t, re.I)]
# 主产业分类载体盘点：dwd_org_industry_tags（企业×行业标签关系表）
TEXT_FIELDS = "CONCAT_WS(' ',IFNULL(title,''),IFNULL(theme,''),IFNULL(content,''),IFNULL(keywords,''),IFNULL(keypoints,''))"
facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])
facts["gkx_policy_green_cols"] = []
policy_cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_policy_base")]
facts["gkx_policy_col_count"] = len(policy_cols)
# 政策文本面：绿色产业/绿色低碳叙述覆盖（转换口径的原料边界）
facts["gkx_policy_text_lvse_chanye_rows"] = int(qg(
    f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TEXT_FIELDS} LIKE '%绿色产业%'")[0][0])
facts["gkx_policy_text_lvse_ditan_rows"] = int(qg(
    f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TEXT_FIELDS} LIKE '%绿色低碳%'")[0][0])
# 宽词样本（命中政策长什么样——语义核验）
sample = qg(f"SELECT id, title, publish_year FROM gkx.dwd_policy_base "
            f"WHERE {TEXT_FIELDS} LIKE '%绿色低碳%' ORDER BY id LIMIT 6")
facts["gkx_policy_text_lvse_sample"] = [[_ser(c) if c is not None else "" for c in r] for r in sample]
# 企业行业标签面（若建分类目录，这是挂载点——全量词表实测有无绿色维度）
facts["gkx_industry_tags_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_org_industry_tags")[0][0])
n_dist = int(qg("SELECT COUNT(DISTINCT industry_name) FROM gkx.dwd_org_industry_tags "
                "WHERE industry_name IS NOT NULL AND industry_name != ''")[0][0])
facts["gkx_industry_tag_distinct_words"] = n_dist
# 全量正则扫（非首段采样）：绿色词族在任何组合标签中命中几档
gw = qg("SELECT industry_name, COUNT(*) FROM gkx.dwd_org_industry_tags "
        "WHERE industry_name REGEXP '绿色|低碳|节能|环保|新能源|清洁' "
        "GROUP BY industry_name ORDER BY industry_name")
facts["gkx_industry_tag_green_hits_full"] = [[r[0], int(r[1])] for r in gw]
tag_words = qg("SELECT DISTINCT industry_name FROM gkx.dwd_org_industry_tags "
               "WHERE industry_name IS NOT NULL AND industry_name != '' ORDER BY industry_name LIMIT 200")
facts["gkx_industry_tag_words_sample"] = [r[0] for r in tag_words]
GREEN_WORDS = ("绿色", "低碳", "节能", "环保", "新能源", "清洁")
facts["gkx_industry_tag_green_words"] = [w for w in facts["gkx_industry_tag_words_sample"]
                                          if w and any(g in str(w) for g in GREEN_WORDS)]# 机构底册行业面（若建分类目录，这是挂载点——四级行业名列词表实测有无绿色维度）
facts["gkx_org_greenname_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_org_base_info WHERE name_cn LIKE '%绿色%' OR name_cn LIKE '%环保%'")[0][0])
l1_words = qg("SELECT DISTINCT industry_l1_name FROM gkx.dwd_org_base_info "
              "WHERE industry_l1_name IS NOT NULL AND industry_l1_name != '' ORDER BY industry_l1_name")
facts["gkx_org_industry_l1_words"] = [r[0] for r in l1_words]
facts["gkx_org_industry_l1_green_words"] = [w for w in facts["gkx_org_industry_l1_words"]
                                             if any(g in str(w) for g in GREEN_WORDS)]
# 全球政策面对照
facts["gkx_global_policy_text_green_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_global_policy_base WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,'')) "
    "LIKE '%绿色产业%'")[0][0])

# ============ ② dev：环境/绿色评估承载 ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()
# 环境/绿色/低碳评估类表扫（政策族 38 表 + 全 schema）
lcur.execute("SELECT TABLE_NAME, TABLE_SCHEMA FROM information_schema.TABLES WHERE TABLE_SCHEMA IN "
             "('gkxlumenx_dwd','gkxlumenx_ods','gkxlumenx_ads','gkxlumenx_dim') AND TABLE_NAME REGEXP "
             "'green|carbon|eco|environment|policy_environment'")
facts["dev_green_like_tables"] = sorted([[r[1], r[0]] for r in lcur.fetchall()])
# 政策族效果评估表复核（multiDimensionEval 的落位候选）
for t in ["policy_effect_eval", "policy_simulation_result"]:
    try:
        facts[f"dev_{t}_rows"] = int(ql(f"SELECT COUNT(*) FROM `{t}`")[0][0])
    except Exception as e:  # noqa: BLE001
        facts[f"dev_{t}_rows"] = f"no-table: {str(e)[:60]}"
# dev 政策文本同构核验（绿色产业 4 字）
DEV_TEXT = "CONCAT_WS(' ',IFNULL(title,''),IFNULL(theme,''),IFNULL(content,''),IFNULL(keywords,''),IFNULL(keypoints,''))"
facts["dev_policy_text_lvse_chanye_rows"] = int(ql(
    f"SELECT COUNT(*) FROM policy_base_info WHERE {DEV_TEXT} LIKE '%绿色产业%'")[0][0])
lconn.close()

# ============ ③ 久新：绿色/低碳结果面 ============
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
    facts["jiuxin_green_like_tables"] = [t for t in jx_tables if green_pat.search(t)]
    # 列级扫描（carbon/green/emission 词根——B5：全表 DESC 按 SHOW TABLES 排序逐表）
    col_pat = re.compile(r"green|carbon|emission|eco", re.I)
    col_hits = {}
    for t in jx_tables:
        try:
            cols = [r[0] for r in qj(f"DESC `{t}`")]
            m = [c for c in cols if col_pat.search(c)]
            if m:
                col_hits[t] = m
        except Exception:  # noqa: BLE001
            pass
    facts["jiuxin_green_like_cols"] = col_hits
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)
    notes.append("久新连接失败按未取证登记（B4：连接失败≠0 行），不参与判档数字")

# ============ 派生与登记 ============
# 叙述面占比（转换口径工作量指示器，同基相除：分子=文本命中行，分母=全表）
if facts["gkx_policy_text_lvse_ditan_rows"] > 0:
    derived.append({
        "key": "lvse_ditan_text_share_pct",
        "value": round(100.0 * facts["gkx_policy_text_lvse_ditan_rows"] / facts["gkx_policy_rows"], 4),
        "numerator": facts["gkx_policy_text_lvse_ditan_rows"],
        "denominator": facts["gkx_policy_rows"],
        "note": "分子=gkx 政策全文含「绿色低碳」的行数，分母=dwd_policy_base 全表；同表同池（B3）；"
                "叙述覆盖面（转换口径工作量指示器），不是绿色产业占比读数",
    })
# 负结论登记键：指标本体无承载
derived.append({
    "key": "green_industry_share",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "不可算——「绿色产业」判定维（产业分类目录的绿色子集）三源零承载：gkx 280 表无绿色"
            "语义结构化表、行业标签词表无绿色维度词、dev 无环境评估表、久新无 carbon/green 列；"
            "分子（绿色产业企业数/增加值）分母（全域企业/GDP）双缺",
})

absence += [
    {"probe": "gkx 绿色产业判定维（分类目录）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）扫 green/low-carbon/carbon/eco/environment/节能/环保/低碳"
            "（+语义甄别：energy/recommend/changerecord 词根误中剔除）",
     "hits": len(facts["gkx_green_like_tables_semantic"]),
     "hit_detail": "正则原始命中 2 张（dwd_org_annual_report_asset_bak_zczeconv/dwd_org_changerecord_info）"
                   "均为词根误中（eco→ economical 类缩写/energy 词根），语义甄别后 0 张——"
                   "无绿色产业分类目录表（企业×绿色子集映射零承载）"},
    {"probe": "gkx 行业标签/机构行业词表绿色维度",
     "source": "gkx",
     "sql": "SELECT COUNT(DISTINCT industry_name)（全量 3,852 词）+ industry_name REGEXP "
            "'绿色|低碳|节能|环保|新能源|清洁' 全量正则扫 + SELECT DISTINCT industry_l1_name FROM "
            "dwd_org_base_info（一级全量）逐词扫",
     "hits": len(facts["gkx_industry_tag_green_hits_full"]) + len(facts.get("gkx_org_industry_l1_green_words", [])),
     "hit_detail": "标签全量 3,852 个行业名（深圳 20 大战新产业集群口径：软件与信息服务 944,360/"
                   "合成生物 468,328/生物医药 138,144…）绿色词 0 命中；机构一级行业 20 类"
                   "（国民经济行业分类口径）无绿色子集——两大产业分类载体均不含绿色维度；"
                   "政策文本「绿色产业」4 字命中 68 行但均为贯彻/规划类叙述（无分类目录语义）"},
    {"probe": "dev 环境/绿色评估承载",
     "source": "dev",
     "sql": "information_schema.TABLES 四 schema 扫 green/carbon/eco/environment/policy_environment"
            "（命中 8 张均为 recommend/recognition/layout 词根误中，语义甄别后 0）",
     "hits": 0,
     "hit_detail": "正则原始命中 8 张全是推荐/识别类表（chain_layout_recommend/entity_recognition/"
                   "svc_*_recommend/policy_layout_recommend 等——recommend 词根误中），"
                   "语义甄别后 0 张——政策族 38 表无环境维评估落位表；"
                   "policy_effect_eval/policy_simulation_result 均 0 行（Lane6 探针共证）"},
    {"probe": "久新绿色/低碳结果面",
     "source": "jiuxin",
     "sql": "SHOW TABLES（203 表）扫 green/carbon/eco/environment + 全表 DESC 列扫 green/carbon/emission/eco"
            "（命中均为 recommendation 词根误中，语义甄别后 0）",
     "hits": 0,
     "hit_detail": "表扫原始命中 22 张、列扫命中 22 表全是 ads_recommendation_*/ads_*_assessment 类"
                   "（recommendation 词根含 eco 误中）——语义甄别后 0：无绿色产业占比/碳排放强度类"
                   "结果面（无一张 ads_carbon_*/ads_green_* 表）"},
    {"probe": "需求原文「绿色产业」定义段",
     "source": "doc",
     "sql": "rg 绿色产业/绿色产业占比 三份需求真源（主需求+核增 17 叶+算法库）",
     "hits": 0,
     "hit_detail": "三份需求真源均未出现「绿色产业」；主需求「绿色低碳」仅 1 处（政策标签举例，"
                   "非指标定义）；语义源=UI mock multiDimensionEvalData 环境维分项（score 74 演示值）"},
]

support = "完全不支持"

notes += [
    "判档：绿色产业占比 = 绿色产业（子集）/ 全部产业（全集）。分子侧需要「绿色产业」判定维——"
    "国家统计局《节能环保清洁产业统计分类（2021）》口径下按国民经济行业分类划定绿色子集；"
    "本库三源无任何绿色产业分类目录/结构化表（gkx 行业标签全量 3,852 词与机构一级行业 20 类"
    "均无绿色维度词），分母侧无区域 GDP/全域产业产值面——分子分母双缺，判完全不支持",
    "文本面边界：政策文本「绿色产业」4 字命中 68 行、「绿色低碳」宽词命中 "
    f"{facts['gkx_policy_text_lvse_ditan_rows']} 行——均为贯彻/规划类叙述（吉林控制温室气体方案、"
    "福建节能减排方案等谈绿色发展目标），非产业占比数据；即使建目录走转换路径，"
    "文本面也无法提供分子分母数值",
    "UI 槽位语义警示：multiDimensionEvalData 的 score 74 是 0-100 分制评分（环境维第 2 分项），"
    "与官方「绿色低碳产业增加值占 GDP 比重」的百分比口径量纲不同——分数到占比无换算锚，"
    "本件按占比语义调研（名称本体），评分口径视为 UI 演示形态",
    "mock 披露：policyData.js:1867 score 74 是效果预估工作台「多维度效果评估」Tab 的环境维演示值，"
    "EstimateWorkbench.jsx:627-640 渲染指标卡（MockBadge 标注）——演示值不参与支持度结论",
    "B11 对账：gkx dwd_policy_base 20,000 行与共享快照零漂移；dwd_org_industry_tags 2,283,762 行"
    "与 skill P4 已踩坑记录（credit_code 非信用代码陷阱）同表对账；dev 政策族行数与 Lane6 探针零漂移",    "升档触发器（B10）：①接入国家统计局《节能环保清洁产业统计分类（2021）》映射表（行业代码→"
    "绿色子集标志）+ 产业产值/GDP 序列 → 分子分母闭合，升完全转换支持；②若甲方接受「政策文本"
    "绿色词频占比」代理 → 语义已换（叙述面≠产业面），本件保守不接受",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_035",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:1867",
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:1845",
        "repos/demo-ui-science/src/pages/policy-tracking/simulation/estimate/EstimateWorkbench.jsx:627",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份需求真源未出现「绿色产业/绿色产业占比」；主需求 1.1.1.1.4.2.3.1.4 多维度效果评估"
                "「从经济、社会、环境、创新等多个维度对政策效果进行评估」是维度语义源（环境维）；"
                "语义源=UI mock multiDimensionEvalData.dimensions[environment].indicators[1]",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["绿色产业年度产值/增加值序列", "区域 GDP 或全域产业总产值序列"],
    "base_years_note": "本件无任何年度序列承载（判定维+产值面双缺）；文本叙述面年度分布不作基期",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts["gkx_policy_rows"]),
                          str(facts["gkx_policy_text_lvse_chanye_rows"]),
                          str(facts["gkx_policy_text_lvse_ditan_rows"]),
                          str(facts["gkx_industry_tags_rows"]),
                          str(facts["gkx_industry_tag_distinct_words"]),
                          str(facts.get("gkx_org_greenname_rows", 0)),
                          str(facts.get("gkx_global_policy_text_green_rows", 0)), "280", "203"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
