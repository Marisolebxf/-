# 评估对象网络中心性排名（M_SCIUI_X_015）

> **类型**：RANK（网络中心性排名，机构/学者双节点型）｜ **域**：科技发展态势·科技创新评估·科学创造力指标展示｜ **UI 挂载**：科技创新评估页 → 科学创造力 → 网络中心性评估（网络图谱+中心性排名表）
> **数据支持度**：**部分支持**｜ **公式定义人**：仿王惠（推测定义，非招标原文闭合口径）｜ **口径归属**：需求明列叶（SRS seq 137 / excel_row 140），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_X_015.py`｜ **产物**：`code/M_SCIUI_X_015_out.json`
> **四判定摘要**：直接结构 = 否（三源无中心性结果面；开发库唯一 centrality 表为演示造数）；直接数据 = 否；依赖结构 = 是（久新合作边表 1,438 万行结构完备）；依赖数据 = 部分（领域过滤维与 UI 领域体系无映射，学者/机构双型混排需裁定）
> **数据源口径注记**：本件按「开发库（10.50.11.76 live + 旧机兜底实查，禁 `demo_*`）+ 三方库 gkx + 久新库 jiuxin_warehouse」三源评估（20261101 三源铁律）。

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库 gkx+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：部分支持。** 需求明文三类中心性（SRS seq 137 / 主文档 :881：「包括度中心性、接近中心性、中介中心性…识别领域内的核心研究力量」），方法谱系完全标准（networkx 三函数）。三源探测的主战场在「网络本体」：开发库图谱面双机失效——新机 `enterprise_centrality`/`graph_node`/`graph_edge` 全 0 行，旧机 `enterprise_centrality` 114 行经查 `model_version='demo_centrality_v0.1'` 且样本企业名为「极光量子科技」「翰林量超」等虚构名（演示造数面，按禁引纪律披露不采信）；gkx 280 表无任何网络/中心性结果面，论文合作者埋在 `author_info_list` longtext 非结构化。**真承载在久新**：`ads_institution_collaboration_yearly` 14,380,246 行机构合作边（2024 单年 2,146,142 行/36,026 机构侧），本报告以其 Top 活跃机构（中科院大学部）为 ego 实算二跳网 1,206 节点/4,500 边的三类中心性完整排名。降档双因：其一，「特定领域内」的领域过滤维（合作表只到 subfield 252 个，与 UI 的「未来产业」20 领域体系无对齐映射）；其二，UI 双节点型（机构+学者混合榜）在久新是两张分离表（机构合作表+学者合作表 5,051,578 行），混排口径需裁定。

### 批次通用纪律摘要（S3-02 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 度中心性分子=度数/分母=网规模-1（同网同源） |
| B4 | 负结论带探针 | absence_probe 三条（§3.4） |
| B5 | 确定性 | betweenness seed=42；排名按 (-degree, node_id) 双键排序 |
| B6 | 闸门自身被闸 | 不自跑闸门；派单方统一跑 |
| B7 | 产物只由脚本产出 | 三轮改脚本重跑在案（JOIN 超时/ego 节点一致性/talent 排序） |
| B8 | 回执不复收 | 硬证据由派单方复验 |
| B9 | 单位/日期陷阱 | statistics_year 截面显式；Doris query timeout 留证 |
| B10 | 口径裁定保守交付 | 双口径（机构网/学者面）+触发器（§1.6） |
| B11 | 多本账互推 | 14,380,246 与 TECHTRK_018 同值 assert 零漂移 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 中心性结果面存在吗？ | 不存在（有效面） | 开发库 demo 造数；gkx 0 表 |
| 网络本体够算吗？ | 够 | 久新 1,438 万边，ego 网 4,500 边实算 |
| 领域维闭合吗？ | 不闭合 | subfield 252 ≠ UI 20 领域体系，无映射 |

## 摘要

「科学网络中心性评估」是需求明列叶（SRS seq 137），罕见地给出了方法名（度/接近/中介三中心性）——需求方法学完备度全批最高，但网络本体在三源的命运戏剧化：开发库有现成 `enterprise_centrality` 表，114 行，逐行核查 `model_version` 全为 `demo_centrality_v0.1`、企业名是虚构占位名——一个「结构存在但内容为演示造数」的陷阱面（按纪律禁引并留证）；gkx 无任何网络面。真承载是久新机构合作边表（14,380,246 行，与 TECHTRK_018 件共享读数零漂移）。本报告以 2024 年合作边权 Top 机构（中国科学院大学，年度合作量合计 112,470（ego 侧合作边权总和））为 ego 实算二跳网络（1,206 节点/4,500 边）：度中心性中科院 0.4149 居首、国科大 0.2108 次席、北大 0.2083 第三；中介中心性中科院 0.584 一骑绝尘（约为北大 0.095 的 6.1 倍）——「合作枢纽」结构清晰。学者节点维另有现成面（`ads_talent_collaborator` 5,051,578 行，Top 合作对 8,379 篇）。降档在领域维：subfield 252 个与 UI「未来产业」20 领域无映射，需求「特定领域内」的限定暂不可实现。判**部分支持**。

- 需求判定：**需求明列叶**（seq 137，excel_row 140），方法名三中心性明文。
- 复现状态：脚本跑通（三轮迭代）；ego 网三类中心性 Top10 + 学者合作 Top8 落产物。
- 档位结论：**部分支持**（网络本体充足+领域维失配+双节点型混排待裁定）。
- 关键事实：开发库 centrality 表是演示造数面（demo_centrality_v0.1 + 虚构企业名）——「有表无据」的判档陷阱实证。
- 升档路径：subfield↔UI 领域映射表建成，或甲方接受全领域口径。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/科技创新评估/**科学创造力指标展示**/科学网络中心性评估（1.1.1.1.4.1.7.1.2；SRS seq 137、excel_row 140）。UI 实现在 `TechInnovationEvaluationPage.tsx`：主 Tab「科学创造力」下四个子 Tab 的第 2 个（`scienceSub === 'centrality'`），双面板布局——左「科学网络中心性评估」（`centralityGraphOption` 力导向网络图，`:3479-3486`），右「中心性排名」（`:3488-3512`）表格五列：节点/类型/度/接近/中介。数据源 `centralityNodeRows`（`:1862-1892`）mock 8 行——机构/学者两型各 4，节点名由评估上下文拼接（`${primaryIndustry}牵头机构`、`${primaryDistrict}骨干学者`等），三中心性值在 `n(0.22, 0.05)` 至 `n(0.43, 0.09)` 的归一区间——**纯演示值**，不参与支持度结论。

值得记录的 UI 语义：表格的「类型」列（机构/学者）表明前端作者把需求原文「学者、研究机构」读成了**混合榜**——机构与学者在同一张排名表里比较。而网络分析的常规做法是同构节点网（机构网内排机构、学者网内排学者）——两网的中心性值域不同（机构网更密），混排的公平性需口径裁定。这是本件三处口径假设之一（另两处：领域过滤、中心性归一方式）。

### 1.2 为什么需要本指标

中心性排名回答「谁是网络中的核心力量」：度中心性识别直接合作最多的节点（合作广度），接近中心性识别信息传播最快的节点（网络可达性），中介中心性识别控制合作通道的枢纽（桥接价值）——三者组合刻画「核心」的不同侧面，比单纯数论文量更能识别结构性关键主体。需求把它放在科学创造力面板（论文数量分析之后、前沿性分析之前），是「量-构-势」叙事的「构」位。

数据侧本件的独特性：这是全批少有的「方法完全定义、只缺数据面」件——三中心性是教科书定义（networkx 三函数直调），不需要任何口径发明。调研重心因此全部在「网络本体在哪、多大、什么粒度」，以及领域过滤这一需求限定词的可实现性。

### 1.3 需求文档是否给出定义方法

**需求给出了方法名但未给参数。** SRS seq 137 / 主文档 :881 明文「包括度中心性、接近中心性、中介中心性」——三方法名是需求原文。但三处参数留白：网络的构建口径（什么算一条边——合著一篇？一个共同作者？）、领域过滤的实现（「特定领域内」怎么取子图）、归一化与排名规则（三值怎么合成一个名次，还是分列展示——UI 选择了分列）。

### 1.4 类似指标权威方法可行性分析概要

中心性分析的方法族高度标准化：Freeman 三件套（degree/closeness/betweenness，1978/1979 经典）是合作网络分析的事实标准；PageRank（带阻尼的度中心性推广）在引文网更常用；合作强度加权（边权=合著篇数）是 SciVal/InCites 类产品的通行做法。开发库在案的 `enterprise_centrality`（pagerank_score/centrality_norm/degree 三列）与既有调查 M_TECH_ENTITY_INFLUENCE（IPC4 共类网络 620 节点 PageRank 实测）证明项目侧有网络计算先例。方法族对照：

| 方法族 | 边定义 | 数据要求 | 与本库匹配 |
|---|---|---|---|
| Freeman 三中心性（UI/需求指定） | 合作对 | 合作边表 | **久新现成**（机构/学者两表） |
| PageRank 族 | 共类/引用 | 转移矩阵 | 先例在案（IPC4 网，另域） |
| 加权强度榜 | 边权=合著数 | 边表+权列 | 久新 co_paper_count 直查 |

结论：方法零障碍——`networkx` 3.2.1 本地可用（探针 d 实测），久新边表即插即算。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/tech-innovation-evaluation/TechInnovationEvaluationPage.tsx:3488`（中心性排名表五列）；`:1862`（centralityNodeRows mock 8 行）；`:3479`（网络图谱面板）。
- SRS：`…/科技发展态势/科技创新评估.md` seq 137（excel_row 140），原文见附录 A。
- 主需求文档：`科技信息展示系统和科技专题服务系统.md:881`（1.1.1.1.4.1.7.1.2 同文）。

