# 图谱综合得分（M_SCIUI_KGANALY_049）

> **类型**：无业务逻辑数值类（多指标加权合成，图算法）｜ **域**：科技信息展示系统·科技知识图谱·中心性计算展示·多维度综合分析｜ **UI 挂载**：中心性面板 → `CentralityPanel.jsx:599` 排序字段下拉第三项「综合分」（`composite` 列）；算法真身 `centralityAlgo.js:361-468 runCentralityAnalysis`——度/紧密/中介/PageRank 四维 min-max 归一后加权合成（默认权重各 25%，`centralityAlgo.js:365`）；表格列 `CentralityPanel.jsx:519`「综合」、节点详情抽屉 `:874`「综合分」、异常预警 `:647`「综合分变化」均消费该列
> **数据支持度**：**完全转换支持**（久新真图 5,000 框诱导子图 4,778 节点/38,383 边框内实算——Brandes 全源中介+BFS 全源紧密+PR 36 迭代收敛，四维归一加权合成 Top1=0.845943；三源无现成 composite 结果面，但依赖侧结构+数据量均足）｜ **公式定义人**：UI 前端算法（`runCentralityAnalysis` 真实现，非 mock）——本件按同构算法在真图复算，权威口径锚定｜ **口径归属**：UI 拆件叶（SRS seq 436 多维度综合分析的功能组成维），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_KGANALY_049_050_052.py`（049/050/052 合算）｜ **产物**：`code/M_SCIUI_KGANALY_049_out.json`（四维原值+归一合成+Top10+分布）
> **四判定摘要**：直接结构 = 无 composite 结果面（absence_probe）；直接数据 = 无落库读数；依赖结构 = **足**（node+edge 表可构图）；依赖数据 = **足**（19,430 节点/587,252 边真图，框内实算通过）
> **数据源口径**：三源（dev live `gkxlumenx_*` + 三方库 gkx + 久新 `gkx_technology_analysis_dev` live）逐一探针留证；久新 2026-11-02 当日 live 直连实算；`demo_*` 禁引。

> **铁律：本指标所有信息，均以第二章的“最新指标调研报告”为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全转换支持。**证据链：①久新 `ads_technology_graph_node`+`ads_technology_graph_edge` 真图全量在库（19,430/587,252，`jiuxin_tech_nodes_total`/`jiuxin_tech_edges_total`）；②三源无 composite/centrality 结果面（absence_probe 词族扫描零命中）——综合得分是前端算法产物，须构图转换计算，正当性即「完全转换」档；③本件已在 5,000 框诱导子图（4,778 节点/38,383 边）实算四维中心性+归一加权合成（Brandes 全源 O(VE) 框内 78 秒收敛，PR 36 迭代 diff 8.3e-07）——「现在就能算」已实证；④dev 26 张图表面全 0 行空壳（族级快照）。

### 批次通用纪律摘要（S3-06 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 合成是加权和非相除；分布 min/max/mean 同框披露 |
| B4 | 负结论带探针 | absence_probe 三件；dev 空壳族级快照 |
| B5 | 确定性 | BFS/Brandes 邻居 sorted 序；PR 收敛判据落键；框 ORDER BY node_id |
| B6 | 闸门自身被闸 | 不自跑闸门 |
| B7 | 产物只由脚本产出 | 本件 py 实算出 _out.json |
| B8 | 回执不复收 | 同框重跑逐位一致（B5 保证） |
| B9 | 单位/日期陷阱 | 综合分无量纲 0-1；UI 的 72-96「分」是资产 KPI 另一指标（§1.1 辨析） |
| B10 | 口径裁定保守交付 | UI 公式 PR×5 放大 vs 本件纯归一——双口径披露（§2.5a） |
| B11 | 多本账互推 | 与 039/040 同框（38,383 边）；PR 与 001 全图 Top 域呼应 |

### 判档自检三问（本件 = 完全转换支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有综合得分结果列吗？ | 无 | absence_probe（composite/centrality/score 词族零命中） |
| 构图原料够吗？ | **够（全量真图）** | 久新 19,430 节点/587,252 边（§3.1） |
| 现在就能算吗？ | **已实算（框内 78 秒）** | Top1 composite 0.845943（§2.2） |

## 摘要

「图谱综合得分」是中心性面板的多维合成读数：度/紧密/中介/PageRank 四维中心性各自 min-max 归一到 0-1 后按权重（UI 默认各 25%）加权和——`centralityAlgo.js:399-401` 前端真实现（非 mock），表格「综合」列、排序键、异常预警（Δ≥0.12 骤升降）三处消费。数据侧判定：**完全转换支持**——三源无 composite 结果面，但久新真图可构图实算。本件在 5,000 框诱导子图（4,778 节点/38,383 边）复算：Top1「Computational Methods for Biological Sequence Comparison」综合分 **0.845943**（原始度 832/紧密 0.479393/中介 2,446,338.67/PR 0.008913 四维全头部），第二梯队 0.449439 起断崖式回落；全框分布 min 0.000997/max 0.845943/mean 0.050878——典型幂律头部效应。核心发现：①UI 公式对 PR 维乘 5 放大（`p*5` 后再归一加权）与标准 min-max 归一口径不同，接入真数据时须裁口径；②孤立二点社群（closeness=1.0/低度）在纯归一口径下综合分≈0.254 挤进 Top10 尾部——min-max 归一对「小圈子满分维」的偏置是口径敏感点。

- 需求判定：UI 拆件叶（seq 436 多维度综合分析的功能组成维——综合分列）。
- 复现状态：脚本已实算通过；四维原值+归一合成+Top10+分布全落产物。
- 档位结论：**完全转换支持**。
- 关键事实：框内实算与 UI 算法同构（Brandes/BFS/PR 全源）；PR 36 迭代收敛 diff 8.3e-07 与 001 全图 38 迭代同收敛族；两口径（UI PR×5 vs 纯归一）读数不同但排序头部稳定。
- 降档风险：无；升档路径：composite 结果面落表（夜批算好 Top-N）→ 完全直接支持。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统/科技知识图谱/中心性计算展示——`CentralityPanel.jsx` 五 Tab（度/紧密/中介/PageRank/综合对比）分析面板。本件挂「综合分」三处：其一，排序字段下拉 `:596-600` 第三项 `{value: 'composite', label: '综合分'}`；其二，表格「综合」列 `:519`（蓝 Tag）；其三，节点详情抽屉 `:874`「综合分」+ 异常预警卡 `:647`「综合分变化」。算法真身在 `centralityAlgo.js:361-468 runCentralityAnalysis`：`computeDegree/computeCloseness/computeBetweenness/computePageRank` 四算子全图计算后 `:399-401` 合成。注意辨析：图查询资产抽屉 KPI 行「综合评分」（`queryAssetDeepAnalysis.js:25` seededInt 72-96「分」）是**另一指标形态**（资产体检整数评分），本件是中心性面板的 0-1 连续综合分——两者同名异构，勿混引。

### 1.2 为什么需要本指标

单维中心性各说各话：度高=连接多（但不一定是桥）、中介高=必经之路（但边缘点可为 0）、PR 高=被重要者指向（但不问位置）、紧密高=离谁都近（但忽略流量）。综合分回答「综合看谁最重要」——四维归一加权后一张榜单排序，管理场景用途：关键节点识别（Top-N 榜单）、异常监测（综合分骤升降 Δ≥0.12 预警）、权重敏感性实验（compare Tab 四滑杆调权重看榜单变化）。对展示系统的价值：把四 Tab 的分散读数合成一列，支撑「影响力节点速览」的运营叙事。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**SRS《算法展示.md》seq 436 写「整合多维度中心性指标，通过加权计算形成综合评分」（附录 A）——维度清单、归一方法、权重方案全部未言明。UI 前端 `runCentralityAnalysis` 给出了完整真实现（min-max 归一+四维等权+PR×5 放大），是**事实上的公式定义人**；本件按权威多指标合成方法（min-max 归一+线性加权）锚定，UI 的 PR×5 偏置作口径差披露。检索记录见附录 A.2。

### 1.4 类似指标权威方法可行性分析概要

多指标加权合成是决策科学/网络分析的标准方法，权威锚三重。其一，中心性方法族（R1 Freeman 1978「Centrality in social networks: Conceptual clarification」）：度/紧密/中介三经典中心性的奠基定义与「无单一最优中心性」结论——综合合成的动机来源；其二，TOPSIS/加权和法（R2 Hwang & Yoon 1981 多属性决策）：属性归一后加权聚合的规范框架——UI min-max+线性加权是其在网络中心性上的实例；其三，PageRank（R3 Brin & Page 1998）：第四维 PR 的方法源（本件与 001 同构实现）。方法族对照：

| 方法族 | 代表 | 本库承载 | 贴合度 |
|---|---|---|---|
| 三经典中心性（R1） | Freeman 1978 | UI computeDegree/Closeness/Betweenness 已实现+本件真图复算 | **锚** |
| 归一加权合成（R2） | Hwang & Yoon 1981 | UI :399-401 min-max+线性加权；本件同构 | **锚** |
| PageRank（R3） | Brin & Page 1998 | UI computePageRank+本件 36 迭代收敛 | 高（第四维） |
| 上游结果面 | 三源 | 无 composite 结果列 | 无（转换计算正当性） |

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/tech-knowledge-graph/CentralityPanel.jsx:596-600`（排序键）/`:519`（综合列）/`:874`（详情）/`:647`（预警）；`centralityAlgo.js:361-468`（runCentralityAnalysis 全实现）。
- SRS：`gkx-orchestration/agent-delivery/bid-reference/srs/02-科技信息展示系统/科技知识图谱/算法展示.md` seq 436（excel_row 439，原文见附录 A）。
- 权威方法：R1 Freeman 1978；R2 Hwang & Yoon 1981；R3 Brin & Page 1998。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**定义（本件实算口径，推测定义——UI 公式同构去除 PR×5 偏置）**：

