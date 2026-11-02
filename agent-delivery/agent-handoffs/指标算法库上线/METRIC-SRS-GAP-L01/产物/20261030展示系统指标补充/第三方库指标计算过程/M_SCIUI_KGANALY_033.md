# 按节点类型分组比较（M_SCIUI_KGANALY_033）

> **类型**：无业务逻辑数值类（分组统计实算型）｜ **域**：科技信息展示系统·科技知识图谱·算法展示·中心性计算展示·类型分组条形图｜ **UI 挂载**：`pages/tech-knowledge-graph/CentralityPanel.jsx:664`（typeBarOption 按类型平均度条形图）
> **数据支持度**：**完全转换支持**（久新节点表两个语义最近类型维——current_development_phase 6 档/chain_role 4 档分组完备，采样框分组平均度实算落产物）｜ **公式定义人**：仿王惠（推测定义——UI typeBarOption mock 四类为演示层，真图为技术节点同质图无 entity_type 列，本件以发展阶段/链路角色两维替代）｜ **口径归属**：需求明列叶（row_01=496，按节点类型分组比较）
> **复现脚本**：`code/M_SCIUI_KGANALY_033.py`｜ **产物**：`code/M_SCIUI_KGANALY_033_out.json`（含两维分组全档统计）
> **四判定摘要**：直接结构 = 无 entity_type 列（节点表 26 列全扫）；直接数据 = 无（同左）；依赖结构 = **足**（phase/chain_role 两类型维列在且分组完备）；依赖数据 = **足**（框 5,000 节点两维均 5,000/5,000 无档外漏）
> **数据源口径**：三源（dev live `gkxlumenx_*` + 三方库 gkx + 久新 `gkx_technology_analysis_dev` live 218 表）逐一探针留证；久新 2026-11-02 当日 live 直连实算；`demo_*` 禁引；UI mock 四类（论文/专利/学者/机构）为演示层。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全转换支持。**三源无 entity_type 列（久新节点表为技术节点同质图；gkx scholar_coauthor 亦同质图；dev 图表面 0 行），但两个语义最近类型维原料真实且量足：久新 `ads_technology_graph_node.current_development_phase`（6 档）与 `chain_role`（4 档），框内 5,000 节点两维分组均完备（求和=5,000 无档外漏）——分组平均度（typeBarOption 同构算子）**现在就能算**——本件已实算：链路角色维区分度最显著（INTERMEDIATE 23.0726 vs ISOLATED_IN_CHAIN 3.5381，6.5 倍差）。结构与数据量均足，判完全转换支持（类型维替代关系显式披露）。

### 批次通用纪律摘要（S3-06 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（§2.8 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 组均值分母=组内节点数（同框同基）；框整体均值同基对照 |
| B4 | 负结论带探针 | absence_probe 四件（无 entity_type/gkx 同质/dev 0 行/UI mock） |
| B5 | 确定性 | 节点框 ORDER BY id LIMIT 5000；分组按档名 sorted；两维分组完备性校验 |
| B7 | 产物只由脚本产出 | 本件 py 实算出 _out.json |
| B9 | 单位/日期陷阱 | 度为无量纲计数；ORIGIN 档仅 7 节点（小样本披露） |
| B10 | 口径裁定保守交付 | entity_type→phase/chain_role 替代口径显式披露（同质图必然替代） |
| B11 | 多本账互推 | 框 5,000/38,383 与族级同源；两维分组计数求和=5,000 双验 |

### 判档自检三问（本件 = 完全转换支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有 entity_type 分组承载吗？ | 无（同质图） | absence_probe（4 件） |
| 类型维替代原料够吗？ | **够** | phase 6 档+chain 4 档分组完备（5,000/5,000） |
| 现在就能算吗？ | **已实算** | 两维分组平均度落产物（§2.5） |

## 摘要

