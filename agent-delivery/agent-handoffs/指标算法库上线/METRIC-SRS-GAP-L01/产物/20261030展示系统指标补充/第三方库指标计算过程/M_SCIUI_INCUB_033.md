# 时空事件趋势（时序）（M_SCIUI_INCUB_033）

> **类型**：无业务逻辑数值类（时空事件计数时序三源零承载）｜ **域**：科技信息展示系统·时空演变·分布态势「时空事件趋势」时序图｜ **UI 挂载**：`SpaceTimeEvolutionPage.jsx:724`（buildDistributionCharts 实算：regions.yearly events 按年求和）+ `:46`（distributionYears 2022-2026 硬编码）+ `spaceTimeEvolutionMock.js:630`（charts[0] 静态版）+ `:795`（periodStats 短周期双截面）
> **数据支持度**：**完全不支持**｜ **公式定义人**：无（「时空事件」指标名三说明书未出现；时空演变模块为演示页）｜ **口径归属**：UI 派生读数（mock regions.yearly 驱动组件实算 + charts 静态值两套并存）
> **复现脚本**：`code/M_SCIUI_INCUB_033.py`｜ **产物**：`code/M_SCIUI_INCUB_033_out.json`
> **四判定摘要**：直接结构 = 无（dev event 词族 10 表全 0 行、trend 词族仅企业维空壳）；直接数据 = 无（同左）；依赖结构 = **缺**（时空事件事实表三源无表——与 032 共享上游）；依赖数据 = 无（gkx 0 命中；久新 hotspot_yearly 233,160 行为技术热点年度分——语义排除但「年度分×时序衍生列」范式可引）
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

**本件判定：完全不支持。** 时序 = [COUNT(events, y) for y in years]，与 INCUB_032（环差）同源异算、依赖同为「时空事件计数序列」，独立留证同结论：dev event 词族 `gkxlumenx_ads.innovation_event`/`dwd.event_std`/产业链事件族 10 表全 0 行（`demo_` 副本 108,052 行禁引）；trend 词族仅 `enterprise_growth_trend` 0 行（企业维空壳）；gkx trend/spacetime 词族 280 表 0 命中；久新最近邻 `ads_technology_hotspot_yearly` 233,160 行 = 19,430 节点 × 2015-2026，度量列 paper/citation 热点分——语义排除（但其 `hotspot_score_yoy_change`/`rolling_3y_score`/`trend_status` 时序衍生列证明「年度表→时序衍生」加工范式在库成熟）。mock 层组件实算值与 charts 静态值两套不一致，演示态自证。

### 批次通用纪律摘要（S3-07 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 无除式（计数时序） |
| B4 | 负结论带探针 | absence_probe 四件（dev/gkx/久新/mock 自洽核） |
| B5 | 确定性 | 年份网格固定；词族 sorted() |
| B7 | 产物只由脚本产出 | 本件 py 实探产出 _out.json |
| B9 | 单位/日期陷阱 | 单位「条」；年份 2022-2026 为 mock 演示网格 |
| B10 | 口径裁定保守交付 | mock 序列不作数据证据；derived 留 null |
| B11 | 多本账互推 | dev 542/gkx 280/久新 218 与共享快照零漂移 |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有事件计数年度序列吗？ | 无 | dev 事件族 0 行；gkx 0；久新语义排除 |
| 组件实算链有真实数据源吗？ | 无 | regions.yearly 全 mock 手写 |
| 现在就能产出时序吗？ | 不能 | 无序列即无时序 |

## 摘要