$$\text{composite}(v)=w_d\cdot\hat{d}(v)+w_c\cdot\hat{c}(v)+w_b\cdot\hat{b}(v)+w_p\cdot\hat{p}(v),\quad w_\ast\text{ 归一后 }\sum w=1$$

其中 $\hat{\cdot}$ 为各维框内 min-max 归一：$\hat{x}(v)=(x(v)-\min)/(\max-\min)$；默认 $w_d=w_c=w_b=w_p=0.25$。紧密=BFS 全源、中介=Brandes（无权无向，score 除 2）、PR=power iteration（damping 0.85，收敛 1e-06）。

**待裁项**：PR 维是否乘 5 放大（UI `:400` `p*5` vs 本件纯归一——§2.5a）；权重方案（等权 25% 是默认非需求钦定）；归一域（全图 vs 框内 vs 展示子集——UI 注释「计算仍在全图上进行」）。

**降档/升档触发器（B10 模板）**：①现状框内可算（已实证）→ 维持完全转换支持；②composite 结果面落表（夜批 Top-N）→ 升**完全直接支持**；③甲方裁定权重/PR×5 口径 → 判档不变、公式唯一化；④久新下线 → gkx coauthor 图可算（语义换合作网中心性），维持转换档。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技知识图谱/算法展示.md` |
| 所属 L5 | 中心性计算展示（seq 435-437，5 叶）+ 多维度综合分析（UI 拆件） |
| 本件 | seq 436 多维度综合分析的功能组成维（composite 合成列） |
| 同族件 | KGANALY_001 PageRank（第四维同源实现）、KGANALY_039 密度（同框构图）、KGANALY_040 聚类（同框）、KGANALY_023 社群连接密度（CommunityPanel 侧） |
| 近域件 | seq 435 中心性多算法（四算子实现位）；图查询资产 KPI「综合评分」（同名异构辨析 §1.1） |
| UI 容器 | `CentralityPanel.jsx` 五 Tab 框架 |

本件是中心性族四件（001/039/040/049）的合流点：前三件各自验证单维算子（PR/密度/聚类），本件把度/紧密/中介/PR 四维在同一采样框内合成——同框构图（4,778 节点/38,383 边）保证四维可比，是「一族指标一套原料」的族级复用实证。

## 二、计算过程

> 本件为无业务逻辑数值类，本节给出**实测计算过程**——脚本 `code/M_SCIUI_KGANALY_049_050_052.py` 于 2026-11-02 在久新 live 库实算（Brandes 全源 O(VE) 框内约 78 秒）。

### 2.1 原料装载

主承载：久新 `ads_technology_graph_node` ORDER BY technology_node_id LIMIT 5000 的确定性采样框（B5）+ 框内诱导子图（`WHERE source IN 框 AND target IN 框`）——去孤立点后 **4,778 节点/38,383 边**（canonical (min,max) 去重排序），与 039/040/046/051 同框（B11 对账键 `jiuxin_tech_sample_induced_edges=38383`）。node 表 19,430/edge 表 587,252 全量在库作边界披露。备承载：gkx `dwd_scholar_coauthor` 20,000 行框（合作网中心性可扩，本件未算——语义偏「人」不偏「图资产」，登记为扩展项）。

### 2.2 四维中心性+归一合成实算（本件核心）

| 节点（框内 Top10 by composite） | 综合分 | 度(原始) | 紧密 | 中介 | PageRank |
|---|---|---|---|---|---|
| Computational Methods for Biological Sequence Comparison | **0.845943** | 832 | 0.479393 | 2,446,338.67 | 0.008913 |
| Hardware Architectures for Machine Learning Acceleration | 0.449439 | 481 | 0.42668 | 774,190.28 | 0.005207 |
| Deep Learning Architectures for Object Detection | 0.366092 | 402 | 0.410025 | 442,696.53 | 0.004469 |
| Support Vector Machine Algorithms and Applications | 0.319481 | 311 | 0.4241 | 522,662.21 | 0.003348 |
| Large-scale deep learning model training | 0.280795 | 288 | 0.406599 | 330,305.84 | 0.003102 |
| Equatorial Electrojet and Ionospheric Magnetic Variations | 0.258142 | 3 | 1.0 | 2.0 | 0.000307 |
| Gene Ontology and Functional Annotation Resources | 0.25544 | 268 | 0.413904 | 260,855.49 | 0.002591 |
| Mineral Scale Management in Oilfields | 0.254787 | 1 | 1.0 | 0 | 0.000209 |
| Calcium Sulfate Mineral Growth and Applications | 0.254787 | 1 | 1.0 | 0 | 0.000209 |
| Geothermal Energy Pile Infrastructure Systems | 0.254787 | 1 | 1.0 | 0 | 0.000209 |

全框分布：min **0.000997** / max **0.845943** / mean **0.050878**（4,778 节点）。PR 收敛：**36 迭代**，final_diff **8.32403e-07**（`jiuxin_composite_pagerank_iters`/`final_diff`）。

**头部效应解读**：Top1 序列比对是四维全头部节点（度 832 框内第一/中介 244 万框内第一/紧密 0.479 头部/PR 0.0089 头部）——归一后四维近似满分合成 0.846；第二名起断崖（0.449 仅为 Top1 的 53%）——技术关联图的中心性呈强幂律，与 001 全图 PR 的头部分布一致（B11）。**孤立二点社群偏置**：排名 6/8/9/10 的低度节点（度 1-3/紧密 1.0）综合分≈0.254-0.258 挤进 Top10——min-max 归一下「小圈子满分紧密维」贡献 0.25 固定底分，此为归一法固有偏置（§2.5b 口径敏感点）。

### 2.3 读数解释

综合分 Top10 里 AI/ML 域技术占 5 席（硬件加速/目标检测/SVM/大规模训练/基因本体），生信序列比对居首——技术关联图的「基础方法型」节点（被全领域引用的工具性技术）综合分最高，与「领域热点型」节点（度集中但中介低）形成结构差异。mean 0.0509 vs max 0.8459（16.6 倍差）说明绝大多数节点是长尾——综合分榜单的价值正在于把 4,778 个节点压成一张可扫的 Top-N 榜。UI 场景回填建议：Top1 的 0.846 直接可入「高影响力节点排序」表；异常预警功能需历史快照对比（UI HISTORY_VERSIONS 机制），真图首次接入建议先落基线快照。

### 2.4 与 UI 演示形态的衔接

UI 现状：mock 图（专家/机构/技术节点）跑真算法——`runCentralityAnalysis` 输入换真图邻接表即可，算法零改动。接入路径：久新 node/edge 表 → 诱导子图构建（本件 2.1 流程）→ 四算子+合成（本件 2.2）→ rows 回填。注意 UI 的 `p*5` 放大与排序圆整（`:399-401` toFixed(4)）——接入时建议按本件纯归一口径重算或显式保留 UI 偏置（§2.5a 两口径菜单）。

### 2.5 稳健性与口径敏感性

**（a）PR×5 口径差**：UI `centralityAlgo.js:400` 对 PR 维乘 5（`(p * 5) * nw.pagerank`）——因各维已 min-max 归一到 0-1，乘 5 后 PR 维实际贡献上限达 1.25w_p（等权时占合成上限 31.25%）——非等权偏置。本件按纯归一（四维各贡献上限 w_*=0.25）实算，两口径对头部排序影响有限（Top5 域不变），但中段排序会变——接入前须裁口径（B10 双口径披露不悬空）。**（b）孤立二点偏置**：§2.2 已述——紧密维对 K2 社群恒 1.0，低度节点获 0.25 固定底分；缓解方案：展示层过滤度≥阈值（UI 有 degreeRaw 排序键可配合）或改分位数归一（工程扩展项）。**（c）框效应**：中介/紧密是全路径度量，5,000 框截断会切断跨框路径——本件框内值是「框内拓扑口径」非全图口径（边界披露；全图 Brandes O(19,430×587,252) 代价高，夜批可扩）；PR 框内 36 迭代 vs 001 全图 38 迭代同收敛族（B11 呼应）。**（d）确定性**：BFS/Brandes 邻居访问 sorted 序、PR 初值均匀+收敛判据落键——同框重跑逐位一致（B5）。

### 2.6 需求符合性预评（UI 演示形态 vs 实算形态衔接）

| 需求能力位（seq 436 多维度综合分析） | UI 演示形态 | 实算形态（本件产物） | 衔接判定 |
|---|---|---|---|
| 综合分列/排序键 | composite 列+排序下拉 | 框内 Top10+全分布 | **即期可回填** |
| 权重可调（compare Tab 滑杆） | 四滑杆 | 本件等权实算；权重向量参数化 | 调权重即重算，零结构改动 |
| 异常预警（Δ≥0.12） | HISTORY_VERSIONS 快照 | 真图首次接入需落基线快照 | 前置：基线快照机制 |
| 报表导出 | exportCentralityReport | 产物 JSON 同构 | 直接可导 |

**预评结论**：数据面即期可用；PR×5 口径裁定与基线快照机制是两个前置项，按 §2.5a 菜单交付不悬空。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_KGANALY_049_050_052.py`——三源只读（久新 live 直连；gkx 经 `_gkxdb.py`；dev 读族级快照），BFS/Brandes/PR/合成全自研实现（`_s306_l3_base.py` 底座），零 `demo_*`；运行 `python3 code/M_SCIUI_KGANALY_049_050_052.py`（约 150 秒，Brandes 占 78 秒）。
- 产物：`code/M_SCIUI_KGANALY_049_out.json`，关键读数键与正文对应——`facts.jiuxin_tech_sample_induced_edges=38383`/`jiuxin_composite_weights`（四维 0.25）/`jiuxin_composite_pagerank_iters=36`/`jiuxin_composite_pagerank_final_diff=8.32403e-07`；`derived[0].nodes=4778`/`edges=38383`/`composite_top10`（Top1 0.845943 全维明细）/`composite_distribution={min:0.000997, max:0.845943, mean:0.050878}`；`support_judgment="完全转换支持"`。
- 结果解读：四维中心性框内全算+归一合成——头部幂律（Top1 断崖领先）、孤立二点偏置（0.25 底分）、PR×5 口径差三发现全落键。
- 对照需求功能要求的评审：数据即期可用，PR×5 口径裁定+基线快照两前置，详见 §2.6。

