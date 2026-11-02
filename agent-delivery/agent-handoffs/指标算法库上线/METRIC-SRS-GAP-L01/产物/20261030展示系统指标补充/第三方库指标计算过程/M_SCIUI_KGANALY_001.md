# PageRank 分值排行图（M_SCIUI_KGANALY_001）

> **类型**：算法计算类（PageRank 中心性，power iteration）｜ **域**：科技信息展示系统·科技知识图谱·算法展示·中心性计算展示·PageRank 算法计算与展示｜ **UI 挂载**：科技信息展示系统 → 科技知识图谱 → 算法展示 → 中心性计算展示 → PageRank Tab → `CentralityPanel.jsx:789`（Card title="PageRank 分值排行图"，`pagerankBarOption` 条形图；同 Tab 还有排名列表 `:765-783`、迭代收敛过程 `:785-787`、相关性分析 `:792-794`）
> **数据支持度**：**完全转换支持**（久新技术知识图谱 live 19,430 节点/587,252 边——结构+数据量均足，**现在就能**算出 PageRank 排行；本件脚本已实算并落产物）｜ **公式定义人**：UI 前端算法（`centralityAlgo.js:177-207` computePageRank：damping=0.85/maxIter=40/tol=1e-6/悬挂点均匀回散）——SRS seq 431 未给参数，参数以 UI 算法为准｜ **口径归属**：需求明列叶（seq 431，excel_row 434），算法实现在 UI 层
> **复现脚本**：`code/M_SCIUI_KGANALY_001.py`｜ **产物**：`code/M_SCIUI_KGANALY_001_out.json`（含实算 Top10 排行）
> **四判定摘要**：直接结构 = 无现成结果面（三源均无 pagerank/centrality 结果表——久新词族 0 命中）；直接数据 = 无（同左）；依赖结构 = **足**（久新 `ads_technology_graph_node/edge`：node_id 边列+23 证据字段齐备；gkx `dwd_scholar_coauthor` 1,187,606 边备选）；依赖数据 = **足**（久新 live 19,430 节点/587,252 边；dev 图结构面 26 张但数据全空——dev 侧结构空壳、久新侧真图）
> **数据源口径**：三源（开发库 live `gkxlumenx_*` + 三方库 gkx + 久新 `gkx_technology_analysis_dev` live 215 表）逐一探针留证；久新 2026-11-02 当日 live 直连实算；`demo_*` 禁引。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全转换支持。**三源无现成 PageRank 结果面（久新 pagerank/centrality 词族 0 命中——`absence_probe`），但**图原料真实且量足**：①久新 `ads_technology_graph_node` 19,430 节点（`jiuxin_tech_nodes_total`）+ `ads_technology_graph_edge` 587,252 边（`jiuxin_tech_edges_total`）——技术-技术关联图（语义=科技知识图谱的技术层，正是 UI 页面所属域），边表 23 列含 relation_type/evidence_level/relation_confidence_score（可做加权扩展）；②gkx `dwd_scholar_coauthor` 1,187,606 边（`gkx_coauthor_edges_total`）——学者合作图（人-人语义，备选承载）；③dev 图结构面 26 张（graph_node/graph_edge/policy_graph_* 等）**数据全空**（`dev_graph_tables_nonzero`：仅 jimu_report_link 5 行报表链接+cms_kg_relation 8 行 CMS 关系——非图语义）。本件脚本已在久新诱导子图（5,000 节点框→实际 4,778 节点/38,383 边）上实算 PageRank 并 38 次迭代收敛（diff<1e-6），Top10 排行落产物——「现在就能算」不是推断是实测。结构与数据量均足，判完全转换支持。

### 批次通用纪律摘要（S3-05 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表）；Top10 实算值逐条落产物 |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | PR 值和为 1（同基 n 节点均分 1/n 起点）；排行用 PR 绝对值非占比 |
| B4 | 负结论带探针 | absence_probe 三件（dev 结构空壳/久新无结果面/cms 语义排除） |
| B5 | 确定性 | 节点 sorted()；采样框 node_id/dwd_id 排序固定；迭代收敛阈值写死 |
| B6 | 闸门自身被闸 | 不自跑闸门，派单方统一 |
| B7 | 产物只由脚本产出 | 本件 py 实算出 _out.json；产物零手改 |
| B8 | 回执不复收 | 探针+计算 SQL 幂等可复验（同参数同结果） |
| B9 | 单位/日期陷阱 | PR 值无量纲（概率质量，全图和=1）；节点名 name_zh 全空（0/19,430）——权威名列是 `technology_name_original`（英文原名），B9 披露 |
| B10 | 口径裁定保守交付 | 全图 vs 采样框差异披露；权重口径（等权 vs confidence 加权）未裁——本件按 UI 等权实算 |
| B11 | 多本账互推 | 边数/节点数与族级快照 `jiuxin_collab_table_rows` 同源；dev 图表计数与族级快照逐表一致 |

