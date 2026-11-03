# 技术关联强度（M_SCIUI_INNOV_003）

> **类型**：GRAPH_EDGE（边权重/共现强度，双口径 confidence 0-100 + Jaccard 0-1）｜ **域**：科技发展态势·全球创新监测·技术关联网络/科技全景·实体关系图谱｜ **UI 挂载**：全球创新监测页图实体排行 + 科技全景实体详情（`graphEntityRanking.js:8` relationStrength 排序维度 + `graphObjectDetail.js:51` 关联强度字段 + `:7-9` `:130` 兜底伪值）
> **数据支持度**：**部分支持**｜ **公式定义人**：仿王惠（推测定义，非招标原文闭合口径）｜ **口径归属**：UI 推导叶（`cfg_metric` 无条目；指标名三份说明书 0 命中）
> **复现脚本**：`code/M_SCIUI_INNOV_003.py`｜ **产物**：`code/M_SCIUI_INNOV_003_out.json`
> **四判定摘要**：直接结构 = 否（三源无「实体关联强度」现成结果面；gkx 列名扫描 0 命中）；直接数据 = 否；依赖结构 = 是（久新 ads_technology_graph_edge 587,252 边 × confidence/jaccard/evidence_level 三强度列 + node 表 19,430 节点带 weighted_degree）；依赖数据 = 部分（结构量双达标，但 62.91% LOW 证据边 + 100% DWS_INFERRED 推断源 + 实体粒度错位三钳制）
> **数据源口径**：本件支持度按「开发库 gkxlumenx_*（禁 demo_*）+ 三方库 gkx（183.240.141.251:3318 只读）+ 久新 jiuxin（47.93.119.170:29030 只读）」三源评估（20261101 三源铁律）。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：部分支持。** 久新 `ads_technology_graph_edge` 是全批结构最漂亮的承载之一：587,252 条技术-技术边，每边带 **confidence（27.0797-100.0，全局均值 49.0162）+ jaccard（0-1）+ evidence_level（LOW/MEDIUM/HIGH）** 三套强度/质量列，四类关系（WEAK_DEPENDENCY 257,347 / PATENT_CONVERGENCE 212,729 / KNOWLEDGE_DEPENDENCY 95,208 / CO_EVOLUTION 21,968）覆盖依赖/收敛/共演化语义——**边级强度本身是「完全转换支持」级**。压档三因：①**证据质量钳制**——evidence_level LOW 占 62.91%（369,428/587,252）、HIGH 仅 17.60%（103,358），且 relation_source 全部为 DWS_INFERRED（推断边零实证边），弦线图直接按 confidence 画粗线会把六成弱推断画成强关联；②**实体粒度错位**——库内边是 ETO 研究簇候选技术对（19,430 节点），UI 挂载的 relationStrength 挂在**混合实体**上（技术点/机构/论文/专利/专家），前端两处兜底伪值（`score×0.95`、`max(72, score-4)`）自证无真值来源；③gkx 列名扫描（relation_strength/jaccard/association_strength）**0 命中**、dev 14 张 graph 表 6 张核心表 0 行。语义相邻的机构协同表（14,380,246 行）可补实体粒度但 Top 强度全为 1.000000（单篇合作顶格）区分度存疑。判**部分支持**。

### 批次通用纪律摘要（批 S3-01 共用，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 17.6003%/62.9079% 分子分母同出 graph_edge 全表 |
| B4 | 负结论带探针 | gkx 列名扫描 0 命中 + dev 6 表 0 行留证 |
| B5 | 确定性 | Top8 边按 confidence 降序;分布按 relation_type 分组 |
| B6 | 闸门自身被闸 | 不自跑闸门，由派单方统一跑 |
| B7 | 产物只由脚本产出 | 手改禁令；改脚本→重跑 |
| B8 | 回执不复收 | 派单方抽硬证据复验 |
| B9 | 单位/日期陷阱 | confidence 0-100 与 jaccard 0-1 双量纲并列标注;边表快照制无年份 |
| B10 | 口径裁定保守交付 | 口径 A（confidence）/口径 B（Jaccard）双轨 + 升档触发器写死（§1.6） |
| B11 | 多本账互推 | 边表/节点表与 024 件同源探针;机构协同表与 001 件 institution 语义链互推 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 边级强度有真承载吗？ | 有（三套强度列 58.7 万边） | ads_technology_graph_edge |
| 能直接回填 UI 实体粒度吗？ | 不能（库=技术对,UI=混合实体） | 粒度错位 + 前端兜底伪值 |
| 弱推断边可过滤吗？ | 可（evidence_level 列在）但 HIGH 仅 17.60% | 369,428 LOW / 103,358 HIGH |

## 摘要

