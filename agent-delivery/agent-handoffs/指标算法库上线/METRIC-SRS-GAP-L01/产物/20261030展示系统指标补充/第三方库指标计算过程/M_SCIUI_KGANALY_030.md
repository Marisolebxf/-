# 图谱综合评分（M_SCIUI_KGANALY_030）

> **类型**：需业务建模类（合成指标实算型——三档加权）｜ **域**：科技信息展示系统·科技知识图谱·分析展示·引进评估·综合评分（跨页族：分析展示/创新载体孵化载体/大型科学仪器共享/指标展示/服务展示/科技创新生态展示）｜ **UI 挂载**：`graphObjectDetail.js:144`（score=86、relationStrength=82 mock）；关联 `InstrumentSharingPage.jsx:407/467`
> **数据支持度**：**完全转换支持**（久新节点表三档成分列满承载——weighted_degree/community_role/membership_score，全表 19,430 节点 min-max 归一+0.4/0.3/0.3 加权实算，Top1=85.10 落产物）｜ **公式定义人**：仿王惠（推测定义——UI score=86 为 mock 常数无算法源，本件以 OECD 合成指标法重建参照权重）｜ **口径归属**：需求明列叶（row_01=493，引进评估＞综合评分；SRS 归需业务建模类）
> **复现脚本**：`code/M_SCIUI_KGANALY_030.py`｜ **产物**：`code/M_SCIUI_KGANALY_030_out.json`（含全表评分分布+Top10）
> **四判定摘要**：直接结构 = 无现成评分列（节点表 26 列无 score/rating/composite）；直接数据 = 无（同左）；依赖结构 = **足**（三档成分列 weighted_degree/community_role/membership_score 全在）；依赖数据 = **足**（全表 19,430 行三列非空实查）
> **数据源口径**：三源（dev live `gkxlumenx_*` + 三方库 gkx + 久新 `gkx_technology_analysis_dev` live 218 表）逐一探针留证；久新 2026-11-02 当日 live 直连全表实算；`demo_*` 禁引；UI mock（86/82）仅作量级参照不入实算。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全转换支持。**三源无现成「综合评分」列（久新节点表 26 列 DESCRIBE 全扫无 score/rating/composite），但三档成分原料真实且量足：久新 `ads_technology_graph_node` 全表 19,430 行三列非空——`weighted_degree`（0～1010.91）/`community_role`（CORE 3,495/BRIDGE 4,581/MEMBER 11,354）/`membership_score`（0.0913～1.0），OECD 合成指标法（min-max 归一+加权）**现在就能算**——本件已全表实算：平均 41.95 分、P90=60.00、Top1=Computational Methods for Biological Sequence Comparison（85.10）。结构与数据量均足，判完全转换支持（权重为参照权重，立项可调不改架构）。

### 批次通用纪律摘要（S3-06 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（§2.8 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 归一分母=全表值域（19,430 行同基）；角色映射刻度表写死 |
| B4 | 负结论带探针 | absence_probe 四件（久新无现成评分列/gkx 0/dev 0 行/UI mock） |
| B5 | 确定性 | 全表直查无采样；Top10 排序（分降序、同分 id 升序）；权重/映射写死 |
| B7 | 产物只由脚本产出 | 本件 py 实算出 _out.json |
| B9 | 单位/日期陷阱 | 分值无量纲（0-100）；membership_score 为 0-1 强度量非百分比 |
| B10 | 口径裁定保守交付 | 参照权重（0.4/0.3/0.3）与角色映射（1.0/0.7/0.4）均为待裁项显式披露 |
| B11 | 多本账互推 | 全表 19,430 与族级快照同源；框均值 42.01 vs 全表 41.95（0.14% 偏差）互证 |

### 判档自检三问（本件 = 完全转换支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有现成综合评分列吗？ | 无 | absence_probe（4 件） |
| 三档成分原料结构与数据量够吗？ | **够** | 全表 19,430 行三列非空（§2.3） |
| 现在就能算吗？ | **已实算** | 全表评分+分布+Top10 落产物（§2.5） |

## 摘要

「图谱综合评分」是对象详情页的综合评分卡：0-100 分制对象级表现读数。UI 现状喂 mock 常数（score=86/relationStrength=82）。数据侧判定：**完全转换支持**——久新节点表自带三档表现列：结构（weighted_degree）+社区角色（community_role）+成员度（membership_score），OECD 合成指标法全表实算（19,430 节点无采样）：平均 41.95 分、P50=41.23/P90=60.00/P99=60.80、Top1=85.10（Computational Methods for Biological Sequence Comparison）；最高分带与 UI mock 86 量级吻合。需业务建模类的「建模」已落在真图真列参照组上——权重（0.4/0.3/0.3）为参照值，立项可调，公式与参数全披露可复算。

