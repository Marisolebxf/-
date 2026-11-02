# 模型预测准确率（M_SCIUI_KGANALY_011）

> **类型**：无业务逻辑数值类（模型评估读数）｜ **域**：科技信息展示系统·科技知识图谱·服务展示·图分析集成·图分析与业务决策联动｜ **UI 挂载**：`pages/tech-knowledge-graph/OptimizeDecisionPanel.jsx:128`（trainPerfOption legend 三线含「准确率」）→ `:133`（trainColumns 列 title=准确率, dataIndex=accuracy, render=`${v}%`）→ `:149`（runAutoTrain 传参生成新记录）
> **数据支持度**：**完全不支持**（三源均无模型训练记录/预测落盘/ground truth 标注面——准确率计算原料 TP/TN/FP/FN 无处产生；negative_evidence 在案；与 010 召回率姊妹件共证据同判）｜ **公式定义人**：UI 前端模拟（decisionModel.js runAutoTrain 的 Math.random 增益公式）｜ **口径归属**：需求明列叶（seq 453 图分析与业务决策联动），指标为「模型自动迭代」Tab 训练历史表+折线的准确率读数位
> **复现脚本**：`code/M_SCIUI_KGANALY_010_011.py`（010/011 姊妹件共用）｜ **产物**：`code/M_SCIUI_KGANALY_011_out.json`
> **四判定摘要**：直接结构 = 无（三源无模型评估面表结构）；直接数据 = 无；依赖结构 = **无**（无预测记录表、无标注表）；依赖数据 = **无**（词族 train/model/eval/predict/label/fraud/risk 三源 0 命中——唯一词面命中 dev evaluation_template 为配置模板、久新 ads_talent_capability_model 为评分权重配置，均语义排除）
> **数据源口径**：三源（开发库 live + 三方库 gkx + 久新 live 218 表当日实测）逐一探针留证；`demo_*` 禁引。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全不支持（negative_evidence）。**准确率 = (TP+TN)/(TP+TN+FP+FN)，计算原料是「模型预测记录 + 真实标注（ground truth）」对——与姊妹件 010（召回率）完全同构，三源逐一留证均无：①dev 542 表词族扫描（train/model/eval/predict）0 命中，`gkxlumenx_topic_enterprise.evaluation_template` 为企业评估**模板配置**面（语义排除），无训练记录、无预测落盘、无标注面；②gkx 280 表词族扫描（label/model/train/fraud/risk_eval）**0 命中**——要素库无风险分类场景立项；③久新 218 表词族扫描（feedback/model/train/label/fraud/risk/eval/blacklist）实质 0 命中——唯一词面命中 `ads_talent_capability_model` 经 SHOW CREATE TABLE 实查为人员能力综合评分**权重配置**表（research_perseverance_weight 等 9 个权重/阈值列，无 accuracy/recall/预测/标注列），语义排除；blacklist/trigger 词族 0 命中。UI 现状（mockData decisionTrainHistory 三条 accuracy 92.8/90.1/88.4）是写死演示数据，`runAutoTrain` 新纪录由 `decisionModel.js:23` 的 `accuracy = min(97, base + boost*(0.3+Math.random()*0.8))` 纯前端模拟生成——文件头自注「本地规则模拟自适应/训练/反馈，真源待 algo 训练管线」。

### 批次通用纪律摘要（S3-06 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（§2.8 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | accuracy 以全体样本为分母（同基），B9 披露模拟公式无此结构 |
| B4 | 负结论带探针 | absence_probe 三件（三源逐一，verdict_kind=negative_evidence；与 010 共证据） |
| B5 | 确定性 | 词族扫描 GROUP BY/SHOW CREATE TABLE 幂等 |
| B6 | 闸门自身被闸 | 不自跑闸门，派单方统一 |
| B7 | 产物只由脚本产出 | py 实探落 _out.json |
| B8 | 回执不复收 | 探针 SQL 幂等可复验 |
| B9 | 单位/日期陷阱 | % 读数但分母（全体评估样本）无承载；mock 时间 2026-04/05 为编造演示时间非真实训练时间 |
| B10 | 口径裁定保守交付 | 不拿模拟公式输出冒充准确率读数 |
| B11 | 多本账互推 | mock 三条与 mockData.js:586-588 逐值一致；词族计数与族级快照一致 |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有模型预测+标注对吗？ | 无 | absence_probe 三件 |
| 可从现有图/合作数据近似推导吗？ | 不可 | 科技图谱域无「欺诈/违约」风险场景立项，正负样本无处定义 |
| 有可转换的替代口径吗？ | 无 | 久新词族唯一命中是评分权重配置（语义排除） |

