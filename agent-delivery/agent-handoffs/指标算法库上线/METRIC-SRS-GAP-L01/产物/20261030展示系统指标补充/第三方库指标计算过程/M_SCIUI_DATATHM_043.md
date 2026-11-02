# 同步异常数（期）（M_SCIUI_DATATHM_043）

> **类型**：无业务逻辑数值类（逐次运行日志三源零承载，模块级当前状态可附带交付）｜ **域**：科技信息展示系统·科技数据资源·接入视窗·历史资源接入情况·动态历史趋势可视化「异常数」折线+「异常归档」读数（挂靠 seq 362）｜ **UI 挂载**：科技信息展示系统 → 数据资源 → 接入视窗 → `components/AccessHistorySituation.jsx:112`（series name='异常数' line）｜ 复读位 `:305-309`（Statistic 异常归档 anomalyCount）
> **数据支持度**：**完全不支持**｜ **公式定义人**：无（三份需求说明书未出现「同步异常数」；seq 362 功能句「动态跟踪……异常情况的历史变化」在——异常判定/计数口径/期定义无）｜ **口径归属**：UI 派生读数（挂靠 seq 362），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_DATATHM_043.py`｜ **产物**：`code/M_SCIUI_DATATHM_043_out.json`
> **四判定摘要**：直接结构 = 无（逐次运行日志三源零承载——xxl_job_log 0 行空载体、es_sync_watermark 单笔状态快照非序列、gkx 0 命中、久新 2 张语义排除）；直接数据 = 无（同左）；依赖结构 = 部分（本件新探针：es_sync_watermark 有 sync_status/error_msg/retry_count 三列——状态结构在）；依赖数据 = 部分（排除 demo 后 14 模块实测 13 success + 1 failed（reg_info，RuntimeError 5 万 build/bulk 错误）——当前状态快照可读，但单笔状态≠期计数）
> **数据源口径**：三源（开发库 live `gkxlumenx_*` 非 demo + 三方库 gkx + 久新 `gkx_technology_analysis_dev`）逐一探针留证；`demo_*` 禁引（es_sync 的 reg_info_demo 模块按纪律排除、行内披露）。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全不支持。** 语义是「同步任务在期内的异常运行次数」——计数原料是**逐次运行日志**（任务×时间×状态序列）。三源逐一排除：**dev** `xxl_job_log` **0 行**（xxl_job_info/xxl_job_group 同为 0——调度器全链空载体，列族结构在零数据）；`es_sync_watermark` 有状态三列（sync_status/error_msg/retry_count，本件新探针）且实测有真实 failed——但每模块仅保留**最后一笔状态**（15 行=15 模块各 1 行），是状态快照非运行日志：无时间序列、无失败历史，「期」计数撑不起；**gkx** 280 表 sync/cycle/frequen/watermark 词族 0 命中；**久新** 215 表命中 `ads_research_problem_update_signal`/`ads_scientific_update_signal`（科研内容更新信号面，语义排除）；「期」维全库无承载（041 同法）。附带交付：模块级当前状态读数（排除 demo 后 14 模块 13 success + 1 failed——reg_info，`RuntimeError: reg_info slice has 50000 build/bulk errors`，retry_count=1）——该读数是快照语义非期口径，可作即期监控参考、不得充「异常数（期）」。`sync_anomaly_count_period = null`（B10）。

### 批次通用纪律摘要（S3-05 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 附带键分子=failed 1、分母=14 模块（同基同源） |
| B4 | 负结论带探针 | 五件 absence_probe（xxl/es_sync/gkx/jiuxin/doc，§3.3） |
| B5 | 确定性 | 状态分布按状态名排序；failed 明细按模块名排序 |
| B6 | 闸门自身被闸 | 不自跑闸门，派单方统一 |
| B7 | 产物只由脚本产出 | 本件 py 已跑出 _out.json；产物零手改 |
| B8 | 回执不复收 | 探针 SQL 幂等可复验 |
| B9 | 单位/日期陷阱 | error_msg LEFT(120) 截断披露；demo 模块行内披露词 |
| B10 | 口径裁定保守交付 | 期口径 null；快照读数标签写死「非期口径」；触发器写死 |
| B11 | 多本账互推 | xxl 三表 0 行=019；es_sync 15 行=019/046（状态三列新读数 044 复用） |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有逐次运行日志吗？ | 无 | xxl 0 行；es_sync 单笔快照（§3.3） |
| 状态列实测有 failed 吗？ | 有（1/14，非 demo） | reg_info failed（§3.2） |
| 单笔状态能当「期计数」吗？ | 不能 | 快照无失败历史（§3.3 专段） |

## 摘要

「同步异常数（期）」挂在历史资源接入情况·动态历史趋势可视化卡：`AccessHistorySituation.jsx:112` 是三序列混合图的「异常数」右轴折线（mock trend.anomalyCount 六点 18→8 递减），`:305-309` 是汇总行「异常归档」Statistic（mock 5 条），mock 另有 anomalyByType 四类分布（同步延迟 2/接口错误 1/数据缺失 1/格式异常 1）。数据侧：「期」计数的原料是逐次运行日志——dev 调度器全链空载体（xxl 三表 0 行）、es_sync_watermark 是单笔状态快照；**本件新探针实测发现状态三列真实有值**：排除 demo 模块后 14 模块 13 success + 1 failed（reg_info，RuntimeError 5 万 build/bulk 错误、重试 1 次）——这是接入链路真实存在的异常证据，但它是「当前状态」不是「期计数」。判**完全不支持**（期口径三源零承载），附带交付模块级状态快照读数。脚本已跑通，产物与正文数字逐一对应。

- 需求判定：**UI 派生读数**（挂靠 seq 362；异常判定/计数/期定义无）。
- 复现状态：脚本已跑通；xxl 空载体 + es_sync 状态三列新探针 + failed 明细全落产物。
- 档位结论：**完全不支持**（逐次运行日志三源零承载；单笔状态快照附带交付）。
- 关键事实：reg_info 模块 failed 是接入链路唯一真实异常证据（`RuntimeError: reg_info slice has 50000 build/bulk errors`）——它同时说明 es_sync 状态列是被真实维护的（非摆设），缺的只是逐次留痕的序列语义。
- 升档路径：xxl 调度器实装留日志 → 完全直接支持；es_sync 改逐次留痕 → 完全转换支持（模块级）。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技数据资源/接入视窗/历史资源接入情况（1.1.1.1.4.4.2.3，挂靠 seq 362——组件注释自标「需规 seq 360/362/363」）·动态历史趋势可视化卡。UI 实际挂载（派单 mount 行 112，实查确认）：`AccessHistorySituation.jsx:70-121` getTrendOption 三序列——「异常数」line（:111-118，右轴 dashed 红线）；同卡汇总行「异常归档」Statistic（:303-310，`value={summary.anomalyCount}` suffix="条" 红色）；同卡右路「异常分布」柱图（:145-165 getAnomalyBarOption，消费 anomalyByType 四类）。mock 语义源 `mockData.js:1422-1449`：summary.anomalyCount=5 + trend.anomalyCount=[18,16,14,12,10,8] + anomalyByType（同步延迟 2/接口错误 1/数据缺失 1/格式异常 1）。mock 结构披露：三组演示值内部自洽（byType 合计=summary 5），但 trend 六点（18-8）与 summary 5 是两个量纲（期序列 vs 累计）——演示形态自洽但库内无承载，不作数据证据（B10）。

### 1.2 为什么需要本指标

同步异常数是接入链路的**质量告警读数**：管理者按期回看异常次数与类型分布（trend 折线+byType 柱图），识别接入链路的稳定性风险（接口错误=源端故障、同步延迟=吞吐瓶颈、格式异常=契约变更、数据缺失=源端缺数）。权威对应物是 ETL/调度系统的作业失败监控（R2，Airflow ti_failures 指标——任务实例失败计数按 dag/task 打标；R1，GB/T 36344 数据质量监控框架）——工程口径的原料都是**逐次运行日志**（每次同步一条记录：开始/结束/状态/错误）。

### 1.3 需求文档是否给出定义方法

**三份需求说明书未出现「同步异常数」。**「异常数」是 UI 图例名（:112）；「异常归档」是 Statistic 题名（:305）。挂靠叶 seq 362 功能句「动态跟踪接入量、更新成功率与异常情况的历史变化」——「异常情况」功能词在，但异常判定标准（何种状态算异常：失败？延迟？部分成功？）、计数口径（次数/任务数/记录数）、期定义（自然月？周？）均无。核增需求与算法库 0 命中（附录 A.2）。

### 1.4 类似指标权威方法可行性分析概要

「同步异常计数」的权威方法锚分三层。其一，调度监控口径（R2，Airflow）：`ti_failures` 计数器按 dag_id/task_id 打标逐次累计——成功率与失败数同源于任务实例日志；其二，数据质量监控（R1，GB/T 36344-2018）：数据质量评价指标框架含一致性/及时性监控——异常判定需先定义质量规则；其三，库内现状：es_sync_watermark 状态三列（sync_status/error_msg/retry_count）是模块级状态快照——结构上可判「当前是否异常」，无逐次序列不可计「期」。方法族对照：

| 方法族 | 代表 | 原料 | 与三源匹配 |
|---|---|---|---|
| 调度失败计数 | R2（Airflow） | 任务实例日志 | **无日志**（xxl 0 行） |
| 数据质量监控 | R1（GB/T 36344） | 质量规则+校验记录 | 无校验记录 |
| 状态快照判读 | 库内可行近似 | es_sync 状态三列 | **有结构有数据**（但非期口径） |
| 前端演示 | UI mock 三组 | mock | 结构披露（不作源） |

结论：权威口径的原料（任务日志）三源无；库内唯一可用面（状态快照）语义是「当前」非「期」。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/data-resources/components/AccessHistorySituation.jsx:112`（series line）、`:303-310`（异常归档 Statistic）、`:145-165`（异常分布柱图）；mock 语义源 `repos/demo-ui-science/src/pages/data-resources/mockData.js:1422-1449`。
- 需求：SRS `bid-reference/srs/02-科技信息展示系统/科技数据资源/接入视窗.md` seq 362。
- 权威方法：R1 GB/T 36344-2018（std.samr.gov.cn，数据质量评价）；R2 Apache Airflow Metrics（airflow.apache.org，ti_failures 口径）；R3 Prometheus ALERTS（prometheus.io，告警状态时序形态）。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**推测定义（须披露口径不闭合）**：按调度监控口径推测

