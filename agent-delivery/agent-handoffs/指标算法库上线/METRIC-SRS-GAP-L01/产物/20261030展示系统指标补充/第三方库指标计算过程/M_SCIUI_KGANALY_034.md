# 知识图谱节点按类型分组的指标对比（M_SCIUI_KGANALY_034）

> **类型**：无业务逻辑数值类（分组多指标矩阵实算型）｜ **域**：科技信息展示系统·科技知识图谱·算法展示·中心性计算展示·类型分组（多指标对照）｜ **UI 挂载**：`pages/tech-knowledge-graph/CentralityPanel.jsx:664`（与 033 同挂载点；SRS 名录单列本件为「指标对比」侧面）
> **数据支持度**：**完全转换支持**（久新节点表 4 指标成分列满承载——度/加权度/成员度/CORE 占比，chain_role 分组 × 4 指标矩阵+phase×chain 交叉计数实算落产物）｜ **公式定义人**：仿王惠（推测定义——UI 仅单指标 mock，多指标矩阵为 SRS 名录语义扩展）｜ **口径归属**：需求明列叶（row_01=497，知识图谱节点按类型分组的指标对比/节点类型维度对照）
> **复现脚本**：`code/M_SCIUI_KGANALY_034.py`｜ **产物**：`code/M_SCIUI_KGANALY_034_out.json`（含 4 指标矩阵+交叉计数矩阵）
> **四判定摘要**：直接结构 = 无现成多指标对照面（三源词族 0 命中）；直接数据 = 无（同左）；依赖结构 = **足**（4 指标成分列：度可算+weighted_degree/community_role/membership_score 真列）；依赖数据 = **足**（框 5,000 节点分组完备+membership_score 全表直查 19,430 行）
> **数据源口径**：三源（dev live `gkxlumenx_*` + 三方库 gkx + 久新 `gkx_technology_analysis_dev` live 218 表）逐一探针留证；久新 2026-11-02 当日 live 直连实算；`demo_*` 禁引。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全转换支持。**三源无现成「类型分组多指标对照」结果面，但 4 指标成分原料真实且量足：久新采样框度可算（38,383 诱导边）+真列三档（weighted_degree/community_role/membership_score，后者全表 19,430 行直查），chain_role 4 档分组完备——分组多指标矩阵**现在就能算**——本件已实算：4×4 矩阵全格+phase×chain 交叉计数（6×4）落产物，且矩阵揭示单指标不可见的分层解耦（ISOLATED_IN_CHAIN 度最低 3.54 但成员度最高 0.951、CORE 占比 62%——小而紧社区）。结构与数据量均足，判完全转换支持。

### 批次通用纪律摘要（S3-06 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（§2.8 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 各组均值/占比分母=组内节点数；core_ratio 同基 |
| B4 | 负结论带探针 | absence_probe 三件（无 entity_type 多指标面/gkx 0/UI 单指标 mock） |
| B5 | 确定性 | 节点框 ORDER BY id LIMIT 5000；矩阵按档名 sorted；交叉计数键排序 |
| B7 | 产物只由脚本产出 | 本件 py 实算出 _out.json |
| B9 | 单位/日期陷阱 | 度无量纲；membership_score 0-1；core_ratio 0-1 占比非百分数 |
| B10 | 口径裁定保守交付 | 多指标矩阵为 SRS 名录语义扩展（UI 仅单指标）显式披露 |
| B11 | 多本账互推 | avg_degree 列与 033 件逐格一致；membership 值域与 030 件一致 |

### 判档自检三问（本件 = 完全转换支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有现成多指标对照面吗？ | 无 | absence_probe（3 件） |
| 4 指标成分原料够吗？ | **够** | 度可算+三真列全承载（§2.3） |
| 现在就能算吗？ | **已实算** | 4×4 矩阵+交叉计数落产物（§2.5） |

## 摘要

