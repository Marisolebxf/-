# Handoff：ENT-JAVA-ANALYSIS-CORE

- **时间**：2026-07-27
- **执行**：agent:api-agent（监管：human:侯佳伟）
- **仓库 / 分支**：`lumen-svc-platform` / `dev`
- **派单包**：`ENT-JAVA-ANALYSIS-CORE-派单包.md`
- **状态建议**：代码已 push `origin/dev`；联调与运维项未齐前保持 `in_progress`，联调通过后提 `review`
- **命名裁定（2026-07-27）**：大类 `analysisType`/`analysis_type`，小类 `subType`/`sub_type`；废弃 `mode`；比较篮前端跳转 `?mode=` 不属于本任务，保持不动

## 1. 范围与实现

统一分析任务真源，落在 `gkxlumen-topic-enterprise`，服务内前缀 `/topic/v1/analysis/**`。

| 方法 | 服务内路径 | 说明 |
|---|---|---|
| POST | `/topic/v1/analysis/tasks` | 创建（Java 生成 taskId，Adapter 路由） |
| POST | `/topic/v1/analysis/tasks/list` | 模块内任务列表 |
| GET | `/topic/v1/analysis/tasks/{taskId}` | 详情 |
| GET | `/topic/v1/analysis/tasks/{taskId}/result` | 结果 |
| GET | `/topic/v1/analysis/tasks/{taskId}/asset` | 大结果 JSON 下载 |
| POST | `/topic/v1/analysis/tasks/{taskId}/cancel` | 取消 |
| GET | `/topic/v1/analysis/tasks/running` | running 小窗 |
| GET | `/topic/v1/analysis/tasks/stream` | SSE |
| POST | `/topic/v1/analysis/callback/eval` | 评估回调（`@Inner`） |
| POST | `/topic/v1/analysis/callback/risk` | 风险回调（`@Inner`） |
| POST | `/topic/v1/analysis/callback/recommend` | 推荐回调（`@Inner`） |

表：`analysis_task` / `analysis_task_node`

核心组件：

- `RemoteEnterpriseAiPythonClient` + 独立 `python-ai-base-url` / `python-ai-service-name`
- 显式 Map 路由：`EnterpriseEvalAnalysisAdapter` / `RiskInsightAnalysisAdapter` / `TalentRecommendAnalysisAdapter`
- Redis Lua 并发配额：用户总量 / 用户类型 / 全局
- SSE：复用 `gkxlumen-common-sse` + Redis Pub/Sub
- `AnalysisAssetService`：v3.2 分析结果只存 Python 回传指针，不写完整 `result_data`
- XXL-Job：`analysisStatusReconcileJob`（落在 topic-enterprise）
- Adapter 下游 body：递归 camelCase → snake_case，并补齐 `analysis_type` / `task_id` / `created_by`
- `analysis_task.sub_type` 冗余列 + 列表 `subType` 过滤

## 2. 偏离说明（as-built）

| 项 | 派单 / 旧决议 | As-built | 理由 |
|---|---|---|---|
| `user_id` | 登录态获取、前端传值忽略 | 当前兼容前端传 `user_id`；代码预留登录态注释 | 与 SEARCH-BIZ/COMPARE 现阶段一致；后续可无感切换 |
| Feign 形态 | ARCH 曾写三个 Client | 统一 `RemoteEnterpriseAiPythonClient` | v3.1 收口 |
| 分析结果存储 | 曾有 Java 阈值内联/自传 MinIO | **v3.2**：Python 转 camelCase + 全量写 MinIO；Java 只存指针，不写 `result_data` | 对齐 D-30/C-14 |
| 权重单位 | 评估侧小数/百分数未定 | 推荐三项合计强制 =100；评估权重不在 CORE 强校验 | 对齐 ARCH §11.2；评估单位等算法定 |
| 大结果资产 ID | 资产中心 SysFile ID | 当前存 Python 回传 `result_asset_id` / `result_url` | 资产中心正式登记留给 ARTIFACT/后续 |

## 3. 产物清单

| 产物 | 路径 |
|---|---|
| DDL | `db/9x_gkxlumenx_topic_enterprise.sql` |
| Entity/DTO | `api/entity/AnalysisTask*`、`api/dto/analysis/*` |
| Feign | `feign/RemoteEnterpriseAiPythonClient*` |
| Service | `service/analysis/**`、`support/analysis/**` |
| Controller | `controller/analysis/AnalysisTaskController` |
| Job | `job/analysis/AnalysisStatusReconcileJob` |
| Nacos/Helm | `helm/.../gkxlumen-topic-enterprise-biz-dev.yml` |
| 单测 | `AnalysisAdapterValidationTest` |
| 本 handoff | `ENT-JAVA-ANALYSIS-CORE.md` |

## 4. 验收证据

| 项 | 结果 |
|---|---|
| Maven 编译 | ✅ SUCCESS |
| Adapter 参数校验单测 | ✅ `AnalysisAdapterValidationTest` |
| Redis 并发 / SSE / Asset / XXL-Job 代码 | ✅ 已落地 |
| DDL 执行到目标库 | ⏳ 待运维/本地执行 |
| XXL-Job Admin 注册 `analysisStatusReconcileJob` | ⏳ 待运维配置 |
| Python callback / create 联调 | ⏳ 依赖 AI Python 与 callback 转发 |
| push → CI → K8s | ✅ 已 push `origin/dev`（待看 CI） |

## 5. 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ Adapter 只做校验与 Feign 透传 |
| 2 | 调用链 | ✅ 前端 → Java → Python `/internal/gkx-ai/**` |
| 3 | 图谱 | N/A |
| 4 | 可观测性 | ✅ 沿用平台 OTel Agent |
| 5 | CI/CD | ✅ 已 push，待 Pipeline 结果 |
| 6 | demo2 不 merge lumen | ✅ |
| 7 | 共享聚合核心 | ✅ 落 topic-enterprise |
| 8 | 数据策略 | ✅ 任务表 ADS/业务库先行 |
| 9 | 前端规范 | N/A（本单 Java） |
| 10 | 数据血缘 | ✅ 结果透传，不组装业务结果 |

## 6. cost 四字段（估计，完工前再精算）

| 字段 | 值 |
|---|---|
| `actual_tokens` | TBD |
| `model_used` | gpt-5.6 / cursor |
| `actual_cost` | TBD |
| `cost_warn` | green |

## 7. 开放项

1. 对 `gkxlumenx_topic_enterprise` 执行 `analysis_task` / `analysis_task_node` DDL
2. 在 `gkxlumen-xxl-job-admin` 注册 cron：`analysisStatusReconcileJob`
3. 配置 `python-ai-base-url` 或保证 Nacos 可发现 `gkx-ai-service`
4. 启用 `file.oss.enable=true`（大结果外置才可写 MinIO）
5. 与绍祖侧联调 create / callback / cancel
6. Python callback / create 联调通过后，改 registry → `review`
7. 已部署库补 `sub_type` 增量迁移（初始化 DDL 已含）
