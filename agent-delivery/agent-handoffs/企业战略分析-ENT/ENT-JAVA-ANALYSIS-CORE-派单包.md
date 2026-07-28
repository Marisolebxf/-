# 派单包：ENT-JAVA-ANALYSIS-CORE

## 1. 任务信息

- 执行角色：`api-agent`
- 仓库：`lumen-svc-platform`（`dev`）
- 依赖：`ENT-ARCH-ANALYSIS-TASK-DOC`
- 状态：`backlog`，依赖完成后由 coordinator 转 `ready` 并认领
- 架构真源：`ARCH-ANALYSIS-TASK-设计方案.md` **v3.2**（2026-07-27 监管人 human:徐滕强 确认升版）

## 2. 目标与边界

在 `lumen-svc-platform/gkxlumen-topic-async-service` 建立分析任务唯一编排中心，统一承接
`enterprise_eval`、`risk_insight`、`talent_recommend`。前端只调用 Java；
Java 只编排、存状态和透传结果，不实现评分、图谱或推荐算法。

**本任务实现三个模块的完整场景适配器**（`EnterpriseEvalAnalysisAdapterImpl`、`RiskInsightAnalysisAdapterImpl`、`TalentRecommendAnalysisAdapterImpl`），
包括 FeignClient 建设和参数校验。`ENT-JAVA-EVAL` 只负责企业评估的同步辅助接口（industries/indicators/precheck/compare）和模板管理。

本任务不生成 PDF/Excel，不修改产品定义文档；文件任务由
`ENT-JAVA-ANALYSIS-ARTIFACT` 承接。

## 3. 实现范围

1. MySQL `analysis_task`、`analysis_task_node` DDL、实体、Mapper 和索引。
   - `user_id` 用 `VARCHAR(64)`（从 Java 登录态获取，前端传值忽略）。
   - **不加 `client_request_id`**；taskId 即全局幂等键。
   - 补 MinIO 结果指针字段：`result_asset_id` / `result_url` / `result_size` / `result_bucket`。
2. 服务内路径 `/topic/v1/analysis/tasks` 创建、模块内分页、详情、结果、取消及 running 小窗；网关 `/topicAsync/topic/v1/analysis/**`。
3. SSE 进度推送和 API 查询兜底。
4. `AnalysisTypeAdapter` 扩展点；采用显式 `Map<analysisType, AnalysisTypeAdapter>` 路由（**不使用策略模式，不做自动扫描**）；Adapter 做 `create`/`status`/`result` 透传 + 参数校验。
5. **三个场景适配器实现**（本任务范围内）：
   - `EnterpriseEvalAnalysisAdapterImpl`：`analysisType=enterprise_eval`，调 Python `/internal/gkx-ai/evaluation/tasks`；校验 `subType` ∈ {`technology`,`business`,`competitiveness`} + `enterpriseCodes` 最少数量。
   - `RiskInsightAnalysisAdapterImpl`：`analysisType=risk_insight`，调 Python `/internal/gkx-ai/risk/tasks`；校验 `subType` ∈ {`supply_chain`,`pain_points`} + 对应参数（supply_chain 校验 `relationScope`；pain_points 校验 `diagnosisScope`）。
   - `TalentRecommendAnalysisAdapterImpl`：`analysisType=talent_recommend`，调 Python `/internal/gkx-ai/recommend/tasks`；校验 `subType` ∈ {`attraction`,`cultivation`} + `selectionMode` ∈ {`filter`,`candidate_workbench`}；filter 模式校验 `filters`，candidate_workbench 校验 `enterpriseCodes[]` 非空；三项权重合计=100。
6. **FeignClient**：新建 `RemoteTopicAsyncAiPythonClient`，覆盖 eval/risk/recommend 三组下游端点（eval 8 端点、risk 4 端点、recommend 4 端点）；`TopicAsyncAiPythonFeignConfig` 下游寻址 `gkxlumen.topic.async.python-ai-base-url`（非空直连，为空走 Nacos `gkx-ai-service`）。
7. `/topic/v1/analysis/callback/eval|risk|recommend`，强制校验 `analysisType`。
8. Redis 用户总量、用户类型、全局并发控制及失败回滚。
9. 状态修正器：算法任务查 Python；Java 文件任务不得查 Python。
10. 逻辑取消、幂等、OTel、权限与审计。
11. XXL-Job 复用 `gkxlumen-xxl-job-admin` + `gkxlumen-common-job` + `@XxlJob("analysisStatusReconcileJob")`，不新增 `@Scheduled`。

## 4. 强制契约

