# 派单包：ENT-ALGO-SCIENCE-ASYNC-FRAME

## 1. 任务信息

- 执行角色：`algorithm-agent`
- 仓库：`demo-algo-science`
- 依赖：`ENT-ARCH-ANALYSIS-TASK-DOC`
- 状态：`backlog`

## 2. 目标

为风险洞察与引育推荐建立统一算法侧异步任务框架，同时允许两类业务保留各自节点和结果契约。
实现细节由算法团队发挥，但外部契约必须符合架构 **v3.1**。

## 3. 实现要求

1. `/gdf/tasks` 提供 create-and-start、status、result、cancel 内部 API。
2. 请求接收 Java `taskId`、`analysisType`、`subType`、`callbackUrl`。
   - **不接收 `clientRequestId`**（v3.1 已移除；taskId 即全局幂等键）。
   - `taskId` 由 Java 唯一生成，算法侧复用，不自生成。
3. MySQL 保存算法任务状态、节点、结果和重试信息。
   - 算法侧 MySQL 可保存 `pending` 状态（待跑中），但 **pending 不得回传 Java**；回调/查询时映射为 `running`。
4. 全局并发默认 3 且配置化；支持超时恢复和有限重试。
5. Webhook 只发 Python callback，并强制携带 `analysisType`。
6. 风险支持 `supply_chain/pain_points`；推荐支持 `attraction/cultivation`。
7. 供应链图谱一次计算最多 3 级并形成完整快照，不按展开动作二次计算。
8. 逻辑取消、D9、OTel、配置密钥管理齐全。

## 4. 禁止

- 禁止算法直连 Java 或前端。
- 禁止 PostgreSQL/PG；使用 MySQL。
- 禁止写死并发值。
- 禁止用 Neo4j，图谱仍使用 NebulaGraph。

## 5. 验收

- 两类 analysisType、各 subType 的任务状态和结果契约测试通过。
- 并发、重启恢复、逻辑取消、重复 taskId、回调失败重试测试通过。
- 3 级供应链快照有规模和 MinIO 外置测试。
- CI、handoff、架构合规和 cost 四字段齐全。