### 2.8 分步证据对照表

| # | MD 论断（出处） | 产物键 | 读数 | 一致 |
|---|---|---|---|---|
| 1 | 框内 4,778 节点/38,383 边（§2.1） | `derived[0].nodes`/`edges` | 4778/38383 | ✓ |
| 2 | Top1 综合分 0.845943（§2.2/摘要） | `derived[0].composite_top10[0].composite` | 0.845943 | ✓ |
| 3 | Top1 四维原值（§2.2） | `composite_top10[0]` degree_raw/closeness/betweenness/pagerank | 832/0.479393/2446338.672237/0.008913 | ✓ |
| 4 | 分布 min/max/mean（§2.2） | `derived[0].composite_distribution` | 0.000997/0.845943/0.050878 | ✓ |
| 5 | PR 36 迭代（§2.2/§2.5c） | `facts.jiuxin_composite_pagerank_iters` | 36 | ✓ |
| 6 | PR final_diff 8.3e-07（§2.2） | `facts.jiuxin_composite_pagerank_final_diff` | 8.32403e-07 | ✓ |
| 7 | 等权 0.25×4（§1.6/§2.2） | `facts.jiuxin_composite_weights` | 各 0.25 | ✓ |
| 8 | 久新全图 19,430/587,252（§2.1） | `facts.jiuxin_tech_nodes_total`/`jiuxin_tech_edges_total` | 19430/587252 | ✓ |
| 9 | 与 039/040 同框 38,383（B11） | 与 039/040 `jiuxin_tech_sample_induced_edges` 对账 | 38383=38383 | ✓ |
| 10 | UI PR×5 口径差（§2.5a） | `centralityAlgo.js:400` 源码引证 | `(p * 5) * nw.pagerank` | ✓ |
| 11 | 孤立二点 0.254787 底分（§2.2/§2.5b） | `composite_top10[7-9].composite` | 0.254787×3 | ✓ |
| 12 | 判档完全转换支持（§〇/摘要） | `support_judgment` | 完全转换支持 | ✓ |