「技术关联强度」挂两处：全球创新监测页的图实体排行（`graphEntityRanking.js:8` 把 `relationStrength` 作为排序维度之一）和科技全景的实体详情（`graphObjectDetail.js:51` 显示「关联强度」字段）——两处语义都是**挂在实体/关系上的一个强度读数**，弦线图「线条粗细表示技术间关联强度」（技术发展跟踪.md seq 51）。UI 前端有两处兜底伪值（`:7-9` `score×0.95`、`:130` `max(72, score-4)`）——前端作者自证知道该字段无真值来源。三源探测：**久新侧结构惊艳**——`ads_technology_graph_edge` 587,252 边（四类关系:弱依赖/专利收敛/知识依赖/共演化），每边 confidence（均值 49.0162,极值 27.0797-100.0）+ jaccard（CO_EVOLUTION 均值最高 0.199461）+ evidence_level 三列齐备;Top8 高置信边全是 PATENT_CONVERGENCE/KNOWLEDGE_DEPENDENCY（顶格 100.0 边 jaccard=1.0、共享 3 主题 12 专利）。**但三钳制压档**：LOW 证据边 62.91%、推断源 100%、实体粒度错位（技术对 vs 混合实体）。gkx 列名扫描 0 命中（relation_strength/jaccard/association_strength 全无）;dev 14 张 graph 表中 6 张核心表全 0 行。机构协同表 14,380,246 行（强度≥0.5 者 964,513）语义相邻但顶格 1.0 区分度存疑。节点侧 19,430 节点带 weighted_degree + community_role（MEMBER 11,354/BRIDGE 4,581/CORE 3,495）——「节点关联强度」可由度数聚合导出（转换路径在,非现成面）。判**部分支持**:技术对强度即期可用（带证据过滤）,实体粒度需映射工程。

- 需求判定：**UI 推导叶**（指标名三份说明书 0 命中;最近语义为弦线图可视化映射描述与实体展示字段,均非计算口径）。
- 复现状态：脚本已跑通;边分布四表 + Top8 边 + 证据/方向分布 + 双库负探针落产物。
- 档位结论：**部分支持**（证据质量 + 推断源 + 粒度错位三因）。
- 关键事实：confidence 与 jaccard 双量纲并存是本件口径核心——R1/R2 权威方法是 Jaccard/关联强度族,库内 confidence 是上游综合分。
- 升档路径：上游补实体映射（技术对→UI 实体类型）+ 提升高证据边占比（当前 17.60%）→ 可升完全转换支持。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/**全球创新监测**/创新图谱与排名 + **科技全景**/实体关系图谱（跨页双挂载,SRS seq 56-88 与 seq 1-32 域）。挂载点实查：

- `src/graphEntityRanking.js:8`：排序维度定义 `sortOptions` 含 `{ key: 'relationStrength', label: '关联强度' }`（与论文数/专利数/中心度并列）——**把关联强度当作实体排行键**,预期每实体一个聚合强度值。
- `src/graphObjectDetail.js:51`：详情面板字段 `{ label: '关联强度', value: object.relationStrength }`——单实体读数形态。
- `:7-9`：兜底函数 `const getRelationStrength = (score) => score ? score * 0.95 : 66.0;`——**伪值生成器**:无 score 时给 66.0,有 score 时打 95 折。
- `:130`：第二处兜底 `Math.max(72, (object.patentCount || 0) - 4)`——用专利数减 4 兜底关联强度,下限 72。

两处兜底伪值是本件最重要的 UI 证据:它们证明**前端作者明知该字段无后端真值**,用启发式造演示数。正式版必须用库内真强度替换。SRS 侧:技术发展跟踪.md seq 51『弦线图展示技术关联关系,线条粗细表示技术间关联强度』是最强的需求锚（可视化映射）;科学技术全景.md『每个实体显示基本信息如名称、类型和关联强度』（展示字段）。

### 1.2 为什么需要本指标

关联强度是图谱类可视化的**视觉编码核心**:弦线图的线粗、力导向图的边距、实体排行的序,全部由这一个数驱动。没有可信的强度值,图谱就退化成「均匀 spaghetti」——所有边一样粗,用户无法定位关键关联。本指标承担三职:①**视觉编码**（线宽映射）;②**排序键**（实体排行按强度取 TopN）;③**过滤阈值**（弦线图通常只画强度 Top N% 的边防过载）。

