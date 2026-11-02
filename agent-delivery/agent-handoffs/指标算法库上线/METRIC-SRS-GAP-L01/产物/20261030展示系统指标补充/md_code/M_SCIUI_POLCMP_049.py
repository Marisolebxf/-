#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_049 加计扣除比例（基础值） · 三源探针与登记脚本（S3-03 Lane 4）。

含义：规划指标库「扶持力度」维的量化指标件——研发费用税前加计扣除比例的制度基准档
（基础值史线 50%→75%→100%，2023 年公告第 7 号起 100% 普适化长期实施）。
UI：pages/policy-tracking/policyPcData.js:333 planningMetricLib[3]（pm4，
name 加计扣除比例，sample 120%，dim 扶持力度）；消费引用 :534（pol-zjtx m2 槽位
value '120'）。export l3 挂「规划指标库搭建＞适用范围与除外情形＞加计扣除比例」
（与 UI dim 扶持力度有出入——以 UI 槽位为准，export l3 是拆件层级误差）。
姊妹件：POLCMP_009（调整值=现行 120% 档）——本件 049 是制度基准史线件，
两件须对账零漂移（gkx 文本面 265 行/窄窗 57 行/title 15 行在案）。

三源实况（全部实探，2026-11-01，与 009 同日同库对账）：
- gkx：dwd_policy_base 33 列无比例结构化列（policy_support 占位全 'null'）；
  全文本「加计扣除」265 行、窄窗正则 57 行、title 本体 15 行——与 009 零漂移。
- dev：policy_base_info 40,000 行同构；policy_quantitative_index/policy_index_info
  两张规划指标库落位候选表不存在（1146）。
- 久新：210 张 ads_* 扫 policy/metric/index/quant 的命中面与 009 同类目
  （年度指标/学科分解/指数/人才维度/专利分析/政策证据六类），无政策条款量化面。
判档：部分支持（与 009 同判——结构化承载三源全缺；文本转换面有量可启动抽取，
基础值制度史线 50%→75%→100% 是公开外部锚，对表校验可直接闭合）。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_049_out.json")
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


# ============ ① gkx：比例结构化列 + 加计扣除文本面（与 009 对账） ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

policy_cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_policy_base")]
facts["gkx_policy_col_count"] = len(policy_cols)
facts["gkx_policy_intensity_cols"] = [c for c in policy_cols if re.search(
    r"intensity|ratio|percent|rate|amount|subsid|support|deduct|tax", c, re.I)]
facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])
TEXT_FIELDS = ("CONCAT_WS(' ',IFNULL(title,''),IFNULL(theme,''),IFNULL(content,''),"
               "IFNULL(keywords,''),IFNULL(keypoints,''))")
# 全文本扫「加计扣除」（与 009 同口径零漂移对账）
facts["gkx_text_jjkc_rows"] = int(qg(
    f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TEXT_FIELDS} LIKE '%加计扣除%'")[0][0])
# 窄窗正则（30 字符窗比例值紧邻加计扣除语境——基础值档位 {50,75,100} 的抽取候选）
PAT = "加计扣除[^。；;]{0,30}?([0-9]{2,3})[ ]*%|([0-9]{2,3})[ ]*%[^。；;]{0,20}?加计扣除"
facts["gkx_text_jjkc_with_pct_rows"] = int(qg(
    f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TEXT_FIELDS} REGEXP '{PAT}'")[0][0])
# title 层本体政策（黄金种子集）
facts["gkx_text_jjkc_title_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE title LIKE '%加计扣除%'")[0][0])
# 基础值档位专项窄窗（50%/75%/100% 三档在库内文本的分布——基础值史线的库内证据）
for pct in ["50", "75", "100", "120"]:
    pat_v = (f"加计扣除[^。；;]{{0,30}}?{pct}[ ]*%|{pct}[ ]*%[^。；;]{{0,20}}?加计扣除")
    facts[f"gkx_jjkc_pct{pct}_window_rows"] = int(qg(
        f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TEXT_FIELDS} REGEXP '{pat_v}'")[0][0])
# 基础值史线关键年份样本（2017 提高通知/2018 提高通知是基础值档位切换的公告本体）
rows = qg("SELECT id, title, ministry, publish_year FROM gkx.dwd_policy_base "
          "WHERE title LIKE '%加计扣除%' AND (title LIKE '%提高%' OR title LIKE '%比例%') "
          "ORDER BY publish_year LIMIT 10")
facts["gkx_jjkc_basevalue_title_sample"] = [
    [_ser(c) if c is not None else "" for c in r] for r in rows]
# 占位列三证（与 009 共证）
facts["gkx_policy_support_nonnull"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE policy_support IS NOT NULL "
    "AND policy_support != ''")[0][0])
facts["gkx_policy_support_distinct_sample"] = [_ser(r[0]) for r in qg(
    "SELECT DISTINCT policy_support FROM gkx.dwd_policy_base WHERE policy_support IS NOT NULL "
    "AND policy_support != '' LIMIT 5")]
facts["gkx_policy_support_pct_like"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE policy_support REGEXP "
    "'[0-9]{2,3}[ ]*%'")[0][0])
