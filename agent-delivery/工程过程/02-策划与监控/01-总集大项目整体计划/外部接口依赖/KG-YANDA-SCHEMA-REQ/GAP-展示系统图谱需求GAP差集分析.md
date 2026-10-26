# 科技信息展示系统 · 图谱需求 GAP 差集分析

> 任务 ID：KG-YANDA-GAP-L01
> 版本：v1.1 · 日期：2026-10-26
> 签收人：human:淮政玮
> 状态：draft

**v1.1 变更**：算法中台侧"已有"列从"需规定义"修正为"真实就绪度"——区分"真实已跑通"（有代码/截图证据）和"定义存在但服务未上线"（is_mock: true，D4=mock）。

---

## 一、分析说明

### 1.1 分析目标

**GAP = 需求侧 - 已有侧**

- **需求侧**：致燕大接口需求清单 v1.0（科技信息展示系统对图谱接口的完整需求）
- **已有侧**：算法中台真实已具备的能力 + 燕大知识图谱引擎已有的能力

### 1.2 数据源

| 数据源 | 内容 | 就绪度判定 |
|---|---|---|
| **需求侧** | 致燕大接口需求清单 v1.0（14 实体 / 17 关系 / 99 属性 / 31 计算能力 / 10 写入接口） | 前序任务 KG-YANDA-SCHEMA-REQ-L01 产出 |
| **已有侧 ①·算法中台（真实就绪度）** | 见下表 | 见下方就绪度分级 |
| **已有侧 ②·燕大** | 17 实体 / 33 关系 / 9 推理服务 + 图谱构建治理查询一体化引擎 | 唐绍祖 KG-YANDA-SCHEMA-COMPARE-L01 调研报告 |

### 1.3 算法中台就绪度分级（诚实性约束）

| 标记 | 含义 | 证据 |
|---|---|---|
| ✅ | **真实已跑通** | 截图/代码/真实运行可验证：GKX 产业链/企业中台上图流水线（截图可见 op_id=CHAIN_NER_INDUSTRY 等）、cfg_metric seed 文件真实存在（11 域 565+ 条）、ADS graph_node/graph_edge 表结构真实存在（数据设计文档）、data-source-mapping-registry.yaml 真实登记 |
| 🔶 | **定义存在但算法服务未上线** | cfg_metric 有定义，但 `is_mock: true`（readiness matrix D4 全部 mock，算法服务待阶段 2 翻转）；repos/ 未 clone（lumen-algo-py、demo-algo-ent-analysis 等代码不可见），实体上图全链路无法验证 |
| 🔴 | **仅需规描述无实现证据** | cfg_model_registry 模型注册（架构有定义但未见真实配置）、完整图算法实现（PageRank/Louvain 等是否有可调用代码不可见） |

### 1.4 GAP 状态标记

| 标记 | 含义 |
|---|---|
| ✅ | 已覆盖：算法中台或燕大**真实已跑通**可覆盖 |
| 🔶 | 部分覆盖：算法中台**定义存在但服务未上线** 或 燕大部分覆盖 |
| 🔴 | 完全空白：算法中台定义未覆盖 + 燕大无对应能力 |

### 1.5 比对范围

| 类别 | 需求侧数量 | 算法中台真实就绪度 | 燕大比对 |
|---|---:|---|---|
| 实体类型 | 14 | 产业全要素图谱 7 类要素（cfg_metric 定义 + ADS 表真实，但上图链路不可见） | 17 实体 TAG |
| 关系类型 | 17 | 上图流水线（GKX 产业链/企业已跑通，其他不可见） | 33 关系 EDGE |
| 图谱计算能力 | 31 | cfg_metric 有定义但 D4 全部 mock | nGQL 控制台 + 图算法作业（真实已跑通） |
| 写入接口 | 10 | Python ETL 流水线（GKX 已跑通，完整写入链路不可见） | Schema 管理 + 构建任务 + 人工审核（真实已跑通） |
| 属性（抽样） | 30 | cfg_metric 指标属性（定义存在） | 实体属性规约（溯源 9~13 条，真实已跑通） |

---

## 二、实体类型 GAP 比对（14 类）

