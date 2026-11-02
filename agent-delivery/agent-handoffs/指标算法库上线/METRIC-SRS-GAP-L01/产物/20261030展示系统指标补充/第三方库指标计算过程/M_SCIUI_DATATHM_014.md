# 渠道历史同步成功率（M_SCIUI_DATATHM_014）

> **类型**：无业务逻辑数值类（历史归档批次成功占比读数）｜ **域**：科技信息展示系统·科技数据资源·接入视窗·历史资源接入情况（相邻叶语义锚：seq 360/361/362）｜ **UI 挂载**：科技信息展示系统 → 数据资源 → 接入视窗 → 历史资源接入情况 → 动态历史趋势可视化卡 → `AccessHistorySituation.jsx:298`（Statistic title="历史成功率" suffix="%"，绿色读数位）
> **数据支持度**：**完全不支持**｜ **公式定义人**：无（需求文档未出现指标名；相邻叶 seq 360「详细记录相关资源的接入历史」只述记录功能、成功率口径无）｜ **口径归属**：UI 读数位拆件（无独立需求叶），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_DATATHM_014.py`｜ **产物**：`code/M_SCIUI_DATATHM_014_out.json`
> **四判定摘要**：直接结构 = 无（三源无渠道×表×时间的归档台账——access_history/sync_log/collect_log/ingest 词族 dev 542 表/gkx 280 表/久新 210 张 0 命中）；直接数据 = 无（同左）；依赖结构 = 部分（dev 有 es_sync_watermark 同步动作快照面 + xxl_job 调度框架表族结构在）；依赖数据 = 无（es_sync_watermark 15 行是单模块最后一笔快照非历史批次序列；xxl_job_log/log_report/sys_job_log 实查 0 行空载）
> **数据源口径**：三源（开发库 live `gkxlumenx_*` 非 demo + 三方库 gkx + 久新 `gkx_technology_analysis_dev`）逐一探针留证；`demo_*` 禁引。

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全不支持。** 指标语义是「历史归档批次的成功占比」——分子=成功归档记录数、分母=归档记录总数，两个量都要求**渠道×数据表×时间的归档台账**存在。三源逐一排除：dev 16 schema 542 表 access_history/sync_log/collect_log/ingest_log 词族 0 命中（sync 词族唯一命中 `gkxlumenx_cfg.es_sync_watermark`——单模块**最后一笔**的快照面，无历史批次序列、无渠道维度）；gkx 280 表同词族 0 命中（job 词族唯一命中 `dwd_job`=招聘岗位明细表 10 行，语义排除）；久新 210 张 ads_* 同词族+任务词族（task/schedul/frequen/interval/batch/refresh/job/run/exec）0 命中（run 词族唯一命中 `ads_recommendation_run`=推荐系统运行表，语义排除；ads_* 按 metrics_as_of_date 快照管理，无逐笔同步日志）。dev 调度框架面（xxl_job_log/xxl_job_log_report/sys_job_log）结构在但实查 0 行空载——调度器从未在该环境跑过任务，无历史执行流水。快照代理面 es_sync_watermark 15 行（14 success/1 failed）给出「模块快照成功率 93.33%」读数，但语义是**模块当前健康度**非**渠道历史批次成功率**，且 15 行含 1 行键名含 demo（reg_info_demo，登记不引用），不足以承载历史口径。判完全不支持（台账面三源零承载 + 代理面语义错位 + 空载）。

### 批次通用纪律摘要（S3-04 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 93.33% 分子分母同表同 WHERE（14/15，es_sync_watermark 全量） |
| B4 | 负结论带探针 | 四件 absence_probe（dev/gkx/jiuxin/doc，§3.3） |
| B5 | 确定性 | 词族固定顺序；状态分布按 sync_status 排序 |
| B6 | 闸门自身被闸 | 不自跑闸门，派单方统一 |
| B7 | 产物只由脚本产出 | 改脚本→重跑；产物零手改 |
| B8 | 回执不复收 | 探针 SQL 幂等可复验 |
| B9 | 单位/日期陷阱 | last_sync_time 直接字符串化，无日期比较 |
| B10 | 口径裁定保守交付 | 快照代理语义错位披露写死；升档触发器写死（§1.6） |
| B11 | 多本账互推 | dev 542 表/gkx 280/久新 210 与共享快照 `_probe_lane3_s304_out.json` 一致 |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有渠道归档台账吗？ | 无 | access_history/sync_log 词族三源 0 命中（§3.3） |
| 调度框架日志能当台账吗？ | 不能 | xxl_job_log/log_report/sys_job_log 实查 0 行（§3.3） |
| es_sync_watermark 快照能当历史序列吗？ | 不能（语义错位） | 单模块最后一笔快照，无批次时间序列（§3.2） |

## 摘要

「渠道历史同步成功率」是历史资源接入情况仪表盘五读数位的第四位（`AccessHistorySituation.jsx:298` Statistic「历史成功率」），mock 源 `mockData.js:1423-1430` 给 75.0%（12 条归档记录中 7 成功/3 部分成功/2 失败的演示口径）——前端把它渲染为绿色 KPI，语义是「历史归档批次的成功占比」。数据侧判定核心是渠道×表×时间的归档台账：三源逐一排除（dev 542 表/gkx 280 表/久新 210 张同步日志词族 0 命中），dev 调度框架 xxl_job 三张日志表实查 0 行空载；唯一沾边的 `es_sync_watermark`（15 行）是模块级同步水位快照（14 success/1 failed），语义错位且体量不足。判**完全不支持**：台账零承载 + 代理面语义错位双因。脚本已跑通，产物与正文数字逐一对应。

- 需求判定：指标名未出现于三份需求真源（UI 读数位拆件）；相邻叶 seq 360「详细记录相关资源的接入历史」功能在、成功率口径无。
- 复现状态：脚本已跑通；三源排除探针 + es_sync 快照读数全落产物。
- 档位结论：**完全不支持**（归档台账三源零承载 + 快照代理语义错位 + 调度日志空载）。
- 关键事实：xxl_job_log 结构完整（trigger_code/handle_code/trigger_time/handle_time 列族在）但 0 行——「有骨架无血肉」是本件最典型的排除证据。
- 升档路径：建渠道归档台账（渠道×表×批次×状态）→ 完全直接支持（触发器①）；xxl_job 调度器投产产生执行流水 → 完全转换支持（触发器②）。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技数据资源/接入视窗/历史资源接入情况/**动态历史趋势可视化卡的「历史成功率」读数位**（无独立需求叶；相邻叶 1.1.1.1.4.4.2.4.1-4.3，SRS seq 360-362）。UI 实际容器是 `AccessHistorySituation` 组件「动态历史趋势可视化」卡（Card title 带 DashboardOutlined 图标，extra 标注「接入量 · 更新状况 · 异常分布」）五读数行的第四位：`AccessHistorySituation.jsx:298` `<Statistic title="历史成功率" value={summary.successRate} suffix="%" valueStyle={{ color: '#00b42a' }} />`——绿色百分比读数；数据源是 mock `mockData.js:1423-1430` 的 `historyAccessDashboard.summary.successRate: 75.0`（同 summary：archiveCount 12/channelCount 5/tableCount 12/anomalyCount 5）。mock 注释自标「历史资源接入仪表盘（需规 seq 362）」——即该 KPI 组挂在 seq 362 动态历史趋势可视化叶下，是前端对「历史资源接入量、更新状况」的读数化演绎。同组件 `getTrendOption()`（`:70-121`）的「更新成功率%」折线（mock 序列 94.2→97.5）是本指标的时间序列形态，与 031 件（渠道×成功率表格）同源异构。

### 1.2 为什么需要本指标

接入视窗的管理闭环需要「回看质量」：归档记录数看规模（archiveCount）、渠道数看结构（channelCount）、历史成功率看**质量**——归集动作有多少比例成功落库，是接入运营的核心健康度读数。需求把它放在历史资源接入情况的仪表盘读数行（seq 362 叶的 summary 组）：绿色=达标、红色（异常归档数）=待治理，双色并排构成接入质量的「温度计」。官方对应物是 R1 汇交体系的「先汇交、再验收」机制：汇交成功率（按时完整汇交的项目占比）是科技计划验收的硬指标；R2/R3 的数据工程 SLA 口径（成功率=成功请求/有效请求总数）是本指标的方法学同构——分母是「做过的事」，分子是「做成了的事」，渠道维度是切片轴。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「渠道历史同步成功率」指标名在三份需求真源（主需求/核增需求/算法库）0 命中（附录 A.2）。相邻叶的主需求 :2655（seq 360 渠道名称与表名称历史归集记录）只述「自动归档每个数据接入渠道和对应的数据表，详细记录相关资源的接入历史」——记录功能在，但「成功率」的分子分母口径（批次粒度？记录粒度？成功判定标准？）无任何定义。UI 的 75.0% 是前端演示约定（12 条中 7+3+2 状态分布的某种聚合），不构成口径证据。

### 1.4 类似指标权威方法可行性分析概要

「同步/归档成功率」的权威方法锚分三层。其一，国家科学数据汇交体系（R1）：GB/T 39912-2021 规定汇交流程各环节留痕（提交/审核/编目/维护更新），汇交成功率=按期完整汇交项目/应汇交项目——**制度化形态正是归档台账**（谁、何时、交了什么、成功与否）。其二，数据工程 SLA 口径（R2/R3）：request-based 可用性 = 成功请求/有效请求总数（AWS 白皮书 A = 成功处理工作单元/接收的有效工作单元；Azure SLA 同构），调度场景下工作单元=同步任务批次。其三，UI 演示框架（75.0% 单读数+趋势折线）：KPI+时序双形态。方法族对照：

| 方法族 | 代表 | 分子/分母 | 数据要求 | 与三源匹配 |
|---|---|---|---|---|
| 汇交台账口径 | R1（GB/T 39912） | 按期完整汇交/应汇交 | 归档台账 | **无台账** |
| 请求成功率口径 | R2/R3（AWS/Azure SLA） | 成功批次/总批次 | 任务执行日志 | **日志空载**（xxl 0 行） |
| 模块快照口径 | dev es_sync_watermark | 成功模块/模块总数 | 同步水位表 | **语义错位**（无历史序列） |
| 前端演示 | UI 75.0% | mock 聚合 | mock 常量 | 结构披露（不作源） |

结论：权威两口径（台账/执行日志）一个零承载一个空载，快照口径语义错位。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/data-resources/components/AccessHistorySituation.jsx:298`（Statistic 位）、`:70-121`（getTrendOption 更新成功率折线）；mock 语义源 `mockData.js:1423-1430`（historyAccessDashboard.summary，注释自标「需规 seq 362」）。
- SRS：`bid-reference/srs/02-科技信息展示系统/科技数据资源/接入视窗.md` seq 360-362（相邻叶语境），原文见附录 A。
- 主需求：`科技信息展示系统和科技专题服务系统.md`:2653-2665（历史资源接入情况 L5 段），原文见附录 A。
- 权威方法：R1 GB/T 39912-2021（std.samr.gov.cn）；R2 AWS 可用性白皮书（docs.aws.amazon.com）；R3 Azure SLA 指南（learn.microsoft.com）。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**推测定义（须披露口径不闭合）**：按 UI 语义（summary.successRate 与异常归档数并排）与相邻叶语境：

