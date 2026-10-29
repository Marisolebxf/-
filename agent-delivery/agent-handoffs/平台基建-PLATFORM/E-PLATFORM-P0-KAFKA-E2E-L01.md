# E-PLATFORM-P0-KAFKA-E2E-L01 · dev 实证 Kafka 正式链路（异步分析 → gkx.analysis.result → Worker → Java 回调）

> 结论：**红**。两次真实创建的 `enterprise_eval` 任务都在 Python AI 创建下游任务时失败，原因是 `gkxlumen-platform-ai-py` 连不上 MySQL `10.50.11.76`（2003 超时）。链路没有走到 Kafka，`gkx.analysis.result` end offset 仍为 0。失败归类：**与 Kafka 无关的既有问题（AI Python 数据库依赖不可达）**。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:qa-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 按派单状态 in_progress 执行。本叶未调用 task-registry MCP；未改代码、未 commit、未 push。本文件未提交编排仓，由监管人提交。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单强度一致。QA 只读实测，没有往仓里写脚本；探针脚本放在 `%TEMP%`。可观测（traceId）、D12、D13、handoff 均未用 YAGNI 跳过。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本次会话未挂载。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `ARCH-MSG-KAFKA` |
| 图 diff | 无变化。本叶只实测，不改图。实测结果：前端/测试 → Java `gkxlumen-topic-async-service` → Python `gkxlumen-platform-ai-py` 这一段在 AI 侧失败，后面的 Kafka 段没有被触发。 |
| 会签态 | `draft`（沿用基线 §1.1 frontmatter，未改） |
| 说明 | 实测确认：图里只有 `enterprise_eval` / `risk_insight` / `talent_recommend` 三种类型的 `task_completed` 走 Kafka（`lumen-topic-py/gkx_ai_service/views/callback.py` `_VALID_ANALYSIS_TYPES`）。产业链、SVC、政策类任务不经过本 topic。 |

## 范围与实现

### 1. 现成 e2e 作业是否覆盖 Kafka 路径：不覆盖

- `lumen-ui-topic/.gitlab-ci.yml` 的 `e2e:chain-gold`（L298）在 Playwright 镜像里跑 `e2e/chain-gold.spec.ts` 全部用例。`lumen-svc-platform`（L582）和 `lumen-algo-py`（L191）的同名作业只是 `trigger` 这个项目，跑的是同一套用例。
- 用例 #1–#6 是产业中心：检索、概览、深链、全景、诊断 key-link 等待页（#4）、深圳页不得空跑（#5）。唯一会真实创建任务的是 #4，类型是产业链诊断，走 Java `dispatchChainExecute` / Chain 适配器，不是 eval/risk/recommend，因此不发布到 `gkx.analysis.result`。
- 所以本叶**没有触发任何 CI 作业**（跑 chain-gold 不能证明 Kafka 链路，反而会多产生产业链任务记录）。

### 2. 等效做法：经已发布前端调 Java 创建接口

- 入口：已发布前端 `http://10.50.69.111:30892`，nginx `/api` → `gkxlumen-platform-gateway` → `/topicAsync/**`（StripPrefix）→ `gkxlumen-topic-async-service` 的 `AnalysisTaskController`（`/topic/v1/analysis`）。没有直连 Java 或 Python，符合调用链铁律与 D12。
- 鉴权：接口为 `@Inner(value = false)`，网关匿名可达。Java `AnalysisUserSupport.resolveUserId` 目前只取请求里的 `user_id`；前端 `resolveUserId()` 未登录时为 `guest`。本叶用 `guest`，与前端行为一致，无需令牌。
- 入参：复用 `guest` 名下最近一次成功的企业评估 `EVAL-20261013-002` 的 `targetParams`（`subType=technology`，2 个企业编码、5 个指标与权重、`templateId`、原 `analysis_fp`），加 `force=true`。等同前端「重新分析」，跳过当天成功复用，不绕过运行中单飞。
- 状态查询：`GET /tasks/{taskId}?user_id=guest`（同一 controller 的详情端点）。

### 3. Kafka 只读探针

本机 Python 3.12 + aiokafka 0.14.0，PLAINTEXT。脚本 `%TEMP%\gkx_kafka_probe.py`（不进仓）：

