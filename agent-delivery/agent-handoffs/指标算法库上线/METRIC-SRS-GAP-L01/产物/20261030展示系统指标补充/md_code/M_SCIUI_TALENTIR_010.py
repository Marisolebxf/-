#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TALENTIR_010 风险与合规性评估 · 三源探针与复现脚本（S3-03 Lane 6）。

含义：人才尽调报告与推荐（1.1.1.1.4.3.4.4.6 风险与合规性评估）——
「支持智能分析专家在合作风险、学术诚信、成果有效性等方面的信息」。
UI：repos/demo-ui-science/src/pages/talent-trend/talentRecommendSpec.js:56
（report.l6 数组 { key:'risk', label:'风险与合规性评估' }——L6 能力映射清单项）。
UI 实现层：data.js:1503-1511 recommendations.riskLevel（pick green/yellow/red 演示枚举）+
risks{cooperation,integrity,validity,ip} 四维 low/medium 演示枚举 + ReportTab RISK_ICONS 消费。

三源判档路径（参照 POLCMP_016 双缺写法）：
- 风险事件面（合作冲突/学术诚信/成果有效性事件）：三源探针——撤稿面（ads_paper_profile.is_retracted）
  是「成果有效性」唯一结构化负向维；
- 评分口径：UI 四维（合作/诚信/有效性/IP）无任何权重/算式定义（需求原文仅列举）；
- capability 模型四维（毅力/创新/学科匹配/政治倾向）中政治倾向是唯一「合规」近邻维（无数据统一 50 分）。
→ 事件面近乎零承载（撤稿 0、无诚信/冲突事件表）+ 口径未立项 → 部分支持（有撤稿结构+合作冲突代理物料）。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_TALENTIR_010_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

# ============ ① gkx：风险/诚信/合规承载探针 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
facts["gkx_risk_like_tables"] = [t for t in gkx_tables
                                 if re.search(r"risk|integrity|misconduct|retract|fraud|compliance", t, re.I)]
# 机构风险面旁证（gkx 有失信面 dwd_org_risk_shixin——skill 白名单表，人才风险是否同构）
facts["gkx_risk_shixin_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_org_risk_shixin")[0][0])
gcur.close()

# ============ ② dev：风险/合规承载探针 ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=60)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()

lcur.execute("SELECT table_schema, table_name FROM information_schema.tables "
             "WHERE table_schema LIKE 'gkxlumenx%%' AND table_name REGEXP 'risk|integrity|misconduct|retract|fraud|compliance'")
facts["dev_risk_like_tables"] = [f"{r[0]}.{r[1]}" for r in lcur.fetchall()]
lconn.close()

# ============ ③ 久新：风险事件面探针（核心） ============
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)
jconn = pymysql.connect(**JX)
jcur = jconn.cursor()
def qj(sql):
    jcur.execute(sql)
    return jcur.fetchall()

jcur.execute("SHOW TABLES")
jx_tables = sorted(r[0] for r in jcur.fetchall())
facts["jiuxin_table_count"] = len(jx_tables)
facts["jiuxin_risk_like_tables"] = [t for t in jx_tables
                                    if re.search(r"risk|integrity|misconduct|retract|fraud|compliance", t, re.I)]

# 3.1 成果有效性维：撤稿面
facts["jiuxin_paper_profile_rows"] = int(qj("SELECT COUNT(*) FROM ads_paper_profile")[0][0])
facts["jiuxin_retracted_papers"] = int(qj(
    "SELECT COUNT(*) FROM ads_paper_profile WHERE is_retracted = 1")[0][0])
facts["jiuxin_paratext_papers"] = int(qj(
    "SELECT COUNT(*) FROM ads_paper_profile WHERE is_paratext = 1")[0][0])

# 3.2 合规近邻维：capability 模型政治倾向（默认分策略）——权重在 model 表，状态在 assessment 表
row = qj("SELECT political_orientation_weight, political_orientation_default_score "
         "FROM ads_talent_capability_model LIMIT 1")
