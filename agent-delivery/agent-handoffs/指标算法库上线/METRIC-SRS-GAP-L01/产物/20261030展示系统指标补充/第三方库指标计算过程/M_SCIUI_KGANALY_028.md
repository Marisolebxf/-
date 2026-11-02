# 图谱异常评分（M_SCIUI_KGANALY_028）

> **类型**：无业务逻辑数值类（图算法实算型——度偏离异常评分）｜ **域**：科技信息展示系统·科技知识图谱·分析展示·智能化分析·模式识别·异常点 Tab｜ **UI 挂载**：`pages/tech-knowledge-graph/KgIntelligenceHub.jsx:111`（异常分列，anomalyColumns data dataIndex=`score`）；算法源 `kgIntelligence.js:213-255` detectPatternsAndAnomalies
> **数据支持度**：**完全转换支持**（久新真图可实算——UI 算法（度均值倍率线性映射+阈值检出）在采样框上 1:1 同构复刻，513 节点超阈值检出落产物）｜ **公式定义人**：UI 前端算法（`detectPatternsAndAnomalies`：score=min(99, round(d/avg×28))，threshold=max(avg×2.1, 4)）——SRS seq 404 未给参数，参数以 UI 算法为准｜ **口径归属**：需求明列叶（seq 404「自动识别图谱中的异常点」，异常评分是其量化读数；row_01=491）
> **复现脚本**：`code/M_SCIUI_KGANALY_028.py`｜ **产物**：`code/M_SCIUI_KGANALY_028_out.json`（含 4,778 节点评分+Top10 双口径）
> **四判定摘要**：直接结构 = 无现成异常结果面（三源词族 anomal/abnorm/outlier 0 命中）；直接数据 = 无（同左）；依赖结构 = **足**（久新 node/edge 表结构齐备，度可算）；依赖数据 = **足**（采样框 4,778 节点/38,383 边实算）
> **数据源口径**：三源（dev live `gkxlumenx_*` + 三方库 gkx + 久新 `gkx_technology_analysis_dev` live 218 表）逐一探针留证；久新 2026-11-02 当日 live 直连实算；`demo_*` 禁引；UI 演示回填（isDemo）自披露不入实算。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全转换支持。**三源无现成「图谱异常评分」结果面（absence_probe 四件：久新 218 表词族 0 命中/gkx 企业异常目录为主体级非节点评分/dev 图表面 0 行/UI 演示回填自披露），但图原料真实且量足：久新采样框诱导子图 4,778 节点/38,383 边，UI 算法（度均值倍率线性映射+2.1 倍阈值检出）**现在就能算**——本件已实算：4,778 节点全评分，513 节点（10.74%）超阈值，Top1 z-score=30.09（Computational Methods for Biological Sequence Comparison，度 832）。结构与数据量均足，判完全转换支持。

### 批次通用纪律摘要（S3-06 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（§2.8 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 评分分母 max(avg,1) 框内同基；z-score 分母 σ 同框 |
| B4 | 负结论带探针 | absence_probe 四件（久新无结果面/gkx 语义排除/dev 空壳/UI 回填自披露） |
| B5 | 确定性 | 节点框 ORDER BY id LIMIT 5000；Top10 排序（分降序、同分 id 升序）；阈值公式写死 |
| B7 | 产物只由脚本产出 | 本件 py 实算出 _out.json |
| B9 | 单位/日期陷阱 | 分值无量纲（0-99）；度分布重尾（σ=27.11>μ=16.07）披露 |
| B10 | 口径裁定保守交付 | 线性映射（UI 同构）为主、z-score 为交叉验证副口径 |
| B11 | 多本账互推 | 框 4,778/38,383 与族级 KGANALY_001/025-027 同源同框 |

### 判档自检三问（本件 = 完全转换支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有现成异常评分结果表吗？ | 无 | absence_probe（4 件） |
| 度偏离评分原料结构与数据量够吗？ | **够** | 框内 4,778 节点/38,383 边（度可算） |
| 现在就能算吗？ | **已实算** | 513 检出+Top10 双口径落产物（§2.5） |

## 摘要

「图谱异常评分」是智能化分析「模式识别·异常点」Tab 的核心列读数：每个异常模式的 0-99 分。UI 现状为前端框内子图实时计算（`kgIntelligence.js` detectPatternsAndAnomalies），检出为空时回填演示数据（isDemo=true 自披露）。数据侧判定：**完全转换支持**——久新真图采样框上 UI 算法 1:1 同构复刻：score=min(99, round((d/max(avg,1))×28))，threshold=max(avg×2.1, 4)=33.7398，实算 4,778 节点全评分、513 节点（10.74%）超阈值检出；z-score 交叉验证口径 Top1=30.09（度 832 的重尾枢纽），两口径满分集重合。dev 图表面 0 行、gkx 无节点级异常承载——度偏离评分唯一真源是久新图实算。

