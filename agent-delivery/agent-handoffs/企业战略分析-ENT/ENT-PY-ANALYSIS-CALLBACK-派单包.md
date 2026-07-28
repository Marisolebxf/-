# 派单包：ENT-PY-ANALYSIS-CALLBACK（v3.4，含 D-30/D-31/D-32/D-33）

- **派单方**：coordinator（architect-agent 起草）
- **执行 Agent**：`data-agent`
- **监管人**：human:徐滕强
- **仓**：`demo-svc-topic-py`
- **子项目**：`gkx_ai_service/`（API 进程）+ `gkx_ai_worker/`（Worker 进程）
- **依赖**：`ENT-ARCH-ANALYSIS-TASK-DOC`
- **状态**：`in_progress`
- **架构真源**：`ARCH-ANALYSIS-TASK-设计方案.md` **v3.4**

---

## 0. 铁律前置

1. **本任务只在 `demo-svc-topic-py` 仓**，涉及两个子项目：`gkx_ai_service/`（API 进程）和 `gkx_ai_worker/`（Worker 进程）
2. **Python API 进程是回调中转层**，不解析业务语义，不碰 MinIO（D-33）；`task_completed` 事件投递 RabbitMQ 后立即返回 200
3. **Python Worker 进程是分析结果处理层**，消费 MQ → camelCase 转换 → 写 MinIO → 转发 Java（D-33）
4. **taskId 由 Java 唯一生成**，回调中携带的 taskId 必须与 Java 创建时一致
5. **pending 不回传 Java**：算法回调中的 pending 状态映射为 running 后再转发 Java
6. **JSON 字段命名（D-30 v3.2）**：算法 ↔ Python 统一 snake_case；常规回调字段 Java 用 `@JsonProperty` 对接 snake_case；**分析结果 `result` 例外**：Worker 转 camelCase 后写 MinIO，转发 resultUrl 给 Java

---

## 1. 目标

### 1.1 API 进程（`gkx_ai_service/`）

在 `gkx_ai_service` 新增统一内部回调入口：

```
POST /internal/gkx-ai/analysis/callback
```

算法（entan / science）只能回调 Python API；Python 根据 `analysis_type` 路由：

| analysis_type | 处理方式 | Java callback URL |
|---|---|---|
| `enterprise_eval` | task_completed → 投递 MQ；其余 → 同步转发 | `POST {java_base_url}/topic/v1/analysis/callback/eval` |
| `risk_insight` | 同上 | `POST {java_base_url}/topic/v1/analysis/callback/risk` |
| `talent_recommend` | 同上 | `POST {java_base_url}/topic/v1/analysis/callback/recommend` |

### 1.2 Worker 进程（`gkx_ai_worker/`，D-33 新增）

独立 Python 项目，无 HTTP 服务，纯 asyncio 消费循环：

```
python -m gkx_ai_worker.main
```

消费 RabbitMQ 队列 `gkx.analysis.result`，处理流程：
1. 接收消息（task_id + analysis_type + result + callback_base + java_callback_url）
2. result snake_case → camelCase 递归转换
3. 写 MinIO（camelCase JSON）
4. 转发 Java callback（带 resultUrl 指针）
5. ACK 消息

> **路径变更**：v3.0 为 `/api/analysis/callback/*`，v3.1 已改为 `/topic/v1/analysis/callback/*`（服务内路径，网关为 `/topicAsync/v1/analysis/callback/*`）。

---

## 2. 回调请求契约

### 2.1 算法 → Python API 回调

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
| `task_completed` | 全部节点完成 | `success` | 终态，**投递 MQ 异步处理**（D-33） |
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

**非 task_completed 事件**（同步转发）：Python 校验通过后，同步转发给 Java callback，常规字段保持 **`snake_case`**（Java 用 `@JsonProperty` 接收）。

**task_completed 事件**（异步处理，D-33）：Python API 进程投递消息到 RabbitMQ，Worker 进程消费后做 camelCase 转换 + 写 MinIO + 转发 Java。Java 收到的 payload：

```json
{
  "task_id": "EVAL-20260725-001",
  "analysis_type": "enterprise_eval",
  "event": "task_completed",
  "status": "success",
  "result_url": "http://minio:9000/gkx-analysis-results/enterprise_eval/202607/EVAL-20260725-001/abc12345.json",
  "result_asset_id": "enterprise_eval/202607/EVAL-20260725-001/abc12345.json",
  "result_size": 45678,
  "result_bucket": "gkx-analysis-results",
  "timestamp": "2026-07-25T16:30:00+08:00"
}
```

---

## 3. 实现要求

### 3.1 API 进程（`gkx_ai_service/views/callback.py`）

1. 校验必填字段：`task_id`、`analysis_type`、`event`、`status`。
   - `analysis_type` 必须为 `enterprise_eval` / `risk_insight` / `talent_recommend` 之一。
   - `event` 必须为 `step_started` / `step_completed` / `task_completed` / `task_failed` / `task_cancelled` 之一。
