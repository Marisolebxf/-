# 成果热度值（heat，成果被关注程度排序键）（M_SCIUI_INCUB_028）

> **类型**：无业务逻辑数值类（成果互动行为流三源零承载）｜ **域**：①科技信息展示系统·科技成果展示·软科学成果展示·热门成果栏排序键「热度」（1-10 量表字符串）；②科技政策跟踪·分析评价·热点问题分析看板·议题热度条（0-100 分）｜ **UI 挂载**：`SoftScienceResultsRail.jsx:72`（heat 排序 Tab）+ `__tests__/SoftScienceResultsRail.test.jsx:141`（排序测试）+ `policy-tracking/analysis/interpret/HotIssueDiagnosisBoard.jsx:39`（热度条形图）
> **数据支持度**：**完全不支持**｜ **公式定义人**：无（「热度值」指标名三份说明书未出现；主需求「热度」14 处均为图表伴随词；口径按 Altmetric Attention Score 加权聚合法重建）｜ **口径归属**：UI 派生读数（成果侧 mock「热度 9.4」字符串手写；政策侧 mock heat 95/88，组件注释自认 Mock 打标）
> **复现脚本**：`code/M_SCIUI_INCUB_028.py`｜ **产物**：`code/M_SCIUI_INCUB_028_out.json`
> **四判定摘要**：直接结构 = 无（dev heat 词族 2 命中均 0 行产业链预留面；政策热度预留面 policy_intensity/policy_focus/public_opinion 三表全 0 行）；直接数据 = 无（同左）；依赖结构 = **缺**（成果互动行为流无表+课题成果主档无表——上游双缺）；依赖数据 = 无（gkx 0 命中；久新热度族 12 表全为难题/技术/主题维度语义排除，但加权结构范式可引）
> **数据源口径**：三源（dev live `10.50.11.76` `gkxlumenx_*` 非 demo + 三方库 gkx + 久新 `gkx_technology_analysis_dev` live 218 表复核）逐一探针留证；`demo_*` 禁引；UI mock 值仅作需求语义证据。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库与久新库**均无法构建 |

**四判定**：表结构直接支持 / 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全不支持**（两挂载侧同判）。热度=被关注程度加权分，计算需互动/舆情行为流：①成果侧——dev 互动面 `app_article_collect` 0 行（且为小程序文章收藏语义）、课题成果主档本身无表（INCUB_022 已证）；②政策侧——dev `policy_intensity`/`policy_focus`/`policy_public_opinion` 三预留表全 0 行，`HotIssueDiagnosisBoard` 数据来自 `policyData.js` 手写数组（组件注释自认「Bid §4.2.2.2.1 / E4 规则 Mock 打标」）。gkx 0 命中；久新热度族 12 表全为难题（`heat_component` 2,842 行）/技术/主题维度——语义排除但其「component_score×weight→weighted_contribution」加权结构是本件模型的形态范式。

### 批次通用纪律摘要（S3-07 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 无除式（加权聚合语义） |
| B4 | 负结论带探针 | absence_probe 五件（成果互动/政策热度/gkx/久新/需求原文） |
| B5 | 确定性 | mock 值按文件序；词族 sorted() |
| B7 | 产物只由脚本产出 | 本件 py 实探产出 _out.json |
| B9 | 单位/日期陷阱 | 双量表披露（成果侧 1-10 字符串/政策侧 0-100 整数） |
| B10 | 口径裁定保守交付 | 两 UI 形态两挂载侧并列判档；范式可引与语义排除分开写 |
| B11 | 多本账互推 | dev/久新行数与共享快照零漂移 |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有现成热度结果面吗？ | 无 | dev 预留面全 0 行；gkx 0；久新语义排除 |
| 互动/舆情行为流齐吗？ | **缺** | 互动面 0 行；成果主档无表 |
| 现在就能算吗？ | 不能 | 输入无源 |

## 摘要

「成果热度值」是软科学页热门成果栏的默认排序键（「热度 9.4」字符串经 `parseHeatValue` 提数值降序，1-10 量表），同字段范式复用于政策跟踪热点问题看板的热度条（heat 95/88，0-100 分，xAxis max=100）。数据侧判定：**完全不支持**——热度的计算输入（成果互动行为流/政策舆情流）三源零承载：dev 互动面 0 行+课题成果主档无表、政策热度三预留表全 0 行；gkx 0 命中；久新热度族全为难题/技术维度（最近邻 `ads_research_problem_heat_component` 2,842 行为科研难题热度分量，语义排除但加权三层结构范式可引）。权威参照 Altmetric Attention Score：来源类型加权聚合（博客 8/政策文件 3/维基 3/X 0.25），每人每源一次，是关注度近似非质量度量。

