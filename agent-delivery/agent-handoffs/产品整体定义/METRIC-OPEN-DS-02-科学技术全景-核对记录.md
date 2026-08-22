# METRIC-OPEN-DS-02-科学技术全景-核对记录

> **任务**：DS-02-METRIC-OPEN-L01（METRIC-OPEN-LOOP Round 9）  
> **角色**：product-agent（口径草稿）+ algorithm-agent / data-agent（协作核对，本叶不改 seed）  
> **监管人**：`human:淮政玮`  
> **日期**：2026-08-22  
> **上游**：无独立四件套 / PACK-L01；本工作流书面 **SRS 02 科学技术全景 + 详设 04 顶 PACK**（给人说明 §8.4 甲）  
> **范围**：catalog `ds_id=DS-02` 五页：`TECHGRAPH` / `ENTITY` / `PATH` / `MAINTAIN-GRAPH` / `MAINTAIN-ENTITY`。不替甲方拍板；公式 / `algorithm_type` **不签**，标 `pending_cosign: human:唐绍祖`（8/25 前不派唐绍祖开工本 loop）。  
> **铁律**：与专题技术链 **同源不同页**。可 mapped 同一 05 叶（104 / 105 / 130 / 96），**禁止**把本页指标改挂 `TOPIC-TECH-METRIC-OPEN-L01` / `TOPIC-TECH-05` OPEN。禁止发明正式 `M_*` 写入 seed。禁止改 A2 catalog 正文、专题 TOPIC-TECH 文件、共享 `LOOP-state.yaml` / `METRIC-OPEN-LOOP-a2-patch.yaml`。

---

## §1 适用性结论（Track-MS 五件套 #4 / #5）

| 五件套项 | 状态 | 说明 |
|----------|------|------|
| #4 指标语义卡 | ✅ 三页 kit + 维护一页整页 N/A + 维护一页 kit（仅推荐列表） | 读面 TECHGRAPH / ENTITY / PATH 有图结构、边权、排名、中心度等统计核 → **出卡**（`TEMP_DS02_*`）。MAINTAIN-GRAPH 七叶全是人工编辑器 → **整页 N/A**。MAINTAIN-ENTITY seq 41 点名算法 Top 列表 → **出卡**；CRUD 仍 N/A。无 TRACE / WF 第 6 列 → **禁止**发明正式 `M_*`。 |
| #5 开放项 | ✅ 适用且已登记（本记录） | 无独立 `DS-02-data-gap-catalog.yaml`、无本模块 `Q0xx`。语义债沿用 A2 `TG-B*` / `ENT-B*` / `PATH-B*`。本叶不改 `客户决策清单跟踪表.md`、不升 🟢、不新建 Q。 |
| PDR-05 自检 | ⏳ 有条件 | 无 TRACE/WF 第 6 列；本记录 + A2 pages 可回指。门 1 完整闭合仍须正式 ID 会签（不发明）+ 公式会签。 |
| PDR-06 自检 | ⏳ 有条件 | GRAPH 边权 / STAT 计数可写演示公式；中心度 / 影响力 / 关键节点识别公式 `pending_cosign`。 |
| 语义 Owner（本工作流） | `human:淮政玮` | 口径 / 8 件套身份项 / 适用性 |
| 公式共签 | `pending_cosign: human:唐绍祖` | 本 loop 不签公式、不改 seed `algorithm_type` |
| 页面要哪些指标（展示） | `human:李伟` | 给人说明责任矩阵；技术维三方对接另由 `human:郭万迎` 对九新 |

**结论**：五页不是同一判定。TECHGRAPH / ENTITY / PATH / MAINTAIN-ENTITY（仅推荐列表）**④ 适用（kit）**；MAINTAIN-GRAPH **整页 N/A + 依据**。库缺口（ENTITY 影响力、PATH 中心度三行）**保持 missing**，不得因本 OPEN 改 mapped。甲方 🟡 不阻断定义交付，**阻断**宣称 FULL 口径与门 1「无条件闭合」。

