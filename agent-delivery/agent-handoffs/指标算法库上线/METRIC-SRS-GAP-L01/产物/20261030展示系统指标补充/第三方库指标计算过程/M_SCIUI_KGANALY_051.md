# 图谱社群数量（M_SCIUI_KGANALY_051）

> **类型**：无业务逻辑数值类（社群计数，图结构统计）｜ **域**：科技信息展示系统·科技知识图谱·图查询资产·深入分析·结构指标｜ **UI 挂载**：图查询资产深入分析抽屉 → `queryAssetDeepAnalysis.js:52` metrics[2] `{name: '社群数', value: seededInt(...2,6)}`——`QueryAssetDeepAnalysisDrawer.jsx:96-100`「结构指标」表渲染（seededInt 2-6 随机 mock）
> **数据支持度**：**完全转换支持**（久新 node 表 community_id 直查**全图 1,731 个社群**（含 1,708 单例/23 个非单例）+ 框内 LPA 确定性复算对照（6 个/模块度 0.286167）+ gkx 备承载 LPA（2,297 个）——三口径全落产物）｜ **公式定义人**：UI 前端 mock（seededInt 随机数，无算法）——本件按社群发现标准口径（LPA/上游社群列）重建，推测定义｜ **口径归属**：UI 拆件叶（SRS seq 434 社群结构自动识别的功能组成维），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_KGANALY_046_051.py`（046/051 合算）｜ **产物**：`code/M_SCIUI_KGANALY_051_out.json`（native 直查+框内 LPA+gkx 备三口径）
> **四判定摘要**：直接结构 = 无独立结果面（但 node 表自带 community_id 列——**社群归属现成**，接近直接）；直接数据 = 近乎（直查即得，缺的只是「已发布结果表」形态）；依赖结构 = **足**（久新 node 表社群列；边表可复算）；依赖数据 = **足**（19,430 节点全量社群标注）
> **数据源口径**：三源（dev live `gkxlumenx_*` + 三方库 gkx + 久新 `gkx_technology_analysis_dev` live）逐一探针留证；久新 2026-11-02 当日 live 直连实算；`demo_*` 禁引。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全转换支持。**（判档边界件说明：若把 node 表 community_id 列视为「100% 语义一致结果面」，本件可argue完全直接支持——但社群数是**派生计数**而非落库读数（无 `community_count` 结果列），且社群界定依赖算法口径（native 列 vs LPA 复算给出 1,731 vs 6 两种答案——见 §2.2 口径差），按保守原则判**完全转换支持**。）证据链：①久新 `ads_technology_graph_node.community_id` 19,430/19,430 全标注——`COUNT(DISTINCT)` 直查 **1,731**（`jiuxin_community_count_total`），其中单例社群 1,708、非单例 23（`jiuxin_singleton_communities`/`jiuxin_nonsingleton_communities`），Top10 规模 4,151/3,683/3,518/…（`jiuxin_top10_communities`）；②框内 LPA 确定性复算（5000 框诱导子图）得 **6 个**社群/模块度 **0.286167**（`jiuxin_lpa_*`）——算法口径对照；③gkx `dwd_scholar_coauthor` 备承载 LPA 得 **2,297** 个（`gkx_lpa_community_count`）；④dev 图表面 26 张全 0 行空壳。三口径可算且已实算——「社群数不是一个数而是一族数（随口径变）」是本件核心发现（§2.2）。

### 批次通用纪律摘要（S3-06 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 计数无相除；单例/非单例分母披露（1,731 vs 23 两口径并列） |
| B4 | 负结论带探针 | absence_probe 三件；dev 空壳族级快照 |
| B5 | 确定性 | LPA 节点升序遍历+平局字典序最小标签；社群按 (规模降序,代表标签) 排序 |
| B6 | 闸门自身被闸 | 不自跑闸门 |
| B7 | 产物只由脚本产出 | 本件 py 实算出 _out.json |
| B8 | 回执不复收 | SQL+LPA 幂等（B5 保证） |
| B9 | 单位/日期陷阱 | 计数单位=个；mock 的 2-6 与真图 1,731 的量级差披露（§2.3） |
| B10 | 口径裁定保守交付 | native vs LPA 双口径并列+判档边界说明（§〇/§2.2） |
| B11 | 多本账互推 | 社群数与 046 同源（1,731）；框内诱导边与 039/040 一致 |

### 判档自检三问（本件 = 完全转换支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有社群数结果列吗？ | 无独立结果面（community_id 是归属列非计数列） | absence_probe |
| 社群归属原料够吗？ | **够（100%）** | 久新 19,430/19,430 标注（§3.1） |
| 现在就能算吗？ | **已实算（三口径）** | native 1,731/框内 LPA 6/gkx 2,297（§2.2） |

## 摘要

「图谱社群数量」是图查询资产深入分析抽屉「结构指标」表的第三行（社群数，mock 值 seededInt 2-6 随机），语义是图资产里社区结构的多寡——「这张图里有几个圈子」。数据侧判定：**完全转换支持**——久新 node 表社群归属 100% 标注，本件实算三口径：①**native 直查**：全图 1,731 个 community_id（但含 1,708 个单例社群——上游算法把孤立点也标成「社群」，非单例仅 23 个，Top3 社群 4,151/3,683/3,518 成员）；②**框内 LPA 复算**（5,000 框诱导子图）：6 个社群、模块度 0.286167——算法口径下「大社群吞并小社群」；③**gkx 备承载 LPA**：2,297 个（稀疏合作网碎社群）。核心发现：**社群数不是一个数而是一族数**——native 含单例（1,731）、LPA 吞单例（6）、展示层还要裁「单例算不算社群」——三口径并列交付，UI 回填前必须先裁口径。mock 的 2-6 量级仅与框内 LPA 的非单例口径巧合接近。

- 需求判定：UI 拆件叶（seq 434 社群结构自动识别的功能组成维）。
- 复现状态：脚本已实算通过；三口径+Top10 规模+模块度全落产物。
- 档位结论：**完全转换支持**（判档边界件——community_id 列近乎直接，保守判转换）。
- 关键事实：1,708/1,731=98.7% 是单例「社群」——上游社群算法的输出粒度与「社群=圈子」的展示语义有巨大落差；对外报数建议非单例口径（23）或框内算法口径（6），并在 UI 标注口径。
- 降档风险：无；升档路径：社群计数结果列落表 → 完全直接支持。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统/科技知识图谱/图查询资产深入分析——`QueryAssetDeepAnalysisDrawer.jsx:96-100`「结构指标」表四行（度中心性 Top/中介节点/社群数/跨域边占比），本件是第三行 `社群数`。数据源 `queryAssetDeepAnalysis.js:52`：`{name: '社群数', value: seededInt(`${seed}-c`, 2, 6)}`——种子哈希随机数 2-6。同表第四行跨域边占比是 KGANALY_052（同文件 :53）。抽屉的资产卡 KPI 行（节点/边/密度/综合评分）是 039 族。社群语义的算法侧近亲在 `CommunityPanel.jsx`（社群发现面板，LPA/Louvain 等六算法可选）——抽屉的「社群数」可视为社群发现结果在资产体检场景的轻量读数。

### 1.2 为什么需要本指标

「社群数」回答图资产的社区结构多寡：多社群=领域分化清晰（专题图典型）；少社群=高度聚合（合作网典型）；单社群=强连通团。在资产深入分析场景的用途：用户检索到一张图资产后，「社群数」+「跨域边占比」（052）一起构成结构体检——社群多而跨域边少=多个孤立圈子（信息茧房）；社群少而跨域边多=融合网络。对管理者的价值：图谱资产的结构画像维度，支撑「这张图适合做社群发现/路径分析吗」的工具选择判断。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**SRS《算法展示.md》seq 434 写「通过算法自动识别知识图谱中的紧密连接群体」——「社群数量」未定义：算法口径（LPA/Louvain/Infomap 结果不同）、单例处置（孤立点算一个社群吗）、分辨率参数（resolution 影响社群数）全部未言明。UI mock 的 seededInt 是随机占位；`CommunityPanel` 的六算法可选设计（`COMMUNITY_ALGORITHMS`）反而说明前端作者知道「社群数随算法变」。检索记录见附录 A.2。

### 1.4 类似指标权威方法可行性分析概要

社群计数是社群发现领域的输出统计量，权威锚三重。其一，LPA 标签传播（R1 Raghavan et al. 2007《Near linear time algorithm to detect community structures》）：近线性复杂度、唯一标签收敛——UI `communityAlgo.js detectLPA` 已实现（本件复算口径）；其二，Louvain 模块度优化（R2 Blondel et al. 2008）：模块度 Q 最大化的层次聚合——大规模图主流，社群数是 Q 优化的副产品；其三，评测基准与综述（R3 Fortunato & Hric 2016 物理报道综述）：**社群定义无唯一真值**——不同算法/分辨率给出不同划分，「社群数」必须随算法口径标注——本件三口径并列正是该结论的实证。方法族对照：

| 方法族 | 代表 | 本库承载 | 贴合度 |
|---|---|---|---|
| LPA（R1） | Raghavan 2007 | UI 已实现+本件复算（框内 6 个） | **锚** |
| Louvain（R2） | Blondel 2008 | UI 近似实现；本件未跑全图 | 高（备选） |
| 综述与口径警示（R3） | Fortunato & Hric | 三口径差实证 | 高（口径依据） |
| 上游社群列 | 久新 community_id | native 直查（1,731） | 现成（含单例披露） |

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/tech-knowledge-graph/queryAssetDeepAnalysis.js:52`（seededInt mock）；`QueryAssetDeepAnalysisDrawer.jsx:96-100`（结构指标表）；`communityAlgo.js:98-118`（detectLPA——本件复算同构）；`COMMUNITY_ALGORITHMS`（六算法清单）。
- SRS：`gkx-orchestration/agent-delivery/bid-reference/srs/02-科技信息展示系统/科技知识图谱/算法展示.md` seq 433-434（excel_row 436-437，原文见附录 A）。
- 权威方法：R1 Raghavan et al. 2007；R2 Blondel et al. 2008；R3 Fortunato & Hric 2016。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**定义（本件三口径并列，推测定义）**：