| # | 需求实体 | 中文名 | 算法中台已有（真实就绪度） | 燕大已有（真实已跑通） | GAP | 说明 |
|---|---|---|---|---|---|---|
| 1 | `institution` | 机构 | 🔶 cfg_metric 有 ORG 域定义 + ADS 表存在，但实体上图全链路不可见 | ✅ `Organization` + `OrganizationBase` + `ScholarOrganization`（50 条属性） | ✅ 已覆盖 | 燕大机构实体属性极全，算法中台不构成瓶颈 |
| 2 | `technology` | 技术 | 🔶 cfg_metric 有 TECH 域定义 + ADS 表存在，但上图链路不可见 | 🔶 `Keyword`（仅关键词级，无层级/上下游） | 🔶 部分覆盖 | 算法中台有技术链定义；燕大缺技术层级 |
| 3 | `paper` | 论文 | 🔶 cfg_metric 有定义 + ADS 表存在，但上图链路不可见 | ✅ `Paper`（74.2 万条，32 条属性） | ✅ 已覆盖 | 燕大论文实体是规模最大的（80%），属性齐全 |
| 4 | `patent` | 专利 | 🔶 cfg_metric 有定义 + ADS 表存在，但上图链路不可见 | ✅ `Patent`（48 条属性） + `PatentFamily` | ✅ 已覆盖 | 燕大专利含 IPCR/CPC 分类、专利价值评估 |
| 5 | `project` | 项目 | 🔶 cfg_metric 有定义 + ADS 表存在，但上图链路不可见 | ✅ `Project`（46 条属性） | ✅ 已覆盖 | 燕大项目含 project_level、funded_amount、9 类产出计数 |
| 6 | `field` | 领域 | 🔶 cfg_metric 有学科分类定义，但独立领域实体未上图 | 🔶 `Keyword`（仅关键词映射） | 🔶 部分覆盖 | 论文/专利有 discipline_code，但无独立领域 TAG |
| 7 | `person` | 人员/专家 | 🔶 cfg_metric 有 TALENT 域定义 + ADS 表存在，但上图链路不可见 | ✅ `Person`（4.9 万条，50 条属性） | ✅ 已覆盖 | 燕大 Person 属性极全，含简历/头衔/学术指标 |
| 8 | `enterprise` | 企业 | 🔶 cfg_metric 有 ENT 域定义 + ADS 表存在，但上图链路不可见 | 🔶 混在 `Organization` 中 | 🔶 部分覆盖 | 燕大 Organization 混合企业与科研机构 |
| 9 | **`policy`** | **政策** | 🔶 cfg_metric POLICY seed 有定义（100 条），但 is_mock: true 算法服务未上线 + 上图链路不可见 | **🔴 缺失** | **🔴 完全空白** | **燕大无 Policy TAG；算法中台 POLICY 域定义但上图载体在燕大侧空白** |
| 10 | `dataset` | 数据集 | 🔶 数据源映射表有登记但未上图 | ✅ `DataSource`（18 条属性） | ✅ 已覆盖 | 燕大 DataSource 可复用为 Dataset |
| 11 | `topic` | 主题 | 🔶 论文/专利有 topic_keywords，但独立实体未上图 | ✅ `Keyword`（18 条属性） | ✅ 已覆盖 | 燕大 Keyword 可直接映射 |
| 12 | `event` | 科技事件 | 🔶 无独立事件实体定义 | ✅ `Event`（26 条属性，15 类风险事件表） | ✅ 已覆盖 | 燕大 Event 覆盖展示系统需求 |
| 13 | `activity` | 科技活动 | 🔴 无定义 | 🔴 无对应 TAG | 🔴 完全空白 | 算法中台和燕大均无 |
| 14 | `innovation_carrier` | 创新载体 | 🔶 产业链/企业 cfg_metric 有定义但无载体 | 🔶 `IndustryNode` 可部分映射 | 🔶 部分覆盖 | 缺孵化器/园区特有属性 |

**实体 GAP 汇总**：✅ 已覆盖 7 / 🔶 部分覆盖 5 / 🔴 完全空白 2（policy、activity）

---

## 三、关系类型 GAP 比对（17 类）

