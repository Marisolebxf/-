# M_SCIUI_SOFTSCI_009 转化效率趋势 —— 指标信息 MD

> **类型**：简单统计类｜ **域**：软科学成果展示·时间趋势分析·转化效率趋势（SoftScienceWorkbench.jsx:941+softScienceHomepageMock.js:352，清单空实查定位）
> **数据支持度**：**完全不支持**｜ **UI 挂载**：科技信息展示系统 → 软科学成果展示 → 时间趋势分析「转化效率趋势」（`SoftScienceWorkbench.jsx:941`+`softScienceHomepageMock.js:352`，清单空实查定位）｜ **公式定义人**：无（指标名三源 0 命中；「转化效率」双时点口径无定义）
> **复现脚本**：`code/M_SCIUI_SOFTSCI_009.py`｜ **产物**：`code/M_SCIUI_SOFTSCI_009_out.json`
> **口径归属**：UI 挂载件，SRS 无同名指标｜ **数据源口径**：本件支持度按「开发库 live（10.50.11.76:3306，gkxlumenx_*，禁 demo_*/_devdb）+ 三方库（gkx，183.240.141.251:3318 只读）+ 久新库（jiuxin，Doris 47.93.119.170:29030）」三源评估
> **铁律：本指标所有信息，均以第二章的“最新指标调研报告”为准。第一章指标信息为历史版本，不用作参考。**
> **四判定摘要**：直接结构=无；直接数据=无；依赖结构=无（dwd_patent_transfer 22,809 行仅单时点 18 列断言）；依赖数据=无（双时点原料缺，趋势不可算）

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源中存在数据量充分的相关表/字段，仅需口径转换/间接计算（无额外数据采集）即可产出本指标 |
| **部分支持** | 三源中存在部分可复用表/字段，**只可计算本指标的部分子项**（或关键维度缺失） |
| **完全不支持** | 三源均无承载，需新建数据链路/外部接入 |

**本件判定：完全不支持。**（平均转化周期需项目双时点，三源零承载）。

### 批次通用纪律摘要（S3-07 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B5 | 列表 sorted() | 基期年份/ctx_refs sorted |
| B7 | 数字-出处核对 | 22,809/年分布/12 点序列均已对产物键（附录 B） |
| B10 | ui_demo_fallback 披露 | mock 8.8→7.4 披露 |
| 基期三键 | base_years_used/missing/note | 产物全键 |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有现成周期结果面吗？ | 无 | 三源 conversion 词族命中表均无 cycle/duration/period 列（列级断言 cycle_like=[]） |
| 有项目双时点可算周期吗？ | 无 | dwd_patent_transfer 仅 transfer_effective_date 单时点 |
| 有代理路径吗？ | 无 | jiuxin ads_technology_transfer_stage 是阶段占比快照非周期时长 |

## 摘要

「转化效率趋势」是软科学成果页时间趋势分析面板的第二张图：折线展示「平均转化周期（个月）」12 点月序列（2025.05=8.8 → 2026.04=7.4，累计缩短 1.4 个月），摘要句由 `SoftScienceTrendAnalysis.jsx:97-104` 生成。数据侧判定：**完全不支持**——平均转化周期需项目级双时点（立项日+示范落地日），三源 conversion 词族命中表（dev/gkx `dwd_patent_transfer`、jiuxin `ads_technology_transfer_stage`）均无周期语义：专利转让表只有权属变更生效日单时点（权属变更≠成果转化落地），久新表是技术阶段分布快照。权威侧《中国科技成果转化年度报告》口径为转化合同数/收入，无周期指标——周期类读数属平台自设运营指标。

- 需求判定：指标名三份说明书未出现；派单书清单挂载点空，实查定位至 soft-science 模块趋势面板（附录 A）。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技成果展示 → 软科学成果 → 工作台「时间趋势分析」tab（`SoftScienceWorkbench.jsx:22` stage-tab-trend / `:933-944` tabpanel 渲染）→ 图表卡「转化效率趋势」（trendSeries[1]，`softScienceHomepageMock.js:352-359`；图表 aria-label=转化效率趋势图，`SoftScienceTrendAnalysis.jsx:212-215,247`）。同面板另有成果数量趋势（bar）/重点区域贡献趋势（area）两系列。

