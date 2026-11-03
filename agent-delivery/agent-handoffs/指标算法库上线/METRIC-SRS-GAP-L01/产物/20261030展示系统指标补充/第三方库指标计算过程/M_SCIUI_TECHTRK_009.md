# 领域技术平均成熟度（M_SCIUI_TECHTRK_009）

> **类型**：SCORE（平均分，聚合）｜ **域**：科技发展态势·技术发展跟踪·技术评估结果｜ **UI 挂载**：科技信息展示系统 → 技术发展跟踪 → 评估工作流区 KPI 条（techDevelopmentTracking.js:1023「平均成熟度」，mock 72 分，演示值不参与支持度结论）
> **数据支持度**：**部分支持**｜ **公式定义人**：仿王惠（推测定义，非招标原文闭合口径）｜ **口径归属**：UI 推导叶（筛选记录 row_01 14），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_TECHTRK_009.py`｜ **产物**：`code/M_SCIUI_TECHTRK_009_out.json`
> **四判定摘要**：直接结构 = 否（开发库/gkx 无技术成熟度结果面）；直接数据 = 否；依赖结构 = 是（久新 stage_assessment+transfer_stage 38,860 行阶段面）；依赖数据 = 部分（规则基线两档覆盖+无领域维映射）
> **数据源口径**：本件支持度按「开发库 gkxlumenx_*（禁 demo_*）+ 三方库 gkx（183.240.141.251:3318 只读）+ 久新 jiuxin（47.93.119.170:29030 只读）」三源评估（20261101 三源铁律）。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：部分支持。** 降档根因有二：其一，成熟度的「分值」语义无承载——三源没有任何表给出 0–100 的成熟度分（UI mock 的「分」量纲），久新给的是**八阶段序数**（stage_code/stage_order），分值化必须借口径假设（本报告 B10 双口径并列）；其二，「领域」维度断链——承载表的主键是 ETO 研究簇候选节点（`node_identity_type='RESEARCH_CLUSTER_CANDIDATE'`，`tech_id=NULL`、`mapping_status='UNMAPPED'`），「按领域平均」所需的正式技术目录映射未发布，领域切片口径悬空。结构面（38,860 行阶段研判 × 19,430 节点）与数据量（足够大）都达标，所以不是「完全不支持」，但两条断链均非数据工程可即时闭合，也进不了「完全转换支持」。

### 批次通用纪律摘要（批 S3-01 共用，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 派生比分子分母同源（同一 stage_assessment 表加权） |
| B4 | 负结论带探针 | absence_probe：gkx 280 表+列扫描 / dev dwd+ads 表扫描逐一留证 |
| B5 | 确定性 | 聚合按 stage_code 排序；无 set 迭代序依赖 |
| B6 | 闸门自身被闸 | 不自跑闸门，由派单方统一跑 |
| B7 | 产物只由脚本产出 | 手改禁令；改脚本→重跑 |
| B8 | 回执不复收 | 派单方抽硬证据复验 |
| B9 | 单位/日期陷阱 | 无年份列（版本化制）；stage_confidence DECIMAL 直读 |
| B10 | 口径裁定保守交付 | 8 分制/百分制双口径并列 + 降档/升档触发器写死（§1.6） |
| B11 | 多本账互推 | 共享快照引用零漂移（本件主表为久新，快照无此表，不构成互推对） |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 结果面存在吗？ | 存在但语义不同构（阶段序数非分值） | 久新 stage_assessment 38,860 行（facts.jiuxin_stage_assessment_rows） |
| 分值化口径闭合吗？ | 不闭合（需口径假设） | 8 分制 6.0713 / 百分制 72.4476 两口径并存（derived） |
| 领域维可用吗？ | 不可用（映射未发布） | tech_id=NULL、mapping_status='UNMAPPED'（久新 schema §24.1） |

## 摘要

「平均成熟度」是技术发展跟踪页评估工作流 KPI 条的第三张卡（话题热度/产业化潜力/平均成熟度/待验证瓶颈），前端语义为选中技术集的 maturity 均值取整（mock 72 分）。三源探测：开发库与 gkx 无任何技术成熟度结果面（absence_probe 命中 0，gkx 仅债券/基金的到期日类 `maturity_date` 伪命中）；久新 `ads_technology_stage_assessment` 38,860 行（19,430 节点 × 2 模型版本）给出规则基线的八阶段研判，是唯一结构化承载。本报告以 transfer_stage 八档序数完成两口径复现：全节点 8 分制平均 6.0713、百分制 72.4476；深圳子盘（6,233 节点）8 分制 6.8030、百分制 82.8998。降档双因：分值语义需口径假设（基线只落 ENGINEERING/INDUSTRIALIZATION 两档，19,430 节点无一在其余六档）、领域维映射未发布。判**部分支持**。脚本已跑通，正文与产物数字逐一对应。

- 需求判定：**UI 推导叶**（指标名三份说明书未出现；SRS seq 50 气泡图叶「位置表示技术发展阶段或成熟度」为可视化描述非定义）。
- 复现状态：脚本已跑通；两口径均值 + 深圳切片落产物。
- 档位结论：**部分支持**（分值口径假设 + 领域映射断链双因）。
- 关键事实：基线阶段只落两档（INDUSTRIALIZATION 20,816 行 / ENGINEERING 18,044 行），全节点均值被结构性抬到「贴近产业化」区间。
- 升档路径：甲方裁定分值口径 + Cluster→正式技术目录映射发布 → 可升完全转换支持。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/**技术发展跟踪**/技术评估结果与评估工作流（SRS seq 48–55，excel_rows 51–58）。UI 挂载点是 `techDevelopmentTracking.js` 的 `buildMetrics()`：对当前筛选+选中的技术话题集（上限 10 个）计算四张 KPI 卡，「平均成熟度」是第三张——`averageMaturity = Math.round(topics.reduce((sum, item) => sum + item.maturity, 0) / count)`，单位「分」，配 trend '+6.1%'。该 KPI 条在热力图/气泡图等多个视图顶部共享，随领域/地域/时间筛选联动重算。

挂载行号实查：`techDevelopmentTracking.js:1023`（`{ key: 'maturity', label: '平均成熟度', ... }`），计算式在 `:1017`（averageMaturity 定义）。话题数据源是 `coreHotTopics`（8 个常量话题，maturity 46–82）叠加 `simulatedHotTopics`（36 个种子生成话题，maturity 52–82）——**全部为前端常量/种子生成，演示值，不参与支持度结论**。同文件 `:59` 时间线事件「支撑话题热度、平均成熟度的基线口径」是前端叙事文本，同样非数据证据。

组件行为有两点值得记录：其一，「平均」的作用域是**当前选中话题集**而非全域——mock 默认按热度取 Top10，真实数据接入后作用域语义（选集均值 vs 全域均值 vs 领域均值）需产品裁定；其二，`buildWorkflow()`（`:1098`）用 averageMaturity 决定评估工作流高亮到哪一步（≥74 到「结果生成」、≥62 到「分析计算」），即该读数在 UI 里不只是展示，还驱动流程状态机——上游口径漂移会级联影响工作流展示。

### 1.2 为什么需要本指标

成熟度是技术跟踪的「时钟」：热度告诉你什么受关注，潜力告诉你什么值得投，成熟度告诉你**什么已经能落地**。规划场景下（页面另一挂载 `TechDevelopmentPlan.tsx` 的方案卡语境），决策者需要知道一个领域的平均成熟度处于基础研究还是产业化区间，来决定资源投向是补研发还是补转化。KPI 卡把它做成单值快照，配合 trend 变化幅度，服务「一眼判断领域所处阶段」的汇报需求。

数据侧本件的核心张力在「成熟度」这个词的多义性：学术口径（TRL 1–9 就绪度）、产业口径（实验室→中试→量产的转化阶段）、评分口径（0–100 综合分）。UI mock 用「分」暗示评分口径，而三源唯一承载（久新）是转化阶段口径——这不是简单的换算问题，而是需要甲方显式选择语义的口径裁定问题（§1.6 双口径触发器）。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**三份说明书（《科技发展态势/技术发展跟踪.md》《科技全域态势.md》《全球创新监测.md》）均未出现「平均成熟度」该指标名。技术发展跟踪.md 里最接近的原文是 seq 50 动态气泡图叶：「位置表示技术发展阶段或成熟度」——这是可视化映射描述（气泡坐标轴用什么），不是指标定义（成熟度怎么算）。主需求文档《科技信息展示系统和科技专题服务系统.md》同段只有功能复述。

### 1.4 类似指标权威方法可行性分析概要

成熟度测度的权威方法是 NASA/GAO 的 TRL（Technology Readiness Levels）体系：TRL 1–9 九级，从基本原理观察到实际任务验证，评估必须基于可验证证据（测试报告/分析资料/样机记录），且等级相对目标环境而定（同一技术对地轨任务是 TRL 9、对金星着陆可能只是 TRL 4）（R1/R2/R3）。欧盟 Horizon 计划与 ISO 16290:2013 均沿用 TRL 框架。国内装备预研领域普遍采用 GJB 7688 类似的 9 级制。方法族对照：

| 方法族 | 判定轴 | 数据要求 | 与三源匹配 |
|---|---|---|---|
| TRL 就绪度（NASA/GAO，R1/R2/R3） | 证据链等级（测试/样机/任务验证） | 逐技术的验证证据记录 | **无（三源无证据链表；久新 assessment_evidence 仅论文/专利/项目计数）** |
| 转化阶段制（久新现行，8 阶段） | 论文/专利/企业/项目证据组合规则 | 证据计数即可 | **有（stage_assessment 38,860 行）** |
| 文献计量代理（专利族/引用成熟曲线） | S 曲线位置拟合 | 长时序论文/专利序列 | 部分（gkx 论文/专利有量无技术节点映射） |
| 评分制（UI mock 语义，0–100 分） | 综合评分模型 | 分值结果面 | **无（需口径假设从阶段制映射）** |

结论：权威 TRL 需要的证据链记录三源均无；库内唯一可复算的是久新规则基线的转化阶段制，评分制只能经口径假设映射获得。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/techDevelopmentTracking.js:1023` — `{ key: 'maturity', label: '平均成熟度', value: averageMaturity, unit: '分', direction: 'rise', trend: '+6.1%' }`；`:1017` — `const averageMaturity = Math.round(topics.reduce((sum, item) => sum + item.maturity, 0) / count);`；mock 话题常量 `:109-231`（coreHotTopics 8 条）与 `:308-329`（simulatedHotTopics 36 条种子生成）。
- SRS：`…/科技发展态势/技术发展跟踪.md` seq 50（excel_row 53）动态气泡图叶「位置表示技术发展阶段或成熟度」——可视化描述，非指标定义；检索记录见附录 A。
- 久新 schema：`2026-10-22-ADS_SCHEMA-5.11.0.md` §24.6（阶段研判算法：`RULE_BASED_EVIDENCE_BASELINE` 五条规则）、§24.12.13（stage_assessment 字段字典）、§24.12.19（transfer_stage 八阶段定义）。
- 主需求文档：《科技信息展示系统和科技专题服务系统.md》「成熟度」相关段均为功能复述（检索记录附录 A）。

