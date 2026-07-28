# Handoff：ENT-JAVA-ANALYSIS-CORE

- **时间**：2026-07-27（2026-07-28 提 review；同日路径公约纠偏）
- **执行**：agent:api-agent（监管：human:侯佳伟；任务监管：human:徐滕强）
- **仓库 / 分支**：`lumen-svc-platform` / `dev`
- **派单包**：`ENT-JAVA-ANALYSIS-CORE-派单包.md`
- **状态**：`review`（代码已 push；运维/联调开放项见 §7，不阻断提审）
- **迁移更新（2026-07-28）**：CORE 已迁至 `gkxlumen-topic-async-service`；commit `2aca50d` 已推送 `origin/dev`
- **路径纠偏（2026-07-28，human:侯佳伟）**：对外路径按公约四段拼接为 `/topicAsync/topic/v1/analysis/**`；网关由错误的 RewritePath 改为 `StripPrefix=1`（勿再写 `/topicAsync/v1/analysis/**`）
- **命名裁定（2026-07-27）**：大类 `analysisType`/`analysis_type`，小类 `subType`/`sub_type`；废弃 `mode`；比较篮前端跳转 `?mode=` 不属于本任务，保持不动
- **D-30 Feign 对齐（2026-07-28，human:侯佳伟）**：Python v3.4 body-only 收口后，修正 `RemoteTopicAsyncAiPythonClient` 的 eval/risk/recommend `status|result|compare|cancel`，去掉 `/{taskId}` 路径参数，改为 body 传 `task_id`；三个 Adapter 同步；单测补充 body-only 断言。为 `ENT-JAVA-EVAL` 四辅助接口联调前置。

## 1. 范围与实现

统一分析任务真源，迁移后落在 `gkxlumen-topic-async-service`。

- `@EnableOpenApi("topicAsync")` → 网关前缀 `/topicAsync`
- 服务内 `@RequestMapping("/topic/v1/analysis")` 不变
- **对外完整路径**：`/topicAsync/topic/v1/analysis/**`（网关 `StripPrefix=1`）

| 方法 | 对外路径（经网关） | 服务内路径 | 说明 |
|---|---|---|---|
| POST | `/topicAsync/topic/v1/analysis/tasks` | `/topic/v1/analysis/tasks` | 创建（Java 生成 taskId，Adapter 路由） |
| POST | `/topicAsync/topic/v1/analysis/tasks/list` | `/topic/v1/analysis/tasks/list` | 模块内任务列表 |
| GET | `/topicAsync/topic/v1/analysis/tasks/{taskId}` | `/topic/v1/analysis/tasks/{taskId}` | 详情 |
| GET | `/topicAsync/topic/v1/analysis/tasks/{taskId}/result` | `/topic/v1/analysis/tasks/{taskId}/result` | 结果 |
| GET | `/topicAsync/topic/v1/analysis/tasks/{taskId}/asset` | `/topic/v1/analysis/tasks/{taskId}/asset` | 大结果 JSON 下载 |
| POST | `/topicAsync/topic/v1/analysis/tasks/{taskId}/cancel` | `/topic/v1/analysis/tasks/{taskId}/cancel` | 取消 |
| GET | `/topicAsync/topic/v1/analysis/tasks/running` | `/topic/v1/analysis/tasks/running` | running 小窗 |
| GET | `/topicAsync/topic/v1/analysis/tasks/stream` | `/topic/v1/analysis/tasks/stream` | SSE |
| POST | `/topicAsync/topic/v1/analysis/callback/eval` | `/topic/v1/analysis/callback/eval` | 评估回调（`@Inner`） |
| POST | `/topicAsync/topic/v1/analysis/callback/risk` | `/topic/v1/analysis/callback/risk` | 风险回调（`@Inner`） |
| POST | `/topicAsync/topic/v1/analysis/callback/recommend` | `/topic/v1/analysis/callback/recommend` | 推荐回调（`@Inner`） |

表：`analysis_task` / `analysis_task_node`

核心组件：

- `RemoteTopicAsyncAiPythonClient` + 独立 `python-ai-base-url` / `python-ai-service-name`
- 显式 Map 路由：`EnterpriseEvalAnalysisAdapterImpl` / `RiskInsightAnalysisAdapterImpl` / `TalentRecommendAnalysisAdapterImpl`
- Redis Lua 并发配额：用户总量 / 用户类型 / 全局
- SSE：复用 `gkxlumen-common-sse` + Redis Pub/Sub
- `AnalysisAssetService`：v3.2 分析结果只存 Python 回传指针，不写完整 `result_data`
- XXL-Job：`analysisStatusReconcileJob`（落在 topic-async-service）
- Adapter 下游 body：递归 camelCase → snake_case，并补齐 `analysis_type` / `task_id` / `created_by`
- `analysis_task.sub_type` 冗余列 + 列表 `subType` 过滤

## 2. 偏离说明（as-built）

