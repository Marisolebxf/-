# 派单包：ENT-ALGO-ENTAN-ASYNC-FRAME

## 1. 任务信息

- 执行角色：`algorithm-agent`
- 仓库：`demo-algo-ent-analysis`
- 依赖：`ENT-ARCH-ANALYSIS-TASK-DOC`、`ENT-ALGO-EVAL-INTERACTIVE`
- 状态：`backlog`

## 2. 目标

把 entan 评估从进程内任务态升级为可恢复的算法侧异步任务框架。算法侧使用
MySQL 保存自身任务状态、节点与结果，但不得成为前端历史入口；Java 编排库仍是业务真源。

## 3. 实现要求

1. create-and-start 接收 Java `taskId`、`analysisType`、`callbackUrl` 和 `clientRequestId`。
2. 算法侧 MySQL 保存任务、节点、结果和重试信息；不得继续以 dict 作为生产真源。
3. 全局并发默认 3，由 `GKX_ALGO_GLOBAL_CONCURRENCY` 或等价配置控制。
4. 按 submit→validate→data_gather→compute→confidence→assemble 推进节点。
5. 节点与终态 Webhook 只发 Python `/internal/gkx-ai/analysis/callback`。
6. RUNNING 取消为逻辑取消；算法可完成计算，但不得提交已取消结果。
7. 超时恢复、有限重试、D9 血缘、OTel 和敏感配置管理齐全。

## 4. 禁止

- 禁止算法直接回调 Java。
- 禁止 PostgreSQL/PG；运行时统一 MySQL。
- 禁止把并发值 3 写死在业务代码。
- 禁止改变 `/v1/evaluation/compute` 的三模式业务语义。

## 5. 验收

- MySQL 重启恢复、并发限制、重复 taskId、逻辑取消和失败重试测试通过。
- 回调 payload 强制携带 `analysisType`，并与 Python callback 联调。
- 三模式结果和 D9 字段不回退。
- CI、handoff、架构合规和 cost 四字段齐全。

