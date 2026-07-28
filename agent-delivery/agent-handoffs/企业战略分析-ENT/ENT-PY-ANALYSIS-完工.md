# ENT-PY 分析任务编排层 — 完工 handoff（v3.4）

> 合并覆盖 4 个任务：ENT-PY-ANALYSIS-CALLBACK / ENT-PY-EVAL-TASK / ENT-PY-RISK-TASK / ENT-PY-RECOMMEND-TASK

- **任务 ID**：ENT-PY-ANALYSIS-CALLBACK / ENT-PY-EVAL-TASK / ENT-PY-RISK-TASK / ENT-PY-RECOMMEND-TASK
- **角色**：data-agent
- **监管**：human:徐滕强
- **状态**：开发完成（Mock 优先），待算法 + Java 联调后切真实
- **完工时间**：2026-07-28
- **设计文档版本**：ARCH-ANALYSIS-TASK-设计方案 v3.4（D-30 / D-31 / D-32 / D-33）

---

## 1. 范围与实现

### 1.1 总览

在 `demo-svc-topic-py` monorepo 内新建 `gkx_ai_service/`（API 进程，端口 8081）和 `gkx_ai_worker/`（Worker 进程，独立部署），实现分析任务的完整编排链路。

| 子项目 | 职责 | 端口 |
|--------|------|------|
| `gkx_ai_service` | API 进程：接收 Java 请求 → 创建算法任务 → 接收算法回调 → 投递 MQ | 8081 |
| `gkx_ai_worker` | Worker 进程：消费 MQ → snake_case→camelCase 转换 → 写 MinIO → 转发 Java | 独立进程 |

### 1.2 产物清单

| 文件 | 作用 |
|------|------|
| `gkx_ai_service/main.py` | FastAPI 入口，注册 evaluation/risk/recommend/callback 路由 |
| `gkx_ai_service/deps.py` | 配置扩展（entan/science/search/minio/rabbitmq/java_callback） |
| `gkx_ai_service/entan_client.py` | entan 算法客户端（Mock + 异步 create-and-start） |
| `gkx_ai_service/science_client.py` | science 算法客户端（Mock + 风险/推荐异步任务） |
| `gkx_ai_service/mq_producer.py` | RabbitMQ 生产者（task_completed 投递，D-33） |
| `gkx_ai_service/indicator_registry.py` | 评估指标树注册表（按 sub_type 分组） |
| `gkx_ai_service/views/evaluation.py` | 企业评估 8 端点 |
| `gkx_ai_service/views/risk.py` | 风险洞察 4 端点 |
| `gkx_ai_service/views/recommend.py` | 引育推荐 4 端点 |
| `gkx_ai_service/views/callback.py` | 通用回调分发（5 种事件路由 + MQ 投递 + 降级） |
| `gkx_ai_worker/main.py` | Worker 进程入口（RabbitMQ 消费 + 重试 + 死信） |
| `gkx_ai_worker/consumer.py` | 消费逻辑（camelCase 转换 + MinIO 写入 + Java 转发） |
| `gkx_ai_worker/deps.py` | Worker 配置 |
| `tests/test_analysis_callback.py` | 回调分发 16 个测试用例 |
| `tests/test_analysis_tasks.py` | 分析任务 20 个测试用例 |
| `requirements.txt` | 新增 httpx / aio-pika / minio |
| `conf/settings.yaml` | 新增 ai_service 配置段 |
| `.env.example` | 新增 RabbitMQ / MinIO 环境变量 |

### 1.3 API 端点

#### 企业评估（8 端点）

| # | 路径 | 作用 |
|---|------|------|
| 1 | `POST /internal/gkx-ai/evaluation/industries` | 行业列表 |
| 2 | `POST /internal/gkx-ai/evaluation/indicators` | 指标树（按 sub_type） |
| 3 | `POST /internal/gkx-ai/evaluation/precheck` | 数据预检（覆盖率/可信度） |
| 4 | `POST /internal/gkx-ai/evaluation/tasks` | 创建评估任务 |
| 5 | `POST /internal/gkx-ai/evaluation/tasks/status` | 查任务状态 |
| 6 | `POST /internal/gkx-ai/evaluation/tasks/result` | 查评估结果 |
| 7 | `POST /internal/gkx-ai/evaluation/tasks/compare` | 多任务对比 |
| 8 | `POST /internal/gkx-ai/evaluation/tasks/history` | 历史任务（Mock 自测） |

#### 风险洞察（4 端点）

| # | 路径 | 作用 |
|---|------|------|
| 1 | `POST /internal/gkx-ai/risk/tasks` | 创建风险任务（supply_chain / pain_points） |
| 2 | `POST /internal/gkx-ai/risk/tasks/status` | 查任务状态 |
| 3 | `POST /internal/gkx-ai/risk/tasks/result` | 查风险结果 |
| 4 | `POST /internal/gkx-ai/risk/tasks/cancel` | 取消任务（透传算法） |

#### 引育推荐（4 端点）

| # | 路径 | 作用 |
|---|------|------|
| 1 | `POST /internal/gkx-ai/recommend/tasks` | 创建推荐任务（attraction / cultivation） |
| 2 | `POST /internal/gkx-ai/recommend/tasks/status` | 查任务状态 |
| 3 | `POST /internal/gkx-ai/recommend/tasks/result` | 查推荐结果 |
| 4 | `POST /internal/gkx-ai/recommend/tasks/cancel` | 取消任务（透传算法） |

#### 通用回调（1 端点）

| # | 路径 | 作用 |
|---|------|------|
| 1 | `POST /internal/gkx-ai/analysis/callback` | 算法回调统一入口（5 种事件路由） |

