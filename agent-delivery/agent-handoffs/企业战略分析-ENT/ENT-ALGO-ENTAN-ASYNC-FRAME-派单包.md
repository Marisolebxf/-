# 派单包：ENT-ALGO-ENTAN-ASYNC-FRAME

> **架构真源**：`ARCH-ANALYSIS-TASK-设计方案.md` **v3.2**（2026-07-27，含 D-30 修订/D-31/D-32）

## 1. 任务信息

- 执行角色：`algorithm-agent`
- 仓库：`demo-algo-ent-analysis`
- 依赖：`ENT-ARCH-ANALYSIS-TASK-DOC`、`ENT-ALGO-EVAL-INTERACTIVE`
- 状态：`backlog`

## 2. 目标

把 entan 评估从进程内任务态升级为可恢复的算法侧异步任务框架。算法侧使用
MySQL 保存自身任务状态、节点与结果，但不得成为前端历史入口；Java 编排库仍是业务真源。

## 3. 实现要求

1. create-and-start 接收 Java `taskId`、`analysis_type`、`sub_type`、`callback_url`。
   - **不接收 `client_request_id`**（v3.1 已移除；taskId 即全局幂等键）。
   - `analysis_type` = `enterprise_eval`；`sub_type` = `technology` | `business` | `competitiveness`。
   - `taskId` 由 Java 唯一生成，算法侧复用，不自生成。
2. 算法侧 MySQL 保存任务、节点、结果和重试信息；不得继续以 dict 作为生产真源。
   - 算法侧 MySQL 可保存 `pending` 状态（待跑中），但 **pending 不得回传 Java**；回调/查询时映射为 `running`。
3. 全局并发默认 3，由 `GKX_ALGO_GLOBAL_CONCURRENCY` 或等价配置控制。
4. 按 submit→validate→data_gather→compute→confidence→assemble 推进节点（6 节点，见架构 §3.2）。
5. 节点与终态 Webhook 只发 Python `/internal/gkx-ai/analysis/callback`；回调 payload 强制携带 `analysis_type`。
6. RUNNING 取消为逻辑取消（见架构 §4.6）：
   - 算法收到 `POST /gdf/tasks/{task_id}/cancel` 后设 `cancel_flag=True`；
   - **每个节点开始时检查** `cancel_flag`，命中则终止后续节点、DB 标记 `cancelled`、丢弃结果；
   - 当前正在执行的节点可跑完，但不提交结果；
   - 取消后发 **`task_cancelled`** Webhook（**不是 `task_failed`**，见 D-31）。
7. 超时恢复、有限重试、D9 血缘、OTel 和敏感配置管理齐全。
8. **结果契约以 v3.2 §9 三套 sub_type 结构为准**（technology 五维雷达 / business 经营指标非雷达 / competitiveness 三维雷达）；
   旧四维统一结构（innovation/operation/growth/risk）仅作内部评分计算中间态，**不得作为对外结果 schema**。

## 4. JSON 字段命名风格（D-30）

> **算法侧 ↔ Python 侧统一用 `snake_case`（下划线）**；Java 侧用 `camelCase`。常规字段 Java 用 `@JsonProperty` 对接；分析结果 `result` 的 snake_case → camelCase 转换由 Python 负责（v3.2）。

算法侧所有 JSON 请求/响应/回调 payload 字段一律 `snake_case`：
- 请求：`task_id` / `analysis_type` / `sub_type` / `enterprise_codes` / `callback_url` / `weights`
- 回调：`event` / `task_id` / `analysis_type` / `mission_type` / `status` / `progress` / `node_code` / `node_name` / `timestamp`
- 响应：`success` / `task_id` / `mission_type` / `cost_seconds` / `result` / `error`

> **分析结果回传（v3.2）**：算法 `task_completed` 回调把 `result` 内嵌在 payload 里返回给 Python（snake_case），**算法侧不碰 MinIO、不碰 camelCase**。Python 负责转 camelCase + 写 MinIO + 转发 resultUrl。

## 5. 回调事件（5 种，D-31）

| 事件 | 触发时机 | status 值 |
|------|---------|-----------|
| `step_started` | 每个节点开始时 | `running` |
| `step_completed` | 每个节点完成时 | `running` |
| `task_completed` | 全部节点完成 | `success` |
| `task_failed` | 节点失败，重试耗尽 | `failed` |
| `task_cancelled` | 用户取消，算法检查到 cancel_flag 后终止 | `cancelled` |

> ⚠️ 取消后**不得**发 `task_failed`，必须发 `task_cancelled`。两者语义不同（取消是主动行为不带 error，失败是异常需带 error）。

## 6. 禁止

- 禁止算法直接回调 Java。
- 禁止 PostgreSQL/PG；运行时统一 MySQL。
- 禁止把并发值 3 写死在业务代码。
- 禁止改变 `/v1/evaluation/compute` 的三模式业务语义。
- ❌ 禁止接收或使用 `client_request_id`（v3.1 已移除）。
- ❌ 禁止把 `pending` 状态回传 Java（Java 侧只有 running/success/failed/cancelled）。
- ❌ 禁止取消后发 `task_failed`（必须发 `task_cancelled`，见 D-31）。
- ❌ 禁止 JSON 字段用 camelCase（算法侧统一 snake_case，见 D-30）。

## 7. 验收

- MySQL 重启恢复、并发限制、重复 taskId、逻辑取消和失败重试测试通过。
- 回调 payload 强制携带 `analysis_type`，并与 Python callback 联调。
- 三模式结果按 v3.2 §9 三套 sub_type schema 返回；D9 字段不回退。
- 算法侧 `pending` 不出现在回调/查询响应中（映射为 `running`）。
- 取消后发 `task_cancelled`（不是 `task_failed`），DB 标记 `cancelled`。
- JSON 字段全部 snake_case（D-30）。
- CI、handoff、架构合规和 cost 四字段齐全。
