# 图谱数据源数量（M_SCIUI_KGANALY_037）

> **类型**：无业务逻辑数值类（数据源面盘点统计型）｜ **域**：科技信息展示系统·科技知识图谱·分析展示·接入面板·数据源列表计数｜ **UI 挂载**：`pages/tech-knowledge-graph/IntegrationEtlPanel.jsx:81`（allSources=[...sources, ...uploaded] 合并计数）
> **数据支持度**：**完全转换支持**（三源数据源面两级盘点实查——登记面 jimu 8 源+物理库域 3 库 1,040 表，计数读数直查可得落产物）｜ **公式定义人**：仿王惠（推测定义——UI integrationDataSources 4 项为 mock，本件以登记面+库域两级口径重建）｜ **口径归属**：需求明列叶（row_01=500，数据源）
> **复现脚本**：`code/M_SCIUI_KGANALY_037.py`｜ **产物**：`code/M_SCIUI_KGANALY_037_out.json`（含登记源名单+三库层域分布）
> **四判定摘要**：直接结构 = **足**（dev jimu 登记面+三库 information_schema/SHOW TABLES 可直查）；直接数据 = **足**（8 登记+542+280+218 表实查在案）；依赖结构 = 足（同左）；依赖数据 = 部分（跨库 lineage 谱系无——登记源与库表对应关系缺失，非计数判定性）
> **数据源口径**：三源（dev live `gkxlumenx_*` + 三方库 gkx + 久新 `gkx_technology_analysis_dev` live）逐一实查；久新 SHOW TABLES 当日实跑 218 表（不写死）；`demo_*` 禁引。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全转换支持。**数据源计数读数两级承载均实查在案：①登记面（UI allSources 合并计数同构）——dev `gkxlumenx_bi.jimu_report_data_source` 8 行（名称/类型列齐，含文件数据源/填报数据源对应 uploaded 语义）；②物理库域——dev 16 schema 542 表（ods 75/dwd 144/ads 96…）+gkx 280 表（dwd 279）+久新 218 活表（SHOW TABLES 当日实跑，全 ads 层）。计数算子（COUNT/合并）**现在就能算**——已实算：登记面 8 源/物理 3 库/合计 1,040 表。唯一缺口=跨库 lineage 谱系（登记源↔库表对应），非计数判定性。判完全转换支持。

### 批次通用纪律摘要（S3-06 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（§2.8 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 无比率算子（纯计数）；层域占比分母=库内总表数 |
| B4 | 负结论带探针 | absence_probe 三件（统一 lineage 目录无/久新上游登记无/gkx 层域在案） |
| B5 | 确定性 | 表清单 sorted；层域 GROUP BY 前缀排序 |
| B6 | 闸门自身被闸 | 不自跑闸门 |
| B7 | 产物只由脚本产出 | 本件 py 实查出 _out.json |
| B9 | 单位/日期陷阱 | 久新表数当日实跑值（215→218 波动在案，勿写死） |
| B10 | 口径裁定保守交付 | 两级口径（登记面/物理库域）分野披露；谱系缺口非计数判定性 |
| B11 | 多本账互推 | gkx 280 与族级共享探针一致；dev 16 schema 与 035 件 cfg 盘点同源 |

### 判档自检三问（本件 = 完全转换支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有数据源承载面吗？ | **有**（登记面+库域两级） | derived[0]（8+542+280+218） |
| 计数原料够吗？ | 够 | jimu 8 行/三库表清单实查 |
| 现在就能算吗？ | **已实算** | 两级计数落产物（§2.5） |

## 摘要