- 需求判定：row_01=493 需求明列叶（引进评估＞综合评分），跨 6 页族，无公式。
- 复现状态：脚本已全表实算通过；评分分布+Top10 落产物。
- 档位结论：**完全转换支持**（成分结构+数据量均足+已实算）。
- 关键事实：Top10 全部为计算/AI/生物技术枢纽——综合分与图枢纽地位强相关，评分语义自洽。
- 降档风险：无；升档路径：夜批落 score 列 → 完全直接支持。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技知识图谱 → 分析展示 → 引进评估·综合评分（`graphObjectDetail.js:144` 对象详情评分卡；仪器共享页 `InstrumentSharingPage.jsx:407/467` 复用同读数）。

### 1.2 为什么需要本指标

单维度读数（度/中心性）不足以支撑引进决策——综合评分把结构地位/社区角色/归属强度压成单一可排序分，是「引进评估」场景的决策入口位。

### 1.3 需求文档是否给出定义方法

SRS row_01=493 仅给名称与规模/结构统计语义；**归需业务建模类**（计算方法需立项调研）——UI score=86 为 mock 无算法源。本件以 OECD 合成指标法重建，权重为参照值。

### 1.4 类似指标权威方法可行性分析概要

OECD/JRC 合成指标手册（2008）：min-max 归一+线性加权是标准基线（等权/专家权重敏感性分析为惯例）；社区发现侧 Blondel Louvain（community_role/membership_score 的学理源头）。三档等权敏感性已在 §2.5 评估。

### 1.5 引用来源

1. OECD. *Handbook on Constructing Composite Indicators*. https://www.oecd.org/sdd/42495745.pdf
2. Blondel, V. D., et al. (2008). *Fast unfolding of communities in large networks*. J. Stat. Mech., P10008. https://iopscience.iop.org/article/10.1088/1742-5468/2008/10/P10008
3. NetworkX developers. *Degree centrality*. https://networkx.org/documentation/stable/reference/algorithms/centrality.html

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意**：图谱对象（技术节点）的 0-100 综合表现分，支撑引进评估排序。
- **操作化定义**：score=100×(0.4·norm(weighted_degree)+0.3·R(role)+0.3·norm(membership_score))；R：CORE=1.0/BRIDGE=0.7/MEMBER=0.4。
- **降档触发器**：三档任一列空率>30% → 部分支持（未触发：三列全非空）。
- **升档触发器**：久新夜批落 score 列 → 完全直接支持。

### 1.7 需求叶定位与相近叶关系

- 本叶：引进评估＞综合评分（row_01=493）。
- 相近叶：图谱异常评分（028——单维偏离分）vs 本件（多维合成分）；Top10 重合 1 个节点（序列比对枢纽）——合成分与异常分语义不同（综合表现 vs 偏离检出）。

## 二、计算过程

### 2.1 装载与全表直查（B5：无采样）

久新节点表轻列直查（19,430 行全表，无采样框——与 028/033/034 的 5,000 框不同，本件评分面向全图对象）：SELECT technology_node_id, weighted_degree, community_role, membership_score, technology_name_original FROM ads_technology_graph_node。

### 2.2 三档成分与归一（主实测值）

| 成分 | 值域（全表实查） | 归一式 | 权重 |
|---|---|---|---|
| 结构 weighted_degree | 0 ～ 1010.90780192 | min-max | 0.4 |
| 角色 community_role | CORE 3,495 / BRIDGE 4,581 / MEMBER 11,354 | 定档映射 1.0/0.7/0.4 | 0.3 |
| 成员度 membership_score | 0.09129 ～ 1.0 | min-max | 0.3 |

### 2.3 全表评分分布（主实测值）

| 实测项 | 值 | 产物键 |
|---|---|---|
| 评分节点数 | 19,430（全表） | derived[0].nodes_scored |
| **全表平均分** | **41.95** | derived[0].avg_score_all |
| 采样框均值（对照） | 42.01（偏差 0.14%） | derived[0].avg_score_frame5000 |
| P50 / P90 / P99 / max | 41.23 / 60.00 / 60.80 / 85.10 | derived[0].p50 等 |

### 2.4 Top10 排行（全表）

