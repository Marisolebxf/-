#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_034 碳强度改善幅度（政策后）· 三源探针脚本（S3-03 Lane 2）。

含义：多维度效果评估（DS-12）环境维指标「碳强度改善」——政策实施后区域碳排放强度
（CO₂排放量/GDP，吨CO₂/万元）较政策前的下降幅度（%）。
官方口径：碳排放强度 = 二氧化碳排放量 ÷ GDP（国家统计局/发改委 R1/R2）；
「改善幅度」= (强度_前 − 强度_后)/强度_前。
UI：repos/demo-ui-science/src/pages/policy-tracking/policyData.js:1866
（multiDimensionEvalData.dimensions[environment].indicators[0] '碳强度改善' score 70，
  环境维总分 72；消费方 simulation/estimate/EstimateWorkbench.jsx:614/627 四维雷达+分项柱，
  MockBadge 标注演示）。

三源实况（全部实探，2026-11-01）：
- gkx：280 表名扫 energy|carbon|emission|co2|green|pollut 0 表命中；全库列扫
  energy|carbon|emission|co2|power_consum|electric 仅命中材料计算（energy_above_hull/
  formation_energy_per_atom 材料科学虚拟结构能）与分子光谱（collision_energy）——
  语义完全错位；无能源消费/碳排放序列。
- dev：四 schema 表名扫 energy|carbon|emission|fund|eco|green|environment 仅命中推荐类
  残留表（非能耗面）；列扫 energy|carbon|emission|co2 0 列命中。
- 久新：203 表名扫 energy|carbon|emission 0 表命中（技术分析面无环境序列）。
依赖「区域碳排放序列（或能源消费序列×排放因子）+ GDP 序列 + 政策前后窗口」，三源零承载 → 完全不支持。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_034_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())  # B5
facts["gkx_table_count"] = len(gkx_tables)
energy_pat = re.compile(r"energy|carbon|emission|co2|green|pollut|environment|能耗", re.I)
facts["gkx_energy_like_tables"] = [t for t in gkx_tables if energy_pat.search(t)]

# 全库列扫（ORDER BY，B5）：能耗/碳排语义列
col_hits = qg(
    "SELECT table_name, column_name FROM information_schema.columns "
    "WHERE table_schema='gkx' AND (column_name REGEXP 'energy|carbon|emission|co2|power_consum|electric' "
    "OR column_name LIKE '%能耗%') ORDER BY table_name, column_name")
facts["gkx_energy_col_hits"] = [[r[0], r[1]] for r in col_hits]

# gkx 全库 GDP/产值序列候选（分母侧）
gdp_hits = qg(
    "SELECT table_name, column_name FROM information_schema.columns "
    "WHERE table_schema='gkx' AND column_name REGEXP '^gdp|gross_domestic|output_value' "
    "ORDER BY table_name, column_name")
facts["gkx_gdp_col_hits"] = [[r[0], r[1]] for r in gdp_hits]

# 政策文本叙述面：碳/低碳/绿色 词命中（政策意图声明非排放序列）
facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])
for word, key in [("碳排放", "gkx_policy_text_carbon_rows"), ("低碳", "gkx_policy_text_lowcarbon_rows"),
                  ("绿色发展", "gkx_policy_text_green_rows")]:
    facts[key] = int(qg(
        f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,''),IFNULL(keypoints,'')) LIKE '%{word}%'")[0][0])

# 政策窗口锚（政策前后窗口的政策侧时点）
py = qg("SELECT publish_year, COUNT(*) FROM gkx.dwd_policy_base WHERE publish_year REGEXP '^(19|20)[0-9]{2}$' "
        "GROUP BY publish_year ORDER BY publish_year DESC LIMIT 6")
facts["gkx_policy_by_year_top6"] = [[r[0], int(r[1])] for r in py]

# ============ dev ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()
lcur.execute("SELECT TABLE_SCHEMA, TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA IN "
             "('gkxlumenx_dwd','gkxlumenx_ods','gkxlumenx_ads','gkxlumenx_dim') AND TABLE_NAME REGEXP "
             "'energy|carbon|emission|co2|eco|green|environment' ORDER BY TABLE_SCHEMA, TABLE_NAME")
facts["dev_energy_like_tables"] = [[r[0], r[1]] for r in lcur.fetchall()]
lcur.execute("SELECT table_schema, table_name, column_name FROM information_schema.columns WHERE "
             "table_schema IN ('gkxlumenx_dwd','gkxlumenx_ods','gkxlumenx_ads') AND column_name REGEXP "
             "'energy|carbon|emission|co2' ORDER BY table_schema, table_name, column_name")
facts["dev_energy_col_hits"] = [[r[0], r[1], r[2]] for r in lcur.fetchall()]
lconn.close()

# ============ jiuxin ============
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
    jx_tables = sorted(r[0] for r in jcur.fetchall())  # B5
    facts["jiuxin_table_count"] = len(jx_tables)
    facts["jiuxin_energy_like_tables"] = [t for t in jx_tables if energy_pat.search(t)]
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)
    notes.append("久新连接失败按未取证登记（B4），不参与判档数字")

# ================= 派生（叙述面边界读数，非指标值） =================
derived.append({
    "key": "gkx_policy_text_lowcarbon_share_pct",
    "value": round(100.0 * facts["gkx_policy_text_lowcarbon_rows"] / facts["gkx_policy_rows"], 4),
    "numerator": facts["gkx_policy_text_lowcarbon_rows"],
    "denominator": facts["gkx_policy_rows"],
    "note": "分子=文本含「低碳」的政策行数（title+content+keypoints 拼串 LIKE），分母=gkx.dwd_policy_base "
            "全表 20,000 行；同表同池（B3）；语义=低碳叙事覆盖面（政策意图声明），不是碳排放序列",
})

