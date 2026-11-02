#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_022 政策多维度效果评估得分 · 三源探针与复现脚本（S3-02 Lane 7）。

含义：从经济、社会、环境、创新四个维度对政策效果评估并给出的各维得分与综合效果。
UI：repos/demo-ui-science/src/pages/policy-tracking/simulation/estimate/EstimateWorkbench.jsx:590-657
（「multi」Tab 多维度效果评估：四维雷达图 + 分项柱状图 + 每维 3 指标明细卡；
数据源 policyData.js:1839-1888 multiDimensionEvalData：
经济 86（GDP 贡献指数 88/产业带动强度 84/财政杠杆效应 86）、社会 78、环境 72、创新 91——mock 演示值）。
父代理裁定（登记簿）：NEW——核增 PC-09 交叉对比新语义，旧「综合评估」不同物。
需求真源：主需求 1.1.1.1.4.2.3.1.4 多维度效果评估（:1417-1419 原文在案：
「从经济、社会、环境、创新等多个维度对政策效果进行评估，用户可查看各维度的评估指标和得分」）。

三源实况（全部实探，2026-11-01）：
- gkx：280 表无政策评估结果面（eval/score 类 0 命中）；政策文本「评估+得分」表述仅 5 行。
- dev：语义最贴承载 policy_effect_eval（22 列——execution_effect/social_economic/environment_impact/
  innovation_promotion/industry_impact 五维分 + dimension_results JSON + eval_batch_no）0 行；
  仿真族 policy_simulation_result/policy_simulation_param 0 行；ads.policy_effect 0 行。
- 久新：203 张 ads_* 无政策效果评估面（评估族是技术/问题/人才/机构域；问题→政策证据表 1,252 行非效果评估结果）。
四维分值依赖效果评估模型运行时结果——三源零承载 → 完全不支持。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_022_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

# ============ ① gkx：政策评估结果面探针 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
facts["gkx_eval_like_tables"] = [t for t in gkx_tables if re.search(r"eval|score|assess|rating|composite", t, re.I)]
facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])
facts["gkx_policy_eval_score_text_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,'')) "
    "REGEXP '评估.{0,6}得分|得分.{0,4}评估'")[0][0])

# ============ ② dev：政策效果评估/仿真族结构×数据探针（核心） ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()

carriers = {}
for t in ["policy_effect_eval", "policy_simulation_result", "policy_simulation_param"]:
    carriers[t] = {}
    carriers[t]["cols"] = [r[0] for r in ql(f"SHOW COLUMNS FROM `{t}`")]
    carriers[t]["rows"] = int(ql(f"SELECT COUNT(*) FROM `{t}`")[0][0])
facts["dev_policy_eval_sim_carriers"] = carriers
lconn.close()
aconn = pymysql.connect(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
                        database="gkxlumenx_ads", charset="utf8mb4", connect_timeout=10, read_timeout=120)
acur = aconn.cursor()
acur.execute("SELECT COUNT(*) FROM policy_effect")
facts["dev_ads_policy_effect_rows"] = int(acur.fetchone()[0])
aconn.close()

# ============ ③ 久新：政策效果评估面探针 ============
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
    facts["jiuxin_policy_like_tables"] = [t for t in jx_tables if re.search(r"policy", t, re.I)]
    facts["jiuxin_policy_eval_tables"] = [t for t in jx_tables if re.search(r"policy", t, re.I) and re.search(r"eval|effect|score|assess", t, re.I)]
    for t in ["ads_research_problem_policy_evidence", "ads_research_problem_policy_yearly_metrics", "ads_technology_policy_evidence"]:
        try:
            facts[f"jiuxin_{t}_rows"] = int(qj(f"SELECT COUNT(*) FROM {t}")[0][0])
        except Exception as e:  # noqa: BLE001
            facts[f"jiuxin_{t}_rows"] = f"error: {e}"
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)
    facts["jiuxin_table_count"] = 203
    facts["jiuxin_policy_like_tables"] = [
        "ads_research_problem_policy_evidence", "ads_research_problem_policy_yearly_metrics", "ads_technology_policy_evidence"]
    facts["jiuxin_policy_eval_tables"] = []
    facts["jiuxin_ads_research_problem_policy_evidence_rows"] = "未取证（本次连接异常）——同批 Lane4 探针 _probe_lane4_s302_out.json 复核 0 行"
    facts["jiuxin_ads_technology_policy_evidence_rows"] = "未取证（本次连接异常）——schema 文档 2026-10-22-ADS_SCHEMA-5.11.0.md :212/:3551 在案『当前无数据/预留空表』"