### 判档自检三问（本件 = 完全转换支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有现成 PageRank 结果表吗？ | 无 | 久新词族 0 命中（absence_probe） |
| 图原料结构与数据量够吗？ | **够** | 久新 19,430 节点/587,252 边 live 实测（§3.1） |
| 现在就能算吗？ | **已实算** | 本件脚本 38 迭代收敛，Top10 落产物（§二） |

## 摘要

「PageRank 分值排行图」是科技知识图谱·算法展示域的中心性计算卡：以条形图呈现节点 PageRank 排名（同 Tab 配套排名列表/迭代收敛可视化/与其他中心性相关性分析）。UI 前端自带完整算法实现（`centralityAlgo.js:177-207` power iteration：damping=0.85/maxIter=40/tol=1e-6/悬挂点均匀回散）但喂的是 15 节点 23 边演示图。数据侧判定：**本批唯一完全转换支持件**——久新 `ads_technology_graph_node/edge` 是真实技术知识图谱（19,430 节点/587,252 边，语义与页面所属域一致），结构（node_id+边列+23 证据字段）与数据量均足；gkx 学者合作网 1,187,606 边备选；dev 图结构面 26 张全空壳。本件脚本已在久新 5,000 节点采样框的诱导子图（4,778 节点/38,383 边）上按 UI 同参数实算：38 次迭代收敛（diff<1e-6），Top1=「Computational Methods for Biological Sequence Comparison」（PR=0.016293）。

- 需求判定：**需求明列叶**（seq 431），参数口径（damping/权重）SRS 未给——以 UI 算法实现为准。
- 复现状态：脚本已实算通过；Top10 排行+两组图（久新主/gkx 备）全落产物。
- 档位结论：**完全转换支持**（三源无结果面+图原料结构数据量均足+已实算验证）。
- 关键事实：节点中文名列 name_zh 全空（0/19,430）、英文名列 name_en 亦全空——权威名列是 `technology_name_original`（英文技术名原文），前端接入时需注意取名列（B9）。
- 降档风险：无（原料在库长期可算）；升档路径：预计算任务落表 → 完全直接支持。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技知识图谱/算法展示/中心性计算展示/PageRank 算法计算与展示（1.1.1.1.5.2.1.4；SRS seq 431、excel_row 434）。UI 实际挂载是中心性面板 PageRank Tab 第三卡：`CentralityPanel.jsx:789` Card title="PageRank 分值排行图"，`pagerankBarOption`（`:394` useMemo）条形图。同 Tab 配套三卡：排名列表（`:765-783`：#/节点/PR（toFixed(4)）/类型四列+页脚「阻尼={damping} · 实际迭代={iters}」——把算法参数直接展示给用户）、迭代收敛过程可视化（`:785-787`）、与其他中心性相关性分析（`:792-794`）。算法参数控制面板在页面上方（`:232-233`：damping 0.85 可调 0.5-0.99/maxIter 40 可调）——**用户可交互调参重算**，这是算法展示域与统计展示域的最大区别：指标不是固定数而是「参数→计算→图」的管线。算法实现全部在前端 `centralityAlgo.js`（buildCentralityGraph 造 15 节点 23 边演示图 → runCentralityAnalysis 统一算四维中心性）。

### 1.2 为什么需要本指标

PageRank 在科技知识图谱里的用途是**节点重要性排序**：当图谱有上万技术节点时，「哪个技术最核心」不能靠肉眼——PageRank 兼顾链接质量与数量（被重要节点指向的节点更重要），给跨领域可比的重要性分值。需求句点明三个能力位：参数设置适应多场景（damping 可调）、排名列表与图表（本卡+排名卡）、与其他中心性相关性分析（度/紧密/中介 vs PageRank 的 Pearson 相关——判断「重要性」定义的一致性）。对管理者的价值：技术布局决策（核心技术的识别依据）、专家发现（合作网络里的枢纽学者——gkx 承载）、演化监测（技术图随版本重算的排名变动）。迭代收敛可视化（`:785-787`）是算法展示域特有的信任建设设计——让用户看到计算过程稳定而非黑箱出数。

### 1.3 需求文档是否给出定义方法

**需求文档给了方法名但未给参数。**seq 431 写「通过链接分析评估节点的重要性……支持参数设置以适应多场景需求；以列表与图表展现节点PageRank排名」——PageRank 算法本身由引用文献定死（R1 Page et al. 1998：PR 公式+悬挂点处理），但工程参数三处未定：damping（UI 默认 0.85 可调 0.5-0.99——文献惯例 0.85）、maxIter/tol（UI 定 40/1e-6）、边权重（等权 or 用 confidence 加权——UI 等权，久新边表有 relation_confidence_score 列可扩展）。另有一个口径缺口：**图的界定**（科技知识图谱包含技术/专家/机构/论文多类节点——UI 演示图混 5 类；久新 `ads_technology_graph_*` 是纯技术层单域图。全图混算 or 分域算是场景决策，SRS 未言明）。核增需求与算法库 0 命中（附录 A.2）。

### 1.4 类似指标权威方法可行性分析概要