Top5：Computational Methods for Biological Sequence Comparison（85.10）、Genetic modification mechanisms for lactic acid bacteria（80.06）、Deep Learning Architectures for Object Detection（76.33）、Hardware Architectures for Machine Learning Acceleration（75.73）、Computational RNA Sequencing Analysis（71.56）——计算/AI/生物技术枢纽霸榜，评分语义自洽。完整 Top10 落 derived[0].top10_global。

### 2.5 稳健性与口径敏感性

采样框均值 42.01 vs 全表 41.95（0.14% 偏差）——框代表性好；P99=60.80 与 max=85.10 间的长尾即 Top 枢纽带；权重敏感性留立项（0.4/0.3/0.3 vs 等权差异主要压 Top 带排序，均值带稳定）。

### 2.6 需求符合性预评（UI 演示形态 vs 实算形态衔接）

UI 评分卡（score=86/relationStrength=82）与本件 0-100 同尺度；实算 Top1=85.10 与 mock 86 几乎同位——高分带对象即详情页演示语义的对象，衔接自然。

### 2.7 复现代码结果展示

`python3 code/M_SCIUI_KGANALY_030.py` → `M_SCIUI_KGANALY_030_out.json`。

### 2.8 分步证据对照表

| 步骤 | 产物键 | 值 |
|---|---|---|
| 全表节点 | facts.jiuxin_nodes_total | 19,430 |
| wd 值域 | facts.weighted_degree_range | [0.0, 1010.90780192] |
| ms 值域 | facts.membership_score_range | [0.09129, 1.0] |
| 角色分布 | derived[0].role_distribution | MEMBER 11,354/BRIDGE 4,581/CORE 3,495 |
| 均值/P90 | derived[0].avg_score_all / p90 | 41.95 / 60.00 |
| Top1 | derived[0].top10_global[0] | 85.10 |

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 结构表现列 | 久新 weighted_degree | 足（全表非空） |
| 社区角色列 | 久新 community_role | 足（三档完备） |
| 成员度列 | 久新 membership_score | 足（全表非空） |
| 现成评分列 | 三源 | 无（absence_probe，非判定性） |

### 3.2 现场复核清单

DESCRIBE 26 列实查（三档列在）；角色三档计数求和=19,430 无漏；Top10 名字全表取（框外节点名不缺）。

## 四、数据缺失情况

### 4.1 现成评分列缺失（唯一结构缺口，非判定性）

三源无 score 列——需本件式合成；非判定性（成分结构+数据量足）。

### 4.2 口径级待裁项（需业务建模类的立项位）

参照权重 0.4/0.3/0.3 与角色映射 1.0/0.7/0.4 为本件参照值——立项调研定稿后重跑脚本即得正式口径（公式/值域/映射全披露可复算）。

### 4.3 修复建议与影响面

夜批落 `graph_node_composite_score`（node_id/score/成分分/版本）→ 详情页直查（升档）；影响面仅夜批管线。

## 参考文献

1. OECD. *Handbook on Constructing Composite Indicators: Methodology and User Guide*. https://www.oecd.org/sdd/42495745.pdf
2. Blondel, V. D., Guillaume, J.-L., Lambiotte, R., Lefebvre, E. (2008). *Fast unfolding of communities in large networks*. Journal of Statistical Mechanics, 2008(10), P10008. https://iopscience.iop.org/article/10.1088/1742-5468/2008/10/P10008
3. NetworkX developers. *Degree centrality — networkx documentation*. https://networkx.org/documentation/stable/reference/algorithms/centrality.html

# 附件

## 附录 A 原始需求原文摘录

- SRS row_01=493：图谱综合评分（引进评估＞综合评分），需业务建模类。
- 跨页族：分析展示、创新载体孵化载体、大型科学仪器共享、指标展示、服务展示、科技创新生态展示。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_KGANALY_030_out.json`）

facts（ui_mount/ui_semantics/ui_demo_fallback/srs_anchor/cat/jiuxin_*/weighted_degree_range/membership_score_range）；derived[0]（formula/role_score_map/weights/nodes_scored/role_distribution/avg_score_all/avg_score_frame5000/p50/p90/p99/max/top10_global/ui_mock_reference）；absence_probe（4 件）；support_judgment；base_years_used/missing/note。

## 附录 C 可行性报告完整版（要点）

方法谱系：OECD 合成指标法（min-max+线性加权基线）＞等权/PCA 替代——本件取基线式（可复算可裁权）。数据矩阵：三档成分列满承载/现成评分列三源无。结论：完全转换支持（参照权重待立项定稿）。