gcur.close()

# ============ ② dev：同构与落位表（与 009 共证） ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
DEV_TEXT = ("CONCAT_WS(' ',IFNULL(title,''),IFNULL(theme,''),IFNULL(content,''),"
            "IFNULL(keywords,''),IFNULL(keypoints,''))")
lcur.execute("SELECT COUNT(*) FROM policy_base_info")
facts["dev_policy_base_info_rows"] = int(lcur.fetchone()[0])
facts["dev_text_jjkc_rows"] = int(lcur.execute(
    f"SELECT COUNT(*) FROM policy_base_info WHERE {DEV_TEXT} LIKE '%加计扣除%'")
    or lcur.fetchall()[0][0]) if False else None
lcur.execute(f"SELECT COUNT(*) FROM policy_base_info WHERE {DEV_TEXT} LIKE '%加计扣除%'")
facts["dev_text_jjkc_rows"] = int(lcur.fetchall()[0][0])
for t in ["policy_quantitative_index", "policy_index_info"]:
    try:
        lcur.execute(f"SELECT COUNT(*) FROM {t}")
        facts[f"dev_{t}_rows"] = int(lcur.fetchall()[0][0])
    except Exception as e:  # noqa: BLE001
        facts[f"dev_{t}_rows"] = f"no-table: {str(e)[:60]}"
lconn.close()

# ============ ③ 久新：政策条款量化面（与 009 同类目排除） ============
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
    facts["jiuxin_policy_metric_like_tables"] = [t for t in jx_tables if re.search(
        r"policy|metric|index|quant|deduct|tax", t, re.I)]
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)[:120]

# ============ 派生与登记 ============
derived.append({
    "key": "jjkc_mention_share",
    "value": round(facts["gkx_text_jjkc_rows"] / facts["gkx_policy_rows"] * 100, 3),
    "numerator": facts["gkx_text_jjkc_rows"],
    "denominator": facts["gkx_policy_rows"],
    "note": "叙述面提及占比（转换构建的工作量指示器）——与 POLCMP_009 derived[0] 同口径"
            "零漂移对账",
})
derived.append({
    "key": "rd_deduction_ratio_base",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "不可直查——三源无结构化比例字段；基础值制度史线 50%(2008 立法确认)→75%"
            "(2017 科小/2018 全行业)→100%(2021 制造业/2022 科小/2023 普适化长期实施，"
            "财政部税务总局公告 2023 年第 7 号)在公告原文，库内仅文本提及",
})

absence = [
    {"probe": "gkx 结构化比例列",
     "source": "gkx",
     "sql": "SHOW COLUMNS FROM dwd_policy_base（33 列）扫 intensity/ratio/percent/rate/"
            "deduct/tax",
     "hits": 0,
     "hit_detail": "33 列无比例结构化列；唯一扶持列 policy_support 占位三证"
                   "（20,000/20,000 全 'null'、DISTINCT={'null'}、% 模式 0 命中）"
                   "——与 POLCMP_009 共证零漂移"},
    {"probe": "dev 量化指标承载表",
     "source": "dev",
     "sql": "SELECT COUNT(*)：policy_quantitative_index / policy_index_info",
     "hits": 0,
     "hit_detail": "两表不存在（1146 no-table）——规划指标库（扶持力度维）在开发库无"
                   "落位表（与 POLCMP_009 共证）"},
    {"probe": "久新政策条款量化面",
     "source": "jiuxin",
     "sql": "SHOW TABLES（实测 210 张，探测日 2026-11-01）扫 policy/metric/index/quant/"
            "deduct/tax",
     "hits": 0,
     "hit_detail": "命中面与 009 同类目（年度指标/学科分解/指数/人才维度/专利分析/政策"
                   "证据六类），deduct/tax 词根 0 命中——分析仓无政策条款量化面"},
    {"probe": "需求文档定义",
     "source": "doc",
     "sql": "rg 加计扣除 主需求 + SRS 政策族四文件 + 核增 17 叶",
     "hits": 0,
     "hit_detail": "三份需求真源无该指标名；核增 PC-04 规划指标库四维是维度语义源；"
                   "export mean 是占比类模板语（与 009 同款拆件模板误差），实义以 UI "
                   "pm4 槽位为准；export l3「适用范围与除外情形」层级与 UI dim「扶持"
                   "力度」有出入（拆件层级误差，登记不改判）"},
]

