# 多维综合评价与评分（M_SCIUI_TALENTIR_002）

> **类型**：需业务建模类（尽调评分口径未闭合）｜ **域**：科技信息展示系统·人才引进推荐评估·人才尽调报告与推荐｜ **UI 挂载**：科技信息展示系统 → 人才引进推荐评估 → 尽调报告 Tab（定制化尽调报告生成维度复选项）→ `ReportTab.jsx:119`
> **数据支持度**：**部分支持**｜ **公式定义人**：仿王惠（推测定义，需求原文只给功能行为不给评分算法）｜ **口径归属**：需求明列叶（主需求 1.1.1.1.4.3.4.4.2），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_TALENTIR_002.py`｜ **产物**：`code/M_SCIUI_TALENTIR_002_out.json`
> **四判定摘要**：直接结构 = 部分（久新 `ads_talent_profile` 评分组为现成多维综合评分结果面）；直接数据 = 部分（同表覆盖率 100.0%，但维度集与需求五维不同物）；依赖结构 = 部分（UI 需求五维中权威度/社会影响两维三源无承载）；依赖数据 = 部分（同左）
> **数据源口径**：三源（开发库 live `gkxlumenx_*` 非 demo + 三方库 gkx + 久新 `gkx_technology_analysis_dev`）逐一探针留证；`demo_*` 禁引。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：部分支持。** 这是学者画像族里数据面最好的一件：久新 `ads_talent_profile` 评分组是**结构+数据双在**的现成多维综合评分结果面——`academic_capability` 五分项加权分（paper/citation/h_index/collaboration/core_source 各自 0-100 标准化后按 0.20/0.30/0.30/0.15/0.05 加权）+ `academic_metric_weight_coverage` 覆盖位 + `academic_capability_rank` 唯一稳定排名 + `score_version='talent_academic_mvp_v1'`，100,000 人全覆盖（§2.2/§2.3）；且库内第二套能力评估面 `ads_talent_capability_assessment`（99,996 行，`overall_score`/`overall_rank`）与 `ads_talent_capability_model`（1 行模型定义：0.25×科研毅力+0.25×创新+0.40×学科匹配+0.10×政治倾向）在案。降档根因在**口径不同物**：需求明列五维是「权威度、创新性、项目经验、社会影响」（主需求 :2447），其中权威度与社会影响两维在三源无承载（无荣誉奖项强度数据、无社媒传播数据），UI mock 权重（0.28/0.24/0.22/0.16/0.10）是演示值——评分口径未闭合，不得以库内任一现成维度集冒充需求口径（B10）。

### 批次通用纪律摘要（S3-03 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 覆盖率分子分母同表同 WHERE（100,000/100,000） |
| B4 | 负结论带探针 | UI 五维中两维无承载的排除探针（§3.3） |
| B5 | 确定性 | 分桶按键排序、Top5 按分数+rank 双键排序 |
| B6 | 闸门自身被闸 | 不自跑闸门，派单方统一 |
| B7 | 产物只由脚本产出 | 改脚本→重跑；产物零手改 |
| B8 | 回执不复收 | 探针 SQL 幂等可复验 |
| B9 | 单位/日期陷阱 | 评分为无量纲 0-100；无日期运算 |
| B10 | 口径裁定保守交付 | 不写伪分；mock 结构披露键标注不参与结论；升档触发器写死 |
| B11 | 多本账互推 | gkx 21,316/久新 100,000 与共享快照及族内件零漂移 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 库内有多维综合评分现成结果面吗？ | 有（久新双面） | `academic_capability` 组 + capability 三表族（§2.2/§2.3） |
| 维度集与需求五维一致吗？ | 不一致（核心降档因） | 需求五维 vs 库内两套维度集三套口径互不同物（§2.4） |
| 缺的两维（权威度/社会影响）有承载吗？ | 无 | 三源词族探针 0 命中（§3.3） |

## 摘要

「多维综合评价与评分」是人才尽调报告与推荐的第二功能叶（主需求 1.1.1.1.4.3.4.4.2）：基于权威度、创新性、项目经验、社会影响等多维量化指标，通过人工智能算法对专家综合评分。UI 侧它是尽调报告定制维度的复选项（`ReportTab.jsx:119`，默认勾选），评分语义源是 `data.js:1486-1502` mock 生成器——五维 `random` 常量按固定权重 0.28/0.24/0.22/0.16/0.10 加权出 `aiScore`。数据侧久新给了两套现成评分面：学术力面（`ads_talent_profile` 评分组，100,000 人 100.0% 覆盖，权重公式抽样复算逐位一致）与能力评估面（`ads_talent_capability_assessment` 99,996 行含 overall_score/overall_rank，模型公式在 `ads_talent_capability_model` 1 行在册）。判**部分支持**：库内维度集（论文/被引/H指数/合作广度/Core 或 毅力/创新/学科匹配/政治倾向）与需求五维（权威度/创新性/项目经验/社会影响）不同物，权威度与社会影响两维三源无承载，评分口径未闭合。脚本已跑通，产物与正文数字逐一对应。

- 需求判定：**需求明列叶**（主需求 :2441/:2447-2449），功能行为在、评分算式无。
- 复现状态：脚本已跑通；覆盖率/分布/Top5/权重复算/capability 三表族读数全落产物。
- 档位结论：**部分支持**（现成评分面双在 + 需求维度集两维无承载，口径未闭合）。
- 关键事实：久新权重公式抽样行复算 `abs_diff=2.1e-05` 与存储值逐位一致——库内评分口径自洽可审计。
- 升档路径：甲方出官方映射表（UI 五维 ↔ 库五分项）或裁定采库内维度集 → 直查可算升完全直接支持。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技人才态势/**人才引进推荐评估·人才尽调报告与推荐/多维综合评价与评分**（主需求 1.1.1.1.4.3.4.4.2）。UI 实际容器是人才引进推荐评估页尽调报告 Tab（`ReportTab.jsx`）顶部的「定制化尽调报告生成」复选组：`Checkbox.Group` 在默认维度（学术成果/科研经历/合作网络/风险点等 `DEFAULT_DIMS`）之外追加 `{ value: 'score', label: '多维综合评价与评分' }`（`ReportTab.jsx:119`），且默认勾选（`useState([...DEFAULT_DIMS, 'score'])`）。勾选后 `startBatchReports` 排队并行生成尽调报告，评分维度进入 `DueDiligenceReport` 的组装逻辑。该复选项在能力映射清单 `talentRecommendSpec.js:52` 同名登记（`report.l6` 第二项），与 SRS 叶一一对应——前端作者把「多维综合评价与评分」当作尽调报告的标准组件而非独立图表，这与需求「通过智能匹配和评分机制，生成详尽、客观的人才尽调报告」的定位一致。

### 1.2 为什么需要本指标

尽调报告的业务问题是「多个维度的证据如何收敛成一个可排序的结论」：学术成果、合作网络、风险点各自给出面证据，但用人单位最终要回答「A 与 B 谁更值得引进」——综合评分就是收敛器。需求把它列为尽调报告四核心能力（画像/评分/推荐/跟踪）的第二环：画像给材料、**评分给结论**、推荐给名单、跟踪给时效。官方对应物是科技人才评价改革试点方案（R1）的「立新标」——按创新价值、能力、贡献导向构建评价体系；GB/T 44143-2024（R2）进一步把它标准化为创新价值/能力/创新贡献三方面指标。本件的调研重心因此不在「有没有分」而在「分与需求口径的对齐度」：库内现成分 plentiful，但维度集是否是需求要的那五维，决定了直查可用还是口径待裁。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**主需求 :2447-2449 给出的是功能行为：「基于权威度、创新性、项目经验、社会影响等多维量化指标，通过人工智能算法进行综合评分，帮助用人单位快速对专家进行定量评价」——四维（加「等」字）点名了，但每维的观测源、标准化方法、权重、合成算式一个字都没有。核增需求与算法库两份真源检索 0 命中（附录 A.2）。UI 侧 mock 权重（0.28/0.24/0.22/0.16/0.10）是前端演示值，不构成口径证据。

### 1.4 类似指标权威方法可行性分析概要

「人才多维综合评分」的权威方法锚有三层。其一，国家标准 GB/T 44143-2024《科技人才评价规范》（R2，科技部提出、2024-06-29 实施）：创新价值/能力/创新贡献三方面指标 + 分类评价 + 流程规范——官方框架的维度结构。其二，科技人才评价改革试点方案（R1，国科发才〔2022〕255 号）：按承担重大攻关/基础研究/应用开发/社会公益四类构建「创新价值、能力、贡献」导向的评价体系，基础研究类明确「不把论文数量、影响因子高低作为量化考核指标」——分类评价思想。其三，文献计量单指标传统：h 指数（R3，Hirsch 2005 PNAS）把产出与影响合成单一数字，但作者自陈「single number 永远只是 multifaceted profile 的粗略近似」。方法族对照：

| 方法族 | 代表 | 维度结构 | 数据要求 | 与三源匹配 |
|---|---|---|---|---|
| 国标三方面框架 | GB/T 44143-2024（R2） | 创新价值/能力/创新贡献 | 指标体系+评价流程 | **部分**（久新学术力面可映射能力与创新贡献） |
| 分类评价试点 | 国科发才〔2022〕255 号（R1） | 四类人才×创新价值/能力/贡献 | 分类画像+代表作 | 部分（分类维久新有 career_stage） |
| 文献计量合成 | h 指数（R3）/学术力五分项 | 论文/被引/H/合作/Core | 文献计量计数 | **有**（久新现成，即 academic_capability） |
| 前端演示模型 | UI aiScore | 权威度/创新/项目/影响/社会 | mock 常量 | 结构披露（不作源） |

结论：库内学术力面是文献计量合成族的落地实现（且比单指标 h 更复合），与国标框架的「能力」面高度可映射；缺口在需求点名的「权威度/社会影响」两维。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/talent-trend/components/ReportTab.jsx:119` — `{ value: 'score', label: '多维综合评价与评分' }`（Checkbox.Group 选项）；mock 语义源 `repos/demo-ui-science/src/pages/talent-trend/data.js:1486-1502`（`aiScore = dims.authority*0.28 + dims.innovation*0.24 + dims.project*0.22 + dims.influence*0.16 + dims.social*0.1`，五维全 random）；能力映射 `talentRecommendSpec.js:52`。
- 主需求：`科技信息展示系统和科技专题服务系统.md` :2447-2449（1.1.1.1.4.3.4.4.2），原文见附录 A。
- 权威方法：R1 国科发才〔2022〕255 号（科技部官网）；R2 GB/T 44143-2024（国标全文系统）；R3 Hirsch 2005 PNAS。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**推测定义（须披露口径不闭合）**：

