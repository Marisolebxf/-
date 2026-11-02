#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INCUB_031 数据社区条目数 · 三源探针脚本（S3-07 L3）。

含义：软科学科技信息展示系统全局导航「数据社区」栏目（scienceGlobalHeaderMock.js:50
navItems {key:"community", label:"数据社区", hasChildren:true}——下拉未实现/无页面），
派单清单定名「数据社区条目数」= 数据社区栏目下挂的条目（数据集/数据产品/主题库等）计数。
注意：该导航挂在软科学页 header，语义最近邻是 data-resources 模块的资源总量
（mockData.js overviewKPIs「资源总量 30,398 个」）——同 UI 体系的数据目录演示面。

判档路径（口径 = 数据社区/数据资源目录条目计数）：
- dev：data_resource/dataset/data_asset/data_item/data_catalog/data_service/resource
  词族扫 1171 表（16 schema 非 demo）——命中仅 gkxlumenx_bi.onl_drag_dataset_*
  （BI 拖拽报表数据集配置 87/232/5 行，语义=报表配置非数据社区条目）；
  数据资源登记面无表（Lane7 DATAOV_001 已证 gen_datasource_conf 0 + jimu 8 样例级）；
- gkx：同词族 280 表 0 命中（要素库，无数据目录维）；
- 久新：resource 词族 7 命中全为「科研资源统计」语义（论文/人才/经费量）——
  ads_city_subfield_resource_yearly 27,720 行/ads_institution_subfield_resource_yearly
  985,555 行/ads_research_resource_shortage_yearly 1,408,176 行（city/institution×
  subfield×year 的 paper_count/talent_count/funding_amount_cny 度量）——非数据条目
  计数；community 词族 ads_technology_community（1,731 行）/member（19,430 行）=
  技术社区发现（图谱聚类），语义排除；
- mock：overviewKPIs「资源总量 30,398 个」手写；导航 community 栏目无子页无条目列表；
- 判完全不支持（数据社区条目面——数据资源元数据目录——三源均无法构建）。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_INCUB_031_out.json")
P031 = os.path.join(BASE, "_probe_s307_l3_incub_031_out.json")

probe = json.load(open(P031, encoding="utf-8"))

facts, derived, notes, absence = {}, [], [], []

# ============ ① mock 层 ============
facts["ui_mounts"] = [
    "scienceGlobalHeaderMock.js:50（navItems {key:'community', label:'数据社区', hasChildren:true}——全局导航栏第 7 项，下拉未实现）",
    "ScienceGlobalHeader.jsx:57-67（navItems.map 渲染——community 项仅渲染按钮+下拉箭头，无 onClick/子页面路由）",
    "AchievementPreviewApp.jsx:556-557（ScienceGlobalHeader navItems={scienceGlobalHeaderMock.navItems}——mock 直传，无数据接口）",
]
facts["ui_mock_note"] = ("「数据社区」导航在软科学/talent-preview 两处 header 均为静态按钮（hasChildren:true 仅渲染下拉箭头图标，"
                         "无子菜单数据结构、无条目列表页）；派单清单名「数据社区条目数」的语义最近邻是 data-resources 模块"
                         " overviewKPIs（mockData.js:1656-1658：资源总量 30,398 个/主题库数量 28 个/资源类型数 4 类——手写演示值）")
facts["ui_mock_overview_kpis"] = {"资源总量": "30,398 个", "主题库数量": "28 个", "资源类型数": "4 类"}

# ============ ② dev ============
facts["dev_table_total_16schema"] = probe["dev_table_total"]  # 1171 为全实例非系统库表数
facts["dev_word_tables"] = probe["dev_word_tables"]
facts["dev_word_rows"] = probe["dev_rows"]
facts["dev_semantics_note"] = ("命中仅 gkxlumenx_bi.onl_drag_dataset_head/item/param（87/232/5 行）="
                               "JimuReport BI 拖拽报表的数据集配置表（报表配置语义），非数据社区条目；"
                               "数据资源登记面（Lane7 DATAOV_001 独立留证）：gen_datasource_conf 0 行 + "
                               "jimu_report_data_source 8 行——样例级，无数据资产目录")
facts["dev_word_community"] = []  # 共享快照 dev word_community = []
snap_note = "dev community 词族 0 命中（共享快照 _probe_s307_l3_incub_out.json dev.word_community）"
facts["dev_community_note"] = snap_note

# ============ ③ gkx ============
facts["gkx_table_count"] = probe["gkx_table_count"]
facts["gkx_word_tables"] = probe["gkx_word_tables"]  # []

# ============ ④ 久新 ============
facts["jiuxin_table_count_live"] = probe["jiuxin_table_count_live"]
facts["jiuxin_word_tables"] = probe["jiuxin_word_tables"]
facts["jiuxin_semantics_note"] = ("resource 词族 7 命中全为科研资源统计语义（论文/人才/经费量年度表）："
                                  "ads_city_subfield_resource_yearly 27,720 行 / ads_institution_subfield_resource_yearly "
                                  "985,555 行 / ads_research_resource_shortage_yearly 1,408,176 行——度量列是 "
                                  "paper_count/talent_count/funding_amount_cny（非数据条目计数）；"
                                  "community 词族 ads_technology_community 1,731 行 / _member 19,430 行 = 技术社区发现"
                                  "（图谱聚类：community_method/graph_density/member_count 列）——语义排除，非数据社区栏目")

