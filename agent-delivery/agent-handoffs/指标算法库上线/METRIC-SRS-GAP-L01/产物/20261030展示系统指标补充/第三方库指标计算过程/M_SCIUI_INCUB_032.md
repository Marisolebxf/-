# 时空事件增长量（较上期）（M_SCIUI_INCUB_032）

> **类型**：无业务逻辑数值类（时空事件计数序列三源零承载）｜ **域**：科技信息展示系统·时空演变·趋势洞察「时空事件增长」段｜ **UI 挂载**：`spaceTimeEvolutionMock.js:803-809`（trendSections[0] metric 1,286 条 values[272,434,600,774,894]）+ `:630-636`（charts[0] 同 metric 异 values）+ `SpaceTimeEvolutionPage.jsx:712-737`（buildDistributionCharts 实算：regions.yearly events 按年求和）
> **数据支持度**：**完全不支持**｜ **公式定义人**：无（「时空事件」指标名三说明书未出现；时空演变模块为演示页）｜ **口径归属**：UI 派生读数（mock regions.yearly 驱动；「较上期」按环差口径 period-over-period difference 重建）
> **复现脚本**：`code/M_SCIUI_INCUB_032.py`｜ **产物**：`code/M_SCIUI_INCUB_032_out.json`
> **四判定摘要**：直接结构 = 无（dev event 词族 10 表全 0 行、trend 词族仅空壳 growth_trend）；直接数据 = 无（同左）；依赖结构 = **缺**（时空事件事实表——区域×对象类型×时间事件流——三源无表）；依赖数据 = 无（gkx 0 命中；久新 hotspot_yearly 233,160 行为技术热点年度分，无事件实体计数维——语义排除但结构范式可引）
> **数据源口径**：三源（dev live `10.50.11.76` `gkxlumenx_*` 非 demo + 三方库 gkx + 久新 `gkx_technology_analysis_dev` live 218 表复核）逐一探针留证；`demo_*` 禁引（demo 事件副本 108,052 行等不引）；mock 值仅作需求语义证据。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库与久新库**均无法构建 |

**四判定**：表结构直接支持 / 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全不支持。** 环差 = 当期事件量 − 上期事件量，前提是时空事件计数序列：dev event 词族 `gkxlumenx_ads.innovation_event`/`dwd.event_std`/产业链事件族等 10 表全 0 行（`demo_` 副本有数据但禁引，且语义为产业链/机构事件非时空事件）；trend 词族仅 `enterprise_growth_trend` 0 行（企业维空壳，INCUB_020 已证）；gkx trend/spacetime 词族 280 表 0 命中；久新最近邻 `ads_technology_hotspot_yearly` 233,160 行 = 19,430 技术节点 × 2015-2026 各年，度量列 `paper_count/new_citation_count/hotspot_score`——技术热点年度分语义，无「事件」实体计数维。mock 层三套数字互不一致（trendSections values vs charts values vs metric 1,286 无可对齐口径），演示态自证。

### 批次通用纪律摘要（S3-07 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 无除式（环差为减法） |
| B4 | 负结论带探针 | absence_probe 五件（dev 事件面/时序面/gkx/久新/mock 自洽核） |
| B5 | 确定性 | mock 正则实读汇总；词族 sorted() |
| B7 | 产物只由脚本产出 | 本件 py 实探产出 _out.json |
| B9 | 单位/日期陷阱 | 单位「条」；mock 年份 2022-2026 为演示标注 |
| B10 | 口径裁定保守交付 | mock 环差不作数据证据；derived 留 null |
| B11 | 多本账互推 | dev 542/gkx 280/久新 218 与共享快照零漂移 |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有事件计数序列吗？ | 无 | dev 事件族 0 行；gkx 0；久新语义排除 |
| 有可替代的时序度量吗？ | 结构可引语义不符 | 久新 hotspot_yearly 为 paper/citation 度量 |
| 现在就能算环差吗？ | 不能 | 无序列即无环差 |

## 摘要

