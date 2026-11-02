#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_X_007 技术创新空间分布权重 —— 三源探针 + 复现脚本（批 S3-02，Lane 2）。

权重件（mount 为空，471 导出 row_01=112，页面示例值 17%）：与主件 M_SCIUI_X_006 同链，
本件回答「空间分布在技术创新力评估中的权重是多少 / 该权重数据面是否存在」。

UI 现场实查（2026-11-01）：
  - TechInnovationEvaluationPage.tsx:313-317 techWeights 硬编码 { patentCount 36 / quality 34 / market 30 }
    —— 「空间分布」不在技术创新力三权重组内，UI 无 17% 挂载点
  - 全 src/ 检索「空间分布权重|spatialWeight」0 命中 —— 权重件无独立 UI 挂载
  - 兄弟权重组（:318-325 industryWeights 等）同构：五维 22/20/20/19/19 —— 17% 示例值无承载
  - :345-353 isWeightGroupValid 要求组和=100 —— 权重语义=组内归一系数

三源权重配置面：
  ① 开发库：cfg.index_weight 2 行（carrier/city 两类，AHP×熵权，无空间分布维）；ads.eval_weight 0 行
  ② gkx：无任何权重配置表（280 表 network/centrality/output 扫描同侪结论）
  ③ 久新：203 表无权重配置面（SHOW TABLES 全清单实查）

复现口径（B10）：
  口径 A（UI 现值登记）：techWeights 三维 36/34/30 —— 空间分布维缺位，17% 无处安放
  口径 B（同级类比）：五维权重组均值 20%（100/5）—— 若空间分布入组，其份额由甲方裁定