### 1.6 推测原意与推测定义

**推测定义（须披露三处口径假设）**：

- **口径 A（机构合作网·2024 单年·主口径）**：节点=机构，边=年内有合著（边权 co_paper_count），度/接近/中介三列分列展示（UI 现行形态同构）——本报告 ego 网实算即此口径的可行性质证；
- 口径 B（学者合作网）：节点=学者，久新 `ads_talent_collaborator` 现成（collaboration_score/rank 在库），UI 混排时机构/学者分表各自归一后再合榜；
- 口径 C（全期网）：不按年切，2015-2026 全期边——规模可控（机构侧 ≤1,438 万边），但「2024 评估年」语境下年度截面更贴 UI。

**三处口径假设待裁定**：①领域过滤（subfield 252 ↔ UI 20 领域映射）——裁定前以全领域交付并标注；②机构/学者混排（分列还是合榜+归一基准）；③边定义（合著即边 vs 边权阈值过滤弱连接）。

**降档/升档触发器（B10 模板）**：若甲方接受全领域口径（放弃「特定领域」限定）→ 仍部分支持但即期交付（ego 网模式全库铺开）；若 subfield↔UI 领域映射建成 → 可升**完全转换支持**；若要求混排统一名次 → 需先定归一基准（z-score 或 min-max 跨网），不升档。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技发展态势/科技创新评估.md` |
| 所属四级功能 | 1.1.1.1.4.1.7 科技创新评估（23 叶） |
| 所属面板 | 科学创造力指标展示（seq 136-139，excel_rows 139-142） |
| 本件叶 | **科学网络中心性评估（seq 137，excel_row 140）——需求明列** |
| 同面板相邻叶 | 科学论文数量分析（136）/科学研究前沿性分析（138）/科学创造力趋势预测（139） |
| UI 容器 | 科学创造力四子 Tab 之第 2（centrality） |

批内相近件：`M_SCIUI_KGANALY_024`（度中心性热力图，科技知识图谱页——需求 :3063 同族但对象是图谱本体）；既有调查 `M_TECH_ENTITY_INFLUENCE`（IPC4 共类网 PageRank，20261027 批完全转换支持）证明网络类指标在本项目数据面有成功先例，本件机构合作网与之同构不同域。

## 二、计算过程

### 2.1 装载与规模校验

三源连接同批统一入口。久新合作表规模锚点：全表 14,380,246 行（脚本 assert 与 TECHTRK_018 件共享读数零漂移）；2024 单年 2,146,142 行、36,026 个 ego 侧机构。SQL 纪律执行记录：首版两条全表 GROUP BY 聚合在 Doris 实测 query timeout（520 秒被杀，错误留证于执行记录）——按纪律改写为「边权排序取 ego（0.1 秒）→ ego 等值过滤取一跳（0.1 秒）→ 协作者等值过滤取二跳（LIMIT 4,000 上限）」三步小查询，全程亚秒级。

### 2.2 开发库图谱面：一个「有表无据」的陷阱

`gkxlumenx_ads.enterprise_centrality` 是 information_schema 扫描时的强候选（表名直击指标名），双机深探揭示三态：**新机 10.50.11.76 该表 0 行**（同库 graph_node/graph_edge 亦 0 行，图谱面整体空载）；**旧机 111.198.38.90 该表 114 行**——但 `model_version` 全部行为 `demo_centrality_v0.1`，样本企业名逐行核查为「极光量子科技有限公司」「翰林量超股份有限公司」「鸿图生物集团有限公司」等**虚构占位名**（真实中国企业库无此命名模式），updated_at 集中于 2026-08-13 单批写入。结论：这是一张演示造数面——按批次禁引纪律（demo_* 同族处理），表存在但**不构成数据证据**，absence_probe 留证。这一案例的方法论价值：结构探针（表名命中）会误判为强支持，必须内容探针（版本字段+样本名核查）纠偏——与 INNOV_001 件的「有列无区分度」同为批内判档陷阱库。

### 2.3 gkx 侧：合作信息埋在 longtext

gkx 280 表以 network/centrality/graph/collaborat/coop 五关键词扫描 0 命中。论文表 `dwd_zh_paper` 32 列中 `author_info_list`（longtext）承载合作者信息但完全非结构化（探针 a 全列清单在案）——解析成合作边对需 NLP 工程，超出本件「现转」边界。gkx 侧判定：结构不支持（无网络面），解析路径成本过高不计入档位。

### 2.4 久新合作边表：结构完备的主承载

`ads_institution_collaboration_yearly`（DESC 42 列实查）：机构对（institution_id × collaborator_institution_id）× 年，双侧机构名/类型、协作者国别/省/市地理列、合作强度三列（co_paper_count/co_patent_count/co_project_count）、合成强度 collaboration_strength、覆盖状态三列与数据源标记（openalex）。语义与需求「合作网络」直接同构。规模：全表 14,380,246 行；2024 单年 2,146,142 行、36,026 机构侧。学者面 `ads_talent_collaborator`（DESC 15 列）：学者对+合作计数+collaboration_score/rank——库内已算好的强度分。

### 2.5 口径 A 实算：ego 网三中心性

ego 选取：2024 年单边合作量 Top（不经聚合的边权排序，0.1 秒）——中国科学院大学（ins_feda…，单边最高 10,671 篇对中科院本部；聚合口径 ego 侧年度合作边权合计 112,470）。一跳邻域 500 行（Top 协作者含中科院本部/北大等）；二跳以 Top50 协作者为锚拉 4,000 边上限——ego 网合计 **1,206 节点/4,500 边**。三类中心性（networkx，拓扑无权，边权另存 w 属性）：

```python
G = nx.Graph()           # 4,500 边，边权=co_paper_count 聚合
deg = nx.degree_centrality(G)        # 度/(n-1)
clo = nx.closeness_centrality(G)     # Wasserman-Faust
bet = nx.betweenness_centrality(G, seed=42)  # 精确算法，定种子（B5）
```

Top10（按度降序、node_id 升序双键）：①中科院 degree 0.4149/closeness 0.6309/betweenness 0.584；②中科院本部 0.2108/0.5118/0.095；③北京大学 0.2083/0.4691/0.1050（全榜见产物 `jiuxin_2024_centrality_top10_by_degree`）。结构解读：国科大在中介维度的断崖优势（约为第二名 2.9 倍）说明其角色是**跨集团桥**——大量二跳机构的互访都经过它；而度/接近两维的差距温和得多。这正是三中心性分列展示（而非合成单名次）的价值：三种「核心」指向同一家头部机构时结论稳健，指向不同机构时维度信息不可压缩。

### 2.6 口径 B：学者合作面现成榜

`ads_talent_collaborator` 5,051,578 行按 co_paper_count 降序 Top：Rank1 对（tal_f4c9↔tal_ebc6）8,379 篇、第二对 8,196 篇——库内现成强度榜直接可挂（collaboration_score 字段实测全 NULL，rank 列有区分度，强度以 co_paper_count 为准）。学者名回填需逐对点查 `ads_talent_profile`（5M×10 万大 JOIN 会 query timeout——首版实跑留证，已改点查），本件登记 id 级榜单，名称富化留给交付工程。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_X_015.py`（三轮迭代在案：①免 JOIN 化——5M×100k JOIN 超时改点查；②ego 节点一致性——一跳边 ego 侧统一 id；③talent 榜排序——score 全 NULL 改 co_paper_count 主键）。
- 产物：`code/M_SCIUI_X_015_out.json`。正文数字与产物键逐一对应：`jiuxin_collab_rows_total=14380246`（§2.1，assert 零漂移）、`jiuxin_collab_2024_rows=2146142`/`jiuxin_collab_2024_ego_side_institutions=36026`（§2.4）、`jiuxin_2024_top_ego`（§2.5）、`jiuxin_2024_egonet_nodes=1206`/`jiuxin_2024_egonet_edges=4500`（§2.5）、`jiuxin_2024_centrality_top10_by_degree` 十行三值（§2.5）、`jiuxin_talent_collab_top8`（§2.6）、`devold_enterprise_centrality_versions` demo 版全量（§2.2）、derived 两比（§2.8）。
- 结果解读：一套完整可复放的 ego 网中心性管道（选 ego→拉边→建网→三函数→排名）+ 学者现成榜 + 开发库造数面证据链。
- 对照需求功能要求的评审：三中心性——满足（三列全算）；网络图谱——满足（G 对象即力导向数据源）；「特定领域内」——不满足（subfield 映射缺）；机构+学者混合——部分满足（两源分离，混排待裁定）。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 规模 | 合作边全表 | `jiuxin_collab_rows_total` | 14,380,246 |
| 规模 | 2024 单年 | `jiuxin_collab_2024_rows` | 2,146,142 |
| 规模 | 2024 机构侧 | `jiuxin_collab_2024_ego_side_institutions` | 36,026 |
| 造数 | 旧机 centrality 版本 | `devold_enterprise_centrality_versions` | demo_centrality_v0.1 × 114 |
| absence | gkx 网络面 | `absence_probe[1]` | 0 表 |
| ego | Top 机构 | `jiuxin_2024_top_ego` | 中科院 co_paper_sum 112,470（聚合口径） |
| ego 网 | 节点/边 | `jiuxin_2024_egonet_nodes/edges` | 1,206 / 4,500 |
| 排名 | 度 Top3 | `jiuxin_2024_centrality_top10_by_degree` | 0.4149/0.2108/0.2083 |
| 排名 | 中介 Top1 | 同上 betweenness | 0.584 |
| 学者 | 现成榜 Top | `jiuxin_talent_collab_top8` | 8,379 篇合作对 |
| 派生 | ego 度百分位 | `jiuxin_ego_degree_pct` | 41.49%（500/1,205） |
| 派生 | ego 中介百分位 | `jiuxin_ego_betweenness_pct` | 56.72% |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| N1 | 机构合作边 | jiuxin | `ads_institution_collaboration_yearly` | 14,380,246 | 直查 | **有**（主承载） |
| N2 | 学者合作对 | jiuxin | `ads_talent_collaborator` | 5,051,578 | 直查 | 有（现成 score/rank） |
| N3 | 领域过滤维 | jiuxin | `…subfield_yearly.subfield_id` | 252 subfield | 部分 | **缺映射**（≠UI 20 领域） |
| N4 | 机构中心性结果面 | dev | `ads.enterprise_centrality` | 114（demo 版）/新机 0 | **造数/空载** | 缺（禁引） |
| N5 | 通用图谱面 | dev | `graph_node`/`graph_edge`（双机） | 0/0 | **空载** | 缺 |
| N6 | 网络面 | gkx | —（280 表五关键词） | 0 表 | **不存在** | 缺（结构级） |