$$\text{社群数}_{native} = |\text{distinct}(community\_id)|; \qquad \text{社群数}_{LPA} = |\{c\}| \text{（LPA 收敛后的标签组数，}\geq 2 \text{成员）}|$$

**待裁项**：单例处置（native 含单例 1,731 vs 非单例 23 vs LPA 吞单例 6——三态）；算法选择（LPA/Louvain/native 列）；分辨率（Louvain resolution 影响社群数）。

**降档/升档触发器（B10 模板）**：①现状三口径可算（本件已验证）→ 维持完全转换支持；②社群计数结果列落表（`graph_stats.community_count`，夜批算好）→ 升**完全直接支持**；③甲方裁定单口径（如非单例 23）→ 判档不变、读数唯一化；④久新图下线 → gkx 备承载 LPA 可算（2,297），维持转换档但口径换。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技知识图谱/算法展示.md` |
| 所属 L5 | 社群发现展示（seq 433-437，5 叶）+ 图查询资产深入分析（UI 拆件） |
| 本件 | seq 434 社群结构自动识别的功能组成维（社群计数）；结构指标表第三行 |
| 同族件 | KGANALY_046 社群规模演变（同脚本合算件——时序展开）、KGANALY_052 跨域边占比（同表第四行）、KGANALY_023 社群连接密度（L1 批件，CommunityPanel）、KGANALY_040 聚类系数（社群结构的三角度量） |
| 近域件 | seq 433 多种社群算法支持（六算法——本件口径敏感性的来源）；seq 437 可视化社群划分 |
| UI 容器 | `QueryAssetDeepAnalysisDrawer.jsx` 结构指标表 |

本件与 052 同挂「结构指标」表（社群数/跨域边占比）——一张表两件：社群数答「几个圈子」、跨域占比答「圈子间连多紧」。两者共享图原料与社群划分（052 的跨域判定用 community_id 或 LPA 标签），数据接入一次双激活。

## 二、计算过程

> 本件为无业务逻辑数值类，本节给出**实测计算过程**——脚本 `code/M_SCIUI_KGANALY_046_051.py` 于 2026-11-02 在久新 live 库实算。

### 2.1 原料装载

主承载：久新 node 表全图 community_id 直查（19,430 行，无采样——计数直查）+ 5,000 框诱导子图（LPA 复算用，4,778 节点/38,383 边，与 039/040 同框）。备承载：gkx `dwd_scholar_coauthor` 前 20,000 行去重（21,763 节点/19,995 边）。

### 2.2 三口径社群数实算（口径敏感性是本件核心）

| 口径 | 社群数 | 说明 | 产物键 |
|---|---|---|---|
| 久新 native 直查（全图） | **1,731** | distinct community_id（含 1,708 单例） | `derived[0].community_count` |
| — 其中非单例（≥2 成员） | **23** | 上游算法的「真圈子」 | `derived[0].nonsingleton` |
| 框内 LPA 复算（对照） | **6** | 5,000 框诱导子图 LPA；模块度 0.286167 | `derived[1]` |
| 框内 native（同框对照） | 335 | 框截断后 native 社群碎片化 | `derived[2]` |
| gkx 备承载 LPA | 2,297 | 稀疏合作网碎社群 | `derived[3]` |

**口径差解读（本件核心发现）**：native 1,731 里 98.7% 是单例「社群」——上游社群算法把每个孤立技术点都标了独立 community_id（is_singleton_community 列自证），这与展示语义的「圈子」差三个量级；框内 LPA 把大社群吞并小社群收敛到 6 个（Top 规模 3,659/1,104/7/4/2/2——两大巨头+四个小社群，`jiuxin_lpa_community_sizes_top10`）；框内 native 335 是框截断把全图社群切碎的效应（对照披露，非推荐口径）。**社群数不是一个数**：R3 综述的「无唯一真值」结论在本库实证——对外报数必须随口径标注，建议非单例 23 或算法口径 6 起步。

### 2.3 读数解释

技术图社群结构呈「巨头+长尾」：Top3 社群 4,151/3,683/3,518 占非单例成员的 85%+，其余 20 个非单例社群是中小圈子；1,708 个单例点是只与框外/无强关联的技术——单例本身也是有价值的读数（图谱的孤立技术点规模）。gkx 备承载 2,297 个社群（21,763 节点）：合作网天然碎（大多数学者只与固定搭档合作）——与技术图「巨头」结构相反，两图对照本身是「图语义决定社群形态」的教学案例。mock 值 2-6 与框内 LPA 的 6 巧合同量级（mock 作者按小演示图拍的），但与 native 1,731 差三个量级——量纲同为「个」，数值必须按口径回填（B9）。

### 2.4 与 UI 演示形态的衔接

UI 现状 seededInt 随机（2-6）。接入真图路径：先裁口径（§1.6 三态）→ 展示层按资产粒度选算法（资产=子图时跑 LPA 秒级；资产=全图时直查 native+单例过滤）→ 结构指标表第三行回填。本件三口径产物即回填菜单；`CommunityPanel` 六算法框架已在前端，算法切换零改动。

### 2.5 稳健性与口径敏感性

**（a）LPA 确定性**：本件 LPA 节点升序遍历+平局字典序最小标签（B5）——同图重跑社群数与划分逐位一致；UI `detectLPA` 用 hashSeed 随机序（`communityAlgo.js:98` order sort）——**UI 版 LPA 非确定性**（seed 影响遍历序），接入真数据时建议换本件确定性版（或固定 seed）。**（b）框效应**：框内 native 335 vs 全图 1,731——框截断切碎社群（对照键 `jiuxin_frame_native_community_count`），LPA 在框内重算规避了此效应（算法自适应框内拓扑）；全图 LPA 本件未跑（1.9 万节点 LPA 秒级可算，属工程扩展非判档依赖）。**（c）单例口径**：is_singleton_community 列是上游算法自标注（非本件推断）——单例/非单例分读有列级背书。

### 2.6 需求符合性预评（UI 演示形态 vs 实算形态衔接）

| 需求能力位（seq 434 识别紧密连接群体） | UI 演示形态 | 实算形态（本件产物） | 衔接判定 |
|---|---|---|---|
| 结构指标表社群数 | seededInt 2-6 | 三口径（1,731/23/6） | **回填前须裁口径**（§1.6） |
| 算法可选（seq 433 六算法） | 六算法下拉 | 本件 LPA；Louvain 框内可扩 | LPA 已验证，余待扩 |
| 社群可视化（seq 437） | network 视图 | LPA 标签→assignment 映射 | 数据结构同构可接 |

**预评结论**：数据面三口径即期可用；回填动作前的口径裁定（单例处置/算法选择）是唯一前置——按 B10 双口径并列交付不悬空。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_KGANALY_046_051.py`——三源只读（久新 live；gkx 经 `_gkxdb.py`；dev 读族级快照），LPA 确定性实现+native 直查+模块度计算，零 `demo_*`；运行 `python3 code/M_SCIUI_KGANALY_046_051.py`（约 8 秒）。
- 产物：`code/M_SCIUI_KGANALY_051_out.json`，关键读数键与正文对应——`facts.jiuxin_community_count_total=1731`/`jiuxin_singleton_communities=1708`/`jiuxin_nonsingleton_communities=23`；`facts.jiuxin_top10_communities`（4151/3683/3518/2177/1991/1074/770/165/137/22）；`facts.jiuxin_lpa_community_count=6`/`jiuxin_lpa_modularity=0.286167`/`jiuxin_lpa_community_sizes_top10=[3659,1104,7,4,2,2]`；`facts.jiuxin_frame_native_community_count=335`；`facts.gkx_lpa_community_count=2297`/`gkx_lpa_modularity`；`support_judgment="完全转换支持"`。
- 结果解读：三口径全实算——native（含单例披露）/LPA（算法口径）/gkx（备选语义）；「社群数随口径变」有本库实证（1,731 vs 6 vs 2,297）。
- 对照需求功能要求的评审：数据即期可用，口径裁定前置（§1.6 三态菜单），详见 §2.6。