$$S_{multi} = \sum_{d=1}^{5} w_d \cdot s_d,\quad s_d \in [0,100]$$

五维 = 权威度/创新性/项目经验/社会影响（+「等」字开放维），权重待定版。UI mock 权重结构（0.28/0.24/0.22/0.16/0.10）暗示「权威度主导、社会影响垫底」的排序直觉，按各维 random 区间中位数演示重算加权分 78.7（产物 `ui_mock_ai_score_structure_reference`，mock 结构披露，不参与支持度结论）。库内两个候选真口径：**口径 A（学术力面）** academic_capability = (0.20×paper_score + 0.30×citation_score + 0.30×h_index_score + 0.15×collaboration_score + 0.05×core_source_score) / weight_coverage；**口径 B（能力评估面）** overall_score = 0.25×科研毅力 + 0.25×创新能力 + 0.40×学科匹配度 + 0.10×政治倾向（模型公式原文在案）。三套维度集（需求五维/口径 A 五分项/口径 B 四维）互不同物，以哪套对外须甲方裁定。

**降档/升档触发器**：①甲方裁定尽调评分口径 = 口径 A 或 B（或出官方映射表 UI 五维↔库分项）→ 直查可算，升**完全直接支持**；②若坚持需求五维 → 权威度（荣誉/奖项/学术任职强度）与社会影响（社媒/传播/政策引用）两维在三源无承载，维持部分支持；③两维接外部数据源（人才荣誉库/学术任职库/Altmetric 类）→ 四维以上闭合可升完全转换支持。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在需求文档 | 主需求《科技信息展示系统和科技专题服务系统.md》（SRS 人才引进推荐评估同文转述） |
| 所属四级功能 | 1.1.1.1.4.3.4 人才引进推荐评估（4 个 L5） |
| 所属 L5 | 人才尽调报告与推荐（1.1.1.1.4.3.4.4，7 叶） |
| 本件叶 | **多维综合评价与评分（1.1.1.1.4.3.4.4.2）——需求明列** |
| 同 L5 相邻叶 | 专家画像智能生成（.1）/ 定制化尽调报告生成（.3）/ 专家智能推荐（.4）/ 动态跟踪与更新（.5）/ 风险与合规性评估（.6，TALENTIR_010 承接）/ 团队组合与协同分析（.7） |
| UI 容器 | `ReportTab.jsx:119` 尽调报告定制复选项（默认勾选） |