十二行对照全部以 `_out.json` 已落盘键背书（#10 源码引证、#9 跨件对账）。

> **基期三键说明（物理口径）**：本件基期为**物理口径基期=探针快照日**（2026-11-02 久新 live 直连当日），**无年度基期**——中心性合成是当日图截面读数（异常预警的时序对比依赖历史快照机制，属 UI 工程项非数据基期）；`base_years_used`/`base_years_missing` 按截面语义登记，`base_years_note` 注记此口径，不属「缺年按 0 摊入」情形。

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 图节点表 | 久新 | `ads_technology_graph_node` | **19,430** | 直查 | **足**（构图主料） |
| D2 | 图边表 | 久新 | `ads_technology_graph_edge` | **587,252** | 直查 | **足**（四维算子原料） |
| D3 | composite 结果面 | 三源 | composite/centrality/score 词族 | — | **不存在** | 缺（转换计算正当性来源） |
| D4 | 合作网（备选语义） | gkx | `dwd_scholar_coauthor` | 1,187,606 | 直查 | 足（扩展项，本件未算） |
| D5 | dev 图结构面 | dev | 26 张 | **0**（全空） | 空壳 | 非承载 |

`support_judgment="完全转换支持"`、产物与文首一致。

### 3.2 构图质量读数

| 核查项 | 读数 | 含义 |
|---|---|---|
| 采样框确定性 | ORDER BY technology_node_id LIMIT 5000 | B5 可重放 |
| 诱导边 canonical 去重 | (min,max) 排序去重 | 与 039/040/046/051 同框零漂移 |
| 框内连通性 | 孤立点剔除后 4,778 活跃节点 | 度 0 节点不参与中心性 |
| PR 收敛性 | 36 迭代/diff 8.3e-07 | 收敛判据落键（非截断迭代） |

