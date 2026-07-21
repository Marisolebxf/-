# 派单包：ENT-JAVA-EVAL — Java 企业评估门面对接 gkx-ai-service

- **任务 ID**：ENT-JAVA-EVAL
- **派发角色**：architect-agent（[human:徐滕强] 监管）
- **承接角色**：api-agent
- **仓**：`lumen-svc-platform`
- **模块**：`gkxlumen-topic-enterprise`
- **依赖**：`ENT-PY-EVAL-TASK`（已完工，Mock 模式可用）
- **派发时间**：2026-07-21

---

## 1. 背景

数据侧 `gkx_ai_service`（`demo-svc-topic-py`）已落地企业评估任务编排层 7 端点（`/internal/gkx-ai/evaluation/*`），当前 Mock 模式全链路跑通。Java 侧需建 Feign Client 对接，对外暴露 `/topic/v1/evaluation/*` 供前端调用。

### 调用链

```
前端 → Java(gkxlumen-topic) /topic/v1/evaluation/*
         → Python(gkx_ai_service) /internal/gkx-ai/evaluation/*
              ├─ 任务创建/状态/结果/历史/模板（gkx_ai_service 自管）
              ├─ 数据预检（调 gkx_search_service 既有企业数据）
              └─ 评估计算（Mock 或 HTTP 调 entan，Java 无感知）
```

### 关键约束

1. **新建独立 FeignClient**：`RemoteEnterpriseAiPythonClient`，**不复用** `RemoteEnterprisePythonClient`（后者指向 gkx-search-service:8080，评估服务在 gkx-ai-service:8081）
2. **算法切换 Java 零改动**：gkx_ai_service 当前 Mock 模式，算法侧 `ENT-ALGO-EVAL-INTERACTIVE` 就绪后切 `GKX_MOCK_ENABLED=false`，返回结构不变，Java 无感知
3. **Convoy Risk 隔离**：全新建文件，不混改 `EnterpriseOpenApiController`

---

## 2. 接口契约（data-agent 已整理）

**完整契约文档**：`agent-handoffs/企业战略分析-ENT/API-ENT-EVAL-contract.md`

### 2.1 下游端点（gkx-ai-service，prefix `/internal/gkx-ai/evaluation`）

| # | 方法 | 路径 | 作用 |
|---|---|---|---|
| 1 | POST | `/precheck` | 数据预检 |
| 2 | POST | `/tasks` | 创建评估任务（异步，返回 task_id） |
| 3 | POST | `/tasks/{task_id}/status` | 查任务状态 |
| 4 | POST | `/tasks/{task_id}/result` | 查评估结果 |
| 5 | POST | `/tasks/history` | 历史任务列表 |
| 6 | POST | `/templates` | 评估模板列表 |
| 7 | POST | `/templates/create` | 创建评估模板 |

### 2.2 对外端点（Java 门面，prefix `/topic/v1/evaluation`）

| 对外路径 | 转发到 |
|---|---|
| `POST /topic/v1/evaluation/precheck` | gkx-ai precheck |
| `POST /topic/v1/evaluation/tasks` | gkx-ai tasks |
| `POST /topic/v1/evaluation/tasks/{taskId}/status` | gkx-ai status |
| `POST /topic/v1/evaluation/tasks/{taskId}/result` | gkx-ai result |
| `POST /topic/v1/evaluation/tasks/history` | gkx-ai history |
| `POST /topic/v1/evaluation/templates` | gkx-ai templates |
| `POST /topic/v1/evaluation/templates/create` | gkx-ai create |

### 2.3 核心数据结构

**评估维度**（固定 4 个）：

| 键 | 含义 |
|---|---|
| innovation | 创新能力 |
| operation | 经营能力 |
| growth | 成长性 |
| risk | 风险水平 |

**任务状态流转**：`pending`(0) → `running`(10-90) → `success`(100) / `failed`

**评分结果结构**：

```json
{
  "scores": [
    {
      "enterprise_code": "org_id",
      "total_score": 73.91,
      "rank": 1,
      "dimensions": {"innovation": 73.27, "operation": 54.93, "growth": 86.15, "risk": 81.29},
      "weights": {"innovation": 0.25, "operation": 0.25, "growth": 0.25, "risk": 0.25},
      "data_source": "mock",
      "model_version": "mock-v0.1"
    }
  ],
  "data_source": "mock",
  "model_version": "mock-v0.1"
}
```

---

## 3. 任务范围

### 3.1 必做（DoD）