本件与 TALENTIR_010（风险与合规）共享同一 L5 容器与同一 mock 生成器（`generateEvaluationData` 同时产 `recommendations` 评分与 `riskLevel`），但数据侧分道：本件命中久新现成评分面，010 件是事件面零承载——同族两件判档逻辑相反，正好说明「结构在数据空」与「数据在口径异」是两类不同的缺口。

## 二、计算过程

### 2.1 方法选择（文献依据）

若口径闭合，方法选**多维加权百分制（GB/T 44143-2024 框架的文献计量落地版）**：分项指标在固定基准总体中标准化为 0-100 分（并列值取平均名次），再按公示权重加权、按实际可用权重归一。选择理由：其一，这正是久新 `talent_academic_mvp_v1` 的已实现算法（§2.3 抽样复算一致），「方法选择」在库内已闭合，本件要做的是口径对齐而不是另造公式；其二，国标（R2）的「能力」面与创新贡献面在文献计量口径下可操作化，分类评价思想（R1）可由 `career_stage` 分层实现；其三，h 指数传统（R3）的教训——单数字粗略近似——正是五分项加权要克服的，库内做法（分项分+weight_coverage+解释列）符合国标「评价结果使用」的可解释性要求。UI 五维中缺的两维（权威度/社会影响）按两跳止步规则记缺口（B 类推断依赖维，不代理不推测）。

