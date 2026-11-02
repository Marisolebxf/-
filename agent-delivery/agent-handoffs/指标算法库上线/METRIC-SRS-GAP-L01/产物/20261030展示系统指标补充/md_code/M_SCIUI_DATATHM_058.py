#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_058 数据质量等级（优/良/中/差）· 三源探针脚本（S3-05 L2 质量组）。

含义：科技数据资源·接入视窗/总体视窗·归集资源明细与来源分析明细的行级「质量等级」枚举列
（优/良/中/差，配 qualityScore 百分数）。两处挂载：
- AccessDataResourceDetail.jsx:315「质量」列（quality 数值 + QUALITY_OPTIONS 枚举映射 ≥90 优/80-89 良/<80 中）
- ResourceSourceAnalysisDetail.jsx:317「质量」列（qualityLevel 枚举 + qualityScore，QUALITY_COLOR 四档映射）
mock 源：mockData.js asd-001..012（优/良/中 三档 12 行）与 osa-001..012（含差档映射空间）。

判档路径（口径=「数据质量稽核结果面（资源×等级枚举×评分），等级由质量评分阈值映射」）：
- 需求语义核：SRS 接入视窗 seq 352「数据质量等级」为渠道归集明细的元数据属性项；主需求 :2613 同文；
  :2629「智能数据质量评估算法，实时检测各项数据指标准确性、完整性和一致性」——工程前提（质量评估
  算法+稽核结果登记）三源未建；
- 直接承载：dev quality/score 词族——L7 族探针 dev_value_like_tables 唯一命中
  gkxlumenx_cfg.degrade_switch（运维降级开关，语义排除）；dev_reliability_like_tables=[]；
- gkx 280 表 quality/grade/level 词族 0 命中（要素明细库无稽核面）；
- 久新 live 212 表 quality 词族 0 命中（value 命中 1 张商业化价值仿真面，语义≠质量稽核）；
- 质量稽核结果面（资源级评分×等级映射）三源零承载 → 判完全不支持。
- GB/T 36344-2018 六维（规范性/完整性/准确性/一致性/时效性/可访问性）是等级评定的规则底稿。

B11 锚：三源表数 542/280/210（快照）+212（live 复核）；词族 = _probe_s304_l7_quality_out.json。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_058_out.json")
SNAP7 = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s304_l7_quality_out.json")

snap = json.load(open(SNAP7, encoding="utf-8"))
probe = json.load(open(PROBE, encoding="utf-8"))

# UI 质量等级枚举（两处挂载的阈值映射，从组件源码核对）
# AccessDataResourceDetail.jsx:54-59 QUALITY_OPTIONS: ≥90 优 / 80-89 良 / <80 中（无差档）
# ResourceSourceAnalysisDetail.jsx:37 QUALITY_COLOR: {优,良,中,差} 四档
# mock 分布从 mockData.js 实算（B1：不手写计数，逐行正则解析）
import re
MOCK = "/Users/samuel_tang/my_project/gkx-lumen/repos/demo-ui-science/src/pages/data-resources/mockData.js"
mock_src = open(MOCK, encoding="utf-8").read()
mock_lines = mock_src.split("\n")

def _dist(rows):
    from collections import Counter
    c = Counter(re.search(r"qualityLevel: '(.+?)'", l).group(1) for l in rows)
    return [[k, c[k]] for k in sorted(c)]

asd_rows = [l for l in mock_lines[133:145] if "qualityLevel" in l]      # asd-001..012 单行对象
osa_block = "\n".join(mock_lines[275:472])                               # osa-001..012 多行对象
osa_objs = re.findall(r"qualityLevel: '(.+?)',\s*\n\s*qualityScore: (\d+)", osa_block)
osa_dist = [[k, sum(1 for lvl, _ in osa_objs if lvl == k)] for k in sorted(set(lvl for lvl, _ in osa_objs))]
osa_scores = sorted(int(s) for _, s in osa_objs)
td_block = re.search(r"export const themeDatabases = \[(.*?)\];", mock_src, re.S).group(1)
td_quality = sorted(int(x) for x in re.findall(r"quality: (\d+)", td_block))