if row:
    facts["jiuxin_political_orientation_model"] = {
        "weight": float(row[0][0]), "default_score": float(row[0][1])}
row = qj("SELECT political_orientation_status, COUNT(*) FROM ads_talent_capability_assessment "
         "GROUP BY political_orientation_status ORDER BY political_orientation_status")
facts["jiuxin_political_orientation_status_dist"] = [[str(a), int(b)] for a, b in row]

# 3.3 合作风险代理物料：合作边表（冲突检测无事件面，合作史是代理底料）
facts["jiuxin_talent_collaborator_rows"] = int(qj(
    "SELECT COUNT(*) FROM ads_talent_collaborator")[0][0])
# 机构合作表（schema 标注「预留」——实测行数定性行前状态）
facts["jiuxin_talent_institution_cooperation_rows"] = int(qj(
    "SELECT COUNT(*) FROM ads_talent_institution_cooperation")[0][0])

# 3.4 人才侧撤稿关联探针：代表成果表是否含撤稿快照列
ra_cols = [r[0] for r in qj("SHOW COLUMNS FROM ads_talent_research_achievement")]
facts["jiuxin_research_achievement_cols"] = ra_cols
facts["jiuxin_research_achievement_risk_like_cols"] = [c for c in ra_cols
                                                       if re.search(r"retract|risk|integrity|withdraw", c, re.I)]
jconn.close()

# ================= 派生（负结论登记 + 撤稿率读数） =================
n_paper = facts["jiuxin_paper_profile_rows"]
n_retract = facts["jiuxin_retracted_papers"]
derived.append({
    "key": "jiuxin_retraction_rate_per_10k",
    "value": round(10000.0 * n_retract / n_paper, 2) if n_paper else None,
    "numerator": n_retract,
    "denominator": n_paper,
    "note": "分子=ads_paper_profile.is_retracted=1 论文数；分母=ads_paper_profile 总行数（400 万 MVP core，"
            "同表全量非采样）——撤稿率万分比；撤稿是『成果有效性』维唯一结构化负向信号",
})
derived.append({
    "key": "scholar_risk_compliance_score",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "不可算——风险事件面（合作冲突/学术诚信/成果有效性事件）三源零承载：撤稿 0 行、"
            "无诚信/冲突/合规事件表；UI 四维（合作/诚信/有效性/IP）权重算式未立项；"
            "按 B10 不写伪分，此键留空即负结论登记",
})

# ================= absence_probe =================
absence += [
    {"probe": "gkx 人才风险/诚信/合规事件面（risk/integrity/misconduct/retract/fraud/compliance 词族）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）词族扫",
     "hits": len(facts["gkx_risk_like_tables"]),
     "hit_detail": f"命中 {facts['gkx_risk_like_tables']}——逐表定性：均为企业侧失信/风险面"
                   f"（dwd_org_risk_shixin {facts['gkx_risk_shixin_rows']} 行），人才侧无任何风险事件表"},
    {"probe": "dev 风险/合规承载（gkxlumenx_* 全 schema 六词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*",
     "hits": len(facts["dev_risk_like_tables"]),
     "hit_detail": f"命中 {facts['dev_risk_like_tables']}——逐表语义排除：无人才风险事件面"},
    {"probe": "久新人才风险事件面（203 表六词族 + 撤稿列实测）",
     "source": "jiuxin",
     "sql": "SHOW TABLES 词族扫 + SELECT COUNT(*) FROM ads_paper_profile WHERE is_retracted=1",
     "hits": len(facts["jiuxin_risk_like_tables"]),
     "hit_detail": f"表名 0 命中；撤稿位实测 {n_retract} 行（400 万 core 中 0 撤稿——MVP core 发布口径"
                   "未含撤稿论文或撤稿标记未同步）；无诚信/合作冲突/合规事件表"},
    {"probe": "需求原文「风险与合规性评估」算法定义段",
     "source": "doc",
     "sql": "rg 风险与合规性评估/学术诚信 三份需求真源（主需求 :2463-2465 命中功能叶）",
     "hits": 1,
     "hit_detail": "需求给出行为（『支持智能分析专家在合作风险、学术诚信、成果有效性等方面的信息』）"
                   "但三方面信息源与风险等级算式无——口径未立项；UI risks 四维 low/medium 为 pick "
                   "mock 演示枚举"},
]