- 需求判定：指标名三份说明书未出现；主需求「热度」14 处均为图表伴随词（技术热度分布图/热度指数等）。
- 复现状态：三源探针+双 mock 层实读已跑通；五件 absence_probe 留证。
- 档位结论：**完全不支持**（两挂载侧输入维双缺）。
- 关键事实：mock 成果侧 readCount 118/favoriteCount 13 与「热度 9.4」并列展示但无计算关系（parseHeatValue 只读 value 字段）——演示层自身即无算法源。
- 升档路径：成果互动事件表落库 → Altmetric 式加权 run → 完全转换支持（课题成果主档为上游前提）。

## 一、需求定义概述

### 1.1 所属功能模块

**挂载侧①（成果热度）**：科技成果展示 → 软科学成果展示 → 热门成果栏（`SoftScienceResultsRail.jsx:71-72` `RESULT_SORT_OPTIONS=[{heat,热度},{impact,影响力}]`，`:188` `useState("heat")` 默认热度排序；`:79-83` `parseHeatValue` 从 value 字符串提取数值；`:100-110` `sortHotResultsByMode` 降序稳定排序）。测试件 `__tests__:141` 验证热度→影响力 Tab 切换。数据链 `softScienceHomepageMock.js:600-710` `hotResults[].value="热度 9.4"`。

**挂载侧②（政策议题热度）**：科技政策跟踪 → 分析评价 → 热点问题分析看板（`HotIssueDiagnosisBoard.jsx:39` `issues.map(i=>({value:i.heat,…}))` 条形图，xAxis max=100 name=热度；`:14` 组件默认 `issues=hotIssuesData`）。数据链 `policyData.js:484` 手写数组（heat 95/88…，detectTags 规则打标）。

### 1.2 为什么需要本指标

热度解决「先看哪个」的问题：成果栏需要被关注度排序（序号 462 语境：根据贡献度等多维排序优选；互动统计与传播分析语境：互动行为与影响评价结合）；政策看板需要议题温度（热点识别→异常抬升预警，trendNote「近 4 周热度 +18%，异常抬升」）。

### 1.3 需求文档是否给出定义方法

三份说明书未出现该指标名（检索记录见附录 A）。**固定句式：三份说明书未给出该指标的计算方法。**（主需求「热度」14 处均为图表伴随词。）

### 1.4 类似指标权威方法可行性分析概要

热度/注意力方法族（完整版指向附录 C）：①Altmetric Attention Score——来源类型加权聚合（博客 8/播客 5/政策文件 3/专利 3/维基 3/X 0.25/Facebook 0.25），每人每源只计一次，取整呈现，明确「非质量度量」；②政策文档提及——每政策源 3 分（同源多篇只加一次）；③久新难题热度分量范式——component_score×component_weight→weighted_contribution 三层加权（语义为难题维度，结构可引）。

### 1.5 引用来源

1. Altmetric. How is the Altmetric Attention Score calculated? https://help.altmetric.com/en/articles/9800513
2. Altmetric. Policy Documents（政策文档计分规则）. https://help.altmetric.com/en/articles/9801601
3. Altmetric. The donut and Altmetric Attention Score. https://www.altmetric.com/about-us/our-data/donut-and-altmetric-attention-score/

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意**：成果被关注程度的加权分（阅读/收藏/点赞/传播按来源加权），作排序键；政策侧为议题舆情温度。
- **操作化定义（Altmetric 式重建，本件未实现）**：热度 = Σ(互动事件ᵢ×来源权重ᵢ)，阅读 w₁/收藏 w₂/点赞 w₃/外部分享 w₄（权重平台自定并披露）。
- **降档触发器**：已处最低档。
- **升档触发器**：互动事件表落库+加权 run → 完全转换支持。

### 1.7 需求叶定位与相近叶关系

- 本叶：软科学·成果互动与传播中心·互动统计与传播分析（成果侧）；政策跟踪·热点问题分析看板（政策侧）。
- 相近叶：INCUB_022（成果总览报表）共享「课题成果主档无表」上游结论；KGANALY_017 类热度件（他批）为技术热点语义；本件政策侧与 POLICY 族件（他批）共享 policy_intensity 空壳结论（独立留证）。

## 二、计算过程

从缺。本指标需互动/舆情行为流作加权输入（§1.4 Altmetric 式），三源探针（附录 B 五件）证明：成果侧互动面 0 行+主档无表、政策侧三预留表全 0 行、gkx 0 命中、久新语义排除——无行为流即无热度分，禁伪公式。复现代码与证据对照见产物 `derived[0]/[1]`（两挂载侧负结论留空登记）。

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 课题成果主档（热度的对象） | dev/gkx/久新 | **无表**（INCUB_022 结论） |
| 成果互动行为流（阅读/收藏/点赞） | dev `app_article_collect` | 0 行（且语义为小程序文章收藏） |
| 政策舆情/检索行为流 | dev `policy_intensity`/`policy_focus`/`policy_public_opinion` | 三表全 0 行 |
| 热度加权范式参照 | 久新 `ads_research_problem_heat_component` | 2,842 行（难题维度，结构可引语义排除） |