facts = {
    "dev_table_count": sum(snap["dev"]["schema_table_counts"].values()),
    "gkx_table_count": snap["gkx"]["table_count"],
    "jiuxin_table_count_snapshot_20261101": len(snap["jiuxin"]["tables"]),
    "jiuxin_table_count_live_20261102": probe["jiuxin_table_count_live"],
    # 质量词族命中（L7 族探针 2026-11-02 实跑）
    "dev_reliability_like_tables": probe["dev_reliability_like_tables"],  # []
    "dev_value_like_tables": probe["dev_value_like_tables"],  # [cfg.degrade_switch]
    "gkx_reliability_like_tables": probe["gkx_reliability_like_tables"],  # []
    "gkx_value_like_tables": probe["gkx_value_like_tables"],  # []
    "jiuxin_value_like_tables": probe["jiuxin_value_like_tables"],  # [商业化价值仿真]
    # 语义排除证据
    "dev_degrade_switch_semantic": "gkxlumenx_cfg.degrade_switch 为运维降级开关配置表（开关状态维护），无资源质量字段——语义排除",
    "jiuxin_value_table_semantic": "ads_technology_commercial_value_simulation 为技术成果商业化价值仿真面（成果转化域模拟估值），语义≠数据质量稽核结果——语义排除",
    # UI 等级枚举证据（挂载点组件源码）
    "ui_quality_enum_access_data_detail": {"source": "AccessDataResourceDetail.jsx:54-59 QUALITY_OPTIONS", "bands": [["≥90", "优"], ["80-89", "良"], ["<80", "中"]]},
    "ui_quality_enum_resource_source_detail": {"source": "ResourceSourceAnalysisDetail.jsx:37 QUALITY_COLOR", "levels": ["优", "良", "中", "差"]},
    "ui_quality_render_access_data_detail": "AccessDataResourceDetail.jsx:315-325 质量列 Progress percent=quality（数值分 0-100 阈值映射三档）",
    "ui_quality_render_resource_source_detail": "ResourceSourceAnalysisDetail.jsx:317-325 质量列 Tag『{qualityLevel} · {qualityScore}』（枚举+分数并列）",
    # mock 分布（结构证据，不作数据源；mockData.js 实算）
    "ui_mock_asd_quality_dist": _dist(asd_rows),  # 优5/良5/中2（2026-11-02 复算修正）
    "ui_mock_asd_rows": len(asd_rows),
    "ui_mock_osa_quality_dist": osa_dist,  # 优7/良4/中1（2026-11-02 复算修正）
    "ui_mock_osa_rows": len(osa_objs),
    "ui_mock_osa_quality_scores_sorted": osa_scores,  # 81-96
    "ui_mock_theme_db_quality_values_sorted": td_quality,  # themeDatabases 7 库 quality 数值
}

derived = [{
    "key": "data_quality_level_enum",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『数据质量等级（优/良/中/差）』需资源级质量稽核结果面（评分×阈值映射等级）——三源零承载："
            "dev quality/score 词族唯一命中 cfg.degrade_switch（运维开关，语义排除）；gkx 0 命中；"
            "久新 value 命中 1 张商业化仿真面（语义排除）。mock 三处质量值（asd/osa/themeDatabases）"
            "为演示常量，不作等级原料。按 B10 留空即负结论登记",
}]

