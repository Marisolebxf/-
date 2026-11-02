# 学者未来产出增长预测值（M_SCIUI_TALENTIR_009）

> **类型**：需业务建模类（预测模型输出面未立项，动量面+时序原料双在）｜ **域**：科技信息展示系统·人才引进推荐评估·学者贡献度分析（预测视图缩放）｜ **UI 挂载**：科技信息展示系统 → 人才引进推荐评估 → 贡献度 Tab（预测视图）→ `ContributionTab.jsx:311`（`predictViewMap.stage: { factor: 1.15, label: '阶段增长预测' }`）
> **数据支持度**：**部分支持**｜ **公式定义人**：无（需求 :2355-2357 只给视图切换行为「支持对贡献度预测结果的缩放，用户可切换整体预期、局部影响及阶段性增长视图」，预测算式无）｜ **口径归属**：需求明列行为（主需求 1.1.1.1.4.3.4.1.3(2) 预测视图缩放），「学者未来产出增长预测值」为派单书按 UI 视图语义定名；`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_TALENTIR_009.py`｜ **产物**：`code/M_SCIUI_TALENTIR_009_out.json`
> **四判定摘要**：直接结构 = 无（三源无学者个体产出预测输出面）；直接数据 = 无（同左）；依赖结构 = 部分（久新 potential 动量面 + ads_talent_yearly_metrics 时序原料结构在；gkx 仅快照计数列）；依赖数据 = 部分（动量分 80.17% 覆盖、时序原料 100.0% 覆盖人才池但模型未立项）
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

**本件判定：部分支持。** 按 Lane 6 判定框架（模型承载 = 三源有结构化模型输出面才部分支持）逐层核验：**预测输出面**——三源无「学者个体未来产出增长预测值」模型输出面：久新 forecast 词族命中 3 张（`ads_research_outcome_forecast`/`ads_research_outcome_scope_forecast`/`ads_research_problem_forecast_yearly`）全部是科研问题/技术域的总量预测面（`ads_research_outcome_forecast` 是科研成果总量预测非学者个体粒度）；gkx `dwd_scholar` 27 列只有 paper_nums/citation_nums/h_index/reference_nums 快照计数列（快照≠时序），无逐年序列无预测面；dev 命中 3 张均为企业/政策侧表。**部分承载**——久新双面在：`ads_talent_potential_result`（100,000 行）是面向未来的动量型评估面，`output_momentum_score`（产出动量分）覆盖 80.17%（80,170/100,000），观察窗 2021-2025——「近年产出加速度」的评估分，语义近邻（增长趋势方向）但非外推预测值（无预测目标年、无置信区间）；`ads_talent_yearly_metrics`（1,278,048 行覆盖 100,000 人才即主画像池 100.0%，年份跨度 1952-2026）是学者×年产出序列——回归外推模型（Acuna 型，R2=0.67 的 CV 特征回归先例）的原料结构+数据量双在。`scholar_future_output_growth_forecast = null`（B10 不写伪预测值）。

### 批次通用纪律摘要（S3-03 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 动量覆盖分母=同表全量；时序覆盖分母=profile 池（跨表口径差异 note 写死） |
| B4 | 负结论带探针 | 四件 absence_probe（gkx/dev/jiuxin/doc，§3.3） |
| B5 | 确定性 | career_stages 按 stage 排序；词族扫描固定顺序 |
| B6 | 闸门自身被闸 | 不自跑闸门，派单方统一 |
| B7 | 产物只由脚本产出 | 改脚本→重跑；产物零手改 |
| B8 | 回执不复收 | 探针 SQL 幂等可复验 |
| B9 | 单位/日期陷阱 | 年份跨度含 1952 早段（建库回溯值）；动量分 0-100 分制 |
| B10 | 口径裁定保守交付 | 不写伪预测值；derived 留 null + mock 因子登记；升档触发器写死 |
| B11 | 多本账互推 | potential 100,000/capability 99,996 与族内件零漂移；yearly 1,278,048 与 DATAOV_002 一致 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有学者个体产出预测输出面吗？ | 无 | forecast 词族 3 张全为科研问题/技术域总量面（§3.3） |
| 有面向未来的评估面（语义近邻）吗？ | 有 | potential 动量面 80.17% 覆盖（§3.2） |
| 外推模型的原料在吗？ | 在（结构+数据量双在） | yearly_metrics 1,278,048 行/100,000 人/100.0%（§3.2） |

## 摘要