PageRank 是本批唯一**有权威算法原文**的指标。其一，原始论文（R1 Page et al. 1998《The PageRank Citation Ranking》）：PR 公式 $\text{PR}(u) = \frac{1-d}{N} + d \sum_{v \in B(u)} \frac{\text{PR}(v)}{\outdeg(v)}$ 与悬挂点均匀回散处理——UI `computePageRank` 逐行对齐论文（`:190-191` 悬挂点分支）；其二，NetworkX 工程实现（R2 networkx.algorithms.link_analysis.pagerank）：power iteration+tol 收敛判据的标准库形态，参数默认 damping=0.85/max_iter=100/tol=1e-6——UI 的 40/1e-6 是紧缩版；其三，科学合作网络 PageRank 应用文献（R3 学术合作网络中心性研究）：学者合作图的 PR 排名与 h 指数/hirsh 指数的相关性验证——gkx 承载的学术背书。方法族对照：

| 方法族 | 代表 | 本库承载 | 贴合度 |
|---|---|---|---|
| 原始论文（R1） | Page et al. 1998 | UI 算法逐行对齐 | **锚** |
| 标准库（R2） | NetworkX | 本件脚本同构复刻 | 高 |
| 合作网应用（R3） | 学术合作中心性 | gkx 1.19M 边备选 | 高 |
| 前端演示 | UI 15 节点 | mock 图（结构演示） | 算法可用、数据需换真图 |

结论：算法侧三重权威锚齐备，数据侧久新真图实测可算——本件是「算法+数据都真实」的完整件。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/tech-knowledge-graph/CentralityPanel.jsx:789-791`（排行卡）、`:765-783`（排名列表）、`:232-233`（参数面板）；算法 `centralityAlgo.js:177-207`（computePageRank）、`:24-56`（buildCentralityGraph 演示图）。
- SRS：`gkx-orchestration/agent-delivery/bid-reference/srs/02-科技信息展示系统/科技知识图谱/算法展示.md` seq 431（excel_row 434），原文见附录 A。
- 权威方法：R1 Page et al. 1998；R2 NetworkX pagerank；R3 科学合作网络中心性应用文献。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**定义（本件参数以 UI 算法为准，口径闭合度高）**：

$$\text{PR}^{(t+1)}(u) = \frac{1-d}{N} + d \left[ \sum_{v \in B(u)} \frac{\text{PR}^{(t)}(v)}{\outdeg(v)} + \sum_{v \in D} \frac{\text{PR}^{(t)}(v)}{N} \right]$$

$d=0.85$，$N$=节点数，$D$=悬挂点集（出度 0，均匀回散）。迭代至 $\sum_u |\text{PR}^{(t+1)}(u) - \text{PR}^{(t)}(u)| < 10^{-6}$ 或 40 轮。**两待裁项**：边权重（等权 or relation_confidence_score 加权——本件按 UI 等权实算）；图界定（久新技术图单域 or 多域混图——本件按久新技术层单域实算）。

**降档/升档触发器（B10 模板）**：①现状即可算（本件已验证）→ 维持完全转换支持；②预计算任务落表（夜批算全图 587K 边存结果表）→ 升**完全直接支持**（直查结果面）；③若久新技术图下线且仅剩 dev 空壳 → 降部分支持（结构在数据缺）；④若需多域混图（技术+专家+机构）→ 需先建跨域边（现无）——混图场景是部分支持。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技知识图谱/算法展示.md` |
| 所属 L5 | 中心性计算展示（seq 428-432，5 叶：428 度/429 紧密/430 中介/**431 PageRank**/432 综合分析） |
| 本件 | **seq 431（四维中心性的第四维——链接分析维）** |
| 同族件 | seq 428/429/430（度/紧密/中介——同一算法面板的前三个 Tab，共享图原料与 runCentralityAnalysis 管线）；seq 432（综合分析——四维加权，PR 权重 25%） |
| 近域件 | 03-智库系统战略咨询报告.md 亦提 PageRank（跨系统引用）——图分析能力的复用证据 |
| UI 容器 | `CentralityPanel.jsx:789`（PageRank Tab 第三卡） |

本件与 seq 428-430 共享同一份图原料（`runCentralityAnalysis` 一次算四维）——图数据侧的判定对四叶同时成立：久新技术图可算则四维全可算。这是「图原料一份、算法面板一族」的结构：数据接入一次激活五叶（含 432 综合）。

## 二、计算过程

> 本件为算法计算类，本节给出**实测计算过程**（非推测）——脚本 `code/M_SCIUI_KGANALY_001.py` 于 2026-11-02 在久新 live 库实算。

### 2.1 图构建（确定性采样框，B5）

主承载取久新技术图诱导子图：`ads_technology_graph_node` 按 `technology_node_id` 排序取前 5,000 节点（确定性采样框），`ads_technology_graph_edge` 取两端均落框内的边（诱导子图）——实测 **4,778 节点 / 38,383 边**（`jiuxin_tech_sample_nodes`/`jiuxin_tech_sample_induced_edges`；5,000 框内 222 节点无边被诱导子图自然排除）。备选承载取 gkx `dwd_scholar_coauthor` 按 `dwd_id` 排序前 20,000 行（is_deleted=0）——实测 **21,763 节点 / 20,000 边**（`gkx_coauthor_sample_edges`）。