### 1.6 推测原意与推测定义

**推测定义（B10 双口径并列，均须披露口径假设）**：

- **口径 A（8 分制阶段序数均值）**：$\bar{M}_{order} = \sum_s n_s \cdot order_s / \sum_s n_s$，其中 $order_s$ 取久新 transfer_stage 的 stage_order（基础研究=1 … 市场规模化=8）。实测 **6.0713**（全节点），读数语义「平均已过工程化(5)、贴近产业化(7)」。
- **口径 B（百分制映射）**：$score_s = (order_s - 1)/(8-1) \times 100$ 后同权平均，得 **72.4476**——与 UI「分」量纲对齐（量纲对齐纯属构造，mock 72 与实测 72.45 的接近不构成任何数据证据）。
- 口径 C（TRL 9 级制对齐）：无证据链承载，**不可构建**，仅作方法谱系参照。

**降档/升档触发器（B10 模板）**：若甲方裁定接受口径 A/B 之一且接受「研究簇候选=技术」的临时身份 → 仍部分支持但语义闭合（领域切片仍缺）；若 Cluster→正式技术目录映射发布（`mapping_status` 离开 UNMAPPED）→ 领域维可用，可升**完全转换支持**；若甲方要求 TRL 口径或专家确认口径 → 三源无证据链/专家标注承载，维持部分支持不升档。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技发展态势/技术发展跟踪.md` |
| 所属四级功能 | 技术发展跟踪（8 叶，seq 48–55） |
| 本件挂载视图 | 评估工作流 KPI 条 + 气泡图（X 轴=成熟度，`buildBubbles`）+ 详情卡「详细评估参数」首行（`techDevelopmentTracking.js:1449`） |
| 需求叶对应 | 无同名叶；最近叶为 seq 50 动态气泡图展示（成熟度作轴）与 seq 52 评估流程概览（KPI 条语境） |
| 批内相邻件 | M_SCIUI_TECHTRK_015/016（本次评估得分/潜力评估得分，同为需业务建模类、同依赖久新评估表族）；M_SCIUI_TECHTRK_018（竞争力水平与潜力评估，TechDevelopmentPlan 侧挂载） |

本件与 015/016 是同一评估表族（potential_assessment/stage_assessment）的不同切面：015/016 消费潜力分（DECIMAL 分值，语义同构），本件消费阶段码（序数，语义异构）——这决定了本件必须做口径假设而 015/016 不用，也是本件单独降档的原因。

## 二、计算过程

### 2.1 装载与规模校验

经久新 Doris 只读连接（批统一入口，库 gkx_technology_analysis_dev）。主表 `ads_technology_stage_assessment` 全表 38,860 行（facts.jiuxin_stage_assessment_rows），与共享快照 `_shared_probe_s3_01_out.json` jiuxin 组 `38860` 读数零漂移（B11）。节点级去重后 19,430 个 technology_node_id（facts.jiuxin_stage_assessment_nodes），恰好等于 `ads_technology_profile` 全表节点数——每节点两个模型版本（`technology_insight_mvp_v1` / `technology_insight_mvp_v2_eto_cluster_technology`，facts.jiuxin_stage_assessment_model_versions=2）各留一行研判，两版本在现有发布内的 stage_code 判定一致（按节点去重后 stage 分布与行级分布对应同一 10,408/9,022 切分）。

阶段定义表 `ads_technology_transfer_stage` 8 行全量读取（facts.jiuxin_transfer_stage_def）：BASIC_RESEARCH=1 基础研究 → MARKET_SCALE=8 市场规模化，本件口径映射的序数轴即来自此表，非报告自造。

### 2.2 阶段分布读数

行级分布（facts.jiuxin_stage_code_dist）：INDUSTRIALIZATION 20,816 行 / ENGINEERING 18,044 行——**全表只落两档**。节点级分布（facts.jiuxin_nodes_by_stage_unique）：INDUSTRIALIZATION 10,408 / ENGINEERING 9,022。这与 schema §24.6 的规则说明吻合：首版 Cluster 入选要求 Patent–seed 证据，因此规则五条分支里「无论文→UNCERTAIN」「无专利→EARLY_RESEARCH」等低档分支对入选集不触发，实际只剩「有专利无 company→ENGINEERING_VALIDATION」与「company+project→EARLY_COMMERCIALIZATION」两支的下游映射（发布语义在 stage 表中对应 ENGINEERING/INDUSTRIALIZATION 两档）。**含义**：均值读数不是「技术普遍很成熟」，而是「入选集被前置条件剪枝到成熟段」——报告把这个结构性事实写进 notes，防读数误读。

评估方法全表单一 `RULE_BASED_EVIDENCE_BASELINE`（facts.jiuxin_assessment_method_dist），stage_confidence 全表恒 0.9000（min=max=avg，facts.jiuxin_stage_confidence_*）——置信度无区分度，不可作加权权重。

### 2.3 口径 A：8 分制均值

$\bar{M}_{order} = (10{,}408 \times 7 + 9{,}022 \times 5) / 19{,}430 = 6.0713$（facts.jiuxin_avg_stage_order_8scale；derived 分子 117,966 / 分母 19,430）。SQL 侧两表聚合（stage_assessment 按 stage_code 计节点数 × transfer_stage 取 stage_order），Python 侧加权平均，全流程确定性可复算。

### 2.4 口径 B：百分制映射

$score(order) = (order-1)/7 \times 100$：INDUSTRIALIZATION→85.7143、ENGINEERING→57.1429；同权平均得 **72.4476**（facts.jiuxin_avg_maturity_pct_scale；derived 分子 1,407,657 / 分母 19,430）。映射函数是线性等距假设——这是本件最重的口径假设，若甲方主张「阶段间距不等」（如中试到工程化比概念到中试难），可换单调映射重算，方法论不变。

### 2.5 深圳子盘切片

需求页面语境是深圳科技规划（技术发展跟踪页按深圳/波士顿/东京等区域叙事），补深圳切片：经 `ads_technology_region_yearly_metrics` 以深圳稳定 Location ID（`loc_E16782C21F18EBF8A59C1E98F9C9860B`，schema §24.2 明确「不应按城市名称直接连接」）圈定 6,233 节点（facts.jiuxin_shenzhen_stage_nodes），阶段分布 INDUSTRIALIZATION 5,619 / ENGINEERING 614（facts.jiuxin_shenzhen_nodes_by_stage）——深圳节点 90.1% 已落产业化档，均值 8 分制 6.8030 / 百分制 82.8998（facts.jiuxin_shenzhen_avg_*）。深圳显著高于全域（72.45 → 82.90），方向上与「深圳产业化集中」的先验一致，但注意子盘经深圳证据命中筛选，本身有选择偏置。

### 2.6 稳健性与口径敏感性

三方面敏感性：其一，版本敏感性——两 model_version 现发布判定一致，若未来版本分歧，均值口径需先裁定「取最新版本」还是「跨版本平均」，当前报告按节点去重等效于任选；其二，映射敏感性——口径 B 的等距假设换非单调不动序的映射（如对数间距），百分制读数会变但序不变，均值敏感度约 ±3 分（构造性估计，不入产物）；其三，集合敏感性——UI 语义是「选中话题集均值」（Top10 by heat），本报告给的是全域/深圳两种全集口径，选集口径需真实热度数据接入后才有意义（与 M_SCIUI_TECHTRK_017 热度件共用上游）。负结论侧：gkx 的 `maturity_date`/`fund_maturity_date` 命中（absence_probe 6 列）是债券/基金**到期日**，与技术成熟度无语义关系，属关键词伪命中，已排除。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_TECHTRK_009.py`（久新直连只读 + `_gkxdb.py` 做 gkx 探针 + 开发库直连做 dev 探针；零 `demo_*`）。运行 `python3 code/M_SCIUI_TECHTRK_009.py`。
- 产物：`code/M_SCIUI_TECHTRK_009_out.json`。正文数字与产物键逐一对应：`jiuxin_stage_assessment_rows=38860`（§2.1）、`jiuxin_transfer_stage_def`（§2.1 序数轴）、`jiuxin_stage_code_dist`/`jiuxin_nodes_by_stage_unique`（§2.2）、派生 `jiuxin_avg_stage_order_8scale=6.0713`（§2.3）、`jiuxin_avg_maturity_pct_scale=72.4476`（§2.4）、`jiuxin_shenzhen_*`（§2.5）、absence_probe 三件（§三）。
- 结果解读：两口径均值 + 深圳切片三组读数可直接回填 UI KPI 卡（前提是口径裁定）；「两档覆盖」的结构性事实必须随读数披露。
- 对照需求功能要求的评审：单值平均——满足（口径 A/B 均出数）；「分」量纲——口径 B 满足（假设披露）；按领域切片——不满足（映射未发布）；趋势 '+6.1%'——不满足（无年度序列，版本快管制）。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 装载 | 主表行数 | `jiuxin_stage_assessment_rows` | 38,860 |
| 装载 | 节点数 | `jiuxin_stage_assessment_nodes` | 19,430 |
| 装载 | 模型版本数 | `jiuxin_stage_assessment_model_versions` | 2 |
| 轴定义 | 八阶段序数 | `jiuxin_transfer_stage_def` | 1–8（基础研究→市场规模化） |
| 分布 | 行级 stage 分布 | `jiuxin_stage_code_dist` | INDUSTRIALIZATION 20,816 / ENGINEERING 18,044 |
| 分布 | 节点级分布 | `jiuxin_nodes_by_stage_unique` | 10,408 / 9,022 |
| 置信 | confidence 统计 | `jiuxin_stage_confidence_*` | 恒 0.9000（无区分度） |
| 口径A | 8 分制均值 | `jiuxin_avg_stage_order_8scale` | 6.0713（117,966/19,430） |
| 口径B | 百分制均值 | `jiuxin_avg_maturity_pct_scale` | 72.4476（1,407,657/19,430） |
| 深圳切片 | 深圳节点/均值 | `jiuxin_shenzhen_*` | 6,233 节点；6.8030 / 82.8998 |
| absence | gkx 结果面 | absence_probe[0] | 280 表命中 0 |
| absence | dev 结果面 | absence_probe[2] | 伪命中 3（政策类/链阶段，语义不符） |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 阶段研判结果 | jiuxin | `ads_technology_stage_assessment` | 38,860（19,430 节点） | 直查 | **有**（主承载） |
| D2 | 阶段序数定义 | jiuxin | `ads_technology_transfer_stage` | 8 | 直查 | 有 |
| D3 | 分值结果面（0–100 成熟度分） | 三源 | — | — | **不存在** | **缺**（口径假设替代） |
| D4 | 领域映射（技术→领域） | jiuxin | profile.tech_id / mapping_status | UNMAPPED 全量 | 不可用 | **缺**（映射未发布） |
| D5 | 深圳圈定 | jiuxin | region_yearly_metrics（深圳 loc） | 15,630 行/6,233 节点 | 直查 | 有 |