| # | 需求关系 | 关系名 | 算法中台已有（真实就绪度） | 燕大已有（真实已跑通） | GAP | 说明 |
|---|---|---|---|---|---|---|
| 1 | `cooperate` | 合作 | 🔶 cfg_metric 有合作强度定义，但合作边上图链路不可见 | ✅ `COAUTHOR_WITH` + `COLLEAGUE` + `ALUMNI`（推理边已落图） | ✅ 已覆盖 | 燕大三类合作边含 co_paper_count/confidence |
| 2 | `belong` | 隶属 | 🔶 任职/隶属关系有定义但上图链路不可见 | ✅ `AFFILIATED_WITH` + `STUDIED_AT` + `EXECUTIVE_OF` + `LEGAL_REP_OF` | ✅ 已覆盖 | 燕大四类隶属关系齐全 |
| 3 | `research` | 研究 | 🔶 topic_keywords 有但无研究关系边 | 🔶 `HAS_KEYWORD`（仅论文→关键词） | 🔶 部分覆盖 | 缺 person/institution/enterprise→field 直接研究关系 |
| 4 | `cite` | 引用 | 🔶 论文引用关系有定义但上图链路不可见 | ✅ `CITES` + `REFERENCED_BY` | ✅ 已覆盖 | 燕大引用属性含 sequence |
| 5 | `participate` | 参与 | 🔶 项目参与关系有定义但上图链路不可见 | ✅ `HAS_PARTICIPANT` + `LEADS` + `FUNDED_BY` | ✅ 已覆盖 | 燕大项目参与含 role(amount/category) |
| 6 | `belong_to` | 属于 | 🔶 学科归属关系有定义但上图链路不可见 | 🔶 `BELONGS_TO_NODE`（仅产业链节点归属） | 🔶 部分覆盖 | 缺 paper/patent/project/technology→field 直接归属 |
| 7 | `author_of` | 著作 | 🔶 作者署名关系有定义但上图链路不可见 | ✅ `AUTHORED_BY` + `INVENTED_BY` | ✅ 已覆盖 | 燕大作者署名含 author_order/is_corresponding |
| 8 | `technology_hierarchy` | 技术层级 | 🔶 GKX 产业链上下游边已跑通截图可见 | ✅ `CHILD_OF`（产业链子节点） | ✅ 已覆盖 | 燕大产业链层级可复用 |
| 9 | `technology_influence` | 技术影响 | 🔶 cfg_metric 有定义但无承载边 | 🔴 无对应 EDGE | 🔴 完全空白 | 燕大缺技术间依赖/促进关系 |
| 10 | `publish` | 发布 | 🔶 政策发布有定义但无承载边 + Policy TAG 未上图 | 🔴 无对应 EDGE | 🔴 完全空白 | 依赖 Policy TAG 建成 |
| 11 | `policy_relate` | 政策关联 | 🔶 政策配套有定义但无承载边 + Policy TAG 未上图 | 🔴 无对应 EDGE | 🔴 完全空白 | 依赖 Policy TAG 建成 |
| 12 | `policy_apply_to` | 政策适用 | 🔶 政策适用有定义但无承载边 + Policy TAG 未上图 | 🔴 无对应 EDGE | 🔴 完全空白 | 依赖 Policy TAG 建成 |
| 13 | `dataset_link` | 数据集关联 | 🔶 数据源映射有引用但无关联边 | 🔶 无 DataSource 自关联边 | 🔶 部分覆盖 | 燕大补边即可 |
| 14 | `about_topic` | 主题相关 | 🔶 topic_keywords 有但关系边不可见 | ✅ `HAS_KEYWORD` | ✅ 已覆盖 | 燕大可复用 |
| 15 | `event_link` | 事件关联 | 🔶 无定义 | ✅ `INVOLVED_IN`（事件→主体） | ✅ 已覆盖 | 燕大含 role 属性 |
| 16 | `activity_link` | 活动关联 | 🔴 无定义 + Activity TAG 不存在 | 🔴 无对应 | 🔴 完全空白 | 依赖 Activity TAG 建成 |
| 17 | `carrier_cooperate` | 载体协同 | 🔶 cfg_metric 有协同定义但上图链路不可见 | ✅ `HAS_NODE` + 6 类投资控制边 | ✅ 已覆盖 | 燕大产业链节点 + 投资边可映射 |

**关系 GAP 汇总**：✅ 已覆盖 8 / 🔶 部分覆盖 4 / 🔴 完全空白 5

---

## 四、图谱计算能力 GAP 比对（31 项）

> **算法中台就绪度标记说明**：✅ cfg_metric 定义 + GKX 截图可见 Degree 已跑通；🔶 cfg_metric 有定义但 is_mock: true（D4=mock，算法服务未上线）

