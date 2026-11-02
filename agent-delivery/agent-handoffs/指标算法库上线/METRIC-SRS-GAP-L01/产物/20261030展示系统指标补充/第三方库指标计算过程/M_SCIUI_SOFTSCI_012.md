# M_SCIUI_SOFTSCI_012 满意度分布 —— 指标信息 MD

> **类型**：简单统计类｜ **域**：软科学成果展示·孵化载体页·运行绩效监控看板·满意度分布（IncubationCarrierPage.jsx:1033）
> **数据支持度**：**完全不支持**｜ **UI 挂载**：科技信息展示系统 → 孵化载体 → 运行绩效监控看板「满意度分布」（`IncubationCarrierPage.jsx:1033`）｜ **公式定义人**：无（指标名三源 0 命中；满意度量表口径无定义）
> **复现脚本**：`code/M_SCIUI_SOFTSCI_012.py`｜ **产物**：`code/M_SCIUI_SOFTSCI_012_out.json`
> **口径归属**：UI 挂载件，SRS 无同名指标｜ **数据源口径**：本件支持度按「开发库 live（10.50.11.76:3306，gkxlumenx_*，禁 demo_*/_devdb）+ 三方库（gkx，183.240.141.251:3318 只读）+ 久新库（jiuxin，Doris 47.93.119.170:29030）」三源评估
> **铁律：本指标所有信息，均以第二章的“最新指标调研报告”为准。第一章指标信息为历史版本，不用作参考。**
> **四判定摘要**：直接结构=无；直接数据=无；依赖结构=无（satisfaction 词族命中全为营业额/债券评级语义污染）；依赖数据=无（评价流零承载）

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源中存在数据量充分的相关表/字段，仅需口径转换/间接计算（无额外数据采集）即可产出本指标 |
| **部分支持** | 三源中存在部分可复用表/字段，**只可计算本指标的部分子项**（或关键维度缺失） |
| **完全不支持** | 三源均无承载，需新建数据链路/外部接入 |

**本件判定：完全不支持。**（评价数据面三源零承载，词族命中全为语义污染）。

### 批次通用纪律摘要（S3-07 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B5 | 列表 sorted() | 污染清单/基期年份 sorted |
| B7 | 数字-出处核对 | mock 分布 3/8/18/42/29 N=100 已对 mock 源行号 |
| B10 | ui_demo_fallback 披露 | mock 分布披露 |
| 基期三键 | base_years_used/missing/note | 产物全键 |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有评价/评分结果面吗？ | 无 | semantic_hits=0（三源） |
| 词族命中有语义一致的吗？ | 无 | 命中全为营业额/债券评级/经营状态（污染清单） |
| 有代理路径吗？ | 无 | 火炬统计年报满意度为问卷采集字段非库内计算 |

## 摘要

「满意度分布」是孵化载体页运行绩效监控看板的第四张图：1-5 星评分柱状图（y=企业数量，tooltip 显示占比），mock 分布 1星:3/2星:8/3星:18/4星:42/5星:29（N=100，4 星为众数 42%）。数据侧判定：**完全不支持**——满意度评分需评价数据面（问卷/评分记录：评价主体+载体客体+星级+时间），三源 satisfaction 词族命中全为语义污染：dev `operating_revenue`（营业额）、`issue_issuer_rating`/`latest_bond_rating`/`latest_issuer_rating`（债券评级）、`code_operating_status`（经营状态码表）；gkx 同族污染；久新 rating 类同族污染。权威侧火炬 2019 指标体系无满意度指标（服务能力为人员/导师/机构配置），在孵企业满意度调查属火炬统计调查制度年报问卷字段——需采集非库内计算。

- 需求判定：指标名三份说明书未出现；语义锚为看板覆盖句「满意度等核心绩效指标」（附录 A）。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技成果展示 → 孵化载体（运行绩效监控）→ 图表卡「满意度分布」（`IncubationCarrierPage.jsx:1033` SoftChartFrame，badge「1-5 星评分」）；图表构建 `:833 buildSatisfactionOption`：x=1星..5星（`d.rating`星）、y=企业数量、tooltip 占比=round(count/total×100)。mock 源 `incubationCarrierMock.js:298-304`。

