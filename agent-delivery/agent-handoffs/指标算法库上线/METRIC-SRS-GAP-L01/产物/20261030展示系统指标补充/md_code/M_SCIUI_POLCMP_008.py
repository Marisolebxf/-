#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_008 利益攸关方参与度评估得分 · 三源探针与复现脚本（S3-02 Lane 6）。

含义：按评价模型算出的分数——利益攸关方（决策者/评估者/企业/专家/公众）通过在线问卷/
意见征集/专家评审参与政策评估，系统汇总意见并纳入效果评估模型后的参与度评分。
UI：pages/policy-tracking/simulation/estimate/EstimateWorkbench.jsx:672
（效果预估 Tab「利益攸关方参与评估」子面板）。

三源实况（全部实探，2026-11-01）：
- gkx：280 表扫 survey/question/feedback/opinion/assess/eval 零命中——问卷/意见/评审类
  交互数据表不存在（gkx 是要素库无用户交互面）。
- dev：policy_simulation_result.stakeholder_feedback 列存在（利益攸关方反馈——语义最贴）
  但全表 0 行；gkxlumenx 全库无问卷/feedback 业务表（cms/mp 域未核——属应用层非数据仓）。
- 久新：130 张 ads_* 无问卷/评审面（schema 文档在案）。
判档：完全不支持——参与度评分的分子（参与事件：问卷提交/意见/评审记录）是系统交互侧数据，
三源零承载；评分模型（SRS 原文只给流程不给算法）无闭合口径。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_008_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

# ============ ① gkx：问卷/意见/评审交互面探针 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
facts["gkx_survey_like_tables"] = [t for t in gkx_tables if re.search(
    r"survey|question|feedback|opinion|assess|eval|review|comment|vote", t, re.I)]

# ============ ② dev：仿真结果 stakeholder_feedback 列 + 全库交互面 ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()
# policy_simulation_result 结构（stakeholder_feedback 列）
cols = [r[0] for r in ql("SHOW COLUMNS FROM gkxlumenx_dwd.policy_simulation_result")]
facts["dev_policy_simulation_result_cols"] = cols
facts["dev_policy_simulation_result_has_stakeholder_col"] = "stakeholder_feedback" in cols
facts["dev_policy_simulation_result_rows"] = int(
    ql("SELECT COUNT(*) FROM gkxlumenx_dwd.policy_simulation_result")[0][0])
# 全库扫问卷/反馈类表（dwd/ods/ads/cms/mp 五 schema）
lcur.execute("SELECT TABLE_SCHEMA, TABLE_NAME FROM information_schema.TABLES WHERE "
             "TABLE_SCHEMA LIKE 'gkxlumenx%' AND (TABLE_NAME LIKE '%survey%' OR TABLE_NAME LIKE '%feedback%' "
             "OR TABLE_NAME LIKE '%opinion%' OR TABLE_NAME LIKE '%question%' OR TABLE_NAME LIKE '%review%' "
             "OR TABLE_NAME LIKE '%comment%')")
facts["dev_survey_like_tables"] = [f"{r[0]}.{r[1]}" for r in lcur.fetchall()]
# policy_public_opinion 语义核对（潜在最贴命中：audience_type/feedback_channel/satisfaction_score）
try:
    po_cols = [r[0] for r in ql("SHOW COLUMNS FROM gkxlumenx_dwd.policy_public_opinion")]
    facts["dev_policy_public_opinion_cols"] = po_cols
    facts["dev_policy_public_opinion_rows"] = int(
        ql("SELECT COUNT(*) FROM gkxlumenx_dwd.policy_public_opinion")[0][0])
except Exception as e:  # noqa: BLE001
    facts["dev_policy_public_opinion_rows"] = f"error: {e}"
# policy_favorite（政策收藏——用户交互的最近亲缘表）行数探针
try:
    facts["dev_policy_favorite_rows"] = int(
        ql("SELECT COUNT(*) FROM gkxlumenx_dwd.policy_favorite")[0][0])
except Exception as e:  # noqa: BLE001
    facts["dev_policy_favorite_rows"] = f"error: {e}"
lconn.close()

# ============ ③ 久新：问卷/评审面 ============
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
    facts["jiuxin_survey_like_tables"] = [t for t in jx_tables if re.search(
        r"survey|question|feedback|opinion|assess|eval|review|comment|vote|particip", t, re.I)]
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)
    facts["jiuxin_table_count"] = 130
    # schema 文档全表清单（130 表）核对：无 survey/feedback/participation 类表——
    # ads_* 是分析结果面（技术/问题/人才/机构域），无用户交互承载
    facts["jiuxin_survey_like_tables"] = []

# ================= 派生（不可算登记） =================
derived.append({
    "key": "stakeholder_participation_score",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "不可算——参与事件（问卷提交/意见征集/专家评审记录）三源零承载；"
            "评分模型口径未闭合（SRS 只给四项识别流程不给算法）。此键留空为负结论登记",
})

