# 图谱平均路径长度（M_SCIUI_KGANALY_038）

> **类型**：无业务逻辑数值类（图算法实算型——BFS 采样平均路径）｜ **域**：科技信息展示系统·科技知识图谱·分析展示·网络统计卡·平均路径长度读数（L3：新能源技术形成3个主要集群＞平均路径长度）｜ **UI 挂载**：`pages/tech-knowledge-graph/mockData.js:404`（avg_path: '3.2 hops' mock）
> **数据支持度**：**完全转换支持**（久新真图采样框可实算——LCC 4,770 节点 500 源 BFS 238 万可达对，平均 3.4644 跳落产物，量级与 mock 3.2 同带互证）｜ **公式定义人**：仿王惠（推测定义——UI 3.2 hops 为 mock 常数，本件以 NetworkX average_shortest_path_length 采样估计式重建）｜ **口径归属**：需求明列叶（row_01=501，新能源技术形成3个主要集群＞平均路径长度）
> **复现脚本**：`code/M_SCIUI_KGANALY_038.py`｜ **产物**：`code/M_SCIUI_KGANALY_038_out.json`（含连通域结构+采样估计全参数）
> **四判定摘要**：直接结构 = 无现成路径结果列（节点表 26 列无 path/distance/hop）；直接数据 = 无（同左）；依赖结构 = **足**（node/edge 表结构齐备，连通域+BFS 可算）；依赖数据 = **足**（框 5,000 节点/38,383 边，LCC 占框 95.4%）
> **数据源口径**：三源（dev live `gkxlumenx_*` + 三方库 gkx + 久新 `gkx_technology_analysis_dev` live 218 表）逐一探针留证；久新 2026-11-02 当日 live 直连实算；`demo_*` 禁引；UI mock 3.2 hops 仅作量级参照。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全转换支持。**三源无现成路径结果列（久新节点表 26 列全扫无 path/distance/hop），但图原料真实且量足：久新采样框（5,000 节点/38,383 诱导边）连通域分解 226 域、LCC 4,770 节点占框 95.4%——LCC 内 500 源 BFS 采样估计（全对精确 O(V·E) 不可行的标准替代）**现在就能算**——本件已实算：2,384,500 可达对平均 **3.4644 跳**，观测最大离心率 8 跳。结构与数据量均足，判完全转换支持（采样估计边界已披露，属算法代价标准做法）。

### 批次通用纪律摘要（S3-06 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（§2.8 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 均值分母=LCC 内可达对数（2,384,500，跨域对不计——路径无定义） |
| B4 | 负结论带探针 | absence_probe 四件（无结果列/gkx 0/dev 0 行/UI mock） |
| B5 | 确定性 | 节点框 ORDER BY id LIMIT 5000；源=sorted 等距抽样（step 写死）；BFS 邻接 sorted |
| B7 | 产物只由脚本产出 | 本件 py 实算出 _out.json |
| B9 | 单位/日期陷阱 | 单位=跳（hops，无权边数）；mock 3.2 是字符串带 hops 后缀 |
| B10 | 口径裁定保守交付 | LCC 估计域+采样框双层边界披露；确定性采样偏差方向不可内证已注明 |
| B11 | 多本账互推 | 框 5,000/38,383 与族级同源；226 域规模求和=5,000；对数=500×4,769 精确吻合 |

### 判档自检三问（本件 = 完全转换支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有现成路径长度列吗？ | 无 | absence_probe（4 件） |
| 图原料结构与数据量够吗？ | **够** | 框 5,000/38,383，LCC 95.4%（§2.3） |
| 现在就能算吗？ | **已实算** | 3.4644 跳落产物（§2.5） |

## 摘要

「图谱平均路径长度」是网络统计卡的小世界性读数：任意两节点最短路径边数的期望（单位=跳）。UI mock 3.2 hops。数据侧判定：**完全转换支持**——久新采样框实算：连通域分解 226 域（LCC 4,770 节点占 95.4%，225 小域 ≤8 节点），LCC 内 500 源确定性 BFS 采样 2,384,500 可达对，平均路径 **3.4644 跳**，最大离心率 8 跳——与 mock 3.2 同带（小世界 3-4 跳经验带），高聚簇（平均度 16.07）+短路径的典型小世界特征，与 UI「集群+短路径」展示语义一致。

