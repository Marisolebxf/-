# 数据接入错误率（M_SCIUI_KGANALY_035）

> **类型**：无业务逻辑数值类（链路日志统计型）｜ **域**：科技信息展示系统·科技知识图谱·分析展示·实时监控面板·接入错误率读数｜ **UI 挂载**：`pages/tech-knowledge-graph/realtimeMonitor.js:9`（errorRate: '0.8%'，threshold 2.5% mock）
> **数据支持度**：**部分支持**（批量接入/搬运任务错误率——dev `gkxlumenx_cfg.lumen_analysis_task` 339 行真实日志承载，33.92% 实算落产物；流式逐请求错误率承载缺失）｜ **公式定义人**：仿王惠（推测定义——UI 0.8%/2.5% 为 mock 常数无算法源，本件以任务级错误率重建并披露粒度差异）｜ **口径归属**：需求明列叶（row_01=498，接入错误率）
> **复现脚本**：`code/M_SCIUI_KGANALY_035.py`｜ **产物**：`code/M_SCIUI_KGANALY_035_out.json`（含双口径+承载面盘点）
> **四判定摘要**：直接结构 = 部分（任务日志表在、流式监控面无）；直接数据 = 部分（339 任务真日志 vs 实时错误率无）；依赖结构 = 部分（同左）；依赖数据 = 部分（日志窗口 2026-08-07 起无跨年史）
> **数据源口径**：三源（dev live `gkxlumenx_*` + 三方库 gkx + 久新 `gkx_technology_analysis_dev` live 218 表）逐一探针留证；dev 2026-11-02 当日直连实查；`demo_*` 禁引。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：部分支持。**UI 语义的流式逐请求错误率在三源均无承载（词族 stream/realtime/ingest/error 零命中——无 Flink metrics/Kafka lag 面；UI 0.8%/2.5% 为 mock 常数）；可承载口径为批量任务错误率——dev `lumen_analysis_task` 339 任务（failed=115）真实日志，错误率 33.92% 实算在案（粒度差异显式披露：任务级≥请求级，不可直接互换）。流式侧缺承载，判部分支持。

### 批次通用纪律摘要（S3-06 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（§2.8 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 错误率分子分母同表同窗口（339 任务终态） |
| B4 | 负结论带探针 | absence_probe 四件（流式 0/批量在案/jimu 无错误列/cfg 表域盘点） |
| B5 | 确定性 | 状态 GROUP BY 排序；cfg 表清单 information_schema 排序 |
| B7 | 产物只由脚本产出 | 本件 py 实查出 _out.json |
| B9 | 单位/日期陷阱 | 错误率为比率（百分数呈现）；mock 0.8% 是字符串带 % 号 |
| B10 | 口径裁定保守交付 | 任务级 vs 请求级粒度差异双口径分野披露 |
| B11 | 多本账互推 | 339/115 与 029 件同表同源零漂移 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有流式错误率承载吗？ | 无 | absence_probe（4 件） |
| 批量侧原料够吗？ | 够 | 339 任务真日志（§2.3） |
| 缺口可补吗？ | 需新建流式监控 | §4.3 |

## 摘要

「数据接入错误率」是实时监控面板的 errorRate 读数：接入链路失败占比。UI mock 常数 0.8%（阈值 2.5%）。数据侧判定：**部分支持**——流式逐请求语义三源零承载（无 Flink/Kafka 监控面）；批量侧 dev 任务链路日志（339 任务 failed=115）可实算任务级错误率 33.92%（与 029 件同源交叉一致），cfg 库 11 表盘点确认无独立 ETL 错误日志表、jimu 数据源登记面 8 行无错误列——错误率唯一可算源即任务链路日志。mock 0.8% 与实算 33.92% 相差 42 倍：演示常数不可作真值，接入监控需按真实口径重建。

- 需求判定：row_01=498 需求明列叶（以页面数据说明为准），无公式。
- 复现状态：脚本已实查通过；批量错误率+承载面盘点落产物。
- 档位结论：**部分支持**（批量可算、流式缺承载）。
- 关键事实：UI「实时」监控面板在数据侧实为批量链路——实时语义是演示层。
- 降档风险：无；升档路径：接入网关/流式监控面 → 完全转换支持。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技知识图谱 → 分析展示 → 实时监控面板（`realtimeMonitor.js:9` errorRate 读数）。

### 1.2 为什么需要本指标

接入是图谱数据的第一跳——错误率超阈值意味着下游全部指标的底座腐蚀，是实时监控面板的核心告警位。

### 1.3 需求文档是否给出定义方法

SRS row_01=498：「页面数据说明为准；如需纳入指标体系须先立项调研口径」——读数语义在 UI 层；UI 值为 mock 无算法源。本件以任务级错误率重建+粒度披露。

### 1.4 类似指标权威方法可行性分析概要

SRE 错误率（请求级：失败请求/总请求+SLO 阈值）是权威基线；批量等价物为任务终态比。GB/T 36344-2018 将其归数据质量「可监测性」维度。

### 1.5 引用来源

1. Google SRE Book, Ch.4. https://sre.google/sre-book/service-level-objectives/
2. ISO/IEC 25012:2008. https://www.iso.org/standard/35736.html
3. GB/T 36344-2018. http://www.ttbz.org.cn/standardManage/down/3863594/

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意**：数据接入（搬运/请求）链路的失败比率，超阈值（2.5%）告警。
- **操作化定义（批量侧）**：错误率=failed/total（任务终态）；请求级需流式监控面。
- **降档触发器**：任务日志表空 → 完全不支持（未触发：339 行在案）。
- **升档触发器**：接入 Flink metrics/Kafka lag 视图 → 完全转换支持。

