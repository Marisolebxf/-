# 派单包：ENT-JAVA-EVAL — Java 企业评估场景适配（v3.2）

- **任务 ID**：ENT-JAVA-EVAL
- **派发角色**：architect-agent（[human:徐滕强] 监管）
- **承接角色**：api-agent
- **仓**：`lumen-svc-platform`
- **模块**：`gkxlumen-topic-enterprise`
- **依赖**：`ENT-ARCH-ANALYSIS-TASK-DOC`、`ENT-JAVA-ANALYSIS-CORE`、`ENT-PY-EVAL-TASK`
- **派发时间**：2026-07-21
- **v3.1 修订**：2026-07-25 监管人 human:徐滕强 确认（对齐 ARCH-ANALYSIS-TASK v3.2 + EVAL 契约 v4）

---

> **2026-07-24 范围变更**：本任务不再建设 `/topic/v1/evaluation/tasks*` 第二套任务中心。
> 正式任务创建、状态、结果和历史统一走 Java `/topic/v1/analysis/tasks*`（服务内），网关 `/topicAsync/topic/v1/analysis/tasks*`，并落
> `analysis_task`。本任务只实现企业评估的**同步辅助接口**（industries/indicators/precheck/compare）和**Java 模板管理**。
>
> **2026-07-25 v3.1 补充**：`enterprise_eval` 的场景适配器（`EnterpriseEvalAnalysisAdapter` 的 create/status/result 透传 + 参数校验 + FeignClient）
> 已归入 `ENT-JAVA-ANALYSIS-CORE` 统一实现。本任务不再实现 adapter 本身，只负责同步辅助接口和模板管理。
> FeignClient `RemoteEnterpriseAiPythonClient` 由 CORE 建设，本任务复用。

---

## 1. 背景

数据侧 `gkx_ai_service` 提供企业评估 8 个适配接口。Java 侧由
`ENT-JAVA-ANALYSIS-CORE` 建统一编排中心；本任务为该中心提供企业评估场景适配器，
并保留行业、指标、预检、双企对比等同步接口。系统模板和个人模板在 Java MySQL 管理。

### 调用链

```
前端 → Java /topic/v1/analysis/tasks*（任务生命周期唯一入口）
         → enterprise_eval 场景适配器
              → Python /internal/gkx-ai/evaluation/tasks*

前端 → Java /topic/v1/evaluation/{industries|indicators|precheck|compare|templates*}
         → Python 同步适配（模板除外）或 Java MySQL（模板）
```

### 关键约束

1. **复用 CORE 建设的 FeignClient**：`RemoteEnterpriseAiPythonClient`（由 `ENT-JAVA-ANALYSIS-CORE` 建设），**不复用** `RemoteEnterprisePythonClient`（后者指向 gkx-search-service:8080，评估服务在 gkx-ai-service:8081）
2. **算法切换 Java 零改动**：gkx_ai_service 当前 Mock 模式，算法侧 `ENT-ALGO-EVAL-INTERACTIVE` 就绪后切 `GKX_MOCK_ENABLED=false`，返回结构不变，Java 无感知
3. **Convoy Risk 隔离**：全新建文件，不混改 `EnterpriseOpenApiController`
4. **taskId 由 Java 唯一生成并向下传递**：Python `/tasks` 必须接受并复用 Java 传入的 `task_id`，不自生成；status/result/compare 均用同一 taskId
5. **pending 不回传 Java**：Python status 返回 `running`/`success`/`failed`；算法内部 pending 对 Java 透明
6. **评估结果以 v3.2 §9 三套 subType 结构为最终契约**：`technology`/`business`/`competitiveness` 各自独立 result schema；Java 用 `JsonNode` 原样透传，不组装

---

## 2. 接口契约（data-agent 已整理）

**完整契约文档**：`agent-handoffs/企业战略分析-ENT/API-ENT-EVAL-contract.md`（v4）

### 2.1 下游端点（gkx-ai-service）