### 1.2 为什么需要本指标

转化周期是成果转化效率的时效读数：周期缩短=立项到示范落地的链路提速。管理者需要月度序列判断转化节奏是否持续改善（mock note「用来确认成果从立项到示范落地的效率是否继续改善」）。

### 1.3 需求文档是否给出定义方法

三份说明书未出现该指标名（检索记录见附录 A）。**固定句式：三份说明书未给出该指标的计算方法。**（派单书清单挂载点空，本件挂载为实查定位。）

### 1.4 类似指标权威方法可行性分析概要

权威口径方法族（完整版指向附录 C）：①《中国科技成果转化年度报告（2025）》：转化合同数/合同金额/现金+股权分红——**无周期指标**；②科技部成果转化倾斜指标（转让/许可/作价投资三分法）：事件计数口径，同样无周期；③项目管理双时点法（业界 PMS 通用）：周期=落地时点−立项时点，均值按月聚合。周期属平台自设运营指标，无国标强制口径。

### 1.5 引用来源

1. 财政部、科技部. 中国科技成果转化年度报告（2025）发布稿. https://www.most.gov.cn/kjbgz/202502/t20250228_194265.html
2. 科技部. 促进科技成果转化法实施细则配套——转化方式（转让/许可/作价投资）. https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/fgzc/gfxwj/gfxwj2023/202311/t20231123_188692.html
3. 全国人大. 中华人民共和国促进科技成果转化法（2015 修订）. https://www.gov.cn/zhengce/2021-10/29/content_5647701.htm

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意**：软科学成果（政策研究/战略规划/评估评价类）从项目立项到成果示范落地的平均时长（月），按月滚动观测。
- **操作化定义（权威重建式，本件未实现）**：月度平均转化周期 = mean(落地时点ᵢ − 立项时点ᵢ)，样本为当月落地项目集合。
- **降档触发器**：已处最低档。
- **升档触发器**：项目表（立项日+落地日双时点）入湖（如科技计划项目库）→ 完全转换支持；软科学成果管理平台周期接口直连 → 完全直接支持。

### 1.7 需求叶定位与相近叶关系

- 本叶：软科学成果·时间趋势分析·转化效率趋势（折线）。
- 相近叶：同面板成果数量趋势（SOFTSCI 族邻号语义）/重点区域贡献趋势；gkx/dev `dwd_patent_transfer`（S3-07 批共享探针已采年分布 22,522 有年份+287 无年份）为转化事件量原料，但与本件周期口径不同语义。

## 二、计算过程

从缺。本指标需项目级双时点原料（立项日+落地日），三源探针（附录 B）证明零承载：唯一转化域表 `dwd_patent_transfer`（dev 22,809 行/gkx 同构）18 列列级断言无 cycle/duration/period 列——仅 `transfer_effective_date`（varchar，权属变更生效日）单时点 + `transfer_before`/`transfer_after`（JSON 权利人），权属变更≠成果立项→落地转化；jiuxin `ads_technology_transfer_stage` 为技术阶段占比快照。无双时点即无周期，禁伪公式。mock 8.8→7.4 为演示量级参照（ui_demo_fallback 披露）。复现代码与证据对照见产物 `derived[0]`（负结论 null 登记）。

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 项目立项时点 | dev/gkx/jiuxin | **无表**（无科技计划项目库） |
| 项目落地时点 | dev/gkx/jiuxin | **无表**（无成果落地登记） |
| 转化事件（权属变更） | dev `ods.dwd_patent_transfer` | **有但语义不符**（22,809 行，仅单时点） |
| 阶段分布快照 | jiuxin `ads_technology_transfer_stage` | **语义不符**（阶段占比非周期） |

### 3.2 现场复核清单

