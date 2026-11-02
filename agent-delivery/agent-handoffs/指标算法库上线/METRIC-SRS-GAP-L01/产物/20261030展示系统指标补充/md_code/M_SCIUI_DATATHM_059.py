#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_059 资源质量平均分 · 三源探针脚本（S3-05 L2 质量组）。

含义：总体视窗·资源来源分析与详情·来源结构组成表格的「质量均分」列（avgQuality，分组级均值）
与来源可靠性卡片区「质量均分」读数。挂载：ResourceSourceAnalysisDetail.jsx:264（表格列）/:521-522（卡片读数）。
mock 源：mockData.js:160-230 sourceTypes 5 来源各带 avgQuality（91/94/93/86/84）+
mockData.js:14-21 resourceThemeDistribution 7 主题 avgQuality（92/88/95/86/84/91/89）。

判档路径（口径=「来源分组内资源质量评分的均值」——稽核结果面的聚合读数）：
- 与 058 同根：资源级质量稽核结果面（资源×评分）三源零承载 → 分组均值无从聚合；
- dev quality/score 词族唯一命中 cfg.degrade_switch（运维开关，语义排除）；gkx 0 命中；
  久新 value 命中 1 张商业化仿真面（语义排除）；
- mock 三套演示值互不对账（asd 资源级 / sourceTypes 来源级 / themeDistribution 主题级），
  不作均值原料；
- 判完全不支持（聚合读数随基座面缺位而缺位）。

B11 锚：三源表数 542/280/210（快照）+212（live）；词族 = _probe_s304_l7_quality_out.json。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_059_out.json")
SNAP7 = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s304_l7_quality_out.json")

snap = json.load(open(SNAP7, encoding="utf-8"))
probe = json.load(open(PROBE, encoding="utf-8"))

# asd 12 行资源级 qualityScore 按 channel 分组实算（mockData.js:134-145，校验用，不作源）
asd_by_channel = {
    "科研院所": [95, 87],        # asd-001/006 → 均值 91
    "高等院校": [93, 80],        # asd-002/009 → 均值 86.5
    "企业": [89, 82, 86],        # asd-003/007/011 → 均值 ≈85.67
    "第三方平台": [91, 94, 85],  # asd-004/008/012 → 均值 90
    "政府部门": [88, 92],        # asd-005/010 → 均值 90
}
asd_by_theme_field = {
    "基础科学": [95, 94, 80],  # asd-001/008/009 → 均值 ≈89.67
    "医学健康": [93],          # asd-002 → 93
}
source_types_avg = {"国内数据库": 91, "国外数据库": 94, "科研院所": 93, "企业": 86, "开源平台": 84}
theme_avg = {"基础科学": 92, "医学健康": 95}

# 分组键对齐核（channel 维 vs sourceTypes 维）
asd_channels = sorted(asd_by_channel)
source_type_names = sorted(source_types_avg)
key_overlap = sorted(set(asd_channels) & set(source_type_names))  # [企业, 科研院所]

facts = {
    "dev_table_count": sum(snap["dev"]["schema_table_counts"].values()),
    "gkx_table_count": snap["gkx"]["table_count"],
    "jiuxin_table_count_snapshot_20261101": len(snap["jiuxin"]["tables"]),
    "jiuxin_table_count_live_20261102": probe["jiuxin_table_count_live"],
    "dev_reliability_like_tables": probe["dev_reliability_like_tables"],  # []
    "dev_value_like_tables": probe["dev_value_like_tables"],  # [cfg.degrade_switch]
    "gkx_reliability_like_tables": probe["gkx_reliability_like_tables"],  # []
    "gkx_value_like_tables": probe["gkx_value_like_tables"],  # []
    "jiuxin_value_like_tables": probe["jiuxin_value_like_tables"],  # [商业化仿真面]
    "dev_degrade_switch_semantic": "gkxlumenx_cfg.degrade_switch 运维降级开关配置表，无资源质量字段——语义排除",
    "jiuxin_value_table_semantic": "ads_technology_commercial_value_simulation 商业化价值仿真面，语义≠质量稽核——语义排除",
    # UI 挂载证据
    "ui_mount_table_column": "ResourceSourceAnalysisDetail.jsx:263-269 质量均分列（avgQuality，Tag 色：≥90 success/≥85 processing/else warning）",
    "ui_mount_reliability_card": "ResourceSourceAnalysisDetail.jsx:521-522 可靠性卡片「质量均分」读数（s.avgQuality）",
    # mock 演示值（结构证据，不作数据源）
    "ui_mock_source_types_avg_quality": source_types_avg,
    "ui_mock_theme_avg_quality": theme_avg,
    # mock 三套演示值互不对账披露（asd 资源级 vs sourceTypes 来源级 vs themeDistribution 主题级）
    "ui_mock_asd_channels_sorted": asd_channels,
    "ui_mock_source_type_names_sorted": source_type_names,
    "ui_mock_key_overlap_sorted": key_overlap,
    "ui_mock_inconsistency_notes": [
        "分组键不对齐：asd 明细按 channel 分组为 高等院校/企业/第三方平台/政府部门/科研院所，"
        "sourceTypes 五维为 国内数据库/国外数据库/科研院所/企业/开源平台——交集仅 [企业, 科研院所] 2 项",
        "交集内数值不等：科研院所 asd 实算均值 91 vs sourceTypes avgQuality 93；"
        "企业 asd 实算均值 ≈85.67 vs 86",
        "主题级也不等：基础科学 asd 实算均值 ≈89.67 vs themeDistribution avgQuality 92；"
        "医学健康 93 vs 95",
        "结论：三套手写常量互不聚合对账，均不作均值原料（B10）",
    ],
}