support = "部分支持"

notes = [
    "判档：与 POLCMP_009（调整值）同判同缺口——结构化承载三源全缺（gkx 占位列/dev 落位表"
    "不存在/久新无条款量化面），文本转换面有量（265/57/15 三层，与 009 零漂移对账）。"
    "差异点在「值域」：049 基础值=制度基准史线 50%→75%→100%（50% 是 2008 年企业所得税法"
    "立法确认的基准档，96 年起试点时即 50%）；009 调整值=现行调整档（120% 集成电路线，"
    "普适档 100%）。两件对表校验共用同一窄窗抽取管线",
    "基础值档位的库内证据：窄窗档位分布 50%/75%/100%/120% 四档在 265 行提及面中的分布"
    "落产物（gkx_jjkc_pct{50,75,100,120}_window_rows）——档位分布形态与制度推进史吻合"
    "（2017 科小 75%→2018 全行业 75%→2021 制造业 100%），title 样本含「关于提高科技型"
    "中小企业研究开发费用税前加计扣除比例的通知(2017)」「财政部税务总局科技部关于提高"
    "研究开发费用税前加计扣除比例的通知(2018)」两份基础值切换公告本体",
    "制度史线（外部锚，R1/R2 核验在案）：1996 财工字 41 号试点 50%→2008 企业所得税法立法"
    "确认 50%→财税〔2017〕34 号科小 75%→财税〔2018〕99 号全行业 75%→2021 公告 13 号"
    "制造业 100%→2022 公告 16/28 号科小与 Q4 100%→2023 公告 7 号 100% 普适化长期实施。"
    "「基础值」建议口径：随年度切换的基准档序列（50%:≤2016 / 75%:2017-2020 / "
    "100%:2021→，科小线提前一年）",
    "UI mock 披露：policyPcData.js:333 pm4（sample 120%）是演示值——注意 mock 作者写的是"
    "现行调整档 120%（与 009 的 :523 同一槽位同值），基础值史线在 UI 无独立槽位，"
    "049/009 的拆分是拆件层设计（pm4 同槽两位），MD 登记此形态。演示值不参与支持度结论",
    "升档触发器（B10）：与 009 共用——①条款量化抽取管线（窄窗 57 行起步+gold 标注集）"
    "落地并以制度史线对表校验 → 升完全转换支持；②制度值直录（公告字典表）→ 零转换"
    "直查但语义降常量引用。049 的直录形态比 009 更自然（基础值史线是封闭档位序列，"
    "一张年份×档位维表即可承载）",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_049",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/policyPcData.js:333",
        "repos/demo-ui-science/src/pages/policy-tracking/policyPcData.js:534",
        "repos/demo-ui-science/src/pages/policy-tracking/PolicyPcPages.jsx:578",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份需求真源无该指标名；核增 4.2.4.1.4 规划指标库四维之「扶持力度」是"
                "维度语义源；export l3 挂「适用范围与除外情形」（与 UI dim 扶持力度有"
                "出入，拆件层级误差登记）；与 POLCMP_009（调整值）互为姊妹件",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [2008, 2017, 2018, 2021, 2022, 2023],
    "base_years_missing": [],
    "base_years_note": "基础值制度史线锚年份（公告生效年）；库内文本面年度分布与 009 同"
                       "（2005-2022，峰值 2017 年 38 行）",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts.get("gkx_text_jjkc_rows", "")),
                          str(facts.get("gkx_policy_rows", "")),
                          str(facts.get("gkx_text_jjkc_with_pct_rows", "")),
                          str(facts.get("gkx_text_jjkc_title_rows", "")),
                          str(facts.get("jiuxin_table_count", "")),
                          "50", "75", "100", "120"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", OUT)
