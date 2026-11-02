#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_062 资源分布可视化 · 三源探针脚本（S3-05 L2 可视化组）。

含义：主题视窗·主题库列表右侧「资源分布可视化」卡——七主题资源量饼图
（getThemeDistributionOption 硬编码 4230/3890/3156/2845/2634/2456/1987，Σ=21198）。
挂载：ThemeWindow.jsx:534（Card title=资源分布可视化）/:535（ReactECharts 饼图）
/:125-141（getThemeDistributionOption——数据硬编码在组件内，与 mockData.js:14-21
resourceThemeDistribution 同值复制）。

判档路径（口径=「按主题分组的资源量分布（饼图数据对）」——主题归属面的枚举聚合）：
- 可视化本身是展示层（ECharts 饼图），数据侧判定的是「主题×资源量分布对」的承载；
- 主题归属面（资源→主题的映射登记）三源无承载（theme/subject 词族 0 命中——037 件先例：
  「业务库边界（哪些表构成主题库）无任何登记」，与 DATATHM_004 同根）；
- 降档不到底：主题分布的**近似承载**存在——久新 ads_discipline_*（学科域面：discipline_domain/
  subfield/topic 四级）+ dev gkxlumenx_topic_enterprise 21 表（企业主题域）——但粒度是
  「学科/主题域」非「资源归属计数」，须转换（学科域→资源量映射无登记）；
- mock 双源同值披露：饼图数据硬编码在组件（:126-131）与 mockData resourceThemeDistribution
  （:14-21）同值复制（7 对 name/value 逐对相同，Σ=21198）——非独立两源；
- 判部分支持（主题归属面无承载 ⇒ 分布对不可直查；学科域面有近似承载 ⇒ 转换路径存在但缺映射登记）。

