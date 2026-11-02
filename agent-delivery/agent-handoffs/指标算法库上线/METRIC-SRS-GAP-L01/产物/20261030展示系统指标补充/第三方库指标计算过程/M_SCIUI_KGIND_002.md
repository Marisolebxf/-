# 聚类系数（M_SCIUI_KGIND_002）

> **类型**：简单统计类（图结构统计读数）｜ **域**：科技信息展示系统·科技知识图谱·指标展示·融合统计指标和模型特征｜ **UI 挂载**：指标展示页 → `IndicatorDisplay.jsx:128` indicators Tab → `FusionIndicatorsPanel.jsx:44-98`（seedIndicators 消费 `mockData.js:373 fusionIndicators`）——`mockData.js:389-400` clustering 行 `{graphValue:0.68, ruleValue:0.70, modelValue:0.66, fusionValue:0.68, weight:0.20, source:'rule', unit:'ratio'}`——**mock 挂载件（数据面无真源）**；派单书 UI 挂载列为空（本件为融合指标表第 2 行项，派单按 Tab 归位）
> **数据支持度**：**完全转换支持**（三源无聚类系数现成结果面——探针留证；但久新真图承载即期可算——本件在 5,000 框诱导子图实算双口径：Watts-Strogatz 平均聚类系数 **0.234824** + 全局 transitivity **0.122238**（三角形 95,131 个）——结构侧原料足量真图实算）｜ **公式定义人**：权威定义（Watts & Strogatz 1998 局部聚类 + 全局 transitivity 双口径并报）｜ **口径归属**：UI 拆件叶（SRS seq 413「知识图谱分析指标…统一管理和展示」的图谱分析指标维），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_KGIND_002_KGSVC_001_002_004.py`（四件合算）+ 薄壳 `code/M_SCIUI_KGIND_002.py`（存在性+判档+基期三键校验）｜ **产物**：`code/M_SCIUI_KGIND_002_out.json`
> **四判定摘要**：直接结构 = 无聚类系数结果列（absence_probe 留证）；直接数据 = 无落库读数（mock 0.68 是演示值）；依赖结构 = **足**（久新 node/edge 19,430/587,252）；依赖数据 = **足**（本件 5,000 框 4,778 节点/38,383 边实算通过）
> **数据源口径**：三源（dev live `gkxlumenx_*` + 三方库 gkx + 久新 `gkx_technology_analysis_dev` live）逐一探针留证；久新 2026-11-02 当日 live 直连实算；`demo_*` 禁引。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 姠终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全转换支持。**证据链：①三源无聚类系数结果面（久新 SHOW TABLES 词族扫描无独立 clustering/density 结果表——node 表自带 `community_id` 列社群归属现成但无聚类系数列）；②dev 图结构面 26 张全 0 行空壳（族级快照，非零 4 张均非图拓扑语义）；③久新真图承载即期可算——本件 5,000 框（ORDER BY technology_node_id LIMIT 5000）诱导子图 4,778 节点/38,383 边，双口径实算通过（§2.2）；④gkx `dwd_scholar_coauthor`（合作边）是备选图原料（本件未启用，主承载久新技术图）。

### 批次通用纪律摘要（S3-07 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（§2.8 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写当日 live 读数 |
| B3 | 同基相除 | 局部系数分母 $C(d_v,2)$（节点邻域对）；degree<2 节点 306 个按 NetworkX 惯例剔除出均值分母并披露 |
| B4 | 负结论带探针 | absence_probe 三件（三源逐一留证） |
| B5 | 确定性 | ORDER BY 主键 LIMIT 5000 采样框+sorted 邻域枚举——同框重跑逐位一致 |
| B6 | 闸门自身被闸 | 不自跑闸门 |
| B7 | 产物只由脚本产出 | 本件 py 实算出 _out.json |
| B8 | 回执不复收 | B5 保证幂等 |
| B9 | 单位/日期陷阱 | 无量纲比率 0-1（unit:'ratio' 同构）；mock 0.68 是演示值非读数 |
| B10 | 口径裁定保守交付 | 平均局部 vs 全局 transitivity 双口径并报（语义不同不可互替） |
| B11 | 多本账互推 | 与 049/053/057/066 同框（4,778/38,383 对账键） |

### 判档自检三问（本件 = 完全转换支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有聚类系数结果列吗？ | 无 | absence_probe（久新无结果面；dev 空壳） |
| 结构侧原料够吗？ | **够（全量真图）** | 久新 19,430 节点/587,252 边（§3.1） |
| 现在就能算吗？ | **已实算** | 双口径 0.234824/0.122238（§2.2） |

## 摘要

「聚类系数」是指标展示页融合统计指标表的第 2 项：衡量图谱中「我朋友的朋友也互相是朋友」的抱团程度，输出 0-1 比率（mock fusionValue 0.68）。数据侧判定：**完全转换支持**——三源无聚类系数现成结果面（探针留证），但久新技术关联网真图承载即期可算。本件在 5,000 框诱导子图（4,778 节点/38,383 边，与 049/053/057/066 同框）实算**双口径**：**Watts-Strogatz 平均聚类系数 0.234824**（4,472 个 degree≥2 节点局部系数均值；306 个 degree<2 节点按惯例剔除分母）、**全局 transitivity 0.122238**（三元闭包闭合率，框内三角形 95,131 个）；Top10 局部聚类节点全为 1.0（小型全连通学术团簇——如「Historical Map Data 计算分析」「Carotenoid 鉴定分析方法」）。核心发现：①实测 0.235 与 mock 0.68 差距显著——mock 值不可直接沿用，回填须以实测为准；②平均局部（0.235）≈ 全局（0.122）两倍——闭包集中在低度节点的紧密小团（局部高系数）而非高度枢纽周围（拉低全局），与稀疏技术图「小社群+长尾桥接」结构一致；③聚类系数是 058 融合指标数（mock 5 项之一）与 seq 417 综合评分（scores.clustering 权重位）的共享底座——一处实算三处复用。

- 需求判定：UI 拆件叶（seq 413 统一管理展示的图谱分析指标维）。
- 复现状态：双口径实算通过；Top10+剔除披露全落产物。
- 档位结论：**完全转换支持**。
- 关键事实：三源结果面缺位留证；实测 avg 0.234824/transitivity 0.122238/三角形 95,131。
- 降档风险：无（结构侧全量真图稳定承载）；升档路径：久新物化 clustering 结果列或 dev 激活图表面 → 完全直接支持。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统/科技知识图谱/指标展示/融合统计指标和模型特征——`IndicatorDisplay.jsx:128` indicators Tab 挂 `FusionIndicatorsPanel`；面板 `:44-98` 以 `seedIndicators`（=mockData `fusionIndicators` 5 项）为底，经 `applyScenarioWeights` 场景权重重算后渲染指标表（名称/graph/rule/model/fusion 四值+权重+趋势）。本件=第 2 行「聚类系数」：`mockData.js:389-400` `{source:'rule', graphValue:0.68, ruleValue:0.70, modelValue:0.66, fusionValue:0.68, weight:0.20, unit:'ratio'}`。相关性热力图（`:85-98` buildCorrelationMatrix）与一致性检验（checkConsistency）均以 5 指标为轴——聚类系数是矩阵第 2 轴。

### 1.2 为什么需要本指标

融合统计指标表的价值是「同一指标三源（图谱计算/专家规则/模型特征）并排对比」——聚类系数代表图谱的**局部抱团性**：高聚类+短路径=小世界结构（信息局域流通快），低聚类=星型/树型（枢纽依赖）。对综合评分（seq 417）而言，聚类系数是 5 项加权之一（mock scores.clustering 权重位 0.20）；对异常监测（seq 408）而言，局部聚类骤降是社群解体前兆。对展示系统的价值：把图谱拓扑翻译成「团块化程度」这一个数的业务语言。

### 1.3 需求文档是否给出定义方法

**需求文档提及了方向但没给公式。**SRS seq 413（指标整合）写「知识图谱分析指标、传统统计指标和机器学习模型特征进行统一管理和展示」——聚类系数作为图谱分析指标被点名纳入，但局部/全局口径、邻域定义、degree<2 处理全部未言明。UI 侧是 mock（0.68 演示值）。本件按权威定义双口径并报（§1.6）。检索记录见附录 A.2。

### 1.4 类似指标权威方法可行性分析概要

聚类系数是复杂网络科学奠基指标，权威锚三重。其一，局部聚类定义（R1 Watts & Strogatz 1998 Nature）：节点邻域实际边数/可能边数 $C_v=2t_v/[d_v(d_v-1)]$——「小世界」判据的核心统计量，本件平均局部口径的方法源；其二，全局 transitivity（R2 Newman 2003 SIAM Review）：全网三角形×3/连通三元组——闭包概率的另一种度量，与平均局部系数语义不同（前者按节点等权、后者按三元组等权）；其三，实现参照（R3 NetworkX 官方文档）：`average_clustering`/`transitivity` 双函数与 degree<2 剔除惯例——本件脚本实现的对齐基准。方法族对照：

| 方法族 | 代表 | 本库承载 | 贴合度 |
|---|---|---|---|
| 局部聚类均值（R1） | Watts & Strogatz 1998 | 本件 avg_clustering 0.234824 | **锚** |
| 全局 transitivity（R2） | Newman 2003 | 本件 transitivity 0.122238 | 高（双口径并报） |
| 实现惯例（R3） | NetworkX 文档 | 自研实现+惯例对齐 | 高（B5） |

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/tech-knowledge-graph/IndicatorDisplay.jsx:128`（Tab 挂载）；`FusionIndicatorsPanel.jsx:44-98`（消费+场景权重）；`mockData.js:373`（fusionIndicators 数组）/`:389-400`（clustering 行）。
- SRS：`gkx-orchestration/agent-delivery/bid-reference/srs/02-科技信息展示系统/科技知识图谱/指标展示.md` seq 413（excel_row 416，原文见附录 A）。
- 权威方法：R1 Watts & Strogatz 1998；R2 Newman 2003；R3 NetworkX 官方文档。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**定义（权威双口径并报——UI unit:'ratio' 0-1 语义同构）**：