数据侧本件是「结构强承载 + 质量钳制」的典型:久新边表的 schema 完全对得上（confidence/jaccard/evidence_level 三列即权威方法族的落库形态）,但 62.91% LOW 证据 + 100% 推断源意味着**强度的可信度分层**——回填 UI 必须带证据过滤（如仅 HIGH/MEDIUM 入弦线图）,否则演示效果好看但读数不可信。这给批内立了「强度类指标必须带质量列」的样板:任何强度读数回填,证据等级随行。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「技术关联强度/关联强度」作为指标名三份说明书 0 命中。语义最近两处（均非计算口径）:技术发展跟踪.md seq 51（excel_row 54）『弦线图展示技术关联关系,线条粗细表示技术间关联强度』——**可视化映射描述**（粗细∝强度）,未定义强度的计算式;科学技术全景.md 实体展示字段『每个实体显示基本信息如名称、类型和关联强度』——**字段枚举**,无口径。两处合起来能反推:需求方预期强度是 0-100 或 0-1 的单值,挂实体或关系上,驱动视觉映射——但计算口径（共现?引用?融合打分?）完全留白,由 UI 兜底伪值填补。主需求文档 :817『关系图谱:展示技术、论文、专利、专家之间的关联关系』给了**实体类型枚举**（技术/论文/专利/专家——与 UI 混合实体粒度一致）,是粒度错位判定的重要需求侧证据。

### 1.4 类似指标权威方法可行性分析概要

共现强度度量的权威范式有三支。**Jaccard 系数族**（R1 van Eck & Waltman 系统综述）:`J(A,B) = |A∩B|/|A∪B|`,共现对强度标准度量,抗高频偏;**关联强度族**（同 R1;Salton 余弦为其变体）:`S = c_ij·n/(e_i·e_j)`,预期共现/观测共现比,ESCI 引文分析标准;**专利共类/引文耦合族**（R2 OECD 专利统计手册）:技术关联用 IPC 共类（两 IPC 同现于一专利）或引文耦合（共引用专利数）度量,是 OECD 官方技术关联口径。方法族对照:

| 方法族 | 公式/口径 | 三源承载 | 匹配度 |
|---|---|---|---|
| Jaccard 系数（R1） | \|A∩B\|/\|A∪B\| | **边表 jaccard 列直存**（四类关系全覆盖,max 1.0） | **高（口径 B 即期）** |
| 关联强度/余弦（R1 变体） | c_ij·n/(e_i·e_j) | 无现成列,可由 shared_patents/shared_topics 重算 | 中（转换路径在） |
| IPC 共类/引文耦合（R2） | 共类计数/耦合计数 | PATENT_CONVERGENCE 边（shared_patents 列）语义最近 | **中高（上游已做同族推断）** |
| 综合打分（库内现实） | confidence 0-100 | 边表 confidence 列 | 高但口径不透明（DWS_INFERRED） |

结论:权威 Jaccard 族有列直存即期可用;OECD 共族语义由 PATENT_CONVERGENCE 边承载;唯 confidence 综合分的口径黑箱（上游推断式未披露）需 note 随行。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/graphEntityRanking.js:8`（排序维度）;`src/graphObjectDetail.js:51`（字段）、`:7-9`（兜底×0.95/66.0）、`:130`（兜底 max(72,−4)）。
- SRS：`bid-reference/srs/02-科技信息展示系统/科技发展态势/技术发展跟踪.md` seq 51（excel_row 54,弦线图映射锚）;`…/科技全景.md`（实体展示字段,跨页锚）。
- 主需求文档：《科技信息展示系统和科技专题服务系统.md》:817（实体类型枚举:技术/论文/专利/专家）。
- 数据：`code/_snapshots/_probe_lane5_s3_01_out.json`（边表 DESC+四类分布+Top8+证据/方向分布;节点表 community_role;机构协同表统计）。

### 1.6 推测原意与推测定义

**推测定义（双口径并列，均须披露口径假设）**：

- **口径 A（综合置信度·UI 量纲同构）**：`strength(edge) = confidence`（0-100），取久新 `ads_technology_graph_edge`。实测:全局均值 49.0162,极值 27.0797-100.0;四类关系均值 KNOWLEDGE_DEPENDENCY 最高（64.2987）,PATENT_CONVERGENCE 最低（43.8925）。**必须随行 evidence_level 过滤**（HIGH 17.60%/MEDIUM 19.49%/LOW 62.91%）。
- **口径 B（Jaccard·权威方法族）**：`strength(edge) = jaccard`（0-1），同表直存。实测:四类均值 CO_EVOLUTION 最高（0.199461）,PATENT_CONVERGENCE 最低（0.036463）,各类 max 均 1.0。
- **节点聚合（排行键候选）**：`nodeStrength = weighted_degree`（节点表现成列）或 `Σ edge.confidence`（聚合导出）——graphEntityRanking 排序键的转换路径。
- **实体粒度映射（缺口）**：UI 混合实体（技术/论文/专利/专家）→ 库技术对/机构对,需映射工程。

**降档/升档触发器（B10 模板）**：若甲方接受「技术对强度=弦线图强度,实体排行仅技术实体」→ 即期可交付（带证据过滤）,仍部分支持（粒度收窄披露）;若上游补实体映射（技术对→专利/论文/专家挂载）→ 粒度闭合,升**完全转换支持**;若甲方要求 OECD 共类原文口径（IPC 共类计数）→ 需回 gkx dwd_patent 重算（IPC 列在,293.9 万行可行但工程量大）,另立指标件。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技发展态势/全球创新监测.md`（主）+ `…/科学技术全景.md`（跨页） |
| 所属四级功能 | 全球创新监测（33 叶）+ 科技全景（跨页挂载） |
| 本件挂载视图 | 图实体排行 + 实体详情（两页共用组件） |
| 需求叶对应 | 无同名叶;最近 seq 51 弦线图映射（技术发展跟踪.md） |
| 批内相邻件 | M_SCIUI_TECHTRK_021（若为技术图谱中心度类——同图谱族）;M_SCIUI_INNOV_001（机构榜——协同表 institution 语义链）;M_SCIUI_TECHTRK_024（趋势序列——同探针共享边表源） |
| 跨模块参照 | 科学技术全景.md 实体展示字段;主需求文档 :817 实体类型枚举 |