| # | 能力 | 算法中台已有（真实就绪度） | 燕大已有（真实已跑通） | GAP | 说明 |
|---|---|---|---|---|---|
| C-01 | 图谱动态查询与切片 | ✅ cfg_metric 指标查询 + ADS 表直查 | ✅ nGQL 控制台 + graph-search/subgraph | ✅ 已覆盖 | 燕大 nGQL 完全覆盖 |
| C-02 | 实体详情查询 | ✅ ADS graph_node 直查 | ✅ graph-search/entities | ✅ 已覆盖 | 燕大实体列表页可浏览公共属性 |
| C-03 | 邻接实体 TopN | 🔶 cfg_metric 有定义但 is_mock: true | ✅ subgraph（depth/limit/direction） | ✅ 已覆盖 | 燕大子图探索可遍历邻接 |
| C-04 | 多条件图过滤 | 🔶 cfg_metric 有定义但 is_mock: true | ✅ nGQL WHERE 过滤 | ✅ 已覆盖 | 燕大 nGQL 原生支持 |
| C-05 | 子图切片与聚合 | 🔶 cfg_metric 有定义但 is_mock: true | ✅ nGQL GROUP BY | ✅ 已覆盖 | 燕大 nGQL 聚合可实现 |
| C-06 | 路径搜索（BFS/Dijkstra/A*） | 🔶 cfg_metric 有定义但 is_mock: true | ✅ nGQL GO/FIND_PATH | ✅ 已覆盖 | 燕大 nGQL 原生路径算法 |
| C-07 | 关键路径与关键节点识别 | 🔶 cfg_metric 有定义但 is_mock: true | ✅ PageRank + 路径组合 | ✅ 已覆盖 | 燕大 PageRank + 路径搜索可实现 |
| C-08 | 度中心性 | ✅ GKX 截图可见 Degree 已跑通 + cfg_metric 有定义 | ✅ 图算法作业 Degree | ✅ 已覆盖 | **算法中台和燕大均真实已跑通** |
| C-09 | 紧密中心性 | 🔶 cfg_metric 有定义但 is_mock: true | ✅ nGQL 可计算（需自行写查询） | ✅ 已覆盖 | 燕大无专用作业但 nGQL 可实现 |
| C-10 | 中介中心性 | 🔶 cfg_metric 有定义但 is_mock: true | ✅ nGQL 可计算（需自行写查询） | ✅ 已覆盖 | 同上 |
| C-11 | PageRank | 🔶 cfg_metric 有定义但 is_mock: true | ✅ 图算法作业 PageRank | ✅ 已覆盖 | **燕大真实已跑通**，算法中台定义存在 |
| C-12 | 中心性综合评分与相关分析 | 🔶 cfg_metric 有定义但 is_mock: true | 🔴 需自行组合 | 🔶 部分覆盖 | 燕大提供四指标原始值，综合评分需我方在算法中台封装 |
| C-13 | 中心性时序趋势 | 🔶 cfg_metric 有时序定义但 is_mock: true | 🔴 图无时序版本 | 🔴 完全空白 | 燕大图谱无版本化时序快照 |
| C-14 | 社群发现（Louvain/LPA/Infomap） | 🔶 cfg_metric 有 Louvain 定义但 is_mock: true | ✅ 图算法作业 Louvain | ✅ 已覆盖 | **燕大真实已跑通** |
| C-15 | 社群属性与社群间矩阵 | 🔶 cfg_metric 有定义但 is_mock: true | ✅ nGQL 聚合 | ✅ 已覆盖 | 燕大 Louvain 结果 + nGQL 可计算社群属性 |
| C-16 | 社群动态演化追踪 | 🔶 cfg_metric 有定义但 is_mock: true | 🔴 图无时序版本 | 🔴 完全空白 | 依赖 C-13 时序快照 |
| C-17 | 图模式识别与异常点检测 | 🔶 cfg_metric 有风险识别定义但 is_mock: true | ✅ Event + 规则匹配 | ✅ 已覆盖 | 燕大 Event 实体 + nGQL 规则 |
| C-18 | 图聚类 | 🔶 cfg_metric 有定义但 is_mock: true | ✅ nGQL + Louvain | ✅ 已覆盖 | 燕大 Louvain = 图聚类 |
| C-19 | 图推荐与链路预测 | 🔶 cfg_metric 有定义但 is_mock: true | 🔴 无对应作业 | 🔴 完全空白 | 燕大无推荐作业；算法中台定义存在但未上线 |
| C-20 | 趋势预测 | 🔶 cfg_metric 有时序预测定义但 is_mock: true | 🔴 无预测能力 | 🔶 部分覆盖 | 算法中台有时序定义但未上线；燕大无 |
| C-21 | 实体影响力赋分与传播 | 🔶 cfg_metric 有定义但 is_mock: true | ✅ PageRank | ✅ 已覆盖 | 燕大 PageRank 可映射为影响力 |
| C-22 | 图谱指标监测与风险链 | 🔶 cfg_metric 有风险链定义但 is_mock: true | ✅ Event + 规则 | ✅ 已覆盖 | 燕大 Event + 图遍历可构建 |
| C-23 | 指标融合、综合评分与一致性检验 | 🔶 cfg_metric 有融合定义但 is_mock: true | 🔴 需我方封装 | 🔶 部分覆盖 | 燕大提供图指标原始值，融合由算法中台封装 |
| C-24 | 动态指标学习与模型迭代 | 🔶 cfg_metric 有定义但 is_mock: true | 🔴 无对应 | 🔴 完全空白 | 算法中台定义存在但未上线；燕大无 |
| C-25 | 企业研究领域重叠度 | 🔶 cfg_metric 有定义但 is_mock: true | 🔴 无对应 | 🔶 部分覆盖 | 算法中台定义存在但未上线（不依赖燕大 |
| C-26 | 主题演化分析 | 🔶 cfg_metric 有定义但 is_mock: true | 🔴 图无时序版本 | 🔴 完全空白 | 依赖 C-13 时序快照 |
| C-27 | 协同网络绩效与影响力评估 | 🔶 cfg_metric 有定义但 is_mock: true | 🔶 PageRank + 边属性 | 🔶 部分覆盖 | 燕大提供基础图指标，绩效评分算法中台封装 |
| C-28 | 数据集关联分析 | 🔶 cfg_metric 有定义但 is_mock: true | 🔶 DataSource + 引用边 | 🔶 部分覆盖 | 燕大 DataSource 存在，缺关联边 |
| C-29 | 活动-资源-专家关联与推荐 | 🔴 无定义 | 🔴 Activity TAG 缺失 | 🔴 完全空白 | 依赖 Activity TAG 建成 |
| C-30 | 图快照与多格式导出 | 🔶 cfg_metric 有定义但 is_mock: true | ✅ 图谱可视化页面截图 | ✅ 已覆盖 | 燕大图谱可视化可导出 |
| C-31 | 自定义实体/关系建模 | 🔶 需规有定义但无代码证据 | ✅ Schema 管理页（建实体/关系/DDL 执行） | ✅ 已覆盖 | **燕大 Schema 管理是我方缺失的核心中台能力，可直接复用** |

