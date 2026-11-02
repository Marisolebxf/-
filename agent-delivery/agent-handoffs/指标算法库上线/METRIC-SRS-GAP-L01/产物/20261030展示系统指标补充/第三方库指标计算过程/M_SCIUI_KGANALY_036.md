# 数据更新频率（M_SCIUI_KGANALY_036）

> **类型**：无业务逻辑数值类（快照戳/执行节律统计型）｜ **域**：科技信息展示系统·科技知识图谱·分析展示·KPI 面板·数据更新频率读数｜ **UI 挂载**：`pages/tech-knowledge-graph/mockData.js:1114`（knowledgeGraphKPIs 数据更新频率='实时' mock）
> **数据支持度**：**部分支持**（久新快照戳满承载——批量快照制档位实锤（单版本 202610291012 零宽度同批写入）；dev 批量任务节律在案（23/87 执行日）；但 UI '实时' 语义的流式同步承载缺失+快照周期档位单版本无法内证）｜ **公式定义人**：仿王惠（推测定义——UI '实时' 为 mock 常数，本件以快照戳三列+任务节律重建档位判定）｜ **口径归属**：需求明列叶（row_01=499，数据更新频率）
> **复现脚本**：`code/M_SCIUI_KGANALY_036.py`｜ **产物**：`code/M_SCIUI_KGANALY_036_out.json`（含快照版本明细+任务节律）
> **四判定摘要**：直接结构 = 部分（快照戳三列在、流式同步面无）；直接数据 = 部分（单版本快照可判性质、周期档位无多版本可证）；依赖结构 = 部分（同左）；依赖数据 = 部分（dev 节律窗口 2026-08-07 起）
> **数据源口径**：三源（dev live `gkxlumenx_*` + 三方库 gkx + 久新 `gkx_technology_analysis_dev` live 218 表）逐一探针留证；两库 2026-11-02 当日直连实查；`demo_*` 禁引。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：部分支持。**节律档位判定的两类证据均部分在案：①久新快照戳三列（metrics_as_of_date/data_version/update_time）满承载且**性质实锤**——19,430 节点零宽度同批写入（MIN=MAX=2026-10-29 10:12:20，单版本 202610291012）证明「批量快照制非实时」；但**周期档位**（每日/每周/每月）需连续多版本内证——当前库仅 1 版本（历史版本未保留），无法内证。②dev 批量任务节律 23 执行日/87 天窗口仅佐证批量风格。③UI '实时' 语义的流式同步承载（CDC/binlog/stream）三源 0 命中。性质可判、周期与实时缺——判部分支持。

### 批次通用纪律摘要（S3-06 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（§2.8 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 执行覆盖率分母=窗口自然日数（87 天同基） |
| B4 | 负结论带探针 | absence_probe 三件（流式 0/快照戳在案/任务节律在案） |
| B5 | 确定性 | 快照 GROUP BY 排序；日序列 DATE(created_at) 排序 |
| B7 | 产物只由脚本产出 | 本件 py 实查出 _out.json |
| B9 | 单位/日期陷阱 | update_time datetime；as_of date 与 data_version(202610291012) 三戳互证 |
| B10 | 口径裁定保守交付 | 「批量快照制」实锤 vs 「周期档位待多版本」分野披露 |
| B11 | 多本账互推 | 三戳互证；dev 节律 23 执行日与 029 件 daily 序列同源 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有实时同步承载吗？ | 无 | absence_probe[0] |
| 更新节律性质可判吗？ | **可**——批量快照制 | 零宽度写入+单版本（§2.3） |
| 周期档位可内证吗？ | 否——单版本无历史 | derived[0]（1 个 as_of 日期） |

## 摘要