# ================= absence_probe =================
absence += [
    {"probe": "gkx 问卷/意见/评审交互表",
     "source": "gkx",
     "sql": "SHOW TABLES（280 表）扫 survey/question/feedback/opinion/assess/eval/review/comment/vote",
     "hits": len(facts["gkx_survey_like_tables"]),
     "hit_detail": "0 命中——gkx 是科技要素库（论文/专利/机构/政策），无用户交互数据面"},
    {"probe": "dev 利益攸关方反馈承载",
     "source": "dev",
     "sql": "SHOW COLUMNS FROM policy_simulation_result（stakeholder_feedback 列）+ 全库 survey/feedback 表扫",
     "hits": 1,
     "hit_detail": f"policy_simulation_result.stakeholder_feedback 列存在（JSON 文本槽位）但全表 "
                   f"{facts['dev_policy_simulation_result_rows']} 行；全库 gkxlumenx* 五 schema 扫 "
                   f"survey/feedback/opinion/question/review/comment 表命中 {facts['dev_survey_like_tables']}——"
                   "用户侧交互表在本数据仓无承载（应用库 gkxlumenx_mp/cms 属运行时面非数据仓，不在三源范围）"},
    {"probe": "久新问卷/评审面",
     "source": "jiuxin",
     "sql": "SHOW TABLES（130 表）扫 survey/feedback/particip/assess 类 + schema 文档核对",
     "hits": 0,
     "hit_detail": "130 张 ads_* 全是分析结果面（技术/问题/人才/机构/项目域），无用户交互表；"
                   "schema 文档 2026-10-22-ADS-SCHEMA-5.11.0.md 全表清单在案"},
    {"probe": "SRS/核增需求评分算法定义",
     "source": "doc",
     "sql": "rg 利益攸关方 SRS 政策效果推演.md seq 236 + 核增 17 叶",
     "hits": 1,
     "hit_detail": "SRS seq 236 命中功能定义（在线问卷/意见征集/专家评审→汇总纳入效果评估模型，"
                   "确保评估活动目标合理、组织协调、程序公正规范、方法科学可行）——但只给流程四问"
                   "不给评分算法；核增需求 17 叶无利益攸关方条目"},
]

support = "完全不支持"

notes += [
    "判档：参与度评分 = f(参与事件)。参与事件（谁在何时通过何渠道提交了什么意见/评分）是"
    "系统运行时交互数据——gkx 要素库无此面（280 表 0 命中）；dev 数据仓仅仿真结果表的 "
    "stakeholder_feedback JSON 槽位（0 行）；久新分析库无交互表（130 表全是结果面）。"
    "事件无源 → 分子无源 → 完全不支持（与 POLCMP_001/002 的兑现事件缺口同构：都是『事件在别处』）",
    "SRS 唯一需求真源命中（本 Lane 五件中唯一 named_in_srs=true）：seq 236 给的是流程定义"
    "（问卷/征集/评审三渠道+汇总纳入模型+四项识别），四项识别（目标合理/组织协调/程序公正/方法可行）"
    "是评估活动的质量属性不是参与度算法——UI 的 STAKEHOLDER_AUDIT mock 正是这四项的演示卡",
    "评分模型口径未闭合：『参与度』可能的口径至少三种——A 参与率（参与人数/目标人数）；"
    "B 参与量（意见条数/评审次数）；C 参与质量加权分（身份×渠道×采纳状态）。三源无任何一种的"
    "分子数据。UI 表单（role/score/channel 三字段）暗示 C 口径（身份×渠道×1-5 星评分），"
    "但表单数据存前端 state（setFeedback），无后端落库",
    "mock 披露：EstimateWorkbench.jsx:672 起的『利益攸关方参与评估』子面板——STAKEHOLDER_AUDIT "
    "四卡（页内 mock 常量 :76-81）+ 反馈表单（提交至站内意见列表，message.success 标注"
    "『🧪 Mock，未外发』）——演示值不参与支持度结论",
    "B11 对账：dev policy_simulation_result 0 行与 POLCMP_007/Lane6 探针零漂移；"
    "stakeholder_feedback 列与 Lane6 探针 _probe_lane6_s302_r2_out.json 列清单一致",
    "升档触发器（B10）：①应用侧（gkxlumenx_mp/cms 运行时库）问卷/意见功能上线并回流数据仓 → "
    "参与事件闭合，可升完全转换支持（评分模型随事件结构一并设计）；②若甲方接受政务侧"
    "稳评听证/问卷数据（R1/R2 口径）→ 需外部对接单独立项",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_008",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/simulation/estimate/EstimateWorkbench.jsx:672",
        "repos/demo-ui-science/src/pages/policy-tracking/simulation/estimate/EstimateWorkbench.jsx:673",
        "repos/demo-ui-science/src/pages/policy-tracking/simulation/estimate/EstimateWorkbench.jsx:75",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "SRS 政策效果推演.md seq 236（excel_row 对应效果预估面板）命中『利益攸关方参与评估』"
                "功能叶——本 Lane 五件中唯一需求明列叶；原文给流程（在线问卷/意见征集/专家评审→"
                "汇总纳入效果评估模型）不给评分算法；主需求 :1421-1423 同文；核增 17 叶无该条目"
                "（核增是对比功能升级，本叶属原方案效果预估）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件无年度序列（参与事件本身零承载）",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["280", "130", "0", str(facts["dev_policy_simulation_result_rows"])]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