`support_judgment="部分支持"`，与文首一致（闸 6）。

### 3.2 N1/N2：结构数据双达标的两张边表

机构表 42 列把「合作对+强度+地理+覆盖状态+数据源版本」一次给齐，`data_sources=["openalex"]` 与 `metric_definition_version` 字段保证可追溯；学者表 15 列轻量但 rank 现成。两表合计近 2,000 万行边——全领域中心性即期可算（ego 网模式铺开），领域过滤版待 N3。

### 3.3 N3：领域维失配是降档主因

需求「特定领域内」要求网络先按领域切片。久新的领域粒度是 `subfield_id`（合作 subfield 表 23,363,790 行/252 个 subfield），而 UI 评估上下文的领域体系是「未来产业」20 领域（`futureIndustryDomainOptions`）——两套体系无对齐映射表（久新 `ads_discipline_*` 四级体系与 20 领域亦无官方对照）。缺的不是数据而是**映射**——一张 252↔20 的对照表（或经 discipline 中转）就能闭合，这正是升档触发器的内容。

### 3.4 N4-N6 的 absence_probe 全记录

否定性证据三条：**开发库（旧机）**——enterprise_centrality 114 行 model_version 全量 demo_centrality_v0.1 + 虚构企业名样本（禁引依据）；**gkx**——五关键词表扫描 0 命中 + dwd_zh_paper author_info_list longtext 非结构化；**新机**——enterprise_centrality/graph_node/graph_edge 全 0 行（探针 c 在案，脚本 facts 登记 `devnew_graph_face_rows=0`）。四缺失情形归属：N4/N5「表存在但数据无效/空载」；N6「表不存在」。