$$\bar C=\frac{1}{|\{v: d_v\ge 2\}|}\sum_{v:\,d_v\ge 2}\frac{2\,t_v}{d_v(d_v-1)}\qquad\qquad T=\frac{3\times(\text{三角形数})}{(\text{连通三元组数})}$$

- $\bar C$：平均局部聚类（Watts-Strogatz；degree<2 节点 $C_v$ 无定义按惯例剔除分母并披露剔除数）
- $T$：全局 transitivity（Newman；三元组等权口径）

**待裁项**：回填 fusionValue 用哪个口径（本件建议 avg——「指标表」按指标语义更贴局部均值；transitivity 可作校验列）；三源行（graph/rule/model）的业务含义（graphValue=真图实算可即期回填，rule/model 两行无业务数据待建——与 058/063 同因）。

**降档/升档触发器（B10 模板）**：①现状真图可算（已实证）→ 维持完全转换支持；②久新物化 clustering 结果列或 dev 激活图表面 → 升**完全直接支持**；③框扩大致算力不足（全图 19,430 节点三角形枚举仍可行，暂无此虞）→ 采样估计法降级（精度换速度）。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技知识图谱/指标展示.md` |
| 所属 L4 | 融合统计指标和模型特征（seq 413-417） |
| 本件 | seq 413 指标整合的第 2 项图谱分析指标（mock 5 项之一） |
| 同族件 | 058 融合指标数（5 项计数=count(fusionIndicators)）；049（同框图统计）；053（同框中心性） |
| 近域件 | seq 417 综合评分（scores.clustering 权重位消费本件读数）；seq 415 关联分析（热力图轴） |
| UI 容器 | `FusionIndicatorsPanel`（IndicatorDisplay indicators Tab） |

本件与 058 是「计数 vs 取值」关系：058 数的是指标登记几项（本件即在 5 项之内），本件算的是第 2 项的值——MD 互引但独立留证。

## 二、计算过程

> 本件为简单统计类，本节给出**实测计算过程**——脚本 `code/M_SCIUI_KGIND_002_KGSVC_001_002_004.py` 于 2026-11-02 在久新 live 库实算（5,000 框装载+双口径计算约 6.5 秒）。

### 2.1 原料装载

主承载：久新 `ads_technology_graph_node`/`edge` 5,000 框诱导子图（ORDER BY technology_node_id LIMIT 5000 → 框内节点 4,778 个有效+38,383 条诱导边，与 049/053/057/066 同框——B11 对账键 `jiuxin_tech_sample_induced_edges=38383`）。全图边界 19,430 节点/587,252 边（live 读数）。备选：gkx `dwd_scholar_coauthor`（合作边可构图，本件未启用）；dev 26 张图表面全 0 行空壳（族级快照，非承载）。

### 2.2 聚类系数双口径实算（本件核心）

| 口径 | 实测值 | 分母口径 | 框内读数 |
|---|---|---|---|
| **平均局部聚类 $\bar C$（Watts-Strogatz）** | **0.234824** | 4,472 节点（degree≥2）等权均值 | 剔除 306 个 degree<2 节点 |
| **全局 transitivity $T$（Newman）** | **0.122238** | 连通三元组等权 | 三角形 95,131 个 |

Top10 局部聚类节点（全部 $C_v=1.0$，度 2-4 的小型全连通团）：

| 节点（name_original） | $C_v$ | 度 |
|---|---|---|
| Computational Analysis of Historical Map Data | 1.0 | 4 |
| Analytical Methods for Carotenoid Identification | 1.0 | 2 |
| Computational Analysis of Waveguide Electromagneti | 1.0 | 2 |
| Dietary and Biological Factors in Caries | 1.0 | 3 |
| Data Mining and Knowledge Discovery Processes | 1.0 | 2 |
| Clinical Diagnostic Methods for Allergy Assessment | 1.0 | 2 |
| Dynamics of Expert Knowledge and Authority | 1.0 | 2 |
| Composite Electrode Materials for Supercapacitors | 1.0 | 2 |
| Immune System Interactions in Cancer Biology | 1.0 | 2 |
| Microbial Safety in Fresh Produce Supply Chains | 1.0 | 2 |

**读数解读**：①$\bar C=0.235$ vs mock fusionValue 0.68——实测约为 mock 三分之一，mock 值不可沿用；②$\bar C$（0.235）≈ $T$（0.122）两倍——节点等权 vs 三元组等权的差：低度节点小团（$C_v$ 高）在 $\bar C$ 里放大，高度枢纽邻域（三元组多但闭合少）在 $T$ 里放大——闭包集中在学术小社群而非枢纽周围；③Top10 全 $C_v=1.0$ 且度 2-4——技术图长尾是大量微型全连通主题团（方法论对/应用对），是稀疏图（density 0.0017 同框）里聚类的主要贡献者。

### 2.3 读数解释

0.235 的业务翻译：随机图同规模同密度期望聚类≈density（≈0.002），实测高两个数量级——技术关联网有显著社群结构（非随机），但远低于社交网典型 0.6+——符合「学术主题团+跨域桥接」的领域结构。UI 场景回填建议：graphValue 列填 0.234824（avg 口径），transitivity 0.122238 作一致性校验列；fusionValue 待三源权重场景重算（现状 rule/model 两行无业务数据，融合值暂以 graph 单源标注）。

### 2.4 与 UI 演示形态的衔接

UI 现状：mock 0.68 跑真渲染（表格+权重滑杆+热力图轴全真，仅数值 mock）。接入路径：久新 node/edge → 同框装载（_s306 底座）→ 双口径计算（本件 2.2）→ `fusionIndicators` clustering 行 graphValue 回填 0.234824——前端零结构改动（值绑定即可）；rule/model 两行待业务标注流（058/063 同因）。

### 2.5 稳健性与口径敏感性

**（a）双口径差**：$\bar C$=0.235 vs $T$=0.122——若业务裁 transitivity 口径，回填值减半（B10 双态披露：两口径都落产物不可互替）。**（b）degree<2 剔除**：306 节点剔除出均值分母（$C_v$ 无定义）；若并入按 0 计，$\bar C$ 降至 0.2197（0.234824×4472/4778）——剔除惯例（NetworkX 对齐）是主口径并披露。**（c）框敏感性**：5,000 框是全图 26% 节点（按主键序确定性采样）；全图计算量级（19,430 节点三角形枚举）可行但本批未跑——框内读数作即期回填值、全图读数留作校准项。**（d）确定性**：ORDER BY 主键+sorted 邻域枚举——同框重跑逐位一致（B5）。

### 2.6 需求符合性预评（UI 演示形态 vs 实算形态衔接）

| 需求能力位（seq 413 指标整合） | UI 演示形态 | 实算形态（本件产物） | 衔接判定 |
|---|---|---|---|
| 图谱分析指标（graphValue） | mock 0.68 | **实测 0.234824/0.122238 双口径** | **即期可回填** |
| 专家规则指标（ruleValue） | mock 0.70 | 无业务数据（规则流缺位） | 待建（058 同因） |
| 模型特征指标（modelValue） | mock 0.66 | 无业务数据（模型输出流缺位） | 待建（058 同因） |
| 融合值（fusionValue） | mock 0.68 | graph 单源 0.234824 可先行 | 部分可回填（标注单源） |
| 权重配置（seq 414） | 滑杆 0.20 | 真值+真权重即期可算 | **即期可用** |
| 综合评分消费（seq 417） | scores.clustering | 0.234824 代入 | **即期可用** |

**预评结论**：graphValue 即期可回填（双口径落产物）；rule/model 两行与 fusion 全口径待业务数据（同 058 登记面缺位），按 §4.2 登记不悬空。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_KGIND_002_KGSVC_001_002_004.py`——三源只读（久新 live 直连；dev/gkx 读族级快照+探针），聚类系数自研实现（邻域交集三角形计数，_s306 底座同源），零 `demo_*`；运行 `python3 code/M_SCIUI_KGIND_002_KGSVC_001_002_004.py`（四件合算约 11 秒，本件增量约 6.5 秒）；薄壳 `python3 code/M_SCIUI_KGIND_002.py` 校验产物存在+判档+基期三键。
- 产物：`code/M_SCIUI_KGIND_002_out.json`，关键读数键与正文对应——`derived[0].avg_clustering=0.234824`/`transitivity_global=0.122238`/`triangles=95131`/`nodes=4778`/`edges=38383`/`nodes_ge2deg=4472`/`nodes_lt2deg=306`；`top10_local_clustering`（10 节点全 $C_v=1.0$）；`support_judgment="完全转换支持"`。
- 结果解读：双口径实测+mock 对比+小团结构三发现落键。
- 对照需求功能要求的评审：graphValue 即期回填、rule/model 待建，详见 §2.6。

