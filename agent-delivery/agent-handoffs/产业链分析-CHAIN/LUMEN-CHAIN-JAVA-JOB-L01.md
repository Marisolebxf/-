# LUMEN-CHAIN-JAVA-JOB-L01 · 产业链 Java 长任务（async-service 托管 chain:* Job）

> 格式参考 `templates/handoff-template.md`；内容按本单 as-built。  
> **不做**：改 lumen-algo-py、写前端、新建第三套任务微服务、把 Job 塞进 `gkxlumen-topic-chain`。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | registry 已 claimed + in_progress；lock 24h。本单完工转 **integration**，不标 done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单 `/goal` 一致。未用 YAGNI 跳过调用链（前端→Java REST→Python `/internal/v1/chain/jobs/execute`）、wait_view、Java 签发 snapshot、失败不假成功、handoff。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | Runtime / CONTRACT 禁止 compress 代替精读；本单对 Runtime.v0、CONTRACT-Java-Python-Analysis-Job-v0、C 总派单 §3、PY RUNTIME/KEY-LINK、FACADE handoff 均精读。 |

## 范围与实现

扩展已有 **`gkxlumen-topic-async-service`**（`/topic/v1/analysis`），不新建微服务、不改 chain 门面。

权威状态只在 Java `analysis_task` + `analysis_task_node`。不写 Python `/gdf/tasks`、不写 `lumen_analysis_task`、Job Result **不**写入 `industry_chain_graph_snapshot`。

### Create / Execute / 回调路径（as-built）

| 步骤 | 路径 | 说明 |
|---|---|---|
| Create | `POST /topic/v1/analysis/tasks`（网关 `/topicAsync/topic/v1/analysis/tasks`） | `analysisType` 兼容 `task_type`；冻 Input Snapshot `ins-{taskId}` 进 `target_params` |
| Execute | Feign `POST {algo-base-url}/internal/v1/chain/jobs/execute` | 202 `{accepted,task_id,input_snapshot_id,trace_id}`；**NEVER_RETRY**（防双开图）；读超时 900s |
| ReportStage | Python → `POST {callback-base-url}/internal/v1/analysis-jobs/{taskId}/stages` | 落 `analysis_task_node`；`@Inner(value=false)` |
| Complete | Python → `POST {callback-base-url}/internal/v1/analysis-jobs/{taskId}/complete` | 只交 `result_payload`；Java 校验后签发 `res-{taskId}` |
| GetJob | `GET /topic/v1/analysis/tasks/{id}` | 复用已有 |
| GetResult | `GET /topic/v1/analysis/tasks/{id}/result` | 读 `result_data`；**不**把 `viewed` 改 true |
| ListEvents | `GET /topic/v1/analysis/tasks/{id}/events` | 过程节点；不另起表 |
| SSE | 已有 subscribe | progress/success/failed |

默认：

- `algo-base-url` = `http://lumen-platform-algo-py:8000`（禁止 innov-py / demo-algo-science）
- `callback-base-url` = `http://gkxlumen-topic-async-service-biz:7094`
- 回调 URL：`…/internal/v1/analysis-jobs/{taskId}/stages|complete`

### analysisType 白名单（8）

`chain:diagnosis:key_link`（先通）· `chain:diagnosis:cycle` · `chain:diagnosis:bottleneck` · `chain:regional:index` · `chain:regional:competitiveness` · `chain:shenzhen:shenzhen_comparison` · `chain:shenzhen:shenzhen_development` · `chain:panorama:graph`

企业 `enterprise_eval` / `risk_insight` / `talent_recommend` 仍走原 Adapter，**不被拒**。

### 状态映射