「按节点类型分组比较」是中心性面板的类型分组条形图（typeBarOption）：X 轴节点类型、Y 轴该类型平均度。UI mock 为论文/专利/学者/机构四类（演示层）。数据侧判定：**完全转换支持**——久新真图为技术节点同质图（无 entity_type 列），语义最近类型维是 `current_development_phase`（发展阶段）与 `chain_role`（产业链角色），两维分组完备实算：链路角色维 INTERMEDIATE（中间品）平均度 23.0726 一骑绝尘，ISOLATED_IN_CHAIN（链上孤立）3.5381 垫底（6.5 倍差）；发展阶段维 NO_PUBLICATION_OBSERVED 17.9706 最高、ORIGIN 5.8571 最低。分组语义与图论预期一致——中间品是连接枢纽、链上孤立最边缘。

- 需求判定：row_01=496 需求明列叶，无公式；类型维替代已披露。
- 复现状态：脚本已实算通过；两维分组全档统计落产物。
- 档位结论：**完全转换支持**（替代类型维分组+算子同构+已实算）。
- 关键事实：UI 四类 mock 在真图上无承载——真图的「类型」是发展阶段/产业链角色而非实体类别。
- 降档风险：无；升档路径：若引入多实体异构图（论文/专利节点入图）→ entity_type 直查。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技知识图谱 → 算法展示 → 中心性计算展示 → 类型分组条形图（`CentralityPanel.jsx:664`）。

### 1.2 为什么需要本指标

全图平均度掩盖类型间结构差异——分组比较揭示哪类节点是枢纽（指导采样/推荐/风险定位），是中心性面板的对比分析位。

### 1.3 需求文档是否给出定义方法

SRS row_01=496 仅给名称（规模/结构统计语义）；UI typeBarOption 为 mock 四类。真图同质无实体类型列——本件以 phase/chain_role 两维替代（§2.7 披露）。

### 1.4 类似指标权威方法可行性分析概要

分组中心性对比为网络分析标准操作（NetworkX degree + groupby）；类型维学理：技术发展阶段刻度（Rogers 扩散理论 EMERGENCE→CONSOLIDATION）与产业链角色（SOURCE/INTERMEDIATE/APPLICATION_END，Research Policy 2021）。

### 1.5 引用来源

1. NetworkX developers. *Degree*. https://networkx.org/documentation/stable/reference/classes/reporting.html#degree
2. Rogers, E. M. (2003). *Diffusion of Innovations, 5th ed.* https://doi.org/10.4324/9780203770755
3. Wang, Z., et al. (2021). *Measuring the position of industrial technologies in a supply chain*. Research Policy. https://doi.org/10.1016/j.respol.2021.104232

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意**：不同类型节点的中心性横向对比（哪类节点连接更密）。
- **操作化定义**：组均值 d̄(g)=mean(度|type=g)，两类型维（phase 6 档/chain_role 4 档）。
- **降档触发器**：若类型维列空率高/档位不完备 → 部分支持（未触发：两维 5,000/5,000）。
- **升档触发器**：异构图引入（entity_type 入图）→ 完全直接支持。

### 1.7 需求叶定位与相近叶关系

- 本叶：按节点类型分组比较（row_01=496）——**单指标**（平均度）条形图。
- 相近叶：034 指标对比（row_01=497，同挂载点）——**多指标**矩阵；本件是其单指标同构基座。

## 二、计算过程

### 2.1 装载与确定性采样框（B5）

复用族级共享缓存：5,000 框诱导子图 38,383 边（与 001/025-030 同框）；度=诱导子图无向度（degree_map）。

### 2.2 两类型维分组完备性（主实测值）

| 类型维 | 档数 | 档位 | 节点数求和 |
|---|---|---|---|
| current_development_phase | 6 | ACCELERATION 50/CONSOLIDATION 830/EMERGENCE 56/EXPANSION 758/NO_PUBLICATION_OBSERVED 3,299/ORIGIN 7 | **5,000** |
| chain_role | 4 | APPLICATION_END_CANDIDATE 1,032/INTERMEDIATE 2,630/ISOLATED_IN_CHAIN 721/SOURCE_CANDIDATE 617 | **5,000** |

两维均无 NULL 档外漏（完备性双验）。

### 2.3 维 1：发展阶段分组平均度

| 档 | 平均度 |
|---|---|
| NO_PUBLICATION_OBSERVED | **17.9706** |
| ACCELERATION | 16.4200 |
| CONSOLIDATION | 10.6759 |
| EXPANSION | 9.7836 |
| EMERGENCE | 6.1071 |
| ORIGIN | 5.8571 |

