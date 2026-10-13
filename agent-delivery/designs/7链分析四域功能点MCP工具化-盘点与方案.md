# 7链分析四域功能点 MCP 工具化 — 盘点与总体技术实现方案

> 任务：`CROSS-MCP-7CHAIN-L01`（claimed_by: human:淮政玮）
> 阶段：**盘点与方案**（本文档即 DoD 第 1 项交付物；未启动编码实现）
> 日期：2026-10-13
>
> 真源：
> - 功能点：`agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md` §1.1.1.2.4.2（科技专题战略分析）
> - 术语：`agent-delivery/designs/5链分析与7要素关系网络.md`（7要素 = 5链 + 企业/科研机构两主体）
> - 后端能力：`repos/demo-algo-science/api/main.py`（/v1/chain/**）、`repos/demo-algo-ent-analysis/api/*`（/v1/policy|svc|entan|recommend|evaluation/**）
> - MCP 范式：`scripts/metric-mcp-server.mjs`（编排仓既有 stdio JSON-RPC server 模式）

---

## 1. 背景与范围

将 7 链分析（科技专题战略分析七维度）中**企业、产业链、政策、服务机构**四域的有价值功能点封装为 MCP 工具，供团队 AI agent 在 Cursor 中直接调用，把"打开浏览器点页面"的分析能力变成"agent 一句话取数"的工具能力。

**范围内**：**35 个功能点** = 五域 32 个 L6 功能点（企业 10 / 产业链 8 / 政策 3 / 服务机构 8 / 综合智能 3）+ 3 个基础维度查询（企业/产业/政策查询，数据查询 L4 域入口）；盘点、价值分级、MCP 候选工具粒度设计与总体实现方案。
**范围外**：技术链、人才链、科研机构（后续可按同范式扩展）；UI 可视化呈现类子功能（热力图/雷达图渲染——MCP 只返回结构化数据，不渲染图）。

---

## 2. 价值分级标准（Rubric）

每个功能点按三个维度打分，综合定级：

| 维度 | 高 | 中 | 低 |
|---|---|---|---|
| **决策价值** | 直接产出名单/得分/诊断结论（招商、评估、瓶颈） | 对比/趋势洞察（区域对比、时序） | 纯可视化呈现（图表渲染） |
| **可包装性** | 已有对应 `/v1` API 可直接调 | 需组合多个 API 近似 | 无后端落点 |
| **AI 友好度** | 结构化 JSON 入参/出参 | 需图数据转换（返回节点边即可） | 强依赖人工交互 |

定级：

- **P0**：决策价值高 × 已有 API —— MCP 首批必做
- **P1**：决策价值中或需组合 —— 第二批
- **P2**：低价值或无后端 —— 不进 MCP（本盘点为 0 项：四域在算法库 demo 阶段已全部有后端落点）

---

## 3. 盘点结果

### 3.1 企业分析（10 个 L6 功能点）

| # | L6 功能点 | 决策价值 | 现有后端 API（demo-algo-ent-analysis） | 定级 |
|---|---|---|---|---|
| 1 | 重点企业类型分析 | 中（筛选+地理透视） | `/v1/entan/graph` 实体筛选 + `/v1/analysis/metrics` 组合近似 | **P1** |
| 2 | 重点企业领域分布分析 | 中 | `/v1/entan/graph/intra`（实体关联拆解）组合近似 | **P1** |
| 3 | 企业技术力评估对比分析 | **高**（评分/雷达对比） | `/v1/evaluation/compute?sub_type=tech` | **P0** |
| 4 | 企业商业力评估对比分析 | **高** | `/v1/evaluation/compute?sub_type=business` | **P0** |
| 5 | 深圳企业现状分析 | 中（产业链定位+多城对标） | `/v1/ranking` + 区域筛选参数组合 | **P1** |
| 6 | 招引企业推荐分析 | **高**（招引名单+依据） | `/v1/recommend/attract` | **P0** |
| 7 | 培育企业推荐分析 | **高**（培育名单+建议） | `/v1/recommend/cultivate` | **P0** |
| 8 | 企业供应链关系分析 | **高**（多级下钻+断链风险） | `/v1/entan/graph`（ner/intra/hang/ops/{op_id}） | **P0** |
| 9 | 企业发展痛难点分析 | **高**（诊断报告+建议） | `/v1/diagnosis` | **P0** |
| 10 | 企业竞争力分析 | **高**（综合评分+短板） | `/v1/evaluation/compute?sub_type=competitiveness`、`/v1/score` | **P0** |

辅助 API：`/v1/centrality`（关键节点）、`/v1/risk`（风险）、`/v1/history`（历史轨迹）。

### 3.2 产业链分析（8 个 L6 功能点）

| # | L6 功能点 | 决策价值 | 现有后端 API（demo-algo-science /v1/chain/**） | 定级 |
|---|---|---|---|---|
| 1 | 产业链全景图谱 | **高**（结构+断点识别） | `/{chain_id}/panorama` | **P0** |
| 2 | 产业周期分析 | **高**（周期判断+拐点） | `/{chain_id}/cycle` | **P0** |
| 3 | 区域产业指数评价 | 中（多区域对比） | `/{chain_id}/region-index` | **P1** |
| 4 | 产业关键环节识别 | **高**（高价值环节标注） | `/{chain_id}/key-nodes` | **P0** |
| 5 | 产业瓶颈堵点识别 | **高**（卡脖子归因） | `/{chain_id}/bottlenecks` | **P0** |
| 6 | 深圳产业情况分析对比 | 中（多维对标） | `/{chain_id}/shenzhen`、`/sz-dist`、`/sz-elements` | **P1** |
| 7 | 深圳产业发展分析 | 中（建议+路径规划） | `/{chain_id}/roadmap`、`/recommendation` | **P1** |
| 8 | 区域产业竞争力评价 | 中（综合指数排名） | `/{chain_id}/competitiveness` | **P1** |

辅助 API：`/list`（链清单）、`/market-stats|investment-stats|enterprise-stats|institution-stats|news-stats`（五类统计）、`/global-dist|national-dist`（区域分布）、`/graph/ner|intra|hang|ops`（图谱算子）。

### 3.3 政策分析（3 个 L6 功能点 + 3 个增值 API）

| # | L6 功能点 | 决策价值 | 现有后端 API（demo-algo-ent-analysis /v1/policy/**） | 定级 |
|---|---|---|---|---|
| 1 | 政策时序分析 | **高**（密度指数+窗口期） | `/indicators?kind=timeseries` | **P0** |
| 2 | 区域政策对比 | **高**（结构化条款对比矩阵） | `/indicators` + `/analysis/{model_id}` | **P0** |
| 3 | 深圳政策现状分析 | **高**（三维框架得分） | `/indicators?kind=sz` + `/analysis/focus-one` | **P0** |
| ➕ | 政策文本解析（增值） | **高** | `/text/parse?policy_id=`（NLP 条款抽取） | **P0**（增值） |
| ➕ | 政策匹配（增值） | **高**（企业↔政策匹配） | `/match?subject_id=&subject_type=` | **P0**（增值） |
| ➕ | 政策效果推演（增值） | **高** | `/simulate?scope_code=&scenario_id=` | **P1**（增值） |

> 增值三项不在四域 L6 清单内，但后端已具备且对 AI agent 价值极高（match/simulate 是"一句话问政策"的核心），建议纳入工具面。

### 3.4 产业服务链分析（8 个 L6 功能点）

| # | L6 功能点 | 决策价值 | 现有后端 API（demo-algo-ent-analysis /v1/svc/**） | 定级 |
|---|---|---|---|---|
| 1 | 服务机构产业领域分析 | 中（广度/深度矩阵） | `/indicators`（领域覆盖） | **P1** |
| 2 | 服务机构新增趋势分析 | 中（时序+热度） | `/indicators?kind=`（趋势） | **P1** |
| 3 | 服务机构技术力评估分析 | **高**（多维评分对比） | `/models`（技术力模型） | **P0** |
| 4 | 服务链短板分析 | **高**（断链/空白识别） | `/models`（短板模型，SVC-ALGO-DESIGN-L01 已交付 10 模型） | **P0** |
| 5 | 服务链图谱分析 | **高**（关系网络+中心性） | `/graph` + `ner/intra/hang/ops` | **P0** |
| 6 | 引入服务机构推荐分析 | **高**（招引名单+理由） | `/models`（引入推荐模型） | **P0** |
| 7 | 培育服务机构推荐分析 | **高**（培育名单+建议） | `/models`（培育推荐模型） | **P0** |
| 8 | 深圳服务链现状分析 | 中（横向对标） | `/models`（深圳现状模型） | **P1** |

辅助 API：`/orgs`（机构查询）、`/probe/sample`（探针）。

### 3.5 综合智能分析（3 个 L6 功能点）

| # | L6 功能点 | 决策价值 | 现有后端 API（demo-algo-ent-analysis） | 定级 |
|---|---|---|---|---|
| 1 | 区域创新活力分析 | **高**（活力指数+排名） | `/v1/synth-metric/metric/M_SYNTH_186_1/compute`（四维等权：科技/产业/人才/政策） | **P0** |
| 2 | 区域创新要素分析 | **高**（要素禀赋+配置瓶颈） | `/v1/synth-metric/metric/M_SYNTH_190_1/compute`（类型/层次/领域三维，及其分维 187/188/189） | **P0** |
| 3 | 区域创新协同分析 | **高**（协同指数+图谱） | `/v1/synth-metric/metric/M_SYNTH_191_1/compute`（=M_SYNTH_COLLAB_INDEX）+ `/v1/comp/graph/**`（企业-机构-人才合作网络、中心性/密度） | **P0** |

辅助：`/v1/synth-metric/catalog`（23 个综合指标模型清单，口径/公式/就绪度全带）、`/v1/comp/graph/entities|relations|viz|similar`（图谱探索算子）。

**血缘衔接**：SYNTH 域 23 个指标均已在 metric-registry 注册（8 件套 + calc-logic），MCP 返回透传 `metric_id` 与就绪度字段，与 `metric-registry` MCP 的 `metric-get` 天然衔接（D9 不伪闭合）。

### 3.6 基础维度查询（数据查询 L4 域，3 个功能点 + 1 个对齐项）

> 口径说明：企业查询/产业查询/政策查询/服务机构查询属「科技专题数据查询」L4 域（智能搜索 + 查实体 + 高级筛选），**不在 A 线 v8 战略分析拆分（T01–T32）内**（coverage-fp 已明确 N/A 口径，真源 `qa/test-cases/KJZTFWXT/**/SEARCH-*/coverage-fp.md`）。但它们是 agent 高频第一步（"先查到实体，再进分析"），是 MCP 工具面的**入口层**，本方案纳入。

| # | 查询功能点 | 决策价值 | 现有落点 | 定级 |
|---|---|---|---|---|
| 1 | 企业查询（智能搜索/查企业/高级筛选，US-E1-SCH-01~08） | **高**（agent 入口：企业码/名称→实体） | 前端 `demo-ui-topic /development/search` 已建（mock + `smartParser.ts` 智能解析）；后端 `entan_graph /v1/entan/graph?entity=` 实体检索、`/v1/history` 轨迹 | **P0** |
| 2 | 产业查询（智能检索/查产业/高级筛选，现场增量辅助入口） | **高**（链名/同义词→chain_id） | 前端 `/industry-center/search` 已建；后端 `demo-algo-science /v1/chain/list`（链清单+可解释摘要源） | **P0** |
| 3 | 政策查询（政策检索，门户 `MENU_POLICY_PORTAL_SEARCH`） | **高**（政策名/领域→policy_id） | 前端 `/policy/search` 已建；后端 `/v1/policy/mock/policies`（列表/详情）、`/v1/policy/match`（按主体反查） | **P0** |
| 4 | 服务机构查询（对齐项，SVCSEARCH） | 中 | 前端 `/service-center/search` 已建；后端 `/v1/svc/orgs` + `/v1/svc/indicators` | **P1**（已由 `svc-orgs` 工具覆盖，见 §4） |

**查询类实现要点**：智能检索语义 = 后端已建检索/清单 API + 参数化筛选；前端 `smartParser` 的自然语言→筛选条件解析属 UI 层能力，MCP 场景由 agent 直接给结构化参数（`q`/`industry`/`region`/`type`），**不需要**复刻自然语言解析器。

### 3.7 汇总

| 域 | L6 功能点 | P0 | P1 | P2 | 增值 |
|---|---|---|---|---|---|
| 企业 | 10 | 7 | 3 | 0 | — |
| 产业链 | 8 | 4 | 4 | 0 | — |
| 政策 | 3 | 3 | 0 | 0 | 3（2×P0 + 1×P1） |
| 服务机构 | 8 | 5 | 3 | 0 | — |
| 综合智能 | 3 | 3 | 0 | 0 | — |
| 基础查询（L4） | 3 | 3 | 1（=svc-orgs） | 0 | — |
| **合计** | **35** | **25** | **11** | **0** | **3** |

**结论**：P0 共 19+2（增值）+3（综合智能）+3（基础查询）= **27** 个高价值点；战略分析 24 个点（四域+综合）全部有现成后端 API（纯包装层）；基础查询 3 个点后端有实体/清单落点，其中企业查询的"智能搜索"语义在 MCP 层降维为结构化筛选（agent 天然给得出参数），无新增算法开发。

---

## 4. MCP 候选工具粒度设计

**原则**（ponytail）：不按功能点一一开工具；按"一个工具覆盖一族同构 API"收敛，参数化差异。目标 **19 个工具**（3 基础查询 + 2 综合 + 4 企业 + 4 产业链 + 3 政策 + 3 服务机构）。查询工具命名 `search-*` 与分析工具 `ent-/chain-/policy-/svc-/synth-*` 分层——agent 的典型工作流是 `search-*` 拿实体 ID → 分析工具吃 ID 出结论 → `synth-*` 出区域级综合结论。

### server 名：`gkx-7chain`

| 工具名 | 覆盖功能点（定级） | 后端映射 | 关键参数 |
|---|---|---|---|
| **基础查询层（入口）** | | | |
| `search-enterprise` | 企业查询（P0，US-E1-SCH） | `GET /v1/entan/graph?entity=` + `/v1/history` | `q`（名称/代码模糊）、`industry?`、`region?`、`type?`（外企/高企/小微/上市）、`limit` |
| `search-industry` | 产业查询（P0，现场增量） | `GET /v1/chain/list` | `q`（链名/同义词，如"光刻""低空交通"）、`limit` |
| `search-policy` | 政策查询（P0，门户检索） | `GET /v1/policy/mock/policies`（分页/筛选）+ `/v1/policy/match`（按企业反查） | `q`、`level?`、`industry?`、`subject_id?`（反查模式）、`limit` |
| **综合智能域** | | | |
| `synth-index` | 区域创新活力/要素分析（2×P0） | `POST /v1/synth-metric/metric/{id}/compute`、`GET /catalog` | `index: vitality\|elements\|catalog`，`region`、`year`（活力=M_SYNTH_186_1；要素=M_SYNTH_190_1 及分维 187/188/189） |
| `synth-collab` | 区域创新协同分析（P0） | `POST /v1/synth-metric/metric/M_SYNTH_191_1/compute` + `GET /v1/comp/graph{,/viz,/metrics}` | `action: index\|graph`，`region`、`center?`、`hops` |
| **企业域** | | | |
| `ent-evaluate` | 技术力/商业力/竞争力评估（3×P0） | `POST /v1/evaluation/compute` | `enterprise_codes[]`, `sub_type: tech\|business\|competitiveness` |
| `ent-recommend` | 招引/培育推荐（2×P0） | `POST /v1/recommend/{attract\|cultivate}` | `kind: attract\|cultivate`, `industry`, `limit` |
| `ent-diagnose` | 痛难点诊断（P0）+ 现状/排名（P1 近似） | `GET /v1/diagnosis`、`/v1/ranking`、`/v1/score`、`/v1/risk` | `action: diagnose\|rank\|score\|risk`, `enterprise_code`, `region` |
| `ent-graph` | 供应链关系分析（P0）+ 类型/领域分布（2×P1 近似） | `POST /v1/entan/graph/{ner\|intra\|hang\|ops/{id}}` | `mode`, `entity`, `depth` |
| **产业链域** | | | |
| `chain-list` | 链清单（前置） | `GET /v1/chain/list` | — |
| `chain-panorama` | 全景图谱（P0） | `GET /v1/chain/{id}/panorama` | `chain_id` |
| `chain-analyze` | 周期/关键环节/瓶颈/区域指数/深圳对比/发展/竞争力（4×P0 + 4×P1） | `GET /v1/chain/{id}/{aspect}` | `chain_id`, `aspect: cycle\|key-nodes\|bottlenecks\|region-index\|shenzhen\|roadmap\|recommendation\|competitiveness` |
| `chain-stats` | 五类统计+区域分布（辅助） | `GET /v1/chain/{market\|investment\|enterprise\|institution\|news}-stats`、`/{global\|national\|sz}-dist` | `kind`, `chain_id?`, `stat_year?` |
| **政策域** | | | |
| `policy-indicators` | 时序/区域对比/深圳现状（3×P0） | `GET /v1/policy/indicators` | `kind: level\|type\|timeseries\|national\|sz\|all` |
| `policy-analysis` | 区域对比模型/聚焦分析 | `GET /v1/policy/analysis/{model_id}`、`POST /focus-one` | `model_id?`, `focus?` |
| `policy-apply` | 文本解析/匹配/推演（3×增值） | `GET /text/parse`、`/match`、`/simulate` | `action: parse\|match\|simulate`, `policy_id?`, `subject_id?`, `scope_code?` |
| **服务机构域** | | | |
| `svc-orgs` | 机构查询（辅助） | `GET /v1/svc/orgs`→`/orgs`（mock/ODS） | `q?`, `industry?`, `limit` |
| `svc-analysis` | 领域/趋势/技术力/短板/引入/培育/深圳现状（5×P0 + 3×P1） | `GET /v1/svc/indicators`、`/v1/svc/models` | `kind: indicators\|models`, `model_id?` |
| `svc-graph` | 服务链图谱（P0） | `GET /v1/svc/graph` + `POST /ner\|intra\|hang\|ops/{id}` | `mode`, `center?`, `steps` |

**不重复建设**：指标 8 件套/D1–D4 查询继续用现有 `metric-registry` MCP；任务操作用 `task-registry` MCP。`gkx-7chain` 只做查询层 + 五域分析。

**工具描述规范**：下节每条「完整描述」即该工具将来写入 MCP `description` 的正文。必须点名覆盖的 L6 功能点与 SRS 章节，写清何时调用、入参、返回、以及数据是否为 mock。返回 JSON 中带 `metric_id` 的统计数字保留字段（与 D9 血缘衔接，可再调 `metric-registry` 的 `metric-get` 取 8 件套）。

### 4.1 工具完整描述

#### `search-enterprise`（P0 · 企业查询）

按名称、统一社会信用代码或企业码检索企业，并按产业、区域、企业类型筛选，返回可进入后续分析的企业标识清单。这是企业域所有分析工具的入口：先拿到 `enterprise_code`，再交给 `ent-evaluate` / `ent-diagnose` / `ent-graph`。

- **覆盖**：数据查询 L4 · 企业查询（智能搜索 / 查企业 / 高级筛选，US-E1-SCH-01～08）。不在战略分析 L6 表内。
- **何时调用**：用户给出企业名、代码、产业或城市，需要先定位实体；或需要一份符合类型标签（外企 / 高企 / 小微 / 上市）的企业清单。
- **入参**：`q`（名称或代码，可空但与筛选至少给一项）、`industry?`、`region?`、`type?`（外企|高企|小微|上市）、`limit`（默认 20，上限 50）。
- **返回**：企业列表，每条含 `enterprise_code`、名称、区域、产业标签、企业类型；命中轨迹时附 `/v1/history` 摘要。
- **后端**：`GET /v1/entan/graph?entity=` + `GET /v1/history`。
- **边界**：前端 demo 的自然语言解析（`smartParser`）不在本工具内，调用方直接给结构化条件。当前检索是实体图近似，不是独立 search 服务；结果若带 mock 标记必须原样返回。

#### `search-industry`（P0 · 产业查询）

按产业名、产业链名、链位方向或同义词检索产业链，返回 `chain_id` 与可解释摘要，供 `chain-panorama` / `chain-analyze` 使用。

- **覆盖**：数据查询 L4 · 产业查询（智能检索 / 查产业 / 高级筛选，现场增量辅助入口，coverage-fp 口径 N/A）。
- **何时调用**：用户说「光刻」「低空交通」「集成电路」等词，需要先解析成系统内的 `chain_id`。
- **入参**：`q`（必填）、`limit`（默认 10）。
- **返回**：链列表，每条含 `chain_id`、标准名、匹配词、一句话摘要。
- **后端**：`GET /v1/chain/list`（服务端按 `q` 过滤；清单接口本身无关键词参数时由 MCP 层做包含匹配）。
- **边界**：本工具只定位链，不返回图谱、周期或瓶颈。进入全景用 `chain-panorama`。

#### `search-policy`（P0 · 政策查询）

按标题、产业、效力层级检索政策，或按企业反查其可匹配的政策，返回 `policy_id` 供 `policy-apply` / `policy-indicators` 继续使用。

- **覆盖**：数据查询 L4 · 政策查询（门户政策检索，`MENU_POLICY_PORTAL_SEARCH`）。
- **何时调用**：需要政策清单或某家企业「能申报哪些政策」；不要用它做时序密度或区域对比（那是 `policy-indicators`）。
- **入参**：`q?`、`level?`（国家|省|市）、`industry?`、`subject_id?`（给出则走反查）、`subject_type?`、`limit`（默认 20）。
- **返回**：政策列表，每条含 `policy_id`、标题、发布机关、效力层级、产业标签、发布日期；反查模式额外返回匹配分与理由。
- **后端**：列表 `GET /v1/policy/mock/policies`；反查 `GET /v1/policy/match`。
- **边界**：列表接口当前是 mock 数据面，返回必须带 `data_source=mock`，不得把 mock 政策说成已入库正式政策。

#### `synth-index`（P0 · 区域创新活力 / 要素）

计算选定区域、选定年度的创新活力指数或创新要素综合指数，并可列出综合指标模型目录。这是「总览仪表盘」的指数入口，不展开单条企业或单条链。

- **覆盖**：§1.1.1.2.4.2.8.1 区域创新活力分析；§1.1.1.2.4.2.8.2 区域创新要素分析。
- **何时调用**：问「深圳今年创新活力如何」「南山区要素禀赋强不强」「有哪些综合模型可算」。
- **入参**：`index`（`vitality` | `elements` | `catalog`）、`region?`、`year?`。`catalog` 不需要区域。`elements` 可加 `facet?`（`type` | `level` | `domain` | `composite`，默认 composite）。
- **返回**：`vitality` 返回 `M_SYNTH_186_1` 综合分及科技/产业/人才/政策四维分；`elements` 默认返回 `M_SYNTH_190_1`，分维分别对应 `M_SYNTH_187_1` / `188_1` / `189_1`；`catalog` 返回 23 个模型的 `metric_id`、中文名、口径摘要。每条分数带 `metric_id`。
- **后端**：`POST /v1/synth-metric/metric/{metric_id}/compute`（body：`region`/`year`）；目录 `GET /v1/synth-metric/catalog`。
- **边界**：缺维不补 0、不进平均（与指标公式一致）。8 件套细节不在本工具展开，需要口径时再调 `metric-get`。

#### `synth-collab`（P0 · 区域创新协同）

给出区域创新协同指数，或返回「企业—机构—人才」合作网络及其密度、中心性，用于发现高效协同集群和孤立主体。

- **覆盖**：§1.1.1.2.4.2.8.3 区域创新协同分析（关系图谱、协同度、协同效果）。
- **何时调用**：问某区域产学研协同强不强、谁是网络枢纽、合作边密不密。指数用 `action=index`，看网络用 `action=graph`。
- **入参**：`action`（`index` | `graph`）、`region`、`year?`、`center?`（图谱中心实体）、`hops?`（默认 1，上限 2）、`industry?`。
- **返回**：`index` 返回 `M_SYNTH_191_1`（与 `M_SYNTH_COLLAB_INDEX` 同核）及完整度/中心度/密度分项；`graph` 返回节点、边、密度与中心性，节点数默认截断 80。
- **后端**：`POST /v1/synth-metric/metric/M_SYNTH_191_1/compute`；图谱 `GET /v1/comp/graph`、`/viz`、`/metrics`。
- **边界**：完整度只看企业、科研机构、人才三类是否已有合作边，不含服务机构。图谱过大时截断并在返回里注明 `truncated`。

#### `ent-evaluate`（P0 · 企业技术力 / 商业力 / 竞争力）

对一批企业按同一子模型打分并横向对比，回答「技术强不强、市场赢不赢、综合竞不竞争得过」。

- **覆盖**：§1.1.1.2.4.2.3.3 企业技术力评估对比分析；§1.1.1.2.4.2.3.4 企业商业力评估对比分析；§1.1.1.2.4.2.3.10 企业竞争力分析。
- **何时调用**：已有 `enterprise_codes`（通常来自 `search-enterprise`），需要评分、排名或差距。对比至少 2 家；单家也可出分。
- **入参**：`enterprise_codes[]`（必填，1～20）、`sub_type`（`tech` | `business` | `competitiveness`）。
- **返回**：每家企业的综合分、分项得分、名次；两家及以上时附差距说明。分数字段保留模型对应的 `metric_id`（若后端带回）。
- **后端**：`POST /v1/evaluation/compute`。
- **边界**：不生成雷达图图片，只返回可画图的分项数组。权重自定义不在 M1；沿用后端默认权重。

#### `ent-recommend`（P0 · 招引 / 培育企业推荐）

按目标产业从全国库筛招引对象，或从深圳本地库筛值得培育的企业，返回带理由的名单。

- **覆盖**：§1.1.1.2.4.2.3.6 招引企业推荐分析；§1.1.1.2.4.2.3.7 培育企业推荐分析。
- **何时调用**：招商要「引进谁」，或本地扶持要「培育谁」。不要用它做单家诊断（那是 `ent-diagnose`）。
- **入参**：`kind`（`attract` | `cultivate`）、`industry`（必填）、`limit`（默认 10，上限 30）、`region?`（`attract` 默认全国，`cultivate` 固定深圳）。
- **返回**：推荐列表，每条含企业标识、名称、匹配分、核心理由、关键指标。
- **后端**：`POST /v1/recommend/attract` 或 `POST /v1/recommend/cultivate`。
- **边界**：名单是模型推荐，不是已签约或已立项对象；返回须带模型名与数据来源标记。

#### `ent-diagnose`（P0 + P1 · 痛难点 / 现状 / 排名 / 风险）

围绕单家或一组企业做诊断、排名、综合分或风险查看。一个 `action` 对应一种问题，避免把四个接口拆成四个工具。

- **覆盖**：§1.1.1.2.4.2.3.9 企业发展痛难点分析（P0）；§1.1.1.2.4.2.3.5 深圳企业现状分析、以及排名/评分/风险（P1 近似）。
- **何时调用**：问某家企业卡在哪、在同类里排第几、供应链或经营风险高不高、深圳某产业企业群相对外地如何。
- **入参**：`action`（`diagnose` | `rank` | `score` | `risk`）、`enterprise_code?`、`industry?`、`region?`（现状/排名常用 `深圳` 对标其他城市）。`diagnose`/`risk`/`score` 需要企业标识；`rank` 需要产业或区域。
- **返回**：`diagnose` 返回问题、成因、建议；`rank` 返回名次与对标指标；`score` 返回综合分；`risk` 返回风险点与等级。
- **后端**：`GET /v1/diagnosis`、`/v1/ranking`、`/v1/score`、`/v1/risk`。
- **边界**：现状分析是排名+区域筛选的组合近似，不是独立「深圳坐标系」报表接口。

#### `ent-graph`（P0 + P1 · 供应链与企业关联）

展开企业的供应、客户、合作关系，或做实体识别、链内关联、上卷与图算子，用于看供应链和断链风险；类型分布、领域分布用同一图接口近似。

- **覆盖**：§1.1.1.2.4.2.3.8 企业供应链关系分析（P0）；§1.1.1.2.4.2.3.1 重点企业类型分析、§1.1.1.2.4.2.3.2 重点企业领域分布分析（P1 近似）。
- **何时调用**：问上下游是谁、核心供应商是谁、断链风险在哪；或按类型/领域看一批企业怎么挂到产业上。
- **入参**：`mode`（`supply` | `ner` | `intra` | `hang` | `ops`）、`entity`（企业名或代码）、`depth?`（默认 1，上限 3）、`op_id?`（`mode=ops` 时必填）。
- **返回**：节点与边；`supply` 模式额外标出中心性高的供应商和风险标签。默认最多 80 个节点。
- **后端**：供应链走 `GET /v1/entan/graph`；其余 `POST /v1/entan/graph/{ner|intra|hang|ops/{op_id}}`。
- **边界**：类型分布与领域分布是图筛选近似，不是地理三级下钻地图。`depth>2` 易膨胀，默认拒绝并要求调用方显式提高上限。

#### `chain-list`（辅助 · 产业链清单）

返回系统内可分析的产业链目录。无关键词时用它浏览；有关键词时优先 `search-industry`。

- **覆盖**：产业链分析的前置清单，不单独对应某个 L6。
- **何时调用**：用户还没指定具体链，需要知道有哪些链可以选。
- **入参**：无。可选 `limit?`（默认 50）。
- **返回**：`chain_id`、名称、简要说明。
- **后端**：`GET /v1/chain/list`。
- **边界**：不返回任何分析结果。

#### `chain-panorama`（P0 · 产业链全景图谱）

返回一条产业链的环节结构、环节间连线，以及断点/缺环标记，用来判断链条是否完整。

- **覆盖**：§1.1.1.2.4.2.2.1 产业链全景图谱（结构可视化；节点下钻由返回的环节 ID 再调 `chain-analyze` 或企业查询完成）。
- **何时调用**：已有 `chain_id`，要看骨架、上下游环节、哪里断了。
- **入参**：`chain_id`（必填）。
- **返回**：环节节点、关系边、完整度判断、断点环节列表。节点默认截断 80，并标记 `truncated`。
- **后端**：`GET /v1/chain/{chain_id}/panorama`。
- **边界**：不渲染图谱。环节上的企业明细不在本工具一次返回，需要时用 `search-enterprise` 加 `industry`。

#### `chain-analyze`（P0 + P1 · 产业链八个分析视角）

对一条链按视角取分析结论：周期、关键环节、瓶颈、区域指数、深圳对比、发展路径、推荐、区域竞争力。八个 L6 共用一个工具，用 `aspect` 区分。

- **覆盖**：
  - P0：§1.1.1.2.4.2.2.2 产业周期分析（`cycle`）；§1.1.1.2.4.2.2.4 产业关键环节识别（`key-nodes`）；§1.1.1.2.4.2.2.5 产业瓶颈堵点识别（`bottlenecks`）。
  - P1：§1.1.1.2.4.2.2.3 区域产业指数评价（`region-index`）；§1.1.1.2.4.2.2.6 深圳产业情况分析对比（`shenzhen`）；§1.1.1.2.4.2.2.7 深圳产业发展分析（`roadmap`，建议路径；`recommendation` 为配套推荐）；§1.1.1.2.4.2.2.8 区域产业竞争力评价（`competitiveness`）。
- **何时调用**：已经有 `chain_id`，问题能对应到上面某一个视角。看结构用 `chain-panorama`，不要用本工具。
- **入参**：`chain_id`（必填）、`aspect`（`cycle` | `key-nodes` | `bottlenecks` | `region-index` | `shenzhen` | `roadmap` | `recommendation` | `competitiveness`）。
- **返回**：该视角的结构化结论（阶段判断、环节清单、瓶颈归因、指数、对标、路径建议或竞争力排名），并带后端返回的 `metric_id`。
- **后端**：`GET /v1/chain/{chain_id}/{aspect}`。
- **边界**：一次调用只算一个 `aspect`。周期分析若后端依赖大模型，返回里保留 `generated_by` 字段，不把生成文本改写成已核实事实。

#### `chain-stats`（辅助 · 产业链统计与分布）

按链或按年返回市场规模、投资、企业、机构、新闻等统计，以及全球/全国/深圳分布。给分析工具补数量背景，不替代 `chain-analyze`。

- **覆盖**：产业链分析的统计辅助，不单独对应 L6 决策功能。
- **何时调用**：需要「这条链有多少企业/多少投资/分布在哪」这类计数，而不是诊断或建议。
- **入参**：`kind`（`market` | `investment` | `enterprise` | `institution` | `news` | `global-dist` | `national-dist` | `sz-dist` | `sz-elements`）、`chain_id?`、`stat_year?`。
- **返回**：对应统计序列或分布桶，计数字段尽量带 `metric_id`。
- **后端**：`GET /v1/chain/{kind 对应路径}`（`market-stats`、`investment-stats`、`enterprise-stats`、`institution-stats`、`news-stats`、`global-dist`、`national-dist`、`sz-dist`、`sz-elements`）。
- **边界**：分布接口不接收 `stat_year`。空 `chain_id` 表示全量，返回前在结果里写明范围是全量。

#### `policy-indicators`（P0 · 政策时序 / 区域对比 / 深圳现状）

按产业或技术领域给出政策密度、区域对比矩阵或深圳政策现状得分，回答「政策窗口在哪、各地差在哪、深圳强不强」。

- **覆盖**：§1.1.1.2.4.2.6.1 政策时序分析；§1.1.1.2.4.2.6.2 区域政策对比；§1.1.1.2.4.2.6.3 深圳政策现状分析。
- **何时调用**：已确定产业/技术方向，要趋势或对比，而不是要某一份政策原文（原文用 `policy-apply` 的 `parse`）。
- **入参**：`kind`（`timeseries` | `national` | `sz` | `level` | `type` | `all`）、`industry?`、`tech?`。
- **返回**：`timeseries` 返回密度指数与支持强度序列；`national` 返回区域对比指标；`sz` 返回深圳三维框架（支持力度 / 产业适配性 / 落地实效性）得分；`level`/`type` 返回结构分布。
- **后端**：`GET /v1/policy/indicators?kind=`。
- **边界**：`all` 只在调用方明确要总览时使用，默认不要一次拉全量。指标口径以返回中的 `metric_id` 为准。

#### `policy-analysis`（P1 · 政策模型与聚焦分析）

按已注册的政策分析模型输出对比结果，或对单一对象做聚焦分析。比 `policy-indicators` 更靠近模型层。

- **覆盖**：§1.1.1.2.4.2.6.2 标准化对比分析、§1.1.1.2.4.2.6.3 深圳政策对标的模型入口。
- **何时调用**：已知 `model_id`，或要把某一政策/某一区域单独算一遍。不知道模型编号时先不要调用，改用 `policy-indicators`。
- **入参**：`model_id?`、`focus?`（聚焦对象：政策 ID 或区域）、`industry?`。二者至少给一个。
- **返回**：模型得分、对比矩阵或聚焦报告结构；带模型 ID。
- **后端**：`GET /v1/policy/analysis/{model_id}`；聚焦 `POST /v1/policy/analysis/focus-one`。
- **边界**：不创建新模型、不改权重。

#### `policy-apply`（增值 · 解析 / 匹配 / 推演）

对单份政策做条款解析，或按主体匹配政策，或按范围做效果推演。三个增值能力共用一个工具。

- **覆盖**：增值，不在政策三个 L6 内：政策文本解析、政策匹配、政策效果推演。L6 清单见 §1.1.1.2.4.2.6，增值接口见 `policy_routes` 的 `/text/parse`、`/match`、`/simulate`。
- **何时调用**：已有 `policy_id` 要看条款；已有企业要看能匹配哪些政策；已有区域/情景要做推演。找政策清单仍用 `search-policy`。
- **入参**：`action`（`parse` | `match` | `simulate`）。`parse` 要 `policy_id`；`match` 要 `subject_id` 与 `subject_type`；`simulate` 要 `scope_code`，可选 `scenario_id`。均可带 `limit`。
- **返回**：`parse` 返回结构化条款；`match` 返回政策及匹配分；`simulate` 返回情景结果。推演结果标注为模型输出。
- **后端**：`GET /v1/policy/text/parse`、`/v1/policy/match`、`/v1/policy/simulate`。
- **边界**：`simulate` 不是已发生的政策效果。匹配结果与 `search-policy` 的反查同源，已有 `subject_id` 且只要清单时用 `search-policy` 即可。

#### `svc-orgs`（P1 · 服务机构查询）

按名称或产业检索服务机构，返回机构 ID，供 `svc-analysis` / `svc-graph` 使用。

- **覆盖**：数据查询 L4 · 服务机构查询（SVCSEARCH）。
- **何时调用**：用户点名机构，或要某产业下的服务机构清单。评估、短板、推荐不要用本工具。
- **入参**：`q?`、`industry?`、`limit`（默认 20）。`q` 与 `industry` 至少一项。
- **返回**：机构列表，含 `org_id`、名称、产业领域、区域。
- **后端**：`GET /v1/svc/orgs`（mock/ODS 列表）。
- **边界**：若数据面为 mock，返回带 `data_source=mock`。

#### `svc-analysis`（P0 + P1 · 服务机构分析与推荐）

按指标或按模型取出服务机构的领域覆盖、新增趋势、技术力、短板、引入推荐、培育推荐、深圳服务链现状。

- **覆盖**：
  - P0：§1.1.1.2.4.2.7.3 服务机构技术力评估；§1.1.1.2.4.2.7.4 服务链短板分析；§1.1.1.2.4.2.7.6 引入服务机构推荐；§1.1.1.2.4.2.7.7 培育服务机构推荐。
  - P1：§1.1.1.2.4.2.7.1 服务机构产业领域分析；§1.1.1.2.4.2.7.2 服务机构新增趋势；§1.1.1.2.4.2.7.8 深圳服务链现状分析。
- **何时调用**：已有产业方向或 `model_id`，要评分、短板、名单或趋势。看机构关系网用 `svc-graph`。
- **入参**：`kind`（`indicators` | `models`）、`topic?`（`field` | `trend` | `tech` | `gap` | `attract` | `cultivate` | `shenzhen`）、`industry?`、`org_ids?`、`model_id?`。`kind=models` 时 `topic` 或 `model_id` 必填。
- **返回**：指标序列，或模型得分/推荐名单/短板环节。推荐名单含理由。统计数字保留 `metric_id`。
- **后端**：`GET /v1/svc/indicators`、`GET /v1/svc/models`。
- **边界**：短板与推荐依赖 `SVC-ALGO-DESIGN-L01` 已交付的模型；模型未就绪时返回后端错误，不在 MCP 层编造名单。

#### `svc-graph`（P0 · 服务链图谱）

以服务机构为中心展开投资、合作、竞争、人才流动关系，并给出网络密度与中心性。

- **覆盖**：§1.1.1.2.4.2.7.5 服务链图谱分析（关系网络、图谱探索与统计）。
- **何时调用**：要看某家机构的生态位置、枢纽是谁、网络密不密。短板环节清单用 `svc-analysis` 的 `topic=gap`。
- **入参**：`mode`（`graph` | `ner` | `intra` | `hang` | `ops`）、`center?`、`steps?`（默认 1）、`op_id?`（`ops` 时必填）。
- **返回**：节点、边、密度、中心性；默认截断 80 个节点。
- **后端**：`GET /v1/svc/graph`；算子 `POST /v1/svc/graph/{ner|intra|hang|ops/{op_id}}`。
- **边界**：demo 阶段 svc 网关路由可能尚未同步。路由 404 时返回明确错误，不改道直连算法仓。

---

## 5. 总体技术实现方案

### 5.1 架构

```
Cursor / AI agent
   │  (stdio, JSON-RPC)
   ▼