- `AIOKafkaConsumer`（不带 `group_id`、不提交）只做 `topics()`、`beginning_offsets` / `end_offsets`。
- `AIOKafkaAdminClient` 做 `list_consumer_groups` 与 `list_consumer_group_offsets`（`gkxlumen-ai-worker`、`demo-ai-worker`）。
- 没有生产消息，没有建删 topic，没有用业务组名建消费者，没有提交 offset。
- `describe_consumer_groups` 在本机 aiokafka 0.14 上报协议解码错（`Buffer underrun decoding string`），已去掉，组成员数未取到。

## 验收证据

### 触发记录

| # | 时间（本地） | 请求 | HTTP / code | taskId | traceId | 终态 | 失败原因（Java `errorMsg` 原文） |
|---|---|---|---|---|---|---|---|
| 1 | 2026-10-18 01:19:24 | `POST /api/topicAsync/topic/v1/analysis/tasks`，`enterprise_eval` + `force=true` | 200 / 0，`reused=false`，`status=running` | `EVAL-20261018-001` | `2d5795e25e3f87c7a8e586ee2f2cf622` | 01:19:35 `failed` | `创建下游任务失败：系统异常: (2003, "Can't connect to MySQL server on '10.50.11.76' (timed out)")` |
| 2（同条件重试一次，用于区分偶发） | 2026-10-18 01:21:25 | 同上 | 200 / 0，`status=running` | `EVAL-20261018-002` | `d004fea933f4bef117da6c98da8afe51` | 01:21:35 `failed` | 同上，原文一致 |

两次都是创建后约 10 秒失败，与 MySQL 连接超时一致。错误前缀「创建下游任务失败」来自 Java `EnterpriseEvalAnalysisAdapterImpl.unwrap`，后半段 `(2003, ...)` 是 pymysql 错误，说明 Java → Python `/internal/*` 这一跳是通的，失败点在 AI Python 访问 MySQL。

### offset 前后对比

| 对象 | 触发前 01:09:52 | 第 1 次后 01:20:01 | 第 2 次后 01:22:09 | 期望 | 结果 |
|---|---|---|---|---|---|
| `gkx.analysis.result[0]` end | 0 | 0 | 0 | > 0 | ❌ 未增长 |
| `gkx.analysis.result.dlq[0]` end | 0 | 0 | 0 | 不增长 | ✅（无意义：上游未发布） |
| `gkx.demo.analysis.result[0]` end | 0 | 0 | 0 | 不涉及 | — |
| `gkx.demo.analysis.result.dlq[0]` end | 0 | 0 | 0 | 不涉及 | — |
| 组 `gkxlumen-ai-worker` 已提交 offset | 无 | 无 | 无 | = end | ❌ 无可比数据 |
| 组 `demo-ai-worker` 已提交 offset | 无 | 无 | 无 | 不涉及 | — |
| `list_consumer_groups` | `demo-ai-worker`、`gkxlumen-ai-worker`、`zp-tts-test-group` | 同 | 同 | 含正式组 | ✅ 正式 Worker 组存在 |

4 个 topic 的 begin offset 均为 0；4 个 topic 均存在。

### 根因定位（只读）

- `lumen-topic-py/k8s/dev-ai-py.yaml` L59–60：`GKX_MYSQL_HOST = 10.50.11.76`，库 `demo_gkxlumenx_dwd`。
- `lumen-topic-py/k8s/dev-search-py.yaml` L55–56：同一个库，`GKX_MYSQL_HOST` 已在 `0b1309f`（2026-10-17，`fix(k8s): search 改连现网 MySQL/ES…`）改为 `10.50.11.76`。该提交也动了 `dev-ai-py.yaml`，但没有改 MySQL 地址；Kafka 提交 `21cc71e` 对 `dev-ai-py.yaml` 只替换了总线变量。
- 本机到 `10.50.11.76:3306` 可连通（`Test-NetConnection` True），集群 Pod 内超时。说明是集群到该地址不通，不是库宕机。本机无 kubectl 凭证，未进 Pod 复核。
- 历史：`EVAL-20261013-002`（10-13）成功；`EVAL-20261014-001`（10-14）失败原因为 `DWD enterprise_base 未找到企业`，当时还能连上库。`gkxlumen-platform-ai-py` 于 2026-10-18 00:33（job 13295）重新部署，之后连库超时。重新调度后 Pod 落到不通 `192.168.88.x` 的节点，或该网段对集群关闭，两者都可能，本叶无法区分。

## 问题清单