### 1.2 为什么需要本指标

在孵企业满意度是载体服务质量的直接反馈：分布左偏（低星占比高）提示服务短板，管理者按星级分布定位服务改进优先级（主需求「为孵化载体服务优化提供数据支撑」语义族）。

### 1.3 需求文档是否给出定义方法

三份说明书未出现该指标名（检索记录见附录 A）。**固定句式：三份说明书未给出该指标的计算方法。**（看板描述「覆盖孵化毕业、专利产出、服务利用与满意度等核心绩效指标」为语义锚。）

### 1.4 类似指标权威方法可行性分析概要

权威口径方法族（完整版指向附录 C）：①火炬统计调查制度年报：在孵企业满意度调查为**问卷采集字段**（非库内计算）；②火炬 2019 指标体系：服务能力为人员/导师/中介机构配置——**无满意度指标**；③NPS（净推荐值，贝恩咨询）：推荐者%−贬损者%（0-10 分制），1-5 星映射非标准需转换（星×2≈分制近似）。满意度属问卷统计口径，无库内直算路径。

### 1.5 引用来源

1. 科技部火炬中心. 科技企业孵化器评价指标体系（国科火字〔2019〕239 号）. http://www.chinatorch.gov.cn/fhq/zcfg/202602/bf58a7e77266425e94fa7cc512518095.shtml
2. 国家统计局. 创新创业类服务机构统计调查制度（孵化器年报制度）. https://www.stats.gov.cn/xxgk/tjbz/gmjjhyfl/202311/t20231101_1945621.html
3. Reichheld, F. The One Number You Need to Grow（NPS 原始文献, Harvard Business Review）. https://hbr.org/2003/12/the-one-number-you-need-to-grow

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意**：全市在孵企业对所在载体综合服务满意度的评分分布（1-5 星，企业数为频数）。
- **操作化定义（权威重建式，本件未实现）**：分布 = COUNT(企业) GROUP BY 星级（问卷题「您对载体服务总体满意度」）；可选衍生均值=Σ(星级×频数)/N。
- **降档触发器**：已处最低档。
- **升档触发器**：满意度问卷系统落库（评价表：enterprise_id+carrier_id+rating+survey_date）→ 完全转换支持（直查分布）。

### 1.7 需求叶定位与相近叶关系

- 本叶：孵化载体·运行绩效监控·满意度分布（评分分布图）。
- 相近叶：SOFTSCI_007（孵化毕业统计）同看板第一张图（部分支持件，独立留证）；INCUB_011（成长分）同看板相邻；服务利用雷达图（Top3 载体对比，mock 6 维 72/68/85/91/63/78）为同看板第三张图（无独立指标件）。

## 二、计算过程

从缺。本指标需评价数据面（问卷/评分记录），三源探针（附录 B）证明零承载：satisfaction 词族三源命中全为语义污染——dev 5 命中（`operating_revenue`×2、`issue_issuer_rating`/`latest_bond_rating`/`latest_issuer_rating` 债券评级 3、`code_operating_status` 经营状态码表）、gkx 同族（operating_revenue/rating）、久新 rating 类同族；NPS/评价/问卷（survey/questionnaire/review）子族 0 命中。无评价记录即无分布，禁伪公式。mock (3,8,18,42,29) N=100 为演示量级参照（ui_demo_fallback 披露）。复现代码与证据对照见产物 `derived[0]`（负结论 null 登记）。

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 评价主体（在孵企业名单） | dev `dim.carrier_org_rel` | **近似有**（tenant=39 在驻，SOFTSCI_007 已证） |
| 评价记录（星级+时间） | dev/gkx/jiuxin | **无表**（survey/questionnaire/review 0 命中） |
| 满意度结果面 | dev/gkx/jiuxin | **无表**（semantic_hits=0） |

