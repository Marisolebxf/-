# 算法模型准确率（M_SCIUI_KGANALY_042）

> **类型**：无业务逻辑数值类（模型运营 KPI，读数型）｜ **域**：科技信息展示系统·科技知识图谱·指标展示·模型质量总览｜ **UI 挂载**：指标展示页 KPI 行第三卡 → `IndicatorDisplay.jsx:103` Statistic title="模型准确率" value={92.8} suffix="%"（绿色，源头是 `OptimizeDecisionPanel.jsx:53` perf 态常量 accuracy=92.8，`decisionModel.js runAutoTrain` mock 随机演化）
> **数据支持度**：**完全不支持**（模型预测明细与人工标注面三源均无——准确率的分子分母无来源；dev `cfg_model_registry` 25 行全 `is_mock: true` 无评估值；gkx/久新模型词族 0/2 张且非训练评估语义）｜ **公式定义人**：UI 前端 mock（`decisionModel.js:21-28`：`accuracy=min(97, base+boost×(0.3+rand×0.8))`——纯演示随机数，非真训练）｜ **口径归属**：UI 拆件叶（SRS seq 420 模型自动迭代「准确率持续提升」的功能组成维），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_KGANALY_042_043_044_045_probe.py`（四件合探）｜ **产物**：`code/M_SCIUI_KGANALY_042_out.json`（三源模型/告警/标注词族全量探针）
> **四判定摘要**：直接结构 = 无（三源无模型预测结果面）；直接数据 = 无；依赖结构 = 无（模型版本台账 dev 有 25 行但全 mock 标记；训练流水/预测明细/评估集三件套全缺）；依赖数据 = 无（评估所需「预测-标注」配对数据零立项）
> **数据源口径**：三源（dev live `gkxlumenx_*` + 三方库 gkx + 久新 `gkx_technology_analysis_dev` live）逐一探针留证；`demo_*` 禁引（dev `cfg_model_registry` 内 `is_mock: true` 字段是同向证据）。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全不支持。**「模型准确率」= 正确预测数 / 总预测数，需要**模型预测明细 + 人工标注（ground truth）**两翼数据。三源逐一探针（`absence_probe` 六件）：①dev 模型词族 6 张——`cfg_model_registry` 25 行是模型注册台账（model_id/version/invoke_path），**无一行含准确率评估值**，且全 25 行 `ext.is_mock: true`（版本号带 `-demo` 后缀）；`impact_prediction`/`industry_chain_model_run`/`industry_chain_model_result_detail`/`policy_prediction_indicator` 全 0 行；②gkx 280 表模型/告警/标注词族 0 命中；③久新 live 218 表（当日实测）模型词族 2 张——`ads_research_problem_deployment`（406 行，LLM 部署建议书，review_status 全 AUTO_APPROVED_LLM 无人工标注语义）与 `ads_talent_capability_model`（1 行，能力模型权重配置单）——均非训练评估面；④告警/标注词族三源命中皆非语义（qrtz 调度触发器/审计日志）；⑤dev 图谱结构面 26 张全 0 行——图谱侧模型特征训练无起点。**两翼皆缺**，指标无法构建。

### 批次通用纪律摘要（S3-06 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键 |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 准确率分子分母（预测-标注配对）同池——两翼皆缺无从谈起，判档性披露 |
| B4 | 负结论带探针 | absence_probe 六件（三源×模型/告警/标注+图表空壳） |
| B5 | 确定性 | 词族扫描 sorted()；无迭代计算 |
| B6 | 闸门自身被闸 | 不自跑闸门 |
| B7 | 产物只由脚本产出 | 合探脚本一次产出四件 _out.json |
| B8 | 回执不复收 | 词族 SQL 幂等可复验 |
| B9 | 单位/日期陷阱 | %无量纲；cfg_model_registry 25 行逐行核对 is_mock |
| B10 | 口径裁定保守交付 | 完全不支持档+升档触发器写死（§1.6） |
| B11 | 多本账互推 | 久新表数当日实测 218（与族快照 215 差异=活库自然增长，不写死） |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有模型预测结果面吗？ | 无 | dev 6 张（4 张 0 行+台账无值）/gkx 0/久新 2 张非评估语义 |
| 有人工标注（ground truth）吗？ | 无 | 标注词族三源仅审计日志（cms_op_audit 476 行操作审计非预测标注） |
| 能用别的东西拼出准确率吗？ | 不能 | 无预测明细即无分母，无标注即无分子——非近似可代 |

## 摘要

「算法模型准确率」是知识图谱指标展示页的四张总览 KPI 之一（92.8% 绿色读数，mock 常量），语义源头是优化决策模型面板的模型性能态（`decisionModel.js runAutoTrain` 用随机数演化 accuracy——纯前端演示）。数据侧判定：**完全不支持**——准确率需要「模型预测明细+人工标注」两翼数据，三源探针六件全负：dev 模型注册台账 25 行全部 `is_mock: true` 且无评估值列；预测类表 4 张全 0 行；gkx 词族 0 命中；久新模型词族 2 张均为部署建议/权重配置语义（无人工标注列，406 行 review_status 全 AUTO_APPROVED_LLM 是 LLM 自审批不是人工评估）；图谱结构面（模型特征的原料）26 张全空壳。mock 的 92.8% 是演示数字，三源无任何可支撑其真实性的数据面。

- 需求判定：UI 拆件叶（SRS seq 420 模型自动迭代的功能组成维——「准确率持续提升」无定义方法）。
- 复现状态：探针脚本已跑通；六件负证据落产物。
- 档位结论：**完全不支持**（两翼皆缺，非近似可代）。
- 关键事实：dev `cfg_model_registry` 25 行全 `is_mock: true`——模型运营面在 dev 侧也是演示配置；久新 `ads_research_problem_deployment.reviewer='LLM:deepseek-flash'` 全 406 行，LLM 自评不是人工标注。
- 升档路径：模型训练管线落预测明细表+人工标注闭环（seq 422 决策反馈闭环的真实数据化）→ 方可谈转换档。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统/科技知识图谱/指标展示页——`IndicatorDisplay.jsx` 顶部 KPI 行四卡（活跃告警数/融合指标数/模型准确率/已处理事件），本件是第三卡「模型准确率 92.8%」。页首还有三条告警 Alert（量子计算人才流动异常等 mock）。数据源头在优化决策模型面板：`OptimizeDecisionPanel.jsx:53-58` 初始化 perf 态 `{accuracy: 92.8, recall: 88.5, f1: 90.6, latencyMs: 45}`，「自动训练迭代」按钮触发 `decisionModel.js runAutoTrain`——`accuracy = min(97, base + boost×(0.3+rand×0.8))`，纯随机演化；KPI 卡的 92.8% 就是这个 mock 态的初始值。训练历史表（`decisionTrainHistory` mock）有三行历史（92.8/90.1/88.4%），同样无真源。

### 1.2 为什么需要本指标

模型质量总览位：管理者进指标展示页第一眼要回答「这套图谱决策模型靠谱吗」——准确率是最通用的质量语言。它与「活跃告警数」（本页第一卡，KGANALY_043）、「已处理事件」构成运营健康三读数。需求原文（seq 420 模型自动迭代）点名「使模型在风险判断、用户分类等任务上的准确率和鲁棒性持续提升」——准确率是模型迭代闭环的目标函数，KPI 卡是它的展示位。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**SRS《指标展示.md》seq 420 写「通过定期对历史数据样本进行机器学习教学，不断修正模型参数和结构，使模型在风险判断、用户分类等任务上的准确率和鲁棒性持续提升」——「准确率」作为目标被点名但无定义：哪个任务（风险判断？用户分类？）、什么口径（Top-1？阈值判定？）、评估集怎么圈（留出集？时间切分？）、谁标注（业务部门反馈=seq 422 闭环？）全部未言明。UI mock 的 92.8 与随机演化公式是演示占位。检索记录见附录 A.2。

### 1.4 类似指标权威方法可行性分析概要

模型准确率的权威方法是机器学习评估标准流程（R1 Hastie et al.《The Elements of Statistical Learning》：分类准确率=正确预测/测试集总量，须在留出集/交叉验证上评估，禁止用训练集自评；R2 scikit-learn `accuracy_score`：工程实现形态；R3 中国信通院《人工智能模型评估规范》类官方框架：模型评估的指标体系与数据集要求——测试集需与训练集分布一致且有人工确认标签）。方法本身零难度，**难点全在数据**：三源没有「预测明细+人工标注」任何一翼。方法族对照：

| 方法族 | 代表 | 本库承载 | 贴合度 |
|---|---|---|---|
| 留出集评估（R1） | ESL 标准流程 | **无预测明细** | 不可行 |
| 标准库（R2） | sklearn accuracy_score | 算法可用、无数据 | 空转 |
| 官方评估框架（R3） | 信通院规范 | 无评估数据集立项 | 远期 |
| 前端演示 | mock 92.8 | 随机演化 | 纯占位 |

结论：方法可行、数据零承载——「完全不支持」的成因是数据侧而非方法侧（F11：不轻易判不可能，但两翼皆缺时无从转换）。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/tech-knowledge-graph/IndicatorDisplay.jsx:100-105`（KPI 卡）、`:60-65`（alerts mock）；`OptimizeDecisionPanel.jsx:53-58`（perf 态）；`decisionModel.js:21-28`（runAutoTrain 随机演化）；`mockData.js:585-589`（decisionTrainHistory 三行 mock）。
- SRS：`gkx-orchestration/agent-delivery/bid-reference/srs/02-科技信息展示系统/科技知识图谱/指标展示.md` seq 420（excel_row 423，原文见附录 A）。
- 权威方法：R1 Hastie et al.；R2 scikit-learn；R3 信通院模型评估框架。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**推测定义（UI mock 未闭合，需求无公式）**：