`support_judgment="部分支持"`，与文首同档（闸 6 一致）。

### 3.2 D1/D2 唯一承载的可用性

38,860 行 × 双模型版本的结构完整、行数充足（19,430 节点对「领域均值」级别的聚合绰绰有余），transfer_stage 八档定义齐备（中文名直接可用于 UI 图例）。可用性限制全部来自**语义层**：规则基线（非 TRL/非专家确认，schema §24.6 原文「不冒充联网LLM判断」）、两档覆盖（入选剪枝所致）、confidence 恒定（不可加权）。这三条都已写入产物 notes，作为读数随行披露项。

### 3.3 D3/D4 的 absence_probe 全记录

否定性证据三件套：**查了什么**——① gkx 280 表名扫 `%matur%/%stage%/%trl%/%assess%/%evaluat%` 命中 0 表；② gkx 全列扫 `%matur%/%trl%` 命中 6 列，逐列核对全部是债券/基金的到期日字段（`dwd_high_tech_industry_bonds.maturity_date` 等），语义排除；③ 开发库 gkxlumenx_dwd+ads 表名同模式扫描命中 3 表（policy_support_assessment*2、chain_stage），逐表核对分别是政策扶持评估与产业链阶段标签，均非技术成熟度承载。**条件**——结果面级存在性（表名+字段语义双重核对）。**命中**——0（有效命中）。四缺失情形归属：**表存在但语义不符**（伪命中已逐一排除）+ **映射字段存在但值未发布**（D4）。

