# E-PLATFORM-P0-KAFKA-DEVOPS-L01 · Kafka 建 4 个 topic；demo-svc-platform helm 改为 Kafka；运维手记删去旧总线与口令

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 状态由监管人改，本叶未调用 task-registry MCP。本文件未提交编排仓，由监管人提交。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单强度一致。只改派单点名的 values / 注释 / 手记行，没有新增模板或脚本进仓。可观测、D12、D13、handoff 没有用 YAGNI 跳过。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本次会话未挂载。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `ARCH-MSG-KAFKA` |
| 图 diff | 无变化。按基线 §1.1 施工：4 个 topic 落地到 `10.50.11.76:9092`；`demo-platform-ai-py` → `gkx.demo.analysis.result`，`demo-platform-worker-py` 组 `demo-ai-worker`、死信 `gkx.demo.analysis.result.dlq` 写进 helm。禁止事项不变。 |
| 会签态 | `draft`（抄基线 §1.1 frontmatter `signoff_status: draft`，未改） |
| 说明 | 没有另画图。`demo-platform-worker-py` 这条边在 helm 里已接好变量，但 `values-demo.yaml` 仍关闭（见偏离）。 |

## 范围与实现

依据：`E-PLATFORM-P0-KAFKA-RMQ-L01.md`（环境变量表、topic 参数、按仓替换要点）、`E-PLATFORM-P0-KAFKA-ALGO-L01.md`（镜像读取的变量）、基线 §1.1 与 D13。

### 第一步：Kafka 建 topic

本机 Python 3.12 + aiokafka 0.14.0，`AIOKafkaAdminClient`，PLAINTEXT 无认证。脚本放在 `%TEMP%\gkx_kafka_topics.py`，不进任何仓，不含口令。逻辑：先 `list_topics`，已存在的跳过；不存在的按 1 分区、副本数 1、`max.message.bytes=67108864` 创建；再用 `describe_topics` 和 `describe_configs` 确认，并只读查询 broker 配置。没有删除或修改 `zp-tts-demo`，没有发布任何消息，没有改 broker 配置。

### 第二步：`demo-svc-platform` helm

- `helm/gkx-platform/values.yaml`
  - `aiPy.env`：删去 `GKX_RABBITMQ_URL`，换成 `KAFKA_BOOTSTRAP_SERVERS=10.50.11.76:9092`、`KAFKA_TOPIC=gkx.demo.analysis.result`。
  - `workerPy.env`：删去 `GKX_RABBITMQ_URL`，换成 `KAFKA_BOOTSTRAP_SERVERS`、`KAFKA_TOPIC=gkx.demo.analysis.result`、`KAFKA_DLQ_TOPIC=gkx.demo.analysis.result.dlq`、`KAFKA_GROUP_ID=demo-ai-worker`、`KAFKA_MAX_IN_FLIGHT=2`、`KAFKA_MAX_RETRIES=3`。
  - 相关段落注释改为 Kafka。MySQL / ES / 对象存储 / Java callback 行未动。
- `helm/gkx-platform/values-demo.yaml`：`workerPy.enabled` 保持 `false`，注释改为“代码已读 KAFKA_*（bb9bab0），topic 已建，镜像未核实”。
- `helm/gkx-platform/templates/ai-service-py.yaml`、`ai-worker-py.yaml`：头注释 RabbitMQ 改为 Kafka，模板逻辑未动。

### 第三步：两份运维手记

`demo-svc-platform/OTEL_INFRA_OPS_HANDOFF.md` 与 `lumen-svc-platform/OTEL_INFRA_OPS_HANDOFF.md`（改动前两份字节相同，改法相同）：

- 删去 §0.2 组件表里旧总线那一行（主机、管理台、口令）。
- 删去 §0.3 端口表 5672 / 15672 那一行。
- “MySQL / … / Neo4j 等密码”一句去掉旧总线名，并补一行：消息总线已改为 Kafka `10.50.11.76:9092`（D13，见基线 §1.1）。
- 未重写 git 历史；commit message 与本文件不含任何口令。MySQL root 与业务库口令行未动。

## 问题清单

- broker 级 `message.max.bytes` / `replica.fetch.max.bytes` 都是 10MiB，低于 64MiB（见验收证据与遗留风险）。按派单只报告、未改。
- broker `auto.create.topics.enable=true`。
- 本机无 kubectl 可用凭证、无 helm、`harbor.test.com` 解析不到，无法确认 demo Worker 镜像已按 bb9bab0 构建。
- 本机 `GKX_GITLAB_TOKEN` 为空，流水线未查。

## 偏离