### 3.3 现场复核清单

| 复核项 | 结果 |
|---|---|
| 框内四维+合成 | Top1 0.845943（B5 确定性） |
| PR 收敛 | 36 迭代/diff 8.3e-07 |
| 全图边界 | 19,430/587,252 live 读数 |
| dev 图表 | 26 张全 0 行（族级快照） |
| 脚本形态 | 三源只读+纯内存图算法；零 demo_* |

## 四、数据缺失情况

### 4.1 composite 结果面缺失（非判定性）

三源无 composite/centrality 结果面（absence_probe）——综合得分是算法派生读数，须构图转换计算。修复最轻量：夜批在框/全图上跑四算子+合成落 `graph_stats` 表（Top-N 即可，UI 榜单场景不需要全量落库）。

### 4.2 口径二态与快照机制（口径级）

待裁项：其一，**PR×5 偏置**（UI `:400` vs 本件纯归一——§2.5a 双口径菜单）；其二，**归一域**（框内 vs 全图——中介/紧密全图计算代价高，工程上夜批全图+在线框内是常见分层）；其三，**异常预警基线快照**（UI HISTORY_VERSIONS 是 mock 快照，真图接入需真实基线落盘机制）。均非数据缺失，属口径/工程前置项。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| PR×5 口径裁定 | 口径裁定 | 本件 | 回填前置（双口径菜单 §2.5a） |
| 夜批 Top-N 综合分落表 | 数据工程（轻） | 本件+001 | 升完全直接支持 |
| 基线快照机制 | 前端工程（轻） | 本件（预警功能） | 首接入先落基线 |
| 全图 Brandes（可选） | 数据工程（中） | 本件+中介维 | 夜批可扩，非判档依赖 |

