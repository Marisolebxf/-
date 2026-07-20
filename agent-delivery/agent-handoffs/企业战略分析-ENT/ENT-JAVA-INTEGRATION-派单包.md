# 企业模块 Java 对接派单包（ENT-JAVA-INTEGRATION）

- **派单方**：architect-agent（架构师 AI）+ 架构师 lead（人）
- **时间**：2026-07-20
- **下游 agent**：api-agent（Java 侧实现）
- **监管人**：human:侯佳伟
- **仓库**：`lumen-svc-platform`（分支 `dev`）
- **依赖任务**：`ENT-ARCH-API-CONTRACT`（已完成，commit `0714332`）

## 1. 背景

Python 侧 `demo-svc-topic-py / gkx-search-service` 已实现 **75 个端点**（57 静态 + 18 动态风险明细），覆盖企业检索、企业详情画像、风险、企业发展概况统计、重点/明星/深圳企业、企业图谱、企业分布等全部功能。

`ENT-ARCH-API-CONTRACT`（侯佳伟）已完成 Java 门面骨架，对接了其中 **15 个端点**（search/compare/profile 基础）。

**本派单包的目标**：将剩余 **60 个端点** 全部对接到 Java 门面，按业务模块拆成 **5 个子任务**，可并行派发、独立验收。

## 2. 架构铁律提醒（执行前必读）

1. **算法只在 Python**：Java 禁止 NLP/图谱算法/模型推理
2. **调用链合规**：前端 → Java REST（`/topic/v1/enterprise/**`）→ Python Feign（`/internal/gkx-search/**`），**不可越层**
3. **Java 只读 ADS**：Java 不写算法、不直连 nGQL、不直连 ES，所有数据经 Python `/internal/*` 转发
4. **Feign 路径统一**：所有 Feign 调用路径前缀为 `/internal/gkx-search`（**注意不是 `/api`**，`ENT-ARCH-API-CONTRACT` 初版有偏离，已在 `0714332` 修正）
5. **可观测性**：Java 侧 OTel instrumentation 必加（traceId 端到端）
6. **commit 标注**：每个 commit 加 `[agent:api-agent]` 或 `[human:侯佳伟]`

## 3. 必读文件

| 文件 | 用途 |
|---|---|
| `repos/demo-svc-topic-py/docs/API-接口文档.md` | **Python 75 端点完整文档（v15.1）**，含请求/响应字段、Feign Client 示例、Mock 数据样例。**这是 Java 对接的唯一字段真源** |
| `agent-handoffs/企业战略分析-ENT/API-ENT-contract-draft.md` | `ENT-ARCH-API-CONTRACT` 的 handoff，含已对接的 15 端点说明 |
| `agent-handoffs/企业战略分析-ENT/DATA-ENT-impl-path-signoff.md` | 架构实现设计（接口分层/权限点/端点分类） |
| `repos/lumen-svc-platform/gkxlumen-topic-enterprise/.../feign/RemoteEnterprisePythonClient.java` | 已有 Feign Client 骨架，新增端点按此模式扩展 |
| `repos/lumen-svc-platform/gkxlumen-topic-enterprise/.../controller/EnterpriseOpenApiController.java` | 已有 Controller，新增端点按此模式扩展 |

## 4. 已对接清单（不重复对接）

以下 15 个端点 `ENT-ARCH-API-CONTRACT` 已完成，**本次不在范围内**：

| Java 对外路径 | Python 下游 |
|---|---|
| `/search/query` | `/enterprises` |
| `/search/suggest` | `/enterprises/suggest` |
| `/search/advanced` | `/enterprises/advanced` |
| `/recommend` | `/enterprises/recommend` |
| `/search/meta/filters` | `/meta/filters` |
| `/search/meta/regions` | `/meta/regions` |
| `/search/meta/company-types` | `/meta/company-types` |
| `/search/meta/enterprise-scales` | `/meta/enterprise-scales` |
| `/search/meta/tags` | `/meta/tags` |
| `/compare-basket/compare` | `/enterprises/compare` |
| `/profile/panorama` | `/profile` |
| `/profile/card` | `/profile/card` |
| `/profile/basic` | `/profile/basic` |
| `/profile/overview` | `/profile/overview` |
| `/profile/news` | `/profile/news` |
| `/profile/risk/summary` | `/profile/risk/summary` |