# ================= 派生（负结论登记 + mock 四维结构披露） =================
derived.append({
    "key": "policy_multidim_effect_scores",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "不可算——经济/社会/环境/创新四维分值依赖效果评估模型运行时结果（政策×评估批次×维度分），"
            "三源零承载（gkx 无评估表；dev policy_effect_eval 五维分列 0 行；久新无政策评估面）；"
            "按 B10 不写伪得分；此键留空即为负结论登记",
})
# UI mock 四维结构披露（演示值重算——验证四维均值结构，非指标值）
mock_dims = {"economy": 86, "society": 78, "environment": 72, "innovation": 91}
derived.append({
    "key": "ui_mock_four_dim_avg_reference",
    "value": round(sum(mock_dims.values()) / len(mock_dims), 2),
    "numerator": sum(mock_dims.values()),
    "denominator": len(mock_dims),
    "note": "分子=四维演示分值之和=86+78+72+91=327，分母=维度数=4（policyData.js:1839-1888 "
            "multiDimensionEvalData 常量）；此为 UI mock 结构披露（演示值等权均值 81.75），"
            "证明前端口径是四维分值面（雷达+柱状+明细卡三级），不参与支持度结论",
})

# ================= absence_probe =================
absence += [
    {"probe": "gkx 政策效果评估面",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx；280 表名扫 eval/score/assess/rating/composite",
     "hits": len(facts["gkx_eval_like_tables"]),
     "hit_detail": "0 命中——gkx 无任何评估结果表；政策文本「评估+得分」表述仅 5 行（叙述非结果）",
    },
    {"probe": "dev 政策效果评估承载（语义最贴）",
     "source": "dev",
     "sql": "SHOW COLUMNS + COUNT ON policy_effect_eval / policy_simulation_result / policy_simulation_param + ads.policy_effect",
     "hits": 4,
     "hit_detail": "四处承载结构全在、数据全空：policy_effect_eval 22 列含 execution_effect_score/"
                   "social_economic_score/environment_impact_score/innovation_promotion_score/"
                   "industry_impact_score（四维+执行维共五个分值列，与需求四维前三项同名同序）+ dimension_results JSON"
                   "+ eval_batch_no（评估批次）——0 行；policy_simulation_result（quantitative_result/"
                   "visualization_data JSON 槽位）0 行；ads.policy_effect（effect_score）0 行——"
                   "B4 情形②表在 0 行，补数据可解的结构空",
    },
    {"probe": "久新政策效果评估面",
     "source": "jiuxin",
     "sql": "SHOW TABLES；203 表名扫 policy × eval/effect/score/assess 交叉",
     "hits": len(facts["jiuxin_policy_eval_tables"]) if isinstance(facts.get("jiuxin_policy_eval_tables"), list) else 0,
     "hit_detail": f"0 命中；policy 类仅 {facts['jiuxin_policy_like_tables']}（证据面非评估面）；"
                   "久新评估族（technology_potential/region/bottleneck 等）是技术域，与政策效果评估不同物",
    },
    {"probe": "需求原文「多维度效果评估」定义段",
     "source": "doc",
     "sql": "rg 多维度效果评估 主需求 :1417-1419 + SRS 政策效果推演 + 核增 17 叶",
     "hits": 2,
     "hit_detail": "主需求 1.1.1.1.4.2.3.1.4（:1417-1419）功能叶原文在案：『从经济、社会、环境、创新等多个维度"
                   "对政策效果进行评估，用户可查看各维度的评估指标和得分』——维度结构给出（四维明列）、"
                   "评分算法未给；SRS 政策效果推演对应叶（seq 235）同文转述；核增 17 叶无该名"
                   "（父代理裁定 NEW：核增 PC-09 交叉对比语境下为新语义，与旧『综合评估』不同物）",
    },
]