- 需求判定：row_01=501 需求明列叶（新能源技术形成3个主要集群＞平均路径长度），无公式。
- 复现状态：脚本已实算通过；LCC 结构+采样估计全参数落产物。
- 档位结论：**完全转换支持**（图结构+数据量足+已实算，采样边界披露）。
- 关键事实：226 连通域中小域 225 个（ISOLATED 语义呼应 033/034 件）——路径只在 LCC 内有定义。
- 降档风险：无；升档路径：夜批落 avg_path 结果列 → 完全直接支持。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技知识图谱 → 分析展示 → 网络统计卡（`mockData.js:404` avg_path 读数；L3 路径：新能源技术形成3个主要集群＞平均路径长度——集群描述卡的量化支撑位）。

### 1.2 为什么需要本指标

平均路径长度是网络「多紧密」的直接读数：短路径=技术间转化/组合便利（小世界性）——与集群数（社区结构）共同刻画图的拓扑画像，是「3 个主要集群」叙事的量化底座。

### 1.3 需求文档是否给出定义方法

SRS row_01=501 仅给名称（规模/结构统计语义）；UI mock 3.2 hops 无算法源。本件以 NetworkX average_shortest_path_length 采样估计式重建。

### 1.4 类似指标权威方法可行性分析概要

Watts & Strogatz (1998) 小世界模型：平均路径长度 L 与重连概率关系是开创定义；Newman (2003) 综述给出技术共现网经验带（3-4 跳）；NetworkX 实现：全对精确 O(V·E) → 大图标准做法=源采样估计（本件 500 源）。

### 1.5 引用来源

1. Watts, D. J., Strogatz, S. H. (1998). *Collective dynamics of 'small-world' networks*. Nature, 393, 440-442. https://www.nature.com/articles/30918
2. NetworkX developers. *average_shortest_path_length*. https://networkx.org/documentation/stable/reference/algorithms/shortest_paths.html
3. Newman, M. E. J. (2003). *The structure and function of complex networks*. SIAM Review, 45(2), 167-256. https://doi.org/10.1137/S003614450342480

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意**：图谱全局平均最短路径（跳数），支撑小世界/集群叙事。
- **操作化定义**：LCC 上 500 源 BFS 采样估计 ℓ̄=Σd(s,t)/|pairs|（跨域对无路径不计入分母——标准口径）。
- **降档触发器**：图结构空 → 完全不支持（未触发：真图满承载）。
- **升档触发器**：夜批落 avg_path 结果列 → 完全直接支持。

### 1.7 需求叶定位与相近叶关系

- 本叶：平均路径长度（row_01=501）。
- 相近叶：网络密度（039，他批）——同为「集群」叙事的结构量；本件 LCC 结构（226 域）亦为其分母口径基础。

## 二、计算过程

### 2.1 装载与确定性采样框（B5）

族级共享缓存：5,000 框诱导子图 38,383 边（与 001/025-034 同框）；无向处理。

### 2.2 连通域分解（估计域界定）

226 连通域：LCC 4,770 节点（95.4%）+225 小域（Top2 域仅 8 节点，全清单落 facts.top5_cc_sizes）。**路径仅在同域对上有定义**——估计域=LCC（标准口径，跨域对不计入分母）。

### 2.3 采样估计参数（主实测值口径）