「时空事件趋势（时序）」是时空演变模块分布态势区的时序折线（派单挂载组件实算点+mock 静态点双证据）。组件实算链（`SpaceTimeEvolutionPage.jsx:712-737`）：按硬编码 `distributionYears`（2022-2026）对 `regions` 过滤后求和 `getRegionStats(year).events`，得 272/434/600/774/894；mock `charts[0]` 静态版却是 [168,226,284,312,296]（同 metric「1,286」）——两套演示数字不一致。数据侧判**完全不支持**：事件计数年度序列三源零承载（dev 事件族 10 表全 0 行、gkx 0 命中、久新热点年度分为 paper/citation 度量）。本件与 INCUB_032（同序列的环差）共享上游结论、独立留证。

- 需求判定：指标名三说明书未出现；时空演变模块为演示页。
- 复现状态：三源探针+组件实算链实读已跑通；四件 absence_probe 留证。
- 档位结论：**完全不支持**（事件计数时序无法构建）。
- 关键事实：mock `periodStats` 短周期（12m/90d/quarter/month）current/previous 双截面（南山 12m：186/148）与年度序列并存——全部手写，无任何计算源。
- 升档路径：事件事实表落库 → 年度时序+环差+短周期一次到位（032/033 联动升完全转换支持）。

## 一、需求定义概述

### 1.1 所属功能模块

时空演变 → 分布态势 → 「时空事件趋势」时序图。实算链：`SpaceTimeEvolutionPage.jsx:46` `distributionYears` 五年网格硬编码 → `:388-390` `getRegionStats(region, year)` 读 `region.yearly[year]` → `:712-737` `buildDistributionCharts` 求和成 `eventValues` → `{key:"event-trend", values}` 驱动图表；短周期分支（`:718-724` `isShortDistributionPeriod`）走 `region.periodStats[period].current/previous`。

### 1.2 为什么需要本指标

时序回答「事件量按年怎么走」：分布态势区需展示筛选口径（区域/对象类型/周期）下的事件量演变，支撑「持续增长」类判断与回放时间轴联动。

### 1.3 需求文档是否给出定义方法

三份说明书无「时空事件」功能叶。**固定句式：三份说明书未给出该指标的计算方法。**

### 1.4 类似指标权威方法可行性分析概要

事件计数时序方法族（要点版，完整版指向附录 C）：①GDELT 事件库——按日/周/月计数作时间序列（更新频率固定、时区披露）；②OECD MSTI 年度指标时序惯例——固定年份网格+缺失年显式标注（不插零）；③久新 hotspot_yearly 衍生列范式——`yoy_change`/`rolling_3y`/`trend_status` 证明年度表→时序衍生加工在库成熟。

### 1.5 引用来源

1. GDELT Project. Event Database — Updates and Frequency. https://www.gdeltproject.org/
2. OECD. Main Science and Technology Indicators（年度时序口径）. https://www.oecd.org/en/data/datasets/main-science-technology-indicators.htm
3. 久新 `ads_technology_hotspot_yearly` 时序衍生列（结构范式参照，语义排除）

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意**：筛选口径下时空事件量的年度（或短周期）计数序列，驱动趋势折线与「持续增长」badge。
- **操作化定义**：series[y] = COUNT(事件事实表 WHERE year=y AND 筛选条件)，年份网格固定、缺失年显式标注。
- **降档触发器**：已处最低档。
- **升档触发器**：事件事实表落库 → 完全转换支持。

### 1.7 需求叶定位与相近叶关系

- 本叶：时空演变·分布态势（演示模块派生命名）。
- 相近叶：INCUB_032 同源异算（序列 vs 环差）共享三源结论；INCUB_020 共享 `enterprise_growth_trend` 空壳结论；INCUB_034 是软科学侧通用趋势件（不同模块，判档独立）。

## 二、计算过程

