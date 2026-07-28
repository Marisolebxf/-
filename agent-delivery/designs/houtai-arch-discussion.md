# 后台整体实现架构讨论 · 全栈场景与数据流时序图汇编

> **来源**：2026-07-27 会话讨论（4 轮问答）
> **参与方**：用户 + AI assistant
> **依据**：`architecture-baseline.md`（方案 A 共享聚合核心）· `scope-baseline.yaml`（58 功能点 ±10%）· `数据库设计.md` · `graph-engine.md` · `observability.md` · `cicd-pipeline.md` · `repo-registry.yaml` · `task-registry.yaml` · `bid-reference/智能服务集群-完整.md`（425K 字）· `bid-reference/科技专题服务算法库.md`（105K 字）
> **导出时间**：2026-07-27 19:42 UTC+8

---

## 目录

1. [第一轮：后台整体实现架构讨论提纲](#第一轮后台整体实现架构讨论提纲)
2. [第二轮：向量数据库需求分析](#第二轮向量数据库需求分析)
3. [第三轮：四大技术栈应用场景全景图](#第三轮四大技术栈应用场景全景图)
4. [第四轮：典型场景数据流时序图 + 服务调用链全集](#第四轮典型场景数据流时序图--服务调用链全集)
5. [附录：速查总表与关键模式总结](#附录速查总表与关键模式总结)

---

# 第一轮：后台整体实现架构讨论提纲

> 基于架构基线、范围基线、仓库映射、数据设计、CI/CD、可观测性和当前任务进度梳理。任务统计：done 85 / blocked 26 / in_progress 11 / review 15 / ready 8。

## 一、总体目标拓扑（方案 A 共享聚合核心）

**核心命题**：科技信息展示系统 + 科技专题服务系统共享同一套 Java 聚合核心（`gkxlumen-topic` + `gkxlumen-metrics`），不各造一套算法调用。

讨论点：
1. 调用链铁律复核：`前端 → 网关 → Java 聚合（只读 ADS + Feign /internal/*）→ Python 算法库`，三层是否仍有越层风险？
2. `gkxlumen-innov`（M1 创新监测展示域）与 `gkxlumen-topic`（七要素专题聚合）的长期关系——何时并入、是否保留独立快路径？
3. `gkxlumen-display` 薄 BFF（Wave4 建）是否仍需要，还是直接由 `topic` + `metrics` 拼装？
4. 两个前端（`lumen-ui-science-pc` 展示 34 页 + `lumen-ui-topic` 专题服务）共享聚合核心的实际边界与冲突点。

## 二、服务清单与边界（5+1 服务）

| 服务 | 语言 | 路由 | 状态 |
|---|---|---|---|
| `gkxlumen-gateway` | Java | 全部对外路由 | 待建（demo 有 gkx-gateway） |
| `gkxlumen-topic` | Java | `/topic/v1/{element}/*` | 待建（七要素聚合核心） |
| `gkxlumen-metrics` | Java | `/metrics/v1/*` | 待建（指标注册中心） |
| `gkxlumen-innov` | Java | `/innov/v1/*` | demo 已有，待移植 |
| `gkxlumen-display` | Java | `/display/v1/*` | Wave4 待建 |
| Python 算法库 | Python | 仅 `/internal/*` | innov-algo / ent-analysis / topic-py |

讨论点：
1. Java 服务的模块拆分粒度：是 PigX 多模块单体（`lumen-svc-platform` / `demo-svc-platform` 现状）还是独立微服务？
2. 网关统一鉴权/SSO/权限的落地方案（D6 横切统一）——目前鉴权细节是否已定？
3. Python 算法库的"统一出口"（指标注册 `cfg_metric` + 模型注册 `cfg_model_registry`）如何强制落地——绕过注册中心的检测机制？
4. 各服务的禁止项红线复核：Java 禁算法/NLP/图谱/写 ADS；Python 禁对前端暴露 REST。

## 三、数据架构与契约面（D3 + D7）

**铁律**：Java 业务 API 仅读 `*_ads`（+ `app_user` 读写）；禁止扫 ODS/DWD、禁止 Java 写 ADS。

### 3.1 三引擎分工
| 引擎 | 产品 | 读写方 |
|---|---|---|
| RDBMS | MySQL 8.0 | Python 写 ADS/DWD；Java 只读 ADS |
| Graph | NebulaGraph 3.x | Python 灌数/查询；Java 禁直连 nGQL |
| Search | Elasticsearch 8.x | Python 写；Java 只读或经 Python 代理 |

### 3.2 Schema 划分（10 库）
- 创新监测：`innov_dim` / `innov_dwd` / `innov_dwm` / `innov_ads` / `innov_cfg`
- 七要素平台：`gkx_dim` / `gkx_dwd` / `gkx_dwm` / `ads` / `gkx_cfg`
- 用户中心：`app_user`（Java 维护）

讨论点：
1. **D7 数据契约先行 + Mock 先行**：三方原始数据源表结构未定期间，Python 写 Mock 至 ADS——当前 Mock 覆盖率？三方源就绪时间表？
2. 数据工厂 `ODS → DWD → ADS` 转换链路归属与 SLA——`lumen-etl-es-py`（DWD→ES）已起，全链路谁负责？
3. 七要素与存储映射（E1 企业 `entan`/`ads.ent_*` … E7 政策 `gkx_policy`/`ads.policy_*`）——各要素 ADS 表落地进度？
4. ADS 结构变更会签机制（Python + Java 双方 handoff）是否落地？
5. `cfg_metric` 指标注册表 + `cfg_model_registry` 模型注册表的物理落地与 Java catalog API 对接。

## 四、算法库架构（Python 侧）

**定位**：全部算法（ETL / NLP / 图谱 / 模型推理 / 指标计算）只在 Python，仅暴露 `/internal/*`。

讨论点：
1. 算法仓划分：`demo-algo-science`（innov P1–P9）/ `demo-algo-ent-analysis`（企业图谱）/ `demo-svc-topic-py`（专题服务，部分未实现）/ `lumen-etl-es-py`（DWD→ES）——是否需要新建正式 `lumen-algo-*` 仓？
2. 七类基础指标 + 产业全要素图谱 + 七要素深度分析模型（共 15 个算法单元）的实现路径与替代策略。
3. 算法能力注册强约束：新算法必须注册 `cfg_metric` / `cfg_model_registry`，如何 CI 扫描兜底？
4. Python 服务的 `/internal/*` 接口契约标准化。

## 五、图谱引擎（NebulaGraph）

**铁律**：统一 NebulaGraph（`192.168.88.43:9669`），禁止 Neo4j。

讨论点：
1. Space 规划：`entan`（demo 已有）/ `gkx_policy`（Wave1 待建）/ `gkx_innov`（networkx 待迁）/ `gkx_topic`（二期）。
2. Java 经 Feign 调 Python `/internal/graph/*`，响应必带 `source: nebula|pg|error`。
3. PG 兜底机制（Nebula 不可用时读 PG 镜像 1 跳子图）。
4. `demo-algo-science` P5 networkx → NebulaGraph 迁移排期。

## 六、可观测性（OTel 全栈）

讨论点：
1. Java：OTel JavaAgent + 网关回传 traceparent——`lumen-svc-platform` 移植进度（E-INNOV-M1-L02b 待做）。
2. Python：`opentelemetry-instrument`——`demo-algo-science` 仍裸 uvicorn，待对齐。
3. 前端：`observability.ts` + axios 拦截器——`lumen-ui-science-pc` 已具备，topic/mobile 待补。
4. 基础设施：OTel Collector → Tempo/Prometheus/Loki → Grafana。
5. 跨服务 trace 连续性验收（Java → Python 跨服务 span 串联）。

## 七、CI/CD 与部署

讨论点：
1. 各仓 CI/CD 现状缺口：`lumen-svc-platform` 全量 CI 待建——最大缺口；`demo-svc-topic-py` 的 ai/analytics/graph 服务未实现。
2. 分支策略：业务子仓 `feat/* → MR/merge → dev → CI/CD → K8s dev`；`main` 仅稳定快照。
3. 部署方式：前端 NodePort（pc 30891 / topic 30892 / admin 30893）；Java helm gkx-platform；Python helm 热更新。
4. **Pipeline Waiver**（2026-06-20 PM 决策）：当前略过等待 Pipeline/K8s——何时取消恢复全闭环？

## 八、仓库结构与迁移（RFC-002）

讨论点：
1. 路径真源：`GKX_ROOT=F:/gkx-lumen`，老根 `E:/gkx_src` deprecating——M5 strict 验收时间表？
2. demo ↔ lumen 镜像关系：demo2 原型仓只读参考，禁止 merge；`frontend-agent` 工程化复刻模式。
3. GitLab group `gkx-lumen`（id 336）项目管理与权限。

## 九、前端架构边界（D8 + D10，与后台对接面）

讨论点：
1. 前端只调 Java REST（经网关），禁直连 Python/DB/Nebula——如何 CI 扫描兜底？
2. 网关路由划分：`/display/**` / `/topic/**` / `/innov/**` / `/metrics/**`。
3. 数据血缘（D9）：界面每个统计指标旁 ⓘ 触发 MetricSpecCard，需 Java `/metrics/v1/catalog` 提供元数据"8 件套"。
4. Mock 数据标识：Wave 0 阶段 Mock 数据需 🧪 MockBadge——Java 如何透传 Mock 标记？

## 十、架构合规与治理

讨论点：
1. 10 项锁定决策（D1–D10）复核——是否有需修订项？
2. 机器可读依赖规则的 CI 校验。
3. ±10% 范围浮动铁律：当前 58 功能点基线。
4. 架构师评审机制：Epic 首任务开工前设计评审 + 里程碑签收合规评审。

## 十一、当前进度与风险

### 11.1 任务进度（task-registry 统计）
| 状态 | 数量 |
|---|---|
| done | 85 |
| blocked | 26 |
| backlog | 16 |
| review | 15 |
| in_progress | 11 |
| claimed | 9 |
| ready | 8 |
| pending | 2 |
| superseded | 1 |

### 11.2 Epic 分布（Top）
- `E-ENT-SCRUM-PDR` 86（企业域 PDR 主战场）
- `E-ENT-PROTOTYPE` 16 / `E-CHAIN-PROTOTYPE` 13 / `E-POLICY-PROTOTYPE` 10（要素原型）
- `E-INNOV-M1` 11（创新监测移植）
- `E-ENT-REALDATA` 10（企业真实数据）
- `E-PLATFORM-P0` 9（平台脚手架）

### 11.3 关键风险
1. `lumen-svc-platform` 全量 CI 待建——后台 Java 交付链路最大缺口。
2. 三方数据源未就绪——Mock 先行能撑多久？数据工厂转换链路谁负责？
3. `demo-svc-topic-py` 的 ai/analytics/graph 服务未实现——专题服务后端能力空缺。
4. 26 个 blocked 任务——阻塞原因分类与解除路径。
5. D10 交互规范上线前需 PM+架构师补签——是否影响后台 API 契约稳定性？

## 建议讨论顺序

1. **一、总体拓扑** → 确认方案 A 边界与 innov/topic/display 关系
2. **三、数据架构** → ADS 契约面 + Mock 策略 + 数据工厂（后台根基）
3. **二、服务边界** → Java 模块拆分 + 网关鉴权 + Python 出口
4. **四、算法库** + **五、图谱** → Python 侧能力与 Nebula 落地
5. **六、可观测性** + **七、CI/CD** → 横切与交付闭环（含 waiver 取消时机）
6. **十一、风险** → blocked 任务与缺口优先级

---

# 第二轮：向量数据库需求分析

## 结论速览

| 维度 | 现状 | 判断 |
|---|---|---|
| **招标需求** | 招标文件多处出现"智能问答/知识库/语义检索/自然语言转化" | ✅ 业务需求已埋种子 |
| **架构基线** | `architecture-baseline.md` 当前未列入向量库；三引擎仅 MySQL/Nebula/ES | ⚠️ 架构有缺口 |
| **PigX 基座能力** | `lumen-svc-platform` 根 pom 已引入 `langchain4j 1.12.1`；PigX 原版有 `pigx-knowledge` 模块（支持 PGVector/Qdrant/Milvus/Chroma） | ✅ 技术栈已就绪 |
| **当前实现** | demo 仓与 lumen 仓均无 `knowledge`/向量模块落地；Python 算法仓无 embedding 代码 | ❌ 尚未落地 |
| **是否要用** | **建议用，但需走架构变更流程（architect + PM 评审）** | 🟡 待决策 |

## 一、招标需求里的"向量库信号"

### 1. 科技信息展示系统（72 处命中）
- **知识图谱构建**：从文本数据集自动识别实体、抽取属性、关系，构建知识网络——涉及实体消歧、合并，典型需要 embedding 做语义相似度匹配。
- **智能问答/自然语言交互**：AI 助手基于科技文献、专家、专利等数据库，融合多模态信息，"通过模型对底层数据库进行分布式查询，按用户意图调用并分析获取相关信息"——这是典型 NL2SQL + RAG 场景。
- **语义检索/精准推荐**：用户日常行为分析，主动推荐感兴趣的信息。

### 2. 科技专题服务算法库（21 处命中）
- **产业全要素图谱**：涉及实体融合、冲突识别、知识网络扩展——实体对齐常用 embedding 相似度。
- **深度分析模型**：多源异构数据采集后，进行字段映射、实体识别——语义匹配环节。

### 3. 科技服务群集-总体（153 处命中）
- **知识库协同**：知识库创建、协同编辑、文档编辑存档。
- **AI 助手**：自然语言问答，将自然语言转化为结构化查询指令。
- **人才画像/团队推荐**：基于研究内容、学术影响力的智能标签与推荐算法——embedding 语义相似度。

> 这些需求当前在 `scope-baseline.yaml` 的 58 功能点里**未单列为独立功能点**，而是作为算法能力的实现细节隐藏在 E1–E7 要素和图谱/指标里。但一旦要做"智能问答"或"语义检索"，向量库几乎是必选项。

## 二、架构基线的现状与缺口

### 当前三引擎分工（`数据库设计.md §1.1`）

| 引擎 | 产品 | 职责 |
|---|---|---|
| RDBMS | MySQL 8.0 | 维表/DWD/DWM/ADS/配置/用户态 |
| Graph | NebulaGraph 3.x | 实体关系网络、多跳子图、图算法 |
| Search | Elasticsearch 8.x | 事件/全文检索、快速筛选聚合 |

**缺口**：没有向量检索引擎。ES 8.x 虽然支持 `dense_vector` 字段类型 + kNN 搜索，但当前架构里 ES 定位是"全文检索/聚合"，未规划向量字段。

### 架构铁律的约束

`architecture-baseline.md` §2 D3 契约面 = ADS，Java 只读 ADS。如果引入向量库：
- **向量库归 Python 算法层写**（embedding 计算、灌数），与 Nebula/ES 同级。
- **Java 聚合层只读或经 Python 代理**（与 ES 当前模式一致："Java 只读或通过 Python 代理"）。
- 不得破坏"算法写、API 读"铁律。

## 三、PigX 基座已自带向量能力

`lumen-svc-platform`（基于 PigX 5.11.0 fork）的技术栈：
- **LangChain4j 1.6.0 / Spring AI 1.0.2**（根 pom 实际是 `langchain4j 1.12.1`）
- **数据库**：PostgreSQL with **pgvector** extension（PigX boot 模式默认）
- **支持向量库**：Qdrant / Milvus / Chroma / Neo4j / PGVector（工厂模式 `EmbeddingStoreFactory`）

PigX 原版有完整的 `pigx-knowledge` 模块（AI 知识库/RAG/文档解析），但当前 `lumen-svc-platform` **未移植该模块**。

> 也就是说：**技术栈的票已经买好，但还没上车。** 如果要启用向量库，最小代价路径是从 PigX 原版移植 `pigx-knowledge` 模块。

## 四、可能用到的场景（按优先级）

| 优先级 | 场景 | 需求来源 | 向量库用途 | 替代方案 |
|---|---|---|---|---|
| P1 | **智能问答 / AI 助手** | 招标总体 §3 | 文档 chunk embedding + RAG 检索 | 无（纯关键词检索体验差） |
| P1 | **语义检索**（文献/专利/专家） | 展示系统 | query embedding → kNN 召回 | ES BM25（语义能力弱） |
| P2 | **实体对齐/消歧** | 图谱构建 | 实体 embedding 相似度匹配 | 规则匹配 + 人工标注 |
| P2 | **人才/团队推荐** | E5 人才、团队推荐 | 画像 embedding 相似度 | 协同过滤 + 规则 |
| P3 | **政策/资讯智能推送** | E7 政策、用户行为 | 内容 embedding 匹配用户兴趣 | 标签匹配 |

## 五、如果要引入，该怎么走（建议路径）

### 5.1 架构变更流程（铁律要求）

根据 `00-team-constitution.mdc §6`，引入向量库属于"突破架构基线"，必须：
1. 暂停执行
2. 明确说明突破点：`数据库设计.md §1.1` 三引擎 → 四引擎
3. 要求 PM + 架构师签字批准
4. 在 handoff 中记录批准证据
5. 更新 `architecture-baseline.md`（新增 D11 或扩展 D3/D6）+ `数据库设计.md §1.1`

### 5.2 技术选型建议（供架构师评审）

| 候选 | 优势 | 劣势 | 适配度 |
|---|---|---|---|
| **PGVector** | PigX 基座原生支持；复用现有 PG 实例；运维简单 | 大规模（千万级向量）性能一般 | ⭐⭐⭐⭐ demo/中等规模首选 |
| **ES dense_vector** | 复用现有 ES 8.x；统一检索栈 | kNN 性能不如专用库 | ⭐⭐⭐ 若向量量小可复用 |
| **Milvus** | PigX 已支持；专业向量库；大规模友好 | 多一套运维 | ⭐⭐⭐ 大规模/生产首选 |
| **Qdrant** | PigX 已支持；Rust 性能好 | 新依赖 | ⭐⭐ |

**建议**：demo 阶段用 **PGVector**（零新依赖，PigX boot 模式自带），生产规模化时评估迁 **Milvus**。

### 5.3 落地位置（符合方案 A 调用链）

```
前端 → 网关 → Java 聚合（gkxlumen-topic / gkxlumen-knowledge）
                ↓ Feign /internal/*
            Python 算法库（embedding 计算 + 灌数）
                ↓ 写
            向量库（PGVector / Milvus）
```

- **Python 侧**：新增 embedding 服务（sentence-transformers / OpenAI / 智谱），写向量库。
- **Java 侧**：可选移植 `gkxlumen-knowledge`（从 PigX `pigx-knowledge`），或经 Python `/internal/vector/*` 代理检索。

## 六、建议讨论点

1. **业务优先级**：智能问答 / 语义检索 是否在本期 58 功能点的 ±10% 范围内？还是作为二期增强？
2. **架构变更**：是否走 D11 决策（向量库作为第四引擎）？还是先在 ES 上试 `dense_vector` 不改架构？
3. **模块归属**：向量检索能力放 Python `/internal/vector/*`（Java 代理）还是移植 `gkxlumen-knowledge`（Java 直读）？
4. **Embedding 模型选型**：智谱 / OpenAI / 本地 sentence-transformers？涉及成本与合规。
5. **与图谱的关系**：NebulaGraph 做关系网络，向量库做语义相似度——两者是互补还是重叠？

### 补充确认：Python 算法仓当前无向量能力

后台搜索结果（扫了 4 个 Python 仓的全部 `.py` / `requirements.txt` / `pyproject.toml`）：

| 仓 | 结果 | 说明 |
|---|---|---|
| `demo-algo-science` | 命中均为 celery 标准库误报 | 无真实 embedding/vector 代码 |
| `demo-algo-ent-analysis` | 同上误报 | 无真实 embedding/vector 代码 |
| `demo-svc-topic-py` | 无命中 | — |
| `lumen-etl-es-py` | 无命中 | — |

**进一步印证**：向量库目前是"需求侧有信号、供给侧全空白"的状态——如果要启动，需要从零搭建 Python embedding 服务 + 决定向量库选型 + 走架构变更（D11）。

---

# 第三轮：四大技术栈应用场景全景图

> **技术栈**：ES（Elasticsearch 检索/聚合）· 图技术（NebulaGraph 关系网络/图算法）· RAG（向量检索 + 大模型生成）· 算法（指标计算/深度模型/预测仿真/推荐匹配）
>
> **招标依据**：`智能服务集群-完整.md`（425K 字）+ `科技专题服务算法库.md`（105K 字），关键词命中：知识图谱 156、语义 107、检索 367、推荐 524、画像 152、预测 184、预警 170、相似 53、匹配 171、聚类 104、向量 17、实体 296、关系 430、路径 248、社区 33。

## 一、技术栈能力定位（先对齐边界）

| 技术栈 | 核心能力 | 招标原文信号 | 当前架构归属 |
|---|---|---|---|
| **ES** | 全文检索、结构化筛选、聚合分析、日志/事件检索 | "全文检索""分布式检索""关键词搜索""词位扩展" | ✅ 已纳入（Python 写 / Java 读或代理） |
| **图技术（NebulaGraph）** | 实体关系网络、多跳子图、路径搜索、中心度、社区发现、图算法运行时 | "路径搜索展示、中心性计算展示、社群发现展示""知识图谱""产业全要素图谱" | ✅ 已纳入（Python 灌数/查询，Java 禁直连） |
| **RAG（向量+LLM）** | 语义检索、意图理解、NL2SQL/NL2Graph、知识摘要生成、问答 | "融合语义检索与大模型解析""自然语言转化为结构化查询指令""智能问答式查询" | ❌ 未纳入架构（PigX 基座已备 langchain4j） |
| **算法（Python）** | 指标计算、深度分析模型、预测仿真、推荐匹配、NLP 实体识别、赋分评级 | "基础指标体系""深度分析模型""预测仿真""推荐匹配""NER""赋分""指数" | ✅ 已纳入（Python 算法库，写 ADS/Nebula/ES） |

## 二、独立场景（单技术栈）

### 2.1 ES 独立场景

| # | 场景 | 招标依据 | 实现要点 |
|---|---|---|---|
| ES-1 | **全文检索门户** | "全文检索""基础服务" | ES `match`/`bool` 查询论文/专利/政策/资讯 |
| ES-2 | **多维条件筛选 + 聚合** | "分类聚合、分布可视化" | ES `aggs` 按时间/地区/领域/机构分桶统计 |
| ES-3 | **关键词搜索 + 词位扩展** | "词位扩展技术抽取初始查询概念" | ES `match_phrase` + 同义词词典扩展 |
| ES-4 | **政策全文检索** | `idx_policy`（已规划） | ES 倒排索引政策全文，高亮关键词 |
| ES-5 | **日志/事件检索** | `idx_innov_event`（已规划） | 创新事件检索 + 时序聚合 |
| ES-6 | **用户行为分析** | "用户日常行为分析" | ES 聚合用户搜索/浏览/点击行为 |

### 2.2 图技术独立场景

| # | 场景 | 招标依据 | 实现要点 |
|---|---|---|---|
| G-1 | **产业全要素图谱可视化** | "产业全要素图谱""知识网络" | NebulaGraph 多跳子图 `GET SUBGRAPH`，前端 G6 渲染 |
| G-2 | **关键节点识别（中心度）** | "中心度、影响力""特征向量中心性" | NebulaGraph 图算法 `degree`/`betweenness`/`eigenvector` |
| G-3 | **路径搜索（上下游追溯）** | "路径搜索展示""关键路径" | `FIND SHORTEST PATH` / `FIND ALL PATH` |
| G-4 | **社区发现（产业集群/合作网络）** | "社群发现展示""科技社会网络" | 社区发现算法识别产业集群/学者合作圈 |
| G-5 | **技术点图谱 + 关联实体排名** | "技术点图谱""关联实体排名" | NebulaGraph + 按度中心性排序 |
| G-6 | **专家-成果关联图谱** | "专家与各类科创成果智能关联" | 专家节点 → 论文/专利/项目边，多跳查询 |
| G-7 | **产业链上下游布局** | "产业链上下游布局" | 产业链节点拓扑，层级展开 |

### 2.3 RAG 独立场景

| # | 场景 | 招标依据 | 实现要点 |
|---|---|---|---|
| R-1 | **智能问答（自然语言提问）** | "自然语言查询""智能问答式查询" | query embedding → 向量检索 → LLM 生成结构化答案 |
| R-2 | **AI 搜索（语义检索 + 大模型解析）** | "AI 搜索：融合语义检索与大模型解析" | 向量召回 + BM25 混合检索 + LLM 提炼关键信息 |
| R-3 | **报告语义检索** | "嵌入向量空间模型""报告间语义相似度" | 报告标题/摘要/关键词 embedding，余弦相似度排序 |
| R-4 | **智能阅读辅助** | "智能阅读" | 文档 chunk embedding，按段落问答 |
| R-5 | **智能问数（NL2SQL）** | "智能问数：自然语言查询、数据看板" | LLM 意图识别 → 字段映射 → 生成 SQL → 返回可视化 |
| R-6 | **政策智能解读** | "政策效果评估" | 政策文本 RAG，LLM 结构化抽取要点 |

### 2.4 算法独立场景

| # | 场景 | 招标依据 | 实现要点 |
|---|---|---|---|
| A-1 | **七要素基础指标计算** | "七类基础指标"（58 功能点中的 7） | Python ETL 算指标写 ADS，Java 只读 |
| A-2 | **企业竞争力评估模型** | "竞争力判断""优势评分" | 规则/ML 赋分，写 `ads.ent_*` |
| A-3 | **技术前沿热点识别** | "技术前沿热点识别模型" | 时序 + 聚类识别新兴技术方向 |
| A-4 | **政策效果评估模型** | "政策效果评估模型" | 指标体系 + 因果推断 |
| A-5 | **预测仿真（趋势研判）** | "预测仿真""动态预测结果" | 时序预测模型（ARIMA/Prophet/LSTM） |
| A-6 | **风险预警** | "风险预警""使用预警" | 阈值 + 异常检测 |
| A-7 | **NER 实体识别 + 关系抽取** | "NER""实体识别构建、关系抽取" | NLP 模型抽实体关系写 Nebula |
| A-8 | **区域产业指数计算** | "区域产业指数" | 加权聚合 + 标准化 |
| A-9 | **技术产业化潜力评估** | "技术产业化潜力评估" | 多因子模型 |

## 三、交叉场景（多技术栈协同）⭐

### 3.1 ES × 图技术

| # | 场景 | 协同方式 | 招标依据 |
|---|---|---|---|
| EG-1 | **图谱节点详情检索** | 图谱点击节点 → ES 检索该节点相关论文/专利/政策全文 | "知识图谱整合论文及相关学术资源" |
| EG-2 | **产业链节点下钻** | 图谱产业链节点 → ES 聚合该产业的企业数量/专利数/人才数 | "产业链上下游布局" |
| EG-3 | **关系网络 + 事件流** | Nebula 查关系拓扑 → ES 按时间线查关联事件 | "科技网络呈现" |
| EG-4 | **图算法结果回写 ES** | 社区发现/中心度结果写 ES，支持按"影响力排名"筛选 | "中心性计算展示""社群发现展示" |

### 3.2 ES × RAG

| # | 场景 | 协同方式 | 招标依据 |
|---|---|---|---|
| ER-1 | **混合检索（BM25 + 向量）** | ES 关键词召回 + 向量语义召回，RRF 融合排序 | "关键词搜索""语义检索"双通道 |
| ER-2 | **AI 搜索全链路** | ES 结构化筛选 → 向量语义召回 → LLM 提炼摘要 | "AI 搜索：融合语义检索与大模型解析" |
| ER-3 | **同义词扩展 + 语义补全** | ES 同义词词典 + 向量近义词召回 | "同义词扩展、模糊匹配及语义补全" |
| ER-4 | **政策检索 + 智能解读** | ES 全文检索政策 → RAG 对命中政策做结构化解读 | "政策全文检索""政策效果评估" |

### 3.3 图技术 × RAG

| # | 场景 | 协同方式 | 招标依据 |
|---|---|---|---|
| GR-1 | **NL2Graph（自然语言查图谱）** | LLM 解析意图 → 生成 nGQL → Nebula 查询 → LLM 组织答案 | "自然语言转化为结构化查询指令" |
| GR-2 | **图谱增强 RAG（GraphRAG）** | 向量召回文档 → 图谱扩展关联实体/关系 → LLM 综合生成 | "知识图谱与自动语义挖掘" |
| GR-3 | **专家智能问答** | "查某专家研究方向"→ 图谱查专家节点+关联成果 → RAG 生成画像摘要 | "专家与各类科创成果智能关联" |
| GR-4 | **产业链智能问答** | "深圳新能源产业链短板"→ 图谱查产业链子图 → LLM 分析瓶颈 | "瓶颈识别""路径优化" |

### 3.4 图技术 × 算法

| # | 场景 | 协同方式 | 招标依据 |
|---|---|---|---|
| GA-1 | **图算法驱动的指标计算** | Nebula 跑 PageRank/中心度 → 结果写 ADS 作为"影响力指标" | "网络密度、中心度等网络指标" |
| GA-2 | **产业集群识别** | 社区发现算法 → 聚类结果写 ADS 作为"产业集群标签" | "产业集群""社群发现" |
| GA-3 | **推荐匹配（图路径 + 评分）** | 图谱查候选集 → 算法评分排序 → 推荐结果 | "推荐匹配""协同潜力识别" |
| GA-4 | **瓶颈识别（图路径 + 指标）** | 图谱查产业链路径 → 算法计算各环节指标 → 识别短板 | "瓶颈识别""补链强链" |
| GA-5 | **合作网络分析** | 图谱构建合作网络 → 图算法 + 统计模型 → 输出核心团队/桥接节点 | "科技社会网络""超网络" |

### 3.5 ES × 算法

| # | 场景 | 协同方式 | 招标依据 |
|---|---|---|---|
| EA-1 | **聚类结果写 ES 支持筛选** | 算法做 K-means/主题聚类 → 标签写 ES → 前端按"主题"筛选 | "自动聚类及主题推荐" |
| EA-2 | **推荐结果写 ES 支持检索** | 推荐算法产出"相似企业/相似人才" → 写 ES → 搜索时附带推荐 | "智能推荐相似信息" |
| EA-3 | **指标计算 + ES 聚合校验** | 算法算指标写 ADS → ES 做独立聚合交叉验证 | "量化评估""数据校验" |

### 3.6 RAG × 算法

| # | 场景 | 协同方式 | 招标依据 |
|---|---|---|---|
| RA-1 | **智能问数（NL2SQL + 指标计算）** | LLM 生成 SQL → 触发算法计算 → 返回指标 + 可视化 | "智能问数：自然语言查询、数据看板" |
| RA-2 | **预测结果自然语言解读** | 算法产出预测数值 → LLM 生成趋势解读报告 | "动态预测结果""综合预测报告" |
| RA-3 | **评估报告自动生成** | 算法算评分/指数 → RAG 模板 + LLM 生成分析报告 | "一键生成可定制化数据报告" |

### 3.7 ES × 图 × 算法（三栈）

| # | 场景 | 协同方式 | 招标依据 |
|---|---|---|---|
| EGA-1 | **产业全景一张图** | ES 聚合产业基础数据 → 图谱展示产业链拓扑 → 算法标注优势/短板节点 | "产业全景""产业链全景" |
| EGA-2 | **科技决策分析看板** | ES 多维统计 → 图谱关系网络 → 算法预测/预警叠加 | "科技决策分析成果""多图层展示" |

### 3.8 图 × RAG × 算法（三栈）

| # | 场景 | 协同方式 | 招标依据 |
|---|---|---|---|
| GRA-1 | **战略咨询智能支持** | 图谱查产业格局 → 算法评估竞争力/瓶颈 → RAG 生成战略建议报告 | "战略咨询智能支持" |
| GRA-2 | **人才智慧服务（画像+推荐+问答）** | 图谱查人才网络 → 算法画像评分 → RAG 生成人才报告 + 智能问答 | "科技人才智慧服务""人才画像" |
| GRA-3 | **基础研究智能决策** | 图谱查技术演进路径 → 算法预测前沿 → RAG 生成决策建议 | "基础研究智能决策" |

### 3.9 全栈交叉（ES × 图 × RAG × 算法）⭐

| # | 场景 | 协同方式 | 招标依据 |
|---|---|---|---|
| ALL-1 | **AI 搜索全链路旗舰场景** | ES 关键词召回 + 向量语义召回 → 图谱扩展关联实体 → 算法重排评分 → LLM 生成结构化知识摘要 | "AI 搜索：融合语义检索与大模型解析" |
| ALL-2 | **智能科研全链条** | ES 检索文献 → 图谱构建知识网络 → 算法识别前沿/热点 → RAG 辅助阅读与问答 | "智能科研：知识管理、协作与文献处理" |
| ALL-3 | **科技专题战略分析** | ES 查专题数据 → 图谱展示七要素关系 → 算法深度分析/预测 → RAG 生成专题研究报告 | "科技专题战略分析（七要素专题）" |
| ALL-4 | **产业链深度分析 + 智能问答** | ES 聚合产业数据 → 图谱查产业链拓扑 → 算法识别瓶颈/优势 → RAG 支持自然语言问答 | "产业链深度分析模型""瓶颈识别" |

## 四、场景 × 技术栈覆盖矩阵

> ✅ = 主驱动，🔵 = 辅助参与，空白 = 不涉及

| 场景大类 | ES | 图 | RAG | 算法 | 优先级 |
|---|---|---|---|---|---|
| 全文检索/筛选 | ✅ | | | | P0 |
| 图谱可视化/关系查询 | | ✅ | | | P0 |
| 指标计算/赋分评级 | | | | ✅ | P0 |
| 实体识别/关系抽取（NLP） | | 🔵 | | ✅ | P0 |
| 产业/技术链分析 | 🔵 | ✅ | | ✅ | P1 |
| 推荐/匹配（人才/团队/企业） | 🔵 | ✅ | | ✅ | P1 |
| 预测仿真/预警 | 🔵 | 🔵 | | ✅ | P1 |
| 智能问答/NL2SQL | 🔵 | 🔵 | ✅ | 🔵 | P1-P2 |
| 语义检索/报告检索 | ✅ | | ✅ | | P2 |
| AI 搜索全链路 | ✅ | ✅ | ✅ | ✅ | P2（旗舰） |
| 战略咨询/智能决策 | 🔵 | ✅ | ✅ | ✅ | P2-P3 |
| 自动报告生成 | 🔵 | 🔵 | ✅ | ✅ | P2-P3 |

## 五、建议讨论焦点

1. **P0 已落地**：ES 检索 + NebulaGraph 图谱 + Python 指标算法——这三栈是当前架构基线已覆盖的。
2. **P1 关键交叉**：`图 × 算法`（GA-1~GA-5）是算法库的核心交付，但 `demo-svc-topic-py` 的 graph/analytics 服务未实现——最大工程缺口。
3. **P2 RAG 引入决策**：需走 D11 架构变更。智能问答/NL2SQL 是本期 58 功能点内还是二期？招标原文"智能问数""AI 搜索"已明确要求。
4. **全栈旗舰场景**：建议拆解为"分阶段交付"：先跑通 `ES + 图 + 算法` 三栈，RAG 作为增强层叠加。
5. **数据流方向对齐**：所有交叉场景都必须遵守"Python 写 / Java 读"铁律。

---

# 第四轮：典型场景数据流时序图 + 服务调用链全集

> **服务缩写**：FE=前端 · GW=`gkxlumen-gateway` · TOPIC=`gkxlumen-topic` · METRICS=`gkxlumen-metrics` · INNOV=`gkxlumen-innov` · DISP=`gkxlumen-display` · PY-ALGO=Python 算法库 · NEB=NebulaGraph · ES=Elasticsearch · VEC=向量库(PGVector/Milvus) · LLM=大模型 · ADS=MySQL ADS
>
> **铁律**：所有图遵守 `前端 → 网关 → Java 聚合（只读 ADS + Feign /internal/*）→ Python 算法库 → 存储`；Java 不写算法/不直连 nGQL；Python 不对前端暴露 REST。

## 第一组：独立场景（单技术栈）

### 场景 ES-1：全文检索门户

```mermaid
sequenceDiagram
    participant U as 用户
    participant FE as 前端
    participant GW as gkxlumen-gateway
    participant TOPIC as gkxlumen-topic
    participant PY as Python 算法库
    participant ES as Elasticsearch
    participant ADS as MySQL ADS

    U->>FE: 输入关键词'新能源汽车补贴'
    FE->>GW: GET /topic/v1/policy/search?q=新能源汽车补贴
    GW->>TOPIC: 路由 + 鉴权 + 注入 traceparent
    TOPIC->>PY: Feign GET /internal/search/policy?q=...
    PY->>ES: POST idx_policy/_search （match, highlight, size:20）
    ES-->>PY: 命中文档列表 + 高亮片段
    PY->>ADS: SELECT metric_id,name_zh FROM cfg_metric WHERE element='policy'
    ADS-->>PY: 指标元数据（8件套）
    PY-->>TOPIC: （hits:（...）, total:42, metric_spec:（...））
    TOPIC-->>GW: 200 + traceparent 回传
    GW-->>FE: JSON 响应
    FE->>U: 渲染结果列表 + i MetricSpecCard
```

**服务调用链**：`FE → GW(StripPrefix) → TOPIC(/topic/v1/policy/search) → Feign → PY(/internal/search/policy) → ES(idx_policy _search) + ADS(cfg_metric 只读)`

**数据流**：`ES 倒排索引命中 → Python 封装 + 附带指标元数据 → Java 透传 → 前端渲染`

---

### 场景 G-1：产业全要素图谱可视化

```mermaid
sequenceDiagram
    participant U as 用户
    participant FE as 前端
    participant GW as gkxlumen-gateway
    participant TOPIC as gkxlumen-topic
    participant PY as Python 算法库
    participant NEB as NebulaGraph
    participant ADS as MySQL ADS

    U->>FE: 点击'企业要素' to  展开子图
    FE->>GW: GET /topic/v1/enterprise/graph?depth=2&limit=50
    GW->>TOPIC: 路由 + traceparent
    TOPIC->>PY: Feign GET /internal/graph/enterprise?depth=2&limit=50
    PY->>NEB: USE gkx_enterprise, GET SUBGRAPH 2 STEPS FROM 'ent_001'
    NEB-->>PY: nodes:（（vid,tag,props））, edges:（（src,dst,type））
    PY->>ADS: SELECT ent_name,ent_industry FROM ads.ent_base WHERE org_uid IN （...）
    ADS-->>PY: 节点属性补充
    PY-->>TOPIC: （nodes, edges, source:'nebula'）
    TOPIC-->>GW: 200 + source 字段
    GW-->>FE: JSON
    FE->>U: G6 力导向布局渲染 + source 标签
```

**服务调用链**：`FE → GW → TOPIC(/topic/v1/enterprise/graph) → Feign → PY(/internal/graph/enterprise) → NEB(GET SUBGRAPH) + ADS(ads.ent_base 属性补充)`

**关键契约**：响应必带 `source: "nebula" | "pg" | "error"`（`graph-engine.md §2`）

---

### 场景 A-1：七要素基础指标计算（ETL 批处理）

```mermaid
sequenceDiagram
    participant CRON as 定时调度
    participant PY as Python ETL
    participant ODS as MySQL ODS
    participant DWD as MySQL DWD
    participant ADS as MySQL ADS
    participant CFG as cfg_metric

    CRON->>PY: 触发 /internal/run-pipeline E1-enterprise
    PY->>ODS: 读取企业原始数据
    PY->>PY: 清洗/去重/标准化
    PY->>DWD: 写入 dwd_ent_base_info
    PY->>PY: 指标计算（企业数量/增长率/集中度...）
    PY->>CFG: SELECT metric_id, formula_ref FROM cfg_metric WHERE element='enterprise'
    PY->>ADS: UPSERT ads.ent_scale, ads.ent_growth, ads.ent_concentration
    PY->>PY: 写入 trace_id + 计算版本 calc_version
    PY-->>CRON: pipeline status=success
```

**服务调用链**（无前端参与，纯批处理）：`CRON → PY(/internal/run-pipeline) → ODS(读) → DWD(写) → ADS(写) + CFG(读指标定义)`

**铁律**：Java 不参与此流程；ADS 由 Python 独占写

---

## 第二组：双栈交叉场景

### 场景 EG-1：图谱节点详情检索（ES × 图）

```mermaid
sequenceDiagram
    participant U as 用户
    participant FE as 前端
    participant GW as 网关
    participant TOPIC as gkxlumen-topic
    participant PY as Python
    participant NEB as NebulaGraph
    participant ES as ES

    U->>FE: 图谱中点击'专家张三'节点
    FE->>GW: GET /topic/v1/expert/detail?org_uid=expert_001
    GW->>TOPIC: 路由
    par 并行查询1: 图谱关联关系
        TOPIC->>PY: Feign /internal/graph/expert_001/relations?depth=1
        PY->>NEB: GO 1 STEP FROM 'expert_001' OVER co_author,advisor
        NEB-->>PY: 合作伙伴/师生关系边
    and 并行查询2: ES 检索成果
        TOPIC->>PY: Feign /internal/search/paper?author=张三&size=10
        PY->>ES: POST idx_paper/_search （match_author, sort:date）
        ES-->>PY: 论文列表 + 引用数
    end
    PY-->>TOPIC: （profile, relations:（...）, papers:（...））
    TOPIC-->>FE: 聚合响应
    FE->>U: 左侧画像 + 右侧关系图 + 底部论文列表
```

**服务调用链**：`FE → GW → TOPIC ├→ Feign → PY(/internal/graph/.../relations) → NEB └→ Feign → PY(/internal/search/paper) → ES → TOPIC 聚合两路结果 → FE`

---

### 场景 ER-1：混合检索 BM25 + 向量（ES × RAG）

```mermaid
sequenceDiagram
    participant U as 用户
    participant FE as 前端
    participant GW as 网关
    participant TOPIC as gkxlumen-topic
    participant PY as Python
    participant ES as ES
    participant VEC as 向量库
    participant LLM as 大模型

    U->>FE: 输入'固态电池关键技术趋势'
    FE->>GW: POST /topic/v1/tech/search （query, mode:'hybrid'）
    GW->>TOPIC: 路由
    TOPIC->>PY: Feign POST /internal/search/hybrid
    par BM25 召回
        PY->>ES: POST idx_tech/_search （match, size:50）
        ES-->>PY: 关键词命中集 A
    and 向量语义召回
        PY->>LLM: POST /embedding （input: query）
        LLM-->>PY: query_vector（768）
        PY->>VEC: kNN search vector=query_vector top_k=50
        VEC-->>PY: 语义命中集 B
    end
    PY->>PY: RRF 融合排序（A  union  B）
    PY->>LLM: POST /chat （context: top10, question: query）
    LLM-->>PY: 结构化摘要 + 关键要点
    PY-->>TOPIC: （results:（...）, summary:'...', key_points:（...））
    TOPIC-->>FE: 混合检索结果 + AI 摘要
    FE->>U: 左侧结果列表 + 右侧 AI 提炼面板
```

**服务调用链**：`FE → GW → TOPIC → Feign → PY(/internal/search/hybrid) ├→ ES(BM25 召回) ├→ LLM(embedding) → VEC(kNN 召回) └→ LLM(chat 生成摘要) → PY RRF 融合 → TOPIC → FE`

---

### 场景 GR-1：NL2Graph 自然语言查图谱（图 × RAG）⭐

```mermaid
sequenceDiagram
    participant U as 用户
    participant FE as 前端
    participant GW as 网关
    participant TOPIC as gkxlumen-topic
    participant PY as Python
    participant LLM as 大模型
    participant NEB as NebulaGraph
    participant ADS as ADS

    U->>FE: 输入'张三和哪些企业有合作关系？'
    FE->>GW: POST /topic/v1/expert/ask （question）
    GW->>TOPIC: 路由 + traceparent
    TOPIC->>PY: Feign POST /internal/nl2graph （question）
    
    PY->>LLM: POST /chat （prompt: '将问题转为nGQL', schema: gkx_enterprise）
    LLM-->>PY: （intent:'cooperation', entity:'张三', nGQL:'GO 1 STEP FROM ...'）
    
    PY->>ADS: SELECT org_uid FROM ads.ent_expert_map WHERE expert_name='张三'
    ADS-->>PY: expert_001
    
    PY->>NEB: USE gkx_enterprise, GO 1 STEP FROM 'expert_001' OVER cooperate_with
    NEB-->>PY: 合作企业节点列表 + 关系属性
    
    PY->>LLM: POST /chat （context: 图谱结果, question: 原问题）
    LLM-->>PY: '张三与企业A、企业B...有合作，主要合作领域为...'
    
    PY-->>TOPIC: （answer:'...', graph_data:（nodes,edges）, source:'nebula'）
    TOPIC-->>FE: 自然语言答案 + 关系子图
    FE->>U: 上方文字答案 + 下方图谱可视化
```

**服务调用链**：`FE → GW → TOPIC(/topic/v1/expert/ask) → Feign → PY(/internal/nl2graph) → LLM(意图识别 + nGQL 生成) → ADS(实体名→vid 映射) → NEB(执行 nGQL 查询) → LLM(结果组织为自然语言) → TOPIC → FE`

**关键点**：LLM 生成 nGQL 需在 Python 侧做语法校验 + 注入防护（禁止 DDL/DROP）

---

### 场景 GR-2：GraphRAG 图谱增强检索（图 × RAG）⭐

```mermaid
sequenceDiagram
    participant U as 用户
    participant FE as 前端
    participant GW as 网关
    participant TOPIC as gkxlumen-topic
    participant PY as Python
    participant VEC as 向量库
    participant NEB as NebulaGraph
    participant LLM as 大模型

    U->>FE: 提问'深圳新能源汽车产业链有哪些关键短板？'
    FE->>GW: POST /topic/v1/chain/ask （question）
    GW->>TOPIC: 路由
    TOPIC->>PY: Feign POST /internal/graphrag （question）
    
    PY->>LLM: POST /embedding （input: question）
    LLM-->>PY: query_vector
    PY->>VEC: kNN top_k=10  to  召回相关文档/报告 chunk
    VEC-->>PY: chunks:（（text, entity_mentions））
    
    PY->>NEB: USE gkx_industry, GET SUBGRAPH 2 STEPS FROM 识别的产业链节点
    NEB-->>PY: 产业链子图（上下游节点 + 关系）
    
    PY->>NEB: 执行图算法: 找度数低/中心度低的节点（瓶颈候选）
    NEB-->>PY: 瓶颈节点列表
    
    PY->>LLM: POST /chat （context: chunks + 子图 + 瓶颈节点, question）
    LLM-->>PY: '深圳新能源产业链在［正极材料回收］环节存在短板，仅有X家企业...'
    
    PY-->>TOPIC: （answer, graph:（nodes,edges,bottleneck_nodes）, refs:（...））
    TOPIC-->>FE: 答案 + 产业链图谱（瓶颈高亮） + 参考来源
    FE->>U: AI 分析报告 + 可交互图谱
```

**服务调用链**：`FE → GW → TOPIC → Feign → PY(/internal/graphrag) → LLM(embedding) → VEC(向量召回文档) → NEB(子图扩展 + 图算法识别瓶颈) → LLM(综合生成分析) → TOPIC → FE`

---

### 场景 GA-1：图算法驱动的指标计算（图 × 算法）

```mermaid
sequenceDiagram
    participant CRON as 定时调度
    participant PY as Python 算法库
    participant NEB as NebulaGraph
    participant ADS as MySQL ADS
    participant CFG as cfg_metric

    CRON->>PY: 触发 /internal/graph/compute-centrality
    
    PY->>CFG: SELECT metric_id,formula_ref FROM cfg_metric WHERE metric_id LIKE 'ENT_INFLUENCE percent'
    CFG-->>PY: 指标定义（影响力指数）
    
    PY->>NEB: USE gkx_enterprise, EXECUTE degree_centrality（）
    NEB-->>PY: （ent_001: 0.85, ent_002: 0.62, ...）
    
    PY->>NEB: EXECUTE betweenness_centrality（）
    NEB-->>PY: 中介中心性分数
    
    PY->>PY: 归一化加权 = 0.6*degree + 0.4*betweenness
    PY->>PY: 附加 calc_version=v1, trace_id
    
    PY->>ADS: UPSERT ads.ent_influence （org_uid, score, version）
    
    PY-->>CRON: （computed: 1200, version: v1）
```

**服务调用链**（批处理，无前端）：`CRON → PY(/internal/graph/compute-centrality) → CFG(读指标定义) → NEB(图算法) → PY(加权计算) → ADS(写指标)`

**数据流**：`NebulaGraph 图算法 → Python 后处理 → ADS 物化 → Java 只读查询`

---

### 场景 GA-3：推荐匹配——人才引进推荐（图 × 算法）

```mermaid
sequenceDiagram
    participant U as 用户
    participant FE as 前端
    participant GW as 网关
    participant TOPIC as gkxlumen-topic
    participant PY as Python
    participant NEB as NebulaGraph
    participant ADS as ADS

    U->>FE: 输入需求'机器视觉方向,副高以上,深圳'
    FE->>GW: POST /topic/v1/talent/recommend （field, level, region）
    GW->>TOPIC: 路由
    TOPIC->>PY: Feign POST /internal/recommend/talent （criteria）
    
    PY->>ADS: SELECT org_uid FROM ads.talent_profile WHERE field='CV' AND level＞=2 AND region='SZ'
    ADS-->>PY: 候选人列表（50人）
    
    PY->>NEB: USE gkx_talent, GO 1-2 STEP FROM candidates OVER co_author
    NEB-->>PY: 合作网络子图
    
    PY->>PY: 评分模型 = 0.4*学术影响力（ADS） + 0.3*合作网络中心度（Nebula） + 0.3*领域匹配度
    PY->>PY: 排序 top 10
    
    PY-->>TOPIC: （recommendations:（（uid,score,reason,graph_path））, total:50）
    TOPIC-->>FE: 推荐列表 + 每人推荐理由
    FE->>U: 推荐卡片 + 评分依据 + 查看合作网络
```

**服务调用链**：`FE → GW → TOPIC(/topic/v1/talent/recommend) → Feign → PY(/internal/recommend/talent) → ADS(候选人初筛) → NEB(合作网络扩展) → PY(评分模型排序) → TOPIC → FE`

---

### 场景 RA-1：智能问数 NL2SQL（RAG × 算法）

```mermaid
sequenceDiagram
    participant U as 用户
    participant FE as 前端
    participant GW as 网关
    participant TOPIC as gkxlumen-topic
    participant PY as Python
    participant LLM as 大模型
    participant ADS as ADS

    U->>FE: 输入'去年深圳专利申请量按区排名'
    FE->>GW: POST /topic/v1/ask （question）
    GW->>TOPIC: 路由
    TOPIC->>PY: Feign POST /internal/nl2sql （question）
    
    PY->>LLM: POST /chat （prompt:NL2SQL, schema:ads.patent_stats, examples:（））
    LLM-->>PY: SQL: 'SELECT district, COUNT（*） FROM ads.patent_stats WHERE year=2025 AND city='SZ' GROUP BY district ORDER BY count DESC'
    
    PY->>PY: SQL 安全校验（只读/白名单表/限制LIMIT）
    PY->>ADS: EXECUTE SQL
    ADS-->>PY: （（district:'南山区',count:3245）,...）
    
    PY->>LLM: POST /chat （context:结果, question:原问题）
    LLM-->>PY: '2025年深圳专利申请量南山区排名第一（3245件），其次...'
    
    PY-->>TOPIC: （answer, sql, data:（...）, chart_spec:（type:'bar',...））
    TOPIC-->>FE: 答案 + 数据表 + 图表配置
    FE->>U: 自然语言答案 + 排名柱状图 + 可下钻表格
```

**服务调用链**：`FE → GW → TOPIC(/topic/v1/ask) → Feign → PY(/internal/nl2sql) → LLM(生成SQL) → PY(SQL安全校验) → ADS(执行只读查询) → LLM(结果解读) → TOPIC → FE`

**安全铁律**：SQL 只允许 SELECT + 白名单 ADS 表 + 强制 LIMIT + 只读账号

---

## 第三组：三栈交叉场景

### 场景 EGA-1：产业全景一张图（ES × 图 × 算法）

```mermaid
sequenceDiagram
    participant U as 用户
    participant FE as 前端
    participant GW as 网关
    participant DISP as gkxlumen-display
    participant TOPIC as gkxlumen-topic
    participant PY as Python
    participant ES as ES
    participant NEB as NebulaGraph
    participant ADS as ADS

    U->>FE: 进入'新能源产业全景'页面
    FE->>GW: GET /display/v1/industry/panorama?industry=new_energy
    GW->>DISP: BFF 路由
    
    par 并行聚合1: ES 产业基础统计
        DISP->>TOPIC: Feign /topic/v1/industry/stats
        TOPIC->>PY: /internal/search/aggregate
        PY->>ES: POST idx_enterprise/_search （aggs:by_region,by_scale）
        ES-->>PY: 企业数量/规模分布
    and 并行聚合2: 图谱产业链拓扑
        DISP->>TOPIC: Feign /topic/v1/industry/graph
        TOPIC->>PY: /internal/graph/chain?industry=new_energy
        PY->>NEB: USE gkx_industry, GET SUBGRAPH FROM 'chain_new_energy'
        NEB-->>PY: 上下游节点+边
    and 并行聚合3: ADS 算法指标
        DISP->>TOPIC: Feign /topic/v1/industry/metrics
        TOPIC->>ADS: SELECT * FROM ads.ind_strength WHERE industry='new_energy'
        ADS-->>TOPIC: 优势评分/瓶颈指数/发展态势
    end
    
    DISP->>DISP: BFF 页面级拼装 （stats + graph + metrics）
    DISP-->>FE: 聚合 JSON
    FE->>U: 左侧产业链图谱 + 中央地图分布 + 右侧指标面板
```

**服务调用链**：`FE → GW → DISP(/display/v1/industry/panorama) ├→ TOPIC → PY → ES(聚合统计) ├→ TOPIC → PY → NEB(产业链子图) └→ TOPIC → ADS(算法指标只读) → DISP 聚合 → FE`

**关键点**：BFF 模式典型场景——`gkxlumen-display` 做页面级拼装，复用 `/topic` + `/metrics`，不新增 Python 直连

---

### 场景 GRA-2：人才智慧服务全链路（图 × RAG × 算法）⭐

```mermaid
sequenceDiagram
    participant U as 用户
    participant FE as 前端
    participant GW as 网关
    participant TOPIC as gkxlumen-topic
    participant PY as Python
    participant NEB as NebulaGraph
    participant VEC as 向量库
    participant ADS as ADS
    participant LLM as 大模型

    U->>FE: 点击'人才智慧服务' to  查看专家张三
    FE->>GW: GET /topic/v1/talent/profile?uid=expert_001
    GW->>TOPIC: 路由
    
    par 1. 基础画像(ADS)
        TOPIC->>ADS: SELECT * FROM ads.talent_profile WHERE org_uid='expert_001'
        ADS-->>TOPIC: 基本信息/学术指标/成果统计
    and 2. 关联图谱(Nebula)
        TOPIC->>PY: /internal/graph/expert_001?depth=2
        PY->>NEB: GET SUBGRAPH 2 STEPS FROM 'expert_001'
        NEB-->>PY: 合作网络/师生关系/项目关联
    and 3. 研究领域画像(算法+向量)
        TOPIC->>PY: /internal/talent/research-topics?uid=expert_001
        PY->>VEC: kNN search（该专家论文 embedding 聚类中心）
        VEC-->>PY: 研究主题分布
        PY->>PY: 主题建模（LDA）  to  研究方向演变时间线
    and 4. 人才评分(算法)
        TOPIC->>PY: /internal/talent/score?uid=expert_001
        PY->>ADS: 读取成果数据
        PY->>NEB: 计算合作网络中心度
        PY->>PY: 综合评分模型  to  领域权威度/学术影响力/合作活跃度
    end
    
    TOPIC->>TOPIC: 聚合画像 （basic + graph + topics + score）
    TOPIC-->>FE: 完整画像 JSON
    FE->>U: 基础画像 + 关系图谱 + 研究领域演变 + 评分雷达图
    
    Note over U,FE: 用户进一步提问
    U->>FE: '张三近年来研究重点有什么变化？'
    FE->>GW: POST /topic/v1/talent/ask （uid, question）
    GW->>TOPIC: 路由
    TOPIC->>PY: Feign /internal/graphrag/talent （uid, question）
    PY->>VEC: 检索该专家历年论文 chunk
    PY->>NEB: 查研究主题关联子图
    PY->>LLM: （context: 论文+图谱+评分, question）
    LLM-->>PY: '张三2022年前聚焦CNN，2023年起转向Transformer...'
    PY-->>TOPIC: （answer, timeline:（...）, refs:（...））
    TOPIC-->>FE: 自然语言分析 + 时间线
```

**服务调用链**（两阶段：画像加载 + 智能问答）：

阶段1 画像加载: `FE → GW → TOPIC ├→ ADS(基础画像) ├→ Feign→PY→NEB(关系图谱) ├→ Feign→PY→VEC+PY(研究领域) └→ Feign→PY→ADS+NEB+PY(评分模型) → TOPIC 聚合 → FE`

阶段2 智能问答: `FE → GW → TOPIC → Feign→PY(/internal/graphrag/talent) → VEC(论文检索) → NEB(主题子图) → LLM(综合生成) → TOPIC → FE`

---

## 第四组：全栈旗舰场景

### 场景 ALL-1：AI 搜索全链路（ES × 图 × RAG × 算法）⭐⭐⭐

```mermaid
sequenceDiagram
    participant U as 用户
    participant FE as 前端
    participant GW as gkxlumen-gateway
    participant TOPIC as gkxlumen-topic
    participant PY as Python 算法库
    participant ES as Elasticsearch
    participant VEC as 向量库
    participant NEB as NebulaGraph
    participant LLM as 大模型
    participant ADS as MySQL ADS

    U->>FE: 输入'深圳在固态电池领域的技术布局和主要竞争对手'
    FE->>GW: POST /topic/v1/ai-search （query, mode:'full'）
    GW->>TOPIC: 路由 + traceparent 注入
    TOPIC->>PY: Feign POST /internal/ai-search （query）
    
    Note over PY,LLM: 阶段1: 意图识别 + 查询规划
    PY->>LLM: POST /chat （prompt:'解析搜索意图', query）
    LLM-->>PY: （intent:'tech_landscape', entities:（'固态电池','深圳'）, sub_queries:（'固态电池技术链','深圳企业布局','竞争对手'））
    
    Note over PY,ADS: 阶段2: 多路召回（并行）
    par 2a. ES 关键词召回
        PY->>ES: POST idx_tech/_search （match:'固态电池', size:30）
        ES-->>PY: 技术文档集 A
    and 2b. 向量语义召回
        PY->>LLM: POST /embedding （input: query）
        LLM-->>PY: query_vector
        PY->>VEC: kNN top_k=30
        VEC-->>PY: 语义命中集 B
    and 2c. 图谱关联召回
        PY->>NEB: USE gkx_industry, MATCH （t:Tech）-（:belongs_to*1..2）-（c:Company） WHERE t.name= regex '固态电池'
        NEB-->>PY: 技术-企业关联子图 C
    and 2d. ADS 结构化指标
        PY->>ADS: SELECT * FROM ads.tech_stats WHERE keyword='固态电池' AND region='SZ'
        ADS-->>PY: 专利数/论文数/企业数 D
    end
    
    Note over PY,NEB: 阶段3: 算法重排 + 图谱扩展
    PY->>PY: RRF 融合 A union B  to  初步排序
    PY->>NEB: 对 top10 结果实体, GET SUBGRAPH 1 STEP  to  竞争对手扩展
    NEB-->>PY: 竞争关系子图
    PY->>PY: 算法重排: 0.5*相关性 + 0.3*影响力（图中心度） + 0.2*时效性
    
    Note over PY,LLM: 阶段4: LLM 生成结构化摘要
    PY->>LLM: POST /chat （context: top10文档+竞争子图+指标D, question: 原query, output_format: structured）
    LLM-->>PY: （summary:'深圳在固态电池领域...', key_points:（'点1','点2',...）, competitors:（（name,relation,strength））, tech_timeline:（...））
    
    PY->>PY: 组装最终响应 + metric_spec（血缘8件套） + trace_id
    PY-->>TOPIC: （results, summary, key_points, graph, metrics, refs）
    TOPIC-->>GW: 200 + traceparent 回传
    GW-->>FE: 完整 JSON
    FE->>U: AI摘要卡片 + 结果列表 + 竞争图谱 + 指标面板 + 参考来源
```

**完整服务调用链**：

```
FE → GW → TOPIC(/topic/v1/ai-search)
  → Feign → PY(/internal/ai-search)
    │
    ├─ 阶段1: LLM(意图识别 + 查询分解)
    │
    ├─ 阶段2(并行):
    │   ├─ ES(BM25 关键词召回)
    │   ├─ LLM(embedding) → VEC(向量语义召回)
    │   ├─ NEB(图谱关联召回)
    │   └─ ADS(结构化指标)
    │
    ├─ 阶段3: NEB(竞争对手子图扩展) + PY(RRF融合 + 算法重排)
    │
    └─ 阶段4: LLM(结构化摘要生成)
    │
  → PY 组装(附 metric_spec 血缘) → TOPIC → GW → FE
```

**数据流总结**：`用户自然语言 → LLM 意图分解 → [ES + 向量库 + Nebula + ADS] 四路并行召回 → 图谱扩展 + 算法重排 → LLM 综合生成 → 结构化知识摘要 + 可视化数据`

---

### 场景 ALL-3：科技专题战略分析（七要素综合）⭐⭐

```mermaid
sequenceDiagram
    participant U as 用户
    participant FE as 前端
    participant GW as 网关
    participant TOPIC as gkxlumen-topic
    participant METRICS as gkxlumen-metrics
    participant PY as Python
    participant ES as ES
    participant NEB as NebulaGraph
    participant VEC as 向量库
    participant ADS as ADS
    participant LLM as LLM

    U->>FE: 选择'新能源汽车产业'专题分析
    FE->>GW: GET /topic/v1/chain/strategic-analysis?topic=nev
    GW->>TOPIC: 路由
    
    par E1 企业要素
        TOPIC->>PY: /internal/element/enterprise?topic=nev
        PY->>ADS: ads.ent_strength
        PY->>NEB: gkx_enterprise 子图
        PY-->>TOPIC: （enterprises, graph, score）
    and E2 产业链要素
        TOPIC->>PY: /internal/element/chain?topic=nev
        PY->>NEB: gkx_industry 产业链拓扑 + 瓶颈算法
        PY-->>TOPIC: （chain_graph, bottlenecks）
    and E3 技术要素
        TOPIC->>PY: /internal/element/tech?topic=nev
        PY->>ES: idx_tech 技术热点聚合
        PY->>ADS: ads.tech_frontier
        PY-->>TOPIC: （hotspots, frontier_score）
    and E5 人才要素
        TOPIC->>PY: /internal/element/talent?topic=nev
        PY->>NEB: gkx_talent 人才网络
        PY->>ADS: ads.talent_profile
        PY-->>TOPIC: （talents, network, distribution）
    and E7 政策要素
        TOPIC->>PY: /internal/element/policy?topic=nev
        PY->>ES: idx_policy 政策检索
        PY->>ADS: ads.policy_effect
        PY-->>TOPIC: （policies, effect_score）
    end
    
    TOPIC->>METRICS: GET /metrics/v1/catalog?element in （E1,E2,E3,E5,E7）
    METRICS->>ADS: cfg_metric
    METRICS-->>TOPIC: 各要素指标8件套元数据
    
    TOPIC->>TOPIC: 七要素聚合 + 交叉分析矩阵
    
    Note over U,FE: 用户点击'生成战略分析报告'
    U->>FE: 点击'AI 生成报告'
    FE->>GW: POST /topic/v1/chain/report （topic, elements:（all））
    GW->>TOPIC: 路由
    TOPIC->>PY: Feign /internal/report/generate
    PY->>VEC: 检索历年行业报告 chunk
    PY->>LLM: （context: 七要素数据+历史报告, template:战略分析）
    LLM-->>PY: 结构化报告（产业现状/竞争格局/瓶颈/建议）
    PY-->>TOPIC: （report_md, charts_spec, refs）
    TOPIC-->>FE: 报告内容
    FE->>U: 可下载报告 + 嵌入式图表 + 数据联动
```

**服务调用链**：

```
FE → GW → TOPIC(/topic/v1/chain/strategic-analysis)
  ├─ 并行 → PY(/internal/element/{element}) × 5要素
  │   每路: ES/NEB/ADS 组合查询 + 算法计算
  ├─ → METRICS(/metrics/v1/catalog) 指标血缘
  └─ → TOPIC 聚合

报告生成:
FE → GW → TOPIC(/topic/v1/chain/report)
  → Feign → PY(/internal/report/generate)
    → VEC(历史报告检索) → LLM(报告生成)
  → TOPIC → FE
```

---

### 场景 ALL-4：产业链深度分析 + 智能问答（全栈闭环）⭐⭐

```mermaid
sequenceDiagram
    participant U as 用户
    participant FE as 前端
    participant GW as 网关
    participant TOPIC as gkxlumen-topic
    participant PY as Python
    participant ES as ES
    participant NEB as NebulaGraph
    participant VEC as 向量库
    participant ADS as ADS
    participant LLM as LLM

    U->>FE: 进入'新能源汽车产业链'深度分析页
    FE->>GW: GET /topic/v1/chain/deep-analysis?industry=nev
    GW->>TOPIC: 路由

    par 1. 产业链拓扑(Nebula)
        TOPIC->>PY: /internal/graph/chain?industry=nev&depth=3
        PY->>NEB: USE gkx_industry, GET SUBGRAPH 3 STEPS FROM 'chain_nev'
        NEB-->>PY: 上中下游节点+边
    and 2. 各环节指标(ADS)
        TOPIC->>ADS: SELECT * FROM ads.ind_strength WHERE industry='nev'
        ADS-->>TOPIC: 各环节企业数/专利数/人才数
    and 3. 瓶颈识别(图算法)
        TOPIC->>PY: /internal/graph/bottleneck?industry=nev
        PY->>NEB: 度中心性 + 中介中心性计算
        NEB-->>PY: 低中心度节点=瓶颈候选
        PY->>PY: 结合 ADS 产能数据  to  确认短板环节
    and 4. 动态资讯(ES)
        TOPIC->>PY: /internal/search/news?industry=nev&sort=date
        PY->>ES: POST idx_news/_search （match, sort:date, size:20）
        ES-->>PY: 最新产业资讯
    end

    TOPIC->>TOPIC: 聚合 （graph + metrics + bottlenecks + news）
    TOPIC-->>FE: 产业链全景数据
    FE->>U: 左侧产业链图谱（瓶颈红色标注） + 右侧指标面板 + 底部资讯流

    Note over U,FE: 用户自然语言追问
    U->>FE: '正极材料回收环节为什么是短板？有哪些改进建议？'
    FE->>GW: POST /topic/v1/chain/ask （industry, question, context:bottleneck_node）
    GW->>TOPIC: 路由
    TOPIC->>PY: Feign /internal/graphrag/chain （question, node:'cathode_recycle'）

    PY->>VEC: kNN 检索回收技术相关报告/论文 chunk
    VEC-->>PY: 相关文档集
    PY->>NEB: USE gkx_industry, GO 1 STEP FROM 'cathode_recycle' OVER supply_to
    NEB-->>PY: 该环节上下游关联节点
    PY->>ADS: SELECT * FROM ads.ind_strength WHERE node='cathode_recycle'
    ADS-->>PY: 该环节量化指标（企业数仅2家/专利数15/人才数8）
    PY->>LLM: POST /chat （context: 文档+子图+指标, question）
    LLM-->>PY: '该环节仅有2家企业，技术专利数远低于上游（正极材料87件），且缺乏专门研究机构...建议：1.引进XX方向团队 2.设立专项基金...'

    PY-->>TOPIC: （answer, evidence:（graph, metrics, docs）, suggestions:（...））
    TOPIC-->>FE: 答案 + 证据链 + 建议
    FE->>U: AI 分析卡片 + 可展开证据（图谱/指标/文献） + 行动建议
```

**服务调用链**（两阶段：分析加载 + 闭环问答）：

```
阶段1 分析加载:
FE → GW → TOPIC(/topic/v1/chain/deep-analysis)
  ├→ Feign→PY→NEB(产业链拓扑)
  ├→ ADS(各环节指标)
  ├→ Feign→PY→NEB+ADS(瓶颈识别算法)
  └→ Feign→PY→ES(动态资讯)
  → TOPIC 聚合 → FE

阶段2 闭环问答:
FE → GW → TOPIC(/topic/v1/chain/ask)
  → Feign → PY(/internal/graphrag/chain)
    → VEC(文档召回) → NEB(子图扩展) → ADS(指标佐证) → LLM(综合生成)
  → TOPIC → FE
```

**全栈协同要点**：ES 提供资讯动态 → Nebula 提供拓扑与瓶颈 → 算法做指标与识别 → RAG 补全语义与建议 → LLM 组织自然语言输出，四栈形成"看全局—识瓶颈—问原因—得建议"闭环

---

# 附录：速查总表与关键模式总结

## 场景 × 服务调用链 速查总表

| 场景 | 技术栈 | 调用链（缩写） | Java 是否直连存储 |
|---|---|---|---|
| ES-1 全文检索 | ES | FE→GW→TOPIC→PY→ES+ADS | ❌ 只读 ADS 经 PY 代理 ES |
| G-1 图谱可视化 | 图 | FE→GW→TOPIC→PY→NEB+ADS | ❌ |
| A-1 指标计算 | 算法 | CRON→PY→ODS/DWD/ADS+CFG | Java 不参与 |
| EG-1 节点详情 | ES+图 | FE→GW→TOPIC→(PY→NEB ∥ PY→ES) | ❌ |
| ER-1 混合检索 | ES+RAG | FE→GW→TOPIC→PY→(ES ∥ LLM→VEC)+LLM | ❌ |
| GR-1 NL2Graph | 图+RAG | FE→GW→TOPIC→PY→LLM→ADS→NEB→LLM | ❌ |
| GR-2 GraphRAG | 图+RAG | FE→GW→TOPIC→PY→LLM→VEC→NEB→LLM | ❌ |
| GA-1 图算法指标 | 图+算法 | CRON→PY→CFG→NEB→PY→ADS | Java 不参与 |
| GA-3 人才推荐 | 图+算法 | FE→GW→TOPIC→PY→ADS→NEB→PY | ❌ Java 只读 ADS |
| RA-1 NL2SQL | RAG+算法 | FE→GW→TOPIC→PY→LLM→ADS→LLM | ❌ ADS 只读 |
| EGA-1 产业全景 | ES+图+算法 | FE→GW→DISP→(TOPIC→PY→ES ∥ TOPIC→PY→NEB ∥ TOPIC→ADS) | ❌ 只读 ADS |
| GRA-2 人才画像 | 图+RAG+算法 | FE→GW→TOPIC→(ADS ∥ PY→NEB ∥ PY→VEC+PY ∥ PY→ADS+NEB)+PY→LLM | ❌ |
| ALL-1 AI搜索 | 全栈 | FE→GW→TOPIC→PY→LLM→(ES ∥ VEC ∥ NEB ∥ ADS)→PY重排→LLM | ❌ |
| ALL-3 专题战略 | 全栈 | FE→GW→TOPIC→(PY×5要素 ∥ METRICS→ADS)+PY→VEC→LLM | ❌ |
| ALL-4 链+问答 | 全栈 | FE→GW→TOPIC→(PY→NEB ∥ ADS ∥ PY→NEB+ADS ∥ PY→ES)+PY→VEC→NEB→ADS→LLM | ❌ |

---

## 关键模式总结

### 共性铁律（所有场景）

1. **Java（TOPIC/METRICS/DISP）永不直连** Nebula/ES/向量库/LLM——一律 Feign 调 Python `/internal/*`
2. Java 唯一直读的存储是 **MySQL ADS + app_user**（D3 契约面）
3. 所有跨服务调用经网关，**traceparent 全链路透传**
4. **LLM 调用一律在 Python 侧**，Java 不直接调 LLM
5. **向量库写入由 Python 独占**，Java 经 Python 代理检索

### 四种调用模式

| 模式 | 典型场景 | 特点 |
|---|---|---|
| **直通型** | ES-1, G-1 | Java 透传 Python 结果，无聚合 |
| **并行聚合型** | EG-1, EGA-1, GRA-2, ALL-3 | Java/TOPIC 并行 Feign 多路，聚合后返回 |
| **管道型** | GR-1, RA-1, ER-1 | Python 内部多步串联（LLM→存储→LLM），Java 等单次返回 |
| **全栈闭环型** | ALL-1, ALL-4 | 意图分解→多路召回→算法重排→LLM 生成，四阶段管道 |

### 架构缺口提示

当前 `gkxlumen-topic` 和 Python 算法库的 `/internal/*` 接口大多尚未实现。以上时序图中的接口路径是建议契约，落地时需 architect 评审确认后写入 `architecture-baseline.md` 服务清单。

### 分阶段交付建议

1. **Wave 0-1（P0 三栈）**：ES 检索 + NebulaGraph 图谱 + Python 指标算法——当前架构基线已覆盖
2. **Wave 2（P1 交叉）**：图 × 算法（GA-1~GA-5）——算法库核心交付，需补 `demo-svc-topic-py` graph/analytics 服务
3. **Wave 3（P2 RAG 引入）**：向量库 D11 架构变更 + LLM 接入 + RAG 场景——需 PM + 架构师签字
4. **Wave 4（P2 旗舰）**：全栈场景 ALL-1~ALL-4——在 Wave 2/3 基础上叠加，BFF 层 `gkxlumen-display` 建成

---

## 文件清单与引用

| 文档 | 路径 | 用途 |
|---|---|---|
| 架构基线 | `agent-delivery/architecture-baseline.md` | 方案 A + D1-D10 决策 |
| 范围基线 | `agent-delivery/scope-baseline.yaml` | 58 功能点 ±10% |
| 数据库设计 | `agent-delivery/数据库设计.md` | 三引擎分工 + ADS 契约面 |
| 图谱引擎 | `agent-delivery/graph-engine.md` | NebulaGraph 规范 |
| 可观测性 | `agent-delivery/observability.md` | OTel 全栈 |
| CI/CD | `agent-delivery/cicd-pipeline.md` | 发布闭环 |
| 仓库注册表 | `agent-delivery/repo-registry.yaml` | demo↔lumen 映射 |
| 任务注册表 | `agent-delivery/task-registry.yaml` | 进度跟踪 |
| 招标总体 | `agent-delivery/bid-reference/智能服务集群-完整.md` | 需求真源 |
| 算法库 | `agent-delivery/bid-reference/科技专题服务算法库.md` | 算法需求 |
| 团队公约 | `.cursor/rules/00-team-constitution.mdc` | 铁律与必读 |

---

> **本文档维护**：architect-agent；变更走 `architecture-baseline.md §8` 变更记录 + PM 知情。
> 
> **下次讨论建议**：针对某个具体场景展开 Python `/internal/*` 接口 OpenAPI schema 定义 + Java Feign client 代码骨架。

---

*导出于 2026-07-27 19:42 UTC+8 · 会话涉及 4 轮讨论 · 涵盖架构提纲 / 向量库分析 / 场景全景 / 时序图全集*