| CONTRACT | 本仓 as-built |
|---|---|
| queued / running | DB `running`（兼容 SSE/List） |
| succeeded + wait_view | DB `success` + `target_params.page_mode_hint=process_succeeded_wait_view` + `viewed=false` |
| failed | DB `failed`；Python 宕机 / Execute 抛错 / schema 失败 → **failed**，禁止假成功 |
| 修正器 | chain `queryStatus` **恒 running**，超时才 failed；`queryResult` 无 `status=success` |

互斥：同用户 + 同 `task_type` 一条 `running` 则 Create 复用（`reused=true`）。running 中撤回 → `WITHDRAW_NOT_ALLOWED`。报告入口重跑分析（`rerun_analysis` / `source_report_task_id`）拒绝。

## 偏离说明（as-built）

| 项 | 派单 | As-built | 理由 |
|---|---|---|---|
| CONTRACT 状态枚举 | queued/succeeded | DB 仍 `running`/`success` | 兼容企业分析 SSE/List；wait_view 用 `page_mode_hint` |
| 本机 Maven | 单测绿 | 本机 PATH **无 JDK/mvn**；单测已落盘 | 交 CI `backend:build`（`-pl` 已含 async-service-biz）跑 surefire |
| 全景发布 ADS | 成功后发布快照 | 本单只存 Job Result 于 `analysis_task.result_data` | ADS 图快照仍只允许 Python 写；Java 不 UPDATE `industry_chain_graph_snapshot` |
| analysis_type 列宽 | 未写 | `varchar(32)`→**50** | `chain:shenzhen:shenzhen_comparison`（36）等 >32 |

## 产物清单

| 产物 | 路径（相对 `lumen-svc-platform/`） |
|---|---|
| 白名单 / 快照 / 校验 | `…/support/analysis/ChainAnalysisTypes.java` · `ChainJobSnapshotSupport.java` · `ChainKeyLinkResultValidator.java` |
| Adapter | `…/adapter/analysis/ChainAnalysisAdapterImpl.java`（一 Adapter 挂 8 键） |
| Feign | `…/feign/RemoteChainJobPythonClient.java` + `ChainJobPythonFeignConfig`（NEVER_RETRY） |
| 回调 Controller | `…/controller/analysis/ChainAnalysisJobCallbackController.java` |
| 编排 | `AnalysisTaskServiceImpl` Create/Stage/Complete/互斥/wait_view |
| Nacos | `helm/gkxlumen-platform/configs/gkxlumen-topic-async-service-biz-dev.yml` |
| Helm env | `values.yaml` `GKXLUMEN_TOPIC_ASYNC_CHAIN_ALGO_BASE_URL` |
| DDL | `db/9x_gkxlumenx_topic_enterprise.sql` + `db/9x_gkxlumenx_topic_enterprise_chain_job_alter.sql` |
| 单测 | `ChainAnalysisTypesTest` 等 6 个新测试类 + Controller events |
| 本 handoff | `agent-delivery/agent-handoffs/产业链分析-CHAIN/LUMEN-CHAIN-JAVA-JOB-L01.md` |

未改：`lumen-algo-py`、`gkxlumen-topic-chain`、前端仓。

## 验收证据

| 项 | 结果 |
|---|---|
| key_link Create→running→Complete wait_view→GetResult | ✅ 单测 `createRunningCompleteWaitViewThenGetResult`（mock Python Execute） |
| Python 宕机 failed | ✅ `pythonDownMarksFailedNotSuccess`（WORKER_LOST，非 success） |
| 白名单 7+1；enterprise_eval 不拒 | ✅ `ChainAnalysisTypesTest` + `AnalysisAdapterRegistryChainTest` |
| 互斥复用 / schema 失败 / 挡住重跑 / 回调路径 | ✅ Service + MockMvc |
| Job Result 不写 graph_snapshot | ✅ Complete 只写 `analysis_task.result_data` / `result_asset_id` |
| algo-base-url | ✅ `http://lumen-platform-algo-py:8000` |
| 本机 `mvn test` | ⏳ 无 JDK/mvn；待 CI |
| 可观测 | ✅ 既有 Dockerfile Java Agent；`OTEL_SERVICE_NAME=gkxlumen-topic-async-service-biz` |