- Java 状态仅 `running/success/failed/cancelled`，无 `pending`（pending 只在算法侧，Adapter 收到映射为 running）。
- taskId **由 Java 唯一生成**，全局流转；Python `/tasks` 必须接受并复用 Java 传入的 `task_id`，不自生成；status/result/compare 均用同一 taskId。
- `analysisType` 必填。
- 正式历史和结果以 Java MySQL 为唯一真源。
- 分析幂等键：taskId 全局唯一即幂等键（**不引入 `client_request_id`**）；报告/导出幂等键 `userId + analysisType + parentTaskId + format`，同任务多次下载复用已有产物。
- 回调链：算法 → Python callback → Java callback。
- **JSON 字段命名（D-30 v3.2）**：Java 对前端/SSE 输出用 `camelCase`；常规字段（`task_id`/`analysis_type`/`event`/`node_code` 等）Java 用 `@JsonProperty` 对接 Python 的 snake_case。**分析结果例外**：由 Worker 转 camelCase 后写 MinIO，Java 只存 resultUrl 指针，不存 result JSON、不解析。
- **回调事件（D-31）**：Java 收到 5 种 event — `step_started`/`step_completed`/`task_completed`/`task_failed`/`task_cancelled`；`task_cancelled` 标记 cancelled（不显示 error），`task_failed` 标记 failed（显示 error）。
- **分析结果 MinIO（v3.4，全量外置，D-33）**：分析结果统一由 **Python Worker 进程**写 MinIO，Java 只收 `resultUrl` 指针，存 `result_asset_id`/`result_url`/`result_size`/`result_bucket`。**Java 不存 result JSON、不碰分析结果 MinIO**。报告/导出文件 MinIO 仍归 ARTIFACT。**Java 无需感知 MQ**（Java 仍接收 Python 转发的 HTTP callback，只是 task_completed 的 result_url 由 Worker 异步写入，可能有秒级延迟）。

## 5. 验收

- **三个场景适配器**（eval/risk/recommend）均可用 Mock 完成创建→回调→SSE→结果闭环。
  - eval：校验 subType ∈ {technology,business,competitiveness} + enterpriseCodes 最少数量（technology/business≥2，competitiveness≥1）。
  - risk：校验 subType ∈ {supply_chain,pain_points}；supply_chain 校验 relationScope 非空；pain_points 校验 diagnosisScope 非空。
  - recommend：校验 subType ∈ {attraction,cultivation} + selectionMode ∈ {filter,candidate_workbench}；filter 校验 filters 非空；candidate_workbench 校验 enterpriseCodes 非空；三项权重合计=100。
- FeignClient `RemoteTopicAsyncAiPythonClient` 覆盖 eval 8 + risk 4 + recommend 4 端点。
- 并发拒绝、创建失败回滚、重复回调、逻辑取消和重启修正均有测试。
- Maven/JDK17 构建、CI、OTel 验证通过。
- handoff 按模板填写 commit、Pipeline、架构合规和 cost 四字段。

## 6. 关键实现细节（Java agent 直接可用）

### 6.1 FeignClient 端点清单

```java
@FeignClient(name = "gkx-ai-service", url = "${gkxlumen.topic.async.python-ai-base-url:}", fallbackFactory = ...)
public interface RemoteTopicAsyncAiPythonClient {

    // ===== eval（8 端点，ENT-JAVA-EVAL 复用同步部分）=====
    @PostMapping("/internal/gkx-ai/evaluation/industries")
    R<Map> evalIndustries(@RequestBody EvalIndustriesRequest req);

    @PostMapping("/internal/gkx-ai/evaluation/indicators")
    R<Map> evalIndicators(@RequestBody EvalIndicatorsRequest req);

    @PostMapping("/internal/gkx-ai/evaluation/precheck")
    R<Map> evalPrecheck(@RequestBody EvalPrecheckRequest req);

    @PostMapping("/internal/gkx-ai/evaluation/tasks")
    R<Map> evalCreateTask(@RequestBody EvalCreateTaskRequest req);

    @PostMapping("/internal/gkx-ai/evaluation/tasks/{taskId}/status")
    R<Map> evalStatus(@PathVariable String taskId);

    @PostMapping("/internal/gkx-ai/evaluation/tasks/{taskId}/result")
    R<Map> evalResult(@PathVariable String taskId);

    @PostMapping("/internal/gkx-ai/evaluation/tasks/{taskId}/compare")
    R<Map> evalCompare(@PathVariable String taskId, @RequestBody EvalCompareRequest req);

    @PostMapping("/internal/gkx-ai/evaluation/tasks/history")
    R<Map> evalHistory(@RequestBody EvalHistoryRequest req);

    // ===== risk（4 端点）=====
    @PostMapping("/internal/gkx-ai/risk/tasks")
    R<Map> riskCreateTask(@RequestBody RiskCreateTaskRequest req);

    @PostMapping("/internal/gkx-ai/risk/tasks/{taskId}/status")
    R<Map> riskStatus(@PathVariable String taskId);

    @PostMapping("/internal/gkx-ai/risk/tasks/{taskId}/result")
    R<Map> riskResult(@PathVariable String taskId);

    @PostMapping("/internal/gkx-ai/risk/tasks/{taskId}/cancel")
    R<Map> riskCancel(@PathVariable String taskId);

    // ===== recommend（4 端点）=====
    @PostMapping("/internal/gkx-ai/recommend/tasks")
    R<Map> recommendCreateTask(@RequestBody RecommendCreateTaskRequest req);

    @PostMapping("/internal/gkx-ai/recommend/tasks/{taskId}/status")
    R<Map> recommendStatus(@PathVariable String taskId);

    @PostMapping("/internal/gkx-ai/recommend/tasks/{taskId}/result")
    R<Map> recommendResult(@PathVariable String taskId);

    @PostMapping("/internal/gkx-ai/recommend/tasks/{taskId}/cancel")
    R<Map> recommendCancel(@PathVariable String taskId);
}
```