档位后果：结果面落表 → 完全直接支持；现状 → 完全转换支持（框内已实算）；久新下线 → gkx 合作网可算（语义换），维持转换档。

## 参考文献

1. Freeman L C. Centrality in Social Networks: Conceptual Clarification[J]. Social Networks, 1978-79, 1(3): 215-239. https://doi.org/10.1016/0378-8733(78)90021-7 （R1，2026-11-02 WebSearch 核验可达——度/紧密/中介三中心性奠基与「无单一最优」结论，综合合成的动机源）
2. Hwang C L, Yoon K. Multiple Attribute Decision Making: Methods and Applications[M]. Berlin: Springer-Verlag, 1981. https://doi.org/10.1007/978-3-642-48318-9 （R2，2026-11-02 WebSearch 核验可达——多属性决策归一加权框架，UI min-max+线性加权的方法源）
3. Brin S, Page L. The Anatomy of a Large-Scale Hypertextual Web Search Engine[J]. Computer Networks and ISDN Systems, 1998, 30(1-7): 107-117. https://doi.org/10.1016/S0169-7552(98)00110-X （R3，2026-11-02 WebSearch 核验可达——PageRank 原始论文，第四维方法源，与 001 同构实现）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技知识图谱/算法展示.md》seq 436（excel_row 439）：

