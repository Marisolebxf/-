# 架构师验收：算法侧异步框架 + 交互式评估

- **时间**：2026-07-29
- **评审范围**：`ENT-ALGO-ENTAN-ASYNC-FRAME` / `ENT-ALGO-SCIENCE-ASYNC-FRAME` / `ENT-ALGO-EVAL-INTERACTIVE`
- **评审人**：architect-agent（监督人：human:徐滕强）
- **设计文档真源**：`ARCH-ANALYSIS-TASK-设计方案.md` v3.4

---

## 1. 七条铁律检查

| # | 检查项 | 结果 |
|---|-------|---------|
| 1 | 算法只在 Python | ✅ |
| 2 | 调用链前端→Java→Python→算法 | ✅ |
| 3 | 图谱 NebulaGraph | N/A |
| 4 | 可观测性 | ✅ 结构化日志 |
| 5 | CI/CD | ✅ main 直推 |
| 6 | demo2 不污染 lumen | ✅ |
| 7 | 方案 A 共享聚合核心 | ✅ 经 Python svc 屏蔽 |

---

## 2. 逐项验收

### 2.1 ENT-ALGO-ENTAN-ASYNC-FRAME — ✅ 通过

| 检查项 | 设计文档 | 算法实现 | 结果 |
|--------|---------|---------|------|
| 双进程拆分 | §2.1 API 进程只写 MySQL 立即返回，Worker 轮询 pending | `api/main.py` + `worker/main.py` 独立进程，MySQL `SELECT...FOR UPDATE` 抢占 | ✅ |
| 并发控制 N=3（C-15） | 不写死代码，读环境变量 | `BoundedSemaphore` + `GKX_ALGO_GLOBAL_CONCURRENCY` 默认 3 | ✅ |
| 定时超时检测（A-3） | §6.4 每分钟跑 detect_timeout_tasks | Worker 内 `_timeout_loop` 每分钟一次 | ✅ |
| 5 种 Webhook 事件（D-31） | step_started/step_completed/task_completed/task_failed/task_cancelled | `_fire_webhook` 5 事件全实现，Python `_VALID_EVENTS` 完全匹配 | ✅ |
| 晚一步取消（D-31） | §4.6.2 节点跑完→检查 cancel_flag→不进入下一节点 | 节点完成后检查内存 DB 状态缓存，取消则终止发 task_cancelled | ✅ 语义等价 |
| D-30 snake_case | 算法↔Python 全 snake_case | `task_id`/`analysis_type`/`sub_type`/`enterprise_codes`/`callback_url` | ✅ |
| D-32 sub_type | 废弃 mode，统一 sub_type | `create-and-start` 入参用 `sub_type` | ✅ |
| MySQL 持久化（C-16） | 算法侧 MySQL 独立 schema | `gkxlumenx_cfg.analysis_task` 独立表 | ✅ |

### 2.2 ENT-ALGO-SCIENCE-ASYNC-FRAME — ✅ 通过

复刻 entan 框架到 `demo-algo-science`，实现一致性验证：

| 检查项 | 结果 |
|--------|------|
| 双进程拆分 | ✅ `api/main.py` + `worker/main.py` |
| 并发控制 N=3 | ✅ `BoundedSemaphore` + 环境变量 |
| 定时超时检测 | ✅ `_timeout_loop` |
| 5 种 Webhook 事件 | ✅ 与 entan 完全一致 |
| 晚一步取消 | ✅ |
| D-30 snake_case | ✅ |
| D-32 sub_type | ✅ `supply_chain`/`pain_points`/`attraction`/`cultivation` |

### 2.3 ENT-ALGO-EVAL-INTERACTIVE — ⚠️ 有条件通过

| 检查项 | 派单包 DoD | 算法实现 | 结果 |
|--------|-----------|---------|------|
| 新增 POST `/v1/evaluation/compute` | ✅ 必做 | `api/entan_evaluation_routes.py` 已实现 | ✅ |
| 入参 enterprise_codes[] | ✅ | `body.get("enterprise_codes", [])` | ✅ |
| 入参 weights{} | ✅ | `body.get("weights")` | ✅ |
| 入参 **sub_type** | ✅ DoD 第 2 项明确要求 | **用 `mode` 而非 `sub_type`** | ❌ D-32 违规 |
| 入参 template_id | ✅ 可选 | `body.get("template_id")` | ✅ |
| 出参 scores[] | ✅ | 返回 enterprise_code/total_score/rank/dimensions/confidence | ✅ |
| 权重从请求体读 | ✅ | 从 body 读，不写死 | ✅ |
| 三模式支持 | ✅ | technology/business/competitiveness | ✅ |
| calc_process D9 血缘 | ✅ | 含 metric_id/formula/source_tables | ✅ |
| 响应包络 {code,msg,data} | ✅ | `_ok` / `_err` | ✅ |

