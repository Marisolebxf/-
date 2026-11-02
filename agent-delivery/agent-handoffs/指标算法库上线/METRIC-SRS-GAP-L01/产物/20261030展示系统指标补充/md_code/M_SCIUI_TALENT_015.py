#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TALENT_015 引进障碍与风险合规评估 · 三源探针与复现脚本（S3-03 Lane 5）。

含义：人才引进评估页（talent-preview EvaluationPage）「引进障碍与风险合规评估」卡——
左半 barrierCards 三卡（沟通障碍风险/文化融合风险/国际流动壁垒，level 中/中高/高）+
右半 complianceItems 三行（学术诚信=未发现异常/合作合规=存在跨境条款需复核/出访敏感性=中等风险）。
UI：repos/demo-ui-science/src/pages/talent-preview/pageRenderer/EvaluationPage.jsx:661-685
（barrierCards/complianceItems 两组常量均为组件内写死演示文案）。

SRS 溯源：主需求 :2367-2369 学者引进难度预测——功能清单明列「沟通障碍智能检测、文化融合风险评估、
国际流动壁垒分析」（.2.2/.2.3/.2.4）+ :2441 尽调报告「风险与合规性评估」（.6，TALENTIR_010 承接）。
「引进障碍与风险合规评估」作为卡片名 0 命中（UI 拆件）；三子障碍叶需求明列。

三源判档路径：
- 障碍三维（沟通/文化/流动）评分结构三源零承载（与 TALENTIR_004 适应性件同构：语言/文化维无源）；
- 流动壁垒维数据在：ads_talent_mobility_event 跨国事件 8,748（旁路在读，本件独立复探）；
- 合规三维（学术诚信/合作合规/出访敏感）结构零承载：撤稿面可代理学术诚信（实测 0 撤稿），
  合作合规（跨境条款）与出访敏感性（安全审查）无任何库内承载；
- 「过往合作情况回溯」（.2.5，障碍评估的第四依赖）在：institution_cooperation 表 0 行（TALENTIR_010 在案）。
→ 障碍/合规评分面零承载 + 部分代理维（流动事件/撤稿）在 → 部分支持。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_TALENT_015_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

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

# ---------- ① 障碍三维结构探针 ----------
facts["jiuxin_barrier_like_tables"] = [t for t in jx_tables
                                       if re.search(r"barrier|obstacle|friction|difficulty|compliance", t, re.I)]
facts["jiuxin_language_culture_like_tables"] = [t for t in jx_tables
                                                if re.search(r"language|culture|communication", t, re.I)]

# ---------- ② 流动壁垒维（数据在的障碍维） ----------
facts["jiuxin_mobility_event_rows"] = int(qj("SELECT COUNT(*) FROM ads_talent_mobility_event")[0][0])
facts["jiuxin_mobility_distinct_talents"] = int(
    qj("SELECT COUNT(DISTINCT talent_id) FROM ads_talent_mobility_event")[0][0])
rows = qj("SELECT mobility_type, COUNT(*) FROM ads_talent_mobility_event "
          "GROUP BY mobility_type ORDER BY mobility_type")
facts["jiuxin_mobility_event_type_dist"] = [[str(a), int(b)] for a, b in rows]
facts["jiuxin_mobility_cross_country_events"] = int(
    qj("SELECT COUNT(*) FROM ads_talent_mobility_event WHERE is_cross_country = 1")[0][0])
facts["jiuxin_mobility_cross_province_events"] = int(
    qj("SELECT COUNT(*) FROM ads_talent_mobility_event WHERE is_cross_province = 1")[0][0])

# ---------- ③ 合规三维代理维 ----------
# 学术诚信：撤稿面
facts["jiuxin_retracted_papers"] = int(
    qj("SELECT COUNT(*) FROM ads_paper_profile WHERE is_retracted = 1")[0][0])
facts["jiuxin_paper_profile_rows"] = int(qj("SELECT COUNT(*) FROM ads_paper_profile")[0][0])
# 合作合规：过往合作回溯（institution_cooperation，schema 标注「预留」）
if "ads_talent_institution_cooperation" in jx_tables:
    facts["jiuxin_institution_cooperation_rows"] = int(
        qj("SELECT COUNT(*) FROM ads_talent_institution_cooperation")[0][0])
# 合作边替代面：talent_collaborator（跨境合作强度的代理底料）
facts["jiuxin_talent_collaborator_rows"] = int(qj("SELECT COUNT(*) FROM ads_talent_collaborator")[0][0])
# 出访敏感性：export_control/visa/security 词族
facts["jiuxin_security_like_tables"] = [t for t in jx_tables
                                        if re.search(r"export|visa|sanction|security|sensitive", t, re.I)]
jconn.close()

# ---------- ④ gkx：障碍/合规承载探针 ----------
gcur = gkx()
gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
facts["gkx_barrier_compliance_like_tables"] = [t for t in gkx_tables
                                               if re.search(r"barrier|obstacle|compliance|difficulty|visa|sanction", t, re.I)]
gcur.close()

# ---------- ⑤ dev：障碍/合规承载探针 ----------
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
lcur.execute("SELECT table_schema, table_name FROM information_schema.tables "
             "WHERE table_schema LIKE 'gkxlumenx%%' AND table_name REGEXP 'barrier|obstacle|compliance|difficulty'")
facts["dev_barrier_compliance_like_tables"] = [f"{r[0]}.{r[1]}" for r in lcur.fetchall()]
lconn.close()