- **`workerPy.enabled` 保持 false**：`demo-svc-topic-py` 的 `origin/dev` 已含 `bb9bab0`（`git branch -r --contains bb9bab0` → `origin/dev`，且为 HEAD）。该仓 CI 以 commit 短 sha 打镜像 tag 并在 deploy 时 `kubectl set image`。但本叶无法核实该流水线是否成功、镜像是否已推送：本机没有 helm；在 `10.50.69.111`（node01）上只读执行 `kubectl get deploy` 返回未认证，`sudo kubectl --kubeconfig /etc/kubernetes/admin.conf` 超时；本机解析不到 `harbor.test.com`；GitLab token 为空。`values.yaml` 中 `workerPy.image.tag` 是 `latest`，不是固定 sha，无法从 values 判断。按派单“确认不了就保持 false”。
- 手记里没有保留“不再使用 RabbitMQ”这类字样，以保证仓内检索清零；说明行只写 Kafka 与 D13。

## 修改内容

| 仓 | commit | 文件 | 已推 origin/dev |
|----|--------|------|----------------|
| `demo-svc-platform` | `48d025a3a82412cc33bad4a79cb4db4c6628ac36` | `helm/gkx-platform/values.yaml`、`values-demo.yaml`、`templates/ai-service-py.yaml`、`templates/ai-worker-py.yaml`、`OTEL_INFRA_OPS_HANDOFF.md`（5 文件，+27 / −16） | ✅ `git log origin/dev -1` = 该 SHA |
| `lumen-svc-platform` | `cb71ecc8aad9ce03c22a92275d4a2e43f2d0feb6` | `OTEL_INFRA_OPS_HANDOFF.md`（+2 / −3） | ✅ `git log origin/dev -1` = 该 SHA |

commit message：`chore(helm): 消息总线改为 Kafka，去掉 RabbitMQ [agent:devops-agent]`、`docs(ops): 运维手记删去 RabbitMQ 与口令 [agent:devops-agent]`，正文写任务 ID，不含口令。两仓开工前 `git pull --rebase origin dev` 均为 Already up to date，推送未被拒。

## 验收证据

### topic 创建与配置确认（2026-10-18 00:2x，本机输出原文）

```
before: ['__consumer_offsets', 'zp-tts-demo']
create_topics: [('gkx.analysis.result', 0, None), ('gkx.analysis.result.dlq', 0, None), ('gkx.demo.analysis.result', 0, None), ('gkx.demo.analysis.result.dlq', 0, None)]
after: ['__consumer_offsets', 'gkx.analysis.result', 'gkx.analysis.result.dlq', 'gkx.demo.analysis.result', 'gkx.demo.analysis.result.dlq', 'zp-tts-demo']
describe: gkx.analysis.result err 0 partitions 1 replicas [1]
describe: gkx.analysis.result.dlq err 0 partitions 1 replicas [1]
describe: gkx.demo.analysis.result err 0 partitions 1 replicas [1]
describe: gkx.demo.analysis.result.dlq err 0 partitions 1 replicas [1]
topic cfg: gkx.analysis.result max.message.bytes = 67108864
topic cfg: gkx.analysis.result.dlq max.message.bytes = 67108864
topic cfg: gkx.demo.analysis.result max.message.bytes = 67108864
topic cfg: gkx.demo.analysis.result.dlq max.message.bytes = 67108864
```

4 个 topic 此前都不存在，本次全部新建，错误码 0。`zp-tts-demo` 未动。

### broker 上限（只读，broker id 1）

```
message.max.bytes = 10485760        (10MiB)
replica.fetch.max.bytes = 10485760  (10MiB)
auto.create.topics.enable = true
socket.request.max.bytes = 104857600 (100MiB)
```

结论：broker 级两个值 **< 64MiB**。topic 级 `max.message.bytes=67108864` 会覆盖 broker 的 `message.max.bytes`，所以这 4 个 topic 的写入上限是 64MiB；单 broker、副本数 1，不存在 follower 复制，`replica.fetch.max.bytes` 对这 4 个 topic 实际不生效。`socket.request.max.bytes` 100MiB ≥ 64MiB。未在集群上做大消息真实发布验证。

### 检索清零

- `demo-svc-platform`：`rg -n -i "rabbitmq|amqp|5672|GKX_RABBITMQ|guest" --glob "!db/**" .` 无命中（exit 1）；全仓 `rg -c -i "rabbitmq|amqp|GKX_RABBITMQ"` 无命中（exit 1）。`5672` 剩余命中只在 `db/99gkxx_bi.sql`，是经纬度与 ID 中的数字。
- `lumen-svc-platform`：`rg -i "rabbitmq|amqp|:5672|GKX_RABBITMQ|15672"` 只剩 `db/99gkxlumenx_bi.sql` 的经纬度数字。

