# 数据社区条目数（M_SCIUI_INCUB_031）

> **类型**：无业务逻辑数值类（数据资产目录面三源零承载）｜ **域**：科技信息展示系统·软科学成果展示·全局导航「数据社区」栏目（静态按钮，无子页）｜ **UI 挂载**：`scienceGlobalHeaderMock.js:50`（navItems community 项）+ `ScienceGlobalHeader.jsx:57-67`（navItems.map 渲染，无 onClick/路由）+ `AchievementPreviewApp.jsx:556`（mock 直传）+ `talent-preview/App.jsx:1002`（同名导航第 2 处）
> **数据支持度**：**完全不支持**｜ **公式定义人**：无（「数据社区条目数」为派单清单从 UI mock 命名提取；三份说明书无此功能叶）｜ **口径归属**：UI 派生读数（导航按钮 mock，hasChildren:true 仅渲染箭头图标——无子菜单数据结构、无条目列表页）
> **复现脚本**：`code/M_SCIUI_INCUB_031.py`｜ **产物**：`code/M_SCIUI_INCUB_031_out.json`
> **四判定摘要**：直接结构 = 无（dev data_resource/dataset/catalog 词族仅命中 BI 报表数据集配置表；gkx 0 命中）；直接数据 = 无（同左）；依赖结构 = **缺**（数据资产登记面无表——dev 登记面样例级 8 条）；依赖数据 = 无（久新 resource 词族 7 表全为科研资源统计语义、community 词族 2 表全为技术社区发现语义——逐一排除）
> **数据源口径**：三源（dev live `10.50.11.76` `gkxlumenx_*` 非 demo + 三方库 gkx + 久新 `gkx_technology_analysis_dev` live 218 表复核）逐一探针留证；`demo_*` 禁引；mock 值仅作需求语义证据。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库与久新库**均无法构建 |

**四判定**：表结构直接支持 / 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全不支持。** 条目数的前提是「可数对象」：UI 层——「数据社区」导航是静态按钮（`hasChildren:true` 只渲染下拉箭头，无子菜单数组、无条目页路由，soft-science 与 talent-preview 两处同样）；数据层——数据资产目录面三源均无：dev 词族命中仅 `gkxlumenx_bi.onl_drag_dataset_head/item/param`（JimuReport BI 报表数据集配置 87/232/5 行，报表配置语义），登记面 `gen_datasource_conf` 0 行 + `jimu_report_data_source` 8 行（样例级，DATAOV_001 独立留证）；gkx 280 表 0 命中（要素库无资产管理维）；久新 resource 词族 7 表全为科研资源统计（论文/人才/经费年度度量），community 词族 `ads_technology_community` 1,731 行/`_member` 19,430 行为图谱聚类社区发现——语义全排除。

### 批次通用纪律摘要（S3-07 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 无除式（计数语义） |
| B4 | 负结论带探针 | absence_probe 四件（dev/gkx/久新/UI 可数对象） |
| B5 | 确定性 | 词族扫描固定顺序；列表 sorted() |
| B7 | 产物只由脚本产出 | 本件 py 实探产出 _out.json |
| B9 | 单位/日期陷阱 | 条目=登记时点截面计数（单位「个/条」披露） |
| B10 | 口径裁定保守交付 | 不挪用 DATA 族演示值充数；derived 留 null |
| B11 | 多本账互推 | dev 1171/gkx 280/久新 218 表数与探针件零漂移 |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| UI 有可数条目对象吗？ | 无 | 导航静态按钮，无子页无列表 |
| 三源有数据资产目录表吗？ | 无 | dev 仅 BI 配置表；gkx 0；久新语义排除 |
| 现在就能算吗？ | 不能 | 无登记面即无计数源 |

## 摘要