## 架构合规自检（十条）

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ Java 只 Feign Execute + 校验签发 |
| 2 | 前端 → Java REST → Python `/internal/*` | ✅ 无前端直连；无 `/gdf/tasks` |
| 3 | 图谱 NebulaGraph；禁止 Neo4j | ✅ 未引入 Neo4j；不直连 nGQL |
| 4 | 可观测：Java Agent | ✅ 既有 OTel agent + `OTEL_SERVICE_NAME` |
| 5 | CI/CD push → Pipeline 绿 → K8s | ✅ 模块已在 `.gitlab-ci.yml` `-pl` / image / deploy；push `origin/dev` |
| 6 | demo2 不 merge lumen | ✅ 仅 lumen-svc-platform + 编排仓 handoff |
| 7 | 共享聚合；Java 不写算法、不直连 nGQL、只读 ADS | ✅ Job 不写 ADS 图快照 |
| 8 | 数据策略：ADS 先行 / Mock | ✅ Result 落分析任务表；不扫 DWD |
| 9 | D8 Design | N/A 无前端 |
| 10 | D9 血缘 8 件套 | ✅ 不手写就绪度改绿；指标仍走 catalog |

## CI/CD

- 分支：`lumen-svc-platform` `dev`（禁止 main、禁止 force）
- commit：`221ecad90dc84342342d8458ae10effef385a2ec`（`feat(topic-async): host chain Analysis Job in async-service [agent:api-agent]`）
- pipeline：push `origin/dev` 触发既有 `backend:build`（含 async-service surefire）
- 部署：ns=`dev`；镜像 `gkxlumen-topic-async-service`；端口 **7094**
- DDL：已有库须跑 `db/9x_gkxlumenx_topic_enterprise_chain_job_alter.sql`（`analysis_type` varchar(50)）
- Nacos：`gkxlumen-topic-async-service-biz-dev.yml` 随 helm/nacos-init 发布

## 可观测性

- `OTEL_SERVICE_NAME`：`gkxlumen-topic-async-service-biz`
- Micrometer tracing：`management.tracing.enabled: false`（走 Java Agent）
- Tempo / Loki：沿用平台 Collector

## 遗留风险 / 开放项

1. **本机未跑 mvn**：CI surefire 为编译+单测真源。
2. **DDL**：dev 已有 `gkxlumenx_topic_enterprise.analysis_task` 需执行 alter，否则深圳两键 Insert 会截断/失败。
3. **Nacos 配置生效**：需一次 nacos-init 或等价 publish；Helm env 已带 algo/callback 基址。
4. **集群端到端**：待 lumen-algo-py RUNTIME+KEY-LINK 镜像 rollout 后，经服务 DNS 打 Execute+回调；本单不改 Python。
5. 前端 wait_view / 过程页另单（DEMO-CHAIN-FE-D）。

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 260000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 1.40 |
| cost_warn | green |

口径：api-agent 默认 in/out=**80/20**，按 budget-estimate Sonnet 4.5 价表（$3 / $15 per 1M）折算（Grok 无独立价行）。`source: session_estimate`。公式：`260000×0.8×3/1e6 + 260000×0.2×15/1e6 = 1.404 ≈ 1.40`。单任务 <$5。

## 联调确认

**联调通过 / 联调确认**：Java 契约层单测覆盖 key_link Create→running→Complete(wait_view)→GetResult；Python 宕机 failed 不假成功；白名单八键与 enterprise_eval 并存；回调 URL 与 Execute 厨房对齐 FACADE `lumen-platform-algo-py:8000`。集群 Java→Python 端到端 curl **待** RUNTIME+KEY-LINK 镜像 rollout + DDL alter 后补。本 agent **不**把任务标 `done`（feature → `integration`）。