### values 取值

本机 PyYAML 加载 `values.yaml`：

```
aiPy ['KAFKA_BOOTSTRAP_SERVERS=10.50.11.76:9092', 'KAFKA_TOPIC=gkx.demo.analysis.result']
workerPy ['KAFKA_BOOTSTRAP_SERVERS=10.50.11.76:9092', 'KAFKA_TOPIC=gkx.demo.analysis.result', 'KAFKA_DLQ_TOPIC=gkx.demo.analysis.result.dlq', 'KAFKA_GROUP_ID=demo-ai-worker', 'KAFKA_MAX_IN_FLIGHT=2', 'KAFKA_MAX_RETRIES=3']
```

`values-demo.yaml` → `workerPy: {'enabled': False}`。变量名与 ALGO 单所述镜像读取一致（AI 进程 2 个、Worker 6 个）。

## 测试结果

- topic 创建脚本一次成功（首次因 aiokafka 0.14 的 `ConfigResource` 导入路径报 ImportError，未连 broker，修正导入后重跑）。
- YAML 解析通过。本机无 helm，未跑 `helm lint` / `helm template`；该仓 `helm:lint` job 对 `helm/**` 变更在 dev 自动运行，结果未查。
- 未在集群发布业务消息，未做消费冒烟。

## 遗留风险

- **broker 级 10MiB**：若以后新建 topic 未带 `max.message.bytes` 覆盖，或改为多副本，大结果会被拒。扩副本前需运维把 `replica.fetch.max.bytes`（及按需 `message.max.bytes`）调到 ≥ 64MiB。本叶未改 broker。
- **自动建 topic 开启**：拼错 topic 名会被静默按 broker 默认（10MiB、默认分区）建出来，排障时注意。
- **helm 改动尚未生效**：本仓 `helm:chart` / `helm:deploy` 均为 dev 手动 job，需要有人点 `helm:chart`（只改 chart，钉住现网 Python 镜像 tag）。另外 `demo-svc-topic-py` 自己的 CI 每次 deploy 都 apply 其 `k8s/*.yaml`（已是 KAFKA_*），两边 env 现已一致。
- **demo Worker 未打开**：`gkx.demo.analysis.result` 目前没有消费者，demo AI 进程发布的 `task_completed` 会积压在 topic 里，直到 Worker 打开。打开前先核实 `gkx-ai-worker:bb9bab0`（或更新）已在 Harbor、`demo-svc-topic-py` dev 流水线绿，再把 `values-demo.yaml` 的 `workerPy.enabled` 改为 true 并点 `helm:chart`。
- **旧口令仍在 git 历史**：两份手记的旧口令只从现行文件删除，未重写历史。若该中间件仍在运行，建议运维改口令或下线。
- **流水线未查**：token 为空，两仓本次 push 的 pipeline 需人工在 GitLab 查看。

## CI/CD（必填）

- 分支：两仓均为 `dev`
- commit：demo-svc-platform `48d025a3a82412cc33bad4a79cb4db4c6628ac36`；lumen-svc-platform `cb71ecc8aad9ce03c22a92275d4a2e43f2d0feb6`
- pipeline URL / ID：**未查**（`gkx-orchestration/.env` 的 `GKX_GITLAB_TOKEN` 为空，本机无 glab）
- 部署 namespace / 镜像 tag：demo-svc-platform 的 helm 部署为手动 job（ns `zhipu-tts`），本叶未触发；lumen-svc-platform 只改文档
- K8s rollout：未执行
- dev 测试 URL / 命令与结果：Kafka admin 创建与 describe（见验收证据）

## 可观测性

- OTEL_SERVICE_NAME：未改；`ai-service-py.yaml` / `ai-worker-py.yaml` 的 `commonOtelEnv` 未动
- traceId（dev 抽样）：无（未部署）
- Tempo / Loki：无新数据

## 涉及文件