### 3.2 现场复核清单

成果侧数据链实读：`hotResults` 9 项 value「热度 9.4→7.5」与 readCount 118→68/favoriteCount 13→7 并列递减——视觉上像联动但 `parseHeatValue` 只读 value 字段（`:79-83`），计算关系不存在（产物键 `ui_mock_semantics_note`）。政策侧 `hotIssuesData` 首条：topic 人工智能伦理治理/heat 95/detectTags[高频,异常,重点]（E4 规则打标自认）。久新 `heat_component` 列实读（problem_id/model_version/component_code/component_score/component_weight/weighted_contribution/source_table/coverage_status）——完整三层加权范式。

## 四、数据缺失情况

### 4.1 缺口清单

①课题成果主档无表（对象缺）；②互动事件表无承载（输入缺）；③政策舆情流三表空壳；④权重口径未定（Altmetric 式来源权重需平台裁定）。

### 4.2 修复建议与影响面

短期：课题成果主档立项（上游）+互动事件表（阅读/收藏/点赞，`cms_op_audit` 442 行审计流可作技术底座扩容）。中期：Altmetric 式加权 run（仿久新 heat_component 三层结构）落 `gkxlumenx_ads` → 本件与 INCUB_022/SOFTSCI 族联动升档。政策侧：舆情采集（政策解读阅读/检索行为）落 `policy_intensity` → 议题热度可算。

### 4.3 影响面

热门成果栏热度/影响力双 Tab 排序、政策热点看板热度条+异常打标全为 mock；影响力分（impactIndex 96/94/91…）同为 mock 常数。

## 参考文献

1. Altmetric. How is the Altmetric Attention Score calculated? https://help.altmetric.com/en/articles/9800513
2. Altmetric. Policy Documents. https://help.altmetric.com/en/articles/9801601
3. Altmetric. The donut and Altmetric Attention Score. https://www.altmetric.com/about-us/our-data/donut-and-altmetric-attention-score/

# 附件

## 附录 A 原始需求原文摘录

- 检索记录：`rg 热度值|成果热度` 三份说明书 + 主需求 → 指标名 0 命中；`rg 热度` 主需求 14 处全为图表伴随词（:399 技术热度分布图/:1103 热度指数/:1565 人才分布热度/:2571 应用热度/:2751 使用热度等）。
- 语义锚原文（主需求 :3337 成果互动与传播中心）：「互动行为、传播数据与影响评价相结合，有效提升成果社会参与度和品牌认知度。」
- 政策侧组件注释（`HotIssueDiagnosisBoard.jsx:13`）：「热点问题分析看板 · Bid §4.2.2.2.1 / E4 规则 Mock 打标」——自认演示态。
- UI：`softScienceHomepageMock.js:602` `value: "热度 9.4"`；`policyData.js:486` `heat: 95`（mock 演示值）。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_INCUB_028_out.json`）

facts（ui_mounts/ui_mock_result_heat_values/ui_mock_result_readcounts/ui_mock_result_favoritecounts/ui_mock_policy_heat_values_head/ui_mock_semantics_note/dev_table_total=542/dev_heat_word_tables/dev_heat_hits_note/dev_policy_heat_candidate_rows/dev_interaction_note/gkx_table_count=280/gkx_heat_word_tables/jiuxin_table_count_live=218/jiuxin_heat_word_tables_head/jiuxin_heat_component_cols/jiuxin_heat_component_rows_snapshot=2842/jiuxin_hotspot_yearly_cols_head/jiuxin_semantics_note/srs_anchor/named_in_srs/named_note/authoritative_reference）；derived[0]（成果热度负结论）/derived[1]（政策议题热度负结论）；absence_probe（五件）；support_judgment=完全不支持；base_years 三键；ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：Altmetric 加权聚合（来源权重 8/5/3/0.25，每人每源一次）→ 政策文档计分（每源 3 分）→ 久新 heat_component 三层加权范式（component×weight→contribution）。数据矩阵：成果主档无表+互动流 0 行+政策舆情三表空壳；久新范式在库可仿。分期方案：一期主档+互动事件表、二期加权 run（完全转换支持）。风险登记：互动数据冷启动、权重口径需产品裁定并披露（Altmetric 透明度惯例）。总判：完全不支持（两挂载侧输入维双缺，范式参照在库）。
