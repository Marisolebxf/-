# ENT-JAVA-ENUM-CONTRACT-L02 交接

- **task-id**：`ENT-JAVA-ENUM-CONTRACT-L02`
- **状态**：`review`
- **执行**：`agent:api-agent`
- **监管（本机会话）**：`human:侯佳伟`
- **派单方**：`human:徐滕强`
- **仓**：`lumen-svc-platform`（`gkxlumen-topic-enterprise`）→ `origin/dev`
- **契约真源**：`demo-svc-topic-py/docs/API-接口文档.md` §25 + §3.1.0/§3.1.1/§3.1.2/§3.6/§3.6b（v16.4）
- **实施方案**：`repos/lumen-svc-platform/ENT-JAVA-ENUM-CONTRACT-L02-实施方案.md`
- **catalog**：`API-ENT-full-catalog.md` #9 扩展 + **#137** query-tree-schema

---

## 1. 范围与实现

| 项 | 结果 |
|----|------|
| §25.2 P0/P1 请求契约 enum | ✅ `api/dto/enums/*` |
| 接到 Request DTO | ✅ 三检索 sort；distribution；aggregations；regions.mode；key-analysis base_tag/map dimension；key-chain node_stage |
| Feign 纠错 | ✅ `node_key` 本已正确；`region_type` 枚举钉死；filters 纠错已上市/规上；QueryTreeOp 含 not_in/all/exist |
| `POST .../meta/query-tree-schema` | ✅ Controller + Feign + `QueryTreeSchemaResponse` |
| `/meta/filters` 扩三数组 | ✅ `stock_types` / `supply_chain_roles` / `core_tech_tags` |
| 禁止硬编码动态码表 / 算法 | ✅ 仅透传 meta |

### 1.1 枚举对照表（handoff DoD）

| Java enum | JSON 字面值 | 接到 |
|-----------|-------------|------|
| `SearchSortField` | competitiveness_score / patent_valid_count / latest_revenue / incorporation_date | Search / SmartSearch |
| `SearchSortOrder` | asc / desc | 同上 |
| `ListingStatus` | 上市/未上市/退市（已上市→上市，拟上市→未上市） | filters 纠错 + 枚举可用 |
| `EnterpriseScale` | 大型/中型/小型/微型（规上→`is_above_scale=true`） | filters 纠错 |
| `OperatingStatus` / `RiskLevel` / `StockType` / `SupplyChainRole` / `CoreTechTag` | 见 §25.2 | 枚举落地；filters 部分纠错 |
| `QueryTreeOp` | eq…exist（含 not_in/all/exist） | `SearchBizJsonSupport` 校验 |
| `QueryTreeLogic` | AND/OR | 同上 |
| `DistributionDimension` / `DistributionRegionType` | global…city / standard\|city_cluster | DistributionRequest |
| `AggregationField` | 九字段白名单 | AggregationRequest |
| `RegionMetaMode` | children/tree | RegionRequest |
| `NodeStage` | 1/2/3 | KeyChainListRequest |
| `KeyAnalysisBaseTag` / `KeyAnalysisMapDimension` | key_enterprise\|star_enterprise / province\|city\|district | key-analysis DTO |
| `ExistFlag` / `SzRoleCode` | 1\|0；upstream… | 枚举可用（P2 缺口补齐） |

非法值策略：排序/维度等与 Python 一致回退默认；query_tree 非法 op → 400；filters 非法枚举剔除或纠错。

---

## 2. 产物

| 路径 | 说明 |
|------|------|
| `…/api/dto/enums/*` | §25 契约枚举 |
| `…/api/dto/meta/QueryTreeSchemaResponse.java` | schema 响应 |
| `RemoteEnterprisePythonClient#queryTreeSchema` | Feign |
| `EnterpriseOpenApiController` `/search/meta/query-tree-schema` | 对外 |
| `SearchFilterContractSupport` / 增强 `SearchBizJsonSupport` | 纠错 + op 白名单 |
| `API-ENT-full-catalog.md` | #137 + #9 |

---

## 3. 验证

- `mvn -pl gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-api,gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-biz -am compile -DskipTests` → **通过**
- 联调依赖：Python `/meta/query-tree-schema` 已 push（`ec1ff14`）；现网需 search-py 部署后点验

---

## 4. 架构合规自检

| # | 铁律 | 结果 |
|---|------|------|
| 1 | 算法只在 Python | ✅ |
| 2 | FE→Java→Python `/internal/*` | ✅ |
| 3 | Nebula 不在本单 | ✅ N/A |
| 4 | 可观测性 | ✅ 未改观测链路 |
| 5 | CI/CD required | ✅ push `origin/dev` |
| 6 | demo2 只读 | ✅ |
| 7 | 共享聚合 / 不写算法 | ✅ |
| 8 | ADS/Mock | ✅ N/A |
| 9 | Design.md | ✅ N/A（门面） |
| 10 | 数据血缘 | ✅ N/A |

---

## 5. 偏离 / 开放项

- 上游 `API-ENT-ENUM-CONTRACT-L01` registry 可能仍为 `review`；本单按已 push 文档开工（派单允许）。
- P2 响应侧全量枚举化未做（按方案只补缺口：`SzRoleCode`/`ExistFlag`）。
- 前端高筛接线另开 `FE-ENT-ADV-FILTER-WIRE`。

---

## 6. cost

| 字段 | 值 |
|------|-----|
| `actual_tokens` | 180000 |
| `model_used` | cursor-grok-4.5 |
| `actual_cost` | 3.0 |
| `cost_warn` | green |