## 摘要

「模型预测准确率」是优化决策模型面板「模型自动迭代」Tab 的训练历史读数位：折线三线之一（`OptimizeDecisionPanel.jsx:133`）+ 训练记录表 accuracy 列（:133），由「触发自动迭代」按钮（:149）经 runAutoTrain 生成新记录。UI 现状是三层纯模拟：mockData 写死三条历史（92.8/90.1/88.4）、runAutoTrain 用 Math.random 增益公式造新值、文件头自注真源待 algo 训练管线。数据侧判定：**完全不支持**——准确率的计算原料是分类模型的预测落盘与 ground truth 标注对，而 UI 场景（金融欺诈/信用违约风控预警，mockData.js:591-596）在科技图谱域三源均无立项：dev 无模型面、gkx 无风险分类场景、久新 ADS 结果面为图/合作/人才域。姊妹件 010（召回率）同面板同数据流同判——两件共享完全相同的负证据结构，仅读数列不同；F1 为两者的调和平均（UI 已内联公式），原料齐则自动可算。

- 需求判定：**需求明列叶**（seq 453「图分析结果能直接与业务流程系统对接…风控策略动态调整」——决策联动能力位），指标语义清晰但三源无承载。
- 复现状态：脚本已跑通；三源词族扫描+语义排除实录全落产物（负证据）。
- 档位结论：**完全不支持**（negative_evidence，探针三件套在案）。
- 关键事实：即使最宽松的「人工评估折算」口径也无原料——三源连一条模型预测记录都没有（不只是没有标注）。
- 升档路径：algo 训练管线立项（预测落盘表+复核标注表）→ 可算；本次探针未发现任何可转换路径。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技知识图谱/服务展示/图分析集成/图分析与业务决策联动（1.1.1.1.5.3.2.4；SRS seq 453、excel_row 456）。UI 实际挂载：`OptimizeDecisionPanel.jsx` 决策反馈闭环区——`:123-138` trainPerfOption（折线 legend=['准确率','召回率','F1']，x 轴=最近 5 条训练时间，y 轴 80-100），本件为准确率线（`:134`）；`:140-160` trainColumns 训练历史表含 `:133`「准确率」列（dataIndex=accuracy，render `${v}%`）；`:148-152` 「触发自动迭代」按钮调 runAutoTrain(trainHistory, algorithm, perf) 生成新记录入折线与表。数据源：mockData.js:585-589 `decisionTrainHistory` 三条（tr-1 hybrid_rule accuracy 92.8 deployed、tr-2 temporal_gcn 90.1 archived、tr-3 graphsage 88.4 archived）。

### 1.2 为什么需要本指标

「模型自动迭代」回答的是决策模型的可信度问题：图分析触发风控动作（预警/拦截/审批流转）之前，业务方必须知道模型整体判对多少——准确率是总体判对率的核心读数（误报过多=正常客户被扰、漏报过多=欺诈漏网，准确率+召回率+F1 三线同看才能定位失衡方向）。UI 把它放进训练历史折线（近 5 次趋势）+表格（逐批次），配合「触发自动迭代」按钮展示「样本滚动训练→指标爬升」的闭环叙事。mockData note 侧写用途：「Q1样本重训，准确率+3.2%」——重训收益的运营语言。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**seq 453 只给能力位（「分析结果可触发自动预警、智能审批流转、精准推送或风控策略动态调整」），「准确率」的字面语义由 ML 通用标准闭合（(TP+TN)/全体)，UI 常量（% 单位、y 轴 80-100、mock 88-93 区间）与之自洽。定义本身无悬念——缺口全在数据侧：预测记录与标注对在三源均不存在（§〇 absence_probe）。

### 1.4 类似指标权威方法可行性分析概要

分类模型评估有成熟标准。其一，机器学习评估权威教材（R1 Zhou 的《Machine Learning》）：准确率=(TP+TN)/(TP+TN+FP+FN)，需预测-标注对；其二，scikit-learn 文档（R2）：`accuracy_score` 实现及「ground truth 必需」前提；其三，工业 ML 流程标准（R3 Google ML best practices）：评估数据集须独立于训练集、含人工复核标注。方法族对照：

