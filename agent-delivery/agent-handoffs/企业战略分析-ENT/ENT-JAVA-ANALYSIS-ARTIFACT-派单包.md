# 派单包：ENT-JAVA-ANALYSIS-ARTIFACT（v3.2）

## 1. 任务信息

- 执行角色：`api-agent`
- 仓库：`lumen-svc-platform`（`dev`）
- 模块：`gkxlumen-topic-enterprise`（与 CORE 同落）
- 依赖：`ENT-JAVA-ANALYSIS-CORE`、`ENT-MOD-EXPORT-PDR-G1`
- 状态：`backlog`
- 架构真源：`ARCH-ANALYSIS-TASK-设计方案.md` **v3.2**
- 产品定义边界：只读取既有导出 PDR，禁止修改产品定义任务或文档

## 2. 目标

实现 Java 本地异步报告与导出执行器：

- `eval_report` / `risk_report` / `recommend_report`：PDF，6 节点。
- `eval_export` / `risk_export` / `recommend_export`：Excel/CSV，5 节点。

任务复用 `analysis_task`，通过 `parent_task_id` 读取父分析结果快照，不再次调用
Python 或算法。

## 3. 实现范围

1. 文件任务创建、幂等、节点推进、取消、失败和超时处理。
   - 创建入口仍归 CORE（`POST /topic/v1/analysis/tasks`，analysisType=`*_report`/`*_export`）；ARTIFACT 以本地执行器扩展接入。
   - 父任务校验、幂等和并发由 CORE 执行。
   - ARTIFACT 未就绪时，CORE 对 `*_report`/`*_export` 返回明确的"功能尚未开放"，不写入无人执行的 running 任务。
2. 幂等键固定为 `userId + analysisType + parentTaskId + format`；同任务多次下载复用已有产物，不重复生成。
   - running：直接返回原任务。
   - success：默认返回已有有效资产。
   - 显式重新生成：要求 `force=true`。
   - failed：创建新的重试任务并关联 `retry_of_task_id`。
   - 上传成功但落库失败：记录待清理对象，由补偿任务处理。
3. 资产中心元数据和 MinIO 上传、鉴权下载、过期与审计。
   - **Java agent 按框架现状设计**：复用 `gkxlumen-common-oss` / `OssTemplate` / `SysFile` 等已有能力，封装统一 `AnalysisAssetService`。
   - object key 规范：`analysis/{analysisType}/{parentTaskId}/{taskId}/report.pdf` 或 `.../export.xlsx`。
   - 下载鉴权：经资产中心统一鉴权，禁止向前端暴露永久 MinIO URL；临时下载 URL 有效期由配置项控制。
   - 过期/删除/作废/审计策略：由 Java agent 按框架现状设计，在 handoff 中记录最终方案。
4. 大结果阈值外置：**分析结果 JSON 外置归 Python svc**（v3.2 D-30 修订，Python 负责阈值判断 + MinIO 读写 + snake_case → camelCase 转换）；**PDF/Excel/CSV 上传归 ARTIFACT**；ARTIFACT 只管报告/导出文件的 MinIO 读写。MySQL 存 `result_asset_id`/`result_url`/`result_size`/`result_bucket`。
5. SSE 进度通知和 Java 本地状态修正，不访问 Python。
6. 文件模板严格按已签收 PDR；本任务不自行定义业务口径。
   - PDR 未签收前只实现执行器框架、Mock 文件和资产上传冒烟。
   - 正式 PDF/Excel/CSV 模板必须由 PDR 提供（`ENT-MOD-EXPORT-PDR-G1`）。
7. XXL-Job 状态修正沿用 CORE 的 `analysisStatusReconcileJob`（复用 `gkxlumen-xxl-job-admin` + `gkxlumen-common-job`），不新增第二个定时器；文件任务超时由该 Job 检查本地执行状态、锁、节点更新时间和超时阈值。
8. 文件生成技术方案：**由 Java agent 按框架现状选型**，在 handoff 中记录最终方案。
   - PDF：HTML 模板 + 服务端渲染，或现有报告平台能力。
   - 图表：服务端生成图片后嵌入 PDF，禁止依赖用户浏览器。
   - Excel：Apache POI 流式 SXSSF 或框架现有导出能力。
   - CSV：UTF-8 BOM，防止中文 Excel 打开乱码。
   - 中文字体：以容器镜像内置字体为准，并在 CI 验证。
9. Java 本地异步执行与重启恢复：**由 Java agent 按框架现状设计**，在 handoff 中记录最终方案。
   - 使用独立可配置线程池，禁止共用 Web 请求线程池。
   - 任务节点状态全部写 `analysis_task_node`。
   - 执行前用分布式锁 `analysis:artifact:lock:{taskId}`。
   - XXL-Job 状态修正发现本地 running 任务后：无执行器持有锁→重新投递；有执行器运行→保持 running；超过超时阈值→标 failed。
   - 文件生成按父任务快照保证可重放。

## 4. 禁止

- 禁止用时间戳作为幂等键。
- 禁止报告/导出重新发起算法分析。
- 禁止把大图谱 JSON 或文件二进制直接塞入 MySQL。
- 禁止绕过资产中心直接向前端暴露永久 MinIO URL。
- 禁止新增 `@Scheduled`；状态修正走 XXL-Job。

## 5. 验收

- 三模块 report/export 均能从父任务快照生成文件并完成下载鉴权。
- **success 原子边界**：文件生成成功 + MinIO 上传成功 + 资产中心元数据登记成功 + `analysis_task.result_data` 回写成功 + SSE 终态推送已触发；任一步失败进入失败或补偿流程，避免产生无法下载的"成功任务"。
- 重复提交返回同一业务任务；失败重试不重复生成有效资产。
- 取消、超时、无权限、父任务不存在和快照缺失场景有测试。
- Maven/JDK17、CI、OTel、handoff 和 cost 四字段齐全。