「时空事件增长量（较上期）」是时空演变模块趋势洞察段「时空事件增长」的派生读数（派单措辞「较上期」= 环差：当期 − 上期，绝对条数）。mock 层脚本实读：`regions` 4 区域 `yearly.events` 按年求和 = 272/434/600/774/894（2022-2026），环差 +162/+166/+174/+120；但 trendSections 与 charts 两处 metric 同为「1,286」却与当期 894、累计 2,974 均不等，且两处 values 数组互不相同——mock 三套数字无法对齐，演示态自证。数据侧判**完全不支持**：时空事件计数序列三源零承载（dev 事件族 10 表全 0 行、gkx 0 命中、久新热点年度分无事件维）。

- 需求判定：指标名三说明书未出现；时空演变模块为演示页。
- 复现状态：三源探针+mock 正则实读已跑通；五件 absence_probe 留证。
- 档位结论：**完全不支持**（事件计数序列——本指标与 033 的共同上游——三源无法构建）。
- 关键事实：dev `demo_gkxlumenx_*` 事件副本有数据（`industry_chain_news_event` 108,052 行、`svc_org_finance_event` 15,755 行），按铁律禁引——非 demo 侧同名表全 0 行，空壳结构坐实。
- 升档路径：时空事件事实表（区域×对象类型×时间）落库 → 计数序列+环差可算 = 完全转换支持。

## 一、需求定义概述

### 1.1 所属功能模块

时空演变 → 趋势洞察 → 「时空事件增长」段（`spaceTimeEvolutionMock.js:803-809` trendSections[0]：metric「1,286」unit 条 badge 持续增长 values 五点）。组件侧实算链：`SpaceTimeEvolutionPage.jsx:712-737` `buildDistributionCharts` 按 `distributionYears`（2022-2026）对 `regions` 过滤求和 `getRegionStats(region, year).events`（`:388-390` 读 `region.yearly[year]`）；短周期（12m/90d/quarter/month）走 `region.periodStats[period].current/previous` 双截面。

### 1.2 为什么需要本指标

环差回答「事件量在涨还是跌、涨多少条」：趋势洞察段以 badge「持续增长」作定性标注，需定量锚（较上期 +N 条）支撑区域创新活跃度的期际比较。

### 1.3 需求文档是否给出定义方法

三份说明书无「时空事件」功能叶。**固定句式：三份说明书未给出该指标的计算方法。**（「较上期」措辞来自派单清单 §1 定名。）

### 1.4 类似指标权威方法可行性分析概要

环差方法族（要点版，完整版指向附录 C）：①US Census Bureau「change from preceding period」——增长量 = 当期值 − 上期值（绝对量非率）；②BEA 环差惯例同式；③GDELT 事件库——事件按日计数作时序源（事件计数语义参照）。本件「较上期」与①②一致。

### 1.5 引用来源

1. US Census Bureau. Quarterly Reports — change from preceding period. https://www.census.gov/
2. BEA. GDP Change from Preceding Period（环差口径）. https://www.bea.gov/data/gdp/gdp-by-state
3. GDELT Project. Event Database（事件计数时序）. https://www.gdeltproject.org/

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意**：时空事件（区域创新事件：协同项目验收/团队流动/专利转化节点等 mock `eventItems` 语义）当期较上期的净增条数。
- **操作化定义**：增长量 = COUNT(events, T) − COUNT(events, T−1)，T 为年度（mock 序列年粒度）。
- **降档触发器**：已处最低档。
- **升档触发器**：事件事实表落库 → 完全转换支持。

### 1.7 需求叶定位与相近叶关系

- 本叶：时空演变·趋势洞察（演示模块派生命名）。
- 相近叶：INCUB_033（时空事件趋势）共享事件计数序列上游——033 是序列本身、032 是序列环差，同源异算独立留证；INCUB_020 共享 `enterprise_growth_trend` 空壳结论。

## 二、计算过程

从缺。环差需事件计数序列作输入（§1.4 环差式），三源探针（附录 B 五件）证明：dev 事件族 10 表全 0 行、时序面空壳、gkx 0 命中、久新热点年度分无事件维——无序列即无环差，禁伪算。mock 环差 +162/+166/+174/+120 为演示值不作数据证据。复现代码与证据对照见产物 `derived[0]`（负结论留空登记）。

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 时空事件事实表（区域×对象×时间） | dev/gkx/久新 | **无表**（dev 事件族空壳） |
| 事件计数年度序列 | 同上 | **无** |
| 分年计数结构范式 | 久新 `ads_technology_hotspot_yearly` | 233,160 行（19,430 节点×12 年；paper/citation 度量——范式可引） |
| mock 演示序列 | UI mock | 272/434/600/774/894（三套数字不自洽） |

