# 政策当前评估得分（M_SCIUI_POLCMP_016）

> **类型**：需业务建模类（评估模型口径未闭合）｜ **域**：科技政策跟踪·政策分析评价·政策分析报告可视化呈现｜ **UI 挂载**：科技信息展示系统 → 政策跟踪 → 政策分析（评估指标雷达图）→ `PolicyAnalysis.jsx:357`（radar series `name:'当前评估'`，读 `policyData.js:446-452` `evaluationMetrics` 常量）
> **数据支持度**：**完全不支持**｜ **公式定义人**：仿王惠（推测定义，需求原文只给展示语境不给评分算法）｜ **口径归属**：父代理裁定 **NEW**——核增 PC-09「跨政策交叉对比」语境下的多维对比新语义；候选旧件 PG_COMPOSITE 是原方案「综合评估」，不同物，不可搬判档
> **复现脚本**：`code/M_SCIUI_POLCMP_016.py`｜ **产物**：`code/M_SCIUI_POLCMP_016_out.json`
> **四判定摘要**：直接结构 = 否（三源无政策评估结果面）；直接数据 = 否；依赖结构 = 部分（dev 五处承载结构全在：`policy_effect_eval` 22 列五维分/`policy_support_assessment` 27 列 composite_score/`policy_support_assessment_indicator` 21 列权重公式维表/ads `policy_effect`——均为「规划过落位」）；依赖数据 = 否（五处承载全 0 行）
> **数据源口径**：三源（开发库 live `gkxlumenx_*` 非 demo + 三方库 gkx + 久新 `gkx_technology_analysis_dev`）逐一探针留证；`demo_*` 禁引。

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全不支持。** 当前评估得分 = f(评估事件)。评估事件（何政策、何批次、何维、多少分）是评估模型运行时的产物——**结果面三源零承载**：gkx 280 表扫 eval/score/assess/rating/composite 五词族命中 0（gkx 是科技要素库，天然无评估面），政策文本「评估+得分」表述仅 5 行（政策原文叙述非评估结果）；dev 数据仓五处「结构在、数据全空」——`policy_effect_eval`（22 列，含 execution_effect/social_economic/environment_impact/innovation_promotion/industry_impact 五个分值列）、`policy_intensity_eval`（23 列）、`policy_support_assessment`（27 列，含 composite_score/composite_rank）、`policy_support_assessment_indicator`（21 列，含 indicator_weight/calculation_formula——权重公式维表）、`gkxlumenx_ads.policy_effect`（12 列，effect_score）——**全部 0 行**；久新 203 张 `ads_*` 表扫 policy×eval/score/assess 交叉 0 命中（解锁后实测；久新评估族是技术/问题/人才域，与政策评估不同物）。**双缺叠加**：数据缺（评估从未运行，五处落位表零写入）+ 口径缺（五维权重体系未立项——UI mock 权重 20/25/20/25/10 是演示值）。父代理裁定 NEW：本件语义为核增 PC-09 跨政策交叉对比语境下的当前评估快照，与旧件 M_POLICY_PG_COMPOSITE（综合评估）不同物，判档独立。

### 批次通用纪律摘要（S3-02 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | mock 结构披露比（7,670/100）注明非指标值 |
| B4 | 负结论带探针 | absence_probe 四件：gkx/dev/jiuxin/doc（§3.3） |
| B5 | 确定性 | 表名扫描词表固定、列清单按 ordinal 输出 |
| B6 | 闸门自身被闸 | 不自跑闸门，派单方统一 |
| B7 | 产物只由脚本产出 | 改脚本→重跑；产物零手改 |
| B8 | 回执不复收 | 探针 SQL 幂等可复验 |
| B9 | 单位/日期陷阱 | 评估无量纲运算；无日期运算 |
| B10 | 口径裁定保守交付 | 不写伪得分（登记键留空）；升档双触发器写死 |
| B11 | 多本账互推 | dev 政策族 5 表 0 行与 `_probe_lane6_s302_r2_out.json`/POLCMP_002/_008 产物零漂移；gkx 20,000 与共享快照一致 |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 评估结果面（政策×批次×维×分值）在三源有承载吗？ | 无（结构在数据空） | gkx 0 命中；dev 五承载 0 行；久新 0 命中（§3.3） |
| 评分口径（五维权重）闭合吗？ | 不闭合 | UI mock 权重 20/25/20/25/10 演示值；dev 权重维表 0 行；需求无算式（§1.3） |
| 有任何可算的替代读数吗？ | 无 | 政策文本「评估+得分」5 行是原文叙述；mock 加权 76.7 是演示重算（不参与结论） |