### 3.4 深圳切片链路（D5）

深圳圈定走 schema 指定路径：`ads_location` 治理 ID（非城市名硬连）→ region_yearly_metrics 过滤 → 节点集交 stage_assessment。6,233 节点（与共享读数一致）产出深圳均值 82.8998（百分制）。该链路同时服务 008（区域排名）与 015/016（评估得分）件，本件 SQL 即批内可复用资产。

### 3.5 现场复核清单

| 复核项 | 结果 |
|---|---|
| 主表行数对账 | 38,860 = 共享快照 jiuxin 组读数（零漂移） |
| 节点去重 | 19,430 = ads_technology_profile 全表节点数 |
| 双版本一致性 | 两 model_version 各 19,430 行，stage 判定一致 |
| 口径 A 算术 | (10,408×7+9,022×5)/19,430 = 6.0713 ✓ |
| 口径 B 算术 | (10,408×85.7143+9,022×57.1429)/19,430 = 72.4476 ✓ |
| 伪命中排除 | maturity_date 6 列 + dev 3 表逐一语义核对 |
| 脚本形态 | 单进程顺序查询，三源连接分离，零 demo_* |

## 四、数据缺失情况

### 4.1 分值结果面缺失（口径级，主因）

三源没有任何表给出技术级 0–100 成熟度分。UI 的「分」量纲只能经阶段序数映射构造，而映射函数（等距/不等距）是口径假设。修复建议：甲方从三个选项裁定——A1 接受等距映射（本报告口径 B，即期可用）；A2 指定非等距映射表（提供阶段间距权重，半日工程重算）；A3 坚持评分制语义（则需新建评分模型立项，本件维持部分支持）。影响面：本件 + 015/016（若同样需分值语义）+ 020（技术发展指数，同评分语义族）。