- `${GKX_ROOT}/repos/demo-svc-platform/helm/gkx-platform/values.yaml`
- `${GKX_ROOT}/repos/demo-svc-platform/helm/gkx-platform/values-demo.yaml`
- `${GKX_ROOT}/repos/demo-svc-platform/helm/gkx-platform/templates/ai-service-py.yaml`
- `${GKX_ROOT}/repos/demo-svc-platform/helm/gkx-platform/templates/ai-worker-py.yaml`
- `${GKX_ROOT}/repos/demo-svc-platform/OTEL_INFRA_OPS_HANDOFF.md`
- `${GKX_ROOT}/repos/lumen-svc-platform/OTEL_INFRA_OPS_HANDOFF.md`
- Kafka `10.50.11.76:9092`：新建 4 个 topic（集群资源，非仓文件）
- `agent-delivery/agent-handoffs/平台基建-PLATFORM/E-PLATFORM-P0-KAFKA-DEVOPS-L01.md`（本文件，未提交）

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未改 Java 与 Python 代码 |
| 调用链 前端 → Java → Python `/internal/*` | ✅ Java callback 与 webhook 路径未动；总线只在 AI 进程与 Worker 之间 |
| 图谱 Nebula | ✅ 未改图库配置；手记中图库行未动 |
| 可观测 | ✅ `commonOtelEnv` 与 OTEL 相关 values 未动 |
| CI/CD | ✅ 两仓 push `origin/dev`；helm 部署为手动 job，结果未查（见 CI/CD） |
| demo 不污染 lumen | ✅ 两仓各自提交，无 merge；正式与原型 topic 分开建 |
| 方案 A / 前端只调 Java | ✅ 未改网关与前端 |
| 数据走 ADS | ✅ 未改库配置，MySQL root 与业务库口令行未动 |
| D8 / D9 / D10 | ✅ 无页面、指标、交互改动 |
| D12 | ✅ demo helm 只用原型 topic / 死信 / 组 `demo-ai-worker`，不与正式 `gkxlumen-ai-worker` 共用；lumen-svc-platform 只改文档，未引用任何 `demo-*` 服务 |
| D13 | ✅ 4 个 topic 按 D13 名称建在 `10.50.11.76:9092`，单条上限 64MiB；demo-svc-platform 已无 `GKX_RABBITMQ_*` / AMQP；手记删去旧总线行 |
| 口令红线 | ✅ 脚本、commit、本文件不含中间件口令；未改 `.gitignore`；未 force push；未碰 `E:\gkx-lumen\` |

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 120000 |
| model_used | claude-opus-5.5 |
| actual_cost | 3.24 |
| cost_warn | green |

口径：无 Console 精确 in/out，按会话估算 120000 tokens。预算表 C 旗舰档（输入 $15/M、输出 $75/M），80/20 比例：`120000×0.8×15/1e6 + 120000×0.2×75/1e6 = 1.44 + 1.80 = 3.24`。低于 $10 暂停线。`source: session_estimate`。

## Coordinator 复核与部署（2026-10-18，agent:coordinator-agent）

GitLab token 已补，以下替代上文"流水线未查 / 未部署"各条：

- **Topic 复核**：`10.50.11.76:9092` 上 4 个 `gkx.*` topic 均在。
- **算法流水线**：lumen-topic-py pipeline 2547（`21cc71e`）与 demo-svc-topic-py pipeline 2548（`bb9bab0`）的 smoke 与镜像作业全绿。coordinator 手动触发部署：
  - lumen job 13295 `deploy:ai-py`：`gkxlumen-platform-ai-py` successfully rolled out。
  - lumen job 13296 `deploy:ai-worker`：`gkxlumen-platform-ai-worker` successfully rolled out。
  - demo job 13302 `deploy:ai-py`：`demo-platform-ai-py` successfully rolled out。
  - demo job 13303 `deploy:worker-py`：`demo-platform-worker-py` successfully rolled out。
  - 部署后探针日志里的 `cannot exec into a container in a completed pod` 是在 exec 已结束的旧 pod，作业状态为 success。
- **消费冒烟**：Kafka `list_consumer_groups` 返回 `gkxlumen-ai-worker`、`demo-ai-worker`，两个 Worker 已上线订阅。因此上文"demo Worker 未打开、topic 积压"不成立。
- **demo Worker 由谁部署**：由 demo-svc-topic-py 自己的 `k8s/dev-worker-py.yaml` 部署，含 6 个 KAFKA_* 变量。helm `values-demo.yaml` 的 `workerPy.enabled=false` **保持**，打开会多出一份重复 Worker。`helm:chart` 不点，现网不依赖它。
- **平台流水线**：
  - demo-svc-platform pipeline 2549（`48d025a3`）：`helm:lint` success。7 个 `backend:image:*` 里 6 个失败，原因是 `ADD gkx-demo-a/target/*.jar` 找不到构建产物，上一条 pipeline 2529 同样失败，是既有问题，与本叶只改 helm 和文档无关。
  - lumen-svc-platform pipeline 2550（`cb71ecc8`）复核时还在跑镜像作业，本叶只改文档。
- **签收**：用户（human:淮政玮）2026-10-18 在聊天中授权"不需要我会签，Kafka 全部任务做完前不打扰"，coordinator 据此代签收。