| 方法族 | 代表 | 本库承载 | 贴合度 |
|---|---|---|---|
| 混淆矩阵（R1） | Zhou ML 教材 | **无预测/标注对** | 方法可行、数据无承载 |
| accuracy_score（R2） | scikit-learn | 同上 | 同上 |
| 独立评估集+人工标注（R3） | Google ML 指南 | 无标注流程 | 同上 |

结论：方法侧零悬念（混淆矩阵计数），数据侧三源连最低原料（一条预测记录）都没有——方法文献只佐证定义清晰，不能改变无承载判定。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/tech-knowledge-graph/OptimizeDecisionPanel.jsx:123-138`（折线）、`:140-160`（表+按钮）；`decisionModel.js:1-4`（自注）、`:21-44`（runAutoTrain 模拟公式）；`mockData.js:585-589`（三条历史）、`:591-596`（风险场景）。
- SRS：`gkx-orchestration/agent-delivery/bid-reference/srs/02-科技信息展示系统/科技知识图谱/服务展示.md` seq 453（excel_row 456），原文见附录 A。
- 权威方法：R1 Zhou ML 教材；R2 scikit-learn accuracy_score；R3 Google ML best practices。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**推测定义（UI 常量+ML 标准闭合）**：$\text{accuracy} = \frac{TP+TN}{TP+TN+FP+FN}$——模型自动迭代场景下，最近一次训练批次在评估集上的准确率，% 读数；UI 增益模拟公式 `min(97, base + boost*(0.3+rand*0.8))` 只是演示层。**数据侧最低可行口径**（若训练管线立项）：逐预测记录（decision_id, predicted_label, score）× 复核标注（result 含「有效/误判」）→ 混淆矩阵 → accuracy。

**降档/升档触发器（B10 模板）**：①现状三源无预测/标注面 → 完全不支持（本件判定）；②algo 训练管线立项+预测落盘（不含人工标注）→ 升**部分支持**（有预测无真值，只可算覆盖率类代理指标，非真准确率）；③+复核标注面（decisionFeedbackItems 的 result 字段形态：有效拦截/确认违约/误判）→ 升**完全转换支持**（混淆矩阵可算）。真准确率必须走②+③——训练管线与标注流程都是新立项，不是现有库表能转换的。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技知识图谱/服务展示.md` |
| 所属 L4 | 图分析集成（seq 449-454，6 叶） |
| 本件 | seq 453 图分析与业务决策联动的训练历史读数位之一 |
| 同面板件 | KGANALY_010（召回率，`:134`——姊妹件同判共证据）；KGANALY_015（反馈均分，`:379`） |
| UI 容器 | `OptimizeDecisionPanel.jsx`（优化决策模型面板） |

训练历史三读数（准确率/召回率/F1）同挂一个表同一份数据流——010 与本件共享「无预测+标注对」的负证据（本件探针即两件共用证据）；F1 是准确率与召回率的调和平均（UI 公式 `2*a*r/(a+r)` 已内联），两原料齐则自动可算，不单独派件。反馈闭环件 015 的复核数据（rating）是升档路径③的标注面雏形——但现状 mock 四条也是写死，无真承载。

## 二、计算过程

> 本件为完全不支持档，计算过程**从缺**。探测证据（三源词族+语义排除）进本节与 §四。

### 2.1-2.6 从缺（完全不支持档——§〇 定义）

计算过程从缺：三源无预测记录与标注对，混淆矩阵无从谈起。以下为**否定性证据的实测过程**（非计算过程）：

