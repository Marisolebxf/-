# 派单包：ENT-PY-ANALYSIS-CALLBACK（v3.2，含 D-30 修订/D-31/D-32）

- **派单方**：coordinator（architect-agent 起草）
- **执行 Agent**：`data-agent`
- **监管人**：human:徐滕强
- **仓**：`demo-svc-topic-py`
- **子项目**：`gkx_ai_service/`
- **依赖**：`ENT-ARCH-ANALYSIS-TASK-DOC`
- **状态**：`backlog`
- **架构真源**：`ARCH-ANALYSIS-TASK-设计方案.md` **v3.2**

---

## 0. 铁律前置

1. **本任务只在 `demo-svc-topic-py` 仓**，复用 `gkx_ai_service/` 子项目
2. **Python 是回调中转层**，不解析业务语义，但负责 result JSON 的 snake_case → camelCase 命名转换 + 写 MinIO + 转发 resultUrl（v3.2 D-30 修订）
3. **taskId 由 Java 唯一生成**，回调中携带的 taskId 必须与 Java 创建时一致
4. **pending 不回传 Java**：算法回调中的 pending 状态映射为 running 后再转发 Java
5. **JSON 字段命名（D-30 v3.2）**：算法 ↔ Python 统一 snake_case；常规回调字段（`task_id`/`analysis_type`/`event`/`node_code` 等）Java 用 `@JsonProperty` 对接 snake_case；**分析结果 `result` 例外**：Python 转 camelCase 后转发 Java（因 Java 透传不解析、前端直接消费）

---

## 1. 目标

在 `gkx_ai_service` 新增统一内部回调入口：

```
POST /internal/gkx-ai/analysis/callback
```

算法（entan / science）只能回调 Python；Python 根据 `analysis_type` 转发到 Java：

| analysis_type | Java callback URL |
|---|---|
| `enterprise_eval` | `POST {java_base_url}/topic/v1/analysis/callback/eval` |
| `risk_insight` | `POST {java_base_url}/topic/v1/analysis/callback/risk` |
| `talent_recommend` | `POST {java_base_url}/topic/v1/analysis/callback/recommend` |

> **路径变更**：v3.0 为 `/api/analysis/callback/*`，v3.1 已改为 `/topic/v1/analysis/callback/*`（服务内路径，网关为 `/enterprise/topic/v1/analysis/callback/*`）。

---

## 2. 回调请求契约

### 2.1 算法 → Python 回调

算法侧（entan / science）通过 Webhook 回调 Python，payload 字段统一 **`snake_case`**：

```json
{
  "task_id": "EVAL-20260725-001",
  "analysis_type": "enterprise_eval",
  "event": "step_started | step_completed | task_completed | task_failed | task_cancelled",
  "node_code": "compute",
  "node_name": "指标计算",
  "node_index": 3,
  "status": "running | success | failed | cancelled",
  "progress": 50.0,
  "result": {},
  "error": null,
  "timestamp": "2026-07-25T16:30:00+08:00"
}
```

**event 枚举（5 种，D-31）**：

| event | 触发时机 | status 值 | 说明 |
|-------|---------|-----------|------|
| `step_started` | 每个节点开始时 | `running` | 中间态 |
| `step_completed` | 每个节点完成时 | `running` | 中间态 |
| `task_completed` | 全部节点完成 | `success` | 终态 |
| `task_failed` | 节点失败，重试耗尽 | `failed` | 终态，需带 error |
| `task_cancelled` | 用户取消，算法检查到 cancel_flag 后终止 | `cancelled` | 终态，不带 error（见 D-31） |

**状态映射规则**：

| 算法回调 status | Python 转发 Java status | 说明 |
|---|---|---|
| `pending` | `running` | 算法排队中，映射为 running（**pending 不得透传 Java**） |
| `running` | `running` | 算法执行中 |
| `success` | `success` | 算法完成 |
| `failed` | `failed` | 算法失败 |
| `cancelled` | `cancelled` | 用户取消 |

### 2.2 Python → Java 转发

Python 校验通过后，转发给 Java callback。常规字段保持 **`snake_case`**（Java 用 `@JsonProperty` 接收）；**`result` 字段转 camelCase** 后转发（v3.2 D-30 修订）。Python 转 camelCase 后统一写 MinIO，转发 `resultUrl` 指针（全量外置，不区分大小）：

```json
{
  "task_id": "EVAL-20260725-001",
  "analysis_type": "enterprise_eval",
  "event": "step_completed",
  "node_code": "compute",
  "node_name": "指标计算",
  "node_index": 3,
  "status": "running",
  "progress": 50.0,
  "result": {},
  "error": null,
  "timestamp": "2026-07-25T16:30:00+08:00"
}
```

---

## 3. 实现要求

1. 校验必填字段：`task_id`、`analysis_type`、`event`、`status`。
   - `analysis_type` 必须为 `enterprise_eval` / `risk_insight` / `talent_recommend` 之一。
   - `event` 必须为 `step_started` / `step_completed` / `task_completed` / `task_failed` / `task_cancelled` 之一。
2. **状态映射**：算法返回 `pending` 时映射为 `running` 再转发 Java；其他状态原样转发。
3. Java callback base URL、超时和重试参数走 Nacos / 环境变量 `gkxlumen.topic.enterprise.java-callback-base-url`。
4. **result 命名转换 + MinIO 读写（v3.2 新增）**：`task_completed` 回调带 `result` 时，Python 将 result JSON 整体 snake_case → camelCase 转换（递归转 key），然后**统一写 MinIO**（camelCase），转发 `resultUrl` 给 Java。**不解析 result 业务语义**，只做 key 风格转换 + MinIO 读写。无阈值判断。
5. 使用 `task_id + event + node_code` 或等价键记录重复回调，保证转发幂等。
6. 结构化日志必须含 task_id、analysis_type、traceId、下游状态和重试次数。
7. Java 不可达时有限重试（默认 3 次，指数退避）并返回明确错误；禁止无限阻塞算法线程。
8. 保留 `/internal/*` 路径、鉴权和 OTel，禁止对前端暴露。

---

## 4. 禁止

- 禁止算法直接回调 Java（必须经 Python 中转）
- 禁止解析 result 业务语义（Python 只做 key 风格转换 + MinIO 读写，不消费 result 字段含义）
- 禁止把 `pending` 状态转发给 Java
- 禁止无限重试阻塞算法线程
- 禁止对前端暴露 `/internal/*` 路径
- ❌ 禁止常规回调字段用 camelCase（Python 侧统一 snake_case，见 D-30）；**例外**：result JSON 转 camelCase 后转发 Java
- ❌ 禁止把 `task_cancelled` 当作 `task_failed` 处理（两者语义不同，见 D-31）

---

## 5. 验收

- 三类 callback 路由（eval/risk/recommend）单测通过
- 节点事件（`step_started` / `step_completed`）、终态事件（`task_completed` / `task_failed` / `task_cancelled`）单测通过
- pending → running 映射测试通过
- 重复回调幂等测试通过
- 错误 analysis_type、缺字段、Java 超时和非 2xx 有明确响应和日志
- 常规回调字段全部 snake_case（D-30）；result 已转 camelCase
- result snake_case → camelCase 转换测试通过
- 全量写 MinIO + 转发 resultUrl 测试通过（不区分大小结果）
- 与 Java callback Mock 联调通过
- CI、handoff、架构合规和 cost 四字段齐全