「图谱数据源数量」是接入面板的数据源列表计数（allSources 合并内置源与上传源）。UI mock 4 项（演示层）。数据侧判定：**完全转换支持**——两级口径实查：①登记面（UI 同构主口径）dev jimu 数据源登记 8 个（含「1029608668138668032文件数据源」「填报数据源」等——uploaded 语义在案）；②物理库域 3 库（dev live/gkx/久新 Doris）合计 1,040 表：dev 16 schema 542 表（ods 75→dwd 144→ads 96 数仓三层递进）、gkx 280 表（dwd 279）、久新 218 活表（全 ads 结果层，SHOW TABLES 当日实跑）。唯一缺口=跨库 lineage 谱系（哪张表源自哪个登记源）——不影响计数读数，已在 §4 披露。

- 需求判定：row_01=500 需求明列叶（规模/结构统计语义），无公式。
- 复现状态：脚本已实查通过；两级计数+层域分布落产物。
- 档位结论：**完全转换支持**（两级承载直查+已实算）。
- 关键事实：UI 4 项 mock vs 真实 8 登记源/1,040 库表——演示层严重低估供给面。
- 降档风险：无；升档路径：jimu 登记面直连 UI → 完全直接支持。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技知识图谱 → 分析展示 → 接入面板（`IntegrationEtlPanel.jsx:81` allSources 合并列表）。

### 1.2 为什么需要本指标

数据源数量是图谱供给面的规模读数——多源接入是图谱覆盖度/可信度的前置位（接入面板的列表计数卡）。

### 1.3 需求文档是否给出定义方法

SRS row_01=500 仅给名称（规模/结构统计语义）；UI allSources 为合并计数（sources+uploaded）。本件以登记面+库域两级口径对齐。

### 1.4 类似指标权威方法可行性分析概要

DAMA DMBK 数据源目录/元数据登记管理规范：登记面（catalog）是数据源计数的权威层；数仓分层（Kimball ods/dwd/ads）是物理供给域标准划分。两级口径（登记面/物理域）为元数据管理惯例。

### 1.5 引用来源

1. DAMA International. *DMBOK 2nd ed.* https://www.dama.org/cpages/body-of-knowledge
2. Kimball, R., Ross, M. *The Data Warehouse Toolkit, 3rd ed.* https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/books/data-warehouse-dw-toolkit/
3. Apache Doris. *SHOW TABLES*. https://doris.apache.org/docs/sql-manual/sql-reference/Show-Statements/SHOW-TABLES/

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意**：图谱接入的数据源个数（内置+上传合并计数）。
- **操作化定义**：登记面口径=|jimu_report_data_source|=8（UI 同构）；物理域口径=3 库/1,040 表。
- **降档触发器**：登记面空 → 退物理域口径（未触发：8 行在案）。
- **升档触发器**：jimu 面直连 UI 列表 → 完全直接支持。

### 1.7 需求叶定位与相近叶关系

- 本叶：数据源数量（row_01=500）。
- 相近叶：数据更新频率（036，节律）/接入错误率（035，质量）——接入面板三件套（源数/节律/质量）。

## 二、计算过程

### 2.1 数据源与承载面（三库直查）

dev jimu 登记面（SELECT id,name,type）+dev information_schema（16 schema 计数）+gkx information_schema（280 表+层域）+久新 SHOW TABLES（218 表——Doris 对 information_schema.tables 的 TABLE_SCHEMA 列无权限，SHOW TABLES 替代）。

### 2.2 登记面计数（主实测值·UI 同构口径）

8 个登记源（sorted 名单）：1029608668138668032文件数据源、Local积木平台库、ceshi库、jeecg、localcloud、sqlserver、填报数据源、本地积木库（facts.dev_jimu_names）——含文件/填报源（uploaded 语义）与库源（sources 语义），与 allSources 合并计数同构。

### 2.3 物理库域盘点（主实测值）

| 库 | 表数 | 层域 Top |
|---|---|---|
| dev live（16 schema） | 542 | dwd 144/ods 75/ads 96/bi 41/cms 36 |
| gkx 第三方 | 280 | dwd 279/nums 1 |
| 久新 Doris | 218 | ads 218（单一结果层） |