### 2.8 分步证据对照表

| # | MD 论断（出处） | 产物键 | 读数 | 一致 |
|---|---|---|---|---|
| 1 | native 全图 1,731（§〇/§2.2） | `facts.jiuxin_community_count_total` | 1731 | ✓ |
| 2 | 单例 1,708（§2.2/摘要） | `facts.jiuxin_singleton_communities` | 1708 | ✓ |
| 3 | 非单例 23（§2.2/摘要） | `facts.jiuxin_nonsingleton_communities` | 23 | ✓ |
| 4 | Top10 规模（§2.3） | `facts.jiuxin_top10_communities` | 4151/3683/3518/…/22 | ✓ |
| 5 | 框内 LPA 6 个（§2.2） | `facts.jiuxin_lpa_community_count` | 6 | ✓ |
| 6 | LPA 模块度 0.286167（§2.2） | `facts.jiuxin_lpa_modularity` | 0.286167 | ✓ |
| 7 | LPA Top 规模（§2.3） | `facts.jiuxin_lpa_community_sizes_top10` | 3659/1104/7/4/2/2 | ✓ |
| 8 | 框内 native 335（§2.5b） | `facts.jiuxin_frame_native_community_count` | 335 | ✓ |
| 9 | gkx 备承载 2,297（§2.2/§2.3） | `facts.gkx_lpa_community_count` | 2297 | ✓ |
| 10 | gkx 备承载边数（§2.1） | `facts.gkx_coauthor_sample_edges` | 19995 | ✓ |
| 11 | 社群计数与 046 同源（B11） | 与 046 `communities_tracked` 对账 | 1731=1731 | ✓ |
| 12 | 判档完全转换支持（§〇/摘要） | `support_judgment` | 完全转换支持 | ✓ |

