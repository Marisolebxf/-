# 异常数据监测（M_SCIUI_KGANALY_029）

> **类型**：无业务逻辑数值类（链路日志统计型）｜ **域**：科技信息展示系统·科技知识图谱·分析展示·功能面板·异常数据监测卡片｜ **UI 挂载**：`pages/tech-knowledge-graph/kgL6Functions.js:22`（异常数据监测卡片）；关联 `BlacklistTriggerPanel.jsx:147`、`IndicatorDisplay.jsx:33`、`mockData.js:285`
> **数据支持度**：**部分支持**（批量任务链路失败率——dev `gkxlumenx_cfg.lumen_analysis_task` 339 行真实日志满承载，33.92% 实算落产物；流式实时错误率承载缺失）｜ **公式定义人**：仿王惠（推测定义——UI 无算法实现，realtimeMonitor mock 0.8% 为演示常数，本件以任务链路失败率重建）｜ **口径归属**：需求明列叶（seq 408 异常数据监测/黑名单触发面板；row_01=492）
> **复现脚本**：`code/M_SCIUI_KGANALY_029.py`｜ **产物**：`code/M_SCIUI_KGANALY_029_out.json`（含总/剔取消双口径+23 日序列+错误归因 Top5）
> **四判定摘要**：直接结构 = 部分（dev 任务日志表结构在、流式监控面无）；直接数据 = 部分（339 任务真实日志 vs 实时错误率无）；依赖结构 = 部分（同左）；依赖数据 = 部分（日志窗口 2026-08-07 起，无跨年史）
> **数据源口径**：三源（dev live `gkxlumenx_*` + 三方库 gkx + 久新 `gkx_technology_analysis_dev` live）逐一探针留证；dev 2026-11-02 当日直连实查；`demo_*` 禁引。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：部分支持。**核心语义「数据搬运/刷新任务失败的次数」有真实承载——dev `gkxlumenx_cfg.lumen_analysis_task` 339 行真实执行日志（status/created_at/error_message 全列），失败率 115/339=33.92% 实算在案（含 23 执行日序列+错误归因 Top5）；但 UI 实时面板语义的**流式逐请求错误率**在三源均无承载（无 Flink/Kafka lag 面、无实时错误率表，`realtimeMonitor.js:9` 的 0.8% 为 mock 常数）。批量侧可算、流式侧缺承载——判部分支持。

### 批次通用纪律摘要（S3-06 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（§2.8 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 失败率分子分母同表同窗口（剔取消口径分母=total-cancelled 显式分基） |
| B4 | 负结论带探针 | absence_probe 四件（流式承载 0/久新无调度日志/UI mock/dev 日志在案） |
| B5 | 确定性 | 日序列按 DATE(created_at) 排序；错误归因 GROUP BY+count 降序 |
| B7 | 产物只由脚本产出 | 本件 py 实查出 _out.json |
| B9 | 单位/日期陷阱 | 失败率为比率（0-1）+百分数双写；created_at datetime 无零日期 |
| B10 | 口径裁定保守交付 | 批量任务失败率（可承载）vs 流式错误率（缺承载）双口径分野披露 |
| B11 | 多本账互推 | 339/115/212/12 与 035 件同表同源零漂移 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有现成「异常数据监测」结果面吗？ | 批量侧有（任务日志），流式侧无 | absence_probe + derived[0] |
| 原料结构与数据量够吗？ | 批量够/流式缺 | 339 任务/23 执行日 vs 0 流式面 |
| 缺口可补吗？ | 需新建流式监控管线 | §4.3 修复建议 |

## 摘要

「异常数据监测」是功能面板的链路健康卡片：数据搬运/刷新任务失败读数。UI 现状喂 mock 常数（realtimeMonitor errorRate 0.8%/阈值 2.5%）。数据侧判定：**部分支持**——dev `lumen_analysis_task`（339 任务，2026-08-07～2026-11-01 共 23 执行日）承载批量链路失败率：总口径 33.92%（115/339）、剔取消口径 35.17%，日失败率带 17.65%～29.03%，错误归因 Top1 单一错误 63 次（占 failed 54.8%）；节点级 1,790 条（success 1,197）。流式实时错误率承载缺失（三源无 Kafka lag/Flink metrics 面）——需接入流式监控方可补全。