### 2.4 数仓分层自洽

dev ods(75)→dwd(144)→ads(96) 三层递进；久新全 ads 层与「图谱结果库」定位一致；gkx 全 dwd 层与「第三方明细供给」定位一致——三库层域分工自洽。

### 2.5 两级计数结果

登记面 **8**（UI 同构主口径）；物理域 3 库 **1,040** 表（供给盘点副口径）。derived[0].physical_databases 逐库明细。

### 2.6 需求符合性预评（UI 演示形态 vs 实算形态衔接）

allSources 列表可由 jimu 登记面直供（名称/类型列齐）；uploaded 语义对应文件/填报源在案。

### 2.7 复现代码结果展示

`python3 code/M_SCIUI_KGANALY_037.py` → `M_SCIUI_KGANALY_037_out.json`。

### 2.8 分步证据对照表

| 步骤 | 产物键 | 值 |
|---|---|---|
| 登记源数 | facts.dev_jimu_datasources | 8 |
| 登记源名单 | facts.dev_jimu_names | sorted 8 名 |
| dev 库域 | facts.dev_schema_table_counts | 16 schema/542 表 |
| gkx 表数/层域 | facts.gkx_table_total / gkx_layer_distribution | 280 / dwd 279 |
| 久新表数/层域 | facts.jiuxin_table_total / jiuxin_layer_distribution | 218 / ads 218 |
| 合计 | derived[0].physical_databases | 3 库 1,040 表 |

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 数据源登记面 | dev jimu | 足（8 行名称/类型列） |
| 物理库表清单 | 三库 | 足（1,040 实查） |
| 跨库 lineage 谱系 | 三源 | 无（absence_probe，非计数判定性） |

### 3.2 现场复核清单

information_schema 别名适配（TABLE_SCHEMA AS sch）；久新 SHOW TABLES 替代（权限约束 B9 记录）；gkx 280 与族级探针一致。

## 四、数据缺失情况

### 4.1 统一 lineage 目录缺失（非判定性）

三库独立无统一数据源目录——登记源↔库表对应关系不可内证；计数读数不受影响（两级各自内证）。

### 4.2 口径级待裁项

主口径选择（登记面 8 vs 物理域 3/1,040）供立项裁定；UI allSources 语义与登记面同构已论证。

### 4.3 修复建议与影响面

jimu 登记面直连 IntegrationEtlPanel（升档完全直接支持）；跨库 lineage 需建元数据目录（大工程，非计数必需）。

## 参考文献

1. DAMA International. *DMBOK 2nd ed.*（数据源目录/元数据管理）. https://www.dama.org/cpages/body-of-knowledge
2. Kimball, R., Ross, M. *The Data Warehouse Toolkit, 3rd ed.*（数仓分层供给体系）. https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/books/data-warehouse-dw-toolkit/
3. Apache Doris. *SHOW TABLES — documentation*. https://doris.apache.org/docs/sql-manual/sql-reference/Show-Statements/SHOW-TABLES/

# 附件

## 附录 A 原始需求原文摘录

- SRS row_01=500：图谱数据源数量（实体与连接的规模/结构统计）。
- UI：IntegrationEtlPanel.jsx:81 allSources=[...sources, ...uploaded]（mock 4 项演示层）。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_KGANALY_037_out.json`）

facts（ui_mount/ui_semantics/ui_demo_fallback/srs_anchor/cat/dev_jimu_*/dev_schema_table_counts/gkx_*/jiuxin_*）；derived[0]（physical_databases/registered_datasources_dev_jimu/ui_mock_reference）；absence_probe（3 件）；support_judgment；base_years_used/missing/note。

## 附录 C 可行性报告完整版（要点）

方法谱系：元数据两级口径（登记面 catalog/物理域 inventory）。数据矩阵：登记面 8+物理 1,040 全实查/lineage 缺。结论：完全转换支持。