### 2.4 维 2：链路角色分组平均度（区分度最显著维）

| 档 | 平均度 |
|---|---|
| **INTERMEDIATE** | **23.0726** |
| SOURCE_CANDIDATE | 10.1702 |
| APPLICATION_END_CANDIDATE | 7.0339 |
| ISOLATED_IN_CHAIN | 3.5381 |

### 2.5 结果解读与框对照

框整体平均度 16.0666（derived[0].frame_avg_degree）；INTERMEDIATE 23.07 与 ISOLATED 3.54 的 6.5 倍差证明分组语义有效——中间品技术是跨域连接枢纽，链上孤立技术最边缘。NO_PUBLICATION_OBSERVED 最高（17.97）系跨领域通用技术（无单一学科归属但连接广泛）。

### 2.6 需求符合性预评（UI 演示形态 vs 实算形态衔接）

typeBarOption 条形数据结构（type/平均度数组）与本件分组输出字段级对应；类型名替换为真图档位名即可渲染。

### 2.7 复现代码结果展示

`python3 code/M_SCIUI_KGANALY_033.py` → `M_SCIUI_KGANALY_033_out.json`。

### 2.8 分步证据对照表

| 步骤 | 产物键 | 值 |
|---|---|---|
| 框节点/边 | facts.frame_nodes / frame_edges | 5,000 / 38,383 |
| 框整体平均度 | derived[0].frame_avg_degree | 16.0666 |
| phase 组 | derived[0].dimension_1_development_phase | 6 档（表 §2.3） |
| chain 组 | derived[0].dimension_2_chain_role | 4 档（表 §2.4） |
| 组均值极差 | 同上 | 23.0726-3.5381=19.53 |

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 类型维 1（发展阶段） | 久新 current_development_phase | 足（6 档完备） |
| 类型维 2（链路角色） | 久新 chain_role | 足（4 档完备） |
| 度算子 | 本件 py（诱导子图） | 已实算 |
| entity_type 列 | 三源 | 无（同质图，absence_probe） |

### 3.2 现场复核清单

两维分组计数求和=5,000 双验；ORIGIN 档 7 节点小样本已披露（均值解读需谨慎）。

## 四、数据缺失情况

### 4.1 entity_type 列缺失（结构缺口，有替代非判定性）

真图为技术节点同质图（19,430 节点全为技术实体）——论文/专利/学者/机构四类实体入图是异构图改造项，非当前图语义。

### 4.2 口径级待裁项

类型维替代（phase/chain_role vs entity_type）已披露；若立项要求实体类别维，需先改图构（异构改造）。

### 4.3 修复建议与影响面

短期：本件两维分组直供 typeBarOption；长期：异构图引入后 entity_type 分组直查。影响面=图构改造（大工程），当前两维已满足分组对比语义。

## 参考文献

1. NetworkX developers. *Degree — networkx documentation*. https://networkx.org/documentation/stable/reference/classes/reporting.html#degree
2. Rogers, E. M. (2003). *Diffusion of Innovations, 5th ed.*（发展阶段刻度学理）. https://doi.org/10.4324/9780203770755
3. Wang, Z., et al. (2021). *Measuring the position of industrial technologies in a supply chain*. Research Policy（链路角色维学理）. https://doi.org/10.1016/j.respol.2021.104232

# 附件

## 附录 A 原始需求原文摘录

- SRS row_01=496：按节点类型分组比较（实体与连接的规模/结构统计）。
- UI：CentralityPanel.jsx:664 typeBarOption（mock 四类演示层）。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_KGANALY_033_out.json`）

facts（ui_mount/ui_semantics/ui_demo_fallback/srs_anchor/cat/jiuxin_*/frame_*）；derived[0]（dimension_1_development_phase 6 档/dimension_2_chain_role 4 档/frame_avg_degree）；absence_probe（4 件）；support_judgment；base_years_used/missing/note。

## 附录 C 可行性报告完整版（要点）

方法谱系：分组中心性（groupby degree mean）为标准算子；类型维替代（同质图→发展阶段/链路角色）显式披露。数据矩阵：两类型维满承载/entity_type 三源无。结论：完全转换支持。
