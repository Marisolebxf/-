#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_060 资源质量等级分布 · 三源探针脚本（S3-05 L2 质量组）。

含义：总体视窗·来源分析明细「按质量等级」分组视图（GROUP_OPTIONS 含 qualityLevel 维）——
对归集资源明细按 qualityLevel 枚举做 GROUP BY，产出各等级的资源条数(count)/数据量(volume)分布。
挂载：AccessSourceAnalysisDetail.jsx:62（GROUP_OPTIONS 含 '按质量等级'）/:195-205（groupedData
客户端分组聚合：count 累加 + volume 累加）/:289-296（明细行 qualityLevel 列）/:530-536（分组选择器）。
mock 源：mockData.js:134-145 asd 12 行（qualityLevel 优6/良4/中2，同 058 分布）。

判档路径（口径=「qualityLevel 枚举 × (count, Σvolume) 的分布」——稽核结果面的离散聚合）：
- 与 058 同根：资源级 qualityLevel（稽核结果面）三源零承载 → 枚举分布无从 GROUP BY；
- dev quality/grade/score/reliability 词族唯一命中 cfg.degrade_switch（运维开关，语义排除）；gkx 0 命中；
  久新 value 命中 1 张商业化仿真面（语义排除）；
- mock asd 12 行可算演示分布（优6/良4/中2；volume 优 Σ8100/良 Σ4860/中 Σ1360）——
  但 qualityLevel 为手写常量（无稽核依据），不作分布原料（B10）；
- 判完全不支持（分布读数随基座面缺位而缺位）。

B11 锚：三源表数 542/280/210（快照）+212（live）；词族 = _probe_s304_l7_quality_out.json。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_060_out.json")
SNAP7 = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s304_l7_quality_out.json")

snap = json.load(open(SNAP7, encoding="utf-8"))
probe = json.load(open(PROBE, encoding="utf-8"))

# asd 12 行按 qualityLevel 分组实算（mockData.js:134-145 逐行解析，校验用，不作源）
import re
MOCK = "/Users/samuel_tang/my_project/gkx-lumen/repos/demo-ui-science/src/pages/data-resources/mockData.js"
mock_src = open(MOCK, encoding="utf-8").read()
mock_lines = mock_src.split("\n")
asd_rows = []
for l in mock_lines[133:145]:
    m_lvl = re.search(r"qualityLevel: '(.+?)'", l)
    m_vol = re.search(r"volume: (\d+)", l)
    m_id = re.search(r"id: '(asd-\d+)'", l)
    if m_lvl and m_vol and m_id:
        asd_rows.append((m_id.group(1), m_lvl.group(1), int(m_vol.group(1))))
assert len(asd_rows) == 12, len(asd_rows)
dist = {}
for _id, lvl, vol in asd_rows:
    c, v = dist.get(lvl, (0, 0))
    dist[lvl] = (c + 1, v + vol)
mock_dist = {lvl: {"count": c, "volume": v} for lvl, (c, v) in sorted(dist.items())}
mock_dist_check = {"优": {"count": 5, "volume": 7600}, "中": {"count": 2, "volume": 1360}, "良": {"count": 5, "volume": 5760}}
assert mock_dist == mock_dist_check, mock_dist

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
    "ui_mount_group_option": "AccessSourceAnalysisDetail.jsx:62 GROUP_OPTIONS 含 {value:'qualityLevel', label:'按质量等级'}",
    "ui_mount_group_aggregation": "AccessSourceAnalysisDetail.jsx:195-205 groupedData 客户端分组：按 r[groupBy] 建 map，count += 1 与 volume += r.volume 累加，按 volume 降序",
    "ui_mount_detail_column": "AccessSourceAnalysisDetail.jsx:288-296 明细行质量等级列（Tag QUALITY_COLOR[t] · qualityScore）",
    "ui_mount_group_select": "AccessSourceAnalysisDetail.jsx:530-536 分组选择器（含按质量等级）作用于明细表",
    "ui_mount_quality_filter": "AccessSourceAnalysisDetail.jsx:520-526 质量筛选器（filters.quality → r.qualityLevel 等值过滤）",
    # mock 演示分布（实算，结构证据，不作源）
    "ui_mock_quality_level_dist": mock_dist,
    "ui_mock_dist_note": "asd 12 行按 qualityLevel 实算：优 5 条 Σ7600 / 良 5 条 Σ5760 / 中 2 条 Σ1360（无差档样本）",
}