「知识图谱节点按类型分组的指标对比」是 033 的多指标侧面：SRS 名录将其单列（row_01=497），本件按此语义在 chain_role 4 档分组上输出 4 指标对照矩阵（平均度/平均加权度/平均成员度/CORE 占比）+phase×chain 交叉计数。数据侧判定：**完全转换支持**——矩阵实算揭示单指标不可见的分层解耦：INTERMEDIATE 度/加权度一骑绝尘（23.07/15.77）但 CORE 占比仅 15.89%；ISOLATED_IN_CHAIN 度最低（3.54）却成员度最高（0.951）、CORE 占比 62%——链上孤立技术是「小而紧」的微型社区核心。多指标对照的信息量超出单指标，SRS「指标对比」语义在真图上成立。

- 需求判定：row_01=497 需求明列叶（与 033 同挂载点不同侧面），无公式。
- 复现状态：脚本已实算通过；4×4 矩阵+交叉计数落产物。
- 档位结论：**完全转换支持**（4 指标成分满承载+已实算）。
- 关键事实：三指标分层解耦（度↓成员度↑CORE↑的 ISOLATED 档）是矩阵对照独有发现。
- 降档风险：无；升档路径：异构 entity_type 入图后矩阵扩维。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技知识图谱 → 算法展示 → 中心性计算展示 → 类型分组（多指标对照矩阵；`CentralityPanel.jsx:664` 同挂载点）。

### 1.2 为什么需要本指标

单指标分组条形图（033）只答「谁连接密」；多指标矩阵答「不同类型节点在结构/社区/归属上的组合画像」——分组对比的完整形态，支撑技术选型/引进的多维论证。

### 1.3 需求文档是否给出定义方法

SRS row_01=497 仅给名称（指标对比/节点类型维度对照）；UI 仅单指标 mock。本件按名录语义扩展为 4 指标矩阵（§1.6 披露），指标集取节点表现三档（030 同源）+框内度。

### 1.4 类似指标权威方法可行性分析概要

多指标分组对照为网络科学标准分析（groupby + multi-metric）；社区侧 Fortunato & Hric (2016) 用户指南界定 membership strength/role 指标族；加权度（Opsahl 2010）为连接强度标准量。

### 1.5 引用来源

1. Fortunato, S., Hric, D. (2016). *Community detection in networks: A user guide*. Physics Reports, 659, 1-44. https://doi.org/10.1016/j.physrep.2016.09.002
2. Blondel, V. D., et al. (2008). *Fast unfolding of communities in large networks*. J. Stat. Mech., P10008. https://iopscience.iop.org/article/10.1088/1742-5468/2008/10/P10008
3. NetworkX developers. *Degree*. https://networkx.org/documentation/stable/reference/classes/reporting.html#degree

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意**：类型维度上多指标横向对照（不同类型节点的组合画像）。
- **操作化定义**：chain_role 4 档 × {avg_degree, avg_weighted_degree, avg_membership_score, core_ratio}+phase×chain 交叉计数。
- **降档触发器**：任一指标列空率高 → 部分支持（未触发：全列满承载）。
- **升档触发器**：异构 entity_type 入图 → 完全直接支持（矩阵直查）。

### 1.7 需求叶定位与相近叶关系

- 本叶：指标对比（row_01=497）——多指标矩阵。
- 相近叶：033 分组比较（单指标条形图，本件 avg_degree 列与其逐格一致）；030 综合评分（把多指标压成单分——本件矩阵是其成分展开）。

## 二、计算过程

### 2.1 装载与数据源（B5）

族级共享缓存（5,000 框/38,383 诱导边）+membership_score 全表直查（19,430 行，与 030 件同法同源）。

### 2.2 4 指标定义（主实测值口径）

| 指标 | 定义 | 数据源 |
|---|---|---|
| avg_degree | 诱导子图无向度均值 | 框内实算 |
| avg_weighted_degree | 全图证据加权连接度均值 | 久新真列 |
| avg_membership_score | 社区归属强度均值（0-1） | 久新真列（全表直查） |
| core_ratio | community_role='CORE' 占比 | 久新真列 |

### 2.3 分组完备性

chain_role 4 档计数 1,032+2,630+721+617=5,000；phase 6 档=5,000（与 033 一致）。

### 2.4 chain_role × 4 指标矩阵（主实测值）