$$A_t = |\{r: r.\text{status} \neq \text{success} \wedge t \in \text{period}(r.\text{ts})\}|$$

即期内状态非成功的运行记录数（Airflow ti_failures 的期窗聚合形态）。**前提是逐次运行日志存在（每次运行一条含时间戳与状态的记录），三源实测无**（§3.3）——es_sync 单笔快照只支持「当前异常模块数」（附带交付键），不支持期计数。公式列示仅作口径锚（F4：本件 §二 从缺）。

**降档/升档触发器（B10 模板）**：①xxl 调度器实装并留日志（handle_code≠200 逐次累计）→ 升**完全直接支持**；②es_sync 改逐次留痕（模块×时间×状态序列表）→ 升**完全转换支持**（模块级粒度）；③维持现状 → 完全不支持（期位暂无数据态；当前状态读数可作即期监控参考，标签「当前异常模块数」非「异常数（期）」）。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技数据资源/接入视窗.md` |
| 所属 L5 | 历史资源接入情况（挂靠 seq 360-363） |
| 本件 | **UI 派生读数**（异常序列位+异常归档读数位，挂靠 seq 362） |
| 同卡并列读数 | 042（历史接入量）/044（更新成功率——同卡成功率维，状态三列共享）/045（本期接入量） |
| 跨族近件 | 017（问题资源总数——问题口径同根）/019（渠道平均同步周期——es_sync 同源先例） |
| UI 容器 | `AccessHistorySituation.jsx:275-330` 动态历史趋势可视化卡 |

本件与 044 构成「运行质量双件」：043 取异常计数维、044 取成功率维——两件同源于「运行日志序列」，共享 es_sync 状态三列新探针（044 的分子分母直接复用本件状态分布）。与 019（渠道平均同步周期）构成 es_sync_watermark 三读数位：019 取耗时维（已判完全不支持）、本件取状态维、046 取模式维。

## 二、计算过程

从缺（逐次运行日志三源零承载——「期」计数不可构建；es_sync 状态三列是单笔快照非序列，见 §3.3。按 F4 纪律不写伪计算过程；附带交付的当前状态读数与排除证据进 §三/附录 B）。

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 逐次运行日志（任务×时间×状态） | 三源 | xxl_job_log / — / — | **0 行** / 无 / 无 | 空载体 | **缺（判定性）** |
| D2 | 状态快照（模块级当前状态） | dev | `es_sync_watermark.sync_status` 等 | 15 行（14 非 demo） | 直查 | **有**（快照语义，附带交付） |
| D3 | 异常类型轴 | 三源 | —（同步延迟/接口错误/数据缺失/格式异常四类为 UI 枚举） | — | **不存在** | 缺（判定标准无） |
| D4 | 期维（月/周序列） | 三源 | — | 无承载（041 同法） | **不存在** | 缺 |
| D5 | UI 演示值 | UI | mock 三组 | 5/18-8/四类 | mock | 边界证据（不作源） |

`support_judgment="完全不支持"`、产物与文首一致（闸 6）。

### 3.2 D2 状态快照读数（附带交付核心）

es_sync_watermark 状态三列实查（本件新探针）：全 15 行分布 success 14 + failed 1（`dev_es_sync_status_dist_all15`）；**排除 demo 模块后 14 行：success 13 + failed 1**（`dev_es_sync_status_dist_excl_demo`）。唯一 failed 明细（`dev_es_sync_failed_detail_excl_demo`）：模块 **reg_info**，`error_msg`（LEFT 120 截断）=`RuntimeError: reg_info slice has 50000 build/bulk errors`，`retry_count=1`——工商注册信息切片在 ES build/bulk 阶段 5 万条错误，重试 1 次后仍 failed。demo 模块披露（`dev_es_sync_demo_modules_disclosed`）：reg_info_demo=success——demo 前缀模块按纪律排除、行内披露。读数边界：这 1 个 failed 是**当前状态快照**（最后一笔同步的结果）——reg_info 历史上可能已失败多次（retry_count=1 只记最后一轮），「期内异常次数」不可从单笔推算。

### 3.3 D1 的 absence_probe 全记录（含快照≠序列专段）

否定性证据三件套：**查了什么**——①dev `gkxlumenx_job.xxl_job_log` COUNT=**0**（xxl_job_info=0/xxl_job_group=0——调度器全链空载体；xxl_job_log 列族 id/job_group/job_id/executor_address/executor_handler…结构在，属「表存在但数据为空」）；②dev `es_sync_watermark` 状态序列能力：**状态三列在**（sync_status/error_msg/retry_count）且实测有真实 failed——但 15 行=15 模块各 1 行，每模块仅最后一笔状态：**无时间序列、无失败历史**，是快照不是日志——「期」计数需要「该期内每次运行一条」，快照只有「现在一条」；③gkx 280 表 sync/cycle/frequen/watermark 词族 0 命中；④久新 215 表命中 2 张 update_signal（科研内容更新信号，研究对象错位，语义排除）；⑤三份需求真源（指标名 0 命中；seq 362 功能句在——异常判定/计数/期定义无）。**条件**——表级存在性+序列结构+语义三层核对。**命中**——0（期口径语义级）。四缺失情形归属：D1 属「**表存在但数据为空**」（xxl_job_log 结构在零行——修复动作是调度器实装或日志接入）；D3/D4 属「**表不存在**」（异常类型轴与期维无承载）。

### 3.4 现场复核清单

| 复核项 | 结果 |
|---|---|
| xxl 三表 | log/info/group = 0/0/0（调度器空载体） |
| xxl_job_log 列族 | 结构在（id/job_group/job_id/executor_*…） |
| es_sync 状态三列 | sync_status/error_msg/retry_count（本件新探针） |
| 状态分布（非 demo） | 14 模块：13 success + 1 failed |
| failed 明细 | reg_info：RuntimeError 5 万 build/bulk 错误，retry 1 |
| demo 模块披露 | reg_info_demo=success（行内披露排除） |
| gkx/久新词族 | [] / 2 张语义排除 |
| B9 | error_msg LEFT(120)；demo 披露词 |
| 脚本形态 | dev 直连实查；零 demo_*（demo 模块排除） |

## 四、数据缺失情况

### 4.1 逐次运行日志零承载（结构级，判定性缺口）

「异常数（期）」的原料是逐次运行记录（§1.6 公式的 r 序列）。dev 调度器全链空载体（xxl 三表 0 行——平台从未通过 xxl 跑过同步任务，或日志从未留存）；es_sync_watermark 是水位表设计（每模块覆盖式更新最后一笔），**设计上就不留存历史**。**四缺失情形归属两形态**：xxl「表存在但数据为空」（调度器实装即填）；es_sync「表存在、状态列在、序列语义不存在」（须改表或新建留痕表）。修复动作见触发器①②。

### 4.2 异常判定标准缺位（口径级，次因）

即便有日志，「什么算异常」也无定义：UI mock 的四类（同步延迟/接口错误/数据缺失/格式异常）是前端演示枚举；es_sync 状态只有 success/failed 两态（无「延迟」「部分成功」分级——xxl 的 handle_code 可细分但未实装）。正式口径需先裁定异常分级（失败/延迟/部分成功/超时），再定计数规则——这是 R1 数据质量监控框架的质量规则先行原则。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| xxl 调度器实装留日志 | 调度工程 | 本件 + 044 + 019 + seq 343-344 族 | 触发器①（运行日志族共用） |
| es_sync 逐次留痕表（模块×时间×状态） | 数据工程 | 本件 + 044 | 触发器②（模块级粒度） |
| 异常分级口径裁定（失败/延迟/部分） | 口径裁定 | 本件前置 | R1 框架先行 |
| UI 暂无数据态+当前状态参考位 | 展示规范 | 本件 | mock 5 条替换；reg_info failed 可作即期监控披露 |

档位后果：xxl 实装 → **完全直接支持**；es_sync 留痕 → **完全转换支持**；现状 → 完全不支持。推荐：xxl 实装为主线（与 044/019 三件共用），异常分级裁定先行（一纸文件）。

## 参考文献

1. 信息技术 数据质量评价指标体系：GB/T 36344-2018[EB/OL]. 国家标准全文公开系统. https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=A3B39F82FBD34B8CB85F10271B0CAD1A4 （R1，2026-11-01 WebSearch 核验可达——数据质量评价指标框架，异常判定的质量规则先行原则）
2. Metrics Configuration — Apache Airflow Documentation[EB/OL]. Apache Software Foundation. https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/logging-monitoring/metrics.html （R2，2026-11-02 WebSearch 核验可达——ti_failures/ti_successes 按 dag_id/task_id 打标的任务实例失败计数口径，逐次运行日志是原料）
3. ALERTS — Prometheus Query Docs[EB/OL]. Prometheus. https://prometheus.io/docs/prometheus/latest/querying/functions/ （R3，2026-11-01 WebSearch 核验可达——告警状态时序的监控形态参照）

# 附件

## 附录 A 原始需求原文摘录

三份需求说明书均未出现「同步异常数」。挂靠上下文原文：

SRS《02-科技信息展示系统/科技数据资源/接入视窗.md》seq 362（历史资源接入情况总览）：

> 支持长期数据接入历史的趋势展示与归档记录查询，动态跟踪接入量、更新成功率与异常情况的历史变化。

（「异常情况」功能词在；异常判定标准、计数口径、期定义无。）

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 同步异常数 / 同步异常 | 主需求/核增/算法库 + SRS 分册 | 0 |
| 异常数 | UI AccessHistorySituation.jsx | :112（图例名） |
| 异常归档 | UI AccessHistorySituation.jsx | :305（Statistic 题名，mock 5 条） |
| anomalyCount / anomalyByType | UI mockData.js | :1429/:1437-1442（mock 常量） |
| 异常情况…历史变化 | SRS 接入视窗.md seq 362 | 1（功能句） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_DATATHM_043_out.json`（2026-11-02 实跑：xxl 空载体 + es_sync 状态三列新探针 + failed 明细 + demo 排除披露）。
- 共享探针：`code/_probe_s305_l1_out.json`（L1 词族+xxl 计数+es_sync 形态）。
- 族内对账：xxl 三表 0 行=019 实测；es_sync 15 行=019/046；**状态三列实值为本批新读数**（044 复用分子分母）。