### 3.2 现场复核清单

UI 链实读（`IncubationCarrierPage.jsx`）：`:1033` SoftChartFrame 挂载 → `:833` 构建函数解构 `{satisfactionData}` → `:836` total=Σcount → `:846` 占比公式 → `:850` x 轴 `${d.rating}星`。mock 源 `incubationCarrierMock.js:299-303` 五档 (3,8,18,42,29)。共享快照复核：dev 542 表/gkx 280 表/久新 218 表（SHOW TABLES 实数）satisfaction 词族扫描命中清单（污染判定）。

## 四、数据缺失情况

### 4.1 缺口清单

①评价记录无表（问卷/评分零承载）；②评价主体-载体关联仅近似（tenant 39 在驻企业可作问卷投放名单，但无答卷）；③调查周期/抽样框未定（全量 vs 抽样、年度 vs 半年）；④1-5 星与 NPS 0-10 分制的口径映射未定。

### 4.2 修复建议与影响面

短期：建满意度问卷（在驻企业 39 家为初始投放框）落 `gkxlumenx_dwd.carrier_satisfaction_survey` → 本件完全转换支持（直查分布）。中期：问卷系统与载体工作台集成（实时评价流）→ 月度分布可滚动。远期：对接火炬统计年报满意度字段 → 完全直接支持。同看板服务利用雷达图（第三张）联动受益。

### 4.3 影响面

孵化载体页运行绩效监控看板第四张图为 mock 演示态；整页无任何后端接口调用。

## 参考文献

1. 科技部火炬中心. 科技企业孵化器评价指标体系（国科火字〔2019〕239 号）——服务能力指标构成（无满意度项）. http://www.chinatorch.gov.cn/fhq/zcfg/202602/bf58a7e77266425e94fa7cc512518095.shtml
2. 国家统计局. 创新创新创业类服务机构统计调查制度（满意度为年报问卷字段）. https://www.stats.gov.cn/xxgk/tjbz/gmjjhyfl/202311/t20231101_1945621.html
3. Reichheld, F. The One Number You Need to Grow（NPS 口径）. https://hbr.org/2003/12/the-one-number-you-need-to-grow

# 附件

## 附录 A 原始需求原文摘录

- 检索记录：`rg 满意度` 三份说明书 + 主需求 → 指标名 0 命中。
- 语义锚原文（`IncubationCarrierPage.jsx:1004-1006`）：「运行绩效监控看板——覆盖孵化毕业、专利产出、服务利用与满意度等核心绩效指标。」
- mock 参照（`incubationCarrierMock.js:299-303`）：五档 3/8/18/42/29。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_SOFTSCI_012_out.json`）

facts（ui_mount/ui_build_fn/ui_mock_data/ui_mock_note/dev_table_total=542/dev_satisfaction_word_hits_note/dev_satisfaction_semantic_tables=[]/gkx_table_count=280/gkx_satisfaction_word_hits_note/jiuxin_table_count_live=218/jiuxin_satisfaction_word_hits_note/named_in_srs=false/named_note）；derived[0]（satisfaction_rating_distribution 负结论 null 登记）；absence_probe（三件 semantic_hits=0 + 污染清单 sorted）；support_judgment=完全不支持；base_years 三键（used=[] / missing=2021-2026 / note）；ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：火炬年报问卷字段（满意度为采集项非计算项）→ 火炬 2019 指标体系（无满意度，服务能力=配置类）→ NPS（推荐者−贬损者，0-10 制）。数据矩阵：评价记录三源 0 命中，词族命中全为营业额/债券评级/经营状态污染；评价主体可近似（tenant 39 在驻企业）但无答卷。分期方案：一期问卷落库（完全转换支持）、二期实时评价流（月度滚动）、三期火炬年报对接（完全直接支持）。风险登记：抽样框窄（39 家）、星制-分制映射、问卷回收率。总判：完全不支持（升档路径明确——问卷落库即活）。
