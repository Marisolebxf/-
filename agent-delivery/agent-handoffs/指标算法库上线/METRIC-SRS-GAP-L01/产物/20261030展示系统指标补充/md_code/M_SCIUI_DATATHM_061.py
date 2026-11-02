#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_061 资源质量评分（单资源）· 三源探针脚本（S3-05 L2 质量组）。

含义：单资源粒度的质量评分读数——总体视窗两处与主题视窗两处：
- OverviewWindow.jsx:465-469 知识图谱节点详情面板「质量: {detail.quality}分」（单库/单表节点级）
- OverviewWindow.jsx:560 主题透视表「质量评分」列（avgQuality，主题级——061 的分组形态边缘）
- ThemeWindow.jsx:614 数据库详情导出表「质量评分」列（quality，单库级）
- ThemeWindow.jsx:497-506/:277-279 质量筛选器（≥90/80-89/<80 三档过滤 d.quality——单库级评分的筛选用法）
mock 源：mockData.js:1611-1620 knowledgeGraphNodeDetails（n1 94/n2 93/n3 91/n6 96/n7 95/n8 94）
+ themeDatabases 7 库 quality（86/88/90/91/92/94/96）。

判档路径（口径=「资源（库/表）粒度的质量评分，评分由质量稽核算法产出」——058 同根行级形态）：
- 资源级质量稽核结果面（资源×评分）三源零承载 → 单资源评分无处读出；
- dev quality/score 词族唯一命中 cfg.degrade_switch（运维开关，语义排除）；gkx 0 命中；
  久新 value 命中 1 张商业化仿真面（语义排除）；
- mock 两处评分为手写常量（无稽核依据），不作评分原料（B10）；
- 判完全不支持（行级评分随稽核面缺位而缺位）。