「数据社区条目数」源于软科学页全局导航 mock 的「数据社区」栏目（派单清单从 `scienceGlobalHeaderMock.js:50` 提取命名）。实查 UI：该导航在 `ScienceGlobalHeader.jsx` 仅渲染按钮+箭头图标（`hasChildren:true` 无子菜单数据、无路由），soft-science 与 talent-preview 两处同样——UI 层不存在可数的条目对象。数据侧按「数据资产目录条目计数」口径探三源：dev 词族命中仅 JimuReport BI 数据集配置表（87/232/5 行，报表语义），登记面样例级 8 条；gkx 280 表 0 命中；久新 resource 7 表（27,720/985,555/1,408,176 行）全为科研资源统计、community 2 表（1,731/19,430 行）为图谱聚类——语义全排除。判**完全不支持**。

- 需求判定：非三说明书功能叶；UI 派生命名件（demo 演示层导航）。
- 复现状态：三源探针+UI 渲染逻辑实读已跑通；四件 absence_probe 留证。
- 档位结论：**完全不支持**（可数对象与目录面双缺）。
- 关键事实：demo 内 `data-resources` 模块有完整数据资源统计（DATAOV/DATAAPP 族覆盖，mock 资源总量 30,398 个），但与本件挂载点（软科学 header）无路由联通——不能挪用其读数充数。
- 升档路径：数据资产目录立项（登记面落库）→ 完全直接支持；或导航接通 data-resources 路由 → 语义归位至 DATA 族。

## 一、需求定义概述

### 1.1 所属功能模块

软科学成果展示 → 全局导航「数据社区」栏目（`scienceGlobalHeaderMock.js:50` navItems 第 7 项 `{key:"community", label:"数据社区", hasChildren:true}`）。渲染链：`AchievementPreviewApp.jsx:556-557` 将 mock 直传 `ScienceGlobalHeader`，`ScienceGlobalHeader.jsx:57-67` `navItems.map` 仅渲染 `<button>` + `DownOutlined` 箭头——无 onClick、无子菜单、无路由。第 2 处同名导航 `talent-preview/App.jsx:1002`（静态数组 map）。派单清单语义最近邻：data-resources 模块 `overviewKPIs`（`mockData.js:1654-1658`）。

### 1.2 为什么需要本指标

若数据社区栏目上线，条目数是栏目运营的基础读数（已登记数据集/数据产品/主题库个数），对应主需求科技数据资源章「数据汇聚/共享」的数据资产盘点诉求（该章功能叶由 DATA 族覆盖）。

### 1.3 需求文档是否给出定义方法

三份说明书无「数据社区」功能叶。**固定句式：三份说明书未给出该指标的计算方法。**

### 1.4 类似指标权威方法可行性分析概要

数据目录条目计数（要点版，完整版指向附录 C）：行业口径（OpenDW 等数据目录管理规范）——目录条目 = 已登记数据资产（数据集/数据产品/API）计数，前提是资产登记元数据面（名称/责任方/更新频率/质量分）。demo 最近邻 `overviewKPIs` 口径 = 资源总量（接入数据集个数，mock 30,398）。

### 1.5 引用来源

1. OpenDW. Data Catalog Management（目录条目=登记资产计数口径）. https://opendw.io/
2. Data Governance Professionals. Data Asset Inventory Best Practices. https://www.datagovernanceprofessionals.org/
3. demo UI data-resources 模块（语义参照，mock 值不作数据证据）. `repos/demo-ui-science/src/pages/data-resources/mockData.js:1654`

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意**：数据社区导航上线后栏目下挂条目（数据集/产品/主题库）的登记计数。
- **操作化定义**：条目数 = COUNT(目录登记面 WHERE status='active')，登记时点截面。
- **降档触发器**：已处最低档。
- **升档触发器**：①登记面落库 → 完全直接支持；②导航接通 data-resources → 语义归位 DATA 族。

### 1.7 需求叶定位与相近叶关系

- 本叶：INCUB 族 UI 派生命名件（软科学 header 导航）。
- 相近叶：DATAOV_001 共享「登记面样例级 8 条」结论；DATA 族（Lane 7）覆盖 data-resources 真件；本件与两者均边界清晰、独立留证。