**阻断项**：`/v1/evaluation/compute` 入参用 `mode` 而非 `sub_type`（D-32 违规）。
**影响**：此接口目前 Python 侧未调用（异步任务走 `/gdf/tasks/create-and-start`），不影响当前联调。但违反 D-32 命名约束，后续对接时会产生混淆。
**要求**：算法侧将 `mode` 改为 `sub_type` 后方可标记 `done`。

---

## 3. 交互对齐检查（算法 ↔ Python）

### 3.1 create-and-start 入参对齐

| 字段 | Python 发出 | 算法 entan 接收 | 算法 science 接收 | 结果 |
|------|------------|----------------|------------------|------|
| task_id | ✅ 顶层 | ✅ `body.get("task_id")` | ✅ | ✅ |
| analysis_type | ✅ 顶层 | ✅ `body.get("analysis_type")` | ✅ | ✅ |
| sub_type | ✅ 顶层 | ✅ `body.get("sub_type")` | ✅ | ✅ |
| enterprise_codes (eval) | ✅ 顶层 | ✅ `body.get("enterprise_codes")` | N/A | ✅ |
| enterprise_codes (risk/rec) | ✅ 顶层（已修复） | N/A | ✅ `body.get("enterprise_codes")` | ✅ |
| callback_url | ✅ 顶层 | ✅ 存 DB | ✅ 存 DB | ✅ |
| weights (eval) | ✅ 顶层 | ✅ `body.get("weights")` | N/A | ✅ |

> **P0-1 修复**：Python `science_client.create_risk_task` / `create_recommend_task` 原把 `enterprise_codes` 嵌套在 `params` 里，算法 science 侧从 body 顶层读会拿到空列表。已修复为顶层传递。

### 3.2 Webhook 回调 payload 对齐

| 字段 | 算法发出 | Python 接收 | 结果 |
|------|---------|------------|------|
| event | ✅ | ✅ `body.get("event")` | ✅ |
| task_id | ✅ | ✅ | ✅ |
| analysis_type | ✅ | ✅ | ✅ |
| sub_type | ✅ | ✅（未校验但转发） | ✅ |
| status | ✅ | ✅ `body.get("status")` | ✅ |
| node_code | ✅ | ✅ | ✅ |
| node_name | ✅ | ✅ | ✅ |
| progress | ✅ | ✅ | ✅ |
| result | ✅ (task_completed) | ✅ 投递 MQ | ✅ |
| error | ✅ (task_failed) | ✅ | ✅ |
| timestamp | ✅ | ✅（转发） | ✅ |
| **node_index** | ❌ 未发 | `body.get("node_index")` = None | ⚠️ |
| **total_nodes** | ❌ 未发 | `body.get("total_nodes")` = None | ⚠️ |

> **P2-1 非阻断**：算法侧 webhook 缺 `node_index` / `total_nodes`。Java 派单包 §214 要求传这两个字段。当前 Python 转发 null 不 crash，但 Java 侧无法渲染"第 N/M 节点"进度条。建议算法侧补发。

### 3.3 cancel 端点对齐

| 层 | 端点 | 结果 |
|----|------|------|
| Python → 算法 | `POST /gdf/tasks/{task_id}/cancel` body: `{task_id, reason}` | ✅ 算法 `gdf_cancel(task_id, body)` 接收 |
| 算法取消后 | 发 `task_cancelled` webhook（不是 task_failed） | ✅ |

---

## 4. 遗留问题

| 级别 | 问题 | 责任方 | 状态 |
|------|------|--------|------|
| P1 | `/v1/evaluation/compute` 入参用 `mode` 而非 `sub_type`（D-32 违规） | algorithm-agent | 待修复 |
| P2 | webhook 缺 `node_index` / `total_nodes` 字段 | algorithm-agent | 建议补发 |
| P2 | Worker 部署形态未确认 | architect + devops | 建议：独立 Deployment |
| P0 | Python `science_client` enterprise_codes 嵌套（已修复） | data-agent | ✅ 已修复 |

---

## 5. 决议

| 任务 | 决议 | 理由 |
|------|------|------|
| `ENT-ALGO-ENTAN-ASYNC-FRAME` | ✅ **done** | 双进程拆分+并发控制+定时调度+5事件webhook+晚一步取消 全部符合设计文档 |
| `ENT-ALGO-SCIENCE-ASYNC-FRAME` | ✅ **done** | 同上，science 仓复刻 entan 框架，实现一致 |
| `ENT-ALGO-EVAL-INTERACTIVE` | ⚠️ **暂不 done** | 核心功能完成，但 `mode`→`sub_type` 需算法侧修复（P1） |

---

## 6. 签字

- architect-agent：✅ 通过（ENTAN-ASYNC-FRAME / SCIENCE-ASYNC-FRAME）
- 架构师 lead（人）：human:徐滕强 确认执行