- **主阻塞**：`gkxlumen-platform-ai-py` 连 MySQL `10.50.11.76` 超时，`enterprise_eval` 无法创建下游任务，Kafka 段不会被触发。风险洞察、人才推荐由同一个 AI 进程处理，按同一份 env 推断也会受影响（未实测，避免多造记录）。
- **观察项（与本叶无关）**：经网关调用 `POST /api/enterprise/topic/v1/search/by-codes` 和 `POST /api/enterprise/topic/v1/search/query` 均返回 HTTP 500（`{"status":500,"path":"/topic/v1/search/query"}`）。因此本叶无法预先核验企业编码。
- **观察项**：本机 aiokafka 0.14 `describe_consumer_groups` 解码失败，无法查看 Worker 组成员数。

## 修改内容

- 无。业务仓与编排仓零代码改动；只新增本 handoff。
- 线上数据：新增 2 条失败的分析任务记录 `EVAL-20261018-001`、`EVAL-20261018-002`（user `guest`，类型 `enterprise_eval`）。未删除，留作证据。

## 测试结果

| DoD | 结果 | 证据 |
|---|---|---|
| 1. 触发至少一次真实异步分析，`gkx.analysis.result` end offset 从 0 增长 | ❌ | 已真实触发 2 次（HTTP 200，Java 落库），但 AI 未完成；end offset 前后均为 0 |
| 2. `gkxlumen-ai-worker` lag=0、`.dlq` 无新增、Java 任务状态完成 | ❌ | 无消息可消费，组无已提交 offset；DLQ 为 0；两条任务 Java 侧终态 `failed`，不是 `success` |
| 3. handoff 含 pipeline/job ID、offset 前后对比、任务 ID 或 traceId | ✅ | 见上方触发记录、offset 表与 CI/CD 节 |

**失败分类**：与 Kafka 无关的既有问题，即 AI Python 的数据库依赖在集群内不可达。不属于 Kafka 不可达（探针 3 次均连通）、Worker 未消费、回调失败或进 DLQ，因为链路没有走到这些环节。也不是登录或前端问题（创建接口 200，Java 正常落库并调到 Python）。

**建议修复角色**：`devops-agent` 改 `lumen-topic-py/k8s/dev-ai-py.yaml` 的 `GKX_MYSQL_HOST`，与 `dev-search-py.yaml` 对齐到现网库；账号与库名由 `algorithm-agent` 确认与 search 一致。改完推 dev，点 `deploy:ai-py`（QA 不点 deploy）。之后 coordinator 再派本叶复测，复测命令见下。

## 遗留风险

- 修复 MySQL 后，Kafka 段仍是首次真实运行，可能暴露新问题：Worker 写 rustfs、Worker 回调 `gkxlumen-platform-topic-async-service:7094`、64MiB 上限。复测时需按 DoD 2 再看 lag 和 DLQ。
- 即使 MySQL 通了，选用的两个企业编码（`12ceab1a…`、`09f2c519…`）可能已不在 DWD（10-14 曾报 `12ceab1a…` 未找到），会以 `task_failed` 结束，不走 Kafka。复测前需由前端或数据侧给出确认存在的企业编码；企业检索接口目前 500，也要先修。
- `EVAL-20261018-001/002` 两条失败记录会出现在 `guest` 的评估历史中。

## CI/CD（必填）

- 分支：不涉及（本叶不提交）
- commit：不涉及。被测部署对应 `lumen-topic-py` `21cc71e8`
- pipeline URL / ID：**本叶未触发任何 pipeline**（现成 e2e 不覆盖 Kafka 路径，见范围 §1）。只读查询被测部署所在流水线：`lumen-topic-py`（project id 9）pipeline **2547**（`21cc71e8`，状态 manual）：`py:smoke` 13290 ✅，`py:image:ai/search/worker` 13291–13293 ✅，**`deploy:ai-py` 13295 ✅（2026-10-17T16:33:46Z）**，**`deploy:ai-worker` 13296 ✅**，`deploy:search-py` 13294 未点（manual）
- 部署 namespace / 镜像 tag：未改；被测 AI / Worker 镜像 tag 为 `21cc71e8` 构建
- K8s rollout：本叶未执行
- dev 测试 URL / 命令与结果：
  - 创建：`POST http://10.50.69.111:30892/api/topicAsync/topic/v1/analysis/tasks`，body `{"user_id":"guest","analysisType":"enterprise_eval","force":true,"params":<EVAL-20261013-002 的 targetParams>}` → 200 / `EVAL-20261018-001`、`EVAL-20261018-002`
  - 详情：`GET .../tasks/{taskId}?user_id=guest` → 两条均为 `failed`（原因见验收证据）
  - Kafka：`python %TEMP%\gkx_kafka_probe.py`（只读）→ 见 offset 表
  - 复测：修复后重复以上三步；看 `gkx.analysis.result` end ≥ 1、`gkxlumen-ai-worker` 已提交 offset = end、`.dlq` = 0、详情 `status=success` 且带 `resultBucket` / `resultAssetId`