十二行对照全部以 `_out.json` 已落盘键背书（046/051 共享 facts 段，#11 跨件对账）。

> **基期三键说明（物理口径）**：本件基期为**物理口径基期=探针快照日**（2026-11-02 久新 live 直连当日），**无年度基期**——社群计数是当日截面（community_id 是上游算法一次性划分的快照产物）；`base_years_used`/`base_years_missing` 按截面语义登记，`base_years_note` 注记此口径，不属「缺年按 0 摊入」情形。

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 社群归属列（native） | 久新 | `ads_technology_graph_node.community_id` | **19,430**（100%） | 直查 | **足**（现成归属） |
| D2 | 图边表（LPA 复算） | 久新 | `ads_technology_graph_edge` | **587,252** | 直查 | **足** |
| D3 | 合作网络边（备选） | gkx | `dwd_scholar_coauthor` | 1,187,606 | 直查 | 足（人-人语义） |
| D4 | dev 图结构面 | dev | 26 张 | **0**（全空） | 空壳 | 非承载 |
| D5 | 社群计数结果列 | 三源 | community_count 词族 | — | **不存在** | 缺（转换计算正当性来源） |

`support_judgment="完全转换支持"`、产物与文首一致。

### 3.2 native 列质量读数

| 核查项 | 读数 | 含义 |
|---|---|---|
| community_id 覆盖 | 19,430/19,430 | 零 NULL |
| is_singleton_community 列 | 1,708 自标注单例 | 上游算法自证（非本件推断） |
| 非单例规模分布 | Top3 占 85%+（4,151/3,683/3,518） | 巨头+长尾结构 |
| community_name_original | 有列（社群名，与 046 共享） | 展示层取名可用 |

