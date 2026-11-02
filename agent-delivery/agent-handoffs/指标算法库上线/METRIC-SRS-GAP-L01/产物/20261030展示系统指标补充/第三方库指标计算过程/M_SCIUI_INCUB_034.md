# 指标时间趋势分析（通用）（M_SCIUI_INCUB_034）

> **类型**：简单统计类（通用时序容器·软科学三序列上游主档三源零承载）｜ **域**：科技信息展示系统·软科学成果展示·时空工作台·「时间趋势分析」中心舞台 Tab｜ **UI 挂载**：`SoftScienceWorkbench.jsx:22`（stageTabs trend 项）+ `:731/:941`（resolvedTrendSeries→SoftScienceTrendAnalysis）+ `softScienceHomepageMock.js:339-378`（trendSeries 3 序列）+ `SoftDesignSystem.test.jsx:129/138`（Tab 契约测试）
> **数据支持度**：**完全不支持**｜ **公式定义人**：无（「指标时间趋势分析」指标名三说明书未出现；软科学 SRS 仅「趋势分析」功能分句——成果数量/转化效率按时间分布观察）｜ **口径归属**：UI 派生读数（mock trendSeries 3 序列×12 点手写；容器为纯前端几何渲染）
> **复现脚本**：`code/M_SCIUI_INCUB_034.py`｜ **产物**：`code/M_SCIUI_INCUB_034_out.json`
> **四判定摘要**：直接结构 = 无（dev trend 词族仅企业维空壳表）；直接数据 = 无（同左）；依赖结构 = **缺**（三序列上游主档——课题成果主档/转化过程表/成果×区域关联面——三源全无表）；依赖数据 = 无（gkx 要素库无软科学成果维；久新 resource_yearly 27,720 行年度网格可作通用容器演示源——但为科研资源语义非本件口径）
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

**本件判定：完全不支持。** 本件是「通用容器件」：容器逻辑（归一化折线/面积几何 + trend 方向标注）前端已备（`SoftScienceTrendAnalysis.jsx` 纯几何渲染无数据接口），判档看序列数据面——mock 3 序列（成果数量 bar 项/转化效率 line 个月/重点区域贡献 area %）对应三类典型指标（计数/均值/占比），其上游：课题成果主档无表（INCUB_022 已证）、转化周期过程表无承载（词族 convert/transfer 0 命中）、成果×区域关联面无表；dev trend 词族仅 `enterprise_growth_trend` 0 行；gkx trend 0 命中（要素库无软科学成果维）；久新 `ads_city_subfield_resource_yearly` 27,720 行年度网格结构完整——通用时序容器的演示数据源在库，但科研资源语义非本件软科学口径。容器无真实序列可载。

### 批次通用纪律摘要（S3-07 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 占比序列（focus-city-share %）口径披露同基 |
| B4 | 负结论带探针 | absence_probe 四件（dev 上游/gkx/久新/UI 接口） |
| B5 | 确定性 | 序列点按 mock 文件序；词族 sorted() |
| B7 | 产物只由脚本产出 | 本件 py 实探产出 _out.json |
| B9 | 单位/日期陷阱 | 三序列单位异（项/个月/%）逐一披露；月粒度 2025.05-2026.04 |
| B10 | 口径裁定保守交付 | 久新演示源可引与语义排除分开写；derived 留 null |
| B11 | 多本账互推 | dev 542/gkx 280/久新 218 与共享快照零漂移 |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 容器有真实序列可载吗？ | 无 | 三序列上游主档三源全缺 |
| 前端有统计计算吗？ | 无 | 纯归一化几何渲染 |
| 久新年度表能顶替吗？ | 语义不符 | 科研资源语义非软科学口径（可作换语义演示源） |

## 摘要

「指标时间趋势分析（通用）」是软科学时空工作台「时间趋势分析」Tab 的通用多序列趋势看板：mock `trendSeries` 3 序列×12 点（2025.05-2026.04）——成果数量（bar，1,880→2,486 项，up「规模仍在上行区间」）、转化效率（line，8.8→7.4 个月，down「周期持续缩短」）、重点区域贡献（area，59.4%→68.2%，up「集聚程度继续增强」）。容器逻辑前端已备（`SoftScienceTrendAnalysis.jsx` 归一化几何+方向标注，无数据接口），但三序列上游主档（课题成果主档/转化过程表/成果×区域关联面）三源全缺（dev `enterprise_growth_trend` 空壳、gkx 无软科学维、久新 resource_yearly 为科研资源语义）——容器无真实序列可载，判**完全不支持**。