## 可观测性

- OTEL_SERVICE_NAME：未改（被测 `gkxlumen-ai-service` / `gkxlumen-ai-worker`）
- traceId（dev 抽样，网关响应头 `X-Trace-Id` / `traceparent`）：
  - `EVAL-20261018-001`：`2d5795e25e3f87c7a8e586ee2f2cf622`（`traceparent=00-2d5795e25e3f87c7a8e586ee2f2cf622-ac6c4984af55d158-01`）
  - `EVAL-20261018-002`：`d004fea933f4bef117da6c98da8afe51`
- Tempo / Loki：本机无访问入口，未查。建议修复方按上面两个 traceId 在 Tempo 确认失败 span 在 `gkxlumen-ai-service` 的 MySQL 连接上。

## 涉及文件

- 只读：`lumen-ui-topic/.gitlab-ci.yml`、`lumen-ui-topic/e2e/chain-gold.spec.ts`、`lumen-ui-topic/e2e/playwright.config.ts`、`lumen-ui-topic/src/composables/useEvalTask.ts`、`lumen-ui-topic/src/utils/currentUser.ts`
- 只读：`lumen-svc-platform/.gitlab-ci.yml`、`gkxlumen-topic-async-service` 的 `AnalysisTaskController.java`、`AnalysisTaskServiceImpl.java`、`EnterpriseEvalAnalysisAdapterImpl.java`、`AnalysisTaskCreateRequest.java`、`AnalysisUserSupport.java`、`TopicAsyncAiPythonRoutingClient.java`
- 只读：`lumen-topic-py/gkx_ai_service/views/callback.py`、`gkx_ai_worker/consumer.py`、`k8s/dev-ai-py.yaml`、`k8s/dev-search-py.yaml`、`k8s/dev-ai-worker.yaml`
- 新增：`agent-delivery/agent-handoffs/平台基建-PLATFORM/E-PLATFORM-P0-KAFKA-E2E-L01.md`（本文件，未提交）

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未改代码；实测确认 Java 只做适配与透传 |
| 调用链 前端 → Java → Python `/internal/*` | ✅ 从已发布前端 nginx 经网关进 Java，没有直连 Java 或 Python |
| 图谱 Nebula | ✅ 未涉及 |
| 可观测 | ✅ 记录了网关 traceId；未改 OTel 配置 |
| CI/CD | ✅ 未点任何 deploy / helm 作业；未触发 e2e（理由见范围 §1）；只用 GitLab API 只读查 pipeline |
| demo 不污染 lumen | ✅ 只打 lumen 前端 30892；只看正式 topic 和正式组 |
| 方案 A / 前端只调 Java | ✅ |
| 数据走 ADS | ✅ 未改数据配置 |
| D8 / D9 / D10 | ✅ 无页面、指标、交互改动 |
| D12 | ✅ 请求只经 `gkxlumen-*`；被测 AI 是 `gkxlumen-platform-ai-py` |
| D13 | ⚠️ 配置层面成立：topic 存在、正式 Worker 组在线、Java 不连总线。运行层面**未实证**，因为上游 AI 失败，没有消息发布 |
| 红线 | ✅ 未改代码、未 commit/push、未调用 task-registry MCP、未碰 `E:\gkx-lumen\`；token 只读进内存变量后清除，没有打印或落盘；Kafka 只读；线上只新增 2 条任务记录 |

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 150000 |
| model_used | claude-opus-5.5 |
| actual_cost | 4.05 |
| cost_warn | green |

口径：无 Console 精确 in/out，按会话估算 150000 tokens。预算表 C 旗舰档（输入 $15/M、输出 $75/M），80/20：`150000×0.8×15/1e6 + 150000×0.2×75/1e6 = 1.80 + 2.25 = 4.05`。低于 $10 暂停线。`source: session_estimate`。（首轮值，累计见下方复测节）

## 复测（2026-10-18）

> 结论：**仍为红**。修复 `lumen-topic-py` `a11364e` 已部署，但错误原文不变。复测确认 2003 不是 ai-py 报的，是它下游的算法服务 `lumen-algo-py`（`lumen-platform-algo-py`）报的；该服务的 MySQL 仍指向 `10.50.11.76`。**更正首轮根因**：首轮把故障归到 `dev-ai-py.yaml` 的 `GKX_MYSQL_HOST`，这个判断不对。ai-py 的企业评估路径不读这个变量；真正需要改的是 `lumen-algo-py/k8s/api.yaml`（以及 `worker.yaml`）的 `LUMEN_ALGO_MYSQL_HOST`。分类不变：与 Kafka 无关的既有问题（算法服务数据库依赖不可达）。

### 被测部署

- `lumen-topic-py`（project 9）pipeline **2556**（`a11364ee`）：`py:smoke` 13420 ✅，`py:image:*` 13421–13423 ✅，**`deploy:ai-py` 13425 ✅**；`deploy:ai-worker` 13426、`deploy:search-py` 13424 为 manual 未点（本叶不点）。
- `lumen-algo-py`（project 8）最近部署：pipeline **2553**（`c0290161`，`fix(ci): e2e:chain-gold trigger full project path`），`deploy:api` **13412** ✅、`deploy:worker` **13413** ✅（2026-10-17T17:12Z）。该提交 `k8s/api.yaml`：`LUMEN_ALGO_MYSQL_HOST = 10.50.11.76`，`LUMEN_ALGO_MYSQL_DWD_DB = demo_gkxlumenx_dwd`。`origin/dev` 上 `api.yaml`、`worker.yaml` 仍是 `10.50.11.76`。

### 企业编码选取（只读）

- 口径：企业校验在 `lumen-algo-py/lumen_common/tasks/executor.py` 的 `validate` 节点，调 `real_data.resolve_enterprises`，即 `SELECT … FROM demo_gkxlumenx_dwd.enterprise_base WHERE org_id IN (…) OR enterprise_code IN (…)`。`assert_real_identifiers` 已是 no-op，不按前缀拒绝。
- 查询：按派单从 `dev-ai-py.yaml` 读连接信息进内存（口令不打印、不落盘），连 `10.50.11.76:3306/demo_gkxlumenx_dwd`，会话设 `READ ONLY`，只执行 SELECT。
- 结果：`enterprise_base` 共 50 行。Java 侧历史成功任务里的 6 个编码（`12ceab1a…`、`09f2c519…`、`0a2b8220…`、`0a063a94…`、`09c00f06…`、`09c373a7…`）**全部不在该库**。改从库内选专利记录最多的企业：`demo-org-bj-10`（`enterprise_patent_history` 6 行）。
- 注意：算法服务修好后连的就是这个库，所以这个编码对修复后的复测有效；历史编码在新库里不存在，复测不能再用。

### 触发记录

| # | 时间（本地） | 入参要点 | HTTP / code | taskId | traceId | 终态 | 失败原因（Java `errorMsg` 原文） |
|---|---|---|---|---|---|---|---|
| 3 | 2026-10-18 01:53:16 | `enterprise_eval`，`subType=competitiveness`，`enterpriseCodes=["demo-org-bj-10"]`，`TPL-SYSTEM-COMPETITIVENESS`，新 `analysis_fp=4e0baa8d…bb6c2`，`force=true` | 200 / 0，`reused=false`，`running` | `EVAL-20261018-003` | `fc7b25d575e93de7ccb2c4f02932dd81`（`traceparent=00-fc7b25d575e93de7ccb2c4f02932dd81-8272911f0d40ff2a-01`） | 01:53:27 `failed` | `创建下游任务失败：系统异常: (2003, "Can't connect to MySQL server on '10.50.11.76' (timed out)")` |

**没有重试**：派单允许同样的失败重试 1 次。但根因已定位到一个确定的配置项，重试只会多一条失败记录，不会带来新信息，所以没有重试。

### 定位依据

- 调用顺序：Java `EnterpriseEvalAnalysisAdapterImpl` → ai-py `evalCreateTask` → `gkx_ai_service/algo_client.py`，地址 `GKX_ALGO_BASE_URL=http://lumen-platform-algo-py:8000` → 算法服务 `lumen_algo_service/views/tasks.py` 的 `create-and-start` → `task_manager.create_and_start` 写库。
- 「系统异常: {e}」这个前缀在 lumen 仓里只出现在 `lumen-algo-py/lumen_algo_service/views/tasks.py:97`。`lumen-topic-py/gkx_ai_service` 中没有任何代码读 `GKX_MYSQL_*`，只有 search、svc 和 `gkx_common` 在用。
- 外层「创建下游任务失败：」来自 Java 适配器 `unwrap`。