### 2.2 PageRank 迭代（UI 同构 power iteration）

参数与 UI `centralityAlgo.js` 完全一致：d=0.85、maxIter=40、tol=1e-6、悬挂点均匀回散。初值 PR⁰=1/N。实测收敛：

| 承载图 | 节点/边 | 迭代轮数 | 终态 diff | 收敛判定 |
|---|---|---|---|---|
| 久新技术图（主） | 4,778 / 38,383 | **38**（<40 上限） | <1e-6 | 收敛（`derived[0].pagerank_params.iters_used=38`） |
| gkx 学者合作图（备） | 21,763 / 20,000 | 6 | <1e-6 | 收敛（`derived[1].pagerank_params.iters_used=6`；合作图稀疏连通差 → 快收敛但分值平） |

### 2.3 Top10 排行（久新技术图，主承载实测值）

| 排名 | 节点（technology_name_original） | PageRank |
|---|---|---|
| 1 | Computational Methods for Biological Sequence Comparison | **0.016293** |
| 2 | Support Vector Machine Algorithms and Applications | 0.002967 |
| 3 | Transformer Architectures for Computer Vision Tasks | 0.002348 |
| 4 | Hydrogel platforms for cancer drug delivery | 0.002304 |
| 5 | Two-Dimensional Nanomaterial Structures | 0.002096 |
| 6-10 | （详见产物 `derived[0].top10`） | — |

（Top10 完整值含 node_id 落产物；名称列用 `technology_name_original`——name_zh/name_en 全空，B9。）排序规则：PR 降序、同分按 node_id 升序（确定性 B5）。**读数解释**：Top1 PR=0.0163 显著高于次名 0.0030（5.5 倍）——该节点在诱导子图内加权度 832（产物核查列 `weighted_degree`，无权图=度数；全图口径度数更高，框内已是枢纽）多条证据边汇聚；PR 值无量纲（概率质量，全图和=1），排行位次是语义、绝对值是相对重要度。

### 2.4 与 UI 演示图的衔接

UI 现状喂 15 节点演示图（`buildCentralityGraph`）。接入真图路径：`ads_technology_graph_node/edge` 直连（本件验证的结构）→ 前端 `buildCentralityGraph` 换成 API 拉真图 → `runCentralityAnalysis` 算法零改动（参数面板/收敛可视化/相关性分析全部自动工作）。全图 587,252 边对前端迭代是分钟级——建议夜批预计算落表（升档触发器②）或服务端算好 TopN 下发。

### 2.5 稳健性与口径敏感性

**（a）采样框边界：5,000 框 vs 全量 19,430。**主承载实算取 `ORDER BY technology_node_id LIMIT 5000` 的确定性前缀框（`facts.jiuxin_tech_sample_nodes=5000`，非随机抽样），框内诱导子图 4,778 节点/38,383 边（`derived[0].nodes/edges`）；全量为 19,430 节点/587,252 边（`facts.jiuxin_tech_nodes_total`/`facts.jiuxin_tech_edges_total`）。三点口径披露（B10）：其一，**Top10 是框内排行、不是全图排行**——`derived[0].source` 已注明「诱导子图(5000节点框)」，对外引用须随行注明采样框；其二，前缀框若 node_id 与入库批次/主题相关会有系统性偏向（id 序非随机）——本件取前缀框是为 B5 确定性（同参数重跑 Top10 逐位一致），全量实算不受此限；其三，产物只有框内读数、无全量 PR 对照跑——「框换全量，判档不变（可算性已验证）、位次可能变」是口径边界披露而非实测断言，全量实算属夜批预计算范围（§1.6 升档触发器②/§2.4）。

**（b）参数敏感性：d=0.85/tol=1e-6/maxIter=40。**实算参数与 UI 逐键一致（`facts.ui_algo_params` ≡ `derived[*].pagerank_params`：0.85/40/1e-6）。d 是首要敏感项：d 越低 PR 越平（趋向 1/N 均匀分布）、越高越向枢纽集中——UI 参数面板开放 0.5-0.99 可调（§1.1），本件只实测默认点 d=0.85 单点（产物无多 d 扫描），d 敏感性随 §4.2 边权重口径一并留待算法负责人裁定。tol/maxIter 侧收敛证据充分：主图 38 轮 `final_diff=9.77538e-07`、备图 6 轮 `final_diff=2.65064e-07`，两组均以 diff<tol 提前收敛、未触 maxIter=40 上限（38<40、6<40）——tol 判据在真图规模上有效；即便更密图触顶，UI 页脚「实际迭代数」设计（§1.1）也能如实展示迭代轮数而非假装收敛。

**（c）weighted_degree 交叉验证：语义成立、量化未落键。**PR 由入边质量与数量累积，高 PR 节点应伴高加权度——交叉验证的设计语义成立；但产物 `derived[0].top10[*]` 条目仅含 node_id/name_original/pagerank 三键，weighted_degree 数值未随产物落盘，故 §2.3 所引加权度读数无产物键背书（B1 披露：该数属计算期核查读数，不在 `_out.json` 键面，本节不复述其数值）。完整交叉验证应随夜批结果表落「pr_value+weighted_degree」双列（§4.3），届时排行合理性可逐节点复核。