## 5. 子任务拆分

### 5.1 ENT-JAVA-PROFILE-DETAIL（企业详情明细接口对接）

- **范围**：企业详情中的工商高管、创新载体、资质、财务、专利、供应链、投资、融资、股东、招投标、竞争力、标签，共 **17 个端点**
- **Python 端点清单**：

| # | Python 下游路径 | 用途 |
|---|---|---|
| 1 | `/internal/gkx-search/profile/executives` | 主要人员 |
| 2 | `/internal/gkx-search/profile/innovation-carriers` | 创新载体 |
| 3 | `/internal/gkx-search/profile/qualifications` | 资质认证 |
| 4 | `/internal/gkx-search/profile/finance` | 财务历史 |
| 5 | `/internal/gkx-search/profile/finance/latest` | 最新财务 |
| 6 | `/internal/gkx-search/profile/finance/trend` | 财务趋势 |
| 7 | `/internal/gkx-search/profile/patent` | 专利汇总 |
| 8 | `/internal/gkx-search/profile/patent/history` | 专利历史 |
| 9 | `/internal/gkx-search/profile/supply-chain` | 供应链 |
| 10 | `/internal/gkx-search/profile/invest` | 对外投资 |
| 11 | `/internal/gkx-search/profile/shareholders` | 股东信息 |
| 12 | `/internal/gkx-search/profile/financings` | 融资历史 |
| 13 | `/internal/gkx-search/profile/financings/summary` | 融资汇总 |
| 14 | `/internal/gkx-search/profile/competitiveness` | 竞争力评分 |
| 15 | `/internal/gkx-search/profile/tags` | 企业标签 |
| 16 | `/internal/gkx-search/profile/bids` | 招投标 |
| 17 | `/internal/gkx-search/enterprises/smart` | 智能搜索（多关键词） |

- **Java 对外路径建议**：`/topic/v1/enterprise/profile/{action}`（如 `/profile/executives`、`/profile/finance`、`/profile/finance/latest` 等）；`/enterprises/smart` 映射为 `/topic/v1/enterprise/search/smart`
- **DoD**：
  - 每个端点 Feign Client + Controller + Service 三层齐全
  - 请求/响应 DTO 按 `API-接口文档.md` 字段定义 typed DTO（禁止 `R<Object>` 透传）
  - OTel span 注入 Feign header
  - 本地 Maven 编译通过
  - handoff 文档含端点对照表 + commit SHA
- **预估**：effort_points: 5, difficulty: M, estimated_tokens: 200_000

### 5.2 ENT-JAVA-RISK（风险模块 20 端点对接）

- **范围**：`/risk/all` + 18 类风险明细 + `/enterprises/aggregations`、`/enterprises/by-codes`、`/enterprises/hot`，共 **23 个端点**（风险 20 + 检索辅助 3）
- **Python 端点清单**：

| # | Python 下游路径 | 用途 |
|---|---|---|
| 1 | `/internal/gkx-search/profile/risk/all` | 全部风险分组 |
| 2-19 | `/internal/gkx-search/profile/risk/{type}` | 18 类风险明细（见下表） |
| 20 | `/internal/gkx-search/enterprises/aggregations` | 检索聚合 |
| 21 | `/internal/gkx-search/enterprises/by-codes` | 按 org_id 批量查 |
| 22 | `/internal/gkx-search/enterprises/hot` | 热门搜索词 |

**18 类风险明细路径段**（`/internal/gkx-search/profile/risk/` + 下述段）：