- 需求判定：指标名三说明书未出现；软科学 SRS 仅「趋势分析」功能分句（行为描述非定义）。
- 复现状态：三源探针+组件/测试双挂载实读已跑通；四件 absence_probe 留证。
- 档位结论：**完全不支持**（通用容器的序列数据面零承载）。
- 关键事实：`trend/trendLabel` 判读是 mock 常数非计算值——「通用」仅指容器形态；三序列对应计数/均值/占比三类典型指标口径（第三类同基相除）。
- 升档路径：成果主档+转化过程表落库 → 三序列可算 = 完全转换支持；或容器接入久新 resource_yearly 作科研资源趋势（换语义需产品裁定）。

## 一、需求定义概述

### 1.1 所属功能模块

软科学成果展示 → 时空工作台 → 「时间趋势分析」中心舞台 Tab（`SoftScienceWorkbench.jsx:22-26` stageTabs 第 2 项）。数据链：`:731` `resolvedTrendSeries = asArray(workbench.trendSeries)` → `:941` `<SoftScienceTrendAnalysis series>` 渲染；mock 源 `softScienceHomepageMock.js:339-378`（3 序列×12 点）。渲染层 `SoftScienceTrendAnalysis.jsx`：`buildChartGeometry`（min/max 归一化坐标）、`buildLinePath/buildAreaPath`（几何）、`formatMetricValue`（单位感知格式化：个月/% 一位小数）——纯前端无接口。契约测试 `SoftDesignSystem.test.jsx:129/138`（Tab 切换）。

### 1.2 为什么需要本指标

趋势 Tab 回答「盘面按月怎么走」：成果规模是否持续扩张（数量）、转化效率是否改善（周期缩短）、空间分布是否向核心区收敛（贡献占比）——软科学 SRS「趋势分析」功能分句的落点（成果数量/转化效率按时间分布观察）。

### 1.3 需求文档是否给出定义方法

三份说明书无此指标名；软科学 SRS 仅功能分句。**固定句式：三份说明书未给出该指标的计算方法。**

### 1.4 类似指标权威方法可行性分析概要

通用时序分析方法族（要点版，完整版指向附录 C）：①OECD MSTI——指标×年份矩阵，缺失年显式标注；②Hyndman & Athanasopoulos《FPP3》趋势成分分析——斜率/移动平均定方向，窗口需注明；③久新 `hotspot_yearly` 衍生列范式（`trend_status`/`rolling_3y_score`）——趋势判读加工在库成熟。mock 三序列恰对应三类典型指标：计数（项）/均值（个月）/占比（%，同基相除）。

### 1.5 引用来源

1. OECD. Main Science, Technology and Innovation Indicators. https://www.oecd.org/en/data/datasets/main-science-technology-indicators.htm
2. Hyndman & Athanasopoulos. Forecasting: Principles and Practice (3rd ed.) — Trend. https://otexts.com/fpp3/trend.html
3. 久新 `ads_city_subfield_resource_yearly`（通用容器演示数据源参照，语义排除）. 久新库 live 实读

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意**：软科学核心指标的多序列月度趋势看板，方向判读（up/down + 文案）辅助决策。
- **操作化定义**：每指标产出 points[(label, value)]；方向 = 窗口斜率或首尾比较（FPP3 口径注明窗口）；占比序列同基相除。
- **降档触发器**：已处最低档。
- **升档触发器**：成果主档+转化过程表落库 → 完全转换支持。

### 1.7 需求叶定位与相近叶关系

- 本叶：软科学·时空工作台·趋势 Tab（通用容器件）。
- 相近叶：INCUB_022/020 上游结论共享（成果主档无表/growth_trend 空壳）；INCUB_032/033 是时空演变侧时序件（不同模块独立留证，同判完全不支持）。

## 二、计算过程