### 2.2 装载与久新学术力面定档证据

经 `_gkxdb.py` 连 gkx、直连 dev 与久新（三源串行只读）。主画像 `ads_talent_profile` 100,000 行（与 M_TALENT_UI_CHINESE_RATIO 久新回填段零漂移）。评分组字段逐一非空实测：`academic_capability`/`paper_score`/`citation_score`/`h_index_score`/`collaboration_score` 各 100,000（100%），`core_source_score` 99,869（99.87%），`talent_potential` 80,170（潜力模型只覆盖合格评估者）——`score_version` 全表单值 `talent_academic_mvp_v1`，`academic_metric_weight_coverage` 取值 [0.95, 1.00]（Core 缺值行按 0.95 归一，公式语义自洽）。覆盖率派生键 `jiuxin_academic_capability_coverage_pct = 100.0`（100,000/100,000，同表全量非采样）。

### 2.3 分布、Top5 与权重公式复算

学术力分布（10 分桶）：0-9 分 4,346 人 / 10-19 分 11,720 / 20-29 分 10,727 / 30-39 分 10,201 / 40-49 分 10,344 / 50-59 分 11,371 / 60-69 分 11,263 / 70-79 分 11,548 / 80-89 分 11,537 / 90-100 分 6,943——全距 [0.9676, 99.5423]，均值 51.5532，分布平滑无堆积点（百分位标准化的正常形态）。Top5 样例（按分数降序、同分按 rank 升序）：J. R. Pater 99.5423（rank 1）/ H. Zhu 99.5365 / M. Düren 99.5256 / R. W. L. Jones 99.4932 / M. Costa 99.4783——均为 paper_score/citation_score 双 99+ 的高被引学者，样例可人工解释。权重公式复算：抽样行 stored=44.074，按 (0.20×paper+0.30×citation+0.30×h_index+0.15×collab+0.05×core)/coverage 重算 = 44.074，`abs_diff=2.1e-05`（DECIMAL 存储精度内）——**库内权重口径可审计、逐位可复算**，这是「现成结果面」判定的硬证据。

### 2.4 capability 三表族：第二套现成评分面

久新另有通用能力评估模型三表族（本批首探）：`ads_talent_capability_assessment` 99,996 行（含 `research_perseverance_score`/`innovation_capability_score`/`discipline_match_score`/`political_orientation_score` 分项分 + `overall_score`/`overall_rank`，36 列）；`ads_talent_capability_dimension_metric` 599,976 行（dimension/metric 双层明细 + `metric_weight` + `weighted_contribution` + `calculation_method`——**审计级明细面**）；`ads_talent_capability_model` 1 行（模型定义：`talent_problem_match_shenzhen_v1`「人员能力与深圳基础研究问题匹配模型V1」，观察窗 2000-2025，公式 `0.25*科研毅力+0.25*创新能力+0.40*学科匹配度+0.10*政治倾向；政治倾向无数据统一50分`，source_snapshot_ids 记录 Iceberg 快照血缘）。这套面的价值：其一，证明久新侧有「权重公式+分项明细+总分排名」全链路评分工程范式；其二，其「无数据维统一默认分」策略（政治倾向 50 分）是口径不闭合维的保守处理先例——本件缺的权威度/社会影响两维可援引同策略。

