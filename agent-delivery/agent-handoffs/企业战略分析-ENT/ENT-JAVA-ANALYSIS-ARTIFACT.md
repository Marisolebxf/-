# Handoff：ENT-JAVA-ANALYSIS-ARTIFACT

- **时间**：2026-07-29
- **执行**：agent:api-agent（监管：human:侯佳伟；认领：human:侯佳伟；supervised_by：human:徐滕强）
- **仓库 / 分支**：`lumen-svc-platform` / `dev`；文档仓 `gkx-orchestration` / `dev`
- **派单包**：`ENT-JAVA-ANALYSIS-ARTIFACT-派单包.md`
- **状态**：`review`（代码已 push `9c6dc44`；待 coordinator 验收）
- **前置**：`ENT-JAVA-ANALYSIS-CORE` done；EXPORT PDR 以已签收口径参考，本任务不发明业务定义

## 1. 范围与实现

落仓 **`gkxlumen-topic-async-service`**，复用 ANALYSIS-CORE 创建 / SSE / 取消 / `/asset` 端点。

| 能力 | 说明 |
|---|---|
| 6 类产物任务 | `eval/risk/recommend` × `_report/_export`，挂 `parent_task_id` |
| 本地执行器 | `ArtifactExecutionServiceImpl` + 独立 `analysisArtifactExecutor` |
| 报告 PDF | Thymeleaf `templates/analysis/report.html` → OpenHTMLtoPDF |
| 导出 | EasyExcel 写内存 xlsx；CSV UTF-8 BOM；**不用** `@ResponseExcel` |
| 下载 | `GET .../tasks/{taskId}/asset` 鉴权代理；仅 `success`；文件任务始终代理，禁止永久 MinIO URL |
| 幂等 | `userId+analysisType+parentTaskId+format`；Redis 创建锁；`force` / failed 重试写 `retry_of_task_id` |
| 补偿 | 上传成功但指针/终态未落库时删除孤儿对象；取消竞态不得回写 success |
| 状态修正 | 沿用 `analysisStatusReconcileJob`：超时 failed；无锁 redeliver；有锁保持 |

## 2. 偏离说明（as-built）

| 项 | 派单 / 理想 | As-built | 理由 |
|---|---|---|---|
| success 原子性 | 五步同一事务 | 可恢复状态机：仅指针+任务回写成功后提交 success；SSE 失败不回滚 | MinIO / MySQL / SSE 无法单库事务（🟡） |
| 中文字体 | 镜像内置字体 | 运行时探测 Windows/Linux 字体 + classpath 兜底 | 部署镜像需装 YaHei/Noto CJK（🟡） |
| 报告章节 | 完整产品章节 | 由父任务快照抽取通用章节/导出表 | 业务章节口径仍跟 EXPORT PDR，不自行发明 |
| `file.oss.enable` | 热开关 | 仍需滚动重启 | Bean 条件装配限制 |

## 3. 产物清单

| 产物 | 路径 |
|---|---|
| DDL | `db/9x_gkxlumenx_topic_enterprise.sql` + `db/9x_gkxlumenx_topic_enterprise_artifact_alter.sql` |
| Entity | `AnalysisTaskEntity.retryOfTaskId` |
| 执行 / 渲染 | `service/artifact/*`、`service/impl/artifact/*`、`support/artifact/*` |
| 线程池 / OSS 热更 | `AnalysisArtifactExecutorConfiguration`、`OssClientRefreshConfiguration`、`OssTemplate.rebuildClient()` |
| 模板 | `resources/templates/analysis/report.html` |
| 单测 | Controller / Reconcile / Asset / Create / Render / Snapshot / Types / Execution 共 26 tests |
| Nacos | `ENT-JAVA-ANALYSIS-ARTIFACT-Nacos配置.md` |
| catalog | `API-ENT-full-catalog.md` #102/#106 增补 6 类产物 |
| 本 handoff | `ENT-JAVA-ANALYSIS-ARTIFACT.md` |

## 4. 验收证据

| 项 | 结果 |
|---|---|
| Maven 单测 | ✅ `mvn -pl gkxlumen-topic-async-service/gkxlumen-topic-async-service-biz -am test` → **26 tests 绿** |
| 下载边界 | ✅ 非 success → 404；文件任务即使关闭 JSON 代理也走鉴权流 |
| Reconcile | ✅ 无锁 redeliver；有锁不重复提交 |
| 取消竞态 | ✅ 指针更新失败时删除已上传对象 |
| 渲染冒烟 | ✅ PDF `%PDF`；xlsx `PK`；csv UTF-8 BOM |
| Java/Python bucket 对齐 | ✅ 生产值 `gkxlumen-topic-analysis-results`（`result-bucket`、`file.bucket-name`、Python `GKX_MINIO_BUCKET` 一致） |
| push `origin/dev` | ✅ `9c6dc44` |

代码 commit：`lumen-svc-platform` `9c6dc44` — `feat(topic-async): generate analysis artifacts asynchronously [agent:api-agent]`。

## 5. 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 只读父任务快照，无 NLP/模型调用 |
| 2 | 调用链 | ✅ 前端 → Java；产物不调 Python `/internal/*` |
| 3 | 图谱 | N/A |
| 4 | 可观测性 | ✅ 沿用平台 OTel；SSE/审计保留 |
| 5 | CI/CD | ⏳ `9c6dc44` 已 push，跟 Pipeline |
| 6 | demo2 不 merge lumen | ✅ |
| 7 | 共享聚合核心 | ✅ async-service 编排门面 |
| 8 | 数据策略 | ✅ ADS/父任务结果先行；产物只写资产指针 |
| 9 | 前端规范 | N/A |
| 10 | 数据血缘 | ✅ 不改写父任务指标口径；摘要仅文件元数据 |

## 6. cost 四字段（估计）

| 字段 | 值 |
|---|---|
| `actual_tokens` | 320000（Wave A–D 粗估，in+out） |
| `model_used` | gpt-5 |
| `actual_cost` | 1.54（按 api-agent 默认 80/20 × gpt-5 价：`320000*0.8*3/1e6 + 320000*0.2*15/1e6`） |
| `cost_warn` | green |

## 7. 开放项

1. 目标库执行 `retry_of_task_id` 增量 DDL
2. Nacos 文档已按生产值对齐：Python `http://demo-platform-ai-py:8081`、MinIO `http://192.168.88.43:9900`、bucket `gkxlumen-topic-analysis-results`；实际 DataId 仍须由运维核对/发布，AK/SK 优先由 `GKX_MINIO_*` 注入
3. K8s / 联调环境冒烟：创建 report/export → SSE → `/asset` 下载
4. 部署镜像确认中文字体（YaHei / Noto CJK）
5. coordinator 验收后转 `done`
