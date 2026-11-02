#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_044 最高支持额度 · 三源探针与复现脚本（S3-03 Lane 3）。

含义：政策条款规定的单项/单企最高资助额度（万元）——扶持力度维的量化锚。
官方口径先例：深圳「揭榜挂帅」按项目投资额 50% 最高 3000 万元（R1）；国家科技创新
专项担保分险比例分档（R2）——额度值写死在政策公告原文里，是政策条款属性非统计量。
UI：repos/demo-ui-science/src/pages/policy-tracking/policyPcData.js:303
planningMetricLib[0]（pm1：name 最高支持额度，dim 扶持力度，unit 万元，
sample 10000，scope 核心技术攻关项目，applyCond 揭榜挂帅立项且通过中期评估）；
消费引用 :417（pol-ai-2026 metrics m1，value '10000' unit '万元'）——
PC 端多维政策对比「规划指标库」扶持力度维 + 政策详情卡。

三源实况（全部实探，2026-11-01）：
- gkx：dwd_policy_base 33 列无额度类结构化列（唯一扶持类列 policy_support 全 'null' 占位，
  与 POLCMP_009 共证）；全文本「最高支持/最高资助/最高不超过」命中 433 行——
  窄窗金额值模式（万元/亿元/元）紧邻「最高」语境 447 行（转换面有量，两段式正则有少量
  交叉计数，以两段并集语义读）。
- dev：policy_base_info 44 列同构无额度列；政策族 38 表无量化指标落位表
  （policy_quantitative_index/policy_index_info 不存在，Lane6 探针共证）。
- 久新：203 张 ads_* 无政策条款量化面（POLCMP_009 已逐表排除 24 张 metric 类命中，
  本件复扫 policy/amount/quota 词根独立留证）。
判档：部分支持——结构化承载三源全无；文本转换面有量（433 行提及/447 行窄窗金额两段并集），
与 POLCMP_009 加计扣除比例同型缺口、共享抽取管线。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_044_out.json")
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

# ============ ① gkx：额度结构化列 + 文本转换面 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

policy_cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_policy_base")]
facts["gkx_policy_col_count"] = len(policy_cols)
# 额度/金额类结构化列扫
facts["gkx_policy_amount_like_cols"] = [c for c in policy_cols if re.search(
    r"amount|quota|limit|ceiling|cap|fund|subsid|support|grant|award", c, re.I)]
facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])
TEXT_FIELDS = "CONCAT_WS(' ',IFNULL(title,''),IFNULL(theme,''),IFNULL(content,''),IFNULL(keywords,''),IFNULL(keypoints,''))"
# 全文本扫「最高支持/最高资助/最高不超过」（叙述面命中总量）
ZG = "(最高支持|最高资助|最高不超过|最高给予|最高补助|最高奖励)"
facts["gkx_text_zuigao_rows"] = int(qg(
    f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TEXT_FIELDS} REGEXP '{ZG}'")[0][0])
# 窄窗金额值模式：「最高X」语境 30 字符内万元/亿元/元金额（两段式简化正则，防 ICU 3699 超时）
AMT_A = r"最高(支持|资助|不超过|给予|补助|奖励)[^。；;]{0,30}?[0-9](万|亿)?元"
AMT_B = r"[0-9](万|亿)?元[^。；;]{0,20}?最高(支持|资助|不超过|给予|补助|奖励)"
n_amt = 0
for pat in (AMT_A, AMT_B):
    n_amt += int(qg(f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TEXT_FIELDS} REGEXP '{pat}'")[0][0])
facts["gkx_text_zuigao_amount_rows"] = n_amt
# title 层本体（政策名直接含「支持/资助」——抽取种子层）
facts["gkx_text_zhichi_title_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE title REGEXP '支持|资助|补贴|奖励'")[0][0])
# 命中样本（语义核验：最高语境长什么样）
sample = qg(f"SELECT id, title, publish_year FROM gkx.dwd_policy_base "
            f"WHERE {TEXT_FIELDS} REGEXP '{ZG}' ORDER BY id LIMIT 8")
facts["gkx_text_zuigao_sample"] = [[_ser(c) if c is not None else "" for c in r] for r in sample]
# 「万元/亿元」金额面整体覆盖（扶持类政策普遍面——简化正则防超时）
facts["gkx_text_wanyuan_rows"] = int(qg(
    f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TEXT_FIELDS} REGEXP '[0-9]万元|[0-9]亿元'")[0][0])
# policy_support 占位复核（与 009 共证）
facts["gkx_policy_support_nonnull"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE policy_support IS NOT NULL AND policy_support != ''")[0][0])
# 全球政策面对照
facts["gkx_global_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_global_policy_base")[0][0])
facts["gkx_global_text_zuigao_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_global_policy_base WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,'')) "
    f"REGEXP '{ZG}'")[0][0])

# ============ ② dev：同构核验 + 量化落位表 ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()
dev_cols = [r[0] for r in ql("SHOW COLUMNS FROM policy_base_info")]
facts["dev_policy_base_info_col_count"] = len(dev_cols)
facts["dev_policy_base_info_amount_cols"] = [c for c in dev_cols if re.search(
    r"amount|quota|limit|ceiling|cap|fund|subsid|support|grant|award", c, re.I)]
DEV_TEXT = "CONCAT_WS(' ',IFNULL(title,''),IFNULL(theme,''),IFNULL(content,''),IFNULL(keywords,''),IFNULL(keypoints,''))"
facts["dev_text_zuigao_rows"] = int(ql(
    f"SELECT COUNT(*) FROM policy_base_info WHERE {DEV_TEXT} REGEXP '{ZG}'")[0][0])
for t in ["policy_quantitative_index", "policy_index_info"]:
    try:
        facts[f"dev_{t}_rows"] = int(ql(f"SELECT COUNT(*) FROM `{t}`")[0][0])
    except Exception as e:  # noqa: BLE001
        facts[f"dev_{t}_rows"] = f"no-table: {str(e)[:60]}"
lconn.close()

# ============ ③ 久新：政策条款量化面 ============
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
    facts["jiuxin_policy_amount_like_tables"] = [t for t in jx_tables if re.search(
        r"policy|amount|quota|subsid|grant|award", t, re.I)]
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)
    notes.append("久新连接失败按未取证登记（B4：连接失败≠0 行），不参与判档数字")

# ============ 派生与登记 ============
# 叙述面占比（转换口径工作量指示器，同基相除）
if facts["gkx_text_zuigao_rows"] > 0:
    derived.append({
        "key": "zuigao_mention_share_pct",
        "value": round(100.0 * facts["gkx_text_zuigao_rows"] / facts["gkx_policy_rows"], 4),
        "numerator": facts["gkx_text_zuigao_rows"],
        "denominator": facts["gkx_policy_rows"],
        "note": "分子=gkx 政策全文含「最高支持/最高资助/最高不超过」等语境的行数，分母=dwd_policy_base "
                "全表 20,000；同表同池（B3）；叙述覆盖面（转换口径工作量指示器），不是最高支持额度读数",
    })
# 负结论登记键：结构化额度值不可直查
derived.append({
    "key": "max_support_amount_wan",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "不可直查——三源无「政策→最高支持额度」结构化承载（gkx policy_support 占位列/dev 量化表"
            "不存在/久新无政策条款量化面）；文本面窄窗金额 447 行（两段并集）可 NLP 抽取但无 gold "
            "校准；额度本体写死在政策公告原文（如深圳揭榜挂帅最高 3000 万元）",
})