$$\text{SR}_{hist} = \frac{\text{成功归档记录数}}{\text{归档记录总数}} \times 100\%$$

其中归档记录=渠道×数据表的一次接入/更新动作（粒度待甲方裁定：批次级或记录级；mock 12 条记录中 success 7/partial 3/failed 2 的演示分布提示记录级，但 partial 是否计分子无定义）。**前提是归档台账存在，三源实测无**（§3.3）。

**降档/升档触发器（B10 模板）**：①建渠道归档台账（渠道×表×批次时间×状态×记录数）→ 直查升**完全直接支持**；②xxl_job 调度器投产、`xxl_job_log` 产生真实执行流水（trigger_code/handle_code 可直接算成功率，列结构已勘明）→ 转换升**完全转换支持**；③甲方裁定快照口径可代理（es_sync_watermark 模块健康度冒充历史成功率）→ 仍语义错位不升档（本报告不建议）。维持现状 → 完全不支持。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技数据资源/接入视窗.md` |
| 所属 L5 | 历史资源接入情况（1.1.1.1.4.4.2.4，4 叶：seq 360-363） |
| 本件定位 | UI 读数位拆件（挂在 seq 362 动态历史趋势可视化卡的 summary 组）——**无独立需求叶** |
| 相邻叶 | 渠道名称与表名称历史归集记录（360，台账语境）/ 历史更新周期统计与分析（361，019 件的锚）/ 动态历史趋势可视化（362，DATAIN_001 件的锚） |
| 同组件族件 | DATATHM_031（各渠道数据同步成功率——同组件 :417 表格列，渠道×成功率分列形态）；DATATHM_019（平均周期，:415 列） |
| UI 容器 | `AccessHistorySituation.jsx:298`（五读数行第四位） |

本件与 031 构成「成功率双件」：**014 是总口径单读数**（历史成功率的 KPI 位，不分渠道）、**031 是渠道分列口径**（每渠道一行的表格形态）——两件 UI 挂载点同组件相邻（:298 vs :417）、mock 数据同源（historyAccessDashboard vs updateCycleStats）、语义同物（归档/同步成功占比）仅聚合粒度不同（总体 vs 分渠道）。**判定两件为同物异构**：MD 互引 + 合并建议登记（两件均判完全不支持、缺口同根——归档台账/同步日志面，一次立项两件闭合；若甲方认定「总体 KPI」与「渠道分列」为两个交付位，则保留两件、口径裁定一次共用）。与 019（平均周期）同挂 mock `updateCycleStats` 表格族，三件共用台账缺口。

## 二、计算过程

从缺。归档台账与任务执行日志三源零承载（§3.3 探针全记录），快照代理面语义错位（模块健康度≠历史批次成功率），无法构建任何合法计算链；伪公式与探测 SQL 不进本区（F4）。

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 渠道归档台账（渠道×表×时间×状态） | 三源 | — | — | **不存在** | **缺（主降档因）** |
| D2 | 任务执行流水 | dev | `xxl_job_log`（trigger_code/handle_code 列族） | 0（空载） | 结构在数据无 | **缺（空载）** |
| D3 | 日汇总面 | dev | `xxl_job_log_report`（suc_count/fail_count） | 0（空载） | 结构在数据无 | **缺（空载）** |
| D4 | 同步水位快照（代理） | dev | `es_sync_watermark.sync_status` | 15（14 success/1 failed） | 直查 | **有但语义错位** |
| D5 | UI 演示值 | UI | mockData historyAccessDashboard | — | mock | 边界证据（不作源） |

`support_judgment="完全不支持"`、产物与文首一致。

### 3.2 D4 快照面的读数与语义边界

`gkxlumenx_cfg.es_sync_watermark` 15 行（`dev_es_sync_watermark_rows=15`）：14 行 sync_status='success'、1 行 'failed'（reg_info 模块，retry_count=1，`dev_es_sync_failed_modules`）——派生键 `es_sync_snapshot_success_rate_pct=93.33`（分子 14/分母 15，同表同 WHERE，B3）。但三点语义边界写死：其一，**单模块一行**——每模块只保留最后一笔同步的水位（module_name 主键式），历史批次序列不存在，「历史成功率」的时间维从根上缺；其二，**无渠道维度**——module_name 是业务域（bid/patent/news/finance 等 15 个），与「API 接口/文件传输/数据库同步」渠道枚举无映射；其三，**15 行含 1 行键名含 demo**（reg_info_demo，`dev_es_sync_rows_with_demo_in_module_name`，其 189,115 计数不进任何分子分母——披露但整行不引用）。该面能回答「哪些模块当前同步健康」，不能回答「历史批次成功占比」。

### 3.3 D1/D2/D3 的 absence_probe 全记录

否定性证据三件套：**查了什么**——①dev 16 schema 542 表 access_history/sync_log/collect_log/ingest_log 词族（0 命中；sync 词族唯一命中 `gkxlumenx_cfg.es_sync_watermark` 已单列语义核对，job 词族命中 21 张调度框架表族——xxl_job_log/xxl_job_log_report/sys_job_log 三张日志表实查 **0 行**，`dev_xxl_job_log_rows=0`/`dev_xxl_job_log_report_rows=0`/`dev_sys_job_log_rows=0`，`xxl_job_info` 任务注册面同 0 行——调度器从未投产）；②gkx 280 表 sync/channel/cycle/etl/ingest/pipeline 词族（0 命中；job 词族唯一命中 `dwd_job`=招聘岗位明细表 10 行——job=职位语义，语义排除）；③久新 210 张 ads_* 两轮词族（sync/channel/cycle/etl/ingest/pipeline + task/schedul/frequen/interval/batch/refresh/job/run/exec；run 词族唯一命中 `ads_recommendation_run`=推荐系统运行表，语义排除；ads_* 全库按 metrics_as_of_date 快照管理——每期全量重刷，无逐笔同步日志留存）；④三份需求真源（指标名 0 命中，相邻叶功能在口径无）。**条件**——表级存在性+语义核对（词族命中须过语义关）。**命中**——0（语义级）。四缺失情形归属：D1 属「**表不存在**」（台账三源均无——修复动作是建表立项）；D2/D3 属「**表存在但 0 行**」（调度框架表族结构在、空载——修复动作是调度器投产+任务注册，非建表）。

### 3.4 现场复核清单

| 复核项 | 结果 |
|---|---|
| dev 同步日志词族 | 0 命中（es_sync_watermark 单列） |
| dev 调度日志三表 | xxl_job_log 0 / log_report 0 / sys_job_log 0（空载） |
| dev es_sync 快照 | 15 行（14 success/1 failed；1 行键名含 demo 登记不引用） |
| gkx 词族 | 0 命中（dwd_job 招聘语义排除） |
| 久新两轮词族 | 0 命中（ads_recommendation_run 语义排除） |
| 快照面派生 | 93.33%（14/15，同表同 WHERE） |
| 脚本形态 | 三源串行只读；零 demo_* 值引用 |

## 四、数据缺失情况

### 4.1 渠道归档台账零承载（结构级，主因）

「历史成功率」的计算前提是归档动作有台账（渠道×表×批次时间×状态×记录数）。三源实测零承载（§3.3）——与 DATAOV_002/DATAIN_001 的接入流水缺口同根：数据工程的操作层事件（ETL 批次、同步任务、归档动作）从未在库内留痕。**四缺失情形归属「表不存在」**：修复动作是归档台账建设，与 DATAOV_001 资产目录、DATAOV_002 接入流水台账同族可并项——目录记资产、流水记动作、台账记批次结果，三表构成数据资源管理的最小元数据对（本件与 031/019 共用此缺口）。

### 4.2 调度框架空载（数据级，次因）

dev 的 xxl_job 调度框架表族结构完整（`xxl_job_log` 17 列含 trigger_code/handle_code/trigger_time/handle_time——正是成功率所需的全部字段；`xxl_job_log_report` 的 suc_count/fail_count 日汇总列设计就是成功率的预聚合面），但三张日志表+任务注册面实查全 0 行。**四缺失情形归属「表存在但 0 行」**：修复动作不是建表而是**调度器投产**——任务注册（xxl_job_info 写入数据同步任务）+执行留痕后，成功率可由 handle_code 直接聚合（转换路径现成）。这与 4.1 的修复动作完全不同（建表 vs 投产），分开登记。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 归档台账建设 | 数据工程立项 | 本件 + 031 + 019 + DATAOV_002 + DATAIN_001/003 | 触发器①（族级共用，一次立项六件受益） |
| xxl_job 调度器投产 | 运维动作 | 本件 + 019（执行时长→周期） | 触发器②（列结构已勘明，投产即转换支持） |
| 快照面改名展示 | 展示规范 | 本件 | es_sync 93.33% 只能标「模块健康度」不得标「历史成功率」 |

档位后果：台账建成 → **完全直接支持**；调度器投产 → **完全转换支持**；现状 → 完全不支持。推荐顺序：台账立项为主线（族级并项），调度器投产随数据管道工程推进，快照面即期可作内部健康度参考（标签改写零成本）。

## 参考文献

1. 科技计划形成的科学数据汇交 技术与管理规范：GB/T 39912-2021[EB/OL]. 全国标准信息公共服务平台. https://std.samr.gov.cn/gb/search/gbDetailed?id=BD89DE8E06AC3D08E05397BE0A0A4FAD （R1，2026-11-01 WebSearch 核验可达——汇交流程各环节留痕与「先汇交、再验收」机制，归档台账口径的制度化形态）
2. Measuring availability[EB/OL]. AWS Architecture Blog Whitepaper. https://docs.aws.amazon.com/whitepapers/latest/availability-and-beyond-improving-resilience/measuring-availability.html （R2，2026-11-01 WebSearch 核验可达——request-based 可用性 A = 成功处理工作单元/接收的有效工作单元，任务批次成功率的方法学同构）
3. How to read a Service-Level Agreement (SLA)[EB/OL]. Microsoft Learn. https://learn.microsoft.com/en-us/azure/reliability/concept-service-level-agreements （R3，2026-11-01 WebSearch 核验可达——time-based vs request-based 两口径与聚合范围界定，成功率分母口径的权威参照）

# 附件

## 附录 A 原始需求原文摘录

指标名「渠道历史同步成功率」在三份需求真源 0 命中。相邻叶语境（本指标 UI 挂载的语义锚）：

SRS《02-科技信息展示系统/科技数据资源/接入视窗.md》seq 360（excel_row 363）：

> ### 渠道名称与表名称历史归集记录 · 序号 360
> #### 需规功能描述
> 自动归档每个数据接入渠道和对应的数据表，详细记录相关资源的接入历史，便于用户快速查找和比对不同渠道、表格的历史数据归集情况。

主需求《科技信息展示系统和科技专题服务系统.md》:2655（1.1.1.1.4.4.2.4.1）同文；:2653（L5 总述）「自动归集并展示不同渠道名称和表名称下的历史归档数据」。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 渠道历史同步成功率 | 主需求 | 0 |
| 渠道历史同步成功率 | SRS 接入视窗.md | 0 |
| 同步成功率 | 主需求/SRS/核增/算法库 | 0 |
| 历史成功率 | UI AccessHistorySituation.jsx | :298（Statistic 位）；mockData.js:1428（75.0 演示值） |
| 历史归集记录（相邻叶） | SRS 接入视窗.md | seq 360（台账语境锚） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_DATATHM_014_out.json`（2026-11-01 实跑：三源排除探针 + es_sync 快照读数）。
- 共享探针：`code/_snapshots/_probe_lane3_s304_out.json`（三源词族+调度表结构）、`_probe_lane3_s304b_out.json`（es_sync_watermark 15 行全量）、`_lane7_shared_probe_out.json`（dev 542/gkx 280/久新 210 表清单——B11 锚）。