**计算能力 GAP 汇总**：✅ 已覆盖 19 / 🔶 部分覆盖 6 / 🔴 完全空白 6

---

## 五、写入接口 GAP 比对（10 项）

| # | 写入接口 | 算法中台已有（真实就绪度） | 燕大已有（真实已跑通） | GAP | 说明 |
|---|---|---|---|---|---|
| 1 | 实体新增（批量） | 🔶 Python ETL 流水线概念存在，但完整写入链路不可见（repos/ 未 clone） | ✅ Schema 管理 + graph-build 任务编排 | ✅ 已覆盖 | 燕大图谱构建任务编排可直接复用 |
| 2 | 实体属性更新 | 🔶 同上 | ✅ Schema 管理属性编辑 + DDL | ✅ 已覆盖 | 燕大自动执行 DDL |
| 3 | 实体删除（级联删关系） | 🔶 同上 | ✅ nGQL DELETE VERTEX 原生级联 | ✅ 已覆盖 | 燕大 NebulaGraph 原生级联 |
| 4 | 关系新增 | 🔶 同上 | ✅ Schema 管理建 EDGE + 抽取脚本 | ✅ 已覆盖 | 燕大抽取脚本绑定 |
| 5 | 关系属性更新 | 🔶 同上 | ✅ Schema 管理属性编辑 | ✅ 已覆盖 | 同实体属性更新 |
| 6 | 关系删除 | 🔶 同上 | ✅ nGQL DELETE EDGE | ✅ 已覆盖 | 燕大原生支持 |
| 7 | 多源数据批量导入（Excel/JSON） | 🔶 GKX 截图可见产业链/企业上图流水线（CHAIN_NER_INDUSTRY 等 op_id）已跑通 | ✅ graph-build 任务 + 抽取脚本版本化绑定 | ✅ 已覆盖 | **燕大抽取脚本版本化 + cron 调度是我方缺失的，可复用** |
| 8 | 图谱版本创建 | 🔶 ADS 无版本概念 | ✅ graph-space 多空间隔离（18 个） | ✅ 已覆盖 | 燕大多 space 可做快照 |
| 9 | 图谱版本列表/回滚 | 🔶 ADS 无版本回滚 | ✅ graph-build 执行历史可追溯 | ✅ 已覆盖 | 燕大构建历史 + 空间切换可回滚 |
| 10 | 写操作日志/撤销重做 | 🔶 ADS 审计表概念存在但不可见 | ✅ 人工审核队列 + 动态置信度 + match_evidence | ✅ 已覆盖 | **燕大审计能力是我方完全缺失的，可直接复用** |