### 4.2 领域映射断链（维度级，次因）

「按领域平均」所需的 Cluster→正式技术目录映射 `mapping_status='UNMAPPED'` 全量未发布（schema §24.1 明确当前身份是研究簇候选）。替代路径：`profile` 的 `domains_raw/fields_raw` 快照字段是来源 Domain/Field 名称文本，可作临时分组轴（语义弱：非受控词表）；或等久新发布正式 mapping release。影响面：本件领域切片 + 017 热度件的话题分组 + 020 发展指数的领域维。

### 4.3 年度序列缺失（时序级）

stage 表是 model_version 快照制，无统计年份列；UI trend '+6.1%' 类同比读数无承载。上游 `ads_technology_yearly_metrics` 有年度论文/专利序列，可支撑「文献计量代理」的 S 曲线拟合路线（§1.4 方法族③），但那是另一口径的成熟度，需独立立项。影响面：本件 trend 位 + 022 评估结果追踪件（历史得分序列，Lane 4）。

| 缺失项 | 类型 | 对档位的影响 |
|---|---|---|
| 0–100 成熟度分值面 | 口径级 | 分值语义需假设 → 主降档因 |
| Cluster→技术目录映射 | 维度级 | 领域切片不可用 → 次降档因 |
| 年度成熟度序列 | 时序级 | trend 读数无承载 → 附加缺口 |
| 证据链/专家标注 | 源级 | TRL 口径不可构建 → 升档路径受阻 |

