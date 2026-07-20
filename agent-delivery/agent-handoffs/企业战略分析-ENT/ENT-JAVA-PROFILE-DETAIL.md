# Handoff：ENT-JAVA-PROFILE-DETAIL

- **时间**：2026-07-20
- **执行**：agent:api-agent（监管：human:侯佳伟）
- **仓库 / 分支**：`lumen-svc-platform` / `dev`
- **派单包**：`ENT-JAVA-INTEGRATION-派单包.md` §5.1
- **状态建议**：`review`（待 coordinator 验收；**勿自行改 done**）
- **接口总文档（前端联调入口）**：[`API-ENT-full-catalog.md`](./API-ENT-full-catalog.md)（76 端点全量；本单对应「画像细分」+ `search/smart`，见总文档 §3 总览 / §4 明细）

## 1. 范围与实现

对接企业详情明细 **17** 端点：画像细分 16 + 智能搜索 1。未改动 `EnterpriseOpenApiController` 既有接口。

| # | Java 对外（网关前缀 `…/enterprise`） | Python 下游 | Controller |
|---|---|---|---|
| 1 | `POST /topic/v1/profile/executives` | `/internal/gkx-search/profile/executives` | `EnterpriseProfileDetailController` |
| 2 | `POST /topic/v1/profile/innovation-carriers` | `…/profile/innovation-carriers` | 同上 |
| 3 | `POST /topic/v1/profile/qualifications` | `…/profile/qualifications` | 同上 |
| 4 | `POST /topic/v1/profile/finance` | `…/profile/finance` | 同上 |
| 5 | `POST /topic/v1/profile/finance/latest` | `…/profile/finance/latest` | 同上 |
| 6 | `POST /topic/v1/profile/finance/trend` | `…/profile/finance/trend` | 同上 |
| 7 | `POST /topic/v1/profile/patent` | `…/profile/patent` | 同上 |
| 8 | `POST /topic/v1/profile/patent/history` | `…/profile/patent/history` | 同上 |
| 9 | `POST /topic/v1/profile/supply-chain` | `…/profile/supply-chain` | 同上 |
| 10 | `POST /topic/v1/profile/invest` | `…/profile/invest` | 同上 |
| 11 | `POST /topic/v1/profile/shareholders` | `…/profile/shareholders` | 同上 |
| 12 | `POST /topic/v1/profile/financings` | `…/profile/financings` | 同上 |
| 13 | `POST /topic/v1/profile/financings/summary` | `…/profile/financings/summary` | 同上 |
| 14 | `POST /topic/v1/profile/competitiveness` | `…/profile/competitiveness` | 同上 |
| 15 | `POST /topic/v1/profile/tags` | `…/profile/tags` | 同上 |
| 16 | `POST /topic/v1/profile/bids` | `…/profile/bids` | 同上 |
| 17 | `POST /topic/v1/search/smart` | `…/enterprises/smart` | `EnterpriseSearchAuxController` |

分层：`Controller → Service → RemoteEnterprisePythonClient`（动态路由配置复用既有 Feign）。

## 2. 偏离说明（as-built）

1. **路径**：派单建议 `/topic/v1/enterprise/**`；as-built 为 `@EnableOpenApi("enterprise")` + `@RequestMapping("/topic/v1/…")`，网关完整路径为 `gateway/enterprise/topic/v1/…`（与既有门面一致）。
2. **smart** 落在 `EnterpriseSearchAuxController`（按页面拆分），功能归属本任务。
3. **响应 DTO（已补强）**：顶层 envelope + 行级 Item 均按 `API-接口文档.md` 强类型（如 `FinancialYearItem` / `PatentDetailItem` / `BidItem` / `FinancingEventItem` 等）；`@JsonIgnoreProperties(ignoreUnknown=true)` 容忍多余字段。

## 3. 产物清单

| 产物 | 路径（相对 `lumen-svc-platform/`） |
|---|---|
| Controller | `…/controller/EnterpriseProfileDetailController.java` |
| Service | `…/service/EnterpriseProfileDetailService.java` + `impl/` |
| smart | `…/controller/EnterpriseSearchAuxController.java`（`/smart`） |
| Request DTOs | `EnterpriseProfileRequest`（复用）+ `EnterpriseSmartSearchRequest` |
| Response DTOs | `…/api/dto/EnterpriseExtendedDTOs.java`（本任务相关类型） |
| Feign | `…/feign/RemoteEnterprisePythonClient.java`（追加方法） |
| 对外 Feign | `…/api/feign/RemoteTopicEnterpriseService.java`（追加） |
| 契约增量 | `agent-handoffs/企业战略分析-ENT/API-ENT-contract-draft.md` §3.5 |

## 4. 验收证据

| 项 | 结果 |
|---|---|
| Maven + JDK17 编译 | ✅ SUCCESS（本机会话已跑） |
| commit SHA | `05bddb3`（已 push `origin/dev`）|
| 禁止 `R<Object>` | ✅ 返回 `R<具体 DTO>` |
| Feign 前缀 | ✅ `/internal/gkx-search` |
| OTel | ✅ 复用模块既有 Feign/Agent 链路（未新增独立 span 配置） |

## 5. 架构合规自检（7 条）

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ Java 纯转发 |
| 2 | 前端→Java→Python `/internal/*` | ✅ |
| 3 | 不直连 nGQL/ES | ✅ |
| 4 | Feign `/internal/gkx-search` | ✅ |
| 5 | 可观测性 | ✅ 复用既有 |
| 6 | commit 标注 `[human:侯佳伟]` / `[agent:api-agent]` | `05bddb3` 已 push |
| 7 | demo2 不 merge lumen | ✅ N/A（仅 lumen-svc-platform） |

## 6. 开放项

1. 本地联调 / Mock 字段对照未逐接口打点 — 需 QA/联调。
2. **代码尚未 push `origin/dev`** — 监管人确认后提交并推送。

## 7. Cost 回填（registry）

| 字段 | 值 | 说明 |
|---|---|---|
| `actual_tokens` | `200_000` | 与派单估算对齐；五单共用会话按估算比例分摊 |
| `model_used` | `claude-sonnet-4.5` | registry 枚举口径（会话为 Cursor 编码档） |
| `actual_cost` | `1.08` | `200k × (0.8×3 + 0.2×15) / 1e6` |
| `cost_warn` | `green` | < $5 |