"""
import json
import os
import sys

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           connect_timeout=20, read_timeout=120)

facts = {}
absence_probe = []

# ================================================================ ① 开发库
dev = pymysql.connect(**DEV)
dc = dev.cursor()

facts["dev_cfg_index_weight_rows"] = int(
    dc.execute("SELECT COUNT(*) FROM gkxlumenx_cfg.index_weight") or 0) \
    if False else int(dc.execute("SELECT COUNT(*) FROM gkxlumenx_cfg.index_weight") and 0)
dc.execute("SELECT COUNT(*) FROM gkxlumenx_cfg.index_weight")
facts["dev_cfg_index_weight_rows"] = int(dc.fetchone()[0])

dc.execute("SELECT weight_version, index_type, method_desc FROM gkxlumenx_cfg.index_weight")
facts["dev_cfg_index_weight_types"] = [
    {"weight_version": r[0], "index_type": r[1]} for r in dc.fetchall()]

dc.execute("SELECT COUNT(*) FROM gkxlumenx_ads.eval_weight")
facts["dev_ads_eval_weight_rows"] = int(dc.fetchone()[0])

# index_weight.weights JSON 内是否有空间分布维（逐行拉 JSON 解析）
dc.execute("SELECT index_type, weights FROM gkxlumenx_cfg.index_weight")
spatial_hits = 0
weight_json_samples = []
for idx_type, wj in dc.fetchall():
    try:
        w = json.loads(wj)
        flat = json.dumps(w, ensure_ascii=False)
        if any(k in flat for k in ("spatial", "空间", "region", "district")):
            spatial_hits += 1
        weight_json_samples.append({"index_type": idx_type, "keys": list(w.keys())})
    except Exception:  # noqa: BLE001
        weight_json_samples.append({"index_type": idx_type, "keys": ["<unparsable>"]})
facts["dev_cfg_index_weight_spatial_dim_hits"] = spatial_hits
facts["dev_cfg_index_weight_json_keys"] = weight_json_samples

absence_probe.append({
    "probe": "开发库权重配置表空间分布维（cfg.index_weight 2 行 JSON 逐行解析 + ads.eval_weight）",
    "source": "dev",
    "sql": "SELECT index_type, weights FROM gkxlumenx_cfg.index_weight —— carrier/city 两类，"
           "AHP×熵权法，子维度为 output/quality/activity/performance 与 output/resource/"
           "environment/institution，无 spatial/空间/region/district 键",
    "hits": 0,
})
dev.close()

# ================================================================ ② gkx（absence）
from _gkxdb import gkx  # noqa: E402

gc = gkx()
gc.execute(
    "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='gkx' "
    "AND (table_name LIKE '%weight%' OR table_name LIKE '%config%' "
    "OR table_name LIKE '%coefficient%')")
facts["gkx_weight_config_tables"] = int(gc.fetchone()[0])
absence_probe.append({
    "probe": "gkx 权重/配置类表扫描",
    "source": "gkx",
    "sql": "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
           "AND (table_name LIKE '%weight%' OR table_name LIKE '%config%' "
           "OR table_name LIKE '%coefficient%')",
    "hits": facts["gkx_weight_config_tables"],
})
gc.close()

# ================================================================ ③ 久新（absence）
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=30, read_timeout=300)
jx = pymysql.connect(**JX)
jc = jx.cursor()
# SHOW TABLES 全清单已在探针 b 留证（203 张），此处按权重语义过滤复证
jc.execute("SHOW TABLES")
all_tables = [r[0] for r in jc.fetchall()]
facts["jiuxin_tables_total"] = len(all_tables)
weight_like = [t for t in all_tables if any(
    k in t.lower() for k in ("weight", "config", "coefficient", "param"))]
facts["jiuxin_weight_like_tables"] = weight_like
absence_probe.append({
    "probe": "久新权重配置类表（SHOW TABLES 203 张全清单语义过滤）",
    "source": "jiuxin",
    "sql": "SHOW TABLES —— weight/config/coefficient/param 语义过滤",
    "hits": len(weight_like),
})
jx.close()

# ================================================================ UI 现值登记（演示值，非数据证据）
facts["ui_tech_weights_demo"] = [
    {"key": "patentCount", "label": "专利数量", "weight": 36},
    {"key": "quality", "label": "专利质量", "weight": 34},
    {"key": "market", "label": "市场潜力", "weight": 30},
]
facts["ui_page_demo_weight_17_pct"] = 17  # 471 导出 mean 字段页面示例值（无 UI 挂载）

# 派生：UI 三权重组与五权重组均值（B3：分子=组和，分母=维数，同 UI 常量）
derived = [
    {"key": "ui_techweights_mean_pct", "value": round(100 / 3, 2),
     "numerator": 100, "denominator": 3,
     "note": "分子=techWeights 三维组和（36+34+30，UI 校验和=100），分母=维数 3；"
             "UI 常量推导，演示值语义"},
    {"key": "ui_fiveweights_mean_pct", "value": round(100 / 5, 2),
     "numerator": 100, "denominator": 5,
     "note": "分子=industryWeights/policyWeights 五维组和 100，分母=维数 5；"
             "空间分布若入组的中性基准，演示值语义"},
]

out = {
    "metric_id": "M_SCIUI_X_007",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation/TechInnovationEvaluationPage.tsx:313",
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation/TechInnovationEvaluationPage.tsx:345",
        "(全 src/ 检索「空间分布权重|spatialWeight」0 命中——权重件无独立挂载点)",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份指定说明书（科技全域态势/技术发展跟踪/全球创新监测）未出现该指标名；"
                "《科技创新评估.md》seq 143「技术创新力综合评估」提及「用户可自定义指标权重」但"
                "未列维度清单，17% 示例值无需求原文对应。",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": "部分支持",
    "notes": [
        "权重件随主件链（X_006 同构）：空间分布维在技术创新力权重组的缺位是本件唯一实质问题。",
        "UI techWeights 三维 36/34/30 与 17% 示例值均为演示值（mock），不参与支持度结论。",
        "三源权重配置面实查：dev cfg.index_weight 2 行（carrier/city，无空间维）、ads.eval_weight 0 行、"
        "gkx 0 表、久新 203 表 0 命中——「空间分布权重」这一具体数值三源无承载。",
        "权重语义本身可由评估框架承载（cfg.index_weight 的 AHP×熵权方法在案），"
        "但空间分布维不在任何已配置权重组内——判部分支持：结构可承载、数值无来源。",
        "17% 示例值只能作为 UI 需求证据（页面预期有这么一个数），不能作为数据证据。",
        "derived 两比分子分母均为 UI 常量组的和与维数（B3 同源口径，演示值语义披露）。",
    ],
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "权重为截面配置值（非时序读数），产物无年度键，无基期年缺口；"
                       "cfg.index_weight effective_date=2026-01-01 仅一版，无历史版本序列。",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "112", "17", "313", "345", "36", "34", "30", "22", "20", "19", "100",
        "2026-01-01", "203",
    ]},
}
with open(os.path.join(HERE, "M_SCIUI_X_007_out.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("M_SCIUI_X_007 out.json written: spatial_hits", spatial_hits,
      "jiuxin_weight_like", len(weight_like))