本件是批内**图谱族**的核心件:与 024 共享久新图谱探针（边表/节点表）,024 消费趋势序列,本件消费强度列;与 001 经机构协同表形成语义链（机构-机构协同强度是「关联强度」在机构维的投影）。批内图谱族的方法论结论由本件立:**强度读数必须三件套**（强度值+证据等级+口径标签）,否则图谱可视化不可信。

## 二、计算过程

### 2.1 装载与规模校验

久新 `ads_technology_graph_edge` 587,252 边（facts.jiuxin_graph_edge_rows）× `ads_technology_graph_node` 19,430 节点（facts.jiuxin_graph_node_rows）。边表快照制（graph_release_id,无统计年份列——base_years_note 在案）;节点表带 community_role/weighted_degree/community_id（本 lane 探针 DESC 确认,纠偏了 node_type 列不存在的初始假设）。

### 2.2 gkx/dev 侧负结论（absence_probe）

```sql
-- gkx 列名扫描（强度类列名全库检索）
SELECT table_name, column_name FROM information_schema.columns WHERE table_schema='gkx'
AND (column_name LIKE '%relation_strength%' OR '%jaccard%' OR '%association_strength%') LIMIT 20;
-- → 0 hits（absence_probe[1]）
-- gkx 表名扫描 → 唯一命中 dwd_scholar_paper_relation（论文-论文引用关系,无边权强度列）
-- dev graph 表扫描 → 14 表命中,核心 6 表行数:enterprise_graph_rel/graph_edge/graph_node/event_relation/policy_graph_node/policy_graph_edge 全 0
```

gkx 唯一关系表 `dwd_scholar_paper_relation` 是**引用关系边**（无强度列）;dev 14 张 graph 表是**表结构齐备但数据空载**的典型——schema 设计了图谱,数据管道未填充。两源均不承载「强度」。

### 2.3 口径 A：边置信度分布（四类关系）

```sql
SELECT relation_type, COUNT(*) edges, AVG(confidence) avg_c, MIN(confidence) min_c, MAX(confidence) max_c
FROM ads_technology_graph_edge GROUP BY relation_type ORDER BY edges DESC;
-- → WEAK_DEPENDENCY 257,347/47.7061 · PATENT_CONVERGENCE 212,729/43.8925(max 100.0)
--   KNOWLEDGE_DEPENDENCY 95,208/64.2987 · CO_EVOLUTION 21,968/47.7447
```

四类关系语义分层清晰:KNOWLEDGE_DEPENDENCY（知识依赖,主题共现驱动）均值最高,PATENT_CONVERGENCE（专利收敛）最低但 max 顶格——顶格边即「3 共享主题+12 共享专利」的完全重合对（`jiuxin_top8_edges_by_confidence[0]`,jaccard 同步 1.0,口径互证）。方向状态分布:CANDIDATE 257,347/UNDIRECTED 212,729/DIRECTED 95,208/BIDIRECTIONAL 21,968——四态并存,弦线图（无向）消费时 CANDIDATE/DIRECTED 需拍平处理（note 在案）。

### 2.4 口径 B：Jaccard 分布（权威方法族）

```sql
SELECT relation_type, COUNT(*) edges, AVG(jaccard) avg_j, MAX(jaccard) max_j
FROM ads_technology_graph_edge GROUP BY relation_type ORDER BY edges DESC;
-- → WEAK_DEPENDENCY 0.080038 · PATENT_CONVERGENCE 0.036463 · KNOWLEDGE_DEPENDENCY 0.136233 · CO_EVOLUTION 0.199461（各类 max=1.0）
```