> ### 多维度综合分析 · 序号 436
> #### 需规功能描述
> 整合多维度中心性指标，通过加权计算形成综合评分，为关键节点识别和多维度影响力评估提供统一标尺。

（「综合评分」的维度清单/归一法/权重未定义——UI 前端 `runCentralityAnalysis` 是事实定义人；本件按权威方法锚定+口径差披露。）

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 综合分/composite | UI CentralityPanel.jsx | :519/:574-581/:599/:874（多处消费） |
| composite 公式 | UI centralityAlgo.js | :399-401（min-max 归一+加权+PR×5） |
| 多维度综合 | SRS 算法展示.md | seq 436（一句功能描述，无算法定义） |
| composite/centrality 词族 | 三源表名扫描 | 零命中（无结果面） |
| 综合评分（同名辨析） | UI queryAssetDeepAnalysis.js | :25 seededInt 72-96（另一指标形态） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_KGANALY_049_out.json`（2026-11-02 实算：四维+合成）。
- 共享探针：`code/_snapshots/_probe_s305_l3_call_out.json`。
- 合算脚本：`code/M_SCIUI_KGANALY_049_050_052.py`；算法底座：`code/_s306_l3_base.py`。

### B.2 本件产物逐键清单（`code/M_SCIUI_KGANALY_049_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `facts.jiuxin_tech_nodes_total`/`jiuxin_tech_edges_total` | 全图边界 | 19,430/587,252 | §2.1/§3.1 |
| `facts.jiuxin_tech_sample_induced_edges` | 同框对账键 | 38,383 | §2.1（B11） |
| `facts.jiuxin_composite_weights` | 口径 | 四维各 0.25 | §1.6/§2.2 |
| `facts.jiuxin_composite_pagerank_iters` | 收敛 | 36 | §2.2 |
| `facts.jiuxin_composite_pagerank_final_diff` | 收敛 | 8.32403e-07 | §2.2 |
| `derived[0].composite_top10` | **实算值** | Top1 0.845943 全维明细 | §2.2 |
| `derived[0].composite_distribution` | 分布 | 0.000997/0.845943/0.050878 | §2.2/§2.3 |
| `absence_probe` | 探针 | 三件 | §4.1 |
| `support_judgment` | 判档 | 完全转换支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 本库承载 | 贴合度 |
|---|---|---|---|
| 三经典中心性 | R1 Freeman 1978 | UI 实现+本件真图复算 | 锚 |
| 归一加权合成 | R2 Hwang & Yoon 1981 | UI :399-401+本件同构 | 锚 |
| PageRank | R3 Brin & Page 1998 | UI+本件 36 迭代收敛 | 高 |
| 上游结果面 | 三源 | 无 | 无（转换正当性） |

