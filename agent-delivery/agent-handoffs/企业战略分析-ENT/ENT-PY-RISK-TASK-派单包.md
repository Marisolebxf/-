# 派单包：ENT-PY-RISK-TASK（v3.2）

- **派单方**：coordinator（architect-agent 起草）
- **执行 Agent**：`data-agent`
- **监管人**：human:徐滕强
- **仓**：`demo-svc-topic-py`
- **子项目**：`gkx_ai_service/`（与 EVAL 同子项目，复用已有骨架）
- **依赖**：`ENT-ARCH-ANALYSIS-TASK-DOC`、`ENT-MOD-RISK-PDR-G1`、`ENT-PY-ANALYSIS-CALLBACK`、`ENT-ALGO-SCIENCE-ASYNC-FRAME`
- **状态**：`backlog`
- **架构真源**：`ARCH-ANALYSIS-TASK-设计方案.md` **v3.2** §10

---

## 0. 铁律前置（违反必拒）

1. **本任务只在 `demo-svc-topic-py` 仓**，复用 `gkx_ai_service/` 子项目（EVAL 已建骨架）。**禁止**修改 `demo-algo-science`（算法组项目）
2. **gkx_ai_service 是算法服务的屏蔽层**。Java 只调 gkx_ai_service `/internal/gkx-ai/risk/*`；gkx_ai_service 内部 HTTP 调 science 算法；需要基础数据时调 gkx_search_service
3. **算法只在 Python**。本任务是数据编排层，不做算法计算（图谱构建/痛点诊断由 science 提供）
4. **Mock 优先**。science 异步框架未就绪前，用 Mock 结果；切换时仅改内部 HTTP 客户端，`/internal/gkx-ai/risk/*` 契约不变
5. **数据血缘 D9**。结果中每个统计指标须可追溯 metric_id 或标 🟡 GAP
6. **taskId 由 Java 唯一生成**，Python 复用，不自生成
7. **pending 只在算法侧**，Python status 不返回 pending，回调/查询映射为 running

---

## 1. 目标

在 `gkx_ai_service` 新增 `/internal/gkx-ai/risk/tasks` 场景适配，屏蔽 science 算法接口差异。
Python 不作为正式历史、状态和结果真源——正式真源为 Java MySQL `analysis_task`。

---

## 2. 端点（4 个，prefix=`/internal/gkx-ai/risk`）

| # | 端点 | 方法 | 功能 |
|---|---|---|---|
| 1 | `/tasks` | POST | 接收 Java taskId，适配并转发算法任务 |
| 2 | `/tasks/{task_id}/status` | POST | 算法任务状态适配，供 Java 修正器调用 |
| 3 | `/tasks/{task_id}/result` | POST | 按 subType 返回风险洞察结果 |
| 4 | `/tasks/{task_id}/cancel` | POST | 逻辑取消 |

> Python **不提供** `/tasks/history`（历史只查 Java MySQL）。
> Python **不提供** 同步辅助接口（风险洞察无 industries/indicators/precheck/compare）。

---

## 3. 请求/响应契约

### 3.1 创建任务 `POST /tasks`

**请求体**：

```json
{
  "task_id": "RISK-20260725-001",
  "analysisType": "risk_insight",
  "callbackUrl": "http://gkx-ai-service:8081/internal/gkx-ai/analysis/callback",
  "params": {
    "subType": "supply_chain",
    "enterpriseCodes": ["6bc50eca...", "6eeabc49..."],
    "relationScope": ["supplier", "customer", "partner"],
    "displayMode": "expand_by_node"
  }
}
```

**pain_points 请求体**：

```json
{
  "task_id": "RISK-20260725-002",
  "analysisType": "risk_insight",
  "callbackUrl": "...",
  "params": {
    "subType": "pain_points",
    "enterpriseCodes": ["6bc50eca..."],
    "diagnosisScope": ["tech_rd", "market_expand", "financing", "management"],
    "diagnosisMethod": "joint_common"
  }
}
```

**响应**（立即返回，不等待算法完成）：

```json
{
  "code": 0,
  "data": {
    "task_id": "RISK-20260725-001",
    "status": "running"
  }
}
```

> Python 收到请求后立即返回 `running`，算法异步执行，完成后通过 callback 通知。

### 3.2 查询状态 `POST /tasks/{task_id}/status`

**响应**：

```json
{
  "code": 0,
  "data": {
    "task_id": "RISK-20260725-001",
    "status": "running",
    "current_stage": "compute",
    "stages": [
      {"name": "task_submit", "status": "done", "elapsed_ms": 120},
      {"name": "data_gather", "status": "done", "elapsed_ms": 320},
      {"name": "compute", "status": "running", "elapsed_ms": 1800},
      {"name": "result_assembly", "status": "pending"}
    ],
    "elapsed_ms": 2240
  }
}
```

**状态枚举**：
- Python status 接口返回 `running` / `success` / `failed`
- **不返回 `pending`**：算法侧 pending（排队待跑）映射为 `running` 回传 Java
- Java 侧只有 `running` / `success` / `failed` / `cancelled`（cancelled 由 Java 逻辑取消触发，Python 收到 cancel 后回 `cancelled`）

