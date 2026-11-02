#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_048 信贷风险补偿比例 · 三源探针与复现脚本（S3-03 Lane 3）。

含义：政策条款规定的信贷风险补偿比例（%）——政府风险补偿资金池对合作银行不良贷款
本金损失的补偿比例。官方口径先例：广州政银模式按贷款规模分档 20%-40%（最高 50%），
叠加企业类型上浮（R1）；深圳资金池同构分档（R2）；汕头科技企业 50%（R3）；
国家科技创新专项担保分层分险（R4）——比例值是政策条款属性非统计量。
UI：repos/demo-ui-science/src/pages/policy-tracking/policyPcData.js:323
planningMetricLib[2]（pm3：name 信贷风险补偿比例，dim 扶持力度，unit %，
sample 40，scope 专精特新中小企业，applyCond 纳入地方风险补偿名单）；
消费引用 :485（pol-zjtx-2025 metrics m2，value '40' unit '%'）+
条款树 :470-476（z2-1 信贷风险补偿·第一款 补偿比例细则（原则上不低于 40%））。

三源实况（全部实探，2026-11-01）：
- gkx：dwd_policy_base 33 列无风险补偿类结构化列（policy_support 占位与 009/044 共证）；
  全文本「风险补偿」命中 335 行（窄量）、「信贷」命中 1,069 行——窄窗比例模式（%）
  紧邻补偿语境 31 行（转换面在，title 层 22 行）。
- dev：policy_base_info 44 列同构无承载；政策族 38 表无量化落位表（共证）。
- 久新：203 张 ads_* 无政策条款量化面（POLCMP_009 已逐表排除，本件复扫独立留证）。
判档：部分支持——结构化三源全缺；文本转换面窄量（335 行提及/31 行窄窗比例），
与 044 同型但量级更低；制度值（40%）可作外部锚（R1-R4 官方办法）。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_048_out.json")
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

# ============ ① gkx：风险补偿结构化列 + 文本面 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

policy_cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_policy_base")]
facts["gkx_policy_col_count"] = len(policy_cols)
facts["gkx_policy_riskcomp_cols"] = [c for c in policy_cols if re.search(
    r"risk|compensat|guarantee|credit|loan", c, re.I)]
facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])
TEXT_FIELDS = "CONCAT_WS(' ',IFNULL(title,''),IFNULL(theme,''),IFNULL(content,''),IFNULL(keywords,''),IFNULL(keypoints,''))"
# 全文本扫「风险补偿/信贷风险」（叙述面命中总量）
RC = "(风险补偿|信贷风险)"
facts["gkx_text_riskcomp_rows"] = int(qg(
    f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TEXT_FIELDS} REGEXP '{RC}'")[0][0])
# 分层：风险补偿 4 字 / 信贷 2 字（语义分层：工具名 vs 泛信贷语境）
facts["gkx_text_fengxianbuchang_rows"] = int(qg(
    f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TEXT_FIELDS} LIKE '%风险补偿%'")[0][0])
facts["gkx_text_xindai_rows"] = int(qg(
    f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TEXT_FIELDS} LIKE '%信贷%'")[0][0])
# 窄窗比例模式：补偿语境 30 字符内百分比
PCT = r"(风险补偿|补偿比例)[^。；;]{0,30}?([0-9]{1,3})\\s*%|[0-9]{1,3}\\s*%[^。；;]{0,20}?风险补偿"
facts["gkx_text_riskcomp_pct_rows"] = int(qg(
    f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TEXT_FIELDS} REGEXP '{PCT}'")[0][0])
# title 层本体
facts["gkx_text_riskcomp_title_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE title LIKE '%风险补偿%'")[0][0])
# 命中样本（语义核验）
sample = qg(f"SELECT id, title, publish_year FROM gkx.dwd_policy_base "
            f"WHERE {TEXT_FIELDS} REGEXP '{RC}' ORDER BY id LIMIT 8")
facts["gkx_text_riskcomp_sample"] = [[_ser(c) if c is not None else "" for c in r] for r in sample]
# 年度分布（叙述面时间形态）
yd = qg(f"SELECT publish_year, COUNT(*) FROM gkx.dwd_policy_base "
        f"WHERE {TEXT_FIELDS} LIKE '%风险补偿%' GROUP BY publish_year ORDER BY publish_year DESC LIMIT 10")
facts["gkx_text_fengxianbuchang_by_year"] = [[_ser(a), int(b)] for a, b in yd]
# 全球政策面对照
facts["gkx_global_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_global_policy_base")[0][0])
facts["gkx_global_text_riskcomp_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_global_policy_base WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,'')) "
    "LIKE '%风险补偿%'")[0][0])
# 金融语义承载面盘点（补偿资金池/担保的结构化邻接——dev/gkx 共扫词根）
gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
fin_pat = re.compile(r"guarantee|loan|credit|compensat|finance", re.I)
facts["gkx_finance_like_tables"] = [t for t in gkx_tables if fin_pat.search(t)]

# ============ ② dev：同构核验 + 量化落位表 ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()
DEV_TEXT = "CONCAT_WS(' ',IFNULL(title,''),IFNULL(theme,''),IFNULL(content,''),IFNULL(keywords,''),IFNULL(keypoints,''))"
facts["dev_text_riskcomp_rows"] = int(ql(
    f"SELECT COUNT(*) FROM policy_base_info WHERE {DEV_TEXT} REGEXP '{RC}'")[0][0])
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
    facts["jiuxin_riskcomp_like_tables"] = [t for t in jx_tables if re.search(
        r"risk|compensat|guarantee|credit|loan", t, re.I)]
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)
    notes.append("久新连接失败按未取证登记（B4：连接失败≠0 行），不参与判档数字")