### offset 前后对比

| 对象 | 触发前 01:48:26 | 触发后 01:56:27 | 期望 | 结果 |
|---|---|---|---|---|
| `gkx.analysis.result[0]` end | 0 | 0 | ≥ 1 | ❌ |
| `gkx.analysis.result.dlq[0]` end | 0 | 0 | 不增长 | ✅（上游未发布，无意义） |
| `gkx.demo.analysis.result[0]` end | 0 | 0 | 不涉及 | — |
| `gkx.demo.analysis.result.dlq[0]` end | 0 | 0 | 不涉及 | — |
| `gkxlumen-ai-worker` 已提交 offset | 无 | 无 | = end | ❌ 无可比数据 |
| `demo-ai-worker` 已提交 offset | 无 | 无 | 不涉及 | — |

4 个 topic 均存在；`list_consumer_groups` 仍返回 `demo-ai-worker`、`gkxlumen-ai-worker`、`zp-tts-test-group`。

### DoD 重判

| DoD | 结果 | 证据 |
|---|---|---|
| 1. 真实触发，`gkx.analysis.result` end offset 从 0 增长 | ❌ | `EVAL-20261018-003` 已真实创建，但在算法服务创建阶段失败；end 仍为 0 |
| 2. Worker lag=0、DLQ 无新增、Java 任务完成 | ❌ | 没有消息；组无已提交 offset；DLQ 为 0；Java 终态 `failed` |
| 3. handoff 含 pipeline/job ID、offset 对比、任务 ID / traceId | ✅ | 本节 |