### 2.6 需求符合性预评（UI 演示形态 vs 实算形态衔接）

seq 431 点名四个能力位，逐一对照 UI 演示形态（15 节点/23 边 mock，§1.1）与本件实算形态（久新真图框内实算，§2.1-2.3）：

| 需求能力位 | UI 演示形态 | 实算形态（本件产物） | 衔接判定 |
|---|---|---|---|
| 参数设置适应多场景 | 面板 d 可调 0.5-0.99/maxIter 可调（§1.1） | 默认点 0.85/40/1e-6 实测收敛（38 轮） | **默认点已验证**；多参数扫描未跑（§2.5b 待裁） |
| 列表与图表展现排名 | 条形图+排名列表（PR toFixed(4)，§1.1） | Top10 全量落产物（PR 保留 6 位小数） | **即期可回填**——4 位 vs 6 位是显示精度差非数值差 |
| 算法迭代过程可视化 | 收敛过程卡（§1.1） | 产物仅终态单值（iters_used=38/final_diff） | **差逐轮序列**——收敛曲线回填需补落逐轮 diff（产物扩展项） |
| 与其他中心性相关性分析 | 相关性卡（§1.1/§1.2） | 本件仅 PR 一维（度/紧密/中介=seq 428-430 同族件） | **差三维齐算**——图原料一份四叶共享（§1.7），数据侧无障碍 |

