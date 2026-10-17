# E-PLATFORM-P0-KAFKA-ALGO-L01 · 两个 Python 仓的消息总线改为 Kafka（aiokafka），去掉 aio-pika

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 状态由监管人改，本叶未调用 task-registry MCP。编排仓本文件未提交，由监管人提交。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单强度一致。未用 YAGNI 跳过可观测、D12、D13、handoff。偏离见下文「偏离」：AI 进程只读它用得到的两个 Kafka 变量。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本次会话未挂载。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `ARCH-MSG-KAFKA` |
| 图 diff | 无变化。按基线 §1.1 施工，没有另画图。 |
| 会签态 | `draft`（抄基线 §1.1 frontmatter，未改） |
| 说明 | 发布者 `gkxlumen-platform-ai-py` / `demo-platform-ai-py`，消费者 `gkxlumen-platform-ai-worker` / `demo-platform-worker-py`，topic、死信 topic、消费组与图一致。 |

## 范围与实现

依据：`E-PLATFORM-P0-KAFKA-RMQ-L01.md` 的按仓文件表、替换要点、环境变量表；基线 §1.1 与 D13。

两仓改法相同，各自提交，未互相 merge。demo 仓中改动前与 lumen 字节相同、且不含平面名的文件（`mq_producer.py`、`gkx_ai_worker/main.py`、`consumer.py` 注释、`callback.py` 注释、`Dockerfile.worker`、`requirements.txt`、两个测试文件）同步了文件内容；含 topic / 组名的文件在 demo 仓按原型名单独改写。

| 仓 | topic | 死信 topic | 消费组 | k8s 清单 |
|----|-------|-----------|--------|---------|
| `lumen-topic-py` | `gkx.analysis.result` | `gkx.analysis.result.dlq` | `gkxlumen-ai-worker` | `k8s/dev-ai-py.yaml`、`k8s/dev-ai-worker.yaml` |
| `demo-svc-topic-py` | `gkx.demo.analysis.result` | `gkx.demo.analysis.result.dlq` | `demo-ai-worker` | `k8s/dev-ai-py.yaml`、`k8s/dev-worker-py.yaml` |

改动要点：

- `conf/settings.yaml`：`rabbitmq` 段换成 `kafka` 段（bootstrap `10.50.11.76:9092`、topic、dlq_topic、group_id、max_in_flight=2、max_retries=3），不写口令。
- `gkx_ai_service/deps.py`：读 `KAFKA_BOOTSTRAP_SERVERS`、`KAFKA_TOPIC`。新增常量 `KAFKA_MAX_MESSAGE_BYTES=67108864` 和函数 `kafka_security_kwargs()`：没有 `KAFKA_SASL_PASSWORD` 时用 PLAINTEXT，有则用 SASL_PLAINTEXT，口令只从环境变量读。`GKX_RABBITMQ_*` 和本机 5672 回落已删除。
- `gkx_ai_worker/deps.py`：读全部 6 个 `KAFKA_*` 变量，默认值用本仓的 topic 和组名。
- `gkx_ai_service/mq_producer.py`：`AIOKafkaProducer`，`acks="all"`，`max_request_size=67108864`，首次发布时懒加载，用锁防并发。函数名 `publish_analysis_result` 不变，失败返回 False。`callback.py` / `result_delivery.py` 的现有语义不变：发布失败 → HTTP 503；无 result → 422；不向 Java 转发没有指针的结果。消息 key 为 task_id，header 带 task_id、analysis_type。正文 JSON 结构不变。
- `gkx_ai_worker/main.py`：`AIOKafkaConsumer` 按消费组拉取，`enable_auto_commit=False`，`max_partition_fetch_bytes` 和 `fetch_max_bytes` 均为 67108864。每次 `getmany` 最多拉 `KAFKA_MAX_IN_FLIGHT` 条并发处理。`handle_record` 的处理规则：
  - 处理成功：提交位点。
  - 处理失败或抛异常：重试次数小于 3 时，写入或递增 header `x-retry-count`，发回同一 topic，然后提交位点；达到 3 次后发到死信 topic，然后提交位点。
  - 坏 JSON（或不是 JSON 对象）：直接进死信 topic，然后提交位点。
  - 重投或死信发布本身失败：只提交到第一条失败之前，`seek` 回失败位点，等 5 秒再拉（至少一次语义）。
  - `consumer.py` 处理逻辑没有改（camelCase、对象存储、HTTP 转发 Java），只改了模块注释。