absence_probe = [
    {"probe": "dev 资源质量稽核结果面（quality/grade/score/reliability 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表，L7 族探针 2026-11-02 实跑）",
     "hits": 0,
     "hit_detail": "reliability 词族命中 []；value 词族唯一命中 gkxlumenx_cfg.degrade_switch——"
                   "运维降级开关配置表（开关状态维护，无资源质量字段），语义排除；dev 无资源级质量评分/等级表"},
    {"probe": "gkx 资源质量稽核结果面（quality/grade/level/reliability/value 词族）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）词族扫（经 _gkxdb.py，L7 族探针）",
     "hits": 0,
     "hit_detail": "命中 []——gkx 为要素明细库（论文/专利/机构/学者），无资源质量稽核面，无评分/等级结果表"},
    {"probe": "久新资源质量稽核结果面（同词族）",
     "source": "jiuxin",
     "sql": "SHOW TABLES（2026-11-02 live，212 表）词族扫（L7 族探针）",
     "hits": 0,
     "hit_detail": "quality/reliability 词族 0 命中；value 词族唯一命中 ads_technology_commercial_value_simulation"
                   "——技术成果商业化价值仿真面（成果转化域模拟估值），语义≠数据质量稽核——语义排除后 0 张"},
    {"probe": "需求原文「数据质量等级」定义段",
     "source": "doc",
     "sql": "rg 数据质量等级|质量等级|质量评估 三份需求真源",
     "hits": 3,
     "hit_detail": "SRS 接入视窗 seq 352『包括数据类型、采集时间、数据质量等级、关联项目、所属领域等元数据』"
                   "（等级为归集明细元数据属性项）；主需求 :2613 同文；:2629『内置智能数据质量评估算法，"
                   "实时检测各项数据指标准确性、完整性和一致性』——需求自己点名工程前提（质量评估算法），"
                   "该前提三源未建；『优/良/中/差』四档字面三份说明书 0 命中（仅见 UI 枚举）"},
]

notes = [
    "判档：资源级质量稽核结果面（评分×阈值映射等级）三源零承载 → 指标及关键依赖三源均无法构建"
    " → 完全不支持；需求 :2629 自点名『智能数据质量评估算法』工程前提，该前提三源未建"
    "（缺口归属『表不存在』，修复动作=质量稽核结果面立项，与 017/059/060/061/069 共用）",
    "UI 语义核：两处挂载同为行级质量枚举列——AccessDataResourceDetail（seq 357-359 接入资源详情）"
    "用数值分阈值映射（≥90 优/80-89 良/<80 中，无差档）；ResourceSourceAnalysisDetail（seq 351 来源分析）"
    "用枚举+分数并列（优/良/中/差 四档色映射，mock 无差档行）——同一语义两套阈值形态，正式版须统一",
    "mock 披露：asd 12 行（优5/良5/中2）与 osa 12 行（优7/良4/中1，qualityScore 81-96）质量值为演示常量；"
    "themeDatabases 7 库 quality 86-96 全落优/良两档——mock 无任何差档样本，四档枚举在演示数据中未完整行使（B10）",
    "B11 对账：三源表数 542/280/210（快照）+212（live 复核）；质量词族与 _probe_s304_l7_quality_out.json 逐键一致",
    "升档触发器（B10）：①质量稽核结果面立项（规则库+资源级跑批+评分登记，GB/T 36344 六维底稿）"
    "→ 等级直查 → 升完全直接支持；②乙方自建稽核规则跑批（资源级核查脚本+阈值映射）→ 升完全转换支持"
    "（规则集与阈值须登记）；③维持现状 → 完全不支持（UI 该列建议『暂无数据』）",
    "权威口径参照（R1 GB/T 36344-2018）：数据质量六维（规范性/完整性/准确性/一致性/时效性/可访问性）"
    "是评分的规则维度源——等级=评分的阈值离散化，阈值裁定须甲方一纸确认",
]

support = "完全不支持"

out = {
    "metric_id": "M_SCIUI_DATATHM_058",
    "batch": "S3-05",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/components/AccessDataResourceDetail.jsx:315",
        "repos/demo-ui-science/src/pages/data-resources/components/ResourceSourceAnalysisDetail.jsx:317",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:134",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "「数据质量等级」作为元数据属性项见于 SRS 接入视窗 seq 352 与主需求 :2613"
                "（渠道归集明细属性枚举）；工程前提『智能数据质量评估算法』见 :2629；"
                "『优/良/中/差』四档字面仅见 UI 枚举（QUALITY_COLOR/QUALITY_OPTIONS）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["质量稽核时间序列整体缺承载（无评分登记面即无期次）"],
    "base_years_note": "等级为稽核结果快照读数，无期次序列需求承载",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["542", "280", "210", "212", "12", "86", "96", "90", "80", "352", "2613", "2629"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