$$\text{Accuracy} = \frac{\text{TP}+\text{TN}}{\text{TP}+\text{TN}+\text{FP}+\text{FN}} = \frac{\text{正确预测数}}{\text{评估集总预测数}}$$

评估集须人工标注（或业务闭环确认）且与训练集隔离。**待裁项**：任务定义（风险判断/用户分类——UI 两处语义并存）、评估集圈法、标签来源（seq 422 反馈闭环 vs 专项标注）。

**降档/升档触发器（B10 模板）**：①现状两翼皆缺 → **完全不支持**（本件判档）；②模型训练管线落「预测明细表」（model_version/entity_id/predicted_label/score/time）+「人工标注表」（entity_id/true_label/annotator）→ 可升**完全转换支持**（两表 JOIN 直算）；③标注闭环走 seq 422 业务反馈（有效拦截/误判等 result 字段数据化）→ 同②；④仅落预测明细无标注 → 最高**部分支持**（有分母无分子）。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技知识图谱/指标展示.md` |
| 所属 L5 | 优化决策模型（seq 418-422，5 叶）+ 指标展示页 KPI 行（UI 拆件） |
| 本件 | seq 420 模型自动迭代的功能组成维（准确率）；KPI 卡展示位 |
| 同族件 | KGANALY_043 活跃告警条数（同页第一卡）、KGANALY_044 漏检率、KGANALY_045 目标误报率（同面板 riskSummary/feedbackAdj）、KGANALY_010/011（召回率/预测准确率，L1 批件同 mock 源）、KGANALY_015 反馈均分（L1 批件） |
| 近域件 | seq 421 风险识别优化（「降低漏检与误判」=044/045 语义源）；seq 422 决策反馈闭环（标注数据化的远期载体） |
| UI 容器 | `IndicatorDisplay.jsx` KPI 行第三卡 |

本件与 010/011（召回率/预测准确率）同源 mock（perf 态）——「一态多卡」结构：perf 四值（accuracy/recall/f1/latencyMs）被两张页面五张卡消费。数据侧判定同构：一翼缺失则五卡同判。

## 二、计算过程

> 本件为完全不支持档：**计算过程从缺**。探测证据进第三章/第四章（skill §4.3 契约）。
> 三源探针由 `code/M_SCIUI_KGANALY_042_043_044_045_probe.py` 于 2026-11-02 执行，负证据六件落 `M_SCIUI_KGANALY_042_out.json`（absence_probe 键，与 043/044/045 共用同一次扫描）。

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 模型预测明细 | dev | impact_prediction/industry_chain_model_run/result_detail/policy_prediction_indicator | **0**（4 张全空） | 结构在 | **缺**（空壳） |
| D2 | 模型版本台账 | dev | `cfg_model_registry`（model_id/version/evaluation） | 25 | 直查 | 台账在、**无评估值**（全 is_mock） |
| D3 | gkx 模型面 | gkx | 模型词族 280 表扫描 | — | **0 命中** | **缺** |
| D4 | 久新模型面 | 久新 | ads_research_problem_deployment（406）/ads_talent_capability_model（1） | 407 | 直查 | 部署建议/权重配置语义，**非评估面** |
| D5 | 人工标注（ground truth） | 三源 | label/annotat/feedback 词族 | — | **0 语义命中** | **缺**（两翼之一不存在） |

`support_judgment="完全不支持"`、产物与文首一致。两跳止步说明：D5 标注维属 B 类（推断补充依赖，非需求明列独立指标）——按 skill §P2.1 情形 B 直接记无数据支持，不再二级拆解。

### 3.2 dev 模型面读数（cfg_model_registry 25 行语义排除）

25 行逐一核对（产物 `dev_model_word_tables`）：model_id 覆盖 ENT_BIZ_POWER/ENT_CENTRALITY/ENT_DIAGNOSIS 等 7 个直发模型+MDL_* 18 个注册模型；`evaluation` 列全是 baseline 方法名+report_ref 文档引用（如 `{"baseline": "pagerank_degree", "report_ref": "算法设计说明.md#第4章"}`）——**没有一行含 accuracy 数值**；`ext` 列 25 行全部 `is_mock: true`，版本号带 `-demo` 后缀（如 `demo_centrality_v0.1`）。结论：dev 模型注册面是「演示工程的配置清单」，其自身就声明了 mock 身份——不是准确率的承载面。预测类 4 张表 0 行：模型从未在 dev 跑过真预测。

### 3.3 久新模型面读数（语义排除）

`ads_research_problem_deployment`（406 行）：科研问题部署建议书——reviewer 全 406 行 `LLM:deepseek-flash`、review_status 全 `AUTO_APPROVED_LLM`、inference_provider=deepseek——这是 **LLM 推理输出面**（研究问题优先级评估），非模型训练评估面；且「LLM 自审批」不构成人工标注（B9 同向证据）。`ads_talent_capability_model`（1 行）：人才能力模型**权重配置单**（research_perseverance_weight 等权重列）——配置语义非结果语义。两表连「预测明细」都不算（无实体级预测行），更无标注配对。

### 3.4 gkx 与告警/标注词族读数

gkx 280 表模型/告警/标注三词族 0 命中（`gkx_model_word_tables: []` 等）——gkx 是数据明细库（专利/论文/机构），无模型运营面。dev 告警词族命中 7 张全是 quartz 调度触发器（qrtz_*_triggers，0 行）；标注词族命中 2 张：sys_audit_log（0 行）与 cms_op_audit（476 行 CMS 操作审计）——审计「谁改了什么内容」不是「预测对错标注」，语义排除。

### 3.5 现场复核清单

| 复核项 | 结果 |
|---|---|
| dev 模型词族 6 张 | cfg_model_registry 25（全 is_mock）+ 4 张 0 行 + model_registry 0 行 |
| dev evaluation 列 | 25 行全 baseline 方法名，无 accuracy 数值 |
| gkx 词族 | 模型/告警/标注 0/0/0 |
| 久新词族（218 表当日实测） | 模型 2 张（406+1，语义排除）/告警 0/标注 0 |
| 久新 deployment review_status | 406 行全 AUTO_APPROVED_LLM |
| 图谱结构面 | 26 张全 0 行（族级快照） |
| 脚本形态 | 三源只读词族扫描；零 demo_* |

## 四、数据缺失情况

### 4.1 两翼皆缺（结构级，判定性）

准确率的可构建性=「预测明细×人工标注」交集。三源现状：预测明细零立项（dev 4 张空壳+久新非实体级预测+gkx 无模型面）；人工标注零立项（词族仅审计日志，语义排除；seq 422 决策反馈闭环在 UI 是 mock List 无台账表）。**一翼缺尚可谈部分支持，两翼皆缺即完全不支持**——不存在能用现有数据拼出的近似口径（图谱结构统计与模型准确率无替代关系）。

### 4.2 dev 台账的 is_mock 自声明（披露级）

`cfg_model_registry` 25 行全 `is_mock: true` 是重要同向证据：模型运营面在 dev 侧是演示配置工程，其版本号（demo_centrality_v0.1 等）与 skill P4.1 造数甄别的「真骨架+假血肉」模式一致。若后续这些模型真跑（impl_status=implemented 的 MDL_* 行），预测明细表会有数据——那是升档触发器②的起点。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 预测明细表落库（model_version/entity/pred_label/score/time） | 数据工程（重） | 本件+044/045+010/011 | 分母侧 |
| 人工标注闭环（seq 422 数据化：反馈 result 字段→标注表） | 数据工程（重）+流程 | 本件+044/045+015 | 分子侧——业务部门每复核一条告警即一条标注 |
| 评估集圈法与任务定义 | 口径裁定 | 本件 | 任务/切分/标签三定义 |
| KPI 卡降级方案 | 前端工程（轻） | 本件 | 无真值期隐藏该卡或标「演示值」 |

档位后果：两翼落齐 → 完全转换支持（JOIN 直算）；仅预测明细 → 部分支持；维持现状 → 完全不支持。推荐：优先推动 seq 422 反馈闭环数据化（标注与 044/045/015 三件共受益）。

## 参考文献

1. Hastie T, Tibshirani R, Friedman J. The Elements of Statistical Learning: Data Mining, Inference, and Prediction[M]. 2nd ed. Springer, 2009. https://doi.org/10.1007/978-0-387-84858-7 （R1，2026-11-02 WebSearch 核验可达——分类准确率的标准评估流程（留出集/交叉验证），禁止训练集自评）
2. scikit-learn accuracy_score 文档[EB/OL]. scikit-learn. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html （R2，2026-11-02 WebSearch 核验可达——工程实现形态）
3. 人工智能模型评估方法与框架相关标准化研究（中国信息通信研究院）[EB/OL]. http://www.caict.ac.cn/kxyj/qwfb/bps/ （R3，2026-11-02 WebSearch 核验可达——中国官方模型评估框架体系，评估数据集要求）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技知识图谱/指标展示.md》seq 420（excel_row 423）：

> ### 模型自动迭代 · 序号 420
> #### 需规功能描述
> 支持自动化的模型训练与迭代优化。通过定期对历史数据样本进行机器学习教学，不断修正模型参数和结构，使模型在风险判断、用户分类等任务上的准确率和鲁棒性持续提升。此外，该功能还可以根据业务场景灵活切换和升级不同的模型算法，实现业务驱动下的智能进化。

（「模型准确率」未单列叶——本件为 UI 拆件：IndicatorDisplay KPI 卡+OptimizeDecisionPanel perf 态。）

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 模型准确率 | SRS 指标展示.md | 0（未单列叶；seq 420 提「准确率持续提升」） |
| 模型准确率 | UI IndicatorDisplay.jsx | :103（KPI 92.8%） |
| accuracy | UI decisionModel.js | :21-28（runAutoTrain 随机演化） |
| model/train/predict 词族 | 三源表名扫描 | dev 6 张（25 行台账+4 空）/gkx 0/久新 2 张非评估语义 |
| label/feedback 词族 | 三源表名扫描 | dev 2 张审计日志（语义排除）/gkx 0/久新 0 |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_KGANALY_042_out.json`（2026-11-02 三源词族探针，与 043/044/045 共用同一次扫描）。
- 共享探针：`code/_snapshots/_probe_s305_l3_call_out.json`（dev 图表面）。
- 探针脚本：`code/M_SCIUI_KGANALY_042_043_044_045_probe.py`。

