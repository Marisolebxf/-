# API 契约：gkx-ai-service 企业评估接口（供 Java Feign 对接）

- **整理人**：data-agent
- **时间**：2026-07-21
- **任务**：ENT-PY-EVAL-TASK
- **服务**：gkx-ai-service（`demo-svc-topic-py` 仓 `gkx_ai_service/` 子项目）
- **端口**：8081（dev）
- **路由前缀**：`/internal/gkx-ai/evaluation`
- **当前模式**：Mock 优先（`GKX_MOCK_ENABLED=true`），评分结果为确定性 Mock；算法侧 `ENT-ALGO-EVAL-INTERACTIVE` 就绪后切 `false` 走真实 entan
- **响应包络**：统一 `{code, msg, data}`，`code=0` 成功，`code!=0` 业务错误

> **Java 对接要点**：新建独立 FeignClient（`RemoteEnterpriseAiPythonClient`），不要复用 `RemoteEnterprisePythonClient`（那个指向 gkx-search-service:8080）。下游寻址配置项：`gkxlumen.topic.enterprise.python-ai-base-url`（或 Nacos 服务发现 `gkx-ai-service`）。

---

## 1. 接口清单

| # | 方法 | 路径 | 作用 | 异步 |
|---|---|---|---|---|
| 1 | POST | `/internal/gkx-ai/evaluation/precheck` | 数据预检（企业存在性 + 数量上限） | 否 |
| 2 | POST | `/internal/gkx-ai/evaluation/tasks` | 创建评估任务 | 是（立即返回 task_id） |
| 3 | POST | `/internal/gkx-ai/evaluation/tasks/{task_id}/status` | 查任务状态 | 否 |
| 4 | POST | `/internal/gkx-ai/evaluation/tasks/{task_id}/result` | 查评估结果 | 否 |
| 5 | POST | `/internal/gkx-ai/evaluation/tasks/history` | 历史任务列表 | 否 |
| 6 | POST | `/internal/gkx-ai/evaluation/templates` | 评估模板列表 | 否 |
| 7 | POST | `/internal/gkx-ai/evaluation/templates/create` | 创建评估模板 | 否 |

---

## 2. 逐接口契约

### 2.1 数据预检

`POST /internal/gkx-ai/evaluation/precheck`

**请求体**：

```json
{
  "enterprise_codes": ["6bc50eca3435d4b53fb7bf661d058a47", "6eeabc4997a7838e86d559ac0c9bc93e"]
}
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| enterprise_codes | string[] | 是 | 企业 org_id 列表，1-50 个 |

**响应**：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "total": 2,
    "found": 2,
    "missing_codes": [],
    "ready": true,
    "data_source": "mock"
  }
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| total | int | 传入企业总数 |
| found | int | 找到的企业数 |
| missing_codes | string[] | 不存在的企业 code 列表 |
| ready | bool | 是否可生成（missing 为空且未超上限） |
| data_source | string | `mock` / `search` |

---

### 2.2 创建评估任务

`POST /internal/gkx-ai/evaluation/tasks`

**请求体**：

```json
{
  "enterprise_codes": ["6bc50eca3435d4b53fb7bf661d058a47", "6eeabc4997a7838e86d559ac0c9bc93e"],
  "weights": {"innovation": 0.5, "operation": 0.2, "growth": 0.2, "risk": 0.1},
  "template_id": "TPL-INNOVATION",
  "task_name": "2026Q3技术力评估",
  "created_by": "user001"
}
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| enterprise_codes | string[] | 是 | 企业 org_id 列表，1-50 个 |
| weights | object | 否 | 自定义权重，键为维度名，值为 0-1 浮点数；缺省用模板或默认 |
| template_id | string | 否 | 评估模板 ID；提供时取模板权重作为默认 |
| task_name | string | 否 | 任务名称；缺省自动生成 |
| created_by | string | 否 | 创建人 ID |

**权重优先级**：显式 `weights` > `template_id` 模板权重 > 内置默认（四维各 0.25）

**维度键名**（固定 4 个）：

| 键 | 含义 |
|---|---|
| innovation | 创新能力 |
| operation | 经营能力 |
| growth | 成长性 |
| risk | 风险水平 |

**响应**：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "task_id": "EVAL-dcc4b5a2bd1d",
    "status": "pending"
  }
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| task_id | string | 任务 ID（EVAL- 开头） |
| status | string | 初始状态 `pending`，后台异步执行 |

---

### 2.3 查任务状态

`POST /internal/gkx-ai/evaluation/tasks/{task_id}/status`

**路径参数**：`task_id`

**请求体**：空（可传 `{}`）

**响应**：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "task_id": "EVAL-dcc4b5a2bd1d",
    "status": "success",
    "progress": 100,
    "error": null,
    "created_at": "2026-07-21T09:26:06.114826+00:00",
    "updated_at": "2026-07-21T09:26:06.115491+00:00"
  }
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| task_id | string | 任务 ID |
| status | string | `pending` / `running` / `success` / `failed` |
| progress | int | 0-100 |
| error | string\|null | 失败原因 |
| created_at | string | ISO8601 时间 |
| updated_at | string | ISO8601 时间 |