UI 链实读：`SoftScienceWorkbench.jsx:941` `<SoftScienceTrendAnalysis series={resolvedTrendSeries}/>`；mock 源 `softScienceHomepageMock.js:352-359` conversion-cycle 定义 + `:356-359` 12 点（8.8/8.6/8.5/8.3/8.1/8.0/7.9/7.8/7.7/7.6/7.5/7.4）；摘要句模板 `SoftScienceTrendAnalysis.jsx:97-104`。dev 实连复核（本件脚本断言）：`gkxlumenx_ods.dwd_patent_transfer` 18 列 cycle/duration/period 零命中；年分布 2021:326/2022:1670/2023:3770/2024:7711/2025:5799/2026:3246/无年份:287（共享快照键 `dev_patent_transfer_year_counts`）。

## 四、数据缺失情况

### 4.1 缺口清单

①项目立项时点无表；②项目落地时点无表；③软科学成果与项目的关联键缺失（成果表无 project_id 回链）；④周期均值口径未定（算术平均 vs 中位数，业界无强制标准）。

### 4.2 修复建议与影响面

短期：对接科技计划项目库（立项日+验收/落地日）落 `gkxlumenx_dwd` → 本件完全转换支持。中期：软科学成果管理平台增加里程碑登记（立项/中试/示范落地三时点）→ 周期可分段。远期：成果转化全链路事件流 → 完全直接支持。同面板三趋势系列中「成果数量趋势」可由 dwd_patent_transfer 年分布近似（另件处理），本件与「重点区域贡献趋势」均待项目库。

### 4.3 影响面

软科学成果页时间趋势分析面板第二张图为 mock 演示态；整页趋势面板无任何后端接口调用。

## 参考文献

1. 财政部、科技部. 中国科技成果转化年度报告（2025）——转化合同/收入口径（无周期指标）. https://www.most.gov.cn/kjbgz/202502/t20250228_194265.html
2. 科技部. 科技成果转化方式（转让/许可/作价投资）相关规定. https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/fgzc/gfxwj/gfxwj2023/202311/t20231123_188692.html
3. 全国人大. 中华人民共和国促进科技成果转化法（2015 修订）. https://www.gov.cn/zhengce/2021-10/29/content_5647701.htm

# 附件

## 附录 A 原始需求原文摘录

- 检索记录：`rg 转化效率|转化周期|转化效率趋势` 三份说明书 + 主需求 → 指标名 0 命中。
- 派单书挂载点：清单空（登记：清单未给 + 实查定位）。
- 实查定位链：`rg 转化效率` achievement-preview 页族 → `softScienceHomepageMock.js:352`（series 定义）→ `SoftScienceWorkbench.jsx:941`（面板渲染挂载）。
- mock 参照（`softScienceHomepageMock.js:356-359`）：12 点月序列 8.8→7.4。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_SOFTSCI_009_out.json`）

facts（ui_mount/ui_series/ui_points/ui_mock_note/dev_patent_transfer_cols 18 列/dev_patent_transfer_cycle_like_columns=[]/dev_patent_transfer_year_counts/dev_patent_transfer_total=22809/gkx_table_count=280/jiuxin_table_count_live=218/named_in_srs=false/named_note）；derived[0]（avg_conversion_cycle_monthly 负结论 null 登记）；absence_probe（三件，列级 cycle_hits=0）；support_judgment=完全不支持；base_years 三键（used=[] / missing=2021-2026 / note）；ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：成果转化年度报告（合同数/收入口径，无周期）→ 转化三分法（转让/许可/作价投资事件计数）→ 项目管理双时点法（落地−立项，PMS 通用）。数据矩阵：项目双时点三源 0 命中；唯一转化域表为专利权属变更单时点（语义不符）；久新阶段快照为占比语义。分期方案：一期科技计划项目库入湖（完全转换支持）、二期成果-项目关联键+落地登记、三期全链路事件流（完全直接支持）。风险登记：周期均值口径无国标（算术平均/中位数需裁定）、权属变更冒充转化落地的语义污染。总判：完全不支持（升档路径明确——项目双时点表入湖即活）。