- **dev（开发库）**：542 表词族扫描（train/model/eval/predict）0 命中训练评估面；`gkxlumenx_topic_enterprise.evaluation_template` 词面命中但为企业评估**模板配置**（UI 配置面，非模型训练/评估记录）——语义排除。
- **gkx（要素库）**：280 表词族扫描（label/model/train/fraud/risk_eval）**0 命中**——专利/学者/合作要素域无风险分类场景、无预测记录、无 ground truth 标注。
- **久新（ADS 结果面）**：218 表词族扫描（feedback/model/train/label/fraud/risk/eval/blacklist）唯一命中 `ads_talent_capability_model`——SHOW CREATE TABLE 实查：人员能力综合评分**权重配置**表（model_version/model_name + research_perseverance_weight 等 9 个权重与阈值列 + window_start/end_year），无 accuracy/recall/预测记录/标注列，语义排除；blacklist/trigger 词族 0 命中（无黑名单/触发落盘，误报复核反馈环 rating 亦无承载）。
- **UI 模拟链实测**（非计算过程，公式形态复现）：`decisionModel.js:21-28` boost 按算法 1.2（hybrid_rule）/0.9（gat）/0.7（其他）；复现脚本 `sim_next('hybrid_rule', 92.8, 88.5, 45)`（rand 取中点）= accuracy 93.6 / recall 89.2 / f1 91.3 / latency 46ms——验证增益逻辑与上限（97/96）联动，**不是训练结果**。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_KGANALY_010_011.py`（010/011 共用）——三源只读探针（dev 词族/gkx 词族/久新词族+SHOW CREATE TABLE 语义排除）+ UI 模拟公式形态复现，零 `demo_*`；运行 `python3 code/M_SCIUI_KGANALY_010_011.py`（约 1 秒）。
- 产物：`code/M_SCIUI_KGANALY_011_out.json`，关键负证据——`facts.gkx_model_label_word_tables`（空表）、`facts.jiuxin_label_word_tables`（仅 ads_talent_capability_model）、`facts.jiuxin_capability_model_semantic_exclusion`（权重配置语义排除实录）、`facts.jiuxin_blacklist_word_tables`（空表）、`absence_probe` 三件、`derived[1]`（模拟公式复现）、`support_judgment="完全不支持"`。
- 结果解读：三源词族核查形成完整负证据链——准确率的计算原料（预测+标注对）在三源任何一库都不存在，且唯一词面命中均经语义排除（配置面≠记录面）。UI 面板照常渲染的 92.8% 是写死演示值，不因页面存在而改变数据面判定。
- 对照需求功能要求的评审：seq 453 的决策联动能力位中「模型自动迭代」读数在数据侧完全落空；需训练管线+标注流程立项才可交付。

### 2.8 分步证据对照表

| # | MD 论断（出处） | 产物键 | 读数 | 一致 |
|---|---|---|---|---|
| 1 | UI 折线 legend 三线（§1.1） | `facts.ui_mount_011` | :128 legend 含准确率 | ✓ |
| 2 | 表列准确率 dataIndex=accuracy（§1.1） | `facts.ui_mount_011` | :133 | ✓ |
| 3 | 按钮触发 runAutoTrain（§1.1） | `facts.ui_mount_011` | :149 | ✓ |
| 4 | mock 三条 accuracy 92.8/90.1/88.4（§〇/摘要） | `facts.ui_mock_train_history` | 92.8/90.1/88.4 | ✓ |
| 5 | 模拟公式自注「真源待 algo 训练管线」（§〇/§1.1） | `facts.ui_sim_source` | decisionModel.js:1-4 | ✓ |
| 6 | 场景=金融欺诈/信用违约（§1.2/§4.2） | `facts.ui_risk_scenario_note` | mockData.js:591-596 | ✓ |
| 7 | dev 词族 0 命中（§2.1） | `absence_probe[0]` | evaluation_template 语义排除 | ✓ |
| 8 | gkx 词族 0 命中（§〇/§2.1） | `facts.gkx_model_label_word_tables` | [] | ✓ |
| 9 | 久新唯一命中被语义排除（§〇/§2.1） | `facts.jiuxin_capability_model_semantic_exclusion` | 权重配置表 | ✓ |
| 10 | blacklist 词族 0 命中（§2.1） | `facts.jiuxin_blacklist_word_tables` | [] | ✓ |
| 11 | gkx 280 表（§2.1） | `facts.gkx_table_count` | 280 | ✓ |
| 12 | 久新 218 表（§2.1） | `facts.jiuxin_table_count_live` | 218 | ✓ |
| 13 | 模拟公式复现 93.6/89.2（§2.1） | `derived[2].derived` | sim_next 实算 | ✓ |
| 14 | 判档完全不支持（§〇/摘要） | `support_judgment` | 完全不支持 | ✓ |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 模型预测记录面（decision_id/predicted_label/score） | 三源 | 词族扫描（predict/train/model） | — | **不存在** | **缺**（主判定维） |
| D2 | ground truth 标注面（复核结果：有效/误判） | 三源 | 词族扫描（feedback/label/blacklist） | — | **不存在** | 缺 |
| D3 | 训练批次记录面（train_history） | 三源 | 词族扫描（train） | — | **不存在** | 缺 |
| D4 | 词面近邻表（配置面） | dev | `evaluation_template` | 配置面 | 不可用 | 语义排除 |
| D5 | 词面近邻表（配置面） | 久新 | `ads_talent_capability_model` | 权重配置 | 不可用 | 语义排除（SHOW CREATE 实查） |

`support_judgment="完全不支持"`（`verdict_kind="negative_evidence"`）、产物与文首一致。

### 3.2 词面命中语义排除细节

三源词族扫描唯一两个词面命中都是**配置面而非记录面**：dev `evaluation_template`（企业评估模板——评估的是企业资质不是模型）；久新 `ads_talent_capability_model`（model_version 列名带 model，但整表是人员能力评分的权重/阈值参数——「模型」指评分公式版本，非机器学习模型）。语义排除的判据：准确率需要**逐样本预测-标注对**，配置面只有参数没有样本，结构上就不可能承载。

### 3.3 现场复核清单

| 复核项 | 结果 |
|---|---|
| dev/gkx/久新词族 GROUP BY | 0/0/1（久新 1 命中已排除） |
| ads_talent_capability_model SHOW CREATE | 9 权重/阈值列，无评估列 ✓ |
| mock 三条与 mockData.js 逐值核对 | 一致 ✓ |
| sim_next 公式复现 assert | 93.6/89.2 通过 ✓ |
| 脚本形态 | 三源只读；零 demo_* |

## 四、数据缺失情况

### 4.1 预测+标注对全缺（结构级，主因）

准确率的分子分母（全体评估样本判对数/总数）三源不存在（`absence_probe` 三件——D1/D2/D3 全为「表不存在」级缺失）。修复只有一条正路：**algo 训练管线立项**——预测落盘表（decision_id/predicted_label/score/time）+ 复核标注表（decision_id/result/rating，形态可仿 decisionFeedbackItems）。这是新数据源工程，非现有库表转换可得。折中路径不存在：无预测记录则连代理指标（覆盖率类）都无处算起。

### 4.2 UI 面板的连带影响

训练历史三读数（011 本件/010 召回率/F1 内联）+ 反馈闭环件 015 同挂优化决策面板同吃一条数据流——本件负证据对 010 直接适用（同结构同判，姊妹件共证据）；F1 由 010/011 原料调和平均自动可算（不单独派件）；015 的反馈 rating 面（词族 feedback 0 命中）同判可预期。面板整体在数据侧落空，UI 现状 mock 三条+Math.random 是唯一「数据源」。建议：面板先标注「演示」，待训练管线立项后逐读数点亮。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| algo 训练管线立项（预测落盘+标注流程） | **新数据源** | 本件 + 010 + F1 + 015 | 唯一满足准确率/召回率语义的路径 |
| 预测落盘先行（无标注） | 数据工程 | 本件 + 010 | 升部分支持（仅代理指标） |
| 面板标注「演示」 | 前端 | 三读数 + 015 | 防误导 |

档位后果：训练管线+标注 → 完全转换支持；仅预测落盘 → 部分支持；现状 → 完全不支持。

## 参考文献

1. Zhou Z-H. Machine Learning[M]. Singapore: Springer, 2021. https://link.springer.com/book/10.1007/978-981-15-1967-3 （R1，2026-11-02 核验可达——准确率 (TP+TN)/全体 与混淆矩阵的标准定义出处，本件语义的方法学依据）
2. scikit-learn accuracy_score 文档[EB/OL]. scikit-learn. https://scikit-learn.org/stable/modules/model_evaluation.html#accuracy-metric （R2，2026-11-02 核验可达——工业实现参照，明确 ground truth 必需前提）
3. Google Machine Learning Best Practices / ML Crash Course — Evaluation[EB/OL]. Google. https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall （R3，2026-11-02 核验可达——评估集独立+人工标注的流程标准）

（注：本件为完全不支持档，参考文献仅佐证指标定义的方法学出处（§1.4 方法族），不构成计算过程依据。）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技知识图谱/服务展示.md》 seq 453（excel_row 456）：

> ### 图分析与业务决策联动 · 序号 453
> #### 需规功能描述
> 图分析结果能直接与业务流程系统对接。例如，分析结果可触发自动预警、智能审批流转、精准推送或风控策略动态调整。将分析洞察落地至具体操作，使数据分析赋能实际业务、加速创新与风险防控智能化。

（「模型预测准确率」名称为 UI 训练历史列命名（`OptimizeDecisionPanel.jsx:133`）；需求句「风控策略动态调整」「智能决策」即本件能力位原文映射——模型迭代质量读数。）

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 准确率/模型/迭代 | 全 SRS 目录 | 0（UI 层命名） |
| 风控策略动态调整/智能决策 | SRS 服务展示.md seq 453 | 1 |
| accuracy | UI OptimizeDecisionPanel.jsx | :128/:133/:149 |
| train/model/eval/predict | dev 542 表词族 | 0 命中（evaluation_template 语义排除） |
| label/model/train/fraud/risk_eval | gkx 280 表词族 | 0 命中 |
| feedback/model/train/label/fraud/risk/eval/blacklist | 久新 218 表词族 | 1 命中（ads_talent_capability_model，语义排除） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_KGANALY_011_out.json`（2026-11-02 实探：三源词族负证据链+语义排除实录）。
- 共享探针：`code/_snapshots/_probe_s306_l1_out.json`（S3-06 族级：三库表清单+词族计数）。