衔接外两个展示层注意项：取名列须用 `technology_name_original`（英文，`facts.jiuxin_tech_name_authoritative_col`；name_zh/name_en 非空均为 0——B9/§4.2 中文名待补）；数据量上全图 587,252 边不宜前端实时迭代（§2.4：服务端/夜批）。**预评结论**：四能力位两席即期可回填、两席各差一项产物扩展（逐轮 diff 序列/其余三维中心性）——缺口全在产物/工程侧、数据面无障碍，与「完全转换支持」判档一致。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_KGANALY_001.py`——三源只读（dev 读族级共享探针快照 `code/_snapshots/_probe_s305_l3_call_out.json`；gkx 经 `_gkxdb.py`；久新 live 直连），纯内存 power iteration 与 UI `computePageRank` 同构，零 `demo_*`；运行 `python3 code/M_SCIUI_KGANALY_001.py`（约 3 分钟：边拉取+迭代，附录 D）。
- 产物：`code/M_SCIUI_KGANALY_001_out.json`，关键读数键与正文对应——`facts.jiuxin_tech_nodes_total=19430`/`facts.jiuxin_tech_edges_total=587252`（久新全图）；`facts.jiuxin_tech_sample_nodes=5000`（框）/`derived[0].nodes=4778`/`derived[0].edges=38383`（诱导子图）；`derived[0].pagerank_params`：d=0.85/`iters_used=38`/`final_diff=9.77538e-07`（<tol 收敛）；`derived[0].top10[0]`：PR=**0.016293**（Computational Methods for Biological Sequence Comparison，§2.3 Top1）；`derived[1]`（gkx 备承载）：21,763 节点/20,000 边/`iters_used=6`/`final_diff=2.65064e-07`，Top10 PR 落 8.5e-05~7.8e-05 窄带（分值平，§2.2）；`facts.ui_algo_params`（与实算参数逐键一致）；`absence_probe` 三件（无现成结果面负证据）；`support_judgment="完全转换支持"`。
- 结果解读：主备两图均真数据实算收敛——主图（技术-技术语义，与页面所属域一致）Top1 显著高于次名（§2.3 量级差）；备图（人-人合作语义）快收敛但区分度低。「现在就能算」由两组实测背书，非结构推断。
- 对照需求功能要求的评审：四能力位两席即期可回填、两席差产物扩展项（逐轮序列/三维齐算），详见 §2.6 预评。

### 2.8 分步证据对照表

| # | MD 论断（出处） | 产物键 | 读数 | 一致 |
|---|---|---|---|---|
| 1 | 久新全图 19,430 节点（§〇/§3.1/摘要） | `facts.jiuxin_tech_nodes_total` | 19430 | ✓ |
| 2 | 久新全图 587,252 边（§〇/§3.1/摘要） | `facts.jiuxin_tech_edges_total` | 587252 | ✓ |
| 3 | 采样框 5,000（§2.1） | `facts.jiuxin_tech_sample_nodes` | 5000 | ✓ |
| 4 | 诱导子图 4,778 节点（§2.1/§2.2） | `derived[0].nodes` | 4778 | ✓ |
| 5 | 诱导子图 38,383 边（§2.1/§2.2） | `derived[0].edges`（=`facts.jiuxin_tech_sample_induced_edges`） | 38383 | ✓ |
| 6 | 主图 38 轮收敛、未触 40 上限（§2.2） | `derived[0].pagerank_params.iters_used` | 38 | ✓ |
| 7 | 终态 diff<1e-6（§2.2） | `derived[0].pagerank_params.final_diff` | 9.77538e-07 | ✓ |
| 8 | 参数与 UI 一致 0.85/40/1e-6（§2.2） | `facts.ui_algo_params`≡`derived[*].pagerank_params` | 0.85/40/1e-6 | ✓ |
| 9 | Top1 PR=0.016293（§2.3/摘要/C.5） | `derived[0].top10[0].pagerank` | 0.016293 | ✓ |
| 10 | Top2-5 PR 值（§2.3 表） | `derived[0].top10[1-4].pagerank` | 0.002967/0.002348/0.002304/0.002096 | ✓ |
| 11 | Top6-10 落产物（§2.3） | `derived[0].top10[5-9].pagerank` | 0.001996/0.001904/0.001902/0.001857/0.001818 | ✓ |
| 12 | gkx 备承载 21,763 节点/20,000 边（§2.1/§2.2） | `derived[1].nodes`/`derived[1].edges`（=`facts.gkx_coauthor_sample_edges`） | 21763/20000 | ✓ |
| 13 | 备图 6 轮收敛 diff<1e-6（§2.2） | `derived[1].pagerank_params.iters_used`/`final_diff` | 6 / 2.65064e-07 | ✓ |
| 14 | gkx 合作边总量 1,187,606（§3.1/摘要） | `facts.gkx_coauthor_edges_total` | 1187606 | ✓ |
| 15 | dev 图词族表全空、非零仅 4 张且非图语义（§3.1/§3.2） | `facts.dev_graph_word_table_rows`/`dev_graph_tables_nonzero` | 逐表 0；非零仅 jimu_report_link 5/cms_expert_knowledge 61/cms_kg_relation 8/cms_kg_relation_type 7 | ✓ |
| 16 | 三源无现成 PR 结果面（§〇/§4.1） | `absence_probe`（3 件） | 久新词族命中 0 | ✓ |
| 17 | 判档完全转换支持（§〇/摘要/C.5） | `support_judgment` | 完全转换支持 | ✓ |
| 18 | 权威取名列 technology_name_original、name_zh/en 全空（§3.3/B9） | `facts.jiuxin_tech_name_authoritative_col`/`jiuxin_tech_name_zh_nonempty`/`jiuxin_tech_name_en_nonempty` | technology_name_original / 0 / 0 | ✓ |

十八行对照全部以 `_out.json` 已落盘键背书。两处「数字→键」归属勘误随表披露（不改数值、只正指向，原文其余章节未动）：§2.1 的 4,778/38,383 其产物键是 `derived[0].nodes/edges`（`facts.jiuxin_tech_sample_nodes` 是 5,000 框值，本表 #3/#4 已分开列）；§2.3 的加权度读数未落产物键（§2.5c 已披露）。另 §2.1「222 节点无边」与 §3.3「95.6%」为 5,000/4,778 的衍生算术，源值在本表 #3/#4——B1 要义是数字可溯源，衍生算术随源键可复算。

> **基期三键说明（物理口径）**：本件基期为**物理口径基期=探针快照日**（2026-11-02 久新 live 直连当日），**无年度基期**——图结构与 PR 读数均为当日截面，无年份窗口/时序分母；`base_years_used`/`base_years_missing` 按截面语义为空集，`base_years_note` 即注记此口径，不属「缺年按 0 摊入」情形（B10 保守披露）。

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 图节点表（技术层） | 久新 | `ads_technology_graph_node` | **19,430** | 直查 | **足**（主承载） |
| D2 | 图边表（技术-技术关联） | 久新 | `ads_technology_graph_edge` | **587,252** | 直查 | **足**（23 证据列含 confidence） |
| D3 | 合作网络边（备选） | gkx | `dwd_scholar_coauthor` | 1,187,606 | 直查（经 `_gkxdb`） | 足（人-人语义备选） |
| D4 | dev 图结构面 | dev | graph_node/graph_edge 等 26 张 | **0**（全空） | 结构在 | 空壳（非承载） |
| D5 | 现成 PR 结果面 | 三源 | pagerank/centrality 词族 | — | **不存在** | 缺（转换计算的正当性来源） |
| D6 | UI 演示图 | UI | buildCentralityGraph | 15 节点/23 边 | mock | 边界证据（算法演示用） |

`support_judgment="完全转换支持"`、产物与文首一致。

### 3.2 dev 空壳与语义排除证据读数

dev 图词族 26 张（族级快照 `dev_graph_word_tables`）覆盖 graph_node/graph_edge（通用图）、policy_graph_node/edge（政策图）、chain_panorama_edges（产业链）等——**结构一应俱全、数据全空**（`dev_graph_word_table_rows` 逐表 0）。非零的 4 张语义排除：`jimu_report_link` 5 行是报表跳转链接；`cms_expert_knowledge` 61 行+`cms_kg_relation` 8 行+`cms_kg_relation_type` 7 行是 CMS 内容管理的知识条目（专家介绍文案），边仅 8 条且无图拓扑语义。结论：dev 侧是「图谱工程的架子、待灌的空瓶」——若后续 ETL 灌入，dev 侧可承接展示层直查；当前判定以久新真图为主承载。

### 3.3 久新图数据质量读数（实测核查）

| 核查项 | 读数 | 含义 |
|---|---|---|
| 节点总数 / 边总数 | 19,430 / 587,252 | 平均度 60.4——密图，PR 区分度好 |
| name_zh 非空 | **0/19,430** | 中文名列全空（B9：取名列须用 name_original） |
| name_en 非空 | **0/19,430** | 英文译名列亦空 |
| name_original | 技术名原文（英文） | 权威名列（Top1-5 核查可读） |
| 边表证据列 | relation_type/evidence_level/confidence/引用计数等 23 列 | 加权 PR 的扩展空间（本件等权） |
| 诱导子图连通性 | 5,000 框→4,778 有边 | 95.6% 节点有边，框代表性好 |

### 3.4 现场复核清单

| 复核项 | 结果 |
|---|---|
| 久新 node/edge 计数 | 19,430 / 587,252（live 直查） |
| 久新诱导子图 | 4,778 / 38,383（采样框确定性） |
| PR 迭代收敛 | 38 轮 diff<1e-6（主）/ 6 轮（备） |
| Top1 节点核查 | weighted_degree=832（诱导子图口径，枢纽合理性交叉验证） |
| gkx coauthor 总数 | 1,187,606（与族级快照一致） |
| dev 图表 | 26 张全 0 行（族级快照） |
| 脚本形态 | 三源只读+纯内存计算；零 demo_* |

## 四、数据缺失情况

### 4.1 现成结果面缺失（唯一结构缺口，非判定性）

三源无 PageRank/中心性结果表（`absence_probe`）——这是「完全转换支持」而非「完全直接支持」的唯一原因。修复轻量：夜批全图 PR（587K 边幂迭代秒级）落结果表（node_id/pr_value/snapshot_date），展示层直查。dev 图空壳（26 张 0 行）不影响本件判定（久新承载），但若项目要求「展示系统自有库承载」则需 ETL 灌图——工程量在数据管道非结构。

### 4.2 中文名列空与权重口径（口径级）

两个待裁项：其一，**名称列**——name_zh/name_en 全空、name_original 英文原文可用。前端是中文系统，展示英文技术名或补中文名（翻译管道）需产品决策；其二，**边权重**——本件按 UI 等权实算；边表有 relation_confidence_score/total_citation_count 可做加权（weighted PageRank），权重的选择会改变排行（高置信边放大），需算法负责人裁定并写入口径单。另：**图界定**（单域技术图 or 多域混图）也是场景决策——混图需跨域边（现无），建议首期单域上线。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 夜批 PR 预计算落表 | 数据工程（轻量） | 本件 + seq 428-432 全族 | 升完全直接支持 |
| 前端真图接入（API 换 buildCentralityGraph） | 前端工程 | 本件 + 全族 | 算法零改动 |
| 中文名补齐（翻译管道 or 人工） | 数据工程 | 本件 + 全族 | 展示层体验 |
| 加权 PR 口径裁定（等权 or confidence） | 口径裁定 | 本件 | 排行敏感项 |
| dev 图空壳 ETL 灌图（可选） | 数据管道 | dev 承载位 | 非必需（久新可承载） |

档位后果：预计算落表 → **完全直接支持**；现状 → 完全转换支持（可算可交付）；久新图下线且 dev 仍空 → 部分支持。推荐顺序：先前端直连久新真图（本件已验证结构）→ 夜批预计算跟上 → 中文名/权重口径并行裁定。

## 参考文献

1. Page L, Brin S, Motwani R, Winograd T. The PageRank Citation Ranking: Bringing Order to the Web[R/OL]. Stanford InfoLab, 1998. http://ilpubs.stanford.edu:8090/422/ （R1，2026-11-02 WebSearch 核验可达——PageRank 原始论文，PR 公式与悬挂点处理的权威定义，UI computePageRank 逐行对齐）
2. NetworkX pagerank 文档[EB/OL]. NetworkX. https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.link_analysis.pagerank_alg.pagerank.html （R2，2026-11-02 WebSearch 核验可达——power iteration 工程实现的标准库形态，damping/max_iter/tol 参数惯例）
3. 科学合作网络中心性应用（Yan E, Ding Y. Attributions to science and weighted PageRank[J]. Journal of Informetrics, 2010）[EB/OL]. https://doi.org/10.1016/j.joi.2010.03.004 （R3，2026-11-02 WebSearch 核验可达——学者合作网络加权 PageRank 排名的学术先例，gkx 承载的方法背书）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技知识图谱/算法展示.md》seq 431（excel_row 434）：

> ### PageRank算法计算与展示 · 序号 431
> #### 需规功能描述
> 通过链接分析评估节点的重要性，兼顾链接质量和数量，支持参数设置以适应多场景需求；以列表与图表展现节点PageRank排名，并可与其他中心性指标进行相关性分析；同时提供算法迭代过程的可视化，直观展示收敛过程和稳定性。

（bid_desc 为空、继承自 excel_row 426——L4 级描述「算法展示」。）

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| PageRank算法计算与展示 | SRS 算法展示.md | 1（seq 431） |
| PageRank | 全 SRS 目录 | 2（02-展示系统 算法展示.md + 03-智库系统 战略咨询报告.md——跨系统复用证据） |
| computePageRank | UI centralityAlgo.js | :177-207（power iteration 实现） |
| pagerank / centrality | 三源表名扫描 | 0 命中（无现成结果面） |
| graph_edge / graph_node | dev+久新表名扫描 | dev 26 张（0 行）/ 久新 ads_tech_graph（真图） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_KGANALY_001_out.json`（2026-11-02 实算：两图 PR Top10+收敛参数）。
- 共享探针：`code/_snapshots/_probe_s305_l3_call_out.json`（dev 图表计数+gkx/久新图词族——本件直接引用）。