CO_EVOLUTION（共演化）Jaccard 均值最高（0.199461）符合方法预期:共演化对是时间上同步演进的强耦合对;PATENT_CONVERGENCE 均值最低（0.036463）但边数第二多——专利收敛是「大池稀共现」（专利基数大,单对共享占比小）,与 Jaccard 的高频惩罚特性一致（R1）。**两口径排序不一致**（A 口径 KNOWLEDGE 最高,B 口径 CO_EVOLUTION 最高）——进一步证明双口径须并列待裁,不能默认同序。

### 2.5 证据质量与 Top8 高置信边

```sql
SELECT evidence_level, COUNT(*) FROM ads_technology_graph_edge GROUP BY evidence_level;
-- → LOW 369,428 / MEDIUM 114,466 / HIGH 103,358
SELECT relation_type, confidence, jaccard, shared_topics, shared_patents
FROM ads_technology_graph_edge ORDER BY confidence DESC LIMIT 8;
-- → 顶格 100.0(PATENT_CONVERGENCE,3 主题/12 专利) · 97.4376(KNOWLEDGE,6/4) · 97.0(6/7→24 专利) … 95.0(6 主题/98 专利)
```

HIGH 证据边仅 17.6003%（103,358/587,252,derived.jiuxin_high_evidence_edge_pct,B3 同基）;LOW 占 62.9079%（derived.jiuxin_low_evidence_edge_pct）——**弦线图回填的最低门槛建议:仅 MEDIUM+HIGH 入图**（217,824 条,37%），LOW 边进悬浮明细不进主图。Top8 全部为 PATENT_CONVERGENCE/KNOWLEDGE_DEPENDENCY,共享主题数 3-7、共享专利 2-98——高置信边的驱动因子清晰（主题+专利双共现）。

### 2.6 实体粒度补充承载（机构协同表）