### B.2 本件产物逐键清单（`code/M_SCIUI_KGANALY_042_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `facts.ui_mount` | 挂载 | IndicatorDisplay.jsx:103 | §〇/§1.1 |
| `facts.ui_algo_source` | mock 源 | decisionModel.js runAutoTrain | §〇/§1.1 |
| `facts.dev_model_word_tables` | 探针 | 6 张 | §3.1/§3.2 |
| `facts.dev_model_word_table_rows` | 计数 | 25/0×4/0 | §3.2 |
| `facts.dev_alert_word_table_rows` | 计数 | qrtz 7 张全 0 | §3.4 |
| `facts.dev_label_word_table_rows` | 计数 | 0/476（审计语义） | §3.4 |
| `facts.gkx_model/alert/label_word_tables` | 探针 | 0/0/0 | §3.4 |
| `facts.jiuxin_table_count_live` | 计数 | 218（当日实测） | §3.3 |
| `facts.jiuxin_model_word_tables` | 探针 | 2 张（406+1） | §3.3 |
| `facts.jiuxin_alert/label_word_tables` | 探针 | 0/0 | §3.4 |
| `absence_probe` | 负证据 | 六件 | §〇/§三/§4.1 |
| `support_judgment` | 判档 | 完全不支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 本库承载 | 贴合度 |
|---|---|---|---|
| 留出集评估 | R1 ESL | 无预测明细 | 不可行（数据侧） |
| 标准库 | R2 sklearn | 算法零门槛 | 空转 |
| 官方评估框架 | R3 信通院 | 无评估数据集 | 远期 |
| 前端演示 | mock 92.8 | 随机演化 | 纯占位 |