- `gkx_ai_worker/__init__.py`、`docker/Dockerfile.worker`、`gkx_ai_service/views/callback.py` 中的注释改为 Kafka，逻辑未动。
- k8s：`GKX_RABBITMQ_URL` 已删除。Worker 清单写入 6 个 `KAFKA_*` 变量；AI 清单写入 `KAFKA_BOOTSTRAP_SERVERS` 和 `KAFKA_TOPIC`。MySQL、ES、对象存储、OTel 等行未动。
- `requirements.txt`：删除 `aio-pika`，加入 `aiokafka>=0.11.0`（本机测试用的是 0.14.0）。
- `.env.example`：补充 6 个 `KAFKA_*` 变量，不写口令。

## 偏离

- **AI 进程只读 2 个 Kafka 变量**：派单要求两份 deps 都读 6 个变量，两份 k8s 都换成 KAFKA_* 变量。AI 进程只发布，用不到 DLQ、组、in-flight、重试次数，所以 `gkx_ai_service/deps.py` 和 `dev-ai-py.yaml` 只放 `KAFKA_BOOTSTRAP_SERVERS`、`KAFKA_TOPIC`；Worker 侧 6 个变量都有。如需补齐，在 AI 清单里加 4 行即可，代码不用改。
- **另加了两个可选的非密钥变量**：SASL PLAIN / SCRAM 除口令外还需要用户名和机制，所以增加 `KAFKA_SASL_USERNAME`（默认空）和 `KAFKA_SASL_MECHANISM`（默认 `PLAIN`）。它们只在设置了 `KAFKA_SASL_PASSWORD` 时生效。目前探测结果是 PLAINTEXT 可连，本次没有用到。
- **callback.py、consumer.py 动了注释**：为了让 rg 检索清零，删掉了注释里的 RabbitMQ 字样，代码逻辑未变。
- Worker 处理异常的语义有变化：原来是 `nack(requeue=True)` 无限重排，现在计入重试次数，最多 3 次后进死信，与 handoff 写定的失败语义一致。

## 问题清单

- 4 个目标 topic 在集群上都还不存在（见验收证据）。
- 本机无 glab，`.env` 中 `GKX_GITLAB_TOKEN` 为空（API 返回 401），未能查询流水线。

## 修改内容

| 仓 | commit | 已推 origin/dev |
|----|--------|----------------|
| `lumen-topic-py` | `21cc71e8ec25ff1721a199dbdeba10011c14ac98` | ✅（`git log origin/dev -1` 确认） |
| `demo-svc-topic-py` | `bb9bab0514f1cc31bb49d298198f3d0930774f4f` | ✅（`git log origin/dev -1` 确认） |

每仓 15 个文件：`.env.example`、`conf/settings.yaml`、`docker/Dockerfile.worker`、`gkx_ai_service/{deps.py,mq_producer.py,views/callback.py}`、`gkx_ai_worker/{__init__.py,consumer.py,deps.py,main.py}`、两份 k8s 清单、`requirements.txt`、`tests/test_analysis_callback.py`，以及新增的 `tests/test_worker_retry_dlq.py`。

commit message：`feat(mq): 消息总线改为 Kafka，去掉 aio-pika [agent:algorithm-agent]`，正文写了任务 ID，没有口令。

## 验收证据