### B.2 本件产物逐键清单

| 产物键 | 类型 | 值/形态 | 正文引用 |
|---|---|---|---|
| `facts.ui_mount_011` | UI 挂载 | :128/:133/:149 | §1.1/摘要 |
| `facts.ui_mock_train_history` | mock 数据 | 三条（92.8/90.1/88.4） | §〇/摘要 |
| `facts.ui_sim_source` | 模拟源 | decisionModel.js:21-44 | §〇/§1.1 |
| `facts.ui_risk_scenario_note` | 场景 | 欺诈/违约风控 | §1.2/§4.2 |
| `facts.gkx_model_label_word_tables` | 负证据 | [] | §2.1 |
| `facts.jiuxin_label_word_tables` | 负证据 | [ads_talent_capability_model] | §2.1 |
| `facts.jiuxin_capability_model_semantic_exclusion` | 语义排除 | SHOW CREATE 实查 | §2.1/§3.2 |
| `facts.jiuxin_blacklist_word_tables` | 负证据 | [] | §2.1 |
| `derived[0-2]` | 公式/复现 | accuracy 定义+模拟复现 | §2.1 |
| `absence_probe` | 探针 | 三件 | §3.1/§4.1 |
| `support_judgment` | 判档 | 完全不支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 数据要求 | 本库承载 |
|---|---|---|---|
| 混淆矩阵（R1） | Zhou ML 教材 | 预测+标注对 | **无** |
| accuracy_score（R2） | scikit-learn | 同上 | **无** |
| 独立评估集（R3） | Google ML 指南 | 评估集+人工标注 | **无** |

