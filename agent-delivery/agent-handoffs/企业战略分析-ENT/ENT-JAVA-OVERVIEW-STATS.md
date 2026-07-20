# Handoff：ENT-JAVA-OVERVIEW-STATS

- **时间**：2026-07-20
- **执行**：agent:api-agent（监管：human:侯佳伟）
- **仓库 / 分支**：`lumen-svc-platform` / `dev`
- **派单包**：`ENT-JAVA-INTEGRATION-派单包.md` §5.3
- **状态建议**：`review`
- **接口总文档（前端联调入口）**：[`API-ENT-full-catalog.md`](./API-ENT-full-catalog.md)（76 端点全量；本单对应「发展概况」7 端点，见总文档 §3 / §4）

## 1. 范围与实现

企业发展概况统计 **7** 端点，Java 纯转发。

| # | Java | Python |
|---|---|---|
| 1 | `POST /topic/v1/stats/overview/kpi` | `/internal/gkx-search/stats/overview/kpi` |
| 2 | `POST /topic/v1/stats/overview/industry-distribution` | `…/industry-distribution` |
| 3 | `POST /topic/v1/stats/overview/trend` | `…/trend` |
| 4 | `POST /topic/v1/stats/overview/district-heat` | `…/district-heat` |
| 5 | `POST /topic/v1/stats/overview/industry-kpi` | `…/industry-kpi` |
| 6 | `POST /topic/v1/stats/overview/industry-comparison` | `…/industry-comparison` |
| 7 | `POST /topic/v1/stats/overview/industry-trend` | `…/industry-trend` |

Controller：`EnterpriseStatsOverviewController`（`@RequestMapping("/topic/v1/stats/overview")`）。

## 2. 偏离说明

1. 路径 as-built：`gateway/enterprise/topic/v1/stats/overview/…`。
2. 行级已强类型：`ChainCountItem` / `GrowthTrendItem` / `DistrictHeatItem` / `YearCountItem`。

## 3. 产物清单

- `EnterpriseStatsOverviewController` / `EnterpriseStatsOverviewService`(+Impl)
- Request：`EnterpriseStatsRegionRequest`、`EnterpriseChainCodeRequest` 等
- Response：`EnterpriseExtendedDTOs` stats overview 类型
- Feign 追加方法；契约 §3.5

## 4. 验收证据

| 项 | 结果 |
|---|---|
| 三层齐全 ×7 | ✅ |
| 编译 | ✅ |
| commit SHA | `05bddb3`（已 push `origin/dev`）|

## 5. 架构合规自检（7 条）

算法 Python ✅ · 调用链 ✅ · 不直连 ✅ · Feign 前缀 ✅ · OTel 复用 ✅ · commit 标注 `05bddb3` · demo2 N/A ✅

## 6. 开放项

联调验证预聚合字段；已 commit/push：`05bddb3`

## 7. Cost 回填

| 字段 | 值 |
|---|---|
| `actual_tokens` | `120_000` |
| `model_used` | `claude-sonnet-4.5` |
| `actual_cost` | `0.65` |
| `cost_warn` | `green` |