# ============ ⑤ 需求溯源 ============
facts["named_in_srs"] = False
facts["named_note"] = ("「数据社区」在三份说明书未作为功能叶出现（软科学页导航为 demo 演示层）；"
                       "主需求科技数据资源章有「数据社区/数据共享」相关功能句但属于 DATA 族（Lane 7 已覆盖）；"
                       "本件挂载在软科学 header mock——UI 派生命名")

# ============ ⑥ 权威口径 ============
facts["authoritative_reference"] = ("数据目录条目计数的行业口径：OpenDW 等 data catalog 管理规范——目录条目=已登记数据资产"
                                    "（数据集/数据产品/API）计数，需资产登记元数据（名称/责任方/更新频率/质量分）；"
                                    "demo 最近邻 data-resources overviewKPIs 口径=资源总量（接入数据集个数）")

# ============ ⑦ absence_probe ============
absence = [
    {"probe": "dev 数据社区/数据资源目录面（data_resource/dataset/catalog 词族，16 schema 非 demo）",
     "source": "dev", "sql": "information_schema.tables 词族扫描 + COUNT(*)",
     "hits": 3,
     "hit_detail": "仅 onl_drag_dataset_head/item/param（BI 报表数据集配置 87/232/5 行）——报表配置语义；数据资源登记面 gen_datasource_conf 0 + jimu_report_data_source 8（DATAOV_001 结论）；community 词族 0 命中"},
    {"probe": "gkx 数据目录面（同词族，280 表）",
     "source": "gkx", "sql": "SHOW TABLES FROM gkx 词族过滤",
     "hits": 0, "hit_detail": "0 命中——gkx 为科技要素库（论文/专利/机构/学者），无数据资产管理维"},
    {"probe": "久新数据目录面（resource/community/theme/catalog 词族，live 218 表）",
     "source": "jiuxin", "sql": "SHOW TABLES 词族过滤 + resource 表列实读",
     "hits": 9,
     "hit_detail": "resource 7 命中=科研资源统计（city/institution×subfield×year 的 paper/talent/funding 度量，27,720/985,555/1,408,176 行）；community 2 命中=技术社区发现（图谱聚类 1,731/19,430 行）——均语义排除，无数据条目登记面"},
    {"probe": "UI 数据社区栏目条目列表",
     "source": "doc", "sql": "rg 数据社区 src/pages + ScienceGlobalHeader 渲染逻辑实读",
     "hits": 2,
     "hit_detail": "仅 2 处导航按钮（soft-science scienceGlobalHeaderMock.js:50 / talent-preview App.jsx:1002），hasChildren:true 但无子菜单数据、无条目页——「条目数」在 UI 层即不存在可数对象"},
]

# ============ ⑧ derived ============
derived = [
    {"key": "data_community_entry_count", "value": None, "numerator": None, "denominator": None,
     "note": "『数据社区条目数』=数据社区栏目下挂条目（数据集/数据产品）计数。UI 层：community 导航为静态按钮无子页——无可数对象；数据层：dev 目录面无表（登记面样例级 8 条）、gkx 0 命中、久新 resource/community 词族均语义排除 → 不可构建，按 B10 留空即负结论登记"},
]

notes = [
    "判档：数据社区条目面（数据资产目录）三源均无法构建 + UI 栏目无子页 → 完全不支持",
    "语义辨析：demo 体系内「数据资源统计」有完整模块（data-resources，DATAOV/DATAAPP 族覆盖），但本件挂载点是软科学页 header 的「数据社区」导航——两模块无路由联通（ AchievementPreviewApp 无 data-resources 路由），不能挪用 DATA 族读数充数",
    "权威口径（R1 OpenDW data catalog 惯例）：目录条目=已登记数据资产计数，前提是资产登记元数据面——三源均无",
    "mock 披露：overviewKPIs「资源总量 30,398 个」为 data-resources 模块手写演示值（本件不引用为指标值，仅作语义参照）",
    "同族件关系：DATAOV_001（多源数据整合分析）共享「数据源登记面样例级 8 条」结论；DATA 族（Lane 7）覆盖 data-resources 模块真件——本件是 INCUB 族 UI 派生命名件",
    "升档路径：①数据资产目录立项（数据集/产品/API 登记面落 gkxlumenx_ads）→ 条目数可直查=完全直接支持；②软科学 header community 导航接通 data-resources 路由 → 语义归位",
]

out = {
    "metric_id": "M_SCIUI_INCUB_031",
    "batch": "S3-07",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/achievement-preview/modules/soft-science/mock/scienceGlobalHeaderMock.js:50",
        "repos/demo-ui-science/src/pages/achievement-preview/modules/soft-science/components/ScienceGlobalHeader.jsx:57",
        "repos/demo-ui-science/src/pages/achievement-preview/AchievementPreviewApp.jsx:556",
        "repos/demo-ui-science/src/pages/talent-preview/App.jsx:1002",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「数据社区」非三说明书功能叶；软科学页导航为 demo 演示层命名；主需求科技数据资源章的数据社区/共享功能归 DATA 族（Lane 7）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": "完全不支持",
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["无年度基期维（目录条目计数为登记时点截面值，UI 亦无历史序列）"],
    "base_years_note": "条目数是目录登记截面计数（无基期对齐问题）；三源无承载无基期可言；非「缺年按 0 摊入」",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": ["30398", "28", "4", "87", "232", "5", "8", "0", "3", "9", "2", "1171", "280", "218", "27720", "985555", "1408176", "1731", "19430"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", OUT)
print("support_judgment:", out["support_judgment"])