| 参数 | 值 | 产物键 |
|---|---|---|
| 估计域 | LCC 4,770 节点（95.4% of 框） | derived[0].largest_cc |
| 源抽样 | sorted 等距 500 源（step=max(1,4770//500)=9） | derived[0].sources_sampled |
| 可达对 | 500×4,769=**2,384,500**（精确吻合，LCC 全可达） | derived[0].reachable_pairs |

### 2.4 BFS 实算（主实测值）

每源 BFS 单源最短路（邻接 sorted 确定性），累加可达对跳数：Σd=8,261,196 → **ℓ̄=3.4644 跳**；观测最大离心率 8 跳（derived[0].max_eccentricity_observed）。

### 2.5 结果与量级对照

| 输出项 | 值 |
|---|---|
| **平均路径长度（LCC 采样估计）** | **3.4644 跳** |
| 对照 UI mock | 3.2 hops（同带——小世界 3-4 跳经验带，Newman 2003） |
| 直径上界/均值比 | 8/3.4644≈2.3（无标度网「超小世界」特征量级） |

### 2.6 稳健性与口径敏感性

确定性源抽样（非随机）偏差方向不可内证——作为边界披露（§2.7）；LCC 口径 vs 全框口径：跨域对（4.6% 节点相关）剔除是标准做法，若计入将虚增均值（无路径对不可定义）。

### 2.7 边界与披露汇总

①估计域=LCC（跨域对无定义）；②500 源确定性抽样（B5）非随机估计；③框 5,000/19,430 采样（诱导边 38,383/全边 587,252——框内稠密度低于全图，全图真实 ℓ̄ 可能更短）。三层边界均不影响量级结论（同带互证）。

### 2.8 分步证据对照表

| 步骤 | 产物键 | 值 |
|---|---|---|
| 连通域 | facts.connected_components / largest_cc_size | 226 / 4,770 |
| 域规模 Top5 | facts.top5_cc_sizes | [4770, 8, …] |
| 源数/对数 | derived[0].sources_sampled / reachable_pairs | 500 / 2,384,500 |
| **均值** | derived[0].avg_path_length_hops | **3.4644** |
| 最大离心率 | derived[0].max_eccentricity_observed | 8 |
| UI 参照 | derived[0].ui_mock_reference | 3.2 hops |

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 图节点/边结构 | 久新 node/edge 表 | 足（19,430/587,252） |
| 连通域/BFS 算子 | 本件 py | 已实算 |
| 现成路径结果列 | 三源 | 无（absence_probe，非判定性） |

### 3.2 现场复核清单

226 域规模求和=5,000；对数=500×4,769 精确吻合（LCC 全可达零 unreach）；LCC 4,770 与 028 件 present 4,778 差 8（8 节点度=0 不入 LCC——两口径自洽）。

## 四、数据缺失情况

### 4.1 现成路径结果列缺失（非判定性）

需图算法实算——结构与数据量足，非缺口。

### 4.2 口径级待裁项

加权路径（relation_confidence_score 为权）vs 无权跳数——本件按 UI 单位（hops）取无权；加权口径留立项。

### 4.3 修复建议与影响面

夜批落 `graph_metric_snapshot`（avg_path/diameter/density 按版本）→ 直查（升档）；全图精确值可分布式 BFS（Spark GraphX）——当前采样估计已满足展示精度。

## 参考文献

1. Watts, D. J., Strogatz, S. H. (1998). *Collective dynamics of 'small-world' networks*. Nature, 393, 440-442. https://www.nature.com/articles/30918
2. NetworkX developers. *average_shortest_path_length — networkx documentation*. https://networkx.org/documentation/stable/reference/algorithms/shortest_paths.html
3. Newman, M. E. J. (2003). *The structure and function of complex networks*. SIAM Review, 45(2), 167-256. https://doi.org/10.1137/S003614450342480

# 附件

## 附录 A 原始需求原文摘录

- SRS row_01=501：图谱平均路径长度（新能源技术形成3个主要集群＞平均路径长度）。
- UI：mockData.js:404 avg_path: '3.2 hops'（mock）。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_KGANALY_038_out.json`）

facts（ui_mount/ui_semantics/ui_demo_fallback/srs_anchor/cat/jiuxin_*/frame_*/connected_components/largest_cc_size/top5_cc_sizes）；derived[0]（largest_cc/components_total/top5_cc_sizes/sources_sampled/reachable_pairs/avg_path_length_hops/max_eccentricity_observed/ui_mock_reference）；absence_probe（4 件）；support_judgment；base_years_used/missing/note。

## 附录 C 可行性报告完整版（要点）

方法谱系：全对精确（O(VE) 不可行）→ 源采样估计（NetworkX 惯例）→ 本件 500 源确定性 BFS。数据矩阵：图结构满承载/结果列无。结论：完全转换支持（三层采样边界披露）。