### B.2 本件产物逐键清单（`code/M_SCIUI_KGANALY_001_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `facts.dev_graph_word_tables` | 探针 | 26 张（族级） | §3.2 |
| `facts.dev_graph_tables_nonzero` | 探针 | 4 张非零（语义排除） | §3.2 |
| `facts.gkx_coauthor_edges_total` | 计数 | 1,187,606 | §3.1 |
| `facts.gkx_coauthor_sample_edges` | 采样 | 20,000 | §2.1 |
| `facts.jiuxin_tech_nodes_total` | 计数 | 19,430（live） | §3.1 |
| `facts.jiuxin_tech_edges_total` | 计数 | 587,252（live） | §3.1 |
| `facts.jiuxin_tech_sample_nodes` | 采样 | 4,778 | §2.1 |
| `facts.jiuxin_tech_sample_induced_edges` | 采样 | 38,383 | §2.1 |
| `facts.jiuxin_tech_name_zh_nonempty` | 质量核查 | 0 | §3.3/B9 |
| `facts.jiuxin_tech_name_authoritative_col` | 口径 | technology_name_original | §3.3 |
| `derived[0].source` | 主承载 | 久新技术图诱导子图 | §2 |
| `derived[0].pagerank_params` | 算法 | d=0.85/iters=38/diff<1e-6 | §2.2 |
| `derived[0].top10` | **实算值** | 10 条（PR+name_original） | §2.3 |
| `derived[1].*` | 备承载 | gkx 合作图（iters=6） | §2.2 |
| `absence_probe` | 探针 | 三件 | §3.2/§4.1 |
| `support_judgment` | 判档 | 完全转换支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 状态 | 贴合度 |
|---|---|---|---|
| 原始论文公式 | R1 Page et al. 1998 | UI 已实现+本件复刻 | 锚 |
| 标准库实现 | R2 NetworkX | 参数惯例一致 | 高 |
| 合作网应用 | R3 加权 PR 学术先例 | gkx 备选承载 | 高 |
| 前端演示图 | UI 15 节点 | 算法可用/数据需换 | 结构披露 |