2. **状态映射**：算法返回 `pending` 时映射为 `running` 再转发 Java；其他状态原样转发。
3. **task_completed 投递 MQ（D-33）**：`task_completed` 回调带 `result` 时，Python API 进程**投递消息到 RabbitMQ**（消息体含 task_id / analysis_type / result / callback_base / java_callback_url），立即返回 `200 {"status": "accepted", "processing": "mq"}`。**API 进程不做 camelCase 转换、不碰 MinIO**。
4. **MQ 降级策略**：MQ 不可用时，API 进程降级同步转发（不带 result_url），返回 503 告知 Java 侧需 XXL-Job 兜底。
5. **非 task_completed 同步转发**：`step_started`/`step_completed`/`task_failed`/`task_cancelled` 事件 payload 小，保持同步转发到 Java callback。
6. 使用 `task_id + event + node_index` 记录重复回调，保证转发幂等。
7. 结构化日志必须含 task_id、analysis_type、traceId、下游状态和重试次数。
8. Java 不可达时有限重试（默认 3 次，指数退避）并返回明确错误；禁止无限阻塞算法线程。
9. 保留 `/internal/*` 路径、鉴权和 OTel，禁止对前端暴露。

### 3.2 Worker 进程（`gkx_ai_worker/`，D-33 新增）

1. **纯 asyncio 消费循环**，无 HTTP 服务，无 FastAPI。
2. 消费 RabbitMQ 队列 `gkx.analysis.result`，prefetch=2（控制内存）。
3. **camelCase 转换**：result JSON 整体 snake_case → camelCase 递归转换（转 key）。
4. **写 MinIO**：camelCase JSON 写入 MinIO，object key 格式 `{analysis_type}/{YYYYMM}/{task_id}/{uuid8}.json`。MinIO 不可用时降级本地文件兜底。
5. **转发 Java**：构建带 resultUrl 指针的 payload，转发到 Java callback（重试 3 次，指数退避）。
6. **ACK 策略**：成功 → ACK；失败 → NACK + requeue（最多 3 次，带 `x-retry-count` header）；超过 3 次 → reject 进死信队列。
7. **信号处理**：SIGINT/SIGTERM 优雅关闭（停止消费，等待在途消息完成）。

### 3.3 MQ 配置（`gkx_ai_service/deps.py` + `gkx_ai_worker/deps.py`）

| 配置项 | 环境变量 | 默认值 | 说明 |
|---|---|---|---|
| RabbitMQ URL | `GKX_RABBITMQ_URL` | `amqp://guest:guest@127.0.0.1:5672/` | 连接地址 |
| 队列名 | `GKX_RABBITMQ_QUEUE` | `gkx.analysis.result` | 持久化队列 |
| 死信交换机 | `GKX_RABBITMQ_DLX` | `gkx.analysis.result.dlx` | DIRECT 类型 |
| prefetch | `GKX_RABBITMQ_PREFETCH` | 2 | Worker 每次最多处理消息数 |
| max_retries | `GKX_RABBITMQ_MAX_RETRIES` | 3 | 超过后 reject 进死信队列 |

---

## 4. 禁止

- 禁止算法直接回调 Java（必须经 Python API 中转）
- 禁止 Python API 进程做 camelCase 转换或碰 MinIO（D-33：这些归 Worker 进程）
- 禁止解析 result 业务语义（Worker 只做 key 风格转换 + MinIO 读写，不消费 result 字段含义）
- 禁止把 `pending` 状态转发给 Java
- 禁止无限重试阻塞算法线程
- 禁止对前端暴露 `/internal/*` 路径
- ❌ 禁止常规回调字段用 camelCase（Python 侧统一 snake_case，见 D-30）；**例外**：result JSON 由 Worker 转 camelCase 后写 MinIO 转发 Java
- ❌ 禁止把 `task_cancelled` 当作 `task_failed` 处理（两者语义不同，见 D-31）
- ❌ 禁止用 `asyncio.create_task` 在 API 进程内处理 task_completed 大 JSON（D-33：改用 RabbitMQ + Worker）

---

## 5. 验收

- 三类 callback 路由（eval/risk/recommend）单测通过
- 节点事件（`step_started` / `step_completed`）、终态事件（`task_completed` / `task_failed` / `task_cancelled`）单测通过
- pending → running 映射测试通过
- **task_completed 投递 MQ 测试通过**（D-33：API 返回 `{"status": "accepted", "processing": "mq"}`）
- **MQ 降级测试通过**（MQ 不可用时 API 降级同步转发，返回 503）
- **Worker 消费 MQ 测试通过**（camelCase 转换 + 写 MinIO + 转发 Java + ACK）
- **Worker 重试 + 死信队列测试通过**（失败 3 次后进死信队列）
- 重复回调幂等测试通过
- 错误 analysis_type、缺字段、Java 超时和非 2xx 有明确响应和日志
- 常规回调字段全部 snake_case（D-30）；result 由 Worker 转 camelCase
- 与 Java callback Mock 联调通过
- CI、handoff、架构合规和 cost 四字段齐全