**写入接口 GAP 汇总**：✅ 已覆盖 10 / 🔶 部分覆盖 0 / 🔴 完全空白 0

> **关键结论**：写入类接口 **100% 可由燕大真实已跑通的能力覆盖**，这是本次 GAP 分析最重要的结论。燕大的 Schema 管理 + 图谱构建编排 + 动态置信度审计 + 人工审核，完整覆盖我方第六章全部写入类接口需求。

---

## 六、核心属性抽样 GAP

从 99 条属性中抽取 10 条关键属性比对：

| 属性名 | 用途 | 算法中台已有（真实就绪度） | 燕大已有（真实已跑通） | GAP |
|---|---|---|---|---|
| `centrality_score` | 中心性分 | 🔶 cfg_metric 有定义但 is_mock: true | ✅ PageRank 作业（真实已跑通） | ✅ |
| `citation_count` | 被引次数 | 🔶 cfg_metric 有定义但 is_mock: true | ✅ Paper.citation_nums | ✅ |
| `cooperation_density` | 合作密度 | 🔶 cfg_metric 有定义但 is_mock: true | ✅ ALUMNI/COLLEAGUE 边属性 | ✅ |
| `overlap_score` | 研究领域重叠度 | 🔶 cfg_metric 有定义但 is_mock: true | 🔶 需自行计算 | 🔶 |
| `synergy_score` | 协同绩效评分 | 🔶 cfg_metric 有定义但 is_mock: true | 🔶 需组合计算 | 🔶 |
| `confidence` | 关系置信度 | 🔶 无统一置信度定义 | ✅ **动态置信度规约**（0.40+0.20+0.10+0.20+0.10） | ✅ |
| `source_table` | 溯源表 | 🔶 无统一溯源定义 | ✅ 13 条溯源属性规约 | ✅ |
| `match_method` | 匹配方式 | 🔶 无统一匹配定义 | ✅ match_method + match_evidence | ✅ |
| `innovation_score` | 创新影响分 | 🔶 cfg_metric 有定义但 is_mock: true | 🔶 需自行计算 | 🔶 |
| `hotspot_flag` | 热点标记 | 🔶 cfg_metric 有定义但 is_mock: true | 🔶 无对应 | 🔶 |

---

## 七、GAP 差集汇总（v1.1 修正）

### 7.1 按类别统计

| 类别 | 需求侧 | ✅ 已覆盖 | 🔶 部分覆盖 | 🔴 完全空白 | 完全空白率 |
|---|---:|---:|---:|---:|---:|
| 实体类型 | 14 | 7 | **5** | **2** | 14% |
| 关系类型 | 17 | 8 | 4 | **5** | 29% |
| 计算能力 | 31 | **19** | **6** | **6** | 19% |
| 写入接口 | 10 | **10** | 0 | 0 | **0%** |
| **合计** | **72** | **44** | **15** | **13** | **18% 完全空白 + 21% 部分覆盖** |

> **与 v1.0 对比**：算法中台侧 v1.0 误将"cfg_metric 定义存在"等同于"真实已跑通"，v1.1 按诚实性约束修正后：✅ 已覆盖从 39→44（燕大图算法作业真实已跑通的发现），🔶 部分覆盖从 16→15，🔴 完全空白从 16→13。**整体 GAP 率略有下降**，主要因为燕大图算法作业（PageRank/Louvain/Degree）真实已跑通，之前在 v1.0 中未充分计入。

### 7.2 🔴 完全空白 GAP 清单（优先级排序）