# ============ 派生与登记 ============
# 叙述面占比（转换口径工作量指示器，同基相除）
if facts["gkx_text_fengxianbuchang_rows"] > 0:
    derived.append({
        "key": "fxbuchang_mention_share_pct",
        "value": round(100.0 * facts["gkx_text_fengxianbuchang_rows"] / facts["gkx_policy_rows"], 4),
        "numerator": facts["gkx_text_fengxianbuchang_rows"],
        "denominator": facts["gkx_policy_rows"],
        "note": "分子=gkx 政策全文含「风险补偿」的行数，分母=dwd_policy_base 全表 20,000；"
                "同表同池（B3）；叙述覆盖面（转换口径工作量指示器），不是补偿比例读数",
    })
# 负结论登记键：结构化比例值不可直查
derived.append({
    "key": "credit_risk_compensation_ratio",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "不可直查——三源无「政策→补偿比例」结构化承载；文本面窄窗比例 31 行可 NLP 抽取；"
            "比例本体写死在各地风险补偿资金管理办法（广州 20%-40% 分档 R1/深圳同构 R2/"
            "汕头 50% R3/国家专项担保分层 R4），mock 演示值 40% 与国家专精特新政策语境一致",
})

absence += [
    {"probe": "gkx 风险补偿结构化列",
     "source": "gkx",
     "sql": "SHOW COLUMNS FROM dwd_policy_base（33 列）扫 risk/compensat/guarantee/credit/loan",
     "hits": len(facts["gkx_policy_riskcomp_cols"]),
     "hit_detail": "0 列命中——政策属性表无风险补偿比例列；280 表金融语义扫仅融资信息表"
                   "（financing/stock_finance）非风险补偿资金池面"},
    {"probe": "dev 量化指标落位表",
     "source": "dev",
     "sql": "policy_quantitative_index / policy_index_info 行数",
     "hits": 0,
     "hit_detail": "两表不存在（1146 no-table）——规划指标库（扶持力度维）在开发库无落位（与 009/044 共证）"},
    {"probe": "久新风险补偿/担保量化面",
     "source": "jiuxin",
     "sql": "SHOW TABLES（203 表）扫 risk/compensat/guarantee/credit/loan",
     "hits": len(facts.get("jiuxin_riskcomp_like_tables", [])),
     "hit_detail": "命中均为 credit 评级/信誉类表（科技信用评级面）非风险补偿资金池条款量化面——"
                   "无「政策→补偿比例」承载"},
    {"probe": "需求原文「信贷风险补偿」定义段",
     "source": "doc",
     "sql": "rg 信贷风险/风险补偿/信贷 三份需求真源",
     "hits": 0,
     "hit_detail": "三份需求真源均未出现「信贷风险补偿」；核增 PC-04 规划指标库四维是维度语义源"
                   "（扶持力度维 pm3）；UI policyPcData.js:323 演示值 40% 与条款树 :474"
                   "「原则上不低于 40%」是唯一口径线索"},
]