- **rg 清零**：两仓执行 `rg -n -i "rabbitmq|aio_pika|aio-pika|amqp|5672|GKX_RABBITMQ"`，无命中（exit 1）。
- **配置取值**：本机加载配置后，lumen 为 `10.50.11.76:9092 gkx.analysis.result gkx.analysis.result.dlq gkxlumen-ai-worker 2 3`，demo 为 `10.50.11.76:9092 gkx.demo.analysis.result gkx.demo.analysis.result.dlq demo-ai-worker 2 3`。两边 topic 和组不重叠。
- **发布失败路径**：把 `KAFKA_BOOTSTRAP_SERVERS` 设为 `127.0.0.1:1` 后调用 `publish_analysis_result`，返回 False，日志为 `KafkaConnectionError: Unable to bootstrap`。callback 测试覆盖了 False → 503。
- **Kafka 只读探测**（2026-10-18 本机，aiokafka 0.14.0，PLAINTEXT，只做 metadata 与 topic 列表，没有创建 topic，也没有发布消息）：
  - 连通：✅ broker `1 @ 10.50.11.76:9092`，PLAINTEXT 无需认证即可取 metadata。
  - 集群现有 topic 1 个：`zp-tts-demo`。
  - `gkx.analysis.result`：**不存在**
  - `gkx.analysis.result.dlq`：**不存在**
  - `gkx.demo.analysis.result`：**不存在**
  - `gkx.demo.analysis.result.dlq`：**不存在**
  - 为避免在 broker 开启自动建 topic 时误建，没有做真实发布冒烟。

## 测试结果

- 相关测试：每仓 `pytest tests/test_analysis_callback.py tests/test_worker_retry_dlq.py tests/test_result_delivery.py`，lumen 26 passed，demo 26 passed。
  - callback：发布成功 → 200 + accepted；发布失败 → 503 且不转发 Java；无 result 或空 result → 422。
  - `test_worker_retry_dlq.py`（新增 5 例，用假生产者，不引入框架）：成功不重投；第一次失败写入 `x-retry-count=1`；`retry=1` 时重投同一 topic 并递增为 2；`retry=3` 时进死信；坏 JSON 进死信。
- 全量 `pytest tests`：
  - lumen：改动前 7 failed / 231 passed，改动后 7 failed / 236 passed。
  - demo：改动前 5 failed / 178 passed，改动后 5 failed / 183 passed。
  - 失败用例在改动前后完全相同，都是已有的 `test_qa_passthrough_fixes`、`test_query_tree_dsl`、`test_meta_dimension_endpoints`（lumen）检索 / 元数据用例，与本叶无关，本叶未处理。

## 遗留风险

- **topic 尚未创建**：DEVOPS 单 `E-PLATFORM-P0-KAFKA-DEVOPS-L01` 还没有创建 4 个 topic。如果集群不自动建 topic，生产者等 metadata 超时（aiokafka 默认约 40s）后发布失败，`task_completed` 回调返回 **503**，算法侧按非 2xx 重试；Worker 订阅一个不存在的 topic 时拉不到消息。如果集群自动建 topic，会按 broker 默认参数建（`max.message.bytes` 很可能是 1MB），大结果会因超限返回 503。两种情况都要等 DEVOPS 单按 1 分区、`max.message.bytes=67108864` 预先建好 topic。
- **发布超时可能长于算法侧 Webhook 超时**：首发等 metadata 时，503 可能比算法 HTTP 超时晚返回，算法侧看到的是超时而不是 503，但同样会重试。topic 建好后不会出现这种情况。
- **镜像发布顺序**：新镜像只读 `KAFKA_*`。`demo-svc-platform` helm 的 `values.yaml` 仍注入 `GKX_RABBITMQ_URL`，新镜像会忽略它，并按 `settings.yaml` 默认值连 Kafka；改 helm、打开 `workerPy` 归 DEVOPS 单。
- **64MiB 上限**：超过 64MiB 的 result 发布失败，返回 503。
- **至少一次投递**：重投或死信发布失败时会回退位点，同一批里排在失败记录之后、已经处理成功的记录会再处理一次。下游（对象存储覆盖写、Java 回调）需要能承受重复。重试会立即发回同一 topic，没有延迟退避，与原 RabbitMQ 行为一致。
- **流水线未查**：没有 glab，token 为空。需要人工在 GitLab 查看两仓 dev 上这两个 SHA 的流水线和 K8s rollout。

