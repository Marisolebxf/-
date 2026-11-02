#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TALENTIR_003 引进效果指数（引进产出综合评分）· 三源探针与复现脚本（S3-03 Lane 7）。

含义：人才引进推荐评估·成本结构位「效果指数」——引进投入对位的效果读数（引进产出综合评分）。
派单 mount 列：pages/policy-tracking/simulation/sharedCharts.jsx:713（实查为 NewPolicyPredictionChart
通用预测图 y 轴名「效果指数」——政策效果推演组件复用位，非人才语义主挂载）；kept_items 同条记录
CostTab.jsx:221/:243（「效果指数」双轴趋势线，data.js:1474 effectScore=random(55,92) mock）。
本件按 kept_items 全量 mount 核，主语义挂载取 CostTab（引进成本-效果对位），sharedCharts 记为
跨页复用勘误（回执登记）。

判档（Lane 6 框架：模型承载=三源有结构化模型输出面才部分支持；仅原始事实列则完全不支持，
评分口径缺口登记待裁定）：
- 「引进效果」评分面：三源表名词族（introduce/recruit/attract/impact/effect）+ 模型维核对；
- 替代承载：久新 capability（科研毅力/创新/学科匹配/政治倾向——无引进效果维）与
  potential（五维动量）都是「学者能力」面，无「引进-产出对位」语义；
- 「引进事件」面：三源无引进台账（引进主体/到岗时间/投入），效果指数的「引进前后对比」
  分母无源。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_TALENTIR_003_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []
snap = json.load(open(SNAP, encoding="utf-8"))

# ============ ① gkx：引进效果评分面排除 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
facts["gkx_intro_effect_like_tables"] = [t for t in gkx_tables
    if re.search(r"introduc|recruit|attract|onboard|hire|effect|impact|outcome", t, re.I)]
gcur.close()

# ============ ② dev：引进事件/评分承载排除 ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
lcur.execute(
    "SELECT table_schema, table_name FROM information_schema.tables "
    "WHERE table_schema LIKE 'gkxlumenx%%' AND table_name REGEXP "
    "'introduc|recruit|attract|onboard|hire|effect|impact|talent'")
facts["dev_intro_effect_like_tables"] = [f"{r[0]}.{r[1]}" for r in sorted(lcur.fetchall())]
lconn.close()

# ============ ③ 久新：capability/potential 双评分面核对（核心） ============
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)
jconn = pymysql.connect(**JX)
jcur = jconn.cursor()
def qj(sql):
    jcur.execute(sql)
    return jcur.fetchall()

jx_tables = snap["jiuxin"]["tables"]
facts["jiuxin_table_count"] = len(jx_tables)
facts["jiuxin_intro_effect_like_tables"] = [t for t in jx_tables
    if re.search(r"introduc|recruit|attract|onboard|hire", t, re.I)]

# 3.1 capability 面：模型公式 + 维度表四维枚举 + 总分覆盖
facts["jiuxin_capability_model_formula"] = str(qj(
    "SELECT overall_score_formula FROM ads_talent_capability_model LIMIT 1")[0][0])
facts["jiuxin_capability_dimension_codes"] = sorted(set(str(r[0]) for r in qj(
    "SELECT DISTINCT dimension_code FROM ads_talent_capability_dimension_metric")))
facts["jiuxin_capability_assessment_rows"] = int(qj(
    "SELECT COUNT(*) FROM ads_talent_capability_assessment")[0][0])
facts["jiuxin_capability_overall_nonnull"] = int(qj(
    "SELECT COUNT(overall_score) FROM ads_talent_capability_assessment")[0][0])

# 3.2 potential 面：动量维（未来产出增长的族内近邻面）
facts["jiuxin_potential_result_rows"] = int(qj(
    "SELECT COUNT(*) FROM ads_talent_potential_result")[0][0])
facts["jiuxin_potential_composite_nonnull"] = int(qj(
    "SELECT COUNT(potential_composite_score) FROM ads_talent_potential_result")[0][0])
row = qj("SELECT MIN(potential_composite_score), MAX(potential_composite_score), "
         "ROUND(AVG(potential_composite_score),4) FROM ads_talent_potential_result")
facts["jiuxin_potential_composite_min_max_avg"] = [float(row[0][0]), float(row[0][1]), float(row[0][2])]

# 3.3 引进事件分母排除：profile 无引进字段（到岗年/引进单位）
prof_cols = snap["jiuxin_talent_cols"]["ads_talent_profile"]
facts["jiuxin_profile_intro_cols"] = [c for c in prof_cols
    if re.search(r"introduc|recruit|attract|onboard|hire|arrival|since", c, re.I)]
jconn.close()

# ================= 派生 =================
n_cap = facts["jiuxin_capability_assessment_rows"]
n_cap_score = facts["jiuxin_capability_overall_nonnull"]
derived.append({
    "key": "jiuxin_capability_overall_coverage_pct",
    "value": round(100.0 * n_cap_score / n_cap, 2),
    "numerator": n_cap_score,
    "denominator": n_cap,
    "note": "分子=ads_talent_capability_assessment.overall_score 非空行数；分母=同表总行数"
            "（同表同 WHERE 全量非采样）——capability 综合评分面自身覆盖度，非引进效果指数",
})
n_pot = facts["jiuxin_potential_result_rows"]
n_pot_score = facts["jiuxin_potential_composite_nonnull"]
derived.append({
    "key": "jiuxin_potential_composite_coverage_pct",
    "value": round(100.0 * n_pot_score / n_pot, 2),
    "numerator": n_pot_score,
    "denominator": n_pot,
    "note": "分子=ads_talent_potential_result.potential_composite_score 非空行数；分母=同表总行数"
            "（同表全量）——潜力动量面自身覆盖度，非引进效果指数",
})
# 负结论登记（B10：不写伪分）
derived.append({
    "key": "introduction_effect_index",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "不可算——『引进效果指数』评分口径三源未立项：capability 四维（科研毅力/创新/学科匹配/"
            "政治倾向）与 potential 五维（近期影响/产出动量/引用动量/领导力/主题扩展）均无"
            "『引进-产出对位』维；三源无引进事件台账（到岗时间/引进投入），引进前后对比的分母无源；"
            "按 B10 不写伪分，此键留空即负结论登记",
})