derived = [{
    "key": "resource_quality_level_distribution",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『资源质量等级分布』= qualityLevel 枚举 × (count, Σvolume) GROUP BY——需资源级质量等级列"
            "（058 同根），三源零承载（dev 开关表语义排除/gkx 0/久新仿真面语义排除）。mock 12 行等级为"
            "手写常量（无稽核依据），不作分布原料。按 B10 留空即负结论登记",
}]

absence_probe = [
    {"probe": "dev 资源质量等级列与稽核结果面（quality/grade/score/reliability 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表，L7 族探针 2026-11-02）",
     "hits": 0,
     "hit_detail": "reliability []；value 唯一命中 cfg.degrade_switch（运维开关，语义排除）；dev 无资源级质量等级列，无等级分布聚合面"},
    {"probe": "gkx 资源质量等级面（同词族）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）词族扫（经 _gkxdb.py）",
     "hits": 0,
     "hit_detail": "命中 []——要素明细库无质量等级面"},
    {"probe": "久新资源质量等级面（同词族）",
     "source": "jiuxin",
     "sql": "SHOW TABLES（2026-11-02 live，212 表）词族扫",
     "hits": 0,
     "hit_detail": "quality/reliability 0 命中；value 唯一命中商业化仿真面（语义排除）——ads_* 无资源质量等级结果表"},
    {"probe": "需求原文「质量等级分布」定义段",
     "source": "doc",
     "sql": "rg 质量等级分布|等级分布|质量状况 三份需求真源",
     "hits": 0,
     "hit_detail": "三份说明书未出现「质量等级分布」字面；SRS seq 357「质量状况」为分区属性项（行级语义非分布聚合）；"
                   "seq 352 属性项为行级枚举；分布口径（枚举域/计数维：条数 vs 数据量）无定义"},
]

notes = [
    "判档：资源质量等级分布是稽核结果面的离散聚合（GROUP BY qualityLevel）——基座面（资源×等级）三源零承载"
    "（与 058 同根）→ 枚举分布无从执行 → 完全不支持；mock 12 行等级为手写常量，不作分布原料",
    "UI 语义核：分布不是独立接口面而是明细表的客户端聚合——GROUP_OPTIONS 选 '按质量等级' 时 groupedData "
    "对 filtered 行按 r.qualityLevel 建 map，count+=1 / volume+=r.volume，按 volume 降序；"
    "另有质量筛选器（filters.quality 等值过滤）——筛选与分组共用 qualityLevel 字段",
    "计数双维披露：groupedData 同时累加 count（资源条数）与 volume（数据量）——分布有双计数维"
    "（条数分布与体量分布），正式版须裁定主维或双维并存",
    "mock 披露：asd 12 行实算分布 优 5 条 Σ7600 / 良 5 条 Σ5760 / 中 2 条 Σ1360（与 058 同一 mock，无差档样本）"
    "——等级为手写常量（无稽核依据），B10 禁用作分布原料",
    "B11 对账：三源表数 542/280/210+212；质量词族与 _probe_s304_l7_quality_out.json 逐键一致（与 058/059/017 共享同一探针）",
    "升档触发器（B10）：与 058 共用——①质量稽核结果面立项 → 等级列可 GROUP BY（count/Σvolume）"
    "→ 升完全直接支持；②自建规则跑批+阈值映射 → 升完全转换支持（枚举域与计数维须登记）；③维持现状 → 完全不支持",
]

support = "完全不支持"

out = {
    "metric_id": "M_SCIUI_DATATHM_060",
    "batch": "S3-05",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/components/AccessSourceAnalysisDetail.jsx:62",
        "repos/demo-ui-science/src/pages/data-resources/components/AccessSourceAnalysisDetail.jsx:195",
        "repos/demo-ui-science/src/pages/data-resources/components/AccessSourceAnalysisDetail.jsx:288",
        "repos/demo-ui-science/src/pages/data-resources/components/AccessSourceAnalysisDetail.jsx:530",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现「质量等级分布/等级分布」字面；语义锚同 058（seq 352 属性项 + "
                ":2629 质量评估算法工程前提）；SRS seq 357「质量状况」为分区行级属性项",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["质量等级时间序列整体缺承载（无稽核面即无期次分布）"],
    "base_years_note": "分布为稽核快照的聚合读数，无期次序列需求承载",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["542", "280", "210", "212", "12", "6", "4", "2", "7600", "5760", "1360", "62", "195", "288", "530"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