### 3.5 现场复核清单

| 复核项 | 结果 |
|---|---|
| 全表 assert | 14,380,246 == TECHTRK_018 共享值 |
| ego 网 | 1,206 节点/4,500 边（LIMIT 4,000+一跳 500） |
| 三中心性 | Top3 度 0.4149/0.2108/0.2083；中介头名 0.584 |
| betweenness | 精确算法 seed=42（B5 复跑同值） |
| 学者榜 | Top 对 8,379 篇（co_paper_count 序） |
| 造数面 | 114 行 demo 版全量登记 |
| 超时留证 | 首版 520s timeout + JOIN 超时两案在案 |

## 四、数据缺失情况

### 4.1 领域映射缺失（映射级，主因）

252 subfield 与 20 UI 领域无对照表——需求「特定领域内」的领域切片暂不可行，本件以全领域口径交付并标注。修复是一张映射表（含 discipline 四级中转）+ 一次领域内子图重算，工程量天级。

### 4.2 机构/学者混排基准未定（口径级，次因）

UI 混合榜语义下两网中心性值域不可直接比（机构网密、学者网疏）。候选基准：分表展示（最稳，UI 现行五列已按「类型」列区分）/跨网 z-score 归一合榜（激进）。本报告按分表交付，混排待裁定。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 全领域版即期交付 | 产品决策 | 本件即期 | ego 网模式铺开全库 |
| subfield↔20 领域映射表 | 数据工程 | 本件+KGANALY 族 | 252 行对照表 |
| 学者名称富化点查批 | 数据工程 | 本件 | talent_profile 逐对回填 |
| 混排归一基准裁定 | 口径裁定 | 本件 | z-score vs 分表 |