从缺。时序需事件计数序列作输入（§1.4 GDELT/OECD 口径），三源探针（附录 B 四件）证明：dev 事件族全 0 行、gkx 0 命中、久新语义排除——无序列即无时序，禁伪序列。mock 两套数字（实算链 vs charts 静态）均为演示值不作数据证据。复现代码与证据对照见产物 `derived[0]`（负结论留空登记）。

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 时空事件事实表 | dev/gkx/久新 | **无表**（dev 事件族空壳） |
| 事件计数年度序列 | 同上 | **无**（与 032 共享） |
| 年度表→时序衍生范式 | 久新 `ads_technology_hotspot_yearly` | 233,160 行，衍生列 `yoy_change/rolling_3y_score/trend_status`（范式可引） |
| mock 演示序列 | UI mock | 实算 272/434/600/774/894 与静态 [168,226,284,312,296] 两套并存 |

### 3.2 现场复核清单

dev 实读：事件族 10 表 0 行（`event_type` 字典 12 行）；trend 词族 `enterprise_growth_trend` 0 行。久新实读：`hotspot_yearly` 2015-2026 各 19,430 行（12 年完整网格——范式成熟），列含 `paper_activity_score/citation_attention_score/hotspot_score`（技术热点分度量）。组件实读：短周期双截面分支与年度分支并存；`getRegionStats` 缺年回退末年（`:389` fallback）——实算链对缺年不敏感，全靠 mock 手填。

## 四、数据缺失情况

### 4.1 缺口清单

①事件事实表无承载；②年度序列无表；③事件类型口径未定义（同 032）；④年份网格硬编码 2022-2026（无动态范围）。

### 4.2 修复建议与影响面

短期：事件口径裁定+年份网格参数化。中期：事件事实表落 `gkxlumenx_dwd`（仿久新年度表结构+dev `event_std` 骨架）→ 时序/环差/短周期双截面一次到位（032/033 联动升档）。

### 4.3 影响面

分布态势时序图、趋势洞察段、时间轴回放 metrics 全为 mock；INCUB_032 同源受累。

## 参考文献

1. GDELT Project. Event Database — Updates and Frequency. https://www.gdeltproject.org/
2. OECD. Main Science and Technology Indicators. https://www.oecd.org/en/data/datasets/main-science-technology-indicators.htm
3. 久新 `ads_technology_hotspot_yearly`（结构范式参照）. 久新库 live 实读列证

# 附件

## 附录 A 原始需求原文摘录

- 检索记录：`rg 时空事件` 三份说明书 + 主需求 → 0 命中；派单清单 §1 定名「时空事件趋势（时序）」（挂载组件 `:724` + mock `:630` 双点）。
- mock 原文（`spaceTimeEvolutionMock.js:630-636`）：`{ key: "event-trend", title: "时空事件趋势", metric: "1,286", unit: "条", badge: "持续增长", values: [168, 226, 284, 312, 296] }`（演示值）。
- 组件实算（`SpaceTimeEvolutionPage.jsx:724` 附近）：`years.map((year) => regions.filter(...).reduce((total, region) => total + (getRegionStats(region, year).events ?? 0), 0))`（mock 驱动）。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_INCUB_033_out.json`）

facts（ui_mounts/ui_mock_computed_series/ui_mock_chart_static_values/ui_mock_periodstats_12m_head/ui_mock_semantics_note/dev_table_total/dev_event_word_rows/dev_event_note/dev_trend_word_tables/dev_trend_word_rows/dev_trend_note/gkx_table_count/gkx_word_tables/gkx_note/jiuxin_table_count_live/jiuxin_nearest_rows/jiuxin_hotspot_yearly_trend_cols/jiuxin_semantics_note/named_in_srs/named_note/authoritative_reference）；derived[0]（负结论留空）；absence_probe（四件）；support_judgment=完全不支持；base_years 三键；ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：GDELT 计数时序 → OECD 年度网格惯例（缺失年显式标注）→ 久新衍生列范式。数据矩阵：dev 事件族空壳、gkx 0、久新范式在库语义排除。mock 自洽性：实算链与静态 charts 两套数字不一致。分期方案：一期口径裁定+网格参数化、二期事实表落库。风险登记：事件定义边界+短周期窗口口径需产品裁定。总判：完全不支持。