### §1.1 本叶必须消费本核对记录

| 页 `page_id` | 中文 | ④ | 消费的 ID | 禁止 |
|--------------|------|----|-----------|------|
| `DS-02-TECHGRAPH` | 展示技术点图谱 | **kit** | `TEMP_DS02_TECH_GRAPH` / `TEMP_DS02_TECH_EDGE_STRENGTH` | 挂 `TOPIC-TECH` OPEN；消费 `M_CHAIN_NODE_COUNT` / `EDGE_COUNT` / `M_SVC_GRAPH_*`；把导入壳 / 图交互打 missing |
| `DS-02-ENTITY` | 展示技术点关联实体 | **kit** | `TEMP_DS02_ENT_TOP5` / `TEMP_DS02_ENT_PAPER_PATENT` / `TEMP_DS02_ENT_REL` / `TEMP_DS02_ENT_INFLUENCE` | 挂 `TOPIC-TECH` OPEN；用 `M_CHAIN_ACADEMIC_POWER` / `M_SVC_GRAPH_INFLUENCE` 顶替；把 PATH 中心度改挂本页 |
| `DS-02-PATH` | 展示关键路径和关键节点 | **kit** | `TEMP_DS02_PATH_CENTRALITY` / `TEMP_DS02_PATH_KEYNODE` / `TEMP_DS02_PATH_PRIORITY` | 挂 `TOPIC-TECH` OPEN；mapped seq 130/131/116；用 `M_CHAIN_KEY_NODE_COUNT` / `M_SVC_GRAPH_CENTRALITY` 顶替；因 501 未注册整页 N/A |
| `DS-02-MAINTAIN-GRAPH` | 维护技术图谱 | **na_with_reason** | 无 TEMP_ | 把 CRUD 改判 mapped/missing；把 seq 18 构图抢进本页；发明 `M_GRAPH_EDIT_*` |
| `DS-02-MAINTAIN-ENTITY` | 维护关键实体及关系 | **kit**（仅 seq 41） | `TEMP_DS02_MENT_REC_TOP` | 挂 `TOPIC-TECH` OPEN；硬挂 seq 140；用 `M_SVC_REC_*` 顶替；重列读面 Top5 / xlsx 行 18 |

**专题技术链（A2.1 `TOPIC-TECH-05`）**：本叶 **不消费**。同源 = 可 mapped 同一 05 叶；不同页 = 展示全景五级 ≠ 专题全景下钻。`TOPIC-TECH-METRIC-OPEN-L01` 核对记录 **不是**本页语义层。专题 third_party 热点 / 潜力 / 瓶颈 / 阶段 / 深圳综合 **禁止**改挂为本页缺口。

### §1.2 五页 × 差集（A2 已写，本叶不改判定）

| 页 | SRS seq | 差集要点 | ④ |
|----|---------|----------|----|
| TECHGRAPH | 17–21 | A=0；mapped 图结构 + 关联强度；输入/交互 `n/a_ops`；搜索/详情 `other_system` | kit |
| ENTITY | 22–27 | A=1（影响力/优先级）；mapped Top5/边权、论文专利计数、实体关系网 | kit |
| PATH | 28–33 | A=3（中心度 / 关键节点重要性 / 节点优先级）；mapped=0；501 未注册 | kit |
| MAINTAIN-GRAPH | 34–40 | A=0；七叶全 `n/a_ops`（无算法生成句） | **N/A** |
| MAINTAIN-ENTITY | 41–47 | A=0；seq 41 mapped 104/105；CRUD 六叶 `n/a_ops` | kit（推荐列表） |

### §1.3 TRACE / A2 语义层指针（Round 18 才回写 catalog 正文）

本叶 **不改** `metrics/request/展示系统/A2-GAP-page-catalog.yaml` 与 pages yaml 正文。指针写入 `_work/open-loop/DS-02-METRIC-OPEN-L01-a2-patch.yaml`（本叶私有；**不**写共享 `METRIC-OPEN-LOOP-a2-patch.yaml`）。