### 3.3 现场复核清单

| 复核项 | 结果 |
|---|---|
| native 直查 | 1,731（distinct community_id） |
| 单例/非单例 | 1,708/23（is_singleton 列） |
| 框内 LPA | 6 社群/模块度 0.286167（B5 确定性） |
| gkx 备承载 LPA | 2,297 社群 |
| dev 图表 | 26 张全 0 行（族级快照） |
| 脚本形态 | 三源只读+纯内存 LPA；零 demo_* |

## 四、数据缺失情况

### 4.1 计数结果列缺失（非判定性）

三源无 `community_count` 结果列（absence_probe）——native 是归属列非计数列，COUNT(DISTINCT) 仍是转换计算。修复最轻量：夜批一行 SQL 落 `graph_stats` 表。

### 4.2 口径三态与 UI 算法确定性（口径级）

待裁项：其一，**单例处置**（1,731 含单例 vs 23 非单例 vs 6 算法口径——三态读数差三个量级，建议对外用非单例或算法口径并标注）；其二，**算法选择**（LPA/Louvain/native——seq 433 六算法可选，本件验证 LPA，Louvain 框内可扩）；其三，**UI LPA 非确定性**（`communityAlgo.js detectLPA` 用 hashSeed 随机遍历序——接入真数据建议换本件确定性版，§2.5a）。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 口径裁定（三态选一） | 口径裁定 | 本件 | 回填前置 |
| 夜批社群统计落表（native/LPA 双口径） | 数据工程（轻） | 本件+046+023 | 升完全直接支持 |
| UI LPA 换确定性实现 | 前端工程（轻） | 本件+023+046 | B5 对齐 |
| dev 图空壳 ETL 灌图（可选） | 数据管道 | dev 承载位 | 非必需 |