## CI/CD（必填）

- 分支：两仓均为 `dev`
- commit：lumen `21cc71e8ec25ff1721a199dbdeba10011c14ac98`；demo `bb9bab0514f1cc31bb49d298198f3d0930774f4f`
- pipeline URL / ID：**未查**（本机无 glab；`gkx-orchestration/.env` 的 `GKX_GITLAB_TOKEN` 为空，GitLab API 返回 401）
- 部署 namespace / 镜像 tag：未查（推送后由 CI 触发，tag 为 commit sha）
- K8s rollout：未查
- dev 测试 URL / 命令与结果：本机 pytest（见测试结果）；Kafka 只读探测（见验收证据）

## 可观测性

- OTEL_SERVICE_NAME：未改（`gkxlumen-ai-service` / `gkxlumen-ai-worker`；demo 为 `gkx-ai-service` / `gkx-ai-worker`）
- instrument：保留。`Dockerfile.worker` 的 `ENTRYPOINT ["opentelemetry-instrument"]` 未动，k8s 中的 OTEL_* 行未动，日志仍走 `gkx_common.observability`
- traceId（dev 抽样）：无（未部署验证）
- Tempo / Loki：无新数据

## 涉及文件

- `${GKX_ROOT}/repos/lumen-topic-py/`：上表 15 个文件
- `${GKX_ROOT}/repos/demo-svc-topic-py/`：上表 15 个文件（k8s 为 `dev-ai-py.yaml`、`dev-worker-py.yaml`）
- `agent-delivery/agent-handoffs/平台基建-PLATFORM/E-PLATFORM-P0-KAFKA-ALGO-L01.md`（本文件，未提交）

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 只改 Python 仓，没有在 Java 增加任何代码 |
| 调用链 前端 → Java → Python `/internal/*` | ✅ Webhook 入口和 Java 回调路径不变；总线只在 AI 进程和 Worker 之间 |
| 图谱 Nebula | ✅ 未改图库配置 |
| 可观测 | ✅ opentelemetry-instrument、OTEL_* 环境变量和日志封装保留 |
| CI/CD | ✅ 两仓 push `origin/dev` 触发流水线；结果未查（见 CI/CD） |
| demo 不污染 lumen | ✅ 两仓各自 commit，没有 merge，也没有拷贝 git 历史 |
| 方案 A / 前端只调 Java | ✅ 未改网关与前端 |
| 数据走 ADS | ✅ 未改库配置，MySQL 相关行未动 |
| D8 / D9 / D10 | ✅ 无页面、指标、交互改动 |
| D12 | ✅ lumen 只用 `gkxlumen-*` 服务名和正式 topic / 组；demo 只用原型 topic / 组；两边不共用；lumen 不引用任何 `demo-*` 服务 |
| D13 | ✅ 运行时只连 Kafka `10.50.11.76:9092`；两仓 rabbitmq / aio-pika / amqp / 5672 / GKX_RABBITMQ 已清零；单条上限 64MiB；口令只从环境变量读，没有进 git |
| 口令红线 | ✅ commit、代码、本 handoff 都没有中间件口令；未改 `.gitignore`；依赖只改了 `requirements.txt` |

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 200000 |
| model_used | claude-opus-5.5 |
| actual_cost | 5.40 |
| cost_warn | green |

口径：没有 Console 精确 in/out，按会话估算 200000 tokens。用预算表 C 旗舰档（输入 $15/M、输出 $75/M），按 80/20 比例：`200000×0.8×15/1e6 + 200000×0.2×75/1e6 = 2.40 + 3.00 = 5.40`。低于 $10 暂停线。`source: session_estimate`。