| 层 | 路径 | 本叶要求的指针 |
|----|------|----------------|
| 核对记录 | **本文件** | DS-02 五页唯一 OPEN 真源 |
| A2 页 yaml | `metrics/request/展示系统/pages/DS-02-*.yaml` | 应收口：`metric_open_status: present`；`metric_open_path` = 本文件；`metric_open_task: DS-02-METRIC-OPEN-L01`。**库缺口 `missing` 不动**（ENTITY-D04、PATH-D01/D02/D03）。 |
| A2 catalog | `A2-GAP-page-catalog.yaml` 的 DS-02 五条 | Round 18 才改 `missing`→`present` |
| TRACE / WF | **无**展示 DS-02 四件套 | `trace_metrics` / `wireframe_metric_ids` 保持空 |
| PACK | 无独立 `DS-02-PACK-L01` | SRS 02 + 详设 04 顶 PACK；FDS **不顶** OPEN |

口径会签：`owner_semantic = human:淮政玮`；公式 / `algorithm_type` 共签仍 `human:唐绍祖`。

---

## §2 模块消费矩阵（TEMP_ 草稿 · 禁止正式 M_*）

> 差集列维持 A2 已写判定。本表只闭合语义层。`algorithm_type` 列为 **草稿建议**，未会签。  
> **`TEMP_*` ≠ 正式 `M_*`**：只存在于本核对记录与机器卡；**禁止**写入 `metrics/registry/` seed。  
> **禁止**把下表改写成 `M_TECH_*` / `M_PATH_*` / `M_CHAIN_*` / `M_SVC_*`，也禁止改挂 `TEMP_TOPIC_TECH_*`（若专题叶另造）。

| temp_id | 宿主页 | 适用 | 建议 type（未签） | A2 差集 | pending |
|---------|--------|------|-------------------|---------|---------|
| TEMP_DS02_TECH_GRAPH | TECHGRAPH | ✅ kit | GRAPH | mapped（TG-D02；05 seq 130/105/104） | 同源 TOPIC-TECH-05 不改挂 OPEN |
| TEMP_DS02_TECH_EDGE_STRENGTH | TECHGRAPH | ✅ kit | GRAPH | mapped（TG-D03；seq 105） | 实体排序边权归 ENTITY |
| TEMP_DS02_ENT_TOP5 | ENTITY | ✅ kit | GRAPH | mapped（ENT-D01） | 读面 Top5；不重列维护面 |
| TEMP_DS02_ENT_PAPER_PATENT | ENTITY | ✅ kit | STAT | mapped（ENT-D02；seq 96） | 材料计数，不进点类型 |
| TEMP_DS02_ENT_REL | ENTITY | ✅ kit | GRAPH | mapped（ENT-D03） | 禁止 seq 116 |
| TEMP_DS02_ENT_INFLUENCE | ENTITY | ✅ kit | MODEL | **missing**（ENT-D04） | 保持 missing；不发明 M_* |
| TEMP_DS02_PATH_CENTRALITY | PATH | ✅ kit | GRAPH | **missing**（PATH-D01） | 保持 missing；禁 `M_SVC_GRAPH_CENTRALITY` |
| TEMP_DS02_PATH_KEYNODE | PATH | ✅ kit | GRAPH | **missing**（PATH-D02） | 501 未注册 ≠ N/A；禁 seq 131 深圳链 |
| TEMP_DS02_PATH_PRIORITY | PATH | ✅ kit | GRAPH | **missing**（PATH-D03） | 与 KEYNODE 同识别族、半成品分行 |
| TEMP_DS02_MENT_REC_TOP | MAINTAIN-ENTITY | ✅ kit | GRAPH | mapped（MENT-D01） | 维护面候选；不重列读面 Top5 |

**10/10 TEMP_ 均有本叶 present。** mapped 行不得改 missing；missing 行不得因 OPEN 改 mapped。MAINTAIN-GRAPH **零 TEMP_**。