| 链路角色 | n | avg_degree | avg_wd | avg_ms | core_ratio |
|---|---|---|---|---|---|
| INTERMEDIATE | 2,630 | **23.0726** | **15.7749** | 0.7784 | 0.1589 |
| SOURCE_CANDIDATE | 617 | 10.1702 | 6.7843 | 0.8385 | 0.0373 |
| APPLICATION_END_CANDIDATE | 1,032 | 7.0339 | 3.3156 | 0.8520 | 0.0078 |
| ISOLATED_IN_CHAIN | 721 | 3.5381 | 1.6605 | **0.9510** | **0.6200** |

### 2.5 分层解耦发现与交叉计数

三指标分层解耦（矩阵独有）：度/加权度 INTERMEDIATE 最高；成员度 ISOLATED 最高（0.951）；CORE 占比 ISOLATED 62% vs APPLICATION_END 0.78%（79 倍差）——孤立技术=小而紧微型社区核心。phase×chain 交叉计数（6×4 全矩阵落产物）：NO_PUBLICATION_OBSERVED 档 3,299 中 INTERMEDIATE 1,722；EMERGENCE 56 中 APPLICATION_END 34；ORIGIN 7 中 ISOLATED 5。

### 2.6 需求符合性预评（UI 演示形态 vs 实算形态衔接）

UI typeBarOption 单指标条形可由矩阵 avg_degree 列直供；多指标矩阵供表格/热力图扩展渲染。

### 2.7 复现代码结果展示

`python3 code/M_SCIUI_KGANALY_034.py` → `M_SCIUI_KGANALY_034_out.json`。

### 2.8 分步证据对照表

| 步骤 | 产物键 | 值 |
|---|---|---|
| 矩阵 4 档 | derived[0].matrix_by_chain_role | §2.4 表 |
| 指标集 | derived[0].metrics | 4 指标定义 |
| 交叉计数 | derived[0].cross_phase_x_chain_count | 6×4 全矩阵 |
| 极差例 | core_ratio 差 | 0.6200-0.0078 |

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 度算子 | 框内实算 | 足 |
| 加权度/角色/成员度 | 久新三真列 | 足（全承载） |
| entity_type 多指标面 | 三源 | 无（absence_probe，非判定性） |

### 3.2 现场复核清单

avg_degree 列与 033 件逐格一致；membership 值域与 030 件一致；交叉矩阵行和=phase 计数、列和=chain 计数双验。

## 四、数据缺失情况

### 4.1 现成多指标对照面缺失（非判定性）

三源无现成矩阵面——本件式实算即结果；成分列满承载非缺口。

### 4.2 口径级待裁项

指标集（4 指标）为名录语义扩展选择——立项可增删（如补 betweenness 需全图采样代价评估）。

### 4.3 修复建议与影响面

夜批落分组矩阵结果表（GROUP BY chain_role 直查化）；UI 扩表格/热力图组件渲染矩阵。

## 参考文献

1. Fortunato, S., Hric, D. (2016). *Community detection in networks: A user guide*. Physics Reports, 659, 1-44. https://doi.org/10.1016/j.physrep.2016.09.002
2. Blondel, V. D., Guillaume, J.-L., Lambiotte, R., Lefebvre, E. (2008). *Fast unfolding of communities in large networks*. Journal of Statistical Mechanics, 2008(10), P10008. https://iopscience.iop.org/article/10.1088/1742-5468/2008/10/P10008
3. NetworkX developers. *Degree — networkx documentation*. https://networkx.org/documentation/stable/reference/classes/reporting.html#degree

# 附件

## 附录 A 原始需求原文摘录

- SRS row_01=497：知识图谱节点按类型分组的指标对比（节点类型维度对照）。
- UI：CentralityPanel.jsx:664（单指标 mock；矩阵为名录语义扩展）。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_KGANALY_034_out.json`）

facts（ui_mount/ui_semantics/ui_demo_fallback/srs_anchor/cat/jiuxin_*/frame_*）；derived[0]（metrics/matrix_by_chain_role/cross_phase_x_chain_count）；absence_probe（3 件）；support_judgment；base_years_used/missing/note。

## 附录 C 可行性报告完整版（要点）

方法谱系：分组多指标矩阵（groupby multi-metric）+交叉计数；指标集取节点表现三档+框内度。数据矩阵：三真列+度可算全承载。结论：完全转换支持。