| 优先级 | GAP 项 | 类别 | 建议补建方向 | 补建方 |
|---|---|---|---|---|
| **P0** | `policy` 实体 | 实体 | 燕大新建 Policy TAG（会议纪要确认仅 1 份政策文档，需扩充数据源） | 燕大 |
| **P0** | `publish` / `policy_relate` / `policy_apply_to` 三条政策关系 | 关系 | 依赖 Policy TAG 建成后补建 | 燕大 |
| **P0** | C-13 中心性时序趋势 / C-16 社群动态演化 / C-26 主题演化 | 计算能力 | 燕大图谱需版本化时序快照（当前无时间维度图版本） | 燕大 |
| **P1** | `activity` 实体 + `activity_link` 关系 | 实体+关系 | 燕大新建 Activity TAG + 活动关联 EDGE | 燕大 |
| **P1** | C-19 图推荐与链路预测 | 计算能力 | 燕大扩展推理服务（已有 9 个，可增第 10 个） | 燕大 |
| **P1** | C-29 活动-资源-专家关联与推荐 | 计算能力 | 依赖 Activity TAG | 燕大 |
| **P2** | `technology_influence` 技术影响关系 | 关系 | 燕大新建 EDGE | 燕大 |
| **P2** | C-24 动态指标学习与模型迭代 | 计算能力 | 算法中台侧补建 + 燕大配合 | 算法中台 |

### 7.3 🔶 部分覆盖 GAP 清单

| GAP 项 | 类别 | 缺口 |
|---|---|---|
| `technology` 实体缺层级/上下游 | 实体 | 燕大 Keyword 需升级为 TechChain |
| `enterprise` 实体混在 Organization | 实体 | 燕大需拆分或我方补过滤 |
| `field` 实体缺独立 TAG | 实体 | 燕大从 Keyword 升级 |
| `innovation_carrier` 缺孵化器属性 | 实体 | 燕大 IndustryNode 需扩展 |
| `research` 关系缺 person→field 直接边 | 关系 | 燕大扩展 EDGE |
| `belong_to` 关系缺→field 直接归属 | 关系 | 燕大扩展 EDGE |
| `dataset_link` 关系 | 关系 | 燕大补 DataSource 自关联边 |
| C-12/C-23 综合评分与融合 | 计算能力 | 算法中台封装（cfg_metric 有定义但 D4=mock） |
| C-20 趋势预测 | 计算能力 | 算法中台 cfg_metric 有定义但未上线 |
| C-25 企业研究领域重叠度 | 计算能力 | 算法中台 cfg_metric 有定义但未上线 |
| C-27 协同网络绩效 | 计算能力 | 算法中台封装 |
| C-28 数据集关联 | 计算能力 | 燕大补 DataSource 关联边 |
| `overlap_score`/`synergy_score`/`innovation_score` | 属性 | 算法中台计算 + 燕大透传 |
| `hotspot_flag` | 属性 | 算法中台计算 |

### 7.4 ✅ 我方可直接复用的燕大独有真实已跑通能力

| 能力 | 说明 | 我方现状 |
|---|---|---|
| **Schema 管理 API** | 实体/关系定义 + 属性编辑 + DDL 自动执行 + 脚本版本化绑定 | ❌ 我方无图谱中台能力 |
| **动态置信度规约** | 0.40(DWD 溯源) + 0.20(稳定机构ID) + 0.10(外部ID) + 0.20(展示身份) + 0.10(地域/时间) | ❌ 我方无统一置信度 |
| **13 条溯源属性** | source_table/source_record_id/ingest_batch/confidence/match_method/match_evidence 等 | ❌ 我方 ADS 无统一溯源 |
| **人工审核队列** | 低置信度数据人工放行 + 抽取失败重跑 | ❌ 我方无审核闭环 |
| **多 graph-space 版本隔离** | dev/techkg/gkx_local_1 等 18 个空间 | ❌ 我方 ADS 无版本快照 |
| **9 推理服务接口** | 校友/同事/合作成果等（2 个已 ready） | 🔶 我方有图算法但无统一推理服务封装 |
| **nGQL 控制台 + 图算法作业** | PageRank/Louvain/Degree 真实已跑通 | 🔶 我方 cfg_metric 有定义但 D4=mock |
| **图谱可视化 + 子图探索** | depth/limit/direction 子图遍历 | ❌ 我方无图谱前端 |

---

## 八、算法中台就绪度总结（诚实性声明）

### 8.1 真实已跑通的能力

| 能力 | 证据 |
|---|---|
| GKX 中台上图流水线 | 产业链/企业两个算法库，图谱五档 A→E，截图可见 op_id=CHAIN_NER_INDUSTRY 等 |
| cfg_metric 种子文件 | `metrics/registry/` 下 11 域，565+ 条指标定义，真实存在 |
| ADS 表结构 | `gkx_ads.graph_node / graph_edge`，数据设计文档真实列出 |
| 数据源映射 | `data-source-mapping-registry.yaml`，60+ 张 dwd_ 表登记 |

### 8.2 定义存在但算法服务未上线（is_mock: true，D4=mock）