# ================= absence_probe =================
absence += [
    {"probe": "gkx 能源消费/碳排放序列面",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx；280 表名扫 energy|carbon|emission|co2|green|pollut|environment",
     "hits": len(facts["gkx_energy_like_tables"]),
     "hit_detail": "0 表命中——无任何能源消费/碳排放/环境序列表"},
    {"probe": "gkx 全库能耗/碳排语义列",
     "source": "gkx",
     "sql": "information_schema.columns 扫 energy|carbon|emission|co2|power_consum|electric（ORDER BY，B5）",
     "hits": len(facts["gkx_energy_col_hits"]),
     "hit_detail": "仅 6 列命中且全部语义错位：dwd_material_virtual_structure(.bak).energy_above_hull/"
                   "formation_energy_per_atom（材料科学虚拟结构的形成能/凸包能）与 dwd_molecular_spectrum"
                   "(.bak).collision_energy（分子光谱碰撞能）——物理化学计算字段，非能源消费/碳排放"},
    {"probe": "gkx 区域 GDP 序列（强度分母侧）",
     "source": "gkx",
     "sql": "information_schema.columns 扫 ^gdp|gross_domestic|output_value（ORDER BY，B5）",
     "hits": len(facts["gkx_gdp_col_hits"]),
     "hit_detail": "0 列命中——区域 GDP 序列亦无承载（分子分母双缺）"},
    {"probe": "dev 能耗/碳排面",
     "source": "dev",
     "sql": "四 schema 表名+列名双扫 energy|carbon|emission|co2（ORDER BY）",
     "hits": len(facts["dev_energy_like_tables"]) + len(facts["dev_energy_col_hits"]),
     "hit_detail": "表名命中仅为推荐类残留（chain_layout_recommend/entity_recognition/svc_*_recommend——"
                   "表名含 eco/green 子串的推荐表，非能耗面）；列名 0 命中"},
    {"probe": "久新碳排放/能耗面",
     "source": "jiuxin",
     "sql": "SHOW TABLES；203 表名扫 energy|carbon|emission|co2|green|pollut|environment",
     "hits": len(facts.get("jiuxin_energy_like_tables", [])),
     "hit_detail": "0 表命中——久新 203 张 ads_* 全为技术/人才/机构分析面，无环境序列"},
    {"probe": "需求原文「碳强度/碳排放」定义段",
     "source": "doc",
     "sql": "rg 碳强度 三份需求真源",
     "hits": 0,
     "hit_detail": "「碳强度/碳排放」三份需求真源 0 命中；主需求 1.1.1.1.4.2.3.1.4 多维度效果评估段仅枚举"
                   "「从经济、社会、环境、创新等多个维度对政策效果进行评估」——环境维被点名但无任何指标"
                   "定义（无碳强度口径、无窗口、无数据源）；核增需求与算法库 0 命中"},
]

support = "完全不支持"

notes += [
    "判档：碳强度改善幅度 = (碳强度_政策前 − 碳强度_政策后)/碳强度_政策前，碳强度=CO₂排放量/GDP"
    "（官方口径 R1/R2）。依赖：①区域碳排放序列（或能源消费×排放因子）②区域 GDP 序列（不变价）"
    "③政策前后窗口+处理组。①②三源零承载（gkx 全库唯一 energy 列是材料形成能、dev/gkx GDP 列 0 命中、"
    "久新 203 表无环境面），③仅有政策发布年——分母分子双缺，判完全不支持",
    "代理面边界：政策文本「低碳」命中率是叙事面（政策谈双碳目标），不是排放结果；把叙事强度当碳强度改善"
    "会犯「意图≠结果」的语义错误",
    "mock 披露：policyData.js:1866「碳强度改善 70 分」是 multiDimensionEvalData 环境维 indicators 的"
    "前端演示常量（0-100 评分形态，演示值，不参与支持度结论）；消费方 EstimateWorkbench.jsx 四维雷达",
    "B11 对账：gkx 政策 20,000 行与共享快照零漂移；gkx energy 列扫与 _probe_lane2_s303_out.json "
    "gkx_energy_col_hits 零漂移",
    "升档触发器（B10）：接入区域能源消费/碳排放序列（统计侧能源平衡表或碳市场数据）+ 区域 GDP 序列 → "
    "强度差分运算平凡，可升完全转换支持；若甲方接受全国碳强度官方序列外接 → 需统计局/发改委数据源且"
    "粒度是全国年度非政策区域，单独立项",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_034",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:1866",
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:1863",
        "repos/demo-ui-science/src/pages/policy-tracking/simulation/estimate/EstimateWorkbench.jsx:614",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「碳强度」三份需求真源 0 命中；主需求 1.1.1.1.4.2.3.1.4 多维度效果评估枚举「环境」维度"
                "（无指标条目、无定义方法）；UI 层 multiDimensionEvalData 环境维演示常量",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["政策前碳强度基期年", "政策后碳强度观测年"],
    "base_years_note": "本件无碳排放/能源序列可算（三源零承载）；政策侧 publish_year（varchar）仅能界定政策"
                       "发布年分布（2021:2,120 / 2020:2,402 / 2019:2,035…），不构成碳强度基期",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts["gkx_policy_rows"]), str(facts["gkx_policy_text_lowcarbon_rows"]),
                          str(facts["gkx_policy_text_carbon_rows"]), "280", "203"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