「数据更新频率」是 KPI 面板的刷新节律读数：UI mock 常数 '实时'。数据侧判定：**部分支持**——久新快照戳三列满承载且性质实锤：19,430 节点 update_time MIN=MAX=2026-10-29 10:12:20（零宽度原子写入）+单版本 data_version=202610291012，证明**批量快照制非实时**；边表批（2026-10-26）早于节点表批（10-29）3 天——上下游独立批量进一步排除实时联动。但周期档位（每日/每周/每月）因库内仅 1 个快照版本（历史未保留）无法内证；dev 任务节律（23 执行日/87 天，26.4% 覆盖）仅佐证批量风格；流式同步承载三源 0 命中。'实时' 读数是演示层——真值口径为「批量快照制，周期待多版本观察」。

- 需求判定：row_01=499 需求明列叶（节律档位语义），无公式。
- 复现状态：脚本已实查通过；快照版本+任务节律落产物。
- 档位结论：**部分支持**（性质实锤、周期与实时缺）。
- 关键事实：零宽度同批写入是「非实时」的结构级证据——流式写入应呈连续时间散布。
- 降档风险：无；升档路径：连续多版本快照落库 → 周期档位可证；CDC 接入 → 实时可算。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技知识图谱 → 分析展示 → KPI 面板（`mockData.js:1114` knowledgeGraphKPIs 数据更新频率）。

### 1.2 为什么需要本指标

数据新鲜度决定全部图谱指标的时效上限——用户需知读数是实时流还是某日快照，是 KPI 面板的元信息位。

### 1.3 需求文档是否给出定义方法

SRS row_01=499：「某类数据每隔多久刷新一次（如每日一次、每月一次）」——节律档位制语义；UI mock '实时' 无算法源。本件以快照戳+任务节律重建档位判定。

### 1.4 类似指标权威方法可行性分析概要

数据仓库快照事实表理论（Kimball）：as-of 日期维度+批次原子写入是快照制标准设计；数据质量时效性维（GB/T 36344/ISO 25012 Timeliness）：新鲜度=当前时刻-最近更新。节律档位判定=多版本间隔统计——单版本下只可判性质不可判周期。

### 1.5 引用来源

1. Kimball, R., Ross, M. *The Data Warehouse Toolkit, 3rd ed.* https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/books/data-warehouse-dw-toolkit/
2. GB/T 36344-2018 信息技术 数据质量评价指标. http://www.ttbz.org.cn/standardManage/down/3863594/
3. ISO/IEC 25012:2008 *Data quality model*. https://www.iso.org/standard/35736.html

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意**：图谱数据的刷新节律档位（实时/每日/每月），供用户判断读数新鲜度。
- **操作化定义**：快照戳证据（版本数/写入宽度）+执行节律证据（任务日覆盖率）→ 档位判定。
- **降档触发器**：快照戳列缺失 → 部分支持（未触发：三列在）；流式面 0 命中（已触发：实时档不可判）。
- **升档触发器**：多版本快照连续落库（周期可证）或 CDC 接入（实时可算）→ 完全转换支持。

### 1.7 需求叶定位与相近叶关系

- 本叶：数据更新频率（row_01=499）——节律档位。
- 相近叶：接入错误率（035，链路质量）——同为链路面板元信息；异常数据监测（029，失败次数）——三者构成链路健康三件套（节律/质量/失败）。

## 二、计算过程

### 2.1 数据源与表（两库直查）

久新 `ads_technology_graph_node`（metrics_as_of_date/data_version/update_time GROUP BY+MIN/MAX）+ `ads_technology_graph_edge`（update_time MAX）；dev `lumen_analysis_task`（DATE(created_at) 分布）。

### 2.2 快照戳证据（主实测值）

| 实测项 | 值 | 产物键 |
|---|---|---|
| as_of 日期数 | 1（2026-10-29） | facts.jiuxin_distinct_asof_days |
| data_version | 202610291012（19,430 节点同版本） | facts.jiuxin_snapshot_versions |
| 节点表写入窗口 | [10:12:20, 10:12:20] 零宽度 | facts.jiuxin_node_update_time_window |
| 边表批次 max | 2026-10-26 06:00:00 | facts.jiuxin_edge_update_time_max |

### 2.3 任务节律证据（dev）

23 执行日/87 天窗口（2026-08-07～2026-11-01），执行日覆盖率 26.4%（derived[0].dev_task_cadence.exec_day_ratio）——工作日制批量节律。