### B.2 本件产物逐键清单（`code/M_SCIUI_DATATHM_043_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `facts.dev_xxl_job_log_rows` | 计数 | **0**（空载体） | §3.3 |
| `facts.dev_xxl_job_info_rows` / `dev_xxl_job_group_rows` | 计数 | 0 / 0 | §3.3 |
| `facts.dev_xxl_job_log_cols` | 结构 | 列族在（结构证据） | §3.3 |
| `facts.dev_es_sync_cols` | 结构 | 15 列（含状态三列） | §3.2/§3.3 |
| `facts.dev_es_sync_status_dist_all15` | 分布 | success 14 + failed 1 | §3.2 |
| `facts.dev_es_sync_status_dist_excl_demo` | 分布 | **success 13 + failed 1（14 模块）** | §3.2 |
| `facts.dev_es_sync_failed_detail_excl_demo` | 明细 | reg_info failed（error_msg/retry） | §3.2 |
| `facts.dev_es_sync_demo_modules_disclosed` | 披露 | [reg_info_demo, success]（行内披露） | §3.2 |
| `facts.ui_mock_anomaly_count_summary` | mock | 5 | §1.1 |
| `facts.ui_mock_anomaly_trend` | mock | 6 点递减（18→8） | §1.1 |
| `facts.ui_mock_anomaly_by_type_sorted` | mock | 4 类（名称排序） | §1.1 |
| `derived[0]` | 附带 | sync_failed_module_count_current_snapshot = 1（分母 14） | §3.2 |
| `derived[1]` | 负结论 | sync_anomaly_count_period = null（B10） | §1.6 |
| `absence_probe` | 探针 | 五件（xxl/es_sync/gkx/jiuxin/doc） | §3.3 |
| `support_judgment` | 判档 | 完全不支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 原料 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| 调度失败计数 | R2（Airflow ti_failures） | 任务实例日志 | **无日志**（xxl 0 行） | 高（工程口径锚） |
| 数据质量监控 | R1（GB/T 36344） | 质量规则+校验记录 | 无校验记录 | 中（框架先行） |
| 状态快照判读 | 库内可行近似 | es_sync 状态三列 | **有结构有数据**（非期口径） | 中（即期监控参考） |
| 前端演示 | UI mock 三组 | mock | 内部自洽（库内无承载） | 结构披露（不作源） |