档位后果：映射表建成 → 升**完全转换支持**；仅全领域交付 → 维持部分支持（标注全领域）。

## 参考文献

1. Freeman L C. Centrality in social networks conceptual clarification[EB/OL]. https://www.sciencedirect.com/science/article/abs/pii/S0378873378900217 （度/中介中心性经典，2026-11-01 WebSearch 核验可达）
2. NetworkX centrality documentation[EB/OL]. https://networkx.org/documentation/stable/reference/algorithms/centrality.html （三中心性实现，本地 3.2.1 实测可用）
3. Sabidussi G. The centrality index of a graph[EB/OL]. https://doi.org/10.1007/BF02289527 （接近中心性定义，2026-11-01 WebSearch 核验可达）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技发展态势/科技创新评估.md》seq 137（excel_row 140）：

> 基于合作网络分析，评估特定领域内学者、研究机构在科学网络中的中心性指标，包括度中心性、接近中心性、中介中心性，用户可查看网络图谱和中心性排名，识别领域内的核心研究力量。

需求主文档 `科技信息展示系统和科技专题服务系统.md:881`（1.1.1.1.4.1.7.1.2）同文（多一「等」字）。UI 组件 `TechInnovationEvaluationPage.tsx:3488` 表头「节点/类型/度/接近/中介」为三方法名的组件化落地。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 网络中心性 | 科技创新评估.md | 2（seq 137 叶+:20 面板列举） |
| 度中心性 | 同上 | 1（seq 137 叶） |
| 中心性排名 | 同上 | 1（seq 137 叶）；主需求文档 :881 |
| 中心性 | 科技全域态势/技术发展跟踪/全球创新监测.md | 0 |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_X_015_out.json`（20261101 实跑：ego 网三中心性 Top10、学者榜、造数面证据、三条 absence）。
- Lane 2 联合探针：`_probe_lane2_s302_out.json`（dev 网络/图谱表扫描 32 表、gkx 网络面 0）、`_probe_lane2_s302b_out.json`（合作表 DESC 42 列+样本、久新 203 表）、`_probe_lane2_s302c_out.json`（旧机 enterprise_centrality 114 行样本含 demo 版本与虚构名、talent 表 DESC+5,051,578 行、2024 单年计数）、`_probe_lane2_s302f_out.json`（subfield 合作表 DESC+23,363,790 行/252 subfield）。
- 既有调查互证：`../../20261027三系统兼容升级/md_code/M_TECH_ENTITY_INFLUENCE_out.json`（IPC4 共类网 620 节点先例）。

### B.2 本件产物逐键清单

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `metric_id` | 标识 | M_SCIUI_X_015 | 文首 |
| `ui_evidence` | 证据 | 3 条组件行号 | §1.5 |
| `requirement_trace.named_in_srs` | 事实 | **true**（seq 137 / excel_row 140） | §1.1/附录 A |
| `facts.devold_enterprise_centrality_rows` | 计数 | 114 | §2.2 |
| `facts.devold_enterprise_centrality_versions` | 版本 | demo_centrality_v0.1 全量（演示造数版本号，禁引留证） | §2.2 |
| `facts.devnew_graph_face_rows` | 计数 | 0 | §3.4 |
| `facts.gkx_network_tables` | 计数 | 0 | §2.3 |
| `facts.jiuxin_collab_rows_total` | 计数 | 14,380,246（assert 对账） | §2.1 |
| `facts.jiuxin_collab_2024_rows` | 计数 | 2,146,142 | §2.4 |
| `facts.jiuxin_collab_2024_ego_side_institutions` | 计数 | 36,026 | §2.4 |
| `facts.jiuxin_2024_top_ego` | 事实 | 中科院 co_paper_sum 112,470 | §2.5 |
| `facts.jiuxin_2024_egonet_nodes/edges` | 规模 | 1,206 / 4,500 | §2.5 |
| `facts.jiuxin_2024_centrality_top10_by_degree` | 排名 | 十行三中心性 | §2.5 |
| `facts.jiuxin_talent_collab_top8` | 榜单 | 8,379 篇合作对居首 | §2.6 |
| `derived[0]` | 派生比 | jiuxin_ego_degree_pct=39.75 | §2.8 |
| `derived[1]` | 派生比 | jiuxin_ego_betweenness_pct=56.72 | §2.8 |
| `absence_probe` | 负证据 | 3 条（dev 造数/gkx 0 表/jiuxin 领域注记） | §3.4 |
| `support_judgment` | 判档 | 部分支持 | §〇 |

### B.3 共享探针复用

`jiuxin_collab_rows_total=14,380,246` 与 TECHTRK_018 件 `jiuxin_collaboration_yearly_rows` 同值（批内互推零漂移，脚本 assert 强制）；`jiuxin_talent_collaborator` 5,051,578 行为首登（本 Lane 探针 c）。subfield 表 23,363,790 行/252 为领域维证据（本 Lane 探针 f）。

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 边定义 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| Freeman 三中心性 | R1/R3 | 合作对 | 久新边表现成 | **最高（需求指定）** |
| PageRank | 既有 IPC4 网先例 | 共类/引用 | 先例在案（另域） | 中 |
| 强度加权榜 | SciVal 族 | 边权=合著数 | co_paper_count 直查 | 高（快通道） |

### C.2 数据矩阵

| 依赖 | 行数/状态 | 覆盖/质量 | 缺口 |
|---|---|---|---|
| 机构合作边 | 14,380,246 | 2015-2026 年度+地理+强度 | 领域维只到 subfield |
| 学者合作对 | 5,051,578 | rank 现成 | score NULL/名称待点查 |
| dev centrality | 114（demo）/0 | 造数面 | 禁引 |
| gkx 网络面 | 0 表 | — | author_info_list 非结构化 |
| subfield 映射 | 252↔20 无对照 | — | 映射表 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | 全领域 ego 网中心性榜（机构）+学者现成榜 | 无（本件管道铺开） |
| v2 | subfield↔20 领域映射→领域内子图 | 映射表 |
| v3 | 混排归一基准+学者名称富化 | 口径裁定 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| dev 造数面被误采信 | **高** | absence 留证+版本字段核查入探针 SOP |
| 全领域口径被当领域口径交付 | 高 | UI 标注「全领域」 |
| ego 网截断（LIMIT 4000）代表性 | 中 | 随行披露网规模与截断参数 |
| 混排值域不可比 | 中 | 分表展示为默认 |

### C.5 总判

**部分支持**：网络本体结构数据双达标（1,438 万边），三中心性方法零障碍且已实算验证；领域映射缺失与混排基准未定是两个待闭合项。升档前置：映射表建成即升完全转换支持。

## 附录 D　复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_X_015.py` | 退出码 0，落 `_out.json` |
| 数据入口 | Doris 直连 + `_gkxdb.py` + pymysql 双机 | demo_* raise |
| 全表 assert | 14,380,246 | 零漂移 |
| 确定性 | betweenness seed=42 复跑 | 同值 |
| 判档一致 | `support_judgment` vs 文首 | 部分支持 |
| 负证据探针 | 产物 absence_probe 3 条 | 三源留证 |
| networkx | 3.2.1（探针 d 登记） | 本地可用 |