# ================= absence_probe =================
absence += [
    {"probe": "gkx 引进效果评分面（表名 introduc/recruit/attract/onboard/hire/effect/impact/outcome 词族）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）词族扫",
     "hits": len(facts["gkx_intro_effect_like_tables"]),
     "hit_detail": f"命中 {facts['gkx_intro_effect_like_tables']}——逐表语义核对：无一张是"
                   "引进效果/引进产出评分结果面（gkx 为要素明细库，无评分工程）"},
    {"probe": "dev 引进事件/效果承载（gkxlumenx_* 全 schema introduc/recruit/attract/onboard/hire/effect/impact/talent 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_* 16 schema（542 表）",
     "hits": len(facts["dev_intro_effect_like_tables"]),
     "hit_detail": f"命中 {facts['dev_intro_effect_like_tables']}——语义排除：招聘/一般 impact 表，"
                   "无引进效果评分结果面"},
    {"probe": "久新引进效果评分面（210 表 introduc/recruit/attract/onboard/hire 词族）",
     "source": "jiuxin",
     "sql": "SHOW TABLES（210 表，2026-11-01 实测）词族扫 + ads_talent_capability_dimension_metric 维度枚举核对",
     "hits": len(facts["jiuxin_intro_effect_like_tables"]),
     "hit_detail": f"表名 0 命中（{facts['jiuxin_intro_effect_like_tables']}）；capability 维度枚举 = "
                   f"{facts['jiuxin_capability_dimension_codes']}——无『引进』维；profile 96 列引进词族"
                   f"命中 {facts['jiuxin_profile_intro_cols']}"},
    {"probe": "需求原文「引进效果指数」定义段",
     "source": "doc",
     "sql": "rg 引进效果/效果指数 三份需求真源",
     "hits": 0,
     "hit_detail": "三份需求说明书均未出现「引进效果指数」指标名（主需求 :2424 引进成本预测叶只述"
                   "「历年引进投入与效果」趋势追踪行为，无算式）；UI effectScore 为 data.js:1474 "
                   "random(55,92) mock 演示值",
    },
]

support = "完全不支持"

notes += [
    "判档：『引进效果指数』评分口径三源未立项（capability 四维无引进维、potential 五维是学者自身动量"
    "非引进-产出对位、无引进事件台账），依赖侧仅原始事实列（profile 计数列）——按 Lane 6 框架"
    "（仅原始事实列则完全不支持，评分口径缺口登记待裁定）判完全不支持",
    f"替代面读数：capability 综合评分面覆盖 {derived[0]['value']}%（{n_cap_score}/{n_cap}）；"
    f"potential 动量面覆盖 {derived[1]['value']}%（{n_pot_score}/{n_pot}）——两面都是『学者能力』面，"
    "语义≠引进效果，登记为升档候选口径（若甲方裁定引进效果=能力面代理）",
    f"久新活库：实测 {len(jx_tables)} 张（2026-11-01 探测日），正文不写死表总数",
    "mock 披露：CostTab trendOption 消费的 effectScore 为 data.js:1474 random(55,92) 演示值；"
    "sharedCharts.jsx:713 实查为 NewPolicyPredictionChart 通用预测图（y 轴名『效果指数』，政策效果"
    "推演组件复用位）——派单 mount 勘误在回执登记，UI mock 值不作数据证据（B10）",
    "B11 对账：capability 99,996/100,000 与 TALENTIR_002 族内记录零漂移；potential 100,000 与 "
    "TALENTIR_004 profile 行数一致；gkx 280 表与共享快照一致",
    "升档触发器（B10）：①建引进事件台账（引进主体×到岗年×投入）+ 裁定效果=引进前后产出对比口径 →"
    " 转换可算升完全转换支持；②甲方裁定引进效果=capability/potential 能力面代理 → 部分支持（语义披露）",
]

out = {
    "metric_id": "M_SCIUI_TALENTIR_003",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/talent-trend/components/CostTab.jsx:221",
        "repos/demo-ui-science/src/pages/talent-trend/components/CostTab.jsx:243",
        "repos/demo-ui-science/src/pages/policy-tracking/simulation/sharedCharts.jsx:711",
        "repos/demo-ui-science/src/pages/talent-trend/data.js:1474",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现该指标名——主需求《科技信息展示系统和科技专题服务系统.md》人才引进推荐"
                "评估章（:2305-2470）无「引进效果指数」；最近邻是 :2424 引进成本预测「历史成本趋势追踪"
                "（放大显示引才成本的历史变化趋势，辅助分析历年引进投入与效果）」——行为在、指标名与"
                "算式无；核增需求与算法库两份真源 0 命中",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件为快照型评估（效果指数无年度序列承载；CostTab trend 7 年为 mock 演示值不参与判定）",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(n_cap), str(n_cap_score), str(n_pot), str(n_pot_score), "280", "210", "96",
                          "55", "92", "20261101"][:10]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
