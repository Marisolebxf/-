# Handoff：API-ENT-DICT-JAVA-L04

- **task-id**：`API-ENT-DICT-JAVA-L04`
- **执行**：`agent:api-agent`
- **监管**：`human:淮政玮`
- **认领**：`coordinator_dispatch` · `claimed_at=2026-07-29T20:25:00+08:00` → `in_progress` → **`review`**
- **性质**：实现类（`cicd: required` · `lumen-svc-platform`）
- **状态建议**：`done`（coordinator 2026-07-29T21:05 条件验收关单）
- **日期**：2026-07-29

> **Coordinator 验收纪要（2026-07-29T21:05）**：DoD 对照 handoff 通过；`lumen-svc-platform@6316e54` 已 push `origin/dev`。残差：本机未 `mvn compile`，待 CI Pipeline。已开闸 `FE-ENT-DICT-WIRE-L05`。


---

## 1. 范围与实现（对照派单 / DoD）

| DoD | 状态 | 证据 |
|-----|------|------|
| Java REST 对外暴露与 topic 契约对齐的 meta 端点（含 region-scopes） | ✅ | 新增 `POST /topic/v1/search/meta/region-scopes`；既有 filters/regions/company-types/enterprise-scales/tags 透传对齐 L02 |
| scales/listing/tags/company-types/filters 行为对齐 L02 | ✅ | DTO 补 `is_above_scale`；filters 透传 listing=`上市/未上市/退市`（Python 真源）；regions 补 `mode`/`keyword`/`has_children`/`children` |
| 仅透传/聚合，不写算法、不直连 nGQL、不绕过 Python `/internal/*` | ✅ | Feign → `/internal/gkx-search/meta/*` |
| OpenAPI/接口说明或 handoff 列出路径与样例 | ✅ | 本文件 §3 |
| 尽量可编译；CI required | ⏳ | 本机无 JDK/Maven，未本地 compile；push `origin/dev` 后由 Pipeline 验证 |
| handoff + cost 四字段 | ✅ | 本文件 §6–§7 |
| 明确不做：前端 / 全量国标 / 改 Python 算法 | ✅ | 未改 `demo-svc-topic-py` 业务；未改前端 |

**上游**：`DATA-ENT-DICT-IMPL-L02`（done）。

---

## 2. 代码变更（`lumen-svc-platform`）

| 层 | 文件 | 变更 |
|----|------|------|
| DTO | `…/api/dto/EnterpriseRegionScopeRequest.java` | **新增**（parent_code / mode / include_members） |
| DTO | `…/api/dto/EnterpriseRegionRequest.java` | 补 `mode` / `keyword` |
| DTO | `…/api/dto/EnterpriseResponseDTOs.java` | `FiltersResponse.isAboveScale`；`OptionsResponse.isAboveScale`；`RegionScopesResponse` / `RegionScopeItem` / `RegionScopeMember` / `AboveScaleOption`；`RegionItem` 补 hasChildren/children |
| Controller | `…/controller/EnterpriseOpenApiController.java` | 新增 `/search/meta/region-scopes` |
| Service | `EnterpriseOpenApiService` + `Impl` | `regionScopes` 透传 |
| Feign（下游） | `RemoteEnterprisePythonClient` | `POST /internal/gkx-search/meta/region-scopes` |
| Feign（对外） | `RemoteTopicEnterpriseService` | `POST /topic/v1/search/meta/region-scopes` |

---

## 3. 对外 REST 路径与样例

网关前缀以现网为准（通常 `/enterprise` + 服务路径）。服务内路径：

| Java 对外 | Python 下游 |
|-----------|-------------|
| `POST /topic/v1/search/meta/filters` | `/internal/gkx-search/meta/filters` |
| `POST /topic/v1/search/meta/regions` | `/internal/gkx-search/meta/regions` |
| `POST /topic/v1/search/meta/region-scopes` | `/internal/gkx-search/meta/region-scopes` |
| `POST /topic/v1/search/meta/company-types` | `/internal/gkx-search/meta/company-types` |
| `POST /topic/v1/search/meta/enterprise-scales` | `/internal/gkx-search/meta/enterprise-scales` |
| `POST /topic/v1/search/meta/tags` | `/internal/gkx-search/meta/tags` |

**region-scopes 请求样例**：

```json
{ "mode": "tree", "include_members": true }
```

**enterprise-scales 响应关键字段**（透传 Python）：

```json
{
  "items": [
    { "code": "大型", "name": "大型" },
    { "code": "中型", "name": "中型" },
    { "code": "小型", "name": "小型" },
    { "code": "微型", "name": "微型" }
  ],
  "is_above_scale": {
    "code": "is_above_scale",
    "name": "规上",
    "field": "is_above_scale",
    "combinable": true
  }
}
```

**filters**：`listing_statuses` = `["上市","未上市","退市"]`；另含 `is_above_scale`（L02）。

---

## 4. 偏离说明

无范围外实现。开放项：

1. **本机未跑 `mvn compile`**（环境无 JDK/Maven）——依赖 CI Pipeline 绿。
2. **未联调现网 Python**——契约以 L02 + `docs/API-接口文档.md` v10.2 为准；前端接线归 `FE-ENT-DICT-WIRE-L05`。
3. **listing ODS→ES 派生**归 `DATA-ENT-LISTING-SCALE-ETL-L06`，本单仅 meta 透传。

---

## 5. 验收证据

- 代码 diff：`gkxlumen-topic-enterprise` 上述文件
- 调用链：`EnterpriseOpenApiController` → `EnterpriseOpenApiServiceImpl` → `RemoteEnterprisePythonClient` → `/internal/gkx-search/meta/*`
- CI：push `origin/dev` 后查看 Pipeline（本 handoff 提交时本地无法 compile）

---

## 6. 架构合规自检

| # | 铁律 | 结果 |
|---|------|------|
| 1 | 算法只在 Python | ✅ Java 仅 Facade 透传 |
| 2 | 调用链 FE→Java→Python `/internal/*` | ✅ Feign 前缀 `/internal/gkx-search` |
| 3 | NebulaGraph | ✅ 不涉及 |
| 4 | 可观测性 | ✅ 既有服务入口；本单未改中间件 |
| 5 | CI/CD required | ⏳ push 后 Pipeline |
| 6 | demo 不 merge lumen | ✅ 只改 lumen-svc-platform |
| 7 | 共享聚合 / Java 不写算法、不直连 nGQL | ✅ |
| 8 | 数据策略 ADS/码表 | ✅ 读码经 Python |
| 9 | Design.md 前端规范 | ✅ 本单无前端 |
| 10 | 数据血缘 D9 | ✅ 字典透传；指标卡不涉及 |
| 11 | 交互规范 D10 | ✅ 本单无 UI |

---

## 7. Cost 四字段（回填 registry）

| 字段 | 值 |
|------|-----|
| `actual_tokens` | ~95000（估） |
| `model_used` | cursor-grok-4.5 |
| `actual_cost` | ~1.8（估 USD） |
| `cost_warn` | green |

---

## 8. 建议 follow-up

| ID | 内容 | Agent |
|----|------|-------|
| `FE-ENT-DICT-WIRE-L05` | RegionSelect / 规模 / 上市 UI 接线（等本单 done） | frontend |
| CI 绿确认 | coordinator 验收前确认 Pipeline | devops/coordinator |
| `DATA-ENT-LISTING-SCALE-ETL-L06` | listing/规上 ODS→ES 派生 | data |