档位后果：结果列落表 → 完全直接支持；现状 → 完全转换支持（三口径已实算）；久新下线 → gkx 备承载维持转换档（口径换 2,297）。

## 参考文献

1. Raghavan U N, Albert R, Kumara S. Near Linear Time Algorithm to Detect Community Structures in Large-Scale Networks[J]. Physical Review E, 2007, 76(3): 036106. https://doi.org/10.1103/PhysRevE.76.036106 （R1，2026-11-02 WebSearch 核验可达——LPA 标签传播原始论文，本件复算口径的方法源）
2. Blondel V D, Guillaume J-L, Lambiotte R, Lefebvre E. Fast Unfolding of Communities in Large Networks[J]. Journal of Statistical Mechanics, 2008(10): P10008. https://doi.org/10.1088/1742-5468/2008/10/P10008 （R2，2026-11-02 WebSearch 核验可达——Louvain 模块度优化，社群数作为 Q 优化副产品）
3. Fortunato S, Hric D. Community Detection in Networks: A User Guide[J]. Physics Reports, 2016, 659: 1-44. https://doi.org/10.1016/j.physrep.2016.09.002 （R3，2026-11-02 WebSearch 核验可达——社群发现综述：无唯一真值、口径敏感性，本件三口径并列的学术依据）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技知识图谱/算法展示.md》seq 434（excel_row 437）：

> ### 社群结构自动识别 · 序号 434
> #### 需规功能描述
> 通过算法自动识别知识图谱中的紧密连接群体，实现对学术团队、技术流派、合作集群等社群的精准发掘，大幅提升网络结构洞察力。