### 3.2 现场复核清单

dev 实读：`gkxlumenx_ads.innovation_event` 0 行/`dwd.event_std` 0 行/产业链事件 5 表全 0 行/`event_relation` 0 行（`event_type` 字典 12 行）；demo 副本 `industry_chain_news_event` 108,052 行禁引。久新实读：`hotspot_yearly` 2015-2026 各 19,430 行（均衡分布=节点全量快照），列 `paper_count/new_citation_count/hotspot_score/hotspot_score_yoy_change`——注意其自带 `yoy_change` 是分数环差非事件环差。组件实读：`SpaceTimeEvolutionPage.jsx:718-724` 短周期双截面（current/previous）与年度单序列两分支——mock `periodStats` 有 12m 环差对（186/148 等），同为演示值。

## 四、数据缺失情况

### 4.1 缺口清单

①时空事件事实表无承载（对象缺）；②事件计数序列无表（序列缺）；③事件类型字典仅 12 行 demo 级；④区域×对象×时间三维度口径未定义（需产品裁定哪些行为算「事件」）。

### 4.2 修复建议与影响面

短期：事件类型口径裁定（协同项目/团队流动/转化节点等 mock eventItems 语义产品化）。中期：事件事实表落 `gkxlumenx_dwd`（可仿久新 hotspot_yearly 的维度×年份结构 + dev `event_std` 空壳骨架扩容）→ 年度序列+环差+短周期双截面一次到位（032/033 联动升档）。

### 4.3 影响面

趋势洞察段两卡片（事件增长/路径强度）、分布图 event-trend、时间轴回放 metrics.events 全为 mock；INCUB_033 同源受累。

## 参考文献

1. US Census Bureau. Quarterly Reports — change from preceding period. https://www.census.gov/
2. BEA. GDP by State — change from preceding period. https://www.bea.gov/data/gdp/gdp-by-state
3. GDELT Project. Event Database. https://www.gdeltproject.org/

# 附件

## 附录 A 原始需求原文摘录

- 检索记录：`rg 时空事件` 三份说明书 + 主需求 → 0 命中（时空演变模块无 SRS 功能叶）；派单清单 §1 定名「时空事件增长量（较上期）」。
- mock 原文（`spaceTimeEvolutionMock.js:803-809`）：`{ key: "events", title: "时空事件增长", metric: "1,286", unit: "条", badge: "持续增长", values: [272, 434, 600, 774, 894] }`（演示值）。
- 组件实算（`SpaceTimeEvolutionPage.jsx:712-737`）：regions→`getRegionStats(year).events` 求和链（mock 驱动）。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_INCUB_032_out.json`）

facts（ui_mounts/ui_mock_yearly_events/ui_mock_yearly_events_note/ui_mock_period_diff/ui_mock_inconsistency/ui_mock_semantics_note/dev_table_total/dev_event_word_rows/dev_event_note/dev_trend_word_tables/dev_trend_word_rows/dev_trend_note/gkx_table_count/gkx_word_tables/gkx_note/jiuxin_table_count_live/jiuxin_nearest_rows/jiuxin_hotspot_yearly_by_year/jiuxin_semantics_note/named_in_srs/named_note/authoritative_reference）；derived[0]（负结论留空）；absence_probe（五件）；support_judgment=完全不支持；base_years 三键；ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：Census/BEA 环差（当期−上期绝对量）→ GDELT 事件计数时序。数据矩阵：dev 事件族空壳（非 demo 全 0 行）、gkx 0、久新热点年度分（范式可引无事件维）。mock 自洽性：三套数字（trendSections values/charts values/metric 1,286）互不一致。分期方案：一期事件口径裁定、二期事实表落库。风险登记：事件定义边界（哪些行为入计）需产品裁定。总判：完全不支持。
