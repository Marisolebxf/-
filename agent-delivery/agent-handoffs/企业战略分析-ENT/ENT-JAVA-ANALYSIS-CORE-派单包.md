# 派单包：ENT-JAVA-ANALYSIS-CORE

## 1. 任务信息

- 执行角色：`api-agent`
- 仓库：`lumen-svc-platform`（`dev`）
- 依赖：`ENT-ARCH-ANALYSIS-TASK-DOC`
- 状态：`backlog`，依赖完成后由 coordinator 转 `ready` 并认领
- 架构真源：`ARCH-ANALYSIS-TASK-设计方案.md` v3.0

## 2. 目标与边界

在 Java `gkxlumen-topic` 建立分析任务唯一编排中心，统一承接
`enterprise_eval`、`risk_insight`、`talent_recommend`。前端只调用 Java；
Java 只编排、存状态和透传结果，不实现评分、图谱或推荐算法。

本任务不生成 PDF/Excel，不修改产品定义文档；文件任务由
`ENT-JAVA-ANALYSIS-ARTIFACT` 承接。

## 3. 实现范围

1. MySQL `analysis_task`、`analysis_task_node` DDL、实体、Mapper 和索引。
2. `/api/analysis/tasks` 创建、模块内分页、详情、结果、取消及 running 小窗。
3. SSE 进度推送和 API 查询兜底。
4. `AnalysisTypeAdapter` 扩展点；按 `analysisType` 显式路由三类 Python 服务。
5. `/api/analysis/callback/eval|risk|recommend`，强制校验 `analysisType`。
6. Redis 用户总量、用户类型、全局并发控制及失败回滚。
7. 状态修正器：算法任务查 Python；Java 文件任务不得查 Python。
8. 逻辑取消、幂等、OTel、权限与审计。

## 4. 强制契约

- Java 状态仅 `running/success/failed/cancelled`，无 `pending`。
- taskId 由 Java 生成并向下传递；`analysisType` 必填。
- 正式历史和结果以 Java MySQL 为唯一真源。
- 分析幂等键：`userId + analysisType + clientRequestId`。
- 回调链：算法 → Python callback → Java callback。
- 大结果按阈值写 MinIO，MySQL 只留指针。

## 5. 验收

- 三类 adapter 可用 Mock 完成创建→回调→SSE→结果闭环。
- 并发拒绝、创建失败回滚、重复回调、逻辑取消和重启修正均有测试。
- Maven/JDK17 构建、CI、OTel 验证通过。
- handoff 按模板填写 commit、Pipeline、架构合规和 cost 四字段。