## 摘要

「政策当前评估得分」是政策分析页评估雷达图的系列名：`PolicyAnalysis.jsx:357` 的 radar series `name:'当前评估'` 五维值读 `policyData.js:446-452` `evaluationMetrics` 常量——覆盖广度 85/深度力度 78/协同程度 72/实施效果 68/创新引领 82，各带权重（20/25/20/25/10%）。「当前」是快照语态：区别于趋势分析（同比序列，POLCMP_019 件）与效果推演（多维评估，POLCMP_022 件），它回答「这项政策此刻评多少分」。需求侧三份真源均无该指标名，最近语境是主需求 1.1.1.1.4.2.2.1 政策分析报告可视化呈现（多维指标趋势图「组合选取评估指标，查看政策绩效」）+ 核增 PC-09 跨政策交叉对比（维度明列：核心指标/扶持力度/适用范围/实施路径，无评分算法）；父代理裁定其为核增多维对比新语义（NEW），旧综合评估（PG_COMPOSITE）不同物。数据侧双缺：dev 五处评估承载（含权重公式维表）结构完整但全部 0 行——评估体系「规划过、从未写入」；gkx/久新无政策评估面。且五维权重口径未立项（UI mock 权重是演示值）。判**完全不支持**。

- 需求判定：**named_in_srs = false**——三份需求真源无「当前评估得分」字样；语义源=UI mock 实现层（雷达图系列常量）。
- 复现状态：负结论登记键（`policy_current_eval_score=null`）+ 三源评估面探针落产物；mock 结构披露键（加权 76.7）标注不参与结论。
- 档位结论：**完全不支持**（评估结果面零数据 + 权重口径未立项，双缺）。
- 关键事实：dev `policy_support_assessment_indicator` 带 `indicator_weight`/`calculation_formula` 列——权重公式维表也规划过但 0 行，与 `policy_effect_eval` 五维分列共同构成「评估体系完整落位、从未运行」的标准样本。
- 升档路径：①评估模型立项（五维体系+权重表，可参照 T/CASTEM 1010-2023 打分范式）+ 首批评估批次运行写入 `policy_effect_eval` → 直查可算升完全直接支持；②若甲方裁定以核增 PC-07 关键指标结构化产物做规则打分 → 转换可算升完全转换支持（口径须公示）。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技政策跟踪/**政策分析评价·政策分析报告可视化呈现**（主需求 1.1.1.1.4.2.2.1）。UI 实际容器是政策分析页（`PolicyAnalysis.jsx`）的评估雷达图卡：`:357` 起 radar option 的 series 数据 `{ value: evaluationMetrics.map(item => item.value), name: '当前评估', areaStyle: {...} }`——五维多边形，「当前评估」是蓝色填充系列名。数据源 `policyData.js:446-452` `evaluationMetrics` 常量（key/label/value/weight 四字段五条）。同卡上方的指标说明区（`:1617` 附近）还给出五维权重展示。整条链路无 API 调用——五维值与权重全部为页内 mock 演示值。

### 1.2 为什么需要本指标

政策对比的业务问题是「凭啥说 A 政策比 B 政策好」：定性比对（条款并排）容易陷入各说各话，需要一个可横比的量化锚——当前评估得分就是这个锚。雷达五维（覆盖广度/深度力度/协同程度/实施效果/创新引领）把政策质量拆成五个可打分的面，「当前」快照保证对比同时性（同一评估批次下的政策 A/B/C 横比）。在核增 PC-09 跨政策交叉对比语境下，它是「核心指标」维的量化形态；在政策分析报告语境下，它是多维指标趋势图「组合选取评估指标，查看政策绩效」（主需求 :1331）的绩效读数基线。它的政务对应物是科技评估机构的事中/事后评估打分（T/CASTEM 1010-2023 规范的政策评估框架，R1）。

### 1.3 需求文档是否给出定义方法

**三份需求说明书均无「当前评估得分」字样。**最近的两处语境：主需求 :1325（1.1.1.1.4.2.2.1 政策分析报告可视化呈现）「通过多个维度对政策评估结果进行展示」「组合选取评估指标，查看政策绩效随变量变化的动态趋势」——**评估结果的展示语境在、评分算法无**；核增需求 :80（1.1.1.1.4.2.4.3.1 跨政策交叉对比）「支持多份政策文件在条款内容、核心指标、扶持力度、适用范围、实施路径等维度的交叉比对」——**对比维度明列、评分体系无**。SRS 政策分析评价对应叶同文转述主需求。语义源=UI mock 实现层（evaluationMetrics 常量 + radar 系列名）。

### 1.4 类似指标权威方法可行性分析概要

「政策评估得分」的权威方法锚是政策评估标准体系：

| 方法族 | 代表 | 评分结构 | 数据要求 | 与本库匹配 |
|---|---|---|---|---|
| 科技创新政策评估规范 | T/CASTEM 1010-2023（R1，科技部评估中心起草） | 多维框架（价值/过程/绩效）×指标体系×前后对比 | 评估批次运行结果 | **无承载** |
| 政策工具量化评估 | 文本共词/LDA 政策工具分类（R2） | 政策工具维度计分 | 政策文本（有）+评分规则 | 文本在、规则未立项 |
| 国际政策评估 | OECD evaluation（R3） | 相关性/有效性/效率/影响四问 | 评估证据链 | **无承载** |
| 前端演示模型 | UI evaluationMetrics | 五维×权重加权百分制 | mock 常量 | 结构披露（不作源） |

方法链条的共同前置是**评估运行时结果**（政策×批次×维×分值）——T/CASTEM 规范给出的是评估框架（怎么组织评估），打分仍要评估活动真实发生。本库 dev 五处承载正是为这类评估活动预留的落位，但 0 行。完整版见附录 C。

### 1.5 引用来源

- UI：`repos/demo-ui-science/src/pages/policy-tracking/PolicyAnalysis.jsx:357`（radar series name:'当前评估'）、`:1617`（权重展示区）；`repos/demo-ui-science/src/pages/policy-tracking/policyData.js:446-452`（evaluationMetrics 常量）。
- 主需求：`科技信息展示系统和科技专题服务系统.md` :1325/:1327-1331（1.1.1.1.4.2.2.1 政策分析报告可视化呈现——「组合选取评估指标，查看政策绩效」语境）。
- 核增需求：`科技信息展示系统(政策对比功能升级)核增需求.md` :78-80（1.1.1.1.4.2.4.3.1 跨政策交叉对比——PC-09 五维比对语境）、:134（PC-09 叶表）。
- 权威方法：R1 T/CASTEM 1010-2023 科技创新政策评估规范（国家标准馆著录页）；R2 政策文本量化评估（POLPAN_005 件已核验文献族）；R3 OECD policy evaluation。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**推测定义**：

$$S_{current} = \sum_{d=1}^{5} w_d \cdot s_d,\quad \sum w_d = 100,\quad s_d \in [0,100]$$

即五维（覆盖广度/深度力度/协同程度/实施效果/创新引领）加权百分制——UI mock 权重结构（20/25/20/25/10）暗示该口径，按该结构演示值重算加权分 = 85×0.20+78×0.25+72×0.20+68×0.25+82×0.10 = **76.7**（产物登记键 `ui_mock_weighted_score_reference`，mock 结构披露，不参与支持度结论）。两个口径分歧点待裁定：**A 维度集**——UI 五维（覆盖/深度/协同/实施/创新）vs dev `policy_effect_eval` 五维分列（执行/社会经济/环境/创新促进/产业影响）——两套五维结构同构不同名（§3.2），以哪套为准须立项定版；**B 权重来源**——专家德尔菲（主观）vs 政策文本规则打分（客观代理）vs 等权（保守）。两分歧当前均无依据可裁——权重维表（dev `policy_support_assessment_indicator.indicator_weight`）0 行，评估活动从未发生。

**降档/升档触发器**：①评估模型立项（五维体系定版+权重表——可参照 T/CASTEM 1010-2023 或科技部创新积分制打分范式）+ 首批政策评估批次运行写入 `policy_effect_eval` → 直查可算，升**完全直接支持**；②若甲方裁定以核增 PC-07「关键指标自动提取」的结构化指标做规则打分（政策文本侧特征分）→ 转换可算，升**完全转换支持**（口径须公示，维度集分歧 A 随之消解）。降档无空间（已到底档）。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 挂靠四级功能（export 口径） | 多维政策对比族（核增 PC-09 语境）；UI 实挂政策分析评价 |
| UI 实际容器 | `PolicyAnalysis.jsx` 评估雷达图（政策分析页） |
| 语义源叶 | 无直接需求叶——主需求 :1325/:1331 展示语境 + 核增 :80 对比维度语境 |
| 旧件关系 | **父代理裁定 NEW**：候选 PG_COMPOSITE（原方案综合评估）不同物不可搬判档；政策族旧 MD 无当前评估快照语义件 |
| 批内姊妹件 | **POLCMP_022 多维度效果评估（同评估族姊妹——共享 dev `policy_effect_eval` 结构证据）**；POLCMP_019 同比增长率（同页趋势侧）；POLCMP_007 创新指数提升（同推演语境指数侧） |
| 依赖链 | 评估批次 ← 评估模型立项（无）→ 运行写入 `policy_effect_eval`（无） |

## 二、计算过程

> 本件为完全不支持件：评估结果数据从缺，本区不构造任何伪得分——按契约仅作方法面与证据面陈述。

### 2.1 方法选择（文献依据）

若评估面闭合，方法选**多维加权百分制（T/CASTEM 1010-2023 范式的运维简化版）**：五维指标体系 + 权重表（德尔菲定权或文本规则代理）+ 评估批次运行打分。选择理由：其一，T/CASTEM 规范（科技部评估中心起草，R1）给出的就是「评估框架×指标体系×方法（前后对比/成本效益/专家评议）×程序」全链条，运维化落地即批次打分；其二，dev `policy_effect_eval` 的列结构（eval_batch_no 评估批次 + 五个分值列 + dimension_results JSON + eval_model_version 模型版本）与该方法一一对应——落位表就是按这个范式设计的；其三，UI 雷达五维×权重的展示结构与加权合成口径天然对齐。但该方法当前**不可执行**——评估从未运行，五处落位 0 行。

### 2.2 gkx 评估面排除

gkx 280 表扫 eval/score/assess/rating/composite 五词族——0 命中（`gkx_eval_like_tables=[]`）。gkx 是科技要素库（论文/专利/机构/政策/宏观），数据面来自公开科技统计与文献库采集，天然无评估活动数据。文本面旁证：政策文本「评估+得分」拼串表述仅 5 行（`gkx_policy_eval_score_text_rows=5`）——通读为政策原文叙述（如「开展评估工作」「第三方评估」字样），不是评估结果数据。

### 2.3 dev 五处承载定性与结构证据（本件核心证据）

dev `gkxlumenx_dwd`/`gkxlumenx_ads` 五处评估承载，结构全在、数据全空（产物 `dev_policy_eval_carriers` 全列清单）：

| 承载 | 列数 | 关键列 | 行数 | 语义定性 |
|---|---|---|---|---|
| `policy_effect_eval` | 22 | `eval_batch_no`/五分值列/`dimension_results` JSON/`eval_model_version`/`exec_status` | **0** | 效果评估批次结果（与 UI 雷达五维结构同构不同名） |
| `policy_intensity_eval` | 23 | `intensity_index`/`effect_score`/`coverage_score`/`intensity_level`/`rank_nationwide` | **0** | 政策强度评估（含全国排名） |
| `policy_support_assessment` | 27 | `strategy_guidance_score`/`composite_score`/`composite_rank`/`delphi_result`/`simulation_prediction` | **0** | 支撑综合评估（含德尔菲与仿真预测槽位） |
| `policy_support_assessment_indicator` | 21 | `indicator_code`/`indicator_weight`/`calculation_formula`/`threshold_high/medium` | **0** | **指标权重维表**（含权重/公式/阈值列——评估体系的设计图落位） |
| `gkxlumenx_ads.policy_effect` | 12 | `scope_type`/`effect_score`/`shortboard_cnt`/`layout_rec_cnt`/`metric_id` | **0** | ads 层效果分镜像（服务 OLAP） |

五处共同构成「评估体系完整规划、从未运行写入」的标准样本（B4 情形②表在 0 行——补数据可解的结构空）。与 Lane6 探针（`_probe_lane6_s302_r2_out.json` rowcounts 组）逐表对账零漂移。

### 2.4 久新评估面排除与口径归属

**久新**：203 张 `ads_*` 表扫 policy×eval/score/assess 交叉——0 命中（`jiuxin_policy_eval_tables=[]`，解锁后实测）；policy 类仅 `ads_research_problem_policy_evidence`/`ads_technology_policy_evidence`/`ads_research_problem_policy_yearly_metrics`（问题→政策证据面 1,252 行 / 技术→政策证据面 0 行 / 问题×年政策计数切片 39 行——实测定性见 §2.4）。久新的评估族表（`ads_technology_potential_*`/`ads_region_*` 等技术域评估）是**技术/问题/人才域**评估，与政策评估不同物——不可搬。**口径归属**：父代理裁定登记簿 NEW——「政策当前评估得分」为核增 PC-09 多维度对比新语义（跨政策交叉对比语境下的当前评估快照），候选 PG_COMPOSITE 是旧「综合评估」，不同物；判档独立调查如上。

### 2.5 UI mock 边界披露

`PolicyAnalysis.jsx:357` 雷达五维全部读 `policyData.js:446-452` 页内常量：五维值 85/78/72/68/82 × 权重 20/25/20/25/10%——按 UI 自身权重结构重算加权分 76.7（产物 `ui_mock_weighted_score_reference=76.7`，分子 Σ(分值×权重)=7,670、分母权重和=100）。**此为 mock 结构披露**：它证明前端口径是「五维加权百分制」，不证明任何真实得分——演示值不参与支持度结论。同页 `:1617` 权重展示区把 20/25/20/25/10 显式画出来，说明前端作者把权重当作产品语义的一部分（而非随意数），权重体系待立项正是本件口径层缺口。

### 2.6 复现代码结果展示

- 代码：`code/M_SCIUI_POLCMP_016.py`（三源串行只读；gkx 经 `_gkxdb.py`；dev 直连含五承载 SHOW COLUMNS+COUNT；久新锁定按「未取证+旁证」登记、解锁后复跑）；运行 `python3 code/M_SCIUI_POLCMP_016.py`。
- 产物：`code/M_SCIUI_POLCMP_016_out.json`。正文数字与产物键对应：`gkx_eval_like_tables=[]` + `gkx_policy_eval_score_text_rows=5`（§2.2）、`dev_policy_eval_carriers`（五承载全列清单+rows=0）+ `dev_ads_policy_effect_rows=0` + `dev_ads_realdata_policy_metrics_rows=0`（§2.3）、`jiuxin_policy_eval_tables=[]`（§2.4）、`derived[0].policy_current_eval_score=null`（负结论登记）+ `derived[1].ui_mock_weighted_score_reference=76.7`（mock 结构披露）。
- 结果解读：无可算得分（登记键留空）；可交付的是五承载结构证据（评估体系设计图）+ 三源排除链 + mock 权重结构披露。
- 对照需求功能要求的评审：需求要求「组合选取评估指标，查看政策绩效」——**未满足**（评估结果无数据，绩效无从展示）；双触发器闭合后可满足。

### 2.7 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 评估面排除 | gkx 表名扫 | `gkx_eval_like_tables` | `[]`（280 表 0 命中） |
| 文本旁证 | 政策文本评估表述 | `gkx_policy_eval_score_text_rows` | 5（叙述非结果） |
| 结构证据 | dev 效果评估表 | `dev_policy_eval_carriers.policy_effect_eval` | 22 列（五分值列在）0 行 |
| 结构证据 | dev 权重维表 | `policy_support_assessment_indicator` | 21 列（weight/formula 列在）0 行 |
| 结构证据 | dev 综合评估表 | `policy_support_assessment` | 27 列（composite_score 在）0 行 |
| 结构证据 | ads 层镜像 | `dev_ads_policy_effect_rows` | 0 |
| 评估面排除 | 久新交叉扫 | `jiuxin_policy_eval_tables` | `[]`（203 表） |
| 口径缺口 | UI mock 权重 | `ui_mock_weighted_score_reference` | 76.7（演示结构披露） |
| absence | 三源+doc | §3.3 四件 | 评估面 0 命中/0 行 ×3 + 需求无算式 |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| E1 | 评估结果面 | gkx | 280 表词族扫 | 0 命中 | **不存在** | **缺（数据层主因）** |
| E1' | 评估结果面 | dev | `policy_effect_eval` 等 5 承载 | **0 行** | 空表 | 缺（结构在数据空） |
| E1'' | 评估结果面 | jiuxin | 203 表交叉扫 | 0 命中 | **不存在** | 缺 |
| E2 | 评估批次维 | dev | `eval_batch_no`/`eval_stage`/`exec_status` | 列在、无值 | 结构有 | 缺数据（与 E1' 同表） |
| E3 | 五维分值 | dev | 五分值列 + `dimension_results` JSON | 列在、无值 | 结构有 | 缺数据 |
| E4 | 权重/口径维表 | dev | `indicator_weight`/`calculation_formula` | 0 行 | 空维表 | **缺（口径层主因）** |
| E5 | UI 演示值 | UI | evaluationMetrics | — | mock | 边界证据（不作源） |

`support_judgment="完全不支持"`、产物与文首一致。

### 3.2 dev 五维结构与 UI 五维的同构不同名（E3 结构证据）

`policy_effect_eval` 五个分值列（execution_effect 执行效果/social_economic 社会经济/environment 环境/innovation_promotion 创新促进/industry_impact 产业影响）与 UI 雷达五维（覆盖广度/深度力度/协同程度/实施效果/创新引领）**结构同构、命名不同**：两者都是「执行×经济×环境/社会×创新×（覆盖/产业）」的五面体——dev 偏评估机构口径（T/CASTEM 式），UI 偏产品运营口径。这一同构性有两个含义：其一，评估体系立项时两套维度可互映（不必重造）；其二，「以哪套命名对外」是产品裁定不是数据裁定——口径分歧 A（§1.6）的本质。`dimension_results` JSON 槽位可承载每维明细（UI 权重展示区的数据位）。

### 3.3 评估面 absence_probe 全记录

否定性证据四件套：**其一（gkx）**——280 表名扫 eval/score/assess/rating/composite 五词族命中 0；文本面「评估+得分」仅 5 行叙述。**其二（dev）**——五承载（§2.3 表）SHOW COLUMNS + COUNT 全 0 行——「规划过落位、从未写入」；与 Lane6 探针零漂移。**其三（jiuxin）**——203 表交叉扫 0 命中；久新评估族（technology_potential/region/bottleneck）为技术域评估，与政策评估不同物（本件补连被账号锁定阻断时以 Lane4 快照 + schema 文档双证补位，解锁后复跑）。**其四（doc）**——三份需求真源无「当前评估得分」；主需求 :1325/:1331 只给展示语境（「通过多个维度对政策评估结果进行展示」「组合选取评估指标」）；核增 :80 列对比维度（条款/指标/力度/范围/路径）无评分算法；父代理裁定 NEW 在案。

### 3.4 现场复核清单

| 复核项 | 结果 |
|---|---|
| gkx 表名扫 | 280 表，五词族 0 命中 |
| dev 五承载列结构 | 22/23/27/21/12 列（含权重公式列） |
| dev 五承载行数 | **全部 0** |
| 久新交叉扫 | 0 命中（解锁后实测） |
| 需求检索 | 三份真源 0 条目；语境两处在案 |
| 口径归属 | 父代理裁定 NEW（不可搬 PG_COMPOSITE） |
| UI 状态 | mock 五维×权重（76.7 结构披露） |
| 脚本形态 | 三源串行只读；零 demo_* |

## 四、数据缺失情况

### 4.1 评估批次零运行（数据级，主因一）

当前评估得分是评估活动的运行时产物：评估模型按批次对政策打分（何政策×何批次×各维分值）写入结果表。当前链路断在源头——评估模型未立项、评估活动从未发生，dev 五处落位 0 行。修复路径唯一且清晰：评估体系立项 → 首批评估批次运行 → 写入 `policy_effect_eval`（结构已备，含批次号/模型版本/执行状态全链路列）。这一缺口与 POLCMP_022（多维度效果评估）**完全同源**——两件共享同一评估族缺口，是同一接入工程（评估模型立项）的两个读数面；与 POLCMP_008（参与度评估）共享 `policy_simulation_result`/评估语境旁支。

### 4.2 权重口径未立项（方法级，主因二）

即便评估面有数据，「五维→得分」的合成规则也待定版：权重来源三选（专家德尔菲——`policy_support_assessment` 已预留 `delphi_result` 列；文本规则代理——依赖核增 PC-07 指标提取产物；等权保守），维度集两套（UI 五维 vs dev 五维，§3.2 互映可行）。dev 权重维表（`policy_support_assessment_indicator` 的 indicator_weight/calculation_formula/threshold 列）的 0 行状态说明：**权重体系连设计图落位都做了、就是没填数**——立项后填维表即可，无需建表。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 评估模型立项（五维+权重定版） | 建模立项 | **本件 + POLCMP_022（同族）** + 008（旁支） | 可参照 T/CASTEM 1010-2023 范式 |
| 首批评估批次运行+写入 | 评估工程 | 同上 | `policy_effect_eval` 直查可算 |
| 权重维表填数 | 立项子任务 | 本件 | `indicator_weight`/`calculation_formula` 列已备 |
| PC-07 指标提取联动（可选口径②） | 依赖核增产物 | 本件口径② | 文本侧规则打分（须公示口径） |

档位后果：评估立项+批次运行 → **完全直接支持**（五维分直查、加权即得）；仅 PC-07 指标提取（无评估批次）→ 部分支持→完全转换支持（口径公示后）；两者皆无（现状）→ 完全不支持。推荐顺序：与 POLCMP_022 合并立项（同一评估体系摊薄成本），首批批次选 3-5 条政策试点。

## 参考文献

1. T/CASTEM 1010-2023 科技创新政策评估规范[EB/OL]. 国家标准馆·国家数字标准馆. https://www.ndls.org.cn/standard/detail/1268534868d901d05e7d6d004e7095a7 （R1，2026-11-01 WebSearch 核验可达——科技部科技评估中心/清华/中科院战略咨询院起草，规定科技创新政策评估的原则/对象/框架与指标体系/方法（政策文本分析、前后对比、成本效益、专家评议、利益相关者调研）/程序，事前-事中-事后三段适用——本件评估体系立项的直接范式锚）
2. Making policy evaluation work[EB/OL]. OECD. https://www.oecd.org/content/dam/oecd/en/publications/reports/2017/04/making-policy-evaluation-work_c3f3bbfd/c9bb055f-en.pdf （R2，2026-11-01 WebSearch 核验可达（同批 POLPAN_005 件 R5 已核）——OECD 政策评估方法论：相关性/有效性/效率/影响评估四问框架，国际评估维度集对照）
3. Quantitative Evaluation of Big Data Development Policy: Text Data Analysis Based on Coword Network and Policy Tools[EB/OL]. Computational Intelligence and Neuroscience. https://doi.org/10.1155/2022/5141431 （R3，2026-11-01 WebSearch 核验可达（同批 POLPAN_005 件 R1 已核）——政策工具文本量化评估路径：政策文本侧特征打分的方法论，对应本件口径②（PC-07 规则打分）的可行性参照）

# 附件

## 附录 A 原始需求原文摘录

**三份需求说明书均无「当前评估得分」字样。**两处最近语境：

主需求 :1325（1.1.1.1.4.2.2.1 政策分析报告可视化呈现）：

> 通过多维指标趋势图、分区对比分析、结构关联可视化等方式，将政策评估数据和分析结果全面立体地展示。……有效解决传统数据分析难以全景展示政策效能的问题。

主需求 :1331（1.1.1.1.4.2.2.1.1 多维指标趋势图）：

> 系统针对政策效能评估核心数据自动生成趋势分析图，支持按时间、区域、类别进行多维切换。用户可组合选取评估指标，查看政策绩效随变量变化的动态趋势。

核增需求 :80（1.1.1.1.4.2.4.3.1 跨政策交叉对比，PC-09）：

> 支持多份政策文件在条款内容、核心指标、扶持力度、适用范围、实施路径等维度的交叉比对，自动识别政策间的共性、差异、互补与冲突点。

UI mock 语义源（`policyData.js:446-452`）：

> export const evaluationMetrics = [
>   { key: 'coverage', label: '覆盖广度', value: 85, weight: 20 },
>   { key: 'depth', label: '深度力度', value: 78, weight: 25 },
>   { key: 'coordination', label: '协同程度', value: 72, weight: 20 },
>   { key: 'implementation', label: '实施效果', value: 68, weight: 25 },
>   { key: 'innovation', label: '创新引领', value: 82, weight: 10 },
> ];

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 当前评估/当前评估得分 | 主需求 + SRS 政策族 + 核增 17 叶 | 0 |
| 评估指标体系/评估得分 | 同上 | 0（仅评估语境段） |
| 政策绩效 | 主需求 :1331 | 1（展示语境） |
| 交叉比对 | 核增 :80 | 1（PC-09 维度语境） |
| evaluationMetrics | `policyData.js` | `:446-452`；消费方 `PolicyAnalysis.jsx:357/:1617` |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_POLCMP_016_out.json`（2026-11-01 实跑：gkx 评估词族扫 + dev 五承载全列结构行数 + 久新补连与旁证登记 + absence 四件）。
- 共享探针：`code/_snapshots/_shared_probe_s3_01_out.json`（fix2_20261101 政策 20,000——B11 锚）、`code/_probe_lane6_s302_r2_out.json`（dev 政策族 rowcounts/columns 组——五承载 0 行与列结构一致性来源）、`code/_probe_lane4_s302_out.json`（久新锁定时段快照）、ADS Schema 5.11.0 文档。

### B.2 本件产物逐键清单（`code/M_SCIUI_POLCMP_016_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `facts.gkx_table_count` | 计数 | 280 | §2.2 |
| `facts.gkx_eval_like_tables` | 探针 | `[]`（0 命中） | §〇/§2.2 |
| `facts.gkx_policy_rows` | 计数 | 20,000 | §2.2 |
| `facts.gkx_policy_eval_score_text_rows` | 计数 | 5（叙述） | §2.2 |
| `facts.dev_policy_eval_carriers` | 结构 | 4 表全列清单（22/23/27/21 列）+ rows 全 0 | §2.3/§3.2 |
| `facts.dev_ads_policy_effect_cols/rows` | 结构+计数 | 12 列 / **0** 行 | §2.3 |
| `facts.dev_ads_realdata_policy_metrics_rows` | 计数 | 0 | §2.3 |
| `facts.jiuxin_table_count` | 计数 | 203 | §2.4 |
| `facts.jiuxin_policy_eval_tables` | 探针 | `[]` | §2.4 |
| `facts.jiuxin_ads_research_problem_policy_evidence_rows` | 登记 | 未取证（旁证复核 0 行） | §2.4 |
| `derived[0]` | 登记 | `policy_current_eval_score=null` | §2.6 |
| `derived[1].ui_mock_weighted_score_reference` | 披露 | 76.7（7,670/100） | §2.5 |
| `absence_probe` | 探针 | 四件（gkx/dev/jiuxin/doc） | §3.3 |
| `support_judgment` | 判档 | 完全不支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 评分结构 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| 评估规范范式 | T/CASTEM 1010-2023（R1） | 框架×指标×程序 | dev 落位表同构、0 行 | **最高（立项目标态）** |
| 文本量化打分 | 政策工具计分（R3） | 文本特征分 | 文本在、规则未立项 | 中（口径②候选） |
| 国际评估框架 | OECD 四问（R2） | 相关/有效/效率/影响 | 无承载 | 中（维度集对照） |
| 专家德尔菲 | `delphi_result` 列预留 | 专家加权 | 列在 0 行 | 中（权重来源候选） |
| 前端演示 | UI 五维×权重 | 加权百分制 | mock | 结构披露（不作源） |

### C.2 数据矩阵

| 依赖 | gkx | dev | jiuxin |
|---|---|---|---|
| 评估结果面 | 0 命中 | 5 承载 0 行 | 0 命中（技术域评估不同物） |
| 批次/模型版本维 | — | 列在（eval_batch_no/eval_model_version） | — |
| 权重维表 | — | 列在（indicator_weight/formula）0 行 | — |
| 政策底表 | 20,000 行 | policy_base_info（同源池） | — |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v0（现状） | 负结论登记 + 五承载结构证据 | — |
| v1 | 评估体系立项（五维定版+权重维表填数） | 建模立项 |
| v2 | 首批评估批次运行写入（3-5 条政策试点） | v1 |
| v3 | 批次常态化 + 当前快照直查（本件升档） | v2 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 维度集两套（UI vs dev）对外口径打架 | 中 | 立项时互映表定版（§3.2） |
| 权重主观性引发公信力质疑 | **高** | 权重来源三选公示+敏感性分析随行 |
| 「当前」快照时效（批次间隔期读数老化） | 中 | 快照时间戳随行展示 |
| 评估成本高（批次难以常态化） | 中 | 首批试点→文本规则打分混合模式过渡 |

### C.5 总判

**完全不支持**：评估结果面三源零数据（280 表/五承载 0 行/203 表三扫留证）+ 权重口径未立项——双缺叠加；dev 五承载（含权重公式维表）是「补数据可解」的直接结构证据，升档双触发器（评估立项+批次运行 / PC-07 规则打分口径公示）写死不悬空；口径归属从父代理裁定 NEW（核增 PC-09 新语义，不搬 PG_COMPOSITE）。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_POLCMP_016.py` | 退出码 0，落 `_out.json` |
| 数据入口 | `_gkxdb.py`（gkx）+ 直连 dev/久新 | demo_* 直接 raise |
| 判档一致 | 文首 vs `support_judgment` | 完全不支持 |
| 负证据探针 | 产物 `absence_probe` 四件 | gkx/dev/jiuxin/doc 各一 |
| B11 对账 | dev 5 表 0 行 = Lane6 探针 = POLCMP_002/_008 产物 | 零漂移 |
| 幂等重跑 | SQL 全只读无随机 | 逐位一致（久新连接状态键随解锁变化，属连接状态非数据漂移） |