### B.2 本件产物逐键清单（`code/M_SCIUI_DATATHM_014_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `facts.dev_table_total` | 计数 | 542 | §3.3 |
| `facts.dev_sync_family_tables` | 探针 | ['gkxlumenx_cfg.es_sync_watermark'] | §3.3 |
| `facts.dev_xxl_job_log_rows` | 计数 | 0（空载） | §3.3/§4.2 |
| `facts.dev_xxl_job_log_report_rows` | 计数 | 0（空载） | §3.3 |
| `facts.dev_sys_job_log_rows` | 计数 | 0（空载） | §3.3 |
| `facts.dev_es_sync_watermark_rows` | 计数 | 15 | §3.2 |
| `facts.dev_es_sync_status_dist` | 分布 | [['failed',1],['success',14]] | §3.2 |
| `facts.dev_es_sync_failed_modules` | 明细 | reg_info（retry 1） | §3.2 |
| `facts.dev_es_sync_rows_with_demo_in_module_name` | 披露 | ['reg_info_demo']（整行不引用） | §3.2 |
| `facts.gkx_table_count` | 计数 | 280 | §3.3 |
| `facts.gkx_sync_channel_family_tables` | 探针 | {'job': ['dwd_job']}（语义排除） | §3.3 |
| `facts.jiuxin_table_count` | 计数 | 210（2026-11-01 探测日） | §3.3 |
| `facts.jiuxin_task_family_tables` | 探针 | {'run': ['ads_recommendation_run']}（语义排除） | §3.3 |
| `derived[0].es_sync_snapshot_success_rate_pct` | 派生比 | 93.33（14/15） | §3.2 |
| `absence_probe` | 探针 | 四件（dev/gkx/jiuxin/doc） | §3.3 |
| `support_judgment` | 判档 | 完全不支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 分子/分母 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| 汇交台账口径 | R1（GB/T 39912） | 按期完整汇交/应汇交 | 无台账 | 高（目标态） |
| 请求成功率口径 | R2/R3（AWS/Azure） | 成功批次/总批次 | 日志表空载（0 行） | 高（结构在） |
| 模块快照口径 | dev es_sync_watermark | 成功模块/模块总数 | 15 行（语义错位） | 低（无历史维） |
| 前端演示 | UI 75.0% | mock 聚合 | mock 常量 | 结构披露（不作源） |