### 2.8 分步证据对照表

| # | MD 论断（出处） | 产物键 | 读数 | 一致 |
|---|---|---|---|---|
| 1 | 框内 4,778 节点/38,383 边（§2.1） | `derived[0].nodes`/`edges` | 4778/38383 | ✓ |
| 2 | 平均局部聚类 0.234824（§2.2/摘要） | `derived[0].avg_clustering` | 0.234824 | ✓ |
| 3 | 全局 transitivity 0.122238（§2.2） | `derived[0].transitivity_global` | 0.122238 | ✓ |
| 4 | 三角形 95,131（§2.2） | `derived[0].triangles` | 95131 | ✓ |
| 5 | degree≥2 节点 4,472 / <2 节点 306（§2.2/§2.5b） | `derived[0].nodes_ge2deg`/`nodes_lt2deg` | 4472/306 | ✓ |
| 6 | Top1 Historical Map Data $C_v=1.0$ 度 4（§2.2） | `derived[0].top10_local_clustering[0]` | 1.0/deg 4 | ✓ |
| 7 | 久新全图 19,430/587,252（§2.1） | `facts.jiuxin_tech_nodes_total`/`jiuxin_tech_edges_total` | 19430/587252 | ✓ |
| 8 | 框诱导边 38,383 对账（B11） | `facts.jiuxin_tech_sample_induced_edges` | 38383 | ✓ |
| 9 | dev 图表面 26 张空壳（§〇） | `facts.dev_graph_word_table_rows` | 26 张 0 行（非零 4 张非拓扑） | ✓ |
| 10 | mock 0.68 演示值（§1.1/B9） | `facts.ui_mock_source` 源码引证 | clustering fusionValue 0.68 | ✓ |
| 11 | UI 挂载 IndicatorDisplay/FusionIndicatorsPanel（§1.1） | `IndicatorDisplay.jsx:128`/`FusionIndicatorsPanel.jsx:44` 源码引证 | Tab+面板 | ✓ |
| 12 | 判档完全转换支持（§〇/摘要） | `support_judgment` | 完全转换支持 | ✓ |