### 2.5 三源排除与 UI 五维缺口定性

**gkx**：280 表 talent/scholar×score/eval/assess/rating/capab 词族交叉 0 命中；`dwd_scholar` 27 列逐一核对（dwd_id/id/scholar_id/name_en/name_zh/avatar/scholar_org_name_en/scholar_org_name_zh/scholar_department_name_en/scholar_department_name_zh/scholar_org_id/orc_id/bio/bio_zh/paper_nums/citation_nums/h_index/status/created_time/updated_time/creater/updater/table_data_source/operator_remarks/is_deleted/insert_remark/reference_nums）——只有 paper_nums/citation_nums/h_index/reference_nums 原始计数，无任何合成评分列。**dev**：gkxlumenx_* 全 schema talent/scholar/expert 词族仅 2 张（`gkxlumenx_cms.cms_expert_knowledge`/`gkxlumenx_ods.scholar`），交叉评分词族 0 命中。**UI 需求五维缺口**：权威度（荣誉/奖项/任职强度）——三源无荣誉强度结构化数据（taxonomy 称谓族是分类关系非强度评分）；社会影响（社媒/传播）——三源无任何社媒/传播面。两维按两跳止步规则记缺口，不代理。

### 2.6 稳健性与口径敏感性

三套口径（需求五维/UI mock/库内 A、B）的敏感性定性：口径 A 对论文量纲学者（高产低引）与引用量纲学者（少产高引）的排序差异大——权重 0.30/0.30 双高意味着被引与 H 指数主导；口径 B 的 0.40 学科匹配权重使其本质是「深圳问题适配度」评分，直接用于普适尽调会引入地域偏置（模型名明示 SHENZHEN_RESEARCH_PROBLEM scope）；UI mock 五维的 authority 权重最高但该维无数据——若按 mock 权重硬套库内分项，等于把无数据维换成 proxy 悄悄改口径（B10 禁止）。结论：三口径不得混用，对外口径以甲方裁定为准，本件交付口径 A 的全量读数作为「库内现成」的证据面。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_TALENTIR_002.py`（三源串行只读；gkx 经 `_gkxdb.py`；dev/久新直连；零 `demo_*`）；运行 `python3 code/M_SCIUI_TALENTIR_002.py`。
- 产物：`code/M_SCIUI_TALENTIR_002_out.json`。正文数字与产物键逐一对应：`jiuxin_talent_profile_rows=100000`（§2.2）、`jiuxin_profile_score_nonnull`（各分项非空数）、派生键 `jiuxin_academic_capability_coverage_pct=100.0`（§2.2）、`jiuxin_academic_capability_decile` 十桶分布 + `jiuxin_academic_capability_avg=51.5532` + `jiuxin_top5_by_academic_capability`（§2.3）、`jiuxin_weight_formula_sample_check.abs_diff=2.1e-05`（§2.3）、`jiuxin_capability_family`（三表族行数 99,996/599,976/1）+ `jiuxin_capability_model_rows_detail`（模型公式原文）（§2.4）、`gkx_scholar_rows=21316` + `gkx_scholar_score_like_cols=[]`（§2.5）、`ui_mock_ai_score_structure_reference=78.7`（§1.6 披露）。
- 结果解读：三个可用读数（学术力面全量覆盖+分布+Top5；权重公式可审计；capability 模型范式在案）+ 一个待裁口径（需求五维两缺）。mock 结构披露键 78.7 证明前端口径是五维加权百分制，不参与支持度结论。
- 对照需求功能要求的评审：「基于权威度、创新性、项目经验、社会影响等多维量化指标进行综合评分」——**部分满足**：创新性/项目经验两维可由库内分项映射（citation/h_index→创新性，project_count→项目经验），权威度/社会影响两维无承载；「通过人工智能算法」——库内算法为文献计量合成（非 AI 学习模型），语义可接受但须披露口径差异。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 装载 | 主画像行数 | `jiuxin_talent_profile_rows` | 100,000 |
| 覆盖 | 学术力非空 | `jiuxin_profile_score_nonnull.academic_capability` | 100,000（100.0%） |
| 覆盖 | Core 分非空 | `jiuxin_profile_score_nonnull.core_source_score` | 99,869（99.87%） |
| 覆盖 | 潜力分非空 | `jiuxin_profile_score_nonnull.talent_potential` | 80,170 |
| 分布 | 均值/全距 | `jiuxin_academic_capability_avg` / min/max | 51.5532 / [0.9676, 99.5423] |
| 分布 | 90 分以上 | `jiuxin_academic_capability_decile` 桶 90 | 6,943 人 |
| 样例 | Top1 | `jiuxin_top5_by_academic_capability[0]` | J. R. Pater 99.5423（rank 1） |
| 复算 | 权重公式 | `jiuxin_weight_formula_sample_check` | stored=recalc=44.074，diff=2.1e-05 |
| 二面 | 能力评估行数 | `jiuxin_capability_family.*.rows` | 99,996 / 599,976 / 1 |
| 排除 | gkx 评分列 | `gkx_scholar_score_like_cols` | []（27 列 0 命中） |
| 排除 | dev 评分表 | `dev_talent_eval_like_tables` | [] |
| 口径 | UI mock 权重 | `ui_mock_ai_score_structure_reference` | 78.7（演示结构披露） |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 现成综合评分面 | jiuxin | `ads_talent_profile` 评分组 | 100,000（100.0%） | 直查 | **有（口径 A）** |
| D2 | 第二评分面 | jiuxin | `ads_talent_capability_assessment` 族 | 99,996 / 599,976 / 1 | 直查 | 有（口径 B，深圳 scope） |
| D3 | 权威度维（需求） | 三源 | — | — | **不存在** | **缺（主降档因）** |
| D4 | 社会影响维（需求） | 三源 | — | — | **不存在** | **缺（主降档因）** |
| D5 | 创新性/项目经验维 | jiuxin | citation/h_index/project_count | 100,000 | 直查/映射 | 有 |
| D6 | UI 演示值 | UI | data.js aiScore | — | mock | 边界证据（不作源） |

`support_judgment="部分支持"`、产物与文首一致。

### 3.2 D1/D2 双面结构与覆盖（久新）

学术力面（口径 A）五分项覆盖 99.87%-100%（`jiuxin_profile_score_nonnull` 逐键在案），weight_coverage 语义自洽（Core 有值 1.0000/缺值 0.9500，产物 `jiuxin_weight_coverage_min/max`）。能力评估面（口径 B）99,996 行与主画像 100,000 差 4 行（eligibility 过滤的正常损耗），dimension_metric 明细面 599,976 行 = 人均约 6 条维度明细，审计链完整（calculation_method 逐条在册）。

### 3.3 D3/D4 需求两维的 absence_probe 全记录

否定性证据三件套：**查了什么**——gkx 280 表 talent/scholar×五评分词族交叉 + `dwd_scholar` 27 列逐一核对；dev 全 schema talent/scholar/expert×评分词族；久新 203 表 capability 族维度清单核对（四维=毅力/创新/学科匹配/政治倾向，无权威度/社会影响维）。**条件**——表级与列级存在性。**命中**——0。四缺失情形归属：**表不存在**（权威度强度表/社媒传播表三源均无）——修复动作是接外部数据源（人才荣誉库/学术任职库/Altmetric 类），不是补数据。

### 3.4 现场复核清单

| 复核项 | 结果 |
|---|---|
| 主画像评分覆盖 | 100,000/100,000 = 100.0%（全量非采样） |
| 权重公式复算 | abs_diff 2.1e-05（逐位一致） |
| 分布形态 | 10 桶平滑，均值 51.5532 |
| capability 模型 | 1 行在册，公式+权重+快照血缘全录 |
| gkx 评分承载 | 27 列 0 命中 |
| dev 评分承载 | 词族 0 命中 |
| 脚本形态 | 三源串行只读；零 demo_* |

## 四、数据缺失情况

### 4.1 权威度与社会影响两维零承载（结构级，主因）

需求五维中权威度（荣誉/奖项/学术任职的强度量化）与社会影响（学术圈外的传播/政策引用）在三源均无承载：gkx 学者面只有文献计量原始计数；久新 taxonomy 称谓族是分类关系（是否院士/是否领军）而非强度评分；dev 无人才评估面。四缺失情形归属「表不存在」，修复只能靠外部数据源——人才荣誉库（国家级人才计划入选强度）、学术任职库（学会/期刊编委）、Altmetric 类传播数据。这与 CHINESE_RATIO 件的判定维缺失同型：需求点名的判定轴库内无字段，proxy 会悄悄改口径（B10 禁止）。

### 4.2 口径三套并存待裁（方法级，次因）

库内口径 A（学术力五分项）与口径 B（深圳问题匹配四维）都是现成、可审计的评分面，但与需求五维三套互不同物。口径 B 还有 scope 限制（模型名明示深圳基础研究问题匹配），直接复用会引入地域偏置。裁定权在甲方：出官方映射表（哪维↔哪分项、权重多少）或指定采库内某套——裁定前本件保守交付口径 A 的证据面读数，不合成伪综合分。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 甲方出维度映射表/指定口径 | 口径裁定 | 本件即期可升档 | 触发器①（§1.6） |
| 权威度数据源接入（荣誉/任职库） | 外部数据源 | 本件 + TALENT 族评价件 | 补需求维 |
| 社会影响数据源接入（Altmetric 类） | 外部数据源 | 本件 | 补需求维 |
| 复用 capability 面默认分策略 | 工程范式 | 族内缺口维处理 | 无数据维统一默认分+状态标注 |

档位后果：口径裁定 → **完全直接支持**（双面直查）；仅补两维外部源（不裁口径）→ 完全转换支持；现状 → 部分支持。推荐顺序：先裁口径（零成本即期），外部源接入列中期。

## 参考文献

1. 科技部等八部门印发《关于开展科技人才评价改革试点的工作方案》的通知（国科发才〔2022〕255 号）[EB/OL]. 中华人民共和国科学技术部. https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/fgzc/gfxwj/gfxwj2022/202211/t20221109_183356.html （R1，2026-11-01 WebSearch 核验可达——按创新价值/能力/贡献导向构建分类评价体系，「破四唯立新标」，本件口径裁定的政策框架）
2. GB/T 44143-2024 科技人才评价规范[EB/OL]. 国家标准全文公开系统. https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=F103B9E696C8D48881568E5E9D45368C （R2，2026-11-01 WebSearch 核验可达——科技部提出、SAC/TC580 归口，2024-06-29 实施的创新价值/能力/创新贡献三方面指标规范，人才综合评分的国标锚）
3. Hirsch J E. An index to quantify an individual's scientific research output[EB/OL]. PNAS. https://www.pnas.org/doi/10.1073/pnas.0507655102 （R3，2026-11-01 WebSearch 核验可达——单指标合成传统及其「粗略近似」局限，库内五分项加权设计的反面参照）

# 附件

## 附录 A 原始需求原文摘录

主需求《科技信息展示系统和科技专题服务系统.md》:2447-2449（1.1.1.1.4.3.4.4.2 多维综合评价与评分）：

> 功能基于权威度、创新性、项目经验、社会影响等多维量化指标，通过人工智能算法进行综合评分，帮助用人单位快速对专家进行定量评价，优选具备潜力和实力的人才。

:2441（L5 功能清单）：

> 人才尽调报告与推荐的具体功能包括专家画像智能生成、多维综合评价与评分、定制化尽调报告生成、专家智能推荐、动态跟踪与更新、风险与合规性评估、团队组合与协同分析。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 多维综合评价与评分 | 主需求 | 2（:2441 清单 + :2447 叶） |
| 多维综合评价 | SRS 人才族 | 同文转述 |
| 多维综合评价/评分 | 核增需求 | 0 |
| 多维综合评价 | 科技专题服务算法库.md | 0 |
| aiScore/ai 评分 | UI data.js | :1486-1502（mock 生成器） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_TALENTIR_002_out.json`（2026-11-01 实跑：三源探针 + 学术力面全量读数 + capability 三表族首探）。
- 共享快照：`code/_snapshots/_shared_probe_s3_01_out.json`（gkx dwd_scholar 21,316——B11 锚）。
- 族内对账：`M_SCIUI_X_015_out.json`（久新 talent 族表清单）；`M_TALENT_UI_CHINESE_RATIO.md` 久新回填段（ads_talent_profile 100,000）。

