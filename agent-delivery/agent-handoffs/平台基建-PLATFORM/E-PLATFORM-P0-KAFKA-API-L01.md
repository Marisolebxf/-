# E-PLATFORM-P0-KAFKA-API-L01 · 确认 Java 不接消息总线

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 首次派出的子智能体工具通道故障，未扫到任何文件。coordinator 会话用同一份派单范围重做只读扫描。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 零代码。扫描结论为不需要改 Java，也不加 `spring-kafka`。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `ARCH-MSG-KAFKA` |
| 图 diff | 无变化。图中 Java（`gkxlumen-topic-async-service`）只收 HTTP，与扫描结果一致。 |
| 会签态 | `draft` |

## 范围与实现

只读扫描 `lumen-svc-platform`、`demo-svc-platform` 全仓（Java 源码、`pom.xml`、Nacos / `application*.yml`、helm）。检索词（不区分大小写）：`rabbit`、`amqp`、`kafka`、`:5672`、`:9092`。

### 命中清单

| 仓 | 文件 | 归属 | 处理 |
|---|---|---|---|
| `lumen-svc-platform` | `OTEL_INFRA_OPS_HANDOFF.md` L36 / L47 / L57 | 文档（旧运维表，主机 `192.168.88.48`，含口令） | 归 `E-PLATFORM-P0-KAFKA-DEVOPS-L01` 删除口令行。本文不抄口令 |
| `demo-svc-platform` | `OTEL_INFRA_OPS_HANDOFF.md` L36 / L47 / L57 | 同上 | 同上 |
| `demo-svc-platform` | `helm/gkx-platform/values.yaml` L681、L718–721、L747、L762–764 | Python 服务 `aiPy` / `workerPy` 段的 `GKX_RABBITMQ_URL` 与注释 | 归 DEVOPS 单 |
| `demo-svc-platform` | `helm/gkx-platform/values-demo.yaml` L64 | Python Worker 注释 | 归 DEVOPS 单 |
| `demo-svc-platform` | `helm/gkx-platform/templates/ai-worker-py.yaml` L3、`ai-service-py.yaml` L5 | Python 模板注释 | 归 DEVOPS 单 |

Java 源码、`pom.xml`、Nacos / `application*.yml`：**零命中**。两仓没有 AMQP 客户端，也没有 Kafka 客户端。

### 回调契约

- `lumen-svc-platform/gkxlumen-topic-async-service/gkxlumen-topic-async-service-biz/.../controller/analysis/AnalysisTaskController.java`：类级 `@RequestMapping("/topic/v1/analysis")`（L55），`@PostMapping("/callback/eval")`（L393）、`/callback/risk`（L406）、`/callback/recommend`（L419）。HTTP 入口存在，契约不变。
- `lumen-svc-platform/helm/gkxlumen-platform/values.yaml` L511–512：`GKXLUMEN_TOPIC_ASYNC_PYTHON_AI_BASE_URL = http://gkxlumen-platform-ai-py:8081`，由 `TopicAsyncAiPythonRoutingClient.java` 读取。符合 D12。

## 结论

Java 不接消息总线。本叶零代码，不新增 `spring-kafka`。仓内 RabbitMQ 残留全部在 Python 服务的 helm 段和运维文档，已由 `E-PLATFORM-P0-KAFKA-DEVOPS-L01` 覆盖。

## 偏离

- 首派子智能体工具故障未产出；本次扫描由 coordinator 会话执行，范围与派单一致。

## 测试结果

- `rg -i "rabbit|amqp|kafka|:5672|:9092"` 两仓：结果见命中清单，Java 侧零命中。
- 回调路由与 AI base URL：见上，均已定位到文件和行。

## 遗留风险

- 无 Java 侧风险。
- 两份 OTEL 手记里的口令仍在现行文件和 git 历史中，等 DEVOPS 单删除现行行；历史不重写。

## 产物清单

- 本 handoff。业务仓零改动。

## 验收证据

- 命中清单与回调位置如上。

## CI/CD（必填）

- 分支 / commit：业务仓无提交
- pipeline：`cicd: skip`（只读探针）
- K8s rollout：未执行

## 可观测性（建议）

- 未改。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ Java 无算法、无总线客户端 |
| 调用链 前端 → Java → Python `/internal/*` | ✅ 回调仍是 HTTP |
| 图谱 Nebula | ✅ 未涉及 |
| 可观测 | ✅ 未改 |
| CI/CD | ✅ `cicd: skip` |
| demo 不污染 lumen | ✅ 只读 |
| 方案 A | ✅ 未改网关 |
| 数据走 ADS | ✅ 未涉及 |
| D8 / D9 / D10 | ✅ 无页面 / 指标 / 交互 |
| D12 | ✅ AI base URL 指向 `gkxlumen-platform-ai-py`，无 demo 回落 |
| D13 | ✅ Java 不连总线 |

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 60000 |
| model_used | claude-opus-5.5 |
| actual_cost | 0.36 |
| cost_warn | green |

口径：首派子智能体约 45000（工具故障）+ coordinator 重扫约 15000。B 档单价、80/20：`60000×0.8×3/1e6 + 60000×0.2×15/1e6 = 0.36`。`source: session_estimate`。