- 需求判定：seq 404 需求明列叶（「自动识别图谱中的异常点」），无公式，参数以 UI 算法为准。
- 复现状态：脚本已实算通过；513 检出+Top10 双口径落产物。
- 档位结论：**完全转换支持**（图结构+数据量均足+已实算）。
- 关键事实：UI 的「异常分」是线性映射非孤立森林等模型——同构复刻即真值口径，无需建模立项。
- 降档风险：无；升档路径：夜批落异常评分结果表 → 完全直接支持。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技知识图谱 → 分析展示 → 智能化分析 → 模式识别·异常点 Tab（`KgIntelligenceHub.jsx:111` 异常分列）。

### 1.2 为什么需要本指标

图谱中高度数枢纽（明星节点）与异常连接模式是数据质量与技术情报的双信号：自动识别异常点帮用户从 19,430 节点中定位结构异常（过度连接/孤立簇），是智能化分析的核心能力位。

### 1.3 需求文档是否给出定义方法

SRS seq 404（分析展示.md）原文「自动识别图谱中的异常点」——仅给能力语义，未给公式；异常评分读数与算法参数（倍率 28/阈值系数 2.1/封顶 99）以 UI 前端算法为准（kgIntelligence.js 读码）。

### 1.4 类似指标权威方法可行性分析概要

图异常检测谱系（Akoglu 2015 综述）：结构特征法（度偏离/z-score）、社区法（模块度残差）、关系法（OddBall）。UI 算法属最简结构特征法（度均值倍率线性映射）——与 NetworkX degree centrality 标准化同族；z-score 为其标准化变体。本件以 UI 同构为主口径、z-score 为交叉验证。

### 1.5 引用来源

1. Akoglu, L., Tong, H., Koutra, D. (2015). *Graph based anomaly detection and description: a survey*. Data Min. Knowl. Discov., 29(3), 626-688. https://link.springer.com/article/10.1007/s10618-014-0365-y
2. Chandola, V., Banerjee, A., Kumar, V. (2009). *Anomaly detection: A survey*. ACM Comput. Surv., 41(3). https://dl.acm.org/doi/10.1145/1541880.1541882
3. NetworkX developers. *Degree centrality*. https://networkx.org/documentation/stable/reference/algorithms/centrality.html

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意**：对图谱节点/模式给出可排序的异常程度分（0-99），支撑异常点 Tab 的列表排序与阈值告警。
- **操作化定义（UI 同构）**：S(v)=min(99, round((d_v/max(d̄,1))×28))；检出阈值 d_v≥max(d̄×2.1, 4)。
- **降档触发器**：若三源均无图结构（节点/边表空）→ 完全不支持（未触发：久新真图满承载）。
- **升档触发器**：久新夜批落异常评分结果表（score 列直查）→ 完全直接支持。

### 1.7 需求叶定位与相近叶关系

- 本叶：异常分（row_01=491）——模式识别·异常点 Tab 的量化读数。
- 相近叶：异常关系密度（027，LOW 证据边占比——边级密度代理）vs 本件（节点级度偏离评分）——节点/边两个粒度的异常族；异常数据监测（029，链路健康——运维侧非图结构侧）。

## 二、计算过程

### 2.1 装载与确定性采样框（B5）

复用族级共享缓存 `_s306_graph_base.py`：久新 `ads_technology_graph_node ORDER BY technology_node_id LIMIT 5000`（确定性前 5000 框）→ 诱导子图 4,778 连通节点/38,383 边（与 001/025-027 同框同基）。全图基数 19,430 节点/587,252 边（族级快照）。

### 2.2 UI 算法读码还原

`kgIntelligence.js:213-255` detectPatternsAndAnomalies（先期筛查读码记录）：

```js
threshold = max(avgDegree * 2.1, 4)              // 检出阈值
score = min(99, round((d / max(avg, 1)) * 28))   // 评分：度均值倍率线性映射，封顶 99
// 检出为空时 ensureDemoAnomalies() 回填演示数据，isDemo=true 自披露
```

### 2.3 全节点评分实算（主实测值）

present 集（度>0）= 4,778 节点（本框全连通）；μ=16.0666、σ=27.1148；阈值=33.7398。

| 实测项 | 值 | 产物键 |
|---|---|---|
| 评分节点数 | 4,778 | derived[0].nodes_scored |
| 框内平均度 μ | 16.0666 | derived[0].degree_avg |
| 框内度标准差 σ | 27.1148 | derived[0].degree_sd |
| UI 阈值（μ×2.1） | 33.7398 | derived[0].ui_threshold |
| **超阈值检出** | **513（10.74%）** | derived[0].detected_count |

### 2.4 Top10 双口径排行（UI 分主口径 / z-score 交叉验证）