### 6.2 AnalysisAssetService（分析结果指针存储 + ARTIFACT 文件上传）

```java
@Service
public class AnalysisAssetService {

    // 注：分析结果统一由 Worker 写 MinIO 后传 resultUrl（v3.4 D-33，全量外置，无阈值判断）
    // Java 只存 result_url 等指针字段，不存 result JSON

    /**
     * 分析结果指针落库（CORE 调用）。
     * Worker 已将 result 写入 MinIO 并传 resultUrl；Java 只存指针：
     * result_asset_id / result_url / result_size / result_bucket
     */
    public void saveResultPointer(String taskId, String analysisType, String resultUrl, Long resultSize, String resultBucket) { ... }

    /**
     * PDF/Excel/CSV 文件上传（ARTIFACT 调用）。
     * object key: analysis/{analysisType}/{parentTaskId}/{taskId}/report.pdf 或 export.xlsx
     */
    public String uploadFile(String taskId, String analysisType, String parentTaskId, byte[] bytes, String ext) { ... }

    /**
     * 生成临时下载 URL（经资产中心鉴权，禁止暴露永久 MinIO URL）。
     */
    public String generateDownloadUrl(String assetId, Duration expiry) { ... }
}
```

> 复用 `gkxlumen-common-oss` / `OssTemplate` / `SysFile` 等已有能力，封装统一 `AnalysisAssetService`。具体实现方案由 Java agent 按框架现状设计，在 handoff 中记录。

### 6.3 状态修正器（XXL-Job）

```java
@Component
public class AnalysisStatusReconcileJob {

    @XxlJob("analysisStatusReconcileJob")
    public void reconcile() {
        // 1. 查 status='running' 的任务（批量，每次最多 100 条）
        // 2. 分支：
        //    A. analysisType ∈ {*_report, *_export}：不调 Python；查 Java 本地执行状态/超时
        //       - 完成 → success + 释放配额 + SSE
        //       - 失败/超时 → failed + 释放配额 + SSE
        //    B. 其余分析类型：调 Python status 确认
        // 3. Python 返回 success → 更新 MySQL + 若无 result_data 调 Python result 取回（Python 负责从 MinIO 拉 camelCase result 返回）+ 释放配额 + SSE
        // 4. Python 返回 failed → 更新 failed + 释放配额 + SSE
        // 5. 仍 running / Python 不可达 → 等下一轮
    }
}
```

### 6.4 并发控制 Redis Key

```
# 用户级总并发（Set）
analysis:running:user:{userId}              → Set<taskId>

# 用户级类型并发（Set）
analysis:running:user:{userId}:type:{analysisType}  → Set<taskId>

# 全局并发（计数器）
analysis:running:global                     → Integer

# 分布式锁
analysis:lock:user:{userId}                 → SETNX + Lua
```

### 6.5 SSE 消息格式

```json
{
  "type": "analysis_progress",
  "taskId": "EVAL-20260725-001",
  "analysisType": "enterprise_eval",
  "status": "running",
  "currentNode": { "index": 4, "total": 6, "code": "compute", "name": "指标计算", "status": "started" },
  "elapsedSeconds": 42,
  "timestamp": "2026-07-25T16:30:00Z"
}
```

终态消息带 `resultUrl`，复用 `gkx-common-sse` 模块，Redis Pub/Sub 跨实例广播。

### 6.6 回调接口

> **回调请求体格式**：与 `ENT-PY-ANALYSIS-CALLBACK-派单包.md` §2.2 定义一致，Python 透明透传（**snake_case**，Java 用 `@JsonProperty` 转驼峰）：
> `{ task_id, analysis_type, event, node_code, node_name, node_index, status, progress, result, error, timestamp }`
> `event` ∈ { `step_started`, `step_completed`, `task_completed`, `task_failed`, `task_cancelled` }
> status 已经过 Python 做 pending→running 映射，Java 侧只会收到 running/success/failed/cancelled。
> ⚠️ `task_cancelled` 与 `task_failed` 语义不同（D-31）：取消是主动行为不带 error，失败是异常需带 error。

```java
@RestController
@RequestMapping("/topic/v1/analysis/callback")
public class AnalysisCallbackController {

    @PostMapping("/eval")
    public R<Void> onEvalCallback(@RequestBody AnalysisCallbackRequest req) {
        // 强制校验 req.analysisType == "enterprise_eval"
        // 更新 MySQL + 推 SSE + 释放配额（终态时）
        // task_cancelled → 标记 cancelled（不显示错误）；task_failed → 标记 failed（显示 error）
    }

    @PostMapping("/risk")
    public R<Void> onRiskCallback(@RequestBody AnalysisCallbackRequest req) { ... }

    @PostMapping("/recommend")
    public R<Void> onRecommendCallback(@RequestBody AnalysisCallbackRequest req) { ... }
}
```
