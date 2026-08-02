# 派单包：ENT-JAVA-ENUM-CONTRACT-L02

- **派单方**：`human:徐滕强` 已确认（2026-08-02）
- **执行 Agent**：`agent:api-agent`（实际认领人：`human:侯佳伟`）
- **监管人**：`human:徐滕强`
- **Sprint**：2026-W31
- **Epic**：`E-ENT-SCRUM-PDR`
- **性质**：实现（`cicd: required`）
- **仓**：`lumen-svc-platform`（默认 push `origin/dev`）
- **上游**：`API-ENT-ENUM-CONTRACT-L01`（Python 契约 + §25）
- **优先级**：P1
- **编排资产**：`gkx-orchestration/agent-delivery`

---

## 0. 为何现在派

Python 侧已把检索/高筛枚举与代码对齐，并新增：

- `POST /internal/gkx-search/meta/query-tree-schema`
- `/meta/filters` 扩展 `stock_types` / `supply_chain_roles` / `core_tech_tags`
- API 文档 **§25【Java Agent】枚举契约修复手册**（v16.4）
- Python 运行时枚举白名单（非法值不进 ES/SQL）

Java 门面若仍用旧枚举（`已上市`/`拟上市`、规上作规模档、`target_key`、缺 `not_in/all/exist`、无 schema 透传），前端/联调会继续踩坑。  
**本单只改 Java；禁止改 Python / 禁止并入 ENT-ES-ETL-L01。**

---

## 1. 铁律前置（违反必拒）

1. **算法只在 Python**：Java 只做 enum / DTO / Feign / Controller 透传  
2. **调用链**：前端 → Java REST → Python `/internal/gkx-search/**`  
3. **码表**：动态下拉（地区/标签等）**禁止硬编码**；走既有 meta 透传  
4. **契约真源**：只读 `docs/API-接口文档.md` **§25 + §3.1.0 + §3.1.2 + §3.6b**；不要扫 Python 源码猜值  
5. **分文件**：优先独立 Enum / Meta Feign 方法；避免无必要大范围混改既有 Controller（Convoy）  

---

## 2. 必读

| 文件 | 用途 |
|------|------|
| `repos/demo-svc-topic-py/docs/API-接口文档.md` §25 | **主真源**：枚举总表 / Feign 易错点 / meta 策略 |
| 同上 §3.1.0 | `SearchSortField` / `SearchSortOrder` |
| 同上 §3.1.1 / §3.1.2 | listing/scale/`is_above_scale` / query_tree ops+fields |
| 同上 §3.6 / §3.6b | `/meta/filters` 扩展 + `query-tree-schema` |
| `agent-handoffs/企业战略分析-ENT/API-ENT-ENUM-CONTRACT-L01.md` | 上游 Python 交接（§11） |
| `agent-handoffs/企业战略分析-ENT/ENT-JAVA-INTEGRATION-派单包.md` | 既有门面分层范式 |
| 既有 `RemoteEnterprise*Client` / Search DTO | 改枚举与 Feign 挂载点 |

---

## 3. 范围与产出

### 3.1 必须做 — 请求契约枚举（Java enum）

按 §25.2 至少落地并接到对应 Request DTO：

| 优先级 | 枚举 | 用途 |
|--------|------|------|
| P0 | `SearchSortField` / `SearchSortOrder` | 三检索 |
| P0 | `ListingStatus` / `EnterpriseScale` + `is_above_scale` | filters / query_tree（Q058/Q059） |
| P0 | `QueryTreeOp`（含 `not_in`/`all`/`exist`）/ `QueryTreeLogic` | 高筛 |
| P0 | `DistributionRegionType` | distribution（仅 `standard`/`city_cluster`） |
| P1 | `OperatingStatus` / `RiskLevel` / `StockType` / `SupplyChainRole` / `CoreTechTag` | query_tree |
| P1 | `AggregationField` / `DistributionDimension` / `RegionMetaMode` | aggs / distribution / meta |
| P1 | `NodeStage` / `KeyAnalysisBaseTag` / `KeyAnalysisMapDimension` | key-enterprise / sz-status / key-analysis |
| P2 | 响应类枚举（`SzRoleCode` / graph types / `RiskTypePath` 等） | 按现有 DTO 缺口补齐 |