十二行对照全部以 `_out.json` 已落盘键背书（#10/#11 源码引证）。

> **基期三键说明（物理口径）**：本件基期为**物理口径基期=探针快照日**（2026-11-02 久新 live 直连当日）——聚类系数是当日图截面读数（时序对比依赖逐月快照，属 004 同因待建数据面非本件基期）；`base_years_used`/`base_years_missing` 按截面语义登记，`base_years_note` 注记此口径，不属「缺年按 0 摊入」情形。

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 图节点表 | 久新 | `ads_technology_graph_node` | **19,430** | 直查 | **足**（框 4,778 有效） |
| D2 | 图边表 | 久新 | `ads_technology_graph_edge` | **587,252** | 直查 | **足**（框诱导 38,383） |
| D3 | 聚类系数结果面 | 三源 | clustering/density 词族 | — | **不存在** | 缺（转换计算正当性来源） |
| D4 | 合作边（备选） | gkx | `dwd_scholar_coauthor` | 探针在册 | 直查 | 备选（本件未启用） |
| D5 | dev 图结构面 | dev | 26 张 | **0**（全空） | 空壳 | 非承载 |

`support_judgment="完全转换支持"`、产物与文首一致。

### 3.2 构图质量读数

| 核查项 | 读数 | 含义 |
|---|---|---|
| 采样框确定性 | ORDER BY technology_node_id LIMIT 5000 | B5 可重放 |
| 三角形计数实现 | 邻域交集法（sorted 枚举） | 与 NetworkX 惯例对齐 |
| 双口径一致性 | avg 0.235 ≈ 2×T 0.122 | 结构解读自洽（§2.2） |
| 同框对账 | 4,778/38,383 与 049/053/057/066 一致 | B11 零漂移 |