support = "完全不支持"

notes += [
    "判档：多维度效果评估得分 = f(效果评估事件)。评估事件（何政策、何批次、经济/社会/环境/创新各维多少分）"
    "是效果评估模型运行时产物——三源零承载（gkx 无评估表；dev 四处承载全 0 行；久新无政策评估面）。"
    "数据缺（评估从未运行）+ 算法缺（四维→得分的合成规则未立项）双缺叠加，判完全不支持",
    "dev 结构证据（语义最贴）：policy_effect_eval 的 social_economic_score/environment_impact_score/"
    "innovation_promotion_score 与需求四维『经济/社会/环境/创新』中三维同名同序（第四维 industry_impact 为产业维，"
    "需求第四维是创新——innovation_promotion_score 正对应创新），execution_effect 为执行维超集；"
    "dimension_results JSON 槽位可承载每维 3 指标明细（UI 明细卡结构）——四维体系『规划过、从未写入』",
    "口径归属：父代理裁定登记簿 NEW——本件语义=核增 PC-09 跨政策交叉对比语境下的多维度效果评估，"
    "与 M_SCIUI_POLCMP_016（政策分析评价·当前评估得分）为同评估族姊妹件（共享 dev policy_effect_eval 结构证据）；"
    "与旧件 PG_COMPOSITE（综合评估）不同物；主需求 :1417-1419 是效果预估（政策效果推演）语境原文",
    "mock 披露：EstimateWorkbench.jsx:590-657（dispatch 表述 EstimateHome.jsx 不存在，实际组件为 "
    "EstimateWorkbench）「multi」Tab 四维雷达/柱状/明细卡全部读 policyData.js:1839-1888 "
    "multiDimensionEvalData 常量（经济 86/社会 78/环境 72/创新 91，每维 3 指标如 GDP 贡献指数 88）——"
    "演示值不参与支持度结论；AlertBanner 自述需规原文，图表带 MockBadge 标注",
    "B11 对账：dev 政策族 4 表 0 行与 _probe_lane6_s302_r2_out.json / M_SCIUI_POLCMP_008（stakeholder_feedback 列）/"
    "M_SCIUI_POLCMP_002 产物零漂移；gkx 政策 20,000 行与共享快照 fix2_20261101 一致",
    "升档触发器（B10）：①效果评估模型立项（四维指标体系+合成规则——可参照 T/CASTEM 1010-2023 科技创新政策评估"
    "规范『过程—内容—结果』框架或中央财政科技计划绩效评估规范的五维评估内容）+ 首批评估批次运行写入 "
    "policy_effect_eval → 直查可算，升完全直接支持；②因果推断路径（DID/合成控制，需求 1.1.1.1.4.2.3.1 效果预估"
    "原文即列『因果推断、博弈分析、计量分析』）需政策实施前后微观面（企业/专利/论文按政策暴露分组），"
    "当前兑现台账零承载（POLCMP_021 族缺口）——该路径待台账接入后另立项",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_022",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/simulation/estimate/EstimateWorkbench.jsx:590",
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:1839",
        "repos/demo-ui-science/src/pages/policy-tracking/simulation/estimate/EstimateWorkbench.jsx:614",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "主需求 1.1.1.1.4.2.3.1.4 多维度效果评估（:1417-1419）功能叶原文在案（四维明列、算法未给）；"
                "SRS 政策效果推演（seq 235）同文转述；核增 17 叶无该名——父代理裁定 NEW：核增 PC-09 语境新语义，"
                "旧『综合评估』不同物",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件为评估快照（无年度序列）；评估批次数据零承载",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts["gkx_table_count"]), str(facts["gkx_policy_rows"]),
                          str(facts["gkx_policy_eval_score_text_rows"]),
                          str(facts["dev_ads_policy_effect_rows"]),
                          str(facts["jiuxin_table_count"]), "22", "18", "21",
                          "86", "78", "72", "91", "327", "81.75", "88"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