---

## §赋号表（TEMP_ → M_* · 赋号草稿 · 类型未签）

> **日期**：2026-08-22。`algorithm_type` = `suggested_unsigned`，**不**会签、**不**写 seed、**不**改展示 catalog。ELEMENT 默认 `TECH`。  
> 与 TOPIC-TECH **同口径**才共享 ID；**禁止**把 `TOPIC-TECH-METRIC-OPEN-L01` 改挂为本页唯一消费。  
> 库 missing（影响力 + 中心度三行）**保持**；赋号 ≠ mapped。MAINTAIN-GRAPH **整页 N/A，不造 ID**。

| temp_id | metric_id | reuse | 建议 type（未签） | Q | A2 | 页 |
|---------|-----------|-------|-------------------|---|----|----|
| TEMP_DS02_TECH_GRAPH | `M_TECH_GRAPH_STRUCT` | — | GRAPH | — | mapped | TECHGRAPH |
| TEMP_DS02_TECH_EDGE_STRENGTH | `M_TECH_EDGE_STRENGTH` | — | GRAPH | — | mapped | TECHGRAPH |
| TEMP_DS02_ENT_TOP5 | `M_TECH_ENTITY_TOP5` | —（被维护面复用） | GRAPH | Q-MO-DS02-01 | mapped | ENTITY |
| TEMP_DS02_ENT_PAPER_PATENT | `M_TECH_PAPER_PATENT_CNT` | 预共享 TOPIC-TECH 同口径 | STAT | Q-MO-DS02-04 / 05 | mapped | ENTITY |
| TEMP_DS02_ENT_REL | `M_TECH_ENTITY_REL` | — | GRAPH | — | mapped | ENTITY |
| TEMP_DS02_ENT_INFLUENCE | `M_TECH_ENTITY_INFLUENCE` | — | MODEL | Q-MO-DS02-03 | **missing 保持** | ENTITY |
| TEMP_DS02_PATH_CENTRALITY | `M_TECH_PATH_CENTRALITY` | — | GRAPH | — | **missing 保持** | PATH |
| TEMP_DS02_PATH_KEYNODE | `M_TECH_PATH_KEYNODE` | — | GRAPH | Q-MO-DS02-02 | **missing 保持** | PATH |
| TEMP_DS02_PATH_PRIORITY | `M_TECH_PATH_PRIORITY` | — | GRAPH | Q-MO-DS02-02 | **missing 保持** | PATH |
| TEMP_DS02_MENT_REC_TOP | `M_TECH_ENTITY_TOP5` | 复用读面 Top5 | GRAPH | Q-MO-DS02-01 | mapped | MAINTAIN-ENTITY |
| （无 TEMP_） | **不造号** | — | — | — | n/a_ops | MAINTAIN-GRAPH |

**计数**：TEMP 赋号 10；唯一 `M_*` 9；复用 2（专题同口径预共享 1 + 页内同源不同面 1）；Q 5（`Q-MO-DS02-01`…`05`，全 🟡）；MAINTAIN-GRAPH 0 ID。建议类型：GRAPH 8 / STAT 1 / MODEL 1。路径中心性偏 GRAPH，不改挂 `M_SVC_GRAPH_*` / `M_SYNTH_COLLAB_CENTRALITY` / `M_ENT_NODE_CENTRALITY`。

叶级卡：`metrics/request/_work/id-assign/DS-02-METRIC-OPEN-L01.yaml`；Question：`…/DS-02-METRIC-OPEN-L01-questions.yaml`（**不**写共享 `METRIC-SEMANTIC-QUESTIONS.md`）。

---

## §3 ④ 指标语义卡（按页 · 不写 seed）

身份项（temp_id / 中文名 / 口径）由淮政玮本工作流确认适用。公式 / 权重 / `algorithm_type` 一律 `pending_cosign: human:唐绍祖`。源表以详设 04「display BFF + 可选 `graph/view`、读面 A 技术点网」+ A1 技术链维 ODS 判定为准，**不**把项目 DWD 反推成 ODS `full`。