absence += [
    {"probe": "gkx 额度结构化列",
     "source": "gkx",
     "sql": "SHOW COLUMNS FROM dwd_policy_base（33 列）扫 amount/quota/limit/ceiling/cap/fund/subsid/grant/award",
     "hits": len(facts["gkx_policy_amount_like_cols"]),
     "hit_detail": "唯一扶持类列 policy_support 实测 20,000/20,000 全为字面 'null' 占位（与 POLCMP_009 "
                   "共证）——无额度数值列"},
    {"probe": "dev 量化指标落位表",
     "source": "dev",
     "sql": "policy_quantitative_index / policy_index_info 行数",
     "hits": 0,
     "hit_detail": "两表不存在（1146 no-table）——规划指标库（扶持力度维）在开发库无落位；"
                   "policy_base_info 44 列同构无额度列"},
    {"probe": "久新政策条款量化面",
     "source": "jiuxin",
     "sql": "SHOW TABLES（203 表）扫 policy/amount/quota/subsid/grant/award",
     "hits": len(facts.get("jiuxin_policy_amount_like_tables", [])),
     "hit_detail": "命中均为 policy 证据/语境表（POLCMP_009 已逐表排除：科技活动指标面非政策条款面）"
                   "——无「政策→额度值」承载"},
    {"probe": "需求原文「最高支持额度」定义段",
     "source": "doc",
     "sql": "rg 最高支持额度/支持额度/额度 三份需求真源",
     "hits": 0,
     "hit_detail": "三份需求真源均未出现「最高支持额度」；核增 PC-04 规划指标库四维（扶持力度/"
                   "适用范围/实施时效/申请条件）是维度语义源（本件挂扶持力度维首位 pm1）；"
                   "UI policyPcData.js:303 演示值 10000 万元是唯一口径线索"},
]

support = "部分支持"

notes += [
    "判档：最高支持额度是政策条款属性（额度写死在政策公告原文，如深圳 AI 揭榜挂帅按项目投资额 "
    "50% 最高 3000 万元），非统计量。库内无结构化承载（gkx 占位列/dev 无落位表/久新无量化面），"
    "但文本转换面有量：「最高支持/资助/不超过」语境 433 行、窄窗金额模式两段并集 447 行"
    "（正向 30 字符窗+反向 20 字符窗，两段有交叉计数，作并集口径读）、title 层支持语义 1,126 行、"
    "万元/亿元金额面 3,143 行——与 POLCMP_009 加计扣除比例同型缺口（结构缺+文本量在），判部分支持",
    "抽取语义警示：「最高X万元」语境混有多重语义——项目资助上限（本指标）/贷款额度/社保基数/"
    "罚款上限/奖励封顶——窄窗正则须加「支持/资助/补助/奖励」动词锚并排除处罚语境；"
    "gold 校准集（人工标注）是精度保证的前置",
    "mock 披露：policyPcData.js:303 pm1（sample 10000 万元）与 :417 m1（value '10000'）是 PC 端"
    "规划指标库演示值——mock 政策 pol-ai-2026「揭榜挂帅最高支持 1 亿元」的条款演示；"
    "演示值不参与支持度结论",
    "B11 对账：gkx dwd_policy_base 20,000 行/policy_support 占位三证与 POLCMP_009 探针零漂移；"
    "dev 量化表 no-table 与 Lane6 探针零漂移；久新 24 张 metric 类命中逐表排除结论与 009 共证",
    "升档触发器（B10）：①条款量化抽取管线（窄窗金额 447 行起步+gold 标注集）落地并以官方额度"
    "公告（R1 类）对表校验 → 升完全转换支持；②若甲方接受「制度值直录」（公告原文人工维护字典表）"
    "→ 零转换直查但语义降为常量引用",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_044",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/policyPcData.js:303",
        "repos/demo-ui-science/src/pages/policy-tracking/policyPcData.js:417",
        "repos/demo-ui-science/src/pages/policy-tracking/policyPcData.js:393",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份需求真源未出现「最高支持额度」；核增 4.2.4.1.4 政策数据治理·规划指标库四维是"
                "维度语义源——本件挂扶持力度维首位（pm1）；UI policyPcData.js:303 是 PC 端规划指标库"
                "演示槽位，消费引用 :417 政策详情卡 m1",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["政策→最高支持额度 结构化序列"],
    "base_years_note": "指标本体是条款属性无年度序列（额度随政策生效切换）；文本叙述面年度分布不作基期",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts["gkx_policy_rows"]),
                          str(facts["gkx_text_zuigao_rows"]),
                          str(facts["gkx_text_zuigao_amount_rows"]),
                          str(facts["gkx_text_zhichi_title_rows"]),
                          str(facts["gkx_text_wanyuan_rows"]),
                          str(facts["gkx_policy_support_nonnull"]),
                          str(facts.get("gkx_global_text_zuigao_rows", 0)), "33", "203"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