### C.2 数据矩阵

| 依赖 | dev | gkx | jiuxin |
|---|---|---|---|
| 预测记录 | 无 | 无 | 无 |
| 标注对 | 无 | 无 | 无 |
| 训练批次记录 | 无 | 无 | 无 |
| 词面命中 | 配置面（排除） | — | 配置面（排除） |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v0（现状） | mock 三条+Math.random 模拟 | — |
| v1 | 代理指标（覆盖率类） | 预测落盘（升部分支持） |
| v2 | 真准确率 | +标注流程（升完全转换支持） |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 模拟值被误当真实准确率 | **高** | §2.1 B9/B10 披露（公式复现仅供形态验证） |
| 配置面词面命中被误判承载 | 中 | §3.2 语义排除实录（SHOW CREATE） |

### C.5 总判

**完全不支持**（negative_evidence）：三源无预测记录、无标注对、无训练批次面——修复须新数据源立项（训练管线+标注流程），非转换可得。姊妹件 010 同判。

## 附录 D 复现与对照清单

| 项 | 命令/路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_KGANALY_010_011.py` | 退出码 0，落双 `_out.json`（约 1 秒） |
| 词族复核 | 三源 GROUP BY | 0/0/1（久新 1 命中已排除） |
| 语义排除复核 | SHOW CREATE TABLE ads_talent_capability_model | 9 权重/阈值列，无评估列 |
| §二 从缺 | 完全不支持档 | 从缺（§2.1 为否定性证据实录） |