「学者未来产出增长预测值」是贡献度分析预测视图的「阶段性增长视图」数值（主需求 :2355-2357：引进模拟场景下切换整体预期/局部影响/阶段性增长视图）。UI 侧它是 `ContributionTab.jsx:311` 的 `predictViewMap`——stage 因子 1.15/overall 1.05/local 0.85 全是前端常量（近两年点 v×factor+斜率外推），mock 演示值。数据侧三源均无学者个体产出预测模型输出面（久新 forecast 表族是科研问题/技术域预测），但久新双承载在：potential 动量面（`output_momentum_score` 覆盖 80.17%，观察窗 2021-2025，分布 [0,100] 均值 50.0——「近年产出加速度」评估分，语义近邻非预测值）与 `ads_talent_yearly_metrics` 时序原料（1,278,048 行覆盖 100,000 人才 100.0%，年份跨度 1952-2026，22 列含 paper_count/citation_count/专利/项目/合作——Acuna 型回归外推的原料结构+数据量双在）。判**部分支持**：预测模型未立项（无目标年/无置信区间的输出面），但按 Lane 6 框架有结构化模型输出面（动量面）+转换原料双在。脚本已跑通，产物与正文数字逐一对应。

- 需求判定：**需求明列行为**（:2355-2357 预测视图缩放），视图名在、预测算式无。
- 复现状态：脚本已跑通；三源排除探针 + 动量面/时序原料读数全落产物。
- 档位结论：**部分支持**（预测输出面未立项 + 动量面/时序原料双在）。
- 关键事实：`ads_talent_yearly_metrics` 100.0% 覆盖主画像池（100,000/100,000）——外推模型的数据量前提已闭合，缺的只是模型工程立项。
- 升档路径：甲方裁定预测口径=potential 动量分代理 → 完全直接支持（触发器①）；基于 yearly_metrics 建外推模型 → 完全转换支持（触发器②）。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技人才态势/人才引进推荐评估/**学者贡献度分析·智能分析与推荐（预测视图缩放）**（主需求 1.1.1.1.4.3.4.1.3(2)）。UI 实际容器是人才引进推荐评估页贡献度 Tab 的预测图：`ContributionTab.jsx:302` `predictOption` 双折线（历史贡献 vs 预测线），`:307-311` `predictViewMap` 三视图常量——overall `{factor:1.05, label:'整体预期贡献'}`/local `{factor:0.85, label:'局部影响预估'}`/stage `{factor:1.15, label:'阶段增长预测'}`；预测线算法是 `:313` 前端外推：`i >= actual.length - 2 ? Math.min(100, Math.round(v * cfg.factor + (i - actual.length + 3) * 2)) : v`——即近两年点乘因子加斜率增量再封顶 100，无任何模型输入。本件挂载 :311（stage 因子行）；`:316` 预测系列渲染。「阶段增长预测」对应「学者未来产出增长」的阶段性视图，因子 1.15 是演示放大系数（mock 登记，不作数据证据）。

### 1.2 为什么需要本指标

引进决策的时间结构决定了预测的必要性：贡献度分析看的是历史存量，而引进买的是未来产出——一名 52 岁高存量的学者与一名 34 岁高增速的学者，历史贡献图分不出优劣，产出增长预测才能。需求把预测视图放进「引进模拟场景」（:2356 原文）：用户在模拟不同引进方案时，切换整体预期/局部影响/阶段性增长三种视图，本质是对「未来产出」做乐观/悲观/分期三档情景分析——这是人才投资决策的标准姿势（对应学术界的 tenure 决策场景，Acuna et al. 正是为 hiring committee 的 CV 审视提供统计辅助）。数据侧的落点因此是「未来产出」的可计算性：库内有没有面向未来的评估面（动量/潜力），有没有逐年产出序列（外推原料），有没有现成的预测输出面（目标年+预测值+置信区间）——三问分层探针即是本件调研主线。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**主需求 :2355-2357（1.1.1.1.4.3.4.1.3(2) 预测视图缩放）给出的是视图切换行为：「在引进模拟场景中，支持对贡献度预测结果的缩放，用户可切换整体预期、局部影响及阶段性增长视图，灵活掌控分析细节」——「贡献度预测结果」如何产生（模型？外推？专家判断？）、「阶段性增长」的期数与算式，一个字都没有。核增需求与算法库两份真源检索 0 命中（附录 A.2）。UI 的因子外推是前端演示算法，不构成口径证据。

### 1.4 类似指标权威方法可行性分析概要

「未来学术产出预测」的权威方法锚是 Acuna-Allesina-Kording 模型（R1，Nature 2012）：用 CV 特征（论文数/h 指数/首篇发表年数/顶刊论文数/期刊多样性）做 elastic net 正则化线性回归，预测 5 年后 h 指数，神经科学家样本交叉验证 R2=0.67——该方法证明了「CV 快照特征 → 未来产出」的统计可预测性。其二，Mazloumian（R2，PLOS ONE 2012）的时序口径：年度被引是未来被引的最佳预测子，但「未来论文的被引」几乎不可预测（1 年期预测尚可、长期失效）——提示预测窗越长不确定性越大，置信区间必设。其三，预测类指标的方法论纪律（M_INNOV_IMPACT_FORECAST 范式）：区间覆盖率与 `na` 占比必须并列报告，只报覆盖率会高估区间质量。方法族对照：

| 方法族 | 代表 | 特征面 | 数据要求 | 与三源匹配 |
|---|---|---|---|---|
| CV 特征回归（Acuna 型） | R1 | 论文/引用/h 指数快照 | 快照特征+未来标签 | **原料全在**（yearly_metrics 22 列） |
| 时序外推（Mazloumian 型） | R2 | 逐年产出序列 | 学者×年面板 | **面板在**（1,278,048 行/100.0%） |
| 动量评估（库内 potential 面） | 久新工程 | 近年产出加速度 | 观察窗序列 | **有面**（80.17% 覆盖，非外推） |
| 前端因子外推 | UI predictViewMap | mock 因子 | mock 常量 | 结构披露（不作源） |

结论：Acuna 型与 Mazloumian 型的原料在久新时序面板全部可得（结构+数据量双在），缺的是模型工程立项；potential 动量面是唯一的「面向未来」现成评估面但非预测值。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/talent-trend/components/ContributionTab.jsx:311`（stage 因子 1.15）、`:307`（predictViewMap 结构）、`:316`（预测系列渲染）、`:313`（前端外推式）；mock 语义源同段常量。
- 主需求：`科技信息展示系统和科技专题服务系统.md`:2355-2357（1.1.1.1.4.3.4.1.3(2) 预测视图缩放），原文见附录 A。
- 权威方法：R1 Acuna et al. Nature 2012（PMC 全文）；R2 Mazloumian PLOS ONE 2012。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**推测定义（须披露口径不闭合）**：若模型立项，预测值的推测算式为分期外推：

$$\hat{P}_{t+h} = f(\mathbf{x}_t),\quad \mathbf{x}_t = \{P_{t-k..t}, C_{t-k..t}, \text{career\_stage}, \ldots\},\ h \in \{1,2,3\}$$

即以学者×年产出面板（论文数 P/被引 C 序列+职业阶段）训练回归（Acuna 型 elastic net 或时序模型），输出目标年 h 的产出预测值与置信区间——**此算式当前无从直接落地**（模型未立项：无训练管线、无目标年定义、无区间输出）。库内可交付的两条候选口径（不派生，B10）：**口径 A（现成直查）** potential 动量分 = `output_momentum_score`（近年产出加速度评估分，方向语义近邻——动量高≈增长趋势向上）；**口径 B（转换可算）** yearly_metrics 面板外推（原料 100.0% 覆盖，需模型工程立项）。

**降档/升档触发器（B10 模板）**：①甲方裁定预测口径=potential 动量分代理（披露「评估分非预测值，无目标年」）→ 现成直查升**完全直接支持**；②基于 yearly_metrics 建外推模型（目标年+置信区间随行，区间覆盖率与 na 占比并列报告）→ **完全转换支持**；③维持现状（模型未立项）→ 部分支持。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在需求文档 | 主需求《科技信息展示系统和科技专题服务系统.md》（SRS 人才引进推荐评估同文转述） |
| 所属四级功能 | 1.1.1.1.4.3.4 人才引进推荐评估 |
| 所属 L5 | 学者贡献度分析（1.1.1.1.4.3.4.1）→ 智能分析与推荐（:2353 起 3 叶） |
| 本件叶 | **预测视图缩放（1.1.1.1.4.3.4.1.3(2)）——需求明列行为（阶段性增长视图）** |
| 同族近邻 | 自动深度分析（(1)）/ 智能交互反馈（(3)）；TALENTIR_008（分阶段产出增长——历史对比轴，本件是未来预测轴） |
| UI 容器 | `ContributionTab.jsx` 预测图三视图 |

本件与 TALENTIR_008（近 3 年产出增长，挂 `ContributionTab.jsx:741`）构成贡献度分析的时间双轴：008 看历史增量（面板直接可算），本件看未来增量（需模型外推）——两件的档位差（008 部分支持因历史面板在；本件部分支持因模型面在原料在但输出面缺）体现了「同一容器内历史/未来的数据面分层」。与 TALENTIR_003 的对照见 003 §1.7。

## 二、计算过程

### 2.1 方法选择（文献依据）

若模型立项，方法选 **CV 特征回归 + 时序面板外推的双轨**：Acuna 型（R1）证明 CV 快照特征可预测 5 年后 h 指数（R2=0.67），其特征面（论文数/引用/h 类/职业阶段）在 `ads_talent_yearly_metrics` 22 列中全部有对应列；Mazloumian 型（R2）的时序口径提示年度产出量是更直接的预测子但长期预测失效——所以目标年应设近窗（h=1-3 年）并强制置信区间。选择理由：其一，原料面板 100.0% 覆盖（100,000 人才全量有逐年序列），数据量前提闭合；其二，库内已有 potential 动量面作方向性参照（动量分高≈增长趋势向上），可作模型的基线对照；其三，预测类纪律（区间覆盖率与 na 占比并列）从 M_INNOV_IMPACT_FORECAST 范式继承。模型未立项前本件不产出预测值（B10），仅交付 §2.2-2.4 的面读数与原料盘点。

### 2.2 预测输出面排除（三源词族 + 语义核对）

**gkx**：280 表 forecast/predict/potential/yearly/trend/momentum 词族 0 命中；`dwd_scholar` 27 列时序/预测词族 0 命中——只有 paper_nums/citation_nums/h_index/reference_nums 快照计数列（快照≠时序，无逐年序列无预测面）。**dev**：gkxlumenx_* 16 schema 542 表词族命中 3 张（`impact_prediction`/`policy_prediction_indicator`/`scholar`）——企业影响/政策指标预测与学者快照表，无学者个体产出预测面。**久新**：210 表词族命中 3 张 `ads_research_outcome_forecast`/`ads_research_outcome_scope_forecast`/`ads_research_problem_forecast_yearly`——逐张语义核对全部是 research_problem/technology 域预测面（科研问题预测/技术域预测/成果总量预测），`ads_research_outcome_forecast` 是科研成果总量预测非学者个体粒度。结论：学者个体「未来产出增长预测值」输出面三源未立项。

### 2.3 动量面读数（口径 A 候选）

久新 `ads_talent_potential_result` 100,000 行：`potential_composite_score` 非空 80,170；`output_momentum_score`（产出动量分）非空 80,170（派生键 `jiuxin_output_momentum_coverage_pct` = 80.17%，分子分母同表同 WHERE 全量非采样），分布 min/max/avg = 0.0/100.0/50.0。观察窗 `jiuxin_potential_window` = [2021, 2025]（observation_start/end_year）；职业阶段分布 `jiuxin_potential_career_stages`：0_4 年 10,353 人/5_9 年 21,961 人/10_14 年 67,684 人/未标 2 人——池以职业中期（10_14 年）为主。动量分的语义边界（写死，防误读）：它是**观察窗内产出加速度的评估分**（近年产出较早期的增速），方向语义与「产出增长预测」同族（动量高→增长趋势向上），但它没有预测目标年、没有置信区间、没有外推算式——**是评估不是预测**。作口径 A 代理须随行披露此边界。

### 2.4 时序原料读数（口径 B 前提）

久新 `ads_talent_yearly_metrics`（DESC 实测 22 列：talent_id/year/paper_count/citation_count/first_author_paper_count/corresponding_author_paper_count/patent_application_count/patent_grant_count/patent_metrics_as_of_date/patent_metric_definition_version/project_count/collaborator_count/institution_count/institution_cooperation_count/new_topic_count/academic_capability/industrial_capability/score_version/metric_definition_version/metrics_as_of_date/data_version/update_time）：行数 1,278,048，去重 talent 100,000（派生键 `jiuxin_yearly_metrics_talent_coverage_pct` = 100.0%，分母=profile 全池 100,000——跨表面分母，口径差异在 note 写死，B3）；年份跨度 [1952, 2026]——早段年份（1952 起）是学术生涯回溯建库值，外推建模时应取近窗（如近 10 年）截取。Acuna 型特征面（论文数/引用/合作者/职业阶段代理）与 Mazloumian 型时序口径（逐年产出量）在该面板全部可得：**原料结构+数据量双在，转换路径成立**，缺的只是模型工程（训练管线/目标年定义/区间输出）。

### 2.5 稳健性与口径敏感性

预测口径的两向风险定性：其一，面板的**回溯性偏差**——yearly_metrics 的早段年份（1952-2000）是回溯建库，边缘学者早年记录可能不全，近窗截取（近 10 年）可规避；其二，**幸存者偏差**——potential 面覆盖 80.17%（80,170/100,000），未覆盖的 19,993 人在动量分口径下缺席（可能是观察窗内无产出者），若把动量分当预测值用，会系统性高估全体池的增长前景；其三，Acuna 模型的学科迁移性——原模型在神经科学家样本训练（R2=0.67），跨学科套用需重训（本池 career_stages 以 10_14 年中期为主，与原样本 5-12 年窗接近但学科分布未知）。三风险都指向同一条交付纪律：模型立项前不产出预测值，口径 A 代理须带边界披露（B10）。

### 2.6 需求符合性预评

需求要的是「贡献度预测结果的缩放视图」（三情景切换）。即便口径 A（动量分）被裁定代理，它只给**单一数值**（0-100 动量分）而非**分期序列**——三视图（整体/局部/阶段性）的情景结构需要模型输出「分目标年序列」才能支撑，单一动量分只能填一个视图。所以完整需求满足必须走口径 B（模型外推分期输出）；口径 A 是降级展示。此预评写入升档触发器的优先级：触发器②（模型）优先于触发器①（代理）。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_TALENTIR_009.py`（三源串行只读；gkx 经 `_gkxdb.py`；dev/久新直连；零 `demo_*`）；运行 `python3 code/M_SCIUI_TALENTIR_009.py`。
- 产物：`code/M_SCIUI_TALENTIR_009_out.json`。正文数字与产物键逐一对应：`gkx_table_count=280` + `gkx_forecast_like_tables=[]` + `gkx_scholar_snapshot_cols`（4 快照列）+ `gkx_scholar_timeseries_cols=[]`（§2.2）、`dev_forecast_like_tables`（3 张语义排除）（§2.2）、`jiuxin_potential_result_rows=100000` + `jiuxin_potential_composite_nonnull=80170` + `jiuxin_potential_momentum_nonnull=80170` + 派生键 `jiuxin_output_momentum_coverage_pct=80.17` + `jiuxin_output_momentum_min_max_avg=[0.0,100.0,50.0]` + `jiuxin_potential_window=[2021,2025]` + `jiuxin_potential_career_stages`（§2.3）、`jiuxin_yearly_metrics_cols`（22 列）+ `jiuxin_yearly_metrics_rows=1278048` + `jiuxin_yearly_metrics_talents=100000` + 派生键 `jiuxin_yearly_metrics_talent_coverage_pct=100.0` + `jiuxin_yearly_metrics_year_span=[1952,2026]`（§2.4）、`jiuxin_forecast_like_tables`（3 张语义排除）（§2.2/§3.3）、`scholar_future_output_growth_forecast=null`（B10 留空）。
- 结果解读：预测输出面三源未立项（词族+语义双排除）+ 动量面语义近邻读数（80.17% 覆盖，观察窗 2021-2025）+ 时序原料双在（100.0% 覆盖，1,278,048 行）——「模型缺、原料全」，derived 留 null 即负结论登记。
- 对照需求功能要求的评审：「支持对贡献度预测结果的缩放，用户可切换整体预期、局部影响及阶段性增长视图」——**部分满足**：口径 A（动量分）可填单一视图但无分期序列；口径 B（面板外推）原料闭合但模型未立项；三视图情景结构需模型分期输出（§2.6 预评）。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 排除 | gkx 预测表族 | `gkx_forecast_like_tables` | [] |
| 排除 | gkx 学者时序列 | `gkx_scholar_timeseries_cols` | []（仅 4 快照列） |
| 排除 | dev 预测承载 | `dev_forecast_like_tables` | 3 张（语义排除） |
| 排除 | 久新预测表族 | `jiuxin_forecast_like_tables` | 3 张（科研/技术域，语义排除） |
| 动量 | potential 行数 | `jiuxin_potential_result_rows` | 100,000 |
| 动量 | 动量分覆盖 | `jiuxin_output_momentum_coverage_pct` | 80.17%（80,170/100,000） |
| 动量 | 动量分分布 | `jiuxin_output_momentum_min_max_avg` | [0.0, 100.0, 50.0] |
| 动量 | 观察窗 | `jiuxin_potential_window` | [2021, 2025] |
| 动量 | 职业阶段 | `jiuxin_potential_career_stages` | 0_4:10,353 / 5_9:21,961 / 10_14:67,684 / None:2 |
| 原料 | 面板行数 | `jiuxin_yearly_metrics_rows` | 1,278,048 |
| 原料 | 覆盖人才 | `jiuxin_yearly_metrics_talent_coverage_pct` | 100.0%（100,000/100,000） |
| 原料 | 年份跨度 | `jiuxin_yearly_metrics_year_span` | [1952, 2026] |
| 预测 | 增长预测值 | `scholar_future_output_growth_forecast` | null（B10） |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 学者产出预测输出面 | 三源 | — | — | **不存在** | **缺（主降档因）** |
| D2 | 动量评估面（口径 A） | jiuxin | `ads_talent_potential_result.output_momentum_score` | 80,170（80.17%） | 直查 | **有**（评估非预测） |
| D3 | 逐年产出面板（口径 B 原料） | jiuxin | `ads_talent_yearly_metrics`（22 列） | 1,278,048（100.0% 人才） | 聚合可算 | **有** |
| D4 | 学者快照特征 | gkx | `dwd_scholar.paper_nums` 等 4 列 | 21,316 | 直查 | 有（快照≠时序） |
| D5 | UI 演示值 | UI | data.js/predictViewMap 因子 | — | mock | 边界证据（不作源） |

`support_judgment="部分支持"`、产物与文首一致。

### 3.2 D2/D3 读数的覆盖与量级（久新）

动量面 80.17% 覆盖（80,170/100,000，同表全量非采样）：未覆盖的约两成人才在观察窗（2021-2025）内无可评估产出——这部分人在动量分口径下缺席（§2.5 幸存者偏差）。时序面板 100.0% 覆盖（100,000/100,000，分母=profile 全池，跨表口径 note 写死）：数据量前提闭合，Acuna 型特征（论文/引用/合作/阶段）全列在。两面的互补结构：动量面给**方向**（谁在增长），面板给**幅度**（每年增长多少）——预测模型（口径 B）可用面板训练、用动量面做基线校验。

### 3.3 D1 的 absence_probe 全记录

否定性证据三件套：**查了什么**——gkx 280 表 forecast/predict/potential/yearly/trend/momentum 词族 + `dwd_scholar` 27 列时序词族；dev 16 schema 542 表 forecast/predict/potential/scholar/talent 词族；久新 210 表 forecast/predict 词族 + 命中表逐张语义核对；三份需求真源算式段。**条件**——表级/列级存在性 + 语义核对（预测主体是否为学者个体、粒度是否个体级）。**命中**——0（语义级：久新 3 张命中表全为科研问题/技术域/成果总量预测面，非学者个体）。四缺失情形归属：**表不存在**（学者个体预测输出面三源均无——修复动作是模型工程立项，不是补数据）。

### 3.4 现场复核清单

| 复核项 | 结果 |
|---|---|
| gkx 预测表族 | []（0 张）；学者面仅 4 快照列 |
| dev 预测承载 | 3 张（企业/政策侧，语义排除） |
| 久新预测表族 | 3 张（科研问题/技术域，语义排除） |
| 动量分覆盖 | 80,170/100,000 = 80.17%（同表全量） |
| 观察窗 | [2021, 2025]；职业阶段 10_14 年 67,684 人为主 |
| 面板覆盖 | 100,000/100,000 = 100.0%（分母=profile 池，note 写死） |
| 面板年份 | [1952, 2026]（早段回溯值，建模取近窗） |
| 脚本形态 | 三源串行只读；零 demo_* |

## 四、数据缺失情况

### 4.1 预测模型输出面未立项（结构级，主因）

「未来产出增长预测值」需要模型输出面：目标年 × 预测值 × 置信区间的结构化结果表。三源实测无此面（§3.3 词族+语义双排除）——久新的 forecast 表族（3 张）预测主体是科研问题/技术域/成果总量，学者个体粒度未立项。这与 TALENTIR_003 的评分面缺口同型：需求/UI 点名的输出面，库内工程未覆盖。**四缺失情形归属「表不存在」**：修复动作是模型工程立项（训练管线+输出表设计），依赖侧（面板原料）已 100.0% 就位——这是本件与 003 的关键差别：003 连原料（引进事件）都缺，本件原料全在只缺模型。

### 4.2 动量面的语义边界（方法级，次因）

口径 A（动量分代理）的可用性受语义边界钳制：动量分是观察窗（2021-2025）内的加速度评估，无目标年/无区间/无分期——填不进需求的「三视图切换」情景结构（§2.6）。且覆盖 80.17%，两成池缺席。所以口径 A 只能作**过渡期单视图展示**（须随行披露「评估分非预测值」），完整需求满足必须走口径 B 模型立项。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 学者产出外推模型立项 | 模型工程 | 本件即期升档 | 触发器②（Acuna/Mazloumian 双轨，区间+na 并报） |
| 甲方裁动量分代理口径 | 口径裁定 | 本件零成本升档 | 触发器①（边界披露随行） |
| potential 面补全覆盖 | 数据回填 | 本件 + 族内潜力件 | 修复 19.83% 缺席 |

档位后果：模型立项 → **完全转换支持**；动量代理裁定 → **完全直接支持**（代理语义下）；现状 → 部分支持。推荐顺序：模型立项为主线（原料已闭合，工程启动即可分期交付），动量代理作过渡（零成本即期）。

## 参考文献

1. Acuna D E, Allesina S, Kording K P. Predicting scientific success[EB/OL]. Nature. https://www.nature.com/articles/489201a （R1，2026-11-01 WebSearch 核验可达——CV 特征 elastic net 回归预测 5 年后 h 指数 R2=0.67，学者未来产出可预测性的方法锚；全文镜像 https://pmc.ncbi.nlm.nih.gov/articles/PMC3770471/）
2. Mazloumian A. Predicting Scholars' Scientific Impact[EB/OL]. PLoS ONE. https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0049246 （R2，2026-11-01 WebSearch 核验可达——年度被引是未来被引最佳预测子、未来论文被引长期不可预测，时序口径与预测窗风险的方法依据）
3. OECD. Handbook on Measuring Human Capital Flows and Migration[EB/OL]. OECD. https://www.oecd.org/en/publications/handbook-on-measuring-international-migration-through-censuses_19de3ab8-en.html （R3，2026-11-01 核验可达——人才流动与能力评估的国际统计框架，人才评估面语义边界的对照锚）

# 附件

## 附录 A 原始需求原文摘录

主需求《科技信息展示系统和科技专题服务系统.md》:2355-2357（1.1.1.1.4.3.4.1.3(2) 预测视图缩放）：

> （2）预测视图缩放
> 在引进模拟场景中，支持对贡献度预测结果的缩放，用户可切换整体预期、局部影响及阶段性增长视图，灵活掌控分析细节。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 阶段性增长视图 | 主需求 | 1（:2357） |
| 预测视图缩放 | 主需求 | 2（:2353 清单 + :2355 叶） |
| 学者未来产出增长预测值 | 全部需求真源 | 0（派单书定名） |
| 产出增长预测 | 核增需求 | 0 |
| 增长预测 | 科技专题服务算法库.md | 0 |
| predictViewMap | UI ContributionTab.jsx | :307-:311（mock 因子） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_TALENTIR_009_out.json`（2026-11-01 实跑：三源排除探针 + 动量面/面板读数 + 预测未立项登记）。
- 共享快照：`code/_snapshots/_lane7_shared_probe_out.json`（jiuxin 210 表清单 + 评分/预测面列扫——B11 锚）。
- 族内对账：`M_SCIUI_TALENTIR_004_out.json`（profile 100,000 一致）；`M_SCIUI_TALENTIR_003_out.json`（potential 100,000/capability 99,996 一致）；`M_SCIUI_DATAOV_002_out.json`（yearly_metrics 1,278,048 一致）。

### B.2 本件产物逐键清单（`code/M_SCIUI_TALENTIR_009_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `facts.gkx_table_count` | 计数 | 280 | §2.2 |
| `facts.gkx_forecast_like_tables` | 探针 | `[]` | §2.2/§3.3 |
| `facts.gkx_scholar_snapshot_cols` | 结构 | 4 快照列 | §2.2 |
| `facts.gkx_scholar_timeseries_cols` | 探针 | `[]` | §2.2/§3.3 |
| `facts.dev_forecast_like_tables` | 探针 | 3 张（语义排除） | §2.2 |
| `facts.jiuxin_table_count` | 计数 | 210（2026-11-01 探测日） | §3.3 |
| `facts.jiuxin_potential_result_rows` | 计数 | 100,000 | §2.3 |
| `facts.jiuxin_potential_composite_nonnull` | 覆盖 | 80,170 | §2.3 |
| `facts.jiuxin_potential_momentum_nonnull` | 覆盖 | 80,170 | §2.3 |
| `facts.jiuxin_output_momentum_min_max_avg` | 统计 | [0.0, 100.0, 50.0] | §2.3 |
| `facts.jiuxin_potential_window` | 窗口 | [2021, 2025] | §2.3 |
| `facts.jiuxin_potential_career_stages` | 分布 | 四档计数 | §2.3 |
| `facts.jiuxin_yearly_metrics_cols` | 结构 | 22 列清单 | §2.4 |
| `facts.jiuxin_yearly_metrics_rows` | 计数 | 1,278,048 | §2.4 |
| `facts.jiuxin_yearly_metrics_talents` | 计数 | 100,000 | §2.4 |
| `facts.jiuxin_yearly_metrics_year_span` | 跨度 | [1952, 2026] | §2.4 |
| `facts.jiuxin_forecast_like_tables` | 探针 | 3 张（语义排除） | §2.2/§3.3 |
| `derived[0].jiuxin_output_momentum_coverage_pct` | 派生比 | 80.17 | §2.3 |
| `derived[1].jiuxin_yearly_metrics_talent_coverage_pct` | 派生比 | 100.0 | §2.4 |
| `derived[2].scholar_future_output_growth_forecast` | 负结论 | null（B10） | §1.6/§2.7 |
| `absence_probe` | 探针 | 四件（gkx/dev/jiuxin/doc） | §3.3 |
| `support_judgment` | 判档 | 部分支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 特征面 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| CV 特征回归 | Acuna（R1） | 快照特征+标签 | 面板 22 列全对应 | **最高（目标态）** |
| 时序外推 | Mazloumian（R2） | 逐年面板 | 1,278,048 行/100.0% | 高（近窗截取） |
| 动量评估代理 | 库内 potential 面 | 观察窗加速度 | 80.17% 覆盖 | 中（方向可用，无预测结构） |
| 前端因子外推 | UI predictViewMap | mock 因子 | mock 常量 | 结构披露（不作源） |

### C.2 数据矩阵

| 依赖 | gkx | dev | jiuxin |
|---|---|---|---|
| 学者个体预测面 | 无 | 无 | 无（forecast 族为科研/技术域） |
| 动量评估面 | — | — | **80,170 行/80.17%** |
| 逐年面板 | 无（仅快照列） | 无 | **1,278,048 行/100.0%** |
| 职业阶段 | — | — | career_stage 四档在 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v0（现状） | 动量面读数 + 原料盘点 + 口径裁定请求 | — |
| v1 | 甲方裁口径 A → 动量分过渡展示（边界披露） | 触发器① |
| v2 | 外推模型立项 → 分期预测值+区间输出 | 触发器②（区间与 na 并报） |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 动量分被冒充预测值 | **高** | 边界披露随行；不写「预测」字样挂动量分 |
| 面板早段回溯值污染模型 | 中 | 建模取近窗（近 10 年）截取 |
| 幸存者偏差（两成池缺席动量面） | 中 | 覆盖率随行披露；缺席人群单独标注 |
| 长窗预测失效 | 中 | 目标年设近窗（h=1-3）+强制区间 |

### C.5 总判

**部分支持**：预测输出面三源未立项（词族+语义双排除），但久新双承载在——动量面（80.17% 覆盖的方向性评估）+ 逐年面板（100.0% 覆盖的外推原料，结构+数据量双在）。与 003 的档位差构成族内对照：预测有原料、效果无分母。升档双路径（代理裁定零成本/模型立项工程量中等）写死在触发器。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_TALENTIR_009.py` | 退出码 0，落 `_out.json` |
| 数据入口 | `_gkxdb.py`（gkx）+ 直连 dev/久新 | demo_* 直接 raise |
| 判档一致 | 文首 vs `support_judgment` | 部分支持 |
| B11 对账 | potential 100,000=004；capability 99,996=003；yearly 1,278,048=DATAOV_002 | 零漂移 |
| 幂等重跑 | SQL 全只读无随机 | 逐位一致 |
| 伪预测值残留 | `scholar_future_output_growth_forecast` | null（无伪值） |