### C.2 数据矩阵

| 依赖 | gkx | dev | jiuxin |
|---|---|---|---|
| 渠道归档台账 | 无 | 无 | 无（快照管理无逐笔日志） |
| 任务执行流水 | 无 | **结构在 0 行**（xxl_job_log 17 列） | 无 |
| 同步水位快照 | 无 | **15 行**（无历史维） | 无 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v0（现状） | 快照健康度内部参考（标签「模块健康度」） | — |
| v1 | xxl_job 投产 → handle_code 聚合成功率 | 触发器② |
| v2 | 归档台账建成 → 渠道×表×批次直查 | 触发器①（族级并项） |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| es_sync 93.33% 被冒充「历史成功率」 | **高** | §3.2 三点语义边界写死；标签改「模块健康度」 |
| reg_info_demo 行泄入分子分母 | 中 | 产物披露键+不引用注记（§3.2） |
| 台账/调度两缺混同 | 中 | §4.1/§4.2 分立（建表 vs 投产） |

### C.5 总判

**完全不支持**：渠道归档台账三源零承载（结构级）+ 调度日志空载（数据级）+ 快照代理语义错位（方法级）三层叠加。xxl_job_log「17 列结构完整但 0 行」是本件最有信息量的探针结论——成功率的数据管道设计已在（列就是按成功率口径设计的），缺的是投产动作；这与台账的「表都不存在」是两种完全不同的修复路径，登记为两条触发器。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_DATATHM_014.py` | 退出码 0，落 `_out.json` |
| 数据入口 | 直连 dev + 共享探针快照 | demo_* 直接 raise（_gkxdb 未用值） |
| 判档一致 | 文首 vs `support_judgment` | 完全不支持 |
| B11 对账 | dev 542/gkx 280/久新 210 = 共享快照 | 零漂移 |
| 幂等重跑 | SQL 全只读无随机；状态分布按键排序 | 逐位一致 |
| 伪值残留 | 无成功率伪值（93.33% 明确标注快照口径） | 无 |
| 同物异构互引 | 031（渠道分列形态） | §1.7 合并建议登记 |