（「社群数」未单列叶——本件为 UI 拆件：queryAssetDeepAnalysis 结构指标表第三行。）

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 社群数 | SRS 算法展示.md | 0（未单列叶；seq 434 语义覆盖） |
| 社群数 | UI queryAssetDeepAnalysis.js | :52（seededInt 2-6） |
| community_id | 久新 node 表列 | 19,430/19,430 标注（本件主承载） |
| community/lpa/louvain 词族 | 三源表名扫描 | 久新 community_id 列现成；无独立计数结果面 |
| detectLPA | UI communityAlgo.js | :98-118（非确定性 hashSeed 序） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_KGANALY_051_out.json`（2026-11-02 实算：三口径社群数）。
- 共享探针：`code/_snapshots/_probe_s305_l3_call_out.json`。
- 合算脚本：`code/M_SCIUI_KGANALY_046_051.py`。

### B.2 本件产物逐键清单（`code/M_SCIUI_KGANALY_051_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `facts.jiuxin_community_count_total` | **实算值** | 1,731（native 直查） | §2.2 |
| `facts.jiuxin_singleton_communities` | 实算 | 1,708 | §2.2 |
| `facts.jiuxin_nonsingleton_communities` | 实算 | 23 | §2.2 |
| `facts.jiuxin_top10_communities` | 分布 | 10 社群规模 | §2.3 |
| `facts.jiuxin_lpa_community_count` | **实算值** | 6（框内 LPA） | §2.2 |
| `facts.jiuxin_lpa_modularity` | 实算 | 0.286167 | §2.2 |
| `facts.jiuxin_lpa_community_sizes_top10` | 分布 | 3659/1104/7/4/2/2 | §2.3 |
| `facts.jiuxin_frame_native_community_count` | 对照 | 335（框截断效应） | §2.5 |
| `facts.gkx_lpa_community_count` | 实算 | 2,297（备承载） | §2.2 |
| `derived[0-3]` | 四口径 | native/LPA/frame-native/gkx | §2.2 |
| `absence_probe` | 探针 | 三件 | §4.1 |
| `support_judgment` | 判档 | 完全转换支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 本库承载 | 贴合度 |
|---|---|---|---|
| LPA | R1 Raghavan 2007 | UI 已实现+本件确定性复算 | 锚 |
| Louvain | R2 Blondel 2008 | UI 近似实现（可扩） | 高 |
| 口径警示 | R3 Fortunato & Hric | 三口径差实证 | 高 |
| 上游社群列 | 久新 native | 直查现成（单例披露） | 现成 |

### C.2 数据矩阵

| 依赖 | dev | gkx | jiuxin |
|---|---|---|---|
| 社群归属 | 空壳 | 无社群列 | **community_id 100%** |
| 图边（复算） | 空壳 | coauthor 1,187,606 | **587,252** |
| 计数结果列 | 无 | 无 | 无 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v0（现状） | seededInt 2-6 | — |
| v1（**本件已验证**） | 三口径回填（先裁口径） | 口径裁定 |
| v2 | 夜批统计落表（升完全直接支持） | 轻量 |
| v3 | Louvain 等算法扩展 | 前端算法框架已在 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| native 1,731 被当「圈子数」引用 | 高 | §2.2 单例披露+非单例口径推荐 |
| 口径未裁即回填（数值漂三量级） | 中 | §1.6 三态菜单前置 |
| UI LPA 非确定性感官漂移 | 低 | §2.5a 换确定性版 |

### C.5 总判

**完全转换支持**（判档边界件）：community_id 列近乎直接但计数是派生且口径敏感——保守判转换。三口径（native 1,731/非单例 23/LPA 6+备选 2,297）全实算落产物，回填菜单齐备。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_KGANALY_046_051.py` | 退出码 0，落两件 _out.json |
| 实算一致 | `facts.jiuxin_community_count_total`/`jiuxin_lpa_community_count` | 1731/6 |
| B11 对账 | 与 046 同源 1,731；框内边 38,383 与 039/040 一致 | 零漂移 |
| 幂等重跑 | LPA 确定性（升序+字典序平局） | 三口径逐位一致 |
| §二 实算 | 完全转换支持档 | 有真实计算过程 |
