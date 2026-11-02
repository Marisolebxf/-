#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_007 创新指数提升 · 三源探针与复现脚本（S3-02 Lane 6）。

含义：科技政策实施后区域创新指数上涨的幅度（分）——回答'政策有没有把创新水平拉起来'。
裁定 NEW：旧创新指数 MD（M_INNOV_* 族）非政策对比语境；本件语义=政策效果推演语境下的
创新指数差分（仿真结果指标，policyData.js:1832 innovationIndex '创新指数提升' unit '分'）。

三源实况（全部实探，2026-11-01）：
- gkx：280 表扫 innov/index 命中 dwd_dim_index_*（3 张维度表）+ dwd_macro_index_data
  （20,000 行宏观指标）。macro 面 index_code 三域：gmjj（国民经济 10,046）/dwjj（对外经济 5,129）/
  a77（国际高技术制造业 R&D 代维 3,000+）；attribute 表 867 码无一含『创新指数』；
  a77 代维的区域分布是国际国别码（054/049/484…），深圳仅 30 码 25 行零创新语义——
  『区域创新指数』结果面在 gkx 无承载。
- dev：policy_effect_eval.innovation_promotion_score 列存在（创新促进得分——语义最贴）但全表 0 行；
  policy_simulation_result（仿真结果）0 行。
- 久新：ads_geo_yearly_index 0 行（Lane4 探针实测）；ads_geo_yearly_metrics 有论文/专利/人才
  年度指标但无『创新指数』合成面（schema 文档在案）。
判档：部分支持——指数的输入维（论文/专利/人才等创新活动指标）三源有承载（久新 geo 年度指标
816,120 行级），但『创新指数』合成口径（指标体系+权重）无任何源承载，且政策×指数的因果
归因（提升幅度）依赖反事实框架（DID/合成控制），处理组划分所需的『政策实施单元×时间』
在库内无结构化承载。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_007_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

# ============ ① gkx：宏观指数面（创新指数承载探查） ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
facts["gkx_index_like_tables"] = [t for t in gkx_tables if re.search(r"innov|index", t, re.I)]
# 宏观指数表结构域
facts["gkx_macro_index_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_macro_index_data")[0][0])
facts["gkx_macro_index_code_domains"] = [[r[0], int(r[1])] for r in qg(
    "SELECT SUBSTRING_INDEX(index_code,'_',1), COUNT(*) FROM gkx.dwd_macro_index_data "
    "GROUP BY 1 ORDER BY 2 DESC LIMIT 5")]
facts["gkx_dim_index_attribute_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_dim_index_attribute")[0][0])
# attribute 表『创新指数』语义扫
facts["gkx_attribute_innovation_index_names"] = [r[0] for r in qg(
    "SELECT index_name FROM gkx.dwd_dim_index_attribute WHERE index_name LIKE '%创新指数%' OR index_name LIKE '%创新能力%'")]
facts["gkx_attribute_rd_names_count"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_dim_index_attribute WHERE index_name LIKE '%R&D%' OR index_name LIKE '%研发%'")[0][0])
# a77 高技术 R&D 代维的区域语义（国际国别码非国内区域）
facts["gkx_a77_area_sample"] = [[r[0], int(r[1])] for r in qg(
    "SELECT area_code, COUNT(*) FROM gkx.dwd_macro_index_data WHERE index_code REGEXP '^a77' "
    "GROUP BY area_code ORDER BY 2 DESC LIMIT 8")]
facts["gkx_sz_macro_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_macro_index_data WHERE area_code LIKE '4403%'")[0][0])
# 政策文本创新指数提及（叙述面）
facts["gkx_policy_text_cxzs_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,'')) LIKE '%创新指数%'")[0][0])

# ============ ② dev：仿真/效果面结构（0 行在案） ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()
# policy_effect_eval 结构（创新促进得分列）+ 行数
for t in ["policy_effect_eval", "policy_simulation_result", "policy_intensity_eval"]:
    try:
        cols = [r[0] for r in ql(f"SHOW COLUMNS FROM `{t}`")]
        rows = int(ql(f"SELECT COUNT(*) FROM `{t}`")[0][0])
        facts[f"dev_{t}"] = {"cols": cols, "rows": rows}
    except Exception as e:  # noqa: BLE001
        facts[f"dev_{t}"] = f"error: {e}"