8 件套草稿字段（TEMP_ 共同）：metric_id=下表 temp_id；源系统=科技信息展示系统·科学技术全景；更新频率=未定；version=`draft-open-ds02`；源表=ADS / Nebula A 面技术点网（A1 表2 未交 → 本叶不填伪 full）。图：节点=技术点（`entity_type=technology`），边=技术–技术或技术–实体；**当前图**（Nebula）。Java 不写 NLP、不直连 nGQL。

### §3.1 DS-02-TECHGRAPH · kit（seq 17–21）

详设 04：G1/G2 · 读面 A 技术点网；与专题 `.4.1` 同源不同页。

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS02_TECH_GRAPH | 技术点网图结构 | 按已有技术点数据自动计算技术–技术关联，生成可视化技术点图谱；层级/类型用颜色形状区分。布局/配色是图壳，不另造 ID | 演示：子图 `entity_type=technology`；构图对上 05 seq 130 + 105 + 104。禁止伪展开 05 散文当公式 | GRAPH |
| TEMP_DS02_TECH_EDGE_STRENGTH | 技术–技术关联强度 | 技术点之间边权重（半成品 xlsx 行 18 本五级只消费技术–技术边）。实体–技术点排序强度归 ENTITY | 边属性随 seq 105；不伪展开。禁止 seq 116 / `M_SVC_GRAPH_*` | GRAPH |

招标父句「时间轴动态实体关联 / 关键实体排名」落 ENTITY，不进本页。详设 §7 不做专题全景时间轴 → **不**因此 missing。

### §3.2 DS-02-ENTITY · kit（seq 22–27）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS02_ENT_TOP5 | 根节点 Top5 关键实体与关联强度 | 初始化展示根节点关联 Top5（人/机构/论文/专利）；卡片含名称、类型、关联强度。Top5=按已有 105 边权截取，不另造排序模型 | `TOP 5 BY edge_weight`；边类型含技术–人才/企业/科研机构。禁止 `M_CHAIN_ACADEMIC_POWER` | GRAPH |
| TEMP_DS02_ENT_PAPER_PATENT | 论文量 / 专利量 | 技术点关联论文、专利的清单与计数（材料，**不进点类型**）。只消费计数，不铺交易额/资讯 11 项 | `COUNT` 对齐技术点；禁止伪增长率；禁止 `M_CHAIN_SZ_PATENT` / `REG_PAPERS` / `REG_PATENT` | STAT |
| TEMP_DS02_ENT_REL | 实体关联关系网 | 连线或网络图展示实体之间关联。消费 seq 105 关系库，不另开模型 | 同 105 关系面；禁止 seq 116；禁止 PATH 关键路径顶替 | GRAPH |
| TEMP_DS02_ENT_INFLUENCE | 技术点影响力 / 实体优先级 | 按「影响力」等指标自动排序、优先展示重要实体（xlsx 行 19）。**关联强度排序已由 TOP5 覆盖，不重复 missing** | 05 无「技术点关联实体优先级」专叶 → 库 **missing** 保持。禁止伪公式、禁止 PATH 中心度改挂、禁止 `M_SVC_GRAPH_INFLUENCE` / `M_CHAIN_TECH_POWER` | MODEL |

### §3.3 DS-02-PATH · kit（seq 28–33）