按 UI 分 Top3：Microscopic Imaging and Tissue Analysis（度 73，分 99，z=2.10）、Computational image captioning systems（度 115，分 99，z=3.65）、Normalizing Flow Models for Probabilisti…（度 83，分 99，z=2.47）——满分 99 节点集=度≥57 集。

按 z-score Top3：Computational Methods for Biological Seq…（度 832，z=30.09）、Hardware Architectures for Machine Learn…（度 481，z=17.15）、Deep Learning Architectures for Object D…（度 402，z=14.23）。两口径满分集重合（线性映射 vs 标准化映射仅排序差异）。完整双 Top10 落 derived[0].top10_by_ui_score / top10_by_zscore。

### 2.5 稳健性与口径敏感性

- 度分布重尾（σ=27.11 远大于 μ=16.07）：线性映射在度≥57 即封顶——头部区分靠 z-score；两口径头部集重合故检出结论稳健。
- 10.74% 检出率落在幂律网络枢纽占比经验带（<15%）。

### 2.6 需求符合性预评（UI 演示形态 vs 实算形态衔接）

UI 列（pattern/nodes/score/type）中 score 列与本件 S(v) 字段级对应；真图检出非空（513）不触发 isDemo 回填——演示层与实算层自然衔接。

### 2.7 复现代码结果展示

`python3 code/M_SCIUI_KGANALY_028.py` → `M_SCIUI_KGANALY_028_out.json`（facts/derived/absence_probe/基期三键全落）。

### 2.8 分步证据对照表

| 步骤 | 产物键 | 值 |
|---|---|---|
| 全图节点/边 | facts.jiuxin_tech_nodes_total / edges_total | 19,430 / 587,252 |
| 采样框 | facts.jiuxin_tech_sample_nodes / induced_edges | 5,000（连通 4,778）/ 38,383 |
| 评分节点 | derived[0].nodes_scored | 4,778 |
| μ/σ | derived[0].degree_avg / degree_sd | 16.0666 / 27.1148 |
| 阈值/检出 | derived[0].ui_threshold / detected_count | 33.7398 / 513 |
| Top1（UI 分） | derived[0].top10_by_ui_score[0] | 分 99（度 73） |
| Top1（z） | derived[0].top10_by_zscore[0] | z=30.09（度 832） |

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 图节点结构 | 久新 `ads_technology_graph_node` | 足（19,430） |
| 图边结构 | 久新 `ads_technology_graph_edge` | 足（587,252） |
| 度统计算子 | 本件 py（degree_map） | 已实算 |
| 现成异常结果面 | 三源 | 无（absence_probe） |

### 3.2 现场复核清单

久新框实算复核：4,778 present=框全连通；Top1 度 832 与 026 件度趋势 Top1 同节点同值（族内互证）。

## 四、数据缺失情况

### 4.1 现成结果面缺失（唯一结构缺口，非判定性）

三源无异常评分结果表——需本件式实算；非判定性（结构+数据量足）。

### 4.2 口径级待裁项

非线性异常模型（isolation forest/社区残差）未用——UI 即线性映射，同构优先；建模扩展留立项。

### 4.3 修复建议与影响面

夜批落 `graph_node_anomaly_score` 结果表（node_id/score/z/检测时间）→ 异常点 Tab 直查（升档完全直接支持）；影响面仅夜批管线，UI 无需改。

## 参考文献

1. Akoglu, L., Tong, H., Koutra, D. (2015). *Graph based anomaly detection and description: a survey*. Data Mining and Knowledge Discovery, 29(3), 626-688. https://link.springer.com/article/10.1007/s10618-014-0365-y
2. Chandola, V., Banerjee, A., Kumar, V. (2009). *Anomaly detection: A survey*. ACM Computing Surveys, 41(3), 1-58. https://dl.acm.org/doi/10.1145/1541880.1541882
3. NetworkX developers. *Degree centrality — networkx documentation*. https://networkx.org/documentation/stable/reference/algorithms/centrality.html

# 附件

## 附录 A 原始需求原文摘录

- SRS seq 404（分析展示.md）：「自动识别图谱中的异常点」。
- SRS row_01=491：实体与连接的规模/结构统计。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_KGANALY_028_out.json`）

facts（ui_mount/ui_algo/ui_demo_fallback/srs_anchor/cat/jiuxin_tech_*）；derived[0]（nodes_scored/degree_avg/degree_sd/ui_threshold/detected_count/top10_by_ui_score/top10_by_zscore）；absence_probe（4 件）；support_judgment；base_years_used/missing/note。

## 附录 C 可行性报告完整版（要点）

方法谱系：结构特征法（度偏离/z-score——本件主口径）> 社区法（模块度残差）> 关系法（OddBall）——UI 线性映射属结构特征法最简式，同构复刻零建模成本。数据矩阵：久新 node/edge 满承载；dev/gkx 零承载（absence_probe）。结论：完全转换支持。