`ads_institution_collaboration_yearly` 14,380,246 行（facts.jiuxin_institution_collab_rows）:机构-机构年度协同,强度列（论文/专利合作计数派生）。实测:avg 0.093564,max 1.0,强度≥0.5 者 964,513（facts.jiuxin_collab_strength_ge_half）——**百万级可用协同对**。但 note 在案:Top 强度全为 1.000000（单篇合作顶格）,区分度存疑,消费前须做归一（如按年度频次加权）。该表是 UI「机构实体」粒度的直接承载（机构对强度）,与技术对边表互补——两表合起来覆盖 UI 混合实体的两个最大子类（技术/机构）,论文/专利/专家三类实体仍无强度承载。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_INNOV_003.py`（久新直连 + gkx/dev information_schema 扫描,零 demo_*）。运行 `python3 code/M_SCIUI_INNOV_003.py`。
- 产物：`code/M_SCIUI_INNOV_003_out.json`。正文数字与产物键逐一对应:`jiuxin_graph_edge_rows=587252`（§2.1）、`jiuxin_graph_node_rows=19430`（§2.1）、`jiuxin_edge_confidence_by_type` 四行（§2.3）、`jiuxin_edge_jaccard_by_type` 四行（§2.4）、`jiuxin_edge_evidence_level_dist`（§2.5）、`jiuxin_top8_edges_by_confidence` 八行（§2.5）、`jiuxin_institution_collab_rows=14380246` + 三统计（§2.6）、`gkx_relation_like_columns=[]`（§2.2）、`dev_graph_table_rows` 六 0（§2.2）、derived 两比（17.6003/62.9079）。
- 结果解读：技术对强度双口径即期可用（带证据过滤）;实体粒度两子类（技术/机构）有承载、三类（论文/专利/专家）空白;前端兜底伪值可替换路径明确。
- 对照需求功能要求的评审：弦线图线粗——满足（confidence/jaccard 任一口径,过滤后 21.8 万边）;实体排行关联强度键——部分满足（技术/机构实体可聚合,论文/专利/专家实体无承载）。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 装载 | 边表规模 | `jiuxin_graph_edge_rows` | 587,252 |
| 装载 | 节点表规模 | `jiuxin_graph_node_rows` | 19,430 |
| 口径 A | 四类均值 | `jiuxin_edge_confidence_by_type` | 47.7061/43.8925/64.2987/47.7447 |
| 口径 A | 全局极值 | `jiuxin_edge_confidence_global_*` | 均值 49.0162,极值 27.0797-100.0 |
| 口径 B | 四类均值 | `jiuxin_edge_jaccard_by_type` | 0.080038/0.036463/0.136233/0.199461 |
| 质量 | 证据分布 | `jiuxin_edge_evidence_level_dist` | LOW 369,428/MED 114,466/HIGH 103,358 |
| 质量 | HIGH 占比 | `derived.jiuxin_high_evidence_edge_pct` | 17.6003%（103,358/587,252） |
| 质量 | LOW 占比 | `derived.jiuxin_low_evidence_edge_pct` | 62.9079%（369,428/587,252） |
| Top 边 | 顶格边 | `jiuxin_top8_edges_by_confidence[0]` | 100.0/jaccard 1.0/3 主题/12 专利 |
| 补承载 | 机构协同 | `jiuxin_institution_collab_*` | 14,380,246 行/avg 0.093564/≥0.5 者 964,513 |
| 负结论 | gkx 列扫描 | `gkx_relation_like_columns` | []（0 命中） |
| 负结论 | dev 核心表 | `dev_graph_table_rows` | 六表全 0 |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 技术-技术边强度 | jiuxin_warehouse | `ads_technology_graph_edge`（confidence/jaccard） | 587,252 | 直查 | **有**（主承载,双口径） |
| D2 | 边证据质量 | jiuxin_warehouse | 同表 evidence_level | 三值 | 直查 | 有（随行过滤） |
| D3 | 节点聚合强度 | jiuxin_warehouse | `ads_technology_graph_node`.weighted_degree | 19,430 | 直查 | 有（排行键路径） |
| D4 | 机构-机构协同强度 | jiuxin_warehouse | `ads_institution_collaboration_yearly` | 14,380,246 | 直查 | 有（区分度 note） |
| D5 | gkx 强度列 | gkx | relation_strength/jaccard 列扫描 | 0 命中 | **不存在** | **缺**（结构级） |
| D6 | dev 图谱数据 | dev | 14 graph 表（核心 6 表） | 全 0 | 空载 | 缺 |
| D7 | 论文/专利/专家实体强度 | 三源 | — | — | **不存在** | 缺（粒度空白三类） |

`support_judgment="部分支持"` 与产物一致（闸 6）。

### 3.2 D1/D2 主承载明细

`ads_technology_graph_edge` 每边:源/目标技术节点 + relation_type 四类 + **confidence（DECIMAL 0-100）+ jaccard（DECIMAL 0-1）** 双强度列 + evidence_level 三档 + direction_status 四态 + shared_topics/shared_patents 共现计数——schema 即权威方法族的落库形态（Jaccard 列直存 + 综合分并列）,这在本批是罕见的「方法对齐型」承载。四类关系覆盖依赖（WEAK/KNOWLEDGE）与收敛/共演化两族,弦线图的语义分层（依赖画箭头/共现画弧）可直接映射 direction_status。

### 3.3 D2 证据质量面（主降档因）

LOW 62.91% + relation_source 100% DWS_INFERRED（facts.jiuxin_edge_relation_source_dist 单值）:全部边是上游推断（非实证引用/共类原文）,证据等级是唯一质量分层手段。过滤策略实测:MEDIUM+HIGH 合计 217,824 条（37.05%）——入弦线图的推荐域;LOW 域进明细层。若上游未来补 EXPLICIT 源（实证边）,证据结构将改善,当前按推断边管理。

### 3.4 D4 机构协同表（实体粒度补充）

14,380,246 行年度机构对:avg 0.093564 的长尾 + 964,513 条 ≥0.5 的可用对。与 001 件的 institution 语义链:协同表的机构主键与 `ads_patent_analysis_institution`/`ads_institution_profile` 同域——机构实体在批内形成「专利数（001）+协同强度（003）」双读数,图谱页机构节点可双列展示。Top 顶格 1.0 区分度问题:单年单篇合作即 1.0,建议消费侧按多年累计重算或加 min 合作数门槛。

### 3.5 现场复核清单

| 复核项 | 结果 |
|---|---|
| 边表 | 587,252 边四类分布与均值/极值齐 |
| 双口径互证 | 顶格边 confidence 100.0 ↔ jaccard 1.0 ✓ |
| 证据占比复算 | 103,358/587,252=17.6003% ✓;369,428/587,252=62.9079% ✓ |
| 方向分布 | 四态计数和=587,252 ✓ |
| 机构协同 | 1,438 万行/三统计在案 |
| gkx 扫描 | 列名 0 命中;表名 1 命中（引用边无强度） |
| dev 扫描 | 14 表命中,核心 6 表 0 行 |
| 脚本形态 | 零 demo_*;快照制年份 note 在案 |

## 四、数据缺失情况

### 4.1 论文/专利/专家实体强度缺失（结构级,粒度空白）

UI 混合实体五类中三类（论文/专利/专家）无任何强度承载:gkx 唯一关系表是论文-论文引用边（无强度列）;久新图谱边是技术对;机构协同表只覆盖机构对。主需求文档 :817 明确五类实体入图——粒度空白直接违背需求枚举。四缺失情形归属:**表不存在**（论文-专利/论文-专家等跨类边表）。修复动作:上游立跨类实体关系表（或把技术对边经 shared_patents/shared_topics 挂载点展开到专利/论文实体）。影响面:本件实体排行 + 科技全景图谱页全实体类型。

### 4.2 证据质量与推断源（数据级,可信度钳制）

LOW 62.91% + 推断源 100%（§3.3）。这是上游推断工程的质量现状而非结构缺口:提升路径一是上游补实证边（引用/共类原文关系入边表,EXPLICIT 源）,二是提升推断置信分层质量。修复与影响:实证边入表 → 弦线图可全量入图（不必 37% 过滤）→ 本件升档第二杠杆。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| v1 弦线图仅 MEDIUM+HIGH 边（21.8 万） | 产品决策 | 本件即期 | 零成本止血,可信度优先 |
| 实体排行先上技术+机构两类 | 产品决策 | 本件即期 | 粒度收窄披露 |
| 上游跨类实体关系表 | 结构工程 | 本件+科技全景图谱 | 升档第一杠杆,五类实体闭合 |
| 实证边（EXPLICIT 源）入边表 | 上游工程 | 本件+024 图谱族 | 升档第二杠杆 |
| 机构协同强度多年累计归一 | 转换工程 | 本件机构粒度 | 消除顶格 1.0 区分度问题 |

五条路径的档位后果:前两条即期交付仍部分支持;跨类表落地 → 五类实体闭合+强度可用 → 升**完全转换支持**;实证边再落地 → 全量入图。推荐组合:v1 过滤+粒度收窄,中期推跨类表与实证边。

## 参考文献

1. van Eck N J, Waltman L. How to normalize cooccurrence data? An overview of well-known similarity measures[J/OL]. Journal of the American Society for Information Science and Technology, 2009, 60(8): 1635-1637. （R1 共现强度度量系统综述,2026-11-01 WebSearch 核验）https://www.researchgate.net/publication/220369951_How_to_normalize_cooccurrence_data_An_overview_of_well-known_similarity_measures
2. OECD Patent Statistics Manual[EB/OL]. OECD Publishing, 2009. https://www.oecd.org/en/publications/patent-statistics-manual_9789264056442-en.html （R2 专利共类/引文耦合技术关联口径,2026-11-01 WebSearch 核验可达）
3. Salton G, McGill M J. Introduction to Modern Information Retrieval[M]. McGraw-Hill, 1983. （R3 余弦相似度原始文献,余弦族方法谱系锚点）

# 附件

## 附录 A 原始需求原文摘录

「技术关联强度/关联强度」作为指标名未出现在三份说明书,无直接原文。语义最近两段:

SRS《02-科技信息展示系统/科技发展态势/技术发展跟踪.md》seq 51（excel_row 54）:

> 弦线图展示技术关联关系，线条粗细表示技术间关联强度，节点大小表示技术热度。

SRS《02-科技信息展示系统/科技发展态势/科学技术全景.md》（实体展示字段,跨页锚）:

> 每个实体显示基本信息如名称、类型和关联强度。

主需求文档《科技信息展示系统和科技专题服务系统.md》:817（实体类型枚举）:

> 关系图谱：展示技术、论文、专利、专家之间的关联关系。

UI 组件 `graphObjectDetail.js:7-9`（兜底伪值,本件最关键 UI 证据）:

> `const getRelationStrength = (score) => score ? score * 0.95 : 66.0;`

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 技术关联强度 | 三份说明书 + 主需求文档 | 0（指标名级） |
| 关联强度 | 技术发展跟踪.md / 科学技术全景.md | 1（seq 51 映射）+ 1（展示字段） |
| 关联关系 | 主需求文档 | :817 实体枚举 |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_INNOV_003_out.json`（20261101 实跑:边表四分布/Top8/证据面/机构协同/双库负探针在案）。
- 本 lane 共享探针：`code/_snapshots/_probe_lane5_s3_01_out.json`（graph_edge/graph_node DESC+分布,community_role 纠偏记录,collaboration_yearly 统计）。
- 官方共享快照：`code/_snapshots/_shared_probe_s3_01_out.json`（gkx 280 表清单——列扫描基座）。