## 二、计算过程

从缺。条目数前提是登记面：UI 层无可数对象（导航无子页）、数据层无目录表（三源证据见 §三）——禁伪计数。复现代码与证据对照见产物 `derived[0]`（负结论留空登记）。

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 数据资产登记面（条目主档） | dev/gkx/久新 | **无表**（dev 登记面样例级 8 条） |
| 数据社区栏目子页/条目列表 | UI | **无**（静态按钮） |
| 科研资源统计面（久新，语义排除参照） | 久新 `ads_*_resource_yearly` | 27,720/985,555/1,408,176 行（论文/人才/经费度量，非条目） |
| 技术社区发现面（久新，语义排除参照） | 久新 `ads_technology_community(_member)` | 1,731/19,430 行（图谱聚类） |

### 3.2 现场复核清单

dev 词族实读：`onl_drag_dataset_head` 87 行/`_item` 232 行/`_param` 5 行（JimuReport 报表数据集配置）。UI 渲染实读：`ScienceGlobalHeader.jsx:60-66` community 项渲染 = 按钮+箭头，无事件。久新列实读：`ads_city_subfield_resource_yearly` 度量列 `paper_count/talent_count/funding_amount_cny`（非条目计数）；`ads_technology_community` 结构列 `community_method/graph_density/member_count`（聚类社区）。

## 四、数据缺失情况

### 4.1 缺口清单

①UI 层无可数对象（导航无子页）；②数据资产登记面无表（dev 仅 BI 配置与样例级数据源登记）；③gkx 无资产管理维；④久新 resource/community 词族语义全排除。

### 4.2 修复建议与影响面

短期：软科学 header community 导航接通 data-resources 路由（语义归位）或建栏目子页。中期：数据资产目录立项（数据集/产品/API 登记面落 `gkxlumenx_ads`，复用 `gen_datasource_conf` 扩容）→ 条目数直查。

### 4.3 影响面

仅本导航项（两处 header 同源）；DATA 族真件不受影响。

## 参考文献

1. OpenDW. Data Catalog Management. https://opendw.io/
2. Data Governance Professionals. Data Asset Inventory Best Practices. https://www.datagovernanceprofessionals.org/
3. demo UI data-resources 模块（语义参照）. `repos/demo-ui-science/src/pages/data-resources/mockData.js:1654`

# 附件

## 附录 A 原始需求原文摘录

- 检索记录：`rg 数据社区` src/pages → 2 处导航按钮（`scienceGlobalHeaderMock.js:50` / `talent-preview/App.jsx:1002`）；三份说明书无「数据社区」功能叶；主需求科技数据资源章的数据共享功能叶归 DATA 族。
- UI：`scienceGlobalHeaderMock.js:50` `{ key: "community", label: "数据社区", hasChildren: true }`（mock 演示配置）。
- 语义参照：`data-resources/mockData.js:1656` `{ label: '资源总量', value: '30,398', unit: '个' }`（手写演示值，不作数据证据）。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_INCUB_031_out.json`）

facts（ui_mounts/ui_mock_note/ui_mock_overview_kpis/dev_table_total_16schema/dev_word_tables/dev_word_rows/dev_semantics_note/dev_word_community/dev_community_note/gkx_table_count/gkx_word_tables/jiuxin_table_count_live/jiuxin_word_tables/jiuxin_semantics_note/named_in_srs/named_note/authoritative_reference）；derived[0]（负结论留空）；absence_probe（四件）；support_judgment=完全不支持；base_years 三键；ctx_refs。

## 附录 C 可行性报告完整版（要点）

行业口径：目录条目 = 已登记数据资产计数（前提登记元数据面）。数据矩阵：三源无目录表；久新 resource/community 词族 9 表逐列语义排除（度量列均非条目计数）。分期方案：一期登记面立项、二期导航接通。风险登记：条目定义需产品裁定（数据集/产品/API 是否合算）。总判：完全不支持。