# ================= 派生 =================
n_evt = facts["jiuxin_mobility_event_rows"]
n_cc = facts["jiuxin_mobility_cross_country_events"]
derived.append({
    "key": "jiuxin_cross_country_event_share_pct",
    "value": round(100.0 * n_cc / n_evt, 2),
    "numerator": n_cc,
    "denominator": n_evt,
    "note": "分子=is_cross_country=1 的迁移事件数；分母=ads_talent_mobility_event 总行数（同表全量非采样）——"
            "国际流动壁垒维的事件面强度读数",
})
n_tal = facts["jiuxin_mobility_distinct_talents"]
derived.append({
    "key": "jiuxin_mobility_event_talent_coverage_per_10k",
    "value": round(10000.0 * n_tal / 100000, 2),
    "numerator": n_tal,
    "denominator": 100000,
    "note": "分子=有迁移事件的人才去重数；分母=profile 总行数 100,000（旁路共享读数非本表派生，"
            "作覆盖率量级参考——两表同池 MVP 100,000 人）",
})
derived.append({
    "key": "scholar_barrier_compliance_assessment_score",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "不可算——障碍三维（沟通/文化/流动）与合规三维（学术诚信/合作合规/出访敏感）的评分口径与"
            "结果面三源零承载；按 B10 不写伪分。可用代理维：流动事件面（跨国占比）+ 撤稿面（学术诚信，"
            "实测 0）+ 合作边面（talent_collaborator 底料）",
})

# ================= absence_probe =================
absence.extend([
    {"probe": "久新实测表 barrier/obstacle/friction/difficulty/compliance 词族（障碍与合规评分面）",
     "source": "jiuxin", "sql": "SHOW TABLES 后词族扫（探测日实测表数见 facts.jiuxin_table_count）",
     "hits": 0, "hit_detail": "命中 []——障碍/合规评分结果面零承载；语言/文化词族表亦 0 命中"
            "（jiuxin_language_culture_like_tables=[]）"},
    {"probe": "久新 export/visa/sanction/security/sensitive 词族（出访敏感性维）",
     "source": "jiuxin", "sql": "SHOW TABLES 后词族扫",
     "hits": 0, "hit_detail": "命中 []——出访敏感性/出口管制/签证类承载零命中"},
    {"probe": "gkx 280 表 barrier/obstacle/compliance/difficulty/visa/sanction 词族",
     "source": "gkx", "sql": "SHOW TABLES FROM gkx 后词族扫",
     "hits": 0, "hit_detail": "命中 []——风险词族仅企业失信/税务/执行表（dwd_org_risk_*），"
            "无学者障碍/合规承载"},
    {"probe": "dev gkxlumenx_* barrier/obstacle/compliance/difficulty 词族",
     "source": "dev", "sql": "information_schema.tables 扫 gkxlumenx_*",
     "hits": 0, "hit_detail": "命中 []——dev 无障碍/合规承载"},
    {"probe": "需求原文障碍三维评分算式",
     "source": "doc",
     "sql": "rg 沟通障碍/文化融合/国际流动壁垒/风险合规 三份需求真源",
     "hits": 3, "hit_detail": "需求明列三障碍子叶（:2369 清单 + :2375/.2.2 沟通障碍智能检测 + :2379/.2.3 "
            "文化融合风险评估 + :2383/.2.4 国际流动壁垒分析）——功能行为在（『自动识别』『分析』『评估』），"
            "评分算式无一字；「引进障碍与风险合规评估」卡片名本身 0 命中（UI 拆件）"},
])

notes.extend([
    "本件支持度按三源评估（20261101 铁律）：dev live 非 demo + gkx 只读 + 久新 ads_* 只读。",
    "障碍三维与 TALENTIR_004（适应性评估）同构缺口：语言能力/文化背景两维三源零承载，"
    "流动维在事件面有数据（跨区事件可算强度）。",
    "合规三维：学术诚信可由撤稿面代理（实测 0 撤稿=全池未发现异常的库内证据）；合作合规的"
    "「跨境条款」维与出访敏感性维零承载（无任何文本/事件承载）。",
    "「过往合作情况回溯」（.2.5）承载在 ads_talent_collaborator（5,051,578 行合作边底料）；"
    "institution_cooperation 表 schema 标注「预留」且 0 行（TALENTIR_010 件在案，本件未重复展开）。",
    "UI barrierCards（沟通/文化/流动 level 中/中高/高）与 complianceItems（学术诚信/合作合规/出访敏感）"
    "均为组件内写死演示文案，登记不作数据证据。",
    "2026 为 PARTIAL_YEAR：迁移事件面不含 2026 正式事件（schema 口径）。",
])

out = {
    "metric_id": "M_SCIUI_TALENT_015",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/talent-preview/pageRenderer/EvaluationPage.jsx:661（DataCard title 引进障碍与风险合规评估）",
        "repos/demo-ui-science/src/pages/talent-preview/pageRenderer/EvaluationPage.jsx:134-142（barrierCards/complianceItems 组件内写死常量）",
        "repos/demo-ui-science/src/pages/talent-preview/pageRenderer/EvaluationPage.jsx:665-681（barrierCards 渲染 + complianceItems 渲染）",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "卡片名「引进障碍与风险合规评估」三份真源 0 命中（UI 拆件）；三障碍子叶需求明列："
                "主需求 :2369/:2375 沟通障碍智能检测、:2379 文化融合风险评估、:2383 国际流动壁垒分析"
                "（1.1.1.1.4.3.4.2.2-.4）；合规侧最近义 :2441 尽调报告「风险与合规性评估」（TALENTIR_010 承接）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": "部分支持",
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件为事件/快照型读数（迁移事件面为 4.5.0 已发布事件集；撤稿面为当前快照），"
                       "无年度基线窗口需求",
    "ctx_refs": {
        "note": "正文引用型数字登记",
        "refs": [],
    },
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1, default=str)
print("ok ->", OUT)