四项中前两项直接压住档位：口径假设未裁定时任何分值读数都是「待裁定交付」；映射未发布时「领域」前缀名不副实。修复组合推荐：即期 A1（等距映射）+ domains_raw 临时分组轴（标注非受控），中期推动 mapping release。

## 参考文献

1. Technology Readiness Levels – Definitions[EB/OL]. NASA Earth Science and Technology Office. https://esto.nasa.gov/trl/ （R1，2026-11-01 WebSearch 核验可达）
2. Technology Readiness Assessment (TRA) Best Practices Guide, SP-20205003605[EB/OL]. NASA. https://ntrs.nasa.gov/api/citations/20205003605/downloads/%20SP-20205003605%20TRA%20BP%20Guide%20FINAL.pdf （R2，2026-11-01 WebSearch 核验可达）
3. GAO-20-48G Technology Readiness Assessment Guide[EB/OL]. U.S. Government Accountability Office. https://www.gao.gov/assets/710/706680.pdf （R3，2026-11-01 WebSearch 核验可达）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技发展态势/技术发展跟踪.md》seq 50 动态气泡图展示叶（excel_row 53）：

> 采用气泡图形式展示技术评估的多维数据，气泡大小代表技术规模或投资额，位置表示技术发展阶段或成熟度，颜色表示技术类型或领域。