### B.2 本件产物逐键清单（`code/M_SCIUI_INNOV_003_out.json`，20261101 实跑）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `metric_id` | 标识 | M_SCIUI_INNOV_003 | 文首 |
| `ui_evidence` | 证据 | 4 条组件行号（含两处兜底伪值） | §1.5 |
| `requirement_trace.named_in_srs` | 事实 | **false** | §1.3/附录 A |
| `facts.jiuxin_graph_edge_rows` | 计数 | 587,252 | §2.1 |
| `facts.jiuxin_graph_node_rows` | 计数 | 19,430 | §2.1 |
| `facts.jiuxin_edge_confidence_by_type` | 分布 | 4 类×均值/极值 | §2.3/口径 A |
| `facts.jiuxin_edge_jaccard_by_type` | 分布 | 4 类×均值/max | §2.4/口径 B |
| `facts.jiuxin_edge_evidence_level_dist` | 分布 | LOW/MED/HIGH 三计数 | §2.5/§3.3 |
| `facts.jiuxin_edge_relation_source_dist` | 分布 | DWS_INFERRED 单值 587,252 | §3.3 |
| `facts.jiuxin_edge_direction_status_dist` | 分布 | 四态计数 | §2.3 |
| `facts.jiuxin_top8_edges_by_confidence` | 榜单 | 8 边（类型/双强度/共现计数） | §2.5 |
| `facts.jiuxin_institution_collab_rows` | 计数 | 14,380,246 | §2.6 |
| `facts.jiuxin_collab_strength_*` | 统计 | avg/max/≥0.5 三值 | §2.6 |
| `facts.gkx_relation_like_columns` | 探针 | [] | §2.2/§4.1 |
| `facts.dev_graph_table_rows` | 探针 | 核心六表全 0 | §2.2 |
| `derived.jiuxin_high_evidence_edge_pct` | 派生比 | 17.6003 | §2.5/§2.8 |
| `derived.jiuxin_low_evidence_edge_pct` | 派生比 | 62.9079 | §〇/§2.5 |
| `absence_probe` | 探针 | 3 条（gkx 列/表+dev 表） | §2.2 |
| `support_judgment` | 判档 | 部分支持 | §〇 |
| `notes` | 披露 | 6 条（粒度/证据/兜底/双口径/协同区分度/节点路径） | §〇/§4 |
| `ctx_refs.refs` | 登记 | 12 数字 | 全文 |