| # | 方法 | 路径 | 作用 |
|---|---|---|---|
| 1 | POST | `/industries` | 行业列表 |
| 2 | POST | `/indicators` | 指标树和默认权重 |
| 3 | POST | `/precheck` | 数据预检 |
| 4 | POST | `/tasks` | 创建算法任务（**接受 Java 传入的 task_id**） |
| 5 | POST | `/tasks/{task_id}/status` | 算法任务状态（返回 running/success/failed，不返回 pending） |
| 6 | POST | `/tasks/{task_id}/result` | 多态评估结果（三套 subType 结构） |
| 7 | POST | `/tasks/{task_id}/compare` | 双企对比 |
| 8 | POST | `/tasks/history` | 仅 svc 自测/状态兜底 |

### 2.2 Java 对外边界

| 对外路径 | 责任 |
|---|---|
| `/topic/v1/analysis/tasks*` | ENT-JAVA-ANALYSIS-CORE；任务唯一入口 |
| `/topic/v1/evaluation/industries` | Feign 透传 Python |
| `/topic/v1/evaluation/indicators` | Feign 透传 Python |
| `/topic/v1/evaluation/precheck` | Feign 透传 Python |
| `/topic/v1/evaluation/tasks/{taskId}/compare` | Feign 透传 Python |
| `/topic/v1/evaluation/templates*` | Java 系统/个人模板 CRUD（**按原型图处理，本派单包不展开表设计**） |

> 禁止新增模块私有的 tasks/status/result/history；正式历史只查 Java MySQL。

### 2.3 核心数据结构

**评估维度**（固定 4 个，评分计算用）：

| 键 | 含义 |
|---|---|
| innovation | 创新能力 |
| operation | 经营能力 |
| growth | 成长性 |
| risk | 风险水平 |

**任务状态流转**：Java 侧只有 `running/success/failed/cancelled`，无 `pending`（pending 只在算法侧，对 Java 透明）。

**评分结果结构**：以 `ARCH-ANALYSIS-TASK-设计方案.md` v3.2 §9 三套 subType 结构为最终契约。下方旧四维统一结构**已废弃**，仅作历史参考。

<details>
<summary>旧四维结构（已废弃，待 Python 按 v3.2 §9 重写后删除）</summary>

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

</details>

---

## 3. 任务范围

### 3.1 必做（DoD）

1. **复用 FeignClient**：`RemoteEnterpriseAiPythonClient`（由 `ENT-JAVA-ANALYSIS-CORE` 建设），本任务只追加同步辅助方法（industries/indicators/precheck/compare 对应的 Feign 方法）
2. **同步 Controller**：仅暴露 `/topic/v1/evaluation/{industries|indicators|precheck|compare}`
3. **模板管理**：Java MySQL 系统模板 + 个人模板 CRUD，含用户隔离、默认互斥和版本快照
4. **全新建文件**：不混改 `EnterpriseOpenApiController` / `RemoteEnterprisePythonClient`（Convoy 隔离）
5. **本地 Maven + JDK17 编译通过**
6. **handoff 文档** + 架构合规自检 + cost 四字段

### 3.1.1 模板表 DDL 骨架（Java agent 直接可用）

```sql
-- 评估模板表（系统模板 + 个人模板共用）
CREATE TABLE evaluation_template (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    template_id     VARCHAR(64) NOT NULL UNIQUE COMMENT '模板ID(TPL-xxx)',
    template_name   VARCHAR(128) NOT NULL COMMENT '模板名称',
    template_type   VARCHAR(16) NOT NULL COMMENT 'system|personal',
    sub_type        VARCHAR(32) NOT NULL COMMENT 'technology|business|competitiveness',
    user_id         VARCHAR(64) NULL COMMENT '个人模板归属用户ID;系统模板为NULL',
    industry        VARCHAR(64) NULL COMMENT '适用行业(business模式用)',
    indicators_json JSON NOT NULL COMMENT '指标选择快照[{key,weight}]',
    weights_json    JSON NOT NULL COMMENT '权重快照{innovation:25,operation:25,...}',
    is_default      TINYINT DEFAULT 0 COMMENT '是否当前用户该sub_type默认模板(1=是)',
    version         INT DEFAULT 1 COMMENT '版本号',
    status          VARCHAR(16) DEFAULT 'active' COMMENT 'active|archived',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_sub_type (user_id, sub_type, status),
    INDEX idx_system_sub_type (template_type, sub_type, status)
) COMMENT '评估模板(系统+个人)';
```