```
judicial-case  dishonest  executed  limit-high  lawsuit  court-filed
court-notice  court-announcement  equity-freeze  equity-pledge  zhongben
chattel-mortgage  judicial-sale  bankruptcy  abnormal  punishment  illegal  tax-punish
```

- **Java 对外路径建议**：`/topic/v1/enterprise/profile/risk/all`、`/topic/v1/enterprise/profile/risk/{type}`（18 个独立 Controller 方法，**不要**用 `@PathVariable`，每个 type 一个独立 `@PostMapping`）；检索辅助映射为 `/topic/v1/enterprise/search/aggregations`、`/search/by-codes`、`/search/hot`
- **实现要点**：18 个风险端点结构高度相似（都是 `org_id + page + size` → `{list, total, page, size, risk_type, risk_name}`），可批量生成；但每类的 `list` 内字段不同，DTO 需按 `API-接口文档.md` §7 逐一定义
- **DoD**：同 5.1；额外要求 18 个端点逐一对照 Mock 响应验证字段
- **预估**：effort_points: 8, difficulty: L, estimated_tokens: 300_000

### 5.3 ENT-JAVA-OVERVIEW-STATS（企业发展概况统计对接）

- **范围**：KPI / 产业分布 / 增长趋势 / 区域热力 / 八大未来产业 KPI / 对比 / 趋势，共 **7 个端点**
- **Python 端点清单**：

| # | Python 下游路径 | 用途 |
|---|---|---|
| 1 | `/internal/gkx-search/stats/overview/kpi` | 企业总揽 KPI |
| 2 | `/internal/gkx-search/stats/overview/industry-distribution` | 产业分布 |
| 3 | `/internal/gkx-search/stats/overview/trend` | 企业增长趋势 |
| 4 | `/internal/gkx-search/stats/overview/district-heat` | 区域热力 |
| 5 | `/internal/gkx-search/stats/overview/industry-kpi` | 八大未来产业 KPI |
| 6 | `/internal/gkx-search/stats/overview/industry-comparison` | 八大产业企业数量对比 |
| 7 | `/internal/gkx-search/stats/overview/industry-trend` | 选中产业历年趋势 |

- **Java 对外路径建议**：`/topic/v1/enterprise/stats/overview/{action}`
- **实现要点**：这些是预聚合统计接口，Python 读 DWD `enterprise_industry_summary`（含 `chain_code='ALL'` 去重行）；Java 纯转发，无业务逻辑
- **DoD**：同 5.1
- **预估**：effort_points: 3, difficulty: S, estimated_tokens: 120_000

### 5.4 ENT-JAVA-KEY-STAR-SZ（重点/明星/深圳企业模块对接）

- **范围**：重点企业 5 + 明星企业 2 + 深圳企业 4 = **11 个端点**
- **Python 端点清单**：

| # | Python 下游路径 | 用途 |
|---|---|---|
| 1 | `/internal/gkx-search/key-enterprise/kpi` | 重点企业 KPI |
| 2 | `/internal/gkx-search/key-enterprise/chain-list` | 全链重点企业（链位分组） |
| 3 | `/internal/gkx-search/key-enterprise/chain-subject-stats` | 产业链主体统计 |
| 4 | `/internal/gkx-search/key-enterprise/qualification-summary` | 资质类型摘要 |
| 5 | `/internal/gkx-search/key-enterprise/type-scale-stats` | 类型 × 国/省/市规模 |
| 6 | `/internal/gkx-search/star-enterprise/kpi` | 明星企业 KPI |
| 7 | `/internal/gkx-search/star-enterprise/list` | 明星企业列表 |
| 8 | `/internal/gkx-search/shenzhen/kpi` | 深圳 KPI |
| 9 | `/internal/gkx-search/shenzhen/growth-trend` | 深圳历年增长趋势 |
| 10 | `/internal/gkx-search/shenzhen/industry-distribution` | 深圳产业分布 |
| 11 | `/internal/gkx-search/shenzhen/key-enterprise-list` | 深圳重点企业清单 |