B11 锚：三源表数 542/280/210；主题词族先例 = M_SCIUI_DATATHM_037/004。
"""
import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_062_out.json")
SNAP7 = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
MOCK = "/Users/samuel_tang/my_project/gkx-lumen/repos/demo-ui-science/src/pages/data-resources/mockData.js"
THEME_JS = "/Users/samuel_tang/my_project/gkx-lumen/repos/demo-ui-science/src/pages/data-resources/ThemeWindow.jsx"

snap = json.load(open(SNAP7, encoding="utf-8"))
mock_src = open(MOCK, encoding="utf-8").read()
theme_src = open(THEME_JS, encoding="utf-8").read()

# mock resourceThemeDistribution（:14-21）实算
rtd = re.findall(r"\{ name: '(.*?)', value: (\d+), avgQuality: \d+ \}", mock_src[:1000])
rtd_pairs = {name: int(v) for name, v in rtd}
rtd_sum = sum(rtd_pairs.values())  # 21198
assert len(rtd_pairs) == 7, rtd_pairs

# ThemeWindow 饼图硬编码数据（:126-131）实算——双源同值核
pie_block = re.search(r"function getThemeDistributionOption\(\) \{\s*const data = \[(.*?)\];", theme_src, re.S).group(1)
pie_pairs = {name: int(v) for v, name in re.findall(r"\{ value: (\d+), name: '(.*?)' \}", pie_block)}
pie_sum = sum(pie_pairs.values())
assert pie_pairs == rtd_pairs, (pie_pairs, rtd_pairs)  # 双源同值 assert

# 久新学科域面（lane7 快照 jiuxin 表清单）
jiuxin_tables = snap["jiuxin"]["tables"]
discipline_tables = sorted(t for t in jiuxin_tables if t.startswith("ads_discipline_"))
# dev 主题域表（topic_enterprise schema 21 表）
topic_schema_tables = [t[0] for t in snap["dev"]["schemas"]["gkxlumenx_topic_enterprise"]]

facts = {
    "dev_table_count": sum(snap["dev"]["schema_table_counts"].values()),
    "gkx_table_count": snap["gkx"]["table_count"],
    "jiuxin_table_count": len(jiuxin_tables),
    # 主题归属面承载（037/004 先例复用）
    "theme_registration_absence_note": "主题归属面（资源→主题映射登记）三源无承载——theme/subject 词族 0 命中"
                                       "（037 件先例：业务库边界无任何登记，与 DATATHM_004 同根）",
    # 近似承载：久新学科域面 + dev 主题域 schema
    "jiuxin_discipline_tables_sorted": discipline_tables,  # ads_discipline_domain/subfield/topic 等
    "jiuxin_discipline_note": "学科域四级面（domain/subfield/field/topic）——粒度是学科分类非资源归属计数，"
                              "学科域→资源量映射无登记（转换阻断件）",
    "dev_topic_schema_table_count": len(topic_schema_tables),  # 21
    "dev_topic_schema_note": "gkxlumenx_topic_enterprise 21 表（企业主题域）——粒度是企业主题非资源分布",
    # UI 挂载证据
    "ui_mount_card": "ThemeWindow.jsx:534 资源分布可视化卡（Card title）",
    "ui_mount_chart": "ThemeWindow.jsx:535 ReactECharts 饼图（getThemeDistributionOption，height 220）",
    "ui_mount_option_fn": "ThemeWindow.jsx:125-141 getThemeDistributionOption——数据硬编码组件内"
                          "（饼图七对 name/value + 七色板 #165dff…）",
    # mock 双源同值披露
    "ui_mock_theme_distribution": rtd_pairs,   # 7 对
    "ui_mock_theme_distribution_sum": rtd_sum,  # 21198
    "ui_mock_pie_hardcoded_sum": pie_sum,       # 21198（assert 同值）
    "ui_mock_dual_source_note": "饼图数据硬编码在组件（:126-131）与 mockData resourceThemeDistribution（:14-21）"
                                "7 对逐对同值复制——非独立两源（双源同值 assert 防漂移）；"
                                "themeDatabases 7 库每主题 1 库（categories 7 主题各 1）——库级分布与资源量分布无对账关系",
}

derived = [{
    "key": "resource_distribution_visualization",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『资源分布可视化』= 主题×资源量分布对（饼图数据）——主题归属面三源无承载"
            "（theme/subject 0 命中，037/004 先例）；近似承载存在（久新学科域四级面+dev 企业主题域 21 表）"
            "但学科域→资源量映射无登记（转换阻断）。mock 双源同值（组件硬编码=mockData 复制，Σ=21198）。"
            "按 B10 留空即负结论登记",
}]

absence_probe = [
    {"probe": "dev 主题归属登记面（theme/subject/topic 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表，lane7 快照）",
     "hits": 0,
     "hit_detail": "主题词族唯一命中 gkxlumenx_topic_enterprise schema 21 表——企业主题域分析面"
                   "（topic×企业），非资源→主题归属登记，语义排除；资源×主题映射表 0 命中"},
    {"probe": "gkx 主题归属面（同词族）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）词族扫",
     "hits": 0,
     "hit_detail": "gkx 为要素明细库（论文/专利/机构/学者），无主题归属登记面"},
    {"probe": "久新主题归属面（theme/subject + 学科域近似承载）",
     "source": "jiuxin",
     "sql": "SHOW TABLES（lane7 快照 210 表）词族扫",
     "hits": 4,
     "hit_detail": "theme 词族 0 命中；近似承载 ads_discipline_* 4 张（domain/subfield/field/topic 学科域四级面）"
                   "——粒度是学科分类树非资源归属计数；discipline→资源量映射无登记（转换阻断件）"},
    {"probe": "需求原文资源分布可视化定义段",
     "source": "doc",
     "sql": "rg 资源分布|分布可视化 三份需求真源",
     "hits": 0,
     "hit_detail": "三份说明书未出现「资源分布可视化」字面；语义锚主题视窗语境（主题库列表+分布展示）；"
                   "分布的分组键（主题七类）与计数维（资源量·个）无正式定义（mock 七类自定）"},
]

notes = [
    "判档：分布对（主题×资源量）依赖主题归属面——三源无承载（037/004 先例：业务库边界无登记）；"
    "但近似承载存在（久新学科域四级面+dev 企业主题域）——转换路径存在但缺映射登记 ⇒ 部分支持",
    "可视化本体零成本：ECharts 饼图是展示层（render 无数据依赖）——本件数据侧全部重量在分布对的承载，"
    "「可视化」三字不参与判档（任何分布对都能画饼）",
    "mock 双源同值披露：饼图数据硬编码在组件（ThemeWindow:126-131）与 mockData resourceThemeDistribution"
    "（:14-21）7 对逐对同值（assert 防漂移，Σ=21198）——前端作者复制非独立两源；"
    "themeDatabases 7 库每主题恰 1 库——库级（7×1）与资源量级（4230…1987）无对账关系",
    "分组键口径：mock 七主题（基础科学/工程技术/医学健康/农业科技/能源环境/信息技术/材料科学）——"
    "与 GB/T 13745 学科分类的对应关系无登记（久新 ads_discipline_* 四级可作映射底稿）",
    "B11 对账：三源表数 542/280/210；主题词族结论与 037/004 先例一致（同一「业务库边界无登记」缺口）",
    "升档触发器（B10）：①主题归属面立项（资源→主题映射登记）→ 分布对直查 GROUP BY theme"
    "→ 升完全直接支持；②学科域→资源映射裁定（久新 discipline 四级为底稿+登记映射规则）"
    "→ 升完全转换支持；③维持现状 → 部分支持（UI 饼图建议空态或挂学科域近似）",
    "权威口径参照（GB/T 13745-2009 学科分类与代码）：主题分组的分类学底稿——58 一级学科"
    "（mock 七类是展示级聚簇，正式版须裁分类层级）",
]

support = "部分支持"

out = {
    "metric_id": "M_SCIUI_DATATHM_062",
    "batch": "S3-05",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/ThemeWindow.jsx:534",
        "repos/demo-ui-science/src/pages/data-resources/ThemeWindow.jsx:125",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:14",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现「资源分布可视化」字面；语义锚主题视窗语境（主题库列表+分布展示）；"
                "分组键（主题七类）与计数维无正式定义",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["主题归属时间序列整体缺承载（分布对无期次）"],
    "base_years_note": "分布为归属面的快照聚合读数，无期次序列需求承载",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["542", "280", "210", "21198", "4230", "3890", "3156", "2845", "2634", "2456", "1987", "7", "21", "534"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