### 3.3 现场复核清单

| 复核项 | 结果 |
|---|---|
| 双口径值 | 0.234824/0.122238（B5 确定性） |
| 剔除披露 | degree<2 共 306 芽点落键 |
| 三源结果面 | 探针三件逐一留证 |
| 全图边界 | 19,430/587,252 live 读数 |
| 脚本形态 | 三源只读+纯内存图算法；零 demo_* |

## 四、数据缺失情况

### 4.1 聚类系数结果面缺失（非判定性）

三源无聚类系数结果面（absence_probe）——统计读数是计算产物，正当性来自转换计算而非直查。本件已实证结构侧可算（双口径落键）。

### 4.2 三源行的 rule/model 数据缺失（判定性约束·融合全口径）

mock 行的四值里 ruleValue 0.70/modelValue 0.66 语义为「专家规则口径值/模型特征口径值」——三源无规则流（专家规则登记面缺位，058 同因）与模型输出流（算法管线未落库）业务数据。此缺位不否定 graphValue 即期回填，但约束 fusionValue 全口径（现状仅 graph 单源可先行，须标注单源口径防误读）。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 久新物化 clustering 列 | 数据工程（轻） | 本件+058 | node 表加列或结果表落库 → 升完全直接支持 |
| 结果面口径裁定 | 口径裁定（前置） | 本件 | avg vs transitivity 择一回填 |
| 规则流/模型流落库 | 数据工程（中） | 本件+058+063 | rule/model 两行补全（fusion 全口径） |