### 1.7 需求叶定位与相近叶关系

- 本叶：接入错误率（row_01=498，实时监控面板）——**比率**读数。
- 相近叶：异常数据监测（029，黑名单面板）——失败**次数**监测；同源（任务日志）不同面板不同读数，两件互证（339/115 零漂移）。

## 二、计算过程

### 2.1 数据源与承载面盘点（dev 直查）

dev `lumen_analysis_task`（339 行）+cfg 库 11 表 information_schema 盘点+jimu 数据源登记 8 行——确认错误率唯一可算源为任务链路日志。

### 2.2 任务级错误率（主实测值）

| 实测项 | 值 | 产物键 |
|---|---|---|
| 任务总数/失败 | 339 / 115 | facts.dev_task_total / dev_task_failed |
| **任务错误率** | **33.92%** | derived[0].task_error_rate_overall |
| 状态分布 | success 212/failed 115/cancelled 12 | derived[0].status_breakdown |

### 2.3 承载面核查读数

| 面 | 实查结果 | 产物键 |
|---|---|---|
| cfg 库表域 | 11 表（lumen_analysis_task/node 为主，无独立 ETL 错误表） | facts.dev_cfg_tables |
| jimu 数据源登记 | 8 行（名称/类型列，无错误日志列） | facts.dev_jimu_datasources / dev_jimu_names |
| 流式监控面 | 三源 0 命中 | absence_probe[0] |

### 2.4 粒度差异与量级对照

任务级 33.92% vs UI mock 0.8%（42 倍差）——粒度不同（任务终态 vs 请求瞬时）亦量级不同；mock 阈值 2.5% 亦为演示值。日序列与错误归因复用 029 件（同表同源，`M_SCIUI_KGANALY_029_out.json` daily_fail_series/top_error_messages）。

### 2.5 稳健性与口径敏感性

总口径 33.92% 与 029 件剔取消口径 35.17% 差 1.25pp——cancelled 占比小敏感性低；日失败率带 17.65-29.03% 与总口径自洽。

### 2.6 需求符合性预评（UI 演示形态 vs 实算形态衔接）

UI errorRate 卡片读数可由批量口径直供（标注「任务级」）；「实时」语义待流式监控接入后激活。

### 2.7 复现代码结果展示

`python3 code/M_SCIUI_KGANALY_035.py` → `M_SCIUI_KGANALY_035_out.json`。

### 2.8 分步证据对照表

| 步骤 | 产物键 | 值 |
|---|---|---|
| 任务数/失败 | facts.dev_task_total / dev_task_failed | 339 / 115 |
| 错误率 | derived[0].task_error_rate_overall | 0.3392 |
| 状态分布 | derived[0].status_breakdown | 212/115/12 |
| cfg 表域 | facts.dev_cfg_tables | 11 表清单 |
| jimu 登记 | facts.dev_jimu_datasources | 8 |
| UI mock | derived[0].ui_mock_reference | 0.8%/2.5% |

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 批量任务日志 | dev `lumen_analysis_task` | 足（339 行） |
| 流式实时错误率 | 三源 | **缺**（absence_probe） |
| 数据源错误登记 | dev jimu | 无错误列（仅登记面） |

### 3.2 现场复核清单

information_schema 别名大写（TABLE_SCHEMA/TABLE_NAME）适配；339/115 与 029 件零漂移。

## 四、数据缺失情况

### 4.1 流式逐请求错误率承载缺失（判定性缺口）

三源无 Flink metrics/Kafka consumer lag/网关日志面——UI「实时」语义不可承载（判部分支持的依据）。

### 4.2 口径级待裁项

任务级 vs 请求级粒度不可互换；阈值（mock 2.5%）需按真实链路重校。

### 4.3 修复建议与影响面

接入网关访问日志或 Flink metrics 落库（请求级错误面）→ 实时错误率可算（升档）；影响面=新建监控管线，批量侧已就绪。

## 参考文献

1. Google. *Site Reliability Engineering, Ch.4 SLOs（错误率与预算）*. https://sre.google/sre-book/service-level-objectives/
2. ISO/IEC 25012:2008. *Software engineering — SQuaRE — Data quality model*. https://www.iso.org/standard/35736.html
3. GB/T 36344-2018 信息技术 数据质量评价指标. http://www.ttbz.org.cn/standardManage/down/3863594/

# 附件

## 附录 A 原始需求原文摘录

- SRS row_01=498：数据接入错误率（页面数据说明为准；纳入指标体系须先立项调研口径）。
- UI：realtimeMonitor.js:9（errorRate '0.8%'，threshold 2.5%——mock）。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_KGANALY_035_out.json`）

facts（ui_mount/ui_semantics/ui_demo_fallback/srs_anchor/cat/dev_cfg_tables/dev_jimu_*/dev_task_*）；derived[0]（task_error_rate_overall/status_breakdown/ui_mock_reference）；absence_probe（4 件）；support_judgment；base_years_used/missing/note。

## 附录 C 可行性报告完整版（要点）

方法谱系：SRE 请求级错误率（权威）→ 批量任务终态比（可承载等价物）。数据矩阵：任务日志满承载/流式面零承载/jimu 无错误列。结论：部分支持。