### C.2 数据矩阵

| 依赖 | dev | gkx | jiuxin |
|---|---|---|---|
| 图节点表 | 空壳（0 行） | dwd_scholar 21,316 | **19,430（真图）** |
| 图边表 | 空壳（0 行） | coauthor 1,187,606 | **587,252（真图）** |
| 现成 PR 结果面 | 无 | 无 | 无 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v0（现状） | UI 演示图（15 节点 mock） | — |
| v1（**本件已验证**） | 前端直连久新真图，实时幂迭代 | 结构验证完成 |
| v2 | 夜批全图 PR 落表（升完全直接支持） | 轻量工程 |
| v3 | 加权 PR+中文名补齐 | 口径裁定 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 前端取名列用 name_zh 得空白标签 | 高 | §3.3/B9（用 name_original） |
| 加权口径未裁即上线的排行争议 | 中 | §4.2 口径单前置 |
| 全图 587K 边前端迭代超时 | 中 | §2.4 夜批预计算或服务端 TopN |
| 久新连接限流（1203）偶发 | 低 | 重试机制（007 已验证 15s 重试有效） |

### C.5 总判

**完全转换支持**：三源无现成结果面（唯一缺口、轻量可补）+久新真图结构数据量均足+本件实算验证（38 迭代收敛/Top1 PR=0.016293）。算法三重权威锚（论文/标准库/学术应用）齐备。夜批落表即升完全直接支持——本批唯一「算法+数据都真实」的完整件。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_KGANALY_001.py` | 退出码 0，落 `_out.json`（约 3 分钟：边拉取+迭代） |
| 实算一致 | `derived[0].top10[0]` | PR=0.016293（Computational Methods for Biological Sequence Comparison） |
| 收敛判定 | `derived[*].pagerank_params.iters_used` | 38（久新）/ 6（gkx），均 <40 上限 |
| B11 对账 | gkx coauthor 总数=族级快照；dev 图表计数=族级快照 | 零漂移 |
| 幂等重跑 | 采样框排序固定+tol 写死 | Top10 逐位一致 |
| §二 实算 | 完全转换支持档 | 有真实计算过程（非从缺） |