### C.2 数据矩阵

| 依赖 | dev | gkx | jiuxin |
|---|---|---|---|
| 模型预测明细 | 4 张 0 行 | 无 | 无（LLM 建议书非预测行） |
| 模型版本台账 | 25 行（全 is_mock） | 无 | 1 行权重配置 |
| 人工标注 | 审计日志（语义排除） | 无 | 无 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v0（现状） | mock 92.8% | — |
| v1 | 预测明细落库 | 模型真跑（impl_status=implemented 行激活） |
| v2 | 标注闭环（seq 422 数据化） | 业务流程 |
| v3 | 准确率直算+回填（升转换档） | v1+v2 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| mock 92.8% 被当真值引用 | 高 | KPI 卡标「演示值」或隐藏 |
| LLM 自审批被误当人工标注 | 中 | §3.3 语义披露 |
| 训练集自评（数据泄漏） | 中 | 升档后按 R1 留出集规范 |

### C.5 总判

**完全不支持**：两翼（预测明细/人工标注）三源零立项，dev 台账自声明 is_mock——判档性缺失而非口径性缺失。升档路径唯一（两翼落齐），已写触发器。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_KGANALY_042_043_044_045_probe.py` | 退出码 0，落四件 _out.json |
| 词族扫描 | `absence_probe` 六件 | dev 6/7/2 张、gkx 0、久新 2/0/0 |
| is_mock 核查 | `dev_model_word_tables`+cfg_model_registry 25 行 | 全 is_mock: true |
| §二 | 完全不支持档 | 从缺（负证据在 §三/§四） |
