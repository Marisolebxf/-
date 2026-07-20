# Handoff：ENT-JAVA-RISK

- **时间**：2026-07-20
- **执行**：agent:api-agent（监管：human:侯佳伟）
- **仓库 / 分支**：`lumen-svc-platform` / `dev`
- **派单包**：`ENT-JAVA-INTEGRATION-派单包.md` §5.2
- **状态建议**：`review`
- **接口总文档（前端联调入口）**：[`API-ENT-full-catalog.md`](./API-ENT-full-catalog.md)（76 端点全量；本单对应「风险」+ 检索辅助 aggregations/by-codes/hot，见总文档 §3 / §4）

## 1. 范围与实现

对接 **22** 端点（派单包写 23：`risk/all` + 18 类明细 + 检索辅助 3；计数口径为 **1+18+3=22**，无额外第 23 个独立路径）。

| 分组 | Java 前缀 | 数量 | Controller |
|---|---|---:|---|
| 风险全部 | `POST /topic/v1/profile/risk/all` | 1 | `EnterpriseRiskDetailController` |
| 18 类风险明细 | `POST /topic/v1/profile/risk/{type}` 独立 `@PostMapping` | 18 | 同上 |
| 检索辅助 | `POST /topic/v1/search/{aggregations,by-codes,hot}` | 3 | `EnterpriseSearchAuxController` |

**18 类 path 段**（均独立方法，无 `@PathVariable`）：

`judicial-case` · `dishonest` · `executed` · `limit-high` · `lawsuit` · `court-filed` · `court-notice` · `court-announcement` · `equity-freeze` · `equity-pledge` · `zhongben` · `chattel-mortgage` · `judicial-sale` · `bankruptcy` · `abnormal` · `punishment` · `illegal` · `tax-punish`

Python：`/internal/gkx-search/profile/risk/**` 与 `/internal/gkx-search/enterprises/{aggregations,by-codes,hot}`。

## 2. 偏离说明

1. 网关路径 as-built：`gateway/enterprise/topic/v1/…`（同契约草案 §2.1）。
2. 风险明细：18 类共用 `RiskDetailItem`（§11.3 共性核心字段：`case_no`/`case_title`/`case_cause`/`court_name`/日期/`party_role`/`is_history`）；**未**拆 18 个完整独立类（文档无逐类完整字段表）。
3. 端点总数按路径计 **22**（非 23）。

## 3. 产物清单

| 产物 | 路径 |
|---|---|
| Risk Controller/Service | `…/EnterpriseRiskDetailController.java` + Service/Impl |
| Search aux（本任务 3） | `…/EnterpriseSearchAuxController.java` |
| Request | `EnterpriseRiskAllRequest`、`EnterpriseAggregationRequest`、`EnterpriseByCodesRequest`、`EnterpriseHotRequest`；明细复用 `EnterpriseProfileRequest` |
| Response | `EnterpriseExtendedDTOs` 风险/检索相关类型 |
| Feign | `RemoteEnterprisePythonClient` 追加 |

## 4. 验收证据

| 项 | 结果 |
|---|---|
| 独立 `@PostMapping` ×18 | ✅ |
| 编译 | ✅ Maven SUCCESS |
| commit SHA | `05bddb3`（已 push `origin/dev`）|
| Feign `/internal/gkx-search` | ✅ |

## 5. 架构合规自检（7 条）

| # | 结果 |
|---|---|
| 1 算法只在 Python | ✅ |
| 2 调用链 | ✅ |
| 3 不直连图/ES | ✅ |
| 4 Feign 前缀 | ✅ |
| 5 OTel | ✅ 复用 |
| 6 commit 标注 | `05bddb3` |
| 7 demo2 边界 | ✅ N/A |

## 6. 开放项

1. 若需 18 类完整独立 Item：待 Python/DWD 补齐逐类字段表后再拆 — follow-up。
2. Mock 逐类对照 — QA/联调。
3. 代码已 commit + push `origin/dev`。
## 7. Cost 回填

| 字段 | 值 |
|---|---|
| `actual_tokens` | `300_000` |
| `model_used` | `claude-sonnet-4.5` |
| `actual_cost` | `1.62` |
| `cost_warn` | `green` |