| 项 | 派单 / 旧决议 | As-built | 理由 |
|---|---|---|---|
| `user_id` | 登录态获取、前端传值忽略 | 当前兼容前端传 `user_id`；代码预留登录态注释 | 与 SEARCH-BIZ/COMPARE 现阶段一致；后续可无感切换 |
| Feign 形态 | ARCH 曾写三个 Client | 统一 `RemoteTopicAsyncAiPythonClient` | v3.1 收口 |
| Feign 任务子路径 | 派单包曾写 `/tasks/{taskId}/status|result|compare|cancel` | **D-30**：`/tasks/status|result|compare|cancel` + body.`task_id`；eval/risk/recommend 全对齐 Python v3.4 | 2026-07-28 联调前置修正 |
| 分析结果存储 | 曾有 Java 阈值内联/自传 MinIO | **v3.2**：Python 转 camelCase + 全量写 MinIO；Java 只存指针，不写 `result_data` | 对齐 D-30/C-14 |
| 权重单位 | 评估侧小数/百分数未定 | 推荐三项合计强制 =100；评估权重不在 CORE 强校验 | 对齐 ARCH §11.2；评估单位等算法定 |
| 大结果资产 ID | 资产中心 SysFile ID | 当前存 Python 回传 `result_asset_id` / `result_url` | 资产中心正式登记留给 ARTIFACT/后续 |

## 3. 产物清单

| 产物 | 路径 |
|---|---|
| DDL | `db/9x_gkxlumenx_topic_enterprise.sql` |
| Entity/DTO | `gkxlumen-topic-async-service-api/.../api/entity/AnalysisTask*`、`api/dto/analysis/*` |
| 对外 Feign | `gkxlumen-topic-async-service-api/.../api/feign/RemoteTopicAsyncService` + `FeignClient.imports` |
| Python Feign | `gkxlumen-topic-async-service-biz/.../feign/RemoteTopicAsyncAiPythonClient*` |
| Service | `service/analysis/**`、`service/impl/analysis/**`、`service/adapter/analysis/**`、`support/analysis/**` |
| Controller | `controller/analysis/AnalysisTaskController` |
| Job | `job/analysis/AnalysisStatusReconcileJob` |
| Nacos/Helm | `helm/.../gkxlumen-topic-async-service-biz-dev.yml` |
| 单测 | `AnalysisAdapterValidationTest` |
| 本 handoff | `ENT-JAVA-ANALYSIS-CORE.md` |

## 4. 验收证据

| 项 | 结果 |
|---|---|
| Maven 编译 | ✅ SUCCESS（async-service-biz） |
| Adapter 参数校验单测 | ✅ `AnalysisAdapterValidationTest` |
| Redis 并发 / SSE / Asset / XXL-Job 代码 | ✅ 已落地 |
| 迁移 commit | ✅ `2aca50d` → `origin/dev`（`feat(topic-async): migrate analysis orchestration`） |
| 网关 / Nacos / Helm / CI 镜像 job | ✅ `/topicAsync/**` + StripPrefix=1（对外 `/topicAsync/topic/v1/analysis/**`）；DataId `gkxlumen-topic-async-service-biz-dev.yml`；deploy job 已加 |
| DDL 执行到目标库 | ⏳ 待运维/本地执行 |
| XXL-Job Admin 注册 `analysisStatusReconcileJob` | ⏳ 待运维配置 |
| Python callback / create 联调 | ⏳ 依赖 AI Python 与 callback 转发 |

## 5. 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ Adapter 只做校验与 Feign 透传 |
| 2 | 调用链 | ✅ 前端 → Java → Python `/internal/gkx-ai/**` |
| 3 | 图谱 | N/A |
| 4 | 可观测性 | ✅ 沿用平台 OTel Agent |
| 5 | CI/CD | ✅ 已 push `origin/dev`，含 async-service 镜像/部署 job |
| 6 | demo2 不 merge lumen | ✅ |
| 7 | 共享聚合核心 | ✅ 分析编排独立 `gkxlumen-topic-async-service`；企业门面仍留 enterprise |
| 8 | 数据策略 | ✅ 任务表 ADS/业务库先行 |
| 9 | 前端规范 | N/A（本单 Java） |
| 10 | 数据血缘 | ✅ 结果透传，不组装业务结果 |

## 6. cost 四字段（估计，完工前再精算）

| 字段 | 值 |
|---|---|
| `actual_tokens` | ~280000（含 CORE 落地 + async 迁移，粗估） |
| `model_used` | cursor-grok-4.5 / gpt-系列 |
| `actual_cost` | ~$4.5（粗估，低于 $10 告警） |
| `cost_warn` | green |

## 7. 开放项

1. 对 `gkxlumenx_topic_enterprise` 执行 `analysis_task` / `analysis_task_node` DDL
2. 在 `gkxlumen-xxl-job-admin` 注册 cron：`analysisStatusReconcileJob`（执行器 AppName=`gkxlumen-topic-async-service-biz`）
3. 配置 `python-ai-base-url` 或保证 Nacos 可发现 `gkx-ai-service`
4. 启用 `file.oss.enable=true`（大结果外置才可写 MinIO）
5. 与绍祖侧联调 create / callback / cancel
6. 已部署库补 `sub_type` 增量迁移（初始化 DDL 已含）
7. 验收人确认 CI Pipeline / K8s rollout 绿后，可由 coordinator 转 `done`