档位后果：物化结果面 → 完全直接支持；现状 → 完全转换支持（已实证）；图结构面持续空壳且久新下线 → 降部分支持（仅剩 gkx coauthor 备选）。

## 参考文献

1. Watts D J, Strogatz S H. Collective dynamics of 'small-world' networks[J]. Nature, 1998, 393(6684): 440-442. https://doi.org/10.1038/30918 （R1，2026-11-02 检索核验可达——聚类系数奠基定义：节点邻域实际边/可能边，「小世界」判据核心统计量，本件平均局部口径的方法源）
2. Newman M E J. The structure and function of complex networks[J]. SIAM Review, 2003, 45(2): 167-256. https://doi.org/10.1137/S003614450342480 （R2，2026-11-02 检索核验可达——复杂网络综述：全局 transitivity（三角形×3/连通三元组）与平均局部系数的口径区分，本件双口径并报的方法源）
3. NetworkX Developers. Clustering — NetworkX 3.x documentation[EB/OL]. https://networkx.org/documentation/stable/reference/algorithms/clustering.html （R3，2026-11-02 检索核验可达——`average_clustering`/`transitivity` 实现惯例与 degree<2 处理，本件自研实现对齐基准）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技知识图谱/指标展示.md》seq 413（excel_row 416）：

> ### 指标整合 · 序号 413
> #### 需规功能描述
> 提供多源指标整合功能，支持将知识图谱分析指标、传统统计指标和机器学习模型特征进行统一管理和展示。