catalog note：路径/关键节点 **未注册 501**；与专题技术链同源不同页。未注册 ≠ 整页 ④ N/A。原文要识别算法且 05 无路径/关键节点专叶 → 三行 **missing 保持**，卡面仍出。

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS02_PATH_CENTRALITY | 中心度 | 节点在技术点网中的核心程度；seq 29 作为关键节点识别输入（xlsx 行 17） | seq 96 无中心度；seq 130 无中心度；seq 116 有中心度但是综合维图谱工作台，**禁止 mapped**。不消费 `M_SVC_GRAPH_CENTRALITY` | GRAPH |
| TEMP_DS02_PATH_KEYNODE | 关键节点重要性 | 按中心度、影响力自动识别关键节点并特殊样式标记（xlsx 行 20）。放大/变色/图标是同一结果的前端壳 | seq 130 全文无「识别关键节点」；seq 131 有该短语但是 **深圳链**，禁止改挂全景。05 无专叶 → missing | GRAPH |
| TEMP_DS02_PATH_PRIORITY | 节点优先级 / 重要度 | 图谱节点关键程度，用于识别核心节点（xlsx 行 22）。与 KEYNODE 同识别族、半成品分行 | 05 无对应专叶 → missing。筛选「重要性级别」交互壳不另开 ID | GRAPH |

禁止用 `M_CHAIN_KEY_NODE_COUNT` / `M_CHAIN_BOTTLENECK_*` / seq 136 转化瓶颈顶替本页技术路径。

### §3.4 DS-02-MAINTAIN-ENTITY · kit（仅 seq 41）

catalog default_hint：维护面偏 `n/a_ops`，**有算法生成再 mapped**。seq 41 原文点名「算法自动计算 Top 关键实体」→ 对上 104/105 → mapped → 出卡。seq 42–47 CRUD 见 §3.6。

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS02_MENT_REC_TOP | 关键实体推荐列表 | 维护面：按算法计算并展示与当前技术领域相关的 Top 人/机构/论文/专利候选（名称、类型、关联强度）。与 ENTITY Top5 **同源不同面**（读面侧栏 vs 维护候选），不重列 xlsx 行 18 | 按 105 边权截取；不另造推荐模型。禁止硬挂 seq 140 深圳布局领域推荐。禁止 `M_SVC_REC_*` / `M_CHAIN_LAYOUT_RECOMMEND_COUNT` | GRAPH |

「添加到全景图时智能计算关联强度」复用本卡边权，不另造 TEMP_。

### §3.5 ④ 不适用 · MAINTAIN-GRAPH 整页 N/A

| 宿主 | 项 | 差集判定 | N/A 依据 |
|------|----|----------|----------|
| `DS-02-MAINTAIN-GRAPH` seq 34–40 | 技术节点/关系增删、属性编辑、历史撤销、保存版本 | **`n/a_ops`**（七叶全） | 原文是右键/工具栏/对话框 **人工编辑器**。无「算法自动生成 / 推荐补边」。UUID ≠ seq 104 NER；人工填关系强度 ≠ 网络边权。05 seq 104/105 描述里的增删改是 **算法库实体库运维**，不是本页 G6 编辑器。禁止 mapped、禁止 missing、禁止发明 `M_GRAPH_EDIT_*`。seq 18 构图权在 TECHGRAPH，禁止抢进本页。 |

### §3.6 ④ 不适用（页内 N/A + 依据）

整包五页 N/A：**无**（三读面 + 维护推荐列表有统计核）。页内 N/A 如下。