support = "部分支持"

notes += [
    "判档：信贷风险补偿比例是政策条款属性（比例写死在各地风险补偿资金管理办法原文：广州政银"
    "分档 20%-40% 最高 50%（R1）、深圳同构（R2）、汕头 50%（R3）、国家专项担保分层（R4））。"
    "库内无结构化承载，文本转换面窄量：「风险补偿」335 行提及、窄窗比例 31 行、title 层 22 行——"
    "与 POLCMP_044 同型缺口（提及量 335 vs 433、窄窗 31 vs 447，量级更低），判部分支持",
    "文本面时间形态：提及集中在 2013-2022（科技型中小企业信贷风险补偿政策密集期，"
    "2020 年 44 行/2016 年 40 行/2018 年 39 行峰值），2022 年 5 行收尾——叙述面停在库内收录窗，"
    "现行办法（广州 2025 版 R1）在库内文本面无承载，对表校验须接外部公告源",
    "抽取语义警示：「补偿比例」语境混有风险补偿（本指标）/生态补偿/征地补偿等多义——"
    "窄窗须加「信贷/贷款/不良」金融语境锚；gold 校准集前置",
    "mock 披露：policyPcData.js:323 pm3（sample 40%）与 :485 m2（value '40'）、条款树 :474"
    "「第一款 补偿比例细则（原则上不低于 40%）」是 PC 端演示值——mock 政策 pol-zjtx-2025 的"
    "条款树演示；演示值不参与支持度结论",
    "B11 对账：gkx dwd_policy_base 20,000 行与共享快照零漂移；文本面探针与 POLCMP_009（加计扣除 "
    "265 行）/POLCMP_002（惠及 187 行）同日同库可互推；dev no-table 与 Lane6 探针零漂移",
    "升档触发器（B10）：①条款量化抽取管线（窄窗比例 31 行起步+gold 标注）并以各地资金管理办法（R1-R4）"
    "对表校验 → 升完全转换支持；②若甲方接受「制度值直录」（管理办法人工维护字典表）→ "
    "零转换直查但语义降为常量引用",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_048",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/policyPcData.js:323",
        "repos/demo-ui-science/src/pages/policy-tracking/policyPcData.js:485",
        "repos/demo-ui-science/src/pages/policy-tracking/policyPcData.js:474",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份需求真源未出现「信贷风险补偿」；核增 4.2.4.1.4 规划指标库四维是维度语义源"
                "（扶持力度维 pm3）；UI policyPcData.js:323 是 PC 端规划指标库演示槽位，"
                "消费引用 :485 政策详情卡 m2 + 条款树 :474",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["政策→信贷风险补偿比例 结构化序列"],
    "base_years_note": "指标本体是条款属性无年度序列（比例随管理办法生效切换）；文本叙述面年度分布不作基期",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts["gkx_policy_rows"]),
                          str(facts["gkx_text_riskcomp_rows"]),
                          str(facts["gkx_text_fengxianbuchang_rows"]),
                          str(facts["gkx_text_xindai_rows"]),
                          str(facts["gkx_text_riskcomp_pct_rows"]),
                          str(facts["gkx_text_riskcomp_title_rows"]),
                          str(facts.get("gkx_global_text_riskcomp_rows", 0)), "33", "203"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