### 失败分类与建议

- **分类**：与 Kafka 无关的既有问题，算法服务 `lumen-platform-algo-py` 的 MySQL `10.50.11.76` 在集群内不可达。
- **建议修复角色**：`devops-agent` 把 `lumen-algo-py/k8s/api.yaml` 与 `worker.yaml` 的 `LUMEN_ALGO_MYSQL_HOST` 改为 `10.50.11.76`，库名保持 `demo_gkxlumenx_dwd`。账号口令由 `algorithm-agent` 确认现网可用，并核对 `LUMEN_ALGO_MYSQL_*` 下其他库名（ODS、任务表所在库）在 10.50.11.76 上是否存在。推 dev 后点 `deploy:api`、`deploy:worker`（QA 不点）。
- `lumen-topic-py` 的 `a11364e` 不需要回退，保留无害；search 与 ai-py 已经一致。
- **下一轮复测**：直接用 `demo-org-bj-10` 和本节的入参。修复后若出现 `DWD 未汇聚到企业特征` 一类数据错误，结果会是 `task_failed` 同步回 Java，同样不走 Kafka。届时需要换成画像字段更全的企业，或改测风险洞察。

### 线上数据

累计新增 3 条失败的分析任务记录：`EVAL-20261018-001`、`-002`、`-003`（`guest`，`enterprise_eval`），未删除。数据库只读，没有写入。

### 红线自检（复测）

未改代码、未 commit/push、未点 deploy/helm、未生产 Kafka 消息、未用业务组名建消费者、未提交 offset、未写数据库（会话 `READ ONLY`）、未打印或落盘 token/口令、未调用 task-registry MCP。

### Cost 回填（累计）

| 字段 | 值 |
|------|-----|
| actual_tokens | 220000（首轮 150000 + 复测 70000） |
| model_used | claude-opus-5.5 |
| actual_cost | 5.94 |
| cost_warn | green |

口径：C 旗舰档 80/20，`220000×0.8×15/1e6 + 220000×0.2×75/1e6 = 2.64 + 3.30 = 5.94`。低于 $10 暂停线。`source: session_estimate`。

## 第二次复测（2026-10-18）

**结论：正式链路 Java → ai-py → Kafka → Worker → Java 回调在 dev 上跑通了一次，DoD 三条全部 ✅。**

### 部署证据（复测前提）

| 项 | 值 |
|---|---|
| 修复 commit | `lumen-algo-py` `ee939a81`：`k8s/api.yaml`、`k8s/worker.yaml` 的 `LUMEN_ALGO_MYSQL_HOST` 改为 `10.50.11.76` |
| pipeline | 2557 |
| job | `deploy:api` 13433，`deploy:worker` 13434（rollout 成功；镜像 `:latest` 与 `:ee939a81` digest 相同） |
| 运维前置核对 | 新库上 dwd/ads/cfg 三库和 13 张 `enterprise_*` 表都在；`enterprise_risk_summary` 为空，所以本轮测企业评价，不测风险洞察 |

### 触发