### C.2 数据矩阵

| 依赖 | dev | gkx | jiuxin |
|---|---|---|---|
| 逐次运行日志 | xxl 0 行（结构在） | 无 | 无（2 张语义排除） |
| 状态快照 | **13 success + 1 failed**（14 模块非 demo） | — | — |
| 异常类型轴 | 无（UI 四类为演示枚举） | 无 | 无 |
| 期维 | 无（041 同法） | 无 | 快照单日 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v0（现状） | 当前异常模块数参考读数（1/14，标签「非期口径」） | — |
| v1 | es_sync 逐次留痕 → 模块级期计数 | 触发器② |
| v2 | xxl 实装 → 任务级期计数+异常分级 | 触发器①+分级裁定 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 快照 1 failed 被当「异常数」充数 | **高** | 附带键标签写死「当前状态快照非期口径」 |
| mock 治理改善叙事误导 | 中 | §1.1 递减形态披露 |
| reg_info 错误被误读为数据丢失 | 低 | §3.2 error_msg 全文披露（ES build 阶段错误） |

### C.5 总判

**完全不支持**：逐次运行日志三源零承载（xxl 空载体+es_sync 快照无序列）；es_sync 状态三列真实有值（1/14 failed）可作即期监控参考但非期口径——运行日志族（本件+044+019）共享 xxl 实装触发器，一次建设三件升档。

## 附录 D　复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_DATATHM_043.py` | 退出码 0，落 `_out.json` |
| 数据入口 | dev 直连实查 | demo 模块排除（reg_info_demo 行内披露） |
| 判档一致 | 文首 vs `support_judgment` | 完全不支持 |
| B11 对账 | xxl=019；es_sync 15 行=019/046 | 零漂移 |
| 幂等重跑 | SQL 只读；状态分布确定性排序 | 逐位一致（活表状态可能变化——快照语义） |
| §二 从缺 | 完全不支持档 | 无伪公式（F4） |
| 伪值残留 | `sync_anomaly_count_period` | null（无伪值） |