### 3.3 查询结果 `POST /tasks/{task_id}/result`

**结果契约**：以 `ARCH-ANALYSIS-TASK-设计方案.md` v3.2 §10.3 为最终契约。

- **supply_chain**：任务摘要 + 图谱（nodes[]/edges[]/maxDepth=3）+ 统计 + 关键节点 Tab + 断链风险 Tab + 报告区
- **pain_points**：对象与诊断摘要 + 四维诊断卡片 + 共性问题 TopN + 报告区

> 大结果（供应链 3 级图谱可能很大）由 **Python** 判断阈值后写 MinIO（camelCase），转发 `resultUrl` 给 Java；MySQL 只留指针。Java 不碰分析结果 MinIO（v3.2 D-30 修订）。

### 3.4 取消 `POST /tasks/{task_id}/cancel`

逻辑取消（见 ARCH §4.6 / D-31）：
- Python 标记内存 `cancelled` + **同步透传**给算法 `POST /gdf/tasks/{task_id}/cancel`
- 算法收到后设 `cancel_flag`，**每个节点开始时检查**，命中则终止
- 算法取消后发 `task_cancelled` Webhook（**不是 `task_failed`**）
- Python 收到 `task_cancelled` 回调后转发 Java
- 响应 `{code: 0, data: {task_id, status: "cancelled"}}`

---

## 4. 子类型枚举与参数校验

| subType | 名称 | 必填参数 | 可选参数 |
|---|---|---|---|
| `supply_chain` | 供应链关系 | `enterpriseCodes[]` + `relationScope[]`（supplier/customer/partner） | `displayMode`（默认 expand_by_node） |
| `pain_points` | 发展痛难点 | `enterpriseCodes[]` + `diagnosisScope[]`（tech_rd/market_expand/financing/management） | `diagnosisMethod`（默认 joint_common） |

---

## 5. Mock 策略

- science 异步框架（`ENT-ALGO-SCIENCE-ASYNC-FRAME`）未就绪前，gkx_ai_service 自造 Mock 结果
- supply_chain Mock：固定 3 级图谱快照（5 节点 / 8 边），含关键节点和断链风险
- pain_points Mock：四维诊断卡片 + 3 条共性问题
- 标注 🧪 MockBadge；指标受阻断的标 ⚠️
- 切换 science 时仅改 `science_client.py` 内部实现，`/internal/gkx-ai/risk/*` 契约不变

---

## 6. 服务间调用

```
Java → gkx_ai_service /internal/gkx-ai/risk/tasks
  → science_client.py HTTP 调 science /gdf/tasks（create-and-start）
  → 需要基础数据时调 gkx_search_service /internal/gkx-search/* 
  → 算法完成后回调 gkx_ai_service /internal/gkx-ai/analysis/callback
  → Python 转发 Java /topic/v1/analysis/callback/risk
```

---

## 6.5 JSON 字段命名风格（D-30）

> **Python ↔ 算法侧统一 `snake_case`**；Java 侧用 `camelCase`。常规字段 Java 用 `@JsonProperty` 对接 snake_case；**分析结果 `result` 例外**：Python 转 camelCase 后转发 Java（v3.2 D-30 修订）。大结果 Python 写 MinIO（camelCase）转发 resultUrl，Java 不碰分析结果层面的 MinIO。

Python 侧所有 JSON 请求/响应字段一律 `snake_case`：`task_id` / `analysis_type` / `sub_type` / `enterprise_codes` / `callback_url` / `event` / `node_code` / `node_name` / `status` 等。result JSON 例外：Python 转 camelCase 后转发 Java。

---

## 7. 禁止

- 修改 `demo-algo-science` 仓任何文件（算法组项目）
- 把风险代码写进 `gkx_search_service/`（违反服务边界，风险归 ai-service）
- 在 gkx_ai_service 写图谱算法/诊断算法——这些归 science
- 对 Java 暴露 science 的原始路径（必须经 gkx_ai_service 屏蔽）
- 自生成 taskId（必须复用 Java 传入的）
- 返回 `pending` 状态给 Java
- 维护正式任务历史（历史只查 Java MySQL）
- 提供 `/tasks/history` 端点

---

## 8. DoD

1. `gkx_ai_service/views/risk.py` 4 端点齐全（tasks/status/result/cancel）
2. 两个 subType 的创建、状态、结果、取消契约测试通过
3. 3 级图谱、痛难点四维结果、错误和超时场景覆盖
4. taskId 复用 Java 传入值，不自生成
5. status 不返回 pending，映射为 running
6. Mock 模式跑通创建→状态→结果→取消全链路
7. science_client.py 对接 science `/gdf/tasks`，Mock/真实切换不改变 Java 契约
8. 大结果由 Python 判断阈值写 MinIO（camelCase）并转发 resultUrl
9. D9 血缘字段（metric_id/calc_process/source_tables/pending_ref）齐全
10. `/internal/*` 路径、OTel、CI、handoff 与 cost 四字段齐全