lconn.close()

# ============ ③ 久新：指数结果面（复用 Lane4 同日探针，本件补连） ============
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
    facts["jiuxin_geo_yearly_index_rows"] = int(qj("SELECT COUNT(*) FROM ads_geo_yearly_index")[0][0])
    facts["jiuxin_geo_yearly_metrics_rows"] = int(qj("SELECT COUNT(*) FROM ads_geo_yearly_metrics")[0][0])
    # geo 指标列族（创新输入维探查）
    facts["jiuxin_geo_metric_cols"] = [r[0] for r in qj("SHOW COLUMNS FROM ads_geo_yearly_metrics")]
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)
    facts["jiuxin_geo_yearly_index_rows"] = "未取证（连接被锁）——Lane4 探针 _probe_lane4_s302_out.json A5 同日实测 0 行"
    facts["jiuxin_geo_yearly_metrics_rows"] = "未取证（连接被锁）——Lane4 探针 A1-A6 同日实测 171,736 行（四层 location_level）"
    facts["jiuxin_geo_metric_cols"] = "未取证（连接被锁）——schema 文档 2026-10-22-ADS-SCHEMA-5.11.0.md 在案：paper/patent/talent/institution 计数列族"

# ================= 派生（不可算登记 + 输入维覆盖读数） =================
derived.append({
    "key": "policy_innovation_index_uplift",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "不可算——『创新指数』合成口径（指标体系+权重）三源无承载；政策→指数的因果归因"
            "需反事实框架（DID/合成控制），处理组结构（政策实施单元×时间）无承载。"
            "此键留空为负结论登记，不写伪提升值",
})
# gkx 创新代理维覆盖（R&D 类指标码 30+ 个但区域在国际面——证明输入维有码无国内区域覆盖）
derived.append({
    "key": "gkx_rd_indicator_codes_count",
    "value": float(facts["gkx_attribute_rd_names_count"]),
    "numerator": facts["gkx_attribute_rd_names_count"],
    "denominator": facts["gkx_dim_index_attribute_rows"],
    "note": "分子=attribute 表名称含 R&D/研发 的指标码数，分母=attribute 表全量 867 码；"
            "同表同池（B3）；语义=R&D 输入维的码覆盖面（3.5%），且这些码的数值面（a77）"
            "仅国际国别区域有值——国内区域（含深圳）R&D 值无承载",
})

# ================= absence_probe =================
absence += [
    {"probe": "gkx『创新指数』结果面",
     "source": "gkx",
     "sql": "280 表名扫 innov/index + dwd_dim_index_attribute 867 码名称扫『创新指数/创新能力』"
            " + dwd_macro_index_data 三域分布",
     "hits": 0,
     "hit_detail": "表名命中 4 张（3 张 dim 维度表 + macro 数据表）均为宏观统计面非创新指数；"
                   "867 码无一含『创新指数/创新能力』（gkx_attribute_innovation_index_names=[]）；"
                   "macro 三域 gmjj 国民经济 10,046/dwjj 对外经济 5,129/a77 国际高技术 R&D——"
                   "无创新指数合成面"},
    {"probe": "dev 政策效果/仿真结果面",
     "source": "dev",
     "sql": "policy_effect_eval（innovation_promotion_score 列）+ policy_simulation_result 行数",
     "hits": 2,
     "hit_detail": f"policy_effect_eval 列含 innovation_promotion_score（创新促进得分——语义最贴的结构），"
                   f"但全表 {facts['dev_policy_effect_eval']['rows'] if isinstance(facts['dev_policy_effect_eval'], dict) else '?'} 行；"
                   f"policy_simulation_result 同 0 行——结构存在数据空（B4 情形②：补数据可解）"},
    {"probe": "久新指数结果面",
     "source": "jiuxin",
     "sql": "ads_geo_yearly_index COUNT + ads_geo_yearly_metrics 列族核对",
     "hits": 0,
     "hit_detail": "ads_geo_yearly_index（指数结果面候选）Lane4 同日实测 0 行；"
                   "ads_geo_yearly_metrics 171,736 行有 paper/patent/talent/institution 年度计数"
                   "（创新活动输入维）但无指数合成列——输入维有、指数面无"},
    {"probe": "核增需求与 SRS『创新指数提升』定义",
     "source": "doc",
     "sql": "rg 创新指数 核增需求 17 叶 + SRS 政策族 + 主需求",
     "hits": 0,
     "hit_detail": "三份需求真源无『创新指数提升』指标名（主需求 1.1.1.1.4.2.3.1『创新促进等方面』"
                   "语境涵盖）；UI policyData.js:1832（innovationIndex 创新指数提升 分）与 :2067"
                   "（解读报告 mock『创新指数提升约 5 分』）是唯一语义源，均为演示值"},
]