B11 锚：三源表数 542/280/210（快照）+212（live）；词族 = _probe_s304_l7_quality_out.json。
"""
import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_061_out.json")
SNAP7 = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s304_l7_quality_out.json")
MOCK = "/Users/samuel_tang/my_project/gkx-lumen/repos/demo-ui-science/src/pages/data-resources/mockData.js"

snap = json.load(open(SNAP7, encoding="utf-8"))
probe = json.load(open(PROBE, encoding="utf-8"))
mock_src = open(MOCK, encoding="utf-8").read()

# knowledgeGraphNodeDetails quality 实算（mockData.js:1611-1620 逐行解析）
kg_block = re.search(r"export const knowledgeGraphNodeDetails = \{(.*?)\n\};", mock_src, re.S).group(1)
kg_nodes = re.findall(r"'(n\d+)': \{ name: '(.*?)', category: '(.*?)'.*?quality: (\d+)", kg_block)
kg_quality = {nid: {"name": name, "category": cat, "quality": int(q)} for nid, name, cat, q in kg_nodes}
assert len(kg_quality) == 6, kg_quality  # n1/n2/n3/n6/n7/n8 六节点带 quality

# themeDatabases quality（与 058/060 共用实算）
td_block = re.search(r"export const themeDatabases = \[(.*?)\];", mock_src, re.S).group(1)
td_quality = sorted(int(x) for x in re.findall(r"quality: (\d+)", td_block))

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
    # UI 挂载证据（四处）
    "ui_mount_graph_node_detail": "OverviewWindow.jsx:465-469 图谱节点详情「质量: {detail.quality}分」（库/表节点级）",
    "ui_mount_theme_drilldown": "OverviewWindow.jsx:560 主题透视表「质量评分」列（avgQuality，Progress percent）——主题级分组形态",
    "ui_mount_theme_db_export": "ThemeWindow.jsx:614 数据库详情导出表「质量评分」列（quality，单库级）",
    "ui_mount_quality_filter": "ThemeWindow.jsx:497-506 质量筛选器（≥90/80-89/<80）+ :277-279 过滤逻辑（d.quality 数值分三档）",
    # mock 演示值（实算，结构证据，不作源）
    "ui_mock_kg_node_quality": kg_quality,  # 6 节点 91-96
    "ui_mock_theme_db_quality_sorted": td_quality,  # 7 库 86-96
    "ui_mock_note": "知识图谱 10 节点中 4 节点（应用系统/主题领域类 n4/n5/n9/n10）无 quality 字段——评分配挂在库/表类节点",
}

derived = [{
    "key": "resource_quality_score_single",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『资源质量评分（单资源）』需资源级质量稽核结果面（资源×评分，058 同根）——三源零承载"
            "（dev 开关表语义排除/gkx 0/久新仿真面语义排除）。mock 两处评分（图谱节点 6 值/主题库 7 值）"
            "为手写常量，不作评分原料。按 B10 留空即负结论登记",
}]

absence_probe = [
    {"probe": "dev 资源级质量评分列与稽核结果面（quality/score/reliability 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表，L7 族探针 2026-11-02）",
     "hits": 0,
     "hit_detail": "reliability []；value 唯一命中 cfg.degrade_switch（运维开关，语义排除）；dev 无资源级评分列"},
    {"probe": "gkx 资源级质量评分面（同词族）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）词族扫（经 _gkxdb.py）",
     "hits": 0,
     "hit_detail": "命中 []——要素明细库无质量评分面"},
    {"probe": "久新资源级质量评分面（同词族）",
     "source": "jiuxin",
     "sql": "SHOW TABLES（2026-11-02 live，212 表）词族扫",
     "hits": 0,
     "hit_detail": "quality/reliability 0 命中；value 唯一命中商业化仿真面（语义排除）——ads_* 无资源质量评分结果表"},
    {"probe": "需求原文单资源质量评分定义段",
     "source": "doc",
     "sql": "rg 质量评分|质量分|数据质量等级 三份需求真源",
     "hits": 0,
     "hit_detail": "三份说明书未出现「质量评分/质量分」字面；语义锚同 058（seq 352 属性项「数据质量等级」+ "
                   ":2629 工程前提「智能数据质量评估算法……为数据管理和资源优化提供量化依据」——量化依据即评分语义）"},
]

notes = [
    "判档：单资源质量评分是稽核结果面的行级读数——基座面（资源×评分）三源零承载（与 058 同根）"
    "→ 行级评分无处读出 → 完全不支持；mock 两处评分（图谱节点/主题库）为手写常量，不作评分原料",
    "UI 语义核：评分挂载粒度谱系——图谱节点详情（库/表节点级，OverviewWindow:465-469）→ 主题库详情导出"
    "（单库级，ThemeWindow:614）→ 主题透视列（主题级 avgQuality，OverviewWindow:560——分组形态，059 边缘）；"
    "另有质量筛选器（ThemeWindow:497-506）按 ≥90/80-89/<80 三档过滤 d.quality——评分的筛选用法",
    "阈值形态第三套披露：ThemeWindow 质量筛选器三档（≥90/80-89/<80）与 AccessDataResourceDetail QUALITY_OPTIONS "
    "同形——这是 UI 第 3 处阈值形态（058 已披露两套），进一步印证阈值无正式定义须裁定",
    "mock 披露：知识图谱 10 节点中仅 6 节点带 quality（n1 基础研究库 94/n2 基因测序 93/n3 蛋白质结构 91/"
    "n6 医学影像库 96/n7 CT扫描 95/n8 MRI数据 94——库/表类节点）；应用系统/主题领域类 4 节点（n4/n5/n9/n10）"
    "无 quality 字段——评分配挂在数据资产节点，非全节点普配",
    "B11 对账：三源表数 542/280/210+212；质量词族与 _probe_s304_l7_quality_out.json 逐键一致（与 058/059/060 共享同一探针）；themeDatabases 7 值与 058 逐键一致",
    "升档触发器（B10）：与 058 共用——①质量稽核结果面立项 → 单资源评分直查 → 升完全直接支持；"
    "②自建规则跑批+评分登记 → 升完全转换支持（评分算式与权重须登记）；③维持现状 → 完全不支持",
    "权威口径参照（R2 Dataphin）：表质量分 = sum(规则权重×规则得分)/sum(规则权重)（满分 100）——单资源评分的工程范式",
]

support = "完全不支持"

out = {
    "metric_id": "M_SCIUI_DATATHM_061",
    "batch": "S3-05",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:465",
        "repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:560",
        "repos/demo-ui-science/src/pages/data-resources/ThemeWindow.jsx:614",
        "repos/demo-ui-science/src/pages/data-resources/ThemeWindow.jsx:497",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现「质量评分/质量分」字面；语义锚同 058（seq 352「数据质量等级」属性项 + "
                ":2629「智能数据质量评估算法……提供量化依据」工程前提——量化依据即评分语义）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["质量评分时间序列整体缺承载（无稽核面即无评分历史）"],
    "base_years_note": "评分为稽核结果快照读数，无期次序列需求承载",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["542", "280", "210", "212", "94", "93", "91", "96", "95", "86", "88", "90", "92", "465", "560", "614", "497"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