从缺。容器件需真实序列作输入（§1.4 OECD/FPP3 口径），三源探针（附录 B 四件）证明三序列上游主档全缺——容器无序列可载，禁伪序列。mock 3 序列×12 点为演示值不作数据证据。复现代码与证据对照见产物 `derived[0]`（负结论留空登记）。

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 课题成果主档（数量序列上游） | dev/gkx/久新 | **无表**（INCUB_022 已证） |
| 转化过程表（周期序列上游） | 同上 | **无表**（词族 convert/transfer 0 命中） |
| 成果×区域关联面（占比序列上游） | 同上 | **无表** |
| 通用容器演示源 | 久新 `ads_city_subfield_resource_yearly` | 27,720 行年度网格（科研资源语义——可引需换语义） |

### 3.2 现场复核清单

mock 实读：`trendSeries[0]` points 12 点 1,880→2,486（首尾三点产物留痕）；`[1]` 8.8→7.4；`[2]` 59.4→68.2；trend/trendLabel 三序列均常数标注。组件实读：`SoftScienceTrendAnalysis.jsx:11-40` `buildChartGeometry` 归一化（max==min 时 0.5 居中）；`formatMetricValue` 单位感知（个月/% 一位小数）。久新实读：`city_subfield_resource_yearly` 27,720 行（city×subfield×2015-2026 年度网格，paper_count/talent_count/funding 度量）。

## 四、数据缺失情况

### 4.1 缺口清单

①成果主档无表（数量序列缺）；②转化过程表无承载（周期序列缺）；③区域关联面无表（占比序列缺）；④方向判读口径未定（窗口/方法需产品裁定）。

### 4.2 修复建议与影响面

短期：三序列口径裁定（窗口/粒度/判读方法按 FPP3 披露）。中期：成果主档+转化过程表落 `gkxlumenx_dwd` → 月度序列可算；通用容器框架（前端已备）直接复用——本件与 INCUB_022 联动升档。

### 4.3 影响面

趋势 Tab 三卡片、trendInsights 判读卡（当前判断/风险提示/建议动作）全为 mock；工作台三 Tab 中唯一无真实数据接入的 Tab。

## 参考文献

1. OECD. Main Science, Technology and Innovation Indicators. https://www.oecd.org/en/data/datasets/main-science-technology-indicators.htm
2. Hyndman & Athanasopoulos. Forecasting: Principles and Practice — Trend. https://otexts.com/fpp3/trend.html
3. 久新 `ads_city_subfield_resource_yearly`（演示源参照）. 久新库 live 实读列证

# 附件

## 附录 A 原始需求原文摘录

- 检索记录：`rg 时间趋势分析` 三份说明书 → 指标名 0 命中；软科学 SRS 有「趋势分析」功能分句（成果数量/转化效率按时间分布观察——行为描述）。
- mock 原文（`softScienceHomepageMock.js:341-343`）：`{ key: "total-results", title: "成果数量趋势", … trend: "up", trendLabel: "规模仍在上行区间", points: [{ label: "2025.05", value: 1880 }, …] }`（演示值）。
- 组件（`SoftScienceWorkbench.jsx:941`）：`<SoftScienceTrendAnalysis series={resolvedTrendSeries} />`（mock 直取渲染）。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_INCUB_034_out.json`）

facts（ui_mounts/ui_mock_series/ui_mock_semantics_note/dev_table_total/dev_trend_word_tables/dev_trend_word_rows/dev_upstream_note/gkx_table_count/gkx_word_tables/gkx_note/jiuxin_table_count_live/jiuxin_resource_yearly/jiuxin_semantics_note/named_in_srs/named_note/authoritative_reference）；derived[0]（负结论留空）；absence_probe（四件）；support_judgment=完全不支持；base_years 三键；ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：OECD 指标×年份矩阵 → FPP3 趋势成分（斜率/移动平均，窗口披露）→ 久新 trend_status 范式。数据矩阵：三序列上游全缺（主档/转化/区域关联）；久新 27,720 行年度网格可作换语义演示源。分期方案：一期口径裁定、二期主档+转化表落库。风险登记：判读口径（窗口/方法）需产品裁定并披露；占比序列同基披露。总判：完全不支持。