**状态流转**：`pending`(0) → `running`(10-90) → `success`(100) 或 `failed`

**Java 轮询建议**：前端提交后每 2-3 秒轮询一次 status，`status==success` 或 `status==failed` 时停止。

---

### 2.4 查评估结果

`POST /internal/gkx-ai/evaluation/tasks/{task_id}/result`

**路径参数**：`task_id`

**请求体**：空（可传 `{}`）

**响应（成功）**：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "scores": [
      {
        "enterprise_code": "68dd51ce03544ad958d3533729d954b6",
        "total_score": 73.91,
        "rank": 1,
        "dimensions": {
          "innovation": 73.27,
          "operation": 54.93,
          "growth": 86.15,
          "risk": 81.29
        },
        "weights": {"innovation": 0.25, "operation": 0.25, "growth": 0.25, "risk": 0.25},
        "data_source": "mock",
        "model_version": "mock-v0.1"
      },
      {
        "enterprise_code": "6bc50eca3435d4b53fb7bf661d058a47",
        "total_score": 68.63,
        "rank": 2,
        "dimensions": {"innovation": 56.96, "operation": 63.93, "growth": 85.02, "risk": 68.61},
        "weights": {"innovation": 0.25, "operation": 0.25, "growth": 0.25, "risk": 0.25},
        "data_source": "mock",
        "model_version": "mock-v0.1"
      }
    ],
    "data_source": "mock",
    "model_version": "mock-v0.1"
  }
}
```

**响应（任务未完成）**：

```json
{
  "code": 409,
  "msg": "任务未完成，当前状态: running",
  "data": {"status": "running", "progress": 60}
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| scores | object[] | 评分列表，按 total_score 降序（rank 1 起） |
| scores[].enterprise_code | string | 企业 org_id |
| scores[].total_score | float | 综合得分（加权汇总，0-100） |
| scores[].rank | int | 排名（1 起） |
| scores[].dimensions | object | 各维度得分（0-100），键为 innovation/operation/growth/risk |
| scores[].weights | object | 本次使用的权重 |
| scores[].data_source | string | `mock` / `entan` |
| scores[].model_version | string | 算法版本 |
| data_source | string | 顶层冗余 |
| model_version | string | 顶层冗余 |

---

### 2.5 历史任务列表

`POST /internal/gkx-ai/evaluation/tasks/history`

**请求体**：

```json
{
  "page": 1,
  "size": 20,
  "status": "success"
}
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| page | int | 否 | 页码，默认 1 |
| size | int | 否 | 每页条数，默认 20 |
| status | string | 否 | 状态过滤（pending/running/success/failed） |

**响应**：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "total": 1,
    "page": 1,
    "size": 20,
    "items": [
      {
        "task_id": "EVAL-dcc4b5a2bd1d",
        "task_name": "2026Q3技术力评估",
        "status": "success",
        "enterprise_count": 3,
        "created_by": "user001",
        "created_at": "2026-07-21T09:26:06.114826+00:00",
        "updated_at": "2026-07-21T09:26:06.115491+00:00"
      }
    ]
  }
}
```

---

### 2.6 评估模板列表

`POST /internal/gkx-ai/evaluation/templates`

**请求体**：空（可传 `{}`）

**响应**：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "items": [
      {
        "template_id": "TPL-INNOVATION",
        "name": "创新驱动型",
        "description": "侧重创新能力评估",
        "weights": {"innovation": 0.5, "operation": 0.2, "growth": 0.2, "risk": 0.1},
        "created_at": "...",
        "updated_at": "..."
      },
      {
        "template_id": "TPL-BALANCED",
        "name": "综合均衡型",
        "description": "四维均衡权重",
        "weights": {"innovation": 0.25, "operation": 0.25, "growth": 0.25, "risk": 0.25},
        "created_at": "...",
        "updated_at": "..."
      }
    ],
    "total": 2
  }
}
```

**预置模板**：

| template_id | name | 权重 |
|---|---|---|
| TPL-INNOVATION | 创新驱动型 | innovation:0.5 / operation:0.2 / growth:0.2 / risk:0.1 |
| TPL-BALANCED | 综合均衡型 | 四维各 0.25 |

---

### 2.7 创建评估模板

`POST /internal/gkx-ai/evaluation/templates/create`

**请求体**：

```json
{
  "name": "风险规避型",
  "description": "侧重风险控制",
  "weights": {"innovation": 0.1, "operation": 0.2, "growth": 0.2, "risk": 0.5}
}
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| name | string | 是 | 模板名称 |
| description | string | 否 | 描述 |
| weights | object | 是 | 权重，键为维度名，值为 0-1 浮点数 |