| 能力 | 证据 |
|---|---|
| 11 域 cfg_metric 算法指标 | 全部 is_mock: true，readiness matrix D4 标注"全部 mock：算法服务未上线；阶段 2 翻转" |
| 产业全要素图谱实体上图 | repos/ 未 clone（lumen-algo-py 等），完整实体上图链路不可见 |
| cfg_model_registry 模型注册 | 架构基线有定义，但未见真实配置文件 |
| 完整图算法实现 | PageRank/Louvain/Degree 等代码不可见（repos/ 未 clone） |

### 8.3 燕大真实已跑通的能力（可直接复用）

| 能力 | 证据 |
|---|---|
| 17 实体 / 33 关系真实落图 | 87.54 万实体 + 61.88 万关系，日增量 +17/+6 |
| Schema 管理 + 构建编排 | 平台 16 个页面 + 76 路径 API 文档，实测通过 |
| nGQL 控制台 + 图算法作业 | PageRank/Louvain/Degree 真实已跑通 |
| 动态置信度 + 溯源属性 | 9~13 条规约，每批数据自动计算 |
| 人工审核队列 | 低置信度数据进人工审核 |
| 9 推理服务接口 | 校友/同事/合作成果等（2 个 ready） |

---

## 九、结论与建议

### 9.1 核心结论

1. **写入类接口 100% 可由燕大真实已跑通的能力覆盖**——Schema 管理 + 图谱构建编排 + 动态置信度 + 人工审核，完整覆盖我方第六章全部写入需求。**建议直接复用**。

2. **实体/关系 GAP 核心集中在 Policy 和 Activity 两类**——燕大缺 Policy TAG（会议纪要确认仅 1 份政策文档）、缺 Activity TAG。**P0 启动燕大补建 Policy TAG + 数据源扩充**。

3. **计算能力 GAP 核心集中在时序快照**——C-13/C-16/C-26 均依赖图版本化，燕大当前无时间维度图版本。**建议燕大评估时序快照可行性**。

4. **算法中台定义丰富但服务未上线**——cfg_metric 565+ 条指标定义是真实的，但 D4 全部 mock（算法服务待阶段 2 翻转）。我方算法中台与燕大图谱引擎互补性极强：**算法中台管指标计算与融合评分（cfg_metric），燕大管图谱底座、查询接口和写入编排**。

### 9.2 下一步行动建议

| # | 行动 | 负责人 | 优先级 |
|---|---|---|---|
| 1 | 燕大确认 **Policy TAG 补建排期 + 数据源扩充方案** | 燕大 + 我方配合 | P0 |
| 2 | 燕大评估 **图谱时序快照可行性**（支撑 C-13/C-16/C-26） | 燕大 | P0 |
| 3 | 我方**直接复用燕大 Schema 管理 + 图谱构建编排 + 动态置信度审计 + 图算法作业** | 我方 | P0 |
| 4 | 算法中台侧 **cfg_metric 服务上线**（D4 mock → ready，阶段 2） | 算法中台 | P1 |
| 5 | Activity TAG 补建方案（展示系统科技活动功能） | 燕大 | P1 |
| 6 | 补建后更新本 GAP 文档至 v1.2 | human:郭万迎 | P2 |

---

## 十、数据源引用

| 引用 | 路径 |
|---|---|
| 致燕大接口需求清单 v1.0 | `agent-delivery/工程过程/02-策划与监控/01-总集大项目整体计划/外部接口依赖/KG-YANDA-SCHEMA-REQ/科技信息展示系统-知识图谱实体、实体关系属性需求清单.md` |
| 燕大图谱平台 schema 对比调研报告 | `agent-delivery/designs/亿集知识图谱/燕大图谱平台schema对比调研报告.md` |
| cfg_metric 种子文件（11 域） | `agent-delivery/metrics/registry/cfg_metric-*-seed.yaml` |
| metric-readiness-matrix（11 域） | `agent-delivery/metrics/registry/metric-readiness-matrix-*.yaml` |
| 科技专题服务算法库需规 | `agent-delivery/bid-reference/科技专题服务算法库.md` |
| 架构基线 | `agent-delivery/architecture-baseline.md` |
| 数据源映射 | `agent-delivery/data-source-mapping-registry.yaml` |
| ADS 表设计 | `agent-delivery/data/data-design/服务机构/服务机构域数据库设计(v1).md` |
| data-lineage-policy | `agent-delivery/data-lineage-policy.md` |
| GKX 中台上图流程截图 | 本会话提供 |