| 宿主 | 项 | 差集判定 | N/A 依据 |
|------|----|----------|----------|
| TECHGRAPH seq 17 | 技术点图谱数据输入（手动/Excel/JSON） | `n/a_ops` | 导入/schema 解析是运营壳，不是 05 NER。禁止 mapped seq 104，禁止 missing「库无导入叶」 |
| TECHGRAPH seq 19 | 图谱交互（缩放/平移/拖拽/展开折叠/高亮路径） | `n/a_ops` | 图壳。「高亮路径」≠ 关键路径识别（PATH） |
| TECHGRAPH seq 20 | 技术点搜索定位 | `other_system` | 检索门面 + 图定位。禁止 mapped seq 116。xlsx 行 21 技术主题热度不进本页 |
| TECHGRAPH seq 21 | 技术点详情 | `other_system` | ADS/graph 节点字段。「发展状态」≠ seq 137 阶段 Job。论文专利列表归 ENTITY |
| ENTITY seq 23 | 节点点击交互 | `n/a_ops` | 侧栏刷新壳；结果集仍是 TOP5 |
| ENTITY seq 24 | 实体详情弹窗 | `other_system` | ADS/实体库字段；计数已由 PAPER_PATENT 覆盖 |
| ENTITY seq 25 | 类型/时间筛选 | `n/a_ops` | 前端过滤 |
| ENTITY seq 26 后半 | 实体关联时间轴回放 | `n/a_ops` | 边时间戳前端回放；不是 PATH 演示、不是 seq 132 |
| ENTITY seq 27 后半 | 用户按时间/名称/类型排序 | `n/a_ops` | 前端排序；自动影响力见 INFLUENCE |
| PATH seq 28 | 关键路径数据接收与处理 | `other_system` | 展示 BFF 读已算结果；识别缺口在三张 TEMP_，不把接收叶打 missing |
| PATH seq 30 | 路径详情 | `other_system` | 读路径字段；详情「发展历程」≠ seq 132 |
| PATH seq 31 | 路径筛选过滤 | `other_system` | 前端过滤 |
| PATH seq 32 | 路径比较（并排/重叠） | `n/a_ops` | 展示对比，不是比较模型。禁止 missing、禁止挂 seq 135 |
| PATH seq 33 | 关键路径动态演示 | `n/a_ops` | 前端播放。禁止 mapped seq 132 |
| MAINTAIN-ENTITY seq 42–47 | 添加到图 / 删实体 / 删关系 / 改属性 / 改关系 / 批量 | `n/a_ops` | 人工编辑器。表单「重要性等级 / 关系强度」≠ 算法分，不重开 ENT-D04 missing |
| 本叶范围外 | `TOPIC-TECH-05` 整包 | `other_system` | **禁止**改挂本页 OPEN。专题 A=0 不重列其 missing |
| 本叶范围外 | DS-03 技术评估工作流/结果 | `other_system` | 不在本页跑专题技术链 Job |
| 无独立核 | 布局配色、标记样式、版本操作人 | 图壳 / CMS | **禁止**发明正式 `M_*` |

---

## §4 ⑤ 开放项（已登记 · 不升 🟢）

| ID | 本轮动作 | 状态保持 |
|----|----------|----------|
| TG-B01 / ENT-B01 / PATH 语义层「无 OPEN」 | **本叶闭合文件级**：核对记录 present。A2 catalog 正文 Round 18 才改指针 | 语义欠账→有指针；非 A 类 missing |
| TG-B02 | 图结构 / 关联强度无正式 `metric_id` | 覆盖 mapped；不发明 M_* |
| TG-B03 / PDR-05/06 | 有条件；公式未签 | ⏳ |
| ENT-B02 | 关联强度无正式 ID | mapped 保持 |
| ENT-B03 / ENT-D04 | 技术点影响力 / 实体优先级 | **库 missing 保持** |
| PATH-B01 / D01 | 中心度 | **库 missing 保持** |
| PATH-B02 / D02 | 关键节点重要性 | **库 missing 保持** |
| PATH-B03 / D03 | 节点优先级/重要度 | **库 missing 保持** |
| data-gap-catalog | **N/A** | 无 `DS-02-data-gap-catalog.yaml`；缺口长文案真源 = A2 `semantic_debt` + 本 §4。本叶不新建 catalog |
| Q0xx | **N/A** | 客户决策清单 **无** DS-02 专号。不发明 `Q-DS02-*`、不改挂企业/专题 Q。赋号叶级 `Q-MO-DS02-01`…`05` 只写 `id-assign/*-questions.yaml`，**不**进本表、不升 🟢 |

未关闭任何甲方项。未改 `客户决策清单跟踪表.md`。

---

## §5 贴源摘要（data-agent 协作 · 不改 registry）