**「平均成熟度」指标名在三份说明书未出现。**UI 组件 `techDevelopmentTracking.js:1023` 的「平均成熟度」标签是前端作者对「成熟度」可视化语义的 KPI 化推导。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 平均成熟度 | srs/…/技术发展跟踪.md | 0 |
| 平均成熟度 | srs/…/科技全域态势.md | 0 |
| 平均成熟度 | srs/…/全球创新监测.md | 0 |
| 成熟度 | srs/…/技术发展跟踪.md | 1（seq 50 可视化描述） |
| 成熟度 | 科技信息展示系统和科技专题服务系统.md | 功能复述段（无定义） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_TECHTRK_009_out.json`（20261101 实跑：两口径均值、深圳切片、absence_probe 三件）。
- 共享快照：`code/_snapshots/_shared_probe_s3_01_out.json`（jiuxin 组 `ads_technology_stage_assessment` 38,860 行读数，本件主表行数与之零漂移）。

### B.2 本件产物逐键清单

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `metric_id` | 标识 | M_SCIUI_TECHTRK_009 | 文首 |
| `ui_evidence` | 证据 | 3 条组件行号 | §1.5 |
| `requirement_trace.named_in_srs` | 事实 | **false** | §1.3/附录 A |
| `facts.jiuxin_stage_assessment_rows` | 计数 | 38,860 | §2.1 |
| `facts.jiuxin_stage_assessment_nodes` | 计数 | 19,430 | §2.1 |
| `facts.jiuxin_transfer_stage_def` | 定义 | 8 阶段含中文名 | §2.1 |
| `facts.jiuxin_stage_code_dist` | 分布 | 2 档 | §2.2 |
| `facts.jiuxin_nodes_by_stage_unique` | 分布 | 10,408/9,022 | §2.2 |
| `facts.jiuxin_stage_confidence_*` | 统计 | 恒 0.9000 | §2.2 |
| `facts.jiuxin_avg_stage_order_8scale` | 均值 | 6.0713 | §2.3 |
| `facts.jiuxin_avg_maturity_pct_scale` | 均值 | 72.4476 | §2.4 |
| `facts.jiuxin_shenzhen_*` | 切片 | 6,233 节点 / 6.8030 / 82.8998 | §2.5 |
| `derived[0]` | 派生 | 6.0713（117,966/19,430） | §2.3 |
| `derived[1]` | 派生 | 72.4476（1,407,657/19,430） | §2.4 |
| `absence_probe` | 负证据 | gkx 0 表/6 伪命中列 + dev 3 伪命中表 | §3.3 |
| `support_judgment` | 判档 | 部分支持 | §〇 |
| `notes` | 披露 | 规则基线/两档覆盖/口径巧合禁引 | §〇/§2.2 |

### B.3 共享快照消费

本件消费 `_shared_probe_s3_01_out.json` jiuxin 组 `ads_technology_stage_assessment` 行数键（38,860）作对账锚点；未消费 gkx/dev 组键（本件 gkx/dev 侧均为 absence 探针，由本件脚本自跑留证）。

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表文献/机构 | 判定轴 | 数据要求 | 三源承载 | 贴合度 |
|---|---|---|---|---|---|
| TRL 就绪度 | NASA NPR 7123.1 / GAO-20-48G（R1/R2/R3） | 证据链等级 | 测试报告/样机/任务验证记录 | 无 | 高（目标态，不可行） |
| 转化阶段制 | 久新现行 RULE_BASED_EVIDENCE_BASELINE | 证据计数组合规则 | 论文/专利/企业/项目计数 | **stage_assessment 38,860 行** | 中（现成，语义异构） |
| 文献计量 S 曲线 | 专利族/引用成熟曲线方法 | 时序拟合 | 长时序论文/专利 | gkx 有量无节点映射；久新 yearly_metrics 有 | 中（可算非现成） |
| 评分制 | UI mock 语义 | 综合评分模型 | 分值结果面 | 无（需映射假设） | 低（需口径裁定） |

### C.2 数据矩阵

| 依赖 | 行数/状态 | 覆盖/质量 | 缺口 |
|---|---|---|---|
| stage_assessment | 38,860 行/19,430 节点 | 双版本、两档覆盖 | 分值语义、年度序列 |
| transfer_stage | 8 行 | 定义完备 | — |
| profile.tech_id | UNMAPPED 全量 | — | 映射未发布 |
| region_yearly_metrics（深圳） | 15,630 行/6,233 节点 | 可用 | 选择偏置需披露 |
| TRL 证据链 | 无 | — | 源级缺失 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | 口径 B 百分制全域+深圳均值回填 KPI（随行披露两档覆盖/规则基线） | 甲方裁定 A1 等距映射 |
| v2 | 领域切片均值（domains_raw 临时轴，标注非受控） | 词表治理或接受临时轴 |
| v3 | 正式技术目录映射后的领域均值 + 年度序列 | mapping release + 年度化发布 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 72.45 被读作「技术平均 72 分成熟」 | **高** | 随行披露阶段制来源+两档覆盖事实 |
| 等距映射假设被默认为权威 | 中 | A1 裁定留痕；notes 写死「口径假设」 |
| 深圳切片选择偏置 | 中 | 披露「深圳证据命中筛选」前提 |
| 版本分歧未来出现 | 低 | 裁定「取最新 model_version」规则预留 |

### C.5 总判

**部分支持**：承载结构充足（38,860 行唯一结果面）但分值语义需口径假设、领域维映射未发布双因压档；升档路径（A1 裁定 + mapping release）写死在 §1.6 触发器，按 B10 保守交付。

## 附录 D　复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_TECHTRK_009.py` | 退出码 0，落 `_out.json` |
| 主表行数 | 产物 `jiuxin_stage_assessment_rows` | 38,860 |
| 口径 A | `jiuxin_avg_stage_order_8scale` | 6.0713 |
| 口径 B | `jiuxin_avg_maturity_pct_scale` | 72.4476 |
| 深圳切片 | `jiuxin_shenzhen_avg_maturity_pct_scale` | 82.8998 |
| 数据入口 | 久新只读直连 + `_gkxdb.py`（gkx） | demo_* 直接 raise |
| 正文产物一致 | 本 MD §2.8 对照表 | 逐键对齐 |
| 判档一致 | 文首 vs `support_judgment` | 均为部分支持 |
| 负证据探针 | 产物 absence_probe（gkx 2 件 + dev 1 件） | 有效命中 0 |
| mock 残留检查 | `rg "maturity.*72" repos/demo-ui-science/src/techDevelopmentTracking.js` | 正式版替换后 KPI 位无 mock 值 |