support = "部分支持"

notes += [
    "判档：创新指数提升 = Index(政策后) − Index(政策前)（分）。两个依赖维均缺——"
    "①指数合成口径：三源无任何现成区域创新指数结果面（gkx 宏观面是国民经济统计非创新指数；"
    "dev 效果表 0 行；久新 ads_geo_yearly_index 0 行）；②政策因果归因：处理组结构"
    "（政策实施单元×时间窗）无承载。但输入维（论文/专利/人才年度指标）三源有量"
    "（久新 geo 171,736 行级），合成+归因工程可立项 → 部分支持",
    "裁定 NEW 语境披露：旧创新指数 MD（M_INNOV_IMPACT_FORECAST 等族）是区域创新监测语境"
    "（无政策变量）；本件在政策效果推演语境下要求『政策实施后』的提升幅度——因果语义是新的，"
    "不可直接搬旧判档。旧件可引作指数合成方法的依赖面旁证（R4 区域创新能力四级指标体系）",
    "gkx 宏观面语义边界：a77 系（3,000+ 行）名称是『规模以上高技术制造业 R&D』类——内容确实是"
    "创新活动统计，但区域维是国际国别码（054 印度/049 孟加拉/484 墨西哥/EU…）且深圳仅 30 码"
    "25 行零『创新指数』语义——国内区域的创新统计值无承载，不能当深圳创新指数输入",
    "政策文本叙述面：『创新指数』一词在政策全文命中 6 行（年度 2016-2021 零散）——政策文本"
    "会提及创新指数目标（如某市『全社会研发投入强度达到X%』类表述），但政策文本不是指数数据源",
    "mock 披露：policyData.js:1832 innovationIndex（创新指数提升 分）与 :2067 解读报告"
    "『一年内…创新指数提升约 5 分』均为 Wave0 mock——演示值不参与支持度结论",
    "B11 对账：gkx macro 20,000 行/attribute 867 码与 Lane6 探针 _probe_lane6_gkx_macro*.json "
    "零漂移；久新 geo 指标行数与 Lane4 探针一致",
    "升档触发器（B10）：①构建区域创新指数合成（久新 geo 输入维 + R4 四级指标体系方法）并落地"
    "ads_geo_yearly_index 类结果面 → 指数闭合；②政策实施清单结构化（政策×区域×实施时间窗）+"
    "DID/合成控制归因 → 提升幅度闭合；两者齐备升完全转换支持。若甲方接受『仿真演示模型』"
    "口径（前端 SIMPLE_EFFECT_MODEL 系数）→ 那是 mock 语义，本件不接受",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_007",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:1832",
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:2067",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「创新指数提升」未出现在三份需求真源；主需求 1.1.1.1.4.2.3.1 未出台政策仿真模拟"
                "『预测政策实施后可能产生的效果，包括经济效益、社会影响、创新促进等方面』"
                "是语义源（『创新促进』即本件上位语）；UI mock 实现层给出『分』单位——"
                "暗示指数制（非百分比）口径",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "指数序列不可算（指数面零承载）；久新 geo 输入维年份 2000-2026（27 期）可作未来合成基期",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["20,000", "867", "10,046", "5,129", "30", "25", "6",
                          "171,736", "0", "280", "5"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