**响应**：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "template_id": "TPL-e6bff562",
    "name": "风险规避型",
    "description": "侧重风险控制",
    "weights": {"innovation": 0.1, "operation": 0.2, "growth": 0.2, "risk": 0.5},
    "created_at": "...",
    "updated_at": "..."
  }
}
```

---

## 3. Java Feign 对接建议

### 3.1 新建 FeignClient

不要复用 `RemoteEnterprisePythonClient`（指向 gkx-search-service:8080）。新建 `RemoteEnterpriseAiPythonClient`，指向 gkx-ai-service:8081。

```java
@FeignClient(contextId = "remoteEnterpriseAiPythonClient",
    name = "topic-enterprise-ai-python",
    configuration = EnterpriseAiPythonFeignConfig.class)
public interface RemoteEnterpriseAiPythonClient {

    @PostMapping("/internal/gkx-ai/evaluation/precheck")
    R<EvalPrecheckResponse> precheck(@RequestBody EvalPrecheckRequest request);

    @PostMapping("/internal/gkx-ai/evaluation/tasks")
    R<EvalTaskCreateResponse> createTask(@RequestBody EvalTaskCreateRequest request);

    @PostMapping("/internal/gkx-ai/evaluation/tasks/{taskId}/status")
    R<EvalTaskStatusResponse> taskStatus(@PathVariable("taskId") String taskId);

    @PostMapping("/internal/gkx-ai/evaluation/tasks/{taskId}/result")
    R<EvalTaskResultResponse> taskResult(@PathVariable("taskId") String taskId);

    @PostMapping("/internal/gkx-ai/evaluation/tasks/history")
    R<EvalTaskHistoryResponse> taskHistory(@RequestBody EvalTaskHistoryRequest request);

    @PostMapping("/internal/gkx-ai/evaluation/templates")
    R<EvalTemplateListResponse> templates();

    @PostMapping("/internal/gkx-ai/evaluation/templates/create")
    R<EvalTemplateResponse> createTemplate(@RequestBody EvalTemplateCreateRequest request);
}
```

### 3.2 下游寻址配置

复用现有 `EnterprisePythonFeignConfig` 范式，新建 `EnterpriseAiPythonFeignConfig`：

- `gkxlumen.topic.enterprise.python-ai-base-url` 非空 → 直连
- 为空 → Nacos 服务发现 `gkx-ai-service`

### 3.3 对外 REST 路径建议

Java 门面对前端暴露（`@RequestMapping("/topic/v1")`）：

| 对外路径 | 转发到 |
|---|---|
| `POST /topic/v1/evaluation/precheck` | gkx-ai precheck |
| `POST /topic/v1/evaluation/tasks` | gkx-ai tasks |
| `POST /topic/v1/evaluation/tasks/{taskId}/status` | gkx-ai status |
| `POST /topic/v1/evaluation/tasks/{taskId}/result` | gkx-ai result |
| `POST /topic/v1/evaluation/tasks/history` | gkx-ai history |
| `POST /topic/v1/evaluation/templates` | gkx-ai templates |
| `POST /topic/v1/evaluation/templates/create` | gkx-ai create |

---

## 4. 联调说明

### 4.1 Mock 模式（当前可用）

gkx-ai-service 当前 `GKX_MOCK_ENABLED=true`，7 端点全部可用，返回确定性 Mock 评分。Java 可立即对接。

### 4.2 联调验证步骤

1. 启动 gkx-ai-service：`GKX_MOCK_ENABLED=true uvicorn gkx_ai_service.main:app --port 8081`
2. 取 3 个 Mock org_id：
   ```
   6bc50eca3435d4b53fb7bf661d058a47
   6eeabc4997a7838e86d559ac0c9bc93e
   68dd51ce03544ad958d3533729d954b6
   ```
3. Java Feign 调 precheck → create task → 轮询 status → 取 result
4. 期望 result 含 3 家企业评分排名（rank 1/2/3），`data_source=mock`

### 4.3 算法切换后

`ENT-ALGO-EVAL-INTERACTIVE` 就绪后，gkx-ai-service 切 `GKX_MOCK_ENABLED=false`，**Java 代码零改动**，返回结构不变，仅 `data_source` 从 `mock` 变 `entan`。

---

## 5. 已知限制（当前版本）

| 项 | 现状 | 后续 |
|---|---|---|
| 评分来源 | Mock（md5 种子） | entan 真实算法 |
| 任务持久化 | 进程内 dict（重启丢失） | 接 PG eval_task/eval_task_result 表（DDL 已就绪） |
| 评估维度 | 固定 4 维（innovation/operation/growth/risk） | 待算法侧对齐 UI 三模式（technology/business/competitiveness） |
| D9 血缘 | 仅 data_source/model_version | 补 metric_id/formula/source_tables 8 件套 |
| 数据预检覆盖度 | 仅校验企业存在性 | 补字段级覆盖率/可信度（对齐 Wireframe F-EVAL-01 §④） |