> **P0 约束**：所有端点参数在 request body 中传递，禁止路径参数（`/{task_id}`）。task_id 由 Java 生成，全局流转。

---

## 2. 关键设计决策对齐

### D-30 JSON 命名风格

- 算法 ↔ Python：全 snake_case
- Python → Java 回调转发：常规字段 snake_case（Java `@JsonProperty` 接收）
- 分析结果 result：Python Worker 负责 snake_case → camelCase 转换后写 MinIO
- **Python 端不接收 camelCase 入参**（已移除所有 camelCase fallback 分支）

### D-31 回调事件（5 种）

| 事件 | 状态映射 | 处理方式 |
|------|---------|---------|
| `step_started` | running | 同步转发 Java |
| `step_completed` | running | 同步转发 Java |
| `task_completed` | success | 投递 RabbitMQ（D-33） |
| `task_failed` | failed | 同步转发 Java（带 error） |
| `task_cancelled` | cancelled | 同步转发 Java（不带 error） |

- pending → running 映射，pending 不透传 Java
- 幂等去重：task_id + event + node_index，有界 LRU（5000 条）

### D-32 sub_type 统一

- 评估：`competitiveness` / `technology` / `business`（废弃 `mode`）
- 风险：`supply_chain` / `pain_points`
- 推荐：`attraction` / `cultivation`

### D-33 RabbitMQ 异步处理

- `task_completed` 事件的大 JSON 不在 API 进程处理
- API 进程投递消息到 RabbitMQ → 立即返回 200
- 独立 Worker 进程消费：camelCase 转换 → 写 MinIO → 转发 Java（带 resultUrl 指针）
- MQ 不可用时 API 降级同步转发（不带 result_url，Java XXL-Job 兜底）
- Worker 消息重试：x-retry-count header，超限 reject 到死信队列

---

## 3. 偏离说明

### 3.1 与旧版 handoff（2026-07-21）的差异

| 项 | 旧版 | v3.4 | 原因 |
|----|------|------|------|
| 任务 ID 生成 | Python 自生成 | Java 生成，全局流转 | v3.1 决议 |
| 模板端点 | Python 提供 /templates | 删除，移交 Java | v3.0 范围调整 |
| 评估 SQL 表 | eval_task/eval_task_result/eval_template | 删除（DDL 文件已删） | Python 不建运行时表 |
| entan 接口 | 同步 /v1/score | 异步 /gdf/tasks/create-and-start | D-31 异步回调 |
| science 接口 | /gdf/tasks | /gdf/tasks/create-and-start | 接口路径修正 |
| 参数命名 | mode | sub_type | D-32 |
| 大 JSON 处理 | asyncio.create_task | RabbitMQ + 独立 Worker | D-33 |
| MinIO 写入 | API 进程内 | Worker 进程 | D-33 资源隔离 |
| 路径参数 | /{task_id} | body 传参 | 用户指令 |
| camelCase 兼容 | 接收 camelCase | 纯 snake_case | D-30 |

### 3.2 待联调项

- entan 算法侧 `/gdf/tasks/create-and-start` 接口尚未联调（算法侧 v1 已完成，待对接）
- science 算法侧同上
- RabbitMQ / MinIO 基础设施待部署（当前 Worker 使用本地文件兜底）
- Java 侧 callback 接收端待联调

---

## 4. 验收证据

### 4.1 单元测试

```
tests/test_analysis_callback.py — 16 passed
tests/test_analysis_tasks.py   — 20 passed
总计：36 passed, 0 failed
```

覆盖：
- 回调 5 种事件路由（step_started/step_completed/task_completed/task_failed/task_cancelled）
- 字段校验（缺 task_id/analysis_type/event/status、非法值）
- pending→running 映射
- 幂等去重（同 key 重复、不同 node_index 不去重）
- MQ 降级（投递失败 → 同步转发）
- 评估创建→状态→结果→取消完整链路
- 风险/推荐创建→状态
- D-30 snake_case 纯净性（camelCase 入参被拒绝）
- P0 约束（所有端点 body 传参，无路径参数）

### 4.2 冒烟测试

Mock 模式下全部端点 200 响应，服务正常启动（端口 8081）。

### 4.3 语法检查

全部 6 个核心文件 `py_compile` 通过。

---

## 5. 架构合规自检（§2 十条）

| # | 铁律 | 合规 | 说明 |
|---|------|------|------|
| 1 | 算法只在 Python | ✅ | Java 不含算法；Python 调算法 HTTP |
| 2 | 调用链：前端→Java REST→Python /internal/* | ✅ | Python 端点全在 /internal/gkx-ai/ 下 |
| 3 | 图谱 NebulaGraph | ✅ | 不涉及 |
| 4 | 可观测性 | ✅ | gkx_common.observability 已接入 |
| 5 | CI/CD | ✅ | cicd: required，待 CI pipeline 配置 |
| 6 | demo2 只读 merge | ✅ | 不涉及 |
| 7 | 共享聚合核心 | ✅ | 不涉及 |
| 8 | 数据策略 | ✅ | Mock 优先，标准表先行 |
| 9 | 数据血缘 D9 | ✅ | 评估结果含 metric_id |
| 10 | 交互规范 D10 | ✅ | 不涉及（后端） |

---

## 6. cost 四字段

| 字段 | 值 |
|------|-----|
| actual_tokens | ~350,000（含多轮 code review 修正） |
| model_used | zs-glm-5.2 |
| actual_cost | ~$8 |
| cost_warn | green（< $10） |
