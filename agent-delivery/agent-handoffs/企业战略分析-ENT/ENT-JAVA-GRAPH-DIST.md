# Handoff：ENT-JAVA-GRAPH-DIST

- **时间**：2026-07-20
- **执行**：agent:api-agent（监管：human:侯佳伟）
- **仓库 / 分支**：`lumen-svc-platform` / `dev`
- **派单包**：`ENT-JAVA-INTEGRATION-派单包.md` §5.5
- **状态建议**：`review`
- **接口总文档（前端联调入口）**：[`API-ENT-full-catalog.md`](./API-ENT-full-catalog.md)（76 端点全量；本单对应「图谱」+「分布」，见总文档 §3 / §4）

## 1. 范围与实现

图谱 **2** + 分布 **1** = **3** 端点。

| # | Java | Python | Controller |
|---|---|---|---|
| 1 | `POST /topic/v1/profile/graph/subgraph` | `/internal/gkx-search/profile/graph/subgraph` | `EnterpriseGraphController` |
| 2 | `POST /topic/v1/profile/graph/expand` | `…/profile/graph/expand` | 同上 |
| 3 | `POST /topic/v1/stats/distribution` | `/internal/gkx-search/stats/distribution` | `EnterpriseDistributionController` |

图谱响应 DTO 含 `nodes` / `edges` / **`source`**（`nebula|mock|error`）字段，Feign 透传不丢弃。

## 2. 偏离说明

1. 网关路径 as-built：`gateway/enterprise/topic/v1/profile/graph/…` 与 `…/stats/distribution`。
2. `nodes`/`edges`/`map_data`/`kpi` 已强类型；仅节点/边的开放扩展袋 `props` 保留 `Map<String,Object>`（文档即为自由 object）；`source` 字段保留。

## 3. 产物清单

- `EnterpriseGraphController` / `EnterpriseGraphService`(+Impl)
- `EnterpriseDistributionController` / `EnterpriseDistributionService`(+Impl)
- Request：`EnterpriseGraphSubgraphRequest`、`EnterpriseGraphExpandRequest`、`EnterpriseDistributionRequest`
- Response：`EnterpriseExtendedDTOs` graph/distribution 类型；Feign 追加；契约 §3.5

## 4. 验收证据

| 项 | 结果 |
|---|---|
| `source` 字段保留 | ✅ DTO / 透传 |
| 三层 ×3 | ✅ |
| 编译 | ✅ |
| commit SHA | `05bddb3`（已 push `origin/dev`）|

## 5. 架构合规自检（7 条）

算法 Python ✅（图算法在下游）· 调用链 ✅ · Java 不直连 Nebula ✅ · Feign 前缀 ✅ · OTel 复用 ✅ · commit 标注 `05bddb3` · demo2 N/A ✅

## 6. 开放项

联调验证 `source` 与 city 默认 `parent_region_id=440300`；已 commit/push：`05bddb3`

## 7. Cost 回填

| 字段 | 值 |
|---|---|
| `actual_tokens` | `100_000` |
| `model_used` | `claude-sonnet-4.5` |
| `actual_cost` | `0.54` |
| `cost_warn` | `green` |
