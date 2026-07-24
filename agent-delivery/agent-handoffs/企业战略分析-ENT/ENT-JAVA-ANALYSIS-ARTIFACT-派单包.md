# 派单包：ENT-JAVA-ANALYSIS-ARTIFACT

## 1. 任务信息

- 执行角色：`api-agent`
- 仓库：`lumen-svc-platform`（`dev`）
- 依赖：`ENT-JAVA-ANALYSIS-CORE`、`ENT-MOD-EXPORT-PDR-G1`
- 状态：`backlog`
- 产品定义边界：只读取既有导出 PDR，禁止修改产品定义任务或文档

## 2. 目标

实现 Java 本地异步报告与导出执行器：

- `eval_report` / `risk_report` / `recommend_report`：PDF，6 节点。
- `eval_export` / `risk_export` / `recommend_export`：Excel/CSV，5 节点。

任务复用 `analysis_task`，通过 `parent_task_id` 读取父分析结果快照，不再次调用
Python 或算法。

## 3. 实现范围

1. 文件任务创建、幂等、节点推进、取消、失败和超时处理。
2. 幂等键固定为 `userId + analysisType + parentTaskId + format`。
3. 资产中心元数据和 MinIO 上传、鉴权下载、过期与审计。
4. 大结果阈值外置：正文写 MinIO，MySQL 存 `resultAssetId/resultUrl/resultSize/resultBucket`。
5. SSE 进度通知和 Java 本地状态修正，不访问 Python。
6. 文件模板严格按已签收 PDR；本任务不自行定义业务口径。

## 4. 禁止

- 禁止用时间戳作为幂等键。
- 禁止报告/导出重新发起算法分析。
- 禁止把大图谱 JSON 或文件二进制直接塞入 MySQL。
- 禁止绕过资产中心直接向前端暴露永久 MinIO URL。

## 5. 验收

- 三模块 report/export 均能从父任务快照生成文件并完成下载鉴权。
- 重复提交返回同一业务任务；失败重试不重复生成有效资产。
- 取消、超时、无权限、父任务不存在和快照缺失场景有测试。
- Maven/JDK17、CI、OTel、handoff 和 cost 四字段齐全。