**约束**：
- `template_type=system` 时 `user_id` 为 NULL，仅 OPS/SYS（L4）可维护
- `template_type=personal` 时 `user_id` 必填，用户只能查/改自己的个人模板
- 同一用户同一 subType 最多 1 个 `is_default=1`（默认互斥）；设置新默认时旧默认置 0
- 任务创建时 `analysis_task.params` 固化 `template_id` + `version` + 完整 indicators/weights 快照，模板后续修改不影响已生成任务

### 3.1.2 模板 REST API

| 路径 | 方法 | 功能 |
|---|---|---|
| `/topic/v1/evaluation/templates` | GET | 系统模板列表 + 当前用户个人模板列表（按 subType 过滤） |
| `/topic/v1/evaluation/templates` | POST | 新建个人模板 |
| `/topic/v1/evaluation/templates/{templateId}` | PUT | 更新个人模板（仅本人） |
| `/topic/v1/evaluation/templates/{templateId}` | DELETE | 归档个人模板（仅本人，软删除） |
| `/topic/v1/evaluation/templates/{templateId}/default` | PUT | 设为默认（同 subType 互斥） |

### 3.2 不做（禁止项）

1. ❌ 不改 `EnterpriseOpenApiController` — 评估端点独立 Controller
2. ❌ 不改 `RemoteEnterprisePythonClient` — 使用 CORE 建设的 `RemoteEnterpriseAiPythonClient`
3. ❌ 不写评估算法 — Java 只做透传/门面，算法在 Python 侧
4. ❌ 不直连 entan — 只调 gkx-ai-service 屏蔽层
5. ❌ 不另建评估任务表 — 复用统一 `analysis_task`
6. ❌ 不把模板转发给 Python — 模板属于 Java 业务配置
7. ❌ 不暴露第二套 tasks/status/result/history API
8. ❌ 不在 Java MySQL 保存 `pending` 状态
9. ❌ **不实现 `EnterpriseEvalAnalysisAdapter`** — 已归 `ENT-JAVA-ANALYSIS-CORE`

---

## 4. 场景适配骨架

> **以下场景适配骨架已归 `ENT-JAVA-ANALYSIS-CORE` 实现**，本任务不实现，仅作参考。

```java
// 归属：ENT-JAVA-ANALYSIS-CORE
@Component
public class EnterpriseEvalAnalysisAdapter implements AnalysisTypeAdapter {
    public String analysisType() {
        return "enterprise_eval";
    }

    public DownstreamTaskRef create(AnalysisTask task, JsonNode params) {
        // Java taskId 向下传递；调用 /internal/gkx-ai/evaluation/tasks
        // Python 必须复用 task.getTaskId()，不自生成
        // 校验 subType ∈ {technology, business, competitiveness} + enterpriseCodes 最少数量
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
4. 期望 result 按三套 subType 结构返回（v3.2 §9），`data_source=mock`

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

- [ ] 复用 CORE 建设的 `RemoteEnterpriseAiPythonClient`，追加同步辅助方法（industries/indicators/precheck/compare）
- [ ] 同步 Controller 仅提供 industries/indicators/precheck/compare
- [ ] compare 使用 Java taskId；校验任务属于当前用户且 `status=success`；compare 只能选择父评估任务结果中的企业；compare 不创建新 `analysis_task`
- [ ] Java MySQL 模板 CRUD、用户隔离、默认互斥、版本快照（按原型图）
- [ ] 不存在第二套 tasks/status/result/history API
- [ ] Java MySQL 永不保存 `pending`
- [ ] D9 血缘与预览字段强制透传（`metric_id`/`data_status`/`is_preview`/`preview_note`/`data_source`/`model_version`），Java 不将 `GAP-*` 或 `pending` 擅自转成 available；DoD 含字段透传测试
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