### B.2 本件产物逐键清单（`code/M_SCIUI_TALENTIR_002_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `facts.gkx_table_count` | 计数 | 280 | §2.5 |
| `facts.gkx_talent_eval_like_tables` | 探针 | `[]` | §2.5/§3.3 |
| `facts.gkx_scholar_rows` | 计数 | 21,316 | §2.5/B11 |
| `facts.gkx_scholar_score_like_cols` | 探针 | `[]`（27 列 0 命中） | §3.3 |
| `facts.dev_talent_eval_like_tables` | 探针 | `[]` | §2.5 |
| `facts.jiuxin_talent_profile_rows` | 计数 | 100,000 | §2.2 |
| `facts.jiuxin_profile_score_nonnull` | 覆盖 | 七分项逐一非空数 | §2.2/§3.2 |
| `facts.jiuxin_academic_capability_avg` | 统计 | 51.5532 | §2.3 |
| `facts.jiuxin_academic_capability_decile` | 分布 | 10 桶 | §2.3 |
| `facts.jiuxin_top5_by_academic_capability` | 样例 | 5 人（rank/name/分项分） | §2.3 |
| `facts.jiuxin_weight_formula_sample_check` | 复算 | abs_diff=2.1e-05 | §2.3 |
| `facts.jiuxin_capability_family` | 结构 | 三表 99,996/599,976/1 行+全列 | §2.4 |
| `facts.jiuxin_capability_model_rows_detail` | 登记 | 模型公式原文 | §2.4 |
| `derived[0].jiuxin_academic_capability_coverage_pct` | 派生比 | 100.0（100,000/100,000） | §2.2 |
| `derived[1].ui_mock_ai_score_structure_reference` | 披露 | 78.7（mock 结构披露） | §1.6 |
| `absence_probe` | 探针 | 三件（gkx/dev/doc） | §3.3 |
| `support_judgment` | 判档 | 部分支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 维度结构 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| 国标三方面 | GB/T 44143-2024（R2） | 创新价值/能力/创新贡献 | 学术力面可映射 | **高（框架锚）** |
| 分类评价试点 | 国科发才 255 号（R1） | 四类×价值/能力/贡献 | career_stage 分层在 | 高（分类维可加） |
| 文献计量合成 | 学术力五分项（库内） | 论文/被引/H/合作/Core | **现成 100%** | **最高（即期可用）** |
| 深圳问题匹配 | capability 四维（库内） | 毅力/创新/匹配/政治 | 现成（scope 限深圳） | 中（地域偏置） |
| 单指标传统 | h 指数（R3） | 单数字 | h_index_score 在 | 低（粗略近似） |