| 项 | 值 |
|---|---|
| 入口 | 已发布前端 `http://10.50.69.111:30892/api` → gateway → `gkxlumen-topic-async-service` `POST /topic/v1/analysis` |
| 入参 | `analysis_type=enterprise_eval`，`sub_type=competitiveness`，企业 `demo-org-bj-10`，`force=true`，`user_id=guest` |
| 创建时间 | 2026-10-18 02:14:20，HTTP 200，`code=0`，`reused=false` |
| 任务 ID | **`EVAL-20261018-004`** |
| traceId | **`bffaa343fd0ec85db16f627c3f7d6f81`**（`traceparent: 00-bffaa343fd0ec85db16f627c3f7d6f81-4fb8ba46481da7ba-01`） |
| Java 终态 | 02:14:30 查询为 `success`，节点 4/6；结果指针 `gkx-analysis-results` / `analysis/enterprise_eval/202610/EVAL-20261018-004/result.json`（2011 B），完成时间 02:14:23 |

### Offset 对比（只读探针，无 group_id，不提交 offset）

| 项 | 前（02:13:54） | 后（02:14:46） | 期望 | 判定 |
|---|---|---|---|---|
| `gkx.analysis.result[0]` end | 0 | **1** | 增长 | ✅ |
| `gkx.analysis.result.dlq[0]` end | 0 | 0 | 不增 | ✅ |
| `gkx.demo.analysis.result[0]` end | 0 | 0 | 不涉及 | — |
| `gkx.demo.analysis.result.dlq[0]` end | 0 | 0 | 不涉及 | — |
| `gkxlumen-ai-worker` 已提交 offset | 无 | **1** | = end | ✅ lag 0 |
| `demo-ai-worker` 已提交 offset | 无 | 无 | 不涉及 | — |

end 恰好为 1，说明没有重试重发。结果对象存储指针只由 Worker 写入，并经 `callback/eval` 回填 Java。这两点加上 offset，可以确认任务成功走的是 Kafka 路径，不是同步直转。

### DoD 判定（第二次复测）

| DoD | 结果 | 证据 |
|---|---|---|
| 1. 真实触发，`gkx.analysis.result` end offset 从 0 增长 | ✅ | `EVAL-20261018-004`，end 0 → 1 |
| 2. Worker lag=0、DLQ 无新增、Java 任务完成 | ✅ | 已提交 1 = end 1；DLQ 0；Java `success` 且有结果指针 |
| 3. handoff 含 pipeline/job ID、offset 对比、任务 ID / traceId | ✅ | 本节 |

### 任务表位置（只读核对）

| 侧 | 库.表 | 配置依据 | `EVAL-20261018*` 只读查询 |
|---|---|---|---|
| Java `gkxlumen-topic-async-service` | `gkxlumenx_topic_enterprise.analysis_task` @ 10.50.11.76 | `lumen-svc-platform/helm/gkxlumen-platform/configs/gkxlumen-topic-async-service-biz-dev.yml` L9；`AnalysisTaskEntity` `@TableName("analysis_task")`；host 由 `values-lumen.yaml` L38 → `_helpers.tpl` L124–125 注入 `MYSQL_HOST` | 4 行：-001/-002/-003 `failed`（MySQL 2003 → 10.50.11.76），-004 `success` |
| 算法 `lumen-platform-algo-py` | `gkxlumenx_cfg.lumen_analysis_task` @ 10.50.11.76 | `lumen-algo-py/lumen_common/tasks/repository.py` L11–14；`k8s/api.yaml` L36、`worker.yaml` L34 `LUMEN_ALGO_MYSQL_CFG_DB` | 1 行：-004 `success`，progress 100 |

两张表本来就分开（各服务各管自己的状态），靠 `task_id` 加 HTTP 回调对齐。本轮链路已经闭合，所以**不算失败**。运维看不到 `EVAL-20261018*` 的原因：-001 到 -003 在算法服务连库这一步就失败了，根本没写进算法表；-004 是修复后的第一条。

### 失败分类

本轮无失败。顺带记录几项与 Kafka 无关的观察，没有在本单处理：
- 经 gateway 调企业检索 `search/query` 和 `search/by-codes` 返回 HTTP 500（前几轮已见）。
- `enterprise_risk_summary` 是空表，风险洞察链路目前没有数据可测；`talent_recommend` 本单未覆盖。
- `e2e:chain-gold` 只覆盖产业中心，不覆盖 Kafka 路径；若要回归，需要另立单补用例（QA 不改代码）。