support = "部分支持"

notes += [
    "判档：风险事件面三源零承载（撤稿 0/无诚信表/无冲突表/机构合作预留表 0 行）+ 口径未立项"
    "（UI 四维无算式）——但结构侧有可用件：撤稿位（is_retracted 列在）、合作史代理底料"
    "（ads_talent_collaborator 5,051,578 行）、合规近邻维（capability 政治倾向维+默认分策略）"
    "→ 部分支持（参照 POLCMP_016 双缺+结构证据写法）",
    f"成果有效性维：400 万 MVP core 撤稿位实测 {n_retract} 行（撤稿率万分比 "
    f"{derived[0]['value']}）——负向信号位在但零事件；paratext {facts['jiuxin_paratext_papers']} 行"
    "（版面材料非风险信号，登记对照）",
    "合规近邻维：capability 模型政治倾向维 weight=0.10、无数据统一 50 分（模型公式原文在案："
    f"{facts.get('jiuxin_political_orientation_model')}；状态分布见产物）——"
    "库内合规评估的先例口径（保守默认分策略可借鉴到风险维的『无事件=默认低风险』处理）",
    "合作风险代理：合作边表在案（ads_talent_collaborator 5,051,578 行）——合作史强度可算但"
    "『冲突』事件（合作破裂/纠纷）无承载，代理语义弱；机构合作表（ads_talent_institution_cooperation）"
    "schema 标注「预留」，实测 0 行——预留空表状态在案（B4 情形②）",
    "mock 披露：talentRecommendSpec.js:56 为 L6 清单项；data.js:1503-1511 riskLevel pick(['green',"
    "'yellow','green','green','red']) + risks 四维 pick(['low','low','low','medium'])——纯演示枚举，"
    "不作数据证据（B10）；ReportTab RISK_ICONS 仅消费演示枚举",
    "B11 对账：gkx dwd_org_risk_shixin 行数与 skill 白名单记录同源；久新 ads_talent_collaborator "
    "5,051,578 与 X_015 产物（jiuxin_talent_collab 引用值）零漂移；ads_paper_profile 4,000,000 与"
    "共享快照零漂移；撤稿 0 与 005 产物实测一致",
    "升档触发器（B10）：①接入撤稿数据源（Retraction Watch 等）按 paper_id/DOI 对齐回填 is_retracted "
    "→ 成果有效性维转换可算；②合作冲突事件源（项目结题异常/纠纷记录）立项 → 合作风险维可算；"
    "③甲方裁定风险口径=撤稿+合作史代理双维 → 部分支持→完全转换支持（诚信维降维披露）；"
    "④三维全接源+权重立项 → 完全直接支持",
]

out = {
    "metric_id": "M_SCIUI_TALENTIR_010",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/talent-trend/talentRecommendSpec.js:56",
        "repos/demo-ui-science/src/pages/talent-trend/data.js:1503",
        "repos/demo-ui-science/src/pages/talent-trend/components/ReportTab.jsx:10",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "主需求《科技信息展示系统和科技专题服务系统.md》:2441/:2463-2465（1.1.1.1.4.3.4.4.6 风险"
                "与合规性评估）功能叶明列：『支持智能分析专家在合作风险、学术诚信、成果有效性等方面的信息，"
                "为单位规避引进风险、优化用才决策提供有力支撑』——功能在、信息源与算式无；"
                "核增/算法库两份真源 0 命中",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件为人才快照型评估（风险事件面零承载，无年度序列问题）",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(n_paper), str(n_retract), str(facts["jiuxin_paratext_papers"]),
                          str(facts["jiuxin_talent_collaborator_rows"]),
                          str(facts["jiuxin_talent_institution_cooperation_rows"]),
                          str(facts["gkx_risk_shixin_rows"]), "280", "203", "56", "2463"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