| 层 | 结论 |
|----|------|
| 调用链 | 前端 → Java display BFF / REST → 只读 ADS；图读 Nebula A 面 `graph/view`。Java 不写 NLP / 不直连 nGQL。PATH 识别算法 501 未注册 → 结果包若存在也只经 Java 下发，本叶不伪挂 05 叶 |
| 准入 / ODS | 技术点主键归一；A1 技术链维表2 未交 → 本叶 D3 不得伪 `full` |
| 算法库 05 | TECHGRAPH 可 mapped 130/105/104；ENTITY 可 mapped 105/104/96；MAINTAIN-ENTITY 推荐列表同 104/105。PATH **不对上**任何 05 专叶。专题热点/潜力/瓶颈/阶段 **不改挂** |
| 本叶不做 | 不写 `cfg_metric-*-seed.yaml`；不改 A2 catalog / pages 判定；不改 TOPIC-TECH 文件；不把 4 条库 missing 改 mapped |

---

## §6 UI / 评审挂载要求（给 V1 / 迁移叶）

- 凡统计数字：ⓘ MetricSpecCard。seed **仍无**本页正式 ID → 回指 **§赋号表 `M_TECH_*` 草稿**（对照 `TEMP_DS02_*`），**禁止**点开 `TOPIC-TECH` OPEN 当本页唯一 8 件套，**禁止**点开 `M_CHAIN_*` / `M_SVC_*` 伪 8 件套
- Wave 0：🧪 MockBadge
- 库 missing 的影响力 / 中心度 / 关键节点：D1 按 `missing` 诚实（红问号），**不显伪 8 件套**
- 关闭评审模式 DOM 零泄漏 `metric_id` / `TEMP_` / `Q-*` / 就绪度字样
- 功能实现 Owner（展示页指标清单）= `human:李伟`；技术维三方对接 = `human:郭万迎`（对九新）。STAT → GDF ADS + Java 聚合；GRAPH 计算仍归唐绍祖监管 Python（给人说明 §2.3）

---

## §7 产物清单

| 产物 | 路径 |
|------|------|
| 本核对记录 | `agent-handoffs/产品整体定义/METRIC-OPEN-DS-02-科学技术全景-核对记录.md`（含 §赋号表） |
| 机器卡 | `metrics/request/_work/open-loop/DS-02-METRIC-OPEN-L01.yaml`（demands 已换 `M_*`，保留 `temp_id`） |
| A2 指针补丁（本叶私有） | `metrics/request/_work/open-loop/DS-02-METRIC-OPEN-L01-a2-patch.yaml`（本轮 **未改**） |
| 赋号卡 | `metrics/request/_work/id-assign/DS-02-METRIC-OPEN-L01.yaml` |
| 叶级 Question | `metrics/request/_work/id-assign/DS-02-METRIC-OPEN-L01-questions.yaml` |
| 薄 handoff | `agent-handoffs/算法库联调-ALGO-LIB/DS-02-METRIC-OPEN-L01.md` |
| **未改** | `metrics/registry/` seed / 矩阵；A2 catalog 正文；pages yaml 差集判定；TOPIC-TECH 文件；共享 `LOOP-state.yaml`；共享 `METRIC-OPEN-LOOP-a2-patch.yaml`；共享 `METRIC-SEMANTIC-QUESTIONS.md` |

---

## §8 签署区（待真人）

| 角色 | 姓名 | 结论 | 日期 |
|------|------|------|------|
| 语义 Owner（本工作流） | 淮政玮 | _口径草稿已出；适用性：TECHGRAPH / ENTITY / PATH / MAINTAIN-ENTITY **kit**；MAINTAIN-GRAPH **整页 n/a_ops**；库 missing 4 行保持；**零改挂** TOPIC-TECH OPEN；赋号草稿 10 TEMP→`M_TECH_*`（类型未签）；**仍零**写入 seed_ | 2026-08-22 |
| 公式 / `algorithm_type` | 唐绍祖 | _pending_cosign（8/25 前不派本 loop）；本叶仅为 suggested_unsigned_ | |
| 甲方 Q | — | 本模块无 Q0xx；叶级 `Q-MO-DS02-01`…`05` 全 🟡，不写客户决策清单、不升 🟢 | |