derived = [{
    "key": "resource_quality_avg_score",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『资源质量平均分』= 分组内资源质量评分均值——需资源级质量稽核结果面（058 同根），"
            "三源零承载（dev 开关表语义排除/gkx 0/久新仿真面语义排除）。mock 三套演示值互不对账，"
            "不作均值原料。按 B10 留空即负结论登记",
}]

absence_probe = [
    {"probe": "dev 资源质量稽核结果面与评分列（quality/score/avg/reliability 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表，L7 族探针 2026-11-02）",
     "hits": 0,
     "hit_detail": "reliability []；value 唯一命中 cfg.degrade_switch（运维开关，语义排除）；dev 无资源级评分列，无来源分组聚合面"},
    {"probe": "gkx 资源质量评分面（同词族）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）词族扫（经 _gkxdb.py）",
     "hits": 0,
     "hit_detail": "命中 []——要素明细库无质量评分面"},
    {"probe": "久新资源质量评分面（同词族）",
     "source": "jiuxin",
     "sql": "SHOW TABLES（2026-11-02 live，212 表）词族扫",
     "hits": 0,
     "hit_detail": "quality/reliability 0 命中；value 唯一命中商业化仿真面（语义排除）——ads_* 无资源质量评分结果表"},
    {"probe": "需求原文「质量均分/平均质量」定义段",
     "source": "doc",
     "sql": "rg 质量均分|平均质量|质量评分 三份需求真源",
     "hits": 0,
     "hit_detail": "三份说明书未出现「质量均分/资源质量平均分」字面；语义锚同 058（seq 352 属性项/:2629 工程前提）；"
                   "SRS seq 357「质量状况」为分区属性项（分布语义非均值）；均值口径（分组键/加权否）无定义"},
]

notes = [
    "判档：资源质量平均分是稽核结果面的聚合读数——基座面（资源×评分）三源零承载（与 058 同根）"
    "→ 聚合无从执行 → 完全不支持；mock 三套常量互不对账（分组键不对齐+交集内数值不等），不作均值原料",
    "UI 语义核：ResourceSourceAnalysisDetail 的「质量均分」有两处读数位——来源结构组成表格列（:263-269，"
    "按来源分组）与来源可靠性卡片区（:521-522，同值复用）；分组键=sourceTypes 五维",
    "mock 披露（三套演示值互不对账）：①asd 资源级 12 行（channel 分组 高等院校/企业/第三方平台/政府部门/科研院所）；"
    "②sourceTypes 来源级 5 值（91/94/93/86/84）；③themeDistribution 主题级 7 值（92/88/95/86/84/91/89）——"
    "①②分组键交集仅 [企业, 科研院所] 且交集内数值不等（91≠93；≈85.67≠86）；①③主题级也不等（≈89.67≠92；93≠95）",
    "B11 对账：三源表数 542/280/210+212；质量词族与 _probe_s304_l7_quality_out.json 逐键一致（与 058/017/006 共享同一探针）",
    "升档触发器（B10）：与 058 共用——①质量稽核结果面立项 → 资源级评分可聚合（AVG GROUP BY 来源/主题）"
    "→ 升完全直接支持；②自建规则跑批+评分登记 → 升完全转换支持（分组键与加权规则须登记）；③维持现状 → 完全不支持",
    "权威口径参照（R2 Dataphin）：项目/数据源质量分 = sum(表权重×表质量分)/sum(表权重)——聚合均值有加权先例，"
    "正式版须裁定等权（AVG）还是加权（按资源规模/权重）",
]

support = "完全不支持"

out = {
    "metric_id": "M_SCIUI_DATATHM_059",
    "batch": "S3-05",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/components/ResourceSourceAnalysisDetail.jsx:264",
        "repos/demo-ui-science/src/pages/data-resources/components/ResourceSourceAnalysisDetail.jsx:522",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:170",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现「质量均分/资源质量平均分」字面；语义锚同 058（seq 352 属性项 + "
                ":2629 质量评估算法工程前提）；SRS seq 357「质量状况」为分区属性项",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["质量评分时间序列整体缺承载（无稽核面即无期次均值）"],
    "base_years_note": "均值为稽核快照的聚合读数，无期次序列需求承载",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["542", "280", "210", "212", "91", "94", "93", "86", "84", "95", "264", "522"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
