# 派单包：ENT-JAVA-EVAL — Java 企业评估场景适配（v3.0）

- **任务 ID**：ENT-JAVA-EVAL
- **派发角色**：architect-agent（[human:徐滕强] 监管）
- **承接角色**：api-agent
- **仓**：`lumen-svc-platform`
- **模块**：`gkxlumen-topic-enterprise`
- **依赖**：`ENT-ARCH-ANALYSIS-TASK-DOC`、`ENT-JAVA-ANALYSIS-CORE`、`ENT-PY-EVAL-TASK`
- **派发时间**：2026-07-21

---

> **2026-07-24 范围变更**：本任务不再建设 `/topic/v1/evaluation/tasks*` 第二套任务中心。
> 正式任务创建、状态、结果和历史统一走 Java `/api/analysis/tasks*`，并落
> `analysis_task`。本任务只实现 `enterprise_eval` 场景适配、同步辅助接口和 Java 模板管理。

---

## 1. 背景

数据侧 `gkx_ai_service` 提供企业评估 8 个适配接口。Java 侧由
`ENT-JAVA-ANALYSIS-CORE` 建统一编排中心；本任务为该中心提供企业评估场景适配器，
并保留行业、指标、预检、双企对比等同步接口。系统模板和个人模板在 Java MySQL 管理。

### 调用链

```
前端 → Java /api/analysis/tasks*（任务生命周期唯一入口）
         → enterprise_eval 场景适配器
              → Python /internal/gkx-ai/evaluation/tasks*

前端 → Java /topic/v1/evaluation/{industries|indicators|precheck|compare|templates*}
         → Python 同步适配（模板除外）或 Java MySQL（模板）
```

### 关键约束

1. **新建独立 FeignClient**：`RemoteEnterpriseAiPythonClient`，**不复用** `RemoteEnterprisePythonClient`（后者指向 gkx-search-service:8080，评估服务在 gkx-ai-service:8081）
2. **算法切换 Java 零改动**：gkx_ai_service 当前 Mock 模式，算法侧 `ENT-ALGO-EVAL-INTERACTIVE` 就绪后切 `GKX_MOCK_ENABLED=false`，返回结构不变，Java 无感知
3. **Convoy Risk 隔离**：全新建文件，不混改 `EnterpriseOpenApiController`

---

## 2. 接口契约（data-agent 已整理）

**完整契约文档**：`agent-handoffs/企业战略分析-ENT/API-ENT-EVAL-contract.md`

### 2.1 下游端点（gkx-ai-service）

| # | 方法 | 路径 | 作用 |
|---|---|---|---|
| 1 | POST | `/industries` | 行业列表 |
| 2 | POST | `/indicators` | 指标树和默认权重 |
| 3 | POST | `/precheck` | 数据预检 |
| 4 | POST | `/tasks` | 创建算法任务 |
| 5 | POST | `/tasks/{task_id}/status` | 算法任务状态 |
| 6 | POST | `/tasks/{task_id}/result` | 多态评估结果 |
| 7 | POST | `/tasks/{task_id}/compare` | 双企对比 |
| 8 | POST | `/tasks/history` | 仅 svc 自测/状态兜底 |

### 2.2 Java 对外边界

| 对外路径 | 责任 |
|---|---|
| `/api/analysis/tasks*` | ENT-JAVA-ANALYSIS-CORE；任务唯一入口 |
| `/topic/v1/evaluation/industries` | Feign 透传 Python |
| `/topic/v1/evaluation/indicators` | Feign 透传 Python |
| `/topic/v1/evaluation/precheck` | Feign 透传 Python |
| `/topic/v1/evaluation/tasks/{taskId}/compare` | Feign 透传 Python |
| `/topic/v1/evaluation/templates*` | Java 系统/个人模板 CRUD |

> 禁止新增模块私有的 tasks/status/result/history；正式历史只查 Java MySQL。

### 2.3 核心数据结构

**评估维度**（固定 4 个）：

| 键 | 含义 |
|---|---|
| innovation | 创新能力 |
| operation | 经营能力 |
| growth | 成长性 |
| risk | 风险水平 |

**任务状态流转**：Java 侧只有 `running/success/failed/cancelled`，无 `pending`。

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

1. **新建 FeignClient**：`RemoteEnterpriseAiPythonClient`，8 个方法对应 Python 契约
2. **新建 FeignConfig**：`EnterpriseAiPythonFeignConfig`，下游寻址配置项 `gkxlumen.topic.enterprise.python-ai-base-url`（非空直连，为空走 Nacos `gkx-ai-service`）
3. **场景适配器**：实现 `enterprise_eval` 的 create/status/result 路由，接入统一 `AnalysisTaskService`
4. **同步 Controller**：仅暴露 industries/indicators/precheck/compare
5. **模板管理**：Java MySQL 系统模板 + 个人模板 CRUD，含用户隔离、默认互斥和版本快照
6. **全新建文件**：不混改 `EnterpriseOpenApiController` / `RemoteEnterprisePythonClient`（Convoy 隔离）
7. **本地 Maven + JDK17 编译通过**
8. **handoff 文档** + 架构合规自检 + cost 四字段

### 3.2 不做（禁止项）

1. ❌ 不改 `EnterpriseOpenApiController` — 评估端点独立 Controller
2. ❌ 不改 `RemoteEnterprisePythonClient` — 新建独立 Ai FeignClient
3. ❌ 不写评估算法 — Java 只做透传/门面，算法在 Python 侧
4. ❌ 不直连 entan — 只调 gkx-ai-service 屏蔽层
5. ❌ 不另建评估任务表 — 复用统一 `analysis_task`
6. ❌ 不把模板转发给 Python — 模板属于 Java 业务配置
7. ❌ 不暴露第二套 tasks/status/result/history API

---

## 4. 场景适配骨架

```java
@Component
public class EnterpriseEvalAnalysisAdapter implements AnalysisTypeAdapter {
    public String analysisType() {
        return "enterprise_eval";
    }

    public DownstreamTaskRef create(AnalysisTask task, JsonNode params) {
        // Java taskId 向下传递；调用 /internal/gkx-ai/evaluation/tasks
    }
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
3. Java 同步门面调 precheck；统一编排中心完成 create → status → result
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
| 8 | 数据走 ADS | ✅ | Java 模板写业务配置表；分析数据仍按架构契约读取 |
| 9 | D8 前端规范 | N/A | 本任务不涉前端 |
| 10 | D9 数据血缘 | ✅ | Java 透传 metric_id/calc_process/pending_ref，不丢字段 |

---

## 7. DoD 清单

- [ ] 新建 `RemoteEnterpriseAiPythonClient`（8 方法，独立 FeignClient）
- [ ] 新建 `EnterpriseAiPythonFeignConfig`（下游寻址 `python-ai-base-url` / Nacos）
- [ ] 实现 `enterprise_eval` 场景适配器并接入统一 `AnalysisTaskService`
- [ ] 同步 Controller 仅提供 industries/indicators/precheck/compare
- [ ] Java MySQL 模板 CRUD、用户隔离、默认互斥、版本快照
- [ ] 不存在第二套 tasks/status/result/history API
- [ ] 全新建文件，不混改现有 Controller / FeignClient
- [ ] 本地 Maven + JDK17 编译通过
- [ ] 与 ENT-JAVA-ANALYSIS-CORE 联调统一任务全链路
- [ ] handoff 文档 + 架构合规自检 + cost 四字段

---

## 8. cost 预估

- estimated_tokens: 120_000
- effort_points: 5
- difficulty: M
- 预计耗时：1 天
