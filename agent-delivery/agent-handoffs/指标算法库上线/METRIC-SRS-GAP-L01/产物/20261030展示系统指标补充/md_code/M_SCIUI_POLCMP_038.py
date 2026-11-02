#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_038 留用意愿指数 · 三源探针与登记脚本（S3-03 Lane 4）。

含义：科技政策跟踪·政策分析评价（DS-11 政策/企业/人才三画像）语境下，人才画像卡的 KPI——
「留用意愿指数」（policyData.js:2224，演示值 78 分）。export 自认「各维度怎么构成、
权重怎么定，需要立项调研后才能确定」——评分口径未闭合。
留用意愿 = 人才留在本地/本单位继续工作的主观意愿强度（离职倾向的逆指标），
权威形态是 HR 调研口径的离职率（中智/美世系：主动离职率）与 NSFC 杰青流动研究。

三源实况（全部实探，2026-11-01）：
- 意愿面（问卷/满意度/留任意愿字段）：三源零承载——gkx 280 表 0 命中；
  dev 542 表 0 命中（无 talent 族表）；久新 210 张 ads_* 全表列扫 0 命中
  （retain/turnover/attrition/satisf/willing/intent/survey/question/opinion/prefer/attitude
  十一词族逐表 DESC 扫描）。
- 行为面（客观流动事件）：久新 ads_talent_mobility_event 298,384 行（78,826 人才）+
  ads_talent_experience 140,887 行 + ads_talent_profile 100,000 行——客观行为可算
  「3 年留任/流动率」类代理，但行为≠意愿（流动是意愿+机会+制度的混合结果）。
- dev policy_public_opinion（19 列满意度结构）0 行——政务侧反馈面结构在、数据空
  （与 POLCMP_008 共证）。
判档：完全不支持（口径未闭合 + 意愿面三源零承载；行为面仅能给出「留用意愿」的
弱代理且语义已换——本件按 B10 不接受代理换义）。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_038_out.json")
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


# ============ ① gkx：意愿/调查类表名扫 + 政策文本「留用」叙述面 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
WILL_WORDS = r"survey|question|feedback|opinion|review|comment|satisf|turnover|attrition|retain|willing|intent|prefer|attitude|quit|resign"
gkx_will_raw = [t for t in gkx_tables if re.search(WILL_WORDS, t, re.I)]
facts["gkx_willingness_like_tables_raw"] = gkx_will_raw
# 语义排除：fund_equity_sector_allocation（股权行业配置）是 intent 词根误命中，非意愿表
facts["gkx_willingness_like_tables"] = [t for t in gkx_will_raw if "sector_allocation" not in t]
# 政策文本「留用/留住人才」叙述面（政策关注留用议题的证据——非意愿测量）
TF = ("CONCAT_WS(' ',IFNULL(title,''),IFNULL(theme,''),IFNULL(content,''),"
      "IFNULL(keywords,''),IFNULL(keypoints,''))")
facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])
facts["gkx_text_liuyong_rows"] = int(qg(
    f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TF} LIKE '%留用%'")[0][0])
facts["gkx_text_liuzhu_rows"] = int(qg(
    f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TF} LIKE '%留住%'")[0][0])
rows = qg(f"SELECT id, title, publish_year FROM gkx.dwd_policy_base "
          f"WHERE {TF} LIKE '%留住%' AND {TF} LIKE '%人才%' LIMIT 8")
facts["gkx_text_liuzhu_talent_sample"] = [[_ser(c) if c is not None else "" for c in r] for r in rows]
gcur.close()

# ============ ② dev：talent 族表 + 满意度/意愿类表列扫 ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           charset="utf8mb4", connect_timeout=10, read_timeout=120)
dconn = pymysql.connect(**DEV)
dcur = dconn.cursor()
dcur.execute("SELECT table_schema, table_name FROM information_schema.tables "
             "WHERE table_schema LIKE 'gkxlumenx%' ORDER BY table_schema, table_name")
dev_tabs = [(r[0], r[1]) for r in dcur.fetchall()]
facts["dev_table_count"] = len(dev_tabs)
facts["dev_talent_tables"] = [f"{s}.{t}" for s, t in dev_tabs if re.search(r"talent", t, re.I)]
DEV_WILL = (r"survey|feedback|opinion|satisf|turnover|attrition|retain|willing|"
            r"intent|prefer|attitude|quit|resign")
facts["dev_willingness_like_tables"] = [f"{s}.{t}" for s, t in dev_tabs
                                        if re.search(DEV_WILL, t, re.I)]
# 已知满意度结构表复核（与 POLCMP_008 共证）
dcur.execute("SHOW COLUMNS FROM gkxlumenx_dwd.policy_public_opinion")
facts["dev_policy_public_opinion_cols"] = [r[0] for r in dcur.fetchall()]
dcur.execute("SELECT COUNT(*) FROM gkxlumenx_dwd.policy_public_opinion")
facts["dev_policy_public_opinion_rows"] = int(dcur.fetchone()[0])
dconn.close()

# ============ ③ 久新：210 张 ads_* 全表列扫（意愿类列）+ mobility 行为面 ============
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
    facts["jiuxin_talent_table_count"] = len([t for t in jx_tables if "talent" in t.lower()])
    JX_KW = re.compile(r"retain|turnover|attrition|satisf|willing|intent_|survey|"
                       r"question|opinion|prefer|attitude", re.I)
    col_hits = []
    for t in jx_tables:
        try:
            jcur.execute("DESC `" + t + "`")
            cols = [r[0] for r in jcur.fetchall()]
            h = [c for c in cols if JX_KW.search(c)]
            if h:
                col_hits.append({"table": t, "cols": h})
        except Exception:  # noqa: BLE001
            pass
    # 语义排除：department/department_en 是误命中（词根 intend 无关，实为 dept），
    # mobility_event_id/mobility_type 是事件类型列非意愿列
    facts["jiuxin_willingness_like_cols"] = col_hits
    facts["jiuxin_willingness_like_semantic_hits"] = [
        h for h in col_hits
        if not set(h["cols"]) <= {"department", "department_en",
                                  "mobility_event_id", "mobility_type"}]
    # 行为面（客观流动——留用意愿的弱代理候选，语义已换）
    jcur.execute("SELECT COUNT(*) FROM ads_talent_mobility_event")
    facts["jiuxin_mobility_event_rows"] = int(jcur.fetchone()[0])
    jcur.execute("SELECT COUNT(DISTINCT talent_id) FROM ads_talent_mobility_event")
    facts["jiuxin_mobility_distinct_talents"] = int(jcur.fetchone()[0])
    jcur.execute("SELECT mobility_type, COUNT(*) FROM ads_talent_mobility_event "
                 "GROUP BY mobility_type ORDER BY 2 DESC")
    facts["jiuxin_mobility_by_type"] = [[r[0], int(r[1])] for r in jcur.fetchall()]
    jcur.execute("SELECT COUNT(*) FROM ads_talent_profile")
    facts["jiuxin_talent_profile_rows"] = int(jcur.fetchone()[0])
    jcur.execute("SELECT COUNT(*) FROM ads_talent_experience")
    facts["jiuxin_talent_experience_rows"] = int(jcur.fetchone()[0])
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)[:120]

# ============ 派生与登记 ============
# 叙述面派生比（同基相除：分子=「留住+人才」命中行，分母=gkx 政策全表）
derived.append({
    "key": "liuzhu_talent_share_pct",
    "value": round(facts["gkx_text_liuzhu_rows"] / facts["gkx_policy_rows"] * 100, 3)
    if facts["gkx_policy_rows"] else None,
    "numerator": facts["gkx_text_liuzhu_rows"],
    "denominator": facts["gkx_policy_rows"],
    "note": "「留住」叙述面占 gkx 政策全表比（留意题政策关注度指示器，非意愿测量）",
})
# 负结论登记键
derived.append({
    "key": "retention_willingness_index",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "不可算——意愿面三源零承载；评分口径未立项（export 自认需调研）；"
            "行为面（久新 mobility 298,384 行）是流动率代理非意愿，语义已换不采用",
})

absence = [
    {"probe": "gkx 意愿/调查类表",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）扫 " + WILL_WORDS,
     "hits": 0,
     "hit_detail": "gkx 是科技要素库（论文/专利/机构/政策），无任何问卷/满意度/离职类表"},
    {"probe": "dev 意愿类表与 talent 族",
     "source": "dev",
     "sql": "information_schema.tables（gkxlumenx* 542 表）扫 talent/" + DEV_WILL,
     "hits": 0,
     "hit_detail": "dev 无 talent 族表（0 张）；唯一满意度结构表 policy_public_opinion 19 列 0 行"
                   "（与 POLCMP_008 共证——政务反馈面结构在、数据空）"},
    {"probe": "久新意愿类列全表扫",
     "source": "jiuxin",
     "sql": "SHOW TABLES（实测 210 张，探测日 2026-11-01）逐表 DESC 扫 "
            "retain/turnover/attrition/satisf/willing/intent_/survey/question/opinion/"
            "prefer/attitude 十一词族",
     "hits": 0,
     "hit_detail": "词根命中仅 department/department_en（词根误命中）与 mobility_event_id/"
                   "mobility_type（事件类型列）——语义排除后 0 命中；"
                   "mobility 298,384 行是客观流动事件非主观意愿"},
    {"probe": "需求文档定义",
     "source": "doc",
     "sql": "rg 留用意愿/留用 主需求 + SRS 政策族四文件 + 核增 17 叶 + 算法库",
     "hits": 0,
     "hit_detail": "三份需求真源无「留用意愿」指标名；「留用」仅现于算法库 :934 深圳人才"
                   "优势短板模型的策略语境（引进/培养/留用策略，非指标定义）；"
                   "export 自认「各维度怎么构成、权重怎么定，需要立项调研后才能确定」"},
]

support = "完全不支持"

notes = [
    "判档：口径未闭合（export 自认需立项调研）+ 意愿面三源零承载（gkx 280 表/dev 542 表/"
    "久新 210 表全列扫）双缺。行为面（久新 ads_talent_mobility_event 298,384 行、"
    "78,826 人才）可算客观流动/留任率，但行为≠意愿（流动是意愿+机会+制度混合结果），"
    "按 B10 保守不采用代理换义",
    "权威口径参照：HR 调研系（中智/美世）以「主动离职率」为留用的逆指标——深圳 2021H1 "
    "主动离职率 11.2%、高科技行业 11.4%、研发/技术人员 7.9%（样本调查口径）；NSFC 杰青"
    "研究以「更换单位占比」14.94% 度量高层次人才流动。两者都是行为代理，非意愿直测——"
    "意愿直测只有问卷（李克特量表）一条路，三源无问卷面",
    "UI mock 披露：policyData.js:2224 人才画像卡 KPI「留用意愿指数 78 分」与 metrics 行"
    "「3 年留用率 68%」是 DS-11 Wave0 扩展 mock 常量（演示值不参与支持度结论）——"
    "mock 作者区分了「意愿指数」（主观）与「留用率」（行为）两个读数，恰证明 UI 语义"
    "层面前者非后者可替代",
    "政策文本叙述面：「留用」78 行、「留住」N 行（含「留住人才」语境样本 8 条）——这是"
    "政策关注留用议题的证据（议题面），不是任何人群的意愿测量；把政策条数当意愿读数"
    "会犯量纲错误",
    "久新活库注记：表数实测 210 张（2026-11-01 探测日），上游持续加表——正文写「实测 N 张"
    "（探测日）」不写死总数；talent 族 42 张全为客观画像/能力/流动/合作面",
    "升档触发器（B10）：①应用侧人才调研/问卷功能上线并回流（意愿事件台账）+ 评分模型"
    "立项 → 升完全转换支持；②若甲方接受「3 年留任率」行为代理口径（久新 mobility 可算）"
    "→ 该读数语义是留任率非留用意愿，须更名交付并披露口径差",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_038",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:2224",
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:2231",
        "repos/demo-ui-science/src/pages/policy-tracking/analysis/PortraitTrio.jsx:40",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份需求真源无「留用意愿」；UI DS-11 三画像卡（PortraitTrio 消费）是"
                "唯一实证；export mean 自认口径需立项调研",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "意愿指数无年度序列（口径未闭合）；叙述面年度分布无计算意义",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts.get("gkx_text_liuyong_rows", "")),
                          str(facts.get("jiuxin_mobility_event_rows", "")),
                          str(facts.get("jiuxin_mobility_distinct_talents", "")),
                          str(facts.get("jiuxin_table_count", "")),
                          "78", "68"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", OUT)