### 线上数据

累计 4 条分析任务记录（`guest`，`enterprise_eval`）：-001/-002/-003 失败、-004 成功；另有 -004 的算法表记录和结果对象 `result.json`。都没有删除。数据库全程 `READ ONLY` 会话，只执行 SELECT。

### 红线自检（第二次复测）

未改代码、未 commit/push、未点 deploy/helm、未生产 Kafka 消息、未用业务组名建消费者、未提交 offset、未写数据库、未打印或落盘 token/口令、未调用 task-registry MCP。临时探针脚本只在 `%TEMP%`，不在任何仓里。

### Cost 回填（累计）

| 字段 | 值 |
|------|-----|
| actual_tokens | 260000（首轮 150000 + 复测 70000 + 第二次复测 40000） |
| model_used | claude-opus-5.5 |
| actual_cost | 7.02 |
| cost_warn | green |

口径：C 旗舰档 80/20，`260000×0.8×15/1e6 + 260000×0.2×75/1e6 = 3.12 + 3.90 = 7.02`。低于 $10 暂停线。`source: session_estimate`。

## Kafka 迁移收口（2026-10-18，agent:coordinator-agent）

### 最终独立验收（qa-agent，未参与实施）

| DoD | 结论 | 说明 |
|---|---|---|
| 线上都已部署 | ✅（有一项未验证） | 各受影响服务都已部署 dev 最新提交。helm 双管已由 HELM-FIX-L01 解除；release 存储值里的旧 AMQP 由 HELM-FIX-L02（rev 17，job 13452）用 `env: []` 覆盖，这一点是推断，没有直接读出 release 值。rev 17 之后 gateway / auth / upms / demo-a / innov 经 30887 探测正常；**demo-b-biz 没有只读入口，未验证** |
| 联通正常 | 正式链路 ✅ / 原型链路 ⚪ | 正式链路：`EVAL-20261018-004` 走 Kafka 完成，coordinator 独立复核 offset，结果 topic end=1、组已提交 1、DLQ 0。原型链路：现有架构里没有合法调用方，未实证 |
| 无残留 | ✅ | 5 个仓 origin/dev 的运行时代码、清单、helm、requirements 都没有 rabbit / amqp / pika；demo-svc-topic-py CI 注释已由 L02 清理 |

### 修复叶（本轮派单）

| 任务 | 提交 | 作用 |
|---|---|---|
| E-PLATFORM-P0-KAFKA-HELM-FIX-L01 | demo-svc-platform `4c0aa0d` | helm 不再管 `demo-platform-ai-py`，只由算法 CI 部署 |
| E-PLATFORM-P0-KAFKA-AIPY-DB-L01 | lumen-topic-py `a11364e` | ai-py 库地址与 search 对齐到 10.50.11.76 |
| E-PLATFORM-P0-KAFKA-ALGOPY-DB-L01 | lumen-algo-py `ee939a81` | 算法服务库地址改为 10.50.11.76（链路真正的阻塞点） |
| E-PLATFORM-P0-KAFKA-HELM-FIX-L02 | demo-svc-platform `4eb9e520`、demo-svc-topic-py `0ed52603` | 清空 release 存储的旧 env，删除 CI 里的 RabbitMQ 注释 |

### 待人决策（AI 不替人拍板，公约 §3.1）

1. **原型 Kafka 链路没有调用方**：lumen Java 禁止回落到 demo（D12），demo Java 和 demo 前端都没接分析接口，demo AI 只开了 `/internal/*`。另外 demo AI 的算法下游和回调都指向 lumen，和 `ARCH-MSG-KAFKA` 图上画的 demo 路径不一致。需要架构师二选一：给 demo 补 Java 调用方，或者把原型这一路从验收和图里拿掉。
2. **旧 RabbitMQ 口令**：helm 历史 revision（≤16）和 git 历史里仍有明文。要彻底消除，得靠运维改口令或下线旧中间件。

### 遗留（不属 Kafka 迁移范围）

- 企业检索 `search/query` 和 `search/by-codes` 返回 500，`e2e:chain-gold` 因此长期是红的。
- ai-py 没有注入 `GKX_ES_HOST`，推荐模块会回落到 10.50.11.76；集群里 Milvus 地址同样不可达，影响产业锚点和政策 enrich。
- demo-svc-platform 的 `backend:image:*` 长期失败（找不到 jar），所以 helm:deploy 走不通。
- `enterprise_risk_summary` 是空表；多份 k8s 清单里有明文 MySQL 口令。
