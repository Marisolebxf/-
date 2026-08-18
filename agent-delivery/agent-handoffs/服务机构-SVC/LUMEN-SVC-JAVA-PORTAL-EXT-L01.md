# LUMEN-SVC-JAVA-PORTAL-EXT-L01 · SVC Gate-1：Java 门面透传门户扩展字段

> 日期：2026-08-18  
> Task：`LUMEN-SVC-JAVA-PORTAL-EXT-L01`  
> 总控：`DEMO-SVC-ABCD-长任务总控.md` / `DEMO-SVC-FULL-底座后全量-长任务总控.md`（已授权 · human:侯佳伟）  
> 上游：`DEMO-SVC-PY-PORTAL-AGG-L01`（integration · topic-py `858af1b` · search-py job 22719）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| lock | 24h |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 探现有 Map 透传是否已够；够则不加 Feign/DTO/专用 path（YAGNI）；未跳过 D12 / 调用链铁律 |

## 范围与实现

### 调用链（已存在，本叶未改代码）

`ServicePortalFacadeController`  
→ `ServiceFacadeService.portalOverview`  
→ `ServiceFacadeServiceImpl.unwrap`（解包 Python `R` 的 `data`）  
→ `RemoteSvcPythonClient.portalOverview`  
→ `POST /internal/gkx-svc/portal/overview`（`lumen-topic-py`，禁 demo-*）

对外：服务内 `/topic/v1/service-portal/**`；网关 `/api/svc/topic/v1/service-portal/**`。

### 结论：**Map 透传已足够，无 Java diff**

| 层 | 类型 | 行为 |
|----|------|------|
| Controller | `R<Map<String, Object>>` | 原样返回 service |
| Feign | `Map<String, Object>` | JSON → Map，无 DTO 白名单 |
| unwrap | `data instanceof Map` → `R.ok(map)` | **不剥未知键** |

上游 overview 已嵌 sections：`industry_distribution` / `region_map` / `capability_rank` / `shenzhen`（及既有 `trend` / `scale_dist` / `by_service_type`）。  
Python 另有专用 `/internal/gkx-svc/portal/{industry-distribution,region-map,capability-rank,shenzhen}`；**现行 FE 不调用**。

### 专用 REST path：不加

`lumen-ui-topic` 门户薄页一律 `svcPortalOverview`：

- `ServicePortalIndustryDistribution.vue` → `data.industry_distribution`
- `ServicePortalRegionMap.vue` → `data.region_map`
- `ServicePortalCapabilityRank.vue` → overview + ranking
- `ServicePortalShenzhen.vue` → `data.shenzhen`

`SvcTopicPaths` 仅 `portalOverview` / `portalRanking`。故本叶不加 Java 四分段路由。

## 偏离说明

- 相对上游 handoff「四分段 path 待 EXT」：本叶判定 **overview 嵌段已覆盖 FE**，专用 path 延至 FE 明确需要独立请求时再开（仍只 Feign lumen-topic-py）。
- `lumen-svc-platform` working tree clean；**无 commit**（避免空提交）。

## 产物清单

| 产物 | 路径 |
|------|------|
| 本 handoff | `agent-handoffs/服务机构-SVC/LUMEN-SVC-JAVA-PORTAL-EXT-L01.md` |
| 既有门面（未改） | `gkxlumen-topic-svc/**` · `RemoteSvcPythonClient` · `ServicePortalFacadeController` |

## 验收证据

- [x] 外网冒烟 `POST http://111.198.38.90:50892/api/svc/topic/v1/service-portal/overview` → **code=0**
- [x] `data` 顶键含：`industry_distribution` / `region_map` / `capability_rank` / `shenzhen` / `trend` / `scale_dist` / `by_service_type`（另有 `kpi` / `sample` / `mock` / `gap` 等）
- [x] FE 仅 overview 消费 sections；无需专用 Java path
- [x] D12：Feign `name=lumen-topic-py`，无 demo-*

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 2 | 前端→Java→Python `/internal/*` | ✅ |
| D12 | 禁 Feign demo-* | ✅ |
| 算法 | Java 不写算法 | ✅ 只透传 |
| ponytail | 够则不加 | ✅ |

## Cost

| 字段 | 值 |
|------|-----|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~3.5 万 |
| actual_cost | 估 ~$1.50 |
| cost_warn | false |

## CI/CD

- Java 仓：无变更、无新 pipeline
- 冒烟依赖已发布：topic-py `858af1b` + topic-svc 现网 Map 门面
- 外网基址：`http://111.198.38.90:50892/api/svc/topic/v1/service-portal/**`

## 联调确认

联调通过：50892 overview 经既有 Java Map 透传完整返回门户扩展 sections；缺字段补 DTO **不必**；专用 path **不必**。下一叶：`LUMEN-SVC-FE-PORTAL-FULL-L01`（若有）可直接绑 overview 字段。