### C.2 数据矩阵

| 依赖 | gkx | dev | jiuxin |
|---|---|---|---|
| 综合评分结果面 | 无（27 列原始计数） | 无 | **双面**（100,000 / 99,996 行） |
| 权重/审计维 | — | — | model+dimension_metric（公式/明细/血缘） |
| 权威度维 | 无 | 无 | 无（taxonomy 是分类非强度） |
| 社会影响维 | 无 | 无 | 无 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v0（现状） | 口径 A 证据面读数 + 口径裁定请求 | — |
| v1 | 甲方口径裁定 → 直查综合分接入 UI | 映射表/指定函 |
| v2 | 权威度外部源接入 → 五维四闭合 | 数据源立项 |
| v3 | 社会影响源接入 → 五维闭合 | 数据源立项 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 三套口径混用（需求/UI/库内） | **高** | 裁定前只出证据面读数；映射表公示 |
| 口径 B 地域偏置（深圳 scope） | 中 | 不作普适尽调分；scope 随行披露 |
| 权威度维 proxy 化（拿 h_index 冒充） | 中 | 两跳止步规则；不代理不推测 |
| mock 权重被当真 | 中 | 结构披露键+「演示值」标注 |

### C.5 总判

**部分支持**：久新双评分面结构+数据双在（100% 覆盖、公式可审计）是族内最强数据面；降档唯一根因是需求五维与库内维度集不同物（权威度/社会影响两维三源零承载）。升档触发器两条（口径裁定→完全直接支持；两维外部源→完全转换支持）写死不悬空。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_TALENTIR_002.py` | 退出码 0，落 `_out.json` |
| 数据入口 | `_gkxdb.py`（gkx）+ 直连 dev/久新 | demo_* 直接 raise |
| 判档一致 | 文首 vs `support_judgment` | 部分支持 |
| B11 对账 | gkx 21,316 = 共享快照；久新 100,000 = 族内件 | 零漂移 |
| 幂等重跑 | SQL 全只读无随机 | 逐位一致 |
| mock 残留 | `ui_mock_ai_score_structure_reference` | 标注「演示结构披露，不参与结论」 |