- 需求判定：seq 408 需求明列叶（黑名单触发面板·异常数据监测），无公式。
- 复现状态：脚本已实查通过；双口径+日序列+归因 Top5 落产物。
- 档位结论：**部分支持**（批量可算、流式缺承载）。
- 关键事实：UI 0.8% mock 与实算 33.92% 相差 42 倍——演示常数不可作真值。
- 降档风险：无；升档路径：接入 Flink/Kafka 监控面 → 完全转换支持。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技知识图谱 → 分析展示 → 功能面板（`kgL6Functions.js:22` 异常数据监测卡片；黑名单触发面板 `BlacklistTriggerPanel.jsx:147`）。

### 1.2 为什么需要本指标

图谱数据经多源搬运/刷新入仓，链路失败会静默腐蚀下游全部指标——失败监测是数据可信度的运维前置位（黑名单触发面板的触发源之一）。

### 1.3 需求文档是否给出定义方法

SRS seq 408 仅给名称「异常数据监测」（黑名单触发面板）；row_01=492 语义「数据搬运/刷新任务失败的次数——回答数据链路出没出问题」。未给公式；本件以任务链路失败率为操作化口径。

### 1.4 类似指标权威方法可行性分析概要

SRE 错误率预算（Google SRE Ch.4）：错误率=失败请求/总请求，配 SLO 阈值。批量任务粒度等价物：failed/total（终态口径）。GB/T 36344-2018 数据质量监测体系将其归「可监测性」维度。

### 1.5 引用来源

1. Google SRE Book, Ch.4 *Service Level Objectives*. https://sre.google/sre-book/service-level-objectives/
2. ISO/IEC 25012:2008 *Data quality model*. https://www.iso.org/standard/35736.html
3. GB/T 36344-2018 信息技术 数据质量评价指标. http://www.ttbz.org.cn/standardManage/down/3863594/

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意**：数据接入/搬运链路的失败监测读数（失败次数/失败率），超阈值触发黑名单面板。
- **操作化定义（批量侧）**：失败率=failed/total（任务终态）；剔取消口径=failed/(total-cancelled)。
- **降档触发器**：任务日志表空或无 status 列 → 完全不支持（未触发：339 行满承载）。
- **升档触发器**：接入流式监控面（Kafka consumer lag/Flink checkpoint 错误率）→ 完全转换支持。

### 1.7 需求叶定位与相近叶关系

- 本叶：异常数据监测（row_01=492，黑名单面板）——任务失败**次数**语义。
- 相近叶：接入错误率（035，realtimeMonitor errorRate）——链路**比率**语义；两者同源（dev 任务日志）不同读数不同面板。

## 二、计算过程

### 2.1 数据源与表（dev 直查）

dev `gkxlumenx_cfg.lumen_analysis_task`（339 行，26 列含 status/created_at/error_message/cost_seconds）+ `lumen_analysis_task_node`（1,790 行，node_status）。列名以 DESCRIBE 实查为准（status 非 task_status）。

### 2.2 状态分布与失败率（主实测值）

| 实测项 | 值 | 产物键 |
|---|---|---|
| 任务总数 | 339 | facts.dev_task_total |
| failed / success / cancelled | 115 / 212 / 12 | facts.dev_task_failed 等（by_status） |
| **失败率（总口径）** | **33.92%** | derived[0].task_fail_rate_overall |
| 失败率（剔取消） | 35.17% | derived[0].task_fail_rate_excl_cancelled |
| 执行日 | 23 天（2026-08-07～2026-11-01） | derived[0].daily_fail_series |

### 2.3 日粒度序列与错误归因