（聚类系数作为图谱分析指标被纳入统一管理，但口径/公式未定义——本件按 R1/R2 权威双口径并报。）

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 聚类系数 | UI IndicatorDisplay.jsx | :128（indicators Tab 挂 FusionIndicatorsPanel） |
| clustering | UI mockData.js | :389-400（第 2 行项，0.68 mock） |
| seedIndicators/applyScenarioWeights | UI FusionIndicatorsPanel.jsx | :44-98（消费链） |
| 聚类系数 | SRS 指标展示.md | seq 413（纳入统一管理，无公式） |
| clustering/density 词族 | 三源表名扫描 | 无结果面；node 表自带 community_id（社群归属现成） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_KGIND_002_out.json`（2026-11-02 实算：双口径+Top10）。
- 共享探针：`code/_snapshots/_probe_s307_l1_out.json`（S3-07 族级三源词族）。
- 合算脚本：`code/M_SCIUI_KGIND_002_KGSVC_001_002_004.py`；薄壳：`code/M_SCIUI_KGIND_002.py`；算法底座：`code/_s306_l3_base.py`。

### B.2 本件产物逐键清单（`code/M_SCIUI_KGIND_002_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `facts.ui_mock_source` | mock 源 | clustering 行 0.68 | §1.1 |
| `facts.dev_graph_word_table_rows` | dev 空壳证据 | 26 张行数 | §〇/§3.1 D5 |
| `facts.jiuxin_tech_nodes_total`/`jiuxin_tech_edges_total` | 全图边界 | 19430/587252 | §2.1 |
| `facts.jiuxin_tech_sample_induced_edges` | 同框对账键 | 38383 | §2.1（B11） |
| `derived[0].avg_clustering` | **实算值** | 0.234824 | §2.2 |
| `derived[0].transitivity_global` | **实算值** | 0.122238 | §2.2 |
| `derived[0].triangles` | 实算值 | 95131 | §2.2 |
| `derived[0].nodes_ge2deg`/`nodes_lt2deg` | 剔除披露 | 4472/306 | §2.5b |
| `derived[0].top10_local_clustering` | Top10 | 全 1.0 小团 | §2.2 |
| `absence_probe` | 探针 | 三件 | §4.1 |
| `support_judgment` | 判档 | 完全转换支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 本库承载 | 贴合度 |
|---|---|---|---|
| 局部聚类均值 | R1 Watts & Strogatz 1998 | avg 0.234824 | 锚 |
| 全局 transitivity | R2 Newman 2003 | 0.122238 | 高（双口径） |
| 实现惯例 | R3 NetworkX | 自研对齐 | 高（B5） |

### C.2 数据矩阵

| 依赖 | dev | gkx | jiuxin |
|---|---|---|---|
| 图节点/边 | 空壳 | coauthor（备选） | **19,430/587,252** |
| 聚类结果面 | 无 | 无 | 无（node 表有 community_id 无 clustering） |
| 规则流/模型流 | 无 | 无 | 无 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v0（现状） | mock 0.68 | — |
| v1（**本件已验证**） | graphValue 回填 0.234824（标注单源） | 口径裁定（avg 建议） |
| v2 | 久新物化 clustering 列 | 数据工程（轻） |
| v3 | rule/model 流落库+fusion 全口径 | 规则流/模型流（中） |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 口径混用（avg vs T） | 中 | 双口径并报+回填裁定单口径 |
| mock 0.68 误当读数 | 中 | §2.2 对比披露+B9 |
| rule/model 行长期 mock | 低 | §4.2 登记与 058 同因同修 |

### C.5 总判

**完全转换支持**：三源无结果面但久新真图即期可算（双口径 0.234824/0.122238 落键）——graphValue 可即期回填（标注单源口径），物化结果列即升完全直接支持；rule/model 两行与 058 同因待建。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_KGIND_002_KGSVC_001_002_004.py` | 退出码 0，落四件 _out.json |
| 薄壳校验 | `python3 code/M_SCIUI_KGIND_002.py` | verified 完全转换支持 |
| 实算一致 | `derived[0].avg_clustering` | 0.234824 |
| B11 对账 | 4,778/38,383 与 049/053/057/066 | 零漂移 |
| 幂等重跑 | B5（主键采样+sorted 枚举） | 逐位一致 |
| §二 实算 | 完全转换支持档 | 有真实计算过程 |