gkx-7chain MCP server（编排仓 scripts/，Node .mjs）
   │  (HTTP fetch, 只读为主)
   ▼
Java REST 网关（demo 阶段: demo-svc-platform 网关；正式: gkxlumen-platform-gateway）
   │  (Feign/internal 路由，ALGO-GATEWAY-ROUTE-SYNC-L01 已同步 ent/policy/chain)
   ▼
Python 算法服务 /internal/*（demo-algo-science、demo-algo-ent-analysis）
```

- **调用链合规**（架构铁律 §2.2）：MCP → Java REST → Python `/internal/*`，不越层直连算法仓、不绕网关。demo 阶段 ent/policy/chain 网关路由已通；**svc 路由未见同步记录**，M1 前置补一条网关路由同步（或过渡期 MCP 直调 `/v1/svc/*` 并在配置中标注 demo-only）。
- **D12 合规**：MCP 是团队内部 AI 工具（编排仓资产），不在 lumen 生产调用链内；正式化时仅切后端地址到 `gkxlumen-*`，MCP 代码零改动。
- **可观测**：MCP server 透传 trace header（复用 Python 侧 `TraceHeaderMiddleware` 约定的 header 名）；stdout 打 JSON-RPC 日志。

### 5.2 技术选型（零新依赖）

| 项 | 选型 | 理由 |
|---|---|---|
| 运行时 | Node ≥18（本机已装，`task-registry`/`metric-registry` 同栈） | 复用 `scripts/metric-mcp-server.mjs` 成熟范式（stdio JSON-RPC ~200 行） |
| HTTP | 全局 `fetch`（Node 18 内置） | 不加 npm 依赖 |
| 协议 | MCP stdio（JSON-RPC 2.0，`initialize`/`tools/list`/`tools/call`） | 与 Cursor MCP 面板直接兼容 |
| 配置 | 环境变量：`GKX_MCP_API_BASE`（网关地址）、`GKX_MCP_TOKEN`?、`GKX_MCP_TIMEOUT_MS`（默认 30s） | 不引配置库 |

### 5.3 代码结构（最少文件）

```
scripts/
  7chain-mcp-server.mjs      # 唯一 server 文件：TOOLS 注册表 + JSON-RPC 循环 + fetch 封装（~500 行）
  7chain-mcp-selfcheck.mjs   # 唯一自检：不连后端，mock fetch 断言 19 个工具的参数校验与路由正确（ponytail 检查件）
```

单文件优先；若超 500 行再拆 `scripts/lib/7chain-lib.mjs`（工具表与 HTTP 封装）。

### 5.4 注册与配置

`.cursor/mcp.json` 增加（任务 DoD 明确要求，属授权改动）：

```json
"gkx-7chain": {
  "type": "stdio",
  "command": "node",
  "args": ["scripts/7chain-mcp-server.mjs"],
  "env": { "GKX_MCP_API_BASE": "http://<demo网关dev地址>" }
}
```

### 5.5 实施阶段

| 阶段 | 内容 | 验收 |
|---|---|---|
| **M1 最小可用** | server 骨架 + 3 个查询工具（`search-enterprise`、`search-industry`、`search-policy`）+ 11 个 P0 分析工具：`ent-evaluate`、`ent-recommend`、`ent-diagnose`、`chain-panorama`、`chain-analyze`、`policy-indicators`、`policy-apply`、`svc-analysis`、`synth-index`、`synth-collab` | 每域 ≥1 工具真实调用出结果（DoD 第 4 条）；`search-*` 三件 + 综合域两件全通；selfcheck 绿 |
| **M2 补全** | 其余工具：`ent-graph`、`chain-list`、`chain-stats`、`policy-analysis`、`svc-orgs`、`svc-graph`；svc 网关路由补同步 | 19 工具全通；tools/list 与本文档 §4.1 描述一致 |
| **M3 正式化**（可延后） | 后端切 `gkxlumen-*`；鉴权 token 接入；trace 透传验证 | 架构合规自检全 ✅ |

### 5.6 风险与边界

| 风险 | 影响 | 对策 |
|---|---|---|
| 网关鉴权未确认（demo internal 可能免鉴权） | M1 联调阻塞 | 建单时先跑 `probe/sample` 验证；需 token 则 `GKX_MCP_TOKEN` 预留位 |
| 企业查询后端无统一 search API（前端 demo 走 mock + smartParser） | `search-enterprise` 语义降维 | M1 用 `/v1/entan/graph?entity=` 实体检索近似；政策查询过渡用 `/v1/policy/mock/policies`（返回带 mock 标记，不伪闭合）；正式 search API 落地后切地址 |
| svc 域网关路由未同步 | `svc-*` 工具 404 | M1 前置小任务补路由；过渡直调 `/v1` 并标注 |
| 后端 Mock 数据（D4=mock） | 结果非真实 | 工具返回透传后端 `data_source/mock` 标记，agent 侧可见（不伪闭合） |
| 大响应（panorama 全图） | 上下文膨胀 | 统一 `limit`/`depth` 参数 + MCP 层截断（默认 80 节点，与后端一致） |

### 5.7 DoD 对照

| DoD 条 | 本方案覆盖 |
|---|---|
| 1. 功能点盘点+价值分级+工具粒度 | §3 + §4（本文档） |
| 2. MCP server 实现并注册 | §5.2–5.4 |
| 3. 架构合规（不越层） | §5.1 |
| 4. 每域 ≥1 高价值点真实调用 | §5.5 M1 验收 |
| 5. handoff + cost 回填 | M1 完成后写 `agent-handoffs/CROSS-MCP-7CHAIN-L01.md` |

---

## 6. 待拍板项（淮政玮确认）

1. **网关地址**：M1 用哪个 demo 网关 dev 地址作为 `GKX_MCP_API_BASE` 默认值？
2. **增值 API 纳入**：政策 parse/match/simulate 三个增值工具是否进 M1（建议：parse+match 进，simulate 进 M2）？
3. **M3 正式化时间点**：是否等 lumen 侧对应服务就绪后再切，还是 demo 阶段先长期用？