1. **新建 FeignClient**：`RemoteEnterpriseAiPythonClient`，7 个方法对应 7 端点
2. **新建 FeignConfig**：`EnterpriseAiPythonFeignConfig`，下游寻址配置项 `gkxlumen.topic.enterprise.python-ai-base-url`（非空直连，为空走 Nacos `gkx-ai-service`）
3. **新建 DTO**：请求/响应 DTO（`EvalPrecheckRequest/Response`、`EvalTaskCreateRequest/Response`、`EvalTaskStatusResponse`、`EvalTaskResultResponse`、`EvalTaskHistoryRequest/Response`、`EvalTemplateResponse`、`EvalTemplateCreateRequest`）
4. **新建 Controller**：`EnterpriseEvaluationController`，`@RequestMapping("/topic/v1/evaluation")`，7 个端点
5. **新建 Service**：`EnterpriseEvaluationService` + `Impl`，Controller → Service → FeignClient 三层
6. **全新建文件**：不混改 `EnterpriseOpenApiController` / `RemoteEnterprisePythonClient`（Convoy 隔离）
7. **本地 Maven + JDK17 编译通过**
8. **handoff 文档** + 架构合规自检 + cost 四字段

### 3.2 不做（禁止项）

1. ❌ 不改 `EnterpriseOpenApiController` — 评估端点独立 Controller
2. ❌ 不改 `RemoteEnterprisePythonClient` — 新建独立 Ai FeignClient
3. ❌ 不写评估算法 — Java 只做透传/门面，算法在 Python 侧
4. ❌ 不直连 entan — 只调 gkx-ai-service 屏蔽层
5. ❌ 不直读 DB — 评估任务/结果/模板由 gkx-ai-service 自管

---

## 4. FeignClient 骨架参考

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

---

## 5. 联调验证

### Mock 模式（当前可用）

1. gkx-ai-service 已部署或本地启动：`GKX_MOCK_ENABLED=true uvicorn gkx_ai_service.main:app --port 8081`
2. 可用 Mock org_id：
   ```
   6bc50eca3435d4b53fb7bf661d058a47
   6eeabc4997a7838e86d559ac0c9bc93e
   68dd51ce03544ad958d3533729d954b6
   ```
3. Java Feign 调 precheck → create task → 轮询 status（2-3s/次）→ 取 result
4. 期望 result 含 3 家企业评分排名（rank 1/2/3），`data_source=mock`

### 算法切换后

`ENT-ALGO-EVAL-INTERACTIVE` 就绪后，gkx-ai-service 切 `GKX_MOCK_ENABLED=false`，**Java 代码零改动**，返回结构不变，仅 `data_source` 从 `mock` 变 `entan`。

---

## 6. 架构合规自检（§2 铁律）

| # | 铁律 | 本次 | 说明 |
|---|---|---|---|
| 1 | 算法只在 Python | ✅ | Java 只做门面透传，不写算法 |
| 2 | 调用链前端→Java→Python | ✅ | Java→gkx-ai-service(`/internal/*`) |
| 3 | 图谱 NebulaGraph | N/A | 本任务不涉图 |
| 4 | 可观测性 | ✅ | Feign 透传 trace 头；Java Agent 监控 |
| 5 | CI/CD | ✅ | lumen-svc-platform 走 PR + CI |
| 6 | demo2 不 merge lumen | ✅ | 本任务在 lumen 正式仓 |
| 7 | 共享聚合核心 | ✅ | 评估经 gkxlumen-topic |
| 8 | 数据走 ADS | ✅ | Java 不直读库，数据由 Python 侧管 |
| 9 | D8 前端规范 | N/A | 本任务不涉前端 |
| 10 | D9 数据血缘 | ⚠️ | gkx-ai-service 当前仅 data_source/model_version，后续补 metric_id；Java 透传不丢字段 |

---

## 7. DoD 清单

- [ ] 新建 `RemoteEnterpriseAiPythonClient`（7 方法，独立 FeignClient，不混入 search client）
- [ ] 新建 `EnterpriseAiPythonFeignConfig`（下游寻址 `python-ai-base-url` / Nacos）
- [ ] 新建 7 对 DTO（请求/响应）
- [ ] 新建 `EnterpriseEvaluationController`（`/topic/v1/evaluation/*` 7 端点）
- [ ] 新建 `EnterpriseEvaluationService` + `Impl`（三层）
- [ ] 全新建文件，不混改现有 Controller / FeignClient
- [ ] 本地 Maven + JDK17 编译通过
- [ ] Mock 模式 Feign 联调通过（precheck → task → status → result 全链路）
- [ ] handoff 文档 + 架构合规自检 + cost 四字段

---

## 8. cost 预估

- estimated_tokens: 120_000
- effort_points: 5
- difficulty: M
- 预计耗时：1 天
