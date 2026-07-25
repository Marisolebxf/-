# 派单包：ENT-ALGO-ENTAN-ASYNC-FRAME

> **架构真源**：`ARCH-ANALYSIS-TASK-设计方案.md` **v3.1**（2026-07-25）

## 1. 任务信息

- 执行角色：`algorithm-agent`
- 仓库：`demo-algo-ent-analysis`
- 依赖：`ENT-ARCH-ANALYSIS-TASK-DOC`、`ENT-ALGO-EVAL-INTERACTIVE`
- 状态：`backlog`

## 2. 目标

把 entan 评估从进程内任务态升级为可恢复的算法侧异步任务框架。算法侧使用
MySQL 保存自身任务状态、节点与结果，但不得成为前端历史入口；Java 编排库仍是业务真源。

## 3. 实现要求

1. create-and-start 接收 Java `taskId`、`analysisType`、`mode`、`callbackUrl`。
   - **不接收 `clientRequestId`**（v3.1 已移除；taskId 即全局幂等键）。
   - `analysisType` = `enterprise_eval`；`mode` = `technology` | `business` | `competitiveness`。
   - `taskId` 由 Java 唯一生成，算法侧复用，不自生成。
2. 算法侧 MySQL 保存任务、节点、结果和重试信息；不得继续以 dict 作为生产真源。
   - 算法侧 MySQL 可保存 `pending` 状态（待跑中），但 **pending 不得回传 Java**；回调/查询时映射为 `running`。
3. 全局并发默认 3，由 `GKX_ALGO_GLOBAL_CONCURRENCY` 或等价配置控制。
4. 按 submit→validate→data_gather→compute→confidence→assemble 推进节点（6 节点，见架构 §3.2）。
5. 节点与终态 Webhook 只发 Python `/internal/gkx-ai/analysis/callback`；回调 payload 强制携带 `analysisType`。
6. RUNNING 取消为逻辑取消；算法可完成计算，但不得提交已取消结果。
7. 超时恢复、有限重试、D9 血缘、OTel 和敏感配置管理齐全。
8. **结果契约以 v3.1 §9 三套 mode 结构为准**（technology 五维雷达 / business 经营指标非雷达 / competitiveness 三维雷达）；
   旧四维统一结构（innovation/operation/growth/risk）仅作内部评分计算中间态，**不得作为对外结果 schema**。

## 4. 禁止

- 禁止算法直接回调 Java。
- 禁止 PostgreSQL/PG；运行时统一 MySQL。
- 禁止把并发值 3 写死在业务代码。
- 禁止改变 `/v1/evaluation/compute` 的三模式业务语义。
- ❌ 禁止接收或使用 `clientRequestId`（v3.1 已移除）。
- ❌ 禁止把 `pending` 状态回传 Java（Java 侧只有 running/success/failed/cancelled）。

## 5. 验收

- MySQL 重启恢复、并发限制、重复 taskId、逻辑取消和失败重试测试通过。
- 回调 payload 强制携带 `analysisType`，并与 Python callback 联调。
- 三模式结果按 v3.1 §9 三套 mode schema 返回；D9 字段不回退。
- 算法侧 `pending` 不出现在回调/查询响应中（映射为 `running`）。
- CI、handoff、架构合规和 cost 四字段齐全。