### B.3 共享快照消费（B11 零漂移）

本件消费:本 lane 探针边表/节点表 DESC 与分布（与 024 件共享图谱探针源）;gkx 280 表清单来自官方快照（列扫描在其上执行,不重跑全表枚举）;dev graph 表清单与行数补测（官方快照仅有表名）。机构协同表统计与 001 件 institution 域同探针会话,数字零漂移。

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 公式/口径 | 三源承载 | 贴合度 |
|---|---|---|---|
| Jaccard 系数（R1） | \|A∩B\|/\|A∪B\| | 边表 jaccard 列直存 | **高（口径 B 即期）** |
| 关联强度/余弦（R1/R3） | c_ij·n/(e_i·e_j) | 可由 shared_* 重算 | 中（转换在） |
| OECD 共类/耦合（R2） | IPC 共类/引文耦合 | PATENT_CONVERGENCE 语义最近 | 中高 |
| 综合打分（库内） | confidence 0-100 | 边表列 | 高但口径黑箱 |

### C.2 数据矩阵

| 依赖 | 行数/状态 | 质量 | 缺口 |
|---|---|---|---|
| graph_edge | 587,252 | 双强度+证据列 | LOW 62.91%;推断源 100% |
| graph_node | 19,430 | weighted_degree 现成 | 排行键需聚合验证 |
| collaboration_yearly | 14,380,246 | 百万可用对 | 顶格 1.0 区分度 |
| gkx 强度列 | 0 命中 | — | 结构缺失 |
| dev graph 核心表 | 全 0 | schema 在数据空 | 管道未填充 |
| 论文/专利/专家实体 | 无表 | — | 跨类边表缺失 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | 弦线图 MEDIUM+HIGH 边（21.8 万,双口径任选）+实体排行限技术/机构 | 证据过滤策略甲方认可 |
| v2 | 跨类实体关系表落地 → 五类实体闭合 | 结构工程 |
| v3 | 实证边入表 → 全量入图 | 上游工程 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 弱推断边画粗线误导 | **高** | 证据过滤门槛入图 |
| 双口径排序不一致被混用 | 高 | 口径标签随图例固化 |
| 机构协同顶格 1.0 失真 | 中 | 多年累计归一 |
| CANDIDATE/DIRECTED 拍平丢语义 | 中 | 弦线图只取无向域+方向态注记 |

### C.5 总判

**部分支持**:技术对边强度是全批最强单点承载（双口径直存 58.7 万边）,但证据质量（LOW 62.91%/推断 100%）与实体粒度空白（五类缺三）双钳制。v1 过滤+收窄即期可用;升档双杠杆（跨类表+实证边）路径清晰。批内图谱族「强度三件套」纪律（强度+证据+口径标签）由本件立。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_INNOV_003.py` | 退出码 0，落 `_out.json` |
| 数据入口 | jiuxin 直连只读;gkx/dev information_schema | demo_* 直接 raise |
| 证据占比复算 | 产物 derived vs 手算 | 17.6003%/62.9079% ✓ |
| 四态分布校验 | 方向四计数求和 | =587,252 ✓ |
| 双口径互证 | Top 边 confidence↔jaccard | 100.0↔1.0 ✓ |
| 判档一致 | MD 文首 vs 产物 `support_judgment` | 部分支持 |
| mock 残留检查 | `rg "score \* 0.95\|max\(72" repos/demo-ui-science/src` | 正式版替换后无兜底伪值 |