- **Java 对外路径建议**：`/topic/v1/enterprise/key-enterprise/{action}`、`/star-enterprise/{action}`、`/shenzhen/{action}`
- **实现要点**：`type-scale-stats` 是交叉统计表，响应结构较复杂（`type × region_level` 矩阵），DTO 需按 `API-接口文档.md` §16.5 精确定义
- **DoD**：同 5.1
- **预估**：effort_points: 5, difficulty: M, estimated_tokens: 180_000

### 5.5 ENT-JAVA-GRAPH-DIST（图谱 + 分布模块对接）

- **范围**：图谱 2 + 企业分布 1 = **3 个端点**
- **Python 端点清单**：

| # | Python 下游路径 | 用途 |
|---|---|---|
| 1 | `/internal/gkx-search/profile/graph/subgraph` | 企业关系子图 |
| 2 | `/internal/gkx-search/profile/graph/expand` | 图谱节点拓展 |
| 3 | `/internal/gkx-search/stats/distribution` | 企业地理分布（4 维度） |

- **Java 对外路径建议**：`/topic/v1/enterprise/profile/graph/{action}`、`/stats/distribution`
- **实现要点**：
  - 图谱响应含 `nodes[]` + `edges[]`，`source` 字段标识 `nebula | mock | error`，Java 需透传
  - 分布接口参数 `dimension`（global/national/regional/city）+ `region_type` + `parent_region_id`，city 维度默认 `parent_region_id=440300`（深圳）
- **DoD**：同 5.1；额外要求图谱响应的 `source` 字段不可丢弃
- **预估**：effort_points: 3, difficulty: S, estimated_tokens: 100_000

## 6. 通用 DoD（所有子任务共同）

1. Feign Client 路径前缀统一 `/internal/gkx-search`
2. 每个端点三层齐全：Controller（`/topic/v1/enterprise/**`）→ Service → Feign Client
3. 请求/响应 typed DTO（禁止 `R<Object>` 透传，按 `API-接口文档.md` 字段定义）
4. OTel instrumentation（traceId 端到端，Feign header 注入）
5. 本地 Maven + JDK17 编译通过
6. handoff 文档 `agent-handoffs/企业战略分析-ENT/{task-id}.md`，含端点对照表 + commit SHA + 架构合规自检 7 条
7. cost 四字段回填（`actual_tokens` / `model_used` / `actual_cost` / `cost_warn`）
8. commit message 标注 `[agent:api-agent]` 或 `[human:侯佳伟]`

## 7. 并行度与依赖

- 5 个子任务**互不依赖**，可全部并行派发
- 均依赖 `ENT-ARCH-API-CONTRACT`（已完成）
- 如触碰同一 Java 文件（`RemoteEnterprisePythonClient.java` / `EnterpriseOpenApiController.java`），需 Convoy 串行或分文件提交避免冲突。建议：每个子任务新增独立 Feign Client 类（如 `RemoteEnterpriseRiskClient`、`RemoteEnterpriseStatsClient`），避免单文件争用

## 8. 风险与提醒

| 风险 | 处理 |
|---|---|
| Python Mock 数据字段与生产 ES 字段有差异 | 以 `API-接口文档.md` 字段定义为准，Mock 仅用于联调 |
| 18 个风险 DTO 字段各异，易遗漏 | 逐类对照 `API-接口文档.md` §7.2-§7.19 |
| `type-scale-stats` 交叉矩阵 DTO 复杂 | 参考 Python `enterprise_key_enterprise.py` 响应样例 |
| 图谱 `source` 字段丢失 | Feign 返回类型用 `Map<String,Object>` 或专用 DTO 保留该字段 |

## 9. 验收方

- 架构合规：architect-agent（铁律 7 条）
- 字段一致性：data-agent（对照 `API-接口文档.md`）
- 状态流转：coordinator-agent（收 handoff → 更 task-registry）

---

**派单包维护**：architect-agent。如有字段疑问，先查 `API-接口文档.md`，仍不明确再提 issue 到 `客户决策清单跟踪表.md`。