非法值处理：Java 侧校验失败返回 400，或落到与 Python 相同的默认值；**禁止**把任意字符串当 ES 字段名透传。

### 3.2 必须做 — Feign / 字段纠错

| 错误 | 正确 |
|------|------|
| graph expand `target_key` | `node_key` |
| `region_type=country/province/...` | `standard` / `city_cluster` |
| `listing_status=已上市/拟上市` | `上市`/`未上市`/`退市` |
| `enterprise_scale=规上` | 四档 + `is_above_scale=true` |
| `enterprise_region` + `containsAny` | 仅 `eq`/`in` |
| 排序中文文案 | `competitiveness_score` 等四字段 |

### 3.3 必须做 — meta 透传

| Java 对外（建议沿用既有 `/topic/v1/enterprise/meta/**` 前缀） | Python |
|--------------------------------------------------------------|--------|
| `POST .../meta/query-tree-schema`（**新增**） | `/internal/gkx-search/meta/query-tree-schema` |
| `POST .../meta/filters`（**扩展响应**） | 须含 `stock_types` / `supply_chain_roles` / `core_tech_tags` |

既有 `/meta/regions` `/company-types` `/enterprise-scales` `/tags` `/region-scopes` 保持透传；本单不重做。

### 3.4 明确不做

- 改 `demo-svc-topic-py` / ETL / Mock  
- 前端高筛面板接线（另开 `FE-ENT-ADV-FILTER-WIRE`）  
- 在 Java 硬编码动态码表  
- 写评估/图谱算法  

---

## 4. DoD

1. §25.2 P0/P1 枚举已落地并接到 Request DTO（handoff 附对照表：枚举名 ↔ 字段 ↔ 接口）  
2. Feign 纠错项全部消除（`node_key` / `region_type` / listing / scale / `is_above_scale` / query_tree ops）  
3. 新增 Java → Python `query-tree-schema` 透传；`filters` DTO 含三项新数组  
4. 本地 Maven + JDK17 编译通过  
5. handoff：`agent-handoffs/企业战略分析-ENT/ENT-JAVA-ENUM-CONTRACT-L02.md`  
   含端点/枚举对照 + commit SHA + 架构合规自检 + cost 四字段  
6. push `origin/dev` 后 CI 证据写入 handoff（或登记 waiver）  

---

## 5. 派单话术（粘贴到新会话）

```markdown
/goal api-agent
身份：你是经验丰富的 Java 聚合层工程师，精通 Feign + typed DTO，禁止写算法。
任务 ID：ENT-JAVA-ENUM-CONTRACT-L02
性质：实现（cicd: required）
监管：human:徐滕强
认领人：human:侯佳伟（coordinator_dispatch；先按 gkx-task-claim-supervision 写入 claimed 后再动手）
派单包：agent-handoffs/企业战略分析-ENT/ENT-JAVA-ENUM-CONTRACT-L02-派单包.md
上游：API-ENT-ENUM-CONTRACT-L01（review/done）+ API 文档 §25（v16.4）
目标：
  1) 按 §25.2 落地请求契约 enum，接到三检索/高筛/distribution 等 Request
  2) Feign 纠错：node_key、region_type、listing/scale/is_above_scale、QueryTreeOp
  3) 透传 POST meta/query-tree-schema；filters 响应含 stock/supply/core_tech
不做：改 Python、硬编码动态码表、前端接线、ETL
DoD：见 task-registry ENT-JAVA-ENUM-CONTRACT-L02
Handoff：agent-handoffs/企业战略分析-ENT/ENT-JAVA-ENUM-CONTRACT-L02.md
仓 git：lumen-svc-platform push origin/dev；commit 含 [agent:api-agent] 或 [human:侯佳伟]
```

---

## 6. 状态机提示

1. `depends_on: [API-ENT-ENUM-CONTRACT-L01]` 未 `done` 前可先认领读 §25，但联调以 Python 已 push 为准  
2. `claimed_by=human:侯佳伟` → 开工改 `in_progress`  
3. 交卷 `review` + handoff；coordinator / 监管验收 → `done`  

---

## 7. 预估

- effort_points: 3  
- difficulty: M  
- estimated_tokens: 100_000  
