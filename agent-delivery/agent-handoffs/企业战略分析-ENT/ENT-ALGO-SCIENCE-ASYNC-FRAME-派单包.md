# 派单包：ENT-ALGO-SCIENCE-ASYNC-FRAME

> **架构真源**：`ARCH-ANALYSIS-TASK-设计方案.md` **v3.2**（2026-07-27，含 D-30 修订/D-31/D-32）

## 1. 任务信息

- 执行角色：`algorithm-agent`
- 仓库：`demo-algo-science`
- 依赖：`ENT-ARCH-ANALYSIS-TASK-DOC`
- 状态：`backlog`

## 2. 目标

为风险洞察与引育推荐建立统一算法侧异步任务框架，同时允许两类业务保留各自节点和结果契约。
实现细节由算法团队发挥，但外部契约必须符合架构 **v3.2**。

## 3. 实现要求

1. `/gdf/tasks` 提供 create-and-start、status、result、cancel 内部 API。
2. 请求接收 Java `taskId`、`analysis_type`、`sub_type`、`callback_url`。
   - **不接收 `client_request_id`**（v3.1 已移除；taskId 即全局幂等键）。
   - `taskId` 由 Java 唯一生成，算法侧复用，不自生成。
3. MySQL 保存算法任务状态、节点、结果和重试信息。
   - 算法侧 MySQL 可保存 `pending` 状态（待跑中），但 **pending 不得回传 Java**；回调/查询时映射为 `running`。
4. 全局并发默认 3 且配置化；支持超时恢复和有限重试。
5. Webhook 只发 Python callback，并强制携带 `analysis_type`。
6. 风险支持 `supply_chain/pain_points`；推荐支持 `attraction/cultivation`。
7. 供应链图谱一次计算最多 3 级并形成完整快照，不按展开动作二次计算。
8. RUNNING 取消为逻辑取消（见架构 §4.6）：
   - 算法收到 `POST /gdf/tasks/{task_id}/cancel` 后设 `cancel_flag=True`；
   - **每个节点开始时检查** `cancel_flag`，命中则终止后续节点、DB 标记 `cancelled`、丢弃结果；
   - 当前正在执行的节点可跑完，但不提交结果；
   - 取消后发 **`task_cancelled`** Webhook（**不是 `task_failed`**，见 D-31）。
9. D9、OTel、配置密钥管理齐全。

## 4. JSON 字段命名风格（D-30）

> **算法侧 ↔ Python 侧统一用 `snake_case`（下划线）**；Java 侧用 `camelCase`。常规字段 Java 用 `@JsonProperty` 对接；分析结果 `result` 的 snake_case → camelCase 转换由 Python 负责（v3.2）。

算法侧所有 JSON 请求/响应/回调 payload 字段一律 `snake_case`：
- 请求：`task_id` / `analysis_type` / `sub_type` / `enterprise_codes` / `callback_url`
- 回调：`event` / `task_id` / `analysis_type` / `status` / `progress` / `node_code` / `node_name` / `timestamp`
+
> **分析结果回传（v3.2）**：算法 `task_completed` 回调把 `result` 内嵌在 payload 里返回给 Python（snake_case），**算法侧不碰 MinIO、不碰 camelCase**。Python 负责转 camelCase + 阈值判断 + MinIO 读写。
- 响应：`success` / `task_id` / `cost_seconds` / `result` / `error`

## 5. 回调事件（5 种，D-31）

| 事件 | 触发时机 | status 值 |
|------|---------|-----------|
| `step_started` | 每个节点开始时 | `running` |
| `step_completed` | 每个节点完成时 | `running` |
| `task_completed` | 全部节点完成 | `success` |
| `task_failed` | 节点失败，重试耗尽 | `failed` |
| `task_cancelled` | 用户取消，算法检查到 cancel_flag 后终止 | `cancelled` |

> ⚠️ 取消后**不得**发 `task_failed`，必须发 `task_cancelled`。

## 6. 禁止

- 禁止算法直连 Java 或前端。
- 禁止 PostgreSQL/PG；使用 MySQL。
- 禁止写死并发值。
- 禁止用 Neo4j，图谱仍使用 NebulaGraph。
- ❌ 禁止接收或使用 `client_request_id`（v3.1 已移除）。
- ❌ 禁止把 `pending` 状态回传 Java。
- ❌ 禁止取消后发 `task_failed`（必须发 `task_cancelled`，见 D-31）。
- ❌ 禁止 JSON 字段用 camelCase（算法侧统一 snake_case，见 D-30）。

## 7. 验收

- 两类 analysis_type、各 sub_type 的任务状态和结果契约测试通过。
- 并发、重启恢复、逻辑取消、重复 taskId、回调失败重试测试通过。
- 3 级供应链快照有规模测试（**算法侧不碰 MinIO**，大结果内嵌回调返回 Python，由 Python 负责阈值判断 + MinIO 读写）。
- 取消后发 `task_cancelled`（不是 `task_failed`），DB 标记 `cancelled`。
- JSON 字段全部 snake_case（D-30）。
- CI、handoff、架构合规和 cost 四字段齐全。