### C.2 数据矩阵

| 依赖 | dev | gkx | jiuxin |
|---|---|---|---|
| 图节点/边 | 空壳 | coauthor（备选语义） | **19,430/587,252** |
| composite 结果面 | 无 | 无 | 无 |
| 历史快照（预警用） | 无 | 无 | 无（工程机制项） |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v0（现状） | mock 图跑真算法 | — |
| v1（**本件已验证**） | 真图框内综合分回填 | PR×5 口径裁定 |
| v2 | 夜批 Top-N 落表（升完全直接支持） | 轻量 |
| v3 | 基线快照+异常预警真数据 | 快照机制 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| PR×5 口径未裁即回填 | 中 | §2.5a 双口径菜单 |
| 孤立二点 0.25 底分误读 | 中 | §2.5b 展示层度过滤/分位数归一 |
| 全图中介代价误估（在线算） | 低 | 夜批分层方案（§4.3） |

### C.5 总判

**完全转换支持**：三源无结果面但真图全量在库，框内四维+合成已实算（Top1 0.845943 幂律头部+两口径差+偏置三发现落键）——回填菜单齐备，前置仅口径裁定。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_KGANALY_049_050_052.py` | 退出码 0，落三件 _out.json |
| 实算一致 | `derived[0].composite_top10[0].composite` | 0.845943 |
| B11 对账 | 同框 38,383 与 039/040/046/051 一致 | 零漂移 |
| 幂等重跑 | B5（sorted 邻居+PR 收敛判据） | 逐位一致 |
| §二 实算 | 完全转换支持档 | 有真实计算过程 |
