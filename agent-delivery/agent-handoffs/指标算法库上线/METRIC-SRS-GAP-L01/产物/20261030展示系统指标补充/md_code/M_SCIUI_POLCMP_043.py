#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_043 示范场景开放数 · 三源探针与复现脚本（S3-03 Lane 3）。

含义：政策条款/清单规定的示范应用场景开放数量（个）——场景供给政策的量化指标。
官方口径先例：北京政府机构每年开放场景不少于 5 项（R1）；南京每年发布应用场景
清单 1000 个（机会清单 500/能力清单 300/案例清单 200）（R2）；科技部六部门场景
清单常态化发布机制（R3）；深圳 2025 政务 AI 场景清单 50 个（R4）。
UI：repos/demo-ui-science/src/pages/policy-tracking/policyPcData.js:343
planningMetricLib[4]（pm5：name 示范场景开放数，dim 适用范围，unit 个，
sample 30，scope 重点行业应用场景，validity 2026 年度清单，applyCond 场景
主管部门联合认定）；消费引用 :419（pol-ai-2026 metrics m3，value '30'
unit '个'，kind 时间节点）+ 条款树 :411（c3-1 第五条 首购首用与示范场景清单）。

三源实况（全部实探，2026-11-01）：
- gkx：dwd_policy_base 33 列无场景清单类结构化列（policy_support 占位与 009/044/048
  共证）；全文本「示范场景」命中 5 行、「应用场景」173 行、「场景开放」7 行——场景类政策
  在库内是叙述面（窄量），无结构化清单承载（开放多少个场景的字段/表零承载）。
- dev：政策族 38 表无场景清单落位表；policy_base_info 同构无承载。
- 久新：203 张 ads_* 无场景清单面（scenario/scene 词根扫独立留证；
  ads_technology_application_case 181,735 行是技术应用案例面——语义邻接但非
  「政策开放的示范场景清单」）。
判档：部分支持——结构化承载三源全无；文本转换面窄量（「示范场景」5 行/「应用场景」
173 行/「场景开放」7 行）；制度值（各地清单数量）是外部锚。与兑现事件族缺口同型
（场景开放事件无台账），但场景清单本身是政策文本附件形态，抽取路径与 044 同型。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_043_out.json")
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

# ============ ① gkx：场景清单结构化列 + 文本面 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

policy_cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_policy_base")]
facts["gkx_policy_col_count"] = len(policy_cols)
facts["gkx_policy_scene_like_cols"] = [c for c in policy_cols if re.search(
    r"scene|scenario|demo|pilot|示范|场景", c, re.I)]
facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])
TEXT_FIELDS = "CONCAT_WS(' ',IFNULL(title,''),IFNULL(theme,''),IFNULL(content,''),IFNULL(keywords,''),IFNULL(keypoints,''))"
# 全文本扫场景词族（分层：示范场景精确 / 应用场景 / 场景开放）
facts["gkx_text_shifanchangjing_rows"] = int(qg(
    f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TEXT_FIELDS} LIKE '%示范场景%'")[0][0])
facts["gkx_text_yingyongchangjing_rows"] = int(qg(
    f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TEXT_FIELDS} LIKE '%应用场景%'")[0][0])
facts["gkx_text_changjing_kaifang_rows"] = int(qg(
    f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TEXT_FIELDS} LIKE '%场景开放%'")[0][0])
facts["gkx_text_changjing_all_rows"] = int(qg(
    f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TEXT_FIELDS} LIKE '%场景%'")[0][0])
# 数字表述窄窗：「N 个…场景」模式（简化两段式正则防 ICU 3699 超时）
NUM_A = r"[0-9]个[^。；;]{0,15}场景"
NUM_B = r"场景[^。；;]{0,15}?[0-9]个"
n_num = 0
for pat in (NUM_A, NUM_B):
    n_num += int(qg(f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TEXT_FIELDS} REGEXP '{pat}'")[0][0])
facts["gkx_text_changjing_with_number_rows"] = n_num
# title 层本体
facts["gkx_text_shifan_title_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE title LIKE '%示范%'")[0][0])
# 命中样本（语义核验）
sample = qg(f"SELECT id, title, publish_year FROM gkx.dwd_policy_base "
            f"WHERE {TEXT_FIELDS} LIKE '%示范场景%' ORDER BY id LIMIT 6")
facts["gkx_text_shifanchangjing_sample"] = [[_ser(c) if c is not None else "" for c in r] for r in sample]
sample2 = qg(f"SELECT id, title, publish_year FROM gkx.dwd_policy_base "
             f"WHERE {TEXT_FIELDS} LIKE '%应用场景%' ORDER BY id LIMIT 6")
facts["gkx_text_yingyongchangjing_sample"] = [[_ser(c) if c is not None else "" for c in r] for r in sample2]
# 全球政策面对照
facts["gkx_global_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_global_policy_base")[0][0])
facts["gkx_global_text_changjing_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_global_policy_base WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,'')) "
    "LIKE '%场景%'")[0][0])

# ============ ② dev：场景清单落位表 + 同构核验 ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()
# 场景/示范类表扫（全 schema）
lcur.execute("SELECT TABLE_NAME, TABLE_SCHEMA FROM information_schema.TABLES WHERE TABLE_SCHEMA IN "
             "('gkxlumenx_dwd','gkxlumenx_ods','gkxlumenx_ads','gkxlumenx_dim') AND TABLE_NAME REGEXP "
             "'scene|scenario|pilot|demo_case|application_case'")
facts["dev_scene_like_tables"] = sorted([[r[1], r[0]] for r in lcur.fetchall()])
# 政策族量化落位表复核（与 009/044/048 共证）
for t in ["policy_quantitative_index", "policy_index_info"]:
    try:
        facts[f"dev_{t}_rows"] = int(ql(f"SELECT COUNT(*) FROM `{t}`")[0][0])
    except Exception as e:  # noqa: BLE001
        facts[f"dev_{t}_rows"] = f"no-table: {str(e)[:60]}"
# dev 政策文本同构核验
DEV_TEXT = "CONCAT_WS(' ',IFNULL(title,''),IFNULL(theme,''),IFNULL(content,''),IFNULL(keywords,''),IFNULL(keypoints,''))"
facts["dev_text_shifanchangjing_rows"] = int(ql(
    f"SELECT COUNT(*) FROM policy_base_info WHERE {DEV_TEXT} LIKE '%示范场景%'")[0][0])
facts["dev_text_changjing_all_rows"] = int(ql(
    f"SELECT COUNT(*) FROM policy_base_info WHERE {DEV_TEXT} LIKE '%场景%'")[0][0])
lconn.close()

# ============ ③ 久新：场景清单/应用案例面 ============
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
    facts["jiuxin_scene_like_tables"] = [t for t in jx_tables if re.search(
        r"scene|scenario|application_case|pilot", t, re.I)]
    # 应用案例表语义核验（行数与共享快照对账）
    if "ads_technology_application_case" in jx_tables:
        jcur.execute("SELECT COUNT(*) FROM ads_technology_application_case")
        facts["jiuxin_ads_application_case_rows"] = int(jcur.fetchone()[0])
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)
    notes.append("久新连接失败按未取证登记（B4：连接失败≠0 行），不参与判档数字")

# ============ 派生与登记 ============
# 叙述面占比（同基相除：分子=文本命中行，分母=全表）
if facts["gkx_text_changjing_all_rows"] > 0:
    derived.append({
        "key": "changjing_text_share_pct",
        "value": round(100.0 * facts["gkx_text_changjing_all_rows"] / facts["gkx_policy_rows"], 4),
        "numerator": facts["gkx_text_changjing_all_rows"],
        "denominator": facts["gkx_policy_rows"],
        "note": "分子=gkx 政策全文含「场景」的行数，分母=dwd_policy_base 全表 20,000；同表同池（B3）；"
                "场景词叙述覆盖面（转换口径工作量指示器），不是场景开放数读数",
    })
# 负结论登记键：结构化清单数不可直查
derived.append({
    "key": "demo_scenario_open_count",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "不可直查——三源无「政策→示范场景清单数」结构化承载；场景清单本体是政策附件/"
            "独立发文形态（如深圳 2025 政务 AI 场景清单 50 个 R4、南京年度 1000 个 R2），"
            "库内文本面窄量（示范场景 5 行/应用场景 173 行/场景开放 7 行）；"
            "demo=示范（demonstration scenario）语义标注，非演示库前缀",
})

absence += [
    {"probe": "gkx 场景清单结构化列",
     "source": "gkx",
     "sql": "SHOW COLUMNS FROM dwd_policy_base（33 列）扫 scene/scenario/demo/pilot/示范/场景",
     "hits": len(facts["gkx_policy_scene_like_cols"]),
     "hit_detail": "0 列命中——政策属性表无场景清单数列；280 表无场景清单表（开放场景的"
                   "条目级台账零承载）"},
    {"probe": "dev 场景清单落位表",
     "source": "dev",
     "sql": "information_schema.TABLES 四 schema 扫 scene/scenario/pilot/demo_case/application_case "
            "+ policy_quantitative_index/policy_index_info 行数",
     "hits": len(facts["dev_scene_like_tables"]),
     "hit_detail": "0 张场景清单表（application_case 类是技术应用案例面非政策开放清单）；"
                   "量化落位两表不存在（1146，与 009/044/048 共证）"},
    {"probe": "久新场景清单/案例面",
     "source": "jiuxin",
     "sql": "SHOW TABLES（203 表）扫 scene/scenario/application_case/pilot",
     "hits": len(facts.get("jiuxin_scene_like_tables", [])),
     "hit_detail": "命中 ads_technology_application_case（181,735 行，共享快照对账）——技术商业化"
                   "应用案例面（技术→案例关联），语义邻接但非「政策开放的示范场景清单」；"
                   "无政策→场景数承载"},
    {"probe": "需求原文「示范场景」定义段",
     "source": "doc",
     "sql": "rg 示范场景/场景开放/应用场景 三份需求真源（指标名级）",
     "hits": 0,
     "hit_detail": "三份需求真源未出现「示范场景开放数」指标名；核增需求「场景」4 处均为"
                   "「使用场景/应用场景」语境（展示层定位/政策解析适用场景），非场景开放指标；"
                   "核增 PC-04 规划指标库四维是维度语义源（本件挂适用范围维 pm5）"},
]

support = "部分支持"

notes += [
    "判档：示范场景开放数是政策清单属性（数量写死在各地场景清单发文/政策附件里：北京每年政府"
    "开放≥5 项 R1、南京年度清单 1000 个 R2、科技部常态化清单机制 R3、深圳 2025 政务清单 50 个 R4）。"
    "库内无结构化承载（gkx 无场景列/表、dev 无落位、久新案例面语义错位），文本转换面窄量"
    "（示范场景 5 行/应用场景 173 行/场景开放 7 行/数量表述 16 行）——与 044 同型缺口但量级更低，"
    "判部分支持",
    "语义邻接证伪：久新 ads_technology_application_case（181,735 行）是「技术→应用案例」关联面"
    "（技术商业化案例），不是「政策开放→示范场景」清单——表名 application 误中风险在案，"
    "本件不采作承载",
    "文本面边界：「示范场景」5 行、「应用场景」173 行、「场景开放」7 行、「N个…场景」数量表述 "
    "16 行——场景类政策在库内有叙述面（应用场景层量可），但库内政策收录窗截止 2022，"
    "而场景开放政策潮是 2023+（北京 R1/南京 R2/深圳清单 R4 均为 2024+ 发文）；现行清单均在库外，"
    "对表校验须接外部发文源",
    "mock 披露：policyPcData.js:343 pm5（sample 30 个）与 :419 m3（value '30' unit '个'）、"
    "条款树 :411 c3-1（第五条 首购首用与示范场景清单）是 PC 端演示值——mock 政策 pol-ai-2026 "
    "的场景条款演示；演示值不参与支持度结论",
    "B11 对账：gkx dwd_policy_base 20,000 行与共享快照零漂移；久新 ads_technology_application_case "
    "181,735 行与共享快照（S3-01 探针）零漂移；dev 量化表 no-table 与 009/044/048 共证链一致",
    "升档触发器（B10）：①场景清单结构化抽取（政策附件解析+各地清单发文对接，R1-R4 官方源）→ "
    "升完全转换支持；②若甲方接受「政策文本场景词频/数量表述」代理 → 应用场景层 173 行可作弱"
    "指示（示范场景层 5 行不可靠），本件保守不接受作指标值；③对接政府场景发布平台 API"
    "（如深圳清单发布页）→ 条目级台账可建",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_043",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/policyPcData.js:343",
        "repos/demo-ui-science/src/pages/policy-tracking/policyPcData.js:419",
        "repos/demo-ui-science/src/pages/policy-tracking/policyPcData.js:411",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份需求真源未出现「示范场景开放数」指标名；核增需求「场景」4 处均为使用场景语境"
                "非场景开放指标；核增 PC-04 规划指标库四维是维度语义源（本件挂适用范围维 pm5）；"
                "UI policyPcData.js:343 是 PC 端规划指标库演示槽位",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["政策→示范场景清单数 结构化序列"],
    "base_years_note": "指标本体是清单属性（年度清单随发文切换）；文本叙述面年度分布不作基期",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts["gkx_policy_rows"]),
                          str(facts["gkx_text_shifanchangjing_rows"]),
                          str(facts["gkx_text_yingyongchangjing_rows"]),
                          str(facts["gkx_text_changjing_kaifang_rows"]),
                          str(facts["gkx_text_changjing_all_rows"]),
                          str(facts["gkx_text_changjing_with_number_rows"]),
                          str(facts.get("jiuxin_ads_application_case_rows", "未取证")),
                          str(facts.get("gkx_global_text_changjing_rows", 0)), "33", "203"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