### 2.4 档位判定结论

**批量快照制（非实时）**：零宽度同批写入（原子快照特征）+单版本+边节点错批 3 天（独立批量）三证互锁；具体周期档位（每日/每周/每月）单版本无法内证——需连续多版本。

### 2.5 稳健性与口径敏感性

三戳互证（as_of/data_version/update_time）无矛盾；dev 节律仅佐证风格（任务节律≠快照节律，已在 §2.4 分离）。

### 2.6 需求符合性预评（UI 演示形态 vs 实算形态衔接）

UI '实时' 档与实判「批量快照」档不符——建议 KPI 读数改为「每日快照（最近 2026-10-29）」式真实披露。

### 2.7 复现代码结果展示

`python3 code/M_SCIUI_KGANALY_036.py` → `M_SCIUI_KGANALY_036_out.json`。

### 2.8 分步证据对照表

| 步骤 | 产物键 | 值 |
|---|---|---|
| 快照版本 | facts.jiuxin_snapshot_versions[0] | as_of 2026-10-29/v 202610291012/n 19,430 |
| 写入宽度 | facts.jiuxin_node_update_time_window | 零宽度 |
| 边表批 | facts.jiuxin_edge_update_time_max | 2026-10-26 06:00:00 |
| 执行日/窗口 | facts.dev_task_exec_days / dev_window_span_days | 23 / 87 |
| 覆盖率 | derived[0].dev_task_cadence.exec_day_ratio | 0.264 |

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 快照戳三列 | 久新 node/edge 表 | 足（性质可判） |
| 多版本历史 | 久新 | **缺**（单版本，周期不可证） |
| 流式同步面 | 三源 | **缺**（0 命中） |
| 任务节律 | dev 任务日志 | 足（佐证） |

### 3.2 现场复核清单

久新普通 cursor tuple 索引适配（非 DictCursor）；三戳互证一致。

## 四、数据缺失情况

### 4.1 多版本快照历史缺失（判定性缺口）

库内仅 1 版本（历史未保留）——周期档位（每日/每周/每月）无法内证，只能判「批量快照制」性质。

### 4.2 流式同步承载缺失（判定性缺口）

UI '实时' 语义需 CDC/binlog/stream 面——三源 0 命中。

### 4.3 修复建议与影响面

保留历史版本（快照表按版本分区/追加）→ 下次快照落库后周期可证；或接入 CDC（实时档激活）。影响面=快照保留策略调整，零迁移成本。

## 参考文献

1. GB/T 36344-2018 信息技术 数据质量评价指标（时效性维度）. http://www.ttbz.org.cn/standardManage/down/3863594/
2. Kimball, R., Ross, M. *The Data Warehouse Toolkit, 3rd ed.*（快照事实表 as-of 设计）. https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/books/data-warehouse-dw-toolkit/
3. ISO/IEC 25012:2008. *Software engineering — SQuaRE — Data quality model*（Timeliness）. https://www.iso.org/standard/35736.html

# 附件

## 附录 A 原始需求原文摘录

- SRS row_01=499：数据更新频率——某类数据每隔多久刷新一次（如每日一次、每月一次）。
- UI：mockData.js:1114 数据更新频率='实时'（mock）。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_KGANALY_036_out.json`）

facts（ui_mount/ui_semantics/ui_demo_fallback/srs_anchor/cat/jiuxin_snapshot_versions/jiuxin_distinct_asof_days/jiuxin_node_update_time_window/jiuxin_edge_update_time_max/dev_task_*）；derived[0]（jiuxin_batch_snapshot_cadence/dev_task_cadence/ui_mock_reference）；absence_probe（3 件）；support_judgment；base_years_used/missing/note。

## 附录 C 可行性报告完整版（要点）

方法谱系：快照事实表理论（as-of 维+原子批）+数据质量时效维。判定规则：流式承载→实时；零宽度单批→批量快照；多版本间隔→周期档。数据矩阵：快照戳满承载/多版本缺/流式缺。结论：部分支持。