日失败率带 17.65%（2026-11-01）～29.03%（2026-08-07），23 点全序列落 derived[0].daily_fail_series；错误归因 Top5 落 top_error_messages（Top1 单一错误 63 次=54.8% of failed——集中性故障非长尾）。

### 2.4 节点级交叉验证

`lumen_analysis_task_node` 1,790 条：success 1,197/pending 482/running 111——节点级无 failed 态（节点失败回写任务级），状态机自洽。

### 2.5 稳健性与口径敏感性

总口径 33.92% vs 剔取消 35.17%（差 1.25pp）——cancelled 占比小（3.54%），口径敏感性低；日序列与总口径量级自洽（日带 17-30%，累积 33.92%）。

### 2.6 需求符合性预评（UI 演示形态 vs 实算形态衔接）

UI mock 0.8%/阈值 2.5% 与实算 33.92% 不同口径（请求级 vs 任务级）亦不同量级——演示常数不可作真值；实算值供黑名单触发面板按真实阈值重校。

### 2.7 复现代码结果展示

`python3 code/M_SCIUI_KGANALY_029.py` → `M_SCIUI_KGANALY_029_out.json`。

### 2.8 分步证据对照表

| 步骤 | 产物键 | 值 |
|---|---|---|
| 任务总数/失败 | facts.dev_task_total / dev_task_failed | 339 / 115 |
| 失败率双口径 | derived[0].task_fail_rate_overall / excl_cancelled | 0.339233 / 0.351682 |
| 日序列首/末 | derived[0].daily_fail_series[0] / [-1] | 2026-08-07（29.03%）/ 2026-11-01（17.65%） |
| 归因 Top1 | derived[0].top_error_messages[0].count | 63 |
| 节点级 | derived[0].node_status_breakdown | success 1,197/pending 482/running 111 |

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 任务执行日志 | dev `lumen_analysis_task` | 足（339 行真日志） |
| 节点级明细 | dev `lumen_analysis_task_node` | 足（1,790 行） |
| 流式实时错误率 | 三源 | **缺**（absence_probe） |

### 3.2 现场复核清单

DESCRIBE 双表列名实查（status/node_status）；339/115 与 035 件同表零漂移。

## 四、数据缺失情况

### 4.1 流式实时错误率承载缺失（判定性缺口）

三源无 Flink/Kafka lag/实时错误率面——UI realtimeMonitor 语义不可承载（判部分支持的依据）。

### 4.2 口径级待裁项

任务级失败率与请求级错误率不可直接互换（粒度差异）；黑名单触发阈值（UI mock 2.5%）需立项重校。

### 4.3 修复建议与影响面

接入网关/流式监控面（Flink metrics 表或 Kafka consumer lag 视图）→ 实时错误率可算（升档）；影响面=新建监控管线，任务日志侧无需动。

## 参考文献

1. Google. *Site Reliability Engineering, Ch.4 SLOs（错误率预算）*. https://sre.google/sre-book/service-level-objectives/
2. ISO/IEC 25012:2008. *Software engineering — SQuaRE — Data quality model*. https://www.iso.org/standard/35736.html
3. GB/T 36344-2018 信息技术 数据质量评价指标. http://www.ttbz.org.cn/standardManage/down/3863594/

# 附件

## 附录 A 原始需求原文摘录

- SRS seq 408（分析展示.md）：异常数据监测（黑名单触发面板）。
- SRS row_01=492：数据搬运/刷新任务失败的次数——回答「数据链路出没出问题」。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_KGANALY_029_out.json`）

facts（ui_mount/ui_semantics/ui_demo_fallback/srs_anchor/cat/dev_task_*）；derived[0]（task_fail_rate_overall/excl_cancelled/status_breakdown/node_status_breakdown/daily_fail_series/top_error_messages）；absence_probe（4 件）；support_judgment；base_years_used/missing/note。

## 附录 C 可行性报告完整版（要点）

方法谱系：SRE 错误率预算（请求级）→ 批量任务等价物（任务终态比）。数据矩阵：dev 任务日志满承载/流式面三源零承载。结论：部分支持（批量可算+流式缺）。
